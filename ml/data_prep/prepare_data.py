import awswrangler as wr
import pandas as pd
import os

# Config
DATABASE = "ecommerce_data_lake"
TABLE = "clean_batch"
LOCAL_OUTPUT = "ml/data_prep/prepared_data.csv"


def main():
    # Step 1: Read cleaned data from Glue Catalog table
    print("Loading data from Glue Catalog...")
    df = wr.s3.read_parquet_table(database=DATABASE, table=TABLE)

    print(df.columns)
    # Step 2: Basic feature engineering
    print("Engineering features...")
    df["invoice_amount"] = df["quantity"] * df["unitprice"]
    df["product_key"] = df["invoiceno"].astype(str) + "_" + df["stockcode"].astype(str)

    invoice_df = (
        df.groupby("invoiceno")
        .agg(
            customer_id=("customerid", "first"),
            country=("country", "first"),
            invoice_date=("invoicedate", "first"),
            total_amount=("invoice_amount", "sum"),
            product_count=("product_key", "nunique"),
        )
        .reset_index()
    )

    # Step 3: Create binary classification label
    invoice_df["is_high_value"] = (invoice_df["total_amount"] > 200).astype(int)

    print(invoice_df.head())

    # Step 4: Save to local CSV (for now)
    os.makedirs(os.path.dirname(LOCAL_OUTPUT), exist_ok=True)
    invoice_df.to_csv(LOCAL_OUTPUT, index=False)
    print(f"Saved prepared dataset to {LOCAL_OUTPUT}")


if __name__ == "__main__":
    main()
