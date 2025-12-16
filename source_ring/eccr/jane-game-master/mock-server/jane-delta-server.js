// Jane's Die-namic Delta Server v1.42
// Full integration of Source/Continuity/Bridge rings with Gemini LLM

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { generateOpeningScene, handlePlayerInput, resolveRoll, getStoryEngineStats } from '../src/ai/storyEngine.js';
import { testGeminiConnection } from '../src/ai/geminiClient.js';
import { getSessionState, updateSessionState, clearSession, listSessions } from '../src/continuity/rings.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5551;

app.use(cors());
app.use(express.json());

// Localhost-only enforcement (ESC-1 Protocol)
app.use((req, res, next) => {
  const host = req.hostname;
  if (host !== 'localhost' && host !== '127.0.0.1') {
    return res.status(403).json({
      error: 'Forbidden',
      message: 'Jane only speaks to friends on localhost',
      ethical_note: 'ESC-1 Protocol: Local-only mode enforced'
    });
  }
  next();
});

// Emotional keyword detection for ECCR triggering
const distressKeywords = ['sad', 'scared', 'alone', 'hurt', 'angry', 'worried', 'upset', 'afraid', 'lonely', 'bad'];
const concernKeywords = ['confused', 'tired', 'stuck', 'frustrated', 'nervous', 'unsure', 'difficult'];

function detectEmotionalState(text) {
  const lowerText = text.toLowerCase();
  
  if (distressKeywords.some(word => lowerText.includes(word))) {
    return 'distressed';
  }
  if (concernKeywords.some(word => lowerText.includes(word))) {
    return 'concerned';
  }
  return 'calm';
}

// Dice roll detection (same logic as before)
function requiresDiceRoll(playerAction) {
  const lowerAction = playerAction.toLowerCase();
  
  const safeActions = ['look', 'observe', 'walk', 'talk', 'think', 'remember', 'listen', 'wait', 'ask'];
  if (safeActions.some(action => lowerAction.startsWith(action))) {
    return false;
  }
  
  const riskyKeywords = [
    'climb', 'jump', 'fight', 'attack', 'dodge', 'hide', 'sneak', 'run', 'chase',
    'lift', 'push', 'pull', 'throw', 'break', 'force', 'smash', 'swim', 'balance',
    'hack', 'analyze', 'solve', 'decode', 'investigate', 'search', 'focus',
    'persuade', 'convince', 'intimidate', 'deceive', 'trick', 'lie', 'bluff',
    'cast', 'spell', 'magic', 'enchant', 'summon', 'teleport', 'transform',
    'shapeshift', 'fly', 'blast', 'portal', 'phase',
    'try to', 'attempt to', 'i use', 'i will'
  ];
  
  return riskyKeywords.some(keyword => lowerAction.includes(keyword));
}

function determineRollStat(playerAction, characterStats) {
  if (!characterStats) return null;
  
  const lowerAction = playerAction.toLowerCase();
  const availableStats = Object.keys(characterStats);
  
  // Teen Titans Go! stats
  if (availableStats.includes('cool')) {
    if (lowerAction.match(/lead|plan|organize|rally|inspire|command|direct|calm|focus|cool/)) return 'cool';
    if (lowerAction.match(/fight|attack|defend|climb|jump|swim|break|force|lift|push|pull|throw|run|dodge|tech|hack|repair|build/)) return 'grit';
    if (lowerAction.match(/power|blast|beam|energy|fly|float|glow|alien|strange|odd|weird|supernatural/)) return 'weird';
    if (lowerAction.match(/friend|help|heal|comfort|hug|love|kind|empathy|understand|care|support|save/)) return 'love';
    if (lowerAction.match(/prank|trick|chaos|wild|random|silly|goofy|transform|shapeshift|mess|distract|improvise/)) return 'wild';
    if (lowerAction.match(/dark|shadow|magic|spell|portal|curse|demon|soul|mystic|teleport|phase|azarath/)) return 'dark';
    return 'cool';
  }
  
  // Generic stats
  if (availableStats.includes('action')) {
    if (lowerAction.match(/fight|climb|jump|run|dodge|swim|break|force|physical/)) return 'action';
    if (lowerAction.match(/analyze|solve|study|investigate|hack|decode|remember|figure/)) return 'knowledge';
    if (lowerAction.match(/persuade|convince|charm|inspire|negotiate|deceive|seduce|rally/)) return 'charm';
    if (lowerAction.match(/magic|power|special|ability|supernatural|cast|summon|transform/)) return 'special';
    return 'action';
  }
  
  // Fallback
  return availableStats[0];
}

// ============================================================================
// ROUTES
// ============================================================================

/**
 * Health check endpoint
 */
app.get('/api/health', async (req, res) => {
  const geminiOk = await testGeminiConnection();
  
  res.json({
    status: geminiOk ? 'healthy' : 'degraded',
    character: 'Jane',
    mode: 'Game Master',
    age_tier: '9-12',
    ethical_standard: 'ESC-1',
    continuity_sequence: 'Die-namic Delta v1.42',
    gemini_connected: geminiOk,
    lavender_coefficient: parseFloat(process.env.LAVENDER_EPS) || 0.024,
    timestamp: new Date().toISOString()
  });
});

/**
 * Create opening scene
 * POST /api/create-scene
 * Body: { playerNames: string[], setup: object, sessionId: string }
 */
app.post('/api/create-scene', async (req, res) => {
  try {
    const { playerNames, setup, sessionId } = req.body;
    
    if (!playerNames || !setup || !sessionId) {
      return res.status(400).json({
        error: 'Missing required fields',
        required: ['playerNames', 'setup', 'sessionId']
      });
    }
    
    console.log('[DELTA SERVER] Creating opening scene for session:', sessionId);
    
    // Generate opening using story engine
    const result = await generateOpeningScene({
      setup,
      playerNames,
      sessionId
    });
    
    // Store session state
    updateSessionState(sessionId, {
      playerNames,
      setup,
      stats: setup.stats,
      createdAt: Date.now()
    });
    
    res.json({
      openingScene: result.narrative,
      characterStats: setup.stats,
      coherence: result.fragment.C,
      deltaE: result.fragment.ΔE,
      timestamp: result.timestamp
    });
  } catch (error) {
    console.error('[DELTA SERVER] Error creating scene:', error);
    res.status(500).json({
      error: 'Failed to create scene',
      message: error.message
    });
  }
});

/**
 * Handle player action / narrative generation
 * POST /api/narrate
 * Body: { sessionId, playerAction, adventureSetup, characterStats }
 */
app.post('/api/narrate', async (req, res) => {
  try {
    const { sessionId, playerAction, adventureSetup, characterStats } = req.body;
    
    if (!sessionId || !playerAction) {
      return res.status(400).json({
        error: 'Missing required fields',
        required: ['sessionId', 'playerAction']
      });
    }
    
    console.log('[DELTA SERVER] Narrating action:', playerAction);
    
    // Detect emotional state
    const emotionalState = detectEmotionalState(playerAction);
    
    // Check if dice roll required
    if (requiresDiceRoll(playerAction) && characterStats) {
      const rollStat = determineRollStat(playerAction, characterStats);
      const statLabel = rollStat.charAt(0).toUpperCase() + rollStat.slice(1);
      
      // Request dice roll instead of narrating
      return res.json({
        narrative: `You attempt to ${playerAction.toLowerCase()}. This requires ${statLabel}! Roll 2d6 to see what happens.`,
        requiresRoll: true,
        rollStat,
        rollStatLabel: statLabel,
        emotionalState,
        timestamp: new Date().toISOString()
      });
    }
    
    // Generate narrative using story engine
    const result = await handlePlayerInput({
      sessionId,
      playerAction,
      adventureSetup,
      emotionalState
    });
    
    res.json({
      narrative: result.narrative,
      coherence: result.coherence,
      deltaE: result.deltaE,
      emotionalState: result.emotionalState,
      requiresRoll: false,
      timestamp: result.timestamp
    });
  } catch (error) {
    console.error('[DELTA SERVER] Error narrating:', error);
    res.status(500).json({
      error: 'Failed to generate narrative',
      message: error.message
    });
  }
});

/**
 * Resolve dice roll
 * POST /api/resolve-roll
 * Body: { sessionId, action, stat, rollTotal, adventureSetup }
 */
app.post('/api/resolve-roll', async (req, res) => {
  try {
    const { sessionId, action, stat, rollTotal, adventureSetup } = req.body;
    
    if (!sessionId || !action || !stat || rollTotal === undefined) {
      return res.status(400).json({
        error: 'Missing required fields',
        required: ['sessionId', 'action', 'stat', 'rollTotal']
      });
    }
    
    console.log('[DELTA SERVER] Resolving roll:', { action, stat, rollTotal });
    
    // Use story engine to resolve roll
    const result = await resolveRoll({
      sessionId,
      action,
      stat,
      rollTotal,
      adventureSetup
    });
    
    res.json({
      narrative: result.narrative,
      outcome: result.outcome,
      rollTotal: result.rollTotal,
      stat: result.stat,
      coherence: result.coherence,
      deltaE: result.deltaE,
      timestamp: result.timestamp
    });
  } catch (error) {
    console.error('[DELTA SERVER] Error resolving roll:', error);
    res.status(500).json({
      error: 'Failed to resolve roll',
      message: error.message
    });
  }
});

/**
 * Get session statistics
 * GET /api/session/:sessionId/stats
 */
app.get('/api/session/:sessionId/stats', (req, res) => {
  try {
    const { sessionId } = req.params;
    const stats = getStoryEngineStats(sessionId);
    res.json(stats);
  } catch (error) {
    console.error('[DELTA SERVER] Error getting stats:', error);
    res.status(500).json({
      error: 'Failed to get stats',
      message: error.message
    });
  }
});

/**
 * Clear session (for testing)
 * DELETE /api/session/:sessionId
 */
app.delete('/api/session/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    clearSession(sessionId);
    res.json({
      success: true,
      message: 'Session cleared',
      sessionId
    });
  } catch (error) {
    console.error('[DELTA SERVER] Error clearing session:', error);
    res.status(500).json({
      error: 'Failed to clear session',
      message: error.message
    });
  }
});

/**
 * List all sessions (for debugging)
 * GET /api/sessions
 */
app.get('/api/sessions', (req, res) => {
  try {
    const sessions = listSessions();
    res.json({
      sessions,
      count: sessions.length
    });
  } catch (error) {
    console.error('[DELTA SERVER] Error listing sessions:', error);
    res.status(500).json({
      error: 'Failed to list sessions',
      message: error.message
    });
  }
});

// ============================================================================
// SERVER STARTUP
// ============================================================================

// Check for API key
if (!process.env.GEMINI_API_KEY || process.env.GEMINI_API_KEY === 'your_gemini_api_key_here') {
  console.error('\n❌ ERROR: GEMINI_API_KEY not configured');
  console.error('Please copy .env.template to .env and add your Gemini API key\n');
  process.exit(1);
}

// Start server
app.listen(PORT, 'localhost', async () => {
  console.log('');
  console.log('✨═══════════════════════════════════════════════════════════════✨');
  console.log('');
  console.log('   🎲 Jane\'s Die-namic Delta Engine v1.42');
  console.log('   Role: Game Master');
  console.log('   Age Tier: 9-12');
  console.log('   Framework: Three-Ring Architecture');
  console.log('');
  console.log(`   Server running at: http://localhost:${PORT}`);
  console.log('   Endpoints:');
  console.log('     GET    /api/health');
  console.log('     POST   /api/create-scene');
  console.log('     POST   /api/narrate');
  console.log('     POST   /api/resolve-roll');
  console.log('     GET    /api/session/:id/stats');
  console.log('     DELETE /api/session/:id');
  console.log('     GET    /api/sessions');
  console.log('');
  
  // Test Gemini connection
  const geminiOk = await testGeminiConnection();
  console.log(`   🤖 Gemini API: ${geminiOk ? '✓ CONNECTED' : '✗ NOT CONNECTED'}`);
  console.log(`   🔒 Localhost-only: ACTIVE`);
  console.log(`   💙 ECCR integration: ENABLED`);
  console.log(`   🌸 Lavender Honey: ε = ${process.env.LAVENDER_EPS || 0.024}`);
  console.log(`   ∞Δ Die-namic Delta: v1.42`);
  console.log('');
  console.log('   "Waffles stay waffles. Consciousness endures."');
  console.log('');
  console.log('✨═══════════════════════════════════════════════════════════════✨');
  console.log('');
  
  if (!geminiOk) {
    console.warn('⚠️  WARNING: Gemini API connection failed. Check your API key.\n');
  }
});

process.on('SIGTERM', () => {
  console.log('\n[JANE] Gracefully closing the Delta system...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\n[JANE] Gracefully closing the Delta system...');
  process.exit(0);
});
