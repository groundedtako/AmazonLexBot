import boto3     #boto3 to interact with AWS services
import botocore  #boto3 exceptions
import typing    #typing for python typing
import logging   #logging for cloudwatch
import sys
import json

#Hard Coded In Order To Test
if __name__ == 'AWS_Lambda.handleBACKUPEvent':
    from AWS_Lambda.utils import *
    from AWS_Lambda.constants import *
else:
    from utils import *  #util functions for lex interactions
    from constants import *


### AWS BACKUP


logger = logging.getLogger()


def get_amazon_resource_name(backup_resource: str) -> str:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_backup_plan
    https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html

    Args:
        backup_resource (str): DynamoDB / EC2

    Returns:
        str: Arn for each resources
    """
    if backup_resource == "DynamoDB":
        return [ALL_DDB_ARN]
    elif backup_resource == "EC2":
        return [ALL_EC2_ARN]
    return "Error"


def get_cron_expression(backup_frequency: str) -> str:
    if backup_frequency == "Hourly":
        return HOURLY_CRON
    elif backup_frequency == "Daily":
        return DAILY_CRON
    return "Error"


def search_backup_selection(backup_client: typing.Any, backup_plan_id: str, backup_resource: str) -> dict:
    backup_selections = backup_client.list_backup_selections(BackupPlanId=backup_plan_id)["BackupSelectionsList"]
    target_name = f"Lex-{backup_resource}-selection"
    for selection in backup_selections:
        if selection["SelectionName"] == target_name:
            return selection
    return None


def search_backup_plan(all_backup_plans: list, backup_frequency: str) -> dict:
    #Search for plan
    target_name = f"Lex-{backup_frequency.lower()}-plan"
    for plan in all_backup_plans:
        if plan["BackupPlanName"] == target_name:
            return plan
    return None


def search_role(iam_client: typing.Any, role_name: str):
    roles = iam_client.list_roles()
    for role in roles["Roles"]:
        if role["RoleName"] == role_name:
            return True
    return False


def createServiceRoleForBackup(iam_client: typing.Any):
    Assume_Role_Policy_Document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "backup.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })

    role = iam_client.create_role(RoleName="LexBackupRole", AssumeRolePolicyDocument=Assume_Role_Policy_Document)

    iam_client.attach_role_policy(RoleName="LexBackupRole", PolicyArn=POLICY_FOR_BACKUP_ARN)

    return role


def create_backup_plan(backup_client: typing.Any, backup_frequency: str) -> dict:
    """Creating a backup plan in AWS Backup

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_backup_plan

    Args:
        backup_client (typing.Any): _description_
        backup_frequency (str): _description_

    Returns:
        dict: _description_
    """
    target_name = f"Lex-{backup_frequency.lower()}-plan"

    backup_plan = {
        "BackupPlanName": target_name,
        "Rules": [{
            "RuleName": f"{backup_frequency}-backup-rule",
            "TargetBackupVaultName": "Default",
            "ScheduleExpression": get_cron_expression(backup_frequency)
        }]
    }
    new_backup_plan = backup_client.create_backup_plan(BackupPlan=backup_plan)
    return new_backup_plan


def backup_create_selection(backup_client: typing.Any, intent_request: dict, all_backup_plans: list) -> tuple:
    """Assign resources to a backup plan

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_backup_selection

    Args:
        backup_client (typing.Any): A low-level client representing AWS Backup
        intent_request (dict): Amazon Lex Event Input
        all_backup_plans (list): List of current backup plans

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """
    backup_resource = get_slot(intent_request, "backupResource")
    #Default Vault For Now.
    backup_frequency = get_slot(intent_request, "backupFrequency")

    iam_client = boto3.client("iam")
    if not search_role(iam_client, "LexBackupRole"):
        createServiceRoleForBackup(iam_client)

    role_info = iam_client.get_role(RoleName="LexBackupRole")

    logger.info(f"Role Info : {role_info}")

    backup_plan = search_backup_plan(all_backup_plans, backup_frequency)
    if backup_plan is None:
        backup_plan = create_backup_plan(backup_client, backup_frequency)

    try:
        selection = backup_client.create_backup_selection(BackupPlanId=backup_plan["BackupPlanId"],
                                                          BackupSelection={"SelectionName": f"Lex-{backup_resource}-selection",
                                                                           "IamRoleArn": role_info["Role"]["Arn"],
                                                                           "Resources": get_amazon_resource_name(backup_resource)})
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    if selection is None:
        return False, "Fail Creating Backup Selection"

    return True, f"Successfully Created Beckup Selection Id -> {selection['SelectionId']}!"


def backup_delete_selection(backup_client: typing.Any, intent_request: dict, all_backup_plans: list) -> tuple:
    """Deletes the resource selection associated with a backup plan

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html?highlight=backup#Backup.Client.delete_backup_selection

    Args:
        backup_client (typing.Any): A low-level client representing AWS Backup
        intent_request (dict): Amazon Lex Event Input
        all_backup_plans (list): List of current backup plans

    Returns:
        tuple: (Status, The message that should be shown to the user)
    """
    backup_resource = get_slot(intent_request, "backupResource")
    #Default Vault For Now.
    backup_frequency = get_slot(intent_request, "backupFrequency")

    backup_plan = search_backup_plan(all_backup_plans, backup_frequency)
    if backup_plan is None:
        return False, "Such Backup Plan Doesn't Exists!"

    backup_selections = search_backup_selection(backup_client, backup_plan["BackupPlanId"], backup_resource)
    if backup_selections is None:
        return False, "Such Selections Doesn't Exists!"

    try:
        selection = backup_client.delete_backup_selection(BackupPlanId=backup_plan["BackupPlanId"],
                                                          SelectionId=backup_selections["SelectionId"])
    except botocore.exceptions.ClientError as client_error:
        return False, "[Error] " + client_error.response["Error"]["Message"]
    except botocore.exceptions.ParamValidationError as param_error:
        return False, f"[Error] {param_error}"
    except:  #For All Other Errors
        logger.error(sys.exc_info()[0])
        return False, f"[Error] ({sys.exc_info()[0]}) Unknown Errors. Please Retry Later!"

    return True, f"Successfully Deleted Beckup Selection Id -> {backup_selections['SelectionId']}!"


def backup_handler(intent_request: dict, action: str) -> dict:
    backup_client = boto3.client("backup")

    all_backup_plans = backup_client.list_backup_plans()['BackupPlansList']

    if action == "CreateSelection":
        response = backup_create_selection(backup_client, intent_request, all_backup_plans)
    elif action == "DeleteSelection":
        response = backup_delete_selection(backup_client, intent_request, all_backup_plans)
    else:
        response = (False, f"Sorry Action : {action} Not Supported Yet!")

    if type(response) != tuple:
        return response

    return close(intent_request, "Fulfilled" if response[0] else "Failed", [response[1]] + ENDING_PHRASE)
