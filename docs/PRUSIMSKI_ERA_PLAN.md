# The Prusimski era: plan

Written 2026-10-06 at the editor's request ("Before you start anything, make a
plan for everything in this prompt"). Nothing in it has been started. It
covers: finishing APP 53/17/0/-/Konin Gr.145; bringing in the other court
books from the State Archive in Poznań; the spelling question; the glossary;
and what the rest of the site owes these holdings.

All of this is desktop work: the scans and the editor's text files are on the
editor's machine (`J:\Documents\Archive\Genealogy\References\Poznań State
Archives`), not in the repository. A cloud session can write summaries, prose
and authorities once a holding is built, but cannot build one.

## What the editor has decided (2026-10-06)

- **Konin Gr.145: check the whole text for dropped phrases.** At the end,
  list each one found and say whether it matters to the meaning. The English
  may be updated with whatever was dropped.
- **Konin Gr.145 is one document.** The editor's section headings were added
  to make a very long text followable; something like them stays in the
  English.
- **The fonds** of the Konin books is "Księgi sądu i urzędu grodzkiego w
  Koninie" (books of the castle court and castle office of Konin). The
  archive's note on it, as the editor pasted it: the castle court took shape
  at the end of the fourteenth century and at first judged nobles in the
  four "castle articles" (arson, an attack on a nobleman's house, robbery on
  the public road, rape); later also other criminal cases and suits over
  land and sums of money, and appeals from town courts. Beside the court
  grew the castle office, where the court books were kept. The office was
  open every day for entries in matters not in dispute, and the books had
  "public faith".
- **No account of the Prusimski era yet.** Many documents are still to come.
- **No work on the glossary yet.** It is already long. Think about how to
  keep it useful (below).
- **The other Prusimski-era folders are to be added.** Their texts have
  largely been corrected; a lighter touch is better. The English translations
  exist and are not matched line by line, and need not be. No paid runs.
- **Splits and crops are approved by the editor** before any page is used.
- **Folders without texts are flagged**; the editor will supply the texts.

## 1. Finishing Konin Gr.145

1. **Dropped phrases.** Read the 117 pages not yet compared, each cut into
   three enlarged strips, against the Polish, looking for words on the scan
   that are missing from the text (and noting any other slip that changes
   the sense). About ten sittings of twelve pages. Each find goes into
   `intake/corrections.py` in a second block, is logged, and the English
   gets the missing words through `FIXES` in
   `intake/translation/build_doc1.py`.
2. **The report the editor asked for:** a table at the end, one row per
   dropped phrase: the leaf, the words restored, their English, and a
   verdict in three grades: changes what the court found or ordered; adds a
   fact (a place, a person, a measure); formula only. Put in the holding's
   `notes.md` and given to the editor in the reply.
3. **The fonds and its background** go into `unit.yml` (`archive_title`,
   description), `about.md` and `about_de.md` ("Historical background"), and
   `notes.md`. The same paragraph serves every Konin castle-court book below.
4. **Headings in the English** stay as they are: the editor's, in square
   brackets.
5. Then `process.md` loses its sentence that 117 pages were not compared and
   says what the full check found. Publish at the editor's word.

## 2. The folders

Twenty-nine folders are left after the editor's list of folders to ignore
and Konin Gr.145. Twenty have a transcription and an English translation;
nine have none.

### With texts (to be added)

| Unit | Archive's title | Scans | Words (original / English) | Notes |
|---|---|---|---|---|
| 53/6/0/-/17 | Inscriptiones, relationes, decreta [inducta] 1589 | 3 openings | 714 / 2,230 | Latin. Register no. 1 |
| 53/6/0/-/36 | Decreta [inducta] 1641-1644 | 1 opening | 317 / 1,784 | Latin. Register no. 2 |
| 53/6/0/-/40 | Decreta [inducta] 1722-1780 | 4 pages, 1 opening | 962 / 3,467 | Latin. Register no. 3 |
| 53/6/0/-/45 | Decreta [protocollon] 1750-1765 (Konin) | 1 opening | 281 / 1,074 | Latin. Register no. 5 |
| 53/6/0/-/46 | Decreta [protocollon] 1773-1777 | 2 openings | 589 / 1,394 | Latin |
| 53/6/0/-/47 | Decreta [protocollon] 1781-1791 | 3 openings | 621 / 1,642 | Latin |
| 53/15/0/-/Kalisz Gr.414 | Relationes [protocollon] 1771 | 2 openings | 577 / 2,688 | Latin and Polish. Register no. 9 |
| 53/15/0/-/Kalisz Gr.424 | Relationes [protocollon] 1776 | 1 opening | 174 / 275 | Latin |
| 53/15/0/-/Kalisz Gr.425 | Relationes [protocollon] 1776 | 3 openings | 331 / 510 | Latin |
| 53/17/0/-/Konin Gr.114 | Relationes [protocollon] 1765-1767 | 2 pages, 12 openings | 554 / 1,560 | Two pairs of text files (one for leaves 334-334v) and an `info.txt` |
| 53/17/0/-/Konin Gr.115 | Relationes [protocollon] 1768-1774 | 16 openings | 1,237 / 1,694 | A subfolder "Incorrect Pages" with 11 more images |
| 53/17/0/-/Konin Gr.116 | Relationes [protocollon] 1775-1777 | 9 openings | 753 / 1,243 | |
| 53/17/0/-/Konin Gr.117 | Relationes [protocollon] 1778-1779 | 15 openings | 4,269 / 6,602 | |
| 53/17/0/-/Konin Gr.118 | Relationes [protocollon] 1780-1782 | 32 openings | 4,715 / 7,341 | The English has a stray line from a chat ("Claude responded: [523]") |
| 53/17/0/-/Konin Gr.119 | Relationes [protocollon] 1783-1784 | 14 openings | 1,444 / 2,191 | |
| 53/17/0/-/Konin Gr.120 | Relationes [protocollon] 1785-1786 | 2 openings | 386 / 615 | |
| 53/17/0/-/Konin Gr.121 | Relationes [protocollon] 1787-1788 | 2 openings | 310 / 497 | |
| 53/17/0/-/Konin Gr.136 | Relationes-oblatae [protocollon] 1754 | 1 page, 2 openings | 1,041 / 4,757 | Polish and Latin. Register no. 4 |
| 53/17/0/-/Konin Gr.153 | Relationes-oblatae [protocollon] 1782 | 1 page, 13 openings | 4,965 / 10,682 | Latin. Register no. 13. `info.txt` |
| 53/21/0/-/Pyzdry Gr.75 | Relationes [protocollon] 1768-1771 | 2 pages | 351 / 914 | Latin. See the question on Pyzdry Gr.75 below |

About 144 scans and 24,600 words of original text; the English is about
twice as long because it carries the editor's outlines, notes and
glossaries.

### Without texts (flagged for the editor)

| Folder | What is there |
|---|---|
| Inscriptiones [protocollon] 1724-1735 (53.17.0.-.Konin Gr.79) | 17 camera raw files (.cr2), no text |
| Inscriptiones [protocollon] 1736-1746 (53.17.0.-.Konin Gr.80) | 2 camera raw files, no text |
| Inscriptiones [protocollon] 1746-1756 (53.17.0.-.Konin Gr.81) | 3 camera raw files, no text |
| Inscriptiones [protocollon] 1768-1781 (53.21.0.-.Pyzdry Gr.75) | 2 scans, no text |
| Relationes [protocollon] 1786 (53.20.0.-.Poznań Gr.1181) | 14 scans, no text |
| Relationes [protocollon] 1791-1792 (53.21.0.-.Pyzdry Gr.115 | 1 scan, no text |
| Relationes-oblatae [protocollon] 1770-1773 (53.17.0.-.Konin Gr.142) | 4 scans, no text |
| Relationes-oblatae [protocollon] 1781 (53.17.0.-.Konin Gr.150) | 1 scan, no text |
| Relationes [protocollon] 1727-1728, 1750 (43.4.0.-.76) (Kalisz) (Unrelated) | 2 scans, no text; the folder's own name says "Unrelated", and its number begins 43, not 53 |

The three folders of camera raw files will need the images converted to JPEG
before anything else; the project's tools do not read .cr2.

### Questions about the folders

1. **Pyzdry Gr.75 appears twice**, as "Relationes [protocollon] 1768-1771"
   (with texts) and as "Inscriptiones [protocollon] 1768-1781" (without).
   One signature cannot be two volumes. Which title is right for each?
2. **"(43.4.0.-.76) (Kalisz) (Unrelated)":** leave it out?
3. **Konin Gr.115, "Incorrect Pages":** ignore those eleven images?
4. **Konin Gr.114** has two sets of texts. Taken as two entries of the one
   volume unless the editor says otherwise.

## 3. How each holding is added

One holding per archive unit (per folder), as now. The steps, in order:

1. **Inventory.** Read the two text files and list the entries: leaf, the
   entry's own heading, its date, its language. Match each to the scan it
   is on. The editor's `Chronological_Document_Register.md` and
   `Cross_Reference_Map.md` (in the Poznań folder; copies go into
   `reference/sources/`) give the date, court, parties and cross-references
   of sixteen of the matters; each is checked against the text before use.
2. **Pages, for the editor's approval.** Nearly every scan is an opening.
   Each is cut at the fold into two whole pages, as for Konin Gr.145. A page
   is kept if it carries any of the transcribed text and left out if it
   carries none. **No page is cropped to an entry**: the whole page stays, so
   that no line can be cut off, and the reader sees the entry where it sits
   among its neighbours. Before anything is staged, the editor gets one
   sheet per holding showing every scan with the proposed fold drawn on it
   and each half marked "kept" or "left out", and approves or moves them
   (the existing fold review, `review_folds.py`). Nothing is cut until then.
3. **Documents.** See "One document or many" below.
4. **Text.** The transcription is cut to the pages by a script in the
   holding's `intake/`, which checks nothing is lost. Markdown is taken off.
   The editor's apparatus (outlines, translator's notes, glossaries,
   summaries) is kept out of the text and used for the holding's page.
5. **A light check**, the same for every holding: every entry's heading,
   names, dates and sums are read against the scan; one page in five is
   read word for word, and for a holding of one or two pages all of it. The
   holding's page says how many pages were compared. Accents that are plain
   slips are put right as in Konin Gr.145. Nothing is re-spelled.
6. **English.** The editor's translation is cut to the documents (not to
   pages or lines; it "doesn't need to be" matched). Their headings stay, in
   square brackets; their notes follow the paragraph they belong to. Where a
   long document has no headings, short ones are added in the same form.
   Stray lines from the drafting ("Claude responded") are removed. The
   automatic check runs; rows that are the editor's deliberate renderings
   are recorded, not changed.
7. **Summaries**, in session, no paid run: one per document, written in
   German and English from the text, with the editor's outline or register
   entry as a guide, then each statement checked against the document
   (`intake/claim_check.yml`). A one-line register note gets a one-sentence
   summary.
8. **Authorities**: people, places, estates in focus, relations (next
   section).
9. **Holding page** in English and German, in the form already used.
10. **Build, verify, commit locally; publish at the editor's word.**

### One document or many

A court book is not a file about one matter. The editor photographed the
leaves on which the dispute appears, and a volume's entries are years apart
and unrelated to their neighbours. So the package rule ("a court file is one
document") does not fit: each **entry** of a court book is a document, with
its own date, heading and parties. That matches the editor's register, which
lists matters, not volumes.

To keep it from becoming too fine-grained: where a page carries a run of
one-line register notes of the same sitting ("Videatur hoc loco ...", see
here), the run is one document, not one per line. A long entry with
embedded older decrees (Konin Gr.153, Konin Gr.145) is one document.

By this rule the twenty folders make very roughly 80 to 120 documents; the
count is fixed in the inventory step and shown to the editor before a
holding is built. **This is the main thing to confirm.**

### Order

Five batches, each built, shown and published before the next is started:

1. Konin Gr.145 finished (section 1).
2. The early land-court books, small and each one matter: 53/6/0/-/17
   (1589), -/36 (1641-44), -/40 (1728), -/45 (1750-65), and Konin Gr.136
   (1754). These also test the method on Latin.
3. The 1760s and 1771: Konin Gr.114, Pyzdry Gr.75, Kalisz Gr.414, Konin
   Gr.115.
4. Around the commission: Konin Gr.116, Kalisz Gr.424 and Gr.425, Decreta
   -/46, Konin Gr.117.
5. After it: Konin Gr.118, Konin Gr.153, Decreta -/47, Konin Gr.119, Gr.120,
   Gr.121.

## 4. Modern spelling beside the scribe's spelling

The editor's Polish is in modern spelling in many places, for ease of
reading, and asks whether a mix across the edition is acceptable.

**Recommendation: accept the mix, and label it.** Re-spelling 24,000 words
back to the scribes' forms would be a second transcription, for little gain:
the sense, the names and the dates are what these documents are read for.
The issues, and what answers each:

- **A reader who quotes the Polish must know it is not the scribe's
  spelling.** Each document says which it is: a field in `rulings.yml`
  (`spelling: modern`, `partly modern` or `as written`), shown on the
  document's page beside the existing "transcribed by paragraph" note, and
  said on the holding's page. The About page already states the exception
  and will state the rule.
- **The mix must not be silent inside one document.** Where a text is
  partly modernised it is labelled "partly modern", not tidied either way.
- **Search and the index** are helped by modern spelling. The patterns for
  people and places must match both forms (Trąpczyn and Trąbczyn already
  do); each new holding's index hits are read by eye, because patterns made
  for German match Polish words wrongly (seven did in Konin Gr.145).
- **Checking against the scans** then compares words, not letters. That is
  what a light check does anyway.
- **Latin** is unaffected: it is given as written with abbreviations
  filled out, and the square brackets show what was supplied.
- **Not to do:** convert in either direction, or correct a modernised form
  "back" on one page.

This becomes a standing rule in `docs/EDITORIAL_RULES.md` once confirmed.

## 5. People, places, estates, relations, and the other pages

- **People.** One entry per person, as now. This era brings several people
  of one surname (Krzysztof and Antoni Prusimski; Jerzy, Franciszek, Józef,
  Stanisław and Heliodor Chełmski; the Otto-Trąmpczyński brothers). The
  existing entries "Antoni Prusimski" and "Chełmski" match on the surname
  alone and would swallow them, so they are narrowed (`only_in`, forename
  patterns) as each holding comes in, and every hit is read. Court officers
  and witnesses are not indexed unless they recur across holdings.
- **Places and estates.** Most are in the authority already (Trąbczyn,
  Łukomia, Łukom, Drzewce, Osiny, Zagórów, Biskupice's neighbours). New
  ones (the Lusnia wood, the Trąbczyn Olędry, Tomice, Grab, Smoleniec and
  others from the cross-reference map) are added only where a holding names
  them. Each document gets its estates in focus in `rulings.yml`.
- **Relations.** The register's cross-references become `relations` between
  documents where the text itself refers to the other document (the decree
  of 1775 cites the delivery of possession of 1771, the inspection of 1592
  and the decree of 1760).
- **Timeline.** One entry per matter that the register lists, not per
  document, added with its holding.
- **The story page** says how many documents the era has; that sentence is
  updated with each batch. The era's own account waits, as the editor said.
- **The About page**: its few figures, and the sentence on spelling.
- **Sources page and holding pages** build themselves.
- **Kinds of document.** A small set is added for court books: decree,
  citation, protest (manifest), inspection, court-book note. Labels in
  English and German.

## 6. The glossary: thoughts, nothing to build yet

The editor's view: German, Polish or Latin words that do not appear in the
English texts should not appear in the English glossary, except words that
keep their original language.

**Agreed, and it points to a clearer model.** A glossary answers "what does
this word in front of me mean". So:

- **The English glossary is keyed on what stands in the English**: words
  kept in the original (stawisko, staj, grzywna, Starost) and English
  renderings that need explaining (boundary mound, sworn inquiry,
  sub-chamberlain, delivery of possession). The original word is given
  inside the entry, not as a headword. This is how the editor's own
  glossaries in these files are already written ("boundary line [dukt]").
- **The German glossary is keyed on the original words**, because the German
  site shows the original text.
- **One entry, two headwords**, so a definition is written once.
- **An entry earns its place by use**: it appears on a page only if its
  headword occurs in a published text of that language. The build can
  check this; today one entry already "is found nowhere".
- **To keep the page from growing without limit**: filter by era and by
  holding; on a document's page show "terms on this page"; and hold the
  editor's 89 terms and the later files' glossaries in `reference/sources/`
  until the model is settled, merging duplicates (the edition already has
  some of the same words) before any go in.

Open for the editor: whether an English rendering that is plain English
("corner mound") needs an entry at all, or only those a reader could not
guess.

## What is needed from the editor before work starts

1. **One document per court-book entry** (section 3), or another rule.
2. **Accept and label the mixed spelling** (section 4).
3. **Whole pages, cut at the fold, approved on a sheet per holding**
   (section 3, step 2), or cropping to the entry.
4. The four questions about the folders (section 2).
5. The order of the batches, and that each is published before the next.
