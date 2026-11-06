import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// Built into this directory and committed: the CI builds Jekyll only, so
// the compiled app travels with the tree (pipeline/genealogy/README.md).
// outDir is the project root with emptyOutDir off: vite writes index.html
// (the transformed shell), assets/app.js and assets/index.css, nothing
// else, and never deletes a thing. The base is relative (./assets/...)
// because the site is published under different prefixes - a user site at
// /genealogy/ and a project site at /<repo>/genealogy/ - and an absolute
// base breaks everything but one of them: the browser then asks for the
// script at a path that does not exist, the server answers with its HTML
// 404 page, and the module load dies on the disallowed text/html MIME type
// while the boot screen spins forever. Relative to the document it works
// everywhere; the data fetches were already resolved against the document
// URL for the same reason.
export default defineConfig({
  base: './',
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
