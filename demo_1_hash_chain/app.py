import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


STORAGE_PATH = Path(__file__).with_name("storage.json")


def load_chain() -> List[Dict[str, Any]]:
    if not STORAGE_PATH.exists():
        return []

    with STORAGE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, dict):
        chain = data.get("chain", [])
        return chain if isinstance(chain, list) else []

    return data if isinstance(data, list) else []


def save_chain(chain: List[Dict[str, Any]]) -> None:
    STORAGE_PATH.write_text(json.dumps({"chain": chain}, indent=2), encoding="utf-8")


def compute_hash(record: Dict[str, Any]) -> str:
    content = {key: record.get(key) for key in ("index", "timestamp", "payload", "prev_hash")}
    serialized = json.dumps(content, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def append_entry(message: str) -> Dict[str, Any]:
    chain = load_chain()
    prev_hash = chain[-1]["hash"] if chain else None
    record: Dict[str, Any] = {
        "index": len(chain),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": {"message": message},
        "prev_hash": prev_hash,
    }
    record["hash"] = compute_hash(record)
    chain.append(record)
    save_chain(chain)
    return record


def verify_chain(chain: List[Dict[str, Any]]) -> Tuple[bool, str]:
    for idx, record in enumerate(chain):
        expected_prev = chain[idx - 1]["hash"] if idx > 0 else None
        if record.get("prev_hash") != expected_prev:
            return False, f"Chain break at index {idx}: previous hash mismatch"

        if compute_hash(record) != record.get("hash"):
            return False, f"Chain break at index {idx}: hash does not match contents"

    return True, f"Chain valid with {len(chain)} entr{'y' if len(chain) == 1 else 'ies'}"


def show_chain(chain: List[Dict[str, Any]]) -> str:
    return json.dumps(chain, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal hash chain demo (append-only log).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Append a new message to the hash chain.")
    add_parser.add_argument("message", help="Message payload to record.")

    subparsers.add_parser("verify", help="Verify the integrity of the stored chain.")
    subparsers.add_parser("show", help="Print the stored chain.")

    args = parser.parse_args()
    chain = load_chain()

    if args.command == "add":
        record = append_entry(args.message)
        print(f"Added entry {record['index']} with hash {record['hash']}")
        return

    if args.command == "verify":
        ok, message = verify_chain(chain)
        print(message)
        return

    if args.command == "show":
        print(show_chain(chain))


if __name__ == "__main__":
    main()
