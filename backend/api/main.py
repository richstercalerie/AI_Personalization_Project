from fastapi import FastAPI

app = FastAPI()  # ✅ Defines the FastAPI instance

@app.get("/")
def read_root():
    return {"message": "API is running successfully"}
