"""Turn one of Jutta Dennerlein's digital reissues of Albert Breyer's articles
(UpstreamVistula.org, PDF) into a work's original.md.

The editor supplied the PDFs (their folder "Books_2", 2026-10-19). The text
layer of the PDF is read with PyMuPDF (`pip install pymupdf`, free), not
retyped, and laid out in the form of the other works (docs/LITERATURE_PLAN.md):

- `[p. N]` on a line of its own where page N of the reissue begins (the
  number of its running head "N von 59"). The reissue's pages are not those
  of the first print, which the PDF does not give: the work is cited by them.
- One paragraph per line, a blank line between paragraphs. A paragraph
  carried over a page is cut at the mark; a word divided there keeps its
  hyphen ("Frühjahrsüberschwem-" / "mung"). Inside a page a word divided at
  the end of a line is joined again; a hyphen before a capital ("Alt-
  Beelitz") or before "und"/"oder" ("Erlen- und") stays.
- A line that stops short of the right margin (verse, a caption) keeps its
  line break; one that stops at a picture beside it runs on.
- Pieces of one printed line that the PDF holds apart (the words of a
  justified line beside a picture, the names of a row of signatures) are
  made one line again, left to right (merge_rows).
- Headings: chapters (bold, or plain at 12 points as in the articles of
  1935) `##`, sections (bold italic) `###`.
- Letter-spaced words, printed in italic in the reissue, `*so*`; a quotation
  or a caption set wholly in italic is `*so*` as a whole.
- Footnote markers `[^n]`, the notes `[^n]: ...` under their page's text. A
  raised 2 or 3 after "m" or "km" is the square or cube ("km²"), not a note.
- Pictures are not reproduced: a caption stands as `[Bild: ...]` (`[Karte:
  ...]` for a map, by --label). Words drawn in a picture are not in the text
  layer; --insert puts an editorial line in their place.
- Indented quotations as Markdown quotations (`> `); a line indented only
  because a picture stands left of it is not one.
- Tables as Markdown tables, from PyMuPDF's table finder, cell by cell. A row
  with a single filled cell across joined cells or in the first column (the
  village a table is about, "Kreis Turek") is set as a line of its own in
  italic and the table cut there; so is a short line standing just over a
  table. A table found again inside a larger one is read once.
- The front (before the first numbered page): its lines as they stand, the
  contents as one table of chapter and page.
- A page turned on its side with its text running up the page (the
  statistics of chapter VI) is drawn upright on a page of its own first
  (upright), so that its words are read in order.

Left out: the running heads and feet, and the pages given by --skip (the
reissue's own foreword: the editor, 2026-10-19). The words are the PDF's;
nothing is corrected. A slip is noted in the work's notes.md.

Usage:
  python pipeline/literature/upstream_pdf.py <pdf> <slug> [--skip 2] [--pages 1-56]
      [--label 30=Karte] [--insert "14=[Karte: ...]"]
--skip    PDF pages (1-based) left out
--pages   reissue pages kept (all if not given); the pages before the first
          numbered page are the front and are kept unless skipped
--label   N=word: the captions on reissue page N are of a map, not a picture
--insert  N=text: an editorial line at the end of reissue page N
The command for each work is in its notes.md.
Writes literature/<slug>/original.md (LF).
"""
import argparse, os, re, sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HEAD_Y, FOOT_Y = 60, 775          # running head above, running foot below
MARGIN_X = 470                    # a line ending right of this runs on
QUOTE_X = 95                      # a line starting right of this is indented
BODY_GAP = 9                      # more space than this between lines: new paragraph
RUNHEAD = re.compile(r'^\s*(\d+) von \d+\s*$', re.M)
# the running head and foot, wherever a turned page puts them
RUNNING = re.compile(r'^\s*(Albert Breyer: .*|\d+ von \d+|Digital Revision.*|'
                     r'Version 1\.0 .*|www\.UpstreamVistula\.org)\s*$')
LEADER = re.compile(r'^(.*?)\s*\.{3,}\s*(\d+)\s*$')
ROMAN = re.compile(r'^[IVX]+\.$')
KEEP_HYPHEN = ('und', 'oder', 'bis', 'sowie', 'als', 'wie', 'u.')


def span_kind(s):
    bold = 'Bold' in s['font'] or s['flags'] & 16
    italic = 'Italic' in s['font'] or s['flags'] & 2
    t = s['text']
    if s['size'] < 7.5 and t.strip().isdigit():
        return 'sup'
    return ('bold-italic' if bold and italic else 'bold' if bold
            else 'italic' if italic else 'plain')


def line_record(line):
    spans = [s for s in line['spans'] if s['text']]
    kinds = [span_kind(s) for s in spans]
    # a Polish letter set in another font inside a spaced word takes the
    # word's italic
    for i, s in enumerate(spans):
        t = s['text']
        if kinds[i] == 'plain' and t.strip() == t and 0 < len(t) <= 2:
            near = [kinds[j] for j in (i - 1, i + 1) if 0 <= j < len(spans)]
            if 'italic' in near:
                kinds[i] = 'italic'
    sizes = [s['size'] for s, k in zip(spans, kinds) if k != 'sup' and s['text'].strip()]
    size = max(sizes) if sizes else 0
    styles = {k for s, k in zip(spans, kinds) if s['text'].strip() and k != 'sup'}
    first = next((k for s, k in zip(spans, kinds) if s['text'].strip()), None)
    if first == 'sup' and size and size < 9:
        kind = 'note'
    elif styles and styles <= {'bold'}:
        kind = 'h2'
    elif styles and styles <= {'bold-italic'}:
        kind = 'h3'
    elif size >= 11.5:
        kind = 'large'                  # a chapter set large, not bold (1935),
                                        # or the title on the front
    elif size and size < 9:
        kind = 'small'
    else:
        kind = 'body'
    out = ''
    for s, k in zip(spans, kinds):
        t = s['text']
        if k == 'sup':
            n = t.strip()
            if re.search(r'\b[kq]?m$', out) and n in ('2', '3'):
                out += '²' if n == '2' else '³'     # "1000 km²", not a note
                continue
            out += f'[^{n}]: ' if first == 'sup' and not out.strip() else f'[^{n}]'
            continue
        # emphasis in the text, not in a heading or a caption set wholly in italic
        if k != 'italic' or styles & {'bold', 'bold-italic'} or (
                styles == {'italic'} and kind != 'body'):
            out += t
            continue
        # emphasis: open and close round the words, not the spaces
        lead = t[:len(t) - len(t.lstrip())]
        core = t.strip()
        trail = t[len(t.rstrip()):]
        if out.endswith('*') and not lead and core:
            out = out[:-1] + core + '*' + trail
        elif core:
            out += lead + '*' + core + '*' + trail
        else:
            out += t
    out = re.sub(r'\*[ \t]+\*', ' ', out)       # two runs of emphasis made one
    x0, y0, x1, y1 = line['bbox']
    return dict(x0=x0, y0=y0, x1=x1, y1=y1, text=out.rstrip(), kind=kind)


def join(lines):
    """One paragraph's lines, joined as the docstring says."""
    text = lines[0]['text'].strip()
    for prev, ln in zip(lines, lines[1:]):
        t = ln['text'].strip()
        if prev['x1'] < MARGIN_X and not prev.get('wrap'):
            text += '\n' + t
        elif text.endswith('-*') and t.startswith('*'):
            # a spaced word divided at the end of a line ("Emilien-" / "heim")
            nxt = t[1:].split(' ')[0]
            if nxt[:1].islower() and nxt not in KEEP_HYPHEN:
                text = text[:-2] + t[1:]
            else:
                text = text[:-1] + t[1:]
        elif text.endswith('-') and not text.endswith(' -'):
            nxt = t.split(' ')[0]
            if nxt[:1].islower() and nxt not in KEEP_HYPHEN and not nxt.startswith('*'):
                text = text[:-1] + t
            else:
                text += t if nxt[:1].isupper() else ' ' + t
        else:
            text += ' ' + t
    return re.sub(r'\*[ \t]+\*', ' ', text)


HEAD_ROW = re.compile(r'^(Jahr|Nr)\b')


def row_texts(page, row):
    """A table row's cells as text (None for a cell joined to the one before)."""
    cells = []
    for c in row.cells:
        t = ' '.join((page.get_textbox(c) if c else '').split())
        # a word divided at the end of a line in the cell ("Vermögens- stand")
        t = re.sub(r'(\w)- ([a-zäöüß]\w*)',
                   lambda m: m.group(0) if m.group(2) in KEEP_HYPHEN
                   else m.group(1) + m.group(2), t)
        cells.append(t)
    return cells


def table_md(page, table, next_first=None):
    """A table as Markdown; rows with one filled cell become lines of their own.

    next_first: the first row of the next table on the page, which may be
    the header a label at the foot of this one stands over."""
    out, seg = [], []

    def flush():
        if not seg:
            return
        n = max(len(r) for r in seg)
        rows = [r + [''] * (n - len(r)) for r in seg]
        head = HEAD_ROW.match(rows[0][0] or '')
        md = ['| ' + ' | '.join(c.replace('|', '/') for c in r) + ' |' for r in rows]
        if head:
            md.insert(1, '|' + '---|' * n)
        out.append('\n'.join(md))
        seg.clear()

    rows = [row_texts(page, r) for r in table.rows]
    for k, (row, cells) in enumerate(zip(table.rows, rows)):
        filled = [c for c in cells if c]
        nxt = rows[k + 1] if k + 1 < len(rows) else next_first
        # one filled cell across a row of joined cells ("Kreis Turek"), in the
        # first column, or over a header ("Budki" over "Jahr der Angabe"); a
        # village alone in its column among the rows is a row of the table
        spans = (any(c is None for c in row.cells) or bool(cells[0])
                 or bool(nxt and HEAD_ROW.match(nxt[0] or '')))
        if len(filled) == 1 and spans and not re.match(r'^\d+$', filled[0]):
            flush()
            out.append('*' + filled[0] + '*')
        elif filled:
            seg.append(cells)
    flush()
    return out


def merge_rows(recs):
    """Pieces of one printed line, cut apart by the PDF (a justified line
    beside a picture, a signature), made one line again, left to right."""
    out = []
    for r in sorted(recs, key=lambda r: (r['y0'], r['x0'])):
        h = next((h for h in reversed(out[-4:])
                  if h['kind'] == r['kind'] and r['kind'] in ('body', 'h2', 'h3')
                  and min(h['y1'], r['y1']) - max(h['y0'], r['y0']) > 0.5 * (r['y1'] - r['y0'])
                  and (r['x0'] >= h['x1'] - 1 or r['x1'] <= h['x0'] + 1)), None)
        if h is None:
            out.append(r)
        elif r['x0'] >= h['x1'] - 1:
            h['text'] = h['text'].rstrip() + ' ' + r['text'].strip()
            h['x1'] = r['x1']
        else:
            h['text'] = r['text'].rstrip() + ' ' + h['text'].strip()
            h['x0'] = r['x0']
    for r in out:
        r['text'] = re.sub(r'\*[ \t]+\*', ' ', r['text'])
    return out


def sideways(page):
    """True for a page turned on its side with its text running up or down
    (the tables of chapter VI), not for one only shown turned (the map)."""
    if not page.rotation:
        return False
    dirs = [l['dir'] for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])]
    return bool(dirs) and sum(abs(d[0]) < 0.5 for d in dirs) > len(dirs) / 2


def upright(path, i, keep):
    """Page i (0-based) of the PDF drawn again upright on a page of its own.

    The page is set unturned in a second copy of the PDF and drawn turned back
    by a quarter onto a new landscape page: its words then run left to right
    at their own size, and the table finder reads them. (Read through the
    page's rotation matrix, the words came out in pieces.) The documents are
    kept in `keep`: a page is no use once its document is gone."""
    src = pymupdf.open(path)
    src[i].set_rotation(0)
    w, h = src[i].rect.width, src[i].rect.height
    tmp = pymupdf.open()
    page = tmp.new_page(width=h, height=w)
    page.show_pdf_page(page.rect, src, i, rotate=-90)
    keep += [src, tmp]
    return page


def page_blocks(page, front):
    """The page's paragraphs, notes and tables, in order down the page."""
    foot_y = page.rect.height - (842 - FOOT_Y)
    tables = page.find_tables().tables
    # a table found again inside a larger one (the summary under the
    # statistics) is read once, as part of the larger
    tables = [t for t in tables if not any(
        o is not t and pymupdf.Rect(o.bbox).contains(pymupdf.Rect(t.bbox)) for o in tables)]
    boxes = [pymupdf.Rect(t.bbox) for t in tables]
    images = [pymupdf.Rect(im['bbox']) for im in page.get_image_info()]
    recs = []
    for b in page.get_text('rawdict')['blocks']:
        for line in b.get('lines', []):
            for s in line['spans']:
                s['text'] = ''.join(c['c'] for c in s['chars'])
            r = line_record(line)
            if not r['text'].strip():
                continue
            if r['kind'] == 'large':
                r['kind'] = 'body' if front else 'h2'
            if r['y0'] < HEAD_Y or r['y0'] > foot_y or RUNNING.search(r['text']):
                continue
            mid = pymupdf.Point((r['x0'] + r['x1']) / 2, (r['y0'] + r['y1']) / 2)
            if any(mid in bx for bx in boxes):
                continue
            recs.append(r)
    recs = merge_rows(recs)
    # a line beside a picture: one stopping at it runs on; one starting
    # right of it is not a quotation
    for r in recs:
        for im in images:
            if im.y0 < r['y1'] and im.y1 > r['y0']:
                if 0 <= im.x0 - r['x1'] < 40:
                    r['wrap'] = True
                if 0 <= r['x0'] - im.x1 < 40:
                    r['by_image'] = True
    recs.sort(key=lambda r: (round(r['y0']), r['x0']))

    order = sorted(range(len(tables)), key=lambda k: boxes[k].y0)
    items = []
    for j, k in enumerate(order):
        nxt = tables[order[j + 1]] if j + 1 < len(order) else None
        first = row_texts(page, nxt.rows[0]) if nxt and nxt.rows else None
        items.append((boxes[k].y0, 'table', table_md(page, tables[k], first)))
    groups = []
    for r in recs:
        g = groups[-1] if groups else None
        if r['kind'] == 'small' and g and g['kind'] == 'note' and r['y0'] - g['lines'][-1]['y1'] < 6:
            g['lines'].append(r)          # a note running on
            continue
        same_row = [h for h in groups if h['kind'] == 'small' and r['kind'] == 'small'
                    and 0 <= r['y0'] - h['lines'][-1]['y1'] < 6
                    and r['x0'] < h['x1'] and r['x1'] > h['x0']]
        if same_row:                       # a caption's second line, under its first
            h = same_row[-1]
            h['lines'].append(r)
            h['x0'], h['x1'] = min(h['x0'], r['x0']), max(h['x1'], r['x1'])
            continue
        quote = r['kind'] == 'body' and r['x0'] > QUOTE_X and not r.get('by_image')
        if (g and g['kind'] == r['kind'] and r['kind'] in ('body', 'h2', 'h3')
                and r['y0'] - g['lines'][-1]['y1'] < BODY_GAP and g['quote'] == quote):
            g['lines'].append(r)
            continue
        groups.append(dict(kind=r['kind'], quote=quote, lines=[r], x0=r['x0'], x1=r['x1']))

    for g in groups:
        y = g['lines'][0]['y0']
        if g['kind'] == 'note':
            items.append((y + 10000, 'note', ' '.join(l['text'].strip() for l in g['lines'])))
        elif front and g['kind'] in ('small', 'body'):
            items.append((y, 'front', g['lines']))      # the title page's lines
        elif g['kind'] == 'small':
            items.append((y, 'caption', ' '.join(l['text'].strip() for l in g['lines'])))
        elif g['kind'] in ('h2', 'h3'):
            items.append((y, g['kind'], ' '.join(l['text'].strip() for l in g['lines'])))
        else:
            items.append((y, 'quote' if g['quote'] else 'body', join(g['lines'])))
    items.sort(key=lambda i: i[0])
    # a short line standing over a table names what it is about ("Daniszew"),
    # like a row with one filled cell
    for k, (y, kind, payload) in enumerate(items[:-1]):
        if (kind in ('body', 'quote') and '\n' not in payload and len(payload) < 80
                and items[k + 1][1] == 'table'):
            items[k] = (y, 'label', payload)
    return items


def render(kind, payload, label):
    if kind == 'table':
        return payload
    if kind == 'note':
        return [payload]
    if kind == 'caption':
        return [f'[{label}: {payload}]']
    if kind == 'h2':
        return ['## ' + payload]
    if kind == 'h3':
        return ['### ' + payload]
    if kind == 'quote':
        return ['\n'.join('> ' + l for l in payload.split('\n'))]
    if kind == 'label':
        return ['*' + payload.replace('*', '') + '*']
    if kind == 'front':
        lines = [l['text'].strip() for l in payload]
        # the contents: a chapter's numeral stands on a line of its own
        joined = []
        for l in lines:
            if joined and ROMAN.match(joined[-1]) and LEADER.match(l):
                joined[-1] += ' ' + l
            else:
                joined.append(l)
        rows = [LEADER.match(l) for l in joined]
        if all(rows):
            return ['\n'.join(f'| {m.group(1).strip()} | {m.group(2)} |' for m in rows)]
        return ['\n'.join(joined)]
    return [payload]


def page_range(spec):
    if not spec:
        return None
    keep = set()
    for part in spec.split(','):
        a, _, b = part.partition('-')
        keep.update(range(int(a), int(b or a) + 1))
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('slug')
    ap.add_argument('--skip', default='')
    ap.add_argument('--pages', default='')
    ap.add_argument('--label', action='append', default=[],
                    help='N=Karte: the caption on reissue page N is a map')
    ap.add_argument('--insert', action='append', default=[],
                    help='N=text: an editorial line on reissue page N, for a '
                         'picture whose words are not in the text layer')
    a = ap.parse_args()
    skip = page_range(a.skip) or set()
    keep = page_range(a.pages)
    labels = dict(l.split('=', 1) for l in a.label)
    inserts = dict(l.split('=', 1) for l in a.insert)
    doc = pymupdf.open(a.pdf)
    out, keep_open = [], []
    for i, page in enumerate(doc, 1):
        if i in skip:
            continue
        m = RUNHEAD.search(page.get_text('text'))
        n = int(m.group(1)) if m else None
        if n is None and out and any(l.startswith('[p. ') for l in out):
            sys.exit(f'PDF page {i} has no page number after the numbered pages began')
        if n is not None and keep is not None and n not in keep:
            continue
        if n is not None:
            out.append(f'[p. {n}]')
        if sideways(page):
            page = upright(a.pdf, i - 1, keep_open)
        label = labels.get(str(n), 'Bild')
        for _, kind, payload in page_blocks(page, front=n is None):
            for block in render(kind, payload, label):
                # the contents' rows, one table though they stand apart
                if (n is None and block.startswith('| ') and out
                        and out[-1].startswith('| ')):
                    out[-1] += '\n' + block
                else:
                    out.append(block)
        if str(n) in inserts:
            out.append(inserts[str(n)])
    text = '\n\n'.join(out) + '\n'
    path = os.path.join(ROOT, 'literature', a.slug, 'original.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'{path}: {text.count(chr(10))} lines, {sum(l.startswith("[p. ") for l in out)} pages')


if __name__ == '__main__':
    main()
