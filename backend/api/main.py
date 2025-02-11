from fastapi import FastAPI
from recommend import get_recommendations  # ✅ Relative Import


app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running successfully"}

# ✅ Register the recommendation route
@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):
    return get_recommendations(customer_id)
