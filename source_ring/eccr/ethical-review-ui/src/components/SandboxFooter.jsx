import { Download, Lock, Database } from 'lucide-react'

export default function SandboxFooter({ onGenerateManifest, selectedArtifact }) {
  const allCriteriaValid = selectedArtifact !== null

  return (
    <footer className="bg-gray-800/80 backdrop-blur-sm border-t border-aionic-gold/20 py-4 px-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Left side - Status */}
        <div className="flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-aionic-blue">All Synthetic ✓</span>
          </div>
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-aionic-gold" />
            <span className="text-aionic-blue">Local-Only ✓</span>
          </div>
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-aionic-gold" />
            <span className="text-aionic-blue">Sandbox Mode ✓</span>
          </div>
        </div>

        {/* Center - Version */}
        <div className="text-xs text-aionic-blue/60 text-center">
          <div>Continuity Snapshot v0.3 — Sandcastle Sequence</div>
          <div className="mt-1">ESC-1 Active | Aionic Ethical Review Interface</div>
        </div>

        {/* Right side - Action */}
        <div>
          <button
            onClick={onGenerateManifest}
            disabled={!allCriteriaValid}
            className={`
              flex items-center gap-2 px-6 py-2 rounded-lg font-medium
              transition-all duration-200
              ${allCriteriaValid
                ? 'bg-aionic-gold text-aionic-dark hover:bg-aionic-amber shadow-lg hover:shadow-aionic-gold/50'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
              }
            `}
          >
            <Download className="w-4 h-4" />
            Generate Ethical Manifest
          </button>
        </div>
      </div>

      {/* Bottom compassion statement */}
      <div className="max-w-7xl mx-auto mt-4 pt-4 border-t border-aionic-gold/10">
        <p className="text-center text-xs text-aionic-gold/60 italic">
          "Care is the measure of intelligence." — Aionic Principle
        </p>
      </div>
    </footer>
  )
}
