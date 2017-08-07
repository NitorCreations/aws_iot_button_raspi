#!/bin/bash
# lol
echo $(echo "$DEVICE_AND_CA_CERT") | base64 -d > deviceCertAndCACert.pem
export CERTIFICATE_PATH=deviceCertAndCACert.pem
echo $(echo "$PRIVATE_KEY") | base64 -d > deviceCert.key
export PRIVATE_KEY_PATH=deviceCert.key
echo $(echo "$AWS_ROOT_CA") | base64 -d > awsRootCA.pem
export AWS_ROOT_CA_PATH=awsRootCA.pem

python run.py
