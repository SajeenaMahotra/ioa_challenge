import pandas as pd

# Load original dataset
df_raw = pd.read_csv('dataset/datawave_music.csv')
print(f"Original dataset: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")

# Load cleaned dataset
df_clean = pd.read_csv('cleaned_data/datawave_cleaned.csv')
print(f"Cleaned dataset: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")

# Optional: Check missing values before and after
print("\nMissing values in original dataset:")
print(df_raw.isna().sum())

print("\nMissing values in cleaned dataset:")
print(df_clean.isna().sum())
