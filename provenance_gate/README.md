# AI-Driven IT Creates a Verification Bottleneck

IT systems are shifting from human-driven workflows to AI-driven automation.

AI agents can now build, test, and deploy software across systems automatically.

But organizations must still answer critical questions:

What executed?
Who approved it?
What policy allowed it?
What artifact ran?
Can we prove it?

Automation accelerates execution.

Verification becomes the bottleneck.

Diya provides a verification gate that inserts evidence and provenance into automated pipelines.

---

## Quick Example

Canonical deployment verification example:

examples/production-deploy/

GitHub Actions CI example:

.github/workflows/diya-verify.yml


---

# Diya — Provenance Verification Gate

Diya is a lightweight verification gate for artifact provenance.

It verifies artifact integrity, produces a deterministic verification record, and records the result in a tamper-evident ledger.

The goal is to provide independent, reproducible evidence that an artifact passed verification before deployment.

---

## How It Works

Build
↓
Verification Gate (Diya)
↓
Verification Record
↓
Ledger Entry
↓
Independent Verification

The system does not replace build pipelines.

It sits between steps and verifies what already happened.

---

## Quick Start

Run verification:

python3 cli/diya.py verify

Verify ledger integrity:

python3 cli/diya.py ledger-verify

Canonical deployment example:

examples/production-deploy/

Canonical deployment example:
examples/production-deploy/

GitHub Actions example:
.github/workflows/diya-verify.yml

---

## Example Output

PASS

Verification record created  
Ledger entry appended  
Ledger integrity verified

---

## Evidence Artifacts

The system produces three artifacts:

verification_record.json  
gate_result.json  
ledger.jsonl

These artifacts allow independent verification of the decision.

---

## Design Principles

Evidence first  
Deterministic hashing  
Independent verification  
Append-only ledger  

The verification record is canonicalized JSON hashed using SHA-256.

---

## Documentation

ARCHITECTURE.md — system design  
SPECIFICATION.md — verification record specification  
STEWARDSHIP.md — governance and evolution rules  

---

## Goal

Provide a minimal verification layer that can be inserted into existing pipelines in minutes while producing cryptographically verifiable evidence.
