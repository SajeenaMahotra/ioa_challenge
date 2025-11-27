import pandas as pd
import numpy as np

df = pd.read_pickle('analysis/cleaned_df.pkl')

print("EXPLORATORY DATA ANALYSIS")

print("1. Subscription Distribution")
print(df['subscription_type'].value_counts())

print("\n2. Churn Rate by Subscription")
churn_by_sub = df.groupby('subscription_type')['churned'].mean().sort_values(ascending=False)
print(churn_by_sub.round(3))

print("\n3. Average Listening Hours by Subscription")
print(df.groupby('subscription_type')['avg_listening_hours_per_week'].mean().round(1).sort_values(ascending=False))

print("\n4. Top 10 Countries by User Count")
print(df['country'].value_counts().head(10))

print("\n5. Churn Rate by Country (Top 10 highest)")
print(df.groupby('country')['churned'].mean().sort_values(ascending=False).head(10).round(3))

print("\n6. Satisfaction vs Churn")
print(df.groupby('satisfaction_score')['churned'].mean().round(3))

print("\n7. Skip Rate Impact")
bins = [0, 0.1, 0.25, 0.5, 1.0]
labels = ['<10%', '10-25%', '25-50%', '>50%']
df['skip_group'] = pd.cut(df['skip_rate'], bins=bins, labels=labels, include_lowest=True)
print(df.groupby('skip_group')['churned'].mean().round(3))