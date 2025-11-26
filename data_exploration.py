import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import os
print("Current directory:", os.getcwd())

# Load dataset - file is in current directory, not in dataset subfolder
df = pd.read_csv('dataset/datawave_music.csv')  # Changed from 'dataset/datawave_music.csv'

# Dataset overview
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])
print("Columns:", df.columns.tolist())

# First few rows
print(df.head(10))

# Data types
print(df.dtypes)

# Basic statistics
print(df.describe(include='all'))

# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing_Count': missing, 'Percentage': missing_pct})
print(missing_df[missing_df['Missing_Count'] > 0])

# Duplicate user_ids
if 'user_id' in df.columns:
    duplicates = df['user_id'].duplicated().sum()
    print("Duplicate user_ids:", duplicates)
    if duplicates > 0:
        print(df[df['user_id'].duplicated(keep=False)].head(10))

# Unique values in categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"\n{col}: {df[col].nunique()} unique values")
    print(df[col].value_counts().head(10))

# Numeric columns summary
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    print(f"\n{col}: Min={df[col].min()}, Max={df[col].max()}, Mean={df[col].mean():.2f}, Median={df[col].median()}")