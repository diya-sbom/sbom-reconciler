# Diya Verification Record Specification

Version: 1.0

## Purpose

The Verification Record defines a deterministic evidence artifact produced during artifact verification.

It enables independent verification of artifact integrity without requiring access to the original build system.

---

## Record Format

The verification record is a JSON document.

Example:

{
  "record_type": "verification_record",
  "record_version": "1.0",
  "timestamp": "ISO-8601 UTC timestamp",
  "artifact": "artifact identifier",
  "artifact_sha256": "SHA256 hash of artifact",
  "decision": "PASS | FAIL",
  "checks": {
    "artifact_hash": "PASS | FAIL",
    "policy": "PASS | FAIL",
    "signature": "PASS | FAIL"
  },
  "notes": [],
  "record_hash": "SHA256 hash of canonicalized record"
}

---

## Canonicalization Rules

Before hashing, the record must be serialized using deterministic JSON:

- UTF-8 encoding
- lexicographically sorted keys
- no insignificant whitespace
- separators: (",", ":")

The SHA-256 hash must be computed over the serialized bytes.

---

## Record Hash

The `record_hash` field contains the SHA-256 digest of the canonicalized record excluding the `record_hash` field itself.

This ensures the integrity of the verification record.

---

## Ledger Integration

Verification results may be recorded in a hash-chained ledger.

Each ledger entry contains:

- timestamp
- artifact identifier
- decision
- bundle_sha256
- prev_entry_hash
- entry_hash

The ledger enables tamper detection and independent verification.

---

## Independent Verification

Verification of records and ledger entries must not require access to the original build system.

Any compliant implementation must be able to verify:

- canonical record integrity
- ledger chain integrity
