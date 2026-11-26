# -*- coding: utf-8 -*-
"""APP 53/21/0/-/Pyzdry Gr.75: the editor's transcription of entry no. 39 into the edition.

    python units/app5321pyzdrygr75/intake/holding.py            # check
    ... --scans      web copies of the two page images (from the images the editor sent)
    ... --write      corpus.txt from intake/editor_latin.md (once)
    ... --correct    apply ROWS, the readings corrected against the images (once)
    ... --english    write translation/doc1.yml
    ... --cache      put it into the translation cache
    ... --summaries  write the summaries S everywhere they are kept

The volume is "Inscriptiones [protocollon] 1768-1781" (the editor, 2026-11-26: the
folder "Relationes [protocollon] 1768-1771" was a second copy of the same volume
and is deleted). The editor supplied two single-page images, leaf 19 recto and
verso (page ids 0019_a and 0019_b), no cutting needed, with their Latin and
English (intake/editor_latin.md, intake/editor_english.md, kept as received).

The check (2026-11-26). The text was read against the images by Claude from
enlarged strips, with a second reader working from the editor's text (a table of
differences) and two blind readers (one read the verso well, the other gave a
weak reading and was not relied on). Corrections are made only where the letters
or the grammar prove them (ROWS). Left as the editor has them and put to the
editor on a spot sheet: "Borram" (the page may read "Borrarum"), "erogatam [i?]"
(a smear), "iure" (the page may read "aere": from his own money), "ea
praedictis" ("ex"?), "Da[m/s?]" in "Actaque praesenti Da...", the docket's "in Per"
(the page may read "inter"), the first word of the interlinear line above line 10
of leaf 19 verso, and above all the PLACING of the two inserted lines: the
interlinear "... ab ejusdem summis capitalibus provenientibus &" carries a cross that
matches a cross in line 10 before "cessit" (the editor has it at the end), and the
foot line "Recognoscentem successoribus Prusimscianis instituto" carries a cross
that matches the cross after "per[tinente]" at the end of the signature line (the
editor has it before "cessit").

Struck-out words, not transcribed (the ruling of 2026-10-05): "per" after
"elaboratis" (leaf 19, line 6 of the entry), about three words after "Prusimski pro"
("usu seu conversione"), and "sibi" before "hasce" (leaf 19 verso, line 4).

The sitting heading on leaf 19 verso under the signature ("Actum in Advocatia
Pyzdrensi extra Civitatem sitta, Feria Sexta in Crastino Festi Nativitatis Beatissimae
Virginis Mariae anno Domini 1768 ob conflagrationem per hostem Patriae Die Undecima
Mensis Junij anno praesenti totius Civitatis ... Pyzdry et Ecclesiarum ... Autoritate
publicorum Castrensium Districtus Pyzdrensis") heads the entries from no. 40 on and is
not transcribed; the entry's own date comes from the Konin decree (rulings.yml).

Abbreviations. The editor's text marks them with "~" and the older holdings keep that
form. The ruling of 2026-11-22 (expand in square brackets) holds for holdings worked
on from now; the supplied letters in ROWS are bracketed, and the editor's "~" forms
stand until they rule how far to carry it over (TODO).
"""
import glob
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app5321pyzdrygr75'
REF = '53/21/0/-/Pyzdry Gr.75'
RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Inscriptiones [protocollon] 1768-1781 (53.21.0.-.Pyzdry Gr.75)")
DOCS = [(1, ['0019_a', '0019_b'])]
LEAF = {'0019_a': '19 recto', '0019_b': '19 verso'}
PREFIX = 'APP_53_21_0_Pyzdry_Gr_75'


def read_source():
    head, leaves = courtbook.read_leaves(os.path.join(HERE, 'editor_latin.md'))
    assert head == [] and [l for l, _ in leaves] == ['19', '19v'], (head, [l for l, _ in leaves])
    assert len(leaves[0][1]) == 1, leaves[0][1]
    # the verso: the entry's end, the signature line, the docket line under it
    assert len(leaves[1][1]) == 3 and leaves[1][1][1] == 'Jan Traholtz ręką trzymaną', leaves[1][1]
    return {(1, '0019_a'): leaves[0][1], (1, '0019_b'): leaves[1][1]}


# (page, text as transcribed, text as on the page, why)
ROWS = [
    ('0019_a', 'Manifestatione Recedendo e[dem?]ce~', 'Manifeste Recedendo &c[etera]',
     'the page has "Mnfte Recedendo &ce Recognovit": the abbreviated adverb and the &c of the formula, '
     'not a noun in the ablative'),
    ('0019_a', 'Imperialium Paulum Prusimski',
     'Imperialium Grossorum Tredecim, Fenicorum[?] sex per olim Magnificum Paulum Prusimski',
     'the editor\'s line jumps from "Imperialium" to "Paulum": the page has "Grossorum Tredecim, [?]icorum sex per '
     'olim Magnificum" between them (13 groschen and, it seems, 6 pfennigs after the 1,053 imperials). The editor read '
     '"sex" (2026-11-26) and could not settle the word before it (Ferricorum, Fenicorum, Fersicorum); Claude takes '
     '"Fenicorum[?]", the pfennig, because the sum runs in the series imperial, grosz, fenig and r/n are '
     'minim confusions'),
    ('0019_a', 'ea positam', 'expositam',
     'the line ends "ex-" with the word divided and continues "positam": "expositam" ... specificatam'),
    ('0019_a', 'Borram et sylvarum', 'Borrarum et sylvarum',
     'the editor (2026-11-26): Borrarum, as the page may read; the genitive plural matches "sylvarum"'),
    ('0019_a', 'erogatam [i?] partim', 'erogatam partim',
     'the editor (2026-11-26): there is no "i" after erogatam; the mark on the page is a smear'),
    ('0019_a', 'seorsivo[?]', 'se[?]rsivo',
     'the editor (2026-11-26): "se[?]rsivo" is their best reading of the word'),
    ('0019_a', 'proque sisce[?] ac commodo', 'proque sisc[e?] ac commodo',
     'the editor (2026-11-26): the word looks more like "sisc[e?] ac" than Claude\'s "usuq[ue]", which is withdrawn; '
     'the doubt mark is moved to the letter'),
    ('0019_a', 'manuali his ac Regestris', 'manualibus ac',
     'the page ends "manuali-bus ac" at the torn corner; "Regestris" stands at the head of leaf 19 verso '
     '(next row), not at the foot of this page'),
    ('0019_b', 'tum variis connotationibus', 'Regestris tum variis connotationibus',
     'the word before "tum variis" stands at the head of line 1 of the verso (read as "Regestris", '
     'abbreviated; the spelling is doubtful)'),
    ('0019_b', 'ea praedictis summis', 'ex praedictis summis',
     'the editor (2026-11-26): the word is "ex"'),
    ('0019_b', 'se referentibus et hasce summas enucleantibus Recognoscentem successoribus Prusimscianis instituto ac cum '
              'processe juris pertinente cessit',
     'se referentibus et hasce summas enucleatibus un[s?][u?][o?]n provisionibus ab ejsdem summis capitalibus '
     'provenientibus ac[u?]um process[ae?] juris per Recognoscentem successoribus Prusimscianis instituto cessit',
     'the editor\'s new reading of the passage (2026-11-26), made from the interlinear line above line 10 and the '
     'foot line, by the crosses: "una cum provisionibus ab ejusdem summis capitalibus provenientibus, ac cum '
     'processu juris per Recognoscentem successoribus Prusimscianis instituto": "together with the interest '
     'arising from the same principal sums and with the legal process instituted by the acknowledger against '
     'the Prusimski successors", a single sentence; "per" is the preposition, not "pertinente". Claude saw that it '
     'reads as one sentence and that "un[...]n" fits "unacum", the written-together "una cum"'),
    ('0019_b', 'libere accedente fun[d?]u[m?] provisionibus ab ejsdem summis capitalibus provenientibus',
     'libere accedente',
     'the same reading: the words "provisionibus ... provenientibus" belong at the cross before "cessit", '
     'not at the end'),
    ('0019_b', 'recog~tioni', 'recog[ni]tioni',
     'the editor (2026-11-26, TODO t904): the tilde forms are expanded in square brackets, where certain. This is the '
     'only one: "alisculi~" is an unresolved word and cannot be expanded; it stands'),
    ('0019_b', 'Super Transfusionem', 'Sup[er] Transfusionem',
     'the docket under the signature has "Sup" abbreviated'),
    ('0019_b', 'actas praesenti', 'Actaq[ue] praesenti',
     'the page has "Actaq" with the stroke of the abbreviation'),
]

# ---------------------------------------------------------------- web copies of the images
# The two images came as 1185 x 2000 pictures; the site's copies are 1100 pixels wide.
IMAGES = {'0019_a': ('leaf19r.jpg', 1), '0019_b': ('leaf19v.jpg', 2)}


def scans(src_dir):
    from PIL import Image
    out = os.path.join(ROOT, 'site', 'assets', 'scans')
    for pid, (name, n) in IMAGES.items():
        im = Image.open(os.path.join(src_dir, name)).convert('RGB')
        h = round(im.height * 1100 / im.width)
        dst = '%s_%s-L1_%02d.jpg' % (PREFIX, pid, n)
        im.resize((1100, h), Image.LANCZOS).save(os.path.join(out, dst), quality=78)
        print('wrote', dst)


# ---------------------------------------------------------------- the English
# Translated in session (no paid run) from the corrected Latin; the editor's
# English (intake/editor_english.md) was a guide and was checked against the
# Latin phrase by phrase. Doubt in the English follows the editor's ruling of 2026-11-22
# (EDITORIAL_RULES, "An unread word in the English"): the sense with [?] after it where the
# passage fixes the sense, [...] where it does not; never the original's letters.
PAGES = [
    # leaf 19 recto
    'No. 39: The Excellent Jan Tracholz, merchant and inhabitant of Witkowo, sound in mind and body, '
    'openly, withdrawing, etc., acknowledged that he himself, wholly and entirely, his own '
    'monetary sums, one of them being 1,053 imperials, 13 groszy and 6 Pfennig[?], '
    'owed through the late Right Honourable Paweł Prusimski, for trees bought by the present acknowledger, the '
    'honourable Tracholz, in the pine forests and woods of Trąbczyn by means of a contract written out for '
    'the said late Right Honourable Prusimski for the purchase of those same trees [...], worked out from the '
    'honourable acknowledger Tracholz\'s own funds and care (although the same late Right Honourable '
    'Prusimski had once received from the same acknowledger full satisfaction according to the tenor of '
    'the aforesaid contract), the trees having been seized from the same acknowledger by force in the said '
    'pine forests and woods of Trąbczyn by this late Right Honourable Prusimski and sold by the same Right '
    'Honourable Prusimski to the honourable Simon, merchant of Szczecin; received in this amount (as the '
    'written acknowledgement of the same honourable Simon, merchant of Szczecin, commonly called an '
    '*Auscuk* [the German Auszug, an extract of account], attests);\n\n'
    'and then a second sum, of 1,513 złoty, spent by the same honourable Tracholz, the present '
    'acknowledger, partly on the making of sawn goods, that is, nine stacks of *Klapek* [a kind of sawn timber], commonly called '
    '*Rynek*, likewise seized by the late Right Honourable Antoni Prusimski, full brother of the same late '
    'Right Honourable Paweł Prusimski, by reason of what followed upon the pine forests and '
    'woods in controversy and inquiry between them, seized in this pine forest; spent by the acknowledger, '
    'the honourable Tracholz, and partly laid out for the benefit and interest of the said late '
    'Right Honourable Paweł Prusimski, set out in a separate[?] register written by this acknowledger, and '
    'received for these sawn goods by this late Right Honourable Antoni Prusimski and disposed of for [...] and for his own '
    'benefit; and other sums, [shown] by writings and documents, handwritten ones and registers,',
    # leaf 19 verso
    'and also explained by various annotations, called [...]; these sums belonging to the '
    'acknowledger by right of legacy, reserving and excepting nothing from the aforesaid sums for himself and '
    'his successors thereafter, he has ceded, conferred, transposed, transferred and made over (as he cedes, '
    'confers, transposes, transfers and makes over) into the person of the Right Honourable Stanisław '
    'Chełmski, as one paying these sums to the acknowledger by his own right[?] and fully '
    'satisfying him for the foregoing, and to his successors, with full, total and entire right, dominion, '
    'ownership and competence, together with any and all rights of claiming that relate to these sums and '
    'set these sums out, together[?] with the interest arising from the same principal sums and '
    'with[?] the legal process instituted by the acknowledger against the '
    'successors of the Prusimskis; and by the present act [...] and conceding [...], '
    'this his personal acknowledgement freely assenting to the foregoing.\n\n'
    'Jan Tracholz, by his held hand\n\n'
    'On the transfer of his right in the person of M. Chełmski',
]


def english():
    return {1: PAGES}


# ---------------------------------------------------------------- the summaries
S = {
 1: ('Der Kaufmann Jan Tracholz aus Witkowo erklärt vor dem Burggericht in Pyzdry, dass er an Stanisław '
     'Chełmski, der ihn dafür bezahlt, seine eigenen Geldforderungen an den verstorbenen Paweł Prusimski '
     'abtritt. Die erste Summe, 1053 Imperialen, 13 Groschen und (wie es scheint) 6 Pfennig, betrifft Bäume aus '
     'den Kiefernwäldern von Trąbczyn, die er aufgrund eines schriftlichen Vertrags gekauft hatte und die '
     'Prusimski ihm gewaltsam wegnahm und an einen Kaufmann Simon aus Stettin verkaufte. Die zweite, 1513 Złoty, '
     'hatte er teils für die Herstellung von Schnittware (neun Stapel) aufgewendet, die Pawełs leiblicher Bruder '
     'Antoni Prusimski ebenfalls wegnahm, teils zu Pawełs Nutzen ausgelegt. Mit den Summen gehen die Rechte '
     'daran, die Zinsen und das von Tracholz gegen Paweł Prusimskis Nachfolger eingeleitete Verfahren über. '
     'Tracholz unterschreibt mit „gehaltener Hand“, von einer fremden Hand geführt.',
     'The merchant Jan Tracholz of Witkowo declares before the municipal court of Pyzdry that he makes over to '
     'Stanisław Chełmski, who pays him for them, his own monetary claims against the late Paweł Prusimski. The '
     'first sum, 1,053 imperials, 13 groszy and (it seems) 6 Pfennig, concerns trees from the pine forests of '
     'Trąbczyn that he had bought under a written contract and which Prusimski seized from him by force and '
     'sold to a merchant Simon of Szczecin. The second, 1,513 złoty, he had spent partly on the making of sawn '
     'goods (nine stacks), which Paweł\'s full brother Antoni Prusimski likewise seized, and partly laid out for '
     'Paweł\'s benefit. With the sums pass the rights to them, the interest, and the proceedings Tracholz had '
     'begun against Paweł Prusimski\'s successors. Tracholz signs "by his held hand", another hand guiding his.'),
}
HOW = ('written in the working session from the corrected transcription (2026-11-26).')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    parts = read_source()
    print(len(parts), 'parts of pages,', sum(len(' '.join(p).split()) for p in parts.values()), 'words')
    if '--scans' in arg:
        scans(arg[arg.index('--scans') + 1])
    if '--write' in arg:
        assert not os.path.exists(os.path.join(UNIT_DIR, 'transcription_decisions.csv')), \
            'corrections are already logged: --write would put the uncorrected text back'
        courtbook.write_pages(UNIT_DIR, DOCS, parts)
    if '--correct' in arg or '--write' in arg:
        courtbook.correct(UNIT_DIR, SLUG, DOCS, ROWS, True, source='read on the page image')
    if '--english' in arg:
        tdir = os.path.join(HERE, 'translation')
        os.makedirs(tdir, exist_ok=True)
        courtbook.write_doc_yml(os.path.join(tdir, 'doc1.yml'), english()[1])
        # write_doc_yml counts only the old "[uncertain:" form; the rule of 2026-11-22 uses [?] and [...]
        import re
        import yaml
        path = os.path.join(tdir, 'doc1.yml')
        doc = yaml.safe_load(io.open(path, encoding='utf-8'))
        for pg in doc['pages']:
            pg['marker_count'] = len(re.findall(r'\[\?\]|\[\.\.\.\]|\[uncertain|\[text lost', pg['en']))
        io.open(path, 'w', encoding='utf-8', newline='\n').write(
            yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100))
    if '--cache' in arg:
        courtbook.save_cache(ROOT, SLUG, os.path.join(HERE, 'translation'))
    if '--summaries' in arg:
        courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S, HOW)


if __name__ == '__main__':
    main()
