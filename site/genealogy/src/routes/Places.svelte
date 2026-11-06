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
</script>

<h1>{i18n.t('nav_places')}</h1>

{#if db.places}
  <MapView points={mapPoints} height="22rem" zoom={6} />
{/if}

<p>
  <input type="search" placeholder="filter …" bind:value={filter}>
  <span class="stat">{shown.length} · {geoCount} {i18n.t('geocoded_count')}</span>
</p>

<div class="letters">
  <button class:active={letter === ''} onclick={() => { letter = ''; filter = '' }}>All</button>
  {#each letters as c}
    <button class:active={letter === c} onclick={() => setLetter(c)}>{c}</button>
  {/each}
</div>

{#if db.places}
  <table>
    <thead><tr><th>{i18n.t('nav_places')}</th><th class="n">{i18n.t('events_at')}</th><th></th></tr></thead>
    <tbody>
      {#each shown as [name, v]}
        <tr>
          <td><a href={'#/place/' + encodeURIComponent(name)}>{name}</a></td>
          <td class="n">{v.n}</td>
          <td class="geo">{#if v.c}<span class="pill ok">◦</span>{/if}</td>
        </tr>
      {/each}
    </tbody>
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
  .geo { width: 3rem; }
</style>
