// The tree layout.
//
// The positions come from d3-flextree - the standard tidy-tree algorithm
// (Reingold-Tilford 1981, in van der Ploeg's 2013 linear-time form for
// variable node sizes). That is what fixes the spacing: a person with a
// spouse beside them is simply a two-card-wide node, and the algorithm
// packs the generations without overlaps - the hand-rolled layout this
// replaces could not (seen 2026-11-06: spouse cards overlapping the
// focus card and the siblings' cards).
//
// The genealogy semantics stay here: who counts as a child, where
// spouses sit, and how the hourglass folds two tidy trees around the
// focus person - ancestors above (every parent a node of its own, so
// both blood lines walk up), descendants below (spouse beside, children
// beneath the couple). Coordinates are card units: x in cards, y in rows.
//
// Limits: MAX_UP generations of ancestors, MAX_DOWN of descendants. The
// chart is re-rootable - clicking a card makes that person the focus -
// so the limits bound a view, not the graph.

import { flextree } from 'd3-flextree'

export const CARD_W = 150
export const CARD_H = 56
export const GAP_X = 16
export const CELL = CARD_W + GAP_X
export const ROW_H = 96
// The chart is a window, not the whole graph: the focus's parents and
// grandparents above, the children below - and the grandchildren behind
// "+n" badges on the children's cards, one branch open at a time (the
// editor's ruling, 2026-11-07: render it in parts, or the wide families
// sprawl past twenty screen widths). The navigation arrows re-centre
// the window on a frontier person; the badges open a branch in place.
export const WINDOW_UP = 2
export const WINDOW_DOWN = 2

const makeTree = flextree({
  nodeSize: n => [n.data.w, 1],
  spacing: () => 0.55,
})

// hierarchy first, then the layout - the layout function wants hierarchy
// nodes, not raw data (raw input gets halfway wrapped and the nodeSize
// accessor then meets a node without .data)
function runTree(data) {
  const t = makeTree.hierarchy(data)
  makeTree(t)
  return t
}

function fam(db, idf) { return idf ? db.families[idf] || null : null }

function parentsOf(db, pid) {
  const p = db.index[pid]
  const f = p && p.fc && p.fc.length ? fam(db, p.fc[0]) : null
  if (!f) return []
  return [f.husb, f.wife].filter(Boolean)
}

function unionsOf(db, pid) {
  const p = db.index[pid]
  if (!p) return []
  return (p.fs || []).map(f => fam(db, f)).filter(Boolean)
    .map(f => ({ spouse: f.husb === pid ? f.wife : f.husb,
                 children: f.chil || [] }))
}

// The ancestor half: children edges point at the parents. Every parent
// becomes a node of its own - no spouse folding - so the father's line
// and the mother's line both walk to their full depth, and couples that
// share a child end up adjacent wherever the layout puts them.
function upTree(db, pid, depth, seen, maxUp = WINDOW_UP) {
  seen.add(pid)
  const children = []
  if (depth < maxUp) {
    for (const par of parentsOf(db, pid)) {
      if (!db.index[par] || seen.has(par)) continue
      const t = upTree(db, par, depth + 1, seen, maxUp)
      if (t) children.push(t)
    }
  }
  return { id: pid, spouses: [], w: 1, root: depth === 0, children }
}

// The descendant half: the person, the spouse their children share
// beside them (a card each), the children beneath the couple.
//
// The window the editor approved (2026-11-07) is expandable: the focus's
// children always render, but their children (the grandchildren) stay
// behind a "+n" badge on the child's card until the reader opens that
// branch - one branch open at a time (opening a second collapses the
// first), so the chart can never sprawl the ~21 screen widths the
// always-everything render produced (I0272). A spouse card appears only
// where the couple's children are visible - a hidden branch's couple is
// one card, the marriage still on the person page. openSet carries the
// branch currently open: the ids on the focus-to-leaf path (what
// descendantPath computes), so a deep branch keeps its ancestors open.
function downTree(db, pid, depth, seen, openSet) {
  seen.add(pid)
  const showKids = depth === 0 || openSet.has(pid)
  const spouses = []
  const children = []
  let kc = 0   // children in the published data, whatever the chart shows
  for (const u of unionsOf(db, pid)) {
    const kids = u.children.filter(c => db.index[c])
    kc += kids.length
    if (showKids) {
      if (u.spouse && u.spouse !== pid && db.index[u.spouse] &&
          !spouses.includes(u.spouse) &&
          (kids.length || depth === 0)) {
        spouses.push(u.spouse)
      }
      for (const c of kids) {
        if (seen.has(c)) continue
        const t = downTree(db, c, depth + 1, seen, openSet)
        if (t) children.push(t)
      }
    }
  }
  return { id: pid, spouses, w: spouses.length ? 2 : 1,
           root: depth === 0, children,
           kc, nk: showKids ? 0 : kc, on: showKids && depth > 0 }
}

// the focus-to-leaf path of family-child links: the ids a single open
// branch needs rendered above its leaf (the leaf's ancestors up to but
// excluding the focus). Empty when the leaf is not a descendant of the
// focus - a stale expansion after re-rooting opens nothing.
export function descendantPath(db, focusId, leafId) {
  const path = new Set()
  function walk(pid) {
    if (pid === focusId) return true
    if (path.has(pid)) return false
    path.add(pid)
    const p = db.index[pid]
    const f = p && p.fc && p.fc.length ? db.families[p.fc[0]] : null
    if (f) {
      for (const par of [f.husb, f.wife]) {
        if (par && db.index[par] && walk(par)) return true
      }
    }
    path.delete(pid)
    return false
  }
  if (leafId && db.index[leafId]) walk(leafId)
  return path
}

// does more tree exist beyond the window? (whether the arrows show)
export function hasMoreUp(db, pid, gens = WINDOW_UP) {
  const seen = new Set([pid])
  let frontier = [pid]
  for (let d = 0; d < gens; d++) {
    const next = []
    for (const x of frontier)
      for (const par of parentsOf(db, x))
        if (!seen.has(par) && db.index[par]) { seen.add(par); next.push(par) }
    if (!next.length) return false
    frontier = next
  }
  // one more generation beyond the window?
  for (const x of frontier)
    if (parentsOf(db, x).some(p => db.index[p] && !seen.has(p))) return true
  return false
}

export function hasMoreDown(db, pid, gens = WINDOW_DOWN) {
  const seen = new Set([pid])
  let frontier = [pid]
  for (let d = 0; d < gens; d++) {
    const next = []
    for (const x of frontier)
      for (const u of unionsOf(db, x))
        for (const c of u.children)
          if (!seen.has(c) && db.index[c]) { seen.add(c); next.push(c) }
    if (!next.length) return false
    frontier = next
  }
  for (const x of frontier)
    for (const u of unionsOf(db, x))
      if (u.children.some(c => db.index[c] && !seen.has(c))) return true
  return false
}

function elbow(x1, y1, x2, y2) {
  const my = (y1 + y2) / 2
  return `M ${x1} ${y1} L ${x1} ${my} L ${x2} ${my} L ${x2} ${y2}`
}

export function layout(db, id, mode = 'hourglass', openSet = new Set()) {
  if (!id || !db.index || !db.index[id]) return null
  // every mode renders the same window now - the modes differ only in
  // which half they show
  const up = (mode !== 'descendants')
    ? runTree(upTree(db, id, 0, new Set(), WINDOW_UP)) : null
  const down = (mode !== 'pedigree')
    ? runTree(downTree(db, id, 0, new Set(), openSet)) : null

  // both roots are the focus: align their centres on x=0, and let the
  // ancestor rows run upward (negative y), the descendant rows downward
  if (up) up.each(n => { n.px = (n.x - up.x) * CELL })
  if (down) down.each(n => { n.px = (n.x - down.x) * CELL })

  const nodes = []
  const links = []
  const splices = []
  let minX = Infinity, maxX = -Infinity
  let minY = Infinity, maxY = -Infinity
  let focusCX = 0, focusCY = CARD_H / 2   // the focus card's own centre

  function grow(min, max) {
    if (min < minX) minX = min
    if (max > maxX) maxX = max
  }

  // one card block: the person, plus the spouse card beside them when
  // the data has one. x/y is the block's top-left.
  function card(px, py, data, isFocus) {
    const w = data.w
    const blockLeft = px - w * CELL / 2
    nodes.push({ id: data.id, x: blockLeft, y: py, w,
                 spouse: data.spouses?.[0] || null, focus: isFocus,
                 nk: data.nk || 0, kc: data.kc || 0, on: !!data.on })
    if (isFocus) {
      focusCX = blockLeft + w * CELL / 2
      focusCY = py + CARD_H / 2
    }
    if (data.spouses?.length) {
      // the marriage line: origin-anchored (its left end) so the
      // component can animate it with the cards - it is always
      // GAP_X long, drawn at translate(x, y)
      splices.push({ x: blockLeft + CARD_W, y: py + CARD_H / 2,
                     id: data.id })
    }
    grow(blockLeft, blockLeft + w * CELL)
    if (py < minY) minY = py
    if (py + CARD_H > maxY) maxY = py + CARD_H
  }

  if (up) {
    up.each(n => {
      if (n.data.root && down) return   // the focus card comes from `down`
      card(n.px, -n.y * ROW_H, n.data, !down && n.data.root)
    })
    // the shift from a block's centre to the blood person's card centre:
    // the person card sits at the block's left, the spouse beside them
    const blockShift = w => w > 1 ? (w * CELL - CARD_W) / 2 : 0
    // the focus row renders the spouse from the down data, which the up
    // tree's own root node does not know about
    const focusShift = down && down.data.spouses?.length
      ? blockShift(down.data.w) : 0
    for (const l of up.links()) {
      // source = the person nearer the focus (lower on screen),
      // target = their ancestor (higher on screen)
      const s = l.source, t = l.target
      const sx = s.data.root ? s.px - focusShift : s.px
      // the key rides with the path: the component keys the drawn
      // elements on it, so a link persists across re-layouts and can
      // morph (or fade in when it is new) instead of teleporting
      links.push({ id: 'u' + s.data.id + '>' + t.data.id,
                   d: elbow(sx, -s.y * ROW_H,
                            t.px, -t.y * ROW_H + CARD_H) })
    }
  }
  if (down) {
    down.each(n => { card(n.px, n.y * ROW_H, n.data, n.data.root) })
    const blockShift = w => w > 1 ? (w * CELL - CARD_W) / 2 : 0
    for (const l of down.links()) {
      const s = l.source, t = l.target
      // land on the blood person's own card, not the couple block's
      // middle - otherwise the line lands ambiguously between the
      // spouses and nobody can tell who married in (the editor's
      // screenshot: Krystyna Celmer and Bogusław Stark)
      const sx = s.px - blockShift(s.data.w)
      const tx2 = t.px - blockShift(t.data.w)
      links.push({ id: 'd' + s.data.id + '>' + t.data.id,
                   d: elbow(sx, s.y * ROW_H + CARD_H,
                            tx2, t.y * ROW_H) })
    }
  }

  const pad = 24
  const baseX = -minX + pad
  const baseY = -minY + pad
  return {
    nodes, links, splices,
    baseX, baseY,
    // the whole chart's bounding box (what "fit" needs) ...
    cx: (minX + maxX) / 2, cy: (minY + maxY) / 2,
    width: maxX - minX + pad * 2,
    height: maxY - minY + pad * 2,
    // ... and the focus person's centre, post-base - what centring on
    // the person needs (the bounding box centre is not the person when
    // one half of the hourglass spreads wider or deeper than the other)
    focusX: focusCX + baseX, focusY: focusCY + baseY,
  }
}
