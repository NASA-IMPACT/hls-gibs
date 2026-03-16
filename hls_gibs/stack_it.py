from typing import Optional

from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class NotificationITStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        managed_policy_name: Optional[str] = None,
    ) -> None:
        super().__init__(scope, construct_id)

        if managed_policy_name:
            iam.PermissionsBoundary.of(self).apply(
                iam.ManagedPolicy.from_managed_policy_name(
                    self,
                    "PermissionsBoundary",
                    managed_policy_name,
                )
            )

        self.bucket = s3.Bucket(
            self,
            "MockHlsBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        self.queue = sqs.Queue(self, "MockGibsQueue", fifo=True)

        # Set outputs for use within integration tests

        CfnOutput(self, "HlsBucketName", value=self.bucket.bucket_name)
        CfnOutput(self, "GibsQueueUrl", value=self.queue.queue_url)
