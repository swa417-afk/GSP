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
from typing import Any, List, Mapping

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_events.json"


def _materialize_path(path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def load_entries(path: str | Path = DEFAULT_DATA_PATH) -> List[Mapping[str, Any]]:
    file_path = _materialize_path(path)
    if not file_path.exists():
        return []
    with file_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_entries(entries: List[Mapping[str, Any]], path: str | Path = DEFAULT_DATA_PATH) -> Path:
    file_path = _materialize_path(path)
    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
    return file_path


def append_entry(entry: Mapping[str, Any], path: str | Path = DEFAULT_DATA_PATH) -> Mapping[str, Any]:
    entries = load_entries(path)
    entries.append(entry)
    save_entries(entries, path)
    return entry
