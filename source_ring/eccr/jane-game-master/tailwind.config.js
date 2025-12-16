/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Neutral, adaptable palette
        'jane-amber': '#FFA726',
        'jane-deep-blue': '#1E3A5F',
        'jane-steel': '#546E7A',
        'jane-forest': '#2E7D32',
        'jane-crimson': '#C62828',
        'jane-void': '#0D1117',
        'jane-slate': '#263238',
        'jane-parchment': '#E8DCC4',
        'jane-gold': '#D4AF37',
        'jane-electric': '#00BCD4',
      },
      fontFamily: {
        'story': ['Courier New', 'Consolas', 'monospace'],
        'adventure': ['Impact', 'Arial Black', 'sans-serif'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { 
            opacity: '1',
          },
          '50%': { 
            opacity: '0.6',
          },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
}
