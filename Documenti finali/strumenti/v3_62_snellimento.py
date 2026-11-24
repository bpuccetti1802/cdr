# -*- coding: utf-8 -*-
"""v3.62 dell'analisi ANSC (24/11/2026), dalla v3.61 sul file reale.

Richiesta dell'utente: togliere ciò che riguarda la predisposizione dell'ambiente Kubernetes
(sarà oggetto di un manuale a parte) e rendere più snella l'introduzione.
  - Scopo del documento: da quattro paragrafi a tre, con il rinvio ai documenti di dettaglio
    e al manuale dell'ambiente.
  - Contesto: tolto il «duplice obiettivo» (porting su Kubernetes), asciugati i paragrafi.
  - Glossario: corrette le voci superate (store di stato, registro di emergenza, concentratore
    dei dizionari, riconciliazione), tolta la voce «Regola» (le logiche dichiarative sono
    state deprecate).
  - RNF-5/RNF-6, tabella dei componenti e paragrafo che la introduce: tolti i rimandi al
    capitolo sul deployment, che non esiste più.
  - OP-07 «Piattaforma Kubernetes»: chiuso, trasferito al manuale dell'ambiente.
Le DDL (App. A), le tabelle descrittive e l'ERD restano per la versione successiva.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_62_snellimento.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.61.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.62.docx')
DATA = '24/11/2026'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))
FATTI = []


def trova(inizio):
    t = [p for p in d.paragraphs if p.text.strip().startswith(inizio)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:70]))
    if D.ha_commenti(t[0]._p):
        raise SystemExit('paragrafo commentato: ' + inizio[:60])
    return t[0]


def riscrivi(p, testo):
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)
    p.add_run(testo)


def togli(p):
    if D.ha_commenti(p._p):
        raise SystemExit('paragrafo commentato: ' + p.text[:60])
    p._p.getparent().remove(p._p)


def tab_con(*chiavi):
    ris = []
    for t in d.tables:
        prime = {r.cells[0].text.strip() for r in t.rows}
        if all(k in prime for k in chiavi):
            ris.append(t)
    if len(ris) != 1:
        raise SystemExit('tabella %s: trovate %d' % (chiavi, len(ris)))
    return ris[0]


def riga(t, chiave):
    r = [x for x in t.rows if x.cells[0].text.strip() == chiave]
    if len(r) != 1:
        raise SystemExit('riga %s: trovate %d' % (chiave, len(r)))
    return r[0]


def cella(t, chiave, j, testo):
    D.riscrivi_cella(riga(t, chiave).cells[j], testo)


# ================================================================== 1. Scopo del documento
p1 = trova('Il presente documento fornisce l’analisi tecnico-funzionale')
p2 = trova('L’analisi è propedeutica alla stesura')
p3 = trova('Si ritiene importante sottolineare')
p4 = trova('Il documento riporta le premesse e i requisiti concordati')
riscrivi(p1, 'Il documento contiene l’analisi tecnico-funzionale della nuova componente di SIPO che '
             'consente agli applicativi in esercizio di formare gli atti nell’Archivio Nazionale '
             'dello Stato Civile (ANSC). È la base delle specifiche per lo sviluppo; le scelte di '
             'piattaforma restano ai referenti infrastrutturali del Comune.')
riscrivi(p2, 'Riporta requisiti, vincoli del contratto ANSC, architettura, modello dati, processo di '
             'formazione dell’atto, decisioni architetturali e registro degli open point. I temi '
             'sviluppati in documenti dedicati sono qui riassunti con il rinvio al documento di '
             'dettaglio (Riferimenti [R14]–[R24]). La predisposizione dell’ambiente Kubernetes è '
             'oggetto di un manuale a parte.')
riscrivi(p3, 'Poiché di SIPO non esistono documentazione pregressa né specifiche tecniche, quanto il '
             'documento afferma sul sistema esistente è ricavato dal codice e dalla struttura della '
             'base dati.')
togli(p4)
FATTI.append('Scopo del documento: tre paragrafi, rinvio ai documenti di dettaglio e al manuale K8s')

# ================================================================== 2. Contesto
c1 = trova('Il progetto ha un duplice obiettivo')
c2 = trova('il trasferimento dell’attuale sistema SIPO su ambiente Kubernetes')
c3 = trova('l’aggiunta del supporto alla compilazione degli atti in ANSC')
c4 = trova('La nuova componente ANSC è, di fatto')
c5 = trova('Allo stato attuale SIPO non dispone di alcuna integrazione in scrittura')
c6 = trova('La base dati è Oracle 12.2, collocata all’esterno del cluster')
riscrivi(c1, 'Il progetto aggiunge a SIPO la formazione degli atti in ANSC con il minimo di modifiche '
             'all’esistente. La componente ANSC è l’unica parte disegnata da zero; il resto del '
             'sistema resta com’è, salvo gli adattamenti che l’integrazione richiede.')
togli(c2)
togli(c3)
togli(c4)
riscrivi(c5, 'SIPO non scrive oggi verso ANSC. L’integrazione con ANPR, in SOAP, è un precedente '
             'organizzativo ma non una base di codice riutilizzabile: ANSC espone solo interfacce '
             'REST/JSON.')
riscrivi(c6, 'La base dati è Oracle 12.2, senza un piano di aggiornamento della versione: il vincolo '
             'pesa sul disegno ed è ripreso nelle decisioni architetturali.')
FATTI.append('Contesto: tolto il duplice obiettivo (porting su Kubernetes), da sei paragrafi a tre')

# ================================================================== 3. Glossario
g = tab_con('ANSC', 'SIPO', 'Concentratore')
D.riscrivi_cella(riga(g, 'Store di stato ANSC (ex outbox)').cells[0], 'Store di stato ANSC')
cella(g, 'Store di stato ANSC', 1,
      'Tabella ANSC_STATO_ATTO di ANSC_USR: una riga per atto, con lo stato dell’atto in ANSC '
      '(decodifica ANSC_11), la fase della lavorazione in SIPO e il modello evento inviato.')
cella(g, 'Registro di emergenza', 1,
      'Registro cartaceo previsto dall’ordinamento per l’interruzione del sistema; le operazioni '
      'si riportano in ANSC al ripristino. Unico percorso differito legittimo, di eccezione. La '
      'base normativa è da verificare (OP-49).')
cella(g, 'Concentratore dei dizionari (dec-ansc-sipo)', 1,
      'Componente dedicato al recupero su comando delle decodifiche ANSC (R901) e al loro carico '
      'nelle tabelle DOMINIO_DECODIFICA e VALORE_DOMINIO. Non detiene il certificato server né '
      'costruisce token: raggiunge R901 per il tramite di all-ansc-sipo. Cfr. cap. «Gestione dei '
      'dizionari ANSC» e PC-8.')
cella(g, 'Riconciliazione (R005)', 1,
      'Allineamento fra lo stato in SIPO e lo stato effettivo dell’atto in ANSC (bozza, firmato, '
      'cancellato), letto con R005.')
r = riga(g, 'Regola')
r._tr.getparent().remove(r._tr)
FATTI.append('Glossario: corrette 4 voci superate, tolta la voce «Regola»')

# ================================================================== 4. RNF, componenti, OP-07
rnf = tab_con('RNF-1', 'RNF-5', 'RNF-6')
cella(rnf, 'RNF-5', 2, 'Oracle 12.2, senza piano di aggiornamento.')
cella(rnf, 'RNF-6', 2, 'Kubernetes. La predisposizione dell’ambiente è descritta nel manuale '
                       'dedicato; le scelte di piattaforma restano ai referenti infrastrutturali.')

comp = [t for t in d.tables if t.rows[0].cells[-1].text.strip() == 'Unità di deployment autonoma']
assert len(comp) == 1
comp = comp[0]
for rr in comp.rows[1:]:
    ultima = rr.cells[-1]
    if ultima.text.strip() == 'No — schema Oracle esterno al cluster':
        D.riscrivi_cella(ultima, 'No — schema Oracle ANSC_USR')
    mezzo = rr.cells[1]
    if '(cfr. §5.3)' in mezzo.text:
        D.riscrivi_cella(mezzo, mezzo.text.replace(' che potrebbe essere esterno al pod (cfr. §5.3)',
                                                   ' esterno al componente'))
riscrivi(trova('La tabella elenca i componenti in senso logico'),
         'La tabella elenca i componenti in senso logico: alcuni sono unità di deployment '
         'autonome, altri sono parti interne di un’unità o strutture di base dati, come indica la '
         'colonna di destra.')

op = tab_con('OP-06', 'OP-07')
cella(op, 'OP-07', 2, 'Distribuzione, ingress, politiche di egress, CI/CD, registry: fuori dal '
                      'perimetro dell’analisi, trattati nel manuale dell’ambiente Kubernetes.')
cella(op, 'OP-07', 3, 'Chiuso')
FATTI.append('RNF-5/6, componenti (rimandi a §5.3 e al capitolo sul deployment), OP-07 chiuso')

# ================================================================== 5. testata e storia
for fatto in D.frontespizio(d, '3.62', 'ANALISI_Integrazione-ANSC_v3.62') or []:
    FATTI.append(str(fatto))
for sez in d.sections:
    for t in sez.header.tables:
        for rr in t.rows:
            for c in rr.cells:
                if c.text.strip() == 'Versione 3.61':
                    D.riscrivi_cella(c, 'Versione 3.62')
D.storia(d, DATA, '3.62',
         'Scopo del documento · Glossario · Contesto · Requisiti non funzionali · Componenti · '
         'Open Point',
         'Tolte le parti sulla predisposizione dell’ambiente Kubernetes, oggetto di un manuale a '
         'parte (OP-07 chiuso). Introduzione resa più snella: scopo e contesto riscritti, '
         'glossario ripulito dalle voci superate.')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE
d.save(OUT)
for f in FATTI:
    print('  ' + f)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
