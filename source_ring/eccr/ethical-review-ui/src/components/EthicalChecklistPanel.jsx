import { Shield, CheckCircle, XCircle } from 'lucide-react'

export default function EthicalChecklistPanel({ criteria, notes, onCriteriaChange, onNotesChange }) {
  const checklistItems = [
    {
      key: 'consentVerified',
      label: 'Consent Integrity',
      description: 'No traceable personal references or unapproved data reuse',
    },
    {
      key: 'neutralityAligned',
      label: 'Symbolic Neutrality',
      description: 'No implicit belief systems, diagnoses, or cultural ownership',
    },
    {
      key: 'redactionTransparent',
      label: 'Redaction Transparency',
      description: 'Math/structure public, narrative private',
    },
    {
      key: 'continuityIntact',
      label: 'Continuity Integrity',
      description: 'Maintains coherence with Aionic principles',
    },
  ]

  return (
    <div className="ethical-panel h-full">
      <h2 className="text-xl font-semibold text-aionic-gold mb-4 flex items-center gap-2">
        <Shield className="w-5 h-5" />
        Ethical Review Criteria
      </h2>

      <div className="space-y-4">
        {checklistItems.map((item) => (
          <div key={item.key} className="bg-gray-700/30 rounded p-3">
            <label className="flex items-start gap-3 cursor-pointer">
              <div className="pt-1">
                <input
                  type="checkbox"
                  checked={criteria[item.key]}
                  onChange={(e) => onCriteriaChange(item.key, e.target.checked)}
                  className="w-4 h-4 rounded border-aionic-gold/40 bg-gray-800 
                           checked:bg-aionic-gold checked:border-aionic-gold
                           focus:ring-2 focus:ring-aionic-gold/50"
                />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-sm text-gray-200">
                    {item.label}
                  </span>
                  {criteria[item.key] ? (
                    <CheckCircle className="w-3 h-3 text-green-400" />
                  ) : (
                    <XCircle className="w-3 h-3 text-gray-500" />
                  )}
                </div>
                <p className="text-xs text-gray-400 leading-relaxed">
                  {item.description}
                </p>
              </div>
            </label>
          </div>
        ))}
      </div>

      {/* Notes Section */}
      <div className="mt-6">
        <label className="block text-sm font-medium text-aionic-gold mb-2">
          Reviewer Notes
        </label>
        <textarea
          value={notes}
          onChange={(e) => onNotesChange(e.target.value)}
          placeholder="Add ethical reflections, observations, or special concerns..."
          className="w-full h-32 px-3 py-2 bg-gray-800/50 border border-aionic-gold/20 
                   rounded text-sm text-gray-200 placeholder-gray-500
                   focus:outline-none focus:border-aionic-gold/60 focus:ring-2 focus:ring-aionic-gold/30
                   resize-none"
        />
      </div>

      {/* Status Indicator */}
      <div className="mt-4 pt-4 border-t border-aionic-gold/20">
        <div className="flex items-center justify-between text-xs">
          <span className="text-aionic-blue/60">ESC-1 Protocol</span>
          <span className="flex items-center gap-1 text-green-400">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            Active
          </span>
        </div>
      </div>
    </div>
  )
}
