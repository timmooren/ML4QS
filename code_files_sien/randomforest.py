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



param_dist = {'n_estimators': randint(50,500),
              'max_depth': randint(1,20)}

# Create a random forest classifier
mod = RandomForestClassifier()

# Use random search to find the best hyperparameters
rand_search = RandomizedSearchCV(mod, 
                                 param_distributions = param_dist, 
                                 n_iter=5, 
                                 cv=5)

# Fit the random search object to the data
rand_search.fit(X_train, y_train)

# Create a variable for the best model
best_rf = rand_search.best_estimator_

# Print the best hyperparameters
print('Best hyperparameters:',  rand_search.best_params_)