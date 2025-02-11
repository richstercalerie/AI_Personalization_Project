import os
from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd

app = FastAPI()

# Use an absolute path based on the project structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models/saved/recommendation_svd.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data/processed/cleaned_customer_data.csv")

# Load the trained model
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
else:
    raise FileNotFoundError(f"🚨 Model file not found at {MODEL_PATH}! Please train the model first.")

# Load customer-policy data
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    raise FileNotFoundError(f"🚨 Processed data file not found at {DATA_PATH}! Please preprocess the data first.")

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
