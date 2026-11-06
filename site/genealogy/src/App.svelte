<script>
  import { initDB, db, goto } from './lib/db.svelte.js'
  import { i18n } from './lib/i18n.js'
  import Home from './routes/Home.svelte'
  import Person from './routes/Person.svelte'
  import Search from './routes/Search.svelte'
  import Surnames from './routes/Surnames.svelte'
  import Places from './routes/Places.svelte'
  import Place from './routes/Place.svelte'
  import Map from './routes/Map.svelte'
  import Tree from './lib/Tree.svelte'

  initDB()

  let route = $state(parse(location.hash))
  let tick = $state(0)   // bumped on language change so the strings re-render

  function parse(h) {
    const s = (h || '').replace(/^#\/?/, '')
    const [path, query] = s.split('?')
    return {
      parts: path.split('/').filter(Boolean),
      q: new URLSearchParams(query || ''),
    }
  }

  addEventListener('hashchange', () => { route = parse(location.hash) })
  i18n.subscribe(() => { tick++ })

  $effect(() => { document.title = i18n.t('app') + ' · Trąbczyn Archive' })

  const tabs = [
    ['home', 'nav_home'], ['search', 'nav_search'],
    ['surnames', 'nav_surnames'], ['places', 'nav_places'],
    ['map', 'nav_map'],
  ]

  function activeTab() {
    const p = route.parts[0] || 'home'
    if (p === 'person' || p === 'surname') return 'surnames'
    if (p === 'place') return 'places'
    if (p === 'map') return 'map'
    return p
  }
</script>

{#key tick}
<header>
  <a class="brand" href="#/home"><h1>{i18n.t('app')}</h1></a>
  <nav>
    {#each tabs as [key, label]}
      <a href={'#/' + key} class:active={activeTab() === key}>{i18n.t(label)}</a>
    {/each}
  </nav>
  <select class="lang" value={i18n.lang}
          onchange={(e) => { i18n.lang = e.target.value }}>
    {#each i18n.langs as l}<option value={l}>{l.toUpperCase()}</option>{/each}
  </select>
</header>
{/key}

<main>
  {#key tick}
  {#if !db.ready}
    <div class="boot"><span>Loading the family database …</span></div>
  {:else if db.error}
    <div class="boot error">{db.error}</div>
  {:else if route.parts[0] === 'person'}
    <Person id={route.parts[1]} />
  {:else if route.parts[0] === 'search'}
    <Search q={route.q.get('q') || ''} />
  {:else if route.parts[0] === 'surnames'}
    <Surnames />
  {:else if route.parts[0] === 'surname'}
    <Surnames selected={route.parts[1]} />
  {:else if route.parts[0] === 'places'}
    <Places />
  {:else if route.parts[0] === 'map'}
    <Map />
  {:else if route.parts[0] === 'tree'}
    <Tree id={route.parts[1]} mode={route.q.get('mode') || 'hourglass'} />
  {:else if route.parts[0] === 'place'}
    <Place name={decodeURIComponent(route.parts[1] || '')} />
  {:else}
    <Home />
  {/if}
  {/key}
</main>

<style>
  header { position: sticky; top: 0; z-index: 10; display: flex;
    flex-wrap: wrap; gap: .4rem 1.1rem; align-items: center;
    background: var(--paper2); border-bottom: 1px solid var(--rule);
    padding: .55rem 1rem; }
  .brand h1 { font-size: 1.02rem; margin: 0; }
  .brand { color: inherit; }
  nav { display: flex; gap: .8rem; flex: 1; }
  nav a { font-size: .86rem; color: var(--soft); padding: .15rem .2rem;
    border-bottom: 2px solid transparent; }
  nav a.active { color: var(--accent); border-bottom-color: var(--accent);
    font-weight: 600; }
  .lang { font: inherit; font-size: .74rem; padding: .2rem .3rem;
    border: 1px solid var(--rule); border-radius: 3px; background: var(--card); }
  main { max-width: 58rem; margin: 0 auto; padding: 1.2rem 1rem 4rem; }
  .boot { display: grid; place-items: center; min-height: 50vh;
    color: var(--faint); font-family: var(--serif); }
  .boot.error { color: var(--warn); white-space: pre-wrap; padding: 1rem; }
  @media (max-width: 640px) {
    nav { order: 3; flex-basis: 100%; gap: 1rem; }
    main { padding: 1rem .8rem 4rem; }
  }
</style>
