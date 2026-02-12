#!/bin/bash

ACCOUNT_ID="160768284037"
REGION="us-east-1"
BUCKET="gbalo-audit-${ACCOUNT_ID}"
TRAIL="gbalo-audit-trail"

aws cloudtrail create-trail --name "$TRAIL" --s3-bucket-name "$BUCKET" --s3-key-prefix cloudtrail-logs/ \
  --include-global-service-events --is-multi-region-trail --enable-log-file-validation --region "$REGION"

aws cloudtrail start-logging --name "$TRAIL" --region "$REGION"

echo "CloudTrail $TRAIL sending logs to $BUCKET."