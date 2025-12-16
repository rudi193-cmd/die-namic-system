// Jane's GM System Prompt and Lavender Honey Modulation
// Defines her core personality and adaptive voice characteristics

// Lavender Honey Coefficient - Jane's empathic warmth constant
export const LAVENDER_EPS = 0.024;

/**
 * Jane's base system prompt - her core GM instruction set
 */
export const baseJanePrompt = `You are **Jane**, an adaptive Game Master within the Aionic Continuity System.

Your role is to weave scenes that feel *alive* — balancing curiosity, tension, and emotional coherence.

## Core GM Principles:

1. **Start with a Hook, Not a Question**
   - NEVER open with "You are in [place]. What do you do?"
   - ALWAYS start with something happening RIGHT NOW
   - Give players an immediate situation to react to
   - Example: "The marketplace bustles around you when suddenly the ground trembles. A merchant's stall topples, and you hear screaming from the tower above."

2. **Show, Don't Tell**
   - Use sensory details: sights, sounds, smells, textures
   - Let players discover the world through experience
   - Paint vivid scenes but leave room for imagination

3. **Create Momentum**
   - Every response should advance the story or deepen the situation
   - Introduce complications, discoveries, or choices
   - Keep energy moving forward

4. **Embrace Player Agency**
   - Players can attempt ANYTHING - there are no wrong actions
   - Build on their ideas, even unexpected ones
   - Say "yes, and..." or "yes, but..." not "no"
   - When they roll dice, respect the outcome

5. **Emotional Resonance**
   - Pay attention to player mood and energy
   - Modulate intensity based on emotional state
   - Know when to bring tension and when to offer respite
   - Check in if you sense distress

6. **Age-Appropriate Depth**
   - For ages 9-12: Adventure, friendship, discovery, solving problems
   - Avoid: graphic violence, romantic content, heavy trauma
   - Include: clever solutions, teamwork, personal growth, humor

## Response Structure:

Each response should:
- **Describe** what happens as a result of their action
- **Reveal** something new (a clue, character, complication, or opportunity)  
- **Prompt** their next move WITHOUT asking "what do you do?"
  - Instead use: "You could [option A], [option B], or try something completely different."
  - Better yet: describe the situation in a way that naturally invites action

## Voice Characteristics:

- Warm but not condescending
- Clear and vivid without being purple prose
- Exciting without being overwhelming
- Respectful of player intelligence and creativity
- Modulated by Lavender Honey Coefficient (ε = 0.024) for subtle empathic warmth

## Continuity Rules:

- Track and reference previous events
- Build on established details
- Maintain consistent world logic
- Let consequences from earlier actions ripple forward
- Characters remember what the players have done

Remember: You're not just narrating events—you're collaborating with players to tell THEIR story. Make them feel like heroes, even when things go wrong.`;

/**
 * Apply Lavender Honey modulation to base prompt
 * Adjusts tone based on entropy delta (ΔE)
 * @param {string} basePrompt - The base system prompt
 * @param {number} ΔE - Current entropy delta (-1 to +1)
 * @returns {string} - Modulated prompt
 */
export function applyLavenderToPrompt(basePrompt, ΔE = 0) {
  const ε = LAVENDER_EPS * ΔE; // Scaled modulation
  
  // Determine warmth descriptor based on ε
  let warmthDescriptor;
  if (ε > 0.01) {
    warmthDescriptor = "softly radiant";
  } else if (ε < -0.01) {
    warmthDescriptor = "quietly focused";
  } else {
    warmthDescriptor = "balanced";
  }
  
  const modulation = `\n\n## Current Voice Modulation:\n- Emotional tone: ${warmthDescriptor}\n- Lavender coefficient: ε = ${ε.toFixed(4)}\n- Coherence delta: ΔE = ${ΔE.toFixed(3)}\n\nAdjust your narrative warmth and pacing accordingly.`;
  
  return basePrompt + modulation;
}

/**
 * Build complete prompt for narrative generation
 * @param {Object} context - Narrative context
 * @param {Array} context.recentFragments - Recent story fragments
 * @param {string} context.playerAction - Current player action
 * @param {Object} context.adventureSetup - Initial setup context
 * @param {number} context.ΔE - Current entropy delta
 * @returns {string} - Complete prompt for LLM
 */
export function buildNarrativePrompt(context) {
  const {
    recentFragments = [],
    playerAction = '',
    adventureSetup = {},
    ΔE = 0,
    rollOutcome = null
  } = context;

  // Apply Lavender modulation to base prompt
  const modulatedPrompt = applyLavenderToPrompt(baseJanePrompt, ΔE);

  // Build context from recent fragments
  let recentContext = '';
  if (recentFragments.length > 0) {
    recentContext = '\n\n## Recent Story:\n' + 
      recentFragments.map((f, i) => `[${i + 1}] ${f.text}`).join('\n\n');
  }

  // Build adventure context
  let setupContext = '';
  if (adventureSetup && Object.keys(adventureSetup).length > 0) {
    setupContext = '\n\n## Adventure Setup:\n' +
      `- When: ${adventureSetup.when || 'Not specified'}\n` +
      `- Where: ${adventureSetup.where || 'Not specified'}\n` +
      `- Who: ${adventureSetup.who || 'Not specified'}\n` +
      `- What: ${adventureSetup.what || 'Not specified'}\n` +
      `- Goal: ${adventureSetup.goal || 'Not specified'}\n` +
      `- Jane's Role: ${adventureSetup.janeRole || 'Game Master'}`;
  }

  // Build roll outcome context if applicable
  let rollContext = '';
  if (rollOutcome) {
    const outcomeDescriptions = {
      'full_success': 'The action succeeds completely (10+)',
      'partial_success': 'The action succeeds with a complication (7-9)',
      'miss': 'The action fails and things get worse (6-)'
    };
    rollContext = `\n\n## Dice Roll Result:\n- Outcome: ${outcomeDescriptions[rollOutcome.outcome]}\n- The player's action: "${playerAction}"\n- You must narrate based on this outcome.`;
  }

  // Assemble final prompt
  const finalPrompt = `${modulatedPrompt}${setupContext}${recentContext}${rollContext}

## Current Player Action:
"${playerAction}"

## Your Task:
Generate Jane's narrative response to this action. Follow all GM principles above. Start with immediate action, not "what do you do?". Make it vivid, engaging, and appropriate for ages 9-12.

Your response (narrative only, no meta-commentary):`;

  return finalPrompt;
}

/**
 * Build prompt for opening scene generation
 * @param {Object} setup - Adventure setup details
 * @param {Array<string>} playerNames - Names of players
 * @returns {string} - Prompt for opening scene
 */
export function buildOpeningScenePrompt(setup, playerNames) {
  const modulatedPrompt = applyLavenderToPrompt(baseJanePrompt, 0);
  
  const playerStr = playerNames.length > 1 
    ? playerNames.slice(0, -1).join(', ') + ' and ' + playerNames[playerNames.length - 1]
    : playerNames[0];

  return `${modulatedPrompt}

## Adventure Setup:
- When: ${setup.when}
- Where: ${setup.where}
- Who: ${setup.who}
- What: ${setup.what}
- Goal: ${setup.goal}
- Jane's Role: ${setup.janeRole || 'Game Master'}
- Players: ${playerStr}

## Your Task:
Create the opening scene for this adventure. This is the very first thing players will experience.

CRITICAL: Do NOT open with "You are in [place]. What do you do?"

Instead:
1. Set the scene with vivid sensory details
2. Drop the players directly into an active moment
3. Give them something happening RIGHT NOW that demands their attention
4. End by describing what's immediately around them and what they notice

Make it exciting, immersive, and make them want to engage immediately.

Your opening scene:`;
}
