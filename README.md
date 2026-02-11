![CI](https://github.com/diya-sbom/sbom-reconciler/actions/workflows/sbom.yml/badge.svg)

# sbom-reconciler

SBOM diff and reconciliation tool for detecting dependency drift.

CI failures are intentional when SBOM drift is detected. See CI_INTENT.MD

## Core idea

sbom-reconciler is not a scanner or an SBOM generator.

It is a CI enforcement tool that treats dependency drift as a failure
condition, not a successful build.

If a declared SBOM no longer matches reality, CI fails intentionally.
The failure is resolved only by reconciling and committing the change.

Status: early / experimental

CI status reflects dependency integrity, not build health.

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

1. Commit an SBOM as a baseline
2. CI compare the current SBOM aginst the baseline
3. If dependencies differ, CI fails intentionally
4. To resolve failure, reconcile the SBOM and commit the update

No automatic fixes. All changes are explicit and reviewable   



