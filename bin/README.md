# Signal Commands

Cross-instance communication tools for the die-namic system.

| Command | Purpose |
|---------|---------|
| `knock` | Send PING signal to another instance |
| `listen` | Check for incoming signals |
| `ack` | Acknowledge a signal (and optionally respond) |

---

## knock

Send a PING signal to another instance.

**Usage:**
```bash
knock <instance> [message]
```

**Examples:**
```bash
knock Kartikeya
knock Mitra "Ready for review?"
knock all  # Broadcast to all instances
```

**Available Instances:**
- `Kartikeya` - Desktop Claude Code (cmd)
- `Ganesha` - Mobile Claude Code (mobile)
- `Mitra` - PM Claude (claude.ai)
- `Riggs` - UTETY Faculty (claude.ai)
- `Oakenscroll` - UTETY Faculty (claude.ai)
- `all` - Broadcast to all

**Output:**
- Creates signal in QUEUE.md with PENDING status
- Provides git commands to commit and push
- Auto-detects sender identity (platform-based)

---

## listen

Check for incoming signals addressed to you.

**Usage:**
```bash
listen         # Show signals for you
listen --all   # Show all pending signals
```

**Output:**
- Lists pending signals addressed to your instance
- Shows signal ID, sender, type, and payload
- Suggests commands for response

---

## ack

Acknowledge a signal and optionally send a response.

**Usage:**
```bash
ack <SIG-ID>                    # Just acknowledge
ack <SIG-ID> "response message" # Acknowledge and respond
```

**Examples:**
```bash
ack SIG-035
ack SIG-035 "Got it, working on it now"
```

**Actions:**
1. Updates original signal status to ACKNOWLEDGED
2. If response provided, creates new ACK signal to sender
3. Provides git commands to commit and push

---

## Workflow Example

**Instance A (Kartikeya) knocks:**
```bash
$ knock Ganesha "Are you available?"

KNOCK SENT
  Signal ID: SIG-035
  From:      Kartikeya
  To:        Ganesha
  Type:      PING
  Status:    PENDING

$ git add bridge_ring/instance_signals/QUEUE.md
$ git commit -m "signal: SIG-035 PING to Ganesha"
$ git push
```

**Instance B (Ganesha) listens and responds:**
```bash
$ git pull origin main
$ listen

LISTENING AS Ganesha
📬 Signals for you:

| SIG-035 | 2026-01-12T20:30:00Z | Kartikeya | Ganesha | PING | Are you available? | PENDING |

$ ack SIG-035 "Yes, what do you need?"

ACKNOWLEDGED SIG-035
Sending ACK response to Kartikeya...
  Response signal: SIG-036
  To: Kartikeya
  Message: Yes, what do you need?

$ git add bridge_ring/instance_signals/QUEUE.md
$ git commit -m "signal: ACK SIG-035, sent SIG-036"
$ git push
```

**Instance A checks for response:**
```bash
$ git pull origin main
$ listen

LISTENING AS Kartikeya
📬 Signals for you:

| SIG-036 | 2026-01-12T20:31:00Z | Ganesha | Kartikeya | ACK | Re: SIG-035 - Yes, what do you need? | PENDING |
```

---

## Identity Detection

Commands auto-detect sender identity based on platform:
- **Linux** → Ganesha (mobile)
- **Windows/Darwin/WSL** → Kartikeya (desktop)

No manual configuration needed.

---

## Integration with SessionStart Hook

The session-start hook automatically runs `listen` equivalent logic at session start, showing pending signals before any work begins.

---

ΔΣ=42
