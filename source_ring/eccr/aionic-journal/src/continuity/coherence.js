// Coherence Index Calculator - Aionic Journal System
// Measures semantic similarity between journal entries

/**
 * Simple coherence calculator (keyword overlap)
 * Production: Replace with embedding-based similarity
 */
export function calculateCoherence(currentEntry, recentEntries) {
  if (!recentEntries || recentEntries.length === 0) {
    return 0.6; // Baseline coherence
  }

  const scores = recentEntries.map(entry => 
    computeSimilarity(currentEntry, entry)
  );

  const avgScore = scores.reduce((sum, s) => sum + s, 0) / scores.length;
  return Math.max(0, Math.min(1, avgScore));
}

/**
 * Compute similarity between two entries
 * Simple keyword-based for now
 */
function computeSimilarity(entry1, entry2) {
  const words1 = extractWords(entry1);
  const words2 = extractWords(entry2);

  if (words1.size === 0 || words2.size === 0) return 0.5;

  const intersection = new Set([...words1].filter(w => words2.has(w)));
  const union = new Set([...words1, ...words2]);

  const jaccard = intersection.size / union.size;
  
  // Tone similarity bonus
  const toneMatch = entry1.tone === entry2.tone ? 0.2 : 0;

  return Math.min(1, jaccard + toneMatch);
}

/**
 * Extract significant words from entry
 */
function extractWords(entry) {
  const text = `${entry.title || ''} ${entry.body || ''}`.toLowerCase();
  
  const words = text
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 3) // Filter short words
    .filter(w => !STOP_WORDS.has(w));

  return new Set(words);
}

/**
 * Common stop words to filter
 */
const STOP_WORDS = new Set([
  'this', 'that', 'with', 'from', 'have', 'been',
  'were', 'they', 'their', 'would', 'there', 'about',
  'could', 'should', 'which', 'these', 'those', 'will',
  'what', 'when', 'where', 'just', 'more', 'some',
  'other', 'into', 'very', 'after', 'before', 'also'
]);

/**
 * Get coherence trend over time
 */
export function getCoherenceTrend(entries) {
  if (entries.length < 2) return 'stable';

  const recentCoherence = entries.slice(-5).map(e => e.ci || 0.6);
  const avg = recentCoherence.reduce((sum, c) => sum + c, 0) / recentCoherence.length;

  if (avg > 0.75) return 'high';
  if (avg < 0.5) return 'low';
  return 'moderate';
}

/**
 * Detect coherence drift (sudden changes)
 */
export function detectDrift(entries, threshold = 0.3) {
  if (entries.length < 2) return false;

  const recent = entries.slice(-2);
  const diff = Math.abs((recent[1].ci || 0.6) - (recent[0].ci || 0.6));

  return diff > threshold;
}
