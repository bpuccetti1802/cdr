# -*- coding: utf-8 -*-
"""Genera «PROPOSTA_Osservabilita-OpenTelemetry» — la proposta di adottare OpenTelemetry
come impianto di registrazione per i componenti dell'integrazione ANSC e per la catena
dell'atto in SIPO.

Perimetro e scelte, decisi con l'utente il 09/11/2026:
  * perimetro = i quattro pod nuovi + i back-end di stato civile toccati dalla catena
    dell'atto + i front-end (Angular nuovi e Thymeleaf esistenti);
  * OpenTelemetry **affianca** ANSC_LOG_AUDIT, non la sostituisce: l'audit resta la traccia
    probatoria, OTel copre diagnostica e supporto;
  * Oracle e' una preferenza, non un vincolo: il documento descrive le due vie con i loro
    limiti reali e raccomanda;
  * si tratta anche il front-end, Angular e Thymeleaf, perche' il problema e' diverso nei due.

Richieste aggiunte dall'utente dopo l'approvazione del piano: una revisione della tabella di
log attuale, un back-office per il supporto, una classificazione degli errori per origine e
i livelli di severita' con la loro descrizione, esempi d'uso della libreria nei capitoli.

Tutti i numeri sullo stato di fatto sono verificati sui sorgenti (39 logBack.xml, 11 dichiarati
con logging.config, 0 campi MDC, 78 ConsoleAppender, logstash-logback-encoder 7.4 in 9 pom e
usato da 1 sola configurazione, 0 moduli con actuator).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_otel.py
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
IMG = os.path.join(BASE, 'Documenti finali', 'strumenti', 'img')
OUT = os.path.join(BASE, 'Documenti finali',
                   'PROPOSTA_Osservabilita-OpenTelemetry_v0.1.docx')

TAGLIA_DA = 29
DATA = '09/11/2026'


# ------------------------------------------------------------------ primitive
def pezzi_di(s):
    """«testo **grassetto** e `monospazio`» -> [(testo, grassetto, mono)]."""
    out = []
    for frammento, grassetto in D.segmenta('', s):
        for i, parte in enumerate(frammento.split('`')):
            if parte:
                out.append((parte, grassetto, i % 2 == 1))
    return out


def _versa(p, s, grassetto_forzato=False, dim=None):
    for txt, grassetto, mono in pezzi_di(s):
        r = p.add_run(txt)
        r.bold = grassetto or grassetto_forzato
        if mono:
            r.font.name = 'Courier New'
            r.font.size = Pt((dim or 10) - 1)
        elif dim:
            r.font.size = Pt(dim)
    return p


def h(d, livello, t):
    p = d.add_paragraph(style='Heading %d' % livello)
    p.add_run(t)
    return p


def par(d, t, stile='Normal'):
    return _versa(d.add_paragraph(style=stile), t)


def voce(d, testa, corpo):
    p = d.add_paragraph(style='List Paragraph')
    _versa(p, testa + ' ', grassetto_forzato=True)
    return _versa(p, corpo)


def codice(d, righe, didascalia=None):
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)
    if didascalia:
        p = d.add_paragraph()
        _versa(p, didascalia, dim=9)
        for r in p.runs:
            r.italic = True
            r.font.size = Pt(8)
    d.add_paragraph()


def tabella(d, righe, larghezze=None):
    t = d.add_table(rows=len(righe), cols=len(righe[0]))
    t.style = 'Table Grid'
    for i, riga in enumerate(righe):
        for j, v in enumerate(riga):
            cel = t.cell(i, j)
            cel.text = ''
            _versa(cel.paragraphs[0], str(v), grassetto_forzato=(i == 0), dim=9)
    if larghezze:
        for j, w in enumerate(larghezze):
            for riga in t.rows:
                riga.cells[j].width = Inches(w)
        griglia = t._tbl.find(qn('w:tblGrid'))
        if griglia is not None:
            for col, w in zip(griglia.findall(qn('w:gridCol')), larghezze):
                col.set(qn('w:w'), str(int(round(Inches(w).twips))))
        t._tbl.tblPr.append(docx.oxml.parse_xml(
            '<w:tblLayout %s w:type="fixed"/>' % docx.oxml.ns.nsdecls('w')))
    d.add_paragraph()
    return t


def figura(d, nome_png, pollici, didascalia):
    p = d.add_paragraph()
    p.alignment = 1
    p.add_run().add_picture(os.path.join(IMG, nome_png), width=Inches(pollici))
    c = d.add_paragraph()
    c.alignment = 1
    r = c.add_run(didascalia)
    r.italic = True
    r.font.size = Pt(9)
    d.add_paragraph()


def testo(par_, s):
    if par_.runs:
        par_.runs[0].text = s
        for r in par_.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        par_.add_run(s)


def costruisci():
    shutil.copyfile(TEMPLATE, OUT)
    d = docx.Document(OUT)
    body = d.element.body
    for ch in list(body.iterchildren())[TAGLIA_DA:]:
        if ch.tag != qn('w:sectPr'):
            body.remove(ch)
    for p in d.paragraphs:
        if '\u201cLorem Ipsum\u201d' in p.text:
            testo(p, '\u201cIntegrazione SIPO \u2013 ANSC\u201d')
        elif p.style.name == 'Subtitle':
            testo(p, 'Proposta per l\u2019osservabilit\u00e0: OpenTelemetry come impianto di '
                     'registrazione, diagnosi e supporto')
    return d


# =================================================================== contenuti
GLOSSARIO = [
    ['Termine', 'Significato', 'Nota'],
    ['OpenTelemetry (OTel)', 'Specifica e insieme di librerie, sotto la Cloud Native Computing '
     'Foundation, per produrre e trasportare dati di osservabilit\u00e0.',
     'Non \u00e8 un prodotto: non archivia e non mostra nulla.'],
    ['Segnale', 'Una delle tre famiglie di dati: log, tracce, metriche.', ''],
    ['Traccia (trace)', 'Il racconto completo di una richiesta attraverso tutti i processi che '
     'attraversa.', '\u00c8 ci\u00f2 che oggi manca del tutto.'],
    ['Span', 'Un singolo passo dentro una traccia: una chiamata, una query, un calcolo.',
     'Ha un inizio, una durata, un esito e degli attributi.'],
    ['`trace_id` / `span_id`', 'Gli identificativi che legano fra loro gli span e i log di una '
     'stessa richiesta.', '32 e 16 cifre esadecimali.'],
    ['Propagazione del contesto', 'Il passaggio di `trace_id` e `span_id` da un processo al '
     'successivo, per intestazione HTTP.', 'Standard W3C `traceparent`.'],
    ['OTLP', 'Il protocollo con cui i segnali viaggiano verso il raccoglitore.', ''],
    ['Collector', 'Il processo che riceve i segnali, li filtra e li inoltra alla destinazione.',
     '\u00c8 il punto in cui si cambia destinazione senza toccare il codice.'],
    ['MDC', 'La mappa di contesto per thread di SLF4J, da cui il motore di log attinge i campi '
     'da stampare.', 'In SIPO non \u00e8 usata in nessun pattern.'],
    ['Cardinalit\u00e0', 'Il numero di valori distinti che un attributo pu\u00f2 assumere.',
     'Alta cardinalit\u00e0 su una metrica la rende impraticabile.'],
]

RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[R1]', '`ANALISI_Integrazione-ANSC` (versione corrente) \u2014 architettura, unit\u00e0 di '
     'deployment, modello dati e DDL di `ANSC_LOG_AUDIT`.', 'Documento di progetto'],
    ['[R2]', '`DISEGNO_Back-Office_ANSC` (versione corrente) \u2014 le pagine del back-office e '
     'il registro delle pagine e del menu.', 'Documento di progetto'],
    ['[R3]', '`ANALISI_Front-End-Angular` (versione corrente) \u2014 i micro-frontend e la '
     'libreria condivisa.', 'Documento di progetto'],
    ['[R4]', '`ANALISI_Identita-Profilazione-IAM` (versione corrente) \u2014 identit\u00e0 '
     'dell\u2019utente e perimetro del vecchio ambiente.', 'Documento di progetto'],
    ['[R5]', '`Naming_convention_X_DB_v1.01` \u2014 nomenclatura degli oggetti di base dati.',
     'Standard aziendale'],
    ['[S1]', 'I 39 file `logBack.xml` dei moduli di SIPO e i rispettivi '
     '`application.properties`.', 'Sorgente applicativo'],
    ['[S2]', '`common/profilazione-utente` \u2014 l\u2019unico modulo che usa gi\u00e0 un '
     'codificatore di log strutturato.', 'Sorgente applicativo'],
    ['[S3]', '`back-end/all-ansc-sipo`, `all-anpr-sipo`, `statocivile-be`, `matrim-be`, '
     '`nascita-be`, `decessi-be` \u2014 i moduli della catena dell\u2019atto.',
     'Sorgente applicativo'],
    ['[O1]', 'Specifica OpenTelemetry e convenzioni semantiche, Cloud Native Computing '
     'Foundation.', 'Standard aperto'],
    ['[O2]', 'W3C Trace Context \u2014 la raccomandazione sull\u2019intestazione '
     '`traceparent`.', 'Standard aperto'],
]

STATO = [
    ['Che cosa', 'Quanto', 'Che cosa significa'],
    ['File `logBack.xml` nei moduli', '**39**', 'Ogni modulo ha la sua configurazione, '
     'scritta a mano e non derivata da un modello comune.'],
    ['Moduli che la dichiarano con `logging.config`', '**11**',
     'Il nome `logBack.xml` con la B maiuscola **non \u00e8 quello che Logback cerca da s\u00e9**: '
     'nei restanti 28 moduli il file c\u2019\u00e8 e non viene caricato. Quei moduli girano con la '
     'configurazione predefinita di Spring Boot.'],
    ['Appender console / file / syslog', '**78 / 2 / 2**',
     'La registrazione \u00e8 quasi interamente su standard output, in testo semplice.'],
    ['Campi di contesto (`%X{...}`) nei pattern', '**0**',
     '**Nessun pattern porta un identificativo di correlazione.** \u00c8 la lacuna che questo '
     'documento si propone di colmare.'],
    ['Moduli con `spring-boot-starter-actuator`', '**0**',
     'Non esiste alcun punto di controllo della salute n\u00e9 di esposizione delle metriche: '
     'sotto Kubernetes \u00e8 un\u2019assenza che va nominata.'],
    ['Moduli che dichiarano `logstash-logback-encoder`', '**9**',
     'La libreria per il log strutturato in JSON \u00e8 gi\u00e0 nei `pom.xml`.'],
    ['Configurazioni che la usano davvero', '**1**',
     '`common/profilazione-utente`, il modulo pi\u00f9 recente. Qualcuno ha gi\u00e0 cominciato, '
     'e la proposta ne raccoglie la direzione.'],
]

AUDIT_LIMITI = [
    ['#', 'Limite', 'Che cosa comporta per il supporto'],
    ['1', 'Nessun identificativo di correlazione',
     'Una sola azione dell\u2019operatore attraversa il front-end, un concentratore, forse il '
     'numeratore e poi ANSC. Nulla lega fra loro le righe che ne derivano: **la ricostruzione '
     '\u00e8 manuale e congetturale**, si procede per vicinanza di orario.'],
    ['2', 'Nessuna indicazione del componente che ha scritto la riga',
     'Con quattro processi nuovi e sette back-end esistenti non si sa da dove venga un errore, '
     'quindi non si sa a chi assegnarlo.'],
    ['3', 'Nessuna severit\u00e0',
     '`ESITO` distingue riuscito da fallito. Non esiste la gradazione fra «\u00e8 andata male e '
     'si riprova da s\u00e9» e «\u00e8 andata male e qualcuno deve intervenire adesso».'],
    ['4', 'La chiave esterna lega ogni riga a un atto',
     '`ID_STATO_ATTO` referenzia `ANSC_STATO_ATTO`. Tutto ci\u00f2 che non \u00e8 un atto \u2014 il '
     'caricamento dei dizionari, lo stacco di un numero, una notifica in ingresso, '
     'l\u2019attivazione di una baseline, un\u2019azione di back-office, un errore del front-end '
     '\u2014 **non ha dove essere registrato**.'],
]

DOMANDE = [
    ['Domanda del supporto', 'Oggi', 'Con la proposta'],
    ['«L\u2019operatore dice che alle 17:42 la validazione \u00e8 fallita: che cosa \u00e8 '
     'successo?»', 'Si cercano righe vicine di orario in registri separati.',
     'Si apre la traccia e si vede la sequenza completa.'],
    ['«Di chi \u00e8 il problema: nostro, di Sogei o della rete?»',
     'Si deduce dal testo del messaggio.', 'Lo dice la classificazione per origine.'],
    ['«\u00c8 un caso isolato o succede a tutti?»',
     'Non rispondibile senza interrogare a mano.',
     'Un conteggio per codice evento sulle ultime ore.'],
    ['«Da quando?»', 'Non rispondibile: manca la versione del componente.',
     'L\u2019attributo di versione \u00e8 su ogni evento.'],
    ['«Il numero comunale era gi\u00e0 stato staccato quando \u00e8 fallita?»',
     'Si guarda l\u2019atto e si inferisce.',
     'Gli span sono in sequenza e in scala sui tempi.'],
]

SEGNALI = [
    ['Segnale', 'Che cos\u2019\u00e8', 'A che cosa serve qui', 'Costo'],
    ['**Log**', 'Un evento puntuale, con un testo e degli attributi.',
     'Dire che cosa \u00e8 successo e perch\u00e9.', 'Proporzionale al volume; \u00e8 il pi\u00f9 caro '
     'da conservare.'],
    ['**Tracce**', 'La sequenza degli span di una richiesta attraverso i processi.',
     '**\u00c8 la risposta al problema posto**: correlare e misurare dove si \u00e8 speso il tempo.',
     'Contenibile con il campionamento.'],
    ['**Metriche**', 'Valori aggregati nel tempo (conteggi, durate, quantili).',
     'Accorgersi di un peggioramento prima della segnalazione.', 'Basso, se la '
     'cardinalit\u00e0 degli attributi resta bassa.'],
]

PARTI = [
    ['Parte', 'Che cosa fa', 'Dove vive'],
    ['**API**', 'L\u2019interfaccia che il codice chiama. Stabile e priva di implementazione.',
     'Nei moduli applicativi.'],
    ['**SDK**', 'L\u2019implementazione: campionamento, arricchimento, invio.',
     'Nei moduli, configurata dall\u2019esterno.'],
    ['**Agente**', 'Innesto automatico che strumenta Spring, JDBC e il client HTTP **senza '
     'modificare il codice**.', 'Si aggiunge all\u2019avvio della macchina virtuale Java.'],
    ['**Collector**', 'Riceve, filtra, riduce e inoltra. \u00c8 il punto in cui si cambia '
     'destinazione **senza toccare n\u00e9 ricompilare nulla**.', 'Un processo nel cluster.'],
]

PERIMETRO = [
    ['Unit\u00e0', 'Natura', 'Perch\u00e9 \u00e8 nel perimetro'],
    ['`all-ansc-sipo`', 'Pod nuovo', 'Orchestrazione verso ANSC, sessione, firma.'],
    ['`dec-ansc-sipo`', 'Pod nuovo', 'Dizionari.'],
    ['`be-numeratore-comunale`', 'Pod nuovo', 'Stacco del numero comunale.'],
    ['Processo di automazione', 'Pod nuovo', 'Letture e code.'],
    ['`statocivile-be`', 'Esistente', 'Anteprima, finalizzazione, definizione dell\u2019atto.'],
    ['`matrim-be`, `nascita-be`, `decessi-be`, `unioni-be`', 'Esistenti',
     'Le maschere da cui l\u2019atto si compila.'],
    ['`all-anpr-sipo`', 'Esistente', 'L\u2019altra met\u00e0 della catena, verso ANPR. **\u00c8 '
     'l\u2019unico modulo della catena senza alcun file di configurazione del log.**'],
    ['Micro-frontend Angular', 'Nuovi', 'Da l\u00ec parte l\u2019azione dell\u2019operatore.'],
    ['Front-end Thymeleaf', 'Esistenti', 'Le maschere di stato civile in esercizio.'],
]

LIVELLI = [
    ['Livello', 'Sev. OTel', 'Quando si usa', 'Chi se ne occupa'],
    ['`TRACE`', '1\u20134', 'Dettaglio minuto, utile solo mentre si cerca un difetto preciso. '
     '**Spento in produzione**, accendibile per singolo componente e per un tempo dichiarato.',
     'Chi sviluppa, su richiesta.'],
    ['`DEBUG`', '5\u20138', 'Passaggi interni che aiutano a capire una decisione del programma '
     '(quale caso d\u2019uso \u00e8 stato scelto e perch\u00e9). Spento in produzione.',
     'Chi sviluppa.'],
    ['`INFO`', '9\u201312', '**Il corso normale delle cose**, nei punti che hanno significato '
     'per il dominio: atto aperto, numero staccato, deposito riuscito. Non \u00e8 un diario di '
     'tutto ci\u00f2 che accade.', 'Nessuno, finch\u00e9 non serve.'],
    ['`WARN`', '13\u201316', 'Qualcosa non \u00e8 andato come previsto **ma il programma ha '
     'proseguito**: un tentativo riuscito al secondo colpo, una risposta lenta oltre soglia, '
     'una configurazione incompleta ma supplita.', 'Il supporto, in differita.'],
    ['`ERROR`', '17\u201320', '**L\u2019operazione dell\u2019utente non si \u00e8 compiuta.** '
     'Qualcuno deve guardarla: o si corregge un dato, o si corregge un programma.',
     'Il supporto, in giornata.'],
    ['`FATAL`', '21\u201324', 'Il componente non \u00e8 in grado di servire: credenziale '
     'scaduta, base dati irraggiungibile, configurazione assente all\u2019avvio.',
     'Il presidio, subito.'],
]

ORIGINI = [
    ['Codice', 'Che cosa indica', 'Esempio', 'A chi compete'],
    ['`FE`', 'Il difetto nasce nella presentazione: browser, pagina, chiamata non riuscita '
     'lato client.', 'Una chiamata fallita dopo tre tentativi.', 'Gruppo front-end.'],
    ['`BE`', 'Il difetto nasce nel nostro codice applicativo.',
     'Un\u2019eccezione non attesa nella costruzione del payload.', 'Gruppo back-end.'],
    ['`DB`', 'Il difetto nasce in Oracle: vincolo violato, blocco, esaurimento.',
     'Un deadlock sullo stacco del numero comunale.', 'Amministrazione della base dati.'],
    ['`ANSC`', 'La risposta negativa viene dal servizio nazionale di stato civile.',
     'HTTP 400 codice 400001 per un campo obbligatorio mancante.',
     'Funzionari, oppure Sogei se il difetto \u00e8 del servizio.'],
    ['`ANPR`', 'La risposta negativa viene dall\u2019anagrafe nazionale.',
     'Mutazione 5008 rifiutata.', 'Presidio ANPR.'],
    ['`INFRA`', 'Rete, Kubernetes, certificati, codice di sessione, risorse.',
     'Codice di sessione scaduto a met\u00e0 di una sequenza di firma.', 'Sistemisti.'],
    ['`CONF`', 'La configurazione \u00e8 incompleta o ambigua: non \u00e8 un difetto di programma.',
     'Due righe di configurazione applicabili allo stesso atto.',
     'Funzionari del Comune, dal back-office.'],
]

ATTRIBUTI = [
    ['Attributo', 'Obbligatorio', 'Valore'],
    ['`trace_id`, `span_id`', 'S\u00ec', 'Dal contesto; mai calcolati a mano.'],
    ['`service.name`', 'S\u00ec', 'Il nome del pod: `all-ansc-sipo`, `be-numeratore-comunale`\u2026'],
    ['`service.version`', 'S\u00ec', 'La versione rilasciata. **Senza, non si risponde a «da '
     'quando succede».**'],
    ['`deployment.environment`', 'S\u00ec', 'Produzione, preproduzione, collaudo.'],
    ['`cod_origine`', 'S\u00ec sugli eventi di livello WARN e oltre',
     'Uno dei sette valori della classificazione.'],
    ['`cod_evento`', 'S\u00ec sugli eventi di livello WARN e oltre',
     'Codice stabile e cercabile, non il testo del messaggio.'],
    ['Identificativi dei **tre piani**', 'Quelli noti in quel momento',
     'Atto (`id_atto_sipo`, `id_ansc`, `numero_atto`), allegati (`id_allegato`, '
     '`id_ansc_allegato`), soggetti (`id_soggetto_sipo`, `id_ansc_soggetto`, '
     '`id_scheda_anpr`, `id_unico_nazionale`). Tutti facoltativi.'],
    ['`utente`, `cod_postazione`', 'Quando c\u2019\u00e8 una sessione',
     'Chi stava operando e da dove.'],
]

REGISTRI = [
    ['Registro', 'A che cosa serve', 'Dove vive', 'Per quanto'],
    ['**Diagnostico**', 'Capire perch\u00e9 qualcosa non ha funzionato.',
     'Segnali OTel \u2192 destinazione scelta nel cap. «Dove si archivia».',
     'Giorni o settimane.'],
    ['**Di dominio**', 'Sapere che cosa \u00e8 successo all\u2019atto, in termini di mestiere.',
     'Eventi OTel con `cod_evento` e `id_atto_sipo`.', 'Mesi.'],
    ['**Audit probatorio**', 'Dimostrare che cosa \u00e8 stato mandato ad ANSC, da chi e quando.',
     '**`ANSC_LOG_AUDIT`, dov\u2019\u00e8 adesso.**', 'Secondo la regola di conservazione.'],
    ['**Accesso a dati personali**', 'Rispondere a chi chiede chi ha consultato una posizione.',
     'Registro separato, non in questo perimetro.', 'Secondo la norma.'],
]

AUDIT_NUOVE = [
    ['Colonna', 'Tipo', 'Perch\u00e9'],
    ['`TRACE_ID`', '`VARCHAR2(32 CHAR)`', '**\u00c8 l\u2019aggiunta che vale pi\u00f9 di tutte le '
     'altre**: lega la riga probatoria al racconto diagnostico. Da una riga di audit si apre '
     'la traccia, e viceversa.'],
    ['`SPAN_ID`', '`VARCHAR2(16 CHAR)`', 'Il passo preciso entro la traccia.'],
    ['`COD_SERVIZIO`', '`VARCHAR2(40 CHAR)`',
     'Quale processo ha scritto la riga. Oggi non si sa.'],
    ['`COD_VERSIONE_SW`', '`VARCHAR2(20 CHAR)`',
     'La versione del componente al momento del fatto.'],
    ['`ID_OPERAZIONE_COMUNE`', '`VARCHAR2(40 CHAR)`',
     'L\u2019identificativo che **ANSC stessa** usa per tracciare la chiamata: \u00e8 la chiave '
     'con cui si parla con Sogei quando si apre una segnalazione.'],
    ['`COD_ESITO_ANSC`', '`VARCHAR2(20 CHAR)`',
     'Il codice di errore restituito, distinto dall\u2019esito riuscito/fallito.'],
]

CONFRONTO = [
    ['Criterio', 'Oracle', 'Backend dedicato'],
    ['Infrastruttura nuova', '**Nessuna**: la base dati c\u2019\u00e8 gi\u00e0 ed \u00e8 presidiata.',
     'Un collector e uno store da installare e gestire.'],
    ['Esportatore pronto', '**No.** OpenTelemetry non ha un esportatore per Oracle: serve '
     'uno scarico su misura dal collector.', 'S\u00ec, nativo.'],
    ['Interrogazione', 'SQL, che il gruppo gi\u00e0 conosce.',
     'Linguaggio proprio dello strumento, da imparare.'],
    ['Vista a cascata della traccia', 'Da costruire noi \u2014 **\u00e8 il back-office proposto al '
     'cap. «Il back-office del supporto»**.', 'Gi\u00e0 pronta.'],
    ['Ricerca a testo libero', 'Debole senza indici dedicati.', 'Il suo mestiere.'],
    ['Costo di conservazione', 'Alto: spazio su base dati presidiata.',
     'Basso: archivi compressi e scadenza automatica.'],
    ['Dati personali', '**Restano dentro il perimetro della base dati del Comune.**',
     'Escono verso un altro sistema: va valutato.'],
    ['Passaggio futuro a strumenti specifici', 'Il codice **non cambia**: cambia la '
     'configurazione del collector.', 'Gi\u00e0 fatto.'],
]

VOLUMI = [
    ['Grandezza', 'Valore', 'Fonte'],
    ['Atti formati all\u2019anno', '**144.285**',
     'Ricognizione dei tipi atto citata in [R1].'],
    ['Eventi per atto, stima prudente', '20\u201340',
     'Dalla sequenza del cap. «Perch\u00e9 serve con i microservizi».'],
    ['Eventi all\u2019anno dalla sola formazione', '**3\u20136 milioni**', 'Prodotto dei due.'],
    ['Dimensione media di un evento', '0,5\u20131,5 KB', 'Con gli attributi, senza i payload.'],
    ['Spazio annuo stimato', '**2\u20139 GB**', 'Senza payload. Con richiesta e risposta '
     'per chiamata si moltiplica per dieci: \u00e8 la ragione per cui i payload restano '
     'sull\u2019audit e non nel registro diagnostico.'],
]

PAGINE_BO = [
    ['Pagina', 'A chi serve', 'Che cosa mostra'],
    ['**Errori e diagnostica**', 'Primo livello di supporto',
     'Gli eventi di livello WARN e oltre, filtrabili per periodo, origine, livello, servizio, '
     'codice. Ogni riga porta l\u2019identificativo di traccia.'],
    ['**Dettaglio della traccia**', 'Secondo livello, e chi sviluppa',
     'La cascata degli span in scala sui tempi, con gli eventi agganciati a ciascuno.'],
    ['Riepilogo per codice (proposta)', 'Chi coordina',
     'Conteggio per `cod_evento` e per origine sulle ultime ore: distingue il caso isolato dal '
     'difetto sistematico.'],
]

LIVELLI_CORR = [
    ['Livello', 'Chiave', 'A quale domanda risponde', 'Ampiezza', 'Durata'],
    ['**1 \u2014 tecnico**', '`trace_id` / `span_id`',
     '«Che cosa \u00e8 successo, passo per passo, in quell\u2019azione?»',
     'Una azione attraverso tutti i processi.', 'Secondi.'],
    ['**2 \u2014 di dominio**', 'I tre piani: atto, allegati, soggetti',
     '«Tutto quello che \u00e8 accaduto a questo atto, da quando \u00e8 stato aperto.»',
     'La vita dell\u2019oggetto lavorato.', 'Settimane o mesi.'],
    ['**3 \u2014 esterno**', '`idOperazioneComune` \u2194 `idOperazione`',
     '«Sogei dice che l\u2019operazione X \u00e8 fallita: qual era, da noi?»',
     'Il confine con i servizi nazionali.', 'Una chiamata.'],
]

PIANI = [
    ['Piano', 'Identificativi di tracciabilit\u00e0', 'Dove vivono'],
    ['**1 \u2014 Atto e pratica**',
     '`ID_ATTO_SIPO` \u00b7 `ID_ANSC` \u00b7 `NUMERO_ATTO` (numero comunale) \u00b7 '
     '`COD_MUNICIPIO` \u00b7 ufficiale e data',
     '`ANSC_STATO_ATTO`'],
    ['**2 \u2014 Allegati**',
     '`ID_ALLEGATO` \u00b7 `ID_ANSC_ALLEGATO` \u00b7 `ID_ATTO_SIPO` **quando c\u2019\u00e8**',
     '`MATR_USR.ALLEGATO`'],
    ['**3 \u2014 Intestatari e soggetti**',
     '`ID_SOGGETTO_SIPO` \u00b7 `ID_ANSC_SOGGETTO` \u00b7 `ID_SCHEDA_ANPR` \u00b7 '
     '`ID_UNICO_NAZIONALE`',
     '`ANSC_SOGGETTO_IDENTIFICATIVI`, e per i due codici ANPR `ANAG_USR.SOGGETTO`'],
]

RIEMPIMENTO = [
    ['Momento del percorso', 'Piano 1 \u2014 atto', 'Piano 2 \u2014 allegati',
     'Piano 3 \u2014 soggetti'],
    ['Apertura dell\u2019atto in SIPO', '`ID_ATTO_SIPO`', '\u2014', '\u2014'],
    ['Caricamento di un documento', '\u2014 **oppure** gi\u00e0 noto',
     '`ID_ALLEGATO`, poi `ID_ANSC_ALLEGATO` da R001', '\u2014'],
    ['Ricerca dei soggetti (R005)', 'invariato', '\u2014',
     '`ID_SOGGETTO_SIPO`, `ID_ANSC_SOGGETTO`, e i due codici ANPR se presenti'],
    ['Anteprima', '**+ `NUMERO_ATTO`**', 'invariato', 'invariato'],
    ['Validazione (R009)', '**+ `ID_ANSC`**', 'invariato', 'invariato'],
    ['Firme e definizione', 'invariato', 'invariato', 'invariato'],
]

ESTERNO = [
    ['', 'ANSC', 'ANPR'],
    ['Campo in richiesta', '`testataRichiesta.idOperazioneComune`',
     '`tipoTestataRichiesta.idOperazioneComune`'],
    ['Restituito in risposta', 'S\u00ec, `testataRisposta.idOperazioneComune`',
     'S\u00ec, `tipoTestataRisposta.idOperazioneComune`'],
    ['Identificativo del servizio', '`idOperazione`', '`idOperazioneANPR`'],
    ['Vincolo dichiarato', '`type: string`, **nessuna lunghezza massima**',
     'Alfanumerico, **massimo 30 caratteri**'],
    ['Che cosa ci mette SIPO oggi', 'Nulla: il componente non esiste ancora.',
     '`servizio + anno + sequenza`, e **`null`** se il chiamante non lo passa.'],
]

APERTI = [
    ['#', 'Questione', 'A chi spetta'],
    ['OT-01', '**La versione di Oracle in esercizio.** \u00c8 il punto che decide il capitolo '
     'sull\u2019archiviazione: con 23ai si usano le collezioni JSON native e la tracciatura '
     'dell\u2019SQL, con 19c si resta a SQL/JSON. Gli indizi nei sorgenti sono contraddittori: '
     '`ojdbc8` sta su 12c e oltre, ma due moduli dichiarano ancora `Oracle10gDialect`.',
     'Amministrazione della base dati'],
    ['OT-02', 'Che cosa offra gi\u00e0 il cluster: esiste un collector, un raccoglitore di '
     'metriche, una piattaforma di log dell\u2019ente? Non risulta da alcuna sorgente, e '
     'cambia il costo della proposta.', 'Sistemisti / Architettura'],
    ['OT-03', 'La regola di conservazione dei log diagnostici e di quelli di dominio.',
     'Responsabile della protezione dei dati'],
    ['OT-04', 'Chi gestisce il collector: il gruppo di SIPO o la piattaforma condivisa.',
     'Architettura'],
    ['OT-05', 'Se la telemetria di browser possa uscire dalla rete comunale e verso quale '
     'estremo. Se la risposta \u00e8 no, il front-end invia al proprio back-end e il collector '
     'resta interno.', 'Sicurezza'],
    ['OT-06', 'Se si debba **accendere l\u2019agente automatico** sui sette back-end esistenti '
     'o limitarsi alla propagazione del contesto. L\u2019agente d\u00e0 molto senza toccare il '
     'codice, ma aumenta il volume e va misurato prima.', 'Architettura / Referenti SIPO'],
    ['OT-07', 'Se i ventotto moduli il cui `logBack.xml` non \u00e8 caricato vadano sistemati in '
     'questa occasione o lasciati come sono. Finch\u00e9 restano cos\u00ec, qualunque modifica '
     'alla loro configurazione non ha effetto.', 'Referenti SIPO'],
    ['OT-08', 'Se ANSC accetti davvero un `idOperazioneComune` di 32 caratteri. Il contratto '
     'dichiara `type: string` **senza lunghezza massima**, ma l\u2019assenza di un vincolo nello '
     'schema non garantisce che il servizio in esercizio non ne applichi uno proprio. '
     'Da provare in preproduzione prima di adottare la forma estesa.', 'Presidio ANSC / Sogei'],
    ['OT-09', 'Se per ANPR si adotti la forma compatta in base 36 (25 caratteri entro i 30 '
     'ammessi) oppure si conservi la composizione attuale `servizio + anno + sequenza` '
     'aggiungendo la corrispondenza con la traccia in tabella. La prima \u00e8 pi\u00f9 diretta, '
     'la seconda non tocca i trentadue generatori.', 'Architettura / Referenti SIPO'],
]


def scrivi(d):
    # =============================================================== 1
    h(d, 1, 'Scopo del documento')
    par(d, 'Questo documento propone di adottare **OpenTelemetry** come impianto di '
           'registrazione per i componenti dell\u2019integrazione con ANSC e per la catena '
           'dell\u2019atto in SIPO. La proposta nasce da un\u2019osservazione del committente: '
           '**la tabella di log prevista oggi \u00e8 troppo semplice per sostenere la diagnosi '
           'dei difetti e il lavoro dei gruppi di supporto.** La verifica sui sorgenti '
           'conferma l\u2019osservazione e la estende, perch\u00e9 il problema non riguarda solo '
           'quella tabella.')
    par(d, 'Il documento guarda anche oltre l\u2019immediato: OpenTelemetry \u00e8 uno standard '
           'aperto, e adottarlo ora significa **poter passare domani a strumenti specifici '
           'senza riscrivere il codice che produce i dati**. \u00c8 la ragione principale per cui '
           'si propone uno standard invece di una soluzione.')

    h(d, 2, 'Perimetro e scelte gi\u00e0 compiute')
    par(d, 'Quattro decisioni sono state prese con il committente prima della stesura e '
           'delimitano il documento:')
    voce(d, 'Perimetro.', 'I quattro processi nuovi dell\u2019integrazione e i back-end di '
         'stato civile che partecipano alla catena dell\u2019atto, pi\u00f9 i front-end, sia i '
         'micro-frontend Angular nuovi sia le applicazioni Thymeleaf esistenti.')
    voce(d, 'Rapporto con l\u2019audit.', 'OpenTelemetry **affianca** `ANSC_LOG_AUDIT`, non la '
         'sostituisce: la tabella resta la traccia probatoria di ci\u00f2 che \u00e8 stato '
         'trasmesso ad ANSC, con la sua conservazione e la sua minimizzazione; i segnali '
         'coprono diagnosi e supporto. Due scopi, due cicli di vita.')
    voce(d, 'Oracle.', 'Preferenza, non vincolo. Il documento descrive la via Oracle con i '
         'suoi limiti reali e la via con un raccoglitore dedicato, e raccomanda.')
    voce(d, 'Front-end.', 'Trattati separatamente, perch\u00e9 il problema \u00e8 diverso: nelle '
         'applicazioni Thymeleaf la pagina la compone il server.')

    h(d, 2, 'Metodo e fonti')
    par(d, 'Lo stato di fatto \u00e8 stato misurato sui sorgenti, non desunto: ogni numero del '
           'capitolo seguente viene da un conteggio sui file del repository. La parte su '
           'OpenTelemetry viene dalla specifica pubblica [O1] e dalla raccomandazione W3C '
           '[O2]: \u00e8 metodologia, non evidenza interna, e come tale \u00e8 dichiarata. Le '
           'proposte \u2014 la classificazione, i livelli, le colonne nuove, il back-office \u2014 '
           'sono **nostre**, e il documento le distingue sempre da ci\u00f2 che \u00e8 standard.')

    h(d, 2, 'Glossario')
    tabella(d, GLOSSARIO, [1.5, 3.1, 1.9])

    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 4.3, 1.6])

    # =============================================================== 2
    h(d, 1, 'Lo stato di fatto')
    par(d, 'Prima di proporre conviene misurare. I numeri che seguono sono conteggi sui '
           'sorgenti [S1], non impressioni.')

    h(d, 2, 'Come SIPO registra oggi')
    tabella(d, STATO, [2.1, 0.8, 3.6])
    par(d, 'Due dettagli completano il quadro e si notano subito negli ambienti. '
           '`logging.file=c:/temp/my-log/app.log` compare in sette-otto moduli: \u00e8 un '
           'percorso Windows, inerte sotto Kubernetes. E `logging.level.com.zaxxer.hikari=TRACE` '
           'tiene il gestore delle connessioni al massimo dettaglio in altri sette, '
           'producendo volume senza che nessuno lo legga.')
    par(d, 'Il modulo `all-anpr-sipo` \u2014 il concentratore verso l\u2019anagrafe nazionale, '
           'cio\u00e8 met\u00e0 della catena dell\u2019atto \u2014 **non ha alcun file di '
           'configurazione del log.**')

    h(d, 2, 'Che cosa registra il registro di audit')
    par(d, 'La tabella prevista in [R1] ha nove colonne:')
    codice(d, [
        'CREATE TABLE ANSC_USR.ANSC_LOG_AUDIT (',
        '  ID_AUDIT          NUMBER GENERATED ALWAYS AS IDENTITY,',
        '  ID_STATO_ATTO     NUMBER,',
        '  FASE              VARCHAR2(20 CHAR) NOT NULL,   -- 12 valori ammessi',
        '  RICHIESTA         CLOB,                         -- IS JSON',
        '  RISPOSTA          CLOB,                         -- IS JSON',
        '  ESITO             VARCHAR2(20 CHAR),',
        '  DURATA_MS         NUMBER,',
        '  OPERATORE         VARCHAR2(40 CHAR),',
        '  TS_REGISTRAZIONE  TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
        '  CONSTRAINT FK_ANSC_LOG_AUDIT_STATO_ATTO',
        '    FOREIGN KEY (ID_STATO_ATTO) REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_STATO_ATTO)',
        ') TABLESPACE ANSC_USR;',
    ], 'Lo schema attuale, da [R1].')
    par(d, 'Per il mestiere che le \u00e8 proprio \u2014 conservare che cosa si \u00e8 mandato ad '
           'ANSC e con quale esito \u2014 **la tabella va bene**, e questo documento non propone '
           'di smantellarla. Per la diagnosi ha per\u00f2 quattro limiti strutturali.')
    tabella(d, AUDIT_LIMITI, [0.4, 1.9, 4.2])

    h(d, 2, 'Le cinque domande a cui oggi non si risponde')
    par(d, 'Il modo pi\u00f9 onesto di misurare una proposta \u00e8 elencare prima le domande che '
           'deve rendere rispondibili. Sono quelle che il supporto si sente porre.')
    tabella(d, DOMANDE, [2.6, 2.0, 1.9])

    # =============================================================== 3
    h(d, 1, 'Che cos\u2019\u00e8 OpenTelemetry')
    par(d, 'OpenTelemetry \u00e8 **una specifica e un insieme di librerie**, non un prodotto. '
           'Definisce come un programma produce dati di osservabilit\u00e0 e come questi '
           'viaggiano; **non li archivia e non li mostra**. Questa distinzione, che sembra una '
           'pedanteria, \u00e8 il motivo per cui conviene: ci\u00f2 che si scrive nel codice non '
           'dipende da dove i dati andranno a finire.')

    h(d, 2, 'I tre segnali')
    tabella(d, SEGNALI, [0.9, 1.9, 2.4, 1.3])
    par(d, 'Un avvertimento sull\u2019ordine delle priorit\u00e0. Il problema posto dal '
           'committente \u2014 diagnosi e supporto su pi\u00f9 processi \u2014 **lo risolvono le '
           'tracce, non i log.** Log senza identificativo di correlazione restano quello che '
           'sono oggi, solo in formato migliore. Perci\u00f2 la proposta mette le tracce al '
           'primo posto e i log al secondo, e le metriche per ultime.')

    h(d, 2, 'Il contesto che lega tutto')
    par(d, 'Ogni richiesta riceve un `trace_id`, e ogni passo entro la richiesta un `span_id`. '
           'Quando un processo ne chiama un altro, i due identificativi viaggiano in '
           'un\u2019intestazione HTTP normalizzata dal W3C [O2]:')
    codice(d, [
        'traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01',
        '             │  └── trace_id (32 cifre)        └── span_id      └── campionato',
        '             └── versione del formato',
    ], 'L\u2019intestazione che si propaga fra i processi.')
    par(d, '**Lo stesso `trace_id` finisce negli eventi di log**, ed \u00e8 questo \u2014 non il '
           'formato JSON, non lo strumento \u2014 a rendere ricostruibile una vicenda.')

    h(d, 2, 'Le quattro parti, e perch\u00e9 la separazione conta')
    tabella(d, PARTI, [1.0, 3.3, 2.2])
    par(d, 'La parte che decide la convenienza economica della proposta \u00e8 il **collector**. '
           'I moduli inviano sempre allo stesso indirizzo interno; dove i dati vadano poi \u2014 '
           'Oracle oggi, uno strumento specifico domani, entrambi per un periodo di '
           'sovrapposizione \u2014 si decide nella sua configurazione. \u00c8 la risposta concreta '
           'alla preoccupazione del committente sul «possibile passaggio verso tool '
           'specifici»: **quel passaggio non toccher\u00e0 il codice applicativo.**')

    # =============================================================== 4
    h(d, 1, 'Perch\u00e9 serve in un\u2019architettura a microservizi')

    h(d, 2, 'Il perimetro: undici unit\u00e0 e un servizio di terzi')
    tabella(d, PERIMETRO, [1.9, 1.0, 3.6])

    h(d, 2, 'Una formazione d\u2019atto vista come traccia')
    par(d, 'Si prenda l\u2019azione pi\u00f9 ordinaria: l\u2019operatore preme «VALIDA» su un atto '
           'di matrimonio. Quel gesto attraversa il micro-frontend, il concentratore, il '
           'numeratore e il servizio nazionale. Oggi produce righe in registri separati, '
           'ciascuno con il proprio orologio e nessun elemento che le colleghi. '
           'Con la propagazione del contesto diventa un oggetto solo:')
    figura(d, 'otel_bo_traccia.png', 6.1,
           'Figura 1 \u2014 Una traccia aperta nel back-office di supporto: la sequenza in '
           'scala sui tempi e gli eventi agganciati.')
    par(d, 'La figura mostra anche che cosa si guadagna oltre alla correlazione: **le durate**. '
           'Si legge che la risposta del servizio nazionale ha preso 1.460 millisecondi su '
           '2.180 totali, e che il numero comunale era gi\u00e0 stato staccato quando la '
           'validazione \u00e8 fallita \u2014 un\u2019informazione che cambia ci\u00f2 che il supporto '
           'deve fare dopo.')

    h(d, 2, 'Che cosa non risolve')
    par(d, 'Per onest\u00e0 della proposta, tre cose vanno dette. OpenTelemetry **non migliora '
           'i messaggi scritti male**: se il programma registra «errore», la traccia dir\u00e0 '
           'con precisione dove \u00e8 comparso «errore». **Non sostituisce la gestione delle '
           'eccezioni**: un difetto silenziato da un `catch` vuoto resta invisibile \u2014 e in '
           'SIPO ce n\u2019\u00e8 almeno uno documentato, sull\u2019allineamento verso ANPR. E **non '
           'copre ci\u00f2 che accade dentro ANSC**: la traccia si ferma al confine, dove resta '
           'solo l\u2019identificativo di operazione con cui si parla con Sogei.')

    # =============================================================== 5 (correlazione)
    h(d, 1, 'Il meccanismo di correlazione')
    par(d, 'In un\u2019architettura a pi\u00f9 processi la correlazione non \u00e8 un '
           'accessorio dell\u2019osservabilit\u00e0: **\u00e8 l\u2019osservabilit\u00e0**. '
           'Senza un filo che leghi le righe fra loro, raccogliere meglio significa soltanto '
           'avere pi\u00f9 righe da confrontare a mano.')
    par(d, 'Un livello solo per\u00f2 non basta, e conviene dirlo subito perch\u00e9 \u00e8 la '
           'specificit\u00e0 di questo dominio: **una traccia vive secondi, un atto vive '
           'settimane.** La formazione di un atto di matrimonio comincia con le pubblicazioni '
           'e finisce con la firma dell\u2019ufficiale, dopo la celebrazione: decine di azioni '
           'distinte, ciascuna con la propria traccia. Nessun `trace_id` le abbraccia.')

    h(d, 2, 'Tre livelli, tre domande')
    tabella(d, LIVELLI_CORR, [1.1, 1.6, 2.2, 1.4, 0.8])
    par(d, 'I tre livelli non sono alternativi: **convivono su ogni evento**, e sono i tre '
           'modi in cui il supporto arriva allo stesso fatto da punti di partenza diversi.')

    h(d, 2, 'Primo livello: la traccia')
    par(d, '\u00c8 il meccanismo descritto al capitolo «Che cos\u2019\u00e8 OpenTelemetry»: un '
           '`trace_id` per azione, uno `span_id` per passo, e l\u2019intestazione '
           '`traceparent` che li porta da un processo al successivo. Due regole lo reggono, e '
           'sono quelle che si violano pi\u00f9 spesso.')
    voce(d, 'La traccia nasce una volta sola.', 'Dove nasce l\u2019azione \u2014 nel browser '
         'per i micro-frontend, nel filtro del front-end per le applicazioni Thymeleaf, nel '
         'processo schedulato per i lavori notturni. **Mai pi\u00f9 a valle.**')
    voce(d, 'Si propaga sempre.', 'Anche sulle chiamate che non registrano nulla: una catena '
         'interrotta a met\u00e0 \u00e8 peggio di una assente, perch\u00e9 d\u00e0 '
         'l\u2019impressione di una vicenda completa.')
    par(d, 'Un difetto da prevenire: se un processo riceve una richiesta **senza** '
           '`traceparent` deve crearne uno e registrarlo come tale. Il silenzio \u00e8 la '
           'situazione in cui si perde la correlazione senza accorgersene.')

    h(d, 2, 'Secondo livello: i tre piani della tracciabilit\u00e0')
    par(d, 'Il primo livello risponde a «che cosa \u00e8 successo in quell\u2019azione». Il '
           'supporto per\u00f2 riceve domande di un\u2019altra forma: «questo atto \u00e8 fermo '
           'da tre giorni, perch\u00e9?», oppure «questo documento risulta caricato ma non lo '
           'troviamo da nessuna parte». Serve una chiave che duri quanto l\u2019oggetto.')
    par(d, 'Una chiave sola non basta, e la ragione \u00e8 di dominio prima che tecnica: **gli '
           'oggetti tracciabili sono tre, e vivono su piani indipendenti.** Un evento pu\u00f2 '
           'appartenere a uno, a due o a tutti e tre contemporaneamente.')
    tabella(d, PIANI, [1.5, 3.1, 1.9])
    par(d, '**Il secondo piano \u00e8 quello che rende insufficiente qualunque modello a chiave '
           'unica.** Un documento si carica, riceve il proprio identificativo locale e poi '
           'quello che ANSC gli assegna con R001, e **in quel momento pu\u00f2 non appartenere '
           'ad alcun atto**: l\u2019operatore acquisisce la documentazione prima, e la lega '
           'all\u2019atto dopo. Se la tracciabilit\u00e0 passasse da una sola chiave bisognerebbe '
           'scegliere \u2014 o l\u2019atto o l\u2019allegato \u2014 e nel caso del documento '
           'ancora libero non si potrebbe registrare nulla.')

    h(d, 3, 'Gli identificativi si riempiono per gradi')
    par(d, 'La seconda propriet\u00e0 da cui dipende il disegno: **dentro ciascun piano gli '
           'identificativi non arrivano tutti insieme.** L\u2019atto nasce con il solo '
           'identificativo di SIPO, guadagna il numero comunale all\u2019anteprima e '
           'l\u2019identificativo nazionale solo al deposito.')
    tabella(d, RIEMPIMENTO, [1.6, 1.5, 1.9, 1.5])
    par(d, 'Ne discende la regola per la libreria: **ogni evento porta gli identificativi noti '
           'in quel momento, tutti facoltativi, nessuno obbligatorio.** E la ricerca funziona '
           'per riconoscimento progressivo: si cerca per quello che si ha in mano \u2014 il '
           'numero comunale che l\u2019operatore legge a video, l\u2019identificativo nazionale '
           'che cita Sogei, il codice del documento che compare in un reclamo \u2014 e si '
           'arriva allo stesso insieme di eventi.')
    codice(d, [
        '-- la stessa vicenda, raggiunta da tre porte diverse',
        'SELECT TRACE_ID, TS_EVENTO, COD_LIVELLO, COD_ORIGINE, DESC_MESSAGGIO',
        '  FROM ANSC_USR.ANSC_LOG_EVENTO',
        ' WHERE ID_ATTO_SIPO     = :id_atto      -- piano 1, dalla maschera di SIPO',
        '    OR ID_ANSC          = :id_ansc      -- piano 1, da una segnalazione di Sogei',
        '    OR NUMERO_ATTO      = :num_comunale -- piano 1, da cio\' che l\'operatore legge',
        '    OR ID_ALLEGATO      = :id_allegato  -- piano 2, anche senza atto',
        '    OR ID_ANSC_SOGGETTO = :id_sogg_ansc -- piano 3, dal soggetto',
        ' ORDER BY TS_EVENTO;',
    ], 'Gli identificativi dei tre piani sono colonne distinte, non un campo unico '
       'polimorfo: \u00e8 ci\u00f2 che rende indicizzabile la ricerca.')

    h(d, 3, 'Una trappola di nomenclatura sul terzo piano')
    par(d, 'Sul piano dei soggetti i nomi sono insidiosi e vanno fissati nella libreria, '
           'altrimenti ogni gruppo ne user\u00e0 uno diverso. **Nel vocabolario di ANSC '
           '`idANPR` indica l\u2019identificativo unico nazionale**, cio\u00e8 '
           '`ID_UNICO_NAZIONALE`; la scheda anagrafica \u00e8 un\u2019altra cosa e si chiama '
           '`idsoggettoanpr`, cio\u00e8 `ID_SCHEDA_ANPR`. Sono **due** codici distinti, non uno '
           'con due nomi, e nel nostro modello hanno due colonne distinte. A ci\u00f2 si '
           'aggiunge `ID_ANSC_SOGGETTO`, che \u00e8 di ANSC e non c\u2019entra con ANPR.')
    par(d, 'La proposta \u00e8 di usare **sempre i nomi di colonna** negli attributi degli '
           'eventi, mai le forme dei contratti: sono gi\u00e0 disambiguati e sono quelli che '
           'chi fa assistenza ritrova in tabella.')

    h(d, 2, 'Terzo livello: il confine con i servizi nazionali')
    par(d, 'La traccia si ferma dove finisce il nostro perimetro. Oltre c\u2019\u00e8 Sogei, e '
           'la domanda che arriva da l\u00ec ha sempre la stessa forma: «l\u2019operazione X '
           '\u00e8 stata rifiutata». Trovare *quale* fosse, da noi, oggi \u00e8 un lavoro '
           'manuale.')
    par(d, '**La buona notizia \u00e8 che il meccanismo esiste gi\u00e0 in entrambi i '
           'contratti**, ed \u00e8 simmetrico:')
    tabella(d, ESTERNO, [1.6, 2.6, 2.7])
    par(d, 'Entrambi i servizi **restituiscono il nostro identificativo** e vi affiancano il '
           'proprio. Basta quindi una decisione: **far derivare `idOperazioneComune` dalla '
           'traccia**, invece di comporlo con una regola che non si lega a nulla.')
    codice(d, [
        '// ANSC: il contratto non dichiara lunghezza massima, la traccia entra com\'e\'',
        'testata.setIdOperazioneComune(contesto.traceId());',
        '//        -> "4bf92f3577b34da6a3ce929d0e0e4736"   (32 caratteri)',
        '',
        '// ANPR: alfanumerico, massimo 30 -> forma compatta in base 36, 25 caratteri',
        'testata.setIdOperazioneComune(contesto.traceIdCompatto());',
        '//        -> "3k7x9p2m4qr8vz1n6tb0ac5yd"          (25 caratteri, reversibile)',
        '',
        '// alla risposta si conserva la coppia: il nostro e il loro',
        'audit.setIdOperazioneComune(risposta.getTestataRisposta().getIdOperazioneComune());',
        'audit.setIdOperazioneAnsc (risposta.getTestataRisposta().getIdOperazione());',
    ], 'La conversione in base 36 di un identificativo a 128 bit occupa 25 caratteri: entra '
       'nei 30 ammessi da ANPR ed \u00e8 riconvertibile nella traccia di origine.')
    par(d, 'Oggi SIPO compone quel campo con `generateIdOperazioneComune`, che restituisce '
           '`servizio + anno + sequenza`; e se il chiamante non passa il parametro, **il campo '
           'parte a `null`**. Non \u00e8 un difetto da correggere con urgenza \u2014 funziona '
           '\u2014 ma \u00e8 un\u2019occasione sprecata: quel campo \u00e8 l\u2019unico ponte '
           'verso i registri di Sogei, e oggi non porta nulla che si possa ritrovare da noi.')

    h(d, 2, 'Che cosa si guadagna, in concreto')
    par(d, 'Quattro domande diventano rispondibili in una interrogazione invece che in una '
           'mattinata:')
    voce(d, 'Dal reclamo alla causa.', 'L\u2019operatore dice l\u2019ora e l\u2019atto; si '
         'apre la traccia e si legge la sequenza.')
    voce(d, 'Dall\u2019atto fermo alla ragione.', 'La chiave di dominio raccoglie tutte le '
         'azioni che lo hanno toccato, anche a settimane di distanza.')
    voce(d, 'Da Sogei a noi.', 'L\u2019identificativo che loro citano **\u00e8** la nostra '
         'traccia, o vi si riconduce.')
    voce(d, 'Da noi a Sogei.', 'Si apre una segnalazione citando `idOperazione`, che \u00e8 il '
         'loro, conservato accanto al nostro sull\u2019audit.')

    h(d, 2, 'Una cautela')
    par(d, 'Gli identificativi di correlazione **non sono dati personali e non devono '
           'diventarlo**: non vi si codifica il codice fiscale, il numero dell\u2019atto o '
           'altro di riconoscibile. Un identificativo opaco si pu\u00f2 scrivere nei log, '
           'mostrare all\u2019operatore e citare in una segnalazione a un terzo; uno che porti '
           'con s\u00e9 un dato della persona no. **\u00c8 la ragione per cui si usa la traccia '
           'e non il numero di pratica.**')

    # =============================================================== 6
    h(d, 1, 'I livelli di severit\u00e0 e la classificazione degli errori')
    par(d, 'Oggi in SIPO i livelli esistono come li usa chiunque usi SLF4J, ma **senza una '
           'regola dichiarata**: `INFO` e `DEBUG` si equivalgono nei fatti, e `com.zaxxer.hikari` '
           'sta a `TRACE` in sette moduli. Senza una convenzione un livello non vuol dire '
           'nulla, e filtrare per livello non serve.')

    h(d, 2, 'I livelli, e che cosa ciascuno impegna')
    par(d, 'La regola che si propone \u00e8 questa: **il livello non descrive la gravit\u00e0 del '
           'fatto, dichiara chi deve guardarlo e quando.** \u00c8 l\u2019unico criterio che rende '
           'il filtro utile al supporto.')
    tabella(d, LIVELLI, [0.8, 0.7, 3.3, 1.7])

    h(d, 2, 'La classificazione per origine')
    par(d, 'Il committente ha chiesto una classificazione degli errori del tipo back-end, '
           'front-end, Oracle. La si propone con sette valori, e con un criterio esplicito: '
           '**l\u2019origine non dice dove l\u2019errore \u00e8 comparso, dice a quale gruppo '
           'compete risolverlo.** \u00c8 una differenza che conta, perch\u00e9 un errore di '
           'configurazione si manifesta nel back-end ma lo risolve un funzionario, e un '
           'rifiuto di ANSC compare nel nostro codice ma nasce altrove.')
    tabella(d, ORIGINI, [0.7, 2.1, 2.3, 1.4])
    par(d, 'L\u2019origine si valorizza **nel punto in cui l\u2019errore si riconosce**, non in '
           'quello in cui si propaga: chi cattura una risposta negativa di ANSC la classifica '
           '`ANSC` anche se il codice che la cattura \u00e8 nostro.')

    h(d, 2, 'Gli attributi che ogni evento porta con s\u00e9')
    par(d, 'Un livello e un\u2019origine non bastano: perch\u00e9 il filtro funzioni servono '
           'attributi costanti, scritti sempre allo stesso modo. La convenzione proposta '
           'riusa i nomi standard dove esistono [O1] e ne aggiunge pochi nostri.')
    tabella(d, ATTRIBUTI, [1.8, 1.7, 3.0])
    par(d, '**`cod_evento` non \u00e8 il messaggio.** Il messaggio \u00e8 per chi legge e '
           'pu\u00f2 cambiare; il codice \u00e8 per chi cerca e non cambia mai. \u00c8 ci\u00f2 che '
           'permette di contare quante volte un difetto si \u00e8 ripetuto.')

    # =============================================================== 6
    h(d, 1, 'Le quattro famiglie di registro')
    par(d, 'Il committente ha chiesto di differenziare le tipologie di log. La distinzione che '
           'conta non \u00e8 di formato: \u00e8 di **scopo, destinatario e durata**. Confonderle '
           '\u00e8 ci\u00f2 che rende un registro inservibile per tutti e tre i mestieri.')
    tabella(d, REGISTRI, [1.3, 2.2, 2.0, 1.1])
    par(d, 'La riga che va protetta \u00e8 la terza. L\u2019audit probatorio ha una '
           'conservazione dettata da ragioni giuridiche e contiene i payload trasmessi, '
           'cio\u00e8 dati particolari; il registro diagnostico ha una vita breve e viene letto '
           'da chi fa assistenza. **Tenerli insieme costringerebbe a dare al primo la '
           'leggerezza del secondo, o al secondo la pesantezza del primo.**')

    h(d, 2, 'Che cosa non entra mai in un evento')
    par(d, 'Si registra **che** un dato era assente o malformato, non **quale** fosse. Il '
           'payload per esteso resta in `ANSC_LOG_AUDIT` e sull\u2019atto, dove la '
           'conservazione \u00e8 regolata. Negli eventi diagnostici non entrano codici fiscali, '
           'nomi, indirizzi, dati sanitari, n\u00e9 il codice di sessione o parti di esso. '
           'La libreria del cap. «La libreria di inserimento» **impedisce di sbagliare**, '
           'invece di affidarsi alla diligenza di chi scrive.')

    # =============================================================== 7
    h(d, 1, 'La revisione del registro di audit')
    par(d, 'Su richiesta del committente si propone anche come ampliare la tabella attuale. '
           'La proposta \u00e8 conservativa: **`ANSC_LOG_AUDIT` non cambia mestiere**, guadagna '
           'le colonne che la mettono in comunicazione con il mondo diagnostico.')

    h(d, 2, 'Le colonne da aggiungere')
    tabella(d, AUDIT_NUOVE, [1.7, 1.5, 3.3])
    par(d, 'Sono tutte aggiunte, nessuna modifica distruttiva: la tabella resta leggibile da '
           'chi gi\u00e0 la interroga.')

    h(d, 2, 'Il registro diagnostico, se la destinazione \u00e8 Oracle')
    par(d, 'Il quarto limite \u2014 la chiave esterna che lega ogni riga a un atto \u2014 non si '
           'risolve allargando la tabella, perch\u00e9 \u00e8 proprio quel legame a darle il suo '
           'valore probatorio. Si risolve **affiancandole un secondo registro** che non ha '
           'quel vincolo. I nomi seguono lo standard [R5].')
    codice(d, [
        'CREATE TABLE ANSC_USR.ANSC_LOG_EVENTO (',
        '  ID_EVENTO        NUMBER GENERATED ALWAYS AS IDENTITY,',
        '  TS_EVENTO        TIMESTAMP(6) WITH TIME ZONE NOT NULL,',
        '  TRACE_ID         VARCHAR2(32 CHAR),',
        '  SPAN_ID          VARCHAR2(16 CHAR),',
        '  COD_LIVELLO      VARCHAR2(10 CHAR) NOT NULL,',
        '  NUM_SEVERITA     NUMBER(2)         NOT NULL,   -- 1..24, scala OTel',
        '  COD_ORIGINE      VARCHAR2(10 CHAR),            -- FE BE DB ANSC ANPR INFRA CONF',
        '  COD_SERVIZIO     VARCHAR2(40 CHAR) NOT NULL,',
        '  COD_VERSIONE_SW  VARCHAR2(20 CHAR),',
        '  COD_AMBIENTE     VARCHAR2(10 CHAR),',
        '  COD_EVENTO       VARCHAR2(40 CHAR),',
        '  DESC_MESSAGGIO   VARCHAR2(1000 CHAR),',
        '  TXT_ATTRIBUTI    CLOB,',
        '  TXT_ECCEZIONE    CLOB,',
        '  -- piano 1: atto e pratica',
        '  ID_ATTO_SIPO     NUMBER,                       -- per valore, SENZA chiave esterna',
        '  ID_ANSC          VARCHAR2(50 CHAR),',
        '  NUMERO_ATTO      VARCHAR2(6 CHAR),',
        '  COD_MUNICIPIO    VARCHAR2(10 CHAR),',
        '  -- piano 2: allegati, che possono non appartenere ancora ad alcun atto',
        '  ID_ALLEGATO      NUMBER,',
        '  ID_ANSC_ALLEGATO VARCHAR2(15 CHAR),',
        '  -- piano 3: intestatari e soggetti',
        '  ID_SOGGETTO_SIPO NUMBER,',
        '  ID_ANSC_SOGGETTO VARCHAR2(50 CHAR),',
        '  ID_SCHEDA_ANPR   VARCHAR2(50 CHAR),',
        '  ID_UNICO_NAZIONALE VARCHAR2(50 CHAR),',
        '  --',
        '  UTENTE           VARCHAR2(40 CHAR),',
        '  COD_POSTAZIONE   VARCHAR2(40 CHAR),',
        '  CONSTRAINT PK_ANSC_LOG_EVENTO PRIMARY KEY (ID_EVENTO),',
        '  CONSTRAINT CK_ANSC_LOG_EVENTO_LIV',
        '    CHECK (COD_LIVELLO IN (\'TRACE\',\'DEBUG\',\'INFO\',\'WARN\',\'ERROR\',\'FATAL\')),',
        '  CONSTRAINT CK_ANSC_LOG_EVENTO_ORIG',
        '    CHECK (COD_ORIGINE IN (\'FE\',\'BE\',\'DB\',\'ANSC\',\'ANPR\',\'INFRA\',\'CONF\')),',
        '  CONSTRAINT CK_ANSC_LOG_EVENTO_ATTR CHECK (TXT_ATTRIBUTI IS JSON)',
        ')',
        'PARTITION BY RANGE (TS_EVENTO) INTERVAL (NUMTODSINTERVAL(1,\'DAY\'))',
        '  (PARTITION P_INIZIALE VALUES LESS THAN (TIMESTAMP \'2027-01-01 00:00:00 +00:00\'))',
        'TABLESPACE ANSC_USR;',
        '',
        'CREATE INDEX IX_ANSC_LOG_EVENTO_TRACE ON ANSC_USR.ANSC_LOG_EVENTO (TRACE_ID)',
        '  LOCAL TABLESPACE ANSC_USR;',
        'CREATE INDEX IX_ANSC_LOG_EVENTO_ATTO  ON ANSC_USR.ANSC_LOG_EVENTO (ID_ATTO_SIPO)',
        '  LOCAL TABLESPACE ANSC_USR;',
        'CREATE INDEX IX_ANSC_LOG_EVENTO_ANSC  ON ANSC_USR.ANSC_LOG_EVENTO (ID_ANSC)',
        '  LOCAL TABLESPACE ANSC_USR;',
        'CREATE INDEX IX_ANSC_LOG_EVENTO_ALLEG ON ANSC_USR.ANSC_LOG_EVENTO (ID_ALLEGATO)',
        '  LOCAL TABLESPACE ANSC_USR;',
        'CREATE INDEX IX_ANSC_LOG_EVENTO_SOGG  ON ANSC_USR.ANSC_LOG_EVENTO (ID_ANSC_SOGGETTO)',
        '  LOCAL TABLESPACE ANSC_USR;',
    ], 'Il registro diagnostico proposto. Tre scelte da notare, spiegate sotto.')
    voce(d, 'Nessuna chiave esterna, e i tre piani affiancati.', 'Gli identificativi sono '
         'riferimenti per valore, e i tre piani hanno colonne proprie. **\u00c8 la differenza '
         'che conta**: un documento caricato e non ancora legato a un atto, o un evento del '
         'front-end, devono poter essere registrati lo stesso. Le colonne sono tutte '
         'facoltative e si riempiono per gradi.')
    voce(d, 'Partizionata per giorno.', 'La scadenza diventa un\u2019operazione di '
         'amministrazione \u2014 si elimina una partizione \u2014 invece di una cancellazione di '
         'milioni di righe.')
    voce(d, 'Niente payload.', 'Richiesta e risposta restano sull\u2019audit. \u00c8 ci\u00f2 che '
         'tiene lo spazio nell\u2019ordine di grandezza stimato al cap. «Dove si archivia».')

    # =============================================================== 8
    h(d, 1, 'Dove si archivia e come si analizza')

    h(d, 2, 'La via Oracle, e il suo limite vero')
    par(d, 'Il committente chiede, se possibile, di restare su Oracle. Si pu\u00f2, e il '
           'vantaggio \u00e8 reale: nessuna infrastruttura nuova, i dati restano nel perimetro '
           'della base dati del Comune, e il gruppo interroga in SQL, che gi\u00e0 conosce.')
    par(d, 'Il limite va per\u00f2 detto con chiarezza, perch\u00e9 non \u00e8 un dettaglio: '
           '**OpenTelemetry non ha un esportatore per Oracle.** Nessuno dei componenti '
           'pronti scrive su una base dati relazionale. Per portarci i segnali servono un '
           'collector e **uno scarico scritto da noi** \u2014 poche centinaia di righe, non un '
           'progetto, ma un pezzo su misura da mantenere. Chiunque proponga questa via senza '
           'dirlo sta nascondendo un costo.')
    par(d, 'Un esempio di che cosa si ottiene, una volta che i dati sono in tabella:')
    codice(d, [
        '-- la vicenda completa di una azione, nell\'ordine in cui e\' accaduta',
        'SELECT TS_EVENTO, COD_LIVELLO, COD_ORIGINE, COD_SERVIZIO, COD_EVENTO, DESC_MESSAGGIO',
        '  FROM ANSC_USR.ANSC_LOG_EVENTO',
        ' WHERE TRACE_ID = \'4bf92f3577b34da6a3ce929d0e0e4736\'',
        ' ORDER BY TS_EVENTO;',
        '',
        '-- i difetti sistematici delle ultime ore: caso isolato o no?',
        'SELECT COD_ORIGINE, COD_EVENTO, COUNT(*) AS QUANTI,',
        '       COUNT(DISTINCT ID_ATTO_SIPO) AS ATTI_COINVOLTI',
        '  FROM ANSC_USR.ANSC_LOG_EVENTO',
        ' WHERE TS_EVENTO > SYSTIMESTAMP - INTERVAL \'6\' HOUR',
        '   AND NUM_SEVERITA >= 17',
        ' GROUP BY COD_ORIGINE, COD_EVENTO',
        ' ORDER BY QUANTI DESC;',
        '',
        '-- dall\'atto alla diagnosi, e viceversa: il salto che oggi non esiste',
        'SELECT a.FASE, a.ESITO, a.DURATA_MS, e.COD_LIVELLO, e.DESC_MESSAGGIO',
        '  FROM ANSC_USR.ANSC_LOG_AUDIT  a',
        '  LEFT JOIN ANSC_USR.ANSC_LOG_EVENTO e ON e.TRACE_ID = a.TRACE_ID',
        ' WHERE a.ID_STATO_ATTO = :id_atto',
        ' ORDER BY a.TS_REGISTRAZIONE, e.TS_EVENTO;',
    ], 'Le tre interrogazioni che coprono la gran parte delle richieste al supporto.')

    h(d, 2, 'La via con un raccoglitore dedicato')
    par(d, 'L\u2019alternativa \u00e8 la configurazione per cui OpenTelemetry \u00e8 pensato: un '
           'collector e uno store dei segnali. Si ottengono subito la vista a cascata, la '
           'ricerca a testo libero e la scadenza automatica, senza scrivere nulla; si '
           'introducono per\u00f2 componenti da installare, aggiornare e presidiare, e i dati '
           'escono dalla base dati del Comune.')

    h(d, 2, 'Confronto e raccomandazione')
    tabella(d, CONFRONTO, [1.5, 2.6, 2.4])
    par(d, '**La raccomandazione \u00e8 di strumentare subito e decidere la destinazione dopo.** '
           'Non \u00e8 un rinvio: \u00e8 esattamente ci\u00f2 che la separazione fra codice e '
           'collector rende possibile, ed \u00e8 il principale argomento a favore di uno '
           'standard. Si parte con Oracle come destinazione \u2014 nessuna infrastruttura '
           'nuova, nessuna uscita di dati, il back-office del cap. seguente come interfaccia '
           '\u2014 e se il volume o il bisogno di ricerca lo richiederanno, si aggiunge un '
           'secondo esportatore nel collector **senza toccare una riga di codice '
           'applicativo**.')
    par(d, 'Una condizione: la via Oracle va dimensionata prima, non dopo. La scelta '
           'dipende anche da **OT-01**, la versione in esercizio.')

    h(d, 2, 'Volumi e conservazione')
    tabella(d, VOLUMI, [2.0, 1.4, 3.1])
    par(d, 'La conservazione proposta \u00e8 differenziata: **trenta giorni** per il registro '
           'diagnostico, **dodici mesi** per gli eventi di dominio, e per l\u2019audit la regola '
           'gi\u00e0 stabilita. Il valore esatto \u00e8 **OT-03**.')

    # =============================================================== 9
    h(d, 1, 'La libreria di inserimento')

    h(d, 2, 'Perch\u00e9 una libreria e non una convenzione')
    par(d, 'Una convenzione scritta in un documento viene applicata finch\u00e9 qualcuno la '
           'ricorda. Con undici unit\u00e0 e pi\u00f9 gruppi di lavoro non regge: i nomi degli '
           'attributi divergono, qualcuno dimentica l\u2019origine, qualcuno scrive un codice '
           'fiscale nel messaggio. **La libreria rende la cosa giusta anche la pi\u00f9 '
           'comoda**, ed \u00e8 l\u2019unico modo perch\u00e9 i campi siano davvero costanti.')
    par(d, 'Il punto di partenza esiste gi\u00e0: `logstash-logback-encoder` \u00e8 dichiarato in '
           'nove `pom.xml` e usato da `common/profilazione-utente` [S2]. La libreria proposta '
           'ne raccoglie la direzione invece di aprirne un\u2019altra.')

    h(d, 2, 'Che cosa fa, e che cosa non deve fare')
    voce(d, 'Apre e chiude il contesto.', 'Un filtro legge l\u2019intestazione `traceparent`, '
         'o ne crea una se manca, e mette identificativi, utente e postazione nel contesto '
         'per il tempo della richiesta.')
    voce(d, 'Arricchisce ogni evento.', 'Servizio, versione, ambiente e identificativi si '
         'aggiungono **da s\u00e9**: chi scrive un log non deve ricordarsene.')
    voce(d, 'Offre un\u2019interfaccia per gli eventi classificati.',
         'Dove serve origine e codice, l\u2019API li rende obbligatori.')
    voce(d, 'Protegge.', 'Oscura i valori riconducibili a persone e rifiuta di registrare il '
         'codice di sessione.')
    voce(d, 'Non decide la destinazione.', 'La libreria produce; dove i dati vadano lo stabilisce '
         'la configurazione. **\u00c8 il vincolo che tiene aperta la porta agli strumenti '
         'specifici.**')

    h(d, 2, 'Esempi d\u2019uso')
    par(d, 'Il primo caso \u00e8 il pi\u00f9 importante, perch\u00e9 riguarda le migliaia di punti '
           'di registrazione che esistono gi\u00e0: **non cambiano.**')
    codice(d, [
        '// 1 — I punti di log esistenti restano come sono.',
        'private static final Logger log = LoggerFactory.getLogger(DepositoService.class);',
        '',
        'log.error("Deposito non riuscito", e);',
        '',
        '// La libreria aggiunge da se\': trace_id, span_id, service.name, service.version,',
        '// deployment.environment, utente, cod_postazione, id_atto_sipo.',
        '// Nessuna modifica ai 4.781 punti che gia\' chiamano un logger.',
    ], 'Il caso ordinario: si guadagna il contesto senza toccare il codice.')
    par(d, 'Il secondo caso \u00e8 l\u2019evento classificato, da usare dove il supporto dovr\u00e0 '
           'cercare:')
    codice(d, [
        '// 2 — Un evento che il supporto dovra\' poter trovare e contare.',
        'registro.evento(Origine.ANSC, "ANSC-400001")',
        '        .messaggio("Campo obbligatorio mancante nel payload")',
        '        .atto(idAttoSipo)                   // piano 1: aggiunge anche idAnsc e numero',
        '        .soggetto(idSoggettoSipo)           // piano 3: aggiunge i codici ANSC e ANPR',
        '        .attributo("cod_uc", "311111")',
        '        .attributo("campo", "evento.datiEventoMatrimonio.numeroTestimoni")',
        '        .errore(e)',
        '        .registra();                       // livello ERROR implicito',
        '',
        '// 3 — Un\'attenzione: e\' andata bene, ma qualcuno deve saperlo.',
        'registro.evento(Origine.INFRA, "INFRA-OTP-SCAD")',
        '        .messaggio("Codice di sessione rigenerato a meta\' sequenza")',
        '        .atto(idAttoSipo)',
        '        .livello(Livello.WARN)',
        '        .registra();',
    ], 'L\u2019API esplicita: origine e codice sono obbligatori, il resto \u00e8 facoltativo.')
    par(d, 'Il terzo caso delimita un passo, perch\u00e9 se ne misuri la durata e perch\u00e9 gli '
           'eventi interni gli si aggancino:')
    codice(d, [
        '// 4 — Delimitare un passo: entra nella cascata della traccia.',
        'try (var passo = registro.passo("costruzione-payload")) {',
        '    passo.attributo("cod_uc", uc);',
        '    var payload = costruttore.costruisci(atto, configurazione);',
        '    passo.esito(Esito.OK);',
        '    return payload;',
        '}                                           // durata e chiusura automatiche',
        '',
        '// 5 — Il dato personale non passa: la libreria impedisce di sbagliare.',
        'registro.evento(Origine.BE, "SOGGETTO-NON-TROVATO")',
        '        .messaggio("Intestatario non trovato in ANSC")',
        '        .riservato("codice_fiscale", cf)   // oscurato: RSSMRA****",',
        '        .registra();',
    ], 'La delimitazione di un passo e il trattamento dei dati personali.')

    h(d, 2, 'L\u2019innesto nei moduli')
    par(d, 'Tre interventi, e il primo da solo d\u00e0 gi\u00e0 la correlazione:')
    codice(d, [
        '<!-- a) la dipendenza, una riga per modulo -->',
        '<dependency>',
        '  <groupId>it.romaCapitale.sipo</groupId>',
        '  <artifactId>osservabilita-sipo</artifactId>',
        '</dependency>',
        '',
        '<!-- b) il pattern con i campi di contesto: oggi NESSUN modulo li ha -->',
        '<pattern>%d{ISO8601} %-5level [%X{trace_id}/%X{span_id}] %X{cod_servizio}',
        '         %logger{36} - %msg%n</pattern>',
        '',
        '<!-- c) in alternativa al pattern, l\'uscita strutturata gia\' disponibile -->',
        '<encoder class="net.logstash.logback.encoder.LogstashEncoder"/>',
    ], 'Da aggiungere nei `logBack.xml`. Nei 28 moduli che non dichiarano '
       '`logging.config` la modifica **non avrebbe effetto**: vedi OT-07.')

    # =============================================================== 10
    h(d, 1, 'Il back-office del supporto')
    par(d, 'I dati raccolti servono a qualcuno solo se quel qualcuno li raggiunge. Oggi '
           'leggere i log significa accedere ai processi del cluster, il che **esclude dalla '
           'diagnosi chiunque non sia sistemista** \u2014 e il primo livello di supporto non lo '
           '\u00e8. Si propongono perci\u00f2 due pagine, nello stile e nel registro delle pagine '
           'del back-office gi\u00e0 disegnato [R2].')
    tabella(d, PAGINE_BO, [1.7, 1.5, 3.3])

    h(d, 2, 'La worklist degli errori')
    figura(d, 'otel_bo_errori.png', 6.1,
           'Figura 2 \u2014 Errori e diagnostica: il primo livello di supporto filtra per '
           'origine, livello e servizio, e da ogni riga passa alla traccia.')
    par(d, 'La colonna **Origine** precede il servizio di proposito: \u00e8 la classificazione '
           'che smista la segnalazione al gruppo giusto, mentre il servizio dice soltanto '
           'quale processo ha scritto la riga. Si noti la riga senza numero di atto: \u00e8 un '
           'errore del front-end, e **oggi non avrebbe dove essere registrato**.')

    h(d, 2, 'Il dettaglio della traccia')
    par(d, 'La seconda pagina \u00e8 la Figura 1. Da l\u00ec si salta all\u2019atto, e dall\u2019atto '
           'si torna alla traccia: \u00e8 il legame che la colonna `TRACE_ID` aggiunta '
           'all\u2019audit rende possibile.')

    h(d, 2, 'Le tabelle sottese')
    par(d, 'Entrambe le pagine leggono `ANSC_LOG_EVENTO` e, per il raccordo con l\u2019atto, '
           '`ANSC_LOG_AUDIT` e `ANSC_STATO_ATTO`. **In sola lettura**: il back-office di '
           'supporto non scrive e non corregge nulla. Le abilitazioni seguono il registro '
           'delle pagine di [R2]; il livello di dettaglio visibile \u00e8 **OT-05**, perch\u00e9 '
           'gli attributi possono contenere riferimenti a persone.')

    # =============================================================== 11
    h(d, 1, 'Il front-end')
    par(d, 'I due mondi vanno trattati separatamente, perch\u00e9 il problema \u00e8 diverso.')

    h(d, 2, 'I micro-frontend Angular')
    par(d, '\u00c8 il caso in cui la telemetria di browser d\u00e0 di pi\u00f9: la pagina vive nel '
           'client, le chiamate partono da l\u00ec, e **l\u2019azione dell\u2019operatore comincia '
           'l\u00ec**. Perch\u00e9 la traccia sia completa, il contesto deve nascere nel browser e '
           'viaggiare verso il back-end.')
    codice(d, [
        '// libreria condivisa dei micro-frontend: si configura una volta sola',
        'registerInstrumentations({',
        '  instrumentations: [new DocumentLoadInstrumentation(),',
        '                     new XMLHttpRequestInstrumentation({',
        '                       propagateTraceHeaderCorsUrls: [/\\/ansc\\/v1\\//]})],',
        '});',
        '',
        '// un evento di dominio dal front-end',
        'registro.evento(Origine.FE, \'FE-CHIAMATA-KO\')',
        '        .messaggio(\'Chiamata a /ansc/v1/atti fallita dopo 3 tentativi\')',
        '        .attributo(\'stato_http\', String(err.status))',
        '        .registra();',
    ], 'L\u2019innesto nella libreria condivisa [R3]: i singoli micro-frontend non la '
       'configurano.')
    par(d, '`propagateTraceHeaderCorsUrls` va **limitato ai nostri domini**. Senza quel '
           'filtro il browser aggiungerebbe l\u2019intestazione anche a chiamate verso terzi, '
           'che \u00e8 una perdita di informazione e un rischio inutile.')

    h(d, 2, 'I front-end Thymeleaf')
    par(d, 'Qui il guadagno \u00e8 minore e il costo pure, perch\u00e9 **la pagina la compone il '
           'server**: il browser riceve HTML gi\u00e0 fatto e non ha quasi logica propria. Non '
           'si propone telemetria di browser sulle trentacinque applicazioni esistenti. Si '
           'propone invece la sola cosa che serve: **che il contesto nasca nel front-end e '
           'arrivi al back-end**, cos\u00ec che una pagina e le chiamate che ne derivano stiano '
           'nella stessa traccia.')
    codice(d, [
        '// un filtro nel modulo comune CommonWeb: vale per tutti e 35 i front-end',
        'public class ContestoFilter implements Filter {',
        '  public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {',
        '    try (var ctx = registro.apriContesto(req)) {   // crea o eredita il traceparent',
        '      chain.doFilter(req, res);',
        '    }                                              // chiude e ripulisce l\'MDC',
        '  }',
        '}',
    ], 'Un solo punto di innesto, in `CommonWeb`, da cui dipendono tutti i front-end.')
    par(d, '**\u00c8 la via meno invasiva possibile**: un filtro in un modulo condiviso, nessuna '
           'modifica alle pagine, nessun rilascio delle singole applicazioni oltre a quello '
           'della libreria comune.')

    # =============================================================== 12
    h(d, 1, 'Il percorso di adozione')
    par(d, 'Quattro gradini. Il primo d\u00e0 un risultato utile da solo, ed \u00e8 la condizione '
           'perch\u00e9 gli altri abbiano senso.')
    voce(d, 'Primo \u2014 il contesto.', 'La libreria, il filtro, i campi nel pattern e le due '
         'colonne `TRACE_ID`/`SPAN_ID` sull\u2019audit. **Da qui in poi le righe si legano fra '
         'loro**, anche restando dove sono oggi. Riguarda i quattro pod nuovi e `CommonWeb`.')
    voce(d, 'Secondo \u2014 i livelli e la classificazione.', 'Si adottano i sei livelli con la '
         'loro regola e le sette origini; si ripuliscono i difetti rilevati, fra cui il '
         'percorso Windows e il gestore delle connessioni a `TRACE`.')
    voce(d, 'Terzo \u2014 il registro e il back-office.', '`ANSC_LOG_EVENTO`, lo scarico dal '
         'collector e le due pagine. **\u00c8 il gradino che consegna il risultato al '
         'supporto**, e fino a qui non serve alcuna infrastruttura oltre al collector.')
    voce(d, 'Quarto \u2014 le tracce complete e le metriche.', 'L\u2019agente automatico sui '
         'back-end esistenti e le poche metriche che contano. Si valuta qui, con i volumi '
         'veri in mano, se la destinazione debba restare Oracle.')

    # =============================================================== 13
    h(d, 1, 'Punti aperti')
    par(d, 'Sette questioni. La prima decide il capitolo sull\u2019archiviazione e va chiusa '
           'per prima; le altre non impediscono di cominciare dal primo gradino.')
    tabella(d, APERTI, [0.8, 4.4, 1.4])


def intesta(d):
    for r in d.tables[0].rows:
        if len(r.cells) < 2:
            continue
        etichetta = r.cells[0].text.strip().lower()
        valore = {'progetto': 'SIPO \u2014 Integrazione con ANSC',
                  'data consegna': DATA}.get(etichetta)
        if valore:
            D.riscrivi_cella(r.cells[1], valore)
    for fatto in D.frontespizio(d, '0.1',
                                'PROPOSTA_Osservabilita-OpenTelemetry_v0.1'):
        print('  ' + fatto)
    storia = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for r in list(storia.rows[1:]):
        if not any(c.text.strip() for c in r.cells):
            r._tr.getparent().remove(r._tr)
    D.storia(d, DATA, '0.1', 'Tutti',
             'Prima stesura. Proposta di adottare OpenTelemetry per i quattro processi '
             'dell\u2019integrazione, i back-end della catena dell\u2019atto e i front-end. '
             'Stato di fatto misurato sui sorgenti. Sei livelli di severit\u00e0 con la regola '
             'd\u2019uso e sette origini di errore con il gruppo che vi compete. Quattro '
             'famiglie di registro, con l\u2019audit probatorio che resta dov\u2019\u00e8. Colonne '
             'nuove su ANSC_LOG_AUDIT e nuovo registro diagnostico ANSC_LOG_EVENTO. '
             'Confronto fra archiviazione su Oracle e raccoglitore dedicato, con '
             'raccomandazione di strumentare subito e decidere la destinazione dopo. '
             'Libreria di inserimento con esempi d\u2019uso, due pagine di back-office per il '
             'supporto, trattamento separato dei front-end Angular e Thymeleaf. '
             'Capitolo dedicato al meccanismo di correlazione su tre livelli \u2014 traccia, '
             'oggetto lavorato, confine con i servizi nazionali \u2014 con la derivazione '
             'di idOperazioneComune dalla traccia. Nove punti aperti OT-01\u2026OT-09.')


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
