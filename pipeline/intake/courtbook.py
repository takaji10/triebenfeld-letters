# -*- coding: utf-8 -*-
"""Shared steps for a holding that is a few leaves of a bound court book.

Used by the scripts in units/<slug>/intake/ of the Poznań court books (the
Prusimski era, docs/PRUSIMSKI_ERA_PLAN.md). Nothing about any one holding is
in here: each holding's own script says which scans it has, where each fold
is, which halves are pages, and what was corrected.

- cut():        cut each opening at its fold into two whole pages. Each page
                keeps OVERLAP pixels beyond the fold, so a line that runs into
                the gutter stays whole. A scan that is one page is copied.
- fold_sheet(): the page on which the editor sees every opening whole, pages
                through them with the arrow keys, drags the fold line and
                turns a sheet that was photographed at a slant, and saves,
                before a holding is published (the editor's rule,
                2026-10-06). It is the page of fold_page.py, the same one
                review_folds.py writes for the other holdings. placed() and
                take_folds() bring the saved folds and angles back.
- holding_main(): the steps of one holding, run from its intake/holding.py
                (the later holdings; the first four have a script per step).
- correct():    apply readings corrected against the scan to the page files
                and corpus.txt, each demanded exactly once on its page, and
                log them in transcription_decisions.csv.

The fold is the thin dark line of the gutter, not the darkest band near the
middle of the opening: find_fold() looks for it, and every fold is then
looked at on a strip before it is written into the holding's script.
"""
import csv
import hashlib
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
    # the mark alone on its line, or dressed as a heading: "### **[78v]**"
    parts = re.split(r'(?m)^(?:#+\s*)?\**\\?\[(\d+v?)\\?\]\**\s*$', s)
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
    Where the editor turned a sheet on the fold page (placed()), the scan is
    turned first, so that the cut runs along the fold.
    """
    from PIL import Image
    processed = os.path.join(raw, 'processed')
    apart = os.path.join(processed, '_not_staged')
    os.makedirs(apart, exist_ok=True)
    angles = getattr(scans, 'angles', {})
    n = 0
    for name, fold, left, right in scans:
        im, dx = turned(Image.open(os.path.join(raw, name)).convert('RGB'), angles.get(name, 0))
        if fold is None:
            parts = [(left, (0, 0, im.width, im.height))]
        else:
            x = int(round(fold + dx))
            parts = [(left, (0, 0, x + OVERLAP, im.height)), (right, (x - OVERLAP, 0, im.width, im.height))]
        for pid, box in parts:
            folder = apart if pid in skip else processed
            im.crop(box).save(os.path.join(folder, pid + '.jpg'), quality=92)
            n += 1
    print('cut', n, 'page images into', processed, ('(%d sheet(s) turned)' % len(angles)) if angles else '')


class Scans(list):
    """A holding's SCANS with the editor's folds put in; `.angles` is {file name: degrees} where they turned a sheet."""
    angles = {}
    mine = ()


def placed(here, scans):
    """`scans` with the folds the editor placed, if they saved any (folds.json beside the holding's script).

    The fold page offers "folds_<slug>.json"; `python pipeline/intake/courtbook.py
    folds <slug> <that file>` copies it to units/<slug>/intake/folds.json and
    cuts the pages again. The numbers in the script stay as the first proposal.

    The file is {scan: {"fold": x in pixels, "angle": degrees}}; a file saved
    by the first fold page (2026-10-07), {scan: x}, is read too. The angle is
    how far the sheet is turned, counter-clockwise, before it is cut: cut()
    and fold_sheet() take it from the list this returns.
    """
    import json
    out = Scans(scans)
    out.angles, out.mine = {}, set()
    p = os.path.join(here, 'folds.json')
    if not os.path.isfile(p):
        return out
    mine = json.load(io.open(p, encoding='utf-8'))
    for k, (name, fold, left, right) in enumerate(scans):
        v = mine.get(name)
        if v is None:
            continue
        if not isinstance(v, dict):
            v = {'fold': v}
        if fold is not None and v.get('fold') is not None:
            fold = int(v['fold'])
        if v.get('angle'):
            out.angles[name] = float(v['angle'])
        out[k] = (name, fold, left, right)
        out.mine.add(name)
    return out


def turned(im, angle):
    """The scan turned by `angle` degrees counter-clockwise about its centre, and how far its left edge moved.

    The canvas grows to hold the turned sheet, so nothing is lost; the
    corners this opens are filled with the colour of the scan's own border.
    An x on the unturned scan is x + the second value on the turned one,
    which is how the fold page shows it (the sheet turns about its centre
    under a vertical line).
    """
    from PIL import Image
    if not angle or abs(angle) < 0.01:
        return im, 0
    g = im.resize((64, 64))
    edge = [g.getpixel((x, y)) for x in range(64) for y in (0, 63)] + [g.getpixel((x, y)) for y in range(64) for x in (0, 63)]
    fill = tuple(sorted(c[k] for c in edge)[len(edge) // 2] for k in range(3))
    rot = im.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=fill)
    return rot, (rot.width - im.width) / 2.0


FOLD_PAGE_WIDTH = 2400      # the fold page shows each scan at this width at most


def fold_sheet(root, slug, ref, raw, scans, skip=(), leaf_of=None, note=''):
    """Write review/<slug>/folds/index.html: the fold page, one opening at a time.

    The page is fold_page.py's, the one review_folds.py has always written:
    the whole opening in the window, the arrow keys to page through, the red
    line dragged onto the fold. Here the sheet can also be turned with the
    mouse. "Save" gives folds_<slug>.json with the x of every fold and the
    angle of every sheet; see placed().
    """
    import fold_page
    from PIL import Image
    out = os.path.join(root, 'review', slug, 'folds')
    os.makedirs(out, exist_ok=True)
    for old in os.listdir(out):                  # the strips of the first fold page
        if old.endswith('_strip.jpg'):
            os.remove(os.path.join(out, old))
    leaf_of = leaf_of or {}
    angles = getattr(scans, 'angles', {})
    mine = getattr(scans, 'mine', ())
    items = []

    def say(pid):
        leaf = leaf_of.get(pid)
        return '%s%s' % (('leaf %s, ' % leaf) if leaf else '', 'left out' if pid in skip else 'a page of the edition')
    for name, fold, left, right in scans:
        src = os.path.join(raw, name)
        stem = os.path.splitext(name)[0]
        dst = os.path.join(out, stem + '.jpg')
        with Image.open(src) as im:
            w, h = im.size
            if not os.path.isfile(dst) or os.path.getmtime(dst) < os.path.getmtime(src) \
                    or Image.open(dst).width != min(w, FOLD_PAGE_WIDTH):
                k = min(1.0, FOLD_PAGE_WIDTH / w)
                im.convert('RGB').resize((int(round(w * k)), int(round(h * k))), Image.LANCZOS).save(dst, quality=85)
        item = {'file': name, 'src': stem + '.jpg', 'w': w, 'h': h, 'angle': angles.get(name, 0),
                'fold': None if fold is None else round(fold / w, 6),
                'conf': 'placed by you' if name in mine else 'first proposal'}
        if fold is None:
            item['note'] = 'One page, not cut: %s.' % say(left)
        else:
            item['note'] = 'Left of the line: %s. Right of the line: %s.' % (say(left), say(right))
        if note:
            item['note'] += '  ' + note
        items.append(item)
    page = fold_page.render(ref, items, save='folds_%s.json' % slug, key='folds2:' + slug, rotate=True, pixels=True,
                            overlap=OVERLAP)
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(page)
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

    Runs the holding's own script with --crop --sheet (holding.py, or
    build_pages.py in the first holdings; it reads the file through
    placed()), stages the new page images over the old and remakes the web
    images. Nothing else of the holding changes.
    """
    import json
    import shutil
    import subprocess
    import sys
    mine = json.load(io.open(path, encoding='utf-8'))
    assert mine and all(isinstance(v, int) or (isinstance(v, dict) and 'fold' in v) for v in mine.values()), 'not a folds file'
    intake = os.path.join(root, 'units', slug, 'intake')
    dst = os.path.join(intake, 'folds.json')
    old = json.load(io.open(dst, encoding='utf-8')) if os.path.isfile(dst) else {}
    if os.path.abspath(path) != os.path.abspath(dst):
        shutil.copyfile(path, dst)
    turned_n = sum(1 for v in mine.values() if isinstance(v, dict) and v.get('angle'))
    print(len(mine), 'scans in the file;', sum(1 for k, v in mine.items() if old.get(k) != v), 'differ from the ones on file;',
          turned_n, 'turned')
    script = 'holding.py' if os.path.isfile(os.path.join(intake, 'holding.py')) else 'build_pages.py'
    cmds = [['units/%s/intake/%s' % (slug, script), '--crop', '--sheet']]
    if os.path.isfile(os.path.join(intake, 'fold_sheet.py')):       # Konin Gr.145 writes its fold page with its own script
        cmds.append(['units/%s/intake/fold_sheet.py' % slug])
    cmds += [['pipeline/intake/stage_pages.py', '--unit', slug, '--force'],
             ['pipeline/build/relabel_scans.py', '--unit', slug, '--apply'],
             # no --force: that remakes every web image of the edition (three minutes); the pages just
             # staged are newer than their web images, which is what the script goes by
             ['pipeline/build/make_scan_derivatives.py', '--unit', slug]]
    for cmd in cmds:
        print('>', ' '.join(cmd))
        subprocess.run([sys.executable, '-W', 'ignore'] + cmd, cwd=root, check=True)


def save_cache(root, slug, tdir):
    """Put intake/translation/doc<N>.yml into the translation cache with translate.py's own save().

    The cache record then carries the hash of the source text it belongs to;
    check_translations.py and publish_translations.py read it from there.
    cache/ is not in the repository: doc<N>.yml and the holding's script are
    the record.
    """
    import sys
    import yaml
    os.chdir(root)
    argv, sys.argv = sys.argv, ['translate.py', '--unit', slug]
    sys.path.insert(0, os.path.join(root, 'pipeline', 'translate'))
    import translate as T
    sys.argv = argv
    for rec in T.load_letters():        # one holding: its documents in order
        number = str(rec['letter_id'])
        p = os.path.join(tdir, 'doc%s.yml' % number)
        if not os.path.isfile(p):
            continue
        payload = yaml.safe_load(io.open(p, encoding='utf-8'))
        assert len(payload['pages']) == len(rec['pages']), \
            'document %s: %d pages of English, the corpus has %d' % (number, len(payload['pages']), len(rec['pages']))
        T.save(rec, payload, {'input': 0, 'output': 0}, None, {'model': 'editor'})
        print('saved', T.out_path(number))


def holding_main(g):
    """The steps of one court-book holding, run from its intake/holding.py.

        python units/<slug>/intake/holding.py            # check only
        ... --crop        cut the page images
        ... --sheet       the fold page for the editor
        ... --write       page files and corpus.txt from the editor's text (once)
        ... --correct     apply ROWS, the readings corrected against the scans (once)
        ... --english     write translation/doc<N>.yml from english()
        ... --cache       put them into the translation cache
        ... --summaries   write the summaries S everywhere they are kept

    The holding's script supplies: SLUG, REF, RAW, SCANS, SKIP, LEAF, DOCS,
    read_source() -> {(document, page id): [paragraphs]}, ROWS, english() ->
    {document: [the English of each page]}, S, HOW. After --correct, --write
    must not be run again: it would put the uncorrected text back.
    """
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    here = os.path.dirname(os.path.abspath(g['__file__']))
    unit_dir = os.path.dirname(here)
    root = os.path.dirname(os.path.dirname(unit_dir))
    arg = sys.argv[1:]
    parts = g['read_source']()
    print(len(parts), 'parts of pages,', sum(len(' '.join(p).split()) for p in parts.values()), 'words in the editor\'s text')
    if '--crop' in arg:
        cut(g['RAW'], placed(here, g['SCANS']), g.get('SKIP', ()))
    if '--sheet' in arg:
        fold_sheet(root, g['SLUG'], g['REF'], g['RAW'], placed(here, g['SCANS']), g.get('SKIP', ()), g.get('LEAF'),
                   note=g.get('FOLD_NOTE', ''))
    if '--write' in arg:
        assert not os.path.exists(os.path.join(unit_dir, 'transcription_decisions.csv')), \
            'corrections are already logged: --write would put the uncorrected text back'
        write_pages(unit_dir, g['DOCS'], parts)
    if '--correct' in arg or (not arg and os.path.exists(os.path.join(unit_dir, 'corpus.txt'))
                              and io.open(os.path.join(unit_dir, 'corpus.txt'), encoding='utf-8').read().strip()):
        correct(unit_dir, g['SLUG'], g['DOCS'], g.get('ROWS', []), '--correct' in arg)
    if '--english' in arg:
        tdir = os.path.join(here, 'translation')
        os.makedirs(tdir, exist_ok=True)
        for n, texts in sorted(g['english']().items()):
            write_doc_yml(os.path.join(tdir, 'doc%d.yml' % n), texts)
    if '--cache' in arg:
        save_cache(root, g['SLUG'], os.path.join(here, 'translation'))
    if '--summaries' in arg:
        write_summaries(root, unit_dir, g['SLUG'], g['REF'], g['S'], g['HOW'])


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == 'folds':
        take_folds(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), sys.argv[2], sys.argv[3])
    else:
        sys.exit('usage: python pipeline/intake/courtbook.py folds <slug> <folds_<slug>.json>')
