#!/bin/bash

echo "Step 1: Verify artifact"
python3 ../../cli/provenance.py verify --artifact artifact.txt --attestation attestation.json

echo "Step 2: Export evidence"
python3 ../../cli/export_evidence.py

echo "Step 3: Write ledger entry"
python3 ../../cli/write_ledger.py ../../evidence/gate_result.json

echo "Step 4: Verify ledger"
python3 ../../cli/verify_ledger.py ../../ledger/ledger.jsonl

echo "Production deploy allowed"
