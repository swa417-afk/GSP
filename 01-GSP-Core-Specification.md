# GSP Core Specification (Normative)

## Scope
This document defines mandatory requirements for immutable auditability, cryptographic
attestation, and reconstruction capability in AI systems.

## Normative Requirements
- Systems MUST generate cryptographically verifiable attestations for all governed actions.
- Attestations MUST be stored in write‑once‑read‑many (WORM) storage.
- Attestations MUST form an unbroken hash chain.
- Loss or modification of attestations invalidates compliance.
