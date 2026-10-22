# -*- coding: utf-8 -*-
"""Tesseract OCR for the project, on the editor's machine.

    from pipeline.ocr import read, words
    text = read('scan.png')            # the page's text, Polish by default
    for w in words('scan.png'): ...    # every word with its box and confidence

Installed 2026-10-22 at the editor's word ("Can you install pytesseract or the
needed tesseract solution so that the project has access to this from now on?"),
when the Dziennik Poznanski clipping of 7 August 1937 was read: the engine is
Tesseract 5.5.3 (winget, tesseract-ocr.tesseract, C:\\Program Files\\Tesseract-OCR),
the Polish model was fetched from tessdata_best into
%LOCALAPPDATA%\\Tesseract\\tessdata (the installer's own tessdata carries English
only). Neither is on PATH, so this module looks them up itself.

The tessdata directory is chosen by which language files it holds: the
LOCALAPPDATA one first (best + standard pol), the install's own second. Pass
`lang` ('pol', 'pol-std', 'deu', 'eng', ...) to read() or words(); psm 6
("assume a uniform block of text") suits a newspaper column, psm 4 the looser
kind. Returns are str/UTF-8; errors raise, because a silent empty page is the
worse outcome.
"""
import os
import subprocess

TIF = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
TIF_ALT = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs',
                       'Tesseract-OCR', 'tesseract.exe')
DATA = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tesseract', 'tessdata')


def tesseract():
    """The engine's path, or the error to raise."""
    for p in (TIF, TIF_ALT):
        if os.path.isfile(p):
            return p
    if os.environ.get('TESSDATA_PREFIX'):
        return 'tesseract'
    raise RuntimeError(
        'tesseract.exe not found: install it with '
        '`winget install tesseract-ocr.tesseract` or put it on PATH')


def tessdata(lang):
    """The tessdata directory that holds `lang`, best first, or None."""
    cand = []
    if os.path.isdir(DATA):
        cand.append(DATA)
    base = os.path.dirname(tesseract())
    cand.append(os.path.join(base, 'tessdata'))
    for d in cand:
        if os.path.isfile(os.path.join(d, lang + '.traineddata')):
            return d
    return None


def _run(img, lang, psm, extra):
    exe = tesseract()
    env = dict(os.environ)
    d = tessdata(lang)
    if d:
        env['TESSDATA_PREFIX'] = d
    args = [exe, img, 'stdout', '-l', lang, '--psm', str(psm)] + extra
    r = subprocess.run(args, capture_output=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode('utf-8', 'replace').strip() or
                           f'tesseract exited {r.returncode}')
    return r.stdout.decode('utf-8', 'replace')


def read(img, lang='pol', psm=6):
    """The page's text, one line of output per line found."""
    return _run(img, lang, psm, []).replace('\r\n', '\n')


def words(img, lang='pol', psm=6):
    """Every word as (left, top, width, height, confidence, text).

    The TSV comes as a stream, so a list; the page's own coordinates are kept
    (a crop's box is then `im.crop((left, top, left+width, top+height))`).
    """
    out = []
    tsv = _run(img, lang, psm, ['-c', 'tessedit_create_tsv=1'])
    for line in tsv.split('\n'):
        f = line.rstrip('\r\n').split('\t')
        if len(f) < 12 or not f[0].strip().isdigit() or not f[11].strip():
            continue
        out.append((int(f[6]), int(f[7]), int(f[8]), int(f[9]),
                    float(f[10]), f[11]))
    return out
