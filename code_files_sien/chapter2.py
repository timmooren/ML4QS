import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import copy

# import data of climb with a fall
df_gyro = pd.read_csv("../climb_data_phyphox/climb_phy_4_sien/Gyroscope.csv")
df_lin = pd.read_csv("../climb_data_phyphox/climb_phy_4_sien/Linear Accelerometer.csv")
df_bar = pd.read_csv("../climb_data_phyphox/climb_phy_4_sien/Barometer.csv")

# alter column names
df_gyro.rename(columns = {"X (rad/s)": "gyro_X", "Y (rad/s)" : "gyro_Y", "Z (rad/s)": "gyro_Z"}, inplace=True)
df_lin.rename(columns = {"X (m/s^2)": "acc_X", "Y (m/s^2)" : "acc_Y", "Z (m/s^2)": "acc_Z"}, inplace=True)

# combine the acceleration data and the gyroscope data
extract_col1, extract_col2, extract_col3= df_lin["acc_X"], df_lin["acc_Y"], df_lin["acc_Z"]
data = df_gyro.join([extract_col1, extract_col2, extract_col3])

# convert to normal day time
data["Time (s)"] = pd.to_datetime(data["Time (s)"], unit="s")

# copy data and time interval to 1 second
data_copy = copy.deepcopy(data)
data_copy = data_copy.resample("1S", on="Time (s)").mean().reset_index()


"""plot the data"""

# plot the Accelerometer data with 0.20 seconds time stamp
df_melt = data.melt(id_vars="Time (s)", value_vars=["acc_X", "acc_Y", "acc_Z"], var_name='variable', value_name="m/s^2")
g = sns.FacetGrid(df_melt, row = "variable")
g.map(sns.lineplot, "Time (s)", "m/s^2")
g.fig.set_size_inches(20, 7)
plt.savefig("../plots/chapter2_plots/acc_plot_fall_0.20sec.png")

# plot the Gyroscope data 0.20 seconds time stamp
df_melt = data.melt(id_vars="Time (s)", value_vars=["gyro_X", "gyro_Y", "gyro_Z"], var_name='variable', value_name="(rad/s)")
g = sns.FacetGrid(df_melt, row = "variable")
g.map(sns.lineplot, "Time (s)", "(rad/s)")
g.fig.set_size_inches(20, 7)
g.savefig("../plots/chapter2_plots/gyro_plot_fall_0.20sec.png")

# plot the Accelerometer data with 1 seconds time stamp
df_melt = data_copy.melt(id_vars="Time (s)", value_vars=["acc_X", "acc_Y", "acc_Z"], var_name='variable', value_name="m/s^2")
g = sns.FacetGrid(df_melt, row = "variable")
g.map(sns.lineplot, "Time (s)", "m/s^2")
g.fig.set_size_inches(20, 7)
plt.savefig("../plots/chapter2_plots/acc_plot_fall_1sec.png")

# plot the Gyroscope data 1 seconds time stamp
df_melt = data_copy.melt(id_vars="Time (s)", value_vars=["gyro_X", "gyro_Y", "gyro_Z"], var_name='variable', value_name="(rad/s)")
g = sns.FacetGrid(df_melt, row = "variable")
g.map(sns.lineplot, "Time (s)", "(rad/s)")
g.fig.set_size_inches(20, 7)
g.savefig("../plots/chapter2_plots/gyro_plot_fall_1sec.png")

