// ΔE Field Calculations - Aionic Journal System
// Measures entropy delta for emotional/behavioral coherence tracking

/**
 * Compute ΔE (Entropy Delta)
 * 
 * Formula: ΔE = (dC/dt) × R
 * 
 * Where:
 *   C = Coherence value (0-1)
 *   t = Time (milliseconds)
 *   R = Resonance multiplier (default 1.0)
 *   ΔE = Rate of coherence change
 * 
 * States:
 *   ΔE > 0: Regenerative (coherence increasing)
 *   ΔE = 0: Stable (no change)
 *   ΔE < 0: Decaying (coherence decreasing)
 */
export function computeDeltaE({ Cprev, tPrev, Cnow, tNow, R = 1.0 }) {
  const dt = (tNow - tPrev) / 1000; // Convert to seconds
  
  if (dt <= 0) return 0;
  
  const dCdt = (Cnow - Cprev) / dt;
  const deltaE = dCdt * R;
  
  return deltaE;
}

/**
 * Compute ΔE series from multiple measurements
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
 */
export function averageDeltaE(deltaEs, windowSize = 3) {
  if (deltaEs.length === 0) return 0;
  
  const window = deltaEs.slice(-windowSize);
  const sum = window.reduce((acc, val) => acc + val, 0);
  return sum / window.length;
}

/**
 * Classify state based on ΔE
 */
export function classifyState(deltaE) {
  if (deltaE > 0.05) return 'regenerative';
  if (deltaE < -0.05) return 'decaying';
  return 'stable';
}

/**
 * Calculate resonance factor
 * Higher resonance = stronger coherence effects
 */
export function calculateResonance(context = {}) {
  let R = 1.0;
  
  // Amplify during emotional moments
  if (context.emotionalState === 'distressed') R *= 1.3;
  else if (context.emotionalState === 'concerned') R *= 1.15;
  
  // Amplify with engagement
  if (context.engagement) {
    R *= (0.8 + context.engagement * 0.4);
  }
  
  return R;
}

/**
 * Get recommended adjustment based on ΔE
 */
export function getAdjustment(deltaE) {
  if (deltaE > 0.1) {
    return {
      action: 'sustain',
      description: 'Momentum is strong - maintain current direction',
      tone: 'encouraging'
    };
  } else if (deltaE > 0) {
    return {
      action: 'continue',
      description: 'Building coherence - keep current approach',
      tone: 'steady'
    };
  } else if (deltaE > -0.1) {
    return {
      action: 'stabilize',
      description: 'Coherence declining - introduce familiar elements',
      tone: 'grounding'
    };
  } else {
    return {
      action: 'reset',
      description: 'Significant drift - return to established themes',
      tone: 'gentle'
    };
  }
}
