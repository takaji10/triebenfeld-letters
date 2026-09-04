# Spelling audit

Demonstrable transcription slips in ordinary words. **Applied 2026-09-03**:
66 of the 106 candidates accepted and corrected in the archival text (72 token
instances -- six forms occur twice); 40 checked and kept. Each correction is
root-only, verified against `von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt.bak5`,
and rebuilt through `regenerate.py` (archival text still character-exact,
20,750 content lines, all fidelity checks green).

## The bar

63% of the distinct words in this corpus appear exactly once, and the text is full of period forms (*laßen*, *seyn*, *nöthig*, *Ewr*) that are correct as written. Frequency alone therefore proves nothing, and a pass driven by impression would damage more than it fixed. A candidate is only listed if:

1. it appears at most **2** times here;
2. a near neighbour appears at least **8** times and at least **10x** more often;
3. the single difference between them is a confusion this transcription is known to make (c/e, n/u, m/w, b/v, long-s, and so on) - not any edit;
4. the pair is checked against DWDS where a lookup exists.

The list below was then read candidate by candidate against the manuscript's
own context before anything was applied. Line numbers are corpus lines in the
canonical text; letter numbers use the archival IDs.

## Applied

| Letter | Line | Was | Now | Basis |
|---|---|---|---|---|
| 4 | 291 | `ſerden` | `ſenden` | r/n: send the servant to Schlawenschitz |
| 4 | 303 | `Schlawerschitz` | `Schlawenschitz` | r/n: place name |
| 7 | 463 | `Durchlauchſtigſter` | `Durchlauchtigſter` | long-s/t: salutation |
| 11 | 589 | `ſehleunig` | `ſchleunig` | c/e (sch>seh): "so schleunig als möglich" |
| 14 | 763 | `höchstern` | `höchsten` | excrescent r: "in höchster/höchsten Noth" |
| 21 | 1262 | `Grädigster` | `Gnädigster` | r/n: salutation "Gnädigster Fürst und Herr" |
| 29 | 1954 | `Schlawentschitz` | `Schlawenschitz` | excrescent t: place name |
| 31 | 2056 | `gestandt` | `gesandt` | non-word: "ward hierher gesandt" |
| 33 | 2357 | `Hypoteque` | `Hypotheque` | missing h; cf. "Hypothequen" elsewhere |
| 36 | 2520 | `Triebenfeldt` | `Triebenfeld` | trailing -dt: subject name (project canon) |
| 40 | 2972 | `durchlaus` | `durchaus` | excrescent l: "durchaus nichts" |
| 43 | 3204 | `gestandt` | `gesandt` | non-word: "der Befehl ... nach Warschau gesandt" |
| 43 | 3302 | `Scharden` | `Schaden` | excrescent r: "zu Schaden werde" |
| 45 | 3461 | `Zagorowa` | `Zagorowo` | a/o: place name (project canon) |
| 47 | 3625 | `wünden` | `würden` | n/r: "die Durchlaucht würden nie Zinsen erhalten" |
| 53 | 3979 | `Königberg` | `Königsberg` | missing s: place name |
| 55 | 4173 | `geſchieben` | `geſchrieben` | missing r: "um seinen Abschied geschrieben" |
| 63 | 4782 | `Schreibn` | `Schreiben` | missing e: "deren Schreiben vom 9ten" |
| 65 | 5071 | `Durchaucht` | `Durchlaucht` | missing l: "Ewr Durchlaucht haben" |
| 67 | 5476 | `Triebenfeldt` | `Triebenfeld` | trailing -dt: subject name (project canon) |
| 72 | 5617 | `Brzechsa` | `Brzechsta` | missing t: name -> majority form |
| 72b | 5806 | `Berzechsta` | `Brzechsta` | metathesis: name -> majority form |
| 72d | 5900 | `Worſchau` | `Warſchau` | o/a: place name |
| 72f | 5945 | `Sequestation` | `Sequestration` | missing r: legal term |
| 73 | 6072 | `Brezechsta` | `Brzechsta` | excrescent e: name -> majority form |
| 74a | 6168 | `Warschan` | `Warschau` | n/u: "Herzogthum Warschau" |
| 74d | 6201 | `Schreibn` | `Schreiben` | missing e: "mit diesem Schreiben eingesandte" |
| 86 | 6935 | `Palajewo` | `Polajewo` | a/o: place name |
| 86 | 6969 | `Revenuce` | `Revenue` | excrescent c: "eine reine Revenue von 11000 Rthl" |
| 97 | 7684 | `bestehnt` | `besteht` | excrescent n: "der mit der Ehre besteht" |
| 101 | 8008 | `dardurch` | `dadurch` | excrescent r: "dadurch ruinirt ist" |
| 101 | 8026 | `wordurch` | `wodurch` | excrescent r: "wodurch ich mehr gewähre" |
| 112 | 8729 | `Wechſtel` | `Wechſel` | excrescent t: "den Wechsel" |
| 115 | 8859 | `Liefster` | `Tiefster` | l/t: "zu tiefster Submission ersterbe" |
| 118a | 9026 | `Sonstern` | `Sonsten` | excrescent r: "Sonsten aber hat..." |
| 131 | 9488 | `Nußland` | `Rußland` | n/r: "das Rußland will absolut Krieg" |
| 136 | 9978 | `Intresen` | `Intressen` | missing s: "von 2 Jahr Intressen" |
| 140 | 10458 | `Geſchiehte` | `Geſchichte` | e/c: "in der Geschichte kan ich..." |
| 151 | 11019 | `erſterebe` | `erſterbe` | excrescent e: closing formula "ersterbe" |
| 161 | 11497 | `Augenblik` | `Augenblick` | missing c: "in dem Augenblick" |
| 163 | 11605 | `Durchlauchtigter` | `Durchlauchtigster` | missing s: salutation |
| 168 | 12073 | `bestreht` | `besteht` | excrescent r: "Schenck besteht absolut auf..." |
| 191 | 13916 | `glüklich` | `glücklich` | missing c: "glücklich abgemacht" |
| 213 | 15268 | `Sequetration` | `Sequestration` | missing s: legal term |
| 214 | 15452 | `Geſehichte` | `Geſchichte` | e/c: "jene Berliner Geschichte" |
| 217 | 15906 | `Triebunal` | `Tribunal` | ie/i: "aus dem ersten Tribunal" |
| 231 | 17098 | `Antworth` | `Antwort` | excrescent h: writer's own form is "Antwort" (83x) |
| 244 | 18000 | `Liefster` | `Tiefster` | l/t: "In tiefster Ehrfurcht ersterbe" |
| 248 | 18221 | `Fürstern` | `Fürsten` | excrescent r: "dem alten Fürsten" |
| 263 | 18979 | `gnädigter` | `gnädigster` | missing s: set formula "gnädigster Fürst und Herr" |
| 253 | 19707 | `Fürstern` | `Fürsten` | excrescent r: "dHl. Fürsten St. K." |
| 278 | 19991 | `Cuhrischen` | `Curischen` | excrescent h: "die Curischen Erben" (cf. L19517) |
| 281 | 20190 | `Schlowenschitz` | `Schlawenschitz` | o/a: place name |
| 281 | 20227 | `tiefstern` | `tiefsten` | excrescent r: "In tiefsten Respect verharren" |
| 287 | 20744 | `vorgesten` | `vorgestern` | missing r: "der vorgestern hier eintraf" |
| 287 | 20797 | `Bemühern` | `Bemühen` | excrescent r: "daß mein Bemühen gelingen wird" |
| 289 | 20896 | `Mandatorius` | `Mandatarius` | o/a: legal term (cf. "Kurz Mandatarius") |
| 291 | 21020 | `gesanndt` | `gesandt` | doubled n: "an Kircheisen gesandt" |
| 291 | 21050 | `konzler` | `kanzler` | o/a: "Fürst [Staats-]Kanzler" |
| 292 | 21130 | `Geheimte` | `Geheime` | excrescent t: "Geheime Rath Philippsborn" |
| 297 | 21423 | `Scherck` | `Schenck` | r/n: person Schenck |
| 299 | 21594 | `Zerbani` | `Zerboni` | a/o: person Zerboni |
| 2 | 105 | `geweldet` | `gemeldet` | w/m: "Seine Durchlaucht gemeldet daß..." |
| 4 | 278 | `läglich` | `täglich` | l/t: "der Himmel droht täglich" |
| 43 | 3282 | `getrettet` | `gerettet` | excrescent t: "circa 1500 Rthl gerettet werden" |
| 47 | 3624 | `umsamehr` | `umsomehr` | a/o: "um so mehr" |
| 60 | 4685 | `Expresen` | `Expressen` | missing s: "durch einen Expressen" |
| 64 | 4977 | `angewiſen` | `angewieſen` | missing e: "baar angewiesen" |
| 65 | 5131 | `Comision` | `Comission` | missing s: "meine Commission" |
| 228 | 16840 | `umsamehr` | `umsomehr` | a/o: "um so mehr" |
| 259 | 18667 | `einreichern` | `einreichen` | excrescent r: "einreichen sollte" |
| 268 | 19284 | `Hoffroth` | `Hoffrath` | o/a: "von Ihrem Hofrath Hahn" |

## Checked and kept

These 40 were raised by the automated pass and rejected on inspection. Recorded
here so the same candidates are not raised again. Broad reasons: valid period
forms (`hiedurch`, `geschiehet`, `kleinern`, `urtheilt`, the `-ff`/`-fft`
spellings, `gezahlet`, `gebetten`); the audit's proposed correction is wrong or
ambiguous (`vesten` = *Vestungen*, `durcht` = *deucht*, `wenschen`, `gewinnten`
= *gemeinten*, `klogen` = a place, `desten` = *dessen*); line-wrap fragments
(`geleiste`, `hochfürst`); and readings the surrounding text is too garbled to
settle.

| Form | Where | Why kept |
|---|---|---|
| `gnädigter` | L263 | audit also proposed `gnädiger` here; `gnädigster` (the set salutation) was applied instead |
| `wenschen` | L36 / L47 | context splits: `Dero Wünschen` at L36, `unter Menschen` at L47 — the audit's single target `menschen` is wrong for one |
| `durcht` | L31 (×2) | reads `deucht`/`dünkt mir` (it seems to me), not an abbreviation of `Durchlaucht` |
| `desfalls` | L108 | period orthographic variant of the house form `desfals`, not a misreading |
| `hochwohlgebohrnen` | L155 | possible deliberate inflected form of the address honorific |
| `gebetten` | L87 | period spelling of `gebeten` |
| `gewinnten` | L11 | `treu gewinnten Rath` is almost certainly `treu gemeinten Rath` (well-meant), not `gewinnen` |
| `hochwohlgebohrn` | L114 / L294 (×2) | period contraction of the address honorific (schwa-less `-gebohrn`) |
| `gesundtheit` | L227 | period spelling with excrescent -t-; surrounding line is itself garbled |
| `verkauff` | L116 | period `-ff` orthography, still current c. 1800 |
| `verkauffen` | L202 | period `-ff` orthography |
| `gezahlet` | L292 | period uncontracted participle (`-et`), correct as written |
| `kurgen` | L228 | `benen Kurgen` — surrounding text garbled; the fix does not recover a reading |
| `klogen` | L51 | `ihre Magazine aus Klogen zu Wasser [schaffen]` — `Klogen` is a place; `klagen` (complaints) makes no sense |
| `ewodurch` | L210 | `geruhen Ewodurch` — a fused/garbled reading (`Ew.` + something), not a clean dropped letter |
| `vesten` | L246 / L270 (×2) | `Vesten` = `Vestungen`/`Festungen` (fortresses; L246 wraps to `-gen`), not `besten` |
| `zukunfft` | L87 | period `-fft` orthography |
| `dürfften` | L86 | period `-fft` orthography |
| `geworffen` | L271 | period `-ff` orthography |
| `herrschafft` | L189 | period `-fft` orthography |
| `herrschaftl` | L191 | abbreviation of `herrschaftlich(en)`, line-final — not a dropped letter |
| `hiedurch` | L135 | standard period form (cf. `hiemit`, `hiebei`, `hiezu`) |
| `geschiehet` | L294 | standard period form of `geschieht` |
| `kleinern` | L10 | valid period inflected adjective (`den kleinern` = `den kleineren`) |
| `nachmahls` | L54 | `nachmals` is a real word; cannot be shown to be a slip for `nochmahls` |
| `urtheilt` | L253 | correct finite verb (`daß man ... gleichstimmig urtheilt`), not a truncation of `Urtheil` |
| `geleiste` | L87 | line-wrap fragment of `geleisteten` (`geleiste` + `ten` on the next line) |
| `hochfürst` | L182 / L245 (×2) | line-wrap fragment of `Hochfürstl. Durchlaucht` — not to be rejoined per project policy |
| `vorgesteren` | L73 | source reads `vorgestern vorgesteren` (a dittography/rewrite); needs the manuscript |
| `wohren` | L277 | `großes Kopf wohren` — garbled; `wahren` does not fit |
| `creditorn` | L245 (×2) | period syncope of `creditoren`, parallel to `andern` in the same clause |
| `gnädigte` | L284 | surrounding sentence badly garbled; reading not recoverable |
| `hicher` | L67 | reads as a surname (the sentence's subject), not the adverb `hieher` |
| `hochwolgeb` | L257 | `wol` for `wohl` is a standard period spelling |
| `eingericht` | L277 | ambiguous between `eingereicht` and `eingerichtet`; garbled context |
| `gewißert` | L177 | neither `gewißert` nor `gewißer` yields a reading; unresolved |
| `desten` | L136 | `die Bestätigung desten` = `dessen` (of what Blomberg had said), not `besten` |
| `weines` | L72a | `eben so weines als` — garble; `meines` does not fit |
| `commer` | L256 | ambiguous: `Cammer` (the chamber) or an unrecorded surname |
| `unglückt` | L251 | `gränzenlose unglückt Lage` points to `unglückliche`, which `unglück` does not give |
