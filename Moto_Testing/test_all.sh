#!/bin/bash
cd testing_DDB

pytest test_ddb.py -s

read -p "Press any key to continue..."

cd .. 

cd testing_EC2

pytest test_ec2.py -s

read -p "Press any key to continue..."

cd ..

cd testing_S3

pytest test_s3.py -s

cd ..

read -p "Press any key to continue..."