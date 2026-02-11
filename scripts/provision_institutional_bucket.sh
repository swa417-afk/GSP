#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   REGION=us-east-1 BUCKET_NAME=glass-substrate-ledger KMS_ALIAS=alias/glass-substrate-key \
#     ./scripts/provision_institutional_bucket.sh

REGION="${REGION:-us-east-1}"
BUCKET_NAME="${BUCKET_NAME:-glass-substrate-ledger}"
KMS_ALIAS="${KMS_ALIAS:-alias/glass-substrate-key}"

log() {
  echo "[gsp-setup] $*"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Required command not found: $1" >&2
    exit 1
  }
}

require_cmd aws
require_cmd jq

log "Ensuring KMS key exists for alias: ${KMS_ALIAS}"
if aws kms list-aliases --query "Aliases[?AliasName=='${KMS_ALIAS}'].TargetKeyId" --output text | grep -qE '^[a-f0-9-]+'; then
  KMS_KEY_ID="$(aws kms list-aliases --query "Aliases[?AliasName=='${KMS_ALIAS}'].TargetKeyId" --output text)"
  log "Reusing existing KMS key: ${KMS_KEY_ID}"
else
  KMS_KEY_ID="$(aws kms create-key \
    --description "Glass Substrate Protocol KMS Key" \
    --query KeyMetadata.KeyId \
    --output text)"
  aws kms create-alias --alias-name "${KMS_ALIAS}" --target-key-id "${KMS_KEY_ID}"
  log "Created KMS key and alias: ${KMS_KEY_ID}"
fi

log "Ensuring S3 bucket exists with Object Lock enabled: ${BUCKET_NAME}"
if aws s3api head-bucket --bucket "${BUCKET_NAME}" >/dev/null 2>&1; then
  log "Bucket already exists, skipping create"
else
  if [[ "${REGION}" == "us-east-1" ]]; then
    aws s3api create-bucket \
      --bucket "${BUCKET_NAME}" \
      --region "${REGION}" \
      --object-lock-enabled-for-bucket
  else
    aws s3api create-bucket \
      --bucket "${BUCKET_NAME}" \
      --region "${REGION}" \
      --create-bucket-configuration "LocationConstraint=${REGION}" \
      --object-lock-enabled-for-bucket
  fi
  log "Created bucket ${BUCKET_NAME}"
fi

log "Applying security controls"
aws s3api put-bucket-versioning \
  --bucket "${BUCKET_NAME}" \
  --versioning-configuration Status=Enabled

aws s3api put-object-lock-configuration \
  --bucket "${BUCKET_NAME}" \
  --object-lock-configuration '{"ObjectLockEnabled":"Enabled","Rule":{"DefaultRetention":{"Mode":"COMPLIANCE","Days":365}}}'

aws s3api put-bucket-encryption \
  --bucket "${BUCKET_NAME}" \
  --server-side-encryption-configuration "$(jq -cn --arg key "${KMS_KEY_ID}" '{Rules:[{ApplyServerSideEncryptionByDefault:{SSEAlgorithm:"aws:kms",KMSMasterKeyID:$key}}]}')"

aws s3api put-public-access-block \
  --bucket "${BUCKET_NAME}" \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

SUMMARY_FILE="setup-summary.txt"
{
  echo "Bucket: ${BUCKET_NAME}"
  echo "Key: ${KMS_KEY_ID}"
  echo "Alias: ${KMS_ALIAS}"
  echo "Region: ${REGION}"
  aws s3api get-object-lock-configuration --bucket "${BUCKET_NAME}"
} >"${SUMMARY_FILE}"

cat > restore_env.sh <<ENV
export REGION=${REGION}
export BUCKET_NAME=${BUCKET_NAME}
export KMS_KEY_ID=${KMS_KEY_ID}
export KMS_ALIAS=${KMS_ALIAS}
ENV
chmod +x restore_env.sh

log "Provisioning complete"
log "Summary written to ${SUMMARY_FILE}; env restore script written to restore_env.sh"
