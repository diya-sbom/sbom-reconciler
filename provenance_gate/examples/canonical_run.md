# Canonical Example — Diya Provenance Gate

This example demonstrates the full verification flow.

## Step 1 — Create artifact

echo "example artifact" > artifact.txt

## Step 2 — Run verification

python3 cli/diya.py verify

Output:

{
  "result": "PASS",
  "record_file": "evidence/verification_record.json"
}

## Step 3 — Verification Record

cat evidence/verification_record.json

Example:

{
  "record_type": "verification_record",
  "record_version": "1.0",
  "timestamp": "...",
  "artifact": "artifact.txt",
  "artifact_sha256": "...",
  "decision": "PASS",
  "checks": {
    "artifact_hash": "PASS",
    "policy": "PASS",
    "signature": "PASS"
  },
  "notes": [],
  "record_hash": "..."
}

## Step 4 — Ledger Entry

Verification results are written to:

ledger/ledger.jsonl

Each entry includes:

- bundle_sha256
- prev_entry_hash
- entry_hash

## Step 5 — Verify ledger

python3 cli/diya.py ledger-verify

Output:

{
  "result": "PASS",
  "entries_verified": N
}

## Result

Artifact verification produced a deterministic record and a verifiable ledger entry.

Independent verification does not require access to the original build system.
