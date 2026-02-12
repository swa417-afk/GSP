#!/bin/bash
# 2. Enable AWS CloudTrail with Object Lock bucket, multi-region, KMS encryption, log file validation

BUCKET=gbalo-audit-bucket
KMS_KEY_ARN="arn:aws:kms:us-east-1:123456789012:key/your-kms-key-id"
TRAIL=gbalo-audit-trail

aws cloudtrail create-trail \
  --name $TRAIL \
  --s3-bucket-name $BUCKET \
  --s3-key-prefix cloudtrail-logs/ \
  --is-multi-region-trail \
  --include-global-service-events \
  --enable-log-file-validation \
  --kms-key-id $KMS_KEY_ARN \
  --region us-east-1

# Enable management events (read/write: enabled by default on new trail)
aws cloudtrail update-trail \
  --name $TRAIL \
  --is-multi-region-trail \
  --include-global-service-events \
  --enable-log-file-validation \
  --region us-east-1

aws cloudtrail start-logging --name $TRAIL --region us-east-1