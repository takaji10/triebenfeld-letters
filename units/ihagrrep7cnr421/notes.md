# I. HA GR, Rep. 7 C, Nr. 421

The Prussian ministry's file of October to December 1799 on the complaints of
Stanisław von Chełmski of Łukom over his claim of 12,000 ducats on the former
Starost Antoni Prusimski: seven documents on 23 pages, the cover as front
matter. Added 2026-11-21 at the editor's word, branch `trampczynski-family`;
**not published**.

The archive's title, as the editor gave it: "Beschwerden des v. Chelmski wegen
seiner Forderung an den ehemaligen Starosten v. Prusinski". The cover reads
"SüdPreussen", "d. 21 Octobr 1799" (the editor's "24" changed on reader 1's word,
spot sheet q1), "Acta Die Beschwerden des von Chełmski wegen seiner Forderung an
den ehemaligen Starosten von Prusinski betr."

## Provenance

GStA PK. The editor gave "I. HA Rep. 7 C Nr. 421"; written with GR, as the
siblings (the archive's label: "I. HA Geheimer Rat, Rep. 7 C Südpreußen"). Slug
`ihagrrep7cnr421`.

Twenty-one files (Downloads\74344_Lacko\I_HA_Rep_7_C_Nr_421), with the
editor's transcriptions of seventeen in `txt/`. Left out, having no
transcription (the editor: "For pages without a transcription, don't include
them in the project"): 0015 and 0018 (a blank side and the archive's slip "Es
folgen leere Seiten") and 0019 (the back cover); and 0014, the opening the
editor's own crops 0014a and 0014b replace (their transcriptions are of the
crops). The crops are one page each and not cut; their pages are named
`0014_a1` and `0014_a2`, because match_scans and relabel_scans take a capture of
four digits (`SOURCE_OF` in `intake/holding.py` says which of the editor's files
each reads). 0001 is the cover; the other openings are cut at the fold by
`intake/holding.py --crop` (courtbook.cut, the folds proposed by
courtbook.find_fold, the edges by eye to leave off the ruler). Blank sides and
the archive's slips are not cut out at all (the editor: "don't include the blank
sides"; `keep_skipped=False`): the left sides of 0002 (the archive's user sheet),
0006, 0008, 0011, 0016 (a large blank sheet; the page is the small slip beside
it) and 0017, and the right of 0010. **The fold page** (`holding.py --sheet` ->
`review/ihagrrep7cnr421/folds/index.html`): **the editor's folds and edges
applied 2026-11-21** (their `folds_ihagrrep7cnr421.json`, now `intake/folds.json`,
put in with `python pipeline/intake/courtbook.py folds ihagrrep7cnr421 <file>`;
the fold moved on eight scans (0003, 0005, 0007-0012, by 1 to 56 pixels), the edges set on every scan, none turned). The text is not touched by it.

Pages: 0001_a (cover), 0002_a2, 0003_a1, 0003_a2, 0004_a1, 0004_a2, 0005_a1,
0005_a2, 0006_a2, 0007_a1, 0007_a2, 0008_a2, 0009_a1, 0009_a2, 0010_a1,
0011_a2, 0012_a1, 0012_a2, 0013_a1, 0013_a2, 0014_a1, 0014_a2, 0016_a2,
0017_a2.

## The documents

**Seven** (the editor, 2026-11-21, asked before the cut: "Seven: bond with the
suit"; Claude had proposed eight, the bond its own document). The editor's
standing word for this file: do not split documents too readily, least of all
where two stand on the same side.

| Doc | Pages | What it is | Date, place |
|---|---|---|---|
| 1 | 0002_a2 to 0005_a2 | Chełmski's petition to the King, with the official's note and the decision of 21 Oct. in the margin of its first side | 8 Oct. 1799, Kalisz |
| 2 | 0006_a2, 0007_a1 | Copies of the Kalisz government's two decrees (the second begins on the same side) | 10 and 27 Sept. 1799, Kalisz |
| 3 | 0007_a2 | Draft of the King's answer to Chełmski | 21 Oct. 1799, Berlin |
| 4 | 0008_a2 to 0010_a1, 0016_a2 | Mondro's petition for Chełmski, with the office's slip of 23 Dec. | 7 Dec. 1799, Kalisz |
| 5 | 0011_a2, 0012_a1 | A copy of the same petition, headed "Abschrift" | 1 Dec. 1799, Kalisz |
| 6 | 0012_a2 to 0014_a2 | Copy of Chełmski's suit against Prusimski, with the copy of Prusimski's undertaking in Polish (0014_a2) | 19 March 1799, Poznań (the bond 16 June 1794, Łukom) |
| 7 | 0017_a2 | Draft to Mondro | 23 Dec. 1799, Berlin |

**The slip stands out of the file's order**: bound after the suit (0016), it
decides Mondro's petition ("ad n: 9", the petition's folio), so it is read with
document 4, as Nr. 3132's slip was. `holding.py` writes corpus.txt itself (DOCS);
`scan_decisions.json` (`image_order`) gives match_scans the same order. The
official's note, the decision of 21 Oct., the note "Anteriora ..." on 0008_a2 and
the slip are in `office_notes.yml`.

**The margin of 0002_a2 is placed first on the page**, before the petition's
text: the column's last line ends "von Kö¬" and its catchword "nigl:" stands at
the foot, so the notes cannot stand between them without breaking the word in
the reading text (the line-break pass looks for the catchword on the page's last
line). 

Types: petitions 1, 4, 5, 6 (a copy keeps the type of what it copies; the suit
is addressed to the King); decree 2; drafts 3 and 7 (the layout of Nr. 3132's).
Relations: 1 transmits 2; 3 answers 1; 4 supplements 1 and transmits 6; 5 copies
4; 7 answers 4.

## The transcription checked

The editor's transcription (a recognition model's reading, corrected, with [?])
was checked at their word ("the Nr. 3132 method") by four Sonnet readers in
strips at full resolution: reader 1 the clean hands and copies (cover, 2, 3, 5,
the slip, 7); reader 2 Chełmski's petition; reader 3 Mondro's petition and the
suit; reader 4, independently and image first, the Polish bond, the margin of
0002_a2, the slip and the registry notes. Readers 2 and 3 left strips unopened
(0005_a2's foot, 0009_a2, 0010_a1); Claude read those against the clean copy.
**The witnesses inside the file**: Mondro's petition and its clean copy (4 and
5), the decision in the margin and the clean draft (1 and 3), the suit and the
bond it describes (6). 133 corrections, each with its witness, in
`intake/holding.py` (CORRECTIONS). Among them: "Plage" -> "Klage", "rest" ->
"fest"/"vest", "Perer¬ste" -> "Rever¬se", "Chett[?] der Justiz gestöhet" ->
"Chef der Justiz zustehet", "Pla¬von[?]" -> "kla¬ren", "langt seine Bewerde" ->
"lediglich sein Bewenden", "Erste[?]" / "eigl." -> "Kö¬" / "nigl:" (the
catchword), "1746" -> "1796", "ex Mirographa" -> "ex Chirographo", "aequistriren"
-> "sequestriren", "antechreticam" -> "antichreticum", "reta[s?]is" -> "refusis",
the line-end "ß" of the recognition model in 0007_a2 ("Staß", "Resoluß", "Anß")
-> "¬", and in the Polish "wypołucona" -> "wypłacona", "wyrażana" ->
"wyrażona", "żadnzey" -> "żadney". Where the readers disagree and the editor's
word is possible, the editor's word stands and the question is on the spot
sheet.

Not transcribed, as in the editor's text: stamps, registry numbers beyond those
the editor wrote, red crayon strokes, a short word struck out in the margin
decision, a struck word in the bond (line 25), paraphs.

**The spot sheet** (`intake/spot_sheet_html.py` ->
`review/ihagrrep7cnr421/spot_sheet.html`, one self-contained page): 21 readings
and 3 decisions (a person entry for Stanisław Chełmski, the Mondro entry, the
connection). **Answered by the editor 2026-11-21** and applied through
CORRECTIONS (the block "The editor's spot sheet"):

- Kept as they stood: q1 (the cover's 21), q2 (the official's note as the
  editor read it), q3 ("habe"), q9 (the suit's **1799**: the digit is read so,
  though the suit's own words, the eviction suit of 7 Dec. 1795, "27. Februar
  c." and "zu Johanni v. J.", fit 1796; the document stays under 1799 and the
  difference stays in NEEDS_CONFIRMATION), q16 ("Swiętego"), q20 ("geworden").
- Changed: q4 "werde", q5 "Hoflager den", q6 "Deckung", q7 "selbst", q8 "16t"
  (the copy agrees with the original), q10 "muste ich", q11 "Rük¬ / zalung"
  (the copyist's line-end mark, so "¬"), q12 "nehm¬ / lich" (the editor's
  own), q13 "abrechnen", q14 "meine Anforderun¬ / gen", q15 "die ich ab¬ /
  hören" (the editor's own), q18 "Fabryki", q19 "Crim. R.", q21 "ita conclus.
  eod.".
- q17, the editor unsure ("could be myslnie, wyslnie, ucystnie... take some
  more time"): Claude at twice the size reads u-m-y, the long s with its head
  looped high, l-n-i-e: "na umyslnie", that is naumyślnie, deliberately,
  after "z dobrey woli" (of free will), the formula of a voluntary bond.
  Written "na umyslnie" without the accent, as the copyist writes
  "Swiętego".
- q20, the editor's question whether "gewordenen" fits better: yes, the
  grammar wants it ("der seinem principal gewordenen resol.", the resolution
  given to his principal), and the word ends in a rising stroke after "den"
  that may be the clerk's shorthand for the ending. The letters on the page
  are "geworden", so the transcription keeps them; the English says "given".

**The lawyer's name is Mondro** (the editor, 2026-11-21: "In some places I
thought it was Mondro, and others Mondio. Can you please fix my mistakes?").
Claude read every place against the scans: his own signature under the
petition (0010_a1) and the clean copy's (0012_a1), the decree copies (0006_a2,
0007_a1), the petition's docket (0008_a2) and both places in the draft
(0017_a2) read "Mondro", the Kurrent n written like u ("Moudro"). Five readings
corrected in CORRECTIONS; q22 taken off the spot sheet. The registry's "conc
Mondo" under document 1 (0005_a2) shows no r and stands as written.

## Line ends and paragraphs

The resolver split 21 words broken with "¬" whose joined form it found nowhere
(old spellings, Latin, Polish, names); 17 are joined by hand
(`intake/linebreaks.py`; two more, "u[?]hab¬" and "re[?]ha[l?]¬", became
"ab¬ / hören" and "nehm¬ / lich" on the spot sheet and join by themselves), "allen¬ / persönlichen" and "einer¬ / wider" stay two
words. Paragraphs set by `intake/paragraphs.py` on stated principles (31 rows
held). Run both after a rebuild.

## Translation and summaries

Translated in session (2026-11-21), no paid run: `intake/translation/english.py`
writes doc1-7.yml, `write_cache.py` caches them. check_translations raised 23
rows, all cleared (the termbase's "criminal-court councillor", "Hollander",
"Nowawies", "I remain, until death,"; "the Prince of Hohenlohe"; the rare pair
Abweisung flagged on its five pages; a date set on its own page); none since.
The Polish page translated from the Polish. The English follows the spot
sheet's readings (2026-11-21: "selbst" himself, "16th", "muste ich" I had to
advance, "nehmlich" namely, "meine Anforderungen" my claims, "die ich abhören
zu laßen" whom I ask to have examined, "na umyslnie" deliberately, "Crim. R."
the criminal-court councillor); words still unread are kept as written.

Summaries in session (`intake/write_summaries.py`), claim-checked by a Sonnet
reader (`intake/claim_check.yml`: 88 statements, 78 supported, 10 overstated;
all ten taken).

## Index

**A new person entry, `stanislaw-chelmski`** (the editor, spot sheet d1:
"he is the Stanisław of the boundary decree of 1775 - make a person entry for
this person"), with a page (`reference/genealogy.yml`: parents from Boniecki
and the database, his wife Dorota Skórzewska and son Franciszek Ksawery from
Boniecki) and a bio (`reference/people_bios.yml`). His pattern takes the
surname after his forename or before his title (Thes., Skarbnik) anywhere,
and the bare surname in the documents that so name him, in all of Nr. 421,
and in Oe 1 Bü 9454, 75, 102, 103, 286 (Claude's, by the connection kept);
not after "Jerzym", "Jerzemu", "Józefowi" or "rodzonym". 67 documents, 1763
to 1815. The family entry `chemski` keeps every Chełmski as before.
**Mondro has an entry** (`mondro`, the criminal councillor who was the
Prince's attorney in the Olesnica suits of 1805, Nr. 3705): with the name
settled it tags him in documents 2, 4, 5 and 7 (not the registry's "Mondo");
the same man, the editor's word (spot sheet d2), now in his identity and
bio. Places: Kalisz, Trąbczyn, Berlin,
Łukom, Łukomia, Poznań, Pyzdry, Osiny; Nowa Wieś (the estate's Nowawies, matched
narrowly on purpose), Łazy and Mierzewo are not matched here. New glossary entry `fiscus` (checked: false,
Krünitz to check against; 122 marks across the edition); "Dec", "Octbr.",
"huj.", "praes." ruled out under `excluded:`.

## Connections

One, kept at the editor's word (spot sheet d3): `chelmski-suit-against-hohenlohe`, documents 1 and
4 with Oe 1 Bü 9454, letters 75, 102, 103 (Triebenfeld on "Chełmski's process"
against the Prince, 1798-1799) and 286 (the memorandum of 1815: the pledge "für
36000 Ducaten"; this file: 12,000). The letters' "second instance" is not
equated with Chełmski's "Revisions Erkenntniß": in Prussian procedure the
appeal was the second instance and the revision the third.

## Era

`hohenlohe`, as Nr. 1414, 3067 and 3132.

## Damage

None recorded.
