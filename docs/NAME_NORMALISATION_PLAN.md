# The Pełzucki 1896 names: normalisation plan

The liquidation table's names are Russian renderings of German and Polish
names — Вильгельмъ Кинастъ is Wilhelm Kinast, Стржижиковскій Фр. is a
Strzyżkowski Franciszek. The map's farm table (and the pills) currently
show a Latin **transliteration** of the Cyrillic (`Vilgelm Kinast`), which
is faithful to the document but reads as neither German nor Polish. This
plan adds an editorial **normalised rendering** (`name_norm`) beside the
documentary form, with an explicit language tag, evidence note, and
confidence per row, and answers first the question the editor asked: are
the readings themselves sound?

## 0. What the sources are

Every name in the table stands behind **up to four independent witnesses**,
all already joined by farm number (scratch/map4456/link_tables.py,
oleders_linked.json):

| witness | document | what it is |
|---|---|---|
| A (1868) | APL 39/98/0/-/6603-1 | the original liquidation table |
| B (1869) | APL 39/98/0/-/6603-2 | the governorate copy, another hand |
| C (Breyer) | APP 53/968/0/-/716-4 | Albert Breyer's 1930s copy of the 1868 table (from a Słupca copy), with his 1875 pencil notes of who held each farm |
| D (1896) | APL 39/98/0/-/6603-6 | the survey statement, the map's own source |

A and C are two different physical documents of the same 1868 table; B is
a contemporary copy; D is thirty years later. Agreement between A/B/C is
therefore real corroboration, not a single hand repeated.

## 1. Are the readings correct? (collation of 2026-11-05)

Row-by-row collation of A, B, D (the three the pipeline parses):

- **61 of 97 rows: all three agree exactly.**
- **36 rows diverge.** Most divergences are transliteration style (B
  writes *Krishtof* where D writes *Kristof*, *Martsin* vs *Martin*) or
  Russian grammar (the genitive *Rungi/Rungě* for the surname Runge) —
  no bearing on the reading of the name itself.
- The divergences that are **real findings**:

| row | A (1868) | B (1869) | C (Breyer) | D (1896) | what to rule on |
|---|---|---|---|---|---|
| 77 | Khaupt Gotfridov Kristiian | same | same | **Gebel Kristiian** | D alone says Gebel; three witnesses say Khaupt (Haupt). Either the 1896 clerk erred, or the farm changed hands — the table's own inscriptions (doc 4/5) may say. The join currently carries D's reading. **Highest-priority ruling.** |
| 12 | Slivinskii Gotlib | same | **Slivinskii Gotl.** plainly | [uncertain: Slivinskii] | C's plain reading lifts the doubt: three of four agree. The `uncertain` flag can be dropped. |
| 25 | Promist Shchepan | same | same | [uncertain: Promins] Shchepan | all four read the same uncertain word (Promist/Promins). Stays uncertain; normalisation carries the doubt. |
| 39 | Khaupt Frants Kristiian | same | — | Khaupt Kristiian | D drops the middle name. The fuller 1868 form should be noted, not lost. |
| 75, 76 | Khaupt Gotfrid Kristiian / Khaupt Kristiian Kristiianov | same | same | Khaupt Gotfrid / Khaupt Kristiian | D truncates the distinguishing middle names — two different Haupts share a first name, and only the middle name tells them apart (father/son). Normalisation keeps the full form in a note. |
| 44 | Rash Friderik Ivan | same | — | Rash Friderik | D drops Ivan (same pattern as 39). |
| 84 | heirs of Shtirtsenbekera Ivana | Shtirtsenbekera Ivana | Shtirtsenbekera Iv. | heirs of Shtirtsenbekera | D drops the given name of the deceased. Note the 1868 form. |
| 96 | Reikh Kristiian | Kristian Reikh | (blank) | Reikh Kristiian (with `..` marks in D) | a near-duplicate of row 72 (same name, 1896 columns dotted) — a second plot of the same man, or a clerical repetition. Worth one look at the scan. |

So the honest answer: **the readings are in good shape but not yet
adjudicated row-by-row.** Six rulings (77, 12, 39, 75/76, 44, 84, 96) fall
out of the collation immediately; the rest is style variance, already
correctly marked `changed: false`.

**Stage 1 of this plan is that ruling pass** (half a day): every
divergent row decided in the unit's `rulings.yml` pattern, the `name` /
`name_1868` fields corrected where a ruling says so, the `uncertain`
flags adjusted (12 down, 25 stays), and a scan glance for 77 and 96.

## 2. The normalisation itself

### 2.1 Data model

`farms.yml` gains, per row:

```yaml
- n: 19
  name: Stirtsenbeker Kristiian     # documentary transliteration - untouched
  name_1868: Stirtsenbeker Kristiian
  name_norm: Stürzenbecker Christian
  name_lang: de                     # de | pl - the surname's language
  norm_note: Stirtsenbeker → Stürzenbecker (documented Olęder family,
             SGGEE/Breyer); Kristiian → Christian (German given name)
  norm_conf: firm                   # firm | conjectural
```

Rules the schema enforces:

- `name` and `name_1868` are **never rewritten** — they are the
  transcription, the same class of text as the unit corpus.
- `name_norm` carries brackets only where the reading itself is unsure
  (`Prom[is?] Szczepan`), mirroring the source's uncertainty.
- Institution rows (92–95, 97) get Polish normalisations only
  (Wieś szkoła → `Szkoła wiejska`, `Cmentarz wspólny`, …) with `lang: pl`,
  or none where the phrase needs no normalisation.
- `norm_conf: conjectural` rows keep the documentary form prominent
  everywhere the norm is shown (see 2.4).

### 2.2 The rule set (mechanical first pass)

A builder script (scratch/map4456/name_norm.py) applies, in order:

1. **Given names from a fixed mapping table**, split by target language:

   - German: Vilgelm→Wilhelm, Kristiian→Christian, Kristof→Christoph,
     Gotfrid→Gottfried, Gotlib→Gottlieb, Karl→Karl, Frants→Franz,
     Genrikh→Heinrich, Mikhail→Michael, Avgust→August, Andrei→Andreas,
     Anton→Anton, Liudvik→Ludwig, Emanuil→Emanuel, Morits→Moritz,
     Veniiamin→Benjamin, Friderik→Friedrich, Samuil→Samuel, Ivan→Johann†,
     Ian→Johann†, Iakov→Jakob, Daniil→Daniel, Mateush→Matthäus†, Foma†
   - Polish: the same Cyrillic source names in their Polish equivalents:
     Vilgelm→Wilhelm (unchanged name), Voitsekh→Wojciech, Kristiian→Chrystian,
     Kristof→Krzysztof, Osip→Józef, Foma→Tomasz, Ian/Ivan→Jan, Iakov→Jakób,
     Daniil→Daniel, Mateush→Mateusz, Karl→Karol, Frants→Franciszek,
     Genrikh→Henryk, Mikhail→Michał, Avgust→August, Andrei→Andrzej,
     Anton→Antoni, Liudvik→Ludwik, Emanuil→Emanuel, Morits→Moritz(‡),
     Veniiamin→Beniamin, Friderik→Fryderyk, Samuil→Samuel,
     Stanislav→Stanisław, Shchepan→Szczepan, Martsin→Marcin

   † doubtful rows: `Ivan` stands for Jan, Iwan or Johann — resolved by
   the surname's language, flagged conjectural when the surname itself is
   undecided. `Foma` (Russian Тома/Фома) → Tomasz (Polish) / Thomas
   (German) — farm 78's Zelchak Foma is Polish, so Tomasz.
   ‡ Moritz is the German form; Polish records also used Moritz/Moryc —
   keep Moritz for both, no conjecture needed.

2. **Surnames by class:**

   - `-skii` → Polish `-ski`, with the stem de-russified by rule:
     Strzhizhikovskii→Strzyżkowski†, Konchinskii→Kończyński†,
     Sanikovskii→Sannikowski†, Slivinskii→Śliwiński, Bludzinskii→Bludziński,
     Shmigelskii→Śmigelski, Malinovskii→Malinowski, Shchepinskii→Szczepiński,
     Rogatskii→Rogacki, Marylskii→Marylski, Tarnovskii→Tarnowski,
     Przhistanskii→Przystański†
     († = several stems possible: Strzhizhik- is Strzyżyk- or Strzyż-,
     Konchin- is Kończ- or Końc-; the note records the choice and the
     alternative. Web evidence decides where it can.)
   - German surnames, restored spelling: Khaupt→Haupt, Shults→Schulz,
     Tselmer→Zellmer, Stirtsenbeker/Sturt-/Shtirt-→Stürzenbecker (one
     family, three transliterations), Runga/Goska→Runge/Goske (the Russian
     declension flattened), Reikh→Reich, Fogel→Vogel, Shtark→Stark,
     Girsh→Hirsch†, Gebel→Göbel†, Merts→Mertz/Merz†, Shtark†,
     Fridenberg→Friedenberg†, Falkenberg, Falk, Obst, Gotter, Marek (pl),
     Morits (70: given name as surname? row 70 is "Morits Gotfrid" —
     surname Moritz), Hermann/German (88: Германъ → Hermann†),
     Zeer→Zeer†, Bandzert→Banzert†, Rash→Rasch, Kitke→Kitke†,
     Betke→Betke, Rytamer→Rittamer†, Kun→Kuhn†, Kusman→Kussmann†,
     Lipelt→Liepelt†, Knafkus→Knaufkus†, Sheinfish→Scheinfisch†,
     Shteinbord→Steinbord/Steinbart†, Bitner→Bittner/Büttner†,
     Fetter→Fetter/Vetter†, Gerke→Gehrke, Khоlm→Holm, Zeer†.
     Rows marked † are the **conjecture class**: the minimal de-russified
     form is what the Cyrillic can prove (e.g. Gebel, Bitner, Fetter);
     the commoner German form (Göbel, Büttner, Vetter) goes in the note,
     and web evidence promotes it to `firm` only when an index of the
     right region and period shows it.

3. **Mixed rows**: German surname + Polish given name (Runga Voitsekh,
   German Voitsekh!) and the reverse are normalised per element — the
   surname's language chooses the given-name table, not the row.

### 2.3 Evidence, in order of weight

1. **The four witnesses** (section 0) — a reading agreed by A+B+C is firm
   as a *Cyrillic* reading; the Latin normalisation still needs rule 2.2.
2. **Breyer's own published work on these colonies** — he mapped and
   described exactly this settlement landscape (Karte der Deutschen
   Siedlungen in Mittelpolen, 1938; his Ostdeutsche Heimathefte articles;
   upstreamvistula.org carries transcriptions of his material). Family
   names in Latin script from Breyer outrank phonology.
3. **Regional genealogical indexes**: geneteka.genealodzy.pl (parish
   registers of Słupca/Strzałkowo/Białobłoty deaneries — these families
   married there), WTG Gniazdo forum threads on Olęder families,
   SGGEE indexes, Genealogy Indexer (German address books/gazetteers).
   A hit of the right surname in the right parish around 1850–1900 makes
   a form `firm`; a plausible form with no hit stays `conjectural`.
4. **Phonology and frequency** — only the fallback, always marked
   conjectural in the note.

The web-research stage is bounded: one search per undecided surname, one
verification hit to promote, no deep genealogical rabbit holes. Estimated
twenty-odd undecided surnames (the † list), a few hours.

### 2.4 Where the normalised name appears

- **The farm table** (site/_layouts/map.html): a second name column,
  "Proper spelling" (i18n key `map_farm_norm`), showing `name_norm`;
  the documentary transliteration stays the first column. Conjectural
  rows show the norm with a marker (asterisk + tooltip of the note).
- **The pills on the map**: switch to `name_norm` when firm — a map label
  is an editorial object, not a transcription. Conjectural rows keep the
  documentary form on the pill.
- **The DE text pane**: the table's German rendering can reuse
  `name_norm` for the German rows (and Polish for Polish ones) — it is
  the form the names' owners would have written.
- `pipeline/maps/map_pages.py` carries the three new fields through to
  the page data.

### 2.5 Process

1. **Ruling pass** (stage 1 above) — outcomes recorded, yml corrected.
2. Builder script drafts `name_norm`, `name_lang`, `norm_note`,
   `norm_conf` for all 97 rows; output is a **review sheet** (the
   faithfulness-review pattern: an HTML page of rows, current vs
   proposed, with a decisions export the editor fills in).
3. Editor rules each row (the sheet is sorted to put conjectural and
   divergent rows first); the export is applied by the builder.
4. Web evidence round for the surviving † surnames; promotions recorded
   in the same sheet.
5. Rebuild: `map_pages.py`, jekyll, `pipeline/verify_site.py`; the
   browser test for the new column (both pages, both languages' tabs);
   CHANGELOG + WORKING_NOTES entries.

## 4. Status (2026-11-05)

- **Collation complete** (section 1): 61/97 rows agree across all three
  parseable witnesses; 36 diverge (style/grammar, or the seven findings
  listed there).
- **Editor's rulings applied as firm**: **Gibel** (not Göbel) and
  **Bitner** (not Büttner) — seen in other records (2026-11-05).
- **Draft built**: `scratch/map4456/name_norm_draft.json` — all 97 rows
  with proposed `norm`, `lang`, `conf` (61 firm / 36 conjectural), note,
  and the four witnesses per row. The 36 divergent rows carry the
  witness readings inline.
- **Review sheet built**: `scratch/map4456/name_norm_sheet.html`
  (http://127.0.0.1:8779/scratch/map4456/name_norm_sheet.html) with
  filters for All / Conjectural (36) / Conflicts (1) / Witnesses differ
  (36).
- **Pending the editor**: the rulings of section 1 (rows 77, 12, 25,
  39, 44, 75, 76, 84, 96) and the conjectural confirmations. Row 77 is
  marked `conflict` in the draft and is the one real decision.
- After the editor's pass: apply to `farms.yml` (new fields only), then
  display (2.4), rebuild, verify. The web-evidence round (2.3) runs for
  whichever conjectural rows the editor wants promoted.

## 5. What this plan does not do

- It does not silently rewrite the transcription anywhere — `name` stays
  as read.
- It does not invent certainty: a surname the Cyrillic can spell two ways
  stays two ways in the note until evidence picks one.
- It does not treat Breyer's copies as a new transcription unit — his
  copy is a witness to A, and his pencil notes (the 1875 holders) are
  already in the join; this plan only reads his name column as a second
  witness, which the collation in section 1 now does.
