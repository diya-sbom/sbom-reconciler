# Verification Record

The Verification Record is the public contract produced by Provenance Gate.

It is the stable evidence artifact created after verification and intended
to be consumed by deployment systems, audit workflows, and other tools.

## Purpose

The Verification Record answers:

- what artifact or action was verified
- what decision was made
- what evidence was generated
- what ledger entry recorded the result

## Core Flow

artifact or action
↓
verification
↓
decision
↓
evidence record
↓
ledger entry
↓
ledger verification

## Required Properties

A valid Verification Record must be:

- deterministic
- machine-readable
- stable in meaning
- verifiable independently
- appendable to ledger history

## Minimal Fields

A Verification Record should include at least:

- `artifact`
- `decision`
- `sha256`
- `timestamp`
- `modules`
- `signature_check`
- `license_policy`

## Decision Semantics

`PASS`
The verification gate determined that the artifact or action satisfied
the required checks and policy conditions.

`FAIL`
The verification gate determined that one or more required checks or
policy conditions were not satisfied.

The meaning of PASS and FAIL is frozen.

## Evidence Relationship

The Verification Record may be represented through the generated evidence bundle,
including files such as:

- `gate_result.json`
- `metadata.json`
- `modules.json`
- `policy.json`
- `signature.json`
- `bundle.json`

## Ledger Relationship

A Verification Record becomes durable when linked to a ledger entry.

The ledger entry should include:

- artifact identifier
- decision
- bundle hash
- previous entry hash
- entry hash
- timestamp

## Public Contract

Public:
- record semantics
- field meanings
- verification result meaning
- ledger linkage model

Private:
- internal heuristics
- edge-case handling
- optimization strategies
- rollback and recovery logic
- pathological test cases
