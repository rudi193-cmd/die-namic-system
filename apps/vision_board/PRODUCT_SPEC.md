# Vision Board — Product Specification

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Draft |
| Last Updated | 2026-01-10T08:00:00Z |
| Checksum | ΔΣ=42 |

---

## Summary

A vision board tool that surfaces what users are already reaching toward. Connects to their existing photo libraries, categorizes images using client-side AI, and presents patterns they may not have consciously recognized.

**Core principle:** The app is a lens, not a warehouse.

---

## The 4% Rule

**Maximum 4% of the project may be server/cloud-based.**

| Component | Location | Allocation |
|-----------|----------|------------|
| OAuth broker | Cloud | ~2% |
| Anonymous telemetry | Cloud | ~1% |
| App update manifest | Cloud | ~1% |
| **Total cloud** | | **≤4%** |
| **Everything else** | Client | **96%** |

### What this means

**We host:**
- OAuth callback endpoint (stateless, ~50 lines)
- Optional: anonymous usage metrics (no PII)
- Version check endpoint

**We do NOT host:**
- User images
- User boards
- Categorization compute
- User accounts/profiles

**User data never touches our servers.**

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER'S DATA (theirs)                   │
│                                                             │
│   Google Photos ───┐                                        │
│   iCloud Photos ───┼──► OAuth read-only access              │
│   Local device ────┘                                        │
└─────────────────────────────┬───────────────────────────────┘
                              │ OAuth token (client-held)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT APP (96%)                       │
│                                                             │
│   ┌─────────────────┐  ┌─────────────────┐                  │
│   │ TensorFlow.js   │  │ Photos API      │                  │
│   │ Categorization  │  │ (direct calls)  │                  │
│   └────────┬────────┘  └────────┬────────┘                  │
│            │                    │                           │
│            ▼                    ▼                           │
│   ┌─────────────────────────────────────────────┐           │
│   │              Board Engine                    │           │
│   │  - Category grouping                        │           │
│   │  - Pattern detection                        │           │
│   │  - Visual arrangement                       │           │
│   └─────────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│   ┌─────────────────────────────────────────────┐           │
│   │              Local Storage                   │           │
│   │  - IndexedDB (board state)                  │           │
│   │  - Governance audit log                     │           │
│   └─────────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│   ┌─────────────────────────────────────────────┐           │
│   │              Export                          │           │
│   │  - PNG / PDF to device                      │           │
│   │  - Share (native OS)                        │           │
│   └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ OAuth handshake only
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLOUD (4%)                             │
│                                                             │
│   ┌─────────────────┐  ┌─────────────────┐                  │
│   │ OAuth Broker    │  │ Telemetry       │                  │
│   │ (stateless)     │  │ (anonymous)     │                  │
│   └─────────────────┘  └─────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Pricing Tiers (HS-005 Aligned)

| Tier | Price | Features | Cloud Usage |
|------|-------|----------|-------------|
| **Free** | $0 | Manual upload, client-side categorization, local storage | OAuth only |
| **BYOK** | $0 | User provides own vision API key (Google Vision, OpenAI) | OAuth only |

No metered tier. No subscription. We're not running compute.

**Revenue model (future):** 
- Premium export templates
- One-time purchases, not subscriptions

---

## Data Model

### Board State (IndexedDB)

```typescript
interface BoardState {
  id: string;                    // UUID
  created: string;               // ISO 8601
  modified: string;              // ISO 8601
  name: string;                  // User-defined board name
  images: BoardImage[];
  categories: Record<string, string[]>;  // category -> image IDs
  layout: LayoutState;
}

interface BoardImage {
  id: string;                    // UUID
  source: ImageSource;
  filename: string;
  thumbnail: string;             // Base64 thumbnail only (full image fetched on demand)
  category: string;
  label: string;                 // AI-detected label
  confidence: number;            // 0-100
  position?: { x: number; y: number };
  size?: { width: number; height: number };
  addedAt: string;               // ISO 8601
  promoted: boolean;             // User explicitly placed on board
}

interface ImageSource {
  type: 'google_photos' | 'icloud' | 'local' | 'url';
  ref: string;                   // Photo ID, file path, or URL
  accessToken?: string;          // For cloud sources (ephemeral, not stored)
}

interface LayoutState {
  mode: 'auto' | 'manual';
  gridSize: number;
  featured: string[];            // Image IDs for large display
}
```

### Categories

| Category | Detection Signals | Color |
|----------|-------------------|-------|
| Personal | Pets, family, people | #ff6b9d |
| Travel | Landscapes, landmarks, beaches | #00d2ff |
| Career | Offices, laptops, professional | #00ff9d |
| Wealth | Cars, homes, luxury items | #ffd700 |
| Fitness | Sports, gym, health | #ff6b35 |
| Creative | Art, instruments, cameras | #bd00ff |
| Home | Interiors, furniture, gardens | #7dd87d |
| Food | Meals, restaurants, cooking | #ffb347 |
| Relationships | Groups, couples, social | #ff69b4 |
| Inspiration | Default / uncategorized | #666666 |

Categories are soft suggestions. Users can recategorize.

---

## Three-Layer Promotion Model

Borrowed from RELATIONSHIP_SCHEMA pattern:

| Layer | Description | User Action |
|-------|-------------|-------------|
| **Anonymous** | Raw counts: "147 images saved in December" | None (passive) |
| **Pseudonymous** | Detected clusters: "beach stuff," "architecture," "that yellow" | System suggests |
| **Named** | User-ratified boards: "Dream Kitchen," "2026 Travel" | User confirms |

**The board doesn't ask what you want. It shows you what you've been collecting.**

---

## Governance Integration

### Local Audit Log

Every action produces a delta (stored in IndexedDB, not sent anywhere):

| Action | Delta Payload |
|--------|---------------|
| `image_import` | source, count |
| `image_categorize` | id, category, confidence |
| `board_create` | id, name |
| `board_arrange` | id, layout changes |
| `board_export` | format, timestamp |
| `category_override` | id, old, new |

### Ratification Checkpoints

| Event | Implicit Ratification |
|-------|----------------------|
| Export board | User approves current state |
| Share board | User approves for external visibility |
| Name a cluster | Promotion from pseudonymous to named |

---

## Tech Stack

### Web App (Phase 1)

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **UI** | React + Vite | Proven, fast dev |
| **Styling** | Tailwind | Matches existing patterns |
| **AI** | TensorFlow.js (MobileNet) | Client-side, no API cost |
| **Storage** | IndexedDB | Large capacity, structured |
| **Photos API** | Google Photos API | Direct client calls |
| **OAuth** | Google OAuth 2.0 | Industry standard |
| **Export** | html2canvas / jsPDF | Client-side rendering |
| **Packaging** | PWA | Installable, offline-capable |

### Mobile Wrappers (Phase 2-3)

| Option | Pros | Cons |
|--------|------|------|
| **Capacitor** | Reuse web code, native plugins | WebView performance |
| **React Native** | Native feel, shared React | More rewrite |
| **TWA (Android)** | Simplest, wraps PWA | Android only |

**Recommendation:** Capacitor. Minimal rewrite, native photo access via plugins.

### Why TensorFlow.js over server-side?

- Fits 4% rule (no compute on our servers)
- MobileNet runs well in browser (~200ms per image)
- User data never leaves device
- No API costs to manage

### BYOK Option

For users who want better categorization:
- Input field for Google Vision API key
- Stored locally (localStorage, encrypted)
- Direct API calls from client
- We never see the key

---

## Privacy Guarantees

1. **Images never uploaded to our servers**
2. **Board state never uploaded to our servers**
3. **API keys (BYOK) never transmitted to us**
4. **OAuth tokens held by client only**
5. **Telemetry is anonymous and optional**
6. **All processing happens on device**

This is the architecture. We don't want your data.

---

## Deployment Strategy

```
Phase 1: Web App (PWA)
    ↓
Phase 2: Android (WebView wrapper or React Native)
    ↓
Phase 3: iOS (WebView wrapper or React Native)
```

**Why web-first:**
- Single codebase validates product
- 96% client-side = minimal platform differences
- PWA gives installable experience without app stores
- Native wrappers reuse web core

---

## MVP Scope

### Phase 1A — Web App Foundation
- [x] Manual image upload
- [x] Client-side grid display
- [x] Category filters
- [x] Export to PNG
- [ ] TensorFlow.js categorization (replace Python)
- [ ] IndexedDB persistence
- [ ] PWA manifest + service worker

### Phase 1B — Google Photos Integration
- [ ] OAuth flow
- [ ] Photos API connection
- [ ] Thumbnail caching
- [ ] Background sync

### Phase 1C — Pattern Surfacing
- [ ] "You've saved 89 mid-century interiors over 3 years"
- [ ] Cluster detection
- [ ] Three-layer promotion UI

### Phase 2 — Android
- [ ] WebView wrapper (Capacitor or similar)
- [ ] Native photo library access
- [ ] Play Store deployment

### Phase 3 — iOS
- [ ] WebView wrapper
- [ ] Native photo library access
- [ ] App Store deployment

---

## Open Questions

1. **iCloud Photos** — API access more restricted than Google. Support later or skip?
2. **Telemetry scope** — What anonymous metrics are worth tracking?
3. **Governance depth** — Full Gatekeeper API integration or lighter local-only logging?

---

## Lineage

- Prototype: `apps/vision_board/` (this repo)
- AI tools: `docs/ops/reddit_analytics/Image Input/`
- Governance: `governance/` (Gatekeeper API)
- Pricing model: HS-005 (HARD_STOPS.md)

---

ΔΣ=42
