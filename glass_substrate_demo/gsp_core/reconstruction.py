from collections import Counter
from typing import Any, Dict, Iterable, List, Mapping

from .engine import compute_hash
from .verification import verify_entries


def reconstruct_timeline(entries: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    materialized = list(entries)
    verification = verify_entries(materialized)

    timeline: List[Dict[str, Any]] = []
    for entry in materialized:
        timeline.append(
            {
                "index": entry.get("index"),
                "actor": entry.get("actor"),
                "action": entry.get("action"),
                "timestamp": entry.get("timestamp"),
                "hash_ok": entry.get("hash") == compute_hash(entry),
            }
        )

    timeline.sort(key=lambda item: item.get("timestamp") or "")
    return {"verification": verification, "timeline": timeline}


def actor_rollups(entries: Iterable[Mapping[str, Any]]) -> Dict[str, int]:
    actors = [entry.get("actor", "unknown") for entry in entries]
    return dict(Counter(actors))
