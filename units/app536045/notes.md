# 53/6/0/-/45 (APP)

One document on two pages: entry no. 17 of the sitting of 1763 in a book of
decrees of the land court at Konin, the suit over potash between Katarzyna
Prusimska and Stanisław Ścibor Chełmski. Latin. Added on 2026-10-06 from the
editor's scan, transcription and English translation, the first holding of
the second Prusimski-era batch (`docs/PRUSIMSKI_ERA_PLAN.md`). Status
`translated`. Built and verified locally, **not published: the editor
approves the fold first** (`review/app536045/folds/`).

## Provenance

Archiwum Państwowe w Poznaniu, fonds 53/6, unit 45: a volume the editor's
folder calls "Decreta [protocollon] 1750-1765 (Konin)". **The name of the
fonds as the archive gives it is not known here** (the archive's site
refuses automated access); the court is named from the text, "Judiciis
Terrestribus ... in Conin", the land court at Konin.

- **Scan.** One, `673.jpg`: an opening, leaf 653 verso and leaf 654 recto.
  The file name is the archive's image number, not a leaf.
- **Pages.** `intake/build_pages.py --crop` cuts it at the fold (x 1728, the
  gutter, looked at on a strip) into `0673_a1` and `0673_a2`, whole pages,
  each keeping 30 pixels beyond the fold. The upper half of `0673_a1` is the
  end of entry no. 16 and is not transcribed.
- **Leaf 638**, with the heading of the sitting, is transcribed by the editor
  but has no scan. It is not a page; it is quoted in `about.md` and is the
  ground of the date. If the editor has the image, it can be added as a page.

## Transcription and check (2026-10-06)

The editor's file, "... (Latin).md", by paragraph, abbreviations filled out
without marks. All of it read against the scan: 13 readings corrected
(`intake/corrections.py`, logged in `transcription_decisions.csv`). Entry 16
on the same page has the same formulas and settled several. The ones that
change the sense:

- "addit praesentibus eisdem Ministerialem ad pronuntiandam ... eorum testium
  juramenti rotham" (was "addant ... [Ill___?] ad [pro___?] ... earundem
  tertium"): the court assigns its summoner to speak the oath to the
  witnesses.
- "mutuo est indultum" (was "resoluo est").
- "ad quarum lectionem" (was "ad quartam sectionem"): the reading of the
  testimony, not a fourth session.
- "opponente se Notario Thelonei" (was "Magnifico").
- "ac alia in Judicio Tribunalis Regni ... indecisa" (was "ac acta").
- "extradendas" (was "excdendum").

Left as the editor has them: "deducendum" and "deducendo" (both "deduc" with
a mark on the scan; the ending is not written), "Rozdrazewska" (the scan may
have "Rozdrazewskie"), "post hac".

## The document

One document, `doc_type: decree`, Latin, place Konin, estates trabczyn and
lukomia. **Dated by the sitting** (`rulings.yml`, `dates: sitting:`), a new
kind of date made for the court books: the reader sees "from the heading of
the court's sitting" and the basis. Year only: the sitting opened on the
Monday after Trinity Sunday 1763 (30 May); the day of this decree is not
given. The editor's register had "c. 1762-1765 (exact session date not
given)"; the heading on leaf 638 gives the year.

## Translation (2026-10-06)

The editor's English, cut to the two pages by
`intake/translation/build_docs.py`, saved by `write_cache.py`. Six changes
follow the corrected Latin (`FIXES`), each with its reason. Five of the
seven footnotes are left out (`DROP_NOTES`): they discuss readings the scan
does not have. The file's glossary of seven terms is not used; its entry
"roll [Lat. rotha]" was a misunderstanding ("rotha juramenti" is the formula
of an oath).

check_translations.py: 3 rows, none a fault (the termbase expects
"sequestration" and "indult"; one page has twice the words because of the
notes).

## Summary and claim check (2026-10-06)

One summary, German first (`intake/summaries_draft.py`, which also puts the
holding's lines into the site's summary files), 10 statements, all supported
(`intake/claim_check.yml`).

## Authorities (2026-10-06)

New person: Katarzyna Prusimska, born Rozdrażewska (`prusimska-katarzyna`,
matched as "Prusimska" in this document only). The entry for Michalina
(`prusimska`) is shut out of this document (`not_in`). Whose widow she was
comes from the editor's register (Paweł Prusimski, from the inspection of
1754 in Konin Gr.136), copied to
`reference/sources/poznan_cross_reference_map.md`; this document says only
"relicta vidua". Matched without change: the Chełmski family, Trąbczyn,
Łukom, Pyzdry. Not indexed: Gdańsk and Poznań (Latin "Gedanum",
"Posnaniam"), and the lesser parties.

## Still to do

- The editor's approval of the fold, then publishing at their word.
- The fonds' name for 53/6, and the image of leaf 638, if the editor has
  them.
- The editor's look at the changes to their English.
