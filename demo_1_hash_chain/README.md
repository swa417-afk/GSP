# Demo 1: Hash Chain

Append-only attestation log demonstrating hash-chained entries for GSP evidence.

## Prerequisites

- Python 3.9+ (standard library only)

## Usage

```bash
cd demo_1_hash_chain
python app.py
```

Menu options:
1. Create an attestation (prompts for `userId` and `action`)
2. Verify the stored chain
3. Reconstruct (prints timestamps, actions, and hash prefixes)
4. Exit

Entries are stored in `storage.json` as a list, each containing:
- `id`: attestation UUID
- `issuer`: fixed to `GSP-Demo`
- `userId`: actor identifier
- `action`: recorded action
- `metadata`: optional JSON object
- `timestamp`: UTC timestamp at creation
- `previousHash`: hash of the prior attestation (or `null` for the first)
- `hash`: SHA-256 over the attestation contents (excluding this `hash` field)

Any tampering with an entry or its order will cause verification to fail.
