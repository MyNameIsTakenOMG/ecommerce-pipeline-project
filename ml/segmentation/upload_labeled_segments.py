# upload_segment_csv.py
import boto3
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

bucket_name = os.getenv("RAW_BUCKET_NAME")

s3_prefix = "lake/analytics/customer_segments/"
local_path = Path("ml/segmentation/labeled_customer_segments.csv")

s3 = boto3.client("s3")

s3.upload_file(
    Filename=str(local_path), Bucket=bucket_name, Key=f"{s3_prefix}{local_path.name}"
)

print("Upload complete.")
