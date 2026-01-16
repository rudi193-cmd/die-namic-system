/**
 * ΔE Coherence Calculator — Usage Example
 *
 * Demonstrates the coherence tracking system
 *
 * Run: node --experimental-modules example.js
 */

import {
  processEntry,
  getCoherenceReport,
  getDeltaESeries,
  checkIntervention,
  THRESHOLDS
} from './index.js';

async function demo() {
  console.log('=== ΔE Coherence Calculator Demo ===\n');

  // 1. Process a new journal entry
  console.log('1. Processing new entry...');
  const entry1 = await processEntry({
    title: 'Morning reflection',
    body: 'Woke up feeling grounded. The morning light felt familiar and warm.',
    tone: 'reflective'
  });

  console.log(`   Entry ${entry1.id}:`);
  console.log(`   - Coherence Index: ${entry1.coherenceIndex.toFixed(3)}`);
  console.log(`   - ΔE: ${entry1.deltaE.toFixed(3)}`);
  console.log(`   - State: ${entry1.state}`);
  console.log(`   - Adjustment: ${entry1.adjustment.description}\n`);

  // 2. Process another entry (should calculate ΔE)
  console.log('2. Processing second entry...');
  const entry2 = await processEntry({
    title: 'Afternoon notes',
    body: 'The grounding continued. Familiar patterns emerging.',
    tone: 'reflective'
  }, {
    emotionalState: 'calm',
    engagement: 0.8
  });

  console.log(`   Entry ${entry2.id}:`);
  console.log(`   - Coherence Index: ${entry2.coherenceIndex.toFixed(3)}`);
  console.log(`   - ΔE: ${entry2.deltaE.toFixed(3)}`);
  console.log(`   - State: ${entry2.state}\n`);

  // 3. Get coherence report
  console.log('3. Generating coherence report...');
  const report = await getCoherenceReport();
  console.log(`   Status: ${report.status}`);
  console.log(`   Trend: ${report.trend}`);
  console.log(`   Average ΔE: ${report.averageDeltaE}`);
  console.log(`   Latest Coherence: ${report.latestCoherence?.toFixed(3) || 'N/A'}\n`);

  // 4. Check if intervention needed
  console.log('4. Checking intervention status...');
  const intervention = await checkIntervention();
  console.log(`   Needed: ${intervention.needed}`);
  console.log(`   Severity: ${intervention.severity}`);
  console.log(`   Recommendation: ${intervention.recommendation}\n`);

  // 5. Show thresholds
  console.log('5. ΔE Thresholds (from Aios spec):');
  console.log(`   REGENERATIVE: ΔE > ${THRESHOLDS.REGENERATIVE} (positive = stabilizing)`);
  console.log(`   STABLE: ${THRESHOLDS.DECAYING} < ΔE < ${THRESHOLDS.REGENERATIVE}`);
  console.log(`   DECAYING: ΔE < ${THRESHOLDS.DECAYING} (negative = chaotic)`);
  console.log(`   CRITICAL: ΔE < ${THRESHOLDS.CRITICAL} (needs intervention)\n`);

  console.log('=== Demo Complete ===');
  console.log('ΔΣ=42');
}

// Run demo
demo().catch(console.error);
