import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
import botocore  #boto3 exceptions
import re        #regex for param checking
import logging   #logging for cloudwatch
import sys

#Hard Coded In Order To Test
if __name__ == 'AWS_Lambda.handleS3Event':
    from AWS_Lambda.utils import *
    from AWS_Lambda.constants import *
else:
    from utils import *  #util functions for lex interactions
    from constants import *

### S3

logger = logging.getLogger()


def valid_bucket_name(bucket_name):
    if re.match(r'(?!.*\.\.)^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', bucket_name):
        return True
    return False


def s3_create_bucket(s3_client: typing.Any, intent_request: dict) -> tuple:
    """Creating Bucket in Amazon S3

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket

    Args:
        s3_client (typing.Any): A low-level client representing Amazon Simple Storage Service (S3)
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """

    bucket_name = get_slot(intent_request, "bucketName", True)

    #Parameter Checking For bucket name
    if not valid_bucket_name(bucket_name):
        return elicit_slot(intent_request, "bucketName", "Invalid Bucket Name, Please Enter A Valid Bucket Name.")

    try:
        bucket = s3_client.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if bucket is None:
        return False, "Fail Creating Bucket"

    return True, f"Successfully Created Bucket {bucket_name}"


def s3_put_object(s3_client: typing.Any, intent_request: dict) -> tuple:
    """Putting Object in Amazon S3

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object

    Args:
        s3_client (typing.Any): A low-level client representing Amazon Simple Storage Service (S3)
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)

    Notes:
        only support text as object right now.
    """

    bucket_name = get_slot(intent_request, "bucketName", True)
    body = get_slot(intent_request, "body")
    key = get_slot(intent_request, "key", True)

    #Parameter Checking For bucket name
    if not valid_bucket_name(bucket_name):
        return elicit_slot(intent_request, "bucketName", "Invalid Bucket Name, Please Enter A Valid Bucket Name.")

    try:
        bucket = s3_client.put_object(Bucket=bucket_name, Body=body.encode('ascii'), Key=key)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if bucket is None:
        return False, "Fail Putting Object Into Bucket"
    return True, f"Successfully Put {key} Inside {bucket_name}"


def s3_delete_object(s3_client: typing.Any, intent_request: dict) -> tuple:
    """Deleting Object in Amazon S3

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object

    Args:
        s3_client (typing.Any): A low-level client representing Amazon Simple Storage Service (S3)
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """

    bucket_name = get_slot(intent_request, "bucketName", True)
    key = get_slot(intent_request, "key", True)

    #Parameter Checking For bucket name
    if not valid_bucket_name(bucket_name):
        return elicit_slot(intent_request, "bucketName", "Invalid Bucket Name, Please Enter A Valid Bucket Name.")

    try:
        bucket = s3_client.delete_object(Bucket=bucket_name, Key=key)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if bucket is None:
        return False, "Fail Deleting Object From Bucket"
    return True, f"Successfully Deleted {key} Inside {bucket_name}"


def s3_delete_bucket(s3_client: typing.Any, intent_request: dict) -> tuple:
    """Deleting Bucket in Amazon S3

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket

    Args:
        s3_client (typing.Any): A low-level client representing Amazon Simple Storage Service (S3)
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """

    bucket_name = get_slot(intent_request, "bucketName", True)

    #Parameter Checking For bucket name
    if not valid_bucket_name(bucket_name):
        return elicit_slot(intent_request, "bucketName", "Invalid Bucket Name, Please Enter A Valid Bucket Name.")

    try:
        bucket = s3_client.delete_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if bucket is None:
        return False, "Fail Deleting Bucket"
    return True, f"Successfully Deleted Bucket {bucket_name}"


def s3_handler(intent_request: dict, action: str) -> dict:
    """Amazon S3's handler

    Args:
        intent_request (dict): Amazon Lex Event Input
        action (str): Action user wants to perform

    Returns:
        dict: Close response
    """
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

    if type(response) != tuple:
        return response

    return close(intent_request, "Fulfilled" if response[0] else "Failed", [response[1]] + ENDING_PHRASE)
