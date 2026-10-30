# House style

For everything written *about* the documents: the site's prose, holding
descriptions, era essays, summaries, commit messages, these docs. Not for the
transcriptions, which are diplomatic and obey `EDITORIAL_RULES.md` instead.

Every rule here was made because the opposite was written first and had to be
taken out again. They are the editor's rulings, not suggestions.

---

## The governing question

**Would the reader need to know this?**

If the answer is no, it does not go in, however true it is. The commonest failure
on this project is not error but jargon and process where the reader needs plain
sense: how the pipeline works, what a holding is called internally, which file a
figure came from, why two copies let one settle the other. All of that is real
and none of it belongs in a sentence a reader meets on the way to a document.
Method goes in **About the edition** and on a holding's "How it was prepared"
tab, and only as much of it as a reader needs to judge the text (see "About the
edition" below).

```
NO   The documents set against the events that shaped them, from the
     partition of Poland to the Congress of Vienna.
NO   Documents from all of them are read together as one correspondence; the
     holding a document comes from is part of its citation, and part of its
     web address.
NO   The volume's own title page calls it Originalia et Copiae vidimatae, and
     much of it is exactly that.
```

The first says nothing and dates itself the moment a source outside those events
arrives. The second is about the software. The third explains the edition to
itself in a language the reader has not been taught.

## The reader has never encountered any of this

Not the estate, not the Hohenlohes, not the partitions of Poland. Introduce;
do not summarise. A name in a heading says who the person is.

**First mention takes "a", not "the".** "The ten-paragraph contract" claims the
reader has already met it. They have not. This holds in summaries, descriptions
and essays alike, and it is the single rule most often broken.

## No cryptic statements

The editor, 2026-10-03: "don't write cryptic statements". A sentence the
reader cannot follow without having read the letters is a failure, however
true it is. Before a sentence ships, ask of it:

- **Who?** Every person is named and placed ("Barbe, the court councillor in
  Hardenberg's chancery"), never "the man", "his", "the recurring figure".
- **What, exactly?** Not "nothing coming in" but what was owed, by whom, to
  whom. Not "the settlers cannot pay" but which settlers, and pay what.
- **Which office, which court?** "The chambers", "the government", "court
  administration", "attaches", "heads of agreement", "pledge" are explained or
  replaced by what they did.
- **Why does it matter here?** A bare event ("the estates' court still issues
  papers", "the Congress is thrown into suspension") says what it meant for
  Hohenlohe-Ingelfingen or the estates.
- **Proposed or done?** A proposal, a draft or a petition is not a result.

A short entry that leaves the reader asking is worse than a longer one that
does not. Where an entry cannot be made clear without a paragraph, it belongs
on the era page, and the timeline keeps the core of it.

## The documents first

The editor, 2026-10-20: "All facts must be first verified against
primary-source (ie. archival) documents before literature or other sources,
and if there's a discrepancy, then flag and record it." This holds for every
fact about the estates, their people and their places, wherever it is
written: a summary, a person's or place's entry, an era's name, ownership
line or account, the story, the timeline, a link's sentence, a holding's
notes, NEEDS_CONFIRMATION.

1. **Look in the edition's documents first.** Search the corpus
   (`dataset/documents/`, the transcription and the English) for the name,
   the year, the place, before taking anything from a book, the editor's
   notes from outside the edition, a reference work or a web page. A
   document often cites an older one the edition does not hold: the
   boundary decree of 1775 cites the rights granted the Hollanders in 1746,
   which are not themselves in the edition.
   Say which it is: what the document says, and what it says of an older
   paper.
2. **Where the documents say it, they are the source**, and the sentence
   rests on them. A book that says the same is a second witness, not the
   authority.
3. **Where no document says it**, a book or another source may supply it,
   and the sentence says whose account it is ("by Breyer's account"), never
   "it was".
4. **Where a document and another source disagree**, the edition takes the
   document's fact or date, without asking: the editor, 2026-10-21: "Always
   take the facts/dates from primary documents over literary sources, and
   flag when there's a discrepancy so that you know to take the primary
   source over a fact stated in a literary source." The difference is
   flagged and recorded, so that no later sitting takes the book's version,
   in the places that already exist for it:
   - `docs/NEEDS_CONFIRMATION.md`, in the section the matter belongs to (a
     book: "The literature"), as settled by this rule: what each says, with
     the page of the book and the document, and that the document is taken.
     Nothing is changed on the strength of the other source;
   - the work's `literature/<slug>/notes.md` ("Points for the reader"), or
     the holding's `notes.md` where the other source is not a book, so the
     record stays with the source;
   - on the site, where a link joins the passage and the document, its
     sentence says what each says and that the edition follows the document
     (`docs/WORKING_NOTES.md`, "A hand-made link says what each side
     says").
5. **Where two documents disagree**, neither is chosen without the editor;
   recorded the same way.
6. **A fact the editor gives** (a date of death, an identification) stands
   as their ruling. Where a document says otherwise, it is put to them the
   same way.
7. **A book's fact goes back to the source the book cites** (the editor,
   2026-10-28, on Chodyła): "For any facts coming from Chodyła, consult the
   primary source first, which should be taken before Chodyła. Cite the
   primary source wherever possible." Before a book's fact is proposed,
   follow its footnote: where the edition holds the document it names, read
   the document, take the fact from it and cite it, not the book; where the
   edition does not, cite the book and name the source it cites beside it,
   so that it can be brought in (`docs/MISSING_SOURCES.md`). Footnotes
   often cite a document the edition holds on a leaf it does not (Pyzdry
   Gr.115 has leaf 543, not 543v): check the leaf, not only the volume.

Examples, both of 2026-10-19 and 10-20: Żychliński (1891) has Maryanna
Dąmbska die on 2 September 1797, but the Prussian resident's dispatch from
Venice of 14 December 1796 already speaks of her death (I. HA GR, Rep. 7 C,
Nr. 1414, document 2); flagged in NEEDS_CONFIRMATION, the edition keeps to
the dispatch. Breyer (1935) has "Paul von Kolno-Prusiński" found Łazińsk
Holland in 1746; Claude wrote that "the edition has no document of 1746",
without searching it. The boundary decree of 1775 (Konin Gr.145, p. 76) is
the primary source for the privilege of 1746 (the editor, 2026-10-20), and
the summons of 1860 (APP 53/968/0/-/783) names who granted it. The fact
rests on them; Breyer is the second witness.

## Descriptions stand alone

A holding's description is read on its own, in a list, by someone who has seen
nothing else. It cannot lean on the line above it or on another holding.

```
NO   Not correspondence but title deeds.
NO   The main correspondence file.
```

Both are answers to a question the reader did not ask, and both go dead the
moment they are read anywhere but next to each other. Write what the thing **is**.

And write it so it survives the next source. A description that is true only
while the project holds what it holds today will have to be rewritten, and will
instead quietly go stale.

## A holding's own page

Each holding has a page with a full description (`units/<slug>/about.md`) and
a short account of how it was prepared (the `prepared:` block of its unit.yml,
from the sentences of `reference/prepared.yml`). Both are read by someone
meeting the holding for the first time (editor, 2026-10-01):

- The description reads like an archive's own description of a holding
  (creator and dates, historical background, contents, related holdings): impersonal, matter of fact, academic. No narrative
  devices and no verdicts ("Every attempt failed", "it was damning").
  Headings name the section plainly ("Contents"), not the story ("Three
  attempts"). The editor ruled this on 2026-10-01 after a first, storytelling
  draft.
- Every person, estate and office is identified where it first appears.
  A person is introduced once in full and then called by name: **Prince
  Friedrich Ludwig of Hohenlohe-Ingelfingen**, thereafter
  **Hohenlohe-Ingelfingen**. Not "a Prince", not "the Prince".
- Length follows the holding. A single deed takes a few paragraphs; several
  hundred letters take several thousand words, under headings.
- Each statement cites the documents it rests on, and says what is not known.
- Method belongs in the "How it was prepared" tab and in **About the edition**, not in the
  description. It is told plainly and briefly: what was done, who decided,
  what is still uncertain. No tool names, no costs.
  The editor, 2026-10-30, of the "How it was prepared" tabs: method stays
  there, but no file names or paths, no script names or flags, no page ids
  (`0543_a`), no NEEDS_CONFIRMATION, no "spot sheet" or its address, and no
  dated citations of a ruling ("(the editor, 2026-10-14)"). Say who decided
  in the sentence ("at the editor's word", "the editor ruled on 26 October
  2026"); call the model Claude, not "the session"; an open question is "still
  open", not "put to the editor"; a translation made in session is "written
  in a working session under the same rules as the other holdings".

**What the tab tells (the editor, 2026-10-30).** The point of "How it was
prepared" is to tell the reader about the AI decisions that affected the text,
as an editor would explain their handling of it, not every detail of the work.
It answers four questions: who made the transcription; how much was checked,
and by whom; what Claude changed or supplied that the source does not contain
(corrections and their rule, standardised names, a passage transcribed or
translated that the editor's text lacked); who translated, and how the
summaries were checked. Everything that matters only to the editor stays in the
holding's `notes.md`: the handling of the images (counts, cropping, folds,
watermarks), counts of corrections and marks of doubt, the editor's spot
sheets and checks of samples, decisions that were reversed ("an earlier reading
was dropped"), additions from the scan, open points and "still to do", and
whatever the page already shows (that each letter is one document, the label
on an office note, that a text is set by paragraph). The tab is written from
`prepared:` in unit.yml so that it stays short and the German is written from
the same keys.

**No physical description for its own sake (the editor, 2026-10-30).** A
holding's description has no "Form and language" section: the hand, the ruling,
the leaf numbers, the film frames and the abbreviations are not told, and the
languages are one line in the header. What changes how a document is read is
kept, under "Contents": the basis of a date, a part that is not transcribed,
which sheet is the original and which the copy, a spelling the copyist kept.
The same test applies to every page: say what the reader needs to understand
the source, not what it looks like.

## The era essay

An era's page (`site/hohenlohe.md`) is the one place where the edition tells a
story: what happened, in order, with the documents quoted and linked (editor,
2026-10-02). Metaphor is kept to a minimum, and every statement is a fact the
documents give or a fact of standard history, said plainly. No verdicts and no
flourishes; inference is marked as inference.

```
NO   The relationship curdles.
NO   One woman, and she wins.
NO   A river decides everything.
```

What goes in, the sections and the sources each rests on are in
`docs/HOHENLOHE_ERA_PLAN.md`.

## About the edition

The About page (`site/reading-this-edition.md`, German `site/de/ueber-diese-edition.md`)
is written for a reader or researcher who wants to know what the edition is and
how far to trust it. The editor, 2026-10-05, of a version three times as long: "way
too dense and includes information not relevant to the reader. It feels like
you're treating it as your own memory for the project."

It answers, in this order: what the edition contains; where the documents are
held; how the text was made and how far it can be relied on; how to read a
document page and its marks; what the translations and summaries are; dates,
names and money; how documents are numbered and grouped; what is still open;
where to find how to cite.

It leaves out everything that is the project's own record: counts of line-break
marks and how each was decided, the reference data and thresholds used, file
names and paths, image sizes, what fails the build, the per-holding figures, and
single unresolved readings. Those belong on the holding's "How it was prepared"
tab, in the holding's notes, or in `docs/`.

```
NO   A form counts as a real word at a thousand corpus hits or more; below that,
     what comes back is proper-name noise.
NO   Every decision is recorded with its evidence in linebreak_decisions.csv.
NO   The images published here are downscaled to 1100 pixels wide.
```

**How the edition describes who made the text** (the editor, 2026-10-06, correcting "The
transcription was not made by a trained palaeographer"): the editor is an
amateur palaeographer, and that is the phrase to use (their word; they asked
for it in place of "has transcribed this handwriting for some years"). The
work is supported by AI.
Do not write, on this page or a holding's, that the text was "not made by a
trained reader". Say what was done: a machine reading, corrected; a language
model that weighs context removes many character errors and not all; some
inaccuracy always remains, which the editor has accepted for this project
because of the number of documents; and anything taken from the texts for
academic work should first be checked against the original document.

**The English translations are not called drafts, and no page says they have not
been checked** (the editor, 2026-10-06: "I don't think we need to mark the English
translations as drafts, and we don't need to mention that they haven't been
checked"). This holds for the About page, the document pages (which no longer
show a translation's status), the rights page and every holding's "How it was
prepared" text: do not end one with "The English has not yet been read against
the scans". The pages say that the translations were made by an AI model, and
that anything taken for academic work should be checked against the original.
The `status:` field in `site/_data/translations/` stays; it is the pipeline's.
The same for the Glossary (the editor, 2026-10-06): its definitions are not
called drafts. Each entry names the reference work it was checked against, or
is still to be checked against, and that is all.

Few figures, because each is counted by hand: holdings, documents, pages,
documents by language, translations, marks of doubt. A mark or a view is
described as the reader meets it on the page, so check the page before
describing it: the old text explained a line-end mark that the page no longer
shows, and a fourth view that is not a view.

## Concision

Do not over-describe. Cut the sentence that counts and classifies what the next
sentence is about to say.

```
NO   twelve documents, all correspondence
```

## No signposting

The editor, 2026-10-20: identify signposting and avoid it, "unless a topic
is being reintroduced that the reader hasn't come across for a long
time". A signpost is a sentence about the text instead of about the past:
it announces, points back or lists topics, and tells the reader nothing.

**How to spot one.** The subject of the sentence is the text, the page,
the book, the writer or the reader, not a person, a place or an event;
or its verb is one of presenting, examining, discussing, giving attention
to. Take it out and no fact is lost.

```
NO   This section examines the boundary dispute between Trąbczyn and Łukom.
NO   Close attention is given to the events of the 18th century.
NO   The characteristics of Olęder settlements have also been examined,
     including their legal, religious, and social structures.
NO   As mentioned above, Chełmski ...
NO   It is worth noting that ...
```

**What to do instead.** Begin with the first fact. A list of topics
becomes the topics themselves, each with one thing the documents say.

**The exception: a topic the reader has not met for a long time.** It is
brought back, and it is brought back by restating the fact, not by
pointing at an earlier page: "Stanisław Chełmski, the owner of Łukom who
had been given possession of the Lusnia wood and its Olęder settlers in
November 1771, ..." and not "As mentioned earlier, Chełmski ...". The
reminder is useful to a reader who has forgotten and costs nothing to one
who has not. (The editor's exception; the form of
it is Claude's suggestion, 2026-10-20.)

**Not signposts:** text whose task is to say where things are, such as
the About page's guide to a document page, a holding's "How it was
prepared", a list of contents, or a book's plan in its preface. These
are kept short and stay where they are (Claude's suggestion,
2026-10-20, for the editor to confirm).

When this rule was made, a search of the site's English prose (the
story, the era page, the About page, the holdings' descriptions and
accounts of preparation, the era blurbs, the timeline, the summaries,
the interface strings and the literature's links) found no signposts:
23 matches, every one a false alarm ("addressed to", "the witnesses are
examined"). The rule guards what is written next.

## No method talk

The editor, 2026-10-23, of their own index of places: "note that I never
explain to the reader what I'm doing or how (like this project tends to
over-do)". A page about a place, a person, a document or a work begins
with the facts. It has no sentence on what the page gathers, how it was
made, what was read or compared, or which rule it follows; its sources are
in its footnotes and links, and its doubts in a "possibly" or a "likely"
where the fact stands.

```
NO   The page gathers what the place tells about itself, beside what the
     edition's documents tell about it.          (Zagórów's page, 2026-10-22)
NO   Where a source and the documents differ, the documents stand.
```

Method has two places, and only there is it told: the About page and a
holding's "How it was prepared" (above, "A holding's own page" and "About
the edition"). The project's record goes in `docs/` and the notes. A
reading of the site's existing pages for method talk is offered to the
editor (`docs/TODO.md`), not yet done.

## No self-narrating standfirsts

The editor, 2026-10-28: the pages do not describe themselves. A section
opens with its heading and then its content - no prose between them that
says what the page contains, however true. The reference the editor gave
for the wanted style (a Sway page) renders headings, lists and images,
and nothing speaking between them.

A self-narrating standfirst is the site talking to itself. Its four
marks, each from an example the editor struck out:

1. **Self-reference.** The text talks about the page, not the world:
   "Every place the edition records, each with its own page."
2. **Redundancy.** It restates what the heading and the list beneath
   already demonstrate: "how often the documents name each person, and
   in which documents."
3. **Explaining the obvious.** It narrates structure or interaction:
   "each with its own page", "tap one to see what it means."
4. **A designed literary voice.** Dash-appended appositions and
   rhetorical triads: "its villages, hamlets and colonies, the market
   towns and seats around them."

```
NO   Everyone named often enough to follow from one document to the next:
     how often the documents name each person, and in which documents.
NO   Words in the documents that a reader today cannot be expected to
     know: money and measures, the law of land and estates, offices and
     forms of address, and the events the letters take for granted. In
     the documents these words are faintly underlined; tap one to see
     what it means.
NO   The ten Evangelical cemeteries of the area and its neighbourhood,
     visited and their headstones read in 2023 — the editor's own
     survey, shown here with the places they belong to.
```

It is "No signposting" and "No method talk" carried to the page openers
and the interface strings - the subject of the sentence is the page and
what it gathers, not a person, place, event or document. A standfirst
stands only where it carries what the page cannot show: how the site is
used, or where its material comes from.

```
YES  All %d documents. Search the full German text, or narrow by year,
     person, place and condition.     (the search runs on the German)
YES  Every place of the neighbourhood, whether or not it is named in the
     documents.    (the tier carries names no document explains)
```

Descriptions of the material itself - a holding's archive description,
the story's opening, an era's note - are content, not narration, and do
not fall under this rule. A translation's or an origin's caveat is a
disclosure and stands too.

The same holds for the helper text of a document's page (the editor,
2026-10-29): no sentence under the tabs saying what a view is ("One line per
manuscript line, with broken words hyphenated..."), no note that a page is
transcribed by paragraph, no "no page image" notice, no filename under a scan.
A page's layout shows it: a paragraph transcription is set without line
numbers, a page with no image has no image pane. What stays is a disclosure
that is short ("English translation by Claude, an AI model, not checked
against the original as a whole.", "Not yet translated.").

**No relevance talk** (the editor, 2026-10-29): a page does not explain why
a work or an item is on the site, or that it does not name Trąbczyn. That
reasoning is the project's and stands in the work's or item's `notes.md`,
"Why it is here". EDITORS_VOICE, "The editor's rulings on the pilot".

**The site does not call itself "the edition"** (the editor, 2026-10-29): a
reader does not need to know that the site is an edition, and "the edition holds
her letters", "the edition follows the documents" and "in the edition" are the
site explaining itself. Where such a sentence only says what the site holds or
how it decides, it is cut; where it carries a fact, the fact stays and the
phrase goes ("The edition has the decree of the commission" becomes "The decree
of the commission"). The About page is "About", the footer says what the site
holds, the list label is "In the documents". "Edition" stays only where a real
published edition is meant: the printed Kodeks, a source edition, a book's
second edition. The word may stand in comments and notes, not on a page.

The removal made under this rule (the whole family, both languages),
with what stood and what went, is recorded in
`docs/STANDFIRSTS_PLAN.md`. The German texts obey the same rule as the
English: a ruling on one is a ruling on both.

## The maker is not named

The editor, 2026-10-28: "Don't mention anything about an 'editor' - this
is you talking about me, which is not what should appear on the site.
The site is for other people to experience the materials." The site
speaks only to its reader about the materials. No page text, label or
note names the person who made them: provenance says what was done
("visited and their headstones read in 2023"), and where a maker must be
named for the reader's sake, the work is named and its limits stated,
not the person by it.

Found standing under the rule, left for the editor's ruling:
`np_caveat_editor` ("The English translation is the editor's own.", with
its German twin), and the cemetery pages' "From the editor's survey of
the Evangelical cemeteries" openings (`cemeteries/*/notes.md`). The
ruling that stood them (2026-10-28) is in the changelog;
`docs/STANDFIRSTS_PLAN.md` lists them.

## English

Everything into English unless there truly is no equivalent. A *Kriegs- und
Forstrath* is a Councillor of War and Forests. No Latin the reader has not been
given, and no term that has to be looked up: an instrument is **issued** or
**made out**, never *engrossed*; a copy checked against the original is
**certified**, never *vidimated*; a judgement is **set aside**, not *cassated*.

Where a term genuinely has no plain equivalent and the document turns on it, use
it and say in three words what it means.

Currency and measure stay: Rthl, Groschen, Hufe, Morgen.

## Names

The prince is **Prince Friedrich Ludwig of Hohenlohe-Ingelfingen**, and
thereafter **the Prince of Hohenlohe-Ingelfingen**. Never *Fürst*, never *zu*,
never *von*. The particle points at a territory, so it is translated. This is
not a general rule about *von*: von Triebenfeld is a surname and stays, 175 times
over.

A bare surname takes no article. **Honrichs**, not *the Honrichs*.

Spellings are settled once, in `reference/people.yml` and `reference/places.yml`,
and the termbase generates the table from them. A spelling decided anywhere else
is not decided.

## Typography

No em dashes in English prose. Where a dash sets off an aside or an
explanation, it is the **spaced en dash** ( – ), never the em dash (—)
and never a hyphen ( - ) standing in for one (the editor, 2026-10-20:
"Let's use the spaced en dash as a rule"). It is used where it helps
the sentence; a comma, a colon, a semicolon or a full stop still does
the work where it can. Until 2026-10-20 the rule was no dashes at all,
so the prose written before then has none. A range between two figures
takes an **unspaced en dash**: 8,000–9,000 Rthl, 1771–1782 (the editor,
2026-10-20: "Short dash with no spaces is fine for number ranges").
Ranges written before then have a hyphen (8,000-9,000).

The German pages keep the spaced Gedankenstrich, which is the same mark
( – ) and correct German typography.

Straight quotes. Sentence case in headings, not Title Case.

## Before it ships

Run the `humanizer` skill over finished prose.

---

## Where a ruling goes

A style ruling written into one prompt holds in one place and drifts everywhere
else. "Engrossed" was banned for the translator and reached the summaries anyway;
so did "the Honrichs", after the editor had ruled against it.

So:

| The ruling is about | It goes in |
|---|---|
| a word the English must not use | `reference/translation_glossary.yml`, under `forbidden_renders` |
| how a name is spelled | `reference/people.yml` / `places.yml`, which generate the table |
| a term's English | `translation_glossary.yml`, in the section that fits |
| how prose is written | this file |

`translate.py` and `summarise.py` both read the termbase, so a row added there
holds in both. Nothing reads this file but a person, which is why the rules that
can be mechanised should not be left in it.
