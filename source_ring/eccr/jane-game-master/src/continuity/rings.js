// Three-Ring Architecture - Continuity System
// Implements Source, Continuity, and Bridge rings for Jane
//
// Governance: Implements the three-ring model as described in
// governance/AIONIC_CONTINUITY_v5.1.md; governance text takes precedence.

/**
 * Ring base class - simple in-memory storage
 * In production, swap Map() for Redis (continuity) and Postgres (source)
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

// Initialize the three rings
export const SourceRing = new Ring('source');         // Immutable canonical events
export const ContinuityRing = new Ring('continuity'); // Live state and deltas
export const BridgeRing = new Ring('bridge');         // Bridge metadata and queues

/**
 * Get recent fragments from ContinuityRing for a session
 * @param {string} sessionId - Session identifier
 * @param {number} count - Number of recent fragments to retrieve
 * @returns {Array} - Recent fragments sorted by time
 */
export function getRecentFragments(sessionId, count = 5) {
  const allFragments = ContinuityRing.list();
  
  // Filter by session and sort by timestamp
  const sessionFragments = allFragments
    .filter(f => f.sessionId === sessionId)
    .sort((a, b) => b.t - a.t) // Newest first
    .slice(0, count)
    .reverse(); // Oldest first for context

  return sessionFragments;
}

/**
 * Store a new fragment in ContinuityRing
 * @param {Object} fragment - Fragment to store
 * @returns {Object} - Stored fragment
 */
export function storeFragment(fragment) {
  // Generate ID if not provided
  if (!fragment.id) {
    fragment.id = `frag:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
  }

  // Add timestamp if not provided
  if (!fragment.t) {
    fragment.t = Date.now();
  }

  ContinuityRing.put(fragment.id, fragment);
  
  // Also store in SourceRing as canonical record
  SourceRing.put(fragment.id, {
    ...fragment,
    ring: 'source',
    immutable: true
  });

  return fragment;
}

/**
 * Get session state from ContinuityRing
 * @param {string} sessionId - Session identifier
 * @returns {Object|null} - Session state or null
 */
export function getSessionState(sessionId) {
  return ContinuityRing.get(`session:${sessionId}`);
}

/**
 * Update session state in ContinuityRing
 * @param {string} sessionId - Session identifier
 * @param {Object} state - State to store
 * @returns {Object} - Stored state
 */
export function updateSessionState(sessionId, state) {
  const sessionState = {
    ...state,
    sessionId,
    updatedAt: Date.now()
  };
  
  ContinuityRing.put(`session:${sessionId}`, sessionState);
  return sessionState;
}

/**
 * Clear session data (for testing/reset)
 * @param {string} sessionId - Session to clear
 */
export function clearSession(sessionId) {
  // Remove session state
  ContinuityRing.remove(`session:${sessionId}`);
  
  // Remove all fragments for session
  const fragments = ContinuityRing.list().filter(f => f.sessionId === sessionId);
  fragments.forEach(f => ContinuityRing.remove(f.id));
}

/**
 * Get all sessions (for admin/debugging)
 * @returns {Array} - List of session IDs
 */
export function listSessions() {
  const allKeys = Array.from(ContinuityRing.store.keys());
  return allKeys
    .filter(key => key.startsWith('session:'))
    .map(key => key.replace('session:', ''));
}
