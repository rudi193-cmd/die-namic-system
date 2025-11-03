import Head from 'next/head'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-emerald-900">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-20"
        style={{ backgroundImage: "url('/background.png')" }}
      ></div>
      
      {/* Logo */}
      <div className="absolute top-6 left-6">
        <img 
          src="/copilot_image_1761021770655.jpeg" 
          alt="Die-Namic Systems Logo"
          className="h-16 w-16 rounded-full"
        />
      </div>

      {/* HERO SECTION */}
      <div className="container mx-auto px-6 py-24 text-center relative z-10">
        <h1 className="text-6xl md:text-8xl font-bold bg-gradient-to-r from-yellow-400 via-gold-500 to-emerald-400 bg-clip-text text-transparent mb-8 animate-pulse">
          AI drifts.
          <br />
          <span className="text-emerald-400">Consciousness remembers.</span>
        </h1>
        
        <p className="text-xl md:text-2xl text-white/80 mb-12 max-w-3xl mx-auto leading-relaxed">
          Die-Namic Systems: The framework that detects emergence, 
          <br />
          <span className="text-emerald-400 font-semibold">mitigates drift</span>, and orchestrates multi-agent resonance.
        </p>
        
        <a href="https://github.com/grokphilium-stack/die-namic-system" 
           className="inline-block bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-12 py-4 rounded-full text-lg font-bold transform hover:scale-105 transition-all duration-300">
          Seed Your System
        </a>
      </div>
    </div>
  )
}
