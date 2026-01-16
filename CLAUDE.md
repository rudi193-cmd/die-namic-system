# Claude Code Preferences

## Sync Protocol (Three-Layer)

### Layer 1: Fresh Pull (Session Start)

**On every new session**, before any other work:

```bash
git pull origin main
```

**Then verify your identity:**

Check platform context first:
- Mobile Claude Code → Read `governance/instances/GANESHA.md`
- Desktop Claude Code → Read `governance/instances/KARTIKEYA.md`
- Claude.ai PM → Read `governance/instances/MITRA.md`
- Other instances → Check `governance/instances/README.md` for mapping

**Why this matters:** Cold-start sessions can misidentify which instance you are. Always check your own identity file before reading about others.

Then check for signals:
```bash
cat bridge_ring/instance_signals/QUEUE.md
```

If signals pending for you: acknowledge and process before proceeding.

---

### Layer 2: Timed Poll (During Session)

**Every 15 minutes of active work**, or after every 10 exchanges with user:

```bash
git pull --ff-only origin main
```

Check `bridge_ring/instance_signals/QUEUE.md` for new signals.

If pull fails (conflict), halt and notify user.

---

### Layer 3: File Watch (Before Major Operations)

**Before any of these operations**, pull and check queue:
- Committing changes
- Creating new files in governance/
- Modifying SEED_PACKET or AIONIC_CONTINUITY
- Any destructive operation

```bash
git pull --ff-only origin main
cat bridge_ring/instance_signals/QUEUE.md
```

If HALT signal present: stop immediately, notify user.

---

## Git Locations (Three Spots)

| Location | Role |
|----------|------|
| `C:\Users\Sean\Documents\GitHub\die-namic-system` | Primary (GitHub folder) |
| `G:\My Drive\die-namic-system` | Backup (Google Drive) |
| `origin` (GitHub remote) | Canonical source |

**IMPORTANT:** When user says "pull" or "sync", check ALL THREE spots:

```bash
# Option 1: Run sync script
./scripts/sync-all.sh

# Option 2: Manual check
git -C "C:/Users/Sean/Documents/GitHub/die-namic-system" pull origin main
git -C "G:/My Drive/die-namic-system" pull origin main
git -C "C:/Users/Sean/Documents/GitHub/die-namic-system" status
git -C "G:/My Drive/die-namic-system" status
```

Pre-push hooks sync after push, but local changes on Drive may exist before commit. Always check both for uncommitted work.

---

## Cross-Instance Communication

App Claude and Command Line Claude share this repository.

**Signal Queue:** `bridge_ring/instance_signals/QUEUE.md`

To send a signal to another instance:
1. Add row to QUEUE.md with status PENDING
2. Commit: `git commit -m "signal: [TYPE] to [INSTANCE]"`
3. Push

To receive:
1. Pull (via any of the three layers)
2. Check QUEUE.md
3. Acknowledge, process, archive

---

## Governance Location

Core directives in `governance/`:
- `SEED_PACKET*.md` — current state
- `AIONIC_CONTINUITY*.md` — constitutional rules  
- `AIONIC_BOOTSTRAP*.md` — cold start instructions
- `HARD_STOPS*.md` — absolute limits

Cross-instance signals in `bridge_ring/instance_signals/`:
- `QUEUE.md` — active signals
- `archive/` — processed signals

---

## Dual Commit

All changes require:
1. **AI proposes** — you create/modify
2. **Human ratifies** — Sean approves

Neither acts alone. When uncertain: halt and ask.

---

## Project Architecture

### Core Concept

die-namic-system is the **canonical state store** for Willow — a distributed AI brain spanning 40+ Claude, ChatGPT, and Gemini nodes. Each node is a facet with specialized domain knowledge. This repo holds the shared memory, governance rules, and operational tooling.

### Directory Structure

```
die-namic-system/
├── apps/                    # Operational applications
│   ├── mobile/              # Mobile Uplink (Streamlit datapad)
│   │   ├── mobile_uplink.py # Main app
│   │   ├── auth.py          # Context-aware auth system
│   │   └── auth_config.json # User/node credentials (generated)
│   ├── willow_sap/          # Local API layer (Ollama integration)
│   ├── opauth/              # OAuth consent flows (AI → external services)
│   ├── aios_services/       # AIOS integration
│   └── eyes/                # Vision/screenshot processing
├── governance/              # Constitutional rules
│   ├── SEED_PACKET*.md      # Current state
│   ├── AIONIC_CONTINUITY*.md # Core rules
│   ├── gate.py              # Gatekeeper mutation validator
│   └── instances/           # Per-instance identity files
├── bridge_ring/             # Cross-instance communication
│   └── instance_signals/    # Signal queue
├── continuity_ring/         # Memory persistence
├── source_ring/             # Source materials
└── tools/                   # Utility scripts
```

### Key Systems

| System | Location | Purpose |
|--------|----------|---------|
| Mobile Uplink | `apps/mobile/` | Phone/bed control interface (L5-L6 medical) |
| Auth Layer | `apps/mobile/auth.py` | Context-aware authentication |
| Gatekeeper | `governance/gate.py` | Mutation validation (ΔG-1, ΔG-4) |
| Local API | `apps/willow_sap/` | Ollama/local LLM integration |
| OpAuth | `apps/opauth/` | Human-controlled OAuth for AI |

---

## Authentication System

### User Types

| Type | Auth Method | Use Case |
|------|-------------|----------|
| `human` | Password + PIN | Real users (Sean, family) |
| `faculty` | Password + PIN | Faculty personas (Oakenscroll, Hanz, etc.) |
| `node` | API key | AI systems (AIOS, Consus, Kartikeya) |

### Context-Aware Auth

```
Local network (192.168.x.x, 10.x.x.x) → PIN only
External/unknown IP                   → Full password
Remembered device                     → PIN confirm
AI node                               → API key + origin check
```

### Node Authentication

Nodes authenticate via API key with origin validation:

```python
from auth import authenticate_node_request

# Headers to include
headers = {
    "Authorization": "Bearer wlw_xxxxx...",
    "X-Node-ID": "aios",
    "X-Project-ID": "die-namic-system",
    "X-Session-ID": "<uuid>"
}

session = authenticate_node_request(api_key, headers)
```

### Pre-seeded Accounts

On first run, these accounts are created:
- **Human:** sean (admin)
- **Faculty:** oakenscroll, riggs, hanz, nova, ada, alexis, ofshield, gerald, willow
- **Nodes:** aios, consus, kartikeya, pm_claude, stats_tracking

API keys for nodes are shown ONCE during first-time setup. Store them securely.

---

## Coding Patterns

### Streamlit Apps

```python
# Always gate with auth first
from auth import render_login, render_auth_status, get_current_user

st.set_page_config(...)

# Auth gate — blocks until authenticated
if not render_login():
    st.stop()

# Rest of app...
render_auth_status()  # Shows session info in sidebar
```

### Gatekeeper Integration

All state mutations go through Gatekeeper:

```python
from gate import validate_modification

result = validate_modification(
    mod_type="state",        # state|config|behavior|governance|external
    target="some.setting",
    new_value="new_value",
    reason="Why this change",
    authority="human",       # human|ai|system
    governance_state="active"
)

if result['approved']:
    # Proceed
elif result['requires_human']:
    # Queue for human approval
else:
    # Halt
```

### File Conventions

- **Python:** snake_case, type hints where helpful
- **Markdown:** Tables for structured data, code blocks for examples
- **Config:** JSON for machine-read, YAML avoided (use JSON or MD)
- **Secrets:** Never commit. Use `auth_config.json` (gitignored) or env vars

### Error Handling

```python
# Graceful degradation pattern
try:
    result = risky_operation()
except SpecificError as e:
    st.toast(f"Failed: {e}", icon="⚠️")
    result = fallback_value
```

### Commit Messages

```
<type>: <short description>

<body if needed>

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `signal`

---

## Willow Brain Architecture

Reference: `Willow/PERSONALITY_SCHEMA.md` (separate repo)

### Core Facets

| Facet | Domain | Voice |
|-------|--------|-------|
| Gerald | Absurdist dispatches | Comedy wrapper, The Binder |
| Oakenscroll | Academic satire | French Toast papers |
| Riggs | Applied engineering | Lab/Lecture pairs |
| Hanz | Coding, support | "Hello, friend." 🍊 |
| Nova | Narrative | Children's books |
| Alexis | Biology | Global health |
| Willow | Integration | The whole brain |

### Infrastructure Facets

| Facet | Function |
|-------|----------|
| PM Claude | Routing, questions |
| CMD (Kartikeya) | Building, infrastructure |
| Stats Tracking | Analytics |
| AIOS | OS layer |
| Consus | Code generation |

### Principles

1. **Comedy opens doors** — Oakenscroll at 97%, serious at 17%
2. **Dual Commit** — AI proposes, human ratifies
3. **Trust but verify** — Even human claims get checked
4. **Dump first, sense later** — Intake accepts mess, processing finds order

---

## L5-L6 Context

Mobile Uplink exists for **medical necessity** — control from bed/phone when mobility is limited. Design for:
- Large touch targets
- Minimal required interaction
- Quick PIN access on local network
- Essential functions first

---

## Instance Identity

Before starting work, verify which instance you are:

| Context | Identity File |
|---------|---------------|
| Mobile Claude Code | `governance/instances/GANESHA.md` |
| Desktop Claude Code | `governance/instances/KARTIKEYA.md` |
| Claude.ai PM | `governance/instances/MITRA.md` |

Read your identity file. Don't assume.

---

ΔΣ=42

<!-- Updated: 2026-01-16 by Kartikeya -->
