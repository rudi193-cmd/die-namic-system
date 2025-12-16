import { FileText, CheckCircle, AlertCircle, Clock } from 'lucide-react'

export default function ManifestAutoIndex({ artifacts, selectedArtifact, onSelect, loading }) {
  const getStatusIcon = (artifact) => {
    if (artifact.status === 'verified') {
      return <CheckCircle className="w-4 h-4 text-green-400" />
    } else if (artifact.status === 'pending') {
      return <Clock className="w-4 h-4 text-yellow-400" />
    } else {
      return <AlertCircle className="w-4 h-4 text-red-400" />
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      theory: 'text-blue-400',
      governance: 'text-purple-400',
      sandbox: 'text-green-400',
      narrative: 'text-pink-400',
    }
    return colors[category] || 'text-gray-400'
  }

  if (loading) {
    return (
      <div className="ethical-panel h-full">
        <h2 className="text-xl font-semibold text-aionic-gold mb-4">Artifact Index</h2>
        <div className="flex items-center justify-center h-64">
          <div className="animate-pulse text-aionic-blue">Loading artifacts...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="ethical-panel h-full">
      <h2 className="text-xl font-semibold text-aionic-gold mb-4 flex items-center gap-2">
        <FileText className="w-5 h-5" />
        Artifact Index
      </h2>

      <div className="space-y-2 max-h-[calc(100vh-300px)] overflow-y-auto pr-2">
        {artifacts.length === 0 ? (
          <div className="text-aionic-blue/60 text-sm text-center py-8">
            No artifacts found. Start the mock server to load synthetic data.
          </div>
        ) : (
          artifacts.map((artifact) => (
            <div
              key={artifact.id}
              className={`manifest-item ${selectedArtifact?.id === artifact.id ? 'selected' : ''}`}
              onClick={() => onSelect(artifact)}
            >
              <div className="flex items-start gap-2">
                {getStatusIcon(artifact)}
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm truncate">
                    {artifact.title}
                  </div>
                  <div className={`text-xs mt-1 ${getCategoryColor(artifact.category)}`}>
                    {artifact.category}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    {artifact.id}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-aionic-gold/20">
        <div className="text-xs text-aionic-blue/60">
          <div className="flex items-center gap-2 mb-1">
            <CheckCircle className="w-3 h-3 text-green-400" /> Verified
          </div>
          <div className="flex items-center gap-2 mb-1">
            <Clock className="w-3 h-3 text-yellow-400" /> Pending Review
          </div>
          <div className="flex items-center gap-2">
            <AlertCircle className="w-3 h-3 text-red-400" /> Needs Attention
          </div>
        </div>
      </div>
    </div>
  )
}
