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
