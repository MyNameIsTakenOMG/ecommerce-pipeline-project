import pandas as pd
from pathlib import Path

# Load raw data
raw_path = Path("temp.csv")  # Adjust path if necessary
df = pd.read_csv(raw_path)

# Basic cleaning
df = df.dropna(subset=["CustomerID", "InvoiceDate", "Description"])
df["Country"] = df["Country"].str.lower().str.strip()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Convert CustomerID to string to avoid type mismatch
df["CustomerID"] = df["CustomerID"].astype(str)
df["StockCode"] = df["StockCode"].astype(str)

# Create the user-item interaction data: sum of quantity per (CustomerID, StockCode)
interaction_df = (
    df.groupby(["CustomerID", "StockCode"])["Quantity"]
    .sum()
    .reset_index()
    .rename(columns={"Quantity": "TotalQuantity"})
)

# Save to CSV
output_path = Path("ml/recommendation/user_item_interactions.csv")
interaction_df.to_csv(output_path, index=False)

print(f"✅ user_item_interactions.csv saved to {output_path.resolve()}")
