# -*- coding: utf-8 -*-
"""Cut the archive's supplied French transcript into one file per page.

    python units/agad118501169/intake/transcripts.py [--with-157]

The transcript in raw_dir ("...(French).md") carries [N] page marks that
fall on the manuscript's own page breaks (verified against every scan; see
review/agad118501169/split_proposal.md). This script turns it into
transcriptions/<page_id>.txt, page ids by pencil number and side of the
opening: even pages are the left side of an opening (a1), odd pages the
right (a2) - which is why the missing first page 157 is a2, the right side
of an opening whose left half belongs to the preceding file.

Rulings of the editor of 2026-10-21 that this script carries out:

  - The heading of p. 157 stands as the transcript gives it, heavily
    corrected in the manuscript, garbles included (markdown ** stripped;
    the corpus is plain text).
  - Block A (the Hohenlohe action of 1808), which the transcript jumps,
    is restored on p. 159 - it is plain manuscript text.
  - The manuscript's crossed-out text is not recorded. Block C ("Le
    Tribunal ayant pris en consideration qu'il ne s'agissait plus ici ...
    s'est reconnu competent.") and the lead "En statuant ensuite sur le
    fond et considerant :" on p. 160 are struck and dropped. The
    surviving text flows "Le Tribunal ayant pris en consideration: 1o que
    dans l'affaire ...", so p. 159 ends with the lead line and p. 160
    begins at "1o que dans".
  - p. 199 (blank) has no page file at all.

The p. 159 closing line is not in the transcript; its wording follows the
struck block C's own opening ("Le Tribunal ayant pris en consideration"),
which the surviving lead must have read; it is settled word for word
against the scan at the correction pass.

Page 157's text is emitted only with --with-157, when its scan has
arrived; until then the corpus starts at p. 158, mid-sentence, which the
document-boundaries pass will put right.
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, ROOT)
import unitlib

unitlib.utf8_stdout()
UNIT_SLUG = 'agad118501169'
UNIT = unitlib.one_unit(UNIT_SLUG)
OUT = os.path.join(UNIT.dir, 'transcriptions')

# The 1808 Hohenlohe passage, restored from the scan; wording as legible now,
# settled at the correction pass (split proposal section 5).
BLOCK_A = (
    "En 1808 le Prince Hohenlohe voulant rentrer en possession des dits "
    "biens intenta action devant le Tribunal de Kalisz contre la Dame "
    "Miączyńska. — Le Tribunal de Kalisz ayant allégué que l'examen des "
    "actes de l'autorité Souveraine n'est pas du ressort du Tribunal et que "
    "l'objet en question a été décidé par l'autorité Suprême, s'est "
    "reconnu incompétent pour juger cette affaire. —")

# The lead the struck block C opens with; p. 159's last line.
TAIL_159 = "Le Tribunal ayant pris en considération:"

# Readings corrected against the scan, on the editor's ruling: (pencil page,
# as the archive transcript has it, as the manuscript has it, why). Applied
# after the page texts are cut; each is logged here as the record of the
# change. A re-run applies them again only to the freshly cut transcript.
ROWS = [
    (179, 'Godtewski', 'Godłewski',
     'the manuscript writes the Polish crossed l; the name is Godłewski, '
     'which is a Polish surname, where Godtewski is not (the editor, '
     '2026-10-21; the archive translator marks the reading uncertain)'),
]


def page_id(n):
    """Pencil page number -> page id. Even pages open an opening (a1)."""
    return '%04d_%s' % (n, 'a1' if n % 2 == 0 else 'a2')


def unescape(s):
    """The transcript is markdown-escaped: \\[157\\], 1834\\. and friends."""
    return s.replace('\\[', '[').replace('\\]', ']').replace('\\.', '.')


def read_pages():
    srcs = glob.glob(os.path.join(UNIT.raw_dir, '*French*.md'))
    if len(srcs) != 1:
        raise SystemExit(f'expected one French transcript in {UNIT.raw_dir}, '
                         f'found {len(srcs)}')
    pages, current = {}, None
    for raw in io.open(srcs[0], encoding='utf-8'):
        line = unescape(raw.rstrip('\n')).rstrip()
        m = re.fullmatch(r'\[(\d+)\]', line.strip())
        if m:
            current = int(m.group(1))
            pages[current] = []
            continue
        if current is None:
            if line.strip():
                raise SystemExit(f'text before the first page mark: {line!r}')
            continue
        # the transcript bolds the report's heading; the corpus is plain text
        pages[current].append(line.replace('**', ''))
    return pages


def main():
    with_157 = '--with-157' in sys.argv
    pages = read_pages()
    got = sorted(pages)
    want = list(range(157, 199))        # 157..198; 199 is blank, excluded
    if got != want:
        raise SystemExit(f'page marks {got[0]}..{got[-1]} ({len(got)} pages) '
                         f'!= expected 157..198')

    # p. 159: block A back in, and the surviving lead line at the end.
    p159 = pages[159]
    at = next(i for i, p in enumerate(p159)
              if p.startswith("de la Somme de 30.000 écus"))
    p159[at + 1:at + 1] = ['', BLOCK_A]
    p159.extend(['', TAIL_159])

    # p. 160: the crossed-out lead goes; the page begins at "1° que dans".
    p160 = pages[160]
    while p160 and not p160[0].strip():
        del p160[0]
    if not p160[0].startswith('En statuant ensuite sur le fond'):
        raise SystemExit(f'p. 160 does not open with the struck lead: {p160[0]!r}')
    del p160[0]
    while p160 and not p160[0].strip():
        del p160[0]

    if not with_157:
        del pages[157]

    os.makedirs(OUT, exist_ok=True)
    for n in sorted(pages):
        pid = page_id(n)
        lines, out = [], pages[n]
        for l in out:               # a blank run is one blank line
            if not l.strip() and (not lines or not lines[-1].strip()):
                continue
            lines.append(l)
        for pn, was, now, _why in ROWS:     # corrections against the scan
            if pn != n:
                continue
            hits = [i for i, l in enumerate(lines) if was in l]
            assert len(hits) == 1, (pid, was, len(hits))
            lines[hits[0]] = lines[hits[0]].replace(was, now)
            print(f'  corrected on {pid}: {was} -> {now}')
        text = '\n'.join(lines).strip('\n') + '\n'
        with io.open(os.path.join(OUT, pid + '.txt'), 'w',
                     encoding='utf-8', newline='\n') as f:
            f.write(text)
        first = next(l for l in pages[n] if l.strip())
        print(f'  {pid}  {first[:60]}')
    n = len(pages)
    print(f'\nwrote {n} page file(s) to {os.path.relpath(OUT, ROOT)}'
          + (' (incl. 0157_a2)' if with_157 else ' (p. 157 waits for its scan; '
             're-run with --with-157 then)'))
    print('next: python pipeline/intake/import_pages.py --unit ' + UNIT_SLUG
          + ' --pages-only')


if __name__ == '__main__':
    main()
