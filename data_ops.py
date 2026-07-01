from typing import List, Dict, Any


# -----------------------------
# Data Operations (Extended Module)
# -----------------------------


def compare_items(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        return {"result": True, "reason": "empty"}

    first = items[0]
    return {
        "result": all(i == first for i in items),
        "count": len(items)
    }


def filter_pairs(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []

    for idx, r in enumerate(records):
        if r.get("a") is True and r.get("b") is True:
            output.append({
                "index": idx,
                "record": r,
                "tag": "pair"
            })

    return output


def summarize(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "count": len(events),
        "last": events[-1] if events else None,
        "is_structured": all(isinstance(e, dict) for e in events)
    }


# -----------------------------
# Extension Utilities
# -----------------------------


def group_by_key(items: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    Groups a list of dictionaries by a given key.
    """
    grouped: Dict[Any, List[Dict[str, Any]]] = {}

    for item in items:
        k = item.get(key)
        if k not in grouped:
            grouped[k] = []
        grouped[k].append(item)

    return grouped
