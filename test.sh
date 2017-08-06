#!/bin/bash
set -x

export IOT_HOST=$(aws iot describe-endpoint | jq -r .endpointAddress)
export AWS_ROOT_CA_PATH=../aws_iot_poc/cacert/awsRootCA.pem
export PRIVATE_KEY_PATH=../aws_iot_poc/cacert/deviceCert.key
export CERTIFICATE_PATH=../aws_iot_poc/cacert/deviceCertAndCACert.pem
export IOT_CLIENT_ID_PREFIX=button/raspibutton-
export RESIN_DEVICE_UUID=fakeResinDeviceUUID
export THING_NAME=button
export COUNTDOWN_LENGTH=60000
#export TEST_RUN=1

python run.py
