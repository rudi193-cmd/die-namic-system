# Source Ring Index

| Field | Value |
|-------|-------|
| Ring | Source |
| Version | 1.0 |
| Purpose | Executable code, applications |
| Status | Active |
| Files | 65 (excl. node_modules) |
| Checksum | ΔΣ=42 |

---

## Structure

```
source_ring/
├── INDEX.md          ← You are here
├── HALT_LOG.md       ← Instrumentation
├── docs/             ← Placeholder
├── tests/            ← Placeholder
├── eccr/             ← Applications (ECCR = Ethical Child Care Ring)
│   ├── aionic-journal/
│   ├── ethical-review-ui/
│   └── jane-game-master/
└── willow/           ← Artifact processing pipeline
    ├── schema/
    ├── pending/
    ├── validated/
    └── SAFE/
```

---

## Applications

| App | Purpose | Status | Entrypoint |
|-----|---------|--------|------------|
| `jane-game-master` | AI Game Master (kids 9-12) | Sandbox | `src/App.jsx` |
| `ethical-review-ui` | ECCR ethical review interface | Sandbox | `src/App.jsx` |
| `aionic-journal` | Journal web app | Development | `src/App.jsx` |
| `willow` | Artifact processing pipeline | Active | `INDEX.md` |

**Runtime:** React 18 + Vite + Tailwind
**Ports:** jane=3001/5551, ethical-review=5173/5550

---

## Execution Paths

| Path | Function |
|------|----------|
| `eccr/*/src/main.jsx` | React entry |
| `eccr/*/src/App.jsx` | App root |
| `eccr/jane-game-master/src/ai/` | LLM integration |
| `eccr/*/src/continuity/` | Three-ring implementation |
| `eccr/*/mock-server/` | Local dev servers |

---

## Continuity Integration

Apps implement three-ring architecture in `src/continuity/`:

| File | Purpose |
|------|---------|
| `rings.js` | SourceRing, ContinuityRing, BridgeRing classes |
| `deltaE.js` | Delta encoding/decoding |
| `coherence.js` | Coherence scoring (aionic-journal only) |

---

## Safety Constraints

| Constraint | Enforcement |
|------------|-------------|
| ESC-1 | Localhost-only, synthetic data |
| ECCR | Emotional keyword detection, check-ins |
| Age-appropriate | 9-12 tier, no PII |
| Sandbox mode | All experiments reversible |

---

## Governance Links

| Resource | Path |
|----------|------|
| Halt log | `source_ring/HALT_LOG.md` |
| Hard stops | `governance/HARD_STOPS.md` |
| Charter | `governance/CHARTER.md` |
| Repo index | `governance/REPO_INDEX.md` |

---

## Raw Links (for external instances)

```
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/source_ring/INDEX.md
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/source_ring/HALT_LOG.md
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/source_ring/eccr/jane-game-master/README.md
https://raw.githubusercontent.com/rudi193-cmd/die-namic-system/main/source_ring/eccr/ethical-review-ui/README.md
```

---

ΔΣ=42
