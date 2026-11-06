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
  import { fmtDate } from './dates.js'
  import { layout, hasMoreUp, hasMoreDown,
           CARD_W, CARD_H, CELL, ROW_H, WINDOW_UP, WINDOW_DOWN } from './tree.js'

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
    // presses inside the expanded card belong to the panel - its links
    // and buttons need the events (pointer capture would retarget them
    // to the viewport, the Firefox lesson)
    if (e.target?.closest?.('.detail')) return
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
      cardClick(was.id)
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

  // clicking a card expands it in place - the detail panel (birth
  // date+place, death date+place, a link to the person page) opens
  // beside the card, rendered inside the chart so it pans and zooms
  // with everything else; and the view centres on the card, which
  // otherwise sits cut off at the viewport's edge (the editor,
  // 2026-11-06). The panel closes on a second click, on its ×, or when
  // another card is opened.
  let openCard = $state(null)

  function cardClick(pid) {
    openCard = openCard === pid ? null : pid
    if (openCard) centreOnCard(openCard)
  }

  function gotoPerson(pid) { goto('person/' + pid) }

  // the portrait URL for a person in the index; null when there is none
  function avatarOf(pid) {
    const v = db.index?.[pid]
    return v?.pt && db.meta?.media_base ? db.meta.media_base + v.pt : null
  }

  // the open card's node (the card itself, or the block whose spouse it
  // is) - the panel renders in chart coordinates
  const openNode = $derived.by(() => {
    if (!openCard || !chart) return null
    return chart.nodes.find(x => x.id === openCard || x.spouse === openCard)
      || null
  })

  // centre the view on a card (content coordinates, base included)
  function centreOn(cx, cy) {
    if (!el) return
    const rect = el.getBoundingClientRect()
    if (rect.width <= 0) return
    tx = rect.width / 2 - cx * scale
    ty = rect.height / 2 - cy * scale
  }

  function centreOnCard(pid) {
    if (!chart) return
    const n = chart.nodes.find(x => x.id === pid || x.spouse === pid)
    if (!n) return
    // the block centre of the card that was clicked (the spouse card's
    // centre when the spouse was clicked)
    const left = n.spouse === pid ? n.x + CELL : n.x
    centreOn(chart.baseX + left + CARD_W / 2,
             chart.baseY + n.y + CARD_H / 2)
  }

  // the navigation arrows: does more tree exist beyond the window?
  const moreUp = $derived(db.ready && focusId ? hasMoreUp(db, focusId) : false)
  const moreDown = $derived(db.ready && focusId ? hasMoreDown(db, focusId) : false)

  // step: slide the window one generation out - the next step renders
  // while the far row derenders (the editor's model of the master tree)
  function step(dir) {
    const dbi = db
    if (dir === 'up') {
      // a parent of the focus: the window slides one row up
      const par = parentsOf(dbi, focusId).find(p => dbi.index[p])
      if (par) setFocus(par)
    } else {
      // a child with recorded descendants
      const child = unionsOf(dbi, focusId)
        .flatMap(u => u.children)
        .find(c => dbi.index[c])
      if (child) setFocus(child)
    }
  }

  function parentsOf(dbi, pid) {
    const p = dbi.index[pid]
    const f = p && p.fc && p.fc.length ? dbi.families[p.fc[0]] : null
    if (!f) return []
    return [f.husb, f.wife].filter(Boolean)
  }
  function unionsOf(dbi, pid) {
    const p = dbi.index[pid]
    if (!p) return []
    return (p.fs || []).map(f => dbi.families[f]).filter(Boolean)
      .map(f => ({ spouse: f.husb === pid ? f.wife : f.husb,
                   children: f.chil || [] }))
  }

  // setFocus: the window's centre changes (embed: local state; route:
  // the URL)
  function setFocus(pid) {
    openCard = null
    if (embed) localId = pid
    else goto('tree/' + pid + (effMode !== 'hourglass' ? '?mode=' + effMode : ''))
  }

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
               class:open={openCard === n.id}
               transform="translate({n.x},{n.y})">
              <rect width={CARD_W} height={CARD_H} rx="4"
                    stroke={n.focus || openCard === n.id ? 'var(--accent)'
                      : v?.sx === 'F' ? '#9c5470'
                      : v?.sx === 'M' ? '#46618a' : 'var(--rule)'}
                    stroke-width={n.focus || openCard === n.id ? 2 : 1} fill="var(--card)" />
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
    {#if openNode}
      {@const on = openNode}
      {@const isSpouse = on.spouse === openCard}
      {@const dv = db.index[openCard]}
      {@const px = isSpouse ? on.x + CELL : on.x}
      <!-- the expanded card, rendered inside the chart: it pans and
           zooms with everything else, the way the editor asked -->
      <foreignObject x={px} y={on.y + CARD_H + 6} width="250" height="190"
                     class="detailspace">
        <div class="detail" xmlns="http://www.w3.org/1999/xhtml">
          <button class="dclose" onclick={() => { openCard = null }}
                  aria-label="close">×</button>
          <div class="dhead">
            {#if avatarOf(openCard)}
              <img class="dav" src={avatarOf(openCard)} alt="">
            {:else}
              <svg class="dav" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#e8e2d6" stroke="var(--rule)" /><g fill="#b3a897"><circle cx="24" cy="18.5" r="9" /><path d="M 8 41 a 16 12.5 0 0 1 32 0 Z" /></g></svg>
            {/if}
            <div>
              <div class="dname">{dv?.n || openCard}</div>
              <div class="dpid">{openCard}</div>
            </div>
          </div>
          {#if dv && !dv.L}
            {#if dv.br || dv.b}<div class="drow"><span class="dlab">born</span> {dv.br ? fmtDate(dv.br, i18n.lang) : dv.b}{#if dv.bp} · {dv.bp}{/if}</div>{/if}
            {#if dv.dr || dv.d}<div class="drow"><span class="dlab">died</span> {dv.dr ? fmtDate(dv.dr, i18n.lang) : dv.d}{#if dv.dp} · {dv.dp}{/if}</div>{/if}
          {:else if dv?.L}
            <div class="drow">{i18n.t('privacy_note')}</div>
          {/if}
          <div class="dacts">
            <a class="dlink" href={'#/person/' + openCard}>{i18n.t('go_to_person')} →</a>
            {#if openCard !== focusId}
              <button class="dcentre" onclick={() => { setFocus(openCard) }}>
                {i18n.t('centre_here')}
              </button>
            {/if}
          </div>
        </div>
      </foreignObject>
    {/if}
  </div>
  <div class="navarrows">
    {#if moreUp}
      <button class="narr" title={i18n.t('show_ancestors')}
              onclick={() => step('up')}>↑ {i18n.t('show_ancestors')}</button>
    {/if}
    {#if moreDown}
      <button class="narr" title={i18n.t('show_descendants')}
              onclick={() => step('down')}>↓ {i18n.t('show_descendants')}</button>
    {/if}
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
  .viewport { position: relative; overflow: hidden; border: 1px solid var(--rule);
    border-radius: 3px; background: var(--paper2); touch-action: none;
    cursor: grab; user-select: none; max-height: 78vh; }
  /* the dedicated tree page: a window on the page, not a strip - 80%
     of the window's width and height (the editor's measure) */
  .viewport:not(.embed) { width: 80vw; height: 80vh; max-height: none;
    margin: 0 auto; }
  .viewport.embed { max-height: 34rem; }
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
  /* the expanded card, inside the chart: it pans and zooms with the
     tree; foreignObject carries the HTML */
  .detailspace { overflow: visible; }
  .detail { position: relative; width: 250px; box-sizing: border-box;
    background: var(--card); border: 1px solid var(--accent);
    border-radius: 5px; box-shadow: 0 6px 24px rgba(40, 32, 26, .18);
    padding: .6rem .7rem; font-size: .8rem; cursor: default; }
  .dclose { position: absolute; top: .2rem; right: .3rem; border: 0;
    background: none; font: inherit; font-size: 1rem; color: var(--faint);
    cursor: pointer; padding: .1rem .3rem; }
  .dclose:hover { color: var(--ink); }
  .dhead { display: flex; gap: .55rem; align-items: center; margin-bottom: .45rem; }
  .dav { width: 38px; height: 38px; border-radius: 50%; object-fit: cover;
    border: 1px solid var(--rule); flex: none; }
  .dname { font-weight: 600; line-height: 1.2; }
  .dpid { font-family: ui-monospace, Consolas, monospace; font-size: .7rem;
    color: var(--faint); }
  .drow { margin: .12rem 0; color: var(--soft); line-height: 1.35; }
  .dlab { display: inline-block; min-width: 2.4rem; color: var(--faint);
    font-size: .72rem; text-transform: uppercase; letter-spacing: .04em; }
  .dlink { display: inline-block; color: var(--accent); font-weight: 600; }
  .dlink:hover { text-decoration: underline; }
  .dacts { display: flex; gap: .7rem; align-items: center; margin-top: .45rem; }
  .dcentre { font: inherit; font-size: .74rem; padding: .12rem .5rem;
    border: 1px solid var(--rule); border-radius: 3px; background: var(--paper2);
    color: var(--soft); cursor: pointer; }
  .dcentre:hover { border-color: var(--accent); color: var(--accent); }
  /* the navigation arrows: render the next step, derender the previous */
  .navarrows { display: flex; gap: .5rem; margin-top: .4rem; }
  .narr { font: inherit; font-size: .78rem; padding: .2rem .7rem;
    border: 1px solid var(--accent); border-radius: 3px;
    background: var(--card); color: var(--accent); cursor: pointer; }
  .narr:hover { background: var(--accent); color: #fff; }
</style>
