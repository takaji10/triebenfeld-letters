<script>
  import { db, goto, treeId, treeTitle, startPerson, hasMedia } from '../lib/db.svelte.js'
  import { i18n } from '../lib/i18n.js'

  let q = $state('')

  // top surnames by count, from the index itself
  const counts = $derived.by(() => {
    if (!db.index) return []
    const c = {}
    for (const v of Object.values(db.index)) {
      if (v.sn) c[v.sn] = (c[v.sn] || 0) + 1
    }
    return Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 24)
  })
</script>

<section class="hero">
  <h1>{treeTitle(i18n.lang) || i18n.t('app')}</h1>
  {#if db.meta?.lead?.[i18n.lang] || db.meta?.lead?.en}
    <p class="lead">{db.meta.lead[i18n.lang] || db.meta.lead.en}</p>
  {:else if treeId() === 'zelmer'}
    <p class="lead">
      The Zelmer family and its related lines — the database behind the
      Trąbczyn archive edition. Living people are shown by surname only.
    </p>
  {/if}
  <form onsubmit={(e) => { e.preventDefault(); goto('search?q=' + encodeURIComponent(q)) }}>
    <input type="search" placeholder={i18n.t('search_placeholder')} bind:value={q}>
    <button class="primary">{i18n.t('nav_search')}</button>
  </form>
</section>

{#if db.meta}
  <div class="counts">
    <div class="count"><b>{db.meta.counts.people.toLocaleString()}</b><span>{i18n.t('people_count')}</span></div>
    <div class="count"><b>{db.meta.counts.families.toLocaleString()}</b><span>{i18n.t('families_count')}</span></div>
    {#if hasMedia()}
      <div class="count"><b>{db.meta.counts.media.toLocaleString()}</b><span>{i18n.t('media_count')}</span></div>
    {/if}
    <div class="count"><b>{db.meta.counts.geocoded_places.toLocaleString()}</b>
      <span>{i18n.t('places_count')} · {i18n.t('geocoded_count')}</span></div>
  </div>
  <p class="stamp">{i18n.t('data_as_of')} {db.meta.built}</p>
{/if}

<a class="startree" href={'#/tree/' + startPerson() + '?mode=big'}>
  ⧗ {i18n.t('nav_tree')} — {treeId() === 'zelmer' ? i18n.t('start_tree') : i18n.t('start_tree_generic')}
</a>

<h2>{i18n.t('nav_surnames')}</h2>
<div class="chips">
  {#each counts as [name, n]}
    <a class="chip" href={'#/surname/' + encodeURIComponent(name)}>
      {name} <b>{n}</b>
    </a>
  {/each}
  <a class="chip all" href="#/surnames">…</a>
</div>

<style>
  .hero { text-align: center; padding: 1.6rem 0 1rem; }
  .hero h1 { font-size: 1.6rem; margin: 0 0 .5rem; }
  .lead { color: var(--soft); max-width: 34rem; margin: 0 auto 1rem;
    font-size: .92rem; }
  form { display: flex; gap: .5rem; justify-content: center; flex-wrap: wrap; }
  button.primary { background: var(--accent); color: #fff;
    border-color: var(--accent); }
  .counts { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center;
    margin: 1.2rem 0 .3rem; }
  .count { border: 1px solid var(--rule); border-radius: 4px; background: var(--card);
    padding: .5rem .9rem; min-width: 7rem; text-align: center; }
  .count b { display: block; font-size: 1.2rem; font-family: var(--serif); }
  .count span { font-size: .7rem; color: var(--faint); }
  .stamp { text-align: center; font-size: .74rem; color: var(--faint); }
  h2 { font-size: 1.02rem; margin: 1.6rem 0 .5rem; text-align: center; }
  .chips { display: flex; flex-wrap: wrap; gap: .4rem; justify-content: center; }
  .chip { border: 1px solid var(--rule); border-radius: 999px; background: var(--card);
    padding: .25rem .7rem; font-size: .82rem; color: var(--ink); }
  .chip:hover { border-color: var(--accent); text-decoration: none; }
  .chip b { color: var(--faint); font-weight: 600; margin-left: .2rem; }
  .chip.all { color: var(--accent); }
  .startree { display: block; max-width: 44rem; margin: 1.4rem auto 0;
    text-align: center; padding: .8rem 1.2rem; border: 1px solid var(--accent);
    border-radius: 6px; background: var(--card); color: var(--accent);
    font-family: var(--serif); font-size: .95rem; }
  .startree:hover { background: #f6f1e8; text-decoration: none; }
</style>
