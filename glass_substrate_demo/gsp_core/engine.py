from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .storage import Storage


class Engine:
    """Coordinates record creation and persistence for the demo ledger."""

    def __init__(self, storage: Storage | None = None, verifier: Verification | None = None) -> None:
        from .verification import Verification  # delayed to preserve both ledger APIs
        self.storage = storage or Storage()
        self.verifier = verifier or Verification()

    def submit(
        self,
        *,
        model_id: str,
        input_hash: str,
        output_hash: str,
        policy_id: str,
        actor: str = "system",
        notes: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new chained record and persist it."""
        state = self.storage.load()
        records: List[Dict[str, Any]] = state.get("records", [])
        prev_hash = records[-1]["record_hash"] if records else None

        record = {
            "record_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "model_id": model_id,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "policy_id": policy_id,
            "notes": notes or "",
            "metadata": metadata or {},
            "prev_hash": prev_hash,
        }

        record["record_hash"] = self.verifier.calculate_hash(record)
        self.storage.append(record)
        return record

    def list_records(self) -> List[Dict[str, Any]]:
        """Return the current set of records."""
        return self.storage.load().get("records", [])

    def integrity_status(self) -> Dict[str, Any]:
        records = self.list_records()
        status, issues = self.verifier.verify_chain(records)
        return {"ok": status, "issues": issues, "count": len(records)}

# Compatibility helpers for the original indexed, SHA-256 chained GSP event ledger.
# The Engine/Storage/Verification record_hash-format demonstration is preserved.
import hashlib
import json
from .storage import DEFAULT_DATA_PATH, load_entries, save_entries, append_entry


def compute_hash(entry: Dict[str, Any]) -> str:
    fields = ("index", "timestamp", "actor", "action", "payload", "prev_hash")
    body = {key: entry.get(key) for key in fields}
    serialized = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def ensure_genesis(path: str = str(DEFAULT_DATA_PATH)) -> List[Dict[str, Any]]:
    entries = load_entries(path)
    if entries:
        return entries
    genesis = {
        "index": 0,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "actor": "system",
        "action": "init-ledger",
        "payload": {"note": "Genesis event for GSP log"},
        "prev_hash": None,
    }
    genesis["hash"] = compute_hash(genesis)
    save_entries([genesis], path)
    return [genesis]


def record_event(actor: str, action: str, payload=None, path: str = str(DEFAULT_DATA_PATH)) -> Dict[str, Any]:
    entries = ensure_genesis(path)
    from .verification import verify_entries
    if not verify_entries(entries)["ok"]:
        raise ValueError("GSP ledger integrity check failed; refusing append")
    previous = entries[-1]
    record = {
        "index": previous["index"] + 1,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "actor": actor,
        "action": action,
        "payload": payload or {},
        "prev_hash": previous["hash"],
    }
    record["hash"] = compute_hash(record)
    append_entry(record, path)
    return record
