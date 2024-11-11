from setuptools import find_packages, setup  # type: ignore

aws_cdk_extras = [
    "aws-cdk-lib>=2.0.0",
    "constructs>=10.0.0",
]

install_requires: list[str] = []

extras_require_test = [
    *aws_cdk_extras,
    "boto3",
    "moto[s3,sqs]",
    "pytest-cov",
    "pytest",
    "ruff",
]

extras_require_dev = [
    *extras_require_test,
    "aws_lambda_typing",
    "boto3-stubs[iam,lambda,s3,sqs,ssm]",
    "botocore-stubs",
    "mypy",
    "nodeenv",
    "pre-commit",
    "pre-commit-hooks",
]

extras_require = {
    "test": extras_require_test,
    "dev": extras_require_dev,
}

setup(
    name="hls-gibs",
    version="0.1.0",
    python_requires=">=3.12",
    author="Development Seed",
    packages=find_packages(),
    package_data={
        ".": [
            "cdk.json",
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
)
