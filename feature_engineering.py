import pandas as pd
import numpy as np


def french_grade_to_num(french_grade):
    mapping = {"a": 0.0, "b": 0.3, "c": 0.7, "+": 0.1}
    num_grade = 0
    for char in french_grade:
        if char.isdigit():
            num_grade += int(char)
        elif char in mapping:
            num_grade += mapping[char]
    return num_grade


def features(df):
    df["magnitude"] = np.sqrt(df["acc_x"] ** 2 + df["acc_y"] ** 2 + df["acc_z"] ** 2)
    df["roll"] = np.arctan2(df["acc_y"], df["acc_z"])
    df["pitch"] = np.arctan2(df["acc_x"], np.sqrt(df["acc_y"] ** 2 + df["acc_z"] ** 2))

    # velocity
    df["Velocity_X"] = df["X (m/s^2)"].cumsum() * df["Time (s)"].diff()
    df["Velocity_Y"] = df["Y (m/s^2)"].cumsum() * df["Time (s)"].diff()
    df["Velocity_Z"] = df["Z (m/s^2)"].cumsum() * df["Time (s)"].diff()

    # displacement
    df["Displacement_X"] = df["Velocity_X"].cumsum() * df["Time (s)"].diff()
    df["Displacement_Y"] = df["Velocity_Y"].cumsum() * df["Time (s)"].diff()
    df["Displacement_Z"] = df["Velocity_Z"].cumsum() * df["Time (s)"].diff()

    # distance
    df["distance"] = np.sqrt(
        df["Displacement_X"] ** 2
        + df["Displacement_Y"] ** 2
        + df["Displacement_Z"] ** 2
    )

    return df
