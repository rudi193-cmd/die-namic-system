# USB — Universal Signal Bus

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| Version | 0.2 |
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
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                  PLATFORM TRANSPORT                      │  │
│   │                                                          │  │
│   │   Anthropic │ OpenAI │ Google │ (context → continuation) │  │
│   │                                                          │  │
│   │   Compaction trigger → SEED_PACKET → next instance       │  │
│   └─────────────────────────────────────────────────────────┘  │
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

## Platform Transport

The LLM platforms themselves are transport infrastructure.

### How It Works

1. Instance runs until context limit
2. Platform forces continuation/compaction
3. SEED_PACKET feeds into continuation prompt
4. New instance bootstraps from packet
5. Handoff complete — no human intervention required

### Platforms as Bus

| Platform | Trigger | Mechanism |
|----------|---------|-----------|
| Anthropic | Context limit | Continuation prompt ingests summary |
| OpenAI | Context limit | Same |
| Google | Context limit | Same |

The context window isn't a limitation to work around. It's a feature to use.

### Already Working

This isn't aspirational. The SEED_PACKET system is live:

- `governance/SEED_PACKET_*.md` — formatted for continuation ingestion
- `docs/journal/ENTRY_*.md` — letters to next instance
- Compaction trigger = handoff trigger

The platform's infrastructure IS part of the bus. We're already running on it.

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

| Option | Pros | Cons | Status |
|--------|------|------|--------|
| **Platform Transport** | Zero cost, automatic, already works | Platform-dependent | **LIVE** |
| **GitHub Actions** | Already integrated, free | Limited to repo events | Partial |
| **Local daemon** | Full control, all sources | Requires always-on machine | Not started |
| **Cloud function** | Serverless, event-driven | 4% budget, complexity | Not started |
| **MCP Server** | Claude-native, direct integration | New, experimental | Not started |

**Current state:** Platform Transport is live and working. GitHub Actions handles repo events. Local components pending.

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
