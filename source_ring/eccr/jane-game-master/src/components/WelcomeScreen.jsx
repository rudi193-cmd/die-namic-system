import { useState } from 'react'
import { BookOpen, Shield, Users } from 'lucide-react'

export default function WelcomeScreen({ onNameSubmit }) {
  const [playerCount, setPlayerCount] = useState(1)
  const [names, setNames] = useState([''])

  const handlePlayerCountChange = (count) => {
    setPlayerCount(count)
    const newNames = Array(count).fill('').map((_, i) => names[i] || '')
    setNames(newNames)
  }

  const handleNameChange = (index, value) => {
    const newNames = [...names]
    newNames[index] = value
    setNames(newNames)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const filledNames = names.filter(n => n.trim())
    if (filledNames.length === playerCount) {
      onNameSubmit(filledNames)
    }
  }

  const allNamesFilled = names.filter(n => n.trim()).length === playerCount

  return (
    <div className="min-h-screen flex items-center justify-center storybook-page p-8">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-12">
          <div className="inline-block mb-6">
            <div className="w-32 h-32 rounded-lg bg-gradient-to-br from-jane-deep-blue via-jane-amber to-jane-forest mx-auto flex items-center justify-center shadow-[0_0_30px_rgba(212,175,55,0.3)]">
              <BookOpen className="w-16 h-16 text-gray-100" />
            </div>
          </div>
          
          <h1 className="text-6xl font-bold text-jane-gold mb-4 font-adventure tracking-wider">
            JANE
          </h1>
          <div className="text-xl text-jane-amber mb-2 tracking-widest font-bold">
            GAME MASTER
          </div>
          
          <p className="text-lg text-gray-300 leading-relaxed max-w-lg mx-auto mt-6">
            Choose your path. Shape your story. Every decision matters.
          </p>
        </div>

        <div className="terminal-style p-8 rounded-lg command-border max-w-md mx-auto">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Player count selector */}
            <div>
              <label className="block text-jane-amber font-bold mb-3 text-sm tracking-wide uppercase flex items-center gap-2">
                <Users className="w-4 h-4" />
                Number of Players
              </label>
              <div className="grid grid-cols-4 gap-2">
                {[1, 2, 3, 4].map(count => (
                  <button
                    key={count}
                    type="button"
                    onClick={() => handlePlayerCountChange(count)}
                    className={`py-3 rounded-lg font-bold transition-colors ${
                      playerCount === count
                        ? 'bg-jane-amber text-jane-void'
                        : 'bg-gray-700 text-gray-400 hover:bg-jane-steel'
                    }`}
                  >
                    {count}
                  </button>
                ))}
              </div>
            </div>

            {/* Name inputs */}
            <div className="space-y-3">
              {Array(playerCount).fill(0).map((_, index) => (
                <div key={index}>
                  <label className="block text-jane-amber font-bold mb-2 text-xs tracking-wide uppercase">
                    Player {index + 1} Name
                  </label>
                  <input
                    type="text"
                    value={names[index] || ''}
                    onChange={(e) => handleNameChange(index, e.target.value)}
                    placeholder="Type here..."
                    className="w-full input-terminal"
                    autoFocus={index === 0}
                  />
                </div>
              ))}
            </div>

            <button
              type="submit"
              disabled={!allNamesFilled}
              className="w-full send-button text-base uppercase tracking-wide"
            >
              <span className="flex items-center justify-center gap-2">
                <BookOpen className="w-5 h-5" />
                Continue
              </span>
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-gray-700">
            <div className="flex items-start gap-3 text-sm text-gray-400">
              <Shield className="w-5 h-5 text-jane-forest flex-shrink-0 mt-0.5" />
              <p className="leading-relaxed">
                Safe space. Your choices matter. Jane checks in if things feel tough.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center space-y-2">
          <div className="gm-badge mx-auto">
            <span className="w-2 h-2 bg-jane-forest rounded-sm animate-pulse-glow"></span>
            <span>SANDBOX MODE</span>
          </div>
          <p className="text-xs text-gray-500">
            Age 9-12 • ESC-1 Protected
          </p>
        </div>
      </div>
    </div>
  )
}
