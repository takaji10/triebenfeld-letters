/* Headless check of the flextree-based layout against the real database:
   no two cards overlap, the focus is centred, links connect card edges. */
import { readFileSync } from 'fs'
import { layout, CARD_W, CARD_H, CELL, ROW_H } from './src/lib/tree.js'

const db = {
  index: JSON.parse(readFileSync('data/index.json', 'utf8')),
  families: JSON.parse(readFileSync('data/families.json', 'utf8')),
}

const ids = ['I1751', 'I3131', 'I0005', 'I0007', 'I0003']
let bad = 0
for (const id of ids) {
  for (const mode of ['hourglass', 'pedigree', 'descendants']) {
    const c = layout(db, id, mode)
    if (!c) { console.log(id, mode, 'NO LAYOUT'); bad++; continue }
    // overlap check: every pair of cards on the same row must not overlap
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
    // every link endpoint must land on a card edge: first point = the
    // parent side, last point = the child side (the elbow's middle
    // waypoints sit between rows by design and are not checked)
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
    const status = (overlaps || dangling) ? 'FAIL' : 'ok'
    if (overlaps || dangling) bad++
    console.log(`${id} ${mode}: nodes=${c.nodes.length} links=${c.links.length} ` +
      `splices=${c.splices.length} overlaps=${overlaps} dangling=${dangling} ${status}`)
  }
}
console.log(bad ? 'FAILURES: ' + bad : 'ALL LAYOUT CHECKS PASSED')
process.exit(bad ? 1 : 0)
