import pandas as pd
import matplotlib.pyplot as plt
import os

# Load dataset
df = pd.read_csv('cleaned_data/datawave_analyzed.csv')
os.makedirs('visualizations', exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 10))

# Hours listened by subscription type
hours_sub = df.groupby('subscription_type')['avg_listening_hours_per_week'].mean().sort_values(ascending=False)
axes[1].bar(range(len(hours_sub)), hours_sub.values, color='#9b59b6')
axes[1].set_xticks(range(len(hours_sub)))
axes[1].set_xticklabels(hours_sub.index, rotation=45, ha='right')
axes[1].set_ylabel('Average Hours/Week')
axes[1].set_title('Average Listening Hours by Subscription Type', fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

# Engagement level distribution
engagement_counts = df['engagement_level'].value_counts()
axes[0].pie(engagement_counts, labels=engagement_counts.index, autopct='%1.1f%%',
               colors=['#e74c3c', '#f39c12', '#2ecc71', '#3498db'])
axes[0].set_title('User Engagement Levels', fontweight='bold')


plt.tight_layout()
#plt.savefig('charts/03_engagement_patterns.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
#print("✓ Saved: 03_engagement_patterns.png")
