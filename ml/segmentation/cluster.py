import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the prepared customer features
df = pd.read_csv("ml/segmentation/customer_features.csv")

# Select features for clustering
features = ["total_spent", "order_count", "avg_basket_size", "recency"]
X = df[features]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply KMeans clustering
k = 4  # You can change this value later if needed
kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
df["cluster"] = kmeans.fit_predict(X_scaled)

# Save the clustered data to a new CSV file
df.to_csv("ml/segmentation/customer_segments.csv", index=False)

print(f"Clustering complete. {k} customer segments created.")
