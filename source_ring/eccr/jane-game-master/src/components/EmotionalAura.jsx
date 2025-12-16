export default function EmotionalAura({ state }) {
  const auraClass = {
    calm: 'aura-calm',
    concerned: 'aura-concerned',
    distressed: 'aura-distressed'
  }[state] || 'aura-calm'

  return <div className={`emotional-aura ${auraClass}`} />
}
