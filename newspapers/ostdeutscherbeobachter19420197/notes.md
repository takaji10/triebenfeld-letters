# Ostdeutscher Beobachter, Jg. 4, Nr. 197 (19. Juli 1942): how the item came in

Given by the editor on 2026-10-22 as the folder
`C:/Users/Tersnaus/Downloads/131605_Ostdeutscher_Beobachter_Organ_der_Nationalsozialis/`
with the article's image (`1492.jpg`, the WBC page, 2586 × 2064, JPEG
grayscale), a markdown file with the German transcription and an English
beside it, and the link
https://www.wbc.poznan.pl/dlibra/publication/121214/edition/131605/content .
The editor's words: "Add a new newspaper article to the project" and "No need
to inspect the original article against the image; the transcription is
secure". The image file and the markdown are not kept in the repository (raw
scans are not; the site carries the page image the item page shows,
`site/assets/newspapers/ostdeutscherbeobachter19420197/page.jpg`, a copy of
the WBC file).

## Provenance

The page comes from the **Wielkopolska Digital Library** (Wielkopolska
Biblioteka Cyfrowa, the digitisation of Instytut Zachodni w Poznaniu):
publication 121214, edition 131605, object 1492 — the issue of 19 July 1942,
Jg. 4, Nr. 197, of the *Ostdeutscher Beobachter: Organ der
Nationalsozialistischen Deutschen Arbeiterpartei: Verkündungsblatt des
Reichsstatthalters im Reichsgau Wartheland und seiner Behörden*, Posen,
NS-Gauverlag (the paper ran from 1 November 1939 to 1945 as the NSDAP's
organ in the Warthegau, successor of the Posener Tageblatt). The link is the
item's `source:`, shown on its page. The WBC site was behind its browser
check when the record was looked at; the citation was confirmed from the
library's own record data and the Zeitschriftendatenbank's title information
through search results.

The slug follows the plan's rule (`<papertitle><year><issue>`):
`ostdeutscherbeobachter19420197`. The item is in the era `twentieth-century`
(its working name), like the 1937 item.

## The editor's rulings of 2026-10-22 (the identifications)

Put to the editor with the item's open questions, answered the same day in
three sentences:

- **"Drommin = Trąbczyn."** The article's Amtsbezirk Drommin is the commune
  of Trąbczyn under its occupation name — what the register already carried
  (`renamed`, from Jehke, the editor's word of 2026-10-21) is confirmed as
  the identification of the article's name.
- **"Lazinsk = German-era name for Łazińsk, the colony which went by many
  name variants."** The article's Lazinsk is Łazińsk — the colony, not a
  part of one: this settles the register's open question ("whether the
  register's Łazińsk / Łaziny is that name or a part of the colony") in the
  direction that Łazińsk names the colony. The register records Łazińsk as
  a variant of **Trąbczyńskie Stare Olędry**, so the article's Lazinsk is
  that colony — the 1746 foundation, later Łazińskie Stare Olędry and
  Staro-Łazińska. The paper treats the place as one village of some 170
  families with one school and one cemetery; Breyer's notebook of 1936
  distinguishes its "Nowou. Alt Łazinsk" — the Stare and Nowe colonies —
  so the article's single name covers what the notebook names in two.
  Breyer's own open question ("whether 'Łazinsk' of 1936 is both Łazińskie
  colonies", the notebook's NEEDS_CONFIRMATION) is untouched by this.
- **"Kolonia Łazińskie is a variant of Łazińsk/Lazinsk."** Mielewczyk's
  form (2017, p. 48, among the new villages on the parcelled lands of
  Trąbczyn) names the same colony. This settles the question his item had
  left open ("a pattern would have to say which colony"): it is the Stare
  colony, and the form is matched.

Worked in the same day:

- `reference/places.yml`: "Drommin" a matched variant of trabczyn; "Lazinsk"
  and "Kolonia Łazińskie" matched variants of trabczynskie-stare-oledry;
  the register's open question rewritten with the ruling. The bare Polish
  "Łazińsk"/"Łaziny" stay `match: false` (their literal would also catch
  the Nowe colony's "Łazińskie"; matching them would bring Breyer's
  "Łazinsk" of 1936 in — the editor's word).
- `newspapers/index.yml`: the item's "Drommin" (1 hit) ruled to trabczyn,
  its "Lazinsk" (6 hits) to trabczynskie-stare-oledry.
- `literature/index.yml`: Mielewczyk's "Kolonia Łazińskie" ruled yes to
  trabczynskie-stare-oledry — the hit his item's index had left unmade.
  **The index files are shared with parallel sessions**: the newspapers
  file's hunks went in with the Twoja Słupca session's commit of that file
  (which carried the whole of it, this item's rulings included); the
  literature file also carries the Łukasiewicz (1997) session's uncommitted
  rulings, so only the Mielewczyk hunk was staged for this work's commit,
  theirs left for that session.

## How it was read

The transcription came **with the file** and was not read against the page
(the editor's word: "the transcription is secure"; no OCR, no spot sheet, no
paid run). The English came with the file too and is Claude's — the editor's
word of 2026-10-22 on the direct question — so the item's page carries the
standing caveat, as the 1937 item's does (`english_by`, no
`translation: editor`).

The text stands as the file gives it, with two mechanical differences:

- the markdown escapes of the file (`\-`, `\!`, `\."`) are resolved to the
  marks they stand for;
- the article's own picture (the photograph of the school, "Aufn.: Spatz")
  stands in the file as the reference `![][image1]`; its place is marked
  "[Abbildung]" (English "[Picture]") and its caption is kept as text, in
  italics — the convention of the literature's figures.

The print's line division was not kept: the file came with the paragraphs
whole, and the transcription is the editor's, not re-read. The headline and
the subhead stand as the file sets them; the signature "Willi Spatz." as
printed.

## What was noticed, standing as given

The editor ruled the transcription secure, and nothing was changed. What the
reading of the text itself noticed, recorded here so it is known:

- "auf die wir auch **beute** noch ... treffen" — surely the print's "heute";
  standing as given.
- "die Namen **Kuhn. Merk**, Schönfisch, Haupt" — a period for a comma;
  standing as given.
- the caption's "Kantoratschule" stands against the body's
  "Kantoratsschule"; standing as given.
- "deutsch erhalten **hat. und** deren unbeugsames Ausharren" — the period
  for a comma; standing as given.
- "als ein grauer Zeuge aus **einen** längst vergangenen Zeit" — the
  grammar of the print or of the transcription; standing as given.

## What the item is, and what it bears on

- The paper: the NSDAP's daily for the Reichsgau Wartheland, Posen, from
  1 November 1939 to 1945; a party paper of the occupation. The article is
  kept as a witness of its day, its judgements the paper's own (the item's
  account says so on its page).
- **The place is the edition's own, by the editor's rulings of 2026-10-22**
  (the block above). The article's "Amtsbezirk Drommin" is the wartime name
  of the rural commune of Trąbczyn (`renamed` in reference/places.yml); its
  "Lazinsk" is the German-era name of Łazińsk, the colony the register
  records as Trąbczyńskie Stare Olędry. Its "Lazinsk" is the Łazinsk of
  Albert Breyer's notebook of July 1936 (APP 53/968/0/-/669), which writes
  "Lehrer i. Łazinsk: Mielke seit 1925" and names "Michalinow" beside it —
  the same teacher and the same neighbouring name six years before the
  article; the item is the press's only witness of the place and its school.
- **The date.** The paper's founding of 1718 by fourteen Silesian families
  stands against the edition's own records: the colony is carried from the
  1746 foundation (the register; Chodyła 2015 covers the Olęder settlements
  of the Pyzdry Forest from 1746), and the Nowe Olędry are first attested
  29 September 1776. The difference is recorded in the summary; the edition
  keeps to the documents (the documents-first rule). Flagged in
  NEEDS_CONFIRMATION.
- The people of the article are not in the edition's register: Mielke (the
  teacher and farmer; no person entry), Willi Spatz (the signature; also the
  photographer of the article's picture), the families Kuhn, Merk,
  Schönfisch, Haupt. "Spatz" is likely a pen name; nothing is claimed.
- The article's numbers (about 170 families, 153 children, four teachers)
  and its dates (the school until 1933, the transfer 1937 — "only four years
  more" — the dismissal 1939, the headship since 1940) are the paper's.

## The index

The index of people and places runs over the items (the editor, 2026-10-22).
What the item brings the patterns:

- **Konin** is matched (the article's "Kreisstadt Konin" and the English's
  rendering); ruled in `newspapers/index.yml`.
- **Schlesien** is matched (the region the fourteen founding families set
  out from; the article's "Schlesierlande" is matched by no pattern); ruled.
- **Drommin** (1 hit) and **Lazinsk** (6 hits) are matched from
  2026-10-22, when the editor ruled the identifications (the block above);
  ruled in `newspapers/index.yml`, Drommin to trabczyn, Lazinsk to
  trabczynskie-stare-oledry.
- **Michalinow** is matched by no pattern (the name stands in Breyer's
  notebook too, unmatched); the families Kuhn, Merk, Schönfisch, Haupt and
  the signature Willi Spatz are matched by no pattern.

## Rights

The item is signed ("Willi Spatz"), so the question was put to the editor
directly, with the German term (70 years past an author's death) and the
WBC record's copyright notice named. The editor's word (2026-10-22): "Show
it, no need to flag the rights." The item is shown whole; no rights entry
was added anywhere.
