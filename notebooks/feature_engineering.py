import pandas as pd
from pathlib import Path

# Load cleaned data
input_path = Path("cleaned_data.csv")
output_path = Path("engineered_features.csv")
df = pd.read_csv(input_path, parse_dates=["InvoiceDate"])

# Compute a new column for total price
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Feature Engineering
now = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Group by CustomerID
features = (
    df.groupby("CustomerID")
    .agg(
        total_spent=("TotalPrice", "sum"),
        order_count=("InvoiceNo", "nunique"),
        avg_basket_size=("Quantity", "mean"),
        recency_days=("InvoiceDate", lambda x: (now - x.max()).days),
    )
    .reset_index()
)

# Save to CSV
features.to_csv(output_path, index=False)
print(f"✅ Engineered features saved to {output_path.resolve()}")
