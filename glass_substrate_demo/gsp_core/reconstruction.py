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
