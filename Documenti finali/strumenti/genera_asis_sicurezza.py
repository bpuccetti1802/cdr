# -*- coding: utf-8 -*-
"""Genera «ASIS_Autenticazione-Profilazione_SIPO» — lo stato di fatto, non il disegno futuro.

Il documento risponde a una domanda sola: come SIPO riconosce chi ha davanti e come decide
che cosa può fare. Tutto ciò che afferma è tratto dai sorgenti e ne porta il riferimento
«file:riga»; dove le fonti tacciono c'è un segnaposto [DA VERIFICARE], non un'ipotesi.

⚠️ Per scelta del committente il documento NON tratta le conseguenze sull'integrazione
SIPO→ANSC: si ferma alla descrizione dell'esistente. L'unico capitolo prospettico è
l'ultimo, sull'eventuale riuso dell'impianto per le nuove applicazioni Angular.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_asis_sicurezza.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
OUT = os.path.join(BASE, 'Documenti finali',
                   'ASIS_Autenticazione-Profilazione_SIPO_v0.2.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

TAGLIA_DA = 29


def testo(par, s):
    if par.runs:
        par.runs[0].text = s
        for r in par.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        par.add_run(s)


def costruisci():
    shutil.copyfile(TEMPLATE, OUT)
    d = docx.Document(OUT)
    body = d.element.body
    for ch in list(body.iterchildren())[TAGLIA_DA:]:
        if ch.tag != qn('w:sectPr'):
            body.remove(ch)
    for p in d.paragraphs:
        if '“Lorem Ipsum”' in p.text:
            testo(p, '“SIPO — Sistema Informativo dei Servizi alla Persona”')
        elif p.style.name == 'Subtitle':
            testo(p, 'Autenticazione e profilazione: lo stato di fatto')
    return d


def copertina(d):
    """Compila la tabella di testata e la prima riga della storia del documento."""
    valori = {
        'Progetto': 'Integrazione SIPO – ANSC',
        'Data consegna': '25/09/2026',
        'Versione': '0.2',
        'Documento': 'ASIS_Autenticazione-Profilazione_SIPO_v0.2',
    }
    for t in d.tables:
        if t.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in t.rows:
                nome = r.cells[0].text.strip()
                if nome in valori:
                    D.riscrivi_cella(r.cells[1], valori[nome])
            break
    # il template lascia tre righe vuote nella storia: a una prima stesura non servono
    st = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for r in list(st.rows)[1:]:
        if not any(c.text.strip() for c in r.cells):
            r._tr.getparent().remove(r._tr)
    D.storia(d, '25/09/2026', '0.1', 'Tutti',
             'Prima stesura. Ricognizione dello stato di fatto di autenticazione e '
             'profilazione in SIPO, condotta sui soli sorgenti applicativi: la catena '
             'dell’accesso, il modello dati della profilazione, i luoghi in cui il permesso '
             'è verificato, l’ambito organizzativo e il tracciamento. Quindici rilievi e otto '
             'punti aperti. Il capitolo conclusivo valuta il riuso dell’impianto per le nuove '
             'applicazioni Angular.')
    D.storia(d, '25/09/2026', '0.2', 'Autenticazione · Librerie (nuovo) · Riuso · '
                                     'Rilievi · Punti aperti',
             'Ricognizione estesa alle librerie disponibili, che la prima stesura non '
             'copriva. Nuovo capitolo «Le librerie e le strutture disponibili»: lo stack PKI, '
             'keystore, firma e SAML del client ANPR, il registro delle postazioni, le '
             'capacità presenti ma inerti, il materiale crittografico versionato e l’origine '
             'dell’impianto. Riscritta la sezione sul certificato di postazione, che la v0.1 '
             'descriveva solo dal lato dell’accesso degli operatori. Riscritto il capitolo '
             'sul riuso, ora articolato sulle tre famiglie — meccanismo, strutture, librerie. '
             'I rilievi passano da quindici a ventuno e i punti aperti da otto a dodici.')


def h(d, livello, t):
    p = d.add_paragraph(style=f'Heading {livello}')
    p.add_run(t)
    return p


def par(d, t, stile='Normal'):
    p = d.add_paragraph(style=stile)
    for pezzo, grassetto in D.segmenta('', t):
        r = p.add_run(pezzo)
        r.bold = grassetto
    return p


def voce(d, testa, corpo):
    p = d.add_paragraph(style='List Paragraph')
    r = p.add_run(testa + ' ')
    r.bold = True
    for pezzo, grassetto in D.segmenta('', corpo):
        rr = p.add_run(pezzo)
        rr.bold = grassetto
    return p


def codice(d, t):
    p = d.add_paragraph()
    r = p.add_run(t)
    r.font.name = 'Courier New'
    r.font.size = Pt(8.5)
    return p


def tabella(d, righe, larghezze=None):
    t = d.add_table(rows=len(righe), cols=len(righe[0]))
    t.style = 'Table Grid'
    for i, r in enumerate(righe):
        for j, v in enumerate(r):
            cel = t.cell(i, j)
            cel.text = ''
            p = cel.paragraphs[0]
            # anche nelle celle «**…**» significa grassetto: senza questo passaggio
            # i marcatori finirebbero visibili nel documento consegnato.
            for pezzo, grassetto in D.segmenta('', v):
                run = p.add_run(pezzo)
                run.bold = grassetto or (i == 0)
                run.font.size = Pt(8.5)
    if larghezze:
        for j, w in enumerate(larghezze):
            for r in t.rows:
                r.cells[j].width = Inches(w)
    return t


def figura(d, png, didascalia, larghezza=6.3):
    d.add_paragraph().add_run().add_picture(os.path.join(IMG, png), width=Inches(larghezza))
    cap = d.add_paragraph()
    r = cap.add_run(didascalia)
    r.italic = True
    r.font.size = Pt(9)


# ---------------------------------------------------------------- contenuti

RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[S1]', 'common/profilazione-utente/ProfilazioneUtente — filtro di ingresso, '
             'configurazione di sicurezza del front-end, modello dell’utente di sessione, '
             'accesso ai dati di profilazione',
     'Sorgente applicativo'],
    ['[S2]', 'common/rest-security/RestSecurity — server di autorizzazione OAuth2, '
             'resource server, caricamento delle utenze tecniche',
     'Sorgente applicativo'],
    ['[S3]', 'common/rest-client/RestClient — client delle chiamate fra front-end e '
             'back-end, con le proprietà clientConfig.properties',
     'Sorgente applicativo'],
    ['[S4]', 'common/anagrafe-entities/AnagrafeEntities — entità JPA delle tabelle di '
             'profilazione dello schema ANAG_USR',
     'Sorgente applicativo'],
    ['[S5]', 'common/commo-web/CommonWeb — controller e frammenti Thymeleaf condivisi, '
             'fra cui l’intestazione che costruisce il menu',
     'Sorgente applicativo'],
    ['[S6]', 'fsha_mf-shared-library-main — libreria Angular condivisa di Roma Capitale '
             '(servizi di autenticazione e autorizzazione, guardie, intercettori)',
     'Sorgente applicativo'],
    ['[S7]', 'ANALISI_Front-End-Angular_v0.4.docx — impostazione del front-end Angular '
             'sulla libreria condivisa',
     'Documento di progetto'],
    ['[S8]', 'common/anpr-client/AnprClient — package «sicurezza»: keystore, firma CMS, '
             'asserzione SAML2, callback di WS-Security, configurazione del canale; '
             'ConfigHandler per la lettura del registro delle postazioni',
     'Sorgente applicativo'],
    ['[S9]', 'back-end/anagrafe-be (arruolamento dei certificati di postazione) e '
             'cross/firma-id-postazione (il medesimo procedimento a riga di comando)',
     'Sorgente applicativo'],
    ['[S10]', 'back-end/not-anpr e common/siel — cifratura CMS delle notifiche ANPR e firma '
              'SOAP del canale verso il Ministero dell’Interno',
     'Sorgente applicativo'],
    ['[S11]', 'cross/Signps — sistema per la gestione delle nomine di presidenti e '
              'scrutatori: prodotto distinto, citato come probabile origine dell’impianto '
              'di autenticazione di SIPO',
     'Sorgente applicativo'],
]

ASSENZE_AUT = [
    ['Meccanismo cercato', 'Esito della ricerca sui sorgenti'],
    ['Controller o endpoint di login applicativo',
     'Assente. Le rotte /login dichiarate in sei classi BasicConfiguration sono soltanto '
     '«permitAll» sul form di default, e il gestore delle credenziali non è configurato.'],
    ['Pagina di login',
     'Assente: nessun login.html in alcuno dei moduli di front-end.'],
    ['Pagine accessDenied.htm, sessionInvalid.htm, nouser.jsp',
     'Referenziate dal codice ma inesistenti come file.'],
    ['LDAP o Active Directory', 'Assenti.'],
    ['CAS, Shibboleth', 'Assenti.'],
    ['SAML applicativo',
     'Assente. La libreria opensaml è dichiarata da due moduli, ma per la firma dei servizi '
     'web verso ANPR e SIEL, non per l’accesso degli utenti.'],
    ['SPID o CIE come fornitore di identità',
     'Assenti. I moduli che nominano la carta d’identità elettronica la trattano come '
     'documento, non come credenziale.'],
    ['Keycloak, OpenID Connect, client OAuth2',
     'Assenti.'],
    ['Verifica crittografica degli header di identità',
     'Assente: gli header sono accolti come sono.'],
    ['Validazione del certificato di postazione nell’applicativo',
     'Assente: SIPO ne legge il solo numero di serie da un header di testo.'],
    ['Attributi di sicurezza del cookie di sessione (secure, http-only, SameSite)',
     'Mai configurati in alcun file di proprietà.'],
    ['Sessione distribuita, controllo di concorrenza delle sessioni',
     'Assenti.'],
    ['Clausola anyRequest() di chiusura delle catene di sicurezza',
     'Assente in entrambe le catene: front-end e resource server.'],
    ['Propagazione dell’identità dell’operatore ai back-end',
     'Assente: al suo posto un’utenza tecnica scelta sul ruolo.'],
]

ASSENZE_PROF = [
    ['Meccanismo cercato', 'Esito della ricerca sui sorgenti'],
    ['Associazione diretta ruolo → funzionalità',
     'Assente. Il legame passa sempre per R_UTENTI_RUOLI, cioè per il singolo utente.'],
    ['Validità temporale dell’assegnazione di un ruolo',
     'Assente: R_UTENTI_RUOLI non ha date di inizio o fine.'],
    ['Ambito sull’assegnazione',
     'Assente: l’ambito è attributo dell’utente, non dell’assegnazione. Non è quindi '
     'esprimibile «questo ruolo, ma solo per questo municipio».'],
    ['Annotazioni @Secured, @PostAuthorize, @RolesAllowed', 'Assenti.'],
    ['Metodi applicativi di verifica del permesso '
     '(isAbilitato, checkFunzionalita, hasPermission)',
     'Assenti: non esiste un punto unico dove la domanda «può farlo?» sia posta.'],
    ['Intercettori o aspetti di autorizzazione',
     'Le due classi CheckPermission esistenti sono interamente commentate.'],
    ['Log delle modifiche ai permessi',
     'Assente: la gestione delle utenze crea e cancella assegnazioni senza traccia storica.'],
    ['Auditing automatico (@EnableJpaAuditing, AuditingEntityListener, @CreatedBy)',
     'Assente: zero occorrenze nell’intero perimetro.'],
    ['Tabella di audit generale',
     'Assente nello stato civile. L’unica tabella di audit mappata è '
     'AUDIT_EVENTO_ELETTORALE, di dominio elettorale.'],
]

RILIEVI = [
    ['#', 'Rilievo', 'Evidenza', 'Natura'],
    ['R-01', 'Gli header di identità non sono verificati',
     'CdRLoginFilter.java:91-92 e 132-142 leggono iv-user e sysgroup senza alcun controllo '
     'di provenienza o di firma. L’identità è quella che il livello di rete dichiara.',
     'Fiducia implicita'],
    ['R-02', 'Esiste un percorso alternativo di identificazione',
     'CdRLoginFilter.java:83-88: con il parametro di richiesta mode=local l’identità è letta '
     'dagli attributi di sessione anziché dagli header. Non è disabilitato per profilo né '
     'per ambiente.',
     'Funzione di sviluppo attiva'],
    ['R-03', 'Nessuna catena di sicurezza si chiude',
     'Né SecurityConfig.java (front-end, 210 antMatchers) né ResourceServerConfig.java '
     '(back-end, 171 antMatchers) dichiarano anyRequest(). Un percorso non elencato non '
     'incontra alcuna regola.',
     'Copertura per enumerazione'],
    ['R-04', 'Una sola chiave firma i token di tutti i back-end',
     'security.signing-key ha lo stesso valore in 45 file application.properties, e '
     'security.jwt.resource-ids è parimenti unico. Un token emesso da un back-end è '
     'accettato da ogni altro.',
     'Assenza di separazione'],
    ['R-05', 'L’identità dell’operatore non raggiunge i back-end',
     'GenericController.java:113-115 e oltre: il profilo passato al client è '
     'user.getRuoli().get(0).getRuoloBe(), cioè il primo ruolo. Il soggetto del token è '
     'un’utenza tecnica condivisa, non la persona.',
     'Perdita di identità'],
    ['R-06', 'Il primo ruolo decide per tutti',
     'Lo stesso criterio ricorre nell’intestazione del menu (header.html:310-313, '
     'user.ruoli[0].descrizione) e nel filtro delle azioni '
     '(ricercaCertificatoStepUno.html:115-159, user.ruoli[0].id). Per un utente con più '
     'ruoli il comportamento dipende dall’ordinamento della query.',
     'Ambiguità sui profili multipli'],
    ['R-07', 'L’ambito organizzativo è dichiarato dal chiamante',
     'IrreperibilitaController.java:657-658 riceve idOrg come parametro di richiesta e vi '
     'fonda il controllo di competenza territoriale. In 32 punti del back-end l’ambito '
     'arriva così. Nulla lo confronta con l’utente autenticato — né potrebbe, poiché il '
     'token porta l’utenza tecnica.',
     'Controllo aggirabile'],
    ['R-08', 'Il catalogo delle funzionalità ha un solo effetto autorizzativo',
     'CdRLoginFilter.java:247-250: la verifica avviene all’ingresso su /init/*, con un '
     'confronto per contenimento sulla sola destinazione iniziale. Le navigazioni '
     'successive non la ripercorrono.',
     'Controllo di sola soglia'],
    ['R-09', 'Sei moduli espongono le proprie rotte senza autenticazione',
     'Le classi BasicConfiguration di all-nas-be, all-matr-be, all-dec-be, faxpec-be, '
     'sad-be e del duplicato di faxpec-be dichiarano permitAll sulle rotte utili e '
     'disabilitano la protezione CSRF; il gestore delle credenziali è vuoto.',
     'Perimetro aperto'],
    ['R-10', 'Il tracciamento è puntuale e la sua chiave arriva dal client',
     'Nove occorrenze di ID_UTENTE_LOG e poche altre colonne con sei nomi diversi; il '
     'valore è preso dal parametro di richiesta (es. PubblicazioniController.java:122).',
     'Traccia non attendibile'],
    ['R-11', 'Il tracciamento dei rilasci ha una lista di esclusione',
     'EstrattiDownloadLogServiceImpl.java:40-46: se ESTRATTI_UTENZA_LOG.FLAG_SKIP vale «Y» '
     'il rilascio non viene registrato.',
     'Esenzione configurabile'],
    ['R-12', 'Codice di sicurezza presente ma non attivo',
     'InvalidSessionHandlerInterceptor non è registrato da alcun configuratore; '
     'TestJunctionFilter non è raccolto perché manca @ServletComponentScan; '
     'checkPoliziaLocale (CdRLoginFilter.java:167-184), che vincola un ruolo alla '
     'giunzione di provenienza, non è invocato da alcun punto.',
     'Presidio apparente'],
    ['R-13', 'Segreti in chiaro nei sorgenti versionati',
     'security.jwt.client-secret con prefisso {noop} in 45 moduli; jwt.secret di '
     'cert-online-be (application.properties:62); credenziali fra moduli cifrate in TripleDes '
     'ma con la chiave scritta nel codice e condivisa da dieci copie della classe su '
     'quattordici.',
     'Segreto non protetto'],
    ['R-14', 'La scadenza della sessione è configurata da un solo modulo',
     'server.servlet.session.timeout compare una volta sola in tutto il perimetro, in '
     'statistica-web (1800 secondi). Gli altri moduli usano il valore predefinito del '
     'contenitore.',
     'Configurazione non governata'],
    ['R-15', 'L’impianto di profilazione è duplicato',
     'Il modulo di profilazione, quello di sicurezza REST, il client e le entità esistono in '
     'copia sotto sipo-root/sipo-elezioni, con le credenziali tecniche ripetute nel secondo '
     'file di proprietà. ⚠️ Un modulo di produzione, gest-evel-be, dipende dal fork delle '
     'elezioni per utenti, ruoli e abilitazioni, non dal componente comune.',
     'Doppia manutenzione'],
    ['R-16', 'Verso ANPR l’identità di postazione è sempre la stessa',
     'ConfigHandler.java:67 sovrascrive con un valore scritto nel codice il parametro '
     'ricevuto, e quel valore è l’unico argomento in ingresso della procedura che seleziona '
     'certificato, password e firma della postazione. Chiunque operi, verso ANPR si presenta '
     'la medesima identità di macchina.',
     'Identità di macchina fissa'],
    ['R-17', 'Il filtro a chiave API non protegge gli endpoint che emettono gettoni',
     'ApiKeyFilter (righe 43-46) agisce solo se il percorso è esattamente «/generate» o '
     '«/validate», ma il controller è mappato su «/api/token/…» e il modulo non dichiara '
     'alcun context-path: la condizione non si verifica mai. Gli endpoint restano privi di '
     'chiave; nessun modulo del workspace li consuma.',
     'Presidio inefficace'],
    ['R-18', 'La configurazione del canale sicuro verso ANPR è orfana',
     'anpr-client/src/main/resources/cxf.xml (259 righe) non è caricato da alcun file del '
     'workspace e nomina dieci volte una classe «client.ClientKeystorePasswordCallback» che '
     'non esiste; saml.properties è caricato solo da lì. Poiché è l’unico punto in cui il '
     'callback SAML risulta agganciato, non è dimostrabile dal codice che '
     'SAML2CallbackHandler e Signer siano mai invocati.',
     'Configurazione non risolvibile'],
    ['R-19', 'Dati personali in file di configurazione versionati',
     'I file PROD_Keystore.properties e PRE_Keystore.properties di anpr-client contengono, '
     'oltre alle password dei keystore, il codice fiscale di operatori reali nel campo '
     'ID_OPERATORE. È un profilo diverso dal segreto applicativo: è dato personale in '
     'versionamento.',
     'Dato personale esposto'],
    ['R-20', 'Il modello a permessi per aspetti è stato abbandonato a metà',
     'Le quattro classi CheckPermission (gest-evel-be, gest-evel-web e le due copie di '
     'backup) sono commentate riga per riga, e non ricompilerebbero: importano '
     'UtentiElettoraleDao, classe assente dal workspace. Era il tentativo di sostituire '
     'l’autorizzazione per indirizzo con una per permessi.',
     'Lavoro interrotto'],
    ['R-21', 'La firma dell’identificativo di postazione esiste in tre implementazioni',
     'La stessa logica CMS/PKCS#7 con SHA256withRSA è scritta tre volte: in '
     'anpr-client/sicurezza/pki/Signer, in cross/firma-id-postazione/helper/Helper e in '
     'anagrafe-be/helper/Helper. A queste si aggiungono sedici copie indipendenti della '
     'classe TripleDes, con tre chiavi distinte scritte nei sorgenti.',
     'Duplicazione di logica crittografica'],
]

PUNTI = [
    ['#', 'Questione', 'Perché è aperta', 'A chi compete'],
    ['PA-1', 'Che cosa valida il certificato di postazione, e con quali regole',
     'SIPO riceve il numero di serie in un header (CdRLoginFilter.java:225-226) e non '
     'compie alcuna verifica. La validazione avviene a monte, ma la configurazione del '
     'livello che la esegue non è fra le sorgenti disponibili.',
     'Infrastruttura / Sistemi'],
    ['PA-2', 'Quale sia il perimetro di rete che rende attendibili gli header',
     'La fiducia dell’intera catena poggia sul fatto che nessuno possa raggiungere '
     'l’applicativo se non attraverso la giunzione. La topologia che lo garantisce non è '
     'documentata nelle sorgenti.',
     'Infrastruttura / Sistemi'],
    ['PA-3', 'Se il servizio msAuth della libreria Angular sia la stessa identità del '
             'portale',
     'La libreria condivisa reindirizza a /msAuth/api/v1/autenticazione/loginIAM '
     '(authentication-iam.guard.ts:20), che non compare in alcun sorgente di SIPO. Non è '
     'accertabile dal codice se dietro vi sia lo stesso fornitore di identità del portale o '
     'un secondo impianto.',
     'Analisi / Cliente'],
    ['PA-4', 'Quale sia la forma completa del profilo restituito da msAuth',
     'Il tipo AuthData proviene dal pacchetto privato test-library-frankmd93, risolto da un '
     'registro interno e non presente nel workspace. Del profilo si conoscono solo i campi '
     'effettivamente letti dal codice: token, user.abilitazioni, struttura, ufficio, tributo.',
     'Analisi / Fornitore'],
    ['PA-5', 'Dove il token venga agganciato alle chiamate HTTP della libreria',
     'L’intercettore di autenticazione (authentication.interceptor.ts:10-14) non modifica la '
     'richiesta, e il segnaposto SHOULD_SKIP_TOKEN_HANDLER non è consumato da alcun '
     'intercettore. La costruzione degli header avviene in una classe del pacchetto esterno, '
     'non ispezionabile.',
     'Analisi / Fornitore'],
    ['PA-6', 'Quale sia il vocabolario delle abilitazioni dello stato civile',
     'Il meccanismo esiste nella libreria, l’elenco no. CONF_FUNZIONALITA è l’unico catalogo '
     'di azioni presente nel sistema attuale, ma è costruito su indirizzi di pagina del '
     'front-end esistente.',
     'Analisi / Cliente'],
    ['PA-7', 'Se l’ambito organizzativo debba diventare parte del profilo',
     'Nella libreria il profilo porta struttura, ufficio e tributo; in SIPO l’ambito è '
     'ID_ORGANIZZAZIONE e ID_SEDE_MUNICIPIO, oggi propagati come parametro dal chiamante. '
     'Se le due nozioni coincidano non è accertabile dalle fonti.',
     'Analisi / Cliente'],
    ['PA-8', 'Quale sia il criterio di conservazione dei dati di accesso',
     'L’unica traccia sistematica degli accessi è una riga di registro applicativo '
     '(CdRLoginFilter.java:234-236). Non è documentato per quanto tempo i registri siano '
     'conservati né chi possa consultarli.',
     'Organizzazione / Privacy'],
    ['PA-9', 'Che cosa faccia la procedura che legge il registro delle postazioni',
     'ANAG_USR.PKG_ANPR.get_postazione_cert_sign è l’unico lettore di REG_USER_ANPR, e il '
     'suo sorgente non è nel repository. Manca anche il DDL delle due tabelle: i dati di '
     'collaudo ne mostrano sette colonne, il DAO del programma a riga di comando ne inserisce '
     'nove. Il disallineamento non è risolvibile senza lo schema.',
     'Base dati / Sistemi'],
    ['PA-10', 'Se il canale SAML verso ANPR sia configurato altrove',
     'Dal solo repository il callback SAML risulta agganciato unicamente in due file orfani. '
     'Se la configurazione sia fornita dal contenitore, dall’EAR o da proprietà di ambiente '
     'non è deducibile dai sorgenti, e dall’esito dipende se l’asserzione venga firmata al '
     'momento o riusata dal database.',
     'Infrastruttura / Sistemi'],
    ['PA-11', 'Se gli endpoint che emettono gettoni siano raggiungibili dall’esterno',
     'Dal codice «/api/token/generate» e «/api/token/validate» sono mappati e privi di '
     'presidio (R-17). La raggiungibilità di rete non è deducibile dai sorgenti, e da essa '
     'dipende la portata del rilievo.',
     'Infrastruttura / Sistemi'],
    ['PA-12', 'Perché l’identificativo di postazione verso ANPR sia fisso',
     'La sovrascrittura del parametro (R-16) può essere una svista rimasta da un collaudo '
     'oppure una scelta deliberata, se ANPR accreditasse il Comune come postazione unica. '
     'Le due letture hanno conseguenze opposte sulla tracciabilità e il codice non consente '
     'di distinguerle.',
     'Analisi / Fornitore'],
]

LIBRERIE_USO = [
    ['Libreria', 'Capacità offerta', 'Diffusione'],
    ['common/profilazione-utente',
     'Filtro di ingresso dal portale, configurazione di sicurezza del front-end, modello '
     'dell’utente di sessione, lettura di ruoli e funzionalità.',
     'Circa 34 moduli di front-end'],
    ['common/rest-security',
     'Server di autorizzazione OAuth2, resource server, caricamento delle utenze tecniche, '
     'cifratura delle parole d’ordine con BCrypt.',
     '45 moduli di back-end su 53'],
    ['common/rest-client',
     'Chiamate fra front-end e back-end con flusso OAuth2 a password e utenze tecniche per '
     'ruolo; cifratura TripleDes delle credenziali di configurazione.',
     'Diffusa nei front-end'],
    ['common/anpr-client — package «sicurezza»',
     '51 file: caricamento di keystore PKCS#12, firma CMS/PKCS#7 con SHA256withRSA, '
     'asserzione SAML2, callback di WS-Security, configurazione TLS. **È lo stack '
     'crittografico del progetto.**',
     'Dipendenza di 30 moduli di back-end'],
    ['back-end/not-anpr — package «sicurezza»',
     'Cifratura e decifratura CMS con AES256-CBC su BouncyCastle, caricamento di keystore, '
     'gestione della richiesta firmata.',
     'Endpoint di ricezione delle notifiche ANPR'],
    ['common/siel — package «handler»',
     'Firma SOAP WS-Security completa e attiva: firma più marca temporale, durata di '
     'validità dichiarata, parti firmate selezionate.',
     'Canale verso il Ministero dell’Interno'],
    ['back-end/anagrafe-be — arruolamento certificati',
     'Operazione REST che riceve i PKCS#12 delle postazioni, ne estrae chiave e certificato, '
     'firma l’identificativo di postazione e lo registra.',
     'Amministrazione delle postazioni'],
    ['common/anagrafe-entities',
     'Le entità e i repository di utenti, ruoli, assegnazioni e utenze tecniche: è il livello '
     'dati di tutta la profilazione.',
     'Trasversale'],
]

CAPACITA_INERTI = [
    ['Componente', 'Capacità che offrirebbe', 'Stato accertato'],
    ['Le quattro classi CheckPermission (gest-evel-be, gest-evel-web e due copie di backup)',
     'Autorizzazione per aspetti: caricamento dei ruoli nel contesto di sicurezza e '
     'valutazione prima di ogni metodo. Era il tentativo di sostituire l’autorizzazione per '
     'indirizzo con una per permessi.',
     '⚠️ Commentate riga per riga, e non ricompilerebbero: importano UtentiElettoraleDao, '
     'classe assente dal workspace.'],
    ['anpr-client — cxf.xml e saml.properties',
     'Il collegamento fra il canale CXF e il callback che costruisce l’asserzione SAML.',
     '⚠️ Orfani: nessun file li carica, e cxf.xml nomina dieci volte una classe che non '
     'esiste. Ne discende PA-10.'],
    ['anpr-client — ConfigSSL e TrustAllX509TrustManager',
     'Disattivazione della validazione dei certificati TLS.',
     'Morti: l’unico richiamo è commentato. Restano però nel percorso di classe di trenta '
     'moduli.'],
    ['anpr-client — KeyStoreComune',
     'Caricamento del keystore del Comune da file di proprietà.',
     'Morta: nessun riferimento nell’intero workspace.'],
    ['anpr-client — ProxyAuthenticator',
     'Autenticazione verso il proxy di rete.',
     'Morta: l’unico richiamo è commentato e contiene credenziali in chiaro.'],
    ['profilazione-utente — CallServlet, LogIpConfig, TestJunctionFilter, '
     'InvalidSessionHandlerInterceptor',
     'Recupero dell’utente dal portale per servizio, tracciatura dell’indirizzo nei '
     'registri, diagnosi della giunzione, gestione della sessione scaduta.',
     'Tutte inerti. ⚠️ InvalidSessionHandlerInterceptor è invece **registrato e vivo in '
     'Signps**: è un residuo del port.'],
    ['cert-online-be — package jwttokenareasipo (8 classi)',
     'Servizio completo di emissione e verifica di gettoni JWT con nome, cognome e codice '
     'fiscale.',
     '⚠️ Caricato e quindi **esposto**, ma senza alcun consumatore nel workspace e senza '
     'presidio efficace (R-17).'],
    ['cross/cert-online-dotnet — librerie Unisys',
     'Un impianto di accesso unico e di autorizzazione completo: moduli di autenticazione, '
     'generatore di gettoni, gestione di utenti, gruppi e diritti, archivio cifrato.',
     'Tecnologia estranea (.NET): nessun consumatore Java possibile. Sono il lascito del '
     'sistema precedente a SIPO.'],
    ['cross/Signps — CSRFTokenManager',
     'Protezione contro la falsificazione di richiesta con gettone per sessione.',
     'Funzionante, ma confinata nell’altro prodotto.'],
]

MAPPA_ANGULAR = [
    ['Elemento dell’impianto attuale', 'Corrispondente nella libreria Angular',
     'Trasferibile?'],
    ['Identificazione per header iv-* iniettati dalla giunzione',
     'Token opaco conservato in localStorage con chiave «auth»; in assenza, rinvio a '
     '/msAuth/api/v1/autenticazione/loginIAM',
     'No: i due modelli sono alternativi'],
    ['HttpSession con l’attributo LOGIN_USER',
     'AuthenticationService, con BehaviorSubject in memoria e copia in localStorage',
     'No: non esiste sessione lato server'],
    ['Autorizzazione per indirizzo (210 antMatchers con elenchi di ruoli)',
     'AuthorizationGuard su route.data[«authorizations»], con esito vero se almeno una '
     'abilitazione richiesta è posseduta',
     'No nella forma, sì nell’intento'],
    ['CONF_RUOLI e le authority ROLE_*',
     'Nessun concetto di ruolo: solo abilitazioni',
     'No: il ruolo non ha corrispondente'],
    ['CONF_FUNZIONALITA — il catalogo delle azioni',
     'user.abilitazioni, lista di stringhe confrontata da AbilityService e da '
     'AuthorizationService.filterByAuthorization',
     'Sì, ed è il raccordo principale'],
    ['CONF_AMBITO e CONF_AREE_TEMATICHE — la gerarchia del menu',
     'Nessun corrispondente: il menu di ciascun micro-front-end è suo',
     'Parzialmente: come tassonomia, non come struttura di navigazione'],
    ['R_UTENTI_RUOLI — l’assegnazione per utente',
     'Nessun corrispondente lato client: il profilo arriva già risolto',
     'Sì come tabella, no come criterio (vedi il testo)'],
    ['ID_ORGANIZZAZIONE e ID_SEDE_MUNICIPIO',
     'struttura, ufficio e tributo nel profilo (AuthDataExtended, righe 7-21)',
     'Sì, previa verifica di corrispondenza (PA-7)'],
    ['Utenze tecniche CONF_APP_USER e CONF_APP_ROLE',
     'Nessun corrispondente',
     'No, e non è auspicabile'],
]


def scrivi(d):
    # ---------------------------------------------------------- 1. scopo
    h(d, 1, 'Scopo del documento')
    par(d, 'Questo documento descrive **come SIPO riconosce chi ha davanti e come decide che '
           'cosa quella persona può fare**. È una ricognizione dello stato di fatto: non '
           'propone un disegno, non valuta alternative e non tratta le conseguenze sui '
           'progetti in corso. Dove il sistema si comporta in modo inatteso il documento lo '
           'registra come rilievo, senza indicare la correzione.')
    par(d, 'La ragione per cui serviva metterlo per iscritto è che l’argomento non è trattato '
           'in alcun documento esistente, mentre ricorre in ogni discussione di progetto: '
           'l’accesso, i ruoli, la competenza territoriale e la tracciabilità sono dati per '
           'noti e non lo sono. Ciò che segue è stato ricavato leggendo i sorgenti, non '
           'chiedendo a chi li ha scritti.')
    par(d, '⚠️ **Una precisazione necessaria fin d’ora**: SIPO non autentica nessuno. Non ha '
           'una pagina di accesso, non confronta credenziali e non emette una prova di '
           'identità. Riceve un’identità già formata e la usa. Tutto il capitolo '
           'sull’autenticazione descrive, in sostanza, come questa identità entra e che cosa '
           'ne viene fatto.')

    h(d, 2, 'Perimetro e metodo')
    par(d, 'Sono stati esaminati i sorgenti applicativi di SIPO presenti nel workspace: le '
           'cartelle di front-end, back-end, componenti comuni, moduli trasversali e la '
           'radice di progetto. Sono esclusi il repository di ANSC, la documentazione di ANPR '
           'e i prodotti di terzi inclusi nella radice. È incluso, per il solo capitolo '
           'finale, il codice della libreria Angular condivisa.')
    par(d, 'Ogni affermazione tecnica porta il riferimento al file e, quando utile, alla riga. '
           '**I conteggi sono stati verificati direttamente e non stimati**; quando una '
           'ricerca non ha prodotto risultati, l’assenza è riportata come tale, perché '
           'un’assenza accertata è a sua volta un’informazione. Dove le fonti tacciono il '
           'documento si ferma e segnala un punto aperto: non completa per congettura.')
    par(d, 'Vale la pena dichiarare un limite del metodo. Leggendo il codice si accerta che '
           'cosa il sistema fa, non che cosa il livello di rete davanti a esso impedisce. '
           'Alcuni dei rilievi che seguono sono neutralizzati, in esercizio, da una '
           'configurazione di rete che non è fra le sorgenti disponibili: il documento lo dice '
           'dove accade, e lo registra come punto aperto anziché tacerlo o darlo per risolto.')

    h(d, 2, 'Glossario')
    tabella(d, [
        ['Termine', 'Significato in questo documento'],
        ['Autenticazione', 'Il procedimento con cui si stabilisce chi è l’utente.'],
        ['Autorizzazione', 'La decisione se un utente già riconosciuto possa compiere '
                           'una certa azione.'],
        ['Profilazione', 'L’insieme dei dati che descrivono l’utente ai fini della '
                         'decisione: ruoli, funzionalità abilitate, ambito organizzativo.'],
        ['Pre-autenticazione', 'Il modo di lavorare in cui l’applicativo non verifica '
                               'credenziali ma si fida di un’identità stabilita a monte e '
                               'trasmessa insieme alla richiesta.'],
        ['Giunzione', 'Il punto della rete che intercetta la richiesta del browser, la '
                      'associa alla sessione del portale e la inoltra all’applicativo '
                      'aggiungendovi l’identità.'],
        ['Ruolo', 'Nel sistema attuale, una riga di CONF_RUOLI. Genera l’autorità '
                  'ROLE_<nome> valutata dalle regole di sicurezza.'],
        ['Funzionalità', 'Una riga di CONF_FUNZIONALITA: una voce di menu con il proprio '
                         'indirizzo di pagina.'],
        ['Abilitazione', 'Nel modello della libreria Angular, una stringa nell’elenco '
                         'user.abilitazioni del profilo. È il corrispondente più prossimo '
                         'della funzionalità.'],
        ['Utenza tecnica', 'Una riga di CONF_APP_USER: un’identità applicativa usata per '
                           'chiamare i servizi di back-end, distinta dalle persone.'],
    ], larghezze=[1.5, 5.0])

    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, larghezze=[0.55, 4.45, 1.5])

    # ---------------------------------------------------------- 2. quadro
    h(d, 1, 'Il quadro d’insieme')
    par(d, 'La catena che porta un operatore dalla propria postazione fino a un dato di SIPO '
           'attraversa sei passaggi, e **nessuno di quelli interni all’applicativo verifica '
           'una credenziale**. Il riconoscimento avviene fuori; dentro, ciò che accade è la '
           'traduzione di un’identità ricevuta in un insieme di autorità, e l’uso di quelle '
           'autorità per consentire o negare l’accesso a un indirizzo.')
    figura(d, 'aut_catena.png',
           'Figura 1 — La catena dell’accesso. Il pallino rosso segna i punti in cui un '
           'elemento è accolto senza essere verificato.')
    par(d, 'Il disegno mette in evidenza una simmetria che conviene tenere a mente leggendo '
           'il resto: **l’identità della persona vive nella sessione del front-end e si ferma '
           'lì**. Verso il basso, cioè verso i back-end, non prosegue: al suo posto viaggia '
           'un’utenza tecnica scelta in base al ruolo. Verso l’alto, cioè verso il contesto di '
           'sicurezza di Spring, prosegue soltanto l’elenco delle autorità. Sono tre '
           'rappresentazioni della stessa persona, che non si parlano fra loro.')

    # ---------------------------------------------------------- 3. autenticazione
    h(d, 1, 'L’autenticazione')

    h(d, 2, 'Non esiste un accesso applicativo')
    par(d, 'La ricerca di un punto di accesso in SIPO non produce risultati: non c’è un '
           'controller che riceva credenziali, non c’è una pagina che le chieda, non c’è un '
           'servizio che le verifichi. Le rotte «/login» che compaiono in alcune '
           'configurazioni di back-end sono dichiarate accessibili a tutti e appartengono al '
           'modulo di form predefinito, il cui gestore delle credenziali non è configurato: '
           'sono un residuo, non una funzione.')
    par(d, 'Il fatto merita di essere affermato con chiarezza perché ha un corollario pratico: '
           '**non esiste, in SIPO, un luogo in cui si possa intervenire sull’accesso**. '
           'Qualunque cambiamento riguardi il modo in cui gli operatori si identificano si '
           'decide altrove e arriva a SIPO come un cambiamento del formato degli header.')

    h(d, 2, 'L’ingresso: il filtro di portale e gli header di identità')
    par(d, 'Il percorso comincia con un indirizzo della forma '
           '«/<Modulo>Web/init/default?goUrl=…», intercettato da un filtro di servlet '
           'registrato sul solo schema «/init/*» '
           '(FilterConfig.java:13-21). Il filtro è CdRLoginFilter [S1], e ciò che fa è leggere '
           'l’identità dagli header della richiesta HTTP (righe 91-92 e 132-142).')
    par(d, 'Gli header sono dichiarati in un file di proprietà (portale.properties:22-37) e '
           'portano, oltre all’identificativo dell’utente e al gruppo di appartenenza, i dati '
           'anagrafici di chi accede:')
    codice(d, 'cdr.portale.userIdHeaderParam=iv-user\n'
              'cdr.portale.groupIdHeaderParam=sysgroup\n'
              'cdr.portale.codFisHeaderParam=iv-codfis\n'
              'cdr.portale.nomeHeaderParam=iv-nome   ·   cognomeHeaderParam=iv-cognome\n'
              'cdr.portale.nascitaDataIdHeaderParam=iv-nascita-data   ·   … e altri dieci')
    par(d, 'Il prefisso «iv-» e l’indirizzo di disconnessione configurato per i tre ambienti '
           '(dynamicGeneric.properties:4-10, che per lo sviluppo punta a '
           '«comune.roma.it/oamsso-bin/logout.pl») identificano il prodotto a monte come il '
           'sistema di accesso unico del portale di Roma Capitale. Quando la sessione manca, '
           'il punto di ingresso della sicurezza rinvia al portale con un indirizzo scritto '
           'nel codice (CustomSecurityEntryPoint.java:23-30).')
    par(d, '⚠️ **Nessuna verifica crittografica accompagna gli header.** Non c’è una firma da '
           'controllare, non c’è un segreto condiviso con la giunzione, non c’è un elenco di '
           'indirizzi di provenienza ammessi. L’identità è quella che la richiesta dichiara, e '
           'l’unica cosa che impedisce di dichiararne una falsa è che nessuno possa parlare '
           'con l’applicativo senza passare per la giunzione. Questa condizione è '
           'un’assunzione di rete, non una proprietà del codice, e la sua verifica è il punto '
           'aperto PA-2.')
    par(d, 'Il filtro distingue poi due popolazioni (righe 95-107): se l’identificativo è un '
           'codice fiscale, oppure se il gruppo è quello dei cittadini, l’utente è trattato '
           'come cittadino e i suoi dati anagrafici sono presi dagli header; altrimenti è '
           'trattato come dipendente. In entrambi i casi ruoli e funzionalità sono poi letti '
           'dal database (righe 113 e 195-253), e l’oggetto risultante è depositato nella '
           'sessione con il nome LOGIN_USER (riga 232).')
    par(d, '⚠️ Esiste un secondo modo di entrare. Se la richiesta porta il parametro '
           '«mode=local», l’identificativo dell’utente e il gruppo **non sono letti dagli '
           'header ma dagli attributi di sessione** (righe 83-88). È una comodità di sviluppo; '
           'non è però condizionata al profilo attivo né all’ambiente, e resta quindi presente '
           'nel codice che va in esercizio.')

    h(d, 2, 'Dalla sessione al contesto di sicurezza')
    par(d, 'Il secondo filtro della catena, CustomAuthenticationProcessingFilter [S1], è la '
           'cerniera fra il mondo del portale e quello di Spring Security. Prende come '
           'soggetto autenticato il nome utente contenuto in LOGIN_USER (righe 32-41) e '
           'costruisce un gettone di pre-autenticazione in cui **le credenziali sono la '
           'stringa vuota** (riga 43-45):')
    codice(d, 'new PreAuthenticatedAuthenticationToken(utenteSSO.getCf(), "")')
    par(d, 'È la forma canonica della pre-autenticazione, e dice in una riga ciò che il '
           'capitolo intero descrive: non c’è nulla da verificare, perché la verifica è già '
           'avvenuta altrove. Il gettone viene autenticato, dichiarato valido e riposto nel '
           'contesto di sicurezza insieme alle autorità (righe 57-79); le stesse autorità sono '
           'anche scritte in sessione sotto il nome «ruoli» (riga 75).')
    par(d, 'Le autorità provengono da MyUserDetailsService [S1], che le costruisce anteponendo '
           'il prefisso «ROLE_» al nome del ruolo letto dal database (righe 30-57). Vi è un '
           'comportamento di ripiego che vale la pena conoscere: **se il nome utente è un '
           'codice fiscale e nessun ruolo risulta assegnato, l’utente riceve comunque '
           'l’autorità ROLE_CITTADINO_CRI_ON** (righe 41-43). Un ripiego analogo esiste lato '
           'back-end (AppUserDetailsService.java:42-44).')

    h(d, 2, 'Dove risiede l’identità a sistema acceso')
    par(d, 'Coesistono due rappresentazioni dell’utente, e non sono sincronizzate fra loro.')
    par(d, 'La prima, e la sola che il codice applicativo consulti, è l’oggetto depositato in '
           'sessione. È una classe con oltre cinquanta campi: identificativo, nome, cognome, '
           'codice fiscale, ruolo, gruppo, organizzazione e sua descrizione, struttura '
           'convenzionata, indirizzo di base, indirizzo IP della postazione, più sette '
           'indicatori di presenza per i gruppi di funzionalità, l’elenco dei ruoli e quello '
           'delle aree tematiche. I controller la ricevono per iniezione dichiarativa:')
    codice(d, '@SessionAttribute("LOGIN_USER") User user')
    par(d, 'La diffusione di questo schema è la migliore misura della sua centralità: la '
           'stringa LOGIN_USER **ricorre in 8.975 righe** fra front-end, componenti comuni e '
           'back-end. Anche le viste vi attingono direttamente, a partire dal frammento di '
           'intestazione condiviso (header.html:3, [S5]).')
    par(d, 'La seconda rappresentazione è il contesto di sicurezza di Spring. Il soggetto che '
           'vi risiede è un oggetto diverso, omonimo ma di un altro pacchetto, che porta '
           'soltanto il nome utente e le autorità. Serve a valutare le regole di sicurezza e '
           'nient’altro: **nessun controller applicativo legge l’identità da qui**. Nei '
           'sorgenti, il contesto è interrogato direttamente in tre soli punti, tutti '
           'appartenenti all’infrastruttura di sicurezza.')

    h(d, 2, 'La sessione')
    par(d, 'Il contenitore è la sessione HTTP standard del contenitore servlet, con il cookie '
           'JSESSIONID (nominato in SecurityConfig.java:348, dove la disconnessione lo '
           'cancella). Attorno a questa scelta, semplice e adeguata, mancano però tutti i '
           'parametri che di norma l’accompagnano.')
    tabella(d, [
        ['Aspetto', 'Stato di fatto'],
        ['Durata della sessione',
         'Configurata da un solo modulo su circa trentaquattro: statistica-web dichiara '
         'server.servlet.session.timeout=1800. Per tutti gli altri vale il valore '
         'predefinito del contenitore. Nessun punto del codice imposta la durata in modo '
         'programmatico.'],
        ['Attributi del cookie',
         'Né «secure», né «http-only», né «SameSite» sono configurati in alcun file di '
         'proprietà: valgono i valori predefiniti.'],
        ['Sessione distribuita',
         'Assente. Non vi è alcun archivio condiviso fra istanze: la sessione vive nella '
         'memoria del nodo che l’ha creata.'],
        ['Sessioni concorrenti',
         'Nessun limite e nessun controllo: lo stesso utente può avere più sessioni aperte '
         'senza che il sistema ne sia informato.'],
        ['Disconnessione',
         'Curata: CustomLogoutSuccessHandler rimuove gli attributi, azzera i cookie, svuota '
         'il contesto di sicurezza, invalida la sessione e rinvia all’indirizzo di '
         'disconnessione del portale (righe 27-57).'],
        ['Back-end',
         'Esplicitamente privi di sessione: la politica dichiarata è STATELESS '
         '(SecurityConfig.java:61, [S2]).'],
    ], larghezze=[1.6, 4.9])
    par(d, 'Una proprietà chiamata «cdr.loginfilter.timeout» (portale.properties:5) potrebbe '
           'trarre in inganno: sta sotto l’intestazione dei parametri delle servlet e regola '
           'l’attesa delle chiamate verso i servizi di verifica del portale, non la durata '
           'della sessione.')

    h(d, 2, 'Il certificato di postazione')
    par(d, 'Le postazioni degli uffici sono dotate di un certificato, e il suo esito arriva a '
           'SIPO, ma non come certificato: come testo. Il filtro di ingresso legge due header '
           'e li ripone nell’oggetto di sessione (CdRLoginFilter.java:220-229):')
    codice(d, 'user.setIpPostazione(requ.getHeader("x-real-ip"));\n'
              'user.setHostname(requ.getHeader("x-client-sn-sipo"));   // numero di serie')
    par(d, 'Il commento nel codice dichiara esplicitamente di riusare il campo destinato al '
           'nome della macchina per conservarvi il numero di serie del certificato. '
           '**Sul percorso di accesso l’applicativo non compie alcuna verifica**: non '
           'controlla la catena di certificazione, non verifica la revoca, non confronta il '
           'numero di serie con un registro di postazioni ammesse. La validazione, se '
           'avviene, avviene a monte, e quale sia il livello che la esegue non è accertabile '
           'dalle sorgenti: è il punto aperto PA-1.')
    par(d, '⚠️ **Sarebbe però un errore concluderne che SIPO non sappia trattare i '
           'certificati di postazione.** Ne tratta, e in modo compiuto: possiede un registro '
           'delle postazioni con i certificati, un’operazione di arruolamento, una firma '
           'crittografica dell’identificativo di postazione e le librerie per produrla e '
           'verificarla. Tutto questo però **non serve a riconoscere l’operatore**: serve a '
           'identificare il Comune verso ANPR. Sono due impianti distinti, che convivono '
           'nello stesso applicativo senza toccarsi, ed è per questo che la prima stesura di '
           'questo documento ne aveva visto uno solo. Il secondo è descritto nel capitolo '
           '«Le librerie e le strutture disponibili».')
    par(d, 'Nella stessa classe esiste un metodo che vincolerebbe un ruolo alla giunzione di '
           'provenienza — la Polizia Locale soltanto da un certo dominio, gli altri da un '
           'altro (righe 167-184). ⚠️ **Il metodo non è invocato da alcun punto del filtro.** '
           'È un presidio scritto e mai attivato.')

    h(d, 2, 'L’autenticazione fra i servizi')
    par(d, 'Quando un front-end chiama un back-end, un’autenticazione vera e propria avviene. '
           'Il client condiviso [S3] esegue un flusso OAuth2 nella modalità a password: '
           'presenta le credenziali del modulo come autenticazione di base, invia nome utente '
           'e parola d’ordine in un corpo codificato e ottiene un gettone dall’indirizzo '
           '«/oauth/token» (RestClient.java:96-130). Il gettone accompagna poi la chiamata di '
           'servizio (righe 156-161 e analoghe).')
    par(d, 'Due caratteristiche di questo flusso meritano di essere annotate.')
    voce(d, 'Nessuna conservazione del gettone.',
         'Il metodo che lo genera è invocato all’inizio di ciascun metodo pubblico del '
         'client (righe 154, 195, 246, 304): **si richiede un gettone nuovo a ogni chiamata**, '
         'e la scadenza non viene mai sfruttata.')
    voce(d, 'L’identità che viaggia non è quella dell’operatore.',
         'Il profilo passato al client è il primo ruolo dell’utente di sessione, e seleziona '
         'un’utenza tecnica fra le tredici dichiarate nel file di proprietà. Lato back-end il '
         'soggetto del gettone è dunque ADMIN, AUTH_USER, FUNZ_TERR o simili, **mai il codice '
         'fiscale di chi sta operando**.')
    codice(d, 'return restClient.callRestServicePost(Constant.URL_ANAGRAFE_BE,\n'
              '        "/getDettaglioPersona", Constant.DOMINIO_ANAGRAFE_BE,\n'
              '        user.getRuoli().get(0).getRuoloBe(), …);        // GenericController:113')
    par(d, 'Le credenziali contenute nel file di proprietà non sono in chiaro: sono cifrate in '
           'TripleDes e codificate, e il client le decifra all’avvio. ⚠️ La chiave di cifratura '
           'è però scritta nel sorgente della classe che la usa, e **dieci delle quattordici '
           'copie di quella classe presenti nel workspace condividono lo stesso valore**: la '
           'cifratura protegge da una lettura distratta del file di configurazione, non da chi '
           'disponga del codice.')
    par(d, 'Sul versante della verifica, i back-end sono resource server OAuth2 con gettoni '
           'JWT firmati simmetricamente ([S2], righe 66-86). ⚠️ **La chiave di firma è la '
           'stessa per tutti**: il valore di «security.signing-key» è identico in 45 file di '
           'proprietà, e altrettanto lo è l’identificativo della risorsa. Ne discende che un '
           'gettone emesso da un qualsiasi back-end è accettato da ogni altro: i domini non '
           'sono separati. I segreti dei client, per contro, variano da modulo a modulo, ma '
           'sono scritti in chiaro con il prefisso che ne dichiara l’assenza di cifratura.')

    h(d, 2, 'Un secondo meccanismo a gettone, indipendente dal primo')
    par(d, 'Il modulo dei certificati online realizza un proprio gettone JWT, con una libreria '
           'diversa e fuori dal flusso OAuth2: genera e verifica gettoni con nome, cognome e '
           'codice fiscale, firmati con un segreto dichiarato nelle proprietà del modulo '
           '(application.properties:62-64), della durata di un’ora. Gli indirizzi sono '
           '«/api/token/generate» e «/api/token/validate».')
    par(d, '⚠️ Il percorso «/api/token/**» non compare fra gli indirizzi elencati nella '
           'configurazione del resource server, e quella configurazione — come si vedrà — non '
           'ha una clausola di chiusura: **l’operazione che emette gettoni non risulta coperta '
           'da alcuna regola di autenticazione**.')

    h(d, 2, 'Le regole di autorizzazione per indirizzo')
    par(d, 'La configurazione di sicurezza del front-end [S1] è una lista unica di **210 '
           'regole** nella forma «indirizzo → elenco di ruoli ammessi», estesa su circa '
           'duecentosessanta righe e comprendente tutti i moduli: anagrafe, cambi di '
           'residenza, irreperibilità, certificati, AIRE, carte d’identità, elettorale, '
           'pagamenti. La configurazione dei back-end [S2] ha struttura analoga, con **171 '
           'regole** nella forma «indirizzo → autenticato».')
    par(d, '⚠️ **Nessuna delle due liste si chiude con una clausola generale.** Non compare '
           'mai «anyRequest()», né per richiedere l’autenticazione né per negare l’accesso. '
           'La conseguenza è di metodo prima che di merito: la protezione è ottenuta '
           'enumerando ciò che va protetto, e quindi **un indirizzo nuovo nasce non '
           'protetto** finché qualcuno non ricorda di aggiungerlo alla lista. È la ragione per '
           'cui il caso citato poco sopra si presenta.')
    par(d, 'Sei moduli fanno eccezione e adottano una configurazione propria, molto permissiva: '
           'dichiarano accessibili a tutti le proprie rotte di servizio, disabilitano la '
           'protezione contro la falsificazione di richiesta e non configurano alcun utente. '
           'Sono i moduli di allineamento di nascite, matrimoni e decessi, il modulo di '
           'fax e posta certificata, quello della carta d’identità elettronica e una copia '
           'del modulo fax collocata fuori dall’albero dei sorgenti. Altri quattro moduli '
           '(agendasc-be, clientpa, not-anpr, verifica-ele) **non dichiarano alcuna '
           'dipendenza di sicurezza**: dei 53 moduli di back-end, 45 adottano il componente '
           'comune.')

    h(d, 2, 'Ciò che non esiste')
    par(d, 'Chiude il capitolo l’elenco dei meccanismi cercati e non trovati. Sono riportati '
           'perché l’assenza accertata è un dato: evita che la stessa ricerca sia rifatta e '
           'impedisce di assumere come presente ciò che non c’è.')
    tabella(d, ASSENZE_AUT, larghezze=[2.2, 4.3])

    # ---------------------------------------------------------- 4. profilazione
    h(d, 1, 'La profilazione')
    par(d, 'Se l’autenticazione è quasi tutta fuori da SIPO, la profilazione è tutta dentro: '
           'sei tabelle dello schema anagrafico, una gestione dalle maschere e due letture che '
           'si compiono all’ingresso.')

    h(d, 2, 'Il modello dati')
    figura(d, 'prof_modello.png',
           'Figura 2 — Le tabelle della profilazione. Il perno è R_UTENTI_RUOLI, che lega '
           'in una sola riga l’utente, il ruolo, l’area tematica e la funzionalità.')
    par(d, 'Le entità e i repository che le mappano stanno tutti in [S4]; le letture che le '
           'interrogano all’ingresso appartengono invece a [S1].')
    tabella(d, [
        ['Tabella', 'Che cosa contiene', 'Da annotare'],
        ['UTENTI', 'La persona: nome utente, anagrafica, codice fiscale, indicatori di '
                   'attività e cancellazione, e i tre legami di ambito.',
         'Il legame con l’organizzazione è obbligatorio nella lettura dei ruoli: la query '
         'lo usa come giunzione, non come dato accessorio.'],
        ['CONF_RUOLI', 'Il ruolo: identificativo, descrizione e il nome tecnico usato per '
                       'comporre l’autorità.',
         '⚠️ La colonna con il nome tecnico esiste a base dati ma **non è mappata '
         'nell’entità**: è raggiunta soltanto dalla lettura in SQL nativo.'],
        ['CONF_AMBITO', 'Il raggruppamento maggiore: anagrafe, stato civile, elettorale, '
                        'statistica.',
         'I quattro valori sono documentati in un commento del codice, non in una fonte '
         'di dati.'],
        ['CONF_AREE_TEMATICHE', 'La partizione intermedia, con il proprio indirizzo di '
                                'pagina e un ordinamento.',
         'La colonna di ordinamento è usata dalla lettura ma non è mappata nell’entità.'],
        ['CONF_FUNZIONALITA', 'La singola voce: descrizione, indirizzo di pagina, '
                              'indicatore di visibilità al cittadino.',
         'È **l’unico catalogo di azioni esistente nel sistema**, ed è espresso in termini '
         'di pagine del front-end attuale.'],
        ['R_UTENTI_RUOLI', 'L’assegnazione, con quattro legami: utente, ruolo, area '
                           'tematica, funzionalità.',
         '⚠️ Nessuna validità temporale, nessun ambito. È qui che risiede, per intero, la '
         'risposta alla domanda «chi può fare che cosa».'],
    ], larghezze=[1.3, 2.4, 2.8])
    par(d, 'Due tabelle ulteriori appartengono a un’altra popolazione e non vanno confuse con '
           'le precedenti: CONF_APP_USER e CONF_APP_ROLE contengono le **utenze tecniche** con '
           'cui i front-end chiamano i back-end. Il raccordo fra il ruolo tecnico e il ruolo '
           'della persona è una colonna che contiene l’identificativo di CONF_RUOLI ma **non è '
           'dichiarata come relazione**, e le due tabelle non sono amministrate dalle maschere '
           'di gestione delle utenze: sono configurate fuori dall’applicativo.')

    h(d, 2, 'Come si ricava il permesso')
    par(d, 'All’ingresso si compiono due letture distinte, entrambe in SQL nativo [S1]. '
           'Conviene guardarle da vicino, perché la differenza fra le due è il punto più '
           'importante del capitolo.')
    par(d, 'La prima ricava i **ruoli**, e percorre cinque tabelle:')
    codice(d, 'UTENTI u, CONF_RUOLI cr, R_UTENTI_RUOLI r, CONF_APP_ROLE app,\n'
              'CONF_STRUTTURE_INTERNE_RC csir\n'
              'where u.nome_utente = ? and u.FLG_ATTIVO = ?\n'
              '  and u.id = r.id_utente and r.id_ruolo = cr.id\n'
              '  and cr.id = app.id_conf_ruoli and u.id_organizzazione = csir.id')
    par(d, 'La seconda ricava le **funzionalità**, e ne percorre quattro:')
    codice(d, 'utenti u, r_utenti_ruoli r, conf_aree_tematiche a, conf_funzionalita f\n'
              'where u.nome_utente = ?\n'
              '  and u.id = r.id_utente\n'
              '  and r.id_area_tematica = a.id_aree_tematiche\n'
              '  and r.id_funzionalita = f.id')
    par(d, '⚠️ **Nella seconda lettura il ruolo non compare.** Le funzionalità di un utente '
           'non discendono dal ruolo che gli è stato attribuito: discendono direttamente dalle '
           'righe di assegnazione che lo riguardano. Il ruolo e la funzionalità viaggiano '
           'sulla stessa riga ma restano indipendenti, e nulla impone che siano coerenti fra '
           'loro.')
    par(d, 'Ne discende la proprietà che determina il costo di gestione dell’intero impianto: '
           '**non esiste un luogo in cui sia scritto che cosa un ruolo può fare**. Un ruolo è '
           'un’etichetta; le azioni consentite sono elencate utente per utente. Per sapere '
           'che cosa comporti, ad esempio, il ruolo di funzionario di stato civile, occorre '
           'esaminare le righe di chi lo possiede e confidare che siano state compilate allo '
           'stesso modo; per modificarlo, occorre intervenire su tutte.')

    h(d, 2, 'Dove il permesso è verificato: i back-end')
    par(d, 'La sicurezza a livello di metodo è abilitata in due soli punti, entrambi nei '
           'componenti comuni di sicurezza REST, e da lì vale per i moduli che li adottano. '
           'L’annotazione di autorizzazione compare in **374 file** sotto la cartella dei '
           'back-end.')
    par(d, 'Le espressioni sono però, quasi senza eccezione, **elenchi di ruoli scritti nel '
           'codice**:')
    codice(d, '@PreAuthorize("hasAuthority(\'ROLE_AUTH_USER\') or hasAuthority(\'ROLE_ADMIN\')")')
    par(d, 'Fra tutte le espressioni presenti nei back-end **una sola** autorizza su una '
           'funzionalità anziché su un ruolo. Il catalogo delle funzionalità, che pure esiste '
           'ed è popolato, non partecipa dunque alla decisione di autorizzazione dei servizi.')
    par(d, '⚠️ Va infine ricordato, perché cambia il significato di tutto il paragrafo, che '
           '**l’autorità valutata da queste annotazioni non è quella dell’operatore**: è '
           'quella dell’utenza tecnica con cui il front-end ha ottenuto il gettone. Il '
           'controllo verifica che quel tipo di chiamante sia ammesso a quel servizio, non che '
           'quella persona lo sia.')

    h(d, 2, 'Dove il permesso è verificato: il front-end')
    par(d, 'Nel front-end la verifica è quasi interamente per indirizzo, secondo le 210 regole '
           'già descritte. La sicurezza a livello di metodo **non è abilitata**: le due sole '
           'annotazioni presenti nei moduli di front-end non hanno quindi effetto, e una delle '
           'due è per giunta commentata.')
    par(d, 'Esiste un unico controllo fondato sulle funzionalità, e si trova nel filtro di '
           'ingresso (CdRLoginFilter.java:247-250): la destinazione richiesta viene confrontata '
           'con gli indirizzi delle funzionalità possedute dall’utente.')
    codice(d, 'boolean check = StringUtils.isEmpty(goUrl)\n'
              '  || user.getAreeTematiche().stream()\n'
              '        .flatMap(areaT -> areaT.getFunzionalita().stream())\n'
              '        .map(ConfFunzionalitaVO::getUrl)\n'
              '        .anyMatch(url -> url.contains(goUrl))\n'
              '  || goUrl.equalsIgnoreCase(Constant.GOURL_HELP) || … GOURL_FAQ;')
    par(d, 'Tre proprietà di questo controllo vanno annotate. È un **controllo di soglia**: '
           'agisce sulla destinazione iniziale e non è ripercorso dalle navigazioni successive '
           'all’interno dell’applicazione. Il confronto è **per contenimento**, non per '
           'uguaglianza. E una destinazione vuota **supera il controllo**, perché la prima '
           'condizione della disgiunzione è soddisfatta.')

    h(d, 2, 'Il menu e il filtro delle azioni')
    par(d, 'Il menu è costruito dal frammento di intestazione condiviso [S5] scorrendo le aree '
           'tematiche dell’utente e, dentro ciascuna, le sue funzionalità. **È qui che il '
           'catalogo delle funzionalità produce il suo effetto principale**: non decide che '
           'cosa si possa fare, decide che cosa si veda.')
    par(d, 'I gruppi di primo livello sono però mostrati in base a sette indicatori calcolati '
           'in Java, dentro il metodo che riceve le aree tematiche (User.java:359-412), '
           'secondo l’ambito e secondo **elenchi di identificativi numerici scritti nel '
           'codice**. Gli stessi numeri ricorrono, scritti a mano, nelle condizioni del '
           'modello di pagina. Il filtro delle azioni dentro le pagine segue lo stesso '
           'criterio, confrontando identificativi numerici di ruolo:')
    codice(d, 'th:if="${user.ruoli[0].id == 1 or user.ruoli[0].id == 2 …}"'
              '     <!-- ricercaCertificatoStepUno.html:115 -->')
    par(d, '⚠️ Si noti il pedice: **il primo ruolo**. Lo stesso criterio governa la '
           'descrizione mostrata nella barra di intestazione e la scelta dell’utenza tecnica '
           'per le chiamate ai servizi. Per un utente a cui siano attribuiti più ruoli, il '
           'comportamento del sistema dipende dunque dall’ordine in cui la lettura li '
           'restituisce — che è l’ordine dell’identificativo del ruolo.')
    par(d, 'La libreria che consentirebbe di esprimere le condizioni di sicurezza direttamente '
           'nelle viste è dichiarata fra le dipendenze, ma **delle sei occorrenze presenti '
           'cinque sono commentate**; l’unica attiva si trova in una pagina del modulo di '
           'gestione degli eventi elettorali che non dichiara nemmeno lo spazio dei nomi '
           'necessario a interpretarla.')

    h(d, 2, 'L’ambito organizzativo')
    par(d, 'La nozione di ambito esiste, ed è articolata su tre dimensioni distinte: la '
           '**struttura interna** di appartenenza, la **sede di municipio** e la **struttura '
           'convenzionata** per i professionisti e gli enti esterni. Sono tre legami di '
           'UTENTI, e le tabelle di dominio ne conservano traccia: l’identificativo di '
           'organizzazione compare su atti, variazioni, rettifiche, prenotazioni e registri.')
    par(d, 'Da queste dimensioni si derivano competenze territoriali. Il caso più esplicito è '
           'il controllo di residenza del modulo di irreperibilità, che ricava il municipio '
           'dall’organizzazione e lo confronta con quello di residenza del soggetto, '
           'prevedendo un’eccezione per una organizzazione dichiarata.')
    par(d, 'Tre osservazioni sullo stato di fatto.')
    voce(d, 'Il filtro non è trasversale.',
         'Non esiste alcun meccanismo automatico che restringa le letture all’ambito '
         'dell’utente: nessun filtro dichiarativo, nessun archivio di base che lo applichi. '
         'L’ambito è aggiunto **caso per caso**, come parametro delle interrogazioni.')
    voce(d, 'L’ambito viaggia come parametro dal chiamante.',
         'Il front-end lo legge dall’oggetto di sessione — vi ricorrono 136 righe — e lo '
         'accoda alla chiamata; il back-end lo riceve come parametro di richiesta in 32 punti. '
         '⚠️ **Nulla verifica che corrisponda a quello dell’utente autenticato**, e nulla '
         'potrebbe verificarlo, poiché l’autorità presente nel gettone è quella dell’utenza '
         'tecnica, che di organizzazione non ne ha.')
    voce(d, 'L’ambito non si può attribuire a un’assegnazione.',
         'Essendo attributo dell’utente e non della riga di assegnazione, **non è esprimibile '
         'un ruolo limitato a un municipio**: chi possiede un ruolo lo possiede ovunque la sua '
         'organizzazione arrivi. Si aggiunga che la sede di municipio, pur presente in tabella, '
         'non è riportata sull’oggetto di sessione.')

    h(d, 2, 'L’amministrazione delle utenze')
    par(d, 'Esiste una gestione completa, con maschera dedicata e servizi propri: si creano e '
           'si modificano utenti e assegnazioni, e si consultano gli elenchi di '
           'organizzazioni, ruoli, aree tematiche e funzionalità per area. È la superficie '
           'attraverso cui il permesso viene attribuito.')
    par(d, 'Due limiti sono rilevanti per una descrizione dello stato di fatto. Le utenze '
           'tecniche **non sono amministrate da questa maschera**: vivono in tabelle proprie e '
           'sono configurate al di fuori dell’applicativo. E la gestione **non lascia traccia**: '
           'le assegnazioni sono create, modificate e cancellate senza che nulla registri chi '
           'sia intervenuto, quando e su che cosa.')

    h(d, 2, 'Ciò che non esiste')
    tabella(d, ASSENZE_PROF, larghezze=[2.2, 4.3])

    # ---------------------------------------------------------- 4bis. librerie
    h(d, 1, 'Le librerie e le strutture disponibili')
    par(d, 'I due capitoli precedenti hanno descritto il **meccanismo**: come l’identità '
           'entra e come il permesso viene deciso. Questo capitolo descrive il '
           '**patrimonio**: quali componenti riusabili esistono nel workspace, quali sono in '
           'esercizio e quali giacciono inerti. La distinzione conta, perché una capacità che '
           'esiste ma non è collegata a nulla non è una funzione del sistema: è un materiale '
           'a disposizione, e va contata come tale e non di più.')

    h(d, 2, 'Le librerie in uso')
    tabella(d, LIBRERIE_USO, larghezze=[1.7, 3.2, 1.6])
    par(d, '⚠️ Si noti la quarta riga, perché smentisce un’impressione che i capitoli '
           'precedenti potrebbero avere lasciato. **SIPO possiede uno stack crittografico '
           'maturo**: carica keystore PKCS#12, estrae chiavi private, produce e verifica '
           'firme CMS, costruisce asserzioni SAML, firma messaggi SOAP con marca temporale. '
           'Solo che tutto ciò **non serve a riconoscere gli operatori**: serve a identificare '
           'il Comune verso ANPR e verso il Ministero. Le due sicurezze — quella delle '
           'persone e quella delle macchine — hanno in SIPO maturità molto diverse.')

    h(d, 2, 'L’identità di postazione: certificati, firma e registro')
    par(d, 'È la parte meno nota dell’impianto e merita di essere descritta per intero, '
           'perché è anche la sola che tratti materiale crittografico reale. Le fonti sono '
           '[S8] per il consumo e [S9] per l’arruolamento; il medesimo stack serve anche i '
           'canali descritti in [S10].')
    par(d, 'Esiste un **registro delle postazioni** in due tabelle dello schema anagrafico, '
           'ANAG_USR.REG_USER_ANPR e REG_USER_ANPR_SIGN. La prima conserva, per ciascuna '
           'postazione, l’operatore, la sede, il certificato in formato PKCS#12 come dato '
           'binario e la parola d’ordine del keystore cifrata; la seconda l’alias, il numero '
           'di serie e la **firma dell’identificativo di postazione**.')
    par(d, 'Il popolamento avviene per **arruolamento**. Il modulo anagrafico espone '
           'un’operazione REST, protetta da ruolo, che riceve un archivio compresso di file '
           'PKCS#12 e il prospetto delle relative parole d’ordine; per ciascuno estrae chiave '
           'privata, certificato e numero di serie, calcola una firma CMS/PKCS#7 con '
           'SHA256withRSA dell’identificativo di postazione e la registra. La stessa '
           'procedura esiste anche come **programma a riga di comando** in '
           'cross/firma-id-postazione, con una propria copia della medesima logica.')
    par(d, 'Il consumo avviene dal lato opposto. Il client ANPR, prima di ogni chiamata, '
           'invoca una procedura di base dati che restituisce sede, identificativo di '
           'postazione, certificato, parola d’ordine, alias e la firma precalcolata; il '
           'materiale così ottenuto alimenta il keystore di postazione, la firma del '
           'messaggio SOAP e l’asserzione SAML verso ANPR. Un parametro di configurazione '
           'decide se la firma dell’identificativo debba essere **ricalcolata al momento** '
           'oppure **riletta dal registro**.')
    par(d, '⚠️ Tre riserve, tutte accertate, che vanno lette insieme alla descrizione. '
           'La prima: **l’identificativo di postazione passato alla procedura è scritto nel '
           'codice** e sovrascrive quello ricevuto, sicché verso ANPR ogni chiamata proviene '
           'dalla stessa postazione, chiunque stia operando (R-16, PA-12). La seconda: la '
           'configurazione che collega il callback SAML al canale sta in **due file orfani**, '
           'e dal solo codice non è dimostrabile che quella parte sia mai eseguita (R-18, '
           'PA-10). La terza: **il sorgente della procedura di lettura non è nel '
           'repository**, e neppure il DDL delle due tabelle, i cui conti fra dati di '
           'collaudo e istruzioni di inserimento non tornano (PA-9).')

    h(d, 2, 'Le capacità presenti ma non utilizzate')
    par(d, 'Sono il risultato più istruttivo della ricognizione. Nessuna di queste voci è un '
           'difetto in sé; insieme però raccontano un sistema in cui si è cominciato più '
           'volte a fare una cosa e non la si è finita.')
    tabella(d, CAPACITA_INERTI, larghezze=[1.7, 2.6, 2.2])
    par(d, '⚠️ La prima riga è la più significativa. Qualcuno ha scritto, per intero, '
           'l’autorizzazione per permessi — quella che manca a tutto il sistema e che il '
           'capitolo sulla profilazione ha descritto come assente — e l’ha poi commentata. '
           'Il fatto che il codice referenzi una classe inesistente dice che **non è stato '
           'commentato perché superato, ma perché non funzionava ancora**. La capacità che il '
           'modello dei permessi richiede non è dunque inesplorata: è stata tentata.')

    h(d, 2, 'Il materiale crittografico nel repository')
    par(d, 'La ricognizione ha accertato che nel versionamento si trovano chiavi private e '
           'segreti di esercizio. Si riporta perché è materia di fatto, non di valutazione.')
    voce(d, 'Chiavi private di produzione.',
         'Sette file PKCS#12 nella cartella di produzione del client ANPR, più le copie di '
         'collaudo, triplicate in tre percorsi, e una copia residua nell’area di lavoro di un '
         'ambiente di sviluppo.')
    voce(d, 'Parole d’ordine dei keystore in chiaro.',
         'Nei file di proprietà dei tre ambienti del client ANPR — e la medesima parola '
         'd’ordine vale per tutti e tre — nonché nei file del canale SIEL, dove peraltro i '
         'PKCS#12 corrispondenti non sono presenti: sono versionate le sole parole d’ordine.')
    voce(d, 'Dati personali.',
         '⚠️ I file di proprietà di produzione e preproduzione del client ANPR contengono il '
         '**codice fiscale di operatori reali** nel campo dell’operatore. È un profilo '
         'distinto dal segreto applicativo (R-19).')
    voce(d, 'Cifratura simmetrica duplicata.',
         'La classe TripleDes esiste in **sedici copie** indipendenti, con tre chiavi '
         'distinte scritte nei sorgenti; opera in modalità a blocchi indipendenti, senza '
         'vettore di inizializzazione.')
    par(d, 'Due librerie di terze parti meritano una nota di versione: BouncyCastle è alla '
           'versione 1.78.1 nel programma di firma delle postazioni — recente — mentre le '
           'copie incluse nell’altro prodotto descritto qui sotto sono ferme a una versione '
           'del 2007, e la sua libreria di sicurezza applicativa a una del 2014.')

    h(d, 2, 'L’origine dell’impianto')
    par(d, 'Un ritrovamento della ricognizione spiega molto di ciò che i capitoli precedenti '
           'hanno descritto. Nel workspace è presente **cross/Signps** [S11], che non è un modulo '
           'di SIPO ma un prodotto a sé: il sistema per la gestione delle nomine di '
           'presidenti e scrutatori, con repository proprio, schema di base dati proprio e '
           'una pila tecnologica diversa — applicazione JEE classica con una versione di '
           'Spring Security del 2014. Fra i due prodotti **non esiste alcun riferimento '
           'incrociato di codice**, in nessuna direzione.')
    par(d, 'Contiene però classi con gli stessi nomi e gli stessi ruoli di quelle di '
           'common/profilazione-utente: il filtro di ingresso dal portale, il filtro di '
           'pre-autenticazione, il punto di ingresso della sicurezza, il gestore della '
           'disconnessione, il modello dell’utente, l’interceptor di sessione invalida, il '
           'filtro di diagnosi della giunzione. **L’impianto di autenticazione di SIPO è con '
           'ogni probabilità il port a Spring Boot di quel codice.**')
    par(d, 'Non è una curiosità archeologica: è la spiegazione di due fatti altrimenti '
           'oscuri. Spiega perché SIPO si porti dietro classi inerti che nell’altro prodotto '
           'sono vive — l’interceptor di sessione invalida vi è registrato davvero — e '
           'spiega l’età del disegno. ⚠️ Va segnalato per contro che l’altro prodotto possiede '
           'una cosa che SIPO non ha: **un gestore di gettone contro la falsificazione di '
           'richiesta**.')

    # ---------------------------------------------------------- 5. tracciamento
    h(d, 1, 'Il tracciamento delle azioni')
    par(d, 'Il sistema conserva memoria di poche cose, in modi non uniformi, e mai attraverso '
           'un meccanismo generale.')
    par(d, '**Non esiste alcuna forma di registrazione automatica.** Le annotazioni che '
           'Spring Data mette a disposizione per attribuire a ogni riga il suo autore e il suo '
           'momento non compaiono in nessun punto del perimetro; non vi sono ascoltatori di '
           'entità, né interceptor di persistenza. Le colonne «chi» esistono dove qualcuno le '
           'ha aggiunte, e sono **nove occorrenze** di un nome più poche altre con **cinque '
           'nomi diversi**. Le colonne di data sono invece diffuse, spesso senza la colonna di '
           'utente corrispondente: si sa quando, non da chi.')
    par(d, '⚠️ Dove la colonna esiste, il valore **arriva dal client**: è preso dal parametro '
           'della richiesta e assegnato direttamente. Una traccia così formata registra ciò '
           'che il chiamante ha dichiarato di essere, non ciò che il sistema ha accertato.')
    par(d, 'Esistono due registri applicativi veri, entrambi specifici:')
    tabella(d, [
        ['Registro', 'Che cosa conserva', 'Da annotare'],
        ['ESTRATTI_DOWNLOAD_LOG',
         'I rilasci di estratti: utente, organizzazione, municipio, data, tipo di estratto e '
         'di rilascio, dati dell’atto.',
         '⚠️ Ha una **lista di esclusione**: se l’indicatore della tabella delle utenze '
         'vale «Y», il rilascio non viene registrato.'],
        ['LOG_EVENTI_STATO_CIVILE',
         'Gli errori di integrazione con ANPR: tipo di evento, tipo ed esito dell’errore, '
         'identificativo dell’operazione.',
         'È un registro tecnico: **non contiene l’utente**.'],
    ], larghezze=[1.5, 2.6, 2.4])
    par(d, 'Nello stato civile non esiste alcuna tabella di audit generale. L’unica tabella di '
           'audit mappata da un’entità nell’intero perimetro appartiene al dominio elettorale. '
           'Resta, come traccia degli accessi, una riga di registro applicativo scritta a ogni '
           'connessione con nome utente, gruppo, indirizzo della postazione, numero di serie '
           'del certificato, identificativo e momento di creazione della sessione '
           '(CdRLoginFilter.java:234-236): è un file, non un dato interrogabile.')

    # ---------------------------------------------------------- 6. duplicazioni
    h(d, 1, 'La duplicazione dell’impianto')
    par(d, 'L’intero impianto descritto esiste in **due copie**. Sotto la radice delle elezioni '
           'si trovano un secondo modulo di profilazione, un secondo componente di sicurezza '
           'REST e un secondo client, con le classi omonime: la lettura dei dati di '
           'profilazione, il modello dell’utente, la configurazione di sicurezza, il servizio '
           'che carica le autorità. Le entità delle tabelle di profilazione sono a loro volta '
           'duplicate, e ne esistono varianti per lo stato civile e sinonimi per l’elettorale.')
    par(d, '⚠️ La duplicazione riguarda anche il file che contiene le credenziali tecniche, '
           'che è ripetuto per intero. Dal punto di vista dello stato di fatto ciò significa '
           'che **una modifica all’impianto di sicurezza non ha un solo luogo in cui essere '
           'fatta**, e che le due copie possono divergere senza che nulla lo segnali. Un '
           'modulo di front-end risulta inoltre presente in duplice esemplare, uno dei quali '
           'nominato come copia di salvataggio.')

    # ---------------------------------------------------------- 7. rilievi
    h(d, 1, 'Rilievi')
    par(d, 'Si raccolgono qui i punti in cui il sistema si comporta diversamente da come '
           'ci si attenderebbe leggendone la documentazione o osservandone le maschere. '
           'Sono osservazioni sullo stato di fatto: il documento non propone correzioni e non '
           'attribuisce priorità, perché la valutazione del rischio richiede di conoscere il '
           'contesto di rete in cui il sistema opera, che non è fra le fonti disponibili '
           '(PA-2).')
    tabella(d, RILIEVI, larghezze=[0.5, 1.5, 3.0, 1.1])

    # ---------------------------------------------------------- 8. angular
    h(d, 1, 'Il riuso per le nuove applicazioni')
    par(d, 'Le nuove applicazioni di front-end sono state impostate come micro-front-end '
           'Angular su una libreria condivisa di Roma Capitale [S6], secondo quanto descritto '
           'in [S7]. La domanda che questo capitolo affronta è che cosa, di quanto descritto '
           'nei capitoli precedenti, possa servirle.')
    par(d, '**La domanda non ha una risposta sola, perché non c’è un impianto solo.** Ciò che '
           'i capitoli precedenti hanno censito si divide in tre famiglie, con destini '
           'diversi, e confonderle è il modo più rapido per rispondere male.')
    tabella(d, [
        ['Famiglia', 'Che cosa comprende', 'Esito'],
        ['Il meccanismo di riconoscimento dell’utente',
         'Gli header del portale, il filtro di ingresso, la sessione lato server, '
         'l’autorizzazione per indirizzo, le utenze tecniche verso i back-end.',
         '**Non trasferibile.** È legato a una forma di applicazione che le nuove non hanno.'],
        ['Le strutture dati della profilazione',
         'Le sei tabelle di utenti, ruoli, ambiti, aree tematiche, funzionalità e '
         'assegnazioni; le tre dimensioni di ambito organizzativo.',
         '**Trasferibili**, con due correzioni che il capitolo argomenta.'],
        ['Le librerie di identità di macchina',
         'Lo stack keystore, firma CMS, SAML e WS-Security del client ANPR e del canale '
         'SIEL; il registro delle postazioni e l’arruolamento dei certificati.',
         '**Riusabili così come sono**, e indipendenti dalla tecnologia di front-end.'],
    ], larghezze=[1.7, 2.9, 1.9])
    par(d, 'In sintesi: **non è riusabile il modo in cui SIPO riconosce le persone; sono '
           'riusabili il modo in cui descrive i loro permessi e il modo in cui riconosce le '
           'macchine.** Le tre famiglie sono trattate qui di seguito, dopo una ricognizione '
           'di ciò che la libreria condivisa già offre.')

    h(d, 2, 'Che cosa la libreria condivisa già prevede')
    par(d, 'Prima di valutare il riuso conviene accertare che cosa esista dall’altra parte. '
           'La libreria porta un impianto proprio, completo nella forma.')
    tabella(d, [
        ['Elemento', 'Realizzazione verificata'],
        ['Servizio di sessione',
         'AuthenticationService, con il profilo conservato in localStorage sotto la chiave '
         '«auth» e replicato in memoria in un soggetto osservabile. Il profilo comprende il '
         'gettone, l’elenco delle abilitazioni e tre nozioni di ambito: struttura, ufficio e '
         'tributo.'],
        ['Rinvio al servizio di identità',
         'AuthenticationIAMGuard rinvia, con un cambio di pagina, a '
         '/msAuth/api/v1/autenticazione/loginIAM. ⚠️ Il codice porta il commento «manca '
         'codice ambito e applicazione»: la funzione è dichiarata incompleta dai suoi stessi '
         'autori.'],
        ['Guardie di rotta',
         'Quattro, tutte nella forma CanActivate o CanActivateChild. Una verifica la '
         'presenza del gettone, una le abilitazioni, una un semplice indicatore booleano.'],
        ['Modello di autorizzazione',
         'Le **abilitazioni**: un elenco di stringhe nel profilo. AbilityService offre le tre '
         'verifiche (possiede, possiede almeno una, possiede tutte); AuthorizationService '
         'filtra un insieme di elementi confrontando le abilitazioni richieste con quelle '
         'possedute. La guardia applica lo stesso criterio alle rotte, con esito positivo se '
         '**almeno una** delle richieste è posseduta.'],
        ['Trattamento degli errori',
         'L’intercettore gestisce il 401 cancellando la sessione locale e rinviando alla '
         'disconnessione, e il 503 rinviando a una pagina di manutenzione. ⚠️ **Non esiste un '
         'trattamento specifico del 403**: un diniego di autorizzazione produce solo un '
         'messaggio generico.'],
    ], larghezze=[1.5, 5.0])
    par(d, '⚠️ Due lacune vanno dichiarate, perché incidono sulla valutazione. '
           'L’**intercettore di autenticazione non aggiunge alcun header**: riceve il servizio '
           'di sessione ma non lo usa, e restituisce la richiesta immutata. Esiste un '
           'segnaposto che allude a un gestore del gettone, ma nessun intercettore lo '
           'consuma. La costruzione effettiva degli header avviene in una classe astratta di '
           'un pacchetto privato, risolto da un registro interno e non presente nel workspace: '
           '**dove il gettone venga agganciato alle chiamate non è accertabile** (PA-5). Per '
           'la stessa ragione la forma completa del profilo non è ispezionabile: se ne '
           'conoscono i soli campi che il codice legge (PA-4).')

    h(d, 2, 'Prima famiglia: il meccanismo di riconoscimento')
    par(d, 'L’identificazione per header iniettati dalla giunzione **non è portabile su '
           'un’applicazione Angular**, e la ragione non è di opportunità ma di forma.')
    par(d, 'Il meccanismo attuale funziona perché ogni pagina di SIPO è prodotta dal server: '
           'la richiesta che genera la pagina è la stessa che porta gli header, e la sessione '
           'che ne deriva vive nel server e accompagna ogni richiesta successiva dello stesso '
           'browser. Un’applicazione Angular non funziona così: è un insieme di file statici '
           'che il browser scarica una volta e poi esegue, e ogni dato successivo arriva da '
           'chiamate a servizi. **Non c’è una pagina da produrre e non c’è una sessione lato '
           'server in cui depositare l’identità.**')
    par(d, 'Se ne ricava che i due modelli sono alternativi e non componibili: o l’identità '
           'sta in un gettone che il client conserva e presenta, come la libreria già assume, '
           'oppure sta in header che un livello di rete aggiunge, come SIPO assume. '
           '**Tentare di averli entrambi significherebbe mantenere due verità sull’identità '
           'dello stesso operatore**, con il problema, non risolvibile dal codice applicativo, '
           'di decidere quale prevalga quando divergono.')
    par(d, 'Non sono trasferibili, per ragioni analoghe o conseguenti, anche i seguenti '
           'elementi.')
    voce(d, 'L’autorizzazione per indirizzo.',
         'Le 210 regole valutate dal server presuppongono che il server conosca l’indirizzo '
         'richiesto e possa negarlo. In un’applicazione a pagina singola la navigazione è '
         'interna al browser: l’equivalente è la guardia di rotta, che la libreria già offre. '
         'Va notato che **una guardia lato client non è un controllo di sicurezza**: nasconde, '
         'non impedisce. Il controllo effettivo resta sui servizi.')
    voce(d, 'Il ruolo come veicolo dell’autorizzazione.',
         'La libreria **non ha una nozione di ruolo**: non compaiono i termini ruolo, permesso '
         'o ambito di autorizzazione, ma solo abilitazioni. Trasferire i ruoli significherebbe '
         'introdurre nella libreria un concetto che non le appartiene, mentre la traduzione '
         'nell’altro verso — dal ruolo alle abilitazioni che comporta — è possibile ed è '
         'discussa più avanti.')
    voce(d, 'Le utenze tecniche per chiamare i servizi.',
         'È lo schema che oggi fa perdere l’identità dell’operatore fra front-end e back-end '
         '(R-05). La libreria assume l’opposto: un gettone per persona, che accompagna le '
         'chiamate. Riproporre le utenze tecniche significherebbe **riprodurre nel nuovo '
         'impianto il difetto del vecchio**, e per giunta a fronte di un meccanismo già '
         'predisposto a evitarlo.')

    h(d, 2, 'Seconda famiglia: le strutture dati della profilazione')
    par(d, 'La parte riusabile è il modello di profilazione, e il raccordo è più diretto di '
           'quanto la distanza tecnologica lasci supporre.')
    par(d, '**Il corrispondente delle abilitazioni esiste già e si chiama CONF_FUNZIONALITA.** '
           'La libreria chiede al profilo un elenco di stringhe e verifica se contenga quelle '
           'richieste; il sistema attuale possiede un catalogo di voci, associate a ciascun '
           'utente attraverso la tabella di assegnazione. Le due nozioni combaciano quasi '
           'esattamente: cambia la forma — una tabella contro un elenco — non la sostanza. '
           'Ciò che [S7] registra come mancante non è dunque il meccanismo né il dato, ma il '
           '**vocabolario**: quali abilitazioni debbano esistere per lo stato civile.')
    par(d, 'La tabella seguente mette a fronte gli elementi dei due impianti.')
    tabella(d, MAPPA_ANGULAR, larghezze=[2.1, 2.9, 1.5])
    par(d, '⚠️ Due avvertenze sul riuso, che discendono dai rilievi del capitolo precedente e '
           'sono la ragione per cui il riuso non può essere una copia.')
    voce(d, 'Il catalogo va ripensato per azioni, non per pagine.',
         'CONF_FUNZIONALITA descrive **voci di menu con il loro indirizzo**, ed è questa forma '
         'a renderla oggi inutilizzabile per autorizzare un servizio: fra i back-end una sola '
         'espressione di autorizzazione si fonda su una funzionalità, tutte le altre sui '
         'ruoli. Un’abilitazione che dica «può annullare un atto» è riusabile da una rotta '
         'Angular, da un pulsante e da un servizio; una che dica «/statocivile/ricerca» è '
         'riusabile soltanto da una rotta. **Il catalogo è trasferibile come struttura; il suo '
         'contenuto va riscritto in termini di azioni.**')
    voce(d, 'L’assegnazione va portata sul ruolo.',
         'Trasferendo R_UTENTI_RUOLI così com’è si trasferirebbe anche la sua proprietà più '
         'onerosa: il permesso attribuito utente per utente, senza che esista un luogo in cui '
         'leggere che cosa un ruolo comporti. **Nel modello per abilitazioni la traduzione '
         'naturale è opposta**: il ruolo porta un insieme di abilitazioni, l’utente riceve il '
         'ruolo, e il profilo che il servizio di identità restituisce contiene l’unione delle '
         'abilitazioni dei ruoli posseduti. La tabella di assegnazione resta, ma diventa un '
         'legame fra utente e ruolo, e nasce accanto a essa la tabella oggi mancante fra ruolo '
         'e abilitazione.')
    par(d, '⚠️ Su questa seconda correzione vale la pena aggiungere un fatto emerso dalla '
           'ricognizione delle librerie, perché cambia il modo di valutarla. **Il passaggio '
           'da un’autorizzazione per indirizzo a una per permessi è già stato tentato in '
           'SIPO, e non è stato portato a termine**: le quattro classi che lo realizzavano '
           'sono commentate per intero e referenziano una classe mai scritta. Non si tratta '
           'dunque di una direzione inesplorata né di un’idea estranea alla cultura del '
           'progetto; si tratta di un lavoro interrotto, e la libreria Angular assume '
           'esattamente il modello che quel lavoro voleva introdurre.')
    par(d, 'Vi è infine l’**ambito organizzativo**, che è l’elemento più prossimo al riuso '
           'immediato e insieme il più incerto. La libreria porta nel profilo tre nozioni — '
           'struttura, ufficio e tributo — che nella forma corrispondono a quelle di SIPO: '
           'organizzazione, sede di municipio, struttura convenzionata. Se siano le stesse '
           'nozioni, con la stessa codifica e la stessa origine, **non è accertabile dalle '
           'fonti** (PA-7). Se lo fossero, il riuso sarebbe diretto e porterebbe con sé un '
           'miglioramento non accessorio: l’ambito viaggerebbe **dentro il profilo** anziché '
           'come parametro dichiarato dal chiamante, e verrebbe meno la condizione che oggi '
           'rende il controllo di competenza territoriale aggirabile (R-07).')

    h(d, 2, 'Terza famiglia: le librerie di identità di macchina')
    par(d, 'È la famiglia che la prima stesura di questo documento non conteneva, ed è quella '
           'con l’esito più favorevole. **Queste librerie sono riusabili così come sono, e per '
           'una ragione che le distingue da tutto il resto: non hanno nulla a che vedere con '
           'la tecnologia del front-end.**')
    par(d, 'Caricare un keystore PKCS#12, estrarne la chiave privata, produrre una firma '
           'CMS/PKCS#7, costruire un’asserzione SAML, firmare un messaggio SOAP con marca '
           'temporale: sono operazioni che avvengono in un processo di back-end, su richiesta '
           'di qualcuno, e a cui è del tutto indifferente se quel qualcuno sia una pagina '
           'prodotta dal server o un’applicazione Angular. **Il confine che rende non '
           'trasferibile il meccanismo di riconoscimento — la scomparsa della sessione lato '
           'server — qui non passa.**')
    par(d, 'Vale la pena essere espliciti su quanto sia il patrimonio, perché è maggiore di '
           'quanto il progetto sembri ricordare: trenta moduli di back-end hanno già nel '
           'proprio percorso di classe una libreria che sa fare tutto questo, e in esercizio '
           'la usano ogni volta che parlano con ANPR. Un’applicazione nuova che debba '
           'presentarsi a un ente terzo con un certificato non parte da zero.')
    par(d, '⚠️ Tre riserve, però, che non sono di principio ma di igiene, e che il riuso deve '
           'affrontare invece di ereditare.')
    voce(d, 'La logica è duplicata tre volte.',
         'La firma dell’identificativo di postazione esiste in tre implementazioni '
         'indipendenti, e la cifratura simmetrica in sedici copie con tre chiavi diverse '
         '(R-21). Riusare significa **scegliere quale copia diventa la libreria**, non '
         'aggiungerne una quarta.')
    voce(d, 'Una parte non è dimostrabilmente attiva.',
         'Il collegamento del callback SAML sta in due file orfani, e dal codice non risulta '
         'che venga eseguito (R-18, PA-10). Prima di riusare quella parte occorre sapere se '
         'oggi funzioni, e come.')
    voce(d, 'Il materiale crittografico è nel versionamento.',
         'Chiavi private di produzione, parole d’ordine identiche nei tre ambienti e dati '
         'personali stanno nel repository (R-13, R-19). È un difetto della conservazione dei '
         'segreti, non delle librerie: ma un riuso che lo ricopiasse lo moltiplicherebbe.')

    h(d, 2, 'Una struttura che già esiste: il registro delle postazioni')
    par(d, 'Merita un paragrafo a sé perché è una **struttura**, non una libreria, e perché è '
           'il caso in cui il riuso costa meno di tutti: non va scritto nulla, va solo '
           'accertato che cosa c’è.')
    par(d, 'Il registro associa a ciascuna postazione la sede, l’operatore, il certificato, '
           'la parola d’ordine cifrata e la firma dell’identificativo; l’arruolamento dei '
           'certificati è già un’operazione esposta e protetta da ruolo. Un’applicazione '
           'nuova che debba sapere da quale postazione avviene un’operazione, o presentarsi '
           'con il certificato di quella postazione, ha già dove leggerlo.')
    par(d, '⚠️ Con due avvertenze rilevanti. La prima: oggi **l’identificativo di postazione '
           'effettivamente usato è fisso** (R-16), quindi il registro è popolato e '
           'interrogabile ma il suo contenuto non discrimina chi sta operando; se questa sia '
           'una svista o una scelta di accreditamento è il punto aperto PA-12, e la risposta '
           'decide se la struttura sia riusabile tal quale o vada prima corretta. La seconda: '
           '**il DDL delle due tabelle e il sorgente della procedura che le legge non sono '
           'nel repository** (PA-9): la struttura si conosce per come la usano i programmi, '
           'non per come è dichiarata.')

    h(d, 2, 'Due cose che sembrano riusabili e non lo sono')
    par(d, 'La ricognizione ha portato alla luce due componenti che a prima vista '
           'risponderebbero proprio al bisogno delle nuove applicazioni. Si argomenta qui '
           'perché non siano la risposta, affinché la valutazione non debba essere rifatta.')
    voce(d, 'Il servizio di gettoni già presente in cert-online-be.',
         'Emette e verifica gettoni JWT con nome, cognome e codice fiscale: sembra il '
         'meccanismo che alle applicazioni Angular serve. ⚠️ Ma il segreto di firma è scritto '
         'in chiaro nel repository, la firma è simmetrica — chi verifica può anche emettere — '
         'il presidio a chiave non funziona per un errore di percorso (R-17), il nome stesso '
         'del pacchetto denuncia l’origine da un modello estraneo al modulo, e **nessuno lo '
         'consuma**. Non è un impianto di identità: è un servizio rimasto acceso.')
    voce(d, 'Le librerie di accesso unico del sistema precedente.',
         'In cross/cert-online-dotnet giace un impianto completo — moduli di autenticazione, '
         'generatore di gettoni, gestione di utenti, gruppi e diritti, archivio cifrato. È '
         'però in tecnologia .NET: **nessun consumatore Java può usarlo**, e le nuove '
         'applicazioni non sono .NET. Va contato come storia, non come patrimonio.')

    h(d, 2, 'A quali condizioni il riuso è praticabile')
    par(d, 'Riassumendo in forma di condizioni, e senza indicare soluzioni, il riuso richiede '
           'che siano prima chiarite otto cose. Le prime cinque riguardano le persone, le '
           'ultime tre le macchine.')
    tabella(d, [
        ['Condizione', 'Stato'],
        ['Che sia noto se msAuth e il sistema di accesso del portale siano la stessa '
         'identità, o due.',
         'Non accertabile dalle fonti — PA-3. È la condizione preliminare: da essa dipende se '
         'gli operatori avranno una o due identità, e se un utente profilato in SIPO sia '
         'riconoscibile dalla nuova applicazione.'],
        ['Che sia nota la forma del profilo restituito dal servizio di identità.',
         'Non ispezionabile: il tipo proviene da un pacchetto privato assente dal workspace — '
         'PA-4. Senza, non è dimostrabile che il profilo possa portare le abilitazioni e '
         'l’ambito nella forma richiesta.'],
        ['Che sia definito il vocabolario delle abilitazioni dello stato civile.',
         'Da scrivere — PA-6. Il catalogo esistente è per pagine e va riespresso per azioni; '
         'è lavoro di analisi, non di realizzazione.'],
        ['Che sia stabilito se l’ambito organizzativo entri nel profilo.',
         'Da decidere — PA-7. Riguarda anche la corrispondenza fra le tre nozioni della '
         'libreria e le tre di SIPO.'],
        ['Che sia deciso come le due popolazioni convivano nel periodo di transizione.',
         'Non trattato da alcuna fonte. Finché esisteranno insieme maschere di SIPO e '
         'applicazioni Angular, lo stesso operatore attraverserà i due impianti nella stessa '
         'giornata di lavoro; se il profilo sia uno o due, e quale prevalga, è questione '
         'aperta.'],
        ['Che sia accertato se il canale sicuro verso ANPR funzioni come il codice lascia '
         'supporre.',
         'Non dimostrabile dai sorgenti — PA-10. Riguarda la parte SAML delle librerie '
         'crittografiche: se non fosse attiva, ciò che si riusa è meno di ciò che si legge.'],
        ['Che sia deciso se l’identificativo di postazione debba tornare a essere reale.',
         'Oggi è fisso — R-16, PA-12. Finché lo è, il registro delle postazioni è riusabile '
         'come archivio di certificati ma non come fonte di identità della postazione.'],
        ['Che sia scelta quale copia delle librerie crittografiche diventi la libreria.',
         'La firma esiste in tre implementazioni e la cifratura in sedici — R-21. È una '
         'scelta da compiere prima del riuso, non una conseguenza di esso.'],
    ], larghezze=[2.8, 3.7])
    par(d, 'Una considerazione conclusiva, che non è una raccomandazione ma una '
           'constatazione. Ciò che di SIPO invecchia male è **il modo in cui riconosce le '
           'persone**: è legato a una forma di applicazione che le nuove non hanno, e non lo '
           'si porta avanti. Ciò che invece regge sono **le descrizioni e gli strumenti**: le '
           'sei tabelle di profilazione, che sono oggi la sola descrizione esistente di chi '
           'fa che cosa e in quale ambito, e le librerie crittografiche, che risolvono '
           'problemi difficili e indifferenti alla tecnologia di chi le invoca.')
    par(d, '⚠️ Va detta però anche la cosa meno comoda, perché la ricognizione la mostra con '
           'chiarezza. Il patrimonio riusabile **non è in ordine**: la stessa logica è '
           'scritta più volte, una parte non è dimostrabilmente collegata, i segreti e alcuni '
           'dati personali stanno nel versionamento, e il tentativo di passare a un modello a '
           'permessi è stato interrotto a metà. Nessuno di questi è un ostacolo al riuso; '
           'tutti sono lavoro che il riuso rende inevitabile, perché **ciò che si riusa si '
           'moltiplica, difetti compresi**.')

    # ---------------------------------------------------------- 9. punti aperti
    h(d, 1, 'Registro dei punti aperti')
    par(d, 'Le questioni che il documento ha incontrato e che le fonti disponibili non '
           'consentono di chiudere. Sono numerate con il prefisso PA per non confondersi con i '
           'registri degli altri documenti di progetto.')
    tabella(d, PUNTI, larghezze=[0.5, 1.7, 3.0, 1.1])


if __name__ == '__main__':
    d = costruisci()
    copertina(d)
    scrivi(d)
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    print('capitoli/tabelle/immagini:', D.riepilogo(OUT))
