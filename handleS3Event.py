import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
from lambdaUtils import * #lambdaUtils for lex interactions


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