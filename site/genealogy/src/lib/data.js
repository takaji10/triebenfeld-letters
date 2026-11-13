// Data access. Everything loads from the tree's own data/ folder next to its page
// (site/genealogy/zelmer/data, site/genealogy/trabczyn/data; committed by
// the Python builds); media URLs join meta.media_base with the media repo's
// manifest copy. Hash-routed, so relative fetches always resolve here.

const CACHE = new Map()

function dirURL() {
  return document.URL.replace(/#.*$/, '').replace(/[^/]*$/, '')
}

export async function getJSON(path) {
  if (!CACHE.has(path)) {
    CACHE.set(path, fetch(new URL(path, dirURL())).then(r => {
      if (!r.ok) throw new Error(`${path}: ${r.status}`)
      return r.json()
    }))
  }
  return CACHE.get(path)
}

export const index = () => getJSON('data/index.json')
export const surnames = () => getJSON('data/surnames.json')
export const places = () => getJSON('data/places.json')
export const families = () => getJSON('data/families.json')
export const sources = () => getJSON('data/sources.json')
export const repos = () => getJSON('data/repos.json')
export const mediaFiles = () => getJSON('data/media_files.json').catch(() => ({}))
export const meta = () => getJSON('data/meta.json')
export const person = id => getJSON(`data/people/${id}.json`)

// Media URL for a path, joined with the manifest's hash-named file.
export function mediaURL(files, path, thumb = false) {
  const entry = files[path]
  if (!entry) return null
  const f = thumb ? (entry.thumb || entry.file) : entry.file
  return (files.__base__ || '') + f
}
