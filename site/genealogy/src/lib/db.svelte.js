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

// Per-tree settings from meta.json (the Zelmer meta may lack them: the
// fallbacks are the Zelmer values). tree: 'zelmer' | 'trabczyn'.
export const treeId = () => db.meta?.tree || 'zelmer'
export const treeTitle = (lang) =>
  (db.meta?.title && (db.meta.title[lang] || db.meta.title.en)) || null
export const startPerson = () => db.meta?.start || 'I2867'
export const hasMedia = () => db.meta?.media !== false

// The folder of the tree's own page, and the site root two levels above
// it (/<prefix>/genealogy/<tree>/ -> /<prefix>/): computed from the
// document URL so one build serves under any prefix.
export const siteRoot = () => {
  const dir = document.URL.replace(/#.*$/, '').replace(/[^/]*$/, '')
  return new URL('../../', dir).href
}

// A url from the data: absolute (https) as is, site-relative ('/people/x/')
// resolved against the site root, never the domain root.
export function resolveUrl(u) {
  if (!u) return null
  if (/^[a-z][a-z0-9+.-]*:/i.test(u)) return u
  if (u.startsWith('/')) return new URL(u.replace(/^\/+/, ''), siteRoot()).href
  return new URL(u, siteRoot()).href
}
export const isExternal = (u) => !!u && /^[a-z][a-z0-9+.-]*:/i.test(u) &&
  !u.startsWith(location.origin + '/')

export function goto(path) {
  location.hash = '#/' + path.replace(/^\/+/, '')
}

export function personName(id) {
  if (id && id.startsWith && id.startsWith('F')) id = id.slice(1)
  const row = db.index && db.index[id]
  return row ? row.n : id
}
