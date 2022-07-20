cd testing_DDB

pytest test_ddb.py -s

pause

cd .. 

cd testing_EC2

pytest test_ec2.py -s

pause

cd ..

cd testing_S3

pytest test_s3.py -s

pause