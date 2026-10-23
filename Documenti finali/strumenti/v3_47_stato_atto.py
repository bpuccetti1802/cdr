# -*- coding: utf-8 -*-
"""v3.47 dell'analisi ANSC, dalla v3.46 (23/10/2026).

Richiesta dell'utente: di ANSC_STATO_ATTO interessano, per la parte legata al ModelEvento, solo
i campi che la tabella «La testata del modello evento» registra in colonna, esclusi i deprecati;
le altre colonne restano come sono.

Verifica: le colonne legate al ModelEvento sono esattamente le sedici di quella tabella e
nessuna è deprecata; scheda descrittiva e DDL hanno lo stesso insieme di colonne. Restano tre
disallineamenti sui campi del ModelEvento, che questo script corregge:
  - ID_TIPO_EVENTO e ID_TIPO_CONTENUTO: la scheda dichiarava VARCHAR2(20) e valori a parole
    (MORTE…), la DDL VARCHAR2(10) e le decodifiche ANSC_01/ANSC_02 sono codici;
  - NUM_COMUNALE: VARCHAR2(30) contro sei cifre della serie (NUMERATORE_COMUNALE, NUMBER(6));
    la nota citava OP-44, chiuso dalla v3.38.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_47_stato_atto.py
"""
import os
import sys

import docx

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.46.docx')
OUT = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.47.docx')

RIGHE = {
    'ID_TIPO_EVENTO': ('VARCHAR2(10)',
                       'idTipoEvento, decodifica ANSC_01: 1 nascita, 2 morte, 3 matrimonio, '
                       '4 unione civile, 5 cittadinanza. È quello dell’UC determinato '
                       '(ANSC_CFG_UC.ID_TIPO_EVENTO).'),
    'ID_TIPO_CONTENUTO': ('VARCHAR2(10)',
                          'idtipocontenuto, decodifica ANSC_02: atto, annotazione, trascrizione, '
                          'annotazione automatica, rifiuto. È quello dell’UC determinato '
                          '(ANSC_CFG_UC.ID_TIPO_CONTENUTO).'),
    'NUM_COMUNALE': ('VARCHAR2(6)',
                     'numeroatto: il numero comunale dell’atto, staccato da num-ansc-sipo '
                     'all’Anteprima. Sei cifre, come la serie del numeratore; il contratto ne '
                     'dichiara cinque (OP-73). Sull’atto di stato civile di SIPO non esiste una '
                     'colonna dedicata: se aggiungerla lì resta da decidere (OP-60).'),
}


def main():
    if os.path.exists(OUT):
        raise SystemExit('esiste già: ' + OUT)
    doc = docx.Document(SRC)
    t = D.tabella_colonne(doc, 'ID_STATO_ATTO')
    for r in t.rows:
        nome = r.cells[0].text.strip()
        if nome in RIGHE:
            D.riscrivi_cella(r.cells[1], RIGHE[nome][0])
            D.riscrivi_cella(r.cells[2], RIGHE[nome][1])
    D.sostituisci(doc, '  NUM_COMUNALE            VARCHAR2(30 CHAR),',
                  '  NUM_COMUNALE            VARCHAR2(6 CHAR),', attese=1)
    D.storia(doc, '23/10/2026', '3.47', 'Adeguamenti database · Appendice A',
             'Verificata ANSC_STATO_ATTO contro la testata del modello evento: le colonne legate '
             'al ModelEvento sono le sedici che la testata registra in colonna, nessuna deprecata. '
             'Allineati alla DDL e alle decodifiche ID_TIPO_EVENTO e ID_TIPO_CONTENUTO (codici '
             'ANSC_01 e ANSC_02, dieci caratteri); NUM_COMUNALE portato a sei caratteri come la '
             'serie del numeratore.')
    D.frontespizio(doc, '3.47', 'ANALISI_Integrazione-ANSC_v3.47')
    doc.save(OUT)
    print('scritto:', OUT)


if __name__ == '__main__':
    main()
