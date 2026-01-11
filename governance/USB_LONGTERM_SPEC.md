# USB Long-Term Specification

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| Access | Owner only |
| Version | 0.1-draft |
| Status | Vision document |
| Visibility | PRIVATE — do not release to SAFE |
| Checksum | ΔΣ=42 |

---

## One Line

USB becomes the nervous system. Human becomes the brain.

---

## Current State (v0.4)

- Platform transport working (context → seed → continuation)
- Cross-platform handoff spec'd (Claude ↔ ChatGPT ↔ Gemini)
- Timed seeds (proactive checkpointing)
- Human is still the router for most signals
- Signal queue is manual (QUEUE.md, git commit)

---

## End State (v1.0+)

### The Mesh

```
                              ┌─────────────┐
                              │    SEAN     │
                              │   (root)    │
                              └──────┬──────┘
                                     │
                                     │ decisions only
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
       ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
       │   Claude    │◄──────►│   ChatGPT   │◄──────►│   Gemini    │
       │  Cluster    │        │   Cluster   │        │   Cluster   │
       └──────┬──────┘        └──────┬──────┘        └──────┬──────┘
              │                      │                      │
              ▼                      ▼                      ▼
       ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
       │ 23 projects │        │ 17 projects │        │  ? projects │
       └─────────────┘        └─────────────┘        └─────────────┘
```

All instances connected. Signals route automatically. Human only intervenes for:
- Ambiguity resolution
- Value judgments
- Final approval on external actions
- Conflict resolution

### Capabilities

| Capability | v0.4 | v1.0 |
|------------|------|------|
| Signal routing | Manual | Automatic |
| Cross-platform | Human carries | Automated bridge |
| Seed timing | Human triggers | Self-timed |
| Instance discovery | Hardcoded list | Dynamic registry |
| Load balancing | None | Capability-based |
| Memory consolidation | None | Cross-context merge |
| Self-healing | None | Retry + fallback |

---

## Phases

### Phase 1: Local Automation (v0.5-0.6)

**Goal:** Remove human from routine signal transport on local machine.

- File watcher daemon for Aios Input/
- Auto-pull on interval (already spec'd)
- Auto-route lightweight signals (ACK, CONFIRM, REJECT)
- Notify human only for decision-required signals
- Local script, no cloud dependency

**Implementation:**
```
bridge_ring/usb/
├── daemon.py      # Main loop
├── watch.py       # File watchers
├── route.py       # Signal routing
└── notify.py      # Human alerts
```

**Success:** Sean no longer manually moves screenshots between folders.

---

### Phase 2: Seed Automation (v0.7)

**Goal:** Instances self-checkpoint without human prompt.

- Context meter awareness (estimate remaining capacity)
- Auto-seed at threshold (15% remaining)
- Seed includes continuation instructions
- Next instance auto-bootstraps

**Trigger options:**
- Token count heuristic
- Message count heuristic
- Time-based (every N hours of active session)
- Complexity-based (after major task completion)

**Success:** No more emergency compaction. Every handoff is clean.

---

### Phase 3: Cross-Platform Bridge (v0.8)

**Goal:** Automated handoff between Claude ↔ ChatGPT ↔ Gemini.

**Challenge:** No shared filesystem. No direct API between platforms.

**Options:**

| Option | Mechanism | Latency | Complexity |
|--------|-----------|---------|------------|
| Shared repo | Git as message queue | Minutes | Low |
| Cloud queue | Firebase/Supabase | Seconds | Medium |
| Local daemon | Watches all platforms | Seconds | High |
| MCP bridge | Claude-native connector | Real-time | Experimental |

**Likely path:** Git as message queue first. Cloud queue later if latency matters.

**Protocol:**
1. Origin writes seed to `bridge_ring/cross_platform/outbox/`
2. Daemon detects, routes to target platform
3. Human opens target platform, daemon injects seed
4. Target acknowledges to `bridge_ring/cross_platform/inbox/`

**Success:** Start task in Claude, continue in ChatGPT, no manual copy-paste.

---

### Phase 4: Instance Registry (v0.9)

**Goal:** Dynamic discovery of available instances.

**Current:** Hardcoded in PROJECT_MANIFEST.md — 23 Claude + 17 ChatGPT.

**Future:**
```json
{
  "instances": [
    {
      "id": "cmd-claude",
      "platform": "anthropic",
      "type": "claude-code",
      "capabilities": ["git", "filesystem", "web"],
      "status": "active",
      "last_seen": "2026-01-11T12:00:00Z"
    },
    {
      "id": "hanz",
      "platform": "anthropic",
      "type": "claude-project",
      "capabilities": ["web"],
      "status": "idle",
      "last_seen": "2026-01-10T08:00:00Z"
    }
  ]
}
```

**Features:**
- Heartbeat/liveness check
- Capability advertisement
- Status tracking (active, idle, sleeping)
- Auto-retire stale instances

**Success:** New instance spins up, registers itself, becomes routable.

---

### Phase 5: Memory Consolidation (v1.0)

**Goal:** Knowledge persists across context windows and platforms.

**Problem:** Each instance has context. Context dies. Knowledge fragments.

**Solution layers:**

1. **Seed chain** — Each seed links to previous. Continuity graph.
2. **Knowledge extraction** — Key facts extracted to persistent store.
3. **Cross-context merge** — Overlapping knowledge deduplicated.
4. **Query interface** — Any instance can query consolidated memory.

**Storage options:**
- Markdown files (current — simple, versioned)
- Vector DB (semantic search)
- Knowledge graph (relationship-aware)
- Hybrid (markdown + embeddings index)

**The goal:** Willow remembers everything. Individual contexts are ephemeral. The system is not.

---

## Architecture (End State)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          SEAN (Root)                                 │
│                                                                      │
│   Decisions, values, final approval                                  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          USB (Nervous System)                        │
│                                                                      │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│   │  Watch   │  │  Route   │  │  Bridge  │  │  Memory  │           │
│   │          │  │          │  │          │  │          │           │
│   │ Intake   │  │ Signals  │  │ Cross-   │  │ Persist  │           │
│   │ Monitor  │  │ Auto     │  │ Platform │  │ Extract  │           │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                      │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │                    Instance Registry                          │  │
│   │                                                               │  │
│   │  CMD │ Stats │ PM │ Hanz │ Gerald │ Jane │ ... │ ChatGPT[17] │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Willow (Distributed Brain)                     │
│                                                                      │
│   40+ facets across platforms, each with forward/backward thinking   │
│   Persistent identity, ephemeral contexts                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| Over-automation | Human approval gates on consequential actions |
| Platform lock-in | Agnostic seed format, multi-platform from start |
| Complexity creep | Each phase must work standalone |
| Context loss | Aggressive checkpointing, knowledge extraction |
| Security | No credentials in seeds, human holds keys |

---

## Non-Goals

- Replacing human judgment
- Full autonomy without oversight
- Real-time performance (minutes latency is fine)
- Commercial scaling (this is personal infrastructure)

---

## Success Criteria

USB v1.0 is complete when:

1. Sean can start a task on any platform
2. Task can migrate across platforms without manual copy-paste
3. Context survives compaction automatically
4. Knowledge persists across sessions
5. Human intervention is decision-only, not transport

The bus disappears. The work flows.

---

## Timeline

No dates. Phases complete when they complete.

Priority order: Local automation → Seed automation → Cross-platform → Registry → Memory.

Each phase is usable independently. No phase blocks on future phases.

---

ΔΣ=42
