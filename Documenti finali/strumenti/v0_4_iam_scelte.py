# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.3 → v0.4 (06/10/2026).

Due cose: la verifica di congruenza con la documentazione nuova della cartella
«Sorgenti Documentali/Interazione IAM», e il capitolo 6 «Scelte effettuate», che
recepisce in termini operativi «Processo_Autenticazione_sipo-auth.txt».

⚠️ Verifiche fatte di persona sulle fonti, non riprese dalle analisi del fornitore:
  · «management» NON è un servizio di IAM: le 57 occorrenze nel manuale sono il titolo
    del documento stesso (Identity and Access **Management**). PI-05 si chiude.
  · `iv_pg_*` / `iv_dg_*` / `iv_ass_*` NON esistono: 0 occorrenze. Persona giuridica e
    delega stanno solo negli header `IV-PG-*` (Tab. 3) e `IV-DG-*` (Tab. 4.1), e il
    §3.9.2.1 dichiara che i claim corrispondono alla sola Tabella 2. «assistito» non
    compare mai. ⚠️ Il committente ha chiesto di descrivere comunque la fase 3 in forma
    affermativa: il rilievo resta nei punti aperti, non nel corpo.
  · In OIDC non esiste alcun claim di gruppo o ruolo: `iv-portal-groups` è solo header.
  · `getRuoloBe()` nei front-end: 4.781 — verificato, è il numero che decide.
  · AnprClient: 59 dichiarazioni nei pom, 41 moduli distinti di back-end (non «trenta»).
  · msAuth esiste nella libreria Angular (AuthenticationIAMGuard), non nel manuale IAM,
    e nella libreria non è richiamato da nessuno.
  · Il vocabolario dell'autorizzazione non coincide: i BE su un ruolo solo, l'Angular su
    `user.abilitazioni`. Il token SIPO non porta le abilitazioni.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_4_iam_scelte.py
"""
import os
import shutil
import subprocess
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.3.docx')
DST = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.4.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

PARTECIPANTI = [
    ['Componente', 'Che cosa fa', 'Stato'],
    ['IAM di Roma Capitale',
     'Autentica la persona con OIDC. Resta l’unico luogo in cui si verificano le '
     'credenziali, SPID o CIE.', 'Esistente'],
    ['sipo-auth',
     '**Il solo punto di autenticazione di SIPO.** Parla con IAM, recupera il profilo ed '
     'emette il token SIPO. Espone il JWKS con cui i back-end verificano la firma. Fa da '
     'BFF per la shell Angular.', '**Nuovo**'],
    ['sipo-profili',
     'Restituisce ruoli, aree e funzionalità dell’utente a partire dal codice fiscale, '
     'leggendo ANAG_USR. Raggiungibile solo da sipo-auth, mai pubblicato.',
     '**Nuovo**, come estensione di AnagrafeBE'],
    ['I 35 front-end Java',
     'Con la libreria ProfilazioneUtente aggiornata. Tengono in sessione LOGIN_USER — '
     'invariato — e accanto il token SIPO, mai nel browser.',
     'Si configurano, non si riscrivono'],
    ['I back-end',
     'Con RestSecurity aggiornata: verificano il token SIPO con il JWKS e concedono '
     'ROLE_<profiloBe>. Leggono chi opera dal token e non più dal corpo della richiesta.',
     'Una libreria sola da aggiornare'],
    ['Portale',
     'Resta il reverse proxy davanti a SIPO, ma **non inietta più l’identità**: passa '
     'soltanto x-real-ip e x-client-sn-sipo.', 'Cambia configurazione'],
]

CLAIM = [
    ['Che cosa dice', 'Claim', 'A che serve'],
    ['Chi è', '`sub` (codice fiscale), idUtente, username, tipoUtente',
     'Identifica la persona. ⚠️ È il codice fiscale a legare l’utente di IAM a quello di '
     'SIPO (decisione D3): la bonifica di ANAG_USR.CODICE_FISCALE ne è il prerequisito.'],
    ['Dove opera', 'idOrganizzazione, idSedeMunicipio, idStrutturaConv',
     'L’ambito organizzativo, che oggi i front-end leggono da ANAG_USR per conto proprio.'],
    ['Che cosa può fare', 'ruoli (lista completa) e **profiloBe** (il primo ruolo)',
     '⚠️ `profiloBe` esiste per non toccare le @PreAuthorize dei back-end, che ragionano '
     'su un ruolo solo: nel solo StatoCivileBE sono **393**. La lista completa viaggia '
     'accanto, per le regole future.'],
    ['Da dove', 'postazione (x-client-sn-sipo) e ip',
     'È ciò che consente ad All-Anpr di dichiarare ad ANPR l’operatore e la postazione '
     'reali, invece di un valore cablato.'],
    ['Per chi è valido', '`aud` = sipo-be',
     'Il token è speso verso i back-end di SIPO e non altrove.'],
    ['Per conto di chi', 'contesto (persona giuridica, delega, assistito)',
     'Solo nel front office, dalla fase 3. Chi opera resta la persona fisica; il contesto '
     'dice per conto di chi.'],
]

SEQUENZE = [
    ['Aspetto', 'Sequenza A — la libreria diventa client OIDC',
     'Sequenza B — sipo-auth fa da proxy davanti ai front-end'],
    ['Modifiche ai front-end nella prima fase',
     'ProfilazioneUtente cambia: 35 rilasci e 35 regressioni.',
     'Nessuna. I front-end continuano a leggere gli stessi header di oggi, valorizzati '
     'però da dati verificati.'],
    ['Chiude la fiducia negli header',
     'Sì, per costruzione: gli header non si leggono più.',
     '⚠️ Solo con una NetworkPolicy che impedisca di raggiungere i front-end senza passare '
     'da sipo-auth. **Senza quella regola la sequenza non è sicura e non va adottata.**'],
    ['Traffico che attraversa sipo-auth', 'Il solo login.',
     'Tutto il traffico dei front-end: capacità, latenza e affidabilità vanno dimensionate '
     'di conseguenza.'],
    ['Credenziali di ANAG_USR nei front-end', 'Rimosse nella prima fase.',
     'Restano fino alla terza fase, quando la libreria viene aggiornata.'],
    ['Tempo per uscire dagli header del portale', 'Circa 55-75 giorni/uomo.',
     'Circa 35-50 giorni/uomo.'],
]

SOSTENIBILITA = [
    ['Questione', 'Come sta oggi', 'Che cosa serve fare'],
    ['**Il vocabolario dell’autorizzazione non coincide**',
     'I back-end decidono su **un solo ruolo** (`ROLE_<profiloBe>`); la libreria Angular '
     'decide su **una lista di abilitazioni** (`user.abilitazioni`, usata da '
     'AbilitationService, AuthorizationService e dalla guardia delle rotte). ⚠️ Il token '
     'SIPO porta `ruoli[]` e `profiloBe`, **non le abilitazioni**.',
     'Il token deve portare anche le abilitazioni, oppure il BFF deve esporre un punto di '
     'lettura del profilo corrente. ⚠️ Senza, il menu del back-office ANSC — che poggia '
     'interamente su ANSC_CFG_PAGINA_ABILITAZ — non ha su che cosa filtrare.'],
    ['Il gettone nel browser',
     'La libreria Angular conserva i dati di autenticazione in `localStorage`, sotto la '
     'chiave `auth`, e li rilegge a ogni richiesta.',
     'È esattamente ciò che il ruolo di BFF risolve: il browser tiene un cookie di '
     'sessione e il token non lo raggiunge mai. È il guadagno più immediato della '
     'soluzione, e vale di per sé.'],
    ['I micro-frontend e il BFF',
     'La shell carica i remote a runtime; il disegno del back-office prevede quattro '
     'remote sotto un’unica shell, più quello delle operazioni di postazione.',
     '**Un BFF per shell, non per micro-frontend.** Vanno verificati due dettagli che '
     'passano inosservati finché non rompono: da dove si serve il manifesto dei remote, e '
     'che il cookie di sessione resti valido per le chiamate del browser (origine e '
     'attributo SameSite coerenti).'],
    ['⚠️ Il BFF non è senza stato',
     'Tiene la sessione. Con più repliche servono sessioni appiccicate all’istanza o un '
     'archivio condiviso.',
     'Archivio di sessione condiviso, deciso insieme all’alta affidabilità del componente. '
     'È lo stesso nodo già segnalato per i front-end attuali.'],
    ['La convivenza con la sessione verso ANSC',
     'Sono **due sessioni distinte e lo restano**: quella di SIPO dura minuti e si rinnova '
     'da sola; il codice che abilita le operazioni verso ANSC dura quattro ore, lo genera '
     'l’ufficiale sulla web app nazionale e lo custodisce il concentratore.',
     'Nessuna fusione fra le due. Il documento del front-end le tiene già separate; va solo '
     'detto che la scadenza dell’una non è la scadenza dell’altra, perché l’operatore vede '
     'due contatori e deve sapere che cosa significano.'],
    ['L’intercettore che «aggiunge le credenziali»',
     '⚠️ Nella libreria condivisa l’intercettore di autenticazione **non aggiunge alcuna '
     'intestazione**: passa la richiesta inalterata.',
     'È il punto in cui il token andrà aggiunto quando le applicazioni Angular parleranno '
     'con i back-end di SIPO. Con il BFF quel compito si sposta sul server, e '
     'l’intercettore resta vuoto per scelta e non per dimenticanza.'],
    ['Il profilo nella console del browser',
     '⚠️ Il servizio di autorizzazione scrive l’intero oggetto di autenticazione — token '
     'compreso — nella console del browser.',
     'Da togliere prima del primo rilascio. È una riga di codice, e non dipende da nessuna '
     'delle decisioni aperte.'],
    ['msAuth',
     'Esiste nella libreria Angular come guardia di rotta verso '
     '`/msAuth/api/v1/autenticazione/loginIAM`. ⚠️ Ma **non è richiamata da nessuna parte**, '
     'porta scritto dal suo autore che mancano il codice di ambito e quello '
     'dell’applicazione, e **nel manuale di IAM non compare**: non è quindi un servizio '
     'dell’IAM.',
     'L’accertamento di PI-17 resta, ma cambia di natura: non «esiste?» bensì «chi lo '
     'possiede, che cosa copre e con quale impegno di esercizio». Se la risposta fosse '
     'adeguata, sipo-auth si riduce a un adattatore verso di esso e il resto del piano non '
     'cambia.'],
]

CAMBIA = [
    ['Aspetto', 'Oggi', 'A regime'],
    ['Chi autentica', 'Il portale, con intestazioni HTTP', 'IAM, per il tramite di sipo-auth'],
    ['Prova dell’identità', 'Intestazioni non firmate, di cui ci si fida',
     'Un gettone firmato, che si verifica'],
    ['Lettura dei profili', 'Ogni front-end per conto proprio su ANAG_USR',
     'sipo-profili, una volta sola'],
    ['Credenziali del database nei front-end', 'Sì, nel pacchetto applicativo', 'No'],
    ['Identità verso i back-end', 'Un’utenza tecnica per ruolo',
     'Il token dell’utente che sta operando'],
    ['Chi opera, per il back-end', 'Dichiarato nel corpo della richiesta, quindi '
     'falsificabile', 'Preso dal token'],
    ['Emittenti di gettoni', '44 back-end, con una chiave condivisa',
     'Solo sipo-auth, con firma asimmetrica'],
    ['Client registrati presso IAM', '—', 'Uno'],
    ['Tracciamento degli accessi', 'Non centralizzato', 'Un registro unico'],
    ['Per chi sviluppa i front-end', 'LOGIN_USER in sessione', 'LOGIN_USER invariato'],
]

PREREQ = [
    ['Prerequisito', 'Perché', 'A chi compete'],
    ['La bonifica di ANAG_USR.CODICE_FISCALE',
     'È la chiave che lega l’utente di IAM a quello di SIPO. Senza, il raccordo non si fa.',
     'Base dati / Referenti SIPO'],
    ['La registrazione del client presso IAM',
     'Una sola, per sipo-auth: client, redirect e scope si concordano con il Presidio IAM.',
     'Presidio IAM / Referenti SIPO'],
    ['La piattaforma di sipo-auth e il suo Manuale Operativo',
     'È un componente nuovo in esercizio: va censito con il modulo del CED, come ogni altro.',
     'Architettura / CED'],
    ['La clausola di chiusura sui back-end',
     '⚠️ **Non dipende da IAM e va fatta comunque.** Finché i servizi rispondono senza '
     'gettone, il resto conta poco.', 'Sviluppo'],
    ['La raggiungibilità diretta dei front-end',
     'Decide quale delle due sequenze convenga, ed è il presupposto di sicurezza della '
     'sequenza B.', 'Sistemi / Rete'],
]

NUOVI_PI = [
    ('PI-20', 'Se il token SIPO debba portare anche le abilitazioni, oltre ai ruoli, '
              'oppure se il profilo corrente si legga da un punto dedicato. ⚠️ I back-end '
              'decidono su un ruolo solo, le applicazioni Angular su una lista di '
              'abilitazioni: senza una delle due vie il menu del back-office non è '
              'filtrabile.', 'Architettura / Referenti SIPO'),
    ('PI-21', 'Dove risieda la sessione del componente di autenticazione quando è in più '
              'repliche, e come si dimensiona il suo esercizio nella sequenza che gli fa '
              'attraversare tutto il traffico dei front-end.', 'Architettura / Sistemi'),
    ('PI-22', 'Chi possiede il servizio di autenticazione usato dalle applicazioni Angular, '
              'che cosa copre e con quale impegno di esercizio. ⚠️ Esiste come codice '
              'client nella libreria condivisa, ma non è richiamato e non compare nel '
              'manuale di IAM: non è un servizio dell’IAM.', 'Dipartimento / Presidio'),
    ('PI-23', 'Come si ottengono in modalità OIDC gli attributi di persona giuridica e di '
              'delega. ⚠️ Il manuale li documenta come intestazioni HTTP e dichiara che i '
              'claim corrispondono alla sola tabella degli attributi della persona '
              'autenticata; «assistito» non vi compare. È il presupposto della fase 3.',
     'Presidio IAM'),
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)

    def commenti(p):
        return int(subprocess.run(
            ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                           "grep -o '<w:comment ' | wc -l" % repr(p)],
            capture_output=True, text=True).stdout.strip() or 0)
    prima = commenti(DST)

    d = docx.Document(DST)
    fatti = []
    MOD = d.tables[16]   # «Componente | Intervento | Note»: modello di bordi

    # ---------------------------------------------------------- 1. congruenza
    D.sostituisci(d, 'vegono', 'vengono', attese=1, etichetta='refuso «vegono»', fatti=fatti)
    D.sostituisci(
        d, 'ed è dipendenza di trenta moduli di back-end',
        'ed è dichiarato come dipendenza in cinquantanove punti, che corrispondono a '
        'quarantuno moduli distinti di back-end',
        attese=1, etichetta='conteggio reale dei moduli che dipendono dal client ANPR',
        fatti=fatti)
    D.sostituisci(
        d, 'resta nel percorso di classe di trenta moduli',
        'resta nel percorso di classe di quarantuno moduli',
        attese=1, etichetta='stesso conteggio nel registro dei rilievi', fatti=fatti)

    t14 = d.tables[14]
    for r in t14.rows:
        et = r.cells[0].text.strip()
        if et.startswith('Registrazioni presso IAM'):
            D.riscrivi_cella(r.cells[2], 'un client con 35 redirect, oppure 35 client')
            D.riscrivi_cella(r.cells[5], 'da accertare')
        elif et.startswith('Dove vive il segreto'):
            D.riscrivi_cella(r.cells[2], 'in ciascuno dei 35 front-end')
            D.riscrivi_cella(r.cells[5], 'da accertare')
        elif et.startswith('Serve anche ai front-end'):
            D.riscrivi_cella(r.cells[5], 'da accertare')
    fatti.append('completate le celle vuote di S1 e tolte le affermazioni non verificate su S4')

    ancora_r = D.h(d, 3, 'La raccomandazione')
    D.para(d, ancora_r._p.getnext(),
           '⚠️ **Questa raccomandazione è superata dal capitolo «Scelte effettuate».** Vi si '
           'proponeva di cominciare dalla soluzione S1 e di tenere S3 come approdo; la '
           'scelta effettivamente compiuta costruisce S3 da subito, per una ragione di '
           'codice che allora non era quantificata e che il capitolo finale espone. Il '
           'confronto fra le soluzioni resta valido e si legge come la motivazione della '
           'scelta, non come la scelta.')
    fatti.append('la raccomandazione della v0.3 è dichiarata superata dal capitolo 6')

    # riferimenti nuovi
    tr = D.trova_tabella(d, '#', 'Riferimento')
    D.sostituisci(d, 'ANALISI_Front-End-Angular_v0.4.docx',
                  'ANALISI_Front-End-Angular_v0.6.docx', attese=1,
                  etichetta='[F8] portato alla versione corrente', fatti=fatti)
    for sigla, rif, nat in (
        ('[F9]', 'Processo_Autenticazione_sipo-auth.txt — la soluzione scelta, descritta '
                 'dal referente tecnico: componenti, flussi, periodo di transizione',
         'Scelta del committente'),
        ('[F10]', 'Analisi_Incrociata_IAM_Profilazione.txt — confronto fra questo documento '
                  'e le analisi del fornitore, con la soluzione proposta e le stime',
         'Analisi del fornitore'),
        ('[F11]', '«Manuale Operativo Applicazione RDE_COEC», modello DTD 2026.2 — il modulo '
                  'con cui un applicativo entra in esercizio al CED. ⚠️ Non descrive '
                  'un’integrazione con IAM: vi rinvia alle linee guida della Direzione '
                  'Servizi Digitali', 'Modulistica dell’ente'),
    ):
        D.clona_riga(tr, (sigla, rif, nat))
    fatti.append('[F9], [F10] e [F11] aggiunti ai Riferimenti')

    # ---------------------------------------------------------- 2. il capitolo 6
    cap = next(p for p in d.paragraphs
               if p.style.name == 'Heading 1' and p.text.strip() == 'Scelte effettuate')
    coda = cap._p.getnext()

    def par(t, stile='Normal'):
        return (D.para(d, coda, t, stile=stile) if coda is not None
                else D.para(d, cap._p.getnext() or cap._p, t, stile=stile))

    def tab(righe, larghezze):
        return D.tabella(d, coda, righe, modello=MOD, larghezze=larghezze)

    def didascalia(t):
        p = par(t)
        for r in p.runs:
            r.italic = True
            r.font.size = docx.shared.Pt(9)

    par('La scelta è stata compiuta dal referente tecnico del progetto ed è descritta in '
        '[F9]. Questo capitolo la recepisce in termini operativi: che cosa si costruisce, '
        'come si arriva allo stato finale e — poiché il front-end di destinazione è '
        'Angular e il back-end è Java — che cosa va verificato perché regga su '
        'quell’architettura.')

    par('La soluzione: un solo punto di autenticazione', 'Heading 2')
    par('**Si costruisce un componente nuovo, `sipo-auth`, che diventa l’unico punto di '
        'autenticazione di SIPO.** Parla lui con IAM, recupera il profilo dell’utente ed '
        'emette un gettone proprio — il **token SIPO** — che vale dentro il perimetro di '
        'SIPO. I trentacinque front-end non conoscono IAM: conoscono sipo-auth. I back-end '
        'non conoscono IAM: verificano la firma di sipo-auth.')
    par('Il token SIPO è firmato con chiave asimmetrica, dura dieci-quindici minuti e si '
        'rinnova da solo. ⚠️ **Il gettone di IAM non esce mai da sipo-auth**: è il confine '
        'che tiene separato ciò che l’ente governa da ciò che governiamo noi, e che '
        'consente di cambiare il modo di autenticarsi senza toccare nulla a valle.')
    D.immagine(d, coda, os.path.join(IMG, 'iam_sipoauth.png'), 6.3,
               'Figura 6 — L’architettura scelta. I numeri sono i passi del login; le due '
               'righe in fondo sono i confini che il disegno non deve mai violare.')
    par('Chi partecipa, e che cosa è davvero nuovo.')
    tab(PARTECIPANTI, [1.5, 3.3, 1.5])
    par('Che cosa contiene il token SIPO.')
    tab(CLAIM, [1.3, 2.0, 3.0])

    par('Perché non si comincia dalla libreria', 'Heading 2')
    par('Il capitolo precedente raccomandava di cominciare da S1 — l’OIDC dentro la '
        'libreria condivisa — tenendo il componente centrale come approdo. **La scelta va '
        'nella direzione opposta, e la ragione è un dato di codice che non era stato '
        'misurato.**')
    par('Nei front-end ci sono **4.781 chiamate** al metodo che restituisce il profilo di '
        'back-end, e altrettante chiamate ai servizi che ne dipendono. Il conteggio è '
        'stato verificato. ⚠️ **Ne discende che la fase in cui l’identità della persona '
        'arriva ai back-end non si può fare cambiando i punti di chiamata**: il '
        'cambiamento deve avvenire dentro il componente che li serve, a parità di firma. E '
        'quel componente può sostituire il gettone solo se un gettone dell’utente esiste '
        'già nella sessione — cioè solo se l’emittente c’è dal primo accesso.')
    par('Con S1 l’emittente non esisterebbe: il gettone di IAM non è spendibile verso i '
        'back-end, e la fase successiva richiederebbe comunque di costruirlo. Si '
        'pagherebbero inoltre trentacinque registrazioni presso IAM, trentacinque copie '
        'dello stesso segreto e trentacinque regole di uscita verso l’esterno — lavoro che '
        'si butta quando arriva il componente centrale.')
    par('⚠️ **Il costo della scelta è reale e va dichiarato**: si introduce un componente '
        'sul percorso del login, e il login è il punto in cui un disservizio ferma tutti. '
        'Vanno quindi messe in conto almeno due repliche, le chiavi e la sessione fuori '
        'dalla memoria locale, e una sonda di prontezza che **non dipenda dalla '
        'raggiungibilità di IAM** — altrimenti un disservizio esterno fa riavviare un '
        'componente sano.')

    par('Il login di un operatore', 'Heading 2')
    par('L’operatore apre una maschera di SIPO e non ha una sessione. Il front-end lo manda '
        'a sipo-auth, conservando lato server la pagina che aveva chiesto. sipo-auth non '
        'ha una sessione per lui e lo manda a IAM, che lo autentica con le credenziali, '
        'SPID o CIE — la scelta è di IAM, non nostra. Al ritorno sipo-auth scambia il '
        'codice con il gettone di IAM, **ne verifica la firma in locale**, ne estrae il '
        'codice fiscale e chiede a sipo-profili chi sia quella persona in SIPO.')
    par('Se l’utente non è censito o è disabilitato l’accesso è negato **con un messaggio '
        'esplicito**: è un miglioramento concreto rispetto a oggi, dove lo stesso caso si '
        'presenta all’operatore come un generico «utente senza ruoli» e manda il supporto '
        'a cercare nel posto sbagliato.')
    par('Altrimenti sipo-auth registra l’accesso, emette il token SIPO e riporta l’operatore '
        'al front-end, che costruisce l’oggetto utente **come oggi** e lo mette in sessione '
        'sotto lo stesso nome di oggi. Accanto vi tiene il token, **solo lato server**. '
        'L’identificativo di sessione viene rigenerato, e l’operatore arriva alla pagina '
        'che aveva chiesto all’inizio.')
    par('⚠️ **Da qui discende una proprietà che oggi non c’è**: se apre un altro front-end '
        'di SIPO non si autentica di nuovo, perché sipo-auth ha già la sua sessione. È il '
        'passaggio unico fra le applicazioni, e non costa nulla in più.')

    par('Il login di un cittadino e il contesto operativo', 'Heading 2')
    par('Il percorso è lo stesso, con il client e gli ambiti del front office. Due '
        'differenze. Il cittadino non censito riceve il ruolo previsto per il pubblico, e '
        '**la decisione si prende sul tipo di utente dichiarato da IAM** — un attributo che '
        'il manuale prevede e che vale «cittadino» o «dipendente» — invece che sul formato '
        'del codice fiscale, come oggi. ⚠️ Non è un dettaglio: il controllo attuale '
        'restituisce vero quando il valore è assente, e un’intestazione mancante produce un '
        'utente vuoto anziché un errore. La seconda differenza è che se durante la sessione '
        'cambia il codice fiscale autenticato la sessione viene invalidata.')
    par('**Operare per conto di altri.** Dalla terza fase il cittadino può agire come '
        'rappresentante di una persona giuridica, come delegato o per un assistito. Lo '
        'sceglie nel front-end; sipo-auth lo manda alla pagina personale di IAM, dove la '
        'selezione avviene; IAM richiama la stessa callback e sipo-auth ottiene un nuovo '
        'gettone con gli attributi del soggetto rappresentato. sipo-auth ne controlla la '
        'validità temporale e **verifica che il servizio di SIPO sia fra quelli per cui la '
        'delega vale** — è una condizione dichiarata dall’ente, non una cautela nostra — ed '
        'emette un nuovo token SIPO con il contesto operativo.')
    par('Il cambio viene registrato. Da quel momento i back-end imputano gli atti al '
        'soggetto rappresentato e tracciano chi ha operato: **chi opera resta la persona '
        'fisica, per conto di chi è il soggetto scelto.** È la distinzione che rende '
        'ricostruibile a posteriori un atto compiuto in rappresentanza.')

    par('Le chiamate verso i back-end', 'Heading 2')
    par('**Dal front-end al back-end.** Il codice applicativo chiama il componente di '
        'accesso ai servizi come oggi, con la stessa firma e lo stesso parametro: **nessuna '
        'delle chiamate esistenti cambia.** È dentro quel componente che il gettone '
        'dell’utenza tecnica viene sostituito dal token SIPO trovato nella sessione '
        'corrente, rinnovandolo prima se sta per scadere. Il back-end verifica firma, '
        'emittente, scadenza e destinatario, concede l’autorità corrispondente al profilo e '
        '**legge chi opera dal token**, non dal corpo della richiesta.')
    par('⚠️ **Il passaggio su quest’ultimo punto è graduale e va misurato prima di essere '
        'imposto**: se il corpo dichiara un utente diverso da quello del token, per un '
        'periodo la cosa si registra soltanto; solo dopo si rifiuta. È il modo di conoscere '
        'l’impatto prima di produrlo.')
    par('**Da back-end a back-end** lo stesso token viene inoltrato, così il servizio che '
        'dialoga con ANPR può dichiarare l’operatore e la postazione reali. **I processi '
        'senza utente** — i trattamenti pianificati — non hanno una richiesta in corso: '
        'usano un’utenza tecnica dedicata al trattamento, non il codice fiscale di una '
        'persona, con il gettone tenuto in memoria.')

    par('Scadenza, uscita, indisponibilità', 'Heading 2')
    D.voce(d, coda, 'Token scaduto durante il lavoro.',
           'Si rinnova senza che l’operatore se ne accorga.')
    D.voce(d, coda, 'Sessione del front-end scaduta.',
           'Si rifà il giro verso sipo-auth; se la sua sessione è ancora valida il rientro '
           'è silenzioso.')
    D.voce(d, coda, 'Uscita.',
           'Il front-end chiude la propria sessione e quella di sipo-auth. ⚠️ **Non si '
           'propaga l’uscita a IAM**: il manuale dell’ente sconsiglia espressamente di '
           'invocare quella funzione, perché terminerebbe la sessione dell’utente anche '
           'sugli altri sistemi su cui potrebbe star lavorando.')
    D.voce(d, coda, 'IAM non raggiungibile.',
           'Chi ha già una sessione continua a lavorare fino alla scadenza; i nuovi accessi '
           'falliscono con un messaggio chiaro. ⚠️ sipo-auth resta dichiarato pronto: la sua '
           'prontezza non dipende da IAM.')
    D.voce(d, coda, 'Intestazioni contraffatte inviate dal browser.',
           'Vengono scartate e non autenticano nessuno. È il difetto che la soluzione '
           'chiude alla radice.')

    par('Come ci si arriva: due sequenze', 'Heading 2')
    par('Lo stato finale è lo stesso; cambia l’ordine in cui ci si arriva, e la scelta '
        'dipende da un accertamento: **se oggi i front-end siano raggiungibili senza '
        'passare dal portale.**')
    tab(SEQUENZE, [1.3, 2.5, 2.5])
    par('**Il criterio è questo.** Se i front-end sono raggiungibili direttamente, la '
        'fiducia nelle intestazioni è sfruttabile davvero e conviene la sequenza B, che la '
        'chiude prima. Se invece la rete già impedisce di scavalcare il portale, la regola '
        'aggiuntiva aggiunge poco e conviene la sequenza A, che toglie prima le credenziali '
        'del database dai front-end e non fa attraversare a sipo-auth tutto il traffico.')
    par('In entrambe, fino alla dismissione, i back-end continuano ad accettare anche il '
        'gettone tecnico di oggi, il token dell’utente si accende dove serve e **ogni '
        'passaggio si può annullare con un cambio di configurazione, per ambiente**. È la '
        'proprietà che rende il percorso percorribile a ritroso, e va conservata.')

    par('La sostenibilità sull’architettura di destinazione', 'Heading 2')
    par('La soluzione è stata concepita a partire dal mondo Java, che è la parte più grande '
        'del sistema. **Regge anche sul front-end Angular**, e la variante del Backend For '
        'Frontend già prevista ne è la ragione: le applicazioni a pagina singola non possono '
        'usare le intestazioni, e tenere il gettone nel browser è ciò che il BFF evita. Ci '
        'sono però sette punti da chiudere perché «regge» diventi «funziona», e il primo è '
        'un disallineamento vero.')
    tab(SOSTENIBILITA, [1.5, 2.6, 2.7])
    par('⚠️ **Il primo punto della tabella merita di essere letto due volte**, perché è '
        'l’unico che possa fermare il back-office nuovo. I due mondi autorizzano su '
        'vocabolari diversi, e nessuno dei due è sbagliato: il Java decide su un ruolo solo '
        'perché così sono scritte le quasi quattrocento regole esistenti, l’Angular decide '
        'su una lista di abilitazioni perché una pagina ha un’abilitazione per accedervi e '
        'una per ciascuna azione. **Il token deve parlare entrambe le lingue**, altrimenti '
        'la shell non ha su che cosa costruire il menu — e il menu, nel disegno del '
        'back-office, è un dato, non codice.')

    par('Che cosa cambia rispetto a oggi', 'Heading 2')
    tab(CAMBIA, [1.7, 2.4, 2.7])

    par('Prerequisiti e adempimenti', 'Heading 2')
    par('La soluzione non parte finché cinque cose non sono fatte o decise. Nessuna di esse '
        'è tecnica in senso stretto, e per questo si perdono di vista.')
    tab(PREREQ, [1.9, 2.9, 2.0])
    par('⚠️ **L’ultima riga della tabella non è un prerequisito di IAM ed è la più urgente.** '
        'Oggi i servizi di back-end non hanno una clausola che chiuda tutto ciò che non è '
        'esplicitamente consentito: finché resta così, un accesso robusto davanti a servizi '
        'aperti non migliora la sicurezza complessiva. Si fa in giorni e non dipende da '
        'nessuna delle decisioni ancora aperte.')
    fatti.append('capitolo «Scelte effettuate» scritto: 10 sezioni, 6 tabelle, 1 figura')

    # ---------------------------------------------------------- 3. punti aperti
    to = D.trova_tabella(d, '#', 'Questione')
    for r in to.rows[1:]:
        if r.cells[0].text.strip() == 'PI-05':
            D.riscrivi_cella(
                r.cells[1], 'Chiuso. Se l’IAM offra un servizio che restituisca i profili a '
                            'partire dal codice fiscale. ⚠️ Verificato sul manuale: non '
                            'esiste. L’unica informazione autorizzativa che l’IAM fornisce '
                            'sono i gruppi, e solo in modalità header: in OIDC non c’è alcun '
                            'claim di ruolo o gruppo. I profili restano di SIPO.')
        elif r.cells[0].text.strip() == 'PI-17':
            D.riscrivi_cella(
                r.cells[1], 'Se il servizio di autenticazione usato dalle applicazioni '
                            'Angular copra anche le utenze dei dipendenti, con quale '
                            'granularità di profilo e se il gettone che emette sia '
                            'verificabile dai back-end di SIPO. ⚠️ Esiste come codice client '
                            'nella libreria condivisa, ma non è richiamato da alcuna '
                            'applicazione e non compare nel manuale dell’IAM: vedi PI-22.')
    for sigla, q, chi in NUOVI_PI:
        D.clona_riga(to, (sigla, q, chi))
    fatti.append('PI-05 chiuso, PI-17 riformulato, PI-20…PI-23 aperti')

    # ---------------------------------------------------------- 4. testata e storia
    for tab_ in d.tables:
        if tab_.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tab_.rows:
                v = {'Versione': '0.4',
                     'Documento': 'ANALISI_Identita-Profilazione-IAM_v0.4'}.get(
                        r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '06/10/2026', '0.4',
             'Parte I · Parte II (confronto, raccomandazione) · Scelte effettuate (nuovo) · '
             'Riferimenti · Punti aperti',
             'Aggiunto il capitolo «Scelte effettuate», che recepisce in termini operativi '
             'la soluzione scelta dal referente tecnico: un unico punto di autenticazione '
             'di SIPO, che parla con IAM ed emette un gettone proprio. Comprende un '
             'sottocapitolo sulla sostenibilità rispetto all’architettura di destinazione, '
             'Angular davanti e Java dietro. Recepita la documentazione nuova messa a '
             'disposizione dall’ente: ne discendono la chiusura di un punto aperto — l’IAM '
             'non offre alcun servizio di profilazione per codice fiscale — e quattro punti '
             'nuovi, fra cui il disallineamento fra il vocabolario di autorizzazione dei '
             'back-end e quello delle applicazioni Angular. Corretti il conteggio dei moduli '
             'che dipendono dal client ANPR, le celle incomplete del confronto fra le '
             'soluzioni e un refuso; la raccomandazione della versione precedente è '
             'dichiarata superata dal nuovo capitolo.')
    fatti.append('testata e storia aggiornate')

    # ---------------------------------------------------------- 5. grassetti
    def grassetti(p):
        if '**' not in p.text or D.ha_commenti(p._p):
            return 0
        pezzi = D.segmenta('', p.text)
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        for testo, gr in pezzi:
            run = p.add_run(testo)
            run.bold = gr
        return 1
    n = sum(grassetti(p) for p in d.paragraphs)
    for tb in d.tables:
        for r in tb.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    n += grassetti(p)
    fatti.append('%d paragrafi con grassetto applicato' % n)

    d.save(DST)
    dopo = commenti(DST)
    if dopo != prima:
        raise SystemExit('COMMENTI PERSI: erano %d, sono %d' % (prima, dopo))

    print('\n'.join(' · ' + f for f in fatti))
    print('capitoli/tabelle/immagini:', D.riepilogo(DST))
    print('scritto:', os.path.relpath(DST, BASE))


if __name__ == '__main__':
    main()
