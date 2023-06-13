import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import cumtrapz
from ahrs.filters import Madgwick
import quaternion  # new library for quaternion operations

# Load the data
df = pd.read_csv("datasets/raw_data_sien")
# select rows where entry num is  5
df = df[df["entry_num"] == 15]
from ahrs.filters import Madgwick
from ahrs.common.orientation import acc2q
from ahrs.common import DEG2RAD, Quaternion
import numpy as np
import matplotlib.pyplot as plt

# Assume df is your dataframe and has columns 'Time (s)', 'X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)', 'X (rad/s)', 'Y (rad/s)', 'Z (rad/s)'

# Convert the pandas columns to numpy arrays
time = df['Time (s)'].to_numpy()
acc = df[['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)']].to_numpy()
gyro = df[['X (rad/s)', 'Y (rad/s)', 'Z (rad/s)']].to_numpy()

# Convert acceleration and gyro data to float
acc = acc.astype(float)
gyro = gyro.astype(float)

# Scale gyro from degrees to rad/s
gyro *= DEG2RAD

# Create the orientation filter
filter = Madgwick()

# Initial quaternion
Q = np.tile([1., 0., 0., 0.], (len(time), 1))

# For all samples...
epsilon = 1e-6  # small constant to avoid division by zero
for i in range(1, len(time)):
    if np.linalg.norm(acc[i]) > epsilon:  # only update if acceleration is non-zero
        Q[i] = filter.updateIMU(Q[i-1], gyro[i], acc[i])

# Convert acceleration to world frame
acc_world = np.empty_like(acc)
for i in range(len(time)):
    if np.linalg.norm(Q[i]) > epsilon:  # only perform rotation if quaternion is non-zero
        acc_world[i] = Quaternion(Q[i]).rotate(acc[i])

# Double integrate acceleration to get position
vel = np.cumsum(acc_world, axis=0) * np.mean(np.diff(time))
pos = np.cumsum(vel, axis=0) * np.mean(np.diff(time))

# Plot position
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(pos[:, 0], pos[:, 1], pos[:, 2])
plt.show()
