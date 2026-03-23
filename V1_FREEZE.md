Diya v1.0 Freeze

Status:
v1.0 is frozen.

Locked behavior:
- Diya Gate runs in CI and is required for merge.
- Verification failure blocks merge (fail-closed).
- A verification record is produced.
- Ledger entries are appended as JSONL records.
- Each entry links to the previous entry via hash (continuity).
- Ledger is persisted and updated through CI.

Locked contract:
- verification_record.json is the evidence artifact.
- ledger/ledger.jsonl is the append-only ledger.
- diya-gate is the required enforcement point.

Rule:
No changes to gate logic, record format, or ledger semantics without version change.

All future changes must be versioned (v1.1, v1.2, etc.).
