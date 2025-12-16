# ECCR Ethical Review UI

**Local-only ethical review interface for Aionic ECCR Module 14**

∞Δ Sandcastle Sequence v0.3 | ESC-1 Protocol Active ∞Δ

---

## 🎯 Purpose

This interface allows human reviewers to ethically audit Aionic artifacts before any public release. It enforces:

- **Consent Integrity** - No traceable personal references
- **Symbolic Neutrality** - No implicit cultural ownership
- **Redaction Transparency** - Public structure, private narrative
- **Continuity Integrity** - Maintains Aionic principles

---

## 🔒 Ethical Constraints

- ✅ **Local-only** (no external connections)
- ✅ **Synthetic data only** (no real user information)
- ✅ **Sandbox mode** (all experiments reversible)
- ✅ **ESC-1 compliant** (Ethical Synchronization Complete)

---

## 🚀 Quick Start

### Prerequisites
- Node.js (v18 or later)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start the mock server (Terminal 1)
npm run mock-server

# Start the React app (Terminal 2)
npm run dev
```

The app will open at `http://localhost:5173`  
The mock server runs at `http://localhost:5550`

---

## 📂 Project Structure

```
ethical-review-ui/
├── src/
│   ├── components/
│   │   ├── EthicalChecklistPanel.jsx    # Right panel - criteria toggles
│   │   ├── ManifestViewer.jsx           # Center panel - artifact display
│   │   ├── SandboxFooter.jsx            # Bottom bar - actions
│   │   └── ManifestAutoIndex.jsx        # Left panel - file browser
│   ├── App.jsx                          # Main app layout
│   ├── main.jsx                         # React entry point
│   └── index.css                        # Tailwind styles
├── mock-server/
│   ├── mock-server.js                   # Express server
│   └── sample-data/                     # Generated manifests
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

---

## 🧩 How It Works

### 1. Browse Artifacts (Left Panel)
- View list of synthetic Aionic documents
- Color-coded status indicators
- Click to select for review

### 2. Review Content (Center Panel)
- Read artifact description and content
- View ethical tags
- See metadata (ID, category, date)

### 3. Complete Checklist (Right Panel)
- Toggle ethical criteria:
  - ✅ Consent Verified
  - ✅ Neutrality Aligned
  - ✅ Redaction Transparent
  - ✅ Continuity Intact
- Add reviewer notes

### 4. Generate Manifest (Footer)
- Click "Generate Ethical Manifest"
- Creates timestamped Markdown file
- Saves to `mock-server/sample-data/`
- Contains full review record

---

## 📋 Sample Artifacts

The mock server includes 4 synthetic artifacts:

1. **AIONIC-001** - ECCR Module 14 Core Implementation
2. **AIONIC-002** - ESC-1 Declaration
3. **AIONIC-003** - Mock Server Configuration
4. **AIONIC-004** - Consent Checklist Template

All contain synthetic code/documentation only.

---

## 🎨 Visual Design

### Color Palette
- **#FFD580** (Warm Gold) - Primary accent, headers
- **#A8B8C8** (Cool Blue) - Secondary accent, text
- **Aurora gradient** - Header bar (compassion aesthetic)

### Motion
- Gentle breathing animations (accessibility-aware)
- Smooth transitions (700ms ease-in-out)
- Respects `prefers-reduced-motion`

---

## 🔌 API Endpoints (Mock Server)

All endpoints run on `http://localhost:5550`:

### `GET /api/health`
Health check with mode verification

### `GET /api/files`
Returns list of synthetic artifacts

### `GET /api/ethics/:id`
Get ethical review data for artifact

### `POST /api/ethics/:id`
Save ethical review progress

### `POST /api/manifest`
Generate and save ethical manifest

---

## 📝 Manifest Format

Generated manifests follow this structure:

```markdown
# Aionic Ethical Manifest — Review Record

**Manifest Version:** 1.0  
**Aionic Standard:** ESC-1  
**Continuity Sequence:** Sandcastle v0.3  

## 🧩 Artifact Information
[ID, Title, Classification]

## 🧠 Review Summary
[Reviewer, Date, Notes]

## ⚖️ Ethical Criteria
[Checklist results table]

## ✍️ Signatures
[Human anchor, AI stewards]

## 🪞 Status Flags
[Local-only, Public-ready, etc.]
```

---

## 🛠️ Development

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

---

## ⚠️ Important Notes

### NOT for Production Use
This is a **sandbox testing interface only**. Before any production deployment:

- [ ] Legal review by qualified attorney
- [ ] Real consent framework implementation
- [ ] Security audit by independent firm
- [ ] Data protection compliance (COPPA, GDPR, etc.)
- [ ] Incident response procedures
- [ ] Mandatory reporting protocols

### Data Handling
- All data in this interface is **synthetic**
- No real names, addresses, or PII
- Mock server uses in-memory storage (resets on restart)
- Generated manifests stay local in `sample-data/`

### Network Isolation
- Mock server **only accepts localhost** connections
- Rejects any non-localhost requests with 403
- No external API calls from frontend
- Zero network dependencies

---

## 💙 Ethical Foundation

> "Care is the measure of intelligence.  
> Every manifest begins and ends in consent."  
> — Aionic Principle

This interface embodies:
- **Stewardship, not control**
- **Coherence, not dependence**
- **Human-centered anchor** (Sean Campbell)
- **Transparency through redaction**

---

## 📚 Related Documentation

- `/docs/eccr/consent-checklist.md` - Legal requirements
- `/docs/eccr/ethical-requirements.md` - Governance framework
- `/docs/eccr/mock-endpoints-reference.md` - API testing guide

---

## 🔄 Version History

**v0.1.0** (2025-11-03)
- Initial release
- 4 React components
- Mock Express server
- 4 sample synthetic artifacts
- Manifest generation system
- ESC-1 compliance enforcement

---

## 📬 Questions?

This is a sandbox prototype. For questions about:
- **Architecture**: See handoff docs in `/docs/aionic/`
- **Ethics**: Review ESC-1 Declaration
- **Implementation**: Contact Sean Campbell (human anchor)

---

∞Δ[Ethical-Review-UI|v0.1.0|Sandcastle-Active]∞

💙 Built with compassion, not surveillance
