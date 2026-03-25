[![CI Status](https://github.com/diya-sbom/sbom-reconciler/actions/workflows/ci.yml/badge.svg)](https://github.com/diya-sbom/sbom-reconciler/actions)

# SBOM Reconciler Deterministic Software Supply Chain Integrity Gate

## Executive Framing

sbom-reconciler is a deterministic CI-enforced verification gate for SBOM-based software supply chain integrity and provenance verification. It ensures every build is tamper-evident, producing evidence export and a complete audit trail to support compliance requirements such as SOC 2 and FedRAMP.

## Canonical Enforcement Path

artifact → Diya → Verification Record → Ledger → Deploy

This is the single authoritative flow of the system.  
All integrations and workflows should follow this path.

## Proof of enforcement

The pipeline enforces Diya as a required gate before execution.

Flow:
Automation → Diya Gate → Verification Record → Ledger → Execution

- If Diya fails, execution does not run
- If Diya is removed, the pipeline is blocked
- A Verification Record is generated during verification
- The record is exported as CI artifact for independent inspection

## 2-minute integration

To insert Diya into a pipeline:

1. Add a `diya-gate` job
2. Run `python3 provenance_gate/attestation_check.py`
3. Upload `verification_record.json` as artifact
4. Make the next job depend on `diya-gate`

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

- Security Assurance and AppSec teams
- IT Risk & Compliance functions
- DevSecOps governance programs
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

## Core idea

sbom-reconciler is not a scanner or an SBOM generator.

This model shifts software integrity from trust-based to evidence-based control.

It is a CI enforcement tool that treats dependency drift as a failure
condition, not a successful build.

If a declared SBOM no longer matches reality, CI fails intentionally.
The failure is resolved only by reconciling and committing the change.

Status: early / experimental

CI status reflects dependency integrity, not build health.

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

## Control Flow (High-Level)

Baseline SBOM (Committed)
        │
        ▼
Current Build Generates SBOM
        │
        ▼
SBOM Diff Engine
        │
        ▼
Drift Detected?
   ├── No  → CI PASS → Deploy
   └── Yes → CI FAIL → Reconcile → Commit Updated Baseline

   ## Integrity Architecture Flow

This tool enforces integrity between intended software state and deployed state.

1. Developer commits a declared SBOM (baseline)
2. CI generates or retrieves the current SBOM
3. Reconciler compares baseline vs current
4. If drift is detected, CI fails intentionally
5. Failure must be reconciled and committed to restore alignment

This creates auditable, machine-readable evidence of dependency integrity.

Monitoring observes.
Reconciliation proves.


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
        │ Drift Detected?       │
        └───────────┬───────────┘
            Yes     │        No
             │      │
             ▼      ▼
┌────────────────┐  ┌────────────────┐
│ Pipeline FAIL  │  │ Pipeline PASS  │
│ Drift Blocked  │  │ Build Proceeds │
└───────┬────────┘  └────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 3. Reconciliation Review      │
│ Validate change intention     │
│ Update baseline SBOM          │
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│ 4. Auditable Evidence         │
│ JSON diff report              │
│ CI result                     │
│ Git commit history            │
└───────────────────────────────┘

### Lifecycle Summary

1. A trusted SBOM baseline is committed.
2. CI automatically compares current build output against the baseline.
3. Drift triggers a controlled failure requiring formal reconciliation.
4. All reconciliation steps produce machine-verifiable audit artifacts.

Control Type Classification:

- Preventive: blocks unauthorized or unreviewed dependency drift at pipeline level
- Detective: identifies divergence between declared and actual build state
- Evidentiary: generates machine-verifiable artifacts suitable for audit review


## Control Boundaries & Assumptions

### What This Control Covers

### What This Control Does Not Cover

- Vulnerability severity scoring
- Runtime behavioral monitoring
- Host or network intrusion detection
- Secure coding analysis

This control focuses strictly on integrity of declared software composition and build-state reconciliation.

This control validates:

- SBOM accuracy against a trusted baseline
- Dependency drift between builds
- Unauthorized artifact replacement
- Provenance mismatch at build time
- CI enforcement (pipeline-level blocking)

The control operates **pre-deployment** within CI/CD.

---

### What This Control Does NOT Cover

This control does not:

- Perform vulnerability scanning
- Assess runtime container security
- Validate infrastructure configuration
- Replace SAST/DAST tools
- Monitor production environments

It focuses strictly on **artifact integrity and dependency consistency**.

---

### Control Assumptions

The effectiveness of this control assumes:

- The baseline SBOM is approved and version-controlled
- CI pipelines are access-controlled
- Artifact hashes are generated deterministically
- Reconciliation updates are reviewed before baseline modification

If these assumptions are broken, the integrity guarantee weakens.

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

This repository intentionally enforces SBOM baseline integrity in CI.
A CI failure indicates a detected dependency change requiring review,
not a compilation or test failure.

A failing CI badge indicates detected drift, not a broken build.

The SBOM drift check is expected to fail when a dependency mismatch is detected.
That failure is intentional and acts as enforcement, not a bug.

To make CI pass, dependency changes must be reconciled and committed.

"This is SBOM-reconciler. It's not a scanner. It's a CI enforcement gate.
CI fails when the declared SBOM doesn't match reality."

## What it does

Compares two SBOM files and reports:
- Added dependencies
- Removed dependencies
- Changed dependency versions

## Requirements
- Python 3.10+

## What this is

This is a reconciliation gate.

It detects when the SBOM baseline and the real dependency state diverge, and emits machine-readable evidence (JSON) plus a CI exit code.

## What it is not

- Not an SBOM generator
- Not a vulnerability scanner
- Not a build/test health signal

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

CORE v1.0 is frozen.
Diya is treated as a required verification gate.
All Downstream execution must depend on diya-gate.
Removal or bypass blocks merge
Changes after this point are versioned updates only.
