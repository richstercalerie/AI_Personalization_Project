#!/bin/bash
set -e  # Exit on first error

echo "🚀 Starting Build Process"

# Ensure the models directory exists
mkdir -p models/saved

# Check if the model exists
if [ ! -f "models/saved/recommendation_svd.pkl" ]; then
    echo "🚨 Model file NOT FOUND in deployment!"
    exit 1  # Stop deployment
else
    echo "✅ Model file exists: models/saved/recommendation_svd.pkl"
fi

# Start the FastAPI server
cd backend/api
uvicorn main:app --host 0.0.0.0 --port 10000
