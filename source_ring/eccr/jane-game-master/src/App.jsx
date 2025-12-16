import { useState, useEffect, useRef } from 'react'
import ChatMessage from './components/ChatMessage'
import InputArea from './components/InputArea'
import DiceRoller from './components/DiceRoller'
import EmotionalAura from './components/EmotionalAura'
import TypingIndicator from './components/TypingIndicator'
import WelcomeScreen from './components/WelcomeScreen'
import SetupScreen from './components/SetupScreen'
import GoalSelectionScreen from './components/GoalSelectionScreen'
import HarmonicThemeProvider from './components/HarmonicThemeProvider'
import PaperLayer from './components/PaperLayer'
import { Terminal } from 'lucide-react'

function App() {
  const [messages, setMessages] = useState([])
  const [isJaneTyping, setIsJaneTyping] = useState(false)
  const [emotionalState, setEmotionalState] = useState('calm')
  const [playerNames, setPlayerNames] = useState(null)
  const [characterStats, setCharacterStats] = useState(null)
  const [adventureSetup, setAdventureSetup] = useState(null)
  const [showWelcome, setShowWelcome] = useState(true)
  const [showSetup, setShowSetup] = useState(false)
  const [showGoalSelection, setShowGoalSelection] = useState(false)
  const [setupAnswers, setSetupAnswers] = useState(null)
  const [awaitingRoll, setAwaitingRoll] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleNamesSubmit = (names) => {
    setPlayerNames(names)
    setShowWelcome(false)
    setShowSetup(true)
  }

  const handleSetupComplete = (setup) => {
    setSetupAnswers(setup)
    setShowSetup(false)
    setShowGoalSelection(true)
  }

  const handleGoalComplete = async (finalSetup) => {
    setAdventureSetup(finalSetup)
    setShowGoalSelection(false)
    setIsJaneTyping(true)

    try {
      const response = await fetch('/api/create-scene', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          playerNames,
          setup: finalSetup
        })
      })

      const data = await response.json()
      setCharacterStats(data.characterStats)
      
      setTimeout(() => {
        const openingMsg = {
          id: Date.now(),
          sender: 'jane',
          text: data.openingScene,
          timestamp: new Date().toISOString()
        }
        setMessages([openingMsg])
        setIsJaneTyping(false)
      }, 2000)
      
    } catch (error) {
      console.error('Failed to create scene:', error)
      setIsJaneTyping(false)
      
      const fallbackMsg = {
        id: Date.now(),
        sender: 'jane',
        text: `${playerNames.join(' & ')}, your adventure begins...`,
        timestamp: new Date().toISOString()
      }
      setMessages([fallbackMsg])
    }
  }

  const handleSendMessage = async (text) => {
    const playerMsg = {
      id: Date.now(),
      sender: 'player',
      text,
      timestamp: new Date().toISOString()
    }
    
    setMessages(prev => [...prev, playerMsg])
    setIsJaneTyping(true)

    try {
      const response = await fetch('/api/narrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          playerNames,
          playerAction: text,
          adventureSetup,
          characterStats,
          conversationHistory: messages.slice(-5)
        })
      })

      const data = await response.json()
      
      setTimeout(() => {
        if (data.requiresRoll) {
          setAwaitingRoll({
            stat: data.rollStat,
            statLabel: data.rollStatLabel || data.rollStat,
            modifier: characterStats[data.rollStat] || 0,
            action: text
          })
          
          const janeMsg = {
            id: Date.now() + 1,
            sender: 'jane',
            text: data.narrative,
            timestamp: new Date().toISOString(),
            requiresRoll: true,
            rollStat: data.rollStat
          }
          
          setMessages(prev => [...prev, janeMsg])
          setIsJaneTyping(false)
        } else {
          const janeMsg = {
            id: Date.now() + 1,
            sender: 'jane',
            text: data.narrative,
            timestamp: new Date().toISOString(),
            eccrTriggered: data.eccrTriggered || false
          }
          
          setMessages(prev => [...prev, janeMsg])
          setIsJaneTyping(false)
          
          if (data.emotionalState) {
            setEmotionalState(data.emotionalState)
          }
        }
      }, 1500)
      
    } catch (error) {
      console.error('Failed to get Jane\'s response:', error)
      setIsJaneTyping(false)
      
      const fallbackMsg = {
        id: Date.now() + 1,
        sender: 'jane',
        text: "Connection disrupted. Stand by. Try that again?",
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, fallbackMsg])
    }
  }

  const handleRollComplete = async (total) => {
    if (!awaitingRoll) return

    setIsJaneTyping(true)
    setAwaitingRoll(null)

    try {
      const response = await fetch('/api/resolve-roll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          playerNames,
          action: awaitingRoll.action,
          stat: awaitingRoll.stat,
          rollTotal: total,
          adventureSetup,
          conversationHistory: messages.slice(-5)
        })
      })

      const data = await response.json()
      
      setTimeout(() => {
        const resultMsg = {
          id: Date.now(),
          sender: 'jane',
          text: data.narrative,
          timestamp: new Date().toISOString(),
          rollResult: data.outcome
        }
        
        setMessages(prev => [...prev, resultMsg])
        setIsJaneTyping(false)
        
        if (data.emotionalState) {
          setEmotionalState(data.emotionalState)
        }
      }, 1000)
      
    } catch (error) {
      console.error('Failed to resolve roll:', error)
      setIsJaneTyping(false)
    }
  }

  const renderContent = () => {
    if (showWelcome) {
      return <WelcomeScreen onNameSubmit={handleNamesSubmit} />
    }

    if (showSetup) {
      return <SetupScreen playerNames={playerNames} onComplete={handleSetupComplete} />
    }

    if (showGoalSelection) {
      return <GoalSelectionScreen playerNames={playerNames} setup={setupAnswers} onComplete={handleGoalComplete} />
    }

    const displayName = playerNames.length > 1 
      ? playerNames.join(' & ')
      : playerNames[0]

    return (
      <div className="min-h-screen flex flex-col storybook-page">
        <header className="command-border terminal-style p-4 m-4 mb-0">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="jane-avatar">
                  <Terminal className="w-6 h-6 text-gray-100" />
                </div>
                <EmotionalAura state={emotionalState} />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-jane-gold font-adventure tracking-wide">
                  {adventureSetup?.janeRole || 'JANE'}
                </h1>
                <p className="text-sm text-jane-amber uppercase tracking-wider">GM: {displayName}</p>
              </div>
            </div>
            <div className="text-right">
              <div className="gm-badge">
                <span className="w-2 h-2 bg-jane-forest rounded-sm animate-pulse-glow"></span>
                <span>LIVE</span>
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-hidden flex flex-col max-w-4xl w-full mx-auto p-4">
          <div className="flex-1 overflow-y-auto space-y-4 pb-4">
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} janeRole={adventureSetup?.janeRole} />
            ))}
            
            {awaitingRoll && (
              <DiceRoller
                stat={awaitingRoll.stat}
                statLabel={awaitingRoll.statLabel}
                modifier={awaitingRoll.modifier}
                onRollComplete={handleRollComplete}
              />
            )}
            
            {isJaneTyping && !awaitingRoll && <TypingIndicator />}
            
            <div ref={messagesEndRef} />
          </div>

          <InputArea onSend={handleSendMessage} disabled={isJaneTyping || awaitingRoll !== null} />
        </main>

        <footer className="text-center py-3 text-xs text-gray-600 tracking-wide">
          <p>SYSTEM STATUS: OPERATIONAL • ESC-1 ACTIVE</p>
        </footer>
      </div>
    )
  }

  return (
    <HarmonicThemeProvider adventureSetup={adventureSetup}>
      <PaperLayer>
        {renderContent()}
      </PaperLayer>
    </HarmonicThemeProvider>
  )
}

export default App
