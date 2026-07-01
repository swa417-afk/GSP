from typing import List, Dict, Any


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
