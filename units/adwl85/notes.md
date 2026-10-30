# ADWł 85

Two documents on nine pages from the volume of the visitation of the Konin
deanery of 1790 and 1791, Diocesan Archive in Włocławek, signature 85: the
parish of Trąbczyn (document 1, leaves 23v to 25v and 28v to 29v) and the
table of the souls of the parish of Zagórów (document 2, leaf 34a). Added
on 2026-10-15 at the editor's request: the editor's transcript read in,
the passages it left out of these pages transcribed in session at the
editor's word, every page read against the scans, translated and
summarised in session, the summaries claim-checked, with the holding's page.
The editor answered the spot sheet on 2026-10-16, said the reference has no
series name, and gave the word to publish: **published 2026-10-16**.

Everything about how the holding was made is in the docstrings of
`intake/holding.py` and `intake/text85.py`.

## Provenance

The editor's folder `Archiwum Diecezjalne we Włocławku/Wizytacja` has fifty
photographs of the volume, one page each, named by leaf
(`Wizytacja_0385_k_24.jpg`, `..._k_25_v.jpg`, `..._k_34a.jpg`; leaves 14v,
23v to 46), and their transcript `Akta wizytacji dekanatu konińskiego
1790-1791, sygn. 85.md`, copied as `intake/editor_transcript.md`. Only the
nine pages the transcript covers are in the edition (editor, 2026-10-15).
The archive and its signature are as the editor gave them; the archive is
new to the edition (`reference/repositories.yml`, `site/_data/rights.yml`,
no website of its own found, so no link).

Page ids: `0023_b` (leaf 23 verso), `0024_a`, `0024_b`, `0025_a`, `0025_b`,
`0028_b`, `0029_a`, `0029_b`, and `0034_c` for leaf 34a (34 recto and verso
being `_a` and `_b`). Single pages, nothing cut: `holding.py --crop` copies
them to `processed/`.

## Decisions (editor, 2026-10-15)

- **The gaps transcribed.** The transcript left out parts of the pages it
  covers; the editor chose to have them transcribed in session. Left out:
  the top of 23v (the end of the parish before Trąbczyn) and, on 34a, the
  description of the church of Zagórów under the table, which runs on to
  34a verso (as the option the editor chose said).
- **Two documents**: Trąbczyn, and the Zagórów table.

## The text

- By paragraph, as the editor's transcript was; the edition's text is
  `intake/text85.py`. The editor's expansions of abbreviations are not
  kept ("Jego Wysokość Magnifici" for JWo Mści was wrong); abbreviations
  stand as written (EDITORIAL_RULES).
- **The tables are lines of text** with cells parted by " | ", not the
  site's table view: `unitlib.table_of` needs a number in the first cell of
  every entry, and these tables have none; and the two Trąbczyn tables stand
  inside a page of prose. Figures without the scribe's stops.
- **Catchwords** stand on a line of their own. On leaf 29 the scribe wrote
  "te=" with "raz" below and began 29v with "teraz": `catchwords.yml` drops
  the "raz" so the reading text does not say "teraz" twice.
- A phrase dropped between two occurrences of "Miasta" (leaf 24, "na mil 5
  od Konina") is restored: the editor's text gave Kalisz the 2 miles of
  Konin. What changed for the editor is in `intake/changes.yml`.
- 12 marks of doubt, all on the spot sheet `readings.csv`
  (`intake/spot_sheet.py`), each with a picture. The editor answered
  (2026-10-16; `intake/spot_answers.py` says how each was taken): nine
  settled (obok, trumną, Bogusławskiego, Golinską, Dręzgi, Illust:,
  Gralewska, 58, rozrządzonę), three kept with doubt (Kozierog[?],
  Uła[?], podciorze[?]). Their note "Maybe Ułazwany" was taken as "Uła"
  and the separate word "zwany", called: in this hand ł is a t with a bar.

## The figures

- The Trąbczyn table of 1791 adds up in every column to the scribe's totals
  and to 760, the number in the text. The register extract of 1790 has no
  totals.
- The Zagórów table: the women's column adds up to 1040 against the clerk's
  1030, and his eight totals to 2740 against his 2734. Every figure was
  looked at on the scan (his 8 is a loop with a stroke inside, like a θ).
  The boys of the town: the digit looks like his 6, but 270 comes out
  only with 58, and the editor read 58.
- All figures of both tables agree with the editor's transcript.

## People and places

- The Chamberlain's wife who enlarged the church, "Pani z Rozrazeskich
  Prusimska Szambelanowa", is Katarzyna Prusimska, born Rozdrażewska, widow
  of the chamberlain Paweł Prusimski (people.yml, `prusimska-katarzyna`).
- New people: Józef Zurkowski, Teodor Czartoryski, Ignacy Augustyn
  Kozierowski, Paprocki, Dorposki, Stefan Wardencki, Strzałkowski; after
  the spot sheet, Bogusławski and Golińska (not shown to be the Teresa
  Golińska who married Krzysztof Prusimski, nor the Anna Golińska, born
  Bojanowska, of the decree of 1775).
- Patterns added for this holding's spellings: Trąmbczyn/Trambczyn,
  Maryanton, Skokom, the parish's Nowa Wieś, Łazy and Olędry; "po Swięcie"
  (the feast) shut out of Swięcia; "Komornikow" (cottagers) shut out of the
  glossary's court officer and the termbase's komornik. The Trambczyn
  pattern also finds Trąbczyn in Breyer's notebook (APP 53/968/0/-/669,
  document 2), correctly.

## Still to do

- The reference stays "ADWł 85": the archive's holdings have no series
  name to put before it (editor, 2026-10-16).
- Offered: the rest of the visitation of Trąbczyn (leaves 26 to 28 recto,
  and the parsonage and income after leaf 29 verso) and the text under the
  Zagórów table, all photographed.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Polish, in one clear hand, in the spelling of its time (iest, ktorey, Dyecezyi), with the usual abbreviations of titles (JWo, JMść, X.) and a few Latin phrases. The two tables of Trąbczyn and the table of Zagórów are drawn with ruled lines; the column headings stand upright and are cut short in the narrow columns. Leaf numbers are written in the top right corners.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The editor photographed fifty pages of the volume, each a single page, named by leaf. Only the nine pages their transcription covers are included: leaves 23 verso, 24, 24 verso, 25, 25 verso, 28 verso, 29 and 29 verso, and leaf 34a. Leaf 34a is a leaf added after leaf 34.

### Transcription

The editor transcribed the parts of the nine pages that concern Trąbczyn and the Zagórów table. That transcription left out some passages of the same pages (the souls of the parish and the register extract of 1790, the second half of leaves 25 and 25 verso, and parts of leaves 28 verso to 29 verso). At the editor's request these were transcribed from the scans by an AI model (Claude). Every page was then read against the scans, the editor's text with it, word by word. The words and figures checked in this way and the passages added are listed for the editor separately.

Two passages on these pages are not transcribed, because they belong to other parts of the visitation: the top of leaf 23 verso, the end of the record of the parish before Trąbczyn; and on leaf 34a the description of the church of Zagórów under the table.

The text keeps the spelling of the page (iest, ktorey, Dyecezyi), and the scribe's abbreviations as he wrote them (JWo, JMści, X., Rku); a colon marks a word he cut short. Each line of the transcription is a paragraph of the page. The word the scribe wrote at the foot of a page to announce the next stands on a line of its own and is not repeated in the reading text. The tables are given row by row, their cells separated by an upright stroke ( | ); the column headings, which the scribe cut short in narrow columns, are given as far as he wrote them. A word read with doubt is marked "[?]". The editor looked at all twelve such words on the scans and settled nine of them; three remain.

### Checking the figures

The table of the souls of Trąbczyn checks itself: every column adds up to the scribe's total, and the totals to his 760, the number the text gives above the table. The Zagórów table does not: the women's column adds up to ten more than the scribe's total, and his grand total is six short of his own column totals. The figures are given as the scribe wrote them. One digit, among the boys of the town of Zagórów, looks like the scribe's 6, but the column comes out at his total only with 5, and the editor read it as 58.

### Division and dating

The pages are two documents: the record of the parish of Trąbczyn, and the table of the parish of Zagórów. Both are dated 1791, the year of the tables; the record of Trąbczyn speaks of 1790 as the past year.

### Summary and translation

The summaries were written in German from the Polish and translated into English; each of their 34 statements was then checked against the text. The English translation was made in the same session from the Polish as checked. It gives the names of the places in the forms used here (Trąbczyn, Mariantów, Nowawies, Zagórów, Oleśnica, Skokum, Kopojno) and leaves the others as written; Latin titles of books stay in Latin.
