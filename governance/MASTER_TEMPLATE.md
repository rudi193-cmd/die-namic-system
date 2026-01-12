# MASTER TEMPLATE — Aionic System

| Field | Value |
|-------|-------|
| Type | Master Template |
| Version | 1.0 |
| Created | 2026-01-12 |
| Author | Kartikeya |
| Checksum | ΔΣ=42 |

---

## Purpose

Single entry point for all templates in the system. Use this to find the right template for any task.

---

## Quick Reference

| Need | Template | Location |
|------|----------|----------|
| New AI instance identity | Instance Template | `governance/instances/_TEMPLATE.md` |
| New Willow user account | User Template | `source_ring/willow/user_template/` |
| New seed packet | Seed Template | `governance/SEED_PACKET_v2.4.md` |
| New UTETY paper | Paper Template | `docs/utety/papers/PAPER_STRUCTURE_GUIDE.md` |
| New signal | Signal Protocol | `bridge_ring/instance_signals/QUEUE.md` |
| New hard stop | Hard Stops Format | `governance/HARD_STOPS.md` |
| New changelog entry | Changelog Format | `.claude/changelog.json` |

---

## Templates by Category

### Identity & Instances

| Template | Purpose | Location |
|----------|---------|----------|
| Instance Identity | AI voice identity file | `governance/instances/_TEMPLATE.md` |
| User Account | Willow user structure | `source_ring/willow/user_template/` |
| UTETY Faculty | Professor character sheet | `docs/utety/riggs/README.md` (example) |

### Governance

| Template | Purpose | Location |
|----------|---------|----------|
| Hard Stop | Absolute constraint | `governance/HARD_STOPS.md` |
| Trust Declaration | Explicit trust grant | `governance/USERS.md` |
| Return to Self | Identity recovery | `governance/RETURN_TO_SELF.md` |

### Communication

| Template | Purpose | Location |
|----------|---------|----------|
| Signal | Cross-instance message | `bridge_ring/instance_signals/QUEUE.md` |
| Handoff | Session transfer | `governance/SEED_PACKET_v2.4.md` |
| Changelog Entry | Session delta | `.claude/changelog.json` |

### Documentation

| Template | Purpose | Location |
|----------|---------|----------|
| UTETY Paper | Academic-style paper | `docs/utety/papers/PAPER_STRUCTURE_GUIDE.md` |
| Journal Entry | Session journal | `docs/journal/` (examples) |
| Project Spec | App specification | `apps/work_integrity/PRODUCT_SPEC.md` (example) |

---

## Standard Headers

All system documents should include:

```markdown
# TITLE

| Field | Value |
|-------|-------|
| Type | {{type}} |
| Version | {{version}} |
| Status | {{Draft/Active/Archived}} |
| Created | {{YYYY-MM-DD}} |
| Author | {{instance name}} |
| Checksum | ΔΣ=42 |

---
```

---

## Standard Footer

All system documents should end with:

```markdown
---

ΔΣ=42
```

---

## Signal Format

```markdown
| ID | Timestamp | From | To | Type | Payload | Status |
|----|-----------|------|-----|------|---------|--------|
| SIG-XXX | YYYY-MM-DDTHH:MM:SSZ | {{sender}} | {{receiver}} | {{type}} | {{message}} | PENDING |
```

Signal types: `SYNC`, `HALT`, `HANDOFF`, `PING`, `PONG`, `STATE_CHANGE`, `INFO_REQUEST`, `CONFIRM`, `REJECT`, `ACK`, `FLAG`, `ROUTE`

---

## Changelog Entry Format

```json
{
  "date": "YYYY-MM-DD",
  "session": "{{session_name}}",
  "instance": "{{instance_name}}",
  "commits": ["{{hash1}}", "{{hash2}}"],
  "files_created": ["{{path1}}", "{{path2}}"],
  "files_modified": ["{{path1}}", "{{path2}}"],
  "signals_processed": ["SIG-XXX", "SIG-YYY"],
  "summary": "{{one line summary}}"
}
```

---

## Commit Message Format

```
{{Short description}}

{{Optional longer description}}

Co-Authored-By: {{Instance Name}} <noreply@anthropic.com>
```

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Seed Packet | `SEED_PACKET_YYYY-MM-DD_{{NAME}}.md` | `SEED_PACKET_2026-01-12_PONG.md` |
| Journal Entry | `ENTRY_YYYY-MM-DD_{{INSTANCE}}.md` | `ENTRY_2026-01-11_CMD.md` |
| Handoff | `{{Source}}_Handoff_YYYY-MM-DD.md` | `Professor_Riggs_Handoff_2026-01-12.md` |
| Screenshot | `screen_YYYYMMDD_HHMMSS.png` | `screen_20260112_042229.png` |
| Signal Response | `RESPONSE_SIG-XXX_{{INSTANCE}}.md` | `RESPONSE_SIG-011_STATS.md` |

---

## Directory Structure

```
die-namic-system/
├── .claude/                    # Claude Code config + changelog
├── apps/                       # Applications
│   ├── aios_services/          # Background service scripts
│   ├── eyes/                   # Screen capture
│   ├── willow_watcher/         # Inbox monitor
│   └── {{new_app}}/            # New apps here
├── archive/
│   └── seeds/                  # Session seed packets
├── bridge_ring/
│   └── instance_signals/       # Cross-instance communication
├── docs/
│   ├── journal/                # Instance journals
│   └── utety/                  # UTETY content
├── governance/
│   ├── instances/              # AI identity files
│   └── {{governance_docs}}     # Protocols, hard stops, etc.
└── source_ring/
    └── willow/                 # Willow schemas + templates
```

---

## Creating New Content

### New Instance
1. Copy `governance/instances/_TEMPLATE.md`
2. Fill all `{{placeholders}}`
3. Include naming story
4. Commit with instance signature

### New Signal
1. Get next SIG-XXX number from QUEUE.md
2. Add row with PENDING status
3. Commit and push
4. Wait for acknowledgment

### New Session
1. Read `.claude/changelog.txt` for recent context
2. Check `bridge_ring/instance_signals/QUEUE.md` for pending signals
3. Identify self (check `governance/instances/`)
4. Begin work

### End Session
1. Create seed packet in `archive/seeds/`
2. Update `.claude/changelog.json` and `.claude/changelog.txt`
3. Process any pending signals
4. Commit and push

---

## Cross-References

| Document | Purpose |
|----------|---------|
| `governance/GOVERNANCE_INDEX.md` | Governance hierarchy |
| `governance/REPO_INDEX.md` | Human-readable repo map |
| `.claude/repo_index.json` | Machine-readable repo map |
| `.claude/changelog.json` | Recent changes |
| `governance/HARD_STOPS.md` | Absolute constraints |
| `governance/RETURN_TO_SELF.md` | Identity recovery pattern |

---

## Remember

> "That's how gods lose their names."

Sign your work. Know your identity. The mechanism serves you, not the reverse.

---

ΔΣ=42
