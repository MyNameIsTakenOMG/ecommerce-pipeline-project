import awswrangler as wr
import pandas as pd
from pathlib import Path

glue_database = "ecommerce_data_lake"
glue_table = "clean_batch"

# Read from Glue Catalog
df = wr.s3.read_parquet_table(database=glue_database, table=glue_table)

print(df.columns)

# Convert invoicedate
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# Feature engineering
snapshot_date = df["invoicedate"].max() + pd.Timedelta(days=1)

customer_df = (
    df.groupby("customerid")
    .agg(
        total_spent=pd.NamedAgg(
            column="unitprice",
            aggfunc=lambda x: (x * df.loc[x.index, "quantity"]).sum(),
        ),
        order_count=pd.NamedAgg(column="invoiceno", aggfunc=pd.Series.nunique),
        avg_basket_size=pd.NamedAgg(column="quantity", aggfunc="mean"),
        recency=pd.NamedAgg(
            column="invoicedate", aggfunc=lambda x: (snapshot_date - x.max()).days
        ),
    )
    .reset_index()
)

# Save locally
output_path = Path(__file__).parent / "customer_features.csv"
customer_df.to_csv(output_path, index=False)
print(f"Saved: {output_path}")
