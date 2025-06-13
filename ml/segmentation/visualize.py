import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the customer segments
df = pd.read_csv("ml/segmentation/customer_segments.csv")

# Features used for clustering
features = ["total_spent", "order_count", "avg_basket_size", "recency"]
X = df[features]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reduce dimensions to 2 for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Add PCA components to the dataframe
df["PC1"] = X_pca[:, 0]
df["PC2"] = X_pca[:, 1]

# Plotting
plt.figure(figsize=(10, 6))
for cluster_id in df["cluster"].unique():
    cluster_data = df[df["cluster"] == cluster_id]
    plt.scatter(
        cluster_data["PC1"],
        cluster_data["PC2"],
        label=f"Cluster {cluster_id}",
        alpha=0.7,
    )

plt.title("Customer Segments (PCA Projection)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
