// The tree layout, pure and testable: no Svelte, no DOM. Reads the app's
// data stores and returns nodes, links and geometry for the SVG layer.
//
// Modes: hourglass (ancestors above, descendants below), pedigree
// (ancestors only), descendants (below only). Couples are paired into one
// row slot; every slot keeps the child it was reached through so the link
// lines can be drawn after all positions are known.

export const CARD_W = 150
export const CARD_H = 44
export const GAP_X = 14
export const CELL = CARD_W + GAP_X
export const ROW_H = 96
export const MAX_UP = 4
export const MAX_DOWN = 3

function fam(db, idf) { return idf ? db.families[idf] || null : null }

function parentsOf(db, pid) {
  const p = db.index[pid]
  const f = p && p.fc && p.fc.length ? fam(db, p.fc[0]) : null
  if (!f) return null
  return { father: f.husb || null, mother: f.wife || null }
}

function marriagesOf(db, pid) {
  const p = db.index[pid]
  if (!p) return []
  return (p.fs || []).map(f => fam(db, f)).filter(Boolean)
    .map(f => ({ spouse: f.husb === pid ? f.wife : f.husb,
                 children: f.chil || [] }))
}

function isCouple(db, a, b) {
  const pa = db.index[a], pb = db.index[b]
  if (!pa || !pb) return false
  const fa = new Set(pa.fs || [])
  return (pb.fs || []).some(f => fa.has(f))
}

// ancestor rows, top generation last. Only real parents become slots; each
// slot keeps the child (on the row below, or the focus for row 0) it was
// reached through, so the link lines can be drawn after positioning.
export function ancestorRows(db, pid) {
  const rows = []
  let current = [pid]
  const seen = new Set([pid])
  for (let g = 0; g < MAX_UP; g++) {
    const next = []
    let any = false
    for (const cid of current) {
      const par = parentsOf(db, cid)
      if (!par || (!par.father && !par.mother)) continue
      any = true
      const pair = []
      for (const key of [par.father, par.mother]) {
        if (key && !seen.has(key)) { seen.add(key); pair.push(key) }
      }
      if (pair.length === 2 && isCouple(db, pair[0], pair[1])) {
        next.push({ id: pair[0], spouse: pair[1], child: cid })
      } else {
        for (const key of pair)
          next.push({ id: key, spouse: null, child: cid })
      }
    }
    if (!next.length) break
    rows.push(next)
    current = next.map(s => s.id)
    if (!any) break
  }
  return rows
}

export function descendantTree(db, pid, depth, seen) {
  if (depth > MAX_DOWN || seen.has(pid)) return null
  seen.add(pid)
  return {
    id: pid,
    marriages: marriagesOf(db, pid).map(m => ({
      spouse: m.spouse,
      children: m.children.map(c => descendantTree(db, c, depth + 1, seen))
        .filter(Boolean),
    })),
  }
}

export function subWidth(node) {
  const fams = node.marriages.filter(m => m.children.length)
  if (!fams.length) return 1
  let w = 0
  for (const m of fams) for (const c of m.children) w += subWidth(c)
  return w
}

export function depthOf(node) {
  let d = 0
  for (const m of node.marriages) for (const c of m.children)
    d = Math.max(d, 1 + depthOf(c))
  return d
}

export function layout(db, id, mode = 'hourglass') {
  if (!id || !db.index || !db.index[id]) return null
  const up = mode !== 'descendants' ? ancestorRows(db, id) : []
  const down = mode !== 'pedigree'
    ? descendantTree(db, id, 0, new Set()) : null

  const nodes = []
  const links = []

  const upWidths = up.map(row =>
    row.reduce((s, slot) => s + (slot.spouse ? 2 : 1), 0))
  const downWidth = down ? subWidth(down) : 1
  const totalW = Math.max(1, ...upWidths, downWidth)

  // ancestors, oldest generation first
  for (let r = up.length - 1; r >= 0; r--) {
    const row = up[r]
    const w = upWidths[r]
    let x = (totalW - w) / 2
    for (const slot of row) {
      nodes.push({ id: slot.id, x: x + 0.5, y: r })
      if (slot.spouse)
        nodes.push({ id: slot.spouse, x: x + 1.5, y: r })
      x += slot.spouse ? 2 : 1
    }
  }
  const focusY = up.length
  nodes.push({ id, x: downWidth / 2, y: focusY, focus: true })

  // descendants; the focus row's own spouses are placed beside the focus
  function place(node, x0, level) {
    const withKids = node.marriages.filter(m => m.children.length)
    if (level > 0) {
      const w = subWidth(node)
      nodes.push({ id: node.id, x: x0 + w / 2, y: focusY + level })
    }
    if (withKids.length >= 1 && withKids[0].spouse) {
      const w = level > 0 ? subWidth(node) : downWidth
      nodes.push({ id: withKids[0].spouse, x: x0 + w / 2 + 0.5,
                   y: focusY + level })
    }
    let cx = x0
    for (const m of withKids) {
      for (const c of m.children) {
        const cw = subWidth(c)
        place(c, cx, level + 1)
        cx += cw
      }
    }
  }
  if (down) place(down, 0, 0)

  // links from ancestor slots down to their children (row r-1, or the
  // focus for row 0)
  const posOf = new Map()
  for (const n of nodes) {
    const key = n.id + '@' + n.y
    if (!posOf.has(key)) posOf.set(key, n)
  }
  for (let r = 0; r < up.length; r++) {
    const targetY = r === 0 ? focusY : r - 1
    for (const slot of up[r]) {
      if (slot.child == null) continue
      const child = posOf.get(slot.child + '@' + targetY)
      if (!child) continue
      const self = posOf.get(slot.id + '@' + r)
      if (!self) continue
      links.push([self.x * CELL + CARD_W / 2, r * ROW_H + CARD_H,
                  child.x * CELL + CARD_W / 2, targetY * ROW_H])
    }
  }
  // links through the descendant tree
  function linkDesc(node, level) {
    const self = posOf.get(node.id + '@' + (focusY + level))
    if (!self) return
    for (const m of node.marriages.filter(m => m.children.length)) {
      for (const c of m.children) {
        const child = posOf.get(c.id + '@' + (focusY + level + 1))
        if (child) {
          links.push([self.x * CELL + CARD_W / 2, self.y * ROW_H + CARD_H,
                      child.x * CELL + CARD_W / 2, child.y * ROW_H])
        }
        linkDesc(c, level + 1)
      }
    }
  }
  if (down) linkDesc(down, 0)

  const rows = Math.max(focusY + 1,
                        focusY + (down ? 1 + depthOf(down) : 0))
  return { nodes, links, rows, totalW, focusY }
}
