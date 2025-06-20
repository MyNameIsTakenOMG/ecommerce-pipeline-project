import boto3
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

bucket_name = os.getenv("RAW_BUCKET_NAME")

s3 = boto3.client("s3")

# Read and convert to CSV
df = pd.read_excel(Path("data/online_retail.xlsx"))
df.dropna(
    subset=[
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ],
    inplace=True,
)

date_str = datetime.now(timezone.utc).strftime("year=%Y/month=%m/day=%d")
key = f"lake/raw/batch/{date_str}/online_retail.csv"

# Save locally then upload
local_path = Path("temp.csv")
df.to_csv(local_path, index=False)

s3.upload_file(str(local_path), bucket_name, key)
print(f"✅ Uploaded to s3://{bucket_name}/{key}")
