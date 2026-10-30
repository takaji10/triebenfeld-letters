# 53/6/0/-/47 (APP)

One document on three pages: entry no. 26 of the Kalisz land court's
sitting at Konin of October 1783, a decree on an assault at Smoleniec.
Latin, from a microfilm. Added on 2026-10-07 in the fifth Prusimski-era
batch. Status `translated`. Built and verified locally, **not published**.

**Read the docstring of `intake/holding.py` first.**

- **Page names** are in reading order, not by leaf: 0240_b1 (leaf 239
  verso), 0240_b2 (leaf 240), 0240_b3 (leaf 236 verso), as for 53/6/0/-/46.
  The editor's "[236v]" is right: the entry ends on an earlier leaf.
- **Read whole** against the film. A skipped line restored on leaf 239
  verso (an eye-skip between two "et quoniam").
- **"Cond~nem" is condemnationem** here, as in Konin Gr.153, where the same
  condemnation at Grab is named; the editor had "Condescensionem". The
  abbreviations Cond~nis (condescensionis) and Cond~nem (condemnationem)
  differ by one letter: look at each.
- **"Arestum ... non praevenit"**: the arrest did not reach the men (so read with Konin
  Gr.119, document 7); the first build had "did not forestall".
- **Date**: `sitting`, year 1783 only; heading of 20 October 1783 on leaf
  213, not photographed.
- **Entry no. 43 is not in the edition** (leaves 295 verso and 296, 306.jpg,
  sitting of 3 May 1784: Skórzewski against Chełmski over the boundary of
  Biskupice and Łomów; Prusimski and Stadnicki cited). It was transcribed
  and translated in session on 2026-10-07 at the editor's word, built as
  document 2, and taken out the same day at their word: not relevant to
  the project. Its text is kept in `intake/entry_43.md`. Do not build it
  again without the editor's word.
- **Zeromski.** Document 1 had "Albertum [T/F?]eromski"; entry no. 43 writes the
  same proxy "Zeromski", plainly. Corrected in document 1 at the
  editor's word (`intake/full_check.json`, applied with `--full`; not to be
  applied again).
- **"Capitanealis" stands.** Document 1 has "medium vadii Capitanealis",
  written out on the scan; entry no. 43 has "medium Vadii Capitalis". I had
  told the editor that document 1 had an abbreviation there. It does not;
  nothing is changed.
- **Left as the editor has them:** "procuratorem", "ex monte", "gasam". The pen lines along the last two lines of writing on
  leaf 236 verso are taken for the closing rule, not a deletion.
- Not indexed as people: Kłonica, Stablewski, the coachman and
  under-coachman.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 2 scan(s), 2 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- Nothing else.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The entry is no. 26 of its sitting. It fills leaf 239 verso and leaf 240; for want of room the clerk wrote its end on an earlier leaf, 236 verso, under entry no. 22, and marked both places. The first page is in a hurried hand that abbreviates heavily; from the findings on, a second and clearer hand writes. The images are frames of a black and white microfilm. 

The entry has no date of its own. The heading of the sitting, which the editor transcribed from a page that is not among the images, reads: "Actum in Judiciis Terrestribus Palatinatus Calissiensis Districualibus Feria Secunda post Festum Sanctae Haedvigis Viduae Electae videlicet Die vigesima mensis Octobris Anno Domini Millesimo Septingentesimo Octuagesimo Tertia in Conin Celebratis". The entry stands twenty-six leaves after that heading.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The folder has three frames of a microfilm of this book, each showing two facing pages. Two carry the entry. They were cut at the fold, and three of their four halves are shown, in the order in which the entry is read. The third frame has a later entry between other parties, which is not included.

### Transcription

The editor transcribed the entry and the heading of its sitting and supplied them by paragraph, with the Latin written out.

### Check against the scans

An AI model (Claude) read the whole entry against the microfilm and corrected 18 readings. On the first page a line had been skipped, between two occurrences of the words "et quoniam": the court finds Prusimski bound to show his right to be heard, and he does not show it. What Chełmski raises against him is a "condemnation" at Grab, not a sitting on the ground. The witnesses are examined on written questions "exchanged between the parties"; the word that had been left unread after that is "the accused", whose production the court puts off. The servant who came home is "the aforesaid" servant, not one who had been released. Prusimski is to swear "from now and from this act" within six weeks. The clerk's two directions that join the parts of the entry were added. Each change is logged with its reason.

### Division and dating

The entry is one document. It has no date of its own; it is dated to the year from the heading of its sitting, 20 October 1783, which stands twenty-six leaves earlier on a page that is not among the images, and the document says so.

### Translation

The English is the editor's own translation and was not made again. It was changed in eleven places where the text had been corrected. The editor's translator's notes, which discussed readings now settled, are left out.

### Summary

The summary was written in German from the Latin and translated into English. Each of its eleven statements was then checked against the document. All held.
