from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os

app = FastAPI()

# ✅ Load the trained model
model_path = "models/saved/churn_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    raise FileNotFoundError("🚨 Churn model file not found! Train the model first.")

# ✅ Load column names
data_path = "data/processed/preprocessed_churn_data.csv"
df = pd.read_csv(data_path)
feature_columns = df.drop(columns=["churn"]).columns.tolist()  # Remove target column

@app.get("/")
def home():
    return {"message": "Churn Prediction API is running successfully"}

@app.post("/predict_churn/")
def predict_churn(customer_data: dict):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([customer_data])
        input_df = input_df[feature_columns]  # Ensure correct feature order

        # Predict churn probability
        churn_proba = model.predict_proba(input_df)[0][1]  # Probability of churning

        return {"churn_probability": churn_proba}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
