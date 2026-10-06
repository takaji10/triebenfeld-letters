# -*- coding: utf-8 -*-
"""Shared steps for a holding that is a few leaves of a bound court book.

Used by the scripts in units/<slug>/intake/ of the Poznań court books (the
Prusimski era, docs/PRUSIMSKI_ERA_PLAN.md). Nothing about any one holding is
in here: each holding's own script says which scans it has, where each fold
is, which halves are pages, and what was corrected.

- cut():        cut each opening at its fold into two whole pages. Each page
                keeps OVERLAP pixels beyond the fold, so a line that runs into
                the gutter stays whole. A scan that is one page is copied.
- fold_sheet(): the page on which the editor sees every fold, moves the
                ones that are wrong and saves them, before a holding is
                published (the editor's rule, 2026-10-06). placed() and
                take_folds() bring the saved folds back.
- correct():    apply readings corrected against the scan to the page files
                and corpus.txt, each demanded exactly once on its page, and
                log them in transcription_decisions.csv.

The fold is the thin dark line of the gutter, not the darkest band near the
middle of the opening: find_fold() looks for it, and every fold is then
looked at on a strip before it is written into the holding's script.
"""
import csv
import hashlib
import html
import io
import os

OVERLAP = 30


def plain(text):
    """Markdown off: the escapes before brackets and stops, and asterisks."""
    import re
    text = re.sub(r'\\([\[\]\.\-\*_#~()>])', r'\1', text)
    return text.replace('*', '')


def read_leaves(path):
    """The editor's text file, cut at its leaf marks ("[653v]" on a line of its own).

    Returns (lines before the first mark, [(leaf, [paragraphs])]), Markdown
    taken off, each paragraph on one line. Nothing is dropped: the caller
    says what it does with every part.
    """
    import re
    s = io.open(path, encoding='utf-8-sig').read().replace('\r\n', '\n')
    parts = re.split(r'(?m)^\\?\[(\d+v?)\\?\]\s*$', s)

    def paras(t):
        return [re.sub(r'\s+', ' ', plain(l)).strip() for l in t.split('\n') if l.strip()]
    return paras(parts[0]), [(leaf, paras(t)) for leaf, t in zip(parts[1::2], parts[2::2])]


def read_english(path, drop_notes=()):
    """The editor's English file, cut at its leaf marks, in the edition's forms.

    Returns [(leaf, [paragraphs])]. The file's own heading before the first
    leaf mark, and its "Translator's Notes" and "Glossary" sections at the
    end, are the editor's apparatus and are left out. A footnote becomes
    "[Translator's note: ...]" after the paragraph it belongs to, unless its
    number is in `drop_notes` (the holding's script says why). A heading
    becomes a line in square brackets; "word[?]" becomes "[uncertain: word]".
    """
    import re
    s = io.open(path, encoding='utf-8-sig').read().replace('\r\n', '\n')
    notes = {}
    for m in re.finditer(r'(?m)^\[\^(\d+)\]:\s*(.*)$', s):
        notes[m.group(1)] = re.sub(r'\s+', ' ', plain(m.group(2)).replace('`', '"')).strip()
    s = re.sub(r'(?m)^\[\^\d+\]:.*\n?', '', s)
    cut = re.search(r"(?m)^#+\s*\**\s*(Translator's Notes|Translator’s Notes|Glossary)", s)
    if cut:
        s = s[:cut.start()]
    parts = re.split(r'(?m)^\\?\[(\d+v?)\\?\]\s*$', s)
    out = []
    for leaf, text in zip(parts[1::2], parts[2::2]):
        paras = []
        for raw in text.split('\n'):
            line = raw.rstrip()
            if not line.strip() or re.fullmatch(r'-{3,}', line.strip()):
                continue
            m = re.match(r'^(#+)\s*(.*)$', line)
            if m:
                paras.append('[' + re.sub(r'[*_]', '', m.group(2)).strip() + ']')
                continue
            line = re.sub(r'^\s*\*\s+', '', line)
            line = plain(line).replace('[[', '[').replace(']]', ']')
            line = re.sub(r'\s*\[see Glossary\]', '', line)
            line = re.sub(r'([^\s\[\]]+)\[\?\]', lambda k: '[uncertain: %s]' % k.group(1), line)
            line = re.sub(r'\[([^\[\]]{1,60})\?\]', lambda k: '[uncertain: %s]' % k.group(1).strip(), line)
            # "[T.N.12]": the editor's other way of marking a note; the notes
            # themselves are in the section that is cut off above
            line = re.sub(r'\s*\[T\.N\.\d+\]', '', line)
            refs = re.findall(r'\[\^(\d+)\]', line)
            line = re.sub(r'\s+', ' ', re.sub(r'\[\^\d+\]', '', line)).strip()
            if line:
                paras.append(line)
            for r in refs:
                if r not in drop_notes:
                    paras.append("[Translator's note: %s]" % notes[r])
        out.append((leaf, paras))
    return out


def fix_english(pages, fixes):
    """pages: {page id: [paragraphs]}; fixes: [(old, new, why)], each `old` exactly once in the whole text."""
    for old, new, why in fixes:
        hits = [pid for pid, paras in pages.items() if old in '\n\n'.join(paras)]
        assert len(hits) == 1, ('English fix found on %d pages: %s' % (len(hits), old[:60]))
        joined = '\n\n'.join(pages[hits[0]])
        assert joined.count(old) == 1, old[:60]
        pages[hits[0]] = [p for p in joined.replace(old, new).split('\n\n') if p.strip()]
    return pages


def write_doc_yml(path, page_texts):
    """One doc<N>.yml in the shape translate.py saves: a list of the pages' English, in order."""
    import re
    import yaml
    doc = {'pages': []}
    for n, en in enumerate(page_texts, 1):
        doc['pages'].append({'page': n, 'confidence': 'high',
                             'marker_count': len(re.findall(r'\[(?:uncertain: |illegible|text lost)', en)),
                             'en': en, 'names': [], 'numbers': [], 'flagged': []})
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=100)
    print('wrote', os.path.basename(path), 'with', len(page_texts), 'page(s)')


def find_fold(path, lo=0.40, hi=0.60):
    """x of the gutter: a line 5 px wide, darker than the paper 25 to 60 px either side."""
    from PIL import Image
    g = Image.open(path).convert('L')
    W, H = g.size
    row = list(g.crop((0, int(H * 0.15), W, int(H * 0.85))).resize((W, 1), Image.BOX).getdata())
    best, bx = None, None
    for x in range(int(W * lo), int(W * hi)):
        line = sum(row[x - 2:x + 3]) / 5
        side = (sum(row[x - 60:x - 25]) + sum(row[x + 25:x + 60])) / 70
        if best is None or side - line > best:
            best, bx = side - line, x
    return bx


def cut(raw, scans, skip=()):
    """scans: [(file name, fold x or None, left page id, right page id)].

    A scan with fold None is one page; its id is the third field. Pages go to
    raw/processed/; halves named in `skip` go to raw/processed/_not_staged/.
    """
    from PIL import Image
    processed = os.path.join(raw, 'processed')
    apart = os.path.join(processed, '_not_staged')
    os.makedirs(apart, exist_ok=True)
    n = 0
    for name, fold, left, right in scans:
        im = Image.open(os.path.join(raw, name)).convert('RGB')
        if fold is None:
            parts = [(left, (0, 0, im.width, im.height))]
        else:
            parts = [(left, (0, 0, fold + OVERLAP, im.height)), (right, (fold - OVERLAP, 0, im.width, im.height))]
        for pid, box in parts:
            folder = apart if pid in skip else processed
            im.crop(box).save(os.path.join(folder, pid + '.jpg'), quality=92)
            n += 1
    print('cut', n, 'page images into', processed)


def placed(here, scans):
    """`scans` with the folds the editor placed, if they saved any (folds.json beside the holding's script).

    The fold page offers "folds_<slug>.json"; `python pipeline/intake/courtbook.py
    folds <slug> <that file>` copies it to units/<slug>/intake/folds.json and
    cuts the pages again. The numbers in the script stay as the first proposal.
    """
    import json
    p = os.path.join(here, 'folds.json')
    if not os.path.isfile(p):
        return scans
    mine = json.load(io.open(p, encoding='utf-8'))
    return [(name, (int(mine[name]) if fold is not None and name in mine else fold), left, right)
            for name, fold, left, right in scans]


STRIP_HALF = 650      # the fold page shows this many pixels either side of the proposed fold
STRIP_SCALE = 0.5

_FOLD_PAGE = r"""<!doctype html><html lang="en"><meta charset="utf-8"><title>Folds: __REF__</title>
<style>
body{font:16px/1.5 Georgia,serif;margin:0;background:#fbfaf7;color:#222}
header{position:sticky;top:0;z-index:5;background:#222;color:#eee;padding:.5em 1em;display:flex;gap:1em;align-items:center;flex-wrap:wrap}
header button{font:inherit;padding:.3em .9em;cursor:pointer}
main{max-width:1250px;margin:1em auto;padding:0 16px}
section{margin:2.2em 0;padding-top:.6em;border-top:1px solid #ccc}
h2{margin:0 0 .2em;font-size:1.1em}
.row{display:flex;gap:18px;align-items:flex-start}
.whole{width:420px;flex:none}.whole img{width:100%;border:1px solid #ccc}
.strip{position:relative;flex:none;cursor:crosshair;user-select:none;border:1px solid #999;overflow:hidden}
.strip img{display:block;pointer-events:none}
.line{position:absolute;top:0;bottom:0;width:2px;background:#f00;pointer-events:none}
.band{position:absolute;top:0;bottom:0;background:rgba(255,0,0,.13);pointer-events:none}
.first{position:absolute;top:0;bottom:0;width:1px;background:#06c;opacity:.7;pointer-events:none}
.tools{margin:.3em 0}.tools button{font:inherit;padding:.1em .7em;cursor:pointer}
.moved{color:#b3261e;font-weight:bold}
textarea{width:100%;height:7em;display:none;margin-top:.5em}
</style>
<header><b>Folds: __REF__</b><span id="count"></span>
<button id="save">Save my folds</button><button id="resetall">Put all back</button></header>
<main>
<p>Each opening is cut at the red line into two pages. Each page also keeps the pink strip beyond the line, so writing
inside the pink strip is on both pages and is not lost. <b>To move a line, click in the wide picture where the fold
is</b> (or drag; the arrow buttons move it a little). The thin blue line is where I first put it. Your changes are
kept in this browser as you go. When you are done, press <b>Save my folds</b>: the browser saves a small file,
<code>folds___SLUG__.json</code>, into your Downloads folder. Tell me, and I cut the pages again from it.</p>
__NOTE__
<textarea id="out" readonly></textarea>
<div id="list"></div>
</main>
<script>
const SLUG = "__SLUG__", OVERLAP = __OVERLAP__, SCALE = __SCALE__;
const ITEMS = __ITEMS__;
const KEY = 'folds_' + SLUG;
let mine = {};
try { mine = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
const list = document.getElementById('list');
function cur(it) { return (it.name in mine) ? mine[it.name] : it.fold; }
function draw(it) {
  const x = (cur(it) - it.x0) * SCALE;
  it.line.style.left = (x - 1) + 'px';
  it.band.style.left = (x - OVERLAP * SCALE) + 'px';
  it.band.style.width = (2 * OVERLAP * SCALE) + 'px';
  const d = cur(it) - it.fold;
  it.say.textContent = d ? ('moved ' + Math.abs(d) + ' pixels to the ' + (d > 0 ? 'right' : 'left')) : 'not moved';
  it.say.className = d ? 'moved' : '';
  const n = ITEMS.filter(i => i.fold !== null && cur(i) !== i.fold).length;
  document.getElementById('count').textContent = n + ' of ' + ITEMS.filter(i => i.fold !== null).length + ' moved';
}
function set(it, v) {
  v = Math.round(Math.max(it.x0 + 5, Math.min(it.x0 + it.w / SCALE - 5, v)));
  if (v === it.fold) delete mine[it.name]; else mine[it.name] = v;
  try { localStorage.setItem(KEY, JSON.stringify(mine)); } catch (e) {}
  draw(it);
}
for (const it of ITEMS) {
  const sec = document.createElement('section');
  sec.innerHTML = '<h2>' + it.name + '</h2><p>' + it.text + '</p>';
  const row = document.createElement('div'); row.className = 'row';
  if (it.fold === null) {
    row.innerHTML = '<div class="whole" style="width:700px"><img loading="lazy" src="' + it.whole + '"></div>';
    sec.appendChild(row); list.appendChild(sec); continue;
  }
  const strip = document.createElement('div'); strip.className = 'strip';
  strip.style.width = it.w + 'px'; strip.style.height = it.h + 'px';
  strip.innerHTML = '<img loading="lazy" width="' + it.w + '" height="' + it.h + '" src="' + it.strip + '">' +
    '<div class="first" style="left:' + ((it.fold - it.x0) * SCALE) + 'px"></div><div class="band"></div><div class="line"></div>';
  it.line = strip.querySelector('.line'); it.band = strip.querySelector('.band');
  const at = e => set(it, it.x0 + (e.clientX - strip.getBoundingClientRect().left) / SCALE);
  let down = false;
  strip.addEventListener('pointerdown', e => { down = true; strip.setPointerCapture(e.pointerId); at(e); });
  strip.addEventListener('pointermove', e => { if (down) at(e); });
  strip.addEventListener('pointerup', e => { down = false; });
  const side = document.createElement('div');
  side.innerHTML = '<div class="tools"><button data-d="-4">&#9664; left</button> <button data-d="4">right &#9654;</button> ' +
    '<button data-d="0">put back</button></div><div class="say"></div>' +
    '<div class="whole" style="margin-top:1em"><img loading="lazy" src="' + it.whole + '"></div>';
  it.say = side.querySelector('.say');
  side.querySelectorAll('button').forEach(bt => bt.addEventListener('click', () => {
    const d = +bt.dataset.d; set(it, d ? cur(it) + d : it.fold); }));
  row.appendChild(strip); row.appendChild(side); sec.appendChild(row); list.appendChild(sec);
  draw(it);
}
document.getElementById('resetall').addEventListener('click', () => {
  if (!confirm('Put every line back where it was first?')) return;
  mine = {}; try { localStorage.removeItem(KEY); } catch (e) {}
  ITEMS.forEach(it => { if (it.fold !== null) draw(it); });
});
document.getElementById('save').addEventListener('click', async () => {
  const all = {}; ITEMS.forEach(it => { if (it.fold !== null) all[it.name] = cur(it); });
  const text = JSON.stringify(all, null, 1);
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], {type: 'application/json'}));
  a.download = 'folds_' + SLUG + '.json'; a.click();
  const out = document.getElementById('out'); out.value = text; out.style.display = 'block';
  try { await navigator.clipboard.writeText(text); } catch (e) {}
});
</script></html>
"""


def fold_sheet(root, slug, ref, raw, scans, skip=(), leaf_of=None, note=''):
    """Write review/<slug>/folds/index.html: every scan, with a fold line the editor can move and save.

    For each opening the page shows the whole scan small, and beside it a
    strip STRIP_HALF pixels either side of the proposed fold at half size, on
    which a click places the line. "Save my folds" gives folds_<slug>.json
    with the x of every fold; see placed().
    """
    import json
    from PIL import Image, ImageDraw
    out = os.path.join(root, 'review', slug, 'folds')
    os.makedirs(out, exist_ok=True)
    leaf_of = leaf_of or {}
    items = []
    for name, fold, left, right in scans:
        im = Image.open(os.path.join(raw, name)).convert('RGB')
        stem = os.path.splitext(name)[0]

        def say(pid):
            what = 'left out' if pid in skip else 'a page of the edition'
            leaf = leaf_of.get(pid)
            return '%s<b>%s</b>' % (('leaf %s: ' % leaf) if leaf else '', what)
        small = im.copy()
        if fold is not None:
            ImageDraw.Draw(small).line([(fold, 0), (fold, im.height)], fill=(255, 0, 0), width=8)
        k = 700 / im.width
        small.resize((700, int(im.height * k)), Image.LANCZOS).save(os.path.join(out, stem + '.jpg'), quality=78)
        item = {'name': name, 'fold': fold, 'whole': stem + '.jpg'}
        if fold is None:
            item['text'] = 'One page, not cut. %s.' % say(left)
        else:
            x0 = max(0, fold - STRIP_HALF)
            x1 = min(im.width, fold + STRIP_HALF)
            strip = im.crop((x0, 0, x1, im.height))
            w, h = int(strip.width * STRIP_SCALE), int(strip.height * STRIP_SCALE)
            strip.resize((w, h), Image.LANCZOS).save(os.path.join(out, stem + '_strip.jpg'), quality=82)
            item.update({'strip': stem + '_strip.jpg', 'x0': x0, 'w': w, 'h': h,
                         'text': 'Left half, %s. Right half, %s.' % (say(left), say(right))})
        items.append(item)
    page = (_FOLD_PAGE.replace('__REF__', html.escape(ref)).replace('__SLUG__', slug)
            .replace('__OVERLAP__', str(OVERLAP)).replace('__SCALE__', str(STRIP_SCALE))
            .replace('__NOTE__', ('<p>%s</p>' % html.escape(note)) if note else '')
            .replace('__ITEMS__', json.dumps(items, ensure_ascii=False)))
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.join(out, 'index.html'), 'with', len(items), 'scan(s)')


def _put(unit_dir, docs, parts):
    """parts: {(document number, page id): [lines]}. Writes corpus.txt and one file per page.

    A page that carries the end of one document and the beginning of the
    next stands under both in corpus.txt; its page file has both parts, in
    the order of the documents.
    """
    tdir = os.path.join(unit_dir, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    out, whole, order = [], {}, []
    for n, ids in docs:
        out.append('[DOC %d]' % n)
        for pid in ids:
            out.append('[PAGE %s]' % pid)
            out.extend(parts[(n, pid)])
            if pid not in whole:
                whole[pid] = []
                order.append(pid)
            whole[pid].extend(parts[(n, pid)])
    for pid in order:
        io.open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(whole[pid]) + '\n')
    io.open(os.path.join(unit_dir, 'corpus.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    return len(order)


def _read_corpus(unit_dir):
    """corpus.txt back into {(document number, page id): [lines]}."""
    import re
    parts, doc, key = {}, None, None
    for line in io.open(os.path.join(unit_dir, 'corpus.txt'), encoding='utf-8').read().rstrip('\n').split('\n'):
        m = re.match(r'^\[DOC (\d+)\]$', line)
        if m:
            doc = int(m.group(1))
            continue
        m = re.match(r'^\[PAGE (\S+)\]$', line)
        if m:
            key = (doc, m.group(1))
            parts[key] = []
            continue
        parts[key].append(line)
    return parts


def correct(unit_dir, slug, docs, rows, write, source='read on the scan'):
    """docs: [(document number, [page ids])]; rows: [(page id, old, new, why)].

    Each `old` must stand exactly once on its page (in whichever document's
    part of it). Returns the number applied. With write=False only checks.
    """
    parts = _read_corpus(unit_dir)
    assert set(parts) == {(n, pid) for n, ids in docs for pid in ids}, 'corpus.txt and DOCS disagree'
    log, bad = [], []
    for pid, old, new, why in rows:
        hits = [(k, i) for k in parts if k[1] == pid for i, l in enumerate(parts[k]) if old in l]
        n = sum(parts[k][i].count(old) for k, i in hits)
        if n != 1:
            bad.append('%s: found %d time(s): %r' % (pid, n, old[:70]))
            continue
        k, i = hits[0]
        parts[k][i] = parts[k][i].replace(old, new)
        page = dict(docs)[k[0]].index(pid) + 1
        key = hashlib.md5(('%s|%s|%s' % (pid, old, new)).encode()).hexdigest()[:8]
        log.append([key, '%s-%03d' % (slug, k[0]), page, old, new, '%s: %s -> %s' % (pid, old[:60], new[:60]),
                    '%s: %s' % (source, why)])
    print(len(rows), 'rows;', len(bad), 'do not apply')
    for b in bad:
        print('  ', b)
    if bad or not write:
        return 0
    _put(unit_dir, docs, parts)
    path = os.path.join(unit_dir, 'transcription_decisions.csv')
    new_file = not os.path.exists(path)
    with io.open(path, 'a', encoding='utf-8-sig' if new_file else 'utf-8', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['key', 'pad', 'page', 'transcribed', 'proposed', 'decision', 'why'])
        w.writerows(log)
    print('written and logged')
    return len(log)


def write_pages(unit_dir, docs, pages):
    """docs: [(document number, [page ids])]; pages: {page id: [lines]} or {(document number, page id): [lines]}."""
    parts = {}
    for n, ids in docs:
        for pid in ids:
            parts[(n, pid)] = pages[(n, pid)] if (n, pid) in pages else pages[pid]
    print('wrote', _put(unit_dir, docs, parts), 'page files and corpus.txt')


def write_summaries(root, unit_dir, slug, ref, S, how):
    """S: {document number: (German, English)}. Writes every place a summary is kept.

    units/<slug>/summaries_de.yml, the two cache folders, and this holding's
    lines in site/_data/summaries.yml and summaries_de.yml. In the site
    files only this holding's own lines are replaced or put in; every other
    line stays as it is (they carry corrections made by hand).
    """
    import json
    import re
    import yaml
    with open(os.path.join(unit_dir, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# German summaries of %s, %s\n# Claim-checked in session (intake/claim_check.yml).\n'
                '# A finding aid, not part of the edition text.\n' % (ref, how))
        for n, (de, _en) in sorted(S.items()):
            f.write('%s-%03d: %s\n' % (slug, n, json.dumps(de, ensure_ascii=False)))
    for sub, i in (('summaries-raw-de', 0), ('summaries-raw', 1)):
        d = os.path.join(root, 'cache', sub)
        os.makedirs(d, exist_ok=True)
        for n, pair in S.items():
            pad = '%s-%03d' % (slug, n)
            json.dump({'letter': str(n), 'pad': pad, 'summary': pair[i],
                       'model': 'in-session; claim-checked in session',
                       'usage': {'input': 0, 'output': 0, 'cache_read': 0}},
                      open(os.path.join(d, pad + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for name, i in (('summaries_de.yml', 0), ('summaries.yml', 1)):
        path = os.path.join(root, 'site', '_data', name)
        keep = [l for l in io.open(path, encoding='utf-8', newline='').read().split('\n') if not l.startswith(slug + '-')]
        new = [yaml.safe_dump({'%s-%03d' % (slug, n): pair[i]}, allow_unicode=True, width=10 ** 9).rstrip('\n')
               for n, pair in sorted(S.items())]
        assert all('\n' not in l for l in new)
        at = next((k for k, l in enumerate(keep)
                   if re.match(r'^[a-z0-9]+-\d+[a-z]?: ', l) and l.split('-', 1)[0] > slug), len(keep))
        keep[at:at] = new
        io.open(path, 'w', encoding='utf-8', newline='').write('\n'.join(keep))
    print(len(S), 'summary/ies written, German and English, and put into the site data')


def take_folds(root, slug, path):
    """The editor's saved folds become the holding's: copied to units/<slug>/intake/folds.json, pages cut again.

    Runs the holding's own build_pages.py --crop --sheet (which reads the
    file through placed()), stages the new page images over the old and
    remakes the web images. Nothing else of the holding changes.
    """
    import json
    import shutil
    import subprocess
    import sys
    mine = json.load(io.open(path, encoding='utf-8'))
    assert mine and all(isinstance(v, int) for v in mine.values()), 'not a folds file'
    intake = os.path.join(root, 'units', slug, 'intake')
    dst = os.path.join(intake, 'folds.json')
    old = json.load(io.open(dst, encoding='utf-8')) if os.path.isfile(dst) else {}
    shutil.copyfile(path, dst)
    print(len(mine), 'folds taken;', sum(1 for k, v in mine.items() if old.get(k) != v), 'differ from the ones on file')
    for cmd in (['units/%s/intake/build_pages.py' % slug, '--crop', '--sheet'],
                ['pipeline/intake/stage_pages.py', '--unit', slug, '--force'],
                ['pipeline/build/relabel_scans.py', '--unit', slug, '--apply'],
                ['pipeline/build/make_scan_derivatives.py', '--unit', slug, '--force']):
        print('>', ' '.join(cmd))
        subprocess.run([sys.executable, '-W', 'ignore'] + cmd, cwd=root, check=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == 'folds':
        take_folds(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), sys.argv[2], sys.argv[3])
    else:
        sys.exit('usage: python pipeline/intake/courtbook.py folds <slug> <folds_<slug>.json>')
