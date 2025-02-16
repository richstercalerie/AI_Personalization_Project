import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load processed data
DATA_PATH = "data/processed/preprocessed_churn_data.csv"
MODEL_PATH = "models/saved/churn_model.pkl"

df = pd.read_csv(DATA_PATH)

# ✅ Drop unnecessary columns
X = df.drop(columns=["customer_id", "churn"], errors="ignore")  # Fix: Drop only if exists
y = df["churn"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("✅ Model Training Complete! 🎯 Model saved successfully at 'models/saved/churn_model.pkl'!")
