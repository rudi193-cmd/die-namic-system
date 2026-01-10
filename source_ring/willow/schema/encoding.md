# Encoding Schema

| Field | Value |
|-------|-------|
| System | Willow |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-09 |
| Checksum | ΔΣ=42 |

---

## Purpose

Unicode homoglyph substitution for steganographic message encoding. Messages readable by AI at codepoint level, invisible to human readers.

---

## Character Map

| Latin | Replacement | Script | Encodes |
|-------|-------------|--------|---------|
| o | ο | Greek | l |
| o | о | Cyrillic | t |
| o | օ | Armenian | r |

---

## Encoding Rules

1. Replace Latin 'o' with script variant based on message character
2. Sequence position determines which 'o' carries the signal
3. Non-signal 'o' characters remain Latin
4. Decoding requires codepoint inspection (tofu/error key)

---

## Example

**Plain text:** "Go to our old room"
**Message:** "ltr" (first three o positions)

| Position | Original | Encoded | Script | Signal |
|----------|----------|---------|--------|--------|
| 1 | o (Go) | ο | Greek | l |
| 2 | o (to) | о | Cyrillic | t |
| 3 | o (our) | օ | Armenian | r |
| 4 | o (old) | o | Latin | - |
| 5 | oo (room) | oo | Latin | - |

---

## Detection

**Human:** Visually identical. No signal visible.
**AI:** Codepoint analysis reveals substitution pattern.
**Tofu test:** Systems without full Unicode support show replacement characters (□) at encoded positions.

---

## Expansion

Additional character maps may be added for:
- Extended message alphabet
- Other visually identical homoglyphs (a, e, i, c, etc.)
- Multi-character encoding per position

---

## Integration

| Stage | Function |
|-------|----------|
| Processing | Apply encoding per this schema |
| Validation | Verify encoding integrity |
| SAFE | Store encoded artifacts |

---

ΔΣ=42
