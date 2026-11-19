# I. HA GR, Rep. 7 C, Nr. 3067

Three documents of 16 February 1797 on six pages: the Grand Chancellor
Goldbeck's promemoria to King Friedrich Wilhelm II on the outcome of the
proceedings against the insurgents of 1794 in South Prussia and on a further
pardon (1), the King's own-hand decision written beneath it, refusing any
reduction (2), and the list the promemoria encloses, of the 31 rebels
sentenced to death, to the fortress for life or for long terms (3). Added
2026-11-19 at the editor's word, branch `trampczynski-family`.

The archive's title, as the editor gave it: "Promemoria Goldbecks mit Angaben
über das Ergebnis des Rechtsverfahrens gegen die Insurgenten und Anfragen
wegen deren Begnadigung sowie eine eigenhändige ablehnende Entscheidung des
Königs".

## Provenance

GStA PK. The editor gave the reference as "I. HA Rep. 7 C, Nr. 3067"; it is
written "I. HA GR, Rep. 7 C, Nr. 3067" with the series' GR, as its siblings
Nr. 1414, 3570, 3705 and 3709 are (the scans' file names omit GR for all of
them). Slug `ihagrrep7cnr3067`. NEEDS_CONFIRMATION asks.

Four scans as the editor gave them (Downloads\74344_Lacko\I_HA_Rep_7_C_Nr_3067\Process),
0005 to 0008, the archive's pencil folios 3 to 6; scans 0001-0004 were not
supplied (presumably the folder). 0005 and 0007 the editor had cut to the
leaf; 0006 and 0008 are openings, cut at the fold on the binding thread by
`intake/build_pages.py --crop` (the boxes are in its CROPS). Page ids: 0005_a,
0006_a1, 0006_a2, 0007_a, 0008_a1, 0008_a2.

## Documents

- **1, memorandum**, 0005_a to 0006_a2: Goldbeck's promemoria, "Berlin den
  16ten Februar 1797". The date "d. 16 Feb. 1797" at the head of the first page
  is in another hand (a docket); kept where the editor put it.
- **2, royal_resolution** (a new document kind, label added to i18n.yml in
  both languages), 0006_a2 from line 10: the King's decision, "Fr. Wilhelm / d 16
  Februariy 1797". A decision written on the paper it answers is its own
  document (NEW_UNIT, "A file the office wrote on").
- **3, register**, 0007_a to 0008_a2: the list. Kept line by line as the
  editor transcribed it, cell by cell (number, name, offence, length,
  beginning), as a register; not made into a table, since `render_table`
  sets every cell after the name as a figure. Its date is inferred from the
  promemoria, whose enclosure it is ("nach der beyliegenden Liste"). Two other
  registers (Oe 1 Bü 14525, documents 13 and 14) also keep their line-end "¬"
  in the reading.

The promemoria counts 3 sentenced to death and 2 for life; the list has 2
under A (death) and 3 under B (life), Nowicki among B with "zum Galgen
verurtheilt; ist aber ... pardonnirt worden". The promemoria counts him with
the death sentences ("wovon aber einer unter dem Galgen Pardon erhalten"). The
figures 307 + 49 + 26 + 2 + 3 = 387 add up; the list's C has 26 entries.

## The transcription checked

The transcription is the editor's. At the editor's word ("examine the
transcripts to see if there are any transcription errors ... use Sonnet
subagents where possible") four Sonnet readers checked it against the page
images, two independently for each part (promemoria and the King's note;
the list), each given the page in overlapping strips at full resolution and a
list of suspect spots without the suspected answer; reader 2 read the King's
lines from the image before opening the transcription, reader 4 the names and
dates of 0008_a2. Claude then looked at every disputed word on an enlarged
crop. 24 corrections, each with its witness, in `intake/build_pages.py`
(CORRECTIONS): among them "zufürtzerer" → "zu kürtzerer", "größtintheils" →
"größtentheils" (the same word six lines below), "ge¬ / geldet" →
"ge¬ / meldet", "Straf E[w?][r?][m?]¬pel" → "Straf Exem¬pel" (the fixed
formula), "Mnewski" → "Mniewski", "Höym" → "Hoym", "Weiler" → "Weil er"
(three times), "Ausgleicher" → "Aus gleicher" (twice), "des Insurrektion" →
"der", "December" → "Dezember" (entry 14), "4 Jahre" → "4 Jahr" (entry 26).
In the King's hand: "binnen" → "keinen" (the one reading of the sentence:
"finde keinen der Condemnirten einer Minderung der Strafe würdig"),
"Betrachtung" → "Untersuchung[?]", "erkennen[?]" → "erlegung[?]",
"am[e?]st" → "arest", and the struck word "straffe" taken out (struck-out text
is not transcribed: EDITORIAL_RULES, 2026-10-05; two words on that line are
struck, the editor had transcribed one of them).

Left as transcribed, on the editor's spot sheet (`intake/spot_sheet.py`,
`review/ihagrrep7cnr3067/open_queries.csv`, eight rows): "befreyt" (all three
readings see "freyt", but the figures that follow are sentences, not
releases; a thought, not a reading: "befragt"?), the King's "Untersuchung[?]",
"verbrach[en?]", "erlegung[?]", "da[?]" (one reader: "die schon"),
"dererjenigen" (one reader: "derjenigen"), "Pistrzkowski" (one reader:
"Pistzkowski"), "Mißbrauch" of entry 23 (entry 5 has "Mißbrauchs").

Not transcribed, as in the editor's text: the "# #" marks above "Sollten Sr
Königliche Majestät" (0005_a), above "Es schweben noch einige wenige
Untersuchungen" (0006_a1) and above "auf obige Vorschläge" (0006_a2); a small
brown-ink mark at the foot of 0005_a, read "v. Sh." by one reader; the pencil
folio numbers; the underlining of "nach der beyliegenden Liste" and "nach
eben dieser Liste"; in the list, the filler dots and dashes after the names
and the lengths (only entry 16's "6 Jahre -" is in the transcription), the
full stops after the column heads of 0008_a1, and the braces that join the
reason of A 1 and 2, and the reason and the date "März 1796" of C 20 and 21
(the transcription gives the reason and the date once).

Goldbeck's signature stands on the page at the right edge, in a thin
red-brown ink, underlined, level with the King's sixth and seventh lines,
which run round it; the transcription puts it after his date, where it
belongs to document 1.

Line ends: the resolver's "split" of lebens wie¬rige, Posen¬schen, be¬freyt,
exten¬diren, exa¬miniren and Con¬foederation set to `join` by hand;
"Krieg¬ / Commission" left split. Paragraph breaks set by hand (`hand` rows):
the docket, "Promemoria", "Bey allen diesen", "Die Haupträdelsführer", "Daher
ist es", "= 387.", "Sollten Sr.", the dateline; the King's date joined.

## Translation and summaries

Translated in session (2026-11-19), no paid run: `intake/translation/doc1-3.yml`,
written to the cache by `write_cache.py`; check_translations.py raised
nothing. The English uses Poznań, Włocławek, Wieluń, Łęczyca, Kalisz;
"Ostrzewo" kept as written (Ostrzeszów, which lay in the Wieluń land, is a
thought only). Summaries written in session (`intake/write_summaries.py`),
claim-checked by a Sonnet sub-agent (`intake/claim_check.yml`: 58 statements,
6 overstated, 4 cut or weakened and 2 kept with the reason given there).

## Index

- Goldbeck: `only_in` extended to document 1. Friedrich Wilhelm II: his
  signature "Fr. Wilhelm" added to his `issuer_match`, document 2 to
  `issued_in`. Hoym matched.
- Wybicki and Niemojewski (document 1) are matched to the existing entries,
  whose confiscated estates were returned in 1807: Claude's identification,
  noted in both entries and in NEEDS_CONFIRMATION.
- Shut out: the minister Sobolewski of 1820 (not Joseph Sobolewski, documents
  1 and 3), Grand Duke Constantin (not Constantin v. Mielewski), the creditor
  Magnuski of 1805 (not shown to be Vincent von Magnuski; `seed_not_in`).
- Places: Włocławek now matches "Wraclawec" (the pattern hit only this list
  and the existing "Wraclawek" of Oe 1 Bü 14525-28); Łęczyca matches
  "Lenczyc..."; Rypin added as a place. The broken "Wrac¬lawek" (B 2) is not
  found by the matcher.
- No person entries for the 31 names of the list or the other ringleaders:
  NEEDS_CONFIRMATION asks.

## Era

`hohenlohe`, as Nr. 1414: the insurgency era's own blurb says the Prussian
files of these years stand in the era of the estate's Prussian years.
NEEDS_CONFIRMATION asks whether the editor would rather have it in
`insurgency`.

## Damage

None recorded.
