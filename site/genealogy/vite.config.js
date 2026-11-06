import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// Built into this directory and committed: the CI builds Jekyll only, so
// the compiled app travels with the tree (pipeline/genealogy/README.md).
// outDir is the project root with emptyOutDir off: vite writes index.html
// (the transformed shell), assets/app.js and assets/index.css, nothing
// else, and never deletes a thing. The base is absolute because the site
// lives permanently at /genealogy/ and verify_site.py resolves links from
// the site root.
export default defineConfig({
  base: '/genealogy/',
  plugins: [svelte()],
  build: {
    outDir: '.',
    emptyOutDir: false,
    rollupOptions: {
      output: {
        entryFileNames: 'assets/app.js',
        assetFileNames: 'assets/[name].[ext]',
      }
    }
  }
})
