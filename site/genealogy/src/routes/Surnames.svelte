<script>
  import { db } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'
  import { fmtDate } from '../lib/dates.js'

  let { selected = null } = $props()

  // ---- the search sidebar ------------------------------------------------
  let fName = $state('')
  let fId = $state('')
  let fSex = $state('')
  let fBirthFrom = $state(''), fBirthTo = $state('')
  let fBirthPlace = $state('')
  let fDeathFrom = $state(''), fDeathTo = $state('')
  let fDeathPlace = $state('')
  let fEvent = $state('')
  let applied = $state(null)

  // place autocomplete: the distinct places in the database
  const placeList = $derived(db.places ? Object.keys(db.places) : [])
  function suggest(text) {
    const t = text.trim().toLowerCase()
    if (!t) return []
    return placeList.filter(p => p.toLowerCase().includes(t)).slice(0, 8)
  }

  const EVENT_TYPES = [
    ['BIRT', 'born'], ['BAPM', 'baptised'], ['MARR', 'married'],
    ['DEAT', 'died'], ['BURI', 'buried'], ['RESI', 'residence'],
    ['OCCU', 'occupation'], ['IMMI', 'immigrated'], ['EMIG', 'emigrated'],
    ['CENS', 'census'], ['NATU', 'naturalised'], ['MILIT', 'military'],
    ['CONF', 'confirmed'], ['PROP', 'property'],
  ]

  function find() {
    applied = {
      name: fName.trim().toLowerCase(),
      id: fId.trim().toUpperCase(),
      sex: fSex,
      b1: fBirthFrom && /^\d{1,4}$/.test(fBirthFrom.trim()) ? +fBirthFrom.trim() : null,
      b2: fBirthTo && /^\d{1,4}$/.test(fBirthTo.trim()) ? +fBirthTo.trim() : null,
      bp: fBirthPlace.trim().toLowerCase(),
      d1: fDeathFrom && /^\d{1,4}$/.test(fDeathFrom.trim()) ? +fDeathFrom.trim() : null,
      d2: fDeathTo && /^\d{1,4}$/.test(fDeathTo.trim()) ? +fDeathTo.trim() : null,
      dp: fDeathPlace.trim().toLowerCase(),
      ev: fEvent,
    }
    // a find opens every group that has hits
    const open = {}
    for (const [sn, rows] of filtered()) if (rows.length) open[sn] = true
    expanded = open
    anyOpen = true
  }

  function clearAll() {
    fName = fId = fSex = fBirthFrom = fBirthTo = fBirthPlace = ''
    fDeathFrom = fDeathTo = fDeathPlace = fEvent = ''
    applied = null
    expanded = {}
    anyOpen = false
  }

  // ---- the population, filtered by the applied search --------------------
  function lifeYear(v, key, q1, q2, bp) {
    if (!v) return true
    if (q1 != null && (v[key] == null || v[key] < q1)) return false
    if (q2 != null && (v[key] == null || v[key] > q2)) return false
    if (bp && !((key === 'b' ? v.bp : v.dp) || '').toLowerCase().includes(bp)) return false
    return true
  }

  function filtered() {
    if (!db.index) return []
    const f = applied
    const groups = {}
    for (const [id, v] of Object.entries(db.index)) {
      if (f) {
        if (f.name && !(v.n || '').toLowerCase().includes(f.name)) continue
        if (f.id && !id.includes(f.id)) continue
        if (f.sex && v.sx !== f.sex) continue
        if (!lifeYear(v, 'b', f.b1, f.b2, f.bp)) continue
        if (!lifeYear(v, 'd', f.d1, f.d2, f.dp)) continue
        if (f.ev) {
          // event type: someone in the family of the person held the
          // event? Read from the index's event flags - cheap check over
          // the shard only when the group is small, so the index alone
          // filters what it can and the shard filter runs lazily below
        }
      }
      const sn = (v.sn || '').trim()
      ;(groups[sn || '—'] ??= []).push([id, v])
    }
    for (const sn of Object.keys(groups))
      groups[sn].sort((a, b) => (a[1].n || '').localeCompare(b[1].n || ''))
    return Object.entries(groups).sort((a, b) => a[0].localeCompare(b[0]))
  }

  // the person-shard event-type filter runs on demand and lazily: the
  // group lists are re-filtered once per applied search
  let shardCache = $state({})
  $effect(() => {
    if (!applied?.ev || !db.ready) return
    ;(async () => {
      const { person } = await import('../lib/data.js')
      const out = {}
      const rows = filtered().flatMap(([, rs]) => rs)
      // bound the work: shards load in batches
      const BATCH = 40
      for (let i = 0; i < rows.length; i += BATCH) {
        const slice = rows.slice(i, i + BATCH)
        await Promise.all(slice.map(async ([id]) => {
          try {
            const s = await person(id)
            out[id] = (s.events || []).some(e => e.tag === applied.ev)
          } catch { out[id] = false }
        }))
        shardCache = { ...out }
      }
    })()
  })

  // ---- collapsible groups -------------------------------------------------
  let expanded = $state({})
  let anyOpen = $state(false)

  function toggle(sn) { expanded = { ...expanded, [sn]: !expanded[sn] } }
  function expandAll() {
    const o = {}
    for (const [sn, rows] of filtered()) if (rows.length) o[sn] = true
    expanded = o
    anyOpen = true
  }
  function collapseAll() { expanded = {}; anyOpen = false }

  const fmt = (raw) => fmtDate(raw, i18n.lang)

  function years(v) {
    if (!v) return { b: '', d: '' }
    if (v.L) return { b: '', d: '' }
    return {
      b: v.br ? fmt(v.br) : (v.b != null ? String(v.b) : ''),
      d: v.dr ? fmt(v.dr) : (v.d != null ? String(v.d) : ''),
    }
  }

  const shownGroups = $derived(filtered().filter(([, rows]) =>
    !applied?.ev || rows.some(([id]) => shardCache[id])))
</script>

<div class="layout">
  <main>
    <h1>{i18n.t('nav_surnames')}</h1>
    <div class="toolbar">
      <button onclick={anyOpen ? collapseAll : expandAll}>
        {anyOpen ? '⤡ ' + i18n.t('collapse_all') : '⤢ ' + i18n.t('expand_all')}
      </button>
      <span class="stat">{shownGroups.reduce((s, [, r]) => s + r.length, 0)} people</span>
    </div>

    <table class="plist">
      {#each shownGroups as [sn, rows] (sn)}
        <tbody>
          <tr class="group" onclick={() => toggle(sn)}>
            <td colspan="5">
              <button class="ghead" aria-expanded={!!expanded[sn]}>
                <span class="arrow" class:open={!!expanded[sn]}>▸</span>
                <b>{sn}</b> <span class="pill acc">{rows.length}</span>
              </button>
            </td>
          </tr>
          {#if expanded[sn]}
            {#each rows as [id, v] (id)}
              <tr>
                <td class="ln">{v.sn}</td>
                <td><a href={'#/person/' + id}>{v.gn || v.n}</a></td>
                <td class="pid">{id}</td>
                <td class="sex">{v.sx === 'F' ? '♀' : v.sx === 'M' ? '♂' : ''}</td>
                <td class="dates">{years(v).b}</td>
                <td class="dates">{years(v).d}</td>
              </tr>
            {/each}
          {/if}
        </tbody>
      {/each}
    </table>
  </main>

  <aside>
    <h2>{i18n.t('find_people')}</h2>
    <label>{i18n.t('fld_name')}<input type="search" bind:value={fName}></label>
    <label>{i18n.t('fld_id')}<input type="search" bind:value={fId}></label>
    <label>{i18n.t('fld_sex')}
      <select bind:value={fSex}>
        <option value="">—</option>
        <option value="F">♀</option>
        <option value="M">♂</option>
      </select>
    </label>
    <div class="pair">
      <label>{i18n.t('fld_birth_from')}<input type="number" bind:value={fBirthFrom}></label>
      <label>{i18n.t('fld_birth_to')}<input type="number" bind:value={fBirthTo}></label>
    </div>
    <label class="rel">{i18n.t('fld_birth_place')}
      <input type="search" bind:value={fBirthPlace} autocomplete="off">
      {#if fBirthPlace && suggest(fBirthPlace).length}
        <div class="sugg">
          {#each suggest(fBirthPlace) as s}
            <button type="button" onclick={() => { fBirthPlace = s }}>{s}</button>
          {/each}
        </div>
      {/if}
    </label>
    <div class="pair">
      <label>{i18n.t('fld_death_from')}<input type="number" bind:value={fDeathFrom}></label>
      <label>{i18n.t('fld_death_to')}<input type="number" bind:value={fDeathTo}></label>
    </div>
    <label class="rel">{i18n.t('fld_death_place')}
      <input type="search" bind:value={fDeathPlace} autocomplete="off">
      {#if fDeathPlace && suggest(fDeathPlace).length}
        <div class="sugg">
          {#each suggest(fDeathPlace) as s}
            <button type="button" onclick={() => { fDeathPlace = s }}>{s}</button>
          {/each}
        </div>
      {/if}
    </label>
    <label>{i18n.t('fld_event')}
      <select bind:value={fEvent}>
        <option value="">—</option>
        {#each EVENT_TYPES as [tag, key]}
          <option value={tag}>{i18n.t(key)}</option>
        {/each}
      </select>
    </label>
    <div class="fbtns">
      <button class="primary" onclick={find}>{i18n.t('find')}</button>
      <button onclick={clearAll}>{i18n.t('clear')}</button>
    </div>
  </aside>
</div>

<style>
  .layout { display: flex; gap: 1.4rem; align-items: flex-start; }
  main { flex: 1; min-width: 0; }
  aside { width: 17rem; flex: none; position: sticky; top: 3.2rem;
    border: 1px solid var(--rule); border-radius: 4px; background: var(--card);
    padding: .8rem .9rem; }
  aside h2 { font-size: .8rem; margin: 0 0 .6rem; color: var(--soft);
    text-transform: uppercase; letter-spacing: .05em; }
  aside label { display: block; font-size: .74rem; color: var(--soft);
    margin: 0 0 .5rem; }
  aside input, aside select { width: 100%; font: inherit; font-size: .8rem;
    margin-top: .15rem; }
  .pair { display: flex; gap: .4rem; }
  .pair label { flex: 1; }
  .rel { position: relative; }
  .sugg { position: absolute; z-index: 20; left: 0; right: 0; top: 100%;
    background: var(--card); border: 1px solid var(--rule); border-radius: 3px;
    max-height: 12rem; overflow: auto; }
  .sugg button { display: block; width: 100%; text-align: left; font-size: .74rem;
    padding: .25rem .5rem; border: 0; background: none; cursor: pointer;
    color: var(--ink); }
  .sugg button:hover { background: #f6f1e8; }
  .fbtns { display: flex; gap: .4rem; margin-top: .6rem; }
  .fbtns .primary { background: var(--accent); color: #fff;
    border-color: var(--accent); }
  .toolbar { display: flex; gap: .7rem; align-items: center; margin: .4rem 0 .6rem; }
  .toolbar .stat { font-size: .78rem; color: var(--faint); }
  table.plist { width: 100%; }
  tr.group td { padding: 0; border-bottom: 1px solid var(--rule);
    background: var(--card); }
  .ghead { display: flex; gap: .5rem; align-items: center; width: 100%;
    background: none; border: 0; font: inherit; padding: .4rem .5rem;
    cursor: pointer; text-align: left; color: var(--ink); }
  .ghead:hover { background: #f6f1e8; }
  .arrow { display: inline-block; transition: transform .15s ease;
    color: var(--faint); }
  .arrow.open { transform: rotate(90deg); }
  td.ln { color: var(--soft); }
  td.pid { font-family: ui-monospace, Consolas, monospace; font-size: .72rem;
    color: var(--faint); white-space: nowrap; }
  td.sex { color: var(--faint); width: 2rem; }
  td.dates { color: var(--faint); font-size: .8rem; white-space: nowrap; }
  @media (max-width: 900px) {
    .layout { flex-direction: column-reverse; }
    aside { width: auto; position: static; }
  }
</style>
