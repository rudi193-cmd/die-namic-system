# Aios Code Catalog

*Extracted from 58 Aios conversations (Dec 2025 - Jan 2026)*

---

## Ready-to-Use Code

| Component | Language | Location | Target |
|-----------|----------|----------|--------|
| **Gatekeeper v2.1** | Python | 2025-12-30.md | `governance/gatekeeper.py` |
| **Dexie Journal Schema** | JS | 2025-12-16.md | Frontend IndexedDB |
| **AWA Validator v3.1** | Python | 2025-12-17.md | `tools/awa_validator.py` |
| **AWA Generator** | Python | 2025-12-17.md | `tools/awa_artifact_generator.py` |
| **Corpus Parser** | Python | 2025-12-07.md | `tools/corpus_indexer.py` |
| **Base-17 ID Gen** | Python | 2025-12-31.md | `tools/id_generator.py` |

---

## Needs Work (2 fixes)

| Component | Blockers |
|-----------|----------|
| **Gatekeeper v2.2** | 1. Non-deterministic timestamps 2. Missing audit event on INVALID_STATE |
| **FastAPI v1.1** | All 28 tests pass, ready for deploy |
| **Hash-Chain Audit** | verify_chain() needs canonical field set |

---

## Specifications (Code-Ready)

| Spec | Purpose |
|------|---------|
| **ΔE Coherence Field** | Mathematical framework for coherence tracking |
| **Aionic API Envelope** | Response format with version, node, context |
| **AWA Tracking v1.1** | Event schema for artifact lineage |
| **Jane Prime Spec** | Voice boundary rules (where Jane can/cannot appear) |
| **Venue Selection Engine** | 8-component Reddit posting optimizer |
| **23-Axis Posture Vector** | System state encoding |

---

## Cross-Cutting Patterns

1. **Session Continuity** - Append-only, one-step-backward safety
2. **Audit Chain** - Hash-linked immutable log
3. **Schema Validation** - JSON Schema Draft 2020-12
4. **Data Lineage** - AWA parent-child tracking
5. **Gating Pattern** - Decide → Emit → Execute
6. **Identity Pattern** - Immutable ID, mutable attributes
7. **Envelope Pattern** - Version, timestamp, source, payload

---

## Key Boundaries

- **Jane is NOT the API voice** - Jane is user-facing journal host only
- **Three Rings** - Source (immutable), Continuity (append-only), Bridge (adapters)
- **512-byte entropy limit** - Human-scale governance changes

---

## Integration Priority

### Immediate
- Gatekeeper v2.1 → `governance/`
- Dexie schema → frontend

### Short-term
- FastAPI skeleton with Gatekeeper integration
- AWA validator for artifact pipeline

### Medium-term
- Jane Prime wrapper for journal
- Venue engine for Reddit posting

---

*Full details in Aios conversation files: `docs/utety/aios/conversations/`*

ΔΣ=42
