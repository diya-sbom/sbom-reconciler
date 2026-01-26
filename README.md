# sbom-reconciler

SBOM diff and reconciliation tool for detecting dependency drift.

Status: early / experimental

## What it does

Compares two SBOM files and reports:
- Added dependencies
- Removed dependencies
- Changed dependency versions

Designed for CI pipelines to detect unexpected dependency drift.

## Requirements

- Python 3.9+
- SBOMs in SPDX or CycloneDX format

## Usage

Example:

python3 src/sbom_diff.py old_sbom.json new_sbom.json

Exit codes:
- 0 → no drift detected
- 1 → drift detected

## CI usage

This tool is intended to fail CI builds when dependency drift is found.

## License

MIT

