# -*- coding: utf-8 -*-
"""Genera «PROCEDURA_Formazione-Atto_SIPO-ANSC» — il percorso dell'operatore, passo per passo.

Il documento risponde a una domanda che l'analisi tratta per parti sparse: che cosa fa
concretamente chi forma un atto, dal menu di SIPO fino all'atto firmato, e in quali momenti
ANSC entra in gioco. Gli otto passi sono quelli indicati dal committente; il documento li
mette in fila e vi aggiunge ciò che l'analisi ha già accertato — che cosa serve a ciascun
passo, che cosa può andare storto, quali conseguenze una scelta produce più avanti.

⚠️ Due punti che il documento non nasconde: l'ottavo passo confligge con la prassi attuale di
Roma (correzioni fino alla mezzanotte), e il secondo è facoltativo ma si paga alla fine.
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
OUT = os.path.join(BASE, 'Documenti finali', 'PROCEDURA_Formazione-Atto_SIPO-ANSC_v0.1.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'formazione_atto.png')

TAGLIA_DA = 29


def testo(par, s):
    if par.runs:
        par.runs[0].text = s
        for r in par.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        par.add_run(s)


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
            testo(p, 'La formazione di un atto: il percorso dell’operatore')
    return d


def h(d, livello, t):
    p = d.add_paragraph(style=f'Heading {livello}')
    p.add_run(t)
    return p


def par(d, t, stile='Normal'):
    p = d.add_paragraph(style=stile)
    for pezzo, grassetto in D.segmenta('', t)[0:]:
        r = p.add_run(pezzo)
        r.bold = grassetto
    return p


def voce(d, testa, corpo):
    p = d.add_paragraph(style='List Paragraph')
    r = p.add_run(testa + ' ')
    r.bold = True
    for pezzo, grassetto in D.segmenta('', corpo):
        rr = p.add_run(pezzo)
        rr.bold = grassetto
    return p


def tabella(d, righe, larghezze=None):
    t = d.add_table(rows=len(righe), cols=len(righe[0]))
    t.style = 'Table Grid'
    for i, r in enumerate(righe):
        for j, v in enumerate(r):
            cel = t.cell(i, j)
            cel.text = ''
            p = cel.paragraphs[0]
            run = p.add_run(v)
            run.bold = (i == 0)
            run.font.size = Pt(9)
    if larghezze:
        for j, w in enumerate(larghezze):
            for r in t.rows:
                r.cells[j].width = Inches(w)
    return t


PASSI = [
    (1, 'L’operatore sceglie l’operazione dal menu di SIPO',
     ['Il percorso comincia dove è sempre cominciato: nel menu di SIPO l’operatore sceglie il '
      'tipo di atto da formare — una dichiarazione di morte in abitazione, una nascita in '
      'costanza di matrimonio, una trascrizione. Nulla, in questo passo, cambia rispetto a '
      'oggi.',
      'Cambia però ciò che la scelta mette in moto dietro le quinte. Il tipo atto scelto è '
      'registrato in CONF_TIPO_ATTI e porta con sé il Modello di atto e la maschera di '
      'immissione; sono i due valori con cui la configurazione dell’integrazione aggancia il '
      'lavoro dell’operatore. Da quel momento il componente sa quali casi d’uso di ANSC sono '
      'candidati, perché la configurazione ne dichiara uno o più per ciascun Modello.',
      '⚠️ La determinazione del caso d’uso non avviene però qui. Fra i candidati la scelta '
      'dipende dai dati dell’atto, che l’operatore non ha ancora immesso: avviene alla '
      'chiusura, ed è la ragione per cui il passo 5 può chiedere documenti che al passo 1 non '
      'erano prevedibili.'],
     [('Che cosa serve', 'nulla che l’operatore non abbia già.'),
      ('Che cosa produce', 'il tipo atto, e con esso Modello e maschera.'),
      ('Se manca', 'non si dà: è il punto di partenza.')]),

    (2, 'Viene richiesto di acquisire il token da ANSC',
     ['Per parlare con ANSC servono due cose: un certificato che identifica il Comune e la '
      'postazione, e un codice temporaneo che identifica l’ufficiale. Il primo lo detiene il '
      'componente; il secondo lo genera l’ufficiale, di persona, sulla web app di ANSC, '
      'autenticandosi con smart card o SPID. Il codice ha una validità di quattro ore.',
      'L’ufficiale copia il codice e lo consegna a SIPO, che lo trasmette al concentratore. Da '
      'quel momento e per le quattro ore successive il componente può rivolgersi ad ANSC per '
      'conto di quell’ufficiale, da quella postazione.',
      '⚠️ **Il passo è facoltativo, e questa è una scelta di disegno, non una mancanza.** '
      'L’operatore che non acquisisce il token può ugualmente aprire l’atto e compilarlo per '
      'intero: gli sono precluse le sole funzioni che richiedono ANSC, e in particolare la '
      'ricerca del soggetto del passo 4. La ragione per cui la facoltà esiste è pratica: '
      'l’acquisizione richiede una autenticazione forte e non sempre l’ufficiale è alla '
      'postazione nel momento in cui la compilazione comincia.',
      '⚠️ **La scelta però si paga alla fine, non subito.** È il punto che il presente '
      'documento tiene a rendere esplicito, perché nel percorso non se ne vede la conseguenza '
      'finché non è tardi: si veda il passo 4.'],
     [('Che cosa serve', 'l’ufficiale, di persona, con la propria identità digitale.'),
      ('Che cosa produce', 'una sessione di quattro ore verso ANSC.'),
      ('Se manca', 'l’atto si compila lo stesso; la ricerca in ANSC è inibita.')]),

    (3, 'L’operatore inserisce i metadati previsti da SIPO',
     ['La compilazione avviene nelle maschere di SIPO, quelle di sempre. È il passo più lungo '
      'del percorso ed è anche quello in cui il presente progetto interviene di meno: '
      'l’operatore lavora come ha sempre lavorato, e il componente osserva senza intervenire.',
      'La ragione di questa scelta è dichiarata nell’analisi: il sistema è SIPO-centrico. '
      'L’atto si registra in SIPO e da lì si trasferisce ad ANSC; ANSC non è una seconda '
      'scrivania su cui l’operatore debba affacciarsi, ma la destinazione di ciò che in SIPO è '
      'già stato scritto.'],
     [('Che cosa serve', 'i dati dell’atto, come oggi.'),
      ('Che cosa produce', 'l’atto salvato sulle tabelle di SIPO.'),
      ('Se manca', 'le verifiche di SIPO già in esercizio segnalano l’incompletezza.')]),

    (4, 'Con il token valido si cercano gli intestatari in ANSC',
     ['ANSC conosce le persone e le identifica con un proprio codice. Perché l’atto che stiamo '
      'formando si leghi correttamente alla storia di stato civile del soggetto, quel codice '
      'va recuperato e riportato nell’atto. È ciò che fa il servizio di consultazione, '
      'interrogato con i dati anagrafici che l’operatore ha appena immesso.',
      'Il recupero riguarda gli intestatari — il defunto per un atto di morte, il neonato e i '
      'genitori per una nascita — e avviene solo se la sessione del passo 2 è stata aperta.',
      '⚠️ **Qui si vede il prezzo di aver saltato il passo 2.** Senza il codice del soggetto '
      'l’atto si può depositare ugualmente, ma gli automatismi di ANSC non scattano: il '
      'collegamento fra l’atto e la persona va poi stabilito con un’operazione a parte, che la '
      'nota di processo di ANSC definisce «fortemente sconsigliata». La conseguenza non è '
      'tecnica ma di merito: da quel collegamento dipendono le annotazioni sugli atti '
      'collegati e la comunicazione all’ufficio anagrafe.',
      'Ne discende una raccomandazione operativa che vale la pena scrivere: **il token va '
      'acquisito prima di cominciare**, non quando serve. Rimediare dopo costa più che '
      'prevenire.'],
     [('Che cosa serve', 'la sessione aperta e i dati anagrafici del soggetto.'),
      ('Che cosa produce', 'l’identificativo nazionale del soggetto, riportato nell’atto.'),
      ('Se manca', 'l’atto prosegue, ma il legame con la persona andrà stabilito a mano.')]),

    (5, 'Prima di chiudere si chiedono i dati e i documenti che ANSC richiede',
     ['Alla fine della compilazione, e prima che l’atto si chiuda, il componente confronta ciò '
      'che l’operatore ha scritto con ciò che ANSC pretende per quel caso d’uso. È il momento '
      'in cui il caso d’uso viene determinato: la configurazione valuta, sui dati ormai '
      'presenti, quale dei casi candidati corrisponde all’atto in lavorazione.',
      'Determinato il caso d’uso si sa tutto il resto, perché la configurazione lo dichiara per '
      'caso d’uso: quali campi sono obbligatori, quali documenti vanno allegati, quali '
      'diciture accompagnano l’atto. All’operatore vengono quindi chieste due cose: i campi '
      'che le maschere di SIPO non prevedono perché servono solo ad ANSC, e il caricamento dei '
      'documenti obbligatori.',
      '⚠️ **L’elenco dei documenti non è fisso: dipende dal caso d’uso determinato.** Due atti '
      'che in SIPO appaiono identici possono richiedere certificati diversi — è quanto accade '
      'alla dichiarazione di nascita, dove il nato morto e il nato vivo poi deceduto '
      'richiedono due certificati medici differenti. È la ragione per cui questo passo non può '
      'stare all’inizio.',
      'La verifica è locale e non consuma nulla: nessun servizio di ANSC viene invocato, e '
      'nessun identificativo nazionale viene assegnato. Serve a evitare che l’atto arrivi al '
      'deposito incompleto, quando l’errore costerebbe di più.'],
     [('Che cosa serve', 'l’atto compilato e la configurazione del caso d’uso.'),
      ('Che cosa produce', 'l’elenco di ciò che manca, campo per campo e documento per documento.'),
      ('Se manca', 'l’atto arriverebbe al deposito per essere rifiutato da ANSC.')]),

    (6, 'I file sono registrati in una struttura locale del Comune',
     ['I documenti caricati sono conservati in un archivio del Comune — un archivio a oggetti '
      'o altra soluzione già nella disponibilità dell’amministrazione — e non nella base dati '
      'dell’atto. La scelta tiene separati i documenti dai dati e consente di governarne '
      'diversamente conservazione e accesso.',
      'Da lì i file sono trasmessi ad ANSC, che li sottopone a scansione antivirus prima di '
      'accettarli. ⚠️ **La scansione non è immediata**: il documento assume uno stato che '
      'evolve, e solo quando risulta acquisito l’atto può proseguire. È l’unico passo del '
      'percorso in cui il componente attende un esito che non dipende da sé, e la maschera '
      'deve dirlo all’operatore invece di sembrare bloccata.',
      '⚠️ Va segnalato che oggi **SIPO non gestisce documenti allegati agli atti di stato '
      'civile**: non esistono né il file, né il tipo, né lo stato. Le maschere di caricamento '
      'sono quindi da realizzare, e con esse l’archivio e il raccordo con ANSC.'],
     [('Che cosa serve', 'un archivio documentale del Comune e le maschere di caricamento.'),
      ('Che cosa produce', 'i documenti acquisiti da ANSC e pronti per il deposito.'),
      ('Se manca', 'l’atto resta in attesa: senza documenti acquisiti non si prosegue.')]),

    (7, 'SIPO produce l’atto, che viene depositato e firmato',
     ['A questo punto l’atto è completo e il componente lo costruisce nella forma che ANSC '
      'attende, prendendo ciascun valore dalla colonna di SIPO che la configurazione indica. '
      'Il risultato è depositato: **è il momento in cui l’atto entra in ANSC e riceve '
      'l’identificativo nazionale**, e da qui in avanti esiste in due luoghi.',
      'Seguono le firme. Firma chi ha dichiarato, quando la legge lo prevede, e firma '
      'l’ufficiale dello stato civile; quest’ultima richiede un secondo codice temporaneo, '
      'distinto da quello di sessione, perché è una firma remota e non un semplice accesso. '
      'Insieme all’atto è generata l’attestazione di conformità, che accompagna i documenti '
      'allegati.',
      '⚠️ Il deposito non è una prenotazione: l’atto depositato esiste in ANSC come bozza, con '
      'un identificativo già consumato. Se dopo il deposito ci si accorge di un errore, la '
      'bozza va annullata esplicitamente — non basta abbandonarla.'],
     [('Che cosa serve', 'l’atto completo, i documenti acquisiti, le credenziali di firma.'),
      ('Che cosa produce', 'l’identificativo nazionale dell’atto e le firme.'),
      ('Se manca', 'l’atto resta bozza in ANSC e va annullato, non abbandonato.')]),

    (8, 'Avviata la firma, l’atto non è più modificabile',
     ['Con l’avvio del processo di firma l’atto diventa immutabile. Non è una scelta del '
      'progetto ma una proprietà di ANSC: un atto firmato è un atto formato, e ciò che è '
      'formato non si modifica — si annota, si rettifica, si annulla, e ciascuna di queste è '
      'un procedimento con le proprie regole.',
      '⚠️ **Qui il percorso incontra la prassi attuale di Roma, e la contraddice.** Oggi '
      'l’ufficio può correggere i dati di un atto fino alla mezzanotte del giorno in cui è '
      'stato redatto: è una finestra di tolleranza che assorbe gli errori materiali senza '
      'aprire procedimenti. Con ANSC quella finestra non esiste più: si chiude quando comincia '
      'la firma.',
      'La contraddizione non si risolve con una scelta tecnica, perché nessuna delle due parti '
      'può cedere: ANSC non consente di modificare un atto firmato, e il Comune non può '
      'rinunciare a correggere un errore materiale. Si risolve decidendo **quando firmare**. '
      'Le strade praticabili sono tre, e vanno valutate con l’ufficio.'],
     [('Che cosa serve', 'una decisione organizzativa, non una funzione.'),
      ('Che cosa produce', 'l’atto formato, valido e immutabile.'),
      ('Se manca', 'l’atto resta depositato ma non formato: nessun effetto giuridico.')]),
]

STRADE = [
    ['Strada', 'In che consiste', 'Che cosa costa'],
    ['Allineare la prassi',
     'La correzione dopo la firma diventa un procedimento, come per ogni atto formato.',
     'Formazione e cambio di abitudini per gli uffici; più procedimenti di rettifica per errori '
     'che oggi si correggevano senza traccia.'],
    ['Ritardare la firma',
     'L’atto si deposita subito e si firma a fine giornata, conservando di fatto la finestra '
     'di tolleranza.',
     'Gli atti restano in bozza per ore: serve un presidio che garantisca che nessuno resti '
     'non firmato, e i termini di legge non si fermano.'],
    ['Distinguere per tipo di errore',
     'Errori materiali evidenti entro la giornata sulla bozza non ancora firmata; tutto il '
     'resto per procedimento.',
     'Richiede una regola chiara su che cosa sia «materiale»: senza, la distinzione la fa '
     'l’operatore, e non è una decisione che gli competa.'],
]


def scrivi(d):
    h(d, 1, 'Scopo del documento')
    par(d, 'Il presente documento descrive il percorso che un operatore dello stato civile '
           'compie per formare un atto quando SIPO opera in collaborazione con ANSC. Non '
           'aggiunge requisiti né decisioni architetturali: riprende quanto stabilito '
           'nell’analisi di integrazione e lo dispone nell’ordine in cui i fatti accadono '
           'davanti a chi lavora, dal menu iniziale all’atto firmato.')
    par(d, 'La ragione di un documento a parte è che l’analisi tratta questi fatti per parti: '
           'la sessione in un capitolo, la configurazione in un altro, le firme in un terzo. '
           'Chi deve realizzare le maschere, o formare il personale, ha bisogno di vederli in '
           'fila, con l’indicazione di che cosa serve a ciascun passo e di che cosa accade se '
           'manca.')
    par(d, 'Due punti meritano attenzione fin da subito, perché non sono dettagli realizzativi '
           'ma scelte che riguardano l’organizzazione del lavoro: il secondo passo è '
           'facoltativo ma le sue conseguenze si manifestano alla fine, e l’ottavo confligge '
           'con la prassi oggi in uso a Roma. Entrambi sono trattati nel loro punto e ripresi '
           'in chiusura.')

    h(d, 1, 'Il principio: si lavora in SIPO, ANSC è la destinazione')
    par(d, 'L’impianto adottato è SIPO-centrico. L’operatore compila l’atto nelle maschere che '
           'già conosce e ANSC interviene in momenti definiti, per fare cose che SIPO non può '
           'fare da solo: riconoscere una persona nel registro nazionale, custodire i '
           'documenti allegati, ricevere l’atto e raccoglierne le firme.')
    par(d, 'Ne discende una proprietà che conviene tenere presente leggendo i passi che '
           'seguono: **il lavoro dell’operatore non si sposta**. Nessuno dei passi chiede di '
           'aprire un secondo applicativo, con una sola eccezione dichiarata — la generazione '
           'del codice di sessione, che ANSC consente solo dalla propria web app.')
    par(d, 'Su otto passi, quattro chiamano ANSC e uno solo di questi è facoltativo. Gli altri '
           'tre restano interamente dentro SIPO.')

    h(d, 1, 'Il percorso in otto passi')
    par(d, 'La figura riassume il percorso: a sinistra ciò che accade in SIPO, a destra ciò '
           'che si chiede ad ANSC, e in mezzo le due biforcazioni che il testo commenta.')
    d.add_picture(IMG, width=Inches(6.6))
    d.paragraphs[-1].alignment = 1
    cap = d.add_paragraph(style='Normal')
    r = cap.add_run('Il percorso di formazione dell’atto. Il tratteggio segnala il ramo di chi '
                    'non acquisisce il token; la linea rossa il punto oltre il quale l’atto '
                    'non si modifica più.')
    r.italic = True
    r.font.size = Pt(9)

    for numero, titolo, paragrafi, scheda in PASSI:
        h(d, 2, f'Passo {numero} — {titolo}')
        for t in paragrafi:
            par(d, t)
        tabella(d, [['', '']] + [[k, v] for k, v in scheda], larghezze=[1.5, 5.0])
        # la prima riga della tabella fa da intestazione muta: la si riempie
        t = d.tables[-1]
        t.cell(0, 0).paragraphs[0].runs[0].text = 'In sintesi'
        t.cell(0, 1).paragraphs[0].runs[0].text = ''

    h(d, 1, 'Le due decisioni che il percorso mette davanti')
    h(d, 2, 'Quando acquisire il token')
    par(d, 'Il secondo passo è facoltativo e la sua conseguenza compare al quarto, quando la '
           'ricerca del soggetto è inibita, ma si paga al settimo, quando l’atto si deposita '
           'senza il legame con la persona. Fra la scelta e il suo effetto passa l’intera '
           'compilazione: è il tipo di conseguenza che nessuno collega alla causa, se non è '
           'scritta.')
    par(d, 'La raccomandazione è quindi che l’acquisizione del token sia parte '
           'dell’apertura del lavoro e non un passo da rimandare: **prima di cominciare, non '
           'quando serve**. Dove ciò non sia possibile, la maschera dovrebbe segnalare in modo '
           'esplicito che l’atto sta procedendo senza il legame con il registro nazionale, e '
           'quali conseguenze ne derivano.')

    h(d, 2, 'Quando firmare')
    par(d, 'L’ottavo passo contraddice una prassi consolidata: a Roma un atto si corregge fino '
           'alla mezzanotte del giorno in cui è redatto. Con ANSC la finestra si chiude '
           'all’avvio della firma, e dopo la correzione non è più una modifica ma un '
           'procedimento.')
    par(d, 'Nessuna delle due parti può cedere — ANSC non consente di modificare un atto '
           'firmato, il Comune non può rinunciare a correggere un errore materiale — e quindi '
           'la questione non si risolve tecnicamente ma decidendo quando firmare. Le strade '
           'praticabili sono tre.')
    tabella(d, STRADE, larghezze=[1.5, 2.6, 2.6])
    par(d, '⚠️ La scelta compete all’ufficio e non al progetto. Va però compiuta prima '
           'dell’avvio in esercizio, perché determina la formazione del personale, il testo '
           'delle maschere e il presidio da mettere in campo: la seconda strada, in '
           'particolare, richiede che qualcuno garantisca ogni sera che nessun atto sia '
           'rimasto non firmato.')

    h(d, 1, 'Che cosa manca oggi per percorrere questi passi')
    par(d, 'Il percorso descritto poggia su funzioni che in parte non esistono ancora. Si '
           'elencano qui perché siano visibili come lavoro da fare e non come dettaglio '
           'realizzativo.')
    for testa, corpo in [
        ('Le maschere di caricamento dei documenti.',
         'SIPO non gestisce allegati agli atti di stato civile: non esistono il file, il tipo '
         'né lo stato. Vanno realizzate le maschere, l’archivio e l’attesa della scansione.'),
        ('I campi che ANSC richiede e SIPO non prevede.',
         'Al passo 5 vanno chiesti all’operatore: la loro individuazione è il lavoro di '
         'mappatura in corso, e cambia da caso d’uso a caso d’uso.'),
        ('La consegna del codice di sessione.',
         'Occorre il punto in cui l’operatore incolla il codice generato sulla web app e la '
         'maschera che ne mostra il tempo residuo, perché la sessione dura quattro ore.'),
        ('La segnalazione dello stato dell’atto in ANSC.',
         'Dal deposito in avanti l’atto esiste anche altrove: le maschere di ricerca e di '
         'dettaglio devono mostrarne l’identificativo nazionale e lo stato.'),
    ]:
        voce(d, testa, corpo)
    par(d, 'Nessuna di queste è una funzione grande. Insieme però costituiscono la differenza '
           'fra un atto che si forma soltanto in SIPO e un atto che si forma in SIPO e vive '
           'anche in ANSC, ed è su di esse che si misura l’impegno di realizzazione del '
           'percorso qui descritto.')


if __name__ == '__main__':
    d = costruisci()
    scrivi(d)
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    print('capitoli/tabelle/immagini:', D.riepilogo(OUT))
