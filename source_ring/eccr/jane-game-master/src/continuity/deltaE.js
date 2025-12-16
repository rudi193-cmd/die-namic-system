// ΔE Field Calculations
// Computes entropy delta for narrative coherence tracking

/**
 * Compute discrete ΔE using last two coherence samples
 * 
 * Formula: ΔE = (dC/dt) × R
 * Where:
 *   - C = Coherence value (0-1)
 *   - t = Time (milliseconds)
 *   - R = Resonance multiplier (default 1.0)
 *   - ΔE = Entropy delta (change rate of coherence)
 * 
 * Interpretation:
 *   - ΔE > 0: Regenerative (narrative coherence increasing)
 *   - ΔE = 0: Stable (no change in coherence)
 *   - ΔE < 0: Decaying (narrative coherence decreasing)
 * 
 * @param {Object} params - Calculation parameters
 * @param {number} params.Cprev - Previous coherence value
 * @param {number} params.tPrev - Previous timestamp (ms)
 * @param {number} params.Cnow - Current coherence value
 * @param {number} params.tNow - Current timestamp (ms)
 * @param {number} params.R - Resonance multiplier (default 1.0)
 * @returns {number} - Entropy delta (ΔE)
 */
export function computeDeltaE({ Cprev, tPrev, Cnow, tNow, R = 1.0 }) {
  // Calculate time difference in seconds
  const dt = (tNow - tPrev) / 1000;
  
  // Avoid division by zero
  if (dt <= 0) return 0;
  
  // Calculate rate of coherence change
  const dCdt = (Cnow - Cprev) / dt;
  
  // Apply resonance multiplier
  const deltaE = dCdt * R;
  
  return deltaE;
}

/**
 * Compute ΔE from a series of coherence measurements
 * Useful for tracking trends over multiple fragments
 * 
 * @param {Array<{C: number, t: number}>} measurements - Array of {C, t} measurements
 * @param {number} R - Resonance multiplier
 * @returns {Array<number>} - Array of ΔE values
 */
export function computeDeltaESeries(measurements, R = 1.0) {
  if (measurements.length < 2) return [];
  
  const deltaEs = [];
  for (let i = 1; i < measurements.length; i++) {
    const prev = measurements[i - 1];
    const curr = measurements[i];
    
    const deltaE = computeDeltaE({
      Cprev: prev.C,
      tPrev: prev.t,
      Cnow: curr.C,
      tNow: curr.t,
      R
    });
    
    deltaEs.push(deltaE);
  }
  
  return deltaEs;
}

/**
 * Calculate average ΔE over recent history
 * Used to determine overall narrative trajectory
 * 
 * @param {Array<number>} deltaEs - Array of ΔE values
 * @param {number} windowSize - Number of recent values to average
 * @returns {number} - Average ΔE
 */
export function averageDeltaE(deltaEs, windowSize = 3) {
  if (deltaEs.length === 0) return 0;
  
  const window = deltaEs.slice(-windowSize);
  const sum = window.reduce((acc, val) => acc + val, 0);
  return sum / window.length;
}

/**
 * Classify narrative state based on ΔE value
 * 
 * @param {number} deltaE - Current ΔE value
 * @returns {string} - State classification
 */
export function classifyNarrativeState(deltaE) {
  if (deltaE > 0.05) return 'regenerative';
  if (deltaE < -0.05) return 'decaying';
  return 'stable';
}

/**
 * Calculate resonance factor based on context
 * Higher resonance = stronger coherence effects
 * 
 * @param {Object} context - Narrative context
 * @param {string} context.emotionalState - Current emotional state
 * @param {number} context.playerEngagement - Engagement level (0-1)
 * @returns {number} - Resonance factor R
 */
export function calculateResonance(context = {}) {
  let R = 1.0; // Base resonance
  
  // Amplify during emotional moments
  if (context.emotionalState === 'distressed') {
    R *= 1.3;
  } else if (context.emotionalState === 'concerned') {
    R *= 1.15;
  }
  
  // Amplify with high player engagement
  if (context.playerEngagement) {
    R *= (0.8 + context.playerEngagement * 0.4); // 0.8-1.2 range
  }
  
  return R;
}

/**
 * Get recommended narrative adjustment based on ΔE
 * 
 * @param {number} deltaE - Current ΔE value
 * @returns {Object} - Adjustment recommendations
 */
export function getNarrativeAdjustment(deltaE) {
  if (deltaE > 0.1) {
    return {
      action: 'sustain',
      description: 'Narrative momentum is strong - maintain current direction',
      pacing: 'steady',
      complexity: 'increase_slightly'
    };
  } else if (deltaE > 0) {
    return {
      action: 'continue',
      description: 'Narrative is building coherence - keep current approach',
      pacing: 'steady',
      complexity: 'maintain'
    };
  } else if (deltaE > -0.1) {
    return {
      action: 'stabilize',
      description: 'Narrative coherence declining - introduce familiar elements',
      pacing: 'slow',
      complexity: 'reduce'
    };
  } else {
    return {
      action: 'reset',
      description: 'Significant drift detected - return to established themes',
      pacing: 'pause',
      complexity: 'simplify'
    };
  }
}
