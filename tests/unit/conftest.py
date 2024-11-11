import json
import os
from typing import Any, Iterator

import boto3
import pytest
from moto import mock_aws

from aws_lambda_typing.events import S3Event
from mypy_boto3_s3 import S3ServiceResource
from mypy_boto3_s3.service_resource import Bucket, Object
from mypy_boto3_sqs import SQSServiceResource
from mypy_boto3_sqs.service_resource import Queue


@pytest.fixture
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def s3(aws_credentials: Any) -> Iterator[S3ServiceResource]:
    with mock_aws():
        yield boto3.resource("s3")


@pytest.fixture
def s3_bucket(s3: S3ServiceResource) -> Bucket:
    bucket = s3.Bucket("mybucket")
    bucket.create()

    return bucket


@pytest.fixture(params=("L30", "S30"))
def s3_object(request: pytest.FixtureRequest, s3_bucket: Bucket) -> Object:
    return make_s3_object(request.param, s3_bucket)


@pytest.fixture
def s3_object_event(s3_object: Object) -> tuple[Object, S3Event]:
    return s3_object, make_s3_event(s3_object)


@pytest.fixture
def s3_object_event_bad_prefix(s3_bucket: Bucket) -> S3Event:
    return make_s3_event(make_s3_object("bad_key", s3_bucket))


def make_s3_object(key_prefix: str, bucket: Bucket) -> Object:
    return bucket.put_object(
        Key=f"{key_prefix}/path/to/dummy.json",
        Body=json.dumps(dict(key_prefix=key_prefix)),
    )


def make_s3_event(s3_object: Object) -> S3Event:
    return {
        "Records": [
            {
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "",
                    "bucket": {
                        "name": f"{s3_object.bucket_name}",
                        "ownerIdentity": {
                            "principalId": "",
                        },
                        "arn": "",
                    },
                    "object": {
                        "key": f"{s3_object.key}",
                        "size": s3_object.content_length,
                        "eTag": s3_object.e_tag,
                        "versionId": s3_object.version_id,
                        "sequencer": "",
                    },
                },
            },
        ],
    }


@pytest.fixture
def sqs(aws_credentials: Any) -> Iterator[SQSServiceResource]:
    with mock_aws():
        yield boto3.resource("sqs")


@pytest.fixture
def sqs_queue(sqs: SQSServiceResource) -> Queue:
    return sqs.create_queue(QueueName="myqueue.fifo", Attributes={"FifoQueue": "true"})
