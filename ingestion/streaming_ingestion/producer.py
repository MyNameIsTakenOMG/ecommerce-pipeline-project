import boto3
import json
import pandas as pd
import time
import random
from pathlib import Path

# === CONFIG ===
STREAM_NAME = "KinesisPipelineStack-RetailRawDataStream05819AA3-Y4TRcxabQiB3"  # your actual stream name
REGION = "us-east-1"  # update if not us-east-1
FILE_PATH = Path("data/online_retail.xlsx")  # adjust if stored elsewhere

# === INIT KINESIS CLIENT ===
kinesis = boto3.client("kinesis", region_name=REGION)

# === LOAD A FEW RECORDS ===
df = pd.read_excel(FILE_PATH)

# Clean up NaNs
df = df.dropna(
    subset=[
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]
)

# Sample 20 records for testing
sample = df.sample(n=20, random_state=42)

# === SEND TO KINESIS ===
for _, row in sample.iterrows():
    record = {
        "invoice_no": str(row.InvoiceNo),
        "stock_code": str(row.StockCode),
        "description": row.Description,
        "quantity": int(row.Quantity),
        "unit_price": float(row.UnitPrice),
        "invoice_date": str(row.InvoiceDate),
        "customer_id": int(row.CustomerID),
        "country": row.Country,
    }

    partition_key = str(random.randint(1, 100))  # simple random key

    print(f"Sending: {record}")
    response = kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(record),
        PartitionKey=partition_key,
    )

    time.sleep(1)  # simulate stream delay

print("✅ Done sending records.")
