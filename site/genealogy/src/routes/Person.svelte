<script>
  import { db, personName, goto } from '../lib/db.svelte.js'
  import { i18n, EVENT_LABELS } from '../lib/i18n.js'
  import { fmtDate } from '../lib/dates.js'
  import { person, mediaURL } from '../lib/data.js'
  import MediaViewer from '../lib/MediaViewer.svelte'
  import Tree from '../lib/Tree.svelte'

  let { id } = $props()

  // the interface language rides behind i18n's back for dates; read it
  // from the same store so a switch re-renders them
  let langTick = $state(0)
  i18n.subscribe(() => { langTick++ })
  const fmt = (raw) => { langTick; return fmtDate(raw, i18n.lang) }

  // life dates from the index: year pair for the compact lists, the raw
  // texts for the formatted rendering
  function life(v) {
    if (!v) return ''
    if (v.L) return i18n.t('living')
    const b = v.br ? fmt(v.br) : (v.b != null ? String(v.b) : '')
    const d = v.dr ? fmt(v.dr) : (v.d != null ? String(v.d) : '')
    if (!b && !d) return ''
    return b && d ? `${b} – ${d}` : (b || d)
  }

  let shard = $state(null)
  let error = $state(null)

  $effect(() => {
    let live = true
    shard = null
    error = null
    if (!id) return
    person(id).then(s => { if (live) shard = s })
      .catch(e => { if (live) error = String(e) })
    return () => { live = false }
  })

  function fam(idf) { return db.families?.[idf] || null }

  const parents = $derived.by(() => {
    if (!shard?.famc?.length) return []
    const f = fam(shard.famc[0])
    if (!f) return []
    return [f.husb, f.wife].filter(Boolean)
  })

  // the other children of the person's own parent family
  const siblings = $derived.by(() => {
    if (!shard?.famc?.length) return []
    const f = fam(shard.famc[0])
    if (!f) return []
    return (f.chil || []).filter(c => c !== id)
  })

  const partners = $derived.by(() => {
    if (!shard?.fams?.length) return []
    return shard.fams.map(fx => {
      const f = fam(fx)
      if (!f) return null
      const spouse = f.husb === id ? f.wife : f.husb
      return {
        spouse, marr: f.marr || null, children: f.chil || [],
      }
    }).filter(Boolean)
  })

  const events = $derived(shard?.events || [])

  const gallery = $derived.by(() => {
    if (!shard) return []
    const seen = new Set()
    const items = []
    for (const m of shard.media || []) {
      if (!seen.has(m.path)) { seen.add(m.path); items.push(m) }
    }
    for (const e of events) {
      for (const c of e.citations || []) {
        for (const m of c.m || []) {
          if (!seen.has(m.path)) { seen.add(m.path); items.push({ ...m, region: null }) }
        }
      }
    }
    return items
  })

  // the portrait URL for any person in the index (the thumb derivative
  // joined with the media base); null when there is no picture
  function avatar(x) {
    const v = db.index?.[x]
    return v?.pt && db.meta?.media_base ? db.meta.media_base + v.pt : null
  }

  function label(ev) {
    return i18n.t(EVENT_LABELS[ev.tag] || 'in_tree')
  }

  function sourceOf(cit) {
    return cit.s ? (db.sources?.[cit.s] || null) : null
  }

  function repoOf(cit) {
    const s = sourceOf(cit)
    return s?.repo ? (db.repos?.[s.repo] || null) : null
  }
</script>

{#if error}
  <p class="lead error">{error}</p>
{:else if !shard}
  <p class="lead">…</p>
{:else}
  <article>
    <header class="head">
      <div class="idline">
        {#if avatar(id)}
          <img class="avatar" src={avatar(id)} alt="">
        {:else}
          <svg class="avatar" viewBox="0 0 48 48" aria-hidden="true">
            <circle cx="24" cy="24" r="23" fill="#e8e2d6" stroke="var(--rule)" />
            <g fill="#b3a897">
              <circle cx="24" cy="18.5" r="9" />
              <path d="M 8 41 a 16 12.5 0 0 1 32 0 Z" />
            </g>
          </svg>
        {/if}
        <div>
          <h1>{shard.name} <span class="idn">{id}</span></h1>
          <div class="pills">
            <span class="sxline">{shard.sex === 'F' ? '♀' : shard.sex === 'M' ? '♂' : ''}</span>
            {#if db.index?.[id]}<span class="headlife">{life(db.index[id])}</span>{/if}
            {#if shard.living}<span class="pill warn">{i18n.t('privacy_note')}</span>{/if}
            {#each shard.names as alt}
              {#if alt.type}<span class="pill dim">{alt.type}: {alt.given} {alt.surname}</span>{/if}
            {/each}
          </div>
        </div>
      </div>
    </header>

    <section>
      <h2>{i18n.t('in_tree')}</h2>
      <Tree {id} embed />
    </section>

    {#if parents.length}
      <section>
        <h2>{i18n.t('parents')}</h2>
        <ul class="people">
          {#each parents as pid}
            {@const v = db.index?.[pid]}
            <li>
              <a href={'#/person/' + pid}>{personName(pid)}</a>
              <span class="pid">{pid}</span>
              {#if v}<span class="yrs">{life(v)}</span>{/if}
            </li>
          {/each}
        </ul>
      </section>
    {/if}

    {#if siblings.length}
      <section>
        <h2>{i18n.t('siblings')}</h2>
        <ul class="people">
          {#each siblings as sid}
            {@const v = db.index?.[sid]}
            <li>
              <a href={'#/person/' + sid}>{personName(sid)}</a>
              <span class="pid">{sid}</span>
              {#if v}<span class="yrs">{life(v)}</span>{/if}
            </li>
          {/each}
        </ul>
      </section>
    {/if}

    {#if partners.length}
      <section>
        <h2>{i18n.t('spouses_children')}</h2>
        {#each partners as p, i}
          <div class="union">
            <p class="spouse">
              {#if p.spouse}
                <a href={'#/person/' + p.spouse}>{personName(p.spouse)}</a>
                <span class="pid">{p.spouse}</span>
                {#if db.index?.[p.spouse]}<span class="yrs">{life(db.index[p.spouse])}</span>{/if}
              {:else}—{/if}
              {#if p.marr?.date}
                <span class="marr">· {i18n.t('married')} {fmt(p.marr.date.raw)}
                  {#if p.marr.place} — {p.marr.place}{/if}</span>
              {/if}
            </p>
            {#if p.children.length}
              <ul class="people">
                {#each p.children as cid}
                  {@const v = db.index?.[cid]}
                  <li>
                    <a href={'#/person/' + cid}>{personName(cid)}</a>
                    <span class="pid">{cid}</span>
                    {#if v}<span class="yrs">{life(v)}</span>{/if}
                  </li>
                {/each}
              </ul>
            {/if}
          </div>
        {/each}
      </section>
    {/if}

    {#if events.length}
      <section>
        <h2>{i18n.t('timeline')}</h2>
        <ol class="timeline">
          {#each events as ev}
            <li>
              <div class="rowline">
                <span class="tag">{label(ev)}</span>
                {#if ev.date}<span class="date">{fmt(ev.date.raw)}</span>{/if}
                {#if ev.sp}
                  <span class="value">{i18n.t('with_spouse')}
                    <a href={'#/person/' + ev.sp}>{ev.with || personName(ev.sp)}</a>
                    <span class="pid">{ev.sp}</span>
                  </span>
                {/if}
                {#if ev.place}
                  <span class="place">
                    <a href={'#/place/' + encodeURIComponent(ev.place)}>{ev.place}</a>
                  </span>
                {/if}
                {#if ev.value && ev.tag !== 'NAME'}<span class="value">{ev.value}</span>{/if}
              </div>
              {#if ev.note}<div class="note">{ev.note}</div>{/if}
              {#if ev.citations?.length}
                <details class="cits">
                  <summary>{ev.citations.length} {i18n.t('citations')}</summary>
                  {#each ev.citations as cit}
                    {@const s = sourceOf(cit)}
                    {@const rep = repoOf(cit)}
                    <div class="cit">
                      {#if s}<span class="src">{s.title || cit.s}</span>
                        {#if s.author}<span class="dim"> · {s.author}</span>{/if}
                        {#if rep}
                          <span class="dim"> · {rep.name}
                            {#if s.callno} [{s.callno}]{/if}</span>
                        {/if}
                      {:else}<span class="src dim">{cit.s}</span>{/if}
                      {#if cit.page}<div class="page">{i18n.t('page')}: {cit.page}</div>{/if}
                      {#if cit.text}<blockquote>{cit.text}</blockquote>{/if}
                      {#each cit.m || [] as m}
                        <div class="citmedia">
                          <MediaViewer path={m.path} title={m.title}
                                       form={m.form} personId={id} />
                        </div>
                      {/each}
                    </div>
                  {/each}
                </details>
              {/if}
            </li>
          {/each}
        </ol>
      </section>
    {/if}

    {#if shard.notes?.length}
      <section>
        <h2>{i18n.t('notes')}</h2>
        {#each shard.notes as n}
          <p class="note-block">{n}</p>
        {/each}
      </section>
    {/if}

    {#if gallery.length}
      <section>
        <h2>{i18n.t('media')} <span class="pill acc">{gallery.length}</span></h2>
        <div class="gallery">
          {#each gallery as m}
            <div class="item">
              <MediaViewer path={m.path} title={m.title} form={m.form}
                           personId={id} />
            </div>
          {/each}
        </div>
      </section>
    {/if}
  </article>
{/if}

<style>
  .lead { color: var(--soft); }
  .error { color: var(--warn); }
  .head h1 { font-size: 1.4rem; margin: 0 0 .4rem; }
  .idline { display: flex; gap: .9rem; align-items: center; }
  .avatar { width: 64px; height: 64px; border-radius: 50%; object-fit: cover;
    border: 1px solid var(--rule); background: var(--card); flex: none; }
  .avatar.ph { display: grid; place-items: center; font-size: 1.6rem;
    color: var(--faint); }
  .headlife { color: var(--faint); font-size: .84rem; }
  .idn { font-family: ui-monospace, Consolas, monospace; font-size: .82rem;
    color: var(--faint); font-weight: 400; margin-left: .35rem; }
  .sxline { color: var(--soft); font-size: 1rem; }
  .pills { display: flex; flex-wrap: wrap; gap: .35rem; align-items: center; }
  section { margin-top: 1.6rem; }
  h2 { font-size: .95rem; margin: 0 0 .5rem; color: var(--soft);
    text-transform: uppercase; letter-spacing: .05em; font-family: var(--sans);
    font-weight: 600; font-size: .74rem; }
  ul.people { list-style: none; margin: 0; padding: 0; }
  ul.people li { padding: .2rem 0; }
  .pid { font-family: ui-monospace, Consolas, monospace; font-size: .72rem;
    color: var(--faint); margin-left: .35rem; white-space: nowrap; }
  .yrs { color: var(--faint); font-size: .8rem; margin-left: .45rem;
    white-space: nowrap; }
  .union { border-left: 3px solid var(--rule); padding-left: .8rem; margin: 0 0 .8rem; }
  .spouse { margin: .1rem 0 .3rem; }
  .marr { color: var(--faint); font-size: .84rem; }
  ol.timeline { list-style: none; margin: 0; padding: 0; }
  ol.timeline li { border-left: 2px solid var(--rule); padding: .35rem 0 .5rem 1rem;
    position: relative; }
  ol.timeline li::before { content: ''; position: absolute; left: -5px; top: .7rem;
    width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
  .rowline { display: flex; flex-wrap: wrap; gap: .5rem; align-items: baseline; }
  .tag { font-size: .74rem; text-transform: uppercase; letter-spacing: .04em;
    color: var(--accent); font-weight: 700; min-width: 6.2rem; }
  .date { font-family: var(--serif); }
  .value { color: var(--soft); }
  .place { font-size: .84rem; color: var(--soft); }
  .rowline .place { font-size: .84rem; }
  .note { font-size: .84rem; color: var(--soft); white-space: pre-wrap; }
  .cits { margin-top: .3rem; }
  .cits summary { font-size: .76rem; color: var(--faint); cursor: pointer; }
  .cit { margin: .5rem 0; padding: .4rem .6rem; background: var(--card);
    border: 1px solid var(--rule); border-radius: 3px; font-size: .82rem; }
  .src { font-weight: 600; }
  .dim { color: var(--faint); }
  .page { color: var(--soft); }
  blockquote { margin: .4rem 0 0; padding-left: .7rem; border-left: 3px solid var(--rule);
    color: var(--soft); font-family: var(--serif); white-space: pre-wrap; }
  .citmedia { margin-top: .4rem; }
  .note-block { font-family: var(--serif); white-space: pre-wrap;
    background: var(--card); border: 1px solid var(--rule); padding: .7rem .9rem;
    border-radius: 3px; font-size: .9rem; }
  .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
    gap: .8rem; }
</style>
