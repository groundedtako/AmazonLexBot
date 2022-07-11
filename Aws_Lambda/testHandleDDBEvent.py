from cgi import test
import resource
from unittest import mock
import boto3
from moto import mock_dynamodb
from handleDDBEvent import *
import typing
import unittest
from createTestEventInput import *

@mock_dynamodb
class TestMockClassLevel(unittest.TestCase):
    def __init__(self):
        self.ddb_client = boto3.client("dynamodb", region_name="us-east-1")

    def test_ddb_creating_table(self):
        
        # case 1: create table with valid name and valid partitionKeys
        resource = resource="DynamoDB"
        intent_name="DynamoDBCreateTableIntent"
        slots_pairs={"partitionKey":"S", "partitionKeyType":"S", "tableName": "testing_table"}
        intent_request = create_test_event(resource, intent_name, slots_pairs)
        bucket = ddb_create_table(self.ddb_client, intent_request)
        print(bucket[1])
        assert bucket[0] == True

        # case 2: create an existing table
        bucket = ddb_create_table(self.ddb_client, intent_request)
        print(bucket[1])
        assert bucket[0] == False
        # query mock_dynamodb, ask whether invoked parameters in order, whether certain calls were made

        # case 3: create table with invalid partitionKeys
        
    def test_ddb_delete_table(self):

        # case 1: delete an existing table

        # case 2: delete a non-existing table

        # case 3: delete a non-empty table
        pass

    def test_ddb_create_item(self):
        
        # case 1: create a valid item

        # case 2: create an existing item. Can the partitionKeys be the same?

        # case 3: creat invalid item

        # case 4: creating an item over the maximum number of items in table

        # case 5: creating multiple valid items

        # case 6: create multiple items with one or more invalid items
        pass

    def test_delete_item(self):
        # delete_item not yet implemented
        pass
    
if __name__ == "__main__":
    test = TestMockClassLevel()
    test.test_creating_table()

    