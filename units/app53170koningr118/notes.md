# 53/17/0/-/Konin Gr.118 (APP)

Twenty-nine documents on thirty-seven pages: entries of the Konin municipal
court register, 1780 to 1782 (sixteen one-line notes, five messengers'
reports, six protests, a certificate of a search, an unwritten entry).
Latin, three in Polish. Added on 2026-10-07 in the fifth Prusimski-era
batch. Status `translated`. Built and verified locally, **not published**.

**Read the docstring of `intake/holding.py` first**: it has the table of
which entry is on which leaf and scan, and the two passes of the check.

- **Fully checked** (2026-10-07, at the editor's word, after a light check
  the same day). 42 corrections in `holding.py` (ROWS), 133 more in
  `intake/full_check.json`, applied with `--full`. Neither is to be applied
  again. No document is marked `rough` any more; 19 marks of doubt remain.
- **Five passed-over passages restored**: three lines in document 13, one
  line in document 10, some words in document 17.
- **Document 14** is addressed to Prusimski and to the Bogdańskis: Teresa,
  born Rozdrażewska, is the successor of her late sisters Katarzyna
  Prusimska (heiress of Grab) and Molska, castellan's wife of Rogoźno.
  "Illustris Magnifice Prusimski" is the vocative: there is no "Magnifica
  Prusimska" in it. Its citation is dated 26 November 1781 and was served
  on 7 December 1781, yet the entry stands among those of spring 1782 and
  names 3 June 1782: the date in `rulings.yml` (1782, inferred) is left.
- **Leaf numbers** are the later ones in the margins; the struck-through
  numbers at the head of the pages are an older count. The right-hand leaf
  of each scan is in `SCANS`.
- **Document 2** (leaf 266 verso) was not in the editor's file; I
  transcribed and translated it. **The entry under "[173]"** (Gurowski and
  the townsmen of Brdów) is left out. Both are in the questions file.
- **Dates.** Ten read, three from a heading elsewhere on the opening, fifteen
  inferred (six to the month, nine to the year); the bases are in
  `rulings.yml`. Document 24: the heading says Saturday before Michaelmas
  and "29"; dated 28 September (the Saturday).
- **What the Tribunal decided** is known only from Górski's protest
  (document 17): a post-commission decree of 23 January 1782, the cause
  decided "ex Mappa", two contradictory commission decrees resolved, mounds
  to be raised along the line on the map. The decree itself, the map, the
  decrees of the sittings on the ground (documents 11 and 28) and the
  inspection (18) are "in productis" and not in the book.
- **Antoni Prusimski's descent** (document 23): son of Stefan Prusimski and
  Wiktoria Malczewska; grandson of Krzysztof Prusimski and Teresa Golińska;
  uncles Jan, Bogumił, Antoni and Paweł. `reference/people.yml`: the entries
  for Krzysztof, Paweł and Katarzyna take the documents that name them.
- **"anteacti ... Praesentanei"** (document 6): the former and the present
  heir of Biskupice. The editor's English had "formerly Starost".
- **Left as the editor has them:** "Loci busto" (document 18; the English
  has "at the mound"); "pro quo pa[c?]em Cavet" (13); in document 27 the
  name before "Szkudlarka", "z Torami", and the words lost at the edge of
  leaf 673 verso; "ac [A?] cum Haerede" (10).
- Not indexed as people: Zielonacki, Górski, Gosławski, Malechowski,
  Lubstowski, the Zakrzewskis and the other heirs, Maszewski, the
  messengers Głabik, Wrzask and Matuszkiewicz.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 32 scan(s), 21 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- Nothing else: the full check is done.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Each entry stands among others on its page; the pages are shown whole and the other entries are not transcribed. The Latin is heavily abbreviated; the long entries were read against the scans a second time, word for word, and a few words in them remain marked as doubtful. Fifteen entries have no dated heading of a sitting above them and are dated from the headings before and after, some only to the year; each says so. One heading gives a weekday and a day of the month that do not agree, and the weekday is followed. One note is unfinished, and one entry is a heading with nothing written under it. One note, which the editor had photographed but not transcribed, was transcribed. 

Antoni Prusimski appears here as "Ostroróg Prusimski" and as knight of the Order of St Stanislaus. The citation of September 1782 is the only document that names his parents and grandparents.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The folder has thirty-two photographs of this book, each showing two facing pages. Each was cut at the fold. Thirty-seven of the sixty-four halves carry an entry that is transcribed and are shown whole; twenty-seven are left out. The photographs are from Skanoteka, the scanning project of the Polish genealogical society (skanoteka.genealodzy.pl), and carry its watermark across the middle of the image.

### Transcription

The editor transcribed the entries that concern Trąbczyn and supplied them by paragraph, with the Latin written out. One note on a photographed page was not in the editor's text; an AI model (Claude) transcribed it from the scan, four lines in a clear hand. One entry in the editor's text, a note of a decree for the town of Brdów, does not concern Trąbczyn and is left out.

### Check against the scans

An AI model (Claude) read the holding against the scans in two passes and corrected 175 readings. The first pass was a light one: every heading and date line, the twenty short entries word for word, the opening and close of the longer ones, and the signatures, 42 readings. At the editor's word the longer entries were then read through, eight documents on sixteen pages, and 133 more readings were corrected. Nineteen words remain marked as doubtful: they were looked at and could not be read with confidence.

Those that change the sense: the first note is a report "to the Tribunal", and its plaintiff Zielonacki is "judge", not the court. Gałecki and Skórzewski are "the former and the present" heirs of Biskupice; a citation is to the "condescension", the sitting on the ground, at Grab. The abbot is Ludwik Benedykt Lubstowski; the witnesses of a note of August 1782 are Reczkowski, Świętosław Bogusławski and the messenger Matuszkiewicz; and the boundary decree of December 1782 was "given", not entered "in the protocol". Signatures were added under six entries.

The second pass found five passages where the transcription had passed over a line or some words, and restored them. In the protest for Prusimski against the land court, three lines: the court refused the delay because, it said, the cause belonged to the register of Greater Poland, while the Tribunal was then hearing that of Płock; it "cut off the delay and ordered the matter to be brought in". In Górski's protest, the words that Chełmski acted "setting at nought the authority of the Tribunal". Other corrections that change the sense: in the citation to the sitting at Grab, Teresa Bogdańska is the successor of her two late sisters, and the four working men to be produced are Prusimski's own subjects. Chełmski charges Górski with "interpreting" the decree, and says its line cannot be carried out without cutting off the one settler adjudged to him. The pines felled in November 1782 were carted away "to" Chełmski's estates. Each change is logged with its reason.

### Division and dating

Each entry is a document. Ten are dated by the line "Actum in Conin" directly above them and three by the heading of their sitting elsewhere on the opening. Fifteen have no dated heading on a photographed page: six of them could be dated to the month and nine only to the year, from the headings before and after them. One heading names the Saturday before Michaelmas and the 29th, which was the Sunday; it is dated to the Saturday, the 28th. Each says so.

### Translation

The English is the editor's own translation and was not made again. It was changed in forty-nine places where the text had been corrected; six lines that had come into the file from a chat window were taken out; and the note that was newly transcribed was translated in the editor's terms.

### Summaries

The summaries were written in German from the Latin and Polish and translated into English. Each of their 69 statements was then checked against its document and rests on words that are not marked as doubtful. All held.
