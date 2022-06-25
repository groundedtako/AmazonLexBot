# AmazonLexBot

## Table of Content

<hr></hr>

-   [Team Info](#team-info)
-   [Project Description](#project-description)
-   [Basic Terminology](#basic-terminology)
-   [Features](#features)
-   [Architecture Diagram](#architecture-diagram)
-   [Demo Video](#demo-video)
-   [How To Test It Locally](#how-to-test-it-locally)
-   [Sample Input Event Format With Explanations](#sample-input-event-format-with-explanations)
-   [Sample Response Format With Explanations](#sample-response-format-with-explanations)
-   [Useful Links](#useful-links)

## Team Info

<hr></hr>

### Sparc Competition Summer 2022

### Project Amazon Lex - Team Blue

</br>

## Project Description

<hr></hr>

Use voice to manage AWS resources. Use voice through Amazon Lex (V2) to create an EC2 instance, DDB table, or S3 bucket. The voice command should also be able to create a row in the DDB table or an object in the S3 bucket. When the command is complete, the application should be able to notify the user through a vocal output using Amazon Polly. (Amazon Lex comes pre-integrated with the neural speech-to-text voices from Amazon Polly)

</br>

## Basic Terminology

<hr></hr>

-   <b>Bot</b>
    -   Think of it as a robot which is powered by speech recognition. They are able to preform automated task based on the given voice input.
-   <b>Intent</b>
    -   Think of it as a task that you can assign to the bot. A bot can support multiple intent
    -   The following parameters are required for an intent
        -   <b>Intent name</b>
            -   Desciptive name for the intent
        -   <b>Sample utterances</b>
            -   A spoken word or statement that can convey the intent (works like a trigger)
-   <b>Slot</b>
    -   Think of it as necessary informations in order for the bot to fulfill the intent.
        It could be zero or more.
-   <b>Slot Type</b>

    -   Type for the slot. There is a built-in slot type or you can also create your own slot type.

-   <b>Lambda Function</b>
    -   An AWS serverless compute service runs code in response to event triggers. In this case, we are using it to fulfill intent and data validation.

</br>

## Features

<hr></hr>

### TBD

</br>

## Architecture Diagram

<hr></hr>

![Diagram](/ArchitectureDiagram.JPG)

</br>

## Demo Video

<hr></hr>

### TBD

</br>

## How To Test It Locally

<hr></hr>

To import a Lex Bot into your own AWS account

1. Sign in to the [AWS Management Console](https://aws.amazon.com/), and open the [Amazon Lex](https://console.aws.amazon.com/lex/) console

2. Choose Bots, then choose the bot to import. To import a new bot, skip this step.

3. For Actions, choose Import.

4. For Import Bot, choose the [.zip archive](https://github.com/Kelvin-Hui/AmazonLexBot/blob/main/ResourceLex-LexBot.zip) that contains the JSON file that contains the bot to import. If you want to see merge conflicts before merging, choose to Notify me of merge conflicts. If you turn off conflict checking, the $LATEST version of all of the resources used by the bot is overwritten.

5. Choose Import. If you have chosen to be notified of merge conflicts and there are conflicts, a dialog appears that lists them. To overwrite the $LATEST version of all conflicting resources, choose Overwrite and continue. To stop the import, choose Cancel.

6. Make Sure you have a valid [lambda function](https://github.com/Kelvin-Hui/AmazonLexBot/blob/main/handleLexEventInput.py) both deployed and attached to the bot before you build & test

</br>

## Sample Input Event Format With Explanations

<hr></hr>

This is the general format that Amazon Lex Event that is passed to a Lambda function

```json
{
    "messageVersion": "1.0",
    /*
    invocationSource – Indicates the action that is called the Lambda function.
    When the source is DialogCodeHook, the Lambda function was called after input from the user.
    When the source is FulfillmentCodeHook the Lambda function was called after all required slots have been filled and the intent is ready for fulfillment.
    */
    "invocationSource": "DialogCodeHook | FulfillmentCodeHook",
    "inputMode": "DTMF | Speech | Text",
    "responseContentType": "CustomPayload | ImageResponseCard | PlainText | SSML",
    "sessionId": "string",
    //The text that was used to process the input from the user.
    "inputTranscript": "string",
    "bot": {
        "id": "string",
        "name": "string",
        "aliasId": "string",
        "localeId": "string",
        "version": "string"
    },
    /*
    interpretations – One or more intents that Amazon Lex V2 considers possible matches to the user's utterance
    */
    "interpretations": [
        {
            "intent": {
                "confirmationState": "Confirmed | Denied | None",
                "name": "string",
                "slots": {
                    "string": {
                        "value": {
                            "interpretedValue": "string",
                            "originalValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        }
                    },
                    "string": {
                        "shape": "List",
                        "value": {
                            "interpretedValue": "string",
                            "originalValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        },
                        "values": [
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "interpretedValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            },
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "interpretedValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            }
                        ]
                    }
                },
                "state": "Failed | Fulfilled | FulfillmentInProgress | InProgress | ReadyForFulfillment | Waiting",
                "kendraResponse": {
                    // Only present when intent is KendraSearchIntent. For details, see
                    // https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html#API_Query_ResponseSyntax
                }
            },
            "nluConfidence": {
                "score": number
            },
            "sentimentResponse": {
                "sentiment": "string",
                "sentimentScore": {
                    "mixed": number,
                    "negative": number,
                    "neutral": number,
                    "positive": number
                }
            }
        }
    ],
    /*
    proposedNextState – The next state of the dialog between the user and the bot if the Lambda function doesn't change the flow.
    */
    "proposedNextState": {
        "dialogAction": {
            "slotToElicit": "string",
            "type": "Close | ConfirmIntent | Delegate | ElicitIntent | ElicitSlot"
        },
        "intent": {
            "name": "string",
            "confirmationState": "Confirmed | Denied | None",
            "slots": {},
            "state": "Failed | Fulfilled | InProgress | ReadyForFulfillment | Waiting"
        }
    },
    //requestAttributes – Request-specific attributes that the client sends in the request. Use request attributes to pass information that doesn't need to persist for the entire session.
    "requestAttributes": {
        "string": "string"
    },
    //sessionState – The current state of the conversation between the user and your Amazon Lex V2 bot.
    "sessionState": {
        "activeContexts": [
            {
                "name": "string",
                "contextAttributes": {
                    "string": "string"
                },
                "timeToLive": {
                    "timeToLiveInSeconds": number,
                    "turnsToLive": number
                }
            }
        ],
        "sessionAttributes": {
            "string": "string"
        },
        "runtimeHints": {
            "slotHints": {
                "string": {
                    "string": {
                        "runtimeHintValues": [
                            {
                                "phrase": "string"
                            },
                            {
                                "phrase": "string"
                            }
                        ]
                    }
                }
            }
        },
        "dialogAction": {
            "slotToElicit": "string",
            "type": "Close | ConfirmIntent | Delegate | ElicitIntent | ElicitSlot"
        },
        "intent": {
            "confirmationState": "Confirmed | Denied | None",
            "name": "string",
            "slots": {
                "string": {
                    "value": {
                        "interpretedValue": "string",
                        "originalValue": "string",
                        "resolvedValues": [
                            "string"
                        ]
                    }
                },
                "string": {
                    "shape": "List",
                    "value": {
                        "interpretedValue": "string",
                        "originalValue": "string",
                        "resolvedValues": [
                            "string"
                        ]
                    },
                    "values": [
                        {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "string",
                                "interpretedValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        },
                        {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "string",
                                "interpretedValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        }
                    ]
                }
            },
            "state": "Failed | Fulfilled | FulfillmentInProgress | InProgress | ReadyForFulfillment | Waiting",
            "kendraResponse": {
                // Only present when intent is KendraSearchIntent. For details, see
                // https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html#API_Query_ResponseSyntax                     }
            },
            "originatingRequestId": "string"
        }
    },
    //transcriptions – one or more transcriptions that Amazon Lex V2 considers possible matches to the user's audio utterance
    "transcriptions": [
        {
            "transcription": "string",
            "transcriptionConfidence": {
                "score": "number"
            },
            "resolvedContext": {
                "intent": "string"
            },
            "resolvedSlots": {
                "string": {
                    "shape": "List",
                    "value": {
                        "originalValue": "string",
                        "resolvedValues": [
                            "string"
                        ]
                    },
                    "values": [
                        {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        },
                        {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        }
                    ]
                }
            }
        }
    ]
}
```

</br>

## Sample Response Format With Explanations

<hr></hr>

This is the general response format that Amazon Lex expects from Lambda

```json
{
    /*
    sessionState – Required.
    The current state of the conversation with the user.
    The actual contents of the structure depend on the type of dialog action.
    */
    "sessionState": {
        "activeContexts": [
            {
                "name": "string",
                "contextAttributes": {
                    "key": "value"
                },
                "timeToLive": {
                    "timeToLiveInSeconds": number,
                    "turnsToLive": number
                }
            }
        ],
        "sessionAttributes": {
            "string": "string"
        },
        "runtimeHints": {
            "slotHints": {
                "string": {
                    "string": {
                        "runtimeHintValues": [
                            {
                                "phrase": "string"
                            },
                            {
                                "phrase": "string"
                            }
                        ]
                    }
                }
            }
        },
        /*
        dialogAction – Determines the type of action that Amazon Lex V2 should take in response to the Lambda function.
        The type field is always required.
        The slotToElicit field is required only when dialogAction.type is ElicitSlot
        */
        "dialogAction": {
            "slotElicitationStyle": "Default | SpellByLetter | SpellByWord",
            "slotToElicit": "string",
            "type": "Close | ConfirmIntent | Delegate | ElicitIntent | ElicitSlot"
        },
        /*
        intent – The name of the intent that Amazon Lex V2 should use.
        Not required when dialogAction.type is Delegate or ElicitIntent.
        */
        "intent": {
            "confirmationState": "Confirmed | Denied | None",
            "name": "string",
            "slots": {
                "string": {
                    "value": {
                        "interpretedValue": "string",
                        "originalValue": "string",
                        "resolvedValues": [
                            "string"
                        ]
                    }
                },
                "string": {
                    "shape": "List",
                    "value": {
                        "originalValue": "string",
                        "interpretedValue": "string",
                        "resolvedValues": [
                            "string"
                        ]
                    },
                    "values": [
                        {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "string",
                                "interpretedValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        },
                        {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "string",
                                "interpretedValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        }
                    ]
                }
            },
            //state – Required.
            //The state can only be ReadyForFulfillment if dialogAction.type is Delegate
            "state": "Failed | Fulfilled | FulfillmentInProgress | InProgress | ReadyForFulfillment | Waiting"
        }
    },
    /*
    messages – Required if dialogAction.type is ElicitIntent.
    One or more messages that Amazon Lex V2 shows to the customer to perform the next turn of the conversation.
    If you don't supply messages, Amazon Lex V2 uses the appropriate message defined when the bot was created.
    */
    "messages": [
        {
            //contentType – The type of message to use.
            "contentType": "CustomPayload | ImageResponseCard | PlainText | SSML",
            //content – If the message type is PlainText, CustomPayload, or SSML, the content field contains the message to send to the user.
            "content": "string",
            //imageResponseCard – If the message type is ImageResponseCard, contains the definition of the response card to show to the user.
            "imageResponseCard": {
                "title": "string",
                "subtitle": "string",
                "imageUrl": "string",
                "buttons": [
                    {
                        "text": "string",
                        "value": "string"
                    }
                ]
            }
        }
    ],
    "requestAttributes": {
        "string": "string"
    }
}
```

</br>

## Useful links

<hr></hr>

-   [AWS Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
-   [Boto3 Client vs. Resource](https://www.learnaws.org/2021/02/24/boto3-resource-client/)
-   [JSON Formattor & Validator](https://jsonformatter.curiousconcept.com/#)
-   [AWS Lambda Function Logging In Python](https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html)
-   [Amazon Lex V2 Deveoper Guide](https://docs.aws.amazon.com/lexv2/latest/dg/lex2.0.pdf)
-   [Sharing Slots Between Intent Using Context](https://docs.aws.amazon.com/lex/latest/dg/context-mgmt-active-context.html)
-   [More Terminology Explanations](https://docs.aws.amazon.com/lexv2/latest/dg/API_Types_Amazon_Lex_Runtime_V2.html)

</br>
