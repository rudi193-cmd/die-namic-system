import { Eye, Shield, Database } from 'lucide-react'

export default function ManifestViewer({ artifact }) {
  if (!artifact) {
    return (
      <div className="ethical-panel h-full flex items-center justify-center">
        <div className="text-center">
          <Database className="w-16 h-16 text-aionic-blue/40 mx-auto mb-4" />
          <p className="text-aionic-blue/60">
            Select an artifact from the left to view its contents
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="ethical-panel h-full">
      {/* Header */}
      <div className="mb-6 pb-4 border-b border-aionic-gold/20">
        <div className="flex items-start justify-between mb-2">
          <h2 className="text-2xl font-bold text-aionic-gold">{artifact.title}</h2>
          <div className="flex items-center gap-2 text-xs">
            {artifact.synthetic && (
              <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded">
                SYNTHETIC
              </span>
            )}
            <span className="px-2 py-1 bg-aionic-blue/20 text-aionic-blue rounded">
              {artifact.source_classification}
            </span>
          </div>
        </div>
        
        <div className="text-sm text-gray-400 space-y-1">
          <div>ID: {artifact.id}</div>
          <div>Category: {artifact.category}</div>
          <div>Created: {new Date(artifact.created_at).toLocaleDateString()}</div>
        </div>
      </div>

      {/* Content */}
      <div className="space-y-4 max-h-[calc(100vh-450px)] overflow-y-auto pr-2">
        <div>
          <h3 className="text-lg font-semibold text-aionic-gold mb-2 flex items-center gap-2">
            <Eye className="w-4 h-4" />
            Description
          </h3>
          <p className="text-gray-300 text-sm leading-relaxed">
            {artifact.description}
          </p>
        </div>

        {artifact.content && (
          <div>
            <h3 className="text-lg font-semibold text-aionic-gold mb-2">Content Preview</h3>
            <div className="bg-gray-900/50 rounded p-4 text-sm text-gray-300 font-mono whitespace-pre-wrap max-h-96 overflow-y-auto">
              {artifact.content}
            </div>
          </div>
        )}

        {artifact.ethical_tags && artifact.ethical_tags.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-aionic-gold mb-2 flex items-center gap-2">
              <Shield className="w-4 h-4" />
              Ethical Tags
            </h3>
            <div className="flex flex-wrap gap-2">
              {artifact.ethical_tags.map((tag, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-aionic-gold/10 text-aionic-gold text-xs rounded-full border border-aionic-gold/30"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer Quote */}
      <div className="mt-6 pt-4 border-t border-aionic-gold/20">
        <blockquote className="compassion-quote">
          "Care is the measure of intelligence. Every manifest begins and ends in consent."
          <div className="text-xs text-aionic-blue/60 mt-1">— Aionic Principle</div>
        </blockquote>
      </div>
    </div>
  )
}
