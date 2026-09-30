# REVIEW — ANALISI_Integrazione-ANSC v2.1 → v2.2

**Data:** 03/08/2026
**Sorgente:** `Documenti finali/ANALISI_Integrazione-ANSC_v2.1.docx` (invariata, SHA-1 `7f938581469961d27cdb5eb11b4848ec5912cac8`)
**Prodotto:** `Documenti finali/ANALISI_Integrazione-ANSC_v2.2.docx`
**Diff leggibile:** `Documenti finali/DIFF_v2_1_v2_2.md` (pandoc → markdown, `diff -u`)

> **Il Sommario (TOC) non è stato rigenerato**: è un campo Word e va aggiornato aprendo il documento
> e premendo F9 (oppure «Aggiorna sommario → Aggiorna intero sommario»). Dopo l'aggiornamento vanno
> ricontrollati i numeri di pagina, perché la v2.2 aggiunge una tabella (§9.2), tre righe di Open
> Point e alcuni capoversi.

**Integrità verificata:** 17 capitoli, 43 tabelle (42 + la nuova tabella dei casi d'uso in §9.2),
13 file multimediali e 11 immagini in linea (invariati), 10 richiami di nota a piè di pagina,
XML di `document.xml`, `footnotes.xml` e `styles.xml` ben formato. Stili, numerazione dei capitoli e
didascalie non sono stati toccati se non dove espressamente richiesto.

---

## Fase 1 — Esito delle verifiche sulle fonti

| V | Oggetto | Esito | Fonte |
|---|---|---|---|
| **V1** | Natura di R023 | **Il rilievo è confermato nella sostanza, ma per una ragione diversa da quella ipotizzata.** R023 **non è** una validazione a vuoto dell'evento: è la *dmnm validation API* (`POST /dmnm/validazione/{version}`, «Validazione documento dmnm verso TS»), che valida i **documenti DMNM provenienti dal Sistema Tessera Sanitaria**. Il suo schema di richiesta (`ValidazioneDmnmRequest`) richiede `numeroRicezione`, `idTipodocumento`, `sezioneUfficialeStatoCivile` — campi del documento DMNM, non del modello evento — e le descrizioni parlano di «record da aggiornare», quindi persiste. R009 `/validazione/evento` restituisce `idEvento` e `idAnsc` e deposita. **Non esiste alcun endpoint di validazione a vuoto: §3.2 è corretto e resta.** | `ansc/docs/openapi/R023_dmnm_validazione.yaml`, `R009_validazione.yaml`, `R022_dmnm_ricerca.yaml` |
| **V2** | Versione del contratto | **Confermata**: `## [1.53.0 - 30-06-2026]` è l'ultima release. Nessuna modifica. | `ansc/docs/Changelog.md` |
| **V3** | Numero di decodifiche | **87**, non 88: le occorrenze letterali distinte sono 88 ma `ANSC_04` e `ANSC_4` sono la stessa decodifica. Corretto in §3.1. | `ansc/docs/openapi/model_evento.yaml` |
| **V4** | Percorsi reali del modello evento | Confermati e usati per la correzione: `evento.intestatari[0].*` (defunto), `evento.datiEventoMorte.comparente1.*` (comparente/dichiarante), `evento.datiDiMorte.*` (data/luogo morte), `evento.numeroatto`/`dataformazione`/`ora`/`minuto`. `ModelLuogo` è usato per `luogoRedazione`, **non** per il luogo del decesso. `numeroRicezione` esiste in `ModelEvento` ma è «Numero ricezione documentazione da TS». **`sezioneUfficialeStatoCivile` non esiste nel modello evento**: compare solo in R022/R023. | `model_evento.yaml`, `ansc/docs/Mapping_casi_uso/morte/Morte_001.csv`, `Decessi_ANSC.xlsx` |
| **V5** | Casi d'uso Morte_xxx | **Il rilievo B1 è confermato e ampliato**: 14 casi d'uso, il prefisso UC non determina la tipologia. Dettaglio in B1. | `Decessi_ANSC.xlsx` (11 fogli), `ansc/docs/Mapping_casi_uso/morte/` |
| **V6** | Semantica dei servizi | R002 = **certificazione** (non «creazione»); R012 = firma **elettronica** del dichiarante (link e-mail, polling); R013 = validazione della **rettifica**; R016 = validazione del **provvedimento di rifiuto**; R017 = **rettifica di un'annotazione** (non «annotazione»); R018 = **riconciliazione di due soggetti** (è una scrittura, non una lettura); R021 = reminder notifiche (lettura); R024 = gestione richieste cittadino (`/elenco`, `/dettaglio` letture; `/aggiorna` scrittura); R901 = decodifiche. | `ansc/docs/openapi/*.yaml` |
| **V7** | OTP, claim JWT, certificati | Confermati: OTP di **quattro ore**, valore fisso **123456** valido solo in ambiente di test, produzione solo via web app (`https://anscweb.anpr.interno.it/ansc/login/otp`); claim `sub`, `sede` (codice ISTAT), `postazione` («Nome del certificato utilizzato. In genere corrisponde al CN del **certificato di postazione**»), `otp`, `jti`/`exp`/`iat`; header `alg` RS256, `typ`, `x5c`; JWS Detached. **La nota tecnica non menziona la modalità M2M, non dichiara opzionale l'attributo `otp` e parla di PKCS#12 *di postazione*; l'Allegato 4 del D.M. 18/10/2022 non è presente nel repository.** L'ambiguità certificato server ↔ certificato di postazione è quindi reale e **non chiudibile sulle fonti** → OP-23. | `ansc/docs/Note/SpecificheTecnicheServiziCooperativiJWT/…_v1.1.1.pdf` |
| **V8** | Colonne di ATTO_DECESSO | Confermate tutte le premesse dei rilievi B3/B4/B5: `DATA_DECESSO` DATE «Data/orario Decesso/Rinvenimento corpo/parti non superiore alle 24h dalla data dell'atto»; `ID_ORA_DECESSO` NUMBER «Identificativo del **tipo di informazione mancante**»; `ID_COMUNE_DECESSO` NUMBER «Comune decesso (**prima di arrivo in ospedale**)» — **non esiste altra colonna** per il comune di decesso; `LUOGO_DECESSO` VARCHAR2(200), `ZONA_DECESSO` VARCHAR2(200), `DETTAGLIO_LUOGO_DECESSO` VARCHAR2(1000), tutte testo libero. | `B9DA959E80-05-008-05-002_v1.00.docx` (letto come OOXML: è un vero .docx), `sql/matr_usr.sql` |
| **V9** | CODICE_ANPR e CONF_TIPO_ATTI | Confermati: `ANAG_USR.CONF_STATO_ESTERO.CODICE_ANPR VARCHAR2(20 BYTE)` e `MATR_USR.CONF_TIPO_ATTI.MASCHERA_UI VARCHAR2(100 BYTE)` esistono. Gli script `sql/` contengono solo DDL: **il popolamento non è verificabile** da questo workspace. | `sql/anag_usr.sql`, `sql/matr_usr.sql`, DBD |
| **V10** | Anti-pattern ANPR | Confermati tutti: `param.setEnvironment(EnvironmentHandler.TEST)` cablato (`AnprClient.java:78`); truststore a percorso fisso `keystore/cacerts` con password in chiaro (`AnprClient.java:241-242`) e credenziali proxy commentate nel sorgente (`:244`); `catch` vuoti (`AttoNasciteFlow.java:402-404`, `:720-722`); `"http://localhost:9393"` residuo; `@Scheduled` in 36 moduli; Thymeleaf in 35 moduli front-end; **137 `pom.xml`** (di cui alcuni aggregatori) — «~125 moduli» resta una stima corretta. Nessuna modifica necessaria. | `common/anpr-client/`, `back-end/`, `front-end/` |

---

## Fase 2 — Esito rilievo per rilievo

### Gruppo A — Coerenza con la tesi portante

| # | Stato | Capitoli/paragrafi | Note |
|---|---|---|---|
| **A1** | **Applicato** | §5.1, §5.5, §8, §8.1, §8.2, §10.2, §10.6.4, §14.4.1, §14.5, App. A, App. B | `ANSC_OUTBOX` → `ANSC_STATO_ATTO` (15 occorrenze), `ID_OUTBOX` → `ID_STATO_ATTO` (8), `idOutbox` → `idStatoAtto` (3); rinominati `IX_OUTBOX_*` → `IX_STATO_ATTO_*`, `PK_/UQ_/CK_ANSC_OUTBOX_*`, `TRG_ANSC_OUTBOX_UPD`, `FK_ANSC_AUDIT_OUTBOX`. Sottotitolo §8.1 → «ANSC_STATO_ATTO — store di stato ANSC per atto». `COMMENT ON TABLE` riscritto. Corretti §5.1 («ospita lo store di stato ANSC; è la sorgente di verità locale»), §5.5, §8.2 punto 4 (rinominato «Registrazione dello stato»), §10.7, didascalia wireframe §14.5 («timeline verifica → deposito → firma»). Il valore `INVIO` di `ANSC_AUDIT.FASE` è stato eliminato con D5. **Unico residuo volutamente conservato**: la voce di glossario «Store di stato ANSC (ex outbox)», che serve a raccordare la v2.0. |
| **A2** | **Applicato — esito «R023 non è un dry-run»** | RF-3, §3.2, §8.2 punto 3, App. B (`/ansc/preverifica`, §17.4) | Il pre-filtro è ora **puramente locale** ovunque. §3.2 («Non esiste alcun endpoint di validazione a vuoto») **non è stato toccato: la fonte lo conferma**. Rimossa l'invocazione ANSC da §8.2 punto 3 e da `/ansc/preverifica`; la riga di §17.4 recita ora «Nessuno: pre-filtro locale su configurazione e decodifiche in cache (allineate con R901)». **Nessun OP-23 è stato aperto per questo punto**: la verifica V1 lo chiude. Cfr. però il rilievo aggiuntivo **Z1**. |
| **A3** | **Applicato** | §14.5 (righe «Dettaglio atto» e «Supervisione atti»), §14.6, App. B (`POST /ansc/bo/atti/{id}/azioni`) | «Dettaglio atto» → «Consulta esito, riconcilia (R005), apri in «Finalizza»»; «Supervisione atti» → nota in maiuscolo rimossa e sostituita dal rimando a OP-22; §14.6 «Supporto» → «diagnosi, riconciliazione, apertura dell'atto in «Finalizza»»; endpoint azioni riscritto come non dispositivo, ruolo portato a **Supporto**. |
| **A4** | **Applicato** | §8.2 punto 3, §9.3, App. B | `abilitaSalvataggio` → `abilitaFinalizza` (risposta 200 e risposta KO); «ne abilita il salvataggio» → «ne abilita la finalizzazione»; «abilita il «Salva» (RF-4)» → «abilita il «Finalizza» (RF-4)» in §8.2 e §9.3. |
| **A5** | **Applicato** | §4.2 (capoverso introduttivo), §10.2, §10.4 (punti 3-4 e capoverso introduttivo) | Sequenza canonica **R001 → R005 → R009 → R006 → R007** uniformata. **PC-1 e Roadmap Fase 1 verificati: non contraddicono l'ordine** (lo abbreviano soltanto) e sono stati lasciati invariati. |
| **A6** | **Applicato** | §4.3 (riga «Gestore della sessione OTP e del token»), §5.1 (riga «Concentratore»), §5.3 | Aggiunto in §5.3 il capoverso sulla sessione OTP come stato condiviso da conservare fuori dal pod (cache distribuita o tabella dedicata in `ANSC_USR`, TTL allineato alle quattro ore, cancellazione all'invalidazione), con l'affinità di sessione dichiarata mitigazione temporanea. Richiamato in §5.1 e §4.3. |
| **A7** | **Applicato con adattamento — aperto OP-23 (non OP-24)** | §10.7, §14.4.5, cap. 13 | Le fonti **non confermano** che le letture possano avvenire senza OTP (V7). §3.3 non è stato modificato — riporta il contenuto del D.M., che è la fonte citata — ma l'uso M2M è ora marcato come **assunto da verificare** in §10.7 e §14.4.5, con rimando a **OP-23**. Rimosso R018 dall'elenco delle «consultazioni in lettura» di §10.7: R018 è la riconciliazione di due soggetti, cioè una scrittura (V6). **Numerazione:** il rilievo proponeva OP-24; poiché V1 ha chiuso la questione che avrebbe occupato OP-23, l'open point è stato numerato **OP-23** per non lasciare buchi nella sequenza (la stessa incoerenza che C2 chiede di eliminare). |
| **A8** | **Applicato** | §10.8 | Il differimento è ora riferito al momento di formazione dell'atto, non alla durata della sessione: «ogni sessione di formazione si esaurisce entro la validità dell'OTP (quattro ore) e una formazione differita apre semplicemente una nuova sessione». La frase sull'atto di morte è stata resa **neutra e verificabile**: «l'atto di morte è il caso più stretto, perché da esso dipende il rilascio del permesso di seppellimento […] I termini applicabili per tipologia sono quelli del D.P.R. 396/2000 e vanno verificati puntualmente in sede di specifica» — il testo del D.P.R. non è nel repository, quindi non si citano articoli. |

### Gruppo B — Correzioni fattuali

| # | Stato | Capitoli/paragrafi | Note |
|---|---|---|---|
| **B1** | **Applicato e ampliato** | §9.2 | Sostituita la frase con la **tabella completa dei 14 casi d'uso** (Codice UC → Descrizione → Tipologia → Codice Motore) e la conclusione corretta. Oltre a quanto segnalato dal rilievo, la verifica ha trovato **un caso in più**: **2.2.2.1** («Trascrizioni di sentenza dichiarazione di scomparsa per disastri aerei o a bordo di navi», Morte_008) è classificato **Dichiarazione**. Per **quattro** casi d'uso (2.1.0.5, 2.1.0.6, 2.1.0.7, 2.2.1.6 → Morte_016/017/019/020) la colonna *Tipologia* **è vuota nel foglio**: sono riportati come `n.d.` anziché essere classificati d'ufficio. **Propagazione al glossario: non applicabile** — il glossario non contiene alcuna voce «dichiarazione/trascrizione». Propagato invece a `COD_CASISTICA` (B6). |
| **B2** | **Applicato** | §8.2 (nota `CAMPO_ANSC` + tabella d'esempio), §9.1 (tabella completa), §16.2.1 (tabella completa + didascalia), App. B (esempi JSON) | Tutti i percorsi inventati sostituiti con quelli reali. `defunto.*` → `evento.intestatari[0].*`; `defunto.luogoNascita.idComune|idStato` → `evento.intestatari[0].idComuneNascita|idStatoNascita`; `dichiarante.qualita` → `evento.datiEventoMorte.comparente1.flagDichiarante` (più `evento.datiDichiarante.comprensione`, decodifica ANSC_32, anch'esso obbligatorio); `datiDiMorte.*` → `evento.datiDiMorte.*`. **Coppia divergente risolta a favore di `evento.datiDiMorte.idComuneMorte`**: `luogo.idComune` appartiene a `ModelLuogo`, che nel modello evento alimenta `luogoRedazione`, non il luogo del decesso. `sezioneUfficialeStatoCivile` **rimosso** da configurazione ed esempi: è un campo della richiesta R023 (DMNM/TS), non del modello evento. Corretta anche la decodifica: `ANSC_03` è `dec_use_case`, **non** la decodifica dei comuni — comuni e stati non hanno decodifica ANSC. |
| **B3** | **Applicato** | §9.1 (riga ora del decesso), §16.2.1 | `CAMPO_SIPO` per `oraMorte`/`minutoMorte` diventa `ATTO_DECESSO.DATA_DECESSO (componente oraria)`; la nota spiega che `ID_ORA_DECESSO` è «Identificativo del tipo di informazione mancante» e va mappata come qualificatore dell'informazione assente. |
| **B4** | **Applicato** | §9.1, §16.2.1 | Aggiunta la precisazione sulla semantica ristretta e sull'assenza di una colonna alternativa (`ID_OSPEDALE`/`ID_TIPO_DECESSO` qualificano il decesso in struttura). L'obbligatorietà nell'esempio del pilota è stata **condizionata**: `OBBL = N`, condizione «se decesso in Italia» — coerente con il mapping ufficiale, che per Morte_001 dichiara `idComuneMorte` non obbligatorio. |
| **B5** | **Applicato con adattamento** | §9.1 (riga LUOGO/ZONA + capoverso finale), OP-14 | La premessa del rilievo è **parzialmente smentita**: nel modello evento `luogoMorte` e `indirizzoMorte` sono **testo libero senza decodifica** (esempi «Casa», «Via Cattaneo, 15»); la lista codificata (`ANSC_150`, «Abitazione», «Istituto di cura», «Hospice»…) appartiene al canale DMNM/TS. Il capoverso aggiunto parla quindi di **regola di composizione** tre colonne SIPO → due campi ANSC, con la riconduzione al valore codificato «dove serve», ed è ricondotto esplicitamente a OP-14. |
| **B6** | **Applicato** | §8.1, App. A (`COMMENT ON COLUMN`) | Nota e commento riscritti come richiesto. |
| **B7** | **Applicato — fonte non trovata** | RNF-3, nota su RNF-3, cap. 13 | La cifra di 90.000 **non è riconducibile ad alcuna fonte** del workspace (compare solo nelle versioni precedenti dello stesso documento). Sostituita con «stima da confermare, ordine di grandezza 3·10⁴ atti/anno, pari a ~120 al giorno lavorativo», valore giornaliero ricalcolato anche nella nota successiva, e aperto **OP-24 — Volumi reali degli atti di morte**. |
| **B8** | **Applicato** | §8.2 (`SERVIZIO_ANSC`), §10.7, §17.4 | `SERVIZIO_ANSC` → «es. R009 per la validazione/deposito dell'evento. R002 è il servizio di certificazione, non di creazione». §17.4: R013, R017 e R011 marcati **fuori dal perimetro del pilota** con la semantica corretta (R017 = *rettifica di un'annotazione*); R012 = firma **elettronica** del dichiarante via link e-mail, fuori perimetro; aggiunto R006 dove mancava. §10.7: R018 rimosso dalle letture (è una scrittura) e R024 qualificato («/elenco e /dettaglio letture, /aggiorna scrittura sulla richiesta»). R016, R021, R901 risultano già usati con semantica corretta: nessuna modifica. |

### Gruppo C — Riferimenti e numerazione

| # | Stato | Capitoli/paragrafi | Note |
|---|---|---|---|
| **C1** | **Applicato** | §8.1, §5.1, Storia del Documento | `(PC-4)` → `(PC-2)`; rimosso `(cfr. PC-6)` dalla riga «Broker di messaggistica» (nessun PC esistente copre quel punto: il riferimento è stato eliminato, non sostituito); Storia del Documento riga 2.0 → `PC-1/2/3/5/7`. Nessun PC rinumerato. |
| **C2** | **Applicato con adattamento** | Tabella RNF, §5.5, cap. 8 | **RNF-5 non è stato reinserito**: nella v1.0 era «SLA scrittura asincrona» (consegna p95 < 5 min), rimosso deliberatamente in v2.0 perché la scrittura asincrona non esiste più — reintrodurlo contraddirebbe l'impianto. Si è quindi **rinumerato in sequenza**: RNF-6→**RNF-5**, RNF-7→**RNF-6**, RNF-8→**RNF-7**, aggiornando i 3 richiami nel testo (§5.5, cap. 8 ×2). |
| **C3** | **Applicato** | cap. 3 (capoverso introduttivo) | «descritto nella sezione «Modifiche rispetto alla v1.0»» → «dell'impianto errato della v1.0 (cfr. Storia del Documento)». |
| **C4** | **Applicato** | didascalia figura §4.2 | «Flusso §3.2» → «Flusso §4.2». |
| **C5** | **Applicato** | §16.2.1 | «ANPR_02 (cfr. DV-32)» → «— (stati: archivio ANPR; cfr. registro DA VERIFICARE, voce DV-32)», che rinvia al documento esterno già elencato fra i Riferimenti (R4, `DAD_Area-Stato-Civile_TRACCIAMENTO-DA-VERIFICARE`). |
| **C6** | **Applicato** | §4.1 | Frase rimossa. |
| **C7** | **Applicato in parte — una premessa smentita** | Storia del Documento | Corretto «0,4» → «0.4». **Le date identiche di v0.4 e v1.0 (23/07/2026) NON sono state modificate: sono corrette.** I file di progetto lo dimostrano — `ANALISI_Integrazione-ANSC_v0.4.docx` è del 23/07/2026 09:16 e `_v1.0.docx` del 23/07/2026 11:45: due consegne dello stesso giorno. Aggiunta la riga **v2.2** (03/08/2026) con capitoli toccati e sintesi richiesta. **Rilievo aggiuntivo applicato:** la tabella conteneva una **riga vuota** fra 1.0 e 2.0 e **mancava del tutto la riga v2.1**; è stata compilata e ricollocata dopo la 2.0 (03/08/2026, «Porting in Kubernetes (capp. 6 e 7); Modello dati — revisione redazionale: «lift-and-shift» sostituito da «porting»…»), descrizione ricavata dal diff v2.0→v2.1. |
| **C8** | **Applicato** | cap. 13 | Aggiunta la colonna **Stato** (larghezza sottratta alla colonna Questione, larghezza complessiva della tabella invariata a 9326 twips). Stati: OP-02 e OP-03 → **Chiuso** (priorità «—», coerente con il fatto che un punto chiuso non ha priorità); OP-12 → **Riformulato**; tutti gli altri → **Aperto**. I marcatori di stato («Aperta.», «CHIUSO.», «RIFORMULATO») sono stati rimossi dal testo della colonna Questione. **Owner e Priorità valorizzati su tutte le righe**: OP-01 → Cliente / Sogei, Alta (prima l'Owner conteneva «Aperto»); OP-02 → Analisi, — (prima «aperto», priorità vuota); OP-03 → Fornitore ANSC, — (prima conservava «Media» pur essendo chiuso). Aggiunte le righe **OP-23, OP-24, OP-25**. |

### Gruppo D — Modello dati e API

| # | Stato | Capitoli/paragrafi | Note |
|---|---|---|---|
| **D1** | **Applicato** | §8.1, App. A | `UQ_ANSC_XREF UNIQUE (COD_TIPO_EVENTO, ID_ATTO_SIPO, COD_TIPO_OPERAZIONE)`; in §8.1 aggiunta la motivazione (sequenze distinte per `ATTO_DECESSO`, `ATTO_NASCITA`, …). |
| **D2** | **Applicato** | §8.1, App. A (DDL, vincolo, commento), App. B (JSON) | `CHIAVE_IDEMPOTENZA` → **`CHIAVE_ANTI_DUPLICATO`** (5 occorrenze), `UQ_ANSC_STATO_ATTO_IDEMP` → `UQ_ANSC_STATO_ATTO_ANTIDUP`, `chiaveIdempotenza` → `chiaveAntiDuplicato`. Regola di composizione corretta: **tipo evento + id atto + tipo operazione**, esplicitamente senza versione di configurazione (con la motivazione: cambiando versione la chiave cambierebbe e il vincolo `UNIQUE` non proteggerebbe più). Esempio JSON `"88012-CREAZIONE-v12"` → `"MORTE-88012-CREAZIONE"`. |
| **D3** | **Applicato** | §8.1, App. A | Aggiunte in §8.1 le righe **`ID_UFFICIALE`** e **`COD_MUNICIPIO`** (già presenti nel DDL e citate dall'indice di supervisione) e la nuova colonna **`ID_ANSC VARCHAR2(50)`**, propagata al DDL subito dopo `ID_OPERAZIONE_ANSC`. `ID_OPERAZIONE_ANSC` è ora descritto come identificativo di operazione/protocollo di tracciamento, distinto dall'identificativo nazionale. |
| **D4** | **Applicato** | §8, §8.1, cap. 13 | `ANSC_XREF.STATO_ANSC`: `ACQUISITO/REGISTRATO/RIFIUTATO` → vocabolario ANSC_11 dello store di stato (`CONFERMATO, FIRMATO_DICHIARANTE, FIRMATO_USC, RIFIUTATA, ANNULLATO`). **Valutazione argomentata in §8**: con `ID_ANSC` nello store, `ANSC_XREF` non conserva nulla di più salvo `DATA_ACQUISIZIONE`; è mantenuta solo come mappa storica durevole indipendente dall'archiviazione dello store, e la scelta fra mantenerla e fonderla è aperta come **OP-25**. |
| **D5** | **Applicato** | §8.1, §14.6, App. A | Enum canonico adottato ed esteso: **`VERIFICA, ALLEGATI, SOGGETTO, DEPOSITO, FIRMA_DICH, FIRMA_USC, RICONCILIAZIONE`**. Aggiunto al DDL il vincolo `CK_ANSC_AUDIT_FASE` (prima `FASE` non aveva alcun `CHECK`). |
| **D6** | **Applicato** | §8 (tabella oggetti + nuovo capoverso), cap. 12 (riga «Tracciabilità») | La nota «a fini di tracciabilità e GDPR» è stata riformulata come rischio da governare. Aggiunto in §8 il capoverso «Conservazione dei payload di audit» (termine di conservazione esplicito con cancellazione automatica, minimizzazione, mascheratura, accesso limitato ad Auditor e Supporto), collegato a OP-10; la riga «Tracciabilità» del cap. 12 riporta gli stessi obblighi. Non è stata creata una nuova sezione. |
| **D7** | **Applicato** | App. B (Convenzioni, `/ansc/preverifica`) | Esiti HTTP → «200 OK con envelope (esito OK/KO) · 400 · 401/403 · 404 · 409 conflitto · 500. Gli esiti applicativi negativi viaggiano nell'envelope; i codici 4xx sono riservati agli errori di protocollo». Rimossi **202 Accepted** e **422**; `/ansc/preverifica` risponde ora «200 — esito KO». |
| **D8** | **Applicato** | glossario, §4.1, §4.3 | Testo uniformato sull'ipotesi di lavoro «certificato server unico per Roma», con rimando esplicito a OP-15 sia nel glossario sia in §4.1. La voce «Certificato di postazione» conserva la definizione del D.M. (è il termine normativo, confermato dalla nota tecnica JWT) ma dichiara che nell'ipotesi adottata la firma è apposta con il certificato server. |
| **D9** | **Applicato** | §4.3 (riga «Client ANSC») | La costruzione e la firma del token restano **solo** al «Gestore della sessione OTP e del token»; il Client ANSC «trasporta le chiamate applicando il token e la firma JWS già prodotti dal gestore della sessione […] Non costruisce né firma token». |
| **D10** | **Applicato** | App. A, §8.2 (nota `FLG_FIRMA` e tabella d'esempio) | `FLG_FIRMA CHAR(1) DEFAULT 'S' NOT NULL`; nota riscritta; nella tabella d'esempio la colonna «Firma» passa da `[OP-01]` a `S`, coerente con l'`INSERT` che già usava `'S'`. |
| **D11** | **Applicato** | App. B | `"operatore": "RSSMRA80A01H501U"` → `"VRDGPP75B02H501Z"`; il defunto in `/ansc/bo/tracciabilita` resta «Rossi Mario (RSSMRA80A01H501U)». I due valori sono ora distinti e corrispondono ai nomi segnaposto convenzionali. |

### Gruppo E — Forma

| Voce | Stato | Note |
|---|---|---|
| Refusi | **Applicati tutti** | `possessp`→`possesso` (§10.6); `convolgere`→`coinvolgere` (cap. 7); `sull aparte di FE`→`sulla parte di FE` (§3.4, con «richiederà **un** intervento»); `indetirminazione`→ nota 4 riscritta; `invio automatic, code`→ nota 1 riscritta; `Nessun ritentativo automatic.`→`automatico.` (§14.2); `riprendi un atto incomplete`→ corretto insieme ad A3 (§14.5); `prerogative di SIPO`→`prerogativa` (nota 10); `ed ad oggi`→`e ad oggi` (§2.1); `l' opzione`→`l'opzione` (§3.5); aggiunto «è» in §4.1; rimosso «1.» in §14.6. |
| Registro impersonale | **Applicato** | §3.5 «si ritiene sia l'opzione più praticabile»; §4.1 «Si ritiene che questa sia la scelta…»; §6.2 «Lo stato di partenza è comunque favorevole» (rimosso «a nostro avviso»). |
| Nomenclatura ambienti | **Applicato** | La corrispondenza è dichiarata **una volta sola**, in §3.1: ambienti ANSC = produzione / preproduzione / mock locale; ambienti SIPO = sviluppo / test / esercizio; corrispondenza «esercizio SIPO → produzione ANSC, test e sviluppo SIPO → preproduzione ANSC o mock locale». Allineati di conseguenza il cap. 12 (era «collaudo, esercizio») e OP-09 (era «collaudo ed esercizio»). §6.2 e §14.5 usavano già la terminologia corretta. |
| Note redazionali | **Applicate** | **Nota 1** riscritta in forma affermativa; **nota 3** → il formato del numero comunale va concordato con la committenza, con il richiamo a `idOperazioneComune` di `base_servizi.yaml`; **nota 4** → timeout applicativo lato front-end; **nota 5** (`[DA VERIFICARE: …]`) → rimando a **OP-19**; **nota 7** → rimando a §10.6.4 e OP-22; **nota 9** → rimando a OP-12, **rimossa l'affermazione non documentabile** («rilevati in letteratura diversi casi di comuni…»); **nota in §14.5** → gestita in A3. Nessuna nota è stata eliminata: tutte convertite in testo affermativo o in rimando a open point numerato. |

---

## Rilievi aggiuntivi emersi dalle verifiche (non previsti nell'elenco)

| # | Rilievo | Fonte | Trattamento |
|---|---|---|---|
| **Z1** | **R023 è sistematicamente descritto come «le regole di validazione ANSC» e usato come fonte dell'obbligatorietà dei campi.** È falso: R023 valida i documenti **DMNM provenienti dal Sistema Tessera Sanitaria**. L'esempio di §9.3 («il luogo del decesso (ModelLuogo) dichiara obbligatori idComune, nomeComune, idProvincia…») è **inventato**: `ModelLuogo` non ha alcun blocco `required`, e i campi `numeroRicezione`/`idTipodocumento`/`sezioneUfficialeStatoCivile` sono i `required` di `ValidazioneDmnmRequest`, cioè del documento DMNM. | `R023_dmnm_validazione.yaml`, `model_evento.yaml` | **Corretto** in §8.2 (nota `ID_TIPO_DOCUMENTO`, alimentazione di `ANSC_CFG_CAMPO`, punto 1 della modalità operativa), §9.3 (obbligatorietà + esempio riscritto su Morte_001 + manutenzione), OP-13, §14.5, App. B (endpoint di importazione), didascalia wireframe. |
| **Z2** | **Esiste una fonte pubblicata per l'obbligatorietà dei campi, che il documento ignora**: `ansc/docs/Mapping_casi_uso/` contiene, per ogni caso d'uso, un CSV/XLSX con le colonne *Sezione, Campo, Obbligatorio, Binding Object, Binding Field, Note obbligatorietà formule, Condizioni obbligatorietà* — esattamente ciò che serve a `ANSC_CFG_CAMPO` e a OP-14. Per Morte_001: 219 righe, 38 obbligatorie. La semantica delle colonne è documentata in `readme_mapping.md`. | `ansc/docs/Mapping_casi_uso/` | **Inserito** come fonte primaria in §8.2, §9.3, OP-13 e nella didascalia di §16.2.1. Riduce sensibilmente l'incognita di OP-14. |
| **Z3** | `ANSC_CFG_OPERAZIONE.ID_TIPO_DOCUMENTO` era descritto come «idTipodocumento ANSC»: il campo esiste **solo** in R022/R023, cioè nel canale DMNM/TS. | `openapi/*.yaml` (grep) | **Corretto** in §8.2: pertinente ai soli casi d'uso alimentati da documentazione sanitaria (Morte_016/017). |
| **Z4** | `numeroRicezione` era presentato come protocollo assegnato da ANSC («ANSC assegna proprio protocollo e numeroRicezione»). È il «Numero ricezione documentazione da TS»; in `Decessi_ANSC.xlsx` è il binding dei soli casi 2.1.0.5 e 2.1.0.6. | `model_evento.yaml`, `Decessi_ANSC.xlsx` | **Corretto** nella riga «Atto» di §9.1. |
| **Z5** | La decodifica `ANSC_03` era usata per il comune del decesso: `ANSC_03` è `dec_use_case`. Comuni e stati **non hanno** decodifica ANSC (provengono dagli archivi ANPR). | `ansc/docs/Decodifiche/3_dec_use_case.csv` | **Corretto** in §16.2.1 e in App. B (`"decodificaAnsc": null`). |
| **Z6** | R018 era elencato fra le «consultazioni in lettura» automatizzabili: è il servizio di **riconciliazione di due soggetti**, cioè una scrittura. | `R018_servizi.yaml` | **Rimosso** dall'elenco di §10.7 (resta correttamente citato in §10.6.2, §14.4.2 e OP-20). |
| **Z7** | La Storia del Documento non aveva alcuna riga per la **v2.1** (una riga vuota al suo posto). | file di progetto + diff v2.0→v2.1 | **Compilata** (cfr. C7). |
| **Z8** | Il numero di decodifiche referenziate era 88; le decodifiche distinte sono **87** (`ANSC_04` e `ANSC_4` coincidono). | `model_evento.yaml` | **Corretto** in §3.1. |

---

## Decisioni che richiedono la committenza

Punti che **non è stato possibile chiudere sulle fonti** e che sono diventati open point nel documento.

### OP-23 — Perimetro ammesso della modalità M2M (consultazioni senza OTP)
*Owner: Fornitore ANSC / Sogei — Priorità: Alta — richiamato in §10.7 e §14.4.5*

L'impianto della v2.1 (e della v2.2) assume che letture e code — R004, R005, R008, R021, R901 — possano
essere eseguite da un processo non presidiato, senza l'OTP del singolo operatore. **Le fonti disponibili
non lo confermano.** La nota tecnica `SpecificheTecnicheServiziCooperativiJWT v1.1.1` elenca `otp` fra
gli attributi del payload del token JWT senza dichiararlo opzionale, non descrive alcuna modalità
machine-to-machine e mostra l'apertura di un PKCS#12 **di postazione**. L'Allegato 4 del D.M.
18 ottobre 2022, che secondo il documento distingue le due modalità, **non è presente nel repository**:
la tabella di §3.3 poggia quindi su una fonte non verificabile qui. Se la risposta fosse negativa,
cadrebbero il «Processo di automazione (letture/code)» di §5.1 e l'intera premessa di §10.7 e §14.4.5,
e la vista di supervisione dovrebbe operare entro una sessione OTP di un operatore.

### OP-24 — Volumi reali degli atti di morte
*Owner: Cliente — Priorità: Media — richiamato in RNF-3*

La cifra di 90.000 atti/anno non è riconducibile ad alcuna fonte di progetto. RNF-3 riporta ora un
ordine di grandezza dichiarato come stima (3·10⁴ atti/anno, ~120 al giorno lavorativo). Serve il dato
reale, ripartito per municipio e per casistica, perché dimensiona postazioni, sessioni OTP concorrenti
e carico della supervisione — non il throughput, che resta irrilevante.

### OP-25 — Ridondanza di ANSC_XREF rispetto allo store di stato
*Owner: Analisi / Settore tecnico — Priorità: Bassa — richiamato in §8*

Con `ID_ANSC` sullo store di stato, `ANSC_XREF` non conserva informazioni proprie salvo
`DATA_ACQUISIZIONE`. Mantenerla ha senso solo se la politica di conservazione prevede l'archiviazione
o la purga dello store: è una decisione che dipende da OP-10 e dal settore tecnico.

### Punti preesistenti su cui la revisione ha aumentato la pressione

- **OP-14 (mappatura campo-per-campo)** — ora **parzialmente risolvibile senza committenza**: il
  mapping ufficiale `ansc/docs/Mapping_casi_uso/` fornisce percorsi, obbligatorietà e condizioni per
  ciascun caso d'uso. Resta a carico dell'analisi il lato SIPO (colonne di `SOGGETTO`, del dichiarante,
  della sede) e la **regola di normalizzazione del luogo del decesso** (tre colonne di testo libero
  verso due campi di testo libero), aggiunta a §9.1.
- **OP-15 (certificato server ↔ certificato di postazione)** — la verifica V7 conferma che la nota
  tecnica ANSC parla di certificato **di postazione**: l'ipotesi «certificato server unico per Roma»
  resta un'ipotesi di lavoro dichiarata, non una scelta validata dal fornitore.
- **OP-19 (semantica dell'esito KO di R009)** — la nota 5 `[DA VERIFICARE]` è stata convertita nel
  rimando a questo open point: la questione resta aperta e incide su numerazione e bonifica.
- **OP-22 (deleghe di firma)** — la nota redazionale in maiuscolo di §14.5 è stata sostituita dal
  rimando a questo open point: chi può riprendere e firmare un atto in eccezione è una decisione
  organizzativa del Comune.

---

---

## Intervento aggiuntivo — Gestione dei dizionari ANSC (nuovo cap. 10)

Richiesta successiva alla revisione: rendere i dizionari (decodifiche) di ANSC fruibili anche da SIPO,
tramite un concentratore specializzato che li recupera e li introduce in tabelle SIPO su comando
manuale, previa verifica che la funzione non fosse già coperta dalle API dell'unico concentratore.

### Esito della verifica: la funzione non c'era, ma era nominata in due punti

Nel documento fino alla v2.2 R901 compariva **solo** in richiami impliciti, mai come funzione progettata:

| Dove | Che cosa diceva | Trattamento |
|---|---|---|
| §5.1, riga «Processo di automazione (letture/code)» | «…polling notifiche (R008), reminder (R021), **allineamento decodifiche (R901)**, consultazioni» | **Estratto**: R901 rimosso dall'elenco, aggiunta una riga di topologia per il componente dedicato |
| §11.7 «Automazione dove è ammessa» | «…**allineamento delle decodifiche (R901)**, consultazioni in lettura» | **Estratto**: R901 rimosso, con rinvio esplicito al nuovo capitolo |
| §8.2 (modalità operativa, punto 1), RF-3, §9.3 | «decodifiche cachate via R901», «Fonte primaria: … le decodifiche (R901)» | Riformulati: le decodifiche si leggono **in locale**, non chiamando ANSC |
| App. B, `POST /ansc/bo/config/…/campi/importa`; §15.5; didascalia wireframe | «Importa i campi … **dalle decodifiche R901**» | Riformulati su «dai dizionari ANSC replicati in locale» |
| OP-13 | «…e alle decodifiche (R901)» | Riformulato |

**Non esistevano** né una struttura di destinazione, né un'interfaccia, né un comando: nessuna tabella,
nessun endpoint, nessuna schermata. La funzione era citata, non progettata. Nessuna API del
concentratore la copriva: l'unico endpoint che nominava R901 era quello di importazione dei campi di
configurazione, che è cosa diversa (e che, come già corretto nel gruppo B, confondeva R023 con il
mapping dei casi d'uso).

### Che cosa è stato aggiunto

- **RF-10** (nuovo requisito funzionale) e voce di glossario «Dizionario ANSC (decodifica)».
- **Nuovo capitolo 10 — «Gestione dei dizionari ANSC»**, inserito fra «Mappatura del payload» e
  «Modello di esecuzione», con cinque sezioni: il servizio R901 e il corpus; perché un componente
  dedicato; il comando di aggiornamento; il modello dati; la fruizione da parte di SIPO.
  **Tutti i capitoli successivi slittano di uno** (Modello di esecuzione → 11, … Appendice B → 18);
  i tre riferimenti numerici interni sono stati aggiornati (§10.7 → §11.7, §14.4.5 → §15.4.5,
  nota 7 §10.6.4 → §11.6.4).
- **§5.1**: nuova riga di topologia per `dec-ansc-sipo` (Deployment, 1 replica).
- **Appendice A**: DDL di `ANSC_DIZIONARIO`, `ANSC_DIZIONARIO_VALORE`,
  `ANSC_DIZIONARIO_CARICAMENTO` e della vista `V_ANSC_DIZIONARIO_VALIDO`.
- **Appendice B**: cinque endpoint `/ansc/dizionari/*` con gli esempi JSON, più la riga nella mappa
  API ↔ servizi ANSC consumati.
- **Back-office**: schermata «Dizionari ANSC» (ruolo Amministratore), voce nella mappa dei menu e
  nell'attività di Amministrazione.
- **OP-26** — Adozione dei dizionari ANSC nelle maschere SIPO.
- Storia del Documento: riga v2.2 estesa.

### Le tre decisioni di disegno e il perché

**1. Il componente non parla con ANSC direttamente.** `dec-ansc-sipo` invoca R901 **per il tramite di
`all-ansc-sipo`**. Il documento stabilisce (cap. 4) che il concentratore è «il solo luogo dove può
risiedere la chiave privata del certificato server (PKCS#12)»: mettere un secondo PKCS#12 in un
componente che scarica tabelle sarebbe stato un peggioramento della postura di sicurezza a guadagno
nullo. Il precedente esiste già in SIPO: i moduli di stato civile non parlano con ANPR ma passano dal
concentratore `all-anpr-sipo`.

**2. Il comando manuale non è una limitazione, è ciò che rende il disegno indipendente da OP-23.**
R901 è una lettura e in teoria sarebbe schedulabile, ma l'ammissibilità della modalità non presidiata
non è confermata dalle fonti. Con il comando manuale l'aggiornamento è avviato da un amministratore
autenticato: se ANSC pretendesse comunque l'OTP, l'operazione si svolge nella sua sessione. Se OP-23
si chiudesse in senso favorevole, aggiungere una schedulazione è un'estensione, non una riprogettazione.

**3. Il contratto verso SIPO è la base dati, non un'API.** I dizionari sono esposti dalla vista
`V_ANSC_DIZIONARIO_VALIDO` in `ANSC_USR`, raggiunta per sinonimo con grant di sola lettura — lo stesso
schema con cui i moduli dello Stato Civile già raggiungono le tabelle anagrafiche di `ANAG_USR`. Gli
endpoint REST servono al back-office e alla diagnosi.

### Dati verificati sulle fonti e usati nel capitolo

| Dato | Valore | Fonte |
|---|---|---|
| Operazioni di R901 | 4: `/config/decodifica/elenco`, `/dettaglio`, `/data_adesione`, `/usecase-multilingua` | `R901_config_decodifica.yaml` |
| Meccanismo di aggiornamento incrementale | `/elenco` restituisce **id, descrizione e versione** per ogni tabella → il confronto di versione decide che cosa scaricare | `ModelSintesiDecodifica` |
| Formato dello scarico | `/dettaglio` restituisce `contenuto` in **base64**, formato `csv`, **compresso per default** | `DecodificaDettaglioRequest/Response` |
| Dimensione del corpus | **145 file** su **143 identificativi distinti**, **1.376 righe** di dato | `ansc/docs/Decodifiche/` (conteggio diretto) |
| Copertura | **87** identificativi referenziati dal modello evento, **56** no; tutti gli 87 hanno un file pubblicato | `model_evento.yaml` + `Decodifiche/` |
| Tracciato | **140/145** con `ID, DESCRIZIONE, DATAINIZIOVALIDITA, DATAFINEVALIDITA, ORDINAMENTO`; 3 con sole `ID, DESCRIZIONE` (28, 60, 63); 2 con colonna extra (`IDTIPOCONTENUTO` in 3, `CODICECONSOLATO` in 97) | conteggio diretto |
| Dimensionamento colonne | descrizione più lunga **286 caratteri** → `VARCHAR2(500)` | conteggio diretto |
| Anti-pattern ANPR richiamato | `WS7001` (scarico tabelle) ha URI e handler ma **nessun generatore di richiesta e nessun call-site applicativo**; nessuna procedura aggiorna le `CONF_*` | `WSTypeHandler.java:45,64,146`; assenza di `Richiesta7001XmlGenerator` |

### Due punti da segnalare

- **Ambiguità nel corpus pubblicato.** Due identificativi hanno due file ciascuno. Il 135 è un refuso
  nel nome del file (contenuto identico). Il **134 ha contenuto diverso** fra le due varianti — il
  valore `4` è «Altro» in `dec_dichiarante_trascr_nascita` e «Tutore» in
  `dec_dichiarante_trascr_postuma`. Il capitolo lo segnala come verifica da fare al primo caricamento
  e per questo la chiave locale è presa su `(ID_DECODIFICA, NOME)` e non sul solo identificativo.
- **`/config/decodifica/data_adesione` non è replicabile.** Restituisce la data di adesione di **un**
  comune per volta, non un elenco: resta una consultazione a runtime. È però l'unica delle «regole non
  replicabili localmente» elencate al cap. 9 per cui esista un servizio dedicato — il capitolo lo
  annota senza contraddire §9.3, che già la colloca fra le consultazioni.

---

## Cosa fare all'apertura del documento

1. Aprire `ANALISI_Integrazione-ANSC_v2.2.docx` in Word.
2. **Aggiornare il Sommario (F9 → «Aggiorna intero sommario»)** e verificare i numeri di pagina.
3. Controllare la resa della nuova tabella di §9.2 (casi d'uso), delle tabelle del nuovo cap. 10 e
   della colonna «Stato» nel registro Open Point: la larghezza complessiva delle tabelle è stata
   mantenuta, ma l'impaginazione va verificata a video.
4. Verificare che il nuovo capitolo 10 sia numerato come tale e che i capitoli successivi risultino
   rinumerati da 11 a 18 (la numerazione è automatica, legata agli stili di titolo).
5. La v2.1 non è stata modificata (SHA-1 invariato) e resta disponibile per il confronto.

**Stato finale del documento:** 18 capitoli, 49 tabelle, 13 file multimediali e 11 immagini in linea
(invariati), 10 note a piè di pagina, 26 open point.
