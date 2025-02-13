import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# 🔹 Load the processed dataset
df = pd.read_csv("data/processed/preprocessed_churn_data.csv")

# 🔹 Ensure the dataset has 'churn' column
if "churn" not in df.columns:
    raise ValueError("🚨 'churn' column is missing! Check preprocessing.")

# 🔹 Split features and target variable
X = df.drop(columns=["churn"])
y = df["churn"]

# 🔹 Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train a Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 Save the trained model
with open("models/saved/churn_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model Training Complete! 🎯 Model saved at 'models/saved/churn_model.pkl'!")
