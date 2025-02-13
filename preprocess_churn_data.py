import pandas as pd

# Load raw data
processed_data_path = "data/processed/preprocessed_churn_data.csv"
df = pd.read_csv(processed_data_path)

# 🔹 Ensure "churn" column exists (Creating it if missing)
if "churn" not in df.columns:
    print("🚨 'churn' column not found! Creating based on past_claims...")
    df["churn"] = (df["past_claims"] > 3).astype(int)  # Customers with >3 claims churn

# 🔹 Fill missing churn values with 0
df["churn"].fillna(0, inplace=True)  # Ensure no NaN values in "churn"

# Save processed data
df.to_csv(processed_data_path, index=False)
print(f"✅ Data preprocessing complete! Saved as '{processed_data_path}'")
print("✅ Data Before Saving:\n", df.tail(10))  # Print last 10 rows
