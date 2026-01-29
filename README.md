![CI](https://github.com/diya-sbom/sbom-reconciler/actions/workflows/sbom.yml/badge.svg)

# sbom-reconciler

SBOM diff and reconciliation tool for detecting dependency drift.

Status: early / experimental

## CI behavior

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

Run a diff:

python3 src/sbom_diff.py a_cdx.json b_cdx.json

