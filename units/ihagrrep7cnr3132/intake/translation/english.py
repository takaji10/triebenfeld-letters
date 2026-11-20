# -*- coding: utf-8 -*-
"""The English of I. HA GR, Rep. 7 C, Nr. 3132, written in session (Claude, 2026-11-20).

    python units/ihagrrep7cnr3132/intake/translation/english.py      # writes doc<N>.yml beside it

Translated from the corrected German page by page, under the rules
translate.py gives its translator (the termbase in
reference/translation_glossary.yml: Regierung is Government, Kammer
Chamber; the edition's names: Prusimski for the clerks' Prusiemski, Poznań
for Posen, Kalisz for Kalisch, Włocławek for Wraclawek; Jezierski as
written). Marks of doubt ([?], [H?]) are kept where the German has them;
the office's marks are translated where they are words ("pr." received,
"abg." sent) and kept as written where they are numbers or initials.
write_cache.py puts the files into the translation cache.
"""
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))

EN = {
    1: ["""South Prussia
No. 5.
received 23 February 1803
19 Feb. 1803.

His Majesty the King has been pleased to remit to Your Excellency and to me, for a report, the enclosed original petition of a former Starost von Prusimski and of one Xaver Jezierski for leave to return to their fatherland. As I consider it necessary for our full information to see the files of the proceedings on their offences and their property, I have had the rescript to the Government at Poznań, enclosed in draft and fair copy, dispatched, and most obediently ask Your Excellency (factum) kindly to countersign it, to forward the fair copy for dispatch, and to be so good as to have the draft returned to the Privy State Chancery.

Berlin, 19 February 1803.

Goldbeck

To His Royal Actual Privy State, War and Cabinet Minister and directing Minister of Finance, Count von Haugwitz, Excellency"""],

    2: ["""received 22 April 1803

The Government at Poznań having sent in the files of the confiscation proceedings against the former Starost Anton von Prusimski and the canon von Jezierski, I do not fail to communicate them to Your Excellency herewith in 6 volumes, together with the draft of the joint report required by His Majesty the King, with the most obedient request that, should you have nothing to remark against the latter, you kindly countersign it, have the fair copy made and sent to me for my co-signature, and be so good as to return the draft and the files to me.

Berlin, 22 April 1803.

Goldbeck

To His Royal Actual Privy State, War and Cabinet Minister and directing Minister of Finance, Count von Haugwitz, Excellency"""],

    3: ["""An d 29 Apr. 1803

To His [sub?] lit. Lord von Goldbeck, Excellency

An v Prusimski & Jezierski

In full agreement with Your Excellency's enlightened opinion on Prusimski and Jezierski, I have signed the report Your Excellency kindly communicated to me, and had the fair copy made; and I have the honour to send you most obediently the fair copy, for your kind countersignature and dispatch, together with the draft. At the one place where it says that the confiscation of property must remain unalterable, I have believed, since this point belongs solely to your department, that I had to add that I

d. 3rd May. ins: cum 2 vol: Actor: pLch:""",
        """refrain from expressing an opinion, since this matter lies outside my sphere of business.

The files kindly communicated to me I return herewith with thanks.

Berlin, 29 Apr. 1803.

Haug[witz]"""],

    4: ["""received 21 May 1803

Our joint report on the return of Anton von Prusimski and Xaver von Jezierski to their fatherland having been answered by the cabinet order of yesterday's date, enclosed in the original and to be returned, I do not fail to send it most obediently to Your Excellency for your information, and with it, for your kind countersignature, the resolution to be given to the two petitioners and the order required to the Government at Poznań, in draft and fair copy; also a copy of the joint report, probably meant for Your Excellency's files, which the chancery had attached, no doubt by mistake, to your most esteemed letter; with the request that you be so good as to return the draft and the fair copies to me once you have co-signed them.

Berlin, 11 May 1803

Goldbeck

To His Royal Actual Privy State, War and Cabinet Minister and directing Minister of Finance, Count von Haugwitz, Excellency""",
        """Urgent
1261

1, The fair copies are to be laid before His [?] for signature[?], as is the draft. That done, they are to be delivered to His Excellency von Goldbeck's department with the cabinet order, act. copy of the cab. order and the expeditions,

and that with

2, Exp. 2., namely a [?] to His Excellency von Goldbeck aus dieses[?], and Exp. 3. 4. notified.

3, Exp. notificatorium to the Chamber cum mand.

[?]""",
        """to have these subjects take the oath of allegiance, and to report here how it has been done

4, Chamb. Exp. 3. [?]

v. Voss for co- Count Haug[witz]

27 May [?]"""],

    5: ["""Copy

Your Royal Majesty has most graciously been pleased to send us, for a report, the enclosed original representation of the former Starost von Prusimski and of Xaver von Jezierski, who left the country because of their part in the South Prussian insurrection and have now asked from Dresden for leave to return to their fatherland.

The files required from the Government at Poznań having come in, we can now most humbly report the following.

1., Anton von Prusimski was accused of having gone on 2 August 1794, before the outbreak of the South Prussian insurrection, from his estates near Kalisz to his Smiłowice estates in the district of Kuyavia, which now belongs to the department of the Government at Poznań; of having received daily visits there from the neighbouring nobility; and of the so-called Kuyavian insurrection having been brought to completion at his house on 21 Aug., and the act of confederation drafted and executed. He is also said to be among those South Prussian noblemen who met at Dresden in the winter of 1793/94 on account of the changes in the Polish state. All these accusations, however, rest for the most part only on a so-called Memoire raisonné, drawn up from the statements of some unnamed trusted Poles and officials, and have not been closely examined.

Nor did the Government think them sufficient to order against him the criminal proceedings against absent offenders, as was done in respect of some chief insur""",
        """gents, but, at the instance of the fiscal, only instituted the confiscation proceedings, because he had not returned in accordance with the general ordinances issued.

The fugitive was duly summoned in public; he did, from Italy, where his wife, who also died there, allegedly had to stay at the time to recover her health, hold out hope of his return and seek to avert the confiscation; but as he did not appear after all, the sentence of confiscation was drawn up, and after it had become final, his Trąbczyn estates were given to the Prince of Hohenlohe, his Pawłów estates to the present Major General von Sanitz, and his Smiłowice estates to Lieutenant General von Bischofswerder. Besides these he held no other property in the country.

2., The second petitioner, Xaver von Jezierski, was a canon in Włocławek and parish priest at Neustadt. He was named, partly in the Memoire mentioned above, partly by persons who were named, as one of those who stayed most often with von Prusimski at Smiłowice before the outbreak of the Kuyavian insurrection and worked most actively to bring this insurrection about. He is said to have drafted the proclamations to the people, to have""",
        """raised men, and to have been a member of a security commission set up by the insurgents at the time.

Against him too, who did not return from his flight, only the confiscation proceedings were instituted, and confiscation of his small property was decreed with final effect; it consisted only of the income of his benefices, taken into sequestration and since filled otherwise, of which he was also deprived by the sentence.

Neither of the two petitioners has been declared to have forfeited his nobility, nor has any capital punishment otherwise been fixed or reserved against them.

In proportion to their part in the insurrection, they have been punished, by the confiscation of their property, at which it must remain unalterably /: a point on which I, Count von Haugwitz, refrain from expressing an opinion, since it is not of my department :/, and by a 9 years' banishment from their fatherland, more harshly than many others who returned and submitted to a moderate fine or a term in a fortress. Nor is their part of such a kind that it would mark them out as dangerous men before others who stayed in the country or returned to it later; and since their petition is directed only""",
        """at leave to return, we are most humbly of the opinion:

that it might well be granted;

which, however, we most devotedly leave entirely to Your Royal Majesty's most high judgement.

Berlin, 30 April 1803

Goldbeck. Haugwitz

To His Royal Majesty."""],

    6: ["""Copy.

My dear Ministers of State, Grand Chancellor von Goldbeck and Count von Haugwitz! In view of the reasons seen from your report of the 30th of last month on the petition of the former Starost von Prusimski and of Xaver von Jezierski, which goes back herewith, and since I join you, the Grand Chancellor, in the view that the petitioners have been punished hard enough by the confiscation of their estates and nine years' banishment, I will hereby grant them the leave they asked for to return to their fatherland, and leave the further disposition to you accordingly, as your well-affectioned King.

Potsdam, 10 May 1803.

Friedrich Wilhelm

To the Ministers of State, Grand Chancellor v. Goldbeck and Count v. Haugwitz."""],

    7: ["""Copy.

Friedrich Wilhelm etc.

Our etc. In returning to you the 6 vol. of files in the matter of the inquiry against the former Starost Anton v. Prusimski and the former canon Xaver von Jezierski, sent in with your report of the 24th of March of this year, we at the same time send you, in the copy enclosed, the cabinet order issued on the 10th of last month, from which you will see that both have been granted the leave they asked for to return to their fatherland, and that the confiscation of property decreed against them, together with their 9 years' banishment, has been deemed a sufficient punishment for their part in the insurrection. Sind etc. Berlin, 11 May 1803.

Auzl etc. special command.

Goldbeck Haugwitz

To the South Prussian Government at Poznań

His Royal Majesty of Prussia, our most gracious Lord, hereby lets Anton v. Prusimski and Xaver von Jezierski know, on their immediate representation of 27 Jan. of this year, that the leave they asked for to return to their fatherland has been granted, on the assumption that they will conduct themselves there in future as loyal[?] subjects; that the confiscation of property decreed against them with final effect remains, however, unalterably in force, and that von""",
        """Jezierski must remain deprived of his clerical offices and benefices; but that otherwise they need fear no further inquiry or punishment for their part in the insurrection, on which the necessary has been ordered to the Government at Poznań this day.

Berlin, 11 May 1803.

Auzl.[?] etc. special command.

Goldbeck Haugwitz

To the former Starost Anton v. Prusimski and Xaver von Jezierski at Dresden."""],

    8: ["""Berlin, 30 May 1803

To His Royal Minister of State etc. von Voss, Excellency.

[H?]

His Royal Majesty having been pleased, by cabinet order of the 10th of this month, most graciously to grant the former Starost von Prusimski and Xaver von Jezierski the leave they asked for to return to their fatherland, I do not fail to bring this to Your Excellency's closer knowledge through the copy enclosed, and leave it most obediently to you whether you will be pleased to countersign the notificatorium on this matter to the Chamber at Poznań, enclosed in draft and fair copy.

Berlin, 30 May 1803

To His Royal Grand Chancellor, Minister of State, v. Goldbeck, Excellency.

[Signature M?]

d. 6th June both c. alltis ins.

I thank Your Excellency most kindly for the news given me in your most esteemed letter of the 11th of this month of the return of v. Prusimski and Xaver von Jezierski. With the original cabinet order kindly communicated to me I return to you""",
        """herewith the drafts and fair copies countersigned by me, and add most obediently that, with the countersignature of His Royal Minister of State etc. v. Voss, Excellency, I have also already instructed the Chamber at Poznań to have these subjects now take the oath of allegiance.

Berlin, 30 May 1803

Haug[witz]"""],

    9: ["""Berlin, 30 May 1803

To the Chamber at Poznań.

[H.?]

for the kind countersignature of His Royal Minister of State etc. von Voss, Excellency, in draft and fair copy

8 June of this year, sent by post.

Friedrich Wilhelm

In the copy enclosed We send you the cabinet order issued on the 10th of this month, by which the former Starost Anton von Prusimski and the former canon Xaver von Jezierski are granted leave to return to their fatherland, and command you now to have both take the oath of allegiance, and to report here how it has been done.

Sind etc.

Berlin, 30 May 1803.

By command:

[M?] Haugwitz"""],
}


def main():
    for n, pages in EN.items():
        doc = {'pages': [{'page': i + 1, 'confidence': 'high', 'marker_count': p.count('[?]') + p.count('?]') - p.count('[?]'),
                          'en': p} for i, p in enumerate(pages)]}
        with open(os.path.join(HERE, 'doc%d.yml' % n), 'w', encoding='utf-8', newline='\n') as f:
            yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=100000)
    print('wrote', len(EN), 'documents')


if __name__ == '__main__':
    main()
