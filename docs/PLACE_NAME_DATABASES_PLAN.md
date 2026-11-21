# Plan: the place-name databases against the gazetteer

Status (2026-11-21): **steps 1 to 5 done, step 6 open.** Agreed with the
editor 2026-10-24, the rulings of section 8 in the same day. Steps 1, 2 and
4 were made on the branch `place-name-sources` (24-25 October); steps 3 and
5 were done on `main` on 26-27 October: the editor answered the match sheet
(126 decisions), the Nazwy miejscowe and Słownik facts were cited for 46
places, the two dictionaries entered as literature works kept off the site
(`literature/nmpol`, `literature/slownik`), four places added, and the match
log committed. The branch's own work reached `main` on 2026-11-21 at the
editor's word: the ten Kodeks entries (documents 22 to 31 of `kdw`), this
plan and `pipeline/gazetteer/match_sources.py`; its Places-page grouping (Ląd
and Świątniki with the area) had already been carried over by the tiered
Places index. The branch was then deleted. **Step 6** (2026-11-21): the
candidate sheet is built and waits on the editor
(`pipeline/gazetteer/candidates_sheet.py` ->
`review/place_name_sources/candidates.html`). The Słownik's gmina
paragraphs give area and population only, not the gminas' villages, so the
candidates came from every entry that names the parish or gmina of
Trąbczyn or Zagórów (an OCR-tolerant search of all 16 volumes: 78 marks in
65 entries), read by two Sonnet readers and checked by Claude, with the
estates' own lists of their parts (Trąbczyn, Łukom, Kopojno, Oleśnica).
14 places and features are new to the gazetteer; the rest are its places
under other spellings, recorded on the sheet. The editor then widened the
scope (2026-11-21: "Yes, read the Słownik around the others as well"): the
parishes of Rzgów, Pyzdry, Stawiszyn and Zbiersk and the gmina of Grodziec,
around the gazetteer's places that lie outside the two parishes - 72 more
entries (powiat słupecki, koniński or kaliski; the Rzgów of powiat łódzki
left out), 64 places new to the gazetteer, section E of the same sheet
(`pipeline/gazetteer/candidates_outlying.json`). The decision page and the
translations of the snippets stay out of the repository
(`review/place_name_sources/`, two of the three works in copyright).

The editor, 2026-10-24, on the three Polish reference works converted in
Igor's repository (`polish-place-name-sources`, now holding the full text of
all three): the facts from them are to be stated **in the editor's own voice
and cited accordingly** — not copied word for word from the dictionaries.
The text on the site stays prose in the editor's style; the databases are
where the facts come from and what every sentence rests on.

## 1. The three sources, what each gives

The converted text is at `C:\Users\Tersnaus\Downloads\polish-place-name-sources\`
(a clone beside this repository; private, two collaborators, see its
`RIGHTS.md` — reading, searching and citing with a normal citation is what it
is for).

| Source | What it gives the gazetteer | Text quality | Cited as |
|---|---|---|---|
| **Nazwy miejscowe Polski** (IJP PAN, 18 vols, 1996–2025) | the meaning of a name (etymology), every recorded historical spelling with its date and its printed source, the administrative location | vols 10–18 born-digital, quotable as read; vols 7–9 a modern scan's text layer; vols 1–6 the 1990s OCR — every character intended for a citation is read against the recovered layer (`nmpol-recovered/`) and the scan | Rymut (red.), *Nazwy miejscowe Polski*, t. N, s. P (the page anchors `<!-- p.NNN -->` give the printed page) |
| **Kodeks dyplomatyczny Wielkopolski** (T.1–11, 4,843 charters) | the medieval record: first mentions, old spellings, the transaction behind a charter, the editors' identifications of places | the publisher's own HTML text, quotable as read | already in the edition: the `kdw` source key, a locator of volume and number; entries not yet in the edition are plain citations until they are brought in |
| **Słownik geograficzny Królestwa Polskiego** (1880–1902, 15 vols in 16 parts) | the state of a place about 1880: houses, population, confessions, parish, gmina, school, post office, mill, distillery, owners, neighbours, distances; the gmina and parafia tables name the surrounding villages — where the candidates come from | the digitising institution's OCR of 1880s print — check the page image before quoting a decisive word | volume and page, by the file's page anchors (the anchor before "Trąbczyn" in t. XII is p. 448, matching the editor's own citation of pp. 448–449) |

**NMPol stops at Ś** (t. 18, 2025; the series is still appearing). The names
beginning T–Ż — Trąbczyn, Tarszew, Włodzimirów, Wrąbczyn, Wymysłów, Zagórów,
Zalesie, Zwierzyniec and the rest — get no NMPol entry until later volumes;
they rest on the Słownik, the Kodeks and the edition's documents. About half
the 112 places are in covered letters.

## 2. Precedence and voice

- **The documents first** (HOUSE_STYLE): every fact is first looked for in
  the edition's own documents. The databases are brought in for what the
  documents do not say — chiefly the name's meaning and its older spellings
  (NMPol, KDW), and the state of the place in the 1880s (SGKP). Where a
  dictionary disagrees with a document, the document stands and the
  difference goes to NEEDS_CONFIRMATION ("The gazetteer"). The same for a
  dictionary's own slip read against the documents (the Słownik's
  "Przemyśław" for Przemysł at Trąbczyn).
- **The voice** (`docs/EDITORS_VOICE.md`, "Index entries"): the additions
  follow the order of the editor's own entries and their formulas — the name
  where it has a meaning ("The name is an adjective for beech trees
  (*Buk*)"), the history in time order with the first mention and its
  spelling ("First mentioned as *X* in a YEAR document where ..."), the
  Słownik's facts as dated sentences ("The Geographical Dictionary of the
  Kingdom of Poland in 1892 stated that ..."), the maps last as a chain.
  Nothing is copied from the dictionaries' own sentences; each fact is
  restated and carries its citation.
- **No method talk on a page** (the editor's rule): the additions read as
  part of the entry, not as a report on sources consulted. The credit for a
  fact is the footnote.
- The editor's own text is never rewritten: additions extend it. Where an
  addition would sit inside an existing sentence, the entry keeps the
  editor's order and the new material is placed after the fact it continues.

## 3. Matching a name to an entry (the homonym trap)

Built 2026-10-24 (`pipeline/gazetteer/match_sources.py`). A bare name is
not an identifier: the Słownik's "Łukom" search returns the Łukomski family's
estate near Orsha before ours. Every match is made on **name plus
administrative context**, and each candidate is recorded in
`pipeline/gazetteer/source_matches.yml` (locator, whether its own text names
our ground, the editor's decision):

- the search forms: the entry's heading, its recorded names (Trąbczyn's
  *Trampczino*, *Trupcino*, *Tropcssino*…), its aliases, and the register's
  variants, ascii-folded for the OCR;
- the qualifying context read in the candidate's own text: SGKP's
  `pow. słupecki`, `gm. Trąbczyn`, `par. Zagórów`; the neighbours (Ląd,
  Pyzdry, Konin, Rzgów…); NMPol's gmina and voivodeship;
- the two dictionaries show two kinds of row: **entry** (the work's own
  headword) and **mention** (the name inside another entry — the gmina and
  parish tables, which are also where the candidates of step 6 come from);
  mentions without our context are dropped as noise, and a form that floods
  the dictionary (Laski: hundreds of hamlets; Mały: the adjective) must
  show our ground to stand at all;
- the decisions: yes / no / unsure, recorded on the decision page and
  applied with `--apply`; a row already cited by the entry's footnotes is
  pre-decided yes ("already cited"), a Kodeks charter in the edition but
  not yet cited is left to the editor.

The decision page (`review/place_name_sources/match_log.html`, generated,
not committed — two of the three works are in copyright and the
repository is public) shows every candidate with its snippet, its context
verdict, a link where the charter is already a document of the edition,
and the three buttons; it keeps the work in the browser between reloads
and its Save button gives `match_decisions.json` for `--apply`.

## 4. What an entry gains

Per place, in the order of the editor's entries:

1. **The name** (NMPol, where the letter is covered): its meaning, in one
   sentence in the editor's formula; where NMPol gives several derivations,
   the contested ones are named as contested.
2. **The older spellings** (NMPol's attestation strings, and KDW where the
   entry's first mention is earlier or differently spelt than the editor
   records): dated, in time order, each with its citation. An attestation
   that only names a different place of the same name is not brought in
   (section 3).
3. **The Kodeks entries not yet cited**: where a charter mentions the place
   and the entry's footnotes do not cite it, it is proposed as a footnote —
   and, where the edition is to bring the entry in (the ten in
   `docs/MISSING_SOURCES.md` are already wanted), as a document link.
4. **The state of the place about 1880** (SGKP): population, houses,
   confessions, the institutions, the owners, the land of the estates —
   as dated sentences ("The Geographical Dictionary of the Kingdom of
   Poland in 1892 stated that ..."), the form the editor already uses.
5. **The first mention**: where a database's first recorded mention is older
   than the entry's, it is proposed — with the note that the edition's
   documents remain the authority where they speak.

Nothing is added about the twentieth century from these sources: they stop
at 1902 (SGKP), 1399 (KDW), or their publication year (NMPol, which carries
no place history after its attestations).

## 5. The citation mechanics

- `reference/gazetteer_sources.yml` gains a key **`nmpol`** (cite, kind
  `dictionary`, resolve by tome and page) and the existing **`slownik`**
  key gains its resolution (by volume and page, the Słownik text not in the
  edition as a holding unless the editor rules otherwise). A footnote
  citing either is then linked to the page's source on the site — or stays
  a plain citation where the work is not shown.
- **What appears on the public site** (ruled 2026-10-24): the facts in the
  editor's sentences with their citations; **no entry text reproduced** —
  not of NMPol or KDW T.6–11 (in copyright), and not of the Słownik either
  (public domain as a work, but the digitisation's terms were never
  confirmed, and its entries are far more than a site page needs). This is
  the same shape as the book's own rule: quote and cite, do not reproduce.
- OCR care: a quoted word from SGKP, or from NMPol vols 1–9, is checked
  against the page image (SGKP: dir.icm.edu.pl; NMPol: RCIN) before it goes
  on the site; the check is recorded in the match log. KDW and NMPol
  vols 10–18 need no such check.

## 6. The steps

1. **The frame** (this file; the branch): agreed shape, the rulings of
   section 8 in.
2. **The match log built** (2026-10-24; the count corrected 2026-10-25):
   all 112 places run against the three sources — Kodeks 444 charters (53
   already cited by the entries, pre-decided), Słownik 703 rows (463 with
   our ground named in the candidate's own text), Nazwy miejscowe 826 rows
   (262 with; the series stops at Ś, so T–Ż names have no entries). 32
   places, chiefly the Trąbczyn-compound and colony names, have no
   candidates in any of the three works. The decisions are the editor's,
   on the review page — which since 2026-10-25 shows each candidate's
   English first, the original folded beneath.
3. **The proposal sheet** (`review/place_name_sources/proposal.md`),
   from the decided log: per place — the entry's text as it stands, the
   proposed sentences in the editor's voice with their footnotes, the
   sources each rests on, and the conflicts flagged for
   NEEDS_CONFIRMATION. **No file of the site changes until the editor has
   ruled on the sheet.**
4. **The outstanding references brought in** (done 2026-10-24): the ten
   KDW entries are documents 22 to 31 of the holding, full intake, the
   footnotes links.
5. **The additions applied** (only after the editor's ruling on the sheet):
   the gazetteer YAMLs edited by hand, the sources file extended, the
   German written to the same voice, `gazetteer.py --check` and
   `--missing` run, MISSING_SOURCES and NEEDS_CONFIRMATION updated, the
   changelog written, all committed on this branch.
6. **The candidates** (`docs/GAZETTEER_PLAN.md`, step 7's list the editor
   asked for): the Słownik's gmina and parafia tables of the area read
   whole, the places named there checked against the 112 slugs and the
   register's 203 places, and the remainder — a village, hamlet, colony or
   feature of the Trąbczyn/Zagórów ground the edition does not yet carry —
   presented as a list for the editor to accept or refuse, one line of what
   the sources say about each. **Scope, ruled 2026-10-24: the parishes of
   Trąbczyn and Zagórów only**, and beside them any names in the editor's
   own list which fall outside those areas are carried into the review, so
   nothing the editor has listed stands outside the process.

## 7. What this plan does not do

- It does not touch the editor's own text (only adds after it), the
  register's identity data, or the maps.
- It does not bring the texts into this repository: the databases live in
  Igor's repo, read from there; nothing is copied in but the citations.
- It does not publish anything: the branch stays unpushed until the editor
  says so, like the gazetteer.

## 8. The editor's rulings (2026-10-24)

1. **The base**: settled — the gazetteer and the maps are merged to `main`
   (2026-10-24), and this branch stands on that `main`, so the 112 entries
   are its input.
2. **The site and the sources**: the Słownik contributes **facts with
   citations only** — no entry of it is reproduced or brought in as a
   holding. The same for NMPol. A fact's citation is a footnote in the
   entry's own style; where the digitised page is stable it may link to it
   (dir.icm.edu.pl for the Słownik, RCIN for Nazwy miejscowe).
3. **The ten Kodeks entries**: **added to the site like the other ones** —
   the full intake of the `kdw` holding: the whole entry as the text,
   transcribed from the WBC HTML on the editor's drive and checked against
   Igor's independent conversion, the English, the summaries, the claim
   check, the era `medieval`, the footnotes, the timeline. They are
   documents 22 to 31 of the holding, in date order with the existing 21.
4. **The candidates' scope**: **the parishes of Trąbczyn and Zagórów
   only**, and, beside what the Słownik's tables name there, any names in
   the editor's own list of place names which fall outside those areas are
   included in the review, so that nothing the editor has listed stands
   outside the process.
5. **The voice of the additions**: **no "Claude's addition" marker** and no
   preamble about the AI process on any page — the additions read as part
   of the entry, every fact cited by its footnote (the editor, 2026-10-24:
   "any preamble/info about the AI process should be silent"). What is new
   is seen in the proposal sheet before anything is applied. This rules
   down the "marked as Claude's addition" of GAZETTEER_PLAN, step 7.
