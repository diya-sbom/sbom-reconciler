# Insertion Model

Provenance Gate is designed to be inserted into existing automation
without replacing existing workflows.

## Design Principle

Verify workflows.  
Do not replace workflows.

## Standard Insertion Point

automation system
↓
artifact or action produced
↓
verification gate
↓
PASS / FAIL decision
↓
execution allowed or blocked
↓
evidence bundle generated
↓
ledger entry recorded

## Typical Integrations

The verification gate can be inserted into:

• CI/CD pipelines  
• build systems  
• deployment workflows  
• cloud automation  
• AI agent execution  
• financial automation

## Minimal Integration Pattern

A system integrates with Provenance Gate by calling:

verify artifact
↓
read PASS / FAIL decision
↓
allow or block execution
↓
store evidence bundle
↓
record ledger entry

## Key Property

Insertion must be low friction.

A verification step should require only:

• a CLI call  
or  
• a simple API request

## Outcome

The result is a verifiable record of automation decisions.

automation  
↓  
verification  
↓  
execution  
↓  
proof
