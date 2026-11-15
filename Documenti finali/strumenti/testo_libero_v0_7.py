# -*- coding: utf-8 -*-
"""v0.7 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC»: la strategia adottata e il secondo punto di
accesso (13/11/2026, con l'utente).

Si parte dal FILE REALE della v0.6, ristrutturato a mano dall'utente la sera del 12/11. Porta
due commenti di Word ancorati al paragrafo dello store («dettagliare gli stati di fase»,
«Chiedere a Rosa»): quei paragrafi non si riscrivono; si corregge soltanto il refuso
«WEBAAPP», che sta in un run a sé.

Che cosa cambia:
  · cap. 4 «Le due strategie proposte» → «La strategia adottata»: la sintesi delle due gestioni
    (compilazione e testo in SIPO dalla G1, numero comunale staccato da SIPO dalla G2, aggancio
    con DEFINISCI invece dell'importazione), figura nuova in PowerPoint
    (DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.3.pptx), tabella dei passi, confronto a tre colonne
    (che stava, con i titoli «Considerazioni…» e «Il confronto», DENTRO la cella della
    comunicazione ANSC). Decisioni dell'utente: la stessa strategia vale per i tipi atto a testo
    libero scelti all'inizio e per le trascrizioni;
  · §2.3: la comunicazione ANSC torna qui, in riquadro; via il «terzo percorso»;
  · §5.1: flusso logico rifatto (DEFINISCI, finestra di aggancio, stato WA), istruzioni agli
    sviluppatori allineate, Figure 4 e 5 rigenerate;
  · §5.2: il numero comunale si stacca prima della stesura dal back-office o con POST /richiesta
    [R3]; flusso logico nuovo (Figura 6), pagine dell'acquisizione rifatte (Figure 7-10),
    tabella di ciò che l'acquisizione scrive;
  · capp. 6 e 7, punti aperti (TL-01 e TL-04 chiusi, TL-13 e TL-14 nuovi), riferimenti.

Figure: diagramma_strategia_pptx.py, diagrammi_testo_libero.py, schermate_tl_definisci.py,
schermate_tl_acquisizione.py (da eseguire prima di questo script).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/testo_libero_v0_7.py
"""
import os
import shutil
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D            # noqa: E402
import testo_libero_v0_6 as V6     # noqa: E402
from testo_libero_v0_6 import _versa, h, par, tabella, voce   # noqa: E402

BASE = V6.BASE
FIN = V6.FIN
NOME = V6.NOME
SRC = os.path.join(FIN, NOME + '_v0.6.docx')
OUT = os.path.join(FIN, NOME + '_v0.7.docx')
IMG = V6.IMG
DATA = '13/11/2026'


# ------------------------------------------------------------------ primitive
def trova(doc, inizio):
    trovati = [p for p in doc.paragraphs if p.text.strip().startswith(inizio)]
    if len(trovati) != 1:
        raise SystemExit('attesa 1 occorrenza di «%s», trovate %d' % (inizio, len(trovati)))
    return trovati[0]


def riscrivi(doc, inizio, nuovo):
    p = trova(doc, inizio)
    if D.ha_commenti(p._p):
        raise SystemExit('paragrafo con commento, non si riscrive: ' + inizio)
    D.testo_di(p, '')
    _versa(p, nuovo)
    return p


def dopo(p):
    """L'elemento prima del quale inserire per scrivere subito dopo p."""
    return p._p.getnext()


def togli(elementi, etichetta):
    for el in elementi:
        if D.ha_commenti(el):
            raise SystemExit('elemento con commento in «%s»: non si elimina' % etichetta)
    for el in elementi:
        el.getparent().remove(el)
    print('  tolti %d elementi: %s' % (len(elementi), etichetta))


def fra(da, a):
    """Gli elementi da «da» (compreso) ad «a» (escluso), fratelli nel corpo."""
    out, el = [], da
    while el is not None and el is not a:
        out.append(el)
        el = el.getnext()
    if el is None:
        raise SystemExit('fine non raggiunta')
    return out


def tabella_che(doc, testa):
    t = [t for t in doc.tables if t.rows[0].cells[0].text.strip() == testa]
    if len(t) != 1:
        raise SystemExit('tabella «%s»: %d' % (testa, len(t)))
    return t[0]


def cella(t, prima_col, col, testo):
    for r in t.rows:
        if r.cells[0].text.strip().startswith(prima_col):
            D.riscrivi_cella(r.cells[col], testo)
            return
    raise SystemExit('riga non trovata: ' + prima_col)


def didascalia(doc, inizio, nuovo):
    p = trova(doc, inizio)
    D.testo_di(p, nuovo)


# =================================================================== contenuti
PASSI = [
    ['#', 'Passo', 'Dove', 'Servizio', 'Stato'],
    ['1', 'Stesura dell’atto fino al Riepilogo, con la ricerca dell’intestatario. Per un '
          'tipo atto a testo libero il testo si scrive nella pagina del testo libero di SIPO, '
          'e si passa direttamente al passo 3.', 'SIPO',
     'R005 `/consultazione/ansc/intestatario`', 'SIPO: 1 IN LAVORAZIONE'],
    ['2', 'Il Riepilogo non trova un UC: messaggio di rinvio alla WebApp, CONFERMA inibito, '
          'niente firmatari né allegati.', 'SIPO', '—', '—'],
    ['3', 'DATI PER ANSC: stacco del numero comunale.', 'SIPO',
     'be-numeratore-comunale `POST /richiesta`', 'numero: Disponibile'],
    ['4', 'Anteprima con il numero comunale in alto; COPIA TESTO copia negli appunti il testo '
          'composto o scritto in SIPO.', 'SIPO', '—',
     'store: WA · ATTESA WEBAPP'],
    ['5', 'Stesura sulla WebApp con il caso d’uso di servizio: numero comunale, testo '
          'incollato, intestatari. Validazione, firme e chiusura sulla WebApp.', 'WebApp ANSC',
     '— (funzioni della WebApp)', 'ANSC: 5 FIRMATO DA USC'],
    ['6', 'Rientro in SIPO: DEFINISCI, abilitato dallo stato WA, apre la finestra di aggancio '
          'con l’atto dal numero comunale coincidente già selezionato.', 'SIPO',
     'R005 `/consultazione/ansc/evento`', '—'],
    ['7', 'Conferma: l’atto è definito con il percorso di salvataggio ordinario.', 'SIPO',
     '`/finalizzaAtto`; be-numeratore-comunale `PUT /utilizza`',
     'SIPO: 2 DEFINITO · store: 5 FIRMATO DA USC · numero: Utilizzato'],
]

CONFRONTO = [
    ['Criterio', 'Gestione 1', 'Gestione 2', 'Strategia adottata'],
    ['Quando si riconosce il caso', 'Tardi: al Riepilogo, dopo l’intera compilazione.',
     'Subito: alla scelta del tipo atto.',
     'Al Riepilogo per i tipi atto ordinari, alla scelta del tipo atto per quelli a testo '
     'libero.'],
    ['Immissioni dei dati', 'Due: in SIPO e di nuovo sulla web app.',
     'Una: sulla web app. SIPO li riceve importandoli.',
     'Una completa, in SIPO. Sulla WebApp si incolla il testo e si riportano gli intestatari e '
     'i pochi dati obbligatori del caso d’uso di servizio.'],
    ['Probabilità di errore', 'Alta: due immissioni dello stesso dato possono divergere.',
     'Bassa: il dato è uno e SIPO lo riceve da ANSC.',
     'Contenuta: il testo è uno solo, copiato; i dati da riportare sono pochi; il numero '
     'comunale preseleziona l’atto da agganciare.'],
    ['Testo dell’atto', 'Generato da SIPO e copiabile.', 'Si scrive sulla web app.',
     'Composto o scritto in SIPO, copiato sulla WebApp con COPIA TESTO.'],
    ['Soggetti in SIPO', 'Già presenti dalla compilazione.',
     'Nascono dall’importazione, con la transcodifica dei luoghi.',
     'Già presenti dalla compilazione: nessuna importazione, nessuna transcodifica inversa.'],
    ['Ritorno in SIPO', 'Ricerca e importazione dei dati.',
     'Ricerca e importazione con la transcodifica.',
     'DEFINISCI: aggancio all’atto ANSC e definizione dell’atto SIPO, in un passaggio.'],
    ['Che cosa resta da costruire', 'Riepilogo senza UC, stato di attesa, ritorno con R005, '
     'importazione.', 'Pagina dello stacco, stato di attesa, ritorno con R005, importazione con '
     'la transcodifica inversa.',
     'Messaggio e DATI PER ANSC nel Riepilogo; COPIA TESTO, DEFINISCI e la finestra di aggancio '
     'nell’Anteprima; lo stato WA.'],
]

CONFRONTO_ACCESSI = [
    ['', 'Atto cominciato in SIPO', 'Atto nato sulla WebApp'],
    ['Il numero comunale', 'Staccato all’Anteprima con DATI PER ANSC: è legato all’atto SIPO.',
     'Staccato prima della stesura, dal back-office o con `POST /richiesta` [R3]: SIPO conosce '
     'il numero, non l’atto.'],
    ['L’atto in SIPO', 'Esiste già, in 1 IN LAVORAZIONE, con dati e testo.',
     'Non esiste: nasce all’acquisizione.'],
    ['Da dove si parte', 'Dall’Anteprima, con DEFINISCI.',
     'Dalla pagina «Recupero Atto ANSC».'],
    ['Come si chiude', 'Un passaggio: finestra di aggancio e conferma.',
     'Ricerca, riepilogo e ACQUISISCI.'],
    ['Che cosa legge SIPO da ANSC', 'L’identificativo e lo stato.',
     'Il modello evento intero, per compilare l’atto.'],
    ['Figure', '2, 3, 4 e 5', '6, 7, 8, 9 e 10'],
]

ACQUISIZIONE = [
    ['Dove', 'Che cosa viene scritto'],
    ['L’atto di SIPO', 'Una riga nuova di `MATR_USR.ATTO`: area e tipo atto scelti nel '
     'riepilogo, numero comunale, anno, data di formazione; `ID_STATO_PRATICA` **2 DEFINITO** e '
     '`DATA_DEFINIZIONE_ATTO`. `FLG_ATTO_TESTOLIBERO` a 1 per un caso d’uso di servizio.'],
    ['`ATTO_TESTO_LIBERO`', 'Per un caso d’uso di servizio, `composizioneCompleta` per intero '
     'nel primo corpo (TL-06).'],
    ['I soggetti', 'Gli intestatari e gli altri soggetti del modello evento, con la '
     'transcodifica di luoghi e cittadinanze (TL-05). Gli identificativi ANSC e ANPR in '
     '`ANSC_SOGGETTO_IDENTIFICATIVI`, e in `ANAG_USR.SOGGETTO` solo se vuoti [R1].'],
    ['`ANSC_STATO_ATTO`', 'Una riga con `ID_ANSC`, `NUMERO_ATTO`, lo stato **5 FIRMATO DA '
     'USC**, `ID_MOTIVO_RECUPERO` e il modello evento letto in `TXT_EVENTO`; e il canale '
     'WEBAPP, che ANSC non registra e che va aggiunto allo store [R4].'],
    ['Il numeratore comunale', 'Il numero passa da Disponibile a **Utilizzato** con '
     'l’identificativo ANSC (`PUT /utilizza`).'],
]


# =================================================================== interventi
def frontespizio_e_scopo(doc):
    for p in doc.paragraphs:
        if p.style.name == 'Subtitle' and p.text.startswith('Gli atti a testo libero'):
            D.testo_di(p, 'Gli atti a testo libero e gli atti senza caso d’uso: la strategia '
                          'adottata, le pagine di SIPO e i servizi ANSC da usare')
    riscrivi(doc, 'Riprende il capitolo «Atti a Testo Libero»',
             'Riprende il capitolo «Atti a Testo Libero» dell’analisi di integrazione [R1] e lo '
             'sviluppa: che cosa sono questi atti in SIPO e in ANSC, quando si ricorre a essi, '
             'la strategia adottata — una sintesi delle due proposte dell’analisi —, le '
             'pagine di SIPO e i servizi ANSC che occorrono. Tratta anche il secondo punto di '
             'accesso: l’atto formato interamente sulla WebApp, senza essere mai cominciato in '
             'SIPO, che SIPO acquisisce. Tiene conto della comunicazione ANSC sui casi d’uso di '
             'servizio [A6]. Le decisioni ancora da prendere sono raccolte in coda, come punti '
             'aperti TL-01…TL-14.')
    riscrivi(doc, 'Due caratteristiche del caso d’uso di servizio',
             'Tre caratteristiche del caso d’uso di servizio contano per il disegno:')


def riferimenti(doc):
    t = [x for x in doc.tables if x.rows[0].cells[0].text.strip() == '#'
         and x.rows[0].cells[1].text.strip() == 'Riferimento'][0]
    cella(t, '[R2]', 1, 'DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.3.pptx — la strategia '
                        'adottata in PowerPoint, modificabile. La v0.2 riporta le due '
                        'gestioni dell’analisi.')
    D.clona_riga(t, ('[R3]', 'PROCESSO_Numerazione-Comunale_SIPO-ANSC_v0.5.docx — la '
                     'numerazione comunale: pagina della richiesta nel back-office, servizio '
                     'be-numeratore-comunale (POST /richiesta, GET /ricerca, PUT /utilizza, '
                     'PUT /scarta), scenari 1 e 6 (atto formato sulla web app, aggancio).',
                     'Documento di progetto'))
    D.clona_riga(t, ('[R4]', 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.3.docx — gli atti '
                     'formati sulla web app con numero staccato in SIPO: livelli di presenza '
                     'in SIPO, registrazione del canale, pagina del back-office per il recupero.',
                     'Documento di progetto'))


def comunicazione(doc):
    """§2.3 senza il terzo percorso, e il riquadro della comunicazione ANSC riportato qui."""
    riscrivi(doc, 'Ne discende che il percorso dipende',
             'Per una dichiarazione a testo libero, quindi, l’atto si forma sulla web app. Per '
             'una trascrizione il gestionale potrebbe ancora depositare l’atto con il caso '
             'd’uso di servizio, ma solo finché dura la fase ibrida, la cui fine ANSC lega '
             'all’adesione di tutti i comuni senza indicarne la data. La strategia adottata '
             '(capitolo seguente) non usa questa possibilità: dichiarazioni e trascrizioni '
             'seguono lo stesso percorso, che non cambierà quando la fase ibrida finirà.')
    p3 = riscrivi(doc, 'La stessa comunicazione suggerisce',
                  'La stessa comunicazione suggerisce alle case software di sviluppare servizi '
                  'per recuperare gli atti registrati sulla web app, così da mantenere '
                  'allineati i sistemi locali e svolgere gli adempimenti successivi [A6]. È '
                  'ciò che fanno, nel capitolo «Le pagine di SIPO», DEFINISCI per l’atto '
                  'cominciato in SIPO e l’acquisizione per l’atto nato sulla WebApp.')

    note = [t for t in doc.tables if t.rows[0].cells[0].text.strip().startswith('Si comunica')]
    if len(note) != 1:
        raise SystemExit('riquadro della comunicazione: %d' % len(note))
    riquadro = note[0]
    c = riquadro.rows[0].cells[0]
    # fuori dalla cella i titoli e il confronto finiti dentro per errore
    figli = list(c._tc)
    inizio = None
    for i, el in enumerate(figli):
        if el.tag.endswith('}p') and Paragraph(el, c).text.strip().startswith(
                'Considerazioni sulle due strategie'):
            inizio = i
    if inizio is None:
        raise SystemExit('titolo «Considerazioni» non trovato nella cella')
    togli(figli[inizio:], 'considerazioni e confronto dentro la cella')
    if not figli[inizio - 1].tag.endswith('}p'):
        c.add_paragraph()

    # il titolo «Note» del cap. 5 e il riquadro si spostano nel §2.3
    nota = D.h(doc, 2, 'Note', esatto=True)
    togli([nota._p], 'titolo «Note»')
    p3._p.addnext(riquadro._tbl)
    par(doc, riquadro._tbl, 'Il testo della comunicazione [A6] è riportato nel riquadro che '
                            'segue.')


def tabella_quando(doc):
    t = tabella_che(doc, 'Situazione')
    cella(t, 'L’ufficiale sceglie un tipo atto a testo libero', 2,
          'Apre la pagina del testo libero, dove l’ufficiale scrive il testo; da lì DATI PER '
          'ANSC.')
    cella(t, 'L’ufficiale sceglie un tipo atto a testo libero', 3,
          'Testo libero: la strategia adottata, dal passo dello stacco del numero.')
    cella(t, 'Nessuna condizione di applicabilità', 3,
          'Testo libero: la strategia adottata, dal Riepilogo.')
    D.sostituisci(doc, 'Per le trascrizioni l’esito «testo libero» non porta alla web app ma '
                       'al terzo percorso, interamente in SIPO.',
                  'Lo stesso vale per le trascrizioni.', attese=1, etichetta='cap. 3')


def capitolo_4(doc):
    testa = D.h(doc, 1, 'Le due strategie proposte', esatto=True)
    D.testo_di(testa, 'La strategia adottata')
    cap5 = D.h(doc, 1, 'Gli atti a testo libero partendo')
    vecchio = fra(dopo(testa), cap5._p)
    togli(vecchio, 'le due strategie, con la figura e le due tabelle dei passi')

    a = cap5._p
    modello = tabella_che(doc, 'Situazione')
    par(doc, a, 'L’analisi di integrazione [R1] propone due modalità per gli atti che SIPO non '
                'gestisce in automatico. In entrambe l’atto si forma sulla web app e il numero '
                'comunale esce da SIPO, perché SIPO è l’unico luogo in cui la serie è '
                'governata. **La strategia adottata non è né l’una né l’altra: ne è una '
                'sintesi**, e vale per le dichiarazioni, per le quali la web app è l’unica via '
                '[A6], come per le trascrizioni.')

    h(doc, a, 2, 'Le due gestioni dell’analisi')
    voce(doc, a, 'Gestione 1 — l’atto scoperto al Riepilogo.', 'L’atto si compila in SIPO e '
         'l’assenza di un UC emerge al Riepilogo. Sulla web app l’atto si forma con il caso '
         'd’uso di servizio, e i dati vanno immessi una seconda volta; al ritorno SIPO ritrova '
         'l’atto con R005 e ne importa i dati. L’analisi la qualifica come onerosa e '
         'rischiosa.')
    voce(doc, a, 'Gestione 2 — l’atto a testo libero riconosciuto alla richiesta.', 'Il caso si '
         'riconosce alla scelta del tipo atto: SIPO stacca il numero e manda l’ufficiale sulla '
         'web app, dove l’atto si stende con qualsiasi UC. Al ritorno SIPO importa ciò che '
         'ANSC ha formato, con la transcodifica dei luoghi.')
    par(doc, a, 'La Gestione 1 tiene i dati in SIPO ma li fa immettere due volte; la Gestione 2 '
                'li fa immettere una volta, ma sulla web app, e obbliga SIPO a ricostruirli '
                'importandoli. Nessuna delle due ricava vantaggio dal fatto che, al ritorno, '
                'SIPO ha già tutto tranne l’identificativo ANSC.')

    h(doc, a, 2, 'La sintesi adottata')
    par(doc, a, 'La strategia prende da ciascuna gestione ciò che funziona e cambia il ritorno:')
    voce(doc, a, 'Dalla Gestione 1:', 'l’atto si compila in SIPO, che ne compone il testo; '
         'SIPO resta la fonte dei dati dell’atto.')
    voce(doc, a, 'Dalla Gestione 2:', 'il numero comunale lo stacca SIPO prima di andare sulla '
         'web app, e l’ufficiale lo riporta nell’atto.')
    voce(doc, a, 'Nuovo:', 'al ritorno non si importano i dati. **DEFINISCI aggancia l’atto ANSC '
         'e definisce l’atto SIPO in un passaggio solo**: l’atto SIPO va in 2 DEFINITO con il '
         'percorso di salvataggio ordinario, lo store riceve l’identificativo ANSC e lo stato '
         '5 FIRMATO DA USC. Fra un momento e l’altro lo store è nello stato WA · ATTESA '
         'WEBAPP e l’atto SIPO resta in 1 IN LAVORAZIONE.')
    D.immagine(doc, a, os.path.join(IMG, 'strategia_adottata.png'), 5.6,
               'Figura 1 — Gli atti che SIPO non gestisce in automatico: la strategia adottata '
               '[R2].')
    par(doc, a, 'I passi, con i servizi chiamati e gli stati:')
    tabella(doc, a, PASSI, modello, [0.3, 2.6, 0.8, 1.4, 1.4])
    par(doc, a, 'Il tipo atto a testo libero scelto all’inizio segue la stessa strada: il testo '
                'si scrive nella pagina del testo libero che SIPO ha già, e da lì si passa a '
                'DATI PER ANSC. Le pagine e il flusso di dettaglio sono nel capitolo «Le pagine '
                'di SIPO».')

    h(doc, a, 2, 'Il confronto')
    tabella(doc, a, CONFRONTO, modello, [1.3, 1.6, 1.6, 1.9])
    par(doc, a, 'Il punto su cui la sintesi è più debole è la seconda immissione degli '
                'intestatari sulla WebApp: è ridotta al minimo dal caso d’uso di servizio, che '
                'chiede pochi dati, ma non è eliminata, e nessun controllo la confronta con i '
                'dati di SIPO. Il riepilogo dell’atto scelto nella finestra di aggancio è il '
                'momento in cui l’ufficiale può accorgersi di una divergenza.')

    h(doc, a, 2, 'Il secondo punto di accesso: gli atti formati interamente sulla WebApp')
    par(doc, a, 'Un atto può anche nascere e chiudersi sulla WebApp senza essere mai cominciato '
                'in SIPO. Il numero comunale lo stacca comunque SIPO, prima della stesura: '
                'dalla pagina della richiesta del back-office oppure, da un altro applicativo, '
                'con `POST /richiesta` del servizio be-numeratore-comunale, come descritto nel '
                'documento di processo della numerazione comunale [R3]. Al rientro SIPO non ha '
                'un atto da definire ma un numero impegnato: l’atto lo **acquisisce** da ANSC, '
                'con la pagina «Recupero Atto ANSC» descritta nel capitolo seguente.')


def capitolo_5(doc):
    testa = D.h(doc, 1, 'Gli atti a testo libero partendo')
    D.testo_di(testa, 'Le pagine di SIPO')
    riscrivi(doc, 'Il capitolo disegna le pagine di SIPO',
             'Il capitolo disegna le pagine di SIPO della strategia adottata: per l’atto di cui '
             'al Riepilogo non viene identificato un UC, che SIPO definisce con DEFINISCI, e per '
             'l’atto formato interamente sulla WebApp, che SIPO acquisisce. Le pagine partono '
             'da schermate reali di SIPO (Riepilogo, Anteprima, Gestione Decessi), ritoccate '
             'secondo la sequenza indicata dal committente; i numeri gialli sulle figure sono i '
             'passi della sequenza. L’esempio è un atto di morte in abitazione a Roma.')
    riscrivi(doc, 'Il flusso va dalla determinazione',
             'Il flusso va dalla determinazione dell’UC alla definizione dell’atto in SIPO. A '
             'destra sono indicati i servizi chiamati; in viola il lavoro che l’ufficiale svolge '
             'sulla WebApp, fuori da SIPO. A sinistra l’ingresso del tipo atto a testo libero, '
             'che salta il Riepilogo.')
    D.sostituisci_immagine(doc, 'Figura 2 —', os.path.join(IMG, 'tl_flusso_definisci.png'))
    didascalia(doc, 'Figura 2 —', 'Figura 2 — Atto senza UC: dal Riepilogo alla WebApp ANSC e '
                                  'a DEFINISCI.')
    riscrivi(doc, 'Due cicli regolano il ritorno',
             'Il ritorno ha una sola decisione. Se nella finestra di aggancio compare l’atto con '
             'il numero comunale staccato, l’ufficiale conferma; altrimenti digita '
             'l’identificativo ANSC, se lo ha annotato, oppure usa la ricerca puntuale. Finché '
             'l’atto ANSC non è agganciato lo store resta in WA e l’atto SIPO in 1 IN '
             'LAVORAZIONE: DEFINISCI resta disponibile e il back-office ne segnala '
             'l’anzianità.')

    # istruzioni per gli sviluppatori: le ultime due voci dicevano «modale in attesa»
    riscrivi(doc, 'La nuova pagina mostra una modale',
             'Al rientro DEFINISCI, abilitato dallo stato WA, apre la finestra di aggancio: '
             'cerca con R005 gli atti del giorno e preseleziona quello con il numero comunale '
             'staccato; in alternativa l’identificativo ANSC si digita.')
    riscrivi(doc, 'Operazione completata.',
             'Alla conferma l’atto è definito: `/finalizzaAtto` (2 DEFINITO), '
             '`ANSC_STATO_ATTO` con `ID_ANSC` e lo stato 5, `PUT /utilizza` sul numero. '
             'Operazione completata.')

    # il refuso «WEBAAPP» sta in un run a sé, nel paragrafo commentato
    p = trova(doc, 'Viene inserito un record sulla tabella')
    corretti = 0
    for i, r in enumerate(p.runs[:-1]):
        if r.text == 'A' and p.runs[i + 1].text.startswith('APP'):
            r.text = ''
            corretti += 1
    if corretti != 1:
        raise SystemExit('refuso WEBAAPP: %d' % corretti)

    D.sostituisci_immagine(doc, 'Figura 4 —', os.path.join(IMG, 'tl_2_anteprima_numero.png'))
    didascalia(doc, 'Figura 4 —', 'Figura 4 — Anteprima: il numero comunale in alto, COPIA '
                                  'TESTO e DEFINISCI, abilitato dallo stato WA.')
    D.sostituisci_immagine(doc, 'Figura 5 —', os.path.join(IMG, 'tl_2b_definisci_modale.png'))
    riscrivi(doc, '5 bis — DEFINISCI.',
             '**5 bis — DEFINISCI.** Il bottone compare accanto a COPIA TESTO e si abilita '
             'quando lo store passa nello stato WA, cioè all’Anteprima. È **lo stato sullo store '
             'ad abilitarlo, non il clic nella sessione del browser**: l’operatore esce da SIPO, '
             'forma l’atto sulla WebApp e rientra dopo minuti, magari riaprendo la pagina. Se '
             'dipendesse dal clic, al rientro il bottone sparirebbe; dipendendo dallo stato WA, '
             'al rientro è già lì.')
    riscrivi(doc, 'Quando l’atto non compare.',
             '**Quando l’atto non compare.** Un rimando porta alla **ricerca puntuale** descritta '
             'nel paragrafo «Gli atti formati interamente in ANSC», per intestatario o su un '
             'intervallo di date più largo; in questo caso l’atto trovato si aggancia, non si '
             'acquisisce. Non si duplica dentro la finestra ciò che esiste già come pagina.')

    # la tabella dei due casi lascia il §5.1 e va, corretta, nel §5.2
    via = D.h(doc, 3, 'Gli atti nati interamente sulla WebApp', esatto=True)
    s52 = D.h(doc, 2, 'Gli atti formati interamente in ANSC')
    togli(fra(via._p, s52._p), 'sezione «Gli atti nati interamente sulla WebApp» del §5.1')


def sezione_5_2(doc):
    modello = tabella_che(doc, 'Situazione')
    riscrivi(doc, 'Gli atti possono essere effettuati anche direttamente',
             'Un atto può essere formato anche interamente sulla WebApp, senza essere mai '
             'cominciato in SIPO: un atto a testo libero redatto direttamente in ANSC, ma anche '
             'un atto con un caso d’uso ordinario. Il problema è riportarlo in SIPO.')
    riscrivi(doc, 'Il punto di aggancio è lo stacco',
             'Il punto di aggancio è lo stacco del numero comunale. L’ufficiale lo chiede prima '
             'della stesura, dalla pagina della richiesta del back-office oppure, da un altro '
             'applicativo, con `POST /richiesta` del servizio be-numeratore-comunale. La '
             'funzione esiste ed è descritta nel documento di processo della numerazione '
             'comunale [R3] (scenari 1 e 6, pagina della richiesta, servizio '
             'be-numeratore-comunale). Con il numero in mano la WebApp porta a termine la '
             'stesura dell’atto.')
    ultimo = riscrivi(doc, 'A questo punto l',
                      'Il meccanismo di rientro prevede la scelta degli atti formati in ANSC, '
                      'filtrati per giorno o periodo, comune e tipo di atto, e la possibilità di '
                      '**acquisirli**: con l’azione ACQUISISCI SIPO compila i propri dati a '
                      'partire dal modello evento letto con R005.')

    a = dopo(ultimo)
    # le figure del recupero scalano di uno: dalla più alta, per non accavallarsi
    for vecchio, nuovo in ((9, 'Figura 10 — La conferma dell’acquisizione.'),
                           (8, 'Figura 9 — Acquisizione dell’atto ANSC: il riepilogo prima di '
                               'ACQUISISCI.'),
                           (7, 'Figura 8 — Recupero dell’atto ANSC: la ricerca puntuale.'),
                           (6, 'Figura 7 — Recupero dell’atto ANSC: gli atti del periodo, con '
                               'la colonna «In SIPO».')):
        didascalia(doc, 'Figura %d —' % vecchio, nuovo)
    for n, png in ((7, 'tl_7_acq_periodo.png'), (8, 'tl_8_acq_ricerca.png'),
                   (9, 'tl_9_acq_riepilogo.png'), (10, 'tl_10_acq_conferma.png')):
        D.sostituisci_immagine(doc, 'Figura %d —' % n, os.path.join(IMG, png))

    h(doc, a, 3, 'Il flusso logico')
    par(doc, a, 'Il flusso va dallo stacco del numero alla creazione dell’atto in SIPO. Le '
                'decisioni sono due: se l’atto compare fra quelli del periodo, e se il suo '
                'numero comunale è fra quelli staccati da SIPO.')
    D.immagine(doc, a, os.path.join(IMG, 'tl_flusso_acquisizione.png'), 6.0,
               'Figura 6 — Atto formato interamente sulla WebApp: l’acquisizione in SIPO.')
    par(doc, a, 'Un atto che non compare può non essere ancora firmato: il numero resta '
                'Disponibile e la ricerca si ripete più tardi. Un atto il cui numero non è fra '
                'quelli staccati da SIPO si può acquisire con un avviso, secondo la decisione '
                'di TL-12.')
    h(doc, a, 3, 'Rispetto all’atto cominciato in SIPO')
    par(doc, a, 'Le pagine di ricerca sono le stesse che la finestra di DEFINISCI usa come '
                'ricerca estesa; cambia ciò che succede dopo:')
    tabella(doc, a, CONFRONTO_ACCESSI, modello, [1.3, 2.6, 2.5])

    # la ricerca: periodo e colonna «In SIPO» al posto del numero atteso
    riscrivi(doc, 'Al rientro, la pagina «Recupero Atto ANSC» propone',
             'La pagina «Recupero Atto ANSC» propone gli atti firmati nel periodo, per difetto '
             'il giorno corrente, ottenuti con R005 `/consultazione/ansc/evento`. I criteri:')
    t = tabella_che(doc, 'Criterio nella pagina')
    cella(t, 'Data da', 1, 'il giorno corrente, modificabile per un periodo')
    cella(t, 'Numero comunale atteso', 0, 'In SIPO')
    cella(t, 'In SIPO', 1, 'calcolata da SIPO; «Mostra» nasconde gli atti già noti')
    cella(t, 'In SIPO', 2, 'Non è un criterio: SIPO confronta idAnsc con ANSC_STATO_ATTO '
                           '(atto già noto) e numeroatto con i numeri staccati e non '
                           'utilizzati (be-numeratore-comunale GET /ricerca).')
    D.sostituisci(doc, 'intestatario, data di nascita e stato.',
                  'intestatario, data di nascita e la colonna «In SIPO»: da acquisire con il '
                  'numero staccato, oppure con un numero non staccato da SIPO (TL-12).',
                  attese=1, etichetta='colonne dei risultati')
    riscrivi(doc, 'Se fra gli atti del giorno il numero comunale non compare',
             'Se l’atto non compare nel periodo, la seconda linguetta offre due modi di cercare:')
    D.sostituisci(doc, 'numero comunale con il riscontro rispetto al numero staccato',
                  'numero comunale con il riscontro sui numeri staccati da SIPO', attese=1,
                  etichetta='riepilogo')
    D.testo_di(D.h(doc, 3, 'Il riepilogo dell’atto ANSC e la conferma', esatto=True),
               'Il riepilogo e l’acquisizione')
    p = riscrivi(doc, 'Che cosa SIPO aggiorna.',
                 '**Tipo atto in SIPO.** Proposto dal caso d’uso: per un caso d’uso di '
                 'servizio, il tipo atto a testo libero dell’area; per un caso d’uso ordinario, '
                 'il tipo atto che la configurazione lega all’UC. L’ufficiale lo può cambiare.')
    riscrivi(doc, 'La conferma è esplicita',
             'La conferma è esplicita: una finestra riepiloga identificativo ANSC e numero '
             'comunale e avverte che l’atto sarà registrato in SIPO già definito. In quel '
             'momento:')
    fine = trova(doc, 'La conferma è esplicita')
    a = dopo(fine)
    tabella(doc, a, ACQUISIZIONE, modello, [1.5, 4.9])
    par(doc, a, 'Per un caso d’uso di servizio i dati da acquisire sono pochi, l’intestatario e '
                'il testo, e l’acquisizione è completa. Per un atto con caso d’uso ordinario, '
                'formato sulla WebApp per scelta, l’acquisizione completa richiede la '
                'transcodifica inversa dell’intero modello evento; l’analisi del recupero '
                '[R4] propone in quel caso, come regola, una scheda essenziale. Quale livello '
                'adottare è TL-13.')
    return p


def capitoli_6_7(doc):
    riscrivi(doc, 'Per le trascrizioni SIPO usa i servizi',
             'Nella strategia adottata SIPO non deposita e non firma, né per le dichiarazioni '
             'né per le trascrizioni: lo fa la WebApp, e i servizi che SIPO chiama sono quasi '
             'tutti letture, concentrate nel ritorno. Nelle colonne «Da SIPO» (atto cominciato '
             'in SIPO e definito con DEFINISCI) e «Da WebApp» (atto acquisito), «sì» indica il '
             'servizio necessario, «cond.» quello necessario solo in una condizione, «facolt.» '
             'quello facoltativo, «ind.» quello usato indirettamente.')
    t = [x for x in doc.tables if x.rows[0].cells[0].text.strip() == 'Servizio'
         and x.rows[0].cells[1].text.strip() == 'Operazione'][0]
    D.riscrivi_cella(t.rows[0].cells[3], 'Da SIPO')
    D.riscrivi_cella(t.rows[0].cells[4], 'Da WebApp')
    valori = {  # riga (per operazione e scopo) → (Da SIPO, Da WebApp)
        'Ricerca dell’intestatario': ('sì', '—'),
        'Ritrova l’atto': ('sì', 'sì'),
        'Ricerca puntuale': ('cond.', 'cond.'),
        'Completa i dati': ('—', 'facolt.'),
        'Recupera i documenti': ('—', 'facolt.'),
        'Registra la data': ('cond.', 'cond.'),
        'Verifica le notifiche': ('facolt.', 'facolt.'),
        'Recupera le comunicazioni': ('facolt.', 'facolt.'),
        'Rileva una nota': ('facolt.', 'facolt.'),
        'Dizionari ANSC': ('—', 'ind.'),
    }
    fatti = 0
    for r in t.rows[1:]:
        for chiave, (a, b) in valori.items():
            if r.cells[2].text.strip().startswith(chiave):
                D.riscrivi_cella(r.cells[3], a)
                D.riscrivi_cella(r.cells[4], b)
                fatti += 1
    if fatti != len(valori):
        raise SystemExit('righe dei servizi: %d su %d' % (fatti, len(valori)))
    for r in t.rows:
        if r.cells[2].text.strip().startswith('Ritrova l’atto'):
            D.riscrivi_cella(r.cells[2], 'Ritrova l’atto formato sulla WebApp: a DEFINISCI '
                                         'basta l’identificativo; all’acquisizione serve il '
                                         'modello evento intero.')
        if r.cells[2].text.strip().startswith('Ricerca puntuale'):
            D.riscrivi_cella(r.cells[5], 'Solo se l’atto non compare fra i candidati del '
                                         'giorno, o nel periodo.')
        if r.cells[2].text.strip().startswith('Dizionari ANSC'):
            D.riscrivi_cella(r.cells[2], 'Dizionari ANSC per la transcodifica inversa dei '
                                         'valori acquisiti.')
    for r in t.rows:
        for j, (vecchio, nuovo) in ((2, ('di un soggetto importato', 'di un soggetto acquisito')),
                                    (5, ('se l’importazione lo richiede',
                                         'se l’acquisizione lo richiede')),
                                    (5, ('nel modello evento importato', 'nel modello evento '
                                                                         'letto'))):
            if vecchio in r.cells[j].text:
                D.riscrivi_cella(r.cells[j], r.cells[j].text.replace(vecchio, nuovo))
    D.sostituisci(doc, 'Accanto ai servizi ANSC, le strategie usano il servizio della '
                       'numerazione be-numeratore-comunale [R1]: POST /richiesta allo stacco, '
                       'PUT /utilizza alla conclusione, PUT /scarta all’abbandono.',
                  'Accanto ai servizi ANSC, la strategia usa il servizio della numerazione '
                  'be-numeratore-comunale [R1] [R3]: POST /richiesta allo stacco, da DATI PER '
                  'ANSC oppure dal back-office per l’atto formato sulla WebApp; PUT /utilizza a '
                  'DEFINISCI o all’acquisizione; PUT /scarta all’abbandono.',
                  attese=1, etichetta='numerazione')
    D.sostituisci(doc, 'i servizi della formazione che nelle due strategie esegue la web app',
                  'i servizi della formazione che nella strategia adottata esegue la web app',
                  attese=1, etichetta='servizi non chiamati')
    t = [x for x in doc.tables if x.rows[0].cells[0].text.strip() == 'Servizio'
         and x.rows[0].cells[1].text.strip().startswith('Perché')][0]
    cella(t, 'R009', 1, 'Il deposito avviene sulla WebApp. Per le dichiarazioni il caso d’uso '
                        'di servizio non è disponibile tramite servizi cooperativi dal '
                        '09/09/2024 [A6]; per le trascrizioni lo è ancora, nella fase ibrida, '
                        'ma la strategia non lo usa: il percorso è uno solo e non cambia quando '
                        'la fase ibrida finirà.')
    cella(t, 'R010', 1, 'L’anteprima dell’atto la mostra la web app. Quella con COPIA TESTO è '
                        'l’anteprima di SIPO.')

    t = tabella_che(doc, 'Struttura')
    D.sostituisci(doc, 'Che cosa le strategie richiedono al modello dati',
                  'Che cosa la strategia richiede al modello dati', attese=1, etichetta='cap. 7')
    cella(t, 'ANSC_STATO_ATTO', 1, 'Lo stato applicativo WA · ATTESA WEBAPP, dall’Anteprima; '
                                   'gli stati di COD_FASE delle pagine del percorso, da '
                                   'dettagliare (TL-03). A DEFINISCI o all’acquisizione, '
                                   'ID_ANSC e lo stato 5 FIRMATO DA USC. Per un atto acquisito, '
                                   'il canale WEBAPP [R4].')
    cella(t, 'ANSC_STATO_ATTO.ID_MOTIVO_RECUPERO', 1, 'Valorizzato dal modello evento letto con '
                                                      'R005 (atteso 3).')
    cella(t, 'MATR_USR.ATTO.FLG_ATTO_TESTOLIBERO', 1, 'Posto a 1 per un atto a testo libero o '
                                                      'formato con un caso d’uso di servizio, a '
                                                      'DEFINISCI come all’acquisizione.')
    cella(t, 'ATTO_TESTO_LIBERO', 1, 'Per l’atto cominciato in SIPO contiene già il testo. Per '
                                     'l’atto acquisito riceve composizioneCompleta: la divisione '
                                     'in corpi e formule non è ricostruibile, il testo va per '
                                     'intero nel primo corpo (TL-06).')
    cella(t, 'ANSC_SOGGETTO_IDENTIFICATIVI', 1, 'Gli identificativi dei soggetti acquisiti, con '
                                                'la regola «solo se vuoto» verso l’anagrafe '
                                                '[R1].')
    cella(t, 'Back-office', 1, 'Una categoria di eccezione «In attesa della stesura sulla web '
                               'app» (stato WA), con l’anzianità in evidenza; i numeri staccati '
                               'per la WebApp e non ancora acquisiti; l’abbandono che porta il '
                               'numero a Scartato (PUT /scarta).')
    cella(t, 'Configurazione dei tipi atto', 1, 'Per ciascun tipo atto a testo libero, il caso '
                                                'd’uso di servizio da usare sulla WebApp; nel '
                                                'verso opposto, il tipo atto SIPO da proporre '
                                                'all’acquisizione per ciascun caso d’uso.')
    cella(t, 'Pagine di SIPO', 1, 'Riepilogo senza UC con il messaggio e DATI PER ANSC; '
                                  'nell’Anteprima il pannello del numero comunale, COPIA TESTO e '
                                  'DEFINISCI con la finestra di aggancio; pagina nuova «Recupero '
                                  'Atto ANSC» con due linguette; pagina nuova «Acquisizione Atto '
                                  'ANSC» con ACQUISISCI.')


def punti_aperti(doc):
    riscrivi(doc, 'Dodici questioni restano da chiudere',
             'Le questioni sono quattordici; TL-01 e TL-04 sono chiuse dalla strategia '
             'adottata. Le altre servono a completare il disegno: gli stati dello store (TL-03), '
             'la transcodifica e il testo dell’atto acquisito (TL-05, TL-06), la permanenza in '
             'attesa (TL-07), il numero comunale non coincidente (TL-12) e la nuova funzione di '
             'acquisizione (TL-13, TL-14). I punti si legano a OP-66, OP-71, OP-78 e OP-79 '
             'dell’analisi di integrazione [R1].')
    t = [x for x in doc.tables if x.rows[0].cells[0].text.strip() == '#'
         and x.rows[0].cells[1].text.strip() == 'Questione'][0]
    cella(t, 'TL-01', 1, 'Chiuso: si adotta la sintesi delle due gestioni (capitolo «La '
                         'strategia adottata»), per le dichiarazioni e per le trascrizioni.')
    cella(t, 'TL-02', 1, 'Chiuso nel merito dalla comunicazione ANSC [A6]: i casi d’uso di '
                         'servizio delle dichiarazioni sono solo sulla web app, quelli delle '
                         'trascrizioni restano cooperativi nella fase ibrida, ma la strategia '
                         'non li usa. Resta la prenotazione dei gemelli, che con R009 '
                         '/prenota/evento predispone atti con il caso d’uso 11999999, non più '
                         'cooperativo: se prenotazione e completamento delle bozze siano ancora '
                         'possibili dal gestionale (si lega a OP-46 di [R1]).')
    cella(t, 'TL-03', 1, 'Lo stato applicativo è WA · ATTESA WEBAPP. Restano da dettagliare gli '
                         'stati di COD_FASE delle pagine del percorso e il posto di WA fra gli '
                         'stati applicativi di ANSC_STATO_ATTO.')
    cella(t, 'TL-04', 1, 'Chiuso: l’atto cominciato in SIPO si conclude con DEFINISCI, nello '
                         'stato 2 DEFINITO, con il percorso di salvataggio ordinario; l’atto '
                         'acquisito nasce in SIPO già nello stato 2.')
    cella(t, 'TL-06', 1, 'Collocazione del testo acquisito in ATTO_TESTO_LIBERO (primo corpo, '
                         'formule vuote) e resa dell’anteprima di SIPO su un testo non composto '
                         'da SIPO.')
    cella(t, 'TL-07', 1, 'Termine massimo di permanenza nello stato WA, e sorte del numero '
                         'staccato per un atto mai formato o mai acquisito.')
    cella(t, 'TL-08', 1, 'Se formare sulla WebApp, e poi acquisire, anche atti con un UC '
                         'ordinario, per gli UC meno complessi, sia ammesso e in quali casi: è '
                         'una scelta organizzativa.')
    cella(t, 'TL-12', 1, 'Che cosa fare se l’atto ritrovato porta un numero comunale diverso da '
                         'quello staccato o, per un atto acquisito, un numero non staccato da '
                         'SIPO: bloccare la conferma, oppure consentirla con un avviso e chiudere '
                         'come Scartato il numero staccato. Un numero sbagliato in un atto '
                         'firmato si corregge solo con la nota tecnica sulla WebApp.')
    D.clona_riga(t, ('TL-13', 'Livello dell’acquisizione per un atto con caso d’uso ordinario '
                     'formato sulla WebApp: atto completo, con la transcodifica inversa '
                     'dell’intero modello evento, oppure scheda essenziale come propone '
                     'l’analisi del recupero [R4].', 'Analisi / Cliente'))
    D.clona_riga(t, ('TL-14', 'Dove si colloca nel menu la pagina «Recupero Atto ANSC», chi la '
                     'usa (ufficiale o back-office) e come si raccorda con la pagina del '
                     'back-office per il recupero proposta in [R4].', 'Cliente'))


def intesta(doc):
    for fatto in D.frontespizio(doc, '0.7', NOME + '_v0.7', DATA):
        print('  ' + fatto)
    D.storia(doc, DATA, '0.7', '1 · 2.3 · 3 · 4 · 5 · 6 · 7 · Punti aperti · Riferimenti',
             'Il capitolo 4 diventa «La strategia adottata»: una sintesi delle due gestioni, '
             'con la compilazione e il testo in SIPO, il numero comunale staccato da SIPO prima '
             'della WebApp e il ritorno con DEFINISCI invece dell’importazione; vale anche per '
             'i tipi atto a testo libero e per le trascrizioni. Figura in PowerPoint, tabella '
             'dei passi e confronto a tre colonne. Il secondo punto di accesso, l’atto formato '
             'interamente sulla WebApp, ha il numero staccato dal back-office o con POST '
             '/richiesta [R3], un flusso logico e le pagine dell’acquisizione rifatte. Il flusso '
             'logico dell’atto senza UC è rifatto con DEFINISCI e lo stato WA. La comunicazione '
             'ANSC torna nel paragrafo 2.3. Chiusi TL-01 e TL-04, nuovi TL-13 e TL-14.')


if __name__ == '__main__':
    shutil.copyfile(SRC, OUT)
    doc = docx.Document(OUT)
    frontespizio_e_scopo(doc)
    riferimenti(doc)
    comunicazione(doc)
    tabella_quando(doc)
    capitolo_4(doc)
    capitolo_5(doc)
    sezione_5_2(doc)
    capitoli_6_7(doc)
    punti_aperti(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
