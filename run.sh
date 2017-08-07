#!/bin/bash
# lol
echo "$DEVICE_AND_CA_CERT" > deviceCertAndCACert.pem
export CERTIFICATE_PATH=deviceCertAndCACert.pem
echo "$PRIVATE_KEY" > deviceCert.key
export PRIVATE_KEY_PATH=deviceCert.key
echo "$AWS_ROOT_CA" > awsRootCA.pem
export AWS_ROOT_CA_PATH=awsRootCA.pem

python run.py
