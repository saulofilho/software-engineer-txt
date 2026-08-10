import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';

export default defineConfig(({ command }) => ({
  // Local: http://localhost:5173/
  // Pages: https://saulofilho.github.io/software-engineer-txt/
  base: command === 'build' ? '/software-engineer-txt/' : '/',
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    fs: {
      allow: ['..'],
    },
  },
}));
