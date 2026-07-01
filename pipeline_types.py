from dataclasses import dataclass
from typing import Any, Dict, List, Callable, Optional

from data_ops import compare_items, filter_pairs, summarize, group_by_key


# -----------------------------
# Typed Data Models
# -----------------------------


@dataclass
class ItemPayload:
    """
    Generic item container used for pipeline processing.
    """
    data: Dict[str, Any]


@dataclass
class EventPayload:
    """
    Generic event container used for pipeline processing.
    """
    record: Dict[str, Any]


@dataclass
class PipelineResult:
    """
    Standard output wrapper for pipeline execution results.
    """
    stage: str
    output: Any
    metadata: Dict[str, Any]


# -----------------------------
# Pipeline Executor
# -----------------------------


class PipelineExecutor:
    """
    Executes a simple sequence of transformations over structured data.
    Each stage is a pure function operating on in-memory Python objects.
    """

    def __init__(self):
        self.steps: List[Callable[[Any], Any]] = []

    def add_step(self, fn: Callable[[Any], Any]) -> "PipelineExecutor":
        self.steps.append(fn)
        return self

    def run(self, input_data: Any) -> List[PipelineResult]:
        results: List[PipelineResult] = []
        current = input_data

        for i, step in enumerate(self.steps):
            output = step(current)
            results.append(
                PipelineResult(
                    stage=f"step_{i}",
                    output=output,
                    metadata={"function": step.__name__}
                )
            )
            current = output

        return results


# -----------------------------
# Prebuilt Pipeline Configurations
# -----------------------------


def build_standard_pipeline() -> PipelineExecutor:
    """
    Constructs a default pipeline using data_ops utilities.
    """
    pipeline = PipelineExecutor()

    pipeline.add_step(lambda data: compare_items(data))
    pipeline.add_step(lambda data: summarize(data if isinstance(data, list) else []))

    return pipeline


def build_grouping_pipeline(key: str) -> PipelineExecutor:
    """
    Constructs a pipeline that groups data and summarizes results.
    """
    pipeline = PipelineExecutor()

    pipeline.add_step(lambda data: group_by_key(data, key))
    pipeline.add_step(lambda data: summarize(list(data.values()) if isinstance(data, dict) else []))

    return pipeline