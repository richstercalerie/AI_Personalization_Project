import pandas as pd

# ✅ File Paths
processed_data_path = "data/processed/preprocessed_churn_data.csv"
raw_data_path = "data/raw/customer_policy_data.csv"

# ✅ Load Data
df_raw = pd.read_csv(raw_data_path)
df_processed = pd.read_csv(processed_data_path)

# ✅ Ensure `customer_id` is an integer to prevent merge issues
df_raw["customer_id"] = df_raw["customer_id"].astype(int)
df_processed["customer_id"] = df_processed["customer_id"].astype(int)

# ✅ Keep only necessary columns from `df_raw`
df_raw = df_raw[['customer_id', 'policy_id', 'age', 'income', 'past_claims', 'engagement_score', 'occupation']]

# ✅ Drop duplicate columns from `df_processed` BEFORE merging
df_processed = df_processed.loc[:, ~df_processed.columns.duplicated()]

# ✅ Merge while keeping all customer IDs
df_processed = df_raw.merge(
    df_processed.drop(columns=['policy_id', 'age', 'income', 'past_claims', 'engagement_score', 'occupation'],
                      errors='ignore'),
    on="customer_id",
    how="outer"  # 🔥 Keeps all customers from both datasets
)

# ✅ Ensure 'churn' column exists with proper logic
if "churn" not in df_processed.columns:
    df_processed["churn"] = ((df_processed["past_claims"] > 2) | (df_processed["engagement_score"] < 50)).astype(int)

# ✅ Drop duplicate columns after merging (if any)
df_processed = df_processed.loc[:, ~df_processed.columns.duplicated()]

# ✅ One-Hot Encode `occupation` (Fix "Doctor" issue)
if "occupation" in df_processed.columns:
    df_processed = pd.get_dummies(df_processed, columns=["occupation"], dtype=int, drop_first=True)  # Avoids duplicate features

# ✅ Fill missing values
df_processed.fillna(0, inplace=True)

# ✅ Save the cleaned data
df_processed.to_csv(processed_data_path, index=False)

print(f"✅ Data preprocessing complete! Saved as '{processed_data_path}'")
print("✅ Data Columns After Processing:\n", df_processed.columns.tolist())  # Debugging line
print("✅ Data Before Saving:\n", df_processed.tail(10))  # Print last 10 rows
