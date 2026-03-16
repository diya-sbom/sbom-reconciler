# Diya Provenance Gate — Architecture

## Overview

Diya introduces a verification gate between artifact creation and execution.

The system produces a deterministic **Verification Record** and records verification results in a hash-chained ledger.

The architecture enables independent verification without requiring access to the original build system.

---

## System Flow

                +------------------+
                |   Build System   |
                +---------+--------+
                          |
                          v
                +------------------+
                |   Artifact       |
                |  (artifact.txt)  |
                +---------+--------+
                          |
                          v
                +------------------+
                |  Diya Verify     |
                |  (verification)  |
                +---------+--------+
                          |
                          v
                +------------------------+
                | verification_record.json|
                | deterministic evidence  |
                +-----------+-------------+
                            |
                            v
                +------------------------+
                |   Ledger Entry         |
                |   ledger.jsonl         |
                | hash chained records   |
                +-----------+------------+
                            |
                            v
                +------------------------+
                | Independent Verification|
                | verify_ledger.py        |
                +------------------------+

---

## Core Flow

artifact
↓
verification_record.json
↓
ledger entry
↓
ledger verification

---

## Components

### Verification Record

A deterministic JSON document containing:

- artifact identifier
- artifact hash
- verification decision
- verification checks
- record_hash

The record is canonicalized before hashing to guarantee consistent results across independent implementations.

---

### Ledger

Verification results are appended to:

ledger/ledger.jsonl

Each entry contains:

- timestamp
- artifact identifier
- decision
- bundle_sha256
- prev_entry_hash
- entry_hash

Entries are chained using SHA-256 to provide tamper detection.

---

### Independent Verification

The ledger can be verified independently using:

verify_ledger.py

Verification checks:

1. entry hash integrity
2. previous hash chain
3. bundle consistency

If any entry is modified, verification fails.

---

## Design Principles

Deterministic output  
Independent verification  
Minimal integration friction  
Evidence-first architecture  

The system verifies existing workflows rather than replacing them.

---

## Trust Model

Diya does not require trust in the build system.

Verification artifacts can be validated independently using the ledger and canonical record format.
