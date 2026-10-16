# Notes for Claude

Read at the start of every session. Short on purpose: the detail lives in the
files it points to.

## Start here

- `README.md`: what the edition is, the layout, how a holding is added.
- `docs/README.md`: which docs are standing reference. `docs/NEEDS_CONFIRMATION.md`
  is the live list of open questions; keep it current when something is settled.
  `docs/TODO.md` is the editor's to-do list (next steps, in order): tick or
  remove an item when it is done.
- `docs/HOUSE_STYLE.md` governs everything written about the documents;
  `docs/EDITORIAL_RULES.md` the transcriptions, which are never "tidied".
  No cryptic statements: every sentence says who, what, and why it matters
  (HOUSE_STYLE, "No cryptic statements").
- The editor is `takaji10`. They do not read German: German text is written
  here, and checked by the claim check or by Claude, not by them.
- `docs/WORKING_NOTES.md`: how the editor works, the mistakes already made
  once, and the traps in the tools. **Read it.**
- No paid model run without the editor's agreement to that run; free checks
  need none (WORKING_NOTES, "Working with the editor").

## Lessons go into the repository (the editor's rule, 2026-10-05)

The editor switches between desktop and cloud sessions. A desktop session's
memory folder is on their machine and no cloud session can read it. So:

1. **Whatever a session learns that a later session will need is written
   into the repository in the same sitting**: a correction or ruling from
   the editor, a mistake made, a trap in a tool, a method that worked. It
   goes into `docs/WORKING_NOTES.md`, or the document it belongs to
   (`docs/EDITORIAL_RULES.md` for the text, `docs/HOUSE_STYLE.md` for prose,
   `docs/NEW_UNIT.md` for the procedure, the holding's `notes.md` for one
   holding), and is committed with the work. A desktop session may save it
   to memory too; memory is never the only place.
2. **Every report to the editor on work that was committed ends with one
   line beginning "Lessons:"**, saying what was written down, or "Lessons:
   none." The editor sees that the question was asked.
3. **A check holds the session to this.** `.claude/settings.json` has Claude
   Code run `.claude/hooks/lessons_check.py` each time Claude is about to
   stop, on the desktop and in the cloud. If the session has committed work
   that did not change `docs/WORKING_NOTES.md`, and the reply has no
   "Lessons:" line, it stops Claude from finishing once and says so. Do not
   remove or weaken the check without the editor's word.
4. A lesson that is only committed is not yet in the other kind of session:
   it travels when the work is pushed. Say so if a session ends with
   unpushed lessons.

## "Access the dictionary hosts"

When the editor says this, they mean: the cloud environment now allows the
reference sites the glossary's draft definitions are to be checked against,
so check them.

1. Confirm the hosts answer: `curl -sS -o /dev/null -w '%{http_code}'` to
   `https://www.woerterbuchnetz.de/` (Adelung, Grimm),
   `https://kruenitz.uni-trier.de/` (Krünitz, Oekonomische Encyklopädie) and
   `https://pl.wikisource.org/wiki/Encyklopedia_staropolska` (Gloger). Try
   WebFetch too. If any is refused, say which, and how to allow it: the cloud
   environment menu in the session's title bar, Edit, Network access, add the
   host to the allowed domains (read `read_documentation` topic
   `environment.network` for the current wording). Do what the reachable
   hosts allow.
2. Work through `reference/glossary.yml`: every entry with `checked: false`
   names its `check_against` work. Look the term up there (Gloger for Polish
   terms: starosta, wójt, sołtys, olędrzy, propinacja, łan, komornik, sąd
   pokoju; Krünitz for land, money and measures; Adelung for words and
   formulas). Correct the English and German definitions where the work says
   otherwise, then set `checked: true` and a `source:` naming the work and
   the entry (with its URL). Leave `checked: false` where the work is not
   online here (the Allgemeines Landrecht, the Hypothekenordnung, Acta
   Borussica, Grotefend) and say so.
3. Rebuild and verify: `python3 pipeline/build/build_site_data.py`,
   `cd site && bundle exec jekyll build` (gems: `bundle config set --local
   path vendor/bundle && bundle install` first in a fresh container),
   `python3 verify_site.py`. Commit, and update `docs/NEEDS_CONFIRMATION.md`
   (Glossary section) and the changelog.

## How this project is worked

- **Branch and publishing.** Develop on the session's branch. The live site
  (https://takaji10.github.io/triebenfeld-letters/) is built from `main` by
  `.github/workflows/pages.yml`, which runs `verify_site.py` as a gate. To
  publish, fast-forward `main` to the branch and push, then confirm the
  "Build and deploy" run succeeded. Publish only when the editor says so.
- **Line endings.** Many files are CRLF (`docs/*.md`, `site/_data/i18n.yml`,
  `site/_layouts/*.html`, `README.md`, `browse.js`). Edit them preserving CRLF
  and check `git diff --stat` shows only the real change.
- **Not in the repository:** `review/` (generated sheets), `cache/` (model
  output, on the editor's machine), raw scans. There is no Anthropic API key
  here: paid runs (translate.py, summarise.py, read_letters.py) happen on the
  editor's machine. `regenerate.py` cannot run end to end in the cloud (its
  early steps fetch from DWDS and write into `review/`); run the later steps
  directly.
- **Fixing the English** without re-translating: rules go in
  `reference/english_forms.yml`, one-page corrections (with the German that
  decided them) in `reference/english_corrections.yml`. Both are applied by
  `pipeline/translate/english_forms.py --apply` and by publish_translations.py
  at every publish, so a re-publish keeps them. Never hand-edit
  `site/_data/translations/` alone.
- **The glossary** (`reference/glossary.yml`, plan in `docs/GLOSSARY_PLAN.md`):
  English and German written separately; read every new pattern against its
  matches in `review/glossary_matches.csv` before publishing.
  `glossary_candidates.py --check` is a gate in regenerate.py: a translated
  holding's qualifying words must each be an entry or ruled out under
  `excluded:` with a reason.
- **Sources supplied by the editor** go in `reference/sources/`, verbatim with
  a working translation, and entries cite them with `source:`.

## Where things stand (2026-10-16)

- **Kuryer Polski 1754, nr 75** (slug `kuryerpolski1754075`, added
  2026-10-16, **published 2026-10-16**): the first holding from print and from a
  library (repository `bkpan-kornik`, document type `newspaper`): the
  report on the funeral of Paweł Prusimski at Trąbczyn, 5 December 1754.
  The editor means to add more newspaper items; the slug for another issue
  is `kuryerpolski<year><number>`. The editor kept the one doubtful word,
  "[Cleri?]". Nothing waits. Read `units/kuryerpolski1754075/notes.md` first.
- **ADWł 85** (slug `adwl85`, added 2026-10-15, **published 2026-10-16**), the
  first holding from the Diocesan Archive in Włocławek: nine pages of the
  visitation of the Konin deanery of 1790 and 1791, the pages the editor's
  transcript covers. Two documents (editor): the parish of Trąbczyn (leaves
  23v-25v, 28v-29v) and the table of the souls of the parish of Zagórów
  (leaf 34a). The passages of these pages the transcript left out were
  transcribed in session at the editor's word; every page read against the
  scans; English, summaries and claim check in session; era
  `prusimski-boundary`. The editor answered the spot sheet (3 marks of
  doubt remain); the reference has no series name. Published at the
  editor's word; the edition now has 591 documents in 43 holdings and 882
  marks of doubt. Still offered: the rest of the visitation of Trąbczyn.
  Read `units/adwl85/notes.md` first.
- **Published and pushed before ADWł 85 (2026-10-15)**: 589 documents in
  42 holdings, 879 marks of doubt (with letters 9 and 300 of Oe 1 Bü 9454,
  published later the same day). The last two went out together at the
  editor's word: APŁ 39/98/0/-/6603 and APP 53/968/0/-/716 (below). Three
  eras carry working names until the editor names them: `wlodzimierz`,
  `liquidation` and `twentieth-century` (`reference/eras.yml`).
- **APŁ 39/98/0/-/6603** (slug `apl399806603`, added and published
  2026-10-15), the first holding from the State Archive in Łódź: the
  liquidation table of the Łazińsk colony (1868), its copy (1869) and the
  entries to 1901, six documents, three of them tables; openings joined into
  one page by cut edges (`EDGES` in its `holding.py`). It and Breyer's copies
  of the tables in -/716 stand in the new era `liquidation` (editor,
  working name). Read `units/apl399806603/notes.md` first. The editor
  approved its page edges and answered its spot sheet (18 marks remain).
- **APP 53/968/0/-/716** (added 2026-10-14, published 2026-10-15) (slug `app539680716`), Albert
  Breyer's notebook on Łazińsk, Emilienheim and Orliny, with a loose sheet
  of 1858: thirteen documents by content (the editor's choice), six of them
  tables (Russian liquidation tables of 1868, Breyer's counts, the Polish
  hearth-tax list of 1858), read from the editor's raw photos in session.
  **A copy takes the date and era of what it copies** (editor,
  2026-10-14): Breyer's copies of 1858 to 1892 stand in `wlodzimierz`, his
  own notes in `twentieth-century` (`reference/eras.yml`, header).
  The editor's answers on both spot sheets are in (2026-10-15); names and
  figures in Breyer's copy of the Łazińsk table follow the original
  (6603), and Zelmer is always Цельмеръ (editor). Michalina died 19 January 1851, Włodzimierz 20 December
  1879, then his nephew Władysław was heir (editor). The folds and page
  edges are approved (editor, 2026-10-15). Read `units/app539680716/notes.md` first.
- **Published 2026-10-14**: 570 documents in
  40 holdings, 1589 to 1936. The last three, all from
  the State Archive in Poznań, went out together at the editor's word
  (`docs/TODO.md`, sections 10 to 12). Two eras carry working names until
  the editor names them: `wlodzimierz` and `twentieth-century`
  (`reference/eras.yml`).
  - **APP 53/968/0/-/783** (slug `app539680783`): a printed summons of
    1860 in Polish, Count Włodzimierz Miączyński's counterclaim against 97
    colonists of Trąbczyn over pasture and wood in his forest; one
    document on five pages, with the cover. The editor's Polish checked
    against the scans; **the editor's English, a machine's, was wrong in
    substance and was written again** (`intake/changes.yml`, on the page
    of changes). Read `units/app539680783/notes.md` first. The folds are
    approved; the Count was Michalina's son; the Staro- and Nowo-Łazińska
    colonies are the estate's two Olęder colonies (earlier Trąbczyńskie
    Stare / Nowe Olędry), not the village of Łazy (editor, 2026-10-14).
    Their answers on the spot sheet "Pen marks on the summons"
    (`review/app539680783/pen_marks.csv`,
    `docs/TODO.md` section 10) are worked in (no. 58 Heck, no. 70
    Krystofa, costs 47). Its era is the new `wlodzimierz` (editor,
    2026-10-14; working name). Published 2026-10-14.
  - **APP 53/64/0/-/Kalisz Tab.21** (slug `app53640kalisztab21`): thirteen
    pages of the hearth-tax register of 1789, a table of 387 entries
    (Trąbczyn is 178 of the third district). No transcription existed: read
    from the scans in session, like AGAD 1/169/0/1/1745; the reading is
    `intake/table.csv` and everything is made from it by
    `intake/holding.py`. **Checked by the editor** (2026-10-14: 69 names
    corrected, no figure changed) and worked in; the clean spreadsheet is
    in the unit's folder. `017v.jpg` is leaf 9 verso (editor). Published
    2026-10-14.
  - **APP 53/968/0/-/669** (slug `app539680669`): Albert Breyer's pencil
    notebook of July 1936 from Łazińsk and Emilienheim, 35 pages in German,
    one document. Only the notebook in the scans folder "Notes on Łazińsk"
    (editor); the editor's "Breyer Notes.md" there renders another notebook
    and was not used. No transcription existed: read from the scans in
    session (`intake/holding.py`), English in `intake/english.py`,
    summaries claim-checked. Read `units/app539680669/notes.md` first.
    The editor answered three spot sheets (42 readings; 70 marks of
    doubt remain, on the inside covers and in the photo log, not asked). Its era is the new `twentieth-century`
    (editor, 2026-10-14; working name). Published 2026-10-14 with document
    1. **Document 2**, the notebook "V. Grodziec Juli 1936" from the
    editor's photos IMG_5192 to IMG_5205, was added the same day, its
    readings checked by the editor on two spot sheets, and published.
- All cloud branches are in `main` (2026-10-14).
- **AGAD 1/169/0/1/1745** (slug `agad1169011745`, added, checked and
  published 2026-10-13), "Die neuesten topografischen Nachrichten von
  Südpreussen": six pages of a Prussian table of the villages around
  Konin, of about 1797 (entries 140 to 303, Trąbczyn is 291), one document,
  a table. There was no transcription: the table was read from the scans
  in session, and the editor then checked every line on a spreadsheet with
  a picture of each line (25 names corrected, no mark of doubt left, no
  figure changed) and let the folds stand. The reading is
  `units/agad1169011745/intake/table.csv`; the text, the English and the
  clean spreadsheet to keep (`AGAD_1_169_0_1_1745_table.xlsx` in the
  unit's folder) are made from it by `intake/holding.py` (read its
  docstring and the unit's `notes.md` first). "Szyman." in it is short for
  Szymanowice (editor). Nothing waits on the editor; offered and not
  answered: modern names for the 164 villages, a sentence in the era essay.
- **The sitting of 2026-10-07 and 10-08** published the
  twenty-one Prusimski-era holdings, put that era on the timeline (sixteen
  events, 1589 to 1788, and a band where each era begins;
  `site/_data/timeline.yml`, `site/_includes/timeline.html`), and worked in
  the archive's new scans of **Oe 1 Bü 9454, letters 245 and 289**
  (`units/oe1bu9454/notes.md`, "Rescans of letters 245 and 289": text made
  from the old text, the editor's new transcription and the scans; English
  and summaries follow; the editor settled ten words on a spot sheet).
  The edition then had 565 documents in 36 holdings.
- **The summaries of Oe 1 Bü 14525 and 14526 were written again** at the
  editor's word (2026-10-08, cloud session): read whole in the German,
  summarised in German, English from the German, claim-checked (212 and 182
  statements; each holding's `intake/summaries_draft.py` and
  `intake/claim_check.yml`, "Summaries" in its `notes.md`). Every holding's
  summaries have now had the check. One date corrected against the scan
  (14525, doc. 7) and one name (14526, doc. 26: Kriede, editor 2026-10-09);
  the dates of 14525, docs 13 and 21, stay as they are (editor). Merged
  into `main` and published on 2026-10-13.
- **Spot sheets** (`pipeline/review/queries.py`): a sheet can run across
  holdings (a `unit` column), ask for a decision (a `summary` column) and
  show a picture of a line (an `image` column). `docs/WORKING_NOTES.md`,
  "Working with the editor".
- Glossary live: 111 entries, 125 words ruled out (2026-10-14; Matura added
  at the editor's word). 55 checked: the
  patrimonial court (the editor's Szukaj w Archiwach source) and 54 read
  against Krünitz, Adelung, Grimm and Gloger. The other 56 wait on works not
  online here, or have no entry in those that are (NEEDS_CONFIRMATION).
- Names standardised in the English (the names audit and the editor's
  rulings of 2026-10-03, live): only Schliefen / Schlieffen is open.
- The Hohenlohe-Ingelfingen years page is rebuilt from all nine holdings;
  seven files from the Geheimes Staatsarchiv are still to be added, each
  worked in per `docs/HOHENLOHE_ERA_PLAN.md`.
- **III. HA MdA, III. Nr. 12366** (slug `iiihamdaiiinr12366`, added
  2026-10-04) is in: six documents, five French and one Polish, corrected
  against the scans, summarised in both languages, translated in session
  (pilot first; pages kept in `intake/translation/`) and its summaries
  claim-checked in session (`intake/claim_check.yml`); status `translated`,
  untagged. Read `units/iiihamdaiiinr12366/notes.md` first; its `review/`
  records are copied into its `intake/`. Still open: the
  editor's ruling on its era (Hohenlohe or restitution), and the words in
  `intake/unresolved.md`.
- **III. HA MdA, III. Nr. 12367** (slug `iiihamdaiiinr12367`, added
  2026-10-04), the second volume of the same file: eleven documents of 1828
  to 1832 on the compensation of the banker Weigel (eight French, two
  Polish, one German), corrected against the scans and summarised in both
  languages, with its page, timeline entries and a paragraph in the era
  essay; translated and its summaries claim-checked in session on
  2026-10-05 (pages in `intake/translation/`, `intake/claim_check.yml`);
  status `translated`, untagged. Read `units/iiihamdaiiinr12367/notes.md`
  first. Still open: its era, the unread signature on scan 0007 (tried
  again 2026-10-05), and the words in `intake/unresolved.md`. The German
  translations beside the two Polish letters stay untranscribed (editor,
  2026-10-05); the end of the note on scan 0004 and its margin line were
  read that day (`intake/second_reading.py`, `sideways.yml`).
- **AGAD 1/174/0/2/73** (slug `agad11740273`) and **AGAD 1/174/0/1/6** (slug
  `agad1174016`), added 2026-10-04, the first holdings from AGAD in Warsaw:
  six documents of July 1807, Michalina Dąbska's petitions and the Governing
  Commission's resolution returning the Prusimski estates (five Polish, one
  French). Pages cut out of the editor's images by boxes recorded in each
  unit's `intake/build_pages.py`; corrected against the scans, summarised in
  both languages, with holding pages, a timeline entry and two sentences in
  the era essay; translated and claim-checked in session on 2026-10-05;
  status `translated`, untagged. Read each unit's `notes.md` first. Still
  open:
  the era (placed in `hohenlohe` for now; by `reference/eras.yml` they
  belong to `restitution`), and the editor's look at the crops and at
  image 06.
- Nr. 12367 and the two AGAD holdings were published at the editor's word
  on 2026-10-05 (commit df7a05da). What is left for each is in
  `docs/TODO.md`.
- **How a holding is translated in session** (as for these three and Nr.
  12366): one `doc<N>.yml` per document and `write_cache.py` in the unit's
  `intake/translation/` (copy from any of them), then check_translations.py,
  publish_translations.py, uncanonical_names.py; the claim check in
  `intake/claim_check.yml`; then status `translated`, the glossary gate, the
  holding's "Still to do", `docs/TODO.md`, NEEDS_CONFIRMATION and the
  changelog. `match_scans.py` needs the raw scans and does not run here; a
  change to a document's pages means correcting `page_scan_map.csv` by hand
  (Nr. 12367's notes, "Mardi put back").
- Every holding is now translated (the four of Oe 1 Bü 9454 without text
  excepted: 121, 181, 225, 293). **Letter 9 of Oe 1 Bü 9454**, long marked
  "skipped", was added from the editor's transcription on 2026-10-15
  (`units/oe1bu9454/notes.md`, "Letter 9"; spot sheet `letter_9.csv`).
  The editor answered its spot sheet the same day. **Letter 300** of the
  same holding was made again from the editor's new crops and
  transcription (2026-10-15, `intake/scripts/recrop_300.py`). Both
  **published 2026-10-15** at the editor's word; the edition counts 879
  marks of doubt (the count includes "[...]").
- **APP 53/968/0/-/801** (slug `app539680801`, added and published
  2026-10-05): three documents on sixteen pages, copies made about 1930
  (papers of Albert Breyer): the Prince's power of attorney for Triebenfeld
  (1, 19 February 1805), the chamber's consent to the parcelling of Zagórów
  and Trąbczyn (2, 28 January 1806) and the lease of 100 Hufen of the
  Drzewce forest to eighteen settlers (3, engrossed 21 March 1806). First
  built as one document, divided at the editor's word the same day
  (`intake/split_documents.py`; `intake/corrections.py` is a record, not to
  be re-run). 84 passages corrected against the scans, summarised in both
  languages, holding page, two timeline entries; translated and its
  summaries claim-checked in session the same day (`intake/translation/`,
  `intake/claim_check.yml`); status `translated`, untagged. Read
  `units/app539680801/notes.md` first. Heinrichs,
  who attests the lease, has his own person entry and is not Honrichs
  (kept separate: editor, 2026-10-05).
- **I. HA Rep. 162, Nr. 295** (slug `iharep162nr295`, added 2026-10-05),
  "Capital on the Zagorow estates": the cover and eleven pages of copies of
  1805, three documents: Triebenfeld's bond to the Invalids' Fund for 50,000
  Rthl (1, Berlin, 28 January), the Kalisz court's certificate of its second
  acknowledgement (2, 5 March) and the mortgage certificate for Zagórów (3,
  13 March). The editor photographed each page twice, top and bottom;
  `intake/build_pages.py --crop` joins each pair into one page image
  (numbers in `intake/stitch.json`, found by `intake/find_stitch.py`, which
  needs OpenCV). The editor transcribed from those images; 34 passages
  corrected, summarised, translated and claim-checked in session; status
  `translated`, untagged. Read `units/iharep162nr295/notes.md` first. Published
  at the editor's word on 2026-10-05. The editor confirmed "Grądzyn" in the bond's list of estates and
  the three documents, and answered a spot sheet of five readings, which
  is applied (2026-10-05). Nothing is open.
- **I. HA GR, Rep. 7 C, Nr. 1414** (slug `ihagrrep7cnr1414`, added
  2026-10-05), "Anton Prusimski Venice Residence": three documents on four
  pages, December 1796 to March 1797 (the extract of the Prussian
  resident's dispatch from Venice, in French; the foreign department's draft
  to Hoym, Schroetter and Goldbeck; Schrötter's reply). Scans 0002 to 0005
  only (editor); three openings cut to the written side by boxes in
  `intake/build_pages.py`. The editor's line-by-line transcription cut to
  pages, office marks set apart (`office_notes.yml`), 20 passages corrected,
  summarised, translated and claim-checked in session; status `translated`,
  untagged. Read `units/ihagrrep7cnr1414/notes.md` first. Published at
  the editor's word on 2026-10-05, with Nr. 295. The
  editor confirmed Raumer, Goldbeck and Haugwitz and ruled that the papers
  are filed under no estate (2026-10-05). The first signature under the
  draft stands as "A[lvensleben]" (initial read, name supplied from his
  office; the editor cannot verify it). Open: the editor's look at the four
  crops.
- **APP 53/17/0/-/Konin Gr.145** (slug `app53170koningr145`, added
  2026-10-06), the first holding of the Prusimski era
  (`era: prusimski-boundary`): one document of 122 pages, the decree of the
  commission that fixed the boundary between Trąbczyn and Łukomia in 1775,
  from a court book of Konin for 1776. 62 openings cut at the fold
  (`intake/build_pages.py`); the editor's Polish transcription, in modern
  spelling and by paragraph, and the editor's own English translation, cut
  to the pages (`intake/translation/build_doc1.py`), not translated again.
  A light check first, then at the editor's word all 122 pages read against
  the scans (2026-10-06): 233 corrections, 27 dropped phrases restored
  (`intake/full_check_rows.py`, `intake/corrections_full.py`, neither to be
  run again); the English follows in 32 places
  (`intake/translation/fixes_full.py`), one of them a paragraph the English
  itself lacked. Status `translated`. Read
  `units/app53170koningr145/notes.md` first. Published on 2026-10-07 with
  the other Prusimski-era holdings; the editor placed its folds and
  confirmed the tower sentence and the paragraph on leaf 680 on the spot
  sheet "Before publishing". The era's fuller account waits for the
  transcriptions the editor will supply; the glossary for these Latin and
  Polish holdings has not been begun.
- **The Prusimski-era run (editor, 2026-10-07): process every unit without
  stopping; all questions, fold adjustments and reviews of readings are held
  for one review at the end.** Each question goes into
  `docs/PRUSIMSKI_QUESTIONS.md` with the default that was taken, and the
  holding is built on the default. Nothing is published before the review.
  (The review was held on 2026-10-07 and the holdings published that day.)
- **The run is finished and published: every court-book folder with a text
  is built** (2026-10-07) and went live the same day at the editor's word.
  Twenty-one Prusimski-era holdings, 93 documents, 1589 to 1788; the edition
  has 565 documents in 36 holdings. Beside Konin Gr.145 they are:
  **53/6/0/-/17** (`app536017`, 1589), **-/36** (`app536036`, 1644), **-/40**
  (`app536040`, 1728), **-/45** (`app536045`, 1763), **-/46** (`app536046`,
  1777), **-/47** (`app536047`, 1783); **Kalisz Gr.414**
  (`app53150kaliszgr414`, 1771), **Gr.424** and **Gr.425** (1776); and the
  Konin registers **Gr.136** (1754), **Gr.114** (1767), **Gr.115**
  (1768-73), **Gr.116** (1775-77), **Gr.117** (1778-79), **Gr.118**
  (1780-82), **Gr.153** (the boundary decree of 1782), **Gr.119** (1783-84),
  **Gr.120** (1785-86), **Gr.121** (1788), slugs `app53170koningr<n>`. Read
  each holding's `notes.md` first; from Konin Gr.136 on, everything about how
  a holding was made is in the docstring of its `intake/holding.py` (one
  script for all steps, `courtbook.holding_main`). Pyzdry Gr.75 is deferred
  by the editor.
- **The editor's review is done but for the word to publish** (2026-10-07).
  They placed the folds of all twenty holdings (each holding's
  `intake/folds.json`), read the page of changes and answered the main
  questions (`docs/PRUSIMSKI_QUESTIONS.md`, "The editor's answers"). Carried
  out the same day: **the full check of Konin Gr.117, Gr.118, Gr.153 and
  Gr.119** (every page read; the record is each holding's
  `intake/full_check.json`, applied once by `holding.py --full`; no document
  is marked rough); **Górski** in the English, "Gorski" kept in the
  transcription; **entry no. 17 of 53/6/0/-/46 transcribed in session** as that holding's
  document 2. (Entry no. 43 of 53/6/0/-/47 was transcribed too and taken out
  again at the editor's word, as not relevant; its text is kept in that
  holding's `intake/entry_43.md`. Do not build it again.) **Published at the
  editor's word on 2026-10-07**, after they answered the spot sheet "Before
  publishing" (`docs/PRUSIMSKI_QUESTIONS.md` lists the answers; the rows are
  `docs/PRUSIMSKI_before_publishing.csv`). Nothing waits on the editor for
  these holdings. **The account of the
  era waits** until they have supplied the missing transcriptions. The
  backlog (headings of sittings, the middle of Konin Gr.136, three entries
  of 53/6/0/-/17) is in `docs/TODO.md`, section 7. The seven untranscribed
  scans of Konin Gr.119 are not relevant (editor) and stay out.
- **The fold pages** (`review/<slug>/folds/index.html`, made by each
  holding's `holding.py --sheet`, `build_pages.py --sheet` in the first
  four, `fold_sheet.py` for Konin Gr.145). **One fold page for every
  holding** (`pipeline/intake/fold_page.py`, the page `review_folds.py`
  always wrote): one opening at a time, shown whole, arrow keys to page
  through, the red line dragged onto the fold. For the court books the
  sheet can also be turned with the mouse (wheel, or shift-drag) where the
  fold was photographed at a slant. Two green lines mark the page edges,
  what is kept on each side (editor, 2026-10-15: "give me the ability to
  mark vertical lines for where to crop pages"); a holding can propose
  them (`EDGES` in 53/968/0/-/716's `holding.py`). "Save" gives
  `folds_<slug>.json` with the fold, angle and edges of every scan; `python pipeline/intake/courtbook.py
  folds <slug> <file>` copies it to the holding's `intake/folds.json`,
  turns and cuts the scans, stages and remakes the page images. **Do not
  build another review page where one exists** (the editor, 2026-10-07).
  A holding's `intake/folds.json` is the editor's and wins over the
  numbers in its script; never overwrite it except with a file they saved.
- **The page of changes** (`review/changes/index.html`, made by
  `pipeline/review/changes_page.py` from each holding's
  `intake/changes.yml`): what the check against the scans changed, graded,
  for the editor to put right what they have written outside the project.
  Write a holding's `changes.yml` when it is checked and run the script.
  **The editor keeps this page and works from it**: an entry written after
  they read it (2026-10-07) carries `new:` and is marked on the page.
- **The Prusimski era** (editor, 2026-10-06): `docs/PRUSIMSKI_ERA_PLAN.md`
  has the editor's decisions, the inventory, the method and the batches,
  all five now built. Nine folders without texts are listed there for the
  editor. Desktop work only: the scans are on the editor's machine.
- **Rulings of 2026-10-05, standing** (`docs/EDITORIAL_RULES.md`):
  struck-out text is not transcribed; a translation of the time written
  beside a document is not transcribed where the original is given.
- The fifteen summaries of Nr. 3709 were claim-checked in session on
  2026-10-05 (`units/ihagrrep7cnr3709/intake/claim_check.yml`): every
  holding's summaries written from the German have now had the check.
- Open before wider sharing: the archives' permission for the scans; the
  editor's full name for the licences (`site/_data/rights.yml` and `LICENSE`).
- Everything else open is in `docs/NEEDS_CONFIRMATION.md`.
