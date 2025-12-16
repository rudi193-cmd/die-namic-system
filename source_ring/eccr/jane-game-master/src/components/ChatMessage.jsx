import { Terminal, User } from 'lucide-react'

export default function ChatMessage({ message, janeRole }) {
  const isJane = message.sender === 'jane'
  const janeName = janeRole || 'JANE'
  
  return (
    <div className={`flex gap-3 ${isJane ? '' : 'flex-row-reverse'}`}>
      <div className={isJane ? 'jane-avatar' : 'w-12 h-12 rounded-lg bg-gradient-to-br from-jane-steel to-jane-electric flex items-center justify-center shadow-lg border border-jane-electric/60'}>
        {isJane ? (
          <Terminal className="w-6 h-6 text-gray-100" />
        ) : (
          <User className="w-6 h-6 text-gray-100" />
        )}
      </div>
      
      <div className={`max-w-[70%] ${isJane ? 'jane-message' : 'player-message'}`}>
        <div className="text-xs font-bold mb-2 tracking-widest uppercase" style={{ color: isJane ? '#FFA726' : '#00BCD4' }}>
          {isJane ? janeName : 'YOU'}
        </div>
        <div className="whitespace-pre-wrap leading-relaxed font-story">
          {message.text}
        </div>
        {message.eccrTriggered && (
          <div className="mt-3 pt-3 border-t border-jane-amber/30 text-xs text-jane-amber italic">
            ⚡ STATUS CHECK INITIATED
          </div>
        )}
      </div>
    </div>
  )
}
