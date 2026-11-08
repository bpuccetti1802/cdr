# -*- coding: utf-8 -*-
"""v3.60 dell'analisi ANSC (08/11/2026), dalla v3.59 sul file reale.

Richiesta dell'utente: allineare al disegno della pagina «Anteprima · Validazione» (WORKFLOW
v0.6, [R17]) i punti che lo contraddicevano:
  - § «Il passo «VALIDA»», primo paragrafo: non una pagina finale di solo salvataggio da cui
    non si torna indietro, ma la pagina che valida all'apertura; ritorno ai dati fino alla
    firma dell'ufficiale, come in «Le quattro fasi» → OP-77 chiuso;
  - la nota sulla forzatura e il § «Il codice di forzatura»: non più «prima che ANSC risponda»
    né «in una prossima release», ma ANSC restituisce il forcingCode con le anomalie e
    l'ufficiale ripete R009 con il codice (contratto R009: forcingCode in richiesta e risposta;
    forzatura_validazione.cd_forzatura «generato da ANSC»);
  - OP-21 riformulato di conseguenza.
Nessuno dei paragrafi toccati porta ancore di commento.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_60_allinea_validazione.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.59.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.60.docx')
DATA = '08/11/2026'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))


def trova(inizio):
    t = [p for p in d.paragraphs if p.text.strip().startswith(inizio)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:60]))
    if D.ha_commenti(t[0]._p):
        raise SystemExit('paragrafo commentato: ' + inizio[:60])
    return t[0]


def riscrivi(p, pezzi):
    """pezzi: lista di (testo, grassetto)."""
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)
    for t, b in pezzi:
        r = p.add_run(t)
        if b:
            r.bold = True


# ------------------------------------------------------------------ il passo VALIDA
riscrivi(trova('Nella maschera SIPO, finita la parte di validazione'), [(
    "Nella maschera SIPO, finita la parte di validazione, l’operatore preme «VALIDA» nella "
    "pagina di Anteprima. Si apre la pagina «Anteprima · Validazione», che chiama R009 da sé con "
    "i dati raccolti nelle pagine precedenti. Se la validazione riesce, l’atto è depositato in "
    "ANSC nello stato 2 CONFERMATO, il suo identificativo nazionale si salva su SIPO e un "
    "messaggio porta alle firme. Fino alla firma dell’ufficiale dello stato civile si può ancora "
    "tornare ai dati: l’atto passa allo stato 0 e si valida di nuovo lo stesso atto, con lo "
    "stesso identificativo nazionale; dopo le firme dei dichiaranti, solo se tutti possono "
    "firmare di nuovo (sezione «Le quattro fasi»).", False)])

riscrivi(trova('Nota. Nelle prossime release del documento sarà introdotta'), [
    ("La forzatura. ", True),
    ("La forzatura della validazione è riservata all’ufficiale dello stato civile. Quando ANSC "
     "risponde con anomalie superabili, restituisce anche un codice di forzatura (forcingCode) e "
     "la pagina attiva il pulsante «FORZA LA VALIDAZIONE», che apre una finestra con le anomalie "
     "e il codice. Confermando, R009 si ripete con il codice di forzatura; a operazione avvenuta "
     "il codice si registra in forzatura_validazione con le anomalie superate e il nome o altro "
     "identificativo dell’ufficiale (si veda «Il codice di forzatura», OP-21).", False)])

# ------------------------------------------------------------------ il codice di forzatura
riscrivi(trova('La forzatura si chiede prima che ANSC risponda'), [(
    "La forzatura è un secondo passaggio della validazione. Alla prima chiamata R009 ANSC "
    "segnala le anomalie superabili e restituisce il codice di forzatura; se l’ufficiale dello "
    "stato civile decide di forzare, la richiesta R009 si ripete portando quel codice. A "
    "operazione avvenuta il codice si registra nella tabella forzatura_validazione, ereditata da "
    "Side, con le anomalie superate e il nome o altro identificativo dell’ufficiale che ha "
    "forzato. Le forzature possono essere effettuate soltanto dall’ufficiale dello stato civile: "
    "la funzione è riservata al suo profilo. Nella pagina «Anteprima · Validazione» si chiede con "
    "il pulsante «FORZA LA VALIDAZIONE» e una finestra di conferma delle anomalie [R17].", False)])

# ------------------------------------------------------------------ OP-21 e OP-77
op = [t for t in d.tables if [c.text.strip() for c in t.rows[0].cells][:4] ==
      ['#', 'Tema', 'Questione', 'Stato']
      and {'OP-21', 'OP-77'} <= {r.cells[0].text.strip() for r in t.rows}]
assert len(op) == 1
righe = {r.cells[0].text.strip(): r for r in op[0].rows}
D.riscrivi_cella(righe['OP-21'].cells[2],
                 "Chiuso. La forzatura è riservata all’ufficiale dello stato civile: ANSC "
                 "restituisce il codice di forzatura con le anomalie superabili, l’ufficiale "
                 "decide di forzare dalla pagina «Anteprima · Validazione» e R009 si ripete con il "
                 "codice; a operazione avvenuta il codice si registra in forzatura_validazione con "
                 "il nome o altro identificativo dell’ufficiale. Resta aperto OP-41 sul flusso di "
                 "conferma degli atti anomali.")
D.riscrivi_cella(righe['OP-77'].cells[2],
                 "Chiuso. Il paragrafo sul passo «VALIDA» è riallineato alla sezione «Le quattro "
                 "fasi»: la validazione riuscita porta alle firme e, fino alla firma "
                 "dell’ufficiale, si può tornare ai dati con lo stato 0 e una nuova validazione "
                 "dello stesso atto; dopo le firme dei dichiaranti solo se tutti possono firmare di "
                 "nuovo.")
D.riscrivi_cella(righe['OP-77'].cells[3], 'Chiuso')

# ------------------------------------------------------------------ testata e storia
for fatto in D.frontespizio(d, '3.60', 'ANALISI_Integrazione-ANSC_v3.60') or []:
    print('  ' + str(fatto))
for sez in d.sections:
    for t in sez.header.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip() == 'Versione 3.59':
                    D.riscrivi_cella(c, 'Versione 3.60')
D.storia(d, DATA, '3.60', 'Il passo «VALIDA» · Il codice di forzatura · Open Point',
         'Allineati alla pagina «Anteprima · Validazione» [R17] il paragrafo sul passo «VALIDA» '
         '(la pagina valida all’apertura, si torna ai dati fino alla firma dell’ufficiale) e la '
         'forzatura (ANSC restituisce il codice con le anomalie, l’ufficiale ripete R009 con il '
         'codice). OP-21 riformulato, OP-77 chiuso.')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE
d.save(OUT)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
