import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
from lambdaUtils import * #lambdaUtils for lex interactions

### DynamoDB
#Todo Implement actions


def ddb_create_table(ddb_resource: typing.Any, intent_request: dict) -> typing.Tuple[bool, str]:
    """Using DynamoDB resource to craete a new table

    Args:
        ddb_resource (typing.Any): Boto AWS resource
        intent_request (dict): Amazon Lex Event Input

    Returns:
        typing.Tuple[bool, str]: bool indicating Success or not, str representing Message back to user
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

    table = ddb_resource.create_table(AttributeDefinitions=attributeDefinitions, TableName=tableName,
                                      KeySchema=keySchema, BillingMode=billingMode)

    if table is None:
        return False, "Fail Creating Table"

    return True, f"Successfully Created Table -> {tableName}!"


def ddb_create_item(ddb_resource: typing.Any, intent_request: dict) -> tuple:
    tableName = get_slot(intent_request, "tableName", True)
    ddb_table = ddb_resource.Table(tableName)
    #Todo validate table!

    #Get The Table's Primary Key
    #Maybe we should prompt the user for primary key
    table_definitions = ddb_table.attribute_definitions[0]

    table_key = table_definitions['AttributeName']
    table_key_type = table_definitions['AttributeType']

    attributeName = get_slot(intent_request, "attributeName")
    attributeValue = get_slot(intent_request, "attributeValue")

    item_dict = {
        table_key: get_random_id(table_key_type),
        attributeName: attributeValue
    }

    rsp = ddb_table.put_item(Item=item_dict)

    if rsp is None:
        return False, "Fail Creating Item"

    return True, f"Successfully Created Item! {item_dict}"


def ddb_delete_table(ddb_resource, intent_request):
    tableName = get_slot(intent_request, "tableName", True)
    ddb_table = ddb_resource.Table(tableName)

    rsp = ddb_table.delete()

    if rsp is None:
        return False, "Fail Deleting Table"

    return True, f"Successfully Deleted Table {tableName}"


def ddb_handler(intent_request: dict, action: str) -> dict:
    ddb_resource = boto3.resource("dynamodb")

    if action == "CreateTable":
        response = ddb_create_table(ddb_resource, intent_request)

    elif action == "CreateItem":
        response = ddb_create_item(ddb_resource, intent_request)

    elif action == "DeleteTable":
        response = ddb_delete_table(ddb_resource, intent_request)

    else:
        response = (False, f"Sorry Action : {action} Not Supported Yet!")

    return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])