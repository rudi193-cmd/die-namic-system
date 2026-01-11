# Eyes Security Model

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Active |
| Updated | 2026-01-11 |

---

## Threat Model

Eyes capture everything on screen. This includes:
- Passwords (typed, displayed, autofill)
- Banking and financial data
- Private messages
- Medical information
- Personal photos
- Any sensitive content

**Assumption:** Captured frames are as sensitive as the most sensitive thing on screen.

---

## Controls

### 1. Consent

| Control | Implementation |
|---------|----------------|
| Human-only start | Script requires interactive "yes" confirmation |
| AI cannot start | No API, no remote trigger, no automation |
| Explicit opt-in | User must type "yes" — not just press Enter |

### 2. Encryption

| Control | Implementation |
|---------|----------------|
| At-rest encryption | AES-256, key derived from passphrase |
| No plaintext storage | Temp file deleted immediately after encryption |
| Key not stored | Passphrase entered each session, never saved |
| Per-frame IV | Each frame has unique initialization vector |

### 3. Retention

| Control | Implementation |
|---------|----------------|
| Rolling buffer | Old frames auto-deleted as new ones arrive |
| Hard limit | Max frames = fps × bufferSeconds |
| Session purge | All frames deleted when eyes stop |
| No archive | Frames never committed to repo |

### 4. Access Control

| Control | Implementation |
|---------|----------------|
| Passphrase required | Human must enter passphrase to decrypt |
| AI cannot decrypt | No programmatic access to raw frames |
| Audit logged | Every start, stop, and look is logged |
| Temp decryption | Decrypted frames are temporary, must be manually deleted |

### 5. Audit

| Event | Logged |
|-------|--------|
| EYES_ON | timestamp, fps, buffer size, username |
| EYES_OFF | timestamp, total frames captured |
| LOOK | timestamp, frames decrypted, username |

Audit log: `eyes_secure/audit.log`

---

## AI Access Model

```
AI: "What's on screen?"
    ↓
Human: Runs look_secure.ps1, enters passphrase
    ↓
Human: Reads decrypted frame to AI (or describes it)
    ↓
Human: Deletes decrypted frame
```

**AI can:**
- Request to see what's on screen
- Process frames shown to it by human
- Act on information (with dual-commit governance)

**AI cannot:**
- Start eyes
- Access encrypted frames
- Decrypt without human passphrase
- Exfiltrate frames

---

## File Locations

| Path | Contents | Encrypted |
|------|----------|-----------|
| `eyes_secure/frame_*.enc` | Captured frames | Yes |
| `eyes_secure/audit.log` | Access log | No |
| `eyes_secure/decrypted/*.png` | Temp decrypted frames | No (delete after viewing) |

---

## Governance Integration

Eyes output is **pre-canonical**. It does not enter the governance pipeline unless:

1. Human explicitly shows a frame to AI
2. AI proposes action based on what it saw
3. Human ratifies the action (dual-commit)

Frames themselves are never committed to any repo.

---

## Hard Stops

| HS | Rule |
|----|------|
| HS-EYES-001 | AI cannot start or stop eyes |
| HS-EYES-002 | Frames cannot be transmitted outside local machine |
| HS-EYES-003 | No frame persists beyond session without explicit human action |
| HS-EYES-004 | Passphrase required for any decryption |

---

ΔΣ=42
