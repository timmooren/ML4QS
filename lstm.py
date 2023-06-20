# %%
import numpy as np
import optuna
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.metrics import Precision, Recall, AUC

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

n_features = X_train.shape[2]  # number of features


def create_model(learning_rate, dropout_rate, hidden_units):
    model = Sequential()
    model.add(
        LSTM(hidden_units, activation="relu", input_shape=(time_steps, n_features))
    )
    model.add(Dense(1, activation="sigmoid"))
    return model


# Creating an instance for each metric
precision = Precision(name="precision")
recall = Recall(name="recall")
auc = AUC(name="auc")


def objective(trial, X_train=X_train, y_train=y_train, X_val=X_test, y_val=y_test):
    # Define the hyperparameters to be tuned
    learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-1, log=True)
    dropout_rate = trial.suggest_float("dropout_rate", 0.0, 0.5)
    hidden_units = trial.suggest_int("hidden_units", 16, 256, log=True)

    # Create and compile the model with the suggested hyperparameters
    model = create_model(learning_rate, dropout_rate, hidden_units)
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["accuracy"])

    # Train the model
    model.fit(X_train, y_train, epochs=20, verbose=0)

    # Evaluate the model on the validation set
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)

    # Return the performance metric to be optimized
    return val_acc


study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler())
study.optimize(objective, n_trials=100)

best_params = study.best_params
best_learning_rate = best_params["learning_rate"]
best_dropout_rate = best_params["dropout_rate"]
best_hidden_units = best_params["hidden_units"]

final_model = create_model(best_learning_rate, best_dropout_rate, best_hidden_units)
final_model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy", precision, recall, auc],
)
history = final_model.fit(
    X_train, y_train, epochs=50, verbose=1, validation_data=(X_test, y_test)
)


test_loss, test_acc = final_model.evaluate(X_test, y_test, verbose=2)
print("Test accuracy:", test_acc)

import seaborn as sns
import matplotlib.pyplot as plt

# convert the history.history dict to a pandas DataFrame
hist_df = pd.DataFrame(history.history)

# or save to csv
hist_df.to_csv("history.csv")

# plot the learning curves
plt.figure(figsize=(12, 6))

# plot training & validation accuracy values
plt.figure(figsize=(12, 6))
sns.lineplot(data=hist_df[["accuracy", "val_accuracy"]], palette="tab10", linewidth=2.5)
plt.title("Model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()

# plot training & validation precision values
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=hist_df[["precision", "val_precision"]], palette="tab10", linewidth=2.5
)
plt.title("Model precision")
plt.ylabel("Precision")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()

# plot training & validation recall values
plt.figure(figsize=(12, 6))
sns.lineplot(data=hist_df[["recall", "val_recall"]], palette="tab10", linewidth=2.5)
plt.title("Model recall")
plt.ylabel("Recall")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()

# plot training & validation AUC values
plt.figure(figsize=(12, 6))
sns.lineplot(data=hist_df[["auc", "val_auc"]], palette="tab10", linewidth=2.5)
plt.title("Model AUC")
plt.ylabel("AUC")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()

# plot training & validation loss values
plt.figure(figsize=(12, 6))
sns.lineplot(data=hist_df[["loss", "val_loss"]], palette="tab10", linewidth=2.5)
plt.title("Model loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()
