// Jane's Story Engine
// Orchestrates LLM, coherence tracking, and narrative generation

import { generateJaneResponse } from '../ai/geminiClient.js';
import { scoreCoherence } from '../ai/scoreCoherence.js';
import { buildNarrativePrompt, buildOpeningScenePrompt } from '../ai/prompts.js';
import { getRecentFragments, storeFragment } from '../continuity/rings.js';
import { computeDeltaE, calculateResonance } from '../continuity/deltaE.js';

/**
 * Generate opening scene for new adventure
 * @param {Object} params - Scene parameters
 * @param {Object} params.setup - Adventure setup
 * @param {Array<string>} params.playerNames - Player names
 * @param {string} params.sessionId - Session ID
 * @returns {Promise<Object>} - Opening scene data
 */
export async function generateOpeningScene({ setup, playerNames, sessionId }) {
  try {
    console.log('[STORY ENGINE] Generating opening scene...');
    
    // Build prompt for opening
    const prompt = buildOpeningScenePrompt(setup, playerNames);
    
    // Generate with Gemini
    const narrative = await generateJaneResponse(prompt);
    
    // Create initial fragment
    const fragment = {
      sessionId,
      text: narrative,
      C: 0.6, // Neutral starting coherence
      R: 1.0,
      ΔE: 0,
      t: Date.now(),
      type: 'opening',
      anchors: ['opening_scene']
    };
    
    // Store in continuity
    storeFragment(fragment);
    
    console.log('[STORY ENGINE] Opening scene generated successfully');
    
    return {
      narrative,
      fragment,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('[STORY ENGINE] Error generating opening scene:', error);
    throw error;
  }
}

/**
 * Handle player input and generate narrative response
 * @param {Object} params - Input parameters
 * @param {string} params.sessionId - Session ID
 * @param {string} params.playerAction - Player's action
 * @param {Object} params.adventureSetup - Adventure context
 * @param {string} params.emotionalState - Detected emotional state
 * @param {Object} params.rollOutcome - Dice roll outcome (if applicable)
 * @returns {Promise<Object>} - Narrative response with metrics
 */
export async function handlePlayerInput({
  sessionId,
  playerAction,
  adventureSetup = {},
  emotionalState = 'calm',
  rollOutcome = null
}) {
  try {
    console.log('[STORY ENGINE] Processing player input:', playerAction);
    
    // Get recent fragments for context
    const recentFragments = getRecentFragments(sessionId, 5);
    
    // Calculate resonance based on emotional state
    const R = calculateResonance({ emotionalState });
    
    // Build prompt with full context
    const prompt = buildNarrativePrompt({
      recentFragments,
      playerAction,
      adventureSetup,
      ΔE: recentFragments.length > 0 ? recentFragments[recentFragments.length - 1].ΔE : 0,
      rollOutcome
    });
    
    // Generate narrative with Gemini
    const narrative = await generateJaneResponse(prompt);
    
    // Score coherence against recent history
    const coherenceResult = await scoreCoherence(narrative, recentFragments);
    
    // Calculate ΔE if we have previous coherence
    let deltaE = 0;
    if (recentFragments.length > 0) {
      const lastFragment = recentFragments[recentFragments.length - 1];
      deltaE = computeDeltaE({
        Cprev: lastFragment.C,
        tPrev: lastFragment.t,
        Cnow: coherenceResult.score,
        tNow: Date.now(),
        R
      });
    }
    
    // Create new fragment
    const fragment = {
      sessionId,
      text: narrative,
      C: coherenceResult.score,
      R,
      ΔE: deltaE,
      t: Date.now(),
      embedding: coherenceResult.embedding,
      type: rollOutcome ? 'roll_resolution' : 'narrative',
      emotionalState,
      playerAction,
      anchors: extractAnchors(narrative, adventureSetup)
    };
    
    // Store in continuity
    storeFragment(fragment);
    
    console.log('[STORY ENGINE] Narrative generated:', {
      coherence: coherenceResult.score.toFixed(3),
      deltaE: deltaE.toFixed(4),
      emotionalState
    });
    
    return {
      narrative,
      coherence: coherenceResult.score,
      deltaE,
      emotionalState,
      fragment,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('[STORY ENGINE] Error handling player input:', error);
    throw error;
  }
}

/**
 * Generate narrative for dice roll outcome
 * @param {Object} params - Roll parameters
 * @param {string} params.sessionId - Session ID
 * @param {string} params.action - Action being attempted
 * @param {string} params.stat - Stat being rolled
 * @param {number} params.rollTotal - Dice total (2d6)
 * @param {Object} params.adventureSetup - Adventure context
 * @returns {Promise<Object>} - Roll resolution narrative
 */
export async function resolveRoll({
  sessionId,
  action,
  stat,
  rollTotal,
  adventureSetup = {}
}) {
  try {
    console.log('[STORY ENGINE] Resolving roll:', { action, stat, rollTotal });
    
    // Determine outcome (PBtA style)
    let outcome;
    if (rollTotal >= 10) {
      outcome = 'full_success';
    } else if (rollTotal >= 7) {
      outcome = 'partial_success';
    } else {
      outcome = 'miss';
    }
    
    // Use story engine to generate outcome narrative
    const result = await handlePlayerInput({
      sessionId,
      playerAction: action,
      adventureSetup,
      emotionalState: 'calm', // Rolls are usually neutral emotionally
      rollOutcome: {
        outcome,
        total: rollTotal,
        stat
      }
    });
    
    return {
      ...result,
      outcome,
      rollTotal,
      stat
    };
  } catch (error) {
    console.error('[STORY ENGINE] Error resolving roll:', error);
    throw error;
  }
}

/**
 * Extract narrative anchors (key elements) from text
 * Anchors help maintain continuity across fragments
 * @param {string} text - Narrative text
 * @param {Object} setup - Adventure setup
 * @returns {Array<string>} - List of anchors
 */
function extractAnchors(text, setup) {
  const anchors = [];
  
  // Add setup-based anchors
  if (setup.where) anchors.push(`location:${setup.where.toLowerCase().substring(0, 20)}`);
  if (setup.goal) anchors.push(`goal:${setup.goal.toLowerCase().substring(0, 20)}`);
  
  // Simple keyword extraction (can be enhanced with NLP)
  const keywords = text
    .toLowerCase()
    .match(/\b[a-z]{4,}\b/g) // Words 4+ chars
    ?.filter((word, index, self) => self.indexOf(word) === index) // Unique
    ?.slice(0, 5) // Top 5
    || [];
  
  keywords.forEach(kw => anchors.push(`keyword:${kw}`));
  
  return anchors;
}

/**
 * Get story engine health/statistics
 * @param {string} sessionId - Session ID
 * @returns {Object} - Engine statistics
 */
export function getStoryEngineStats(sessionId) {
  const fragments = getRecentFragments(sessionId, 20);
  
  if (fragments.length === 0) {
    return {
      sessionId,
      fragmentCount: 0,
      averageCoherence: 0,
      averageDeltaE: 0,
      trend: 'new_session'
    };
  }
  
  const avgC = fragments.reduce((sum, f) => sum + (f.C || 0), 0) / fragments.length;
  const avgDE = fragments.reduce((sum, f) => sum + (f.ΔE || 0), 0) / fragments.length;
  
  let trend;
  if (avgDE > 0.05) trend = 'regenerative';
  else if (avgDE < -0.05) trend = 'decaying';
  else trend = 'stable';
  
  return {
    sessionId,
    fragmentCount: fragments.length,
    averageCoherence: avgC,
    averageDeltaE: avgDE,
    trend,
    oldestFragment: fragments[0]?.t,
    newestFragment: fragments[fragments.length - 1]?.t
  };
}
