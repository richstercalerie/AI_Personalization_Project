#!/bin/bash
set -e  # Exit immediately if a command fails

echo "🚀 Starting Build Process"

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Ensure model directory exists
mkdir -p models/saved

# Debugging step: List all files before checking model
echo "📂 Listing project directory before checking model:"
ls -R

# Check if the model file exists
if [ ! -f "models/saved/recommendation_svd.pkl" ]; then
    echo "🚨 Model file NOT FOUND in Render!"
    echo "📂 Listing 'models' directory for debugging:"
    ls -R models  # Debugging step
    exit 1  # Stop deployment if model is missing
else
    echo "✅ Model file exists: models/saved/recommendation_svd.pkl"
fi

# Start FastAPI server
cd backend/api
exec uvicorn main:app --host 0.0.0.0 --port 10000
