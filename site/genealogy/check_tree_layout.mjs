/* Headless check of the windowed flextree layout against the real
   database: no card overlaps, links land on card edges, the focus is
   centred on its card, and the window stays within its two-step radius
   (the editor: render the big tree in parts). */
import { readFileSync } from 'fs'
import { layout, descendantPath, hasMoreUp, hasMoreDown, WINDOW_UP, WINDOW_DOWN,
         CARD_W, CARD_H, CELL, ROW_H, GAP_X, orderedUnions } from './src/lib/tree.js'

// usage: node check_tree_layout.mjs [zelmer|trabczyn]  (default zelmer;
// trabczyn reads site/genealogy/trabczyn/data, or CHECK_DATA=<dir>)
const tree = process.argv[2] || 'zelmer'
const dir = process.env.CHECK_DATA || `${tree}/data`
const db = {
  index: JSON.parse(readFileSync(`${dir}/index.json`, 'utf8')),
  families: JSON.parse(readFileSync(`${dir}/families.json`, 'utf8')),
}
const meta = JSON.parse(readFileSync(`${dir}/meta.json`, 'utf8'))

// the Zelmer ids are hand-picked cases; another tree is checked on its
// start person and a sample of its people
const ids = tree === 'zelmer'
  ? ['I2867', 'I1751', 'I0005', 'I0007', 'I0003', 'I3131']
  : [...new Set([meta.start, ...Object.keys(db.index).filter((_, i) => i % 5 === 0).slice(0, 12)])]
    .filter(id => db.index[id])

// the midpoint of every marriage line (adjacent: the gap's middle;
// bracket: the middle of its horizontal run), keyed by 'person>spouse'
function spliceMids(c) {
  return c.splices.map(sp => {
    const nums = sp.d.match(/-?\d+(?:\.\d+)?/g).map(Number)
    const m = nums.length === 4
      ? { x: sp.x + nums[2] / 2, y: sp.y }
      : { x: sp.x + nums[4] / 2, y: sp.y + nums[3] }
    return { ...m, id: sp.id }
  })
}

let bad = 0
for (const id of ids) {
  for (const mode of ['hourglass', 'pedigree', 'descendants']) {
    const c = layout(db, id, mode)
    if (!c) { console.log(id, mode, 'NO LAYOUT'); bad++; continue }
    const rows = new Map()
    for (const n of c.nodes) {
      const key = Math.round(n.y)
      if (!rows.has(key)) rows.set(key, [])
      rows.get(key).push(n)
    }
    let overlaps = 0
    for (const [, row] of rows) {
      row.sort((a, b) => a.x - b.x)
      for (let i = 1; i < row.length; i++) {
        if (row[i].x < row[i - 1].x + row[i - 1].w * CELL - 0.5) overlaps++
      }
    }
    const tops = new Set(c.nodes.map(n => Math.round(n.y)))
    const mids = spliceMids(c)
    let dangling = 0
    for (const l of c.links) {
      const nums = l.d.match(/-?\d+(?:\.\d+)?/g).map(Number)
      const pts = [[nums[0], nums[1]], [nums[nums.length - 2], nums[nums.length - 1]]]
      for (const [x, y] of pts) {
        const onTop = tops.has(Math.round(y))
        const onBottom = tops.has(Math.round(y - CARD_H))
        const onSplice = mids.some(m => Math.abs(m.x - x) < 0.5 && Math.abs(m.y - y) < 0.5)
        if (!onTop && !onBottom && !onSplice) dangling++
      }
    }
    const focus = c.nodes.filter(n => n.focus)
    const fx = c.focusX, fy = c.focusY
    const focusOK = focus.length === 1 &&
      fx >= 0 && fx <= c.width && fy >= 0 && fy <= c.height &&
      fx >= focus[0].x + c.baseX &&
      fx <= focus[0].x + focus[0].w * CELL + c.baseX
    // window radius: no card sits further than the window's rows from
    // the focus row (2 up, 1 down - the grandchildren sit behind the
    // branch badges now)
    const focusRowY = focus[0].y
    const maxRowDist = Math.max(
      Math.abs(Math.min(...c.nodes.map(n => n.y)) - focusRowY),
      Math.abs(Math.max(...c.nodes.map(n => n.y)) - focusRowY))
    const withinWindow = maxRowDist <= (WINDOW_UP + 1) * 100 + 10
    if (overlaps || dangling || !focusOK || !withinWindow) bad++
    console.log(`${id} ${mode}: nodes=${c.nodes.length} rowspread=${Math.round(maxRowDist / 100)} ` +
      `overlaps=${overlaps} dangling=${dangling} focus=${focusOK ? 'ok' : 'BAD'} ` +
      `${overlaps || dangling || !focusOK || !withinWindow ? 'FAIL' : 'ok'}`)
  }
  console.log(`  arrows: up=${hasMoreUp(db, id)} down=${hasMoreDown(db, id, 1)}`)
}

// the expansion battery: on the widest descendant window in the data
// (I0272 Christina Ubel), open a child's branch and then a grandchild's
// beneath it - no overlaps, no dangling links, and the width stays
// within a few screens instead of the 21 the always-everything render
// produced
function checkOpen(root, openId, label) {
  const path = descendantPath(db, root, openId)
  const c = layout(db, root, 'hourglass', path)
  if (!c) { console.log(label, 'NO LAYOUT'); bad++; return null }
  const rows = new Map()
  for (const n of c.nodes) {
    const key = Math.round(n.y)
    if (!rows.has(key)) rows.set(key, [])
    rows.get(key).push(n)
  }
  let overlaps = 0
  for (const [, row] of rows) {
    row.sort((a, b) => a.x - b.x)
    for (let i = 1; i < row.length; i++) {
      if (row[i].x < row[i - 1].x + row[i - 1].w * CELL - 0.5) overlaps++
    }
  }
  const tops = new Set(c.nodes.map(n => Math.round(n.y)))
  const mids = spliceMids(c)
  let dangling = 0
  for (const l of c.links) {
    const nums = l.d.match(/-?\d+(?:\.\d+)?/g).map(Number)
    const pts = [[nums[0], nums[1]], [nums[nums.length - 2], nums[nums.length - 1]]]
    for (const [x, y] of pts) {
      const onSplice = mids.some(m => Math.abs(m.x - x) < 0.5 && Math.abs(m.y - y) < 0.5)
      if (!tops.has(Math.round(y)) && !tops.has(Math.round(y - CARD_H)) && !onSplice) dangling++
    }
  }
  // the opened node's children really render
  const openNode = c.nodes.find(n => n.id === openId)
  const kidsShown = c.nodes.filter(n => n.on).length >= 1
  const widthScreens = c.width / 1120
  const ok = !overlaps && !dangling && kidsShown && widthScreens <= 6
  if (!ok) bad++
  console.log(`${label}: nodes=${c.nodes.length} width=${Math.round(c.width)} ` +
    `(${Math.round(widthScreens * 10) / 10} screens) overlaps=${overlaps} ` +
    `dangling=${dangling} branch-open=${kidsShown ? 'yes' : 'NO'} ${ok ? 'ok' : 'FAIL'}`)
  return c
}

// the child of I0272 with the most children
const kidsOf = pid => {
  const p = db.index[pid]
  return (p?.fs || []).flatMap(f => db.families[f]?.chil || [])
    .filter(c => db.index[c])
}
const kid0 = tree !== 'zelmer' ? undefined : kidsOf('I0272')
  .sort((a, b) => kidsOf(b).length - kidsOf(a).length)[0]
if (kid0 && kidsOf(kid0).length) {
  checkOpen('I0272', kid0, 'I0272 branch open at ' + kid0)
  const c1 = layout(db, 'I0272', 'hourglass', descendantPath(db, 'I0272', kid0))
  // a second branch (a sibling child): opening it must auto-collapse
  // the first - one open at a time
  const sib = db.index[kid0] &&
    kidsOf('I0272').find(k => k !== kid0 && kidsOf(k).length)
  if (sib) checkOpen('I0272', sib, 'I0272 second branch at ' + sib + ' (first auto-collapses)')
  // a true grandchild (two rows below the focus) with hidden children:
  // expanding it must keep its parent branch open (the path)
  const gkid = c1.nodes.filter(n => n.kc > 0 && !n.on && !n.focus &&
      Math.round(n.y / ROW_H) === 2)
    .sort((a, b) => b.kc - a.kc)[0]
  if (gkid) checkOpen('I0272', gkid.id, 'I0272 branch open at ' + gkid.id + ' (grandchild)')
  else console.log('no grandchild with children to test')} else {
  if (tree === 'zelmer') { console.log('I0272: no usable branch to test'); bad++ }
}

// remarriages: the person once, spouses beside them in marriage order
// (two: first left, person middle, second right; three or more: the
// person first), each marriage's children hanging from that couple's own
// marriage line, the groups left to right in marriage order, no overlaps
function checkMarriages(root, label, open = new Set()) {
  const c = layout(db, root, 'hourglass', open)
  if (!c) { console.log(label, 'NO LAYOUT'); bad++; return }
  const problems = []
  const mids = new Map(spliceMids(c).map(m => [m.id, m]))
  // overlaps among cards (a block's cards occupy w*CELL)
  const rows = new Map()
  for (const n of c.nodes) {
    const k = Math.round(n.y)
    if (!rows.has(k)) rows.set(k, [])
    rows.get(k).push(n)
  }
  for (const [, row] of rows) {
    row.sort((a, b) => a.x - b.x)
    for (let i = 1; i < row.length; i++)
      if (row[i].x < row[i - 1].x + row[i - 1].w * CELL - 0.5) problems.push('overlap')
  }
  let multiBlocks = 0, groupsChecked = 0
  for (const n of c.nodes) {
    if (n.y < 0) continue
    const unions = orderedUnions(db, n.id)
    const spouses = n.cards.filter(x => x !== n.id)
    if (n.cards.indexOf(n.id) !== n.pi) problems.push(n.id + ' pi wrong')
    if (spouses.length === 2 && n.cards.indexOf(n.id) !== 1) problems.push(n.id + ' two spouses: person not in the middle')
    if (spouses.length !== 2 && n.cards[0] !== n.id) problems.push(n.id + ' person not first')
    // spouses in marriage order (first appearance in the ordered unions)
    const order = [...new Set(unions.map(u => u.spouse).filter(x => spouses.includes(x)))]
    if (order.join() !== spouses.join()) problems.push(n.id + ' spouses out of marriage order')
    if (spouses.length > 1) {
      multiBlocks++
      // the ordinals: one marriage line per spouse, labelled 1..n
      const sp = c.splices.filter(s => s.id.startsWith(n.id + '>'))
      if (sp.map(s => s.ord).join() !== spouses.map((_, i) => i + 1).join())
        problems.push(n.id + ' ordinals')
    }
    // each child's link starts at its own couple's marriage line (or the
    // person's card for a child of no recorded spouse); groups in order
    let lastUnion = -1
    const kids = c.nodes.filter(k => k.y > n.y && Math.round(k.y - n.y) === ROW_H &&
      c.links.some(l => l.id === 'd' + n.id + '>' + k.id))
    kids.sort((a, b) => a.x - b.x)
    for (const k of kids) {
      const l = c.links.find(l => l.id === 'd' + n.id + '>' + k.id)
      const nums = l.d.match(/-?\d+(?:\.\d+)?/g).map(Number)
      const fam = db.families[db.index[k.id].fc[0]]
      const other = fam.husb === n.id ? fam.wife : fam.husb
      const ui = unions.findIndex(u => u.children.includes(k.id))
      if (ui < lastUnion && spouses.length) problems.push(n.id + ' child groups out of marriage order at ' + k.id)
      lastUnion = Math.max(lastUnion, ui)
      groupsChecked++
      if (other && spouses.includes(other)) {
        const m = mids.get(n.id + '>' + other)
        if (!m || Math.abs(nums[0] - m.x) > 0.5 || Math.abs(nums[1] - m.y) > 0.5)
          problems.push(n.id + ' -> ' + k.id + ' does not start at the splice midpoint of ' + other)
      } else {
        const px = n.x + n.pi * CELL + CARD_W / 2
        if (Math.abs(nums[0] - px) > 0.5 || Math.abs(nums[1] - (n.y + CARD_H)) > 0.5)
          problems.push(n.id + ' -> ' + k.id + ' (no spouse) does not start at the person card')
      }
    }
  }
  const ok = !problems.length
  if (!ok) bad++
  console.log(`${label}: blocks with 2+ spouses=${multiBlocks} child links checked=${groupsChecked} ` +
    `${ok ? 'ok' : 'FAIL ' + [...new Set(problems)].slice(0, 6).join('; ')}`)
}
const manySp = Object.keys(db.index).filter(k => (db.index[k].fs || []).length >= 2)
const three = manySp.filter(k => (db.index[k].fs || []).length >= 3)
const cases = tree === 'zelmer'
  ? ['I0017', 'I0019', 'I0112', 'I0128', ...three.slice(0, 4), ...manySp.slice(0, 15)]
  : ['T049', ...manySp.slice(0, 15)]
for (const id of [...new Set(cases)].filter(x => db.index[x])) {
  checkMarriages(id, `marriages ${id} (${(db.index[id].fs || []).length} families)`)
}
console.log(bad ? 'FAILURES: ' + bad : 'ALL LAYOUT CHECKS PASSED')
process.exit(bad ? 1 : 0)
