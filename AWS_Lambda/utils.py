import uuid     #unique id
import typing   #typing for python typing


### Lex Utils Functions

def get_random_id(type: str) -> typing.Union[int, str]:
    """Generate a random id based on given type

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
    id = str(id)
    if(type == 'B'):
        return id.encode('ascii')
    return id


def get_intent_name(intent_request: dict) -> str:
    """Get intent's name based on the event input

    Args:
        intent_request (dict): Amazon Lex Event Input

    Returns:
        str: Intent Name
    """
    return intent_request["sessionState"]["intent"]["name"]


def get_session_attributes(intent_request: dict) -> dict:
    """Get session's attributes based on the event input

    Args:
        intent_request (dict): Amazon Lex Event Input

    Returns:
        dict: Session Attributes or Empty dict
    """
    sessionState = intent_request["sessionState"]
    if "sessionAttributes" in sessionState:
        return sessionState["sessionAttributes"]
    return {}


def get_slots(intent_request: dict) -> dict:
    """Get all the slots based on the event input

    Args:
        intent_request (dict): Amazon Lex Event Input

    Returns:
        dict: All the slots
    """
    return intent_request["sessionState"]["intent"]["slots"]


def get_slot(intent_request: dict, slotName: str, original: bool = False) -> str:
    """Get the corrsponding slot based on name

    Args:
        intent_request (dict): Amazon Lex Event Input
        slotName (str): Slot Name
        original (bool, optional): Original value instead of Resolved value.  Defaults to False.

    Returns:
        str: Corrsponding value or None
    """
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        val = slots[slotName]["value"]
        return val["originalValue"] if original else val["interpretedValue"]
    else:
        return None


### Response Functions
#Todo ConfirmIntent

'''
There are 5 type of dialog actions (https://docs.aws.amazon.com/lex/latest/dg/API_runtime_DialogAction.html)

- Close - Indicates that there will not be a response from the user.
          For example, the statement "Your order has been placed" does not require a response.

- ConfirmIntent - The next action is asking the user if the intent is complete and ready to be fulfilled.
                  This is a yes/no question such as "Place the order?"

- Delegate - The next action is determined by Amazon Lex V2.

- ElicitIntent - The next action is to elicit an intent from the user.

- ElicitSlot - The next action is to elicit a slot value from the user.
'''


def close(intent_request: dict, fulfillment_state: str, message: str) -> dict:
    """Generate response back to Amazon Lex with Dialog Action = Close
       - Indicates that there will not be a response from the user.

    Args:
        intent_request (dict): Amazon Lex Event Input
        fulfillment_state (str): The fulfillment state of the intent
        message (str): The message that should be shown to the user

    Returns:
        dict: Response for closing dialog action
    """
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
    """Generate response back to Amazon Lex with Dialog Action = Elicit Intent
       - The next action is to elicit an intent from the user.

    Args:
        intent_request (dict): Amazon Lex Event Input
        message (str): The message that should be shown to the user

    Returns:
        dict: Response for elicit intent dialog action
    """
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


def elicit_slot(intent_request, slot_name, message):
    """Generate response back to Amazon Lex with Dialog Action = Elicit Slot
       - The next action is to elicit a slot value from the user.

    Args:
        intent_request (_type_): Amazon Lex Event Input
        slot_name (_type_): The name of the slot that should be elicited from the user.
        message (_type_): The message that should be shown to the user.

    Returns:
        _type_: Response for elicit slot dialog action
    """
    intent_request["sessionState"]["intent"]["state"] = "InProgress"
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": slot_name
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
