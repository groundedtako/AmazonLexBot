import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing

#Hard Coded In Order To Test
if __name__ == 'AWS_Lambda.handleDDBEvent':
    from AWS_Lambda.utils import *
else:
    from utils import *  #util functions for lex interactions


### DynamoDB


def ddb_create_table(ddb_client: typing.Any, intent_request: dict) -> tuple:
    """Creating Table in DynamoDB

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table

    Args:
        ddb_client (typing.Any): A low-level client representing Amazon DynamoDB
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """

    table_key = get_slot(intent_request, "partitionKey")
    key_type = get_slot(intent_request, "partitionKeyType")
    tableName = get_slot(intent_request, "tableName", True)

    attributeDefinitions = [{
        'AttributeName': table_key,
        'AttributeType': key_type
    }]

    keySchema = [{
        'AttributeName': table_key,
        'KeyType': 'HASH'
    }]

    #TODO could ask user to input
    billingMode = 'PAY_PER_REQUEST'

    table = ddb_client.create_table(AttributeDefinitions=attributeDefinitions, TableName=tableName,
                                    KeySchema=keySchema, BillingMode=billingMode)

    if table is None:
        return False, "Fail Creating Table"

    return True, f"Successfully Created Table -> {tableName}!"


def ddb_create_item(ddb_client: typing.Any, intent_request: dict) -> tuple:
    """Creating item in specified DynamoDB table

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item

    Args:
        ddb_client (typing.Any): A low-level client representing Amazon DynamoDB
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)

    Todo:
        May want another slot for attribute's type
    """
    tableName = get_slot(intent_request, "tableName", True)
    #Todo validate table!

    #Get The Table's Primary Key
    #Maybe we should prompt the user for primary key

    table_info = ddb_client.describe_table(TableName=tableName)

    table_definitions = table_info["Table"]["AttributeDefinitions"][0]

    table_key = table_definitions['AttributeName']
    table_key_type = table_definitions['AttributeType']

    attributeName = get_slot(intent_request, "attributeName")
    attributeValue = get_slot(intent_request, "attributeValue")

    item_dict = {
        table_key: {
            table_key_type: get_random_id(table_key_type)
        },
        attributeName: {
            table_key_type: attributeValue
        }
    }

    rsp = ddb_client.put_item(TableName=tableName, Item=item_dict)

    if rsp is None:
        return False, "Fail Creating Item"

    return True, f"Successfully Created Item! {item_dict}"


def ddb_delete_table(ddb_client: typing.Any, intent_request: dict) -> tuple:
    """Deleting Table in DynamoDB

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_table

    Args:
        ddb_client (typing.Any): A low-level client representing Amazon DynamoDB
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """
    tableName = get_slot(intent_request, "tableName", True)

    rsp = ddb_client.delete_table(TableName=tableName)

    if rsp is None:
        return False, "Fail Deleting Table"

    return True, f"Successfully Deleted Table {tableName}"


def ddb_handler(intent_request: dict, action: str) -> dict:
    ddb_client = boto3.client("dynamodb")

    if action == "CreateTable":
        response = ddb_create_table(ddb_client, intent_request)
    elif action == "CreateItem":
        response = ddb_create_item(ddb_client, intent_request)
    elif action == "DeleteTable":
        response = ddb_delete_table(ddb_client, intent_request)
    else:
        response = (False, f"Sorry Action : {action} Not Supported Yet!")

    return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])
