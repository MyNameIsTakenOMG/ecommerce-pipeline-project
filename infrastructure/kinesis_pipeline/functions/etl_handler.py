# etl_handler.py
import os
import json
import logging
import awswrangler as wr
import pandas as pd
from urllib.parse import unquote_plus

logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logger = logging.getLogger()
# logger.setLevel(logging.INFO)

RAW_BUCKET = os.environ["RAW_BUCKET"]
RAW_PREFIX = os.environ["RAW_PREFIX"]
CLEAN_PREFIX = os.environ["CLEAN_PREFIX"]
GLUE_DATABASE = os.environ["GLUE_DATABASE"]
GLUE_TABLE = os.environ["GLUE_TABLE"]


def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event))

    for record in event["Records"]:
        # !!! important: unquote_plus is used to decode the S3 object key.
        # The s3 object key name value is URL encoded.
        key = unquote_plus(record["s3"]["object"]["key"])
        if not key.endswith(".csv"):
            logger.info(f"Skipping non-CSV file: {key}")
            continue

        s3_path = f"s3://{RAW_BUCKET}/{key}"
        logger.info("Processing %s", s3_path)

        # --- Read raw CSV ---
        df = wr.s3.read_csv(path=s3_path)
        logger.info("Read raw data from %s", s3_path)
        # --- Clean / transform ---
        df = df.dropna(subset=["CustomerID", "InvoiceDate", "Description"])
        df["Country"] = df["Country"].str.lower().str.strip()
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        logger.info("Cleaned data: %d rows", len(df))
        # --- Write Parquet to clean zone ---
        clean_path = f"s3://{RAW_BUCKET}/{CLEAN_PREFIX}"
        wr.s3.to_parquet(
            df=df,
            path=clean_path,
            dataset=True,
            mode="overwrite_partitions",
            database=GLUE_DATABASE,
            table=GLUE_TABLE,
            partition_cols=["Country"],
        )

        logger.info("Written clean data to %s", clean_path)

    return {"status": "ok"}
