# -*- coding: utf-8 -*-
"""ANALISI_Front-End-Angular v0.2 -> v0.3 (22/09/2026).

Si MODIFICA il file reale (la v0.2 porta un commento dell'utente sul paragrafo
dell'autenticazione): nessuna rigenerazione dal generatore.

  1. via ogni riferimento a Keycloak (nessuna conferma nelle fonti: nella libreria il
     pacchetto è dichiarato ma non importato da alcun sorgente; l'unico meccanismo presente
     è la guardia che reindirizza al servizio di accesso /msAuth/.../loginIAM);
  2. la libreria è lo standard per TUTTE le nuove applicazioni di front-end [F7];
  3. le nuove applicazioni sono micro-frontend e la shell condivide la libreria con tutti
     i micro-frontend che richiama [F7];
  4. il caricamento differito: oggi non usato [F7], perché serve, perché è la buona pratica.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/fe_v0_3.py
"""
import os
import shutil
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'ANALISI_Front-End-Angular_v0.2.docx')
DST = os.path.join(BASE, 'ANALISI_Front-End-Angular_v0.3.docx')
IMG = os.path.join(BASE, 'strumenti', 'img')

if os.path.exists(DST):
    raise SystemExit('la v0.3 esiste già: non si sovrascrive')
shutil.copy(SRC, DST)
doc = docx.Document(DST)
fatti = []


def par_che_inizia(inizio):
    trovati = [p for p in doc.paragraphs if p.text.strip().startswith(inizio)]
    if len(trovati) != 1:
        raise SystemExit(f'attesa 1 occorrenza di «{inizio[:50]}», trovate {len(trovati)}')
    return trovati[0]


def riscrivi(inizio, nuovo):
    D.testo_di(par_che_inizia(inizio), nuovo)
    fatti.append('riscritto: ' + inizio[:50])


def riga_con(t, prima_cella):
    for r in t.rows:
        if r.cells[0].text.strip() == prima_cella:
            return r
    raise SystemExit('riga non trovata: ' + prima_cella)


def dopo(p):
    """L'elemento che segue il paragrafo: il punto d'innesto per D.para & co."""
    return p._p.getnext()


# ───────────────────────────────────────────── scheda, storia, riferimenti, glossario
scheda = D.trova_tabella(doc, 'area organizzativa')
D.riscrivi_cella(riga_con(scheda, 'Data consegna').cells[1], '22/09/2026')
D.riscrivi_cella(riga_con(scheda, 'Versione').cells[1], '0.3')

storia = D.trova_tabella(doc, 'versione', 'sintesi dei cambiamenti')
vuota = storia.rows[-1]
valori = ('22/09/2026', '0.3',
          'Contesto · Stakeholder · Tecnologie · Architettura · Design system · Requisiti · '
          'Classi di rischio · Strategie di test · Punti aperti',
          'Rimossa l’indicazione del prodotto di gestione delle identità, che nessuna fonte '
          'conferma: il meccanismo di '
          'autenticazione è rinviato all’impianto di sicurezza e profilazione (OP-FE-11). '
          'Recepita la conferma che la libreria è lo standard per tutte le nuove applicazioni '
          'di front-end, concepite come micro-frontend con la shell che condivide la libreria '
          'con tutti i micro-frontend richiamati. Aggiunta la sezione sul caricamento '
          'differito, oggi non adottato, con le ragioni per cui è necessario, il modo di '
          'adottarlo e il relativo requisito, rischio e punto aperto (OP-FE-12).')
if any(c.text.strip() for c in vuota.cells):
    D.storia(doc, *valori)
else:
    for c, v in zip(vuota.cells, valori):
        D.riscrivi_cella(c, v)

rif = D.trova_tabella(doc, 'id', 'riferimento', 'contenuto')
D.clona_riga(rif, ('[F7]', 'Colloquio con uno sviluppatore della libreria condivisa — '
                   '22/09/2026',
                   'Conferma che i componenti della libreria possono e devono essere usati in '
                   'tutte le nuove applicazioni di front-end, che queste sono concepite come '
                   'micro-frontend con una shell che condivide la libreria, e che oggi le '
                   'applicazioni non adottano il caricamento differito.'))

glo = D.trova_tabella(doc, 'termine', 'significato')
D.clona_riga(glo, ('Caricamento differito (lazy loading)',
                   'Tecnica con cui il codice di una rotta o di un micro-frontend viene '
                   'scaricato e inizializzato soltanto quando l’operatore vi naviga, e non '
                   'all’avvio dell’applicazione.'))
D.clona_riga(glo, ('Precaricamento',
                   'Caricamento differito anticipato di proposito: il codice di una rotta che '
                   'l’operatore quasi certamente aprirà viene scaricato in background, prima che '
                   'la apra.'))

# ───────────────────────────────────────────── contesto
riscrivi('La proposta tecnica [F1] è stata redatta per un altro progetto',
         'La proposta tecnica [F1] è stata redatta per un altro progetto — la firma dei '
         'certificati di postazione — e il presente documento la usa per il metodo e per i '
         'punti critici che solleva, non per il contenuto. I punti critici sono però gli stessi '
         'che si porrebbero qui, ed è utile notare che tre dei sei hanno già risposta nella '
         'libreria: il modello dei permessi, la molteplicità degli ambienti e la conformità a un '
         'design system. Un quarto, l’integrazione con l’autenticazione esistente, trova nella '
         'libreria il punto d’innesto ma non la risposta: la stessa proposta chiede di definirne '
         'protocollo, token e gestione della sessione, e il presente documento lo rinvia '
         'all’impianto di sicurezza e profilazione. La proposta si chiedeva anche se usare '
         'Bootstrap o Bootstrap Italia e se esistesse un design system formalizzato: esiste, ed '
         'è Bootstrap Italia con il tema di Roma Capitale.')

# ───────────────────────────────────────────── stakeholder e accesso
riscrivi('Tutte le figure sopra sono utenti interni',
         'Tutte le figure sopra sono utenti interni, autenticati dal servizio di accesso '
         'dell’ente. La visibilità di rotte, voci di menu e azioni discende dalle abilitazioni '
         'presenti nel profilo: la libreria offre già il servizio che filtra gli elementi in base '
         'a esse, e le guardie che proteggono le rotte.')
riscrivi('Due autenticazioni, da non confondere.',
         'Due autenticazioni, da non confondere. L’accesso a SIPO è quello del servizio di '
         'accesso dell’ente. La sessione verso ANSC è un’altra cosa: nasce da un codice che '
         'l’ufficiale genera sulla web app di ANSC con smart card o identità digitale, dura '
         'quattro ore, e serve soltanto per le operazioni che toccano la piattaforma nazionale. '
         'Un operatore autenticato a SIPO può non avere alcuna sessione ANSC, e questo è normale.')

# ───────────────────────────────────────────── tecnologie e servizi
tec = D.trova_tabella(doc, 'componente', 'proposta tecnica', 'baseline adottata')
r = riga_con(tec, 'Autenticazione')
D.riscrivi_cella(r.cells[2], 'guardia che reindirizza al servizio di accesso dell’ente')
D.riscrivi_cella(r.cells[3], '[DA VERIFICARE] — da definire nell’impianto di sicurezza e '
                             'profilazione (OP-FE-11)')

srv = D.trova_tabella(doc, 'servizio esposto', 'a che cosa serve')
r = riga_con(srv, 'AuthenticationService · AuthenticationGuard · AuthenticationIAMGuard')
D.riscrivi_cella(r.cells[1], 'Dati di sessione dell’operatore, conservati nel browser sotto la '
                             'chiave «auth» e comprensivi di struttura, ufficio e tributo; guardia '
                             'che, in assenza del token, reindirizza al servizio di accesso '
                             'dell’ente.')
D.riscrivi_cella(r.cells[2], 'Il punto 3.1 della Proposta Tecnica: non si introduce un secondo '
                             'meccanismo di autenticazione. Protocollo, token e durata della '
                             'sessione restano da definire (OP-FE-11).')

# ───────────────────────────────────────────── architettura: micro-frontend e shell
riscrivi('L’applicazione non è un blocco unico.',
         'Le nuove applicazioni di front-end che usano la libreria sono concepite come '
         'micro-frontend [F7]: l’applicazione non è un blocco unico. Una shell, detta anche host, '
         'governa le rotte di primo livello, il layout comune e il caricamento della '
         'configurazione; dentro di essa vengono caricati a runtime i micro-frontend, ciascuno '
         'con il proprio ciclo di rilascio. La libreria condivisa è essa stessa un '
         'micro-frontend, ma di natura diversa: non porta schermate, porta ciò che tutti usano — '
         'il design system, i componenti, il client HTTP con i suoi intercettori, i servizi di '
         'sessione, di autorizzazione e di configurazione.')

D.sostituisci_immagine(doc, 'L’architettura del front-end.',
                       os.path.join(IMG, 'fe_architettura.png'))
fatti.append('figura dell’architettura rigenerata (senza Keycloak, con la shell che condivide '
             'la libreria)')

ancora = D.h(doc, 2, 'La federazione e il vincolo di versione')._p
D.para(doc, ancora, 'La shell e la condivisione della libreria', stile='Heading 2')
for t in [
    'La shell è l’applicazione che l’operatore apre. Carica la libreria condivisa una sola volta '
    'e la mette a disposizione di tutti i micro-frontend che richiama [F7]: nessun '
    'micro-frontend porta con sé una propria copia della libreria, né delle dipendenze che essa '
    'dichiara condivise.',
    'In pratica questo significa che nella pagina c’è un solo esemplare di ciascuna delle cose '
    'che la libreria fornisce:',
]:
    D.para(doc, ancora, t)
for testa, corpo in [
    ('Un solo design system. ', 'Tema, font e icone sono caricati una volta; un micro-frontend '
     'non può presentarsi con un aspetto diverso da quello della shell che lo ospita.'),
    ('Un solo client HTTP. ', 'Tutte le chiamate, di qualunque micro-frontend, attraversano gli '
     'stessi intercettori: le credenziali, il trattamento degli errori e l’indicatore di attesa '
     'sono uniformi per costruzione.'),
    ('Un solo stato di sessione e di abilitazioni. ', 'I servizi della libreria sono dichiarati '
     'al livello radice dell’applicazione: il micro-frontend che legge i dati di sessione legge '
     'quelli che ha scritto la shell, e le abilitazioni valgono allo stesso modo ovunque.'),
    ('Un solo canale fra micro-frontend. ', 'Il bus di eventi della libreria consente a due '
     'micro-frontend di comunicare senza conoscersi.'),
]:
    D.voce(doc, ancora, testa, corpo)
D.para(doc, ancora, 'La ripartizione dei compiti fra shell, micro-frontend e libreria è la '
                    'seguente.')
modello = D.trova_tabella(doc, 'servizio esposto', 'a che cosa serve')
D.tabella(doc, ancora, [
    ('Elemento', 'Chi lo possiede', 'Nota'),
    ('Rotte di primo livello e menu', 'Shell', 'La shell conosce tutte le rotte; il codice che '
     'le realizza sta nei micro-frontend e si carica alla navigazione.'),
    ('Layout comune — intestazione, piè di pagina, barra di navigazione', 'Shell',
     'Composto con i componenti della libreria, non ridisegnato.'),
    ('Configurazione di ambiente (config.json)', 'Shell', 'Letta a runtime con il servizio di '
     'configurazione della libreria; contiene anche gli indirizzi dei micro-frontend.'),
    ('Accesso e guardie di autenticazione', 'Shell', 'Con i servizi della libreria; il '
     'meccanismo di identità è da definire (OP-FE-11).'),
    ('Schermate e rotte interne di un’area funzionale', 'Micro-frontend', 'Ciascuno con il '
     'proprio ciclo di rilascio.'),
    ('Componenti, tema, client HTTP, servizi trasversali', 'Libreria', 'Caricata una volta dalla '
     'shell e usata da tutti.'),
], modello)
D.para(doc, ancora, '⚠️ Il rovescio della condivisione va detto: ciò che sta nella libreria è '
                    'in comune, e un difetto in un suo servizio si manifesta in tutti i '
                    'micro-frontend presenti nella pagina. È una ragione in più per i test di cui '
                    'al capitolo «Strategie di test».')
fatti.append('nuova sezione «La shell e la condivisione della libreria»')

# ───────────────────────────────────────────── il caricamento differito
ancora = D.h(doc, 2, 'Autenticazione e sessione')._p
D.para(doc, ancora, 'Il caricamento differito dei micro-frontend', stile='Heading 2')
D.para(doc, ancora, 'Lo stato attuale', stile='Heading 3')
for t in [
    'È stato appurato che oggi le applicazioni non usano il caricamento differito [F7]: il '
    'codice dei micro-frontend e delle loro schermate è scaricato e inizializzato all’avvio, '
    'prima che l’operatore abbia scelto che cosa fare. È una situazione da cambiare, e la '
    'presente sezione spiega perché.',
    'Due precisazioni evitano di confondere lo stato attuale con ciò che gli somiglia. La prima: '
    'il punto di ingresso della libreria importa il proprio avvio in modo asincrono; quel '
    'confine serve alla federazione per negoziare le dipendenze condivise prima che Angular '
    'parta, e non è caricamento differito. La seconda: la libreria non è l’ostacolo. Il suo '
    'componente di navigazione per schede (app-mf-layout-router-outlet) legge già le rotte figlie '
    'sia quando sono dichiarate direttamente sia quando sono caricate in differita. '
    'L’intervento riguarda quindi le shell e i micro-frontend, non la libreria.',
]:
    D.para(doc, ancora, t)
D.immagine(doc, ancora, os.path.join(IMG, 'fe_caricamento.png'), 6.3,
           'Caricamento all’avvio e caricamento differito. La libreria condivisa resta caricata '
           'all’avvio: è la base comune, non una funzione che l’operatore sceglie.')

D.para(doc, ancora, 'Perché è necessario', stile='Heading 3')
D.para(doc, ancora, 'Le ragioni sono cinque, e le prime tre riguardano il motivo stesso per cui '
                    'si è scelta un’architettura a micro-frontend.')
for testa, corpo in [
    ('Il tempo di avvio. ', 'Se tutto si carica all’avvio, il tempo che precede la prima '
     'schermata cresce con il numero di schermate esistenti, non con quelle che l’operatore '
     'usa. Il budget del pacchetto iniziale della libreria è già fissato a 2 MB come errore di '
     'costruzione, e il front-end di SIPO da migrare conta trentacinque moduli e circa '
     'milleseicentottanta template: con il caricamento all’avvio ogni schermata migrata '
     'rallenterebbe tutte le altre.'),
    ('L’indipendenza dei rilasci. ', 'È la ragione principale per adottare i micro-frontend. '
     'Se la shell carica i micro-frontend all’avvio, ne dipende al momento dell’avvio: il '
     'rilascio di uno di essi cambia l’avvio di tutti. Con il caricamento differito la shell '
     'conosce soltanto una rotta, un indirizzo e il nome di ciò che il micro-frontend espone, e '
     'ciascuno si rilascia senza toccare gli altri.'),
    ('L’isolamento dei guasti. ', 'Un micro-frontend irraggiungibile, caricato all’avvio, '
     'impedisce l’uso dell’intera applicazione. Caricato in differita, spegne soltanto la voce '
     'che lo richiama; la libreria dispone già del componente che presenta l’errore '
     '(error-boundary) invece di una pagina bianca.'),
    ('La coerenza con le abilitazioni. ', 'Con il caricamento differito il codice di un’area '
     'che l’operatore non è abilitato ad aprire — il back-office della configurazione, per '
     'esempio — non raggiunge nemmeno il suo browser. Non è una misura di sicurezza, che resta '
     'dei servizi, ma riduce ciò che viene scaricato ed esposto. ⚠️ Le guardie della libreria '
     'implementano oggi il controllo all’attivazione della rotta (CanActivate, '
     'CanActivateChild), che interviene dopo il caricamento: per evitare lo scaricamento serve '
     'la variante che decide prima di caricare (CanMatch). È un’aggiunta piccola, da proporre a '
     'chi governa la libreria.'),
    ('La giornata di lavoro. ', 'Gli operatori tengono l’applicazione aperta per ore. Ciò che '
     'non si carica non occupa memoria e non viene inizializzato: con il caricamento differito '
     'il costo di una postazione dipende da ciò che l’operatore fa, non da ciò che '
     'l’applicazione contiene.'),
]:
    D.voce(doc, ancora, testa, corpo)

D.para(doc, ancora, 'Perché è la buona pratica dei micro-frontend', stile='Heading 3')
for t in [
    'Module Federation nasce per caricare a runtime codice pubblicato altrove, e il suo uso '
    'naturale in Angular è proprio dentro le rotte: la shell dichiara una rotta, e quando '
    'l’operatore vi arriva carica il modulo esposto dal micro-frontend. È lo schema che la '
    'stessa libreria di federazione adottata dal progetto (@angular-architects/module-federation) '
    'propone come uso di riferimento.',
    '⚠️ Caricare tutto all’avvio conserva i costi dei micro-frontend — più artefatti, più '
    'rilasci da coordinare, il vincolo della versione unica — e rinuncia ai loro benefici. Il '
    'risultato è un’applicazione distribuita in più pezzi che si comporta come un blocco unico: '
    'ha la complessità di un sistema federato e la rigidità di un monolite.',
]:
    D.para(doc, ancora, t)

D.para(doc, ancora, 'Come si adotta', stile='Heading 3')
for testa, corpo in [
    ('Ogni micro-frontend espone le proprie rotte. ', 'Alla shell non si espongono singoli '
     'componenti ma l’insieme delle rotte dell’area; ciò che sta dentro resta affare del '
     'micro-frontend.'),
    ('La shell carica il micro-frontend nella rotta. ', 'Per ciascun micro-frontend la shell '
     'dichiara una rotta che ne carica le rotte esposte al momento della navigazione, come '
     'nell’esempio che segue.'),
    ('Gli indirizzi stanno nella configurazione. ', 'L’indirizzo di ciascun micro-frontend si '
     'legge a runtime, come il resto di config.json: un solo artefatto per i quattro ambienti, '
     'coerente con quanto la libreria già fa.'),
    ('Il caricamento differito vale anche all’interno. ', 'Dentro un micro-frontend le aree '
     'funzionali si caricano a loro volta alla navigazione: chi consulta un atto non scarica la '
     'finalizzazione.'),
    ('Le abilitazioni decidono prima di caricare. ', 'Con la guardia di tipo CanMatch, da '
     'aggiungere alla libreria, una rotta non autorizzata non viene scaricata.'),
    ('Si precarica soltanto ciò che è prevedibile. ', 'Quando il percorso è quasi certo — '
     'dalla compilazione di un atto alla sua finalizzazione verso ANSC — il codice del passo '
     'successivo si scarica in background. Precaricare tutto equivarrebbe a tornare al '
     'caricamento all’avvio.'),
    ('Il guasto di un micro-frontend si presenta, non si subisce. ', 'Un errore di '
     'caricamento si mostra con il componente della libreria dedicato agli errori, e la shell '
     'resta utilizzabile.'),
    ('La libreria resta caricata all’avvio. ', 'È condivisa, non differita: la shell la carica '
     'una volta e la mette a disposizione di tutti.'),
]:
    D.voce(doc, ancora, testa, corpo)
D.para(doc, ancora, 'Esempio indicativo di rotta della shell (non è codice del progetto):',
       corsivo=True)
D.ddl(doc, ancora, [
    "{",
    "  path: 'integrazione-ansc',",
    "  canMatch: [ /* guardia di abilitazione, variante CanMatch */ ],",
    "  loadChildren: () =>",
    "    loadRemoteModule({ type: 'manifest', remoteName: 'mfIntegrazioneAnsc',",
    "                       exposedModule: './routes' })",
    "      .then(m => m.ROUTES),",
    "}",
])

D.para(doc, ancora, 'Che cosa costa', stile='Heading 3')
for t in [
    'Il caricamento differito non è gratuito, e i suoi costi sono noti e contenuti. La prima '
    'apertura di un’area richiede lo scaricamento del suo codice, attesa che il precaricamento '
    'mirato riduce e l’indicatore di caricamento comune rende visibile. Gli errori di '
    'caricamento diventano un caso da gestire, per il quale la libreria ha già il componente. '
    'Serve infine un test che verifichi che ciascun micro-frontend si carichi alla navigazione e '
    'che il suo guasto non fermi la shell.',
    'Per le applicazioni nuove il caricamento differito si adotta dall’inizio e non costa nulla '
    'in più. Per quelle esistenti è un intervento sulle shell e sui micro-frontend in '
    'esercizio, che va pianificato da chi li governa: è registrato come punto aperto (OP-FE-12).',
]:
    D.para(doc, ancora, t)
fatti.append('nuova sezione «Il caricamento differito dei micro-frontend» + figura')

# ───────────────────────────────────────────── autenticazione (paragrafo commentato)
p = par_che_inizia('L’identità dell’operatore è quella di Keycloak')
D.testo_di(p, 'L’autenticazione dell’operatore non è governata dal front-end. La libreria porta '
              'il servizio che conserva i dati di sessione, la guardia che protegge le rotte e '
              'quella che, in assenza del token, reindirizza al servizio di accesso dell’ente. I '
              'dati di sessione comprendono, oltre all’utente, la struttura, l’ufficio e il '
              'tributo di appartenenza: sono i valori con cui il front-end sa a quale contesto '
              'organizzativo l’operatore appartiene. [DA VERIFICARE: quale sia il fornitore '
              'dell’identità, con quale protocollo, quale token e quale durata di sessione. Le '
              'fonti non lo dicono e la proposta tecnica chiede di definirlo; la questione va '
              'trattata nell’impianto di sicurezza e profilazione (OP-FE-11), insieme al modo in '
              'cui il profilo porta il municipio e l’ufficio di stato civile.]')
assert D.ha_commenti(p._p), 'il commento dell’utente sul paragrafo non c’è più'
fatti.append('paragrafo dell’autenticazione riscritto, commento conservato')

# ───────────────────────────────────────────── design system: standard per tutti
p = par_che_inizia('Il design system adottato è Bootstrap Italia')
D.para(doc, dopo(p), 'La libreria non è una scelta di questo progetto. È confermato [F7] che i '
                     'suoi componenti possono e devono essere usati in tutte le nuove '
                     'applicazioni di front-end: è lo standard del Comune, e il progetto lo '
                     'adotta come ogni altra applicazione nuova. Ne discende che le regole di '
                     'questo capitolo non sono preferenze di progetto ma condizioni per stare '
                     'nella stessa pagina con gli altri micro-frontend.')
riscrivi('Prima di scrivere un componente si guarda il catalogo.',
         'Prima di scrivere un componente si guarda il catalogo. I componenti della libreria sono '
         'lo standard per tutte le nuove applicazioni [F7], e sessanta componenti coprono la '
         'quasi totalità di ciò che le schermate del pilota richiedono.')

# ───────────────────────────────────────────── requisiti
rf = D.trova_tabella(doc, 'id', 'requisito', 'nota')
r = riga_con(rf, 'RF-FE-1')
D.riscrivi_cella(r.cells[1], 'Ogni nuova applicazione di front-end è realizzata come '
                             'micro-frontend caricato da una shell, che condivide con essa la '
                             'libreria; la libreria è la fonte obbligatoria di componenti e di '
                             'stile.')
D.riscrivi_cella(r.cells[2], 'Vale per tutte le nuove applicazioni di front-end, non solo per '
                             'questo progetto [F7].')
r = riga_con(rf, 'RF-FE-4')
D.riscrivi_cella(r.cells[1], 'L’identità dell’operatore è quella del servizio di accesso '
                             'dell’ente; la sessione OTP verso ANSC è cosa distinta e non si '
                             'confonde con essa.')
D.riscrivi_cella(r.cells[2], 'Due sessioni, due scadenze, due conseguenze diverse quando '
                             'cadono. Il meccanismo di accesso è da definire (OP-FE-11).')
D.clona_riga(rf, ('RF-FE-11', 'I micro-frontend e le loro aree funzionali si caricano alla '
                  'navigazione, non all’avvio; la libreria condivisa è la sola parte caricata '
                  'all’avvio dalla shell.',
                  'Oggi non adottato [F7]. Obbligatorio per le nuove applicazioni; per le '
                  'esistenti cfr. OP-FE-12.'))

rnf = D.trova_tabella(doc, 'id', 'requisito', 'valore')
r = riga_con(rnf, 'RNF-FE-1')
D.riscrivi_cella(r.cells[2], 'Il budget della libreria è oggi fissato a 2 MB come errore di '
                             'build: il margine è scarso e va sorvegliato. Il caricamento '
                             'differito (RF-FE-11) è la misura principale per rispettarlo.')

# ───────────────────────────────────────────── rischi
for t in (D.trova_tabella(doc, 'rischio', 'in che cosa consiste'),
          D.trova_tabella(doc, 'classe', 'rischio', 'mitigazione')):
    for rr in t.rows:
        for c in rr.cells:
            if 'client di autenticazione, ' in c.text:
                D.riscrivi_cella(c, c.text.replace('client di autenticazione, ', ''))
                fatti.append('tolto «client di autenticazione» da un elenco di dipendenze')

rischi = D.trova_tabella(doc, 'classe', 'rischio', 'mitigazione')
# la nuova riga di classe alta va dopo le altre due, non in coda alla bassa
ultima_alta = [rr for rr in rischi.rows if rr.cells[0].text.strip().startswith('A')][-1]
nuova = D.clona_riga(rischi, (
    'A — Alta', 'Il caricamento all’avvio di tutti i micro-frontend',
    'Oggi le applicazioni non usano il caricamento differito [F7]: il tempo di avvio cresce con '
    'ogni schermata migrata, un micro-frontend irraggiungibile ferma l’intera applicazione e il '
    'rilascio di uno tocca l’avvio di tutti.',
    'Adottarlo da subito nelle applicazioni nuove (RF-FE-11) e pianificarlo per le esistenti '
    '(OP-FE-12).'))
ultima_alta._tr.addnext(nuova._tr)

riscrivi('I rischi sono classificati secondo lo schema del modello documentale',
         'I rischi sono classificati secondo lo schema del modello documentale: alta, media e '
         'bassa. Tre sono di classe alta: due riguardano la libreria condivisa, il terzo il modo '
         'in cui le applicazioni caricano i micro-frontend — non le schermate da scrivere.')
riscrivi('⚠️ Va notato che i tre rischi alti hanno una radice comune',
         '⚠️ Va notato che i due rischi alti che riguardano la libreria hanno una radice comune: '
         'la libreria è un bene condiviso che il progetto usa ma non governa. È una situazione '
         'normale e anche desiderabile — è ciò che rende un design system tale — ma comporta che '
         'alcune decisioni del progetto dipendano da tempi altrui, e conviene dirlo prima di '
         'pianificare. Il terzo, il caricamento all’avvio, ha la stessa natura: si corregge nelle '
         'shell e nei micro-frontend in esercizio, che il progetto non governa.')

# ───────────────────────────────────────────── test
test = D.trova_tabella(doc, 'tipologia', 'che cosa verifica', 'strumento')
r = riga_con(test, 'Di integrazione fra remote')
D.riscrivi_cella(r.cells[1], 'Che la shell carichi i micro-frontend alla navigazione e non '
                             'all’avvio, che la libreria sia condivisa in una sola istanza e che '
                             'il guasto di un micro-frontend non fermi la shell.')

# ───────────────────────────────────────────── punti aperti
op = D.trova_tabella(doc, '#', 'questione', 'owner')
D.clona_riga(op, ('OP-FE-11', 'Impianto di sicurezza e profilazione: fornitore dell’identità, '
                  'protocollo, token e durata della sessione di accesso, e modo in cui il profilo '
                  'porta struttura, ufficio e municipio dell’operatore. Il documento non assume '
                  'alcun prodotto.', 'Cliente / Sistemi Informativi'))
D.clona_riga(op, ('OP-FE-12', 'Piano di adozione del caricamento differito nelle shell e nei '
                  'micro-frontend in esercizio: quali applicazioni, in quale ordine, chi '
                  'interviene; e aggiunta alla libreria della guardia di abilitazione di tipo '
                  'CanMatch.', 'Sistemi Informativi'))
riscrivi('⚠️ Una avvertenza finale sul metodo.',
         '⚠️ Una avvertenza finale sul metodo. Questo documento è stato scritto ricavando i '
         'fatti dai sorgenti della libreria e dalle fonti disponibili; dove le fonti tacciono si '
         'è scritto [DA VERIFICARE] invece di colmare con una ipotesi. Le voci così contrassegnate '
         '— il meccanismo di autenticazione, le date esatte di fine supporto delle versioni, il '
         'ciclo di vita della linea di Node adottata, il livello di accessibilità richiesto e i '
         'browser supportati — non sono dimenticanze: sono le cose che nessuna delle fonti dice, '
         'e che vanno chieste.')

doc.save(DST)

# ───────────────────────────────────────────── controlli
d2 = docx.Document(DST)
testo = '\n'.join(p.text for p in d2.paragraphs) + '\n'.join(
    c.text for t in d2.tables for r in t.rows for c in r.cells)
import zipfile   # noqa: E402
xml = zipfile.ZipFile(DST).read('word/document.xml').decode()
assert 'eycloak' not in xml, 'resta un riferimento a Keycloak nel corpo'
ncom = zipfile.ZipFile(DST).read('word/comments.xml').decode().count('<w:comment ')
for p in d2.paragraphs:
    if p.style.name.startswith('Heading') and len(p.text) > 90:
        raise SystemExit('heading anomalo: ' + p.text[:60])
print('\n'.join(fatti))
print('commenti:', ncom, '· capitoli/tabelle/immagini:', D.riepilogo(DST))
print('scritto:', DST)
