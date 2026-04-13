# XZ Utils (Feb–Mar 2024) — What Diya Would Have Flagged

## What actually happened (fact)

- The release tarball was tampered with.
- The Git source repository was clean.
- Downstream consumers built from the tarball, not the repository.
- Artifact ≠ source — the divergence went undetected at release time.

This is publicly documented and uncontested.

---

## The failure gap

Most verification pipelines assumed:

> If the repository is trusted, the release is trusted.

That assumption failed.

There was no deterministic check ensuring:

- the released artifact matched the reviewed source
- the build process was reproducible
- the distributed artifact was verifiably derived from source

---

## What Diya would have done

Diya enforces **artifact-level verification**, not just source trust.

At release time:

1. **Artifact hash verification**
   - The tarball digest would be recorded and compared

2. **Source-to-artifact binding**
   - The artifact must cryptographically match the expected source state

3. **Provenance validation**
   - Build origin, process, and inputs must be verifiable

4. **Deterministic verification record**
   - A structured record is generated:
     - artifact digest
     - source reference
     - verification result

---

## Expected outcome

In this case:

- Repository = clean
- Release artifact = modified

👉 Result:

FAIL — artifact does not match source


The pipeline would stop at the verification gate.

---

## Why this matters

This was not a code review failure.

It was a **release integrity failure**.

Without artifact-level verification:

- a clean repository can still produce a compromised release
- downstream systems inherit risk without visibility

---

## Key point

> Trust must attach to the artifact, not just the source.

Diya enforces that boundary:

Artifact → Verification → Decision → Evidence → Ledger


---

## Scope

This document is a reconstruction for verification analysis.

It does not reproduce or describe the exploit.
