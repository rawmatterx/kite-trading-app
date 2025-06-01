import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    // Explicitly define the `process.env` type
    define: {
      'process.env': env,
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'production'),
    },
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: true, // Enable source maps for debugging
    },
    server: {
      port: 3000,
      open: true,
    },
  };
});
