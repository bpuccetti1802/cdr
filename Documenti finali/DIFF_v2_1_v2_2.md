# DIFF ANALISI_Integrazione-ANSC — v2.1 → v2.2

Generato con `pandoc -f docx -t markdown --wrap=none` su entrambe le versioni e `diff -u`.
Le tabelle sono rese da pandoc in forma testuale: le righe modificate compaiono per intero.

```diff
--- /private/tmp/claude-501/-Users-minimac-Desktop-Comune-di-Roma/3b9ca8c9-37c0-47b3-94e4-e7c7d4aaeb8f/scratchpad/v2_1.md	2026-08-03 14:42:13
+++ /private/tmp/claude-501/-Users-minimac-Desktop-Comune-di-Roma/3b9ca8c9-37c0-47b3-94e4-e7c7d4aaeb8f/scratchpad/v2_2.md	2026-08-03 15:11:01
@@ -46,17 +46,19 @@
 
 **Storia del Documento**
 
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **Data consegna**   **Versione**   **Cap. /Sez. modificati**                                                                                                                 **Sintesi dei cambiamenti**
-  ------------------- -------------- ----------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  23/07/2026          0,4            Prima stesura                                                                                                                             Bozza del documento per iniziare discussione
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Data consegna**   **Versione**   **Cap. /Sez. modificati**                                                                                                                                                                      **Sintesi dei cambiamenti**
+  ------------------- -------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  23/07/2026          0.4            Prima stesura                                                                                                                                                                                  Bozza del documento per iniziare discussione
 
-  23/07/2026          1.0            Prima versione non ancora ufficiale.                                                                                                      Documento con le prime ipotesi di schermate, tabelle, strutture.
+  23/07/2026          1.0            Prima versione non ancora ufficiale.                                                                                                                                                           Documento con le prime ipotesi di schermate, tabelle, strutture.
+
+  26/07/2026          2.0            Vincoli ANSC (nuovo); Requisiti; Architettura; Worker→Modello di esecuzione; PC-1/2/3/5/7; Back-office; App. A/B; Glossario; Open Point                                                        Correzione dell'impianto: la scrittura verso ANSC è presidiata (firma USC con OTP per atto, R009 che deposita la bozza), Eliminata corsia asincrona non presidiata. Rimosse le alcune parti non più coerenti.
 
-                                                                                                                                                                               
+  03/08/2026          2.1            Porting in Kubernetes (capp. 6 e 7); Modello dati                                                                                                                                              Revisione redazionale: «lift-and-shift» sostituito da «porting»; ampliati i presupposti dell'attività e la disamina delle difficoltà.
 
-  26/07/2026          2.0            Vincoli ANSC (nuovo); Requisiti; Architettura; Worker→Modello di esecuzione; PC-1/3/4/5/6; Back-office; App. A/B; Glossario; Open Point   Correzione dell'impianto: la scrittura verso ANSC è presidiata (firma USC con OTP per atto, R009 che deposita la bozza), Eliminata corsia asincrona non presidiata. Rimosse le alcune parti non più coerenti.
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  03/08/2026          2.2            Premesse e requisiti; Vincoli ANSC; Architettura; Deployment; Modello dati; Mappatura payload; Gestione dei dizionari ANSC (nuovo); Modello di esecuzione; Open Point; Back-office; App. A/B   Rilettura critica: bonifica del lessico outbox, coerenza preverifica/back-office/ordine dei servizi, correzione della mappa casistiche Morte_xxx e dei percorsi del modello evento, allineamento del modello dati e delle API. Nuovo capitolo sulla gestione dei dizionari ANSC (RF-10): concentratore dedicato, comando di aggiornamento on request, tabelle e fruizione da SIPO.
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 # Sommario {#sommario .TOC-Heading}
 
@@ -258,9 +260,9 @@
 
 ## Glossario
 
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Termine**                       **Significato**
-  --------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  --------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   ANSC                              Archivio Nazionale dello Stato Civile.
 
   SIPO                              Sistema Informativo della Popolazione di Roma Capitale.
@@ -283,7 +285,7 @@
 
   Sessione OTP                      Sessione presidiata dell'USC delimitata dalla validità dell'OTP (quattro ore), acquisito dalla web app ANSC; risorsa condivisa con ciclo di vita esplicito, propagata nel JWT.
 
-  Certificato di postazione         Certificato X.509 associato alla singola postazione (CN = «postazione» nel JWT), con cui token e payload sono firmati nella modalità presidiata.
+  Certificato di postazione         Certificato X.509 associato alla singola postazione (CN = «postazione» nel JWT), con cui il D.M. prevede che token e payload siano firmati nella modalità presidiata. Nell'ipotesi di lavoro adottata per Roma --- certificato server unico --- il claim «postazione» resta valorizzato dal registro delle postazioni, mentre la firma è apposta con il certificato server: l'ambiguità è tracciata in OP-15.
 
   Certificato server                Certificato usato nella modalità M2M (senza presenza di utente) nel claim x5c; nel pattern a certificato unico per Roma copre tutte le postazioni, con registro delle postazioni a carico del comune.
 
@@ -292,8 +294,10 @@
   Registro di emergenza             Registro cartaceo cronologico previsto dall'art. 10 del D.M. durante l'interruzione del sistema; le operazioni sono riportate in ANSC dopo il ripristino. Unico percorso differito legittimo, di eccezione.
 
   Token JWT / JWS                   Bearer token (header Authorization) con firma JWS Detached del payload, costruito e firmato dal concentratore (BE) con il certificato server; autentica ogni chiamata cooperativa. Porta OTP, sub, postazione, sede, x5c.
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
+  Dizionario ANSC (decodifica)      Tabella di valori codificati pubblicata da ANSC e reperibile con il servizio R901 (identificata come ANSC_xx). Replicata in tabelle locali di ANSC_USR e aggiornata su comando manuale, è il catalogo con cui il pre-filtro valida i codici e le maschere presentano i valori ammessi.
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
 ## Riferimenti
 
   -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@@ -322,7 +326,7 @@
 
 Allo stato attuale SIPO non dispone di alcuna integrazione in scrittura verso ANSC: si tratta quindi di una realizzazione nuova, non della modifica di un flusso esistente. Esiste invece un'integrazione consolidata verso ANPR, di natura tecnologica diversa (SOAP), che assumiamo come precedente organizzativo ma non come base di codice riutilizzabile: ANSC espone interfacce REST/JSON.
 
-La base dati è Oracle 12.2, collocata all'esterno del cluster Kubernetes ed ad oggi non è previsto un piano di aggiornamento della versione. Questi due elementi influenzano di conseguenza il disegno e sono ripresi al capitolo sulle decisioni architetturali.
+La base dati è Oracle 12.2, collocata all'esterno del cluster Kubernetes e ad oggi non è previsto un piano di aggiornamento della versione. Questi due elementi influenzano di conseguenza il disegno e sono ripresi al capitolo sulle decisioni architetturali.
 
 ## Requisiti funzionali
 
@@ -333,7 +337,7 @@
 
   RF-2     L'operazione è innescata da un'azione dell'operatore, dal front-end.                                                                                                                                                                                    Scelta motivata dalla velocità di realizzazione; il disegno ne mitiga i rischi (cfr. punto controverso PC-1).
 
-  RF-3     Il front-end espone il pulsante «Verifica» (pre-filtro dei dati).                                                                                                                                                                                       Pre-filtro locale (RF-9) contro le regole ANSC replicate in cache (R901/R023): non contatta ANSC né deposita nulla.
+  RF-3     Il front-end espone il pulsante «Verifica» (pre-filtro dei dati).                                                                                                                                                                                       Pre-filtro locale (RF-9) contro le regole ANSC replicate in locale (dizionari ANSC replicati con RF-10 e mapping ufficiale dei casi d'uso): non contatta ANSC né deposita nulla.
 
   RF-4     Il superamento della verifica abilita il pulsante «Finalizza».                                                                                                                                                                                          Finché la verifica non è superata, «Finalizza» resta disabilitato.
 
@@ -346,6 +350,8 @@
   RF-8     Perimetro del pilota: creazione dell'atto di morte.                                                                                                                                                                                                     L'architettura è generalizzabile agli altri eventi; si parte dalla morte.
 
   RF-9     Sistema di configurazione dei campi obbligatori per tipo operazione: dato il tipo operazione (ricevuto dal FE o dedotto), verifica in fase di «Verifica» l'obbligatorietà dei campi richiesti da ANSC prima del deposito (R009) e della firma (R007).   Riusabile per tutti i tipi di atto; riduce l'effort e i round-trip di errore verso ANSC.
+
+  RF-10    I dizionari (tabelle di decodifica) di ANSC sono replicati in tabelle locali e resi disponibili a tutto SIPO.                                                                                                                                           Aggiornamento su comando manuale (on request), non schedulato; alimenta il pre-filtro RF-9 e le maschere. Cfr. cap. «Gestione dei dizionari ANSC».
   -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 ## Requisiti non funzionali
@@ -357,30 +363,30 @@
 
   RNF-2         La formazione dell'atto verso ANSC è un'operazione presidiata: non è differibile a un processo non presidiato.   Esistono termini di legge per la formazione degli atti, per tipologia (D.P.R. 396/2000); la trasmissione ad ANSC coincide con la formazione firmata, non è un invio differito. Vedi cap. «Vincoli imposti dal contratto di servizio ANSC».
 
-  RNF-3         Volumi attesi (pilota morte).                                                                                    Circa 90.000 atti/anno, pari a \~360 al giorno lavorativo: carico basso.
+  RNF-3         Volumi attesi (pilota morte).                                                                                    Stima da confermare, ordine di grandezza 3·10⁴ atti/anno, pari a \~120 al giorno lavorativo: carico basso. La cifra non è tracciabile a una fonte del progetto; il dimensionamento reale è tracciato in OP-24.
 
   RNF-4         SLA verifica sincrona.                                                                                           Proposta: p95 \< 2 s (l'operatore è in attesa dell'esito). Da confermare.
 
-  RNF-6         Base dati.                                                                                                       Oracle 12.2, esterna al cluster, senza piano di upgrade.
+  RNF-5         Base dati.                                                                                                       Oracle 12.2, esterna al cluster, senza piano di upgrade.
 
-  RNF-7         Ambiente di esecuzione.                                                                                          Kubernetes (scelte di piattaforma in carico ai referenti infrastrutturali).
+  RNF-6         Ambiente di esecuzione.                                                                                          Kubernetes (scelte di piattaforma in carico ai referenti infrastrutturali).
 
-  RNF-8         Modifiche all'esistente.                                                                                         Nuove tabelle ammesse; modifiche a tabelle o campi esistenti solo su proposta approvata.
+  RNF-7         Modifiche all'esistente.                                                                                         Nuove tabelle ammesse; modifiche a tabelle o campi esistenti solo su proposta approvata.
   ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
-Sul RNF-3: il volume basso (\~360 atti/giorno) rende irrilevante il dimensionamento; ma il driver del disegno non è la portata, bensì il vincolo presidiato. La formazione dell'atto è sincrona e non è disaccoppiabile dalla disponibilità di ANSC: se ANSC è indisponibile l'atto non si forma, e l'unico percorso differito legittimo è il registro di emergenza (art. 10 del D.M.), non una coda automatica. L'elemento portante è quindi la sessione presidiata dell'ufficiale, non una coda di invii.
+Sul RNF-3: il volume basso (\~120 atti/giorno nell'ordine di grandezza stimato) rende irrilevante il dimensionamento; ma il driver del disegno non è la portata, bensì il vincolo presidiato. La formazione dell'atto è sincrona e non è disaccoppiabile dalla disponibilità di ANSC: se ANSC è indisponibile l'atto non si forma, e l'unico percorso differito legittimo è il registro di emergenza (art. 10 del D.M.), non una coda automatica. L'elemento portante è quindi la sessione presidiata dell'ufficiale, non una coda di invii.
 
 # Vincoli imposti dal contratto di servizio ANSC
 
-Il capitolo documenta i vincoli accertati sul contratto di servizio ANSC, verificati direttamente sui sorgenti del repository italia/ansc (docs/openapi/, docs/Note/, docs/Decodifiche/, docs/Changelog.md) e sulla normativa (D.P.R. 396/2000; D.M. 18 ottobre 2022 e relativo Allegato 4 «Misure di sicurezza»). È il presupposto dell'architettura proposta ed esiste perché nessuno, a valle, reintroduca l'impianto errato descritto nella sezione «Modifiche rispetto alla v1.0»: la scrittura verso ANSC è un'operazione presidiata, non una corsia asincrona non presidiata.
+Il capitolo documenta i vincoli accertati sul contratto di servizio ANSC, verificati direttamente sui sorgenti del repository italia/ansc (docs/openapi/, docs/Note/, docs/Decodifiche/, docs/Changelog.md) e sulla normativa (D.P.R. 396/2000; D.M. 18 ottobre 2022 e relativo Allegato 4 «Misure di sicurezza»). È il presupposto dell'architettura proposta ed esiste perché nessuno, a valle, reintroduca l'impianto errato della v1.0 (cfr. Storia del Documento): la scrittura verso ANSC è un'operazione presidiata, non una corsia asincrona non presidiata.
 
 ## Catalogo e natura dei servizi
 
-ANSC espone i servizi cooperativi da R001 a R024 più R901 (docs/openapi/): sono tutti sincroni e operano su singola operazione (POST). Non esistono servizi batch o massivi: nessun endpoint accetta array di eventi; la paginazione (base_servizi.yaml, DatiPaginazione) esiste soltanto in lettura, sulle ricerche. Gli ambienti sono produzione (anscservice.anpr.interno.it), preproduzione (anscservicepre.anpr.interno.it) e un mock locale; la versione del servizio è nel path della richiesta ({version}). La versione del contratto a cui ci si allinea è quella pubblicata nel Changelog (all'analisi: 1.53.0 del 30-06-2026); i singoli file OpenAPI portano una propria versione.
+ANSC espone i servizi cooperativi da R001 a R024 più R901 (docs/openapi/): sono tutti sincroni e operano su singola operazione (POST). Non esistono servizi batch o massivi: nessun endpoint accetta array di eventi; la paginazione (base_servizi.yaml, DatiPaginazione) esiste soltanto in lettura, sulle ricerche. Gli ambienti ANSC sono produzione (anscservice.anpr.interno.it), preproduzione (anscservicepre.anpr.interno.it) e un mock locale. Nel seguito si usa questa terminologia per gli ambienti ANSC e quella SIPO --- sviluppo, test, esercizio --- per gli ambienti interni; la corrispondenza operativa è esercizio SIPO → produzione ANSC, test e sviluppo SIPO → preproduzione ANSC o mock locale; la versione del servizio è nel path della richiesta ({version}). La versione del contratto a cui ci si allinea è quella pubblicata nel Changelog (all'analisi: 1.53.0 del 30-06-2026); i singoli file OpenAPI portano una propria versione.
 
 La testata di richiesta (base_servizi.yaml, TestataRichiesta) porta idOperazioneComune («identificativo dell'operazione scelto dal comune»), dataOraRichiesta e i campi nomeApplicativo, versioneApplicativo, fornitoreApplicativo. Corollario verificato: idOperazioneComune è un identificativo di tracciamento scelto dal comune, non è dichiarato come chiave di deduplica lato ANSC. Non esiste quindi una chiave di idempotenza ANSC.
 
-Il modello dell'evento (model_evento.yaml) referenzia 88 decodifiche ANSC_xx distinte, i cui valori risiedono nelle tabelle di decodifica (docs/Decodifiche/) e sono reperibili tramite il servizio R901. La configurazione dei campi (RF-9) può quindi replicare localmente le decodifiche cachandole via R901.
+Il modello dell'evento (model_evento.yaml) referenzia 87 decodifiche ANSC_xx distinte (88 le occorrenze letterali: ANSC_04 e ANSC_4 sono la stessa), i cui valori risiedono nelle tabelle di decodifica (docs/Decodifiche/) e sono reperibili tramite il servizio R901. La configurazione dei campi (RF-9) può quindi replicare localmente le decodifiche cachandole via R901.
 
 ## Il ciclo di vita dell'atto
 
@@ -408,11 +414,11 @@
 
 L'OTP generato dall'applicazione web ANSC ha una durata di quattro ore (nota tecnica JWT ANSC, v1.1.1). Va trattato come risorsa di sessione condivisa con ciclo di vita esplicito, non come parametro di chiamata: la firma di ogni atto (R007, ParametriFirma.inputFirma3) richiede l'OTP, e l'intera sessione presidiata dell'ufficiale è delimitata dalla sua validità.
 
-Un timeout su una chiamata può invalidare l'OTP della sessione, rendendo inutilizzabili anche le chiamate successive; il recupero richiede che l'operatore rigeneri l'OTP dalla web app. La gestione del ciclo di vita della sessione (acquisizione, rilevazione dell'invalidazione, richiesta di rigenerazione) è responsabilità del concentratore. Questo tipo di problematica richiederà intervento sull aparte di FE.
+Un timeout su una chiamata può invalidare l'OTP della sessione, rendendo inutilizzabili anche le chiamate successive; il recupero richiede che l'operatore rigeneri l'OTP dalla web app. La gestione del ciclo di vita della sessione (acquisizione, rilevazione dell'invalidazione, richiesta di rigenerazione) è responsabilità del concentratore. Questo tipo di problematica richiederà un intervento sulla parte di FE.
 
 ## Il pattern di certificazione per i comuni grandi
 
-Se il comune usa un unico certificato server per tutte le postazioni, è responsabilità del comune creare e mantenere aggiornato l'elenco delle postazioni autorizzate, ciascuna identificata da un codice attribuito da ANPR, e conservare l'associazione tra postazione fisica e identificativo. Per Roma, data la numerosità delle postazioni e dei municipi, ritengo sia l' opzione più praticabile: va dichiarata come scelta architetturale, con le componenti che ne discendono a carico del sistema (registro delle postazioni, tracciamento postazione ↔ identificativo, presidiato dall'audit).
+Se il comune usa un unico certificato server per tutte le postazioni, è responsabilità del comune creare e mantenere aggiornato l'elenco delle postazioni autorizzate, ciascuna identificata da un codice attribuito da ANPR, e conservare l'associazione tra postazione fisica e identificativo. Per Roma, data la numerosità delle postazioni e dei municipi, si ritiene sia l'opzione più praticabile: va dichiarata come scelta architetturale, con le componenti che ne discendono a carico del sistema (registro delle postazioni, tracciamento postazione ↔ identificativo, presidiato dall'audit).
 
 Il decreto su questo punto è ambiguo: nella sezione M2M indica il certificato server nel claim x5c, ma ripete poi che token e payload sono firmati con il certificato di postazione.
 
@@ -426,19 +432,17 @@
 
 ## Visione d'insieme
 
-Si propone un concentratore unico, denominato in via provvisoria «all-ansc-sipo», deployato su Kubernetes, che media tutto il dialogo fra i moduli SIPO e ANSC. È il gemello concettuale del modulo «all-anpr-sipo» già esistente per ANPR: gli applicativi non parlano con ANSC direttamente, ma invocano il concentratore attraverso una chiamata REST interna. In questo modo tutta la complessità propria di ANSC --- protocollo REST/JSON, autenticazione JWT (OTP, certificato di postazione), gestione della sessione presidiata --- resta confinata in uno o più componenti nuovi, e l'impatto sui moduli chiamanti risulterà minimo.
+Si propone un concentratore unico, denominato in via provvisoria «all-ansc-sipo», deployato su Kubernetes, che media tutto il dialogo fra i moduli SIPO e ANSC. È il gemello concettuale del modulo «all-anpr-sipo» già esistente per ANPR: gli applicativi non parlano con ANSC direttamente, ma invocano il concentratore attraverso una chiamata REST interna. In questo modo tutta la complessità propria di ANSC --- protocollo REST/JSON, autenticazione JWT (OTP e certificato server, nell'ipotesi di lavoro adottata per Roma --- OP-15), gestione della sessione presidiata --- resta confinata in uno o più componenti nuovi, e l'impatto sui moduli chiamanti risulterà minimo.
 
-Ritengo che questa sia la scelta che meglio interpreta il vincolo di integrazione «con il minimo effort».
+Si ritiene che questa sia la scelta che meglio interpreta il vincolo di integrazione «con il minimo effort».
 
 Il concentratore ha tre responsabilità, tutte lato back-end: il pre-filtro locale di verifica (RF-9); la gestione della sessione OTP e del token (custodia dell'OTP di sessione, costruzione e firma del JWT/JWS con il certificato server, instradamento della postazione); e l'orchestrazione del percorso presidiato di formazione dell'atto (R009 deposito bozza → R007 firma USC). Il front-end resta quello di SIPO: ospita le maschere esistenti, attiva la web-login OTP e trasmette l'OTP al concentratore, ma non dialoga con ANSC. La trasmissione ad ANSC coincide con la formazione firmata dell'atto, dentro il flusso SIPO.
 
-L'esempio che segue serve a dimostrare l'universalità del modello e la sua applicabilità a tutte le possibili operazioni verso ansc.
+Nel pattern a certificato server unico con elenco delle postazioni autorizzate a carico del comune (cap. «Vincoli imposti dal contratto di servizio ANSC»), la gestione centralizzata del certificato, del registro postazione ↔ identificativo e della sessione OTP è la scelta più opportuna. Il concentratore all-ansc-sipo è quindi l'unico punto di governo della sessione presidiata e dell'identità di postazione. Inoltre è il solo luogo dove può risiedere la chiave privata del certificato server (PKCS#12) e dove l'OTP di sessione può essere custodito e trasformato in token firmati: la firma dei JWT/JWS e la gestione della sessione sono per costruzione centralizzate nel concentratore.
 
-Nel pattern a certificato server unico con elenco delle postazioni autorizzate a carico del comune (cap. «Vincoli imposti dal contratto di servizio ANSC»), la gestione centralizzata del certificato, del registro postazione ↔ identificativo e della sessione OTP è la scelta più opportuna. Il concentratore all-ansc-sipo quindi l'unico punto di governo della sessione presidiata e dell'identità di postazione. Inoltre è il solo luogo dove può risiedere la chiave privata del certificato server (PKCS#12) e dove l'OTP di sessione può essere custodito e trasformato in token firmati: la firma dei JWT/JWS e la gestione della sessione sono per costruzione centralizzate nel concentratore.
-
 ## Flusso funzionale del pilota (creazione atto di morte)
 
-Il flusso realizza il percorso presidiato: pre-filtro locale, deposito della bozza (R009, che assegna idAnsc), eventuale attesa della verifica degli allegati (R001), firma dell'USC (R007, con OTP di sessione), atto formato; la riconciliazione R005/R011 interviene solo sugli esiti indeterminati.
+Il flusso realizza il percorso presidiato, nella sequenza del flusso base ufficiale: pre-filtro locale, invio e verifica degli allegati (R001), consultazione del soggetto (R005), deposito della bozza (R009, che assegna idAnsc), firma del dichiarante (R006), firma dell'USC (R007, con OTP di sessione), atto formato; la riconciliazione R005/R011 interviene solo sugli esiti indeterminati.
 
   -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Passo**   **Fase**                        **Descrizione**
@@ -464,27 +468,27 @@
 
 Il punto in cui l'impianto è a prova di errore non è più un salvataggio da drenare in differita, ma il fatto che la bozza è depositata in ANSC (con idAnsc) contestualmente alla validazione, e la firma è un atto presidiato dell'ufficiale: non esiste un invio automatico da presidiare.
 
-*Flusso §3.2 --- formazione dell'atto (SIPO-centrico). In SIPO: Compila → Verifica (pre-filtro RF-9) → «Finalizza» → web-login OTP se la sessione non è valida. Orchestrazione ANSC (concentratore, entro la sessione OTP) secondo il flusso base ufficiale: R001 allegati → R001 verifica → R005 consultazione soggetto → R009 validazione (CONFERMATO, idAnsc) → R006 firma dichiarante → R007 firma USC → atto formato. Rami: anomalie; esiti indeterminati (R005/R011).*
+*Flusso §4.2 --- formazione dell'atto (SIPO-centrico). In SIPO: Compila → Verifica (pre-filtro RF-9) → «Finalizza» → web-login OTP se la sessione non è valida. Orchestrazione ANSC (concentratore, entro la sessione OTP) secondo il flusso base ufficiale: R001 allegati → R001 verifica → R005 consultazione soggetto → R009 validazione (CONFERMATO, idAnsc) → R006 firma dichiarante → R007 firma USC → atto formato. Rami: anomalie; esiti indeterminati (R005/R011).*
 
 ![](media/image2.png){width="6.6in" height="5.094736439195101in"}
 
 ## Componenti
 
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Componente**                                       **Responsabilità**
-  ---------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   Front-end (modulo esistente)                         Maschere SIPO esistenti (formazione dell'atto, modifica minima); attiva la web-login OTP alla postazione e trasmette l'OTP al concentratore. Non parla con ANSC né costruisce token.
 
   Concentratore all-ansc-sipo (nuovo)                  Pre-filtro locale di verifica (RF-9); gestione della sessione OTP e del token (costruzione e firma JWT/JWS con il certificato server); orchestrazione del percorso presidiato (R009 deposito bozza → R007 firma USC). Idempotenza locale e gestione degli esiti indeterminati.
 
   Store di stato ANSC (schema ANSC_USR)                Una riga per atto×operazione con lo stato reale in ANSC; attributo dell'atto SIPO, non coda di trasporto. La lista atti incompleti è una vista di supervisione su questo store.
 
-  Gestore della sessione OTP e del token (nuovo, BE)   Custodisce l'OTP di sessione (USC+postazione, 4h), costruisce e firma il JWT/JWS con il certificato server, rileva l'invalidazione e richiede la rigenerazione; non firma atti in autonomia (la firma R007 è azione dell'USC).
+  Gestore della sessione OTP e del token (nuovo, BE)   Custodisce l'OTP di sessione (USC+postazione, 4h) in uno store condiviso esterno al pod (cfr. §5.3), costruisce e firma il JWT/JWS con il certificato server, rileva l'invalidazione e richiede la rigenerazione; non firma atti in autonomia (la firma R007 è azione dell'USC).
 
-  Client ANSC (nuovo, generato)                        Adattatore REST/JSON verso ANSC generato dagli OpenAPI; gestisce autenticazione JWT (OTP, x5c, certificato di postazione) e la firma R007.
+  Client ANSC (nuovo, generato)                        Adattatore REST/JSON verso ANSC generato dagli OpenAPI: trasporta le chiamate applicando il token e la firma JWS già prodotti dal gestore della sessione, e invoca R007 con i parametri di firma raccolti dalla maschera. Non costruisce né firma token.
 
   Ricevitore notifiche ANSC (eventuale)                Consumo in lettura delle notifiche R008 (modalità non presidiata, ammessa): allinea lo stato, non forma atti. Eventuale.
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 # Architettura di deployment su Kubernetes
 
@@ -492,25 +496,27 @@
 
 ## Topologia
 
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **Elemento**                             **Oggetto Kubernetes**                         **Collocazione**       **Note**
-  ---------------------------------------- ---------------------------------------------- ---------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  Concentratore all-ansc-sipo              Deployment stateless, ≥ 2 repliche + Service   In-cluster             Espone il pre-filtro di verifica e orchestra la formazione presidiata (R009 deposito → R007 firma) entro la sessione OTP; gestisce token e chiamate ANSC lato server.
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Elemento**                                **Oggetto Kubernetes**                         **Collocazione**       **Note**
+  ------------------------------------------- ---------------------------------------------- ---------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Concentratore all-ansc-sipo                 Deployment stateless, ≥ 2 repliche + Service   In-cluster             Espone il pre-filtro di verifica e orchestra la formazione presidiata (R009 deposito → R007 firma) entro la sessione OTP; gestisce token e chiamate ANSC lato server. La sessione OTP è stato condiviso e non può risiedere nel pod: cfr. §5.3.
 
-  Processo di automazione (letture/code)   Deployment, 1--2 repliche                      In-cluster             Esegue le sole attività non presidiate ammesse: polling notifiche (R008), reminder (R021), allineamento decodifiche (R901), consultazioni. Non forma né firma atti.
+  Processo di automazione (letture/code)      Deployment, 1--2 repliche                      In-cluster             Esegue le sole attività non presidiate ammesse: polling notifiche (R008), reminder (R021), consultazioni. Non forma né firma atti. L'aggiornamento dei dizionari non è fra queste: è un comando manuale, affidato al componente dedicato.
 
-  Ricevitore notifiche ANSC                Deployment + Service + Ingress                 In-cluster             Eventuale: solo se ANSC notifica soggetti terzi (OP-03); richiede ingresso dall'esterno.
+  Concentratore dei dizionari dec-ansc-sipo   Deployment, 1 replica + Service                In-cluster             Recupera le decodifiche ANSC su comando manuale (R901) e le carica nelle tabelle di ANSC_USR. Invoca R901 passando per all-ansc-sipo: non detiene certificati e non costruisce token.
 
-  Broker di messaggistica                  StatefulSet in alta affidabilità               In-cluster             Opzionale (cfr. PC-6); non è deposito di verità.
+  Ricevitore notifiche ANSC                   Deployment + Service + Ingress                 In-cluster             Eventuale: solo se ANSC notifica soggetti terzi (OP-03); richiede ingresso dall'esterno.
+
+  Broker di messaggistica                     StatefulSet in alta affidabilità               In-cluster             Opzionale; non è deposito di verità.
 
-  Configurazione                           ConfigMap                                      In-cluster             URL, ambiente, parametri di ritentativo: risolve l'anti-pattern dell'ambiente cablato.
+  Configurazione                              ConfigMap                                      In-cluster             URL, ambiente, parametri di ritentativo: risolve l'anti-pattern dell'ambiente cablato.
 
-  Segreti                                  Secret / secret manager                        In-cluster / esterno   Credenziali e certificati verso ANSC e verso il DB: fuori dal codice e dal repository.
+  Segreti                                     Secret / secret manager                        In-cluster / esterno   Credenziali e certificati verso ANSC e verso il DB: fuori dal codice e dal repository.
 
-  Base dati                                --- (Oracle 12.2)                              ESTERNA al cluster     Accesso in uscita dai pod; ospita l'outbox, sorgente di verità.
+  Base dati                                   --- (Oracle 12.2)                              ESTERNA al cluster     Accesso in uscita dai pod; ospita lo store di stato ANSC; è la sorgente di verità locale.
 
-  ANSC                                     --- (endpoint remoto)                          ESTERNO                Accesso in uscita; autenticazione e rete da definire (OP-05).
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ANSC                                        --- (endpoint remoto)                          ESTERNO                Accesso in uscita; autenticazione e rete da definire (OP-05).
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 ## Flussi di traffico
 
@@ -534,6 +540,8 @@
 
 I componenti sono privi di stato locale ovvero nessun dato risiederà nei pod, lo stato dell'atto in ANSC è nello store ANSC_USR su Oracle. Un pod può quindi essere terminato o riavviato senza perdita di informazioni e senza sessioni da preservare.
 
+Fa eccezione la sessione OTP. L'OTP dell'ufficiale (validità quattro ore) è stato condiviso fra le repliche: se fosse custodito nella memoria del pod, un riavvio o l'instradamento su una replica diversa costringerebbe l'operatore a rigenerarlo. Va quindi conservato fuori dal pod, in uno store condiviso --- cache distribuita o tabella dedicata in ANSC_USR --- con TTL allineato alle quattro ore e cancellazione all'invalidazione; l'affinità di sessione all'ingress è ammessa solo come mitigazione temporanea, non come soluzione.
+
 La configurazione segue il principio dell'immagine unica per tutti gli ambienti, differenziata solo tramite ConfigMap e Secret: nessuna ricompilazione per ambiente. Questa è la correzione diretta dell'anti-pattern riscontrato nell'integrazione ANPR, dove l'ambiente risulta cablato nel codice; analogamente, i segreti vanno gestiti fuori dal repository, correggendo l'altro anti-pattern rilevato.
 
 ## Scalabilità e resilienza
@@ -552,7 +560,7 @@
 
 ## Connettività verso la base dati esterna
 
-La collocazione della base dati all'esterno del cluster (RNF-6) non pregiudica il pattern proposto: le transazioni --- incluso l'inserimento nell'outbox contestuale al salvataggio dell'atto --- restano interamente lato Oracle. Ai pod è richiesto un accesso in uscita verso host e porta della base dati, un pool di connessioni dimensionato sul carico basso e una gestione robusta della riconnessione in caso di riavvii o interruzioni di rete.
+La collocazione della base dati all'esterno del cluster (RNF-5) non pregiudica il pattern proposto: le transazioni --- incluso l'aggiornamento dello stato ANSC contestuale al salvataggio dell'atto --- restano interamente lato Oracle. Ai pod è richiesto un accesso in uscita verso host e porta della base dati, un pool di connessioni dimensionato sul carico basso e una gestione robusta della riconnessione in caso di riavvii o interruzioni di rete.
 
 ## Osservabilità
 
@@ -572,7 +580,7 @@
 
 ## Stato di partenza
 
-Lo stato di partenza è, a nostro avviso, comunque favorevole. Dall'analisi del codice infatti risulta che i moduli sono già containerizzati --- la configurazione prevede profili distinti per ambiente (sviluppo, test, esercizio) in forma «Docker» e i moduli si individuano reciprocamente per nome host (ad esempio «anprsipo», «crianprbe»). La comunicazione interna è già REST, mediata da un client comune con modello a dominio e token. Il passaggio a Kubernetes è quindi, in prima approssimazione, un repackaging con relativi manifest e l'esternalizzazione di configurazione e segreti, non una riscrittura. La base dati Oracle 12.2, esterna al cluster, resta invariata quindi i moduli continueranno a raggiungerla in uscita come già oggi.
+Lo stato di partenza è comunque favorevole. Dall'analisi del codice infatti risulta che i moduli sono già containerizzati --- la configurazione prevede profili distinti per ambiente (sviluppo, test, esercizio) in forma «Docker» e i moduli si individuano reciprocamente per nome host (ad esempio «anprsipo», «crianprbe»). La comunicazione interna è già REST, mediata da un client comune con modello a dominio e token. Il passaggio a Kubernetes è quindi, in prima approssimazione, un repackaging con relativi manifest e l'esternalizzazione di configurazione e segreti, non una riscrittura. La base dati Oracle 12.2, esterna al cluster, resta invariata quindi i moduli continueranno a raggiungerla in uscita come già oggi.
 
 ## Unità di deployment
 
@@ -638,7 +646,7 @@
 
 Le difficoltà non sono generiche ma risultano legate alle caratteristiche reali del sistema riscontrate nell'analisi del codice. L'obiettivo di consentire una pianificazione dell'attività di porting che minimizzi il rischio, richiede comunque una attenta attività di studio ed analisi distinguendo ciò che va necessariamente affrontato da ciò che può essere rimandato.
 
-Lo studio del porting dovrà inevitabilmente convolgere esperti di sistema in grado di verificare le rotte ip interne al cluster, strutturare la sicurezza, ecc...; sviluppatori in grado di effettuare il minimo indispensabile di modifiche di adattamento; architetti di sistema ed infine dei tester per fare l'analisi comparativa con il sistema attuale.
+Lo studio del porting dovrà inevitabilmente coinvolgere esperti di sistema in grado di verificare le rotte ip interne al cluster, strutturare la sicurezza, ecc...; sviluppatori in grado di effettuare il minimo indispensabile di modifiche di adattamento; architetti di sistema ed infine dei tester per fare l'analisi comparativa con il sistema attuale.
 
 ## Principi guida
 
@@ -742,34 +750,36 @@
 
 # Modello dati
 
-Si può pensare ad uno schema dedicato nuovo, «ANSC_USR», coerente con la convenzione di denominazione degli schemi esistenti. La scelta mantiene la logica del "tutto additivo" e non impatta gli schemi esistenti (coerentemente con RNF-8): lo stato ANSC dell'atto vive in ANSC_USR, agganciato alla chiave dell'atto SIPO. La proposta è da sottoporre al settore tecnico per la verifica di grant e tablespace.
+Si può pensare ad uno schema dedicato nuovo, «ANSC_USR», coerente con la convenzione di denominazione degli schemi esistenti. La scelta mantiene la logica del "tutto additivo" e non impatta gli schemi esistenti (coerentemente con RNF-7): lo stato ANSC dell'atto vive in ANSC_USR, agganciato alla chiave dell'atto SIPO. La proposta è da sottoporre al settore tecnico per la verifica di grant e tablespace.
 
-  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **Oggetto**   **Ruolo**                                           **Note principali**
-  ------------- --------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  ANSC_OUTBOX   Store di stato ANSC per atto (non coda di invii).   Una riga per atto×operazione: chiave atto + tipo operazione/evento, stato del ciclo di vita reale in ANSC (IN_PREPARAZIONE (SIPO), CONFERMATO (R009), FIRMATO_DICHIARANTE (R006), FIRMATO_USC (R007), RIFIUTATA (KO validazione), ANNULLATO (R011)), idAnsc, ufficiale, municipio, audit. La supervisione è una vista su questo store.
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Oggetto**       **Ruolo**                                           **Note principali**
+  ----------------- --------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ANSC_STATO_ATTO   Store di stato ANSC per atto (non coda di invii).   Una riga per atto×operazione: chiave atto + tipo operazione/evento, stato del ciclo di vita reale in ANSC (IN_PREPARAZIONE (SIPO), CONFERMATO (R009), FIRMATO_DICHIARANTE (R006), FIRMATO_USC (R007), RIFIUTATA (KO validazione), ANNULLATO (R011)), idAnsc, ufficiale, municipio, audit. La supervisione è una vista su questo store.
 
-  ANSC_XREF     Mappa durevole atto SIPO ↔ protocollo/id ANSC.      Registra l'esito finale e consente la riconciliazione.
+  ANSC_XREF         Mappa durevole atto SIPO ↔ protocollo/id ANSC.      Registra l'esito finale e consente la riconciliazione. Con l'aggiunta di ID_ANSC allo store di stato la tabella non conserva alcun dato che lo store non abbia già, salvo la data di acquisizione: la sua permanenza come tabella distinta è motivata solo dall'essere una mappa storica durevole, indipendente dall'eventuale archiviazione dello store. La scelta fra mantenerla e fonderla nello store è tracciata in OP-25.
 
-  ANSC_AUDIT    Log di ogni chiamata verso ANSC.                    Richiesta, risposta, esito, tempi, operatore; a fini di tracciabilità e GDPR.
-  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ANSC_AUDIT        Log di ogni chiamata verso ANSC.                    Richiesta, risposta, esito, tempi, operatore. Indispensabile alla diagnosi e al canale di supporto, ma conserva integralmente dati di stato civile: è un rischio da governare, non una misura di conformità (cfr. capoverso in calce e OP-10).
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 Lo store di stato non duplica l'intero payload: registra la chiave dell'atto e i discriminanti di tipo (evento/operazione/casistica), e i dati prevalidati sono riletti da SIPO al momento del deposito e della firma. La chiave è locale (anti-doppio-accodamento), non una chiave di deduplica ANSC, che non esiste.
 
 Su Oracle 12.2 non è disponibile il tipo JSON nativo (introdotto dalla versione 21c): gli eventuali campi JSON si memorizzano come CLOB con vincolo «IS JSON». Lo store di stato è letto e aggiornato dal concentratore in modo presidiato (per ufficiale/municipio); non è drenato da un pool di worker. La collocazione della base dati all'esterno del cluster non pregiudica il pattern.
 
-La proposta di default non modifica alcuna tabella d'atto esistente. Qualora si volesse rendere lo stato ANSC dell'atto visibile nelle interrogazioni esistenti, si potrebbe aggiungere una sola colonna «stato_ansc» sulla tabella dell'atto di morte: essendo una modifica all'esistente, resta però una proposta separata da approvare (RNF-8, cfr. OP-11).
+Conservazione dei payload di audit. ANSC_AUDIT conserva in CLOB la richiesta e la risposta integrali di ogni chiamata: sono dati di stato civile, quindi dati personali e in parte particolari. La tracciabilità richiesta dall'Allegato 4 riguarda l'operazione, l'operatore e la postazione, non necessariamente il contenuto dell'atto. Vanno perciò definite, prima dell'esercizio, una politica di conservazione con termine esplicito e cancellazione automatica, la minimizzazione dei payload registrati e la mascheratura dei campi non necessari alla diagnosi; l'accesso all'audit va limitato ai ruoli Auditor e Supporto. Il punto è tracciato in OP-10.
 
+La proposta di default non modifica alcuna tabella d'atto esistente. Qualora si volesse rendere lo stato ANSC dell'atto visibile nelle interrogazioni esistenti, si potrebbe aggiungere una sola colonna «stato_ansc» sulla tabella dell'atto di morte: essendo una modifica all'esistente, resta però una proposta separata da approvare (RNF-7, cfr. OP-11).
+
 ## Struttura dettagliata delle tabelle operative
 
 Le tabelle seguono le convenzioni di SIPO (schema dedicato ANSC_USR, tipi Oracle 12.2). I payload eventuali sono CLOB con vincolo «IS JSON»; il tipo JSON nativo non è disponibile nella versione in uso. Gli identificativi sono NUMBER con sequenza; le date sono TIMESTAMP.
 
-ANSC_OUTBOX --- coda transazionale degli invii.
+ANSC_STATO_ATTO --- store di stato ANSC per atto.
 
-  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Colonna**             **Tipo**                **Note**
-  ----------------------- ----------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  ID_OUTBOX               NUMBER (PK)             Chiave tecnica (sequenza).
+  ----------------------- ----------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ID_STATO_ATTO           NUMBER (PK)             Chiave tecnica (sequenza).
 
   ID_ATTO_SIPO            NUMBER                  Chiave dell'atto in SIPO (aggregato da rileggere).
 
@@ -777,9 +787,9 @@
 
   COD_TIPO_OPERAZIONE     VARCHAR2(20)            CREAZIONE, RETTIFICA, ANNOTAZIONE, ANNULLAMENTO.
 
-  COD_CASISTICA           VARCHAR2(30)            Dichiarazione/trascrizione; corrisponde al codice evento ANSC (Morte_001...020).
+  COD_CASISTICA           VARCHAR2(30)            Casistica SIPO (dichiarazione/trascrizione e variante del caso d'uso); si traduce nel codice evento ANSC tramite COD_EVENTO_ANSC.
 
-  CHIAVE_IDEMPOTENZA      VARCHAR2(64)            Univoca; base della deduplica (PC-4).
+  CHIAVE_ANTI_DUPLICATO   VARCHAR2(64)            Univoca; composta da COD_TIPO_EVENTO + ID_ATTO_SIPO + COD_TIPO_OPERAZIONE (non dalla versione di configurazione, che cambia nel tempo e vanificherebbe il vincolo). Base della difesa locale dal doppio deposito (PC-2).
 
   COD_VERSIONE_CONFIG     VARCHAR2(20)            Versione di configurazione usata in verifica (OP-13).
 
@@ -787,22 +797,28 @@
 
   TIPO_ESITO              VARCHAR2(20)            Esito negativo qualificato: RIFIUTATO (KO validazione ANSC) o INDETERMINATO (timeout su R009/R007 → riconciliazione R005, non retry cieco).
 
-  ID_OPERAZIONE_ANSC      VARCHAR2(50)            Protocollo/identificativo restituito da ANSC.
+  ID_OPERAZIONE_ANSC      VARCHAR2(50)            Identificativo di operazione/protocollo restituito da ANSC (tracciamento della chiamata).
 
+  ID_ANSC                 VARCHAR2(50)            Identificativo nazionale dell'evento (idAnsc) restituito da R009: è il campo distinto restituito da /ansc/deposita-bozza, da non confondere con il protocollo di operazione.
+
   OPERATORE / HOSTNAME    VARCHAR2(40) / (80)     Identità operatore e postazione.
 
+  ID_UFFICIALE            VARCHAR2(40)            Ufficiale competente: con COD_MUNICIPIO e STATO forma l'indice di supervisione.
+
+  COD_MUNICIPIO           VARCHAR2(10)            Municipio di competenza, per l'instradamento della worklist di supervisione.
+
   ULTIMO_ERRORE           VARCHAR2(4000)          Ultimo errore (CLOB se serve maggiore capienza).
 
   DATA_INS / DATA_UPD     TIMESTAMP               Tracciamento.
-  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
-Indici: chiave primaria ID_OUTBOX; indice di supervisione su (COD_MUNICIPIO, ID_UFFICIALE, STATO) per la vista degli atti incompleti per ufficiale; vincolo di unicità locale su CHIAVE_IDEMPOTENZA.
+Indici: chiave primaria ID_STATO_ATTO; indice di supervisione su (COD_MUNICIPIO, ID_UFFICIALE, STATO) per la vista degli atti incompleti per ufficiale; vincolo di unicità locale su CHIAVE_ANTI_DUPLICATO.
 
 ANSC_XREF --- mappa durevole atto SIPO ↔ ANSC.
 
-  ---------------------------------------------------------------------------------------------------
+  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Colonna**                             **Tipo**                **Note**
-  --------------------------------------- ----------------------- -----------------------------------
+  --------------------------------------- ----------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------
   ID_XREF                                 NUMBER (PK)             Chiave tecnica.
 
   ID_ATTO_SIPO                            NUMBER                  Atto SIPO.
@@ -811,30 +827,30 @@
 
   ID_OPERAZIONE_ANSC                      VARCHAR2(50)            Protocollo ANSC assegnato.
 
-  STATO_ANSC                              VARCHAR2(20)            ACQUISITO, REGISTRATO, RIFIUTATO.
+  STATO_ANSC                              VARCHAR2(20)            Stato reale in ANSC (decodifica ANSC_11), stesso vocabolario dello store di stato: CONFERMATO, FIRMATO_DICHIARANTE, FIRMATO_USC, RIFIUTATA, ANNULLATO.
 
   DATA_ACQUISIZIONE                       TIMESTAMP               Momento della conferma.
-  ---------------------------------------------------------------------------------------------------
+  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
-Vincolo di unicità su (ID_ATTO_SIPO, COD_TIPO_OPERAZIONE): è la base della riconciliazione (PC-5).
+Vincolo di unicità su (COD_TIPO_EVENTO, ID_ATTO_SIPO, COD_TIPO_OPERAZIONE): è la base della riconciliazione (PC-5). Il tipo evento è parte della chiave perché gli identificativi d'atto vivono in tabelle distinte per evento (ATTO_DECESSO, ATTO_NASCITA, ...), ciascuna con la propria sequenza: senza di esso due atti di eventi diversi potrebbero collidere.
 
 [^1]ANSC_AUDIT --- traccia delle chiamate.
 
-  --------------------------------------------------------------------------------------
+  ------------------------------------------------------------------------------------------------------------------------------------
   **Colonna**             **Tipo**                   **Note**
-  ----------------------- -------------------------- -----------------------------------
+  ----------------------- -------------------------- ---------------------------------------------------------------------------------
   ID_AUDIT                NUMBER (PK)                Chiave tecnica.
 
-  ID_OUTBOX               NUMBER (FK)                Riferimento all'invio.
+  ID_STATO_ATTO           NUMBER (FK)                Riferimento all'invio.
 
-  FASE                    VARCHAR2(20)               VERIFICA, INVIO, RICONCILIAZIONE.
+  FASE                    VARCHAR2(20)               VERIFICA, ALLEGATI, SOGGETTO, DEPOSITO, FIRMA_DICH, FIRMA_USC, RICONCILIAZIONE.
 
   RICHIESTA / RISPOSTA    CLOB (IS JSON)             Payload inviato e risposta ANSC.
 
   ESITO / DURATA_MS       VARCHAR2(20) / NUMBER      Esito e tempo.
 
   OPERATORE / DATA        VARCHAR2(40) / TIMESTAMP   Chi e quando.
-  --------------------------------------------------------------------------------------
+  ------------------------------------------------------------------------------------------------------------------------------------
 
 **\**
 
@@ -844,9 +860,9 @@
 
 ANSC_CFG_OPERAZIONE --- anagrafica delle operazioni supportate.
 
-  -------------------------------------------------------------------------------------------------------------------------------------
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Colonna**                                 **Tipo**                **Note**
-  ------------------------------------------- ----------------------- -----------------------------------------------------------------
+  ------------------------------------------- ----------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   ID_CFG_OPERAZIONE                           NUMBER (PK)             Chiave tecnica.
 
   COD_TIPO_EVENTO                             VARCHAR2(20)            MORTE, ...
@@ -857,31 +873,31 @@
 
   COD_EVENTO_ANSC                             VARCHAR2(20)            Codice evento ANSC (Morte_001...020).
 
-  SERVIZIO_ANSC                               VARCHAR2(20)            Interfaccia ANSC (es. R002 creazione, R009/R023 validazione).
+  SERVIZIO_ANSC                               VARCHAR2(20)            Interfaccia ANSC dell'operazione (es. R009 per la validazione/deposito dell'evento). R002 è il servizio di certificazione, non di creazione.
 
-  ID_TIPO_DOCUMENTO                           VARCHAR2(20)            idTipodocumento ANSC.
+  ID_TIPO_DOCUMENTO                           VARCHAR2(20)            Identificativo del tipo di documento del canale DMNM/TS (R022/R023): pertinente ai soli casi d'uso alimentati da documentazione sanitaria (Morte_016/017), non al modello evento.
 
   ID_MAPPER                                   VARCHAR2(40)            Strategia di mapping SIPO → ANSC selezionata dal concentratore.
 
   FLG_TRASCRIZIONE                            CHAR(1)                 S/N: valorizza i dati dell'atto di provenienza.
 
-  FLG_FIRMA                                   CHAR(1)                 S/N: l'operazione richiede firma (OP-01).
+  FLG_FIRMA                                   CHAR(1)                 S/N, default «S»: nessun atto è formato senza la firma dell'USC (R007). Il valore «N» resta previsto per eventuali operazioni non soggette a firma.
 
   COD_VERSIONE                                VARCHAR2(20)            Versione della configurazione.
 
   DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA   DATE                    Validità temporale (come le decodifiche).
-  -------------------------------------------------------------------------------------------------------------------------------------
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 ANSC_CFG_CAMPO --- campi obbligatori e mappatura per operazione.
 
-  ----------------------------------------------------------------------------------------------------------------------------------
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Colonna**             **Tipo**                **Note**
-  ----------------------- ----------------------- ----------------------------------------------------------------------------------
+  ----------------------- ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   ID_CFG_CAMPO            NUMBER (PK)             Chiave tecnica.
 
   ID_CFG_OPERAZIONE       NUMBER (FK)             Operazione di riferimento.
 
-  CAMPO_ANSC              VARCHAR2(120)           Percorso del campo nel payload ANSC (es. datiDiMorte.dataMorte, luogo.idComune).
+  CAMPO_ANSC              VARCHAR2(120)           Percorso del campo nel modello evento ANSC (es. evento.datiDiMorte.dataMorte, evento.intestatari\[0\].idNazionalita), nella forma «Binding Object + Binding Field» del mapping ufficiale dei casi d'uso.
 
   CAMPO_SIPO              VARCHAR2(120)           Sorgente SIPO (tabella.campo): doppia funzione, mapping e validazione.
 
@@ -889,22 +905,22 @@
 
   COND_OBBLIGATORIETA     VARCHAR2(200)           Condizione (es. «se trascrizione», «se idStato\<\>200»).
 
-  COD_DECODIFICA_ANSC     VARCHAR2(20)            Decodifica R901 per validare il valore (opzionale).
+  COD_DECODIFICA_ANSC     VARCHAR2(20)            Dizionario ANSC con cui validare il valore (opzionale); il controllo avviene sulle tabelle locali (RF-10).
 
   MESSAGGIO               VARCHAR2(200)           Messaggio in caso di mancanza/errore.
-  ----------------------------------------------------------------------------------------------------------------------------------
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
-Le due tabelle sono versionate insieme (COD_VERSIONE) e hanno validità temporale, come le decodifiche ANSC e SIPO. ANSC_CFG_CAMPO è alimentata dai blocchi obbligatori della validazione ANSC (R023) e dalle decodifiche (R901): l'allineamento nel tempo è tracciato in OP-13.
+Le due tabelle sono versionate insieme (COD_VERSIONE) e hanno validità temporale, come le decodifiche ANSC e SIPO. ANSC_CFG_CAMPO è alimentata dal mapping ufficiale dei casi d'uso pubblicato da ANSC (docs/Mapping_casi_uso/, colonne Obbligatorio, Binding Object, Binding Field, Condizioni obbligatorietà) e dalle decodifiche (R901): l'allineamento nel tempo è tracciato in OP-13.
 
 **Modalità operativa.** Il flusso d'uso della configurazione è il seguente.
 
-1\. Caricamento e cache: il concentratore carica la configurazione valida e la mette in cache, con invalidazione per versione. Fonte primaria: le regole di validazione ANSC (R023) e le decodifiche (R901).
+1\. Caricamento e cache: il concentratore carica la configurazione valida e la mette in cache, con invalidazione per versione. Fonte primaria: il mapping ufficiale dei casi d'uso ANSC e i dizionari ANSC replicati in locale (RF-10).
 
 2\. Determinazione dell'operazione: il front-end invia il tipo operazione, oppure lo si deduce dal tipo atto SIPO (CONF_TIPO_ATTI.mascheraUi → casistica). Il concentratore risolve la riga ANSC_CFG_OPERAZIONE valida.
 
-3\. Verifica (sincrona): letti i campi da ANSC_CFG_CAMPO, il concentratore controlla presenza e validità dei campi (incluse le condizioni) sul payload ricostruito da SIPO; opzionalmente invoca la validazione ANSC. L'esito abilita il «Salva» (RF-4).
+3\. Verifica (sincrona): letti i campi da ANSC_CFG_CAMPO, il concentratore controlla presenza e validità dei campi (incluse le condizioni) sul payload ricostruito da SIPO. Nessun servizio ANSC è invocato in questa fase. L'esito abilita il «Finalizza» (RF-4).
 
-4\. Salva: l'outbox registra chiave, discriminanti (evento/operazione/casistica) e COD_VERSIONE_CONFIG.
+4\. Registrazione dello stato: lo store di stato registra chiave, discriminanti (evento/operazione/casistica) e COD_VERSIONE_CONFIG.
 
 5\. Deposito e firma (presidiati): al deposito (R009) la configurazione della versione registrata seleziona il mapper e materializza il payload da SIPO; la firma (R007) è eseguita dall'ufficiale con l'OTP di sessione. Nessun invio automatico.
 
@@ -915,29 +931,29 @@
   ------------------------------------------------------------------------------------------------------------------
   **Evento**   **Operazione**   **Casistica**     **Evento ANSC**   **Mapper**           **Trascriz.**   **Firma**
   ------------ ---------------- ----------------- ----------------- -------------------- --------------- -----------
-  MORTE        CREAZIONE        DICH_ABITAZIONE   Morte_001         MorteDichiarazione   N               \[OP-01\]
+  MORTE        CREAZIONE        DICH_ABITAZIONE   Morte_001         MorteDichiarazione   N               S
 
   ------------------------------------------------------------------------------------------------------------------
 
-ANSC_CFG_CAMPO (estratto, dai campi obbligatori del luogo del decesso in R023 e dai dati del defunto):
+ANSC_CFG_CAMPO (estratto, dal mapping ufficiale del caso d'uso Morte_001 per il luogo del decesso e i dati del defunto):
 
-  ----------------------------------------------------------------------------------------------------------------
-  **Campo ANSC**                   **Campo SIPO**                         **Obbl.**     **Condizione**
-  -------------------------------- -------------------------------------- ------------- --------------------------
-  luogo.idComune                   ATTO_DECESSO.ID_COMUNE_DECESSO         S             ---
+  ----------------------------------------------------------------------------------------------------------------------------------
+  **Campo ANSC**                                     **Campo SIPO**                         **Obbl.**     **Condizione**
+  -------------------------------------------------- -------------------------------------- ------------- --------------------------
+  evento.datiDiMorte.idComuneMorte                   ATTO_DECESSO.ID_COMUNE_DECESSO         N             se decesso in Italia
 
-  luogo.nomeComune                 (descrizione comune)                   S             ---
+  evento.datiDiMorte.nomeComuneMorte                 (descrizione comune)                   N             se decesso in Italia
 
-  luogo.idStato / nomeStato        (Italia per dichiarazione)             S             ---
+  evento.datiDiMorte.idStatoMorte / nomeStatoMorte   (Italia per dichiarazione)             N             ---
 
-  luogo.comuneEstero               ATTO_DECESSO.LOCALITA_ESTERA_DECESSO   S             se estero / trascrizione
+  evento.datiDiMorte.comuneEstero                    ATTO_DECESSO.LOCALITA_ESTERA_DECESSO   N             se estero / trascrizione
 
-  datiDiMorte.dataMorte            ATTO_DECESSO.DATA_DECESSO              S             ---
+  evento.datiDiMorte.dataMorte                       ATTO_DECESSO.DATA_DECESSO              N             ---
 
-  defunto.cognome / nome / sesso   SOGGETTO                               S             ---
+  evento.intestatari\[0\].nome / sesso               SOGGETTO                               S             ---
 
-  defunto.dataNascita              SOGGETTO                               S             ---
-  ----------------------------------------------------------------------------------------------------------------
+  evento.intestatari\[0\].dataNascita                SOGGETTO                               S             ---
+  ----------------------------------------------------------------------------------------------------------------------------------
 
 # Mappatura del payload e validazione dei campi obbligatori
 
@@ -949,56 +965,244 @@
 
 La tabella mappa i campi principali fra le tabelle SIPO (ATTO_DECESSO, SOGGETTO, ATTO) e i modelli ANSC (ModelDatiDiMorte, ModelSoggetto). È una ricognizione dei campi salienti, non una mappatura esaustiva campo per campo: quest'ultima va completata sull'intero modello evento e sulle regole di validazione ANSC.
 
-  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **Ambito**         **Campo SIPO**                                                        **Campo ANSC**                                                                                       **Note**
-  ------------------ --------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------- -------------------------------------------------------------------
-  Luogo/data morte   ATTO_DECESSO.DATA_DECESSO                                             datiDiMorte.dataMorte (+ anno/mese/giornoMorte)                                                      Data del decesso; componenti derivate.
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Ambito**         **Campo SIPO**                                                        **Campo ANSC**                                                                                                 **Note**
+  ------------------ --------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Luogo/data morte   ATTO_DECESSO.DATA_DECESSO                                             evento.datiDiMorte.dataMorte (+ annoMorte / meseMorte / giornoMorte)                                           Data del decesso; componenti derivate.
 
-  Luogo/data morte   ATTO_DECESSO.ID_ORA_DECESSO                                           datiDiMorte.oraMorte / minutoMorte                                                                   Da decodifica ora.
+  Luogo/data morte   ATTO_DECESSO.DATA_DECESSO (componente oraria)                         evento.datiDiMorte.oraMorte / minutoMorte                                                                      L'orario si ricava da DATA_DECESSO, commentata nel Disegno Base Dati «Data/orario Decesso/Rinvenimento». ID_ORA_DECESSO non è l'ora del decesso: il Disegno Base Dati la definisce «Identificativo del tipo di informazione mancante», quindi qualifica l'informazione assente (ora ignota) e va mappata come tale, non su oraMorte.
 
-  Luogo/data morte   ATTO_DECESSO.ID_COMUNE_DECESSO                                        datiDiMorte.idComuneMorte / nomeComuneMorte (+ idProvinciaMorte / siglaProvinciaMorte)               Comune italiano del decesso; id da tradurre nella codifica ANSC.
+  Luogo/data morte   ATTO_DECESSO.ID_COMUNE_DECESSO                                        evento.datiDiMorte.idComuneMorte / nomeComuneMorte (+ idProvinciaMorte / siglaProvinciaMorte)                  Comune italiano del decesso; l'id va tradotto nella codifica attesa da ANSC. Semantica ristretta: il Disegno Base Dati commenta la colonna «Comune decesso (prima di arrivo in ospedale)» e in ATTO_DECESSO non esiste altra colonna per il comune di decesso; il decesso in struttura è qualificato da ID_OSPEDALE e ID_TIPO_DECESSO.
 
-  Luogo/data morte   ATTO_DECESSO.LOCALITA_ESTERA_DECESSO                                  datiDiMorte.comuneEstero / luogoMorte (+ idStatoMorte / nomeStatoMorte)                              Caso estero; stato secondo tabella ANPR_02.
+  Luogo/data morte   ATTO_DECESSO.LOCALITA_ESTERA_DECESSO                                  evento.datiDiMorte.comuneEstero / luogoMorte (+ idStatoMorte / nomeStatoMorte)                                 Caso estero; stato secondo tabella ANPR_02.
 
-  Luogo/data morte   ATTO_DECESSO.LUOGO_DECESSO / ZONA_DECESSO / DETTAGLIO_LUOGO_DECESSO   datiDiMorte.luogoMorte / indirizzoMorte                                                              Luogo e indirizzo del decesso.
+  Luogo/data morte   ATTO_DECESSO.LUOGO_DECESSO / ZONA_DECESSO / DETTAGLIO_LUOGO_DECESSO   evento.datiDiMorte.luogoMorte / indirizzoMorte                                                                 Tre colonne di testo libero VARCHAR2 (LUOGO_DECESSO «Luogo del decesso (anche ospedale)», ZONA_DECESSO «Descrizione Zona del decesso», DETTAGLIO_LUOGO_DECESSO) verso due campi di testo libero del modello evento: serve una regola esplicita di composizione (cfr. in calce al paragrafo).
 
-  Luogo/data morte   ATTO_DECESSO.FLAG_MORTE_PRESUNTA                                      datiDiMorte.testoDataPresuntaMorte / dataPresuntaMorteDa / ...A                                      Morte presunta: intervallo e testo.
+  Luogo/data morte   ATTO_DECESSO.FLAG_MORTE_PRESUNTA                                      evento.datiDiMorte.testoDataPresuntaMorte / dataPresuntaMorteDa / ...A                                         Morte presunta: intervallo e testo.
 
-  Luogo/data morte   (cadavere non identificato)                                           datiDiMorte.ritrovamento / dataRinvenimentoCadavere                                                  Casistica «Non identificato».
+  Luogo/data morte   (cadavere non identificato)                                           evento.datiDiMorte.ritrovamento / dataRinvenimentoCadavere                                                     Casistica «Non identificato».
 
-  Defunto            SOGGETTO (cognome, nome, sesso)                                       ModelSoggetto.cognome / nome / sesso                                                                 Generalità del defunto.
+  Defunto            SOGGETTO (cognome, nome, sesso)                                       evento.intestatari\[0\].cognome / nome / sesso                                                                 Generalità del defunto.
 
-  Defunto            SOGGETTO (data e luogo nascita)                                       ModelSoggetto.dataNascita, idComuneNascita / nomeComuneNascita, idStatoNascita / nomeStatoNascita    Stato nascita da tabella ANPR_02 (ID=\'200\' = NON ATTRIBUIBILE).
+  Defunto            SOGGETTO (data e luogo nascita)                                       evento.intestatari\[0\].dataNascita, idComuneNascita / nomeComuneNascita, idStatoNascita / nomeStatoNascita    Stato nascita da tabella ANPR_02 (ID=\'200\' = NON ATTRIBUIBILE).
 
-  Defunto            SOGGETTO (cittadinanza, residenza, CF)                                ModelSoggetto.idNazionalita / nazionalita, nomeComuneResidenza / nomeStatoResidenza, codiceFiscale   Cittadinanza e residenza.
+  Defunto            SOGGETTO (cittadinanza, residenza, CF)                                evento.intestatari\[0\].idNazionalita / nazionalita, nomeComuneResidenza / nomeStatoResidenza, codiceFiscale   Cittadinanza e residenza.
 
-  Atto               ATTO (numero, parte, serie, anno)                                     metadati dell'atto / testata                                                                         ANSC assegna proprio protocollo e numeroRicezione.
-  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Atto               ATTO (numero, parte, serie, anno)                                     evento.numeroatto, dataformazione, ora, minuto                                                                 Il numero comunale resta a carico del comune (evento.numeroatto); l'identificativo nazionale è idAnsc, restituito da R009. numeroRicezione non è un protocollo assegnato da ANSC: il modello evento lo descrive come «Numero ricezione documentazione da TS» ed è valorizzato solo nei casi d'uso alimentati da documentazione sanitaria (Morte_016/017).
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 Molti identificativi SIPO (comune, stato, nazionalità) vanno tradotti nella codifica attesa da ANSC, che per gli stati coincide con la tabella ANPR_02. Si richiama il vincolo già noto: la colonna CODICE_ANPR di CONF_STATO_ESTERO è la chiave di traduzione e deve risultare popolata (open point sul popolamento/semantica, coordinato con l'analisi decodifiche).
 
+Normalizzazione del luogo del decesso. In SIPO il luogo del decesso è distribuito su tre colonne di testo libero (LUOGO_DECESSO, ZONA_DECESSO, DETTAGLIO_LUOGO_DECESSO); nel modello evento ANSC i campi corrispondenti --- luogoMorte e indirizzoMorte --- sono anch'essi testo libero e non richiamano alcuna decodifica, mentre il canale DMNM/TS usa una lista codificata (decodifica ANSC_150, «Abitazione», «Istituto di cura», «Hospice», ...). Occorre quindi una regola esplicita che stabilisca quale colonna alimenta luogoMorte e quale indirizzoMorte, come si compongono i valori quando più colonne sono valorizzate e come il testo libero SIPO si riconduce, dove serve, al valore codificato. La definizione della regola è parte di OP-14.
+
 ## Distinzione dichiarazione / trascrizione
 
-La casistica «a Roma» rispetto a «fuori Roma» non cambia soltanto i valori, ma l'operazione ANSC e la porzione di modello valorizzata: la dichiarazione (evento originale formato dal comune) usa i dati evento di morte, la trascrizione (atto formato altrove e trascritto) usa il modello di trascrizione morte e valorizza i dati dell'atto di provenienza --- in SIPO la tabella ATTO_DECESSO_ESTERO per l'estero. Ai due casi corrispondono codici caso d'uso distinti (2.1.0.x contro 2.2.x) ed eventi ANSC distinti (Morte_001...005 contro Morte_009/011/015/020). La conseguenza progettuale è che il concentratore deve selezionare il mapper in base al tipo operazione: è il presupposto del requisito seguente.
+La casistica «a Roma» rispetto a «fuori Roma» non cambia soltanto i valori, ma l'operazione ANSC e la porzione di modello valorizzata: la dichiarazione (evento originale formato dal comune) usa i dati evento di morte, la trascrizione (atto formato altrove e trascritto) usa il modello di trascrizione morte e valorizza i dati dell'atto di provenienza --- in SIPO la tabella ATTO_DECESSO_ESTERO per l'estero. La distinzione non è però leggibile dal codice del caso d'uso: il prefisso 2.1.0.x non coincide con «dichiarazione» né 2.2.x con «trascrizione». La mappa completa dei casi d'uso della morte, ricavata da Decessi_ANSC.xlsx, è la seguente.
 
+  ------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Codice UC**   **Descrizione UC (Decessi_ANSC.xlsx)**                                                                   **Tipologia**         **Codice Motore**
+  --------------- -------------------------------------------------------------------------------------------------------- --------------------- -------------------
+  2.1.0.1         Decesso in abitazione o in luogo pubblico                                                                Dichiarazione         Morte_001
+
+  2.1.0.5         Decesso in abitazione o in luogo pubblico con documentazione da Struttura Sanitaria                      n.d.                  Morte_016
+
+  2.1.0.2         Decesso in ospedale o casa di cura                                                                       Dichiarazione         Morte_002
+
+  2.1.0.6         Decesso in ospedale o casa di cura con documentazione da Struttura Sanitaria                             n.d.                  Morte_017
+
+  2.1.0.3         Decesso in caso di morte violenta                                                                        Dichiarazione         Morte_003
+
+  2.1.0.7         Dichiarazione di morte su avviso di pubblica autorità                                                    n.d.                  Morte_019
+
+  2.1.0.4         Decesso relativo a cadavere rinvenuto non identificato                                                   Dichiarazione         Morte_004
+
+  2.2.1.1         Decesso durante il viaggio in treno o aereo o nave                                                       Dichiarazione         Morte_005
+
+  2.2.1.5         Trascrizione di decesso reso da pubblica autorità                                                        Trascrizione          Morte_018
+
+  2.2.1.6         Trascrizioni di sentenza estera di morte presunta o scomparsa o assenza richiesta da pubblica autorità   n.d.                  Morte_020
+
+  2.2.2.1         Trascrizioni di sentenza dichiarazione di scomparsa per disastri aerei o a bordo di navi                 Dichiarazione         Morte_008
+
+  2.2.2.2         Trascrizione atto di morte pervenuto da comune estero di decesso                                         Trascrizione          Morte_009
+
+  2.2.2.4         Trascrizioni di sentenze di accertamento morte già dichiarata presunta                                   Trascrizione          Morte_011
+
+  2.2.2.5         Trascrizione dichiarazione di morte su decreto del tribunale                                             Trascrizione          Morte_015
+  ------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+Il prefisso del codice UC non determina quindi la tipologia: sono dichiarazioni tanto i casi 2.1.0.1--2.1.0.7 quanto 2.2.1.1 (decesso durante il viaggio) e 2.2.2.1 (sentenza di scomparsa per disastri aerei o navali), mentre 2.2.1.5 è una trascrizione. Per quattro casi d'uso (2.1.0.5, 2.1.0.6, 2.1.0.7 e 2.2.1.6) la colonna Tipologia non è valorizzata nel foglio ed è indicata come n.d. La tipologia va letta dalla configurazione --- COD_CASISTICA e FLG_TRASCRIZIONE di ANSC_CFG_OPERAZIONE --- e non dedotta dal codice. La conseguenza progettuale è che il concentratore deve selezionare il mapper in base al tipo operazione risolto in configurazione: è il presupposto del requisito seguente.
+
 ## Verifica dei campi obbligatori guidata da configurazione (RF-9)
 
 Si introduce un livello di configurazione (metadati) che, dato il tipo di operazione, conosce i campi obbligatori richiesti da ANSC e ne verifica la presenza in fase di «Verifica», prima del deposito (R009) e della firma (R007). Il beneficio è duplice: riduce l'effort perché generalizza a tutti i tipi di atto (non solo la morte) invece di replicare i controlli caso per caso, e anticipa lato SIPO i controlli che altrimenti ANSC restituirebbe come errore, riducendo i round-trip.
 
 ### Necessità della configurazione. 
 
-La configurazione dei campi obbligatori è un pre-filtro che intercetta gli errori sintattici prima di occupare un identificativo nazionale con R009, non un sostituto di R009. Distingue regole replicabili localmente --- struttura, obbligatorietà per caso d'uso, formati, decodifiche cachate via R901 --- da regole non replicabili perché dipendono da stato centrale: esistenza e stato dell'atto collegato formato altrove, adesione ad ANSC del comune destinatario, riconciliazione del soggetto, posizione anagrafica ANPR, unicità della numerazione. Queste ultime restano di competenza esclusiva di R009 e delle consultazioni.
+La configurazione dei campi obbligatori è un pre-filtro che intercetta gli errori sintattici prima di occupare un identificativo nazionale con R009, non un sostituto di R009. Distingue regole replicabili localmente --- struttura, obbligatorietà per caso d'uso, formati, decodifiche replicate in locale (RF-10) --- da regole non replicabili perché dipendono da stato centrale: esistenza e stato dell'atto collegato formato altrove, adesione ad ANSC del comune destinatario, riconciliazione del soggetto, posizione anagrafica ANPR, unicità della numerazione. Queste ultime restano di competenza esclusiva di R009 e delle consultazioni.
 
-Il modello dati di ANSC (model_evento) non dichiara l'obbligatorietà a livello di schema: nel modello i campi sono tutti opzionali. L'obbligatorietà è espressa dal servizio di validazione (R023 / R009), che restituisce esiti strutturati (array di messaggi errors, warnings, infos in ValidazioneDmnmResponse). Ne segue che l'obbligatorietà non è derivabile dal solo modello e va codificata come configurazione, per tipo operazione, allineata alle regole di validazione ANSC.
+Il modello dati di ANSC (model_evento) non dichiara l'obbligatorietà a livello di schema: nel modello i campi sono tutti opzionali. L'obbligatorietà è pubblicata da ANSC nel mapping dei casi d'uso (docs/Mapping_casi_uso/) ed è verificata dal servizio di validazione R009, che restituisce esiti strutturati (array di messaggi errors, warnings, infos). Ne segue che l'obbligatorietà non è derivabile dal solo modello e va codificata come configurazione, per tipo operazione, allineata alle regole di validazione ANSC.
 
-Esempio, dalle regole di validazione ANSC (R023): il luogo del decesso (ModelLuogo) dichiara obbligatori i campi:
+Esempio, dal mapping ufficiale del caso d'uso Morte_001 (219 righe, di cui 38 obbligatorie): per il defunto sono dichiarati obbligatori i campi
 
-idComune, nomeComune, idProvincia, siglaProvincia, idStato, nomeStato, luogo, indirizzo, numeroCivico, comuneEstero;
+evento.intestatari\[0\].nome, sesso, dataNascita, idStatoNascita, nomeStatoNascita, idNazionalita, nazionalita, idstatocivile, descrizionestatocivile;
 
-e la richiesta di validazione (ValidazioneDmnmRequest) richiede numeroRicezione, idTipodocumento e sezioneUfficialeStatoCivile. Questi elenchi sono la fonte diretta per popolare la configurazione dei campi obbligatori per l'evento morte.
+mentre cognome, codiceFiscale, idComuneNascita e i campi di datiDiMorte risultano non obbligatori per quel caso d'uso. Per ogni campo il file dichiara il percorso (Binding Object e Binding Field) e l'eventuale condizione di obbligatorietà: è la fonte diretta per popolare la configurazione dei campi obbligatori. Va tenuto distinto R023, che valida i documenti DMNM provenienti dal Sistema Tessera Sanitaria (schema ValidazioneDmnmRequest, con numeroRicezione, idTipodocumento e sezioneUfficialeStatoCivile) e non è una validazione a vuoto del modello evento.
 
-Una tabella di configurazione --- collocabile in ANSC_USR o riusando il meccanismo delle decodifiche --- associa (tipo operazione, tipo evento) all'elenco dei campi obbligatori. In fase di «Verifica» il concentratore controlla i campi presenti nel payload ricostruito da SIPO contro tale configurazione; l'esito alimenta l'abilitazione del «Salva» (RF-4). La configurazione va mantenuta allineata alle decodifiche e alle regole ANSC (R901 / R023): è un punto di manutenzione, tracciato come open point.
+Una tabella di configurazione --- collocabile in ANSC_USR o riusando il meccanismo delle decodifiche --- associa (tipo operazione, tipo evento) all'elenco dei campi obbligatori. In fase di «Verifica» il concentratore controlla i campi presenti nel payload ricostruito da SIPO contro tale configurazione; l'esito alimenta l'abilitazione del «Finalizza» (RF-4). La configurazione va mantenuta allineata ai dizionari ANSC (aggiornati con il comando di RF-10) e al mapping dei casi d'uso ANSC: è un punto di manutenzione, tracciato come open point.
 
+# Gestione dei dizionari ANSC
+
+ANSC pubblica le proprie tabelle di decodifica --- i dizionari --- attraverso un servizio cooperativo dedicato. I loro valori servono a due consumatori distinti: al pre-filtro locale (RF-9), che deve riconoscere i codici ammessi prima di occupare un identificativo nazionale, e alle maschere di SIPO, che devono presentarli all'operatore. Questo capitolo definisce il componente che li recupera, il comando con cui si aggiornano e il modo in cui SIPO li consuma: è il contenuto del requisito RF-10.
+
+## Che cosa pubblica ANSC e con quale servizio
+
+Il servizio R901 --- «Servizio di configurazione per il reperimento delle tabelle di decodifica» --- espone quattro operazioni, di cui due sono il fondamento del meccanismo di aggiornamento.
+
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Operazione**                           **Che cosa restituisce**                                                                                                                                               **Uso previsto**
+  ---------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  /config/decodifica/elenco                L'elenco delle decodifiche disponibili: per ciascuna identificativo, descrizione (il nome della tabella, ad esempio dec_stato_evento) e versione (ad esempio 1.4.0).   Primo passo di ogni aggiornamento. È il confronto fra la versione dichiarata da ANSC e quella già caricata in locale a determinare che cosa vada scaricato: senza questa operazione l'aggiornamento sarebbe un travaso integrale a ogni esecuzione.
+
+  /config/decodifica/dettaglio             Il contenuto di una singola decodifica: identificativo, formato (csv), compressione (per default attiva) e contenuto, restituito come stringa binaria in base64.       Scarico effettivo della singola tabella. Il componente decodifica il base64, decomprime e interpreta il CSV. Si invoca una volta per ciascuna decodifica risultata disallineata.
+
+  /config/decodifica/data_adesione         La data di adesione ad ANSC di un comune, dato il suo identificativo; risponde 404 se il comune non esiste o non ha ancora aderito.                                    È una consultazione puntuale, un comune alla volta, non un elenco: non è quindi replicabile come dizionario e resta una verifica da eseguire quando serve. È la sola delle regole non replicabili localmente (cap. «Mappatura del payload») per cui esista un servizio dedicato.
+
+  /config/decodifica/usecase-multilingua   L'elenco dei casi d'uso per i quali è supportata la composizione dell'atto in più lingue.                                                                              Fuori dal perimetro del pilota; l'operazione è citata per completezza del contratto.
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+Dimensione del corpus. Il repository pubblica 145 file di decodifica su 143 identificativi distinti, per 1.376 righe di dato complessive; l'elenco effettivo va comunque letto da R901, che è la fonte autoritativa. È un volume che sta comodamente in una tabella Oracle e che non giustifica alcuna infrastruttura di caching dedicata: la replica locale è una tabella, non un servizio di memoria. Di quegli identificativi, 87 sono referenziati dal modello dell'evento (cap. «Vincoli imposti dal contratto di servizio ANSC») e i restanti 56 servono altri servizi cooperativi e le schermate della web app: il componente li scarica tutti, perché la selezione dipende dagli eventi che verranno via via attivati e non conviene legarla al pilota.
+
+Tracciato. Centoquaranta decodifiche su 145 hanno lo stesso tracciato --- identificativo, descrizione, data di inizio e di fine validità, ordinamento --- e sono quindi caricabili in una sola struttura generica. Le eccezioni sono cinque e vanno previste esplicitamente: tre decodifiche (tipo firma, dichiarazione congiunta, ruolo dell'USC) portano le sole colonne di identificativo e descrizione; la decodifica dei casi d'uso aggiunge IDTIPOCONTENUTO e quella dei consolati aggiunge CODICECONSOLATO. Le due colonne aggiuntive si conservano in un attributo JSON, senza moltiplicare le strutture per due soli casi.
+
+Un'ambiguità da sciogliere al primo caricamento. Due identificativi compaiono nel repository con due file ciascuno. Nel caso 135 si tratta di un refuso nel nome del file e il contenuto è identico. Nel caso 134, invece, i due file hanno contenuto diverso: il dichiarante per la trascrizione di nascita e quello per la trascrizione postuma differiscono sul valore 4, che vale «Altro» nel primo e «Tutore» nel secondo. Poiché il carico avviene per identificativo, va verificato sull'elenco restituito da R901 se l'identificativo 134 sia effettivamente unico; per prudenza la chiave locale è presa su identificativo e nome della tabella, non sul solo identificativo.
+
+## Perché un componente dedicato
+
+Verifica preliminare. La funzione non era presente come tale nelle versioni precedenti dell'analisi. Comparivano soltanto due richiami impliciti --- una voce «allineamento decodifiche (R901)» nell'elenco delle attività del processo di automazione e la stessa formula fra le automazioni ammesse --- e un riferimento a R901 come fonte da cui «importare» i campi della configurazione, per di più confuso con il mapping ufficiale dei casi d'uso, che è cosa diversa. Non esistevano né una struttura di destinazione, né un'interfaccia, né un comando: la funzione era nominata, non progettata. Qui viene estratta e resa esplicita, e i due richiami impliciti sono stati riportati a questo capitolo.
+
+Perché è un componente a sé. Il ciclo di vita è diverso da quello del concentratore di formazione: l'aggiornamento dei dizionari è un'operazione di durata non trascurabile, eseguita raramente e su comando, che non deve competere per le risorse di un componente sul cui tempo di risposta l'operatore è in attesa (RNF-4). Diversi sono i consumatori, perché i dizionari servono a tutto SIPO e non al solo componente ANSC. Ed è diverso il dominio di guasto: un aggiornamento fallito non deve in alcun modo impedire la formazione degli atti.
+
+Che cosa il componente non fa. Non detiene la chiave privata del certificato server e non costruisce token. Il vincolo posto al capitolo sull'architettura --- il concentratore all-ansc-sipo è il solo luogo in cui possono risiedere il PKCS#12 e la logica di firma JWT/JWS --- resta intatto: dec-ansc-sipo invoca R901 passando per all-ansc-sipo, con una chiamata REST interna al cluster. È lo stesso schema già in uso in SIPO verso ANPR, dove i moduli dello Stato Civile non parlano con ANPR ma con il concentratore all-anpr-sipo, che traduce e firma. Duplicare la chiave privata in un secondo componente sarebbe un peggioramento netto della postura di sicurezza a fronte di un guadagno nullo.
+
+Conseguenza sulla modalità di autenticazione. R901 è una lettura e come tale rientrerebbe nel perimetro automatizzabile; ma l'ammissibilità della modalità non presidiata non è confermata dalle fonti (OP-23). La scelta del comando manuale rende il disegno indipendente da quell'esito: l'aggiornamento è avviato da un amministratore autenticato e, se ANSC richiedesse comunque l'OTP, l'operazione si svolge entro la sua sessione come qualunque altra chiamata cooperativa. Se OP-23 si chiudesse in senso favorevole, l'aggiunta di una schedulazione sarebbe un'estensione e non una riprogettazione.
+
+Un anti-pattern da non ripetere. Nell'integrazione ANPR esistente i soggetti si allineano ma le tabelle di riferimento no: il servizio di scarico tabelle è dichiarato nel client ma non ha alcun generatore di richiesta né alcun punto di invocazione applicativo, e nessuna procedura aggiorna le tabelle CONF\_\*, caricate una tantum al subentro (cfr. il riferimento R3 e la relativa voce del registro dei punti da verificare). Il risultato è un catalogo che invecchia in silenzio. Il comando descritto in questo capitolo esiste perché lo stesso non accada con ANSC: l'aggiornamento è manuale, ma è previsto, tracciato e verificabile.
+
+## Il comando di aggiornamento (on request)
+
+L'aggiornamento è avviato su richiesta dalla schermata «Dizionari ANSC» del back-office, dal ruolo Amministratore. Non esiste alcuna schedulazione automatica: la periodicità è una decisione organizzativa, tipicamente legata alle comunicazioni di rilascio del fornitore, non un intervallo cablato nel sistema.
+
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Passo**   **Attività**    **Nota**
+  ----------- --------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  1           Avvio           Il comando è eseguito da un amministratore autenticato in SIPO. La chiamata verso ANSC è instradata su all-ansc-sipo, che costruisce e firma il token.
+
+  2           Elenco remoto   /config/decodifica/elenco restituisce, per ogni decodifica, identificativo, nome e versione dichiarata da ANSC.
+
+  3           Confronto       La versione remota è confrontata con quella registrata in locale per la stessa decodifica. Si scaricano solo le decodifiche nuove o di versione diversa; le altre sono contate come invariate. È il passo che rende l'operazione economica.
+
+  4           Scarico         Per ciascuna decodifica da aggiornare, /config/decodifica/dettaglio restituisce il contenuto in base64, compresso per default. Il componente decodifica, decomprime e interpreta il CSV, gestendo i cinque tracciati anomali descritti sopra.
+
+  5           Carico          Per ogni decodifica, in una transazione propria: sostituzione integrale dei valori e aggiornamento della riga di catalogo con la nuova versione. La granularità per decodifica evita che l'errore su una tabella lasci l'intero dizionario in stato incoerente.
+
+  6           Esito           Una riga di caricamento registra operatore, istante di inizio e di fine e i conteggi: esaminate, aggiornate, invariate, in errore. L'elenco delle decodifiche in errore resta consultabile per la diagnosi.
+
+  7           Ripetibilità    Il comando è ripetibile senza effetti collaterali: alla seconda esecuzione le decodifiche già allineate risultano invariate e non vengono riscaricate. Un aggiornamento interrotto si riprende semplicemente rieseguendolo.
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+Sono previste tre modalità d'uso.
+
+Aggiornamento completo: il caso ordinario, esamina tutte le decodifiche pubblicate.
+
+Aggiornamento selettivo: una o più decodifiche indicate per identificativo, utile quando il fornitore comunica la modifica di una tabella specifica.
+
+Simulazione: esegue il confronto e mostra il differenziale --- quali decodifiche cambierebbero e da quale versione a quale --- senza applicare nulla. È la modalità con cui valutare l'impatto prima di aggiornare in esercizio.
+
+Un aggiornamento non interferisce con la formazione degli atti in corso: la sostituzione avviene per singola decodifica e i lettori continuano a vedere i valori precedenti fino al commit. La validità temporale pubblicata da ANSC --- data di inizio e di fine validità di ciascun valore --- è conservata così com'è, senza reinterpretazioni locali: è il consumatore ad applicarla in lettura.
+
+## Modello dati dei dizionari
+
+Le strutture sono tre, tutte nuove e collocate in ANSC_USR come il resto del componente, più una vista per la fruizione. Valgono le convenzioni già adottate al capitolo «Modello dati»: Oracle 12.2, identificativi con colonne IDENTITY, JSON come CLOB con vincolo «IS JSON».
+
+ANSC_DIZIONARIO --- catalogo delle decodifiche replicate.
+
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Colonna**                                **Tipo**                   **Note**
+  ------------------------------------------ -------------------------- -----------------------------------------------------------------------------------------------------------------------------------------
+  ID_DIZIONARIO                              NUMBER (PK)                Chiave tecnica.
+
+  ID_DECODIFICA                              VARCHAR2(20)               Identificativo della tabella secondo R901 (es. 11).
+
+  NOME                                       VARCHAR2(100)              Nome della tabella restituito da R901 (es. dec_stato_evento). Con ID_DECODIFICA forma la chiave logica.
+
+  COD_DECODIFICA_ANSC                        VARCHAR2(20)               Codice nella forma usata dal modello evento e dalla configurazione (es. ANSC_11): è il raccordo con ANSC_CFG_CAMPO.COD_DECODIFICA_ANSC.
+
+  VERSIONE_ANSC                              VARCHAR2(20)               Versione dichiarata da ANSC nell'elenco: è il termine di confronto che decide se scaricare.
+
+  NUM_VALORI                                 NUMBER                     Numero di valori caricati, per controllo a colpo d'occhio.
+
+  DATA_ULTIMO_CARICO / ESITO_ULTIMO_CARICO   TIMESTAMP / VARCHAR2(20)   Quando e con quale esito (AGGIORNATA, INVARIATA, ERRORE).
+
+  DATA_INS / DATA_UPD                        TIMESTAMP                  Tracciamento.
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+ANSC_DIZIONARIO_VALORE --- i valori di ciascuna decodifica.
+
+  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Colonna**                                 **Tipo**                **Note**
+  ------------------------------------------- ----------------------- ---------------------------------------------------------------------------------------------------------------------------------
+  ID_VALORE                                   NUMBER (PK)             Chiave tecnica.
+
+  ID_DIZIONARIO                               NUMBER (FK)             Decodifica di appartenenza.
+
+  CODICE                                      VARCHAR2(20)            Il valore codificato (colonna ID del tracciato ANSC).
+
+  DESCRIZIONE                                 VARCHAR2(500)           Descrizione pubblicata. La più lunga nel corpus attuale misura 286 caratteri: la capienza è dimensionata con margine.
+
+  DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA   DATE                    Validità temporale come pubblicata da ANSC; i valori cessati restano in tabella.
+
+  ORDINAMENTO                                 NUMBER                  Ordine di presentazione suggerito da ANSC.
+
+  ATTRIBUTI                                   CLOB (IS JSON)          Colonne aggiuntive delle sole decodifiche che le prevedono (IDTIPOCONTENUTO per i casi d'uso, CODICECONSOLATO per i consolati).
+  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+ANSC_DIZIONARIO_CARICAMENTO --- storico dei comandi eseguiti.
+
+  -----------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Colonna**                                                   **Tipo**                **Note**
+  ------------------------------------------------------------- ----------------------- ---------------------------------------------------------------------
+  ID_CARICAMENTO                                                NUMBER (PK)             Chiave tecnica.
+
+  MODALITA                                                      VARCHAR2(20)            COMPLETO, SELETTIVO o SIMULAZIONE.
+
+  OPERATORE                                                     VARCHAR2(40)            Chi ha impartito il comando: l'operazione è manuale e va imputata.
+
+  DATA_INIZIO / DATA_FINE                                       TIMESTAMP               Durata effettiva dell'esecuzione.
+
+  NUM_ESAMINATE / NUM_AGGIORNATE / NUM_INVARIATE / NUM_ERRORE   NUMBER                  I conteggi che rendono leggibile l'esito senza aprire il dettaglio.
+
+  ESITO                                                         VARCHAR2(20)            OK, PARZIALE (qualche decodifica in errore) o KO.
+
+  DETTAGLIO_ERRORI                                              CLOB (IS JSON)          Elenco delle decodifiche non caricate, con il motivo.
+  -----------------------------------------------------------------------------------------------------------------------------------------------------------
+
+La vista V_ANSC_DIZIONARIO_VALIDO espone il join fra catalogo e valori limitato ai valori in corso di validità: è il punto di accesso ordinario per SIPO, e la ragione per cui i consumatori non devono conoscere la regola sulla validità temporale. Il DDL completo è in Appendice A.
+
+## Fruizione da parte di SIPO
+
+Il contratto verso SIPO è la base dati, non un'interfaccia applicativa. È la scelta coerente con il modo in cui SIPO già lavora: le maschere ottengono comuni, province, stati e località interrogando tabelle locali, e i moduli dello Stato Civile raggiungono le tabelle anagrafiche di ANAG_USR per sinonimo, senza che ciò comporti una dipendenza applicativa fra moduli. Allo stesso modo i dizionari ANSC sono esposti da ANSC_USR attraverso la vista di sola lettura, e raggiunti dai moduli per sinonimo e con grant di sola lettura. Gli endpoint REST descritti in Appendice B servono al back-office e alla diagnosi, non sono la via di consumo delle maschere.
+
+Tre precisazioni sono necessarie perché il capitolo non venga letto per più di quanto dice.
+
+I dizionari ANSC non sostituiscono le tabelle CONF\_\* di SIPO e non ne modificano il contenuto (RNF-7): sono un catalogo aggiuntivo che convive con quello esistente. Quali maschere debbano passare a leggere da qui, e con quale raccordo con le CONF\_\* corrispondenti dove una corrispondenza esiste, è una decisione funzionale che eccede il pilota ed è tracciata in OP-26.
+
+Comuni, province, stati e nazionalità non arrivano da qui. R901 non pubblica quei cataloghi: la titolarità del dato è di ANPR e in SIPO risiedono in ANAG_USR. Resta quindi valido quanto detto al capitolo sulla mappatura: la traduzione degli stati passa per CONF_STATO_ESTERO.CODICE_ANPR.
+
+La validità temporale va sempre applicata in lettura. I valori cessati restano nel dizionario, perché servono a interpretare gli atti già formati; una lettura che li ignorasse li proporrebbe all'operatore come ancora scegliibili. Per questo la fruizione ordinaria avviene sulla vista e non sulla tabella dei valori.
+
+Effetto sul pre-filtro. Con i dizionari replicati in locale, il controllo di RF-9 sui campi che portano COD_DECODIFICA_ANSC diventa una verifica in base dati, senza alcuna chiamata verso ANSC: è ciò che consente al pre-filtro di restare, come richiesto dal requisito, puramente locale.
+
 # Modello di esecuzione: percorso presidiato in SIPO e sessione OTP
 
 Il capitolo definisce come SIPO forma gli atti verso ANSC. Il principio è SIPO-centrico: l'operatore lavora nelle maschere SIPO esistenti; l'integrazione con ANSC è un passo di finalizzazione dell'atto, non un sottosistema attorno a cui riorganizzare il lavoro. Il vincolo presidiato (deposito che consuma un id nazionale, firma per singolo atto con OTP) è rispettato innestandolo nel flusso SIPO, non spostando l'operatore altrove.
@@ -1009,9 +1213,9 @@
 
 ## Percorso ordinario: dentro SIPO
 
-Il percorso ordinario resta nelle maschere SIPO. L'operatore compila e «definisce» l'atto come oggi; alla finalizzazione, se la sessione OTP è attiva, il concentratore esegue in modo per lo più sincrono: pre-filtro locale (RF-9) → R009 (deposito della bozza, con assegnazione di idAnsc) → eventuale attesa della verifica degli allegati (R001) → R007 firma dell'USC (con l'OTP di sessione) → atto formato. L'esito (protocollo/idAnsc, numero comunale) è mostrato nella stessa maschera SIPO.
+Il percorso ordinario resta nelle maschere SIPO. L'operatore compila e «definisce» l'atto come oggi; alla finalizzazione, se la sessione OTP è attiva, il concentratore esegue in modo per lo più sincrono: pre-filtro locale (RF-9) → R001 (invio e verifica degli allegati) → R005 (consultazione del soggetto) → R009 (deposito della bozza, con assegnazione di idAnsc) → R006 (firma del dichiarante) → R007 (firma dell'USC, con l'OTP di sessione) → atto formato. L'esito (protocollo/idAnsc, numero comunale) è mostrato nella stessa maschera SIPO.
 
-Lo stato ANSC è un attributo dell'atto SIPO. ANSC_OUTBOX si conserva come struttura, ma è uno store di stato per atto (una riga per atto×operazione) con gli stati del ciclo di vita reale in ANSC (decodifica ANSC_11: CONFERMATO dopo la validazione R009, FIRMATO DA DICHIARANTE dopo R006, FIRMATO DA USC dopo R007; RIFIUTATA su KO di validazione, ANNULLATO via R011), oltre allo stato locale IN_PREPARAZIONE prima dell'invio. Non è una coda di trasporto. La lista degli atti non ancora completati è una vista di supervisione su questo store.
+Lo stato ANSC è un attributo dell'atto SIPO. ANSC_STATO_ATTO si conserva come struttura, ma è uno store di stato per atto (una riga per atto×operazione) con gli stati del ciclo di vita reale in ANSC (decodifica ANSC_11: CONFERMATO dopo la validazione R009, FIRMATO DA DICHIARANTE dopo R006, FIRMATO DA USC dopo R007; RIFIUTATA su KO di validazione, ANNULLATO via R011), oltre allo stato locale IN_PREPARAZIONE prima dell'invio. Non è una coda di trasporto. La lista degli atti non ancora completati è una vista di supervisione su questo store.
 
 ![](media/image3.png){width="6.4in" height="4.095999562554681in"}
 
@@ -1035,7 +1239,7 @@
 
 ## Il passo «Finalizza»: interazione UX e ruolo del back-end
 
-Nella maschera SIPO l'operatore dispone di un pulsante «Verifica» che esegue il pre-filtro locale (RF-9); se l'esito è positivo si abilita il pulsante «Finalizza». La finalizzazione avvia la sequenza presidiata verso ANSC (deposito R009, eventuale attesa allegati R001, firma R007). La domanda operativa è dove collocare la logica di accesso ad ANSC: direttamente nella UX o in una funzione dedicata di back-end.
+Nella maschera SIPO l'operatore dispone di un pulsante «Verifica» che esegue il pre-filtro locale (RF-9); se l'esito è positivo si abilita il pulsante «Finalizza». La finalizzazione avvia la sequenza presidiata verso ANSC (allegati R001, soggetto R005, deposito R009, firma dichiarante R006, firma USC R007). La domanda operativa è dove collocare la logica di accesso ad ANSC: direttamente nella UX o in una funzione dedicata di back-end.
 
 [^2]I due passaggi che restano in UX derivano dal fatto che ANSC prevede due segreti distinti, entrambi legati all'operatore fisico:
 
@@ -1048,9 +1252,9 @@
 
 2\) Se non c'è un OTP di sessione valido, il concentratore risponde «autenticazione richiesta» e il front-end apre la web app OTP di ANSC (nuova finestra); l'USC si autentica, copia il codice OTP e lo incolla in SIPO, che lo inoltra al concentratore.
 
-3\) Il concentratore, con il JWT firmato lato server, esegue R009 (deposito bozza, idAnsc) ed eventualmente attende la verifica degli allegati (R001).
+3\) Il concentratore, con il JWT firmato lato server, esegue nell'ordine R001 (invio e verifica degli allegati), R005 (consultazione del soggetto) e R009 (deposito bozza, idAnsc).
 
-4\) Per la firma, SIPO raccoglie Utenza/PIN/OTP Provider e il concentratore invoca R007.
+4\) Per la firma, acquisita la firma del dichiarante (R006), SIPO raccoglie Utenza/PIN/OTP Provider e il concentratore invoca R007.
 
 5\) Ad atto formato, protocollo e numero comunale sono restituiti alla maschera. Il front-end non dialoga mai con ANSC.
 
@@ -1078,7 +1282,7 @@
 
 ## Errori in fase di formazione e logiche di recupero
 
-La formazione dell'atto attraversa più servizi cooperativi in sequenza (R001 → R005 → R009 → R006 → R007), ciascuno dei quali può fallire. Poiché ogni passo che va a buon fine avanza lo stato reale dell'atto in ANSC (ed R009 consuma un identificativo nazionale), la gestione degli errori non è un ritentativo cieco ma una ripresa dallo stato raggiunto. Questo capitolo classifica gli errori per fase e definisce le logiche di recupero sulla base di quanto evinto dalla documentazione in nostro possessp.
+La formazione dell'atto attraversa più servizi cooperativi in sequenza (R001 → R005 → R009 → R006 → R007), ciascuno dei quali può fallire. Poiché ogni passo che va a buon fine avanza lo stato reale dell'atto in ANSC (ed R009 consuma un identificativo nazionale), la gestione degli errori non è un ritentativo cieco ma una ripresa dallo stato raggiunto. Questo capitolo classifica gli errori per fase e definisce le logiche di recupero sulla base di quanto evinto dalla documentazione in nostro possesso.
 
 ### Struttura dell'esito ANSC
 
@@ -1142,7 +1346,7 @@
   Non risolvibile allo sportello                                                        Coda di supervisione (dead-letter presidiata) per l'ufficiale competente; nessun ritentativo automatico della formazione.
   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
-ANSC_OUTBOX.STATO è il campo che riflette lo stato reale (decodifica ANSC_11) e TIPO_ESITO distingue il rifiuto di business (RIFIUTATA) dall'esito indeterminato (timeout tecnico); ULTIMO_ERRORE conserva code e text del messaggio ANSC (es. 406002). ANSC_AUDIT registra richiesta e risposta di ogni chiamata, indispensabile alla diagnosi e al canale di supporto Sogei (che richiede header Authorization/JWS, IP pubblico, body).
+ANSC_STATO_ATTO.STATO è il campo che riflette lo stato reale (decodifica ANSC_11) e TIPO_ESITO distingue il rifiuto di business (RIFIUTATA) dall'esito indeterminato (timeout tecnico); ULTIMO_ERRORE conserva code e text del messaggio ANSC (es. 406002). ANSC_AUDIT registra richiesta e risposta di ogni chiamata, indispensabile alla diagnosi e al canale di supporto Sogei (che richiede header Authorization/JWS, IP pubblico, body).
 
 ### Fallback: registro di emergenza
 
@@ -1150,11 +1354,11 @@
 
 ## Automazione dove è ammessa
 
-Resta una componente non presidiata, ma con perimetro esplicito e coerente con l'Allegato 4 (letture e code, che non mutano lo stato degli atti): polling delle notifiche (R008), reminder (R021), richieste di estratti dei cittadini (R024), allineamento delle decodifiche (R901), consultazioni in lettura (R004, R005, R018). È l'unico ambito in cui outbox, scheduling e retry conservano senso pieno. Questa possibilità deve essere analizzata nel dettaglio per verificarne la reale necessità e l'opportunità quindi di essere inserita come funzione nel BackOffice
+Resta una componente non presidiata, ma con perimetro esplicito e coerente con l'Allegato 4 (letture e code, che non mutano lo stato degli atti): polling delle notifiche (R008), reminder (R021), gestione delle richieste dei cittadini (R024: /elenco e /dettaglio sono letture, /aggiorna è una scrittura sulla richiesta, non sull'atto), consultazioni in lettura (R004, R005). L'aggiornamento dei dizionari (R901) non rientra in questo elenco: è un comando manuale, descritto al capitolo «Gestione dei dizionari ANSC». L'uso di queste letture senza l'OTP del singolo operatore è un assunto da verificare: la nota tecnica JWT ANSC elenca l'attributo otp fra quelli del payload del token senza dichiararne l'opzionalità, e l'Allegato 4 del D.M. non è disponibile nel repository (OP-23). È l'unico ambito in cui code di lavoro, scheduling e retry conservano senso. Questa possibilità deve essere analizzata nel dettaglio per verificarne la reale necessità e l'opportunità quindi di essere inserita come funzione nel BackOffice
 
 ## Differimento per caso d'uso, non come modalità
 
-Un eventuale differimento non è una modalità generale ma una proprietà del singolo caso d'uso, vincolata ai termini di legge della tipologia: l'atto di morte non prevede alcuna forma di differimento per i permessi di seppellimento, la nascita ha una finestra stretta, cittadinanza e trascrizioni sono più elastiche. In nessun caso comunque può eccedere la sessione OTP dell'operatore.[^8]
+Un eventuale differimento non è una modalità generale ma una proprietà del singolo caso d'uso, vincolata ai termini di legge della tipologia: l'atto di morte è il caso più stretto, perché da esso dipende il rilascio del permesso di seppellimento; la nascita ha una finestra breve; cittadinanza e trascrizioni sono più elastiche. I termini applicabili per tipologia sono quelli del D.P.R. 396/2000 e vanno verificati puntualmente in sede di specifica. Il differimento riguarda il momento in cui l'atto viene formato, non la durata di una singola sessione di lavoro: ogni sessione di formazione si esaurisce entro la validità dell'OTP (quattro ore) e una formazione differita apre semplicemente una nuova sessione.[^8]
 
 # Decisioni architetturali proposte
 
@@ -1206,81 +1410,89 @@
 
 La nuova componente, essendo nativa per il cloud, va disegnata evitando esplicitamente gli anti-pattern riscontrati nell'integrazione ANPR esistente e documentati nell'analisi di riferimento.
 
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Aspetto**                          **Indicazione**
-  ------------------------------------ -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  Ambiente di esecuzione               L'ambiente (collaudo, esercizio) va risolto da configurazione esterna, mai cablato nel codice. Nell'integrazione ANPR l'ambiente risulta forzato a un valore fisso: da non replicare.
+  ------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Ambiente di esecuzione               L'ambiente SIPO (sviluppo, test, esercizio) e l'endpoint ANSC corrispondente vanno risolti da configurazione esterna, mai cablati nel codice. Nell'integrazione ANPR l'ambiente risulta forzato a un valore fisso: da non replicare.
 
   Segreti                              Credenziali e certificati vanno gestiti con un meccanismo dedicato (secret manager o segreti di piattaforma), non versionati nel repository. Nell'integrazione ANPR le credenziali risultano nel codice: da non replicare (cfr. OP-06).
 
   Gestione errori                      Ogni esito verso ANSC va registrato in audit. Gli esiti negativi non si ritentano ciecamente: RIFIUTATO (KO validazione) richiede correzione presidiata; INDETERMINATO (timeout) richiede riconciliazione R005 ed eventuale R011. Da evitare il silenziamento degli errori riscontrato in ANPR.
 
-  Tracciabilità                        Ogni operazione va tracciata con l'identità dell'operatore e della postazione, sul modello già adottato verso ANPR, con conservazione conforme alle esigenze di audit e privacy (OP-10).
+  Tracciabilità                        Ogni operazione va tracciata con l'identità dell'operatore e della postazione, sul modello già adottato verso ANPR. La traccia include richiesta e risposta integrali verso ANSC, quindi dati di stato civile: servono termine di conservazione esplicito, minimizzazione dei payload registrati, mascheratura dei campi non necessari alla diagnosi e accesso limitato ai ruoli Auditor e Supporto (OP-10).
 
   Certificati di postazione / server   Gestione del certificato di postazione e, nel pattern Roma, del certificato server unico: emissione, rinnovo, distribuzione e associazione postazione ↔ identificativo ANPR (registro postazioni), presidiata dall'audit (obbligo Allegato 4).
 
   Sessione OTP                         L'OTP (validità 4 ore) è materiale di sessione, non un segreto statico: acquisito dalla web app ANSC, propagato nel JWT, mai persistito oltre la sessione; gestione esplicita di scadenza e rigenerazione.
 
   Tracciamento postazione              L'audit deve reggere il tracciamento postazione ↔ identificativo previsto dall'Allegato 4: acquisisce rilevanza normativa, non solo diagnostica.
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 # Registro degli Open Point
 
 Elenco delle questioni aperte, da chiudere con la committenza (Comune di Roma) e con il fornitore di ANSC prima del consolidamento delle specifiche.
 
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| **\#** | **Tema**                                            | **Questione**                                                                                                                                                                                                                                                                                                            | **Owner**                | **Priorità** |
-+:=======+:====================================================+==========================================================================================================================================================================================================================================================================================================================+==========================+==============+
-| OP-01  | Firma digitale                                      | Aperta. La firma dell'USC è richiesta per la formazione dell'atto (R007 /firma_usc), è per singolo atto e richiede OTP (ParametriFirma.inputFirma3): non è automatizzabile da un processo non presidiato.                                                                                                                | Aperto                   | Alta         |
-|        |                                                     |                                                                                                                                                                                                                                                                                                                          |                          |              |
-|        |                                                     | La firma è un argomento che deve essere ancora approfondito ma al momento risultano due possibilità:                                                                                                                                                                                                                     |                          |              |
-|        |                                                     |                                                                                                                                                                                                                                                                                                                          |                          |              |
-|        |                                                     | 1)  Firma olografa (su carta ) e scansione pdf                                                                                                                                                                                                                                                                           |                          |              |
-|        |                                                     |                                                                                                                                                                                                                                                                                                                          |                          |              |
-|        |                                                     | 2)  Formazione atto da firmare digitalmente                                                                                                                                                                                                                                                                              |                          |              |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-02  | Idempotenza ANSC                                    | ANSC non espone una chiave di idempotenza: idOperazioneComune è «l'identificativo dell'operazione scelto dal comune» (base_servizi), per tracciamento, non dichiarato come chiave di deduplica lato ANSC. La difesa dai duplicati è la riconciliazione (R005) + R011.                                                    | aperto                   | ---          |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-03  | Notifiche ANSC                                      | CHIUSO. R008 è il servizio cooperativo di notifica verso i comuni; il suo consumo (polling) è un'attività di lettura, ammessa in modalità non presidiata.                                                                                                                                                                | Fornitore ANSC           | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-04  | Ritorno esito in SIPO                               | L'operatore deve poter vedere lo stato e il protocollo ANSC? Serve una maschera di monitoraggio dei sospesi/falliti?                                                                                                                                                                                                     | Cliente                  | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-05  | Egress verso ANSC                                   | Rete di uscita (internet, PDND, rete governativa), autenticazione (mTLS/OAuth), eventuale IP sorgente fisso, proxy. ANSC identifica il chiamante anche dall'indirizzo IP pubblico di uscita (richiesto nel canale di supporto): serve un egress con IP sorgente stabile/prevedibile.                                     | Architetti di sistema    | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-06  | Gestione segreti                                    | Meccanismo per credenziali e certificati (secret manager o segreti di piattaforma). Questione già segnalata e da non sottovalutare.                                                                                                                                                                                      | Cliente / Architetti     | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-07  | Piattaforma Kubernetes                              | Distribuzione (es. OpenShift), ingress, politiche di egress, CI/CD, registry. Non in carico all'analisi, ma prerequisito realizzativo.                                                                                                                                                                                   | Architetti di sistema    | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-08  | Ordinamento invii                                   | È sufficiente l'ordine per singolo aggregato (atto/soggetto)? Rilevante quando si aggiungeranno le annotazioni.                                                                                                                                                                                                          | Analisi                  | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-09  | Ambienti ANSC                                       | Disponibilità di collaudo ed esercizio, credenziali, onboarding e certificati.                                                                                                                                                                                                                                           | Cliente / ANSC           | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-10  | Audit e privacy                                     | Tracciamento dell'operatore, conservazione dei log, base giuridica per il trattamento dei dati d'atto.                                                                                                                                                                                                                   | Cliente / DPO            | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-11  | Modifica tabella atto                               | Eventuale aggiunta della colonna «stato_ansc» sulla tabella dell'atto di morte: è modifica all'esistente, quindi proposta a parte.                                                                                                                                                                                       | Settore tecnico          | Bassa        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-12  | Semantica di consegna                               | RIFORMULATO (perde l'oggetto originario sulla semantica di consegna). Diventa: politica di trattamento degli esiti indeterminati (timeout su R009/R007) --- mai retry cieco; prima riconciliazione via R005, poi eventuale R011 sul duplicato.                                                                           | Analisi                  | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-13  | Configurazione campi obbligatori                    | Allineamento della configurazione dei campi obbligatori alle regole di validazione ANSC (R023) e alle decodifiche (R901): fonte, formato e processo di aggiornamento nel tempo.                                                                                                                                          | Analisi / Fornitore ANSC | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-14  | Mappatura campi SIPO ↔ ANSC e obbligatorietà        | Completare la mappatura campo-per-campo fra le tabelle SIPO e il modello evento ANSC, per ogni evento/operazione/casistica, con l\'obbligatorietà e le condizioni. Alimenta la Configurazione (ANSC_CFG_CAMPO) e la pre-verifica (RF-9). La ricognizione del capitolo «Mappatura del payload» è parziale (pilota morte). | Analisi / Fornitore ANSC | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-15  | Utenza tecnica e certificato server Roma            | Modalità operativa concordata con Sogei per l'utenza tecnica e il certificato server di Roma, incluso il chiarimento dell'ambiguità del D.M. (Allegato 4): il claim x5c in M2M indica il certificato server, ma il decreto ripete che token e payload sono firmati con il certificato di postazione.                     | Cliente / Sogei          | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-16  | Registro delle postazioni autorizzate (scala Roma)  | Dimensionamento e governo del registro postazione↔identificativo (codice attribuito da ANPR) su scala Roma, con l'associazione postazione fisica ↔ identificativo richiesta dall'Allegato 4.                                                                                                                             | Cliente / Architetti     | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-17  | Limiti di rate / fair use                           | Verifica di eventuali limiti di rate o soglie di fair use sui servizi cooperativi, non documentati nelle specifiche pubbliche.                                                                                                                                                                                           | Fornitore ANSC           | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-18  | Accreditamento come software house                  | Roma, sviluppando in proprio, assume il ruolo di software house nel canale di supporto ANSC: popolamento di nomeApplicativo/versioneApplicativo/fornitoreApplicativo (testata richiesta) e uso del piano di test pubblicato come riferimento per la preproduzione.                                                       | Cliente / Sogei          | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-19  | Semantica dell'esito KO di R009                     | Un esito KO della validazione R009 consuma un idAnsc / persiste un evento in stato RIFIUTATA, oppure è solo una risposta d'errore senza deposito? Incide su numerazione, bonifica e conteggio dei rifiuti.                                                                                                               | Fornitore ANSC           | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-20  | Riconciliazione del soggetto (R005/R018)            | Per il pilota morte il soggetto è assunto già presente/allineato in ANSC, o va prevista la riconciliazione R018 nel flusso? Definisce un ramo di errore in fase R005.                                                                                                                                                    | Analisi / Cliente        | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-21  | Uso del forcingCode                                 | Il codice di forzatura per eventi anomali (R009) va esposto all'operatore (forzatura presidiata) o tenuto fuori scope nel pilota? Implica responsabilità e tracciamento dedicati.                                                                                                                                        | Cliente / ANSC           | Media        |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
-| OP-22  | Ripartizione delle responsabilità tra ruoli (firma) | Chi, tra i ruoli del back-office/sportello, è abilitato a firmare l'atto (R007) e a riprendere la lavorazione: dipende dall'organizzazione degli uffici di Roma e da eventuali deleghe di firma. Da definire con il cliente; incide sulla matrice ruoli×azioni della vista di supervisione.                              | Cliente                  | Alta         |
-+--------+-----------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------+
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| **\#** | **Tema**                                                       | **Questione**                                                                                                                                                                                                                                                                                                                                                                                                                                          | **Stato**   | **Owner**                 | **Priorità** |
++:=======+:===============================================================+========================================================================================================================================================================================================================================================================================================================================================================================================================================================+=============+===========================+==============+
+| OP-01  | Firma digitale                                                 | La firma dell'USC è richiesta per la formazione dell'atto (R007 /firma_usc), è per singolo atto e richiede OTP (ParametriFirma.inputFirma3): non è automatizzabile da un processo non presidiato.                                                                                                                                                                                                                                                      | Aperto      | Cliente / Sogei           | Alta         |
+|        |                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                        |             |                           |              |
+|        |                                                                | La firma è un argomento che deve essere ancora approfondito ma al momento risultano due possibilità:                                                                                                                                                                                                                                                                                                                                                   |             |                           |              |
+|        |                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                        |             |                           |              |
+|        |                                                                | 1)  Firma olografa (su carta ) e scansione pdf                                                                                                                                                                                                                                                                                                                                                                                                         |             |                           |              |
+|        |                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                        |             |                           |              |
+|        |                                                                | 2)  Formazione atto da firmare digitalmente                                                                                                                                                                                                                                                                                                                                                                                                            |             |                           |              |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-02  | Idempotenza ANSC                                               | ANSC non espone una chiave di idempotenza: idOperazioneComune è «l'identificativo dell'operazione scelto dal comune» (base_servizi), per tracciamento, non dichiarato come chiave di deduplica lato ANSC. La difesa dai duplicati è la riconciliazione (R005) + R011.                                                                                                                                                                                  | Chiuso      | Analisi                   | ---          |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-03  | Notifiche ANSC                                                 | R008 è il servizio cooperativo di notifica verso i comuni; il suo consumo (polling) è un'attività di lettura, ammessa in modalità non presidiata.                                                                                                                                                                                                                                                                                                      | Chiuso      | Fornitore ANSC            | ---          |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-04  | Ritorno esito in SIPO                                          | L'operatore deve poter vedere lo stato e il protocollo ANSC? Serve una maschera di monitoraggio dei sospesi/falliti?                                                                                                                                                                                                                                                                                                                                   | Aperto      | Cliente                   | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-05  | Egress verso ANSC                                              | Rete di uscita (internet, PDND, rete governativa), autenticazione (mTLS/OAuth), eventuale IP sorgente fisso, proxy. ANSC identifica il chiamante anche dall'indirizzo IP pubblico di uscita (richiesto nel canale di supporto): serve un egress con IP sorgente stabile/prevedibile.                                                                                                                                                                   | Aperto      | Architetti di sistema     | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-06  | Gestione segreti                                               | Meccanismo per credenziali e certificati (secret manager o segreti di piattaforma). Questione già segnalata e da non sottovalutare.                                                                                                                                                                                                                                                                                                                    | Aperto      | Cliente / Architetti      | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-07  | Piattaforma Kubernetes                                         | Distribuzione (es. OpenShift), ingress, politiche di egress, CI/CD, registry. Non in carico all'analisi, ma prerequisito realizzativo.                                                                                                                                                                                                                                                                                                                 | Aperto      | Architetti di sistema     | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-08  | Ordinamento invii                                              | È sufficiente l'ordine per singolo aggregato (atto/soggetto)? Rilevante quando si aggiungeranno le annotazioni.                                                                                                                                                                                                                                                                                                                                        | Aperto      | Analisi                   | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-09  | Ambienti ANSC                                                  | Disponibilità degli ambienti ANSC di preproduzione e produzione, credenziali, onboarding e certificati.                                                                                                                                                                                                                                                                                                                                                | Aperto      | Cliente / ANSC            | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-10  | Audit e privacy                                                | Tracciamento dell'operatore, conservazione dei log, base giuridica per il trattamento dei dati d'atto.                                                                                                                                                                                                                                                                                                                                                 | Aperto      | Cliente / DPO             | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-11  | Modifica tabella atto                                          | Eventuale aggiunta della colonna «stato_ansc» sulla tabella dell'atto di morte: è modifica all'esistente, quindi proposta a parte.                                                                                                                                                                                                                                                                                                                     | Aperto      | Settore tecnico           | Bassa        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-12  | Semantica di consegna                                          | Riformulato rispetto alla v1.0 (l'oggetto originario sulla semantica di consegna è venuto meno): politica di trattamento degli esiti indeterminati (timeout su R009/R007) --- mai retry cieco; prima riconciliazione via R005, poi eventuale R011 sul duplicato.                                                                                                                                                                                       | Riformulato | Analisi                   | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-13  | Configurazione campi obbligatori                               | Allineamento della configurazione dei campi obbligatori al mapping ufficiale dei casi d'uso ANSC (docs/Mapping_casi_uso/) e ai dizionari ANSC replicati in locale (RF-10): fonte, formato e processo di aggiornamento nel tempo.                                                                                                                                                                                                                       | Aperto      | Analisi / Fornitore ANSC  | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-14  | Mappatura campi SIPO ↔ ANSC e obbligatorietà                   | Completare la mappatura campo-per-campo fra le tabelle SIPO e il modello evento ANSC, per ogni evento/operazione/casistica, con l\'obbligatorietà e le condizioni. Alimenta la Configurazione (ANSC_CFG_CAMPO) e la pre-verifica (RF-9). La ricognizione del capitolo «Mappatura del payload» è parziale (pilota morte).                                                                                                                               | Aperto      | Analisi / Fornitore ANSC  | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-15  | Utenza tecnica e certificato server Roma                       | Modalità operativa concordata con Sogei per l'utenza tecnica e il certificato server di Roma, incluso il chiarimento dell'ambiguità del D.M. (Allegato 4): il claim x5c in M2M indica il certificato server, ma il decreto ripete che token e payload sono firmati con il certificato di postazione.                                                                                                                                                   | Aperto      | Cliente / Sogei           | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-16  | Registro delle postazioni autorizzate (scala Roma)             | Dimensionamento e governo del registro postazione↔identificativo (codice attribuito da ANPR) su scala Roma, con l'associazione postazione fisica ↔ identificativo richiesta dall'Allegato 4.                                                                                                                                                                                                                                                           | Aperto      | Cliente / Architetti      | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-17  | Limiti di rate / fair use                                      | Verifica di eventuali limiti di rate o soglie di fair use sui servizi cooperativi, non documentati nelle specifiche pubbliche.                                                                                                                                                                                                                                                                                                                         | Aperto      | Fornitore ANSC            | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-18  | Accreditamento come software house                             | Roma, sviluppando in proprio, assume il ruolo di software house nel canale di supporto ANSC: popolamento di nomeApplicativo/versioneApplicativo/fornitoreApplicativo (testata richiesta) e uso del piano di test pubblicato come riferimento per la preproduzione.                                                                                                                                                                                     | Aperto      | Cliente / Sogei           | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-19  | Semantica dell'esito KO di R009                                | Un esito KO della validazione R009 consuma un idAnsc / persiste un evento in stato RIFIUTATA, oppure è solo una risposta d'errore senza deposito? Incide su numerazione, bonifica e conteggio dei rifiuti.                                                                                                                                                                                                                                             | Aperto      | Fornitore ANSC            | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-20  | Riconciliazione del soggetto (R005/R018)                       | Per il pilota morte il soggetto è assunto già presente/allineato in ANSC, o va prevista la riconciliazione R018 nel flusso? Definisce un ramo di errore in fase R005.                                                                                                                                                                                                                                                                                  | Aperto      | Analisi / Cliente         | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-21  | Uso del forcingCode                                            | Il codice di forzatura per eventi anomali (R009) va esposto all'operatore (forzatura presidiata) o tenuto fuori scope nel pilota? Implica responsabilità e tracciamento dedicati.                                                                                                                                                                                                                                                                      | Aperto      | Cliente / ANSC            | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-22  | Ripartizione delle responsabilità tra ruoli (firma)            | Chi, tra i ruoli del back-office/sportello, è abilitato a firmare l'atto (R007) e a riprendere la lavorazione: dipende dall'organizzazione degli uffici di Roma e da eventuali deleghe di firma. Da definire con il cliente; incide sulla matrice ruoli×azioni della vista di supervisione.                                                                                                                                                            | Aperto      | Cliente                   | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-23  | Perimetro ammesso della modalità M2M (consultazioni senza OTP) | La nota tecnica ANSC SpecificheTecnicheServiziCooperativiJWT (v1.1.1) elenca l'attributo otp fra quelli del payload del token JWT senza dichiararne l'opzionalità e non descrive alcuna modalità machine-to-machine; l'Allegato 4 del D.M. 18/10/2022 non è disponibile nel repository. Va confermato se le letture (R004/R005) e le code (R008/R021/R901) possano essere eseguite senza l'OTP del singolo operatore, come assunto in §11.7 e §15.4.5. | Aperto      | Fornitore ANSC / Sogei    | Alta         |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-24  | Volumi reali degli atti di morte                               | La cifra di 90.000 atti/anno riportata fino alla v2.1 non è riconducibile ad alcuna fonte di progetto ed è incoerente con la popolazione di Roma; RNF-3 riporta ora un ordine di grandezza dichiarato come stima. Serve il dato reale, ripartito per municipio e per casistica, per dimensionare postazioni, sessioni OTP e supervisione.                                                                                                              | Aperto      | Cliente                   | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-25  | Ridondanza di ANSC_XREF rispetto allo store di stato           | Con l'aggiunta della colonna ID_ANSC allo store di stato, ANSC_XREF non conserva informazioni che lo store non abbia già, salvo DATA_ACQUISIZIONE. Va deciso se mantenerla come mappa storica durevole o fonderla nello store, in funzione della politica di conservazione e archiviazione (collegato a OP-10).                                                                                                                                        | Aperto      | Analisi / Settore tecnico | Bassa        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
+| OP-26  | Adozione dei dizionari ANSC nelle maschere SIPO                | Il pilota si limita a replicare i dizionari ANSC in locale e a renderli disponibili (RF-10). Resta da decidere quali maschere debbano leggere i valori da qui invece che dalle CONF\_\* esistenti, e quale raccordo prevedere fra i due cataloghi dove una corrispondenza esiste: è una decisione funzionale, con impatto sulle viste e sulle tendine a cascata già in esercizio.                                                                      | Aperto      | Cliente / Analisi         | Media        |
++--------+----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+---------------------------+--------------+
 
 # Back-office del componente ANSC
 
@@ -1308,19 +1520,19 @@
 
 ## Ruoli e visibilità
 
-  --------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------
   **Ruolo**                    **Responsabilità**
-  ---------------------------- ---------------------------------------------------------------------------------------------------------------------------
-  Operatore di supporto (SC)   Worklist per ufficiale, ricerca e tracciabilità, riconciliazione dello stato via R005/R011. Nessun ritentativo automatic.
+  ---------------------------- ----------------------------------------------------------------------------------------------------------------------------
+  Operatore di supporto (SC)   Worklist per ufficiale, ricerca e tracciabilità, riconciliazione dello stato via R005/R011. Nessun ritentativo automatico.
 
   Amministratore               Configurazione (operazioni, campi, versioni), ambienti e connettività, azioni massive, politiche di conservazione.
 
   Auditor (sola lettura)       Consultazione di audit, log e tracciabilità; nessuna azione di modifica.
-  --------------------------------------------------------------------------------------------------------------------------------------------------------
+  ---------------------------------------------------------------------------------------------------------------------------------------------------------
 
 ## Mappa dei menu del backoffice
 
-Le sezioni coprono il back-office: supervisione atti per ufficiale (stato reale dell'atto in ANSC), dettaglio atto, ricerca/tracciabilità, configurazione dei campi obbligatori con versionamento, audit, registro delle postazioni autorizzate e stato della sessione OTP.
+Le sezioni coprono il back-office: supervisione atti per ufficiale (stato reale dell'atto in ANSC), dettaglio atto, ricerca/tracciabilità, configurazione dei campi obbligatori con versionamento, dizionari ANSC, audit, registro delle postazioni autorizzate e stato della sessione OTP.
 
 ## La vista di supervisione
 
@@ -1328,7 +1540,7 @@
 
 ### Cosa mostra e come è organizzata
 
-La vista è una worklist di atti in stato non chiuso o problematico, letta sullo store di stato (ANSC_OUTBOX), filtrabile per municipio, ufficiale, categoria di eccezione e stato reale in ANSC. Le eccezioni sono raggruppate in categorie che ricalcano la tassonomia degli errori per fase: ogni riga porta l'atto, l'evento, lo stato reale in ANSC (badge coerente con la decodifica ANSC_11), la descrizione del problema, l'ufficiale competente, l'ultimo errore (code e testo restituiti da ANSC) e l'azione contestuale. Le categorie sono esposte come contatori in testa alla lista, così da rendere immediata la dimensione del lavoro arretrato per tipo di anomalia.
+La vista è una worklist di atti in stato non chiuso o problematico, letta sullo store di stato (ANSC_STATO_ATTO), filtrabile per municipio, ufficiale, categoria di eccezione e stato reale in ANSC. Le eccezioni sono raggruppate in categorie che ricalcano la tassonomia degli errori per fase: ogni riga porta l'atto, l'evento, lo stato reale in ANSC (badge coerente con la decodifica ANSC_11), la descrizione del problema, l'ufficiale competente, l'ultimo errore (code e testo restituiti da ANSC) e l'azione contestuale. Le categorie sono esposte come contatori in testa alla lista, così da rendere immediata la dimensione del lavoro arretrato per tipo di anomalia.
 
 ### Le categorie di eccezione
 
@@ -1386,7 +1598,7 @@
 
 Amministratore --- non opera sui singoli atti: gestisce configurazione, registro delle postazioni e profilazione, che determinano instradamento e abilitazioni.
 
-La vista di supervisione osserva, diagnostica, riconcilia e instrada: non finalizza gli atti. Le letture verso ANSC usate per diagnosi e riconciliazione (R005 e la consultazione dell'audit) si appoggiano alla sessione di servizio del concentratore --- l'insieme automatizzabile delle sole letture --- e non richiedono l'OTP del singolo operatore. Le scritture verso ANSC --- ripresa del deposito (R009), firma (R006/R007), annullamento (R011) --- sono invece atti presidiati: non sono eseguiti dal back-office, ma dall'USC nel flusso di finalizzazione ordinario (passo «Finalizza» sulla maschera SIPO), dove risiede la sessione OTP. Dalla worklist l'USC potrà aprire l'atto bloccato e ne completa la formazione in quel contesto: è lì, e non nel back-office, che semmai si sollecita la web-login OTP. Il back-office non detiene né usa l'OTP dell'operatore e non forma atti.
+La vista di supervisione osserva, diagnostica, riconcilia e instrada: non finalizza gli atti. Le letture verso ANSC usate per diagnosi e riconciliazione (R005 e la consultazione dell'audit) si appoggiano --- nell'ipotesi di lavoro adottata --- alla sessione di servizio del concentratore, l'insieme automatizzabile delle sole letture, e non richiedono l'OTP del singolo operatore; il perimetro ammesso della modalità M2M è da confermare con il fornitore (OP-23). Le scritture verso ANSC --- ripresa del deposito (R009), firma (R006/R007), annullamento (R011) --- sono invece atti presidiati: non sono eseguiti dal back-office, ma dall'USC nel flusso di finalizzazione ordinario (passo «Finalizza» sulla maschera SIPO), dove risiede la sessione OTP. Dalla worklist l'USC potrà aprire l'atto bloccato e ne completa la formazione in quel contesto: è lì, e non nel back-office, che semmai si sollecita la web-login OTP. Il back-office non detiene né usa l'OTP dell'operatore e non forma atti.
 
 ![](media/image7.png){width="6.5in" height="3.966101268591426in"}
 
@@ -1396,41 +1608,43 @@
 
 ## Le schermate
 
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **Schermata**                     **Scopo**                                                                                                                                                                                                                                                     **Azioni principali**                                                                                                         **Ruolo**
-  --------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------- -------------------------
-  Supervisione atti (stato ANSC)    Vista di supervisione degli atti e del loro stato reale in ANSC (confermato, firmato dal dichiarante, firmato da USC, rifiutato, annullato), per ufficiale e municipio. Non è la superficie di lavoro ordinaria: la formazione avviene nelle maschere SIPO.   Consulta stato, riconcilia (R005), riprendi un atto incomplete. QUESTA ATTIVITà DI RECUPERO DEVE ESSERE DISCUSSO E GESTITO.   Supporto / USC
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Schermata**                     **Scopo**                                                                                                                                                                                                                                                     **Azioni principali**                                                                                                                                             **Ruolo**
+  --------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------
+  Supervisione atti (stato ANSC)    Vista di supervisione degli atti e del loro stato reale in ANSC (confermato, firmato dal dichiarante, firmato da USC, rifiutato, annullato), per ufficiale e municipio. Non è la superficie di lavoro ordinaria: la formazione avviene nelle maschere SIPO.   Consulta stato, riconcilia (R005), apri l'atto in «Finalizza». Le modalità di ripresa della lavorazione e la loro attribuzione ai ruoli sono rimandate a OP-22.   Supporto / USC
 
-  Dettaglio atto                    Scheda dell'atto: stato reale in ANSC, idAnsc, timeline dell'audit; nessuna azione di ritentativo automatico.                                                                                                                                                 Deposita bozza, firma, consulta esito, riconcilia (R005), elimina bozza (R011)                                                USC / Auditor (lettura)
-
-  Riconciliazione                   Allineamento tra stato SIPO e stato effettivo dell'atto in ANSC (bozza, firmato, cancellato logicamente) tramite consultazione R005. Non è la rete di sicurezza di un invio non presidiato.                                                                   Consulta stato ANSC (R005), allinea                                                                                           Supporto
+  Dettaglio atto                    Scheda dell'atto: stato reale in ANSC, idAnsc, timeline dell'audit; nessuna azione di ritentativo automatico.                                                                                                                                                 Consulta esito, riconcilia (R005), apri in «Finalizza»                                                                                                            USC / Auditor (lettura)
 
-  Ricerca / Tracciabilità           Ricerca per atto SIPO, protocollo ANSC o soggetto; stato end-to-end con XREF e timeline dell'audit.                                                                                                                                                           Apri, ri-verifica                                                                                                             Tutti
+  Riconciliazione                   Allineamento tra stato SIPO e stato effettivo dell'atto in ANSC (bozza, firmato, cancellato logicamente) tramite consultazione R005. Non è la rete di sicurezza di un invio non presidiato.                                                                   Consulta stato ANSC (R005), allinea                                                                                                                               Supporto
 
-  Configurazione --- operazioni     ANSC_CFG_OPERAZIONE: evento × operazione × casistica → evento ANSC, mapper, flag firma/trascrizione, versione, validità.                                                                                                                                      Nuova versione, attiva/disattiva, clona                                                                                       Admin
+  Ricerca / Tracciabilità           Ricerca per atto SIPO, protocollo ANSC o soggetto; stato end-to-end con XREF e timeline dell'audit.                                                                                                                                                           Apri, ri-verifica                                                                                                                                                 Tutti
 
-  Configurazione --- campi          ANSC_CFG_CAMPO: campo ANSC ↔ SIPO, obbligatorietà, condizioni, decodifica, messaggio.                                                                                                                                                                         Modifica, importa da regole ANSC (R023/R901)                                                                                  Admin
+  Configurazione --- operazioni     ANSC_CFG_OPERAZIONE: evento × operazione × casistica → evento ANSC, mapper, flag firma/trascrizione, versione, validità.                                                                                                                                      Nuova versione, attiva/disattiva, clona                                                                                                                           Admin
 
-  Audit & Log                       ANSC_AUDIT: chiamate con richiesta/risposta; filtri per data, atto, esito, fase.                                                                                                                                                                              Consulta, esporta                                                                                                             Auditor / Supporto
+  Configurazione --- campi          ANSC_CFG_CAMPO: campo ANSC ↔ SIPO, obbligatorietà, condizioni, decodifica, messaggio.                                                                                                                                                                         Modifica, importa dal mapping dei casi d'uso ANSC e dai dizionari locali                                                                                          Admin
 
-  Sistema & Connettività            Ambiente, connettività ANSC (produzione/preproduzione), versione di configurazione attiva, stato della sessione OTP.                                                                                                                                          Test connessione, cambia versione config attiva                                                                               Admin
+  Audit & Log                       ANSC_AUDIT: chiamate con richiesta/risposta; filtri per data, atto, esito, fase.                                                                                                                                                                              Consulta, esporta                                                                                                                                                 Auditor / Supporto
 
-  Registro postazioni autorizzate   Elenco delle postazioni autorizzate con l'associazione postazione fisica ↔ identificativo attribuito da ANPR; obbligo normativo (D.M. 18/10/2022, All. 4) nel pattern a certificato server unico.                                                             Aggiungi/aggiorna postazione, esporta                                                                                         Amministratore
+  Sistema & Connettività            Ambiente, connettività ANSC (produzione/preproduzione), versione di configurazione attiva, stato della sessione OTP.                                                                                                                                          Test connessione, cambia versione config attiva                                                                                                                   Admin
 
-  Sessione OTP                      Stato della sessione presidiata dell'ufficiale (OTP valido 4 ore); acquisizione, scadenza, richiesta di rigenerazione dalla web app ANSC.                                                                                                                     Rigenera OTP, chiudi sessione                                                                                                 USC / Amministratore
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Registro postazioni autorizzate   Elenco delle postazioni autorizzate con l'associazione postazione fisica ↔ identificativo attribuito da ANPR; obbligo normativo (D.M. 18/10/2022, All. 4) nel pattern a certificato server unico.                                                             Aggiungi/aggiorna postazione, esporta                                                                                                                             Amministratore
 
+  Sessione OTP                      Stato della sessione presidiata dell'ufficiale (OTP valido 4 ore); acquisizione, scadenza, richiesta di rigenerazione dalla web app ANSC.                                                                                                                     Rigenera OTP, chiudi sessione                                                                                                                                     USC / Amministratore
+
+  Dizionari ANSC                    Catalogo delle decodifiche replicate in locale con versione, numero di valori, esito e data dell'ultimo aggiornamento; storico dei caricamenti.                                                                                                               Aggiorna (completo / selettivo / simulazione), consulta i valori, apri lo storico dei caricamenti                                                                 Amministratore
+  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
 ![](media/image8.png){width="6.3in" height="3.8571423884514435in"}
 
 *Wireframe --- Configurazione (Operazioni): metadati per evento × operazione × casistica e versione attiva; «campi »» apre i campi obbligatori.*
 
 ![](media/image9.png){width="6.3in" height="3.8571423884514435in"}
 
-*Wireframe --- Ricerca / Tracciabilità: stato end-to-end di un atto con timeline verifica → invio → ACK.*
+*Wireframe --- Ricerca / Tracciabilità: stato end-to-end di un atto con timeline verifica → deposito → firma.*
 
 ![](media/image10.png){width="6.3in" height="3.8571423884514435in"}
 
-*Wireframe --- Configurazione (Campi obbligatori): mapping campo ANSC ↔ SIPO e obbligatorietà con condizioni, importabili dalle regole ANSC (R023/R901).*
+*Wireframe --- Configurazione (Campi obbligatori): mapping campo ANSC ↔ SIPO e obbligatorietà con condizioni, importabili dal mapping dei casi d'uso ANSC e dai dizionari ANSC replicati in locale.*
 
 ![](media/image11.png){width="6.3in" height="3.8571423884514435in"}
 
@@ -1438,17 +1652,17 @@
 
 ## Attività coperte
 
-  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Attività**      **Schermate che la realizzano**
-  ----------------- -----------------------------------------------------------------------------------------------------------------------------------------------------
-  Verifica          Pre-filtro locale (RF-9) prima del deposito; Dettaglio atto (esito R009/R007); Audit (fase VERIFICA/DEPOSITO/FIRMA).
+  ----------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Verifica          Pre-filtro locale (RF-9) prima del deposito; Dettaglio atto (esito R009/R007); Audit (fasi VERIFICA, ALLEGATI, SOGGETTO, DEPOSITO, FIRMA_DICH, FIRMA_USC, RICONCILIAZIONE).
 
-  Supporto          Worklist per ufficiale (prepara, deposita bozza, firma, abbandona), Dettaglio atto (stato reale, riconciliazione R005/R011), Ricerca/Tracciabilità.
+  Supporto          Worklist per ufficiale (diagnosi, riconciliazione, apertura dell'atto in «Finalizza»), Dettaglio atto (stato reale, riconciliazione R005/R011), Ricerca/Tracciabilità.
 
-  Amministrazione   Configurazione (operazioni, campi, versioni), Sistema & Connettività (ambiente, connettività, versione attiva).
-  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  Amministrazione   Configurazione (operazioni, campi, versioni), Dizionari ANSC (aggiornamento on request e storico dei caricamenti), Sistema & Connettività (ambiente, connettività, versione attiva).
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
-Il back-office 1. rende osservabile lo stato reale degli atti in ANSC e fornisce all'ufficiale la supervisione degli atti, la consultazione dell'audit, l'amministrazione della configurazione e il registro delle postazioni; non contiene più leve di ritentativo automatico, prive di oggetto nel modello presidiato.
+Il back-office rende osservabile lo stato reale degli atti in ANSC e fornisce all'ufficiale la supervisione degli atti, la consultazione dell'audit, l'amministrazione della configurazione e il registro delle postazioni; non contiene più leve di ritentativo automatico, prive di oggetto nel modello presidiato.
 
 # Roadmap
 
@@ -1470,11 +1684,11 @@
 
 ## Tabelle operative
 
-**ANSC_OUTBOX**
+**ANSC_STATO_ATTO**
 
-CREATE TABLE ANSC_USR.ANSC_OUTBOX (
+CREATE TABLE ANSC_USR.ANSC_STATO_ATTO (
 
-ID_OUTBOX NUMBER GENERATED ALWAYS AS IDENTITY,
+ID_STATO_ATTO NUMBER GENERATED ALWAYS AS IDENTITY,
 
 ID_ATTO_SIPO NUMBER NOT NULL,
 
@@ -1484,7 +1698,7 @@
 
 COD_CASISTICA VARCHAR2(30 CHAR),
 
-CHIAVE_IDEMPOTENZA VARCHAR2(64 CHAR) NOT NULL,
+CHIAVE_ANTI_DUPLICATO VARCHAR2(64 CHAR) NOT NULL,
 
 COD_VERSIONE_CONFIG VARCHAR2(20 CHAR),
 
@@ -1494,6 +1708,8 @@
 
 ID_OPERAZIONE_ANSC VARCHAR2(50 CHAR),
 
+ID_ANSC VARCHAR2(50 CHAR),
+
 OPERATORE VARCHAR2(40 CHAR),
 
 HOSTNAME VARCHAR2(80 CHAR),
@@ -1508,51 +1724,51 @@
 
 DATA_UPD TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
 
-CONSTRAINT PK_ANSC_OUTBOX PRIMARY KEY (ID_OUTBOX),
+CONSTRAINT PK_ANSC_STATO_ATTO PRIMARY KEY (ID_STATO_ATTO),
 
-CONSTRAINT UQ_ANSC_OUTBOX_IDEMP UNIQUE (CHIAVE_IDEMPOTENZA),
+CONSTRAINT UQ_ANSC_STATO_ATTO_ANTIDUP UNIQUE (CHIAVE_ANTI_DUPLICATO),
 
-CONSTRAINT CK_ANSC_OUTBOX_STATO
+CONSTRAINT CK_ANSC_STATO_ATTO_STATO
 
 CHECK (STATO IN (\'IN_PREPARAZIONE\',\'CONFERMATO\',\'FIRMATO_DICHIARANTE\',
 
 \'FIRMATO_USC\',\'RIFIUTATA\',\'ANNULLATO\')),
 
-CONSTRAINT CK_ANSC_OUTBOX_ESITO
+CONSTRAINT CK_ANSC_STATO_ATTO_ESITO
 
 CHECK (TIPO_ESITO IS NULL OR TIPO_ESITO IN (\'RIFIUTATO\',\'INDETERMINATO\'))
 
 ) TABLESPACE ANSC_USR;
 
-CREATE INDEX ANSC_USR.IX_OUTBOX_STATO
+CREATE INDEX ANSC_USR.IX_STATO_ATTO_STATO
 
-ON ANSC_USR.ANSC_OUTBOX (COD_MUNICIPIO, ID_UFFICIALE, STATO) TABLESPACE ANSC_USR;
+ON ANSC_USR.ANSC_STATO_ATTO (COD_MUNICIPIO, ID_UFFICIALE, STATO) TABLESPACE ANSC_USR;
 
-CREATE INDEX ANSC_USR.IX_OUTBOX_ATTO
+CREATE INDEX ANSC_USR.IX_STATO_ATTO_ATTO
 
-ON ANSC_USR.ANSC_OUTBOX (ID_ATTO_SIPO) TABLESPACE ANSC_USR;
+ON ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO) TABLESPACE ANSC_USR;
 
-COMMENT ON TABLE ANSC_USR.ANSC_OUTBOX IS
+COMMENT ON TABLE ANSC_USR.ANSC_STATO_ATTO IS
 
-\'Coda transazionale degli invii verso ANSC (stessa txn dell\'\'atto).\';
+\'Store di stato ANSC per atto x operazione (stessa txn dell\'\'atto); NON e\'\' una coda di invii.\';
 
-COMMENT ON COLUMN ANSC_USR.ANSC_OUTBOX.COD_CASISTICA IS
+COMMENT ON COLUMN ANSC_USR.ANSC_STATO_ATTO.COD_CASISTICA IS
 
-\'Casistica / codice evento ANSC (dichiarazione vs trascrizione).\';
+\'Casistica SIPO (dichiarazione/trascrizione e variante del caso d\'\'uso); il codice evento ANSC e\'\' in COD_EVENTO_ANSC.\';
 
-COMMENT ON COLUMN ANSC_USR.ANSC_OUTBOX.CHIAVE_IDEMPOTENZA IS
+COMMENT ON COLUMN ANSC_USR.ANSC_STATO_ATTO.CHIAVE_ANTI_DUPLICATO IS
 
-\'Chiave locale anti-doppio-accodamento (NON deduplica ANSC).\';
+\'Chiave locale anti-doppio-deposito = COD_TIPO_EVENTO\|\|ID_ATTO_SIPO\|\|COD_TIPO_OPERAZIONE (NON deduplica ANSC).\';
 
-COMMENT ON COLUMN ANSC_USR.ANSC_OUTBOX.TIPO_ESITO IS
+COMMENT ON COLUMN ANSC_USR.ANSC_STATO_ATTO.TIPO_ESITO IS
 
 \'Esito negativo qualificato: RIFIUTATO o INDETERMINATO (timeout).\';
 
 **Trigger di aggiornamento del timestamp**
 
-CREATE OR REPLACE TRIGGER ANSC_USR.TRG_ANSC_OUTBOX_UPD
+CREATE OR REPLACE TRIGGER ANSC_USR.TRG_ANSC_STATO_ATTO_UPD
 
-BEFORE UPDATE ON ANSC_USR.ANSC_OUTBOX
+BEFORE UPDATE ON ANSC_USR.ANSC_STATO_ATTO
 
 FOR EACH ROW
 
@@ -1584,7 +1800,7 @@
 
 CONSTRAINT PK_ANSC_XREF PRIMARY KEY (ID_XREF),
 
-CONSTRAINT UQ_ANSC_XREF UNIQUE (ID_ATTO_SIPO, COD_TIPO_OPERAZIONE)
+CONSTRAINT UQ_ANSC_XREF UNIQUE (COD_TIPO_EVENTO, ID_ATTO_SIPO, COD_TIPO_OPERAZIONE)
 
 ) TABLESPACE ANSC_USR;
 
@@ -1598,7 +1814,7 @@
 
 ID_AUDIT NUMBER GENERATED ALWAYS AS IDENTITY,
 
-ID_OUTBOX NUMBER,
+ID_STATO_ATTO NUMBER,
 
 FASE VARCHAR2(20 CHAR) NOT NULL,
 
@@ -1616,10 +1832,16 @@
 
 CONSTRAINT PK_ANSC_AUDIT PRIMARY KEY (ID_AUDIT),
 
-CONSTRAINT FK_ANSC_AUDIT_OUTBOX
+CONSTRAINT CK_ANSC_AUDIT_FASE
 
-FOREIGN KEY (ID_OUTBOX) REFERENCES ANSC_USR.ANSC_OUTBOX (ID_OUTBOX),
+CHECK (FASE IN (\'VERIFICA\',\'ALLEGATI\',\'SOGGETTO\',\'DEPOSITO\',
 
+\'FIRMA_DICH\',\'FIRMA_USC\',\'RICONCILIAZIONE\')),
+
+CONSTRAINT FK_ANSC_AUDIT_STATO_ATTO
+
+FOREIGN KEY (ID_STATO_ATTO) REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_STATO_ATTO),
+
 CONSTRAINT CK_ANSC_AUDIT_REQ_JSON CHECK (RICHIESTA IS JSON),
 
 CONSTRAINT CK_ANSC_AUDIT_RES_JSON CHECK (RISPOSTA IS JSON)
@@ -1650,7 +1872,7 @@
 
 FLG_TRASCRIZIONE CHAR(1) DEFAULT \'N\' NOT NULL,
 
-FLG_FIRMA CHAR(1) DEFAULT \'N\' NOT NULL,
+FLG_FIRMA CHAR(1) DEFAULT \'S\' NOT NULL,
 
 COD_VERSIONE VARCHAR2(20 CHAR) NOT NULL,
 
@@ -1726,61 +1948,211 @@
 
 Righe di ANSC_CFG_CAMPO per la stessa operazione (estratto):
 
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **CAMPO_ANSC**                  **CAMPO_SIPO**                   **OBBL**   **COND_OBBLIGATORIETA**   **DECOD**              **MESSAGGIO**
-  ------------------------------- -------------------------------- ---------- ------------------------- ---------------------- ---------------------------------------
-  datiDiMorte.dataMorte           ATTO_DECESSO.DATA_DECESSO        S          ---                       ---                    Data del decesso obbligatoria
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **CAMPO_ANSC**                                                   **CAMPO_SIPO**                                    **OBBL**   **COND_OBBLIGATORIETA**   **DECOD**                                                             **MESSAGGIO**
+  ---------------------------------------------------------------- ------------------------------------------------- ---------- ------------------------- --------------------------------------------------------------------- --------------------------------------------------
+  evento.datiDiMorte.dataMorte                                     ATTO_DECESSO.DATA_DECESSO                         N          ---                       ---                                                                   Data del decesso
 
-  datiDiMorte.oraMorte            ATTO_DECESSO.ID_ORA_DECESSO      N          se nota                   (ora)                  ---
+  evento.datiDiMorte.oraMorte / minutoMorte                        ATTO_DECESSO.DATA_DECESSO (componente oraria)     N          se l'ora è nota           ---                                                                   ID_ORA_DECESSO qualifica l'informazione mancante
 
-  luogo.idComune                  ATTO_DECESSO.ID_COMUNE_DECESSO   S          ---                       ANSC_03                Comune del decesso obbligatorio
+  evento.datiDiMorte.idComuneMorte                                 ATTO_DECESSO.ID_COMUNE_DECESSO                    N          se decesso in Italia      --- (comuni: archivio ANPR)                                           Comune del decesso
 
-  luogo.idStato                   (Italia, costante)               S          ---                       (stati)                ---
+  evento.datiDiMorte.idStatoMorte                                  (Italia, costante)                                N          ---                       --- (stati: archivio ANPR)                                            ---
 
-  datiDiMorte.luogoMorte          ATTO_DECESSO.LUOGO_DECESSO       S          ---                       (tipo luogo)           Tipologia del luogo obbligatoria
+  evento.datiDiMorte.luogoMorte                                    ATTO_DECESSO.LUOGO_DECESSO                        N          ---                       --- (testo libero nel modello evento)                                 Luogo del decesso
 
-  datiDiMorte.indirizzoMorte      ATTO_DECESSO.ZONA_DECESSO        N          se abitazione             ---                    ---
+  evento.datiDiMorte.indirizzoMorte                                ATTO_DECESSO.ZONA_DECESSO                         N          se disponibile            ---                                                                   ---
 
-  defunto.cognome                 SOGGETTO (col. da mappare)       S          ---                       ---                    Cognome del defunto obbligatorio
+  evento.intestatari\[0\].cognome                                  SOGGETTO (col. da mappare)                        N          ---                       ---                                                                   Cognome del defunto
 
-  defunto.nome                    SOGGETTO (col. da mappare)       S          ---                       ---                    Nome del defunto obbligatorio
+  evento.intestatari\[0\].nome                                     SOGGETTO (col. da mappare)                        S          ---                       ---                                                                   Nome del defunto obbligatorio
 
-  defunto.sesso                   SOGGETTO (col. da mappare)       S          ---                       (sesso)                ---
+  evento.intestatari\[0\].sesso                                    SOGGETTO (col. da mappare)                        S          ---                       ---                                                                   Sesso del defunto obbligatorio
 
-  defunto.dataNascita             SOGGETTO (col. da mappare)       S          ---                       ---                    Data di nascita obbligatoria
+  evento.intestatari\[0\].dataNascita                              SOGGETTO (col. da mappare)                        S          ---                       ---                                                                   Data di nascita obbligatoria
 
-  defunto.luogoNascita.idComune   SOGGETTO (col. da mappare)       S          se nato in Italia         ANSC_03                ---
+  evento.intestatari\[0\].idComuneNascita                          SOGGETTO (col. da mappare)                        N          se nato in Italia         --- (comuni: archivio ANPR)                                           ---
 
-  defunto.luogoNascita.idStato    SOGGETTO (col. da mappare)       S          se nato all'estero        ANPR_02 (cfr. DV-32)   Stato estero di nascita
+  evento.intestatari\[0\].idStatoNascita / nomeStatoNascita        SOGGETTO (col. da mappare)                        S          ---                       --- (stati: archivio ANPR; cfr. registro DA VERIFICARE, voce DV-32)   Stato di nascita obbligatorio
 
-  defunto.codiceFiscale           SOGGETTO (col. da mappare)       N          se disponibile            ---                    CF non valido: warning, non bloccante
+  evento.intestatari\[0\].codiceFiscale                            SOGGETTO (col. da mappare)                        N          se disponibile            ---                                                                   CF non valido: warning, non bloccante
 
-  defunto.cittadinanza            SOGGETTO (col. da mappare)       S          ---                       (stati)                ---
+  evento.intestatari\[0\].idNazionalita / nazionalita              SOGGETTO (col. da mappare)                        S          ---                       --- (stati: archivio ANPR)                                            Cittadinanza obbligatoria
 
-  dichiarante.qualita             (parte dichiarante)              S          ---                       (qualità dich.)        Qualità del dichiarante obbligatoria
+  evento.intestatari\[0\].idstatocivile / descrizionestatocivile   SOGGETTO (col. da mappare)                        S          ---                       ANSC_61                                                               Stato civile del defunto obbligatorio
 
-  sezioneUfficialeStatoCivile     (config sede / ATTO)             S          ---                       ---                    Sezione USC assente
-  --------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  evento.datiEventoMorte.comparente1.flagDichiarante               ATTO_DECESSO.ID_SOGGETTO_DICHIARANTE → SOGGETTO   S          ---                       ---                                                                   Dichiarante obbligatorio
 
-*Estratto di ANSC_CFG_CAMPO per il pilota. I nomi dei campi ANSC seguono ModelDatiDiMorte/ModelSoggetto (cap. Mappatura); le colonne di ATTO_DECESSO sono verificate sull'area Decessi, mentre le colonne di SOGGETTO, del dichiarante e della sede sono indicative e vanno consolidate in OP-14 sui blocchi obbligatori di R023.*
+  evento.datiDichiarante.comprensione                              (condizioni del dichiarante, da mappare)          S          ---                       ANSC_32                                                               Condizioni del dichiarante obbligatorie
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+*Estratto di ANSC_CFG_CAMPO per il pilota. I percorsi dei campi ANSC e la colonna OBBL seguono il mapping ufficiale del caso d'uso Morte_001 (colonne Binding Object, Binding Field, Obbligatorio, Condizioni obbligatorietà); le colonne di ATTO_DECESSO sono verificate sul Disegno Base Dati, mentre le colonne di SOGGETTO e del dichiarante restano indicative e vanno consolidate in OP-14. Comuni e stati non hanno decodifica ANSC: provengono dagli archivi ANPR.*
+
+## Tabelle dei dizionari
+
+Strutture di destinazione del comando di aggiornamento dei dizionari ANSC (cap. «Gestione dei dizionari ANSC», requisito RF-10). Tutti gli oggetti sono nuovi.
+
+ANSC_DIZIONARIO
+
+CREATE TABLE ANSC_USR.ANSC_DIZIONARIO (
+
+ID_DIZIONARIO NUMBER GENERATED ALWAYS AS IDENTITY,
+
+ID_DECODIFICA VARCHAR2(20 CHAR) NOT NULL,
+
+NOME VARCHAR2(100 CHAR) NOT NULL,
+
+COD_DECODIFICA_ANSC VARCHAR2(20 CHAR) NOT NULL,
+
+VERSIONE_ANSC VARCHAR2(20 CHAR),
+
+NUM_VALORI NUMBER DEFAULT 0 NOT NULL,
+
+DATA_ULTIMO_CARICO TIMESTAMP,
+
+ESITO_ULTIMO_CARICO VARCHAR2(20 CHAR),
+
+DATA_INS TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
+
+DATA_UPD TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
+
+CONSTRAINT PK_ANSC_DIZIONARIO PRIMARY KEY (ID_DIZIONARIO),
+
+CONSTRAINT UQ_ANSC_DIZIONARIO UNIQUE (ID_DECODIFICA, NOME),
+
+CONSTRAINT UQ_ANSC_DIZIONARIO_COD UNIQUE (COD_DECODIFICA_ANSC),
+
+CONSTRAINT CK_ANSC_DIZIONARIO_ESITO
+
+CHECK (ESITO_ULTIMO_CARICO IS NULL OR
+
+ESITO_ULTIMO_CARICO IN (\'AGGIORNATA\',\'INVARIATA\',\'ERRORE\'))
+
+) TABLESPACE ANSC_USR;
+
+COMMENT ON TABLE ANSC_USR.ANSC_DIZIONARIO IS
+
+\'Catalogo delle decodifiche ANSC replicate in locale (una riga per decodifica).\';
+
+COMMENT ON COLUMN ANSC_USR.ANSC_DIZIONARIO.VERSIONE_ANSC IS
+
+\'Versione dichiarata da R901 /config/decodifica/elenco: termine di confronto del comando.\';
+
+ANSC_DIZIONARIO_VALORE
+
+CREATE TABLE ANSC_USR.ANSC_DIZIONARIO_VALORE (
+
+ID_VALORE NUMBER GENERATED ALWAYS AS IDENTITY,
+
+ID_DIZIONARIO NUMBER NOT NULL,
+
+CODICE VARCHAR2(20 CHAR) NOT NULL,
+
+DESCRIZIONE VARCHAR2(500 CHAR),
+
+DATA_INIZIO_VALIDITA DATE,
+
+DATA_FINE_VALIDITA DATE,
+
+ORDINAMENTO NUMBER,
+
+ATTRIBUTI CLOB,
+
+CONSTRAINT PK_ANSC_DIZIONARIO_VALORE PRIMARY KEY (ID_VALORE),
+
+CONSTRAINT FK_ANSC_DIZ_VALORE_DIZ
+
+FOREIGN KEY (ID_DIZIONARIO) REFERENCES ANSC_USR.ANSC_DIZIONARIO (ID_DIZIONARIO),
+
+CONSTRAINT UQ_ANSC_DIZ_VALORE UNIQUE (ID_DIZIONARIO, CODICE),
+
+CONSTRAINT CK_ANSC_DIZ_VALORE_JSON CHECK (ATTRIBUTI IS JSON)
+
+) TABLESPACE ANSC_USR;
+
+CREATE INDEX ANSC_USR.IX_DIZ_VALORE_ORD
+
+ON ANSC_USR.ANSC_DIZIONARIO_VALORE (ID_DIZIONARIO, ORDINAMENTO) TABLESPACE ANSC_USR;
+
+COMMENT ON COLUMN ANSC_USR.ANSC_DIZIONARIO_VALORE.ATTRIBUTI IS
+
+\'Colonne aggiuntive delle sole decodifiche che le prevedono (IDTIPOCONTENUTO, CODICECONSOLATO).\';
+
+ANSC_DIZIONARIO_CARICAMENTO
+
+CREATE TABLE ANSC_USR.ANSC_DIZIONARIO_CARICAMENTO (
+
+ID_CARICAMENTO NUMBER GENERATED ALWAYS AS IDENTITY,
+
+MODALITA VARCHAR2(20 CHAR) NOT NULL,
+
+OPERATORE VARCHAR2(40 CHAR) NOT NULL,
+
+DATA_INIZIO TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
+
+DATA_FINE TIMESTAMP,
+
+NUM_ESAMINATE NUMBER DEFAULT 0 NOT NULL,
+
+NUM_AGGIORNATE NUMBER DEFAULT 0 NOT NULL,
+
+NUM_INVARIATE NUMBER DEFAULT 0 NOT NULL,
+
+NUM_ERRORE NUMBER DEFAULT 0 NOT NULL,
+
+ESITO VARCHAR2(20 CHAR),
+
+DETTAGLIO_ERRORI CLOB,
+
+CONSTRAINT PK_ANSC_DIZ_CARICAMENTO PRIMARY KEY (ID_CARICAMENTO),
+
+CONSTRAINT CK_ANSC_DIZ_CAR_MODALITA
+
+CHECK (MODALITA IN (\'COMPLETO\',\'SELETTIVO\',\'SIMULAZIONE\')),
+
+CONSTRAINT CK_ANSC_DIZ_CAR_ESITO
+
+CHECK (ESITO IS NULL OR ESITO IN (\'OK\',\'PARZIALE\',\'KO\')),
+
+CONSTRAINT CK_ANSC_DIZ_CAR_JSON CHECK (DETTAGLIO_ERRORI IS JSON)
+
+) TABLESPACE ANSC_USR;
+
+Vista di fruizione (valori in corso di validita\')
 
+CREATE OR REPLACE VIEW ANSC_USR.V_ANSC_DIZIONARIO_VALIDO AS
+
+SELECT d.COD_DECODIFICA_ANSC, d.ID_DECODIFICA, d.NOME,
+
+v.CODICE, v.DESCRIZIONE, v.ORDINAMENTO, v.ATTRIBUTI
+
+FROM ANSC_USR.ANSC_DIZIONARIO d
+
+JOIN ANSC_USR.ANSC_DIZIONARIO_VALORE v ON v.ID_DIZIONARIO = d.ID_DIZIONARIO
+
+WHERE TRUNC(SYSDATE) \>= NVL(v.DATA_INIZIO_VALIDITA, TRUNC(SYSDATE))
+
+AND TRUNC(SYSDATE) \<= NVL(v.DATA_FINE_VALIDITA, TRUNC(SYSDATE));
+
+La vista è il punto di accesso previsto per i moduli SIPO, raggiungibile per sinonimo con grant di sola lettura; applica la validità temporale così che i consumatori non debbano conoscerne la regola.
+
 # Appendice B --- Interfacce API del componente
 
 Sono le API REST/JSON esposte dal componente all-ansc-sipo: verso il front-end (Preverifica e Inserimento) e verso il back-office. Sono interne a SIPO (raggiunte come gli altri servizi, con dominio e token) e vanno tenute distinte dai servizi di ANSC (R0xx) che il componente consuma internamente. Gli esempi JSON sono indicativi e da consolidare in fase di specifica di dettaglio.
 
 ## Convenzioni
 
-  ------------------------------------------------------------------------------------------------------------
+  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **Aspetto**       **Valore**
-  ----------------- ------------------------------------------------------------------------------------------
+  ----------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   Base path         /ansc (applicative) · /ansc/bo (back-office)
 
   Formato           JSON; UTF-8
 
   Autenticazione    Interna SIPO (dominio/token, come rest-client); ruoli: Supporto, Amministratore, Auditor
 
-  Esiti HTTP        200 OK · 202 Accepted · 400 · 401/403 · 404 · 409 conflitto · 422 validazione · 500
-  ------------------------------------------------------------------------------------------------------------
+  Esiti HTTP        200 OK con envelope (esito OK/KO) · 400 · 401/403 · 404 · 409 conflitto · 500. Gli esiti applicativi negativi viaggiano nell'envelope; i codici 4xx sono riservati agli errori di protocollo.
+  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 **Envelope di risposta comune**
 
@@ -1806,7 +2178,7 @@
 
 **POST /ansc/preverifica --- pre-filtro locale (RF-9)**
 
-Verifica i dati dell'atto per il tipo operazione; ne abilita il salvataggio. I dati sono letti da SIPO tramite idAttoSipo. Internamente invoca la validazione ANSC (R023/R009).
+Verifica i dati dell'atto per il tipo operazione; ne abilita la finalizzazione. I dati sono letti da SIPO tramite idAttoSipo. Non invoca alcun servizio ANSC: è un controllo puramente locale sulla configurazione e sulle decodifiche in cache.
 
 Richiesta:
 
@@ -1834,7 +2206,7 @@
 
 \"dati\": {
 
-\"abilitaSalvataggio\": true,
+\"abilitaFinalizza\": true,
 
 \"codEventoAnsc\": \"Morte_001\",
 
@@ -1846,7 +2218,7 @@
 
 }
 
-Risposta 422 --- esito KO (campi mancanti / validazione ANSC):
+Risposta 200 --- esito KO (campi obbligatori mancanti):
 
 {
 
@@ -1854,21 +2226,21 @@
 
 \"messaggi\": \[
 
-{ \"tipo\": \"ERROR\", \"campo\": \"luogo.idComune\",
+{ \"tipo\": \"ERROR\", \"campo\": \"evento.intestatari\[0\].idNazionalita\",
 
-\"codice\": \"OBBL_MANCANTE\", \"descrizione\": \"Comune del decesso obbligatorio\" },
+\"codice\": \"OBBL_MANCANTE\", \"descrizione\": \"Cittadinanza del defunto obbligatoria\" },
 
-{ \"tipo\": \"ERROR\", \"campo\": \"sezioneUfficialeStatoCivile\",
+{ \"tipo\": \"ERROR\", \"campo\": \"evento.intestatari\[0\].idstatocivile\",
 
-\"codice\": \"ANSC_KO\", \"descrizione\": \"Sezione USC assente (R023)\" },
+\"codice\": \"OBBL_MANCANTE\", \"descrizione\": \"Stato civile del defunto obbligatorio\" },
 
-{ \"tipo\": \"WARNING\", \"campo\": \"defunto.codiceFiscale\",
+{ \"tipo\": \"WARNING\", \"campo\": \"evento.intestatari\[0\].codiceFiscale\",
 
 \"codice\": \"FORMATO\", \"descrizione\": \"CF formalmente non valido\" }
 
 \],
 
-\"dati\": { \"abilitaSalvataggio\": false }
+\"dati\": { \"abilitaFinalizza\": false }
 
 }
 
@@ -1888,11 +2260,11 @@
 
 \"casistica\": \"DICH_ABITAZIONE\",
 
-\"chiaveIdempotenza\": \"88012-CREAZIONE-v12\",
+\"chiaveAntiDuplicato\": \"MORTE-88012-CREAZIONE\",
 
 \"versioneConfig\": \"v.12\",
 
-\"operatore\": \"RSSMRA80A01H501U\",
+\"operatore\": \"VRDGPP75B02H501Z\",
 
 \"hostname\": \"PDL-SC-014\"
 
@@ -1906,7 +2278,7 @@
 
 \"dati\": {
 
-\"idOutbox\": 550123, \"stato\": \"CONFERMATO\",
+\"idStatoAtto\": 550123, \"stato\": \"CONFERMATO\",
 
 \"idAnsc\": \"2026-058091-000123\", \"codEventoAnsc\": \"Morte_001\"
 
@@ -1922,13 +2294,13 @@
 
 \"messaggi\": \[
 
-{ \"tipo\": \"ERROR\", \"campo\": \"sezioneUfficialeStatoCivile\",
+{ \"tipo\": \"ERROR\", \"campo\": \"evento.intestatari\[0\].idstatocivile\",
 
-\"codice\": \"ANSC_KO\", \"descrizione\": \"Sezione USC assente (R009)\" }
+\"codice\": \"ANSC_KO\", \"descrizione\": \"Stato civile del defunto assente (R009)\" }
 
 \],
 
-\"dati\": { \"idOutbox\": 550123, \"stato\": \"RIFIUTATA\" }
+\"dati\": { \"idStatoAtto\": 550123, \"stato\": \"RIFIUTATA\" }
 
 }
 
@@ -1936,49 +2308,49 @@
 
 Elenco completo degli endpoint a supporto delle schermate del back-office.
 
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-  **Metodo e path**                                    **Scopo**                                                                                                       **Ruolo**
-  ---------------------------------------------------- --------------------------------------------------------------------------------------------------------------- ----------------------
-  GET /ansc/bo/worklist                                Coda di lavorazione presidiata per ufficiale/municipio, con lo stato reale dell'atto in ANSC                    USC / Supporto
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Metodo e path**                                    **Scopo**                                                                                                                                                                                  **Ruolo**
+  ---------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------------
+  GET /ansc/bo/worklist                                Coda di lavorazione presidiata per ufficiale/municipio, con lo stato reale dell'atto in ANSC                                                                                               USC / Supporto
 
-  GET /ansc/bo/atti                                    Lista atti in lavorazione, filtrabile per stato reale/ufficiale/municipio                                       USC / Supporto
+  GET /ansc/bo/atti                                    Lista atti in lavorazione, filtrabile per stato reale/ufficiale/municipio                                                                                                                  USC / Supporto
 
-  GET /ansc/bo/atti/{id}                               Dettaglio atto con stato ANSC e timeline dell'audit                                                             USC / Auditor
+  GET /ansc/bo/atti/{id}                               Dettaglio atto con stato ANSC e timeline dell'audit                                                                                                                                        USC / Auditor
 
-  POST /ansc/bo/atti/{id}/azioni                       Prepara, deposita bozza (R009), firma (R007), abbandona, elimina bozza (R011). Nessun ritentativo automatico.   USC / Supporto
+  POST /ansc/bo/atti/{id}/azioni                       Azioni di back-office non dispositive: riconcilia (R005), ri-verifica, instrada, annota. Le scritture verso ANSC (R009/R006/R007/R011) avvengono solo nel flusso presidiato «Finalizza».   Supporto
 
-  GET /ansc/bo/riconciliazione/stato/{idAtto}          Allineamento stato SIPO ↔ ANSC via consultazione R005                                                           Supporto
+  GET /ansc/bo/riconciliazione/stato/{idAtto}          Allineamento stato SIPO ↔ ANSC via consultazione R005                                                                                                                                      Supporto
 
-  GET /ansc/bo/tracciabilita                           Stato end-to-end per atto / protocollo / CF                                                                     Tutti
+  GET /ansc/bo/tracciabilita                           Stato end-to-end per atto / protocollo / CF                                                                                                                                                Tutti
 
-  POST /ansc/bo/atti/{id}/ri-verifica                  Riesegue la preverifica                                                                                         Supporto
+  POST /ansc/bo/atti/{id}/ri-verifica                  Riesegue la preverifica                                                                                                                                                                    Supporto
 
-  GET /ansc/bo/config/operazioni                       Elenco operazioni (per versione)                                                                                Admin
+  GET /ansc/bo/config/operazioni                       Elenco operazioni (per versione)                                                                                                                                                           Admin
 
-  GET\|PUT /ansc/bo/config/operazioni/{id}             Leggi / modifica un'operazione                                                                                  Admin
+  GET\|PUT /ansc/bo/config/operazioni/{id}             Leggi / modifica un'operazione                                                                                                                                                             Admin
 
-  GET\|PUT /ansc/bo/config/operazioni/{id}/campi       Leggi / modifica i campi obbligatori                                                                            Admin
+  GET\|PUT /ansc/bo/config/operazioni/{id}/campi       Leggi / modifica i campi obbligatori                                                                                                                                                       Admin
 
-  POST /ansc/bo/config/operazioni/{id}/campi/importa   Importa i campi dalle regole ANSC (R023/R901)                                                                   Admin
+  POST /ansc/bo/config/operazioni/{id}/campi/importa   Importa i campi dal mapping dei casi d'uso ANSC e dai dizionari ANSC replicati in locale                                                                                                   Admin
 
-  POST /ansc/bo/config/versioni                        Crea nuova versione (bozza)                                                                                     Admin
+  POST /ansc/bo/config/versioni                        Crea nuova versione (bozza)                                                                                                                                                                Admin
 
-  POST /ansc/bo/config/versioni/{v}/attiva             Attiva una versione                                                                                             Admin
+  POST /ansc/bo/config/versioni/{v}/attiva             Attiva una versione                                                                                                                                                                        Admin
 
-  GET /ansc/bo/audit                                   Elenco chiamate (filtri)                                                                                        Auditor / Supporto
+  GET /ansc/bo/audit                                   Elenco chiamate (filtri)                                                                                                                                                                   Auditor / Supporto
 
-  GET /ansc/bo/audit/{id}                              Dettaglio richiesta / risposta                                                                                  Auditor / Supporto
+  GET /ansc/bo/audit/{id}                              Dettaglio richiesta / risposta                                                                                                                                                             Auditor / Supporto
 
-  GET /ansc/bo/sistema/stato                           Ambiente, connettività, versione attiva, metriche                                                               Admin
+  GET /ansc/bo/sistema/stato                           Ambiente, connettività, versione attiva, metriche                                                                                                                                          Admin
 
-  POST /ansc/bo/sistema/test-connessione               Test di connettività verso ANSC                                                                                 Admin
+  POST /ansc/bo/sistema/test-connessione               Test di connettività verso ANSC                                                                                                                                                            Admin
 
-  GET /ansc/bo/sessione                                Stato della sessione OTP (validità, scadenza)                                                                   USC / Admin
+  GET /ansc/bo/sessione                                Stato della sessione OTP (validità, scadenza)                                                                                                                                              USC / Admin
 
-  POST /ansc/bo/sessione/rigenera                      Richiede all'operatore la rigenerazione dell'OTP dalla web app ANSC                                             USC
+  POST /ansc/bo/sessione/rigenera                      Richiede all'operatore la rigenerazione dell'OTP dalla web app ANSC                                                                                                                        USC
 
-  GET\|PUT /ansc/bo/postazioni                         Registro postazioni autorizzate (postazione ↔ identificativo ANPR)                                              Admin
-  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  GET\|PUT /ansc/bo/postazioni                         Registro postazioni autorizzate (postazione ↔ identificativo ANPR)                                                                                                                         Admin
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 **GET /ansc/bo/tracciabilita?idAtto=88012 --- risposta**
 
@@ -2038,13 +2410,13 @@
 
 {
 
-\"campoAnsc\": \"luogo.idComune\",
+\"campoAnsc\": \"evento.datiDiMorte.idComuneMorte\",
 
 \"campoSipo\": \"ATTO_DECESSO.ID_COMUNE_DECESSO\",
 
-\"obbligatorio\": true, \"condizione\": null,
+\"obbligatorio\": false, \"condizione\": \"se decesso in Italia\",
 
-\"decodificaAnsc\": \"ANSC_03\", \"messaggio\": \"Comune del decesso obbligatorio\"
+\"decodificaAnsc\": null, \"messaggio\": \"Comune del decesso\"
 
 }
 
@@ -2056,55 +2428,117 @@
 
 \"dati\": {
 
-\"idAudit\": 900321, \"idOutbox\": 550044, \"fase\": \"DEPOSITO\", \"servizio\": \"R009\",
+\"idAudit\": 900321, \"idStatoAtto\": 550044, \"fase\": \"DEPOSITO\", \"servizio\": \"R009\",
 
 \"esitoChiamata\": \"KO\", \"durataMs\": 320, \"data\": \"2026-07-23T10:07:03\",
 
-\"richiesta\": { \"idTipodocumento\": \"\...\",
+\"richiesta\": { \"evento\": { \"idUsecase\": \"\...\",
 
 \"datiDiMorte\": { \"dataMorte\": \"2026-07-20\" },
 
-\"sezioneUfficialeStatoCivile\": null },
+\"intestatari\": \[ { \"idstatocivile\": null } \] } },
 
-\"risposta\": { \"esito\": \"KO\", \"errors\": \[ \"sezioneUSC assente\" \] }
+\"risposta\": { \"esito\": \"KO\", \"errors\": \[ \"stato civile del defunto assente\" \] }
 
 }
 
 }
 
+## API dei dizionari (dec-ansc-sipo)
+
+Interfacce del concentratore dei dizionari. Servono al back-office e alla diagnosi: la fruizione ordinaria dei valori da parte delle maschere avviene in base dati, sulla vista V_ANSC_DIZIONARIO_VALIDO (cap. «Gestione dei dizionari ANSC»).
+
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  **Metodo e path**                      **Scopo**                                                                                                    **Ruolo**
+  -------------------------------------- ------------------------------------------------------------------------------------------------------------ ----------------------
+  POST /ansc/dizionari/aggiornamento     Avvia l'aggiornamento on request nelle tre modalità: completo, selettivo, simulazione                        Admin
+
+  GET /ansc/dizionari                    Catalogo locale: identificativo, nome, codice, versione, numero di valori, esito e data dell'ultimo carico   Admin / Auditor
+
+  GET /ansc/dizionari/{cod}/valori       Valori di una decodifica, per default i soli in corso di validità                                            Tutti
+
+  GET /ansc/dizionari/caricamenti        Storico dei comandi eseguiti, con i conteggi e l'esito                                                       Admin / Auditor
+
+  GET /ansc/dizionari/caricamenti/{id}   Dettaglio di un caricamento, con l'elenco delle decodifiche aggiornate e di quelle in errore                 Admin / Auditor
+  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+
+POST /ansc/dizionari/aggiornamento --- richiesta
+
+{
+
+\"modalita\": \"COMPLETO\", // COMPLETO \| SELETTIVO \| SIMULAZIONE
+
+\"decodifiche\": \[\] // valorizzato solo se modalita = SELETTIVO
+
+}
+
+Risposta 200 --- esito dell'aggiornamento:
+
+{
+
+\"esito\": \"OK\",
+
+\"dati\": {
+
+\"idCaricamento\": 412, \"modalita\": \"COMPLETO\",
+
+\"esaminate\": 143, \"aggiornate\": 2, \"invariate\": 141, \"inErrore\": 0,
+
+\"durataMs\": 18400,
+
+\"dettaglio\": \[
+
+{ \"codDecodifica\": \"ANSC_11\", \"nome\": \"dec_stato_evento\",
+
+\"versioneDa\": \"1.4.0\", \"versioneA\": \"1.5.0\", \"valori\": 11 },
+
+{ \"codDecodifica\": \"ANSC_03\", \"nome\": \"dec_use_case\",
+
+\"versioneDa\": \"1.52.0\", \"versioneA\": \"1.53.0\", \"valori\": 377 }
+
+\]
+
+}
+
+}
+
+In modalità SIMULAZIONE la risposta ha la stessa forma, ma i conteggi indicano che cosa cambierebbe e nulla viene scritto: «aggiornate» va letto come «da aggiornare».
+
 ## Corrispondenza con i servizi ANSC consumati
 
 Le API del componente si appoggiano internamente ai servizi di ANSC. La tabella riepiloga la corrispondenza; il contratto di dettaglio dei servizi ANSC è negli OpenAPI del repository ansc.
 
-  ----------------------------------------------------------------------------------------------------------------------------------------------------------
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   **API del componente**                    **Servizio ANSC invocato**
-  ----------------------------------------- ----------------------------------------------------------------------------------------------------------------
-  /ansc/preverifica                         R023 / R009 (validazione); R005 / R004 (consultazione esistenza)
+  ----------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
+  /ansc/preverifica                         Nessuno: pre-filtro locale su configurazione e dizionari ANSC replicati in locale (RF-10)
 
-  /ansc/deposita-bozza → firma              R009 (deposito bozza); R007 firma; R013 rettifica, R017 annotazione, R011 annullamento per le altre operazioni
+  /ansc/deposita-bozza → firma              R009 (deposito bozza); R006 (firma del dichiarante); R007 (firma USC). Fuori dal perimetro del pilota: R013 (validazione della rettifica), R017 (rettifica di un'annotazione), R011 (cancellazione logica dell'atto)
 
   /ansc/bo/tracciabilita, riconciliazione   R005 (consultazione ANSC); R008 (notifiche in ingresso)
 
-  firma (se in scope, OP-01)                R006 / R007 / R012
-  ----------------------------------------------------------------------------------------------------------------------------------------------------------
+  firma (se in scope, OP-01)                R006 (firma del dichiarante) / R007 (firma USC); R012 (firma elettronica del dichiarante via link e-mail) è fuori dal perimetro del pilota
 
-[^1]: Non esiste una dead-letter: non essendoci invio automatic, code, gli esiti negativi sono stati reali dell'atto (RIFIUTATO da ANSC) o esiti indeterminati (timeout), gestiti per riconciliazione R005/R011, non per ritentativo automatico
+  /ansc/dizionari/aggiornamento             R901 (/config/decodifica/elenco e /config/decodifica/dettaglio), invocato per il tramite di all-ansc-sipo, che costruisce e firma il token
+  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
+[^1]: Non esiste una dead-letter: non essendoci invio automatico né code, gli esiti negativi sono stati reali dell'atto (RIFIUTATA da ANSC) o esiti indeterminati (timeout), gestiti per riconciliazione R005/R011 e non per ritentativo automatico.
+
 [^2]: La UX non deve costruire token né chiamare ANSC. Tre ragioni: la chiave privata del certificato server (PKCS#12) con cui si firma il JWT/JWS non può risiedere nel browser; le chiamate cooperative e la firma R007 devono partire dal server, non attraversare il client; replicare la meccanica ANSC in ogni maschera moltiplicherebbe l'effort e la superficie di rischio. Alla UX restano solo i due passaggi che per natura avvengono alla postazione dell'operatore.
 
-[^3]: Questo codice è necessario definirlo con la committenza. Potrebbe essere l'id del record piuttosto che un identificativo alternativo. Verificare il formato previsto in ansc.
+[^3]: Il formato del numero comunale --- coincidente con l'identificativo del record oppure distinto --- va concordato con la committenza; la testata di richiesta ANSC ammette in idOperazioneComune un identificativo scelto dal comune (base_servizi.yaml).
 
-[^4]: Questa situazione potrebbe generare stati di indetirminazione da gestire tramite timeout applicativi da gestire sul Front End.
+[^4]: L'attesa dell'esito della scansione va limitata da un timeout applicativo lato front-end: superato il termine l'atto resta in attesa e non si procede a R009.
 
-[^5]: \[DA VERIFICARE: se un esito KO consumi comunque un idAnsc o lasci un evento in stato RIFIUTATA persistito, oppure sia solo una risposta d'errore --- incide su numerazione e bonifica.\]
+[^5]: Se un esito KO consumi comunque un idAnsc o lasci persistito un evento in stato RIFIUTATA, oppure sia solo una risposta d'errore, è questione aperta con il fornitore ANSC (OP-19): incide su numerazione e bonifica.
 
 [^6]: per il caso morte la firma è prevalentemente cartacea (upload pdf standard realizzato in modo autonomo?).
 
-[^7]: Le Azioni di recupero devono essere studiate.
+[^7]: Le azioni di recupero sono classificate al §11.6.4; la loro ripartizione fra i ruoli del back-office è rimandata a OP-22.
 
 [^8]: L'unico percorso differito legittimo resta il registro di emergenza (art. 10 del D.M.), procedura di eccezione tenuta separata dal flusso ordinario.
 
-[^9]: In questi casi deve essere valutato la gestione del timeout dell'attività ansc. Sono stati rilevati in letteratura diversi casi di comuni che hanno avuto un atto bloccato per diversi minuti.
+[^9]: La gestione dei timeout sulle chiamate ANSC va dimensionata esplicitamente lato applicativo; il trattamento degli esiti indeterminati che ne derivano è tracciato in OP-12.
 
 [^10]:
-    > Il backoffice non servirà a modificare il contenuto degli atti, che è prerogative di SIPO.
+    > Il backoffice non servirà a modificare il contenuto degli atti, che è prerogativa di SIPO.
```
