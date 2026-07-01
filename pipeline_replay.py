from dataclasses import dataclass
from typing import Any, Dict, List, Callable

from pipeline_serialization import ExecutionTrace


# -----------------------------
# Replay Result Model
# -----------------------------


@dataclass
class ReplayResult:
    """
    Represents the outcome of re-executing a serialized pipeline trace.
    """
    success: bool
    divergence: Dict[str, Any]


# -----------------------------
# Replay Engine
# -----------------------------


class ReplayEngine:
    """
    Re-executes a recorded ExecutionTrace using a provided
    step registry and compares results for reproducibility.
    """

    def __init__(self, step_registry: Dict[str, Callable[[Any], Any]]):
        self.step_registry = step_registry

    def replay(self, trace: ExecutionTrace) -> ReplayResult:
        """
        Recomputes pipeline output from initial state and step sequence,
        then compares against the recorded final state.
        """
        current = trace.initial_state
        recomputed_steps: List[str] = []

        for step_name in trace.steps_applied:
            fn = self.step_registry.get(step_name)
            if fn is None:
                continue

            current = fn(current)
            recomputed_steps.append(step_name)

        success = current == trace.final_state

        divergence: Dict[str, Any] = {}

        if not success:
            divergence = {
                "expected_final_state": trace.final_state,
                "recomputed_final_state": current,
                "steps_applied": trace.steps_applied,
                "recomputed_steps": recomputed_steps,
                "reason": "state_mismatch"
            }

        return ReplayResult(
            success=success,
            divergence=divergence
        )