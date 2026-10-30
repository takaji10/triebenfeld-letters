# 53/968/0/-/801 (APP)

Three documents on 16 pages, plus the cover as front matter: copies made about
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

## The documents

Three documents, one per paper (editor, 2026-10-05: "three documents is
fine"). The holding was built and published as one document first, a deed
package like APP 53/71/0/-/57, and divided the same day:
`intake/split_documents.py` put the markers into `corpus.txt` and re-keyed
the correction log; `intake/corrections.py` still names every correction
under document 1 and is not to be run again. Document 1 is dated 19 February
1805 (Guhrwitz), document 2 28 January 1806 (Kalisz), document 3 21 March
1806 (Mariantów); 1 and 2 are tied to 3 by a `supplements` relation.

| Pages | Document |
|---|---|
| 0036-0038 (1-3) | 1. "Copia. General-Vollmacht": the Prince's power of attorney for Triebenfeld, Guhrwitz justice office near Breslau, 19 February 1805, with the office's attestation; the copy certified by the patrimonial court, "Marianten den 21. Maerz 1806", signed Schenck |
| 0039-0041 (4-6) | 2. "Wir Friedrich Wilhelm ...": the consent of the South Prussian War and Domains Chamber, Kalisz, 28 January 1806, signed Schmiedecke, Korn, Koch, Woyde, Nenickel |
| 0042-0051 (7-16) | 3. The hereditary-lease contract for 100 Hufen of the Drzewce forest, § I to § XIX, signatures, attestation, and the court's engrossment, "Mariantów d. 21 Mäerz 1806" |

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
  14526 (document 16) is of 20 December 1804 and was engrossed at Marianton
  on 13 May 1806, attested by the same Heinrichs, Schenck and Brauer: the
  same course of business.
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

Three German summaries (one at first, rewritten when the holding was
divided) written in the session from the reading, the English translated
from them (`intake/summaries_draft.py`). **Not claim-checked**; no
`reading.json`. `site/_data/summaries.yml` and `summaries_de.yml` were not
rebuilt from the local cache: the new lines were inserted into each.

## Authorities (2026-10-05)

Matched without change: Triebenfeld, Hohenlohe, Stillfried, Koeppen,
Kaleschke ("Koleschke"), Schenck ("Schenck", "Schenk"). Five place patterns
were widened for the copyist's and the editor's forms: Trąbczyn
("Trompczyn"), Mariantów ("Marianten"), Szetlewek ("Szedlewek"), Swięcia
("Święcia", "Święca"), Nowawies ("Nowawieś"). The last also brought in
"Nowawieś" in III. HA MdA, III. Nr. 12367, document 7, where it stands in a
list of the Trąbczyn villages. No other holding gained or lost a match.

**Heinrichs** has his own entry (`heinrichs`), held to this contract and to
Oe 1 Bü 14526, document 16. The editor asked (2026-10-05) whether he is
Honrichs. He is not, as far as the documents show: the Prince's own copy of
the Althütte lease (14526-16), in another hand, has the same attestation by
"Heinrichs, Königl. Kammer Commissions Rath und Oconomie Commissarius", so
two independent copies write the name with ei and give him a royal office.
Martin Honrichs, the buyer of Witów and later agent on the estates, is
nowhere called Commissionsrath or Oeconomie-Commissarius.

Not added: the eighteen lessees (none is named in another holding), Brauer
the clerk, the five officials of the chamber, and the places Broniki, Stara
Huta, Ratyń and Ląd.

## The site (2026-10-05)

`about.md` and `process.md` in both languages; two timeline entries (the
consent of 28 January 1806, with Oe 1 Bü 14526 document 8 as its other
source; the contract of 21 March 1806) and this document added to the entry
for the power of attorney. In the era essay, section III (both
languages), the sentence on the crown's licence was wrong and is corrected:
it said the division had been licensed the year before the punctation of
April 1805, where both copies of the consent are dated 28 January 1806 and
rest on cabinet orders of October and December 1805 (the letters agree: Oe 1
Bü 9454, 166 and 179). The essay now links both copies, and has a short
paragraph on the Drzewce lease as the case of uncleared forest. The
holding pages of APP 53/71/0/-/57, Oe 1 Bü 14526, Nr. 3705 and Oe 1 Bü 9454
name this holding among their related holdings.

## Translation and claim check (2026-10-05)

Translated in session at the editor's word, as Nr. 12366 was, not by the
paid run; the pages are in `intake/translation/doc<N>.yml`, written into the
untagged cache by `intake/translation/write_cache.py`. Status `translated`,
`published_tag: ""`.

- **Read beside the other copies.** The published English of the power of
  attorney in APP 53/71/0/-/57 and of the consent and a sister lease in Oe 1
  Bü 14526, document 8, was the model, so the same formula has the same
  English ("ground lordship", "hereditary canon", "transfer fee
  (Laudemium)", "manorial lordship (Dominium)", "official copy").
- **Where this copy differs, it is followed and flagged:** "Haupt- und
  Verkauf" (principal and sale; the others "Kauf und Verkauf"), "Special
  Vollmacht", "uns in unserem Königlichen Hause", the edict of "1. März
  1804" (the other copy "1ten May"), "decretiren" for "declariren",
  "Kriegs- und Rath", "Angaben" for "Abgaben", "bis auf ... Holtz", "wer
  dürfen". Proposals for the German are in each page's
  `emendation_suggestions`; none is applied.
- **Names.** Settled forms where the edition has them: Zagórów, Witów,
  Trąbczyn (also for Trompczyn), Kalisz, Wrocław, Górzyce (Guhrwitz),
  Świniary (Schweinern), Mariantów (Marianten, Mariantow), Szetlewek
  (Szedlewek), Swięcia (Święca, Święcia), Świątniki, Kopojno, Schenck. Five
  of these were added as variants in `reference/places.yml` for this copy
  (Trompczyn, Marianten, Mariantow, Szedlewek, Święcia, Święca, Świątnik).
  As the page spells them, because the edition has not settled them or other
  published English keeps them: Drzewiec, Olesnica (document 3), Nowawieś,
  Stara-Hutta, Lond, Ratyń, Koleschke, and every lessee.
- **check_translations.py:** 2 rows, neither a fault. In document 2 the
  termbase patterns for *Dismembration* and *Ausfertigung* match the verbs
  "dismembriren" and "ausfertigen lassen", rendered "to dismember" and
  "caused to be made out".
- **uncanonical_names.py:** nothing in this holding (the five rows it
  reports are older, in Nr. 12765 and Oe 1 Bü 9454).
- **Crosses.** "xxx heißt N." is "xxx is called N."; a dash stays a dash.

`intake/claim_check.yml`: 35 statements, 33 supported, two weakened (the wood
rights of Ląd and Ratyń in document 2; "dafür" before the free years in
document 3). The English summaries follow, and now use the termbase's words
(demesne farm, Government, Midsummer, general attorney).

## Still to do

- The English has not been read against the scans.
- The fee note on the last page (`intake/unresolved.md`).
- Settled by the editor on 2026-10-05: Heinrichs and Honrichs are kept
  separate; three documents; "Dr." before Johann
  Wendel Heilmann is the right reading; Michael Just's 5 Hufen.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

German, in the legal register of the time, with the Latin terms of the courts. The copyist writes the German in Kurrent script and names and foreign words in Latin script, numbers the pages 1 to 16, and spells several places in his own way (Zagurowo, Trompczyn, Lond). He copied the list of the lessees' shares with corrections: two names are written in between the lines and the numbering is altered. A note of the court's fees beside the last lines is not transcribed.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive supplied seventeen images: the cover and sixteen single pages. They are shown as they came, without cropping.

### Transcription

The editor supplied the transcription as one text, written paragraph by paragraph and not line by line, and marked with the page numbers 1 to 15. It was divided to match the pages; the text of page 16, which had no mark of its own, was separated at the first signature on that page. The words on the cover were added from the image.

### Division into documents

Each of the three papers is one document, by the editor's decision: the power of attorney, the consent and the lease contract. Each is dated from its own text: the power of attorney by the day it was given, 19 February 1805; the consent by the day it was issued, 28 January 1806; the contract by the day the court engrossed it, 21 March 1806, since the opening of the record, with the day the contract was made, is missing.

### Corrections

An AI model (Claude) compared the whole transcription with the scans and corrected it where the page is plain. 84 passages were changed, each logged with its reason. Most are typing slips and single misread letters. For two of the three papers another copy of the same text is here, and each was used as a second witness: the power of attorney in [[unit:app5371057]] and the Chamber's consent in [[unit:oe1bu14526]]. Four changes go beyond a letter or two. A line and a half of the consent that the transcription had skipped was added. The share of one lessee, Michael Just, was corrected from 10 Hufen to 5, as the page has it; with 10 the shares would not add up to the 100 Hufen the contract names. One lessee's name was corrected from Siemert and Liemert to Liewert. The three crosses with which eleven lessees signed were added before their names as "xxx". The copyist's own spellings were kept.

### Summaries

The summaries were written in German from a reading of each document against its scans, and translated into English. Each statement in them was then checked against its document, under the same rules as the separate check that the summaries of other holdings received: a summary may say only what the document says. Of 35 statements two said more than the text and were weakened: one on the wood rights in the consent, one on the purpose of the rent-free years in the contract.

### Translation

The documents were translated into English in a working session under the same rules as the other holdings: every figure, name and mark of doubt carried across, names in their settled forms where these exist and otherwise as the page spells them, and passages that do not read left visibly doubtful rather than smoothed. The published English of the other copies of the power of attorney and of the consent, and of a lease from the same court, was read beside them, so that the same German formula has the same English. Where this copy differs from the others in a word, the English follows this copy and a note records the difference. The same automatic check as elsewhere then confirmed that every figure survives into the English.

### Still to do

The note of the court's fees on the last page is not transcribed.
