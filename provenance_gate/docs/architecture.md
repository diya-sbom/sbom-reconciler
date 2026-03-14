# Architecture Overview

Provenance Gate is a verification layer inserted between automation and execution.

Core flow:

artifact / action
↓
verification gate
↓
policy decision
↓
execution allowed or blocked
↓
evidence generation
↓
ledger history

## Canonical deployment flow

build artifact
↓
provenance verify
↓
PASS / FAIL
↓
evidence.json
↓
ledger entry
↓
ledger verification
↓
deployment allowed

## Design rule

Verify workflows.
Do not replace workflows.

## Core properties

- frozen engine semantics
- low-friction insertion
- deterministic verification
- evidence generation
- ledger verification

## Boundary

Public:
- verification contract
- architecture
- canonical example
- schemas

Private:
- internal heuristics
- edge-case handling
- optimization logic
- rollback and recovery strategies
- pathological tests
