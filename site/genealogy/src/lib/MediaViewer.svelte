<script>
  // One media item: the published derivative, with the Gramps focus
  // rectangle drawn when the editor drew one for this person.
  import { db } from './db.svelte.js'
  import { mediaURL } from './data.js'
  import { i18n } from './i18n.js'

  let {
    path,            // media path (the manifest key)
    personId = null, // whose page we are on: selects the region
    title = '',
    form = 'jpg',
  } = $props()

  let showRegion = $state(true)
  let failed = $state(false)

  const info = $derived(db.mediaInfo?.[path] || null)
  const region = $derived.by(() => {
    if (!info) return null
    if (info.regions && personId) return info.regions[personId] || null
    if (info.regions && !personId) return null
    return info.region || null
  })

  const url = $derived(mediaURL(db.mediaFiles || {}, path))
  const thumbURL = $derived(mediaURL(db.mediaFiles || {}, path, true))
  const box = $derived.by(() => {
    if (!region) return null
    const [x1, y1, x2, y2] = region
    return {
      left: Math.min(x1, x2), top: Math.min(y1, y2),
      width: Math.abs(x2 - x1), height: Math.abs(y2 - y1),
    }
  })

  const src = $derived(showRegion && box ? thumbURL : url)
</script>

{#if form === 'docx' || form === 'txt'}
  <a class="doc" href={url} target="_blank" rel="noopener">
    📄 {title || path.split('/').pop()} <span class="pill dim">{form}</span>
  </a>
{:else if url && !failed}
  <figure>
    <div class="frame">
      <img {src} alt={title || path} loading="lazy"
           onerror={() => { failed = true }} class:dimmed={showRegion && box}>
      {#if box && showRegion}
        <div class="region" style:left="{box.left}%" style:top="{box.top}%"
             style:width="{box.width}%" style:height="{box.height}%"></div>
      {/if}
    </div>
    <figcaption>
      {#if box}
        <button class="toggle" onclick={() => { showRegion = !showRegion }}>
          {showRegion ? i18n.t('show_region') : i18n.t('hide_region')}
        </button>
      {/if}
      {#if title}<span class="cap">{title}</span>{/if}
    </figcaption>
  </figure>
{:else}
  <div class="missing">
    {title || path.split('/').pop()}
    <span class="pill dim">{i18n.t('no_media_note')}</span>
  </div>
{/if}

<style>
  figure { margin: 0; }
  .frame { position: relative; overflow: hidden; border: 1px solid var(--rule);
    background: #fff; line-height: 0; }
  /* overflow:hidden keeps the region outline's dimming halo - a
     box-shadow with a 9999px spread - inside the photograph. Unclipped,
     it painted a grey film over the entire page (found 2026-11-06, the
     first person page seen with a working image and a drawn region). */
  img { width: 100%; height: auto; display: block; }
  img.dimmed { opacity: .82; }
  .region { position: absolute; border: 2px solid var(--accent);
    box-shadow: 0 0 0 9999px rgba(28, 26, 23, .28), inset 0 0 0 1px #fff;
    border-radius: 2px; pointer-events: none; }
  figcaption { display: flex; gap: .5rem; align-items: baseline;
    font-size: .74rem; color: var(--faint); padding: .3rem 0; }
  .toggle { font-size: .7rem; padding: .1rem .45rem; }
  .cap { word-break: break-word; }
  .doc, .missing { display: block; border: 1px dashed var(--rule);
    background: var(--card); padding: .6rem .8rem; font-size: .85rem;
    color: var(--soft); border-radius: 3px; }
  .missing { color: var(--faint); }
</style>
