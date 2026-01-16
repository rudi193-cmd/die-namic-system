# Governance Deltas

Ratified governance rules for the Die-Namic system.

**Authority:** Sean Campbell
**System:** Aionic / Die-Namic
**Checksum:** ΔΣ=42

---

## ΔG-1: Authority Boundary Lock

**Status:** RATIFIED
**Ratified:** 2026-01-15
**Source:** Aios proposal

### Rule Text (authoritative)

> Any action that mutates governed state **MUST declare authority**.
>
> Allowed authorities: `human`, `ai`, `system`
>
> **AI is advisory-only.** AI-originated actions may enter `proposed` state but **MUST NOT** transition an artifact to `ratified`, `active`, or `deprecated`.

### Required Fields

```
authority: human | ai | system
```

### Enforcement Rules

1. If `authority = ai`:
   - Allowed state: `proposed`
   - Forbidden states: `ratified`, `active`, `deprecated`

2. If `authority = human` or `system`:
   - All state transitions allowed (subject to ΔG-4)

3. Missing `authority` → **hard fail**

### Validation Hook

```python
def validate_authority(action):
    assert action.authority in {"human", "ai", "system"}

    if action.authority == "ai":
        assert action.target_state == "proposed"
```

### Failure Mode

- Error code: `ERR_AUTHORITY_VIOLATION`
- Message: `AI-originated action attempted restricted state transition`

---

## ΔG-4: Governance State Machine

**Status:** RATIFIED
**Ratified:** 2026-01-15
**Source:** Aios proposal

### Canonical States (closed set)

```
proposed → ratified → active → deprecated
```

No other states are valid.

### Rule Text (authoritative)

> All governed artifacts **MUST exist in exactly one governance state**.
>
> State transitions **MUST be linear** and **MUST NOT skip states**.

### Allowed Transitions

| From | To | Authority Required |
|------|----|--------------------|
| proposed | ratified | human / system |
| ratified | active | human / system |
| active | deprecated | human / system |

### Forbidden Transitions

- proposed → active ❌
- proposed → deprecated ❌
- ratified → deprecated ❌
- deprecated → any ❌

### Required Field

```
governance_state: proposed | ratified | active | deprecated
```

### Validation Hook

```python
ALLOWED_TRANSITIONS = {
    "proposed":   ["ratified"],
    "ratified":   ["active"],
    "active":     ["deprecated"],
    "deprecated": []
}

def validate_state_transition(prev_state, next_state):
    assert next_state in ALLOWED_TRANSITIONS[prev_state]
```

### Failure Mode

- Error code: `ERR_STATE_TRANSITION`
- Message: `Invalid governance state transition`

---

## Combined Enforcement Order

When both rules apply, validate in this order:

1. **Authority Boundary Lock (ΔG-1)** — first
2. **Governance State Machine (ΔG-4)** — second

This ensures:
- Authority violations are caught **before** lifecycle violations
- AI actions fail early and clearly

---

## Compliance Examples

### Valid Human Action

```yaml
artifact_id: AWA-8HN2E
authority: human
governance_state: ratified
timestamp: 2026-01-15T23:18Z
```

### Valid AI Proposal

```yaml
artifact_id: AWA-9KX7Q
authority: ai
governance_state: proposed
timestamp: 2026-01-15T23:19Z
```

### Invalid AI Action (would fail ΔG-1)

```yaml
artifact_id: AWA-FAIL1
authority: ai
governance_state: ratified  # ❌ AI cannot ratify
```

### Invalid Skip (would fail ΔG-4)

```yaml
artifact_id: AWA-FAIL2
authority: human
governance_state: active  # ❌ Cannot skip from proposed
prev_state: proposed
```

---

## Pending Deltas

| Delta | Name | Status |
|-------|------|--------|
| ΔG-2 | Provenance Stamp | PROPOSED |
| ΔG-3 | Reversibility Guarantee | PROPOSED |
| ΔG-5 | Quiet Hours Guard | PROPOSED |

---

ΔΣ=42
