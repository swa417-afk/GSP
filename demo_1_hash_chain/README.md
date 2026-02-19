# Demo 1: Hash Chain

Minimal append-only log demonstrating hash-chained entries for GSP evidence.

## Prerequisites

- Python 3.9+ (standard library only)

## Usage

```bash
cd demo_1_hash_chain

# Validate the provided genesis record
python app.py verify

# Append a new entry
python app.py add "Captured approval for request #1234"

# Show the full chain
python app.py show
```

Entries are stored in `storage.json`, each containing:
- `index`: zero-based position in the chain
- `timestamp`: UTC timestamp when recorded
- `payload`: message body
- `prev_hash`: hash of the previous entry (or `null` for genesis)
- `hash`: SHA-256 over the entry contents (excluding this `hash` field)

Any tampering with an entry or its order will cause `python app.py verify` to fail.
