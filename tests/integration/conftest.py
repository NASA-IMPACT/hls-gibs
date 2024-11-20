from __future__ import annotations

import json
from pathlib import Path

import boto3
import pytest
from mypy_boto3_lambda import LambdaClient
from mypy_boto3_s3 import S3ServiceResource
from mypy_boto3_sqs import SQSServiceResource


@pytest.fixture
def lambda_() -> LambdaClient:
    return boto3.client("lambda")


@pytest.fixture
def s3() -> S3ServiceResource:
    return boto3.resource("s3")


@pytest.fixture
def sqs() -> SQSServiceResource:
    return boto3.resource("sqs")


@pytest.fixture(scope="session")
def cdk_outputs() -> dict[str, str]:
    outputs_by_stack: dict[str, dict[str, str]] = json.loads(
        (Path() / "cdk.out" / "outputs.json").read_text()
    )

    return next(
        (
            outputs
            for stack, outputs in outputs_by_stack.items()
            if stack.casefold().endswith("resources")
        ),
        {},
    )
