# Provenance Gate

Provenance Gate is a verification infrastructure layer for software supply chains.

The system verifies artifacts produced by existing workflows and records cryptographic evidence in an append-only ledger.

The design principle is simple:

Build → Verification Gate → Evidence → Ledger

The system does **not replace existing pipelines**.  
It verifies them.

Engine Semantics

Version: v1.0-engine

Engine semantics frozen.
Future changes are additive only through modules and policies.
---

## Verification Record

The core output of the system is a **Verification Record**.

A Verification Record captures:

- artifact identity
- artifact hash
- verification checks
- policy decision
- timestamp

Example:

examples/verification_record_example.json

The Verification Record is designed to be tool-agnostic and stable.  
Policies, pipelines, and auditors can reference the record format without depending on the CLI implementation.
---

## Architecture

Build Artifact
↓
Verification Gate
↓
Evidence Bundle
↓
Ledger Entry
↓
Ledger Verification
---

## Components

engine/ core verification logic
cli/ command-line interface
policies/ policy rules (licenses, vulnerabilities, signers)
schema/ data schemas
tests/ automated tests
examples/ example artifacts and attestations


---

## Quick Start

Run the full verification pipeline:

```bash
python3 run_pipeline.py

---
This performs:
1.Artifact verification

2.Evidence generation

3.Evidence bundle creation

4.Ledger append

5.edger integrity verification


CLI Commands

Example commands:

python3 cli/export_evidence.py
python3 cli/write_ledger.py evidence/gate_result.json
python3 cli/verify_ledger.py ledger/ledger.jsonl

Security

If you discover a security vulnerability, please report it privately.

Security contact:

security@diyalabs.example

See SECURITY.md for details.

License

This project is licensed under the Business Source License 1.1 (BSL).

Commercial production use requires a separate commercial license.

Change Date: 2029-01-01
Change License: Apache License 2.0

See the LICENSE file for full terms.

Project Status

Early development prototype.

Current features:

artifact verification

evidence bundle creation

append-only ledger

ledger verification

CLI interface

Future features:

policy enforcement

approval workflows

CI/CD integrations

API layer


---

### 3️⃣ Save

Press:


Ctrl + O
Enter
Ctrl + X


---

### Your repository now contains the core professional files:


LICENSE
NOTICE
SECURITY.md
README.md


This is now **structured like a real infrastructure project**.

---

### Next step (important)

The next strong improvement will be adding a **single command interface**, like:


provenance verify artifact.txt
provenance ledger verify
provenance evidence export


That turns the project from scripts into a **real CLI product**.
