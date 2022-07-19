import pytest
from ddb import MyDDBClient

# Append to sys path
import sys
sys.path.append('../../../AmazonLexBot')


from AWS_Lambda.handleDDBEvent import *
from AWS_Lambda.createTestEventInput import create_test_event


@pytest.fixture
def table_schema():
    partitionKey = "S"
    partitionKeyType = "S"
    tableName = "testing_table"
    schema = {
        "partitionKey": partitionKey,
        "partitionKeyType": partitionKeyType,
        "tableName": tableName
    }
    return schema


def test_ddb_create_table(dynamodb_client, table_schema):

    ddb = MyDDBClient()
    assert len(ddb.list_tables()) == 0

    print("\nTesting DynamoDBCreateTableIntent:")
    test_intent = create_test_event("DynamoDB", "DynamoDBCreateTableIntent", table_schema)

    mock_rsp = ddb_create_table(ddb.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert len(ddb.list_tables()) == 1


def test_ddb_delete_table(dynamodb_client):

    ddb = MyDDBClient()
    table = ddb.create_ddb_table()
    print(table)
    assert len(ddb.list_tables()) == 1

    print("\nTesting DynamoDBDeleteTableIntent: ")
    test_intent = create_test_event("DynamoDB", "DynamoDBDeleteTableIntent", {"tableName": "testing_table"})

    mock_rsp = ddb_delete_table(ddb.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert len(ddb.list_tables()) == 0


def test_ddb_create_item(dynamodb_client):

    ddb = MyDDBClient()
    table = ddb.create_ddb_table()
    assert len(ddb.list_tables()) == 1

    print("\nTesting DynamoDBCreateItemIntent: ")
    slots_pairs = {"tableName": "testing_table", "attributeName": "testing_record", "attributeValue": "testing_val"}
    test_intent = create_test_event("DynamoDB", "DynamoDBCreateItemIntent", slots_pairs)

    mock_rsp = ddb_create_item(ddb.client, test_intent)
    print(mock_rsp)
    assert mock_rsp[0] == True

    table_info = ddb.client.describe_table(TableName="testing_table")
    item_count = table_info["Table"]["ItemCount"]
    assert item_count == 1
