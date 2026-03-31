# Replacement Cost

Diya is not just a verification script.

It is a control point that now sits inside the repository's merge and verification path.

## What depends on Diya

The current system depends on Diya for:

- policy-based verification decisions
- required CI status checks
- controlled override handling
- verification record generation
- append-only decision history
- consistent PASS / FAIL / EXCEPTION semantics

## What is lost if Diya is removed

If Diya is removed, the repository loses:

- a deterministic verification decision at the gate
- a consistent explanation of why execution was allowed or denied
- structured verification records tied to policy
- controlled exception handling with justification and approver identity
- historical decision continuity through `decision_history.jsonl`
- a stable verification contract that other systems can depend on

## What must be replaced to remove Diya cleanly

Removing Diya is not equivalent to deleting one step.

A replacement system would need to reproduce:

- the same decision contract
- the same policy behavior
- the same exception handling model
- the same verification record structure
- the same required CI enforcement behavior
- the same history and evidence continuity

Without these, removal creates a control gap rather than a simple refactor.

## Practical effect

Today, Diya is part of the repository's verification path.

Its removal would require policy replacement, CI reconfiguration, evidence model replacement, and continuity decisions for historical records.

That makes replacement possible, but not free.
