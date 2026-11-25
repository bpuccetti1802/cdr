# -*- coding: utf-8 -*-
"""v3.64 dell'analisi ANSC (24/11/2026), dalla v3.63 sul file reale (salvata dall'utente in Word
alle 17:59, con tre ritocchi propri nel cap. «Adeguamenti database»).

Verifica di coerenza del capitolo «Adeguamenti database» con gli script della base dati di
collaudo [R25]: colonne, tipi, chiavi e valori ammessi tornano; il testo no, in sei punti.
  1. numero comunale: gli script aggiungono MATR_USR.ATTO.NUM_COMUNALE_ANSC (nota di NUMERO_ATTO,
     tabella «Dato | Dove risiede», OP-60);
  2. estensioni: la FK verso ATTO manca su ATTO_NASCITA_EXTEND2, ATTO_UNIONE_EXTEND2, ATTO_DELEGA;
  3. redattoNellaCasaComunale: 0/1, non S/N;
  4. nota di ID_USECASE: niente formule né interrogazioni, la baseline solo su allegati e soggetti;
  5. riga ANSC_CFG_UC dell'elenco: rinvio a un capitolo che non c'è più; riga «Famiglia ANSC_CFG_*»;
  6. riga dei dizionari: V_ANSC_DIZ_VALIDO non è negli script (OP-105).
Inoltre: OP-102 (j)(k)(l), nota sulla baseline di ALLEGATI_/SOGGETTI_USECASE (OP-103),
volume del modello evento 8-30 KB in entrambi i paragrafi.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_64_coerenza_cap5.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.63.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.64.docx')
DATA = '24/11/2026'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))
FATTI = []


def sost(vecchio, nuovo, attese=1):
    D.sostituisci(d, vecchio, nuovo, attese=attese, fatti=FATTI)


def cella(prima, colonna, contiene=None):
    """La cella `colonna` della riga, unica, la cui prima cella vale `prima`."""
    ris = []
    for t in d.tables:
        for r in t.rows:
            if r.cells[0].text.strip() == prima and (
                    contiene is None or contiene in r.cells[colonna].text):
                c = r.cells[colonna]
                if all(c._tc is not x._tc for x in ris):
                    ris.append(c)
    if len(ris) != 1:
        raise SystemExit('riga %s: %d' % (prima, len(ris)))
    return ris[0]


def riscrivi(c, testo, etichetta):
    D.riscrivi_cella(c, testo)
    FATTI.append(etichetta)


# ------------------------------------------------------------ 1. numero comunale
sost('Sull’atto di stato civile di SIPO non esiste una colonna dedicata: se aggiungerla lì '
     'resta da decidere (OP-60).',
     'Gli script aggiungono anche, sull’atto di stato civile, la colonna '
     'MATR_USR.ATTO.NUM_COMUNALE_ANSC (si veda «Le estensioni delle tabelle di SIPO»): il numero '
     'ha così due sedi sull’atto, che devono coincidere. Chi scriva la seconda e in quale momento '
     'è OP-60.')
riscrivi(cella('Numero comunale dell’atto', 1),
         'ANSC_STATO_ATTO.NUMERO_ATTO e, sull’atto di stato civile di SIPO, la colonna '
         'MATR_USR.ATTO.NUM_COMUNALE_ANSC che gli script aggiungono. MATR_USR.ATTO porta inoltre '
         'NUMERO_ATTO con parte e serie, mentre NUMERO_COMUNALE esiste sull’ATTO di anagrafe '
         '(ANAG_USR), dove però è valorizzata scomponendo l’identificativo ANSC di un atto '
         'formato altrove.',
         'tabella «Dato | Dove risiede»: numero comunale')
riscrivi(cella('OP-60', 2),
         'Gli script della base dati [R25] aggiungono MATR_USR.ATTO.NUM_COMUNALE_ANSC, '
         'VARCHAR2(6): il numero comunale ha ora tre sedi — DATI_ATTO_ESTERNO per la serie, '
         'ANSC_STATO_ATTO.NUMERO_ATTO e la colonna sull’atto di stato civile, perché le maschere '
         'e le stampe di SIPO lo mostrino. Resta da stabilire quale delle due sull’atto faccia '
         'fede, chi scriva la colonna di SIPO e in quale momento (allo stacco, alla validazione, '
         'alla definizione). Da chiudere insieme a OP-29.',
         'OP-60 riformulato')

# ------------------------------------------------------------ 2. estensioni e FK verso ATTO
sost('(chiave ID_ATTO, che è anche chiave esterna verso ATTO)',
     '(chiave ID_ATTO; la chiave esterna verso ATTO è dichiarata per decessi, matrimonio, '
     'cittadinanza e divorzio, non per nascita, unione civile e ATTO_DELEGA: OP-102)')

# ------------------------------------------------------------ 3. casa comunale
riscrivi(cella('21', 4, 'S/N'),
         '0/1, come il vincolo della colonna; il contratto lo dichiara booleano.',
         'testata, riga 21: 0/1')

# ------------------------------------------------------------ 4. nota di ID_USECASE
sost('Insieme a ID_VERSIONE è il riferimento con cui campi, formule, allegati, soggetti e '
     'interrogazioni richiamano l’UC, per valore.',
     'È il riferimento con cui campi, allegati e soggetti richiamano l’UC, per valore; allegati '
     'e soggetti vi affiancano la baseline (ID_VERSIONE), che ANSC_CFG_CAMPO negli script non '
     'porta (OP-103).')

# ------------------------------------------------------------ 5. righe ANSC_CFG dell'elenco
riscrivi(cella('Famiglia ANSC_CFG_*', 1),
         'Configurazione degli UC e dei campi (pre-filtro RF-9).',
         'elenco: ruolo della famiglia ANSC_CFG_*')
c = cella('Famiglia ANSC_CFG_*', 2)
riscrivi(c,
         'ANSC_CFG_CAMPO e ANSC_CFG_TEMPLATE, con ANSC_CFG_UC e ANSC_CFG_VERSIONE che hanno una '
         'riga propria: i metadati che, per caso d’uso, guidano la selezione dell’UC, la '
         'provenienza dei dati e l’obbligatorietà. Descrizione al paragrafo «Struttura '
         'dettagliata delle tabelle di configurazione», struttura negli script [R25].',
         'elenco: note della famiglia ANSC_CFG_*')
c = cella('ANSC_CFG_UC — gli UC e la loro scelta', 1)
riscrivi(c, 'Catalogo degli UC dichiarati da ANSC e configurazione con cui il Comune li adotta '
            '(RF-11).', 'elenco: ruolo di ANSC_CFG_UC')
sost('Struttura al capitolo «La determinazione dell’UC e le regole di controllo».',
     'Descrizione al paragrafo «ANSC_CFG_UC — il catalogo degli UC e le regole di '
     'identificazione», uso al paragrafo «La determinazione dell’UC».')

# ------------------------------------------------------------ 6. dizionari
sost('più la vista di fruizione V_ANSC_DIZ_VALIDO.',
     'più la vista di fruizione V_ANSC_DIZ_VALIDO, prevista e non ancora negli script (OP-105).')
sost('Struttura al cap. «Gestione dei dizionari ANSC», struttura negli script [R25]',
     'Descrizione al cap. «Gestione dei dizionari ANSC», struttura negli script [R25]')

# ------------------------------------------------------------ baseline di allegati e soggetti
for nome in ('ALLEGATI_USECASE', 'SOGGETTI_USECASE'):
    c = cella(nome, 2, 'baseline')
    riscrivi(c, c.text.strip() + ' Negli script la baseline è nella chiave; le variazioni '
                'annunciate dagli sviluppatori la tolgono (OP-103).',
             'elenco: %s e la baseline' % nome)

# ------------------------------------------------------------ OP-102
c = cella('OP-102', 2)
if '(j)' in c.text:
    raise SystemExit('OP-102 già esteso')
riscrivi(c, c.text.strip() +
         ' (j) ATTO_NASCITA_EXTEND2, ATTO_UNIONE_EXTEND2 e ATTO_DELEGA non dichiarano la chiave '
         'esterna verso ATTO, che le altre estensioni hanno. (k) Il commento della tabella '
         'ANSC_SOGGETTO_IDENTIFICATIVI dice che i codici ANPR stanno su ANAG_USR.SOGGETTO, mentre '
         'la tabella stessa li porta in colonna. (l) ATTO_TESTO_FORMULATO chiama DATA_INS e '
         'DATA_UPD due colonne TIMESTAMP, contro la convenzione dichiarata nel capitolo '
         '«Adeguamenti database» (DATA_ per DATE, TS_ per TIMESTAMP).',
         'OP-102: punti (j), (k), (l)')

# ------------------------------------------------------------ volume del modello evento
sost('una dimensione media fra dieci e trenta kilobyte',
     'una dimensione media fra otto e trenta kilobyte')

# ------------------------------------------------------------ testata e storia
for fatto in D.frontespizio(d, '3.64', 'ANALISI_Integrazione-ANSC_v3.64') or []:
    FATTI.append(str(fatto))
for sez in d.sections:
    for tb in sez.header.tables:
        for rr in tb.rows:
            for cc in rr.cells:
                if cc.text.strip() == 'Versione 3.63':
                    D.riscrivi_cella(cc, 'Versione 3.64')
D.storia(d, DATA, '3.64',
         'Adeguamenti database · Il processo di gestione dei dati ANSC in SIPO · Open Point',
         'Verifica del capitolo «Adeguamenti database» sugli script [R25]: colonne e tipi '
         'coerenti; corretti nel testo il numero comunale sull’atto di SIPO '
         '(MATR_USR.ATTO.NUM_COMUNALE_ANSC, OP-60 riformulato), le chiavi esterne delle '
         'estensioni, redattoNellaCasaComunale 0/1, la nota di ID_USECASE, le righe di '
         'configurazione e dizionari dell’elenco delle tabelle. OP-102 esteso.')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE, 'ancore perse'
d.save(OUT)
for f in FATTI:
    print('  ' + f)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
