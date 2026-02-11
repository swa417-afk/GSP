# GSP

Governed AI runtime with policy enforcement, human approval flow,
and tamper-evident accountability logging.

Status: Active development.

## AWS institutional bucket bootstrap

Use `scripts/provision_institutional_bucket.sh` to create (or reconcile) a compliant S3 bucket with:
- KMS key + alias
- Object Lock (COMPLIANCE, 365 days)
- Versioning
- SSE-KMS default encryption
- Full public access block

### Run from this repository

```bash
cd /workspace/GSP
REGION=us-east-1 \
BUCKET_NAME=glass-substrate-ledger \
KMS_ALIAS=alias/glass-substrate-key \
./scripts/provision_institutional_bucket.sh
```

By default, output files are written to the repository root:
- `setup-summary.txt`
- `restore_env.sh`

If you want those files in a different location, set `OUTPUT_DIR`:

```bash
OUTPUT_DIR=/tmp ./scripts/provision_institutional_bucket.sh
```

### CloudShell quick start (recommended)

If your shell starts in `~/` (for example `/home/cloudshell-user`), clone the repo first so the script exists locally:

```bash
git clone https://github.com/swa417-afk/GSP.git
cd GSP
./scripts/provision_institutional_bucket.sh
```

> Note: `aws s3 sync s3://glass-substrate-ledger .` syncs bucket objects, **not** this Git repository. If you only ran `aws s3 sync`, the `scripts/` folder from this repo may not exist in your current directory.

### Applying patch/diff snippets safely

If you receive a snippet that starts with lines like `diff --git`, `index ...`, `--- a/...`, `+++ b/...`, or `@@ ...`, **do not paste those lines directly into bash**. Those are patch metadata, not shell commands.

Use this flow instead:

```bash
# 1) Enter the repository first
cd /workspace/GSP

# 2) Confirm you're in a git repo
git rev-parse --show-toplevel

# 3) Save/apply patch content via git apply (example)
git apply --3way your.patch
```

If you see `fatal: not a git repository`, you are in the wrong directory. `cd` into the repo root first.

### Common path mistake

`provision_institutional_bucket.sh` is a **file**, not a directory. If you see an error like:

```bash
cd: scripts/provision_institutional_bucket.sh: No such file or directory
```

use one of these instead:

```bash
# Run directly from repo root
./scripts/provision_institutional_bucket.sh

# OR change into the scripts directory first
cd scripts
./provision_institutional_bucket.sh
```

The script handles the `us-east-1` create-bucket behavior (no `LocationConstraint`) and reuses an existing KMS alias when present.

## AWS VPC environment bootstrap

Use `scripts/create_vpc_environment.sh` to provision a baseline VPC environment with:
- 1 VPC
- 2 public subnets + 2 private subnets (across 2 AZs)
- Internet Gateway
- Public and private route tables
- Default security group for the environment
- Optional NAT gateway (disabled by default to avoid cost)

Example:

```bash
cd /workspace/GSP
REGION=us-east-1 ENV_NAME=gsp-dev ./scripts/create_vpc_environment.sh
```

Enable NAT gateway (incurs AWS charges):

```bash
ENABLE_NAT_GATEWAY=true REGION=us-east-1 ENV_NAME=gsp-dev ./scripts/create_vpc_environment.sh
```

Outputs:
- `vpc-environment-summary.json`
- `restore_vpc_env.sh`

Set `OUTPUT_DIR` to write outputs elsewhere.
