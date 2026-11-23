# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.6 (21/11/2026), dal FILE REALE della v0.5 salvato
dall'utente alle 11:02 (casella di testo «I record nella tabella vengono inseriti…», titolo «Nel
caso di gemelli con stato eterogeneo», «Punti da chiarire» tolto: non rieseguire gemellari_v0_5.py).

Decisione dell'utente (21/11/2026): ANSC_SOGGETTO_ATTO porta TUTTO ciò che serve a leggere il
nato, il suo atto e i suoi fratelli da una sola tabella:
  * ID_ANSC e ID_UC_ANSC, copie di ANSC_STATO_ATTO allineate nella stessa transazione;
  * NUM_PROGRESSIVO_GEMELLO e ID_TIPO_NASCITA (ANSC_107 = tipoNascitaSoggetto del modello evento);
  * ID_ANSC_GEMELLO_PREC / ID_ANSC_GEMELLO_SUCC = identificativo ANSC del gemello ADIACENTE (le
    liste attiGemelliPrec/Succ si ottengono seguendo la catena).
Figura: diagrammi_gemellari_v0_6_pptx.py → gem6_erd.

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_6.py
"""
import os
import re
import sys

import docx

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import voce                              # noqa: E402
from gemellari_v0_2 import codice, para_che_inizia, tabella_che_contiene   # noqa: E402
from gemellari_v0_4 import rifai_voce, riga_di, sostituisci_figura  # noqa: E402
from gemellari_v0_5 import inserisci_prima                         # noqa: E402

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.5.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.6.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '21/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')

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
    '  CONSTRAINT FK_ANSC_SOGG_ATTO_STATO FOREIGN KEY (ID_ATTO_SIPO)',
    '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_RIF',
    '    CHECK (ID_NASCITA_SOGGETTO IS NOT NULL OR ID_SOGGETTO IS NOT NULL),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_ORIG',
    "    CHECK (COD_ORIGINE IN ('PRENOTAZIONE','RECUPERO','VALIDAZIONE')),",
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_PROG',
    '    CHECK (NUM_PROGRESSIVO_GEMELLO BETWEEN 1 AND 10),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_GEM',
    '    CHECK (NUM_PROGRESSIVO_GEMELLO IS NOT NULL',
    '           OR (ID_ANSC_GEMELLO_PREC IS NULL AND ID_ANSC_GEMELLO_SUCC IS NULL))',
    ');',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_NASC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_NASCITA_SOGGETTO);',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_SOGG ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_SOGGETTO);',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_ANSC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_ANSC);',
]

COLONNE_ATTO = [
    ['ID_ANSC', 'VARCHAR2(50)', 'Identificativo nazionale dell’atto ANSC: copia di '
     'ANSC_STATO_ATTO.ID_ANSC, scritta e aggiornata nella stessa transazione. Vuota finché l’atto '
     'non è prenotato o recuperato.'],
    ['ID_UC_ANSC', 'VARCHAR2(20)', 'UC con cui l’atto è formato: copia di '
     'ANSC_STATO_ATTO.ID_UC_ANSC. Nel caso 1 l’UC comune ai gemelli, nel caso 2 11999999, il caso '
     'd’uso di servizio.'],
]
COLONNE_GEMELLO = [
    ['NUM_PROGRESSIVO_GEMELLO', 'NUMBER(2)', 'Posizione del gemello nel parto = POS_GEMELLO = '
     'progressivoGemello del modello evento. Vuota fuori dal parto plurimo.'],
    ['ID_TIPO_NASCITA', 'VARCHAR2(10)', 'Tipo di nascita del nato, decodifica ANSC_107 (1 nato '
     'vivo, 2 nato morto, 3 nato vivo ma successivamente deceduto) = tipoNascitaSoggetto del '
     'modello evento. Nel caso 1 si ricava alla prenotazione dai due flag di SIPO; nel caso 2 è '
     'quello letto in ANSC al recupero, dopo il confronto con i flag. I valori si controllano '
     'sulla decodifica, non con un vincolo.'],
    ['ID_ANSC_GEMELLO_PREC', 'VARCHAR2(50)', 'Identificativo ANSC dell’atto del gemello '
     'immediatamente precedente. Vuoto per il gemello 1 e fuori dal parto plurimo.'],
    ['ID_ANSC_GEMELLO_SUCC', 'VARCHAR2(50)', 'Identificativo ANSC dell’atto del gemello '
     'immediatamente successivo. Vuoto per l’ultimo gemello e fuori dal parto plurimo.'],
]

COPIE = (
    'Le copie dallo store.', 'ID_ANSC e ID_UC_ANSC ripetono i valori di ANSC_STATO_ATTO, così '
    'che il nato, il suo atto e i suoi fratelli si leggano da una sola tabella. Una copia può '
    'divergere, quindi vale una regola: le scrive solo il concentratore, nella stessa transazione '
    'in cui aggiorna lo store (prenotazione, validazione, recupero, ripresa), e la ripresa del '
    'parto le confronta con lo store e con ANSC. Il caso da presidiare è la validazione che '
    'restituisce un identificativo diverso da quello prenotato (GE-02): cambiano lo store, la riga '
    'del gemello e i riferimenti dei due fratelli adiacenti. Posizione e UC ripetono anche '
    'nr_progressivo_gemello e ty_use_case di ATTI_GEMELLARI, che resta la struttura ripresa da '
    'Side: coincidono per regola.')
GEMELLI = (
    'I dati del gemello.', 'NUM_PROGRESSIVO_GEMELLO, ID_TIPO_NASCITA e i due riferimenti adiacenti '
    'si valorizzano solo nel parto plurimo; fuori restano vuoti, e un vincolo impedisce i '
    'riferimenti ai fratelli senza la posizione. Nel caso 1 si scrivono tutti alla prenotazione, '
    'quando gli identificativi arrivano insieme; nel caso 2 al recupero, quando ANSC restituisce gli '
    'atti formati sulla web app. Un riferimento è l’identificativo ANSC del solo gemello adiacente: '
    'le liste dei fratelli si ottengono seguendo la catena.')

FRATELLI = (
    'attiGemelliPrec e attiGemelliSucc del gemello k si ricavano da ANSC_SOGGETTO_ATTO seguendo la '
    'catena: i primi risalendo con ID_ANSC_GEMELLO_PREC fino al gemello 1, i secondi scendendo con '
    'ID_ANSC_GEMELLO_SUCC fino all’ultimo, nell’ordine del progressivo; l’interrogazione del parto '
    'dà lo stesso risultato e serve da controllo. numeroGemelli è il numero delle righe del parto, '
    'progressivoGemello è NUM_PROGRESSIVO_GEMELLO, tipoNascitaSoggetto è ID_TIPO_NASCITA, '
    'partoGemellare vale SI. Le liste si scrivono nel TXT_EVENTO della riga k a ogni composizione '
    'del modello evento.')


def main():
    d = docx.Document(IN)
    fatti = []

    # 1. In sintesi
    p = para_che_inizia(d, 'Il soggetto e il suo atto ANSC.')
    rifai_voce(d, p, 'Il soggetto e il suo atto ANSC.',
               'Una tabella nuova, ANSC_SOGGETTO_ATTO, registra per ciascun nato l’atto ANSC che lo '
               'ha per intestatario, con l’identificativo nazionale e l’UC dell’atto e, per i '
               'gemelli, posizione, tipo di nascita e identificativi dei gemelli adiacenti: alla '
               'prenotazione nel caso 1, al recupero nel caso 2. Vale anche fuori dal parto '
               'plurimo.')

    # 2. presentazione della tabella
    p = para_che_inizia(d, 'La tabella nuova sta in ANSC_USR, accanto allo store')
    D.testo_di(p, 'La tabella nuova sta in ANSC_USR, accanto allo store, ed è distinta da '
               'ATTI_GEMELLARI: quella raggruppa il parto, questa lega un soggetto all’atto ANSC di '
               'cui è intestatario, e vale per qualunque atto. Registra il soggetto con il '
               'riferimento disponibile quando l’abbinamento avviene e lo completa dopo; porta '
               'l’identificativo e l’UC dell’atto e, nel parto plurimo, i dati del gemello, così '
               'che il nato, il suo atto e i suoi fratelli si leggano da una riga.')

    # 3. tabella delle colonne
    t = [x for x in d.tables if x.rows[0].cells[0].text.strip() == 'Colonna'
         and any(r.cells[0].text.strip() == 'ID_SOGGETTO_ATTO' for r in x.rows)]
    assert len(t) == 1
    t = t[0]
    ancora = riga_di(t, 'ID_ATTO_SIPO')._tr
    for riga in reversed(COLONNE_ATTO):
        D.clona_riga(t, riga)
        ancora.addnext(riga_di(t, riga[0])._tr)
    ancora = riga_di(t, 'ID_ANSC_SOGGETTO')._tr
    for riga in reversed(COLONNE_GEMELLO):
        D.clona_riga(t, riga)
        ancora.addnext(riga_di(t, riga[0])._tr)

    # 4. DDL
    primo = para_che_inizia(d, 'CREATE TABLE ANSC_USR.ANSC_SOGGETTO_ATTO')
    ultimo = para_che_inizia(d, 'CREATE INDEX IX_ANSC_SOGG_ATTO_SOGG')
    inserisci_prima(d, primo._p, lambda: codice(d, DDL))
    # codice() aggiunge una riga vuota in coda: la vecchia DDL ne ha già una prima di sé
    e, via = primo._p, []
    while True:
        via.append(e)
        if e is ultimo._p:
            break
        e = e.getnext()
    for x in via:
        assert not D.ha_commenti(x)
        x.getparent().remove(x)
    vuota = primo._p  # già rimosso; la riga vuota di codice() resta prima della casella di testo
    del vuota

    # 5. voci sotto la DDL (la casella di testo dell'utente non si tocca)
    rifai_voce(d, para_che_inizia(d, 'Che cosa non ripete.'), *COPIE)
    inserisci_prima(d, para_che_inizia(d, 'Una sola riga per ruolo.')._p,
                    lambda: voce(d, *GEMELLI))

    # 6. figura dei legami
    sostituisci_figura(d, 'Le righe di ANSC_STATO_ATTO nel parto plurimo',
                       os.path.join(IMG, 'gem6_erd.pptx.png'), 6.3,
                       'Le righe di ANSC_STATO_ATTO nel parto plurimo e i loro legami, con '
                       'ATTI_GEMELLARI e ANSC_SOGGETTO_ATTO')

    # 7. righe dello store e legami
    t = tabella_che_contiene(d, 'Righe toccate')
    c = riga_di(t, 'DEFINISCI: R009 /prenota/evento').cells[3]
    D.riscrivi_cella(c, 'INSERT di N righe, fg_stesura_atto 0. ANSC_SOGGETTO_ATTO: N righe, '
                     'COD_ORIGINE PRENOTAZIONE, con ID_ANSC, ID_UC_ANSC, progressivo, tipo di '
                     'nascita e identificativi dei gemelli adiacenti.')
    c = riga_di(t, '«VALIDA» del gemello k').cells[3]
    D.riscrivi_cella(c, 'Se l’idAnsc differisce da quello prenotato: ANSC_SOGGETTO_ATTO.ID_ANSC '
                     'della riga k e ID_ANSC_GEMELLO_PREC/SUCC dei fratelli adiacenti si allineano '
                     'allo store.')
    c = riga_di(t, 'Ripresa del parto').cells[3]
    D.riscrivi_cella(c, 'ANSC_SOGGETTO_ATTO: ID_ANSC e ID_UC_ANSC confrontati con lo store; una '
                     'differenza ferma la ripresa.')
    tl = tabella_che_contiene(d, 'Gemello ↔ parto')
    r = riga_di(tl, 'Fratelli in ANSC')
    for i, v in enumerate(['Fratelli in ANSC', 'ANSC_SOGGETTO_ATTO.ID_ANSC_GEMELLO_PREC, '
                           'ID_ANSC_GEMELLO_SUCC', 'ANSC_SOGGETTO_ATTO.ID_ANSC del gemello '
                           'adiacente', 'Per valore; scritti alla prenotazione (caso 1) o al '
                           'recupero (caso 2). Le liste del modello evento seguono la catena.',
                           '1:0..1']):
        D.riscrivi_cella(r.cells[i], v)
    D.clona_riga(tl, ['Copie dallo store', 'ANSC_SOGGETTO_ATTO.ID_ANSC, ID_UC_ANSC',
                      'ANSC_STATO_ATTO.ID_ANSC, ID_UC_ANSC', 'Copia, allineata nella stessa '
                      'transazione; confrontata alla ripresa.', '1:1'])

    # 8. elenchi dei fratelli e caso 2
    D.testo_di(para_che_inizia(d, 'attiGemelliPrec e attiGemelliSucc del gemello k'), FRATELLI)
    D.sostituisci(d, 'ANSC_SOGGETTO_ATTO la riga dell’intestatario, con COD_ORIGINE RECUPERO.',
                  'ANSC_SOGGETTO_ATTO la riga dell’intestatario, con COD_ORIGINE RECUPERO, '
                  'l’identificativo e l’UC dell’atto, il tipo di nascita letto in ANSC e gli '
                  'identificativi dei gemelli adiacenti.', attese=1, fatti=fatti)

    # 9. punti aperti
    op = D.trova_tabella(d, 'tema', 'questione')
    r = riga_di(op, 'GE-17')
    D.riscrivi_cella(r.cells[2], 'Da riportare in [R1]: la tabella, il dominio di COD_RUOLO, il '
                     'raccordo con ANSC_SOGGETTO_IDENTIFICATIVI una volta creato il soggetto del '
                     'nato, l’origine VALIDAZIONE per gli atti ordinari e le colonne copiate dallo '
                     'store (ID_ANSC, ID_UC_ANSC) con la regola che le tiene allineate.')

    # 10. figure rinumerate, frontespizio, storia
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])
    for fatto in D.frontespizio(d, '0.6', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.6', 'In sintesi · Effetti sul disegno (ANSC_SOGGETTO_ATTO) · Le righe di '
             'ANSC_STATO_ATTO nel parto plurimo · Punti aperti',
             'ANSC_SOGGETTO_ATTO porta l’identificativo e l’UC dell’atto (copie dello store, '
             'allineate nella stessa transazione) e, per i gemelli, posizione, tipo di nascita '
             '(ANSC_107) e identificativi ANSC dei gemelli adiacenti. DDL, colonne, legami ed '
             'elenchi dei fratelli aggiornati; schema delle tabelle rifatto; GE-17 integrato.')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
