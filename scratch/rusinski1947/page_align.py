# -*- coding: utf-8 -*-
"""page_align: band-read a page's body and align the band lines to the
structure2 line tops (fuzzy sequence alignment). Output per page:
  b# <top> | <band text>          (aligned)
  b# ?????? | <band text>         (no structure match)
  --- unmatched structure lines (no band text): top | text
This is the authoring view for MANUAL_ADD/MANUAL_DROP entries."""
import sys, os, io, json, re, difflib
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\align_tmp.png'


def fold(x):
    return re.sub(r'[^a-z0-9]', '', x.lower())


def align(band_lines, struct_lines):
    """Greedy monotonic alignment: for each band line (in order), find
    the next struct line with fold-ratio >= 0.5."""
    out = []
    si = 0
    for bl in band_lines:
        fb = fold(bl)
        if len(fb) < 8:
            out.append((None, bl))
            continue
        best = None
        for j in range(si, min(si + 4, len(struct_lines))):
            fs = fold(struct_lines[j]['text'])
            r = difflib.SequenceMatcher(None, fb[:60], fs[:60]).ratio()
            if best is None or r > best[0]:
                best = (r, j)
        if best and best[0] >= 0.5:
            out.append((struct_lines[best[1]]['top'], bl))
            si = best[1] + 1
        else:
            out.append((None, bl))
    return out


for n in sys.argv[1:]:
    s = json.load(open(os.path.join(OCR, 'structure2.json'),
                       encoding='utf-8'))
    page = s[n]
    ft = min(x['top'] for x in page['notes'])
    lines = sorted(page['lines'], key=lambda l: l['top'])
    body = [l for l in lines if l['top'] < ft]
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read()))
    im.load()
    W, H = im.size
    y0 = 560
    print('=========', n, 'body 560..%d' % ft)
    while y0 < ft - 50:
        y1 = min(ft - 20, y0 + 1800)
        c = im.crop((250, y0, W - 250, y1))
        c = c.resize((c.size[0] * 3, c.size[1] * 3), Image.LANCZOS)
        c.save(TMP)
        try:
            t = read(TMP, lang='pol', psm=4)
        except Exception as e:
            print('  band %d-%d ERR %s' % (y0, y1, str(e)[:60]))
            y0 = y1
            continue
        bl = [x.strip() for x in t.split('\n') if x.strip()]
        seg = [l for l in body if y0 - 30 <= l['top'] < y1 + 30]
        for top, bl_ in align(bl, seg):
            print('  b %5s | %s' % (top if top else '?????', bl_[:88]))
        y0 = y1
    print()
