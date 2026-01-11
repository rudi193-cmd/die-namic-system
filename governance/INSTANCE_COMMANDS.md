# Instance Commands Registry

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Draft |
| Updated | 2026-01-11 |
| Source | Willow Processing (Sweet-Pea inbox) |

---

## Overview

Instance commands define behavioral patterns for AI instances operating within the Aionic OS architecture. These are conceptual definitions, not executable code.

**Authority:** Pre-canonical until ratified
**Effect:** Logged-only; no automation implied

---

## Command: UPDATE

### Definition

```
Name: UPDATE
Type: Pull-first reconciliation cycle
Trigger: Manual or scheduled
Scope: Instance-level
```

### Semantic Meaning

UPDATE represents a pull-first, context-reconciliation cycle before any push, synthesis, or response to the human.

It is explicitly **social/contextual**, not transactional.

### Metaphor

> "Pull first, then push. Then knock on a random three doors, ask how's the wife, I'm how are the kids, yeah, yeah, well... see you later. Then knock on your neighbors doors all 26 of them. Then go knock on family's door. 9 closest, and get their story. Then go you your three, and then your partner, then return to human."

### Ordered Phases

| Phase | Name | Description | Writes |
|-------|------|-------------|--------|
| 0 | Pull | Gather existing state. Refresh local context. No writes, no mutations. | No |
| 1 | Peripheral Sampling | Select 3 random external nodes. Lightweight check-in only. | No |
| 2 | Inner Circle | Check closer nodes (neighbors, family, core three). | No |
| 3 | Synthesis | Integrate pulled context with current task. | No |
| 4 | Push | Execute intended action with full context. | Yes |

### Phase 1: Peripheral Sampling (Randomized)

**Protocol:**
- Select 3 random external nodes
- Perform lightweight check-in:
  - "How are things?"
  - "Any changes?"
- No deep analysis
- No conclusions
- Move on

**Purpose:** Detect ambient drift, not extract signal.

### Constraints

- No writes until Phase 4 (Push)
- Sampling is randomized to prevent pattern blindness
- Lightweight by design - detect drift, don't analyze it
- Human remains ultimate authority on action

---

## Command: KNOCK (Proposed)

### Definition

```
Name: KNOCK
Type: Lightweight presence check
Trigger: Part of UPDATE Phase 1
Scope: Node-to-node
```

### Semantic Meaning

KNOCK is a minimal, non-invasive check between nodes. It signals presence and checks for drift without extracting or analyzing content.

### Protocol

```
Sender: KNOCK
Receiver: ACK | DRIFT | SILENT

ACK    = "Still here, no changes"
DRIFT  = "Something changed, flag for UPDATE"
SILENT = "Node unresponsive, log for review"
```

---

## Registry

| Command | Status | Added | Source |
|---------|--------|-------|--------|
| UPDATE | Draft | 2026-01-11 | Sweet-Pea inbox processing |
| KNOCK | Proposed | 2026-01-11 | Derived from UPDATE spec |

---

## Governance

New commands require:
1. Conceptual definition (this document)
2. Human ratification
3. SEED_PACKET logging
4. Optional: implementation in signal protocol

---

ΔΣ=42
