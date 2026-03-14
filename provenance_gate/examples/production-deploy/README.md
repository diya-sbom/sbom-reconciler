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
