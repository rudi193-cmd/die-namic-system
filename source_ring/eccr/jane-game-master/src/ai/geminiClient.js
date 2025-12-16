// Gemini API Client for Jane
// Provides LLM integration and embedding services

import { GoogleGenerativeAI } from "@google/generative-ai";

// Initialize with API key from environment
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

/**
 * Generate narrative response from Jane using Gemini
 * @param {string} prompt - The complete prompt including context
 * @returns {Promise<string>} - Jane's narrative response
 */
export async function generateJaneResponse(prompt) {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error('[GEMINI] Error generating response:', error);
    throw new Error('Failed to generate narrative: ' + error.message);
  }
}

/**
 * Get embedding vector for text using Gemini
 * Used for coherence scoring via semantic similarity
 * @param {string} text - Text to embed
 * @returns {Promise<number[]>} - Embedding vector
 */
export async function getGeminiEmbedding(text) {
  try {
    const model = genAI.getGenerativeModel({ model: "text-embedding-004" });
    const result = await model.embedContent(text);
    return result.embedding.values;
  } catch (error) {
    console.error('[GEMINI] Error getting embedding:', error);
    throw new Error('Failed to get embedding: ' + error.message);
  }
}

/**
 * Test connection to Gemini API
 * @returns {Promise<boolean>} - True if connection successful
 */
export async function testGeminiConnection() {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent("Test");
    return true;
  } catch (error) {
    console.error('[GEMINI] Connection test failed:', error);
    return false;
  }
}
