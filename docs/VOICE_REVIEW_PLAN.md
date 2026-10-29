# Reviewing the site's own prose against the editor's voice

Agreed with the editor on 2026-10-29. The yardstick is `docs/EDITORS_VOICE.md`
(the samples' analysis and "The brief"), with `docs/HOUSE_STYLE.md` deciding
where the two differ.

## Scope

In: the document summaries (finding aids: the rules applied, not the full
narrative voice), the holdings' "About" and "How it was prepared", the
literature's accounts, briefs and summaries, the newspapers' accounts and
briefs, the hand-made links' sentences, the people's bios and genealogy notes,
the glossary. English and German, each written in its own language.

Out:
- the transcriptions, the reading copies and every translation, including a
  translator's note inside one (the editor, 2026-10-29);
- the timeline and the static pages (About, the story, the Hohenlohe page,
  rights): they will be rewritten separately;
- the gazetteer, which is the editor's own text, kept verbatim.

No paid run. Sonnet sub-agents may take the procedural steps below; the
judgement (what to cut, the rewrites, the claim checks) stays in the main
session.

## Steps

1. **Commit the work so far** (done: 8cf39653).
2. **Read the "edition" pass** (done 2026-10-29). All 444 changed sentences
   read, old against new; 113 hand fixes, among them the German "Ausgabe"
   the rules had missed. Left for step 5: "NEEDS_CONFIRMATION" and dated
   rulings still shown in some literature accounts, "(the documents
   first)" and similar asides, the era slug "wlodzimierz-era" in Kraus
   (2001)'s account.
3. **Mechanical scan** (a script, free): sentence length against the
   editor's 29 words; "however", "moreover", "you", questions, contractions;
   the spaced en dash; Canadian spelling; repository talk on a reader's page
   (NEEDS_CONFIRMATION, file paths, "the editor's ruling", dated rulings);
   signposting and self-narration (HOUSE_STYLE). A report per file.
   Done 2026-10-29: `pipeline/review/voice_scan.py` writes
   `review/voice/report.md` and `counts.csv`. Median sentence (EN): literature
   50 words, newspapers 53, links 39, holdings 25, summaries 23, people and
   glossary 17; 752 dashes not in the spaced en dash; repository talk on
   reader pages mostly in the literature (NEEDS_CONFIRMATION, dated rulings).
4. **Pilot:** one holding page, ten summaries, two literature accounts, a
   handful of bios and glossary entries, before and after on one page for the
   editor; their rulings go into EDITORS_VOICE.
   Done 2026-10-29: the pilot (`review/voice/pilot.html`) and the editor's
   rulings (EDITORS_VOICE, "The editor's rulings on the pilot").
5. **Rollout by kind:** progress -
   - dashes, mechanically (`pipeline/review/dash_fix.py`), all but the
     summaries: done 2026-10-29;
   - the literature's accounts and cards, all 39 works
     (`pipeline/review/set_work_texts.py`, batches in `review/voice/`): done
     2026-10-29, median sentence 29 words from 50;
   - the newspapers' accounts and cards, all 12 items: done 2026-10-29, 24
     words from 53;
   - the hand-made links: fifteen of 32 rewritten (the rest read well), 34
     words from 39: done 2026-10-29;
   - the holdings' pages: the 85 sentences of more than 60 words split by a
     Sonnet sub-agent (`review/voice/holdings_long.yml`, its report
     `holdings_long_report.md`), the diff read word by word in the main
     session; 81 split, 4 lists left whole: done 2026-10-29, 23 words;
   - the detailed summaries of the works shown by summary: the repository
     talk taken out (NEEDS_CONFIRMATION, "the documents first", a dated
     ruling, the citation files' method): done 2026-10-29; their long
     sentences (about 200, mostly in Słowiński 2023 and 2024) still to split;
   - still to do: those long sentences, the document summaries (with their
     dashes), the people, genealogy and glossary (light).
   The order planned: holdings, literature, newspapers and links, people,
   glossary, then the summaries in batches of about fifty. Each batch is
   rebuilt and verified; a changed summary is claim-checked again and carried
   into every place it is kept (WORKING_NOTES, "Where one summary is kept").

## Who does what

| Step | Sonnet sub-agent | Main session |
|---|---|---|
| Extracting before/after pairs and review batches | yes | reads them |
| The scan script and its report | yes | decides what the flags mean |
| Mechanical fixes from a fixed list (dashes, spelling) | yes | spot-checks |
| Rewrites | summaries only, after the pilot, as drafts | all else; reviews every draft batch |
| Claim checks | no | yes |
| Carrying a summary into its six places, rebuild, verify, EN/DE parity | yes | reads the result |
