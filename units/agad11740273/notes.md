# AGAD 1/174/0/2/73

Four documents on five pages, 20 to 23 July 1807: Michalina Dąbska's three
petitions for the return of her father's confiscated estates and the
Governing Commission's draft resolution granting it, from the commission's
file of its stay at Dresden. Added on 2026-10-04 at the editor's request:
pages cut out of the images, the editor's text cut to pages, corrected,
summarised, and given its place on the site; translated and its summaries
claim-checked in session on 2026-10-05. Its companion is
AGAD 1/174/0/1/6 (`units/agad1174016/`), the commission's register.

## Provenance

Archiwum Główne Akt Dawnych, Warsaw, fonds 174 (Komisja Rządząca), series 2,
unit 73: "Akta Komisji Rządzącej pod bytność jej w Dreźnie". The editor first
gave the archive as the State Archive in Poznań and then confirmed AGAD
(2026-10-04). The images carry AGAD's caption.

- **Images.** Five: 05, 06, 07, 08 and 047. The five long-named files in the
  folder (`1_174_0_2_73_2888...jpg`) are the same five again (same sizes) and
  are not used.
- **What the editor asked for.** "Only 05, 07, 08, and 047 need to be added;
  the rest of the pages aren't relevant", and the images "cropped to remove
  the unrelated pages". Their marks 05, 07 and 08 are the pencil leaf numbers,
  not image names: leaf 5 is on image 05, leaf 7 on image 06, leaf 8 on image
  07 and, its back, on image 08. So image 06 is used too. "047" is image 047
  (its leaf is numbered 51 in pencil, over a struck 40).
- **Pages.** One side of each opening, cut out by `intake/build_pages.py
  --crop` (the boxes are in the script; placed on a contact sheet). Page ids
  follow the images: 0005_a2, 0006_a2, 0007_a2, 0008_a1, 0047_a2. The other
  sides are blank, show writing through from the back, or belong to other
  matters (a Niemojewska petition shows at the edge of 047).

## Transcription

The editor's single Markdown file stays in `<raw_dir>`. It is by paragraph.
`intake/build_pages.py` cut it into `transcriptions/<page id>.txt` and wrote
the document boundaries; it checks that the pages add up to the source text.

- **Moved:** the commission's received notes ("Presentatum ...") from the
  head of each petition to the end of its page, and listed in
  `office_notes.yml`; the address of the French petition to its own page
  (0008_a1), where it is written.
- **By paragraph** (rulings.yml): all five pages.

## The documents

| No. | Page | What it is |
|---|---|---|
| 1 | 0005_a2 | Draft: resolution of the Governing Commission, Dresden, 21 July 1807, Polish |
| 2 | 0006_a2 | Michalina Dąbska to the commission, Dresden, 20 July 1807, Polish; presented 21 July |
| 3 | 0007_a2, 0008_a1 | Michalina Dąbska to Napoleon, Dresden, 21 July 1807, French; the address to Małachowski on the back |
| 4 | 0047_a2 | Michalina Dąbska to the commission, Dresden, 23 July 1807, Polish; presented the same day, "ad Acta" |

Bound order, which is not the order of writing: the resolution comes first.

## Corrections (2026-10-04)

25 passages and two added lines, each read on an enlarged crop:
`intake/corrections.py`, logged in `transcription_decisions.csv`. What was
left is in `intake/unresolved.md`.

- **The received note on the French petition** reads "Presentatum 21. Lipca
  1807. na Sessyi Extraordynaryiney w Dreznie przez W. Xcia Dyrektora Woyny z
  rozkazu Nayiaśnieyszego Cesarza y Króla": presented at the extraordinary
  session at Dresden by the Prince Director of War, by order of the Emperor
  and King. The transcription had "Wielmożnego Książęcego Dyrektor Wojny z
  rozkazem". The director of war in the commission was Prince Józef
  Poniatowski; the note does not name him, and he has no mention in the
  index for it.
- **The paraph "St Mał"** (Stanisław Małachowski) under that note and under
  the draft resolution was not transcribed; added as "St[anisław]
  Mał[achowski]".
- **The draft:** "N° Cesarza" (Nayiaśnieyszego) for "W° Cesarza", twice;
  "dla" before "JW. Wybickiemu" is struck out; "JPani" for "JW. Pani";
  "Lipca" stands plainly over a struck "Czerwca".
- **Spelling and abbreviations put back** as the pages have them: "Kommissyi
  Rządzącey", "iaki", "Nayiaśnieyszego", "JW. Wybickiego", "a. c.",
  "zalecić", the address "Jaśnie Wielmożnemu JMci Panu Małachowskiemu ...
  JWWMci Panu Dobrodzieiowi w Dreznie". The meanings are in the docstring of
  `intake/corrections.py` and in `unit.yml` (`translation_note`).

## Rulings and correspondents (2026-10-04)

Dates and places are each document's own dateline. Document 1 is `draft`.
Document 1 answers 3 (the case "referred to us by the Emperor"); 4 answers 1
("the commission's decree of 21 July"). Senders and recipients are in
`correspondents.json`, each with its reason, and in
`reference/correspondents.yml` (Regierungskommission, Michalina Dąbska,
Napoleon).

**Era.** `hohenlohe` for now, as the act that ended his possession. By
`reference/eras.yml` the two AGAD holdings are the first documents of the
restitution era, which is still empty; moving them there needs the editor's
word and a rewrite of `site/the-story.md`.

## Worth knowing from the reading

- She names three Prussian generals as recipients of her father's estates:
  "Xięcia de Hohenlo[h]e, Bischoffswerder i Zanitz". The other holdings name
  Hohenlohe-Ingelfingen and Sanitz only. Bischoffwerder has an entry among
  the people, marked "probably".
- Her list of estates: Trąbczyn (department of Kalisz); Kamionna, Kolno,
  Pawłowo, Pawłówko and a "Magazyn w Wrocławku" (department of Poznań). The
  last is not identified.
- She had petitioned the commission twice before 20 July ("podwakroć").
- The resolution names no estate and reserves nothing. At its end a clause
  is struck out: "z zachowaniem praw Im służących" (with the rights
  belonging to them preserved), read on an enlarged crop; "Im" is the least
  certain word. "Them" is most naturally the owners. It is not transcribed.
  The later lawsuits over Hohenlohe-Ingelfingen's mortgages (III. HA MdA,
  III. Nr. 12366 and 12367) turned on what the return of 1807 carried with
  it, so the clause is worth the editor's eye.
- 12366's Warsaw report of 1818 dates "an order of the Government of the
  Duchy of Warsaw" to 21 July 1807: this is that resolution.

## Summaries (2026-10-04)

German summaries written in session from a reading of each document against
its scan, the English translated from them (`intake/summaries_draft.py`).
Claim-checked in session on 2026-10-05 (below). `site/_data/summaries.yml` and `summaries_de.yml` were
not rebuilt from the local cache: the committed files were restored and the
new entries inserted.

## Authorities (2026-10-04)

People added: Małachowski, Łuszczewski, Bischoffwerder. Patterns widened:
Sanitz takes "Zanitz", Niemojewski "Niemoiewskiego", Hohenlohe the editor's
"Hohenlo[h]e", Michalina the genitive "Dąbskiey / Dambskiey / Dąmbskiey"
(which also found her in the Polish judgment of Nr. 12366). Places: Dresden
takes "Dreznie", "Drezno", "Dresde"; Warsaw "Warszawie"; Kolno "Kolna" after
Kamionna. Not added, for want of a firm identification: Finckenstein,
Pawłowo, Pawłówko, "Wrocławek", and Wybicki's Manieczki, Przylepki, Boreczek
and Esterpol. Glossary: "Lipca" ruled out; the entry for the Prussian court
called Regierung no longer marks "die preußische Regierung" or "the Prussian
Government" (it did so in Nr. 12366 and Nr. 12765 as well).

## Translation and claim check (2026-10-05)

Translated in session, as Nr. 12366 was, not by the paid run; the pages are
in `intake/translation/doc<N>.yml`, written into the untagged cache by
`intake/translation/write_cache.py`. Status `translated`, `published_tag:
""`. check_translations.py: no row. uncanonical_names.py: nothing.

- Names as the page spells them (Dambska, Zanitz, Niemoiewski,
  Hohenlo[h]e with the editor's bracket), except Bischoffswerder, which the
  termbase makes Bischoffwerder, and Trąbczyn. The forms of address JW., JP.
  and JPani are "the Most Illustrious", "Mr" and "Mrs"; the gate's candidate
  "JW." is ruled out in `reference/glossary.yml` for that reason.
- "Magazynu w Wrocławku" is "the Storehouse at Wrocławku", in the page's
  case: the house rule in `english_forms.yml` turns "Wrocławek" into
  Włocławek, which lay in another department.
- "upoznieniem" (document 4) is left in Polish and recorded as not
  construing.

`intake/claim_check.yml`: 28 statements, all supported.

## Still to do

- The editor's ruling on the era.
- Reading the English against the scans.
- The words in `intake/unresolved.md`. The struck clause of the draft is
  settled: the editor ruled on 2026-10-05 that struck-out text is not
  transcribed, so it stays out and is described in these notes only.
