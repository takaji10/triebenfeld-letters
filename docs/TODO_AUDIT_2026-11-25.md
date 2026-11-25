# The to-do audit (2026-11-25)

Every one of the 133 open boxes of `docs/TODO.md` read against the repository by five Sonnet readers (each box: the holding's notes, NEEDS_CONFIRMATION, the changelog, the later sections, the files themselves); Claude checked every verdict that would close a box (the files named exist, the dates agree). **Nothing has been removed from TODO.md yet**; this is the proposal, for the editor's yes. Line numbers are those of `docs/TODO.md` on 2026-11-25. Plan: `docs/TODO_PAGE_PLAN.md`.

| Verdict | Boxes | Proposal |
|---|---|---|
| Done | 13 | tick them off |
| Superseded | 2 | remove |
| Duplicate of a question in NEEDS_CONFIRMATION | 30 | keep the question once (in NEEDS_CONFIRMATION, and later on the page), drop the second copy |
| Can't tell | 2 | the editor decides |
| Still open | 86 | stay: 69 for the editor, 10 for Claude, 7 waiting |


## Proposed: tick off (done)

- **l.190** (section 6) Look at the dropped-phrases sheet for Konin Gr.145. *Because:* docs/archive/PRUSIMSKI_QUESTIONS.md l.89-91: 'Konin Gr.145: the tower sentence as I read it ... my English of the paragraph on leaf 680 is fine.'; CLAUDE.md also says confirmed.
- **l.703** (section 20) Look at Łukasiewicz English, then publish. *Because:* docs/TODO.md and CLAUDE.md: Łukasiewicz 'published 2026-10-22'; the publication half is done.
- **l.1102** (section 33) Gazetteer pages per place, English and German. *Because:* site/_places has 310 pages incl. adamierz.md, bartosz.md, both languages; pipeline/verify_site.py l.516 checks the gazetteer section; coords in site/_data/place_coords.yml.
- **l.1106** (section 33) Labelling page for maps and first map. *Because:* pipeline/maps/label_page.py exists; maps lukom1766, kozlowski1861, pelzucki1896 built (TODO sec. 34 [x] items; changelog 2026-10-31).
- **l.1111** (section 33) Add ten missing Kodeks entries cited by gazetteer. *Because:* units/kdw/notes.md l.105-113 (added at the editor's word); intake/kodeks_missing.txt holds Nr 228,535,672,795,1044,1363,1478,1490,1491,1519; MISSING_SOURCES 'In the edition: 31 entries'.
- **l.1131** (section 34) Coordinates for places that exist today. *Because:* docs/CHANGELOG.md l.6527 'Place coordinates: one generated file for every place... 114 positions from Wikidata'; pipeline/places/coords.py.
- **l.1175** (section 34) Pełzucki 1896 marks, import and page. *Because:* docs/CHANGELOG.md ~l.4071 'The editor's seven marks imported'; maps/pelzucki1896/labels.yml, farms.yml, georef.yml and site/_maps/pelzucki1896.md exist.
- **l.1331** (section 55) Approve five drafted gazetteer entries from cemetery survey. *Because:* reference/gazetteer/ now has lazinsk-pierwszy.yml, lazinsk-drugi.yml, orlina-duza.yml, stawiszyn.yml, zbiersk-kolonia.yml; CLAUDE.md: 'gazetteer's five new entries entered'.
- **l.1567** (section 61) 1882 reports: claim check, index, timeline, era essay. *Because:* TODO.md l.1575: '2026-11-12: spot sheet answered and applied; the index, the timeline event of 1882 and the era paragraph added'; claim_check.yml exists. Only a German reader's review remains.
- **l.1606** (section 63) Publish Nr. 3067 at editor's word. *Because:* CLAUDE.md: Nr. 3067 'published 2026-11-19'; TODO line 1594 header still says 'not published' (stale).
- **l.1646** (section 65) Repair the English of Nr. 421 (seven-step plan). *Because:* TODO line ~1657: 'plan's steps 2, 3, 5 and 6 done the same evening'; NR421_ENGLISH_PLAN step 4 'done'. The 'Next:' list is stale.
- **l.1672** (section 68) Try the layout editor and send an export. *Because:* reference/english_layout/app539680782-001.yml exists (commit 064634c7): an export was applied; CHANGELOG 6508 layout editor built.
- **l.1751** (section 69) Rewrite the ~640 English document summaries. *Because:* TODO section 70 line 1783: 'E: the 649 summaries (648 rewritten, 2026-11-25)'.

## Proposed: remove (superseded)

- **l.1456** (section 57) Publish the holding-pages tightening branch. *Because:* CLAUDE.md: work is on main, old branches deleted 2026-11-21, site overhaul published 2026-11-24 rewrote all 57 holding pages; branch unit-pages-tightening no longer exists (git branch).
- **l.1747** (section 69) Rewrite place and person pages to new rules. *Because:* TODO section 70: 'C4, C5: all 324 bios rewritten', 'E: the Zagórów place page'; era pages done. Only the German (all at once, your word) remains, see item 124.

## Can't tell: your call

- **l.281** (section 7) Full account of the Prusimski era on the story page. *Because:* reference/eras.yml prusimski-boundary now has an intro_en/intro_de (written 2026-11-07, NEEDS_CONFIRMATION l.214), but whether a fuller account is still wanted is not stated; condition (missing transcriptions) only partly met.
- **l.1100** (section 33) Claude reads the gazetteer import against the text. *Because:* docs/GAZETTEER_PLAN.md l.236 defines step 2; changelog shows partial readings (kinds audit, bad OCR readings 2026-11-06) but no record of step 2 being declared finished.

## Duplicates of NEEDS_CONFIRMATION questions

- **l.70** (section 2) Confirm image 06 (Polish petition of 20 July) is wanted. *Because:* Same open point as docs/NEEDS_CONFIRMATION.md l.934 'image 06 of 1/174/0/2/73 is used though the editor named only 05, 07, 08 and 047'.
- **l.83** (section 2) Read 'upoznieniem' in the petition of 23 July 1807. *Because:* units/agad11740273/notes.md l.153 'upoznieniem ... left in Polish and recorded as not'; NEEDS_CONFIRMATION.md l.1840 lists it as the chief open word.
- **l.305** (section 7) Pyzdry Gr.75 deferred. *Because:* Same as TODO section 6, l.212 'You: Pyzdry Gr.75 ... when you come back to it'.
- **l.312** (section 8) Decide era of Nr. 12366. *Because:* Same as TODO section 1 l.31 (era of Nr. 12366 and 12367).
- **l.331** (section 8) Archives' permission for scans; full name for licences. *Because:* docs/NEEDS_CONFIRMATION.md l.2160 'Before the site is shared widely: Scan rights ... The holder's name'.
- **l.445** (section 12) Does Breyer's 'Łazinsk' of 1936 mean both colonies?. *Because:* docs/NEEDS_CONFIRMATION.md l.1706-1707 'whether Łazinsk of 1936 is both Łazińskie colonies' (also reference/places.yml open_questions).
- **l.875** (section 26) Rule on the conflicting Mielke dates in the Słowiński volumes. *Because:* docs/NEEDS_CONFIRMATION.md ~l.2031 'The Mielke dates conflict within the 2024 volume' still open.
- **l.879** (section 26) Which founders of Łazińsk in 1746 the edition follows. *Because:* docs/NEEDS_CONFIRMATION.md ~l.2024 'The founders of the 1746 foundation differ... waits on the editor'.
- **l.883** (section 26) Rule on the 1718 founding date of Łazińsk. *Because:* docs/NEEDS_CONFIRMATION.md l.446-457 'The 1718 of the 1942 article... a third witness to 1718... the ruling still wanted'.
- **l.885** (section 26) Look at the 2024 summary and the slowinski2023 English. *Because:* docs/NEEDS_CONFIRMATION.md ~l.2034 'The English of slowinski2023 on file is the editor's own... The editor's look at that English is wanted'.
- **l.901** (section 27) Extend the register's patterns for unmatched Ląd and region forms?. *Because:* docs/NEEDS_CONFIRMATION.md l.480-492 Ląd/'Lądu'/region-name patterns: 'Same question, whether to extend the register's patterns'; still unmatched.
- **l.1008** (section 30) Is 'Emilienhain' the same colony as Emilienheim?. *Because:* docs/NEEDS_CONFIRMATION.md l.527-539 'Emilienhain against Emilienheim ... is the editor's to rule'.
- **l.1012** (section 30) Identify the dismissed teacher of the 1933 note. *Because:* docs/NEEDS_CONFIRMATION.md l.539-543 'The dismissed teacher ... the question is asked, not answered'.
- **l.1016** (section 30) Should Szymanowice become a place of the edition?. *Because:* docs/NEEDS_CONFIRMATION.md l.544-549 'Szymanowice is matched by no pattern'; no szymanowice entry in reference/places.yml or gazetteer.
- **l.1038** (section 31) Check doubtful readings in the 1879 Miączyński death notice. *Because:* docs/NEEDS_CONFIRMATION.md l.563-573 'The doubtful readings of the notice ... the editor's eye wanted on it'.
- **l.1045** (section 31) Is Pawłowa, the nephew's seat, a register place?. *Because:* docs/NEEDS_CONFIRMATION.md l.575-578 'Pawłowa ... is the editor's'; no Pawłów entry found in reference/gazetteer or places.yml.
- **l.1070** (section 32) Confirm Heinrich Zelmer belongs to the Trąbczyn Zelmers. *Because:* docs/NEEDS_CONFIRMATION.md ~l.1870 'Heinrich Zelmer... not shown. The literature ruling stands on the presumption.'; nothing further found.
- **l.1093** (section 33) Answer the open points in the gazetteer section. *Because:* docs/NEEDS_CONFIRMATION.md l.635ff 'The gazetteer' section holds these points (e.g. Mieszko III, l.640), still open.
- **l.1108** (section 33) Interactive map, once coordinates are in. *Because:* Same as 'The interactive map (/map/)' at TODO l.1179 (section 34); no site/map.html yet; coordinates now in (place_coords.yml).
- **l.1171** (section 34) Add Noga to Wielki-Bór Obręb's districts?. *Because:* docs/NEEDS_CONFIRMATION.md l.719-722 'Wielki-Bór Obręb's district Noga ... Add Noga to the sentence?' still open.
- **l.1205** (section 35) Read the Kurrent lines of sheet 0030. *Because:* docs/NEEDS_CONFIRMATION.md l.1689 'Open: the Kurrent lines of 0030 below the Themen block, if the editor reads them'.
- **l.1247** (section 36) Is '6 gl.' in the 1820 contract gulden or Groschen?. *Because:* docs/NEEDS_CONFIRMATION.md l.2066 'whether this contract's "6 gl." is gulden is put to the editor'; no guard found in reference/english_forms.yml.
- **l.1249** (section 36) Glossary entries for the 1820 contract's single-use terms?. *Because:* Same question in docs/NEEDS_CONFIRMATION.md ~l.2131 'The single-document terms of the contract of 1820'; no glossary entries for St./Böhm/Opfertorium/Viertel exist in reference/glossary.yml.
- **l.1266** (section 54) Check preceding volume pages for the 1727 sitting heading. *Because:* NEEDS_CONFIRMATION.md ~l.1356 'The sitting of the relatio of 1727' holds the same request; units/app534062 still has no dates: sitting.
- **l.1275** (section 54) Three open readings in the Szetlewicz entry. *Because:* NEEDS_CONFIRMATION.md ~l.1845 (APP 53/4/0/-/62 open readings) and units/app534062/intake/unresolved.md list Conte~, Juris Firma, eam.
- **l.1328** (section 55) Exact date of the cemetery visits. *Because:* NEEDS_CONFIRMATION.md ~l.616 'The visits' exact date'; pages still say 'visited in 2023'.
- **l.1565** (section 61) Open readings in Erdmann's 1882 reports. *Because:* NEEDS_CONFIRMATION.md l.2564 section 'AGAD 1/432/0/1/139' lists still-open readings ([Verlangen?], 4 Rubel 61 stroke, [Ho?], Kantor, Manitius).
- **l.1590** (section 62) Rule proposed connections and folio 88 note, Trąbczyn file. *Because:* NEEDS_CONFIRMATION.md ~l.2531 section APŁ 1333, 'Still open' 1 (folio 88) and 3 (connections proposed); none in reference/connections.yml.
- **l.1603** (section 63) Confirm Nr. 3067 reference, identifications, Ostrzewo. *Because:* NEEDS_CONFIRMATION.md ~l.2492 section Nr. 3067, points 2-5 (reference GR, Wybicki/Niemoiewski, Ostrzewo, two differences) still stand as Claude's.
- **l.1805** (section 70) Name the namesake for unplaced places. *Because:* TODO section 70 line 1771: '[ ] name the ones left unplaced (NEEDS_CONFIRMATION, "Place coordinates")'.

## Still open, with the reader's notes

The stale wording flagged by the readers (the item is open but its text is out of date) is marked **rewrite**.

- l.31 [EDITOR, decision] Decide era (Hohenlohe or restitution) for Nr. 12366 and 12367. units/iiihamdaiiinr12366/unit.yml and 12367 still 'era: hohenlohe'; NEEDS_CONFIRMATION.md ~l.795-810 lists the era as still open.
- l.67 [EDITOR, task] Check the AGAD 1807 page crops for bad cuts. CLAUDE.md and TODO still list the look at the AGAD crops as open; nothing in units/agad1174016 or agad11740273 notes records an answer.
- l.74 [EDITOR, decision] Decide era for the two Governing Commission holdings. units/agad1174016 and agad11740273 unit.yml still 'era: hohenlohe'; eras.yml restitution now populated, so moving them is an open choice.
- l.161 [EDITOR, task] Check the four page crops of Nr. 1414. CLAUDE.md for Nr. 1414: 'Open: the editor's look at the four crops'; notes.md l.174 describes the cuts, no answer recorded.
- l.206 [EDITOR, task] Supply transcriptions for Pyzdry Gr.75 and Konin Gr.142, Gr.150. **rewrite** Poznań Gr.1181 is now built (units/app5320pozgr1181) and Pyzdry Gr.115 too; Gr.75, Konin Gr.142 and Gr.150 still have no unit (ls units). Item text still lists Gr.1181 as missing.
- l.212 [EDITOR, decision] Decide what to do with Pyzdry Gr.75 signature. No units/ folder for Pyzdry Gr.75; docs/PRUSIMSKI_ERA_PLAN.md l.349 records the editor's deferral.
- l.287 [EDITOR, task] Photograph headings of sittings to date documents surely. TODO l.287 itself; no later note records photographs of sitting headings; app534062 has a similar open item (TODO l.1265).
- l.298 [EDITOR, task] Transcribe middle of Konin Gr.136 for completeness. units/app53170koningr136/notes.md l.54: 'Its middle is not transcribed'; no later change found.
- l.301 [EDITOR, decision] Decide whether to transcribe three more entries of 53/6/0/-/17. units/app536017/notes.md l.32/98 'Three more entries on the scans, not transcribed ... The editor's word'; no answer found.
- l.333 [EDITOR, task] Supply remaining Geheimes Staatsarchiv files for Hohenlohe years. docs/HOHENLOHE_ERA_PLAN.md l.240-251 marks Nr. 1413, Jena operations, IV. HA biography and Rep. 74 Nr. 4680 'to add'; no units/ folder for them.
- l.336 [WAITING, waiting] Read site prose against editor's voice (at editor's word). TODO l.336 'Later, at your word'; docs/EDITORS_VOICE.md exists, CHANGELOG l.2106 records only the brief; no voice pass logged.
- l.344 [WAITING, waiting] Add a framed 'side road' element to site (at editor's word). TODO l.344 'The site has no such element yet'; grep of site includes finds no side-road element.
- l.370 [EDITOR, decision] Want modern names for the 164 villages of the 1797 table?. units/agad1169011745/notes.md l.193-195 'Nothing waits on the editor. Offered ... not answered: the modern name of each village'.
- l.393 [EDITOR, decision] Name the wlodzimierz era. reference/eras.yml l.287 'Its name is a WORKING NAME'; NEEDS_CONFIRMATION.md l.1721 'The eras' holds Claude's proposed name, unanswered.
- l.437 [EDITOR, task] Read 36 doubtful readings on covers and photo log (optional). NEEDS_CONFIRMATION.md l.1697-1703: '70 marks of doubt remain, 29 on the inside covers and 7 in the photograph log, not put to the editor'. Optional.
- l.439 [EDITOR, task] Place folds for the seventeen Breyer notebook openings (optional). units/app539680669/notes.md l.82-83 'the editor has not placed them'; no folds.json in intake. Optional.
- l.444 [EDITOR, decision] Name the twentieth-century era. reference/eras.yml l.366 'The twentieth century' is a working name (comment l.287ff); NEEDS_CONFIRMATION l.1721 proposal 'The German villages to 1945' unanswered.
- l.447 [EDITOR, decision] Want the other Breyer notebooks (Grodziec 1938, Białobłoty, Dembe)?. **rewrite** Grodziec 'Juli 1936' is already document 2 (TODO section 13), so item text is partly stale; Grodziec 1938, Białobłoty, Dembe not in units/app539680669/notes.md.
- l.531 [EDITOR, task] Read the ADWł 85 entry on the page of changes. TODO l.531 itself; units/adwl85/notes.md l.58 'What changed for the editor is in intake/changes.yml'; no answer recorded.
- l.538 [EDITOR, decision] Whether to add rest of Trąbczyn visitation and Zagórów church description. units/adwl85/notes.md:100 still lists 'Offered: the rest of the visitation of Trąbczyn (leaves 26 to 28 recto...'; no later work found.
- l.570 [EDITOR, decision] Name for the medieval era (working name 'Trąbczyn in the Middle Ages'). reference/eras.yml comment still 'A working name until the editor names it'; NEEDS_CONFIRMATION.md:1732 only has Claude's proposal 'keep'.
- l.592 [EDITOR, task] Look at the 'In the literature' lists on People/Places pages. **rewrite** No later record of the editor reviewing the 'In the literature' lists; five identifications accepted already (line itself).
- l.606 [EDITOR, task] Read the four link sentences for documents 85 and 103 and Materialien. No record in TODO/NEEDS_CONFIRMATION of the editor having read the link sentences on the live site.
- l.609 [EDITOR, task] Correct Guradze's text and add page numbers. NEEDS_CONFIRMATION.md:944 'Waiting on the editor: Guradze's corrected text and its page numbers'.
- l.613 [EDITOR, task] Add missing page 27 mark in Paciorkowski English. literature/paciorkowski1776/notes.md:16 'The English has no mark for page 27'; NEEDS_CONFIRMATION.md:946 same.
- l.615 [EDITOR, decision] Supply notes of Seidel's book if wanted. NEEDS_CONFIRMATION.md:946 'the notes of Seidel's book, untranscribed in both files'; optional.
- l.617 [EDITOR, decision] Later: add timeline events drawn from the books. Only TODO.md:617 itself; no timeline events from the books found as a planned task.
- l.624 [EDITOR, question] Remaining rulings from second set of books (holders 1809-1879, Weigel). NEEDS_CONFIRMATION.md:951-1002: marriage (settled 1810), mother's death (settled by documents rule), Włodzimierz's death (18th, settled :359) are done; 'Who held Trąbczyn 1809-1879', K. G. von Weigel and Claude's identifications remain open.
- l.629 [CLAUDE, claude] Check Breyer 1938 pp. 38-47 against the Łazińsk holdings. TODO.md:629 'Still to be considered'; links.yml has breyer1938-lease only, no pp. 38-47 Łazińsk comparison found.
- l.638 [EDITOR, task] Look at Literature page; judge usefulness of Mączak and Szwiec. Published 2026-10-20 but no record of the editor's look or verdict on Mączak and Szwiec usefulness.
- l.643 [EDITOR, decision] Whether to link Wąsicki pp. 174-176 to the 1806 lease, and transcribe table. literature/links.yml has no wasicki1953 link; offered only.
- l.670 [EDITOR, question] Rule three Karwowski identifications (Trzciński, Weygel, Sobolewski). NEEDS_CONFIRMATION.md:1189-1206 Trzciński, Weygel, Sobolewski still unruled.
- l.675 [EDITOR, decision] Whether to link Karwowski passage to Weigel compensation documents. NEEDS_CONFIRMATION.md:1208 'Offered, not asked for'; no karwowski1900 link in links.yml.
- l.684 [EDITOR, question] Check Janocki transcription, 'Miedzyborze' and citation bracket. NEEDS_CONFIRMATION.md:1218-1221 'Miedzyborze' marked 'For the editor'; bracket wording unruled.
- l.698 [EDITOR, question] Rule three Łukasiewicz identifications (Grävenitz, Schmaling, Reck). NEEDS_CONFIRMATION.md:1960-1971 Grävenitz, Schmaling, von der Reck still open.
- l.740 [EDITOR, task] Look at Dorow (1843) work page. Dorow published 2026-11-01 (TODO.md just above); no record of the editor's look at the page.
- l.750 [EDITOR, question] Look at six Ląd cut pages; confirm year 1447 of no. 16. units/app5314550221/notes.md:58-67: year read 1447 on pencil note and witnesses, still described as inferred; no editor confirmation.
- l.778 [EDITOR, question] Confirm Oleśnica of 1937 item is the register's Oleśnica. NEEDS_CONFIRMATION.md:434 'Oleśnica of the 1937 item ... Claude's identification, not confirmed by the editor'.
- l.791 [EDITOR, question] One woman or two: Władysławowa vs Maria Wielopolska. NEEDS_CONFIRMATION.md:494-498 buyer 'Władysławowa Wielopolska' vs 'Maria Wielopolska' unruled.
- l.812 [EDITOR, decision] Attach 2015 report's Miączyński heirs to person pages?. NEEDS_CONFIRMATION.md:471-480 Miączyński heirs 'Stanisław hrabia', 'Aleksander' unidentified.
- l.816 [EDITOR, decision] Extend patterns for Lądzie, lądzki, Trampczin?. NEEDS_CONFIRMATION.md:483-485 'Lądzie', 'lądzki', 'Trampczin' matched by no pattern.
- l.833 [EDITOR, task] Look at Zagórów place page and transcription. No record of the editor's review of places/zagorowo/zagorowpl20220614.
- l.836 [EDITOR, question] Rule three Zagórów place-section questions. NEEDS_CONFIRMATION.md:~590-607 three questions (index over sources, 1869/1870, medieval dates) unanswered.
- l.855 [EDITOR, question] Is the Jutrzenka digest signed by Lidmanowski?. NEEDS_CONFIRMATION.md:501-510 'The Jutrzenka signature' unruled; newspapers/jutrzenka1913z8/item.yml has author: "".
- l.859 [EDITOR, question] Check Lidmanowski life dates; Słupca place question (likely settled). Life dates still 'the editor's eye' (NEEDS_CONFIRMATION.md:510); the Słupca half looks overtaken: reference/places.yml:1328 now has 'slupca' as a place with match pattern, though NEEDS_CONFIRMATION still says it is not in the register.
- l.1105 [CLAUDE, claude] Gazetteer downloads (JSON, CSV) and place search page. GAZETTEER_PLAN l.221 plans JSON/CSV/GeoJSON downloads; no dataset/places* or site downloads found. Search exists via site/assets/places-index.js.
- l.1109 [WAITING, waiting] Index new gazetteer places in documents; enhancement pass. GAZETTEER_PLAN step 7 'at the editor's word, once the outstanding sources are in'; docs/MISSING_SOURCES.md still lists wanted sources.
- l.1115 [CLAUDE, claude] Offered: read existing pages for method talk. docs/HOUSE_STYLE.md l.667 'A reading of the site's existing pages for method talk is offered to the editor, not yet done.' (site overhaul rewrote pages, but no method-talk read recorded).
- l.1173 [CLAUDE, claude] Record scale in register for maps lacking it. reference/maps.yml: lukom1766, zagorow1841, pelzucki1901, mapadrogi1890 are in_project with no scale: (kozlowski1861, pelzucki1896, trojwiorstowki1880 have one).
- l.1179 [CLAUDE, claude] Build the interactive /map/ page. No site/map.html; docs/MAPS_SITE_PLAN.md l.119 'until the interactive map /map/ is built'; coordinates now exist.
- l.1284 [EDITOR, decision] Whether to add a timeline event for the Szetlewicz entry. units/app534062/notes.md:166 'No event is added to the timeline: the entry names no party'; site/_data/timeline.yml has no 1727 event.
- l.1376 [EDITOR, task] Answer the 62-row spot sheet for Poznań Gr.1181. TODO.md l.1376 only; NEEDS_CONFIRMATION says Termilis/Kanino 'not indexed until the sheet settles them'; no record of the sheet's answers applied in notes or CHANGELOG.
- l.1406 [WAITING, claude] Apply spot-sheet answers and rebuild Poznań Gr.1181 pages. Depends on item 88 (the sheet's answers); nothing applied yet.
- l.1416 [EDITOR, decision] Approve Chodyła's facts list for place pages. docs/CHODYLA_ADDITIONS.md says 'Nothing here is on the site yet'; CHANGELOG 2026-10-28 'waiting on the editor'; no later yes found.
- l.1425 [WAITING, waiting] Add documents' own population figures to place pages. Editor's word 'at a later point'; gazetteer entries carry no 1791 parish figures from ADWł 85.
- l.1436 [CLAUDE, claude] Find where Wąsicki gives Lisewo 1804 figures. reference/gazetteer/lisewska-kolonia.yml has no 1804 figure; no note settling Wąsicki p. 165.
- l.1446 [EDITOR, task] Read new holding tabs: too little or too much?. **rewrite** No record of the editor's reading of the new holding-page tabs; site overhaul rewrote all 57 holding pages after (CLAUDE.md), so may be stale.
- l.1448 [EDITOR, decision] Rule on long titles shortened with [...]. full_title present in 12 unit.yml files; no ruling on written-out shortened titles found.
- l.1451 [EDITOR, decision] Approve a read of other pages for pointless description. Needs paid sub-agent run, 'your word first'; no later approval found in CHANGELOG/WORKING_NOTES.
- l.1477 [EDITOR, task] Rule the 30 documents with zero name mentions. reference/zero_mention_rulings.json does not exist; WORKING_NOTES.md:2954-2957 describes the sheet; reference/places.yml:420 does not tag Adolph.
- l.1484 [EDITOR, decision] Approve paid pass adding name marks to five units. units/app539680783/intake/translation/doc1.yml still has 'names: []'; CHANGELOG ~l.4142 'costs money, and waits for the editor's word'.
- l.1492 [CLAUDE, claude] Fix code-hygiene gate that blocks regenerate.py. Ran pipeline/check_pipeline.py (read-only): still exits 1, e.g. 'pipeline/new_unit.py:186: names one holding: Hohenlohe'.
- l.1524 [EDITOR, task] Read per-passage Related notes and new link sentences. No record of the editor's read of the Related notes; flags e.g. 89,250 Thlr. remain at NEEDS_CONFIRMATION.md ~l.1063.
- l.1533 [CLAUDE, claude] Continue Related-links sweep over literature passages. No later sweep of Paciorkowski's 178 passages or Werner/Frost etc. found in CHANGELOG; waits on the editor's word.
- l.1553 [EDITOR, task] Read the first four cross-holding connections' notes. No record of the editor having read the connection boxes; reference/connections.yml has grown to ~39 ids since.
- l.1555 [CLAUDE, claude] Further connection sweeps between holdings. WORKING_NOTES.md:4366 records a Sonnet sweep method; connections still at the editor's word for more passes.
- l.1571 [WAITING, waiting] More scans of file 139 would help readings. docs/CONSISTORY_1882_PLAN.md section 4: more scans 'not essential'; none supplied.
- l.1620 [EDITOR, decision] Keep or drop the prusimski-wife-italy connection. NEEDS_CONFIRMATION Nr. 3132 point 1: 'Open: prusimski-wife-italy (d2) ... connection stays as built until they rule'.
- l.1622 [EDITOR, question] Answer the open points for Nr. 3132. NEEDS_CONFIRMATION Nr. 3132 still has points 2-8 open (q10/q11 unread words, Smiłowice/Pawłów places, era span 1794-1798).
- l.1642 [EDITOR, decision] Decide timeline event and Hohenlohe paragraph for Nr. 421. No Nr. 421 event in site/_data/timeline.yml; NEEDS_CONFIRMATION Nr. 421 items 2-3 (suit date, 12,000 vs 36,000) still open. Era paragraph unverified.
- l.1661 [EDITOR, question] Person entry for von Massow; scan words of the sweep. NEEDS_CONFIRMATION Nr. 421 item 9 (Massow, 'very probably the signer (Claude)'); no Massow in reference/people.yml.
- l.1689 [EDITOR, task] Check the two added Kneifel pages' cuts. TODO section 66 line 1689 only; no ruling found in NEEDS_CONFIRMATION or CHANGELOG on the Kneifel pp. 180 and 257 cuts.
- l.1721 [EDITOR, question] Rule on Czarna Góra, Orliny, Augustynów. NEEDS_CONFIRMATION 'The gazetteer's candidate places': Czarna Góra, Orliny, Augustynów 358/368 all 'Open'.
- l.1724 [EDITOR, task] Supply the Kodeks entry of 1341 (Pyzdry). docs/MISSING_SOURCES.md:113 'vol. 2, no. None (1341) - Pyzdry' still listed.
- l.1744 [EDITOR, waiting] Supply literature title pages for thumbnails. NEEDS_CONFIRMATION line 28: 'the editor supplies the literature's title pages later'.
- l.1783 [EDITOR, question] Rule on the summaries' open points. NEEDS_CONFIRMATION 'The summaries rewritten' (2026-11-25) lists letter 64, 232, 257, recipients, 74c, Nr. 421 dates, 14525/14 as open.
- l.1786 [CLAUDE, claude] Add glossary entries desiatin, sazhen, mansi. grep of reference/glossary.yml finds no desiatin/sazhen/mansi entries; NEEDS_CONFIRMATION notes 'no glossary entries yet'.
- l.1787 [WAITING, waiting] German summaries, all at once. NEEDS_CONFIRMATION site overhaul: 'A German pass is for later' (editor's word).
- l.1791 [EDITOR, question] Triebenfeld's death: is '13 April' 1816?. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1793 [EDITOR, question] The Prince's age 'nearly 66' vs birth 1746. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1795 [EDITOR, question] Paweł Prusimski's office. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1797 [EDITOR, question] Chełmski loan 12,000 vs 36,000 ducats. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1799 [EDITOR, question] restoration of 1807 date. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1800 [EDITOR, question] sale of 1698 Władysław brother or son. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1802 [EDITOR, question] Jezierski one man or two. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
- l.1804 [EDITOR, question] Kościuszko/Lubecki dates. NEEDS_CONFIRMATION 'The relevant people's pages' (2026-11-25) lists it as unruled; TODO 70a mirrors it.
