# Oe 1 Bü 14525

44 documents on 165 transcribed pages, 1794 to 1804: the royal grants of the
South Prussian estates to Friedrich Ludwig, Prince of Hohenlohe-Ingelfingen,
and the paperwork that carried them into effect - certified copies of the
grants, mortgage certificates, resignation briefs, a valuation of Kaemen and
Kolno, and official correspondence with the Posen and Kalisch chambers. Most
documents are copies rather than originals, which is why the date and place a
record carries are those of the attestation, not of the grant it copies.

## Provenance

Hohenloher Zentralarchiv Neuenstein (HZAN). 128 captures were cropped into 209
single-page images. 165 of those carry transcribed text and are paired one to
one with a page of the corpus; `match_scans.py` sets the other 44 aside as front
matter, blanks, or leaves past the last transcribed page. No image is used
twice and no page is without an image.

## Transcription

One text file per page image, 209 in all, in `processed/txt` beside the scans.
43 pages were left untranscribed on purpose, and `scan_decisions.json` records
them as such so they are not taken for missing pages. `import_pages.py`
assembled `corpus.txt` from the files on 2026-09-15, using the 44 document
boundaries set by the editor in `review/oe1bu14525/document_boundaries.csv`.

**The corpus has been corrected since and no longer matches the page files. Do
not re-run the import with `--force`: it would throw the corrections away.**

The first correction pass made 552 changes: misreadings, eleven places where
lines stood out of order, and two lines that are not on the page. The second
gave the Polish place names the edition's spelling: 97 lines, German names and
adjectives left as written. A third standardised surnames, the prince's
name, garbled place names and the king's titles: 102 lines. Every change,
with the line as it stood before, is in `units/oe1bu14525/transcription_decisions.csv`. The review sheets in
`review/oe1bu14525/` are working copies and are not kept in git.

Unlike the other holdings, this one standardises names in the transcription
itself, on the editor's instruction; see `docs/EDITORIAL_RULES.md`.

**Catchwords are not transcribed.** On the editor's instruction, 2026-09-16, the
49 catchwords - the word the scribe wrote at the foot of a page to announce the
next one - were deleted from the corpus, 4,187 lines to 4,138. The test is
whether the catchword duplicates what the next page carries; where it does, it
is scribal apparatus and goes. Each deletion is in `transcription_decisions.csv`
under the keys `cw-001`..`cw-044` and `cw2-001`..`cw2-005`, and
`review/oe1bu14525/catchwords_applied.md` holds the lines as they stood.

Seven were found by reading rather than by matching, because the transcribed
catchword does not repeat the next page's opening exactly: `fern` for *tenden*
(the word is *haftenden*), `Auf` for *Unsern*, `die` for *sie*, `um` for *und*,
`die` for *den*, `hiezu` for *hierzutreten*, and `König`, which is not even the
last line - a sheet number `1.` stands below it.

Five more are half a word, where the next page then carries the word in full:
`sti¬` + `pulirten` with *stipulirten* overleaf, and likewise `ches`, `heim`,
`minio`, `getragen`. The half-word at the foot duplicates the next page just as
a whole one does, so it goes too. What is left behind on the line above - `sti¬`,
`wel¬`, `Oppen¬`, `Do¬`, `ein¬` - is a stray syllable of the word overleaf, and
is ruled `catchword` in `linebreak_decisions.csv`: it stays in the archival text,
where it was written, and drops out of the reading text, which then runs
"...Erbpachts Contract," into "stipulirten Rechts" on the next page.

Two foot lines that look similar are NOT catchwords and stay. `ments` completes
*gouvernments* and the next page does not repeat it. In document 10 the foot line
is ordinary text and it is the next page that opens by repeating its last word,
`Ahndung.` - a repetition at the head, which is not the same device.

Removing the catchwords exposed 13 words broken across a page break, all ruled by
hand, and four places where the transcription itself was at fault. All four are
corrected, each on the corpus's own evidence rather than on the scan:

- `von Hohen¬` had lost *lohe* and now reads `Hohenlohe`, the next page opening
  *Ingelfingen* and the corpus writing the name that way throughout (`fix-001`);
- `wel` was missing its wrap sign, *welches* standing in full overleaf (`fix-002`);
- `geschlos` was missing its wrap sign: with *senen* it makes *geschlossenen*,
  which stands in full at L226 and is broken the same way in 14526 (`fix-003`);
- `mit vollen¬` is *mit voller*, written so four times in this unit and once of
  the same parties - "Mendel Oppenheim und Wolff in Berlin mit voller Würkung" -
  and `vollen` occurred nowhere else here. *Würkung* follows overleaf (`fix-004`).

## Quirks worth knowing

- **The same instrument recurs.** Documents 3 and 4, 5 and 8, 6 and 11, 43 and
  44 repeat one formulary, sometimes word for word for a page at a time. They
  are not duplicates: each is a separate copy or a separate rescript with its
  own date, attestation and signatories, and 43 and 44 are only 16% identical.
  `rulings.yml` therefore records no `duplicate_of`.
- **13 and 14 are registers**, an inventory of the estates and a forest
  valuation. They are shown one entry per line rather than flowed into prose.
- **21 is part Polish**, an official extract from the Kalisz mortgage register
  of the Duchy of Warsaw, recorded as `de,pl`. The Polish place names elsewhere
  are names inside German text, not a second language.
- **The numbering is the archive's** and does not run in date order: 1794 stands
  at 13, and 1804 at 22.
- **Two documents are wrong in the original, and stay wrong.** Ruled by the
  editor, 2026-09-17, after both were checked: neither is a misreading, so
  neither is corrected. Document 27 dates the Betsche grant "von 10ten Juny
  1797" where every other copy in the holding reads the 19th. Document 29 is
  subscribed "Breslau den 3ten Novbr 1800" and yet sets out to obey an
  "allerhöchstem Befehl vom 18 November" - the order it answers is dated a
  fortnight after the letter answering it. Both are recorded in the relation
  notes in `rulings.yml` rather than smoothed away, because a reader who
  notices the impossibility should find it already accounted for.

## Paragraphs

Where the reading text breaks into paragraphs is decided in
`paragraph_decisions.csv`, and for this unit the rules are stricter than the
edition's default (`paragraphs:` and `linebreaks:` in `unit.yml`): a line ends a
paragraph only if it is short against the page's own measure AND holds three
words or fewer, unless it closes its sentence; a page's last line counts too,
so a paragraph can begin overleaf; and a page ending in a catchword never ends
one, because the catchword says the sentence runs on. Documents 13 and 14 are
registers - an inventory and a forest valuation - and are shown one entry per
line rather than flowed.

389 breaks out of 561 candidates, none left pending: 227 were decided by hand,
the rest left to the rules. Every candidate the rules were unsure of, and every
automatic break that looked wrong, was decided on these principles:

- **Break** at a heading (`Copia`, `Hypothequen-Schein`, `Titulus
  possessionis`), at a new clause where the sentence ended without punctuation
  (`männiglich ungehindert` / `Wir befehlen…`), before a dateline, between
  separate signatures, between the items of a fee list, and before an archive
  number.
- **Run on** within a phrase: a name and its title (`Beda Ingrossator`), an
  address after `An`, an endorsement (`Verleihungs-Urkunde für den regierenden
  Fürsten…`), a list of villages that is part of a sentence, a letter's closing
  formula, and the cells of a table header.

Two machine cues were wrong often enough to be worth naming. A line ending in
an abbreviation (`des Hochfürstl.`) looks like a closed sentence; and `v.`,
`c.`, `d. J.`, a day number or a sum at the head of a line (`den | 28. Januar,
1798.`) looks like a section number. 17 such breaks were reversed by hand; the
numbered clauses of the deeds themselves are genuine and were kept.

## Summaries (written again 2026-10-08)

The first summaries were written by the model from the English translations,
and the German beside them was never checked. At the editor's word
(2026-10-08) they were written again in a working session: every document read whole in
its German text, a German summary written from that reading, the English
translated from the German, and each of the 212 statements held to the
document (`intake/summaries_draft.py`, `intake/claim_check.yml`). The script
writes `summaries_de.yml` and replaces this holding's lines in the site's two
summary files; it applies the English digit grouping itself. What the reading
found:

- **Documents 3 and 4** (copies of the grant of 1796 made in 1798 and 1802):
  the text of the deed names only Kamionna, Kolno and Brzyce; Trąbczyn and the
  other villages of the Konin district stand only in the endorsement.
  Document 1 has the full list. The scans (0010_a2, 0012_a2) show that both
  copyists wrote it so; it is not a line lost in transcription. The summaries
  say what each copy says.
- **Document 7**: the Kalisz attestation was transcribed "7. July 1804". The
  scan (0021_a2) reads 1801, as the same attestation does in document 22, and
  the copy is itself certified in 1802. Corrected in the corpus, the page file
  and the English (`transcription_decisions.csv`, key 7030ab57;
  `reference/english_corrections.yml`).
- **Two dates on the site are not the documents' own** (in
  `docs/NEEDS_CONFIRMATION.md`): document 13 is dated 22 July 1794, which is
  the date of the West Prussian valuation principles it applies (the
  correction of the valuation is attested at Berlin on 16 May 1804); document
  21 is dated 25 January 1804, the date of a settlement it mentions, while the
  extract is certified at Kalisz on 18 September 1811 and its entries run to
  1806.
- **Document 21's bond** for Triebenfeld's 250,000 Rthl is dated "1 Juny
  1814" in the text, which cannot be (it was entered in 1804); left as
  written, and the summary gives no date for it.
- **Documents 39 to 41** (Hoym's letters of 1796 and 1797, certified copies)
  say the most about how the grants were meant: the Prusimski estates were
  burdened with debts, so the church estates were added in 1797; the handing
  over of 1797 was "a superficial ceremony", and the Chambers were told to
  examine the claimants' contracts and hand the estates to the Prince's agents.

## Damage

None recorded beyond what the transcription itself marks: 56 `[?]` readings
and 7 `[...]` gaps. Both counts are unchanged by every pass made on this unit,
which is how the apply step proves it altered no reading.

## Sweeps carried over from 9454 (2026-09-28)

- **Line-end marks.** 10 words broken with - / ‗ / = now take ¬. Of 103 ¬ the line-break resolver did not join: 37 real breaks held as `join` (Latin, Polish, names, period spellings); 22 stray ¬ between whole words and 12 compounds written as two words lost the mark (Landes Eingeborne, Real Verbindlichkeiten, Ober Amts); Bau- und Brennholtzes keeps a real hyphen; 6 lost endings supplied in brackets (seit ger[aumen] Jahren, Che[f] eines Regiments, aus Kö[niglicher] Macht); 12 misread halves or words fixed (un → und, Verleihe → Verleihung, Einschrän¬kungen, Beschleu¬nigung, Christi¬ane). Left: un¬ nicht (letter 13), Rein¬ so (18), Remo¬nern (34), Sei¬strum (38), Rech¬ B (41).
- **Nonwords.** 13 fixes after the DWDS pass (Ingrostator, Hohenlot, Nachkommn, Mescritz, Johanniy, Liebde; Zagórów, Grądzyń, Cujavien to the unit's standard). Latin and Polish forms left.
- **Watch-list.** Majestät, Summa, sign-offs, French, Johanni, Rußland, Pohlen, Posen: nothing to fix. Titles E[wr]. K[önigliche]. M[ajestät]., E[wr]. M[ajestät]., K[önigl]. Reg[ierung]. expanded.
- **Names aligned with 9454 (2026-09-28).** Glenk → Glenck, Schenk → Schenck, Radzinsky → Radzinski, Hirchel → Hirschel, Eichaust → Echaust (as he signs), wherever they occur in this unit. Place names deliberately left in this unit's own forms.

## Place names: German in the text, Polish (German) on the site (editor 2026-09-28)

The transcriptions show the German name the letters use wherever a place has one - Zagorowo, Kaemen, Peisern, Kalisch, Wittow, Betsche, Breslau - including Germanised spellings of Polish names (Kopoyno, Stalluhn, Lowin, Schartzig, Kulligowo, Swiegaszin). Places with no German form (Trąbczyn, Swięcia, Drzewce) keep their Polish spelling, and pure diacritic fixes of a Polish spelling stand (Głażewo, Stołuń, Wieluń, Przybysław). Frankfurth is the edition's spelling of Frankfurt an der Oder. The Polish names are recorded, not printed in the text: `reference/places.yml` gives each place now in Poland its Polish `display` and a `german:` field, and the site names it "Polish (German)" wherever places are listed - Zagórów (Zagorowo), Kamionna (Kaemen), Wrocław (Breslau), Poznań (Posen), Koszęcin (Koschentin). This replaces the brief "Polish everywhere" ruling of the same day: its 309 changes were reversed, and 14525's estate-spelling pass of 2026-09-15 was reversed for German forms. Bornstädt is the established form of that name; Schulze (Geheimer Finanzrat), Schulz of Strelitz and Wilhelm Daniel Schulz are separate index entries.
- In Polish documents and Polish passages (9454 letter 72e; the Polish extract in 14525 letter 21; the Polish original in 14526 letter 30 and the Polish statements in letter 9) place names stay in Polish as written: Dobr Zagorowa, w Kaliszu, Maiętnosći Zagurowskiey (editor 2026-09-28).
- **English translations use Polish place names (editor 2026-09-28).** The published translations and summaries were changed from the German place names to the Polish (Breslau → Wrocław, Posen → Poznań, Betsche → Pszczew, Kaemen → Kamionna; Warsaw kept as the English name); the German column of each segment's name list keeps the German. Future translation runs take the Polish name from places.yml through the glossary.
