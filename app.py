#!/usr/bin/env python3
import os

from aws_cdk import App, Tags

from hls_gibs.stack import NotificationStack

# Required environment variables
stack_name = os.environ["HLS_GIBS_STACK"]
bucket_name = os.environ["HLS_GIBS_BUCKET_NAME"]
queue_arn = os.environ["HLS_GIBS_QUEUE_ARN"]

# Optional environment variables
managed_policy_name = os.getenv("HLS_GIBS_MANAGED_POLICY_NAME", "mcp-tenantOperator")

app = App()

NotificationStack(
    app,
    stack_name,
    hls_bucket_name=bucket_name,
    gibs_queue_arn=queue_arn,
    managed_policy_name=managed_policy_name,
)

for k, v in dict(
    Project="hls",
    Stack=stack_name,
).items():
    Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
