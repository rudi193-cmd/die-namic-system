/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Aionic color palette
        'aionic-gold': '#FFD580',
        'aionic-amber': '#FFB347',
        'aionic-coral': '#E8756F',
        'aionic-rose': '#D6A4A4',
        'aionic-blue': '#A8B8C8',
        'aionic-dark': '#2A2A2A',
      },
      animation: {
        'gentle-breathe': 'gentle-breathe 4s ease-in-out infinite',
        'aurora-flow': 'aurora-flow 8s ease-in-out infinite',
      },
      keyframes: {
        'gentle-breathe': {
          '0%, 100%': { transform: 'scale(1)', opacity: '1' },
          '50%': { transform: 'scale(1.02)', opacity: '0.95' },
        },
        'aurora-flow': {
          '0%, 100%': { 
            backgroundPosition: '0% 50%',
          },
          '50%': { 
            backgroundPosition: '100% 50%',
          },
        },
      },
    },
  },
  plugins: [],
}
