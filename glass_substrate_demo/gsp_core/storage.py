import json
from pathlib import Path
from typing import Any, Dict, List


class Storage:
    """Lightweight JSON storage for demo ledger records."""

    def __init__(self, path: Path | str | None = None) -> None:
        base_path = Path(path) if path else Path(__file__).resolve().parent.parent / "data" / "storage.json"
        self.path = base_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"records": []})

    def load(self) -> Dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_records(self, records: List[Dict[str, Any]]) -> None:
        payload = {"records": records}
        self._write(payload)

    def append(self, record: Dict[str, Any]) -> None:
        current = self.load()
        records: List[Dict[str, Any]] = current.get("records", [])
        records.append(record)
        self.save_records(records)

    def clear(self) -> None:
        self._write({"records": []})

    def _write(self, payload: Dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
