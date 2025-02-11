#!/bin/bash
# Ensure the models directory exists
mkdir -p models/saved

# Ensure the trained model is present
if [ ! -f "models/saved/recommendation_svd.pkl" ]; then
    echo "🚨 Model file missing! Copying from Git..."
    cp ./models/saved/recommendation_svd.pkl models/saved/recommendation_svd.pkl
fi
