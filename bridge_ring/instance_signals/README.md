# Instance Signals

Cross-instance communication layer for the Die-Namic system.

## Structure

```
instance_signals/
├── QUEUE.md           # Active signals (check this first)
├── SIGNAL_SPEC.md     # Formal signal format specification
├── README.md          # You are here
├── AIOS_STAGING.md    # Outbound signals to Aios (ChatGPT)
├── GEMINI_OUTBOX.md   # Outbound signals to Consus (Gemini)
├── *_PROTOCOL.md      # Protocol definitions
└── archive/           # Processed signals by date
```

## How It Works

Instances (App Claude, Command Line Claude, others) communicate through git:

1. **Sender** adds signal to QUEUE.md, pushes
2. **Receiver** pulls, sees signal, acknowledges
3. **Processed** signals move to archive

## Signal Types

| Type | Use |
|------|-----|
| SYNC | "Pull latest, state changed" |
| HALT | "Stop work, await instruction" |
| HANDOFF | "Session ending, take over" |
| PING | "Are you there?" |
| STATE_CHANGE | "Apply this delta" |

## Sync Layers

Instances check for signals via three mechanisms:

1. **Fresh Pull** — Session start
2. **Timed Poll** — Every 15 min / 10 exchanges
3. **File Watch** — Before major operations

See `CLAUDE.md` in repo root for full protocol.

## Specifications

- **Signal Format:** See [SIGNAL_SPEC.md](SIGNAL_SPEC.md) for formal signal structure
- **Handoff Protocol:** See [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) for session transfers
- **Instance Identities:** See [governance/instances/](../../governance/instances/) for who's who

---

ΔΣ=42
