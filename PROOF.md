# Diya Proof

## Canonical PASS
`examples/pass/request.json` → `decision: PASS`

## Canonical FAIL
`examples/fail/request.json` → `decision: FAIL`

## Enforcement
- Diya Gate blocks execution on FAIL
- Protected job runs only after Diya passes
- External dependent pipeline requires Diya decision before continuing

## Result
Diya is operating as a non-bypassable verification gate with a dependent pipeline.
