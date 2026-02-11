#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   REGION=us-east-1 ENV_NAME=gsp-dev ./scripts/create_vpc_environment.sh

REGION="${REGION:-us-east-1}"
ENV_NAME="${ENV_NAME:-gsp-dev}"
VPC_CIDR="${VPC_CIDR:-10.42.0.0/16}"
PUBLIC_SUBNET_A_CIDR="${PUBLIC_SUBNET_A_CIDR:-10.42.1.0/24}"
PUBLIC_SUBNET_B_CIDR="${PUBLIC_SUBNET_B_CIDR:-10.42.2.0/24}"
PRIVATE_SUBNET_A_CIDR="${PRIVATE_SUBNET_A_CIDR:-10.42.11.0/24}"
PRIVATE_SUBNET_B_CIDR="${PRIVATE_SUBNET_B_CIDR:-10.42.12.0/24}"
ENABLE_NAT_GATEWAY="${ENABLE_NAT_GATEWAY:-false}" # true may incur cost
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/..}"

log() {
  echo "[gsp-vpc] $*"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Required command not found: $1" >&2
    exit 1
  }
}

require_cmd aws
require_cmd jq

get_az() {
  local index="$1"
  aws ec2 describe-availability-zones \
    --region "${REGION}" \
    --filters Name=state,Values=available \
    --query "AvailabilityZones[${index}].ZoneName" \
    --output text
}

ensure_tagged_resource() {
  local query="$1"
  aws ec2 describe-tags --region "${REGION}" --filters ${query} --query 'Tags[0].ResourceId' --output text
}

AZ_A="$(get_az 0)"
AZ_B="$(get_az 1)"

if [[ -z "${AZ_A}" || -z "${AZ_B}" || "${AZ_A}" == "None" || "${AZ_B}" == "None" ]]; then
  echo "Need at least 2 availability zones in ${REGION}" >&2
  exit 1
fi

VPC_NAME="${ENV_NAME}-vpc"
IGW_NAME="${ENV_NAME}-igw"
PUB_RT_NAME="${ENV_NAME}-public-rt"
PRIV_RT_NAME="${ENV_NAME}-private-rt"
SG_NAME="${ENV_NAME}-default-sg"

log "Ensuring VPC ${VPC_NAME}"
VPC_ID="$(aws ec2 describe-vpcs --region "${REGION}" --filters Name=tag:Name,Values="${VPC_NAME}" --query 'Vpcs[0].VpcId' --output text)"
if [[ -z "${VPC_ID}" || "${VPC_ID}" == "None" ]]; then
  VPC_ID="$(aws ec2 create-vpc --region "${REGION}" --cidr-block "${VPC_CIDR}" --query 'Vpc.VpcId' --output text)"
  aws ec2 create-tags --region "${REGION}" --resources "${VPC_ID}" --tags Key=Name,Value="${VPC_NAME}" Key=Environment,Value="${ENV_NAME}"
  aws ec2 modify-vpc-attribute --region "${REGION}" --vpc-id "${VPC_ID}" --enable-dns-hostnames '{"Value":true}'
  aws ec2 modify-vpc-attribute --region "${REGION}" --vpc-id "${VPC_ID}" --enable-dns-support '{"Value":true}'
  log "Created VPC ${VPC_ID}"
else
  log "Reusing existing VPC ${VPC_ID}"
fi

create_subnet_if_missing() {
  local name="$1" cidr="$2" az="$3" public_ip="$4"
  local subnet_id
  subnet_id="$(aws ec2 describe-subnets --region "${REGION}" --filters Name=vpc-id,Values="${VPC_ID}" Name=tag:Name,Values="${name}" --query 'Subnets[0].SubnetId' --output text)"
  if [[ -z "${subnet_id}" || "${subnet_id}" == "None" ]]; then
    subnet_id="$(aws ec2 create-subnet --region "${REGION}" --vpc-id "${VPC_ID}" --cidr-block "${cidr}" --availability-zone "${az}" --query 'Subnet.SubnetId' --output text)"
    aws ec2 create-tags --region "${REGION}" --resources "${subnet_id}" --tags Key=Name,Value="${name}" Key=Environment,Value="${ENV_NAME}"
    if [[ "${public_ip}" == "true" ]]; then
      aws ec2 modify-subnet-attribute --region "${REGION}" --subnet-id "${subnet_id}" --map-public-ip-on-launch
    fi
    log "Created subnet ${name}: ${subnet_id}"
  else
    log "Reusing subnet ${name}: ${subnet_id}"
  fi
  echo "${subnet_id}"
}

PUB_A_ID="$(create_subnet_if_missing "${ENV_NAME}-public-a" "${PUBLIC_SUBNET_A_CIDR}" "${AZ_A}" true)"
PUB_B_ID="$(create_subnet_if_missing "${ENV_NAME}-public-b" "${PUBLIC_SUBNET_B_CIDR}" "${AZ_B}" true)"
PRIV_A_ID="$(create_subnet_if_missing "${ENV_NAME}-private-a" "${PRIVATE_SUBNET_A_CIDR}" "${AZ_A}" false)"
PRIV_B_ID="$(create_subnet_if_missing "${ENV_NAME}-private-b" "${PRIVATE_SUBNET_B_CIDR}" "${AZ_B}" false)"

IGW_ID="$(aws ec2 describe-internet-gateways --region "${REGION}" --filters Name=attachment.vpc-id,Values="${VPC_ID}" Name=tag:Name,Values="${IGW_NAME}" --query 'InternetGateways[0].InternetGatewayId' --output text)"
if [[ -z "${IGW_ID}" || "${IGW_ID}" == "None" ]]; then
  IGW_ID="$(aws ec2 create-internet-gateway --region "${REGION}" --query 'InternetGateway.InternetGatewayId' --output text)"
  aws ec2 create-tags --region "${REGION}" --resources "${IGW_ID}" --tags Key=Name,Value="${IGW_NAME}" Key=Environment,Value="${ENV_NAME}"
  aws ec2 attach-internet-gateway --region "${REGION}" --internet-gateway-id "${IGW_ID}" --vpc-id "${VPC_ID}"
  log "Created and attached IGW ${IGW_ID}"
else
  log "Reusing internet gateway ${IGW_ID}"
fi

PUB_RT_ID="$(aws ec2 describe-route-tables --region "${REGION}" --filters Name=vpc-id,Values="${VPC_ID}" Name=tag:Name,Values="${PUB_RT_NAME}" --query 'RouteTables[0].RouteTableId' --output text)"
if [[ -z "${PUB_RT_ID}" || "${PUB_RT_ID}" == "None" ]]; then
  PUB_RT_ID="$(aws ec2 create-route-table --region "${REGION}" --vpc-id "${VPC_ID}" --query 'RouteTable.RouteTableId' --output text)"
  aws ec2 create-tags --region "${REGION}" --resources "${PUB_RT_ID}" --tags Key=Name,Value="${PUB_RT_NAME}" Key=Environment,Value="${ENV_NAME}"
fi
aws ec2 create-route --region "${REGION}" --route-table-id "${PUB_RT_ID}" --destination-cidr-block 0.0.0.0/0 --gateway-id "${IGW_ID}" >/dev/null 2>&1 || true
aws ec2 associate-route-table --region "${REGION}" --route-table-id "${PUB_RT_ID}" --subnet-id "${PUB_A_ID}" >/dev/null 2>&1 || true
aws ec2 associate-route-table --region "${REGION}" --route-table-id "${PUB_RT_ID}" --subnet-id "${PUB_B_ID}" >/dev/null 2>&1 || true

PRIV_RT_ID="$(aws ec2 describe-route-tables --region "${REGION}" --filters Name=vpc-id,Values="${VPC_ID}" Name=tag:Name,Values="${PRIV_RT_NAME}" --query 'RouteTables[0].RouteTableId' --output text)"
if [[ -z "${PRIV_RT_ID}" || "${PRIV_RT_ID}" == "None" ]]; then
  PRIV_RT_ID="$(aws ec2 create-route-table --region "${REGION}" --vpc-id "${VPC_ID}" --query 'RouteTable.RouteTableId' --output text)"
  aws ec2 create-tags --region "${REGION}" --resources "${PRIV_RT_ID}" --tags Key=Name,Value="${PRIV_RT_NAME}" Key=Environment,Value="${ENV_NAME}"
fi
aws ec2 associate-route-table --region "${REGION}" --route-table-id "${PRIV_RT_ID}" --subnet-id "${PRIV_A_ID}" >/dev/null 2>&1 || true
aws ec2 associate-route-table --region "${REGION}" --route-table-id "${PRIV_RT_ID}" --subnet-id "${PRIV_B_ID}" >/dev/null 2>&1 || true

if [[ "${ENABLE_NAT_GATEWAY}" == "true" ]]; then
  EIP_ALLOC_ID="$(aws ec2 describe-addresses --region "${REGION}" --filters Name=tag:Name,Values="${ENV_NAME}-nat-eip" --query 'Addresses[0].AllocationId' --output text)"
  if [[ -z "${EIP_ALLOC_ID}" || "${EIP_ALLOC_ID}" == "None" ]]; then
    EIP_ALLOC_ID="$(aws ec2 allocate-address --region "${REGION}" --domain vpc --query 'AllocationId' --output text)"
    aws ec2 create-tags --region "${REGION}" --resources "${EIP_ALLOC_ID}" --tags Key=Name,Value="${ENV_NAME}-nat-eip" Key=Environment,Value="${ENV_NAME}"
  fi
  NAT_GW_ID="$(aws ec2 describe-nat-gateways --region "${REGION}" --filter Name=vpc-id,Values="${VPC_ID}" Name=state,Values=available,pending --query 'NatGateways[0].NatGatewayId' --output text)"
  if [[ -z "${NAT_GW_ID}" || "${NAT_GW_ID}" == "None" ]]; then
    NAT_GW_ID="$(aws ec2 create-nat-gateway --region "${REGION}" --subnet-id "${PUB_A_ID}" --allocation-id "${EIP_ALLOC_ID}" --query 'NatGateway.NatGatewayId' --output text)"
    log "Created NAT gateway ${NAT_GW_ID} (may take several minutes to become available)"
  fi
  aws ec2 create-route --region "${REGION}" --route-table-id "${PRIV_RT_ID}" --destination-cidr-block 0.0.0.0/0 --nat-gateway-id "${NAT_GW_ID}" >/dev/null 2>&1 || true
else
  log "NAT gateway creation disabled (ENABLE_NAT_GATEWAY=false)"
fi

SG_ID="$(aws ec2 describe-security-groups --region "${REGION}" --filters Name=vpc-id,Values="${VPC_ID}" Name=group-name,Values="${SG_NAME}" --query 'SecurityGroups[0].GroupId' --output text)"
if [[ -z "${SG_ID}" || "${SG_ID}" == "None" ]]; then
  SG_ID="$(aws ec2 create-security-group --region "${REGION}" --vpc-id "${VPC_ID}" --group-name "${SG_NAME}" --description "Default SG for ${ENV_NAME}" --query 'GroupId' --output text)"
  aws ec2 create-tags --region "${REGION}" --resources "${SG_ID}" --tags Key=Name,Value="${SG_NAME}" Key=Environment,Value="${ENV_NAME}"
fi
aws ec2 authorize-security-group-egress --region "${REGION}" --group-id "${SG_ID}" --ip-permissions '[{"IpProtocol":"-1","IpRanges":[{"CidrIp":"0.0.0.0/0"}]}]' >/dev/null 2>&1 || true

jq -n \
  --arg region "${REGION}" \
  --arg envName "${ENV_NAME}" \
  --arg vpcId "${VPC_ID}" \
  --arg pubA "${PUB_A_ID}" \
  --arg pubB "${PUB_B_ID}" \
  --arg privA "${PRIV_A_ID}" \
  --arg privB "${PRIV_B_ID}" \
  --arg igw "${IGW_ID}" \
  --arg publicRt "${PUB_RT_ID}" \
  --arg privateRt "${PRIV_RT_ID}" \
  --arg sg "${SG_ID}" \
  '{region:$region, environment:$envName, vpcId:$vpcId, publicSubnets:[$pubA,$pubB], privateSubnets:[$privA,$privB], internetGatewayId:$igw, publicRouteTableId:$publicRt, privateRouteTableId:$privateRt, securityGroupId:$sg}' \
  > "${OUTPUT_DIR}/vpc-environment-summary.json"

cat > "${OUTPUT_DIR}/restore_vpc_env.sh" <<ENV
export REGION=${REGION}
export ENV_NAME=${ENV_NAME}
export VPC_ID=${VPC_ID}
export PUBLIC_SUBNET_A_ID=${PUB_A_ID}
export PUBLIC_SUBNET_B_ID=${PUB_B_ID}
export PRIVATE_SUBNET_A_ID=${PRIV_A_ID}
export PRIVATE_SUBNET_B_ID=${PRIV_B_ID}
export SECURITY_GROUP_ID=${SG_ID}
ENV
chmod +x "${OUTPUT_DIR}/restore_vpc_env.sh"

log "VPC environment ready"
log "Summary: ${OUTPUT_DIR}/vpc-environment-summary.json"
log "Restore script: ${OUTPUT_DIR}/restore_vpc_env.sh"
