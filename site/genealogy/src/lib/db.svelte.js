// The shared database store, loaded once per session (Svelte 5 runes).
import * as api from './data.js'

export const db = $state({
  ready: false,
  progress: { done: 0, total: 8 },  // files of the opening fetch finished
  index: null,        // id -> {n, sn, gn, sx, b, d, L, M}
  families: null,     // id -> {husb, wife, chil, marr?}
  sources: null,      // id -> {title, author, pub, repo, callno}
  repos: null,        // id -> {name, note}
  places: null,       // place string -> {n, c, ev}
  mediaFiles: null,   // path -> {file, thumb, w, h} + __base__
  mediaInfo: null,    // path -> {oid, form, title, regions}
  meta: null,         // {built, media_base, counts}
})

let started = false

export function initDB() {
  if (started) return
  started = true
  const tick = p => p.then(v => { db.progress.done++; return v })
  // Optional files resolve to {} when absent, so the count stays honest.
  Promise.all([
    tick(api.index()), tick(api.families()), tick(api.sources()),
    tick(api.repos()), tick(api.places()), tick(api.mediaFiles()),
    tick(api.getJSON('data/media.json').catch(() => ({}))),
    tick(api.meta()),
  ]).then(([index, families, sources, repos, places, mediaFiles,
            mediaInfo, meta]) => {
    mediaFiles.__base__ = meta.media_base || ''
    Object.assign(db, { ready: true, index, families, sources, repos,
                        places, mediaFiles, mediaInfo, meta })
  }).catch(err => {
    db.error = String(err)
    db.ready = true
  })
}

export function goto(path) {
  location.hash = '#/' + path.replace(/^\/+/, '')
}

export function personName(id) {
  if (id && id.startsWith && id.startsWith('F')) id = id.slice(1)
  const row = db.index && db.index[id]
  return row ? row.n : id
}
