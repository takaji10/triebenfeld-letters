<script>
  import { db } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'
  import MapView from '../lib/MapView.svelte'

  let filter = $state('')

  const points = $derived.by(() => {
    if (!db.places) return []
    const f = filter.trim().toLowerCase()
    const out = []
    for (const [name, v] of Object.entries(db.places)) {
      if (!v.c) continue
      if (f && !name.toLowerCase().includes(f)) continue
      out.push({ name, coords: v.c, n: v.n })
    }
    return out
  })
</script>

<h1>{i18n.t('nav_map')}</h1>
<p>
  <input type="search" placeholder="filter …" bind:value={filter}>
  <span class="stat">{points.length} / {db.meta ? db.meta.counts.geocoded_places : '…'}
    {i18n.t('places_count')}</span>
</p>
<MapView points={points} height="70vh" />

<style>
  h1 { font-size: 1.2rem; }
  .stat { font-size: .78rem; color: var(--faint); margin-left: .6rem; }
</style>
