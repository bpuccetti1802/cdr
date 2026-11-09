# -*- coding: utf-8 -*-
"""v0.2 di «PROPOSTA_Osservabilita-OpenTelemetry»: il capitolo sulle interfacce.

⚠️ Si parte dal FILE REALE della v0.1, non da `genera_otel.py`: l'utente l'ha rivista in Word
(indice rigenerato, riformulazioni, e soprattutto **tolta la raccomandazione di rinviare la
scelta della destinazione**, sostituita da «Oracle allo stato attuale e' la soluzione
identificata»). Rigenerare dallo script perderebbe quelle modifiche.

Il capitolo nuovo risponde alla richiesta: descrivere in dettaglio le API di scrittura,
lettura e ricerca dei log «per poterle inserire nei diversi programmi». La risposta onesta
distingue due cose che la domanda unisce:

  * cio' che si inserisce nei programmi e' la **libreria in processo**, non una API REST;
  * una API REST di **scrittura** serve a un solo chiamante, il **browser**, che non puo'
    parlare al collector;
  * le API di **lettura e ricerca** servono al back-office e al supporto, e sono quelle che
    meritano le schede di operazione per esteso.

⚠️ **I back-end non devono scrivere i log via REST**: accoppierebbe la loro disponibilita' a
quella del servizio di log, su un volume stimato di 3-6 milioni di eventi l'anno. Il trasporto
e' OTLP, che accoda, ritenta e regola il flusso da se'.

Convenzioni seguite dai contratti gia' in casa (`ansc-numerazione-v1.yaml`): percorso
`/api/v1/<servizio>/<azione>`, `get` per le ricerche con parametri in query, paginazione
`pageOffset`/`pageSize`, risposta `PaginaXxx` con `content[]` e `page{}`, estensioni
`x-sicurezza` e `x-effetti`. Verbi dal vocabolario chiuso: crea, cerca, leggi, elenca.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/otel_v0_2_api.py
"""
import os
import shutil
import sys

import docx
from docx.shared import Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali',
                   'PROPOSTA_Osservabilita-OpenTelemetry_v0.1.docx')
OUT = os.path.join(BASE, 'Documenti finali',
                   'PROPOSTA_Osservabilita-OpenTelemetry_v0.2.docx')
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


def _versa(p, s, dim=None):
    for txt, grassetto, mono in pezzi_di(s):
        r = p.add_run(txt)
        r.bold = grassetto
        if mono:
            r.font.name = 'Courier New'
            r.font.size = Pt((dim or 10) - 1)
        elif dim:
            r.font.size = Pt(dim)
    return p


def par(doc, prima, testo, stile='Normal'):
    return _versa(D.para(doc, prima, '', stile=stile), testo)


def h(doc, prima, livello, testo):
    p = D.para(doc, prima, '', stile='Heading %d' % livello)
    p.add_run(testo)
    return p


def voce(doc, prima, testa, corpo):
    p = D.para(doc, prima, '', stile='List Paragraph')
    r = p.add_run(testa + ' ')
    r.bold = True
    return _versa(p, corpo)


def tabella(doc, prima, righe, modello, larghezze=None):
    """Come D.tabella, ma le celle passano dall'interprete che conosce anche gli apici
    inversi: D.tabella interpreta i ** e lascerebbe il monospazio come testo (132 apici
    rimasti in pagina alla prima stesura della v0.2)."""
    t = D.tabella(doc, prima, [['' for _ in r] for r in righe], modello, larghezze)
    for i, riga in enumerate(righe):
        for j, val in enumerate(riga):
            cel = t.cell(i, j)
            cel.paragraphs[0]._p.getparent().remove(cel.paragraphs[0]._p)
            par_ = cel.add_paragraph()
            par_.alignment = D.GIUST
            for txt, grassetto, mono in pezzi_di(str(val)):
                r = par_.add_run(txt)
                r.bold = grassetto or i == 0
                r.font.size = Pt(8 if mono else 9)
                if mono:
                    r.font.name = 'Courier New'
    return t


def codice(doc, prima, righe, didascalia=None):
    D.ddl(doc, prima, righe)
    if didascalia:
        p = D.para(doc, prima, '')
        _versa(p, didascalia, dim=9)
        for r in p.runs:
            r.italic = True
            r.font.size = Pt(8)
    D.para(doc, prima, '')


# =================================================================== contenuti
INTERFACCE = [
    ['Interfaccia', 'Chi la usa', 'Trasporto', 'Perché è così'],
    ['**Libreria in processo**', 'Tutti i programmi: i quattro pod nuovi, i back-end della '
     'catena dell’atto, i front-end.', 'Chiamata locale',
     '**È questa che si inserisce nei programmi.** Non c’è rete di mezzo: scrivere '
     'un evento non può fallire per una ragione di rete.'],
    ['**OTLP verso il collector**', 'La libreria, non il programma.', 'gRPC o HTTP, interno',
     'Accoda, raggruppa, ritenta e regola il flusso da sé. Il programma non se ne accorge.'],
    ['**API REST di ingestione**', '**Solo il browser.**', 'HTTPS',
     'Il browser non può parlare al collector: non lo si espone, e serve autenticare e '
     'limitare chi scrive.'],
    ['**API REST di lettura e ricerca**', 'Il back-office del supporto, e chi sviluppa.',
     'HTTPS', 'Sono le pagine descritte al capitolo del back-office.'],
]

OPERAZIONI = [
    ['#', 'Percorso', 'Verbo', 'operationId', 'A che cosa serve'],
    ['1', '`/api/v1/osservabilita/eventi`', 'POST', '`creaEventi`',
     'Ingestione in blocco degli eventi del browser. **Unico punto di scrittura esposto.**'],
    ['2', '`/api/v1/osservabilita/eventi`', 'GET', '`cercaEventi`',
     'La worklist: ricerca paginata per periodo, livello, origine, servizio, codice e '
     'identificativi dei tre piani.'],
    ['3', '`/api/v1/osservabilita/eventi/{idEvento}`', 'GET', '`leggiEvento`',
     'Il singolo evento con tutti i suoi attributi. Serve anche come collegamento stabile.'],
    ['4', '`/api/v1/osservabilita/tracce/{traceId}`', 'GET', '`leggiTraccia`',
     'La cascata: gli span in sequenza e gli eventi agganciati a ciascuno.'],
    ['5', '`/api/v1/osservabilita/riepilogo`', 'GET', '`cercaRiepilogo`',
     'Conteggi per codice e per origine su un periodo: distingue il caso isolato dal difetto '
     'sistematico.'],
    ['6', '`/api/v1/osservabilita/oggetti/{piano}/{identificativo}/eventi`', 'GET',
     '`elencaEventiOggetto`',
     'Tutti gli eventi di un oggetto dei tre piani, anche a settimane di distanza.'],
]

METODI_LIB = [
    ['Metodo', 'Che cosa fa', 'Dove si usa'],
    ['`registro.evento(origine, codEvento)`',
     'Apre un evento classificato. Origine e codice sono **obbligatori**: non esiste la forma '
     'senza.', 'Dove il supporto dovrà cercare e contare.'],
    ['`.messaggio(testo)`', 'Il testo per chi legge. Può cambiare senza conseguenze.', ''],
    ['`.livello(livello)`', 'Se omesso vale `ERROR` per gli eventi aperti con un’origine '
     'di errore, `INFO` altrimenti.', ''],
    ['`.atto(idAttoSipo)`', '**Piano 1.** Aggiunge da sé anche `id_ansc`, `numero_atto` e '
     '`cod_municipio` se l’atto li ha già.', 'Eventi che riguardano un atto.'],
    ['`.allegato(idAllegato)`', '**Piano 2.** Aggiunge `id_ansc_allegato` se assegnato. '
     '**Non richiede un atto.**', 'Caricamento e verifica dei documenti.'],
    ['`.soggetto(idSoggettoSipo)`', '**Piano 3.** Aggiunge `id_ansc_soggetto`, '
     '`id_scheda_anpr`, `id_unico_nazionale` se noti.', 'Ricerca e riconciliazione dei '
     'soggetti.'],
    ['`.attributo(nome, valore)`', 'Un attributo libero. Il nome segue le convenzioni '
     'semantiche.', ''],
    ['`.riservato(nome, valore)`', 'Come il precedente ma **oscurato**: ne resta una forma '
     'parziale, non il valore.', 'Dove servirebbe un dato personale.'],
    ['`.errore(eccezione)`', 'Allega tipo, messaggio e pila dell’eccezione.', ''],
    ['`.registra()`', 'Chiude e consegna. **È l’unico metodo che produce un effetto.**',
     ''],
    ['`registro.passo(nome)`', 'Delimita uno span: durata ed esito si chiudono da sé con '
     'il blocco.', 'Intorno a ciò di cui si vuole misurare il tempo.'],
    ['`Registro.corrente()`', 'Il contesto in corso: identificativi di traccia, utente, '
     'postazione.', 'Dove serve propagare a mano.'],
]

PARAMETRI_RICERCA = [
    ['Parametro', 'Tipo', 'Significato'],
    ['`da`, `a`', '`date-time`', 'Estremi del periodo, inclusi. **Obbligatorio almeno `da`**: '
     'senza, la ricerca attraverserebbe tutte le partizioni.'],
    ['`livelloMinimo`', 'stringa', 'Da `TRACE` a `FATAL`. Filtra per severità maggiore o '
     'uguale; il valore consueto per il supporto è `WARN`.'],
    ['`codOrigine`', 'stringa', 'Uno dei sette valori. Ripetibile.'],
    ['`codServizio`', 'stringa', 'Il nome del processo. Ripetibile.'],
    ['`codEvento`', 'stringa', 'Uguaglianza esatta sul codice stabile.'],
    ['`traceId`', 'stringa', 'Tutti gli eventi di una traccia.'],
    ['`idAttoSipo`, `idAnsc`, `numeroAtto`', 'misti',
     '**Piano 1.** In alternativa fra loro.'],
    ['`idAllegato`, `idAnscAllegato`', 'misti', '**Piano 2.**'],
    ['`idSoggettoSipo`, `idAnscSoggetto`, `idUnicoNazionale`', 'misti', '**Piano 3.**'],
    ['`utente`', 'stringa', 'Chi stava operando.'],
    ['`codAmbiente`', 'stringa', 'Produzione, preproduzione, collaudo.'],
    ['`pageOffset`, `pageSize`', 'interi', 'Paginazione, come negli altri contratti: base 0, '
     'dimensione predefinita 10, massima 200.'],
]

ERRORI_API = [
    ['Codice', 'Quando', 'Che cosa fa il chiamante'],
    ['`400`', 'Periodo assente o rovesciato, `pageSize` fuori limite, livello non ammesso, '
     'piano sconosciuto.', 'Corregge la richiesta.'],
    ['`401` / `403`', 'Gettone assente, oppure utente senza l’abilitazione alla pagina di '
     'diagnostica.', 'Non riprova.'],
    ['`404`', 'Traccia o evento inesistenti, **oppure già scaduti**.',
     'Mostra «fuori dal periodo di conservazione», che è diverso da «non è mai '
     'accaduto».'],
    ['`413`', 'Blocco di ingestione oltre il limite dichiarato.',
     'Il front-end riduce il blocco e ritenta.'],
    ['`429`', 'Troppe scritture dalla stessa origine.',
     'Il front-end rallenta e scarta, **senza ritentare all’infinito**.'],
]

APERTI_NUOVI = [
    ['OT-10', 'Se le operazioni di lettura e ricerca debbano stare in un servizio dedicato '
     '(`be-osservabilita`, come proposto) oppure dentro il back-office che già esiste. Il '
     'servizio dedicato tiene separato il dominio di guasto — una diagnostica che si ferma '
     'non deve fermare la formazione degli atti — ma è una quinta unità da gestire.',
     'Architettura'],
    ['OT-11', 'Se si voglia poter **cambiare i livelli a caldo**, per singolo componente e per '
     'un tempo dichiarato, senza rilasciare. Richiederebbe due operazioni in più e un '
     'presidio su chi può farlo: comodissimo per la diagnosi, pericoloso se dimenticato '
     'acceso.', 'Architettura / Referenti SIPO'],
    ['OT-12', 'I limiti dell’ingestione dal browser: dimensione del blocco, frequenza per '
     'sessione, e che cosa fare quando si superano. Senza una regola, un difetto del front-end '
     'in un giro di eventi riempirebbe il registro in poche ore.', 'Sicurezza / Architettura'],
]


def scrivi(doc, prima, modello):
    """Innesta il capitolo prima dell'ancora, con lo stile di tabella del documento."""
    def tab(righe, larghezze):
        tabella(doc, prima, righe, modello, larghezze)

    h(doc, prima, 1, 'Le interfacce: che cosa si inserisce nei programmi')
    par(doc, prima,
        'Il capitolo precedente dice perché serve una libreria; questo dice che cosa '
        'espone, con quali firme e con quali operazioni di rete. La richiesta era di '
        'descrivere le API «di scrittura, lettura e ricerca dei log per poterle inserire nei '
        'diversi programmi»: la risposta distingue due cose che la domanda unisce, e la '
        'distinzione è la parte importante.')

    h(doc, prima, 2, 'Quattro interfacce, e quale si usa dove')
    tab(INTERFACCE, [1.5, 1.7, 1.1, 2.2])
    par(doc, prima,
        '**I back-end non scrivono i log con una chiamata REST, e non è un dettaglio '
        'realizzativo.** Tre ragioni. La prima: una chiamata sincrona per evento '
        '**accoppierebbe la disponibilità dell’applicazione a quella del servizio di '
        'log** — se la diagnostica si ferma, si ferma la formazione degli atti, che è '
        'esattamente il contrario di ciò che serve. La seconda: il volume stimato è di '
        'tre-sei milioni di eventi l’anno dalla sola formazione, e sarebbero altrettante '
        'chiamate. La terza: accodamento, raggruppamento, ritentativo e regolazione del flusso '
        'sono già nel trasporto OTLP, e riscriverli sarebbe lavoro speso per ottenere meno.')
    par(doc, prima,
        'Resta un chiamante che **non può** usare quel trasporto: il browser. Il collector '
        'non si espone verso l’esterno, e ciò che arriva da un browser va autenticato e '
        'limitato. Per quello — e **solo** per quello — serve un’operazione di '
        'scrittura.')

    h(doc, prima, 2, 'L’API della libreria: ciò che si scrive nei programmi')
    par(doc, prima,
        'Questa è l’interfaccia che entra nei moduli. Due principi la governano: i punti '
        'di registrazione già esistenti **non si toccano** — restano `log.info(…)` e '
        'ricevono il contesto da sé — e tutto ciò che il supporto dovrà cercare '
        'passa invece da una forma esplicita, dove origine e codice sono obbligatori.')
    codice(doc, prima, [
        'public interface Registro {',
        '',
        '    /** Evento classificato: origine e codice sono obbligatori per costruzione. */',
        '    Evento evento(Origine origine, String codEvento);',
        '',
        '    /** Delimita uno span: durata ed esito si chiudono con il blocco. */',
        '    Passo passo(String nome);',
        '',
        '    /** Apre il contesto di una richiesta; il filtro la chiama e la chiude. */',
        '    Contesto apriContesto(ServletRequest richiesta);',
        '',
        '    /** Il contesto in corso: identificativi, utente, postazione. */',
        '    static Contesto corrente();',
        '}',
        '',
        'public interface Evento {',
        '    Evento messaggio(String testo);',
        '    Evento livello(Livello livello);',
        '    Evento atto(Long idAttoSipo);            // piano 1',
        '    Evento allegato(Long idAllegato);        // piano 2',
        '    Evento soggetto(Long idSoggettoSipo);    // piano 3',
        '    Evento attributo(String nome, Object valore);',
        '    Evento riservato(String nome, String valore);   // oscurato',
        '    Evento errore(Throwable eccezione);',
        '    void   registra();                       // l\'unico con un effetto',
        '}',
    ], 'L’interfaccia Java. I tre metodi dei piani non chiedono tutti gli identificativi: '
       'ne ricevono **uno** e risolvono gli altri da sé.')
    tab(METODI_LIB, [2.1, 2.9, 1.5])
    par(doc, prima,
        'Il punto da non perdere è nei tre metodi dei piani. Il programma conosce '
        'l’identificativo che ha per le mani — quello di SIPO, quasi sempre — e '
        '**non deve sapere quali altri esistano**: è la libreria a completarli, leggendoli '
        'dallo store. Senza questo, ogni gruppo scriverebbe la propria versione della stessa '
        'risoluzione, e gli attributi divergerebbero.')
    par(doc, prima, 'Per i micro-frontend la forma è la stessa, nel linguaggio loro:')
    codice(doc, prima, [
        'export interface Registro {',
        '  evento(origine: Origine, codEvento: string): Evento;',
        '  passo<T>(nome: string, corpo: () => T): T;',
        '  contesto(): Contesto;',
        '}',
        '',
        '// l\'uso: identico nella forma a quello del back-end',
        'registro.evento(Origine.FE, \'FE-CHIAMATA-KO\')',
        '        .messaggio(\'Chiamata a /ansc/v1/atti fallita dopo 3 tentativi\')',
        '        .atto(idAttoSipo)',
        '        .attributo(\'stato_http\', String(err.status))',
        '        .registra();',
    ], 'La libreria condivisa dei micro-frontend espone la stessa forma: chi passa da un '
       'modulo all’altro non cambia abitudini.')

    h(doc, prima, 2, 'Il servizio e il suo contratto')
    par(doc, prima,
        'Si propone un servizio dedicato, **`be-osservabilita`**, con contesto '
        '`/api/v1/osservabilita` e contratto `osservabilita-v1.yaml`. Segue le convenzioni dei '
        'contratti già in casa: percorso che esprime il dominio e non il modulo, verbi dal '
        'vocabolario chiuso, paginazione `pageOffset`/`pageSize`, risposta con `content[]` e '
        '`page{}`.')
    par(doc, prima,
        'La ragione del servizio separato è il **dominio di guasto**: una diagnostica che '
        'si ferma non deve fermare la formazione degli atti, e tenerla dentro il concentratore '
        'legherebbe le due cose. Il prezzo è una quinta unità da gestire, e la scelta '
        'è **OT-10**.')
    tab(OPERAZIONI, [0.4, 2.2, 0.6, 1.3, 2.0])

    h(doc, prima, 2, 'L’operazione di scrittura')
    par(doc, prima,
        '**`creaEventi`** — `POST /api/v1/osservabilita/eventi`. Riceve un **blocco** di '
        'eventi, non uno per volta: il browser li accumula e li consegna a intervalli o '
        'all’abbandono della pagina.')
    codice(doc, prima, [
        'POST /api/v1/osservabilita/eventi',
        'Authorization: Bearer <gettone di sessione>',
        'Content-Type: application/json',
        '',
        '{ "eventi": [',
        '  { "tsEvento":   "2026-11-09T17:42:11.182+01:00",',
        '    "traceId":    "4bf92f3577b34da6a3ce929d0e0e4736",',
        '    "spanId":     "00f067aa0ba902b7",',
        '    "codLivello": "ERROR",',
        '    "codOrigine": "FE",',
        '    "codEvento":  "FE-CHIAMATA-KO",',
        '    "messaggio":  "Chiamata a /ansc/v1/atti fallita dopo 3 tentativi",',
        '    "idAttoSipo": 1842,',
        '    "attributi":  { "stato_http": "502", "tentativi": "3" } } ] }',
        '',
        '201 Created',
        '{ "accolti": 1, "scartati": 0, "motiviScarto": [] }',
    ], 'Il servizio **non si fida** di ciò che riceve: utente, postazione, ambiente e '
       'versione li scrive lui dal gettone e dalla propria configurazione.')
    voce(doc, prima, 'Che cosa il chiamante non può decidere.',
         'Utente, postazione e ambiente non si accettano dal corpo: **un browser non deve '
         'poter dichiarare per conto di chi scrive.** `codServizio` è forzato al '
         'micro-frontend riconosciuto dal gettone.')
    voce(doc, prima, 'Il livello è limitato.',
         'Dal browser si accettano `INFO` e oltre; `DEBUG` e `TRACE` si rifiutano, perché '
         'aprirebbero la porta a un volume senza controllo.')
    voce(doc, prima, 'L’esito è parziale per costruzione.',
         'La risposta dice quanti eventi sono stati accolti e quanti scartati, con il motivo: '
         '**un blocco non viene rifiutato per intero** se una riga è malformata.')
    voce(doc, prima, 'Non è idempotente, e non deve esserlo.',
         'Un evento ripetuto è un fatto, non un errore. Il chiamante però non ritenta '
         'dopo un `429`: rallenta e scarta.')

    h(doc, prima, 2, 'Le operazioni di lettura e ricerca')
    par(doc, prima,
        'Sono tutte in sola lettura, sicure e ripetibili, e hanno `x-effetti: nessuno`. '
        'La prima è quella su cui poggia la worklist del back-office.')
    par(doc, prima,
        '**`cercaEventi`** — `GET /api/v1/osservabilita/eventi`. Ogni filtro non valorizzato '
        'viene ignorato, come negli altri contratti.')
    tab(PARAMETRI_RICERCA, [2.3, 0.9, 3.1])
    par(doc, prima,
        'Una scelta da motivare: **il periodo è obbligatorio.** La tabella è partizionata '
        'per giorno, e una ricerca senza estremi le attraverserebbe tutte — su Oracle, con '
        'milioni di righe, è la differenza fra una risposta immediata e un blocco. Il '
        'back-office propone le ultime ventiquattro ore e l’operatore allarga se serve.')
    par(doc, prima,
        '**`leggiTraccia`** — `GET /api/v1/osservabilita/tracce/{traceId}`. Restituisce '
        'l’oggetto che la Figura della cascata mostra: gli span con inizio, durata, '
        'servizio ed esito, e sotto ciascuno gli eventi agganciati. È l’unica operazione '
        'che compone due letture — gli span e gli eventi — e le restituisce insieme, '
        'perché separarle costringerebbe il front-end a ricucirle.')
    codice(doc, prima, [
        'GET /api/v1/osservabilita/tracce/4bf92f3577b34da6a3ce929d0e0e4736',
        '',
        '200 OK',
        '{ "traceId": "4bf92f35...", "inizio": "...17:42:09.114", "durataMs": 2180,',
        '  "esito": "ERRORE", "codEventoDeterminante": "ANSC-400001",',
        '  "piani": { "atto": { "idAttoSipo": 1842, "numeroAtto": "001842",',
        '                       "idAnsc": null, "codMunicipio": "MUN-01" },',
        '             "allegati": [], "soggetti": [ { "idSoggettoSipo": 55012 } ] },',
        '  "span":   [ { "spanId": "00f0...", "padre": null, "codServizio": "mfOperation",',
        '                "nome": "VALIDA", "inizioMs": 0, "durataMs": 2180, "esito": "KO" } ],',
        '  "eventi": [ { "idEvento": 90412, "spanId": "00f0...", "codLivello": "ERROR",',
        '                "codOrigine": "ANSC", "codEvento": "ANSC-400001" } ] }',
    ], '`codEventoDeterminante` è l’evento più grave della traccia: evita che il '
       'front-end debba calcolarlo per mostrarlo in testa.')
    par(doc, prima,
        '**`elencaEventiOggetto`** — '
        '`GET /api/v1/osservabilita/oggetti/{piano}/{identificativo}/eventi`, dove `piano` vale '
        '`atto`, `allegato` o `soggetto`. È l’operazione che dà corpo ai tre piani: '
        'raccoglie tutto ciò che ha riguardato un oggetto **attraverso tracce diverse e a '
        'settimane di distanza**. Per l’atto risponde a «questo atto è fermo, '
        'perché?»; per l’allegato risponde anche **quando l’allegato non appartiene '
        'ancora ad alcun atto**, che è il caso per cui i piani sono stati separati.')
    par(doc, prima,
        '**`cercaRiepilogo`** — `GET /api/v1/osservabilita/riepilogo`. Stessi filtri della '
        'ricerca, ma restituisce conteggi raggruppati per codice e origine, con il numero di '
        'oggetti distinti coinvolti. È ciò che distingue il caso isolato dal difetto '
        'sistematico, e che il primo livello di supporto guarda prima di aprire una '
        'segnalazione.')
    par(doc, prima,
        '**`leggiEvento`** — `GET /api/v1/osservabilita/eventi/{idEvento}`. Il singolo '
        'evento con tutti i suoi attributi e l’eventuale eccezione. Serve come collegamento '
        'stabile da citare in una segnalazione.')

    h(doc, prima, 2, 'Regole trasversali e codici di errore')
    voce(doc, prima, 'Autorizzazione.',
         'Le operazioni di lettura seguono le abilitazioni del registro delle pagine del '
         'back-office; la scrittura richiede un gettone di sessione valido e **nient’altro**, '
         'perché deve poter registrare anche l’errore di chi non è abilitato a nulla.')
    voce(doc, prima, 'Paginazione.',
         'Identica agli altri contratti, con un massimo di 200 per pagina: oltre, la risposta '
         'pesa più della domanda.')
    voce(doc, prima, 'Conservazione.',
         'Una ricerca fuori dal periodo conservato non è un errore del chiamante: risponde '
         'con l’insieme vuoto e lo dichiara. Un identificativo scaduto dà `404`, e il '
         'back-office lo distingue da «non è mai accaduto».')
    tab(ERRORI_API, [0.9, 2.9, 2.5])

    h(doc, prima, 2, 'Che cosa non si espone, e perché')
    voce(doc, prima, 'Nessuna cancellazione, nessuna modifica.',
         'Il registro è **solo in aggiunta**. Ciò che scade lo elimina '
         'l’amministrazione eliminando una partizione, non una chiamata. Un registro che si '
         'può correggere non è un registro.')
    voce(doc, prima, 'Nessuna operazione che restituisca payload.',
         'Richiesta e risposta verso ANSC restano nell’audit, con la sua conservazione. '
         'Esporle qui aggirerebbe la minimizzazione per la porta di servizio.')
    voce(doc, prima, 'Nessuna configurazione a caldo dei livelli, per ora.',
         'Sarebbe comoda e la si valuta in **OT-11**: il rischio è lasciarla accesa e '
         'scoprirlo dal volume.')


def intesta(doc):
    for fatto in D.frontespizio(doc, '0.2',
                                'PROPOSTA_Osservabilita-OpenTelemetry_v0.2', DATA):
        print('  ' + fatto)
    D.storia(doc, DATA, '0.2', 'Le interfacce · Punti aperti',
             'Nuovo capitolo sulle interfacce, su richiesta del committente: che cosa si '
             'inserisce nei programmi. Distinte quattro interfacce — la libreria in '
             'processo, il trasporto OTLP, l’ingestione REST per il solo browser, le '
             'operazioni di lettura e ricerca per il back-office — e motivato perché i '
             'back-end non devono scrivere i log con chiamate REST. Riportate le firme della '
             'libreria in Java e nel linguaggio dei micro-frontend, con i tre metodi dei piani '
             'che risolvono da sé gli identificativi collegati. Proposto il servizio '
             'be-osservabilita con sei operazioni su /api/v1/osservabilita, secondo le '
             'convenzioni dei contratti già in uso: una di scrittura e cinque di lettura, '
             'con parametri, esempi, regole trasversali e codici di errore. '
             'Tre punti aperti nuovi, OT-10…OT-12.')


if __name__ == '__main__':
    shutil.copyfile(SRC, OUT)
    doc = docx.Document(OUT)

    # refuso introdotto nella revisione in Word
    for fatto in [D.sostituisci(doc, 'Attualmenet Il modulo', 'Attualmente il modulo',
                                attese=1, etichetta='refuso')]:
        pass

    # ⚠️ D.para innesta prima di un ELEMENTO XML, non di un oggetto Paragraph
    ancora = D.h(doc, 1, 'Il back-office del supporto')._p
    modello = doc.tables[-1]
    scrivi(doc, ancora, modello)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
