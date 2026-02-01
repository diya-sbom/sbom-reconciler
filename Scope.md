# Scope

sbom-reconciler is an enforcement mechanism, not a discovery tool.

It does NOT:
- Generate SBOMs
- Scan dependencies
- Auto-fix drift
- Modify artifacts

It DOES:
- Compare declared SBOMs against reality
- Detect dependency drift
- Fail CI intentionally when drift is detected
- Require explicit reconciliation and review

This scope is intentional and enforced.
