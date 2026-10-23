# -*- coding: utf-8 -*-
"""Rilettura di coerenza dell'ANALISI_Integrazione-ANSC_v3.44 rivista a mano dall'utente
(22/10/2026): i rilievi consolidati in un foglio di lavoro, uno per riga, con il testo da cercare
nel .docx (Ctrl+F), la correzione proposta e se serve una decisione dell'utente.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/revisione_v3_44.py
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(QUI), 'REVISIONE_ANALISI-ANSC_v3.44_v0.1.xlsx')

# (gravità, area, capitolo, dove: testo da cercare, che cosa non torna, correzione, decisione)
R = [
    # ── A. danni meccanici
    ('Alta', 'Danno meccanico', 'Tutto il documento',
     'degli   Le letture · CONF_TIPO_ ID_MODELLO_ATTO · requisiti soddisf · certificati ed estr',
     'Un «sostituisci tutto» di «atti.» (forse per togliere il prefisso di schema atti. dalle DDL di Side) '
     'ha cancellato «atti.»/«ATTI.» anche nel testo: 20 occorrenze nella v3.43, 0 ora. Frasi troncate '
     '(«non finalizza gli », «non forma né firma », «la formazione degli »), nomi rotti '
     '(«CONF_TIPO_ ID_MODELLO_ATTO», «resta CONF_TIPO_», «estr», «soddisf»). Punti: Glossario, RF-21, '
     'Architettura (componenti, tabella unità), Adeguamenti database (ANSC_STATO_ATTO, ANSC_CFG_UC), '
     'dizionari ANSC, schede R002 e R009, vista di supervisione, App. A (ALLEGATO, firmatari, COMMENT).',
     'Ripristinare il testo della v3.43 punto per punto (lo posso fare io con uno script che confronta '
     'le due versioni). In futuro sostituire solo «REFERENCES atti.» / «INSERT INTO atti.».', 'No'),
    ('Media', 'Danno meccanico', 'Scheda del documento',
     'ANALISI_Integrazione-ANSC_v3.41',
     'Il riquadro di testa dichiara la v3.41; R14 cita DISEGNO_Back-Office v0.8 (corrente v0.10); '
     'R9 e R6 sono lo stesso file.',
     'Nome file v3.44 (o la versione che uscirà); R14 → v0.10; fondere R9 in R6.', 'No'),
    ('Media', 'Rimandi', 'Più capitoli',
     'capitolo 13.1 · §3.2 · §5.3 · §11.7 · §15.4.5 · «Mappatura del payload» · «Roadmap» · '
     '«La determinazione dell’UC e le regole di controllo» · «Struttura e meccanismo della Configurazione» '
     '· capitolo sul deployment',
     'Rimandi a numeri o titoli che non esistono più (la rinumerazione li ha rotti: «capitolo 13.1» è '
     'ora «Modello di esecuzione», il contenuto è in «Processo ANSC di validazione dell’atto»). '
     'RF-15 rimanda al modello di esecuzione ma l’emergenza sta nel processo di riferimento.',
     'Tutti i rimandi per titolo: «Costruzione del payload e validazione dei campi obbligatori», '
     '«Struttura dettagliata delle tabelle di configurazione», «Indisponibilità: la modalità di emergenza '
     'e il rientro», «Gestione dei dizionari SIPO». Togliere «Roadmap» e «deployment».', 'No'),
    ('Media', 'Rimandi', 'Open Point', 'OP-76 … paragrafo sul passo «Definisci»',
     'Il paragrafo è stato rinominato «Il passo «VALIDA»».', 'Aggiornare il rimando (vedi anche il rilievo su VALIDA).', 'No'),
    ('Bassa', 'Stile', 'Più capitoli',
     'Chiuso nella v3. · Dalla v3.33 · aggiunto nella v3.29 · Fino alla v3.25 · rispetto alle versioni precedenti · ⚠️',
     'Marcature di versione e «⚠️» rimaste in OP-12/25/28/35/44/47/50/56/59/60/61/73, riconciliazione, '
     'ALLEGATO, App. B («Istanti temporali»), contro lo stile scelto.',
     'Togliere: la storia sta nella «Storia del documento».', 'No'),
    ('Bassa', 'Refusi', 'Più capitoli',
     'oppurtunità · D’atra · trascodifica · elemnto · atto_primarioidAnsc · il codice IdAnsc è . · '
     'Sesso del incaricato · dall’uso mento · Esprima · inviato a ANSC',
     'Refusi e frasi incomplete; «Riportiamo come esempio la corrispondente pagina di Milano:» senza '
     'figura; testo illeggibile su STEP_LAVORAZIONE/STEP_TABLAV; celle troncate «e resta agli |» e '
     '«come per lo store di stato degli |»; «Ne resta una seconda ovvero se…».',
     'Correggere; per STEP_LAVORAZIONE: «STEP_TABLAV è la scheda raggiunta («1»…«4»), STEP_LAVORAZIONE '
     'vale 0, 1 o -1 (atto figlio); significato [DA VERIFICARE]».', 'No'),
    ('Bassa', 'Stile', 'La gestione delle notifiche (Side)', '??? · sarà sempre Milano · Riesco ad alimentarlo',
     'Note di lavoro del documento di Milano riportate come contenuto.',
     'Ripulirle o marcarle come «note della sorgente».', 'No'),

    # ── B. numerazione comunale
    ('Alta', 'Numerazione', 'Il processo… / Numerazione comunale',
     'Con una sequence per anno · MAXVALUE 999999 · NOCACHE e ORDER · la sequence non può superarle · '
     'tiene coerente la sequence · job di dicembre · NEXTVAL · ALL_SEQUENCES · LOCK TABLE',
     'Il testo dice che la serie è NUMERATORE_COMUNALE, ma restano 12 riferimenti a SEQ_NUM_COMUNALE, '
     'il job e la procedura di creazione, LOCK TABLE, e «Lo stacco, passo per passo» è scritto sulle '
     'sequence. Una frase richiama le «due garanzie» della sezione tolta.',
     'Riscrivere lo stacco sul numeratore: (1) se manca, INSERT della riga dell’anno (ORA-00001 da corsa '
     'si ignora); (2) UPDATE … SET pg_atto = pg_atto + :n RETURNING pg_atto (il lock di riga serializza '
     'per anno: LOCK TABLE non serve); (3) INSERT PRENOTAZIONE_ATTI e DATI_ATTO_ESTERNO; (4) COMMIT. '
     'Vantaggio da dichiarare: un rollback ripristina il contatore → blocchi contigui e nessun buco per '
     'costruzione. Registrazione a posteriori: pg_atto = GREATEST(pg_atto, :numero).', 'No'),
    ('Alta', 'Numerazione', 'Appendice A — Numerazione Comunale', 'NUMBER(6,0).',
     'DDL di NUMERATORE_COMUNALE non eseguibile (punto dopo NUMBER(6,0), virgola prima della parentesi) '
     'e senza chiave: due «prime chiamate» concorrenti creerebbero due righe per lo stesso anno. Manca '
     'il grant a <UTENZA_NUM>. nr_ordinamento non ha funzione dichiarata.',
     'PK sull’anno, CHECK pg_atto 0…999999, DEFAULT 0, grant SELECT/INSERT/UPDATE a <UTENZA_NUM>. '
     'Nomi coerenti con le tabelle sorelle (nr_anno_atto) e ts_ per i TIMESTAMP (convenzione Side). '
     'Spostarla accanto a PRENOTAZIONE_ATTI.', 'Sì: a che cosa serve nr_ordinamento?'),
    ('Alta', 'Numerazione', 'Appendice A + Adeguamenti database',
     'SEQ_NUM_COMUNALE_<anno> | · PRC_CREA_SEQ_NUM_COMUNALE · JOB_CREA_SEQ_NUM_COMUNALE · e le sequence della numerazione',
     'Restano nella tabella degli oggetti («Non si ritiene necessario essere una tabella»), nella '
     'didascalia e nel disegno dell’ERD (Figura 3), nel titolo della sezione e nella DDL (CREATE SEQUENCE, '
     'procedura, job, grant).',
     'Togliere; riga «NUMERATORE_COMUNALE | La serie dei numeri comunali | una riga per anno, creata alla '
     'prima richiesta» nella tabella degli oggetti; rigenerare l’ERD.', 'No'),
    ('Media', 'Numerazione', 'Open Point', 'OP-44 … La serie è una sequence per anno · OP-73 … CREATE SEQUENCE',
     'OP-44 e OP-73 (c) descrivono le sequence.',
     'OP-44: serie in NUMERATORE_COMUNALE. OP-73 (c): grant sul numeratore e concorrenza alla creazione '
     'della riga dell’anno.', 'No'),
    ('Media', 'Numerazione', 'Appendice B', 'creaSerie',
     '«creaSerie — Crea la serie di un anno» presuppone il job; con il numeratore la riga nasce alla prima '
     'chiamata. I «buchi» ora nascono solo da creaNumero.',
     'creaSerie = INSERT facoltativa e idempotente della riga dell’anno, oppure toglierla; aggiornare '
     'ansc-numerazione-v1.yaml e rigenerare la SPEC.', 'Sì: tenere creaSerie?'),
    ('Media', 'Numerazione', 'Più capitoli', 'NUM_COMUNALE',
     'Il numero comunale ha tre tipi: VARCHAR2(30) in ANSC_STATO_ATTO, VARCHAR2(6) in Impatti sul '
     'Database, NUMBER(6) in DATI_ATTO_ESTERNO. Il testo di NUM_COMUNALE rimanda a OP-44 come aperto, '
     'ma è chiuso.', 'Un tipo solo (NUMBER(6)); togliere il rimando a OP-44.', 'No'),
    ('Bassa', 'Numerazione', 'Il processo… / Numerazione', 'numero suggerito da ANSC · si stacca al deposito',
     'Contraddice «nessun servizio di ANSC lo attribuisce» e lo stacco all’Anteprima, prima del deposito.',
     '«suggerito dalla web app»; «si stacca all’Anteprima».', 'No'),
    ('Bassa', 'Numerazione', 'Appendice A', 'DATI_ATTO_ESTERNO',
     'nr_anno_atto è ripetuto ma nulla garantisce che coincida con quello della richiesta, e l’unicità '
     'della serie si fida di quel valore.',
     'UK (id_prenotazione_atti, nr_anno_atto) su PRENOTAZIONE_ATTI e FK composta da DATI_ATTO_ESTERNO.', 'No'),

    # ── C. allineamento al processo di riferimento
    ('Alta', 'Processo', 'Il processo… — Il passo «VALIDA»',
     'Porterà alla pagina finale di SIPO',
     'Il paragrafo dice che VALIDA porta a una pagina finale di solo salvataggio, dopo la quale non si '
     'torna indietro. Contraddice il processo stesso: VALIDA chiama R009, poi vengono firme dei '
     'dichiaranti, conformità e firma USC; il ritorno ai dati resta possibile (stato 0) fino alla firma '
     'dell’USC, che è il punto di non ritorno. Pare il vecchio testo di «Definisci» con il titolo cambiato. '
     'In più «Definisci» va rinominato «stampe» in una riga e resta «Definisci» in altre.',
     '«Dalla pagina di Anteprima il pulsante «VALIDA» chiama R009: con esito positivo l’atto riceve '
     'l’idAnsc ed è CONFERMATO, e si prosegue con le firme. Il ritorno sui dati resta possibile fino alla '
     'firma dell’USC e riporta l’atto allo stato 0.» E una riga di lessico, una volta sola: VALIDA = R009; '
     'Definisci (o «Stampe») = salvataggio in SIPO dopo la firma USC, stato 2.',
     'Sì: che cosa fa «Definisci» e come si chiama'),
    ('Alta', 'Processo', 'Il processo… — Riepilogo', 'metterlo in stato 1 BOZZA',
     'Dopo la validazione il ritorno ai dati porta lo stato a «1 BOZZA», mentre la nota subito sotto, la '
     'tabella degli stati e il CHECK usano 0 BOZZA_APPLICATIVA (proprio perché 1 BOZZA non dice che '
     'l’idAnsc esiste).', '«… lo stato locale passa a 0 BOZZA_APPLICATIVA e la validazione va ripetuta» '
     '(rimando a OP-75 a).', 'No'),
    ('Alta', 'Processo', 'Il processo… — tabella degli stati',
     'Cancellazione della firma dell’ufficiale · 3 ANNULLATO INEFFICACE',
     'R011 «elimina logicamente l’evento» (contratto R011_cancellazione_atto): non cancella una firma, e '
     'il prerequisito è «non ancora firmato dall’USC». 3 ANNULLATO e 10 INEFFICACE sono due stati '
     'distinti di ANSC_11; manca 8 RIFIUTATA (R016). Altrove (Vincoli, Architettura, schede R011, '
     'funzioni ANSC) R011 porta ad ANNULLATO.',
     'Righe separate: «Eliminazione dell’evento prima della firma USC | 9 CANCELLATO | R011»; '
     '«Annullamento dopo la formazione | 3 ANNULLATO | rettifica R013»; «Annullamento per inefficacia | '
     '10 INEFFICACE | solo web app»; «8 RIFIUTATA | R016». Uniformare «R011 → CANCELLATO» ovunque '
     '(da confermare in preproduzione).', 'No'),
    ('Alta', 'Processo', 'Vincoli · Architettura · Modello di esecuzione · App. B',
     'R001 → R005 → R009 → R006 → R007 · «Finalizza» → … R005 consultazione soggetto · alla finalizzazione',
     'Le sequenze dei servizi scritte in più punti sono quelle vecchie: R005 dopo R001 o «alla '
     'finalizzazione» (nel riferimento sta nel Dettaglio, prima dell’UC), mancano numero comunale, R012, '
     'l’attestazione di conformità (R010 + R007) e la chiusura con R014. Il «percorso ordinario» dice '
     '«compila e definisce come oggi; alla finalizzazione…».',
     'Una sequenza unica, ripetuta uguale: Dettaglio (R005) → Riepilogo (UC, pre-filtro) → R001 → '
     'Anteprima (numero comunale) → VALIDA (R009) → firme dichiaranti (R006/R012) → conformità (R010, '
     'R007) → firma USC (R007) → Definisci → Chiudi (R014 se previsto).', 'No'),
    ('Media', 'Processo', 'Premesse (RF-3/4/5) · Costruzione del payload · Back-office',
     '«Verifica» · «Finalizza»',
     'I pulsanti Verifica e Finalizza non esistono nel processo di riferimento (Avanti / VALIDA / '
     'Definisci / Chiudi). RF-5 salta firme dei dichiaranti e conformità.',
     'RF-3: «Il Riepilogo esegue il pre-filtro (RF-9)»; RF-4: «il superamento abilita l’Anteprima e '
     'VALIDA»; RF-5: «VALIDA avvia R009; seguono firme dei dichiaranti, conformità e firma USC». '
     'Sostituire «Finalizza» anche nel payload e nel back-office.', 'No'),
    ('Media', 'Processo', 'Vincoli — Il processo di formazione dell’atto (otto passi)',
     'Su otto passi, quattro chiamano ANSC',
     'Gli otto passi non seguono il riferimento: ricerca dei soggetti lasciata aperta, UC determinato «alla '
     'chiusura», niente numero comunale, attestazione «generata insieme all’atto». E «gli altri tre» '
     'invece di quattro.', 'Ridurre il capitolo a sintesi del processo di riferimento, rinviandovi; '
     'correggere «quattro».', 'No'),
    ('Media', 'Processo', 'Recuperi · Back-office · Ciclo di vita (Figura 14)',
     'Resta FIRMATO DA DICHIARANTE · Manca la sola firma dell’USC',
     'Manca lo stato 11 FIRMATO PER CONFORMITÀ: prima della firma USC lo stato è 11, non 4. Manca la riga '
     'di recupero dell’attestazione; la didascalia del ciclo di vita non ha 11 né R012 né lo stato 0.',
     'Firma USC: «Resta FIRMATO PER CONFORMITÀ»; riga «Attestazione (R010, R007) | credenziali errate, '
     'documenti non Inseriti | resta 4 | rigenerare l’anteprima e rifirmare»; aggiornare figura e '
     'didascalia.', 'No'),
    ('Media', 'Processo', 'Il processo… — Dati anagrafici', 'tramite la tabella SOGGETTI_USECASE',
     'Circolarità: l’intestatario si individua da SOGGETTI_USECASE «per UC» già nei Dati anagrafici, ma '
     'l’UC si determina solo al Riepilogo, dopo.',
     'Dire da dove viene l’intestatario prima dell’UC (dal Modello/CONF_TIPO_ATTI e dal ruolo del soggetto '
     'in SIPO, oppure da una determinazione provvisoria dell’UC). Aggiungerlo a OP-76.',
     'Sì: da dove si ricava l’intestatario'),
    ('Media', 'Processo', 'Modello di esecuzione', 'solo quando serve depositare o firmare',
     'L’OTP serve già nel Dettaglio, per R005.', '«alla prima operazione verso ANSC (tipicamente R005 '
     'nella pagina di dettaglio)». «L’acquisizione del token … tramite telefono» → «dell’OTP».', 'No'),
    ('Media', 'Processo', 'Il processo… — tabella degli stati', '1 BOZZA | Bozza disponibile solo tramite WebApp',
     'La prenotazione R009 per il parto plurimo crea atti in BOZZA anche dal gestionale (il back-office lo '
     'prevede).', '«1 BOZZA | R009 /prenota/evento (parto plurimo) o web app».', 'No'),
    ('Media', 'Processo', 'Il processo… — Anteprima', 'certificato di conformità',
     'Altrove è sempre «attestazione»; «certificato» in ANSC è R002, che consuma un OTP di firma.',
     '«attestazione di conformità (anteprima R010, firma R007 /attestazione/firma)».', 'No'),
    ('Media', 'Processo', 'Il processo… — Ricerca dei soggetti · App. A',
     'Da decidere se necessaria · campo IdSoggettoANSC · dati di ritorno dalla funzione R009 · non è mandatoria',
     'Il processo lascia aperta una tabella che lega codice individuale e codice ANSC, e propone un campo '
     'nuovo sulla tabella di SIPO; ma ANSC_SOGGETTO_IDENTIFICATIVI è descritta come decisa. L’App. A dice '
     '«non mandatoria» e la alimenta da R009 invece che da R005.',
     'Decidere; se resta: togliere la frase «da decidere», scrivere R005 in App. A, citare le colonne '
     'ID_SCHEDA_ANPR / ID_UNICO_NAZIONALE / ID_ANSC_SOGGETTO.',
     'Sì: ANSC_SOGGETTO_IDENTIFICATIVI obbligatoria o no'),
    ('Media', 'Processo', 'Il processo… — Chiudi', 'impedirà (consuetudine',
     'Frase ambigua sulla finestra fino alle 24, e altrove si dice che nel software la finestra non c’è.',
     '«Con ANSC non sarà più possibile la prassi di correggere l’atto fino alle ore 24: dopo la firma '
     'dell’USC l’atto è immodificabile. La prassi è organizzativa, SIPO non la impone.»', 'No'),
    ('Media', 'Processo', 'Il processo… — emergenza', 'Una sola cosa non è mai eseguibile',
     '«Una sola cosa» contro la tabella subito dopo («Deposito e firme | Non consentiti»); il rientro '
     'omette l’attestazione.', '«Non sono mai eseguibili il deposito e le firme»; rientro con '
     'R006/R012, attestazione R007, firma R007.', 'No'),
    ('Media', 'Processo', 'SIPO in relazione alla web app — continuità operativa',
     'non ha oggi alcuna risposta scritta',
     'Il documento ha già risposte: modalità di emergenza (ANSC/concentratore giù), numerazione a '
     'posteriori e aggancio (SIPO giù).', 'Riformulare e allineare OP-42.', 'No'),
    ('Media', 'Processo', 'Il flusso operativo — tabella dei passi', 'Chiudi',
     'Manca il passo «Chiudi» con R014 (flag «Comunicazione anagrafica») e R010 nel passo della '
     'conformità.', 'Aggiungere; colonna «Pagina SIPO» per allinearsi alla figura.', 'No'),

    # ── D. atti a testo libero
    ('Media', 'Testo libero', 'Costruzione del payload — Atti a Testo Libero', 'Atti a Testo Libero',
     '«Atto a testo libero» ha due significati: nella fase B, in ALLEGATO.fg_testo_libero e OP-71 è un '
     'documento allegato a un atto che ha un UC; nella sezione nuova è un atto intero senza UC, formato '
     'sulla web app. Le due opzioni stanno solo nella figura; il testo cita «l’opzione 2» senza '
     'descriverla. Lo stato «Sospeso» non è nel CHECK di STATO.',
     'Due nomi distinti («atto non gestito» / «documento a testo libero»); descrivere nel testo i due '
     'percorsi (posso usare i diagrammi di oggi); per Gestione 1 valutare l’UC di servizio *_999 con '
     'motivoRecupero 3 «Caso d’uso non previsto» (ANSC_96), il veicolo ufficiale ANSC; aggiungere lo stato '
     'di sospensione al CHECK; ricollegare OP-66/OP-71.', 'Sì: nomi e codice dello stato «Sospeso» (YY)'),

    # ── E. ANSC_EVENTO / store
    ('Alta', 'Modello dati', 'Appendice A — Tabelle di controllo del flusso', 'Ansc-evento',
     'Ricompare la tabella «evento» di Side (~50 colonne), contro la decisione della v3.44 «una sola '
     'tabella per l’atto» (ANSC_STATO_ATTO si dichiara «corrispondente della tabella evento di Side»). '
     'Non è eseguibile: nome col trattino, tipi PostgreSQL, CHECK «= ANY (ARRAY[…])», COMMENT su '
     '«evento» e su colonne inesistenti (cd_fiscale_operatore, ds_nome_operatore…), una colonna inghiottita '
     'da un commento in linea (ty_ruolo_operatore_usc). La DDL di firmatari punta a evento(id_evento).',
     'Se è solo riferimento a Side: riquadro «struttura di origine, non adottata», fuori dalla DDL. Se è '
     'una scelta nuova: riaprire la decisione, tradurla in Oracle e togliere le colonne già in '
     'ANSC_STATO_ATTO.', 'Sì: residuo o scelta nuova?'),
    ('Media', 'Modello dati', 'Adeguamenti database — ANSC_STATO_ATTO', 'anti-doppio-accodamento · atto×operazione',
     'Nessuna unicità per atto: la ripresa «legge la riga per atto» ma due righe aperte sarebbero '
     'possibili. «anti-doppio-accodamento» è lessico da coda. Tipi divergenti dalla DDL (ID_TIPO_EVENTO, '
     'ID_TIPO_CONTENUTO 20 vs 10; ID_MODELLO_ATTO 30 vs 5); ID_VERSIONE dichiarata FK ma per valore; '
     'ID_UC_ANSC vs COD_UC_ANSC; l’elenco a sei stati è superato (il CHECK ne ha 13).',
     'UK (ID_ATTO_SIPO, COD_TIPO_OPERAZIONE); allineare i tipi alla DDL; «ID_VERSIONE | per valore»; '
     'rimandare l’elenco degli stati al CHECK.', 'No'),
    ('Media', 'Modello dati', 'Decisioni — PC-2, PC-3, PC-5', 'va eliminata via R011 e ri-depositata · polling',
     'PC-3 propone R011 + nuovo deposito dopo una modifica (il processo usa lo stato 0 e la rivalidazione '
     'dello stesso atto); PC-5 propone polling e riconciliazione periodica (deciso: riconciliazione su '
     'richiesta), e rinvia a OP-03 chiuso; PC-2 dice che lo store conserva solo chiave e stato, ora '
     'conserva il modello intero e la ripresa.',
     'Riscrivere le tre decisioni sullo stato attuale.', 'No'),
    ('Media', 'Modello dati', 'Appendice A — firmatari, forzatura_validazione, comunicaz_anagrafica_usecase',
     'bigserial · int8 · bpchar · ::bpchar · VALUES (',
     'DDL di Side in sintassi PostgreSQL, senza schema: lo script non arriva in fondo. firmatari: FK verso '
     'tabelle inesistenti, PK sul solo id_soggetto (una firma per soggetto per sempre). '
     'comunicaz_anagrafica_usecase: 358 righe in INSERT a più VALUES (non in Oracle 12.2), 53 righe con '
     '\'\' su colonna NOT NULL (in Oracle è NULL → errore), nome di vincolo di 46 byte, non descritta nel '
     'corpo né nella tabella degli oggetti.',
     'Tradurre in Oracle con ANSC_USR. e lo standard dei vincoli (posso farlo io), firmatari legata ad '
     'ANSC_STATO_ATTO; dati di comunicaz in un file di carico a parte; aggiungere la tabella al corpo.',
     'Sì: tradurre o tenere come «struttura di origine»'),
    ('Media', 'Modello dati', 'Appendice A', 'ANSC_CFG_VERSIONE',
     'Le FK verso ANSC_CFG_VERSIONE (CFG_UC, CFG_SEZIONE, ALLEGATI/SOGGETTI_USECASE) precedono la sua '
     'CREATE: eseguito in ordine lo script fallisce.', 'Spostarla in testa o dichiarare le FK in coda con ALTER TABLE.', 'No'),
    ('Bassa', 'Modello dati', 'Appendice A — introduzione', 'Tutti gli oggetti sono nuovi',
     'Tace i grant su ANAG_USR.SOGGETTO e la tabella ALLEGATO in MATR_USR.', 'Aggiungerli (OP-74, OP-68).', 'No'),
    ('Media', 'Modello dati', 'Adeguamenti database — elenco delle tabelle', 'Una sola tabella nuova nasce invece in MATR_USR',
     'L’elenco degli oggetti non ha ANSC_CFG_VERSIONE, ANSC_CFG_FORMULA, ANSC_CFG_DOMINIO_SIPO, '
     'RICONCILIAZ_DIZIONARI, firmatari, forzatura_validazione, comunicaz_anagrafica_usecase, '
     'NUMERATORE_COMUNALE.', 'Completare con schema e ruolo.', 'No'),
    ('Bassa', 'Numeri', 'Premesse — RNF-3', '3·10⁴',
     'Stima 30.000 atti di morte l’anno, il documento stesso ne riporta 52.142 dalla ricognizione.',
     '«52.142 decessi l’anno, circa 210 per giorno lavorativo»; aggiornare «~120 atti/giorno».', 'No'),

    # ── F. configurazione
    ('Alta', 'Configurazione', 'Struttura dettagliata delle tabelle di configurazione — ANSC_CFG_CAMPO',
     'ID_DECODIFICA_ANSC · BUSINESS_LOGIC',
     'Tabella descrittiva e DDL divergono: CAMPO_ANSC 120/1000, SCHEMA e TABELLA_SIPO 200/100, CAMPO_SIPO '
     '120/100, VALORE_DEFAULT 1000/100; ID_DECODIFICA_ANSC NUMBER facoltativo nel testo, VARCHAR2(10) NOT '
     'NULL nella DDL. NOT NULL su SCHEMA/TABELLA/CAMPO_SIPO impedisce i campi senza sorgente (proprio '
     'quelli per cui esiste VALORE_DEFAULT). Due COMMENT su BUSINESS_LOGIC (colonna inesistente: è '
     'ID_BUSINESS_LOGIC), duplicati, e uno dice «Script» mentre il testo dice «non è uno script». '
     'Commento di Word «Aggiungere uc+versione»: UC e baseline arrivano già da ID_SEZIONE.',
     'Allineare le lunghezze (una sola scelta); rendere nullabili le tre colonne SIPO e ID_DECODIFICA_ANSC; '
     'COMMENT su ID_BUSINESS_LOGIC; OPERATIVO → FLG_OPERATIVO ([R5]); rispondere al commento.',
     'Sì: le lunghezze giuste'),
    ('Media', 'Configurazione', 'Struttura dettagliata — ANSC_CFG_UC / ANSC_ANA_UC', 'ID_TIPO_DOCUMENTO · ID_TIPO_EVENTO',
     'Stessi nomi di colonna con significati diversi: ID_TIPO_EVENTO è «MORTE, NASCITA» in CFG_UC e il '
     'codice ANSC_01 in ANA_UC; ID_TIPO_DOCUMENTO è «CREAZIONE, TRASCRIZIONE» in una e il canale DMNM '
     'nell’altra. CFG_UC senza unicità (UC per baseline, priorità). ANSC_ANA_UC non ha ID_TIPO_CONTENUTO, '
     'che il testo dice replicato.',
     'Usare i codici ANSC o rinominare; UK (COD_UC_ANSC, ID_VERSIONE) e sulla priorità; aggiungere '
     'ID_TIPO_CONTENUTO VARCHAR2(10).', 'No'),
    ('Media', 'Configurazione', 'Struttura dettagliata — catalogo delle logiche', 'ereditata dalle decodifiche ANSC',
     'ID_DOMINIO «ereditata dalle decodifiche ANSC» contro «numerazione separata e interna»; OP-56 citato '
     'come aperto ma chiuso; il COMMENT di TIPO_LOGICHE_DI_SCELTA ha due domini, il testo tre; il '
     'dominio delle logiche non è vincolato (una logica di sezione può finire nella scelta dell’UC).',
     '«Identificativo del dominio, numerato in proprio»; «OP-56, chiuso»; aggiungere il dominio 3; CHECK '
     'ID_DOMINIO = 1/2/3 sulle tabelle che le usano.', 'No'),
    ('Media', 'Configurazione', 'Struttura dettagliata · Back-office · OP-65', 'COD_ORIGINE',
     'Testo e back-office dicono che campi, sezioni, allegati e formule conservano COD_ORIGINE; la DDL di '
     'ANSC_CFG_CAMPO e ALLEGATI_USECASE non l’ha, e OP-65 dice che non è stata reinserita. Celle di OP-65 '
     'e OP-68 slittate di colonna.', 'Togliere la promessa o reinserire la colonna; sistemare le celle.',
     'Sì: COD_ORIGINE sì o no'),
    ('Media', 'Configurazione', 'Il versionamento della configurazione', 'quattro stringhe libere · COD_VERSIONE_CONFIG',
     'Descrive come attuale lo stato prima della baseline (stringhe libere, CAMPO senza versione): oggi '
     'tutte le tabelle hanno ID_VERSIONE FK. Rimette «copertura e mutua esclusione», che PC-9 dichiara non '
     'dimostrabili. La sentinella è «Automatica», mentre i dizionari escludono ogni schedulazione (OP-23). '
     'Il perimetro della baseline non comprende SOGGETTI_USECASE e RICONCILIAZ_DIZIONARI.',
     'Al passato o riscritto sullo stato attuale; «simulazione su atti reali»; sentinella su comando o '
     'subordinata a OP-23; completare il perimetro.', 'No'),
    ('Bassa', 'Configurazione', 'ALLEGATI_USECASE', 'D.LIB.M.01',
     'La PK (cd_usecase, ty_allegato, id_versione) ammette una sola riga 998 per UC, ma D.LIB.M.01 ne '
     'prevede più; ds_allegato è la chiave d’importazione ma non è unica.', 'UK (id_versione, cd_usecase, ds_allegato).', 'No'),

    # ── G. dizionari
    ('Alta', 'Dizionari', 'Gestione dei dizionari SIPO / ANSC · App. A', 'Tabelle di decodifica dei dati interni di sipo',
     'La separazione è a metà: «Gestione dei dizionari SIPO» contiene DOMINIO_DECODIFICA e VALORE_DOMINIO '
     'descritti come replica di ANSC (R901), mentre le tabelle di Side dei domini interni (tipo_dominio, '
     'valori_dominio: domini 17, 18, 19, 107, 108 citati da DATI_ATTO_ESTERNO, firmatari, comunicaz) non '
     'hanno DDL — eppure c’è un INSERT INTO valori_dominio con colonne che VALORE_DOMINIO non ha. In App. A '
     'DOMINIO_DECODIFICA è «dati interni di sipo» nel titolo e «decodifiche ANSC replicate» nel COMMENT. '
     '«Il comando che le popola … nel paragrafo seguente» ora sta nel capitolo dopo.',
     'Riportare DOMINIO_DECODIFICA/VALORE_DOMINIO nel capitolo ANSC prima del comando; nel capitolo SIPO '
     'descrivere tipo_dominio/valori_dominio di Side con la loro DDL Oracle (PK cd_ente, ty_dominio, '
     'id_valore), prima dell’INSERT.', 'Sì: confermi la ripartizione?'),
    ('Alta', 'Dizionari', 'Appendice A — VALORE_DOMINIO', 'cd_valore',
     'La colonna è stata tolta, ma l’indice IX_VALORE_DOMINIO_RICERCA e la vista V_ANSC_DIZ_VALIDO la usano: '
     'la vista — il contratto verso SIPO — non si crea (ORA-00904).',
     'Togliere v.cd_valore; indice su (id_dominio, nm_dominio) o toglierlo.', 'No'),
    ('Media', 'Dizionari', 'Gestione dei dizionari ANSC — il comando', 'sostituzione integrale dei valori',
     'Il passo 5 dice «sostituzione integrale» (cancella i valori spariti); il processo del fornitore '
     'dice che non si cancella, si chiude la validità, e la frase dopo afferma che coincidono.',
     '«Per ogni decodifica, in una transazione: inserimento dei nuovi, aggiornamento dei modificati, '
     'chiusura della validità dei non più restituiti; aggiornamento della versione.»', 'No'),
    ('Media', 'Dizionari', 'Dizionari ANSC · Back-office · Sicurezza · App. B',
     'storico dei caricamenti · ANSC_DIZ_ · elencaAggiornamenti',
     'Lo storico dei caricamenti è dichiarato assente (rinuncia a Side) ma usato: riga di caricamento, '
     'schermata, ruoli Amministratore/Auditor, operazioni API. Restano i nomi ANSC_DIZ_* in Glossario, '
     'Architettura e Sicurezza.',
     'O tabella di caricamento con DDL, o esito in ANSC_LOG_AUDIT e via le due operazioni; nomi → '
     'DOMINIO_DECODIFICA / VALORE_DOMINIO.', 'Sì: storico sì o no'),
    ('Media', 'Dizionari', 'Riconciliazione dei dizionari', 'la terna dominio, tabella e campo',
     'Il testo dice chiave = terna con il campo; la DDL di ANSC_CFG_DOMINIO_SIPO non ha più CAMPO_SIPO. La '
     'tabella descrittiva di RICONCILIAZ_DIZIONARI non ha ID_DOMINIO_SIPO, SCHEMA/TABELLA/CAMPO_SIPO, che '
     'sono nella DDL; DECODIFICA e ID_DOMINIO_SIPO sono doppioni; l’UK contiene una colonna nullabile.',
     '«La chiave è la coppia dominio e tabella; il campo sta sulla riga di riconciliazione»; allineare '
     'tabella e DDL tenendo una sola delle due chiavi.', 'No'),
    ('Bassa', 'Dizionari', 'Gestione dei dizionari SIPO', 'potrebbe esporre',
     'La vista V_ANSC_DIZ_VALIDO è descritta in tre modi (filtrata, non filtrata con fg_valido, '
     '«potrebbe»).', '«Espone la giunzione con fg_valido: chi traduce legge tutto, chi propone filtra '
     'fg_valido = \'S\'».', 'No'),

    # ── H. notifiche
    ('Media', 'Notifiche', 'La gestione delle notifiche: il processo ereditato da Side', 'STATO INFORMATIVO',
     'ANSC_102 nel corpus ha 1, 2, 3 e 10 INEFFICACE: il valore 4 «STATO INFORMATIVO» è di Side e non è più '
     'pubblicato. Nella tabella delle tre situazioni il genere «Presa visione» non è un valore di ANSC_101.',
     'Annotare «valore di Side non più pubblicato»; «2 Trascrizione (presa visione)».', 'No'),
    ('Media', 'Notifiche', 'La gestione delle notifiche (Side)', 'codice 5646',
     '5646 non è un codice ISTAT: è l’identificativo ANPR di Milano (ISTAT 015146). Per Roma '
     'l’identificativo ANPR è 8165 (ISTAT 058091).',
     '«… con l’identificativo ANPR del Comune (Milano 5646, Roma 8165)», come parametro di configurazione.', 'No'),
    ('Media', 'Notifiche', 'Flusso in ingresso · Notifiche (Side) · PC-10', 'apre il provvedimento di rifiuto',
     'Secondo Side il rifiuto di una notifica apre un provvedimento R016 (deposito vero); il capitolo sul '
     'flusso in ingresso e PC-10 lo trattano come R008 rifiuta con motivazione solo locale.',
     'Dichiarare la sequenza R008 rifiuta ↔ R016 in PC-10 e nella tabella delle operazioni, oppure '
     'motivare lo scostamento; aprire un OP.', 'Sì: si segue Side?'),
    ('Media', 'Notifiche', 'La gestione delle notifiche (Side)', 'notifica_stato_civile · una unità di deployment a sé',
     'Due store senza decisione: ANSC_NOTIFICA (DDL) non ha atto primario/collegato, formula, stato rifiuto, '
     'canale, comune destinatario, operatore — senza, gli scenari e le pagine di Side non si realizzano. '
     'L’«applicativo separato» si sovrappone al processo di automazione e al ricevitore notifiche '
     '(tre candidati per lo stesso compito); il conto delle unità di deployment non lo comprende. «Tre '
     'eredità» non è definito. OP-03 «Chiuso» ma il batch presuppone OP-23, aperto.',
     'Decidere quale tabella vale (tabella di corrispondenza colonna per colonna), che cosa assorbe '
     'l’unità separata (conferma e rifiuto restano in all-ansc-sipo, unico detentore delle credenziali); '
     'OP nuovo; OP-03 «chiuso sul contratto, subordinato a OP-23».', 'Sì: tabella e unità di deployment'),

    # ── I. back-office
    ('Media', 'Back-office', 'Back-office del componente ANSC', 'Apri in Finalizza',
     'Le azioni rinviano a una pagina «Finalizza» che non esiste; le categorie ignorano lo stato 11, lo '
     'stato 0 e le redazioni sospese (FLG_SOSPESO).',
     '«Riapri l’atto in SIPO alla pagina registrata (COD_PAGINA_RIPRESA)»; categorie «Dati modificati '
     'dopo la validazione» e «Redazioni sospese»; FIRMATO_CONFORMITA nelle righe di firma.', 'No'),
    ('Media', 'Back-office', 'Back-office del componente ANSC', 'Thymeleaf · cruscotto con indicatori · XREF',
     'Tecnologia Thymeleaf contro il front-end Angular di [R13]; «cruscotto KPI» contro «non è un cruscotto '
     'di monitoraggio»; «stato end-to-end con XREF», tabella eliminata (OP-25).',
     'Angular e libreria condivisa; togliere KPI; «da ANSC_STATO_ATTO e timeline dell’audit».', 'No'),
    ('Media', 'Back-office', 'Back-office del componente ANSC', 'Ricarica allegato (R001) · Riconcilia soggetto (R005)',
     'Il back-office dovrebbe fare solo letture, ma ha il caricamento R001 (dispositivo) e la '
     'riconciliazione del soggetto, che il processo mette nel dettaglio di SIPO.',
     'Spostare nel percorso SIPO; nel back-office sola consultazione.', 'No'),
    ('Media', 'Back-office', 'Back-office del componente ANSC', 'elenco delle schermate',
     'L’elenco è indietro rispetto al disegno v0.10: mancano Soggetti per UC, Identificativi dei soggetti, '
     'comunicazione anagrafica per UC, i dizionari SIPO di Side, le due pagine della numerazione; il menu '
     'omette Notifiche, Numeri comunali, Documenti, Importazione, Sistema; ruoli USC e Supporto mancanti. '
     '«atti formati durante un fermo ANSC» contraddice «in emergenza si prepara, non si forma».',
     'Ridurre il capitolo a sintesi con rimando a DISEGNO_Back-Office v0.10 (due elenchi paralleli '
     'divergeranno sempre); «atti preparati in emergenza da far rientrare».', 'Sì: sintesi + rimando?'),

    # ── J. funzioni ANSC, schede, OP
    ('Media', 'Servizi ANSC', 'Le funzioni offerte da ANSC · Schede', 'Non impiegata nel pilota · Eventuale',
     'R012 (firma elettronica dei dichiaranti) e R014 (comunicazione anagrafica) sono nel processo ma le '
     'schede li danno fuori uso; il conto «servizi impiegati 11 su 25» sale ad almeno 13. La prenotazione '
     '«riserva identificativi» in tre punti contro «non riserva numeri ma crea atti».',
     '«Uso nel disegno = Sì»; ricontare; «crea in anticipo N atti in bozza».', 'No'),
    ('Media', 'Open Point', 'Registro degli Open Point', 'OP-01 · OP-04 · OP-08 · OP-14 · OP-23 · OP-29 · OP-60 · OP-71 · OP-75',
     'OP-01 aperto ma la firma USC è chiusa e le firme dei dichiaranti sono nel processo; OP-04 e OP-08 '
     '(ordinamento invii) residui dell’impianto asincrono; OP-14 e OP-23 rinviano a capitoli che non '
     'esistono; OP-29 e OP-60 in parte decisi dall’Anteprima («il numero comunale dovrà essere salvato '
     'nell’atto sulle tabelle SIPO»); OP-71 usa la vecchia nozione di testo libero; OP-75 (d): la FK di '
     'firmatari va verso ANSC_STATO_ATTO.',
     'Riformulare o chiudere ciascuno; dividere il registro in aperti e chiusi (chiusi in coda).', 'No'),
    ('Media', 'API', 'Appendice B', 'depositaBozza · firmaAtto · /configurazione/operazioni',
     'Corrispondenze superate (depositaBozza = R005+R009; R012 «fuori perimetro»; mancano R010, '
     'attestazione R007, R014, R005 dei soggetti); mancano le operazioni per anteprima, conformità, '
     'ripresa dell’evento, conferma/rifiuto notifiche, prenotazione del parto plurimo; la configurazione '
     'è ancora per «operazioni» e non ha sezioni, logiche, allegati/soggetti per UC, riconciliazione. Le '
     'ricerche sui dizionari sono attribuite a R901 ma leggono la replica locale.',
     'Aggiornare i .yaml e rigenerare SPEC e tabella (non a mano); intanto un OP dedicato.', 'No'),
    ('Bassa', 'Numeri', 'Più capitoli', 'Due esiti su tre · la penultima · quattro numeri di versione · 219 righe · Il rapporto fra le ultime due righe',
     'Conteggi interni sbagliati: gli esiti della determinazione sono quattro e uno solo non dà UC; la '
     'riga su R901 è la terza, non la penultima; le versioni pubblicate sono cinque righe; Morte_001 ha '
     '218 righe; «le ultime due righe» punta alle righe sbagliate; il modello evento pesa «8-30» in un '
     'punto e «10-30» in un altro.', 'Correggere.', 'No'),
    ('Bassa', 'Impatti', 'Impatti sul FE / sul Database', 'ATTO.ATTO_NUMERO_ANSC · sezione «Documenti»',
     'Impatti sul FE: colonna inesistente, «Documenti» invece di «Allegati» (scelta di Side), mancano le '
     'pagine nuove del processo; limitato a decessi-web ma generale. Impatti sul Database: mancano '
     'ALLEGATO in MATR_USR e l’UPDATE di colonna su ANAG_USR.SOGGETTO; «Sesso del dichiarante» è '
     'dell’incaricato dell’agenzia.', 'Riallineare al processo.', 'No'),
]


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Rilievi'
    testa = ['N.', 'Gravità', 'Area', 'Capitolo', 'Dove (testo da cercare nel .docx)',
             'Che cosa non torna', 'Correzione proposta', 'Serve una tua decisione?', 'Stato', 'Note']
    larg = [5, 9, 15, 30, 38, 70, 70, 26, 13, 30]
    blu = PatternFill('solid', fgColor='1F3A5F')
    fill = {'Alta': 'F6DFE1', 'Media': 'FDF1D6', 'Bassa': 'E9EAEC'}
    sottile = Side(style='thin', color='CBD5E1')
    bordo = Border(left=sottile, right=sottile, top=sottile, bottom=sottile)
    ws.append(testa)
    for c, w in zip(ws[1], larg):
        c.font = Font(bold=True, color='FFFFFF', name='Arial', size=10)
        c.fill = blu
        c.alignment = Alignment(vertical='center', wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    ordine = {'Alta': 0, 'Media': 1, 'Bassa': 2}
    righe = sorted(R, key=lambda r: ordine[r[0]])
    for i, (g, area, cap, dove, problema, corr, dec) in enumerate(righe, 1):
        ws.append([i, g, area, cap, dove, problema, corr, dec, 'Da fare', ''])
        for c in ws[i + 1]:
            c.alignment = Alignment(vertical='top', wrap_text=True)
            c.font = Font(name='Arial', size=9, bold=(c.column == 2))
            c.border = bordo
        ws.cell(i + 1, 2).fill = PatternFill('solid', fgColor=fill[g])
        if dec != 'No':
            ws.cell(i + 1, 8).fill = PatternFill('solid', fgColor='DBE6F5')
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:J{len(righe) + 1}'
    dv = DataValidation(type='list', formula1='"Da fare,Fatto,Scartato,In discussione"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f'I2:I{len(righe) + 1}')

    lg = wb.create_sheet('Legenda')
    lg.column_dimensions['A'].width = 34
    lg.column_dimensions['B'].width = 12
    lg.append(['Rilettura di ANALISI_Integrazione-ANSC_v3.44 (versione rivista a mano, 22/10/2026)'])
    lg['A1'].font = Font(bold=True, name='Arial', size=11)
    lg.append([])
    lg.append(['Gravità', 'Rilievi'])
    for g in ('Alta', 'Media', 'Bassa'):
        lg.append([g, sum(1 for r in R if r[0] == g)])
    lg.append(['Totale', len(R)])
    lg.append(['Con decisione richiesta', sum(1 for r in R if r[6] != 'No')])
    lg.append([])
    lg.append(['Controllo automatico verifica-conteggi.py: nessuna discordanza nei numeri dichiarati '
               '(i rilievi qui sono di coerenza redazionale, che lo script non copre).'])
    wb.save(OUT)
    print('scritto:', OUT, len(R), 'rilievi')


if __name__ == '__main__':
    main()
