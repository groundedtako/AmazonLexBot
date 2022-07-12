import boto3
import unittest

from cgi import test
from moto import mock_ec2

from handleDDBEvent import *
from createTestEventInput import *


@mock_ec2
class TestMockClassLevel(unittest.TestCase):

    def __init__(self):
        self.ec2_client = boto3.client("ec2", region_name="us-east-1")

    def test_ec2_create_instance(self):
        # case 1: create ec2 instance with valid parameters
        resource = "ec2"
        intent_name = "EC2StartInstanceIntent"  # TODO not yet supported
        imageId = ""
        intent_request = create_test_event(resource, intent_name, slots_pairs)
        bucket = ddb_create_table(self.ddb_client, intent_request)
        print(bucket[1])
        assert bucket[0] == True

        # case 2: create an ec2 instance from a template
        # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html

        bucket = ddb_create_table(self.ddb_client, intent_request)
        print(bucket[1])
        assert bucket[0] == False
        # query mock_dynamodb, ask whether invoked parameters in order, whether certain calls were made

        # case 3: create table with invalid partitionKeys

    def test_ec2_lifecycle_control(self):

        # case 1: delete an existing table

        # case 2: delete a non-existing table
        pass

if __name__ == "__main__":
    test = TestMockClassLevel()
