from cgi import test
import resource
from unittest import mock
import boto3
from moto import mock_s3
from handleS3Event import *
import typing
import unittest
from createTestEventInput import *

@mock_s3
class TestMockClassLevel(unittest.TestCase):
    def setUp(self):
        s3_client = boto3.client("s3", region_name="us-east-1")

    def test_creating_a_bucket(self):
        # 'mybucket', created in setUp, is accessible in this test
        # Other clients can be created at will

        s3_client = boto3.client("s3", region_name="us-east-1")
        intent_request = create_test_event(resource="S3", intent_name="S3CreateBucketIntent", slots_pairs=["CreateBucket", "testBucket", "test"])
        bucket = s3_create_bucket(s3_client, intent_request)

        assert bucket == False


if __name__ == "__main__":
    test = TestMockClassLevel()
    test.test_creating_a_bucket()