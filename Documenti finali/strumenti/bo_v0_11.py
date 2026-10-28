# -*- coding: utf-8 -*-
"""v0.11 del disegno del back-office, dalla v0.10 (28/10/2026).

Riallinea il back-office all'analisi v3.53 e alle decisioni dell'utente del 28/10/2026:

  - il servizio della numerazione è be-numeratore-comunale e le sue operazioni sono le quattro
    descritte nell'analisi (POST /richiesta, GET /ricerca, PUT /utilizza, PUT /scarta, base
    /api/v1/numerazione-comunale); ciò che non coprono si dichiara mancante (OP-79);
  - colonne temporali: DATA_ per le DATE, TS_ per le TIMESTAMP;
  - ANSC_CFG_UC senza vincolo di unicità, legata al tipo atto (ID_TIPO_ATTO), senza Modello né
    maschera, con il catalogo degli UC nelle stesse righe (ANSC_ANA_UC non esiste più);
  - TIPO_LOGICHE_DI_SCELTA e LOGICHE_DI_SCELTA deprecate: la pagina «Logiche di scelta» si
    toglie, le logiche sono codici liberi;
  - ANSC_CFG_SEZIONE non esiste; ANSC_CFG_CAMPO porta l'alias SIPO, compilato a mano;
  - ANSC_STATO_ATTO senza versione, esito qualificato ed emergenza vecchia; NUMERO_ATTO;
  - la numerazione senza registro e senza sequence (NUMERATORE_COMUNALE).

Figure: pagine_bo_v6.py, in img/bo_v0_11.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/bo_v0_11.py
"""
import copy
import os
import re
import sys

import docx

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'DISEGNO_Back-Office_ANSC_v0.10.docx')
OUT = os.path.join(BASE, 'DISEGNO_Back-Office_ANSC_v0.11.docx')
IMG = os.path.join(QUI, 'img', 'bo_v0_11')


# ───────────────────────────────────────────────────────────── primitive locali
def _storia(doc):
    return D.trova_tabella(doc, 'versione', 'sintesi dei cambiamenti')._tbl


def _paragrafi(doc):
    st = _storia(doc)
    yield from doc.paragraphs
    for t in doc.tables:
        if t._tbl is st:
            continue
        for r in t.rows:
            for c in r.cells:
                yield from c.paragraphs


def sost(doc, vecchio, nuovo, attese=1):
    """Sostituzione nel corpo e nelle tabelle (esclusa la Storia), con occorrenze attese."""
    n, visti = 0, {}
    for p in _paragrafi(doc):
        if id(p._p) in visti or vecchio not in p.text:
            continue
        visti[id(p._p)] = p._p   # il riferimento impedisce il riuso dell'id
        for r in p.runs:
            if vecchio in r.text:
                r.text = r.text.replace(vecchio, nuovo)
                break
        else:
            D.testo_di(p, p.text.replace(vecchio, nuovo))
        n += 1
    if n != attese:
        raise SystemExit(f'«{vecchio[:70]}»: attese {attese}, trovate {n}')


def via(elemento):
    if D.ha_commenti(elemento):
        raise SystemExit('elemento con commento da eliminare')
    elemento.getparent().remove(elemento)


def righe(doc, primo, contiene=None):
    """Le righe (di tutte le tabelle, Storia esclusa) con la prima cella uguale a `primo`."""
    st = _storia(doc)
    out = []
    for t in doc.tables:
        if t._tbl is st:
            continue
        for r in t.rows:
            if r.cells[0].text.strip() != primo:
                continue
            if contiene and not any(contiene in c.text for c in r.cells):
                continue
            out.append(r)
    return out


def riga(doc, primo, contiene=None):
    trovate = righe(doc, primo, contiene)
    if len(trovate) != 1:
        raise SystemExit(f'riga «{primo}» / «{contiene}»: {len(trovate)}')
    return trovate[0]


def scrivi(r, valori):
    for c, v in zip(r.cells, valori):
        if v is not None and c.text != v:
            D.riscrivi_cella(c, v)


def via_riga(doc, primo, contiene=None):
    via(riga(doc, primo, contiene)._tr)


def riga_dopo(r, valori):
    nuovo = copy.deepcopy(r._tr)
    r._tr.addnext(nuovo)
    from docx.table import _Row
    nr = _Row(nuovo, r._parent)
    for c, v in zip(nr.cells, valori):
        D.riscrivi_cella(c, v)
    return nr


def par(doc, inizio):
    trovati = [p for p in doc.paragraphs if p.text.strip().startswith(inizio)]
    if len(trovati) != 1:
        raise SystemExit(f'«{inizio[:60]}»: {len(trovati)} paragrafi')
    return trovati[0]


# ───────────────────────────────────────────────────────────── 1. cornice e contesto
def cornice(doc):
    scrivi(riga(doc, 'Modello', 'struttura del Comune di Roma'),
           ('Tipo atto', 'La struttura del Comune di Roma (CONF_TIPO_ATTI) che si lega a uno o '
                         'più UC: nella configurazione è ANSC_CFG_UC.ID_TIPO_ATTO.'))
    scrivi(riga(doc, 'Logica di scelta'),
           (None, 'Un codice libero, valutato dal codice applicativo sui dati dell’atto già '
                  'salvato in SIPO: sceglie l’UC fra quelli del tipo atto o condiziona la '
                  'presenza di un documento. Non ha un catalogo.'))
    sost(doc, 'ANALISI_Integrazione-ANSC_v3.40.docx', 'ANALISI_Integrazione-ANSC_v3.54.docx')
    sost(doc, 'SPEC_API_Integrazione-ANSC_v0.2.docx e i contratti OpenAPI dei quattro pod',
         'SPEC_API_Integrazione-ANSC_v0.4.docx e i contratti OpenAPI dei quattro componenti, '
         'compreso quello del servizio be-numeratore-comunale')

    sost(doc, 'per governare le ventuno tabelle già progettate nell’analisi dell’integrazione; '
              'il criterio di completezza è che ciascuna di quelle tabelle abbia almeno una '
              'pagina che la governi, e il capitolo «La copertura del modello dati» lo verifica '
              'riga per riga.',
         'per governare le ventidue tabelle già progettate nell’analisi dell’integrazione; il '
         'criterio di completezza è che ciascuna di quelle tabelle abbia almeno una pagina che '
         'la governi, e il capitolo «La copertura del modello dati» lo verifica riga per riga, '
         'dichiarando quelle che una pagina ancora non l’hanno.')
    sost(doc, 'da cui vengono le ventuno tabelle', 'da cui vengono le ventidue tabelle')

    sost(doc, 'UC elenco e dettaglio · Catalogo · Logiche · Dizionari',
         'UC elenco e dettaglio · Catalogo · Dizionari')
    sost(doc, 'Quattordici catene di costruzione, quattordici artefatti da versionare, '
              'quattordici manifesti',
         'Diciannove catene di costruzione, diciannove artefatti da versionare, diciannove '
         'manifesti')
    sost(doc, 'Un back-office di venti pagine', 'Un back-office di diciannove pagine')
    sost(doc, 'L’applicazione è stata pensata con venti pagine distribuite su quattro aree '
              'funzionali, cui si aggiunge una ventunesima pagina',
         'L’applicazione è stata pensata con diciannove pagine distribuite su quattro aree '
         'funzionali, cui si aggiunge una ventesima pagina')
    sost(doc, 'Configurazione UC (elenco e dettaglio) · Catalogo UC · Logiche di scelta · '
              'Dizionari',
         'Configurazione UC (elenco e dettaglio) · Catalogo UC · Dizionari')
    sost(doc, 'Seguono le venti pagine', 'Seguono le diciannove pagine')
    sost(doc, 'ripeterle in venti sezioni', 'ripeterle in diciannove sezioni')
    sost(doc, 'Spunta o croce accanto al nome della sezione nel dettaglio dell’atto.',
         'Spunta o croce accanto al nome dell’oggetto del modello evento nel dettaglio '
         'dell’atto.')
    sost(doc, 'Qui però non si compila: si legge perché una sezione è incompleta.',
         'Qui però non si compila: si legge perché un oggetto è incompleto.')
    # marcature di versione
    sost(doc, 'Chiuso in questa versione. ', 'Chiuso. ', attese=5)
    sost(doc, 'la pagina rientra ed è descritta in questa versione,',
         'la pagina rientra ed è descritta in questo documento,')
    sost(doc, ', che la versione precedente di questo documento dava per presenti.', '.')
    # una marcatura di versione dentro una cella
    sost(doc, 'del percorso di firma. ⚠️ Nella v0.7 il valore era proposto dalla '
              'configurazione: non lo è più [R1].',
         'del percorso di firma [R1].')


# ───────────────────────────────────────────────────────────── 2. area operativa
def operativa(doc):
    # Supervisione atti
    sost(doc, 'La colonna «Stato» porta il valore di ANSC. È una replica di un dato altrui e il '
              'vincolo tabellare ne ammette dodici valori: gli undici pubblicati da ANSC più '
              'quello iniziale, che è nostro.',
         'La colonna «Stato» porta il valore di ANSC: codice e descrizione della decodifica '
         'ANSC_11 (ID_STATO e STATO). È una replica di un dato altrui; prima della validazione '
         'l’atto in ANSC non esiste, e la colonna lo dice.')
    scrivi(riga(doc, 'ANSC_STATO_ATTO', 'È la tabella dell’elenco'),
           (None, None, 'È la tabella dell’elenco. Le colonne mostrate sono ID_ATTO_SIPO, '
                        'ID_TIPO_EVENTO, ID_UC_ANSC, COD_FASE, ID_STATO e STATO, ID_ANSC, '
                        'NUMERO_ATTO, UTENTE_UPD; i filtri agiscono su queste più '
                        'COD_MUNICIPIO, FLG_EMERGENZA e TS_UPD.'))
    sost(doc, 'proviene da ANSC_STATO_ATTO.ULTIMO_ERRORE; il dettaglio completo sta '
              'nell’audit.',
         'proviene da ANSC_STATO_ATTO.ULTIMO_ERRORE; lo scarto in validazione e l’esito '
         'indeterminato si leggono dall’esito dell’ultima chiamata registrata, e il dettaglio '
         'completo sta nell’audit.')
    sost(doc, 'I dodici valori ammessi dal vincolo di ANSC_STATO_ATTO.',
         'Gli stati della decodifica ANSC_11, da ID_STATO.')
    sost(doc, 'Vista derivata da fase, stato ed esito.',
         'Vista derivata da fase, stato ed esito dell’ultima chiamata registrata nell’audit.')
    sost(doc, 'usando MASCHERA_UI della configurazione',
         'usando la maschera che SIPO associa al tipo atto (CONF_TIPO_ATTI.MASCHERA_UI)')

    # Dettaglio dell’atto
    sost(doc, 'lo stato di completezza sezione per sezione',
         'lo stato di completezza per oggetto del modello evento')
    sost(doc, 'e il payload che è stato depositato.', 'e il modello evento che è stato '
                                                     'depositato.')
    sost(doc, 'La riga di sezioni con spunta e croce è ripresa da S.I.De.',
         'La riga di oggetti con spunta e croce riprende le sezioni di S.I.De.')
    sost(doc, 'accanto alla sezione in errore compare', 'accanto all’oggetto in errore compare')
    sost(doc, 'La scheda «Payload inviato» merita una nota. Il payload è conservato',
         'La scheda «Modello evento inviato» merita una nota. Il modello evento è conservato')
    sost(doc, 'Letto insieme a ID_VERSIONE dice che cosa è stato inviato e con quale '
              'configurazione.',
         'L’atto non registra la versione della configurazione: quella con cui è stato '
         'costruito si ricava confrontando l’istante della validazione (TS_VALIDAZIONE) con le '
         'date di attivazione delle versioni.')
    scrivi(riga(doc, 'ANSC_STATO_ATTO', 'Lo scenario in testa'),
           (None, None, 'Lo scenario in testa (ID_TIPO_EVENTO, ID_MODELLO_ATTO, NUMERO_ATTO, '
                        'ID_UC_ANSC, COD_ORIGINE_UC, ID_STATO e STATO) e il modello evento '
                        'inviato (TXT_EVENTO). Le azioni di ripresa aggiornano COD_FASE e '
                        'COD_PAGINA_RIPRESA; la riconciliazione aggiorna ID_STATO e STATO.'))
    sost(doc, 'La cronologia: FASE, servizio, ESITO, DURATA_MS, OPERATORE, DATA.',
         'La cronologia: FASE, servizio, ESITO, DURATA_MS, OPERATORE, TS_REGISTRAZIONE.')
    scrivi(riga(doc, 'ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO'),
           ('ANSC_CFG_CAMPO', 'Lettura', 'I campi obbligatori dell’UC nella versione attiva, '
                                         'raggruppati per oggetto del modello evento '
                                         '(OGGETTO_ANSC): è ciò che produce la spunta o la '
                                         'croce.'))
    scrivi(riga(doc, 'Sezioni', 'Accordion'),
           ('Campi per oggetto', 'Accordion',
            'Una riga per oggetto del modello evento fra i campi dell’UC, nell’ordine di '
            'ORDINAMENTO. Spunta se tutti i campi obbligatori sono valorizzati, croce '
            'altrimenti. All’apertura elenca i campi con l’alias SIPO (ALIAS_CAMPO_SIPO) e il '
            'valore corrente.'))
    scrivi(riga(doc, 'SCARICA PAYLOAD'),
           ('SCARICA MODELLO EVENTO', None,
            'Restituisce TXT_EVENTO come file. Utile al fornitore in diagnosi.'))
    sost(doc, 'Scrive FLG_EMERGENZA, ID_ATTO_EMERGENZA, COD_MOTIVO_RECUPERO e '
              'DATA_INGRESSO_EMERGENZA.',
         'Scrive FLG_EMERGENZA, ID_ATTO_CARTACEO, ID_MOTIVO_RECUPERO e COD_MOTIVO_RECUPERO.')

    # Identificativi dei soggetti, notifiche
    sost(doc, 'DATA_RICERCA', 'TS_RICERCA', attese=2)
    sost(doc, 'DATA_NOTIFICA', 'TS_NOTIFICA')
    sost(doc, 'DATA_ESITO', 'TS_ESITO')


# ───────────────────────────────────────────────────────────── 3. configurazione
def configurazione(doc):
    # elenco degli UC
    p = par(doc, 'Da qui si governa quali casi d’uso il Comune adotta')
    D.testo_di(p, 'Da qui si governa quali casi d’uso il Comune adotta e come li aggancia alle '
                  'proprie strutture: ogni riga lega un UC a un tipo atto di SIPO '
                  '(ID_TIPO_ATTO). È la pagina in cui il lato ANSC e il lato Comune si '
                  'incontrano.')
    sost(doc, 'È la conseguenza della scelta di determinare l’UC con espressioni sui dati '
              'anziché con regole dichiarative',
         'È la conseguenza della scelta di determinare l’UC con logiche valutate dal codice '
         'applicativo anziché con regole dichiarative')
    p = par(doc, 'La colonna «Priorità» permette di gestire la scelta')
    D.riga_dopo(None, p, 'La tabella non ha vincolo di unicità. Che uno stesso tipo atto non '
                         'leghi due volte lo stesso UC nella stessa versione lo controlla la '
                         'pagina al salvataggio, e lo segnala invece di lasciarlo passare in '
                         'silenzio.')
    scrivi(riga(doc, 'ANSC_CFG_UC', 'COD_UC_ANSC, DESCRIZIONE, ID_MODELLO_ATTO'),
           (None, None, 'L’elenco: COD_UC_ANSC, DESC_UC_ANSC, ID_TIPO_ATTO, ID_CONF_TIPO_ATTO, '
                        'NUM_PRIORITA, LOGICA_DI_SCELTA, COD_QUERY_UC, STATO, '
                        'DATA_INIZIO_VALIDITA e DATA_FINE_VALIDITA. Filtrata per ID_VERSIONE. '
                        'La fine validità segnala un UC adottato che ANSC ha nel frattempo '
                        'ritirato.'))
    via_riga(doc, 'ANSC_ANA_UC', 'Serve a segnalare un UC adottato')
    sost(doc, 'Prepara nella bozza sezioni, campi, allegati e formule a partire dal mapping '
              'ufficiale. I soggetti no: il mapping non ne dichiara i ruoli, e si caricano da '
              'file. Riscrive solo le righe che nessuno ha ancora esaminato; per le altre '
              'produce un elenco di scostamenti.',
         'Prepara nella bozza campi, allegati e formule a partire dal mapping ufficiale. I '
         'soggetti no: il mapping non ne dichiara i ruoli, e si caricano da file. Sulle '
         'formule, che registrano l’origine di ogni riga, riscrive solo le righe che nessuno '
         'ha ancora esaminato e per le altre produce un elenco di scostamenti; campi e allegati '
         'non registrano l’origine, e come distinguere le righe già esaminate resta da '
         'decidere (OP-65 dell’analisi).')
    sost(doc, 'Adotta un caso d’uso presente nel catalogo di ANSC ma non ancora configurato.',
         'Adotta un caso d’uso del catalogo per un tipo atto: valorizza ID_TIPO_ATTO.')

    # dettaglio dell'UC
    sost(doc, 'poche sezioni, decine di campi, pochi allegati e soggetti, alcune formule',
         'decine di campi, pochi allegati e soggetti, alcune formule')
    p = par(doc, 'La scheda «Campi» è la più densa')
    D.testo_di(p, 'La scheda «Campi» è la più densa e la si è disegnata come area di revisione: '
                  'l’importazione porta le righe dal mapping ufficiale e il funzionario compila '
                  'a mano l’alias SIPO di ciascun campo. Il filtro «Senza alias SIPO» è quello '
                  'che ordina il lavoro, perché è esattamente l’elenco di ciò che manca. La '
                  'tabella dei campi non ha chiavi esterne né vincolo di unicità, per scelta: '
                  'un campo ripetuto nello stesso UC e nella stessa versione lo segnala la '
                  'pagina al salvataggio.')
    scrivi(riga(doc, 'ANSC_CFG_CAMPO', 'Scheda «Campi»'),
           (None, None, 'Scheda «Campi»: OGGETTO_ANSC, CAMPO_ANSC, FLG_OBBLIGATORIO, '
                        'OBBLIGATORIETA_EVENTO, ALIAS_CAMPO_SIPO, ID_DECODIFICA_ANSC, '
                        'ORDINAMENTO, OPERATIVO. Filtrata per ID_VERSIONE e COD_UC_ANSC.'))
    scrivi(riga(doc, 'ANSC_CFG_SEZIONE', 'Scheda «Sezioni»'),
           ('ANSC_CFG_UC, ANSC_TEMPLATE', 'Lettura e scrittura',
            'Scheda «Dati generali»: il tipo atto, la priorità, la logica di scelta e '
            'l’interrogazione richiamata da COD_QUERY_UC, con il suo testo (ANSC_TEMPLATE.QUERY) '
            'nella stessa versione. In quale passo del flusso l’interrogazione si esegua resta '
            'da stabilire nell’analisi.'))
    scrivi(riga(doc, 'Sezione', 'Restringe i campi'),
           ('Oggetto', None, 'Restringe i campi a un oggetto del modello evento (OGGETTO_ANSC). '
                             'Con oltre ottanta campi per UC è il filtro che rende la pagina '
                             'praticabile.'))
    scrivi(riga(doc, 'Senza corrispondenza SIPO'),
           ('Senza alias SIPO', None, 'Isola le righe con ALIAS_CAMPO_SIPO vuoto. È la coda di '
                                      'lavoro del funzionario.'))
    r = riga(doc, 'Logica', 'La logica di campo')
    scrivi(r, ('Obblig. evento', 'Colonna',
               'OBBLIGATORIETA_EVENTO. Che cosa la colonna debba contenere si stabilisce in '
               'analisi [DA VERIFICARE].'))
    riga_dopo(r, ('Decodifica · Operativo', 'Colonne',
                  'ID_DECODIFICA_ANSC è il dizionario ANSC del campo: la traduzione del valore '
                  'passa dalla riconciliazione. OPERATIVO vale 0 o 1 e dice se la riga partecipa '
                  'alla costruzione del modello evento.'))
    scrivi(riga(doc, 'REIMPORTA SEZIONE'),
           ('REIMPORTA OGGETTO', None, 'Riporta dal mapping le sole righe dell’oggetto '
                                       'selezionato, con l’elenco degli scostamenti.'))

    # allegati, soggetti e caricamento da file
    sost(doc, 'la condizione, presa dal catalogo delle logiche quando la presenza è '
              'condizionata.',
         'la condizione, quando la presenza è condizionata: un codice di logica libero '
         '(cd_logica), senza catalogo, valutato dal codice applicativo.')
    sost(doc, 'ty_configurazione, id_dominio e cd_logica, nr_ordinamento',
         'ty_configurazione, cd_logica, nr_ordinamento')
    scrivi(riga(doc, 'ANSC_ANA_UC', 'il legame è per valore'), ('ANSC_CFG_UC', None, None))
    scrivi(riga(doc, 'ANSC_ANA_UC', 'Come nella pagina degli allegati'),
           ('ANSC_CFG_UC', None, None))
    sost(doc, 'ed è quindi il raccordo naturale con le sezioni della configurazione.',
         'ed è quindi il raccordo naturale con gli oggetti del modello evento nella '
         'configurazione dei campi (OGGETTO_ANSC).')
    scrivi(riga(doc, 'ANSC_CFG_SEZIONE', 'OP-69'),
           ('ANSC_CFG_CAMPO', None, 'Segnala il soggetto il cui blocco del modello evento non '
                                    'ha campi configurati nell’UC, e viceversa: è la '
                                    'sovrapposizione fra le due tabelle che l’analisi chiede '
                                    'di governare (OP-69).'))
    sost(doc, '(ds_allegato, id_dominio, cd_logica)', '(ds_allegato, cd_logica)')
    scrivi(riga(doc, 'ANSC_ANA_UC, VALORE_DOMINIO'), ('ANSC_CFG_UC, VALORE_DOMINIO', None,
                                                     None))

    # catalogo
    sost(doc, 'e perché serve un luogo dove verificare che un UC adottato sia ancora valido.',
         'e perché serve un luogo dove verificare che un UC adottato sia ancora valido. Il '
         'catalogo non ha una tabella propria: sta nelle righe di ANSC_CFG_UC, e un UC che '
         'nessun tipo atto raggiunge ancora è una riga senza ID_TIPO_ATTO. Per questo il '
         'catalogo appartiene alla versione della configurazione.')
    scrivi(riga(doc, 'ANSC_CFG_UC', 'La colonna «Adottato»'),
           (None, None, 'La colonna «Adottato» dice se per quel codice esiste, nella stessa '
                        'versione, una riga legata a un tipo atto (ID_TIPO_ATTO valorizzato).'))
    scrivi(riga(doc, 'ANSC_ANA_UC', 'COD_MOTORE'),
           ('ANSC_CFG_UC', None, 'COD_UC_ANSC, COD_MOTORE, DESC_UC_ANSC, COD_FAMIGLIA, '
                                 'ID_TIPO_CONTENUTO, DATA_INIZIO_VALIDITA, DATA_FINE_VALIDITA, '
                                 'nella versione scelta.'))
    scrivi(riga(doc, 'AGGIORNA DA ANSC'),
           (None, None, 'Ricarica nella versione in bozza le colonne del catalogo — codice, '
                        'codice motore, descrizione, famiglia, validità — senza toccare i '
                        'legami con i tipi atto, le priorità e le logiche, che sono scelte del '
                        'Comune.'))

    # la pagina delle logiche di scelta, deprecate
    elementi = D.sezione(doc, 'Logiche di scelta', livello=2)
    assert elementi and len(elementi) > 5, 'sezione delle logiche non trovata'
    for el in elementi:
        via(el)
    for primo in ('LOGICHE_DI_SCELTA', 'TIPO_LOGICHE_DI_SCELTA'):
        for r in righe(doc, primo):
            via(r._tr)

    # riconciliazione
    sost(doc, 'La tabella SIPO di riferimento diventa un dato. Nella stesura precedente il '
              'filtro «Tabella SIPO» non poggiava su alcuna colonna: era un criterio che la '
              'pagina offriva e che il modello non sapeva sostenere. RICONCILIAZ_DIZIONARI '
              'acquisisce quindi SCHEMA_SIPO, TABELLA_SIPO e CAMPO_SIPO, con gli stessi nomi '
              'già usati da ANSC_CFG_CAMPO.',
         'La tabella SIPO di riferimento è un dato, e il filtro «Tabella SIPO» poggia su '
         'colonne vere: RICONCILIAZ_DIZIONARI porta SCHEMA_SIPO, TABELLA_SIPO e CAMPO_SIPO.')
    sost(doc, 'È stato accettato perché rende la corrispondenza verificabile sul dato reale, e '
              'perché è la stessa grana con cui la configurazione dei campi già descrive il '
              'lato SIPO.',
         'È stato accettato perché rende la corrispondenza verificabile sul dato reale.')
    sost(doc, ', CAMPO_SIPO, CONDIZIONE, DATA_INIZIO_VALIDITA',
         ', CAMPO_SIPO, DATA_INIZIO_VALIDITA')
    sost(doc, 'TABELLA_SIPO, introdotte in questa versione. Lo schema',
         'TABELLA_SIPO. Lo schema')
    trovate = righe(doc, 'Condizione')
    assert len(trovate) == 2, len(trovate)
    for r in trovate:
        via(r._tr)

    # versioni
    sost(doc, 'portandosi dietro il lavoro umano sui campi SIPO',
         'portandosi dietro il lavoro umano sugli alias SIPO')
    sost(doc, 'campi nuovi senza corrispondenza, campi spariti dal mapping, logiche che perdono '
              'copertura,',
         'campi nuovi senza alias SIPO, campi spariti dal mapping,')
    scrivi(riga(doc, 'ANSC_CFG_VERSIONE', 'COD_VERSIONE, COD_STATO'),
           (None, None, 'COD_STATO, COD_VERSIONE_ANSC, ID_VERSIONE_ANSC, DESCRIZIONE, '
                        'NUM_UC_TOCCATI, TS_ATTIVAZIONE, UTENTE_ATTIVAZIONE.'))
    scrivi(riga(doc, 'Tutte le tabelle versionate'),
           (None, None, 'ANSC_CFG_UC (con il catalogo degli UC), ANSC_TEMPLATE, '
                        'ANSC_CFG_CAMPO, ANSC_CFG_FORMULA, ALLEGATI_USECASE, SOGGETTI_USECASE '
                        'e RICONCILIAZ_DIZIONARI sono duplicate alla creazione della bozza.'))
    scrivi(riga(doc, 'ANSC_ANA_UC', 'UC ritirati e ancora adottati'),
           ('ANSC_CFG_UC', None, 'Le righe del catalogo con la validità chiusa e ancora '
                                 'legate a un tipo atto alimentano la voce «UC ritirati e '
                                 'ancora adottati» del report.'))
    scrivi(riga(doc, 'ANSC_STATO_ATTO', 'timbro storico'),
           (None, None, 'L’atto non registra la versione: quella con cui è stato costruito si '
                        'ricava confrontando TS_VALIDAZIONE con le date di attivazione '
                        '(TS_ATTIVAZIONE). Per questo una versione attivata non si cancella.'))
    sost(doc, 'Scrive COD_STATO, DATA_ATTIVAZIONE e UTENTE_ATTIVAZIONE',
         'Scrive COD_STATO, TS_ATTIVAZIONE e UTENTE_ATTIVAZIONE')

    # comandi
    sost(doc, 'OPERATORE, DATA; RICHIESTA e RISPOSTA', 'OPERATORE, TS_REGISTRAZIONE; RICHIESTA '
                                                       'e RISPOSTA')
    scrivi(riga(doc, 'ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO, ALLEGATI_USECASE, ANSC_CFG_FORMULA'),
           ('ANSC_CFG_CAMPO, ALLEGATI_USECASE, ANSC_CFG_FORMULA', None, None))


# ───────────────────────────────────────────────────────────── 4. numerazione comunale
def numerazione(doc):
    sost(doc, 'Tre numeri consecutivi per un parto trigemino e, sotto, la registrazione a '
              'posteriori.', 'Tre numeri consecutivi per un parto trigemino.')
    sost(doc, 'e poggiano sul servizio della numerazione num-ansc-sipo che l’analisi introduce '
              '[R1]: le pagine non scrivono le tabelle, chiamano le operazioni del servizio '
              '[R6].',
         'e poggiano sul servizio della numerazione be-numeratore-comunale che l’analisi '
         'descrive [R1]: le pagine non scrivono le tabelle, chiamano le quattro operazioni del '
         'servizio — POST /richiesta, GET /ricerca, PUT /utilizza e PUT /scarta, sotto '
         '/api/v1/numerazione-comunale.')
    sost(doc, 'La pagina si apre con il registro corrente, l’anno corrente e un numero, come in '
              'Side, e i tre campi sono modificabili.',
         'La pagina si apre con l’anno corrente e un numero, come in Side, e i due campi sono '
         'modificabili. La serie è unica per tutti i registri, e il registro non si chiede.')
    p = par(doc, '⚠️ Due adattamenti rispetto a Side, dichiarati.')
    D.testo_di(p, 'Un adattamento rispetto a Side, dichiarato. In Side le azioni di riga sono '
                  '«solo ad uso e consumo dell’operatore» e non hanno vincoli; qui gli stati '
                  'Utilizzato e Scartato sono finali, perché in SIPO tutti i numeri passano '
                  'dalla serie — anche quelli del percorso ordinario — e la serie è il luogo in '
                  'cui un buco deve potersi spiegare.')
    D.riga_dopo(None, p,
                'Tre funzioni che il disegno prevedeva non hanno un’operazione nel servizio, e '
                'la pagina non le offre finché non l’avranno (OP-79 dell’analisi [R1]). La '
                'registrazione a posteriori del numero usato sulla web app mentre SIPO non era '
                'disponibile: fino ad allora resta la prassi di Side, una richiesta ordinaria '
                'nella fiducia che il numero ottenuto coincida con quello usato, e una '
                'discordanza si scopre soltanto confrontando. L’identificativo nazionale sul '
                'numero: PUT /utilizza porta l’atto di SIPO ma non l’identificativo, che si '
                'legge dall’atto depositato (ANSC_STATO_ATTO.ID_ANSC). L’operatore: il servizio '
                'registra oggi sempre «admin», e la colonna non dice chi ha staccato il numero.')

    sost(doc, 'La richiesta: registro, anno, quantità, operatore e istante.',
         'La richiesta: anno, quantità, operatore e istante.')
    sost(doc, 'I numeri della richiesta, il loro stato, l’identificativo nazionale e l’atto di '
              'SIPO.', 'I numeri della richiesta, il loro stato e l’atto di SIPO.')
    scrivi(riga(doc, 'SEQ_NUM_COMUNALE_<registro>_<anno>', 'Consumo, tramite il servizio'),
           ('NUMERATORE_COMUNALE', 'Aggiornamento, tramite il servizio',
            'La serie dell’anno: num_atto avanza di tanti numeri quanti ne sono staccati, e la '
            'riga dell’anno si crea alla prima richiesta. La pagina non la nomina.'))
    via_riga(doc, 'VALORE_DOMINIO', 'I cinque registri')
    via_riga(doc, 'Registro', 'Tendina sui registri')
    sost(doc, 'Predefinito l’anno corrente; ammessi il corrente e il precedente.',
         'Predefinito l’anno corrente. La pagina propone il corrente e il precedente; il '
         'servizio accetta gli anni dal 2023.')
    sost(doc, 'Per il parto plurimo, il numero dei nati: i numeri escono consecutivi.',
         'Per il parto plurimo, il numero dei nati: i numeri escono consecutivi. Da 1 a 999.')
    scrivi(riga(doc, 'RICHIEDI'),
           (None, None, 'Stacca i numeri (POST /richiesta, con anno e numeroElementi) e li '
                        'aggiunge alla tabella. La riga dell’anno nel numeratore, se manca, la '
                        'crea il servizio alla prima richiesta.'))
    scrivi(riga(doc, 'Spunta', 'aggiornaNumero'),
           (None, None, 'Segna il numero come Utilizzato (PUT /utilizza), con l’atto di SIPO se '
                        'è noto. L’identificativo nazionale non si registra sul numero: '
                        'l’operazione non lo porta.'))
    scrivi(riga(doc, 'Croce', 'aggiornaNumero'),
           (None, None, 'Segna il numero come Scartato (PUT /scarta). Lo stato è finale.'))
    via_riga(doc, 'Registrazione a posteriori')

    # ricerca e consultazione
    sost(doc, 'Le serie dell’anno in testa, con i buchi; la ricerca delle richieste sotto.',
         'I filtri della ricerca del servizio e i numeri trovati.')
    p = par(doc, 'La pagina riprende la ricerca di Side')
    D.testo_di(p, 'La pagina riprende la ricerca di Side con i filtri che GET /ricerca '
                  'consente: anno, stato, numero, richiesta, atto di SIPO, intervallo delle '
                  'date di richiesta e operatore. Predefinito il giorno corrente; nessun filtro '
                  'è obbligatorio, perché il servizio ignora quelli vuoti e pagina i risultati. '
                  'Il filtro sull’atto di SIPO, che Side non ha, serve a ritrovare il numero di '
                  'un atto in lavorazione; quello sull’operatore non serve finché il servizio '
                  'registra sempre «admin».')
    p = par(doc, 'In testa sta ciò che Side non ha')
    D.testo_di(p, 'Lo stato della serie dell’anno — il prossimo numero, i conteggi per stato e '
                  'i buchi — è ciò che Side non ha e che a SIPO serve, perché in SIPO passano '
                  'dalla serie tutti i numeri e un buco è un fatto da spiegare. Il servizio non '
                  'ha oggi un’operazione che lo restituisca: GET /ricerca elenca i numeri '
                  'staccati, non quelli mancanti. Finché non la avrà (OP-79 dell’analisi [R1]) '
                  'il pannello delle serie non si realizza, e un buco si ricostruisce soltanto '
                  'confrontando i numeri restituiti.')
    p = par(doc, 'CREA SERIE crea le sequence')
    D.testo_di(p, 'La riga dell’anno nel numeratore si crea alla prima richiesta: non serve un '
                  'comando per crearla in anticipo, e il servizio non lo offre. Nemmeno il '
                  'passaggio a Evento acquisito, quando l’atto formato sulla web app viene '
                  'agganciato in SIPO, ha un’operazione: lo stato 4 esiste nel dominio, ma '
                  'nessuna operazione lo imposta (OP-79).')
    sost(doc, 'I numeri delle richieste e i loro cambi di stato.',
         'I numeri delle richieste e i loro cambi di stato (PUT /utilizza, PUT /scarta).')
    scrivi(riga(doc, 'SEQ_NUM_COMUNALE_<registro>_<anno>'),
           ('NUMERATORE_COMUNALE', 'Nessun uso',
            'Il servizio non ne espone il contenuto: il prossimo numero e i buchi non si '
            'leggono da questa pagina (OP-79).'))
    sost(doc, 'Dal numero all’atto depositato: NUM_COMUNALE e ID_ANSC',
         'Dal numero all’atto depositato: NUMERO_ATTO e ID_ANSC')
    via_riga(doc, 'Serie dell’anno')
    scrivi(riga(doc, 'Registro · Richieste da · Richieste a · Operatore · Stato · Atto SIPO'),
           ('Anno · Stato · Numero · ID richiesta · Atto SIPO · Richieste da · Richieste a · '
            'Operatore', None,
            'I parametri di GET /ricerca: un filtro vuoto è ignorato. Predefinito il giorno '
            'corrente. I risultati sono paginati (pageOffset, pageSize).'))
    via_riga(doc, 'Matita', 'Evento acquisito')
    scrivi(riga(doc, 'Occhio', 'leggiNumero'),
           (None, None, 'Il numero e la richiesta che lo ha prodotto, dalla riga restituita da '
                        'GET /ricerca; dal numero di un atto depositato si apre il dettaglio '
                        'dell’atto.'))
    via_riga(doc, 'CREA SERIE')


# ───────────────────────────────────────────────────────────── 5. copertura e punti aperti
def copertura(doc):
    sost(doc, 'le ventuno del modello dell’integrazione più le quattro del registro introdotto '
              'da questa versione. La verifica segue.',
         'le ventidue del modello dell’integrazione più le quattro del registro delle pagine. '
         'La verifica segue. Cinque tabelle del modello non hanno una pagina: '
         'ANSC_CFG_DOMINIO_SIPO per decisione, NUMERATORE_COMUNALE perché la governa soltanto '
         'il servizio della numerazione, e tre per le quali la scelta è aperta (BO-34).')
    sost(doc, 'Completa, tramite il servizio num-ansc-sipo.',
         'Completa, tramite il servizio be-numeratore-comunale.')
    r = riga(doc, 'DATI_ATTO_ESTERNO', 'registrazione a posteriori, tramite il servizio')
    scrivi(r, (None, None, 'Completa per lo stacco e per gli stati Utilizzato e Scartato, '
                           'tramite il servizio. La registrazione a posteriori e lo stato '
                           'Evento acquisito non hanno un’operazione (OP-79).'))
    riga_dopo(r, ('NUMERATORE_COMUNALE', 'Nessuna, di proposito',
                  'La scrive soltanto il servizio be-numeratore-comunale, che non ne espone il '
                  'contenuto. Il prossimo numero e i buchi della serie non si leggono finché il '
                  'servizio non avrà un’operazione per farlo (OP-79).'))
    r = riga(doc, 'ALLEGATO', 'Il contrassegno dell’attestazione')
    r2 = riga_dopo(r, ('firmatari', 'Nessuna',
                       'La scrive il percorso di firma delle maschere di SIPO. Potrebbe '
                       'comparire come scheda del dettaglio dell’atto: da decidere (BO-34).'))
    riga_dopo(r2, ('forzatura_validazione', 'Nessuna',
                   'La scrive la validazione con forzatura, che l’analisi rinvia a una stesura '
                   'successiva. Da decidere se il dettaglio dell’atto debba mostrarla '
                   '(BO-34).'))
    r = riga(doc, 'SOGGETTI_USECASE', 'Soggetti per caso d’uso · Configurazione UC')
    riga_dopo(r, ('comunicaz_anagrafica_usecase', 'Nessuna',
                  'È configurazione per caso d’uso, popolata dallo script di caricamento '
                  'dell’analisi. Da decidere se serva una pagina, come per allegati e soggetti '
                  'per caso d’uso (BO-34).'))
    sost(doc, 'avviata dal riepilogo dei soggetti di SIPO. Nuova in questa versione.',
         'avviata dal riepilogo dei soggetti di SIPO.')
    scrivi(riga(doc, 'ANSC_CFG_UC', 'Configurazione UC — elenco e dettaglio'),
           (None, 'Configurazione UC — elenco e dettaglio · Catalogo dei casi d’uso',
            'Completa. Il catalogo pubblicato da ANSC sta nelle stesse righe: quelle senza tipo '
            'atto sono UC non ancora adottati.'))
    via_riga(doc, 'ANSC_ANA_UC', 'Sola lettura, come deve essere')
    via_riga(doc, 'ANSC_CFG_SEZIONE', 'Configurazione UC (scheda Sezioni)')
    r = riga(doc, 'ANSC_CFG_VERSIONE', 'Versioni della configurazione')
    riga_dopo(r, ('ANSC_TEMPLATE', 'Configurazione UC — dettaglio (scheda Dati generali)',
                  'Completa. In quale passo del flusso l’interrogazione si esegua resta da '
                  'stabilire nell’analisi.'))
    sost(doc, 'Sola lettura: si aggiorna da ANSC. In questa versione acquisisce la versione '
              'della tabella, che R901 restituisce e che il modello non conservava.',
         'Sola lettura: si aggiorna da ANSC. Conserva la versione della tabella che R901 '
         'restituisce (cd_versione).')
    sost(doc, 'Sola lettura: si aggiorna da ANSC. In questa versione perde cd_valore e '
              'acquisisce un attributo JSON per le due colonne aggiuntive di consolati e casi '
              'd’uso.',
         'Sola lettura: si aggiorna da ANSC. Le due colonne aggiuntive di consolati e casi '
         'd’uso stanno nell’attributo JSON (tx_attributi).')
    sost(doc, 'Completa. In questa versione acquisisce SCHEMA_SIPO, TABELLA_SIPO e CAMPO_SIPO.',
         'Completa.')
    sost(doc, 'Si popola a mano, come stabilito nella v3.34 dell’analisi: è l’unica tabella del '
              'modello senza una pagina, e lo è di proposito.',
         'Si popola a mano, come stabilito nell’analisi: è la sola tabella del modello che '
         'resta senza pagina per decisione.')
    sost(doc, 'In sola lettura dall’interfaccia: i temi sono pochi e d’impianto. Nuova in questa '
              'versione.',
         'In sola lettura dall’interfaccia: i temi sono pochi e d’impianto.')

    # punti aperti
    scrivi(riga(doc, 'BO-3'),
           (None, None, 'Deciso nell’analisi [R1]: nelle tabelle di Side PRENOTAZIONE_ATTI e '
                        'DATI_ATTO_ESTERNO, con la serie annuale in NUMERATORE_COMUNALE, unica '
                        'per tutti i registri, governate dal servizio be-numeratore-comunale. '
                        'Le pagine della numerazione sono descritte su quella base.'))
    sost(doc, 'le pagine servono agli atti formati sulla web app, al parto plurimo, alla '
              'registrazione a posteriori e al governo delle serie.',
         'le pagine servono agli atti formati sulla web app, al parto plurimo e alla '
         'consultazione dei numeri staccati.')
    scrivi(riga(doc, 'BO-7'),
           (None, 'Chiuso. Come si presenta una sezione condizionata che non si applica',
            'La sezione non è più un dato della configurazione e la sua presenza non ha una '
            'logica: il dettaglio dell’atto raggruppa i campi per oggetto del modello evento, '
            'senza sezioni condizionate.'))
    scrivi(riga(doc, 'BO-13'),
           (None, 'Chiuso. Recepire nell’analisi le tre correzioni al modello dei dizionari',
            'Recepite nell’analisi [R1]: VALORE_DOMINIO non ha cd_valore e porta l’attributo '
            'JSON tx_attributi, DOMINIO_DECODIFICA porta cd_versione.'))
    scrivi(riga(doc, 'BO-14'),
           (None, 'Chiuso. Recepire nell’analisi le tre colonne nuove della riconciliazione',
            'Recepite nell’analisi [R1]: RICONCILIAZ_DIZIONARI porta SCHEMA_SIPO, TABELLA_SIPO '
            'e CAMPO_SIPO.'))
    scrivi(riga(doc, 'BO-30'),
           (None, None, 'Il servizio non la offre ancora (OP-79). Quando la offrirà, va '
                        'stabilito se basti l’abilitazione dell’ufficiale o serva un profilo '
                        'distinto, come per il caricamento da file (BO-28): un numero '
                        'registrato a posteriori può far avanzare la serie e lasciarvi buchi.'))
    t = D.trova_tabella(doc, '#', 'questione', 'perché è aperta')
    D.clona_riga(t, ('BO-33', 'Le operazioni che mancano al servizio della numerazione',
                     'Le quattro operazioni del servizio be-numeratore-comunale non coprono '
                     'cinque funzioni che le pagine della numerazione prevedevano: la '
                     'registrazione a posteriori di un numero già usato, il passaggio a Evento '
                     'acquisito, l’identificativo nazionale sul numero, lo stato della serie '
                     'con i suoi buchi e l’operatore reale, oggi sempre «admin». Le pagine non '
                     'le offrono finché il servizio non le avrà; nell’analisi è OP-79.'))
    D.clona_riga(t, ('BO-34', 'Le tabelle del modello senza una pagina',
                     'firmatari, forzatura_validazione e comunicaz_anagrafica_usecase non sono '
                     'governate né mostrate da alcuna pagina. Le prime due le scrive il percorso '
                     'di formazione dell’atto e potrebbero comparire come schede del dettaglio '
                     'dell’atto; la terza è configurazione per caso d’uso, oggi popolata da '
                     'script. Va deciso se e dove mostrarle.'))


# ───────────────────────────────────────────────────────────── 6. pulizia e figure
def senza_avvisi(doc):
    """Niente «⚠️» nei documenti (Storia esclusa)."""
    n = 0
    for p in _paragrafi(doc):
        if '⚠️' not in p.text:
            continue
        for r in p.runs:
            r.text = r.text.replace('⚠️ ', '').replace('⚠️', '')
        if '⚠️' in p.text:
            D.testo_di(p, p.text.replace('⚠️ ', '').replace('⚠️', ''))
        n += 1
    return n


def rinumera_figure(doc):
    """Tolta la Figura 20 (Logiche di scelta), le successive scalano di uno."""
    n = 0
    for p in doc.paragraphs:
        m = re.match(r'Figura (\d+) —', p.text)
        if m and int(m.group(1)) > 20:
            vecchio, nuovo = f'Figura {m.group(1)} —', f'Figura {int(m.group(1)) - 1} —'
            for r in p.runs:
                if vecchio in r.text:
                    r.text = r.text.replace(vecchio, nuovo)
                    break
            else:
                D.testo_di(p, p.text.replace(vecchio, nuovo))
            n += 1
    return n


FIGURE = [
    ('Figura 1 —', 'bo_mfe.png'),
    ('Figura 8 —', 'bo_home.png'),
    ('Figura 10 —', 'bo_atto.png'),
    ('Figura 14 —', 'bo_uc_elenco.png'),
    ('Figura 15 —', 'bo_uc_dettaglio.png'),
    ('Figura 16 —', 'bo_allegati_uc.png'),
    ('Figura 19 —', 'bo_catalogo_uc.png'),
    ('Figura 21 —', 'bo_riconciliazione.png'),
    ('Figura 22 —', 'bo_riconciliazione_dettaglio.png'),
    ('Figura 23 —', 'bo_versioni.png'),
    ('Figura 24 —', 'bo_comandi.png'),
    ('Figura 25 —', 'bo_num_richiesta.png'),
    ('Figura 26 —', 'bo_num_ricerca.png'),
]


def main():
    if os.path.exists(OUT):
        raise SystemExit('esiste già: ' + OUT)
    doc = docx.Document(SRC)
    cornice(doc)
    operativa(doc)
    configurazione(doc)
    numerazione(doc)
    copertura(doc)
    print('avvisi tolti:', senza_avvisi(doc))
    print('didascalie rinumerate:', rinumera_figure(doc))
    for didascalia, png in FIGURE:
        D.sostituisci_immagine(doc, didascalia, os.path.join(IMG, png))
    D.storia(doc, '28/10/2026', '0.11',
             'Glossario · Riferimenti · Contesto tecnico · Mappa · Le pagine (Supervisione, '
             'Dettaglio atto, Configurazione UC, Allegati e soggetti per UC, Caricamento da '
             'file, Catalogo, Riconciliazione, Versioni, Comandi, Numerazione) · Copertura · '
             'Punti aperti',
             'Riallineato il back-office alla v3.54 dell’analisi. Tolta la pagina «Logiche di '
             'scelta»: le logiche sono codici liberi, valutati dal codice applicativo, e le due '
             'tabelle del catalogo sono deprecate. La configurazione dei casi d’uso lega l’UC '
             'al tipo atto e accoglie il catalogo degli UC nelle stesse righe; i campi portano '
             'l’alias SIPO, compilato a mano, e si raggruppano per oggetto del modello evento, '
             'perché la sezione non è più un dato. Le pagine della numerazione usano le quattro '
             'operazioni del servizio be-numeratore-comunale, senza registro; registrazione a '
             'posteriori, Evento acquisito e stato della serie non sono offerti finché il '
             'servizio non li avrà (BO-33). Colonne temporali con TS_ per i TIMESTAMP. La '
             'copertura sale a ventidue tabelle del modello e dichiara quelle senza pagina '
             '(BO-34). Le pagine passano a diciannove; BO-7, BO-13 e BO-14 chiusi.')
    D.frontespizio(doc, '0.11', 'DISEGNO_Back-Office_ANSC_v0.11', data='28/10/2026')
    doc.save(OUT)
    print('scritto:', OUT)


if __name__ == '__main__':
    main()
