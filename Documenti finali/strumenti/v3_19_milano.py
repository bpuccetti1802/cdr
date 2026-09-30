# -*- coding: utf-8 -*-
"""v3.19 — le strutture ereditate dal sistema Side di Milano: allegati e dizionari.

Decisioni dell'utente, recepite qui: nomi **as is** (la convenzione di Milano si conserva, per
compatibilità); il file dell'allegato **dentro il database**, con la raccomandazione motivata
a favore di un archivio a oggetti; l'allegato legato alla **chiave dell'atto in SIPO**; i
dizionari **sostituiti** da quelli di Side; tutto in **ANSC_USR**.

⚠️ La convenzione di Milano è a prefissi come quella di Roma, ma con prefissi diversi:
`ty_` tipo · `ds_` descrizione · `nm_` nome · `oj_` oggetto · `cd_` codice · `fg_` flag ·
`ts_` timestamp · `dt_` data · `nr_` numero. Nello schema convivranno quindi due convenzioni,
ed è il prezzo dichiarato della compatibilità.

⚠️ Il DDL di origine è PostgreSQL: `bigserial`, `int8`, `int4`, `bytea`, `bpchar`, `text` non
esistono in Oracle 12.2. La traduzione dei tipi è inevitabile anche restando «as is» sui nomi.

⚠️ **Un difetto che la sostituzione dei dizionari porta con sé e che va dichiarato**: la
chiave primaria di `dominio_decodifica` è il solo `id_dominio`, ma nel corpus pubblicato due
identificativi corrispondono a due tabelle ciascuno — ANSC_134 e ANSC_135 — e il carico
completo violerebbe il vincolo. Sono 145 file su 143 identificativi.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.19.docx')

ALLEGATO = [
    ['Colonna', 'Tipo', 'Note'],
    ['id_allegato', 'NUMBER (PK)', 'Chiave tecnica (in origine bigserial).'],
    ['id_atto_sipo', 'NUMBER',
     'Chiave dell’atto in SIPO a cui il documento appartiene. ⚠️ È l’unico scostamento dal DDL '
     'di origine, dove la colonna si chiama id_evento e punta ad atti.evento: quella tabella '
     'non esiste in SIPO, e l’aggancio naturale è la chiave dell’atto. Senza vincolo di '
     'integrità, perché nessuna chiave esterna attraversa gli schemi.'],
    ['id_ansc_allegato', 'VARCHAR2(15)',
     'Identificativo assegnato da ANSC al documento dopo l’invio. ⚠️ È la colonna che rende '
     'realizzabile RF-17: senza di essa SIPO non saprebbe che cosa rileggere quando '
     'l’operatore vuole consultare un allegato.'],
    ['ty_allegato', 'VARCHAR2(10)', 'Tipo di documento secondo la decodifica ANSC_09.'],
    ['ds_tipo_allegato', 'VARCHAR2(250)',
     'Descrizione del tipo, conservata perché il mapping nomina gli allegati per descrizione e '
     'non per codice.'],
    ['ty_file', 'VARCHAR2(10)', 'Formato del file (decodifica ANSC_10).'],
    ['nm_file', 'VARCHAR2(250)', 'Nome del file come caricato dall’operatore.'],
    ['oj_allegato', 'BLOB',
     'Il documento. ⚠️ In origine è un bytea: il contenuto risiede nel database. Il paragrafo '
     'seguente motiva perché un archivio a oggetti sarebbe preferibile.'],
    ['cd_hash', 'VARCHAR2(250)',
     'Impronta del file: consente di accorgersi se il contenuto è cambiato e di riconoscere un '
     'documento già caricato.'],
    ['cd_stato', 'VARCHAR2(10)',
     'Stato del documento in ANSC (decodifica ANSC_08, cinque valori). ⚠️ Solo «Inserito» '
     'consente di proseguire: è l’esito della scansione antivirus, che non dipende da noi.'],
    ['fg_attestazione', 'CHAR(1)', '0/1: se il documento è un’attestazione.'],
    ['fg_incluso_att_conformita', 'CHAR(1)',
     '0/1: se il documento va incluso nell’attestazione di conformità. ⚠️ È il contrassegno che '
     'il mapping di ANSC non dichiara e che era rimasto aperto in OP-50: Side lo risolve '
     'rendendolo una scelta registrata sul singolo documento.'],
    ['ds_note_dt', 'VARCHAR2(50)', 'Note libere.'],
    ['cd_ope_ins_dt / ts_ins_dt', 'CHAR(6) / TIMESTAMP', 'Chi ha inserito e quando.'],
    ['cd_ope_ult_agg_dt / ts_ult_agg_dt', 'CHAR(6) / TIMESTAMP',
     'Chi ha aggiornato per ultimo e quando.'],
]

DOMINIO = [
    ['Colonna', 'Tipo', 'Note'],
    ['id_dominio', 'NUMBER (PK)',
     'Identificativo della decodifica come lo pubblica ANSC (es. 11 per gli stati dell’evento).'],
    ['nm_dominio', 'VARCHAR2(50)',
     'Nome della tabella restituito dal servizio (es. dec_stato_evento).'],
]

VALORE = [
    ['Colonna', 'Tipo', 'Note'],
    ['id_dominio', 'NUMBER (PK, FK)', 'Decodifica di appartenenza.'],
    ['id_valore', 'VARCHAR2(10) (PK)', 'Il valore codificato: insieme al dominio forma la chiave.'],
    ['ds_valore', 'CLOB',
     'Descrizione pubblicata. In origine è un text; la più lunga nel corpus attuale misura 245 '
     'caratteri, ma il tipo non pone limiti.'],
    ['dt_inizio_validita / dt_fine_validita', 'DATE',
     'Validità temporale come pubblicata da ANSC. ⚠️ Va applicata in lettura: i valori cessati '
     'restano, perché servono a interpretare gli atti già formati.'],
    ['nr_ordinamento', 'NUMBER', 'Ordine di presentazione suggerito da ANSC.'],
    ['cd_valore', 'VARCHAR2(10)', 'Codice alternativo, dove la decodifica ne prevede uno.'],
]

S3 = [
    'Il documento risiede nella colonna oj_allegato, cioè dentro la base dati. È la soluzione '
    'adottata da Side e si conserva per compatibilità, ma va detto che un archivio a oggetti '
    'sarebbe preferibile, e per ragioni che alla scala di Roma pesano.',

    '⚠️ **Il volume.** La ricognizione dei tipi atto conta 144.285 atti l’anno per le aree '
    'censite. Con uno o due documenti scansionati per atto, e una dimensione tipica fra uno e '
    'cinque megabyte, si tratta di centinaia di gigabyte l’anno dentro le tabelle. Un archivio '
    'a oggetti è costruito per questo; una base dati relazionale no, e lo paga nei tempi di '
    'salvataggio, nella dimensione dei backup e nella durata dei ripristini.',

    '⚠️ **La separazione dei cicli di vita.** I documenti hanno una conservazione propria, '
    'spesso più lunga di quella dei dati operativi e soggetta a regole diverse. Tenerli nella '
    'stessa tabella dell’atto significa che ogni politica di conservazione, ogni esportazione '
    'e ogni migrazione dovrà trattarli insieme, anche quando le regole divergono.',

    '⚠️ **L’accesso.** Un archivio a oggetti consente di servire il documento all’operatore '
    'senza che transiti dall’applicazione, con collegamenti a scadenza; con il contenuto in '
    'tabella ogni lettura passa dal componente e ne occupa memoria e banda.',

    'La raccomandazione è quindi di prevedere fin dall’inizio che oj_allegato possa essere '
    'sostituita da un riferimento all’archivio, lasciando invariato il resto della tabella: la '
    'differenza fra le due soluzioni è una colonna, e rimandare la scelta non costa nulla '
    'finché i volumi restano quelli del pilota. ⚠️ Diventa costosa dopo, quando i documenti '
    'già caricati andrebbero spostati.',
]

DUPLICATI = (
    '⚠️ Un vincolo del modello di origine va segnalato prima di adottarlo. La chiave primaria '
    'di dominio_decodifica è il solo id_dominio, ma nel corpus pubblicato da ANSC due '
    'identificativi corrispondono a due tabelle ciascuno: il 134 a dec_dichiarante_trascr_'
    'nascita e a dec_dichiarante_trascr_postuma, il 135 a due file che differiscono per un '
    'refuso nel nome. Sono 145 file per 143 identificativi distinti. Un carico completo '
    'violerebbe quindi la chiave primaria su due decodifiche, e il modello evento referenzia '
    'ANSC_134 in modo condizionato al caso d’uso. La correzione minima è aggiungere nm_dominio '
    'alla chiave; la si segnala qui perché la scelta di restare fedeli a Side non nasconda un '
    'difetto che si manifesta al primo caricamento completo.'
)

STORICO = (
    '⚠️ Il modello di Side non prevede lo storico dei caricamenti: non registra quando una '
    'decodifica è stata aggiornata, da chi, con quale esito e quante righe siano cambiate. '
    'L’operazione resta comunque tracciata nel registro di audit del componente, ma senza una '
    'vista propria: chi amministra non può rispondere a «quando abbiamo aggiornato l’ultima '
    'volta» guardando i dizionari. È una rinuncia accettata in nome della compatibilità, non '
    'una svista.'
)


DDL = """ALLEGATO
CREATE TABLE ANSC_USR.ALLEGATO (
  id_allegato          NUMBER GENERATED ALWAYS AS IDENTITY,
  id_atto_sipo         NUMBER             NOT NULL,
  id_ansc_allegato     VARCHAR2(15 CHAR),
  ty_allegato          VARCHAR2(10 CHAR),
  ds_tipo_allegato     VARCHAR2(250 CHAR),
  ty_file              VARCHAR2(10 CHAR),
  nm_file              VARCHAR2(250 CHAR),
  oj_allegato          BLOB,
  cd_hash              VARCHAR2(250 CHAR),
  cd_stato             VARCHAR2(10 CHAR),
  cd_ope_ins_dt        CHAR(6 CHAR)       NOT NULL,
  ts_ins_dt            TIMESTAMP          NOT NULL,
  cd_ope_ult_agg_dt    CHAR(6 CHAR),
  ts_ult_agg_dt        TIMESTAMP,
  ds_note_dt           VARCHAR2(50 CHAR),
  fg_attestazione      CHAR(1 CHAR),
  fg_incluso_att_conformita CHAR(1 CHAR),
  CONSTRAINT allegato_pk PRIMARY KEY (id_allegato),
  CONSTRAINT allegato_fg_attestazione_check CHECK (fg_attestazione IN ('0','1')),
  CONSTRAINT allegato_fg_incl_att_conf_check
    CHECK (fg_incluso_att_conformita IN ('0','1'))
) TABLESPACE ANSC_USR;
COMMENT ON TABLE ANSC_USR.ALLEGATO IS
  'Documenti allegati agli atti. Struttura ereditata dal sistema Side del Comune di Milano,
   con i nomi di origine; i tipi sono tradotti da PostgreSQL a Oracle.';
COMMENT ON COLUMN ANSC_USR.ALLEGATO.id_atto_sipo IS
  'Chiave dell atto in SIPO. Unico scostamento dall origine, dove la colonna e id_evento e
   referenzia atti.evento: quella tabella non esiste in SIPO.';
COMMENT ON COLUMN ANSC_USR.ALLEGATO.oj_allegato IS
  'Contenuto del documento. Si veda la raccomandazione sull uso di un archivio a oggetti.';
CREATE INDEX ANSC_USR.IX_ALLEGATO_ATTO ON ANSC_USR.ALLEGATO (id_atto_sipo);

DOMINIO_DECODIFICA
CREATE TABLE ANSC_USR.DOMINIO_DECODIFICA (
  id_dominio           NUMBER             NOT NULL,
  nm_dominio           VARCHAR2(50 CHAR)  NOT NULL,
  CONSTRAINT dominio_decodifica_pk PRIMARY KEY (id_dominio)
) TABLESPACE ANSC_USR;
COMMENT ON TABLE ANSC_USR.DOMINIO_DECODIFICA IS
  'Catalogo delle decodifiche ANSC replicate. Struttura ereditata da Side.
   ATTENZIONE: la chiave primaria sul solo id_dominio non regge i due identificativi che nel
   corpus pubblicato corrispondono a due tabelle ciascuno (134 e 135).';

VALORE_DOMINIO
CREATE TABLE ANSC_USR.VALORE_DOMINIO (
  id_dominio           NUMBER             NOT NULL,
  id_valore            VARCHAR2(10 CHAR)  NOT NULL,
  ds_valore            CLOB,
  dt_inizio_validita   DATE,
  dt_fine_validita     DATE,
  nr_ordinamento       NUMBER,
  cd_valore            VARCHAR2(10 CHAR),
  CONSTRAINT valore_dominio_pk PRIMARY KEY (id_dominio, id_valore),
  CONSTRAINT valore_dominio_tipo_dominio_fk
    FOREIGN KEY (id_dominio) REFERENCES ANSC_USR.DOMINIO_DECODIFICA (id_dominio)
) TABLESPACE ANSC_USR;
COMMENT ON COLUMN ANSC_USR.VALORE_DOMINIO.dt_fine_validita IS
  'La validita va applicata in lettura: i valori cessati restano perche servono a interpretare
   gli atti gia formati.';"""


def sostituisci_dizionari(doc):
    """Le tre tabelle nostre lasciano il posto alle due di Side."""
    fatti = []
    intro = next(p for p in doc.paragraphs
                 if p.text.strip().startswith('Le strutture sono tre, tutte nuove'))
    D.testo_di(intro,
               'Le strutture sono due, ereditate dal sistema Side del Comune di Milano e '
               'adottate con i nomi di origine, più una vista per la fruizione. Sostituiscono '
               'le tre tabelle previste dalle versioni precedenti di questo documento: la '
               'scelta è di compatibilità, perché il travaso da un sistema già in esercizio '
               'vale più dell’uniformità dei nomi con il resto dello schema.')
    fatti.append('introduzione del modello dati dei dizionari riscritta')

    # le tre tabelle vecchie: titolo + tabella
    for chiave, titolo, righe in (('ID_CATALOGO', 'DOMINIO_DECODIFICA — il catalogo delle '
                                   'decodifiche replicate.', DOMINIO),
                                  ('ID_VALORE', 'VALORE_DOMINIO — i valori di ciascuna '
                                   'decodifica.', VALORE)):
        t = D.tabella_colonne(doc, chiave)
        assert t is not None, f'tabella {chiave} non trovata'
        D.riscrivi_sicura(t, righe[1:])
        # il paragrafo che la introduce sta appena prima
        corpo = list(doc.element.body)
        i = corpo.index(t._tbl)
        for j in range(i - 1, max(0, i - 4), -1):
            if corpo[j].tag.endswith('}p'):
                from docx.text.paragraph import Paragraph
                p = Paragraph(corpo[j], doc)
                if p.text.strip().startswith('ANSC_DIZ_'):
                    D.testo_di(p, titolo)
                    break
        fatti.append(f'{chiave} → {titolo.split(" —")[0]}')

    # la terza tabella sparisce: il titolo diventa la nota sulla rinuncia
    t = D.tabella_colonne(doc, 'ID_CARICAMENTO')
    if t is not None:
        corpo = list(doc.element.body)
        i = corpo.index(t._tbl)
        from docx.text.paragraph import Paragraph
        for j in range(i - 1, max(0, i - 4), -1):
            if corpo[j].tag.endswith('}p'):
                p = Paragraph(corpo[j], doc)
                if p.text.strip().startswith('ANSC_DIZ_CARICAMENTO'):
                    D.testo_di(p, STORICO)
                    break
        if not D.ha_commenti(t._tbl):
            t._tbl.getparent().remove(t._tbl)
            fatti.append('ANSC_DIZ_CARICAMENTO rimossa; al suo posto la nota sulla rinuncia '
                         'allo storico dei caricamenti')
    return fatti


def aggiungi_allegato(doc):
    """La tabella operativa dei documenti, che al modello mancava del tutto."""
    fatti = []
    modello = D.trova_tabella(doc, 'Colonna', 'Tipo', 'Note')
    # va in coda alle tabelle operative, dopo ANSC_NOTIFICA
    t = D.tabella_colonne(doc, 'ID_NOTIFICA')
    assert t is not None, 'ANSC_NOTIFICA non trovata'
    corpo = list(doc.element.body)
    dopo = corpo[corpo.index(t._tbl) + 1]

    D.para(doc, dopo, 'ALLEGATO — i documenti allegati all’atto.')
    D.para(doc, dopo,
           'La tabella è ereditata dal sistema Side del Comune di Milano e adottata con i nomi '
           'di origine. Registra il documento vero e proprio, mentre ANSC_CFG_ALLEGATO dichiara '
           'quali documenti un caso d’uso richieda: le due non si sovrappongono, e finora al '
           'modello mancava la prima. ⚠️ Senza di essa SIPO non ha dove conservare un allegato: '
           'non esistono oggi, nell’area di stato civile, né il file né il suo stato.')
    D.tabella(doc, dopo, ALLEGATO, modello=modello)
    for testo in S3:
        D.para(doc, dopo, testo)
    fatti.append(f'ALLEGATO: {len(ALLEGATO) - 1} colonne + la raccomandazione '
                 f'sull’archivio a oggetti ({len(S3)} paragrafi)')
    return fatti


def aggiungi_ddl(doc):
    fatti = []
    ancora = next((p for p in doc.paragraphs
                   if p.text.strip().startswith('CREATE TABLE ANSC_USR.ANSC_DIZ_CATALOGO')), None)
    if ancora is None:
        ancora = next(p for p in doc.paragraphs
                      if p.text.strip().startswith('CREATE TABLE ANSC_USR.ANSC_NOTIFICA'))
    i = D.indice_di(doc, ancora)
    # si inserisce prima del blocco dei dizionari vecchi
    for riga in reversed(DDL.split('\n')):
        D.riga_dopo(doc, doc.paragraphs[i - 1], riga)
    fatti.append(f'App. A: DDL di ALLEGATO, DOMINIO_DECODIFICA e VALORE_DOMINIO '
                 f'({len(DDL.splitlines())} righe)')
    return fatti


def rimuovi_ddl_vecchi(doc):
    """I DDL delle tre tabelle sostituite."""
    import re
    fatti = []
    for nome in ('ANSC_DIZ_CATALOGO', 'ANSC_DIZ_VALORE', 'ANSC_DIZ_CARICAMENTO'):
        ps = doc.paragraphs
        inizio = next((i for i, p in enumerate(ps)
                       if re.match(rf'CREATE TABLE ANSC_USR\.{nome}\s*\(', p.text.strip())), None)
        if inizio is None:
            continue
        fine = inizio
        for j in range(inizio + 1, len(ps)):
            t = ps[j].text.strip()
            if t.startswith('CREATE TABLE') or (ps[j].style.name.startswith('Heading') and t):
                break
            fine = j
        testa = inizio - 1 if ps[inizio - 1].text.strip() == nome else inizio
        n = 0
        for p in ps[testa:fine + 1]:
            if D.ha_commenti(p._p):
                continue
            p._p.getparent().remove(p._p)
            n += 1
        fatti.append(f'rimosso il DDL di {nome} ({n} righe)')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    fatti = aggiungi_allegato(doc)
    fatti += sostituisci_dizionari(doc)
    # la nota sui duplicati sostituisce quella già presente, che diceva la stessa cosa
    # per un modello che aveva la chiave giusta
    vecchia = next((p for p in doc.paragraphs
                    if p.text.strip().startswith('Identificativi ripetuti.')), None)
    if vecchia is not None:
        D.testo_di(vecchia, DUPLICATI)
        fatti.append('nota sugli identificativi ripetuti riscritta per la chiave di Side')
    fatti += rimuovi_ddl_vecchi(doc)
    fatti += aggiungi_ddl(doc)
    for f in fatti:
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
