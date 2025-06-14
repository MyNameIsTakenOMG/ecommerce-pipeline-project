import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load engineered features
df = pd.read_csv("engineered_features.csv")

# Set plot style
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

# 1. Total spent vs. order count
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="order_count", y="total_spent")
plt.title("Total Spent vs. Order Count")
plt.savefig("notebooks_visual/fig_total_spent_vs_order_count.png")
plt.close()

# 2. Total spent vs. avg basket size
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="avg_basket_size", y="total_spent")
plt.title("Total Spent vs. Avg Basket Size")
plt.savefig("notebooks_visual/fig_total_spent_vs_avg_basket_size.png")
plt.close()

# 3. Recency vs. total spent
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="recency_days", y="total_spent")
plt.title("Recency vs. Total Spent")
plt.savefig("notebooks_visual/fig_recency_vs_total_spent.png")
plt.close()

# 4. Correlation heatmap
plt.figure(figsize=(6, 5))
corr = df.drop(columns=["CustomerID"]).corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Customer Features")
plt.tight_layout()
plt.savefig("notebooks_visual/fig_correlation_matrix.png")
plt.close()

print("✅ All visualizations saved to the 'notebooks_visual/' folder.")
