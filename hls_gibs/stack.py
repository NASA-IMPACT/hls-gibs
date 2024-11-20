from typing import Optional

from aws_cdk import Duration, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class NotificationStack(Stack):
    def __init__(
        self,
        scope: Construct,
        stack_name: str,
        *,
        hls_bucket_name: str,
        gibs_queue_arn: str,
        managed_policy_name: Optional[str] = None,
    ) -> None:
        super().__init__(scope, stack_name)

        if managed_policy_name:
            iam.PermissionsBoundary.of(self).apply(
                iam.ManagedPolicy.from_managed_policy_name(
                    self,
                    "PermissionsBoundary",
                    managed_policy_name,
                )
            )

        # Define resources

        self.hls_bucket = s3.Bucket.from_bucket_name(self, "HlsBucket", hls_bucket_name)
        self.gibs_queue = sqs.Queue.from_queue_arn(
            self, "GibsQueue", queue_arn=gibs_queue_arn
        )
        self.notification_function = lambda_.Function(
            self,
            "GibsNotifier",
            code=lambda_.Code.from_asset("hls_gibs/forward"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            memory_size=128,
            timeout=Duration.seconds(30),
            environment=dict(
                GIBS_QUEUE_URL=self.gibs_queue.queue_url,
            ),
        )

        # Wire everything up

        self.gibs_queue.grant_send_messages(self.notification_function)
        self.hls_bucket.grant_read(self.notification_function)
        self.hls_bucket.add_object_created_notification(
            s3n.LambdaDestination(self.notification_function),  # pyright: ignore
            s3.NotificationKeyFilter(suffix=".json"),
        )
