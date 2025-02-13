import pickle
import pandas as pd
from fastapi import HTTPException

# Load Model & Data
MODEL_PATH = "models/saved/churn_model.pkl"
DATA_PATH = "data/processed/preprocessed_churn_data.csv"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("🚨 Model file not found! Please train the model.")

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise RuntimeError("🚨 Data file not found! Please preprocess the data.")

# ✅ Churn Prediction Function
def predict_churn(customer_id: int):
    if customer_id not in df["customer_id"].values:
        raise HTTPException(status_code=404, detail="Customer ID not found")

    try:
        features = df[df["customer_id"] == customer_id].drop(columns=["customer_id"])
        prediction = model.predict([features.values[0]])
        return {"customer_id": customer_id, "churn_prediction": bool(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Churn prediction error: {str(e)}")
