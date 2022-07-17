import pytest
from ec2 import MyEC2Client

# Append to sys path
import sys
sys.path.append('../../../AmazonLexBot')


from AWS_Lambda.handleEC2Event import *
from AWS_Lambda.createTestEventInput import create_test_event


@pytest.fixture
def get_ami(ec2_client):
    ami_rsp = ec2_client.describe_images()
    return ami_rsp['Images'][0]['ImageId']


@pytest.fixture
def create_instance_id(ec2_client, get_ami):
    instance_rsp = ec2_client.run_instances(ImageId=get_ami,
                                            MinCount=1,
                                            MaxCount=1,
                                            InstanceType="t2.nano")
    yield instance_rsp["Instances"][0]["InstanceId"]


'''
EC2 Instance State (Code : Name):

0  : Pending
16 : Running
32 : Shutting-Down
48 : Terminated
64 : Stopping
80 : Stopped
'''


def test_ec2_create(ec2_client, get_ami):
    ec2 = MyEC2Client()
    ec2.list_instances()

    print("\nTesting EC2CreateInstanceIntent:")
    test_intent = create_test_event("EC2", "EC2CreateInstanceIntent", {"amazonMachineImages": get_ami, "minCount": 1,
                                                                       "maxCount": 1, "instanceType": "t2.nano"})
    mock_rsp = ec2_create_instance(ec2.client, test_intent)
    print(mock_rsp)

    assert mock_rsp[0] == True
    assert len(ec2.list_instances()) == 1


def test_ec2_start(ec2_client, get_ami, create_instance_id):
    mock_instance_id = create_instance_id
    ec2 = MyEC2Client()
    ec2.check_instances_state(mock_instance_id)
    ec2.control_instance_lifecycle(mock_instance_id, "Stop")
    ec2.check_instances_state(mock_instance_id)

    print("\nTesting EC2StartInstanceIntent:")
    test_intent = create_test_event("EC2", "EC2StartInstanceIntent", {"instanceId": mock_instance_id})
    mock_rsp = ec2_lifecycle_control(ec2.client, test_intent, "StartInstance")
    print(mock_rsp)

    assert mock_rsp[0] == True
    state = ec2.check_instances_state(mock_instance_id)
    assert state['Code'] == 16
    assert state['Name'] == 'running'


def test_ec2_stop(ec2_client, get_ami, create_instance_id):
    mock_instance_id = create_instance_id
    ec2 = MyEC2Client()
    ec2.check_instances_state(mock_instance_id)

    print("\nTesting EC2StopInstanceIntent:")
    test_intent = create_test_event("EC2", "EC2StopInstanceIntent", {"instanceId": mock_instance_id})
    mock_rsp = ec2_lifecycle_control(ec2.client, test_intent, "StopInstance")
    print(mock_rsp)

    assert mock_rsp[0] == True
    state = ec2.check_instances_state(mock_instance_id)
    assert state['Code'] == 80
    assert state['Name'] == 'stopped'


def test_ec2_terminate(ec2_client, get_ami, create_instance_id):
    mock_instance_id = create_instance_id
    ec2 = MyEC2Client()
    ec2.check_instances_state(mock_instance_id)

    print("\nTesting EC2TerminateInstanceIntent:")
    test_intent = create_test_event("EC2", "EC2TerminateInstanceIntent", {"instanceId": mock_instance_id})
    mock_rsp = ec2_lifecycle_control(ec2.client, test_intent, "TerminateInstance")
    print(mock_rsp)

    assert mock_rsp[0] == True
    state = ec2.check_instances_state(mock_instance_id)
    assert state['Code'] == 48
    assert state['Name'] == 'terminated'


def test_ec2_reboot(ec2_client, get_ami, create_instance_id):
    mock_instance_id = create_instance_id
    ec2 = MyEC2Client()
    ec2.check_instances_state(mock_instance_id)

    print("\nTesting EC2RebootInstanceIntent:")
    test_intent = create_test_event("EC2", "EC2RebootInstanceIntent", {"instanceId": mock_instance_id})
    mock_rsp = ec2_lifecycle_control(ec2.client, test_intent, "RebootInstance")
    print(mock_rsp)

    assert mock_rsp[0] == True
    state = ec2.check_instances_state(mock_instance_id)
    assert state['Code'] == 16
    assert state['Name'] == 'running'
