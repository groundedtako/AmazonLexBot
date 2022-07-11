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
    def __init__(self):
        self.s3_client = boto3.client("s3", region_name="us-east-1")

    def test_s3_create_a_bucket(self):

        # case 1: creating a bucket with valid parameters
        intent_request = create_test_event(resource="S3", intent_name="S3CreateBucketIntent", slots_pairs=["CreateBucket", "testBucket", "test"])
        bucket = s3_create_bucket(self.s3_client, intent_request)

        assert bucket == False

        # case 2: creating a bucket with existing parameters


    def test_s3_put_object(self):

        # case 1: test putting valid object in bucket

        pass

    def test_s3_delete_object(self):

        # case 1: test deleting existing object in bucket

        # case 2: test deleting non-existing object in bucket

        # case 3: test deleting existing object in non-existing bucket

        pass

    def test_s3_delete_bucket(self):

        # case 1: test deleting empty existing bucket

        # case 2: test deleting non-empty existing bucket

        # case 3: test deleting non-existing bucket

        pass


if __name__ == "__main__":
    test = TestMockClassLevel()