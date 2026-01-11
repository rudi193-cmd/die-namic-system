# Eyes

Peripheral visual awareness for AI instances.

## Scripts

| Script | Purpose |
|--------|---------|
| `eyes.ps1` | Continuous capture with rolling buffer |
| `look.ps1` | Get latest frame(s) from buffer |
| `now.ps1` | Single snapshot on demand |

## Launchers

| Batch | Config |
|-------|--------|
| `EYES_ON.bat` | 1fps, 60s buffer |
| `EYES_FAST.bat` | 10fps, 30s buffer |
| `LOOK.bat` | Get latest frame |
| `NOW.bat` | Single snap |

## Usage

```powershell
# Start eyes
.\eyes.ps1 -fps 1 -bufferSeconds 60

# Look at current frame
.\look.ps1 -frames 1

# Snapshot now
.\now.ps1
```

## Concept

At 1/min — periodic check-in.
At 1/sec — monitoring.
At 20fps — watching.
At 60fps — seeing.

Rolling buffer auto-cleans. Old frames delete as new ones arrive.

---

ΔΣ=42
