# Adding new text to 9454: the checklist

For text added after the corpus-wide passes, such as the sideways continuations the
editor is transcribing from the scans (2026-09-29). The new lines get every pass
the rest of 9454 had, applied to the new lines only. The reasons behind each rule
are in `notes.md`; this file is the order of work.

Tools: `pipeline/review/show_letter.py` prints a letter with corpus and letter
line numbers. `pipeline/review/fix_sheet.py` turns rulings (corpus line, old, new,
reason) into the sheet `apply_transcription_fixes.py --apply` applies and logs.

## 1. Insert

- The sideways text is the letter continuing where the writer ran out of room.
  It is not a marginal note, so it gets no marker.
- Insert it as ordinary lines in reading order: normally right after the last line
  of the page it is written on, under that `[PAGE ...]`. If the sense shows it
  belongs elsewhere (a postscript after the closing), put it there and say so.
- Ask which page only when the letter has several pages and the sense doesn't
  decide it. Scans are listed in `page_scan_map.csv`.
- Keep the editor's line breaks. Before inserting, note each affected letter's
  line count, for step 8.

## 2. House rules for the new lines

- A word broken at a line end: `¬`. A real hyphen stays `-` (compounds, paired
  words: `Kriegs- und Forst Rath`).
- A dash used as punctuation: `—`, spaced. Figure ranges stay as written (`8-14`).
- Period spelling is his, not an error: ſ, ß/ss, zz, th, doubled letters (`Feeder`),
  `Hube`/`Hufe`, `rt`, `Ewr`, `gerne`, `seyn`. Never normalise it.

## 3. Corrections, at the witness bar only

- **Approved patterns** (apply everywhere): Ewr before Durchlaucht (not
  Eine/Ein/Erer/Eier/Ewo/Er), Jezt (not Jagt), Schicken Sie (not Schaden Sie),
  Indes as the conjunction (not Jedes), schicken meaning "send" (not schulen),
  Summa (not Suma), Königl. Majestät, closings `In tiefster Ehrfurcht ersterbe`,
  `empfehle ich mich`, `unterthänigster`.
- **Known confusions:**
  - zz read as pp;
  - ß read as b;
  - m/w and w/r;
  - bei/bin, ist/ich, um/und, kam/kan(n), iſs/iſt, noch/nach.

  Fix one only where it makes an impossible form, and use the form the same
  letter uses (kan or kann).
- **Nonwords:** check new words against the three units' vocabulary and DWDS
  (`reference/dwds_cache.json`; `spelling_audit.py` for the method). Fix only a
  slip one Kurrent confusion away from a common word.
- **Leave alone:**
  - anything that may be his grammar (case endings, dropped -n, verb endings);
  - figures and dates;
  - the editor's `[..]` expansions;
  - a real word swapped for a better-sounding one (no witness, no change);
  - anything inside a garbled passage.
- A corrupt word with no reading at the bar is left as it is. Log it in
  `review/oe1bu9454/unresolved.md` and do not add `[?]`.
- `[?]` marks the editor wrote are decided from context only where the evidence
  is solid (an idiom, a witness, an abbreviation, a single grammatical reading).
  Otherwise they stay.

## 4. Names, titles, places

- **People:** use the settled form, from `reference/people.yml` display names
  and `name_rulings.json`. For example:
  - Hawich (watch-list: Habisch/Habich/Habik/Hawick);
  - Brzechffa, Niedźwiecki, Prusimski/Prusimska;
  - Bertrand, Götzen, Bornstädt, Glenck, Schenck, Echaust;
  - Beguelin, Schulenburg, Rybbeck, Talleyrand.

  Married names are different names (Dąbska, Moscińska).
- **One-letter variants** with no settled form stay as written: Kiełszewski,
  Weigelt, van der Lahr.
- **Titles:** his most common spelling: Hoffrath, Krieges Rath, Staats Kanzler,
  Bürgermeister, Prefect, Cabinets Rath.
- **Places:** German documents keep the German name as written (Zagorowo,
  Kaemen, Frankfurth, Peisern, Kalisch, Wittow); Polish text keeps Polish.
  Misreadings of a place are fixed to that place's one spelling (Trąbczyn,
  Schlawenschitz, Kontop, Öhringen, Sachsen).
- **Also:** Johanni (the rent day), not Johann; Rußland; Pohlen; Posen.
- **New name or place:** find it in `people.yml` / `places.yml`. A new spelling
  of a known one gets a `match`/`variants` addition. Compare the index
  document counts before and after any authority change.

## 5. Abbreviations

- **Titles** expand in brackets: Gen[eral], Lieut[enant], Geh[eimer] Rath, H. M[ajor].
- **Forms of address:** E[wr]. D[urchlaucht]., E[wr]. H[ochfürstliche]. D[urchlaucht].,
  E[wr]. K[önigliche]. M[ajestät].
- **Single-letter initials** expand only where the same letter or the period
  settles them (B[arbe] in the Vienna letters of 1814-15).
- **Leave as written:** Cur. becomes Cur[ische] (never Curl.); p / pp / ppp
  stay; rt stays.
- A settled doubtful letter loses its brackets ([T]alente becomes Talente).
  Brackets stay only on expansions.

## 6. Apply

- Write the rulings as TSV, run `fix_sheet.py`, then
  `apply_transcription_fixes.py --unit oe1bu9454 --apply`. The reasons land in
  `transcription_decisions.csv`.
- The doubt-mark count must not rise.

## 7. Rebuild and verify

- Run `python regenerate.py`. If it prints `!!`, read the log: the pipeline
  self-check stops the build.
- About 30 s later, run `python verify_site.py`: ALL CHECKS PASSED.
- If a new line fell into a dateline, check that the letter's date, place and
  sender are unchanged in `corpus/letters.json`.

## 8. Reading record and summary

- In `reading.json`, for each affected letter, add the number of inserted lines
  to every claim `lines` value that lies below the insertion point.
- Read the new text against the letter's summary in `summaries_de.yml`.
  - If it adds nothing that matters, leave the summary.
  - If it does, re-run that one letter with `read_letters.py --letters X`, then
    `--verify`. It costs cents; say so first. Then update `summaries_de.yml`,
    write the cache file, and run `summarise.py --build --lang de --tag v2`.
- There is no English yet. The translation will pick up the new lines.

## 9. Record

One entry in `notes.md` listing the letters and lines added and the fixes made.
Then commit.
