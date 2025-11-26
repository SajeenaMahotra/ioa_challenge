"""
MUST-HAVE VISUALIZATION #1 — SKIP RATE ANALYSIS
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv('cleaned_data/datawave_cleaned.csv')
os.makedirs('visualizations', exist_ok=True)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_data/datawave_cleaned.csv')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

churned_skip = df[df['churned'] == 1]['skip_rate'].mean()
active_skip = df[df['churned'] == 0]['skip_rate'].mean()

skip_comparison = pd.DataFrame({
    'User Type': ['Active Users', 'Churned Users'],
    'Skip Rate': [active_skip, churned_skip]
})

colors = ['#2ecc71', '#e74c3c']
bars = axes[0].bar(skip_comparison['User Type'], skip_comparison['Skip Rate'],
                   color=colors, width=0.6)

axes[0].set_ylabel('Average Skip Rate (%)')
axes[0].set_title('Skip Rate: Active vs Churned Users')
axes[0].grid(axis='y', alpha=0.3)
axes[0].set_ylim(0, max(skip_comparison['Skip Rate']) * 1.2)

for bar, value in zip(bars, skip_comparison['Skip Rate']):
    axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                 f'{value:.1f}%', ha='center', va='bottom')

axes[1].hist([
    df[df['churned'] == 0]['skip_rate'].dropna(),
    df[df['churned'] == 1]['skip_rate'].dropna()
], bins=20, label=['Active', 'Churned'], alpha=0.7, color=colors)

axes[1].set_xlabel('Skip Rate (%)')
axes[1].set_ylabel('Number of Users')
axes[1].set_title('Skip Rate Distribution by User Status')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
plt.close()
#plt.savefig('charts/03_skip_rate.png', dpi=300, bbox_inches='tight')



