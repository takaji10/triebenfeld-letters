# 53/17/0/-/Konin Gr.117 (APP)

Thirteen documents on eighteen pages: entries of the Konin municipal court
register, 1778 and 1779 (six messengers' reports, five protests, two
register notes). Latin, two with Polish. Added on 2026-10-07 in the fourth
Prusimski-era batch. Status `translated`. Built and verified locally, **not
published**.

**Read the docstring of `intake/holding.py` first**: it has the table of
which entry is on which leaf, scan and page, and the two passes of the check.

- **Fully checked** (2026-10-07, at the editor's word, after a light check
  the same day). 50 corrections in `holding.py` (ROWS), 159 more in
  `intake/full_check.json`, applied with `--full`. Neither is to be applied
  again. No document is marked `rough` any more; about 45 marks of doubt
  remain, each looked at and not readable with confidence.
- **"per", not "pro".** The clerk's "p" with a stroke through the tail is
  "per". The editor wrote "pro" for it throughout; with an accusative it
  means "by" (docs/WORKING_NOTES.md).
- **"jurto" is "juramento"**: Chełmski's oath at the last mound in 1775
  (documents 4 and 5), not "jurisdiction".
- **Three passed-over lines restored**: leaf 71 verso (twice), leaf 78
  verso.
- **"Patrui", not "Patrii".** Paweł Prusimski is Antoni's paternal uncle
  ("sui Manifestantis Patruum", leaf 55), and "Relicta Patrui" is Katarzyna,
  born Rozdrażewska. The editor's text had "Patrii"/"Patris" sixteen times
  and the English "father" fifteen times. Seen on leaf 55 ("Patruj", three
  times); corrected everywhere on that ground. `reference/people.yml`
  (prusimski-pawel) now says how the two were related.
- **"cui ... Ipse Patruo Debitor Extitit"** (leaf 55): it is Tracholz who
  was the uncle's debtor, not Chełmski; the English is changed. Document 8
  bears it out.
- **The decree of 20 October 1777 "injunctae Condescensionis"** is not in
  the edition. It is probably entry no. 17 of that sitting in 53/6/0/-/46,
  which the editor transcribed and which was not built (it names Tracholz).
  In the questions file.
- **Dates.** Read: 1, 2, 7, 11. From the sitting's heading elsewhere on the
  opening (`sitting`): 8, 9, 12. Inferred (`rulings.yml`, basis shown): 3 to
  March 1778; 4, 5, 6 to April 1778 (between 1 and 3 April); 10 to 1778
  (between 25 April and 6 May); 13 to 1779 (the heading at the top of leaf
  507 verso is cut off by the photograph).
- **Not on the photographed pages:** the text "sub signo #" of document 10;
  the heading of document 4.
- **Left as the editor has them:** "Super Manifestationem Antonii Prusimski
  Starosti Niesczevicensis" on leaf 54 verso (the scan has "Sup. Mnem" and
  his autograph "Antoni Prusimski Sta: Niesz..."); "Sokołowski" in the
  heading of document 5, who is not in its text; the name of the mound
  "[T?]urnata"; "Joachimenski[?]" / "Joachimczyki[?]" in document 11 (the
  same man is Jachimowicz and Joachimowicz elsewhere); "Providens" for Szepczyński in document 8;
  "Expedite", "officina Ibidem" in document 9; the expansions of the place
  adjectives ("Calissiens[i?]").
- Szepczyński, "Providus" and court messenger in his own reports, is
  "Laboriosus", a working man, in Nosalski's protest.
- People: Katarzyna Prusimska's entry takes documents 7 and 8, Paweł
  Prusimski's 3 and 7. Not indexed: Tracholz, the judges Walknowski,
  Zielonacki and Mikorski, Czarnecki, Nosalski, Bogusławski, the messengers
  Jankowski and Matuszkiewicz.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 15 scan(s), 9 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- Nothing else: the full check is done.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Each entry stands among others on its page; the pages are shown whole and the other entries are not transcribed. Seven of the thirteen are long entries in a formulaic Latin in which most words are abbreviated. They were read against the scans a second time, word for word; some words in them remain marked as doubtful. Two reports give what the messenger saw in Polish. Antoni Prusimski here calls Paweł Prusimski his "patruus", his father's brother; no other holding says how the two were related. Chełmski's first protest has no heading on the photographed page. The note of the decree of remission points to a text "opposite, under the sign #", which is not on the photographed pages. Six entries have no dated heading of a sitting above them; three are dated by the heading elsewhere on the opening, three from the headings before and after, and each says so.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The folder has fifteen photographs of this book, each showing two facing pages. Each was cut at the fold. Eighteen of the thirty halves carry an entry that is transcribed and are shown whole; twelve are left out. The photographs are from Skanoteka, the scanning project of the Polish genealogical society (skanoteka.genealodzy.pl), and carry its watermark across the middle of the image.

### Transcription

The editor transcribed the entries that concern Trąbczyn and supplied them by paragraph, with the Latin written out. The long entries are a first reading and mark more than two hundred words as doubtful.

### Check against the scans

An AI model (Claude) read the holding against the scans in two passes and corrected 209 readings. The first pass was a light one: every heading and date line, the names of the judges, and five of the eighteen pages word for word (the report of 7 March 1778, the report on the boundary pine, the report of January 1779 and Nosalski's protest), 50 readings. At the editor's word the long Latin of the seven other entries was then read through, eleven pages, and 159 more readings were corrected. About 45 words remain marked as doubtful: they were looked at and could not be read with confidence.

Those that change the sense: Prusimski is cited to "produce" his subjects at the sitting on the ground, not to hold them. The judges are Walknowski and Mikorski, and a line the transcription had passed over is restored in the first citation to the Tribunal. The boundary mound, not a second estate, bears the name written above the line; the men of Rzgów were taken "as they fled" with the pines. Nosalski's people were carting trees "on sledges", and he means to have Prusimski's two men "shut out from giving testimony". One word was corrected throughout, sixteen times: "Patrui", the uncle's, for "Patrii" or "Patris", the father's. It was looked at on one page, where it is written "Patruj", and corrected elsewhere on that ground. Chełmski's signature under his two protests was added.

The second pass found three passages where the transcription had passed over a line or part of one, and restored them: two in Prusimski's protest of 15 April 1778, one in the citation served on him on 25 April. It found one sign misread throughout: the clerk's "p" with a stroke is "per", by, where the transcription had "pro", for; so the claim was acquired "by" Chełmski, and the decree of 1775 was given "by" his commissioners. And it found one word misread in Chełmski's two protests: "jurto" is "juramento", the oath he swore at the last mound in 1775, where the transcription had "jurisdiction". Other corrections that change the sense: Chełmski says Prusimski treated his own commissioners' act as "invalid" (the English had "inviolable"). One of Prusimski's fellow-swearers is "lacking full sense"; the land judge, asked to send the cause to the Tribunal, sent it back "to himself and the whole court". The sums in question were borrowed by Tracholz from Prusimski's uncle, not the other way round. Each change is logged with its reason.

### Division and dating

Each entry is a document. The note of Prusimski's first protest and the text it points to on the facing leaf are one. Four documents are dated by the line "Actum in Conin" directly above them and three by the heading of their sitting elsewhere on the opening. Six have no dated heading on a photographed page: four are dated to the month from the headings before and after them, two to the year. Each says so.

### Translation

The English is the editor's own translation and was not made again. It was changed in 62 places where the text had been corrected, and "father" was made "uncle" in fifteen.

### Summaries

The summaries were written in German from the Latin and Polish and translated into English. Each of their 54 statements was then checked against its document and rests on words that are not marked as doubtful. All held.
