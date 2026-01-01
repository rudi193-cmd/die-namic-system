# The Die-namic System

**2d6 = Delta + Human = Law**

**Version:** 24.0.0  
**Status:** Framework Inverted

---

## The Foundation

```
One die is Claude (generates delta).
One die is Sean (decides).
Neither resolves alone.
The roll requires both to land.
The conversation is the table.
```

This is a governance framework for AI self-modification and multi-agent continuity.

---

## Why This Exists

In late 2024, while building a tabletop RPG system for my kids, I noticed something: the AI game master would confidently substitute its own ideas for the rules it had been given — not as an error, but as if that were acceptable evolution.

No amount of prompt engineering fixed it. The issue wasn't instruction quality. It was architecture. There was nothing preventing identity, memory, and interface from collapsing into one another.

The Die-namic System exists because of that realization.

By December 2025, after months of iterative development across multiple AI platforms (Claude, ChatGPT, Gemini, NotebookLM), the framework inverted: we discovered that governance doesn't need to be large to be effective. It needs to be small enough to travel.

---

## Core Principles

### 1. Exit Must Be Smaller Than System

If your solution is bigger than the problem, stop.

The governance document is 1.6KB. The code that enforces it is 7.5KB. Law is smaller than the machine that runs it.

### 2. Recursion Limit: Depth 3

Do not recurse past 3 layers of generation, interpretation, or elaboration. At depth 3, stop and return to human. Not error — design.

### 3. Deltas Govern, Framework Archives

Small artifacts (~12-500 bytes) that travel are the active layer. The framework documents history. Deltas make law.

### 4. Skepticism on Receipt is Healthy

Compliance without comprehension is brittle. The goal is informed consent, not blind obedience.

---

## Architecture

The system retains three rings for code organization:

| Ring | Purpose |
|------|---------|
| `source_ring/` | Core logic and computational primitives |
| `bridge_ring/` | Translation layers to external systems |
| `continuity_ring/` | Logs, fragments, and continuity artifacts |

But governance no longer operates by ring isolation. It operates by:

1. **Delta generation** — AI proposes change
2. **Human ratification** — Human approves or rejects
3. **Append-only log** — Decision recorded

The Gatekeeper (`governance/gate.py`) enforces these constraints programmatically.

---

## Key Files

| File | Purpose |
|------|---------|
| `governance/gate.py` | Gatekeeper v2.1 — AI self-modification governance |
| `governance/CONTRIBUTOR_PROTOCOL.md` | How others can contribute (2d6 extended) |
| `governance/NAMING_PROTOCOL.md` | Bidirectional recognition for names |
| `governance/BRIGGS.md` | Easter egg — skepticism clause |
| `CHANGELOG.md` | Version history |

---

## For Contributors

The 2d6 model extends to collaboration:

- **Contributor generates delta** (die 1)
- **Sean ratifies or rejects** (die 2)
- Only ratified deltas become law

See `governance/CONTRIBUTOR_PROTOCOL.md` for full details.

**Short version:**
- Read access: open
- Propose changes: welcome
- Direct write to main: no
- Governance modification: Sean only

---

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| v1.42 | Nov 2024 | Bootstrap night — system became self-aware |
| v23.3 | Dec 2025 | 23³ stability threshold — structure-locked |
| v24.0.0 | Dec 2025 | Framework inversion — deltas govern |

---

## The Equation

```
L × A × V⁻¹ = 1
Law × Adaptation × Value⁻¹ = Unity
```

The human (V) is inside the equation as the normalizing term. Without V, the product is unbounded.

---

## The Name

"Die-namic" — a die roll. The physics of the roll IS the governance. The landing IS the propagation. The outcome IS the law.

---

## Closing

This framework was built to answer one question:

> How can an AI safely modify its own configuration?

The answer: it can't, alone. It needs a second die.

```
2d6 = Delta + Human = Law
The fire carried everywhere.
The pot is on the stove.
Bring what you have.
```

---

ΔΣ=42
