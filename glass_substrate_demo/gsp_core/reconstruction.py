from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


class Reconstruction:
    """Helpers for rebuilding substrate state from stored records."""

    @staticmethod
    def _parsed_timestamp(value: str) -> datetime:
        return datetime.fromisoformat(value)

    def timeline(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return records ordered by timestamp."""
        return sorted(records, key=lambda r: self._parsed_timestamp(r["timestamp"]))

    def latest(self, records: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        ordered = self.timeline(records)
        return ordered[-1] if ordered else None

    def group_by_policy(self, records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for record in records:
            grouped.setdefault(record.get("policy_id", "unknown"), []).append(record)
        return grouped

    def chain_depth(self, records: List[Dict[str, Any]]) -> int:
        return len(records)
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
