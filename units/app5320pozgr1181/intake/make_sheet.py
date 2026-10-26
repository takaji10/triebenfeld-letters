# -*- coding: utf-8 -*-
"""Build the spot sheet for Poznań Gr.1181 as a static, mobile-first page.

    python units/app5320pozgr1181/intake/make_sheet.py            # build into
                                                                  # review/app5320pozgr1181/sheet/
    python units/app5320pozgr1181/intake/make_sheet.py --check    # contact sheet only

Each row's picture is the target line whole, with a line of margin either
side: the page is OCR'd for its line bands (the text is beyond the engine,
the bands are not), the row's passage is placed proportionally by its position
in the page's transcription, and the nearest band is snapped to. The contact
sheet (--check) lets the session check every crop at a glance and fix
outliers with a y override before the sheet is published.
"""
import base64
import html
import io
import json
import os
import re
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))))
from pipeline.ocr import words  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spot_rows import ROWS  # noqa: E402

SLUG = 'app5320pozgr1181'
UNIT = os.path.join(HERE, '..')
CORPUS = os.path.join(UNIT, 'corpus.txt')
SCANS = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\rel1181_scans'
OUT = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'review', SLUG, 'sheet'))

# The pages' ids, as split_and_settle.py writes them (four-digit capture,
# side as crop letter), mapped to the photograph each crop is cut from.
PAGE_FILE = {
    '0161_a': '161', '0161_b': '161v', '0162_a': '162', '0162_b': '162v',
    '0163_a': '163', '0163_b': '163v', '0164_a': '164', '0164_b': '164v',
    '0165_a': '165', '0165_b': '165v', '0166_a': '166', '0166_b': '166v',
    '0167_a': '167', '0167_b': '167v',
}

# Manual y overrides after the contact-sheet check: row id -> (page, y).
Y_OVERRIDE = {}

# The transcription anchor each row's crop is placed by. A distinctive stretch
# of the page's text near the target; the crop is the line holding the text at
# this anchor's proportional position.
ANCHOR = {
    'heading_year':    '4ta Martii',
    'dec_year':        'elapso',
    'francis_day':     'indl~t 8ua Mensis 8bris',
    'junii_word':      'sexta sui Junii',
    'tail_167v':       'Relictam viduam',
    'termilis':        'Termilis Kanino Swi',
    'odechowski':      'voto Mica',
    'zabriski':        'Casimiri Zabriski',
    'strzalko':        'Strzałko iamis',
    'rzekicka':        'Rzek icka',
    'obiesierski':     'Obiesierski',
    'obierunskie':     'Obierun skie',
    'keszycki':        'K szy ciami',
    'schedas_word':    'schaedas trinas',
    'ittis':           'ittis Fratrum intermedium',
    'costensem':       'Costensem',
    'skoli':           'Fundo Bonorum Skoli',
    'flottowa':        'ottowa',
    'mokronos':        'Mokronos',
    'lubraniecki':     'Bogdanski',
    'marszlyn':        'Marszłynowna',
    'sadi':            'Parys sa',
    'nierzychow_sum':  'Nierzychowska ginta',
    'triginta_veto':   'Triginta veto',
    'kowski_name':     'kowski septingentorum',
    'bowski_name':     'bowski sexcentorum',
    'money_formula':   'sex tlor',
    'pawlowa_word':    'Pawłowa Duodecem',
    'reponidem':       'reponi dem',
    'procet':          'procet divisionem perfecerant',
    'quirrimo':        'quirrimo',
    'quani':           'a quani',
    'brtis':           'Oporowa tis Oporowka',
    'hisc_e':          'hisc e partibus',
    'auguratem':       'in augurat em',
    'addidem':         'addi dem mae s',
    'adpsit':          'ad psit',
    'minipali':        'minipali negotio',
    'go_naniae':       'Go naniae',
    'eisneunt':        'eisneunt',
    'hendo':           'extra hendo',
    'compin':          'co m/ns pin dem',
    'arbitatem':       'Arbita tem',
    'insto':           'insto profectitiam',
    'subtam':          'subta am Golinscianam',
    'ressibilibus':    'res s ibilibus',
    'exdiuim':         'exdiuim',
    'illas_manente':   'utramque illa s/m',
    'pro_mimixta':     'binorum et midii pro',
    'summus':          'originalis summ us',
    'scriptuis':       'scriptu is',
    'differ':          'differ itatem',
    'gmae':            'Dominicam gmae',
    'prodisse':        'pro isse',
    'subdapiferida':   'Subdapifinda',
    'p_sabbo':         'sab~bo post Festum',
    'p_diversae':      'diversae formae',
    'p_conges':        'ges~ parte ab altera',
    'p_solutam':       'assurasse summam',
    'p_sororem':       'hanc ultimam fororem',
    'p_kotarbski':     'Kołarbski',
    'p_alterius':      'altenius',
    'p_actis':         'autis Castrensis',
    'p_autem':         'autoni indictionem',
    'pr_nieszwiez':    'Capitaneo Niszczeviens em',
}


BAND_CACHE = os.path.join(SCANS, 'line_bands.json')


def page_lines(photo):
    """[(top, bottom)] of the page's ink lines, from the OCR bands (cached)."""
    cache = {}
    if os.path.isfile(BAND_CACHE):
        cache = json.load(open(BAND_CACHE, encoding='utf-8'))
    if photo in cache:
        return [tuple(b) for b in cache[photo]]
    png = os.path.join(SCANS, photo + '_x2.png')
    if not os.path.isfile(png):
        from PIL import Image
        im = Image.open(os.path.join(SCANS, photo + '.jpg'))
        im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(png)
    ws = words(png, lang='eng', psm=6)
    bands = {}
    for left, top, w, h, conf, txt in ws:
        if not txt.strip():
            continue
        key = round(top / 40)
        b = bands.setdefault(key, [top, top + h])
        b[0] = min(b[0], top)
        b[1] = max(b[1], top + h)
    out = []
    for key in sorted(bands):
        top, bot = bands[key]
        top, bot = top // 2, bot // 2
        if out and top - out[-1][1] < 8:
            out[-1] = (out[-1][0], max(out[-1][1], bot))
        else:
            out.append((top, bot))
    cache[photo] = [list(b) for b in out]
    json.dump(cache, open(BAND_CACHE, 'w', encoding='utf-8'))
    return out


def corpus_pages():
    """{page: (text, offset)} from the built corpus, in order."""
    text = open(CORPUS, encoding='utf-8').read()
    parts = re.split(r'\[(?:DOC \d+|PAGE \S+)\]\n?', text)
    pages = []
    for m in re.finditer(r'\[PAGE (\S+)\]', text):
        pages.append(m.group(1))
    # pages of one document repeat; walk the corpus in order instead
    out = []
    for line in text.split('\n'):
        if line.startswith('[PAGE '):
            out.append(line[6:-1])
    return out


def strip_marks(s):
    """The transcription without its editorial brackets, for placement."""
    return re.sub(r'\[[^\]]*\]', lambda m: re.sub(r'[?]|/\S*?(?=\])|\(|\)',
                                                  '', m.group(0)), s)


def crop_for(row_id, page, y_hint, text):
    """The image bytes of the row's crop: the snapped line plus margin."""
    from PIL import Image
    photo = PAGE_FILE[page]
    key = row_id
    if key in Y_OVERRIDE:
        y = Y_OVERRIDE[key][1]
    elif y_hint:
        y = y_hint
    else:
        anchor = ANCHOR.get(key, '')
        pos = text.find(anchor) if anchor else -1
        if pos < 0:
            pos = len(text) // 2
        frac = pos / max(1, len(text))
        lines = page_lines(photo)
        y = lines[0][0] + frac * (lines[-1][1] - lines[0][0])
    lines = page_lines(photo)
    # snap: the band whose middle is nearest
    band = min(lines, key=lambda b: abs((b[0] + b[1]) / 2 - y))
    top = max(0, band[0] - 58)
    bot = min(Image.open(os.path.join(SCANS, photo + '.jpg')).height,
              band[1] + 58)
    im = Image.open(os.path.join(SCANS, photo + '.jpg'))
    im = im.crop((100, top, im.width - 80, bot))
    scale = 1400 / im.width
    im = im.resize((1400, int(im.height * scale)), Image.LANCZOS)
    path = os.path.join(OUT, 'img', row_id + '.jpg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.convert('RGB').save(path, quality=88)
    return y, band


def context_snippet(page_text, row_id):
    """A short transcription context around the row's anchor."""
    anchor = ANCHOR.get(row_id, '')
    if not anchor:
        return ''
    probe = re.sub(r'[\[\]~?/\\\\]', '.', anchor)
    m = re.search(probe.replace(' ', '.{0,3}'), page_text)
    if not m:
        for w in anchor.split():
            probe = re.sub(r'[\[\]~?/\\\\]', '.', w)
            m = re.search(probe, page_text)
            if m:
                break
    if not m:
        return ''
    a, b = max(0, m.start() - 130), min(len(page_text), m.end() + 130)
    return '…' + page_text[a:b].strip() + '…'


def main():
    check_only = '--check' in sys.argv
    os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
    seq = corpus_pages()
    texts = {}
    cur = None
    for line in open(CORPUS, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('[PAGE '):
            cur = line[6:-1]
            texts.setdefault(cur, '')
        elif cur and not line.startswith('[DOC'):
            texts[cur] = (texts[cur] + ' ' + line).strip()
    rows_meta = []
    for row_id, section, page, y_hint, question, options, note in ROWS:
        if page:
            y, band = crop_for(row_id, page, y_hint, texts.get(page, ''))
        else:
            y = band = None
        rows_meta.append({
            'id': row_id, 'section': section, 'page': page,
            'y': y, 'question': question, 'options': options, 'note': note,
            'context': context_snippet(texts.get(page, ''), row_id),
        })
    print('%d rows; crops in %s' % (len(rows_meta), OUT))
    if check_only:
        # one contact sheet: every crop as a thumbnail, labelled
        from PIL import Image, ImageDraw
        thumbs = []
        for r in rows_meta:
            if not r['page']:
                continue
            im = Image.open(os.path.join(OUT, 'img', r['id'] + '.jpg'))
            im.thumbnail((460, 240))
            thumbs.append((r['id'], r['page'], r['y'], im))
        cols = 3
        cw, ch = 480, 300
        rowsn = (len(thumbs) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * cw, rowsn * ch), 'white')
        d = ImageDraw.Draw(sheet)
        for i, (rid, page, y, im) in enumerate(thumbs):
            x, yy = (i % cols) * cw, (i // cols) * ch
            sheet.paste(im, (x + 8, yy + 28))
            d.text((x + 8, yy + 6), '%s  %s y=%d' % (rid, page, y), fill='black')
        sheet.save(os.path.join(OUT, 'contact_sheet.png'))
        print('contact sheet ->', os.path.join(OUT, 'contact_sheet.png'))
        return
    # the static page
    with open(os.path.join(UNIT, 'intake', 'sheet_template.html'),
              encoding='utf-8') as f:
        tpl = f.read()
    body = []
    section = None
    for r in rows_meta:
        if r['section'] != section:
            section = r['section']
            body.append('<h2>%s</h2>' % html.escape(section))
        opts = ''.join(
            '<button class="opt" data-id="%s" data-v="%s">%s</button>' % (
                r['id'], html.escape(o, quote=True), html.escape(o))
            for o in r['options'])
        img = ('<img loading="lazy" src="img/%s.jpg" alt="line picture">'
               % r['id']) if r['page'] else ''
        wrongline = ('<button class="wrongline" data-id="%s">'
                     'The picture shows the wrong line (the crop was placed '
                     'by machine and unchecked)</button>' % r['id']) if r['page'] else ''
        body.append('''<div class="row" id="{id}">
<h3>{id}</h3>
{img}
{wrongline}
<p class="q">{q}</p>
<p class="ctx">{ctx}</p>
<div class="opts">{opts}</div>
<input class="free" type="text" placeholder="or write the reading">
<p class="note">{note}</p>
</div>'''.format(id=html.escape(r['id']), img=img, wrongline=wrongline,
                 q=html.escape(r['question']),
                 ctx=html.escape(r['context']), opts=opts,
                 note=html.escape(r['note'])))
    page_html = (tpl.replace('<!--ROWS-->', '\n'.join(body))
                 .replace('<!--COUNT-->', str(len(rows_meta))))
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8',
              newline='\n') as f:
        f.write(page_html)
    with open(os.path.join(OUT, 'rows.json'), 'w', encoding='utf-8',
              newline='\n') as f:
        json.dump(rows_meta, f, ensure_ascii=False, indent=1)
    print('sheet ->', os.path.join(OUT, 'index.html'))


if __name__ == '__main__':
    main()
