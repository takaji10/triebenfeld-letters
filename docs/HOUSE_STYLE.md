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
an account of how it was prepared (`process.md`). Both are read by someone
meeting the holding for the first time (editor, 2026-10-01):

- The description reads like an archive's own description of a holding
  (creator and dates, historical background, contents, form and language,
  related holdings): impersonal, matter of fact, academic. No narrative
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
- Method belongs in `process.md` and in **About the edition**, not in the
  description. It is told plainly and briefly: what was done, who decided,
  what is still uncertain. No tool names, no costs.

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

No em dashes and no en dashes in English prose. A comma, a colon, a semicolon or
a full stop does the work. A dash between two figures is a range and is correct:
8,000-9,000 Rthl.

This rule is **English only**. The spaced Gedankenstrich is correct German
typography and stays in the German pages.

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
