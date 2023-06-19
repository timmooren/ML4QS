# %%
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

pd.set_option("display.max_columns", None)

# Load preprocessed data
data = pd.read_csv("datasets/processed_data.csv")
# drop datetime
data = data.drop("datetime", axis=1)

# %%
# show number of rows per climb_id
data.groupby("climb_id").size()


# %%
# for every climb_id, if fall_top is 1, make fall_top is 1 for only the last row
unique_climb_ids = data["climb_id"].unique()

for climb_id in unique_climb_ids:
    subset = data[data["climb_id"] == climb_id]
    if subset["fall_top"].sum() > 0:  # if 'fall_top' is 1 for any row in the subset
        data.loc[
            (data["climb_id"] == climb_id) & (data.index != subset.index[-1]),
            "fall_top",
        ] = 0  # set 'fall_top' to 0 for all rows except the last one


# %%
# check whether every climb_id is the same length
data.groupby("climb_id").size().unique()

# %%
data = data.sort_values(["climb_id", "Time (s)"])
data

# %%
# Normalize the features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data.drop(["fall_top", "climb_id"], axis=1))
scaled_data

# %%
# Transform data into sequences for LSTM, maintaining climb_id integrity
# time_steps
time_steps = 20
X = []
y = []

for climb_id in data["climb_id"].unique():
    climb_data = scaled_data[data["climb_id"] == climb_id]

    for i in range(time_steps, len(climb_data)):
        X.append(climb_data[i - time_steps : i])
        y.append(data.loc[data["climb_id"] == climb_id, "fall_top"].values[i])

ratio = sum(y) / len(y)
print("Ratio of fall_top = 1:", ratio)
# Convert to arrays
X, y = np.array(X), np.array(y)
# show the data together to verify it is correct


# %%
def custom_train_test_split(X, y, test_size=0.2):
    split_index = int(len(X) * (1 - test_size))
    X_train = X[:split_index]
    y_train = y[:split_index]
    X_test = X[split_index:]
    y_test = y[split_index:]
    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = custom_train_test_split(X, y, test_size=0.2)


# %%
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

n_features = X_train.shape[2]  # number of features

model = Sequential()
model.add(LSTM(50, activation="relu", input_shape=(time_steps, n_features)))
model.add(Dense(1, activation="sigmoid"))  # Binary classification

from tensorflow.keras.metrics import Precision, Recall, AUC

# Creating an instance for each metric
precision = Precision(name="precision")
recall = Recall(name="recall")
auc = AUC(name="auc")

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy", precision, recall, auc],
)


class_weights = {
    0: 1.0,
    1: 100.0,
}  # Assuming class 1 is the minority and needs more weight

model.fit(X_train, y_train, epochs=50, verbose=1)

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print("Test accuracy:", test_acc)
