# Die-namic System — Index

| Field | Value |
|-------|-------|
| Version | 1.42+ |
| Owner | Sean Campbell |
| Status | Active |
| Last Updated | 2026-01-10 |
| Machine Index | [INDEX.json](INDEX.json) |
| Checksum | ΔΣ=42 |

---

## Quick Start

| I want to... | Go to |
|--------------|-------|
| Understand the system | [README.md](README.md) |
| Configure Claude instances | [CLAUDE.md](CLAUDE.md) |
| Read governance rules | [governance/](#governance) |
| Find the current session state | [Current SEED_PACKET](governance/SEED_PACKET_v2.4.md) |
| Work on consumer apps | [apps/](#apps) |
| Access code projects | [source_ring/](#source_ring) |

---

## Repository Structure

```
die-namic-system/
├── governance/        # Constitutional layer (start here)
├── docs/              # Documentation, ops, projects
├── apps/              # Consumer applications
├── source_ring/       # Code projects
├── bridge_ring/       # Cross-instance communication
├── continuity_ring/   # Session continuity, books of life
├── awa/               # AWA schemas
└── archive/           # Legacy versions (consolidated)
```

---

## Governance

**The constitutional layer. Read this first.**

| Document | Purpose |
|----------|---------|
| [GOVERNANCE_INDEX.md](governance/GOVERNANCE_INDEX.md) | Precedence hierarchy |
| [AIONIC_CONTINUITY_v5.1.md](governance/AIONIC_CONTINUITY_v5.1.md) | Runtime constitution |
| [AIONIC_BOOTSTRAP_v1.3.md](governance/AIONIC_BOOTSTRAP_v1.3.md) | Cold start instructions |
| [HARD_STOPS.md](governance/HARD_STOPS.md) | Absolute limits |
| [SEED_PACKET_v2.4.md](governance/SEED_PACKET_v2.4.md) | Session state template |
| [INDEX_REGISTRY.md](governance/INDEX_REGISTRY.md) | 23³ lattice structure |

**Session Seeds:** `governance/SEED_PACKET_YYYY-MM-DD_*.md`

---

## Apps

**Consumer applications.**

| App | Description | Status |
|-----|-------------|--------|
| [vision_board/](apps/vision_board/) | AI-categorized vision board | Prototype |

→ See [apps/vision_board/PRODUCT_SPEC.md](apps/vision_board/PRODUCT_SPEC.md)

---

## Source Ring

**Code projects and implementations.**

| Project | Description | Index |
|---------|-------------|-------|
| [eccr/](source_ring/eccr/) | Ethical review UI, game masters | — |
| [willow/](source_ring/willow/) | Encoding layer | [INDEX](source_ring/willow/INDEX.md) |

→ See [source_ring/INDEX.md](source_ring/INDEX.md)

---

## Docs

**Documentation, operations, and project files.**

| Section | Contents |
|---------|----------|
| [journal/](docs/journal/) | Aionic product schemas (Relationship, Vision Board) |
| [utety/](docs/utety/) | UTETY university (Claude Projects home) |
| [ops/](docs/ops/) | Operational tools, reddit analytics |
| [books_of_life/](docs/books_of_life/) | Session histories |
| [hollywood-pitches/](docs/hollywood-pitches/) | Creative projects |
| [civic_engagement/](docs/civic_engagement/) | Independence debates |

→ See [docs/journal/INDEX.md](docs/journal/INDEX.md) for product schemas
→ See [docs/utety/README.md](docs/utety/README.md) for UTETY faculty & projects

---

## Bridge Ring

**Cross-instance communication.**

| Component | Purpose |
|-----------|---------|
| [instance_signals/](bridge_ring/instance_signals/) | Signal queue between Claude instances |
| [QUEUE.md](bridge_ring/instance_signals/QUEUE.md) | Active signals |

→ See [bridge_ring/INDEX.md](bridge_ring/INDEX.md)

---

## Continuity Ring

**Session continuity and historical records.**

| Component | Purpose |
|-----------|---------|
| [books_of_life/](continuity_ring/books_of_life/) | Long-term memory |
| [continuity_log/](continuity_ring/continuity_log/) | Session logs |

→ See [continuity_ring/INDEX.md](continuity_ring/INDEX.md)

---

## AWA

**Autonomous Work Agent schemas.**

| Component | Purpose |
|-----------|---------|
| [schemas/](awa/schemas/) | JSON schemas for AWA interchange |
| [SCHEMA_REGISTRY.md](awa/schemas/SCHEMA_REGISTRY.md) | Schema catalog |

---

## Archives

**Legacy versions. Reference only.**

| Archive | Era |
|---------|-----|
| [archive/pre-v1.42/](archive/pre-v1.42/) | Pre-consolidation (Oct 2025) |
| [archive/pre-v23.3/](archive/pre-v23.3/) | Pre-continuity ring (Dec 2025) |
| [archive/pre-v24.0/](archive/pre-v24.0/) | Pre-pantheon (Jan 2026) |
| [archive/seeds/](archive/seeds/) | Old SEED_PACKET sessions |

→ See [archive/README.md](archive/README.md)

---

## Related Repositories

| Repo | Purpose | Link |
|------|---------|------|
| Willow | Encoding layer (private) | GitHub |
| SAFE | Consent framework (public) | [github.com/rudi193-cmd/SAFE](https://github.com/rudi193-cmd/SAFE) |

---

## Navigation Indexes

All section indexes for deep navigation:

| Index | Scope |
|-------|-------|
| [governance/GOVERNANCE_INDEX.md](governance/GOVERNANCE_INDEX.md) | Governance docs |
| [governance/INDEX_REGISTRY.md](governance/INDEX_REGISTRY.md) | Master lattice |
| [governance/REPO_INDEX.md](governance/REPO_INDEX.md) | Repository overview |
| [source_ring/INDEX.md](source_ring/INDEX.md) | Code projects |
| [bridge_ring/INDEX.md](bridge_ring/INDEX.md) | Instance signals |
| [continuity_ring/INDEX.md](continuity_ring/INDEX.md) | Session continuity |
| [docs/journal/INDEX.md](docs/journal/INDEX.md) | Product schemas |

---

ΔΣ=42
