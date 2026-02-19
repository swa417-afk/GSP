from typing import Any, Dict, List, Mapping

from .engine import compute_hash
from .storage import load_entries, DEFAULT_DATA_PATH


def verify_entries(entries: List[Mapping[str, Any]]) -> Dict[str, Any]:
    failures: List[Dict[str, Any]] = []
    for idx, entry in enumerate(entries):
        expected_prev = None if idx == 0 else entries[idx - 1].get("hash")
        if entry.get("prev_hash") != expected_prev:
            failures.append(
                {
                    "index": idx,
                    "issue": "prev_hash_mismatch",
                    "expected": expected_prev,
                    "found": entry.get("prev_hash"),
                }
            )

        expected_hash = compute_hash(entry)
        if entry.get("hash") != expected_hash:
            failures.append(
                {
                    "index": idx,
                    "issue": "hash_mismatch",
                    "expected": expected_hash,
                    "found": entry.get("hash"),
                }
            )

    return {
        "ok": not failures,
        "count": len(entries),
        "failures": failures,
        "latest_hash": entries[-1].get("hash") if entries else None,
    }


def verify_file(path: str = str(DEFAULT_DATA_PATH)) -> Dict[str, Any]:
    entries = load_entries(path)
    if not entries:
        return {"ok": False, "count": 0, "failures": [{"issue": "no_entries"}]}
    return verify_entries(entries)
