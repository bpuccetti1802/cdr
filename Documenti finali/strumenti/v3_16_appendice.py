# -*- coding: utf-8 -*-
"""v3.16 — l'Appendice A torna a descrivere il modello che il corpo descrive.

⚠️ Erano sedici tabelle contro le nove del corpo. Le tre in più — `ANSC_CFG_UC_CONDIZIONE`,
`ANSC_CFG_REGOLA` e `ANSC_CFG_REGOLA_CONDIZIONE` — appartengono al disegno che la
semplificazione ha superato: la condizione è rientrata nell'UC, i controlli e le generazioni
sono rientrati nelle colonne dei campi. Lasciarle nel DDL significava consegnare a chi
implementa un modello che il documento non descrive più.

⚠️ Va segnalato che cosa la semplificazione ha tolto senza sostituirlo: `SERVIZIO_ANSC`
(quale operazione ANSC invocare), `FLG_TRASCRIZIONE` e `FLG_FIRMA`. Il DDL li perde perché il
corpo li ha persi; se servono vanno rimessi in entrambi i posti, non in uno solo.
"""
import os
import re
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.16.docx')

DA_RIMUOVERE = ['ANSC_CFG_UC_CONDIZIONE', 'ANSC_CFG_REGOLA', 'ANSC_CFG_REGOLA_CONDIZIONE']

CFG_UC = """CREATE TABLE ANSC_USR.ANSC_CFG_UC (
  ID_UC_CFG            NUMBER GENERATED ALWAYS AS IDENTITY,
  COD_UC_ANSC          VARCHAR2(20 CHAR)  NOT NULL,
  COD_TIPO_EVENTO      VARCHAR2(20 CHAR)  NOT NULL,
  COD_TIPO_OPERAZIONE  VARCHAR2(20 CHAR)  NOT NULL,
  ID_MODELLO_ATTO      VARCHAR2(5 CHAR)   NOT NULL,
  ID_CONF_TIPO_ATTO    NUMBER,
  MASCHERA_UI          VARCHAR2(100 CHAR),
  NUM_PRIORITA         NUMBER DEFAULT 100 NOT NULL,
  REGOLA_DI_SCELTA     VARCHAR2(2000 CHAR),
  ID_VERSIONE          NUMBER             NOT NULL,
  DATA_INIZIO_VALIDITA DATE DEFAULT SYSDATE            NOT NULL,
  DATA_FINE_VALIDITA   DATE DEFAULT DATE '9999-12-31'  NOT NULL,
  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  UTENTE_INS           VARCHAR2(40 CHAR),
  UTENTE_UPD           VARCHAR2(40 CHAR),
  CONSTRAINT PK_ANSC_CFG_UC PRIMARY KEY (ID_UC_CFG),
  CONSTRAINT FK_ANSC_CFG_UC_VERSIONE
    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),
  CONSTRAINT UK_ANSC_CFG_UC UNIQUE (COD_UC_ANSC, ID_VERSIONE)
) TABLESPACE ANSC_USR;
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.REGOLA_DI_SCELTA IS
  'Script che stabilisce se l UC si applica all atto in lavorazione, osservando i dati gia
   registrati da SIPO. Il linguaggio non e fissato dal documento: e scelta del Comune.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.NUM_PRIORITA IS
  'Ordine di valutazione fra gli UC dello stesso Modello: il primo la cui regola e soddisfatta
   determina l UC.';"""

CFG_CAMPO = """CREATE TABLE ANSC_USR.ANSC_CFG_CAMPO (
  ID_CAMPO             NUMBER GENERATED ALWAYS AS IDENTITY,
  ID_UC                NUMBER             NOT NULL,
  ID_VERSIONE          NUMBER             NOT NULL,
  SEZIONE_FE_ANSC      VARCHAR2(200 CHAR),
  DESC_COND_OBBLIGATORIETA   VARCHAR2(1000 CHAR),
  REGOLA_COND_OBBLIGATORIETA VARCHAR2(1000 CHAR),
  OGGETTO_ANSC         VARCHAR2(1000 CHAR) NOT NULL,
  CAMPO_ANSC           VARCHAR2(120 CHAR)  NOT NULL,
  FLG_OBBLIGATORIO     CHAR(1) DEFAULT 'N' NOT NULL,
  TABELLA_SIPO         VARCHAR2(200 CHAR),
  CAMPO_SIPO           VARCHAR2(120 CHAR),
  ID_DECODIFICA_ANSC   NUMBER,
  DESCRIZIONE_BUSINESS_LOGIC VARCHAR2(1000 CHAR),
  BUSINESS_LOGIC       VARCHAR2(1000 CHAR),
  ORDINAMENTO          NUMBER DEFAULT 1   NOT NULL,
  VALORE_DEFAULT       VARCHAR2(1000 CHAR),
  MESSAGGIO            VARCHAR2(200 CHAR),
  NOTE                 VARCHAR2(1000 CHAR),
  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  UTENTE_INS           VARCHAR2(40 CHAR),
  UTENTE_UPD           VARCHAR2(40 CHAR),
  CONSTRAINT PK_ANSC_CFG_CAMPO PRIMARY KEY (ID_CAMPO),
  CONSTRAINT FK_ANSC_CFG_CAMPO_UC
    FOREIGN KEY (ID_UC) REFERENCES ANSC_USR.ANSC_ANA_UC (ID_UC),
  CONSTRAINT FK_ANSC_CFG_CAMPO_VERSIONE
    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),
  CONSTRAINT UK_ANSC_CFG_CAMPO
    UNIQUE (ID_VERSIONE, ID_UC, OGGETTO_ANSC, CAMPO_ANSC),
  CONSTRAINT CK_ANSC_CFG_CAMPO_OBBL CHECK (FLG_OBBLIGATORIO IN ('S','N'))
) TABLESPACE ANSC_USR;
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.OGGETTO_ANSC IS
  'Binding Object del mapping ufficiale: l oggetto del modello evento che contiene il campo.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.BUSINESS_LOGIC IS
  'Script che produce il valore quando non e un trasferimento diretto. Linguaggio non fissato.';"""


def blocco(doc, nome):
    """Gli indici di inizio e fine del DDL di una tabella, commenti inclusi."""
    ps = doc.paragraphs
    for i, p in enumerate(ps):
        if re.match(rf'CREATE TABLE ANSC_USR\.{nome}\s*\(', p.text.strip()):
            fine = i
            for j in range(i + 1, len(ps)):
                t = ps[j].text.strip()
                if t.startswith('CREATE TABLE') or (ps[j].style.name.startswith('Heading') and t):
                    break
                fine = j
            return i, fine
    return None, None


def sostituisci_ddl(doc, nome, testo):
    i, f = blocco(doc, nome)
    assert i is not None, f'DDL non trovato: {nome}'
    ps = doc.paragraphs
    ancora = ps[f]
    for riga in reversed(testo.split('\n')):
        D.riga_dopo(doc, ancora, riga)
    for p in ps[i:f + 1]:
        if not D.ha_commenti(p._p):
            p._p.getparent().remove(p._p)
    return f - i + 1


def applica(doc):
    fatti = []
    for nome in DA_RIMUOVERE:
        i, f = blocco(doc, nome)
        if i is None:
            continue
        ps = doc.paragraphs
        # anche il titoletto che precede il blocco, se è il nome della tabella
        inizio = i - 1 if i and ps[i - 1].text.strip() == nome else i
        n = 0
        for p in ps[inizio:f + 1]:
            if D.ha_commenti(p._p):
                continue
            p._p.getparent().remove(p._p)
            n += 1
        fatti.append(f'rimosso il DDL di {nome} ({n} righe)')

    fatti.append(f'ANSC_CFG_UC: DDL riscritto ({sostituisci_ddl(doc, "ANSC_CFG_UC", CFG_UC)} '
                 f'righe sostituite)')
    fatti.append(f'ANSC_CFG_CAMPO: DDL riscritto '
                 f'({sostituisci_ddl(doc, "ANSC_CFG_CAMPO", CFG_CAMPO)} righe sostituite)')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
