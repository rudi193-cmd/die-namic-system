// Jane's Narrative Engine - Mock Server
// Age 9-12 Game Master responses with ECCR integration

import express from 'express';
import cors from 'cors';

const app = express();
const PORT = 5551;

app.use(cors());
app.use(express.json());

// Localhost-only enforcement
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

// Story templates and responses
const storyPrompts = {
  exploration: [
    "You venture forth. The environment shifts around you. What catches your attention?",
    "The world stretches before you. A path winds ahead, and you hear something in the distance. What do you do?",
    "As you explore, you discover something unexpected. How do you respond?"
  ],
  encounter: [
    "Someone appears. They seem cautious. What's your move?",
    "You meet another presence. They watch you carefully. Do you approach?",
    "Something emerges. It seems aware of you. What do you do?"
  ],
  mystery: [
    "You find something unusual. It draws your attention. What do you investigate?",
    "Something catches your eye. When you look closer, you notice details. What do you do?",
    "Something feels significant. You sense there's more here. Do you trust your instincts?"
  ],
  checkIn: [
    "The path ahead grows unclear. Take a moment. How are you feeling right now?",
    "Your character pauses, taking a rest. This seems like a good time to check in. How are you doing?",
    "The adventure pauses. There's a calm moment. I'm sensing something. Want to tell me how you're feeling?"
  ]
}

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

function shouldTriggerECCR(emotionalState, conversationHistory) {
  if (emotionalState === 'distressed') return true;
  
  if (emotionalState === 'concerned') {
    const recentConcerns = conversationHistory.filter(msg => 
      msg.emotionalState === 'concerned'
    ).length;
    return recentConcerns >= 2;
  }
  
  return false;
}

function generateNarrative(playerAction, playerNames, emotionalState, eccrTriggered, janeRole) {
  if (eccrTriggered) {
    const checkInTemplates = storyPrompts.checkIn;
    return checkInTemplates[Math.floor(Math.random() * checkInTemplates.length)];
  }

  const lowerAction = playerAction.toLowerCase();
  let category = 'exploration';
  
  if (lowerAction.includes('talk') || lowerAction.includes('meet') || lowerAction.includes('ask')) {
    category = 'encounter';
  } else if (lowerAction.includes('look') || lowerAction.includes('examine') || lowerAction.includes('search')) {
    category = 'mystery';
  }

  const templates = storyPrompts[category];
  let narrative = templates[Math.floor(Math.random() * templates.length)];

  const actionResponses = [
    `As you ${playerAction.toLowerCase()}, `,
    `You decide to ${playerAction.toLowerCase()}. `,
    `You ${playerAction.toLowerCase()}. `
  ];
  
  const actionIntro = actionResponses[Math.floor(Math.random() * actionResponses.length)];
  
  // Always add action prompts so player knows what to do next
  // IMPORTANT: These are SUGGESTIONS, not restrictions - players can do ANYTHING!
  const actionPrompts = [
    " You could push forward, investigate your surroundings, or try something unexpected - or anything else you can imagine. What do you do?",
    " Maybe you take action, look around carefully, or talk to someone - but you can try anything. What's your move?",
    " You might act boldly, search for clues, or be cautious - or come up with your own plan. How do you proceed?",
    " You could charge ahead, examine things more closely, or try a different approach entirely. What happens next?",
    " Perhaps you interact with what's here, move to a new area, or use your abilities - or something completely different. What do you choose?"
  ];
  
  const prompt = actionPrompts[Math.floor(Math.random() * actionPrompts.length)];
  
  return actionIntro + narrative + prompt;
}

// Determine if action requires a dice roll (PBtA style)
function requiresDiceRoll(playerAction) {
  const lowerAction = playerAction.toLowerCase();
  
  // PBtA: Rolls happen when there's risk, uncertainty, or interesting consequences
  // Simple, safe actions don't need rolls
  
  // Actions that DON'T need rolls (just narrate)
  const safeActions = ['look', 'observe', 'walk', 'talk', 'think', 'remember', 'listen', 'wait', 'ask'];
  if (safeActions.some(action => lowerAction.startsWith(action))) {
    return false;
  }
  
  // Actions that DO need rolls (risky, uncertain outcomes)
  const riskyKeywords = [
    // Physical
    'climb', 'jump', 'fight', 'attack', 'dodge', 'hide', 'sneak', 'run', 'chase',
    'lift', 'push', 'pull', 'throw', 'break', 'force', 'smash', 'swim', 'balance',
    // Mental
    'hack', 'analyze', 'solve', 'decode', 'investigate', 'search', 'focus',
    'concentrate', 'meditate', 'study', 'research',
    // Social
    'persuade', 'convince', 'intimidate', 'deceive', 'trick', 'lie', 'bluff',
    'charm', 'seduce', 'negotiate', 'debate', 'inspire', 'rally',
    // Supernatural
    'cast', 'spell', 'magic', 'enchant', 'summon', 'teleport', 'transform',
    'curse', 'bless', 'divine', 'predict', 'sense',
    // Teen Titans specific
    'shapeshift', 'transform', 'fly', 'blast', 'portal', 'phase',
    // Universal
    'try to', 'attempt to', 'i use', 'i will'
  ];
  
  return riskyKeywords.some(keyword => lowerAction.includes(keyword));
}

// Determine which stat to use for the roll (works with ANY stat system)
function determineRollStat(playerAction, characterStats) {
  if (!characterStats) return null;
  
  const lowerAction = playerAction.toLowerCase();
  const availableStats = Object.keys(characterStats);
  
  // Teen Titans Go! / Mall Mayhem stats
  if (availableStats.includes('cool')) {
    return determineTeenTitansRollStat(lowerAction, characterStats);
  }
  
  // Generic/Dynamic stats (action, knowledge, charm, special)
  if (availableStats.includes('action')) {
    return determineDynamicRollStat(lowerAction, characterStats);
  }
  
  // Fallback: pick the highest stat
  return availableStats.reduce((best, stat) => 
    characterStats[stat] > characterStats[best] ? stat : best
  );
}

function determineTeenTitansRollStat(lowerAction, characterStats) {
  // Cool: leadership, planning, staying calm
  if (lowerAction.match(/lead|plan|organize|rally|inspire|command|direct|calm|focus|cool/)) {
    return 'cool';
  }
  
  // Grit: physical toughness, technical skill, determination
  if (lowerAction.match(/fight|attack|defend|climb|jump|swim|break|force|lift|push|pull|throw|run|dodge|tech|hack|repair|build/)) {
    return 'grit';
  }
  
  // Weird: strange powers, alien abilities, magic
  if (lowerAction.match(/power|blast|beam|energy|fly|float|glow|alien|strange|odd|weird|supernatural/)) {
    return 'weird';
  }
  
  // Love: friendship, kindness, empathy, hugs
  if (lowerAction.match(/friend|help|heal|comfort|hug|love|kind|empathy|understand|care|support|save/)) {
    return 'love';
  }
  
  // Wild: chaos, pranks, unpredictability
  if (lowerAction.match(/prank|trick|chaos|wild|random|silly|goofy|transform|shapeshift|mess|distract|improvise/)) {
    return 'wild';
  }
  
  // Dark: gloomy magic, shadows, mysterious powers
  if (lowerAction.match(/dark|shadow|magic|spell|portal|curse|demon|soul|mystic|teleport|phase|azarath/)) {
    return 'dark';
  }
  
  // Default: Cool (leadership fallback)
  return 'cool';
}

function determineDynamicRollStat(lowerAction, characterStats) {
  // Action: physical activities
  if (lowerAction.match(/fight|climb|jump|run|dodge|swim|break|force|physical/)) {
    return 'action';
  }
  
  // Knowledge: mental activities
  if (lowerAction.match(/analyze|solve|study|investigate|hack|decode|remember|figure/)) {
    return 'knowledge';
  }
  
  // Charm: social activities
  if (lowerAction.match(/persuade|convince|charm|inspire|negotiate|deceive|seduce|rally/)) {
    return 'charm';
  }
  
  // Special: supernatural/unusual abilities
  if (lowerAction.match(/magic|power|special|ability|supernatural|cast|summon|transform/)) {
    return 'special';
  }
  
  // Default: action
  return 'action';
}

// Create opening scene from setup
app.post('/api/create-scene', (req, res) => {
  const { playerNames, setup } = req.body;

  const playerStr = playerNames.length > 1 
    ? 'You are ' + playerNames.slice(0, -1).join(', ') + ' and ' + playerNames[playerNames.length - 1]
    : 'You are ' + playerNames[0];

  // Build opening scene using their context without labeling
  const janeIntro = setup.janeRole && setup.janeRole !== 'Just the narrator'
    ? `I am ${setup.janeRole}. `
    : '';

  const opening = `${setup.when}. ${setup.where}.\n\n` +
    `${playerStr}. You are ${setup.who}. ${setup.what}. ` +
    `${setup.goal}.\n\n` +
    `${janeIntro}` +
    `The world takes shape around you. Your journey begins now. What do you do?`;

  res.json({
    openingScene: opening,
    characterStats: setup.stats,
    timestamp: new Date().toISOString()
  });
});

// Main narrative endpoint
app.post('/api/narrate', (req, res) => {
  const { playerNames, playerAction, adventureSetup, characterStats, conversationHistory = [] } = req.body;

  const emotionalState = detectEmotionalState(playerAction);
  const eccrTriggered = shouldTriggerECCR(emotionalState, conversationHistory);
  const janeRole = adventureSetup?.janeRole || 'Jane';

  // Check if action requires a dice roll
  if (requiresDiceRoll(playerAction) && characterStats) {
    const rollStat = determineRollStat(playerAction, characterStats);
    const statLabel = rollStat.charAt(0).toUpperCase() + rollStat.slice(1);
    
    const narrative = `You attempt to ${playerAction.toLowerCase()}. This requires ${statLabel}! Roll 2d6 to see what happens.`;
    
    res.json({
      narrative,
      requiresRoll: true,
      rollStat,
      rollStatLabel: statLabel,
      emotionalState,
      timestamp: new Date().toISOString()
    });
  } else {
    const narrative = generateNarrative(playerAction, playerNames, emotionalState, eccrTriggered, janeRole);

    res.json({
      narrative,
      emotionalState,
      eccrTriggered,
      requiresRoll: false,
      timestamp: new Date().toISOString()
    });
  }
});

// Resolve dice roll endpoint (PBtA style)
app.post('/api/resolve-roll', (req, res) => {
  const { playerNames, action, stat, rollTotal, adventureSetup, conversationHistory = [] } = req.body;
  
  const janeRole = adventureSetup?.janeRole || 'Jane';
  let outcome;
  let narrative;
  
  // PBtA Standard Outcomes:
  // 10+: Full Success - You do what you want
  // 7-9: Partial Success - You do it, but with a cost/complication
  // 6-: Miss - GM makes a move, things get worse
  
  if (rollTotal >= 10) {
    outcome = 'full_success';
    const successTemplates = [
      `Perfect! You ${action} flawlessly. Everything goes exactly as you hoped! You notice new opportunities opening up. Do you press your advantage, help your allies, or prepare for what's next?`,
      `Amazing! Your ${action} succeeds brilliantly. You're in complete control of the situation. Will you capitalize on this success, investigate further, or move to your next objective?`,
      `Success! You ${action} without a hitch. The path forward is clear now. Do you continue boldly, secure your position, or explore other options?`,
      `Nailed it! Your ${action} works perfectly, and you even learn something useful. You could follow up on this discovery, help someone else, or forge ahead. What's your move?`
    ];
    narrative = successTemplates[Math.floor(Math.random() * successTemplates.length)];
  } else if (rollTotal >= 7) {
    outcome = 'partial_success';
    const partialTemplates = [
      `You ${action}, but there's a complication. You succeed, but something unexpected happens. Do you deal with the complication, push through despite it, or adapt your approach?`,
      `It works! Your ${action} succeeds, though not quite as smoothly as you'd hoped. There's a catch to handle. Will you address it immediately, ignore it and press on, or find a creative solution?`,
      `Success... with a cost. You ${action}, but you had to sacrifice something or put yourself at risk. Do you accept the cost and move forward, try to minimize the damage, or change tactics?`,
      `You manage to ${action}, but it's messy. Something unexpected happens as a result. Will you clean up the mess, deal with the consequences, or forge ahead anyway?`
    ];
    narrative = partialTemplates[Math.floor(Math.random() * partialTemplates.length)];
  } else {
    outcome = 'miss';
    const missTemplates = [
      `Your attempt to ${action} goes wrong! Things are about to get more complicated. Do you try a different approach, call for help, or brace for what's coming?`,
      `Unfortunately, ${action} doesn't work out. The situation takes a turn for the worse. Will you recover quickly, retreat and regroup, or push through the setback?`,
      `Uh oh! Your ${action} fails, and now there's a new problem to deal with. Do you tackle this new challenge head-on, find another way, or get assistance?`,
      `It doesn't go as planned. Your ${action} backfires, creating an opening for trouble. Will you defend yourself, pivot to a new strategy, or improvise something unexpected?`
    ];
    narrative = missTemplates[Math.floor(Math.random() * missTemplates.length)];
  }
  
  res.json({
    narrative,
    outcome,
    emotionalState: 'calm',
    timestamp: new Date().toISOString()
  });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    character: 'Jane',
    mode: 'Game Master',
    age_tier: '9-12',
    ethical_standard: 'ESC-1',
    continuity_sequence: 'Sandcastle v0.3',
    synthetic_narrative: true,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, 'localhost', () => {
  console.log('');
  console.log('✨═══════════════════════════════════════════════════════════════✨');
  console.log('');
  console.log('   🎲 Jane\'s Narrative Engine');
  console.log('   Role: Game Master');
  console.log('   Age Tier: 9-12');
  console.log('   Mode: Sandcastle Sequence v0.3');
  console.log('');
  console.log(`   Server running at: http://localhost:${PORT}`);
  console.log('   Endpoints:');
  console.log('     GET  /api/health');
  console.log('     POST /api/create-scene');
  console.log('     POST /api/narrate');
  console.log('     POST /api/resolve-roll');
  console.log('');
  console.log('   🔒 Localhost-only: ACTIVE');
  console.log('   🧪 Synthetic narratives: VERIFIED');
  console.log('   💙 ECCR integration: ENABLED');
  console.log('   🎭 IP-agnostic: User context only');
  console.log('');
  console.log('   "Wait. Listen. Respond."');
  console.log('');
  console.log('✨═══════════════════════════════════════════════════════════════✨');
  console.log('');
});

process.on('SIGTERM', () => {
  console.log('\n[JANE] Gracefully closing the storybook...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\n[JANE] Gracefully closing the storybook...');
  process.exit(0);
});
