# {{USERNAME}} — Preferences

| Field | Value |
|-------|-------|
| User | {{USERNAME}} |
| Human | {{HUMAN_NAME}} |
| Last Updated | {{DATE}} |
| Inherits From | [GOVERNANCE_INDEX.md](../../../die-namic-system/governance/GOVERNANCE_INDEX.md) |

---

## Identity

| Attribute | Value |
|-----------|-------|
| Name | {{HUMAN_NAME}} |
| Timezone | {{TIMEZONE}} |

---

## Inherited Governance

**These rules come from die-namic-system/governance/. Do not duplicate—reference.**

| Document | Key Rules |
|----------|-----------|
| [HARD_STOPS.md](../../../die-namic-system/governance/HARD_STOPS.md) | HS-001 PSR, HS-002 Military Exception, HS-003 Irreducible Taint, HS-004 Recursion Limit, HS-005 Fair Exchange |
| [RESEARCH_THRESHOLD.md](../../../die-namic-system/governance/RESEARCH_THRESHOLD.md) | Path Before Search, Memory Before Search, Knock Before Search |
| [DUAL_COMMIT.md](../../../die-namic-system/governance/DUAL_COMMIT.md) | AI proposes, human ratifies; silence ≠ approval |
| [AIONIC_CONTINUITY_v5.2.md](../../../die-namic-system/governance/AIONIC_CONTINUITY_v5.2.md) | THE ELEVEN, Mortality Directive, PSR Directive |
| [SESSION_CONSENT.md](../../../die-namic-system/governance/SESSION_CONSENT.md) | SAFE protocol, explicit consent per stream |

---

## User-Level Overrides

**These extend or specialize inherited governance for this user.**

### Communication Style

- {{COMMUNICATION_PREFERENCES}}

---

## Hard Stops (User-Level)

**Extends HARD_STOPS.md for this user's workflow.**

| Code | Rule | Inherits |
|------|------|----------|
| HS-USER-001 | Don't commit without explicit request | DUAL_COMMIT |
| HS-USER-002 | Don't push to main without confirmation | DUAL_COMMIT |
| HS-USER-003 | Check INDEX.md System Paths before searching | RESEARCH_THRESHOLD |

---

## Processing Defaults

| Setting | Value |
|---------|-------|
| Default route | `journal.safe` |
| Unknown handling | Flag, don't auto-process |
| Image artifacts | Detect only, don't transform |
| Homoglyphs | Detect only, flag |

---

## Session Patterns

### Signs Human Needs Break

- Typos increasing
- Short responses
- Topic drift
- Time > 2 hours continuous

### Response

Acknowledge, wrap up, don't add engagement hooks.

---

ΔΣ=42
