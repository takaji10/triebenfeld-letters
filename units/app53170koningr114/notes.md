# 53/17/0/-/Konin Gr.114 (APP)

Two documents on four pages: two reports of the court messenger Bartłomiej
Szepczyński for Antoni Prusimski, 22 April and 6 August 1767, on the
embankment at the pond-ground that flooded the Olęder settlers. Latin with
Polish. Added on 2026-10-07, the first holding of the third Prusimski-era
batch. Status `translated`. Built and verified locally, **not published**.

How it was made is in the docstring of `intake/holding.py`.

- **Not used**: scans 336 to 345 (nothing on them is transcribed); the
  second pair of text files for leaves 334 to 334v (a duplicate of the
  second entry). Both are on the list of questions held for the editor.
- **Check**: both entries read whole; 3 readings corrected. Left as the
  editor has them: "Ministerialis Regalis" (the scan has "M Rglis", which
  may be Regni Generalis), "Eorun[dem?]", "Recepit[?]" (a word written over
  another).
- **People**: Antoni Prusimski here is the Starost (the existing entry).
  New entry for the messenger, Bartłomiej Szepczyński (`szepczynski`), who
  is "Szeptycki" in 1754 (Konin Gr.136).
- The English page of the editor's first file ("(English).md") is used for
  both entries.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 4 scan(s), 4 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The book is a register of rough entries, many to a page. The first report stands at the foot of leaf 297 and the top of leaf 297 verso, the second at the foot of leaf 334 and the top of leaf 334 verso. The other entries on those pages are not transcribed. The frame of each report is abbreviated Latin, which the transcription writes out; what the messenger saw is in Polish, in the spelling of the clerk.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive supplied fourteen images of this book: two single pages and twelve images of two facing pages each. The two entries stand on four pages; the two that come from double images were cut at the fold. Ten images carry nothing that is transcribed and are not used.

### Transcription

The editor transcribed the two entries and supplied them by paragraph, with the abbreviations of the Latin written out.

### Check against the scans

An AI model (Claude) read both entries word for word against the scans. The transcription was close: three readings were corrected, none of which changes what the reports say happened. Each change is logged with its reason.

### Division and dating

Each entry is a document. Each is dated by its own opening line, by the church calendar: the Wednesday after Easter 1767, which was 22 April, and the feast of the Transfiguration, 6 August 1767.

### Translation

The English is the editor's own translation and was not made again. It was changed in five places: three follow the corrected readings, and two make plain that it was the messenger, not Prusimski, who went onto the estate. A second English version of the second entry in the editor's files, with notes, is a duplicate and is not used.

### Summaries

The summaries were written in German from the Latin and Polish and translated into English. Each of their nine statements was then checked against its document. All held.
