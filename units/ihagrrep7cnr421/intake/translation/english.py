# -*- coding: utf-8 -*-
"""The English of I. HA GR, Rep. 7 C, Nr. 421, written in session (Claude, 2026-11-21).

    python units/ihagrrep7cnr421/intake/translation/english.py      # writes doc<N>.yml beside it

Translated from the corrected German (and, for the last page of document 6,
the Polish) page by page, under the rules translate.py gives its translator
(reference/translation_glossary.yml: Regierung is Government, Revers "written
undertaking"; the edition's names: Prusimski for the clerks' Prusimiski,
Poznań for Posen, Kalisz for Kalisch, Pyzdry for Peysern, Trąbczyn for
Trąmpczyn, Gniezno for Gnesen; Mondro, the name as he signs it; "Mondo" in the note under document 1 as written).
"#" after a sum is rendered "ducats" (the bond: Dutch ring ducats in gold).
Marks of doubt ([?], [H?]) are kept where the original has them, on the
word that renders the doubtful one; a word the transcription leaves
unexplained but whose sense the passage fixes is rendered by that sense, as
the translator's rules ask; the editor's spot sheet (2026-11-21) has since
settled most of them ("Hoflager", "Deckung", "abrechnen", "muste ich",
"Fabryki"). Since 2026-11-22 (the editor; EDITORIAL_RULES, "An unread word in
the English") a word that stays unread is never kept in the original's letters:
its sense with [?] where the passage fixes it, "[...]" where not; the Latin is
given in English (the Latin in brackets where the document turns on it), and
abbreviations expanded (S. W. Treasurer of Wschowa, S. N. Starost of
Nieszczewice), after the re-reading of that day (holding.py, CORRECTIONS).
write_cache.py puts the files into the translation cache.
"""
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
# the marks of doubt as check_translations counts them in the English (with "[...]")
MARK = re.compile(r'\[[^\]]*\?\]|\[\.\.\.\]')

EN = {
    1: [
        """The files in which[?] [...] the [...] underlined in red in this petition are to be found (which I do not find in the collection sent to me by His Excellency[?] v. Goldbeck) are to be attached for me, and if need be requested from the archive of the General D[...] etc. 18 Oct. Massow

Resolved: that the resolution of the Government of 10 Sept. this year must simply stand, since every creditor who has personal claims to make on the former property of an insurgent will understand of himself that the costs of the war must[?] far exceed the whole estate of such an insurgent. B[erlin], 21 Oct. [17]99. So resolved the same day. Willenz

Most Serene, Most Mighty, Most Gracious King and Lord! Kalisz, 8 October 1799.

In the year 1794 I gave the Starost von Prusimski a loan of 12,000 ducats in gold against a written undertaking, which he promised to repay at St John's Day 1795. Before the date of payment came, however, von Prusimski became a fugitive, and through the sentence of confiscation passed against him his property was seized by the Fiscus.

After consulting with him, von Prusimski, I did take possession of the estates of Trąbczyn and Nowawies belonging to him, but I had to give them up to the Prince of Hohenlohe-Ingelfingen, to whom these estates had been given by Your Royal""",
        """Majesty's own Most High Person, upon the opening of the judgment of revision, and was referred with my said claim to the Fiscus.

I then sued the Fiscus for payment of it on 6 September this year, but by the decree of the 10th of the same month, which I enclose in copy, I was told that before my suit could be admitted the real character of the said claim must first be proved.

Since by the judgment of revision mentioned above the contrary was already established, and since moreover I demand my satisfaction not from the""",
        """Prince of Hohenlohe but from the Fiscus as possessor of the whole of von Prusimski's property, the suit in this matter was not inadmissible on the ground that the claim in question is merely personal. Referring to the Most High Cabinet Order of 14 September 1796, I pressed repeatedly for a hearing to take evidence to be appointed; against my expectation, however, I was once more dismissed with the suit by the decree of the 27th of the same month, which I likewise present in copy.

As I cannot rest content with these adverse rulings,""",
        """I see myself compelled, for the following reasons, to have recourse to Your Majesty's Most High court. By the Cabinet Order just mentioned, No. 2, it is indeed ordained that the Fiscus, in respect of compensation for damage, takes precedence over all personal creditors of an insurgent, and that it shall then rank after them with the penalty of confiscation. It is thus clear that the Fiscus must give satisfaction from the confiscated property for a personal claim on the insurgent, if its correctness is proved from elsewhere (aliunde), otherwise than by my mere written undertaking; and that there is therefore no sufficient ground in the present case for dismissing the suit because""",
        """the claim is merely personal.

The declaratory Court Rescript of 17 September 1796 can find no application here, since on the one hand it interprets the Cabinet Order, the Most High will of Your Royal Majesty Yourself, extensively and against its clear content, which belongs solely to Your Most High[?] Person and not to the Chief of Justice; and on the other hand it touches on matters of substance.

But even the said Rescript lays down that personal suits against the Fiscus are to be admitted without question at the parties' request, but that a certified""",
        """statement of the damage done by the insurrection, for which by legal principles the insurgents are liable jointly and severally (in solidum), might be laid before such a plaintiff by the Fiscus, from which it should appear that the confiscated property of the insurgents is far from sufficient to cover these damages.

I will gladly accept that procedure, but reserve my objections to such a liquidation of damages, and most humbly ask Your Royal Majesty

to grant me a hearing at law, and to instruct the Government at Kalisz to open the taking of evidence on the suit I have brought against the Fiscus.""",
        """I who remain, until death, in deepest reverence Your Royal Majesty's most humble Stanisl v. Chełmski, in his own hand

drafted by Mondo

No. 55.""",
    ],

    2: [
        """presented 18 Sept. 1799. Copy.

Decree on the representation of v Chełmski of 6 Sept. 1799 in the matter of himself ./. Prusimski: For resolution, by copy of this decree: before the suit he asks for can be admitted, he must first show the real character of the claim, and that he must for that reason be satisfied from the estates. Kalisz, 10 Sept. 1799. Royal South Prussian Government Chancery. To von Chełmski, into the hands of Cr. Councillor Mondro

here.

4980.

presented 5 October 1799. Copy.

Decree

in the case of von Chełmski ./. Prusimski. By copy of the decree, for resolution: it remains, on the ground""",
        """of the entirely clear content of the judgment of revision, by the ruling of the 10th of this month, all the more as he himself treats this claim as a personal one. Kalisz, 27 Sept. 1799. Royal South Prussian Government Chancery. Copy of the decree to[?] the criminal-court councillor[?] Mondro, here.

3459.""",
    ],

    3: [
        """Berlin, 21 October 1799. Resolution for Stanislaus von Chełmski at Kalisz.

(concerning his claim on the insurgent

v. Prusimski.) Gr.

acc. on the 21st.

ad rev. on the 22nd.

Files general: concerning the debts of the insurgents, to the Reg[istry]:

on the 30th to the post. South Pr.

His Royal Majesty of Prussia etc., our most gracious Lord, has Stanislaus von Chełmski informed hereby, as answer to the representation he submitted on the 8th of this month concerning his claim on the former Starost von Prusimski, that the resolution of the Government there of 10 Sept.

this year must simply stand, since every creditor who has personal claims to make on the former property of an insurgent will understand of himself that the costs of war spent on putting down the unrest the insurgents raised, and the damage they caused, far exceed the whole estate of such an insurgent.

Signed: Berlin, 21 October 1799. By command.

[Signature]

[?] on the 22nd.

3426.""",
    ],

    4: [
        """Presented 15 Dec. 99. Most Serene, Most Mighty, Most Gracious King and Lord! Kalisz, 7 December 1799.

The criminal-court councillor Mondro asks, in the name of v Chełmski of Łukom, for a preliminary ruling on the complaint against the Government at Kalisz in his matter ./.

the Fiscus, over the dismissal of the suit.

Earlier papers (Anteriora). [...] with the same [...] [...] 19 [...]

As early as 9 October this year my client, the landowner von Chełmski, submitted to Your Royal Majesty a complaint against the Government here over the improper dismissal of a suit brought against the Fiscus concerning a claim of

12,000 ducats,""",
        """and most humbly asked for a hearing at law. As no preliminary ruling has followed yet, I make bold to petition Your Most High Majesty again on this matter. The decrees of the Government plainly rest on a misunderstanding, in that they confuse the suit that von Chełmski first brought against the Prince of Hohenlohe, as present owner of the Trąbczyn estates confiscated from Prusimski, with the one that is directed against the Fiscus alone.

That the claim of 12,000 ducats cannot be sued for against the Prince of Hohenlohe-Ingelfingen, my client understands of himself. On the other hand, the Court Rescript of 17 September 1796 in no way prevents him from claiming the said capital, under the clear provision of the Most High[?] Cabinet Order of the 16th of the same month and year,""",
        """from the Fiscus.

If, moreover, the Government follows the letter of the Court Rescript, which is not binding in itself, it nonetheless cannot refuse von Chełmski a hearing at law in this matter, since this very Rescript expressly lays down that if the party does not rest content with a dismissal by decree, the taking of evidence is to be opened and the matter formally adjudged.

This, in my opinion, must happen in every legal matter where the party cannot be convinced that the dismissal was lawful. I enclose a copy of the suit with the bond on which it rests (ex quo), which my client had already brought before the Government at Poznań; only I must remark that he had first sued Prusimski before the judgment of confiscation""",
        """had been passed.

On the resumption of the proceedings against the Fiscus nothing was changed but the person. So that the matter may not be delayed any longer and the plaintiff may at last be satisfied, I most humbly ask Your Royal Majesty

to have a preliminary ruling given him without delay. I who remain, until death, in deepest reverence Your Royal Majesty's most humble Mondro

criminal-court councillor

No. 33.""",
        """ad no. 9.

A copy of the resolution of 21 Oct. given to his principal is to be communicated to the criminal-court councillor. B[erlin], 23 Dec. [17]99. So resolved the same day.

Willenz""",
    ],

    5: [
        """Copy

Kalisz, 1 December 1799.

Most Serene etc. As early as 9 October this year my client, the landowner v Chełmski, submitted to Your Royal Majesty a complaint against the Government here over the improper dismissal of a suit brought against the Fiscus concerning a claim of 12,000 ducats, and most humbly asked for a hearing at law. As no preliminary ruling has followed yet, I make bold to petition Your Most High Majesty again on this matter. The decrees of the Government plainly rest on a misunderstanding, in that they confuse the suit that v. Chełmski first brought against the Prince of Hohenlohe, as present owner of the Trąbczyn estates confiscated from Prusimski, with the present one, which is directed against the Fiscus alone.

That the claim of 12,000 ducats cannot be sued for against the Prince of Hohenlohe-Ingelfingen, my client understands of himself. On the other hand the Court Rescript of 17 September 1796 in no way prevents him from claiming the said capital from the Fiscus, under the clear provision of the Most High Cabinet Order of the 16th of the same month and year.

If, moreover, the Government follows the letter of the Court Rescript, which is not binding in itself, it nonetheless cannot refuse v. Chełmski a hearing at law in this matter, since this very Rescript expressly lays down that if the party does not rest content with the dismissal by decree, the taking of evidence is to be opened and the matter formally adjudged. This, in my opinion, must happen in every legal matter where""",
        """the party cannot be convinced that the dismissal was lawful.

I enclose a copy of the suit with the bond on which it rests (ex quo), which my client had already brought before the Government at Poznań, - only I must remark that he had first sued v Prusimski before the judgment of confiscation had been passed.

On the resumption of the proceedings against the Fiscus nothing was changed but the person. So that the matter may not be delayed any longer, and the plaintiff may at last be satisfied, I most humbly ask Your Royal Majesty to have a preliminary ruling given him without delay. I who etc.

Your Royal Majesty etc.

Mondro

criminal-court councillor.""",
    ],

    6: [
        """Copy.

Most Serene etc. Poznań, 19 March 1799. Suit of Stanisl[aus] von Chełmski of Łukom near Pyzdry ./. the Starost Anton v Prusimski of Trąbczyn, concerning 12,000 ducats on the strength of a handwritten bond (ex chirographo).

On 16 June 1794 I had to advance to the Starost Anton von Prusimski of Trąbczyn, Nowawies, Osiny and the Trąbczyn Hollanders 12,000 ducats for one year, namely until St John's Day 1795, for which he handed me the blank note enclosed in copy, in the presence of Jacob von Bieńkowski of Mierzewo near Gniezno and of Antonius v Przeradzki. At the loan itself it was agreed between me and the defendant debtor, in the presence of those witnesses, that if the repayment of these 12,000 ducats did not follow on the date fixed for payment, I might treat the said""",
        """blank note as a contract of antichresis (contractus antichreticus: the creditor takes the income of the pledge in place of interest) and take possession of the estates listed as a pledge. Payment did not in fact follow on the date agreed, namely at St John's Day last year, and I therefore took possession of these estates at that time.

Meanwhile my debtor was charged by the Fiscus with taking part in the insurrection that broke out in this province in 1794, and because he has not even yet returned, his property was to be seized by the Fiscus in the month of May last year, which I had forestalled only by taking possession of the said estates in the month of June.

The Fiscus did then bring a suit for eviction before Your Royal Majesty on 7 December 1795, and a hearing on it was set for the 27th""",
        """27 February this year before Your Most High Government; but at it the following settlement was reached between me and the Fiscus: that I am to sequestrate the oft-mentioned estates, first deduct the interest for delay at 7 per cent from the income, but then render account, while still pursuing my claims at law.

Before Your Royal Majesty I therefore bring my suit against the Starost Anton von Prusimski for these 12,000 ducats, with the request that a hearing to take evidence be appointed, and that the defendant be not only summoned to it but also condemned both to pay the 12,000 ducats owed and to pay interest for delay at 7 per cent, with costs.

In proof of the correctness of the loan, and that he stipulated taking possession of the pledge in""",
        """case of non-payment on the fixed date, I refer also to the witnesses proposed above, whom I at the same time most humbly[?] ask to have examined, and that this my suit be deemed sufficiently substantiated. who am etc.

Your Royal Majesty

etc.

v Chełmski.""",
        """Copy. The blank note named below, signed with my own hand, wishing all the more to secure the date of its payment and to set at rest the concern of the Honourable Lord Chełmski, Treasurer, about being paid on the eve of St John the Baptist in the year 1795, I give this present undertaking of my free will and deliberately, that if on the date I do not pay the 12,000 ducats named below in good Dutch gold ring ducats, without interest, I permit free entry into my[?] estates, that is the villages of Trąbczyn, Nowawies, Osiny, the village of Zarobna[?], Łazy and all the Hollanders belonging to this estate, excepting no village, forest or wood, except the iron works, the magazine and the stores of timber needed for them; which estates named above the Honourable Lord Chełmski shall hold in lieu of interest, without any account, until this sum, expressed in this blank note, turned to my use and taken in cash before witnesses, is repaid; and I wish this undertaking to have[?] such force as though it had been made before a court of my own. Given at Łukom, 16 June 1794 [...].

Belonging[?] to the Honourable Lord Stanisław Chełmski, Treasurer of Wschowa: a blank note for 12,000 Dutch ring ducats. Antoni Prusimski

Starost of Nieszczewice, in his own hand

Jakub Bieńkowski

friend present

Antoni Przeradzki, friend present.""",
    ],

    7: [
        """Berlin, 23 December 1799. To the criminal-court councillor Mondro at Kalisz.

(concerning v. Chełmski's complaints against the Kalisz Gov[ernment] over the dismissal of his suit

against the Fiscus) acc. on the 23rd.

ad rev. on the 24th.

Encl. attached

Gr.

on the 31st O. to the post. South Pr.

To the representation submitted on the 7th of this month by the criminal-court councillor Mondro, as attorney of von Chełmski of Łukom, he is given to see from the enclosed copy in what manner von Chełmski was answered on 21 October this year on his complaints against the Government there over the dismissal of his suit against the Fiscus.

Signed: Berlin, 23 Dec. 1799. By command.

[Signature]

v. [?] on the 25th. 4168.""",
    ],
}

# The rare pair Abweisung/Anweisung (reference/translation_glossary.yml, rare_pairs):
# every Abweisung here is the dismissal of Chełmski's suit, never an instruction.
_ABW = {'de': 'Abweisung', 'rendered_as': 'dismissal', 'alt': 'instruction (Anweisung)',
        'why': 'Abweisung, the dismissal of the suit by the Government; not Anweisung, an instruction.'}
FLAGGED = {(4, 1): [_ABW], (4, 3): [_ABW], (5, 1): [_ABW], (5, 2): [_ABW], (7, 1): [_ABW]}


def main():
    for n, pages in EN.items():
        doc = {'pages': [{'page': i + 1, 'confidence': 'high', 'marker_count': len(MARK.findall(p)),
                          'en': p, 'flagged': FLAGGED.get((n, i + 1), [])} for i, p in enumerate(pages)]}
        with open(os.path.join(HERE, 'doc%d.yml' % n), 'w', encoding='utf-8', newline='\n') as f:
            yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=100000)
    print('wrote', len(EN), 'documents')


if __name__ == '__main__':
    main()
