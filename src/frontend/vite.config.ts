import react from '@vitejs/plugin-react';
import { resolve as resolvePath } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

const frontendDirectory = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@testing-library/react': resolvePath(
        frontendDirectory,
        'node_modules/@testing-library/react/dist/index.js',
      ),
    },
  },
  server: {
    host: '127.0.0.1',
    fs: {
      allow: ['../..'],
    },
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
  build: {
    outDir: '../backend/app/static',
    emptyOutDir: true,
  },
  test: {
    environment: 'jsdom',
    include: ['../../tests/frontend/**/*.{test,spec}.{ts,tsx}'],
  },
});
