<script>
  import { db, personName } from '../lib/db.svelte.js'
  import { i18n, EVENT_LABELS } from '../lib/i18n.js'
  import { fmtDate } from '../lib/dates.js'
  import MapView from '../lib/MapView.svelte'

  let { name = '' } = $props()

  let langTick = $state(0)
  i18n.subscribe(() => { langTick++ })
  const fmt = (raw) => { langTick; return fmtDate(raw, i18n.lang) }

  const place = $derived(db.places ? db.places[name] : null)
  const coords = $derived(place?.c || null)
  const osm = $derived(coords
    ? `https://www.openstreetmap.org/?mlat=${coords[0]}&mlon=${coords[1]}#map=12/${coords[0]}/${coords[1]}`
    : null)

  // one event row, spoken: the label written out, the full date, and for
  // a family event the couple named - "family F1326" says nothing
  function row(ev) {
    const [pid, tag, year, raw] = ev
    const label = i18n.t(EVENT_LABELS[tag] || 'in_tree')
    const date = raw ? fmt(raw) : (year ?? '')
    if (pid.startsWith('F')) {
      const fam = db.families?.[pid.slice(1)]
      const ids = [fam?.husb, fam?.wife].filter(Boolean)
      return { label, date,
               who: ids.map(x => db.index?.[x]?.n || x).join(' & '),
               ids }
    }
    return { label, date, who: null, ids: [pid] }
  }
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
    <!-- the breathing room after the map - the events list began
         flush against its bottom edge (the editor, 2026-11-07) -->
    <div class="mapspace">
      <MapView points={[{ name, coords, n: place.n }]} focus={coords}
               height="18rem" zoom={12} />
    </div>
  {/if}
  {#if place.ev}
    <h2 class="evh">{i18n.t('events')}</h2>
    <table>
      <tbody>
        {#each place.ev as ev}
          {@const r = row(ev)}
          <tr>
            <td class="year">{r.date}</td>
            <td class="what">{r.label}{#if r.who}&nbsp;· {r.who}{/if}</td>
            <td>
              {#each r.ids as x}
                <a href={'#/person/' + x}>{db.index?.[x]?.n || x}</a>
                <span class="pid">{x}</span>{#if r.ids.length > 1 && x !== r.ids[r.ids.length - 1]}&nbsp;·{/if}
              {/each}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
{/if}

<style>
  h1 { font-size: 1.2rem; }
  .mapspace { margin: 1.1rem 0 1.6rem; }
  .evh { font-size: 1rem; font-weight: 600; margin: 0 0 .5rem;
    color: var(--ink); }
  .stat { font-size: .8rem; color: var(--faint); }
  .year { color: var(--faint); white-space: nowrap; width: 14rem;
    font-variant-numeric: tabular-nums; }
  .what { color: var(--soft); white-space: nowrap; }
  .pid { font-family: ui-monospace, Consolas, monospace; font-size: .72rem;
    color: var(--faint); margin-left: .35rem; white-space: nowrap; }
</style>
