import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load preprocessed churn data
data_path = "data/processed/preprocessed_churn_data.csv"
df = pd.read_csv(data_path)

# ✅ Ensure "churn" column exists
if "churn" not in df.columns:
    raise KeyError("🚨 'churn' column is missing from the dataset! Check preprocessing.")

# 🚀 Define features (X) and target variable (y)
X = df.drop(columns=["churn"])
y = df["churn"]

# 🚀 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🚀 Train RandomForest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🚀 Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Training Complete! Accuracy: {accuracy:.4f}")

# ✅ Save Model
model_path = "models/saved/churn_model.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
print(f"🎯 Model saved successfully at '{model_path}'!")
