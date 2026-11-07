<script>
  import { db } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'
  import MapView from '../lib/MapView.svelte'

  let filter = $state('')
  let letter = $state('')

  const shown = $derived.by(() => {
    if (!db.places) return []
    const f = (letter || filter.trim()).toLowerCase()
    const entries = Object.entries(db.places)
    const hit = f ? entries.filter(([n]) => n.toLowerCase().startsWith(f)
      || (letter === '' && n.toLowerCase().includes(f))) : entries
    return hit.sort((a, b) => a[0].localeCompare(b[0]))
  })

  // the list in letter groups - a subheader row opens each letter
  // (the editor: separate the long list into letters, 2026-11-07)
  const groups = $derived.by(() => {
    const map = new Map()
    for (const row of shown) {
      const c = row[0].trim().charAt(0).toUpperCase()
      if (!map.has(c)) map.set(c, [])
      map.get(c).push(row)
    }
    return [...map.entries()]
  })

  const geoCount = $derived(shown.filter(([, v]) => v.c).length)
  const mapPoints = $derived(shown.filter(([, v]) => v.c)
    .map(([name, v]) => ({ name, coords: v.c, n: v.n })))

  // the letters actually present, for the A/B/C navigation
  const letters = $derived.by(() => {
    if (!db.places) return []
    const set = new Set()
    for (const [name] of Object.entries(db.places)) {
      const c = name.trim().charAt(0).toUpperCase()
      if (c) set.add(c)
    }
    return [...set].sort()
  })

  function setLetter(c) {
    letter = (letter === c) ? '' : c
    filter = ''
  }

  // returning from a place page lands where the reader left: the
  // position is saved when a place is opened and restored once the
  // list has rendered (a fresh visit from the nav starts at the top -
  // the saved position is consumed once)
  let pendingScroll = $state(null)
  function rememberScroll() {
    try { sessionStorage.setItem('places.scroll', String(window.scrollY)) }
    catch { /* private modes refuse storage; the back trip just lands high */ }
  }
  $effect(() => {
    if (pendingScroll == null && db.places) {
      try { pendingScroll = sessionStorage.getItem('places.scroll') } catch {}
    }
    if (pendingScroll != null && db.places) {
      const y = Number(pendingScroll)
      pendingScroll = null
      try { sessionStorage.removeItem('places.scroll') } catch {}
      requestAnimationFrame(() => window.scrollTo(0, y))
    }
  })
</script>

<h1>{i18n.t('nav_places')}</h1>

{#if db.places}
  <MapView points={mapPoints} height="34rem" zoom={6} wide />
{/if}

<p>
  <input type="search" placeholder="filter …" bind:value={filter}>
  <span class="stat">{shown.length} · {geoCount} {i18n.t('geocoded_count')}</span>
  <span class="legend"><span class="dot"></span> = {i18n.t('geo_legend')}</span>
</p>

<div class="letters">
  <button class:active={letter === ''} onclick={() => { letter = ''; filter = '' }}>All</button>
  {#each letters as c}
    <button class:active={letter === c} onclick={() => setLetter(c)}>{c}</button>
  {/each}
</div>

{#if db.places}
  <table>
    <thead><tr><th colspan="2">{i18n.t('nav_places')}</th><th class="n">{i18n.t('events_at')}</th></tr></thead>
    {#each groups as [c, rows] (c)}
      <tbody>
        <tr class="ltrrow"><td colspan="3">{c}</td></tr>
        {#each rows as [name, v] (name)}
          <tr>
            <!-- the geolocated mark: a plain round dot in its own
                 column, legend at the top of the page (the editor
                 brought it back, 2026-11-07: small and self-explained
                 rather than a pill) -->
            <td class="geo">{#if v.c}<span class="dot"></span>{/if}</td>
            <td><a href={'#/place/' + encodeURIComponent(name)}
                   onclick={rememberScroll}>{name}</a></td>
            <td class="n">{v.n}</td>
          </tr>
        {/each}
      </tbody>
    {/each}
  </table>
{/if}

<style>
  h1 { font-size: 1.2rem; }
  .stat { font-size: .78rem; color: var(--faint); margin-left: .6rem; }
  .letters { display: flex; flex-wrap: wrap; gap: .2rem; margin: 0 0 .6rem; }
  .letters button { font: inherit; font-size: .74rem; min-width: 1.7rem;
    padding: .15rem .3rem; border: 1px solid var(--rule); border-radius: 3px;
    background: var(--card); color: var(--soft); cursor: pointer; }
  .letters button.active { background: var(--accent); border-color: var(--accent);
    color: #fff; }
  .n { text-align: right; font-variant-numeric: tabular-nums; width: 6rem; }
  /* the geolocated mark: a plain round dot in the palette's green,
     small and quiet - the legend at the top of the page says what it
     means, so no pill, no border, no guessing */
  .geo { width: 1.4rem; text-align: center; }
  .dot { display: inline-block; width: .55rem; height: .55rem;
    border-radius: 50%; background: var(--ok); vertical-align: middle; }
  .legend { font-size: .78rem; color: var(--faint); margin-left: .8rem; }
  .legend .dot { margin-right: .15rem; }
  /* the letter subheader inside the list - quiet, spaced from the
     letter above */
  tr.ltrrow td { padding: .9rem .4rem .25rem; font-size: .8rem;
    color: var(--accent); font-weight: 600; letter-spacing: .06em;
    border-bottom: 1px solid var(--rule); }
  table { border-collapse: collapse; width: 100%; }
  td { padding: .28rem .4rem; border-bottom: 1px solid var(--rule); }
</style>
