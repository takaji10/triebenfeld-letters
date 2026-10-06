# -*- coding: utf-8 -*-
"""What the full check of the Polish against the scans changes in the English.

Read by build_doc1.py. The editor's English is theirs and is not redone. The
full check (intake/full_check_rows.py) found words the Polish transcription
had dropped and readings that change the sense. In most of those places the
English already had the right sense. It is changed only here:

- where the English lacks words the scan has (the dropped phrases the editor
  asked for, 2026-10-06: "You can update the English translations with
  anything that was dropped");
- where the English followed a misreading that changes who or what is meant;
- one paragraph which the English lacked altogether, at the seam between the
  editor's sections 4 and 5. It is translated here in the editor's terms,
  and the holding's process page says so.

Each entry: (words as they stood, words now, the leaf, why). Each `old` must
stand exactly once in the whole English.
"""

FIXES_FULL = [
    ("presented to the office for prosecution, and submitted for enrollment in the present records, a Commissorial Boundary Decree, setting forth in the first instance the estates specified in the said decree, to be laid before the illustrious Right Honourable commissioners, sealed with family seals",
     "presented to the present office for entry, and submitted for enrollment in the present records, a Commissorial Boundary Decree between the estates specified in the said decree, pronounced by the illustrious Right Honourable commissioners, sealed with family seals",
     '655', 'the Latin formula was filled out wrongly: "officio praesenti ad acticandum", "inter haereditates", "per ... commissarios prolatum"'),
    ("and for the convent's Drzewce — and for Drzewce and Trąbczyn Mały, for their own estates and for Łukomia with rejection, and also Bukowe",
     "and for the convent's Drzewce, with rejection only of the estate of Trąbczyn from here — while the heirs of Drzewce and Trąbczyn, for their own estates and for Łukomia, with rejection likewise of the Bukowe",
     '655', 'dropped: "z odpychaniem tylko z tąd dziedziny Trąbczyna, dziedzicy zaś"'),
    ("the Honourable Prusimski to submit and produce in court, in accordance with the enacted constitution, the collateral citations",
     "the Honourable Prusimski, satisfying both the law of the Crown and the enacted constitution, to submit and produce in court the collateral citations",
     '659v', 'dropped: "zadość czyniąc tak prawu koronnemu jako też"'),
    ("and as though from that corner mound consistently acknowledged at all times during the three field sessions by the Convent",
     "and as though from that corner mound, formed by the Honourable Prusimski before and now, and consistently acknowledged at all times during the three field sessions by the Convent",
     '662', 'dropped: "przez urodzonego Prusimskiego przedtem i teraz formowanego a"'),
    ("Tomasz and Kazimierz Czerniakowic, Tomasz and Fabian,", "Tomasz and Kazimierz Czerniak, Tomasz and Fabian,",
     '665', 'the scan has "Czerniakowie", a surname in the plural'),
    ("Piotr, Szyman, [uncertain: narożnik], Wojciech Zelak", "Piotr Szyman, Nadolnik, Wojciech Zelak",
     '665', 'the scan has "Piotr Szyman, Nadolnik"'),
    ("as having no separate boundaries but lying within the boundaries of Łukomia, Drzewce, and Trąbczyn, acknowledged it",
     "as having no separate boundaries but lying within the boundaries of Łukomia, acknowledged them as not of Bukowe but only of Łukomia, Drzewce, and Trąbczyn",
     '666', 'dropped: "leżącą nie Bukowia ale tylko Łukomia"'),
    ("acting in the matter of the ruin and wrong of the complainant with the Honourable Chełmski from the same platform",
     "acting in collusion with the Honourable Chełmski to the ruin and wrong of the complainant",
     '667v', 'the scan has "zmownie", in collusion; the transcription had "z mównic"'),
    ("he came to the fifth mound, larger than the others, not very raised above the ground",
     "he came to the fifth mound, larger than the others, flat, having a small ditch round it and likewise a roundness, not very raised above the ground",
     '670v', 'dropped: "płaskiego rowek koło siebie także okrągłość mającego"'),
    ("still extending considerably further. Therefore the Honourable Prusimski says",
     "still extending considerably further, and assert it — and these are actually found above the Lusnia woodland. Therefore the Honourable Prusimski says",
     '674v', 'dropped: "i twierdzą a te aktu nad lasem Lusnie znajdują"'),
    ("as enclosing and establishing the actual substance and ownership of all these",
     "as enclosing and taking in all this, openly vindicate and prove it for Trąbczyn — and the actual substance and ownership of all these",
     '675', 'dropped: "i zajmujące dla Trąpczyna jawnie ewinkują i dowodzą"'),
    ("as the judicial site inspection itself shows. When this judicial site inspection was conducted in 1589",
     "as the judicial site inspection itself shows, since it is attested only for his portion. And moreover, when this judicial site inspection was conducted in 1589",
     '676', 'dropped: "gdy tylko z części jego jest zeznana a nadto"'),
    ("insofar as it had been marked out with stakes.\n\n[Section 5: Review of Chełmski's Boundary Line — Trąbczyn–Biskupice Boundary — Sworn Inquiry — Resolution on the Starting Point]\n\nAnd that this road",
     "insofar as it had been marked out with stakes.\n\n[Section 5: Review of Chełmski's Boundary Line — Trąbczyn–Biskupice Boundary — Sworn Inquiry — Resolution on the Starting Point]\n\n"
     "And so the Honourable Prusimski, having taken his stand at the corner mound in the place where the Honourable Chełmski establishes his corner mound — that is, at the head, or beginning, of the woodland called Ostrowce, at the Osiny road itself, which runs between the two mounds, supposedly corner mounds of the Honourable Chełmski but in fact Drzewce and Trąbczyn wall mounds — and having led his court out onto that road toward Osiny, showed his court that this road comes not from Trąbczyn but from Osiny, and falls into the Zagórów road a few staj from here, and then also crosses the Zagórów road below the hill and goes by way of Łukom to Pyzdry — as the past decrees, one of 1759 and the other of 1760, submitted and described in the boundary line, also express.\n\n"
     "And that this road",
     '680', 'a paragraph of the Polish (about a hundred words) which the English lacked, at the seam between sections 4 and 5; it includes nine words the Polish had dropped as well'),
    ("acknowledged by the heir of Biskupice by prearranged arrangement — are acknowledged unjustly",
     "acknowledged to him by the Convent, and the second at the Lusnia woodland by the heir of Biskupice, by prearranged arrangement — are acknowledged unjustly",
     '682v', 'dropped: "przez Konwent mu, a drugi przy lesie Lusnie"'),
    ("of the entire boundary line of the Honourable Chełmski as run",
     "of the entire boundary line of the Honourable Chełmski, formed and marked out through Trąbczyn's own ground",
     '682v', 'dropped: "przez grunt własny Trąpczyna uformowanego"'),
    ("where the court, unable to conclude this boundary due to excessively high water, proceeded with further actions on the boundary lines already run",
     "where the court, unable to conclude this boundary due to excessively high water, suspended the further boundary line in it and meanwhile proceeded to further actions on the boundary lines already run",
     '683v', 'dropped: "dalszy w niej dukt zawiesił a tymczasem do"'),
    ("I have neither suborned nor bribed", "I have neither suborned, nor hired, nor bribed",
     '684', 'dropped: "nie przenajęłem", added by the clerk in the margin'),
    ("concerning the division, extracted from the Pyzdry municipal court",
     "concerning the division of Trąbczyn, Nowa Wieś, Osiny, and Łazy, extracted from the Pyzdry municipal court",
     '686', 'dropped: "Trąpczyna Nowej Wsi Osin i Łazów nastąpionym"'),
    ("by which the Trąbczyński, dividing the estates, reserve to themselves the remaining ponds",
     "by which the Honourables Trąbczyński, dividing the Trąbczyn estate, besides the ponds Garmin and Likerowa, reserve to themselves the remaining ponds",
     '691', 'dropped: "majętnością Trąpczyńską prócz stawów Garmin i"'),
    ("and thereafter not prosecuted — that the flooding was made and caused on",
     "and thereafter not prosecuted — concerning the flooding of grounds, meadows, and pastures and the drying-out of timber, made and caused on",
     '691', 'dropped: "o zalewek gruntów, łąk, pastwisk, drzewa posuszenie"'),
    ("likewise in pine, and, as it is overgrown with clumps and various trees",
     "likewise in pine; and, as it is made out of the same kind of marshes as this stawisko, so it is overgrown with clumps and various trees",
     '691v', 'dropped: "z takichże błot jako i to stawisko wyrobiony, tak"'),
    ("in this boundary above the duck bogs [i.e., to the north of the duck bogs] — as expressed above, these belong and belonged",
     "in this boundary, running above the duck bogs [i.e., to the north of the duck bogs] — since it is shown that the duck bogs, as expressed above, belong and belonged",
     '693', 'dropped: "ciągnącego się ponieważ okazuje się iż kacze ługi"'),
    ("as to this boundary, at Studzienka — and moreover",
     "as to this boundary, at Studzienka and the tavern hills and bogs lying by that Studzienka — and moreover",
     '693', 'dropped: "i karczemnych gór i ługów przy tej"'),
    ("that neither the Honourable Chełmski nor the heir of Biskupice can or should have their convergence here",
     "that neither the Honourable Chełmski a corner mound, nor the Honourable Gałecki, Starost of Bydgoszcz, heir of Biskupice, his convergence, can or should have here",
     '695', 'dropped: "narożnika ani urodzony Gałecki starosta bydgoski"'),
    ("dismissing and setting aside it as unlawful and irregular", "dismissing and setting aside it as unlawful and invalid",
     '696v', 'the scan has "nieważną", invalid; the transcription had "nie woźną"'),
    ("touching the Kalisz road at its end — not far, twenty-five pręty — heaped",
     "touching the Kalisz road at its end — not far from the new Łomowo clearings, on which the stumps still stand, twenty-five pręty — heaped",
     '699v', 'dropped: "nowin Łomowskich na których jeszcze pnie stoją"'),
    ("Jan Zalanowski", "Jan Zdanowski", '702', 'the scan has "Zdanowskim"'),
    ("show the further continuity and breadth of the Trąbczyn ground — taking it from",
     "show the further continuity and breadth of the Trąbczyn ground — and this continuity of the Trąbczyn ground, taking it from",
     '703v', 'dropped: "ta zaś ciągłość gruntu Trąpczyńskiego"'),
    ("resolving its suspension concerning the transgressions committed with the Honourable Chełmski expressed above",
     "resolving its suspension, made above, concerning the transgressions and the revenues arising from the ground now bounded off, and likewise concerning the claims and the delivery of possession, with the Honourable Chełmski",
     '708', 'dropped: "i pochodzących prowentów z gruntu odgraniczonego tudzież względem pretensji i tradycji"'),
    ("had settled his own people in that inn, the Honourable Chełmski cried out to beat, kill, and shoot [them]; and likewise ordered all the items in the inn",
     "had settled his own people in that inn, the Honourable Chełmski — proceeding in this against the law, and taking no step at law, but by force, in person, with several dozen men armed with firearms of various kinds, having ridden upon that inn — at once ordered shooting through the window into the inn; and a nobleman, the Honourable Krzeczkowski, was very nearly killed, and had his heel shot off; and moreover the inn was set on fire, and was barely saved after the flight of the men on the Honourable Chełmski's own side. During which attack the Honourable Chełmski himself cried out to beat, kill, and shoot; and likewise ordered all the items there in the inn",
     '709v', 'dropped: about sixty words, the court\'s finding on the armed raid on the inn'),
    ("shall sit in the tower of the Konin municipal court for twelve weeks from the time of the present decree, and shall continue that sitting for two weeks consecutively",
     "shall take his seat in the tower of the Konin municipal court twelve weeks from the time of the present decree, and shall continue that sitting for two weeks consecutively",
     '710', 'not a dropped phrase: the Polish, "zasiadł wieżą ... za niedziel dwanaście od czasu dekretu ... i toż siedzenie przez niedziel dwie kontynuował", '
             'sets the day he is to enter the tower (twelve weeks from the decree) and the length of the sitting (two weeks); the English read as a sitting of twelve weeks'),
    ("on Monday after Saint Bartholomew the Apostle, subsequently [obtained] on the late Honourable Antoni Prusimski",
     "on Monday after Saint Bartholomew the Apostle, in the field, [obtained] on the late Honourable Antoni Prusimski",
     '711v', 'the scan has "na polu", in the field; the transcription had "na potem"'),
]
