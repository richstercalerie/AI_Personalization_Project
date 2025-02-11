import pandas as pd
import numpy as np
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
import os

# Step 1: Load Processed Data
file_path = "data/processed/cleaned_customer_data.csv"
df = pd.read_csv(file_path)

# Step 2: Prepare Data for Surprise Library
reader = Reader(rating_scale=(0, 1))  # Engagement score is normalized
data = Dataset.load_from_df(df[['customer_id', 'policy_id', 'engagement_score']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# Step 3: Train SVD Recommendation Model
model = SVD()
model.fit(trainset)

# Step 4: Evaluate Model
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"✅ Model Training Complete! RMSE: {rmse}")

# Step 5: Generate Policy Recommendations
def recommend_policies(customer_id, n=3):
    all_policies = df['policy_id'].unique()
    predictions = [(policy, model.predict(customer_id, policy).est) for policy in all_policies]
    predictions.sort(key=lambda x: x[1], reverse=True)
    return [policy for policy, _ in predictions[:n]]

# Example: Recommend policies for a customer
customer_id = 1
recommended_policies = recommend_policies(customer_id)
print(f"🎯 Recommended Policies for Customer {customer_id}: {recommended_policies}")

# Step 6: Save Model (Optional)
model_dir = "models/saved"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)
import pickle
with open(f"{model_dir}/recommendation_svd.pkl", "wb") as f:
    pickle.dump(model, f)
print("✅ Model saved successfully!")

