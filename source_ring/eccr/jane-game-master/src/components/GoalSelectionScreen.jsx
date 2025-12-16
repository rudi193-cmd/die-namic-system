import { useState } from 'react'
import { Target, Sparkles, Edit3 } from 'lucide-react'

export default function GoalSelectionScreen({ playerNames, setup, onComplete }) {
  const [selectedGoal, setSelectedGoal] = useState(null)
  const [customGoal, setCustomGoal] = useState('')
  const [isCustom, setIsCustom] = useState(false)

  // Generate 3 goal suggestions based on setup
  const generateGoalSuggestions = () => {
    const who = setup.who.toLowerCase()
    const what = setup.what.toLowerCase()
    const where = setup.where.toLowerCase()
    
    const suggestions = []
    
    // Suggestion 1: Direct confrontation/challenge
    if (what.includes('stop') || what.includes('defeat') || what.includes('fight')) {
      suggestions.push(`Defeat the villain threatening ${where}`)
    } else if (what.includes('find') || what.includes('discover') || what.includes('search')) {
      suggestions.push(`Find what you're looking for before time runs out`)
    } else if (what.includes('save') || what.includes('rescue') || what.includes('help')) {
      suggestions.push(`Save everyone from the danger ahead`)
    } else {
      suggestions.push(`Complete your mission and prove yourself`)
    }
    
    // Suggestion 2: Mystery/Investigation
    if (where.match(/city|town|mall|school|station/)) {
      suggestions.push(`Uncover the mystery behind the strange events`)
    } else if (where.match(/space|galaxy|planet|ship/)) {
      suggestions.push(`Discover the truth about this place`)
    } else if (where.match(/forest|cave|ruins|dungeon|temple/)) {
      suggestions.push(`Explore the secrets hidden here`)
    } else {
      suggestions.push(`Investigate what's really going on`)
    }
    
    // Suggestion 3: Personal/Team goal
    if (who.match(/team|group|squad|crew|friends/)) {
      suggestions.push(`Prove your team is the best and work together`)
    } else if (who.match(/hero|champion|warrior|fighter/)) {
      suggestions.push(`Show everyone what a true hero can do`)
    } else if (who.match(/detective|investigator|spy|agent/)) {
      suggestions.push(`Solve the case no one else could crack`)
    } else {
      suggestions.push(`Achieve what no one thought was possible`)
    }
    
    return suggestions
  }

  const goalSuggestions = generateGoalSuggestions()

  const handleSelectGoal = (goal) => {
    setSelectedGoal(goal)
    setIsCustom(false)
    setCustomGoal('')
  }

  const handleCustomGoal = () => {
    setIsCustom(true)
    setSelectedGoal(null)
  }

  const handleContinue = () => {
    const finalGoal = isCustom ? customGoal : selectedGoal
    if (finalGoal && finalGoal.trim()) {
      onComplete({
        ...setup,
        goal: finalGoal
      })
    }
  }

  const playerNamesStr = playerNames.length > 1 
    ? playerNames.slice(0, -1).join(', ') + ' & ' + playerNames[playerNames.length - 1]
    : playerNames[0]

  const canContinue = (selectedGoal && !isCustom) || (isCustom && customGoal.trim())

  return (
    <div className="min-h-screen flex items-center justify-center storybook-page p-8">
      <div className="max-w-3xl w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-jane-gold font-adventure tracking-wider mb-2">
            CAMPAIGN GOAL
          </h1>
          <p className="text-jane-amber text-sm tracking-widest uppercase">
            {playerNamesStr}, what are you trying to achieve?
          </p>
        </div>

        <div className="terminal-style p-8 rounded-lg command-border space-y-6">
          {/* Jane's Suggestions */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Sparkles className="w-6 h-6 text-jane-gold" />
              <h2 className="text-xl font-bold text-gray-100">
                Jane's Suggestions
              </h2>
            </div>

            <div className="space-y-3">
              {goalSuggestions.map((goal, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectGoal(goal)}
                  className={`
                    w-full p-4 rounded-lg text-left transition-all
                    ${selectedGoal === goal
                      ? 'bg-gradient-to-r from-jane-deep-blue to-jane-amber text-white border-2 border-jane-gold'
                      : 'bg-gray-700 hover:bg-jane-steel text-gray-300 border-2 border-transparent hover:border-jane-gold/30'
                    }
                  `}
                >
                  <div className="flex items-start gap-3">
                    <Target className="w-5 h-5 mt-1 flex-shrink-0" />
                    <span className="font-semibold">{goal}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Custom Goal Option */}
          <div className="pt-6 border-t border-gray-700">
            <div className="flex items-center gap-3 mb-4">
              <Edit3 className="w-6 h-6 text-jane-electric" />
              <h2 className="text-xl font-bold text-gray-100">
                Your Own Goal
              </h2>
            </div>

            {!isCustom ? (
              <button
                onClick={handleCustomGoal}
                className="w-full p-4 rounded-lg bg-gray-700 hover:bg-jane-steel text-gray-300 border-2 border-transparent hover:border-jane-electric/50 transition-all text-left"
              >
                <div className="flex items-start gap-3">
                  <Sparkles className="w-5 h-5 mt-1 flex-shrink-0 text-jane-electric" />
                  <span className="font-semibold">Write your own campaign goal...</span>
                </div>
              </button>
            ) : (
              <div>
                <textarea
                  value={customGoal}
                  onChange={(e) => setCustomGoal(e.target.value)}
                  placeholder="Describe what you want to achieve in this adventure..."
                  className="input-terminal w-full h-32 resize-none mb-3"
                  autoFocus
                />
                <button
                  onClick={() => {
                    setIsCustom(false)
                    setCustomGoal('')
                  }}
                  className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
                >
                  ← Back to suggestions
                </button>
              </div>
            )}
          </div>

          {/* Continue Button */}
          <div className="pt-6 flex justify-end">
            <button
              onClick={handleContinue}
              disabled={!canContinue}
              className="send-button flex items-center gap-2"
            >
              <span>START ADVENTURE</span>
              <Sparkles className="w-5 h-5" />
            </button>
          </div>

          <div className="pt-2 text-center text-xs text-gray-500 tracking-wide">
            Your goal drives the story. Choose wisely!
          </div>
        </div>
      </div>
    </div>
  )
}
