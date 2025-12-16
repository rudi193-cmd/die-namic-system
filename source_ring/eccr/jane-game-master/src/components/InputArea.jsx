import { useState } from 'react'
import { Send } from 'lucide-react'

export default function InputArea({ onSend, disabled }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="command-border terminal-style p-4 mt-4">
      <div className="flex gap-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter command..."
          disabled={disabled}
          className="input-terminal flex-1 resize-none h-20"
          rows={3}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="send-button h-20"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
      <div className="mt-2 text-xs text-gray-600 text-center tracking-wide">
        ENTER: SEND • SHIFT+ENTER: NEW LINE
      </div>
    </form>
  )
}
