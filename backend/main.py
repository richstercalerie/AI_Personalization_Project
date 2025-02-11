from fastapi import FastAPI
from api.recommend import recommend_function  # Import function from recommend.py if needed

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running successfully"}

# Example route using recommend.py
@app.get("/recommend")
def get_recommendations():
    return recommend_function()  # Replace with actual function logic
