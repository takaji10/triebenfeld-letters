<script>
  // The family trees: hourglass (default), pedigree (ancestors only) and
  // descendants. The layout is d3-flextree's tidy-tree algorithm
  // (tree.js); this component draws it and handles the interaction:
  // scroll to zoom, drag (or pinch) to pan, and the two click targets -
  // a card brings that person into view and expands their tree around
  // them, the corner chevron opens their person page.
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
  let moved = 0   // pointer travel since pointerdown: a click is < 6px
  const pointers = new Map()
  let pinch = null

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
    moved = 0
    if (pointers.size === 2) {
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
      moved += Math.abs(e.clientX - prev.x) + Math.abs(e.clientY - prev.y)
    }
  }
  function up(e) {
    pointers.delete(e.pointerId)
    if (pointers.size < 2) pinch = null
    if (pointers.size) return
    dragging = null
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

  // clicking a card: that person becomes the focus and their tree
  // expands around them, centred in view
  function reroot(pid) {
    if (embed) localId = pid
    else goto('tree/' + pid + (effMode !== 'hourglass' ? '?mode=' + effMode : ''))
  }
  function gotoPerson(pid) { goto('person/' + pid) }
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
    {/if}
    <span class="stat"><button onclick={fit}>⤢ fit</button></span>
  </div>
  <div class="viewport" class:embed bind:this={el}
       onwheel={onWheel} onpointerdown={down} onpointermove={move}
       onpointerup={up} onpointercancel={up}>
    <svg width={W} height={H}>
      <g transform="translate({tx},{ty}) scale({scale})">
        <g transform="translate({chart.baseX},{chart.baseY})">
          {#each chart.links as d}
            <path d={d} fill="none" stroke="var(--rule)" stroke-width="1.5" />
          {/each}
          {#each chart.splices as [x1, y1, x2, y2]}
            <line x1={x1} y1={y1} x2={x2} y2={y2}
                  stroke="var(--rule)" stroke-width="1.5" />
          {/each}
          {#each chart.nodes as n (n.id + '@' + n.y)}
            {@const v = db.index[n.id]}
            <g class="node" class:living={v?.L}
               transform="translate({n.x},{n.y})">
              <rect width={CARD_W} height={CARD_H} rx="4"
                    stroke={n.focus ? 'var(--accent)'
                      : v?.sx === 'F' ? '#9c5470'
                      : v?.sx === 'M' ? '#46618a' : 'var(--rule)'}
                    stroke-width={n.focus ? 2 : 1} fill="var(--card)" />
              <text x={CARD_W / 2} y="16" text-anchor="middle" class="nm">
                {(v?.n || n.id).slice(0, 22)}
              </text>
              <text x={CARD_W / 2} y="31" text-anchor="middle" class="yrs">
                {v?.L ? i18n.t('living')
                  : (v?.b || v?.d ? `${v?.b ?? ''}–${v?.d ?? ''}` : '')}
              </text>
              <text x={CARD_W / 2} y="45" text-anchor="middle" class="pid">
                {n.id}
              </text>
              {#if n.spouse}
                <g transform="translate({CELL},0)">
                  <rect width={CARD_W} height={CARD_H} rx="4"
                        stroke={db.index[n.spouse]?.sx === 'F' ? '#9c5470'
                          : db.index[n.spouse]?.sx === 'M' ? '#46618a'
                          : 'var(--rule)'}
                        stroke-width="1" fill="var(--card)" />
                  <text x={CARD_W / 2} y="16" text-anchor="middle" class="nm">
                    {(db.index[n.spouse]?.n || n.spouse).slice(0, 22)}
                  </text>
                  <text x={CARD_W / 2} y="31" text-anchor="middle" class="yrs">
                    {db.index[n.spouse]?.L ? i18n.t('living')
                      : (db.index[n.spouse]?.b || db.index[n.spouse]?.d
                        ? `${db.index[n.spouse]?.b ?? ''}–${db.index[n.spouse]?.d ?? ''}` : '')}
                  </text>
                  <text x={CARD_W / 2} y="45" text-anchor="middle" class="pid">
                    {n.spouse}
                  </text>
                </g>
              {/if}
              {#if !n.focus}
                <g class="chev" onclick={(e) => { e.stopPropagation(); if (moved < 6) gotoPerson(n.id) }}>
                  <circle cx={CARD_W - 4} cy={CARD_H + 1} r="9"
                          fill="var(--accent)" opacity="0.85" />
                  <text x={CARD_W - 4} y={CARD_H + 5} text-anchor="middle"
                        fill="#fff" class="che">›</text>
                </g>
              {/if}
              <rect width={n.w * CELL} height={CARD_H} fill="transparent"
                    class="hit" onclick={(e) => { e.stopPropagation(); if (!n.focus && moved < 6) reroot(n.id) }} />
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
  .viewport { overflow: hidden; border: 1px solid var(--rule); border-radius: 3px;
    background: var(--paper2); touch-action: none; cursor: grab;
    user-select: none; max-height: 78vh; }
  .viewport.embed { max-height: 26rem; }
  .viewport:active { cursor: grabbing; }
  svg { display: block; }
  text { font-family: var(--sans); pointer-events: none; }
  .nm { font-size: 11px; fill: var(--ink); }
  .yrs { font-size: 9.5px; fill: var(--faint); }
  .pid { font-family: ui-monospace, Consolas, monospace; font-size: 8px;
    fill: var(--faint); }
  .node.living rect { stroke-dasharray: 3 2; }
  .node .hit { cursor: pointer; }
  .chev { cursor: pointer; }
  .che { font-size: 12px; }
  .hint { font-size: .74rem; color: var(--faint); margin: .3rem 0 0; }
</style>
