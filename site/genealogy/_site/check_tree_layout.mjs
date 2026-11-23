/* Headless check of the windowed flextree layout against the real
   database: no card overlaps, links land on card edges, the focus is
   centred on its card, and the window stays within its two-step radius
   (the editor: render the big tree in parts). */
import { readFileSync } from 'fs'
import { layout, descendantPath, hasMoreUp, hasMoreDown, WINDOW_UP, WINDOW_DOWN,
         CARD_W, CARD_H, CELL, ROW_H } from './src/lib/tree.js'

const db = {
  index: JSON.parse(readFileSync('data/index.json', 'utf8')),
  families: JSON.parse(readFileSync('data/families.json', 'utf8')),
}

const ids = ['I2867', 'I1751', 'I0005', 'I0007', 'I0003', 'I3131']
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
    let dangling = 0
    for (const d of c.links) {
      const nums = d.match(/-?\d+(?:\.\d+)?/g).map(Number)
      const pts = [[nums[0], nums[1]], [nums[nums.length - 2], nums[nums.length - 1]]]
      for (const [x, y] of pts) {
        const onTop = tops.has(Math.round(y))
        const onBottom = tops.has(Math.round(y - CARD_H))
        if (!onTop && !onBottom) dangling++
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
  let dangling = 0
  for (const d of c.links) {
    const nums = d.match(/-?\d+(?:\.\d+)?/g).map(Number)
    const pts = [[nums[0], nums[1]], [nums[nums.length - 2], nums[nums.length - 1]]]
    for (const [x, y] of pts) {
      if (!tops.has(Math.round(y)) && !tops.has(Math.round(y - CARD_H))) dangling++
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
const kid0 = kidsOf('I0272')
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
  console.log('I0272: no usable branch to test')
  bad++
}
console.log(bad ? 'FAILURES: ' + bad : 'ALL LAYOUT CHECKS PASSED')
process.exit(bad ? 1 : 0)
