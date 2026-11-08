# -*- coding: utf-8 -*-
"""v3.59 dell'analisi ANSC (08/11/2026), dalla v3.58 sul file reale. Interventi solo additivi.

Richiesta dell'utente: riportare in forma semplificata la pagina «Anteprima · Validazione»
descritta nel WORKFLOW v0.6. Nella sezione «Il passo «VALIDA»: interazione UX e ruolo del
back-end», dopo la nota sulla forzatura: un paragrafo con il comportamento della pagina, una
figura (dati respinti da ANSC) e il rinvio al WORKFLOW, citato come [R17].

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_59_anteprima_validazione.py
"""
import copy
import os
import sys

import docx
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.58.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.59.docx')
PNG = os.path.join(QUI, 'img', 'anteprima_validazione', 'v2', 'av2_2_ko_errori.png')
DATA = '08/11/2026'
DOC = 'WORKFLOW_Interfacce-SIPO-ANSC_v0.x.docx'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))


def trova(cond, descr):
    t = [p for p in d.paragraphs if cond(p)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), descr))
    return t[0]


nota = trova(lambda p: p.text.strip().startswith('Nota. Nelle prossime release del documento sarà '
                                                 'introdotta nel passo «VALIDA»'), 'nota forzatura')
modello_did = trova(lambda p: p.text.strip().startswith('Il flusso operativo nelle sue quattro fasi'),
                    'didascalia modello')
modello_fig = d.paragraphs[D.indice_di(d, modello_did) - 1]
assert modello_fig._p.findall('.//' + qn('a:blip'))


def paragrafo_dopo(ancora_p, modello_p, testo):
    np_ = copy.deepcopy(modello_p._p)
    for r in list(np_):
        if r.tag != qn('w:pPr'):
            np_.remove(r)
    ancora_p.addnext(np_)
    q = Paragraph(np_, nota._parent)
    if testo:
        q.add_run(testo)
    return q


testi = [
    "La pagina «Anteprima · Validazione». All’apertura la pagina chiama R009 da sé, con i dati "
    "raccolti nelle pagine precedenti. Mostra il testo dell’atto e, accanto, il modello evento "
    "inviato, diviso nelle sezioni dell’UC con un check per ciascuna, e l’esito nella forma della "
    "risposta di ANSC (errori, avvisi, codice di forzatura). Se ANSC respinge i dati, la sezione "
    "interessata si apre sul campo da correggere e si torna alle pagine dei dati. Se ANSC "
    "restituisce un codice di forzatura, l’ufficiale dello stato civile può forzare con un "
    "pulsante che apre una finestra di conferma delle anomalie. Se la validazione riesce, un "
    "messaggio lo dice e si passa alle firme. Il dettaglio — schermate, stati e transizioni della "
    "pagina — è nel documento " + DOC + " [R17].",
]
p1 = paragrafo_dopo(nota._p, nota, None)
r = p1.add_run('La pagina «Anteprima · Validazione». ')
r.bold = True
p1.add_run(testi[0][len('La pagina «Anteprima · Validazione». '):])
pf = paragrafo_dopo(p1._p, modello_fig, None)
pf.add_run().add_picture(PNG, width=Inches(6.0))
pc = paragrafo_dopo(pf._p, modello_did, None)
rc = pc.add_run("Ipotesi della pagina «Anteprima · Validazione» con dati respinti da ANSC: testo "
                "dell’atto, modello evento per sezioni con il loro check, esito della risposta "
                "ANSC [R17].")
rc.italic = True

# ------------------------------------------------------------------ [R17]
rif = [t for t in d.tables if any(r.cells[0].text.strip() == 'R16' for r in t.rows)]
assert len(rif) == 1
D.clona_riga(rif[0], ('R17', DOC + ' (versione corrente: v0.6)',
                      'Le interfacce del workflow SIPO-ANSC pagina per pagina: pagine, servizi '
                      'ANSC chiamati, tabelle, stati e transizioni, ipotesi di schermata e '
                      'diagrammi a stati delle pagine nuove, fra cui «Anteprima · Validazione».'))

# ------------------------------------------------------------------ testata e storia
for fatto in D.frontespizio(d, '3.59', 'ANALISI_Integrazione-ANSC_v3.59') or []:
    print('  ' + str(fatto))
for sez in d.sections:
    for t in sez.header.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip() == 'Versione 3.58':
                    D.riscrivi_cella(c, 'Versione 3.59')
D.storia(d, DATA, '3.59', 'Il passo «VALIDA» · Riferimenti',
         'Descritta in forma sintetica la pagina «Anteprima · Validazione»: validazione '
         'automatica all’apertura, modello evento per sezioni con il loro check, esito nella '
         'forma della risposta ANSC, forzatura con finestra, messaggio di validazione riuscita; '
         'una figura e il rinvio al documento WORKFLOW [R17].')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE
d.save(OUT)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
