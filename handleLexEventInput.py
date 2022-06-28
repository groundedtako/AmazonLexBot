import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
import logging  #logging for cloudwatch
import uuid     #unique id

#Setting up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

### Constants
AVAILABLE_RESOURCES = ("EC2", "DynamoDB", "S3")
EC2_LIFECYCLE = ("StopInstance", "TerminateInstance", "StartInstance")


def get_random_id(type: str) -> typing.Union[int, str]:
    """Generate a random id based on the args

    Args:
        type (str): data type for the random id
            'B' -> binary
            'N' -> number
            'S' -> string

    Returns:
        id (type): random id generated by uuid
    """    
    #Todo need to consider binary 'B'
    id = uuid.uuid4()
    if(type == 'N'):
        return id.int >> 64
    return str(id)


### EC2
#Todo Implement actions
#DryRun option to check for permission
#Check Instance State (In case flooding requests)
def ec2_lifecycle_control(ec2_client, intent_request, action):
    instanceId = get_slot(intent_request, "instanceId")

    if action == "StopInstance":
        rsp = ec2_client.stop_instances(InstanceIds=[instanceId])
    elif action == "TerminateInstance":
        rsp = ec2_client.terminate_instances(InstanceIds=[instanceId])
    elif action == "StartInstance":
        rsp = ec2_client.start_instances(InstanceIds=[instanceId])

    if rsp is None:
        return False, f"Fail {action}!"
    return True, f"Successfully {action} (Instance's Id : {instanceId})"


# def ec2_stop_instance(ec2_client: typing.Any, intent_request: dict) -> tuple:
#     instanceId = get_slot(intent_request, "instanceId")

#     rsp = ec2_client.stop_instances(InstanceIds=[instanceId])

#     if rsp is None:
#         return False, "Fail Stopping Instance"
#     return True, f"Successfully Stopped Instance (Instance's Id : {instanceId})"


# def ec2_terminate_instance(ec2_client: typing.Any, intent_request: dict) -> tuple:
#     instanceId = get_slot(intent_request, "instanceId")

#     rsp = ec2_client._instances(InstanceIds=[instanceId])

#     if rsp is None:
#         return False, "Fail Stopping Instance"
#     return True, f"Successfully Stopped Instance (Instance's Id : {instanceId})"


# def ec2_start_instance(ec2_client: typing.Any, intent_request: dict) -> tuple:
#     instanceId = get_slot(intent_request, "instanceId")

#     rsp = ec2_client.stop_instances(InstanceIds=[instanceId])

#     if rsp is None:
#         return False, "Fail Stopping Instance"
#     return True, f"Successfully Stopped Instance (Instance's Id : {instanceId})"


def ec2_create_instance(ec2_client: typing.Any, intent_request: dict) -> tuple:
    imageId = get_slot(intent_request, "amazonMachineImages")
    minCount = int(get_slot(intent_request, "minCount"))
    maxCount = int(get_slot(intent_request, "maxCount"))
    instanceType = get_slot(intent_request, "instanceType")
    # keyName = get_slot(intent_request, "keyName")

    instance = ec2_client.run_instances(
        ImageId=imageId,
        MinCount=minCount,
        MaxCount=maxCount,
        InstanceType=instanceType,
    )

    if instance is None:
        return False, "Fail Creating Instance"

    instanceId = instance["Instances"][0]["InstanceId"]
    return True, f"Successfully Created Instance (Instance's Id : {instanceId})"


def ec2_handler(intent_request: dict, action: str) -> dict:
    ec2_client = boto3.client("ec2")

    if action == "CreateInstance":
        response = ec2_create_instance(ec2_client, intent_request)
    elif action in EC2_LIFECYCLE:
        response = ec2_lifecycle_control(ec2_client, intent_request, action)
    # elif action == "StopInstance":
    #     return None
    # elif action == "TerminateInstance":
    #     return None
    # elif action == "StartInstance":
    #     return None
    else:
        response = (False, f"Sorry Action : {action} Not Supported Yet!")

    return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])


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

### S3
#Todo Implement actions


def s3_create_bucket(s3_client: typing.Any, intent_request: dict) -> tuple:
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket
    bucket_name = get_slot(intent_request, "bucketName", True)

    bucket = s3_client.create_bucket(Bucket=bucket_name)

    if bucket is None:
        return False, "Fail Creating Bucket"

    return True, f"Successfully Created Bucket {bucket_name}"


def s3_put_object(s3_client: typing.Any, intent_request: dict) -> tuple:
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object

    bucket_name = get_slot(intent_request, "bucketName", True)
    body = get_slot(intent_request, "body")
    key = get_slot(intent_request, "key", True)

    bucket = s3_client.put_object(Bucket=bucket_name, Body=body.encode('ascii'), Key=key)

    if bucket is None:
        return False, "Fail Putting Object Into Bucket"
    return True, f"Successfully Put {key} Inside {bucket_name}"


def s3_delete_object(s3_client: typing.Any, intent_request: dict) -> tuple:
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object

    bucket_name = get_slot(intent_request, "bucketName", True)
    key = get_slot(intent_request, "key", True)

    bucket = s3_client.delete_object(Bucket=bucket_name, Key=key)

    if bucket is None:
        return False, "Fail Deleting Object From Bucket"
    return True, f"Successfully Deleted {key} Inside {bucket_name}"


def s3_delete_bucket(s3_client: typing.Any, intent_request: dict) -> tuple:
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket
    bucket_name = get_slot(intent_request, "bucketName", True)

    bucket = s3_client.delete_bucket(Bucket=bucket_name)

    if bucket is None:
        return False, "Fail Deleting Bucket"
    return True, f"Successfully Deleted Bucket {bucket_name}"


def s3_handler(intent_request: dict, action: str) -> dict:
    s3_client = boto3.client("s3")

    if action == "CreateBucket":
        response = s3_create_bucket(s3_client, intent_request)
    elif action == "PutObject":
        response = s3_put_object(s3_client, intent_request)
    elif action == "DeleteObject":
        response = s3_delete_object(s3_client, intent_request)
    elif action == "DeleteBucket":
        response = s3_delete_bucket(s3_client, intent_request)
    else:
        response = (False, f"Sorry Action : {action} Not Supported Yet!")

    return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])

### Response Functions
#Todo ConfirmIntent


'''
There are 5 type of dialog actions

- Close - Indicates that there will not be a response from the user.
          For example, the statement "Your order has been placed" does not require a response.

- ConfirmIntent - The next action is asking the user if the intent is complete and ready to be fulfilled.
                  This is a yes/no question such as "Place the order?"

- Delegate - The next action is determined by Amazon Lex V2.

- ElicitIntent - The next action is to elicit an intent from the user.

- ElicitSlot - The next action is to elicit a slot value from the user.
'''


def close(intent_request: dict, fulfillment_state: str, message: str) -> dict:
    intent_request["sessionState"]["intent"]["state"] = fulfillment_state
    return {
        "sessionState": {
            "sessionAttributes": get_session_attributes(intent_request),
            "dialogAction": {
                "type": "Close"
            },
            "intent": intent_request["sessionState"]["intent"]
        },
        "messages": [{
            "contentType": "PlainText",
            "content": message
        }] if message != None else None,
        "sessionId": intent_request["sessionId"],
        "requestAttributes": intent_request["requestAttributes"] if "requestAttributes" in intent_request else None
    }


def elicit_intent(intent_request, message):
    intent_request["sessionState"]["intent"]["state"] = "InProgress"
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitIntent"
            },
            "sessionAttributes": get_session_attributes(intent_request),
            "intent": intent_request["sessionState"]["intent"]
        },
        "messages": [{
            "contentType": "PlainText",
            "content": message
        }] if message != None else None,
        "requestAttributes": intent_request["requestAttributes"] if "requestAttributes" in intent_request else None
    }


def elicit_slot(intent_request, new_slot_name, message):
    intent_request["sessionState"]["intent"]["state"] = "InProgress"
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": new_slot_name
            },
            "sessionAttributes": get_session_attributes(intent_request),
            "intent": intent_request["sessionState"]["intent"]
        },
        "messages": [{
            "contentType": "PlainText",
            "content": message
        }] if message != None else None,
        "requestAttributes": intent_request["requestAttributes"] if "requestAttributes" in intent_request else None
    }


### Utils Functions

def get_intent_name(intent_request: dict) -> str:
    '''
    Return the corrsponding intent 
    '''
    return intent_request["sessionState"]["intent"]["name"]


def get_session_attributes(intent_request: dict) -> dict:
    '''
    Return session attributes
    '''
    sessionState = intent_request["sessionState"]
    if "sessionAttributes" in sessionState:
        return sessionState["sessionAttributes"]
    return {}


def get_slots(intent_request: dict) -> dict:
    '''
    Return all the slots
    '''
    return intent_request["sessionState"]["intent"]["slots"]


def get_slot(intent_request: dict, slotName: str, original: bool = False) -> str:
    '''
    Return the corrrsponding slot or None
    '''
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        val = slots[slotName]["value"]
        return val["originalValue"] if original else val["interpretedValue"]
    else:
        return None


def dispatch(intent_request: dict) -> dict:
    '''
    Dispatch to Lex"s intent handlers
    '''

    resourceType = get_slot(intent_request, "resource")
    action = get_slot(intent_request, f"{resourceType}_action")

    #Check if action is here or not
    if resourceType in AVAILABLE_RESOURCES and action is None:
        logger.debug("Missing Action!")
        return close(intent_request, "Fulfilled", f"What action you want to do with {resourceType}?")

    #Switch Statement Available after Python 3.10
    if resourceType == "EC2":
        return ec2_handler(intent_request, action)
    elif resourceType == 'DynamoDB':
        return ddb_handler(intent_request, action)
    elif resourceType == 'S3':
        return s3_handler(intent_request, action)
    else:
        intent = get_intent_name(intent_request)
        #For other intent

    raise Exception("Intent: " + intent + " Not Supported Yet!")


def lambda_handler(event: dict, context: typing.Any):
    '''
    Entrance for lambda function
    '''
    logger.info("Logging Event!")
    logger.info(event)
    rsp = dispatch(event)

    logger.info("Logging Response!")
    logger.info(rsp)
    return rsp
