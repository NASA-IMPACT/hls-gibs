from __future__ import annotations

from collections.abc import Mapping

from mypy_boto3_s3 import S3ServiceResource
from mypy_boto3_sqs import SQSServiceResource


def test_notification(
    cdk_outputs: Mapping[str, str],
    s3: S3ServiceResource,
    sqs: SQSServiceResource,
) -> None:
    bucket = s3.Bucket(cdk_outputs["HlsBucketName"])
    queue = sqs.Queue(cdk_outputs["GibsQueueUrl"])

    # Write S3 Object with .json suffix to source bucket to trigger notification.
    body = '{ "greeting": "hello world!" }'
    json_key = "S30/greeting.json"
    obj = bucket.Object(json_key)
    obj.put(Body=body)
    obj.wait_until_exists()

    try:
        # Receive message from destination queue, which should be sent by Lambda
        # function triggered by new .json object.
        messages = queue.receive_messages(MaxNumberOfMessages=2, WaitTimeSeconds=20)
        queue.delete_messages(
            Entries=[
                {"Id": m.message_id, "ReceiptHandle": m.receipt_handle}
                for m in messages
            ]
        )
    finally:
        obj.delete()
        obj.wait_until_not_exists()

    # Assert message contents == S3 Object contents (written above)
    assert len(messages) == 1
    assert messages[0].body == body
