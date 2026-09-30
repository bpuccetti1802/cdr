# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.22 -> v3.23 (24/09/2026).

Recepisce le indicazioni dell'utente sul processo di formazione dell'atto:

  1. QUATTRO FASI dichiarate: al termine della lavorazione in SIPO l'UC deve essere
     identificato (scelta dell'operatore ammessa SOLO in caso di ambiguità — commento [55]);
     poi i documenti previsti dall'UC più gli eventuali extra; poi la validazione, prima
     locale e poi di ANSC; poi la firma, dopo la quale l'atto non è più modificabile in SIPO.
  2. OGNI FASE AGGIORNA LO STATO: COD_FASE (lavorazione locale) accanto a STATO (replica di
     ANSC). Sono due cose diverse.
  3. CHE COSA RESTA SULL'ATTO: ID_ANSC, NUM_COMUNALE, COD_UC_ANSC, ID_VERSIONE, payload.
     ⚠️ Il numero comunale non ha una colonna propria sull'atto di stato civile di SIPO.
  4. LA TESTATA DEL MODELLO EVENTO: idTipoEvento (ANSC_01), idtipocontenuto (ANSC_02),
     idUsecase (ANSC_03), idVersion (ANSC_100) — nessuno dei quattro è dichiarato dal
     mapping: li valorizza il concentratore e il pre-filtro li verifica.
  5. ALLEGATI_USECASE dal file `Sorgenti Documentali/allegati_usecase.txt` (struttura Side),
     che sostituisce ANSC_CFG_ALLEGATO; ALLEGATO guadagna fg_extra.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_23_fasi_e_allegati.py
"""
import os
import shutil
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.22.docx')
DST = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.23.docx')
IMG = os.path.join(BASE, 'strumenti', 'img')

if os.path.exists(DST):
    os.remove(DST)
shutil.copy(SRC, DST)
doc = docx.Document(DST)
fatti = []


# ────────────────────────────────────────────────────────────── utilità
def par(inizio, stile=None):
    t = [p for p in doc.paragraphs
         if p.text.strip().startswith(inizio) and (stile is None or p.style.name == stile)]
    if len(t) != 1:
        raise SystemExit(f'attesa 1 occorrenza di «{inizio[:60]}», trovate {len(t)}')
    return t[0]


def riga_con(t, prima_cella):
    for r in t.rows:
        if r.cells[0].text.strip() == prima_cella:
            return r
    raise SystemExit('riga non trovata: ' + prima_cella)


def inserisci_riga(t, dopo, valori):
    nuova = D.clona_riga(t, valori)
    riga_con(t, dopo)._tr.addnext(nuova._tr)
    return nuova


def elimina(elementi, cosa):
    for e in elementi:
        if D.ha_commenti(e):
            raise SystemExit(f'{cosa}: commento di Word ancorato qui, non si cancella')
    for e in elementi:
        e.getparent().remove(e)
    fatti.append('eliminato: ' + cosa)


def mono(testo):
    t = [p for p in doc.paragraphs if p.text.rstrip() == testo.rstrip()]
    if len(t) != 1:
        raise SystemExit(f'riga DDL non univoca: «{testo[:60]}» ({len(t)})')
    return t[0]


def blocco_ddl(create_line):
    p = mono(create_line)
    out, e = [p._p], p._p.getnext()
    while e is not None:
        out.append(e)
        if e.tag.endswith('}p') and Paragraph(e, doc).text.strip().startswith(') TABLESPACE'):
            return out
        e = e.getnext()
    raise SystemExit('blocco DDL non chiuso: ' + create_line)


def sostituisci_blocco(create_line, righe):
    el = blocco_ddl(create_line)
    dopo = el[-1].getnext()
    elimina(el, 'blocco DDL ' + create_line.split('.')[-1].split()[0])
    D.ddl(doc, dopo, righe)


def ddl_dopo(ancora, righe):
    D.ddl(doc, mono(ancora)._p.getnext(), righe)


MOD = D.trova_tabella(doc, 'colonna', 'tipo', 'note')


# ═════════════════════════════════════ 1. scheda e storia
for t in doc.tables:
    if t.rows[0].cells[0].text.strip().lower().startswith(('area organizzativa', 'progetto')):
        for nome, val in (('Data consegna', '24/09/2026'), ('Versione', '3.23')):
            try:
                D.riscrivi_cella(riga_con(t, nome).cells[1], val)
            except SystemExit:
                pass

D.storia(doc, '24/09/2026', '3.23',
         'Flusso operativo · Adeguamenti database · Costruzione del payload · Requisiti · '
         'Open Point · Appendice A',
         'Il processo di formazione è dichiarato in quattro fasi: al termine della lavorazione '
         'in SIPO l’UC deve essere identificato, e la scelta dell’operatore è ammessa solo in '
         'caso di ambiguità; seguono il caricamento dei documenti previsti dall’UC e degli '
         'eventuali extra, la validazione locale e di ANSC, e la firma, dopo la quale l’atto '
         'non è più modificabile in SIPO. Ogni fase aggiorna lo stato dell’atto: COD_FASE '
         'affianca STATO, che resta la replica dello stato dichiarato da ANSC. Sull’atto si '
         'conservano identificativo nazionale, numero comunale, UC e versione della '
         'configurazione. Dichiarata la composizione della testata del modello evento '
         '(idTipoEvento, idtipocontenuto, idUsecase, idVersion) e il controllo contro le '
         'decodifiche. La configurazione degli allegati adotta la struttura del sistema Side '
         '(ALLEGATI_USECASE), al posto della tabella prevista dalle versioni precedenti.')


# ═════════════════════════════════════ 2. le quattro fasi (capitolo del flusso)
ancora = par('Il flusso operativo. In rosso i passi')._p.getprevious()   # il paragrafo-immagine
D.para(doc, ancora, 'Le quattro fasi', stile='Heading 2')
for t in [
    'Il percorso si legge in quattro fasi, e ciascuna ha una condizione di uscita che va '
    'soddisfatta prima di passare alla successiva. Dichiararle serve a due cose: dire che cosa '
    'deve essere vero perché la lavorazione prosegua, e stabilire in quale momento l’atto '
    'smette di essere modificabile.',
]:
    D.para(doc, ancora, t)
for testa, corpo in [
    ('Fase A — la lavorazione in SIPO. ', 'L’operatore compila l’atto nelle maschere che già '
     'conosce. ⚠️ Al termine della lavorazione l’UC deve essere identificato: è la condizione '
     'che apre tutto il resto, perché campi obbligatori, documenti e formule dipendono '
     'dall’UC e non dal Modello. La determinazione è automatica; la scelta da parte '
     'dell’operatore è ammessa soltanto quando la configurazione risulta ambigua, e resta '
     'registrata come tale.'),
    ('Fase B — i documenti. ', 'Formato l’atto, si caricano i file che l’UC prevede — firmati '
     'digitalmente o scansionati — e gli eventuali documenti extra, che la configurazione non '
     'elenca ma che l’ufficiale ritiene di allegare. I primi sono verificabili dal pre-filtro, '
     'i secondi no: sono ammessi, contati e distinti, non ignorati.'),
    ('Fase C — la validazione. ', 'Prima quella locale, che non chiama ANSC e intercetta le '
     'mancanze prima che un identificativo nazionale sia consumato; poi quella di ANSC con '
     'R009, che deposita la bozza e restituisce l’identificativo. Fra le due stanno la ricerca '
     'dei soggetti, la costruzione del payload e l’eventuale anteprima.'),
    ('Fase D — la firma. ', 'La firma del dichiarante, quando prevista, e quella dell’ufficiale '
     'con il proprio OTP. ⚠️ Da questo momento l’atto non è più modificabile in SIPO: ciò che '
     'si può ancora fare passa per gli istituti di ANSC — annotazione, rettifica, annullamento '
     '— e non per la maschera di compilazione. È il punto di non ritorno del percorso, e va '
     'reso evidente all’operatore prima che lo attraversi, non dopo.'),
]:
    D.voce(doc, ancora, testa, corpo)

D.tabella(doc, ancora, [
    ('Fase', 'Condizione di uscita', 'COD_FASE raggiunto', 'Che cosa non è più possibile'),
    ('A — Lavorazione in SIPO', 'L’UC è identificato: una sola riga di configurazione '
     'applicabile, oppure la scelta dell’operatore fra le candidate in caso di ambiguità.',
     'UC_DETERMINATO', 'Nulla: l’atto resta pienamente modificabile.'),
    ('B — Documenti', 'I documenti obbligatori per quell’UC sono stati caricati e accettati '
     'da ANSC; gli extra sono ammessi e contrassegnati come tali.', 'DOCUMENTI_ACQUISITI',
     'Nulla in SIPO; in ANSC un allegato trasmesso si sostituisce, non si modifica.'),
    ('C — Validazione', 'La verifica locale non segnala mancanze e R009 ha accettato il '
     'deposito restituendo l’identificativo nazionale.', 'PREVALIDATO, poi VALIDATO',
     'Dopo il deposito l’identificativo nazionale è consumato: una correzione richiede di '
     'ridepositare o di annullare, non di riscrivere.'),
    ('D — Firma', 'L’atto è firmato dall’ufficiale ed è formato.', 'FIRMATO',
     '⚠️ La modifica dell’atto in SIPO: da qui in avanti si interviene con gli istituti '
     'previsti da ANSC.'),
], MOD)
D.para(doc, ancora, 'Le quattro fasi, con la condizione che consente di proseguire.',
       corsivo=True)
fatti.append('capitolo del flusso: le quattro fasi')

# la figura e la sua didascalia
D.sostituisci_immagine(doc, 'Il flusso operativo. In rosso i passi',
                       os.path.join(IMG, 'flusso_operativo.png'))
D.testo_di(par('Il flusso operativo. In rosso i passi'),
           'Il flusso operativo nelle sue quattro fasi. Per ciascun passo: la configurazione '
           'che lo guida, ciò che resta scritto sull’atto e la fase con cui l’operazione si '
           'registra in ANSC_LOG_AUDIT.')

# ═════════════════════════════════════ 3. l'ambiguità: scelta dell'operatore
t = D.trova_tabella(doc, 'esito della ricerca', 'comportamento')
r = riga_con(t, 'Più righe valide')
D.riscrivi_cella(r.cells[1], 'La priorità le ordina e la prima vince: è il meccanismo '
                             'previsto, non un ripiego. Se due righe hanno la stessa priorità '
                             'la configurazione è ambigua e si applica quanto segue.')
r = [rr for rr in t.rows if 'La scelta' in rr.cells[0].text][0]
D.riscrivi_cella(r.cells[0], 'La scelta dell’operatore, solo in caso di ambiguità')
D.riscrivi_cella(r.cells[1], 'Quando e soltanto quando la configurazione non individua un UC '
                             'unico, il sistema presenta all’operatore gli UC candidati e gli '
                             'consente di sceglierne uno. La scelta è registrata come tale '
                             '(COD_ORIGINE_UC = OPERATORE) insieme all’identità di chi l’ha '
                             'compiuta, così che l’atto resti spiegabile e la configurazione '
                             'ambigua sia visibile a chi la governa. ⚠️ Non è la via '
                             'ordinaria: fuori dall’ambiguità l’UC non è una scelta dello '
                             'sportello, e ogni scelta manuale è il segnale di una '
                             'configurazione da correggere.')
fatti.append('regola dell’ambiguità riscritta (commento [55])')

# ═════════════════════════════════════ 4. che cosa resta sull'atto
ancora = D.h(doc, 2, 'La traccia di ciò che accade')._p
D.para(doc, ancora, 'Che cosa resta sull’atto', stile='Heading 2')
for t in [
    'Conclusa la formazione, quattro informazioni devono restare sull’atto e sopravvivere a '
    'qualunque purga dei registri tecnici: senza di esse l’atto è in ANSC ma non è più '
    'ricostruibile da SIPO.',
]:
    D.para(doc, ancora, t)
D.tabella(doc, ancora, [
    ('Dato', 'Dove risiede', 'Perché deve restare'),
    ('Identificativo nazionale (ID_ANSC)', 'ANSC_STATO_ATTO.ID_ANSC, restituito da R009.',
     'È la chiave con cui l’atto si ritrova in ANSC, si consulta, si annota e si annulla. '
     'Senza di esso ogni operazione successiva richiede una ricerca per dati anagrafici.'),
    ('Numero comunale dell’atto', 'ANSC_STATO_ATTO.NUM_COMUNALE. ⚠️ Sull’atto di stato civile '
     'di SIPO non esiste una colonna dedicata: MATR_USR.ATTO porta NUMERO_ATTO con parte e '
     'serie, mentre NUMERO_COMUNALE esiste sull’ATTO di anagrafe (ANAG_USR), dove però è '
     'valorizzata scomponendo l’identificativo ANSC di un atto formato altrove.',
     'È il numero che il Comune assegna e che viaggia nel payload; la sua allocazione è a '
     'carico nostro (OP-44) e la colonna in cui risiede va decisa (OP-29, OP-60).'),
    ('UC determinato (COD_UC_ANSC)', 'ANSC_STATO_ATTO.COD_UC_ANSC, con COD_LOGICA e '
     'COD_ORIGINE_UC che dicono come vi si è arrivati.',
     'Dal Modello non è ricavabile: più UC lo condividono. Senza l’UC non si sa quali campi '
     'fossero obbligatori né quali documenti fossero richiesti per quell’atto.'),
    ('Versione della configurazione', 'ANSC_STATO_ATTO.ID_VERSIONE, che richiama la baseline '
     'e, per suo tramite, la revisione di ANSC recepita.',
     'Il mapping è rivisto in media ogni diciassette giorni: senza la versione, il payload '
     'depositato non è spiegabile a distanza di mesi, perché la configurazione che lo ha '
     'prodotto non esiste più nella forma di allora.'),
], MOD)
D.para(doc, ancora, '⚠️ Le prime due informazioni interessano anche SIPO, non solo il '
                    'componente: una maschera di ricerca che non mostri l’identificativo '
                    'nazionale costringe l’operatore a cercarlo altrove. Gli impatti sul '
                    'front-end lo registrano.')
fatti.append('nuova sezione «Che cosa resta sull’atto»')

# ═════════════════════════════════════ 5. la testata del modello evento
ancora = D.h(doc, 2, 'Le fonti della configurazione')._p
D.para(doc, ancora, 'La testata del modello evento: tipo evento, contenuto, caso d’uso e '
                    'versione', stile='Heading 2')
for t in [
    'Prima dei dati dell’atto, il modello evento porta una testata di quattro campi che '
    'dichiarano che cosa si sta depositando. ⚠️ Nessuno dei quattro è dichiarato dal mapping '
    'dei casi d’uso: il mapping descrive il contenuto dell’atto, non la sua intestazione. Li '
    'valorizza quindi il concentratore, e poiché non hanno una fonte nella configurazione '
    'importata vanno ricavati dal catalogo degli UC e verificati contro le decodifiche.',
]:
    D.para(doc, ancora, t)
D.tabella(doc, ancora, [
    ('Campo', 'Decodifica', 'Come si valorizza', 'Controllo del pre-filtro'),
    ('idTipoEvento', 'ANSC_01 — cinque valori: 1 nascita, 2 morte, 3 matrimonio, 4 unione '
     'civile, 5 cittadinanza.',
     '⚠️ Coincide con la prima cifra del codice dell’UC: verificato sull’intero catalogo '
     'pubblicato, i codici che cominciano per 1 sono di nascita, per 2 di morte e così via. '
     'Si conserva sul catalogo (ANSC_ANA_UC.ID_TIPO_EVENTO) invece di ricalcolarlo.',
     'Che il valore esista nella decodifica e che concordi con la prima cifra dell’UC '
     'determinato: una discordanza è un errore di configurazione, non dell’atto.'),
    ('idtipocontenuto', 'ANSC_02 — atto, annotazione, trascrizione, annotazione automatica, '
     'rifiuto.',
     'È pubblicato da ANSC per ciascun UC nella decodifica dei casi d’uso e si replica nel '
     'catalogo. ⚠️ Non è la famiglia: le trascrizioni non sono un tipo evento, sono un tipo '
     'di contenuto di un tipo evento.',
     'Che sia valorizzato: per alcuni UC la fonte lo lascia vuoto, e in quel caso va chiesto '
     'invece che dedotto.'),
    ('idUsecase', 'ANSC_03 — il catalogo dei casi d’uso.',
     'È l’UC determinato nella fase A. Va trasmesso nella forma in cui ANSC lo pubblica.',
     '⚠️ Che il codice sia quello pubblicato e non la sua forma puntata: 2101, non 2.1.0.1. '
     'La notazione puntata è redazionale e non appartiene al dato.'),
    ('idVersion', 'ANSC_100 — le versioni del modello evento.',
     'È la versione del modello con cui il payload è costruito, dichiarata dalla baseline '
     'attiva (ANSC_CFG_VERSIONE.ID_VERSIONE_ANSC).',
     'Che corrisponda alla baseline usata. Nessun codice d’errore di ANSC segnala una versione '
     'obsoleta: se ne accorge il deposito, con un rifiuto che non la nomina.'),
], MOD)
D.para(doc, ancora, 'La testata del modello evento e le decodifiche che la governano.',
       corsivo=True)
fatti.append('nuova sezione sulla testata del modello evento')

# il catalogo degli UC guadagna il tipo evento
t = D.tabella_colonne(doc, 'COD_MOTORE')   # la scheda di ANSC_ANA_UC
inserisci_riga(t, 'COD_FAMIGLIA', (
    'ID_TIPO_EVENTO', 'VARCHAR2(10)',
    'Tipo evento secondo la decodifica ANSC_01, trasmesso nella testata del modello evento. '
    'Coincide con la prima cifra del codice dell’UC; si conserva perché il payload lo richiede '
    'e perché una regola implicita nel codice è una regola che nessuno verifica.'))


# ═════════════════════════════════════ 6. ALLEGATI_USECASE (struttura Side)
t = D.tabella_colonne(doc, 'ID_ALLEGATO')
D.riscrivi_sicura(t, [
    ('cd_usecase', 'VARCHAR2(20) (PK)', 'Codice dell’UC come ANSC lo pubblica. ⚠️ Nella '
     'struttura di origine è lungo dieci caratteri: alla scala del nostro catalogo conviene '
     'venti, perché i codici non hanno lunghezza fissa.'),
    ('ty_allegato', 'VARCHAR2(10) (PK)', 'Tipo di allegato secondo la decodifica ANSC_09. È il '
     'valore trasmesso ad ANSC. ⚠️ Essendo in chiave, le sei descrizioni del mapping prive di '
     'corrispondenza (OP-50) vanno raccordate prima del carico, non dopo.'),
    ('id_versione', 'NUMBER (PK, FK)', 'Baseline di appartenenza (ANSC_CFG_VERSIONE). '
     '⚠️ Aggiunta rispetto alla struttura di origine, che non conosce il versionamento della '
     'configurazione: senza, due baseline non possono dichiarare documenti diversi per lo '
     'stesso UC.'),
    ('ds_allegato', 'VARCHAR2(400)', 'Descrizione come compare nel mapping ufficiale. '
     '⚠️ Aggiunta: è la chiave con cui l’importazione riconosce la riga, perché il mapping '
     'nomina gli allegati per descrizione e non per codice.'),
    ('ty_presenza', 'VARCHAR2(10)', 'Se il documento sia obbligatorio, facoltativo o '
     'condizionato. [DA VERIFICARE: i valori ammessi nella struttura di origine, che il file '
     'ricevuto non dichiara.]'),
    ('ty_configurazione', 'VARCHAR2(10)', '[DA VERIFICARE: la semantica nella struttura di '
     'origine. Conservata per fedeltà alla fonte, in attesa di chiarimento (OP-61).]'),
    ('id_dominio / cd_logica', 'NUMBER / VARCHAR2(30) (FK)', 'La condizione che rende il '
     'documento necessario, presa dal catalogo delle logiche. ⚠️ Sostituisce la condizione '
     'scritta in chiaro: è la stessa grammatica delle altre condizioni e la valuta lo stesso '
     'motore.'),
    ('fg_incluso_att_conformita', 'CHAR(1)', 'Se il documento vada incluso nell’attestazione '
     'di conformità. Non è importabile: è una scelta del Comune. Stesso nome della colonna '
     'omologa di ALLEGATO.'),
    ('nr_ordinamento', 'NUMBER', 'Ordine di presentazione all’operatore.'),
    ('fg_operante', 'CHAR(1)', 'Valori 0/1: se la riga è in esercizio. È il contrassegno con '
     'cui il Comune disattiva una configurazione senza cancellarla.'),
    ('tx_note', 'CLOB', 'Testo libero a disposizione di chi configura.'),
    ('cd_ope_ins_dt / ts_ins_dt / cd_ope_ult_agg_dt / ts_ult_agg_dt / ds_note_dt',
     'CHAR(6) / TIMESTAMP', 'Campi tecnici nella convenzione di Side, come per ALLEGATO.'),
])
fatti.append('scheda della configurazione degli allegati riscritta sulla struttura di Side')

# la provenienza della struttura, detta dove la si introduce
D.para(doc, par('La struttura ANSC_CFG_ALLEGATO')._p,
       'La struttura è quella del sistema Side del Comune di Milano, ricevuta come definizione '
       'e adottata con i nomi di origine, come già per ALLEGATO e per i dizionari. Tre '
       'aggiunte la rendono utilizzabile qui: la baseline (id_versione), senza la quale due '
       'revisioni della configurazione non possono coesistere; la descrizione del mapping '
       '(ds_allegato), che è la chiave con cui l’importazione riconosce la riga; e il '
       'riferimento al catalogo delle logiche al posto della condizione scritta in chiaro. '
       '⚠️ La chiave primaria è il tipo di allegato codificato: le sei descrizioni del mapping '
       'che non hanno un tipo corrispondente (OP-50) non sono caricabili finché il raccordo '
       'non è stato fatto, e questo rende quel punto aperto bloccante per la fase B.')

# ALLEGATO: il documento extra
t = D.tabella_colonne(doc, 'id_allegato')
inserisci_riga(t, 'ds_tipo_allegato', (
    'fg_extra', 'CHAR(1)',
    '⚠️ Aggiunta: 0/1 secondo che il documento sia fra quelli previsti dall’UC o sia stato '
    'allegato in più. Gli extra sono ammessi ma non verificabili dal pre-filtro, e vanno '
    'distinti perché la loro assenza non è un errore e la loro presenza non è un requisito '
    'soddisfatto.'))


# ═════════════════════════════════════ 7. il DDL
# 7a — ALLEGATI_USECASE al posto di ANSC_CFG_ALLEGATO
sostituisci_blocco('CREATE TABLE ANSC_USR.ANSC_CFG_ALLEGATO (', [
    'CREATE TABLE ANSC_USR.ALLEGATI_USECASE (',
    '  cd_usecase           VARCHAR2(20 CHAR)  NOT NULL,',
    '  ty_allegato          VARCHAR2(10 CHAR)  NOT NULL,',
    '  id_versione          NUMBER             NOT NULL,',
    '  ds_allegato          VARCHAR2(400 CHAR),',
    '  ty_presenza          VARCHAR2(10 CHAR)  NOT NULL,',
    '  ty_configurazione    VARCHAR2(10 CHAR),',
    '  id_dominio           NUMBER DEFAULT 2,',
    '  cd_logica            VARCHAR2(30 CHAR),',
    '  fg_incluso_att_conformita CHAR(1 CHAR) DEFAULT \'0\' NOT NULL,',
    '  nr_ordinamento       NUMBER DEFAULT 1   NOT NULL,',
    '  fg_operante          CHAR(1 CHAR) DEFAULT \'1\' NOT NULL,',
    '  tx_note              CLOB,',
    '  cd_ope_ins_dt        CHAR(6 CHAR)       NOT NULL,',
    '  ts_ins_dt            TIMESTAMP          NOT NULL,',
    '  cd_ope_ult_agg_dt    CHAR(6 CHAR),',
    '  ts_ult_agg_dt        TIMESTAMP,',
    '  ds_note_dt           VARCHAR2(50 CHAR),',
    '  CONSTRAINT allegati_usecase_pk PRIMARY KEY (cd_usecase, ty_allegato, id_versione),',
    '  CONSTRAINT allegati_usecase_versione_fk',
    '    FOREIGN KEY (id_versione) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),',
    '  CONSTRAINT allegati_usecase_logica_fk',
    '    FOREIGN KEY (id_dominio, cd_logica)',
    '    REFERENCES ANSC_USR.VALORI_DOMINIO (ID_DOMINIO, COD_LOGICA),',
    "  CONSTRAINT allegati_usecase_fg_operante_check CHECK (fg_operante IN ('0','1')),",
    '  CONSTRAINT allegati_usecase_fg_att_conf_check',
    "    CHECK (fg_incluso_att_conformita IN ('0','1'))",
    ') TABLESPACE ANSC_USR;',
    'CREATE INDEX ANSC_USR.IX_ALLEGATI_USECASE_UC',
    '  ON ANSC_USR.ALLEGATI_USECASE (id_versione, cd_usecase) TABLESPACE ANSC_USR;',
    'COMMENT ON TABLE ANSC_USR.ALLEGATI_USECASE IS',
    "  'Documenti richiesti da ciascun UC. Struttura ereditata dal sistema Side con i nomi di",
    "   origine; aggiunte id_versione (baseline), ds_allegato (chiave di importazione) e il",
    "   riferimento al catalogo delle logiche per la condizione.';",
    'COMMENT ON COLUMN ANSC_USR.ALLEGATI_USECASE.ty_allegato IS',
    "  'Decodifica ANSC_09. E in chiave: le descrizioni senza codice vanno raccordate prima",
    "   del carico (OP-50).';",
    'COMMENT ON COLUMN ANSC_USR.ALLEGATI_USECASE.ty_configurazione IS',
    "  'DA VERIFICARE: semantica nella struttura di origine (OP-61).';",
])

# 7b — ALLEGATO: il contrassegno del documento extra
ddl_dopo('  ds_tipo_allegato     VARCHAR2(250 CHAR),',
         ['  fg_extra             CHAR(1 CHAR) DEFAULT \'0\' NOT NULL,'])
D.para(doc, mono('  CONSTRAINT allegato_pk PRIMARY KEY (id_allegato),')._p,
       "  CONSTRAINT allegato_fg_extra_check CHECK (fg_extra IN ('0','1')),", mono=True)

# 7c — ANSC_ANA_UC: il tipo evento
ddl_dopo('  COD_FAMIGLIA         VARCHAR2(30 CHAR)  NOT NULL,',
         ['  ID_TIPO_EVENTO       VARCHAR2(10 CHAR),'])

# 7d — ANSC_STATO_ATTO: fase, numero comunale, origine dell'UC
ddl_dopo('  COD_LOGICA              VARCHAR2(30 CHAR),', [
    '  COD_ORIGINE_UC          VARCHAR2(20 CHAR) DEFAULT \'AUTOMATICA\' NOT NULL,',
    '  COD_FASE                VARCHAR2(30 CHAR) DEFAULT \'IN_LAVORAZIONE\' NOT NULL,',
    '  NUM_COMUNALE            VARCHAR2(30 CHAR),',
])
ddl_dopo("  CONSTRAINT CK_ANSC_STATO_ATTO_FLG_EMERGENZA CHECK (FLG_EMERGENZA IN ('S','N')),", [
    '  CONSTRAINT CK_ANSC_STATO_ATTO_FASE',
    "    CHECK (COD_FASE IN ('IN_LAVORAZIONE','UC_DETERMINATO','DOCUMENTI_ACQUISITI',",
    "                        'PREVALIDATO','VALIDATO','FIRMATO','ANNULLATO')),",
    '  CONSTRAINT CK_ANSC_STATO_ATTO_ORIGINE_UC',
    "    CHECK (COD_ORIGINE_UC IN ('AUTOMATICA','OPERATORE')),",
])
fatti.append('Appendice A: ALLEGATI_USECASE, fg_extra, ID_TIPO_EVENTO, COD_FASE, NUM_COMUNALE')

# 7e — le schede dello store di stato
t = D.tabella_colonne(doc, 'ID_STATO_ATTO')
inserisci_riga(t, 'COD_LOGICA', (
    'COD_ORIGINE_UC', 'VARCHAR2(20)',
    'AUTOMATICA oppure OPERATORE: come l’UC è stato determinato. La seconda è ammessa solo in '
    'caso di ambiguità ed è il segnale di una configurazione da correggere.'))
inserisci_riga(t, 'COD_ORIGINE_UC', (
    'COD_FASE', 'VARCHAR2(30)',
    '⚠️ Fase della lavorazione locale: IN_LAVORAZIONE, UC_DETERMINATO, DOCUMENTI_ACQUISITI, '
    'PREVALIDATO, VALIDATO, FIRMATO, ANNULLATO. Non si confonde con STATO, che è la replica '
    'dello stato dichiarato da ANSC: la fase dice a che punto è il nostro percorso, lo stato '
    'dice che cosa ANSC ha registrato. Le due colonne cambiano in momenti diversi e una sola '
    'delle due ci appartiene.'))
inserisci_riga(t, 'ID_ANSC', (
    'NUM_COMUNALE', 'VARCHAR2(30)',
    'Numero comunale dell’atto, quello che il Comune assegna e che viaggia nel payload. '
    '⚠️ Sull’atto di stato civile di SIPO non esiste una colonna dedicata: va deciso se '
    'aggiungerla lì o se questa resti l’unica sede (OP-60), tenendo presente che '
    'l’allocazione in concorrenza è già aperta come OP-44.'))


# ═════════════════════════════════════ 8. requisiti, impatti, open point
t = D.trova_tabella(doc, 'id', 'requisito', 'nota')
D.clona_riga(t, ('RF-19', 'Al termine della lavorazione in SIPO l’UC deve risultare '
                 'identificato; la scelta da parte dell’operatore è ammessa soltanto quando '
                 'la configurazione è ambigua ed è registrata come tale.',
                 'La fase A non si chiude senza UC: campi, documenti e formule ne dipendono.'))
D.clona_riga(t, ('RF-20', 'Dopo la firma l’atto non è più modificabile in SIPO.',
                 'Le correzioni passano per gli istituti di ANSC. Il blocco è dell’atto in '
                 'SIPO, non soltanto del componente.'))
D.clona_riga(t, ('RF-21', 'Oltre ai documenti previsti dall’UC è ammesso allegare documenti '
                 'ulteriori, contrassegnati come tali.',
                 'Il pre-filtro non li verifica: ne registra la presenza senza trattarli come '
                 'requisiti soddisfatti.'))
D.clona_riga(t, ('RF-22', 'Ogni fase del percorso aggiorna lo stato dell’atto.',
                 'COD_FASE per la lavorazione locale, STATO per la replica di ciò che ANSC '
                 'dichiara.'))

t = D.trova_tabella(doc, 'schermata / componente', 'tipo intervento')
D.clona_riga(t, ('Lavorazione dell’atto — atto firmato', 'Blocco della maschera',
                 'Dopo la firma le maschere di compilazione non consentono più modifiche e '
                 'mostrano lo stato ANSC dell’atto con le azioni ancora possibili.', 'Alta'))
D.clona_riga(t, ('Lavorazione dell’atto — UC ambiguo', 'Maschera nuova',
                 'Nel solo caso di ambiguità, elenco degli UC candidati con la descrizione '
                 'pubblicata da ANSC e la logica che li ha selezionati, per la scelta '
                 'dell’operatore.', 'Media'))

t = D.trova_tabella(doc, '#', 'tema', 'questione')
for num, tema, questione, owner, prio in [
    ('OP-60', 'Numero comunale dell’atto in SIPO',
     'Sull’atto di stato civile non esiste una colonna dedicata al numero comunale: MATR_USR '
     'porta NUMERO_ATTO con parte e serie, mentre NUMERO_COMUNALE sta sull’ATTO di anagrafe e '
     'vi è valorizzata scomponendo l’identificativo di un atto formato altrove. Va deciso dove '
     'risiede il numero che trasmettiamo. Da chiudere insieme a OP-29 e OP-44.',
     'Cliente / Sistemi Informativi', 'Alta'),
    ('OP-61', 'Semantica delle colonne ereditate della configurazione allegati',
     'Nella struttura di Side ty_presenza e ty_configurazione non hanno valori dichiarati nel '
     'file ricevuto. Servono i domini ammessi prima di importare il mapping, altrimenti la '
     'configurazione nasce con due colonne che nessuno sa leggere.',
     'Analisi / Fornitore Side', 'Media'),
]:
    D.clona_riga(t, (num, tema, questione, 'Aperto', owner, prio))
fatti.append('RF-19…22, due impatti FE, OP-60 e OP-61')


# ═════════════════════════════════════ 9. rinomine e figure
n = D.sostituisci(doc, 'ANSC_CFG_ALLEGATO', 'ALLEGATI_USECASE')
fatti.append(f'ANSC_CFG_ALLEGATO → ALLEGATI_USECASE in {n} punti')
D.sostituisci_immagine(doc, 'Schema ANSC_USR.', os.path.join(IMG, 'erd_ansc_usr.png'))
D.sostituisci_immagine(doc, 'Dalla maschera SIPO al payload ANSC.',
                       os.path.join(IMG, 'catena_configurazione.png'))
fatti.append('ERD e catena rigenerati')

doc.save(DST)

# ────────────────────────────────────────────── controlli
import zipfile   # noqa: E402
z = zipfile.ZipFile(DST)
xml = z.read('word/document.xml').decode()
ncom = z.read('word/comments.xml').decode().count('<w:comment ')
assert ncom == 27, f'commenti persi: {ncom} invece di 27'
assert 'ANSC_CFG_ALLEGATO' not in xml or xml.count('ANSC_CFG_ALLEGATO') <= 2, \
    'restano riferimenti ad ANSC_CFG_ALLEGATO fuori dalla storia'
d2 = docx.Document(DST)
for p in d2.paragraphs:
    if p.style.name.startswith('Heading') and len(p.text) > 95:
        raise SystemExit('heading anomalo: ' + p.text[:70])
print('\n'.join(' · ' + f for f in fatti))
print('commenti:', ncom, '· capitoli/tabelle/immagini:', D.riepilogo(DST))
print('scritto:', os.path.relpath(DST, BASE))
