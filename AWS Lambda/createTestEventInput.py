import json
import re


def create_slot_dict(value: str) -> dict:
    """Helper function to create slot's value

    Args:
        value (str): value for that slot

    Returns:
        dict: resulting dictionary based on args

    Todo:
        -May want to include multiple values
    """

    return {
        "shape": "Scalar",
        "value": {
            "originalValue": value,
            "resolvedValues": [value],
            "interpretedValue": value
        }
    }


def create_test_event(resource: str, intent_name: str, slots_pairs: dict) -> dict:
    """Function mimic Amazon Lex event that is passed to a Lambda Function

    Args:
        resource (str): resource name that want to test (Ex. EC2 / DynamoDB / S3)
        intent_name (str): intent name for given resource (It should follow this regex pattern
                           "(<resource>[a-zA-Z0-9]+)(<action>[a-zA-Z0-9]+)Intent"
                           Ex. DynamoDBCreateTableIntent
        slots_pairs (dict): key-value pairs for given intent (Exclude resource / action)

    Returns:
        dict: resulting test event input based on args json object
    """

    slots = {}
    slots["resource"] = create_slot_dict(resource)

    regex_pattern = f'{resource}(.*)Intent'
    action = re.search(regex_pattern, intent_name).group(1)

    slots[f"{resource}_action"] = create_slot_dict(action)

    for k, v in slots_pairs.items():
        slots[k] = create_slot_dict(v)

    TestEventInput = {
        "sessionId": "279344343543764",
        "sessionState": {
            "sessionAttributes": {},
            "activeContexts": [
                {
                    "timeToLive": {
                        "turnsToLive": 20,
                        "timeToLiveInSeconds": 600
                    },
                    "name": "contextWelcome",
                    "contextAttributes": {
                        "resource": resource
                    }
                }
            ],
            "intent": {
                "slots": slots,
                "confirmationState": "None",
                "name": intent_name,
                "state": "ReadyForFulfillment"
            }
        }
    }
    return TestEventInput
