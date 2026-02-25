import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react-swc'

const nodeModules = new URL('node_modules', import.meta.url).pathname

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      {
        // Redirect any bare import (not relative, not absolute, not node built-in)
        // to frontend/node_modules so test files outside frontend/ can find packages
        find: /^(?!node:)([^./].+)$/,
        replacement: `${nodeModules}/$1`,
      },
    ],
  },
  server: {
    fs: {
      allow: ['..'],
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setup_tests.ts',
    include: ['../test/frontend/**/*.{test,spec}.{js,ts,jsx,tsx}'],
  },
})
