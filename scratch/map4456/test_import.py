# -*- coding: utf-8 -*-
"""The Import JSON test: a labels file re-sets the working state.

Covers: the combined export shape ({farms, reds}), the bare [{n,x,y}]
shape, moved farms land, a new farm appears, a red correction lands with
its unsure flag, the import is saved at once (the state files update), it
survives a reload, a malformed file is refused with a message and nothing
changes, and a duplicate farm is refused whole.
"""
import io
import json
import os
import shutil
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


def main():
    backups = {}
    for p in (FARMS, REDS):
        if os.path.isfile(p):
            backups[p] = tempfile.mktemp(suffix='.json')
            shutil.copy(p, backups[p])
    yml_bak = tempfile.mktemp(suffix='.yml')
    import shutil as sh
    sh.copy('maps/pelzucki1896/farms.yml', yml_bak)
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

            # the import file: farm 1 moved to a known spot, farm 25 (one
            # of the unmarked) placed, and a red reading corrected. The red
            # mark used is the first unsure one in the page's own data, and
            # the correction is its own reading minus the doubt brackets -
            # a change, which is what the import has to apply
            target = page.evaluate("""() => {
              const t = redTags.find(t => t.unsure);
              return { x: t.x, y: t.y, raw: t.raw };
            }""")
            red_new = target['raw'].replace('[', '').replace('?', '') \
                .replace(']', '')
            payload = {
                'farms': [{'n': 1, 'x': 11111, 'y': 22222}] + [
                    {'n': m['n'], 'x': m['x'], 'y': m['y']}
                    for m in page.evaluate(
                        "() => marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))")
                    if m['n'] != 1
                ] + [{'n': 25, 'x': 12000, 'y': 3000}],
                'reds': [{'n': red_new, 'x': target['x'],
                          'y': target['y']}]
            }
            tmp = tempfile.mktemp(suffix='.json')
            json.dump(payload, open(tmp, 'w', encoding='utf-8'))

            page.set_input_files('#importfile', tmp)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Imported')",
                timeout=10000)
            check('the import is announced with its counts',
                  '102 farm label(s)' in page.inner_text('#status')
                  and '1 red reading(s) changed' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])
            pos1 = page.evaluate(
                "() => markPos(1)")
            check('the moved farm lands at its file position',
                  pos1 == {'x': 11111, 'y': 22222}, str(pos1))
            check('the new farm appears',
                  page.locator('[data-farm="25"]').count() == 1)
            red = page.evaluate("""(t) => {
              const rec = redTags.find(r => r.x === t.x && r.y === t.y);
              return rec ? { raw: rec.raw, unsure: rec.unsure,
                             span: rec.span.textContent,
                             cls: rec.span.className } : null;
            }""", target)
            check('the red correction lands, unsure cleared',
                  red and red['raw'] == red_new
                  and red['span'] == red_new
                  and red['unsure'] is False and 'unsure' not in red['cls'],
                  str(red))

            # the import saved at once
            d = wait_file(FARMS, lambda x: any(
                xx['n'] == 1 and xx['x'] == 11111 for xx in x))
            check('the import reached the farms file at once',
                  d is not None and len(d) == 102,
                  '%d entries' % len(d) if d else 'no file')
            r = wait_file(REDS, lambda x: any(
                xx['n'] == red_new and xx['x'] == target['x']
                for xx in (x if isinstance(x, list)
                           else x.get('marks', []))))
            check('the red correction reached the reds file at once',
                  r is not None)

            # it survives a reload
            page.reload()
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Restored')",
                timeout=30000)
            check('the import survives a reload',
                  page.evaluate("() => markPos(1)")
                  == {'x': 11111, 'y': 22222}
                  and page.locator('[data-farm="78"]').count() == 1)

            # a malformed file: refused with a message, nothing changes
            bad = tempfile.mktemp(suffix='.json')
            open(bad, 'w', encoding='utf-8').write('{not json')
            page.set_input_files('#importfile', bad)
            time.sleep(0.5)
            check('a malformed file is refused',
                  'not valid JSON' in page.inner_text('#status'))
            check('the state survives the refused file',
                  page.evaluate("() => markPos(1)")
                  == {'x': 11111, 'y': 22222})

            # a duplicate: the same number at the same position twice is
            # refused whole (the same number at DIFFERENT positions is the
            # multi-farmstead feature and is taken)
            dup = tempfile.mktemp(suffix='.json')
            json.dump({'farms': [{'n': 5, 'x': 1, 'y': 2},
                                 {'n': 5, 'x': 1, 'y': 2}]},
                      open(dup, 'w', encoding='utf-8'))
            page.set_input_files('#importfile', dup)
            time.sleep(0.5)
            check('a duplicate label (same place) is refused whole',
                  'twice at' in page.inner_text('#status')
                  and page.evaluate("() => markPos(1)")
                  == {'x': 11111, 'y': 22222})

            # the bare [{n,x,y}] shape also imports (the old export)
            bare = tempfile.mktemp(suffix='.json')
            json.dump([{'n': 1, 'x': 9000, 'y': 5000}] + [
                {'n': m['n'], 'x': m['x'], 'y': m['y']}
                for m in json.load(open(FARMS, encoding='utf-8'))
                if m['n'] not in (1, 25)], open(bare, 'w', encoding='utf-8'))
            page.set_input_files('#importfile', bare)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Imported')",
                timeout=10000)
            check('the bare list shape imports too',
                  page.evaluate("() => markPos(1)")
                  == {'x': 9000, 'y': 5000}
                  and page.locator('[data-farm="25"]').count() == 0,
                  page.inner_text('#status')[:80])

            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
            os.remove(tmp); os.remove(bad); os.remove(dup); os.remove(bare)
    finally:
        for p, b in backups.items():
            shutil.copy(b, p)
        for p in (FARMS, REDS):
            if os.path.isfile(p) and p not in backups:
                os.remove(p)
        shutil.copy(yml_bak, 'maps/pelzucki1896/farms.yml')
        print('working files, farms.yml restored / cleaned')
    failed = [n for n, ok in RESULTS if not ok]
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
