# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Natura del workspace

**Questo NON è un codebase**: è un workspace per la **redazione di documentazione tecnica di
analisi** per il Dipartimento Trasformazione Digitale di Roma Capitale (progetti IT per la
Pubblica Amministrazione — es. Area Stato Civile, Patente a Crediti, integrazione SIPO-ANSC).
Non ci sono build/lint/test. Il "prodotto" sono documenti `.docx`/`.xlsx`. Lingua: **italiano**.

## Ruolo delle tre cartelle (distinti, non intercambiabili)

- **`Template documentale/`** — **STANDARD NORMATIVO**. I file qui (a partire da
  `template_DAD_roma-capitale.docx`) definiscono struttura, stili, sezioni obbligatorie, tono e
  formato che ogni documento finale DEVE rispettare. È la *forma* da seguire, non contenuto da
  copiare. Contiene anche esempi compilati (`INL-DAD - Decurtazioni Patente a Crediti`,
  `PLO02 Integrazione SIPO-ANSC`) e un template Excel (`INL- PdT - SAC2-027.xlsm`).
- **`Sorgenti Documentali/`** — **BASE DI EVIDENZA**. Documenti (docx, pdf, tabelle) e sorgenti
  applicative (codice, config, docker-compose) da cui ricavare i contenuti. Ogni affermazione
  tecnica del documento finale deve poter essere ricondotta a una di queste sorgenti. La cartella
  **cresce nel tempo**: nuovi file possono arrivare in qualsiasi momento.
- **`Documenti finali/`** — **OUTPUT VERSIONATO**. Qui si salvano i documenti prodotti, con
  versione nel nome (es. `DAD_<cliente>_v0.1.docx`). **Mai sovrascrivere** una versione
  precedente: si crea una nuova versione.

## Come leggere/scrivere i file (comandi utili)

Sono disponibili `python-docx` (1.2.0), `openpyxl` (3.1.5), **`PyYAML`** e **`Pillow` (PIL, 11.3.0 arm64)**. I
`.docx`/`.xlsx` sono binari zip: non modificarli con Edit/sed — usa Python. **`python3` è arm64
(3.9, `/usr/bin/python3`)**: la wheel di Pillow deve essere arm64. Se `from PIL import Image` desse
`incompatible architecture (x86_64)`, reinstallare la wheel giusta con
`/usr/bin/python3 -m pip install --user --force-reinstall --no-cache-dir pillow` (già fatto una
volta in questa sessione). Con Pillow **si generano diagrammi/immagini reali** (non solo tabelle o
ASCII) e si inseriscono nel `.docx` via `run.add_picture(png, width=Inches(...))`. Niente
matplotlib/graphviz. Utile poter **leggere il PNG generato con lo strumento immagini** per
verificarne la resa prima di inserirlo (fatto per il flow diagram §3.2 dell'analisi ANSC).

```bash
# Testo grezzo veloce da un .docx
unzip -p "file.docx" word/document.xml | sed 's/<[^>]*>/ /g' | tr -s ' '

# Ossatura strutturata (heading + stili + tabelle)
python3 -c "import docx; d=docx.Document('file.docx'); [print(p.style.name, p.text) for p in d.paragraphs if p.text.strip()]"
```

Note pratiche apprese su questo workspace:
- Lo stile paragrafo per gli elenchi in `template_DAD_roma-capitale.docx` è **`List Paragraph`**
  (non esiste `List Bullet`). Attenzione: clonando un paragrafo con `copy.deepcopy(p._p)` si eredita
  lo stile di origine — **reimposta sempre `np.style`** dopo l'inserimento, altrimenti righe di
  contenuto finiscono come `Heading` e inquinano il TOC.
- Il TOC del template è un campo Word: si aggiorna aprendo il file in Word (F9), non da script.
- Un file `~$*.docx` nella cartella indica che il documento è **aperto in Word** → non
  sovrascrivibile finché non viene chiuso.
- Nel tracciamento `.xlsx`, aggiungendo una riga con `openpyxl` lo stile **non** si eredita: copiare
  `font`/`border`/`fill`/`alignment` dalla riga precedente con `copy()`. Aggiornare sempre anche il
  foglio `Legenda` (totale voci e conteggi per stato/priorità), che non si ricalcola da solo.
- ⚠️ **`SPEC_API_Integrazione-ANSC_*.docx` NON si edita a mano**: è un **artefatto generato** dai
  contratti OpenAPI. Per modificarlo si toccano i `.yaml` e si riesegue
  `/usr/bin/python3 "Documenti finali/genera-spec-api.py"` dalla root del workspace. Vale la regola
  dello standard API: «il manuale di riferimento non si redige: si genera». È l'unica eccezione al
  principio «si modifica il file reale».
- 🔁 **RILETTURA DI COERENZA (fatta il 28/08 sulla v3.8 → v3.9)**: `verifica-conteggi.py` copre i
  **numeri dichiarati** e i riferimenti pendenti, **non** la coerenza redazionale. Controlli aggiuntivi
  che hanno prodotto risultati e che conviene rifare: (a) **DDL ↔ tabelle «Colonna | Tipo | Note»**
  (mancavano i campi tecnici in 5 tabelle su 9 e 2 colonne di `ANSC_NOTIFICA`); (b) **rimandi a
  capitoli per titolo** — ⚠️ **l'utente rinomina i capitoli editando il .docx**, e i rimandi nel testo
  restano al vecchio nome (è successo con «Le due superfici» → «SIPO vs la web app ANSC»);
  (c) **grafie oscillanti** (`back-office`/`backoffice`/`BackOffice`); (d) **termini superati**
  (`outbox`, `worker`, `dead-letter`, `casistica`, `COD_CASISTICA`, `ANSC_UC`, `ANSC_REGOLA`) —
  attenzione ai falsi positivi: molte occorrenze sono negazioni volute («non un worker automatico»);
  (e) **difetti descritti al presente ma già corretti** nella stessa versione; (f) caporali e parentesi
  sbilanciate **escludendo i paragrafi in Courier New**, altrimenti il DDL sommerge il risultato.
  Script: `revisione.py` (ogni sostituzione dichiara le occorrenze attese e si ferma se non
  tornano) — **perso con la ripulitura dello scratchpad**; la primitiva sopravvive come
  `sostituisci(..., attese=n)` in `Documenti finali/strumenti/docx_comune.py`.
- ✅ **PRIMA DI CONSEGNARE UNA NUOVA VERSIONE di un `.docx`, esegui il controllo dei conteggi**:
  ```bash
  /usr/bin/python3 "Documenti finali/verifica-conteggi.py" "Documenti finali/<file>.docx"
  ```
  Esce **1** se trova discordanze. Verifica tre cose: (a) i **numeri scritti in prosa** contro le
  tabelle vere (flussi, unità di deployment, concentratori, componenti nuovi, open point, requisiti,
  operazioni, categorie, capitoli) e contro il **repository ANSC** (file di decodifica, identificativi
  distinti, righe); (b) i **riferimenti pendenti** — ogni `OP-nn`/`RF-n`/`RNF-n` citato deve esistere
  nella tabella che lo definisce, ogni `PC-n` deve avere il suo paragrafo, ogni `[Rn]` deve stare in
  Riferimenti (è il controllo che avrebbe intercettato il duplicato OP-27); (c) heading anomali e
  righe di tabella vuote. **I numeri in prosa non si aggiornano da soli quando si aggiunge una riga a
  una tabella: è la classe di errore più frequente su questi documenti** (è costata le versioni
  v2.6→v2.8, e un dato sbagliato nella v2.9). Aggiungere una regola = una riga nella lista `REGOLE` in testa allo script.
  Nota: la tabella «Storia del Documento» è **esclusa** di proposito, perché cita per mestiere le
  formulazioni superate. ⚠️ In python-docx `document.tables` **restituisce un oggetto `Table` nuovo a
  ogni accesso**: per escludere una tabella confronta `t._tbl`, non l'oggetto (`t is not x` è sempre
  vero e non esclude nulla).
- ⚠️ **GLI SCRIPT NON VANNO NELLO SCRATCHPAD — stanno in `Documenti finali/strumenti/`.** Lo
  scratchpad è **di sessione e viene ripulito**: il 03/09/2026 la ripulitura ha fatto perdere *tutti*
  i generatori (diagrammi, capitoli, revisione). Documenti e immagini incorporate erano al sicuro,
  gli script no. Da allora esistono due moduli durevoli, da usare e da estendere invece di
  riscrivere le stesse primitive:
  - **`strumenti/diagrammi_comune.py`** — disegno PIL: palette `C` (grigio/blu/rosso/giallo/verde/
    viola come coppie bordo/fondo), `INK`/`MUTED`/`ARROW`, font Arial da
    `/System/Library/Fonts/Supplemental`; `tela()` (titolo+sottotitolo già impaginati), `box`,
    `scheda` (usata dagli ERD), `pila`, `rombo`, `banda`, `percorso`/`linea`/`freccia`, `legenda`,
    `avvolgi`. ⚠️ Le stringhe di testo visualizzato usano il **doppio apice**, così l'apostrofo
    tipografico ’ (U+2019) non rompe il sorgente.
  - **`strumenti/docx_comune.py`** — python-docx: `h()` (heading per livello+testo), `indice_di`,
    `trova_tabella`, `tabella_colonne`, `para`/`voce`/`ddl`/`tabella`/`immagine`, `clona_riga`,
    `sostituisci(attese=)`, **`sostituisci_immagine(didascalia, png)`** (riscrive il blob senza
    rigenerare il .docx), `storia`, `riepilogo`.
  Ogni versione ha il suo script `strumenti/v3_NN_*.py`, che importa i due moduli.
- ⚠️ **WORKBOOK GRANDI: `openpyxl.Workbook(write_only=True)`, altrimenti il processo viene ucciso.**
  In modalità ordinaria openpyxl tiene ogni cella in memoria come oggetto: la mappatura di nascite e
  morti fa ~26.000 righe × 30 colonne e il generatore è stato ucciso **due volte** per esaurimento
  memoria prima di arrivare al salvataggio (03-04/09/2026). In streaming il picco scende da GB a
  **215 MB**. `foglio()` in `strumenti/workbook_mappatura.py` è ora **bimodale** e va usata così.
  ⚠️ In write_only larghezze di colonna, `freeze_panes` e altezza della riga 1 vanno impostati
  **prima del primo `append`** (openpyxl chiude lì la testata del foglio e le ignorerebbe), mentre
  `auto_filter.ref` si scrive alla fine ma va calcolato contando le righe, perché `ws.max_row` non
  esiste; le celle si stilano creandole con `WriteOnlyCell(ws, value=...)`, non tornando indietro.
  ⚠️ Concausa da controllare quando la memoria manca: l'estensione Oracle Java di VS Code tiene un
  processo `java` da **5,2 GB** sul priming build dei 139 `pom.xml` (`ps -Ao rss,comm -r | sort -rn`).
- Scrivendo YAML a mano, attenzione agli **scalari in linea non quotati che contengono `,` o `: `**
  (dentro `{ ... }` o dopo `chiave:`): rompono il parsing. Correttore riusabile: `fix_yaml.py`
  (quota descrizioni in linea, scalari a blocco e voci `- { codice: ... }`) — **perso** con lo
  scratchpad, da riscrivere in `strumenti/` se riserve.
- I `.docx`/`.xlsx` **binari non sono raggiungibili da `grep`**: per cercare un termine in tutto il
  workspace serve estrarre l'XML dallo zip (attenzione: `sed` fallisce con *illegal byte sequence*
  su questi file — usare Python). Nel codice Java, valutare anche l'accesso via **reflection**
  (`getMethod("getXxx")`), che sfugge alla ricerca del nome di campo.

## Stato attuale del lavoro

**FOCUS CORRENTE — riparti da qui**: analisi/progettazione della nuova componente **SIPO → ANSC**
(scrittura degli atti su ANSC). Documento di lavoro: **`Documenti finali/ANALISI_Integrazione-ANSC_v3.30.docx`**
— **base corrente, si modifica IL FILE REALE via python-docx** (NON rigenerare da script: contiene edit
manuali e **26 commenti** di Word da preservare). Dalla v3.22: catalogo delle logiche (`TIPO_DOMINIO` +
`VALORI_DOMINIO`, da NON confondere con i dizionari), `ANSC_CFG_SEZIONE`, `ANSC_XREF` eliminata (OP-25
chiuso), cap. 6 = «Il flusso operativo», punto di attenzione sui documenti e sulla firma (OP-57/58/59).
Dalla v3.23: **quattro fasi** con condizione di uscita (UC identificato → documenti → validazione →
firma, dopo la quale l’atto è bloccato in SIPO), **`COD_FASE` accanto a `STATO`**, `NUM_COMUNALE` e
`COD_ORIGINE_UC` sullo store, testata del modello evento (idTipoEvento = prima cifra dell’UC),
**`ALLEGATI_USECASE`** di Side al posto di `ANSC_CFG_ALLEGATO` (OP-50 bloccante, OP-60/61).
Dalla v3.24-3.25: ricerca e **lettura per chiave** sui dizionari (`cercaValori`,
`leggiValoreDizionario`; `ansc-dizionari-v1.yaml` a 8 operazioni; `nm_dominio` nella chiave, perché 2
identificativi su 143 coprono due tabelle) e
ALLEGATI_USECASE che richiama l’UC **per valore** (l’ERD dichiarava una FK inesistente); OP-62 = i
contratti sono ancora alla nomenclatura «operazioni/casistica».
Dalla v3.26: il catalogo delle logiche è `TIPO_LOGICHE_DI_SCELTA`/`LOGICHE_DI_SCELTA` (OP-56
chiuso), con il **dominio 3 = logica dei campi**; nuova `RICONCILIAZ_DIZIONARI` (OP-59 chiuso);
`CHIAVE_ANTI_DUPLICATO` eliminata → **OP-63**. Dalla v3.27: back-office riallineato (UC ambiguo
scelto dall'operatore, 11 categorie, COD_FASE nei filtri), **comandi anche da CLI**, raccordo
riconciliazione ↔ tabelle `CONF_*` di SIPO (OP-64); wireframe in `strumenti/diagrammi_backoffice.py`.
Dalla v3.29: «documenti extra» → **atti a testo libero** (`fg_testo_libero`), **aggancio**
di un atto formato sulla web app (R005 all'avvio della stesura) e **stacco del numero comunale**
(OP-66). Script `strumenti/v3_2*_*.py`. Metodo: dopo ogni modifica il TOC
va rigenerato in Word (F9); ⚠️ `/usr/bin/python3` non parte (licenza Xcode): usare
`/Library/Developer/CommandLineTools/usr/bin/python3`.

**v2.0 = correzione di impianto sostanziale (NON reintrodurre il modello v1.0).** La v1.0 disegnava la
scrittura verso ANSC come **corsia asincrona non presidiata** (outbox→worker→backoff→DLQ→sweep), copiata
da ANPR. **È SBAGLIATO**: ANSC è presidiato. Tre motivi verificati sui sorgenti `ansc/docs/` (contratto
1.53.0): (a) **R009 non è un dry-run** — `/validazione/evento` deposita la bozza e restituisce `idAnsc`
(id nazionale); R011 `/evento/elimina` la cancella logicamente; (b) **la firma R007 richiede OTP per
singolo atto** (`ParametriFirma.inputFirma3`) → non automatizzabile; (c) la modalità **M2M** (Allegato 4
D.M. 18/10/2022) è solo per **letture/code** (es. scarico comunicazioni). **NON esiste** chiave di
idempotenza ANSC (`idOperazioneComune` = tracciamento), né batch, né caricamento del pregresso.
Modello corretto (**SIPO-centrico**, deciso con l'utente): l'operatore lavora nelle **maschere SIPO
esistenti**; ANSC è un **passo di finalizzazione** dell'atto (compila → definisci → R009 deposito bozza+idAnsc
→ R007 firma con OTP → atto formato), non un sottosistema attorno a cui riorganizzare il lavoro. La ex-worklist
è **declassata a "store di stato ANSC per atto"** (`ANSC_OUTBOX` = attributo dell'atto, non coda) + vista di
**supervisione**; il back-office è supervisione/eccezioni, non superficie di lavoro. Esiti indeterminati →
**riconciliazione R005/R011, mai retry cieco**; automazione solo su letture (R008/R021/R024/R901/R004/R005).
RF-9 = **pre-filtro** locale, non sostituto di R009.
**Flusso TOKEN OTP (deciso): NON esiste servizio di login.** L'USC genera l'OTP (4h) sulla **web app OTP di
ANSC** (smart card/SPID, dalla postazione, lato FE) → il **FE trasmette l'OTP al concentratore**, che lo
custodisce come risorsa di sessione (USC+postazione). **Il concentratore (BE) costruisce e firma il JWT Bearer
+ JWS Detached** con la **chiave privata del PKCS#12 del certificato server** (payload: sub, postazione, sede
ISTAT, OTP, x5c) e chiama ANSC. **Il FE non parla mai con ANSC né firma.** Acquisizione OTP **lazy** (alla prima
op. senza OTP valido); gestione di scadenza/invalidazione (timeout invalida l'OTP → rigenerazione da web app).
Concentratore `all-ansc-sipo` **rafforzato** (unico luogo dove risiedono PKCS#12 server + OTP di sessione +
registro postazioni; certificato server unico obbligato alla scala di Roma). Fonti: `ansc/docs/Note/SpecificheTecnicheServiziCooperativiJWT`
(OTP 4h, JWT Bearer RFC 6750, JWS Detached, x5c, postazione=CN cert, sede=ISTAT, firma RS256 con chiave privata PKCS#12).

Capitoli v2.0: 1. Scopo (+ «Modifiche rispetto alla v1.0») · 2. Premesse (RF-1…9, RNF; RNF-2 riscritto,
RNF-5 rimosso) · 3. **Vincoli imposti dal contratto ANSC** (NUOVO, 9 sottosezioni, tutto citato) ·
4. Architettura (flusso §3.2 presidiato) · 5. Deployment K8s · 6. Lift-and-shift + disamina · 7. Modello
dati (`ANSC_USR`: outbox→worklist/xref/audit + Configurazione) · 8. Mappatura payload · 9. **Modello di
esecuzione: percorso presidiato in SIPO e sessione OTP** (sostituisce il Worker; include sottosez.
«Il passo Finalizza», «Sessione OTP e token», «Errori in fase di formazione e logiche di recupero») ·
10. Decisioni (PC-1/2/3/5/7; PC-4/PC-6 rimossi) · 11. Sicurezza (+ certificati postazione/server) ·
12. Open Point (**22**) · 13. Back-office ridotto (**vista di supervisione** con wireframe, audit, config,
registro postazioni; niente cruscotto KPI/DLQ/sweep) · 14. Roadmap · App. A (DDL, senza colonne di
ritentativo/DLQ, + **esempio di popolamento Config del pilota**) · App. B (API, **ripulita dai residui
async v1.0**: deposita-bozza → 200 CONFERMATO+idAnsc / 200 KO RIFIUTATA, tracciabilità con timeline reale
R001→R005→R009→R006→R007). **Diagrammi §3.2 e
ciclo di vita: RIFATTI** fedeli alle figure ufficiali ANSC (Figura 4/5, decodifica ANSC_11), PIL arm64.

**Struttura v3.13 (24 capitoli)**: 1. Scopo · 2. Premesse (RF-1…**RF-12**, RNF-1…7) · 3. Vincoli contratto
ANSC · 4. Architettura · 5. Deployment K8s · 6. Porting K8s di SIPO · 7. Disamina difficoltà del porting ·
8. Modello dati · 9. Mappatura payload · **10. Le regole di determinazione e di controllo (NUOVO v3.0)** ·
11. Gestione dei dizionari ANSC (dalla v2.2) · **12. Il versionamento della configurazione (NUOVO v3.2)** ·
13. Modello di esecuzione · **14. Il flusso in ingresso: notifiche, comunicazioni e solleciti (NUOVO v3.3)** ·
**15. Le due superfici: SIPO e la web app ANSC (NUOVO v3.4)** ·
**16. Le funzioni offerte da ANSC (NUOVO v3.5, generato dai contratti)** ·
**17. Schede dei servizi ANSC per lo sviluppo (NUOVO v3.6, 23 sezioni di 2° livello)** ·
18. Decisioni (PC-1/2/3/5/7/8/9/**10**) · 19. Sicurezza · 20. Open Point · 21. Back-office · 22. Roadmap · App. A (DDL: operative, configurazione, **dizionari**) · **App. B (dalla v2.7 = INVENTARIO
delle 45 operazioni, generato dai contratti OpenAPI: convenzioni, contratti e governo, inventario per
componente, corrispondenza servizi ANSC, «che cosa è cambiato»)**. Stato doc: **24 cap., 126 tabelle, 20 immagini, 52 OP**.
⚠️ **Concentratori = 2, unità di deployment nuove = 3** (i due concentratori + il **processo di
automazione**) + ricevitore notifiche (eventuale, OP-03) + broker (opzionale). La tab. «Componenti»
(§4.3) elenca i componenti **logici** e ha la colonna «Unità di deployment autonoma» che li distingue
dalle parti interne (gestore sessione OTP, client ANSC) e dallo store su Oracle; la tab. «Topologia»
(§5.1) elenca le sole **unità di deployment**. Dalla v2.8 le due tabelle sono riconciliate: non
contare i componenti da una sola delle due.
⚠️ **App. B NON contiene più i JSON di richiesta/risposta**: erano una seconda fonte che divergeva dai
contratti. Il dettaglio delle operazioni sta nei `.yaml` [R7] e in `SPEC_API_Integrazione-ANSC_v0.1.docx` [R8].
Le tabelle di inventario sono **generate** dai `.yaml` (script `aggiorna_v27.py`, **perso con lo
scratchpad**): se cambiano i contratti, vanno rigenerate — riscrivendo lo script in `strumenti/`, non
ricopiando a mano.

**Vista di supervisione (cap. Back-office)**: worklist delle **eccezioni** (atti non conclusi nel percorso
ordinario), NON superficie di lavoro (quella = maschere SIPO). Categorie = tassonomia errori: Da riprendere
(R005→R007), Indeterminati (R005→R011), Rifiutati validazione (correggi+rideposita), Bloccati allegato/soggetto,
Firma non riuscita. Dettaglio atto = stato reale R005 + timeline audit + **azioni contestuali determinate dallo
stato**. Wireframe PIL `bo_supervisione.png`. **Ripartizione firma/ruoli TAGLIATA → OP-22** (l'utente deve
chiedere all'organizzazione: deleghe di firma); categoria «Bloccati su soggetto» condizionata a **OP-20** (R018).

**Configurazione = risposta alla pre-verifica (RF-9, già nell'impianto)**: `ANSC_CFG_OPERAZIONE` (una riga
per atto = evento×operazione×casistica) + `ANSC_CFG_CAMPO` (`CAMPO_ANSC ↔ CAMPO_SIPO`, `FLG_OBBLIGATORIO`,
`COND_OBBLIGATORIETA`, `COD_DECODIFICA_ANSC`, `MESSAGGIO`). `/ansc/preverifica` legge CFG_CAMPO → errori
campo-per-campo. ANSC nel `model_evento` NON dichiara obbligatorietà (tutti opzionali): sta in R023/R009, la
config la materializza localmente. **Struttura c'è, manca il CONTENUTO = OP-14.** App. A ha ora un **esempio
di popolamento pilota** (morte/DICH_ABITAZIONE/Morte_001: INSERT operazione + 16 righe CFG_CAMPO; col.
ATTO_DECESSO verificate, SOGGETTO/dichiarante/sede indicative → OP-14). NB: **R002 = certificazione, NON
deposito** (il deposito è R009) — verificato negli OpenAPI, corretto ovunque nel doc.

**DIZIONARI ANSC — RF-10, secondo componente `dec-ansc-sipo` (cap. 10, dalla v2.2; separazione resa
esplicita ovunque nella v2.6).** ⚠️ **Il sistema è diviso in due parti, non confonderle**: la **parte
operativa** (`all-ansc-sipo`: pre-filtro RF-9, sessione OTP, orchestrazione R009→R007) e la **parte
dizionari** (`dec-ansc-sipo`: recupero delle decodifiche via **R901 su comando manuale**, mai schedulato,
e carico in `ANSC_DIZ_CATALOGO`/`_VALORE`/`_CARICAMENTO`). Il componente dizionari **non detiene il PKCS#12
e non costruisce token**: chiama R901 **per il tramite di `all-ansc-sipo`**, che resta l'unico luogo della
firma JWT/JWS. Tre motivi della separazione: ciclo di vita diverso (operazione lunga e rara vs sessione
sincrona presidiata), consumatori diversi (i dizionari servono a **tutto SIPO**), dominio di guasto diverso
(un aggiornamento fallito non deve impedire la formazione degli atti). **Fruizione da SIPO = base dati, non
API**: vista `V_ANSC_DIZ_VALIDO` (applica la validità temporale) raggiunta **per sinonimo con grant di sola
lettura**; gli endpoint `/ansc/v1/dizionari/*` servono back-office e diagnosi, NON le maschere. Scelta
motivata in **PC-8**, che ne dichiara anche la tensione con la critica al «DB come bus di integrazione»
del cap. 7. Il raccordo `ANSC_CFG_CAMPO.COD_DECODIFICA_ANSC` → catalogo è **per valore, senza FK, di
proposito** (una FK riunificherebbe i domini di guasto). I dizionari **non sostituiscono le `CONF_*`** e
**non portano comuni/province/stati/nazionalità** (titolarità ANPR, restano in `ANAG_USR` → la traduzione
degli stati passa sempre per `CONF_STATO_ESTERO.CODICE_ANPR`). RF-10 è **prerequisito di Fase 1** della
roadmap: senza dizionari in locale il pre-filtro RF-9 non funziona.

**SPECIFICA DELLE API DI TUTTI I POD (20/08/2026)** — metodologia: **`Documenti finali/Naming_convention_X_API_v1.00.docx`**
(scheda di operazione = **15 elementi obbligatori**, Tavola 9; vocabolario chiuso dei verbi, Tavole 7-8;
**«il manuale di riferimento non si redige: si genera»**, §6.1; il documento OpenAPI è la **fonte
autoritativa dei nomi**). Prodotti: **`ansc-v1.yaml`** (`all-ansc-sipo`, 34 op.), **`ansc-dizionari-v1.yaml`**
(`dec-ansc-sipo`, 6 op.), **`ansc-automazione-v1.yaml`** (processo di automazione, 5 op.) = **45 operazioni**;
**`SPEC_API_Integrazione-ANSC_v0.1.docx`** generato da **`genera-spec-api.py`**.
**Decisione di impianto: UN SOLO contesto `/ansc/v1` + UN contratto per pod.** Il percorso esprime il
**dominio**, non il modulo — principio di *opacità dell'implementazione* dello standard: «i nomi non
esprimono né il nome della tabella, né quello della classe, **né quello del modulo**». Il contratto invece
segue il deployable, perché con esso è versionato. Il **ricevitore notifiche non ha contratto**: realizza un
contratto di terzi (ANSC), fuori dal perimetro dello standard.
**Operazioni progettate ora perché MANCAVANO in App. B della v2.6**: **`firmaAtto`** (R006/R007 — mancava
proprio il passo che *forma* l'atto), allegati (`creaAllegato`/`elencaAllegati`/`leggiAllegato` = R001 +
attesa della scansione antivirus), **`PUT /ansc/v1/sessione`** (consegna dell'OTP dal FE al concentratore,
prevista dall'architettura ma senza interfaccia), `annullaAtto` (R011), `creaPostazione`, e l'intero pod di
automazione. **Correzioni di conformità**: `GET .../riconciliazione` → **`POST .../riconciliazioni`** (una
GET non può modificare lo stato, RFC 9110); rimossa `POST /back-office/atti/{id}/verifiche`, duplicato
funzionale della preverifica. **3 scostamenti dichiarati** (nome dei file di contratto, segmento di
raggruppamento `back-office`, sottorisorsa generica `azioni`) e **7 punti aperti PS-1…PS-7**; il più pesante
è **PS-1 = OP-23** (senza OTP per letture/code: è *condizione di esistenza* del pod di automazione).
**Lacuna dello standard rilevata applicandolo → PS-6**: il segmento `back-office` non è né contesto né
collezione e la regola di composizione dell'URI (§3.1) non lo contempla, pur essendo introdotto dal cap. 6
dello standard stesso.

**REGOLE E NOMENCLATURA UC/MODELLO (v3.0-3.1, 25/08/2026) — cap. 10, RF-11, PC-9.**
⚠️ **Nomenclatura vincolante**: **UC** = struttura di **ANSC** (codice numerico 11111000, codice motore
`Dic_Nasc_001`); **Modello** = struttura del **Comune di Roma** (`CONF_TIPO_ATTI.ID_MODELLO_ATTO`, con la
maschera in `MASCHERA_UI`). Rinominati `COD_CASISTICA`→**`ID_MODELLO_ATTO`** e
`COD_EVENTO_ANSC`→**`COD_UC_ANSC`**; «caso d'uso»→«UC». NON toccare «modello dati», «modello evento»,
«modello di esecuzione»: designano altro.
**Il problema**: la corrispondenza Modello→UC **NON è biunivoca**. Ricognizione nascite
(`Sorgenti Documentali/Nascite_ANSC_07.08.2026.xlsx`, 4 fogli = 4 cluster): **102 UC**, di cui **90 su 15
Modelli** (rapporto 6) e **12 senza Modello**. Es.: Modello 30 + tipo atto 1515 → `Dic_Nasc_001/002/003`
secondo **`FLG_NATO_MORTO`** e **`FLG_MORTO_PREDENUNCIA`** (entrambi `CHAR(1)` S/N, e ⚠️ **stanno sul
SOGGETTO, non sull'atto** → `AttoNascitaSoggettoModel`; da qui OP-31 sul parto plurimo).
**⚠️ SIPO HA GIÀ UN MOTORE DI REGOLE** (DBD §2.2.10-16): `CFG_RULEAPP_FORMULA`, `CFG_RULEGEN_FORMULA`,
**`CFG_MAP_RULECTL_MODELLO`** (associa rule↔Modello!), con `FLG_MANDATORY` (AND) / `FLG_AGGREGATE` (OR) e
`ID_RULE_GEN` documentato come **«RULE per sottocasistiche»**. Le sue rule sono però **script in
`SCRIPT_EXECUTION VARCHAR2(4000)`** e stanno in `MATR_USR`.
**Decisione PC-9**: si riusa la **semantica** (3 specie, MANDATORY/AGGREGATE, concatenamento) ma con
**condizioni dichiarative** `campo/operatore/valore` in `ANSC_USR` → nuove **`ANSC_CFG_REGOLA`** +
**`ANSC_CFG_REGOLA_CONDIZIONE`**. `ANSC_CFG_OPERAZIONE` guadagna **`ID_MODELLO_ATTO VARCHAR2(5)`**
(era `COD_CASISTICA VARCHAR2(30)`), **`ID_CONF_TIPO_ATTO`** e **`MASCHERA_UI`** — i tre campi
confermati dall'utente; la chiave di unicità resta per Modello, perché la riga è una per Modello e
la scelta fra i suoi UC spetta alle regole. Scartati: motore di mercato (le condizioni sono congiunzioni di uguaglianze:
nessuna inferenza) e riuso diretto delle `CFG_RULE*` (script non manutenibili dai funzionari → RF-11;
`MATR_USR` riunificherebbe i domini di guasto di PC-8). Prezzo accettato: **niente espressioni composte**
— AND implicito fra le condizioni, OR = due regole. Guadagno: la regola è **un dato**, quindi verificabile
per **copertura e mutua esclusione** (è ciò che avrebbe intercettato le 12 incoerenze → OP-33).
**La preverifica diventa a DUE FASI**: (1) regole di DETERMINAZIONE → sceglie l'UC; (2) campi obbligatori
dell'UC + regole di CONTROLLO. Le regole si valutano **nel concentratore**, non in PL/SQL (il DB come
luogo di logica è il rischio trasversale del cap. 7). Le GENERAZIONE calcolano i derivati alla costruzione
del payload. Governo: **funzionari del Comune** dal back-office (schermata «Regole» con copertura,
mutua esclusione e **simulazione** su atto reale), versionamento bozza→attivazione come la Configurazione.

**⚠️ QUALE STANDARD DB VALE — v1.01, NON v1.00 (verificato 25/08/2026).** I due documenti prescrivono
per il **modello fisico** regole **incompatibili**: v1.00 = `COD4_nome_SUFFISSO` (ANA/DAT/TYP/STO/CNF),
colonne `codice_tabella_nome`, PK `codice_tabella_PK`; **v1.01 = grammatica a prefissi**
`ANSC_[MARCATORE_]nome`, colonne `PREFISSO_RUOLO_nome`, PK `PK_nome_tabella`. Contro la v1.00 lo schema è
**non conforme su 11 tabelle su 11**. Vale la **v1.01** (`Documenti finali/Naming_convention_X_DB_v1.01.docx`,
citata come **[R5]**): non è una revisione minore — dichiara che «la v1.00 non trattava gli oggetti diversi
da tabelle, colonne, chiavi e indici» e **contiene un capitolo su `ANSC_USR`** (verifica condotta sulla v2.2
dell'analisi, allineamenti recepiti nella v2.3). ⚠️ Se il Comune imponesse la v1.00 non sarebbe una rinomina
ma un rifacimento: da decidere prima di procedere.
**Regole della v1.01 da applicare** — Tavola 1 marcatori di tipo: `(assente)`=dati operativi · `ANA`
anagrafica · `CFG` configurazione · `DIZ` dizionario · `STO` storico · `LOG` log. Tavola 2 prefissi di
colonna: `ID_ COD_ DESC_ FLG_ DATA_ NUM_ TXT_ UTENTE_` (assenti solo per stati/fasi/esiti). Tavola 3:
`PK_ FK_ UK_ CK_ IX_`. Tavola 4: `V_ MV_ SEQ_ TRG_ PKG_ PRC_ FNC_ JOB_ RL_`. **Chiave surrogata = `ID_` +
nome tabella SENZA prefisso di modulo E SENZA marcatore** (la Tavola 9 dichiara conforme `ID_AUDIT` per
`ANSC_LOG_AUDIT`) → `ID_OPERAZIONE`, `ID_CAMPO`, `ID_CATALOGO`, `ID_REGOLA`. Campi tecnici (Tavola 6):
`DATA_INS`/`DATA_UPD`/`UTENTE_INS`/`UTENTE_UPD` su operative e configurazione, log esentata.
**v3.1 = allineamento**: `ANSC_REGOLA`→**`ANSC_CFG_REGOLA`**, `ANSC_REGOLA_CONDIZIONE`→
**`ANSC_CFG_REGOLA_CONDIZIONE`**, `ANSC_UC`→**`ANSC_ANA_UC`** (mancava il marcatore); chiavi
`ID_CFG_OPERAZIONE`→`ID_OPERAZIONE` e `ID_CFG_CAMPO`→`ID_CAMPO`; prefissi `COD_CAMPO_DESTINAZIONE`,
`TXT_ESPRESSIONE`, `NUM_PRIORITA`; campi tecnici aggiunti a `ANSC_DIZ_VALORE` e `ANSC_DIZ_CARICAMENTO`.
⚠️ **NON rinominate** ~20 colonne preesistenti senza prefisso di ruolo (`DESCRIZIONE`, `MESSAGGIO`,
`VALORE`, `CAMPO_SIPO`, `MASCHERA_UI`, `SERVIZIO_ANSC`…): ricorrono su più tabelle e una rinomina parziale
peggiorerebbe la coerenza → **OP-35**, da fare in un solo intervento.

**⚠️ IL MODELLO DATI DELLA CONFIGURAZIONE È IN TRE MONDI (v3.0). Non agganciare i campi al Modello.**
`ANSC_CFG_OPERAZIONE` = **lato Comune**, una riga per Modello (evento, operazione, `ID_MODELLO_ATTO`,
`ID_CONF_TIPO_ATTO`, `MASCHERA_UI`) · `ANSC_CFG_REGOLA` = **il ponte** (Modello → UC secondo i dati) ·
**`ANSC_ANA_UC`** = **lato ANSC**, catalogo degli UC (codice, `COD_MOTORE`, descrizione, famiglia), e
**`ANSC_CFG_CAMPO` pende da `ANSC_ANA_UC`** (FK `ID_UC`, non più dall'operazione).
**Perché**: l'obbligatorietà è dichiarata **per UC** e differisce fra UC dello stesso Modello — verificato
su **15 Modelli su 15**, in media 4 insiemi distinti ciascuno (es. Modello 30 → 44/45/46 campi). ⚠️ **Correzione (06/09)**: `luogoFiliazione` è obbligatorio
in `Dic_Nasc_001` (nato vivo) **e in `Dic_Nasc_002` (nato morto)**, e NON in `Dic_Nasc_003` (nato vivo
e poi deceduto) — verificato riga per riga sul mapping. È l'**unico** campo che distingue i tre UC.
Agganciare i campi al Modello costringerebbe a scegliere un solo insieme e perdere gli altri.

**⚠️ ALLEGATI PER UC — `ANSC_CFG_ALLEGATO` (v3.11, 28/08/2026, cap. Mappatura, OP-50/51).**
**Il problema**: un Modello indirizza a UC diversi secondo i dati, e **ogni UC richiede allegati diversi**
→ l'elenco dei documenti dipende dall'**UC determinato**, non dal Modello.
⚠️ **QUASI TUTTO SI EREDITA DA ANSC, dallo STESSO file che già importiamo per i campi**: il tracciato del
mapping ha una sezione **«Allegati»** con le stesse colonne di obbligatorietà e condizione. Numeri
verificati: **346 UC su 374** dichiarano allegati · **1.569 righe** · **320 obbligatorie** · **499 con
condizione** · **125 descrizioni distinte** · dizionario dei tipi **ANSC_09 = 128 valori** (+ ANSC_08 stati,
ANSC_10 formati). ⚠️ **Le condizioni hanno la stessa grammatica delle regole** (`campo,operatore,valore`,
es. `evento.datiEventoCittadinanza.tipoDichiarante,=,3`) → **le valuta lo stesso motore, senza scrivere
nulla di nuovo**.
**Che cosa NON si eredita** (poco, ed è OP-50): il **raccordo descrizione→codice ANSC_09** — 119 su 125
combaciano **dopo aver normalizzato accenti, apostrofi tipografici e spazi**, ne restano **6** da raccordare
a mano una volta sola; e il **contrassegno di inclusione nell'attestazione di conformità**
(`flagInclusoAttConformita` in `ModelAllegatoRif`), che il mapping non dichiara ed è scelta del Comune.
**Tabella nuova `ANSC_CFG_ALLEGATO`**: pende dall'**UC** (FK `ID_UC`) e dalla **baseline** (FK
`ID_VERSIONE`), come `ANSC_CFG_CAMPO`; UK `(ID_VERSIONE, ID_UC, DESCRIZIONE)` — la chiave è la
**descrizione**, perché è così che il mapping li nomina. **Niente schermata nuova**: «Campi per UC» diventa
**«Campi e allegati per UC»** e la stessa importazione popola entrambe.
⚠️ **LACUNA ADIACENTE — LE FORMULE**: il mapping dichiara anche le **formule ministeriali** per UC
(**366 UC su 374, 233 formule distinte**, con una colonna di note sull'obbligatorietà) e **non le
configuriamo**. Le decodifiche ANSC_119/120 hanno **2 valori ciascuna** e **non sono** quel catalogo →
**OP-51**.

**⚠️ IL MODELLO EVENTO È LA SPINA DORSALE — cap. 9, §«Il modello evento» (v3.13, 03/09/2026).**
⚠️ **Equivoco da non ripetere: NON esiste una struttura di payload per UC.** `openapi/model_evento.yaml`
è **un solo albero**, radice unica `ModelEvento`, e vale per tutto lo stato civile. Cifre **verificate**
(non stimarle di nuovo): **90 schemi**, **3.734 righe**, **111 proprietà di primo livello** (57 scalari,
47 oggetti, 7 liste), **8.256 percorsi distinti** (espansione ricorsiva, liste contate una volta,
ricorsione troncata alla ripetizione di uno schema; **7.190** escludendo i rami `*ML`), **382 riferimenti
interni** (`ModelSoggetto` e `ModelAttoCollegato` **49 volte ciascuno**, `ModelEnteDichiarante` 31),
**38 schemi ML su 90**, **19 occorrenze di `deprecated: true`** (⚠️ 6 al primo livello; contarle con
`grep`, non con un parser che guardi solo `properties`: **2 sono annidate in `allOf`** — ci sono cascato).
**16 contratti su 25** lo referenziano, **10 lo usano intero** (R004/R005/R009/R010/R011/R013/R015/R016/
R017/R020); `ModelEventoRidotto` (27 proprietà) sta in R005.
**È un superset discriminato**: `idUsecase` sceglie il caso, la forma non cambia; **nessun `oneOf`, nessun
`discriminator`, nessun campo obbligatorio a livello di schema** → **chi valida deve conoscere l'UC**.
I 374 UC usano **2.958 percorsi distinti = 35,2 %** dell'albero (40,5 % senza i rami ML); per singolo UC
da **14 a 674**, mediana **154**.
**Conseguenza di disegno**: il payload **non si costruisce per UC**, si costruisce **una volta sull'albero**
e si riempie dalla configurazione → **un solo adattatore di mappatura**, non uno per famiglia. Ogni ramo
`if` per famiglia è configurazione mancata.

**⚠️ CONTROLLO DI RISOLVIBILITÀ MAPPING↔MODELLO (v3.13) → OP-52.** Risolvendo `Binding Object`+`Binding
Field` sull'albero: **2.958 percorsi distinti, 2.910 risolti, 48 no** (232 occorrenze, 55 UC; **nessuno
tocca la morte**, quindi il pilota è salvo). Due classi, e **solo la prima si risolve da sé**:
(a) **indice di lista omesso** — 4 percorsi, 157 occorrenze, tutti `evento.datiAnnotazione.*`, che nel
modello è una **lista** di `ModelDatiAnnotazione`: la normalizzazione degli indici li risolve;
(b) **divergenza vera** — 44 percorsi, 75 occorrenze: **37 sotto `datiEventoMatrimonio.regimePatrimoniale`**
(`ModelRegimePatrimoniale` ha 14 proprietà e **non ha `assistenteLegale`**), `formatoDataEvento`/
`idFormatoDataEvento` (⚠️ il **changelog 1.53.0 li dichiara aggiunti a `ModelMatrimonio` e non ci sono**),
`datiEventoUnioneCivile.appartenenzaCognomeComune`/`posizioneCognomeComune` (UnCiv_009),
`trascrizioneUnioneCivile.sessoPrima`/`sessoDopo` (Trascr_UnCiv_006),
`trascrizioneCittadinanza.altraCittadinanzaRiacquistata` (Citt_024).
⚠️ **Regola di disegno scritta nel documento: i riferimenti non risolti si RIPORTANO, non si scartano**
— scartarli in silenzio dà una configurazione che *sembra* completa.
⚠️ **E la colonna SIPO si RIPORTA dalla versione attiva** a ogni rigenerazione: è l'unico lavoro umano
accumulato e l'unica cosa che una reimportazione può distruggere.

**LE FONTI DELLA CONFIGURAZIONE (tabella in cap. 9, v3.13) — nessuna si redige, tutte si importano**:
`openapi/model_evento.yaml` (struttura) · `openapi/R001–R024, R901` (25 contratti → `SERVIZIO_ANSC`) ·
`Mapping_casi_uso/3_dec_use_case.csv` (ANSC_03 → `ANSC_ANA_UC`) · `Mapping_casi_uso/<famiglia>/<motore>.csv`
(**374 file, 67.674 righe, 7 colonne** → `ANSC_CFG_CAMPO` + `ANSC_CFG_ALLEGATO`) · `changelog_mapping.md`
(66 revisioni) · `Decodifiche/` (145 file → `ANSC_DIZ_*` **via R901**, i CSV sono il riscontro) ·
`Changelog.md` (194 rilasci) · **`CONF_TIPO_ATTI` di SIPO** (l'unica fonte del Comune → `ANSC_CFG_OPERAZIONE`).
**Il lavoro umano è dove le fonti tacciono, e sono tre cose**: completare la **colonna SIPO**, raccordare
le **6 descrizioni di allegato** senza tipo (OP-50), scrivere le **~374 regole** di determinazione.

**⚠️ ERD E CHIAVI (v3.10, 28/08/2026) — cap. Modello dati, §«Schema delle relazioni» e §«I legami con
SIPO»** (diagrammi PIL `erd_ansc_usr.png`, `erd_legami_sipo.png`; lo script `diagrammi_erd.py` è **perso con
lo scratchpad** — le sue primitive sono in `strumenti/diagrammi_comune.py`, `scheda()` in particolare).
⚠️ **L'ERD VA RIGENERATO A OGNI MODIFICA DEL MODELLO DATI**: è già successo due volte di lasciarlo
indietro (la v3.11 aggiungeva `ANSC_CFG_ALLEGATO` e la figura restava quella della v3.10 — se ne è
accorto l'utente). **Modello dati e diagramma sono una coppia, non due artefatti.** Per sostituire
l'immagine senza rigenerare il documento si riscrive il blob della parte
(`doc.part.related_parts[rId]._blob = open(png,'rb').read()`): è `sostituisci_immagine()` in
`strumenti/docx_comune.py`.
**FK dichiarate in ANSC_USR: 8** (dalla v3.11 anche `CFG_ALLEGATO.ID_UC` e `.ID_VERSIONE`) — — `LOG_AUDIT.ID_STATO_ATTO`→STATO_ATTO · `CFG_CAMPO.ID_UC`→ANA_UC ·
`CFG_CAMPO/CFG_OPERAZIONE/CFG_REGOLA.ID_VERSIONE`→CFG_VERSIONE · `CFG_REGOLA_CONDIZIONE.ID_REGOLA`→REGOLA ·
`DIZ_VALORE.ID_CATALOGO`→DIZ_CATALOGO. ⚠️ **Le due FK su CFG_OPERAZIONE e CFG_REGOLA sono state aggiunte
dalla v3.10**: disegnare l'ERD ha reso visibile che `ID_VERSIONE` era vincolata solo su CFG_CAMPO.
**TRE riferimenti PER VALORE, e ognuno ha la sua ragione — non sono dimenticanze**: (1)
`COD_DECODIFICA_ANSC`→DIZ_CATALOGO = non riunificare i domini di guasto (PC-8); (2) `COD_UC_ANSC` su
CFG_OPERAZIONE e CFG_REGOLA = si nomina il **codice pubblicato da ANSC**, non la riga locale, così la
configurazione può nominare un UC prima che il catalogo sia ricaricato; (3) **`ANSC_STATO_ATTO.ID_VERSIONE`
= timbro storico**, deve sopravvivere all'archiviazione delle baseline vecchie.
**Legami con SIPO: NESSUNA FK attraversa gli schemi.** Tre escono (`ID_ATTO_SIPO` · `ID_CONF_TIPO_ATTO`/
`ID_MODELLO_ATTO`/`MASCHERA_UI` verso `CONF_TIPO_ATTI` · `CAMPO_SIPO` come testo `TABELLA.COLONNA`), **uno
solo entra**: `V_ANSC_DIZ_VALIDO`, letta per sinonimo in sola lettura. Motivi: domini di guasto separati,
cicli di vita diversi, schemi in esercizio da non toccare.

**⚠️ EMERGENZA — DUE ISTITUTI DA NON CONFONDERE (v3.8, 28/08/2026, RF-15, OP-47/48/49).**
⚠️ **La parola «emergenza» NON compare in nessuna fonte ANSC** (guide, note, contratti, changelog,
decodifiche): il registro di emergenza è un **istituto dell'ordinamento**, non una funzione della
piattaforma. ⚠️ **La citazione «art. 10 del D.M.» delle versioni ≤3.7 NON è verificabile** (il testo del
D.M. non è fra le sorgenti; l'unico «art. 10» presente è del **DL 78/2015**, che istituisce l'ANSC) →
**rimossa ovunque**, sostituita da rinvio a **OP-49**.
**Ma ANSC HA un meccanismo di rientro, che il documento ignorava.** Tre campi del modello evento:
**`motivoRecupero`** (decodifica **ANSC_96**), `descrizioneMotivoRecupero`, **`idAttoCartaceo`** («id Atto
Cartaceo **registro temporaneo**», esempio `123 p1 sA-2025 999999`; aggiunto solo nel **1.41.0, giugno
2025**). ANSC_96 = **6 valori**: **1 Indisponibilità del sistema GESTIONALE** (⚠️ ANSC prevede il caso in
cui a essere giù siamo NOI → risponde a OP-42) · 2 Atto fuori casa comunale · **3 Caso d'uso non previsto
nel sistema centrale** (caso nuovo, si lega a OP-32 dal verso opposto) · 4 Indisponibilità del sistema
centrale · 5 **DISATTIVATO** (fine validità 31/12/1999 < inizio) · 101 ALTRO.
⚠️ **IL VEICOLO DEL RIENTRO È IL CASO D'USO DI SERVIZIO**: `motivoRecupero` è obbligatorio in **10 mapping
su 374**, e sono **esattamente i 10 casi d'uso di servizio** (`*_999*`, `Morte_999` compreso). Non è un
contenitore per casi strani: è il modo in cui ANSC accoglie un atto formato fuori percorso **obbligando a
dichiararne la ragione**.
**MODALITÀ DI EMERGENZA (modello Milano, riferito dall'utente e assunto nel documento)**: ogni atto può
essere messo **temporaneamente** in emergenza, riceve un **id locale** (nessun identificativo nazionale
consumato), le verifiche dipendenti da ANSC sono sospese (**compresa la ricerca del soggetto/comparenti**),
le **letture verso ANSC restano possibili**, **niente carta**. ⚠️ **UNA COSA NON È MAI ESEGUIBILE: la
chiusura/firma dell'atto** — è il vincolo che regge tutto: **in emergenza si PREPARA, non si FORMA**, quindi
non è un registro parallelo ma una minuta.
⚠️ **CORREZIONE FATTA AL MODELLO**: «saltare alcune verifiche» al rientro va spaccato in due. Le verifiche
**locali** si possono saltare (ANSC le rifà al deposito); **la ricerca del soggetto R005 NO**: senza
`idAnscSoggetto` gli automatismi non scattano e serve `/collegamento/evento`, che la nota ANSC definisce
«fortemente sconsigliato». **Al rientro R005 è obbligatoria.**
⚠️ **CHE COSA LA MODALITÀ NON RISOLVE: i TERMINI.** Se il fermo supera il termine, l'atto è tardivo comunque
→ scatta la **comunicazione alla procura** (ANSC_26 tipo 3). È lì che serve il registro di emergenza
dell'ordinamento. **Non confondere i due piani**: è un rilievo da verificazione delle prefetture.
**Store**: 4 colonne nuove su `ANSC_STATO_ATTO` (`FLG_EMERGENZA`, `ID_ATTO_EMERGENZA`,
`COD_MOTIVO_RECUPERO`, `DATA_INGRESSO_EMERGENZA`); **decima** categoria di eccezione «In emergenza da
rientrare». Diagramma PIL: `emergenza.png`. Aperti: **OP-47** numerazione comunale durante l'emergenza (lega
OP-44), **OP-48** termine massimo di permanenza (senza, l'archivio diventa un secondo registro), **OP-49**
base normativa.

**⚠️ PRENOTAZIONE IDANSC / PARTO PLURIMO — §R009 del cap. 16 (v3.7, 27/08/2026).**
⚠️ **`/prenota/evento` NON riserva numeri: CREA GLI ATTI.** La guida: «restituisce gli identificativi unici
nazionali … e **predispone gli atti** di ciascun gemello»; la risposta torna `listaIdEvento` **e**
`listaIdAnsc`. Dopo la chiamata esistono in ANSC **N atti in BOZZA**.
**Perché esiste** (non è la numerazione): `evento.datiDiNascita` porta **`attiGemelliPrec[]`** e
**`attiGemelliSucc[]`** = idAnsc dei fratelli. Il primo atto deve citare l'id del secondo e viceversa, e
ANSC non consente aggiornamenti → **dipendenza circolare**, che solo l'assegnazione anticipata spezza.
**Prassi degli altri comuni (detta dall'utente)**: si prenotano tanti atti quanti i gemelli, poi ciascuno
si **conferma** (compilazione → R009 validazione → firme) **oppure si CHIUDE**. ⚠️ **La chiusura non ha
un'operazione propria: si usa R011** (`/evento/elimina`) → ANNULLATO, e **l'identificativo resta consumato**.
**Sei vincoli operativi verificati**: (1) è il **caso d'uso di servizio `11999999`** → `Dic_Nasc_999.csv`,
e ⚠️ la guida dice «nessun dato obbligatorio salvo l'intestatario» ma il mapping ne dichiara **33** (contro
46 di `Dic_Nasc_001`), obbligatori **in quanto condizionati alla presenza della sezione**; (2) la **minuta
(`composizioneCompleta`) è obbligatoria**, con formule ministeriali 35/36/37 e **gli identificativi dei
gemelli scritti a mano** (errore → solo nota tecnica, quindi web app); (3) **firma dichiarante SOLO
cartacea** (R012 escluso); (4) **un gemello alla volta**, si passa al successivo dopo la propria firma →
trigemino = 3 finalizzazioni, la sessione OTP deve reggerle; (5) **numeri comunali in blocco e in anticipo**
→ aggrava OP-44; (6) ⚠️ **`progressivoGemello` e `numeroGemelli` NON compaiono in NESSUNO dei 374 mapping**
→ la configurazione importata non li avrà mai, li valorizza il concentratore.
**Effetti sul disegno**: N righe in `ANSC_STATO_ATTO` **subito dopo la prenotazione**, in stato **BOZZA**
(possibile perché la v3.4 ha esteso il dominio degli stati); la **chiusura riusa `annullaAtto`**; va
aggiunta al contratto la sola **prenotazione**. **OP-31 PARZIALMENTE RISOLTO** (verso ANSC = **un atto per
nato**); nuovo **OP-46** = `[DA VERIFICARE]` con quale campo la validazione riconosca la bozza prenotata
(`id` o `idAnsc`, entrambi «assegnati dal sistema») — sbagliare non dà errore, dà un **duplicato**.
⚠️ Storia instabile: `idContenitore` «per legare i gemelli» aggiunto nel 1.9.0 e **rimosso senza che il
changelog lo dichiari**; prenotazione corretta nel 1.23.0.

**⚠️ SCHEDE DEI SERVIZI PER LO SVILUPPO — cap. 17 (v3.6, 27/08/2026).** Una **sezione di 2° livello per
ciascuno dei 23 servizi** (esclusi **R022/R023 DMNM**, su indicazione dell'utente), struttura fissa:
spiegazione · tabella operazioni (percorso, che cosa fa, corpo, effetti) · **Prerequisiti** · **Modalità di
adozione** · **Trappole** · **Riferimenti** · **Uso nel disegno**. Fonte: `Caratteristiche_servizi/*.pdf`
(che sono il **rendering dei contratti**: stessa fonte del `.yaml`, non aggiungono nulla) + guide + note.
**Trappole che vale la pena non riscoprire** (tutte verificate): **ANSC_08 stato allegato = 5 valori, e
solo «Inserito» (3) consente di proseguire**; ⚠️ **`idModalitaInput` di R007: «in chiaro» NON sarà
accettato in produzione → usare base64 da subito**, il collaudo negli ambienti inferiori non lo fa emergere;
**R010 anteprima e R011 cancellazione richiedono l'INTERO ModelEvento**, non un identificativo; **R002
certificazione porta `parametriFirma`** → emettere un certificato consuma un OTP di firma; **R018 primo
schema: `properties` accanto ad `allOf` invece che dentro** → alcuni generatori di client la ignorano e
producono una richiesta vuota; **R024: gli schemi di risposta ripetono i campi della richiesta** (residuo
di copiatura, non fidarsi); **R016 rifiuto ≠ scarto in validazione** (lo stato RIFIUTATA non si valorizza
su un HTTP 400); R901 restituisce il contenuto **compresso** per default.
`[DA VERIFICARE]` in R006: se esista un termine per la firma USC dopo quella del dichiarante (il changelog
cita «2 ore», il contratto no).

**⚠️ LE FUNZIONI OFFERTE DA ANSC — cap. 16, inventario GENERATO dai contratti (v3.5, 27/08/2026).**
⚠️ **Non confondere due inventari**: **App. B = le NOSTRE 45 operazioni** (3 pod); **cap. 16 = le 57
operazioni di ANSC** su **25 contratti**. Sono conteggi diversi.
Le tabelle del cap. 16 sono **generate** dai `.yaml` (script `cap_api_ansc.py`, **perso**; dizionario
`CURATE` per la semantica in italiano): **alla revisione dei contratti si rigenerano**, non si ricopiano.
**Nove famiglie funzionali** (somma = 57): Deposito 9 · Firme 7 · Allegati 3 · Consultazione e anteprima 10
· Certificazione 6 · Adempimenti 10 · Ciclo di vita 4 · Canale sanitario DMNM 4 · Configurazione 4.
**Il disegno usa 10 servizi su 25.**
**Caratteristiche trasversali verificate**: **tutte POST**, comprese le letture · **ogni percorso porta
`{version}`** (nessuna eccezione) e **solo 2 operazioni** hanno anche `revision` in query (R005
intestatario, R008 getNotificheByEvento) · testata comune con `nomeApplicativo/versione/fornitore` ·
**nessuna idempotenza** · paginazione uniforme · **21 codici** in `Codici d'errore.xlsx` · **3 ambienti**
(produzione, preproduzione, **mock locale**) · **l'identità viene dal token, non dal corpo**.
**⚠️ R009 — approfondimento**: 3 operazioni (`/validazione/evento` deposita, `/collegamento/evento` è il
**recupero** del CASO 3, `/prenota/evento` per il parto plurimo e **richiede in ingresso i numeri
comunali** → lega OP-31 e OP-44). Il **modello evento** ha **111 proprietà di primo livello**, **48
blocchi**, **19 proprietà deprecate** (fra cui `operatore*`).
⚠️ **Il `forcingCode` è più pericoloso di quanto sembri**: permette di depositare un atto anomalo, **ma**
la nota ANSC dichiara che «per atti anomali il flusso non è stato ancora implementato» → l'atto entra in
ANSC e **il ciclo delle conferme (annotazioni + comunicazione anagrafica) non è previsto**. **OP-21 e OP-41
vanno letti insieme.**
**⚠️ IL DEPOSITO È UNA FAMIGLIA, NON UN SERVIZIO**: **7 operazioni su 6 servizi** portano un evento in ANSC
(R009 validazione, R013 ×2 rettifica/annotazione modificativa, R015 adozione internazionale, R016
provvedimento di rifiuto, R017 correzione di annotazione, R020 adozione multi intestatario). **Il
concentratore ne conosce UNA.** Basta per il pilota, non per il dominio → **OP-45**. È il **quinto**
elemento nuovo per famiglia, che il cap. Roadmap non elencava.

**⚠️ LE DUE SUPERFICI: SIPO E LA WEB APP ANSC — cap. 15, RF-14 (v3.4, 27/08/2026).**
**Visione del Comune (detta dall'utente): il sistema è SIPO-centrico, NON ANSC-centrico.** L'oracolo sono
le tabelle di SIPO; l'atto si registra in SIPO e **poi** si trasferisce ad ANSC via API. La web app ANSC
**copre tutti gli UC e sarebbe un'alternativa completa** al gestionale (l'adesione fa scegliere «web
application **oppure** gestionale comunale»): **Roma l'ha esclusa per ora** — è una scelta **organizzativa,
non tecnica**, e può cambiare.
⚠️ **MA SIPO NON È L'UNICO SCRITTORE VERSO ANSC.** Sei funzioni restano sulla web app comunque:
generazione OTP · **nota tecnica** · **annullamento per inefficacia** · certificati emissibili · allegati
errati · avvisi di sistema. **Le prime tre cambiano stato o contenuto di un atto senza passare da noi.**
**⚠️ DIFETTO CORRETTO NELLA v3.4 — gli stati erano 6 su 11.** `ANSC_11` dichiara **11 stati**; il vincolo
di `ANSC_STATO_ATTO` ne ammetteva **6** e **non poteva registrare `INEFFICACE`**, cioè l'esito di una delle
due funzioni solo-web-app. Mancavano anche `BOZZA`, `FIRMATO PER CONFORMITÀ`, `CANCELLATO`,
`GENERATO DA SISTEMA`, `APPROVATO` (le ultime due servono ora che gestiamo le annotazioni). Ora il CHECK ne
ammette **12** (gli 11 di ANSC + `IN_PREPARAZIONE`, che è nostro e non ha corrispondente). **Lo stato non è
un dato nostro: è una replica di un dato altrui e va accolto per intero.**
**⚠️ SESSIONE OTP: l'unità di verifica è l'AZIONE** (attività avviata da un comando di SIPO, qualunque
sequenza di chiamate ANSC richieda), non la chiamata né l'atto. OTP riusato finché valido. **Timer del
tempo residuo nelle maschere SIPO** (`GET /ansc/v1/sessione` restituisce già `dataScadenza` e
`numMinutiResidui`) + **soglia di guardia**: sotto un margine minimo configurabile (**proposta 15 min**) si
chiede un OTP nuovo *prima* di iniziare, per non rompersi a metà sequenza. ⚠️ Argomento da ricordare: per
la **formazione** la presenza è già provata **due volte** (OTP di sessione + OTP di firma remota Aruba, per
singola firma) → **non serve legare la sessione al singolo atto**; dove la sessione è l'**unica** prova è
nelle azioni dispositive **senza firma** (conferma/rifiuto notifica).
**Riconciliazione: SOLO SU RICHIESTA** (deciso con l'utente) + **adempimento organizzativo**: chi usa la web
app per nota tecnica o annullamento per inefficacia **riconcilia subito dopo** dal back-office. Prezzo
dichiarato: se salta il passo, il disallineamento resta invisibile. Appiglio diagnostico per le note
tecniche: `R005 /consultazione/ansc/evento/note/tecniche`.
**Web app a TUTTI gli USC che formano atti** (deciso): «vai sulla web app» è un'istruzione praticabile.
**Duplicazione del cruscotto = conseguenza ACCETTATA e motivata**, non omissione: la scrivania ANSC conosce
gli eventi, non le pratiche (niente atto SIPO, niente municipio, niente atti non ancora depositati).
Diagramma PIL: `sup_superfici.png`.

**⚠️ IL FLUSSO IN INGRESSO ANSC → COMUNE — cap. 14, RF-13, PC-10, `ANSC_NOTIFICA` (v3.3, 27/08/2026).**
⚠️ **CORREZIONE**: `ansc-automazione-v1.yaml` diceva «le notifiche allineano lo stato, non formano atti»,
effetti nulli. **È SBAGLIATO** (stessa famiglia dell'errore v1.0). La nota ufficiale
`ansc/docs/Note/Nota_Processo_Flusso_Conferma` dice l'opposto: **la conferma è un atto di volontà dell'USC**
che (a) collega l'annotazione all'atto primario e (b) **sblocca la comunicazione anagrafica**. Base normativa:
DM 18/10/2022 punto **B.5.1**.
**⚠️ IL CANCELLO ANAGRAFICO**: «la comunicazione anagrafica **non verrà inviata** all'ufficio anagrafe se
prima non verranno confermate **tutte** le notifiche da parte dei comuni coinvolti»; **un solo rifiuto** →
l'atto **non ha alcuna conseguenza anagrafica**. Una notifica pendente blocca un effetto giuridico **su
un'altra persona, in un altro comune**.
**⚠️ TRE situazioni di notifica, non due** (fonte `NotaProcessoAnnotazioniAndQuickCoopServiceFlow` §2.1.1):
① Roma detiene l'atto primario digitale → **proposta di annotazione**; ② Roma è comune di residenza →
**presa visione** (**non si trascrive più**); ③ **Roma ha formato l'atto e il primario è CARTACEO → ANSC
notifica a Roma STESSA**: conferma + scarico dell'annotazione (R005/R010) + **invio per PEC** al comune che
la stampa e la incolla. ⚠️ **③ è il caso ORDINARIO in adesione progressiva**, non il residuale.
**⚠️ R005 PRIMA DI R009 è obbligatorio**: senza `idAnscSoggetto` gli automatismi non scattano (CASO 3) e
serve `/collegamento/evento` (R009) come recupero — «fortemente sconsigliato» registrare senza.
**Limiti del contratto R008**: **nessuna conferma massiva** (una chiamata per notifica, corpo = solo
`idNotifica`); **nessun campo per la motivazione del rifiuto**; **l'identità è la sessione** (ANSC registra
`nomeusc/cognomeusc/codicefiscaleusc` dell'ufficiale autenticato; nel ModelEvento i campi `operatore*` sono
**DEPRECATI** con nota «vengono usati i dati dell'ufficiale autenticato»).
`getNotificheByEvento` + flag **`tuttiComuni`** = l'unico modo per sapere se gli **altri** comuni hanno
confermato le notifiche generate da un atto formato da Roma → seconda sezione della schermata.
**DECISIONI PRESE CON L'UTENTE (27/08)**: **PC-10 = le notifiche si lavorano nel NOSTRO back-office**
(R008 completo, in sessione OTP dell'USC), **conferma SINGOLA** (niente selezione multipla: darebbe
l'apparenza di un atto unico dove ce ne sono N → costo proporzionale al volume, **OP-38**);
**comunicazioni ad altri enti = FUORI PERIMETRO** (**OP-39**: serve l'interfaccia verso protocollo/PEC del
Comune; ci ricade anche l'invio PEC della situazione ③).
**Comunicazioni** = 7 tipi (ANSC_26: prefettura, comune di residenza, procura fuori tempo massimo, ISTAT,
ASL, INPS, procuratore); **R003 si interroga per singolo `idAnsc`, NON per intervallo di date**; restituisce
il PDF in **base64** con protocollo. **Solleciti** = R021 sola lettura, stati ANSC_124 (Da visionare/Gestita/
**Scaduto**): ⚠️ **il termine che determina «Scaduto» non è pubblicato → OP-40**.
⚠️ **«Per atti anomali il flusso non è stato ancora implementato»** — dichiarato **due volte** nella nota
ANSC → **OP-41** (si lega a OP-21 sul `forcingCode`).
Decodifiche: ANSC_101 genere (6 valori, **il flusso di conferma usa 1=Annotazione e 2=Trascrizione**),
ANSC_102 stato (DA APPROVARE/APPROVATO/RIFIUTATA/INEFFICACE), ANSC_105 canale (DIGITALE/PEC), ANSC_112
stato rifiuto, ANSC_124 sollecito, **ANSC_93 = notifiche ANAGRAFICHE SC01…SC18** (altro dominio, va
all'ufficio anagrafe). Diagrammi PIL: `not_situazioni.png`, `not_cancello.png`.

**⚠️ IL VERSIONAMENTO DELLA CONFIGURAZIONE — cap. 12, RF-12, nuova `ANSC_CFG_VERSIONE` (v3.2, 27/08/2026).**
**La configurazione NON è un carico iniziale, è un flusso.** Numeri verificati su `ansc/docs/` (16/10/2023 →
30/06/2026): **194 rilasci datati** (mediana **4 giorni**), di cui **66 toccano il mapping dei casi d'uso**
(≈ 22/anno, **una ogni 17 giorni**); UC modificati per revisione **mediana 11, media 42, max 301**; **11
revisioni su 65 hanno toccato >100 UC**; **355 UC su 374 toccati almeno una volta**; morte (pilota) **23 UC
su 25, 151 interventi**; **34 versioni** del modello evento (ANSC_100); **3 UC ritirati** in tutto.
⚠️ Verifica incrociata da ricordare: i 3 «casi uso rimossi» del changelog = le 3 righe di **ANSC_03 con
`DATAFINEVALIDITA` chiusa** → **ANSC non cancella un UC, gli chiude la validità**.
**Intercetto — 4 canali, nessuno basta da solo**: ① `R901 /config/decodifica/elenco` restituisce un campo
**`versione` PER CIASCUNA tabella** (era ignorato: è l'appiglio che rende l'intercetto una sola chiamata
leggera) — vede ANSC_03 e ANSC_100, **non** l'obbligatorietà; ② **`Mapping_casi_uso/changelog_mapping.md`**
= **il diff campo-per-campo GIÀ CALCOLATO da ANSC**, grammatica fissa (`## Casi uso aggiunti/rimossi/
modificati`, `### Modifiche per il caso uso <fam>/<UC>.csv`, `* Aggiunto '<path>' (riga:N)`) → **non
calcoliamo il diff, lo leggiamo**; è l'**unico** canale che veda l'obbligatorietà ed è **fuori perimetro**;
③ runtime (`50002 USECASE_NOT_FOUND`, `50001`, `400001`) = **intercetto tardivo**, il cittadino è già allo
sportello; ④ **Avvisi di sistema** della web app: **nessuna API** fra le 57 operazioni → presidio umano.
⚠️ **Nessun codice d'errore segnala una `idVersion` obsoleta** (21 codici in `Codici d'errore.xlsx`).
**VINCOLO scritto nel documento** (deciso con l'utente): il pod `dec-ansc-sipo` **deve raggiungere
github.com/italia/ansc** in HTTPS sola lettura → **OP-36**. Se negato, l'intercetto ridiventa umano: il
documento lo dice invece di nasconderlo.
**Soluzione = BASELINE VERSIONATA PER COPIA INTEGRALE** (stati **BOZZA / ATTIVA / STORICA**, una sola ATTIVA).
Principio: **si versiona ciò che il Comune decide** (`ANSC_CFG_OPERAZIONE`, `ANSC_CFG_CAMPO`,
`ANSC_CFG_REGOLA`+`_CONDIZIONE`) · **si replica con validità temporale ciò che ANSC dichiara**
(`ANSC_ANA_UC`, `ANSC_DIZ_*`). ⚠️ **Scartata la catena di delta**: risparmia spazio che non serve e rende
ricorsiva ogni lettura. La nuova versione **copia** la precedente (portandosi dietro il lavoro umano sui
`CAMPO_SIPO`) e applica **solo il delta** pubblicato.
⚠️ **Il versionamento era già presente a metà, non governato**: `ANSC_CFG_OPERAZIONE.COD_VERSIONE`,
`ANSC_CFG_REGOLA.COD_VERSIONE`, `ANSC_ANA_UC.COD_VERSIONE_MAPPING`, `ANSC_STATO_ATTO.COD_VERSIONE_CONFIG`
erano **quattro stringhe libere** e `ANSC_CFG_CAMPO` non ne aveva alcuna. La v3.2 aggiunge
**`ANSC_CFG_VERSIONE`** (governo) e trasforma le colonne in **`ID_VERSIONE` FK**; `ANSC_CFG_CAMPO` guadagna
`ID_VERSIONE` **nella chiave di unicità** (`ID_VERSIONE, ID_UC, CAMPO_ANSC`) — è ciò che fa coesistere le
versioni. Indice unico su funzione per «una sola ATTIVA». Il rollback è un **cambio di stato**.
**Ciclo**: sentinella → bozza (copia+delta) → **report d'impatto** (Modelli coinvolti · campi nuovi senza
`CAMPO_SIPO` · regole che perdono copertura · UC ritirati ancora referenziati) → il funzionario lavora
**solo i buchi** → controlli copertura/mutua esclusione → attivazione. **Chi attiva = USC**, schema
organizzativo del Comune → **OP-37** (stesso criterio di OP-22: forniamo la funzione, non le deleghe).
Il capitolo **risponde a OP-13** (come restare allineati); **OP-14** resta (contenuto iniziale).
Nuova categoria di eccezione **«Configurazione disallineata»** (9 in tutto) e schermata **«Versioni della
configurazione»** (14 in tutto). Diagrammi PIL: `ver_ciclo.png`, `ver_baseline.png`.

**VOLUMI DELLA CONFIGURAZIONE (decidono il disegno del back-office)** — nascite / intero dominio:
UC da catalogare **90 / 374** · righe di mappatura **16.934 / oltre 60.000** · campi obbligatori
**4.690 / 20.346** · **regole di determinazione ~90 / ~374**.
⚠️ Il confronto fra l'ultima riga e le altre È l'indicazione di disegno: **le regole si scrivono a mano**
(poche, 2-3 condizioni, è lì che serve il giudizio del funzionario), **i campi si importano** (20.346: chi
li immettesse a mano creerebbe divergenze dal mapping ufficiale). Perciò `importaCampi` **non è una
comodità ma il meccanismo principale di popolamento**, e la schermata dei campi è **superficie di
revisione** (completa il lato SIPO), non di immissione.
**Back-office — 13 schermate**: «Configurazione — operazioni»→**«Modelli»**; «campi»→**«Campi per
UC»**; nuova **«Catalogo UC»** (sola consultazione: è ciò che ANSC dichiara); «Dettaglio atto» mostra
**l'UC determinato + la regola che l'ha prodotto**; «Regole».
**Categorie di eccezione: da 6 a 8** — **«UC non determinato»** (nessuna regola scatta: può essere il dato
o una lacuna nelle regole) e **«UC ambiguo»** (più regole con esiti diversi: è **sempre** configurazione,
l'operatore non può sbloccarlo). Entrambe prevenibili dai controlli di copertura/mutua esclusione
all'attivazione della versione.

**Numeri decodifiche VERIFICATI su `ansc/docs/Decodifiche/` (usare questi, non stime)**: **145 file CSV**,
**143 identificativi distinti**, **1.376 righe di dato**. Tracciati: **140 standard**
(ID/DESCRIZIONE/DATAINIZIOVALIDITA/DATAFINEVALIDITA/ORDINAMENTO), 3 con solo ID+DESCRIZIONE, 1 con
`IDTIPOCONTENUTO` (casi d'uso), 1 con `CODICECONSOLATO` (consolati) → le 2 colonne extra stanno in un
attributo JSON. ⚠️ **Identificativi ripetuti**: `134` copre **due tabelle diverse**
(`dec_dichiarante_trascr_nascita`, `dec_dichiarante_trascr_postuma`) e `135` due file che differiscono per
un refuso; `model_evento.yaml` referenzia **ANSC_134 in modo condizionato al caso d'uso** (usecase 1351 e
1317). Perciò l'unicità del catalogo è su **`(COD_DECODIFICA_ANSC, NOME)`** e non sul solo codice,
altrimenti il carico completo violerebbe il vincolo. Risoluzione per caso d'uso = **OP-28**.

**⚠️ LA STRUTTURA DEI DATI DI R901 — verificata il 04/10/2026 su `ansc/docs/openapi/R901_config_decodifica.yaml`
(v1.5.0) + `base_servizi.yaml` + il corpus. NON rifare la verifica, e NON cercarla nel contratto: per metà
non c'è.** Entrambe le operazioni sono **POST** e portano `{version}` nel percorso.
**`/config/decodifica/elenco/{version}`** — richiesta: **solo l'involucro**, nessun parametro proprio.
Risposta: `elenco[]` di **`ModelSintesiDecodifica`**, **tre campi, tutti stringa**: `id` ("1", è l'ANSC_nn) ·
`descrizione` ("dec_tipo_evento") · **`versione`** ("1.4.0", la versione della singola tabella — è l'appiglio
dell'intercetto delle revisioni). `id`+`descrizione` compongono **esattamente** il nome del file nel
repository: `1_dec_tipo_evento.csv`.
**`/config/decodifica/dettaglio/{version}`** — richiesta: `idDecodifica` · `formato` (solo `'csv'`
documentato, default csv) · `compressione` ('true'/'false', **default `true`**). Risposta: `idDecodifica`,
`formato`, `compressione` e **`contenuto`: `type: string`, «Il contenuto binario, base64»**. ⚠️ **Il
contratto si ferma qui: la struttura dei dati NON è dichiarata.** Si ricava solo dal corpus — ed è la
ragione per cui non si trova.
**Involucro comune** (`base_servizi.yaml`): `AnscRequest` = `testataRichiesta` (idComune,
idOperazioneComune, dataOraRichiesta, nomeApplicativo, versioneApplicativo, fornitoreApplicativo) +
`datiPaginazione`; `AnscResponse` = `testataRisposta` (idComune, idOperazioneComune, idOperazione,
**idEsito**) + `datiPaginazione` + `errors[]`.
**Il CSV dentro `contenuto`**: separato da **virgola**, prima riga di intestazione, **tutti i campi fra
doppi apici**, date `YYYY-MM-DD HH:MM:SS.0`, fine validità aperta = `9999-12-31`. ⚠️ **Non è un tracciato,
sono quattro** (vedi il blocco precedente): chi assume cinque colonne **fallisce su 5 file su 145**.
⚠️ **Tre lacune da dichiarare a chi implementa**: (a) **l'algoritmo di compressione non è nominato in alcuna
fonte** — cercato `gzip|zip|deflate` ovunque, zero riscontri — e il default è `true`, quindi è il caso
ordinario, non l'eccezione; (b) **`id` non è una chiave**: 143 identificativi per 145 file, quindi chiedendo
il dettaglio di `134` o `135` **non è determinato quale file si ottenga** (è OP-28, ma sta a monte, nel
servizio, non solo nel nostro modello); (c) gli identificativi **non sono densi**: vanno da 1 a 183 con
**40 buchi**, quindi non si può iterare da 1 a N — l'elenco è l'unica via per sapere che cosa esiste.
⚠️ Il PDF in `Caratteristiche_servizi/` è il **rendering dello stesso contratto**: verificato estraendone il
testo, non aggiunge nulla. **Da riportare** nella pagina «Dizionari ANSC» del disegno e nel capitolo dei
dizionari dell'analisi, dove oggi il tracciato è citato ma non riportato per intero.

**Prossimi passi (Open Point, 52 voci)** — ⚠️ **prima di aggiungerne uno, contare le righe della tabella
OP nel .docx**: la numerazione è arrivata a OP-52 e non coincide più con quanto scritto qui in passato.
**OP-01 CHIUSO** (firma USC richiesta, per atto, OTP, non
automatizzabile — l'errore v1.0 nasce dall'aver progettato senza chiuderlo). **OP-14** mappatura
campo-per-campo SIPO↔ANSC + obbligatorietà (propedeutica a Configurazione/pre-verifica; primo estratto
già in App. A). Nuovi: **OP-15** utenza tecnica + certificato server Roma + ambiguità x5c/postazione
(chiarire con Sogei); **OP-16** registro postazioni scala Roma; **OP-17** rate/fair-use; **OP-18**
accreditamento software house (`nomeApplicativo`/`versioneApplicativo`/`fornitoreApplicativo` in testata);
**OP-19** semantica dell'esito KO di R009 (consuma idAnsc/persiste RIFIUTATA?); **OP-20** riconciliazione
soggetto R005/R018 nel pilota; **OP-21** uso del `forcingCode`; **OP-22** ripartizione responsabilità/firma
tra ruoli del back-office (deleghe di firma — l'utente deve chiedere all'organizzazione). OP-02/03 chiusi;
OP-12 riformulato (esiti indeterminati). **OP-19 CHIUSO sul contratto** (campo obbligatorio mancante →
HTTP 400 codice 400001, l'evento NON è creato e nessun idAnsc è consumato; lo stato RIFIUTATA nasce solo
dal provvedimento di rifiuto R016). Aggiunti dalla v2.1 in poi: **OP-23** perimetro ammesso della modalità
M2M — se letture e code (R004/R005/R008/R021/**R901**) siano eseguibili senza l'OTP del singolo operatore
(la nota JWT elenca `otp` senza dichiararlo opzionale e l'Allegato 4 non è nel repository) → **è il
presupposto dell'automazione e anche del comando dizionari**; **OP-24** volumi reali degli atti di morte;
**OP-25** ridondanza di `ANSC_XREF` rispetto allo store di stato (fondere o tenere); **OP-26** quali
maschere SIPO debbano leggere i dizionari ANSC invece delle `CONF_*`; **OP-27** completezza dell'elenco
degli errori di validazione; **OP-28** identificativi di decodifica ripetuti (ANSC_134/135); **OP-31**
parto plurimo (un atto o più atti: i flag stanno sul soggetto); **OP-32** i 12 UC senza Modello;
**OP-33** le 12 incoerenze fra codice UC e condizione nella ricognizione nascite; **OP-34** combinazioni
di campi discriminanti senza UC (controllo di copertura); **OP-29**
(Alta) colonne ANSC già presenti in `ANAG_USR.ATTO` — vedi il blocco seguente; **OP-30** (Alta)
individuazione dell'atto collegato in ANSC (108 casi d'uso su 374 lo richiedono) — **si lega a OP-29**:
per agganciare un atto già formato bisogna ritrovarlo, e SIPO non espone ricerca per identificativo
nazionale. **OP-29 e OP-30 vanno chiusi insieme.** Dalla v3.2: **OP-36** (Alta) accesso di rete del pod
dizionari a github.com/italia/ansc — è il **prerequisito** dell'intercetto automatico delle revisioni
(vedi il blocco sul versionamento); **OP-37** (Media) ripartizione fra USC della responsabilità di
attivare una baseline della configurazione. Dalla v3.3: **OP-38** (Alta) **volumi delle notifiche in
ingresso** — la conferma è per singola notifica, il presidio è proporzionale al volume e il volume alla
scala di Roma non è noto; **OP-39** (Media) automazione delle comunicazioni ai 7 enti (serve l'interfaccia
verso protocollo/PEC); **OP-40** (Media) **termine entro cui confermare una notifica** (lo stato «Scaduto»
esiste, la scadenza non è pubblicata); **OP-41** (Media) flusso di conferma per gli **atti anomali**, che
ANSC dichiara **non ancora implementato**. Dalla v3.4: **OP-42** (Media) continuità operativa quando
l'indisponibilità è **nostra** (ANSC su, SIPO giù) — oggi il documento copre solo il caso opposto;
**OP-43** (Media) comportamento della **nota tecnica** (`[DA VERIFICARE]`: ricompilazione integrale o soli
campi da correggere — l'utente lo chiede a chi gli ha mostrato l'applicazione); **OP-44** (Alta)
**allocazione del numero comunale in concorrenza** — è a carico del Comune (`evento.numeroatto`), nessun
servizio ANSC lo assegna, alla scala di Roma più operatori lavorano insieme e per il parto plurimo i
numeri vanno allocati **in blocco e in anticipo**. Dalla v3.5: **OP-45** (Media)
ricognizione di **quale servizio di deposito serva a ciascun caso d'uso** (sono 7 su 6 servizi, il
concentratore ne conosce 1). Dalla v3.11: **OP-50** (Media) raccordo delle **6 descrizioni di
allegato** senza corrispondenza in ANSC_09 + contrassegno dell'attestazione di conformità; **OP-51**
(Media) **formule ministeriali per UC** (366 UC, 233 formule) non configurate e senza catalogo pubblicato.
Dalla v3.13: **OP-52** (Media) i **44 percorsi del mapping assenti dal modello evento** (232 occorrenze,
55 UC di matrimonio/unione/cittadinanza/trascrizione): se il campo esiste manca dal contratto, se non
esiste il mapping è da correggere — da chiarire prima di configurare quelle famiglie. Dalla v3.7: **OP-46** (Media) meccanica del completamento di una **bozza prenotata**
(parto plurimo): con quale campo la validazione la riconosca — sbagliare produce un **duplicato**, non
un errore. Da provare in preproduzione. Dalla v3.8: **OP-47** (Alta) numerazione comunale degli atti
lavorati in **modalità di emergenza** (lega OP-44); **OP-48** (Alta) **termine massimo di permanenza in
emergenza** — senza, l'archivio temporaneo diventa un secondo registro; **OP-49** (Media) **base normativa
del registro di emergenza**, la citazione «art. 10 del D.M.» non era verificabile ed è stata rimossa.

**⚠️ SIPO CONOSCE GIÀ L'ID ATTO ANSC (verificato sul codice 21/08/2026 → OP-29). NON assumere che verso ANSC
non ci sia nulla.** `common/anagrafe-entities/.../entities/Atto.java` mappa su `ANAG_USR.ATTO` le colonne
**`ID_ATTO_ANSC`** (riga 161), **`ANNO_ANSC`** (164) e **`DATA_ANSC`** (180). Formato dell'identificativo
(da `common/anagrafe-entities/.../bl/AttoAnscBL.java` e `front-end/statocivile-web/.../utility/UtilityANSC.java`):
**`ANNO(4)-ProgrNazionale-ProgrComunale-CodIstatComune(6)`**, con anno **≥ 2023**.
`AttoAnscBL.creaAttoAnsc()` fa lo `split("-")` e distribuisce le quattro parti su `ANNO_ANSC`,
`NUMERO_NAZIONALE`, `NUMERO_COMUNALE` e `COMUNE`. **Due binari mutuamente esclusivi**:
`eliminaAttoStandard()` azzera NUMERO_ATTO/ANNO/PARTE/SERIE/TRASCRITTO/DATA_FORMAZIONE/COMUNE_ISCRIZIONE/
COMUNE_TRASCRIZIONE ↔ `eliminaAttoAnsc()` azzera le colonne ANSC.
**⚠️ Asimmetria fra i due ATTO**: l'`ATTO` di **stato civile** (`MATR_USR`, entity `AttoMatr`) **NON** porta
l'id ANSC del *proprio* atto — ha solo `ATTO_TRASCR_NUMERO_ANSC`/`_ANNO`/`_NUMEROATTO`/`_PARTE`/`_SERIE`,
cioè i riferimenti dell'atto **trascritto** perché formato altrove. L'id ANSC proprio sta sull'`ATTO` di
**anagrafe**: due schemi, due percorsi di scrittura. Da qui OP-29 (è lo stesso dato di
`ANSC_USR.ANSC_STATO_ATTO.ID_ANSC`? chi lo scrive quando l'atto lo forma il nuovo componente?).

**API DI RICERCA IN SIPO (verificato 21/08/2026 — NON riaprire)**: **per idANSC NON esistono.** Zero
`@Query`/`findBy` che filtrino su `ID_ATTO_ANSC`, `NUMERO_COMUNALE`, `NUMERO_NAZIONALE`, `ANNO_ANSC`,
`ATTO_TRASCR_NUMERO_ANSC` (cercato su tutto `back-end/` e `common/`). L'unico endpoint che tocca l'id è
**`POST /variazioniAnagrafiche/controlloIdAttoAnsc`** (`varana-be/.../SoggettoController.java:7003`) →
`AttoAnscBL.validaIdAttoAnsc()`: **valida il formato** (ritorna 0 oppure -1…-6), **non cerca**.
Per numero atto esiste **una sola** ricerca, strettissima: **`POST /findAttoByNumeroAtto`**
(`statocivile-be/.../UtilityController.java:6155`) → `AttoMatrRepository.getAttoByNumeroAndAnnoAndArea`,
query `NUMERO_ATTO + ANNO + AREA` **`and ID_STATO_PRATICA = 2 and c.TIPO_RITO = 'ART.12'`** → solo matrimoni
già definiti, e restituisce il solo `ID_ATTO`, non l'atto. **Nessuna ricerca di atti per PARTE/SERIE** (le
uniche query con parte/serie stanno su `V_ELENCO_PREPARATORIO_LEVA`, dominio diverso). Il dettaglio si
ottiene per chiave tecnica interna (`/getDettaglioAtto` con `idAtto`). **Conseguenza per il disegno**: se
serve ritrovare un atto dall'identificativo nazionale o dal numero comunale, l'API va costruita — non esiste.

**IL DOMINIO COMPLETO DEGLI ATTI (v2.9, cap. Roadmap — dati verificati su `ansc/docs/Mapping_casi_uso/`).**
Il pilota è la morte, ma l'obiettivo è coprire tutte le tipologie. **374 casi d'uso** in **7 famiglie**,
**48 blocchi distinti** del modello evento, **20.346 campi obbligatori** dichiarati:

| famiglia | casi d'uso | blocchi | intest. max | con evento collegato | campi obbl. |
|---|---:|---:|---:|---:|---:|
| morte (pilota) | 25 | 13 | 1 | 5/25 | 573 |
| nascita | 143 | 25 | 1 | 3/143 | 7.448 |
| riconoscimenti | 23 | 13 | 1 | 0/23 | 1.297 |
| matrimoni | 40 | 16 | 2 | 6/40 | 4.376 |
| unioni civili | 24 | 13 | 2 | 4/24 | 1.255 |
| cittadinanza | 64 | 20 | 1 | **62/64** | 2.456 |
| trascrizioni | 55 | 29 | 2 | **28/55** | 2.941 |

**Regge per tutte le famiglie** (verificato): contratto e servizi unici, percorso presidiato e sessione OTP,
store di stato e ciclo di vita, **tracciato del mapping identico** (stesse 7 colonne, radice unica `evento.`)
→ `ANSC_CFG_CAMPO` e `importaCampi` valgono tal quali, pre-filtro e dizionari già dimensionati sull'intero
dominio, 45 operazioni API nessuna delle quali specifica della morte.
**Quattro elementi nuovi per famiglia**: (1) adattatore di mappatura — 48 blocchi, il pilota ne esercita 13;
(2) **secondo intestatario** — **63** casi d'uso su 374 (33/40 matrimoni, 16/24 unioni, 14/55 trascrizioni)
⚠️ NON 119: le famiglie che *possono* averne due non lo usano in tutti i casi; (3) **soggetto costituito
dall'atto** (nascita: l'intestatario non ha identificativo preesistente nel mapping → la consultazione R005
riguarda i **genitori**, non il neonato); (4) **aggancio all'atto già formato** — 108/374 → OP-30.
Prossimità al pilota: riconoscimenti e nascita → matrimoni e unioni (2° intestatario) → cittadinanza e
trascrizioni (atto collegato).

Lavori precedenti (reverse-engineering, conclusi salvo aggiornamenti): **DAD Area Stato Civile** da
`template_DAD_roma-capitale.docx` sulla sorgente `B9DA959E80-05-008-05-002_v1.00.docx` (Disegno Base
Dati — 24 schemi, ~322 tabelle). La sorgente copre in modo forte solo la Sez.7 "Modello di dati"; il
resto è gap.

Le sorgenti non sono più solo documentali: la cartella include ora il **codice SIPO**
(`front-end/`, `back-end/`, `common/`, `sipo-root/`, `cross/`; **139 `pom.xml` in tutto il workspace** →
se lo apri in VS Code, disabilita l'estensione Oracle Java: fa un «priming build» per progetto), il
**repository ANSC** (`ansc/` — **145 tabelle** di decodifica in `ansc/docs/Decodifiche/`: i 291 file sono
145 csv + 145 xlsx + 1 md, **non 291 tabelle**; OpenAPI R001–R024 + R901 in `ansc/docs/openapi/`,
mapping ufficiale dei casi d'uso in `ansc/docs/Mapping_casi_uso/`)
la **ricognizione delle nascite** `Sorgenti Documentali/Nascite_ANSC_07.08.2026.xlsx` (4 fogli =
4 cluster; per foglio: blocco UC↔Modello alle righe 3..N con la condizione discriminante in col. J,
poi la mappatura dei campi dalla riga con «SIPO» in col. A; le colonne H/I/K/L/M **sono colonne reali
di `CONF_TIPO_ATTI`**)
e la **documentazione ANPR** (`anpr-9.2.9/` — 41 tabelle di decodifica in `src/tab/tab_*.rst` con
titolo «Tabella NN – Nome», WSDL/XSD ufficiali in `src/wsdl/comuni/`, archivio comuni in
`src/archivi/`).

Prodotti in `Documenti finali/` (**versione corrente in grassetto**):
- **`DAD_Area-Stato-Civile_v0.3.docx`** — scheletro completo, Sez.7 popolata (7.1 schemi, 7.2
  dizionario `CONF_*`/`CFG_*`, 7.3 91 entità di dominio — escluse temp `GTT_*`/`TMP_*`,
  bonifica `BON_*`, log, deprecate). v0.3 aggiunge in coda a 7.2 il segnaposto sulla codifica
  degli stati esteri (DV-32). Versioni precedenti: v0.1, v0.2.
- **`DAD_Area-Stato-Civile_TRACCIAMENTO-DA-VERIFICARE_v0.7.xlsx`** — checklist dei segnaposto
  (sezione, cosa manca, sorgente attesa, priorità, stato): **36 voci**, 33 «Da fornire» +
  3 «Parziale (v0.2)»; 26 Alta / 9 Media / 1 Bassa. Il foglio `Legenda` riporta i conteggi e va
  tenuto allineato al foglio `DA VERIFICARE` (**ricalcolarli dalle righe, non a mano**).
  Versioni precedenti: v0.1 (30 voci), v0.2 (31), v0.3 (32 — DV-32), v0.4 (34 — DV-33/34),
  v0.5 (35 — DV-35), v0.6 (DV-35 → Alta).
- **`STUDIO_Client-ANPR_v0.4.docx`** — quadro esaustivo del client ANPR (funzioni, payload,
  utilizzo reale, anomalie A1–A6). v0.2 aggiunge il capitolo sul proxy REST; v0.3 quello sui
  **canali di ingresso** dei dati ANPR; v0.4 gli **esempi di invocazione** tratti dal codice.
  Precedenti: v0.1, v0.2, v0.3.
- `STUDIO_Decodifiche-ANSC_v0.3.docx` e `GAP_Decessi_SIPO-ANSC_v0.1.docx`/`.xlsx` — filoni
  paralleli (decodifiche ANSC; gap Decessi SIPO→ANSC).
- **`MAPPA_Decessi_Schermate-Servizi-Tabelle_v0.2.docx`** — reverse-engineering dell'area Decessi:
  schermata → servizio FE → endpoint BE → tabelle, con **vista invertita** tabella → schermate/servizi
  (v0.2). Ogni riga ha riferimenti `file:riga`. Precedente: v0.1 (senza vista invertita).
- **`ANALISI_Integrazione-ANSC_v3.13.docx`** — analisi tecnico-funzionale del **nuovo** componente per
  la scrittura SIPO→ANSC (progettuale, non reverse-engineering). **È la base di lavoro corrente**:
  si modifica **il file reale** via python-docx, NON rigenerandolo da script (si perderebbero le edit
  manuali dell'utente). Impianto, struttura e numeri sono descritti sopra, in «Stato attuale del lavoro».
  ⚠️ **Le versioni v0.1→v1.0 descrivono un impianto SBAGLIATO** — verifica sincrona + **scrittura
  asincrona** via outbox transazionale + worker, backoff, DLQ, sweep di riconciliazione, macchina a stati
  NEW→IN_PROGRESS→SENT→ACK, cruscotto KPI/dead-letter: **superate dalla v2.0, non riusarle come
  riferimento**, nemmeno per i wireframe del back-office (Cruscotto/Invii/Dead-letter non esistono più).
  Storico: v0.1→v0.4 (rigenerate da script), v1.0 (prima base editata a mano), **v2.0 = correzione
  d'impianto**, v2.1/v2.2 (rilettura critica + nuovo cap. dizionari), v2.3 (nomenclatura oggetti DB [R5]),
  v2.4 (nomenclatura API [R6]), v2.5, v2.6 (separazione operativo/dizionari, PC-8, OP-28),
  v2.7 (App. B = inventario delle 45 operazioni generato dai contratti OpenAPI; riferimenti R7/R8/R9;
  OP-29 sulle colonne ANSC preesistenti in `ANAG_USR.ATTO`), v2.8 (riconciliati elenco dei componenti e topologia; aggiunto il processo di automazione),
  v2.9 (paragrafo «Estensione a tutte le tipologie di atto» con i dati del dominio; OP-30),
  **v3.0 (corrente: nomenclatura UC/Modello; nuovo cap. 10 «Le regole di determinazione e di
  controllo»; RF-11; PC-9; `ANSC_REGOLA`+`ANSC_CFG_REGOLA_CONDIZIONE`; schermata «Regole» nel
  back-office; **`ANSC_UC`** con `ANSC_CFG_CAMPO` agganciata all'UC; back-office a
  13 schermate e 8 categorie di eccezione; OP-31…34),
  v3.1 (allineamento allo standard DB [R5] v1.01 — marcatori di tipo
  `ANSC_CFG_REGOLA`/`ANSC_CFG_REGOLA_CONDIZIONE`/`ANSC_ANA_UC`, chiavi surrogate uniformi,
  prefissi di ruolo, campi tecnici; OP-35),
  v3.2 (nuovo cap. 12 «Il versionamento della configurazione»; RF-12;
  `ANSC_CFG_VERSIONE` + colonne `ID_VERSIONE`; vincolo di rete verso il repository ANSC;
  9 categorie di eccezione e 14 schermate; R10 nei Riferimenti; OP-36/37),
  v3.3 (nuovo cap. 14 «Il flusso in ingresso: notifiche, comunicazioni e
  solleciti»; RF-13; PC-10; `ANSC_NOTIFICA`; schermata «Notifiche»; R11; OP-38…41),
  v3.4 (nuovo cap. 15 «Le due superfici: SIPO e la web app ANSC»; RF-14;
  dominio degli stati esteso da 6 a 12; sessione OTP per azione con timer e soglia di
  guardia; OP-42/43/44),
  v3.5 (nuovo cap. 16 «Le funzioni offerte da ANSC» — inventario delle 57
  operazioni GENERATO dai contratti, 9 famiglie, caratteristiche trasversali,
  approfondimento su R009; OP-45),
  v3.6 (nuovo cap. 17 «Schede dei servizi ANSC per lo sviluppo» — una sezione
  di 2° livello per ciascuno dei 23 servizi, esclusi i due DMNM: spiegazione, operazioni,
  prerequisiti, modalità di adozione, trappole, riferimenti),
  v3.7 (prenotazione degli identificativi per il parto plurimo — §R009 del cap. 16,
  scheda R009 del cap. 17, riga BOZZA fra le azioni per stato; OP-31 parzialmente risolto,
  OP-46),
  v3.8 (riscritto il trattamento dell'indisponibilità — modalità di emergenza vs
  registro di emergenza, meccanismo di rientro ANSC_96, RF-15, 4 colonne nello store,
  decima categoria di eccezione; OP-47/48/49),
  v3.9 (rilettura di coerenza — rimandi al capitolo rinominato, difetto degli
  stati portato al passato, nomenclatura Casistica/Evento ANSC, grafia «back-office»,
  tabelle delle colonne completate, convenzione UC/caso d'uso nel Glossario),
  v3.10 (due schemi ERD nel cap. Modello dati — schema ANSC_USR e legami con
  SIPO; motivati i 3 riferimenti per valore; aggiunte le 2 FK mancanti su `ID_VERSIONE`),
  v3.11 (allegati richiesti dall'UC — `ANSC_CFG_ALLEGATO`, importati dal mapping;
  schermata «Campi e allegati per UC»; OP-50/51),
  v3.12 (rigenerato l'ERD di §8.1, che era fermo alla v3.10 e non conteneva `ANSC_CFG_ALLEGATO`),
  **v3.13 (corrente: revisione della parte di configurazione — il cap. 9 si apre con la definizione
  del **modello evento** e si chiude con le fonti, la catena completa Modello→payload e la procedura
  di revisione della mappatura; corrette in §8.4 le formulazioni «per operazione»; OP-52)**.
- **`MAPPATURA_Campi_ANSC-SIPO_v0.2.xlsx`** — l'inventario di **tutto** il dominio: 63.531 righe di
  mappatura, 374 UC, 4.620 percorsi del modello evento, più i fogli Allegati (1.569), Formule (2.200),
  Non risolti (i 44 di OP-52) e **Dizionario SIPO** (3.804 campi di maschera → colonna, di cui 3.724 non
  ancora collegati a un campo ANSC). ⚠️ **La v0.1 è superata**: era anteriore ai suoi stessi generatori e
  il lato SIPO si fermava all'**etichetta** di maschera. Dalla v0.2 il lato SIPO lo risolve il **ponte**
  (`ponte_ansc_sipo.arricchisci`), non più il raccordo per etichetta di `mappatura_sipo`.
- **`MAPPATURA_Nascite-Morte_SIPO-ANSC_v0.1.xlsx`** — lo scavo sulle due famiglie con codice disponibile:
  26.126 righe UC×campo, fino alla **colonna Oracle** con evidenza `file:riga`. Generatore
  `strumenti/workbook_nascite_morte.py`. È il contenuto di **OP-14**.
  ⚠️ **I due workbook sono complementari, non alternativi**: il primo è l'inventario del dominio (7
  famiglie), il secondo lo scavo sul pilota (2 famiglie, con allegati e formule esclusi). Condividono il
  motore, quindi i conti tornano fra loro: 10.442 righe risolte, 9.569 con colonna, 12.263 assenti in
  SIPO, 3.421 con l'intero soggetto assente.
  ⚠️ **Due terzi dei raccordi sono per «sinonimo»** (6.998 contro 3.444 «struttura»): il nome dichiarato
  differisce fra i due mondi. È il punto da controllare a campione prima di fidarsi della colonna.
- **`documenti elaborati intermedi/`** — cartella di lavoro sulla **configurazione**, distinta dai
  documenti consegnabili. Contiene il foglio compilato **a mano** `Dic_Nasc_001.xlsx` (12 colonne, 181
  righe; il foglio si chiama con l'**ID usecase** `11111000`), che è l'unica fonte del lavoro umano —
  colonna `Tabella/Campo SIPO`, regole di transcodifica, note — e `AREA_TIPO_ATTO_MODELLO.xlsx`.
  Prodotti generati: `Dic_Nasc_001_v0.2.xlsx` (`strumenti/completa_uc.py`: aggiunge le 26 righe delle
  sezioni assenti — Luogo Redazione 13, Formula 8, Allegati 5 — l'esito dell'obbligatorietà e le
  proposte automatiche in colonna separata) e **`MAPPATURA_UC_Nascite-Morti_v0.1.xlsx`**
  (`strumenti/uc_workbook.py`: un foglio per ciascuno dei 168 UC delle due famiglie + Legenda, Indice
  navigabile, «Da compilare», «Percorsi (tutti)», «Soggetti assenti») e **`Morte_001.xlsx`**
  (`strumenti/prepara_foglio_uc.py`: il foglio di lavoro del pilota nella forma di Dic_Nasc_001,
  già popolato con proposte, evidenze e istruzioni — 218 righe, di cui **80 «soggetto assente»**,
  cioè i comparenti, il coniuge, l'unito civilmente e il soggetto intervenuto, che la maschera dei
  decessi non raccoglie affatto).
  ⚠️ **IL LAVORO SI FA PER PERCORSO, NON PER UC.** I percorsi ANSC distinti delle due famiglie sono
  **869**. Stato (05/09/2026): **66 compilati a mano** su Dic_Nasc_001, che coprono **8.443
  occorrenze UC×campo** · 45 proposti dal ponte · 28 suggeriti dall'altra famiglia · **289 da
  compilare** · 441 «soggetto assente in SIPO» (blocchi che SIPO non ha).
  ⚠️ **Due regole di igiene scoperte innestando il foglio a mano, valgono per ogni propagazione**:
  (a) **una colonna SIPO è `TABELLA.COLONNA`**: nel foglio a mano quella cella ospita anche
  annotazioni (`flagDichiarante='false'`), che sono regole di calcolo, non sorgenti — propagarle
  come colonne crea dati falsi (erano **12 percorsi** su 78, per questo il conto è sceso a 66);
  (b) **il lavoro umano batte la proposta automatica**, anche quando viene da un'altra famiglia:
  su `evento.numeroatto` il compilatore ha scelto `ATTO.NUM_COMUNALE_ANSC` dove il codice propone
  `ATTO.NUMERO_ATTO`. Primitive `ben_formata()`/`normalizza()` in `strumenti/uc_famiglia.py`.
  ⚠️ Per la **morte non esiste alcun foglio compilato**: propagare da nascita a morte è ammesso solo se
  la tabella non è specifica (`SOGGETTO`, `ATTO` sì; `ATTO_NASCITA…` no).
- ⚠️ **`documenti elaborati intermedi/AREA_TIPO_ATTO_MODELLO.xlsx` — LA RICOGNIZIONE DEI TIPI ATTO DEL
  COMUNE, con la frequenza d'uso.** 435 righe, 11 colonne: `AREA` · `ID_CONF_TIPO_ATTO` ·
  `ID_MODELLO_ATTO` · descrizioni · `DICHIARANTE` · `Conteggio` · **`Frequenza`** · **`Usecase ANSC`**.
  Ripartizione: NASCITE 338 · CITTADINANZE 36 · MATRIMONI 29 · UNIONI 20 · DECESSI 12.
  ⚠️ **Solo 6 righe su 435 hanno l'UC ANSC dichiarato**, tutte decessi — la mappatura Modello→UC è
  appena iniziata. Frequenza: 24 Elevatissima · 4 Elevata · 24 Media · 109 Bassa · 274 vuota: è il
  criterio per «configurare prima gli UC più frequenti». ⚠️ **Due righe portano DUE UC**
  (`2212, 2213` e `2199, 2299`): è il caso in cui serve la condizione di applicabilità.
  Valori del pilota, da usare al posto del vecchio segnaposto `DICH_ABITAZIONE` (che non entrava nella
  colonna `VARCHAR2(5)`): **MORTE IN ABITAZIONE A ROMA = tipo atto 301, Modello `01`, UC `2101`**
  (Morte_001); MORTE IN OSPEDALE A ROMA = 303 / `03` / `2102`.
- ⚠️ **v3.19 (11/09/2026) — LE STRUTTURE EREDITATE DAL SISTEMA SIDE DI MILANO.** Fonti:
  `Sorgenti Documentali/DDL tabella allegato.txt` e `DDL tabelle domini ANSC.txt` (PostgreSQL).
  Decisioni dell'utente: **nomi as is** · **BLOB** con raccomandazione motivata per S3 · allegato
  legato alla **chiave dell'atto SIPO** · dizionari **sostituiti** · tutto in **ANSC_USR**.
  ⚠️ **`ALLEGATO` NON si sovrappone ad `ANSC_CFG_ALLEGATO`**: la prima è **operativa** (i documenti
  di un atto), la seconda è **configurazione** (quali documenti servono per un UC). Al modello
  mancava la prima. Porta due colonne che chiudono punti aperti: **`id_ansc_allegato`** (rende
  realizzabile **RF-17**) e **`fg_incluso_att_conformita`** (chiude parte di **OP-50**).
  ⚠️ Convenzione Side, diversa da [R5] e ora **compresente** nello schema: `ty_` tipo · `ds_`
  descrizione · `nm_` nome · `oj_` oggetto · `cd_` codice · `fg_` flag · `ts_` timestamp · `dt_` data ·
  `nr_` numero. ⚠️ Tipi da tradurre: `bigserial`→IDENTITY · `int8/int4`→NUMBER · `bytea`→BLOB ·
  `bpchar`→CHAR · `text`→CLOB. ⚠️ Unico scostamento: `id_evento`→**`id_atto_sipo`** (in Side punta a
  `atti.evento`, tabella che SIPO non ha).
  ⚠️ **DIFETTO DICHIARATO DEI DIZIONARI DI SIDE**: `dominio_decodifica` ha PK sul **solo
  `id_dominio`**, ma il corpus ANSC ha **145 file su 143 identificativi** — **ANSC_134**
  (`dec_dichiarante_trascr_nascita` + `_postuma`) e **ANSC_135** (due file che differiscono per un
  refuso) → **il carico completo viola la PK**. Correzione minima proposta: aggiungere `nm_dominio`
  alla chiave. ⚠️ Si perde anche lo **storico dei caricamenti** (`ANSC_DIZ_CARICAMENTO`): rinuncia
  dichiarata, non svista. ⚠️ **La vista `V_ANSC_DIZ_VALIDO` resta**: non viene da Side, è il contratto
  verso SIPO e vale quali che siano le tabelle sottostanti.
- ⚠️ **v3.17/v3.18 (11/09/2026) — RILETTURA DI COERENZA, e la lezione sui commenti.**
  La v3.17 (dell'utente e di una collega) riorganizzava i capitoli **senza rimuovere i vecchi**:
  «Costruzione del payload» (7) ≡ «Mappatura del payload» (11) per **45 paragrafi su 50**, e due
  capitoli con **lo stesso titolo** «Gestione dei dizionari ANSC» (8 e 12) per 29 su 31. Il cap. 9
  «Impatti FE» era uno stub che ripeteva il cap. 11. La v3.18 li elimina.
  ⚠️ **QUATTRO ANCORE DI COMMENTO ERANO AGGANCIATE AI CAPITOLI DA ELIMINARE.** Un commento vive in
  `word/comments.xml` ma **senza ancora nel testo Word non lo mostra più e sparisce**. Poiché i
  paragrafi commentati esistevano identici nei capitoli nuovi, le ancore si spostano lì:
  **`sposta_commenti()`** in `strumenti/docx_comune.py` (sposta `commentRangeStart`/`End` e il run con
  `commentReference`). ⚠️ `elimina()` in `v3_18_duplicati.py` **si interrompe** se un elemento da
  cancellare porta ancora un commento: è il controllo che impedisce la perdita silenziosa.
  **Refusi trovati**: «deco**dica**» (titolo di sezione) · «**ANAS**_CFG_CAMPO» · «**ANAS_CGF**_UC» ·
  «**consuntabili**» (RF-17) · spazio prima della virgola · riga vuota in coda ai requisiti.
  ⚠️ **I RIMANDI PER NUMERO DI CAPITOLO SI ROMPONO A OGNI RINUMERAZIONE**: eliminando due capitoli,
  sei rimandi puntavano a contenuti diversi pur restando «validi» (il numero esisteva). Convertiti in
  **rimandi per titolo**. Il controllo di `verifica-conteggi` non li intercetta: verificare a mano che
  il numero citato contenga davvero quell'argomento.
  **Due requisiti nuovi in v3.17**: **RF-16** (identificativo ANSC/ANPR) — ⚠️ riformulato, perché la
  stesura originale affermava che il modello lo preveda solo per gli intestatari mentre lo chiede in
  **92 punti dell'albero** (madre, padre, dichiarante, interprete, coniuge, ufficiale) **senza
  obbligarlo in nessuno**: è un impegno del Comune, non una proprietà del modello; **RF-17** (allegati
  consultabili da SIPO accedendo ad ANSC) — ⚠️ manca nel modello dati il posto dove registrare
  l'identificativo dell'allegato, senza il quale SIPO non sa che cosa rileggere.
  ⚠️ Attenzione: «**blocchi**» nel documento significa le **48 radici `evento.<blocco>`** — altro dal
  numero dei percorsi. Il verificatore ha intercettato proprio questa confusione in una frase scritta
  da me.
- ⚠️ **v3.15/v3.16 (08/09/2026) — SEMPLIFICAZIONE VOLUTA DAL CLIENTE. Il documento ha 20 capitoli
  (erano 24) e la configurazione **cinque tabelle** invece di nove.** La v3.15 è dell'utente, la v3.16
  è l'allineamento.
  ⚠️ **I 21 COMMENTI DI WORD VANNO PRESERVATI** («nelle successive versioni vorrei che rimanessero»),
  autori Claudia Lombardi e Bernardo Puccetti. **Il round-trip di python-docx li conserva**, ma
  `testo_di()` nella forma ingenua **li distrugge**: scrivere nel primo run e cancellare gli altri
  cancella anche i run che portano `commentReference`. In `strumenti/docx_comune.py` ci sono ora
  `ha_commenti()`, `testo_di()` protetta, `riscrivi_cella()` e **`riscrivi_sicura()`**, che non
  elimina mai una riga commentata. **Usare sempre queste**, non `riscrivi_tabella`.
  **Modello semplificato**: `ANSC_ANA_UC` (catalogo) · **`ANSC_CFG_UC`** con **`REGOLA_DI_SCELTA`
  VARCHAR2(2000)** — la condizione è *fusa* nella riga, `ANSC_CFG_UC_CONDIZIONE` non esiste più ·
  **`ANSC_CFG_CAMPO` a 19 colonne** (`SEZIONE_FE_ANSC`, `OGGETTO_ANSC`+`CAMPO_ANSC`,
  `TABELLA_SIPO`+`CAMPO_SIPO`, `DESC_COND_OBBLIGATORIETA`+`REGOLA_COND_OBBLIGATORIETA`,
  `DESCRIZIONE_BUSINESS_LOGIC`+`BUSINESS_LOGIC`, `ORDINAMENTO`, `VALORE_DEFAULT`, `NOTE`) ·
  `ANSC_CFG_ALLEGATO` · `ANSC_CFG_FORMULA` (⚠️ **da eliminare dopo confronto col cliente**, commento
  [26]: SIPO è già conforme all'uso delle regole per costruire i testi) · `ANSC_CFG_VERSIONE`.
  **Spariti** `ANSC_CFG_REGOLA` e `_CONDIZIONE`. ⚠️ Le tre colonne di regola contengono **codice
  eseguibile in forma di script**: il linguaggio (PL/SQL, SpEL, JavaScript) è **volutamente non
  deciso** — la scelta è del cliente.
  ⚠️ **`COD_UC_ANSC` NON è sempre a 8 cifre**: 11111000 per la nascita, **2101 per la morte**; nel
  catalogo ci sono codici di 4, 5, 6 e 8 cifre. La **notazione puntata `2.1.0.1` è solo redazionale**
  (la usano il RTI e `Integrazione_SIPO_ANSC.xlsx`) e **non va nel database**.
- ⚠️ **IL PAYLOAD INVIATO SI CONSERVA SULL'ATTO — `ANSC_STATO_ATTO.TXT_PAYLOAD`** (v3.16, proposta
  dell'utente per debug e audit). Il payload **c'era già** in `ANSC_LOG_AUDIT` (RICHIESTA/RISPOSTA,
  CLOB IS JSON) ma **per ogni chiamata**: trovare «che cosa abbiamo mandato per questo atto» richiedeva
  di filtrare l'audit per fase di deposito. ⚠️ **La ragione che lo rende necessario e non comodo: il
  payload NON è sempre ricostruibile.** Si potrebbe rigenerare da atto SIPO + configurazione, ma solo
  finché la configurazione non cambia — e il mapping ANSC è rivisto ~20 volte l'anno. Dopo
  l'attivazione di una nuova baseline la rigenerazione darebbe un payload diverso da quello
  depositato, mentre l'atto è già formato. Letto insieme a `ID_VERSIONE` (già sulla stessa riga) dice
  **che cosa** è stato inviato e **con quale configurazione**. Seconda ragione: l'audit conserva dati
  particolari e il documento ne prevede la minimizzazione — la copia sull'atto sopravvive alla purga.
  **Volume dichiarato**: **144.285 atti/anno** dalla ricognizione dei tipi atto (52.142 decessi ·
  42.239 nascite · 26.226 cittadinanze · 23.111 matrimoni · 567 unioni) → **1-4 GB/anno** secondo la
  dimensione media. Si conserva il payload **del deposito**, non di ogni tentativo.
- ⚠️ **NUOVE SORGENTI (08/09/2026) e il documento del RTI.**
  `Sorgenti Documentali/Integrazione_SIPO_ANSC.xlsx` = **il modello della configurazione in Excel**,
  4 fogli: `Conf_UC` · `Dett_UC` · `All_UC` · **`Riconc_decod`** (TRANSCODIFICA, ID_SIPO,
  DESCRIZIONE_SIPO, ID_ANSC, DESCRIZIONE_ANSC, CONDIZIONE) — ⚠️ **la corrispondenza dei VALORI fra
  SIPO e ANSC non ha una tabella nel nostro modello**: `ID_DECODIFICA_ANSC` dice quale dizionario,
  non come tradurre. Buco segnalato, non ancora colmato.
  ⚠️ **`UseCase_Morte (2).xlsx` CONTIENE DATI DI NASCITA**: solo il foglio `2101` è morte; `2102` e
  `2103` contengono gli UseCase `11111100` e `11111200`. E in entrambi i file il foglio `11111100`
  ha **3 righe di `11111200`**.
  **`AT_Dizionari_ANSC-SIPO_Modulo_Decessi_v.3.docx`** = analisi del RTI sul solo modulo decessi
  (7 UC, mapping per sezione, matrice Repository-Entità-Tabella-Schema, impatti FE con priorità).
  ⚠️ **Strategia OPPOSTA alla nostra sul punto centrale**: loro **modificano le tabelle di SIPO**
  (aggiungere `ATTO.NUM_COMUNALE_ANSC`, `ATTO.ATTO_NUMERO_ANSC`, `ATTO_DECESSO_AGENZIA.INCARICATO_SESSO`),
  noi schema dedicato additivo (RNF-7). **Il nostro documento è quello trainante** (deciso dall'utente).
  ⚠️ **`ATTO.NUM_COMUNALE_ANSC` NON ESISTE**: il foglio di lavoro e l'esempio la usano come sorgente
  di `evento.numeroatto`, ma su `ANAG_USR.ATTO` c'è `NUMERO_COMUNALE` (`Atto.java:175`) e non quella.
  È una colonna da creare, e va deciso su quale delle due tabelle `ATTO` (MATR_USR o ANAG_USR).
- ⚠️ **VERIFICA DI CONGRUENZA CAPP. 8-9-10 (06/09/2026) — che cosa ha trovato, da rifare a ogni
  revisione d'impianto.** Quattro controlli, tutti con esito:
  (a) **figura ↔ testo**: la figura di §9.7 (`catena_configurazione.png`) era ferma alla v3.13 —
  `ANSC_CFG_OPERAZIONE`/`ANSC_CFG_REGOLA`, «il lavoro umano non è riempire queste tabelle: tutto il
  resto si importa» (l'opposto della v3.14), niente `ANSC_CFG_FORMULA`, e **«8.293 percorsi» contro
  gli 8.256 del testo**. Rigenerata; ⚠️ «374 validi su 377» invece **è corretto**
  (`Decodifiche/3_dec_use_case.csv` ha 377 righe, 3 con validità chiusa).
  (b) **DDL ↔ tabelle descrittive**: 16 tabelle nel DDL, tutte citate nei capp. 8-10; ma **quattro
  esistevano SOLO come DDL** — `ANSC_CFG_REGOLA`, `ANSC_CFG_REGOLA_CONDIZIONE`, `ANSC_ANA_UC`,
  `ANSC_CFG_VERSIONE`. Le prime due erano un buco **aperto dalla v3.14 stessa** (sostituendo «La forma
  della regola» con «La forma della condizione»). Descritte le prime tre; `ANSC_CFG_VERSIONE` resta
  (sta nel cap. 12). Aggiunta `CHIAVE_ANTI_DUPLICATO`, che era nel DDL ma non nella tabella.
  (c) ⚠️ **il DDL contraddiceva PC-9 in modo ESEGUIBILE**: `CHECK (COD_TIPO_REGOLA IN
  ('DETERMINAZIONE','CONTROLLO','GENERAZIONE'))` con un vincolo che pretendeva `COD_UC_ANSC` per la
  determinazione. Corretto a `('CONTROLLO','GENERAZIONE')`. **È la specie peggiore di contraddizione:
  il database l'avrebbe imposta.**
  (d) **rimandi**: 8 per numero di capitolo e 7 per titolo, tutti risolti.
- ⚠️ **v3.14 (06/09/2026) — LA CONFIGURAZIONE È UN DATO DEL COMUNE, NON UN'IMPORTAZIONE.**
  Deciso dall'utente, capovolge il principio delle versioni precedenti («i campi si importano»,
  `importaCampi` come meccanismo principale di popolamento): **la scrivono i funzionari dal
  back-office, una tantum con revisioni rare**; l'importazione dal mapping prepara le righe in stato
  **PROPOSTO** e l'operatore conferma/modifica/inserisce. Da qui **`COD_ORIGINE`** su `ANSC_CFG_CAMPO`
  e `ANSC_CFG_ALLEGATO` (PROPOSTO/CONFERMATO/MODIFICATO/INSERITO): ⚠️ **la reimportazione riscrive le
  sole righe PROPOSTO**, per le altre produce un elenco di scostamenti.
  ⚠️ **`ANSC_CFG_OPERAZIONE` → `ANSC_CFG_UC`**: da una riga per Modello a **una riga per UC adottato**
  (chiave `ID_UC_CFG`, UK `COD_UC_ANSC + ID_VERSIONE`, nuove `NUM_PRIORITA` e `FLG_ATTIVO`). Il Modello
  diventa un attributo. Sparisce il doppio luogo in cui l'UC poteva essere dichiarato.
  ⚠️ **PC-9 RIVISTA — la determinazione dell'UC è una QUERY SQL sui dati di SIPO** (`ANSC_CFG_UC_CONDIZIONE`:
  `TXT_QUERY` CLOB + `DESCRIZIONE` obbligatoria + `COD_ORIGINE`), non più una terna campo/operatore/valore.
  Motivo dell'utente: **SIPO salva l'atto sul proprio DB prima di depositarlo in ANSC**, quindi il dato su
  cui decidere è già scritto; e SIPO non governa la scelta degli allegati mentre ANSC la fa dipendere
  dall'UC. ⚠️ **Prezzo dichiarato: copertura e mutua esclusione NON sono più dimostrabili** → al loro posto
  `NUM_PRIORITA` (il primo UC che risponde vince) e la **simulazione su atti reali**, che diventa il
  controllo principale. Il regime che risponde alla critica alle `CFG_RULE` di SIPO: sola lettura,
  descrizione obbligatoria, versionata nella baseline, in `ANSC_USR` e non in `MATR_USR`.
  ⚠️ **Restano dichiarative le regole di CONTROLLO e GENERAZIONE**: la revisione tocca la sola
  determinazione. Il cap. 10 si chiama ora **«La determinazione dell'UC e le regole di controllo»**.
  ⚠️ **Gli allegati sono una FUNZIONE MANCANTE, non configurazione**: verificato che l'area di stato civile
  di SIPO non gestisce alcun documento allegato (solo `AllegatoCri`/ANPR e il client SOAP
  `common/protocollo-ged` per la protocollazione) → servono **maschere nuove in SIPO** per il caricamento,
  uno storage fino al deposito, R001 e la scansione antivirus (ANSC_08: solo «Inserito» prosegue).
  ⚠️ **Perimetro: tutti i 374 UC**, configurando compiutamente prima i più frequenti (da qui `FLG_ATTIVO`).
  ⚠️ **`ID_MAPPER` RIMOSSA, al suo posto `ANSC_CFG_CAMPO.TXT_TRANSCODIFICA`** (06/09/2026, su rilievo
  dell'utente). `ID_MAPPER` era un residuo v2.x — un adattatore di codice per famiglia — e
  **contraddiceva il cap. 9** («il payload non si costruisce per caso d'uso: si costruisce una volta
  sola sull'albero»); il punto 6 della modalità operativa arrivava a promettere «un mapper per tipo di
  atto». ⚠️ Ma non era solo inutile: era **il sintomo di una colonna mancante**. Nel foglio a mano di
  Dic_Nasc_001 **53 righe su 181** portano una regola di transcodifica («estrarre YYYY-MM-DD dalla
  stringa», «usare ID_DICHIARANTE come chiave in CONF_DICHIARANTE_NASCITA», «estrarre dal CLOB») e
  `ANSC_CFG_CAMPO` non aveva dove metterle. ⚠️ **Scelta dichiarata: `TXT_TRANSCODIFICA` è una
  SPECIFICA IN LINGUA CORRENTE per chi sviluppa, non un'espressione eseguibile** — dove la provenienza
  è una ricerca su un altro schema (`dichiarante.idANPR` → cercare il soggetto in `ANAG_USR`) nessuna
  stringa la esegue, e il documento lo dice invece di prometterlo. Ripulite **6 frasi** che
  promettevano un mapper per famiglia (zero occorrenze residue).
  ⚠️ **LE FORMULE SONO CONFIGURATE — `ANSC_CFG_FORMULA` (v3.14)**: sono **diciture prestabilite** che
  l'USC può inserire nell'atto, e la scelta si fa **in configurazione per UC**, non davanti al singolo
  atto. Numeri verificati: **2.200 righe «Formula», 366 UC su 374, 233 formule distinte**, da 1 a 22 per
  UC (**mediana 7**), **629 obbligatorie / 1.571 facoltative**. ⚠️ Per le formule le colonne «Note
  obbligatorietà formule» e «Condizioni obbligatorietà» del mapping sono **vuote su tutte e 2.200 le
  righe**: dichiara solo codice e obbligatorietà. Struttura: `ID_UC` (FK, come CFG_CAMPO/ALLEGATO),
  `COD_FORMULA` («197», «41-bis», «121-septies»), `TXT_FORMULA`, **`FLG_OBBLIGATORIA`** (lo dice ANSC)
  vs **`FLG_ADOTTATA`** (lo sceglie il Comune), `CAMPO_ANSC`, `NUM_ORDINE`, `COD_ORIGINE`.
  ⚠️ **ANSC_119/120 = `dec_tipo_formula_secretato`/`_non_secretato`**: contengono NUMERI di formula
  (122, 122-bis / 123, 124), non i testi → **OP-51 si riduce a: chi trascrive i 233 testi dalla
  normativa**. ⚠️ **Sei formule hanno un campo di testo libero nel modello evento** (147-ter,
  121-septies, 121-septies.1, 193, 140-bis, 122-bis.2): per quelle la configurazione deve dire anche
  DOVE scrivere il contenuto, altrimenti la formula si sceglie e resta vuota.
  Script: `strumenti/v3_14_{configurazione,regole,allineamento,ddl,backoffice,coerenza,formule,chiusura}.py`
  (in quest'ordine, dalla copia della v3.13);
  **`strumenti/diagrammi_erd.py` riscritto** (era perso) e ERD rigenerato; nuova primitiva
  `sostituisci_sezione()` in `docx_comune.py`.
- ⚠️ **IL CODICE UC È UNA TUPLA DI SCELTE, NON UN IDENTIFICATIVO OPACO** (verificato sui filmati della
  web app di preproduzione, 06/09/2026 — `Sorgenti Documentali/Registrazione schermo *.mov`).
  L'URL della web app si costruisce **cifra per cifra** mentre l'operatore risponde alle domande:
  `/ansc/1/evento/111xxxxx` → `11111xxx` → `11111000`, e il titolo della pagina lo scrive in chiaro:
  **`[1.1.1.1.1.0.0.0] Dichiarazione entro i 10 giorni – resa dal padre`**. Le posizioni osservate:
  1 registro (Nascita) · 2 tipo evento (Dichiarazioni rese all'USC) · 3 quale dichiarazione (Filiazione
  nel matrimonio) · 4 termine (entro 10 giorni) · 5 **dichiarante** · 6 **stato del soggetto**
  (0 vivo · 1 nato morto · 2 nato vivo e poi deceduto → sono `Dic_Nasc_001/002/003`).
  ⚠️ **DUE MECCANISMI DISTINTI, da non confondere nel disegno**: (a) alcune scelte **compongono l'UC** —
  il procuratore del padre porta la 5ª cifra da 1 a 4, cioè `11111000`→`11114000`, che è
  **Dic_Nasc_001 → Dic_Nasc_008**, un altro caso d'uso; (b) altre scelte **non cambiano l'UC** ma
  attivano una **sezione**: l'interprete lascia l'UC `11114000` e aggiunge «Soggetto intervenuto».
  La determinazione del nostro concentratore deve replicare (a); le condizioni di sezione sono (b).
- ⚠️ **LA MASCHERA ANSC MOSTRA 4 SEZIONI SU 11 DEL MAPPING.** Per `Dic_Nasc_001` la web app chiede solo
  Madre, Padre, Soggetto, Allegati. Le altre **non si chiedono perché ANSC le ricava dal contesto**
  (Ufficiale dello Stato Civile = l'USC autenticato, Formazione atto = data/ora, Luogo Redazione = la
  casa comunale) o **le compone** (Formula). Conseguenza per il concentratore: quei campi li valorizza
  lui da SIPO e dalla sessione, non l'operatore. ⚠️ La **Composizione** (il testo dell'atto) la **genera
  ANSC** e cambia con l'UC: con il procuratore compare «come procuratore speciale di, secondo quanto
  risulta da, documento che, munito del mio visto, inserisco nel volume degli allegati…».
- ⚠️ **«Obbligatorio» = L'ASTERISCO DELLA MASCHERA ANSC — la mia obiezione del 04/09 era sbagliata.**
  Nella web app il Padre ha «Cognome:» **senza** asterisco e «Nome *:» **con** asterisco, esattamente
  come il mapping (`padre.cognome` NO, `padre.nome` SI). Il ragionamento «il cognome della madre non
  può essere facoltativo» è di buon senso ma **smentito dall'evidenza**. Lettura rivista delle due
  colonne: **`Obbligatorio` = compilazione richiesta** (asterisco, e differisce fra UC: `luogoFiliazione`
  SI in 001/002, NO in 003); **`Condizioni obbligatorieta' = «obbligatoria»` = il campo fa parte
  dell'UC**, cioè appartiene al payload, non che vada compilato. ⚠️ Resta un'interpretazione: la
  semantica ufficiale non è pubblicata.
- ⚠️ **L'OBBLIGATORIETÀ NEL MAPPING ANSC È DICHIARATA IN DUE COLONNE CHE SI CONTRADDICONO** (04/09/2026).
  `Obbligatorio` e `Condizioni obbligatorieta'` divergono in **23.111 righe su 67.300 (34 %)**: 22.371
  con `NO` + condizione «obbligatoria», 740 con `SI` + «opzionale». ⚠️ **Il numero «20.346 campi
  obbligatori» citato ovunque nel documento è la sola colonna `Obbligatorio = SI`.** La prova che
  decide: in `Dic_Nasc_001` sezione Madre tutte e 33 le righe hanno condizione «obbligatoria» mentre
  `Obbligatorio` dice SI solo per 10 — e fra i NO c'è **`cognome`**, con `nome` a SI. Regola adottata:
  **governa la condizione** («obbligatoria»→S, «opzionale»→N, espressione→condizionata con la stessa
  grammatica `campo,operatore,valore` di regole e allegati, quindi **stesso motore**), `Obbligatorio`
  vale solo dove la condizione tace. Su Morte_001: 38 campi con la vecchia lettura, **85** con questa.
  ⚠️ La semantica ufficiale **non è pubblicata in nessuna fonte ANSC**: da chiedere a Sogei (open point).
  ⚠️ Nei CSV c'è una **riga di intestazione ripetuta per file** (374 in tutto): 67.674 righe = 67.300 di dato.
- **`ANALISI_Front-End-Angular_v0.6.docx`** (04/10/2026, **corrente**) — impostazione del front-end Angular 18 sulla
  libreria condivisa `fsha_mf-shared-library-main/` (micro-frontend, shell che condivide la libreria,
  **caricamento differito oggi non adottato → RF-FE-11/OP-FE-12**). ⚠️ **Nessun riferimento a Keycloak**
  (non confermato: l'autenticazione è rinviata all'impianto di sicurezza e profilazione, OP-FE-11).
  v0.1/v0.2 generate da `strumenti/genera_frontend_angular.py`; **dalla v0.3 si modifica il file reale**
  (`strumenti/fe_v0_3.py`). Figure: `strumenti/diagrammi_frontend.py img`.
  **v0.5** (`strumenti/fe_v0_5.py`): certificati di postazione assegnati al remote **mfOperation**,
  testata e piè di pagina sul nuovo `Footer cdr.jpeg`, sottocapitolo sulla **deroga del menu da ConfigMap**.
  **v0.6** (`strumenti/fe_v0_6.py`): ⚠️ la mappa delle schermate copriva **undici** voci con il back-office
  ridotto a tre righe aggregate; ora porta l'inventario delle **diciassette pagine** del back-office con i
  loro componenti di libreria. Corretti i conteggi («venticinque schermate», «cinque funzioni da
  costruire») e l'elenco dei micro-frontend, che non comprendeva mfOperation. 16 punti aperti.
- **`DISEGNO_Back-Office_ANSC_v0.6.docx`** (04/10/2026, **corrente**) — il disegno del back-office pagina
  per pagina: **16 pagine**, ciascuna con wireframe, scopo, **tabelle sottese** e **campi, colonne e
  azioni**. Porta **6 commenti di Word** e **22 punti aperti (BO-1…BO-22)**. Capitoli propri: la cornice
  (testata e piè di pagina), il **registro delle pagine e del menu** (4 tabelle `ANSC_CFG_APPLICAZIONE`/
  `_PAGINA`/`_PAGINA_ABILITAZ`/`_TEMA`), la copertura del modello dati, le indicazioni per Kubernetes.
  Wireframe: `strumenti/wireframe_bo.py` (primitive) + `pagine_bo.py` e `pagine_bo_v2.py` (le pagine).
  ⚠️ **Figure e piè di pagina sono una coppia**: la v0.6 ha dovuto risostituire **tutte e 18 le figure**,
  rimaste al piè di pagina a tre colonne dopo che la primitiva era stata riscritta — rigenerare i PNG non
  aggiorna il `.docx`, serve riscriverne il blob. ⚠️ Si legge insieme all'analisi del front-end: qui le
  pagine, lì i componenti ([R2] ↔ [F8]).
- **`ANALISI_Identita-Profilazione-IAM_v0.3.docx`** (02/10/2026, **corrente**) — il documento unico su
  identità, profilazione e IAM, che accorpa l'AS-IS e le due analisi del committente. Il TO-BE è una
  **scala di soluzioni S0…S4** dalla più conservativa alla più coerente, con dentro S3 la variante del
  **BFF**. ⚠️ **S0 non è un'alternativa: è il pavimento** — nessuna delle altre chiude i servizi che oggi
  rispondono senza gettone. 19 punti aperti (PI-01…PI-19). Script `strumenti/genera_identita_iam.py`,
  `v0_2_iam_soluzioni.py`, `v0_3_iam_bff.py`; figure `strumenti/diagrammi_iam.py img`.
- **`ASIS_Autenticazione-Profilazione_SIPO_v0.2.docx`** — la ricognizione dello stato di fatto:
  ⚠️ **due sicurezze che convivono**, quella delle **persone** debole (SIPO non autentica, si fida di
  header di portale, permesso per utente e non per ruolo) e quella delle **macchine** matura
  (PKI/keystore/SAML nel client ANPR, registro postazioni). 12 punti aperti + 21 rilievi.
- **`PROCEDURA_Formazione-Atto_SIPO-ANSC_v0.1.docx`** (10/09/2026) — il percorso dell'operatore in
  **otto passi**, dal menu di SIPO all'atto firmato, generato da `strumenti/genera_formazione_atto.py`
  **a partire dal template DAD** (svuotamento del corpo dopo l'elemento 29, come `genera-spec-api.py`).
  Figura `strumenti/diagrammi_formazione.py` → `img/formazione_atto.png`: due corsie (SIPO / ANSC),
  gli otto passi numerati, il ramo tratteggiato di chi non acquisisce il token, la linea del **punto
  di non ritorno**. Ogni passo ha una tabella «In sintesi» (che cosa serve · che cosa produce · se
  manca). ⚠️ **Due nodi che il documento mette in evidenza e che sono decisioni dell'ufficio, non
  tecniche**: (a) il **passo 2 è facoltativo ma si paga al passo 7** — senza token niente R005, senza
  identificativo del soggetto il deposito richiede il collegamento manuale «fortemente sconsigliato»;
  (b) ⚠️ **il passo 8 CONTRADDICE LA PRASSI DI ROMA**: oggi un atto si corregge **fino alla
  mezzanotte**, con ANSC la finestra si chiude all'avvio della firma. Tre strade tabellate: allineare
  la prassi · ritardare la firma a fine giornata · distinguere per tipo di errore. Chiude con le
  **quattro funzioni oggi mancanti** (maschere di caricamento documenti, campi solo-ANSC, consegna
  del codice di sessione con tempo residuo, stato ANSC nelle maschere di ricerca e dettaglio).
- **`SPEC_API_Integrazione-ANSC_v0.1.docx`** + **`ansc-v1.yaml`**, **`ansc-dizionari-v1.yaml`**,
  **`ansc-automazione-v1.yaml`**, **`genera-spec-api.py`** — specifica delle API di tutti i pod secondo
  `Naming_convention_X_API_v1.00.docx`. **I `.yaml` sono la fonte autoritativa**; il `.docx` (10 cap., ~980
  paragrafi, 211 tabelle, 45 operazioni, 29 codici di errore) è **generato** e non va editato a mano.
  Copre le schede di operazione complete, i modelli di dati per pod, l'elenco unico dei codici di errore, la
  lista di controllo di conformità, gli interventi di allineamento rispetto alla v2.6 e i punti aperti
  PS-1…PS-7. Cfr. il blocco «SPECIFICA DELLE API DI TUTTI I POD» in «Stato attuale del lavoro».
- **`verifica-conteggi.py`** — controllo di coerenza da eseguire **prima di consegnare** ogni nuova
  versione di un `.docx` (vedi il dettaglio in «Come leggere/scrivere i file»). **40 regole**, di cui 31
  verificate direttamente sulle sorgenti ANSC (decodifiche, mapping dei casi d'uso, **changelog dei
  rilasci** dalla v3.2, **contratti OpenAPI** dalla v3.5). Collaudato
  all'indietro: segnala «due componenti nuovi» su v2.6 e v2.7 e tace sulla v2.8. **Ha già trovato un
  errore reale in stesura**: «119 casi d'uso con due intestatari» invece di 63 (avevo sommato tutti i
  casi delle famiglie che *possono* averne due, non quelli che li usano).
- `Naming_convention_X_API_v1.00.docx` e `Naming_convention_X_DB_v1.01.docx` — **standard aziendali**
  (nomenclatura e specifica delle API; nomenclatura dei modelli dati). Sono metodologia da applicare, non
  contenuto da copiare: il DB standard [R5] governa i nomi di tabelle/colonne/vincoli di `ANSC_USR`, l'API
  standard [R6] governa percorsi, campi, artefatti del contratto e stesura delle schede di operazione.

Voci di tracciamento aperte sull'integrazione ANPR: **DV-32** (`CODICE_ANPR` popolamento/semantica),
**DV-33** (ambiente client forzato a TEST), **DV-34** (nessun allineamento delle decodifiche),
**DV-35** (credenziali di modulo versionate), **DV-36** (comuni cessati nelle tendine).

Analisi consolidata sugli **stati esteri** (rilevante per l'integrazione SIPO→ANSC):
- Il catalogo è la tabella Oracle `ANAG_USR.CONF_STATO_ESTERO`, **fuori dal Disegno Base Dati**
  (che la referenzia solo come FK): il DBD copre lo Stato Civile, la tabella sta in Anagrafe.
- Chiave di raccordo: colonna **`CODICE_ANPR`** → codice dello stato dell'archivio **ANPR_02**.
  Conversione lato server in `common/anpr-client/.../AnprUtilities.java` (righe 127 e 282,
  `setCodiceStato` ← `getCodiceAnpr`), via **reflection** (invisibile alle ricerche testuali).
- Le due entity JPA della stessa tabella **divergono**: `common/anagrafe-entities` non mappa
  `CODICE_CATASTALE`, `sipo-elezioni/elett-entities-elezioni` sì.
- Il front-end usa **solo `idStatoEstero`** (551 occorrenze di `.idStatoEstero}` nei template
  Thymeleaf, 0 di `.codiceAnpr}`): stato e località estera sono select codificate, mai testo libero.
  `ID_STATO_ESTERO = '1'` (ITALIA) è **hardcoded in 728 condizioni** di vista → non rinumerare.
- **ANSC non espone alcuna decodifica degli stati**: la titolarità del dato è di ANPR (tracciato
  come DV-32). La tabella è `anpr-9.2.9/src/tab/tab_stati_esteri.rst` («Tabella 02»): per Angola
  `ID=5` ma `CODISTAT/CODMIN=402`, `CODAT=Z302` → **ANPR_02 è nomenclatura ANSC**, in ANPR non esiste.
- `CODICE_ANPR` è **letta ma mai scritta**: nessun `setCodiceAnpr(...)` applicativo, nessuno script la
  popola (in collaudo è NULL), ma `UtilityController.java:8762` filtra su `"998"` (= "NON ATTRIBUIBILE",
  `CODISTAT 998`) → in produzione risulta popolata **per una via non presente nel workspace**.

Analisi consolidata sull'**integrazione ANPR** (rif. `STUDIO_Client-ANPR_v0.2.docx`):
- Unico confine con ANPR: `common/anpr-client/AnprClient` (690 classi), metodo
  `AnprClient.callAnprClient(requestParams, additionalParams, wsName, em)` (`client/AnprClient.java:60`).
  Protocollo **SOAP**; l'XML è costruito a mano dai 32 `xmlRequestGenerator/Richiesta<N>XmlGenerator`.
- **37 operazioni** dichiarate in `config/WSTypeHandler.java` su 11 famiglie (1000 iscrizione, 2000
  cancellazione, 3000 consultazione, 4000 estrazione, 5000 mutazione, 6001, 7001, A000 AIRE, P000, S001,
  TESTCONN); **32 con generator**, **23 realmente invocate** (~178 call-site).
- **Due modalità di accesso**: (A) chiamata diretta al client (Anagrafe, AIRE, Cambi residenza,
  Certificati, Elettorale…); (B) **proxy REST interno** — Stato Civile/Annotazioni/Comunicazioni
  chiamano il dominio `allineamSC` (`http://anprsipo:9393` = modulo `back-end/all-anpr-sipo`), che
  espone **14 endpoint con suffisso `SC`** e traduce in SOAP. 29 call-site, 27 attivi.
  → Per questo le 9 classi `AnprBL` dei moduli di stato civile sono **mai invocate**: non è codice
  residuo, è la via diretta predisposta e mai usata.
- Asimmetria da ricordare: **i soggetti si allineano**, **le decodifiche no**. Il servizio
  **7001 `scarica_tabelle` non è implementato** e nessun job/`@Scheduled`/script aggiorna le `CONF_*`
  (DV-34). L'intera famiglia 4000 (estrazione) è inutilizzata; della 3000 si usa solo il 3002.
- **Canali di INGRESSO dei dati da ANPR** (solo soggetti — cfr. cap. omonimo dello STUDIO):
  1. **Pull 3002 con persistenza**: la risposta è salvata in locale via
     `SoggettoBL.salvaSoggettoAnpr()` (`common/anagrafe-entities/.../bl/SoggettoBL.java:360`) →
     scrive `Soggetto`/`Nascita`/`Matrimonio`/`FamigliaConvivenza`. Chiamanti: `cri-be`
     (`SoggettoController.java:1693,1716,2155`), `irrep-be:325`, `aire-be:1019`, `cre-be:562`.
     **La 3002 NON è una semplice verifica** (lo è solo in `elettorale-be:570`, controllo CF).
  2. **Push notifiche N000**: `not-anpr` è un **server** SOAP (payload cifrato PKCS12) che scrive in
     locale (`Notifica2011.java:113` `soggettoRepository.save`). **8 attive su 11**: disabilitate
     (case commentati in `GestoreNotificheNris.java`) 1001 (:38), A001 (:170), A002 (:192), A006 (:214).
  3. **Subentro** (DPCM 194/2014, `anpr-9.2.9/src/subentro/`): una tantum, **non ripetibile**, e va
     **dal Comune verso ANPR** (solo schede soggetto/famiglia/convivenza). S001 non implementato lato
     client; `cross/anpr-generate-xml` e `cross/anprvalidator` sono i tool offline Sogei.
  → **Le tabelle di riferimento non hanno alcun canale**: caricate una tantum al subentro/migrazione.
  ANPR conosce il problema: la doc subentro tratta il «disallineamento della denominazione dei Comuni»
  e dice che «la correzione del nominativo dei Comuni potrà avvenire solo contestualmente al subentro».
  **Sintesi: dinamico sui soggetti, statico sui dati di riferimento.**
- Anomalie verificate: **ambiente hardcoded a TEST** (`AnprClient.java:78`; il pom si autodescrive
  «A Java **Test** Client») → il keystore di firma è sempre `TEST_Keystore.properties`
  (`RequestHandler.java:44`) — DV-33; **fall-through nello switch** (`WS7001`→XML `A001`,
  `WS5014`→`6001`, `WS5009`→`5010`, `WSS001`→null), latente perché quelle op. non sono invocate;
  credenziali di modulo versionate in `clientConfig.properties` (DV-35).
- I moduli `cross/anprvalidator` e `cross/anpr-generate-xml` sono **tool Sogei offline** (validazione
  XSD, generazione XML subentro): non fanno rete, non sono canali verso ANPR.
- **Falso allarme già smentito — non riaprirlo**: le chiamate al proxy passano letteralmente
  `"http://localhost:9393"` (51 punti), ma è un **ripiego inerte**: `RestClient.java:192-193` fa
  `url = urlProp.equals("local") ? url : urlProp` e **nessun profilo** vale `local` (i tre valorizzano
  `anprsipo-svil`/`anprsipo-test`/`anprsipo`). Vince sempre la config.
  Difetto **reale** invece: `catch` **vuoto** sulla chiamata di allineamento in
  `AttoNasciteFlow.java:402-404` → il fallimento verso ANPR è silenziato.

Come le **maschere** ottengono i dati di pertinenza ANPR (comuni, province, stati, località): **mai
da ANPR**, sempre dal DB locale Oracle (`DBSIPONW`, utenza `MATR_USR`, cfr. `application.properties`
dei BE). Catena tipo: vista Thymeleaf → utility FE → REST interno `/variazioniAnagrafiche/...` →
`Repository` JPA → tabella. Endpoint→tabella: `comuneByProvincia`→`COMUNE`, `getProvince`→`PROVINCIA`,
`statoEstero`→`CONF_STATO_ESTERO`, `getLocalitaByIdStatoEstero`→`LOCALITA`. Tendine **a cascata**
(`onchange` → `caricaComuni`/`caricaLocalitaEstere`), ogni passo è una query locale.
Attenzione (DV-36): `ComuneRepository` ha **tre varianti** della stessa ricerca —
`findComuniByProvincia` (nessun filtro → **include i cessati**), `findComuniByProvinciaAttivi`
(`AND c.dataCessazione IS NULL`), `findComuniByProvinciaNoRoma`. L'endpoint delle tendine usa la
**prima**; verificare sempre quale variante usa il controller prima di trarre conclusioni.

Analisi consolidata sull'**area Decessi** (rif. `MAPPA_Decessi_Schermate-Servizi-Tabelle_v0.2.docx`):
- Tre moduli: `front-end/decessi-web`, `back-end/decessi-be`, `common/decessi-entities`. Connessione
  come **`MATR_USR`** (schema Stato Civile, `DBSIPONW`); le tabelle anagrafiche (`COMUNE`, `LOCALITA`,
  `PROVINCIA`, `CONF_STATO_ESTERO`, `CONSOLATO_STATOCIVILE`, `STATUS_SOGGETTO_ANAG`) sono raggiunte per
  **sinonimo su `ANAG_USR`**. Nessuna entity dichiara `schema=` in `@Table`.
- **Backbone condiviso**: le 11 maschere `attoMorteTipo01…12` **estendono `AttoMorteTipo00Controller`**
  → stessi endpoint (`/findAttoDecessoData` load, `/saveAttoDecessoData` save) e stesse tabelle core.
  La variante di maschera è **guidata dal dato** (`CONF_TIPO_ATTI.mascheraUi`), non da programmi
  separati. Eccezioni FE: **Tipo04** (unica a creare l'atto via `/saveAtto` + SP
  `PKG_PRATICA.get_temp_numatto`) e **Tipo10** (unica con logica estero/consolato,
  `findConsolatiByIdStatoEstero`).
- Scritture core (`/saveAttoDecessoData`, `@Transactional`): `ATTO_DECESSO`, `ATTO`, `SOGGETTO`,
  `ATTO_DECESSO_AGENZIA`, `ATTO_DECESSO_ESTERO`, `ATTO_DECESSO_EXTEND`.
- **Routing dei servizi**: `decessi-be` fa load/save + decodifiche; ma annullamento pratica
  (`/cancellaAnnullaAtto`), tipo rito, parte/serie, stato pratica vanno a **`statocivile-be`**
  (dominio `DOMINIO_STATO_CIVILE`). Quindi la cancellazione effettiva NON è in decessi-be.
- **Casistica «a Roma» vs «fuori Roma» — diversificate** (rif. sorgente `Decessi_ANSC.xlsx`, un foglio
  per casistica): «a Roma» = **Dichiarazione** (atto originale, UC `2.1.0.x`, eventi ANSC
  `Morte_001…005`); «fuori Roma» = **Trascrizione** (atto formato altrove, UC `2.2.x`, eventi
  `Morte_009/011/015/020`). Il «fuori Roma» si sdoppia in altro comune vs estero; l'estero attiva la
  tabella dedicata `ATTO_DECESSO_ESTERO` (vuota per gli atti a Roma) ed è la maschera Tipo10.
  Diversificazione **funzionale/sul dato**, su **backbone tecnico unico**.
- Entità presenti ma **non usate** dai 4 controller core di decessi-be: `ATTO_SINTESI`,
  `ANNOTAZIONE_ATTO`/`ATTO_ANNOTAZIONE`, `RICHIESTE_RICEVUTE` (le annotazioni partono con redirect a
  `/creaAnnotazioniContestuali`, controller separato). `/eliminaAtto` è soft-delete ma il richiamo FE
  è commentato.

## Nota di riferimento (istruzione originale dell'utente)

METODO DI LAVORO:

1. Parti dal template target: leggi il .docx ed estraine l'ossatura (elenco
   sezioni, stili applicati, segnaposto, elementi obbligatori come TOC,
   intestazioni, tabelle standard). Genera l'output PARTENDO dal file .docx
   del template, così da preservare stili e formattazione — non ricostruire
   la struttura a mano.

2. Inventaria "Sorgenti Documentali/". Tratta anche il codice come evidenza
   (architettura, endpoint, configurazioni, dipendenze). Per ogni sezione del
   template individua quali sorgenti la alimentano e produci una MAPPA
   sezione → sorgenti. Segnala esplicitamente i buchi (sezioni senza
   copertura) e i conflitti tra sorgenti.

3. Redigi rispettando lo standard del template. Per ogni contenuto tecnico
   rilevante tieni traccia della sorgente da cui deriva.

4. Non inventare dati assenti dalle sorgenti. Dove manca informazione inserisci
   un segnaposto esplicito [DA VERIFICARE: ...] invece di colmare con ipotesi.

5. Salva in "Documenti finali/" come nuova versione.

PRIMA di generare il documento, mostrami: (a) l'ossatura estratta dal template,
(b) la mappa sezione → sorgenti con gap e conflitti, (c) un piano di stesura.
Attendi mio ok prima di produrre il .docx finale.

TARGET ATTUALE: un documento derivato da template_DAD_roma-capitale.docx,
costruito sulle sorgenti attualmente presenti in "Sorgenti Documentali/".
