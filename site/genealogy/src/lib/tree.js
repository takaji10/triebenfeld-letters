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
export const MAX_UP = 5
export const MAX_DOWN = 4

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
function upTree(db, pid, depth, seen) {
  seen.add(pid)
  const children = []
  if (depth < MAX_UP) {
    for (const par of parentsOf(db, pid)) {
      if (!db.index[par] || seen.has(par)) continue
      const t = upTree(db, par, depth + 1, seen)
      if (t) children.push(t)
    }
  }
  return { id: pid, spouses: [], w: 1, root: depth === 0, children }
}

// The descendant half: the person, the spouse their children share
// beside them (a card each), the children beneath the couple.
function downTree(db, pid, depth, seen) {
  seen.add(pid)
  const spouses = []
  const children = []
  for (const u of unionsOf(db, pid)) {
    if (u.spouse && u.spouse !== pid && db.index[u.spouse] &&
        !spouses.includes(u.spouse) &&
        (u.children.length || depth === 0)) {
      spouses.push(u.spouse)
    }
    if (depth < MAX_DOWN) {
      for (const c of u.children) {
        if (!db.index[c] || seen.has(c)) continue
        const t = downTree(db, c, depth + 1, seen)
        if (t) children.push(t)
      }
    }
  }
  return { id: pid, spouses, w: spouses.length ? 2 : 1,
           root: depth === 0, children }
}

function elbow(x1, y1, x2, y2) {
  const my = (y1 + y2) / 2
  return `M ${x1} ${y1} L ${x1} ${my} L ${x2} ${my} L ${x2} ${y2}`
}

export function layout(db, id, mode = 'hourglass') {
  if (!id || !db.index || !db.index[id]) return null
  const wantUp = mode !== 'descendants'
  const wantDown = mode !== 'pedigree'

  const up = wantUp ? runTree(upTree(db, id, 0, new Set())) : null
  const down = wantDown ? runTree(downTree(db, id, 0, new Set())) : null

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
                 spouse: data.spouses?.[0] || null, focus: isFocus })
    if (isFocus) {
      focusCX = blockLeft + w * CELL / 2
      focusCY = py + CARD_H / 2
    }
    if (data.spouses?.length) {
      splices.push([blockLeft + CARD_W, py + CARD_H / 2,
                    blockLeft + CELL, py + CARD_H / 2])
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
    for (const l of up.links()) {
      // source = the person nearer the focus (lower on screen),
      // target = their ancestor (higher on screen)
      const s = l.source, t = l.target
      links.push(elbow(s.px, -s.y * ROW_H,
                       t.px, -t.y * ROW_H + CARD_H))
    }
  }
  if (down) {
    down.each(n => { card(n.px, n.y * ROW_H, n.data, n.data.root) })
    for (const l of down.links()) {
      const s = l.source, t = l.target
      links.push(elbow(s.px, s.y * ROW_H + CARD_H,
                       t.px, t.y * ROW_H))
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
