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

# 5. Clean avg_listening_hours_per_week
if 'avg_listening_hours_per_week' in df.columns:
    df['avg_listening_hours_per_week'] = pd.to_numeric(df['avg_listening_hours_per_week'], errors='coerce')
    df.loc[(df['avg_listening_hours_per_week'] < 0) | (df['avg_listening_hours_per_week'] > 168), 'avg_listening_hours_per_week'] = np.nan


# 6. Clean skip_rate
if 'skip_rate' in df.columns:
    df['skip_rate'] = df['skip_rate'].astype(str).str.replace('%', '', regex=False)
    df['skip_rate'] = pd.to_numeric(df['skip_rate'], errors='coerce')
    df['skip_rate'] = df['skip_rate'] / 100

# 7. Clean satisfaction_score
if 'satisfaction_score' in df.columns:
    df['satisfaction_score'] = pd.to_numeric(df['satisfaction_score'], errors='coerce')
    df.loc[(df['satisfaction_score'] < 1) | (df['satisfaction_score'] > 10), 'satisfaction_score'] = np.nan

# 8. Standardize churn
for churn_col in ['churn', 'churned']:
    if churn_col in df.columns:

        # normalize text
        df[churn_col] = df[churn_col].astype(str).str.lower().str.strip()

        # handle messy yes/no strings ("00yes0", "nono", "yesno")
        df[churn_col] = df[churn_col].apply(
            lambda x: 1 if 'yes' in x else (0 if 'no' in x else x)
        )

        # final numeric conversion
        df[churn_col] = pd.to_numeric(df[churn_col], errors='coerce')

        # drop rows that are still invalid
        df = df.dropna(subset=[churn_col])

        df[churn_col] = df[churn_col].astype(int)

        # rename to churned so analysis script works
        df = df.rename(columns={churn_col: 'churned'})

        break


# 9. Clean date columns
for col in ['date_joined', 'last_active']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
 

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

