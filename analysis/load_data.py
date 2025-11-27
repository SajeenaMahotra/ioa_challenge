import pandas as pd

print("Loading cleaned dataset...")
df = pd.read_csv('cleaned_data/datawave_cleaned.csv')

print(f"Dataset loaded successfully!")
print(f"Shape: {df.shape[0]} users × {df.shape[1]} columns")

df['join_date'] = pd.to_datetime(df['join_date'])
print(f"Date range: {df['join_date'].min().date()} to {df['join_date'].max().date()}")

df.to_pickle('analysis/cleaned_df.pkl')
print("Saved as cleaned_df.pkl → ready for analysis!")