import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Load your dataset
data = pd.read_csv("your_data.csv")

# Assuming the data has columns 'acc_x', 'acc_y', 'acc_z' for accelerometer data and 'fall' for ground truth labels
features = data[["acc_x", "acc_y", "acc_z"]]
labels = data["fall"]

# Scale the feature data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(features)

# Define a sequence length
sequence_length = 30

# Create sequences
X = []
y = []
for i in range(sequence_length, len(scaled_features)):
    X.append(scaled_features[i - sequence_length : i])
    y.append(labels[i])

X = np.array(X)
y = np.array(y)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

# Define the LSTM model
model = Sequential()
model.add(
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2]))
)
model.add(Dropout(0.2))
model.add(LSTM(50))
model.add(Dropout(0.2))
model.add(Dense(1, activation="sigmoid"))  # Sigmoid function for binary classification

# Compile the model
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])


model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))


# Make predictions
y_pred = model.predict(X_test)
y_pred = y_pred > 0.5

# Evaluate model
from sklearn.metrics import confusion_matrix, classification_report

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
