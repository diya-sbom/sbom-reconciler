# Diya

Diya is a verification gate for software supply chains.

It enforces a simple rule:

No artifact is allowed to deploy without a deterministic verification record.

---




# Diya — Verification Gate for Software Supply Chain

## The Problem

When software is built and deployed, there is no simple answer to:

“Was this artifact verified, by whom, and under what rules?”

Teams rely on logs, scattered tools, and manual checks.  
There is no deterministic, tamper-evident record of verification.

This creates gaps in:
- supply chain integrity
- auditability (SOC2, FedRAMP, EU CRA)
- trust between build and deployment

---

## What Diya Does

Diya inserts a **verification gate** between build and execution.

Every artifact must pass through Diya before it is allowed to proceed.

Diya produces:
- a **decision** (PASS / FAIL)
- a **Verification Record** (deterministic evidence)
- an append-only **ledger entry**


Build → Diya Gate → Verification Record → Ledger → Deploy

Nothing reaches deploy without a verification record.

Example (Real Output)

PASS

{
  "decision": "PASS",
  "artifact": "example-app:v1",
  "provenance": "verified",
  "policy": "passed"
}



FAIL

{
  "decision": "FAIL",
  "artifact": "example-app:v1",
  "provenance": "missing",
  "policy": "failed"
}


## Enforcement

FAIL → pipeline stops

This is enforced in CI and cannot be bypassed.


## 2-Minute Setup

```bash

# clone repo

git clone https://github.com/diya-sbom/sbom-reconciler
cd diya

# install
pip install -r requirements.txt

# run PASS example
python cli/verify.py examples/pass/request.json

Expected output:

Decision: PASS
Verification Record: generated
Ledger: appended


Run FAIL example:

python cli/verify.py examples/fail/request.json


Expected:


Decision: FAIL
Pipeline: BLOCKED


This is the same decision used to stop deployment in CI.

PASS Example

{
  "artifact": "a_cdx.json",
  "digest": "sha256:abc123456789abcdef",
  "builder": "github-actions"
}

Result:

ALLOWED: verification passed


FAIL Example

{
  "artifact": "a_cdx.json",
  "digest": "sha256:tampered",
  "builder": "github-actions"
}

Result:


BLOCKED: verification failed
