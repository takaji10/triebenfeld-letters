# 53/17/0/-/Konin Gr.119 (APP)

Eight documents on eight pages: entries of the Konin municipal court register,
1783 and 1784 (five messengers' reports, two certificates of a search, one
protest). Latin. Added on 2026-10-07 in the fifth Prusimski-era batch.
Status `translated`. Built and verified locally, **not published**.

**Read the docstring of `intake/holding.py` first.**

- **Fully checked** (2026-10-07): every entry read against the scans. 48
  corrections in `holding.py` (ROWS), 8 more in `intake/full_check.json`
  (the first half of document 1, document 6), applied with `--full`.
  Neither is to be applied again.
- **"Arestum X non praevenit"** means that the arrest (laid by the
  citation) did not reach the man, not that someone forestalled it. The
  editor's English had it both ways; see also 53/6/0/-/47, corrected the
  same day.
- **Document 7 is the protest the land court's decree of autumn 1783
  cites** (53/6/0/-/47: "manifestatione coram Actis Castrensibus
  Coninensibus, sub celebratione Judiciorum praesentium ... illata"). It
  names two men Prusimski can produce, Gregory and Thomas; the decree
  names the two accused, Józef the coachman and Walenty the
  under-coachman.
- **Dates.** Read: 3, 5, 8. Sitting: 4. Inferred to the month: 1, 2
  (March 1783), 6 (May 1783), 7 (October 1783).
- **Seven scans not used** (144, 320, 321, 348, 349, 680, 681): entries
  the editor photographed and did not transcribe, several of them on
  Prusimski; listed in `docs/archive/PRUSIMSKI_QUESTIONS.md`.
- **"Captain of Niszczewice"** in the editor's English here for
  "Capitaneus"; the other holdings have "Starost". Left; in the questions
  file.
- Not indexed as people: Maszewski, Jaroszewski, Liberacki, Raczyński, the
  messengers Stachowski, Bekierski, Matuszkiewicz.

- **"Starost", not "Captain".** The editor's English of this holding had
  "Captain of Niszczewice" and "Captain-General of Greater Poland"; at their
  word (spot sheet, 2026-10-07) it is "Starost" throughout, as in their
  other translations (`english()` in `holding.py`).

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 7 scan(s), 5 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- Nothing else. The seven scans with entries that are not transcribed are
  not relevant (editor, 2026-10-07) and stay out; asked again about scans 680
  and 681, which touch the cause of 53/6/0/-/47 entry no. 43, the editor
  said the same.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Each entry stands among others on its page; the pages are shown whole and the other entries are not transcribed. The Latin is formulaic and heavily abbreviated. Four entries have no dated heading of a sitting above them: one is dated from the heading higher on its page, three to the month from the citation they report, the headings before and after, or the land court's decree; each says so. Seven further photographs show entries that are not transcribed.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The folder has fourteen photographs of this book, each showing two facing pages. Seven carry an entry that is transcribed; each of those was cut at the fold, and eight halves are shown whole. Seven photographs show entries that the editor did not transcribe and are not used. The photographs are from Skanoteka, the scanning project of the Polish genealogical society (skanoteka.genealodzy.pl), and carry its watermark across the middle of the image.

### Transcription

The editor transcribed eight entries and supplied them by paragraph, with the Latin written out.

### Check against the scans

An AI model (Claude) read every entry against the scans, word for word, and corrected 56 readings: 48 in a first pass, which left one entry and the first half of another unread, and 8 when those were read at the editor's word.

Those that change the sense: in the search of September 1784 a line had been passed over, and the office certifies that the report of citation does "not exist". In Chełmski's second citation a phrase was restored, that Łomowo "belongs to the plaintiff's principal estate of Łukom"; the acts are charged as done at "your" order, Prusimski's, not his steward's. The citation asks that "the production of the men be ordered and an inquiry held", where two words had been left unread. In his protest Prusimski offers "to clear himself", not to make amends. In the report of May 1783 a line had been passed over, which says that the citation was left at the farm at Nowa Wieś. Each change is logged with its reason.

### Division and dating

Each entry is a document. Three are dated by the line "Actum in Conin" directly above them and one by the heading higher on its page. Four have no dated heading on a photographed page: two are dated to March 1783 from the citation they report and the next heading, one to May 1783 from the heading three leaves before it, and Prusimski's protest to October 1783 from the land court's decree that cites it. Each says so.

### Translation

The English is the editor's own translation and was not made again. It was changed in fourteen places where the text had been corrected, and "Captain" for "Capitaneus" was made "Starost" throughout at the editor's word, as in their other translations.

### Summaries

The summaries were written in German from the Latin and translated into English. Each of their 27 statements was then checked against its document. All held.
