# Examples

This directory contains end-to-end examples for Provenance Gate.

These examples demonstrate how artifact verification, evidence generation,
and ledger recording work in practice.

Structure:

pass/
  A successful verification flow.
  The artifact and attestation match and the pipeline returns PASS.

fail/
  A failed verification flow.
  The artifact or attestation is invalid or mismatched and the pipeline returns FAIL.

Each example contains:

artifact.txt
  Example build artifact being verified.

attestation.json
  Metadata describing the artifact origin.

expected_output.json
  Expected verification result from the pipeline.

These examples allow developers to quickly understand the full workflow:

artifact
↓
verification gate
↓
evidence bundle
↓
ledger entry
↓
ledger verification
