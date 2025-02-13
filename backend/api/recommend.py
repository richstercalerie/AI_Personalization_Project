import pickle
import pandas as pd
from fastapi import HTTPException

# Load Model & Data
MODEL_PATH = "models/saved/recommendation_svd.pkl"
DATA_PATH = "data/processed/cleaned_customer_data.csv"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("🚨 Model file not found! Please train the model.")

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise RuntimeError("🚨 Data file not found! Please preprocess the data.")

# ✅ Recommendation Function
def get_recommendations(customer_id: int):
    if customer_id not in df["customer_id"].values:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    
    try:
        all_policies = df["policy_id"].unique()
        predictions = [(int(policy), float(model.predict(customer_id, policy).est)) for policy in all_policies]
        predictions.sort(key=lambda x: x[1], reverse=True)

        recommended_policies = [policy for policy, _ in predictions[:3]]
        return {"customer_id": customer_id, "recommended_policies": recommended_policies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
