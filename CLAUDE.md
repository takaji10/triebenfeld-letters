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
- **The documents first** (the editor's rule, 2026-10-20): every fact is
  first looked for in the edition's own archival documents, before a book
  or any other source; where they disagree, the edition keeps to the
  document and the difference is flagged in `docs/NEEDS_CONFIRMATION.md`
  and recorded in the source's `notes.md` (HOUSE_STYLE, "The documents
  first"). Restated 2026-10-21: a date or fact from a document is taken over
  a book's without asking; the flag records the difference so that it is
  known.
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
- **Line endings.** Every text file is LF, on the desktop and in the cloud
  (`.gitattributes`, editor 2026-10-19). A script that writes a file to be
  committed uses `newline='\n'` (and `lineterminator='\n'` for `csv`).
  WORKING_NOTES, "Line ends".
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

## Where things stand (2026-10-23)

- **Werner (1904)** (`werner1904`, added 2026-10-23, **committed, not
  published**): Albert Werner, *Geschichte der evangelischen Parochien in
  der Provinz Posen* (Lissa: Friedrich Ebbecke 1904), the numbered
  parish-by-parish history of the evangelical parishes of the Prussian
  province of Posen. Only entry 201, the parish of Wreschen (Września),
  printed pp. 422-424, is brought in, whole, with the title page as the
  work's front - the editor's word: "only entry 201 about Wreschen is
  relevant for the project". Its bearing: the Wreschen parish served the
  German Hauländer country around **Peisern (Pyzdry)** and **Zagorowo
  (Zagórów)** until 1817, when that "an deutschen Hauländereien reiche
  Gegend" went to Russia - the edition's `peyserschen-hauland`. Read by OCR
  alone from the editor's page images of the WBC digitisation (34695/51858;
  no local Tesseract - the lunaroute converter, whole pages then bands then
  lines); the twenty readings the passes did not settle are on the editor's
  spot sheet (`scratch/werner1904_sheet.py`, answers to
  `review/werner1904/query_answers.json`), still open. Index ruled
  (`literature/index.yml`); the Sokolnik refusal and the two identifications
  from outside the page (Orangeriehaus, Hesekiel) open in NEEDS_CONFIRMATION.
  `docs/LITERATURE_PLAN.md`, section 25. Read
  `literature/werner1904/notes.md` first. Not published.
- **The three Lidmanowski texts** (`zdrowie1912z10`, `jutrzenka1913z8`,
  `zdrowie1914z6`, added 2026-10-22, **committed, not published**): the
  first learned-journal articles of the Newspapers section and the first
  batch from the editor's own Markdown file — two in *Zdrowie*, the organ
  of the Warsaw Hygiene Society (the nutrition study of the Słupca powiat,
  R. XXVIII, z. 10, 1912; the housing survey, R. XXX, z. 6, **1914** —
  dated 1914 against the file's name "1912-1913" at the editor's word,
  the metadata, the issue's ToC and the literature agreeing) and one in
  *Jutrzenka* of Łódź (the digest of the attire article, R. 3, nr 8,
  24 April 1913; its signature open, NEEDS_CONFIRMATION — the
  digitisation unreachable from the session). The editor's rulings: three
  separate items; the transcription secure (no OCR, no spot sheet, no
  page images); the English came with the file and was corrected against
  the Polish in session (eleven artifacts, recorded in the notes); all
  three shown whole (Dr. Konstanty Lidmanowski of Zagórów, 1865-1943,
  public domain since 2014); a person entry (`lidmanowski`, the Głowiecki
  shape, the Jutrzenka hit ruled). Read each item's `notes.md` first.
  Not published.
- **Słowiński (2023), finished, and Słowiński & Połom (2024), "Zerwane
  ogniwo"** (`slowinski2023`, `slowinskipolom2024`, added 2026-10-22,
  **committed, not published**): the twin Zagórów volumes from the
  editor's checked Polish and English Markdown exports, both under
  copyright and kept like Seidel (2018) - in the repository for questions,
  the site showing only the detailed summary, `visible: false`,
  verify_site.py checking no stretch of the text appears. The 2024 intake
  (`pipeline/literature/slowinskipolom_md.py`) returns on the export's
  repeated page marks round the picture plates; 0 PDF pages differ. The
  2023 folder committed now; its English is the editor's own files (the
  Claude translation not carried out); its year corrected to 2024. Open:
  the Mielke dates, the founders of 1746, the 1718 ruling (all in
  NEEDS_CONFIRMATION). `docs/LITERATURE_PLAN.md`, section 26. Read the
  works' `notes.md` first. Not published.
- **The place pages: Zagórów** (`zagorowo`, added 2026-10-22, **committed,
  not published**): the editor's new section (`places/`,
  `docs/PLACES_PLAN.md`) — a page per place that has sources of its own,
  hung on the place's card on the Places page and linked from it ("Let's
  add a new source to a place: Zagórów. This site has a lot of information
  that should be added under the place name, on a separate page for the
  place"). Built like the newspapers' machinery
  (`pipeline/places/place_pages.py`, collections `places`/`places_de`,
  layout `place`, one viewbar for the whole page, the card link, the checks
  in verify_site.py), bilingual like the person pages; a place page hangs
  on an estate card and the build fails loudly if its slug is no estate.
  The first place is Zagórów (/places/zagorowo/, /de/orte/zagorowo/); its
  first source `zagorowpl20220614` is the town's own presentation on
  zagorow.pl ("Miasto i gmina Zagórów", the Wayback Machine's capture of
  14 June 2022 the editor gave), the editor's rulings: the source shown
  whole (Polish as printed, nothing tidied, Claude's English beside it), a
  new per-place page, **no pictures** — the photographs marked "[Obraz]".
  Its self-contradictions (1262/1261; 1869/1870) kept as printed and
  recorded; open: the index over the sources, the 1869/1870, the medieval
  dates (NEEDS_CONFIRMATION, "The places"). Read
  `places/zagorowo/zagorowpl20220614/notes.md` first. Not published.
- **Słowo (1892) sells Trąbczyn** (`slowo18920104`, added 2026-10-22,
  **committed, not published**): the "Sprzedaże dóbr" notice in the Warsaw
  daily's "Kronika ekonomiczna" of 4 January 1892, p. 3, the third item of
  the Newspapers section — the press witness of Trąbczyn's sale by Count
  Miączyński to Countess Władysławowa Wielopolska for 225,000 rs., the
  transfer the wlodzimierz era's ownership line records ("by 1892 Countess
  Maria Wielopolska"). The editor's rulings: the snippet named only
  ("only this snippet of the article is needed"), their own crop of the
  column carried on the item's page, five readings ruled on the spot sheet
  (among them "150 włók" against the draft's 159). Read
  `newspapers/slowo18920104/notes.md` first. Not published.
- **Łukasiewicz (1997)** (`lukasiewicz1997`, added 2026-10-22,
  **committed, not published**): Dariusz Łukasiewicz, "Nowa analiza
  „Czarnego Rejestru". Studium źródłoznawcze", *Kwartalnik Historyczny* R.
  CIV, nr 2, pp. 31-62 - the modern source study of the black register the
  edition carries in print. The editor's rulings: the whole article, visible,
  the appendix tables as HTML tables. Read from the RCIN digitisation's page
  images (the OCR layer a scaffold only); the register's manuscript found in
  GStAPK and read against three official lists; the headline figures
  corrected (48 donataries, 52 donations, 245 estates, nominal 2 069 550
  Thaler, real value 4-7 million against the title page's 20 million); the
  corrupt side told (Hoym's circle, Triebenfeld's resale, the rescripts
  against selling to Poles). Two hand-made links tie it to the Prince's
  letters; where its figures differ from the documents, the documents stand.
  Read `literature/lukasiewicz1997/notes.md` first. Not published.
- **Kneifel (1964)** (`kneifel1964`, added 2026-10-22, **committed, not
  published**): Eduard Kneifel, *Geschichte der Evangelisch-Augsburgischen
  Kirche in Polen* (self-published, Niedermarschacht 1964), the first work
  from the editor's Markdown files - the German transcription and an
  English that pairs it page for page, read from their Books folder on J:
  and **not kept in the repository** (313 printed pages, a general church
  history, most of it not bearing on the edition). The editor's rulings,
  asked before the work began: the excerpt carries the place-named pages
  **and** the two colonisation sections; **visible** on the site (in
  copyright: published 1964, put to the editor first); only the excerpt
  scripts and the cut pages committed. The excerpt, 21 printed pages
  (`literature/kneifel1964/notes.md` first): pp. 39-42 (p. 41 names the
  Starost, "Paul von Kolno-Prusinski, Grundherr von Trombezyn", and the
  founding of Łazińsk in 1746), pp. 89-93 (the Prussian colonisation; p. 92
  "die Städte Konin, Zagö-röw und Kolo"), and pp. 45, 94, 102, 112, 123,
  165, 166, 179, 226, 235-236, 256 - the schools of the Kalisch land, the
  Grodziec contract of 1796, the parishes and the diocese list ("Zagörow
  mit dem Filial Lissewo-Pyzdry, Konin mit dem Filial Maslaki"), the
  Zagórów church of 1878-1896 and its pastors to 1945, the Łazińsk
  brethren's circles, the statistics of 1938. The false friend "Trombin bei
  Rypin" (p. 101) ruled out. Index: 140 hits, all read; `Trombezyn`,
  `Zagörow`/`Zagö-röw`, `Lazinsk` and `Prusinski` ruled in, `Brzyczka`
  refused, five old rulings sharpened. One hand-made link: p. 41 against
  the summons of 1860 and the boundary decree of 1775 (Kneifel names the
  husband alone, the documents the couple). `docs/LITERATURE_PLAN.md`,
  section 24. **Published 2026-10-22** at the editor's word, with the
  earlier sessions' committed work. The literature has 31 works, 29 on the
  site (two summary-only).
- **Minakowska (2026), the Starost's page, and the person pages**
  (2026-10-22, committed; not published): the first saved page of
  Minakowska's genealogy database (sejm-wielki.pl, person 4.285.619), with
  the standing rule for the ones that follow
  (`docs/LITERATURE_PLAN.md`, section 22) - one excerpt work per person
  (`minakowska2026<name>`), the whole page kept as the work's `full.md`
  knowledgebase and never shown, the editor's sections shown in full
  detail, **the database's estimated dates never in the edition's prose**
  (EDITORIAL_RULES, 2026-10-22), the documents first. With it the **person
  pages**: a page per person from the authored `reference/genealogy.yml`
  (who they are, their life dates, the family with the source of every
  fact, the documents, the literature), built by
  `pipeline/build/person_pages.py` after the website data and the index,
  layout `person`, both languages, linked from the People page; checked by
  verify_site.py. The pilot: /people/prusimski/
  (/de/personen/prusimski/), with the life-line 1744-ca 1806 (accepted;
  the "ca" open, NEEDS_CONFIRMATION). Read
  `literature/minakowska2026prusimski/notes.md` first. The database's
  pages are ISO-8859-2, not cp1250.
  (`literature/minakowska2026zielonacka/notes.md` first for the second:
  Helena Zielonacka, the Chełmski wife, saved in the database's ENGLISH
  user interface - the work's language is the saved page's own (section
  22), and her page /people/helena-zielonacka/ is the first **standalone**
  person page (`standalone: true` in `reference/genealogy.yml`: her own
  heading and bio, no documents, the literature named by hand). The
  database's Boniecki-derived IDs (2.976.*) are entries of the online
  Boniecki - check them against the edition's works. The database's
  pages are ISO-8859-2, not cp1250.
  (`literature/minakowska2026miaczynski/notes.md` first for the third:
  Stanisław Adam Miączyński, the edition's `miaczynski` - the marriage
  act of 17 August 1810 the page cites against the edition's "about
  1814" inferred from the letters of 1815: NEEDS_CONFIRMATION, the
  entries unchanged until the editor rules; his page /people/miaczynski/
  is the first genealogy block hanging on an entry of the edition. The
  page has a Rodzeństwo section the selection does not bring in. Beware
  duplicate YAML keys in `literature/index.yml` - a second key of the
  same name silently shadows the first; merge instead.)
  (`literature/minakowska2026ottotrampczynski/notes.md` first for the
  fourth: Wojciech Otto-Trąmpczyński, the sixteenth-century man of the
  Trąmpczyński family, the database's "sw." number (a Teki Dworzaczka
  regest number - the person came from a regest, which is the page's one
  source). Two pipeline lessons recorded: an `only_in` person's
  literature hits need the index dedup to ask `applies()` (fixed
  2026-10-22), and a standalone block's slug must not be an entry's slug
  (the collision renamed before commit).
- **The newspapers** (`newspapers/`, added 2026-10-22, **committed, not
  published**): the editor's third section for newspaper articles, "since
  it doesn't really fall under archival sources or literature" — neither
  holdings nor literature; plan in `docs/NEWSPAPERS_PLAN.md`. Four items:
  the "Z Zagórowa" column of Dziennik Poznański R. 79, nr 180 (7 August
  1937) — three municipal notes, transcribed line by line from the clipping
  by OCR with **no paid run** (Tesseract 5.5.3 + Polish models installed at
  the editor's word, `pipeline/ocr.py`; five passes in agreement; thirteen
  words ruled on a spot sheet; `newspapers/dziennikpoznanski19370807/notes.md`)
  — and **the Kuryer Polski's funeral report of 1754, moved here from the
  Sources page at the editor's word** (the edition counts 619 documents in
  46 holdings; the old /documents/ addresses redirect; the timeline's event
  of 1754 links the item) — and **the Ostdeutscher Beobachter's feature on
  Łazińsk of 19 July 1942** (`ostdeutscherbeobachter19420197`, added
  2026-10-22): the NSDAP's daily for the Warthegau on the "purely German
  settlement" of Lazinsk in the Amtsbezirk Drommin, the wartime name of the
  Trąbczyn commune, signed Willi Spatz; the transcription and Claude's
  English came with the editor's file ("the transcription is secure" — no
  reading against the page), the editor ruled the English Claude's for the
  caveat and the item shown whole with the rights not flagged; its Lazinsk
  is Breyer's Łazinsk (the same teacher Mielke, APP 53/968/0/-/669), its
  founding date of 1718 stands against the edition's records, and the
  editor's identifications of 2026-10-22 are worked in (Drommin = Trąbczyn;
  Lazinsk = the German-era name of Łazińsk, the colony the register records
  as Trąbczyńskie Stare Olędry; the forms matched and ruled)
  — and **TwojaSłupca's report of the jubilee of 6 July 2015**
  (`twojaslupca20150706`): the first item of the press from the web, the
  portal's HTML as printed, nothing tidied; shown whole at the editor's
  word (the press of 2015 under copyright), **no picture**; its history
  paragraph is the edition's own documents' story (the KDW's 1240 grant,
  Janek son of Szymon and count Mikołaj of the charter of 1276, Jan and
  Przedpełk of 1346); Antoni Prusimski ruled to the Starost, the report's
  Miączyński heirs ruled out (NEEDS_CONFIRMATION); the slug's date stands
  in the issue's place.
  The editor's rulings of the day are worked in:
  the clipping's source (the blog Zagórów w historii, its post of 2 October
  2024), the rights approved, the clipping and the Kuryer's page carried on
  the item pages, and **the index of people and places run over the items**
  (`pipeline/newspapers/newspapers_index.py`; 42 hits all ruled in
  `newspapers/index.yml`; the "In the newspapers" boxes on /people/ and
  /places/; Głowiecki stands on /people/ with no documents). Open: the
  Oleśnica identification, the 1718 of the 1942 article, the 2015 report's
  Miączyński heirs (NEEDS_CONFIRMATION). Not
  published.
- **The parish's own chronicle** (`luteraniezagorow`, added 2026-10-22,
  **committed, not published**): the page "Zagórów filiał Parafii
  Ewangelicko - Augsburskiej w Koninie" on Luteranie Konin
  (luteranie.konin.pl), the Konin parish's website — "Ważniejsze
  wydarzenia z życia Parafii w Zagórowie", a chronicle in dated entries
  from the Reformation among the monks of Ląd in the sixteenth century to
  the closing of the Evangelical Senior Citizens' Home in 2009, the
  section's first item from a parish website and its first with no date
  anywhere (the site's footer reads © 2011; the page stands as of about
  2015 by its own menus). The editor's rulings of the day: worked on a
  **separate branch from main** (other work being done there); shown
  whole (the rights approved), **no date in the slug** — the plan's rule
  for a web item given a recorded exception, the footer's 2011 kept as
  the list's sort year alone — **no era** (the `era:` field left out for
  the first time), **no picture** (the page's two church photographs and
  the small-print photographs line, Foto Sypniewski, stay off). Read from
  the page's HTML, nothing tidied: the page's line breaks inside its
  paragraphs kept; the paste's "Kościół Ewangelicko-Augsburski w
  Zagórowie" was the photographs' alt text, not prose. Index ruled
  (`newspapers/index.yml`): Zagórów (three spellings) and Grodziec (two)
  stand; "Lądu" and the Polish "Śląska, Pomorza, Prus" matched by no
  pattern (NEEDS_CONFIRMATION). Its bearing: Werner's Wreschen parish
  (the care from Września to 1817, entry 201) and Kneifel's church of
  1878-1896. Read `newspapers/luteraniezagorow/notes.md` first. Not
  published.
- **The Echo Tureckie clipping** (`echotureckie1931018`, added 2026-10-22,
  **committed on its own branch, not published**): "Zajście w Zagórowie"
  in the Zagórów edition of the Turek weekly Echo Tureckie, R. 8, nr 18
  (6 May 1931), nr 379 — the clash at the recruiting commission of
  24 April: the workers' crowd stoning the premises when the quota ran
  out, the starosta of Słupca's police, the second storming, a dozen or
  more persons arrested. Anonymous, no signature and no siglum. From the
  blog **ZAGÓRÓW-MIEJSCE Z HISTORIĄ** (the editor's word for the title;
  the same post of 2 October 2024 the 1937 clipping came from). Read by
  four Tesseract passes (the Windows engine unavailable the day), six
  rulings on a spot sheet; the print breaks its words with printed
  hyphens, so the "¬" convention appears nowhere. Shown whole (the
  rights approved), the clipping carried. The item names nobody; the
  index's hits are Zagórów's forms, already ruled. Its bearing: the
  recruitment for Germany's violence six years before the 1937 column's
  routine. Read `newspapers/echotureckie1931018/notes.md` first. Not
  published.
- **Mielewczyk (2017)** (`mielewczyk2017`, added 2026-10-22, **committed, not
  published**): Wojciec Mielewczyk, "Zmiany przestrzeni wsi w drugiej
  połowie XIX i na początku XX wieku na przykładzie wybranych map ze zbiorów
  Muzeum Narodowego Rolnictwa i Przemysłu Rolno-Spożywczego w Szreniawie",
  *Z Dziejów Kartografii* XXI, pp. 41-57, on the changes in the rural space
  shown on the large-scale village maps of the Szreniawa museum. The
  editor's rulings: **visible, the figures skipped, a link to the article,
  the whole article** — the link is the open-access copy at maphist.waw.pl
  (the `scan:` of `work.yml`). Made from the editor's PDF by
  `pipeline/literature/mielewczyk_pdf.py` (the text layer's "fi" ligature
  and its stray space joined; the 19 notes on their pages; the captions of
  the fourteen figures kept as text, on four pages between two pieces of one
  paragraph); `--check` holds all 17 pages against the layer. Claude's
  English; the article's own English block of p. 57 stands as printed. The
  article bears on the edition's ground: **fig. 4 is the map of the dóbr
  Trąbczyn of 1861** with the field of the enfranchised peasants marked, and
  p. 48 names **Kolonia Łazińskie and Kolonia Huta** on the parcelled lands
  of Trąbczyn — the edition's Staro- and Nowo-Łazińska colonies, which the
  article does not say. Copyright the Institute's (2017), no open licence;
  the Licences page not changed. Index: 17 mentions, all ruled; the
  article's "Kolonia Łazińskie" is ruled (the editor, 2026-10-22: a variant
  of Łazińsk/Lazinsk — the Stare colony) and matched as a variant of
  `trabczynskie-stare-oledry`. No hand-made links yet. `docs/LITERATURE_PLAN.md`,
  section 21; the work's `notes.md` first. The literature has 25 works, 23
  on the site (two summary-only).
- **Janocki (1779)** (`janocki1779`, added and **published 2026-10-21**): the
  entry "Stanislaus Lochowski" (LXXVII, pp. 159-160) of the *Ianociana* II
  (Warsaw and Leipzig 1779), which says Paciorkowski's handbook is Lochowski's
  *Processus iuris limitanei* of 1641 printed under Paciorkowski's own name —
  the editor asked for it attached to Paciorkowski (1776). **The first
  sub-item**: `parent: paciorkowski1776` in its `work.yml`; the Literature page
  shows it inside Paciorkowski's section, Paciorkowski's page carries the note
  (Janocki's words, with a link), and the citation of the parent work now
  reads "Paciorkowski (1776) [= Lochowski 1641]" (the bracket's wording chosen
  without the editor; TODO asks). Built from the editor's PDF (title page and
  the two pages; not kept in the repository); the entry runs to p. 161, the
  extract stops at 160. The doubtful reading "Miedzyborze" and the
  transcription wait on the editor (NEEDS_CONFIRMATION).
  `docs/LITERATURE_PLAN.md`, section 18; the work's `notes.md` first. The
  literature has 22 works, 20 on the site.
- **APP 53/1455/0/2/21** (`app5314550221`, added and **published
  2026-10-21**): six pages (13, 14, 25, 26, 66, the archive's pencil
  numbers, and 15, added at the editor's word) of the eighteenth-century copy-book of the privileges of the
  abbey of Ląd, fond Klasztor cystersów w Lądzie: six Latin documents, the
  exchange of 1362 that gave Ląd the forest where Drzewce was founded, the
  purchase of three mansi of Łukom with the forest of Grądzyń, confirmed
  by the king in 1447 (no. 16, the year written over) and resigned in 1461, the
  boundary of Makownica in 1399, a beginning (no. 26; no photograph of
  p. 27), and p. 66 of the boundary
  decree of 1761 (Łukom, Zagórów, Drzewce). Cut from the editor's raw
  photographs (pp. 13 and 25 below the entry before, at the editor's word),
  read, translated, summarised and claim-checked in session; a new
  set-apart kind for a note in the margin (`margin_notes.yml`). Read
  `units/app5314550221/notes.md` first. The copy's "Gradziem" is Grądzyń
  (editor, 2026-10-21). Published at the editor's word ("Push to main and
  rebuild"). Still open: the overwritten year of no. 16 (read 1447), the
  hand of the margin note on p. 14.

- **Works kept off the site get a summary page** (the editor, 2026-10-21:
  "For each literary source that you don't publish on the site, include an
  entry with a detailed summary of its contents"). A work with
  `visible: false` is listed on the Literature page and its page holds only
  `summary_en`/`summary_de` from its `work.yml`, written by Claude from a
  reading of the whole work; `literature_site.py` stops on one without
  them, and `verify_site.py` checks that no stretch of its text is on the
  site. Two such works: **Seidel (2018)** and **Pinkas Hakehillot (1976)**
  (`dabrowska1976`, added 2026-10-21: JewishGen's English of the entries
  Zagórów, Pyzdry and Konin, kept as Seidel at the editor's word).
  **Published 2026-10-21**, with Drommin and the Ląd copy-book.

- **Karwowski (1900)** (`karwowski1900`, added and **published 2026-10-21**):
  "Klasztor pp. cystersek w Ołoboku", the first article of Roczniki TPNA
  T. XXVI (pp. 1-114), a history of the Cistercian nuns' convent at Ołobok.
  Only the two paragraphs of p. 87 the editor named are brought in, with
  their footnote, read from the WBC digitisation (DjVu id 118639; the files
  not kept), the image checked at 300 dpi and word-level zooms, the scan's
  text layer only as a check. Out of copyright (author d. 1917). Index
  ruled; three identifications open (Trzciński, Weygel, Sobolewski —
  NEEDS_CONFIRMATION). `docs/LITERATURE_PLAN.md`, section 19; the work's
  `notes.md` first. The literature has 22 works, 20 on the site.

- **Frost (2007)** (`frost2007`, added and **published 2026-10-21**): the
  nobility of Poland–Lithuania 1569–1795, the survey chapter from H. M.
  Scott (ed.), *The European Nobilities*, vol. II (2nd ed., Palgrave 2007),
  pp. 266-310, read from the editor's PDF spread by spread from page images
  (the scan has no text layer; not OCR), doubtful spots settled at 300 dpi.
  The chapter's notes are endnotes, kept on their printed pages so a note
  can be cited to its page. Under copyright: put in with `visible: false`
  like Seidel, then given a page the same day at the editor's word ("Give
  it a page - I'll need to decide later what gets displayed"); what the
  page displays is their later decision (NEEDS_CONFIRMATION). The guides
  in the PDF are not to be added (their word: "Don't add the guides from
  the PDF"). Index ruled: the Radziwiłłs, "Florian" (Hieronim Florian) and
  "Augustus" (Augustus II) are not the edition's; Repnin (p. 299, the
  Russian ambassador) is ruled to the letters' Prince Repnin, which the
  editor confirms. The work's `notes.md` first. The literature has 20
  works, 19 on the site.

- **Encyclopedia of Camps and Ghettos (2012)** (`dean2012warthegau`, added
  2026-10-21, **published 2026-10-21**): the USHMM encyclopedia's Warthegau
  chapter, only the pages the editor named (the introduction; Chocz,
  Grodziec, Kalisz, Konin, Rzgów, Zagórów), for the twentieth century.
  English as printed (CC BY-NC-ND: no translation); made from the JSTOR PDF
  by `pipeline/literature/warthegau_pdf.py`, every letter checked. The PDF
  is not in the repository (its feet carry the download's internet
  address). How much bears on the edition is open. The work's `notes.md`
  first. **Grodziec and Rzgów** were added as places at the editor's word
  (Rzgów an estate in focus on KDW 4 and 6 and Konin Gr.117, docs 11 and 12;
  Grodziec not, no document being about it: NEEDS_CONFIRMATION asks).

- **Boniecki (1900)** (`boniecki1900`, added and **published 2026-10-21**):
  the Chełmski family's branch that held Łukomia, from the editor's saved
  page of the online Boniecki (only items 2.976.162-240, at the editor's
  word: Stanisław, Heliodor, the transfers of Łukom). Cut at item numbers;
  Claude's English; four links. Two differences from the documents
  (settled) and one reading of Claude's waiting on the editor
  (NEEDS_CONFIRMATION). The saved page is not in the repository (the
  editor's login is in its header). The work's `notes.md` first.

- **Chodyła (2015)** (`chodyla2015`, added and **published 2026-10-21**):
  the history of the 58 Olęder settlements of the Pyzdry Forest 1746-1793,
  the Trąbczyn colonies first among them. The text is made from the book's
  PDF in the editor's Books folder (`pipeline/literature/chodyla_pdf.py`),
  not from the editor's Word file, and checked against it word by word;
  Claude's English (the editor's machine English read and not used); 39
  pages of pictures. Five details differ from the documents
  (NEEDS_CONFIRMATION, settled: the documents are taken). Six hand-made
  links to the court books and tables it cites. `docs/LITERATURE_PLAN.md`,
  section 13; the work's `notes.md` first. The literature has 17 works, 16
  on the site. Wąsicki (1953) was published with it.

- **Wąsicki (1953)** (`wasicki1953`, added 2026-10-21, **published 2026-10-21**):
  the article on Prussian colonisation in South Prussia 1793-1806 from
  Przegląd Zachodni, read from the scanned PDF, Claude's English, the
  sideways table and the plans as pictures. It names the Zagórów and
  Trąbczyn estates and the 1805 colonies (pp. 174-176, from Breyer).
  `docs/LITERATURE_PLAN.md`, section 12. Offered: a link to the lease of 1806.

- **Three more works of the literature** (2026-10-20, **published 2026-10-20**):
  Pachoński (1973) on the Polish emigrés at Venice (its note 10 names the
  Starost), Mączak (1968) on the grain export 1550-1650 (in English), and
  Szwiec (2009), the catalogue of the Olęder architecture of the Pyzdry
  Forest with its photographs. Pachoński and Mączak were first built as
  holdings by a desktop session that had not fetched the cloud's work; the
  editor: **literature has its own page, and the Sources page is for primary
  sources from archives**. **The Literature page lists the works by author**
  (surname first, title, English title in italics, published, language;
  `author_sort`). A work can show pictures (`figures`). **"Nowa Wieś" is a
  common place name: a link must be sure it is the Trąbczyn estate's**
  (editor). The edition has 613 documents in 45 holdings and 14 works of
  literature. `docs/LITERATURE_PLAN.md`, section 11. Published at the
  editor's word. Open: the editor's view of how useful Mączak and Szwiec are.

- **The literature** (begun 2026-10-19; **published 2026-10-19** at the
  editor's word; a second set of six works added and published the same
  day):
  six books about the sources, original and English (Claude's), in
  `literature/`, cut page by page into `corpus/literature/` by
  `pipeline/literature/build_literature.py`, and shown at /literature/ by
  `pipeline/literature/literature_site.py` (both steps of regenerate.py).
  Plan, layout and next steps: `docs/LITERATURE_PLAN.md`; each work's
  `notes.md` first. Seidel (2018) stays off the site (`visible: false`,
  editor; verify_site.py checks it). The index of people and estates over
  the passages is built (plan, section 8): every hit read and ruled in
  `literature/index.yml`, an "In the literature" list on /people/ and
  /places/; the editor accepted Claude's five identifications. The first
  hand-made links are built (plan, section 9; `literature/links.yml`):
  four, from the black register to ten documents, each with a sentence
  saying why, shown under the passage and beside the document. The
  general "Ruchts" of letter 103 is Rüchel (editor, 2026-10-19): the scan
  reads "Ruchels", and the text is corrected
  (`units/oe1bu9454/intake/scripts/ruechel_103.py`). **The second set**
  (the editor's folder "Books_2", built and **published 2026-10-19** at
  the editor's word):
  Breyer 1935 (twice) and 1938, Żychliński 1885 and 1891, the PSB entry on
  Antoni Prusimski (1982); English Claude's, no German translation of the
  Polish works (an accepted gap, editor); indexed, and eleven more links
  written (plan, section 10). A work's page now shows one text at a time,
  the English first, with buttons for the original (editor). Waiting on
  the editor: the questions in NEEDS_CONFIRMATION
  ("The literature": Michalina's marriage 1809, her mother's death before
  December 1796, and others).

- **Kodeks Dyplomatyczny Wielkopolski** (slug `kdw`, built and
  **published 2026-10-16**): twenty-one entries,
  1173 to 1440, each a document, text only (the WBC has no page images),
  the whole entry from the editor's `intake/kodeks.txt`, never corrected;
  footnotes raised on the site (`footnotes.yml`); translated, summarised
  and claim-checked in session; status `translated`. A new era `medieval`
  (working name), on the timeline from 1173 and the story page. Imielno
  was added to the estates of focus at the editor's word. The edition has
  613 documents in 45 holdings. Only the era's name is open. Read
  `units/kdw/notes.md` first.
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
  editor's word: APŁ 39/98/0/-/6603 and APP 53/968/0/-/716 (below). Two
  eras carry working names until the editor names them: `wlodzimierz` and
  `twentieth-century` (`reference/eras.yml`). The era `liquidation` was
  made one with `wlodzimierz` (editor, 2026-10-20); Claude's proposed names
  for all the eras wait on the editor (NEEDS_CONFIRMATION, "The eras").
- **APŁ 39/98/0/-/6603** (slug `apl399806603`, added and published
  2026-10-15), the first holding from the State Archive in Łódź: the
  liquidation table of the Łazińsk colony (1868), its copy (1869) and the
  entries to 1901, six documents, three of them tables; openings joined into
  one page by cut edges (`EDGES` in its `holding.py`). It and Breyer's copies
  of the tables in -/716 stood in the era `liquidation`, since 2026-10-20
  in `wlodzimierz` (editor). Read `units/apl399806603/notes.md` first. The editor
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
- Glossary live: 111 entries (2026-10-14; Matura added
  at the editor's word). 55 checked: the
  patrimonial court (the editor's Szukaj w Archiwach source) and 54 read
  against Krünitz, Adelung, Grimm and Gloger. The other 56 wait on works not
  online here, or have no entry in those that are (NEEDS_CONFIRMATION).
  **Gród** (the municipal court) and **stawisko** (the noun, not the name
  Stawisko) added 2026-10-21 from Arct's dictionary on Wikisource, which
  the editor named (113 entries, 128 words ruled out); **published 2026-10-21**. The editor means to add more definitions from it.
  **Komornik** split in two at the editor's word (Gloger, 2026-10-21,
  **published** with another session's push the same day): the court officer (Latin camerarius) and the lodger
  (`komornik-lodger`, marked only in its six documents by `only_in`); and
  **kopiec**, the boundary mound (Gloger "Kopce graniczne", with the
  documents' own account of 1775 and 1782); and **pisarz**, the court
  clerk (Gloger "Pisarze"; the Latin notarius terrestris of the court
  books, not the notary public); 116 entries, 60 checked.
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
