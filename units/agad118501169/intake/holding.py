# -*- coding: utf-8 -*-
"""Cut this unit's openings into pages, and show the editor the fold page.

    python units/agad118501169/intake/holding.py            # both steps
    python units/agad118501169/intake/holding.py --sheet    # the fold page only
    python units/agad118501169/intake/holding.py --crop     # cut pages only

--sheet writes review/agad118501169/folds/index.html: the court book's fold
page (pipeline/intake/courtbook.py fold_sheet), the same page other
holdings review their splits on - the whole opening, arrow keys to page
through, the red fold line dragged onto the fold, and the sheet TURNED
with the mouse wheel or shift-drag (or [ and ]) where a fold was
photographed at a slant, plus the green page-edge lines. "Save" offers
folds_agad118501169.json; hand it to

    python pipeline/intake/courtbook.py folds agad118501169 <that file>

which copies it to intake/folds.json, re-runs this script (--crop --sheet),
restages the pages and remakes the web images (courtbook.take_folds).

--crop cuts the pages out of the raw scans (courtbook.cut): turned where
the editor turned a sheet, trimmed to the page edges where they were set,
each half +/- 30px of overlap round the fold, named for its page id and
left in raw_dir/processed/ for stage_pages.py. The two halves that are not
ours - p. 156 of the preceding file (left of the 108 opening) and the blank
p. 199 - go to processed/_not_staged/.

The fold proposals below are where the split_spreads detector cut each
opening when the unit was first split (every cut high confidence); the
editor's placements in intake/folds.json, if present, override them
(courtbook.placed), and the script's numbers stay as the first proposal.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, ROOT)
import unitlib
import courtbook

unitlib.utf8_stdout()
UNIT = unitlib.one_unit('agad118501169')
RAW = UNIT.raw_dir

# (raw scan file, fold x in pixels of the scan, left page id, right page id).
# Page ids carry the pencil page number and the side of the opening: even
# pages are the left side of an opening (a1), odd the right (a2) - which is
# why p. 157, the report's first page, is the RIGHT side (a2) of the 108
# opening, whose left half is p. 156 of the preceding file. A page id given
# to the wrong half or a blank half is named anyway and listed in SKIP, so
# cut() sets it aside in processed/_not_staged/ rather than dropping it
# silently.
SCANS = [
    ('1_185_0_1_169_108_98320255.jpg', 1745,
     '1_185_0_1_169_0156_left', '1_185_0_1_169_0157_a2'),
    ('1_185_0_1_169_98320256.jpg', 1733,
     '1_185_0_1_169_0158_a1', '1_185_0_1_169_0159_a2'),
    ('1_185_0_1_169_98320258.jpg', 1733,
     '1_185_0_1_169_0160_a1', '1_185_0_1_169_0161_a2'),
    ('1_185_0_1_169_98320260.jpg', 1883,
     '1_185_0_1_169_0162_a1', '1_185_0_1_169_0163_a2'),
    ('1_185_0_1_169_98320263.jpg', 1945,
     '1_185_0_1_169_0164_a1', '1_185_0_1_169_0165_a2'),
    ('1_185_0_1_169_98320266.jpg', 1993,
     '1_185_0_1_169_0166_a1', '1_185_0_1_169_0167_a2'),
    ('1_185_0_1_169_98320268.jpg', 1920,
     '1_185_0_1_169_0168_a1', '1_185_0_1_169_0169_a2'),
    ('1_185_0_1_169_98320272.jpg', 1944,
     '1_185_0_1_169_0170_a1', '1_185_0_1_169_0171_a2'),
    # 98320273: a second exposure of 98320272 (identical pages, different
    # file); it sits in raw_dir/duplicates/ and is not cut at all.
    ('1_185_0_1_169_98320274.jpg', 1727,
     '1_185_0_1_169_0172_a1', '1_185_0_1_169_0173_a2'),
    ('1_185_0_1_169_98320275.jpg', 1889,
     '1_185_0_1_169_0174_a1', '1_185_0_1_169_0175_a2'),
    ('1_185_0_1_169_98320276.jpg', 1883,
     '1_185_0_1_169_0176_a1', '1_185_0_1_169_0177_a2'),
    ('1_185_0_1_169_98320278.jpg', 1752,
     '1_185_0_1_169_0178_a1', '1_185_0_1_169_0179_a2'),
    ('1_185_0_1_169_98320279.jpg', 1739,
     '1_185_0_1_169_0180_a1', '1_185_0_1_169_0181_a2'),
    ('1_185_0_1_169_98320280.jpg', 1903,
     '1_185_0_1_169_0182_a1', '1_185_0_1_169_0183_a2'),
    ('1_185_0_1_169_98320281.jpg', 1896,
     '1_185_0_1_169_0184_a1', '1_185_0_1_169_0185_a2'),
    ('1_185_0_1_169_98320283.jpg', 1890,
     '1_185_0_1_169_0186_a1', '1_185_0_1_169_0187_a2'),
    ('1_185_0_1_169_98320284.jpg', 1896,
     '1_185_0_1_169_0188_a1', '1_185_0_1_169_0189_a2'),
    ('1_185_0_1_169_98320285.jpg', 1883,
     '1_185_0_1_169_0190_a1', '1_185_0_1_169_0191_a2'),
    ('1_185_0_1_169_98320286.jpg', 1883,
     '1_185_0_1_169_0192_a1', '1_185_0_1_169_0193_a2'),
    ('1_185_0_1_169_98320287.jpg', 1870,
     '1_185_0_1_169_0194_a1', '1_185_0_1_169_0195_a2'),
    ('1_185_0_1_169_98320288.jpg', 1870,
     '1_185_0_1_169_0196_a1', '1_185_0_1_169_0197_a2'),
    ('1_185_0_1_169_98320289.jpg', 1745,
     '1_185_0_1_169_0198_a1', '1_185_0_1_169_0199_blank'),
]

# Not pages of this file: the left half of the 108 opening (p. 156, the
# preceding file's matter) and the blank p. 199 (editor, 2026-10-21).
SKIP = {'1_185_0_1_169_0156_left', '1_185_0_1_169_0199_blank'}


# --------------------------------------------------------------------------- #
# The English, from the archive's own translation
# --------------------------------------------------------------------------- #

# The passage the archive's transcript jumps (the Hohenlohe action of 1808,
# restored in the corpus on p. 159 from the scan): translated for this edition
# in the archive translation's own terms.
BLOCK_A_EN = (
    "In 1808, Prince Hohenlohe, wishing to re-enter into possession of the "
    "said property, brought an action before the Tribunal of Kalisz against "
    "the Dame Miączyńska. — The Tribunal of Kalisz, having alleged that the "
    "examination of the acts of the Sovereign authority was not within the "
    "Tribunal's province, and that the matter in question had been decided by "
    "the Supreme Authority, declared itself incompetent to judge the case. —")

# The surviving lead of the considered grounds: manuscript p. 159's last line,
# which continues on p. 160 at "1° que dans l'affaire". The archive
# translation's p. 160 opens "Then, ruling on the merits and considering:",
# a rendering of the struck-out lead the corpus does not carry.
TAIL_159_EN = "The Tribunal, having taken into consideration:"


def english():
    """The archive translation's pages, one per corpus page, in order.

    The file is cut at its [p. N] marks, which fall on the manuscript's own
    page breaks like the French transcript's; the Translator's Notes and the
    Glossary at the end are the archive translator's apparatus and are left
    out (editor, 2026-10-21), and with them the superscript note marks in the
    body. Page 199 is blank and has no page here.
    """
    import glob
    import re
    import unicodedata
    f = glob.glob(glob.escape(RAW) + '\\*English*.md') or \
        glob.glob(os.path.join(glob.escape(RAW), '*English*.md'))
    assert len(f) == 1, f
    s = io.open(f[0], encoding='utf-8-sig').read().replace('\r\n', '\n')

    cut = re.search(r"(?m)^#+\s*\**\s*Translator's Notes", s)
    assert cut, 'no Translator\'s Notes heading found'
    s = s[:cut.start()]

    pages, current = {}, None
    for raw_line in s.split('\n'):
        line = courtbook.plain(raw_line).rstrip()
        m = re.fullmatch(r'\[p\. (\d+)( — blank)?\]', line.strip())
        if m:
            n = int(m.group(1))
            if n == 199:
                break           # blank last page: nothing after it is ours
            current = n
            pages[n] = []
            continue
        if current is None:
            continue            # the file's own title and source line
        if not line.strip():
            continue
        # superscript note marks (¹, ², ¹⁰ ...) pointed at the dropped notes
        line = re.sub(r'[\u00b9\u00b2\u00b3\u2070-\u2079]+', '', line)
        pages[current].append(line.strip())

    assert sorted(pages) == list(range(157, 199)), sorted(pages)

    # The corpus's p. 159 keeps the Hohenlohe passage the transcript omits,
    # and ends with the surviving lead; p. 160 begins at the first ground.
    pages[159][1:1] = [BLOCK_A_EN]
    pages[159].append(TAIL_159_EN)
    assert pages[160][0].startswith('Then, ruling on the merits'), pages[160][0]
    del pages[160][0]
    assert pages[160][0].startswith('1° that in the matter at issue'), pages[160][0]

    # Readings corrected against the scan, on the editor's ruling, matching
    # the transcription's corrections (transcripts.py ROWS).
    FIXED = [('that of Sieur Godtewski', 'that of Sieur Godłewski',
              'the manuscript writes the Polish crossed l; the name is '
              'Godłewski (the editor, 2026-10-21)')]
    for was, now, _why in FIXED:
        hits = [k for k in pages if any(was in l for l in pages[k])]
        assert len(hits) == 1, (was, hits)
        k = hits[0]
        pages[k] = [l.replace(was, now) for l in pages[k]]
        print(f'  corrected on p. {k}: {was} -> {now}')

    # corpus page k = pencil page 156 + k (0157_a2 is the document's page 1)
    out = []
    for k in range(1, 43):
        out.append('\n\n'.join(pages[156 + k]))

    # the carry chain: each page opens where the previous one ends
    # (corpus page k = pencil page 156 + k)
    chain = [(2, 'by her second Miączyńska'), (3, 'of the sum of 30,000 écus'),
             (4, '1° that in the matter at issue'),
             (42, 'of Instruction is of opinion')]
    for k, first in chain:
        assert out[k - 1].startswith(first), (k, out[k - 1][:60])
    assert out[41].rstrip().endswith('[signed] Faltz'), out[41][-60:]
    return {1: out}


# --------------------------------------------------------------------------- #
# Summaries, written in session and claim-checked (intake/claim_check.yml)
# --------------------------------------------------------------------------- #

S = {
 1: ('Bericht der Instruktionskommission des Staatsrats des Königreichs Polen '
     'über den Kompetenzkonflikt, den die Finanz- und Schatzkommission, auf '
     'Beschluß des alten Verwaltungsrats vom 4. Oktober 1829 ermächtigt, im '
     'Juli 1830 dem Staatsrat vorgelegt hat: gegen das Urteil, durch das das '
     'Oberste Gericht die Forderung von 30.000 Écus des Karol Weigel, des '
     'Zessionars des Gläubigers Grotowski, aus den Hypothekenregistern des '
     'Guts Trąbczyn der Michalina Miączyńska streichen ließ. Der Bericht '
     'verfolgt den Rechtsweg der Sache von der Konfiskation Trąbczyns 1796 '
     'zugunsten des Prinzen Hohenlohe-Ingelfingen und dem 1800 auf das Gut '
     'eingetragenen Darlehen an: den Beschluß der Regierungskommission vom '
     '5. Juni 1807, der das Gut an Michalina Prusimska, die Tochter des '
     'letzten polnischen Besitzers, zurückgab; Weigels Eintragung als '
     'Zessionar 1808 und seine Klage von 1810 auf die aufgelaufenen Zinsen '
     'vor dem Tribunal in Kalisz, das die Forderung aus den Registern '
     'streichen ließ; den Beschluß des Appellationsgerichts vom '
     '9. November 1820 und das endgültige Urteil des Obersten Gerichts von '
     'Juli 1826, das das Kalischer Urteil bestätigte; die Vorstellungen '
     'beider Parteien bei ihren Regierungen, den Verkehr zwischen Warschau '
     'und Berlin und die oberste Entscheidung vom 4. September 1821, daß der '
     'Rechtsweg in der Sache nicht gehemmt werden solle. Die '
     'Instruktionskommission nimmt die drei Gründe der Finanzkommission für '
     'einen Kompetenzkonflikt einzeln vor, hält sie gegen die vier '
     'Bedingungen, die die Organisation des Staatsrats an einen solchen '
     'Konflikt setzt, und findet, daß kein Kompetenzkonflikt bestanden hat '
     'oder besteht und daß der Rekurs in der Sache eine Kassationsbeschwerde '
     'an ein Gericht ist, als das der Staatsrat nach seiner Organisation '
     'nicht gilt; sie rät, das Begehren als auf keinem Rechtssatz beruhend '
     'abzuweisen, und reicht einen entsprechenden Gesetzentwurf ein. '
     'Vorgetragen in der Sitzung vom 28. Oktober 1834, unterzeichnet vom '
     'Präsidenten Faltz.',
     'Report of the Commission of Instruction of the Council of State of the '
     'Kingdom of Poland on the conflict of jurisdiction that the Commission '
     'of Finances and the Treasury, authorised by the former Council of '
     'Administration on 4 October 1829, laid before the Council of State in '
     'July 1830: against the judgment by which the Supreme Tribunal had the '
     'claim of 30,000 écus of Karol Weigel, assignee of the creditor '
     'Grotowski, struck from the mortgage registers of the Trąbczyn estate of '
     'Michalina Miączyńska. The report retraces the judicial course of the '
     'affair from the confiscation of Trąbczyn in 1796 to Prince '
     'Hohenlohe-Ingelfingen and the loan inscribed on the estate in 1800: the '
     'decree of 5 June 1807 by which the Governing Commission restored the '
     'estate to Michalina Prusimska, the daughter of the last Polish owner; '
     'Weigel\'s inscription as assignee in 1808 and his suit of 1810 for the '
     'accumulated interest before the Tribunal of Kalisz, which had the claim '
     'struck from the registers; the ruling of the Court of Appeal of '
     '9 November 1820 and the definitive sentence of the Supreme Tribunal of '
     'July 1826 confirming the Kalisz judgment; the petitions of both parties '
     'to their governments, the exchanges between Warsaw and Berlin, and the '
     'Supreme decision of 4 September 1821 that the judicial course in the '
     'case was not to be obstructed. The Commission of Instruction takes the '
     'Finance Commission\'s three grounds for a conflict of jurisdiction one '
     'by one, sets them against the four conditions the organisation of the '
     'Council of State requires of one, and finds that no conflict of '
     'jurisdiction existed or exists, and that the recourse is in substance '
     'an appeal in cassation to a court the Council of State is not by its '
     'organisation; it advises that the demand be set aside as based on no '
     'legal principle, and hands in a draft decree to that effect. Presented '
     'at the session of 28 October 1834, signed by the president, Faltz.'),
}

HOW = ('the archive\'s own transcript and English translation; the transcript\n'
       '# extended from the scans where it omits manuscript text, the\n'
       '# manuscript\'s crossed-out passages not recorded; the summaries written\n'
       '# in the working session (intake/holding.py, 2026-10-21).')


def main():
    arg = sys.argv[1:]
    steps = [a for a in arg if a in ('--crop', '--sheet', '--english',
                                     '--cache', '--summaries')]
    if not steps:
        steps = ['--crop', '--sheet']
    scans = courtbook.placed(HERE, SCANS)
    if getattr(scans, 'mine', ()):
        print('%d fold(s) placed by the editor override the proposals'
              % len(scans.mine))
    if '--sheet' in steps:
        courtbook.fold_sheet(ROOT, UNIT.slug, UNIT['ref'], RAW, scans, skip=SKIP)
    if '--crop' in steps:
        courtbook.cut(RAW, scans, skip=SKIP)
        print('next: python pipeline/intake/stage_pages.py --unit %s --force'
              % UNIT.slug)
    if '--english' in steps:
        tdir = os.path.join(HERE, 'translation')
        os.makedirs(tdir, exist_ok=True)
        for n, texts in sorted(english().items()):
            courtbook.write_doc_yml(os.path.join(tdir, 'doc%d.yml' % n), texts)
    if '--cache' in steps:
        courtbook.save_cache(ROOT, UNIT.slug, os.path.join(HERE, 'translation'))
        print('next: python pipeline/translate/publish_translations.py '
              '--unit %s' % UNIT.slug)
    if '--summaries' in steps:
        courtbook.write_summaries(ROOT, UNIT.dir, UNIT.slug, UNIT['ref'],
                                  S, HOW)


if __name__ == '__main__':
    main()
