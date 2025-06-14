import pandas as pd
from pathlib import Path

# Load raw data (same one used for ML prep)
input_path = Path("../temp.csv")
output_path = Path("cleaned_data.csv")

# Load data
df = pd.read_csv(input_path)

print("🔍 Before cleaning:")
print(df.info())
print(df.head())

# Drop rows with missing critical fields
df = df.dropna(
    subset=["CustomerID", "InvoiceDate", "Description", "StockCode", "Quantity"]
)

# Convert types
df["CustomerID"] = df["CustomerID"].astype(str)
df["StockCode"] = df["StockCode"].astype(str)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Drop any rows with invalid InvoiceDate
df = df.dropna(subset=["InvoiceDate"])

# Standardize string fields
df["Country"] = df["Country"].str.strip().str.lower()
df["Description"] = df["Description"].str.strip().str.lower()

# Remove duplicates
df = df.drop_duplicates()

# Filter out rows with non-positive quantity or unit price
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Save cleaned data
df.to_csv(output_path, index=False)
print(f"✅ Cleaned data saved to {output_path.resolve()}")
