# HLS GIBS

Notify GIBS when HLS browse imagery is available.

When a JSON file lands in an HLS browse imagery bucket (configurable), send a
message to a GIBS queue (configurable).

## Requirements

- [pre-commit](https://pre-commit.com/)
- Python >= 3.12
- tox

## Environment Settings

In order to _locally_ run integration tests, you must export the following
environment variables:

```plain
# A unique prefix for a deployment to avoid resource name conflicts between
# deployments in the same AWS account.  Should be developer-specific, such as
# a username or nickname.
export HLS_GIBS_STACK=<stack name>

export AWS_DEFAULT_REGION=us-west-2
export AWS_ACCESS_KEY_ID=<id>
export AWS_SECRET_ACCESS_KEY=<key>
export AWS_SESSION_TOKEN=<token>
```

For _GitHub workflows_, you must define the following environment variables in
each GitHub environment for this repository:

```plain
# A unique prefix for a deployment to avoid resource name conflicts between
# deployments in the same AWS account.  Should correspond to GitHub environment
# name.
HLS_GIBS_STACK=<stack name>

# Bucket to trigger lambda when .json file lands
HLS_GIBS_BUCKET_NAME=<source bucket name>
# Queue to send notification from Lambda triggered by new .json file in bucket
HLS_GIBS_QUEUE_ARN=<destination queue ARN>
```

For integration tests, a sidecar stack with dummy resources is constructed, and
the environment variables referencing the resources are automatically obtained,
so there is no need to manually set environment variables referring to the
resources.

## Development

For active stack development run the following to create a virtual environment
in the `venv` directory:

```plain
make venv
```

Whenever `setup.py` changes, rerun the command above to update the dependencies
in the `venv` directory.

To use it for development:

```plain
source venv/bin/activate
```

Install pre-commit hooks:

```plain
pre-commit install --install-hooks
```

The command above will make sure all pre-commit hooks configured in
`.pre-commit-config.yaml` are executed when appropriate.

To manually run the hooks to check code changes:

```plain
pre-commit run --all-files
```

## Testing

To run unit tests:

```plain
make unit-tests
```

To run integration tests:

```plain
make deploy-it
make integration-tests
make destroy-it
```
