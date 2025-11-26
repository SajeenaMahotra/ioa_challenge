import pandas as pd
import matplotlib.pyplot as plt
import os

# Load dataset
df = pd.read_csv('cleaned_data/datawave_analyzed.csv')
os.makedirs('visualizations', exist_ok=True)

# churned pie chart & by subscription type
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

churned_counts = df['churned'].value_counts()
colors = ['#2ecc71', '#e74c3c']
axes[0].pie(churned_counts, labels=['Active', 'Churned'], autopct='%1.1f%%',
            colors=colors, startangle=90)
axes[0].set_title('Overall Churn Distribution', fontsize=14, fontweight='bold')

churned_sub = df.groupby('subscription_type')['churned'].mean() * 100
churned_sub = churned_sub.sort_values(ascending=True)
axes[1].barh(churned_sub.index, churned_sub.values, color='#e74c3c')
axes[1].set_xlabel('Churn Rate (%)')
axes[1].set_title('Churn Rate by Subscription Type', fontsize=14, fontweight='bold')
axes[1].axvline(df['churned'].mean() * 100, color='black', linestyle='--', label='Overall Average', linewidth=2)
axes[1].legend()

plt.tight_layout()
plt.show()
#plt.savefig('charts/01_churned_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 01_churned_overview.png")


