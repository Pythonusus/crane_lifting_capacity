import path from 'node:path'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Serve the dist folder in production, because it is mounted in backend.
  // During development, we serve the frontend from the root folder.
  // This is needed for hot reloading to work
  base: process.env.NODE_ENV === 'production' ? '/dist/' : '/',
  resolve: {
    alias: {
      '@': path.resolve(process.cwd(), '.'),
    },
  },
  // Development server configuration
  server: {
    proxy: {
      // Proxy API requests to backend in dev mode
      '/process': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/cranes': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/chassis-types': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/manufacturers': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/healthcheck': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
