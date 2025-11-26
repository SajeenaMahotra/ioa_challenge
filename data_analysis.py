import pandas as pd
import numpy as np
from scipy import stats


print("DATA ANALYSIS - DataWave Music Challenge")

# Load cleaned dataset
df = pd.read_csv('cleaned_data/datawave_cleaned.csv')
print(f"Analyzing {df.shape[0]} users across {df.shape[1]} features\n")

# ANALYSIS 1: churned
churned_rate = df['churned'].mean() * 100
print(f"Overall churned Rate: {churned_rate:.2f}%")
print(f"Active Users: {(df['churned']==0).sum()}, churneded Users: {(df['churned']==1).sum()}")

print("\nchurned by Subscription Type:")
churned_sub = df.groupby('subscription_type')['churned'].agg(['mean','count'])
churned_sub['churned_rate'] = churned_sub['mean']*100
print(churned_sub.sort_values('churned_rate', ascending=False))

if 'region' in df.columns:
    print("\nchurned by Region:")
    churned_region = df.groupby('region')['churned'].agg(['mean','count'])
    churned_region['churned_rate'] = churned_region['mean']*100
    print(churned_region.sort_values('churned_rate', ascending=False))

# ANALYSIS 2: Satisfaction
avg_satisfaction = df['satisfaction_score'].mean()
print(f"\nAverage Satisfaction Score: {avg_satisfaction:.2f}/10")

print("\nSatisfaction by Subscription Type:")
sat_sub = df.groupby('subscription_type')['satisfaction_score'].agg(['mean','median','count'])
print(sat_sub.sort_values('mean', ascending=False))

churneded_scores = df[df['churned']==1]['satisfaction_score'].dropna()
active_scores = df[df['churned']==0]['satisfaction_score'].dropna()
print(f"\nSatisfaction churneded vs Active: {churneded_scores.mean():.2f} vs {active_scores.mean():.2f}")
t_stat, p_value = stats.ttest_ind(active_scores, churneded_scores)
print(f"T-test p-value: {p_value:.4f}")

# ANALYSIS 3: Engagement
avg_hours = df['avg_listening_hours_per_week'].mean()
print(f"\nAverage Hours Listened per Week: {avg_hours:.2f}")

hours_sub = df.groupby('subscription_type')['avg_listening_hours_per_week'].agg(['mean','median','count'])
print(hours_sub.sort_values('mean', ascending=False))

churneded_hours = df[df['churned']==1]['avg_listening_hours_per_week'].mean()
active_hours = df[df['churned']==0]['avg_listening_hours_per_week'].mean()
print(f"Hours Listened churneded vs Active: {churneded_hours:.2f} vs {active_hours:.2f}")

df['engagement_level'] = pd.cut(df['avg_listening_hours_per_week'], bins=[0,5,15,30,200],
                                labels=['Low','Medium','High','Very High'])
print("\nEngagement Distribution:")
print(df['engagement_level'].value_counts().sort_index())

print("\nchurned Rate by Engagement Level:")
print(df.groupby('engagement_level')['churned'].mean()*100)

# ANALYSIS 5: Age
print(f"\nAge Statistics: Mean={df['age'].mean():.1f}, Median={df['age'].median():.1f}, Range={df['age'].min():.0f}-{df['age'].max():.0f}")
df['age_group'] = pd.cut(df['age'], bins=[0,18,25,35,50,100], labels=['13-18','19-25','26-35','36-50','51+'])
print("\nAge Group Distribution:")
print(df['age_group'].value_counts().sort_index())
print("\nchurned Rate by Age Group:")
print(df.groupby('age_group')['churned'].mean()*100)


# ANALYSIS 7: Correlations
numeric_cols = ['age','avg_listening_hours_per_week','satisfaction_score','churned']
print("\nCorrelation with churned:")
print(df[numeric_cols].corr()['churned'].sort_values(ascending=False))

# ANALYSIS 8: High-Risk Profile
churneded_users = df[df['churned']==1]
print("\nHigh-Risk User Profile:")
print(f"Average Satisfaction: {churneded_users['satisfaction_score'].mean():.2f}")
print(f"Average Hours Listened: {churneded_users['avg_listening_hours_per_week'].mean():.2f}")
print(f"Most Common Subscription: {churneded_users['subscription_type'].mode()[0]}")
print(f"Average Age: {churneded_users['age'].mean():.1f}")

# Save summary and enhanced dataset
results = {
    'overall_churned_rate': churned_rate,
    'avg_satisfaction': avg_satisfaction,
    'avg_listening_hours_per_week': avg_hours,
    'churneded_satisfaction': churneded_scores.mean(),
    'active_satisfaction': active_scores.mean(),
    'churneded_hours': churneded_hours,
    'active_hours': active_hours
}
pd.DataFrame([results]).to_csv('cleaned_data/analysis_summary.csv', index=False)
df.to_csv('cleaned_data/datawave_analyzed.csv', index=False)

print("DATA ANALYSIS COMPLETE")


