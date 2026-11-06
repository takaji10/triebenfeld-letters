<script>
  import { db, personName } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'
  import MapView from '../lib/MapView.svelte'

  let { name = '' } = $props()

  const place = $derived(db.places ? db.places[name] : null)
  const coords = $derived(place?.c || null)
  const osm = $derived(coords
    ? `https://www.openstreetmap.org/?mlat=${coords[0]}&mlon=${coords[1]}#map=12/${coords[0]}/${coords[1]}`
    : null)
</script>

<p><a href="#/places">← {i18n.t('nav_places')}</a></p>
<h1>{name}</h1>

{#if place}
  <p class="stat">
    {place.n} {i18n.t('search_results')}
    {#if osm}
      · <a href={osm} target="_blank" rel="noopener">{coords[0].toFixed(4)}, {coords[1].toFixed(4)} — OpenStreetMap</a>
    {/if}
  </p>
  {#if coords}
    <MapView points={[{ name, coords, n: place.n }]} focus={coords}
             height="18rem" zoom={12} />
  {/if}
  {#if place.ev}
    <table>
      <tbody>
        {#each place.ev as ev}
          {@const [pid, tag, year, raw] = ev}
          <tr>
            <td class="year">{year ?? raw ?? ''}</td>
            <td>{tag}</td>
            <td>
              {#if pid.startsWith('F')}
                <span class="pill dim">{i18n.t('married')}</span>
                family {personName(pid.slice(1))}
              {:else}
                <a href={'#/person/' + pid}>{personName(pid)}</a>
                <span class="pid">{pid}</span>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
{/if}

<style>
  h1 { font-size: 1.2rem; }
  .stat { font-size: .8rem; color: var(--faint); }
  .year { color: var(--faint); white-space: nowrap; width: 7rem;
    font-variant-numeric: tabular-nums; }
  .pid { font-family: ui-monospace, Consolas, monospace; font-size: .72rem;
    color: var(--faint); margin-left: .35rem; white-space: nowrap; }
</style>
