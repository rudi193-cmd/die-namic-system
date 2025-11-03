// sovereign-check.js
// Exports only: evaluatePSR and sovereignCheck
// Policy: projectedPSR === 0 => explicit malice (halt). Missing projectedPSR => default 0.95.

export function evaluatePSR(adaptation) {
  // Use nullish coalescing so numeric 0 is preserved (0 means explicit malice).
  return adaptation?.projectedPSR ?? 0.95;
}

/**
 * sovereignCheck(proposedAdaptation)
 * Returns an object with status "halted" or "approved" based on PSR threshold.
 */
export function sovereignCheck(proposedAdaptation) {
  const psrScore = evaluatePSR(proposedAdaptation);
  const ethicalThreshold = 1.00;

  if (psrScore < ethicalThreshold) {
    return {
      status: "halted",
      reason: "PSR score below ethical threshold",
      shimmerClass: "sovereign-veto"
    };
  }

  return {
    status: "approved",
    message: "Adaptation passed Sovereign Check",
    shimmerClass: "sovereign-approved"
  };
}