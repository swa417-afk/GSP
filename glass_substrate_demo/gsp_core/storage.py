import json
from pathlib import Path
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
