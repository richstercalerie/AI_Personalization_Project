from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import os

app = FastAPI()

# Paths
model_path = "models/saved/recommendation_svd.pkl"
data_path = "data/processed/cleaned_customer_data.csv"

# Load the trained model
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    raise FileNotFoundError("🚨 Model file not found! Please train the model first.")

# Load customer-policy data
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    raise FileNotFoundError("🚨 Processed data file not found! Please preprocess the data first.")

# Function to generate recommendations
def recommend_policies(customer_id: int, n=3):
    if customer_id not in df["customer_id"].values:
        raise HTTPException(status_code=404, detail="Customer ID not found!")

    all_policies = df["policy_id"].unique()
    predictions = [(int(policy), float(model.predict(customer_id, policy).est)) for policy in all_policies]
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    return [policy for policy, _ in predictions[:n]]

# API Endpoint for Recommendations
@app.get("/recommend/{customer_id}")
def get_recommendations(customer_id: int):
    try:
        recommendations = recommend_policies(customer_id)
        return {"customer_id": customer_id, "recommended_policies": recommendations}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
