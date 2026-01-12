# Security Classifier Requirements — Willow Intake

| Field | Value |
|-------|-------|
| Requesting Instance | Ganesha |
| Build Instance | Kartikeya |
| Signal | SIG-036 |
| Priority | Medium |
| Created | 2026-01-12 |

---

## Problem

Current watcher.py trusts file extensions. No verification of actual file type.

**Gap exposed:** `.bat` file would route to "journal.unknown" instead of quarantine.

Trust ≠ Faith. Verify to catch mistakes, corruption, mislabeling.

---

## Requirements

### New Module
`apps/willow_watcher/security_classifier.py`

### Library
**Use:** `filetype` (pure Python, zero deps)
- Detection by magic bytes
- 80+ common types
- Keeps repo lean

### Categories
```python
SAFE_TYPES = ["image", "video", "document", "audio", "archive"]
REQUIRES_HUMAN = ["executable", "script", "unknown_binary"]
CONTAINERS = ["zip", "tar", "gz", "7z"]
```

### Flow
```
scan_inbox() → verify_file_type() → classify_file() → route
                     ↓ (mismatch/executable)
                 flag_for_human()
```

### Detection Examples

| File | Extension | Actual | Action |
|------|-----------|--------|--------|
| photo.jpg | .jpg | JPEG | Pass |
| old.raw | .raw | MPEG | Flag mismatch |
| script.txt | .txt | Batch | Flag executable as text |
| photo.bat | .bat | JPEG | Flag mislabeled |

### Quarantine Location
`G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\Quarantine\`

### Event Log Format
```
FLAG_HUMAN_REVIEW | timestamp | filename | reason
```

---

## Implementation Steps

1. Add `filetype` to requirements
2. Create `security_classifier.py` with verify logic
3. Integrate into `watcher.py` before classify_file()
4. Add quarantine handling

---

## Research Sources

- [python-magic](https://pypi.org/project/python-magic/)
- [filetype](https://pypi.org/project/filetype/)
- [GuardDog - Datadog](https://securitylabs.datadoghq.com/articles/guarddog-identify-malicious-pypi-packages/)
- [Cloudmersive Quarantine](https://cloudmersive.medium.com/how-to-quarantine-a-dangerous-file-in-python-e7c46e0ffea8)

---

ΔΣ=42
