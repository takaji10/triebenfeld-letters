# 53/4/0/-/62

One document: the entry at the foot of page 222 of the relation and citation
book of the land court at Kalisz for 1726-1727, in Latin - the report of the
court messenger Sebastian Szetlewicz of Szetlewko (Szetlewek) that he served
a citation at Szetlew, and left it on the table in the heated room. The
editor's own transcription, kept as written, with two rulings of 2026-10-26
("Judicius" to "Judicio"; "Citti~" read as Citati). Added 2026-10-26.

Read `intake/unresolved.md` first: it holds the readings the scan did not
settle, the shape of the sentence, and the date-and-place question that is
waiting on the editor's reading of the preceding pages.

## Provenance

Archiwum Państwowe w Poznaniu (APP), fond Księgi sądu ziemskiego w Kaliszu
(53/4), unit 53/4/0/-/62, the archive's title "Relationes, citationes
[protocollon] 1726-1727". The editor gave the fond's description and the
archive's account of the court (kept in `unit.yml`, under `fonds`). The scan
is the editor's download from the archive's online unit
(szukajwarchiwach.gov.pl, jednostka 980058): scan 231 of 349, manuscript page
222, file 53_4_0_-_62_18049603.jpg, copied by `intake/build_pages.py` into
`processed/` as 0222_a (the number is the manuscript's own pagination). The
rest of the volume is not among the scans.

## Transcription

The editor's own reading, given by line, and kept as written. The two
line-end breaks ("Hyp-pocausti", "Ju-ris" in the editor's draft) are written
with the edition's line-end mark ¬ - a matter of convention, no reading
changed. The rulings of 2026-10-26 are in `process.md`; everything else
stands, including the doubt marks ("praeterita[?]", "detulisse[?]",
"[F?]irma") and "(inserat~)" in the editor's parentheses as its own line.

## The point of the entry

The editor added the holding for the name: "Sebastian Szetlewicz de Villa
Szetlewko" shows a Szetlewicz family living at Szetlewko (Szetlewek) in the
1720s. Szetlewicz is a surname, not a place name (the editor, 2026-10-26) -
the session's first draft said the name was formed from the place, and the
editor corrected it. The citation was served at "Villa Szetlewo" - Szetlew,
the neighbouring village.

## The places, and the one mention that moved

The entry is the first text in the edition that tells Szetlew and Szetlewek
apart, so the matching had to change (`reference/places.yml`, 2026-10-26):

- szetlewek's pattern now passes "Szetlew...o" and "Szetlewicz" over
  (`(?!o\b)(?!icz)`); "Szetlewko" still matches szetlewek;
- szetlew is matched for the first time, in the exact form "Szetlewo"
  (`Szetlewo(?![a-zà-ÿ])`), the Kodeks editors' identification (1173
  "Szetlevo", 1261 "Szethowo" glossed "Szetlewo", Szetlew).

Counted against the committed index (the before-snapshots in
`review/app534062/` and WORKING_NOTES mistake 7):

- szetlewek: 91 mention rows before and after; one row moved out - the
  hearth-tax table's "Szetlewo z Częś: Jaroszew:" (APP 53/64/0/-/Kalisz
  Tab.21, page 0019_b) - and one came in, ours ("Szetlewko");
- szetlew: 4 rows, all new - ours, the table's row that moved, and the
  Kodeks's own gloss "Szetlewo" in the entries of 1173 and 1261 (kdw
  documents 2 and 4), which no pattern had matched before;
- people: one mention added, Szetlewicz; nothing else changed anywhere.

The moves follow the same identification the literature index had already
recorded when it refused Breyer 1938's "Szetlewo" for szetlewek ("no:
Szetlew, the village of the Ląd monastery; not Szetlewek"); the matching
ruling for szetlew was added to `literature/index.yml`. Both moves are put
to the editor.

## Dating

`dates: supplied`, 1727, year only - the editor's provisional assignment
from the volume's title. The entry itself gives only "Feria Quinta proxima
praeterita". The sitting's date and its place are to be read from the
preceding pages; then the ruling moves to `dates: sitting:` (the
app536017 shape) and the place override is filled.

## Translation and summary

No paid run (the editor's word, for a single page; the path of
app539680782). The English was written in session under translate.py's rules
and written into the translation cache by `intake/translation/write_cache.py`
- the record carries the source_hash, exactly as a paid run's. The formulas
follow the Konin holdings' established English. `check_translations.py`
raised three rows on the first draft; two resolved on the revision (the
three German doubt markers carried one for one; the termbase's "Court
Summoner" rendering used), the third (the length ratio) ruled OK. The
claim-check reader (`translation_review.py`) had never been run with
`--unit`: it lacked an import, and it recorded cleared keys by letter where
the checker clears by pad - both fixed (WORKING_NOTES, "The
translation-review reader").

The summary was written in English and German in session; its 8 statements
were claim-checked (`intake/claim_check.yml`), all supported after one
corrected in the draft: Matuszkiewicz reports fifty-one years later (1778),
not thirty.

## Damage

None recorded. The page is whole; the writing is firm.

## What the holding owes the site

Done in session 2026-10-26: `about.md`/`process.md` and their German; the
person entries (`reference/people.yml`, `reference/people_bios.yml`); the
place matching above; the summaries; the checks. Timeline: no event added -
the entry names no party and bears on no owner directly; offered to the
editor. The era essay (prusimski-boundary) does not name the holding yet
(offered).
