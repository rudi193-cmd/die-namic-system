// Three-Ring Architecture - Aionic Journal Continuity System
// Adapted from Die-namic Framework v1.42

/**
 * Ring base class - in-memory storage
 * Production: Replace Map() with IndexedDB via Dexie
 */
class Ring {
  constructor(name) {
    this.name = name;
    this.store = new Map();
  }

  put(id, payload) {
    this.store.set(id, payload);
    return payload;
  }

  get(id) {
    return this.store.get(id);
  }

  list() {
    return Array.from(this.store.values());
  }

  remove(id) {
    this.store.delete(id);
  }

  clear() {
    this.store.clear();
  }

  size() {
    return this.store.size;
  }
}

// Initialize three rings
export const SourceRing = new Ring('source');         // Immutable journal entries
export const ContinuityRing = new Ring('continuity'); // Live state & fragments
export const BridgeRing = new Ring('bridge');         // Metadata & queues

/**
 * Store journal entry in rings
 */
export function storeEntry(entry) {
  if (!entry.id) {
    entry.id = `entry:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
  }

  if (!entry.created_at) {
    entry.created_at = new Date().toISOString();
  }

  entry.updated_at = new Date().toISOString();

  // Store in ContinuityRing (live)
  ContinuityRing.put(entry.id, entry);
  
  // Store in SourceRing (canonical)
  SourceRing.put(entry.id, {
    ...entry,
    ring: 'source',
    immutable: true
  });

  return entry;
}

/**
 * Get recent entries
 */
export function getRecentEntries(count = 5) {
  const allEntries = ContinuityRing.list()
    .filter(item => item.id && item.id.startsWith('entry:'))
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, count);

  return allEntries;
}

/**
 * Get entry by ID
 */
export function getEntry(id) {
  return ContinuityRing.get(id) || SourceRing.get(id);
}

/**
 * Update entry (creates new version in ContinuityRing)
 */
export function updateEntry(id, updates) {
  const existing = getEntry(id);
  if (!existing) return null;

  const updated = {
    ...existing,
    ...updates,
    updated_at: new Date().toISOString()
  };

  ContinuityRing.put(id, updated);
  return updated;
}

/**
 * Delete entry (soft delete - mark as deleted)
 */
export function deleteEntry(id) {
  const entry = getEntry(id);
  if (!entry) return null;

  const deleted = {
    ...entry,
    deleted: true,
    deleted_at: new Date().toISOString()
  };

  ContinuityRing.put(id, deleted);
  return deleted;
}

/**
 * Get all entries (excluding deleted)
 */
export function getAllEntries() {
  return ContinuityRing.list()
    .filter(item => 
      item.id && 
      item.id.startsWith('entry:') && 
      !item.deleted
    )
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
}

/**
 * Search entries by text
 */
export function searchEntries(query) {
  const lowerQuery = query.toLowerCase();
  
  return getAllEntries().filter(entry => 
    (entry.title && entry.title.toLowerCase().includes(lowerQuery)) ||
    (entry.body && entry.body.toLowerCase().includes(lowerQuery)) ||
    (entry.tags && entry.tags.some(tag => tag.toLowerCase().includes(lowerQuery)))
  );
}

/**
 * Get entries by tone
 */
export function getEntriesByTone(tone) {
  return getAllEntries().filter(entry => entry.tone === tone);
}

/**
 * Clear all data (for testing/reset)
 */
export function clearAllData() {
  ContinuityRing.clear();
  BridgeRing.clear();
  // SourceRing intentionally preserved (immutable archive)
}
