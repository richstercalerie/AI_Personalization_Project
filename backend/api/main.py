from fastapi import FastAPI
from api.recommend import get_recommendations
from api.churn import predict_churn  # ✅ Import churn prediction function

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running successfully"}

@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):
    return get_recommendations(customer_id)

@app.post("/predict_churn/")
def predict(data: dict):
    return predict_churn(data)
