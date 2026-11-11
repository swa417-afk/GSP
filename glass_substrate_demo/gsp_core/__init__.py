"""
Core modules for the glass substrate demo.

This package exposes the primary runtime components:
- Engine: orchestrates record creation and persistence.
- Storage: JSON-backed persistence layer for the demo ledger.
- Verification: integrity checks for the chained records.
- Reconstruction: helpers for rebuilding timeline views.
"""

from .engine import Engine
from .storage import Storage
from .verification import Verification
from .reconstruction import Reconstruction

__all__ = ["Engine", "Storage", "Verification", "Reconstruction"]

# Original indexed-ledger API, retained alongside the newer Engine API.
from .storage import DEFAULT_DATA_PATH, load_entries, save_entries
from .engine import compute_hash, ensure_genesis, record_event
from .verification import verify_entries, verify_file
from .reconstruction import reconstruct_timeline, actor_rollups

__all__ += [
    "DEFAULT_DATA_PATH", "load_entries", "save_entries", "compute_hash",
    "ensure_genesis", "record_event", "verify_entries", "verify_file",
    "reconstruct_timeline", "actor_rollups",
]
