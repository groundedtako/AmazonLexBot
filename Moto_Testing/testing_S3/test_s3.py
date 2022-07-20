import pytest
from s3 import MyS3Client

# Append to sys path
import sys
sys.path.append('../../../AmazonLexBot')

from AWS_Lambda.handleS3Event import *
from AWS_Lambda.createTestEventInput import create_test_event

@pytest.fixture
def bucket_name():
    return "testing"

@pytest.fixture
def body():
    return "123".encode("ascii")

@pytest.fixture
def key():
    return "123.txt"

@pytest.fixture
def create_bucket(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
    yield

@pytest.fixture
def create_object(s3_client, bucket_name, body, key):
    s3_client.put_object(Bucket=bucket_name, Body=body, Key=key)
    yield


def test_s3_create_bucket(s3_client, bucket_name):
    s3 = MyS3Client()
    assert len(s3.list_buckets()) == 0

    print("\nTesting S3CreateBucketIntent:")
    test_intent = create_test_event("S3", "S3CreateBucketIntent", {"bucketName" : bucket_name})

    mock_rsp = s3_create_bucket(s3.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert len(s3.list_buckets()) == 1

def test_s3_put_object(s3_client, create_bucket, bucket_name):
    s3 = MyS3Client()
    key = "123.txt"
    assert len(s3.list_buckets()) == 1

    print("\nTesting S3PutObjectIntent:")
    test_intent = create_test_event("S3", "S3PutObjectIntent", {"bucketName" : bucket_name,"body" : "123", "key" : key})

    mock_rsp = s3_put_object(s3.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert s3.list_objects(bucket_name, "123.txt") == [key]

def test_s3_delete_bucket(s3_client, create_bucket, bucket_name):
    s3 = MyS3Client()
    assert len(s3.list_buckets()) == 1

    print("\nTesting S3DeleteBucketIntent:")
    test_intent = create_test_event("S3", "S3DeleteBucketIntent", {"bucketName" : bucket_name})

    mock_rsp = s3_delete_bucket(s3.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert len(s3.list_buckets()) == 0

def test_s3_delete_object(s3_client, create_bucket, create_object, bucket_name, key):
    s3 = MyS3Client()
    assert len(s3.list_buckets()) == 1
    assert s3.list_objects(bucket_name, key) == [key]

    print("\nTesting S3DeleteObjectIntent:")
    test_intent = create_test_event("S3", "S3DeleteObjectIntent", {"bucketName" : bucket_name , "key" : key})

    mock_rsp = s3_delete_object(s3.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert len(s3.list_objects(bucket_name, key)) == 0
