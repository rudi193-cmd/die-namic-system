import { motion } from 'framer-motion'
import { useHarmonic } from './HarmonicThemeProvider'

/**
 * PaperLayer.jsx v1.52 - Harmonic Adaptive Breathing
 * Colors shift based on adventure type
 */

export default function PaperLayer({ children }) {
  const { signature, isTransitioning } = useHarmonic()
  
  const duration = 15
  const inhaleDuration = 7
  const inhaleFraction = inhaleDuration / duration

  // Use harmonic colors or fallback to neutral
  const baseColor = signature?.baseColor || '#0D1117'
  const glowColor = signature?.glowColor || 'rgba(212, 175, 55, 0.25)'

  return (
    <>
      {/* Breathing background layer with harmonic colors */}
      <motion.div
        className="fixed inset-0 -z-10"
        style={{
          background: `linear-gradient(135deg, ${baseColor} 0%, #161B22 50%, ${baseColor} 100%)`,
          transition: 'background 40s ease-in-out' // Smooth color transitions
        }}
        animate={{ 
          scale: [1, 1.03, 1],
          opacity: [0.88, 1, 0.88]
        }}
        transition={{ 
          duration: duration,
          times: [0, inhaleFraction, 1],
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        {/* Harmonic glow layer */}
        <motion.div
          className="absolute inset-0"
          style={{
            background: `radial-gradient(ellipse at center, ${glowColor} 0%, ${glowColor.replace('0.25', '0.12')} 40%, transparent 70%)`,
            transition: 'background 40s ease-in-out'
          }}
          animate={{
            opacity: [0, 1, 0]
          }}
          transition={{
            duration: duration,
            times: [0, inhaleFraction, 1],
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </motion.div>

      {children}

      {/* Debug indicator */}
      <div className="fixed bottom-4 right-4 bg-black/70 text-amber-400 text-xs p-2 rounded font-mono z-50 opacity-50 hover:opacity-100 transition-opacity">
        <div>✨ {signature?.name || 'Neutral'}</div>
        <div>{duration}s cycle</div>
        {isTransitioning && <div className="text-cyan-400">🎨 Shifting...</div>}
      </div>
    </>
  )
}
