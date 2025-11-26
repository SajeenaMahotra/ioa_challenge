import pandas as pd
import numpy as np
import os

print("DATA CLEANING - DataWave Music Challenge")

# Load dataset
df = pd.read_csv('dataset/datawave_music.csv')
print(f"Original dataset: {df.shape[0]} rows, {df.shape[1]} columns")

os.makedirs('cleaned_data', exist_ok=True)

# 1. Handle user IDs
df = df.dropna(subset=['user_id'])
df = df.drop_duplicates(subset=['user_id'], keep='first')

# 2. Standardize country names
if 'country' in df.columns:
    df['country'] = df['country'].str.strip().str.title()
    df['country'] = df['country'].replace({
        'Usa': 'USA', 'United States': 'USA', 'United Kingdom': 'UK', 'Uk': 'UK'
    })

# 3. Standardize subscription types
if 'subscription_type' in df.columns:
    df['subscription_type'] = df['subscription_type'].str.strip().str.title()
    df['subscription_type'] = df['subscription_type'].replace({
        'Preminum': 'Premium', 'Premuim': 'Premium', 'Familly': 'Family', 'Studnet': 'Student'
    })

# 4. Clean age
if 'age' in df.columns:
    df['age'] = df['age'].replace({
        'ten': 10, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'seventy': 70
    })
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df.loc[(df['age'] < 13) | (df['age'] > 100), 'age'] = np.nan

# 5. Clean hours_listened
if 'hours_listened' in df.columns:
    df['hours_listened'] = pd.to_numeric(df['hours_listened'], errors='coerce')
    df.loc[(df['hours_listened'] < 0) | (df['hours_listened'] > 168), 'hours_listened'] = np.nan

# 6. Clean satisfaction_score
if 'satisfaction_score' in df.columns:
    df['satisfaction_score'] = pd.to_numeric(df['satisfaction_score'], errors='coerce')
    df.loc[(df['satisfaction_score'] < 1) | (df['satisfaction_score'] > 10), 'satisfaction_score'] = np.nan

# 7. Standardize churn
if 'churn' in df.columns:
    df['churn'] = df['churn'].map({
        'Yes': 1, 'yes': 1, 'YES': 1, 'Y': 1,
        'No': 0, 'no': 0, 'NO': 0, 'N': 0,
        1: 1, 0: 0, '1': 1, '0': 0
    })

# 8. Clean date columns
for col in ['date_joined', 'last_active']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)

# 9. Standardize genre and device
for col in ['favourite_genre', 'device']:
    if col in df.columns:
        df[col] = df[col].str.strip().str.title()

# 10. Missing values summary
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing_Count': missing, 'Percentage': missing_pct})
print(missing_df[missing_df['Missing_Count'] > 0])

# Save cleaned dataset
output_file = 'cleaned_data/datawave_cleaned.csv'
df.to_csv(output_file, index=False)
print(f"Cleaned dataset saved: {output_file}, Shape: {df.shape}")
print("DATA CLEANING COMPLETE")

