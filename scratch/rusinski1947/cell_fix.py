# -*- coding: utf-8 -*-
"""Cell-noise fixer: for every flagged annex cell, re-OCR the cell's
print crop under several configs and pick the best-scoring reading.

Scoring: date/number/siglum pattern compliance + draft-vocabulary
token ratio + junk-char penalty. The strip's raw row text (editor-
verified) provides a per-row reference lexicon: candidate tokens
matching it get a bonus. Deterministic post-fix: the month-year glue
('XI1720' -> 'XI 1720'). Output: annex_md_fixed.json + a report."""
import sys, os, json, re, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annex_cells import detect, fit
from PIL import Image, ImageOps

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TMP = os.path.join(OCR, 'cell_tmp.png')

DRAFT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
         r'\rusinski1947\literature\rusinski1947\original.md')

DATE = re.compile(r'^\d{1,2}\s+[IVX]+\s+\d{4}$')
YEAR = re.compile(r'^\d{4}$')
NUM = re.compile(r'^\d{1,4}$')
SIGLUM = re.compile(r'^(AW\.|Rel\.|AGH|AM\.|Dom\.|Tp\.|Tod\.|Tołł\.|'
                    r'Verz|Kl\.|Kat\.|Q\b|GE\b|MGd?\b|MP\b|Szk\.|'
                    r'Kośc\.|Lustr\.|Inser\.|Decr\.|Werner|Goldmann|'
                    r'Cieplucha|Rutkowski|Bór\.|VO\b|OWK|O\s*83|TKS|'
                    r'Tb\.|St\.|M\.|Parochia|ZHGP|Bir|Kniat|Inscr\.|'
                    r'Repertorium|tamże|Por\.|Tax|Repert\.|l\s*\.\s*b|'
                    r'Posener|Skorowidz|Brak|AGH\.)')


def vocab():
    t = open(DRAFT, encoding='utf-8').read()
    vs = set(re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}', t))
    vs |= {'AW.', 'Rel.', 'AGH', 'AM.', 'Dom.', 'Tp.', 'Tod.', 'Tołł.',
           'Verz', 'Kl.', 'Kat.', 'fol.', 'vol.', 's.', 't.', 'nr',
           'r.', 'maj.', 'sąd', 'sąd.', 'współ.', 'pow.', 'par.',
           'XI', 'XII', 'XIII', 'IV', 'VII', 'VIII', 'IX', 'X', 'VI',
           'III', 'II', 'V', 'I', 'Ol.', 'OI.', 'OI', 'ol.', 'OI.',
           'wieś', 'las', 'zarośla', 'łąki', 'grunt', 'Sołtys'}
    return vs


VOCAB = None


def read_cfg(c, lang, psm):
    c.save(TMP)
    try:
        return read(TMP, lang=lang, psm=psm).strip()
    except Exception:
        return ''


def ocr_variants(im, box):
    x0, y0, x1, y1 = box
    c0 = im.crop((x0, y0, x1, y1))
    outs = []
    for sc in (3, 4):
        c = c0.resize((int(c0.size[0] * sc), int(c0.size[1] * sc)),
                      Image.LANCZOS)
        ca = ImageOps.autocontrast(c)
        for img in (c, ca):
            for lang in ('pol', 'deu'):
                for psm in (6, 7):
                    t = read_cfg(img, lang, psm)
                    if t and t not in outs:
                        outs.append(t)
    return outs


def clean(txt):
    t = txt.replace('|', ' ').replace('¦', ' ')
    t = re.sub(r'([a-ząćęłńóśźżIVX])- ([a-ząćęłńóśźż])', r'\1\2', t)
    toks = []
    for tok in t.split(' '):
        core = tok.strip(' .,;:()[]')
        if core and re.fullmatch(r'[=_\-—~·]+', core):
            continue
        toks.append(tok)
    return re.sub(r'\s+', ' ', ' '.join(toks)).strip(' .,;:-_=+*')


def score(txt, col, row_lex):
    """Higher = better-formed."""
    if not txt:
        return -10.0
    s = 0.0
    toks = txt.split(' ')
    if col == 7:
        t2 = txt.replace('  ', ' ')
        if DATE.match(t2):
            return 20.0
        if YEAR.match(txt.strip()):
            return 16.0
        if re.match(r'^\d{1,2}\s*[IVX]+\s*\d{0,4}$', t2):
            s += 6
        if re.match(r'^\d{1,2}[IVX]+\d*$', t2):
            s += 2  # glue - fixable deterministically
    if col == 6:
        if SIGLUM.match(txt):
            s += 5
    for tok in toks:
        core = tok.strip(' .,;:()[]|')
        if not core:
            continue
        letters = sum(1 for c in core if c.isalpha())
        if letters and letters < len(core) * 0.6:
            s -= 4
            continue
        if re.search(r'[=<>_%~§]{1}|--|—{2,}|\*{2,}', core):
            s -= 4
            continue
        if core in row_lex:
            s += 2.0
        elif core.lower() in VOCAB or core in VOCAB:
            s += 1.0
        elif re.match(r'^\d+$', core):
            s += 1.0
        else:
            s -= 0.5
    return s


def glue(txt):
    txt = re.sub(r'([IVX])(\d{4})', r'\1 \2', txt)
    txt = re.sub(r'(\d{1,2})([IVX]+)(?=[\s,]|$)', r'\1 \2', txt)
    # the strip's l->I: a month group needs a leading day digit -
    # 'I XI 1751' is really '1 XI 1751' (the print's 1 with a serif
    # misread as the Roman I); but a genuine bare month exists too
    # ('I XI' = day 1) - keep I as-is, the digit-shape pass decides
    txt = re.sub(r'(\b\d\s*X)1(\d{3})\b', r'\1 \2', txt)  # X11757 glue
    txt = re.sub(r'\b([IVX]{2,})1(\d{3})\b', r'\1 \2', txt)
    return re.sub(r'\s+', ' ', txt).strip()


def main():
    global VOCAB
    VOCAB = vocab()
    md = json.load(open(os.path.join(OCR, 'annex_md.json'),
                        encoding='utf-8'))
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    tri = []
    for ln in open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
                   r'\noise1.txt', encoding='utf-8'):
        m = re.match(r"(\d+) r(\d+) c(\d+) ", ln)
        if m:
            tri.append((m.group(1), int(m.group(2)), int(m.group(3))))
    ims = {}
    rules_cache = {}
    fixes = {}
    report = []
    for n, num, ci in tri:
        if n not in ims:
            rows = at[n]['rows']
            nums = sorted(int(k) for k in rows if k.isdigit())
            y_lo = min(rows[str(k)]['y'][0] for k in nums)
            y_hi = max(rows[str(k)]['y'][1] for k in nums)
            im, runs = detect(n, y_lo, y_hi)
            got = fit(runs)
            rules = got[1] if got else runs
            ims[n] = im
            rules_cache[n] = rules
        im = ims[n]
        rules = rules_cache[n]
        bounds = rules + [rules[-1] + 120]
        rows = at[n]['rows']
        y0, y1 = rows[str(num)]['y']
        x0, x1 = int(bounds[ci]) + 6, int(bounds[ci + 1]) - 6
        raw = rows[str(num)].get('raw') or ''
        row_lex = set(re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{2,}',
                                 raw)) | {'—'}
        cands = [clean(t) for t in ocr_variants(
            im, (x0, y0 + 4, x1, y1 - 4))]
        # current value from md rows
        cur_row = [r for r in md[n]['rows'] if r['num'] == num][0]
        curv = cur_row['cells'][ci]
        cands = [c for c in cands if c]
        cands.append(glue(curv))
        scored = sorted(((score(c, ci, row_lex), c) for c in cands),
                        reverse=True)
        best_s, best = scored[0]
        cur_s = score(curv, ci, row_lex)
        changed = best != curv and best_s > cur_s + 0.5
        if changed:
            cur_row['cells'][ci] = best
            fixes.setdefault(n, []).append(
                {'num': num, 'col': ci, 'old': curv, 'new': best,
                 'gain': round(best_s - cur_s, 1)})
        report.append((n, num, ci, curv, best, round(best_s, 1),
                       round(cur_s, 1), changed))
    with open(os.path.join(OCR, 'annex_md_fixed.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(md, fh, ensure_ascii=False)
    with open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
              r'\cellfix.txt', 'w', encoding='utf-8') as fh:
        for rep in report:
            fh.write('%s r%s c%d\n  old %r\n  new %r  (s %s vs %s)%s\n'
                     % (rep[0], rep[1], rep[2], rep[3], rep[4], rep[5],
                        rep[6], ' CHANGED' if rep[7] else ''))
    print('flagged:', len(tri), 'changed:', sum(len(v) for v in
                                                fixes.values()))


def _rk(num):
    return str(num)


if __name__ == '__main__':
    main()
