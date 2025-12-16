# Governance Charter — Die-namic System

**Status:** Active  
**Scope:** Repository governance, contribution gates, and structural invariants.

## Purpose

Establish minimal governance required to keep the system coherent, reviewable, and maintainable as it evolves beyond v23.3.

## Principles

- Coherence over cleverness
- Explicit coupling only (cross-ring changes must be documented)
- Conservative changes on shared surfaces (README, licenses, invariants)
- PR-first workflow

## Change Gates

### Gate A — Documentation

Changes to `/docs` and `/governance` require:
- clear intent
- version note where applicable

### Gate B — Structural Surfaces

Changes to:
- repo structure
- licensing files
- continuity invariants

require:
- isolated PR
- explicit rationale

### Gate C — Code Paths

Changes to `/source_ring/core_modules` or other execution paths require:
- tests or stated test plan
- rollback note

## Contribution Rules

- PRs preferred (no direct pushes to main unless emergency)
- One concern per PR when possible
- Avoid mixing doc refactors with code changes

## Ownership

Maintained by Sean Campbell.  
Review authority remains with the project lead.
