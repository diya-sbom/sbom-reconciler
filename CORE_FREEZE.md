# Diya Core Freeze — v1.0

## Status
Core enforcement is locked.

## Definition
Diya v1.0 is an enforced provenance gate.
A failing Diya decision blocks protected progression.

## Guarantees
- Runs in CI on pull requests
- Required check on protected branch (main)
- Fail-closed behavior (failure blocks merge)
- No alternate path around the gate
- Deterministic verification outcome per run

## Non-Negotiables
- Do not weaken enforcement
- Do not change meaning of existing fields
- Do not introduce silent bypass paths
- Do not make Diya optional in protected flows

## Versioning Rule
All changes after v1.0 must be:
- Additive
- Backward-compatible

Breaking or semantic changes require a new version:
v1.1, v1.2, ...

## Allowed Evolution (v1.1+)
- Additional evidence types
- Expanded verification logic
- Policy engine integration
- Better artifact identity resolution
- Pipeline adapters
- API / SDK surfaces

## Not Allowed in v1.0
- Soft-fail modes in protected branch
- Skipping Diya via alternate workflow
- Changing pass/fail semantics
- Reinterpreting existing verification output

## Core Principle
State is the artifact.
Effective state is the complete artifact.
Everything else is metadata.
