# -*- coding: utf-8 -*-
"""The spot sheet for APP 53/20/0/-/Poznań Gr.1181.

The readings that grammar, the register's own formulas and the sibling units
could not settle, with a picture of the line for each. Built into a
self-contained static page (mobile first) that is published at a public
address so the editor can answer it away from this machine; answers come back
pasted into the chat and are recorded here.

Sections: DATES - the entry's own dating; NAMES - persons, estates, courts;
SUMS - the figures and money formulas; WORDS - readings with two plausible
candidates; PROPOSALS - readings changed or suggested in session that the
editor can confirm or reverse; PRINCIPLES - the rule behind the case
completions, with sample rows.
"""

# (id, section, page, y_hint or None, question, [options], note)
# y_hint: an approximate y of the target line on the page image, when known;
# otherwise the generator estimates it from the passage's position in the
# page's text. anchor: words of the transcription around the target, used to
# place the row and printed under the crop.

ROWS = [
    # ------------------------------------------------------------- DATES ---
    # Settled by the editor's fresh line-by-line pass of p. 161 (2026-10-26):
    # the December year is 1783; the decree day reads "videlicet 8ua Mensis
    # 8bris" (the scribe's 8 stands against the computed 7 - recorded in the
    # notes); "Mens(is)" Junii; "oblatam"; "camera-/riali". The rows for those
    # readings are gone; the remaining date questions:
    ('heading_year', 'Dates', '0161_a', 130,
     'The register heading "4ta Martii" - does a year follow it on the page?',
     ['no year', '1785', '1786', 'other year (write it)'],
     'The entry records an actum of 29 March 1784 (the weekday formula fits '
     '1784 exactly, and its own narrative says "anno immediate elapso 1783" '
     'for the December terminus - the year 1783 now read on the page). If '
     'the heading carries a year, it says when the relation was registered.'),
    # tail_167v: settled from the chat, 2026-10-26, and taken off the sheet.
    # The editor ruled "there is no content past 167v" - the register ends
    # there; the entry stops mid-sentence because the volume ends, and no
    # next leaf exists to ask for. (The row asked whether the entry continues
    # on the next leaf; the ruling answers it.)
    # ------------------------------------------------------------- NAMES ---
    ('termilis', 'Names', '0163_a', 2050,
     'The estate name before "Kanino" - read it ("Termilis"? "Ternilis"?)',
     ['Ternilis', 'Termilis', 'other (write it)'],
     'It stands again on 163v ("Bona Ternilis[?] Kanino Swiątniki et '
     'Jaryszki"), disposed of in other hands before 1729. Read the letters.'),
    ('odechowski', 'Names', '0163_b', 2280,
     'The husband of Victoria in "3tio voto ... Odechowski" - read the word',
     ['Caroli', 'Michaeli', 'other (write it)'],
     'On 164v the same couple stands as "Magnificorum Caroli et Victoriae '
     'itidem de Prusimskie Odechowskich conjugum". If the word here is '
     '"Michaeli", the two passages disagree and the genealogy follows the '
     'better attested one.'),
    ('zabriski', 'Names', '0163_b', 2350,
     'The name after "Magnifici Casimiri" - Mariana\'s second husband',
     ['Zabriski', 'Zawadzki', 'other (write it)'],
     '"subalterno connubio Magnifici Casimiri Zabriski[?] Judicio Terrestris '
     'Brestensis" - the surname to read.'),
    ('strzalko', 'Names', '0163_b', 980,
     'The name after "a succ~oribus" - who held Szetlewek before Golinski?',
     ['Strzałkowski', 'Strzałkow + other word', 'other (write it)'],
     '"a succ~oribus Strzałko[?]iamis[?]" - the two words after '
     '"successoribus" both stand open.'),
    ('rzekicka', 'Names', '0166_a', 1300,
     'The widow\'s name and her husband\'s - "Generosae Rzek[?]icka olim '
     'Generosi Jacobi Rzechicki[?]"',
     ['Rzekucka / Rzechicki', 'Raczycka / Raczycki', 'other (write it)'],
     'A Raczycki family stands in the entry already (a load of 7,000 fl.); '
     'if these are they, the index joins them.'),
    ('obiesierski', 'Names', '0166_a', 1750,
     'The husband of Apollonia - "Generosi Sigismundi Obiesierski[?]"',
     ['Obiesierski', 'Oborski', 'other (write it)'],
     'The surname to read.'),
    ('obierunskie', 'Names', '0166_a', 2450,
     'The family name - "a Generosis Obierun[?]skie" (it stands twice)',
     ['Obierzunski', 'Obierunski', 'other (write it)'],
     'The family that released the 6,000 fl. to the Trąmpczyńskis in 1727.'),
    ('keszycki', 'Names', '0164_b', 420,
     'The name after "successoribus" - "Kęszy[?]ciami[?]"',
     ['Kęszyckiami', 'Kęszygórami', 'other (write it)'],
     'The successors holding the 30,000 fl. charge on Pawłowo / Zernik.'),
    ('schedas_word', 'Names', '0164_a', 1700,
     'The word before "schaedas trinas" - read it',
     ['[nothing - just schedas]', 'tres', 'other (write it)'],
     '"Fratram natu majorem [?]sc[h/t?]aedas trinas ... porrexisse" - what '
     'stands before "schaedas"?'),
    ('ittis', 'Names', '0164_a', 2500,
     'The word after "Se~ Rae~" - the office of Paul Prusimski',
     ['Succamararii', 'Subthesaurarii', 'other (write it)'],
     '"Se~ Rae~ [?]ittis Fratrum intermedium" - on 162 the same man is '
     '"Succamarariis" (podskarbi). Read what stands here.'),
    ('costensem', 'Names', '0165_a', 2820,
     'The court of the Oporowo condescensio - "actis Castrensis Costensem[?]"',
     ['Costinens[ibus?]', 'Gostinens[ibus?]', 'other (write it)'],
     'Oporowo lay in the Poznań palatinate; read the court\'s name.'),
    ('skoli', 'Names', '0167_b', 300,
     'The estate name - "in Fundo Bonorum Skoli[s?]"',
     ['Skoki', 'Skoli[n]i', 'other (write it)'],
     'The grounds where the condescensio termini were held before the '
     'decree of Gniezno remitted the cause. Read the name.'),
    ('flottowa', 'Names', '0167_b', 800,
     'The name after "Magnificam" - "[Fl/H?]ottowa"',
     ['Flottowa', 'Hottowa', 'other (write it)'],
     'She stands beside the Radoliński successors disputing the letter of '
     '1736. Read the name.'),
    ('mokronos', 'Names', '0167_b', 850,
     'The village of Peter Florkiewicz - "de Villa Mokronos[??]"',
     ['Mokronosi', 'Mokronosy', 'other (write it)'],
     'Read the ending of the village name.'),
    ('lubraniecki', 'Names', '0167_b', 2350,
     'The name of the Kalisz chamber judge - "Magnificis Lu[s?]br[?]co '
     'Bogdanski"',
     ['Lubraniecki Bogdański', 'Lubomirski Bogdański', 'other (write it)'],
     'He took part with Theresia née Rozdrażewska in the act of 3 June 1782. '
     'Read both name words.'),
    ('marszlyn', 'Names', '0167_b', 2900,
     'Joanna\'s family name - "Marszłynowna[?]" (the mother of Katarzyna '
     'Rozdrażewska)',
     ['Marszłynówna', 'other (write it)'],
     'A patronymic in -ówna would be the only one in the entry. Read the '
     'letters.'),
    ('sadi', 'Names', '0167_b', 3000,
     'The word after "Feliciani Parys" - "sa[is/m?]di"?',
     ['secundi', 'samdi', 'other (write it)'],
     'The sense points to "secundi (voti)" - of her second marriage, to '
     'Karol Rozdrażewski - after "primi ... Feliciani Parys". Read the '
     'letters.'),
    # -------------------------------------------------------------- SUMS ---
    ('nierzychow_sum', 'Sums', '0162_a', 1550,
     'The widow Nierzychowska\'s load - "[?]ginta millium fp"',
     ['octoginta (80,000)', 'triginta (30,000)', 'other (write it)'],
     'The same widow\'s claim is "Triginta millium fp" on p. 167, and on '
     '164 her load is "Triginta Millium fp". If the page says octoginta '
     'here, the scribe slipped; if triginta, the reading is settled.'),
    ('triginta_veto', 'Sums', '0162_a', 1830,
     'The word after "nongentorum Triginta" - "veto[?]"?',
     ['octo (41,938 fl.)', 'other (write it)'],
     'The share of each fraternal caput: 41,930 fl. + this word. "octo" '
     'would complete the figure.'),
    ('kowski_name', 'Sums', '0162_a', 1680,
     'The name before "-kowski" (a load of 700 fl.)',
     ['(read the name - write it)', 'Zaleski again', 'other (write it)'],
     '"Generos[?] [?]kowski septingentorum fp" - the surname is cut at its '
     'start. Read what stands.'),
    ('bowski_name', 'Sums', '0162_a', 1730,
     'The name before "-bowski" (a load of 666 fl. g. 20)',
     ['(read the name - write it)', 'other (write it)'],
     '"Generos[?] [?]bowski sexcentorum sexuginta sex fl." - read the '
     'surname.'),
    ('money_formula', 'Sums', '0162_a', 700,
     'The money formula after the figures - here "sex tlor~[??] ge~[?]"',
     ['flor~ gross~', 'fl. gr.', 'other (write it)'],
     'Elsewhere the entry writes "fl. g~ 20 Polonicalium" and "flor~ gros~ 5 '
     'Polon~". Read what stands in this line (the same question covers "fl. '
     'gn[?] 20" two lines below).'),
    ('pawlowa_word', 'Sums', '0162_a', 1900,
     'The word before "Pawłowa" - "ex [?]tio Pawłowa"',
     ['praedio', 'fund[o]', 'other (write it)'],
     'The 12,000 fl. charge "from the ... of Pawłowa" - read the word.'),
    # ------------------------------------------------------------- WORDS ---
    ('reponidem', 'Words', '0162_b', 1230,
     '"quietatio ... non reponi[dem?]" - the verb form',
     ['reponendam', 'repositam', 'other (write it)'],
     'The quietation of the 3,500 ducats and the silver was not brought '
     'back into court. Read the ending.'),
    ('procet', 'Words', '0162_b', 1400,
     '"procet[?] divisionem perfecerant et procet[?] Decretum" - the word '
     '(it stands twice)',
     ['profectum', 'praecise', 'other (write it)'],
     'Read the word: the division was completed "in that quality and '
     'quantity" ...'),
    ('quirrimo', 'Words', '0162_b', 1750,
     '"nulli casui fortuito subjectus quirrimo[?]" - the word',
     ['quirimo', 'usurario', 'other (write it)'],
     'The sums had out-run their provisions for more than sixty years; read '
     'the word after "subjectus".'),
    ('quani', 'Words', '0163_a', 500,
     '"libertatemque sui a quani[?] eorundem successorum impetitione" - the '
     'word',
     ['quanta', 'quavis', 'other (write it)'],
     'Read the word after "a".'),
    ('brtis', 'Words', '0164_a', 1980,
     'The word between "Oporowa" and "Oporowka" - "[br?]tis"',
     ['sortis', 'cum sortibus', 'other (write it)'],
     'The second scheda lists "Oporowa [br?]tis Oporowka Kałowa" - the '
     'Oporowo with its parts Oporówka and Kałowo. Read the word.'),
    ('hisc_e', 'Words', '0162_a', 300,
     '"liberi pronunciatis, hisc[e?] partibus negotium inducere jubet" - the '
     'word',
     ['hisce', 'ipsis', 'other (write it)'],
     'Read the word before "partibus".'),
    ('auguratem', 'Words', '0161_b', 950,
     '"terminus ... in augurat[em?] intercessit" - the word',
     ['augurationem', 'augustam', 'other (write it)'],
     'The summons term lapsed "in ..." - read the word.'),
    ('addidem', 'Words', '0161_b', 2700,
     '"adjudante et addi[dem?] mae[s?] ad prostrandum Juramentum" - the two '
     'words',
     ['(read them - write it)', 'other (write it)'],
     'Before the oath was taken. Read both words.'),
    ('adpsit', 'Words', '0161_b', 1800,
     '"aliquod documenta ad[?]psit et subscripsit" - the verb',
     ['adhaesit', 'adspexit', 'other (write it)'],
     'He attached some documents to his summary and subscribed. Read the '
     'letters in the middle.'),
    ('minipali', 'Words', '0162_a', 480,
     '"agentibus ulteri[us?] in minipali[?] negotio" - the word after "in"',
     ['principali', 'minipali', 'other (write it)'],
     'The session continues "in the ... business". "principali" is proposed '
     'from sense; read the letters.'),
    ('go_naniae', 'Words', '0164_a', 280,
     '"Feria 2da ante Festum Assumptionis in actum[?] Go[?]naniae[?] anno '
     '1737" - the two words',
     ['(read them - write it)', 'other (write it)'],
     'The complanatio of Mariana\'s dowry was levied at Poznań on the '
     'Monday before the Assumption. Read the two words after "in actum".'),
    ('eisneunt', 'Words', '0167_a', 1000,
     '"transactionesque posteriores praemissam summam non eisneunt[?]" - '
     'the verb',
     ['tangunt', 'eunt', 'other (write it)'],
     'The later transactions do not ... the sum of 30,000 fl. Read the '
     'verb.'),
    ('hendo', 'Words', '0167_a', 250,
     '"portionem Maturnam extra hendo[?]" - the word',
     ['[h]endo', 'ordinem', 'other (write it)'],
     'Read the word after "extra".'),
    ('compin', 'Words', '0167_a', 380,
     '"si Judicio suo co[m/ns]pin[dem?]" - the word',
     ['comprend[er]e', 'compingere', 'other (write it)'],
     'Read the word after "co".'),
    ('arbitatem', 'Words', '0167_a', 1450,
     '"Judicium Arbita[tem?]" - the word',
     ['arbitratum', 'arbitri', 'other (write it)'],
     'Read the ending.'),
    ('insto', 'Words', '0167_a', 1900,
     '"anno 1736to insto[?] profectitiam" - the two words',
     ['(read them - write it)', 'other (write it)'],
     'Read what stands before "profectitiam".'),
    ('subtam', 'Words', '0166_a', 700,
     '"pro debito subta~am Golinscianam maturnam gravante" - the word',
     ['subnatam', 'substantam', 'other (write it)'],
     'Read the word: the maternal Golinscian debt bearing down.'),
    ('ressibilibus', 'Words', '0166_a', 1350,
     '"res[s?]ibilibus ad varias [E?]ulesias" - the two words',
     ['responsalibus / ecclesiis', 'other (write it)'],
     'The inscriptiones of Oporowo ran to various churches. Read both '
     'words.'),
    ('exdiuim', 'Words', '0166_b', 1100,
     '"Determinata ... Maturnae substantiae exdiuim[?]" - the word',
     ['extra', 'ex divisione', 'other (write it)'],
     'Read the word after "substantiae".'),
    ('illas_manente', 'Words', '0166_b', 1250,
     '"quo ad fortunam utramque illa[s/m?] manente" - the word',
     ['illas', 'illam', 'other (write it)'],
     'Read the word after "utramque".'),
    ('pro_mimixta', 'Words', '0166_b', 1600,
     '"soli donum binorum et midii pro[??]" - the two letters',
     ['(read them - write it)', 'other (write it)'],
     'After "duorum et medii" - read what stands before "mimixta".'),
    ('summus', 'Words', '0167_b', 1500,
     '"in uni originalis summ[us?]" - the ending',
     ['summus', 'summa', 'other (write it)'],
     'Read the ending of the word.'),
    ('scriptuis', 'Words', '0167_b', 1100,
     '"numeraris scriptu[?]is" - the ending',
     ['scripturis', 'scriptis', 'other (write it)'],
     'Read the ending.'),
    ('differ', 'Words', '0167_b', 1150,
     '"differ[?]itatem scriptionis" - the word',
     ['diversitatem', 'differentiam', 'other (write it)'],
     'The hand of the letter of 1736 was not that of the late Andrew '
     'Radoliński. Read the word.'),
    ('gmae', 'Words', '0167_b', 2000,
     '"post Dominicam [?]gmae~ anno 1745" - the word',
     ['Gaudete', 'Judica', 'other (write it)'],
     'The Sunday before which Katarzyna\'s 40,000 fl. were inscribed. Read '
     'the word.'),
    ('prodisse', 'Words', '0167_b', 2450,
     '"[?]bus~ pro[?]isse" - the two words',
     ['(read them - write it)', 'other (write it)'],
     'Before "verum hoc Decreto Condicionali" - read what stands.'),
    ('subdapiferida', 'Words', '0161_a', 500,
     '"Dominico Zboinatis Subdapifinda[?] Bidgostiensi" - the office form '
     'and the family name',
     ['Subdapiferida', 'other (write it)'],
     'The scribe\'s office forms run -ida: "Castellanida" here, '
     '"Dapiferidae" in Konin Gr.118, "Thesaurarida" in Gr.117. Read the '
     'letters after "Subdapifer" and the name before it.'),
    # --------------------------------------------------------- PROPOSALS ---
    # Readings proposed in the morning session (intake/split_and_settle.py)
    # and WITHDRAWN the same day: the editor's fresh transcription keeps the
    # original doubts, and their word stands until they rule here.
    ('p_diversae', 'Proposals', '0164_b', 700,
     '"dive[n/r?]ae formae" - proposed: "diversae formae" - rule',
     ['diversae', 'divinae', 'other (write it)'],
     'The silverware of the late Stephen Paul and Antoni, "of ... form".'),
    ('p_conges', 'Proposals', '0163_b', 2500,
     '"[?]ges~" (three places) - proposed: "con~ges~" (conjuges) - rule',
     ['con~ges~', 'other (write it)'],
     'The couples of the complanatio lines; the sibling units write '
     '"conjuges" unflagged.'),
    ('p_solutam', 'Proposals', '0165_b', 850,
     '"[lu?]atam" - proposed: "solutam" ("as if paid over by Kałowski") - '
     'rule',
     ['solutam', 'l[u]atam', 'other (write it)'],
     'Read the letters before "atam".'),
    ('p_sororem', 'Proposals', '0163_b', 2600,
     '"fororem[?]" - proposed: "sororem" ("this last sister") - rule',
     ['sororem', 'fororem', 'other (write it)'],
     'Mariana is the third daughter; "soror" fits the sense. Read the first '
     'letter.'),
    ('p_kotarbski', 'Proposals', '0164_a', 2050,
     '"Kołarbski[?]" - proposed: "Kotarbski" (the family as on p. 165) - '
     'rule',
     ['Kotarbski', 'Kołarbski', 'other (write it)'],
     'Read the fourth letter (ł or t).'),
    ('p_alterius', 'Proposals', '0163_a', 1430,
     '"altenius [post/parte?]" - proposed: "alterius post" (the second '
     'wadion, made after the sterile death of 1708) - rule',
     ['alterius post', 'altenius post', 'other (write it)'],
     '"altenius" is not a Latin word. Read both words.'),
    ('p_actis', 'Proposals', '0167_b', 2050,
     '"coram autis[?] Castrensis" - proposed: "coram actis Castrensis" - '
     'rule',
     ['actis', 'autis', 'other (write it)'],
     'The formula "coram actis Castrensis" stands four times in the entry. '
     'Read the letters.'),
    ('p_autem', 'Proposals', '0164_a', 1200,
     '"jam autoni[?] indictionem" - proposed: "jam autem" - rule',
     ['autem', 'other (write it)'],
     'Read the word: "now however the indiction ... was removed".'),
    # --------------------------------------------------------- PRINCIPLES --
    ('pr_nieszwiez', 'Principles', '0161_a', 1450,
     'The endings of "Nieszczeviec-" (the starost of Niszczewice, 12 places) '
     'were PROPOSED to be completed by the grammar of each sentence (dative '
     '-i, accusative -em, genitive -is), the scribe\'s stem kept - not '
     'applied; your fresh transcription keeps the doubts. Rule on the '
     'principle',
     ['accept the completions (they go back in)',
      'leave the doubts as they stand',
      'review each on a later sheet'],
     'Sample rows: "Capitaneo Niszczeviens[em?]" here; "Capitaneum '
     'Nieszczevice[m?]" on 161v; "in archivo ... Nieszczevicen[em?]" on '
     '161v. The same rule would complete ~100 other flagged case endings '
     '(the list with its witnesses: intake/split_and_settle.py).'),
    ('pr_changes', 'Principles', None, None,
     'The 108 readings applied in the morning session (case endings '
     'completed where the grammar admits one reading, formulas completed, '
     'the scribe\'s spellings kept) were WITHDRAWN when your fresh '
     'transcription of p. 161 kept the original doubts; they wait in '
     'intake/split_and_settle.py with the witness for each. Accept the lot '
     '(re-apply), or leave the text as you transcribed it?',
     ['re-apply the lot', 'leave withdrawn',
      'I will review the list before it stands', 'revert some (write which)'],
     'This row needs no scan - it rules on the principle and the record.'),
]

assert all(r[5] for r in ROWS), 'every row needs options'
