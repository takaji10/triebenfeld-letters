# 53/17/0/-/Konin Gr.116 (APP)

Twelve documents on thirteen pages: entries of the Konin municipal court
register, 1775 to 1777, on the boundary commission between Trąbczyn and
Łukom (register notes, four signed protests, two certificates of a search,
three bare headings). Latin, signatures in Polish. Added on 2026-10-07 in
the fourth Prusimski-era batch. Status `translated`. Built and verified
locally, **not published**.

**Read the docstring of `intake/holding.py` first**: it has the table of
which entry is on which leaf, scan and page, and everything done to the
editor's file.

- **Leaf numbers** were read off the scans; the photographs are numbered in
  a series, not by leaf (the table in holding.py).
- **Folds** set by eye; `courtbook.find_fold` is 20 to 60 px too far right
  on these photographs.
- **Dates.** Three from the "Actum in Conin" line the editor transcribed
  (2, 6, 8). Three from the heading of the sitting elsewhere on the leaf
  (`sitting`: 7, 9, 10). Six inferred (`rulings.yml`, basis shown): 1 to
  August 1775; 3, 4, 5 to September 1775; 11 to 1777 from its place in the
  book; 12 to October 1777 from the land court's decree (53/6/0/-/46),
  which cites Chełmski's own search at Konin that month.
- **Added by me:** signatures under documents 3, 4, 5, 7, 8, 12; "Vacuum"
  and the signature under it in 9 and 10. Three words in the signatures of
  document 3 are not read ("[?]"): Brzeziński's starosty (he was Starost of
  Inowrocław by the decree; only "Sta" and a flourish are sure), Stanisław
  Dąmbski's office (a blot), and the word after "Podwoie:" in Umiński's.
- **The clerk writes "Dapiferi"** for Kwilecki and Umiński; they sign
  "Czesnik", as the decree of 1775 has them. Left as written; the about
  page says so.
- **"Limitatur"** (document 11): the editor's "the matter is thereby
  restricted" is kept. It may mean that the entry is closed off; in the
  questions file.
- **Document 8** asks for a decree "in Contumaciam Magnifici Prusimski
  Prolatum": not the Estates' commission's decree, which was for him. The
  about page says, as my reading and marked as background, that it is
  presumably the act of Chełmski's own commissioners (document 3).
- **Not transcribed:** the pen strokes under the heading on leaf 94 verso;
  the "Vacuum" signed by Chełmski at the top of leaf 95 verso (its heading
  is on a page not photographed).
- People: Ludwik Dąmbski's entry takes document 3. Not indexed: Brzeziński,
  Stanisław Dąmbski, Rajewicz, Lipiński, Ostrowski, Zielonacki, the
  Gliszczyńskis.

- **Rajewicz's protest (document 5): "Cumque".** The check read "Citraque
  Ejus Assensum", without his consent. The editor, on the spot sheet of
  2026-10-07, reads "Cumque" on the page; that stands, their English "with
  his consent [?]" is back, and the summary and the holding's page no longer
  speak of consent. ("Utraque" was also typed into the sheet's box.)

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 9 scan(s), 8 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- The questions in `docs/archive/PRUSIMSKI_QUESTIONS.md`.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Each entry is a few lines among many others on its page; the pages are shown whole and the other entries are not transcribed. The Latin is heavily abbreviated and the transcription writes it out. The signatures are autograph and in Polish, except Rajewicz's; in three of them a word is not read and is marked. The clerk's Latin calls Kwilecki and Umiński "dapifer", pantler; they sign as "cześnik", cup-bearer, which is also what the commission's decree calls them. Five of the twelve entries have no dated heading of a sitting on a photographed page; they are dated from the headings before and after them or, for the last, from the land court's decree, and each says so.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The folder has nine photographs of this book, each showing two facing pages. Each was cut at the fold. Thirteen of the eighteen halves carry an entry that is transcribed and are shown whole; five are left out. The photographs are from Skanoteka, the scanning project of the Polish genealogical society (skanoteka.genealodzy.pl), and carry its watermark across the middle of the image.

### Transcription

The editor transcribed the entries that concern the boundary commission and supplied them by paragraph, with the Latin written out.

### Check against the scans

The entries are short, and an AI model (Claude) read all of them against the scans and corrected 18 readings. Those that change the sense: Dąmbski is the "palatine", the voivode himself, and the heading of the commissioners' protest does not name a president; the Starost of Inowrocław is Brzeziński; and the four headings that ended in an unread word end in "Manifestatur" or "Remanifestatur", protests and counter-protests. The signatures under seven entries, and the word "Vacuum" with the signature under it in two more, were added. Each change is logged with its reason.

### Division and dating

Each entry is a document; the three notes of the sitting of 16 August 1775 are one. Three documents are a heading under which nothing was written. Three entries are dated by the line "Actum in Conin" directly above them, and three by the heading of their sitting elsewhere on the leaf. Six have no dated heading on a photographed page: four are dated to the month from the headings before and after them, one to the year from its place in the book, and the last to October 1777 from the land court's decree that cites it. Each says so.

### Translation

The English is the editor's own translation and was not made again. It was changed in thirteen places where the text had been corrected, and the signatures were added to it.

### Summaries

The summaries were written in German from the Latin and translated into English. Each of their 37 statements was then checked against its document. All held.
