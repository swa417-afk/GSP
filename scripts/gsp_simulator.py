from dataclasses import dataclass
from typing import List, Dict, Any
from scripts.gsp_kernel import GSPOversightKernel, GovernanceVector


class GSPSimulator:
    """
    What-if execution simulator for governance decisions.
    Allows dry-run evaluation of risk states without committing actions.
    """

    def __init__(self):
        self.kernel = GSPOversightKernel()

    def simulate(self, vectors: List[GovernanceVector]) -> List[Dict[str, Any]]:
        results = []

        for i, vector in enumerate(vectors):
            decision = self.kernel.evaluate(vector)

            results.append({
                "index": i,
                "input": vector.__dict__,
                "decision": decision.__dict__,
            })

        return results
