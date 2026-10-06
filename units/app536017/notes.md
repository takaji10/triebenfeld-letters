# 53/6/0/-/17 (APP)

One document on two pages: an order of the land court at Konin of June 1589
for an inspection on the ground, in Albertus (Wojciech) Trąmpczyński's suit
against Thomas Łukomski over a pond at Łukom that flooded the woods of
Trąbczyn. Latin with a Polish sentence. The earliest document of the
edition. Added on 2026-10-07 in the second Prusimski-era batch. Status
`translated`. Built and verified locally, **not published: the editor
approves or moves the folds first** (`review/app536017/folds/`).

## What the editor said (2026-10-07)

"With 53/6/0/-/17, obviously don't import duplicate pages. I think with this
one you should try and re-read it, see if you can fix it, but only if you're
confident."

## Provenance and pages

Archiwum Państwowe w Poznaniu, fonds 53/6, unit 17: "Inscriptiones,
relationes, decreta [inducta] 1589".

- **Three scans**, each an opening: `..864` leaves 26v | 27, `..865` leaves
  27v | 28, `..866` leaves 28v | 29. (An earlier note of mine had the third
  as 27v | 28; it is not.)
- **Two pages of the edition**: `0027_a2` (leaf 27) and `0028_a1` (leaf
  27v). The other halves of those scans are cut and set apart; the third
  scan is not cut.
- **Left out of the editor's file**: "[2]", the heading of the sitting (no
  scan; quoted in `about.md`); "[22]", an entry "Thrampczinski Liber" that
  the editor marks "not relevant" (no scan, and a first reading that cannot
  be checked); and the **second reading of leaf 27 verso** (the duplicate).

## Three more entries on the scans, not transcribed

For the editor to decide. They are the same matter or the same people, and
the decree of 1775 cites them:

1. Leaves 27v to 28, "Lukomski Visionem expediet": the same plaintiff
   against **Stanislaus Łukomski**, nearly word for word as ours.
2. Leaves 28 to 28v, "Thrampczinskich Visio": Nicolaus and Joannes
   Trąmpczyński, brothers, against Albertus, over a pond and a mill in the
   stream between Trąbczyn and Szetlewo.
3. Leaves 28v to 29, "Eorundem Visio": the same against Albertus.

With ours read, 1 could be transcribed with the same confidence; 2 and 3
are the same formulas round new facts and would need more care.

## The re-reading (2026-10-07)

`intake/corrections.py`: the three paragraphs replaced whole by a reading
from the scans, the editor's text kept in the log. **The method**: every
phrase of the court's order recurs in the entries that follow (leaf 28 top
has the end of the order with no damage), so each was read in two to four
places. Readings that change the sense:

- Heading "Visionem exped[ie]t", not "Visio[ru]m expe[cta]t".
- "Exortis ... Controversiis super citationem literalem".
- "in grave damnum et iniuriam Actoris Aestimationis ad Decem millia".
- "decrevit praesentibusque decernit Visionem Juridicam Nihilominusque
  addidit ... **Ministerialem terrestrem** quem sibi pars Citata elegerit ad
  videndum videlicet et conspiciendum quo in loco cuius in fundo iniuria
  praefata illata et utrum facta necne". The first reading had "Mutem
  terem", which the English took as "a mutual term".
- "Cui Visioni partes ambae interesse debent"; "habituri sunt terminum
  peremptorium ad audiendum a praefata Visione iuris restitutionem coram
  Judicio per Ministerialem".

Still marked: "exped[ie]t", "motibus[?]" (the next entry has what looks
like "juditibus" there), "lucran~", "succumben~", "mix~".

## The link to the decree of 1775

Konin Gr.145 (English pages 30, 45, 46, 61, 62, 74) cites "four Kalisz land
decrees in the Konin land court on Monday before Saint Vitus of 1589"
between Wojciech Trąbczyński and the heirs of Łukomia (Tomasz, Jan and
Stanisław Łukomski, and Barbara Brodzińska), over flooding by a new pond;
the inspection held on them on the eve of St James 1589 and attested in
1592; and an oath laid on Tomasz Łukomski. **This entry is the decree
against Tomasz.** Hence the date: Monday before St Vitus 1589 = 12 June
(`rulings.yml`, `dates: sitting:`, with the basis shown). The editor's
"feria se[x?]ta" in the heading is then "secunda".

## Translation, summary, authorities

- English: revised throughout by Claude in the editor's terms
  (`intake/translation/build_docs.py`, which lists what differs in
  substance). The 33 "[T.N.]" notes are not used.
- Summary: German first, 9 statements, all supported
  (`intake/summaries_draft.py`, `intake/claim_check.yml`).
- People: the Trąmpczyński family entry now takes in this document; new
  family entry Łukomski (`lukomski`), matched here only.
- check_translations.py: 2 rows, none a fault.

## Still to do

- The editor's approval of the folds, then publishing at their word.
- The editor's word on the three entries not transcribed.
- The editor's look at the reading and the English.
