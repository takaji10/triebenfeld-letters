# SPOT SHEET — Rusiński 1947, OCR draft review

Crops: `literature/rusinski1947/spot_crops/S<n>_*.png`.
Each item: what the draft says, what is doubtful, my reading,
the alternatives. A tick or a correction per item is all I need.

## A. Boundaries / note structure

**S01 — p. 50 (scan 0065): the quotation after "W nielicznych wypadkach".**
The body ends mid-sentence ("…W nielicznych wypadkach", the sentence
resumes on p. 51 "wybór wymagał zatwierdzenia…"). Then follows the
old-Polish quotation "z pierwszego małżeństwa dzieci równo należeć maią…",
and then note "1 Kar. II, fol. 239.". I read the quotation as NOTE 1 of
p. 50 (the wilkierz quote; its marker + first words sit on a line that
defeats OCR even at 6x — left as body text in the draft). If it is a
note, it also needs its marker's anchor in the body (which word carries
marker 1?). Crop: S01.

**S02 — p. 14 (scan 0029): is the long commentary ONE note or several?**
Note 1 = "Podaną cyfrę trudno skontrolować…" runs ~9 printed lines of
settlement commentary (Dąbrowo, Grabowiec, Łoskońskie… Goraj) set solid,
no readable marker digits. I take it as one note; if the print splits it
(2., 3. …), the split points are in the crop. Crop: S02.

## B. Numbers (each could change a figure)

**S03 — p. 24.** Draft: "wynosi 13.915 dymów… brak zatem 552 dymów"
Why doubtful: 13.915 conflicts with the arithmetic (13.353+552=13.905); 552×6,41=3.538 fits the given person-count. My guess: 13.905 (the total is the misread digit). Crop: S03.

**S04 — p. 26.** Draft: "514 dymów… współczynnik 6.05, otrzymamy 3.122 osoby"
Why doubtful: 514×6,05=3.110, not 3.122. My guess: either "516 dymów" or "3.110 osób". Crop: S04.

**S05 — p. 68.** Draft: "na włókę liczono 50 lub nawet 608 morgów"
Why doubtful: 608 impossible (a włóka = 60 morgów); the trailing 8 looks like a footnote marker fused to "60". My guess: "60 morgów" (the 8 = marker 4?). Crop: S05.

**S06 — p. 66 (Tabela V).** Draft: "kościański … 45,5 | 6,8 | 41,7"
Why doubtful: the row must sum to 100 and 41.7% of 44 settlements ≠ 21. My guess: third value "47,7" (21/44). Crop: S06.

**S07 — p. 43, note.** Draft: "W r. 1043 olędrom Marianowa przedłużono dzierżawę na lat 30"
Why doubtful: impossible year; the same note's context is 1677+. My guess: "r. 1643". Crop: S07.

**S08 — p. 30, note.** Draft: "Inwentarz z r. 1053 odróżnia wsie polskie…"
Why doubtful: impossible year; the parallel note cites the same inventory as r. 1653. My guess: "r. 1653". Crop: S08.

**S09 — p. 16.** Draft: "Tp. 89, 90 — Wymysłowo, 1889 — 1 dym, 1890 — 1 dym"
Why doubtful: impossible years; the passage is about Tp. 89/90 = 1789/1790. My guess: "1789 — 1 dym, 1790 — 1 dym". Crop: S09.

**S10a — p. 98.** Draft: "Jest jednak od niego 21 razy większa. Czynsz wynosił 2627 zł."
Why doubtful: 6588/2627 ≈ 2.5, not 21. My guess: "2½ razy większa". Crop: S10a.

**S10b — p. 98.** Draft: "na włókę przypadnie: w Nowych Dworach 8814 zł"
Why doubtful: larger than the 3187 zł total. My guess: "88 zł 14 gr". Crop: S10b.

**S11 — p. 86.** Draft: "wahając się… od 301 do 70? tynfów"
Why doubtful: range must be 30–70 (przeciętnie 50). My guess: "od 30 do 70 tynfów". Crop: S11.

**S12 — p. 77.** Draft: "wyszynk roczny wynosił 229 beczek 56 garncy piwa, oraz 12 beczek -12121/ garnca wódki"
Why doubtful: digit mush; the beer/wódka ratio suggests 12 beczek i 12½ garnca. My guess: verify both numbers. Crop: S12.

**S13 — p. 78.** Draft: "garnca berlińskiego, który zawierał 4:58 litra"
Why doubtful: the colon is not a decimal separator in this book. My guess: "3,58" or "4,58 litra". Crop: S13.

**S14 — p. 68.** Draft: the inline table: włóka area per pręt length
Why doubtful: the draft reduced it to glyph soup; recoverable: 7½ łokci→16,80 ha; 8→19,10; 8½→21,58; 9→24,20 (math checks). My guess: confirm the four pairs. Crop: S14.

**S15 — p. 98.** Draft: "przyorali sobie 52/5, a w Folsztynie 4%/, włóki"
Why doubtful: fraction glyphs; the Folsztyn figure fits ~4¾. My guess: read both fractions. Crop: S15.

**S16 — p. 47.** Draft: "wyjątkowo 59/, sumy sprzedażnej"
Why doubtful: "5%" or "5/9 of the sale sum" — different meanings. My guess: carried from the earlier sitting. Crop: S16.

**S17 — p. 100.** Draft: "nie przekroczy 109%/; kwoty czynszowej"
Why doubtful: 109% of the rent is odd; possibly 1/9 or 10%. My guess: read the glyph. Crop: S17.

**S18 — p. 43.** Draft: "W Ol. Ujskich dzierżawa wynosiła 44 lata 3, w Ol. Nowe Dwory 60 lat"
Why doubtful: the stray "3," after "lata" — marker 3 riding the number?. My guess: confirm "44 lata" and the "3". Crop: S18.

## C. Markers and labels

The print sets its footnote markers as inline full-size digits, so a
standalone digit in text is ambiguous (marker vs number). Where the
context looked number-like I KEPT the digit and placed the label after
it — those placements are listed in `spot_numctx.csv` (206 items) and
deserve a glance: if a listed digit is actually the marker, the label
sits one token late (harmless); if it is a real number, all good.

123 footnote definitions lack their in-text anchor
(`spot_orphan_defs.csv`: printed page, note no., text). They are real
notes; their markers were lost by OCR. Locating them needs the print
(the page crops on request).

Pages whose recovered markers fall short of the note count:
6, 20, 29, 36, 45, 47, 48, 53, 57, 58, 65, 67, 68, 72, 74, 77, 78, 79, 80, 86, 87, 88, 89, 96, 101, 103, 104, 105, 108, 109, 114, 115, 117, 119, 120 — the missing markers' positions are the crop targets.

## D. ANEKS I tables

Column splitting is a separate open task; what needs YOUR eyes is row
IDENTITY: duplicated rows, merged rows, broken numbering (the list is
in `spot_annex.csv`, worst: sheet 0142 rows 48–61; sheet 0144 rows
75–86 doubled; sheet 0146 the Razem row merged into row 111; sheet
0143's 85/80 misreads as 65/60). Full-sheet crops: S20, S21, S22.

## E. The German petition, p. 97

The 1743 petition of the Ujskie Olędry is quoted in German at length;
the OCR is heavily corrupted ("Allcrgnidigst", "gintzlich"). If the
quote matters for the edition, it needs a careful re-read (crop S19);
otherwise mark it "quote, corrected against nothing" and I leave it
as-is with a sic.

## F. Resolved without you (for the record)

- p. 8: the solid-set note block = ONE long note (verified by a 6x
  read of the number column: single marker "1", then 2, 3, 4 —
  Beheim/Kremmer/Zmiany are notes 2-4).
- p. 8/9, 14, 18, 28, 43, 50/51: the "footnote merged into body" class
  — all traced to psm4 line fusions and marker-glyph misreads; fixed
  in the parse, verified by band reads.
- The percent/fraction artifact family: 99 tokens each re-read at 5x,
  the glyph itself decided; 92 fixes applied. The residue is in §B.
- "44 lata / 60 lat" (p. 43), "co 4 tygodnie" (p. 53) — the numbers the
  earlier draft had lost behind footnote labels are back in the text.
- The wilkierz clause numbering (ANEKS III): the print's markers
  2.-44. are largely unread — flagged in §D-adjacent, crops on request.
