from typing import List, Dict, Any
from scripts.gsp_kernel import GovernanceVector, GSPOversightKernel


class AnalysisTools:
    """
    Diagnostic utilities for evaluating consistency of governance-driven
    decision outputs in a deterministic system model.

    This module focuses on observation and analysis of system state
    rather than enforcement or external action.
    """

    def __init__(self):
        self.kernel = GSPOversightKernel()

    # -----------------------------
    # Consistency Analysis
    # -----------------------------

    def consistency_analysis(self, vector: GovernanceVector, runs: int = 3) -> bool:
        """
        Evaluates whether repeated evaluations of the same input
        produce stable outputs (determinism check).
        """
        results = [self.kernel.evaluate(vector) for _ in range(runs)]
        return all(r == results[0] for r in results)

    # -----------------------------
    # Logical Divergence Identification
    # -----------------------------

    def detect_logical_divergence(self, vectors: List[GovernanceVector]) -> List[Dict[str, Any]]:
        """
        Identifies cases where system state outputs contain
        internally inconsistent or unexpected combinations.
        """
        divergences = []

        for i, v in enumerate(vectors):
            result = self.kernel.evaluate(v)

            if result.allow_execution and result.escalate:
                divergences.append({
                    "index": i,
                    "issue": "LOGICAL_DIVERGENCE_DETECTED",
                    "input_state": v.__dict__,
                    "output_state": result.__dict__,
                })

        return divergences

    # -----------------------------
    # Log Inspection
    # -----------------------------

    def log_inspection(self, ledger_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Performs structural analysis of recorded system events
        without modifying or reinterpreting their contents.
        """
        return {
            "event_count": len(ledger_events),
            "latest_event": ledger_events[-1] if ledger_events else None,
            "hash_chain_present": all("hash" in e for e in ledger_events),
        }
