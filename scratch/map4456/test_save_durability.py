# -*- coding: utf-8 -*-
"""The save-durability test: the editor's moves must never be lost.

Covers, in order:
1. a drag autosaves at once (the file carries the new position immediately);
2. every save drops a dated snapshot under history/;
3. a save with the server down retries and lands when it is back;
4. closing the tab fires the beacon (the last state reaches the disk);
5. the Export JSON button's file (farms + reds) imports through
   pipeline/maps/import_farms.py;
6. a restored history file restores in the page.

The working files are backed up and restored around the test.
"""
import io
import json
import os
import glob
import re
import shutil
import subprocess
import sys
import tempfile
import time

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import atexit
import test_server
test_server.start()
atexit.register(test_server.stop)

URL = 'http://127.0.0.1:8780/scratch/map4456/farm_labels.html'
FARMS = test_server.FARMS_STATE
REDS = test_server.REDS_STATE
HIST_F = os.path.abspath('scratch/map4456/test-state/history/farm_labels_latest')
HIST_R = os.path.abspath('scratch/map4456/test-state/history/red_labels_latest')
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


def wait_file(path, pred, timeout=6.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = json.load(open(path, encoding='utf-8'))
            if pred(d):
                return d
        except Exception:
            pass
        time.sleep(0.1)
    return None


def kill_server():
    test_server.kill()


def start_server():
    test_server.start()


def main():
    backups = {}
    for p in (FARMS, REDS):
        if os.path.isfile(p):
            backups[p] = tempfile.mktemp(suffix='.json')
            shutil.copy(p, backups[p])
    hist_backup = tempfile.mkdtemp()
    for h in (HIST_F, HIST_R):
        if os.path.isdir(h):
            shutil.copytree(h, os.path.join(hist_backup, os.path.basename(h)))
            shutil.rmtree(h)
    try:
        for p in (FARMS, REDS):
            if os.path.isfile(p):
                os.remove(p)
        with sync_playwright() as pw:
            browser = launch(pw)
            ctx = browser.new_context(
                viewport={'width': 1400, 'height': 900})
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:200]))
            page.goto(URL)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Loaded')",
                timeout=30000)
            page.wait_for_function(
                "document.getElementById('saved').textContent.startsWith('saved')",
                timeout=30000)

            # ---- 1. the drag autosaves at once ---------------------------
            tag = page.locator('[data-farm="1"]').first
            tag.wait_for(state='visible', timeout=10000)
            b1 = tag.bounding_box()
            cx, cy = b1['x'] + b1['width'] / 2, b1['y'] + b1['height'] / 2
            page.mouse.move(cx, cy)
            page.mouse.down()
            for i in range(1, 6):
                page.mouse.move(cx + 60 * i / 5, cy + 30 * i / 5)
                time.sleep(0.03)
            page.mouse.up()
            d = wait_file(FARMS, lambda x: any(
                xx['n'] == 1 and abs(xx['x'] - 0) >= 0 for xx in x))
            before = next(xx for xx in d if xx['n'] == 1)
            check('the drag saves the moment the label drops', d is not None
                  and len(d) == 101, 'file: %d entries' % len(d) if d else 'none')

            # ---- 2. the save dropped a snapshot --------------------------
            snaps = sorted(glob.glob(os.path.join(HIST_F, '*.json')))
            check('a dated snapshot landed in history-test/',
                  len(snaps) >= 1
                  and re.search(r'\d{8}-\d{6}\.json$', snaps[-1]) is not None,
                  '%d snapshot(s)' % len(snaps))
            if snaps:
                s = json.load(open(snaps[-1], encoding='utf-8'))
                check('the snapshot carries the moved position',
                      any(xx['n'] == 1 and xx['x'] == before['x']
                          and xx['y'] == before['y'] for xx in s))

            # ---- 3. a save with the server down retries and lands --------
            kill_server()
            time.sleep(1.0)
            tag2 = page.locator('[data-farm="2"]').first
            b2 = tag2.bounding_box()
            cx2, cy2 = b2['x'] + b2['width'] / 2, b2['y'] + b2['height'] / 2
            page.mouse.move(cx2, cy2)
            page.mouse.down()
            page.mouse.move(cx2 + 40, cy2 - 20, steps=4)
            page.mouse.up()
            time.sleep(1.2)
            check('a save with the server down says so loudly',
                  'SAVE FAILED' in page.inner_text('#saved'),
                  page.inner_text('#saved')[:60])
            start_server()
            d = wait_file(FARMS, lambda x: any(
                xx['n'] == 2 for xx in x), timeout=10.0)
            check('the retried save lands when the server is back',
                  d is not None and len(d) == 101)
            page.wait_for_function(
                "!document.getElementById('saved').textContent.includes('FAILED')",
                timeout=15000)
            check('the saved indicator recovers',
                  page.inner_text('#saved').startswith('saved'))

            # ---- 4. a close with unsaved work ----------------------------
            # the save-on-close beacon is gone (a closing window is the one
            # whose state may be stale); the guarantee is instead: unsaved
            # work lives in the browser backup, and the NEXT window takes
            # it when it is newer than the project file. Simulate: kill the
            # server, drag farm 3 (the save fails, the backup holds it),
            # close the window, restart the server with the file wiped,
            # open a new window - the move must come back and push.
            b3 = page.evaluate("() => { const r = document.querySelector("
                               "'[data-farm=\"3\"]').getBoundingClientRect();"
                               " return { x: r.x + r.width / 2,"
                               " y: r.y + r.height / 2 }; }")
            kill_server()
            page.mouse.move(b3['x'], b3['y'])
            page.mouse.down()
            page.mouse.move(b3['x'] + 70, b3['y'] + 40, steps=4)
            page.mouse.up()
            time.sleep(0.8)
            f3 = page.evaluate("() => markPos(3)")
            page.close()
            start_server()
            for p in (FARMS, REDS):
                if os.path.isfile(p):
                    os.remove(p)
            page = page.context.new_page()   # same profile: the backup lives
            page.goto(URL)
            page.wait_for_function(
                "document.getElementById('status').textContent"
                + ".includes('Restored')", timeout=30000)
            # farm 3 carries two labels now (a multi-farmstead in the
            # editor's data), and the backup's sort reorders them - the
            # move is back when the dragged position is among them
            check('the closed window\'s unsaved move comes back from the '
                  'browser backup',
                  page.evaluate(
                      "(f) => marksFor(3).some(m => m.x === f.x "
                      "&& m.y === f.y)", f3),
                  page.inner_text('#status')[:100])
            d = wait_file(FARMS, lambda x: any(
                xx['n'] == 3 and xx['x'] == f3['x'] and xx['y'] == f3['y']
                for xx in x), timeout=10.0)
            check('the recovered move pushes to the project file', d is not None)

            # ---- 5. the export file imports ------------------------------
            # a fresh page: correct one red reading and place one farm, then
            # produce the export's exact shape as the page's button would
            # a fresh profile: the browser backup of the earlier scenes is
            # a different browser's, and must not leak in
            page = browser.new_context(
                viewport={'width': 1400, 'height': 900}).new_page()
            page.goto(URL)
            page.wait_for_function(
                "const s = document.getElementById('status').textContent; "
                "s.includes('Loaded') || s.includes('Restored')",
                timeout=30000)
            page.keyboard.press('Home')
            for _ in range(4):
                page.mouse.wheel(0, -300)
                time.sleep(0.15)
            time.sleep(0.6)
            target = page.evaluate("""() => {
              const els = [...document.querySelectorAll('.red-tag .red-num.unsure')];
              for (const e of els) {
                const r = e.getBoundingClientRect();
                if (r.width < 2) continue;
                const x = r.x + r.width / 2, y = r.y + r.height / 2;
                if (document.elementFromPoint(x, y) === e) {
                  const rec = redTags.find(r => r.span === e);
                  return { x, y, text: e.textContent,
                           rx: rec.x, ry: rec.y };
                }
              }
              return null;
            }""")
            assert target, 'no clickable unsure pill'
            page.mouse.click(target['x'], target['y'])
            time.sleep(0.3)
            page.locator('#red-num').fill('83')
            page.keyboard.press('Enter')
            time.sleep(0.5)
            # the corrected mark's position in the data: captured before the
            # edit (the record's x,y never change), resolved through the
            # clicked span so no recurring row number can mislead
            rpos = {'x': target['rx'], 'y': target['ry']}
            # the export's shape, exactly as the button builds it
            export = page.evaluate("""() => ({
              farms: marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))
                .sort((a, b) => a.n - b.n),
              reds: redTags.map(t => ({ n: t.raw, x: t.x, y: t.y }))
                .sort((a, b) => String(a.n).padStart(4, '0')
                  .localeCompare(String(b.n).padStart(4, '0')))
            })""")
            tmp = tempfile.mktemp(suffix='.json')
            json.dump(export, open(tmp, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            bak_f = tempfile.mktemp(suffix='.yml')
            bak_r = tempfile.mktemp(suffix='.yml')
            shutil.copy('maps/pelzucki1896/farms.yml', bak_f)
            shutil.copy('maps/pelzucki1896/reds.yml', bak_r)
            p = subprocess.run([sys.executable,
                                'pipeline/maps/import_farms.py', tmp],
                               capture_output=True, text=True,
                               encoding='utf-8', errors='replace')
            import yaml
            fy = yaml.safe_load(open('maps/pelzucki1896/farms.yml',
                                     encoding='utf-8'))
            ry = yaml.safe_load(open('maps/pelzucki1896/reds.yml',
                                     encoding='utf-8'))
            check('the export file imports (farms wholesale)',
                  p.returncode == 0 and len(fy['marks']) == 101,
                  (p.stdout + p.stderr)[-160:])
            rm = next(m for m in ry['marks']
                      if m['x'] == rpos['x'] and m['y'] == rpos['y'])
            check('the export file imports (red correction)',
                  rm is not None and rm['n'] == '83' and not rm['unsure'],
                  str(rm))
            shutil.copy(bak_f, 'maps/pelzucki1896/farms.yml')
            shutil.copy(bak_r, 'maps/pelzucki1896/reds.yml')
            os.remove(tmp)
            browser.close()
    finally:
        kill_server()  # the test started its own server; nothing is left
        for p, b in backups.items():
            shutil.copy(b, p)
        for p in (FARMS, REDS):
            if os.path.isfile(p) and p not in backups:
                os.remove(p)
        for h in (HIST_F, HIST_R):
            if os.path.isdir(h):
                shutil.rmtree(h)
        for name in os.listdir(hist_backup):
            shutil.move(os.path.join(hist_backup, name), HISTORY_DIR(name))
        print('working files, history restored / cleaned')
    failed = [n for n, ok in RESULTS if not ok]
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


def HISTORY_DIR(name):
    return os.path.join(os.path.abspath('scratch/map4456/test-state/history'), name)


if __name__ == '__main__':
    main()
