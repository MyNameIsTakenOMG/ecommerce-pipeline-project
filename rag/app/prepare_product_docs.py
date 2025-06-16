# rag/app/generate_product_knowledge.py

import pandas as pd
from pathlib import Path
from datetime import datetime

# Load raw dataset
df = pd.read_csv("../../temp.csv")

# Basic cleanup
df = df.dropna(subset=["StockCode", "Description", "Quantity", "UnitPrice"])
df["Description"] = df["Description"].str.strip().str.title()
df["Country"] = df["Country"].str.lower().str.strip()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Generate a global document summary for all products
grouped = (
    df.groupby("StockCode")
    .agg(
        {
            "Description": "first",
            "Quantity": "sum",
            "TotalPrice": "sum",
            "InvoiceDate": ["min", "max"],
            "Country": lambda x: list(set(x)),
        }
    )
    .reset_index()
)

grouped.columns = [
    "StockCode",
    "Description",
    "TotalQuantity",
    "TotalRevenue",
    "FirstInvoiceDate",
    "LastInvoiceDate",
    "CountriesSold",
]

# Format into a single document string
lines = []
lines.append("# Product Knowledge Base\n")
lines.append(f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")

for _, row in grouped.iterrows():
    lines.append(f"## Product: {row['Description']} (StockCode: {row['StockCode']})")
    lines.append(f"- **Total Quantity Sold:** {int(row['TotalQuantity'])}")
    lines.append(f"- **Total Revenue:** £{row['TotalRevenue']:.2f}")
    lines.append(
        f"- **Available In Countries:** {', '.join(sorted(row['CountriesSold']))}"
    )
    lines.append(
        f"- **Sales Period:** {row['FirstInvoiceDate'].date()} → {row['LastInvoiceDate'].date()}"
    )
    lines.append("")

# Save the document
output_path = Path("product_knowledge.md")
Path(output_path).write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Product knowledge document saved to: {output_path.resolve()}")
