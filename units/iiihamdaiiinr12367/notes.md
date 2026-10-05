# III. HA MdA, III. Nr. 12367 (GStA PK)

Eleven documents on 15 pages, plus the cover as front matter, 1828-1832:
pieces from the second volume of the Prussian foreign ministry's file on
Michalina Miączyńska's claim, which continues III. HA MdA, III. Nr. 12366.
All of them concern the compensation of the Breslau banker Weigel, whose
mortgage on Trąbczyn the Polish courts had struck out. Added on 2026-10-04:
scans staged and the one opening cut, the editor's text cut to pages,
corrected, summarised, and given its place on the site; translated and its
summaries claim-checked in session on 2026-10-05.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, III. HA Ministerium
der auswärtigen Angelegenheiten, III Nr. 12367 (older marks on the cover: AA.
III Rep. 8 Nr. 4544; Zentrales Staatsarchiv 2.4.1. Abt. III Nr. 12367). The
cover calls it "Vol. II vom Janr 1828 bis ult. November 1833, conf. vol III &
I", with "(1827)" added, and lists six journal dates from 25 January 1828 to
26 November 1833. The volume is thick; the 14 scans are a selection, and
nothing later than March 1832 is among them.

- **Pages.** 0001 is the cover; 0002-0008 and 0010-0014 are single written
  sides (`_a`). 0009 is an opening written on both sides, cut at the fold:
  `0009_a1` the left side, `0009_a2` the right. The editor said it needed
  splitting (2026-10-04). The fold was placed at 0.4894 of the width on an
  enlarged strip of the scan (the detector proposed 0.486, which ran along
  the edge of the figures "16 gr." and "8 gr."); the uncut image is in
  `processed/_spreads_unsplit/`, the fold in
  `processed/_spreads_review/folds.json`.
- The ruler and dark border are left on the images, as for Nr. 12366.

## Transcription

The editor's single Markdown file stays in `<raw_dir>` (put there on
2026-10-04; an older version of 27 June 2026 is in `J:\...\Justin Book\
Hohenlohe Context Files` and was not used). It marks the scans each piece
covers in square brackets. `intake/build_pages.py` cut it into
`transcriptions/<page id>.txt` and wrote the document boundaries
(`intake/document_boundaries.csv`, copied to `review/<slug>/`). It checks
that the pages add up to the source text.

- **By paragraph**, except Weigel's German letter (0009 left and the top of
  0009 right), which the editor transcribed line by line with `¬` at broken
  words. `rulings.yml pages: by_paragraph:` lists every other page; 0009
  right is named for document 8 alone ("8:0009_a2"), a form added to
  `build_db.py` and `resolve_paragraphs.py` for this page.
- **Where the text is cut:** 0006 begins "à la décision de", 0012
  "circonstance j'ai fait", 0009 right "Hierdurch hat sich", 0010
  "Jakkolwiek WWPan". The file has no mark for 0010; document 8 begins on
  0009 right at "Nro. 77775".
- **Datelines** stand where the editor put them, at the head, though on
  0011, 0013 and 0014 they are written at the foot.
- **Markdown taken off:** escapes, bold and italic; `*` after a word is
  rendered `[?]`.
- **Paragraphs and line ends of Weigel's letter** were set by hand:
  three words broken at the line end joined (Anerkenntniße, Hochdieselben,
  bezweifelnden) and seven paragraph decisions, three of them rows with cue
  `hand` in `paragraph_decisions.csv` (a form `resolve_paragraphs.py` now
  carries over).
- Not transcribed: the German translations beside the two Polish letters,
  the addresses at the foot of 0005, 0007, 0011, 0013 and 0014, the
  signatures on 0007, 0012 and 0014, a sideways line on 0004, journal numbers
  and dockets. See `intake/unresolved.md`.

## The signature the editor asked about (2026-10-04)

"[L. C. d. Mo…heim?]" is "Le B[ar]on de Mohrenheim". On 0002 it is written
out, "Le Bon D. Mohrenheim" with "on" raised; on 0004 "L. B. d. Mohrenheim"
(the B was read as C); on 0006 plain "Mohrenheim"; on 0003 only the initial
"M" (transcribed "Me[?]"). All four carry the same paraph, a long loop with a
3-shaped hook at its right end. The letterhead of 0002 and 0005 is "Royaume
de Pologne. Affaires Etrangères".

He is Baron Paul von Mohrenheim (1785-1832), general secretary and director
of the diplomatic chancellery of Grand Duke Constantine at Warsaw, father of
the Russian ambassador Arthur von Mohrenheim (English Wikipedia, "Arthur von
Mohrenheim"; the dates also in a genealogy listing). Not checked against a
printed reference work.

Other signatures read on the scans:

- 0012 and 0014: "R. Fuhrmann", in an oval flourish. Roman Fuhrman is named
  in Polish literature as the director presiding in the Government
  Commission of Revenue and Treasury from 1833; the letters show him
  directing the finance commission in December 1831. The correspondents'
  list gives him as "R. Fuhrmann"; he has no entry among the people, since
  his name is not in the text.
- 0013: "(signé) Engel", a copy: Fyodor Engel, president of the Provisional
  Government of the Kingdom of Poland, September 1831 to March 1832.
- 0008, 0010: "sig. X. X. Lubecki" (Prince Ksawery Drucki-Lubecki, minister
  of finance), copies.
- 0007 (29 September 1830): a short signature under a heavy stroke, **not
  read**. The writer speaks of the "Prince Ministre des finances" as another
  person, so he is not Lubecki. The sender is left empty.

The addressee, "Schmidt", is Julius Schmidt, Prussian consul general at
Warsaw from 1817 to 1832 (the Geheimes Staatsarchiv's introduction to I. HA
Rep. 81 Warschau nach 1807).

## The documents

| No. | Pages | What it is |
|---|---|---|
| front | 0001 | The file's cover |
| 1 | 0002 | Mohrenheim to Schmidt, Warsaw, 26 Jan / 7 Feb 1828, French |
| 2 | 0003 | Mohrenheim to Schmidt, a private note, undated, French |
| 3 | 0004 | Mohrenheim to Schmidt, a private note, "Mardi", undated, French |
| 4 | 0005-0006 | Mohrenheim to Schmidt, Warsaw, 8/20 Feb 1830, French |
| 5 | 0007 | Unread signer to Schmidt, Warsaw, 29 Sept 1830, French |
| 6 | 0008 | Copy: Lubecki to Weigel, Warsaw, 22 Sept 1830, Polish |
| 7 | 0009 left, top of 0009 right | Copy: Weigel to Lubecki, Breslau, 14 Oct 1830, German |
| 8 | foot of 0009 right, 0010 | Copy: Lubecki to Weigel, Warsaw, 27 Nov 1830, Polish |
| 9 | 0011-0012 | Fuhrmann to Schmidt, Warsaw, 2/14 Dec 1831, French |
| 10 | 0013 | Copy: Engel to Schmidt, Warsaw, 1/13 March 1832, French |
| 11 | 0014 | Fuhrmann to Schmidt, Warsaw, 8/20 March 1832, French |

One document per letter, as in Nr. 12765 and Nr. 12366.

## Rulings and correspondents (2026-10-04)

Dates are each document's own dateline (`dates.read`), the western date
where both calendars are given. The two notes (2, 3) are `no_date`:

- Document 2 reports what the letter of 20 February 1830 says the
  Administrative Council laid before the Grand Duke "au mois d'Août
  dernier", so it is probably of 1829, before August.
- Document 3 is dated "Mardi". If the "Dubois" he returns is the "Mémoires
  du cardinal Dubois" published at Paris in 1829, it is of 1829 or later;
  that is a guess and is not used.

Senders and recipients are in `correspondents.json`, each with its reason,
and in `reference/correspondents.yml`. Document 7 answers 6 and document 8
answers 7 (`relations`). The "deux pièces ci-annexées" of document 5 are not
identified; documents 6 to 8 look like copies Weigel himself supplied
("Abschrift meiner Antwort"), not those enclosures.

## Corrections (2026-10-04)

62 passages and two added lines, each read on the scan of its page:
`intake/corrections.py`, logged in `transcription_decisions.csv`. What was
left is in `intake/unresolved.md`.

- The two notes: "voilà sur quoi on délibérera" (for "vérele [?] les quoi");
  "voici votre Dubois" (for "Devoir"); "pousser l'affaire Weigel & soyez
  tranquille sur le reste" (for "couver ... le Soyez tranquille. Sur le
  reste"); "un tems affreux" (for "mes tiens affaires").
- The Polish: "Mu strat" (for "Mastrat"), "podług praw u nas" (for "pod _ag
  praw a nas"), "przez Niego taxy sądowey" (for "Niegotascy"), "taxa takowa",
  "ocenioną bydź winna", "do układu warunków", "ocenienie", "użytku". The
  scribe's dotted z in "wierżytelności" and "towarżyszyła" is on the scan
  and stays.
- The German: "Schfl." (for "Schiff."), "Hälfte", "abgezogen" (for
  "abgegeben"), "zu seyn pp." (for "he[g?]u").
- The French letters: typing slips, and in the letters signed Fuhrmann three
  final flourishes that had been read as s ("affaires", "circonstances",
  "j'ais"); "h[um]ble ... ob[éissan]t" for "honorable ... obiesant"; the date
  "8/20 mars 1832" for "8/21".
- The editor's own additions in round brackets ("(Schmidt)", "(Monsieur
  Schmidt,)") are set in square brackets, as they wrote it on 0007.

## Summaries (2026-10-04)

German summaries were written in the session from a reading of each document
against its scan, and the English translated from them
(`intake/summaries_draft.py`). **They have not had the claim check**, and
there is no `reading.json`. `site/_data/summaries.yml` and `summaries_de.yml`
were not rebuilt from the local cache, which rewrote other holdings' lines:
the committed files were restored and the eleven new entries inserted.

Worth knowing from the reading:
- Weigel's demand in 1830: 30,000 thalers capital, 31,800 interest, 1300
  costs, 63,100 in all.
- His reckoning rests on the mortgage certificate of 14 August 1803 (value
  160,000 Reichstaler) and the court valuation of 6 May 1803 (128,917
  Reichstaler 17 groschen). Ahead of him stood church capitals of 7,000
  florins, 5,000 for Przepolewski and 42,000 for Lichnowski. His entry is
  "Rubr. III Nro. 3. pro v. Grottowski modo für mich".
- The estate is listed as Trąbczyn, Osiny, Łazy, Nowawieś, Zarobna and the
  Trąbczyn Hauländer.
- Lubecki holds that the last judgment in Weigel's case was given in 1826
  and that the claim must be valued by land prices of the present day.
- The claimants are called "Weigel & Eisenhardt" in 1829 and 1830 and "la
  maison de commerce Weigel" in 1832.
- "la Convention du 17/29 Mai 1830" between Russia and Prussia, which
  Lubowidzki was to carry out, is named but not explained.

## Authorities (2026-10-04)

People added: Mohrenheim, Schmidt (the consul; held to this holding's
documents, since other Schmidts stand in Oe 1 Bü 9454), Lubecki, Engel (held
to document 10), Lubowidzki, Drake, Eisenhardt. "Eisenhardt" was a matched
variant of the Berlin agent Eysenhardt of 1798 to 1808; it occurs nowhere
but here and now has its own entry, the banker not being shown to be the
same man. Grand Duke Constantine now matches "Césarévitch". Not added:
Przepolewski (a creditor named once), and the villages Łazy, Nowawieś and
Zarobna, for want of a firm identification.

## The site (2026-10-04)

`about.md` and `process.md` in both languages; three timeline entries
(February and September 1830, March 1832) and the timeline's range extended
to 1832; a paragraph in section VIII of the era essay, whose heading now
runs to 1832, in both languages; biographies for the new people and a
sentence added to Weigel's. The era is `hohenlohe` for now, as for Nr.
12366.

## "Mardi" put back with document 3 (2026-10-05)

The corpus had the `[DOC 4]` marker above "Mardi.", the last line of
Mohrenheim's note on scan 0004 (and of `transcriptions/0004_a.txt`), so
document 4 began with a page that had no scan (a "gap" row in
`page_scan_map.csv`) and document 3 lost its day. The marker now follows
"Mardi.". The scan map was corrected by hand, since `match_scans.py` needs
the raw scans: document 3 is lines 19-21, document 4 has two pages, 0005
and 0006. The two web images were renamed to match (`0005_a-L4_01.jpg`,
`0006_a-L4_02.jpg`, and `scan_rename_map.json`); on the editor's machine
`relabel_scans.py --unit iiihamdaiiinr12367 --apply` renames the originals
in `pages/` to the same labels.

## Translation (2026-10-05)

Translated in session, as Nr. 12366 was, not by the paid run (no pilot: French
and Polish were tried on Nr. 12366). The pages are in
`intake/translation/doc<N>.yml`; `intake/translation/write_cache.py` writes
them into the untagged cache for check_translations.py and
publish_translations.py. Status `translated`, `published_tag: ""`.

- **check_translations.py**: one row, document 7: "7,000 fl." is rendered
  "7,000 Polish florins", not the termbase's gulden. The church capital on a
  Polish estate is reckoned at six to the thaler (7,000 = Rthl 1,166 16 gr),
  so the florin is the Polish złoty, not the Austrian gulden. Deliberate; it
  is noted in the cache record.
- **uncanonical_names.py**: nothing. Breslau is Wrocław in the English, by
  the house rule; Eisenhardt stays (not Eysenhardt, see the people register).
- **Doubt kept:** "négrêtes [?]" in document 3 as "[uncertain: négrêtes]",
  the sentence recorded as not construing; "noter" in document 10 translated
  as it stands ("striving to note"), flagged ("hâter" is likely).
- **Forms of address:** WWPan in Lubecki's letters is "Your Honour";
  "Monsieur le Conseiller" "Councillor", "Monsieur le Consul" "Consul".
- **Weigel's reckoning** keeps its order of figure and unit ("Rthl 160,000"),
  its ditto marks as "ditto", and the Rubrik of the mortgage register as
  "Section".

## Claim check (2026-10-05)

`intake/claim_check.yml`: 77 statements, 76 supported, 1 overstated. The
German summary of document 6 said Lubecki "hat ... feststellen lassen" (had
the estates valued on the spot); he says he had to order it, and document 8
is still waiting for the valuation. Now "hat er angeordnet, ...
festzustellen", in `summaries_de.yml`, `site/_data/summaries_de.yml` and
`about_de.md` ("ordnete an, ... zu schätzen"). The English already said
"ordered". The statement that document 3 is dated Tuesday rests on the
corpus correction above.

## Still to do

- The editor's ruling on the era, with Nr. 12366's.
- Reading the English against the scans, as for every holding.
- The German translation columns beside the Polish letters: transcribe or
  leave out, the editor to say.
- The words in `intake/unresolved.md`, and the signature on 0007.
- The edition guide's counts of holdings and documents are written by hand
  and stale; not touched.
