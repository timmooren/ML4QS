# %%
import pandas as pd
import seaborn as sns

# %%
# open dataswet raw data sien
df = pd.read_csv("climb_data_phyphox/sien/climb_phy_4_sien/Linear Accelerometer.csv")
df

# %%
# select rows where entry num is  5
# df = df[df["entry_num"] == 5]

# select last 10 seconds from time column, time is in seconds
# take max of time column
df = df[df["Time (s)"] > df["Time (s)"].max() - 10]


# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

# Assuming the data is in a DataFrame df
# Assume 'Time (s)' is the time column
time = df["Time (s)"].values

# Calculate velocity by integrating the acceleration data
velocity_x = cumtrapz(df["X (m/s^2)"].values, time, initial=0)
velocity_y = cumtrapz(df["Y (m/s^2)"].values, time, initial=0)
velocity_z = cumtrapz(df["Z (m/s^2)"].values, time, initial=0)

# Calculate position by integrating the velocity
position_x = cumtrapz(velocity_x, time, initial=0)
position_y = cumtrapz(velocity_y, time, initial=0)
position_z = cumtrapz(velocity_z, time, initial=0)
from matplotlib import cm

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Create a colormap
colors = cm.viridis(np.linspace(0, 1, len(time)))

# Scatter plot with color hue changing with time
sc = ax.scatter(position_x, position_y, position_z, c=colors)

ax.set_xlabel("X")
ax.set_ylabel("Z")
ax.set_zlabel("Y")
# Inverting the Y-axis
ax.invert_yaxis()

# Adding a colorbar
plt.colorbar(sc, label="Time (s)", pad=0.1)

plt.show()
