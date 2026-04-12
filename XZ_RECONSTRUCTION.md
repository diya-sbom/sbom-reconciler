# XZ Utils (Feb–Mar 2024) — What Diya Would Have Flagged

## What actually happened (fact)

- The release tarball was tampered with  
- The Git source repository remained clean  
- Downstream systems built from the tarball, not the repository  
- Artifact ≠ Source — the divergence went undetected at release time  

This is documented and uncontested.

---

## What Diya would have flagged

### 1. Artifact integrity mismatch
The distributed tarball does not match expected canonical artifact state.

Result: FAIL

---

### 2. Source–artifact inconsistency
The Git commit cannot deterministically reproduce the distributed tarball.

Result: FAIL

---

### 3. Provenance gap
No verifiable linkage between:
- source commit
- build process
- distributed artifact

Result: FAIL

---

### 4. Release-time enforcement
Verification occurs before downstream consumption.

Result: BLOCK

---

## Result

The compromised release would not have passed verification and would not have been consumed downstream.

---

## Observation

The failure was not in code review.  
It was in the absence of artifact-level verification.

---

## Why this matters

Diya is designed to make this class of divergence visible before downstream use.

It does not rely on repository trust alone.  
It verifies the artifact actually being consumed, records the decision, and blocks continuation on failure.
