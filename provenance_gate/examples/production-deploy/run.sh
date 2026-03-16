#!/usr/bin/env bash

set -e

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "Step 1: Verify artifact"

PYTHONPATH=. python3 -m engine.gate \
  --artifact examples/production-deploy/artifact.txt \
  --attestation examples/production-deploy/attestation.json

echo "Step 2: Export evidence"

PYTHONPATH=. python3 cli/export_evidence.py

echo "Step 3: Write ledger entry"

PYTHONPATH=. python3 cli/write_ledger.py evidence/gate_result.json

echo "Step 4: Verify ledger"

PYTHONPATH=. python3 cli/verify_ledger.py ledger/ledger.jsonl

echo "Production deploy allowed"
