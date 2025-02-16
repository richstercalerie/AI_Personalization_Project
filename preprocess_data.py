import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import os

# ✅ Step 1: Load the data
file_path = "data/raw/customer_policy_data.csv"
df = pd.read_csv(file_path)

# ✅ Step 2: Handle missing values (fill NaN values with appropriate replacements)
df.fillna({
    'age': df['age'].median(),
    'income': df['income'].median(),
    'past_claims': 0,  # Assume no past claims if missing
    'engagement_score': df['engagement_score'].median()
}, inplace=True)

# ✅ Step 3: Normalize numerical values (age, income, engagement score)
scaler = MinMaxScaler()
df[['age', 'income', 'engagement_score']] = scaler.fit_transform(df[['age', 'income', 'engagement_score']])

# ✅ Step 4: Encode categorical values (occupation)
encoder = OneHotEncoder(sparse_output=False, drop='first')  # Drop first category to avoid redundancy
occupation_encoded = encoder.fit_transform(df[['occupation']])
occupation_labels = encoder.get_feature_names_out(['occupation'])
df_encoded = pd.DataFrame(occupation_encoded, columns=occupation_labels)

# Drop the original 'occupation' column and merge the encoded data
df.drop(columns=['occupation'], inplace=True)
df = pd.concat([df, df_encoded], axis=1)

# ✅ Step 5: Ensure All Customer IDs (1-10) Exist
expected_customers = pd.DataFrame({'customer_id': range(1, 11)})
df = expected_customers.merge(df, on="customer_id", how="left")

# ✅ Step 6: Fill missing values again (if any new ones appeared)
df.fillna(0, inplace=True)

# ✅ Step 7: Ensure 'processed' folder exists
processed_dir = "data/processed"
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# ✅ Step 8: Save the processed data
output_path = os.path.join(processed_dir, "cleaned_customer_data.csv")
df.to_csv(output_path, index=False)

print(f"✅ Data preprocessing complete! Processed data saved to {output_path}")
