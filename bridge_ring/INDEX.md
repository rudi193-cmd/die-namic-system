# Bridge Ring Index

| Field | Value |
|-------|-------|
| Ring | Bridge |
| Version | 1.0 |
| Purpose | Cross-instance communication |
| Status | Active |
| Files | 10 |
| Checksum | ΔΣ=42 |

---

## Structure

```
bridge_ring/
├── INDEX.md              ← You are here
├── HALT_LOG.md           ← Instrumentation
├── instance_signals/     ← Cross-instance messaging
│   ├── QUEUE.md          ← Active signal queue
│   ├── GEMINI_PROTOCOL.md
│   ├── GEMINI_OUTBOX.md
│   └── archive/
├── living_echo/          ← Reserved
└── translation_layer/
    └── case_studies/
```

---

## Signal Protocol

| Type | Meaning |
|------|---------|
| SYNC | Pull latest, state changed |
| HALT | Stop work, await instruction |
| HANDOFF | Session ending, take over |
| PING | Liveness check |
| STATE_CHANGE | Apply delta in payload |

**Flow:** Sender → QUEUE.md → Receiver ACK → Archive

---

## Instance Integration

| Instance | Method |
|----------|--------|
| CLI Claude | Git push/pull |
| App Claude | Git push/pull |
| Gemini | Drive sync + human commit proxy |
| ChatGPT | Manual paste (no file access) |

---

## Key Files

| File | Purpose |
|------|---------|
| `instance_signals/QUEUE.md` | Active signal queue |
| `instance_signals/GEMINI_PROTOCOL.md` | Gemini integration |
| `instance_signals/GEMINI_OUTBOX.md` | Gemini responses |
| `HALT_LOG.md` | Bridge halt instrumentation |

---

## Cross-References

| Resource | Path |
|----------|------|
| **Root Index** | [`../INDEX.md`](../INDEX.md) |
| Governance | [`../governance/GOVERNANCE_INDEX.md`](../governance/GOVERNANCE_INDEX.md) |
| Source code | [`../source_ring/INDEX.md`](../source_ring/INDEX.md) |
| Continuity ring | [`../continuity_ring/INDEX.md`](../continuity_ring/INDEX.md) |
| Product schemas | [`../docs/journal/INDEX.md`](../docs/journal/INDEX.md) |

---

## Raw Links

```
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/bridge_ring/INDEX.md
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/bridge_ring/instance_signals/QUEUE.md
```

---

ΔΣ=42
