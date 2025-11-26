import pandas as pd
from matplotlib import pyplot as plt

# Load data
df = pd.read_csv('cleaned_data/datawave_analyzed.csv')

# Ensure churned is numeric
df['churned'] = df['churned'].astype(str).str.strip().str.lower()
df['churned'] = df['churned'].replace({'yes': 1, 'no': 0})
df['churned'] = pd.to_numeric(df['churned'], errors='coerce')

# Drop NaNs in satisfaction_score
df = df.dropna(subset=['satisfaction_score'])

# Split data
sat_data = df.groupby('churned')['satisfaction_score'].apply(list)
active_scores = sat_data.get(0, [])
churned_scores = sat_data.get(1, [])

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram: Active vs Churned
axes[0].hist([active_scores, churned_scores],
             bins=5, label=['Active', 'Churned'], alpha=0.7)
axes[0].set_xlabel('Satisfaction Score')
axes[0].set_ylabel('Count')
axes[0].set_title('Satisfaction Score Distribution')
axes[0].legend()

# Average satisfaction by subscription type
sat_sub = df.groupby('subscription_type')['satisfaction_score'].mean().sort_values()
colors = ['#3498db' if x < df['satisfaction_score'].mean() else '#2ecc71' for x in sat_sub.values]
axes[1].barh(sat_sub.index, sat_sub.values, color=colors)
axes[1].axvline(df['satisfaction_score'].mean(), color='black', linestyle='--', label='Overall Average', linewidth=2)
axes[1].set_xlabel('Average Satisfaction Score')
axes[1].set_title('Average Satisfaction by Subscription Type')
axes[1].legend()

plt.tight_layout()
plt.show()
#plt.savefig('charts/02_satisfaction_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
#print("✓ Saved: 02_satisfaction_analysis.png")

