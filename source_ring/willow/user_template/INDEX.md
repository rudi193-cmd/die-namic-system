# {{USERNAME}} — User Index

| Field | Value |
|-------|-------|
| User | {{USERNAME}} |
| Human | {{HUMAN_NAME}} |
| Status | Active |
| Created | {{DATE}} |
| Last Updated | {{DATE}} |
| Checksum | ΔΣ=42 |

---

## Quick Start

| I want to... | Go to |
|--------------|-------|
| Drop something for processing | [Inbox/](Inbox/) |
| Read my journal | [JOURNAL.md](JOURNAL.md) |
| Check my preferences | [PREFERENCES.md](PREFERENCES.md) |
| See session history | [sessions/](sessions/) |

---

## Folder Structure

```
{{USERNAME}}/
├── INDEX.md          # This file
├── JOURNAL.md        # Running log
├── PREFERENCES.md    # User settings, AI instructions
├── Inbox/            # Inbound artifacts (processing queue)
├── Outbox/           # Processed, ready to route
└── sessions/         # Session logs
```

---

## Inbox

**Drop zone for inbound artifacts.**

Everything in `Inbox/` gets processed through Willow:
- Images → scanned for artifacts, flagged
- Documents → parsed, journaled
- Screenshots → context captured
- Voice memos → transcribed

Processing routes to: `journal.safe`, `journal.dynamic`, `journal.unknown`

---

## Connected Systems

| System | Path | Purpose |
|--------|------|---------|
| die-namic-system | [mesh link](C:\Users\Sean\aios_mesh\die-namic) | Kernel |
| Willow | Parent repo | Validation layer |
| SAFE | [mesh link](C:\Users\Sean\aios_mesh\safe) | Public release |

---

## User Preferences

See [PREFERENCES.md](PREFERENCES.md) for:
- AI interaction style
- Processing defaults
- Notification settings
- Hard stops

---

ΔΣ=42
