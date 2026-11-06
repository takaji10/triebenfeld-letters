<script>
  import { db } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'

  let { selected = null } = $props()
  let filter = $state('')
  // the surname index: by count (the default), or A–Z / Z–A
  let sort = $state('count')
  // the people of one surname: A–Z / Z–A by name
  let psort = $state('az')

  const all = $derived.by(() => {
    if (!db.index) return []
    const c = {}
    for (const v of Object.values(db.index)) {
      const sn = (v.sn || '').trim()
      if (sn) c[sn] = (c[sn] || 0) + 1
    }
    const rows = Object.entries(c)
    if (sort === 'az') rows.sort((a, b) => a[0].localeCompare(b[0]))
    else if (sort === 'za') rows.sort((a, b) => b[0].localeCompare(a[0]))
    else rows.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    return rows
  })

  const shown = $derived(
    filter ? all.filter(([n]) => n.toLowerCase().includes(filter.toLowerCase())) : all)

  const people = $derived.by(() => {
    if (!selected || !db.index) return []
    const rows = Object.entries(db.index)
      .filter(([, v]) => v.sn === selected)
      .sort((a, b) => (a[1].n || '').localeCompare(b[1].n || ''))
    return psort === 'za' ? rows.reverse() : rows
  })

  function setSort(s) { sort = s }
  function setPsort(s) { psort = s }
</script>

{#if selected}
  <p><a href="#/surnames">← {i18n.t('nav_surnames')}</a></p>
  <h1>{selected} <span class="pill acc">{people.length}</span></h1>
  <div class="sortbar">
    <button class:active={psort === 'az'} onclick={() => setPsort('az')}>{i18n.t('sort_az')}</button>
    <button class:active={psort === 'za'} onclick={() => setPsort('za')}>{i18n.t('sort_za')}</button>
  </div>
  <table>
    <tbody>
      {#each people as [id, v]}
        <tr>
          <td class="pid">{id}</td>
          <td><a href={'#/person/' + id}>{v.n}</a></td>
          <td class="years">{v.b ?? ''} {v.d ? '– ' + v.d : ''}</td>
          <td class="sex">{v.sx === 'F' ? '♀' : v.sx === 'M' ? '♂' : ''}</td>
          {#if v.M}<td class="media">▪</td>{:else}<td></td>{/if}
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <h1>{i18n.t('nav_surnames')}</h1>
  <p><input type="search" placeholder="filter …" bind:value={filter}></p>
  <div class="sortbar">
    <button class:active={sort === 'count'} onclick={() => setSort('count')}>{i18n.t('sort_count')}</button>
    <button class:active={sort === 'az'} onclick={() => setSort('az')}>{i18n.t('sort_az')}</button>
    <button class:active={sort === 'za'} onclick={() => setSort('za')}>{i18n.t('sort_za')}</button>
  </div>
  <div class="grid">
    {#each shown as [name, n]}
      <a class="row" href={'#/surname/' + encodeURIComponent(name)}>
        <span>{name}</span><b>{n}</b>
      </a>
    {/each}
  </div>
{/if}

<style>
  h1 { font-size: 1.2rem; display: flex; gap: .6rem; align-items: center; }
  .sortbar { display: flex; gap: .3rem; margin: 0 0 .6rem; }
  .sortbar button { font: inherit; font-size: .74rem; padding: .15rem .55rem;
    border: 1px solid var(--rule); border-radius: 3px; background: var(--card);
    color: var(--soft); cursor: pointer; }
  .sortbar button.active { background: var(--accent); border-color: var(--accent);
    color: #fff; }
  .pid { font-family: ui-monospace, Consolas, monospace; font-size: .72rem;
    color: var(--faint); white-space: nowrap; }
  .years { color: var(--faint); font-size: .8rem; white-space: nowrap; }
  .sex { color: var(--faint); width: 2rem; }
  .media { color: var(--accent); width: 2rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
    gap: .3rem; }
  .row { display: flex; justify-content: space-between; gap: .5rem;
    border-bottom: 1px solid var(--rule); padding: .3rem .4rem; color: var(--ink); }
  .row b { color: var(--faint); font-weight: 600; }
  .row:hover { background: #f6f1e8; text-decoration: none; }
</style>
