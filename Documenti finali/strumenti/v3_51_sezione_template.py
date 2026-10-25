# -*- coding: utf-8 -*-
"""v3.51 dell'analisi ANSC, dalla v3.50 dell'utente (25/10/2026).

La v3.50 (dell'utente) introduce ANSC_TEMPLATE e la colonna ANSC_CFG_UC.COD_QUERY_UC e toglie
ANSC_CFG_SEZIONE. Decisioni dell'utente per la v3.51:
  - la sezione sparisce dalle tabelle (troppo onerosa da gestire): resta su ANSC_CFG_CAMPO un
    campo descrittivo, SEZIONE_FE_ANSC, senza riferimenti a codici o tabelle;
  - COD_QUERY_UC e COD_LOGICA_DI_SCELTA sono concetti diversi e restano entrambi, con i
    riferimenti corretti alle rispettive tabelle.
Interventi:
  1. residui di ANSC_CFG_SEZIONE in testo, tabelle, DDL, back-office e figure;
  2. dominio 2 del catalogo delle logiche: non più «attivazione di sezione» ma la condizione di
     presenza di un documento, l'unico uso rimasto (ALLEGATI_USECASE.cd_logica);
  3. DDL: ANSC_CFG_UC (colonne doppie, refuso, FK verso ANSC_TEMPLATE), ANSC_CFG_CAMPO (FK e UK
     senza sezione, FK della baseline), ANSC_TEMPLATE (PK, UK, baseline, indice);
  4. nuova scheda «ANSC_TEMPLATE» nel capitolo delle tabelle di configurazione;
  5. §«Il processo di formazione dell'atto»: gli otto passi riscritti sulle quattro fasi;
  6. refusi e Storia (righe 3.50 e 3.51), frontespizio.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_51_sezione_template.py
"""
import copy
import os
import sys

import docx
from docx.text.paragraph import Paragraph

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.50.docx')
OUT = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.51.docx')
IMG = os.path.join(QUI, 'img')


# ------------------------------------------------------------------ primitive locali
def blocco(doc, titolo):
    """Elementi di una sezione individuata dal titolo ESATTO del suo heading."""
    out, dentro = [], False
    for el in doc.element.body.iterchildren():
        if el.tag.endswith('}p'):
            p = Paragraph(el, doc)
            if p.style.name.startswith('Heading'):
                if dentro:
                    break
                if p.text.strip() == titolo:
                    dentro = True
        if dentro:
            out.append(el)
    if not out:
        raise SystemExit('blocco non trovato: ' + titolo)
    return out


def par_in(doc, titolo, testo, inizia=False):
    """Il paragrafo del blocco con quel testo (esatto o iniziale): deve essere uno solo."""
    trovati = [Paragraph(el, doc) for el in blocco(doc, titolo) if el.tag.endswith('}p')]
    trovati = [p for p in trovati
               if (p.text.startswith(testo) if inizia else p.text == testo)]
    if len(trovati) != 1:
        raise SystemExit(f'«{testo[:50]}» in «{titolo}»: {len(trovati)} paragrafi')
    return trovati[0]


def par_doc(doc, inizio):
    trovati = [p for p in doc.paragraphs if p.text.startswith(inizio)]
    if len(trovati) != 1:
        raise SystemExit(f'«{inizio[:50]}»: {len(trovati)} paragrafi')
    return trovati[0]


def elimina(p):
    if D.ha_commenti(p._p):
        raise SystemExit('paragrafo commentato, non lo elimino: ' + p.text[:60])
    p._p.getparent().remove(p._p)


def righe_dopo(p, testi):
    """Righe di DDL nuove dopo p, clonando il paragrafo per ereditarne il carattere."""
    if D.ha_commenti(p._p):
        raise SystemExit('ancora commentata: ' + p.text[:60])
    for t in testi:
        p = D.riga_dopo(None, p, t)
    return p


def riga_tab_dopo(t, nome, valori):
    """Riga nuova in una tabella «Colonna | Tipo | Note», subito dopo la riga «nome»."""
    rif = next(r for r in t.rows if r.cells[0].text.strip() == nome)
    if D.ha_commenti(rif._tr):
        raise SystemExit('riga commentata: ' + nome)
    tr = copy.deepcopy(rif._tr)
    rif._tr.addnext(tr)
    nuova = next(r for r in t.rows if r._tr is tr)
    for cella, v in zip(nuova.cells, valori):
        D.riscrivi_cella(cella, v)
    return nuova


def riga_tab(t, nome):
    return next(r for r in t.rows if r.cells[0].text.strip() == nome)


# ------------------------------------------------------------------ 1-2. la sezione
def sezione_via(doc, fatti):
    S = lambda v, n, a=1: D.sostituisci(doc, v, n, attese=a, fatti=fatti)  # noqa: E731

    # elenco d'apertura del capitolo «Adeguamenti database»
    t = D.trova_tabella(doc, 'Oggetto', 'Ruolo', 'Note principali')
    r = riga_tab(t, 'ANSC_CFG_SEZIONE')
    if D.ha_commenti(r._tr):
        raise SystemExit('la riga di ANSC_CFG_SEZIONE porta un commento')
    t._tbl.remove(r._tr)
    rif = next(r for r in t.rows if r.cells[0].text.startswith('ANSC_CFG_UC —'))
    tr = copy.deepcopy(rif._tr)
    rif._tr.addnext(tr)
    nuova = next(r for r in t.rows if r._tr is tr)
    for cella, v in zip(nuova.cells, (
            'ANSC_TEMPLATE',
            'Interrogazioni da utilizzare per ciascun UC.',
            'Una riga per interrogazione e per baseline; ANSC_CFG_UC la richiama con '
            'COD_QUERY_UC. È un concetto distinto dalla logica di scelta, che decide se l’UC '
            'si applica all’atto.')):
        D.riscrivi_cella(cella, v)
    S('Struttura e meccanismo al paragrafo «Struttura e meccanismo della Configurazione»',
      'Struttura al paragrafo «Struttura dettagliata delle tabelle di configurazione»')
    S('scelta dell’UC (dominio 1) e attivazione delle sezioni (dominio 2).',
      'scelta dell’UC (dominio 1), presenza condizionata di un documento (dominio 2) e '
      'trasformazione dei campi (dominio 3).')

    # didascalia dell'ERD
    S('il codice dell’UC con cui ANSC_CFG_SEZIONE, ANSC_CFG_FORMULA, ALLEGATI_USECASE e '
      'SOGGETTI_USECASE richiamano ANSC_CFG_UC',
      'il codice dell’UC con cui ANSC_CFG_FORMULA, ALLEGATI_USECASE e SOGGETTI_USECASE '
      'richiamano ANSC_CFG_UC')

    # il catalogo delle logiche
    S('quale UC si applica a un atto, e quando una sezione del modello evento va popolata. '
      'In entrambi i casi la condizione',
      'quale UC si applica a un atto, quando un documento condizionato va richiesto e come si '
      'trasforma un valore letto da SIPO. In ogni caso la condizione')
    S('Il terzo dominio è la trasformazione di un valore — estrarre la data da una stringa, '
      'ricavarne l’ora, tradurre un codice — smette di essere un testo scritto dentro la riga '
      'del campo e diventa una voce del catalogo che i campi richiamano.',
      'Il secondo dominio è la condizione che rende obbligatorio un documento quando '
      'ALLEGATI_USECASE lo dichiara condizionato (ty_presenza C…). Il terzo è la '
      'trasformazione di un valore — estrarre la data da una stringa, ricavarne l’ora, '
      'tradurre un codice —: invece di essere un testo scritto dentro la riga del campo, è una '
      'voce del catalogo che i campi richiamano.')
    S('2 = logica di attivazione di una sezione',
      '2 = condizione di presenza di un documento (ALLEGATI_USECASE)')
    S('NASC_VIVO, NASC_MORTO, MATR_CAT, OBBLIGATORIA, OMISSIBILE, INTERPRETE.',
      'NASC_VIVO, NASC_MORTO, MATR_CAT per la scelta dell’UC; DATA_COMPLETA, ORA, MINUTI per i '
      'campi.')
    for inizio in ('Alcune logiche del secondo dominio non sono condizioni ma dichiarazioni',
                   'OBBLIGATORIA significa che la sezione si costruisce sempre',
                   'OPZIONALE che ANSC non la pretende',
                   'OMISSIBILE che la sezione si può omettere',
                   'Quest’ultima merita attenzione: è il modo in cui la configurazione'):
        elimina(par_doc(doc, inizio))
    fatti.append('catalogo delle logiche: tolte le dichiarazioni del dominio delle sezioni')

    # ANSC_CFG_UC: chi la richiama per valore
    S('sezioni, campi, formule, allegati e soggetti non lo richiamano con una chiave esterna',
      'campi, formule, allegati, soggetti e interrogazioni non lo richiamano con una chiave '
      'esterna')
    S('il riferimento con cui sezioni, campi, formule, allegati e soggetti richiamano l’UC',
      'il riferimento con cui campi, formule, allegati, soggetti e interrogazioni richiamano '
      'l’UC')

    # ANSC_CFG_CAMPO: la scheda
    t = D.tabella_colonne(doc, 'ID_CAMPO')
    for nome, tipo, nota in (
            ('ID_SEZIONE', 'VARCHAR2(200)',
             'SEZIONE_FE_ANSC: la sezione del mapping ufficiale e della web app di ANSC a cui '
             'il campo appartiene (Madre, Padre, Dichiarante, Soggetto intervenuto…), come la '
             'nomina il mapping. È un dato descrittivo: raggruppa i campi nelle pagine di '
             'configurazione e nei messaggi all’operatore, ma non richiama alcuna tabella né '
             'alcuna logica. Che un blocco serva a un atto lo dicono l’obbligatorietà dei suoi '
             'campi e, per le persone, i soggetti previsti dall’UC (SOGGETTI_USECASE).'),
            ('ID_VERSIONE', 'NUMBER (FK)',
             'Baseline di appartenenza (ANSC_CFG_VERSIONE). Con COD_UC_ANSC dice a quale UC e '
             'a quale baseline il campo appartiene, ed entra nella chiave di unicità.'),
            ('COD_UC_ANSC', 'VARCHAR2(20)',
             'Codice dell’UC pubblicato da ANSC: richiama ANSC_CFG_UC per valore insieme alla '
             'baseline, come ALLEGATI_USECASE e SOGGETTI_USECASE.'),
            ('CAMPO_ANSC', 'VARCHAR2(1000)', None),
            ('SCHEMA_SIPO', 'VARCHAR2(100)', None),
            ('TABELLA_SIPO', 'VARCHAR2(100)', None),
            ('CAMPO_SIPO', 'VARCHAR2(100)', None),
            ('VALORE_DEFAULT', 'VARCHAR2(100)', None)):
        r = riga_tab(t, nome)
        if nome == 'ID_SEZIONE':
            D.riscrivi_cella(r.cells[0], 'SEZIONE_FE_ANSC')
            nota = nota.split(': ', 1)[1]
            nota = nota[0].upper() + nota[1:]
        D.riscrivi_cella(r.cells[1], tipo)
        if nota:
            D.riscrivi_cella(r.cells[2], nota)
    fatti.append('scheda di ANSC_CFG_CAMPO: SEZIONE_FE_ANSC al posto di ID_SEZIONE, tipi '
                 'allineati alla DDL')

    # il flusso operativo, la verifica, i soggetti, la catena
    S('ANSC_CFG_SEZIONE per sapere quali blocchi servono, ANSC_CFG_CAMPO per i campi '
      'obbligatori', 'ANSC_CFG_CAMPO per i campi obbligatori')
    S('ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO, ANSC_CFG_FORMULA e i dizionari',
      'ANSC_CFG_CAMPO, ANSC_CFG_FORMULA e i dizionari')
    S('ANSC_CFG_UC, ANSC_CFG_SEZIONE e ANSC_CFG_CAMPO di ANSC_USR',
      'ANSC_CFG_UC e ANSC_CFG_CAMPO di ANSC_USR')
    p = par_doc(doc, 'Ne discende una sovrapposizione da governare, non da nascondere.')
    D.testo_di(p, 'Che una persona sia prevista dall’UC lo dice SOGGETTI_USECASE, con '
                  'ty_presenza. La configurazione dei campi non ha un livello di sezione con '
                  'una propria condizione di attivazione: la sezione del mapping vi resta come '
                  'dato descrittivo (SEZIONE_FE_ANSC). Ne discende che una persona prevista '
                  'dall’UC deve trovare in ANSC_CFG_CAMPO i campi del proprio blocco, e che il '
                  'raccordo delle righe passa per ty_soggetto, che nel file di Side coincide con '
                  'il nome del blocco del modello evento in 941 righe su 1.167 (OP-69).')
    fatti.append('«I soggetti previsti dall’UC»: tolta la sovrapposizione con la sezione')
    S('— ANSC_CFG_UC, ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO, ALLEGATI_USECASE e ANSC_CFG_FORMULA —',
      '— ANSC_CFG_UC, ANSC_TEMPLATE, ANSC_CFG_CAMPO, ALLEGATI_USECASE, SOGGETTI_USECASE e '
      'ANSC_CFG_FORMULA —')

    # back-office
    S('Configurazione (casi d’uso, sezioni, campi,', 'Configurazione (casi d’uso, campi,')
    S('configurazione dei casi d’uso e delle sezioni, campi, allegati e formule',
      'configurazione dei casi d’uso e dei loro campi, allegati e formule')
    S('le logiche dei tre domini — scelta dell’UC, attivazione di una sezione, trasformazione '
      'di un campo —', 'le logiche dei tre domini — scelta dell’UC, presenza condizionata di '
      'un documento, trasformazione di un campo —')
    S('⚠️ Non consente di riscrivere', 'Non consente di riscrivere')
    S('Configurazione — Sezioni, campi, allegati e formule per UC',
      'Configurazione — Campi, allegati e formule per UC')
    S('ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO, ALLEGATI_USECASE e ANSC_CFG_FORMULA per singolo UC: '
      'quali blocchi del modello evento si popolano e a quale condizione, da dove viene ogni '
      'dato', 'ANSC_CFG_CAMPO, ALLEGATI_USECASE e ANSC_CFG_FORMULA per singolo UC: da dove '
      'viene ogni dato e a quale sezione del mapping appartiene')
    S('Precompila dal foglio (sezioni, campi, allegati e formule insieme)',
      'Precompila dal foglio (campi, allegati e formule insieme)')
    S('Nelle schermate delle sezioni, degli allegati e delle formule',
      'Nelle schermate degli allegati e delle formule')
    S('Wireframe — Configurazione (Sezioni, campi, allegati e formule per UC): quattro schede '
      'per un solo UC', 'Wireframe — Configurazione (Campi, allegati e formule per UC): tre '
      'schede per un solo UC')

    # DDL del catalogo delle logiche
    S("  'Domini delle logiche decise dal Comune: 1 scelta dell UC, 2 attivazione di sezione.",
      "  'Domini delle logiche decise dal Comune: 1 scelta dell UC, 2 presenza di un "
      "documento, 3 campi.")
    S("   documento. Vuota per le logiche dichiarative (OBBLIGATORIA...).';",
      "   documento.';")


# ------------------------------------------------------------------ 3. DDL
def ddl(doc, fatti):
    # ANSC_CFG_UC
    T = 'ANSC_CFG_UC'
    elimina(par_in(doc, T, '  NUM_PRIORITA         NUMBER,'))
    elimina(par_in(doc, T, '  ID_VERSIONE          NUMBER,'))
    D.testo_di(par_in(doc, T, '  ID_TIPO_ATTO         NUMBER,        '),
               '  ID_TIPO_ATTO         NUMBER,')
    D.testo_di(par_in(doc, T, '  COD_QUERY_UC.        VARCHAR2 (20 char),'),
               '  COD_QUERY_UC         VARCHAR2(20 CHAR),')
    righe_dopo(par_in(doc, T, '   soddisfatta determina l UC. Due righe con la stessa '
                              'priorita sono una ambiguita.\';'), [
        'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.COD_QUERY_UC IS',
        "  'Interrogazione dell UC in ANSC_TEMPLATE, nella stessa baseline: la chiave esterna",
        "   e aggiunta dopo la creazione di ANSC_TEMPLATE. Distinta da COD_LOGICA_DI_SCELTA.';"])
    fatti.append('DDL ANSC_CFG_UC: tolte le dichiarazioni doppie di NUM_PRIORITA e '
                 'ID_VERSIONE, corretto COD_QUERY_UC, commento sulla colonna')

    # ANSC_CFG_CAMPO
    T = 'ANSC_CFG_CAMPO'
    D.testo_di(par_in(doc, T, '  ID_SEZIONE           \tNUMBER             NOT NULL,'),
               '  SEZIONE_FE_ANSC      \tVARCHAR2(200 CHAR),')
    D.testo_di(par_in(doc, T, '  ID_DECODIFICA_ANSC\t\tVARCHAR2 (10) NOT NULL,'),
               '  ID_DECODIFICA_ANSC\t\tNUMBER,')
    elimina(par_in(doc, T, '  CONSTRAINT FK_ANSC_CFG_CAMPO_SEZIONE'))
    elimina(par_in(doc, T, '    FOREIGN KEY (ID_SEZIONE, ID_VERSIONE, COD_UC_ANSC)'))
    elimina(par_in(doc, T, '    REFERENCES ANSC_USR.ANSC_CFG_SEZIONE (ID_SEZIONE, '
                           'ID_VERSIONE, COD_UC_ANSC),'))
    D.testo_di(par_in(doc, T, '  CONSTRAINT UK_ANSC_CFG_CAMPO UNIQUE (ID_SEZIONE,', True),
               '  CONSTRAINT FK_ANSC_CFG_CAMPO_VERSIONE\n'
               '    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE '
               '(ID_VERSIONE),\n'
               '  CONSTRAINT UK_ANSC_CFG_CAMPO\n'
               '    UNIQUE (ID_VERSIONE, COD_UC_ANSC, OGGETTO_ANSC, CAMPO_ANSC),\n'
               '  CONSTRAINT FK_ANSC_CFG_CAMPO_LOGICA\n'
               '    FOREIGN KEY (ID_DOMINIO, ID_BUSINESS_LOGIC)\n'
               '    REFERENCES ANSC_USR.LOGICHE_DI_SCELTA (ID_DOMINIO, COD_LOGICA_DI_SCELTA),')
    # l'indice su (ID_VERSIONE, COD_UC_ANSC) è ora il prefisso della chiave di unicità
    elimina(par_in(doc, T, 'CREATE INDEX ANSC_USR.IX_ANSC_CFG_CAMPO_UC'))
    elimina(par_in(doc, T, '  ON ANSC_USR.ANSC_CFG_CAMPO (ID_VERSIONE, COD_UC_ANSC) '
                           'TABLESPACE ANSC_USR;'))
    D.testo_di(par_in(doc, T, 'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.ID_SEZIONE IS'),
               'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.SEZIONE_FE_ANSC IS')
    D.testo_di(par_in(doc, T, "  'Sezione di appartenenza: porta l UC e la baseline", True),
               "  'Sezione del mapping ufficiale a cui il campo appartiene (Madre, Padre...):")
    D.testo_di(par_in(doc, T, '   esterna composta ne garantisce la coerenza.\';'),
               "   dato descrittivo, non richiama alcuna tabella ne alcuna logica.';")
    fatti.append('DDL ANSC_CFG_CAMPO: SEZIONE_FE_ANSC, FK della baseline, UK su baseline + UC '
                 '+ oggetto + campo, ID_DECODIFICA_ANSC NUMBER facoltativo, tolto l’indice '
                 'ridondante')

    # ANSC_TEMPLATE
    T = 'ANSC_TEMPLATE'
    D.testo_di(par_in(doc, T, 'Questa tabella contiene le informazioni relative alla query', True),
               'Questa tabella contiene le interrogazioni da utilizzare per ciascun UC; '
               'ANSC_CFG_UC le richiama con COD_QUERY_UC nella stessa baseline. La chiave '
               'esterna si aggiunge dopo la creazione della tabella, che nell’Appendice segue '
               'ANSC_CFG_UC.')
    D.testo_di(par_in(doc, T, '  ID_UC_CFG\t\t\tNUMBER NOT NULL,'),
               '  ID_VERSIONE          \tNUMBER             NOT NULL,')
    righe_dopo(par_in(doc, T, '  UTENTE_UPD           \tVARCHAR2(40 CHAR)'), [
        '  CONSTRAINT PK_ANSC_TEMPLATE PRIMARY KEY (ID_COD_QUERY),',
        '  CONSTRAINT UK_ANSC_TEMPLATE UNIQUE (ID_VERSIONE, COD_QUERY_UC),',
        '  CONSTRAINT FK_ANSC_TEMPLATE_VERSIONE',
        '    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE)'])
    D.testo_di(par_in(doc, T, '  UTENTE_UPD           \tVARCHAR2(40 CHAR)'),
               '  UTENTE_UPD           \tVARCHAR2(40 CHAR),')
    D.testo_di(par_in(doc, T, 'CREATE INDEX ANSC_TEMPLATE.IX_ANSC_TEMPLATE'),
               'CREATE INDEX ANSC_USR.IX_ANSC_TEMPLATE_UC')
    ultimo = par_in(doc, T, '  ON ANSC_USR.ANSC_CFG_CAMPO (ID_COD_QUERY) TABLESPACE ANSC_USR;')
    D.testo_di(ultimo, '  ON ANSC_USR.ANSC_TEMPLATE (ID_VERSIONE, COD_UC_ANSC) '
                       'TABLESPACE ANSC_USR;')
    righe_dopo(ultimo, [
        'ALTER TABLE ANSC_USR.ANSC_CFG_UC ADD CONSTRAINT FK_ANSC_CFG_UC_TEMPLATE',
        '  FOREIGN KEY (ID_VERSIONE, COD_QUERY_UC)',
        '  REFERENCES ANSC_USR.ANSC_TEMPLATE (ID_VERSIONE, COD_QUERY_UC);',
        'COMMENT ON TABLE ANSC_USR.ANSC_TEMPLATE IS',
        "  'Interrogazioni da utilizzare per ciascun UC, richiamate da ANSC_CFG_UC.COD_QUERY_UC",
        "   nella stessa baseline. Distinte dalla logica di scelta, che decide se l UC si applica.';",
        'COMMENT ON COLUMN ANSC_USR.ANSC_TEMPLATE.COD_UC_ANSC IS',
        "  'UC a cui l interrogazione e destinata: riferimento per valore, come in ALLEGATI_USECASE.';"])
    fatti.append('DDL ANSC_TEMPLATE: PK, UK (baseline + codice), ID_VERSIONE al posto di '
                 'ID_UC_CFG, indice corretto, FK da ANSC_CFG_UC con ALTER TABLE, commenti')


# ------------------------------------------------------------------ 4. le schede
def schede(doc, fatti):
    # ANSC_CFG_UC: le due colonne nuove
    t = D.tabella_colonne(doc, 'ID_UC_CFG')
    riga_tab_dopo(t, 'ID_CONF_TIPO_ATTO', (
        'ID_TIPO_ATTO', 'NUMBER',
        'Tipo atto di SIPO. [DA VERIFICARE: il rapporto con ID_CONF_TIPO_ATTO, che porta già il '
        'tipo atto di CONF_TIPO_ATTI ed è nella chiave di unicità: se le due colonne coincidono, '
        'ne resta una.]'))
    riga_tab_dopo(t, 'ID_DOMINIO / COD_LOGICA_DI_SCELTA', (
        'COD_QUERY_UC', 'VARCHAR2(20) (FK)',
        'L’interrogazione da utilizzare per l’UC, in ANSC_TEMPLATE: chiave esterna composta con '
        'ID_VERSIONE, così che la riga richiami soltanto un’interrogazione della propria '
        'baseline. È un concetto distinto dalla logica di scelta: quella decide se l’UC si '
        'applica all’atto, l’interrogazione è quella che si usa per l’UC. Vuota se l’UC non ne '
        'prevede una.'))
    fatti.append('scheda di ANSC_CFG_UC: ID_TIPO_ATTO e COD_QUERY_UC')

    # la determinazione dell'UC: la query non vi partecipa
    p = par_doc(doc, 'Il front-end chiede il completamento passando tre dati')
    D.testo_di(p, p.text + ' La riga porta anche l’interrogazione dell’UC (COD_QUERY_UC, in '
                           'ANSC_TEMPLATE), che non partecipa alla determinazione.')

    # la scheda di ANSC_TEMPLATE, in coda alle tabelle di configurazione
    modello = D.tabella_colonne(doc, 'ID_CAMPO')
    larghezze = [int(c.get(D.qn('w:w'))) / 1440
                 for c in modello._tbl.find(D.qn('w:tblGrid')).findall(D.qn('w:gridCol'))]
    prima = D.h(doc, 1, 'Il flusso operativo')._p
    D.para(doc, prima, 'ANSC_TEMPLATE — le interrogazioni associate agli UC.',
           stile='Heading 3')
    for testo in (
            'La tabella conserva le interrogazioni da utilizzare per ciascun UC. ANSC_CFG_UC le '
            'richiama per codice con la colonna COD_QUERY_UC.',
            'COD_QUERY_UC e COD_LOGICA_DI_SCELTA convivono sulla stessa riga di ANSC_CFG_UC ma '
            'esprimono due concetti diversi. La logica di scelta, presa dal catalogo delle '
            'logiche, stabilisce se l’UC si applica all’atto in lavorazione (si veda «La '
            'determinazione dell’UC»); l’interrogazione è quella da utilizzare per l’UC '
            '[DA VERIFICARE: in quale passo del flusso si esegue, con quali parametri in '
            'ingresso e che cosa restituisce].',
            'I riferimenti sono due e vanno in versi opposti. ANSC_CFG_UC richiama '
            'l’interrogazione con una chiave esterna composta, (ID_VERSIONE, COD_QUERY_UC), verso '
            'la chiave di unicità di ANSC_TEMPLATE: una riga di configurazione può richiamare '
            'soltanto un’interrogazione della propria baseline, e la stessa interrogazione può '
            'servire più righe dello stesso UC, una per ciascun Modello che lo raggiunge. '
            'ANSC_TEMPLATE nomina a sua volta l’UC per valore, con COD_UC_ANSC e ID_VERSIONE, '
            'come ALLEGATI_USECASE e SOGGETTI_USECASE. Che l’interrogazione richiamata da una '
            'riga sia destinata allo stesso UC della riga non lo garantisce un vincolo: lo '
            'verifica il controllo di attivazione della baseline.',
            'La tabella appartiene alla baseline: alla creazione di una nuova versione le '
            'interrogazioni si copiano con il resto della configurazione, e quelle di una '
            'baseline storica restano leggibili.'):
        D.para(doc, prima, testo)
    D.tabella(doc, prima, [
        ('Colonna', 'Tipo', 'Note'),
        ('ID_COD_QUERY', 'NUMBER (PK)', 'Chiave tecnica.'),
        ('COD_QUERY_UC', 'VARCHAR2(20)', 'Codice dell’interrogazione, unico dentro una baseline: '
                                         'è il valore che ANSC_CFG_UC.COD_QUERY_UC richiama.'),
        ('QUERY', 'CLOB', 'Il testo dell’interrogazione. Il linguaggio non è fissato dal presente '
                          'documento, come per le altre colonne di logica.'),
        ('COD_UC_ANSC', 'VARCHAR2(20)', 'UC a cui l’interrogazione è destinata: il codice '
                                        'pubblicato da ANSC, riferimento per valore.'),
        ('ID_VERSIONE', 'NUMBER (FK)', 'Baseline di appartenenza (ANSC_CFG_VERSIONE).'),
        ('DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
         'Campi tecnici di audit previsti dallo standard di nomenclatura [R5].'),
    ], modello, larghezze)
    D.para(doc, prima, 'Vincolo di unicità su (ID_VERSIONE, COD_QUERY_UC).')
    fatti.append('nuova scheda «ANSC_TEMPLATE — le interrogazioni associate agli UC»')


# ------------------------------------------------------------------ 5. il processo di formazione
FASI = [
    ('h', 'Fase A — I dati anagrafici e il dettaglio'),
    ('p', 'Il percorso comincia nel menu di SIPO, che per il momento rimane uguale: l’operatore '
          'sceglie il tipo di atto da formare — una dichiarazione di morte in abitazione, una '
          'nascita in costanza di matrimonio, una trascrizione. Il tipo atto è registrato in '
          'CONF_TIPO_ATTI e porta con sé il Modello di atto e la maschera di immissione: sono i '
          'due valori con cui la configurazione aggancia il lavoro dell’operatore e restringe i '
          'casi d’uso di ANSC candidati.'),
    ('p', 'La compilazione avviene nelle consuete maschere di SIPO, ed è la parte del percorso in '
          'cui il progetto interviene di meno. La differenza è nella pagina di dettaglio: qui si '
          'cercano i soggetti in ANSC con il servizio di consultazione (R005), interrogato con i '
          'dati anagrafici appena immessi, per recuperare il codice con cui ANSC identifica la '
          'persona e legare l’atto alla sua storia di stato civile. Per l’intestatario la ricerca '
          'è obbligatoria, il risultato no. Un soggetto non trovato non ferma l’atto, ma senza il '
          'suo codice gli automatismi di ANSC non scattano: il collegamento fra l’atto e la '
          'persona va stabilito con un’operazione a parte, che la nota di processo di ANSC '
          'definisce «fortemente sconsigliata», e da quel collegamento dipendono le annotazioni '
          'sugli atti collegati e la comunicazione all’ufficio anagrafe.'),
    ('p', 'Nella nascita l’intestatario è il neonato, che l’atto costituisce e che ANSC non '
          'conosce ancora: la ricerca utile riguarda i genitori. [DA VERIFICARE: come si applichi '
          'alla nascita l’obbligo di ricerca dell’intestatario.]'),
    ('p', 'La ricerca richiede il codice di sessione (token): l’ufficiale lo genera di persona '
          'sulla web app di ANSC, autenticandosi con smart card o SPID, e lo consegna a SIPO, che '
          'lo trasmette al concentratore. Vale quattro ore; SIPO deve perciò offrire un comando '
          'per acquisirlo e un timer che ne mostri la validità residua. Senza codice l’atto si '
          'compila per intero, ma non si supera la pagina di dettaglio.'),
    ('p', 'Nella stessa pagina si mostrano i dati che ANSC richiede e SIPO non prevede: finché '
          'mancano non si prosegue.'),
    ('h', 'Fase B — Il Riepilogo'),
    ('p', 'Il Riepilogo determina il caso d’uso: la configurazione valuta, sui dati ormai '
          'registrati, quale dei casi candidati corrisponde all’atto. La determinazione è '
          'automatica; la scelta dell’operatore è ammessa soltanto quando la configurazione è '
          'ambigua, e resta registrata come tale. Avviene qui, e non alla scelta del tipo atto, '
          'perché può dipendere da dati che l’operatore immette durante la compilazione.'),
    ('p', 'Determinato il caso d’uso si sa il resto, perché la configurazione lo dichiara per '
          'caso d’uso: chi firma, quali documenti vanno allegati, quali campi sono obbligatori. '
          'L’elenco dei documenti non è fisso: due atti che in SIPO appaiono identici possono '
          'richiedere certificati diversi — è quanto accade alla dichiarazione di nascita, dove '
          'il nato morto e il nato vivo poi deceduto richiedono due certificati medici '
          'differenti.'),
    ('p', 'I documenti si caricano qui e si conservano nella tabella ALLEGATO, accanto all’atto, '
          'secondo il processo adottato dal sistema Side (paragrafo «La gestione dei documenti: '
          'il processo di Side adottato in SIPO»); da lì si trasmettono ad ANSC con R001, che li '
          'sottopone a scansione antivirus. La scansione non è immediata: il documento assume uno '
          'stato che evolve e l’atto prosegue solo quando risulta acquisito, e la maschera deve '
          'dirlo all’operatore invece di sembrare bloccata. Il punto esatto dell’invio è aperto '
          '(OP-76). Oggi SIPO non gestisce documenti allegati agli atti di stato civile: le '
          'maschere sono da realizzare, adottando quelle di Side.'),
    ('p', 'Il Riepilogo si chiude con la verifica locale contro la configurazione: non chiama '
          'ANSC e non consuma identificativi nazionali, e serve a intercettare le mancanze prima '
          'del deposito, quando l’errore costerebbe di più.'),
    ('h', 'Fase C — L’Anteprima e «VALIDA»'),
    ('p', 'All’Anteprima si stacca il numero comunale definitivo dal servizio num-ansc-sipo; il '
          'componente costruisce il modello evento, prendendo ciascun valore dalla colonna di '
          'SIPO che la configurazione indica, e se serve ne mostra il testo con R010.'),
    ('p', 'Il pulsante «VALIDA» chiama R009, che deposita l’atto in ANSC nello stato CONFERMATO e '
          'gli assegna l’identificativo nazionale: da qui l’atto esiste in due luoghi. Se ANSC '
          'respinge i dati non resta nulla: l’operatore corregge e valida di nuovo, con lo stesso '
          'numero comunale.'),
    ('h', 'Fase D — Le firme e la definizione'),
    ('p', 'Seguono le firme: dei dichiaranti e degli altri firmatari, quando previste (R006 '
          'cartacea o R012 elettronica), poi l’attestazione di conformità dei documenti (R007, '
          'stato FIRMATO PER CONFORMITÀ) e infine la firma dell’ufficiale dello stato civile '
          '(R007, stato FIRMATO DA USC), che richiede le proprie credenziali di firma remota, '
          'distinte dal codice di sessione. Con «Definisci» l’atto passa in SIPO a DEFINITO e, '
          'se il caso d’uso la prevede, parte la comunicazione anagrafica (R014); «Chiudi» '
          'conclude la lavorazione.'),
    ('p', 'La firma dell’ufficiale è il punto di non ritorno. Non è una scelta del progetto ma '
          'una proprietà di ANSC: un atto firmato è un atto formato, e ciò che è formato non si '
          'modifica — si annota, si rettifica, si annulla, e ciascuno di questi è un procedimento '
          'con le proprie regole. Prima di quella firma l’operatore può ancora tornare ai dati: '
          'l’atto torna in bozza e si valida di nuovo lo stesso atto, con lo stesso '
          'identificativo nazionale; dopo le firme dei dichiaranti, solo se tutti possono firmare '
          'di nuovo (sezione «Le quattro fasi»).'),
]


def processo(doc, fatti):
    p = par_doc(doc, 'Due punti meritano attenzione fin da subito')
    D.testo_di(p, 'Due punti meritano attenzione fin da subito, perché non sono dettagli '
                  'realizzativi ma scelte che riguardano l’organizzazione del lavoro: il codice di '
                  'sessione va acquisito prima della pagina di dettaglio, perché la ricerca '
                  'dell’intestatario in ANSC è obbligatoria; e la firma dell’ufficiale chiude '
                  'l’atto, in conflitto con la prassi oggi in uso a Roma. Entrambi sono ripresi in '
                  'chiusura.')
    D.testo_di(D.h(doc, 3, 'Obiettivo lavorare in SIPO'),
               'Obiettivo: lavorare in SIPO, ANSC è la destinazione')
    D.testo_di(par_doc(doc, 'Su otto passi, quattro chiamano ANSC'),
               'Il percorso si articola in quattro fasi, che raggruppano le pagine del processo '
               'descritto nel capitolo «Il processo di gestione dei dati ANSC in SIPO», il '
               'riferimento per gli altri capitoli; che cosa ciascuna legga e scriva è nella '
               'sezione «Le quattro fasi». Qui il percorso si legge dal punto di vista '
               'dell’operatore.')

    testa = D.h(doc, 3, 'Il percorso in otto passi')
    D.testo_di(testa, 'Il percorso in quattro fasi')
    fine = D.h(doc, 4, 'Quando acquisire il token')._p
    el = testa._p.getnext()
    tolti = 0
    while el is not fine:
        succ = el.getnext()
        if D.ha_commenti(el):
            raise SystemExit('il percorso in otto passi porta un commento')
        el.getparent().remove(el)
        tolti += 1
        el = succ
    D.para(doc, fine, 'Le fasi seguono le pagine di SIPO. La figura del processo, con le '
                      'pagine, i servizi ANSC chiamati e i cambi di stato, è nel capitolo «Il '
                      'processo di gestione dei dati ANSC in SIPO».')
    for tipo, testo in FASI:
        D.para(doc, fine, testo, stile='Heading 4' if tipo == 'h' else 'Normal')

    D.testo_di(par_doc(doc, 'Il secondo passo è facoltativo e la sua conseguenza compare'),
               'Senza il codice di sessione l’atto si compila, ma la pagina di dettaglio non si '
               'supera, perché la ricerca dell’intestatario in ANSC è obbligatoria. Chi lo '
               'acquisisce solo quando serve interrompe la lavorazione a metà, spesso davanti '
               'al cittadino.')
    D.testo_di(par_doc(doc, 'La raccomandazione è quindi che l’acquisizione del token'),
               'La raccomandazione è quindi che l’acquisizione del token sia parte dell’apertura '
               'del lavoro: prima di cominciare, non quando serve. La maschera dovrebbe mostrarne '
               'in ogni momento la validità residua e chiedere un codice nuovo prima di una '
               'sequenza di chiamate che rischierebbe di scadere a metà.')
    D.sostituisci(doc, 'I campi che ANSC richiede e SIPO non prevede. Al passo 5 vanno chiesti '
                       'all’operatore:',
                  'I campi che ANSC richiede e SIPO non prevede. Vanno chiesti all’operatore '
                  'nella pagina di dettaglio:', attese=1)
    fatti.append(f'«Il processo di formazione dell’atto»: otto passi → quattro fasi '
                 f'({tolti} elementi sostituiti, figura degli otto passi tolta)')


# ------------------------------------------------------------------ 6. refusi e figure
def varie(doc, fatti):
    S = lambda v, n: D.sostituisci(doc, v, n, attese=1, fatti=fatti)  # noqa: E731
    S('è modificabile o eliminabile via R011 → ANNULLATO',
      'è modificabile o eliminabile via R011 [DA VERIFICARE: se lo stato che ne risulta sia 3 '
      'ANNULLATO o 9 CANCELLATO, che il contratto non dichiara]')
    S('Questa tipologia di atti potranno essere redatti', 'Questa tipologia di atti potrà '
      'essere redatta')

    D.sostituisci_immagine(doc, 'Schema ANSC_USR, con ALLEGATO', os.path.join(
        IMG, 'erd_ansc_usr.png'))
    D.sostituisci_immagine(doc, 'Dalla maschera SIPO al payload ANSC.', os.path.join(
        IMG, 'catena_configurazione.png'))
    D.sostituisci_immagine(doc, 'Wireframe — Configurazione (Campi, allegati e formule',
                           os.path.join(IMG, 'bo_config_campi.png'))
    fatti.append('figure rigenerate: schema ANSC_USR, catena della configurazione, '
                 'configurazione per UC')


def main():
    if os.path.exists(OUT):
        raise SystemExit('esiste già: ' + OUT)
    doc = docx.Document(SRC)
    fatti = []
    sezione_via(doc, fatti)
    ddl(doc, fatti)
    schede(doc, fatti)
    processo(doc, fatti)
    varie(doc, fatti)
    D.storia(doc, '25/10/2026', '3.50', 'Adeguamenti database · Appendice A',
             'Nuova tabella ANSC_TEMPLATE con le interrogazioni da utilizzare per ciascun UC, '
             'richiamate da ANSC_CFG_UC con la nuova colonna COD_QUERY_UC; aggiunta '
             'ID_TIPO_ATTO ad ANSC_CFG_UC. Tolta ANSC_CFG_SEZIONE, giudicata troppo onerosa da '
             'gestire.')
    D.storia(doc, '25/10/2026', '3.51',
             'Vincoli del contratto (Il processo di formazione dell’atto) · Adeguamenti database '
             '· Il flusso operativo · Costruzione del payload · Back-office · Modello dati (ERD) '
             '· Appendice A',
             'Completata la rimozione di ANSC_CFG_SEZIONE: la sezione resta su ANSC_CFG_CAMPO '
             'come dato descrittivo (SEZIONE_FE_ANSC), senza riferimenti a tabelle o logiche; '
             'chiave di unicità dei campi su baseline, UC, oggetto e campo. Il dominio 2 del '
             'catalogo delle logiche è la condizione di presenza di un documento. ANSC_TEMPLATE '
             'descritta e completata (chiave primaria, appartenenza alla baseline, chiave '
             'esterna da ANSC_CFG_UC.COD_QUERY_UC), distinta dalla logica di scelta; corrette '
             'nella DDL di ANSC_CFG_UC le colonne dichiarate due volte. Il processo di formazione '
             'dell’atto riscritto sulle quattro fasi del flusso operativo. Rigenerati lo schema '
             'ANSC_USR, la catena della configurazione e il wireframe della configurazione '
             'per UC.')
    for f in D.frontespizio(doc, '3.51', 'ANALISI_Integrazione-ANSC_v3.51'):
        fatti.append(f)
    doc.save(OUT)
    print('\n'.join('  · ' + f for f in fatti))
    print('scritto:', OUT)


if __name__ == '__main__':
    main()
