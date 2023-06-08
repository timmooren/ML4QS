import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_gyro = pd.read_csv("../climb_data_phyphox/climb_phy_4_sien/Gyroscope.csv")
df_lin = pd.read_csv("../climb_data_phyphox/climb_phy_4_sien/Linear Accelerometer.csv")
df_bar = pd.read_csv("../climb_data_phyphox/climb_phy_4_sien/Barometer.csv")

print(df_gyro)

df_gyro.rename(columns = {"X (rad/s)": "gyro_X", "Y (rad/s)" : "gyro_Y", "Z (rad/s)": "gyro_Z"}, inplace=True)
df_lin.rename(columns = {"X (m/s^2)": "acc_X", "Y (m/s^2)" : "acc_Y", "Z (m/s^2)": "acc_Z"}, inplace=True)

extract_col1, extract_col2, extract_col3= df_lin["acc_X"], df_lin["acc_Y"], df_lin["acc_Z"]

data = df_gyro.join([extract_col1, extract_col2, extract_col3])

# plt_gyrox = sns.lineplot(data, x = "Time (s)", y = "gyro_X")
# plt_gyrox = sns.lineplot(data, x = "Time (s)", y = "gyro_Y")
# plt_gyrox = sns.lineplot(data, x = "Time (s)", y = "gyro_Z")
# plt.show()

# plt_gyrox = sns.lineplot(data, x = "Time (s)", y = "acc_X")
# plt_gyrox = sns.lineplot(data, x = "Time (s)", y = "acc_Y")
# plt_gyrox = sns.lineplot(data, x = "Time (s)", y = "acc_Z")
# plt.show()


df_melt = data.melt(id_vars="Time (s)", value_vars=["acc_X", "acc_Y", "acc_Z"], var_name='variable', value_name="m/s^2")

g = sns.FacetGrid(df_melt, row = "variable")
g.map(sns.lineplot, "Time (s)", "m/s^2")
g.fig.set_size_inches(20, 7)
plt.savefig("../plots/chapter2_plots/acc_plot_fall.png")


df_melt = data.melt(id_vars="Time (s)", value_vars=["gyro_X", "gyro_Y", "gyro_Z"], var_name='variable', value_name="(rad/s)")
g = sns.FacetGrid(df_melt, row = "variable")
g.map(sns.lineplot, "Time (s)", "(rad/s)")
g.fig.set_size_inches(20, 7)
g.savefig("../plots/chapter2_plots/gyro_plot_fall.png")