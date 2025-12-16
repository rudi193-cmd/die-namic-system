import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// ESC-1 Compliant Vite Configuration
// Local-only development server - no external connections
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    host: 'localhost',
    open: false,
    cors: false,
    proxy: {
      '/api': {
        target: 'http://localhost:5550',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      external: []
    }
  }
})
