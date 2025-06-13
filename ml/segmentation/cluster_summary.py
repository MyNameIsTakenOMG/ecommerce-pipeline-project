import pandas as pd

# Load the segmented data
df = pd.read_csv("ml/segmentation/customer_segments.csv")

# Group by cluster and compute the average for each feature
summary = (
    df.groupby("cluster")
    .agg(
        {
            "total_spent": "mean",
            "order_count": "mean",
            "avg_basket_size": "mean",
            "recency": "mean",
            "customerid": "count",  # Number of customers per cluster
        }
    )
    .rename(columns={"customerid": "num_customers"})
)

# Round for better readability
summary = summary.round(2)

# Print the summary
print("Cluster Summary:\n")
print(summary)
