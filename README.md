[![CI Status](https://github.com/diya-sbom/sbom-reconciler/actions/workflows/ci.yml/badge.svg)](https://github.com/diya-sbom/sbom-reconciler/actions)


# Diya — Policy-Driven Verification Gate

Diya is a verification gate that turns software execution into a verifiable record.

It answers a simple question:
**what ran, under what policy, and why was it allowed?**

---

## What Diya Does

Diya evaluates an artifact against policy and produces a decision:

- PASS  
- FAIL  
- EXCEPTION (controlled override)

Every decision produces a **verification record**.

Diya does not replace your workflow.  
It sits between steps and verifies what is already happening.

---

## Why It Matters

CI pipelines prove that a build completed.

They do not prove:

- which artifact actually ran  
- which policy was applied  
- why an exception was allowed  

Diya makes this explicit, deterministic, and verifiable.

---

## Problem

CI pipelines prove that a build completed.

They do not prove what actually ran.

During incidents, teams reconstruct execution from logs and events.
That process is slow, incomplete, and not independently verifiable.

There is no cryptographic record of:
- what artifact was executed
- what dependencies were actually present
- whether execution matched the intended state

This gap makes post-incident verification unreliable.

There is no independent proof of execution.

Modern CI pipelines prove builds.

They do not prove what actually ran.

In incidents, teams reconstruct state manually from logs.
That process is slow, incomplete, and not verifiable.

Diya introduces a verification gate.

Build → Diya Gate → Deploy

If verification fails, deployment stops.
If verification is missing, merge is blocked.

Automation
↓
Diya Gate
↓
Verification Record (proof)
↓
Ledger
↓
Deploy

- Pipelines depend on Diya
- Branch protection requires Diya
- Removal or failure blocks merge

This is not logging.
This is enforcement.

1. Add Diya workflow
2. Make deploy depend on diya-gate
3. Require diya-gate in branch protection

Diya produces a verification record:

- artifact
- digest
- builder identity
- decision (PASS / FAIL)
- hash chain linkage


# SBOM Reconciler Deterministic Software Supply Chain Integrity Gate

## Executive Framing

sbom-reconciler is a deterministic verification gate enforced in CI.

It ensures that execution matches a verified state and produces a tamper-evident verification record.

Each run generates evidence that can be exported and independently inspected.

## Core idea

Introduce a required verification gate in CI.

Build → Diya Gate → Execution

If verification fails → execution stops  
If verification is missing → merge is blocked


## Canonical Enforcement Path

artifact → Diya → Verification Record → Ledger → Deploy

This is the single authoritative flow of the system.  
All integrations and workflows should follow this path.

Automation
↓
Diya Gate
↓
Verification Record (proof)
↓
Ledger
↓
Execution

## Proof of enforcement

Diya is enforced as a required gate before execution.

- Pipelines depend on `diya-gate`
- Branch protection requires `diya-gate`
- Removal or failure blocks merge

Enforcement path:
Automation → Diya Gate → Verification Record → Ledger → Execution

Enforcement exists in both:
- CI workflow
- repository control layer


## CI semantics

CI status reflects dependency integrity, not build success.

A passing check means:
- required dependencies were verified
- verification gate executed

It does not guarantee application correctness.

## 2-minute integration

Diya can be integrated into any CI pipeline with four steps:

1. Define a `diya-gate` job
2. Execute `provenance_gate/attestation_check.py`
3. Export `verification_record.json` as a CI artifact
4. Make all downstream jobs depend on `diya-gate`

Minimal flow:
build → diya-gate → deploy

## Minimal example

```yaml


jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

  diya-gate:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - name: Run Diya verification
        run: python3 provenance_gate/attestation_check.py
      - name: Upload Verification Record
        uses: actions/upload-artifact@v4
        with:
           name: verification-record
           path: verification_record.json

  deploy:
    runs-on: ubuntu-latest
    needs: diya-gate
    steps:
      - run: echo "Deploy allowed after Diya"
  

## Core Concepts

- **bill** = intent / snapshot  
- **ledger** = immutable history

## Intended Audience

- AppSec teams
- Compliance / audit teams
- Incident response teams
- DevSecOps engineers
- Organizations operating under SOX, SOC 2, ISO 27001, or NIST-aligned controls

## Control Classification

Control Type: Preventive + Detective  
Automation Level: Fully automated in CI/CD  
Evidence Produced: Machine-readable JSON  
Failure Mode: Deterministic pipeline exit (non-zero)  
Approval Model: Explicit reconciliation required before redeployment


# sbom-reconciler

SBOM diff and reconciliation tool for detecting dependency drift.

CI failures are intentional when SBOM drift is detected. See CI_INTENT.MD

## Related design documents

- [BIL (Build Intent Ledger)](BIL.md)
- [CI Intent Model](CI_INTENT.md)
- [Scope](Scope.md)

## Control Objectives

The SBOM Reconciler enforces software supply chain integrity by:

1. Detecting dependency drift against an approved SBOM baseline.
2. Validating artifact provenance using SHA-256 digest comparison.
3. Failing CI/CD pipelines when integrity conditions are not met.
4. Requiring reconciliation and approval before deployment proceeds.
5. Generating machine-readable JSON evidence for audit purposes.

## CI Security Gate Behavior

The combined CI gate executes two independent controls:

- **SBOM Drift Check** — compares the build SBOM against the approved baseline.
- **Provenance Integrity Check** — validates artifact hash against signed provenance.

If either control fails, the pipeline exits with a non-zero status code and deployment is blocked.

Exit Codes:
- `0` → PASS
- `1` → Integrity violation detected
- `2` → Misconfiguration / incomplete input

## Control Demonstration (Local)

```bash
EXPECTED_SHA=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

# Provenance PASS
python3 src/provenance_check.py provenance_gate/examples/provenance_example.json "$EXPECTED_SHA"
echo $?   # 0 = PASS

# Provenance FAIL
python3 src/provenance_check.py provenance_gate/examples/provenance_example.json "${EXPECTED_SHA%?}b"
echo $?   # 1 = FAIL

## Control Model

This control enforces reconciliation between:

1. Intended State (Committed SBOM baseline)
2. Built State (CI-generated SBOM at build time)
3. Deployed Artifact (Optional future phase)

Control Objective:
Ensure software deployed matches the declared and approved dependency baseline.

Control Type:
- Preventive (CI blocks unauthorized drift)
- Detective (Identifies dependency changes)
- Evidentiary (Produces machine-verifiable proof)

Control Output:
- Pass / Fail
- Diff artifact
- Commit traceability


## Integrity architecture flow

Build
↓
Verification (Diya Gate)
↓
Record generation
↓
Artifact export
↓
Ledger linkage
↓
Execution

This tool enforces integrity between intended software state and deployed state.

1. Developer commits a declared SBOM (baseline)
2. CI generates or retrieves the current SBOM
3. Reconciler compares baseline vs current
4. If drift is detected, CI fails intentionally
5. Failure must be reconciled and committed to restore alignment

This creates auditable, machine-readable evidence of dependency integrity.

Monitoring observes.
Reconciliation proves.

## Control Flow

The control enforces that execution is gated by verified dependency state.

Flow:

1. Input: build artifact + declared SBOM
2. Verification: Diya compares declared vs observed state
3. Decision: PASS or FAIL (deterministic)
4. Evidence: Verification Record is generated and exported
5. Enforcement:
   - PASS → downstream execution allowed
   - FAIL → execution blocked

Control invariant:

Execution must not occur without a successful Diya verification.



## Control Classification

This tool participates in multiple control layers:

### Preventive Control
CI blocks deployment when SBOM drift is detected.
Unauthorized or undeclared dependency changes cannot proceed silently.

### Detective Control
The SBOM diff engine identifies added, removed, or modified components
between the approved baseline and the current build.

### Evidentiary Control
Machine-readable outputs (e.g., report.json and PASS/FAIL result)
serve as durable compliance artifacts, not transient CI logs.
These artifacts can be retained for audit review.

## Control Mapping (Reference Alignment)

The control behavior implemented by sbom-reconciler aligns with common
security and compliance frameworks:

### NIST SSDF (Secure Software Development Framework)
- PW.4: Review and analyze software components
- RV.1: Identify and confirm software integrity
- RV.3: Detect unauthorized changes

### SOC 2 (Trust Services Criteria)
- CC7.2: Change management controls detect unauthorized modifications
- CC6.1: Logical access prevents unauthorized system changes

### ISO 27001
- A.8.9: Configuration management
- A.12.1: Change management procedures

### EU Cyber Resilience Act (CRA)
- Software component transparency
- Integrity and traceability of dependency changes

## Assessor Questions → Expected Answers

This section anticipates how an auditor, CISO, or assessor would evaluate
the control during a review.

---

### 1. How do you ensure declared dependencies match what is actually built?

**Expected Answer:**
We commit an SBOM as a baseline artifact.  
CI compares the current SBOM against the baseline on every build.  
If differences are detected, the pipeline fails intentionally.

Evidence:
- JSON diff report (e.g., report.json)
- CI run status (PASS/FAIL)

---

### 2. What prevents unauthorized dependency changes from reaching production?

**Expected Answer:**
Any dependency drift triggers a CI failure.  
The change must be reviewed and reconciled before it can be merged.

Control Type:
Preventive (blocks merge)

---

### 3. How is drift formally acknowledged?

**Expected Answer:**
To resolve the CI failure, teams must:
1. Review the detected drift
2. Validate the change is intentional
3. Update the baseline SBOM
4. Commit the reconciliation

This creates an auditable approval trail in Git history.

Control Type:
Evidentiary (Git commit history + diff output)

---

### 4. What artifacts serve as compliance evidence?

**Expected Answer:**
- Machine-readable SBOM diff output (JSON)
- CI pass/fail result
- Git commit history for reconciliation
- Provenance gate result (if enabled)

These are treated as compliance evidence, not just CI logs.

---

### 5. How does this align with secure software practices?

**Expected Answer:**
The control enforces:
- Dependency transparency
- Configuration integrity
- Controlled change management
- Deterministic reconciliation

It converts software drift into a measurable, enforceable control event.

## Control Lifecycle – SBOM Integrity Gate

The control operates across four structured phases:

┌───────────────────────┐
        │ 1. Baseline Defined   │
        │ Commit approved SBOM  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ 2. CI Comparison      │
        │ SBOM vs Baseline      │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │ State Mismatch Detected?       │
        └───────────┬───────────┘
            Yes     │        No
             │      │
             ▼      ▼
┌────────────────┐  ┌────────────────┐
│ FAIL  │  │           PASS  │
│ Execution Blocked  │  Execution Allowed │
└───────┬────────┘  └────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 3. Reconciliation (Controlled Update)    │
│ Validate change intent    │
│ Update declared baseline (SBOM)          │
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│ 4.Evidence (Machine- Verifiable)       │
│ Verification Record(JSON)
  SBOM diff report              │
│ CI decisions (PASS /FAIL)                    │
│ Git commit history (baseline changes)         │
└───────────────────────────────┘

### Lifecycle Summary

1. A declared SBOM baseline is committed.
2. CI compares observed state against the declared baseline.
3. Any State mismatch triggers a deterministic failure.
4. Reconciliation requires an explicit, reviewd baseline update.
5. Each step produces machine-verifiable evidence artifacts.

Control Type Classification:

- Preventive: blocks unauthorized or unreviewed dependency drift at pipeline level
- Detective: identifies divergence between declared and actual build state
- Evidentiary: generates machine-verifiable artifacts suitable for audit review


## Control Boundaries & Assumptions

### What This Control Covers

This control enforces integrity of declared software composition at build time.

It validates:

- Alignment between declared SBOM and observed build state  
- Dependency drift between builds  
- Unauthorized artifact or dependency substitution  
- Provenance mismatch during CI execution  
- Enforcement of verification as a required pipeline gate  

The control operates **pre-deployment** within CI/CD and determines whether execution is permitted.

---

### What This Control Does NOT Cover

- runtime behavior after deployment
- application correctness
- baseline logic validation
- Vulnerability severity scoring
- Runtime behavioral monitoring
- Host or network intrusion detection
- Secure coding analysis
- Static or dynamc code analysis
---

### Control Assumptions

The effectiveness of this control assumes:

- The baseline SBOM is approved and version-controlled
- CI pipelines are access-controlled and protected
- Artifact generation is deterministic and reproducible
- Verification runs are not bypassed or skipped
- Reconciliation updates are reviewed before baseline modification

If these assumptions are not met, the integrity guarantee reduced.

---

### Control Classification

Type: Preventive + Detective + Evidentiary  
Execution Layer: CI/CD  
Evidence Produced: Machine-readable JSON evidence export + commit history (tamper-evidence ledger)
Control Mechanism: provenance gate enforcing SBOM verification and supply chain integrity 
Audit Alignment: SOC 2 CC6 / ISO 27001 A.8 / EU CRA integrity requirements

   
## CI behavior
See [CI_INTENT.md](./CI_INTENT.md) for the formal CI intent statement.

### Auditor / Reviewer Note

This repository enforces SBOM baseline integrity as a CI control.

A CI failure indicates a detected state mismatch between declared and observed software state.
It does not indicate a compilation or test failure.

A failing CI status reflects control enforcement, not build instability.

The control is expected to fail when state mismatch is detected.
This failure is deterministic and intentional.

To achieve a PASS decision, all dependency changes must be explicitly reconciled and committed to the declared baseline.

This system functions as an enforcement gate, not a scanning tool.
Execution is permitted only when declared and observed states are aligned.

## What it does

Enforces alignment between intended and actual software state in CI.

Compares declared SBOM baseline with build-time state and produces a deterministic PASS/FAIL decision.

- PASS → execution allowed  
- FAIL → execution blocked  

Outputs machine-verifiable evidence of alignment or drift.

Transforms dependency changes into an enforceable, auditable control event.


## Requirements
- Python 3.10+

## What this is

- a verification gate
- an enforcement control
- a source of execution proof

## What it is not

- a CI logger
- a build tool
- a vulnerability scanner

## Quick start

 HEAD
Run provenance gate (example):

python3 src/provenance_check.py provenance_gate/examples/provenance_example.json aaaaaaaa

Evidence outputs:
- SBOM diff writes a machine-readable JSON report (e.g., report.json) and returns an exit code.
- Provenance gate prints a JSON result (PASS/FAIL) and returns an exit code.

Treat these outputs as compliance evidence, not as a CI log

## SBOM diff (baseline vs new)

 3d1e993 (docs: update README)

Run a diff:

python3 src/sbom_diff.py a_cdx.json b_cdx.json

## Usage (CI enforcement model)

This model enforces SBOM integrity at merge time.

1. Commit an SBOM as a baseline
2. CI compare the current SBOM aginst the baseline
3. If dependencies differ, CI fails intentionally
4. To resolve failure, reconcile the SBOM and commit the update

No automatic fixes. All changes are explicit and reviewable   

## core Freeze (v1.0)

Core v1.0 is frozen.

Diya is defined as a required verification gate in CI.

- All execution paths must pass through `diya-gate`
- Downstream jobs must depend on `diya-gate`
- Removal or bypass of the gate results in pipeline failure
- CI status reflects control enforcement, not build success

## Core Freeze (v1.0)

Core v1.0 is frozen.

Diya is defined as a required verification gate in CI.

- All execution paths must pass through `diya-gate`
- Downstream jobs must depend on `diya-gate`
- Removal or bypass of the gate results in pipeline failure
- CI status reflects control enforcement, not build success

Changes after this point are versioned updates only (v1.1+).

## License

Business Source License 1.1 (BSL 1.1).
See LICENSE for full terms.
