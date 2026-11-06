/* Headless check of the windowed flextree layout against the real
   database: no card overlaps, links land on card edges, the focus is
   centred on its card, and the window stays within its two-step radius
   (the editor: render the big tree in parts). */
import { readFileSync } from 'fs'
import { layout, hasMoreUp, hasMoreDown, WINDOW_UP, WINDOW_DOWN,
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
    // the focus row
    const focusRowY = focus[0].y
    const maxRowDist = Math.max(
      Math.abs(Math.min(...c.nodes.map(n => n.y)) - focusRowY),
      Math.abs(Math.max(...c.nodes.map(n => n.y)) - focusRowY))
    const withinWindow = maxRowDist <= (WINDOW_UP + WINDOW_DOWN + 1) * 100 + 10
    if (overlaps || dangling || !focusOK || !withinWindow) bad++
    console.log(`${id} ${mode}: nodes=${c.nodes.length} rowspread=${Math.round(maxRowDist / 100)} ` +
      `overlaps=${overlaps} dangling=${dangling} focus=${focusOK ? 'ok' : 'BAD'} ` +
      `${overlaps || dangling || !focusOK || !withinWindow ? 'FAIL' : 'ok'}`)
  }
  console.log(`  arrows: up=${hasMoreUp(db, id)} down=${hasMoreDown(db, id)}`)
}
console.log(bad ? 'FAILURES: ' + bad : 'ALL LAYOUT CHECKS PASSED')
process.exit(bad ? 1 : 0)
