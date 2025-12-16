import { useState, useEffect } from 'react'
import ManifestAutoIndex from './components/ManifestAutoIndex'
import ManifestViewer from './components/ManifestViewer'
import EthicalChecklistPanel from './components/EthicalChecklistPanel'
import SandboxFooter from './components/SandboxFooter'

function App() {
  const [artifacts, setArtifacts] = useState([])
  const [selectedArtifact, setSelectedArtifact] = useState(null)
  const [ethicalCriteria, setEthicalCriteria] = useState({
    consentVerified: false,
    neutralityAligned: false,
    redactionTransparent: false,
    continuityIntact: false,
  })
  const [reviewNotes, setReviewNotes] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load artifacts from mock server
    fetch('/api/files')
      .then(res => res.json())
      .then(data => {
        setArtifacts(data.artifacts || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load artifacts:', err)
        setLoading(false)
      })
  }, [])

  const handleArtifactSelect = (artifact) => {
    setSelectedArtifact(artifact)
    // Load ethical metadata for this artifact
    fetch(`/api/ethics/${artifact.id}`)
      .then(res => res.json())
      .then(data => {
        setEthicalCriteria(data.criteria || {
          consentVerified: false,
          neutralityAligned: false,
          redactionTransparent: false,
          continuityIntact: false,
        })
        setReviewNotes(data.notes || '')
      })
      .catch(err => console.error('Failed to load ethics data:', err))
  }

  const handleCriteriaChange = (key, value) => {
    setEthicalCriteria(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleGenerateManifest = () => {
    if (!selectedArtifact) {
      alert('Please select an artifact first')
      return
    }

    const manifest = {
      artifact_id: selectedArtifact.id,
      title: selectedArtifact.title,
      source_classification: selectedArtifact.source_classification,
      consent_status: ethicalCriteria.consentVerified ? 'confirmed' : 'pending',
      neutrality_assessment: ethicalCriteria.neutralityAligned ? 'aligned' : 'requires-revision',
      redaction_level: ethicalCriteria.redactionTransparent ? 'none' : 'partial',
      continuity_integrity: ethicalCriteria.continuityIntact ? 'verified' : 'unstable',
      reviewer_signature: 'Sean Campbell',
      timestamp: new Date().toISOString(),
      version: 'v0.1',
      ethical_notes: reviewNotes,
      aionic_standard: 'ESC-1',
      continuity_sequence: 'Sandcastle v0.3'
    }

    // Send to mock server
    fetch('/api/manifest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(manifest)
    })
      .then(res => res.json())
      .then(data => {
        alert(`Manifest generated: ${data.filename}`)
      })
      .catch(err => console.error('Failed to generate manifest:', err))
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Aurora Header */}
      <header className="aurora-header py-6 px-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-aionic-gold">
            ∞Δ Aionic Ethical Review Interface
          </h1>
          <p className="text-aionic-blue text-sm mt-2">
            Sandcastle Sequence v0.3 | ESC-1 Protocol Active | Local-Only Mode
          </p>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 grid grid-cols-12 gap-6 p-8 max-w-7xl mx-auto w-full">
        {/* Left Panel - File Index */}
        <div className="col-span-3">
          <ManifestAutoIndex
            artifacts={artifacts}
            selectedArtifact={selectedArtifact}
            onSelect={handleArtifactSelect}
            loading={loading}
          />
        </div>

        {/* Center Panel - Viewer */}
        <div className="col-span-6">
          <ManifestViewer
            artifact={selectedArtifact}
          />
        </div>

        {/* Right Panel - Ethical Checklist */}
        <div className="col-span-3">
          <EthicalChecklistPanel
            criteria={ethicalCriteria}
            notes={reviewNotes}
            onCriteriaChange={handleCriteriaChange}
            onNotesChange={setReviewNotes}
          />
        </div>
      </main>

      {/* Footer */}
      <SandboxFooter
        onGenerateManifest={handleGenerateManifest}
        selectedArtifact={selectedArtifact}
      />
    </div>
  )
}

export default App
