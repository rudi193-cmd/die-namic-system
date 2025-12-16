import { motion } from 'framer-motion'
import { useHarmonic } from './HarmonicThemeProvider'

/**
 * TypingIndicator.jsx - Jane is thinking/typing
 * Animated, alive indicator that syncs with harmonic theme
 */

export default function TypingIndicator() {
  const { signature } = useHarmonic()
  
  // Use harmonic accent color or fallback
  const accentColor = signature?.accentColor || '#d4af37'

  return (
    <div className="flex items-center gap-3 animate-fade-in">
      {/* Jane's avatar pulsing */}
      <motion.div
        className="jane-avatar"
        animate={{
          scale: [1, 1.1, 1],
          rotate: [0, 5, -5, 0]
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <motion.div
          animate={{
            opacity: [0.6, 1, 0.6]
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          ✨
        </motion.div>
      </motion.div>

      {/* Typing bubble with animated dots */}
      <div className="jane-message relative overflow-hidden">
        {/* Shimmer effect across bubble */}
        <motion.div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: `linear-gradient(90deg, transparent, ${accentColor}40, transparent)`
          }}
          animate={{
            x: ['-100%', '200%']
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear"
          }}
        />

        {/* Typing dots */}
        <div className="flex gap-2 items-center relative z-10">
          <span className="text-sm opacity-70">Jane is crafting a response</span>
          <div className="flex gap-1">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: accentColor }}
                animate={{
                  scale: [0.8, 1.2, 0.8],
                  opacity: [0.4, 1, 0.4]
                }}
                transition={{
                  duration: 1.2,
                  repeat: Infinity,
                  delay: i * 0.2,
                  ease: "easeInOut"
                }}
              />
            ))}
          </div>
        </div>

        {/* Particle effects */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          {[...Array(5)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 rounded-full opacity-30"
              style={{
                backgroundColor: accentColor,
                left: `${20 + i * 15}%`,
                top: '50%'
              }}
              animate={{
                y: [-10, -30, -10],
                opacity: [0, 0.6, 0],
                scale: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.3,
                ease: "easeOut"
              }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
