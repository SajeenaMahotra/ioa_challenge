# analysis/04_visualizations.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_pickle('analysis/cleaned_df.pkl')
os.makedirs('presentation_charts', exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Chart 1: Churn by Subscription
plt.figure()
order = df.groupby('subscription_type')['churned'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='subscription_type', y='churned', order=order, palette='Reds_d')
plt.title('Churn Rate by Subscription Type', fontsize=18, fontweight='bold')
plt.ylabel('Churn Rate')
plt.xlabel('')
plt.ylim(0, 0.5)
for i, v in enumerate(df.groupby('subscription_type')['churned'].mean().sort_values(ascending=False)):
    plt.text(i, v + 0.01, f"{v:.1%}", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('presentation_charts/1_churn_by_subscription.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: Listening Hours vs Churn
plt.figure()
sns.barplot(data=df, x='subscription_type', y='avg_listening_hours_per_week', 
            order=df.groupby('subscription_type')['avg_listening_hours_per_week'].mean().sort_values(ascending=False).index,
            palette='Blues_d')
plt.title('Average Weekly Listening Hours by Subscription', fontsize=18, fontweight='bold')
plt.ylabel('Hours per Week')
plt.xlabel('')
plt.tight_layout()
plt.savefig('presentation_charts/2_listening_hours.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Satisfaction vs Churn
plt.figure()
df['sat_group'] = df['satisfaction_score'].apply(lambda x: '≤ 3' if x <= 3 else '4–10')
rates = df.groupby('sat_group')['churned'].mean().reindex(['≤ 3', '4–10'])
ax = rates.plot(kind='bar', color=['#d62728', '#1f77b4'], width=0.5)
plt.title('Churn Rate by Satisfaction Score', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Churn Rate')
plt.xlabel('Satisfaction Score')
plt.xticks(rotation=0)
plt.ylim(0, 1)
for i, v in enumerate(rates):
    ax.text(i, v + 0.02, f'{v:.1%}', ha='center', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig('presentation_charts/3_satisfaction_churn.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4: Skip Rate vs Churn
plt.figure()
bins = [0, 0.1, 0.25, 0.5, 1.0]
labels = ['<10%', '10-25%', '25-50%', '>50%']
df['skip_group'] = pd.cut(df['skip_rate'], bins=bins, labels=labels, include_lowest=True)
sns.barplot(data=df, x='skip_group', y='churned', palette='Oranges_d')
plt.title('Higher Skip Rate = Massive Churn', fontsize=18, fontweight='bold')
plt.xlabel('Skip Rate')
plt.ylabel('Churn Rate')
plt.tight_layout()
plt.savefig('presentation_charts/4_skip_rate_churn.png', dpi=300, bbox_inches='tight')
plt.close()

print("DONE VISULISATION ")