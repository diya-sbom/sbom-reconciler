Diya v1.0 Freeze

Frozen: March 31, 2026
External dependent confirmed: consumer-pipeline
Fail-closed: confirmed
Engine: locked

## Stage order (frozen)

1. Internal pipeline
2. External dependent
3. API as primary decision surface
4. GitHub Action adapter
5. First real dependent

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

## Rule

No changes to gate logic, record format, or ledger semantics without version change.

All future changes must be versioned (v1.1, v1.2, etc.).

Advance only if the next step increases dependency on Diya.

If a step does not make Diya harder to remove, do not proceed.

## Enforcement Proof (Final)

Fail-closed enforcement has been explicitly validated in CI:

- A request with an invalid builder ("unknown") produced decision = FAIL
- `diya-gate` job failed
- downstream `protected-job` did not run (skipped)
- merge was blocked due to required status checks

Pass behavior has also been validated:

- A request with valid builder ("github-actions") produced decision = PASS
- `diya-gate` job passed
- downstream `protected-job` executed
- merge was allowed

This confirms:

Diya is non-bypassable within the CI control flow.
