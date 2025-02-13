from fastapi import FastAPI, HTTPException, Request
import logging
from backend.api.recommend import get_recommendations
from backend.api.churn import predict_churn

app = FastAPI()

# ✅ Configure Logging
logging.basicConfig(
    filename="backend/api/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logging.info(f"{request.method} {request.url} - {response.status_code}")
    return response

# ✅ API Home Route
@app.get("/")
def home():
    return {"message": "API is running successfully"}

# ✅ Recommendation API
@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):
    try:
        return get_recommendations(customer_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in /recommend/{customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Churn Prediction API with Explainability
@app.get("/churn/{customer_id}")
def churn(customer_id: int):
    try:
        return predict_churn(customer_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in /churn/{customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
