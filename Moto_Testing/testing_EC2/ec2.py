import boto3


class MyEC2Client:
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("ec2", region_name=region_name)

    def list_instances(self):
        """Return a list of instances"""
        response = self.client.describe_instances()
        print("\nListing All EC2 Instances : ")
        instances = [i["InstanceId"] for r in response["Reservations"] for i in r["Instances"]]
        print(instances)
        print("-------------------")
        return instances

    def check_instances_state(self, instanceId):
        """Return the status of a specific instance"""
        print("\nInstance's Current State : ")
        state = self.client.describe_instances(InstanceIds=[instanceId])["Reservations"][0]["Instances"][0]["State"]
        print(state)
        print("-------------------")
        return state

    def create_instances(self):
        image_response = self.client.describe_images()
        image_id = image_response['Images'][0]['ImageId']
        return self.client.run_instances(ImageId=image_id,
                                         MinCount=1,
                                         MaxCount=1,
                                         InstanceType="t2.nano")["Instances"][0]["InstanceId"]

    def control_instance_lifecycle(self, instanceId, action):
        if action == "StartInstance":
            self.client.start_instances(InstanceIds=[instanceId])
        elif action == "StopInstance":
            self.client.stop_instances(InstanceIds=[instanceId])
        elif action == "TerminateInstance":
            self.client.terminate_instances(InstanceIds=[instanceId])
        elif action == "RebootInstance":
            self.client.reboot_instances(InstanceIds=[instanceId])
