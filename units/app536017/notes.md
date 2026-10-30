# 53/6/0/-/17 (APP)

One document on two pages: an order of the land court at Konin of June 1589
for an inspection on the ground, in Albertus (Wojciech) Trąmpczyński's suit
against Thomas Łukomski over a pond at Łukom that flooded the woods of
Trąbczyn. Latin with a Polish sentence. The earliest document of the
edition. Added on 2026-10-07 in the second Prusimski-era batch. Status
`translated`. Built and verified locally, **not published**; the editor reviewed the folds on 2026-10-07 (`intake/folds.json`).

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

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 2 scan(s), 2 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- The editor's word on the three entries not transcribed.
- The editor's look at the reading and the English.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The entry begins halfway down leaf 27 under a heading in large letters, "Łukomski Visionem expediet", and ends in ten lines at the top of leaf 27 verso. The Latin is abbreviated in nearly every word; the transcription fills the abbreviations out, and marks the five places where a word is not fully read. 

Three more entries on the same leaves concern the same people and are not transcribed. The next, on leaves 27 verso and 28, is the same plaintiff's suit against Stanislaus Łukomski in nearly the same words. Two more, on leaves 28 to 29, are suits of Nicolaus and Joannes Trąmpczyński against Albertus. 

The entry has no date of its own. The heading of the sitting stands on leaf 2, which the editor transcribed but which is not among the scans: "Actum in terminis terrestribus particularibus Coninensibus feria se[x?]ta ante festum Sancti Viti Martyris proxima Anno Domini 1589 in Conin celebratis". That is, it was done at the particular land court terms of Konin, held at Konin on a weekday before the feast of Saint Vitus the Martyr (15 June) 1589. The editor read the weekday with a doubt. The decree of 1775 gives the day of these decrees as the Monday before Saint Vitus, which in 1589 was 12 June, and the document is dated from that.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive supplied three images, each showing two facing pages of the bound volume. The entry given here stands on the right page of the first image and the left page of the second; those two were cut at the fold and are kept whole. The other pages carry none of the transcribed text and are not shown.

### Transcription

The editor transcribed the entry and supplied it by paragraph. The hand of 1589 abbreviates nearly every word, and the first reading left most words of the court's order in doubt, with 109 marks of doubt in all. The editor's file also had the end of the entry in two readings, an entry from leaf 22 marked as not relevant, and the heading of the sitting from leaf 2. Leaves 2 and 22 are not among the images. The heading is quoted in the description of this holding; the entry from leaf 22 and the second reading are left out.

### Reading again from the scans

At the editor's request an AI model (Claude) read the entry again from the scans, to put it right where that could be done with confidence. It could, because the three entries that follow on the same pages are orders of the same kind in the same set words, and the next one is the same suit against another defendant nearly word for word. Each phrase was read in all the places it occurs. The whole text was replaced by this reading; the editor's first reading is kept beside it in the log. Five places stay marked as not fully read: the tense of the verb in the heading, one word after "under the penalties", and three words whose endings the clerk did not write.

### Division and dating

The entry is one document. It has no date of its own, and the editor's reading of the weekday in the heading of the sitting is in doubt. The boundary decree of 1775 cites this order with its day, the Monday before Saint Vitus 1589, which was 12 June. The document is dated from that.

### Translation

The editor's English had been made from the first reading and marked 33 places as unresolved. It was revised throughout by Claude to follow the new reading, keeping the editor's terms. The largest change: the court does not set "a mutual term"; it adds one of its messengers, chosen and paid by the defendant, to see where and on whose ground the wrong was done. The editor's notes, each on a word that was then unread, are not used.

### Summary

The summary was written in German from the Latin as read again and translated into English. Each of its nine statements was then checked against the document. All held.
