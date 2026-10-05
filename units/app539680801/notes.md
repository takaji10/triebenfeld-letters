# 53/968/0/-/801 (APP)

One document on 16 pages, plus the cover as front matter: copies made about
1930 of three papers of 1805 and 1806 on the parcelling of the Zagórów and
Trąbczyn estates. Added on 2026-10-05: page images staged, the editor's text
cut to pages, corrected, summarised, and given its place on the site. Not
translated.

## Provenance

Archiwum Państwowe w Poznaniu, fonds 53/968, Spuścizna Alberta Breyera (the
papers of Albert Breyer), number 801; an older number 437 on the cover is
struck through. The cover carries the fonds stamp, the archivist's title
"[Odpisy dokumentów w sprawie parcelacji majątków Zagórowo, Wittow i Trąpczyn
z lat 1805-1806]" and "[1930?]", both in square brackets there.

Albert Breyer (2 February 1889, Żyrardów, to 11 September 1939, Warsaw) was a
teacher at the German secondary schools of Zgierz and Sompolno and a historian
of the German settlements in central Poland (German Wikipedia, "Albert
Breyer"; Kulturstiftung der deutschen Vertriebenen, "Breyer, Albert"; looked
up 2026-10-05, not checked against a printed work). The pages do not name the
copyist or say where the originals were. One hand throughout: German in
Kurrent, names and Latin in Latin script, on lined paper.

- **Images.** Seventeen, `Image00035.jpg` to `Image00051.jpg`: the cover and
  pages 1 to 16 (red pencil numbers). The numbering of the images begins at
  35, so the unit as the archive scanned it may hold more than was
  downloaded; only these seventeen are in the folder.
- **Pages.** Single pages, no cropping: copied unchanged into
  `<raw_dir>/processed/` as `<capture>_a.jpg` (`intake/build_pages.py
  --copy`), as for APP 53/71/0/-/57. `0035_a` is the cover, `0036_a` page 1,
  `0051_a` page 16.

## Transcription

The editor's single Markdown file stays in `<raw_dir>`. It marks pages "[01]"
to "[15]"; page 16 has no mark and was cut off at "Friedrich Siering".
`intake/build_pages.py` cut it into `transcriptions/<page id>.txt`, took off
the Markdown (escapes, and a Wikipedia link on the chamber's name), closed one
paragraph break inside a word ("der Flächen." / "Inhalt"), and wrote the cover
text from the image. It checks that the pages add up to the source text.

By paragraph throughout (`rulings.yml pages: by_paragraph:`).

## The document

One document (the editor's rule of 2026-09-30 for APP 53/71/0/-/57: a deed
package is one document). The pieces:

| Pages | Piece |
|---|---|
| 0036-0038 (1-3) | "Copia. General-Vollmacht": the Prince's power of attorney for Triebenfeld, Guhrwitz justice office near Breslau, 19 February 1805, with the office's attestation; the copy certified by the patrimonial court, "Marianten den 21. Maerz 1806", signed Schenck |
| 0039-0041 (4-6) | "Wir Friedrich Wilhelm ...": the consent of the South Prussian War and Domains Chamber, Kalisz, 28 January 1806, signed Schmiedecke, Korn, Koch, Woyde, Nenickel |
| 0042-0051 (7-16) | The hereditary-lease contract for 100 Hufen of the Drzewce forest, § I to § XIX, signatures, attestation, and the court's engrossment, "Mariantów d. 21 Mäerz 1806" |

- **The contract has no beginning.** Page 7 opens "Gute Olesnica. 17. Johann
  Luckow und 18. Johann Liewert aus dem Fürstlichen Gute Święcia anderer
  Seits": the end of the list of the parties. The page numbers run on without
  a gap, so the copyist left the opening out or the leaf was lost before the
  pages were numbered.
- **Date.** 21 March 1806, read from the engrossment and from the
  certificate under the power of attorney (`dates.read`). The contract itself
  looks older: § VI gives four free years "welche sich mit Weynachten dieses
  Jahres anfangen und mit Weynachten Ein Tausend Acht hundert und Acht
  endigen", which makes "this year" 1804. Yet § I calls Triebenfeld
  "legitimated by the enclosed power of attorney", which is of February 1805.
  Not resolved; no date is inferred from it. The Althütte lease in Oe 1 Bü
  14526 (document 16) is of 20 December 1804.
- **Place.** Marianton (Mariantów), where the court sat.
- **Estates.** Drzewce, Zagórów, Trąbczyn.
- **The lessees and their shares** (list on 0042 and 0043; signatures on 0050
  and 0051). 5 Hufen each unless noted: Johann Friedrich Turno (signs
  Tiernow; "Turnow" in the docket), Martin Dickhoff x, Johann Martin Sydow x,
  Johann Gottlieb Haberland 10, Samuel Schubert, Michael Dickhoff 10 x,
  Gottfried Dickhoff x, Friedrich Siering, Christian Friedrich Vagel x,
  Johann Wilhelm Böttcher x, Johann Büchner x, Ephraim Fuchs, Johann Halbott,
  Johann Wendel Heilmann x, Martin Dikhoff (a second of the name) x, Michael
  Just x, Johann Luckow, Johann Liewert x. "x": signed with three crosses,
  eleven of the eighteen. 16 x 5 + 2 x 10 = 100 Hufen.

## Corrections (2026-10-05)

84 passages, each read on the scan of its page: `intake/corrections.py`,
logged in `transcription_decisions.csv`. What was left is in
`intake/unresolved.md`.

- **Witnesses.** The power of attorney is also in APP 53/71/0/-/57 (pages
  0018 to 0021) and twice in Oe 1 Bü 14526; the consent is in Oe 1 Bü 14526,
  document 8 (pages 0045 to 0047). Where the scan and the other copy agree
  against the transcription, the row says so.
- **Larger changes.** A line and a half of the consent restored ("gedachte
  Herrschaften nebst dem übrigen und größern Theil der Forst"). Michael Just
  5 Hufen, not 10 (the page; the sum of 100). Siemert and Liemert are
  Liewert. "Petenck" is Schenck. "Patalitact der nun als" is "Totalitaet der
  von der". "den rechten" is "den ersten halbjährigen Erbzinß". The crosses
  added as "xxx".
- **Left as the editor wrote them:** ss for ß, t for th and similar spellings
  that do not change the word; "Dikhoff" where the page has "Dickhoff" in the
  list; the accents on "Świątnik", "Święca", "Mariantów", "Ratyń", which the
  page does not all have.
- **The two copies of the consent differ** in one date: this copy has the
  Silesian edict of "1. März 1804", Oe 1 Bü 14526 "1ten May 1804". Each
  stands as its page has it.

## Summary (2026-10-05)

One German summary written in the session from the reading, the English
translated from it (`intake/summaries_draft.py`). **Not claim-checked**; no
`reading.json`. `site/_data/summaries.yml` and `summaries_de.yml` were not
rebuilt from the local cache: the one new line was inserted into each.

## Authorities (2026-10-05)

Matched without change: Triebenfeld, Hohenlohe, Stillfried, Koeppen,
Kaleschke ("Koleschke"), Schenck ("Schenck", "Schenk"). Five place patterns
were widened for the copyist's and the editor's forms: Trąbczyn
("Trompczyn"), Mariantów ("Marianten"), Szetlewek ("Szedlewek"), Swięcia
("Święcia", "Święca"), Nowawies ("Nowawieś"). The last also brought in
"Nowawieś" in III. HA MdA, III. Nr. 12367, document 7, where it stands in a
list of the Trąbczyn villages. No other holding gained or lost a match.

Not added: the eighteen lessees (none is named in another holding), Brauer
the clerk, the five officials of the chamber, "Heinrichs" (see
`intake/unresolved.md`), and the places Broniki, Stara Huta, Ratyń and Ląd.

## The site (2026-10-05)

`about.md` and `process.md` in both languages; two timeline entries (the
consent of 28 January 1806, with Oe 1 Bü 14526 document 8 as its other
source; the contract of 21 March 1806) and this document added to the entry
for the power of attorney. The era essay is not changed: section III already
describes the leases and the consent in general terms.

## Still to do

- Translation and the claim check of the summary, with the other holdings
  waiting for the cloud session.
- The editor's word on the items in `intake/unresolved.md`.
- Glossary candidates are ruled on when the holding is `translated`
  (`glossary_candidates.py` reports none now).
