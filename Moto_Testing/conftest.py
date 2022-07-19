import os
import boto3
import pytest

from moto import mock_ec2, mock_s3, mock_dynamodb
# mock_dynamodb2 has been deprecated in favor of mock_dynamodb


@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb_client(aws_credentials):
    with mock_dynamodb():
        conn = boto3.client("dynamodb")
        yield conn


@pytest.fixture
def ec2_client(aws_credentials):
    with mock_ec2():
        conn = boto3.client('ec2')
        yield conn


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.client('s3')
        yield conn
