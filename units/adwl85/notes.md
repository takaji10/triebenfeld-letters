# ADWł 85

Two documents on nine pages from the volume of the visitation of the Konin
deanery of 1790 and 1791, Diocesan Archive in Włocławek, signature 85: the
parish of Trąbczyn (document 1, leaves 23v to 25v and 28v to 29v) and the
table of the souls of the parish of Zagórów (document 2, leaf 34a). Added
on 2026-10-15 at the editor's request: the editor's transcript read in,
the passages it left out of these pages transcribed in session at the
editor's word, every page read against the scans, translated and
summarised in session, the summaries claim-checked, with the holding's page.
**Not published**: waits for the editor's answers on the spot sheet and
their word.

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
  (`intake/spot_sheet.py`), each with a picture. Not yet answered.

## The figures

- The Trąbczyn table of 1791 adds up in every column to the scribe's totals
  and to 760, the number in the text. The register extract of 1790 has no
  totals.
- The Zagórów table: the women's column adds up to 1040 against the clerk's
  1030, and his eight totals to 2740 against his 2734. Every figure was
  looked at on the scan (his 8 is a loop with a stroke inside, like a θ).
  The boys of the town are read 58 with doubt: the digit looks like his 6,
  but 270 comes out only with 58.
- All figures of both tables agree with the editor's transcript.

## People and places

- The Chamberlain's wife who enlarged the church, "Pani z Rozrazeskich
  Prusimska Szambelanowa", is Katarzyna Prusimska, born Rozdrażewska, widow
  of the chamberlain Paweł Prusimski (people.yml, `prusimska-katarzyna`).
- New people: Józef Zurkowski, Teodor Czartoryski, Ignacy Augustyn
  Kozierowski, Paprocki, Dorposki, Stefan Wardencki, Strzałkowski. Not
  entered until the spot sheet settles them: Bagusławski[?] and
  Golinska[?] (a Teresa Golińska married Krzysztof Prusimski).
- Patterns added for this holding's spellings: Trąmbczyn/Trambczyn,
  Maryanton, Skokom, the parish's Nowa Wieś, Łazy and Olędry; "po Swięcie"
  (the feast) shut out of Swięcia; "Komornikow" (cottagers) shut out of the
  glossary's court officer and the termbase's komornik. The Trambczyn
  pattern also finds Trąbczyn in Breyer's notebook (APP 53/968/0/-/669,
  document 2), correctly.

## Still to do

- The editor's answers on the spot sheet, then their word to publish.
- The archive's reference: given as "ADWł 85". Ask whether the archive
  cites it with a series name before the number.
- Offered: the rest of the visitation of Trąbczyn (leaves 26 to 28 recto,
  and the parsonage and income after leaf 29 verso) and the text under the
  Zagórów table, all photographed.
