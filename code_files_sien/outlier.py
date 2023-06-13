
import scipy
import math
from sklearn.mixture import GaussianMixture
import numpy as np
import pandas as pd

import copy


def chauvenets_criterion(data_table, col_list, C):

    # create seperate dataframe for outliers
    data_table = pd.read_csv(data_table)
    output = pd.DataFrame()

    # detect outliers for each column
    for col in col_list:

            ### CODE FROM /Python3Code/Chapter3/OutlierDetection.py
        # Computer the mean and standard deviation.
        mean = data_table[col].mean()
        std = data_table[col].std()
        N = len(data_table.index)
        criterion = 1.0/(C*N)

        # Consider the deviation for the data points.
        deviation = abs(data_table[col] - mean)/std

        # Express the upper and lower bounds.
        low = -deviation/math.sqrt(C)
        high = deviation/math.sqrt(C)
        prob = []
        mask = []

        # Pass all rows in the dataset.
        for i in range(0, len(data_table.index)):
            # Determine the probability of observing the point
            prob.append(
                1.0 - 0.5 * (scipy.special.erf(high[i]) - scipy.special.erf(low[i])))
            # And mark as an outlier when the probability is below our criterion.
            mask.append(prob[i] < criterion)

        output[col + '_outlier'] = mask

    return output   

outlier = chauvenets_criterion("../datasets/cut_data/cut_data_sien.csv", ["X (m/s^2)", "Y (m/s^2)", "Z (m/s^2)", "Time (s).1", "X (rad/s)", "Y (rad/s)", "Z (rad/s)"], 5)

print(outlier)

idk = outlier["X (m/s^2)_outlier"].value_counts()
print(idk)

