import { mount } from 'svelte'
import App from './App.svelte'
import './app.css'

// The shell's static watch (index.html, rebuilt from shell.html) shows
// troubleshooting guidance when the module never arrives; it stands down
// the moment this file runs.
window.__zfBooted = true

mount(App, { target: document.getElementById('app') })
