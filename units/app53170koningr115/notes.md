# 53/17/0/-/Konin Gr.115 (APP)

Ten documents on nine pages: entries of the Konin municipal court register,
1768 to 1773, on the quarrel over the Lusnia wood (four register notes, five
messengers' reports, one protest). Latin with some Polish. Added on
2026-10-07 in the third Prusimski-era batch. Status `translated`. Built and
verified locally, **not published**.

**Read the docstring of `intake/holding.py` first**: it has the table of
which entry is on which leaf, scan and page, and everything done to the
editor's file.

- **Leaf numbers** were read off the scans. The five photographs (006, 040,
  041, 235, 236) are numbered in a series, not by leaf: 006 is leaves 3v|4,
  040 is 35v|36, 041 is 36v|37, 235 is 240v|241, 236 is 241v|242.
- **Dates.** Six from the "Actum in Conin" line on the page. Three inferred
  to the month (`rulings.yml`, with the basis shown): the heading of the
  sitting is on a page not photographed. Leaf 245: no heading on leaf 244
  verso either; it lies between 2 March (leaf 242) and 13 March 1773 (leaf
  246).
- **Not used:** scans 185, 224, 225, 227, 228, 244, 246; "Incorrect Pages".
- **Added by me:** the two notes on leaf 35 verso as far as read (the editor
  had "Videatur hoc loco…"); Chełmski's signature under the protest; the
  English of the three early notes. All listed for the editor in
  `intake/changes.yml`.
- **Left as the editor has them:** "Filip Wąchnicki" in the protest (the scan
  may have "Filio Wąchnik", the miller's son); "Szarpali Czternaście" in
  document 6; "Quietatus est"; "Tomice [?]" in the heading of document 2.
- **The English "goods" for "gaza"** was wrong twice (the innkeeper's house
  besieged; the house shot through). In the decree of 1728 the same word is
  a hut.
- New kind of document: `protest` (manifestatio).
- People: Katarzyna Prusimska's entry takes document 1 ("olim de
  Rozdrażewskie Prusimska"); Szepczyński is found in document 8. Not
  indexed: the messengers Krzepczyński and Bikierski, Lipiński the steward,
  Marzęcki, Gałecki, the abbot Słowiecki.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 9 scan(s), 4 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Each entry is a few lines among many others on its page; the pages are shown whole and the other entries are not transcribed. The Latin is heavily abbreviated and the transcription writes it out. Two of the notes of 1768 are transcribed only as far as they could be read, and "…" marks what is left out. Chełmski's signature stands under his protest, and twice more at the foot of the page with the entries of 20 December 1771. Three entries stand under a sitting whose dated heading is on a page that was not photographed; they are dated to the month from the headings before and after them.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The folder has sixteen images of this book, each showing two facing pages: eleven from the archive and five photographs. Nine carry an entry that is transcribed. Each of those was cut at the fold, and the half with the entry is shown. Seven images, and a subfolder of pages the editor set aside as not the right ones, are not used. The five photographs are from Skanoteka, the scanning project of the Polish genealogical society (skanoteka.genealodzy.pl), and carry its watermark across the middle of the image.

### Transcription

The editor transcribed the entries that concern Trąbczyn and Łukom and supplied them by paragraph, with the Latin written out. Two of the notes of 1768 were given only by their headings.

### Check against the scans

An AI model (Claude) read against the scans every heading and date line, three of the longer entries whole and the second half of three more, and the notes of 1768, and corrected 24 readings. Those that change the sense: the weapons were presented "by special commission" of Chełmski. The wood is "built upon by the settlers"; the breaking of the embankment is laid to "the subjects of Trąbczyn"; the stripped inn's fittings were carried off by a band "fitted out for a tumult"; "men", not one man, of Podbiele cut the alders. In the protest Chełmski is "heir" of Łukom and the possession was adjudged "to him, the protester". The two notes given by their headings were read on the scans as far as that could be done with confidence. Chełmski's signature under his protest was added. Each change is logged with its reason.

### Division and dating

Each entry is a document; two notes of one sitting on one page are one document. Six documents are dated by the line "Actum in Conin" above them on their own page. Three stand under a sitting whose heading is on a page that is not among the images; they are dated to the month, from the dated headings before and after them in the book, and each says so.

### Translation

The English of seven documents is the editor's own translation and was not made again. It was changed in nine places where the text had been corrected or where it had taken the Latin word for a hut to mean goods. The three early notes had no English; Claude translated them in the editor's terms.

### Summaries

The summaries were written in German from the Latin and Polish and translated into English. Each of their 31 statements was then checked against its document. All held.
