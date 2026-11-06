<script>
  // The family trees: hourglass (default), pedigree (ancestors only) and
  // descendants. The layout is pure (tree.js); this component draws it and
  // handles pan (drag), zoom (wheel / pinch) and the two click targets
  // (chevron: recenter the chart there; card: open the person page).
  import { db, goto } from './db.svelte.js'
  import { i18n } from './i18n.js'
  import { layout, CARD_W, CARD_H, CELL, ROW_H } from './tree.js'

  let { id, mode = 'hourglass' } = $props()

  const chart = $derived(db.ready && id ? layout(db, id, mode) : null)
  const W = $derived(chart ? chart.totalW * CELL + 40 : 800)
  const H = $derived(chart ? chart.rows * ROW_H + 60 : 400)

  // ---- pan & zoom -------------------------------------------------------

  let el
  let tx = $state(0), ty = $state(0), scale = $state(1)
  let dragging = null
  const pointers = new Map()
  let pinch = null

  function onWheel(e) {
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
    if (!pointers.size) dragging = null
  }

  let lastKey = ''
  $effect(() => {
    const key = (id || '') + '/' + mode
    if (chart && el && key !== lastKey) {
      lastKey = key
      center()
    }
  })

  function center() {
    if (!el) return
    scale = 1
    const rect = el.getBoundingClientRect()
    if (rect.width > 0) {
      tx = rect.width / 2 - W / 2
      ty = 20
    }
  }

  function gotoPerson(pid) { goto('person/' + pid) }
  function gotoTree(pid) { goto('tree/' + pid) }
</script>

{#if !chart}
  <p class="lead">…</p>
{:else}
  <div class="modes">
    <a class="pill" class:acc={mode === 'hourglass'} href={'#/tree/' + id}>⧗</a>
    <a class="pill" class:acc={mode === 'pedigree'} href={'#/tree/' + id + '?mode=pedigree'}>↑</a>
    <a class="pill" class:acc={mode === 'descendants'} href={'#/tree/' + id + '?mode=descendants'}>↓</a>
    <span class="stat"><button onclick={center}>⤢ fit</button></span>
  </div>
  <div class="viewport" bind:this={el}
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
          {@const isFocus = n.id === id && n.y === chart.focusY}
          <g class="node" class:living={v?.L}
             transform="translate({cx},{cy})">
            <rect width={CARD_W} height={CARD_H} rx="4"
                  stroke={isFocus ? 'var(--accent)'
                    : v?.sx === 'F' ? '#9c5470'
                    : v?.sx === 'M' ? '#46618a' : 'var(--rule)'}
                  stroke-width={isFocus ? 2 : 1} fill="var(--card)" />
            <text x={CARD_W / 2} y="17" text-anchor="middle" class="nm">
              {(v?.n || n.id).slice(0, 22)}
            </text>
            <text x={CARD_W / 2} y="33" text-anchor="middle" class="yrs">
              {v?.L ? i18n.t('living')
                : (v?.b || v?.d ? `${v?.b ?? ''}–${v?.d ?? ''}` : '')}
            </text>
            {#if !isFocus}
              <g class="chev" onpointerup={(e) => { e.stopPropagation(); gotoTree(n.id) }}>
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
  .stat { font-size: .74rem; color: var(--faint); margin-left: auto; }
  .viewport { overflow: hidden; border: 1px solid var(--rule); border-radius: 3px;
    background: var(--paper2); touch-action: none; cursor: grab;
    user-select: none; max-height: 78vh; }
  .viewport:active { cursor: grabbing; }
  svg { display: block; }
  text { font-family: var(--sans); pointer-events: none; }
  .nm { font-size: 11px; fill: var(--ink); }
  .yrs { font-size: 9.5px; fill: var(--faint); }
  .node.living rect { stroke-dasharray: 3 2; }
  .node .hit { cursor: pointer; }
  .chev { cursor: pointer; }
  .che { font-size: 12px; }
</style>
