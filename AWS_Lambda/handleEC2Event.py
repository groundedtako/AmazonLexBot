import boto3     #boto3 to interact with AWS services
import botocore  #boto3 exceptions
import logging   #logging for cloudwatch
import typing    #typing for python typing
import sys

#Hard Coded In Order To Test
if __name__ == 'AWS_Lambda.handleEC2Event':
    from AWS_Lambda.utils import *
    from AWS_Lambda.constants import *
else:
    from utils import *  #util functions for lex interactions
    from constants import *

### EC2

logger = logging.getLogger()


def ec2_lifecycle_control(ec2_client: typing.Any, intent_request: dict, action: str) -> tuple:
    """Controlling Instance's LifeCycle in Amazon EC2

    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html

    - Start Instance
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances
    - Stop Instance
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances
    - Terminate Instance
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.terminate_instances

    Args:
        ec2_client (typing.Any): A low-level client representing Amazon Elastic Compute Cloud (EC2)
        intent_request (dict): Amazon Lex Event Input
        action (str): Corresponding action

    Returns:
        tuple: (Status, The message that should be shown to the user)

    Notes:
        - DryRun option to check for permission
        - Check Instance State (In case flooding requests) using describe_instances()
    """
    instanceId = get_slot(intent_request, "instanceId")

    try:
        if action == "StartInstance":
            rsp = ec2_client.start_instances(InstanceIds=[instanceId])
        elif action == "StopInstance":
            rsp = ec2_client.stop_instances(InstanceIds=[instanceId])
        elif action == "TerminateInstance":
            rsp = ec2_client.terminate_instances(InstanceIds=[instanceId])
        elif action == "RebootInstance":
            rsp = ec2_client.reboot_instances(InstanceIds=[instanceId])

    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if rsp is None:
        return False, f"Fail {action}!"

    return True, f"Successfully {action} (Instance's Id : {instanceId})"


def ec2_create_instance(ec2_client: typing.Any, intent_request: dict) -> tuple:
    """Creating Instance in Amazon EC2

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.run_instances

    Args:
        ec2_client (typing.Any): A low-level client representing Amazon Elastic Compute Cloud (EC2)
        intent_request (dict): Amazon Lex Event Input

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """

    imageId = get_slot(intent_request, "amazonMachineImages")
    minCount = int(get_slot(intent_request, "minCount"))
    maxCount = int(get_slot(intent_request, "maxCount"))
    instanceType = get_slot(intent_request, "instanceType")
    # keyName = get_slot(intent_request, "keyName")

    try:
        instance = ec2_client.run_instances(
            ImageId=imageId,
            MinCount=minCount,
            MaxCount=maxCount,
            InstanceType=instanceType,
        )

    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if instance is None:
        return False, "Fail Creating Instance"

    instanceId = instance["Instances"][0]["InstanceId"]
    return True, f"Successfully Created Instance (Instance's Id : {instanceId})"


def ec2_handler(intent_request: dict, action: str) -> dict:
    """Amazon EC2's handler

    Args:
        intent_request (dict): Amazon Lex Event Input
        action (str): Action user wants to perform

    Returns:
        dict: Close response
    """
    ec2_client = boto3.client("ec2")

    if action == "CreateInstance":
        response = ec2_create_instance(ec2_client, intent_request)
    elif action in EC2_LIFECYCLE:
        response = ec2_lifecycle_control(ec2_client, intent_request, action)
    else:
        response = (False, f"Sorry Action : {action} Not Supported Yet!")

    return close(intent_request, "Fulfilled" if response[0] else "Failed", response[1])
