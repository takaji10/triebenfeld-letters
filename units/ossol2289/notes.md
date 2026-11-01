# B. Ossol. rkp. 2289 II

One document so far: the copy of Kościuszko's letter of 3 September 1798,
written in Paris, on page 145 of the codex (scan 0062 of the thirty-scan
set). The holding was added 2026-11-01. The sweep of the whole scan set is
logged in `scratch/ossolineum2289/index_transcription.md` (uncommitted by
design) and flagged for the editor in `docs/NEEDS_CONFIRMATION.md`, section
"The Ossolineum manuscript NBO 2289/II".

## Provenance

Zakład Narodowy im. Ossolińskich (Ossolineum), Wrocław, manuscript 2289 II,
titled in the catalogue record "Listy, dokumenty i wiersze z lat 1697-1798 :
odpisy sporządzone przeważnie przez Stanisława Przyłęckiego." The scans are
thirty TIFFs of the digitised manuscript (leaves 0033-0062 of the codex,
files `NBO-2289--0033.tif` … `NBO-2289--0062.tif`, 1990x3150, greyscale),
downloaded by the editor into `Downloads/Ossolineum/`. Intake is selective:
`intake/build_pages.py` converts only the leaf the transcribed document
stands on (scan 0062 = manuscript page 145, the editor's page number) into
`pages/NBO_2289_0145_a.jpg` and records the provenance in
`scan_rename_map.json`. The remaining 29 scans stay on disk, unscreened into
the edition.

## Transcription

Claude read the letter from the scans in band crops (one image per read;
the ~16 MB request budget of the model, WORKING_NOTES), produced a flagged
working reading (kept as the record of the first pass in
`scratch/ossolineum2289/transcription_0062_kosciuszko_1798-09-03.md`), and
the editor then corrected the whole reading, line by line. The corrected
text stands as the transcription: the copyist's orthography as the editor
read it (twóy, iak, Żałuię, adressowany, narodowey, pomyślnieyszych,
strzedz, zachoway, chciey, przyimiy, przyiaźń), the superscript expansions
in brackets (Sz[anowny] Ob[ywatel]u, P[aryża]), and the line-end wraps
marked with ¬. No doubt marks remain. The page also carries, above the
letter, the codex's filing hand: the corner note "1798. 3 Wreznia." and the
heading "List Tadeusza Kościuszki"; both are transcribed with the letter.

## The letter and its addressee

The letter never names its addressee. An identification with Antoni
Prusimski was proposed through Pachoński's PSB entry
(`literature/pachonski1982`, sources "B. Ossol.: rkp. 2289/II") - the
émigré's letter of 13 VIII 1798 from Dresden, the polite reply expressing
regret at knowing him only from correspondence - and was the working
attribution when the holding was added. **The editor ruled the connection
out for now on 2026-11-01, until something tells us otherwise.** The
grounds, all checked in session:

- the printed entry's citation of the manuscript is unattached: the file
  the edition holds carries no footnote apparatus, so what Pachoński took
  from this codex, and for which claim, cannot be seen (PSB practice is a
  general source list for the whole entry, not per-claim notes);
- the two phrases the entry quotes for the exchange («Lud i Wolność to dwa
  filary na których muszą oprzeć się Polacy», for the 13 VIII letter;
  «nie zna go osobiście», for the Naczelnik's reply) appear in the copy in
  neither wording - the copy reads "Miłoby mi było poznać cię osobiście"
  and never the filary sentence. A match would be expected had he quoted
  this copy;
- Pachoński's earlier article on the Poles in Venice, 1794-1797
  (`literature/pachonski1973`, complete 31-note apparatus) cites no
  Ossolineum manuscript and ends before 1798; the PSB source list is the
  same archival family extended into the later emigration years, which
  makes the citation's placing consistent with the correspondence
  paragraph - but proves nothing.

What would tell us otherwise: the printed PSB volume's footnote apparatus
(the volume is digitised, t. 27 in parts 1982-83), an Ossolineum inventory
card for rkp. 2289/II, or a name at the index level in the codex's own
index leaves (0033-0034, unread to the name level) or on leaf 0061
(unread; image delivery failed). Until one of those speaks, the recipient
stays unattributed in `correspondents.json` and the prose says the
addressee is not named.

Two discrepancies stand between the copy and the PSB entry:

- **"10 Aug." against the PSB's "13 VIII".** The digit was re-read at 3x in
  the first pass and stands as "10"; the editor's corrected transcription
  keeps "10 Aug.". Either the copyist misdated, PSB misdates, or two letters
  stand behind the two dates (NEEDS_CONFIRMATION).
- The copy's text is a copy, not the original; the original is not known to
  survive. The copyist's spellings are kept as written.

## Line breaks

Six line-end wraps, all genuine word-breaks of the copyist's Polish
(okoli-czności, sło-dzi, Republi-kanską, oczeku-iącemi, nara-żać,
kon-serwować), recorded as `join` in `linebreak_decisions.csv`. The
automatic resolver works on German evidence (DWDS) and read Polish words as
unattested; the decisions were made by hand from the sense, each with its
reason. The resolver's word-regex also dropped a final "ć" from one head
("nara" + "ża"); the row was corrected to the real halves ("nara" + "żać").

## Translation and summary

No paid run (the editor's word for a single-page document, the path of
app534062 and app5320pozgr1181). The English was written in session under
translate.py's rules and written into the translation cache by
`intake/translation/write_cache.py` - the record carries the source_hash,
exactly as a paid run would. `check_translations.py` raised 0 rows. The
superscript expansions are rendered in the English as their words ("Dear
Citizen", "Paris"), per the holding's translation_note. The three difficult
verb forms of the closing sentence (zachoway, chciey, przyimiy) are read by
their formulas ("Keep ... for Yourself; for my part I shall preserve ... and
I accept ..."), noted in the translation file's own record.

The summary was written in English and German in session; its 10 statements
were claim-checked (`intake/claim_check.yml`), all supported. The checks
against the document itself verified the dateline, the salutation and every
sentence's anchor; the two claims that rest on outside knowledge (the PSB
attribution, the PSB's wording) cite where they come from and say so.

## Dating and place

The date is read off the document's own dateline ("d. 3 Września 98" =
1798-09-03, day precision); the corner note "1798. 3 Wreznia." agrees. The
place of writing is the dateline's "z P[aryża]" - Paris, the expansion the
editor's reading; Paris is not a place of the edition's registers, so the
name shows as read.

## What the holding owes the site

Done in session 2026-11-01: `about.md`/`about_de.md`; the person entry
Tadeusz Kościuszko (`reference/people.yml`, `reference/people_bios.yml`;
counted before the pattern was added - no document outside ossol2289 names
him); the new era `insurgency` (`reference/eras.yml`, orders bumped, the
label and blurb a working text for the editor); the summaries; the
translation cache; the checks. Timeline: no event added - offered to the
editor (a 1798 row "Kościuszko replies to Prusimski" would fit the
timeline's 1794-1832 range). Places: no map link (Paris is not a place of
the edition). Glossary: 0 candidates.

## Damage

None. The leaf is whole; the copyist's hand is firm.

## Open (NEEDS_CONFIRMATION)

- the attribution of the letter to Prusimski: **ruled out for now** (the
  editor, 2026-11-01), to be reopened on evidence - the printed PSB's
  footnotes, an Ossolineum inventory card, the codex's index leaves read;
- the "10 Aug." / "13 VIII" discrepancy;
- the copyist's closing-note name (the editor confirms by hand);
- the remaining 29 scans (sweep logged, uncommitted) and the missing
  continuation of the Patent of 25 lipca 1794 between leaves 0048 and 0054;
- the recipient metadata stays empty while the attribution is ruled out.
