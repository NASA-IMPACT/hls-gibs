from __future__ import annotations

import pytest
from aws_lambda_typing.events import S3Event
from mypy_boto3_s3.service_resource import Object
from mypy_boto3_sqs.service_resource import Queue


def test_gibs_forward_handler(
    s3_object_event: tuple[Object, S3Event],
    sqs_queue: Queue,
) -> None:
    # Import here (rather than at top level) to ensure AWS mocks are established.
    # See http://docs.getmoto.org/en/latest/docs/getting_started.html#what-about-those-pesky-imports
    from hls_gibs.forward import handler

    s3_object, s3_event = s3_object_event
    handler(s3_event, None, gibs_queue_url=sqs_queue.url)

    responses = sqs_queue.receive_messages(MaxNumberOfMessages=10)
    actual_messages = [response.body for response in responses]
    expected_messages = [s3_object.get()["Body"].read().decode()]

    assert actual_messages == expected_messages


def test_gibs_forward_handler_invalid_key_prefix(
    s3_object_event_bad_prefix: S3Event,
    sqs_queue: Queue,
) -> None:
    # Import here (rather than at top level) to ensure AWS mocks are established.
    # See http://docs.getmoto.org/en/latest/docs/getting_started.html#what-about-those-pesky-imports
    from hls_gibs.forward import handler

    with pytest.raises(ValueError, match="Key"):
        handler(s3_object_event_bad_prefix, None, gibs_queue_url=sqs_queue.url)
