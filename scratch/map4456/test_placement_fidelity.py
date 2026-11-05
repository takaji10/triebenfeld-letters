# -*- coding: utf-8 -*-
"""The placement-fidelity test: is a placed or moved label recorded at
exactly where the editor put it?

For each of several zoom levels:
1. a farm is PLACED by a real click at a probe point; the recorded image
   coordinates must equal the click's own pixel->viewport->image conversion
   (computed independently in the page, from the raw event coordinates);
2. the page is RELOADED and the pill must come back centred on the same
   image coordinates (the roundtrip through the save file);
3. a label is DRAGGED by a fixed screen distance; the recorded movement
   must track the pointer 1:1 at that zoom.
Finally the Export JSON button's real downloaded file must equal the
page's state exactly.
"""
import atexit
import base64
import io
import json
import os
import shutil
import sys
import tempfile
import time

import test_server
from playwright.sync_api import sync_playwright

test_server.start()
atexit.register(test_server.stop)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

URL = test_server.URL
FARMS = test_server.FARMS_STATE
REDS = test_server.REDS_STATE
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('  -- ' + detail if detail else ''))


def launch(pw):
    for channel in ('msedge', 'chrome'):
        try:
            return pw.chromium.launch(channel=channel, headless=True)
        except Exception:
            pass
    return pw.chromium.launch(headless=True)


def main():
    backups = {}
    for p in (FARMS, REDS):
        if os.path.isfile(p):
            backups[p] = tempfile.mktemp(suffix='.json')
            shutil.copy(p, backups[p])
    try:
        for p in (FARMS, REDS):
            if os.path.isfile(p):
                os.remove(p)
        with sync_playwright() as pw:
            browser = launch(pw)
            page = browser.new_page(viewport={'width': 1400, 'height': 900})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:200]))
            page.goto(URL)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Loaded')",
                timeout=30000)

            unmarked = page.evaluate(
                "() => D.rows.map(r => r.n).filter(n => !markPos(n))")
            placed = {}

            def settle():
                # the wheel zoom's spring moves zoom AND centre; the centre
                # keeps gliding briefly after the zoom figure is stable, so
                # both must be still before any conversion means anything
                page.wait_for_function("""() => {
                  const vp = viewer.viewport;
                  const k = vp.getZoom() + ',' + vp.getCenter().x + ',' +
                    vp.getCenter().y;
                  const st = window.__settle = window.__settle || {};
                  if (st.prev === k) { st.n = (st.n || 0) + 1; }
                  else { st.n = 0; }
                  st.prev = k;
                  return st.n >= 4;
                }""", timeout=10000)

            for zi in range(3):
                farm = unmarked[zi]
                # zoom in a bit more each round, and WAIT until the viewport
                # stops moving: a click (or a conversion) taken mid-animation
                # lands on a different map point than the settled one
                for _ in range(zi and 2 or 3):
                    page.mouse.move(700, 420)
                    page.mouse.wheel(0, -300)
                    time.sleep(0.15)
                settle()
                zoom = page.evaluate("() => viewer.viewport.getZoom()")

                # ---- place the farm at a probed clear point -------------
                page.click('#missing .farmrow:has-text("' + str(farm) + '")')
                time.sleep(0.2)
                spot = page.evaluate("""() => {
                  for (let x = 320; x < 1280; x += 24) {
                    for (let y = 220; y < 780; y += 24) {
                      const e = document.elementFromPoint(x, y);
                      if (e && e.closest('#viewer') && !e.closest('.tag')
                          && !e.closest('.red-tag')) return { x, y };
                    }
                  }
                  return null;
                }""")
                # the expected image coordinates, computed the way the page
                # itself must see the click: from the raw screen point
                expect = page.evaluate("""(pt) => {
                  const rect = document.getElementById('viewer')
                    .getBoundingClientRect();
                  const vp = viewer.viewport.pointFromPixel(
                    new OpenSeadragon.Point(pt.x - rect.left,
                                            pt.y - rect.top));
                  const img = viewer.viewport.viewportToImageCoordinates(vp);
                  return { x: Math.round(img.x), y: Math.round(img.y) };
                }""", spot)
                page.mouse.click(spot['x'], spot['y'])
                time.sleep(0.4)
                rec = page.evaluate(
                    "() => markPos(%d)" % farm)
                placed[farm] = rec
                check('zoom %.2f: the placed farm is recorded exactly where '
                      'was clicked' % zoom,
                      rec == expect, 'recorded %s, expected %s' % (rec, expect))

                # ---- the roundtrip through the save file ----------------
                d = json.load(open(FARMS, encoding='utf-8'))
                filed = next((x for x in d if x['n'] == farm), None)
                check('zoom %.2f: the file holds the click position' % zoom,
                      filed == {'n': farm, 'x': expect['x'], 'y': expect['y']},
                      str(filed))
                page.reload()
                page.wait_for_function(
                    "const s = document.getElementById('status').textContent; "
                    "s.includes('Loaded') || s.includes('Restored')",
                    timeout=30000)
                settle()
                back = page.evaluate(
                    "() => markPos(%d)" % farm)
                check('zoom %.2f: after a reload the pill is at the same '
                      'image coordinates' % zoom,
                      back == expect, 'restored %s' % (back,))

                # ---- drag it by a fixed screen distance -----------------
                el = page.locator('[data-farm="' + str(farm) + '"]').first
                b = el.bounding_box()
                cx, cy = b['x'] + b['width'] / 2, b['y'] + b['height'] / 2
                page.mouse.move(cx, cy)
                page.mouse.down()
                for i in range(1, 7):
                    page.mouse.move(cx + 90 * i / 6, cy - 45 * i / 6)
                    time.sleep(0.03)
                page.mouse.up()
                time.sleep(0.4)
                after = page.evaluate(
                    "() => markPos(%d)" % farm)
                # the dragged distance in image units, independently computed
                dist = page.evaluate("""(pt) => {
                  const rect = document.getElementById('viewer')
                    .getBoundingClientRect();
                  const a = viewer.viewport.pointFromPixel(
                    new OpenSeadragon.Point(pt[0] - rect.left,
                                            pt[1] - rect.top));
                  const c = viewer.viewport.pointFromPixel(
                    new OpenSeadragon.Point(pt[0] + 90 - rect.left,
                                            pt[1] - 45 - rect.top));
                  const ia = viewer.viewport.viewportToImageCoordinates(a);
                  const ic = viewer.viewport.viewportToImageCoordinates(c);
                  return { dx: Math.round(ic.x - ia.x),
                           dy: Math.round(ic.y - ia.y) };
                }""", [cx, cy])
                z2 = page.evaluate("() => viewer.viewport.getZoom()")
                check('zoom %.2f: the drag tracks the pointer 1:1 in image '
                      'units' % z2,
                      abs((after['x'] - expect['x']) - dist['dx']) <= 3
                      and abs((after['y'] - expect['y']) - dist['dy']) <= 3,
                      'moved %s, expected %s' % (
                          {'dx': after['x'] - expect['x'],
                           'dy': after['y'] - expect['y']}, dist))

            # ---- the Export button's real download ----------------------
            page.wait_for_function(
                "document.getElementById('saved').textContent.startsWith('saved')"
                + " || document.getElementById('saved').textContent.includes('reds')",
                timeout=15000)
            state = page.evaluate("""() => ({
              farms: marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))
                .sort((a, b) => a.n - b.n),
              reds: {
                marks: redTags.map(t => {
                  const e = { n: t.raw, x: t.x, y: t.y };
                  if (t.id < 0) e.id = t.id;
                  else if (t.ox != null) { e.ox = t.ox; e.oy = t.oy; }
                  return e;
                }).filter(t => t.n)
                  .sort((a, b) => String(a.n).padStart(4, '0')
                    .localeCompare(String(b.n).padStart(4, '0'))),
                deleted: D.redsDeleted || []
              }
            })""")
            with page.expect_download() as dl:
                page.click('#export')
            tmp = tempfile.mktemp(suffix='.json')
            dl.value.save_as(tmp)
            got = json.load(open(tmp, encoding='utf-8'))
            os.remove(tmp)
            check('the exported file equals the page state exactly',
                  got['farms'] == state['farms'] and got['reds'] == state['reds'],
                  '%d farms, %d reds' % (len(got['farms']), len(got['reds'])))
            for farm, rec in placed.items():
                pass   # placed[] is refreshed with the post-drag spot below

            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
    finally:
        for p, b in backups.items():
            shutil.copy(b, p)
        for p in (FARMS, REDS):
            if os.path.isfile(p) and p not in backups:
                os.remove(p)
        print('working files restored / cleaned')
    failed = [n for n, ok in RESULTS if not ok]
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
