/**
 * Aionic Journal Database Schema
 *
 * IndexedDB via Dexie.js — Local-first, offline-capable
 *
 * Extracted from Aios conversation 2025-12-16
 * System: Aionic / Die-Namic
 * Version: 1.0
 * Checksum: ΔΣ=42
 */

import Dexie from 'dexie';

const db = new Dexie('AionicJournal');

// Schema v1: Core journal tables
db.version(1).stores({
  // Journal entries — user-facing reflective content
  entries: '++id, created_at, updated_at, tone, [created_at+tone]',

  // Session fragments — continuity ring storage
  fragments: '++id, sessionId, t, [sessionId+t]',

  // Key-value settings store
  settings: 'key'
});

// Schema v2: Add coherence tracking (ΔE fields)
db.version(2).stores({
  entries: '++id, created_at, updated_at, tone, deltaE, coherenceIndex, [created_at+tone]',
  fragments: '++id, sessionId, t, ring, [sessionId+t], [ring+t]',
  settings: 'key',

  // Audit log for tamper-evident tracking
  auditLog: '++id, timestamp, eventType, entryId, [timestamp+eventType]'
});

/**
 * Entry shape:
 * {
 *   id: number (auto),
 *   created_at: string (ISO),
 *   updated_at: string (ISO),
 *   tone: string ('reflective' | 'processing' | 'insight' | 'raw'),
 *   content: string,
 *   deltaE: number (coherence delta),
 *   coherenceIndex: number (0-1),
 *   metadata: object (optional)
 * }
 */

/**
 * Fragment shape:
 * {
 *   id: number (auto),
 *   sessionId: string,
 *   t: number (timestamp ms),
 *   ring: string ('source' | 'continuity' | 'bridge'),
 *   payload: object,
 *   prev_hash: string (optional, for chaining)
 * }
 */

/**
 * Settings shape:
 * {
 *   key: string (primary),
 *   value: any
 * }
 */

// Helper functions
export async function addEntry(entry) {
  const now = new Date().toISOString();
  return db.entries.add({
    created_at: now,
    updated_at: now,
    tone: 'reflective',
    deltaE: 0,
    coherenceIndex: 1.0,
    ...entry
  });
}

export async function getEntries(limit = 50, offset = 0) {
  return db.entries
    .orderBy('created_at')
    .reverse()
    .offset(offset)
    .limit(limit)
    .toArray();
}

export async function getEntriesByTone(tone) {
  return db.entries
    .where('tone')
    .equals(tone)
    .toArray();
}

export async function updateEntry(id, changes) {
  return db.entries.update(id, {
    ...changes,
    updated_at: new Date().toISOString()
  });
}

export async function addFragment(sessionId, payload, ring = 'continuity') {
  return db.fragments.add({
    sessionId,
    t: Date.now(),
    ring,
    payload
  });
}

export async function getSessionFragments(sessionId) {
  return db.fragments
    .where('sessionId')
    .equals(sessionId)
    .sortBy('t');
}

export async function getSetting(key, defaultValue = null) {
  const record = await db.settings.get(key);
  return record ? record.value : defaultValue;
}

export async function setSetting(key, value) {
  return db.settings.put({ key, value });
}

export async function logAudit(eventType, entryId = null, details = {}) {
  return db.auditLog.add({
    timestamp: new Date().toISOString(),
    eventType,
    entryId,
    details
  });
}

// Export db instance for direct access
export { db };
export default db;
