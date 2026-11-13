# -*- coding: utf-8 -*-
"""The text of the letters of APŁ 39/98/0/-/1333 (documents 2 to 6); the index (document 1) is intake/index.csv.

DOCS: {document number: [(page id, text)]}. A page id is the folio and the
side: "0088_a" for folio 88, "0088_b" for 88 verso; the index pages are the
scan's number, "0001_a" to "0014_a". The letters are transcribed by
paragraph (rulings.yml, pages: by_paragraph): one line of the text here is
one paragraph of the page, or one line of a heading, a dateline or a
signature.

Sources of the text (notes.md, "Transcription"):
- documents 4 (folios 113-114), 5 and 6: the editor's own transcription
  ("О составлении ликвидационных... Тромбчин, Слупецкаго уезда ч. I
  (39_98_0_-_1333).md", 2026-11-13), kept as written but for the
  corrections listed in notes.md, each read on the image (the editor's word:
  correct only a glaring error, from context first);
- document 4, folios 114v, 115 and 115v (the image named 116): not in the
  editor's file; two independent readings by Sonnet sub-agents, settled on
  the images by Claude;
- document 3 (folios 88-89v): not in the editor's file; transcribed at the
  editor's word (2026-11-13) by the same method.

Conventions (EDITORIAL_RULES): "[?]" a word not read, "[word?]" a word read
with doubt; the writers' spelling, accents and joined prepositions stand; a
punctuation dash is " — "; superscript letters are written inline (Wgo,
6ciu, 7iu, 2ch); "1°" for a superscript o after a figure. A word the writer
divides at a line end is written whole; one divided across the page end
keeps its hyphen on the first page. The catchwords at the foot of 88, 88v
and 89 stand on lines of their own (catchwords.yml). Not transcribed: the
archive's stamps and folio numbers, the pencil marks at the head of 176 and
at the foot of 163 (167, "A M").
"""

PLAN = '0041_a'

DOCS = {
    # 2: the plan of the village of Trąbczyn, 15 May 1865 (No. 30 of the index,
    # folio 41): shown as an image, not transcribed (the editor, 2026-11-13).
    2: [(PLAN, '(skipped)')],

    # 3: Miączyński's petition of 10/22 August 1865 against the decision of
    # the commissar of the 5th district on six farms of Nowa Wieś (No. 59).
    3: [
        ('0088_a', '''№ 1441
10/22 Августа 1865.
do
Wysokiej Komissji dla spraw
włościańskich
w Kaliszu.
Za decyzją zdnia 13/25 Maja 1865 № 83 w ocenieniu i zatwierdzeniu praw włościan dóbr Trąbczyna, przez Wgo Komisarza 5 Rewiru, wydaną, uznanych zostało sześć osad we wsi Nowa wieś w tabelli prestacyjnej z r. 1846 zapisanych pod Nmi 2. 4. 5. 6. 9 i 10, po 5 morgów każda; za ulegające powrotowi, ostatnio posiadającym takowe gospodarzom, albo ich sukcessorom, wraz z zasiewami i budynkami jakie przy opuszczeniu osad pomienionych na gruncie znajdowały się. —
Decyzja powyższa Wgo Komisarza jako zbyt uciążliwa dla właściciela dóbr, zniewala Go do wystąpienia obecnie przed W. Komisją — z prośbą o jej uchylenie — i pozostawienie
Объ [обмѣнѣ?] признать земли, которыя были прежде заняты крестьянами пустками — но такъ какъ ихъ возвратить нельзя, то поручить [Комм…?] добровольную сдѣлку, а потомъ назначить.
Dowody [oddane?] odebrałem.
Kalisz dnia 11 [Paźdz.?]
[A. Kowal…?]
osad'''),
        ('0088_b', '''osad pomienionych na własność dominii directi; ku czemu przedstawiają się następujące Zasady:
Wgo Komisarz 5 Rewiru wyrzeczenie Swe oparł, na mylnem przedstawieniu [czynionem?] przez włościan, prawa do osad quaestionis roszczących, albowiem w motywach wyrzekł:
1° Jakoby właściciel usunął samowolnie z Nowej wsi 6ciu włościan —
2° Jakoby to uczynił w celu przyłączenia tych osad, do gruntów folwarcznych. —
W chwili wydania Najwyższego Ukazu z r. 1846 w Nowej wsi znajdowało się ośm osad włościańskich — obejmujących po mórg 5 — jedna mórg 5 prętów 25 i jedna mórg 5 prętów 75 — które były w posiadaniu rolników aż do r. 1856, ta lokacja włościan, naówczas była bardzo wygodna dla właściciela — i nigdy o żadnej zmianie niemyślał. Dopiero sami włościanie Nowej wsi, ponosząc nieustanne klęski w gospodarstwie skutkiem nazbyt niskiego położenia gruntów, w latach mokrych niezdolnego do uprawy, zgłosili się
z usilną'''),
        ('0089_a', '''z usilną prośbą, o przeniesienie ich w inne miejsce. Właściciel więc, jedynie tylko pragnąc polepszenia bytu swych włościan, i uwzględniając niekorzystne dotychczasowe ich osiedlenie, powyznaczał gdzieindziej grunta i na takowych pozaprowadzał odpowiednie budynki; lecz wprzód już, zanim to nastąpiło to jest przed r. 1856, sześciu gospodarzy, którzy najwięcej podczas lat mokrych ucierpieli, dobrowolnie niezadając nowych osad — i udając się w służbę, swoje opuścili — pozostawiwszy je pustkami; wówczas to właściciel w ścisłem zastosowaniu się do Ukazu Najwyższego z r. 1846 — i spełniając obowiązek w Art. 2 pomienionego prawa na właściciela dóbr włożony, zniewolony był postarać się o innych ludzi, którzyby osady opuszczone w ciągu dwóch lat zajęli; lecz niemogąc wynaleźć takich coby w Nowej wsi — w dawnych miejscach klęsk i niepowodzeń poprzednich posiadaczy, chcieli się osiedlić; był przymuszony za tamte, wydzielić dla nich osady z własnych folwarcznych gruntów, a przez nich zająć się mające — obrócić na folwarczne, gdzie obecnie zaprowadzony został płodozmian — a budynki przeznaczone dla dworskiej czeladzi. Skoro więc włościanie, dziś dochodzący swych praw, dobrowolnie swe osady w Nowej wsi opuścili, (co niepotrzebuje żadnego dowodzenia, albowiem właściciel przemocą niemógłby ich rugować) Skoro dalej w myśl Art. 2 ukazu z r. 1846 — właściciel był wkoniecznym obowiązku postarać się o nowych włościan którzyby opuszczone siedziby zajęli, a ci nowi jako zupełnie reprezentujący poprzednich zgodzili się nawet tego wyraźnie wymagali, aby byli w nowe miejsca przeniesieni, co uskutecznionem zostało, albowiem po dziś dzień takowe zajmują, — i w nich już
uwłaszczeni'''),
        ('0089_b', '''uwłaszczeni zostali — jakimże sposobem pierwszych sześciu czyli obecnie sukcessorowie (którym Wgo Komisarz własność przyznał) mogą mieć prawo żądać powrotu osad, które jako opuszczone, prawnie oddane — i wskutek woli ich zamienione zostały; ta zamiana wreszcie zamieszczona w tabelli dodatkowej z r. 1846 i przez Naczelnika Powiatu oraz Komisją Spraw Wewnętrznych — zatwierdzona, ma moc obowiązującą. Tym sposobem właściciel dóbr za dogodzenie interesowi włościan, przyjście prawdziwe im w pomoc, dwa razy jedne grunta oddawać byłby zmuszony, a co większa, poniósłby znakomite szkody, gdyby W. Komisja w miejsce zaprowadzonego płodozmiennego gospodarstwa, osady wymierzać postanowiła. — Art. 6 Najwyższego Ukazu z r. 1864 wyraźnie stanowi: że tylko te grunta powrotowi ulegają, które bez zamiany na inne grunta — przeszły w rozporządzenie dziedziców, tu zamiana nastąpiła odpowiednio do Ukazu z r. 1846
Dziś, na mocy Art 8. Najwyższego Ukazu z r. 1864 tylko ci, którzy w miejsce żądających, nastąpili, mogliby żądać powrotu do pierwszych siedzib, ale w żadnym wypadku niemają prawa opuszczający gospodarstwa, jeżeli pustki po nich prawnie zajęte zostały (co nastąpiło) i na zasadzie Najwyższych Ukazów tak z r. 1846 jakoteż z r. 1864 praw do własności, dla takich włościan wywieść niepodobna.
Ztąd się okazuje: że właściciel dóbr, nietylko samowolności żadnej niedopuścił się, ale przeciwnie, postąpił prawnie z wolą włościan.
Gdyby fakta powyższe miały być zaprzeczone, w takim razie właściciel odwołuje się do zeznań świadków i na takowych podaje: 1° Wawrzeńca Sowińskiego — 2° Józefa Czajkę — i wielu innych — o przesłuchanie których upraszać ma zaszczyt.
W końcu zwrócić należy uwagę na tę okoliczność: iż stosownie do rejestru pomiarowego w dobrach Trąbczynie włościanie ogółem posiadają więcej gruntów, jak według tabelli prestacyjnej im przypada, gdzie więc prawa włościan są przyznane i szanowane, tam zbytnie i nieprawne żądania, żadnego uwzględnienia znaleść niepowinny — i dla tego właściciel dóbr ufny że W Komisja oceniając słuszność, prośbie tej skutek nadać raczy —
Co do pastwiska — to włościanie z Nowej wsi nigdy niemieli wspólnego z dworem. —
Dowody w liczbie sztuk 4 dołącza się.
Kalisz dnia 10/22 Sierpnia 1865.
Z głębokim szacunkiem
W. Miączyński'''),
    ],

    # 4: Miączyński's petition of 23 July 1865 against Baron von Rosen's
    # decision granting Krystian Lippeldt pasture at the "smugi" (No. 75).
    4: [
        ('0113_a', '''№ 1805
Do Wysokiej Komisji dla spraw Włościańskich Powiatu Kaliskiego.
Jak przekonywa załączająca się decyzja Wielmożnego Barona v Rosen, przyznane zostało niejakiemu Krystianowi Lippeldt służebność pasania 2 koni i 7iu sztuk bydła rogatego na majem territorium a mianowicie na folwarku Włodzimirów w miejscach zwanych smugi. Ponieważ Krystjan Lippeldt jest z wsi sąsiedniej dla niego żadnych obowiązków zaciągać nie pragnę — przeto udaję się z prośbą do Wysokiej Komisji o zniesienie tej decyzji a w poparciu takowej przedsta-'''),
        ('0113_b', '''wiam następujący czyn:
Na folwarku Włodzimirów, do Dóbr moich Trąbczyn należącym, gdzie jest wielopolowe gospodarstwo, posiadam jedyne pastwisko dla młodocianego inwentarza. Tam niekiedy przyjmuje za opłatą lub bezpłatnie, inwentarz moich sąsiadów. Rzeczony Lippeldt będąc z Dominium w styczności przybył do mnie z prośba o dozwolenie mu pasania, siedmiu sztuk bydła i dwóch koni na tem pastwisku za opłatą pieniężną, lub odrobieniem w żniwa.
W jednym polu nad granicą Emilienhejm, znajdują się trzy dołki tak zwane smugi, a że to pole ugorowało w ten czas kilka lat i szkód nie mogłem się obawiać; dozwoliłem mu paść'''),
        ('0114_a', '''wspomniany inwentarz na tych dołkach, ale tylko do 1 Listopada tego roku, na opłatą pieniężną, którą później zmieniłem na usilne prośby jego na robociznę i dla wiadomości mojej Administracji, piśmienne me na to dałem pozwolenie.
Ponieważ jak powiedziałem, to pole ugorowało, więc w następnych latach, Lippeldowi zgłaszającemu się, zawsze na wiosnę, pozwalałem paść na tych dołkach, a teraz twierdzi że Najwyższy Ukaz zastał Go w używalności tego pastwiska. Przeciwnie kontrakt jego z roku 1863 skończył się 1 Listopada a zatem przed wydaniem Najwyższego Ukazu, a nową umowę piśmienną zrobiono 1 Maja 1864 roku a zatem po wydaniu Najwyższego Ukazu.'''),
        ('0114_b', '''W tym roku zawarł także załączający się kontrakt — którego się zrzekł, i zwrócił oryginał przy obecności byłego Rządcy Swiderskiego. —
Z powyższego opisu okazuje się że Lippeldt nie miał żadnych służebności na gruncie moim — że używał go wprawdzie na pastwisko, ale tylko za czasowem dozwoleniem — które nawet dla włościan nie może stanowić tytułu do służebności przeciw dziedzicowi — a cóż dopiero dla człowieka z obcej wsi — który dla gruntu jaki dziś zagarnąć pragnie nic nie uczynił — żadnej nie przyniósł korzyści —
Sądzę więc że gdyby nawet Lippeldt dowiódł użytkowania to nigdy jednak służebność przyznaną być mu nie może, bo Najwyższy Ukaz obejmując swemi dobrodziejstwami ogół włościan Królestwa — jednak głównie'''),
        ('0115_a', '''działa na korzyść włościan tej wsi, w której wzrasli — i pracą swą dobrze się zasłużyli.
Wreszcie Lippeldt nie może dowieść używania, — aby posiadać jakie prawa — trzeba podług przepisów art 1. 5. [11.?] i innych Najwyższego Ukazu użytkować z tego prawa w czasie wydania Ukazu. Lippeldt użytkował przed Ukazem zawarł nowy Kontrakt po Ukazie od którego sam dobrowolnie odstąpił, — ale nigdy nie użytkował w chwili Ukazu — a to właśnie jest główną zasadą do pozyskania jakich praw przez Ukaz włościanom zagwarantowanych. —
Ponieważ więc Lippeldt jako obcy nie może czerpać Łask ze wsi Włodzimierowa. — Ponieważ tenże w czasie'''),
        ('0115_b', '''Ukazu nie pasał w miejscu zwanem smugi — przeto mniemam — że tenże i dziś żadnych praw na te Smugi zyskać nie może — upraszam więc Wysokiej Kommissji o zniesienie decyzji Wgo Kommissarza. —
Trąbczyn
dnia 23 Lipca 1865 r.
W. Miączyński'''),
    ],

    # 5: the petition of the Łazińsk colonists of 6/18 December 1867 to the
    # Constituent Committee (No. 102).
    5: [
        ('0163_a', '''№ 19838/4098
Interes Spraw Włościanskich
Do Komitetu Urządzającego w Królestwie Polskiem
Prózba
Kolonistów z Łazińska, Gmina Trąbczyn powiecie Słupeckim, Gubernii Kaliskiej zamieszkałych, o przyznanie praw przywilejów nadanych przez dawne Dominium.
Jak załączony kwit pocztowy przekonywa, w. r. b. podaliśmy prośbą do Komitetu Urządzającego celem przyznania nam serwitutów w dawniejszych latach nam przez Dominium przyznanych i zapewnionych, to jest wolnego pastwiska, w lesie Trąbczyńskim, grabienia ściółki, Kopania pieńków i Sp. a przecież dotąd żadnej nie odebraliśmy decyzji, zatem upraszamy jak najpokorniej, o wydelegowanie Urzędnika bezstronnego z Bióra Powiatu Słupeckiego dla bliższego sprawdzenia naszych pretensji, a następnie zadecydowania o ile nam prawo to służy i Decyzję tą przesłać na ręce Wielmożnego Naczelnika Powiatu Słupeckiego.
Z [uszgłębonem?] uszanowaniem w imieniu drugich —
wierni poddani —
xxx Daniel Hohm
xxx Wilhelm Moritz
w Łazińsku dnia 6/18 Grudnia 1867 r.'''),
    ],

    # 6: the petition of the Łazińsk colonists of 10/22 August 1868 to the
    # Constituent Committee (No. 112).
    6: [
        ('0176_a', '''№ 16658/2133
Do Wysokiego Komitetu Urządzającego w Królestwie Polskiem w Warszawie
Najpokorniejsza Prośba
Kolonistów z Kolonii Łazieńskiej Gminy Trąbczyn, powiatu Słupeckiego Gubernii Kaliskiej o przyznanie i zatwierdzenie praw w przywileju wymienionych
Wedle Kontraktu kupna Osad, od Księcia Hohenlohe b. Dziedzica Dóbr Trąbczyna i nadanego nam przez Niego przywileju prawa, w roku 1805 — wolno nam paść Inwentarze w Leśie wspolnie z dworskiem na Rewiorże Studźienkowskim do granicy Biskupskiej — wolno nam także [gajć?] się w Boru furami 2 dni w tydzień i grabić Ściółką każdego roku — i oprócz gruntu ornego, mieliśmy 6. mórg gruntu gliniastego na kopalnie gliny do swojej potrzeby — i to wszystko J.W. Komisarz Baron Rosen przyznał nam, za prawne i do dostarczenia, nam potrzebnych, dowodów i złożenia Mappy'''),
        ('0176_b', '''hipotecznej z roku 1805 na dzień 3/15 Sierpnia Dziedzica zobowiązał — co w każdym czasie Świadkami pod przysięgą udowodnić zdołamy. Lecz kiedy Dziedzic w roku 1838 nową Tabelle ułożył, i rewior na którym, mieliśmy pastwisko na 3 Rewiory podzielił, i na 2ch wcale paść Bydła, zabrania, a na trzeci część i, zrobił 11 porębów i zagaja, a my pastwiska nie mamy — ugaju i grabienia Ściółki nie dozwala, kopalnią gliny na rzecz swoje odbiera — i do ułożenia nowego prawa i Tabeli w czasie przybycia Komisarza Wielmożnego Władimirowa, przedstawił fałszywych Świadków i dał im, po 12 Rubli, za to aby tak świadczyli jak on twierdzi — i nato są Świadkami: 1. Marcin Rywarski i 2 Libner Stolarz w Wsi Trąbczynie zamieszkali — a nawet jeden świadek, dziedzica Tomasz Janicki sam o tem oświadczył.
Aby więc nie być pozbawionymi tych służebności, zanieśliśmy trzy prośby do J.W. Prezesa Komisji Kaliskiej Spraw Włościańskich, a mianowicie: w dniu 6/18 Czerwca, 30 Czerwca/12 Lipca, i 3/15 Września roku'''),
        ('0177_a', '''zeszłego 1867 a następnie w miesiącu Październiku do Wysokiego Komitetu i załączliśmy na dowod kopią przywileju i nato uzyskaliśmy odpowiedź, z daty 31 Stycznia roku 1868 odsyłajacą nas do Komisji Kaliskiej Spraw Włościańskich.
Lecz gdy do obecnej Chwili upragnionego skutku ani żadnej Decyzji nie otrzymaliśmy, i Kopia przywileju zwróconą nam nie jest — udajemy śię więc osobiśćie z jak najpokorniejszą powtórną prozbą do Wysokiego Komitetu Urżądzającego i błagamy na klęczkach:
„Aby Wysoki i Sprawiedliwy Rząd Dziedzicowi Dóbr Trąbczyna odbierania nam w prawie zapisanych służebności zakazał wyprowadzenie ścisłego Śledztwa na gruncie zarządził, i do dopełnienia takowego Urzędnika z Warszawy wydelegował — oraz oddanie nam w posiadanie i używalność wspomnianej Kopalni, gliny i pastwiska w dawnej obszerność i dawnych granicach polecił, ugaju kopania pieńków i grabienia Ściółki bronienia'''),
        ('0177_b', '''zakazał — dawne prawo łaskawie nam zatwierdzić raczył.”
Tym bardziej że obok posiadania prawa lub przywileju Najwyższe Ukazy w posiadaniu powyższych, przedmiotów nas zastały — co gdybyśmy nie udowodnili, koszta prowadzenia Śledztwa na siebie przyjmiemy.
Ufamy i mamy mocną nadzieję że Wysoki Rząd jedyna nadzieja, nasza nie dozwoli, Dziedzicowi, czynienia nam tak wielkiej krzywdy, ale raczy łaskawie i litosćiwie przychylić się do naszej błagalnej prośby — sprawiedliwość wymierzy, i do posiadania i używalności rzeczanych — służebności Decyzją swą łaskawie nas przywróci. —
O co w najgłębszej pokorze błagamy. —
Najuniżensi podnożki,
Ludwig Hintz
Krystyan Sehr
Kolonia Łazieńska dnia 10/22 Sierpnia, 1868 r.
w Imieniu Ogółu —'''),
    ],
}

# The office's notes on someone else's paper (office_notes.yml): on 88, the
# Commission's resolution in Russian in the left margin and, below it, the
# receipt of the proofs returned; they stand at the end of the page here.
OFFICE = [(3, '0088_a', 'Объ [обмѣнѣ?] признать земли', 4)]
