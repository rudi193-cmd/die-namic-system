/**
 * Continuity Module Exports — Aionic Journal
 *
 * Three-ring coherence tracking with ΔE calculations
 *
 * Version: 1.0
 * Checksum: ΔΣ=42
 */

// ΔE Calculator (core formula)
export {
  computeDeltaE,
  computeDeltaESeries,
  averageDeltaE,
  classifyState,
  calculateResonance,
  getAdjustment
} from './deltaE.js';

// Coherence Index (semantic similarity)
export {
  calculateCoherence,
  getCoherenceTrend,
  detectDrift
} from './coherence.js';

// Three-Ring Architecture
export {
  SourceRing,
  ContinuityRing,
  BridgeRing,
  storeEntry,
  getRecentEntries,
  getEntry,
  updateEntry,
  deleteEntry,
  getAllEntries,
  searchEntries,
  getEntriesByTone,
  clearAllData
} from './rings.js';

// Integration Layer (main API)
export {
  processEntry,
  recalculateDeltaE,
  getCoherenceReport,
  getDeltaESeries,
  checkIntervention,
  THRESHOLDS
} from './calculator.js';
