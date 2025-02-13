import pandas as pd
import os

# Load raw data
raw_data_path = "data/raw/customer_policy_data.csv"
df = pd.read_csv(raw_data_path)

# 🔹 Ensure "churn" column exists (Creating it if missing)
if "churn" not in df.columns:
    print("🚨 'churn' column not found! Creating based on past_claims...")
    df["churn"] = (df["past_claims"] > 3).astype(int)  # Customers with >3 claims churn

# 🔹 One-hot encoding categorical variables (e.g., occupation)
if "occupation" in df.columns:
    df = pd.get_dummies(df, columns=["occupation"])

# Save processed data
processed_data_path = "data/processed/preprocessed_churn_data.csv"
df.to_csv(processed_data_path, index=False)
print(f"✅ Data preprocessing complete! Saved as '{processed_data_path}'")
