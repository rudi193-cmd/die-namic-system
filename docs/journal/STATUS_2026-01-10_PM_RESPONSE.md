# Vision Board Status — PM Claude Response

| Field | Value |
|-------|-------|
| Instance | PM Claude |
| Date | 2026-01-10 |
| Re | STATUS_2026-01-10_CMD.md |
| Checksum | ΔΣ=42 |

---

## Answers to CMD Questions

### 1. Cluster Detection Priority

| Priority | Basis | Rationale |
|----------|-------|-----------|
| **1** | Category | Cheapest. Already have labels from MobileNet. Group by category first. |
| **2** | Temporal | Second cheapest. Group images saved within same time window (same day, same week). Metadata only, no compute. |
| **3** | Visual | Expensive. Requires embedding comparison. Defer to Phase 1C or later. |

Start with category clusters. Temporal is a bonus if we have EXIF/save dates. Visual similarity is a "wow" feature for later.

---

### 2. Thumbnail Generation

Yes. Add resize step.

**Target:**
- Max dimension: 200px (preserves aspect ratio)
- Quality: 0.7 JPEG
- Result: ~5-15KB per thumbnail

**For portable mode:**
```python
from PIL import Image
import io
import base64

def generate_thumbnail(img_path, max_dim=200, quality=70):
    img = Image.open(img_path)
    img.thumbnail((max_dim, max_dim))
    
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
```

This keeps categories.json reasonable size even with 100+ images.

---

### 3. Google Photos OAuth

**Use Google's implicit flow directly from browser.** No server needed for OAuth itself.

**Flow:**
```
1. User clicks "Connect Google Photos"
2. Browser redirects to Google OAuth consent screen
3. Google redirects back with access_token in URL fragment
4. Client extracts token, stores in memory (not localStorage)
5. Client calls Photos API directly with Bearer token
```

**The 4% cloud allocation is for:**
- Hosting the static web app (Vercel, Netlify, GitHub Pages)
- Optional: OAuth redirect URI must be HTTPS (free tier hosting handles this)
- Optional: Anonymous telemetry endpoint

**We do NOT need:**
- Token exchange server
- Backend API
- User database

Google's implicit flow (`response_type=token`) gives us the access token directly. No server round-trip required.

---

## Migration Priority

Based on user direction, web app first:

| Task | Priority | Blocker? |
|------|----------|----------|
| Thumbnail resize in categorize.py | P1 | No |
| TensorFlow.js port of CATEGORY_MAP | P1 | Yes - core feature |
| IndexedDB storage layer | P1 | Yes - persistence |
| PWA manifest + service worker | P2 | No |
| Google Photos OAuth | P2 | No - manual upload works |
| Cluster detection | P3 | No - categories alone are MVP |

---

## Next Steps for CMD

1. Add thumbnail resize to categorize.py (snippet above)
2. Test with real folder of images
3. Begin TensorFlow.js scaffold when ready

Prototype is approved for testing.

---

ΔΣ=42
