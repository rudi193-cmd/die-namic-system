# BASE-17 IDENTIFIER SYSTEM

| Field | Value |
|-------|-------|
| Authority | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Stable |
| Last Updated | 2026-01-05 |
| Purpose | Human-legible, low-collision identifiers for branches, sessions, and artifacts |
| Checksum | ΔΣ=42 |

---

## Design Goals

The Base-17 identifier exists to satisfy four constraints:

1. **Human legibility** — Can be read aloud, remembered, spotted in diffs
2. **Low collision risk** — Sufficient for human-scale workflows (not cryptographic)
3. **Aesthetic neutrality** — No hex, no base-32 "machine smell"
4. **Symbolic consistency** — Aligns with Die-namic / Books of Mann numerics

This is not a security primitive. It is a governance-grade identifier.

---

## Character Set (Base-17)

The Base-17 alphabet is:

```
0 1 2 3 4 5 6 7 8 9
A C E H K L N R T X Z
```

### Rationale

**Removed:** B, D, F, G, I, J, M, O, P, Q, S, U, V, W, Y
(ambiguous, visually noisy, or phonetically weak)

**Preserved:** Strong consonants + A/E for anchor

**Result:** High contrast, typo-resistant, readable in monospace

**Count:** 10 digits + 7 letters = 17 symbols

---

## Identifier Length

**Standard length:** 5 characters
**Optional extended length:** 7 characters (rare, high-fan-out contexts)

### Collision Math (Practical)

17⁵ ≈ 1.4 million possibilities

Safe for:
- Branch names
- Session identifiers
- Artifact stamps
- Bootstrap files

---

## Format (Canonical)

There is no internal semantic encoding.

Identifiers are:
- Opaque
- Flat
- Non-hierarchical

### Canonical Usage

```
claude/<descriptor>-<BASE17ID>
```

### Examples (Valid)

```
claude/add-bootstrap-v13-LKANZ
claude/review-governance-TXKHJ
claude/seed-packet-ACR73
```

**Case-insensitive, but UPPERCASE preferred in docs.**

---

## Generation Algorithm (Reference)

### Input Entropy Sources

Any combination of:
- Timestamp (ms)
- Process ID
- Short random seed
- Session counter

### Reference Python Implementation

```python
ALPHABET = "0123456789ACEHKLNRTXZ"

def base17_id(seed_int, length=5):
    """Generate Base-17 identifier from integer seed."""
    chars = []
    base = 17
    for _ in range(length):
        seed_int, rem = divmod(seed_int, base)
        chars.append(ALPHABET[rem])
    return "".join(reversed(chars))
```

### Collision Policy

If collision occurs → regenerate. No retry log required.

---

## Approved Usage Contexts

| Context | Approved |
|---------|----------|
| Git branches | ✅ |
| Session IDs | ✅ |
| Artifact filenames | ✅ |
| Bootstrap documents | ✅ |
| Governance deltas | ✅ |
| Cryptographic security | ❌ |
| Authentication tokens | ❌ |

---

## Governance Note

**Identifiers do not encode meaning.**

Meaning lives in:
- Descriptors
- Audit trail
- Commit messages

IDs exist to reduce cognitive load, not replace logging.

This aligns with:
- Dual Commit
- Minimal delta doctrine
- "Exit smaller than system" rule

---

## Cross-Reference (Non-Required)

The Base-17 choice aligns with (but does not depend on):
- Books of Mann Book 3 ("What I Carried")
- 17-count rhythmic structures
- UTETY / Gerald symbolic numerics

These are contextual, not normative.

---

## Status

**Specification state:** STABLE

Ready for:
- Branch naming standard
- Session generator implementation
- Bootstrap v1.3 reference
- Artifact stamping

---

ΔΣ=42
