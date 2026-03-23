# Diya — Contract (Frozen)

This document defines the stable behavior of Diya.

This contract is now considered locked.

---

## Core Behavior

- Diya runs in CI as a required gate
- Failure blocks merge (fail-closed)
- Success produces:
  - verification_record.json
  - ledger append

---

## Ledger Contract

- Ledger is append-only
- Each entry must include:
  - commit_sha
  - entry_hash
  - previous_entry_hash
- Continuity must be verifiable

Any break invalidates trust.

---

## Verification Record

- Must reflect the evaluated state
- Must be reproducible
- Must match ledger entry

---

## Enforcement

- Diya Gate is required for merge
- No bypass allowed

---

## Change Rules

- No breaking changes allowed
- Any change to:
  - ledger format
  - verification_record structure
  - gate behavior

→ requires a new version boundary

---

Diya contract is now frozen.
