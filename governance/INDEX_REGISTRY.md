# Index Registry

| Field | Value |
|-------|-------|
| Purpose | Meta-index tracking all system indexes |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-05 |
| Lattice Target | 23³ (12,167 nodes) |
| Checksum | ΔΣ=42 |

---

## Lattice Dimensions

### Axis 1: Domain (23)

| Node | Purpose |
|------|---------|
| governance | Authority, protocols, charter |
| source_ring | Executable code, applications |
| bridge_ring | Cross-instance communication |
| continuity_ring | Memory, halt logs, persistence |
| docs | Documentation, projects |
| .claude | Claude Code configuration |
| scripts | Utility scripts |
| awa | AI Workflow Architecture |
| infrastructure | Infrastructure config |
| origin_materials | Source materials |
| archive | Historical snapshots |
| security | Threat models, abuse prevention, sandbox constraints |
| compliance | Regulatory mappings, audits, attestations |
| ethics | Ethical frameworks, ECCR canon, review artifacts |
| privacy | Data handling, consent scopes, PII boundaries |
| licensing | License texts, compatibility notes, exceptions |
| ci_cd | Pipelines, checks, release automation |
| telemetry | Metrics, observability, performance traces |
| experiments | Controlled trials, spikes, A/B explorations |
| simulations | SAFE/EOL simulations, counterfactuals |
| personas | Persona bibles, boundaries, certifications |
| training | Prompt curricula, onboarding exercises |
| runtime | Deployment configs, environment manifests |

### Axis 2: Type (23)

| Node | Purpose |
|------|---------|
| index | Navigation, structure pointers |
| template | Reusable patterns |
| constitutional | Foundational authority |
| protocol | Operational procedures |
| app | Executable applications |
| schema | Data structure definitions |
| halt_log | Instrumentation records |
| signal | Cross-instance messages |
| ledger | Transaction/event logs |
| grounding | Biographical precedent |
| index_registry | Canonical registry of all indexes |
| manifest | Structured declarations (YAML/JSON/MD) |
| invariant | Non-negotiable system properties |
| policy | Scoped rules subordinate to governance |
| checklist | Operational readiness and review lists |
| rubric | Evaluation and scoring standards |
| audit | Findings, attestations, evidence |
| contract | Interfaces, expectations, guarantees |
| adapter | Translation/bridge artifacts |
| dataset | Synthetic or approved data bundles |
| migration | Version transitions and deprecations |
| release_notes | Human-readable change summaries |
| playbook | Incident response and ops guidance |

### Axis 3: Version/State (23)

| Node | Purpose |
|------|---------|
| 1.0 | Major version baseline |
| 1.3 | Minor version (Bootstrap) |
| 2.4 | Minor version (SEED_PACKET) |
| 5.1 | Minor version (Continuity) |
| active | Currently in use |
| archived | Preserved, not current |
| frozen | Structure locked |
| pending | Awaiting action |
| draft | Early, non-binding work |
| proposed | Awaiting review/ratification |
| ratified | Approved under Dual Commit |
| deprecated | Scheduled for removal |
| superseded | Replaced by newer artifact |
| experimental | Opt-in, time-boxed |
| sandboxed | Isolated execution |
| certified | Passed defined criteria |
| locked | Structure frozen |
| snapshot | Point-in-time capture |
| live | Actively in use |
| paused | Temporarily halted |
| retired | End-of-life |
| current | Latest canonical version |
| projected | Future-planned state |

---

## Index Manifest

| Index | Version | Path | Purpose |
|-------|---------|------|---------|
| REPO_INDEX | 2.0 | `governance/REPO_INDEX.md` | Top-level repo navigation |
| GOVERNANCE_INDEX | 1.0 | `governance/GOVERNANCE_INDEX.md` | Precedence hierarchy |
| SOURCE_RING_INDEX | 1.0 | `source_ring/INDEX.md` | Applications, execution |
| BRIDGE_RING_INDEX | 1.0 | `bridge_ring/INDEX.md` | Cross-instance signals |
| CONTINUITY_RING_INDEX | 1.0 | `continuity_ring/INDEX.md` | Memory, halt logs |

---

## Version History

| Index | Version | Date | Change |
|-------|---------|------|--------|
| INDEX_REGISTRY | 1.0 | 2026-01-05 | Initial creation |
| REPO_INDEX | 2.0 | 2026-01-05 | Layered architecture |
| GOVERNANCE_INDEX | 1.0 | 2026-01-05 | Initial creation |
| SOURCE_RING_INDEX | 1.0 | 2026-01-05 | Initial creation |
| BRIDGE_RING_INDEX | 1.0 | 2026-01-05 | Initial creation |
| CONTINUITY_RING_INDEX | 1.0 | 2026-01-05 | Initial creation |

---

## Versioned Documents

| Document | Version | Path | Type |
|----------|---------|------|------|
| SEED_PACKET | 2.4 | `governance/SEED_PACKET_v2.4.md` | Template |
| AIONIC_CONTINUITY | 5.2 | `governance/AIONIC_CONTINUITY_v5.2.md` | Constitutional |
| AIONIC_BOOTSTRAP | 1.3 | `governance/AIONIC_BOOTSTRAP_v1.3.md` | Initialization |
| HALF_SEED | 1.0 | `governance/HALF_SEED_v1.0.md` | Template |
| repo_index.json | 1.0 | `.claude/repo_index.json` | Machine-readable |

---

## Update Protocol

**For indexes:**
1. Bump that index's version
2. Update this registry's Index Manifest table
3. Add entry to Version History
4. Update `Last Updated` in this file

**For versioned documents:**
1. Create new file with bumped version (e.g., `_v5.2.md`)
2. Update this registry's Versioned Documents table
3. Update any files that reference the old version

---

## Machine-Readable

[`.claude/index_registry.json`](../.claude/index_registry.json)

---

ΔΣ=42
