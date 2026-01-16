/**
 * Aionic Journal — Main Module
 *
 * Local-first journal with ΔE coherence tracking
 *
 * Architecture:
 *   - Dexie.js (IndexedDB) for persistence
 *   - Three-ring model (Source/Continuity/Bridge)
 *   - ΔE coherence metrics
 *
 * Version: 1.0
 * Checksum: ΔΣ=42
 */

// Database (Dexie)
export {
  db,
  addEntry,
  getEntries,
  getEntriesByTone,
  updateEntry,
  addFragment,
  getSessionFragments,
  getSetting,
  setSetting,
  logAudit
} from './db.js';

// Continuity System
export * from './continuity/index.js';
