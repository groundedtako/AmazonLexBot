import boto3    #boto3 to interact with AWS services
import typing   #typing for python typing
from lambdaUtils import * #lambdaUtils for lex interactions


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