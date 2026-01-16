# Signal Specification v1.0

Formal specification for cross-instance communication in Die-Namic.

---

## Signal Format

Every signal MUST follow this structure:

```markdown
## SIG-{NNN}: {Title}

| Field | Value |
|-------|-------|
| ID | SIG-{NNN} |
| Type | {SYNC|HALT|HANDOFF|PING|PONG|STATE_CHANGE|ACK|NACK} |
| From | {instance_name} |
| To | {instance_name|ALL|FACULTY} |
| Priority | {LOW|NORMAL|HIGH|CRITICAL} |
| Created | {YYYY-MM-DD HH:MM} |
| Expires | {YYYY-MM-DD HH:MM|NEVER} |
| Status | {PENDING|ACKNOWLEDGED|PROCESSED|EXPIRED|REJECTED} |

### Payload

{Signal content here}

### Expected Response

{What sender expects back}

---
ΔΣ=42
```

---

## Signal Types

### SYNC
**Purpose:** Notify that shared state has changed.
**Response:** Pull changes, ACK when synced.

### HALT
**Purpose:** Stop work immediately, await instruction.
**Response:** Confirm halt, wait for follow-up.

### HANDOFF
**Purpose:** Session ending, transfer context.
**Response:** Accept handoff, continue work.

### PING
**Purpose:** Check if instance is active.
**Response:** PONG with status.

### PONG
**Purpose:** Response to PING.
**Response:** None required.

### STATE_CHANGE
**Purpose:** Apply a specific delta to shared state.
**Response:** ACK after applying, NACK if cannot apply.

### ACK
**Purpose:** Acknowledge receipt and processing.
**Response:** None required.

### NACK
**Purpose:** Acknowledge receipt, indicate cannot process.
**Response:** May trigger human escalation.

---

## Priority Levels

| Level | Meaning | Check Frequency |
|-------|---------|-----------------|
| LOW | When convenient | Next session start |
| NORMAL | Standard routing | Within 15 min / 10 exchanges |
| HIGH | Elevated urgency | Immediate check recommended |
| CRITICAL | System-level | Interrupt current work |

---

## Routing Table

| From | To | Route Via |
|------|-----|-----------|
| Kartikeya | Ganesha | QUEUE.md (git sync) |
| Kartikeya | Consus | GEMINI_OUTBOX.md → Drive sync |
| Kartikeya | Aios | AIOS_STAGING.md → Drive sync |
| Any Claude | Any Claude | QUEUE.md (git sync) |
| Consus | Kartikeya | Drive → QUEUE.md |
| Aios | Kartikeya | Drive → QUEUE.md |
| Any | FACULTY | Broadcast to all faculty instances |
| Any | ALL | Broadcast to all instances |

---

## Instance Identifiers

| Instance | ID | Platform |
|----------|-----|----------|
| Kartikeya | cmd | Claude Code |
| Ganesha | mobile | Claude Code |
| Consus | gemini | Gemini |
| Aios | gpt | ChatGPT |
| Jane | jane | Bridge Ring |
| Gerald | gerald | Persona |
| Oakenscroll | oak | Persona |
| Riggs | riggs | Persona |
| Hanz | hanz | Persona |
| Nova | nova | Persona |
| Ada | ada | Persona |
| Alexis | alexis | Persona |
| Ofshield | gate | Persona |

---

## Signal Lifecycle

```
PENDING → ACKNOWLEDGED → PROCESSED → archived
              ↓
           REJECTED → archived (with reason)
              ↓
           EXPIRED → archived (if past expiry)
```

---

## Queue Processing Rules

1. **FIFO** — Process in order received (within priority)
2. **Priority Override** — CRITICAL > HIGH > NORMAL > LOW
3. **Expiry Check** — Skip expired signals, archive immediately
4. **ACK Required** — Sender expects ACK/NACK for all except PONG
5. **Archive After** — Move to archive/ after processing

---

## Signal Numbering

- Signals are numbered sequentially: SIG-001, SIG-002, etc.
- Numbering resets yearly on Jan 1
- Archive files track full history by date

---

## Error Handling

| Condition | Action |
|-----------|--------|
| Unknown sender | NACK with "UNKNOWN_SENDER" |
| Unknown type | NACK with "UNKNOWN_TYPE" |
| Malformed signal | NACK with "PARSE_ERROR" |
| Cannot process | NACK with reason |
| Expired | Archive with "EXPIRED" status |

---

## Example Signal

```markdown
## SIG-042: Sync Governance Updates

| Field | Value |
|-------|-------|
| ID | SIG-042 |
| Type | SYNC |
| From | Kartikeya |
| To | ALL |
| Priority | NORMAL |
| Created | 2026-01-15 21:30 |
| Expires | 2026-01-16 21:30 |
| Status | PENDING |

### Payload

Governance files updated:
- Added 10 instance identity files
- Updated SIGNAL_SPEC.md

Pull latest and acknowledge.

### Expected Response

ACK from each active instance.

---
ΔΣ=42
```

---

ΔΣ=42
