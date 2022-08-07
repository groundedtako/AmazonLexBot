import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
import logging  #logging for cloudwatch

from handleDDBEvent import *  #handleDdbEvent to handle ddb events from the user
from handleEC2Event import *  #handleEc2Event to handle ec2 events from the user
from handleS3Event import *  #handleS3Event to handle s3 events from the user
from handleBACKUPEvent import *  #handleBackupEvent to handle backup events from the user
from constants import *
from utils import *  #util functions for lex interactions

#Setting up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
    if resourceType == 'EC2':
        return ec2_handler(intent_request, action)
    elif resourceType == 'DynamoDB':
        return ddb_handler(intent_request, action)
    elif resourceType == 'S3':
        return s3_handler(intent_request, action)
    elif resourceType == "Backup":
        return backup_handler(intent_request, action)
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
