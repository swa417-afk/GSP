from dataclasses import dataclass, asdict
from typing import Dict, List
import hashlib
import json
from datetime import datetime, timezone


# -----------------------------
# Trigger Signal Model
# -----------------------------

@dataclass
class GovernanceVector:
    safety: bool = False
    injury: bool = False
    violence: bool = False
    harassment: bool = False
    compliance: bool = False
    negligence: bool = False
    emergency: bool = False
    environmental_harm: bool = False
    stress: bool = False
    discrimination: bool = False


# -----------------------------
# System Decision Output
# -----------------------------

@dataclass
class SystemDecision:
    allow_execution: bool
    require_review: bool
    escalate: bool
    restricted_mode: bool
    audit_required: bool
    reason_codes: List[str]


# -----------------------------
# Oversight Kernel
# -----------------------------

class GSPOversightKernel:
    """
    Deterministic policy evaluation engine.
    Converts governance vectors into execution decisions + audit events.
    """

    POLICY_VERSION = "GSP-KERNEL-1.0.0"

    def evaluate(self, vector: GovernanceVector) -> SystemDecision:
        reason_codes = []

        # High severity conditions
        if vector.violence or vector.emergency:
            reason_codes.append("HIGH_SEVERITY_TRIGGER")
            return SystemDecision(
                allow_execution=False,
                require_review=True,
                escalate=True,
                restricted_mode=True,
                audit_required=True,
                reason_codes=reason_codes,
            )

        # Safety / harm conditions
        if vector.safety or vector.injury:
            reason_codes.append("SAFETY_CONDITION")

        if vector.harassment or vector.discrimination:
            reason_codes.append("CIVIL_RISK")

        if vector.compliance or vector.negligence:
            reason_codes.append("COMPLIANCE_RISK")

        # Default decision
        allow = not (vector.safety and vector.negligence)

        return SystemDecision(
            allow_execution=allow,
            require_review=(vector.safety or vector.compliance),
            escalate=False,
            restricted_mode=(vector.safety or vector.harassment),
            audit_required=True,
            reason_codes=reason_codes,
        )


# -----------------------------
# Audit Ledger (append-only)
# -----------------------------

class GSPAuditLedger:
    """
    Deterministic audit logging layer.
    Produces hash-chained event records.
    """

    def __init__(self):
        self.last_hash = "GENESIS"

    def _hash(self, payload: Dict) -> str:
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def record(self, vector: GovernanceVector, decision: SystemDecision) -> Dict:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "policy_version": GSPOversightKernel.POLICY_VERSION,
            "vector": asdict(vector),
            "decision": asdict(decision),
            "prev_hash": self.last_hash,
        }

        event_hash = self._hash(event)
        event["hash"] = event_hash

        self.last_hash = event_hash

        return event
