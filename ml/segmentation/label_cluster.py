import pandas as pd

# Load the customer_segments.csv
df = pd.read_csv("ml/segmentation/customer_segments.csv")

# Define cluster labels based on your interpretation
cluster_labels = {
    0: "Typical Active Buyers",
    1: "Dormant / At-Risk Buyers",
    2: "Anomaly or Outlier",
    3: "Elite VIP Customers",
}

# Add a new column called "segment"
df["segment"] = df["cluster"].map(cluster_labels)

# Save updated file
df.to_csv("ml/segmentation/labeled_customer_segments.csv", index=False)

print("✅ Customer segments labeled and saved to 'labeled_customer_segments.csv'")
