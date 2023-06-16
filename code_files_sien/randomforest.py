import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.tree import export_graphviz
from IPython.display import Image
import graphviz

def random_forest(df):
    x = df.drop('fall_top', axis=1)
    y = df['fall_top']

    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2)

    mod = RandomForestClassifier()
    mod.fit(X_train, Y_train)

    Y_pred = mod.predict(X_test)

    accuracy = accuracy_score(Y_test, Y_pred)
    print("Accuracy:", accuracy)