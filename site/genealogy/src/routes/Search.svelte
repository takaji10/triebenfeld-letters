<script>
  import MiniSearch from 'minisearch'
  import { db, personName } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'

  let { q = '' } = $props()
  let input = $state(q)
  let results = $state(null)

  let mini = $state(null)
  $effect(() => {
    if (!db.index || mini) return
    const m = new MiniSearch({
      fields: ['gn', 'sn', 'n'],
      storeFields: ['id'],
      searchOptions: { prefix: true, fuzzy: 0.2, boost: { sn: 3, gn: 2 } },
    })
    m.addAll(Object.entries(db.index).map(([id, v]) => ({
      id, ...v, n: v.n, gn: v.gn || '', sn: v.sn || '',
    })))
    mini = m
    if (q) run(q)
  })

  function run(text) {
    if (!mini || !text.trim()) { results = null; return }
    results = mini.search(text.trim()).slice(0, 100)
  }

  $effect(() => { if (q && mini && input === q) run(q) })
</script>

<form onsubmit={(e) => { e.preventDefault(); run(input) }}>
  <input type="search" placeholder={i18n.t('search_placeholder')} bind:value={input}
         autofocus>
  <button class="primary">{i18n.t('nav_search')}</button>
</form>

{#if results}
  <p class="stat">{results.length} {i18n.t('search_results')}</p>
  {#if results.length === 0}
    <p class="lead">{i18n.t('no_results')}</p>
  {:else}
    <table>
      <tbody>
        {#each results as r}
          <tr>
            <td>
              <a href={'#/person/' + r.id}>{db.index[r.id]?.n || r.id}</a>
              {#if db.index[r.id]?.L}<span class="pill dim">{i18n.t('living')}</span>{/if}
            </td>
            <td class="years">
              {#if db.index[r.id]?.b || db.index[r.id]?.d}
                {db.index[r.id]?.b ?? '…'} – {db.index[r.id]?.d ?? '…'}
              {/if}
            </td>
            <td class="sn">{db.index[r.id]?.sn}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
{/if}

<style>
  form { display: flex; gap: .5rem; margin: .5rem 0 1rem; }
  form input { flex: 1; max-width: 30rem; }
  button.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
  .stat { font-size: .78rem; color: var(--faint); }
  .lead { color: var(--soft); }
  .years { color: var(--faint); font-size: .8rem; white-space: nowrap; }
  .sn { color: var(--faint); font-size: .8rem; }
  td { cursor: default; }
</style>
