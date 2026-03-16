# Diya — 2 Minute Pipeline Insertion

Diya can be inserted into an existing build pipeline as a verification gate.

Example CI pipeline:

Build Artifact
↓
Run Tests
↓
Run Diya Verification
↓
Deploy if PASS
↓
Record Evidence

---

## Example Script

build.sh

#!/bin/bash

echo "Building artifact..."
echo "example artifact" > artifact.txt

echo "Running tests..."
echo "tests passed"

echo "Running provenance verification..."
python3 cli/diya.py verify

echo "Verifying ledger integrity..."
python3 cli/diya.py ledger-verify

echo "Pipeline completed"

---

## Output

PASS

verification_record.json created  
ledger entry appended  
ledger chain verified

---

## Evidence Produced

evidence/verification_record.json  
evidence/gate_result.json  
ledger/ledger.jsonl

These artifacts allow independent verification of the deployment decision.

---

## Design Principle

Diya does not replace existing systems.

It simply verifies the artifact and records cryptographic evidence.
