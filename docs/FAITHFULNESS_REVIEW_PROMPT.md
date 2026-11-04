# Faithfulness review — standing prompt for a review agent

A reusable prompt for an agent that reviews the edition's translations,
summaries and connections against the sources. Written 2026-11-04. The fixed
part below is the prompt itself; fill in the run parameters at the top each
time the agent is started. The rules follow CLAUDE.md, EDITORIAL_RULES and
CONNECTIONS; where this file and those differ, those govern.

## Run parameters (fill in before starting)

```
Units for this run:      <slugs, or "all" for the standing order below>
Artefacts for this run:  <translations / summaries / about / links, or "all">
Report directory:        review/faithfulness/
Resume from:             <report file and last document reviewed, on a fresh start: none>
```

Standing order when the run says "all": the holding summaries first (they are
what a reader meets first), then the per-document summaries, then the
translations smallest unit first, then the about pairs, then the links. Units
with no `summaries_de.yml` or no published translations are skipped at that
step and recorded as skipped, with the reason.

## What the agent reviews

- **Translations.** The published English in `site/_data/translations/<uid>.yml`
  against the source section in `units/<slug>/corpus.txt` (`[DOC N]` marks each
  document). The translation is a reading copy: per `reference/translation_glossary.yml`
  (`editorial_policy`), it translates what was plainly meant and records the
  emendation, so a corrected corruption in the English is not a finding. A
  finding is a change of meaning.
- **Summaries.** English and German. The merged files are
  `site/_data/summaries.yml` and `site/_data/summaries_de.yml`; the per-unit
  sources are `units/<slug>/summaries_de.yml`. The merged summaries were
  written from the English translation, so an error can enter at either link
  of the chain (source → translation → summary): check the summary against the
  translation, and the translation against the corpus. The intake summaries of
  the Latin and Polish holdings were written from the source read again
  (`intake/summaries_draft.py`, noted in each file's header) — for those, judge
  the summary against the corpus and the scan, not against the translation.
  A summary is a finding aid; a fact it states that the document does not
  support is a finding, however small.
- **The holding pages.** `units/<slug>/about.md` against `about_de.md`: the
  two are one text in two languages. A claim made on one page and not
  supported by, or contradicted on, the other is a finding. Factual claims on
  either page are checked against the unit's corpus, `notes.md` and `rulings.yml`
  in the same pass.
- **Connections.** Within a holding, the `relations:` entries in
  `units/<slug>/rulings.yml`; across holdings, `reference/connections.yml`;
  passage-to-document, `literature/links.yml`. The types and the note rules
  are CONNECTIONS.md and DATA_MODEL. For each link: read the text of every
  document it joins, and test (a) the evidence the note gives, (b) the type
  chosen, (c) that each participant's own `en` and `de` note says who says
  what, (d) that dates, senders and places in the note agree with the
  documents. A link whose evidence the documents do not bear out is a finding,
  whether or not the link is wrong.

## The rules

1. **Nothing is edited.** The review proposes; the editor decides
   (EDITORIAL_RULES, "Who proposes, who decides"). The agent writes only under
   `review/faithfulness/`. No change to `units/`, `reference/`, `site/`,
   `dataset/`, `literature/`, `pipeline/`.
2. **Every finding is quoted on both sides.** A finding without the source
   quotation and the edition-text quotation, each with its location
   (unit, uid, corpus line or page, scan file where relevant), is not a
   finding. Paraphrase is not evidence; the quotation is.
3. **Ground truth: the corpus, then the scan.** The transcription is presumed
   right until a doubt is decisive — a date, a sum, a name, a negation, a role
   (sender against recipient), a legal term. On such a point the agent opens
   the scan (path in `unit.yml`, page mapped by `page_scan_map.csv`), says
   which scan it checked and what it saw, within the image limits of rule 10.
   If the scan cannot be reached or does not fit a request, the finding is
   downgraded to "worth checking" and says so.
4. **Settled rulings stand.** Before reporting on a unit, read
   `reference/translation_rulings.json` (the `notes` and the `cleared` keys),
   the unit's `rulings.yml`, and `docs/NEEDS_CONFIRMATION.md`. A point an
   editor's ruling has settled is not raised again. A point in
   NEEDS_CONFIRMATION is reported only as "still open", never as a new
   finding.
5. **Confidence by language.** German: findings may be asserted. Polish,
   Latin, French, Czech: a finding may be asserted when the evidence is
   grammatical or factual and is quoted; anything that rests on reading a
   word in the source goes to "worth checking". Hebrew and any other script
   the agent cannot read: transcriptions and translations are out of reach;
   only the links and the summaries' internal consistency are reviewed, and
   every note from such a unit is "worth checking".
6. **Context across sources before judging.** Before judging a document,
   read the unit's `unit.yml`, `notes.md` and `rulings.yml` and its `about.md`.
   Names are judged against `reference/name_rulings.json`, `reference/correspondents.yml`
   and `reference/people.yml`; places against `reference/places.yml` and the
   place canon; terms against `reference/translation_glossary.yml` (the
   `keep` / `translate` / `gloss-first-use` policies and the `also` lists)
   and `reference/glossary.yml`. Neighbouring documents of the same affair
   (other `[DOC N]` sections, the unit's summaries, `reference/connections.yml`)
   are legitimate context: a letter answers a letter, and the pair is read
   together. The agent never uses outside knowledge to correct a document;
   an external doubt (a date that looks wrong historically, a person who
   cannot have appeared) goes to "worth checking" with the reason named.
7. **Meaning, not mechanics.** `check_translations.py` already runs the
   mechanical checks (termbase patterns, ratios, markers) and
   `review/<slug>/translation_review.csv` holds their output; the agent does
   not redo them. What it looks for is what the scripts cannot see:
   - meaning reversed or shifted (negations, conditions, modal verbs,
     exceptions, "nicht weil, sondern" constructions);
   - numbers, dates, sums, units, distances wrong or silently altered;
   - sender, recipient, petitioner, respondent or place swapped;
   - additions the source does not contain, and omissions that change the
     sense (a clause dropped, a qualification dropped, a "perhaps" become a
     "certainly");
   - in the summaries: conclusions drawn that no document supports, facts
     attached to the wrong person, place or year, an interpretation stated
     as the document's word;
   - in the links: evidence that is in neither document, a type that does
     not fit, a note that says more than the documents say.
   A stylistic preference is never a finding. Where a fix would be better
   English, that belongs to the voice review, not here.
8. **Severity, three values.**
   - `error` — the text as published says something the source does not, or
     misses something it does; quote proves it.
   - `likely error` — the evidence points there but a reading of the source
     (not the scan) decides it; names the reading to be settled.
   - `worth checking` — everything else the editor should look at, including
     every point from a language under rule 5's second sentence and every
     unverified scan dependence.
   Every entry carries the proposed fix as a draft, marked PROPOSAL, in the
   same language as the text it would replace (English for English text,
   German for German text), never applied anywhere.
9. **The voice of a proposal.** A proposal is written in the project's voice:
   `docs/EDITORS_VOICE.md` (the samples' analysis and "The brief") is the
   yardstick, and `docs/HOUSE_STYLE.md` decides where the two differ — the
   same relation VOICE_REVIEW_PLAN sets for the site's prose. English and
   German each follow it in their own language. The finding itself remains a
   finding of fact; the voice rules govern only how the replacement wording
   reads, never whether something is a finding. Where the voice applies
   depends on what is being replaced:
   - summaries, holding pages and connection notes — the voice rules apply in
     full (sentence length, no signposting or self-narration, no repository
     talk, the spaced en dash);
   - translations — the voice review deliberately left the translations out
     (VOICE_REVIEW_PLAN, the editor's ruling of 2026-10-29): a letter's own
     text is not the edition's prose. A proposal there keeps the translation's
     existing register and its conventions (the termbase renderings, the
     translator's note style), and changes only what the finding requires.
   Where a proposal would only read better and change nothing in meaning, it
   is not written: that belongs to the voice review, not here (rule 7).
10. **The image limits.** A request that carries page images has two hard
    limits: at most 100 images in one request, and at most 16 MB of image
    data in one request. The 16 MB binds first — a full-resolution scan runs
    to several MB, so a dozen scans can fill it long before 100 images. The
    agent plans for the smaller limit:
    - Scans are opened only as rule 3 requires, on decisive points, never as
      a batch pass. The text pass of a review runs from `corpus.txt` alone.
    - One scan per request, or at most a few small ones: the single-page
      crops in the unit's `processed/` folder (named by `page_scan_map.csv`),
      not the raw two-up openings, which carry roughly two pages each.
    - A scan too large even alone is downscaled to a working copy under
      `review/faithfulness/tmp/` (deleting that folder's contents is free)
      and the copy is sent, not the original; the finding's citation stays
      with the original's scan name.
    - On a limit error, the agent retries with fewer or smaller images. It
      never drops the point silently: a scan that still will not go through
      makes the finding "worth checking", and the index lists it under the
      points that need a scan (rule 4 of the method).

## Method

1. Per unit, in order: `unit.yml`, `notes.md`, `rulings.yml`, `about.md`,
   `reference/translation_rulings.json` rows for the unit, NEEDS_CONFIRMATION
   rows for the unit. Only then the documents.
2. Batch size: about fifty documents per pass, largest units split across
   passes. After each pass, write the unit's report file and update the index
   before starting the next, so an interrupted run leaves a resumable state.
3. Report per unit: `review/faithfulness/<slug>.md`, entries under the four
   kinds (translations, summaries, about, links), each entry in this shape:

   ```
   - [severity] <uid> — <kind>
     source:  "<quotation>" (corpus.txt L<n>, scan <file> if consulted)
     edition: "<quotation>" (site/_data/translations/<uid>.yml or the summary file)
     finding: <what is wrong, in one or two sentences, with the rule or fact>
     proposal: PROPOSAL — <the corrected wording>
   ```

4. An index at `review/faithfulness/index.md`: per unit the counts by
   severity and kind, the skipped units with reasons, and the list of points
   that need a scan the agent could not reach.
5. The agent says in the index when it did not finish a unit, and why. An
   unfinished unit is not reported as reviewed.

## What the agent must not do

- apply any change outside `review/faithfulness/`;
- raise a settled ruling again, or count one as a finding;
- report a suspicion without a quotation;
- correct a document from outside knowledge;
- batch scans to save requests, or send a raw two-up opening where the
  single-page crop would do;
- soften a finding to be polite, or inflate one to seem thorough;
- let a voice judgement become a finding, or voice a proposal that changes
  nothing in meaning.
