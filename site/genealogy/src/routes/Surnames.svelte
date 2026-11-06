<script>
  import { db } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'

  let { selected = null } = $props()
  let filter = $state('')

  const all = $derived.by(() => {
    if (!db.index) return []
    const c = {}
    for (const v of Object.values(db.index)) {
      const sn = (v.sn || '').trim()
      if (sn) c[sn] = (c[sn] || 0) + 1
    }
    return Object.entries(c).sort((a, b) => b[1] - a[1])
  })

  const shown = $derived(
    filter ? all.filter(([n]) => n.toLowerCase().includes(filter.toLowerCase())) : all)

  const people = $derived.by(() => {
    if (!selected || !db.index) return []
    return Object.entries(db.index)
      .filter(([, v]) => v.sn === selected)
      .sort((a, b) => (a[1].gn || '').localeCompare(b[1].gn || ''))
  })
</script>

{#if selected}
  <p><a href="#/surnames">← {i18n.t('nav_surnames')}</a></p>
  <h1>{selected} <span class="pill acc">{people.length}</span></h1>
  <table>
    <tbody>
      {#each people as [id, v]}
        <tr>
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
