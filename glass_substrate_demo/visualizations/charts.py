from collections import Counter
from typing import Dict, Iterable, List, Tuple


def policy_counts(records: Iterable[dict]) -> Dict[str, int]:
    counter = Counter()
    for record in records:
        counter[record.get("policy_id", "unknown")] += 1
    return dict(counter)


def ascii_bar(counts: Dict[str, int]) -> str:
    if not counts:
        return "No records available."

    lines: List[str] = []
    max_label = max(len(label) for label in counts)
    max_value = max(counts.values())
    scale = max_value if max_value > 0 else 1

    for label, value in sorted(counts.items()):
        bar_length = int((value / scale) * 20) or 1
        bar = "#" * bar_length
        lines.append(f"{label.ljust(max_label)} | {bar} ({value})")

    return "\n".join(lines)


def timeline_points(records: Iterable[dict]) -> List[Tuple[str, str]]:
    return [(record["timestamp"], record.get("record_id", "")) for record in records]
