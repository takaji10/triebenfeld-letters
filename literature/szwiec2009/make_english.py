# -*- coding: utf-8 -*-
"""Szwiec (2009): english.md from original.md (Claude's English, 2026-10-20).

    python literature/szwiec2009/make_english.py

The English is written here paragraph by paragraph, keyed by the opening
words of the Polish (PARAS), and the photographs' captions by their parts
(CAPTION, PHOTO): the catalogue's captions are a short list of subjects with
the year and the photographer. The bibliography's entries stay as printed
(titles of works are not translated); its headings are. The page marks and the
note markers are carried over. The script stops on a Polish paragraph it has
no English for, so a change to original.md cannot slip through.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CAPTION = {
    'Budynek mieszkalny': 'Dwelling house',
    'Budynek mieszkalny - szczyt': 'Dwelling house – gable',
    'Budynek mieszkalny – szczyt': 'Dwelling house – gable',
    'Budynek mieszkalny – szczyt – konstrukcja szachulcowa': 'Dwelling house – gable – half-timbered construction',
    'Budynek mieszkalny - detal dachu': 'Dwelling house – roof detail',
    'Budynek gospodarczy': 'Farm building',
    'Detal dachu - strzecha': 'Roof detail – thatch',
    'Detal drzwi - budynek gospodarczy': 'Door detail – farm building',
    'Drzwi - budynek gospodarczy': 'Door – farm building',
    'Drzwi wejściowe - budynek mieszkalny': 'Front door – dwelling house',
    'Drzwi wewnętrzne - budynek mieszkalny': 'Inner door – dwelling house',
    'Ganek - budynek mieszkalny': 'Porch – dwelling house',
    'Kalenica - budynek gospodarczy': 'Roof ridge – farm building',
    'Mała architektura - piwniczka': 'Small structures – root cellar',
    'Mała architektura - studnia': 'Small structures – well',
    'Mała architektura - żuraw i studnia': 'Small structures – well sweep and well',
    'Mała architektura – żuraw i studnia': 'Small structures – well sweep and well',
    'Mała architektura – psia buda': 'Small structures – dog kennel',
    'Mała architektura – ubikacja': 'Small structures – privy',
    'Mała architektura- detal płotu': 'Small structures – fence detail',
    'Mała architektura- płot': 'Small structures – fence',
    'Mała architektura- prywatna kapliczka - budynek gospodarczy': 'Small structures – private wayside shrine – farm building',
    'Okap - budynek gospodarczy': 'Eaves – farm building',
    'Okno - budynek mieszkalny': 'Window – dwelling house',
    'Otwór okienny - budynek gospodarczy': 'Window opening – farm building',
    'Szczyt - budynek gospodarczy': 'Gable – farm building',
    'Wrota - budynek gospodarczy': 'Double doors – farm building',
    'Wrota i drzwi - budynek gospodarczy': 'Double doors and door – farm building',
}
# "16. Budynek mieszkalny - fot. 2009, fot. Wiesław Krzyżaniak." and the print's variants
PHOTO = re.compile(r'^(\d+)\. (.*?)\s*-?\s*fot\. (?:(\d{4}), (?:f )?fot\. )?(.*?)\.*$')

MAPS = {
    'Fragmenty mapy niemieckiej tzw. Masstischblatt w skali 1: 25 000. Arkusz nr ':
        'Parts of the German map called the Messtischblatt, scale 1:25,000. Sheet no. ',
    'Fragmenty polskiej mapy sztabowej pas ': 'Parts of the Polish general staff map, zone ',
    'Zdjęcie lotnicze (ortofotomapa) wsi ': 'Aerial photograph (orthophotomap) of the village of ',
}


def map_caption(t):
    m = re.match(r'(\d+)\. (.*)$', t)
    n, rest = m.group(1), m.group(2)
    for pl, en in MAPS.items():
        if rest.startswith(pl):
            rest = en + rest[len(pl):]
            break
    else:
        return None
    rest = (rest.replace(' z roku ', ' of ').replace(' słup ', ', column ')
                .replace(', Wojskowy Instytut Geograficzny, ', ', Military Geographical Institute, ')
                .replace(', skala 1:100000', ', scale 1:100,000')
                .replace(' – pochodzenie z portalu ', ' – from the portal '))
    return f'{n}. {rest}'


BIBLIO = {
    '6. Bibliografia': '6. Bibliography',
    'Monografie': 'Monographs',
    'Artykuły': 'Articles',
    'Słowniki, encyklopedie i zbiory danych statystycznych': 'Dictionaries, encyclopaedias and statistical collections',
    'Zdjęcia lotnicze': 'Aerial photographs',
    'Mapy': 'Maps',
}

PARAS = [
# the title page and the credits (front)
('KATALOG ARCHITEKTURY REGIONALNEJ DLA OBSZARU', 'CATALOGUE OF REGIONAL ARCHITECTURE FOR THE AREA OF'),
('„PUSZCZY PYZDRSKIEJ”', 'THE “PYZDRY FOREST”'),
('OPRACOWANIE BADAŃ NAUKOWYCH', 'A REPORT ON THE RESEARCH'),
('PRZEPROWADZONYCH JESIENIĄ 2009 ROKU', 'CARRIED OUT IN THE AUTUMN OF 2009'),
('Autor opracowania: dr Piotr Szwiec', 'Author of the report: Dr Piotr Szwiec'),
('Autorzy wykorzystanych materiałów - zespół badawczy:', 'Authors of the material used – the research team:'),
('Przemysław Kowalski (Stowarzyszenie MECENAT)', 'Przemysław Kowalski (the MECENAT Association)'),
('dr Anna Weronika Brzezińska (Instytut Etnologii i Antropologii Kulturowej,', 'Dr Anna Weronika Brzezińska (Institute of Ethnology and Cultural Anthropology,'),
('UAM Poznań),', 'Adam Mickiewicz University, Poznań),'),
('mgr Witold Przewoźny (Muzeum Etnograficzne MNP),', 'Witold Przewoźny, MA (Ethnographic Museum of the National Museum in Poznań),'),
('dr Piotr Szwiec (Pracownia Projektowania Detalu, ASP Poznań).', 'Dr Piotr Szwiec (Studio of Detail Design, Academy of Fine Arts, Poznań).'),
('mgr Patrycja Mikołajczak (Pracownia Projektowania Detalu, ASP Poznań', 'Patrycja Mikołajczak, MA (Studio of Detail Design, Academy of Fine Arts, Poznań),'),
('Paulina Baranowska (Instytut Etnologii i Antropologii Kulturowej, UAM', 'Paulina Baranowska (Institute of Ethnology and Cultural Anthropology, Adam Mickiewicz University'),
('Poznań),', 'Poznań),'),
('Bartosz Stańda (Instytut Etnologii i Antropologii Kulturowej, UAM Poz', 'Bartosz Stańda (Institute of Ethnology and Cultural Anthropology, Adam Mickiewicz University, Poznań),'),
('Pyzdry - Poznań 2009', 'Pyzdry – Poznań 2009'),
('Opracowanie materiału pozyskanego w czasie badań naukowych - autor:',
 'The material gathered during the research was written up by Dr Piotr Szwiec. All the photographs and other pictures in the report come from the material gathered in the research programme “THE PYZDRY FOREST: THE OLĘDERS AND THEIR IRON HOUSES”, organised by the MECENAT ASSOCIATION. The project was co-financed from funds of the MINISTRY OF LABOUR AND SOCIAL POLICY under the CIVIC INITIATIVES FUND OPERATIONAL PROGRAMME. The research team, authors of the photographs: Przemysław Kowalski (the MECENAT Association), Dr Anna Weronika Brzezińska (Institute of Ethnology and Cultural Anthropology, Adam Mickiewicz University, Poznań), Witold Przewoźny, MA (Ethnographic Museum of the National Museum in Poznań), Dr Piotr Szwiec (Studio of Detail Design, Academy of Fine Arts, Poznań), Patrycja Mikołajczak, MA (Studio of Detail Design, Academy of Fine Arts, Poznań), Paulina Baranowska (Institute of Ethnology and Cultural Anthropology, Adam Mickiewicz University, Poznań), Bartosz Stańda (Institute of Ethnology and Cultural Anthropology, Adam Mickiewicz University, Poznań). Design and layout: Dr Piotr Szwiec, Studio of Detail Design, Department of Architecture and Urban Planning, Faculty of Architecture and Design, Academy of Fine Arts in Poznań, Al. Marcinkowskiego 29, 60-967 Poznań, tel. 061 85525 21. Publication financed by a grant of the Ministry of Labour and Social Policy. Poznań 2009.'),
# 1. Introduction
('1. Wstęp', '1. Introduction'),
('Puszcza Pyzdrska to obszar o doskonale zachowanym', 'The Pyzdry Forest is an area with a superbly preserved Olęder heritage, notable for its large number of old farmsteads, often built of bog iron ore.'),
('Pozytywnym wyróżnikiem tego terenu', 'What sets this area apart for the better is a local style of architecture with many features in common.'),
('Puszcza Pyzdrska rozciąga się na terenie kilku gmin', 'The Pyzdry Forest stretches over several communes: Blizanów, Chocz, Gizałki, Grodziec, Mycielin, Pyzdry, Rychwał, Rzgów, Stawiszyn and Zagórów.'),
('Jest to niezwykle ciekawy teren pod względem kulturowym',
 'It is an exceptionally interesting area in cultural terms. On a relatively small area a distinctive cultural landscape grew up over the centuries, the result of the changes made by settlers who came not only from Polish lands but above all by Olęder settlers, who began to arrive here from the eighteenth century. The settlers, who came from various German lands and from Silesia, brought with them a cultural baggage which, in contact with the local substance and the conditions of the environment, led to the forming of a distinctive culture. For years the population of Olęder and of Polish descent lived side by side, and only the events that followed the Second World War brought great changes. The Olęders living in these lands were partly resettled, and in their place came settlers from various parts of Poland and people from the neighbouring regions. In time this mixture of population came to identify itself with the area. The new inhabitants of the Pyzdry Forest lived in the old Olęder houses, grew used to the conditions in which they had come to live, and slowly merged with the social fabric they had found.'),
('1.1. Cel badań i metodyka', '1.1. The aim of the research and its method'),
('W ostatnich latach, po przemianie ustrojowej', 'In recent years, since the change of political system and the end of direction from above, we see in many fields the stirring of local communities in search of their own identity.'),
('Projekt ten wpisuje się w ten nurt', 'This project belongs to that current. It aims to help the inhabitants of the region to judge the value of their own historical and cultural heritage, and the value of their architecture together with their native landscape, both natural and built.'),
('Przeprowadzono przez specjalistów', 'Specialists experienced in each field carried out interdisciplinary fieldwork. Ethnographic research (interviews based on a questionnaire) and research on the material heritage (an inventory of the monuments of folk culture: village architecture, churches, small peasant and religious structures, and cemeteries), extended by the reconstruction of local histories, tales and legends, proved exceptionally important in establishing the cultural identity of the inhabitants.'),
('W projektowanych badaniach terenowych, przeprowadzonych', 'In the planned fieldwork, carried out in the villages of the Pyzdry Forest, the present state of the inhabitants’ sense of cultural identity was in part recorded: who they feel themselves to be, how far'),
('identyfikują się z rejonem swego', 'they identify with the district where they have often lived for more than fifty years; and an attempt was made to find traces of the old Olęder settlers in the Pyzdry Forest.'),
('Architektura regionalna, w znaczeniu architektury', 'Regional architecture, in the sense of architecture with definite features, existed in the so-called “Pyzdry Forest” until the end of the 1940s. Later central planning and the promotion of “ready-made designs” of houses and farms imposed from above destroyed for many years the achievement of past generations of the region’s inhabitants. These designs were meant for the whole country, and any regional adaptation touched only their parts, not the whole of the scheme.'),
('Część istniejącej jeszcze dzisiaj architektury', 'Part of the architecture with regional features that still exists today is losing its original function with the economic, social and political changes, and is undergoing an inevitable process of decay, rebuilding or even complete removal.'),
('Detale ulegają przeróbkom', 'Details are altered under the influence of fashions and various tendencies. The composition of the settlements is being destroyed by infill building – the filling of gaps with forms often culturally alien, or with buildings of a purely productive and technical character, rooted in no architectural tradition. There is a fear that through this process the groups of settlement preserved until now will within a few decades be made uniform and lose their regional features.'),
('Powszechna globalizacja przejawia się', 'Universal globalisation shows itself in a free flow of disordered information – in other words, in a chaos of information – which touches this field too. Numerous publications and periodicals on architecture, small structures, and landscape architecture, often reduced to garden architecture, give their readers fragmentary knowledge and pass over the complex relations of architecture and landscape. They often present questions without their regional context, and they set patterns that many builders imitate.'),
('W tej sytuacji konieczne jest zarówno stworzenie', 'In this situation it is necessary both to create a catalogue of architectural forms describing the relations in the existing landscape and to take broader action, such as the administrative protection of the existing regional architecture and spatial planning that is conscious of, and follows, the principles by which that architecture was made. Urban-planning studies that take account of regional distinctness will allow the whole region to develop harmoniously and in proportion.'),
('Należy zebrać i zachować wiedzę o cechach tradycyjnej architektury, jej relacji z krajobrazem i wzajemnego', 'The knowledge of the features of traditional architecture, of its relation to the landscape and of their mutual influence, must be gathered and preserved. In the long term this may help to create a “style, that is, a so-called school of regional architecture.” A contemporary architecture must arise, suited to the present needs of the inhabitants but growing out of the native building tradition.'),
('Celem badań było poszukiwanie stylu', 'The aim of the research was to look for a regional style, and to show the relations of the landscape and their influence on the local architecture and on the rise of a regional style.'),
('W poszukiwaniu tego stylu zostały przebadane', 'In search of this style, architectural and landscape features representing every phase of the development of architectural forms in the area studied were examined. Both existing buildings and those already rebuilt or wholly destroyed were analysed.'),
('1.2. Zebranie materiałów źródłowych', '1.2. Gathering the source material, and the fieldwork'),
('Badania obiektów przebudowanych i nieistniejących', 'The study of rebuilt and vanished buildings was possible thanks to conservation records, archival material and other sources. For these buildings an inspection on the spot was also needed in every case.'),
('Materiał wyjściowy do opracowania stanowiły', 'The starting material for the report was maps, photographs of architecture, aerial photographs, sketches from nature and surveys (plans and elevations), as well as archival material and local and specialist publications of various kinds (on architecture, urban planning, ethnography and the conservation of monuments). This material was obtained in the course of the research. An analytical method was adopted. The research was carried out directly in the field, in archives and by interviews. Detailed photographic and drawn records and surveys were made. On the basis of the source, cultural and historical data gathered, a catalogue was made of valuable existing buildings with regional features. These buildings were located in the field and analysed, and the conclusions were put into graphic form. Comparative studies were made of the architectural and landscape elements typical of the “Pyzdry Forest”. The catalogue contains general and detailed maps marking where the buildings studied stand, sets of photographs, freehand sketches, drawn analyses and surveys of individual buildings. Maps, archival photographs and written archival sources were analysed and set against reality and against the photographs, drawings and surveys made by the research team.'),
('1.3. Określenie obszaru', '1.3. The area of the research'),
('Teren poddany badaniom to gminy', 'The area studied is the communes of Blizanów, Chocz, Gizałki, Grodziec, Mycielin, Pyzdry, Rychwał, Rzgów, Stawiszyn and Zagórów, which lie in the “Pyzdry Forest”.'),
('Jest to obszar o wspólnym krajobrazie', 'It is an area with a common cultural landscape, which coincides with the so-called “Pyzdry Forest”.'),
('Obszar badań obejmował cały teren', 'The research covered the whole area of the so-called “Pyzdry Forest”. The buildings in the following places, with the land around them, were studied in detail in the field and compared with topographical maps (military staff maps at the scales 1:100,000, 1:50,000 and 1:25,000, and topographical maps at 1:100,000, 1:50,000, 1:25,000 and 1:10,000), modern and archival, with the orthophotomap, and with aerial and satellite photographs: Czarny Bród, Dolne Grądy,'),
('Jarantów, Jarantów Kolonia', 'Jarantów, Jarantów Kolonia, Józefów, Kolonia Obory, Królewiny, Lipe, Nowa Kaźmierka, Nowolipsk, Nowy Olesiec, Orlina, Ruda Komorska, Ruda Wieczyńska, Stara Kaźmierka, Trąbczyn, Walga, Wierzchy, Wrąbczynek, Wrąbczynkowskie Holendry, Wronów, Zapowiednia.'),
('Poszczególne miejscowości zostały przebadane', 'Each place was first studied in the field in general terms. At this stage buildings were chosen for detailed study, which was then carried out.'),
('Przeprowadzając badania poszczególnych wsi', 'In studying each village the following questions were taken into account: the village’s position in relation to the neighbouring towns, the plan of the settlement, its internal network of tracks and its relation to the road network, the original division of the plots, the layout of the buildings on the homestead, the existing greenery, that is, trees, crops, farmyard planting, orchards and gardens, and woods among the fields, and the natural and altered network of waters.'),
('Badania naukowe nad tkanką architektoniczną', 'The research on the architectural fabric of town and village covered the spatial structure of the region, which is made up of its urban and architectural composition and of spatial relations and their mutual influence, in the context of the semantics of space in the broad sense.'),
('1.4. Oczekiwane rezultaty.', '1.4. The results expected.'),
('Realizowany projekt ma na celu zebrać', 'The project aims to gather and preserve knowledge of the regional features of the existing architecture, of its relation to the landscape and of their mutual influence.'),
('Celem naukowym projektu jest przeprowadzenie', 'The scientific aim of the project is to carry out research on the architectural fabric of town and village, covering urban and architectural composition, spatial relations and their mutual influence, in the context of the semantics of space in the broad sense. The most important result of the research is to be the “discovery” of the regional features of the existing architecture by describing, comparing and evaluating it, and by making'),
('przykładowych propozycji projektowych', 'sample design proposals. The aim is to create guidelines that may become suggestions for those who make regional architecture. It matters that the work should show regional architecture in a broad visual and scientific (physiographic and historical) context.'),
('Publikacja projektu pozwoli', 'Publishing the project will let the report reach a suitably wide circle of people, some of whom have, in varying degrees, an influence on the relation between building and landscape. It may change attitudes to their own heritage, lead them to appreciate the qualities of the region’s architecture and its particular character, and to see the physiographic relations in areas transformed by settlement.'),
('W dłuższym okresie może to pomóc', 'In the longer term it may help to save the valuable architectural fabric that exists, understood not only as houses and buildings but also as the relations of the landscape. The research carried out made it possible to document the technique of building “houses of iron”, that is, of bog iron ore, found in this region.'),
('dokumentowanie występującej', None),     # joined to the paragraph before in earlier readings
('Biorąc pod uwagę postępującą destrukcję', 'Given the progressive decay and disappearance of regional elements in architecture and landscape, it may be supposed that any further delay in carrying out wide-ranging research in this area may affect the survival of many culturally valuable elements of regional architecture.'),
('Już dzisiaj są możliwe działania ratunkowe', 'Rescue work on existing historic buildings is possible even today. The LEADER+ programme[^1] allows to a large extent the co-financing of the repair of roofs and elevations made in traditional technologies that are now dying out, such as roofing with straw or reed, or outer walls – elevations made of bog iron ore. With funds obtained in this way a building can also be modernised by replacing its damaged window and door joinery with new joinery of the traditional proportions and divisions.'),
('Wnioski z badań interdyscyplinarnych', 'The conclusions of the interdisciplinary research are necessary for a full understanding of the relations of the landscape and are needed for the design of new undertakings. The project is addressed both to conservators, planners and architects and to the local community. It is needed because it will also allow the regional features of the man-made landscape of this district to be given their due place in the national heritage.'),
('[^1]: LEADER+ to aktualna inicjatywa', '[^1]: LEADER+ is a current Community initiative, that is, a programme of non-repayable aid from the European Union to specified bodies. Local authorities, non-governmental organisations and businesses receive aid for the projects of regional development they submit in the member states.\n[…] LEADER+, on the basis of co-operation at regional and transnational level, supports the introduction of modern strategies for the development of rural areas.\nThe programme is financed by the Guidance Section of the European Agricultural Guidance and Guarantee Fund. […] Funds from the LEADER+ programme may be used for three aims:\nsupport for modern strategies for the development of rural areas\nsupport for interregional and international projects of co-operation\nthe building of a network of the EU’s rural areas – both those receiving LEADER+ aid and those not receiving it. In general all the rural areas of the European Union may use the LEADER+ initiative. Aid under aims A and B, however, is meant for a limited number of areas. The beneficiaries of the aid are above all “Local Action Groups”, that is, partnerships of public and private partners undertaking together innovative actions connected with the development of a rural area.\nhttp://www.funduszestrukturalne.gov.pl/LEADER/'),
('1.5. Sposób realizacji projektu', '1.5. How the project was carried out'),
('Projekt „PUSZCZA PYZDRSKA – Olędrzy', 'The project “THE PYZDRY FOREST – The Olęders and their Iron Houses” is addressed to the inhabitants of the communes of Blizanów, Chocz, Gizałki, Grodziec, Mycielin, Pyzdry, Rychwał, Rzgów, Stawiszyn and Zagórów, which lie in the “Pyzdry Forest”.'),
('Opracowanie będące wynikiem badań', 'Once published, the report that results from the research may let many inhabitants see the regional features in the existing architecture, and help to keep its character unchanged.'),
('Przygotowany projekt prezentuje', 'The project as prepared presents regional architecture. It rests on the research carried out in the area of the “Pyzdry Forest”. Source, cultural and historical data were gathered. The research was done in the field: detailed photographic and drawn records and surveys of many buildings were made. The buildings studied were placed in space, and the existing spatial relations were analysed.'),
('Każdy z regionów Wielkopolski', 'Each of the regions of Greater Poland has its own cultural and historical identity, which arises from the sum of the traditions and experiences of its inhabitants and of their cultural and material achievement. Becoming aware of these differences will let the inhabitants of the region keep their own identity in an age of universal globalisation and uniformity.'),
('Regiony te stosunkowo łatwo wydzielić', 'These regions are relatively easy to mark off in those parts of Greater Poland whose boundaries are set apart by geography.'),
('Cały obszar osadniczy jest ograniczony', 'The whole area of settlement is bounded and divided by forests and natural barriers of the landscape. These are, for example, regulated watercourses that were once natural (though today they are hard to tell apart in the field from the dense network of drainage canals made when the forest lands were brought into use). The natural barrier formed by compact tracts of forest is for the most part a remnant of the original forest (understood as places where woods grow, for the woods, and above all the peasants’ woods, were and are intensively used).'),
('Osadnictwo w Puszczy Pyzdrskiej w okresie staropolskim', 'Settlement in the Pyzdry Forest in the Old Polish period went with the industrial use of its riches and the bringing of the land taken up under the plough, advancing into it in the wake of the clearing of the woods as far as the soils and communications allowed. Land of middling fertility was taken up, mostly sandy loam, well enough watered and easy to till. On its edge arose settlements tied to the use of the forest (Wrąbczyn), service villages (Obory), ore-mining and glassworks settlements – Ruda Komorska, Ruda Wieczyńska, Huta Trąbczyńska, Huta Łukomska – and tar-works (Smoliniec).'),
('W czasach nowożytnych rozwój osadnictwa', 'In modern times settlement in the Pyzdry Forest grew almost twice as fast as in the Middle Ages. For 188 settlements arose here, at least 117 of them in the sixteenth and seventeenth centuries, though some older ones were deserted, and 71 in the eighteenth century (more precisely, in the years 1701-1793), among which Olęder settlements clearly prevailed (67.6 per cent).'),
('Zbigniew Chodyła fragment', 'Zbigniew Chodyła, extract from “Settlement in the Pyzdry Forest, from the Middle Ages to the beginning of the twenty-first century”.'),
# 2.1 Dwelling houses
('2.1. Budynki mieszkalne we wsiach', '2.1. Dwelling houses in the villages of the “Pyzdry Forest”'),
('Architektura budynków mieszkalnych wsi olęderskich', 'The architecture of the dwelling houses of the Olęder villages has features in common. They can be found at every stage of its development, and they occur, more or less strongly, over the whole area of settlement in the “Pyzdry Forest”. The dwelling houses have different proportions according to the period in which they were built. The older cottages, however they are set, are of timber construction, log walls with posts, the corners joined with dovetails, with posts into which the beams of the longer walls and those beside the door openings are fixed. Post-and-plank construction is also found, and in villages near deposits of clay, timber framing filled with clay-wrapped staves, or rammed clay. There are also mixed forms, with a clear preference for the “better” and “worse” constructions: timber was held better than clay, and log walls better than post-and-plank or timber framing.'),
('Interesujący jest inny materiał', 'Another material used in this region for building walls is of interest, namely bog iron ore. Building with ore is indeed found in other regions of the country, but nowhere does it occur in such quantity, and nowhere have so many buildings made of it survived.'),
('Najstarsze zachowane chałupy mieszkalne', 'The oldest surviving cottages in this region are usually small single-pile, single-storey buildings with a separate entrance hall and a black kitchen on the axis of the broad front. In the less common one-and-a-half-pile and double-pile cottages (usually the larger buildings) there appears a purlin beam, a kind of wooden girder carrying ceiling beams that are too long. Occasionally its end can be seen in the gable (set off-centre along the wall, at distances of 1:2)[^2].'),
('Szczyty (najczęściej deskowane', 'The gables (mostly boarded, clad with vertical boards) are mostly set flush with the wall of the ground floor. In that case an eaves board is nailed to the ends of the wall-plate beams that stand out beyond the face of the wall (mostly cut off at an angle of 45⁰). This board is set horizontally, sloping at an angle of 45⁰, at the height of the top edge of the gable wall, and further supported by brackets, sometimes decoratively cut, in varying numbers.'),
('Spotyka się też szczyty wysunięte', 'Gables projecting beyond the face of the gable wall by the width of the outermost ceiling beam are also found. This was done by pushing the last truss outwards and resting it on the projecting end of the wall plate or the purlin (the beam carrying the ceiling beams).'),
('Nowsze domy są już wszystkie murowane', 'The newer houses are all of brick; those of the mid-nineteenth century keep the proportions and look of the earlier timber buildings, also have boarded gables, often with extra doors into the loft, and have no ornament on their elevations.'),
('W przypadku niektórych trudno dociec', 'In some of them it is hard to tell what the construction of their walls really is and what lies under the plaster. The roofs of these buildings have boarded gables'),
('[^2]: W odróżnieniu od architektury', '[^2]: Unlike the architecture of the Pyzdry Forest, such a construction and a gable set out beyond the gable wall are very often found in the Olęder cottages around Nowy Tomyśl.'),
('Całość tego budownictwa posiada', 'All this building has the features typical of the architecture of the Olęder village of the “Pyzdry Forest”.'),
('2.1.1. Budynki mieszkalne o konstrukcji drewnianej', '2.1.1. Dwelling houses of timber construction'),
('2.1.2. Budynki mieszkalne o konstrukcji szachulcowej', '2.1.2. Dwelling houses of half-timbered construction'),
('2.1.3. Budynki mieszkalne o ścianach z gliny', '2.1.3. Dwelling houses with walls of clay'),
('2.1.4. Budynki mieszkalne o ścianach z rudy darniowej', '2.1.4. Dwelling houses with walls of bog iron ore (of iron)'),
('2.1.5. Budynki mieszkalne o konstrukcji mieszanej', '2.1.5. Dwelling houses of mixed construction'),
('2.1.6. Budynki mieszkalne o ścianach murowanych z cegły', '2.1.6. Dwelling houses with walls of brick'),
('2.1.7. Dachy w budynkach mieszkalnych', '2.1.7. The roofs of dwelling houses'),
('Dachy są zawsze dwuspadowe', 'The roofs are always pitched, with two symmetrical slopes. Most are constructions at an angle of 40⁰ to 45⁰ set on a broad-fronted building, typical of this region. Buildings with roofs thatched with straw or reed are still found; most buildings now have roofs covered with asbestos-cement sheets (eternit), sometimes with tiles or sheet metal. The rafters mostly rest on ceiling beams projecting beyond the face of the wall, more rarely on a purlin laid on the axis of the wall on the ceiling beams, set off from those ceiling beams.'),
('Najczęściej stosowaną konstrukcją', 'The construction most often used (bound up with the single-pile plan) is the collar-beam roof. On one-and-a-half-pile and double-pile buildings the construction of the roof trusses is more complicated – mostly a rafter roof on posts (stolcowa).[^3]'),
('Dachy są ustawione symetrycznie', 'The roofs are set symmetrically on the building. Their gables are mostly boarded and sometimes have extra doors into the loft.'),
('Dachy wszystkich typów budynków', 'The roofs of all types of building, both dwelling houses and farm buildings, had no dormer gables.'),
('[^3]: Taką konstrukcję posiadają', '[^3]: The buildings studied that have such a construction are two: one in Dolne Grądy, the other in Wrąbczynkowskie Holędry. Inventory cards 007 and 021.'),
('2.1.8. Okna i drzwi w budynkach mieszkalnych', '2.1.8. Windows and doors in dwelling houses'),
('W budynkach mieszkalnych zastosowano otwory okienne', 'The dwelling houses have rectangular window openings, always set vertically, a “standing” rectangle. The proportions of the windows vary, mostly close to a gentle rectangle (3:4 or 4:5). The windows have composite divisions and are divided by glazing bars into smaller panes. The simplest are single-casement windows (square or a gentle rectangle) divided into four equal panes by bars in the casement. There are also double-casement windows in which each casement is divided into smaller equal panes, two to four of them, or two panes in the proportion 2:3, the smaller pane always at the top. Another, more varied type is the double-casement, side-hung window in four parts, in which the fixed transom is mostly set at a height of 2:3. There are a few exceptions to these rules, for example windows with proportions close to 1:2 upright.'),
('Najczęściej stosowano okna skrzynkowe', 'Box windows were used most often. The window joinery was made very simple.'),
('Zachowane drzwi wejściowe wykonane są', 'The surviving front doors are of ledged and of frame-and-panel construction, from the simplest, unornamented, in older buildings, to doors more or less ornamented in farms that were once richer, made from the end of the nineteenth century. These last have carved decoration, more elaborate and eclectic, in various forms. The commonest are double doors of many panels with a fanlight, each leaf divided into three or four equal vertical panels, in proportions close to 3:5, and the doors themselves 3:4, or 4 to 4.5 : 6.5 to 7. Newer doors, from the beginning of the twentieth century, are also double and have the proportions 1:2 with a fanlight over the door, the doors themselves 2:3 and ¼, divided into two unequal panels of which the higher is the larger. There are also double doors without a fanlight in the same proportions (2:3 and ¼), and single doors in the same proportions with panes of glass in the upper part of the leaf, the glass divided, for example, into three panes. The division of the whole door is in proportion (glass 1 : 2.5 wooden panels).'),
('2.1.9. Ganki w budynkach mieszkalnych', '2.1.9. Porches of dwelling houses'),
# 2.2 Farm buildings
('2.2. Budynki gospodarcze we wsiach', '2.2. Farm buildings in the villages of the “Pyzdry Forest”'),
('Budynki gospodarcze mieściły pomieszczenia', 'The farm buildings held the rooms for livestock and those that served them, for example fodder rooms or a cart shed. In timber buildings, which prevailed, log construction was used, log construction with posts (in the larger, longer buildings), and post-and-plank. Where clay is plentiful, rammed clay is found, and here and there timber framing filled with clay-wrapped staves. Many farm buildings, like the dwelling houses, were built of bog iron ore.'),
('Ostateczną formą jest budynek', 'The last form is the building wholly of brick, and mostly of red brick, unplastered.'),
('Budynki mają ściany parteru murowane', 'The buildings have ground-floor walls built of red fired brick.'),
('2.2.1. Dachy w budynkach gospodarczych', '2.2.1. The roofs of farm buildings'),
('Budynki gospodarcze parterowe posiadają', 'The single-storey farm buildings have only pitched roofs with two symmetrical slopes, of collar-beam construction, more rarely on posts. The rafters were fixed with tenons and mostly rest on the ceiling beams, which means that there are as many rafters as beams. The outermost trusses are mostly set flush with the gable wall. In buildings of timber with boarded gables, the ends of the wall-plate beams and the wall beneath them were sometimes covered by a horizontal board set at a slant.'),
('W budynkach o ścianach z drewna i z gliny', 'Buildings with walls of timber and of clay were roofed with straw or reed, brick ones with tiles of various kinds.'),
('2.2.2. Okna i drzwi w budynkach gospodarczych', '2.2.2. Windows and doors in farm buildings'),
('Z uwagi na funkcje obiektu otwory okienne', 'Because of the building’s use, the window openings in the parts for livestock were made small, and in rooms (where more light was needed) such as workshops or fodder rooms, much larger. At first, in timber buildings, these openings were open or closed only by a wooden shutter. In brick buildings small windows were used, mostly of steel or cast iron, of many panes, with one pane that tilted open, in proportions close to 2:3, straight-headed or with a segmental arch.'),
('Interesujące jest zastosowanie w budynkach', 'Of interest is the use, in buildings of bog iron ore, of window openings with a frame nailed together from boards in the shape of an equilateral triangle.'),
('Drzwi do budynków gospodarczych wykonywano', 'The doors of farm buildings were made of simple ledged construction, in various proportions according to the kind of room they closed. The larger openings, through which carts passed, were made in proportions close to a square; the smaller, for people only, mostly in the proportions 1:1¾ or 1:2. The door opening was straight or finished at the top with a segmental arch, and the leaves of the door had the same shape. They were made of plain boards set vertically and hung on strap hinges of steel, which sometimes had ornamental ends.'),
# 2.3, 2.4, 2.5
('2.3. Detal architektoniczny', '2.3. Architectural detail in the buildings of the “Pyzdry Forest”'),
('Detal stosowany w budynkach mieszkalnych', 'The detail of the older dwelling houses and farm buildings, especially those of timber, is very modest and kept to the necessary minimum. Often the only ornament is the patterns on the front doors and the decorative profiles of the ceiling beams in the rooms (mostly in the main room) and of their ends projecting outside the building. Older buildings also had shutters, at first ledged and later panelled.'),
('2.4. Mała architektura i ogrodzenia', '2.4. Small structures and fences in the villages of the “Pyzdry Forest”'),
('W istniejących obecnie ogrodzeniach drewnianych', 'Few original parts survive in the wooden fences that exist today. The reason is that the material does not last. The fences standing now were mostly made after 1945, and so for the most part have nothing to do with the traditional buildings.'),
('Pierwotnie siedlisko w tym regionie', 'Originally the homestead in this region (mostly Olęder) had, besides a paling fence, few small structures, such as wells and a few bread ovens (these stood inside the cottages).'),
('Studnie w starszej wersji posiadały', 'In the older form the wells had wooden sweeps, in the newer often drum windlasses. A few sweeps still survive, especially in the villages deep in the “Pyzdry Forest”.'),
('Piece chlebowe (udało się udokumentować', 'Bread ovens (only one oven could be recorded in the field) were set at a good distance from the buildings, mostly in the orchard outside the house. It may be supposed that they were found on the farms where new dwelling houses were built, or where the bread ovens inside were done away with when existing buildings were rebuilt. These ovens stood originally in the black kitchen, in the stack of the chimney, and many examples of such ovens, now no longer used, survive.'),
('2.5. Układy przestrzenne', '2.5. Spatial layouts – the plan of the villages.'),
('Ponieważ większość wsi powstała', 'Because most of the villages arose as marsh row villages passing into scattered settlement, the layout of the farmsteads and their distribution over the land is quite different from that of the older, compact villages on the edges of and outside the Pyzdry Forest (mainly street villages and manor-farm villages).'),
('Cały teren osadniczy został pokryty', 'The whole area of settlement was covered by a dense mesh of farms, and the distances between them follow from the size of the average settler’s plot, 18 to 20 ha, close in shape to a very elongated rectangle.'),
('Role w tego typu gospodarstwach', 'The arable of such farms was made up of long strips of fields running at right angles to a watercourse or wet ground. The strip ran from the wet field to the dry. All the strips were crossed by a road at right angles to them, which joined the farms. The buildings of each settler were put up near this road; they often lie in rows of several on the same side of it. This way of dividing the land was reasonably fair and in a way evened out the chances of success in farming. As a rule the farms were not, and still are not, joined to one another by roads, for each has roads at right angles to the main road, running the whole length of its land on both sides of the main road.'),
('Nie jest to jednak typowa ulicówka bagienna', 'It is not, however, a typical marsh street village, for some of the farms, because the land was originally wet, were placed on the highest part of the plot, often at some distance from the road, so that they are in a sense scattered.'),
('O specyfice regionu decydują też', 'The character of the region is also shaped by the woods among the fields: deciduous trees and shrubs grow along the drainage ditches, the edges of the roads and the balks.'),
('Poszczególne wsie zlewają się', 'The villages merge into one great village, in which the farm’s position in relation to the main road decides which village it belongs to.'),
('Każda z wsi olęderskich posiadała', 'Each Olęder village had its own cemetery near it, mostly on a hillock or a glacial dune. In some cases these dunes were levelled and shaped. In scattered villages, where there was ground high enough, it was placed near the centre of the village or an important crossroads. In compact villages the cemetery always lies outside the buildings. Mostly there are deciduous trees several hundred years old in it, often oaks, which may remember the time when the cemetery was founded.'),
# 5. Summary
('5. Podsumowanie', '5. Summary'),
('Procesy przekształcania rodzimego krajobrazu', 'The transformation of the native landscape goes on constantly and inevitably, and in recent years we have seen it grow stronger. The rebuilding and modernisation of the village threatens to lose its valuable individual character for the sake of particular universal values, general and often alien, not only in our landscape but even beside other newly built architecture.'),
('Należy zebrać i zachować wiedzę o cechach tradycyjnej architektury, jej relacji z krajobrazem i wzajemnym', 'The knowledge of the features of traditional architecture, of its relation to the landscape and of their mutual influence, must be gathered and preserved. In the long term this may help to create a “style”, that is, a so-called “school of regional architecture.” A contemporary architecture must arise, suited to the present needs of the inhabitants but growing out of the native building tradition.'),
('Na omawianych terenach współzależność', 'In the areas discussed the interdependence of the buildings and the natural environment is plain. The pattern of settlement is closely bound up with the historically formed ways of farming the land: in the classic pattern, manor house – manor farm – farmhands’ cottages – fields, and in the modern one of the Olęder villages and of those founded in the nineteenth century, houses in farmsteads – fields – woods among the fields.'),
('Należy sobie uświadomić, że to od mieszkańców', 'It must be understood that it depends on the inhabitants of the region, who are the builders and the owners of old and new houses, what our surroundings will look like. A very great deal will depend on their decisions about architecture, about the detail of the composition of the landscape, and even about the decoration of buildings.'),
('Nie powinno to jednak prowadzić', 'This should not, however, lead to a kind of artificial open-air-museum treatment of the native architecture: a creative approach to design is needed, one that takes account of regional features, native materials and the proportions of regional buildings.'),
('I to od mieszkańców regionu będzie zależało', 'And what future generations inherit will depend on the inhabitants of the region!'),
]


def english_of(t, page):
    if t in BIBLIO:
        return BIBLIO[t]
    if page >= 96:
        return t                      # a bibliographical entry, as printed
    m = PHOTO.match(t)
    if m and m.group(2) in CAPTION:
        n, subj, year, who = m.groups()
        return f'{n}. {CAPTION[subj]} – ' + (f'photograph {year}, by {who}.' if year else f'photograph by {who}.')
    c = map_caption(t) if re.match(r'\d+\. (Fragmenty|Zdjęcie)', t) else None
    if c:
        return c
    hits = [en for pl, en in PARAS if t.startswith(pl)]
    if not hits:
        sys.exit(f'p. {page}: no English for: {t[:80]}')
    return max(((pl, en) for pl, en in PARAS if t.startswith(pl)), key=lambda x: len(x[0]))[1]


def main():
    src = io.open(os.path.join(HERE, 'original.md'), encoding='utf-8').read()
    out, page = [], 0
    for block in src.split('\n\n'):
        m = re.match(r'^\[p\. (\d+)\]$', block.strip())
        if m:
            page = int(m.group(1))
            out.append(block.strip())
            continue
        if not block.strip():
            continue
        en = english_of(block.strip(), page)
        if en is not None:
            out.append(en)
    io.open(os.path.join(HERE, 'english.md'), 'w', encoding='utf-8', newline='\n').write('\n\n'.join(out) + '\n')
    print('wrote english.md')


if __name__ == '__main__':
    main()
