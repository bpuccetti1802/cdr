# -*- coding: utf-8 -*-
"""v0.3 di «PROPOSTA_Osservabilita-OpenTelemetry»: guida all'uso, catalogo degli errori,
arricchimento degli eventi, percorso dei dati nella transizione.

Si parte dal FILE REALE della v0.2: l'utente vi ha scritto le risposte a OT-01 (Oracle 12),
OT-02 (nel cluster non c'è nulla), OT-05 (la telemetria del browser non esce) e OT-07 (i 28
logBack.xml restano come sono). Non rieseguire `genera_otel.py` né `otel_v0_2_api.py`.

Che cosa fa:
  * correzioni di coerenza: OT-10…OT-12 annunciati e assenti dalla tabella, «Sette questioni»,
    OT-05 con due significati (il secondo diventa OT-13), rimando a un titolo inesistente,
    «undici unità»;
  * recepisce le quattro risposte (Oracle 12 → TS_EVENTO in UTC senza fuso, perché la chiave
    di un partizionamento per intervallo non ammette TIMESTAMP WITH TIME ZONE; OT-07 → la
    libreria aggancia il proprio appender da programma);
  * capitoli nuovi «Guida all’uso» e «Il catalogo dei codici di errore»;
  * sezione sull'arricchimento degli eventi nel capitolo delle interfacce;
  * sezione sul percorso dei dati nella transizione, con figura (`diagrammi_otel.py`) e la
    tabella degli span ANSC_LOG_SPAN, che mancava: `leggiTraccia` restituiva span che nessuna
    tabella conservava.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/otel_v0_3.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D          # noqa: E402
from otel_v0_2_api import par, h, voce, tabella, codice   # noqa: E402
import diagrammi_otel           # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.2.docx')
OUT = os.path.join(BASE, 'Documenti finali', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.3.docx')
DATA = '10/11/2026'


# =========================================================== 1. correzioni di coerenza
def correzioni(doc, fatti):
    S = lambda v, n, a, e: D.sostituisci(doc, v, n, attese=a, etichetta=e, fatti=fatti)  # noqa

    S('Un esempio: undici unità e un servizio di terzi',
      'Un esempio: dieci processi, due famiglie di front-end e i servizi nazionali', 1,
      'titolo «undici unità»')
    S('Con undici unità e più gruppi di lavoro', 'Con una decina di processi e più gruppi '
      'di lavoro', 1, '«undici unità» nella libreria')
    S('cap. «Perché serve con i microservizi»',
      'cap. «Perché serve in un’architettura a microservizi»', 1, 'rimando per titolo')
    S('Il registro diagnostico, se la destinazione è Oracle', 'Il registro diagnostico su '
      'Oracle', 1, 'titolo: la destinazione è decisa')

    # Oracle 12: la chiave del partizionamento per intervallo non può avere il fuso
    S('  TS_EVENTO        TIMESTAMP(6) WITH TIME ZONE NOT NULL,',
      '  TS_EVENTO        TIMESTAMP(6)      NOT NULL,   -- in UTC', 1, 'DDL: TS_EVENTO')
    S("VALUES LESS THAN (TIMESTAMP '2027-01-01 00:00:00 +00:00'))",
      "VALUES LESS THAN (TIMESTAMP '2027-01-01 00:00:00'))", 1, 'DDL: partizione iniziale')
    S(" WHERE TS_EVENTO > SYSTIMESTAMP - INTERVAL '6' HOUR",
      " WHERE TS_EVENTO > SYS_EXTRACT_UTC(SYSTIMESTAMP) - INTERVAL '6' HOUR", 1,
      'interrogazione in UTC')

    S('Una condizione: la via Oracle va dimensionata prima, non dopo. La scelta dipende anche '
      'da OT-01, la versione in esercizio.',
      'Una condizione: la via Oracle va dimensionata prima, non dopo. OT-01 ha risposto — la '
      'base dati in esercizio è Oracle 12 — e le conseguenze sono raccolte più avanti, nella '
      'sezione «Nella transizione: dove vanno i dati e chi li gestisce».', 1, 'OT-01 recepito')

    S('Da aggiungere nei logBack.xml. Nei 28 moduli che non dichiarano logging.config la '
      'modifica non avrebbe effetto: vedi OT-07.',
      'Da aggiungere nei logBack.xml dei moduli che li caricano. Nei 28 moduli che non '
      'dichiarano logging.config il file resta com’è (OT-07): per questo la libreria aggancia '
      'il proprio canale verso il collector da programma, all’avvio, e non dal logBack.xml. In '
      'quei moduli gli eventi arrivano comunque al collector; la riga su standard output resta '
      'quella di oggi, senza identificativi.', 1, 'OT-07 recepito (innesto)')

    S('si ripuliscono i difetti rilevati, fra cui il percorso Windows e il gestore delle '
      'connessioni a TRACE.',
      'si correggono le due impostazioni di application.properties rilevate — il percorso '
      'Windows e il gestore delle connessioni a TRACE — che hanno effetto in tutti i moduli; i '
      'logBack.xml non caricati restano come sono (OT-07).', 1, 'OT-07 recepito (gradino)')
    S('ANSC_LOG_EVENTO, lo scarico dal collector e le due pagine.',
      'ANSC_LOG_EVENTO e ANSC_LOG_SPAN, be-osservabilita come scarico del collector, il '
      'catalogo dei codici e le due pagine.', 1, 'terzo gradino')

    S('il livello di dettaglio visibile è OT-05, perché gli attributi possono contenere '
      'riferimenti a persone.',
      'quali attributi mostrare a quale ruolo è OT-13, perché gli attributi possono contenere '
      'riferimenti a persone. Le pagine leggono anche ANSC_LOG_SPAN per la cascata e il '
      'catalogo ANSC_CFG_CODICE_EVENTO per la colonna «Che cosa fare».', 1, 'OT-05 → OT-13')

    S('"SOGGETTO-NON-TROVATO"', '"BE-SOGG-NON-TROVATO"', 1, 'codice evento conforme')
    S('// oscurato: RSSMRA****",', '// oscurato: RSSMRA**********', 1,
      'refuso nell’esempio 5')

    S('Figura 2 — Errori e diagnostica', 'Figura 3 — Errori e diagnostica', 1,
      'rinumerazione figura')

    S('Sette questioni. La prima decide il capitolo sull’archiviazione e va chiusa per prima; '
      'le altre non impediscono di cominciare dal primo gradino.',
      'Quindici questioni. Quattro hanno già una risposta (OT-01, OT-02, OT-05, OT-07), '
      'riportata in tabella e recepita nel testo. Le altre non impediscono di cominciare dal '
      'primo gradino.', 1, 'introduzione ai punti aperti')


# =========================================================== 2. arricchimento (interfacce)
ARRICCHIMENTO = [
    ['Dato', 'Attributo', 'Chi lo valorizza', 'Da dove viene'],
    ['Momento', '`ts_evento`', 'Libreria', 'Orologio del processo, in UTC, al microsecondo.'],
    ['Traccia e passo', '`trace_id`, `span_id`', 'Libreria',
     'Il contesto della richiesta: `traceparent` in ingresso, oppure creato dal filtro.'],
    ['Componente e versione', '`service.name`, `service.version`', 'Libreria',
     'Variabili `OTEL_*` del pod e versione del rilascio. **Mai scritte nel codice.**'],
    ['Ambiente', '`deployment.environment`', 'Libreria', 'Configurazione del pod.'],
    ['Istanza', '`k8s.pod.name`, `k8s.namespace.name`', 'Collector',
     'Dal cluster. Distinguono due repliche dello stesso servizio.'],
    ['Punto del codice', 'logger (classe), thread', 'Libreria',
     'Dal logger. Metodo e riga **non** si ricavano in produzione: costano, e il codice '
     'evento li rende superflui.'],
    ['Chi opera', '`utente`, `cod_postazione`', 'Libreria',
     'Dal gettone o dalla sessione; la postazione dalla sessione del concentratore. Nei '
     'processi schedulati `utente` vale il nome del processo.'],
    ['Chiamate HTTP', 'metodo, percorso, stato, durata', 'Strumentazione',
     'Filtri e client strumentati. **Il corpo mai.**'],
    ['Interrogazioni', 'tipo di base dati, operazione, durata', 'Strumentazione (OT-06)',
     'Il testo dell’interrogazione solo con i parametri sostituiti da segnaposto.'],
    ['Identificativi verso i servizi nazionali', '`id_operazione_comune`, '
     '`id_operazione_ansc` / `id_operazione_anpr`', 'Libreria',
     'Il client ANSC della libreria li scrive da sé a ogni chiamata. Per ANPR secondo OT-09.'],
    ['Livello', '—', 'Sviluppatore, con un predefinito',
     '`ERROR` se l’evento ha un’origine di errore, `INFO` altrimenti.'],
    ['Origine e codice', '`cod_origine`, `cod_evento`', '**Sviluppatore, obbligatori**',
     'Dal catalogo dei codici.'],
    ['Messaggio', '`messaggio`', 'Sviluppatore',
     'Una frase breve: che cosa, su quale oggetto, con quale esito.'],
    ['Oggetto lavorato', 'identificativi dei tre piani',
     '**Sviluppatore ne fornisce uno, la libreria completa gli altri**',
     'Si imposta una volta per richiesta con `Registro.corrente().atto(…)`.'],
    ['Dati del dominio', '`cod_uc`, `cod_servizio_ansc`, `campo`…', 'Sviluppatore',
     'Dal vocabolario chiuso della tabella seguente.'],
    ['Eccezione', 'tipo, messaggio, pila, causa radice', 'Libreria, se lo sviluppatore la passa',
     'Con `.errore(e)`, oppure come ultimo argomento del logger.'],
]

VOCABOLARIO = [
    ['Attributo', 'Quando si scrive', 'Esempio'],
    ['`cod_uc`', 'L’evento riguarda un caso d’uso già determinato.', '`11111000`'],
    ['`cod_servizio_ansc`', 'L’evento accompagna una chiamata ad ANSC.', '`R009`'],
    ['`cod_stato_ansc`', 'Dopo una lettura o un deposito: lo stato ANSC_11 dell’atto.', '`5`'],
    ['`cod_fase`', 'L’evento accompagna una chiamata registrata nell’audit: il valore di FASE.',
     ''],
    ['`id_versione_cfg`', 'La decisione dipende dalla configurazione: la baseline usata.', '`12`'],
    ['`campo`', 'Errore su un dato: il percorso nel modello evento, mai il valore.',
     '`evento.datiEventoMatrimonio.numeroTestimoni`'],
    ['`stato_http`', 'Errore di una chiamata.', '`502`'],
    ['`num_tentativo`', 'Ritentativi.', '`2`'],
    ['`nome_job`', 'Processi schedulati.', ''],
]


def arricchimento(doc, prima, modello):
    tab = lambda r, w: tabella(doc, prima, r, modello, w)  # noqa: E731
    h(doc, prima, 2, 'Con che cosa si arricchisce un evento')
    par(doc, prima,
        'Un evento vale per gli attributi che porta. La regola è semplice: **ciò che si può '
        'ricavare dal contesto lo ricava la libreria**, sempre e allo stesso modo; **ciò che '
        'solo il programma sa lo scrive lo sviluppatore**, con nomi presi da un vocabolario '
        'chiuso; alcune cose non si scrivono mai.')
    tab(ARRICCHIMENTO, [1.2, 1.6, 1.3, 2.3])
    par(doc, prima,
        '**Il contesto di dominio si imposta una volta per richiesta.** Il punto in cui il '
        'programma conosce l’oggetto lavorato è quasi sempre l’ingresso dell’operazione — il '
        'controller che riceve `idAtto` nel percorso. Impostato lì, gli identificativi '
        'accompagnano **tutte** le righe della richiesta, comprese le `log.info(…)` già '
        'esistenti, senza ripeterli a ogni evento. Serve un’aggiunta all’interfaccia del '
        'contesto:')
    codice(doc, prima, [
        'public interface Contesto {',
        '    String  traceId();                       // 32 cifre esadecimali',
        '    String  traceIdCompatto();               // 25 caratteri, per ANPR',
        '    Contesto atto(Long idAttoSipo);          // piano 1, vale fino a fine richiesta',
        '    Contesto allegato(Long idAllegato);      // piano 2',
        '    Contesto soggetto(Long idSoggettoSipo);  // piano 3',
        '}',
        '',
        '@PostMapping("/ansc/v1/atti/{idAtto}/deposito")',
        'public EsitoDeposito deposita(@PathVariable Long idAtto) {',
        '    Registro.corrente().atto(idAtto);        // da qui ogni riga porta l\'atto',
        '    return deposito.deposita(idAtto);',
        '}',
    ], 'Il contesto di dominio impostato all’ingresso dell’operazione.')
    par(doc, prima,
        '**Gli attributi di dominio hanno un vocabolario chiuso.** Nomi in minuscolo con il '
        'trattino basso, come le colonne; un attributo nuovo si aggiunge come costante della '
        'libreria, non scrivendone il nome a mano nel codice applicativo. È ciò che impedisce '
        'di trovare lo stesso dato sotto tre nomi.')
    tab(VOCABOLARIO, [1.5, 3.1, 1.8])
    par(doc, prima,
        '**Che cosa non si scrive mai**, nemmeno come attributo: codice fiscale, nomi, '
        'indirizzi, contatti, dati sanitari, il contenuto degli allegati e il testo dell’atto, '
        'i payload verso ANSC e ANPR, il codice di sessione, gettoni, password e chiavi. Dove un '
        'riferimento alla persona serve davvero, si usa `.riservato(…)`, che ne conserva una '
        'forma parziale. Il collector cancella comunque le chiavi vietate: è una seconda '
        'barriera, non la prima.')


# =========================================================== 3. guida all'uso
PUNTI_OBBLIGATI = [
    ['Punto del codice', 'Che cosa si registra', 'Livello', 'Forma'],
    ['Ingresso di un’operazione REST', 'Apertura del contesto e oggetto lavorato. Non i '
     'parametri.', '—', 'Filtro automatico + `Registro.corrente().atto(…)`'],
    ['Decisione di dominio (scelta dell’UC, di un ramo, di una regola)',
     'Quale scelta e in base a che cosa, con identificativi e non dati.', '`DEBUG`',
     '`log.debug(…)`'],
    ['Cambio di stato dell’atto', 'Stato di partenza e di arrivo.', '`INFO`',
     'Evento classificato'],
    ['Chiamata a un altro servizio (ANSC, ANPR, numeratore, interni)', 'Durata ed esito.',
     'automatico', 'Client strumentato; un passo se fa parte di un’operazione composta'],
    ['Risposta negativa di un servizio esterno', 'Codice remoto e identificativo '
     'dell’operazione.', '`WARN` se si prosegue, `ERROR` se l’operazione fallisce',
     'Evento con origine `ANSC` o `ANPR`'],
    ['Esito indeterminato (tempo scaduto, risposta assente)', 'Che cosa si sa, che cosa no, '
     'e l’avvio della riconciliazione.', '`ERROR`', 'Evento classificato'],
    ['Ritentativo', 'Il numero del tentativo.', '`WARN` se riesce dopo il primo, `ERROR` '
     'all’ultimo fallito', 'Evento con `num_tentativo`'],
    ['Eccezione gestita', 'L’eccezione con la sua causa.', 'Secondo l’effetto sull’utente',
     'Evento con `.errore(e)`'],
    ['Gestore globale delle eccezioni', 'L’eccezione non prevista.', '`ERROR`',
     'Evento `BE-INATTESO`, una volta sola'],
    ['Avvio del componente', 'Versione e configurazione caricata, senza i segreti.',
     '`INFO`; `FATAL` se manca un requisito', 'Evento classificato'],
    ['Processo schedulato', 'Inizio, conteggi, fine.', '`INFO`; `ERROR` sul fallimento',
     'Un passo intorno all’esecuzione'],
    ['Ciclo su molti elementi', 'Un riepilogo alla fine; gli scarti uno per uno.',
     '`INFO` il riepilogo, `WARN` lo scarto', '`log` semplice'],
]

SBAGLIATO_GIUSTO = [
    ['Così no', 'Così sì', 'Perché'],
    ['`log.error("errore")`', '`registro.evento(Origine.BE, "BE-PAYLOAD-KO")'
     '.messaggio("Costruzione del payload non riuscita").errore(e).registra()`',
     'Il messaggio dice dove, il codice che cosa, l’eccezione perché.'],
    ['`catch (Exception e) { }`', 'Un evento, oppure il rilancio con la causa.',
     'Il catch vuoto è il difetto più costoso da diagnosticare: non lascia traccia.'],
    ['`log.error("Errore: " + e.getMessage())`', '`log.error("Deposito non riuscito", e)`',
     'Concatenando si perdono la pila e la causa radice.'],
    ['`log.error(…); throw new XException(e);`', '`throw new XException("contesto", e);` — '
     'registra chi la gestisce.', 'Due righe di errore per un solo fatto falsano i conteggi.'],
    ['`log.info("CF: " + cf)`', '`.riservato("codice_fiscale", cf)`', 'Dato personale.'],
    ['`log.info("payload: {}", json)`', 'Niente: il payload è nell’audit.',
     'Volume e dati personali.'],
    ['`log.info(…)` dentro un ciclo di diecimila righe', 'Contatori e un riepilogo alla fine.',
     'Il volume nasconde ciò che conta.'],
    ['`log.debug(String.format(…))`', '`log.debug("UC {} scelto", uc)`',
     'Il costo della formattazione si paga anche quando il livello è spento.'],
    ['`new Thread(…)` o un esecutore qualsiasi', 'L’esecutore fornito dalla libreria.',
     'Il contesto non passa al thread nuovo e la traccia si spezza.'],
    ['`registro.passo("deposito-" + idAtto)`', '`registro.passo("deposito-R009")` con '
     'l’atto nel contesto', 'Un nome per atto rende inutilizzabili i conteggi per passo.'],
]

LIVELLI_DOMANDE = [
    ['Domanda da farsi', 'Livello'],
    ['Il componente non è in grado di servire nessuno?', '`FATAL`'],
    ['L’utente non ha ottenuto ciò che chiedeva?', '`ERROR`'],
    ['L’ha ottenuto, ma è servito un ripiego o qualcosa è anomalo?', '`WARN`'],
    ['È un fatto di dominio che qualcuno vorrà ritrovare fra un mese?', '`INFO`'],
    ['Serve a capire una decisione del programma?', '`DEBUG`'],
    ['Serve solo mentre si cerca un difetto preciso?', '`TRACE`'],
]

PROPAGAZIONE = [
    ['Situazione', 'Che cosa fare'],
    ['Thread, metodi `@Async`, esecutori', 'Usare l’esecutore fornito dalla libreria, che porta '
     'con sé il contesto. Mai crearne uno a mano.'],
    ['Processo schedulato', 'La traccia nasce all’inizio dell’esecuzione: un passo radice con '
     'il nome del processo, e `utente` uguale al nome del processo.'],
    ['Chiamate REST fra i nostri servizi', 'Automatico con i client strumentati. Con un client '
     'scritto a mano si aggiunge `traceparent` dal contesto corrente.'],
    ['Chiamate verso ANSC e ANPR', '**Non si propaga `traceparent`**: sono terzi. Si usa '
     '`idOperazioneComune`, che il client della libreria deriva dalla traccia.'],
    ['Client SOAP del modulo `anpr-client`', 'L’XML è costruito a mano: la libreria offre un '
     'intercettore per durata ed esito; `idOperazioneComune` secondo OT-09.'],
    ['Dal front-end Thymeleaf al back-end', 'Il filtro di CommonWeb apre il contesto; il '
     'client REST comune (`RestClient`) aggiunge `traceparent` alle chiamate.'],
    ['Dal browser Angular', 'Strumentazione delle chiamate limitata ai nostri domini.'],
]


def guida(doc, prima, modello):
    tab = lambda r, w: tabella(doc, prima, r, modello, w)  # noqa: E731
    h(doc, prima, 1, 'Guida all’uso: come si scrivono log e tracce nel codice')
    par(doc, prima,
        'Questo capitolo è per chi scrive il codice. Le interfacce dicono **che cosa** offre '
        'la libreria; qui si dice **come** usarla dentro le classi e i metodi, perché un '
        'difetto si ritrovi in pochi minuti partendo da ciò che l’operatore ha in mano — il '
        'numero comunale, l’ora, il messaggio a video. Le regole valgono per i back-end nuovi '
        'e per il codice nuovo dei back-end esistenti; il codice esistente non si riscrive, '
        'riceve il contesto da sé.')

    h(doc, prima, 2, 'Le dieci regole')
    for testa, corpo in [
        ('1. Un evento risponde a tre domande.', 'Che cosa è successo, a quale oggetto, con '
         'quale esito. Se ne manca una, l’evento non serve a chi lo leggerà.'),
        ('2. Si registra dove si decide, non dove si passa.', 'I punti obbligati sono nella '
         'tabella seguente; altrove si registra solo ciò che aiuta a capire una decisione.'),
        ('3. Un errore si registra una volta sola, dove viene gestito.', 'Chi rilancia non '
         'registra; chi registra non rilancia. Il gestore globale registra ciò che nessuno ha '
         'gestito.'),
        ('4. Nessun catch vuoto.', 'Se un’eccezione si ignora di proposito, lo si dichiara '
         'con una riga a DEBUG che dice perché.'),
        ('5. L’origine si classifica dove l’errore si riconosce.', 'Chi riceve un rifiuto di '
         'ANSC lo classifica ANSC, anche se il codice che lo cattura è nostro.'),
        ('6. Il codice evento viene dal catalogo.', 'Non si inventa sul momento: si aggiunge '
         'prima al catalogo, poi alla libreria.'),
        ('7. Parametri con i segnaposto, eccezione in fondo.', '`log.warn("UC {} non attivo", '
         'uc, e)`: niente concatenazioni, niente `e.getMessage()` al posto di `e`.'),
        ('8. Niente dati personali e niente segreti.', 'Si registra che un dato era assente o '
         'malformato, non quale fosse.'),
        ('9. INFO è per i fatti di dominio.', 'Il dettaglio va a DEBUG, che in produzione è '
         'spento.'),
        ('10. Il contesto si apre una volta e si propaga sempre.', 'Anche nei thread, nei '
         'processi schedulati e verso gli altri servizi.'),
    ]:
        voce(doc, prima, testa, corpo)

    h(doc, prima, 2, 'I punti obbligati di una classe')
    par(doc, prima,
        'Ogni componente ha gli stessi punti in cui un evento è dovuto. Fuori da questi si '
        'registra solo se aiuta a capire una scelta del programma.')
    tab(PUNTI_OBBLIGATI, [1.7, 1.9, 1.3, 1.6])

    h(doc, prima, 2, 'Dentro un metodo')
    par(doc, prima,
        '**Non si registrano l’ingresso e l’uscita di ogni metodo.** Lo fa già la traccia, '
        'con le durate, nei punti in cui serve. Righe come «entro in calcolaPayload» '
        'moltiplicano il volume senza aggiungere nulla. Si registrano invece le **decisioni** '
        '(quale ramo, quale caso d’uso, perché) e gli **esiti** che cambiano qualcosa.')
    par(doc, prima,
        'L’esempio che segue è un servizio di deposito scritto secondo le regole. Si notino '
        'tre cose: il contesto dell’atto impostato una volta; i due passi che misurano le '
        'parti lente; e i due rami d’errore, che non sono uguali. Un rifiuto di ANSC è un '
        'esito noto e si gestisce lì; un esito ignoto porta alla riconciliazione, **mai** a '
        'un secondo deposito cieco.')
    codice(doc, prima, [
        '@Service',
        'public class DepositoService {',
        '',
        '    private static final Logger log = LoggerFactory.getLogger(DepositoService.class);',
        '',
        '    public EsitoDeposito deposita(Long idAttoSipo) {',
        '        Registro.corrente().atto(idAttoSipo);          // vale per tutta la richiesta',
        '',
        '        var atto = store.leggi(idAttoSipo);',
        '        var uc   = determinazione.ucDi(atto);',
        '        log.debug("UC {} determinato con priorita\' {}", uc.codice(), uc.priorita());',
        '',
        '        ModelEvento payload;',
        '        try (var passo = registro.passo("costruzione-payload")) {',
        '            passo.attributo("cod_uc", uc.codice());',
        '            payload = costruttore.costruisci(atto, uc);',
        '        }',
        '',
        '        try (var passo = registro.passo("deposito-R009")) {',
        '            var risposta = ansc.valida(payload);       // idOperazioneComune = traccia',
        '            store.registraDeposito(idAttoSipo, risposta.idAnsc());',
        '            registro.evento(Origine.BE, "BE-ATTO-DEPOSITATO")',
        '                    .livello(Livello.INFO)',
        '                    .messaggio("Atto depositato in ANSC")',
        '                    .attributo("cod_uc", uc.codice())',
        '                    .registra();',
        '            return EsitoDeposito.ok(risposta.idAnsc());',
        '',
        '        } catch (AnscRifiutoException e) {             // ANSC ha risposto di no',
        '            registro.evento(Origine.ANSC, "ANSC-" + e.codiceErrore())',
        '                    .messaggio("Deposito rifiutato da ANSC")',
        '                    .attributo("cod_uc", uc.codice())',
        '                    .attributo("campo", e.campo())',
        '                    .errore(e)',
        '                    .registra();',
        '            return EsitoDeposito.rifiutato(e.errori()); // gestito qui: non si rilancia',
        '',
        '        } catch (AnscEsitoIgnotoException e) {         // partito, risposta assente',
        '            registro.evento(Origine.INFRA, "INFRA-ANSC-ESITO-IGNOTO")',
        '                    .messaggio("Esito del deposito non noto: avviata la riconciliazione")',
        '                    .errore(e)',
        '                    .registra();',
        '            riconciliazione.avvia(idAttoSipo);         // R005, mai un nuovo R009 cieco',
        '            return EsitoDeposito.daVerificare();',
        '        }',
        '    }',
        '}',
    ], 'Un metodo scritto secondo la guida: contesto, passi, due rami d’errore distinti.')
    par(doc, prima, 'Gli errori che si vedono più spesso, e la forma corretta:')
    tab(SBAGLIATO_GIUSTO, [2.0, 2.4, 2.0])

    h(doc, prima, 2, 'Scegliere il livello')
    par(doc, prima,
        'Il livello dichiara chi deve guardare l’evento e quando. In pratica basta rispondere '
        'alle domande della tabella, nell’ordine: la prima risposta affermativa dà il livello.')
    tab(LIVELLI_DOMANDE, [5.0, 1.4])
    par(doc, prima,
        'In produzione il livello di partenza è INFO per tutti i componenti. DEBUG si accende '
        'per un componente, per un tempo dichiarato, su richiesta del secondo livello di '
        'supporto: se si voglia poterlo fare senza rilasciare è OT-11.')

    h(doc, prima, 2, 'Le tracce: quando aprire un passo')
    voce(doc, prima, 'Le chiamate sono già passi.', 'Le chiamate HTTP e, con l’agente, quelle '
         'alla base dati sono strumentate da sé: non si avvolgono a mano.')
    voce(doc, prima, 'Si apre un passo intorno a:', 'un’operazione di dominio fatta di più '
         'chiamate (deposito, firma, stacco del numero); un calcolo che può durare (costruzione '
         'del payload, determinazione dell’UC); l’esecuzione di un processo schedulato.')
    voce(doc, prima, 'Non si apre un passo intorno a:', 'metodi semplici, accessi a campi, '
         'ciascun elemento di un ciclo.')
    voce(doc, prima, 'Il nome del passo è stabile.', 'Minuscolo con il trattino, senza '
         'identificativi dentro: `deposito-R009`, non `deposito-1842`. Gli identificativi '
         'stanno negli attributi e nel contesto.')
    voce(doc, prima, 'L’esito si chiude da sé.', 'Un’eccezione che esce dal blocco segna il '
         'passo come fallito; altrimenti `passo.esito(…)` lo dichiara.')

    h(doc, prima, 2, 'Propagare il contesto dove non è automatico')
    tab(PROPAGAZIONE, [2.0, 4.4])

    h(doc, prima, 2, 'Il codice evento: come si costruisce')
    par(doc, prima,
        'Il codice ha la forma `ORIGINE-AREA-FATTO`, in maiuscolo con il trattino, al massimo '
        'quaranta caratteri: `BE-ATTO-DEPOSITATO`, `INFRA-OTP-SCAD`, `CONF-UC-AMBIGUO`. Il '
        'prefisso è uno dei sette valori dell’origine, così il codice da solo dice a chi '
        'compete. Le aree in uso sono poche e si estendono solo se serve: ATTO, ALLEG, SOGG, '
        'NUM, CFG, DIZ, NOTIF, OTP, FIRMA, HTTP, AVVIO, JOB.')
    par(doc, prima,
        'Per i rifiuti dei servizi nazionali il codice riporta quello del servizio: '
        '`ANSC-400001`, `ANSC-406002`; per ANPR `ANPR-` seguito dal codice restituito. In questo '
        'modo il catalogo ANSC si importa com’è, e chi parla con Sogei cita lo stesso numero.')

    h(doc, prima, 2, 'Prima di consegnare: le verifiche')
    for testa, corpo in [
        ('Ogni catch registra o rilancia.', 'Un controllo statico nella build segnala i catch '
         'vuoti.'),
        ('Ogni codice evento usato è nel catalogo.', 'Un test confronta le costanti della '
         'libreria con il catalogo esportato e fallisce se ne manca uno.'),
        ('Nessun dato personale nelle righe.', 'Un test cerca negli eventi prodotti in collaudo '
         'le forme di un codice fiscale e di un indirizzo di posta.'),
        ('Nomi dei passi stabili.', 'Nessun identificativo dentro il nome.'),
        ('La prova che conta.', 'Si provoca l’errore in collaudo e lo si ritrova dal back-office '
         'partendo dal numero comunale. Se non ci si arriva in pochi passaggi, manca qualcosa.'),
    ]:
        voce(doc, prima, testa, corpo)


# =========================================================== 4. catalogo
INTESTAZIONE_CAT = ['Codice', 'Liv.', 'Quando si presenta', 'Che cosa fa il primo livello',
                    'Se non basta']

CATALOGO = [
    ('Sessione e firma', [
        ['`INFRA-OTP-ASSENTE`', 'ERROR', 'L’operazione richiede ANSC e la postazione non ha un '
         'codice di sessione valido (contratto: `SESSIONE_OTP_ASSENTE`).',
         'Far generare un codice sulla web app OTP di ANSC, consegnarlo da SIPO, ripetere. Non '
         'è un difetto.', 'Sistemisti, se si ripete con un codice appena generato.'],
        ['`ANSC-406001`', 'ERROR', 'ANSC non accetta il codice di sessione.',
         'Verificare che il codice sia dell’ufficiale autenticato e della stessa postazione; '
         'rigenerarlo.', 'Presidio ANSC / Sogei, se persiste con un codice nuovo.'],
        ['`ANSC-406002`', 'ERROR', 'Codice di sessione scaduto (quattro ore, oppure '
         'invalidato).', 'Rigenerarlo. Se l’atto era a metà di una sequenza, leggerne lo stato '
         'dal back-office prima di ripetere.', '—'],
        ['`INFRA-OTP-SCAD`', 'WARN', 'Codice rigenerato a metà di una sequenza.',
         'Nessuna azione sul singolo caso.', 'Architettura, se è frequente: la soglia di '
         'guardia è troppo bassa.'],
        ['`ANSC-406004`', 'ERROR', 'Firma non avvenuta.', 'Verificare le credenziali di firma '
         'remota dell’ufficiale e ripetere. Lo stato dell’atto non cambia.',
         'Chi gestisce i dispositivi di firma; poi Sogei.'],
        ['`BE-FIRMA-STATO`', 'WARN', 'Firma chiesta su un atto in uno stato che non la ammette '
         '(`FIRMA_STATO_INCOMPATIBILE`).', 'Riconciliare lo stato dal back-office e seguire '
         'l’azione proposta per quello stato.', 'Back-end, se gli stati concordano e la firma '
         'resta inibita.'],
    ]),
    ('Validazione e deposito', [
        ['`ANSC-400001`', 'ERROR', 'Manca un campo obbligatorio. L’evento non è creato e nessun '
         'idAnsc è consumato.', 'Il campo è nell’attributo `campo`: farlo compilare e ripetere '
         'la validazione.', 'Funzionari, se SIPO non ha dove raccogliere il dato; back-end, se '
         'il dato c’è e non arriva nel payload.'],
        ['`ANSC-400002`, `ANSC-400003`', 'ERROR', 'Dati in ingresso incompleti o non corretti.',
         'Leggere gli errori restituiti: se è un dato si corregge, se è un formato si segnala.',
         'Back-end; funzionari per le decodifiche.'],
        ['`BE-PREVERIFICA-KO`', 'WARN', 'La verifica locale trova campi mancanti o non validi '
         'prima di chiamare ANSC.', 'Comportamento atteso: l’operatore corregge.',
         'Funzionari, se la stessa decodifica è rifiutata su molti atti.'],
        ['`ANSC-50001`, `ANSC-50002`', 'ERROR', 'ANSC non riconosce il caso d’uso indicato.',
         'Controllare nel back-office la versione attiva della configurazione e gli avvisi di '
         'revisione del mapping. L’atto resta in attesa.', 'Funzionari (nuova baseline).'],
        ['`CONF-UC-NON-DETERMINATO`, `CONF-UC-AMBIGUO`', 'ERROR', 'Nessun caso d’uso, oppure più '
         'di uno, si applica all’atto (`CONFIG_ASSENTE`).', 'L’operatore non può sbloccarlo: '
         'segnalare con il numero comunale.', 'Funzionari del Comune.'],
        ['`BE-ATTO-GIA-DEPOSITATO`', 'WARN', 'Deposito chiesto su un atto che ha già '
         'l’identificativo nazionale.', 'Non ripetere: proseguire dalla fase successiva.',
         'Back-end, se il nuovo deposito non è stato chiesto dall’operatore.'],
        ['`INFRA-ANSC-ESITO-IGNOTO`', 'ERROR', 'La chiamata è partita e la risposta non è '
         'arrivata. L’atto può essere stato creato.', '**Non ripetere a occhio**: riconciliare '
         'dal back-office; se l’atto c’è si prosegue, altrimenti si ripete la validazione.',
         'Sistemisti, se ricorrente; Sogei, se ANSC è lento.'],
        ['`ANSC-500`', 'ERROR', 'Errore interno di ANSC.', 'Riconciliare prima di ripetere; '
         'ripetere più tardi.', 'Presidio ANSC / Sogei, citando `idOperazione`.'],
    ]),
    ('Allegati', [
        ['`ANSC-413101`', 'WARN', 'File oltre la dimensione ammessa.', 'Ridurre il file e '
         'ricaricarlo.', '—'],
        ['`BE-ALLEG-TIPO`', 'WARN', 'Tipo di documento non previsto per il caso d’uso.',
         'Verificare il tipo scelto.', 'Funzionari, se il documento è richiesto e il tipo '
         'manca.'],
        ['`BE-ALLEG-NON-VERIFICATO`', 'WARN', 'Deposito chiesto prima che la scansione di ANSC '
         'si concluda (stato ANSC_08 diverso da «Inserito»).', 'Attendere e riprovare; lo stato '
         'dell’allegato si vede dal back-office.', 'Presidio ANSC, se resta «In elaborazione» '
         'oltre la giornata.'],
        ['`ANSC-ALLEG-RESPINTO`', 'ERROR', 'La scansione di ANSC ha respinto il file.',
         'Il file non è utilizzabile: acquisirne uno nuovo.', 'Sicurezza, se ricorre dalla '
         'stessa fonte.'],
    ]),
    ('Soggetti', [
        ['`BE-SOGG-NON-TROVATO`', 'WARN', 'La ricerca del soggetto in ANSC non dà risultati.',
         'Verificare i dati anagrafici. Senza identificativo del soggetto gli automatismi non '
         'scattano: non depositare senza.', 'Presidio ANPR, se il soggetto esiste in '
         'anagrafe.'],
        ['`BE-SOGG-DISCORDANTE`', 'WARN', 'Il codice ANPR restituito è diverso da quello già '
         'presente in anagrafe.', 'Nessuna sovrascrittura: segnalarlo dalla pagina degli '
         'identificativi dei soggetti.', 'Ufficio anagrafe.'],
    ]),
    ('Numerazione, configurazione e dizionari', [
        ['`DB-NUM-BLOCCO`', 'ERROR', 'Lo stacco del numero non ottiene il blocco della riga '
         'dell’anno nel tempo previsto.', 'Ripetere dopo qualche secondo: la transazione è '
         'annullata, il numero non è consumato.', 'Amministrazione della base dati, se '
         'ricorrente.'],
        ['`BE-DIZ-SCARICO-KO`', 'ERROR', 'Il servizio di configurazione ANSC non restituisce '
         'una decodifica.', 'Ripetere il comando; restano in uso i dizionari precedenti.',
         'Presidio ANSC, se persiste.'],
        ['`BE-DIZ-TRACCIATO`', 'ERROR', 'Il file della decodifica ha colonne diverse dal '
         'previsto.', 'Non ripetere: il formato è cambiato.', 'Back-end.'],
        ['`CONF-VERSIONE-INCOMPLETA`', 'WARN', 'Attivazione di una baseline con campi '
         'obbligatori senza corrispondenza in SIPO.', 'Completare i campi indicati, poi '
         'attivare.', 'Funzionari.'],
    ]),
    ('Accessi, infrastruttura e programmi', [
        ['`ANSC-401001`, `ANSC-401002`, `ANSC-403001`', 'ERROR', 'Utente non autorizzato '
         'dall’ANSC all’operazione o alla risorsa.', 'Verificare l’abilitazione dell’ufficiale '
         'in ANSC.', 'Chi gestisce le utenze ANSC del Comune.'],
        ['`ANSC-404001`', 'WARN', 'Dati non presenti in una lettura.', 'Spesso legittimo: '
         'nessun risultato.', '—'],
        ['`ANPR-…`', 'ERROR', 'ANPR rifiuta una richiesta.', 'Leggere codice e messaggio '
         'restituiti; se è un dato, correggerlo.', 'Presidio ANPR; ufficio anagrafe.'],
        ['`INFRA-CERT-SCADENZA`', 'WARN / FATAL', 'Certificato del server o di una postazione '
         'in scadenza, oppure scaduto.', 'Segnalare subito.', 'Sistemisti.'],
        ['`DB-CONNESSIONE`', 'FATAL', 'Base dati irraggiungibile.', 'Segnalare subito.',
         'Amministrazione della base dati; sistemisti.'],
        ['`DB-VINCOLO`', 'ERROR', 'Vincolo violato nella base dati.', 'Segnalare con il '
         'collegamento all’evento.', 'Back-end: è quasi sempre un difetto del programma.'],
        ['`BE-INATTESO`', 'ERROR', 'Eccezione non prevista arrivata al gestore globale.',
         'Aprire la traccia e segnalare con il collegamento all’evento.', 'Back-end.'],
        ['`FE-CHIAMATA-KO`', 'ERROR', 'Chiamata dal browser fallita dopo i tentativi.',
         'Con stato 401 o 403: sessione o abilitazioni. Con 5xx: aprire la traccia del '
         'back-end.', 'Front-end o back-end, secondo la traccia.'],
    ]),
]

COLONNE_CAT = [
    ['Colonna', 'Significato'],
    ['Codice', 'Il codice evento. Il prefisso è l’origine, quindi dice già a quale gruppo '
     'compete.'],
    ['Liv.', 'Il livello predefinito. Chi registra può alzarlo, non abbassarlo.'],
    ['Quando si presenta', 'La situazione in parole del mestiere, con il codice del contratto '
     'fra parentesi quando esiste.'],
    ['Che cosa fa il primo livello', 'L’azione che risolve o che prepara la segnalazione. Se '
     'non c’è nulla da fare, lo dice.'],
    ['Se non basta', 'A chi passa la segnalazione e in quale caso.'],
]


def catalogo(doc, prima, modello):
    tab = lambda r, w: tabella(doc, prima, r, modello, w)  # noqa: E731
    h(doc, prima, 1, 'Il catalogo dei codici di errore e le azioni di risoluzione')
    par(doc, prima,
        'Il codice evento serve a cercare e a contare; per chi fa assistenza serve anche una '
        'cosa in più: **sapere che cosa fare** quando lo vede. Il catalogo lega ogni codice '
        'alla sua causa probabile, all’azione del primo livello e al gruppo a cui passare la '
        'segnalazione. Il back-office lo mostra accanto all’evento, così l’azione non dipende '
        'dalla memoria di chi è di turno.')
    par(doc, prima,
        'Le voci che seguono sono il contenuto iniziale. Vengono da tre fonti: i codici di '
        'errore pubblicati da ANSC [S4], i codici di errore già dichiarati nei nostri contratti '
        '[S5] e i casi di infrastruttura ricorrenti nel disegno [R1]. Le azioni dipendono da '
        'regole già fissate nell’analisi: un esito ignoto si riconcilia e non si ripete, un '
        'rifiuto per campo mancante non consuma l’identificativo nazionale, la sessione dura '
        'quattro ore.')

    h(doc, prima, 2, 'Come si legge una voce')
    tab(COLONNE_CAT, [1.8, 4.6])

    h(doc, prima, 2, 'Il catalogo iniziale')
    for titolo, righe in CATALOGO:
        h(doc, prima, 3, titolo)
        tab([INTESTAZIONE_CAT] + righe, [1.35, 0.55, 1.5, 1.8, 1.2])
    par(doc, prima,
        'Il catalogo cresce con l’esercizio: un evento con un codice che non vi compare è '
        'esso stesso un segnale, e il back-office lo mostra come «codice non catalogato». '
        'Ogni voce nuova nasce da una segnalazione risolta, con l’azione che l’ha risolta.')

    h(doc, prima, 2, 'Dove vive il catalogo')
    par(doc, prima,
        'Perché il back-office possa mostrarlo, il catalogo sta in una tabella di '
        'configurazione dello schema ANSC_USR, con i nomi dello standard [R5].')
    codice(doc, prima, [
        'CREATE TABLE ANSC_USR.ANSC_CFG_CODICE_EVENTO (',
        '  COD_EVENTO            VARCHAR2(40 CHAR)   NOT NULL,',
        '  COD_ORIGINE           VARCHAR2(10 CHAR)   NOT NULL,',
        '  COD_LIVELLO           VARCHAR2(10 CHAR)   NOT NULL,  -- livello predefinito',
        '  DESC_EVENTO           VARCHAR2(400 CHAR)  NOT NULL,  -- quando si presenta',
        '  TXT_AZIONE_PRIMO_LIV  VARCHAR2(2000 CHAR) NOT NULL,  -- che cosa fa il primo livello',
        '  COD_GRUPPO_COMPETENTE VARCHAR2(40 CHAR),             -- a chi passa',
        '  TXT_NOTE_SECONDO_LIV  VARCHAR2(2000 CHAR),',
        '  COD_CODICE_REMOTO     VARCHAR2(40 CHAR),             -- codice ANSC, ANPR o del contratto',
        "  FLG_RIPETIBILE        CHAR(1) DEFAULT 'N' NOT NULL,  -- si risolve ripetendo",
        "  FLG_ATTIVO            CHAR(1) DEFAULT 'S' NOT NULL,",
        '  TS_INS                TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
        '  UTENTE_INS            VARCHAR2(40 CHAR) NOT NULL,',
        '  TS_UPD                TIMESTAMP,',
        '  UTENTE_UPD            VARCHAR2(40 CHAR),',
        '  CONSTRAINT PK_ANSC_CFG_CODICE_EVENTO PRIMARY KEY (COD_EVENTO),',
        '  CONSTRAINT CK_ANSC_CFG_COD_EV_ORIG',
        "    CHECK (COD_ORIGINE IN ('FE','BE','DB','ANSC','ANPR','INFRA','CONF')),",
        '  CONSTRAINT CK_ANSC_CFG_COD_EV_LIV',
        "    CHECK (COD_LIVELLO IN ('TRACE','DEBUG','INFO','WARN','ERROR','FATAL')),",
        "  CONSTRAINT CK_ANSC_CFG_COD_EV_RIP CHECK (FLG_RIPETIBILE IN ('S','N')),",
        "  CONSTRAINT CK_ANSC_CFG_COD_EV_ATT CHECK (FLG_ATTIVO IN ('S','N'))",
        ') TABLESPACE ANSC_USR;',
    ], 'Il catalogo dei codici evento.')
    voce(doc, prima, 'La chiave è il codice, non un identificativo surrogato.',
         'È uno scostamento dichiarato da [R5]: il codice è l’identità stabile della voce, '
         'viaggia per valore negli eventi e nel codice applicativo, e un numero in più non '
         'aggiungerebbe nulla.')
    voce(doc, prima, 'Nessuna chiave esterna dal registro.',
         'ANSC_LOG_EVENTO.COD_EVENTO richiama il catalogo per valore. Il registro deve '
         'accettare anche un codice non ancora catalogato: rifiutarlo farebbe perdere proprio '
         'l’evento nuovo.')
    voce(doc, prima, 'Non è versionato.',
         'Non è configurazione dell’atto: una voce corretta vale subito, anche per gli eventi '
         'passati.')
    voce(doc, prima, 'Le letture lo restituiscono.',
         '`cercaEventi` e `leggiEvento` riportano, accanto al codice, la descrizione e l’azione '
         'del primo livello.')
    voce(doc, prima, 'Chi lo cura.',
         'Il secondo livello di supporto. All’inizio si popola da questo capitolo con uno '
         'script; se serva una pagina di back-office per curarlo è OT-15.')


# =========================================================== 5. transizione
TRATTE = [
    ['Tratta', 'Che cosa succede', 'Dove si configura', 'Se si ferma'],
    ['1 · Nel programma', 'La libreria arricchisce l’evento, lo mette in una coda in memoria di '
     'dimensione limitata e lo consegna a blocchi, a intervalli di pochi secondi. In parallelo '
     'scrive la riga su standard output, come oggi.', 'Variabili `OTEL_*`, uguali per tutti i '
     'pod.', 'A coda piena si scartano gli eventi più vecchi e si conta lo scarto. **Il '
     'programma non si blocca mai.**'],
    ['2 · Verso il collector', 'OTLP su gRPC (4317) o HTTP (4318), dentro il cluster.',
     'Un solo indirizzo interno, il servizio del collector.', 'Il trasporto ritenta per un '
     'tempo limitato, poi scarta.'],
    ['3 · Nel collector', 'Limite di memoria; scarto di TRACE e DEBUG in produzione; '
     'cancellazione delle chiavi vietate; raggruppamento; coda persistente su disco.',
     'Il file di configurazione del collector, in una ConfigMap.', 'La coda su disco tiene '
     'alcune ore di eventi se il servizio a valle è fermo.'],
    ['4 · Verso be-osservabilita', 'OTLP su HTTP verso l’indirizzo interno del servizio.',
     'L’esportatore del collector.', 'Il servizio risponde «non disponibile» se Oracle non '
     'risponde; il collector accoda e ritenta.'],
    ['5 · In be-osservabilita', 'Converte log e span in righe di ANSC_LOG_EVENTO e '
     'ANSC_LOG_SPAN e le inserisce a blocchi, una transazione per blocco.', 'Il codice del '
     'servizio.', '—'],
    ['6 · In Oracle', 'Partizioni giornaliere; la scadenza elimina le partizioni oltre il '
     'periodo di conservazione.', 'Il job notturno `JOB_SCADENZA_LOG` → `PRC_SCADENZA_LOG`.',
     'Se il job salta una notte, recupera la successiva.'],
    ['7 · Lettura', 'Il back-office chiama le operazioni di lettura di be-osservabilita.',
     'Il registro delle pagine [R2].', '—'],
    ['Dal browser', 'I micro-frontend non vedono il collector: consegnano i blocchi a '
     '`creaEventi`, dallo stesso ingresso delle altre API. Il servizio li scrive in tabella '
     'come gli altri.', 'Limiti di OT-12.', 'Il browser scarta, non ritenta all’infinito.'],
]

ORACLE12 = [
    ['Elemento', 'In Oracle 12', 'Che cosa si fa'],
    ['Colonna a numerazione automatica (`IDENTITY`)', 'Disponibile.', 'Invariato.'],
    ['Vincolo `IS JSON` sui CLOB', 'Disponibile dalla 12.1.0.2.', 'Invariato se la release lo '
     'consente; altrimenti CLOB senza vincolo e controllo nel servizio.'],
    ['Partizionamento per intervallo', 'Richiede l’edizione Enterprise con l’opzione '
     'Partitioning.', 'Da verificare (OT-14). In mancanza: tabelle non partizionate e '
     'cancellazione giornaliera a blocchi. Funziona, costa di più.'],
    ['Chiave di partizione', 'Il partizionamento per intervallo accetta date e timestamp, '
     'non timestamp con fuso.', '`TS_EVENTO` e `TS_INIZIO` sono `TIMESTAMP` in UTC. Le API '
     'restituiscono l’ora con il fuso.'],
    ['Lunghezza dei nomi', '30 byte fino alla 12.1, 128 dalla 12.2.', 'I nomi proposti stanno '
     'nei 30.'],
    ['Tipo JSON nativo', 'Non disponibile.', 'Si resta su CLOB con `IS JSON`.'],
    ['Eliminazione di una partizione con chiave primaria globale', 'L’indice globale diventa '
     'inutilizzabile.', 'Il job usa `DROP PARTITION … UPDATE GLOBAL INDEXES`.'],
]

GESTIONE = [
    ['Componente', 'Chi lo gestisce', 'Nota'],
    ['Libreria `osservabilita-sipo`', 'Gruppo SIPO (back-end).', 'Si rilascia come le altre '
     'librerie comuni.'],
    ['Collector: deployment, configurazione, volume per la coda', 'OT-04.', 'Nel cluster non '
     'c’è nulla (OT-02): finché la questione è aperta lo installa il gruppo SIPO.'],
    ['`be-osservabilita`', 'Gruppo SIPO.', 'Quinta unità di deployment (OT-10).'],
    ['Tabelle, partizioni, job di scadenza', 'Amministrazione della base dati.', ''],
    ['Catalogo dei codici', 'Secondo livello di supporto.', 'OT-15.'],
    ['Livelli in produzione e accensioni temporanee', 'Secondo livello, con i referenti.',
     'OT-11.'],
    ['Abilitazioni alle pagine', 'Amministratori del back-office [R2].', 'OT-13 per gli '
     'attributi visibili.'],
]

FERMI = [
    ['Che cosa si ferma', 'Effetto sugli atti', 'Effetto sui log'],
    ['be-osservabilita', 'Nessuno.', 'Il collector accoda su disco e scarica alla ripresa; '
     'oltre la capienza perde i più vecchi.'],
    ['Collector', 'Nessuno.', 'Le librerie accodano in memoria per pochi minuti, poi scartano. '
     'Restano le righe su standard output.'],
    ['Oracle', 'Quello di Oracle: gli atti si fermano comunque.', 'Come per be-osservabilita.'],
    ['Il programma termina in modo anomalo', '—', 'Gli eventi ancora in coda si perdono; la '
     'riga su standard output resta. È per questo che nella transizione la console non si '
     'spegne.'],
]


def transizione(doc, prima, modello, png):
    tab = lambda r, w: tabella(doc, prima, r, modello, w)  # noqa: E731
    h(doc, prima, 2, 'Nella transizione: dove vanno i dati e chi li gestisce')
    par(doc, prima,
        'Due risposte dei punti aperti fissano il quadro. Nel cluster non esiste nulla da '
        'riusare — né collector, né raccoglitore di metriche, né piattaforma di log (OT-02) — '
        'e la base dati in esercizio è **Oracle 12** (OT-01). La configurazione che segue è '
        'quindi quella con cui si parte, ed è anche quella che resta se non si passerà a uno '
        'strumento dedicato. Vi compare be-osservabilita, il servizio descritto nel capitolo '
        '«Le interfacce», che qui fa anche da scarico del collector verso Oracle.')
    D.immagine(doc, prima, png, 6.4,
               'Figura 2 — Il percorso dei dati nella transizione: tutto resta nel cluster e '
               'nella base dati del Comune.')

    h(doc, prima, 3, 'Il percorso, tratta per tratta')
    tab(TRATTE, [1.1, 2.4, 1.4, 1.5])
    par(doc, prima,
        '**Perché lo scarico è be-osservabilita e non un componente del collector.** '
        'OpenTelemetry non offre un esportatore per Oracle. Scriverlo dentro il collector '
        'vorrebbe dire costruire e mantenere una distribuzione propria del collector, nel suo '
        'linguaggio; riceverlo in be-osservabilita è lavoro nel linguaggio del gruppo, in un '
        'servizio che serve comunque — per il browser e per le letture. Il collector resta la '
        'distribuzione standard, configurata e non modificata, ed è ciò che permette domani di '
        'aggiungere un secondo esportatore senza toccare nulla.')
    par(doc, prima,
        '**Il registro probatorio non passa di qui.** ANSC_LOG_AUDIT la scrive il '
        'concentratore, nella propria transazione, come previsto da [R1]: il percorso '
        'diagnostico può perdere dati, l’audit no. Le due strade si toccano solo per valore, '
        'attraverso TRACE_ID.')

    h(doc, prima, 3, 'Le tracce: la tabella che mancava')
    par(doc, prima,
        'Il registro diagnostico conserva gli eventi; la cascata del dettaglio della traccia e '
        'l’operazione `leggiTraccia` hanno però bisogno anche degli **span**, con il loro '
        'inizio, la durata e il passo padre. Serve una seconda tabella, con lo stesso regime di '
        'ANSC_LOG_EVENTO.')
    codice(doc, prima, [
        'CREATE TABLE ANSC_USR.ANSC_LOG_SPAN (',
        '  TRACE_ID         VARCHAR2(32 CHAR)  NOT NULL,',
        '  SPAN_ID          VARCHAR2(16 CHAR)  NOT NULL,',
        '  SPAN_ID_PADRE    VARCHAR2(16 CHAR),',
        '  TS_INIZIO        TIMESTAMP(6)       NOT NULL,   -- in UTC',
        '  NUM_DURATA_MS    NUMBER(12,3)       NOT NULL,',
        '  COD_NOME_PASSO   VARCHAR2(100 CHAR) NOT NULL,   -- es. deposito-R009',
        '  COD_TIPO         VARCHAR2(10 CHAR),             -- SERVER CLIENT INTERNO',
        '  COD_ESITO        VARCHAR2(10 CHAR),             -- OK KO',
        '  COD_SERVIZIO     VARCHAR2(40 CHAR)  NOT NULL,',
        '  COD_VERSIONE_SW  VARCHAR2(20 CHAR),',
        '  ID_ATTO_SIPO     NUMBER,                        -- per valore',
        '  TXT_ATTRIBUTI    CLOB,',
        '  CONSTRAINT CK_ANSC_LOG_SPAN_TIPO',
        "    CHECK (COD_TIPO IN ('SERVER','CLIENT','INTERNO')),",
        "  CONSTRAINT CK_ANSC_LOG_SPAN_ESITO CHECK (COD_ESITO IN ('OK','KO')),",
        '  CONSTRAINT CK_ANSC_LOG_SPAN_ATTR CHECK (TXT_ATTRIBUTI IS JSON)',
        ')',
        "PARTITION BY RANGE (TS_INIZIO) INTERVAL (NUMTODSINTERVAL(1,'DAY'))",
        "  (PARTITION P_INIZIALE VALUES LESS THAN (TIMESTAMP '2027-01-01 00:00:00'))",
        'TABLESPACE ANSC_USR;',
        '',
        'CREATE INDEX IX_ANSC_LOG_SPAN_TRACE ON ANSC_USR.ANSC_LOG_SPAN (TRACE_ID)',
        '  LOCAL TABLESPACE ANSC_USR;',
    ], 'La tabella degli span.')
    voce(doc, prima, 'Nessuna chiave primaria, di proposito.',
         'Un indice unico globale andrebbe ricostruito a ogni eliminazione di partizione, e uno '
         'locale dovrebbe contenere la data. L’unicità di traccia e passo la garantisce chi li '
         'genera; la ricerca passa sempre per TRACE_ID.')
    voce(doc, prima, 'Stessa conservazione del registro diagnostico.',
         'Una traccia serve finché serve la diagnosi; gli span più degli eventi sono numerosi, '
         'ed è la ragione per non tenerli oltre.')
    voce(doc, prima, 'Campionamento al cento per cento, per cominciare.',
         'Con la conservazione breve il volume resta contenuto; si rivede al quarto gradino '
         'con i numeri veri.')

    h(doc, prima, 3, 'Che cosa cambia con Oracle 12')
    tab(ORACLE12, [1.9, 2.0, 2.5])

    h(doc, prima, 3, 'Chi gestisce che cosa')
    tab(GESTIONE, [2.1, 1.9, 2.4])

    h(doc, prima, 3, 'Se qualcosa si ferma')
    par(doc, prima,
        'La regola che regge il percorso: **la diagnostica può perdere dati, la formazione '
        'dell’atto non deve mai fermarsi per colpa sua.** Nessun componente della figura è in '
        'grado di bloccare un programma applicativo.')
    tab(FERMI, [1.7, 1.8, 2.9])

    h(doc, prima, 3, 'Che cosa resta com’è')
    voce(doc, prima, 'La console.',
         'Ogni pod continua a scrivere su standard output; i sistemisti continuano a leggerlo '
         'come oggi. È il ripiego se tutto il resto è fermo.')
    voce(doc, prima, 'I ventotto moduli con il logBack.xml non caricato.',
         'Restano come sono (OT-07). La libreria aggancia il proprio canale verso il collector '
         'all’avvio, da programma: gli eventi arrivano comunque in tabella; la loro console resta '
         'senza identificativi.')
    voce(doc, prima, 'Le metriche.',
         'Nella transizione non si archiviano: non c’è un raccoglitore (OT-02). I conteggi che '
         'servono al supporto vengono dal riepilogo sugli eventi. Le metriche entrano al '
         'quarto gradino.')
    voce(doc, prima, 'Come si esce dalla transizione.',
         'Arrivato uno strumento dedicato, si aggiunge un esportatore nella configurazione del '
         'collector e si tengono le due destinazioni in parallelo per un periodo di confronto. '
         'Il codice applicativo non cambia.')


# =========================================================== 6. aggiunte puntuali
def aggiunte(doc, modello):
    # voce sull'UTC, in coda alle note del registro diagnostico
    ancora = D.h(doc, 1, 'Dove si archivia e come si analizza')._p
    voce(doc, ancora, 'Il tempo in UTC.',
         'TS_EVENTO non porta il fuso: con Oracle 12 la chiave di un partizionamento per '
         'intervallo non lo ammette. L’ora si registra in UTC e le API la restituiscono con il '
         'fuso, così il cambio dell’ora legale non produce né buchi né sovrapposizioni.')

    # la worklist mostra l'azione del catalogo
    ancora = D.h(doc, 2, 'Il dettaglio della traccia')._p
    par(doc, ancora,
        'Aprendo una riga, il pannello di dettaglio riporta dal catalogo dei codici la '
        'descrizione e l’azione del primo livello, e il gruppo a cui passare la segnalazione. '
        'Un codice assente dal catalogo si presenta come «codice non catalogato».')

    # glossario
    glos = D.trova_tabella(doc, 'Termine', 'Significato')
    for riga in [
        ('Codice evento', 'Il codice stabile e cercabile che classifica un evento, nella forma '
         'ORIGINE-AREA-FATTO.', 'Non è il messaggio, che può cambiare.'),
        ('Catalogo dei codici', 'La tabella che lega ogni codice evento a causa, azione del '
         'primo livello e gruppo competente.', 'ANSC_CFG_CODICE_EVENTO.'),
        ('Passo', 'Il nome italiano usato nel codice per lo span.', ''),
    ]:
        D.clona_riga(glos, riga)

    # riferimenti
    rif = D.trova_tabella(doc, 'Riferimento', 'Natura')
    for riga in [
        ('[S4]', 'ansc/docs/openapi/Codici d’errore.xlsx — i 21 codici di errore dei servizi '
         'ANSC.', 'Sorgente ANSC'),
        ('[S5]', 'I contratti ansc-v1.yaml, ansc-dizionari-v1.yaml, ansc-automazione-v1.yaml — '
         'i codici di errore dichiarati per operazione.', 'Documento di progetto'),
    ]:
        D.clona_riga(rif, riga)

    # punti aperti
    op = D.trova_tabella(doc, 'Questione', 'A chi spetta')
    for riga in [
        ('OT-10', 'Se le operazioni di lettura e ricerca debbano stare in un servizio dedicato '
         '(be-osservabilita, come proposto) oppure dentro il back-office che già esiste. Il '
         'servizio dedicato tiene separato il dominio di guasto ed è anche lo scarico del '
         'collector verso Oracle; è però una quinta unità da gestire.', 'Architettura'),
        ('OT-11', 'Se si voglia poter cambiare i livelli a caldo, per singolo componente e per '
         'un tempo dichiarato, senza rilasciare. Comodo per la diagnosi, pericoloso se '
         'dimenticato acceso.', 'Architettura / Referenti SIPO'),
        ('OT-12', 'I limiti dell’ingestione dal browser: dimensione del blocco, frequenza per '
         'sessione, e che cosa fare quando si superano.', 'Sicurezza / Architettura'),
        ('OT-13', 'Quali attributi degli eventi mostrare nel back-office, e a quale ruolo. Gli '
         'attributi possono contenere riferimenti a persone, anche se oscurati.',
         'Responsabile della protezione dei dati / Architettura'),
        ('OT-14', 'Release esatta di Oracle 12 ed edizione in esercizio: se l’opzione '
         'Partitioning è disponibile e se il vincolo IS JSON è ammesso (dalla 12.1.0.2). Da '
         'qui dipende la forma delle tabelle del registro.', 'Amministrazione della base dati'),
        ('OT-15', 'Chi cura il catalogo dei codici e se serva una pagina di back-office per '
         'farlo, oltre al popolamento iniziale da script.', 'Supporto / Referenti SIPO'),
    ]:
        D.clona_riga(op, riga)


def intesta(doc):
    for fatto in D.frontespizio(doc, '0.3', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.3', DATA):
        print('  ' + fatto)
    D.storia(doc, DATA, '0.3',
             'Le interfacce · Guida all’uso · Catalogo dei codici · Dove si archivia · '
             'Punti aperti',
             'Recepite le risposte a OT-01 (Oracle 12), OT-02, OT-05 e OT-07: tempo del '
             'registro in UTC, canale verso il collector agganciato da programma, ingresso del '
             'browser dalle API. Nuova sezione sull’arricchimento degli eventi: che cosa ricava '
             'la libreria, che cosa scrive lo sviluppatore, il vocabolario degli attributi di '
             'dominio. Nuovo capitolo con la guida all’uso di log e tracce nelle classi e nei '
             'metodi. Nuovo capitolo con il catalogo dei codici di errore e le azioni del primo '
             'livello, e la tabella ANSC_CFG_CODICE_EVENTO. Nuova sezione sul percorso dei dati '
             'nella transizione, con figura, la tabella degli span ANSC_LOG_SPAN, gli effetti '
             'di Oracle 12, chi gestisce che cosa e che cosa succede se un componente si ferma. '
             'Ripristinati in tabella OT-10…OT-12; OT-13…OT-15 nuovi. Corretti un rimando e '
             'due conteggi.')


if __name__ == '__main__':
    shutil.copyfile(SRC, OUT)
    doc = docx.Document(OUT)
    modello = D.trova_tabella(doc, 'Questione', 'A chi spetta')
    fatti = []
    correzioni(doc, fatti)
    for f in fatti:
        print('  ' + f)

    png = diagrammi_otel.transizione()
    arricchimento(doc, D.h(doc, 2, 'Il servizio e il suo contratto')._p, modello)
    ancora_bo = D.h(doc, 1, 'Il back-office del supporto')._p
    guida(doc, ancora_bo, modello)
    catalogo(doc, ancora_bo, modello)
    transizione(doc, D.h(doc, 1, 'La libreria di inserimento')._p, modello, png)
    aggiunte(doc, modello)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
