<script>
  // The family trees: hourglass (default), pedigree (ancestors only) and
  // descendants. The layout is pure (tree.js); this component draws it and
  // handles pan (drag), zoom (wheel / pinch) and the two click targets
  // (chevron: recenter the chart there; card: open the person page).
  //
  // Embedded on the person page (embed): the mode pills switch a local
  // mode and the chevron re-roots the chart locally - both without
  // leaving the page; clicking a card still opens that person's page,
  // which is the move up or down the tree. On the tree route the pills
  // and chevron drive the URL as before.
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
  const links = $derived(chart ? chart.links : [])
  const W = $derived(chart ? chart.totalW * CELL + 40 : 800)
  const H = $derived(chart ? chart.rows * ROW_H + 60 : 400)

  // ---- pan & zoom -------------------------------------------------------

  let el
  let tx = $state(0), ty = $state(0), scale = $state(1)
  let dragging = null
  const pointers = new Map()
  let pinch = null

  function onWheel(e) {
    // embedded on the person page: a plain wheel scroll moves the page,
    // Ctrl+wheel zooms the chart (pinch always zooms)
    if (embed && !e.ctrlKey) return
    e.preventDefault()
    const k = e.deltaY < 0 ? 1.12 : 1 / 1.12
    const rect = el.getBoundingClientRect()
    const mx = e.clientX - rect.left, my = e.clientY - rect.top
    scale = Math.min(2.2, Math.max(0.35, scale * k))
    tx = mx - (mx - tx) * k
    ty = my - (my - ty) * k
  }
  function down(e) {
    el.setPointerCapture?.(e.pointerId)
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY })
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
      scale = Math.min(2.2, Math.max(0.35, pinch.s0 * k))
      tx = pinch.mx - (pinch.mx - pinch.tx0) * k
      ty = pinch.my - (pinch.my - pinch.ty0) * k
    } else if (dragging) {
      tx += e.clientX - prev.x
      ty += e.clientY - prev.y
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

  function center() {
    if (!el || !chart) return
    scale = 1
    const rect = el.getBoundingClientRect()
    if (rect.width <= 0) return
    // the focus card, centred both ways: the ancestors sit above it, the
    // descendants below, so the move up and down starts from the middle
    const f = chart.nodes.find(n => n.focus)
    const fx = (f ? f.x : chart.totalW / 2) * CELL + CARD_W / 2
    const fy = chart.focusY * ROW_H + CARD_H / 2
    tx = rect.width / 2 - fx
    ty = Math.max(12, rect.height / 2 - fy)
  }

  function recenter(pid) {
    if (embed) localId = pid
    else goto('tree/' + pid)
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
    <span class="stat"><button onclick={center}>⤢ fit</button></span>
  </div>
  <div class="viewport" class:embed bind:this={el}
       onwheel={onWheel} onpointerdown={down} onpointermove={move}
       onpointerup={up} onpointercancel={up}>
    <svg width={W} height={H}>
      <g transform="translate({tx},{ty}) scale({scale})">
        {#each links as [x1, y1, x2, y2]}
          {@const my = (y1 + y2) / 2}
          <path d="M {x1} {y1} L {x1} {my} L {x2} {my} L {x2} {y2}"
                fill="none" stroke="var(--rule)" stroke-width="1.5" />
        {/each}
        {#each chart.nodes as n (n.id + '@' + n.y)}
          {@const cx = n.x * CELL}
          {@const cy = n.y * ROW_H}
          {@const v = db.index[n.id]}
          {@const isFocus = n.id === focusId && n.y === chart.focusY}
          <g class="node" class:living={v?.L}
             transform="translate({cx},{cy})">
            <rect width={CARD_W} height={CARD_H} rx="4"
                  stroke={isFocus ? 'var(--accent)'
                    : v?.sx === 'F' ? '#9c5470'
                    : v?.sx === 'M' ? '#46618a' : 'var(--rule)'}
                  stroke-width={isFocus ? 2 : 1} fill="var(--card)" />
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
            {#if !isFocus}
              <g class="chev" onpointerup={(e) => { e.stopPropagation(); recenter(n.id) }}>
                <circle cx={CARD_W - 6} cy={CARD_H + 2} r="9"
                        fill="var(--accent)" opacity="0.85" />
                <text x={CARD_W - 6} y={CARD_H + 6} text-anchor="middle"
                      fill="#fff" class="che">›</text>
              </g>
            {/if}
            <rect width={CARD_W} height={CARD_H} fill="transparent"
                  class="hit" onpointerup={(e) => { e.stopPropagation(); gotoPerson(n.id) }} />
          </g>
        {/each}
      </g>
    </svg>
  </div>
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
</style>
