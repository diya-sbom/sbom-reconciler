![CI](https://github.com/diya-sbom/sbom-reconciler/actions/workflows/sbom.yml/badge.svg)

# sbom-reconciler

SBOM diff and reconciliation tool for detecting dependency drift.

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

## What it does

Compares two SBOM files and reports:
- Added dependencies
- Removed dependencies
- Changed dependency versions

## Requirements

- Python 3.10+

## Quick start

Run provenance gate (example):

python3 src/provenance_check.py provenance_gate/examples/provenance_example.json aaaaaaaa

Evidence outputs:
- SBOM diff writes a machine-readable JSON report (e.g., report.json) and returns an exit code.
- Provenance gate prints a JSON result (PASS/FAIL) and returns an exit code.

Treat these outputs as compliance evidence, not as a CI log.

Run a diff:

python3 src/sbom_diff.py a_cdx.json b_cdx.json

