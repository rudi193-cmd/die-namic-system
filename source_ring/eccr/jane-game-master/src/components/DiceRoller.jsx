import { useState } from 'react'
import { Dices, Sparkles } from 'lucide-react'

// Dynamic stat color generation based on stat name
function getStatColor(statName) {
  const colorMap = {
    // Common PBtA stats
    cool: 'from-blue-400 to-cyan-300',
    grit: 'from-red-500 to-orange-400',
    weird: 'from-purple-500 to-violet-400',
    love: 'from-pink-500 to-rose-400',
    wild: 'from-green-500 to-emerald-400',
    dark: 'from-gray-800 to-purple-900',
    // Dungeon World style
    strength: 'from-red-600 to-orange-500',
    dexterity: 'from-green-600 to-teal-500',
    constitution: 'from-orange-600 to-amber-500',
    intelligence: 'from-blue-600 to-indigo-500',
    wisdom: 'from-purple-600 to-violet-500',
    charisma: 'from-pink-600 to-rose-500',
    // Generic stats
    action: 'from-red-500 to-orange-400',
    knowledge: 'from-blue-500 to-indigo-400',
    charm: 'from-pink-500 to-rose-400',
    special: 'from-purple-500 to-violet-400',
    // Generic fallback
    default: 'from-gray-600 to-gray-400'
  }
  
  return colorMap[statName?.toLowerCase()] || colorMap.default
}

export default function DiceRoller({ stat, statLabel, modifier, onRollComplete }) {
  const [isRolling, setIsRolling] = useState(false)
  const [dice1, setDice1] = useState(null)
  const [dice2, setDice2] = useState(null)
  const [total, setTotal] = useState(null)
  const [showResult, setShowResult] = useState(false)

  const rollDice = () => {
    setIsRolling(true)
    setShowResult(false)
    
    // Animate dice rolling
    let rollCount = 0
    const maxRolls = 15
    const rollInterval = setInterval(() => {
      setDice1(Math.floor(Math.random() * 6) + 1)
      setDice2(Math.floor(Math.random() * 6) + 1)
      rollCount++
      
      if (rollCount >= maxRolls) {
        clearInterval(rollInterval)
        
        // Final roll - 2d6
        const finalDice1 = Math.floor(Math.random() * 6) + 1
        const finalDice2 = Math.floor(Math.random() * 6) + 1
        const diceSum = finalDice1 + finalDice2
        const finalTotal = diceSum + modifier
        
        setDice1(finalDice1)
        setDice2(finalDice2)
        setTotal(finalTotal)
        setIsRolling(false)
        setShowResult(true)
        
        // Send result back to parent after showing it
        setTimeout(() => {
          onRollComplete(finalTotal)
        }, 2000)
      }
    }, 80)
  }

  const gradientClass = getStatColor(stat)
  const displayStat = statLabel || stat || 'Roll'

  return (
    <div className="flex justify-center py-4">
      <div className="terminal-style p-6 rounded-lg command-border max-w-md w-full">
        <div className="text-center space-y-4">
          {/* Stat indicator */}
          <div className="flex items-center justify-center gap-2">
            <div className={`px-4 py-2 rounded-lg bg-gradient-to-r ${gradientClass} text-white font-bold uppercase tracking-wide`}>
              {displayStat}
            </div>
            <div className="text-gray-400 text-sm">
              {modifier >= 0 ? '+' : ''}{modifier}
            </div>
          </div>

          {/* Dice display */}
          {!showResult && (
            <div className="relative">
              <button
                onClick={rollDice}
                disabled={isRolling}
                className={`
                  w-full max-w-sm mx-auto p-6 rounded-2xl
                  bg-gradient-to-br ${gradientClass}
                  flex items-center justify-center gap-6
                  shadow-lg border-4 border-white/20
                  transition-all duration-200
                  ${isRolling 
                    ? 'animate-pulse cursor-wait' 
                    : 'hover:scale-105 active:scale-95 cursor-pointer'
                  }
                `}
              >
                {isRolling ? (
                  <>
                    <div className="w-20 h-20 rounded-lg bg-white/20 flex items-center justify-center">
                      <span className="text-5xl font-bold text-white animate-bounce">
                        {dice1}
                      </span>
                    </div>
                    <div className="w-20 h-20 rounded-lg bg-white/20 flex items-center justify-center">
                      <span className="text-5xl font-bold text-white animate-bounce" style={{ animationDelay: '0.1s' }}>
                        {dice2}
                      </span>
                    </div>
                  </>
                ) : (
                  <div className="flex items-center gap-4">
                    <Dices className="w-16 h-16 text-white" />
                    <span className="text-2xl font-bold text-white">2d6</span>
                  </div>
                )}
              </button>
              
              {!isRolling && !dice1 && (
                <div className="mt-4 flex items-center justify-center gap-2 text-gray-400">
                  <Sparkles className="w-4 h-4 animate-pulse" />
                  <p className="text-sm tracking-wide">Click to roll 2d6!</p>
                  <Sparkles className="w-4 h-4 animate-pulse" />
                </div>
              )}
            </div>
          )}

          {/* Result display */}
          {showResult && (
            <div className="space-y-3 animate-fade-in">
              <div className="flex items-center justify-center gap-3 text-2xl font-bold flex-wrap">
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-2 rounded-lg bg-gradient-to-r ${gradientClass} text-white`}>
                    {dice1}
                  </span>
                  <span className="text-gray-500">+</span>
                  <span className={`px-3 py-2 rounded-lg bg-gradient-to-r ${gradientClass} text-white`}>
                    {dice2}
                  </span>
                </div>
                <span className="text-gray-500">+</span>
                <span className="text-gray-400">{modifier}</span>
                <span className="text-gray-500">=</span>
                <span className={`px-4 py-2 rounded-lg bg-gradient-to-r ${gradientClass} text-white animate-pulse text-3xl`}>
                  {total}
                </span>
              </div>
              
              <div className="flex items-center justify-center gap-2 text-jane-gold animate-pulse">
                <Sparkles className="w-5 h-5" />
                <p className="text-lg tracking-wide">Result!</p>
                <Sparkles className="w-5 h-5" />
              </div>

              {/* PBtA Outcome hint */}
              <div className="text-sm text-gray-300 pt-2 font-bold">
                {total >= 10 ? '🌟 FULL SUCCESS!' : total >= 7 ? '⚡ PARTIAL SUCCESS' : '💥 MISS!'}
              </div>
              <div className="text-xs text-gray-500">
                {total >= 10 ? 'You do it perfectly!' : total >= 7 ? 'You do it, but with a cost...' : 'Things get complicated!'}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
