import pickle
import pandas as pd
from fastapi import HTTPException

# Load Model & Data
MODEL_PATH = "models/saved/churn_model.pkl"
DATA_PATH = "data/processed/preprocessed_churn_data.csv"

# ✅ Load Trained Model
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("🚨 Model file not found! Please train the model.")

# ✅ Load Processed Data
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise RuntimeError("🚨 Data file not found! Please preprocess the data.")

# 🔹 **Fix Missing Values Before Conversion**
df.fillna(0, inplace=True)  # Replace NaN values with 0

# 🔹 **Convert Occupation Columns to Integer**
df = df.astype({
    "occupation_Developer": int,
    "occupation_Doctor": int,
    "occupation_Engineer": int,
    "occupation_Retired": int,
    "occupation_Teacher": int
})

# ✅ Select Only Expected Features
expected_features = [
    "policy_id", "age", "income", "past_claims", "engagement_score",
    "occupation_Developer", "occupation_Doctor", "occupation_Engineer",
    "occupation_Retired", "occupation_Teacher"
]

# ✅ Churn Prediction Function
def predict_churn(customer_id: int):
    if customer_id not in df["customer_id"].values:
        raise HTTPException(status_code=404, detail="Customer ID not found")

    try:
        # 🚀 Drop "customer_id" and "churn" to match model input
        features = df[df["customer_id"] == customer_id][expected_features]

        print("🔍 Features Passed to Model:", features.columns.tolist())  # Debugging output
        print("🔹 Model Expects:", model.feature_names_in_)  # Debugging output
        
        # 🚀 Perform Prediction
        prediction = model.predict(features.values)
        return {"customer_id": customer_id, "churn_prediction": bool(prediction[0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Churn prediction error: {str(e)}")
