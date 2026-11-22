# The English of I. HA GR, Rep. 7 C, Nr. 421, and the same faults elsewhere

Plan written 2026-11-22 at the editor's word ("Make a plan for how to do this,
using Sonnet sub-agents where possible to reduce token use"). Nothing below is
done yet; each step says which model does it, under the rules in
WORKING_NOTES, "Sub-agents and token use". The holding's notes are
`units/ihagrrep7cnr421/notes.md`; its English is written by
`units/ihagrrep7cnr421/intake/translation/english.py`.

## What the editor found, and the cause of each

| # | The fault | Where | Cause |
|---|---|---|---|
| 1 | "Mazący" passed into the English | doc 6, the Polish bond's last lines (0014_a2) | the word was not read; the session kept it as written instead of reading the image again |
| 2 | "the Skarbnik" left in Polish | doc 6, the bond | no termbase entry for the office; the session kept it |
| 3 | "Zaro[Zosob?]ney" | doc 6, the bond's list of villages | the recognition model's reading, not settled |
| 4 | "ex Chirographo" (and "ex quo", "aliunde", "in solidum", "contractus antichreticus", "contra Fiscum", "ita conclusum eodem") kept in Latin with no sense given | docs 1, 4, 5, 6, 7 | the session kept the documents' Latin; HOUSE_STYLE, "English", says no Latin the reader has not been given |
| 5 | "4,980", "3,459", "3,426", "4,168": registry numbers given commas | docs 2, 3, 7 | `pipeline/numerals.py` groups every four-digit number above 1999 with no unit after it; registry numbers are not sums |
| 6 | The official's note in the margin of doc 1 came out as German fragments in English ("Es [sind?] [wir?] Acta [t?]orm[?] has the two in this Storstell[s?] ...") | doc 1, page 1 (0002_a2, 21 lines) | the note was never properly read; the session translated the unread fragments word for word, under its own rule "words still unread are kept as written" |
| 7 | Signatures not identified ("[?]llen[?][z?]", "[Willen?]", "[Signature]", "v. [?]") | docs 1, 3, 4, 7 | never compared with other signatures or with the state handbook |

## What is already known (Claude, 2026-11-22, from the edition's own documents)

- **The village is very probably Zarobna.** Nr. 12367 (Breslau, 14 October
  1830) lists the estate as "Trąbczyn, Osiny, Łazy, Nowawieś, Zarobna,
  Trąbczyner Hauländer" (corpus.txt, line 68), the same villages in nearly
  the same order as the bond ("Trąmpczyna, Nowey wśi, Ośin, wśi Zaro[...]ney,
  Łazow tudzież Hollendrow"). "wśi Zarobney" is the genitive of Zarobna. The
  editor's "F[a/o]ro[b?]ney" agrees in the b. Zarobna is in neither the
  register (`reference/places.yml`) nor the gazetteer. To be confirmed on
  the image (step 1).
- **"S. [N?]." under Prusimski's name is "S. N.", Starosta Nieszczewicki**:
  the boundary decree (Konin Gr.145) calls him "staroście nieszczewickiemu".
  **"S. W." after Chełmski's name is Skarbnik Wschowski**: the Konin
  register Gr.118 calls him "Skarbnikowi ziemi Wschowskiey", and his person
  entry has him as Treasurer of Wschowa. The English becomes "Starost of
  Nieszczewice" and "Treasurer of Wschowa".
- **"Mazący"** heads the line that copies the blank note itself ("___ WJM Pana
  Stanisławowi Chełmskiemu S. W. Blankiet na # 12,000"). A participle taking
  the dative fits ("Należący", due to); the image decides (step 1).
- **The note in the margin of doc 1** asks for files. Its legible words
  ("in dieser Storstell[s?]" = Vorstellung, the petition; "die ich in meiner
  v. T. Ets. v. Goldbeck mir zugestellten Saml[?] nicht finde", which I do not
  find in the collection His Excellency v. Goldbeck sent me; "aus dem
  arctio[?] ... zu erbitten", to be requested from the archive[?]) suggest
  the official could not find the two orders of September 1796 the petition
  cites, and asked for them. A reading, not yet a text (step 1).

## The steps

### 1. Read again what was not read (Sonnet readers, Claude settles)

All of the holding's 30 lines with a mark of doubt, the margin note of
0002_a2 and the bond's lines on 0014_a2 first.

- `scratch/nr421_reread/make_strips.py` (Claude writes it, 10 minutes; or a
  Sonnet agent to this spec): cuts each doubtful line from the page images at
  full resolution, three lines of context, twice the size; writes
  `scratch/nr421_reread/strips/*.png` and `rows.tsv` (page, line, transcription
  as it stands).
- **Two Sonnet readers, in parallel, independently.** Reader A blind: the
  strips and the language only. Reader B with the witnesses named: the
  Zarobna list of Nr. 12367, the titles S. N. and S. W., the petition's two
  orders of 14/16 and 17 September 1796, Goldbeck's name. Each writes a TSV
  (reading, confidence, letters seen) and names any strip it did not open.
- **Claude settles** where they disagree, by looking at the strip itself,
  never the whole page. Agreement of the blind reader with the witness is
  the strongest evidence; a reading only reader B gives stays a question.
- Corrections go into CORRECTIONS in `intake/holding.py`, each with its
  witness, as before; what stays unread goes on a short spot sheet for the
  editor.

### 2. The signatures (Sonnet builds the sheet and fetches the handbook, Claude identifies)

- **Sonnet, to a spec:** a signature sheet like Nr. 3709's
  (`units/ihagrrep7cnr3709/intake/signature_sheet.py`): every signature and
  paraph of Nr. 421 (0002_a2 under the decision, 0007_a2, 0016_a2, 0017_a2,
  the registry clerks' marks), beside those already identified in the
  sibling files: Goldbeck's paraph (Nr. 3709), Haugwitz and "A[lvensleben]"
  (Nr. 1414), the signatures of Nr. 3067 and Nr. 3132. Output
  `review/ihagrrep7cnr421/signatures/index.html`.
- **Sonnet (web):** the *Handbuch über den Königlich Preußischen Hof und
  Staat* for 1799 and 1800: the Grand Chancellor's office, the
  Justizdepartement and the councillors who report for South Prussia, and
  the Geheime Kanzlei. Copied verbatim with a working translation into
  `reference/sources/handbuch_1799_1800_justizdepartement.md`, as the Poznań
  extract was. If no digitised volume answers, it says so and stops.
- **Claude** compares the crops with the candidates (the "-llen-" and
  final z of the decision's signature, "[Willen?]" on the slip, which may be
  the same hand) and proposes each identification with its grounds; the
  editor confirms on the spot sheet. A signature that matches no name stays
  "[Signature]".

### 3. The English of the holding (Claude writes, a Sonnet reader checks)

Claude rewrites only the affected pages in `english.py`, from the readings of
step 1:

- the margin note: what is read, in English; what is not, as "[...]", never
  German fragments (the rule proposed in step 6);
- doc 6: "Zarobna" (if confirmed), the participle, "Treasurer of Wschowa",
  "Starost of Nieszczewice";
- the Latin: in English, the Latin in brackets at its first use where the
  document turns on it (HOUSE_STYLE, "English"): "on the strength of a
  handwritten bond (ex chirographo)", "the bond on which the suit rests",
  "from elsewhere", "jointly and severally (in solidum)", "an antichretic
  contract (the creditor takes the pledge's income in lieu of interest)",
  "against the Fiscus", "so resolved the same day";
- then `english.py`, `write_cache.py`, check_translations,
  publish_translations, as the notes' "Translation and summaries" say.

A **Sonnet faithfulness reader** reads each rewritten page against its German
or Polish and lists every sense added, lost or changed; Claude checks each
finding before acting on it. The summaries are read for the same words (a
summary that repeats "Zaro..." or the Latin is corrected and the claim check
re-run on that document only).

### 4. Registry numbers (Claude designs the rule, Sonnet implements and sorts the diff)

- Rule (Claude): in `pipeline/numerals.py`, a four-digit number with no unit
  after it that **stands alone on its line** (an optional full stop after it,
  an optional date or registry mark before it, such as "v. [?] d. 25. 4168.")
  is a registry number and is not grouped. Tables keep the present rule.
- **Sonnet, to a spec:** implement it and write
  `pipeline/review/verify_numerals_diff.py`, which runs the old and the new
  rule over every English page and reading text and writes each change with
  its line to a TSV.
- **Sonnet reader:** sorts every changed number into "registry number" or
  "sum/count" with the line as evidence. **Claude** reads the "sum/count" rows
  and a sample of the others; the rule is narrowed until no sum loses its
  comma.

### 5. The same faults across the edition (a script, then Sonnet, then Claude)

The editor saw the Latin "in some English translations", so the whole English
is swept, not only this holding.

- **Script (free):** `pipeline/review/foreign_in_english.py` lists, per page
  of `site/_data/translations/`: (a) Latin tags from a list (ex quo, aliunde,
  in solidum, ex chirographo, eodem, ita conclusum, contra, in simili, sub
  dato, ad acta, pro memoria, ...); (b) words with Polish letters that are
  not a name or place the index matches (`reference/people.yml`,
  `reference/places.yml`); (c) German words left in the English (a German
  word list against an English one); (d) runs of two or more bracketed
  fragments ("[t?]orm[?]"), the shape of fault 6. Output
  `review/foreign_in_english.tsv`. Today's count of Latin tags alone is
  small (about 20 pages of 662), so the list should be short.
- **Sonnet readers, one per batch of holdings:** each row with its German,
  proposing "translate as ...", "a name, keep", or "an accepted English term,
  keep" (Starost is one, by the editor's rule).
- **Claude** rules each proposal. Corrections go into
  `reference/english_corrections.yml` (one page, with the German that decided
  it) or, for a term that recurs, `reference/english_forms.yml` or the
  termbase `reference/translation_glossary.yml`. Never into
  `site/_data/translations/` alone.

### 6. The rules written down (Claude)

- `reference/translation_glossary.yml`: Skarbnik (Treasurer, with the
  district), the Latin of the courts (ex chirographo, in solidum, antichresis,
  ex quo, aliunde), so that translate.py and in-session translation give
  them the same way.
- `reference/glossary.yml`: `skarbnik` (Gloger, "Skarbnik"), `antichresis`
  (Krünitz), checked: false until read; the glossary gate.
- `docs/EDITORIAL_RULES.md` or the English section of HOUSE_STYLE: **an
  unread word is not carried into the English as the original's letters.**
  What the passage fixes is given in English with "[?]"; what it does not is
  "[...]". The session's old rule ("words still unread are kept as written")
  is withdrawn. **For the editor to confirm** (it changes how every unread
  word shows in English).
- `docs/WORKING_NOTES.md`: the faults of this holding and how they were
  caught.

### 7. Build, check, record

`python pipeline/build/build_site_data.py`, the Jekyll build,
`python pipeline/verify_site.py`; the changelog; NEEDS_CONFIRMATION ("I. HA
GR, Rep. 7 C, Nr. 421": Zarobna, the signatures); the holding's notes; TODO
section 65. Publish at the editor's word.

## For the editor

1. The rule for unread words in the English (step 6): "[?]" with the sense
   where the passage fixes it, "[...]" where it does not. Yes or no?
2. Zarobna, once the image confirms it: a place of the register (and the
   gazetteer), or noted only?
3. The order: Nr. 421 first (steps 1-4, about one sitting), then the sweep
   (step 5).

Paid runs: none. All the work is in session and by sub-agents.
