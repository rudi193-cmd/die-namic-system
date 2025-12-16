import { createContext, useContext, useState, useEffect } from 'react'

/**
 * HarmonicThemeProvider.jsx - Adventure-Based Color Theming
 * Detects adventure type and shifts the visual palette
 */

export const HarmonicContext = createContext({
  signature: null,
  isTransitioning: false
})

// Base harmonic signatures for different adventure types
const HARMONIC_SIGNATURES = {
  space: {
    name: 'Cosmic Vastness',
    baseColor: '#1a2942',      // Deep indigo
    accentColor: '#00bcd4',    // Cyan
    glowColor: 'rgba(0, 188, 212, 0.25)'
  },
  fantasy: {
    name: 'Mythic Wonder',
    baseColor: '#2d1f0f',      // Dark amber
    accentColor: '#d4af37',    // Gold
    glowColor: 'rgba(212, 175, 55, 0.25)'
  },
  cyber: {
    name: 'Digital Edge',
    baseColor: '#1a0f2e',      // Deep violet
    accentColor: '#c026d3',    // Magenta
    glowColor: 'rgba(192, 38, 211, 0.25)'
  },
  nature: {
    name: 'Living Earth',
    baseColor: '#0f2d1a',      // Dark green
    accentColor: '#84cc16',    // Yellow-green
    glowColor: 'rgba(132, 204, 22, 0.25)'
  },
  neutral: {
    name: 'Balanced Presence',
    baseColor: '#0D1117',      // Current dark
    accentColor: '#d4af37',    // Gold
    glowColor: 'rgba(212, 175, 55, 0.25)'
  }
}

// Detect adventure type from setup answers
function detectAdventureHarmonic(setup) {
  if (!setup) return HARMONIC_SIGNATURES.neutral

  const context = `${setup.who} ${setup.what} ${setup.where} ${setup.when}`.toLowerCase()
  
  // Check for space/sci-fi
  if (context.match(/space|alien|robot|cyber|future|tech|ship|station|galaxy|star|planet/)) {
    return HARMONIC_SIGNATURES.space
  }
  
  // Check for fantasy
  if (context.match(/magic|wizard|dragon|knight|castle|fantasy|quest|spell|enchant|realm/)) {
    return HARMONIC_SIGNATURES.fantasy
  }
  
  // Check for cyber/noir
  if (context.match(/hack|neon|digital|matrix|code|virtual|dystopia|program|data/)) {
    return HARMONIC_SIGNATURES.cyber
  }
  
  // Check for nature
  if (context.match(/forest|nature|animal|garden|tree|flower|wild|plant|earth/)) {
    return HARMONIC_SIGNATURES.nature
  }
  
  return HARMONIC_SIGNATURES.neutral
}

export default function HarmonicThemeProvider({ children, adventureSetup }) {
  const [currentSignature, setCurrentSignature] = useState(HARMONIC_SIGNATURES.neutral)
  const [isTransitioning, setIsTransitioning] = useState(false)

  useEffect(() => {
    const targetSignature = detectAdventureHarmonic(adventureSetup)
    
    if (targetSignature.name === currentSignature.name) {
      return // Already using this theme
    }

    // Gradual transition over ~40 seconds (2.5 breathing cycles)
    setIsTransitioning(true)
    
    const transitionDuration = 40000
    const startTime = Date.now()
    const startSig = currentSignature

    const transitionInterval = setInterval(() => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / transitionDuration, 1)
      
      if (progress >= 1) {
        clearInterval(transitionInterval)
        setCurrentSignature(targetSignature)
        setIsTransitioning(false)
      }
    }, 100)

    // Immediately start using the new signature
    setCurrentSignature(targetSignature)

    return () => clearInterval(transitionInterval)
  }, [adventureSetup])

  return (
    <HarmonicContext.Provider value={{ signature: currentSignature, isTransitioning }}>
      {children}
    </HarmonicContext.Provider>
  )
}

export function useHarmonic() {
  return useContext(HarmonicContext)
}
