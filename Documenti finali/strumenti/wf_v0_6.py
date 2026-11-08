# -*- coding: utf-8 -*-
"""v0.6 del workflow delle interfacce SIPO-ANSC, dalla v0.5 sul file reale (08/11/2026).

Capitolo «Anteprima · Validazione», sezione «Ipotesi di schermata» e transizioni, secondo le
indicazioni dell'utente sulla pagina (schermate_anteprima_validazione_v2.py):
  - restano testata e testo dell'atto; a destra il modello evento in sezioni ad accordion con
    il loro check e l'esito nella forma della risposta ANSC;
  - all'apertura la pagina valida da sé (R009) con i dati delle pagine precedenti;
  - la forzatura si chiede con un pulsante e una finestra (spunto: Side);
  - la validazione riuscita si annuncia con un messaggio e si passa alla pagina successiva.
Quattro figure al posto della schermata della v0.3; diagramma a stati della pagina
sostituito da diagrammi_pagine_wf.validazione_v6().

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/wf_v0_6.py
"""
import copy
import os
import sys

import docx
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'WORKFLOW_Interfacce-SIPO-ANSC_v0.5.docx')
OUT = os.path.join(BASE, 'WORKFLOW_Interfacce-SIPO-ANSC_v0.6.docx')
IMG = os.path.join(QUI, 'img')
AV = os.path.join(IMG, 'anteprima_validazione', 'v2')
DATA = '08/11/2026'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))
ps = d.paragraphs


def unico(cond, descr):
    t = [p for p in d.paragraphs if cond(p)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), descr))
    return t[0]


capitolo = unico(lambda p: p.style.name == 'Heading 1' and p.text.strip() == 'Anteprima · Validazione',
                 'capitolo')
body = list(d.element.body)
i_cap = body.index(capitolo._p)
didasc = unico(lambda p: p.text.strip() == 'Ipotesi di schermata: Validazione.', 'didascalia')
i_did = D.indice_di(d, didasc)
figura = ps[i_did - 1]
testo = ps[i_did - 2]
assert figura._p.findall('.//' + qn('a:blip')) and 'La pagina mostra' in testo.text

# ------------------------------------------------------------------ testo della sezione
D.testo_di(testo, "La pagina tiene la testata dell’atto e, a sinistra, il testo dell’atto con la "
           "filigrana ANTEPRIMA. A destra mostra il modello evento inviato ad ANSC, diviso nelle "
           "sezioni del mapping dell’UC (per l’UC 2101: formazione atto, dettagli evento, "
           "deceduto, comparente, dati del decesso, atto di nascita del deceduto, formula, "
           "allegati) e presentato ad accordion: ogni sezione porta il numero dei campi e un "
           "check, verde se ANSC non vi segnala nulla, rosso per un errore, arancione per "
           "un’anomalia superabile; aperta, mostra i valori inviati e, sul campo segnalato, il "
           "collegamento CORREGGI NEL DETTAGLIO. Sotto, l’esito nella forma della risposta di "
           "ANSC: idOperazione e forcingCode della testata, poi i messaggi degli elenchi errors, "
           "warnings e infos con code, severity e text.")
nuovi = [
    "All’apertura la pagina non attende un comando: chiama R009 con i dati raccolti nelle "
    "pagine precedenti e, nell’attesa, mostra le sezioni senza check e l’esito «Validazione in "
    "corso»; i pulsanti restano inattivi.",
    "Se ANSC respinge i dati, l’esito elenca gli errori e la sezione interessata si apre sul "
    "campo da correggere. Si torna alle pagine dei dati con CORREGGI NEL DETTAGLIO o TORNA AI "
    "DATI; VALIDA DI NUOVO ripete la chiamata.",
    "Se ANSC restituisce un codice di forzatura si attiva FORZA LA VALIDAZIONE, riservato "
    "all’ufficiale dello stato civile. Il pulsante apre una finestra «Attenzione!» con le "
    "anomalie restituite e il codice: PROSEGUI ACCETTANDO LE ANOMALIE ripete R009 con il "
    "forcingCode e registra la forzatura in forzatura_validazione; TORNA ALLA COMPILAZIONE la "
    "chiude.",
    "Se la validazione riesce, un messaggio lo dice e riporta l’identificativo nazionale e lo "
    "stato 2 CONFERMATO; PROSEGUI porta alla pagina successiva, le firme dei dichiaranti o, "
    "senza firmatari, la conformità.",
    "Due elementi non sono dichiarati dalle fonti ANSC: in quale elenco della risposta e con "
    "quale code arrivino le anomalie superabili, e se il text di un messaggio contenga il "
    "percorso del campo, che serve per accendere il check della sezione giusta. Le figure li "
    "assumono e vanno verificati in preproduzione.",
]
ancora = testo._p
for t in nuovi:
    np_ = copy.deepcopy(testo._p)
    ancora.addnext(np_)
    q = Paragraph(np_, testo._parent)
    D.testo_di(q, t)
    ancora = np_

# ------------------------------------------------------------------ quattro figure
FIG = [
    ('av2_1_caricamento.png', "Ipotesi di schermata: Validazione, all’apertura della pagina."),
    ('av2_2_ko_errori.png', "Ipotesi di schermata: Validazione, dati respinti da ANSC."),
    ('av2_3_forzatura.png', "Ipotesi di schermata: Validazione, finestra della forzatura."),
    ('av2_4_ok.png', "Ipotesi di schermata: Validazione riuscita."),
]
rid = figura._p.findall('.//' + qn('a:blip'))[0].get(qn('r:embed'))
d.part.related_parts[rid]._blob = open(os.path.join(AV, FIG[0][0]), 'rb').read()
ext = figura._p.find('.//' + qn('wp:extent'))
from PIL import Image  # noqa: E402
w0, h0 = Image.open(os.path.join(AV, FIG[0][0])).size
cx = int(ext.get('cx'))
for e in figura._p.iter(qn('wp:extent'), qn('a:ext')):
    e.set('cy', str(int(cx * h0 / w0)))
D.testo_di(didasc, FIG[0][1])
for r in didasc.runs:
    r.italic = True
ancora = didasc._p
for png, cap in FIG[1:]:
    pf = copy.deepcopy(figura._p)
    for r in pf.findall(qn('w:r')):
        pf.remove(r)
    ancora.addnext(pf)
    Paragraph(pf, didasc._parent).add_run().add_picture(os.path.join(AV, png), width=Inches(6.5))
    pc = copy.deepcopy(didasc._p)
    pf.addnext(pc)
    qc = Paragraph(pc, didasc._parent)
    D.testo_di(qc, cap)
    for r in qc.runs:
        r.italic = True
    ancora = pc

# ------------------------------------------------------------------ diagramma a stati
D.sostituisci_immagine(d, 'Validazione: gli stati della pagina.',
                       os.path.join(IMG, 'wf_sd_validazione_v6.png'))

# ------------------------------------------------------------------ transizioni
body = list(d.element.body)
fine = next(p for p in d.paragraphs if p.style.name == 'Heading 1'
            and body.index(p._p) > i_cap)
i_fine = body.index(fine._p)
tt = [t for t in d.tables if i_cap < body.index(t._tbl) < i_fine
      and t.rows[0].cells[1].text.strip() == 'Evento [condizione]']
assert len(tt) == 1
CAMBI = {
    ('Pronta da validare', 'VALIDA'): ('Apertura della pagina', 'R009 automatica all’apertura'),
    ('Da rivalidare', 'VALIDA'): (None, 'R009 automatica all’apertura'),
    ('Respinta', 'VAI ALLA PAGINA o INDIETRO'): (None, 'CORREGGI NEL DETTAGLIO o TORNA AI DATI'),
    ('Forzabile', 'conferma dell’ufficiale e VALIDA CON FORZATURA'):
        (None, 'FORZA LA VALIDAZIONE e, nella finestra, PROSEGUI ACCETTANDO LE ANOMALIE '
               '(solo l’ufficiale dello stato civile)'),
    ('Forzabile', 'INDIETRO'): (None, 'TORNA ALLA COMPILAZIONE, poi CORREGGI NEL DETTAGLIO o '
                                      'TORNA AI DATI'),
    ('Validata', 'INDIETRO e modifica dei dati'): (None, 'TORNA AI DATI e modifica dei dati'),
    ('Validata', 'AVANTI [ci sono firmatari]'): (None, 'PROSEGUI nel messaggio di esito [ci sono '
                                                       'firmatari]'),
    ('Validata', 'AVANTI [nessun firmatario]'): (None, 'PROSEGUI nel messaggio di esito '
                                                       '[nessun firmatario]'),
}
fatti = 0
for r in tt[0].rows[1:]:
    da, ev = r.cells[0].text.strip(), r.cells[1].text.strip()
    if (da, ev) in CAMBI:
        nda, nev = CAMBI[(da, ev)]
        if nda:
            D.riscrivi_cella(r.cells[0], nda)
        D.riscrivi_cella(r.cells[1], nev)
        fatti += 1
    if r.cells[2].text.strip() == 'Pronta da validare':
        D.riscrivi_cella(r.cells[2], 'Apertura della pagina')
    if 'Errori nella tabella dell’esito' in r.cells[3].text:
        D.riscrivi_cella(r.cells[3], 'Errori nell’esito, nella forma della risposta ANSC; la '
                                     'sezione del modello evento interessata si apre sul campo.')
    if r.cells[3].text.strip().startswith('R009 con forcingCode'):
        D.riscrivi_cella(r.cells[3], 'R009 con forcingCode; a esito positivo la forzatura si '
                                     'registra in forzatura_validazione (WF-15).')
assert fatti == len(CAMBI), fatti

# ------------------------------------------------------------------ frontespizio e storia
D.storia(d, DATA, '0.6', 'Anteprima · Validazione',
         'Nuova ipotesi della pagina: testo dell’atto a sinistra, modello evento ad accordion '
         'con i check e esito nella forma della risposta ANSC a destra; validazione automatica '
         'all’apertura, forzatura con pulsante e finestra, messaggio di validazione riuscita. '
         'Quattro schermate, diagramma a stati e transizioni aggiornati.')
for fatto in D.frontespizio(d, '0.6', 'WORKFLOW_Interfacce-SIPO-ANSC_v0.6', DATA) or []:
    print('  ' + str(fatto))

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE
d.save(OUT)
print('scritto', os.path.relpath(OUT, os.path.dirname(BASE)), '· ancore di commento', ANCORE)
