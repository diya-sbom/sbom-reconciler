# Provenance Gate Example

This example demonstrates the full verification pipeline.

Step 1 — Verify artifact

python engine/gate.py examples/example_artifact.txt

Step 2 — Export evidence

python cli/export_evidence.py

Step 3 — Write ledger entry

python cli/write_ledger.py evidence/gate_result.json

Step 4 — Verify ledger

python cli/verify_ledger.py ledger/ledger.jsonl

Expected result:

PIPELINE PASS
