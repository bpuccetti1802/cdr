# -*- coding: utf-8 -*-
"""v3.14 — le formule diventano configurazione, non più una lacuna dichiarata.

Le formule sono **diciture prestabilite** che l'ufficiale può inserire nell'atto: la scelta
si fa in configurazione, per UC, non atto per atto. Fino alla v3.13 il documento le
riconosceva come «lacuna adiacente» e le rinviava a un punto aperto; qui si configurano.

Numeri verificati sul mapping (non stimarli di nuovo): **2.200 righe «Formula», 366 UC su
374, 233 formule distinte**, da 1 a 22 per UC con **mediana 7**; **629 obbligatorie e 1.571
facoltative**. ⚠️ Le colonne «Note obbligatorietà formule» e «Condizioni obbligatorietà» sono
**vuote su tutte e 2.200 le righe**: per le formule il mapping dichiara il codice e
l'obbligatorietà, nient'altro.

⚠️ Che cosa il mapping NON dà, e resta lavoro del Comune: **il testo della dicitura**. Le
decodifiche ANSC_119 e ANSC_120 (`dec_tipo_formula_secretato` e `_non_secretato`) contengono
numeri di formula, non testi, e sono due valori ciascuna. Il testo va trascritto dalla
normativa: è ciò che resta di OP-51 dopo questa versione.

⚠️ Sei formule hanno un campo di testo libero nel modello evento (147-ter, 121-septies,
121-septies.1, 193, 140-bis, 122-bis.2): per quelle la configurazione deve dire anche dove il
testo va scritto nel payload, altrimenti la formula si sceglie ma non si compila.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

CFG_FORMULA = [
    ['Colonna', 'Tipo', 'Note'],
    ['ID_FORMULA', 'NUMBER (PK)', 'Chiave tecnica.'],
    ['ID_UC', 'NUMBER (FK)',
     'UC di riferimento nel catalogo ANSC_ANA_UC. Come per i campi e gli allegati, la formula '
     'pende dall’UC: lo stesso Modello di atto porta formule diverse secondo il caso d’uso '
     'determinato.'],
    ['COD_FORMULA', 'VARCHAR2(20)',
     'Numero della formula come lo dichiara il mapping: «197», «41-bis», «121-septies».'],
    ['TXT_FORMULA', 'CLOB',
     'La dicitura da inserire nell’atto. ⚠️ ANSC non pubblica i testi: il Comune li trascrive '
     'dalla normativa una volta sola, e da lì valgono per tutti gli UC che richiamano quel '
     'numero.'],
    ['FLG_OBBLIGATORIA', 'CHAR(1)',
     'S/N come dichiarato dal mapping. Delle 2.200 righe, 629 sono obbligatorie: le altre '
     'sono a disposizione dell’ufficiale.'],
    ['FLG_ADOTTATA', 'CHAR(1)',
     'S/N: se il Comune la rende disponibile all’ufficiale per questo UC. È la scelta che il '
     'presente disegno attribuisce alla configurazione — una formula obbligatoria è sempre '
     'adottata, una facoltativa lo è se il Comune decide di offrirla.'],
    ['CAMPO_ANSC', 'VARCHAR2(120)',
     'Percorso del campo di testo libero associato alla formula, quando esiste. Sono sei nel '
     'modello evento (147-ter, 121-septies, 121-septies.1, 193, 140-bis, 122-bis.2): per '
     'queste la scelta della formula non basta, occorre sapere dove scriverne il contenuto.'],
    ['NUM_ORDINE', 'NUMBER',
     'Ordine di presentazione all’ufficiale e di inserimento nell’atto.'],
    ['COD_ORIGINE', 'VARCHAR2(20)',
     'PROPOSTO, CONFERMATO, MODIFICATO, INSERITO: come per i campi e per gli allegati.'],
    ['ID_VERSIONE', 'NUMBER (FK)', 'Baseline di appartenenza (ANSC_CFG_VERSIONE).'],
    ['DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici previsti dallo standard di nomenclatura [R5].'],
]

PROSA = [
    ('p', 'Lo stesso tracciato dichiara, accanto a sezioni e allegati, una terza categoria: le '
          'formule ministeriali associate all’UC. Sono diciture prestabilite che l’ufficiale '
          'inserisce nell’atto, e la scelta di quali rendere disponibili si compie in '
          'configurazione, per caso d’uso, non davanti al singolo atto.'),
    ('p', 'Il mapping ne dichiara 2.200 righe su 366 UC dei 374, per 233 formule distinte: da '
          'una a ventidue per caso d’uso, con mediana sette. Di queste 629 sono obbligatorie e '
          '1.571 facoltative, ed è la proporzione che spiega perché la configurazione debba '
          'distinguere due cose diverse — che cosa ANSC prescrive e che cosa il Comune sceglie '
          'di offrire.'),
    ('p', '⚠️ Per le formule il mapping è più povero che per i campi: le colonne delle note e '
          'delle condizioni sono vuote su tutte e 2.200 le righe. Dichiara il numero della '
          'formula e se sia obbligatoria, nient’altro. In particolare non dichiara il testo '
          'della dicitura, e nemmeno le decodifiche lo pubblicano: ANSC_119 e ANSC_120 '
          'contengono numeri di formula distinti per il caso secretato e non secretato, non i '
          'testi. La trascrizione dei testi resta quindi lavoro del Comune, ed è la parte di '
          'OP-51 che questa versione non chiude.'),
    ('p', 'Un dettaglio da non perdere: sei formule hanno un campo di testo libero nel modello '
          'evento — 147-ter, 121-septies, 121-septies.1, 193, 140-bis e 122-bis.2. Per quelle '
          'la scelta della formula non basta: la configurazione deve dire anche in quale campo '
          'del payload il contenuto va scritto, altrimenti la formula si seleziona e resta '
          'vuota.'),
    ('p', 'ANSC_CFG_FORMULA — le diciture previste dall’UC.'),
]

ORIGINE_ALLEGATO = ('COD_ORIGINE', 'VARCHAR2(20)',
                    'PROPOSTO, CONFERMATO, MODIFICATO, INSERITO: come per i campi e per le '
                    'formule. Governa la reimportazione.')


def applica(doc):
    fatti = []
    modello = D.tabella_colonne(doc, 'ID_ALLEGATO')

    # ------------------------------------- la tabella degli allegati: allineare al DDL
    if 'COD_ORIGINE' not in [r.cells[0].text.strip() for r in modello.rows]:
        righe = [[c.text for c in r.cells] for r in modello.rows[1:]]
        tecnici = [v for v in righe if v[0].startswith('DATA_INS')]
        altri = [v for v in righe if not v[0].startswith('DATA_INS')]
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from v3_14_configurazione import riscrivi_tabella
        riscrivi_tabella(modello, altri + [list(ORIGINE_ALLEGATO)] + tecnici)
        fatti.append('ANSC_CFG_ALLEGATO: aggiunta COD_ORIGINE (era solo nel DDL)')

    # ------------------------------------- la sezione delle formule
    D.sostituisci_sezione(doc, 'Una lacuna adiacente: le formule',
                          'Le formule previste dall’UC', PROSA, livello=3)
    ancora = next(p for p in doc.paragraphs
                  if p.text.strip().startswith('ANSC_CFG_FORMULA —'))
    D.tabella(doc, ancora._p.getnext(), CFG_FORMULA, modello=modello)
    fatti.append(f'sezione «Le formule previste dall’UC» con ANSC_CFG_FORMULA '
                 f'({len(CFG_FORMULA) - 1} colonne)')
    return fatti





DDL = """ANSC_CFG_FORMULA
CREATE TABLE ANSC_USR.ANSC_CFG_FORMULA (
  ID_FORMULA           NUMBER GENERATED ALWAYS AS IDENTITY,
  ID_UC                NUMBER             NOT NULL,
  COD_FORMULA          VARCHAR2(20 CHAR)  NOT NULL,
  TXT_FORMULA          CLOB,
  FLG_OBBLIGATORIA     CHAR(1) DEFAULT 'N' NOT NULL,
  FLG_ADOTTATA         CHAR(1) DEFAULT 'N' NOT NULL,
  CAMPO_ANSC           VARCHAR2(120 CHAR),
  NUM_ORDINE           NUMBER DEFAULT 1   NOT NULL,
  COD_ORIGINE          VARCHAR2(20 CHAR) DEFAULT 'PROPOSTO' NOT NULL,
  ID_VERSIONE          NUMBER             NOT NULL,
  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  UTENTE_INS           VARCHAR2(40 CHAR),
  UTENTE_UPD           VARCHAR2(40 CHAR),
  CONSTRAINT PK_ANSC_CFG_FORMULA PRIMARY KEY (ID_FORMULA),
  CONSTRAINT FK_ANSC_CFG_FORMULA_UC
    FOREIGN KEY (ID_UC) REFERENCES ANSC_USR.ANSC_ANA_UC (ID_UC),
  CONSTRAINT FK_ANSC_CFG_FORMULA_VERSIONE
    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),
  CONSTRAINT UK_ANSC_CFG_FORMULA UNIQUE (ID_VERSIONE, ID_UC, COD_FORMULA),
  CONSTRAINT CK_ANSC_CFG_FORMULA_OBBL CHECK (FLG_OBBLIGATORIA IN ('S','N')),
  CONSTRAINT CK_ANSC_CFG_FORMULA_ADOT CHECK (FLG_ADOTTATA IN ('S','N')),
  CONSTRAINT CK_ANSC_CFG_FORMULA_ORIG
    CHECK (COD_ORIGINE IN ('PROPOSTO','CONFERMATO','MODIFICATO','INSERITO'))
) TABLESPACE ANSC_USR;
COMMENT ON TABLE ANSC_USR.ANSC_CFG_FORMULA IS
  'Diciture ministeriali previste per ciascun UC: quali ANSC prescrive e quali il Comune
   sceglie di offrire all ufficiale.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_FORMULA.TXT_FORMULA IS
  'Testo della dicitura: ANSC non lo pubblica, lo trascrive il Comune (residuo di OP-51).';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_FORMULA.CAMPO_ANSC IS
  'Campo di testo libero del modello evento associato alla formula, dove previsto: sono sei
   (147-ter, 121-septies, 121-septies.1, 193, 140-bis, 122-bis.2).';"""


def applica_2(doc):
    """DDL, back-office e punto aperto: la seconda metà, dopo il modello dati."""
    fatti = []

    # ------------------------------------------------------------------ App. A
    ancora = next(p for p in doc.paragraphs
                  if p.text.strip().startswith('CREATE TABLE ANSC_USR.ANSC_CFG_VERSIONE'))
    i = D.indice_di(doc, ancora)
    coda = next(p for p in doc.paragraphs[i:i + 60]
                if p.text.strip().endswith(') TABLESPACE ANSC_USR;'))
    for riga in reversed(DDL.split('\n')):
        D.riga_dopo(doc, coda, riga)
    fatti.append(f'App. A: DDL di ANSC_CFG_FORMULA ({len(DDL.splitlines())} righe)')

    # ------------------------------------------------------------ back-office
    t = D.trova_tabella(doc, 'Schermata', 'Scopo', 'Azioni principali', 'Ruolo')
    for riga in t.rows:
        if riga.cells[0].text.strip().startswith('Configurazione — Campi'):
            D.testo_di(riga.cells[0].paragraphs[0],
                       'Configurazione — Campi, allegati e formule per UC')
            D.testo_di(riga.cells[1].paragraphs[0],
                       'ANSC_CFG_CAMPO, ANSC_CFG_ALLEGATO e ANSC_CFG_FORMULA per singolo UC: '
                       'la corrispondenza fra percorso ANSC e sorgente SIPO, i documenti '
                       'richiesti e le diciture previste, con l’obbligatorietà dichiarata da '
                       'ANSC e la scelta del Comune.')
            fatti.append('back-office: schermata «Campi, allegati e formule per UC»')

    # ------------------------------------------------------------ OP-51
    D.sostituisci(doc,
                  'Le formule associate a ciascun UC sono dichiarate nel mapping (366 UC su '
                  '374, 233 formule distinte) ma non sono configurate dal presente disegno, e '
                  'fra le decodifiche pubblicate non esiste un catalogo che le descriva.',
                  'Le formule associate a ciascun UC sono ora configurate '
                  '(ANSC_CFG_FORMULA), ma ANSC non ne pubblica i testi: le decodifiche '
                  'ANSC_119 e ANSC_120 contengono numeri di formula per il caso secretato e '
                  'non secretato, non le diciture. Resta quindi da stabilire chi trascriva i '
                  '233 testi dalla normativa e li tenga allineati.',
                  attese=1, etichetta='OP-51 ridotto al solo testo delle diciture', fatti=fatti)
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc) + applica_2(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
