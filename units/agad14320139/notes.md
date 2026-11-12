# AGAD 1/432/0/1/139 (scans 128-130): Pastor Erdmann's reports of 1882

Added 2026-11-11 (slug `agad14320139`, era `wlodzimierz`, both approved by the
editor). **Not published.** Plan and rules: `docs/CONSISTORY_1882_PLAN.md`.

## What it is

Two documents (the editor's word), each of two written sides, in German:
1. the annual report for 1882 of Pastor E. Erdmann on the parish of **Zagórów**
   (pages 0318_a and 0322_a), 2. his report on the filial **Lissewo-Pyzdry**
   (0322_b and 0345_a). Both answer the order of the Warsaw consistory of
   30 October, No. 267, and follow its form (I Kirchenwesen a/b, II
   Merkwürdige Ereignisse, III Zahl der Confirmirten, IV Candidaten, V
   Collekten). The archive's title (the editor, 2026-11-11): "Opis sytuacji w
   gminach ewangelicko-augsburskich w 1882 roku - parafoe Chodecz, Sierpc,
   Zagórów, Prażuchy, Grodziec, Sejny, Duża Paproć, Mariampol, Łomża, Godlewo,
   Lipno, Przasnysz, Lipiny, Mława, Pułtusk, Sompolno, Aleksandrów,
   Sobiesęki]." Fond: Konsystorz Kościoła Ewangelicko-Augsburskiego w
   Warszawie (about 30 % of its archive survives). The editor's original
   scans are three (archive numbers 111110318, 111110322, 111110345; leaf 0322
   carries the end of document 1 on one side and the opening of document 2
   on the other, cut into `_a` and `_b`).

## The damage

The leaves were rescued from a fire. On the first page of each report the
ends of the lines are burnt away (1-3 words per line), on the second the
beginnings; top lines are worst. Every lost stretch is `[...]` in the
transcription and nothing is completed there. The four sample scans the
editor supplied (`samples/`, Włocławek and Konstantynów, other parishes of the
same file) are better kept and show the consistory's form (docs/CONSISTORY_1882_PLAN.md,
section 4a); they were used for the form's headings only, never for words or
figures of Erdmann's.

## How it was made

- **Transcription.** Two Opus sub-agents read the two documents from the page
  images (bands cut at 1.3 x), one each; a third, independent Opus pass read
  all four pages before seeing the first readings and wrote
  `intake/second_reading.md` (30 disagreements). Applied where the standard
  allows (a fixed formula, the same word whole elsewhere, a letterform the
  second reader could name): **häusliche** (0322_a, not "kirchliche", as the form
  and the twin ask), "bei den Mis-…diensten" (0345_a), "Michalinowo",
  "werden" (no bow over the vowel), "[Religi?]" for the first reader's
  "Kateg[?]", "[unbewußt?]" for 0318_a l. 29, "fast" for "sich" (0322_a l. 2);
  the communicants' figures corrected by me from the image after the first
  reader cut three digits (726, 871, 1597; the 6 under an ink blot stays
  `72[6?]`). The line counts match the manuscript on all four pages.
  `intake/reading_doc1.md`, `reading_doc2.md` are the first readers' notes.
- **Line breaks and paragraphs.** Every hyphen at a line end whose next line
  opens on a burnt edge is `split` (`linebreak_decisions.csv`, ruled): the
  halves are not joined across a gap. Paragraphs break at the form's headings
  (rows with cue `hand` in `paragraph_decisions.csv`, which survive a rebuild).
- **The lacunae.** `intake/lacunae_build.py` makes `intake/lacunae.csv` (86
  stretches, each with its best twin line); an Opus agent graded them A 13, B 31,
  C 28, D 14, I demoted one A (0322_a l. 18, "sind": a lost digit before
  "4 Rubel" cannot be ruled out) so **A 12, B 31 (43 shown), C 29, D 14**.
  `supplied.yml` holds the A and B rows only; the site shows them in a
  collapsed panel under each page's text (`supplied_html()` in
  `pipeline/build/build_site_data.py`), never in the transcription, the
  translation or the summaries. Almost every B is a word broken at a line end
  whose beginning and ending are both legible and whose whole word stands
  elsewhere in the four pages; the A rows are formulas whole in the other report.
- **English.** Written by Claude in session (no paid run), `intake/translation/
  build_docs.py` -> `doc1.yml`, `doc2.yml` -> `write_cache.py`; every `[...]`
  is `[text lost]`, marker counts equal the German on every page. A broken word
  is kept as written.
- **Summaries** (`intake/write_summaries.py`, both languages): written from
  what is legible; statements resting on a lost stretch left out (the "vices"
  and "conversions" lines of document 1). Claim check: `intake/claim_check.yml`.
- **Glossary gate** passes (no new entry needed).

## Open readings (for the editor, against the scans)

1. 0322_a l. 1: "für [Verlangen?] noch mehr Schulen" and l. 2 "[...] nicht[?]
   vorhanden" - is it "nicht" (the first reader), or "diese"? A negation:
   the English says "not[?]".
2. 0318_a l. 30: the **6** of "72[6?]"; 0322_a l. 18 the stroke before "4 Rubel
   61" (a dash, or a lost first digit); 0322_b l. 27 the **4** of "73[4?]".
3. "Taufen werden[?]" against "wurden" (0318_a l. 28; 0322_b l. 22 is "werden").
4. 0322_b l. 16 "[Religi?]" against "Kateg"; 0318_a l. 26 "Kreuzen[?]";
   0322_b l. 28 "gegen über" (a space in the manuscript?).
5. 0318_a l. 10: "[Ho?]" - the twin's "folge[nden]" suggests "fo"; if so the
   supply "lgen-" would become a B.
6. 0345_a ll. 5-6: the strokes before "stor" may be a Kurrent P, so "Pastor"
   may be legible there (the supplies hold either way).
7. 0322_a l. 16 and 0345_a l. 15 "wurden nicht [...]sammelt": "ge" fits the gap, not
   "ein" (the usual "eingesammelt") - left C.
Everything else the second reader marked "doubtful" stays doubtful in the text.

## Things to know

- "Zagorow" in the text is the pastor's form of Zagórów; "Lissewo-Pyzdry" the
  filial of Lisewo/Pyzdry (the Pyzdry prayer-house community). Place of
  writing and the day/month are not in what survives; the date is `1882` (year
  only), from the file's title and "Jahre 1881 gegenüber".
- "Superintendent Pastor Manitius at Warsaw" (mission money) and "Superintendent
  von Boerner at Płock" (widows' fund) are the persons the report names; the
  Konstantynów sample is signed "Sig. Manitius, Pastor": whether the Warsaw
  superintendent is the same man is open. Which diocese Zagórów belonged to
  is not in these pages (the Konstantynów report speaks of the superintendent
  of the "Ka[li]scher Diöcese"): check Kneifel and Werner before saying.
- `pipeline/regenerate.py` stops at `check_pipeline.py` (23 "names one holding"
  problems in older review scripts, present before this unit): the steps were
  run one by one (resolve_linebreaks, resolve_paragraphs, build_db,
  match_scans, merge_corpus, build_dataset, connections_site,
  build_site_data, person_pages, place_pages, then jekyll and verify_site).
- The scans are in `C:\Users\Tersnaus\Downloads\AGAD_1_432_0_1_139\processed`
  (the unit's `raw_dir`), not in the repository.
