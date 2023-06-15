import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np


class Data:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)
        self.train_data = None
        self.test_data = None
        self.scaler = StandardScaler()

    def clean_data(self):
        # Remove any rows with missing data
        self.data.dropna(inplace=True)

        # You can add other data cleaning steps here as needed

    def preprocess_data(self, sequence_length):
        X = []
        y = []

        for session_id in self.data["session_id"].unique():
            session_data = self.data[self.data["session_id"] == session_id]
            features = session_data[["acc_x", "acc_y", "acc_z"]]
            labels = session_data["fall"]

            # Scale features
            if self.train_data is None:
                self.scaler.fit(features)
            features = self.scaler.transform(features)

            # Create sequences for this session
            for i in range(sequence_length, len(features)):
                X.append(features[i - sequence_length : i])
                y.append(labels.iloc[i])

        return np.array(X), np.array(y)

    def preprocess_data_rf(self, sequence_length):
        # Add lagged features
        for i in range(1, sequence_length + 1):
            for col in ["acc_x", "acc_y", "acc_z"]:
                self.data[f"{col}_lag{i}"] = self.data.groupby("session_id")[col].shift(
                    i
                )

        # Drop rows with NaN values
        self.data.dropna(inplace=True)

        # Separate features and target
        X = self.data.drop(["session_id", "fall", "time"], axis=1)
        y = self.data["fall"]

        # Scale features
        X = self.scaler.fit_transform(X)

        return X, y

    def split_data(self, test_size, sequence_length):
        X, y = self.preprocess_data(sequence_length)
        (
            self.train_data,
            self.test_data,
            self.train_labels,
            self.test_labels,
        ) = train_test_split(X, y, test_size=test_size, random_state=42)

