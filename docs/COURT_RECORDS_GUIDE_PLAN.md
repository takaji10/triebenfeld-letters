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

## 2. Who it is for, and where it lives

**The reader** is a newcomer who can look up a Latin word but has never read a Polish court
book: a genealogist, a local historian, a student. It assumes no palaeography.

**Proposed home: a section of the site** ("Reading the court books", from the footer and from
each court-book holding's page). The examples then link straight to the page images and
documents the edition already serves, and a reader can go from the guide's example to the
whole entry. English first; German later, all at once, as with the other pages (the editor's
word on the overhaul). No script on the pages (WORKING_NOTES: the viewer does not run it);
"show the answer" panels are plain `<details>`.

The alternative, a standalone PDF or booklet, is weighed in section 7.

## 3. The shape

### Part I - Foundations (common to every book)

1. **The courts and their books.** The castle court (*gród*, *castrensis*) and the land court
   (*ziemski*, *terrestris*); the grod office that kept the books open every day for
   uncontested business; what *protocollon* and *inducta* mean on an archive's title (to be
   checked against Gloger and the archives' fonds descriptions before anything is said; the
   edition holds the descriptions of the Pyzdry and Kalisz fonds in `reference/sources/`).
2. **The page.** Entry numbers in the margin ("No 39"); the heading of a sitting ("Actum in
   Castro ... Feria Sexta in Crastino Festi ..."), which governs the entries **below** it; the
   docket under an entry ("Super Transfusionem ..."), which names it; signatures, including the
   *ręką trzymaną* of a man who could not write; insertions marked with crosses, struck words,
   marginal notes, catchwords. Each shown on a crop from the edition's scans.
3. **Dates.** The *feria* (Feria 2da = Monday) with the feast it counts from ("in Vigilia",
   "in Crastino", "post festum"); the movable Sundays (Septuagesima, Invocavit, Laetare); a short
   table of the feasts the edition's entries use, each with a real example and the date worked
   out. Months written with numerals (*8bris* = October).
4. **Abbreviation.** The kinds, each with the commonest examples from the corpus: suspension
   (*Calissien~*), contraction (*Cond~nis*), doubled consonants for plurals and participles
   (*Citt~* = Citatus/Citati, *Actt~* = Actorum ...), the strokes on p and q, *&c.*, *Mpcus* /
   *Mci* for Magnificus, superscript endings. How the edition writes them: the letters on the
   page, the supplied letters in square brackets (the editor's ruling of 2026-11-22), the tilde
   in the older holdings.
5. **People.** The ladder of courtesy titles and who gets which (the magnate, the noble, the
   townsman, the merchant, the court messenger, the peasant: the edition's examples of each);
   offices (*Capitaneus* = starost, *Succamerarius*, *Thesaurarius Vschovensis* ...); relations
   (*patruus*, *relicta*, *frater germanus*, *successores*).
6. **Places.** The adjective of the place (*Nieszczevicensis*, *Trąmpczynensis*), *de villa*,
   *in*, *haeres bonorum*; how the edition identifies them (the register and the gazetteer).
7. **The vernacular in the Latin.** Polish formulas and Polish entries; German words in Polish
   spelling (*Auscuk*); trade words; *vulgo*; money and measures (imperials, florins, groschen,
   ducats, *mansi* and *łany*).
8. **The hand.** The letter shapes that mislead: minims (r/n/u/m - *Fericorum* or *Fenicorum*),
   c and t, the long s, e with a tail, the clerk's p-stroke, figures. Shown as crops paired
   with the edition's settled reading.
9. **How to transcribe.** Short and practical, from the edition's rules: mark doubt, never complete
   a word from the sense (with the edition's own mistakes as examples: *hasce* for *hisce*),
   leave struck words out, follow the crosses, keep the scribe's spelling.

### Part II - One chapter per kind of book or entry

Each chapter has the same parts: what the book is and who comes to it; the **skeleton** of the
entry (the formula, line by line, with the English beside it and the parts that change marked);
the words and abbreviations of that kind; **one worked example** from the edition (crop, the
transcription with the abbreviations shown and expanded, the English, a link to the document);
**a second example to try**, with the answer behind a `<details>`; and what to watch for.

1. **Messengers' reports** (*relationes ministeriales*): "Ad officium et acta praesentia
   castrensia ... personaliter veniens Providus ... Ministerialis Regni Generalis ... recognovit
   se ... citationem ... reposuisse". The commonest entry in the edition (28).
2. **Royal citations**, as the reports recite them: "Stanislaus Augustus Dei Gratia Rex Poloniae
   ... Tibi ... Mandamus ut ... compareas".
3. **Protests** (*manifestationes*): "... manifestatur solennissime ...", with Antoni Prusimski's
   protests of 1778 as the examples (17).
4. **Register notes** (29): the one-line entries, and how to tell what they are.
5. **Oblata**: a document brought in to be copied into the book: the boundary decree of 1775
   (Konin Gr.145, in Polish) and of 1782 (Gr.153).
6. **Inscriptions** (*inscriptiones*): the voluntary acknowledgement before the court,
   "Recognovit quia ..."; transfer and cession, *cessit contulit transposuit transtulit et
   transfudit*; Tracholz's transfer of 1768 (Pyzdry Gr.75) as the example, with its German words.
7. **Decrees of the land court**: "Inter ... Actorem ... et ... Citatum ... Judicium ...
   decernit"; condescension (a hearing on the ground); the decrees of 53/6/0/-/40 to -/47 and
   the condescension decree of 1784 (Poznań Gr.1181).
8. **Deliveries of possession and certifications** (Kalisz Gr.414 and the certifications).
9. **Copies of privileges**: the medieval charter's formulas (invocation, witness list, dating),
   from the Ląd copy-book and the Kodeks Dyplomatyczny Wielkopolski.
10. **Resignations** (*resignationes*): not in the edition. Either written later from an entry the
    editor supplies, or left out (section 7).

### Part III - Reference

The abbreviation list (every tilde form of the corpus with its expansion, its count and a link to
an example); the feast calendar; the titles ladder; offices; money and measures; the place
adjectives (from `reference/places.yml`); the legal terms (links into the existing glossary,
466 entries' worth of patterns); further reading (Gloger's *Encyklopedia staropolska*, Cappelli's
*Lexicon abbreviaturarum*, Grotefend for dates, the archives' fonds descriptions).

## 4. How it would be made (sub-agents first)

1. **Harvest by script** (free): every tilde form with its context and expansion where the
   edition already settled one; every title, office, feast and *feria* formula; the openings of
   each kind of entry (the first 25 words of every document by `doc_type`); the vernacular words.
   Into `reference/guide/*.yml`, each row pointing to its document and page.
2. **Sonnet sub-agents**, one per chapter: from ten or more entries of the kind, propose the
   skeleton (what is fixed, what varies) and pick the clearest example and the exercise. Claude
   checks each skeleton against the entries and settles the readings.
3. **Crops** of the examples by script from the page images the site already has
   (`site/assets/scans/`), CSS backgrounds as on the spot sheet.
4. **Claude writes the prose**, to HOUSE_STYLE; every fact about an institution checked first in
   the edition's documents and the fonds descriptions, then Gloger (online, Wikisource); what
   only a handbook says is attributed to it.
5. **The editor's own voice and lessons**: a short list from the editor of what tripped them up
   at the start is worth more than any handbook (section 7, question 5).
6. **A build step and a check**: the guide's pages from the YAML and the chapters' Markdown, and
   `verify_site.py` holding that every example's document and crop exists and that every
   abbreviation in the list occurs in the corpus.

## 5. Order of work

1. The harvest (step 1) and the abbreviation list: useful at once, and it shows how much each
   chapter has to work with.
2. **A pilot chapter: messengers' reports** (the most material, the simplest formula). The editor
   reads it and rules on the form before the rest are written.
3. Inscriptions (Tracholz) and protests; then decrees, oblata, citations, notes, deliveries,
   privileges.
4. Part I, written last from what the chapters needed, so it explains only what a reader meets.
5. The German, all at once, at the editor's word.

## 6. What the guide is not

Not a Latin grammar, not a general palaeography, and not a substitute for the archives'
inventories. It covers the books the edition holds, the hands those books were written in, and
the years 1589-1792.

## 7. Questions for the editor

1. **Home**: a section of the site (proposed), or a standalone PDF or booklet, or both?
2. **Reader**: the English-speaking genealogist (proposed), or also the Polish reader (Polish
   pages)?
3. **Polish entries**: include the Polish-language court entries (the boundary decrees of 1775 and
   1782, the closing formulas) in the guide, or Latin only?
4. **Resignations**: leave them out until you supply an example, or write the chapter from the
   general sources, marked so?
5. **Your lessons**: would you write down, in a few lines each, what you found hardest at the
   start, and what finally made it click? They would go into the guide in your words.
6. **The pilot**: messengers' reports first (proposed), or another kind?
