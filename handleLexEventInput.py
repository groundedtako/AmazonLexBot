import json 
import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
import logging  #logging for cloudwatch
import uuid     #unique id

#Setting up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

### Constants
available_resource = ("EC2","DynamoDB","S3")

def get_random_id(type:str):
    '''
    Return unique id based on type
    '''
    #Todo need to consider binary 'B'
    id = uuid.uuid4()
    if(type == 'N'):
        return id.int>>64
    return str(id)


### EC2
#Todo Implement actions

def ec2_handler(intent_request:dict):
    client_ec2 = boto3.client("ec2")
    if action == "create":
        return None
    elif action == "stop":
        return None
    elif action == "terminate":
        return None
    elif action == "rerun":
        return None

    raise Exception("Action: " + action + " Not Supported Yet!")

### DynamoDB
#Todo Implement actions

def ddb_create_table(ddb_resource : typing.Any, intent_request: dict) -> tuple:
    table_key = get_slot(intent_request, "partitionKey")
    key_type = get_slot(intent_request, "partitionKeyType")
    tableName = get_slot(intent_request, "tableName", True)

    attributeDefinitions = [{
        'AttributeName' : table_key,
        'AttributeType' : key_type
    }]

    keySchema = [{
        'AttributeName' : table_key,
        'KeyType': 'HASH'
    }]

    #TODO could ask user to input
    billingMode = 'PAY_PER_REQUEST'


    table = ddb_resource.create_table(AttributeDefinitions=attributeDefinitions, TableName = tableName, KeySchema=keySchema, BillingMode= billingMode)
    if table is None:
        return False, "Fail Creating Table"

    return True, f"Successfully Created Table -> {tableName}!"


def ddb_create_item(ddb_table : typing.Any, intent_request : dict, ) -> tuple:
    
    #Get The Table's Primary Key
    #Maybe we should prompt the user for primary key
    table_definitions = ddb_table.attribute_definitions[0]

    table_key = table_definitions['AttributeName']
    table_key_type = table_definitions['AttributeType']

    attributeName = get_slot(intent_request, "attributeName")
    attributeValue = get_slot(intent_request, "attributeValue")
    

    item_dict = {
        table_key : get_random_id(table_key_type),
        attributeName : attributeValue
    }
    
    rsp = ddb_table.put_item(Item=item_dict)

    if rsp is None:
        return False, "Fail Creating Item"
    
    return True, f"Successfully Created Item! {item_dict}"


def ddb_handler(intent_request:dict, action:str)->dict:
    ddb_resource = boto3.resource("dynamodb")
    

    if action == "CreateTable":
        response = ddb_create_table(ddb_resource, intent_request)
        return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])

    elif action == "CreateItem":
        tableName = get_slot(intent_request, "tableName", True)
        table = ddb_resource.Table(tableName)
        #Todo validate table!

        response = ddb_create_item(table, intent_request)
        return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])

    elif action == "Terminate":
        return None

### S3
#Todo Implement actions

def s3_handler(intent_request:dict):
    client_s3 = boto3.resource("s3")
    if action == "create":
        return None
    elif action == "add_item":
        return None
    elif action == "terminate":
        return None

### Response Functions
#Todo ConfirmIntent
'''
There are 5 type of dialog actions

- Close - Indicates that there will not be a response from the user. For example, the statement "Your order has been placed" does not require a response.

- ConfirmIntent - The next action is asking the user if the intent is complete and ready to be fulfilled. This is a yes/no question such as "Place the order?"

- Delegate - The next action is determined by Amazon Lex V2.

- ElicitIntent - The next action is to elicit an intent from the user.

- ElicitSlot - The next action is to elicit a slot value from the user.
'''


def close(intent_request : dict ,fulfillment_state : str, message : str) -> dict:
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
            "contentType":"PlainText",
            "content":message
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
        "messages":  [{
            "contentType":"PlainText",
            "content":message
        }] if message != None else None,
        "requestAttributes": intent_request["requestAttributes"] if "requestAttributes" in intent_request else None
    }

def elicit_slot(intent_request, new_slot_name, message):
    intent_request["sessionState"]["intent"]["state"] = "InProgress"
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit" : new_slot_name
            },
            "sessionAttributes": get_session_attributes(intent_request),
            "intent": intent_request["sessionState"]["intent"]
        },
        "messages":  [{
            "contentType":"PlainText",
            "content":message
        }] if message != None else None,
        "requestAttributes": intent_request["requestAttributes"] if "requestAttributes" in intent_request else None
    }



### Utils Functions
def get_intent_name(intent_request:dict) -> str:
    '''
    Return the corrsponding intent 
    '''
    return intent_request["sessionState"]["intent"]["name"]

def get_session_attributes(intent_request:dict) -> dict:
    '''
    Return session attributes
    '''
    sessionState = intent_request["sessionState"]
    if "sessionAttributes" in sessionState:
        return sessionState["sessionAttributes"]
    return {}

def get_slots(intent_request:dict) -> dict:
    '''
    Return all the slots
    '''
    return intent_request["sessionState"]["intent"]["slots"]

def get_slot(intent_request:dict, slotName:str, original:bool = False) -> str:
    '''
    Return the corrrsponding slot or None
    '''
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        val = slots[slotName]["value"]
        return val["originalValue"] if original else val["interpretedValue"]
    else:
        return None   


def dispatch(intent_request:dict):
    '''
    Dispatch to Lex"s intent handlers
    '''
    
    resourceType = get_slot(intent_request, "resource")
    action = get_slot(intent_request, "action")

    #Check if action is here or not
    if resourceType in available_resource and action is None:
        logger.debug("Missing Action!")
        return close(intent_request,"Fulfilled", f"What action you want to do with {resourceType}?")

    #Switch Statement Available after Python 3.10
    if resourceType == "EC2":
        return None
    elif resourceType == 'DynamoDB':
        return ddb_handler(intent_request, action)
    elif resourceType == 'S3':
        return None
    else:
        intent = get_intent_name(intent_request)
        #For other intent
        
    raise Exception("Intent: " + intent + " Not Supported Yet!")
    


def lambda_handler(event:dict, context:typing.Any):
    '''
    Entrance for lambda function
    '''
    logger.info("Logging Event!")
    logger.info(event)
    rsp = dispatch(event)

    logger.info("Logging Response!")
    logger.info(rsp)
    return rsp
