# Production Deployment Verification

This is the canonical end-to-end example for Provenance Gate.

Flow:

artifact
↓
provenance verify
↓
PASS / FAIL
↓
evidence.json
↓
ledger entry
↓
ledger verification
↓
deployment allowed

Purpose:
- engineers run it
- reviewers scan it
- the workflow is understandable in under a minute

## Verification Record

This example produces a Verification Record describing the verification decision.

The record represents the public contract of the verification system.

See:

docs/verification-record.md

## Example Flow

artifact.txt
↓
provenance verify
↓
PASS / FAIL
↓
evidence bundle generated
↓
Verification Record
↓
ledger entry
↓
ledger verification
↓
deployment allowed
