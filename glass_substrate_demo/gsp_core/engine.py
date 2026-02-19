from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .storage import Storage
from .verification import Verification


class Engine:
    """Coordinates record creation and persistence for the demo ledger."""

    def __init__(self, storage: Storage | None = None, verifier: Verification | None = None) -> None:
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
