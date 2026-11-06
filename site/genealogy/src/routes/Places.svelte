<script>
  import { db } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'

  let filter = $state('')

  const shown = $derived.by(() => {
    if (!db.places) return []
    const f = filter.trim().toLowerCase()
    const entries = Object.entries(db.places)
    const hit = f ? entries.filter(([n]) => n.toLowerCase().includes(f)) : entries
    return hit.sort((a, b) => a[0].localeCompare(b[0]))
  })

  const geoCount = $derived(shown.filter(([, v]) => v.c).length)
</script>

<h1>{i18n.t('nav_places')}</h1>
<p>
  <input type="search" placeholder="filter …" bind:value={filter}>
  <span class="stat">{shown.length} · {geoCount} {i18n.t('geocoded_count')}</span>
</p>

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
  .n { text-align: right; font-variant-numeric: tabular-nums; width: 6rem; }
  .geo { width: 3rem; }
</style>
