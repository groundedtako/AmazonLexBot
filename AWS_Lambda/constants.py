### Constants
AVAILABLE_RESOURCES = ("EC2", "DynamoDB", "S3")
EC2_LIFECYCLE = ("StopInstance", "TerminateInstance", "StartInstance", "RebootInstance")
HOURLY_CRON = "cron(0 5/1 ? * * *)"
DAILY_CRON = "cron(0 5 ? * * *)"
ALL_DDB_ARN = 'arn:aws:dynamodb:*:*:table/*'
ALL_EC2_ARN = 'arn:aws:ec2:*:*:instance/*'
POLICY_FOR_BACKUP_ARN = 'arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup'
