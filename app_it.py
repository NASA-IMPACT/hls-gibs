#!/usr/bin/env python3
import os

from aws_cdk import App, Tags

from hls_gibs.stack import NotificationStack
from hls_gibs.stack_it import NotificationITStack

managed_policy_name = os.getenv("HLS_LPDAAC_MANAGED_POLICY_NAME", "mcp-tenantOperator")

app = App()

it_stack = NotificationITStack(
    app,
    "MockGibsResources",
    managed_policy_name=managed_policy_name,
)

NotificationStack(
    app,
    "TestGibs",
    hls_bucket_name=it_stack.bucket.bucket_name,
    gibs_queue_arn=it_stack.queue.queue_arn,
    managed_policy_name=managed_policy_name,
)

for k, v in dict(
    Project="hls",
    App="forward-it",
).items():
    Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
