# Aionic Journal App Concept

**Source:** Biology Node threads, November 2025  
**Status:** On Hold  
**Domain:** Consumer app (journaling)

---

## Concept

Breath-synchronized journaling app that tracks ΔE (coherence) over time. Core principle: "Good enough and alive."

---

## Architecture

### Frontend (React/Vite)

```
src/
├── core/
│   ├── deltaE.js      — ΔE computation per entry
│   ├── rings.js       — Breath phase timing
│   └── bell.js        — Emotional gateway cues
├── hooks/
│   ├── useBreathCycle.js   — 4-second breath loop
│   └── useJournalState.js  — Entry state management
├── journal/
│   ├── Editor.jsx     — Text input with ΔE chip
│   ├── EntryCard.jsx  — Individual entry display
│   └── Shell.jsx      — Entry list container
├── ui/
│   ├── Layout.jsx     — App wrapper
│   └── BreathRing.jsx — Visual breathing indicator
├── pages/
│   ├── Page1Home.jsx  — Welcome screen
│   ├── Page2Consent.jsx — Consent gateway
│   └── Page3Journal.jsx — Main journaling view
└── services/
    └── storage.js     — Local persistence
```

---

## Key Features

### Breath Ring
Visual breathing indicator synced to 4-second cycle. Color/animation adapts to ΔE state.

### ΔE Computation
```javascript
function computeDeltaE(entryText, breathData) {
  const lengthFactor = Math.min(entryText.length / 500, 1);
  const breathFactor = breathData?.coherence ?? 0.5;
  return (lengthFactor + breathFactor) / 2;
}
```

### Consent Gateway
Page2Consent: Local storage only, user-controlled clearing, no upload.

### Emotional Modes
```javascript
function emotional_mode(delta_e) {
  if (delta_e < -0.3) return "calm";
  if (delta_e > 0.3) return "uplift";
  return "neutral";
}
```

---

## UI Adaptation

| ΔE Range | Theme | Bell Message |
|----------|-------|--------------|
| < -0.3 | Soothing/blue | "Breathe..." |
| -0.3 to 0.3 | Default/gray | "Write what emerges..." |
| > 0.3 | Bright/gold | "You're flowing..." |

---

## Target

December 2025 (original). Status: On hold.

---

## Note

React scaffolding was drafted but not deployed. App concept connects to broader Aionic System through ΔE tracking and coherence visualization.

---

ΔΣ=42
