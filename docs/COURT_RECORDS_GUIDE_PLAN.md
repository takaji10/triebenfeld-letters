# A guide to reading the Latin court records - the plan

The editor, 2026-11-26: "I have come a long way in my abilities to transcribe Latin court records.
I've often thought about creating a simple guide to help a newbie who is trying to read these
records - things about expansion marks, commonly abbreviated words, structure of entries, etc. ...
Perhaps something for each type of court record that I've handled?"

Nothing is built. This file is the plan, for the editor to rule on (section 7).

## 1. What the guide rests on

The guide is written from the edition's own material, not from a handbook: every rule it states
is shown in a real entry, with the page image beside the transcription, a link to the document,
and the English. The material, counted 2026-11-26:

- **24 court-book holdings**, 1589 to 1792, about 63,600 words of the editor's transcription,
  every one checked against the scans.
- **The kinds of book** the editor has transcribed: *Relationes* (Konin Gr.114-121, Kalisz
  Gr.414, 424, 425, Poznań Gr.1181), *Relationes-oblatae* (Konin Gr.136, 145, 153), *Relationes,
  citationes* (53/4/0/-/62), *Inscriptiones* (Pyzdry Gr.75), *Decreta* in the two forms
  *[protocollon]* and *[inducta]* (53/6/0/-/17, -/36, -/40, -/45, -/46, -/47), and one copy-book
  of privileges (the Ląd copy-book, 53/1455/0/2/21). No *Resignationes* book is in the edition.
- **The kinds of entry** (the documents' `doc_type`): register notes (29), messengers' reports
  (28), protests (17), decrees (13), certifications (6), privileges (3), deliveries of possession
  (2), an attestation, a confirmation, a transfer.
- **327 distinct tilde forms** in the corpora. The commonest: the place adjectives
  (*Nieszczevicen~* 78, *Calissien~* 52, *Vschoven~* 35, *Petricovien~* 24, *Castren~*, *Coninen~*),
  the doubled-consonant plurals (*Actt~* 33, *Citt~* 27, *Litt~*, *editt~*, *notificatt~*), the
  participles (*praesen~*, *Celebran~*, *Audien~*, *viden~*) and the contractions
  (*Cond~nis* for Condescensionis, *Jud~m*, *vn~tis*).
- **The courtesy titles**, which place every person socially: *Magnificus* (540 times),
  *Generosus* (134), *Illustris* (131), *Providus* (33), *Nobilis* (33), *Reverendus*,
  *Honoratus*, *Famatus*, *Laboriosus*, *Excellens*, *Spectabilis*.
- **The vernacular inside the Latin**: Polish closing formulas and whole Polish entries, and German
  trade words in Polish dress, brought in by *vulgo* ("commonly called"): *Auscuk* for Auszug,
  *Klapek*, *Rynek* (Pyzdry Gr.75).
- **The lessons already learnt**, written in `docs/EDITORIAL_RULES.md`, `docs/WORKING_NOTES.md`
  and the holdings' notes: *per*, not *pro*, for the p with a stroke through its tail; *Patrui*,
  not *Patrii*; the sitting's heading belongs to the entries **after** it; the crosses that
  place an insertion; struck words are left out; a word is never completed from the sense.

## 2. The editor's rulings (2026-11-26)

- **A web page on the site that reads like a book**: continuous prose in chapters, read from the
  beginning, not a reference page of crops. The examples are the entries' own words, quoted and
  explained in the text; a link to the document lets the reader see the page if they want it.
- **About how the entries are built**: their openings, their set formulas, their closings ("left on
  the table" and the like), what is fixed and what varies.
- **The tilde forms with care**: an abbreviation expands by its case ("Calissien~" is Calissiensis,
  Calissiensi, Calissiensem ... by the word it agrees with), so the guide teaches the stem and how
  to choose the ending, and points out the hard contractions whose missing letters are in the
  middle ("Cond~nis" = Condescensionis; "condescensorialis").
- **From the difficult places of the edition's own transcriptions**: the readings the checks
  changed, and why.
- **Latin court books first.** (Polish entries, copy-books and resignations later, if at all.)
- **And the plan's own suggestions as well** (the editor: "But also the things you suggested. I was
  just talking about what came to the top of my mind"): the ladder of titles, offices and kin; the
  place adjectives; dates; money and measures; the vernacular inside the Latin; the letter shapes
  that mislead; how to transcribe; a worked example and an exercise in every chapter; the reference
  appendices. Section 3 holds them all.

## 3. The shape of the book

A title page and a short preface (who it is for, what it covers, how to use it with the edition),
then chapters, each a few thousand words, meant to be read in order.

1. **Before you begin.** The courts (castle and land) and their books; what a volume is, how its
   entries follow one another, the sitting heading and the entries under it; the volume's title on
   the archive's catalogue (protocollon, inducta) - checked against the fonds descriptions and
   Gloger before anything is said.
2. **How an entry is built.** The general pattern every entry shares: the number in the margin,
   the opening that brings the person before the court ("Ad Officium et Acta praesentia
   Castrensia ... personaliter veniens ..."), the titles that place him, the act (recognovit,
   manifestatur, decernit), the closing, the signature, the docket underneath.
3. **The messenger's report** (relatio): who the general messenger was, the citation he served,
   where and how he left it ("super mensa hippocaustorum ... reliquisse", in the presence of the
   mother of the household, the steward, the clerk), the royal citation recited inside the report
   ("Stanislaus Augustus Dei Gratia Rex ... Mandamus ut ... compareas").
4. **The protest** (manifestatio): the grievance, the formula of protest, "Salvis de Jure
   Salvandis".
5. **The register note**, the certification, the delivery of possession: the short entries.
6. **The acknowledgement and the transfer** (inscriptio): "Recognovit quia ...", the run of verbs of
   cession ("cessit contulit transposuit transtulit et transfudit"), the vernacular words inside
   (Tracholz's "Auscuk", the Polish "ręką trzymaną").
7. **The decree of the land court**: the parties (Actor, Citatus), the "Judicium ... decernit", the
   condescension (the hearing on the ground) and its vocabulary.
Every chapter of the kinds (3-7) ends with **a worked example** (one whole entry of the edition,
quoted, its abbreviations expanded, put into English part by part) and **an exercise** (a second entry
for the reader to try, the answer behind a plain `<details>`).

8. **Dates.** Feria and feast; in Vigilia, in Crastino, post Dominicam; the movable Sundays; working
   a date out, with the edition's own dated entries as the worked examples.
9. **Abbreviations.** How the clerks abbreviated (suspension, contraction, the doubled consonant of
   the plural and participle, the strokes on p and q); how to choose the ending by the case; the
   hard contractions, one by one.
10. **People and places in the Latin.** The ladder of titles (Magnificus, Generosus, Nobilis,
    Famatus, Honoratus, Providus, Laboriosus ...); offices; kin (patruus, relicta, frater
    germanus); the place adjective (Nieszczevicensis, Trąmpczynensis).
11. **The vernacular and the money.** Polish closing formulas and Polish words in Latin entries;
    German trade words in Polish spelling, brought in by *vulgo* (*Auscuk* for Auszug, *Klapek*,
    *Rynek*); money (imperials, florins, groschen, pfennigs, ducats) and measures (*mansi*, *łany*,
    *włóki*), with what the edition's documents show of them.
12. **The hand.** The letter shapes that mislead, described in words and shown by the readings they
    produced: minims (r/n/u/m: *Fericorum* or *Fenicorum*), c and t, the long s, e with a tail, the
    clerk's p with a stroke (*per*, not *pro*), the figures. A small crop only where a shape cannot be
    told in words (the book is not a spot sheet).
13. **How to transcribe.** The edition's own rules, short: keep the scribe's spelling; mark doubt;
    expand in brackets only where certain; leave struck words out; follow the crosses of an insertion;
    never complete a word from the sense.
14. **Where readers go wrong.** The traps of the edition's own transcriptions, from the logged
    changes: minims, the p with a stroke, words skipped, the inserted line and its cross, the
    struck word, and the word completed from the sense (Claude's own *hasce* for *hisce*).
15. **Appendices**: the list of abbreviations with their expansions by case; the formulas in one
    place; the feasts; the ladder of titles and the offices; money and measures; the place
    adjectives (from `reference/places.yml`); the legal terms (links into the glossary); further
    reading (Gloger, Cappelli's *Lexicon abbreviaturarum*, Grotefend, the archives' fonds
    descriptions).

**Form on the site**: one page per chapter under /guide/court-books/, a contents page, previous and
next at the foot; Latin quoted in italics with the English after it; a short Latin passage may be
set out line by line with the English beside it. No script (WORKING_NOTES). English only.

## 4. How it is made (sub-agents first)

1. **The harvest** (done 2026-11-26, `pipeline/guide/harvest.py`, free): `reference/guide/`
   `abbreviations.yml` (321 tilde forms, 816 occurrences, each with its context),
   `formulas.yml` (openings and closings of 81 Latin documents in seven kinds),
   `difficult.yml` (1,387 logged changes: the checks' corrections and the graded changes).
2. **Three Sonnet readers** (started 2026-11-26): every tilde occurrence expanded by its own case,
   with the reason (`abbreviations_expanded.yml`); the changes sorted into lessons
   (`difficult_lessons.yml`); the skeleton of each kind of entry (`skeletons.yml`). Claude checks
   each before it is used.
3. **Claude writes the chapters**, one at a time, the pilot first (chapter 3, the messenger's
   report); the editor reads it and rules on the voice before the rest.
4. **A build step and a check**: the chapter pages from Markdown in `guide/court-books/`;
   `verify_site.py` holds that every document a chapter cites exists and every Latin quotation
   stands in that document's transcription.

## 5. Order of work

The harvest and the readers (now); the pilot chapter (the messenger's report); the editor's
ruling on its voice; chapters 2, 4-7; then 8-14, which draw on all of them; chapter 1 and the
preface last; the appendices from the data.

## 6. What the guide is not

Not a Latin grammar, not a general palaeography, and not a substitute for the archives'
inventories. It covers the books the edition holds, the hands those books were written in, and
the years 1589-1792.

## 7. Questions settled, and still open

Settled 2026-11-26: a web page on the site, reading like a book; Latin court books only; built
on how entries are made, the tilde forms by case, and the edition's own difficult places.
Open: the pilot chapter's voice (after it is written); whether the editor writes a short preface or
a paragraph of their own experience.
