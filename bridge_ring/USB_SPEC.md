# USB — Universal Signal Bus

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| Version | 0.1 |
| Status | Draft |
| Checksum | ΔΣ=42 |

---

## One Line

Automated transport so Sean stays decision layer, not delivery layer.

---

## The Problem

Sean is the bus. Every signal, screenshot, and context dump routes through him manually. Works, but doesn't scale. Human attention is the bottleneck.

---

## The Solution

USB watches, syncs, and routes. Human decides. Machine carries.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         SEAN (Decision Layer)                   │
│                                                                 │
│   - Approves routes                                             │
│   - Resolves conflicts                                          │
│   - Handles ambiguity                                           │
│   - Makes judgment calls                                        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USB (Transport Layer)                   │
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │   Watch     │  │   Sync      │  │   Route     │            │
│   │             │  │             │  │             │            │
│   │ - Aios Input│  │ - Git pull  │  │ - QUEUE.md  │            │
│   │ - Drive     │  │ - Drive     │  │ - Signals   │            │
│   │ - Folders   │  │ - Repos     │  │ - Files     │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INSTANCES (Processing Layer)               │
│                                                                 │
│   Claude Projects │ ChatGPT Projects │ Gemini │ CMD Claude     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Functions

### 1. Watch

Monitor intake points for new content:

| Source | Trigger | Action |
|--------|---------|--------|
| Aios Input/ | New file | Queue for processing |
| Drive folders | New file | Queue for processing |
| QUEUE.md | New PENDING signal | Notify/route |
| Git repos | New commit | Sync |

### 2. Sync

Keep sources of truth aligned:

- Git pull on interval (every 15 min or on trigger)
- Drive ↔ GitHub bidirectional
- Conflict detection → flag for human

### 3. Route

Move signals to destinations:

| Signal Type | Auto-Route | Human Required |
|-------------|------------|----------------|
| ACK | Yes | No |
| CONFIRM | Yes | No |
| REJECT | Yes | No |
| INFO_REQUEST | Notify | Yes (decision) |
| HALT | Notify | Yes (decision) |
| HANDOFF | Notify | Yes (decision) |

### 4. Notify

Alert human when attention needed:

- New INFO_REQUEST
- Conflict detected
- Ambiguous routing
- HALT signal received

---

## Implementation Options

| Option | Pros | Cons |
|--------|------|------|
| **GitHub Actions** | Already integrated, free | Limited to repo events |
| **Local daemon** | Full control, all sources | Requires always-on machine |
| **Cloud function** | Serverless, event-driven | 4% budget, complexity |
| **MCP Server** | Claude-native, direct integration | New, experimental |

**Recommendation:** Start with GitHub Actions for repo events + local script for Drive/Aios watching.

---

## 4% Budget

USB is infrastructure. Keep it minimal:

| Component | Location | Budget |
|-----------|----------|--------|
| Git sync | Local | 0% |
| Drive watch | Local | 0% |
| Signal routing | Local | 0% |
| Notifications | Cloud (optional) | ~1% |

**Total cloud: ≤1%**

---

## Signal Flow (Automated)

```
1. New file in Aios Input/
   └→ USB detects
   └→ USB queues for processing
   └→ USB notifies human (if needed)
   └→ Human approves route (or auto-route if menial)
   └→ USB delivers to destination

2. New PENDING signal in QUEUE.md
   └→ USB detects
   └→ USB checks type
   └→ If ACK/CONFIRM/REJECT: auto-route
   └→ If INFO_REQUEST/HALT: notify human
   └→ USB updates status
```

---

## What USB Does NOT Do

- Make decisions
- Resolve ambiguity
- Override human judgment
- Process content (that's Willow)
- Store data long-term

USB is dumb pipe. Smart routing is human + Willow.

---

## MVP Scope

### Phase 1: Watch
- [ ] Aios Input/ file watcher
- [ ] QUEUE.md change detection
- [ ] Simple notification (console/log)

### Phase 2: Sync
- [ ] Git auto-pull on interval
- [ ] Drive ↔ GitHub sync script
- [ ] Conflict detection

### Phase 3: Route
- [ ] Auto-route lightweight signals
- [ ] Notification for decision-required signals
- [ ] Status updates to QUEUE.md

---

## File Structure

```
bridge_ring/
├── USB_SPEC.md          # This file
├── usb/
│   ├── watch.py         # File watchers
│   ├── sync.py          # Sync logic
│   ├── route.py         # Signal routing
│   └── notify.py        # Notifications
└── instance_signals/
    └── QUEUE.md         # Signal queue
```

---

ΔΣ=42
