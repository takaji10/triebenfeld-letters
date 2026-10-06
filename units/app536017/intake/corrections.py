# -*- coding: utf-8 -*-
"""APP 53/6/0/-/17 read again from the scans, 2026-10-07.

    python units/app536017/intake/corrections.py            # check only
    python units/app536017/intake/corrections.py --write    # once

Run once, after build_pages.py --write. A record: do not run it again, and do
not run build_pages.py --write after it.

The editor's text of this entry was a first reading with 109 marks of doubt
in 713 words, and the editor asked (2026-10-07) for it to be read again and
put right "only if you're confident". Both pages were read word for word,
enlarged. What made a confident reading possible is on the same scans: the
next entry (leaf 27 verso to leaf 28) is the same plaintiff's suit against
another Łukomski in nearly the same words, and the two after it end in the
same set words, each in a slightly different state of wear. Where all agree
the reading is taken. So each of the three paragraphs is replaced whole
(NEW); the log keeps the editor's text beside it.

The clerk abbreviates nearly every word. As in the edition's other Latin,
the abbreviations are filled out without marks where the word is certain.
What stays marked:

- "exped[ie]t" in the heading: written "expedt" with a mark; the tense is
  supplied.
- "motibus[?]": so it looks here; the next entry has a word of the same
  length that looks like "juditibus". Not resolved.
- "lucran~ et succumben~", "mix~": the letters written; the endings are not.

The Polish words in the middle of the entry are the editor's reading, which
the scan bears out; one doubling ("pospospolithego") is not on the scan.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
import build_pages as B  # noqa: E402

# (page, which paragraph of the editor's page, the text as read on the scan, why)
NEW = [
    ('0027_a2', 0, 'Łukomski Visionem exped[ie]t',
     'the heading is "VISIOm EXPEDt" with marks of abbreviation: Łukomski is to carry out the inspection, which is what the '
     'decree orders ("Quam Visionem pars Citata ... expedire debet"). The same heading stands over the next entry'),
    ('0027_a2', 1,
     'Exortis partium infrascriptarum Controversiis super citationem literalem terrestrem Coninensem qua Nobilis Albertus '
     'Thrąmpczyńsky Otha ex interesse suo Actor Nobilem Thomam Łukomsky cittavit secundo post paenam Contumaciae pro eo: '
     'quia ipse anno praesenti constructo stagno cum caeteris vicinis suis cum quibus sibi salvam agendi actionem '
     'reservavit in haereditate villae Łukom quo stagno eidem Actori quantum ad interesse eius pertinet ingentem '
     'quantitatem silvae et borrae pascuorum sterilium necnon pratorum per nimiam dettentionem aquae in eisdem '
     'haereditatibus villarum Trąmpczino, Nowawiesz et Osziny inundavit alias zalial drzewa pospolithego rodzaynego dembiny '
     'bucziny jeszyeniny thim zaliewkyem poszuszil do budowania i do barczi godnego Faciendo praemissa in grave damnum et '
     'iniuriam Actoris Aestimationis ad Decem millia florenorum Hungaricalium puri auri et iusti ponderis et totidem damni '
     'Citatione ipsa cum sua copia praemissa latius enarrante Judicium praesens Terrestre Coninense Controversiis partium '
     'praefatarum coram Judicio praesenti factis Exauditis Ad affectationem Juridicam partis Citatae Juri communi '
     'inhaerendo decrevit praesentibusque decernit Visionem Juridicam Nihilominusque addidit prout praesentibus addit '
     'Ministerialem terrestrem quem sibi pars Citata elegerit ad videndum videlicet et conspiciendum quo in loco cuius in '
     'fundo iniuria praefata illata et utrum facta necne: Quam Visionem pars Citata sumptibus proprijs Ministeriali '
     'conducto a data praesentis decreti recte in sex',
     'read whole against the scan and against the next entry, which has the same words. What changes the sense: '
     '"Exortis ... Controversiis" (disputes having arisen); "citationem literalem" (a written citation); "in grave damnum et '
     'iniuriam Actoris Aestimationis ad Decem millia"; "Controversiis ... coram Judicio praesenti factis Exauditis"; "Juri '
     'communi inhaerendo decrevit praesentibusque decernit Visionem Juridicam"; "Ministerialem terrestrem quem sibi pars '
     'Citata elegerit ad videndum videlicet et conspiciendum quo in loco cuius in fundo iniuria praefata illata et utrum '
     'facta necne" (the court adds one of its messengers, of the defendant\'s choosing, to see where and on whose ground '
     'the wrong was done and whether it was done: the earlier reading had "Mutem terem", taken as a mutual term); '
     '"Ministeriali conducto a data praesentis decreti"'),
    ('0028_a1', 0,
     'septimanis consensu partium ad id accedente in loco differentiarum expedire debet sub paenis motibus[?] per partem '
     'Citatam in defectu expeditionis lucran~ et succumben~ Cui Visioni partes ambae interesse debent: qua itaque visione '
     'ut praemissum est expedita vel non partes ambae praefatae in proximis futuris terminis terrestribus Coninensibus '
     'proxime et immediate in Conin celebrandis habituri sunt terminum peremptorium ad audiendum a praefata Visione iuris '
     'restitutionem coram Judicio per Ministerialem et alia omnia quae iuris erit in causa praesenti peragendum mix~ '
     'visionis decretum praesens conservationem termini et Acta Nullius partis Jure laeso',
     'read whole against the scan and against the same words at the head of leaf 28: "consensu partium ad id accedente in '
     'loco differentiarum expedire debet"; "Cui Visioni partes ambae interesse debent" (both parties must attend); '
     '"habituri sunt terminum peremptorium"; "ad audiendum a praefata Visione iuris restitutionem coram Judicio per '
     'Ministerialem et alia omnia quae iuris erit in causa praesenti peragendum". The second reading of these lines in the '
     'editor\'s file is not used'),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    _heading, parts = B.read_source()
    rows = [(pid, parts[(1, pid)][i], new, why) for pid, i, new, why in NEW]
    courtbook.correct(UNIT_DIR, B.SLUG, B.DOCS, rows, '--write' in sys.argv, source='read again on the scan')


if __name__ == '__main__':
    main()
