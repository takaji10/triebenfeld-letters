# Kraus (2001): chapter III and Anlagen 8 and 10

Gerlinde Kraus, *Christiane Fürstin von der Osten-Sacken: Eine
frühkapitalistische Unternehmerin und ihre Erben während der
Frühindustrialisierung im 18./19. Jahrhundert* (Stuttgart: Franz Steiner
Verlag, 2001; Beiträge zur Unternehmensgeschichte, Bd. 10; ISBN
3-515-07721-9). Added 2026-10-22 at the editor's word: the scans are in
`D:\Pictures\Scans\Christiane, Fürstin von der Osten-Sacken (2001, Kraus)`,
"the first image contains the book's title and author, while page 2 contains
publishing details. Note that I only want to include images
2026-10-17-0022_2R.tif to 2026-10-17-0027_1L.tif, and then Anlage 8 and 10
from images 2026-10-17-0027_1R.tif to 2026-10-17-0029_1L.tif. The rest of the
images aren't important to the project. 2026-10-17-0030_2R.tif contains keys
to decipher any footnote abbreviations for when you translate into English.
For publishing on the website, display the full text."

## The rulings behind the excerpt

Asked before the work began (2026-10-22), the editor ruled:

- **Full text on the site.** The book is in copyright (printed 2001; the
  imprint forbids any reproduction and translation outside the
  Urheberrechtsgesetz). The standing rule puts such works on the site as a
  detailed summary only (docs/LITERATURE_PLAN.md, §4: Seidel 2018, Słowiński
  2023/2024, Pinkas Hakehillot). Put to the editor with that rule named, they
  ruled: "Full text, at my word" - an exception, like the TwojaSłupca report
  of 2015 in the newspapers. `visible: true`. The ruling is recorded here and
  in the work's `work.yml` header.
- **Anlage 9 and Anlage 11 are not brought in.** The Anlagen range the editor
  named (0027_1R to 0029_1L, printed pp. 325-328) holds Anlage 8 (pp. 325-326),
  Anlage 9 (pp. 326-327) and Anlage 10 (pp. 327-328, running into the first
  lines of Anlage 11 on p. 328). Asked whether the range was meant whole, the
  editor ruled: "Skip what's between." The [.]-lines in `original.md` mark the
  three places (p. 326 after Anlage 8's signature, where Anlage 9 begins; p. 327
  before Anlage 10, Anlage 9's continuation; p. 328 after the codicil's
  signature, where Anlage 11 begins).
- **The title page and the publishing page are not carried on the site.** They
  gave the bibliographic record only (`work.yml`; the CIP page also gives the
  series and ISBN). The editor's word: "Bibliography only".
- The slug `ostensacken2001` was accepted.

## The scans and the reading

Raw scans: 35 two-up page images (TIFF, 3744 x 5521), `_1L` the left page of
each spread, `_2R` the right. The nineteen pages used are converted to JPG
(2200 px long side) in the scans folder's `processed/` folder (beside the raw
scans, as the pipeline does; not in the repository). What stands before the
excerpt in the folder: 0018 the title page, 0019_1L the CIP/publishing page,
0020_2R the table of contents, 0021_1L/0021_2R the Danksagung; 0019_2R is
unidentified (huge file, not looked at closely); 0030_2R is the head of the
Quellen- und Literaturverzeichnis (p. 331) - the archive abbreviations the
editor named:

- HZAN = Hohenlohe Zentralarchiv Neuenstein; AL = Archiv Langenburg; AW =
  Archiv Waldenburg; DK = Domänenkanzlei; Ö = Archiv Oehringen; PA =
  Partikulararchiv; MSL = Manuskript Schlawentzitz: Beschreibung des
  Herzogthums Ujest, Theil I.; Rep. = Repertorium; 80 = Kasten Nr. 80; 5 =
  Fach Nr. 5; 3 = Faszikel Nr. 3.
- APK Kosz. = Archiwum Panstwowe Katowice Koszecina (as printed - no Polish
  diacritics in the key), 460 = Akte 460.
- ThHStAW = Thüringisches Hauptstaatsarchiv Weimar, RG Oppurg (as printed; the
  town is Weimar, "Oppurg" is the Rittergut Oppurg), 364 = Akte 364.

These keys are used in the English translation of the notes that need them
(note 11 "AÖ PA" = Archiv Oehringen, Partikulararchiv; "Kocz."/"Kosz."/"Koscz."
= the Katowice archive, Koszecina; "O.M.R." = Ober-Medizinal-Rath).

No transcription existed: every line was read from the page images. Two OCR
engines were run over every page - Tesseract 5.5.3 with the German traineddata
(`deu`, installed for the newspaper work; the program at `C:\Program
Files\Tesseract-OCR\tesseract.exe`, not on PATH) and the lunaroute document
converter - and the passes checked against each other. Tesseract's TSV output
located doubtful words, which were then read at 3x-6x zoom crops
(`processed/_zoom/`, not in the repository). The lunaroute pass proved the
better reader of the superscript note markers (Tesseract renders unresolved
superscripts as `?`, `*`, `'`, `"` - the closing-quote misreadings at "helfen.
" (note 30), "kam." (note 40), "verstarb." (note 41) and "vergießen werden."
(note 7) are superscript markers, not quotation marks) and of the French
letter in note 21.

The excerpt's pages and their scans:

| Printed page | Scan | Content |
|---|---|---|
| 33 | 2026-10-17-0022_2R | chapter III, heading and opening |
| 34 | 2026-10-17-0023_1L | the prince's career; house history begins |
| 35 | 2026-10-17-0023_2R | house history, Reformation, lines |
| 36 | 2026-10-17-0024_1L | the Peace of Basel, failed undertakings |
| 37 | 2026-10-17-0024_2R | the children, the two letter quotes |
| 38 | 2026-10-17-0025_1L | Bytkow purchased, Baildon |
| 39 | 2026-10-17-0025_2R | Hohenlohe-Hütte, Jena and Auerstedt |
| 40 | 2026-10-17-0026_1L | the Fürstin takes over Bytkow |
| 41 | 2026-10-17-0026_2R | the divorce, second marriage, death |
| 42 | 2026-10-17-0027_1L | the marriage contracts, the sold estates |
| 325 | 2026-10-17-0027_1R | Anlage 8 begins |
| 326 | 2026-10-17-0028_1L | Anlage 8 ends, signature; Anlage 9 begins ([.]) |
| 327 | 2026-10-17-0028_2R | Anlage 9 ends ([.]); Anlage 10 begins |
| 328 | 2026-10-17-0029_1L | Anlage 10 ends, signature; Anlage 11 begins ([.]) |

Chapter III runs pp. 33-42 whole. The chapter's note numbering runs 1-43; the
Anlagen section numbers its own notes from 1 again, so the excerpt holds two
note 4s, two note 5s and so on - the footnote keys in `original.md` and
`english.md` are therefore page-scoped (`[^p33-1]`, `[^p325-4]`), as in
Kneifel (1964), and each definition text begins with the printed number.

Note 21's text is split by the print over the footnote areas of pp. 37 and 38
(the French letter of 4 February 1792, HZAN 47, K 1, F2); it is brought whole
in the p. 37 definition, where its marker stands. Note 41's text is split over
pp. 41 and 42 (the death notice of Hofrat Mangold); brought whole in the p. 41
definition. Note 4 of the Anlagen prints at the bottom of p. 325 but its
marker is not in the excerpt (it belongs to Anlage 7's text on the unscanned
p. 324; Anlage 7 is the printed Baildon letter of 8 March 1808 that body note
30 cites as "siehe Anlage 7"). The definition is kept verbatim on p. 325; the
site's renderer may leave an unused footnote definition unshown - the text
stays in the corpus passage either way. The same holds for Anlagen note 7
(HZAN K47, F5, F1-4, the source of Anlage 9's obituary): its marker stands at
the end of Anlage 9's text, which is not brought in, its definition prints at
the bottom of p. 327 and is kept.

## Readings settled at zoom, and the print's own slips

Kept as printed, each recorded (the editor does not read German; the reasoning
is written out):

- **„Zransact“** (p. 41) - the print's own slip against its own "Transact"
  (note 42 on p. 42, and the Anlage 8 letter, p. 326). Tesseract read Z (the
  6x crop shows top bar, diagonal, bottom bar, no central stem), lunaroute
  read T. As printed: Zransact.
- **"Kompensation"** (p. 41) - Tesseract's K (TSV conf 96.6, and modern
  spelling in a book of 2001); lunaroute read "Compensation". As printed:
  Kompensation.
- **"souveräne Landeshoheit"** (p. 35) - Tesseract three times (full page,
  TSV at conf 92, and a 5x crop pass); lunaroute read "souveräre". As read:
  souveräne.
- **"Militärischen Ruhm suchte er daher er auch nicht"** (p. 33) - the
  doubling "daher er auch" in both passes; a printed slip, kept.
- **"und Baildon war die Aufgabe zugefallen"** (p. 38) - both passes; the
  author's syntax (one would expect "und auf Baildon"), kept.
- **"(1792–1822)"** for Karl August von Hardenberg in note 4 (p. 34) - both
  passes at zoom; the author's slip (Hardenberg lived 1750-1822; the Haller
  book he cites is about 1750-1822). Kept as printed.
- **"die Jahre Ihrer Vollblütigkeit"** (Anlage 8, p. 325) - the letter's own
  slip for "Volljährigkeit", in both passes and the crop. Kept.
- **"das Wohl meiner jüngsten Kinder leidet …, sterbe ich früher"** (Anlage 8,
  p. 326) - the letter's own broken syntax, both passes. Kept.
- **"ich entsagte auch zugleich des Rufes"** (Anlage 8, p. 325) - both passes
  (one would expect "dem Rufe"); the letter's syntax, kept.
- **"nur bis auf die Summe von 60/m tausendstel eintreten werde"** (Anlage 10,
  p. 328) - both passes and a 5x crop read "60/m" (the old millia notation,
  60 with a raised m = 60,000) followed by "tausendstel". The sense of
  "tausendstel" after the figure is not clear (the codicil's cap of 60,000
  thaler Courant is named a sentence earlier); possibly the archival
  document's own wording. Kept as read; the English translates literally
  ("60/m thousandths"). Open with the editor below.
- **Note 36 and Anlagen note 7 read "K47, F5"** - Tesseract read "FS" in both
  (twice each), lunaroute "F5"; at 3x the glyph's flat angular top differs
  from the true S in "S. 359" on the same line, and the book's own pattern
  elsewhere is F plus digit (note 30: "HZAN K 172, F1, F2"). Read as F5.
  Note 36's tail "1-4" has no F before it while Anlagen note 7's has "F1-4" -
  both as the two passes read them.
- The print spells the Katowice archive variously: "Kocz." (note 38, p. 41),
  "Kosz." (note 40, p. 41; note 8, p. 327; the key, p. 331), "Koscz." (note 5,
  p. 325) - each as printed on its page.
- The Anlage 8 letter's own spelling is kept: "October" in the signature
  ("Berlin 12. October 1811", confirmed at 3x) against the author's footnotes'
  "Oktober"; "thun", "Vortheil", "theils", "freyem", "Codicill", "Jussiegel",
  "Revenuen", "Fideicommiß" inside the quoted documents against
  "Fideikommiß" in the author's prose.
- The date of the Transact: p. 41 "am 9. November 1799" and note 42 "Transact
  vom 9. November 1799", the Anlage 8 letter "den Transact vom 19. November
  1799" - the book contradicts itself; each place as printed. (The edition's
  own ruling on such internal contradictions of a printed book: transcribe as
  printed, record the difference.)
- **"Verwirklicht werden"** ends p. 36 and "konnte nur der im Jahr 1782
  begonnene Bau" opens p. 37 - the sentence runs across the page break, as
  printed; likewise "Schutzvog-/tei" (pp. 34/35), "Hüttenwer-/ken" (pp. 38/39)
  and "Gläubi-/gern" (pp. 327/328) are kept broken at the page marks.
- The French letter in note 21 follows the lunaroute reading (the better
  Romance reader), with the letter's own orthographic slips that both passes
  agree on kept: "coulament" (for couramment), "come" (for comme), "pue" (for
  pu), "sont sortie tous", "s'est beaucoup formés", "s'est appliques",
  "Emilie a grandie", "des ces bonheur", "posseder", "Nits". Residual
  uncertainty: accents and some verb endings ("régulièrement"/"regulierement",
  "pleurée et rie", "grée"), which the two passes read differently; the words
  carry no fact.

## The marker positions

Every superscript marker in the excerpt was placed from the reads; the ones
settled at crops: 30 (after "helfen.", p. 40), 31 (after "Einstellung.", p. 40
- the mark after „erhalten" is the closing German quotation mark itself, high
by design), 26 (after "verbunden war.", p. 39), 36 (after "gezogen.", p. 41),
38 (after "trennen.", p. 41 - the print runs "Zur Kompensation" in the same
paragraph, no new paragraph), 39 (after "der Fürstin Sacken.", p. 41), 40
(after "kam.", p. 41), 41 (after "verstarb.", p. 41), 37 (after "erfolgte.",
p. 41 - the faintest of the set; the crop shows a small raised mark, but this
is the one placement to re-check against the page if any doubt arises), 5 of
the Anlagen (after "Schreiben", p. 325), 6 of the Anlagen (after "Gatte",
p. 326 - the note explains who "my husband" in the letter is), 8 of the
Anlagen (after "aufgenommen:", p. 327).

## What it bears on

The chapter names the edition's ground twice, both times in the prince's
story: the "Generalinspektion der schlesischen Füsilierbataillone" and the
governorship of Breslau (pp. 34), and above all p. 42 - the sale of
"die Herrschaften Betsche, Zogorowo, Trobczyn, Botkowo und Winiec weit unter
Wert" to come by "baare Mittel". Zogorowo is the edition's Zagórów and
Trobczyn its Trąbczyn; the sale of both by the prince to Countess Wielopolska
is witnessed by the edition's documents (Słowo of 4 January 1892 records
Trąbczyn's sale for 225,000 rubles; the wlodzimierz-era ownership line).
This passage answers, from a printed witness, the question the literature
section exists for: how such estates were valued and sold. The excerpt's
person story (Marianne, the divorce, the marriage contracts) is the
backdrop of the edition's own documents (the Hohenlohe letters in Oe 1 Bü
9454 and the estate papers). Hand-made links: written in `literature/
links.yml` (the p. 42 passage against the sale documents; the chapter against
the letters). See the index rulings in `literature/index.yml`.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> Its bearing: p. 42, the sale of Zagórów and Trąbczyn, which the documents of
> the later years witness. Anlage 9, which prints between the two appendices
> brought in, is not brought in, nor the first lines of Anlage 11 (marked with
> [.]) – the editor's word of 2026-10-22. The book is in copyright; shown
> whole on the site at the editor's word, an exception to the summary-only
> rule for works under copyright. Published as Beiträge zur
> Unternehmensgeschichte vol. 10 (Franz Steiner Verlag).
