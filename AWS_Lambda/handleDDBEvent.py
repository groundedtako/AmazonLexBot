import boto3     #boto3 to interact with AWS services
import botocore  #boto3 exceptions
import typing    #typing for python typing
import re        #regex for param checking
import logging   #logging for cloudwatch
import sys

#Hard Coded In Order To Test
if __name__ == 'AWS_Lambda.handleDDBEvent':
    from AWS_Lambda.utils import *
    from AWS_Lambda.constants import *
else:
    from utils import *  #util functions for lex interactions
    from constants import *


### DynamoDB

logger = logging.getLogger()


def valid_table_name(tableName: str) -> bool:
    if re.match(r'[a-zA-Z0-9._-]{3,255}', tableName):
        return True
    return False


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

    #Parameter Checking For TableName
    # - Between 3 and 255 characters, containing only letters, numbers, underscores (_), hyphens (-), and periods (.).
    if not valid_table_name(tableName):
        return elicit_slot(intent_request, "tableName", "Invalid Table Name, Please Enter A Valid Table Name.")

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

    try:
        table = ddb_client.create_table(AttributeDefinitions=attributeDefinitions, TableName=tableName,
                                        KeySchema=keySchema, BillingMode=billingMode)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

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

    #Parameter Checking For TableName
    # - Between 3 and 255 characters, containing only letters, numbers, underscores (_), hyphens (-), and periods (.).
    if not valid_table_name(tableName):
        return elicit_slot(intent_request, "tableName", "Invalid Table Name, Please Enter A Valid Table Name.")

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

    try:
        rsp = ddb_client.put_item(TableName=tableName, Item=item_dict)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

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

    #Parameter Checking For TableName
    # - Between 3 and 255 characters, containing only letters, numbers, underscores (_), hyphens (-), and periods (.).
    if not valid_table_name(tableName):
        return elicit_slot(intent_request, "tableName", "Invalid Table Name, Please Enter A Valid Table Name.")

    try:
        rsp = ddb_client.delete_table(TableName=tableName)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

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

    if type(response) != tuple:
        return response

    return close(intent_request, "Fulfilled" if response[0] else "Failed", [response[1]] + ENDING_PHRASE)
