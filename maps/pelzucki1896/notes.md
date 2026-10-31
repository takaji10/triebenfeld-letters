# Pełzucki 1896 — the plan of the Łazińskie Holendry peasant lands

The sixth map in the edition (docs/ADDING_A_MAP.md), named by the editor on
2026-10-31: the file `4456_full.jpg` in the Szreniawa museum's AN-4456 unit on
J:. Brought in with the labelling page's two new conveniences (below).

## What the map is

The plan of the lands that passed into the ownership of the peasants of the
village **Łazińskie Holendry** (the edition's `lazinskie-oledry`, the Olęder
settlement south of Łazy), gmina Tromczyn (Trąbczyn), Słupca uezd, Kalisz
Governorate. Drawn in 1896 by the staff land surveyor of the 2nd class
**Г. А. Пелзуцкій** (G. A. Pełzucki — the surname's reading is marked
uncertain in the transcription, NEEDS_CONFIRMATION); scale **1:4200 in
Russian measure**, from the sheet's own line «Масштабъ русской мѣры 1:4200».
The sheet the museum holds is the **certified copy**: examined and passed
(copy certified at Kalisz, 27 March 1898), issued with the official seal to
the village's peasants on **19 July 1900** under Article 1465 of the
Establishment Committee's decree.

This is the map the gazetteer cites as **Pełzucki 1896** (the appearance of
Glinianki, `reference/gazetteer/glinianki.yml`); its short form stays. The
plan appears in Mielewczyk's 2017 study of the Szreniawa museum's village
maps (`literature/mielewczyk2017`), which names Pełzucki among the surveyors
of the museum's holdings.

## The images of the unit AN-4456

- `4456-1.jpg` … `4456-5.jpg` — the five sheets of the plan (the title
  block's «на пяти листахъ» agrees). Sheet 1 carries the title block, the
  certification texts and the explication.
- `4456_full.jpg` — the five sheets assembled by the editor into one mosaic
  (the sheets are pieces of one map and overlap at their edges). **The
  mosaic is the map of record** (the editor's word, 2026-10-31), 21715 ×
  14206.
- `legend.jpg`, `legend_2.jpg`, `eksplikatsia.jpg`, `written_text.jpg` —
  detail photographs of sheet 1's title block, description of adjoining
  lands, explication and certification texts, transcribed in the unit's
  `*_transcription.md` / `*_translation_en.md` files. The transcriptions
  and their English are the editor's; the German on the map's page is
  Claude's, made against the English.
- `4456-1.psd`, `TIF/`, `JPG/` — the editor's working copies and the
  half-sheet scans; not used by the pipeline.

## The texts on the sheet (on the page in Russian, English and German)

The page shows the three texts in the original Russian with the translation
under (the English page the English, the German page the German):

- the **title block** (cartouche): the title, the surveyor, the five sheets,
  the magnetic needle's deviation of 7°30′ west of the true meridian, the
  survey of 1896; signed by the surveyor and by the Commissioner for Peasant
  Affairs of the Słupca uezd;
- the **certification texts**: the original plan examined and passed
  (Межевой Ревизоръ, Непремѣнный Членъ, За Предсѣдателя, Межевой Техникъ);
  the copy certified at Kalisz, 27 March 1898; the copy issued 19 July 1900
  under Article 1465 of the Establishment Committee's decree; the scale
  line;
- the **description of adjoining lands** (Описаніе смежныхъ земель, the
  unit's `legend_2.jpg`, transcribed in `legend_2_transcription.md`): the
  boundary walk round the plan's perimeter in 20 stretches keyed by stamped
  letters (А–У), in two sections (Участокъ № 1 and № 2) and three uezd
  groups — Słupca uezd, then Konin (Biskupice, Czarnybród), then Słupca
  again. The neighbours: the manor farm Włodzimirów and the forests,
  homestead and parcels of the Trąbczyn estate, the peasants of Osiny,
  Michalinów and Huta, the felled forests Maradz and Wypalanki, the forest
  of Łukom, Stawisko. Row 16's right-hand stamp reads А out of sequence
  (probably a mis-stamp for Р); rows 19 and 20 close the loop;
- the **explication** (Экспликація), the land-area table: the basic allotment
  870 desyatinas 1454 square sazhens (842+28), the additional allotment 197
  desyatinas 2218 square sazhens (192+5), the total 1068 desyatinas 1272
  square sazhens; one desyatina is 2400 square sazhens (about 1.09 ha), one
  square sazhen about 4.55 m². The figures sum correctly, which supports the
  digit readings.

Carried in `texts.yml`, rendered by the `map` layout's "Texts on the sheet"
section (docs/MAPS_SITE_PLAN.md, section 3).

## The georeferencing

The editor's MapWarper points (map **104898**, "Łazińskie Holendry ca.
1896") were made on the **single sheet `4456-4.jpg`** (7454 × 7392), not on
the mosaic: `mapwarper_image` names the sheet and `mapwarper_fit`
[scale, tx, ty] in `reference/maps.yml` moves the fetched points into the
mosaic's pixels (pipeline/maps/mapwarper.py). The fit itself was found by
patch correlation in `scratch/map4456/` — see "The mosaic fit" below.

## The labelling page's new conveniences (the editor's word, 2026-10-31)

- **The type of place fills itself in**: choosing a gazetteer place for a
  label sets the label's `shows` from the place's `kind` in the gazetteer
  (a village for a village, water for a stream; the mapping is KIND2SHOWS in
  pipeline/maps/label_page.py), and the label saves at the end of the trace
  without the third step. A type the editor chose by hand is never
  overwritten; kinds the gazetteer holds that no button covers (mounds,
  locale, unknown…) leave the step as it was.
- **The place-name section moved to the top**: "+ New label" and its form
  stand above the To find list (the form's position in the panel follows the
  list).

## Open (NEEDS_CONFIRMATION carries the list)

- The surveyor's surname (Пелзуцкій / Пелзуцкимъ) and the commissioner's
  (Жемчужинъ or Жемчугинъ) are uncertain readings of the transcription; the
  register records the Polish form Pełzucki from the editor's short form.
- The date "27" of the 1898 certification is a best reading.
- The mosaic's fit (below) is approximate where a sheet's edge sits inside
  its neighbour's overlap; the marks are made on the mosaic, so the fit's
  error rides on every label's pixel.

## The mosaic fit (scratch/map4456/, not committed)

The sheets sit in the mosaic at scale 1.00, matched by zero-normalized patch
correlation (validate the matcher on a self-match first: the first three
takes of the fit script had the numerator's mean-subtraction and the local
sums' conjugate wrong, and every "match" was noise). Sheet 1 locks at score
0.986; the per-sheet (scale, tx, ty) written into `mapwarper_fit` is sheet
4's, which is the one the MapWarper points need.
