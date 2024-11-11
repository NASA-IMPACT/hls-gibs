from __future__ import annotations

import json
import os
import uuid
from functools import cache
from typing import TYPE_CHECKING, Any, Optional

import boto3

if TYPE_CHECKING:  # pragma: no cover
    from aws_lambda_typing.events import S3Event
    from mypy_boto3_sqs.client import SQSClient


VALID_KEY_PREFIXES = {"L30", "S30"}

s3 = boto3.resource("s3")


def handler(
    event: S3Event,
    _context: Any,
    *,
    # Defining optional, keyword-only parameters enables unit testing without the need
    # to monkeypatch `os.environ`.
    gibs_queue_url: Optional[str] = None,
) -> None:
    gibs_queue_url = gibs_queue_url or os.environ["GIBS_QUEUE_URL"]

    bucket, key, message_group_id, message = read_message(event)
    response = sqs_client(gibs_queue_url).send_message(
        QueueUrl=gibs_queue_url,
        MessageGroupId=message_group_id,
        MessageBody=message,
        MessageDeduplicationId=str(uuid.uuid1()),
    )

    print(
        json.dumps(
            dict(
                status_code=response["ResponseMetadata"]["HTTPStatusCode"],
                bucket=bucket,
                key=key,
                identifier=json.loads(message).get("identifier"),
            )
        )
    )


def read_message(event: "S3Event") -> tuple[str, str, str, str]:
    # The S3Event type is not quite correct, so we are forced to ignore a couple
    # of typing errors that would not occur if the type were defined correctly.
    s3_dict = event["Records"][0]["s3"]  # pyright: ignore
    bucket = s3_dict["bucket"]["name"]
    key = s3_dict["object"]["key"]  # pyright: ignore

    if not (prefix := next((p for p in VALID_KEY_PREFIXES if key.startswith(p)), None)):
        raise ValueError(
            f"Key must start with one of {VALID_KEY_PREFIXES}: {bucket=}, {key=}"
        )

    message_group_id = f"HLS{prefix}"
    message = s3.Object(bucket, key).get()["Body"].read().decode()

    return bucket, key, message_group_id, message


# Cache the sqs client, as if we had invoked boto3.client("sqs") at the top level,
# which we cannot do because we don't know the region in advance (although it's
# probably always us-west-2).
@cache
def sqs_client(queue_url: str) -> SQSClient:
    region_name = queue_url.split(".")[1]
    return boto3.client("sqs", region_name=region_name)
