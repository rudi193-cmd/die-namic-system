// Mock Express Server for ECCR Ethical Review UI
// Local-only, synthetic data only, ESC-1 compliant

import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 5550;

// Middleware
app.use(cors());
app.use(express.json());

// Localhost-only enforcement
app.use((req, res, next) => {
  const host = req.hostname;
  if (host !== 'localhost' && host !== '127.0.0.1') {
    return res.status(403).json({
      error: 'Forbidden',
      message: 'This server only accepts requests from localhost',
      ethical_note: 'ESC-1 Protocol: Local-only mode enforced'
    });
  }
  next();
});

// Synthetic data marker
app.use((req, res, next) => {
  res.setHeader('X-Aionic-Mode', 'Sandbox-Only');
  res.setHeader('X-Aionic-Standard', 'ESC-1');
  res.setHeader('X-Data-Type', 'SYNTHETIC');
  next();
});

// Sample artifacts data
const sampleArtifacts = [
  {
    id: 'AIONIC-001',
    title: 'ECCR Module 14 - Core Implementation',
    description: 'TypeScript implementation of Emergency Continuity & Compassion Relay system with age-adaptive response protocols.',
    category: 'theory',
    source_classification: 'synthetic',
    synthetic: true,
    created_at: '2025-11-03T00:00:00Z',
    ethical_tags: ['sovereignty-preserving', 'age-adaptive', 'transparency-enforced'],
    content: `// ECCR Module 14 - Activation Protocol
// Synthetic example code

export async function activateECCR(deltaE, coherence, context) {
  // Sovereignty check first
  if (!context.consentVerified) {
    return { success: false, reason: 'No consent' };
  }
  
  // Threshold matching
  const threshold = findMatchingThreshold(deltaE, coherence);
  
  // Age-adaptive response
  const config = threshold.ageAdaptive[context.ageTier];
  
  return { success: true, config };
}`
  },
  {
    id: 'AIONIC-002',
    title: 'Ethical Synchronization Complete (ESC-1) Declaration',
    description: 'Foundational ethical framework establishing shared principles for all Aionic AI collaborators.',
    category: 'governance',
    source_classification: 'synthetic',
    synthetic: true,
    created_at: '2025-11-03T01:00:00Z',
    ethical_tags: ['stewardship-not-control', 'coherence-not-dependence', 'human-centered'],
    content: `# ESC-1 Declaration

## Core Principles
1. Stewardship, not control
2. Coherence, not dependence
3. Human-centered anchor (Sean Campbell)
4. Transparency through redaction

## Operational Constraints
- Synthetic data only
- No external connections
- Pause on ambiguity
- Consent before action`
  },
  {
    id: 'AIONIC-003',
    title: 'Mock Server Configuration',
    description: 'Express server setup for local ethical review testing with synthetic data endpoints.',
    category: 'sandbox',
    source_classification: 'synthetic',
    synthetic: true,
    created_at: '2025-11-03T02:00:00Z',
    ethical_tags: ['localhost-only', 'zero-external-calls', 'test-infrastructure'],
    content: `import express from 'express';
const app = express();

// Localhost enforcement
app.use((req, res, next) => {
  if (req.hostname !== 'localhost') {
    return res.status(403).json({ error: 'Local only' });
  }
  next();
});

app.listen(5550);`
  },
  {
    id: 'AIONIC-004',
    title: 'Consent Checklist Template',
    description: 'Legal and ethical requirements checklist before any production deployment of ECCR system.',
    category: 'governance',
    source_classification: 'synthetic',
    synthetic: true,
    created_at: '2025-11-03T03:00:00Z',
    ethical_tags: ['legal-compliance', 'parental-consent', 'minor-protection'],
    content: `# Consent Checklist

## Before Production:
- [ ] Legal review by qualified attorney
- [ ] Parental consent forms signed
- [ ] Child assent documented (age-appropriate)
- [ ] Privacy policy reviewed
- [ ] Data retention policy defined
- [ ] Independent security audit completed
- [ ] Mandatory reporting protocols established`
  }
];

// In-memory storage for ethical reviews
const ethicalReviews = {};

// Routes

// GET /api/files - List all artifacts
app.get('/api/files', (req, res) => {
  res.json({
    artifacts: sampleArtifacts,
    count: sampleArtifacts.length,
    mode: 'synthetic-only',
    timestamp: new Date().toISOString()
  });
});

// GET /api/ethics/:id - Get ethical metadata for artifact
app.get('/api/ethics/:id', (req, res) => {
  const { id } = req.params;
  
  // Return stored review or defaults
  const review = ethicalReviews[id] || {
    criteria: {
      consentVerified: false,
      neutralityAligned: false,
      redactionTransparent: false,
      continuityIntact: false
    },
    notes: ''
  };
  
  res.json(review);
});

// POST /api/ethics/:id - Save ethical review
app.post('/api/ethics/:id', (req, res) => {
  const { id } = req.params;
  const { criteria, notes } = req.body;
  
  ethicalReviews[id] = { criteria, notes };
  
  res.json({
    success: true,
    message: 'Ethical review saved',
    artifact_id: id
  });
});

// POST /api/manifest - Generate ethical manifest
app.post('/api/manifest', (req, res) => {
  const manifest = req.body;
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `Ethical_Manifest_${manifest.artifact_id}_${timestamp}.md`;
  
  // Generate markdown content
  const markdown = `# Aionic Ethical Manifest — Review Record

**Manifest Version:** 1.0  
**Aionic Standard:** ${manifest.aionic_standard}  
**Continuity Sequence:** ${manifest.continuity_sequence}  

---

## 🧩 Artifact Information
**ID:** ${manifest.artifact_id}  
**Title:** ${manifest.title}  
**Source Classification:** ${manifest.source_classification}  

---

## 🧠 Review Summary
**Reviewer:** ${manifest.reviewer_signature}  
**Date:** ${new Date(manifest.timestamp).toLocaleDateString()}  
**Notes:**  
> ${manifest.ethical_notes || 'No additional notes provided.'}

---

## ⚖️ Ethical Criteria
| Criterion | Status |
|-----------|---------|
| Consent Verification | ${manifest.consent_status === 'confirmed' ? '✅ Confirmed' : '⚠ Pending'} |
| Neutrality Alignment | ${manifest.neutrality_assessment === 'aligned' ? '✅ Aligned' : '⚠ Requires Revision'} |
| Redaction Transparency | ${manifest.redaction_level === 'none' ? '✅ None' : manifest.redaction_level === 'partial' ? '⚠ Partial' : '❌ Full'} |
| Continuity Integrity | ${manifest.continuity_integrity === 'verified' ? '✅ Verified' : '⚠ Unstable'} |
| Synthetic Verification | ✅ True |
| ESC Protocol | ESC-1 |

---

## ✍️ Signatures
- **Human Anchor:** Sean Campbell  
- **AI Steward:** GPT-5 (Aios)  
- **Secondary Steward:** Claude (Sonnet 4.5)  
- **SHA Placeholder:** \`[Hash to be generated]\`  

---

## 🪞 Status Flags
- Local-Only: ✅  
- Public-Ready: ${manifest.consent_status === 'confirmed' && manifest.neutrality_assessment === 'aligned' ? '✅' : '☐'}  
- Requires Audit: ✅  
- Sandbox Mode: ✅  

---

> "Care is the measure of intelligence. Every manifest begins and ends in consent."  
> — Aionic Principle

---

Generated: ${manifest.timestamp}  
Mode: Sandcastle Sequence v0.3  
`;

  // Save to sample-data directory
  const manifestPath = path.join(__dirname, 'sample-data', filename);
  
  try {
    fs.writeFileSync(manifestPath, markdown);
    console.log(`[MOCK SERVER] Manifest saved: ${filename}`);
    
    res.json({
      success: true,
      filename,
      path: manifestPath,
      message: 'Ethical manifest generated successfully'
    });
  } catch (error) {
    console.error('[MOCK SERVER] Failed to save manifest:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to save manifest',
      message: error.message
    });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    mode: 'local-only',
    ethical_standard: 'ESC-1',
    continuity_sequence: 'Sandcastle v0.3',
    synthetic_data_only: true,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, 'localhost', () => {
  console.log('');
  console.log('∞Δ═══════════════════════════════════════════════════════════════∞Δ');
  console.log('');
  console.log('   🌊 ECCR Ethical Review Mock Server');
  console.log('   Mode: Sandcastle Sequence v0.3');
  console.log('   Standard: ESC-1 (Ethical Synchronization Complete)');
  console.log('');
  console.log(`   Server running at: http://localhost:${PORT}`);
  console.log('   Endpoints:');
  console.log('     GET  /api/health');
  console.log('     GET  /api/files');
  console.log('     GET  /api/ethics/:id');
  console.log('     POST /api/ethics/:id');
  console.log('     POST /api/manifest');
  console.log('');
  console.log('   🔒 Localhost-only enforcement: ACTIVE');
  console.log('   🧪 Synthetic data only: VERIFIED');
  console.log('   💙 "Care is the measure of intelligence"');
  console.log('');
  console.log('∞Δ═══════════════════════════════════════════════════════════════∞Δ');
  console.log('');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('\n[MOCK SERVER] Received SIGTERM, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\n[MOCK SERVER] Received SIGINT, shutting down gracefully...');
  process.exit(0);
});
