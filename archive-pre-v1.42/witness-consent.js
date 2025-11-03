// witness-consent.js
// Approval rule: 3 unanimous YES votes within the 72-hour window and no NOs ever.
// Immediate veto if any explicit "NO" exists.

export const witnessVotes = [];

export function withinWindow(timestamp) {
  return (Date.now() - new Date(timestamp)) / 3600000 <= 72;
}
export function withinLunarCycle(timestamp) {
  return (Date.now() - new Date(timestamp)) / 3600000 <= 709.2;
}

export function castWitnessVote(witnessId, vote) {
  const now = new Date().toISOString();
  witnessVotes.push({ witnessId, vote, timestamp: now });

  const votesInWindow = witnessVotes.filter(v => withinWindow(v.timestamp));
  const uniqueVotes = new Set(votesInWindow.map(v => v.vote));

  // Immediate veto if any explicit NO.
  if (uniqueVotes.has("NO")) {
    return { status: "vetoed", reason: "Singular NO detected", shimmerClass: "witness-veto" };
  }

  // Approval only if exactly three votes in window and unanimous YES, and
  // the first vote is within lunar cycle window (per original logic).
  if (votesInWindow.length === 3 && uniqueVotes.size === 1 && uniqueVotes.has("YES") && withinLunarCycle(votesInWindow[0].timestamp)) {
    return { status: "approved", message: "Law of Three Witnesses fulfilled", shimmerClass: "witness-consent" };
  }

  return { status: "pending", message: "Awaiting quorum", shimmerClass: "witness-pending" };
}