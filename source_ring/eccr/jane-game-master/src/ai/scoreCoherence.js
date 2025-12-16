// Coherence Scoring System
// Quantifies narrative continuity using embeddings and entropy

import { getGeminiEmbedding } from "./geminiClient.js";

/**
 * Calculate cosine similarity between two vectors
 * @param {number[]} vecA - First vector
 * @param {number[]} vecB - Second vector
 * @returns {number} - Similarity score (0-1)
 */
function cosineSimilarity(vecA, vecB) {
  if (vecA.length !== vecB.length) {
    throw new Error('Vectors must have same length');
  }
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  
  normA = Math.sqrt(normA);
  normB = Math.sqrt(normB);
  
  if (normA === 0 || normB === 0) return 0;
  
  return dotProduct / (normA * normB);
}

/**
 * Score coherence of new narrative fragment against recent history
 * @param {string} newText - New narrative text to score
 * @param {Array} recentFragments - Recent fragments with {text, embedding} properties
 * @returns {Promise<{score: number, ΔE: number}>} - Coherence metrics
 */
export async function scoreCoherence(newText, recentFragments = []) {
  try {
    // If no history, return neutral score
    if (recentFragments.length === 0) {
      return {
        score: 0.6, // Neutral starting coherence
        ΔE: 0
      };
    }

    // Get embedding for new text
    const newEmbedding = await getGeminiEmbedding(newText);

    // Calculate similarities to recent fragments
    const similarities = [];
    for (const fragment of recentFragments) {
      if (!fragment.embedding) {
        // Generate embedding if not cached
        fragment.embedding = await getGeminiEmbedding(fragment.text);
      }
      const sim = cosineSimilarity(newEmbedding, fragment.embedding);
      similarities.push(sim);
    }

    // Average similarity across recent fragments
    const avgSim = similarities.reduce((sum, sim) => sum + sim, 0) / similarities.length;

    // Apply diversity penalty to avoid mechanical repetition
    // We want coherence but not monotony
    const diversityPenalty = Math.abs(1 - avgSim) * 0.08;

    // Final coherence score (0-1 range)
    const coherenceScore = Math.max(0, Math.min(1, avgSim - diversityPenalty));

    // Calculate ΔE (entropy delta)
    // Positive ΔE = regenerative (increasing coherence)
    // Negative ΔE = decaying (decreasing coherence)
    const ΔE = (coherenceScore - 0.5) * 2; // Scale to -1 to +1

    return {
      score: coherenceScore,
      ΔE: ΔE,
      embedding: newEmbedding // Cache for next comparison
    };
  } catch (error) {
    console.error('[COHERENCE] Error scoring coherence:', error);
    // Return neutral on error
    return {
      score: 0.5,
      ΔE: 0
    };
  }
}

/**
 * Quick coherence check without embeddings (for real-time monitoring)
 * Uses simple heuristics like length similarity and keyword overlap
 * @param {string} newText - New text to check
 * @param {Array} recentFragments - Recent text fragments
 * @returns {number} - Quick coherence estimate (0-1)
 */
export function quickCoherenceCheck(newText, recentFragments = []) {
  if (recentFragments.length === 0) return 0.6;

  const newWords = new Set(newText.toLowerCase().split(/\s+/));
  const recentWords = new Set();
  
  recentFragments.forEach(frag => {
    frag.text.toLowerCase().split(/\s+/).forEach(word => recentWords.add(word));
  });

  // Calculate word overlap
  const overlap = [...newWords].filter(word => recentWords.has(word)).length;
  const overlapRatio = overlap / newWords.size;

  // Simple heuristic score
  return Math.min(0.9, Math.max(0.3, overlapRatio * 1.2));
}
