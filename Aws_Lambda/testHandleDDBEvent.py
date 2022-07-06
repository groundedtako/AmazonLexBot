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
    def setUp(self):
        ddb_client = boto3.client("dynamodb", region_name="us-east-1")

    def test_creating_a_bucket(self):
        ddb_client = boto3.client("dynamodb", region_name="us-east-1")
        # intent_request = create_test_event(resource="DynamoDB", intent_name="DynamoDBCreateTableIntent",
        # slots_pairs={"partitionKey":"s", "partitionKeyType":"s", "tableName": "testing_table"})
        intent_request = {
                        "sessionId":"12312313",
                        "sessionState":{
                            "sessionAttributes":{
                                
                            },
                            "activeContexts":[
                                {
                                    "timeToLive":{
                                    "turnsToLive":20,
                                    "timeToLiveInSeconds":600
                                    },
                                    "name":"contextWelcome",
                                    "contextAttributes":{
                                    "resource":"DynamoDB"
                                    }
                                }
                            ],
                            "intent":{
                                "slots":{
                                    "resource":{
                                    "shape":"Scalar",
                                    "value":{
                                        "originalValue":"DynamoDB",
                                        "resolvedValues":[
                                            "DynamoDB"
                                        ],
                                        "interpretedValue":"DynamoDB"
                                    }
                                    },
                                    "DynamoDB_action":{
                                    "shape":"Scalar",
                                    "value":{
                                        "originalValue":"CreateTable",
                                        "resolvedValues":[
                                            "CreateTable"
                                        ],
                                        "interpretedValue":"CreateTable"
                                    }
                                    },
                                    "partitionKey":{
                                    "shape":"Scalar",
                                    "value":{
                                        "originalValue":"s",
                                        "resolvedValues":[
                                            "s"
                                        ],
                                        "interpretedValue":"s"
                                    }
                                    },
                                    "partitionKeyType":{
                                    "shape":"Scalar",
                                    "value":{
                                        "originalValue":"s",
                                        "resolvedValues":[
                                            "s"
                                        ],
                                        "interpretedValue":"s"
                                    }
                                    },
                                    "tableName":{
                                    "shape":"Scalar",
                                    "value":{
                                        "originalValue":"testing_table",
                                        "resolvedValues":[
                                            "testing_table"
                                        ],
                                        "interpretedValue":"testing_table"
                                    }
                                    }
                                },
                                "confirmationState":"None",
                                "name":"DynamoDBCreateTableIntent",
                                "state":"ReadyForFulfillment"
                            }
                        }
                    }
        bucket = ddb_create_table(ddb_client, intent_request)
        print(bucket[1])
        assert bucket[0] == True


if __name__ == "__main__":
    test = TestMockClassLevel()
    test.test_creating_a_bucket()