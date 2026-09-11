---
layout: page
title: About this edition
standfirst: How the text was established, what the editorial marks mean, and what is still unresolved.
permalink: /reading-this-edition/
lang: en
alt_url: /de/ueber-diese-edition/
---

## The source

The documents published so far are held in the **Hohenloher Zentralarchiv Neuenstein
(HZAN)**, in two files: `Oe 1 Bü 9454`, eighteen years of correspondence, and
`Oe 1 Bü 14526`, a volume of title deeds. Later eras of the archive will draw on
repositories in Poznań, Warsaw and Berlin; the holding a document comes from is part of its
citation and part of its address here.

The text was transcribed from the original handwriting, which is *Kurrentschrift*, the
German cursive hand of the period, difficult to read and easy to misread. Some of the
deeds carry passages in Polish and Latin, and those are source text too — translated, not
treated as corrupt German.

**The transcription was produced by an AI system, not by a human palaeographer.** This
matters, and the edition does not hide it. Machine transcription of Kurrentschrift makes a
particular kind of mistake: as well as ordinary letter-shape confusions, it can produce
text that is plausible German but not what is on the page. Every editorial decision here
was made with that in mind, and readings that could not be settled from evidence were left
alone rather than guessed at.

## Pages

Letters are presented page by page, as they sit in the archive. Each manuscript page is
shown as its own block, labelled with the range of lines it occupies in the archival text.
Nothing flows across a page break. You still read a letter as a whole; the pages are
structure within it, and they are what the scanned images sit beside.

There are **1,156 manuscript pages** across the 348 documents: 869 pages in the
correspondence, 287 in the volume of deeds.

## Four views of every document

The toggle above the text switches between them.

**Transcription** is the default. It keeps the manuscript's own line breaks, one line per
line on the page, numbered to the archival file so a passage can be cited line by line. But
it is *edited*, not raw. Where a word really is broken across a line it carries a plain
hyphen; where the transcription marked a break that isn't one, the mark is gone. Recurring
names are standardised. This is what the letters say, presented as the editors read them.

**Reading** takes the same text and flows the lines together into continuous prose.

### What has been changed, and why

This edition does not present a strict diplomatic transcription, and the reason is
specific: the transcription was made by an AI system, not a human palaeographer. Most of
what looked like scribal oddity turned out to be machine error. Reproducing those errors
faithfully would preserve nothing of the manuscript and mislead the reader.

Three kinds of change have been made, each on evidence rather than impression:

- **Line-break marks.** In the correspondence, of 1,317 marks at line ends, only 826
  turned out to join a real word. 483 were spurious, 5 were catchwords, and 3 had nothing
  to continue into. Each was decided against this corpus and against historical German
  usage, and every decision is recorded with its evidence. The deeds were checked the same
  way; the figures below are the correspondence's, which is where the marks were densest.
- **Recurring names.** People and places transcribed several ways were standardised to one
  spelling, root only, so German and Polish grammatical endings survive. Where a variant
  turned out to be a *different* person, it was deliberately left alone.
- **Demonstrable slips**, where the same word is spelled correctly elsewhere in the corpus
  or the reading is contradicted by a second copy of the same document.

Period spelling is not corrected. Forms like *laßen*, *seyn*, *nöthig*, *Ewr* and *dero*
are how the writers wrote, and they stand. So do the transcriber's own marks of doubt.

The unedited text still exists. Each holding keeps its transcription exactly as produced,
in `units/<holding>/corpus.txt`, and every editorial layer is checked against it: a change
that no recorded decision accounts for fails the build.

**English** carries the translation, added page by page. Where none exists yet, the view
says so rather than showing nothing.

**Manuscript** shows the page itself. Every image was matched to its page by eye, one at a
time; click it to open full size. In the correspondence, of the 872 images photographed,
865 sit beside a transcribed page: the remaining seven are the series title page, five
sheets that are not manuscript pages, and one page of calculation figures deliberately left
untranscribed.

The images published here are downscaled to 1100 pixels wide, which is enough to read the
hand. The full-resolution originals, about 1 GB, are held offline as the archival masters.

## Why the line-wrap marks had to be checked

The transcription marks a broken word with `¬`, but that mark cannot be taken at face
value, because the transcriber inserted it wrongly a great deal of the time. Of the 1,317
line-end marks in the correspondence, **483 (37%) do not join anything**:

| | |
|---|---|
| `die¬` + `serhalb` | *dieserhalb*, a real conjunction. **Joined** |
| `die¬` + `nöthigsten` | *dienöthigsten* is not a word. **Left apart** |
| `auf¬` + `Übrigens` | two separate words. **Left apart** |

Every mark was therefore decided on evidence, not assumption. Two sources were used: this
corpus itself, which knows the period's spelling, and the [DWDS](https://www.dwds.de)
frequency data, which is lemma-aware, so inflected forms like `Mitgliedern` resolve, and
which covers historical German. A form counts as a real word at a thousand corpus hits or
more; below that, what comes back is proper-name noise.

The result: **826 genuine joins, 483 marks that join nothing, 5 catchwords**, and 19 cases
flagged for checking against the originals. Every decision is recorded with its evidence in
`linebreak_decisions.csv`, and any of them can be overridden.

## Catchwords

Five pages end with a catchword, the old scribal habit of writing the next page's first
word at the foot of the current one, so the reader knows the leaves are in order:

| Letter | Page ends | Next page opens |
|---|---|---|
| 133 | `Con¬` | `Contract` |
| 140 | `Vor-` | `Vorwerk` |
| 168 | `Win¬` | `Winnickischen` |
| 177 | `be¬` | `benennung` |
| 235 | `ver-` | `verliehren` |

These are not broken words. Joining them would manufacture "ConContract". They are kept in
the diplomatic view, where they are part of the page, and dropped from the reading copy,
where they are not part of the text.

## Editorial marks

| Mark | Meaning |
|---|---|
| `¬` | The transcriber's word-continuation mark. Kept in the diplomatic view whether or not it turned out to be genuine, because the mark is itself evidence; the reading view acts on the verified decision. |
| `[?]` | The transcriber could not read the word at all. |
| `[word?]` | A guess at a word the transcriber found unclear. |
| `(missing)` / `(skipped)` | The archival number exists but no text survives under it. |
| `ſ` | The long s, as written in the original. |

There are **150** flagged uncertain readings across the corpus: 98 words nobody could read
at all, and 52 offered as guesses. They stay visible in the text of every document that has
them rather than being smoothed over. Five damaged passages await checking against the
originals.

## Dates

Roughly seven in eight documents carry a date in the letter itself. The rest are dated one
of four ways, and every document says which applies to it:

- **read from the letter**, the dateline as written
- **supplied by the researcher**, established from the original manuscripts
- **inferred from neighbouring letters**, bracketed by the letters on either side, with the
  reasoning recorded on the document
- **taken from its duplicate**, where one document survives in two copies

Eight documents remain undated and are collected at the end of chronological order.

Note that an archive's numbering is not necessarily chronological. In the correspondence,
letters 1 to 74 are a jumbled block spanning 1806 to 1815; 75 to 301 run in order from
1798, and numbers 302 and 303 sit outside that sequence. Both orders are navigable, and the
archival number is the stable citation key — unique within its holding, which is why the
holding is part of every document's address.

## Money

Sums are given in the Prussian system in use until 1821: **1 Reichsthaler = 24 Groschen;
1 Groschen = 12 Pfennig**, written here as `Rthl`, `g` and `d`. The corpus obeys these
limits exactly, which is what made it possible to resolve the many inconsistent
abbreviations in the original into a single notation without guesswork. The `d` for Pfennig
is not an error. It is the historical abbreviation for *denarius*, the same convention
behind British pre-decimal pence.

## Bundled and duplicated documents

Several archival numbers turned out to hold more than one document. These were split into
sub-records, letter 72 into 72a to 72f, letter 74 into 74a to 74e, and so on, each keeping
a link back to its parent. Nothing was removed in the process.

Some documents survive in two copies. In the correspondence, letters **48 and 302** are the
same letter of 7 March 1809 transcribed twice, as are 72d/72e (German and Polish) and
118b/118c. In the deeds, the Betsche hereditary-lease contract is here as **18 and 19**,
copied into the volume twice over — one of them without the royal consent and the archival
attestation that follow the other. The duplicate pairs are unusually valuable, because
comparing two independent transcriptions of one page reveals exactly where transcription
goes wrong, and both copies are presented unaltered.

## What is still unresolved

- One financial figure differs between the two copies of the 7 March 1809 letter (23,000
  against 32,000 Rthl). Both transcriptions are faithful to their own page, so the
  discrepancy belongs to the original copyist, not to this edition.
- Uncertain readings and damaged passages await checking against the originals; the count
  for each document is shown on its own page.
- Some identifications rest on context alone. The people pages state the evidence for each.

## English translations

Translations are being added document by document. Where one exists it appears beneath the
German with its status shown; where none exists yet, the German text is complete and fully
searchable in the meantime. No translation is presented as authoritative until it has been
checked by hand. A translation marked **draft** has been through the mechanical checks
described here but not yet read against the manuscript; **reviewed** means a person has
been through every query raised on it.

**The English shows a hole wherever the German has one.** This is deliberate, and it is the
main thing to understand about reading the translation. A translator, human or machine, can
turn almost any damaged sentence into smooth English, and smooth English gives a reader no
way to tell sound text from guesswork. So the marks of doubt cross over:

| In the German | In the English | Meaning |
|---|---|---|
| `[?]` | `[illegible]` | nothing legible in the manuscript |
| `[word?]` | `[uncertain: word]` | a reading offered, but uncertain |
| `[...]` | `[text lost]` | a gap, or a damaged page edge |

You may also find `[uncertain: …]` in the English where the German shows no mark at all.
That means the transcription reads as ordinary German but does not make sense in context, a
place where the manuscript was probably misread without anyone noticing. Those passages are
collected for checking against the original.

Where the translator could work out what the manuscript *probably* said, that suggestion is
deliberately kept out of the English and recorded separately. Correcting the transcription
is a different act from translating it, and it is done against the manuscript, not against
the sense of the sentence. Figures and proper names are reproduced exactly as transcribed,
never corrected in passing, even where they are plainly wrong. A silently improved figure
would destroy the evidence that it was ever wrong.
