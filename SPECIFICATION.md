# Specification

## Verification Request

Inputs:
- artifact
- digest
- builder
- justification (optional)
- approver (required for exception)

## Decision

Outputs:
- PASS
- FAIL
- EXCEPTION

## Rules

- Missing required fields → FAIL
- Override without justification → FAIL
- Exception requires:
  - justification
  - approver identity

## Output

- decision
- reason
- timestamp
- verification_record
