/**
 * ΔE Coherence Calculator — Integration Module
 *
 * Connects deltaE.js calculations with db.js persistence
 *
 * Aios Spec (2025-12-10):
 *   "ΔE: coherence metric (positive = stabilizing, negative = chaotic)"
 *   - ΔE > 0 → Regenerative expansion
 *   - ΔE ≈ 0 → Stable maintenance
 *   - ΔE < 0 → Structural decay or overload
 *
 * Author: Kartikeya (implemented from Aios spec)
 * Version: 1.0
 * Checksum: ΔΣ=42
 */

import { db, addEntry, getEntries, updateEntry, logAudit } from '../db.js';
import { computeDeltaE, classifyState, getAdjustment, calculateResonance, averageDeltaE } from './deltaE.js';
import { calculateCoherence, detectDrift, getCoherenceTrend } from './coherence.js';

/**
 * Default coherence window size (entries to consider for context)
 */
const COHERENCE_WINDOW = 5;

/**
 * ΔE state thresholds from Aios spec
 */
const THRESHOLDS = {
  REGENERATIVE: 0.05,    // ΔE > 0.05 = actively improving
  DECAYING: -0.05,       // ΔE < -0.05 = actively degrading
  CRITICAL: -0.2         // ΔE < -0.2 = needs intervention
};

/**
 * Process a new journal entry with coherence tracking
 *
 * @param {Object} entry - New entry to process
 * @param {string} entry.title - Entry title
 * @param {string} entry.body - Entry body text
 * @param {string} entry.tone - Tone classification
 * @param {Object} context - Optional context for resonance calculation
 * @returns {Object} - Processed entry with coherence metrics
 */
export async function processEntry(entry, context = {}) {
  // Get recent entries for coherence calculation
  const recentEntries = await getEntries(COHERENCE_WINDOW);

  // Calculate coherence index (Cᵢ) against recent entries
  const coherenceIndex = calculateCoherence(entry, recentEntries);

  // Get previous entry for ΔE calculation
  const prevEntry = recentEntries[0];

  // Calculate ΔE if we have history
  let deltaE = 0;
  let state = 'stable';

  if (prevEntry) {
    const R = calculateResonance(context);

    deltaE = computeDeltaE({
      Cprev: prevEntry.coherenceIndex || 0.6,
      tPrev: new Date(prevEntry.created_at).getTime(),
      Cnow: coherenceIndex,
      tNow: Date.now(),
      R
    });

    state = classifyState(deltaE);
  }

  // Assemble entry with metrics
  const processedEntry = {
    ...entry,
    coherenceIndex,
    deltaE,
    state,
    processedAt: new Date().toISOString()
  };

  // Persist to database
  const entryId = await addEntry(processedEntry);

  // Log to audit trail
  await logAudit('entry_created', entryId, {
    coherenceIndex,
    deltaE,
    state,
    prevEntryId: prevEntry?.id || null
  });

  // Check for drift and log warning if detected
  if (prevEntry && detectDrift([prevEntry, processedEntry])) {
    await logAudit('drift_detected', entryId, {
      delta: Math.abs(coherenceIndex - (prevEntry.coherenceIndex || 0.6)),
      recommendation: getAdjustment(deltaE)
    });
  }

  return {
    id: entryId,
    ...processedEntry,
    adjustment: getAdjustment(deltaE)
  };
}

/**
 * Recalculate ΔE for an existing entry (after context changes)
 *
 * @param {number} entryId - Entry ID to recalculate
 * @param {Object} context - Context for resonance
 * @returns {Object} - Updated entry metrics
 */
export async function recalculateDeltaE(entryId, context = {}) {
  const entries = await getEntries(COHERENCE_WINDOW + 1);

  // Find the target entry and its predecessor
  const entryIndex = entries.findIndex(e => e.id === entryId);
  if (entryIndex === -1) {
    throw new Error(`Entry ${entryId} not found`);
  }

  const entry = entries[entryIndex];
  const prevEntry = entries[entryIndex + 1]; // Older entry

  if (!prevEntry) {
    return { deltaE: 0, state: 'stable', message: 'No previous entry' };
  }

  const R = calculateResonance(context);

  const deltaE = computeDeltaE({
    Cprev: prevEntry.coherenceIndex || 0.6,
    tPrev: new Date(prevEntry.created_at).getTime(),
    Cnow: entry.coherenceIndex || 0.6,
    tNow: new Date(entry.created_at).getTime(),
    R
  });

  const state = classifyState(deltaE);

  // Update entry in database
  await updateEntry(entryId, { deltaE, state });

  // Log recalculation
  await logAudit('deltaE_recalculated', entryId, {
    oldDeltaE: entry.deltaE,
    newDeltaE: deltaE,
    resonance: R
  });

  return {
    entryId,
    deltaE,
    state,
    adjustment: getAdjustment(deltaE)
  };
}

/**
 * Get coherence report for recent history
 *
 * @param {number} windowSize - Number of entries to analyze
 * @returns {Object} - Coherence report
 */
export async function getCoherenceReport(windowSize = 10) {
  const entries = await getEntries(windowSize);

  if (entries.length === 0) {
    return {
      status: 'no_data',
      message: 'No entries to analyze',
      trend: 'unknown',
      averageDeltaE: 0,
      recommendation: 'Start journaling to build coherence history'
    };
  }

  // Extract ΔE values
  const deltaEs = entries
    .map(e => e.deltaE)
    .filter(de => de !== undefined && de !== null);

  const avgDeltaE = averageDeltaE(deltaEs, Math.min(5, deltaEs.length));
  const trend = getCoherenceTrend(entries);
  const currentState = classifyState(avgDeltaE);

  // Build report
  const report = {
    status: currentState,
    trend,
    averageDeltaE: Math.round(avgDeltaE * 1000) / 1000,
    entryCount: entries.length,
    latestCoherence: entries[0]?.coherenceIndex || null,
    latestDeltaE: entries[0]?.deltaE || null,
    adjustment: getAdjustment(avgDeltaE)
  };

  // Add warnings if needed
  if (avgDeltaE < THRESHOLDS.CRITICAL) {
    report.warning = 'Significant coherence decay detected';
    report.recommendation = 'Return to familiar themes, reduce complexity';
  } else if (avgDeltaE < THRESHOLDS.DECAYING) {
    report.warning = 'Coherence declining';
    report.recommendation = 'Consider grounding exercises or familiar content';
  }

  return report;
}

/**
 * Calculate ΔE series for visualization
 *
 * @param {number} count - Number of entries to include
 * @returns {Array} - Array of {timestamp, deltaE, coherenceIndex, state}
 */
export async function getDeltaESeries(count = 20) {
  const entries = await getEntries(count);

  return entries
    .reverse() // Oldest first for time series
    .map(entry => ({
      timestamp: entry.created_at,
      deltaE: entry.deltaE || 0,
      coherenceIndex: entry.coherenceIndex || 0.6,
      state: entry.state || classifyState(entry.deltaE || 0),
      tone: entry.tone
    }));
}

/**
 * Check if current state needs intervention
 *
 * @returns {Object} - Intervention status and recommendations
 */
export async function checkIntervention() {
  const report = await getCoherenceReport(5);

  const needsIntervention = report.averageDeltaE < THRESHOLDS.CRITICAL;

  return {
    needed: needsIntervention,
    severity: needsIntervention ? 'high' :
              report.averageDeltaE < THRESHOLDS.DECAYING ? 'moderate' : 'low',
    currentDeltaE: report.averageDeltaE,
    trend: report.trend,
    recommendation: report.adjustment?.description || 'Continue current approach'
  };
}

// Export thresholds for external use
export { THRESHOLDS };
