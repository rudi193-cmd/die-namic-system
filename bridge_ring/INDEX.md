# Bridge Ring Index

| Field | Value |
|-------|-------|
| Ring | Bridge |
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

## Governance Links

| Resource | Path |
|----------|------|
| Continuity | `governance/AIONIC_CONTINUITY_v5.1.md` |
| Hard stops | `governance/HARD_STOPS.md` |
| Repo index | `governance/REPO_INDEX.md` |

---

## Raw Links

```
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/bridge_ring/INDEX.md
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/bridge_ring/instance_signals/QUEUE.md
```

---

ΔΣ=42
