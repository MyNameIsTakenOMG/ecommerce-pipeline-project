from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_s3 as s3,
    aws_kinesis as kinesis,
    aws_kinesisfirehose as firehose,
    aws_s3_notifications as s3n,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as lambda_py,
    aws_iam as iam,
)
from constructs import Construct


class KinesisPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # S3 bucket for the raw data
        raw_bucket = s3.Bucket(
            self,
            "RawDataBucket",
            versioned=False,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Kinesis Data Stream for the raw data
        stream = kinesis.Stream(
            self,
            "RetailRawDataStream",
            encryption=kinesis.StreamEncryption.UNENCRYPTED,
            removal_policy=RemovalPolicy.DESTROY,
            stream_mode=kinesis.StreamMode.ON_DEMAND,
        )
        # Firehose role
        firehose_role = iam.Role(
            self,
            "FirehoseRole",
            assumed_by=iam.ServicePrincipal("firehose.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonKinesisReadOnlyAccess"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )

        # Prefix for the S3 bucket
        prefix = "lake/raw/stream/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/"
        # Error Prefix for the S3 bucket
        error_prefix = "lake/raw/stream/errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/!{firehose:error-output-type}/"

        # Firehose Delivery Stream
        firehose.DeliveryStream(
            self,
            "RetailFirehoseToS3",
            role=firehose_role,
            source=firehose.KinesisStreamSource(stream),
            destination=firehose.S3Bucket(
                bucket=raw_bucket,
                data_output_prefix=prefix,
                error_output_prefix=error_prefix,
            ),
        )

        # # etl handler lambda layer (using the aws pre-built layer for AWS SDK for Pandas)
        # etl_layer = _lambda.LayerVersion.from_layer_version_arn(
        #     self,
        #     "ETLLayer",
        #     "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:17",
        # )

        # # Lambda function for auto-ETL processing
        # etl_fn = _lambda.Function(
        #     self,
        #     "ETLFunction",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     timeout=Duration.minutes(3),
        #     handler="etl_handler.lambda_handler",
        #     code=_lambda.Code.from_asset("functions"),
        #     memory_size=256,
        #     layers=[etl_layer],
        #     environment={
        #         "RAW_BUCKET": raw_bucket.bucket_name,
        #         "RAW_PREFIX": "lake/raw/batch/",
        #         "CLEAN_PREFIX": "lake/clean/batch/",
        #         "GLUE_DATABASE": "ecommerce_data_lake",
        #         "GLUE_TABLE": "clean_batch",
        #     },
        #     initial_policy=[
        #         iam.PolicyStatement(
        #             actions=[
        #                 "glue:GetTable",
        #                 "glue:GetTables",
        #                 "glue:CreateTable",
        #                 "glue:UpdateTable",
        #                 "glue:GetDatabase",
        #                 "s3:DeleteObject",
        #             ],
        #             resources=["*"],
        #         )
        #     ],
        # )
        # # needs docker to bundle the python lambda function with dependencies
        # etl_fn = lambda_py.PythonFunction(
        #     self,
        #     "ETLFunction",
        #     entry="functions",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     index="etl_handler.py",
        #     timeout=Duration.seconds(30),
        #     environment={
        #         "RAW_BUCKET": raw_bucket.bucket_name,
        #         "RAW_PREFIX": "lake/raw/bathc/",
        #         "CLEAN_PREFIX": "lake/clean/batch/",
        #         "GLUE_DATABASE": "ecommerce_data_lake",
        #         "GLUE_TABLE": "clean_batch",
        #     },
        #     initial_policy=[
        #         iam.PolicyStatement(
        #             actions=[
        #                 "glue:GetTable",
        #                 "glue:GetTables",
        #                 "glue:CreateTable",
        #                 "glue:UpdateTable",
        #                 "glue:GetDatabase",
        #             ],
        #             resources=["*"],
        #         )
        #     ],
        # )

        # # NOTE: to use s3 notification with lambda, must increase the lambda memory size and timeout
        # # Grant the Lambda function permissions to read and write from the raw S3 bucket
        # raw_bucket.grant_read(etl_fn)
        # raw_bucket.grant_put(etl_fn)

        # # Configure S3 notifications to trigger the Lambda function
        # raw_bucket.add_event_notification(
        #     s3.EventType.OBJECT_CREATED,
        #     s3n.LambdaDestination(etl_fn),
        #     s3.NotificationKeyFilter(prefix="lake/raw/batch/", suffix=".csv"),
        # )
