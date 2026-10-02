# Plan: a glossary page, and definitions in the documents

Status: **first batch built** (2026-10-02): 61 entries, all drafts to be
checked against the works named; the in-text definitions, on by default; the
glossary page; the candidate script and the row in `NEW_UNIT.md` §8. Not yet
built: the pipeline check that reports a holding whose candidates are
unruled (§5). Decided: on by default; people and places left out; a first
batch of the most frequent terms across all kinds. When the work is done, the standing parts of this plan move into
`DATA_MODEL.md`, `NEW_UNIT.md` and `HOUSE_STYLE.md`, and this file becomes a
record of how it was decided.

The aim: a reader who is interested in the subject but not an expert meets a
word in a document they cannot be expected to know. It is faintly underlined;
a tap opens a short definition; the glossary page lists every entry.

---

## 1. Which words qualify

The test is the house style's own: **would the reader stop here and not know
what is meant?** Six kinds qualify.

| Kind | Examples from the corpus | Why |
|---|---|---|
| Money, measures, land | Rthl (137 documents), Courant, Groschen, Morgen, Hufe, Scheffel | Units nobody uses now |
| Land and tenure | Vorwerk, Erbpacht, Erbzins, Canon, Propination, allodial, Majorat | The estate business the letters are about |
| Law and administration | Sequestration, Vollmacht, Hypothekenschein, Kammer, Kriegs- und Domänenrat, Starost, Prefect, Auditeur, Rendant, Mandatarius | Prussian, Polish and Napoleonic institutions |
| False friends | Execution (court enforcement), Resignation (conveying title), Interessen (interest on money), Confirmation, Indult | The reader *thinks* they understand. The most valuable kind |
| Latin, French, Polish | Notarius publicus, pretium, ad acta, in fidem; starosta, wójt, sołtys | Set phrases and offices left in the original |
| Events and states | South Prussia (262 mentions in the English), Duchy of Warsaw, Peace of Tilsit, Congress of Vienna, the Kościuszko uprising | Need a paragraph, not a line |

**Left out:**

- **Period spelling** (*gethan*, *Güther*, *kömt*): the reading view deals with it.
- **People and places:** they have their own register pages.
- **A word the sentence explains:** if its meaning is plain from the sentence
  around it, it does not need an entry.

**Finding the candidates.** Four sources, merged into one sheet,
`review/glossary_candidates.csv`:

1. The translation termbase, `reference/translation_glossary.yml`: 89 terms,
   58 already with a short gloss, plus currencies, forms of address and
   Latin.
2. Words frequent in the letters but rare in modern German, from
   `reference/dwds_cache.json`. It flags period spelling as readily as real
   obscurity, so every row needs judgement.
3. Offices and titles from `reference/people.yml`.
4. The events in `site/_data/timeline.yml`.

Each row gives the number of documents the word appears in, a sample line,
and a recommendation: include, maybe, or no. **The editor rules on the
sheet.** Expect roughly 250 candidates and 120–180 entries; a first batch of
the 60 most frequent covers most of what a reader meets.

## 2. The data: one concept, two languages

A new hand-written file, `reference/glossary.yml`. It is kept apart from the
translation termbase, which is written for the translator and carries
instructions a reader should never see, but it is seeded from it: the
termbase already pairs a German pattern with its English rendering.

```yaml
- id: vorwerk
  kind: land                       # money | land | law | title | phrase | event
  lang: de                         # the original's language: de, la, fr, pl
  head_de: Vorwerk
  head_en: demesne farm
  match_de: '\bVorwer(k|ck)\w*'    # where it is underlined in the German
  match_en: '\bdemesne farms?\b'   # where it is underlined in the English
  short_en: An outlying farm of a manor, worked for the lord …
  short_de: Ein Wirtschaftshof eines Gutes …
  long_en: …                       # events only: a paragraph
  long_de: …
  source: Krünitz, Oekonomische Encyklopädie, s.v. Vorwerk
  timeline: tilsit-1807            # optional: a timeline event, a place, a person
```

- **The definition follows the interface language, not the text's.** On the
  German interface, reading the English translation, the reader gets the
  German definition.
- **English and German are written separately,** each for its own reader,
  not translated one from the other.

### Sources for the definitions

Every entry names its source. Prefer works of the period, which define a word
as the letters' writers used it:

| For | Source |
|---|---|
| German words, general | Adelung, *Grammatisch-kritisches Wörterbuch der Hochdeutschen Mundart* (1793–1801); Grimm, *Deutsches Wörterbuch* |
| Economy, land, measures, money | Krünitz, *Oekonomische Encyklopädie* (1773–1858) |
| Prussian law and offices | *Allgemeines Landrecht für die Preußischen Staaten* (1794) |
| **Polish terms and institutions** | **Zygmunt Gloger, *Encyklopedia staropolska ilustrowana* (1900–1903)**, [on Polish Wikisource](https://pl.wikisource.org/wiki/Encyklopedia_staropolska). For starosta, wójt, sołtys, olędrzy, propinacja, łan and the like, and for every Polish term the later eras bring |
| Events | The timeline's own cited sources; standard histories |

The cloud environment used so far cannot reach Wikisource (its network policy
refuses the host). Either the host is added to the environment's allowed
domains, or entries citing Gloger are drafted where it can be reached.

## 3. In the documents

**Matching is done at build time.** A build step finds each entry's matches
in every document, per view (transcription, reading text, English) and in the
summary at the head of the page, and writes:

- a short list per document, carried in the page, of which term falls at which
  line and position; a small script wraps those words when the page opens;
- `review/glossary_matches.csv`, every match with its line, so a wrong one
  (*Gold* inside a name, say) is ruled out once, in `reference/glossary.yml`.

The German in the built HTML stays exactly as it is, so `verify_site.py`'s
character-exact check is untouched.

**What is marked:**

- **Once per term per manuscript page,** not every time: the mock-up of
  letter 48 shows *Vollmacht* three times in ten lines, which is already noise.
- **Not inside a word split across two lines,** and not inside a `[?]` doubtful
  reading.
- **A faint dotted underline** in the accent colour. It turns solid, with a
  light tint, while its box is open.

**The box:**

- **Desktop:** opens under the word, kept inside the screen edges.
- **Phone:** a sheet that rises from the bottom of the screen, full width, at
  most 60% of its height. It has a drag handle, a large close button, and it
  closes when you tap outside it or press Esc. The text stays visible above
  it, so the reader keeps their place.
- **Contents:** the headword, its original language ("German, from Latin"), two
  or three sentences, and links "In the glossary →" and, for events, "On the
  timeline →".
- **Accessibility:** each term is a real button: reachable with Tab, opened
  with Enter, announced by screen readers.

**A switch,** "Glossary terms", in the view bar beside Transcription / Reading
/ English, remembered in the browser. That is a fourth stored preference, so
the privacy section of `/rights/` and `/de/rechte/` gains a sentence.

The "hide scans" checkbox currently crowds the view description on a phone; it
is fixed in the same change, since the switch joins that bar.

## 4. The glossary page

`/glossary/` and `/de/glossar/`, linked from the main navigation; on a phone
it fits on the menu's second row.

- **English page:** headwords in English, with the original and its language
  beside them: *demesne farm*, German *Vorwerk*; *Notarius publicus*, Latin.
  Sorted A–Z by the English headword; the search also finds the original.
- **German page:** headwords and definitions in German.
- **Finding an entry:** a search box that filters as you type, in both
  languages; filter buttons by kind; an A–Z bar, which on a phone becomes one
  row scrolled sideways and stays at the top of the screen.
- **Each entry:** the definition, the longer text for an event, its source,
  and "Appears in 36 documents", linking to the document list filtered to
  them. Each has its own address (`/glossary/#vorwerk`), which is where "In the
  glossary →" leads.
- **Without JavaScript** the page is a complete, readable list.

## 5. Keeping it up to date: part of every new holding

A glossary that is right only for the holdings it was built with goes quietly
stale: a new holding brings new words, and an existing entry's pattern can
start matching something it should not. So it becomes part of the workflow in
`docs/NEW_UNIT.md`, not a separate chore.

- **A row in `NEW_UNIT.md` §8,** "What the holding owes the rest of the site":

  | What the reader sees | File | Note |
  |---|---|---|
  | Glossary: definitions in the text and on the glossary page | `reference/glossary.yml` | Run `glossary_candidates.py --unit <slug>`; rule on its sheet; add entries in English and German, each with its source. Gloger for Polish terms. |

- **A check that cannot be skipped by forgetting.** `glossary_candidates.py
  --unit <slug>` lists the words in the new holding that would qualify and have
  no entry and no recorded "no". The pipeline check reports a published holding
  whose candidates have not been ruled on, the way `check_unit_text.py` holds a
  holding's figures to its documents.
- **Rulings are kept.** A word ruled "no" is recorded with its reason
  (`reference/glossary.yml`, `excluded:`), so the next holding does not ask the
  same question again.
- **Existing entries are re-checked.** The match sheet is regenerated for the
  new holding, and its new matches are read for false hits before publishing.
- **Counts stay true by themselves.** "Appears in N documents" is computed by
  the build, never written by hand.
- **New languages.** A holding in Polish, or a later era with its own
  vocabulary (the boundary dispute, the restitution), extends the same file;
  for Polish, Gloger first.

## 6. Order of work

1. The candidate sheet, for the editor to rule on. No API cost.
2. `reference/glossary.yml`, the build step and the match sheet, with the first
   60 entries.
3. The feature on the document pages, tested at phone and desktop width in a
   real browser.
4. The glossary page.
5. The new-holding workflow: the `NEW_UNIT.md` row, `glossary_candidates.py
   --unit`, and the pipeline check.
6. The remaining entries, in batches.

## Decisions (editor, 2026-10-02)

1. **Underlining is on by default**; a reader can turn it off, and the choice
   is remembered.
2. **People and places are left out** of the in-text definitions.
3. **The first batch** is the most frequent terms across all kinds.

## As built, where it differs from the plan above

- Formulaic terms met on nearly every page (Durchlaucht, the money units, the
  forms of address, the closing formula) are marked once per document, not
  once per page: `per: document` in the entry.
- A marked word is a `<span role="button">`, not a `<button>`: a button is laid
  out as an inline box, took the paragraph's first-line indent and could not
  break across lines.
- `lang` has `de_la` and `de_fr` for German words taken from Latin or French
  (Sequestration, Revers), labelled "German, from Latin"; plain `la` is Latin
  written as Latin (Dominium, Pro Memoria).
- Patterns can mark part of a match (a group named `w`), so Michaelis is
  marked only as a date and Morgen only as a measure.

### Second batch (2026-10-02): 30 more, 91 in all

The first batch came from the translation termbase, which has no entries for
abbreviations or Latin, so Fr. d'or (19 documents) was never offered. Added:
Friedrich d'or; rod, Centner, cord, bushel; donation, Taxe, Competenz,
appurtenances, entry money, fief, allodial; Regierung (before 1808 a court,
not a government: a false friend the English repeats in 60 documents),
Decret, Departement, Gouvernement, Tribunal, cabinet order, Landrath,
cession, Oberlandesgericht, Kammergericht, peace court, Auditeur; pp., geruhen,
L. S., Actum, in fidem, de dato and vigore.

`glossary_candidates.py` now probes for abbreviations (a short word that keeps
its full stop at least 60% of the time; a unit that follows a figure at least
half the time) and Latin (a Latin preposition before a Latin ending; a word
with a distinctively Latin ending), so the next holding is offered them.

### The English: house forms

Building the glossary showed that the English carried the German money
abbreviations in a dozen forms (rt, rtl, rttl, rthlr, gg, ggr, g., gl., pf.,
d., fl., x, Fr. d'or), which the glossary, marking full forms, could not
explain. `reference/english_forms.yml` holds the mechanical replacements, and
`pipeline/translate/english_forms.py` applies them: the thaler to the
termbase's Rthl, the rest written out (Groschen, Pfennig, gulden, kreuzer,
Friedrich d'or). publish_translations.py and summarise.py apply them as they
write, so a re-publish from the cache keeps them; `--apply` brought the
published files into line (186 translations, 32 summaries; about 1,400
replacements). No model call: nothing was re-translated.
