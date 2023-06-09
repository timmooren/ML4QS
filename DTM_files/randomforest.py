from sklearn.ensemble import RandomForestClassifier
from data import Data

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
df = Data("data.csv")


# Fit the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
