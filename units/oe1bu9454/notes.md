# Oe 1 Bü 9454

318 documents, 869 manuscript pages, 1798 to 1816. The backbone of the edition.

## Provenance

Hohenloher Zentralarchiv Neuenstein. 549 archival scans, each a two-up photograph of
one or two document sides. Cropped to 872 single pages by `crop_scans.py`, with the
bifolium cases split again by `split_spreads.py`.

## Transcription

Machine-transcribed from Kurrentschrift, not by a human palaeographer. That shapes every
editorial decision in `rulings.yml`: the failure mode is plausible German that is not what
is on the page, so readings that could not be settled from evidence were left alone rather
than guessed at.

## Quirks worth knowing

- **The archive's numbering is not chronological.** Letters 1 to 74 are a jumbled block
  spanning 1806 to 1815; 75 to 301 run in order from 1798. Numbers 302 and 303 sit outside
  the sequence.
- **Several archival numbers hold more than one document**, split into sub-records: 72 into
  72a to 72f, 74 into 74a to 74e, and so on. Each keeps a link back to its parent.
- **Three documents survive in two copies**: 48 and 302 are the same letter of 7 March 1809
  transcribed twice, as are 72d/72e (German and Polish) and 118b/118c. The duplicate pairs
  are the only place in the corpus where two independent transcriptions of one page can be
  compared, which is what makes them valuable.
- **One financial figure differs between the two copies** of the 7 March 1809 letter,
  23,000 against 32,000 Rthl. Both are faithful to their own page, so the discrepancy
  belongs to the original copyist.
- **Letter 72e is Polish and 283 is French.** Everything else is German.
- **Four archival numbers have no surviving text**: 121, 181, 225, 293.
- **150 uncertain readings** stand marked in the text, 98 illegible and 52 offered as
  guesses.
- **Letter 48's two page-image pairings were never human-confirmed.** They are
  `status=auto, confidence=check` in the scan map, and 48 is the corpus's accuracy
  benchmark, so it is worth an eye.

## Damage

Five passages are damaged. Their line ranges are in `rulings.yml` under `damage`, and the
loader now validates each against the corpus line count. Two of the five ranges that had
been hardcoded in `build_db.py` pointed past the end of the file, which is why `has_damage`
was false for every record until this was fixed.

## Correcting the 2026 transcription

The new transcription (September 2026) is a fresh machine reading, hand-corrected by the
editor for names and layout. Everything else still carries the machine's errors. It shares
94.6% of its words with the old transcription, so the old one is not an independent check:
where the two differ, that is a place to look, not a verdict. The old rulings are treated
as candidates only, because some rested on words around them that were themselves misread.

What gets corrected without asking: one word for one word, close in letterform (0.6
similarity or better). The evidence must be more than "it reads better": the twin copy
(48/302), the same word written correctly elsewhere in the same document, the corpus
attesting the word several times, or a fixed phrase (`in Stand gesezt`, `Dies laße der
Himmel gelingen`, `am erwünschten Ziele`). Names, figures, abbreviations, Polish, French
and Latin are never changed, and neither is anything that would change the meaning.

A word that is clearly wrong but has no correction that meets that bar is left as
written, with no `[?]` added. It is logged in `review/oe1bu9454/unresolved.md`, and only
the few where meaning is at stake go to the editor.

How this machine goes wrong, from the pilot:
- **zz read as pp**: `unterstüppen`, `ersappen`. Triebenfeld doubles z (`besizze`,
  `durchsezze`), and corrections keep his spelling.
- **ß read as b**: `weib`, `lieb` for `weiß`, `ließ`.
- **m/w and w/r**: `gemiß`, `gemartet`, `Rückweise`, `Wollmacht`.
- **A real word swapped for the right one**: `bewürbt` for `bewürkt`, `geringen` for
  `zwingen`, `gelegen` for `gelingen`, `gewesen` for `genesen`. Only the sense catches these.
- **Don't complete a broken word from a fixed phrase in another language.** The pilot
  turned `me¬mora` into `me¬moria` (Pro Memoria); the editor read `me¬moire` on the
  scan, the French *mémoire*. He writes French terms freely, so a wrapped or broken
  word is completed only from a witness (the twin, the same word elsewhere in the
  letter), never from what the phrase is usually called.
- **Recurring misreadings too far from the page form to fix one by one**: `Eine
  Durchlaucht` for `Ewr Durchlaucht` (42 lines), `Jagt` for `Jezt` (12), `Schaden Sie`
  for `Schicken Sie` (5). These wait on an editor's ruling.

Every applied change is in `units/oe1bu9454/transcription_decisions.csv`, with its reason,
and in `review/oe1bu9454/transcription_fixes_applied.md`, with the line before and after.

Two rules added after the second spot check (2026-09-27), because all three of the
editor's corrections so far were readings taken from sense rather than from a witness:
- **No corrections inside a largely garbled letter** (17, 114, 138). When the words
  around a slip are themselves unreliable, a repair builds on sand: `Räumig` in 138 went
  to `Räumung`, and the editor, looking at a messy hand, doubts it. Those letters wait for
  a fresh reading; the five fixes already made in them were reversed.
- **A real word is replaced by another real word only with a witness**: the twin, the
  same letter, or a fixed phrase attested elsewhere in the unit. `muß er rest stehen` was
  changed to `fest` on sense alone, and the page says `rest`.

Two exceptions to the similarity bar, both deliberate. The editor ruled three
recurring misreadings to be corrected wherever they occur: `Eine Durchlaucht` (Ewr),
`Jagt` (Jezt), `Schaden Sie` (Schicken), and on 2026-09-27 also `Jedes` used as a
conjunction (Indes, 28 lines; the determiner *jedes* left alone) and `schulen` in a
request to send (schicken, 5 lines; `Schulen` for *Schulden* left alone). And a two-letter non-word with only one reading (`Iu` for `In`) is
corrected, because a similarity score on two letters means nothing.

Names the editor had already corrected elsewhere are corrected where the same letter
spells them right: `Metzer` for Melzer, `Metzig` for Melzig, `Gencks` for Glenck.

Pilot spot check (2026-09-27): the editor checked 19 of the 109 pilot changes against
the scans. 18 were right; the one miss is the `me¬moire` rule above.
Second spot check, batches 1-3: 21 of 22 right; the miss was `rest`, above.
Third spot check, batches 4-6: 24 of 25 right. The miss was a spelling, not a word:
`Jahrlehns` went to `Darlehns` and the page has `Dahrlehns`. A slip is mended to the
form nearest the page letters, keeping his own spelling, not to the standard one.

Fourth spot check, batches 7-9: 24 of 25 right. The miss was again a word completed from
a fixed phrase: `Töchte` went to `Dichten` ('Dichten und Trachten'); the editor reads
`Tieften[?]`. Both misses of this kind (`me¬moire`, `Tieften`) came from a phrase alone,
with the page word well away from the phrase word. From batch 10 on, a fixed phrase is
evidence only when the page word is close to it (similarity 0.75 or better); below that it
needs a witness in the letter itself.

The old transcription is a useful witness for place names: where it read a place the
edition knows and the new text has a non-place (`Breiten`, `Wun`, `Beedlau`, `Uria`), the
new text is wrong. Ten such were corrected on 2026-09-27; the editor confirmed Breslau
(177) and Brieg (260) on the scans.

- Letter 213, line 88: I had corrected `Feeder` to `Feder`. The editor reads the page as
  `Fe[e?]der`, and that reading now stands. A doubled letter may be his own spelling, so
  a nonword that differs from the right word only by a doubled letter is left alone.

- `d` after a figure (2026-09-27). The transcriber often read `rt` as `d`, but `d` is also
  the pfennig mark (`14 gg 11 d`) and `d.` a date (`den 22 d.`). A `d` after a sum in the
  thousands is `rt`: nobody counts that in pfennig. It was changed in letters 1 (the editor's
  reading), 31, 35, 38, 213 and 221. After gg, or in a date, `d` stays. Small sums (letters
  19, 68, 180, 191, 208) could be pfennig or ducats and are left for the scan.

- Spot check, batches 13-16 (2026-09-27): 24 of 24 answered rows correct. The 25th,
  `frange` -> `fange` in letter 277, was the editor's own query and now reads `fienge`.
  All sixteen batches are done: the pass is complete.

- `d` after a figure, settled on the scans (2026-09-27): every `d` after a plain figure the
  editor checked was `rt`, small sums included. `d` is pfennig only after gg (`14 gg 11 d`).
- Hube/Huben is his form in the letters of 1805-06 (confirmed in letter 173); Hufe/Hufen
  elsewhere. Neither is corrected to the other.
- Letters 48 and 302 are twins that really differ at line 8 (Abweisung / Anweisung).

- Doubt marks resolved from context (2026-09-27). At the editor's instruction, the [?]
  words were read against their context and decided without a per-word review: 95 words
  settled (97 marks), each with its reason in transcription_decisions.csv, and every
  changed line re-read afterwards. Abbreviation expansions such as Cur[landische?] were
  not touched. Letter 41 now reads "Mein Tichten und Trachten" (the editor sees a T;
  Luther's wording, Genesis 8:21). Left marked because the context allows more than
  one reading: facule (626), cst (753), rt d'or (3081), prore¬netica (3202),
  Klag: Courant (3254), Resoussten (3985), [?]ammern (12051), Sliedt (12972),
  decontinanciert (13606), Labirath (13637), monreniren (17475), plus about 320 names,
  figures and garbled phrases that need the page.

- Beguelin (2026-09-27): the name was standardised as "Beugelin"; his own signature
  (letter 283) is Beguelin, Heinrich von Beguelin. Corrected in all nine places, in
  reference/name_rulings.json, name_seeds.json and derive_correspondents.py.
- The editor's own expansions checked against context (2026-09-27): 73 confirmed (the
  ? removed, the bracket kept to show the letters were supplied); 36 corrected, among
  them [C?]rbe -> [Ba]rbe, Allanten[Allantezers?] -> Alentours, Eisen[hardt?] -> Eisen
  (iron), [f?]oulagirt -> [s]oulagirt, [L?]atente -> [T]alente, Gu[r?]l -> Curl. About 65
  are left marked: figures, dates, unknown names and places, and letters the context
  cannot fix.
- Cur. expands to Cur[ische], his own full form (Curische(n) 38 times); Curl. to
  Curl[ändische] (Curländische twice). Corrected 2026-09-27 at the editor's query.
- Settled letters lose their brackets (editor, 2026-09-27): [T]alente -> Talente. Brackets
  stay only where they expand an abbreviation (Cur[ische], K[öckritz], St[ein]:). The
  abbreviation is Cur., never Curl.: the four Curl forms and Curl[ändische] were corrected.

## Names and places pass (2026-09-27)

- 30 name misreadings corrected in the text, each against the correct form in the same
  letter or throughout the unit (Steyemann -> Stegemann, Winzingerock -> Winzingerode,
  Krotosryn -> Krotoszyn, Bertenstein -> Bartenstein, Metterich -> Metternich ...).
- His own spellings are NOT normalised in the text (Köchritz, Steegemann, Humbold, Glenk,
  Franckfurth). They are recorded as variants in reference/people.yml and places.yml, so
  the index finds each person under one entry. Köckritz, Stägemann, Humboldt, Hardenberg,
  Schlabrendorff, Eysenhardt, Göschel, Talleyrand, Schenck, Meierowitz and Trzciński no
  longer split across two or three entries.
- New entries: Beyme, Hohenlohe-Bartenstein, Radziwiłł, Gneisenau; Sachsen, Krotoszyn,
  St Petersburg, Bayern, Meseritz, Polnisch Wartenberg, Frankfurt am Main (kept apart from
  Frankfurt an der Oder: "am Main"/"a/M" decides). Dresden and Öhringen now match the
  plain spellings Dresden and Ohringen.
- name_catalogue.py rewrites reference/name_seeds.json as a side effect, with a much
  looser list (325 seeds against 198); a rebuild then indexes words like Gottes and
  Johanni as people. The committed list was restored. Do not keep its seeds export.
- Standardised (editor's ruling, 2026-09-27): 345 name spellings in the text now use the
  correct name - Steegemann/Stegemann -> Stägemann, Humbolt -> Humboldt, Köchritz ->
  Köckritz, Taillerand -> Talleyrand, Eberhardt -> Eberhard, Beym -> Beyme, Portalis ->
  Pourtalès (except letter 266, where he corrects "Pourtales / nicht Portalis" himself),
  Trzcinski -> Trzciński; places to one spelling (Trąpczyn -> Trąbczyn, Schlawenzitz ->
  Schlawenschitz, Kontopp -> Kontop, Franckfurth -> Frankfurt, Ohringen -> Öhringen,
  Sachßen -> Sachsen). German place names are kept where the index heading is Polish
  (Zagorowo, Kaemen, Wittow, Peisern). Married names stay distinct (Dąbska, Moscinska).
  This supersedes the earlier rule to keep Humbolt, Ohringen, Kontopp and Zagarow.
- Index fixes: Wien no longer matches "Wein" (wine, Weinachten); Eberhard, Stössel merged.
  Known misfile: letter 10 line 22 (1815) "in Frankfurt" is Frankfurt am Main but is
  counted under Frankfurt an der Oder, since a bare "Frankfurt" cannot be told apart.
- Trieb is Triebenfeld: letter 20 "v Trieb:" expanded; "Triebunal" -> Tribunal (217);
  "Triebstender" -> Triebfeder (158). Stocki is a village in 14526 (docs 18, 19), not
  Otocki. Radozimski (14526 doc 28) against Radzinski is with the editor.
- Winnica = Wieniec (editor, 2026-09-28): "Winicer Forste" (letter 103), "nach Winnica …
  die Uebergabe an Dąbrowski" (136) and "Winniec" (286a) are all the Cujavian estate
  Wieniec; merged in reference/places.yml and in the estates in focus. Otocki (a person,
  9454) and Stocki (the Betsche village Stoki, 14526) were already separate entries.
- Estates in focus for all 314 letters are in rulings.yml, documents: estates, with the
  rules at the head of that section (majorat, Pohl Güter, Güter Tausch; datelines,
  chanceries and journeys excluded).
- Names pass, second round (2026-09-28): 53 people and 85 places added to the index
  (Prinz Adolph, Prinz George, Constantin, Landskoy, Stenger, Bally, Albrecht, the Kuh
  brothers; Warschau, Paris, Neisse, Rußland, Württemberg, Memel, Stettin, Boyadel,
  Grüneberg, Karge, Ruschinowitz ...). Michelis is the merchant Michaelis, not a date;
  the text now says Michaelis. 21 further misread names corrected (Tiorge -> George,
  Treibenfeld -> Triebenfeld, Bennebirg -> Henneberg, Kaemin/Kelm -> Kaemen/Kulm ...).
  Magdeburg matches only "zu/nach/von/in/bis Magdeburg": the deeds' "Hufe Magdeburg" is
  a measure. The one-off names still without an entry are listed in
  review/oe1bu9454/names_without_entry.md; the register of creditors (303) is not indexed.
- Watch-list: Hawich (editor, 2026-09-28). The transcriber misreads this name often -
  Habisch, Habich, Habik, Habick (letters 31, 302), Hawick (198). All now read Hawich;
  the forms are variants of his entry in reference/people.yml. Check any new H-a-?-i-?
  name near Zagorowo, the Justiz or a Vollmacht against him first.
- Unidentified names read on the scans by the editor (2026-09-28): Wirr -> Wien, Türth ->
  Fürth, Münse and Nüsse -> Neisse, Peision -> Peisern, Ulre -> Ulm, Palzen confirmed;
  tentative, so still marked: Neasal[?] (letter 66; perhaps Neusalz, named in the same
  letter), Neufallen[?], Spiane[?], Sa[?]en. Syten, Brafurt, Sansenberg, Scharnewand are
  as written. Lottom[?], Stache[?], Ternuis[?], Rewen[?] remain unread.
- Titles (2026-09-28): 15 misread titles corrected (Gehl/Guhl/Ghl/Gel. Rath -> Geh. Rath,
  Gehen Stadt Rath -> Geheimen Staats Rath, Gnl. Leg. Rath -> Geh. Leg. Rath, Haßrath ->
  Hofrath, Geſame -> Geheime, Referandurius -> Referendarius). The editor's expansions were
  aligned with the standardised names (Hard[enberg], Humbo[ldt], B[eyme], Tal[leyrand],
  Gneis[enau], Krot[oszyn], W[ürtemberg]). Then, at the editor's ruling, each title's
  spelling standardised to his most common form: Hoffrath, Krieges (und Forst) Rath,
  Staats / Fürst Kanzler, Bürgermeister, Prefect / Podprefect, Cabinets Rath, Medicinal
  Rath, Justiz, Justiz Commissarius, Secretair, Ober Landes Gericht, Landrath.
  Abbreviations are left as written (K. R., Cab:, O. L. G., J. C.).
- Title abbreviations expanded in brackets (editor, 2026-09-28): Gen[eral], Lieut[enant],
  Geh[eime / eimen / eimer] by the word before it, Min[ister], Exc[ellenz], Ass[essor],
  K[rieges]. R[ath], Kr[ieges]. Rath, C[abinets]. R[ath], Cab[inets], St[aats]. K[anzler],
  J[ustiz]. C[ommissarius], O[ber]. L[andes]. G[ericht], O[brist]. L[ieutenant] (letters
  288, 290), O[ber]. P[räsident], M[edicinal]. R[ath]. C[osmar], Hoffr[ath], Trib[unals].
  "Gen. St. R. Stägemann" (letter 2) is Geh[eime]; "Geh. Lab. Rath B." (179) is Cab[inets].
  Left unexpanded as undecidable: H. z. M. v. Kirche[?] (8), H. M. v. Pirch (59), Gen.
  Haugwitz (79), Sr Min. Sanitz (245), pp. Min. (239), H. C. R. R. N Weigelts (64),
  H. R. R. Falz (207), Gl. (56, 297), Geh. Ewang Rath (78), Geh. Einweg Rath (81, perhaps
  the Geh. Finanz Rath Schulze of letter 83), K. R. Bernhardi (152).
- Abbreviations read on the scans (editor, 2026-09-28): H. M[ajor]. v. Pirch (59); Geh[eimen].
  Finanz Rath for "Geh. Ewang Rath" (78) and "Geh. Einweg Rath" (81) - Schulze, as in 83;
  Gr[af]. Haugwitz (79); pp. Min[ister]. (239, Hardenberg follows); Sr Maj[estät].
  Sanct[ionirte] Acte (245); "Gl. F." reads Gr. F. (297). K. R. Bernhardi (152) stays.
  Open: H. C. R. R. N Weigelts (64; the editor sees perhaps H. C. K. K. N.), H. R. R. Falz
  (207; Regierungs Rath not supported), H. z. M. v. Kirche[?] (8), Gl. Listog[?] (56).
- Trial second reading, letter 251 (2026-09-28): read blind by Claude from the uncompressed
  original scan (J:\...\Oe 1_Bü 9454\processed), cut into enlarged strips; no API. The
  editor checked the 27 differences on the scan: the trial was right on 23, right in the
  word but not the detail on 2, wrong on 1 (Allersebnißest stands), 1 undecided (ihm/ihn).
  26 corrections applied. The project's own scans are compressed (1100x1450, 350 KB
  against 1268x1671, 1.3 MB): use the originals for any re-reading.

## Trial reading, letter 144 (2026-09-28)

A second reading of letter 144 (Amelang) from the original scan was put to the editor as a spot sheet. Ten of fourteen rows confirmed: Befehl vom, dem Graf, Schulenburg, nähere, meiner, einzuberichten, der, unterthänigster Diener. Not decided: v. h. (possibly v. M. or c. h.), Früh/früh, and thenigtes (Unter-thänigkeit), which stay as written. My first pass misread four phrases the current text had right, so I'm not trusted as a blind reader, only as a check on garbled words.

## Garbled letters: fixes with a witness (2026-09-28)

The paid second reading was tried on letters 144 and 251 and rejected: Opus 5 matched 56% of the confirmed words of 251, Opus 5.5 72%, against 89% for the recognition model's own text. The editor then asked for three free routes instead. The rule "no corrections inside a largely garbled letter" is narrowed, not dropped: inside those letters a word is changed only when a witness settles it, and never on sense alone.

- **Fixed formulas.** Address and closing formulas (Durchlauchtigster, Hochfürstlichen Durchlaucht, Hochwohlgebohren, in tiefster Ehrfurcht ersterbe, habe die Ehre, zu Füßen).
- **The corrected form is used elsewhere.** The new word or phrase must occur in the unit's other letters (checked with a phrase count across all three units), or in the same letter. A form the letters never use is not brought in, however likely.
- **One reading.** A handful of non-words where the sentence allows only one word (abgefeimter Bube, dienstags höchstens Mittwochs, das Heer Ihrer General bevollmächtigten).
- **Copies.** No garbled letter has a copy, draft or quoting reply in any of the three units: a shared rare-phrase search finds the known twins (48/302, 118b/118c) but nothing for these.

220 fixes in 26 letters. No doubt mark was removed; figures, dates and the editor's marks were not touched. Much stays garbled and is left as written.

Spot sheet on the garbled-letter fixes (2026-09-28): the editor checked 10 of 20. Seven confirmed, two undecidable from the page (gesezt, gerechnet: kept, as the grammar decides them), one wrong: letter 8 `schweizt` -> `schweigt`, where the page starts sp-; now `Spreizt[?]` on the editor's reading. The miss was a non-word with more than one plausible repair; the formula and same-letter fixes all held.

## Nonword and line-break sweeps (2026-09-28)

- **Nonwords (47 fixes).** The project's spelling audit (rare form one Kurrent slip from a common one, checked against DWDS) gave 76 hits in this unit; 32 were slips, the rest period spellings (Augenblik, Zukunfft, gebetten, dardurch) and were left. A second pass looked only at near-misses of the formula words (Durchlaucht, Hochfürstl., Hochwohlgebohren, Durchlauchtigster, verharren) and fixed 15 more.
- **Line-break words (51 fixes).** Each word split with ¬ or - was joined and checked against the vocabulary of all three units. Of 174 hits most were dashes used as punctuation or correct words; 51 were misjoined or misread halves (Stage¬mann, Abla¬ben for Able¬ben, Vorsche¬rung, ge¬blacht, Schim¬melfennigs). Only the broken half was changed; the break stays where the page has it.
- **Wider nonword sweep (73 fixes).** The audit was rerun on this unit with a lower bar (any single-letter difference, words of 5+ letters, a neighbour used 5+ times): 2,157 hits. Period spelling variants were dropped by rule, and every remaining rare form was looked up in DWDS; the 200 that DWDS does not know were read one by one. 70 forms were clear slips (Revenien, Puppiere, Hypothique, Magestät, Polagewo, Krotoczyner, Pourtales, Kaeminer, unsomehr), fixed wherever they occur. The rest stay: period forms, doubtful contexts, and names the editor has open (Rewen).

## Line-end marks (2026-09-28)

The editor's convention: a word broken at the line end is marked ¬; a real hyphen (a compound written with -) or a dash stays -.
- **- changed to ¬ (61 lines).** A word broken at the line end with an attached - (Ver- / mögen, Durch- / laucht, kön- / nen), plus one ‗. Left as -: compound hyphens (Haupt-Ersaz, Hypothequen-Scheine, Zahlungs‗Sistirung), dashes written against the word before a new sentence (Kinder- / Ich habe), and every spaced dash (checked: none hides a broken word).
- **¬ changed back to - (73 lines).** ¬ stood where no word is broken: a whole word at the line end and a new word or sentence on the next line (Herz¬ / Der Bericht, Monath¬ / Eine, Gesund¬ / und glücklich), and ten compound hyphens (Vestungs¬ / Strafe, Ober¬ / Consistorial, Cammer¬ / Director, Zeit¬ / Verhältnisse). These look like dashes caught up in the change to ¬; the reading copy would otherwise run the two words together. Truncated words before a new sentence (abgefü¬ / Ich) were left, since the page may break there.
- **Split-word DWDS pass (24 fixes).** Every word broken with ¬ that occurs nowhere unbroken was joined and looked up in DWDS; of 271 unknown forms, 24 were clear misreadings of one half (Bä¬sowicht, Ver¬schauungen for Verschanzungen, Ober¬schließen for Oberschlesien, Add¬nau for Adelnau, verne¬theilt for verurtheilt).
- **Correction to the 73 (editor 2026-09-28).** The transcriber sometimes put ¬ at a line end where no mark was needed, so each of the 73 was judged again on its own: 46 end a sentence before a new one and keep the writer's dash, spaced as elsewhere (Herz - / Der Bericht); 27 need no mark at all and it is removed - 17 where the phrase simply runs on (recht Gesund / und glücklich, bey Ihm war / befallen) and the 10 compounds, which these letters write as two words (Vestungs / Strafe, Cammer / Director). The resolver had already treated all 73 as not joined, so the reading text was never run together; the earlier change to - had briefly put a stray hyphen into it. No other line-end - was touched.
- Three of the 61 new ¬ breaks were judged "split" by the line-break resolver because the joined form is a period or garbled spelling (abge¬reißet, über¬wurden, Ze¬tressen); they are held as "join" in linebreak_decisions.csv.
- **The remaining ¬ marks (2026-09-28).** Of 1,111, the line-break resolver joined 941 on evidence. The 170 it did not were read one by one: 43 are real breaks whose joined form is a period, Latin or name spelling (Phi¬lipsborn, Solcher¬gestalt, 23¬ten) and are held as "join"; 23 were stray ¬ between two whole words and removed (gab den Dienst¬ / auf); 11 were real breaks with a half misread and fixed (Ge¬unsung → Ge¬nesung, Wa¬nehmen → Ver¬nehmen, ver¬eigerte → ver¬weigerte); 5 are damage or catchwords and stay. The other 88 - mostly a word whose ending the transcriber lost before a new word (gezüchtiget wer¬ / Hecker) - went to the editor as review/oe1bu9454/break_queries.csv.
- **The 88 queried breaks (editor 2026-09-28).** The editor answered two (nie / aber; sah¬ → Sache). 19 lost endings where the sentence requires one word were supplied in brackets (wer[den], wür[de], erwünscht[en]). For the rest I cropped the original scan at each line end and read it against the candidates: 46 settled (stray ¬ with the word misread, e.g. Wahr¬ → Woche, zie¬ → zur, Sen¬ → Sie; or a real break with a half misread, e.g. Pro¬daß → Pro¬zeß, Ur¬druk → Ur¬laub, Azan¬giment → Aran¬gement). 22 stay as written, in review/oe1bu9454/break_queries_left.csv: the crop missed the line, or the page does not settle it.
- **The last 22 breaks (editor 2026-09-28).** All answered on the spot sheet and applied as the editor read them; letter 47 unglaub¬ became ungeduldig on the editor's request for the likeliest word. Two stay as written (letter 72f erb¬, letter 223 ver¬: obscured).
- **Johanni (2026-09-28).** Six places where the feast day (the Midsummer rent and interest term) was transcribed Johann - after auf, gegen, bis, and Weinachten und Johann ab - now read Johanni; Johs expanded to Joh[anni]s. Left: Johann as a first name (letter 303), Ober Johann[?] in letter 287 (possibly Archduke Johann), and zwischen Johann Fürstens in letter 231.
- **Brzechffa (editor 2026-09-28).** The transcription's Brzechsta (63 places) is standardised to Brzechffa, the family Brzechwa vel Brzechffa, herb Jastrzębiec. His signatures read Brzechfa (72d) and Brzechffa (72e). New curated entry in reference/people.yml; seeds, name rulings and glossary updated.
- **Brzechffa confirmed (2026-09-28).** The editor found him in Kaliski wysiłek zbrojny 1806-1813: 'pod prefekt pow. konińskiego Brzechffa', writing from Konin on 14 May 1809 to Różnowski, podprefekt of Pyzdry (Bibl. Uniw. Warsz. rkp. 210, t. XVII). This confirms both the spelling and his office: sub-prefect of the Konin district. No first name given.
- **Editor's watch-list (2026-09-28).** Königl. Majestät (2 misreadings), Suma → Summa (2), sign-offs zu/Im → In (16, plus erſt erbei → erſterbe), stray French (7 fixed: un → und, par forte → par force, pas → par, et → v, forzon → façon, grè → gré, and two lost breaks where 'de' was the end of a German word). Seven doubtful ones on review/oe1bu9454/watch_queries.csv. Genuine French phrases (au fait, par force, feu de paille, pour parlez, plus ultra) and the French letter 283 are left.
- **Niedźwiecki (editor 2026-09-28).** Niedziewiecki (17, 9454) and Niedzwiedzki/Niedzwidzki/Niedzwiecki (10, 14526 letter 9) standardised to Niedźwiecki; one person, Maciej Niedźwiecki, lessee of Kopojno and the Propination, who signs Maciey Niedzwiecki. **Propination:** all three units searched for lookalikes; one misreading (Propinaten, letter 169). The two Proposition in letters 223 and 230 are real proposals and stay.
- **Single-letter name initials (editor 2026-09-28).** 45 expanded in brackets where the same letters or period settle them: B[arbe] (30, the Vienna letters 1814-15), B[eyme] (Cabinets Rath B., 2), K[öckritz] and G[eneral]. v. K[öckritz] (5), Z[astrow], Z[erboni], T[riebenfeld], V[oss], P[ourtalès], C[urische] Erben / Mandatarien (3). Title initials (E. M., S. M., F. August, K. M.) and the A. of A. Hahn left as written. Eleven uncertain ones on review/oe1bu9454/initial_queries.csv.
- **The uncertain initials, decided on context (editor 2026-09-28: 'you would be able to best').** B[arbe] in letters 3, 15, 242, 246, 274, 287; B[eyme] in 89, 97, 134 and 215 (der Gros Kanzler B); K[öckritz] and Z[astrow] with them in 97 and 89. Left as written: der bidere B (288, Barbe or Beguelin), den B. in 216 (an estate official, not Beyme), A: in 242/246, Gen. B. at Jena (letter 20).
- **Title initials (editor 2026-09-28).** 66 lines: E[wr]. H[ochfürstliche]. D[urchlaucht]., E[wr]. D[urchlaucht]., E[wr]. K[önigliche]. M[ajestät]., S[eine]. M[ajestät]., Sr M[ajestät], des K[önigs]. M[ajestät]., F[ürst]. / F[ürstin]. before names, F[ürst]. H[ardenberg]., F[ürst]. K[anzler]., F[eld]. M[arschall], G[roß]. F[ürst]. Constantin, K[aiser]. Franz / Napoleon, K[önig]. Murat / von Würtemberg, R[ussischen]. K[aiser]., Gr[oß]. K[anzler]. Beyme, M[inister]., P[rinz]. Adolph, Gen[eral] L[ieutenant], O[ber]. P[räsident], O[brist]., K[rieges]. R[ath]., Hoff R[ath]., G[eheime]. Left: H. (Herr, several hundred), date abbreviations (v. M., d. J.), and the unclear ones (K. M. = künftigen Monats in 249/253, das K. M. in 79, Gr. F. in 297, H. C. R. R. N, R. R. Falz, B. R. Glenck, E. M. in 133, S. M. in 288).
- **Rußland / Pohlen / Posen (editor 2026-09-28).** R misreadings of Rußland/Rußisch fixed (letters 68, 205, 246; Rüßland → Rußland in 275). Posen: 38 forms checked, one misreading (Josen, letter 217). Pohlen: misreadings Pohe, Pohn, Pohlnas Lors fixed; 28 abbreviations Pohl / Pohl. / Pohln / Pol expanded in brackets with the case the sentence needs (Pohl[nischen] Güter, Pol[nisch]. Wartenberg, so wenig als Pohl[en].). Left: im Pohl (letter 213), die Pohl allen (letter 199), Alte Pohln. (179, a place in a list), F Bohlen / Bohle (letter 297), Gr. Pohne (letter 55).
- **Letter 254 page order (editor 2026-09-28).** The last page of the letter (scan 0469_a2, 'alle Luftbarkeiten ... v Triebenfeld') sat after the enclosures 254 a-c; moved so the order is the letter's four pages, then a, b, c. Scans relabelled to match (L254_03 = 0469_a2; a-c now L254_04-06). Lines 18137-18205 of corpus.txt changed places, so line numbers recorded before this in transcription_decisions.csv for that range are out of date.

## Rough transcription flag and open questions (2026-09-28)

- 13 letters are marked `rough` in rulings.yml (17, 21, 33, 36, 38, 46, 114, 138, 161, 176, 217, 245, 296): the letter page says the text is still largely an uncorrected machine reading and to check the scan. Take a letter off the list when it has been re-read.
- The editor cannot settle the remaining open questions from the page (letter 64 H. C. R. R. N, 207 H. R. R. Falz, Kircheisen in 8, L'Estocq in 56, Lottom / Stache / Ternuis / Rewen, 144 thenigtes, B. R. Glenck, Gen. B. at Jena in 20, der bidere B in 288). They stay as written.
- Rescans requested for letter 245 (both pages) and 289 page 1: review/oe1bu9454/rescan_request_final.md. The trial reading of 245 (review/oe1bu9454/trial_245.csv, 101 rows) waits for them.

## Place names in Polish, all units (editor 2026-09-28)

The editor ruled that place names take their Polish form in every holding, reversing the earlier 9454 ruling that kept German exonyms. The noun is changed to the form `reference/places.yml` displays (Zagorowo → Zagórów, Peisern → Pyzdry, Kalisch → Kalisz, Wittow → Witów, Stalluhn → Stołuń, Lowin → Łowyń, Schartzig → Szarcz, Kulligowo → Kuligowo, Kopoyno → Kopojno ...); Kaemen / Keemen / Kahmen become **Kamionna [Kaemen]**, since the two names are too different to change silently; Franckfurth / Frankfurt (an der Oder) become **Frankfurth**. German adjectives (Zagorower, Kaemener, Kalischen, Trąbczyner) stay as written, as in the 14525 pass. Places whose edition form is still German with the Polish in brackets (Betsche, Koschentin, Schweinern, Meseritz, Neisse; Posen, Breslau) are not yet changed. Bornstädt is the established form of that name; Schulze (Geheimer Finanzrat), Schulz of Strelitz and Wilhelm Daniel Schulz are separate index entries.
