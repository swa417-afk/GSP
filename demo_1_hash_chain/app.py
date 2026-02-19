import hashlib
import json
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict, List, Optional


STORAGE_FILE = os.path.join(os.path.dirname(__file__), "storage.json")


def load_storage() -> List[Dict[str, Any]]:
    if not os.path.exists(STORAGE_FILE):
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, dict) and isinstance(data.get("chain"), list):
        return data["chain"]

    return data if isinstance(data, list) else []


def save_storage(data: List[Dict[str, Any]]) -> None:
    with open(STORAGE_FILE, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def compute_hash(payload: Dict[str, Any]) -> str:
    payload_string = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload_string).hexdigest()


def create_attestation(user_id: str, action: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    if metadata is None:
        metadata = {}

    chain = load_storage()
    previous_hash = chain[-1]["hash"] if chain else None

    attestation: Dict[str, Any] = {
        "id": str(uuid4()),
        "issuer": "GSP-Demo",
        "userId": user_id,
        "action": action,
        "metadata": metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "previousHash": previous_hash,
    }

    attestation["hash"] = compute_hash(attestation)

    chain.append(attestation)
    save_storage(chain)

    print("Attestation created:")
    print(json.dumps(attestation, indent=2))


def verify_chain() -> bool:
    chain = load_storage()

    for idx, att in enumerate(chain):
        stored_hash = att.get("hash")
        payload = att.copy()
        payload.pop("hash", None)

        computed_hash = compute_hash(payload)

        if stored_hash != computed_hash:
            print(f"Tampering detected at index {idx}")
            return False

        if idx > 0:
            if att.get("previousHash") != chain[idx - 1].get("hash"):
                print(f"Broken chain link at index {idx}")
                return False

    print("Chain is valid.")
    return True


def reconstruct() -> None:
    chain = load_storage()
    print("Reconstruction:")
    for att in chain:
        print(f"{att.get('timestamp')} | {att.get('action')} | {str(att.get('hash', ''))[:10]}...")


def main() -> None:
    while True:
        print("\n1. Create Attestation")
        print("2. Verify Chain")
        print("3. Reconstruct")
        print("4. Exit")

        choice = input("Select: ")

        if choice == "1":
            user = input("User ID: ")
            action = input("Action: ")
            create_attestation(user, action)

        elif choice == "2":
            verify_chain()

        elif choice == "3":
            reconstruct()

        elif choice == "4":
            break


if __name__ == "__main__":
    main()
