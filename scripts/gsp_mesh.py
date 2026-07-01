from dataclasses import dataclass, asdict
from typing import Dict, List, Any
from scripts.gsp_kernel import GSPOversightKernel, GovernanceVector


@dataclass
class DocumentState:
    doc_id: str
    vector: GovernanceVector
    decision: dict


class GSPGovernanceMesh:
    """
    Multi-document governance synchronization layer.
    Enables consistent policy evaluation across multiple DOCX models.
    """

    def __init__(self):
        self.kernel = GSPOversightKernel()
        self.documents: Dict[str, DocumentState] = {}

    def register_document(self, doc_id: str, vector: GovernanceVector):
        decision = self.kernel.evaluate(vector)
        self.documents[doc_id] = DocumentState(
            doc_id=doc_id,
            vector=vector,
            decision=asdict(decision),
        )

    def evaluate_all(self) -> Dict[str, Any]:
        return {doc_id: asdict(state) for doc_id, state in self.documents.items()}

    def get_policy_conflicts(self) -> List[str]:
        conflicts = []
        for doc_id, state in self.documents.items():
            if state.decision.get("allow_execution") is False and state.decision.get("require_review"):
                conflicts.append(f"{doc_id}: BLOCK+REVIEW state")
        return conflicts
