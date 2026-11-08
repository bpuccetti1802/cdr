# -*- coding: utf-8 -*-
"""v3.58 dell'analisi ANSC (07/11/2026), dalla v3.57 sul file reale.

Richiesta dell'utente: nel capitolo «Atti a Testo Libero» dichiarare che il tema è trattato nel
documento specifico «ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.x.docx». Interventi:
  - nota di rinvio in testa al capitolo;
  - il paragrafo aggiunto nella v3.57 in fondo al capitolo perde l'affermazione «per le
    trascrizioni l'atto a testo libero può formarsi interamente in SIPO», che la v0.5 del
    documento specifico (rivista dall'utente) non sostiene più; restano i due fatti della
    comunicazione ANSC;
  - [R16] nomina il documento come v0.x (corrente: v0.5);
  - testata, frontespizio, Storia. Le ancore dei commenti di Word non cambiano.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_58_rinvio_testo_libero.py
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.57.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.58.docx')
DATA = '07/11/2026'
DOC = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.x.docx'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))


def trova(inizio, stile=None):
    t = [p for p in d.paragraphs if p.text.strip().startswith(inizio)
         and (stile is None or p.style.name == stile)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:60]))
    return t[0]


def svuota(p):
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)


# ------------------------------------------------------------------ nota in testa
titolo = trova('Atti a Testo Libero', 'Heading 1')
primo = trova('Questa tipologia di atti potrà essere redatta')
nota = docx.oxml.OxmlElement('w:p')
primo._p.addprevious(nota)
q = Paragraph(nota, primo._parent)
if primo._p.pPr is not None:
    q._p.insert(0, copy.deepcopy(primo._p.pPr))
q.add_run('Gli atti a testo libero sono trattati in un documento specifico, ').bold = True
r = q.add_run(DOC)
r.bold = True
r.font.name = 'Courier New'
q.add_run(' [R16], ').bold = True
q.add_run('al quale si rinvia per le due strategie e il loro confronto, i casi d’uso di servizio '
          'di ANSC, i servizi da usare, le pagine di SIPO e il recupero dell’atto formato sulla '
          'WebApp, i punti aperti. Il presente capitolo conserva l’impostazione iniziale del tema.')

# ------------------------------------------------------------------ paragrafo della v3.57
p = trova('Il tema è sviluppato nel documento dedicato [R16]')
if D.ha_commenti(p._p):
    raise SystemExit('paragrafo commentato')
svuota(p)
p.add_run('Due elementi, sviluppati nel documento specifico, condizionano il tema. Secondo una '
          'comunicazione ANSC [R15] i casi d’uso di servizio delle dichiarazioni — il '
          'corrispettivo ANSC dell’atto a testo libero — sono disponibili solo sulla web app: per '
          'le dichiarazioni le due modalità sono quindi l’unica via. E un atto formato con caso '
          'd’uso di servizio non genera annotazioni automatiche né comunicazioni anagrafiche: quegli '
          'adempimenti restano all’ufficio.')

# ------------------------------------------------------------------ [R16]
righe = [r for t in d.tables for r in t.rows if r.cells[0].text.strip() == 'R16']
assert len(righe) == 1
for c, testo in ((righe[0].cells[1], DOC + ' (versione corrente: v0.5)'),
                 (righe[0].cells[2], 'Documento specifico sugli atti a testo libero e sugli atti '
                                     'senza UC determinabile: casi d’uso di servizio di ANSC, le due '
                                     'strategie della web app e il loro confronto, i servizi ANSC '
                                     'da usare, le pagine di SIPO e il flusso logico del recupero, '
                                     'i punti aperti TL-nn.')):
    p0 = c.paragraphs[0]
    for x in p0.runs[1:]:
        x._r.getparent().remove(x._r)
    p0.runs[0].text = testo

# ------------------------------------------------------------------ testata e storia
for fatto in D.frontespizio(d, '3.58', 'ANALISI_Integrazione-ANSC_v3.58'):
    print('  ' + fatto)
for sez in d.sections:
    for t in sez.header.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip() == 'Versione 3.57':
                    D.riscrivi_cella(c, 'Versione 3.58')
D.storia(d, DATA, '3.58', 'Atti a Testo Libero · Riferimenti',
         'Il capitolo sugli atti a testo libero rinvia al documento specifico '
         'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.x [R16], che tratta il tema per intero; il '
         'capitolo conserva l’impostazione iniziale. Tolta l’affermazione che le trascrizioni a '
         'testo libero si formino interamente in SIPO.')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE
d.save(OUT)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
