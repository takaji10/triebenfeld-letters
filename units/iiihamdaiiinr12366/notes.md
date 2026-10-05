# III. HA MdA, III. Nr. 12366 (GStA PK)

Six documents on 37 pages, plus the cover as front matter, 1818-1827: the
Prussian foreign ministry's file on Michalina Miączyńska's claim to have the
Trąbczyn estates freed of the Prince of Hohenlohe's debts, and on the Polish
judgments against his creditors. Added on 2026-10-04: scans cut at the
editor's folds, the text cut to pages, corrected, summarised, and given its
place on the site; translated and its summaries claim-checked in session the
same day.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, III. HA Ministerium der
auswärtigen Angelegenheiten, III Nr. 12366 (older marks on the cover: AA. III
Rep. 8 Nr. 4543; Zentrales Staatsarchiv 2.4.1. Abt. III Nr. 12366). The cover
calls it "Vol. I, vom 15. Dez. 1818 bis Novbr 1827, conf. Vol. II". The scan
folder is named "Klage der Gräfin Michalina von Miaczynska ... 1834-1836";
nothing in these 25 scans is later than 1827, so that title may belong to the
second volume. The editor: ignore the folder name, it is not relied on
(2026-10-04).

25 scans. Single leaves: 0001 (cover), 0002, 0003, 0009-0013, 0017, 0025.
Openings, written on both sides: 0004-0008, 0014-0016, 0018-0024.

- **Pages.** Each side of an opening is a page: `_a1` the left, `_a2` the
  right. The editor asked for every opening to be split and places the folds
  (`review_folds.py`, `processed/_spreads_review/review.html`).
- **0004 and 0005 are one opening photographed twice.** A slip bound into the
  gutter hides the right page's margin on 0004 and the left page's edge on
  0005. The left page is 0004_a1, the right 0005_a2 (editor, 2026-10-04).
  0004_a2 and 0005_a1 go to `processed/_blank_halves/` after the cut.
- The ruler and dark border are left on the images.

## Transcription

The editor's single Markdown file stays in `<raw_dir>`. It is by paragraph and
marks the scans each piece covers in square brackets. `intake/build_pages.py`
cut it into `transcriptions/<page id>.txt` and wrote the document boundaries
(`intake/document_boundaries.csv`, copied to `review/<slug>/`). It checks that
the pages add up to the source text.

- **Where the text is cut** was read off each scan (the first words of every
  page are listed in the script). A cut inside a paragraph leaves it as the
  last line of one page and the first of the next. One cut falls inside a word
  as transcribed: "spodobniemogą" is "spodob" at the foot of 0021 right and
  "niemogą." at the head of 0022 left.
- **Three lines were moved** from the head of a document to the page where the
  scribe wrote them: "Varsovie le 29 avril 1818" to the foot of 0009; in the
  note to Nesselrode the dateline and the address "A S. E. Mr. le Comte de
  (Karl) Nesselrode" to 0016 right, the date above the signature and the
  address below it. On single-page documents (0002, 0012) the editor's order
  stands, though there too the date is written at the foot.
- **Markdown taken off:** escapes, bold and italic. The editor's `*` after a
  word is rendered `[?]` (18 words), on the reading that it marks a doubtful
  word. Open: confirm with the editor.
- **Added by the editor (2026-10-04):** the cover's line "Vol. 1 vom 15. Dez. 1818
  bis Novbr. 1827.", which the Markdown file does not have. It was added to
  `transcriptions/0001_a.txt` and corpus.txt by hand, so `build_pages.py
  --write` must not be run again. The scan has a "15." written in above
  "Dez."; the editor had it added.
- **By paragraph** (rulings.yml `pages: by_paragraph:`): every page but the
  cover.
- Not transcribed: the received marks and journal numbers on 0002 and 0010,
  the registry notes in the left margin of 0010 and 0011, catchwords, and the
  signature "Sierszewski" at the foot of 0025.

## The documents

| No. | Pages | What it is |
|---|---|---|
| front | 0001 | The file's cover |
| 1 | 0002 | Alopeus to Bernstorff, Berlin, 20 Jan 1819, French |
| 2 | 0003-0009 | Copy: report on Miączyńska's claim, Warsaw, 29 April 1818, French (enclosed in 1) |
| 3 | 0010-0011 | Draft reply to Alopeus, Berlin, 11 May 1819, French |
| 4 | 0012 | Copy: Tarczewski to a creditor, Warsaw, 16 Nov 1819, French |
| 5 | 0013-0016 | Copy: Schöler to Nesselrode, St Petersburg, 10 Feb / 29 Jan 1827, French |
| 6 | 0017-0025 | Certified extract: judgment of the Kalisz civil tribunal, 30 July 1827, Polish |

One document per letter, as in III. HA MdA, III Nr. 12765.

## Rulings and correspondents (2026-10-04)

Dates are each document's own dateline (`dates.read`); the note from St
Petersburg is dated in both calendars and takes the western date. Senders and
recipients are in `correspondents.json`, each with its reason. The Warsaw
report is unsigned: Alopeus's note calls it the report of the Lieutenant of
the Kingdom of Poland, so it is given to Zajączek, whom the text does not
name. Tarczewski's client is not named; the suit then pending was Weigel's.
Document 3 was marked rough until it was corrected (below).

## Corrections (2026-10-04)

72 words, each read on the scan of its page: `intake/rulings_corrections.py`
and `transcription_decisions.csv`. They are typing slips in the French of
documents 1, 2, 4 and 5, which are in clean copy hands (Mnosieur, acif,
Varovie, désai, succomber, indeminser, hypothécaise, étrance, one exiédé),
the name Wichnowski for the scan's Wichrowski, and the editor's doubt mark
dropped on eleven words the page gives plainly. Three stand twice in their
paragraph and were edited directly (indemniser twice, "aussitôt que
possible"); five more that the applying tool refused were made by hand and
are in the log. The writers' own spelling was kept. Documents 3 and 6 were
corrected afterwards (next section).

## The Polish judgment and the draft corrected (2026-10-04)

At the editor's word every page of documents 3 and 6 was read against its
scan: `intake/polish_corrections.py`, which gives each change with what it
means, applies it and logs it in `transcription_decisions.csv`. 64 passages in
the Polish, 21 in the draft; many change more than one word. A change was made
only where the scan is plain and the result is a word of the language that
fits the sentence.

- In the Polish hand k looks like "li" and R like "K": hence "litore" for
  ktore, "politadanych" for pokładanych, "kządu" for Rządu.
- Changes that alter the sense: "Obecni" (present) over the list of judges;
  "przy Ulicy Jozefinie odbywaiącego" (the court sits in Józefina street; the
  transcription had it not sitting); "Xięciu Hohenlohe" (to Prince Hohenlohe,
  not "Zięciu", son-in-law); "warunkowego" (conditional possessor); "obcą"
  (a stranger's debts); "takowy ... zastosować się nie da" (the Treaty of
  Tilsit cannot be applied); "Swiadczę" (I certify).
- The two sums at the end are lettered a and b, as on the scan.
- The draft was read on enlarged crops; its writer's "les" looks like "ly".
  It is no longer marked rough.
- What was left is in `intake/unresolved.md`.
- **The editor's spot sheet (2026-10-04)**, thirteen words
  (`intake/open_queries.py`; answers in `review/<slug>/query_answers.json`).
  Changed on their reading: "Kr. Kosten" and "weil" in the pencil notes,
  "Lama[?]" (they read Lama and say it could be Larna), "Jozef Zapolski",
  "nieobciętym", "Karnecki". Confirmed as they stood: "denn", "Decrete.",
  "Lublinca", "ustalić". They could not tell "Assistant", "Rozdayczer[?]" and
  "Likrę[?]", which stand.

## The margin notes on document 2 (2026-10-04)

A reader in the ministry pencilled objections in German beside passages he
underlined in the Warsaw report. The editor supplied a first reading and the
passage each note stands beside; each was read again on an enlarged crop
(`intake/margin_notes.py`, which holds the text). Thirteen notes on seven
pages (0003 to 0007), one line each at the foot of the page, or before the
last paragraph where the page ends in mid-sentence; listed in
`office_notes.yml` and shown as written by the receiving office. The French
in square brackets before a note is the passage, quoted by the edition.

Changed from the editor's reading: "irgend jemand verantwortlich wäre" (for
"i[n?] zend[?] jemand ... war"); "Venedig"; "denn seit 1807"; "Anspruch wegen
des in der Zwischenzeit geschehenen, zugestanden"; "Kr. Kosten Rbz. Posen"
(for "2. Kosten debg. Posen"; "Kr." is the editor's on the spot sheet); "wo steht das geschrieben? Nicht einmal im
Napoleon. Decrete."; "unwahr" (for "einwahr"); "aber so lang er es besessen,
besaß er es rechtmäßig u. mit vollem Eigenthumsrecht"; "wo steht das
geschrieben?"; "sie bekamen zurück, was da war."; "weil hier Schulden da
sind." The last two stand on the right page of 0007, not the left.

What they say, in English: as if Prussia were answerable to anyone for acts
of government in the former South Prussia; so now he was ill too, she only
fell ill at Venice; October 1803 (the father's death); untrue (that she had no
guardian); why then has she kept silent since 1807, when she was put back in
possession; not even Napoleon granted them a claim for what was done in the
years between; (Manieczki is in) the district of Kosten, government district
of Posen; where is that written, not even in Napoleon's decree; untrue (that
the confiscation was against all justice); but for as long as he possessed it
he possessed it lawfully and with full right of ownership; where is that
written (that the estates were unjustly confiscated); they got back what was
there; because here there are debts.

With the notes in, three more changes to the report's text: the note "1803
Oct." taken out of the running text, where the transcription had it in
brackets; "ne" added in "et qui ne pouvaient être autres que celles de santé"
(0008 right, read on the scan, at the editor's word); "de sa santé" corrected
to "de la santé" (0004 left, read on the scan).

## Summaries (2026-10-04)

German summaries were written in the session from a reading of each document
against its scan, and the English translated from them
(`intake/summaries_draft.py`). They were claim-checked in session, not by the
paid run (below, "Claim check"), and there is no `reading.json`. `site/_data/summaries_de.yml` was not rebuilt from
the local cache, which would have undone corrections made in the cloud: the
six new lines were inserted into the committed file.

Worth knowing from the reading:
- The report of 1818 counts 156,000 écus of Hohenlohe-Ingelfingen's debts on
  Trąbczyn and Szetlewek, and 160,000 on Kolno and Kamionna, sold to Leixner
  for 142,000.
- It gives Prusimski's death as after his wife's, at Venice; the editor's
  bracketed "1803 Oct." is a pencil note in the margin. The ministry's draft
  also says he died in 1803.
- Weigel lost in all three instances but the second: Kalisz 6 March 1819,
  the court of appeal for him, the high tribunal at Warsaw against him on 17
  July 1826. Prussia's notes of 1819 and 1820 went unanswered.
- The judgment of 30 July 1827 strikes out the Lichnowski brothers' 42,000
  thalers (252,000 Polish florins) and the widow Grotowska's 20,000 (120,000
  florins). The figures are written out in Polish words, so the summaries and
  the description give no numerals for them.
- The cover's dockets name earlier journal dates (13 January 1819, 29 January
  1820, 3 February 1826, 11 January 1827): pieces of those dates are not all
  in this volume.

## Authorities (2026-10-04)

People added: Bernstorff, Tarczewski, Wybicki, Niemojewski, Wichrowski,
Rembowski, and an entry for Grotowski (matched until now from the vetted
list; the new pattern also takes Grottowsky and the Polish case forms).
Leixner now matches "Leyner" and Zastrow "Zastrof", the spellings of the
French report. Places: Warsaw now matches "Varsovie" (also in Nr. 12765) and
Kamionna "Kamienno". Not added, for want of a firm identification: Pawłowo,
Dzwonowo and "Berenkusz" (Sanitz's estates), Manieczki, Beskyn, Hetzendorff,
Larna. The two glossary candidates the probe offered ("cette",
"ingelfingen") are ruled out under `excluded:`.

## The site (2026-10-04)

`about.md` and `process.md` in both languages; three timeline entries (1819,
February and July 1827) and the timeline's range extended to 1827; a
paragraph in section VIII of the era essay, whose heading now runs to 1827,
in both languages; biographies for the new people and additions to those of
Weigel, the Lichnowski brothers, Grotowski, Schöler, Alopeus and Nesselrode.
The era is `hohenlohe` for now: the plan leaves it to the editor whether this
file belongs there or in the restitution era.

## Translation (2026-10-04)

Translated in session, as Nr. 3709 was, not by the paid run: under the rules
translate.py gives its translator (its system prompt, termbase and canonical
names, generated for this unit), written to the untagged cache
(cache/translation-raw/) with translate.py's own `save()`, so each record
carries the `source_hash` of the text translated. cache/ is not in the
repository: the pages are kept in `intake/translation/doc<N>.yml`, and
`intake/translation/write_cache.py` writes them into the cache again for
check_translations.py and publish_translations.py. If the editor wants the
model's own translation for comparison, `translate.py --unit iiihamdaiiinr12366
--all` overwrites the cache.

- **Pilot first** (`translation_pilot: [1, 6]` in unit.yml): Alopeus's French
  letter and the Polish judgment, French and Polish being new here. Both
  passed check_translations.py with no row; nothing in the termbase needed
  changing, so the other four followed on the same rules.
- **check_translations.py**: 2 rows, neither a fault. On page 6 of document 2
  the termbase patterns for *Transact* and *Rendant* match the French
  "transactions" and "rendant" (giving back); no termbase word is there.
- **uncanonical_names.py**: nothing. Names are in the edition's forms where
  the termbase's table settles them (Trąbczyn for Trąpczyn, Warsaw, Poznań,
  Wrocław, Międzyrzecz, St Petersburg), and otherwise as the page spells them:
  Leyner, Zastrof, Wichrowsky, Grottowsky, Kamienno, Szetlowek, Szeltowek,
  Micheline, Frédéric Guillaume II and the Polish Fryderyk Wilhelm and
  Fryderyk Ludwik. Szetlowek, Szeltowek and Szetlowka are now matched to
  Szetlewek in reference/places.yml (not made variants), as Kamienno is to
  Kamionna. écus are written Reichsthaler (english_forms.yml); the Polish
  "Talarow" thalers, "złotych polskich" Polish florins, the sums written out
  in words as the judgment writes them.
- **Rendered on purpose:** the words the transcription doubles in the judgment
  ("przy własnosci przy własnosci", page 10; "nie ma bydz nie ma bydz", page
  12) are doubled in the English too. The sentence that runs from page 9 to
  page 10 keeps its last word, "niemogą", on page 10 ("are not able").
  "ne saurait pas être appreciée" (document 2, page 9) is rendered as it
  stands, "could not be appreciated", though the argument wants "could not
  fail to be"; it is flagged in the cache record. The pencil notes are
  translated under "[Written by the receiving office:]", each after the
  English of the passage it stands beside, in square brackets.
- The holding is `status: translated`, `published_tag: ""` (untagged).

## Claim check (2026-10-04)

Each German summary held to its document under the rules read_letters.py
--verify gives its checker: 70 statements, 69 supported, 1 overstated, in
`intake/claim_check.yml` with the passage each rests on. The overstated one:
the summary of document 2 gave the pencil note "aber so lang er es besessen,
besaß er es rechtmäßig ..." to the Prince, but the note says only "he" and
"it", beside a sentence on the gifts to the Prince and to Sanitz alike. It now
reads "der Beschenkte habe das Gut, solange er es besaß, ...", in the German
and English summaries and on the holding's page (about.md, about_de.md). The
statement that document 4 is a copy rests on the scan's hand, not the text.

## Still to do

- The editor's ruling on the era.
- The words in `intake/unresolved.md` stand as written. On the three words
  of the Polish judgment ("Assistant", "Rozdayczer[?]", "Likrę[?]") the
  editor has no further reading (2026-10-05); the question is closed.
- Reading the English against the scans, as for every holding.
- The edition guide's counts of holdings and documents are written by hand
  and were stale before this holding; not touched.
