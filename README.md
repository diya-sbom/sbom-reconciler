# sbom-reconciler

SBOM diff and reconciliation tool for detecting dependency drift.

## What it does
Compares two SBOM JSON files and outputs:
- **added** packages
- **removed** packages
- **changed** packages (version drift)

Supports:
- **CycloneDX JSON** (`components`)
- **SPDX JSON** (`packages`)

## Quick start

### 1) Run a diff
```bash
python3 src/sbom_diff.py a_cdx.json b_cdx.json

