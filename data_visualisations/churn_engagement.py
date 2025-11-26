import pandas as pd
import matplotlib.pyplot as plt
import os

# Load dataset
df = pd.read_csv('cleaned_data/datawave_analyzed.csv')
os.makedirs('visualizations', exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 10))

# churn by engagement level
churned_eng = df.groupby('engagement_level')['churned'].mean() * 100
axes[1].bar(range(len(churned_eng)), churned_eng.values, color='#e67e22')
axes[1].set_xticks(range(len(churned_eng)))
axes[1].set_xticklabels(churned_eng.index, rotation=45, ha='right')
axes[1].set_ylabel('Churn Rate (%)')
axes[1].set_title('Churn Rate by Engagement Level', fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

# Hours listened: Active vs Churned
box_data = [df[df['churned'] == 0]['avg_listening_hours_per_week'].dropna(),
            df[df['churned'] == 1]['avg_listening_hours_per_week'].dropna()]
bp = axes[0].boxplot(box_data, labels=['Active', 'churneded'], patch_artist=True)
for patch, color in zip(bp['boxes'], ['#2ecc71', '#e74c3c']):
    patch.set_facecolor(color)
axes[0].set_ylabel('Hours Listened/Week')
axes[0].set_title('Listening Hours: Active vs churneded Users', fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

plt.tight_layout()
#plt.savefig('charts/03_engagement_patterns.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
#print("✓ Saved: 03_engagement_patterns.png")