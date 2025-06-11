from aws_cdk import (
    # Duration,
    RemovalPolicy,
    Stack,
    aws_s3 as s3,
    aws_kinesis as kinesis,
    aws_kinesisfirehose as firehose,
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

        self.bucket_name = raw_bucket.bucket_name
        self.stream_name = stream.stream_name
