import { useState } from 'react'
import { User, Target, MapPin, Clock, Sparkles, Play } from 'lucide-react'

// Dynamically assign stats based on adventure setup
// This function can work with ANY adventure type, not just pre-defined archetypes
function assignStats(setup) {
  const stats = {}
  const who = setup.who.toLowerCase()
  const what = setup.what.toLowerCase()
  const where = setup.where.toLowerCase()
  
  // Try to infer appropriate stats from the adventure context
  // This is a smart system that adapts to ANY scenario
  
  // PBtA Teen Titans / Mall Mayhem style stats
  if (setup.gameType === 'teen-titans' || who.match(/titan|hero|superhero/)) {
    return assignTeenTitansStats(setup)
  }
  
  // Default: Create dynamic stats based on the adventure
  // We'll generate 3-6 stats with +2/+1/0/0/-1 distribution
  return assignDynamicStats(setup)
}

function assignTeenTitansStats(setup) {
  const stats = {
    cool: 0,
    grit: 0,
    weird: 0,
    love: 0,
    wild: 0,
    dark: 0
  }

  const who = setup.who.toLowerCase()
  const what = setup.what.toLowerCase()
  
  // Assign primary stat (+2) based on character type
  if (who.match(/leader|strategist|planner|commander/)) {
    stats.cool = 2
  } else if (who.match(/fighter|warrior|athlete|soldier|tough/)) {
    stats.grit = 2
  } else if (who.match(/alien|wizard|psychic|mage|supernatural|mystic/)) {
    stats.weird = 2
  } else if (who.match(/friend|helper|healer|diplomat|peacemaker/)) {
    stats.love = 2
  } else if (who.match(/prankster|trickster|joker|wild|chaotic|rebel/)) {
    stats.wild = 2
  } else if (who.match(/goth|dark|shadow|demon|mysterious/)) {
    stats.dark = 2
  } else {
    // Default: balanced
    stats.cool = 1
    stats.grit = 1
  }

  // Assign secondary stat (+1) based on what they're trying to do
  if (what.match(/lead|plan|organize|command/)) {
    if (stats.cool < 2) stats.cool += 1
  } else if (what.match(/fight|battle|defeat|protect|defend/)) {
    if (stats.grit < 2) stats.grit += 1
  } else if (what.match(/magic|power|supernatural|mystical|cast/)) {
    if (stats.weird < 2) stats.weird += 1
  } else if (what.match(/help|save|befriend|heal|rescue|unite/)) {
    if (stats.love < 2) stats.love += 1
  } else if (what.match(/prank|trick|chaos|wild|disrupt|rebel/)) {
    if (stats.wild < 2) stats.wild += 1
  } else if (what.match(/dark|shadow|curse|doom|sinister/)) {
    if (stats.dark < 2) stats.dark += 1
  }

  // Fill remaining to hit PBtA standard: one +2, two +1, two 0, one -1
  const currentTotal = Object.values(stats).reduce((a, b) => a + b, 0)
  const remaining = 3 - currentTotal // Target total is +3
  
  if (remaining > 0) {
    const zeroStats = Object.keys(stats).filter(k => stats[k] === 0)
    for (let i = 0; i < Math.min(remaining, zeroStats.length); i++) {
      stats[zeroStats[i]] = 1
    }
  }
  
  // Ensure one stat is negative for balance
  const lowestStat = Object.keys(stats).find(k => stats[k] === 0)
  if (lowestStat) stats[lowestStat] = -1

  return stats
}

function assignDynamicStats(setup) {
  // For ANY other adventure, create contextual stats
  // This allows the system to work with literally anything
  
  const who = setup.who.toLowerCase()
  const what = setup.what.toLowerCase()
  const where = setup.where.toLowerCase()
  
  // Generate 4-6 relevant stats based on the adventure
  // We'll keep it simple: 4 stats with +2/+1/0/-1 distribution
  
  const stats = {}
  
  // Physical/Action stat (always relevant)
  stats.action = who.match(/fighter|athlete|warrior|soldier|explorer/) ? 2 : 
                 what.match(/fight|run|climb|jump|physical/) ? 1 : 0
  
  // Mental/Knowledge stat (always relevant)
  stats.knowledge = who.match(/scientist|detective|scholar|hacker|analyst/) ? 2 :
                    what.match(/solve|investigate|analyze|study|learn/) ? 1 : 0
  
  // Social/Influence stat (always relevant)
  stats.charm = who.match(/diplomat|leader|friend|speaker|negotiator/) ? 2 :
                what.match(/persuade|convince|befriend|lead|inspire/) ? 1 : 0
  
  // Special/Weird stat (context-dependent)
  stats.special = who.match(/wizard|alien|psychic|mutant|supernatural/) ? 2 :
                  what.match(/magic|power|abilities|strange/) ? 1 : 0
  
  // Normalize to PBtA distribution
  const statArray = Object.entries(stats).map(([key, val]) => ({key, val}))
  statArray.sort((a, b) => b.val - a.val)
  
  // Force distribution: +2, +1, 0, -1
  const finalStats = {}
  finalStats[statArray[0].key] = 2
  finalStats[statArray[1].key] = 1
  finalStats[statArray[2].key] = 0
  finalStats[statArray[3].key] = -1
  
  return finalStats
}

export default function SetupScreen({ playerNames, onComplete }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [answers, setAnswers] = useState({
    who: '',
    what: '',
    where: '',
    when: '',
    janeRole: ''
  })

  const steps = [
    {
      key: 'who',
      icon: User,
      question: 'Who are you in this adventure?',
      placeholder: 'A space explorer, a detective, a wizard, a hacker...',
      examples: ['Space explorer', 'Detective', 'Wizard', 'Hacker', 'Knight', 'Scientist']
    },
    {
      key: 'what',
      icon: Target,
      question: 'What are you trying to do?',
      placeholder: 'Find treasure, solve a mystery, save someone...',
      examples: ['Find lost treasure', 'Solve a mystery', 'Save my friend', 'Explore new worlds', 'Stop a threat']
    },
    {
      key: 'where',
      icon: MapPin,
      question: 'Where does this story begin?',
      placeholder: 'A haunted mansion, outer space, ancient ruins...',
      examples: ['Haunted mansion', 'Space station', 'Ancient ruins', 'Underground lab', 'Mysterious island']
    },
    {
      key: 'when',
      icon: Clock,
      question: 'When does this take place?',
      placeholder: 'The future, medieval times, present day...',
      examples: ['Year 3047', 'Medieval times', 'Present day', 'Wild West', 'Ancient Egypt']
    },
    {
      key: 'janeRole',
      icon: Sparkles,
      question: 'Who do you want ME (Jane) to be?',
      placeholder: 'A wise guide, your sidekick, a mysterious stranger...',
      examples: ['Wise wizard', 'Robot companion', 'Mysterious guide', 'Your best friend', 'A mentor', 'Just the narrator']
    }
  ]

  const currentStepData = steps[currentStep]
  const Icon = currentStepData.icon

  const handleNext = () => {
    if (answers[currentStepData.key].trim()) {
      if (currentStep < steps.length - 1) {
        setCurrentStep(currentStep + 1)
      } else {
        // Auto-assign stats based on answers
        const stats = assignStats(answers)
        const setupWithStats = {
          ...answers,
          stats
        }
        onComplete(setupWithStats)
      }
    }
  }

  const handleExampleClick = (example) => {
    setAnswers({
      ...answers,
      [currentStepData.key]: example
    })
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleNext()
    }
  }

  const playerNamesStr = playerNames.length > 1 
    ? playerNames.slice(0, -1).join(', ') + ' & ' + playerNames[playerNames.length - 1]
    : playerNames[0]

  return (
    <div className="min-h-screen flex items-center justify-center storybook-page p-8">
      <div className="max-w-3xl w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-jane-gold font-adventure tracking-wider mb-2">
            ADVENTURE SETUP
          </h1>
          <p className="text-jane-amber text-sm tracking-widest uppercase">
            {playerNamesStr}, tell me about your story
          </p>
        </div>

        <div className="terminal-style p-8 rounded-lg command-border">
          {/* Progress bar */}
          <div className="mb-8">
            <div className="flex justify-between mb-2">
              {steps.map((step, idx) => (
                <div
                  key={step.key}
                  className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    idx === currentStep
                      ? 'bg-jane-amber text-jane-void'
                      : idx < currentStep
                      ? 'bg-jane-forest text-gray-100'
                      : 'bg-gray-700 text-gray-500'
                  }`}
                >
                  <step.icon className="w-6 h-6" />
                </div>
              ))}
            </div>
            <div className="h-1 bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-jane-amber transition-all duration-500"
                style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Question */}
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-16 h-16 rounded-lg bg-gradient-to-br from-jane-deep-blue to-jane-amber flex items-center justify-center">
                <Icon className="w-8 h-8 text-gray-100" />
              </div>
              <h2 className="text-2xl font-bold text-gray-100">
                {currentStepData.question}
              </h2>
            </div>

            <textarea
              value={answers[currentStepData.key]}
              onChange={(e) => setAnswers({ ...answers, [currentStepData.key]: e.target.value })}
              onKeyDown={handleKeyDown}
              placeholder={currentStepData.placeholder}
              className="input-terminal w-full h-24 resize-none"
              autoFocus
            />
          </div>

          {/* Examples */}
          <div className="mb-6">
            <p className="text-sm text-gray-500 mb-3 tracking-wide uppercase">Quick Ideas:</p>
            <div className="flex flex-wrap gap-2">
              {currentStepData.examples.map((example) => (
                <button
                  key={example}
                  onClick={() => handleExampleClick(example)}
                  className="px-4 py-2 bg-gray-700 hover:bg-jane-steel text-gray-300 rounded text-sm transition-colors"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="px-6 py-3 bg-gray-700 hover:bg-jane-steel disabled:opacity-30 disabled:cursor-not-allowed text-gray-300 rounded-lg transition-colors uppercase tracking-wide font-bold"
            >
              Back
            </button>

            <div className="text-sm text-gray-500 tracking-wide">
              {currentStep + 1} / {steps.length}
            </div>

            <button
              onClick={handleNext}
              disabled={!answers[currentStepData.key].trim()}
              className="send-button"
            >
              <span className="flex items-center gap-2">
                {currentStep === steps.length - 1 ? (
                  <>
                    <Play className="w-5 h-5" />
                    START ADVENTURE
                  </>
                ) : (
                  <>
                    Next
                  </>
                )}
              </span>
            </button>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-700 text-center text-xs text-gray-500 tracking-wide">
            ENTER: NEXT • Your answers shape the entire story
          </div>
        </div>
      </div>
    </div>
  )
}
