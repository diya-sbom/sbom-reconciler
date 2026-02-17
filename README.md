![CI](https://github.com/diya-sbom/sbom-reconciler/actions/workflows/sbom.yml/badge.svg)

## Executive Framing

sbom-reconciler is a CI-enforced integrity control designed for environments where software composition must be provable, not assumed.

It treats dependency drift as a governance event rather than a build inconvenience.

The objective is not detection alone — it is controlled reconciliation with audit traceability.

## Intended Audience

- Security Assurance teams
- IT Risk & Compliance functions
- DevSecOps governance programs
- Organizations operating under SOX, SOC 2, ISO 27001, or NIST-aligned frameworks


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

The SBOM Reconciler enforces dependency integrity by ensuring:

1. Approved SBOM baselines define the expected software composition.
2. Any deviation from the baseline is automatically detected.
3. Drift results in intentional CI failure.
4. Deployment proceeds only after reconciliation and approval.
5. Dependency changes are machine-verifiable and audit-evidenced.

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
Evidence Produced: Machine-readable JSON + commit history  
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



