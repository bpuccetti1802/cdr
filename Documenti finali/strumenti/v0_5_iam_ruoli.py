# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.4 → v0.5 (13/10/2026).

Nuovo capitolo «I ruoli: che cosa porta IAM e come si introducono», chiesto dal
committente che vuole introdurre un meccanismo di gestione dei ruoli.

Tutto ciò che il capitolo afferma su IAM è verificato sul manuale [F4] (Edizione 16 del
23/06/2025), estratto con `strumenti/estrai_pdf.py`; tutto ciò che afferma su SIPO è
verificato sui sorgenti, con il riferimento file:riga.

⚠️ Il manuale è un PDF con font a sottoinsiemi: non è greppabile, e una mappa
`codice → carattere` unica per documento restituisce testo sbagliato (`iv-portal-groups`
diventa `iQ-porPMl-groups`). Le citazioni vengono dall'estrazione per font.

Decisioni del committente recepite:
  · il codice fiscale si prende dall'**header** (PI-06 chiuso in positivo: il manuale lo
    dichiara «garantito» nella variabile iv-codfis);
  · la soglia della matrice iniziale è **10 % / 90 %**;
  · il bivio fra una matrice di capacità o due **resta aperto**: si riportano entrambe le
    possibilità, in attesa di decisione (PI-27).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_5_iam_ruoli.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.4.docx')
DST = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.5.docx')


# ----------------------------------------------------------------------- contenuti

PORTA = [
    ['Che cosa', 'Modalità header (quella di oggi)', 'Modalità OIDC'],
    ['identità della persona',
     'iv-user (username), iv-codfis (codice fiscale)',
     'sub (username) e il claim iv_codfis dello scope profile'],
    ['nome e cognome', 'iv-nome, iv-cognome, iv-fullname',
     'iv_nome, iv_cognome (scope profile)'],
    ['gruppi di appartenenza',
     '**iv-portal-groups**: «elenco dei gruppi LDAP a cui appartiene l’utente»',
     '**nessuno**: gli scope pubblicati non contengono i gruppi'],
    ['tipo di utente',
     'sysgroup (identificati / interniIdentificati) — ⚠️ non è in Tabella 2',
     'iv_tipoutente (scope tipo_utente): cittadino oppure dipendente'],
    ['ruoli applicativi', '**nessuno**', '**nessuno**'],
]

TRE = [
    ['Riscontro', 'Che cosa dice la fonte', 'Conseguenza sul disegno'],
    ['Il codice fiscale è garantito',
     '«Il codice fiscale dell’utente viene garantito nella variabile iv-codfis» [F4] §3.2.',
     'PI-06 si chiude in positivo: la chiave di ricerca su UTENTI può essere il codice '
     'fiscale dell’header. Resta da togliere l’asimmetria del filtro, che oggi lo legge '
     'solo per i cittadini.'],
    ['In OIDC il sub di un dipendente non è il codice fiscale',
     'Il claim sub «conterrà lo username dell’utente: codice fiscale per i cittadini e '
     'una stringa del tipo nome.cognome per i dipendenti» [F4] §3.9.2.1.',
     '⚠️ Un disegno che usasse sub come chiave su UTENTI sbaglierebbe per tutti gli '
     'operatori. La chiave è il claim iv_codfis, non il sub.'],
    ['La disponibilità delle variabili è una policy, non un dato di fatto',
     '«Per ciascuna web application … possono essere definite delle policy che rendano o '
     'meno disponibili alcune delle informazioni» e «le variabili disponibili per '
     'ciascuna applicazione dovranno essere ridotte a quelle strettamente '
     'indispensabili» [F4] §3.2.',
     'Che iv-portal-groups arrivi a SIPO non si deduce dal manuale: si verifica. '
     'Vedi «La verifica preliminare».'],
    ['Esiste un dominio pensato per back-end e SPA',
     '«È opportuno che tali servizi di backend vengano esposti tramite il dominio '
     'ws.comune.roma.it»; vi sono disponibili le stesse header-variables, purché le '
     'richieste del client inoltrino i cookie [F4] §3.1.1.',
     'Le applicazioni Angular possono avere la stessa identità degli altri front-end '
     'senza passare da OIDC. È un’alternativa alla soluzione con gettone, da valutare '
     'con PI-19.'],
    ['sysgroup non è documentato',
     'La variabile non compare nella Tabella 2 né altrove nel manuale.',
     '⚠️ SIPO decide cittadino/dipendente su un header che la specifica IAM non '
     'dichiara. Passando a OIDC va sostituito con iv_tipoutente.'],
]

QUATTRO_NOMI = [
    ['Nome', 'Dove sta', 'Che cos’è'],
    ['CONF_RUOLI.ID', 'ANAG_USR', 'La chiave numerica. ⚠️ Non è un dettaglio interno: '
     'l’ordinamento per ID decide quale ruolo il front-end usa.'],
    ['CONF_RUOLI.DESCRIZIONE', 'ANAG_USR, VARCHAR2(50)', 'L’etichetta per le persone.'],
    ['CONF_RUOLI.RUOLO', 'ANAG_USR',
     'Il nome tecnico. ⚠️ La colonna esiste nella tabella e la query nativa di '
     'UtentiDao la seleziona (cr.ruolo), ma l’entity JPA ConfRuoli mappa solo ID e '
     'DESCRIZIONE: chi lavora con l’entity non sa che c’è.'],
    ['CONF_APP_ROLE.PROFILO_BE', 'ANAG_USR',
     'La proiezione del ruolo su un’utenza tecnica. È ciò che determina l’autorità che '
     'i back-end verificano.'],
]

PROTEGGONO = [
    ['Misura', 'Valore', 'Che cosa significa'],
    ['annotazioni @PreAuthorize nei back-end', '3.360',
     'Il presidio esiste ed è diffuso.'],
    ['citazioni di ROLE_ADMIN / ROLE_AUTH_USER', '3.129 / 3.126',
     '⚠️ L’autorità verificata nella grande maggioranza dei casi è quella di '
     '«un’utenza tecnica autenticata», non il ruolo della persona.'],
    ['citazioni di ruoli di dominio',
     'ROLE_CITTADINO 1.404 · ROLE_UFF_CERT_CORR 966 · ROLE_UFF_CERT_ENTI_EST 965 · '
     'ROLE_DIR 88 · ROLE_FUNZ_ANA 68',
     'La discriminazione per ruolo esiste, ma è concentrata su certificati, anagrafe e '
     'elettorale.'],
    ['occorrenze di getRuoli().get(0) nei front-end', '4.829',
     '⚠️ Il ruolo che conta è il primo per ID, e la scelta è posizionale.'],
    ['occorrenze di getRuoloBe() nei front-end', '4.781',
     'È il valore con cui il front-end sceglie l’utenza tecnica verso il back-end.'],
    ['uso di User.isMultiProfilo', '0',
     '⚠️ Il campo è dichiarato nel modello e non è usato da nessuna parte: il '
     'multi-ruolo è previsto e non governato.'],
]

MATRICE_BANDE = [
    ['Quota di utenti del ruolo che ha la funzionalità', 'Dove va', 'Perché'],
    ['90 % o più', 'in matrice con FLG_PREDEFINITA = S',
     'È di fatto già una capacità del ruolo: l’eccezione è chi non la ha, non chi la ha.'],
    ['fra il 10 % e il 90 %', 'in matrice con FLG_PREDEFINITA = N',
     'La concede il funzionario caso per caso. È la banda in cui serve il giudizio, e '
     'per questo non si decide con una soglia.'],
    ['meno del 10 %', 'fuori dalla matrice, resta COD_ORIGINE = AGGIUNTA',
     'È un’eccezione, e va continuata a trattare come tale invece di essere promossa a '
     'regola.'],
]

BIVIO = [
    ['', 'A — due matrici di capacità', 'B — una matrice sola'],
    ['Come',
     'Il vecchio mondo usa CONF_RUOLO_FUNZIONALITA in ANAG_USR; il back-office ANSC '
     'continua con ANSC_CFG_PAGINA_ABILITAZ in ANSC_USR. Il registro dei ruoli è uno '
     'solo, citato per valore tramite CONF_RUOLI.RUOLO.',
     'Le pagine del back-office si registrano come CONF_FUNZIONALITA di un’area '
     'tematica, e ANSC_CFG_PAGINA_ABILITAZ sparisce: la capacità sta in un posto solo.'],
    ['A favore',
     'Rispetta le due regole di impianto già adottate: nessuna chiave esterna attraversa '
     'gli schemi, e ogni tabella del modello ANSC ha una pagina che la governa. I domini '
     'di guasto restano separati: un fermo di ANAG_USR non spegne il menu del '
     'back-office.',
     'Un solo posto in cui si legge «che cosa può un ruolo», quindi nessun rischio di '
     'divergenza. Il menu di tutte le applicazioni, vecchie e nuove, si amministra da '
     'un’unica schermata.'],
    ['Contro',
     'La stessa domanda ha due risposte in due schemi: allinearle è un adempimento, e '
     'gli adempimenti si dimenticano.',
     '⚠️ Il back-office nuovo diventa dipendente da uno schema in esercizio per '
     'disegnare il proprio menu, e la pagina «Pagine e menu» del disegno del back-office '
     'perde la tabella che governa. Va anche deciso chi registra le pagine Angular in '
     'CONF_FUNZIONALITA, che ha URL_PAGE di 50 caratteri.'],
    ['Quando conviene',
     'Se si vuole che il back-office resti rilasciabile e diagnosticabile da solo.',
     'Se si vuole che «gestione dei ruoli» significhi davvero una schermata sola.'],
]

MODIFICHE = [
    ['File (tutti in common/profilazione-utente)', 'Modifica', 'Righe'],
    ['resources/properties/portale.properties',
     'cdr.portale.groupsHeaderParam = iv-portal-groups', '1'],
    ['portale/Constants.java', 'La costante corrispondente.', '1'],
    ['portale/CdRLoginFilter.java',
     'Leggere la variabile, spezzare i path LDAP e tenere i soli cn=. ⚠️ Valorizzarla '
     'anche nel ramo del dipendente: oggi setHeaderParam() è invocata solo nel ramo del '
     'cittadino, e per questo il codice fiscale dell’header non è mai arrivato agli '
     'operatori.', 'circa 10'],
    ['model/User.java',
     'Il campo dei gruppi, con i suoi accessori. Da qui ogni pagina di ogni front-end lo '
     'vede, perché User sta in sessione come LOGIN_USER.', 'circa 8'],
    ['dao/UtentiDao.java',
     'La ricerca per codice fiscale invece che per NOME_UTENTE, e l’ordinamento per '
     'FLG_PRINCIPALE (vedi «Il primo ruolo»).', 'circa 6'],
]

MINIMIZZARE = [
    ['Accorgimento', 'Perché'],
    ['Solo aggiunte, nessuna sostituzione',
     'Nessun campo esistente cambia nome o significato. Se la variabile non arriva, '
     'l’elenco dei gruppi è vuoto e nessuna pagina esistente si accorge di nulla.'],
    ['Il raggio di ricompilazione si sceglie',
     'La catena è front-end → CommonWeb → ProfilazioneUtente. Essendo la modifica '
     'additiva, si ricompilano **solo i front-end che ospitano pagine ANSC**: da '
     'trentacinque rilasci a due o tre.'],
    ['Alzare la versione del jar prima di toccarlo',
     '⚠️ RI-28: l’impianto esiste in due copie con lo stesso identificativo di '
     'artefatto. Pubblicando il jar nuovo con la stessa versione, quale finisce nella '
     'build dipende dall’ordine di installazione.'],
    ['La decisione non va nei trentacinque front-end',
     'Il gruppo è un cancello, e un cancello si mette dove si entra: nelle pagine nuove '
     'e nel back-office, non sparso nei controller.'],
    ['Il gettone porta tutte e tre le forme',
     'ruoli, profiloBe e abilitazioni viaggiano insieme: i back-end vecchi continuano '
     'con l’utenza tecnica, i nuovi autorizzano sui ruoli, il back-office filtra il menu '
     'sulle abilitazioni. Si lega a PI-20.'],
]

VERIFICA = [
    ['Se risulta', 'Conseguenza sul disegno'],
    ['iv-codfis presente per i dipendenti',
     'La ricerca su UTENTI passa al codice fiscale, e il gettone lo marca con origine '
     '«header di IAM».'],
    ['iv-codfis assente',
     'Si resta su NOME_UTENTE e il codice fiscale si legge dal database, con origine '
     '«base dati». La differenza resta dichiarata invece di essere taciuta.'],
    ['iv-portal-groups presente',
     'I gruppi diventano il cancello di accesso, e serve la convenzione dei nomi '
     '(PI-24).'],
    ['iv-portal-groups assente',
     'Va chiesto a IAM come variabile in modalità header, o come claim in OIDC (PI-26). '
     'Nel frattempo il cancello resta il ruolo di SIPO.'],
    ['header e base dati divergono',
     'Va deciso quale fonte fa fede e la divergenza va segnalata al momento della '
     'login, non risolta in silenzio.'],
]

DDL_MATRICE = [
    "CREATE TABLE CONF_RUOLO_FUNZIONALITA (",
    "  ID                NUMBER(10)   GENERATED AS IDENTITY,",
    "  ID_RUOLO          NUMBER(10)   NOT NULL,   -- CONF_RUOLI.ID",
    "  ID_AREA_TEMATICA  NUMBER(10)   NOT NULL,   -- CONF_AREE_TEMATICHE.ID_AREE_TEMATICHE",
    "  ID_FUNZIONALITA   NUMBER(10)   NOT NULL,   -- CONF_FUNZIONALITA.ID",
    "  FLG_PREDEFINITA   CHAR(1)      DEFAULT 'S' NOT NULL,",
    "  DATA_INS          DATE,        UTENTE_INS VARCHAR2(50),",
    "  DATA_UPD          DATE,        UTENTE_UPD VARCHAR2(50),",
    "  CONSTRAINT PK_CONF_RUOLO_FUNZIONALITA PRIMARY KEY (ID),",
    "  CONSTRAINT UK_CONF_RUOLO_FUNZ UNIQUE (ID_RUOLO, ID_AREA_TEMATICA, ID_FUNZIONALITA),",
    "  CONSTRAINT CK_CONF_RUOLO_FUNZ_PRED CHECK (FLG_PREDEFINITA IN ('S','N'))",
    ");",
    "",
    "-- R_UTENTI_RUOLI diventa una proiezione della matrice, senza cambiare forma",
    "ALTER TABLE R_UTENTI_RUOLI ADD (",
    "  COD_ORIGINE     VARCHAR2(10) DEFAULT 'DERIVATA' NOT NULL,  -- DERIVATA|AGGIUNTA|RIMOSSA",
    "  FLG_PRINCIPALE  CHAR(1)      DEFAULT 'N'        NOT NULL",
    ");",
]

DDL_SCOPERTA = [
    "-- La matrice iniziale si ricava dalle abilitazioni che esistono gia'.",
    "SELECT r.ID_RUOLO, r.ID_AREA_TEMATICA, r.ID_FUNZIONALITA,",
    "       COUNT(DISTINCT r.ID_UTENTE)                            utenti_con,",
    "       tot.utenti                                             utenti_del_ruolo,",
    "       ROUND(100 * COUNT(DISTINCT r.ID_UTENTE) / tot.utenti)  percentuale",
    "  FROM R_UTENTI_RUOLI r",
    "  JOIN (SELECT ID_RUOLO, COUNT(DISTINCT ID_UTENTE) utenti",
    "          FROM R_UTENTI_RUOLI GROUP BY ID_RUOLO) tot",
    "    ON tot.ID_RUOLO = r.ID_RUOLO",
    " GROUP BY r.ID_RUOLO, r.ID_AREA_TEMATICA, r.ID_FUNZIONALITA, tot.utenti",
    " ORDER BY r.ID_RUOLO, percentuale DESC;",
]

PUNTI_NUOVI = [
    ('PI-24', 'Se l’Access Manager di IAM mandi a SIPO la variabile iv-portal-groups, e '
              'con quali nomi di gruppo. Il manuale la prevede ma la disponibilità '
              'dipende dalla policy configurata per l’applicazione; oggi SIPO non la '
              'legge in nessun punto. Si chiude con la pagina di verifica degli header, '
              'su un ambiente di pre-esercizio.',
     'Presidio IAM / Referenti SIPO'),
    ('PI-25', 'Chi amministra l’appartenenza ai gruppi LDAP e con quali tempi di '
              'modifica. Oggi un operatore si abilita dalla schermata di gestione degli '
              'utenti; se l’appartenenza passasse a IAM, ogni cambio di mansione '
              'diventerebbe una richiesta a un altro presidio.',
     'Dipartimento / Presidio IAM'),
    ('PI-26', 'Se in modalità OIDC i gruppi si possano ottenere come claim. Il manuale '
              'dichiara che ogni claim fa riferimento a un attributo della Tabella 2, ma '
              'gli scope pubblicati oggi non li contengono. Da aprire adesso, perché la '
              'risposta ha un tempo di attraversamento non nostro.',
     'Presidio IAM'),
    ('PI-27', 'Se la capacità dei ruoli debba stare in due matrici, una per mondo e '
              'ciascuna nel proprio schema, oppure in una sola, registrando anche le '
              'pagine del back-office come funzionalità. Le due possibilità sono '
              'riportate per esteso nel capitolo dei ruoli; la scelta cambia la pagina '
              '«Pagine e menu» del disegno del back-office.',
     'Architettura / Referenti SIPO'),
    ('PI-28', 'Chi approva la matrice ruolo-funzionalità ricavata dalle abilitazioni '
              'esistenti, e chi la mantiene nel tempo. È la stessa classe di questione '
              'della responsabilità di attivare una configurazione: il meccanismo lo '
              'forniamo, la delega no.',
     'Dipartimento / USC'),
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    modello = d.tables[3]          # Riferimenti: tabella a tre colonne, bordi giusti
    fine = d.element.body[-1]      # il sectPr finale: si innesta tutto prima

    def P(testo='', **kw):
        return D.para(d, fine, testo, **kw)

    def H(livello, testo):
        stile = 'Heading %d' % livello
        p = D.para(d, fine, testo, stile=stile)
        return p

    def V(testa, corpo):
        return D.voce(d, fine, testa, corpo)

    def T(righe, larghezze=None):
        return D.tabella(d, fine, righe, modello, larghezze)

    # =================================================================== capitolo
    H(1, 'I ruoli: che cosa porta IAM e come si introducono')
    P('Il committente chiede di introdurre un meccanismo di gestione dei ruoli. La '
      'domanda che decide il disegno è se i ruoli li porti IAM: se li portasse, il '
      'meccanismo sarebbe una configurazione; se non li porta, va costruito. Questo '
      'capitolo risponde con le fonti alla mano, descrive come si introduce il '
      'meccanismo senza riscrivere ciò che funziona, e dichiara ciò che resta da '
      'decidere.')

    H(2, 'Che cosa porta IAM, e che cosa non porta')
    P('La risposta è che IAM porta **gruppi**, non ruoli applicativi, e li porta in modo '
      'diverso nelle due modalità di integrazione.',
      pezzi=D.segmenta('', 'La risposta è che IAM porta **gruppi**, non ruoli '
                           'applicativi, e li porta in modo diverso nelle due modalità '
                           'di integrazione.'))
    T(PORTA, [1.5, 2.4, 2.4])
    P('Sui gruppi il manuale è esplicito anche sull’uso che se ne può fare: '
      'l’appartenenza «può essere utilizzata come elemento per stabilire '
      '**macroscopicamente** se l’utente è abilitato o meno ad usufruire di una '
      'determinata funzione o ad accedere ad una determinata applicazione» [F4] §3.2. '
      'La parola «macroscopicamente» è la misura del loro impiego: un cancello, non un '
      'permesso.',
      pezzi=D.segmenta('', 'Sui gruppi il manuale è esplicito anche sull’uso che se ne '
                           'può fare: l’appartenenza «può essere utilizzata come elemento '
                           'per stabilire **macroscopicamente** se l’utente è abilitato o '
                           'meno ad usufruire di una determinata funzione o ad accedere ad '
                           'una determinata applicazione» [F4] §3.2. La parola '
                           '«macroscopicamente» è la misura del loro impiego: un '
                           'cancello, non un permesso.'))
    P('Il formato della variabile va riportato perché contiene una trappola. I gruppi '
      'sono separati da virgola; le componenti del path LDAP di ciascun gruppo dalla '
      'sequenza backslash-virgola:')
    D.ddl(d, fine, [
        "cn=gruppo1\\,ou=Groups\\,dc=cdr\\,dc=it,cn=gruppo2\\,ou=Groups\\,dc=cdr\\,dc=it",
    ])
    P('Una divisione ingenua sulla virgola spezza ogni gruppo in quattro pezzi: la '
      'virgola da usare è quella non preceduta da backslash. Sul formato dichiarato dal '
      'manuale, la prima produce otto frammenti, la seconda i due gruppi giusti.')
    P('Oltre ai gruppi, la lettura del manuale ha prodotto quattro riscontri che '
      'cambiano il disegno, e uno che chiude un punto aperto.')
    T(TRE, [1.4, 2.5, 2.4])

    H(2, 'Perché i gruppi LDAP non possono fare i ruoli di SIPO')
    P('Anche nell’ipotesi migliore — la variabile arriva, i nomi dei gruppi sono utili — '
      'i gruppi non possono sostituire i ruoli di SIPO, per tre ragioni di cui l’ultima '
      'è decisiva.')
    V('Granularità. ', 'Il manuale li qualifica come criterio macroscopico: accesso a '
      'un’applicazione o a una macro-funzione. I permessi di SIPO sono per utente, '
      'area tematica e funzionalità.')
    V('Forma. ', 'Sono path LDAP, senza alcuna relazione con CONF_RUOLI.RUOLO. '
      'Servirebbe una tabella di raccordo da mantenere per sempre.')
    V('Governo. ', 'L’appartenenza ai gruppi la amministra il presidio LDAP dell’ente. '
      'Oggi un operatore si abilita dalla schermata di gestione degli utenti; con i '
      'gruppi ogni cambio di mansione diventerebbe una richiesta a un altro presidio, '
      'con i suoi tempi.')
    P('C’è però un argomento più forte dei tre, e vale la pena metterlo in evidenza '
      'perché rende la decisione indipendente dalla risposta di IAM: **i gruppi '
      'potrebbero sostituire al massimo l’appartenenza, mai la capacità.** Nessun gruppo '
      'LDAP saprà mai che un certo ruolo può accedere a una certa funzionalità di una '
      'certa area: quella frase non esiste in nessun sistema dell’ente, e va scritta da '
      'noi in ogni scenario. Il lavoro descritto nel resto del capitolo serve quindi sia '
      'che i gruppi arrivino sia che non arrivino.',
      pezzi=D.segmenta('', 'C’è però un argomento più forte dei tre, e vale la pena '
                           'metterlo in evidenza perché rende la decisione indipendente '
                           'dalla risposta di IAM: **i gruppi potrebbero sostituire al '
                           'massimo l’appartenenza, mai la capacità.** Nessun gruppo LDAP '
                           'saprà mai che un certo ruolo può accedere a una certa '
                           'funzionalità di una certa area: quella frase non esiste in '
                           'nessun sistema dell’ente, e va scritta da noi in ogni '
                           'scenario. Il lavoro descritto nel resto del capitolo serve '
                           'quindi sia che i gruppi arrivino sia che non arrivino.'))
    P('La ripartizione che il documento propone è dunque quella della decisione D2, ora '
      'con la prova del manuale invece dell’ipotesi: IAM dice chi sei e, se la policy lo '
      'concede, a quali gruppi appartieni; SIPO dice che cosa puoi fare.')

    H(2, 'Lo stato di fatto: un ruolo, quattro nomi')
    P('Prima di aggiungere qualcosa conviene dire con precisione che cosa c’è, perché il '
      'modello dei ruoli di SIPO è più sottile di come viene descritto. Lo stesso ruolo '
      'ha quattro nomi, in quattro posti.')
    T(QUATTRO_NOMI, [1.8, 1.5, 3.0])
    P('Per avere una nomenclatura identica fra il vecchio e il nuovo — che è un obiettivo '
      'dichiarato del committente — va sciolto prima questo nodo. La proposta è: **RUOLO '
      'è l’identificatore** che il mondo nuovo cita, **DESCRIZIONE è l’etichetta**, e '
      '**PROFILO_BE è un dettaglio di trasporto del vecchio mondo che il nuovo non deve '
      'conoscere affatto**.',
      pezzi=D.segmenta('', 'Per avere una nomenclatura identica fra il vecchio e il nuovo '
                           '— che è un obiettivo dichiarato del committente — va sciolto '
                           'prima questo nodo. La proposta è: **RUOLO è l’identificatore** '
                           'che il mondo nuovo cita, **DESCRIZIONE è l’etichetta**, e '
                           '**PROFILO_BE è un dettaglio di trasporto del vecchio mondo che '
                           'il nuovo non deve conoscere affatto**.'))

    H(2, 'Il permesso è una quaterna, non un’appartenenza')
    P('La tabella R_UTENTI_RUOLI ha quattro chiavi esterne, tutte obbligatorie:')
    D.ddl(d, fine, [
        "ID_UTENTE  x  ID_RUOLO  x  ID_AREA_TEMATICA  x  ID_FUNZIONALITA",
    ])
    P('Il ruolo **qualifica** il permesso ma non lo contiene. Le conseguenze vanno dette '
      'prima di promettere una gestione dei ruoli.',
      pezzi=D.segmenta('', 'Il ruolo **qualifica** il permesso ma non lo contiene. Le '
                           'conseguenze vanno dette prima di promettere una gestione dei '
                           'ruoli.'))
    V('Non esiste la frase «il ruolo X può fare Y». ', 'Esiste «l’utente U, nel ruolo X, '
      'può fare Y nell’area A». Due utenti con lo stesso ruolo possono avere permessi '
      'diversi, e di fatto li hanno.')
    V('Un meccanismo classico non è una configurazione da aggiungere. ', 'Permessi sul '
      'ruolo e utenti nel ruolo sono un modello diverso da quello in esercizio: '
      'introdurlo è un intervento sul modello dati, non una schermata nuova.')
    V('Il costo è tutto sull’abilitazione. ', 'Ogni utente nuovo va abilitato '
      'funzionalità per funzionalità, ed è esattamente il lavoro che il committente '
      'vuole togliere.')

    H(2, 'Che cosa i ruoli proteggono oggi: il menu, non i servizi')
    P('Questo paragrafo corregge un’impressione diffusa, e i numeri vengono dal conteggio '
      'sui sorgenti.')
    T(PROTEGGONO, [2.2, 1.6, 2.5])
    P('La catena completa, verificata, è questa: il front-end prende il primo ruolo '
      'dell’utente, ne legge il PROFILO_BE, con quello sceglie una utenza tecnica dal '
      'file di configurazione del client, ottiene un gettone per quell’utenza e chiama '
      'il back-end, che verifica l’autorità **dell’utenza tecnica**. La persona non '
      'compare in nessun passaggio di quella catena.',
      pezzi=D.segmenta('', 'La catena completa, verificata, è questa: il front-end prende '
                           'il primo ruolo dell’utente, ne legge il PROFILO_BE, con quello '
                           'sceglie una utenza tecnica dal file di configurazione del '
                           'client, ottiene un gettone per quell’utenza e chiama il '
                           'back-end, che verifica l’autorità **dell’utenza tecnica**. La '
                           'persona non compare in nessun passaggio di quella catena.'))
    P('⚠️ E il menu ha uno strato cablato sopra il dato: il metodo che riceve le aree '
      'tematiche decide le macro-sezioni con identificativi numerici scritti nel codice '
      '(l’ambito dello stato civile, un elenco di aree per il dipartimento, un altro per '
      'i municipi, e sette esclusioni per l’elettorale). Aggiungere un’area o una '
      'funzionalità non accende il menu da sola: è il motivo per cui le pagine nuove '
      'conviene registrarle in un’area esistente dell’ambito dello stato civile.')

    H(2, 'Come si introducono: due livelli, un registro')
    P('Il meccanismo da introdurre non è un registro nuovo: è il livello che manca fra i '
      'due che esistono.')
    T([['Livello', 'Che cosa dice', 'Dove sta oggi'],
       ['Appartenenza', 'Quali ruoli ha una persona.',
        'R_UTENTI_RUOLI, amministrata dalla schermata di gestione degli utenti: **c’è**.'],
       ['Capacità', 'Che cosa può un ruolo.',
        '**Non c’è**: è ciò che si introduce.']], [1.3, 2.0, 3.0])
    P('La tabella nuova e le due colonne che la rendono adottabile senza rifacimenti:')
    D.ddl(d, fine, DDL_MATRICE)
    P('⚠️ Nota di nomenclatura, perché è una scelta e non una dimenticanza: questa '
      'tabella segue la convenzione del **vecchio** mondo e non lo standard dei nomi '
      'adottato per lo schema del nuovo componente. Vive in ANAG_USR accanto a '
      'CONF_RUOLI e CONF_FUNZIONALITA, e la nomenclatura la detta lo schema che ospita, '
      'non il documento che la descrive. Collocarla nello schema nuovo sarebbe l’errore '
      'di impianto.',
      pezzi=D.segmenta('', '⚠️ Nota di nomenclatura, perché è una scelta e non una '
                           'dimenticanza: questa tabella segue la convenzione del '
                           '**vecchio** mondo e non lo standard dei nomi adottato per lo '
                           'schema del nuovo componente. Vive in ANAG_USR accanto a '
                           'CONF_RUOLI e CONF_FUNZIONALITA, e la nomenclatura la detta lo '
                           'schema che ospita, non il documento che la descrive. '
                           'Collocarla nello schema nuovo sarebbe l’errore di impianto.'))
    P('Il meccanismo è che **assegnare un ruolo espande le righe** dalla matrice. La '
      'colonna COD_ORIGINE distingue le righe derivate da quelle messe a mano: è la '
      'stessa primitiva già adottata per la configurazione dei campi del nuovo '
      'componente, e serve allo stesso scopo — cambiare regime senza perdere il lavoro '
      'fatto. La riassegnazione riscrive solo le righe derivate; le eccezioni restano, '
      'sono visibili e si possono elencare.',
      pezzi=D.segmenta('', 'Il meccanismo è che **assegnare un ruolo espande le righe** '
                           'dalla matrice. La colonna COD_ORIGINE distingue le righe '
                           'derivate da quelle messe a mano: è la stessa primitiva già '
                           'adottata per la configurazione dei campi del nuovo '
                           'componente, e serve allo stesso scopo — cambiare regime senza '
                           'perdere il lavoro fatto. La riassegnazione riscrive solo le '
                           'righe derivate; le eccezioni restano, sono visibili e si '
                           'possono elencare.'))
    P('⚠️ E il contratto a runtime non cambia di una virgola. I trentacinque front-end e '
      'la query che carica le aree tematiche continuano a leggere R_UTENTI_RUOLI per '
      'utente: nessuna query da riscrivere, nessun front-end da ricompilare per questo, '
      'nessuna delle 3.360 annotazioni toccata. Il ruolo diventa l’**unità di '
      'amministrazione**; la riga per utente resta l’**unità di esecuzione**. È questo '
      'che rende l’intervento proporzionato invece che un rifacimento.',
      pezzi=D.segmenta('', '⚠️ E il contratto a runtime non cambia di una virgola. I '
                           'trentacinque front-end e la query che carica le aree '
                           'tematiche continuano a leggere R_UTENTI_RUOLI per utente: '
                           'nessuna query da riscrivere, nessun front-end da ricompilare '
                           'per questo, nessuna delle 3.360 annotazioni toccata. Il ruolo '
                           'diventa l’**unità di amministrazione**; la riga per utente '
                           'resta l’**unità di esecuzione**. È questo che rende '
                           'l’intervento proporzionato invece che un rifacimento.'))

    H(2, 'La matrice iniziale si ricava dai dati, non si scrive a mano')
    P('Le abilitazioni esistenti sono il frutto di anni di decisioni: dicono loro quale '
      'sia la matrice. La si ricava con una interrogazione sola, che per ciascun ruolo '
      'misura quanta parte dei suoi utenti ha una data funzionalità.')
    D.ddl(d, fine, DDL_SCOPERTA)
    P('Le soglie adottate sono il dieci e il novanta per cento, e la banda centrale è la '
      'parte che conta.')
    T(MATRICE_BANDE, [2.4, 2.2, 3.0])
    P('⚠️ Prima di cambiare regime va prodotto il **report di differenza**: per ciascun '
      'utente, che cosa guadagnerebbe e che cosa perderebbe passando dalla matrice. '
      'Nessuno gira l’interruttore senza averlo letto. È lo stesso presidio già previsto '
      'per l’attivazione di una configurazione nuova, e per la stessa ragione: una '
      'migrazione di permessi che nessuno ha guardato riga per riga toglie a qualcuno '
      'una funzione di cui ha bisogno, e lo si scopre allo sportello.',
      pezzi=D.segmenta('', '⚠️ Prima di cambiare regime va prodotto il **report di '
                           'differenza**: per ciascun utente, che cosa guadagnerebbe e che '
                           'cosa perderebbe passando dalla matrice. Nessuno gira '
                           'l’interruttore senza averlo letto. È lo stesso presidio già '
                           'previsto per l’attivazione di una configurazione nuova, e per '
                           'la stessa ragione: una migrazione di permessi che nessuno ha '
                           'guardato riga per riga toglie a qualcuno una funzione di cui '
                           'ha bisogno, e lo si scopre allo sportello.'))

    H(2, 'Il primo ruolo, e la riga che lo rende deterministico')
    P('Introdurre i ruoli rende il multi-ruolo normale, e qui c’è un rischio concreto. '
      'Oggi il ruolo che conta è il primo per identificativo, in 4.829 punti, e gli '
      'identificativi dei ruoli esistenti vanno da uno a otto. Creare un ruolo nuovo con '
      'un identificativo basso cambierebbe, in silenzio, l’utenza tecnica di tutte le '
      'chiamate degli utenti che lo ricevono.')
    V('Regola operativa. ', 'I ruoli nuovi prendono un identificativo alto, e se un '
      'operatore riceve il ruolo nuovo **in aggiunta**, il suo primo ruolo deve restare '
      'quello di oggi.')
    V('Correzione strutturale. ', 'La colonna FLG_PRINCIPALE su R_UTENTI_RUOLI e un '
      'ordinamento per quella colonna nella query che carica i ruoli. I 4.829 punti '
      'continuano a funzionare identici e **diventano deterministici**: non è più «il '
      'primo per caso», è «quello designato». Una riga di SQL che dà senso a quasi '
      'cinquemila punti di codice senza toccarne nessuno.')
    P('Se poi si vuole che l’operatore **scelga** con quale ruolo opera, il campo che '
      'segnala il multi-profilo è già nel modello e non è usato da nessuno: diventa il '
      'segnale con cui il front-end offre la scelta. È un passo successivo e facoltativo.',
      pezzi=D.segmenta('', 'Se poi si vuole che l’operatore **scelga** con quale ruolo '
                           'opera, il campo che segnala il multi-profilo è già nel modello '
                           'e non è usato da nessuno: diventa il segnale con cui il '
                           'front-end offre la scelta. È un passo successivo e '
                           'facoltativo.'))

    H(2, 'Dove si amministra')
    P('Nella schermata di gestione degli utenti che esiste già in AnagrafeWeb, con il suo '
      'controllore nel back-end: si aggiunge la matrice ruolo-funzionalità accanto agli '
      'utenti, e l’assegnazione del ruolo diventa l’espansione delle righe. ⚠️ Nel '
      'back-office del nuovo componente non si rifà: sarebbe il secondo registro, cioè '
      'l’errore da cui questo capitolo nasce.')

    H(2, 'Due possibilità ancora aperte: una matrice o due')
    P('Il mondo nuovo è già nella forma giusta: la tabella che abilita le pagine del '
      'back-office è pagina per ruolo, cioè una matrice di capacità. Resta da decidere se '
      'le matrici debbano essere due, una per mondo, o una sola. Le due possibilità sono '
      'riportate per esteso perché la scelta non è tecnica soltanto, e non è ancora '
      'stata presa (PI-27).')
    T(BIVIO, [1.2, 2.9, 2.9])
    P('In entrambe le possibilità il **registro dei ruoli resta uno solo** — CONF_RUOLI, '
      'citato per valore attraverso il nome tecnico del ruolo — e in entrambe non '
      'nascono tabelle di ruolo nello schema del nuovo componente.',
      pezzi=D.segmenta('', 'In entrambe le possibilità il **registro dei ruoli resta uno '
                           'solo** — CONF_RUOLI, citato per valore attraverso il nome '
                           'tecnico del ruolo — e in entrambe non nascono tabelle di ruolo '
                           'nello schema del nuovo componente.'))

    H(2, 'Come i ruoli e i gruppi arrivano nelle pagine Thymeleaf')
    P('Il punto fortunato dell’impianto esistente è che l’identità si legge in un solo '
      'posto e viaggia in un solo oggetto. Le modifiche sono quindi poche e concentrate.')
    T(MODIFICHE, [2.3, 3.4, 0.8])
    P('Nessun controllore e nessun modello di pagina cambia: da quel momento ogni pagina '
      'di ogni front-end vede i gruppi e il codice fiscale dell’header, perché l’oggetto '
      'dell’utente sta in sessione ed è già il canale con cui arrivano nome, cognome e '
      'ruoli. Gli accorgimenti per contenere l’intervento sono cinque.')
    T(MINIMIZZARE, [2.4, 4.1])

    H(2, 'La verifica preliminare')
    P('Una cosa va fatta prima di scrivere codice, e il manuale la suggerisce lui stesso: '
      'una pagina che stampi tutte le variabili dell’header. Dieci minuti su un ambiente '
      'di pre-esercizio, e si sa se i gruppi arrivano, con quali nomi, e se il codice '
      'fiscale arriva anche per gli operatori. Il materiale è pronto in '
      '«verifica-header-iam» fra i prodotti di progetto: un controllore, un modello di '
      'pagina e le istruzioni per innestarli, spenti per difetto e con i valori '
      'personali mascherati.')
    T(VERIFICA, [2.2, 4.3])
    P('⚠️ La pagina va raggiunta **passando dal portale**, perché è quel percorso che si '
      'vuole misurare, e va rispenta appena fatta la verifica: stampa dati personali. Se '
      'invece si riuscisse a raggiungerla scavalcando il portale, quello sarebbe di per '
      'sé il rilievo sulla raggiungibilità diretta dei front-end.',
      pezzi=D.segmenta('', '⚠️ La pagina va raggiunta **passando dal portale**, perché è '
                           'quel percorso che si vuole misurare, e va rispenta appena '
                           'fatta la verifica: stampa dati personali. Se invece si '
                           'riuscisse a raggiungerla scavalcando il portale, quello '
                           'sarebbe di per sé il rilievo sulla raggiungibilità diretta dei '
                           'front-end.'))

    H(2, 'Che cosa questo capitolo non promette')
    P('Due cose, da dire prima e non dopo.')
    V('Che il vecchio diventi autorizzato per ruolo. ', 'I servizi esistenti sono '
      'protetti da un’utenza tecnica, non dalla persona: cambiarlo vuol dire riscrivere '
      '3.360 annotazioni e ridisegnare i profili tecnici. Non è questo intervento, ed è '
      'giusto che non lo sia.')
    V('Che una gestione dei ruoli classica si possa configurare. ', 'Con la quaterna '
      'attuale i permessi stanno sull’utente. Il massimo di uniformità ottenibile senza '
      'riscrivere è: permessi per ruolo nel mondo nuovo, permessi per utente nel '
      'vecchio, e un solo registro di ruoli condiviso. Due modelli di autorizzazione, un '
      'vocabolario. Se il committente vuole il modello unico, va messo a piano come '
      'intervento sul vecchio, con il suo costo.')

    # =================================================================== punti aperti
    tabella_punti = D.trova_tabella(d, '#', 'questione', 'a chi compete')
    for codice, testo, compete in PUNTI_NUOVI:
        D.clona_riga(tabella_punti, (codice, testo, compete))

    # =================================================================== frontespizio
    # ⚠️ La versione non sta solo nella Storia: il template la ripete nel riquadro di
    # testa e nella testata di pagina. Aggiornare solo la Storia lascia un documento che
    # si dichiara ancora la versione precedente in copertina — è successo con questa
    # stessa v0.5, corretta a mano in Word dall'utente.
    for fatto in D.frontespizio(d, '0.5', 'ANALISI_Identita-Profilazione-IAM_v0.5'):
        print('  ' + fatto)

    # =================================================================== storia
    D.storia(d, '13/10/2026', '0.5',
             'I ruoli (nuovo) · Punti aperti',
             'Aggiunto il capitolo sui ruoli: che cosa IAM porta davvero (gruppi LDAP in '
             'modalità header, nessun gruppo negli scope OIDC pubblicati), perché i '
             'gruppi non possono sostituire i ruoli di SIPO, lo stato di fatto del '
             'modello dei permessi, e il meccanismo proposto — matrice '
             'ruolo-funzionalità con R_UTENTI_RUOLI come proiezione, soglie 10/90, '
             'ordinamento deterministico del primo ruolo. Riportate entrambe le '
             'possibilità sul numero delle matrici di capacità. Chiuso PI-06 in '
             'positivo: il manuale dichiara il codice fiscale garantito in iv-codfis. '
             'Nuovi PI-24…PI-28.')

    d.save(DST)

    cap, tab, fig = D.riepilogo(DST)
    print('scritto %s' % os.path.basename(DST))
    print('  capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
    print('  punti aperti in tabella: %d' % (len(tabella_punti.rows) - 1))


if __name__ == '__main__':
    main()
