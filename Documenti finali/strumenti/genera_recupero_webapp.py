# -*- coding: utf-8 -*-
"""Genera la v0.1 di «ANALISI_Recupero-Atti-WebApp_SIPO-ANSC» (10/11/2026).

Richiesta dell'utente: le strategie di integrazione per gli atti redatti con la web app ANSC che
devono essere recuperati in SIPO; il numero comunale è comunque prodotto in SIPO, il problema è
che cosa succede dopo. Dal template DAD, come gli altri documenti di analisi.

Fatti (tre ricognizioni del 10/11, controlli a campione):
  * ANSC: R005 ha 7 operazioni POST; criteri dell'evento (11): idAnsc, idComunale («Numero
    Comunale dell'Atto (codificato ANPR_03)», ambiguo), idEvento, tipo evento e contenuto,
    dataDa/dataA (quale data non è detto), eventoSorgente, flagRettifica, idComuneRegistrazione;
    nessun criterio di stato, canale o data di modifica. Il canale di formazione non è nel
    modello (nomeApplicativo solo in testata della richiesta; operatore* deprecati). Nessun
    push per gli atti propri. PDF: R010 vuole l'intero ModelEvento (presaVisione solo
    CONFERMATO), R002 estratti con firma. Annotazioni con idtipocontenuto=0 (1.41.2, non
    documentato). La web app suggerisce «l'ultimo numero già usato» (1.18.4) e limita il numero
    a 5 caratteri (1.20.0); nessun controllo di unicità documentato. Comunicazioni anagrafiche:
    predisposte da ANSC e notificate all'anagrafe tramite ANPR (servizio 4005); SIPO non le tratta.
  * SIPO: nessun canale crea MATR_USR.ATTO dall'esterno; /finalizzaAtto fa IntegrazioneATTO,
    allineamento ANPR (2001/1001/5008…), formulario con annotazioni contestuali, PDF in
    ATTO_SCANSIONATO, comunicazioni di trascrizione; le annotazioni di SIPO legano MATR_USR e
    ANAG_USR per estremi identici (NUMERO, ANNO, PARTE_SERIE, ESPONENTE, AREA); ricerche per
    estremi con serie ed esponente in uguaglianza stretta; colonne ANSC su ANAG_USR.ATTO scritte
    solo da maschere, dalla 3002 e dalle notifiche ANPR; corpi PL/SQL e viste non fra le sorgenti.
  * Documenti: aggancio e stacco del numero (analisi [R1]), pagine di recupero (testo libero
    [R2]), riallineamento (annullamento [R3]), instradamento della certificazione [R4], OP-79.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_recupero_webapp.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import testo, h, par, voce, tabella, figura   # noqa: E402
import diagrammi_recupero   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(QUI))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
NOME = 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.1'
OUT = os.path.join(BASE, 'Documenti finali', NOME + '.docx')
TAGLIA_DA = 29
DATA = '10/11/2026'


def costruisci():
    shutil.copyfile(TEMPLATE, OUT)
    d = docx.Document(OUT)
    body = d.element.body
    for ch in list(body.iterchildren())[TAGLIA_DA:]:
        if ch.tag != qn('w:sectPr'):
            body.remove(ch)
    for p in d.paragraphs:
        if '“Lorem Ipsum”' in p.text:
            testo(p, '“Integrazione SIPO – ANSC”')
        elif p.style.name == 'Subtitle':
            testo(p, 'Gli atti formati sulla web app ANSC: come riportarli in SIPO e che cosa '
                     'succede dopo')
    return d


# =================================================================== tabelle
RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[R1]', 'ANALISI_Integrazione-ANSC (versione corrente) — capitoli «SIPO in relazione alla '
     'web app ANSC» (l’aggancio, lo stacco del numero), «La numerazione comunale», '
     'ANSC_STATO_ATTO, registro degli Open Point.', 'Documento di progetto'],
    ['[R2]', 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.5 — le pagine «Recupero Atto ANSC» e '
     '«Riepilogo Atto ANSC», i punti aperti TL.', 'Documento di progetto'],
    ['[R3]', 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.3 — il riallineamento '
     'da ANSC.', 'Documento di progetto'],
    ['[R4]', 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.1 — l’instradamento per atto.',
     'Documento di progetto'],
    ['[R5]', 'PROCESSO_Numerazione-Comunale_SIPO-ANSC_v0.5 e ansc-numerazione-v1.yaml 1.2.0 — '
     'be-numeratore-comunale.', 'Documento di progetto'],
    ['[R6]', 'STUDIO_Identificativi-ANSC-verso-ANPR_v0.4 — le colonne ANSC di ANAG_USR.ATTO e '
     'la catena verso ANPR.', 'Documento di progetto'],
    ['[R7]', 'DISEGNO_Back-Office_ANSC (versione corrente) — supervisione, riconciliazione, '
     'numerazione.', 'Documento di progetto'],
    ['[A1]', 'ansc/docs/openapi: R005_consultazione_ansc.yaml 1.4.0, R010_anteprima.yaml, '
     'R001, R002, R003, R008, R009, model_evento.yaml, base_servizi.yaml.', 'Contratti ANSC'],
    ['[A2]', 'ansc/docs/Changelog.md — versioni citate nel testo.', 'Sorgente ANSC'],
    ['[A3]', 'Comunicazione ANSC sui casi d’uso di servizio (Sorgenti Documentali/'
     'Comunicazione_ANSC_Casi-uso-servizio_servizi-cooperativi.txt).', 'Comunicazione ANSC'],
    ['[A4]', 'Guida operativa ANSC; nota «Flusso conferma»; anpr-9.2.9 (servizio 4005, '
     'predisposizione anagrafica).', 'Documentazione ANSC e ANPR'],
    ['[S1]', 'Codice SIPO: statocivile-be (AnteprimaAttoController, InitFlow, ImplFlow, '
     'PropostaAnnotazioneController), decessi-be, nascita-be, matrim-be, unioni-be, '
     'cittadinanza-be, anagrafe-entities (Atto, AttoAnscBL), matrim-entities (AttoMatr), '
     'all-anpr-sipo; Disegno Base Dati di MATR_USR.', 'Sorgente applicativo'],
]

GLOSSARIO = [
    ['Termine', 'Significato'],
    ['Atto formato sulla web app', 'Atto di stato civile che l’ufficiale di Roma ha validato e '
     'firmato direttamente sulla web app di ANSC, con un numero comunale staccato in SIPO.'],
    ['Recupero', 'Il riportare in SIPO un atto formato sulla web app, al livello di presenza '
     'scelto.'],
    ['Livello di presenza', 'Quanto dell’atto si scrive in SIPO: L0 il numero, L1 il '
     'riferimento, L2 la scheda essenziale, L3 l’importazione completa.'],
    ['Riallineamento', 'La rilettura di un atto già recuperato, per riportare in SIPO ciò che è '
     'cambiato in ANSC.'],
    ['Canale di formazione', 'Da dove è stato formato l’atto: SIPO o web app. ANSC non lo '
     'registra; lo deve registrare SIPO.'],
]

CASI = [
    ['Caso', 'Perché l’atto nasce sulla web app', 'Frequenza attesa'],
    ['Dichiarazione a testo libero o senza caso d’uso applicabile', 'I casi d’uso di servizio '
     'delle dichiarazioni non sono cooperativi dal 09/09/2024 [A3]: solo web app.',
     'Rara, ma strutturale.'],
    ['Caso d’uso non ancora configurato in SIPO', 'Il catalogo si configura per frequenza; '
     'finché un caso manca, la web app è la strada.', 'Alta all’inizio, poi in calo.'],
    ['Fermo di SIPO', 'La web app come riserva (OP-42 di [R1]).', 'Episodica.'],
    ['Funzioni solo web app su un atto esistente', 'Nota tecnica, annotazioni, allegati errati: '
     'non formano l’atto, lo cambiano.', 'Trattata come modifica successiva.'],
]

ANSC_OFFRE = [
    ['Che cosa serve', 'Che cosa offre ANSC', 'Limite'],
    ['Sapere che l’atto è stato formato', 'Nulla: nessuna notifica e nessuna coda per gli atti '
     'del proprio comune.', 'Si scopre solo interrogando.'],
    ['Ritrovarlo', 'R005 /consultazione/ansc/evento per idAnsc, idComunale, date, tipo evento, '
     'comune di registrazione.', 'Nessun criterio di stato o di canale; non è detto su quale '
     'data lavorino dataDa e dataA; idComunale è descritto come «codificato ANPR_03» (RW-04).'],
    ['Leggerlo', 'R005 restituisce il modello evento completo; la variante sintetica 27 '
     'proprietà.', 'Paginazione corretta più volte (1.36.3, 1.42.1).'],
    ['Sapere da dove viene', 'Nulla: il modello non porta il canale; nomeApplicativo sta solo '
     'nella testata della richiesta e i campi operatore sono deprecati.', 'SIPO lo deve '
     'registrare da sé.'],
    ['Il documento', 'R010 /anteprima/evento restituisce il PDF, ma vuole l’intero modello '
     'evento; R002 dà l’estratto per copia integrale con la firma dell’ufficiale.', 'Senza firma '
     'il PDF dell’atto firmato potrebbe non essere ottenibile (RW-07).'],
    ['Gli allegati', 'R001 /allegato per identificativo, letto dal modello evento.', '—'],
    ['Le annotazioni', 'R005 con idEvento e idtipocontenuto = 0 (1.41.2).', 'Valore non '
     'documentato nella decodifica ANSC_02.'],
    ['Le modifiche successive', 'R005 con flagRettifica; R005 note tecniche per idEvento.',
     'Nessun «modificati dal…»: si rilegge atto per atto.'],
    ['Dichiarare la presa in carico', 'Nulla.', 'R009 /collegamento/evento serve un altro '
     'scopo (annotazione senza soggetto).'],
]

SIPO_SERVE = [
    ['Funzione di SIPO', 'Che cosa le serve', 'Livello minimo'],
    ['Numerazione (serie, buchi, statistiche del numero)', 'DATI_ATTO_ESTERNO con il numero '
     'Utilizzato e l’idAnsc.', 'L0'],
    ['Certificazione', 'L’identificativo ANSC sull’atto: la regola di [R4] lo cerca nello store '
     'o in ANAG_USR.ATTO.', 'L1'],
    ['Ricerca per identificativo nazionale o numero comunale', 'ANSC_STATO_ATTO; la ricerca va '
     'costruita (OP-30 di [R1]).', 'L1'],
    ['Allineamento ANPR in forma ANSC', 'Le cinque colonne ANSC di ANAG_USR.ATTO [R6].', 'L1'],
    ['Ricerche per area, dettaglio, riepilogo', 'MATR_USR.ATTO, la tabella d’area con gli '
     'intestatari, CONF_TIPO_ATTI e CONF_STATO_PRATICA valorizzati: le ricerche fanno join '
     'interne e la pagina va in errore se mancano.', 'L2'],
    ['Annotazioni di SIPO', 'L’atto in MATR_USR e in ANAG_USR.ATTO con gli stessi estremi '
     '(numero, anno, parte e serie, esponente, area): il legame si fa per estremi.', 'L2'],
    ['Statistiche e registri', 'Viste non fra le sorgenti (ATTI_STATISTICHE_UTENTI, '
     'V_REGISTRO_ATTI) (RW-13).', 'L2'],
    ['Estratti dal formulario, comunicazioni di trascrizione, allineamento ANPR da SIPO',
     'L’atto completo e la definizione in SIPO.', 'L3 — ma per un atto ANSC non servono, o '
     'farebbero danno'],
]

STRATEGIE = [
    ['Aspetto', 'S1 — Riferimento (L0 + L1)', 'S2 — Scheda essenziale (L2)',
     'S3 — Importazione completa (L3)'],
    ['Che cosa scrive', 'Numero, store, colonne ANSC di ANAG_USR.ATTO', 'In più: MATR_USR.ATTO, '
     'tabella d’area, intestatari, testo, PDF se ottenibile', 'In più: tutte le tabelle d’area '
     'dal modello evento'],
    ['Che cosa vede l’operatore in SIPO', 'L’atto non compare nelle ricerche per area: si trova '
     'per idAnsc o numero', 'L’atto compare come gli altri, con i dati essenziali', 'L’atto '
     'compare per intero'],
    ['Certificazione', 'Da ANSC [R4]', 'Da ANSC [R4]', 'Da ANSC [R4]'],
    ['Annotazioni di SIPO', 'No', 'Sì', 'Sì'],
    ['Allineamento ANPR', 'Da ANSC, tramite la predisposizione', 'Uguale', 'Uguale: SIPO non lo '
     'rifà'],
    ['Che cosa serve costruire', 'Ricerca R005, pagina di aggancio, operazioni del numeratore',
     'In più: scrittura di un atto definito senza passare dalla definizione', 'In più: la '
     'mappatura inversa per ogni caso d’uso'],
    ['Rischi', 'L’atto resta «fuori» dalle abitudini dello sportello', 'Atto con pochi dati '
     '(pochissimi con il caso d’uso di servizio)', 'Mappatura inversa non univoca (TL-05); '
     'divergenza fra due copie complete'],
    ['Costo', 'Basso', 'Medio', 'Alto, proporzionale ai casi d’uso'],
]

PASSI = [
    ['#', 'Passo', 'Dove', 'Che cosa fa'],
    ['1', 'Stacco del numero', 'SIPO, be-numeratore-comunale', 'POST /richiesta: il numero è '
     'Disponibile. L’atto di SIPO, se esiste già, passa allo stato applicativo di attesa (TL-03).'],
    ['2', 'Formazione sulla web app', 'Web app ANSC', 'L’ufficiale usa il numero staccato, non '
     'quello che la web app suggerisce.'],
    ['3', 'Ritrovamento', 'SIPO, pagina «Recupero Atto ANSC» [R2]', 'R005 per comune e data, o '
     'puntuale per idAnsc o numero; SIPO filtra lo stato 5 e confronta il numero ANSC con '
     'quello staccato.'],
    ['4', 'Verifica', 'SIPO', 'Numero uguale, comune di Roma, stato FIRMATO DA USC, caso d’uso '
     'e intestatari coerenti con la richiesta. Una divergenza si mostra e si decide (RW-03).'],
    ['5', 'Conferma e scrittura', 'statocivile-be e concentratore', 'Secondo il livello: '
     'store con canale WEBAPP e modello evento, ANAG_USR.ATTO, MATR_USR.ATTO e tabella '
     'd’area, identificativi dei soggetti «solo dove mancano».'],
    ['6', 'Il numero', 'be-numeratore-comunale', 'Utilizzato con l’idAnsc, poi Evento acquisito '
     '(operazioni mancanti, OP-79).'],
    ['7', 'Ciò che non si fa', '—', 'Nessuna definizione in SIPO, nessun formulario, nessuna '
     'chiamata ad ANPR, nessuna comunicazione di trascrizione.'],
]

DOPO = [
    ['Effetto', 'Per un atto formato in SIPO oggi', 'Per un atto formato sulla web app'],
    ['Allineamento anagrafico', 'SIPO chiama all-anpr-sipo alla definizione (2001, 1001, 5008…).',
     'ANSC predispone la comunicazione e la notifica all’anagrafe tramite ANPR. SIPO non chiama '
     'all-anpr-sipo: si avrebbe il doppio aggiornamento (RW-10).'],
    ['Annotazioni contestuali e automatiche', 'Le genera il formulario alla definizione.',
     'Le genera ANSC; con il caso d’uso di servizio nessuna, e le fa l’ufficio (TL-11).'],
    ['Comunicazioni agli altri comuni', 'PKG_COMUNICAZIONI alla definizione.', 'Notifiche ANSC; '
     'SIPO non le rigenera.'],
    ['Comunicazioni agli enti', 'Fuori da SIPO.', 'ANSC le predispone; si scaricano con R003.'],
    ['PDF e copia conforme', 'ATTO_SCANSIONATO alla definizione.', 'Da ANSC, se ottenibile '
     'senza firma (RW-07); altrimenti nessun PDF in SIPO e consultazione su ANSC.'],
    ['Protocollo e richiesta di scansione', 'Alla definizione.', 'Non pertinenti.'],
    ['Certificati ed estratti', 'Formulario di SIPO.', 'ANSC [R4].'],
]

MODIFICHE = [
    ['Che cosa cambia in ANSC', 'Come lo scopre SIPO', 'Che cosa fa SIPO'],
    ['Nota tecnica', 'R005 note tecniche per idEvento', 'Riallineamento: confronto con il modello '
     'conservato e aggiornamento dei dati che SIPO ha (L2 e oltre) [R3].'],
    ['Annotazione per rettifica o errore materiale', 'R005 con flagRettifica', 'Uguale; '
     'registro dell’annotazione [R3].'],
    ['Annullamento, cancellazione, inefficacia', 'Lo stato letto con R005', 'Aggiornamento dello '
     'stato; per l’annullamento, quello di SIPO.'],
    ['Annotazioni di altri comuni', 'Le notifiche R008, già previste [R1]', 'Come per gli atti '
     'formati da SIPO.'],
]

IMPATTI = [
    ['Dove', 'Che cosa serve'],
    ['ANSC_STATO_ATTO', 'Una colonna per il canale di formazione (SIPO, WEBAPP), perché ANSC non '
     'lo dice; il modello evento letto in TXT_EVENTO, che per questi atti è il letto e non il '
     'depositato.'],
    ['be-numeratore-comunale', 'utilizzaNumero con l’idAnsc e il passaggio a Evento acquisito '
     '(OP-79).'],
    ['Concentratore e ansc-v1.yaml', 'cercaAttiAnsc (R005 per comune, data, numero, idAnsc) e '
     'agganciaAtto (lettura, verifica, scrittura del livello scelto). Le letture R005 senza '
     'OTP restano OP-23 di [R1].'],
    ['statocivile-be', 'La scrittura di un atto definito senza passare da /finalizzaAtto: '
     'stato, data di definizione, estremi, tabella d’area, senza integrazione PL/SQL né '
     'allineamento ANPR (RW-11).'],
    ['anagrafe-entities', 'La scrittura delle colonne ANSC di ANAG_USR.ATTO fuori dalle '
     'maschere: è AN-01 di [R6].'],
    ['Pagine', '«Recupero Atto ANSC» e «Riepilogo Atto ANSC» di [R2], estese ai casi diversi dal '
     'testo libero.'],
    ['Back-office', 'La categoria «In attesa della stesura sulla web app»: numeri staccati e non '
     'ancora ricondotti a un atto, con l’anzianità [R2] [R7].'],
]

CONTRADDIZIONI = [
    ['Tema', 'Che cosa dicono i documenti', 'Proposta'],
    ['Dove sta l’idAnsc di un atto agganciato', '[R4] lo cerca anche in ANAG_USR.ATTO; [R7] in '
     'ANSC_STATO_ATTO; [R1] rinvia a OP-29.', 'In entrambi: lo store è la fonte, ANAG_USR.ATTO la '
     'copia per ANPR.'],
    ['Riconciliazione periodica o su richiesta', '[R1] la vuole su richiesta, ma una sua decisione cita una '
     'riconciliazione periodica.', 'Su richiesta per il riallineamento; una lista di lavoro per '
     'i numeri senza atto (questo documento).'],
    ['«Lega un numero a un atto agganciato»', '[R1] la elenca fra le funzioni del back-office; '
     '[R5] e [R7] dicono che l’operazione non esiste.', 'Da realizzare (OP-79).'],
    ['Dati registrati all’aggancio', '[R1] parla di quattro dati, il capitolo a cui rinvia ne '
     'elenca tre.', 'Quelli del livello scelto, in questo documento.'],
    ['Numero sull’atto di SIPO', 'MATR_USR.ATTO non ha una colonna per il numero ANSC; '
     'IntegrazioneATTO assegna un numero della serie SIPO (WF-12).', 'RW-08.'],
]

APERTI = [
    ['#', 'Questione', 'A chi spetta'],
    ['RW-01', 'Perimetro: quale livello per quale atto. Coincide con OP-66 di [R1]. Proposta: L1 '
     'per tutti, L2 come regola, L3 solo per i casi d’uso ordinari che lo giustificano (TL-08).',
     'Comune'],
    ['RW-02', 'Il numero comunale di SIPO ha sei cifre, la web app ne accetta cinque '
     '(1.20.0). Un numero oltre 99.999 non entrerebbe sulla web app. Va chiuso con OP-73.',
     'Comune / Sogei'],
    ['RW-03', 'Numero usato sulla web app diverso da quello staccato: la web app suggerisce '
     'l’ultimo numero usato e nessuna fonte documenta un controllo di unicità. Bloccare, '
     'accettare con avviso, scartare lo staccato (TL-12).', 'Comune'],
    ['RW-04', 'Se il criterio idComunale di R005 cerchi davvero per numero comunale: la '
     'descrizione lo dice «codificato ANPR_03». Da provare in preproduzione.', 'Sogei'],
    ['RW-05', 'Su quale data lavorino dataDa e dataA di R005 (formazione, evento, '
     'decorrenza): decide come si cercano gli «atti del giorno».', 'Sogei'],
    ['RW-06', 'R005 non filtra per stato: SIPO filtra dopo la risposta. Quanti atti tornino per '
     'Roma in un giorno, e con quale paginazione.', 'Analisi / Sogei'],
    ['RW-07', 'Se il PDF di un atto firmato si possa ottenere senza firma: R010 vuole l’intero '
     'modello evento e toglie la filigrana solo sugli atti confermati.', 'Sogei'],
    ['RW-08', 'Estremi dell’atto in MATR_USR per un atto ANSC: NUMERO_ATTO, parte, serie, '
     'esponente; e coerenza con ANAG_USR.ATTO, da cui dipende il legame delle annotazioni. Si '
     'lega a OP-60 di [R1] e a WF-12.', 'Analisi / Sviluppo SIPO'],
    ['RW-09', 'Chi crea la riga di ANAG_USR.ATTO per un atto recuperato (oggi la crea '
     'l’allineamento ANPR, che qui non si fa) e chi ne scrive le colonne ANSC (AN-01 di [R6]).',
     'Analisi / Sviluppo SIPO'],
    ['RW-10', 'Anagrafe: la predisposizione ANSC arriva all’ufficio anagrafe tramite ANPR '
     '(servizio 4005), che SIPO oggi non tratta. Chi la lavora, e come si evita che SIPO '
     'aggiorni due volte.', 'Comune / Analisi'],
    ['RW-11', 'Stato in SIPO dell’atto recuperato (TL-04) e scrittura di un atto definito senza '
     'la definizione: i corpi di PKG_PRATICA (IntegrazioneATTO, CompletaATTO) non sono fra le '
     'sorgenti.', 'Sviluppo SIPO'],
    ['RW-12', 'Provenienza statistica degli atti recuperati (CONF_PROVENIENZA_ATTO), per '
     'distinguerli nei conteggi.', 'Comune'],
    ['RW-13', 'Testo delle viste che decidono la visibilità (GESTIONE_ATTO_*, ATTO_SINTESI, '
     'V_DETTAGLIO_ATTO_*, V_RIEPILOGO_ATTO_*, ATTI_STATISTICHE_UTENTI, V_REGISTRO_ATTI) e DDL '
     'di MATR_USR: da chiedere all’amministrazione della base dati.', 'DBA'],
    ['RW-14', 'Termine entro cui un numero staccato deve trovare il suo atto, e sorte del numero '
     'alla scadenza (TL-07).', 'Comune'],
]


# =================================================================== testo
def scrivi(d):
    h(d, 1, 'Scopo del documento')
    par(d, 'Alcuni atti di Roma nasceranno sulla web app di ANSC invece che in SIPO. Il numero '
           'comunale lo produce comunque SIPO; il problema è che cosa succede dopo la firma: '
           'come l’atto torna in SIPO, quanto di esso vi si scrive, e che cosa ne consegue per '
           'anagrafe, annotazioni, documenti e modifiche successive. Il documento confronta le '
           'strategie e ne propone una.')
    par(d, 'Raccoglie anche ciò che i documenti precedenti avevano già deciso su questo tema — '
           'l’aggancio [R1], le pagine di recupero [R2], il riallineamento [R3] — e ne segnala '
           'le incoerenze.')
    h(d, 2, 'Glossario')
    tabella(d, GLOSSARIO, [1.8, 4.6])
    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 4.6, 1.2])

    # ------------------------------------------------------------------
    h(d, 1, 'Quando un atto nasce sulla web app')
    tabella(d, CASI, [1.8, 3.2, 1.4])
    par(d, 'In tutti i casi l’ufficiale stacca il numero in SIPO prima di andare sulla web app '
           '[R1] [R5]. ANSC stessa suggerisce alle case software di sviluppare servizi che '
           'recuperino gli atti registrati sulla web app [A3]: il recupero è un compito del '
           'gestionale, non un servizio che ANSC offrirà.')

    h(d, 1, 'Il punto di partenza: il numero staccato in SIPO')
    par(d, 'Il numero è l’unico filo fra i due mondi: SIPO lo conosce prima che l’atto esista, e '
           'ANSC lo registra nell’atto (evento.numeroatto). Il servizio be-numeratore-comunale lo '
           'stacca (POST /richiesta, stato Disponibile), lo segna come usato (PUT /utilizza) o '
           'scartato (PUT /scarta) [R5].')
    voce(d, 'Che cosa manca.', 'PUT /utilizza non riceve l’idAnsc, e il passaggio a «Evento '
         'acquisito» non ha un’operazione (OP-79 di [R1]). Senza, il numero non porta con sé '
         'l’atto che l’ha usato.')
    voce(d, 'Due rischi sul numero.', 'La web app suggerisce da sé «l’ultimo numero già usato» '
         '(versione 1.18.4) e nessuna fonte documenta un controllo di unicità: l’ufficiale può '
         'usare un numero diverso da quello staccato (RW-03). E la web app accetta al massimo '
         'cinque caratteri (1.20.0), mentre la serie di SIPO ne prevede sei (RW-02).')

    # ------------------------------------------------------------------
    h(d, 1, 'Che cosa offre ANSC per ritrovare e rileggere l’atto')
    par(d, 'ANSC non avvisa il gestionale, non ha un servizio di recupero e non registra da quale '
           'canale è stato formato l’atto. Tutto passa da letture a richiesta [A1] [A2]:')
    tabella(d, ANSC_OFFRE, [1.5, 2.6, 2.3])
    par(d, 'Ne discende un fatto che regge il resto del documento: **per sapere che un atto di '
           'Roma è nato sulla web app, SIPO deve registrarlo da sé** al momento del recupero. '
           'Dopo, nessuna fonte glielo ricorderà.')

    # ------------------------------------------------------------------
    h(d, 1, 'Che cosa serve in SIPO perché l’atto esista')
    par(d, 'Oggi nessun canale di SIPO crea un atto di stato civile dall’esterno: gli atti '
           'trascritti, a testo libero o scansionati si scrivono sempre su un atto creato e '
           'numerato da SIPO [S1]. E la definizione ordinaria (/finalizzaAtto) non si può '
           'riusare: integra la posizione anagrafica, chiama ANPR, genera dal formulario il PDF '
           'e le annotazioni, crea le comunicazioni di trascrizione. Su un atto formato in ANSC '
           'produrrebbe un secondo testo, diverso dall’originale, e un secondo aggiornamento '
           'anagrafico.')
    par(d, 'Che cosa serve, funzione per funzione:')
    tabella(d, SIPO_SERVE, [2.0, 3.2, 1.2])
    voce(d, 'Le ricerche sono severe.', 'Fanno join interne su tipo atto, area e stato, e '
         'confrontano parte, serie ed esponente per uguaglianza: un atto scritto a metà non solo '
         'non si trova, ma può mandare in errore l’intera pagina dei risultati.')
    voce(d, 'Le annotazioni si legano per estremi.', 'Il modulo delle annotazioni cerca l’atto '
         'in ANAG_USR.ATTO e lo ricongiunge a MATR_USR.ATTO per numero, anno, parte e serie, '
         'esponente e area: un atto recuperato deve averli uguali nei due schemi (RW-08).')
    voce(d, 'Molto è nascosto.', 'Le viste che decidono che cosa vedono dettaglio, riepilogo e '
         'statistiche e i corpi dei package non sono fra le sorgenti (RW-13).')

    # ------------------------------------------------------------------
    h(d, 1, 'Le strategie')
    h(d, 2, 'Quattro livelli di presenza')
    figura(d, diagrammi_recupero.livelli(), 6.5,
           'Figura 1 — I livelli di presenza in SIPO di un atto formato sulla web app.')
    par(d, 'I livelli sono cumulativi, e ciascuno è una strategia possibile:')
    tabella(d, STRATEGIE, [1.4, 1.7, 1.7, 1.6])
    h(d, 2, 'La proposta')
    voce(d, 'L1 subito, per tutti.', 'Numero, store e colonne ANSC di ANAG_USR.ATTO. È il '
         'minimo perché l’atto sia certificabile da ANSC [R4], ricercabile per identificativo e '
         'trasmesso ad ANPR nella forma ANSC [R6]. Costa poco e non dipende dalla mappatura.')
    voce(d, 'L2 come regola.', 'La scheda essenziale fa comparire l’atto allo sportello come gli '
         'altri e gli permette di ricevere le annotazioni di SIPO. Si scrivono gli estremi, gli '
         'intestatari e il testo; i dati di dettaglio si leggono da ANSC quando servono.')
    voce(d, 'L3 solo dove serve.', 'L’importazione completa ha senso per i casi d’uso ordinari '
         'già configurati, dove la mappatura esiste (TL-08 di [R2]); non per i casi d’uso di '
         'servizio, che portano solo intestatario e testo.')
    voce(d, 'In ogni caso, i dati di ANSC prevalgono.', 'Al recupero, ciò che SIPO aveva '
         'compilato prima del rinvio alla web app serve da riscontro: le divergenze si mostrano '
         'all’ufficiale, non si risolvono da sole [R2].')

    # ------------------------------------------------------------------
    h(d, 1, 'Come si aggancia')
    tabella(d, PASSI, [0.3, 1.3, 1.6, 3.2])
    voce(d, 'Chi avvia.', 'L’ufficiale, subito dopo la firma sulla web app, come previsto per le '
         'altre operazioni fatte fuori da SIPO [R1]. È una regola di lavoro, non un controllo del '
         'software.')
    voce(d, 'La rete di sicurezza.', 'Il back-office tiene la lista dei numeri staccati e non '
         'ancora ricondotti a un atto, con l’anzianità [R2]. Da lì si può lanciare la ricerca '
         'R005 per numero su ciascuno, su richiesta. Non è un controllo a calendario: le letture '
         'senza OTP sono ancora da accertare (OP-23 di [R1]).')
    voce(d, 'Che cosa non si fa mai.', 'Rifare in SIPO la definizione dell’atto recuperato.')

    # ------------------------------------------------------------------
    h(d, 1, 'Che cosa succede dopo')
    figura(d, diagrammi_recupero.dopo(), 6.5,
           'Figura 2 — Gli effetti di un atto firmato sulla web app e il ruolo di SIPO.')
    h(d, 2, 'Gli effetti della formazione')
    tabella(d, DOPO, [1.6, 2.2, 2.6])
    par(d, 'Il punto più delicato è l’anagrafe. Per un atto formato in SIPO l’aggiornamento lo '
           'fa SIPO, chiamando ANPR alla definizione. Per un atto formato in ANSC la '
           'comunicazione anagrafica la predispone ANSC e arriva all’ufficio anagrafe tramite '
           'ANPR [A4]: è una notifica da lavorare, non una mutazione già applicata, e SIPO oggi '
           'non la tratta. Se SIPO, recuperando l’atto, chiamasse anche ANPR, la stessa persona '
           'riceverebbe due aggiornamenti. La regola è: **per un atto recuperato SIPO non chiama '
           'ANPR**, e chi lavora la predisposizione va stabilito (RW-10).')
    h(d, 2, 'Le modifiche successive')
    par(d, 'Dopo il recupero l’atto può cambiare ancora, e solo sulla web app o da altri comuni. '
           'Nessuna fonte avvisa SIPO; lo scopre rileggendo l’atto:')
    tabella(d, MODIFICHE, [1.8, 1.8, 2.8])
    par(d, 'Il riallineamento resta su richiesta, come deciso in [R1]. Per gli atti nati sulla '
           'web app conviene però un’attenzione in più: sono quelli su cui è più probabile un '
           'secondo intervento sulla web app, perché è lì che l’ufficiale li ha in mano.')

    # ------------------------------------------------------------------
    h(d, 1, 'Che cosa cambia nel disegno')
    tabella(d, IMPATTI, [1.8, 4.6])

    h(d, 1, 'Allineamenti fra i documenti')
    par(d, 'La ricognizione ha trovato alcune incoerenze fra i documenti precedenti, che questo '
           'documento propone di sciogliere così:')
    tabella(d, CONTRADDIZIONI, [1.6, 2.6, 2.2])

    h(d, 1, 'Punti aperti')
    par(d, 'I più urgenti sono RW-02 e RW-03: riguardano il numero, cioè l’unico filo fra i due '
           'mondi, e vanno chiusi prima di usare la web app in esercizio.')
    tabella(d, APERTI, [0.7, 4.3, 1.4])

    h(d, 1, 'Il percorso di adozione')
    voce(d, 'Primo — L1 e il numero.', 'Le operazioni mancanti del numeratore, la pagina di '
         'ricerca e conferma, lo store con il canale e le colonne ANSC di ANAG_USR.ATTO. Da qui '
         'gli atti sono certificabili e ritrovabili.')
    voce(d, 'Secondo — L2.', 'La scrittura dell’atto definito senza definizione, dopo aver avuto '
         'dal DBA viste e package (RW-11, RW-13).')
    voce(d, 'Terzo — L3 dove serve.', 'Caso d’uso per caso d’uso, partendo dalla mappatura già '
         'configurata.')


def intesta(d):
    for r in d.tables[0].rows:
        if len(r.cells) < 2:
            continue
        etichetta = r.cells[0].text.strip().lower()
        valore = {'progetto': 'SIPO — Integrazione con ANSC',
                  'data consegna': DATA}.get(etichetta)
        if valore:
            D.riscrivi_cella(r.cells[1], valore)
    for fatto in D.frontespizio(d, '0.1', NOME):
        print('  ' + fatto)
    storia = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for r in list(storia.rows[1:]):
        if not any(c.text.strip() for c in r.cells):
            r._tr.getparent().remove(r._tr)
    D.storia(d, DATA, '0.1', 'Tutti',
             'Prima stesura. Quando un atto nasce sulla web app; il numero staccato in SIPO e i '
             'suoi rischi; che cosa offre ANSC per ritrovare e rileggere l’atto; che cosa serve '
             'in SIPO perché l’atto esista; quattro livelli di presenza e tre strategie a '
             'confronto, con la proposta; i passi dell’aggancio; gli effetti dopo la firma e le '
             'modifiche successive; impatti sul disegno; allineamenti fra i documenti; '
             'quattordici punti aperti.')


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
