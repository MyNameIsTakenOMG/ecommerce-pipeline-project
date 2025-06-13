import json
from aws_cdk import (
    # Duration,
    Stack,
    aws_glue as glue,
    aws_iam as iam,
)
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()
bucket_name = os.getenv("RAW_BUCKET_NAME")


class GlueCatalogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # Glue Database for the raw data
        glue_database = glue.CfnDatabase(
            self,
            "RetailRawDataDatabase",
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name="ecommerce_data_lake",  # your database name, all lowercase, no spaces
                description="Glue database for ecommerce data lake",
                # You can omit parameters like locationUri and parameters for now
            ),
            catalog_id=self.account,
        )
        # Glue Cralwer Role
        glue_cralwer_role = iam.Role(
            self,
            "GlueCrawlerRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSGlueServiceRole"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )
        # Glue Crawler for the raw data
        glue_cralwer = glue.CfnCrawler(
            self,
            "RetailRawDataCrawler",
            role=glue_cralwer_role.role_arn,
            database_name=glue_database.ref,
            targets={
                "s3Targets": [
                    {"path": f"s3://{bucket_name}/lake/raw/batch/"},
                    # {"path": f"s3://{bucket_name}/lake/raw/stream/"}, # Uncomment if you have a stream path
                    {"path": f"s3://{bucket_name}/lake/analytics/customer_segments/"},
                ]
            },
            schema_change_policy={
                "updateBehavior": "UPDATE_IN_DATABASE",
                "deleteBehavior": "LOG",
            },
            configuration=json.dumps(
                {
                    "Version": 1.0,
                    "CrawlerOutput": {
                        "Partitions": {
                            "AddOrUpdateBehavior": "InheritFromTable",
                        }
                    },
                }
            ),
            # You can add more configurations as needed
        )
