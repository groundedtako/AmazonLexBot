import boto3
import unittest
from cgi import test
from moto import mock_dynamodb

from handleDDBEvent import *
from createTestEventInput import *


@mock_dynamodb
class TestMockClassLevel(unittest.TestCase):

    def __init__(self):
        self.ddb_client = boto3.client("dynamodb", region_name="us-east-1")
        self.resource = "DynamoDB"

    def test_ddb_creating_table(self):
        # case 1: create table with valid name and valid partitionKeys
        # expected behavior: return tuple of (true, Success message with table name) 
        intent_name = "DynamoDBCreateTableIntent"
        slots_pairs = {"partitionKey":"S", "partitionKeyType":"S", "tableName": "testing_table"}
        intent_request = create_test_event(self.resource, intent_name, slots_pairs)
        result = ddb_create_table(self.ddb_client, intent_request)
        assert result[0] == True
        assert result[1] == f"Successfully Created Table -> {slots_pairs['tableName']}"

        # case 2: create an existing table
        # expected: abort and notify user
        result = ddb_create_table(self.ddb_client, intent_request)
        assert result[0] == False
        assert result[1] == "Fail Creating Table"
        # query mock_dynamodb, ask whether invoked parameters in order, whether certain calls were made

        # case 3: create table with invalid partitionKeys, too small to large reserved names? regex
        # expected: ilicit new intent and notify user, reprompt for valid values. Returns a response dictionary
        result = ddb_create_table(self.ddb_client, intent_request)
        assert result.type != tuple and result.type == dict

        # setup for testing add
        slots_pairs = {"partitionKey":"S", "partitionKeyType":"S", "tableName": "testing_table_for_creating_item"}
        intent_request = create_test_event(self.resource, intent_name, slots_pairs)
        result = ddb_create_table(self.ddb_client, intent_request)
        assert result[0] == True
        assert result[1] == f"Successfully Created Table -> {slots_pairs['tableName']}"

    def test_ddb_delete_table(self):

        # case 1: delete an existing table
        # excepted: success and notify user
        intent_name = "DynamoDBDeleteTableIntent"
        slots_pairs = {"tableName": "testing_table"}
        intent_request = create_test_event(self.resource, intent_name, slots_pairs)
        result = ddb_delete_table(self.ddb_client, intent_request)
        assert result[0] == True
        assert result[1] == f"Successfully Deleted Table {slots_pairs['tableName']}"

        # case 2: delete a non-existing table
        # expected: abort and notify user
        slots_pairs = {"tableName": "non-existing_table"}
        intent_request = create_test_event(self.resource, intent_name, slots_pairs)
        result = ddb_delete_table(self.ddb_client, intent_request)
        assert result.type != tuple and result.type == dict

    def test_ddb_create_item(self):  
        # case 1: create a valid item
        # sucess and notify user
        intent_name = "DynamoDBCreateItemIntent"
        slots_pairs = {"tableName": "testing_table_for_creating_item",
                       "attributeName": "test_item_name", "attributeValue": "test_item_val"}
                       
        intent_request = create_test_event(self.resource, intent_name, slots_pairs)
        result = ddb_create_item(self.ddb_client, intent_request)
        assert result[0] == True
        # here this assert will fail. Should we include the item_dict in the result message? 
        assert result[1] == f"Successfully Created Item! {slots_pairs['tableName']}" 

        # case 2: create an existing item. Can the partitionKeys be the same?
        # expected: abort and notify user
        # skip for now

        # case 3: create invalid item
        # expected: abort and notify user, reprompt for valid values
        # skip for now

        # case 4: create item in non-existing table
        # expected: abort and notify user
        slots_pairs = {"tableName": "invalid_table", "attributeName": "test_item_name_1",
                       "attributeValue": "test_item_val_1"}        
        intent_request = create_test_event(self.resource, intent_name, slots_pairs)
        result = ddb_create_item(self.ddb_client, intent_request)
        assert result.type != tuple and result.type == dict

    def test_delete_item(self):
        # delete_item not yet implemented
        pass


if __name__ == "__main__":
    test = TestMockClassLevel()
    test.test_ddb_creating_table()

