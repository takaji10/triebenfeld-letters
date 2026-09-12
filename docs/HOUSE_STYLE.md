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
Method goes in **About the edition**, and nowhere else.

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
