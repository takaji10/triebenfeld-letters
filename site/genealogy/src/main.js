import { mount } from 'svelte'
import App from './App.svelte'
import './app.css'

// The shell's static watch (index.html, rebuilt from shell.html) shows
// troubleshooting guidance when the module never arrives; it stands down
// the moment this file runs (window.__zfBooted).
window.__zfBooted = true

// Svelte 5's mount() appends to the target - it does not replace what is
// already inside it - so the static boot placeholder inside #app would
// otherwise survive the mount and sit above the application (seen on the
// live site, 2026-11-06). Cleared by hand here, after the watch has stood
// down and before the component renders.
const target = document.getElementById('app')
target.textContent = ''

try {
  mount(App, { target })
} catch (err) {
  // A crash while the component initialises leaves no other word on the
  // page - the static watch has stood down and the placeholder is gone.
  target.innerHTML =
    '<div id="boot"><div class="fallback"><h2>The family explorer failed to start.</h2>' +
    '<p>Please reload the page (Ctrl+F5). If it keeps failing, write to the archive.</p>' +
    '<div class="de"><h2>Deutsch</h2><p>Der Familien-Explorer konnte nicht starten. ' +
    'Bitte laden Sie die Seite neu (Strg+F5).</p></div>' +
    '<p><a href="../">&larr; Back to the archive home page / Zur&uuml;ck zur Startseite</a></p></div></div>'
  throw err
}
