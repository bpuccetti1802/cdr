# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.7 (21/11/2026), dal FILE REALE della v0.6 salvato
dall'utente alle 11:35 («Sul DB ci dovrà essere una riga per gemello…», paragrafo sul costo del
caso 2): non rieseguire gemellari_v0_6.py.

Decisione dell'utente (21/11/2026, «strada 1»): ATTI_GEMELLARI, la tabella di Side, NON si crea.
ANSC_SOGGETTO_ATTO riceve la chiave del parto ID_LAVORAZIONE_PADRE (FK verso la riga dello store
del gemello 1, UK con il progressivo) e diventa l'unica tabella dei gemelli; il resto delle
colonne di Side va dove già sta (audit, stato dello store) o si calcola. Adattamento dichiarato
nella tabella delle scelte di Side.
Figure: diagrammi_gemellari_v0_7_pptx.py (gem7_erd, gem7_panoramica, gem7_flusso_2, gem7_ripresa).

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_7.py
"""
import os
import re
import sys

import docx
from docx.oxml.ns import qn

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import voce                              # noqa: E402
from gemellari_v0_2 import codice, para_che_inizia, tabella_che_contiene   # noqa: E402
from gemellari_v0_4 import (didascalia, rifai_voce, riga_di,      # noqa: E402
                            sostituisci_figura)
from gemellari_v0_5 import inserisci_prima                         # noqa: E402

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.6.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.7.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '21/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')


def png(nome):
    return os.path.join(IMG, nome)


def togli_da_a(primo, ultimo):
    """Toglie gli elementi del corpo da `primo` a `ultimo` compresi."""
    e, via = primo, []
    while True:
        via.append(e)
        if e is ultimo:
            break
        e = e.getnext()
        assert e is not None, 'fine del corpo prima di ultimo'
    for x in via:
        assert not D.ha_commenti(x)
        x.getparent().remove(x)
    return len(via)


def cella(t, primo, col, testo):
    D.riscrivi_cella(riga_di(t, primo).cells[col], testo)


DDL = [
    'CREATE TABLE ANSC_USR.ANSC_SOGGETTO_ATTO (',
    '  ID_SOGGETTO_ATTO         NUMBER GENERATED ALWAYS AS IDENTITY,',
    '  ID_ATTO_SIPO             NUMBER            NOT NULL,',
    '  ID_ANSC                  VARCHAR2(50 CHAR),',
    '  ID_UC_ANSC               VARCHAR2(20 CHAR),',
    '  ID_NASCITA_SOGGETTO      NUMBER,',
    '  ID_SOGGETTO              NUMBER,',
    '  COD_RUOLO                VARCHAR2(20 CHAR) NOT NULL,',
    '  ID_ANSC_SOGGETTO         VARCHAR2(50 CHAR),',
    '  ID_LAVORAZIONE_PADRE     NUMBER,',
    '  NUM_PROGRESSIVO_GEMELLO  NUMBER(2),',
    '  ID_TIPO_NASCITA          VARCHAR2(10 CHAR),',
    '  ID_ANSC_GEMELLO_PREC     VARCHAR2(50 CHAR),',
    '  ID_ANSC_GEMELLO_SUCC     VARCHAR2(50 CHAR),',
    '  COD_ORIGINE              VARCHAR2(20 CHAR) NOT NULL,',
    '  TS_ABBINAMENTO           TIMESTAMP         NOT NULL,',
    '  TS_INS                   TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  TS_UPD                   TIMESTAMP,',
    '  UTENTE_INS               VARCHAR2(40 CHAR) NOT NULL,',
    '  UTENTE_UPD               VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_ANSC_SOGGETTO_ATTO PRIMARY KEY (ID_SOGGETTO_ATTO),',
    '  CONSTRAINT UK_ANSC_SOGG_ATTO_RUOLO UNIQUE (ID_ATTO_SIPO, COD_RUOLO),',
    '  CONSTRAINT UK_ANSC_SOGG_ATTO_PARTO',
    '    UNIQUE (ID_LAVORAZIONE_PADRE, NUM_PROGRESSIVO_GEMELLO),',
    '  CONSTRAINT FK_ANSC_SOGG_ATTO_STATO FOREIGN KEY (ID_ATTO_SIPO)',
    '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
    '  CONSTRAINT FK_ANSC_SOGG_ATTO_PARTO FOREIGN KEY (ID_LAVORAZIONE_PADRE)',
    '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_RIF',
    '    CHECK (ID_NASCITA_SOGGETTO IS NOT NULL OR ID_SOGGETTO IS NOT NULL),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_ORIG',
    "    CHECK (COD_ORIGINE IN ('PRENOTAZIONE','RECUPERO','VALIDAZIONE')),",
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_PROG',
    '    CHECK (NUM_PROGRESSIVO_GEMELLO BETWEEN 1 AND 10),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_GEM',
    '    CHECK ((ID_LAVORAZIONE_PADRE IS NULL AND NUM_PROGRESSIVO_GEMELLO IS NULL',
    '            AND ID_ANSC_GEMELLO_PREC IS NULL AND ID_ANSC_GEMELLO_SUCC IS NULL)',
    '        OR (ID_LAVORAZIONE_PADRE IS NOT NULL AND NUM_PROGRESSIVO_GEMELLO IS NOT NULL))',
    ');',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_NASC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_NASCITA_SOGGETTO);',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_SOGG ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_SOGGETTO);',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_ANSC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_ANSC);',
]

SQL = [
    'SELECT g.NUM_PROGRESSIVO_GEMELLO, g.ID_TIPO_NASCITA, s.ID_ATTO_SIPO, s.ID_UC_ANSC,',
    '       s.NUMERO_ATTO, s.ID_ANSC, s.ID_STATO, s.STATO, s.COD_FASE,',
    '       g.ID_ANSC_GEMELLO_PREC, g.ID_ANSC_GEMELLO_SUCC',
    '  FROM ANSC_USR.ANSC_SOGGETTO_ATTO g',
    '  JOIN ANSC_USR.ANSC_STATO_ATTO s ON s.ID_ATTO_SIPO = g.ID_ATTO_SIPO',
    " WHERE g.COD_RUOLO = 'INTESTATARIO'",
    '   AND g.ID_LAVORAZIONE_PADRE = (SELECT x.ID_LAVORAZIONE_PADRE',
    '                                   FROM ANSC_USR.ANSC_SOGGETTO_ATTO x',
    '                                  WHERE x.ID_ATTO_SIPO = :idAtto',
    "                                    AND x.COD_RUOLO = 'INTESTATARIO')",
    ' ORDER BY g.NUM_PROGRESSIVO_GEMELLO;',
]

SIDE_INTRO = (
    'Side [M1] tiene insieme i gemelli di un parto con una tabella propria, atti_gemellari: una '
    'riga per gemello con l’atto, la richiesta di prenotazione, l’UC, il numero dei gemelli, la '
    'posizione e lo stato della stesura. A Roma questa tabella non si crea. Le stesse informazioni '
    'stanno in ANSC_SOGGETTO_ATTO, descritta più avanti, che lega il nato al suo atto ANSC e riceve '
    'la chiave del parto: tenerle entrambe avrebbe dato due tabelle con gli stessi dati per riga, '
    'da tenere allineate. La tabella che segue dichiara gli adattamenti a Side, compreso dove '
    'finisce ciascuna colonna della tabella di Milano.')

# righe nuove della tabella «Scelta di Side | Per Roma | Ragione», in testa
SCELTE_NUOVE = [
    ['Tabella atti_gemellari.', 'Non si crea: le colonne confluiscono in ANSC_SOGGETTO_ATTO o '
     'vanno dove il dato già sta.', 'Avrebbe ripetuto per ogni gemello atto, posizione e UC già '
     'presenti in ANSC_SOGGETTO_ATTO, che il Comune ha scelto come tabella unica da cui leggere il '
     'nato, il suo atto e i suoi fratelli.'],
    ['Colonne id_richiesta_prenotazione, cd_operatore, ts_operazione.', 'ANSC_LOG_AUDIT (fase '
     'PRENOTAZIONE) e i campi tecnici di ANSC_SOGGETTO_ATTO.', 'La prenotazione è una chiamata '
     'sola per il parto e si registra nell’audit, sulla riga del gemello 1.'],
    ['Colonne ty_use_case, nr_progressivo_gemello.', 'ANSC_SOGGETTO_ATTO.ID_UC_ANSC e '
     'NUM_PROGRESSIVO_GEMELLO.', 'Con i nomi dello standard [R5], come il resto della tabella.'],
    ['Colonna nr_gemelli.', 'Non si registra.', 'È il numero delle righe del parto; SIPO lo ha in '
     'ATTO_NASCITA.N_TOT_GEMELLI.'],
    ['Colonna fg_stesura_atto.', 'Non si registra.', 'Lo dice lo stato dell’atto nello store: 5 '
     'FIRMATO DA USC.'],
]

TABELLA_SA = (
    'La tabella nuova sta in ANSC_USR, accanto allo store. Lega un soggetto all’atto ANSC di cui è '
    'intestatario e vale per qualunque atto; nel parto plurimo raggruppa anche i gemelli, al posto '
    'della tabella di Side. Registra il soggetto con il riferimento disponibile quando '
    'l’abbinamento avviene e lo completa dopo; porta l’identificativo e l’UC dell’atto e, nel parto '
    'plurimo, la chiave del parto e i dati del gemello, così che il nato, il suo atto e i suoi '
    'fratelli si leggano da una riga.')

COPIE = (
    'Le copie dallo store.', 'ID_ANSC e ID_UC_ANSC ripetono i valori di ANSC_STATO_ATTO, così '
    'che il nato, il suo atto e i suoi fratelli si leggano da una sola tabella. Una copia può '
    'divergere, quindi vale una regola: le scrive solo il concentratore, nella stessa transazione '
    'in cui aggiorna lo store (prenotazione, validazione, recupero, ripresa), e la ripresa del '
    'parto le confronta con lo store e con ANSC. Il caso da presidiare è la validazione che '
    'restituisce un identificativo diverso da quello prenotato (GE-02): cambiano lo store, la riga '
    'del gemello e i riferimenti dei due fratelli adiacenti.')
GEMELLI = (
    'I dati del gemello.', 'ID_LAVORAZIONE_PADRE, NUM_PROGRESSIVO_GEMELLO, ID_TIPO_NASCITA e i due '
    'riferimenti adiacenti si valorizzano solo nel parto plurimo; fuori restano vuoti. La chiave '
    'del parto è l’ID_ATTO del gemello 1 ed è chiave esterna verso la sua riga dello store, che '
    'esiste dalla fase dei dati; il vincolo di unicità su parto e posizione impedisce due gemelli '
    'nella stessa posizione, e un vincolo impedisce la posizione senza il parto e i riferimenti ai '
    'fratelli senza la posizione. Nel caso 1 si scrive tutto alla prenotazione, quando gli '
    'identificativi arrivano insieme; nel caso 2 al recupero, e fino ad allora il parto si '
    'riconosce in SIPO da ATTO.ID_LAVORAZIONE_PADRE. Un riferimento è l’identificativo ANSC del '
    'solo gemello adiacente: le liste dei fratelli si ottengono seguendo la catena.')

LEGAME = (
    'ANSC_STATO_ATTO non porta alcuna colonna del parto, e non deve portarne: la riga descrive un '
    'atto, e quasi tutti gli atti non sono gemellari. Il legame sta in ANSC_SOGGETTO_ATTO, che ha '
    'una riga per gemello (il nato intestatario) e la collega alla riga dello store del proprio '
    'atto e a quella del gemello 1, che rappresenta il parto, con due chiavi esterne: le tabelle '
    'stanno nello stesso schema, quindi i vincoli si possono dichiarare. Verso SIPO i legami '
    'restano per valore, come in tutto ANSC_USR.')


def main():
    d = docx.Document(IN)
    fatti = []
    storia_t = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')

    # 1. In sintesi (testo dell'utente: si cambia la sola frase sulla tabella)
    D.sostituisci(d, 'ATTI_GEMELLARI le raggruppa per pratica e lega ciascuna alla propria riga '
                  'dello store; gli elenchi dei fratelli si calcolano, non si registrano.',
                  'ANSC_SOGGETTO_ATTO le raggruppa per parto, con posizione, tipo di nascita e '
                  'gemelli adiacenti di ciascun nato.', attese=1, fatti=fatti)

    # 2. caso 1 e ripresa
    t = tabella_che_contiene(d, 'DEFINISCI: numeri e prenotazione')
    c = riga_di(t, '4').cells[4]
    D.riscrivi_cella(c, c.text.replace('righe in ATTI_GEMELLARI e in ANSC_SOGGETTO_ATTO',
                                       'righe in ANSC_SOGGETTO_ATTO'))
    D.sostituisci(d, '(ATTI_GEMELLARI e ANSC_STATO_ATTO,', '(ANSC_SOGGETTO_ATTO e '
                  'ANSC_STATO_ATTO,', attese=1, fatti=fatti)

    # 3. caso 2: allo stacco nessuna riga della tabella dei gemelli
    t = tabella_che_contiene(d, 'SIPO, DATI PER ANSC')
    c = riga_di(t, '3').cells[2]
    assert '; N righe in ATTI_GEMELLARI.' in c.text
    D.riscrivi_cella(c, c.text.replace('; N righe in ATTI_GEMELLARI.', '. Il parto resta '
                                       'raggruppato in SIPO, da ATTO.ID_LAVORAZIONE_PADRE.'))
    D.sostituisci(d, 'ATTI_GEMELLARI riceve le N righe nello stesso momento, con '
                  'id_richiesta_prenotazione vuoto, perché la prenotazione la fa l’ufficiale sulla '
                  'web app.', 'Fino al recupero il parto si riconosce in SIPO, da '
                  'ATTO.ID_LAVORAZIONE_PADRE.', attese=1, fatti=fatti)
    D.sostituisci(d, 'ATTI_GEMELLARI riceve ty_use_case e fg_stesura_atto 1; ', '', attese=1,
                  fatti=fatti)
    D.sostituisci(d, 'il tipo di nascita letto in ANSC e gli identificativi dei gemelli '
                  'adiacenti.', 'la chiave del parto, la posizione, il tipo di nascita letto in '
                  'ANSC e gli identificativi dei gemelli adiacenti.', attese=1, fatti=fatti)

    D.sostituisci(d, 'una riga della tabella dei gemelli e una di ANSC_SOGGETTO_ATTO, descritte '
                  'più avanti.', 'una riga di ANSC_SOGGETTO_ATTO, descritta più avanti, con la '
                  'chiave del parto e la posizione.', attese=1, fatti=fatti)

    # 4. Effetti sul disegno: via la tabella di Side, restano gli adattamenti dichiarati
    p = para_che_inizia(d, 'Per tenere insieme i gemelli di un parto lato ANSC')
    D.testo_di(p, SIDE_INTRO)
    col_side = tabella_che_contiene(d, 'id_atto_gemellare')
    ultimo = para_che_inizia(d, 'ON ANSC_USR.ATTI_GEMELLARI (id_richiesta_prenotazione);')
    n = togli_da_a(col_side._tbl, ultimo._p)
    fatti.append('tolti colonne e DDL di ATTI_GEMELLARI: %d elementi' % n)
    scelte = tabella_che_contiene(d, 'Scelta di Side')
    intest = scelte.rows[0]._tr
    for riga in reversed(SCELTE_NUOVE):
        D.clona_riga(scelte, riga)
        intest.addnext(riga_di(scelte, riga[0])._tr)
    r = riga_di(scelte, 'Colonne idAnsc, atti_gemelli_prec, atti_gemelli_succ.')
    D.riscrivi_cella(r.cells[1], 'Si registrano in ANSC_SOGGETTO_ATTO: ID_ANSC e gli '
                     'identificativi dei soli gemelli adiacenti.')
    D.riscrivi_cella(r.cells[2], 'Una sola tabella da cui leggere il nato, il suo atto e i suoi '
                     'fratelli. ID_ANSC è una copia dello store, allineata nella stessa '
                     'transazione; le liste del modello evento seguono la catena dei gemelli '
                     'adiacenti.')
    r = riga_di(scelte, '—')
    D.riscrivi_cella(r.cells[1], 'ANSC_SOGGETTO_ATTO.ID_LAVORAZIONE_PADRE, chiave del '
                     'raggruppamento.')
    D.riscrivi_cella(r.cells[2], 'L’ID_ATTO del gemello 1. Raggruppa i gemelli anche quando la '
                     'prenotazione non passa da SIPO (caso 2). Il numero comunale non si ripete: '
                     'sta in ANSC_STATO_ATTO.NUMERO_ATTO e in DATI_ATTO_ESTERNO.')
    D.sostituisci(d, 'registra store, tabella dei gemelli e ANSC_SOGGETTO_ATTO in una sola azione',
                  'registra store e ANSC_SOGGETTO_ATTO in una sola azione', attese=1, fatti=fatti)

    # 5. ANSC_SOGGETTO_ATTO
    D.testo_di(para_che_inizia(d, 'La tabella nuova sta in ANSC_USR, accanto allo store'),
               TABELLA_SA)
    t = [x for x in d.tables if x.rows[0].cells[0].text.strip() == 'Colonna'
         and any(r.cells[0].text.strip() == 'ID_SOGGETTO_ATTO' for r in x.rows)]
    assert len(t) == 1
    t = t[0]
    D.clona_riga(t, ['ID_LAVORAZIONE_PADRE', 'NUMBER (FK)', 'Il parto: l’ID_ATTO del gemello 1, '
                     'cioè ATTO.ID_LAVORAZIONE_PADRE dei gemelli 2…N (per il gemello 1 SIPO lascia '
                     'la colonna vuota e qui si scrive il suo ID_ATTO). Chiave esterna verso la '
                     'riga dello store del gemello 1. Vuota fuori dal parto plurimo.'])
    riga_di(t, 'ID_ANSC_SOGGETTO')._tr.addnext(riga_di(t, 'ID_LAVORAZIONE_PADRE')._tr)
    primo = para_che_inizia(d, 'CREATE TABLE ANSC_USR.ANSC_SOGGETTO_ATTO')
    ultimo = para_che_inizia(d, 'CREATE INDEX IX_ANSC_SOGG_ATTO_ANSC')
    inserisci_prima(d, primo._p, lambda: codice(d, DDL))
    togli_da_a(primo._p, ultimo._p)
    rifai_voce(d, para_che_inizia(d, 'Le copie dallo store.'), *COPIE)
    rifai_voce(d, para_che_inizia(d, 'I dati del gemello.'), *GEMELLI)

    # 6. righe dello store
    t = tabella_che_contiene(d, 'Righe toccate')
    D.riscrivi_cella(t.rows[0].cells[3], 'ANSC_SOGGETTO_ATTO')
    cella(t, 'DEFINISCI: R009 /prenota/evento', 3, 'INSERT di N righe, COD_ORIGINE PRENOTAZIONE, '
          'con ID_LAVORAZIONE_PADRE, ID_ANSC, ID_UC_ANSC, progressivo, tipo di nascita e '
          'identificativi dei gemelli adiacenti.')
    cella(t, '«VALIDA» del gemello k', 3, 'Se l’idAnsc differisce da quello prenotato: ID_ANSC '
          'della riga k e ID_ANSC_GEMELLO_PREC/SUCC dei fratelli adiacenti si allineano allo '
          'store.')
    cella(t, 'Firme del gemello k', 3, '—')
    cella(t, 'Definizione del gemello k, dentro DEFINISCI', 3, 'Si completa ID_SOGGETTO.')
    cella(t, 'Ripresa del parto', 3, 'ID_ANSC e ID_UC_ANSC confrontati con lo store; una '
          'differenza ferma la ripresa.')
    for r in t.rows[1:]:
        assert 'ATTI_GEMELLARI' not in r.cells[3].text and 'fg_stesura' not in r.cells[3].text, \
            r.cells[3].text

    # 7. legami
    D.testo_di(para_che_inizia(d, 'ANSC_STATO_ATTO non porta alcuna colonna del parto'), LEGAME)
    sostituisci_figura(d, 'Le righe di ANSC_STATO_ATTO nel parto plurimo', png('gem7_erd.pptx.png'),
                       6.3, 'Le righe di ANSC_STATO_ATTO nel parto plurimo e i loro legami, con '
                       'ANSC_SOGGETTO_ATTO')
    tl = tabella_che_contiene(d, 'Gemello ↔ parto')
    via = riga_di(tl, 'Gemello ↔ stato in ANSC')._tr
    via.getparent().remove(via)
    for i, v in enumerate(['Gemello ↔ parto', 'ANSC_SOGGETTO_ATTO.ID_LAVORAZIONE_PADRE',
                           'ANSC_STATO_ATTO.ID_ATTO_SIPO del gemello 1 (= ATTO.ID_ATTO)',
                           'Chiave esterna dichiarata; è la chiave del raggruppamento. Verso '
                           'SIPO per valore.', 'N:1']):
        D.riscrivi_cella(riga_di(tl, 'Gemello ↔ parto').cells[i], v)
    D.riscrivi_cella(riga_di(tl, 'Posizione').cells[1], 'ANSC_SOGGETTO_ATTO.'
                     'NUM_PROGRESSIVO_GEMELLO')
    D.riscrivi_cella(riga_di(tl, 'Posizione').cells[3], 'Per valore; uguali per regola (GE-08); '
                     'unica nel parto.')

    # 8. l'interrogazione del parto
    primo = para_che_inizia(d, 'SELECT g.nr_progressivo_gemello')
    ultimo = para_che_inizia(d, 'ORDER BY g.nr_progressivo_gemello;')
    inserisci_prima(d, primo._p, lambda: codice(d, SQL))
    togli_da_a(primo._p, ultimo._p)
    D.sostituisci(d, 'con le righe di ATTI_GEMELLARI', 'con le righe di ANSC_SOGGETTO_ATTO',
                  attese=1, fatti=fatti)

    # 9. figure
    sostituisci_figura(d, 'I due casi: la scelta dopo la divisione', png('gem7_panoramica.pptx.png'),
                       6.3, 'I due casi: la scelta dopo la divisione')
    sostituisci_figura(d, 'Caso 2: le pagine', png('gem7_flusso_2.pptx.png'), 5.9,
                       didascalia(d, 'Caso 2: le pagine').text.split(' – ', 1)[1])
    sostituisci_figura(d, 'La ripresa di un parto interrotto', png('gem7_ripresa.pptx.png'), 5.6,
                       'La ripresa di un parto interrotto')

    # 10. punti aperti
    op = D.trova_tabella(d, 'tema', 'questione')
    c = riga_di(op, 'GE-14').cells[2]
    assert 'La chiave esterna di ATTI_GEMELLARI dipende da questa scelta.' in c.text
    D.riscrivi_cella(c, c.text.replace('La chiave esterna di ATTI_GEMELLARI dipende da questa '
                                       'scelta.', 'Le due chiavi esterne di ANSC_SOGGETTO_ATTO '
                                       'dipendono da questa scelta.'))
    c = riga_di(op, 'GE-17').cells[2]
    D.riscrivi_cella(c, c.text.rstrip('.') + ', e la chiave del parto ID_LAVORAZIONE_PADRE, che '
                     'sostituisce la tabella dei gemelli di Side.')

    # 11. nessun ATTI_GEMELLARI fuori dalla Storia
    residui = [p.text for p in d.paragraphs if 'ATTI_GEMELLARI' in p.text] + \
              [c.text for tb in d.tables if tb._tbl is not storia_t._tbl
               for rr in tb.rows for c in rr.cells if 'ATTI_GEMELLARI' in c.text]
    xml_testo = ''.join(x.text or '' for x in d.element.body.iter(qn('w:t'))
                        if not any(a is storia_t._tbl for a in x.iterancestors()))
    assert not residui and 'ATTI_GEMELLARI' not in xml_testo, residui

    # 12. figure rinumerate, frontespizio, storia
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])
    for fatto in D.frontespizio(d, '0.7', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.7', 'In sintesi · La modalità di integrazione · Effetti sul disegno · '
             'Le righe di ANSC_STATO_ATTO nel parto plurimo · Punti aperti',
             'La tabella dei gemelli di Side non si crea: ANSC_SOGGETTO_ATTO riceve la chiave del '
             'parto ID_LAVORAZIONE_PADRE (chiave esterna verso la riga dello store del gemello 1, '
             'unica con la posizione) ed è l’unica tabella dei gemelli; le altre colonne di Side '
             'vanno nell’audit o si ricavano, come dichiarato negli adattamenti. DDL, legami, '
             'interrogazione del parto, righe dello store e diagrammi aggiornati; GE-14, GE-17.')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
