# -*- coding: utf-8 -*-
"""v3.14 — Appendice A: il DDL segue il modello dati, non lo insegue.

⚠️ La chiave di unicità è il punto che cambia sostanza: era
(evento, operazione, Modello, versione), cioè «un solo UC per Modello», che è esattamente
ciò che la v3.14 nega. Diventa (COD_UC_ANSC, ID_VERSIONE): più UC per Modello, ciascuno con
la propria condizione e la propria priorità.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

CONDIZIONE_DDL = """ANSC_CFG_UC_CONDIZIONE
CREATE TABLE ANSC_USR.ANSC_CFG_UC_CONDIZIONE (
  ID_CONDIZIONE        NUMBER GENERATED ALWAYS AS IDENTITY,
  ID_UC_CFG            NUMBER             NOT NULL,
  TXT_QUERY            CLOB               NOT NULL,
  DESCRIZIONE          VARCHAR2(400 CHAR) NOT NULL,
  NUM_ORDINE           NUMBER DEFAULT 1   NOT NULL,
  COD_ORIGINE          VARCHAR2(20 CHAR) DEFAULT 'INSERITA' NOT NULL,
  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  UTENTE_INS           VARCHAR2(40 CHAR),
  UTENTE_UPD           VARCHAR2(40 CHAR),
  CONSTRAINT PK_ANSC_CFG_UC_CONDIZIONE PRIMARY KEY (ID_CONDIZIONE),
  CONSTRAINT FK_ANSC_CFG_UC_CONDIZIONE_UC
    FOREIGN KEY (ID_UC_CFG) REFERENCES ANSC_USR.ANSC_CFG_UC (ID_UC_CFG),
  CONSTRAINT CK_ANSC_CFG_UC_CONDIZIONE_ORIG
    CHECK (COD_ORIGINE IN ('PROPOSTA','CONFERMATA','MODIFICATA','INSERITA'))
) TABLESPACE ANSC_USR;
COMMENT ON TABLE ANSC_USR.ANSC_CFG_UC_CONDIZIONE IS
  'Condizioni di applicabilita di un UC: interrogazioni in sola lettura sui dati che SIPO ha
   gia registrato per l atto in lavorazione. In congiunzione fra loro.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC_CONDIZIONE.TXT_QUERY IS
  'Query eseguita con utenza priva di privilegi di scrittura; riceve l identificativo dell
   atto come parametro e restituisce una riga quando la condizione e soddisfatta.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC_CONDIZIONE.DESCRIZIONE IS
  'Che cosa la condizione riconosce, in lingua corrente: e l unica parte leggibile da chi non
   conosce SQL, per questo non e facoltativa.';"""


def applica(doc):
    fatti = []
    ps = doc.paragraphs

    # -------------------------------------------------- chiave e colonne di ANSC_CFG_UC
    D.sostituisci(doc, '  ID_OPERAZIONE    NUMBER GENERATED ALWAYS AS IDENTITY,',
                  '  ID_UC_CFG            NUMBER GENERATED ALWAYS AS IDENTITY,',
                  attese=1, etichetta='chiave surrogata', fatti=fatti)
    D.sostituisci(doc, 'PRIMARY KEY (ID_OPERAZIONE)', 'PRIMARY KEY (ID_UC_CFG)',
                  attese=1, etichetta='chiave primaria', fatti=fatti)
    # ⚠️ COD_UC_ANSC compare anche nel DDL delle regole: si agisce dentro il blocco di
    # ANSC_CFG_UC, non per sostituzione globale.
    inizio = next(p for p in doc.paragraphs
                  if p.text.strip() == 'CREATE TABLE ANSC_USR.ANSC_CFG_UC (')
    i0 = D.indice_di(doc, inizio)
    riga_uc = next(p for p in doc.paragraphs[i0:i0 + 25]
                   if p.text.strip().startswith('COD_UC_ANSC'))
    D.testo_di(riga_uc, '  COD_UC_ANSC          VARCHAR2(20 CHAR)  NOT NULL,')
    fatti.append('ANSC_CFG_UC: COD_UC_ANSC obbligatorio')
    D.sostituisci(doc,
                  '    UNIQUE (COD_TIPO_EVENTO, COD_TIPO_OPERAZIONE, ID_MODELLO_ATTO, ID_VERSIONE),',
                  '    UNIQUE (COD_UC_ANSC, ID_VERSIONE),',
                  attese=1, etichetta='unicità per UC e non per Modello', fatti=fatti)

    # le due colonne nuove, prima di ID_VERSIONE
    ancora = next(p for p in doc.paragraphs
                  if p.text.strip().startswith('ID_VERSIONE          NUMBER'))
    for testo in ("  NUM_PRIORITA         NUMBER DEFAULT 100  NOT NULL,",
                  "  FLG_ATTIVO           CHAR(1) DEFAULT 'N' NOT NULL,"):
        D.riga_dopo(doc, ancora, testo)
    fatti.append('ANSC_CFG_UC: aggiunte NUM_PRIORITA e FLG_ATTIVO')

    ck = next(p for p in doc.paragraphs
              if "CK_ANSC_CFG_UC_FLG_FIRMA CHECK (FLG_FIRMA IN ('S','N'))" in p.text)
    D.testo_di(ck, "  CONSTRAINT CK_ANSC_CFG_UC_FLG_FIRMA CHECK (FLG_FIRMA IN ('S','N')),")
    D.riga_dopo(doc, ck,
                "  CONSTRAINT CK_ANSC_CFG_UC_FLG_ATTIVO CHECK (FLG_ATTIVO IN ('S','N'))")
    fatti.append('ANSC_CFG_UC: vincolo su FLG_ATTIVO')

    # -------------------------------------------------- COD_ORIGINE su CAMPO e ALLEGATO
    for tabella, dopo_col in (('ANSC_CFG_CAMPO', 'MESSAGGIO'),
                              ('ANSC_CFG_ALLEGATO', 'ID_VERSIONE')):
        blocco = next((p for p in doc.paragraphs
                       if p.text.strip().startswith(f'CREATE TABLE ANSC_USR.{tabella} (')), None)
        if blocco is None:
            continue
        i = D.indice_di(doc, blocco)
        riga = next((p for p in doc.paragraphs[i:i + 30]
                     if p.text.strip().startswith(dopo_col)), None)
        if riga is not None:
            D.riga_dopo(doc, riga,
                        "  COD_ORIGINE          VARCHAR2(20 CHAR) DEFAULT 'PROPOSTO' NOT NULL,")
            fatti.append(f'{tabella}: aggiunta COD_ORIGINE')

    # -------------------------------------------------- la tabella nuova, in coda a CFG_UC
    fine = next(p for p in doc.paragraphs
                if p.text.strip() == 'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.ID_CONF_TIPO_ATTO IS')
    j = D.indice_di(doc, fine)
    coda = doc.paragraphs[j + 1]
    for riga in reversed(CONDIZIONE_DDL.split('\n')):
        D.riga_dopo(doc, coda, riga)
    fatti.append(f'ANSC_CFG_UC_CONDIZIONE: DDL inserito ({len(CONDIZIONE_DDL.splitlines())} righe)')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
