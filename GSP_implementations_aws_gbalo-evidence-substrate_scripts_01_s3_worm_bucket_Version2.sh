#!/bin/bash

ACCOUNT_ID="160768284037"
REGION="us-east-1"
BUCKET="gbalo-audit-${ACCOUNT_ID}"

# Create the bucket if not present
aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null || \
  aws s3api create-bucket --bucket "$BUCKET" --object-lock-enabled-for-bucket --region "$REGION"

# Enable object lock (WORM) governance mode by default for new objects
aws s3api put-object-lock-configuration \
  --bucket "$BUCKET" \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "GOVERNANCE",
        "Days": 365
      }
    }
  }'

# Block all public access
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

echo "WORM bucket $BUCKET setup complete."