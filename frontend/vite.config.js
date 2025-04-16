import path from 'node:path'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: process.env.NODE_ENV === 'production' ? '/dist/' : '/',
  resolve: {
    alias: {
      '@': path.resolve(process.cwd(), '.'),
    },
  },
  server: {
    proxy: {
      // Proxy API requests to the backend during development
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
      '/healthcheck': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
