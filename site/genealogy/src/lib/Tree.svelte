<script>
  // The family trees: hourglass (default), pedigree (ancestors only) and
  // descendants. The layout is d3-flextree's tidy-tree algorithm
  // (tree.js); this component draws it and handles the interaction:
  // scroll to zoom, drag (or pinch) to pan, and clicking a card opens
  // that person's page (the editor's ruling, 2026-11-06: the move
  // through the tree is a navigation). The mode pills re-root the chart
  // in place on the person page (embed) and through the URL on the tree
  // route.
  //
  // Embedded on the person page (embed): the mode pills and the
  // re-rooting act on local state, so moving around the tree never
  // leaves the page. On the tree route both drive the URL.
  import { db, goto } from './db.svelte.js'
  import { i18n } from './i18n.js'
  import { layout, CARD_W, CARD_H, CELL, ROW_H } from './tree.js'

  let { id, mode = 'hourglass', embed = false } = $props()

  // embedded: the chart's focus and mode are the component's own state
  let localId = $state(null)
  let localMode = $state('hourglass')
  const focusId = $derived(embed ? (localId || id) : id)
  const effMode = $derived(embed ? localMode : mode)

  const chart = $derived(db.ready && focusId ? layout(db, focusId, effMode) : null)
  const W = $derived(chart ? chart.width : 800)
  const H = $derived(chart ? chart.height : 400)

  // ---- pan & zoom -------------------------------------------------------

  let el
  let tx = $state(0), ty = $state(0), scale = $state(1)
  let dragging = null
  const pointers = new Map()
  let pinch = null
  // what a press landed on, decided at pointerdown: the viewport keeps
  // the pointer captured while it pans (that is what makes a drag track
  // outside the frame), and a captured pointer retargets every later
  // pointer event AND the click that follows it to the capture element -
  // so neither pointerup nor click ever reaches the cards in Firefox or
  // any other spec-following browser. The card under the press is read
  // here (data-pid attributes on the card groups), and the action runs
  // at pointerup when the pointer travelled less than a click's worth.
  let press = null

  function onWheel(e) {
    // scroll zooms the chart (the hint below the chart says so); pinch
    // zooms on touch
    e.preventDefault()
    const k = e.deltaY < 0 ? 1.12 : 1 / 1.12
    const rect = el.getBoundingClientRect()
    const mx = e.clientX - rect.left, my = e.clientY - rect.top
    scale = Math.min(2.2, Math.max(0.3, scale * k))
    tx = mx - (mx - tx) * k
    ty = my - (my - ty) * k
  }
  function down(e) {
    el.setPointerCapture?.(e.pointerId)
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY })
    const card = e.target?.closest?.('[data-pid]')
    press = pointers.size === 1 && card
      ? { id: card.getAttribute('data-pid'),
          x: e.clientX, y: e.clientY }
      : null   // two fingers is a pinch, never a click
    if (pointers.size === 2) {
      press = null
      const [a, b] = [...pointers.values()]
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), s0: scale, tx0: tx, ty0: ty,
                mx: (a.x + b.x) / 2 - el.getBoundingClientRect().left,
                my: (a.y + b.y) / 2 - el.getBoundingClientRect().top }
      dragging = null
    } else {
      dragging = { x: e.clientX, y: e.clientY }
    }
  }
  function move(e) {
    if (!pointers.has(e.pointerId)) return
    const prev = pointers.get(e.pointerId)
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY })
    if (pointers.size === 2 && pinch) {
      const [a, b] = [...pointers.values()]
      const k = Math.hypot(a.x - b.x, a.y - b.y) / pinch.d
      scale = Math.min(2.2, Math.max(0.3, pinch.s0 * k))
      tx = pinch.mx - (pinch.mx - pinch.tx0) * k
      ty = pinch.my - (pinch.my - pinch.ty0) * k
    } else if (dragging) {
      tx += e.clientX - prev.x
      ty += e.clientY - prev.y
      // a drag cancels the press: this was a pan, not a click
      if (press && Math.hypot(e.clientX - press.x,
                              e.clientY - press.y) >= 6) press = null
    }
  }
  function up(e) {
    const was = press
    if (pointers.get(e.pointerId)) pointers.delete(e.pointerId)
    if (pointers.size < 2) pinch = null
    if (pointers.size) { press = null; return }
    dragging = null
    press = null
    if (e.type !== 'pointerup' || !was) return
    // a click: pointer stayed under 6px from press to release
    if (Math.hypot(e.clientX - was.x, e.clientY - was.y) < 6) {
      reroot(was.id)
    }
  }

  let lastKey = ''
  $effect(() => {
    const key = (focusId || '') + '/' + effMode
    if (chart && el && key !== lastKey) {
      lastKey = key
      center()
    }
  })

  // centre the view on the focus person, both ways. The content point
  // p renders at tx + scale*(baseX + p), so the focus centre needs the
  // base shift included - chart.focusX/focusY already carry it.
  function center(fitScale = null) {
    if (!el || !chart) return
    const rect = el.getBoundingClientRect()
    if (rect.width <= 0) return
    if (fitScale) scale = fitScale
    tx = rect.width / 2 - chart.focusX * scale
    ty = rect.height / 2 - chart.focusY * scale
  }

  // fit the whole chart inside the viewport
  function fit() {
    if (!el || !chart) return
    const rect = el.getBoundingClientRect()
    if (rect.width <= 0) return
    const s = Math.min(2.2, Math.max(0.3,
      Math.min(rect.width / chart.width, rect.height / chart.height)))
    center(s)
  }

  // clicking a card opens that person's page - the editor's ruling
  // (2026-11-06): the move through the tree is a navigation, not a
  // re-layout; the mode pills and the URL carry the re-rooting. The
  // flash marks the clicked card for the moment before the page turns.
  let flash = $state(false)
  let flashTimer = null
  function reroot(pid) {
    flash = false
    clearTimeout(flashTimer)
    requestAnimationFrame(() => { flash = true })
    flashTimer = setTimeout(() => { flash = false }, 1600)
    setTimeout(() => goto('person/' + pid), 250)
  }
  function gotoPerson(pid) { goto('person/' + pid) }

  // the card's name line: fitted into the card's width, two lines when
  // needed - SVG text does not wrap, so the words are laid by hand. A
  // name that still does not fit loses its end to an ellipsis; the ID
  // below the lines is the identity anyway.
  const NAME_W = CARD_W - 50
  function nameLines(full) {
    const words = String(full || '').split(/\s+/).filter(Boolean)
    const lines = []
    let cur = ''
    for (const w of words) {
      const next = cur ? cur + ' ' + w : w
      if (next.length > 18 && cur) {
        lines.push(cur)
        cur = w
      } else {
        cur = next
      }
    }
    if (cur) lines.push(cur)
    if (lines.length > 2) {
      lines.length = 2
      lines[1] = lines[1].replace(/\s*\S*$/, '') + '…'
    }
    // a single unbreakable word longer than the line (a name written
    // without spaces) loses its end to an ellipsis as well
    if (lines[0].length > 18) lines[0] = lines[0].slice(0, 18) + '…'
    return lines.length ? lines : ['']
  }
</script>

{#if !chart}
  <p class="lead">…</p>
{:else}
  <div class="modes">
    {#if embed}
      <button class="pill" class:acc={effMode === 'hourglass'}
              onclick={() => { localMode = 'hourglass' }}>⧗</button>
      <button class="pill" class:acc={effMode === 'pedigree'}
              onclick={() => { localMode = 'pedigree' }}>↑</button>
      <button class="pill" class:acc={effMode === 'descendants'}
              onclick={() => { localMode = 'descendants' }}>↓</button>
    {:else}
      <a class="pill" class:acc={effMode === 'hourglass'} href={'#/tree/' + focusId}>⧗</a>
      <a class="pill" class:acc={effMode === 'pedigree'} href={'#/tree/' + focusId + '?mode=pedigree'}>↑</a>
      <a class="pill" class:acc={effMode === 'descendants'} href={'#/tree/' + focusId + '?mode=descendants'}>↓</a>
      <a class="pill" class:acc={effMode === 'big'} href={'#/tree/' + focusId + '?mode=big'}>⊞</a>
    {/if}
    <span class="who">{db.index[focusId]?.n || focusId} <span class="pidtxt">{focusId}</span></span>
    <span class="stat"><button onclick={fit}>⤢ fit</button></span>
  </div>
  <div class="viewport" class:embed bind:this={el}
       onwheel={onWheel} onpointerdown={down} onpointermove={move}
       onpointerup={up} onpointercancel={up}>
    <svg width={W} height={H}>
      <g transform="translate({tx},{ty}) scale({scale})">
        <g transform="translate({chart.baseX},{chart.baseY})">
          {#snippet silhouette(cx, cy, r, uid)}
            <!-- the placeholder: a head-and-shoulders silhouette on the
                 tinted disc, the same for everyone whose picture the
                 database lacks. Clipped to the disc: the shoulders' arc
                 is wider than the circle by design. -->
            <clipPath id="sil-{uid}">
              <circle cx={cx} cy={cy} r={r} />
            </clipPath>
            <circle cx={cx} cy={cy} r={r} fill="#e8e2d6" stroke="var(--rule)" />
            <g fill="#b3a897" clip-path="url(#sil-{uid})">
              <circle cx={cx} cy={cy - r * 0.38} r={r * 0.42} />
              <path d={`M ${cx - r * 0.85} ${cy + r * 0.95}
                       a ${r * 0.85} ${r * 0.62} 0 0 1 ${r * 1.7} 0 Z`} />
            </g>
          {/snippet}
          {#each chart.links as d}
            <path d={d} fill="none" stroke="var(--rule)" stroke-width="1.5" />
          {/each}
          {#each chart.splices as [x1, y1, x2, y2]}
            <line x1={x1} y1={y1} x2={x2} y2={y2}
                  stroke="var(--rule)" stroke-width="1.5" />
          {/each}
          {#each chart.nodes as n (n.id + '@' + n.y)}
            {@const v = db.index[n.id]}
            {@const avatar = v?.pt && db.meta?.media_base
              ? db.meta.media_base + v.pt : null}
            <g class="node" class:living={v?.L}
               data-pid={n.id}
               class:flash={n.focus && flash}
               transform="translate({n.x},{n.y})">
              <rect width={CARD_W} height={CARD_H} rx="4"
                    stroke={n.focus ? 'var(--accent)'
                      : v?.sx === 'F' ? '#9c5470'
                      : v?.sx === 'M' ? '#46618a' : 'var(--rule)'}
                    stroke-width={n.focus ? 2 : 1} fill="var(--card)" />
              {#if avatar}
                <clipPath id="av-{n.id}">
                  <circle cx="21" cy="21" r="13" />
                </clipPath>
                <image href={avatar} x="8" y="8" width="26" height="26"
                       preserveAspectRatio="xMidYMid slice"
                       clip-path="url(#av-{n.id})" />
                <circle cx="21" cy="21" r="13" fill="none"
                        stroke="var(--rule)" />
              {:else}
                {@render silhouette(21, 21, 13, n.id)}
              {/if}
              {#if nameLines(v?.n || n.id).length === 2}
                <text x="42" y="14" text-anchor="start" class="nm"
                      textLength={nameLines(v?.n || n.id)[0].length > 18 ? NAME_W : undefined}
                      lengthAdjust="spacingAndGlyphs">
                  {nameLines(v?.n || n.id)[0]}
                </text>
                <text x="42" y="27" text-anchor="start" class="nm"
                      textLength={nameLines(v?.n || n.id)[1].length > 18 ? NAME_W : undefined}
                      lengthAdjust="spacingAndGlyphs">
                  {nameLines(v?.n || n.id)[1]}
                </text>
              {:else}
                <text x="42" y="21" text-anchor="start" class="nm"
                      textLength={nameLines(v?.n || n.id)[0].length > 18 ? NAME_W : undefined}
                      lengthAdjust="spacingAndGlyphs">
                  {nameLines(v?.n || n.id)[0]}
                </text>
              {/if}
              <text x="42" y="40" text-anchor="start" class="yrs">
                {v?.L ? i18n.t('living')
                  : (v?.b || v?.d ? `${v?.b ?? ''}–${v?.d ?? ''}` : '')}
              </text>
              <text x="42" y="52" text-anchor="start" class="pid">
                {n.id}
              </text>
              <rect width={CARD_W} height={CARD_H} fill="transparent"
                    class="hit" />
              {#if n.spouse}
                {@const sv = db.index[n.spouse]}
                {@const sav = sv?.pt && db.meta?.media_base
                  ? db.meta.media_base + sv.pt : null}
                <g transform="translate({CELL},0)" data-pid={n.spouse}>
                  <rect width={CARD_W} height={CARD_H} rx="4"
                        stroke={sv?.sx === 'F' ? '#9c5470'
                          : sv?.sx === 'M' ? '#46618a'
                          : 'var(--rule)'}
                        stroke-width="1" fill="var(--card)" />
                  {#if sav}
                    <clipPath id="av-{n.spouse}">
                      <circle cx="21" cy="21" r="13" />
                    </clipPath>
                    <image href={sav} x="8" y="8" width="26" height="26"
                           preserveAspectRatio="xMidYMid slice"
                           clip-path="url(#av-{n.spouse})" />
                    <circle cx="21" cy="21" r="13" fill="none"
                            stroke="var(--rule)" />
                  {:else}
                    {@render silhouette(21, 21, 13, n.spouse)}
                  {/if}
                  {#if nameLines(sv?.n || n.spouse).length === 2}
                    <text x="42" y="14" text-anchor="start" class="nm"
                          textLength={nameLines(sv?.n || n.spouse)[0].length > 18 ? NAME_W : undefined}
                          lengthAdjust="spacingAndGlyphs">
                      {nameLines(sv?.n || n.spouse)[0]}
                    </text>
                    <text x="42" y="27" text-anchor="start" class="nm"
                          textLength={nameLines(sv?.n || n.spouse)[1].length > 18 ? NAME_W : undefined}
                          lengthAdjust="spacingAndGlyphs">
                      {nameLines(sv?.n || n.spouse)[1]}
                    </text>
                  {:else}
                    <text x="42" y="21" text-anchor="start" class="nm"
                          textLength={nameLines(sv?.n || n.spouse)[0].length > 18 ? NAME_W : undefined}
                          lengthAdjust="spacingAndGlyphs">
                      {nameLines(sv?.n || n.spouse)[0]}
                    </text>
                  {/if}
                  <text x="42" y="40" text-anchor="start" class="yrs">
                    {sv?.L ? i18n.t('living')
                      : (sv?.b || sv?.d ? `${sv?.b ?? ''}–${sv?.d ?? ''}` : '')}
                  </text>
                  <text x="42" y="52" text-anchor="start" class="pid">
                    {n.spouse}
                  </text>
                  <rect width={CARD_W} height={CARD_H} fill="transparent"
                        class="hit" />
                </g>
              {/if}
            </g>
          {/each}
        </g>
      </g>
    </svg>
  </div>
  <p class="hint">{i18n.t('tree_hint')}</p>
{/if}

<style>
  .modes { display: flex; gap: .4rem; align-items: center; margin-bottom: .5rem; }
  .modes .pill { cursor: pointer; }
  .modes button.pill { font: inherit; border: 1px solid var(--rule); }
  .stat { font-size: .74rem; color: var(--faint); margin-left: auto; }
  .who { font-size: .8rem; color: var(--ink); font-weight: 600; }
  .pidtxt { font-family: ui-monospace, Consolas, monospace; font-size: .72rem;
    color: var(--faint); font-weight: 400; margin-left: .2rem; }
  .node.flash rect:first-of-type { animation: focuspulse 1.5s ease; }
  @keyframes focuspulse {
    0% { stroke: var(--accent); stroke-width: 4; }
    70% { stroke-width: 3; }
    100% { stroke-width: 2; }
  }
  .viewport { overflow: hidden; border: 1px solid var(--rule); border-radius: 3px;
    background: var(--paper2); touch-action: none; cursor: grab;
    user-select: none; max-height: 78vh; }
  .viewport.embed { max-height: 26rem; }
  .viewport:active { cursor: grabbing; }
  svg { display: block; }
  text { font-family: var(--sans); pointer-events: none; }
  .nm { font-size: 10.5px; fill: var(--ink); }
  .yrs { font-size: 9.5px; fill: var(--faint); }
  .pid { font-family: ui-monospace, Consolas, monospace; font-size: 8px;
    fill: var(--faint); }
  .node.living rect { stroke-dasharray: 3 2; }
  .node .hit { cursor: pointer; }
    .che { font-size: 12px; }
  .hint { font-size: .74rem; color: var(--faint); margin: .3rem 0 0; }
</style>
