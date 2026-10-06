# -*- coding: utf-8 -*-
"""Shared steps for a holding that is a few leaves of a bound court book.

Used by the scripts in units/<slug>/intake/ of the Poznań court books (the
Prusimski era, docs/PRUSIMSKI_ERA_PLAN.md). Nothing about any one holding is
in here: each holding's own script says which scans it has, where each fold
is, which halves are pages, and what was corrected.

- cut():        cut each opening at its fold into two whole pages. Each page
                keeps OVERLAP pixels beyond the fold, so a line that runs into
                the gutter stays whole. A scan that is one page is copied.
- fold_sheet(): the sheet on which the editor approves the folds, and which
                halves are pages of the edition, before a holding is
                published (the editor's rule, 2026-10-06).
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


def fold_sheet(root, slug, ref, raw, scans, skip=(), leaf_of=None, note=''):
    """Write review/<slug>/folds/index.html: every scan with its fold drawn on it."""
    from PIL import Image, ImageDraw
    out = os.path.join(root, 'review', slug, 'folds')
    os.makedirs(out, exist_ok=True)
    leaf_of = leaf_of or {}
    width = 1500
    rows = []
    for name, fold, left, right in scans:
        im = Image.open(os.path.join(raw, name)).convert('RGB')
        d = ImageDraw.Draw(im, 'RGBA')
        if fold is not None:
            d.rectangle([fold - OVERLAP, 0, fold + OVERLAP, im.height], fill=(255, 0, 0, 40))
            d.line([(fold, 0), (fold, im.height)], fill=(255, 0, 0, 255), width=5)
        k = width / im.width
        pic = os.path.splitext(name)[0] + '.jpg'
        im.resize((width, int(im.height * k)), Image.LANCZOS).save(os.path.join(out, pic), quality=80)

        def say(pid):
            what = 'left out' if pid in skip else 'page of the edition'
            leaf = leaf_of.get(pid)
            return '%s<b>%s</b>' % (('leaf %s: ' % leaf) if leaf else '', what)
        if fold is None:
            line = 'One page, not cut. %s.' % say(left)
        else:
            line = 'Left half, %s. Right half, %s. Fold at %d of %d pixels.' % (say(left), say(right), fold, im.width)
        rows.append('<section><h2>%s</h2><p>%s</p><img src="%s" alt="%s" loading="lazy"></section>'
                    % (html.escape(name), line, html.escape(pic), html.escape(name)))
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Folds: %s</title>'
            '<style>body{font:16px/1.5 Georgia,serif;max-width:1540px;margin:2em auto;padding:0 16px;background:#fbfaf7;color:#222}'
            'img{width:100%%;border:1px solid #ccc}section{margin:2.5em 0}h2{margin:0 0 .2em}</style>'
            '<h1>Folds: %s</h1>'
            '<p>%d scan(s). An opening is cut at the red line into two pages; each page also keeps the shaded strip '
            'beyond the line, so a line of writing that runs into the fold stays whole. Please look for a red line that '
            'crosses writing, and for a half marked wrongly as a page or as left out, and tell me the scan.</p>%s%s</html>'
            % (html.escape(ref), html.escape(ref), len(rows), ('<p>%s</p>' % html.escape(note)) if note else '',
               '\n'.join(rows)))
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.join(out, 'index.html'), 'with', len(rows), 'scan(s)')


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
