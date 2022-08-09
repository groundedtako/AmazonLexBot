### Constants

AVAILABLE_RESOURCES = ("EC2", "DynamoDB", "S3", "Backup")
SUPPORTED_ACTIONS = {
    "EC2": ["Create Instance.", "Start Instance.", "Stop Instance.", "Terminate Instance.", "Reboot Instance."],
    "DynamoDB": ["Create Table.", "Delete Table.", "Create Table Item.", "Delete Table Item."],
    "S3": ["Create Bucket.", "Delete Bucket.", "Put Object.", "Delete Object."],
    "Backup": ["Backup Resource.", "Delete Backups."]
}
ENDING_PHRASE = ["Anything Else I Can Help You With?"]

EC2_LIFECYCLE = ("StopInstance", "TerminateInstance", "StartInstance", "RebootInstance")
LINUX_AMI = "ami-090fa75af13c156b4"
WINDOWS_AMI = "ami-05912b6333beaa478"
UBUNTU_AMI = "ami-052efd3df9dad4825"

HOURLY_CRON = "cron(0 5/1 ? * * *)"
DAILY_CRON = "cron(0 5 ? * * *)"
ALL_DDB_ARN = 'arn:aws:dynamodb:*:*:table/*'
ALL_EC2_ARN = 'arn:aws:ec2:*:*:instance/*'
POLICY_FOR_BACKUP_ARN = 'arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup'
