# Architecture

Diya sits between build and execution.

Flow:

Artifact → Verification → Decision → Evidence → Ledger

- Verification is deterministic
- Decision is policy-driven (PASS / FAIL / EXCEPTION)
- Evidence is exportable and immutable
- Ledger is append-only

Diya does not replace CI/CD.
It verifies what already exists.

All execution paths must pass through Diya.
