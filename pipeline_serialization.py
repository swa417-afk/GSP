from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Callable
import json

from data_ops import compare_items, filter_pairs, summarize, group_by_key


# -----------------------------
# Function Registry
# -----------------------------
# Maps serialized step names to callable implementations

STEP_REGISTRY: Dict[str, Callable[[Any], Any]] = {
    "compare_items": compare_items,
    "filter_pairs": filter_pairs,
    "summarize": summarize,
    "group_by_key": group_by_key,
}


# -----------------------------
# Execution Trace Model
# -----------------------------


@dataclass
class ExecutionTrace:
    """
    Captures a reproducible record of a pipeline execution.
    """
    initial_state: Any
    steps_applied: List[str]
    final_state: Any

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @staticmethod
    def from_json(payload: str) -> "ExecutionTrace":
        data = json.loads(payload)
        return ExecutionTrace(**data)


# -----------------------------
# Pipeline Serialization Layer
# -----------------------------


class PipelineSerializer:
    """
    Converts pipeline configurations into a portable JSON format
    and reconstructs executable pipelines from step identifiers.
    """

    def export(self, steps: List[str]) -> str:
        """
        Serializes a list of step identifiers into JSON.
        """
        payload = {
            "steps": steps
        }
        return json.dumps(payload, ensure_ascii=False)

    def load(self, payload: str) -> List[Callable[[Any], Any]]:
        """
        Reconstructs executable steps from a serialized pipeline.
        """
        data = json.loads(payload)
        steps = data.get("steps", [])

        return [STEP_REGISTRY[name] for name in steps if name in STEP_REGISTRY]


# -----------------------------
# Trace Builder Utility
# -----------------------------


def build_execution_trace(
    initial_state: Any,
    steps: List[str],
) -> ExecutionTrace:
    """
    Executes a sequence of registered steps and records a trace
    of inputs, applied transformations, and final output.
    """
    current = initial_state
    applied: List[str] = []

    for name in steps:
        fn = STEP_REGISTRY.get(name)
        if fn is None:
            continue

        current = fn(current)
        applied.append(name)

    return ExecutionTrace(
        initial_state=initial_state,
        steps_applied=applied,
        final_state=current,
    )