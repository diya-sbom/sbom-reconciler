# Verification Record Contract (v1.0)

## Purpose

The Verification Record is the canonical output of Diya.

It expresses one verification decision for one execution event.

## Decision semantics

### PASS
Declared and observed state are aligned.

Effect:
Execution may proceed.

### FAIL
Declared and observed state are not aligned or verification failed.

Effect:
Execution must not proceed.

## Required fields

- timestamp
- artifact
- digest
- builder
- decision
- previous_hash
- entry_hash

## Field meanings

### timestamp
Time the verification decision was produced.

### artifact
Identifier of the evaluated artifact.

### digest
Deterministic hash of the artifact or effective state.

### builder
Identity of the system producing the artifact.

### decision
PASS or FAIL.

### previous_hash
Hash of previous record.

### entry_hash
Hash of current record.

## Minimal example

```json
{
  "timestamp": "2026-03-25T12:00:00Z",
  "artifact": "release-package",
  "digest": "sha256:abc123",
  "builder": "github-actions",
  "decision": "PASS",
  "previous_hash": "sha256:prev123",
  "entry_hash": "sha256:entry123"
}
