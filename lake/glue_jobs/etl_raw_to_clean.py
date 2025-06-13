import awswrangler as wr
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

bucket_name = os.getenv("RAW_BUCKET_NAME")

# Get the s3 location for the catalog table
s3_path = wr.catalog.get_table_location(
    database="ecommerce_data_lake",
    table="batch",  # e.g., raw_online_retail
)

# Read from Glue Catalog table
df = wr.s3.read_csv(
    path=s3_path,
)

print(df.columns)

# Basic transformations
df = df.dropna(subset=["CustomerID", "InvoiceDate", "Description"])
df["Country"] = df["Country"].str.lower().str.strip()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Write to a clean zone
wr.s3.to_parquet(
    df=df,
    path=f"s3://{bucket_name}/lake/clean/batch/",
    dataset=True,
    database="ecommerce_data_lake",
    table="clean_batch",
    mode="overwrite_partitions",
    partition_cols=["Country"],
)
