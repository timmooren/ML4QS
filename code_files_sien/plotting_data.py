import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import copy
import datetime as dt
import os

def get_file(filepath):


    list_folder = [folder for folder in os.listdir(filepath)]
    list_folder.remove(".DS_Store")
    print(list_folder)
#     for file in files:
        
#         df = pd.read_csv(f"{filepath}/{folder}")
    
    
# df_gyro = pd.read_csv("../climb_data_phyphox/sien/climb_phy_4_sien/Gyroscope.csv")
# df_lin = pd.read_csv("../climb_data_phyphox/sien/climb_phy_4_sien/Linear Accelerometer.csv")
# df_bar = pd.read_csv("../climb_data_phyphox/sien/climb_phy_4_sien/Barometer.csv")



get_file("../climb_data_phyphox/sien")