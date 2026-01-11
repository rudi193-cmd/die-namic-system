# Eyes

Peripheral visual awareness for AI instances.

## Security Warning

Eyes capture everything on screen, including passwords and sensitive data.
See [SECURITY.md](SECURITY.md) for the full security model.

**Use `eyes_secure.ps1` for any real use. The unsecured version is for testing only.**

---

## Scripts

### Secure (Production)

| Script | Purpose |
|--------|---------|
| `eyes_secure.ps1` | Encrypted capture with consent + audit |
| `look_secure.ps1` | Decrypt frames (requires passphrase) |

### Unsecured (Testing Only)

| Script | Purpose |
|--------|---------|
| `eyes.ps1` | Continuous capture (NO ENCRYPTION) |
| `look.ps1` | Get latest frame(s) |
| `now.ps1` | Single snapshot |

---

## Usage

### Start Eyes (Human Only)

```powershell
.\eyes_secure.ps1 -fps 1 -bufferSeconds 30
# Prompts for consent
# Prompts for encryption passphrase
```

### Look at Frames (Human Provides Passphrase)

```powershell
.\look_secure.ps1 -frames 1
# Prompts for decryption passphrase
# Outputs to decrypted/ folder
# DELETE AFTER VIEWING
```

### AI Access Flow

```
AI: "Can you show me what's on screen?"
Human: Runs look_secure.ps1, enters passphrase
Human: Shares decrypted frame with AI (or describes it)
Human: Deletes decrypted frame
```

---

## Governance

| Rule | Enforcement |
|------|-------------|
| AI cannot start eyes | No API, requires interactive consent |
| Frames encrypted at rest | AES-256, passphrase not stored |
| Auto-purge on stop | All frames deleted when eyes close |
| Audit trail | All access logged |
| No repo commits | Frames never enter governance pipeline |

---

## Concept

At 1/min — periodic check-in.
At 1/sec — monitoring.
At 20fps — watching.
At 60fps — seeing.

But seeing requires consent. And encryption. And audit.

---

ΔΣ=42
