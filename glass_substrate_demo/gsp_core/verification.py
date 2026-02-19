import hashlib
import json
from typing import Any, Dict, List, Tuple


class Verification:
    """Integrity checks for the chained ledger records."""

    @staticmethod
    def calculate_hash(record: Dict[str, Any]) -> str:
        """Deterministically hash a record (excluding its own hash field)."""
        base = {k: v for k, v in record.items() if k != "record_hash"}
        serialized = json.dumps(base, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def verify_chain(self, records: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        issues: List[str] = []
        previous_hash: str | None = None

        for record in records:
            if record.get("prev_hash") != previous_hash:
                issues.append(
                    f"Record {record.get('record_id')} has prev_hash "
                    f"{record.get('prev_hash')} but expected {previous_hash}"
                )

            recalculated = self.calculate_hash(record)
            if record.get("record_hash") != recalculated:
                issues.append(f"Record {record.get('record_id')} hash mismatch")

            previous_hash = record.get("record_hash")

        return len(issues) == 0, issues

    def chain_tip(self, records: List[Dict[str, Any]]) -> str | None:
        """Return the latest hash, if any."""
        if not records:
            return None
        return records[-1].get("record_hash")
