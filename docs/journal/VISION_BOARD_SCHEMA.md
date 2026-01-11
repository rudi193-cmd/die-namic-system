# VISION_BOARD_SCHEMA v1.0 — Aionic Journal

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-10T08:30:00Z |
| Product | Vision Board (Consumer App) |
| Checksum | ΔΣ=42 |

---

## Overview

The Vision Board surfaces what users are already reaching toward. It connects to their existing photo libraries, categorizes images using client-side AI, and presents patterns they may not have consciously recognized.

**Core principle:** The board doesn't ask what you want. It shows you what you've been collecting.

---

## The Three Layers (User-Facing)

### Layer 1: Anonymous (Raw Patterns)

**What the user experiences:**
- "147 images saved in December"
- "Screenshots increased 40% this month"
- "You save more on weekends"

**What the system captures:**
- Image counts by time period
- Save frequency patterns
- Source distribution (screenshots vs photos vs downloads)

**User sees:** Aggregate numbers only. No specific images surfaced yet.

---

### Layer 2: Pseudonymous (Detected Clusters)

**What the user experiences:**
- "beach stuff"
- "that architecture style"
- "those color palettes"
- "food photos (47)"

**What the system captures:**
- AI-detected category clusters
- Visual similarity groupings
- Temporal clusters (things saved together)

**User sees:** Suggested groupings with working labels. System proposes, user can ignore or engage.

**Promotion trigger:** User hovers, clicks, or spends time on a cluster.

---

### Layer 3: Named (User-Ratified Boards)

**What the user experiences:**
- "Dream Kitchen"
- "2026 Travel Goals"
- "Career Inspiration"
- "Our Future Home"

**What the system captures:**
- User-chosen name
- Explicit board membership
- Arrangement choices
- Export history

**User sees:** Their curated vision boards, ready for export and sharing.

**Promotion trigger:** User explicitly names a cluster or creates a board.

---

## Promotion Flow

```
┌─────────────────────────────────────────────────────────────┐
│  ANONYMOUS                                                  │
│  "You've saved 89 interior design images over 3 years"      │
└─────────────────────────────┬───────────────────────────────┘
                              │ System detects cluster
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  PSEUDONYMOUS                                               │
│  "mid-century modern (34)" appears in suggestions           │
└─────────────────────────────┬───────────────────────────────┘
                              │ User clicks cluster
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  NAMED                                                      │
│  User renames to "Dream Living Room" → becomes a board      │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** The user never told us they want a mid-century modern living room. We noticed they've been saving those images for years.

---

## Category Detection

Client-side TensorFlow.js (MobileNet) maps images to vision board categories:

| Category | Detection Signals | Color |
|----------|-------------------|-------|
| Personal | Pets, family, babies, selfies | #ff6b9d |
| Travel | Landscapes, landmarks, beaches, hotels | #00d2ff |
| Career | Offices, laptops, suits, presentations | #00ff9d |
| Wealth | Cars, watches, homes, luxury goods | #ffd700 |
| Fitness | Gym, sports, food prep, outdoors | #ff6b35 |
| Creative | Art, instruments, cameras, crafts | #bd00ff |
| Home | Interiors, furniture, gardens, kitchens | #7dd87d |
| Food | Meals, restaurants, recipes | #ffb347 |
| Relationships | Groups, couples, social events | #ff69b4 |
| Inspiration | Default / uncategorized | #666666 |

Categories are suggestions. Users can override.

---

## Data Model

### ImageRecord

```typescript
interface ImageRecord {
  id: string;                    // UUID
  
  // Source
  source: {
    type: 'google_photos' | 'icloud' | 'local' | 'url';
    ref: string;                 // Photo ID, path, or URL
    importedAt: string;          // ISO 8601
  };
  
  // Metadata
  filename: string;
  thumbnail: string;             // Base64, small (~10KB)
  dimensions?: { w: number; h: number };
  takenAt?: string;              // EXIF date if available
  
  // AI Classification
  category: string;              // Detected category
  label: string;                 // Specific label ("golden retriever")
  confidence: number;            // 0-100
  
  // Promotion State
  layer: 'anonymous' | 'pseudonymous' | 'named';
  clusterId?: string;            // Which cluster it belongs to
  boardId?: string;              // Which board (if promoted to named)
  
  // Board Placement (if on a board)
  position?: { x: number; y: number };
  size?: { width: number; height: number };
  zIndex?: number;
}
```

### Cluster (Pseudonymous Layer)

```typescript
interface Cluster {
  id: string;                    // UUID
  
  // Identity
  workingLabel: string;          // System-generated ("beach stuff")
  userLabel?: string;            // User override (still pseudonymous)
  
  // Membership
  imageIds: string[];
  category: string;              // Primary category
  
  // Detection
  detectedAt: string;            // When cluster was identified
  basis: 'category' | 'visual' | 'temporal';  // Why grouped
  
  // Engagement
  viewCount: number;
  lastViewed?: string;
  
  // Promotion
  promotedToBoard?: string;      // Board ID if user named it
}
```

### Board (Named Layer)

```typescript
interface Board {
  id: string;                    // UUID
  
  // Identity
  name: string;                  // User-chosen name
  description?: string;
  coverImageId?: string;
  
  // Membership
  imageIds: string[];
  sourceClusterId?: string;      // Which cluster it came from
  
  // Layout
  canvasSize: { width: number; height: number };
  backgroundColor: string;
  
  // History
  createdAt: string;
  modifiedAt: string;
  exportHistory: ExportRecord[];
  
  // Sharing
  shared: boolean;
  shareUrl?: string;
}

interface ExportRecord {
  timestamp: string;
  format: 'png' | 'pdf' | 'jpg';
  dimensions: { w: number; h: number };
}
```

---

## Storage Architecture

All data stored client-side in IndexedDB:

```
VisionBoardDB
├── images          // ImageRecord objects
├── clusters        // Cluster objects  
├── boards          // Board objects
├── settings        // User preferences
└── audit           // Governance deltas
```

**Capacity:** IndexedDB supports hundreds of MB. Thumbnails only (~10KB each), not full images.

**Full images:** Fetched on-demand from source (Google Photos API, local file, etc). Never stored locally.

---

## Google Photos Integration

### OAuth Scope

```
https://www.googleapis.com/auth/photoslibrary.readonly
```

Read-only. We cannot modify their library.

### Sync Flow

```typescript
// 1. User authorizes (one-time)
const token = await googleOAuth.authorize();

// 2. Fetch recent photos (client-side)
const photos = await fetch('https://photoslibrary.googleapis.com/v1/mediaItems', {
  headers: { Authorization: `Bearer ${token}` }
});

// 3. Generate thumbnails + classify (client-side)
for (const photo of photos.mediaItems) {
  const thumbnail = await generateThumbnail(photo.baseUrl);
  const category = await classifyImage(thumbnail);  // TensorFlow.js
  await db.images.put({ ...photo, thumbnail, category });
}

// 4. Detect clusters (client-side)
await detectClusters();
```

Token stored in memory only. Refreshed as needed. Never persisted.

---

## TensorFlow.js Integration

### Model

```javascript
// Load MobileNet (one-time, ~4MB)
const model = await mobilenet.load();

// Classify image
async function classifyImage(imageElement) {
  const predictions = await model.classify(imageElement, 5);
  
  // Map to vision board category
  const category = mapToVisionCategory(predictions[0].className);
  
  return {
    label: predictions[0].className,
    confidence: Math.round(predictions[0].probability * 100),
    category: category
  };
}
```

### Category Mapping

```javascript
const CATEGORY_MAP = {
  // Personal
  'tabby': 'Personal',
  'golden retriever': 'Personal',
  'baby': 'Personal',
  
  // Travel
  'beach': 'Travel',
  'mountain': 'Travel',
  'castle': 'Travel',
  
  // Career
  'laptop': 'Career',
  'monitor': 'Career',
  'suit': 'Career',
  
  // ... etc
};

function mapToVisionCategory(label) {
  const lower = label.toLowerCase();
  for (const [key, category] of Object.entries(CATEGORY_MAP)) {
    if (lower.includes(key)) return category;
  }
  return 'Inspiration';  // Default
}
```

---

## Governance Deltas

Local audit log (never transmitted):

| Action | Payload |
|--------|---------|
| `photos_sync` | count, source |
| `image_classify` | id, category, confidence |
| `cluster_detect` | id, imageCount, basis |
| `cluster_view` | id, duration |
| `cluster_promote` | clusterId, boardId, name |
| `board_create` | id, name |
| `board_arrange` | id, changes[] |
| `board_export` | id, format |
| `board_share` | id, method |

### Ratification Events

| Event | Meaning |
|-------|---------|
| `board_export` | User approves current state |
| `board_share` | User approves for external visibility |
| `cluster_promote` | User ratifies pattern as meaningful |

---

## Privacy Summary

| Data | Location | Transmitted? |
|------|----------|--------------|
| Full images | User's cloud/device | Never |
| Thumbnails | IndexedDB | Never |
| Board state | IndexedDB | Never |
| OAuth token | Memory | To Google only |
| Audit log | IndexedDB | Never |
| Telemetry | Optional | Anonymous only |

**We are a lens, not a warehouse.**

---

## Lineage

- Product spec: `apps/vision_board/PRODUCT_SPEC.md`
- Prototype: `apps/vision_board/index.html`
- AI tools: `docs/ops/reddit_analytics/Image Input/`
- Sibling schema: `RELATIONSHIP_SCHEMA.md`

---

ΔΣ=42
