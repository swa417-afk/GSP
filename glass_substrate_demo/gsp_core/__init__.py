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
