# Non-Normative Reference Implementations

This directory contains non-normative reference materials demonstrating
conformant deployments of the Glass Substrate Protocol.

These examples are provided for illustrative purposes only.
Equivalent implementations using alternative infrastructure are equally valid.

## AWS Reference Implementation

Initial AWS-based reference implementations and schemas are published here.

### Components

- **S3 WORM Buckets**: Tamper-evident storage configuration
- **CloudTrail Integration**: Audit logging infrastructure
- **KMS Encryption**: Key management and encryption at rest

### Scripts

See the `/scripts` directory in the repository root for:
- `provision_institutional_bucket.sh` - S3 bucket provisioning
- `create_vpc_environment.sh` - VPC infrastructure setup

## Non-Normative Status

These implementations demonstrate **one possible approach** to conformant GSP
deployment. They are not requirements.

Organizations may implement GSP using:
- Different cloud providers (Azure, GCP, on-premises)
- Different storage backends
- Different encryption mechanisms
- Different audit logging systems

As long as the implementation satisfies the protocol requirements for:
1. Tamper-evident logging
2. Cryptographic integrity
3. Audit trail preservation
4. Access controls

The specific infrastructure choices remain at the implementer's discretion.

## Alternative Implementations

We welcome contributions of reference implementations using other platforms
and technologies. All reference materials should be clearly marked as
non-normative.

## Questions

For questions about these reference implementations, open an issue in the
main repository.
