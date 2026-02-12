#!/bin/bash
# 1. Create S3 Audit Bucket with Object Lock, Versioning, Block Public Access, KMS encryption, Default Object Lock

BUCKET=gbalo-audit-bucket
KMS_KEY_ARN="arn:aws:kms:us-east-1:123456789012:key/your-kms-key-id"

# Create bucket with Object Lock (only at creation)
aws s3api create-bucket \
  --bucket $BUCKET \
  --object-lock-enabled-for-bucket \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket $BUCKET \
  --versioning-configuration Status=Enabled \
  --region us-east-1

# Block all public access
aws s3api put-public-access-block \
  --bucket $BUCKET \
  --public-access-block-configuration \
  'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true' \
  --region us-east-1

# Default encryption with SSE-KMS
aws s3api put-bucket-encryption \
  --bucket $BUCKET \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "'"$KMS_KEY_ARN"'"
      }
    }]
  }' \
  --region us-east-1

# Set default Object Lock retention (GOVERNANCE mode, 365 days)
aws s3api put-object-lock-configuration \
  --bucket $BUCKET \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "GOVERNANCE",
        "Days": 365
      }
    }
  }' \
  --region us-east-1