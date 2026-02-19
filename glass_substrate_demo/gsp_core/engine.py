import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping

from .storage import append_entry, load_entries, save_entries, DEFAULT_DATA_PATH


def compute_hash(entry: Mapping[str, Any]) -> str:
    content = {
        "index": entry.get("index"),
        "timestamp": entry.get("timestamp"),
        "actor": entry.get("actor"),
        "action": entry.get("action"),
        "payload": entry.get("payload", {}),
        "prev_hash": entry.get("prev_hash"),
    }
    payload = json.dumps(content, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ensure_genesis(path: str = str(DEFAULT_DATA_PATH)) -> List[Dict[str, Any]]:
    entries = load_entries(path)
    if entries:
        return entries

    genesis = {
        "index": 0,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "actor": "system",
        "action": "init-ledger",
        "payload": {"note": "Genesis event for demo log"},
        "prev_hash": None,
    }
    genesis["hash"] = compute_hash(genesis)
    save_entries([genesis], path)
    return [genesis]


def record_event(
    actor: str,
    action: str,
    payload: Mapping[str, Any] | None = None,
    path: str = str(DEFAULT_DATA_PATH),
) -> Dict[str, Any]:
    entries = ensure_genesis(path)
    last = entries[-1]
    index = int(last.get("index", len(entries) - 1)) + 1
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    event = {
        "index": index,
        "timestamp": timestamp,
        "actor": actor,
        "action": action,
        "payload": payload or {},
        "prev_hash": last.get("hash"),
    }
    event["hash"] = compute_hash(event)

    append_entry(event, path)
    return event
