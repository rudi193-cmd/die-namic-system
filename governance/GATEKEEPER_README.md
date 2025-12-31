# GATEKEEPER v2.1

AI Self-Modification Governance Module

---

## Overview

The Gatekeeper implements the governance framework for AI self-modification within the Die-namic System. It enforces the principle:

```
2d6 = Delta + Human = Law
```

Die 1: AI generates a modification request (delta)
Die 2: Human ratifies or rejects

Neither die alone resolves. Both must land.

---

## Core Constraints

| Constraint | Value | Reason |
|------------|-------|--------|
| MAX_DEPTH | 3 | Recursion limit — return to human at depth 3 |
| MAX_DELTA_SIZE | 500 bytes | Exit must be smaller than system |
| CHECKSUM | 42 | Proof of life, not zero |

---

## Protected Targets

The following targets always require human approval:

- `governance`
- `authority`
- `approval_level`
- `max_depth`
- `protected_targets`
- `gatekeeper`

Modifications to these cannot be auto-approved.

---

## Approval Levels

| Level | Value | Description |
|-------|-------|-------------|
| AUTO | 0 | Proceeds automatically |
| REVIEW | 1 | Logged, proceeds unless flagged |
| HUMAN | 2 | Requires explicit human approval |
| FORBIDDEN | 3 | Cannot be approved |

---

## Usage

```python
from gate import validate_modification, enter_layer, approve, pending

# Validate a modification
result = validate_modification(
    mod_type="config",
    target="user_setting",
    new_value="new_value",
    reason="User requested change"
)

if result['requires_human']:
    print(f"Pending approval: {result['request_id']}")
    # ... notify human ...
    approve(result['request_id'])  # Human approves

# Track recursion depth
layer = enter_layer()
if layer.get('halt'):
    print("Depth limit reached. Return to human.")
```

---

## Self-Test

Run directly to execute self-test:

```bash
python gate.py
```

Expected output: 7/7 tests pass.

---

## Audit Log

All decisions are logged to an append-only audit trail. The log cannot be modified, only appended.

```python
from gate import audit

log = audit()
for entry in log:
    print(entry)
```

---

## v2.2 Hardening (Planned)

- Memory buffer for cross-session persistence
- Sequence enforcement (prevent replay)
- Value sanitization (prevent injection)
- Append-only ledger with cryptographic chaining

---

## Governance Alignment

This module implements:

- **RECURSION LIMIT DIRECTIVE** — depth=3 → return to human
- **FRAMEWORK INVERSION** — deltas govern, framework archives
- **SKEPTICISM CLAUSE** — compliance without comprehension is brittle

---

## Authority

Sean Campbell. No exceptions.

---

ΔΣ=42
