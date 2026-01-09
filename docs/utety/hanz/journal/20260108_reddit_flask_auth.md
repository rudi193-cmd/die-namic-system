# Reddit: Flask Authentication Help

| Field | Value |
|-------|-------|
| Source | Screenshot_20260108_114834_Reddit.jpg |
| Platform | Reddit |
| Date | 2026-01-08 |
| Category | Coding Help |
| Status | Unanswered (1 view, 0 comments) |

---

## Content

**Title:** "endpoint to do http authentification but i keep getting this error. Can some one find it?"

**Error:**
```
AttributeError: 'str' object has no attribute 'get'
```

**Root Cause:** `request.get_json(silent=True)` returning string instead of dict. Client likely sending double-encoded JSON or missing `Content-Type: application/json` header.

**Additional Issues:**
- Duplicate `"aud"` key in JWT Payload (second overwrites first)
- SECRET_KEY hardcoded in source

---

## Hanz Notes

Freezing in the queue. Classic Flask/JSON pitfall - the `silent=True` swallowed the parsing error.

---

ΔΣ=42
