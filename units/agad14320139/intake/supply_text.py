# -*- coding: utf-8 -*-
"""Write the supplied words into the transcription of 1/432/0/1/139, once.

The editor, 2026-11-13: "update the transcriptions to fill in the missing words
that don't add facts by using the square brackets in the same manner which you
did for the English", and "[not]" in both negations of 0322_a. A supplied
stretch stands in square brackets with no question mark (the G[oldbeck]
convention); what would add a fact (a figure, a place, a date, a lost list)
stays [...]. Sources: the A and B rows of supplied.yml, the C rows the English
uses (the form's address, "[feh-]", "[sammelt]", "[aber]" ...), and the two
negations. A supplied hyphen at a burnt line end is written inside the bracket,
"fo[lgen-]", and joined in the reading text (corpus_pages._wrap_mark).

Each row: page, line, the line as it stood, the line as it stands now. The
script refuses a line that is not as recorded, so it cannot run twice.

    python units/agad14320139/intake/supply_text.py
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(HERE)

ROWS = [
 ('0318_a', 1, '[...]ner', '[Sei]ner'),
 ('0318_a', 2, '[...] Herrn General-Superin[...]', '[Hochwürden dem] Herrn General-Superin[tendenten]'),
 ('0318_a', 3, 'des Warschauer Evangelisch-Augsburg[...]', 'des Warschauer Evangelisch-Augsburg[ischen]'),
 ('0318_a', 5, 'Pastor-Administrat[...]', 'Pastor-Administrat[or der Evan-]'),
 ('0318_a', 6, 'gelisch-Augsburgischen [...]', 'gelisch-Augsburgischen [Gemeinde]'),
 ('0318_a', 8, 'In Folge der Anordnung [Ho?][...]', 'In Folge der Anordnung [Ho?][ch-]'),
 ('0318_a', 10, '№267, habe ich die Ehre fo[...]', '№267, habe ich die Ehre fo[lgen-]'),
 ('0318_a', 11, 'den die Parochie Zagórow be[...]', 'den die Parochie Zagórow be[tref-]'),
 ('0318_a', 12, 'fenden Jahresbericht vorzustel[...]', 'fenden Jahresbericht vorzustel[len]'),
 ('0318_a', 15, 'eine gemauerte Kirche; zur völligen Einrichtung derselb[en?] [...]',
                'eine gemauerte Kirche; zur völligen Einrichtung derselb[en?] [feh-]'),
 ('0318_a', 16, 'len noch Taufstein, Orgel und Glocken.– Sowohl das Pastora[...]',
                'len noch Taufstein, Orgel und Glocken.– Sowohl das Pastora[t als]'),
 ('0318_a', 18, 'sehr schlechtem Zustande.– Das Schullokal im Verhältniß [...]',
                'sehr schlechtem Zustande.– Das Schullokal im Verhältniß [zur]'),
 ('0318_a', 19, 'Kinderzahl entsprechend geräumig.– Außer der Religions-Sch[...]',
                'Kinderzahl entsprechend geräumig.– Außer der Religions-Sch[u-]'),
 ('0318_a', 20, 'le in Zagórow, giebt es noch 7 Schulen verbunden mit Beth[...]',
                'le in Zagórow, giebt es noch 7 Schulen verbunden mit Beth[äusern]'),
 ('0318_a', 22, 'Michalinowo.– Die Zahl der Kinder in den 8 Schulen der [...]',
                'Michalinowo.– Die Zahl der Kinder in den 8 Schulen der [Ge-]'),
 ('0318_a', 24, 'ist keine besondere Wohnung vorhanden.– Der Zustand d[?][...]',
                'ist keine besondere Wohnung vorhanden.– Der Zustand d[?][er]'),
 ('0318_a', 28, 'befriedigend.– Die Taufen werden meistens vom Pastor voll[...]',
                'befriedigend.– Die Taufen werden meistens vom Pastor voll[zogen]'),
 ('0318_a', 29, 'Offenbarer Abendmahls-Verächter unbewußt.– Die Zahl d[?][...]',
                'Offenbarer Abendmahls-Verächter unbewußt.– Die Zahl d[?][er Com-]'),
 ('0322_a', 4, '[...] den Missions-Gottesdiensten 10 Rubel 71 Kopeken ge-',
               '[Jahres bei] den Missions-Gottesdiensten 10 Rubel 71 Kopeken ge-'),
 ('0322_a', 5, '[...] worden, welche der Pastor-Administrator an den',
               '[sammelt] worden, welche der Pastor-Administrator an den'),
 ('0322_a', 6, '[...] Superintendenten Pastor Manitius nach Warschau über-',
               '[Herrn] Superintendenten Pastor Manitius nach Warschau über-'),
 ('0322_a', 7, '[...] hat.– Sittlichkeit so wie das häusliche Zusammenleben sind',
               '[sandt] hat.– Sittlichkeit so wie das häusliche Zusammenleben sind'),
 ('0322_a', 8, '[...]A[?]llgemeinen sehr befriedigend.– Baptisten, Irvingianer oder',
               '[im] A[?]llgemeinen sehr befriedigend.– Baptisten, Irvingianer oder'),
 ('0322_a', 9, '[...]dere Sekten giebt es nicht.– Besondere Laster[?] in der Gemeinde',
               '[an]dere Sekten giebt es nicht.– Besondere Laster[?] in der Gemeinde'),
 ('0322_a', 10, '[...]t vorhanden. Uebertritte zu andern Confessionen finden',
                '[nich]t vorhanden. Uebertritte zu andern Confessionen finden'),
 ('0322_a', 11, '[...] statt.–', '[nicht] statt.–'),
 ('0322_a', 16, '[...]mmelt[?], zu andern Zwecken aber Folgende: 1.) Zur Unterstü-',
                '[gesa]mmelt[?], zu andern Zwecken aber Folgende: 1.) Zur Unterstü-'),
 ('0322_a', 17, '[...]g von Gymnasiasten, welche Theologie zu studiren gesonnen',
                '[tzun]g von Gymnasiasten, welche Theologie zu studiren gesonnen'),
 ('0322_a', 20, '[...] Wittwen und Waisen Kasse 2 Rubel 36 Kopeken eingesam-',
                '[die] Wittwen und Waisen Kasse 2 Rubel 36 Kopeken eingesam-'),
 ('0322_a', 21, '[...]elt und Selbiges an Herrn Superintendenten von Boerner',
                '[m]elt und Selbiges an Herrn Superintendenten von Boerner'),
 ('0322_b', 1, '[...]ner', '[Sei]ner'),
 ('0322_b', 2, 'Hochwürden dem Herrn General-Superinten[...]', 'Hochwürden dem Herrn General-Superinten[denten]'),
 ('0322_b', 3, 'des Warschauer Evangelisch-Augsburgisch[...]', 'des Warschauer Evangelisch-Augsburgisch[en]'),
 ('0322_b', 5, 'Pastor-Administrator [...]', 'Pastor-Administrator [der Evan-]'),
 ('0322_b', 6, 'gelisch-Augsburgischen [...]', 'gelisch-Augsburgischen [Gemeinde]'),
 ('0322_b', 8, 'In Folge der Anordnung [...]', 'In Folge der Anordnung [Hoch-]'),
 ('0322_b', 10, '№267, habe ich die Ehre folge[...]', '№267, habe ich die Ehre folge[nden]'),
 ('0322_b', 11, 'das Filial Lissewo-Pyzdry [...]', 'das Filial Lissewo-Pyzdry [betref-]'),
 ('0322_b', 12, 'fenden Jahresbericht vorzu[...]', 'fenden Jahresbericht vorzu[stellen]'),
 ('0322_b', 16, 'ten Lokale abgehalten.– Im Filiale giebt es fünf Religi[...]',
                'ten Lokale abgehalten.– Im Filiale giebt es fünf Religi[ons-]'),
 ('0322_b', 17, 'Schulen verbunden mit Bethäusern, die alle in gutem Zusta[...]',
                'Schulen verbunden mit Bethäusern, die alle in gutem Zusta[nde]'),
 ('0322_b', 21, 'b.) Inneres Kirchenwesen.– Kirchlichkeit und Kirchenbesuch befri[...]',
                'b.) Inneres Kirchenwesen.– Kirchlichkeit und Kirchenbesuch befri[e-]'),
 ('0322_b', 23, 'in den Bethäusern vollzogen, der Pastor bestätigt [bei?] sei[...]',
                'in den Bethäusern vollzogen, der Pastor bestätigt [bei?] sei[ner]'),
 ('0322_b', 24, 'Anwesenheit in den Bethäusern, die von den Kantoren voll[...]',
                'Anwesenheit in den Bethäusern, die von den Kantoren voll[zo-]'),
 ('0322_b', 26, 'Offenbare Abendmahls-Verächter unbewußt. [...] Zahl [...]',
                'Offenbare Abendmahls-Verächter unbewußt. [Die] Zahl [der]'),
 ('0322_b', 28, 'Jahre 1881 gegen über mehr 131.– Die Einwohner [von?] Pyzdry [...]',
                'Jahre 1881 gegen über mehr 131.– Die Einwohner [von?] Pyzdry [möch-]'),
 ('0322_b', 29, 'ten gerne eine Evangelische Schule bei sich ein[...] sind [...]',
                'ten gerne eine Evangelische Schule bei sich ein[richten] sind [aber]'),
 ('0345_a', 3, '[...]en-Mission sind im Laufe des Jahres bei den Mis-',
               '[Für die Heid]en-Mission sind im Laufe des Jahres bei den Mis-'),
 ('0345_a', 4, '[...]diensten 3 Rubel 40 Kopeken eingesammelt worden,',
               '[sions-Gottes]diensten 3 Rubel 40 Kopeken eingesammelt worden,'),
 ('0345_a', 5, '[...] Pastor-Administrator an den Herrn Superintenden-',
               '[welche der] Pastor-Administrator an den Herrn Superintenden-'),
 ('0345_a', 6, '[...] Pastor Manitius nach Warschau übersandt hat.– Sittlichkeit',
               '[ten] Pastor Manitius nach Warschau übersandt hat.– Sittlichkeit'),
 ('0345_a', 7, '[...] das häusliche Zusammenleben sind im Allgemeinen befrie-',
               '[so wie] das häusliche Zusammenleben sind im Allgemeinen befrie-'),
 ('0345_a', 8, '[...]nd.– Besondere Laster in der Gemeinde nicht vorhanden.– Bap-',
               '[dige]nd.– Besondere Laster in der Gemeinde nicht vorhanden.– Bap-'),
 ('0345_a', 9, '[...]en, Irwingianer u. s.w. giebt es nicht.– Uebertritte zu andern',
               '[tist]en, Irwingianer u. s.w. giebt es nicht.– Uebertritte zu andern'),
 ('0345_a', 10, '[...]fessionen finden nicht statt.–', '[Con]fessionen finden nicht statt.–'),
 ('0345_a', 15, '[...]sammelt, zu andern Zwecken aber Folgende: 1.) Zur Unter-',
                '[ge]sammelt, zu andern Zwecken aber Folgende: 1.) Zur Unter-'),
 ('0345_a', 16, '[...]zung von Gymnasiasten, welche Theologie zu studieren geson-',
                '[stüt]zung von Gymnasiasten, welche Theologie zu studieren geson-'),
 ('0345_a', 17, '[...] sind 1 Rubel 76 Kopeken, Selbige hat der Pastor-Administra-',
                '[nen] sind 1 Rubel 76 Kopeken, Selbige hat der Pastor-Administra-'),
 ('0345_a', 18, '[...] seinem Hohen Evangelisch-Augsburgischen Consistorium zu',
                '[tor] seinem Hohen Evangelisch-Augsburgischen Consistorium zu'),
 ('0345_a', 19, '[...]arschau übersandt.– 2.) Für die Wittwen und Waisen Casse',
                '[W]arschau übersandt.– 2.) Für die Wittwen und Waisen Casse'),
 ('0345_a', 21, '[...]uperintendenten von Boerner nach Plock abgesandt.–',
                '[S]uperintendenten von Boerner nach Plock abgesandt.–'),
]


def apply(lines, page_rows):
    for _, n, old, new in page_rows:
        if lines[n - 1] != old:
            raise SystemExit(f'line {n} is not as recorded: {lines[n - 1]!r}')
        lines[n - 1] = new


by_page = {}
for r in ROWS:
    by_page.setdefault(r[0], []).append(r)

for pg, rows in by_page.items():
    p = os.path.join(UNIT, 'transcriptions', pg + '.txt')
    lines = open(p, encoding='utf-8').read().split('\n')
    apply(lines, rows)
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

p = os.path.join(UNIT, 'corpus.txt')
src = open(p, encoding='utf-8').read().split('\n')
out, page, k = [], None, 0
for ln in src:
    m = re.match(r'^\[PAGE (\S+)\]$', ln)
    if m:
        page, k = m.group(1), 0
    elif page and not re.match(r'^\[DOC ', ln):
        k += 1
        for _, n, old, new in by_page.get(page, []):
            if n == k:
                if ln != old:
                    raise SystemExit(f'corpus {page} line {n} is not as recorded: {ln!r}')
                ln = new
    out.append(ln)
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print(f'{len(ROWS)} lines supplied on {len(by_page)} pages')
