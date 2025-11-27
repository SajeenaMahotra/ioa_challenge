import pandas as pd
import numpy as np
import os

print("DATA CLEANING - DataWave Music Challenge")

# Load dataset
df = pd.read_csv('dataset/datawave_music.csv')
print(f"Original dataset: {df.shape[0]} rows × {df.shape[1]} columns")

os.makedirs('cleaned_data', exist_ok=True)

# 1. Basic cleanup – user_id
df = df.dropna(subset=['user_id'])                    # remove rows without ID
df = df.drop_duplicates(subset=['user_id'], keep='first')

# 2. Standardize categorical columns
# Country
country_map = {'IND': 'India', 'UK': 'United Kingdom', 'U.K.': 'United Kingdom', 'USA': 'United States'}
df['country'] = df['country'].replace(country_map)

# Gender
gender_map = {'M': 'Male', 'm': 'Male', 'male': 'Male',
              'F': 'Female', 'f': 'Female', 'female': 'Female',
              'Other': 'Other'}
df['gender'] = df['gender'].map(gender_map).fillna('Unknown')

# Subscription type
sub_map = {'Premum': 'Premium', 'Studnt': 'Student', 'Fam': 'Family'}
df['subscription_type'] = df['subscription_type'].replace(sub_map)

# 3. Clean numeric columns
# Age
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df = df[df['age'].between(13, 100)]                     # realistic age range

# Listening hours per week
df['avg_listening_hours_per_week'] = pd.to_numeric(df['avg_listening_hours_per_week'], errors='coerce')
df = df[df['avg_listening_hours_per_week'].between(0, 168)]

# Total songs played
df['total_songs_played'] = pd.to_numeric(df['total_songs_played'], errors='coerce').astype('Int64')

# Skip rate → convert to proportion (0–1)
def clean_skip_rate(x):
    if pd.isna(x): return np.nan
    s = str(x).strip().lower()
    if s == 'ten': return 0.10
    if '%' in s:   return float(s.replace('%', '')) / 100
    try:
        return float(s)
    except:
        return np.nan

df['skip_rate'] = df['skip_rate'].apply(clean_skip_rate)

# Satisfaction score (1–5 scale in this dataset)
df['satisfaction_score'] = pd.to_numeric(df['satisfaction_score'], errors='coerce')
df['satisfaction_score'] = df['satisfaction_score'].fillna(df['satisfaction_score'].median())

# 4. Churned → binary 0/1
df['churned'] = df['churned'].astype(str).str.lower()
df['churned'] = df['churned'].map({'yes': 1, 'no': 0, '1': 1, '0': 0}).fillna(0).astype(int)

# 5. Monthly fee
df['monthly_fee'] = df['monthly_fee'].astype(str).str.replace(r'\s*USD$', '', regex=True)
df['monthly_fee'] = pd.to_numeric(df['monthly_fee'], errors='coerce')

# Impute missing fee using median per subscription type
fee_medians = df.groupby('subscription_type')['monthly_fee'].median()
df['monthly_fee'] = df.apply(
    lambda row: fee_medians[row['subscription_type']] if pd.isna(row['monthly_fee']) else row['monthly_fee'],
    axis=1
)

# 6. Join date → datetime
df['join_date'] = pd.to_datetime(df['join_date'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['join_date'])   # drop the very few unparseable dates

# 7. Final data types & summary
df['age'] = df['age'].astype(int)
df['satisfaction_score'] = df['satisfaction_score'].astype(int)

# Missing values check (should be zero now)
print("\nMissing values after cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Save
output_path = 'cleaned_data/datawave_cleaned.csv'
df.to_csv(output_path, index=False)
print(f"\nCleaning complete! Cleaned dataset saved to: {output_path}")
