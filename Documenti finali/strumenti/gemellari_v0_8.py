# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.8 (21/11/2026), dal FILE REALE della v0.7.

Decisioni dell'utente (21/11/2026):
  * caso 1: il testo dell'atto lo compone ANSC; SIPO lo recupera da ANSC (R010, anteprima senza
    filigrana dell'atto CONFERMATO) e lo riporta sull'atto di SIPO (ATTO_SCANSIONATO);
  * caso 2: si lavora come per gli atti a testo libero, con una PRATICA GUIDATA che cicla sugli
    atti SIPO dei gemelli e permette la copia del testo sulla web app;
  * in entrambi i casi una FINESTRA DI RACCORDO mostra i numeri comunali di ciascun gemello;
  * la SEQUENZA DELLE SCHERMATE dei due casi.
Si aggiunge in «SIPO oggi» dove SIPO compone e conserva il testo (verificato sul codice).
Figure: schermate_gemellari_v0_8.py (gem8_*.png), diagrammi_gemellari_v0_8_pptx.py
(gem8_flusso_1/_2, gem8_panoramica). GE-23…GE-26, [A13], [S6].

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_8.py
"""
import os
import re
import sys

import docx

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import par, tabella, voce               # noqa: E402
from gemellari_v0_2 import (figura, heading, in_coda, para_che_inizia,  # noqa: E402
                            sposta_prima, tabella_che_contiene)
from gemellari_v0_4 import (didascalia, rifai_voce, riga_di,      # noqa: E402
                            sostituisci_figura)

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.7.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.8.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '21/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')
LARGO = 6.3


def png(nome):
    return os.path.join(IMG, nome)


def inserisci_prima(ancora, costruisci, d):
    racc = in_coda(d)
    costruisci()
    sposta_prima(racc(), ancora)


def cella(t, primo, col, testo):
    D.riscrivi_cella(riga_di(t, primo).cells[col], testo)


# ------------------------------------------------------------------ contenuti
SIPO_TESTO = (
    'Il testo dell’atto SIPO lo compone a richiesta: la procedura '
    'PKG_FORMULARI.FORMULARIO_GENERA_MODELLO lo scrive in una tabella temporanea (GTT_TMP_ATTO), '
    'da cui si genera il PDF; come dato il testo non si conserva. Si conserva il PDF, in '
    'MATR_USR.ATTO_SCANSIONATO (DOCUMENTO e DOCUMENTO_CONFORME, con il nome del file composto da '
    'numero, parte, serie e anno). Lo scrivono la definizione (/finalizzaAtto), per i gemelli '
    '/generaPDFAttoFromFormularioGemelli, chiamato per ciascun atto, e l’atto temporaneo '
    '(/generaAttoTemporaneo, con FLG_SCANSIONATO a N) [S6]. La divisione non compone alcun '
    'testo: crea gli N atti, ciascuno con i dati del proprio nato. Per passare da un gemello '
    'all’altro SIPO ha già getNextATTONascitaGemello e i controlli checkPartoPlurimoAndGemSucc e '
    'checkPartoPlurimoAndGemPrec, che cercano i gemelli non ancora definiti con lo stesso '
    'ID_LAVORAZIONE_PADRE.')

RIGA_RACCORDO_1 = ['5', 'Raccordo dei numeri comunali (finestra nuova)', 'Per ciascun gemello il '
                   'numero comunale in grande e l’identificativo nazionale che lo contiene; '
                   'l’ufficiale verifica l’abbinamento e prosegue.', '—',
                   'Nessuna scrittura: l’abbinamento è già registrato.']

REGOLE_NUOVE_1 = [
    ('Raccordo dei numeri.', 'Subito dopo la prenotazione una finestra mostra, gemello per '
     'gemello, il numero comunale assegnato e l’identificativo nazionale che lo contiene, '
     'descritta più avanti. Si apre di nuovo, in sola lettura, dal riepilogo e dalla ripresa.'),
    ('Il testo dell’atto.', 'Lo compone ANSC; SIPO lo recupera e lo riporta sull’atto di SIPO '
     'alla definizione del gemello, come descritto più avanti.'),
]

TESTO_1_INTRO = (
    'Nel caso 1 ogni atto si forma con l’UC ordinario del nato, e il suo mapping non contiene il '
    'campo del testo, composizioneCompleta: nella famiglia della nascita compare in 6 mapping su '
    '289, quelli dei casi d’uso di servizio [A4]. Il testo lo compone ANSC, dai dati del modello '
    'evento e dalle formule; SIPO non lo trasmette, e nemmeno la prenotazione ne porta (numero dei '
    'gemelli, numeri comunali, UC) [A1]. L’atto giuridico è quello di ANSC, quindi anche il suo '
    'testo: SIPO lo recupera da ANSC e lo riporta sull’atto di SIPO, al posto del testo che '
    'comporrebbe con il formulario.')

TESTO_1_VOCI = [
    ('Quando.', 'Dopo la validazione del gemello (2 CONFERMATO) il concentratore chiede ad ANSC '
     'l’anteprima dell’atto senza filigrana (R010 /anteprima/evento, con presaVisione) [A13]. È il '
     'testo che la pagina mostra e che il dichiarante firma su carta. Il contratto ammette '
     'l’anteprima senza filigrana solo per l’atto CONFERMATO; dopo la firma del dichiarante i dati '
     'sono vincolati, quindi il testo non cambia più fino alla firma dell’ufficiale.'),
    ('Dove.', 'Alla definizione del gemello, subito dopo la firma dell’ufficiale, quel PDF diventa '
     'il documento dell’atto di SIPO: MATR_USR.ATTO_SCANSIONATO.DOCUMENTO della riga dell’atto '
     'del gemello, con lo stesso nome di file di oggi. Il testo che SIPO comporrebbe non si mostra '
     'e non si conserva.'),
    ('La definizione non deve sovrascriverlo.', 'Oggi /finalizzaAtto genera il PDF dal formulario '
     'e lo scrive in ATTO_SCANSIONATO [S6]. Per un atto formato in ANSC il PDF di ANSC si scrive '
     'dopo la definizione, oppure la definizione riceve l’indicazione di non rigenerarlo; la '
     'scelta tocca il codice di SIPO ed è GE-24, insieme a DOCUMENTO_CONFORME, che oggi SIPO '
     'compone accanto all’atto.'),
    ('Senza le firme.', 'Il PDF dell’anteprima è il testo dell’atto, non la copia firmata. La '
     'copia dell’atto firmato ANSC la rilascia come certificato (copia integrale, R002), come ha '
     'indicato sullo «scaricamento atto dopo la firma USC» (issue #418) [A13]; la copia integrale '
     'chiede la firma remota dell’ufficiale con il codice OTP, cioè un’emissione per atto. Se il '
     'Comune vuole in SIPO la copia firmata, è GE-23.'),
    ('Se il recupero non riesce.', 'Un errore di R010 non ferma la formazione: l’atto si firma '
     'sulla copia stampata dalla pagina e il testo si recupera di nuovo prima della definizione; '
     'se manca anche allora, la definizione si ferma come nella tabella degli errori e si '
     'riprende senza altre chiamate di firma.'),
]

RACCORDO_INTRO = (
    'I numeri comunali sono il filo che lega ciascun nato al suo atto: la prenotazione restituisce '
    'gli identificativi nazionali in un elenco, e l’abbinamento si fa sul numero comunale che '
    'ciascun identificativo contiene. Perché l’ufficiale lo veda e lo controlli, in entrambi i '
    'casi una finestra di raccordo estrae i numeri e li mostra in grande, un riquadro per '
    'gemello.')

RACCORDO_VOCI = [
    ('Che cosa mostra.', 'Per ciascun gemello, in ordine di nascita: nato, sesso, tipologia di '
     'nascita, UC; il numero comunale in grande; l’identificativo nazionale con il numero comunale '
     'evidenziato; i controlli e l’esito.'),
    ('I controlli, nel caso 1.', 'Il numero comunale è contenuto in uno e un solo identificativo; '
     'il numero assegnato è quello previsto dal riepilogo, e se differisce (altri operatori hanno '
     'staccato numeri nel frattempo) la differenza si mostra senza essere un errore. Un '
     'identificativo che non contiene alcun numero del parto, o due che contengono lo stesso, '
     'non si abbinano: è un esito anomalo della prenotazione, trattato più avanti.'),
    ('I comandi.', 'PROSEGUI CON IL GEMELLO 1 apre l’atto del primo gemello; STAMPA PROMEMORIA '
     'produce la stessa vista su carta; SOSPENDI chiude senza cambiare nulla.'),
    ('Nel caso 2.', 'La stessa finestra compare due volte: prima della web app, con i numeri da '
     'riportare e l’ordine in cui riportarli, e dopo RECUPERA GEMELLI, con l’identificativo '
     'trovato in ANSC per ciascun numero e l’esito dell’abbinamento.'),
]

SEQ_1 = [
    ['#', 'Schermata', 'Si arriva con', 'Servizi', 'Che cosa mostra o produce'],
    ['1', 'Riepilogo dei gemelli', 'Conferma della divisione; dal dettaglio del gemello 1',
     'lettura del numeratore (GE-19)', 'UC e numero comunale previsto di ciascun nato.'],
    ['2', 'Raccordo dei numeri comunali (finestra)', 'DEFINISCI, dopo la conferma',
     'POST /richiesta; R009 /prenota/evento', 'I numeri assegnati e gli identificativi '
     'abbinati.'],
    ['3', 'Gemello k: documenti, anteprima e validazione, firma del dichiarante, conformità, '
     'firma dell’ufficiale', 'PROSEGUI (gemello 1) o GEMELLO SUCCESSIVO', 'R001, R009, R010, '
     'R006, R007', 'Le pagine del percorso ordinario di un atto [R1], con in testa la fila dei '
     'gemelli e i passi del gemello in lavorazione; il testo mostrato è quello di ANSC.'],
    ['4', 'Gemello k: testo da ANSC e definizione', 'Firma dell’ufficiale riuscita',
     'ATTO_SCANSIONATO; /finalizzaAtto', 'L’atto formato, il suo testo riportato in SIPO e la '
     'definizione; GEMELLO SUCCESSIVO riporta alla schermata 3 per il gemello k+1.'],
    ['5', 'Esito del parto', 'Definizione dell’ultimo gemello', '—', 'Tutti gli atti formati in '
     'ANSC e definiti in SIPO, ciascuno con il testo di ANSC.'],
]
SEQ_1_NOTA = (
    'Gli errori e la sospensione portano fuori dalla sequenza: la schermata di DEFINISCI in corso '
    'e la ripresa dal riepilogo sono descritte più avanti.')

GUIDATA_INTRO = (
    'Gli atti si formano sulla web app con il caso d’uso di servizio, dove il testo va scritto '
    'nella composizione libera. Si lavora come per gli atti a testo libero [R2]: il testo lo '
    'compone SIPO e l’ufficiale lo copia sulla web app. Con N gemelli la copia è da fare N volte, '
    'con un numero e una tipologia di nascita diversi per ciascuno: per questo SIPO la guida, un '
    'gemello alla volta, ciclando sugli atti SIPO del parto.')

GUIDATA_VOCI = [
    ('Da dove si avvia.', 'AVVIA LA PRATICA GUIDATA, nella finestra di raccordo che segue DATI PER '
     'ANSC; solo sul gemello 1 del parto. Riaperta, la pratica riparte dal gemello in cui si era '
     'fermata, che lo store ricorda come pagina di ripresa.'),
    ('Che cosa mostra per ciascun gemello.', 'In testa la fila dei gemelli con il loro numero e lo '
     'stato della pratica (testo copiato, in lavorazione, da fare); il numero comunale del '
     'gemello in grande; che cosa indicare sulla web app: l’ordine, la tipologia di nascita '
     '(ANSC_107), il certificato medico se il nato è morto o vivo e poi deceduto; il testo '
     'dell’atto composto da SIPO con il formulario, in anteprima.'),
    ('COPIA TESTO.', 'Copia negli appunti il testo dell’atto del gemello, da incollare nella '
     'composizione libera della sua bozza, come per gli atti a testo libero [R2].'),
    ('Gli identificativi dei fratelli.', 'Li assegna la web app alla prenotazione: SIPO non li '
     'conosce e il testo li lascia da completare. L’ufficiale li riporta nella composizione, come '
     'chiede la guida ANSC per il parto plurimo [A3].'),
    ('Il promemoria.', 'Caselle che l’ufficiale segna per sé (bozza aperta con il numero, '
     'tipologia indicata, testo incollato, atto firmato). Non sono controlli: SIPO non vede la '
     'web app, e ciò che conta lo verifica RECUPERA GEMELLI al rientro.'),
    ('Comandi.', 'GEMELLO PRECEDENTE e GEMELLO SUCCESSIVO; sull’ultimo gemello il secondo riporta '
     'al riepilogo, dove RECUPERA GEMELLI si usa quando gli atti sono firmati sulla web app. '
     'SOSPENDI chiude senza cambiare nulla: i numeri restano impegnati per il parto.'),
]

TESTO_2 = (
    'Nel caso 2 il testo che entra in ANSC è quello incollato nella composizione libera, '
    'completato dall’ufficiale con gli identificativi dei fratelli. In SIPO resta il PDF che SIPO '
    'compone alla definizione (DEFINISCI GEMELLI), come per gli atti a testo libero. I due testi '
    'possono differire per quanto l’ufficiale ha aggiunto o corretto sulla web app; se conservare '
    'in SIPO anche il testo di ANSC, che R005 restituisce nel modello evento al recupero, è GE-25.')

SEQ_2 = [
    ['#', 'Schermata', 'Si arriva con', 'Servizi', 'Che cosa mostra o produce'],
    ['1', 'Riepilogo dei gemelli (UC diversi)', 'Conferma della divisione; dal dettaglio del '
     'gemello 1', 'all-ansc-sipo (configurazione)', 'UC dei nati e numeri previsti; DEFINISCI non '
     'compare, compare DATI PER ANSC.'],
    ['2', 'Raccordo dei numeri – da riportare (finestra)', 'DATI PER ANSC', 'POST /richiesta',
     'I numeri staccati, in grande, con l’ordine in cui riportarli sulla web app.'],
    ['3', 'Pratica guidata: gemello k', 'AVVIA LA PRATICA GUIDATA o GEMELLO SUCCESSIVO', '—',
     'Numero, tipologia di nascita e testo del gemello k; COPIA TESTO.'],
    ['4', 'Web app ANSC (fuori da SIPO)', 'COPIA TESTO', '—', 'Prenotazione dei gemelli con i '
     'numeri di SIPO; bozza di ciascun gemello con tipologia di nascita e testo; firme.'],
    ['5', 'Raccordo dei numeri – esito del recupero (finestra)', 'RECUPERA GEMELLI, dal gemello 1',
     'R005 per numero comunale', 'Per ciascun numero l’atto trovato e l’esito dell’abbinamento.'],
    ['6', 'Esito del parto', 'DEFINISCI GEMELLI, con tutti i gemelli abbinati', '/finalizzaAtto per '
     'ciascun atto', 'Tutti gli atti agganciati ai gemelli e definiti in SIPO.'],
]

GE_NUOVI = [
    ['GE-23', 'Copia firmata dell’atto', 'Il testo riportato in SIPO è l’anteprima senza '
     'filigrana (R010), senza le firme. La copia dell’atto firmato si ottiene come certificato '
     '(copia integrale, R002), con la firma remota dell’ufficiale e il codice OTP. Se il Comune la '
     'vuole in SIPO, a quale momento chiederla; e [DA VERIFICARE] se R005 restituisca '
     'composizioneCompleta anche per gli atti con UC ordinario.', 'Aperto'],
    ['GE-24', 'Definizione e documento dell’atto', 'Oggi /finalizzaAtto rigenera il PDF dal '
     'formulario e lo scrive in ATTO_SCANSIONATO: per l’atto formato in ANSC va evitato che '
     'sostituisca il testo di ANSC (scrittura dopo la definizione o indicazione di non '
     'rigenerarlo). Che cosa mettere in DOCUMENTO_CONFORME per un atto ANSC.', 'Aperto'],
    ['GE-25', 'Testo nel caso 2', 'Il testo in ANSC può differire da quello copiato da SIPO '
     '(identificativi dei fratelli, correzioni sulla web app). Se al recupero conservare in SIPO '
     'anche il testo di ANSC o segnalare la differenza.', 'Aperto'],
    ['GE-26', 'Numero comunale nel testo di SIPO', 'Nella pratica guidata il testo del gemello '
     'deve già contenere il numero comunale staccato da DATI PER ANSC: con quale dato il '
     'formulario lo legge, come per gli atti a testo libero [R2].', 'Aperto'],
]

RIF_NUOVI = [
    ['[A13]', 'ansc/docs/openapi/R010_anteprima.yaml — /anteprima/evento, presaVisione (anteprima '
     'senza filigrana, risposta 400 se l’atto non è CONFERMATO); Changelog, «Chiarimento: '
     'scaricamento atto dopo la firma USC: Emissione certificati» (issue #418).', 'Contratto ANSC'],
    ['[S6]', 'back-end/statocivile-be — InitFlow (salvataggio del PDF in ATTO_SCANSIONATO), '
     'FormularioServiceImpl (PKG_FORMULARI.FORMULARIO_GENERA_MODELLO), AnteprimaAttoController '
     '(/generaPDFAttoFromFormularioGemelli, /generaAttoTemporaneo, getNextATTONascitaGemello, '
     'checkPartoPlurimoAndGemSucc e GemPrec); DettaglioAttiController (/performAttiPlurigemellari '
     '→ PKG_PRATICA.CREA_ATTI_NASCITA_FIGLI).', 'Sorgente applicativo'],
]


def main():
    d = docx.Document(IN)
    fatti = []

    # 1. In sintesi
    p = para_che_inizia(d, 'Il caso 1 in SIPO.')
    for r in reversed(p.runs):
        if r.text.strip():
            r.text = r.text.rstrip() + (' Il testo dell’atto lo compone ANSC: SIPO lo recupera e '
                                        'lo riporta sull’atto di SIPO.')
            break
    D.sostituisci(d, 'la pagina «Dati per ANSC» del parto;', 'una pratica guidata che porta '
                  'sulla web app, un gemello alla volta, numero comunale e testo composto da '
                  'SIPO;', attese=1, fatti=fatti)
    inserisci_prima(para_che_inizia(d, 'Il soggetto e il suo atto ANSC.')._p, lambda: voce(
        d, 'Il raccordo dei numeri.', 'In entrambi i casi una finestra mostra in grande il numero '
        'comunale di ciascun gemello e l’identificativo nazionale che lo contiene, per '
        'l’abbinamento corretto; le sequenze delle schermate dei due casi sono nel capitolo della '
        'modalità di integrazione.'), d)

    # 2. SIPO oggi: dove si compone e si conserva il testo
    p = para_che_inizia(d, 'Divisa la pratica, l’anteprima scorre i gemelli')
    inserisci_prima(p._p.getnext(), lambda: par(d, SIPO_TESTO), d)

    # 3. panoramica e caso 1
    sostituisci_figura(d, 'I due casi: la scelta dopo la divisione',
                       png('gem8_panoramica.pptx.png'), LARGO,
                       'I due casi: la scelta dopo la divisione')
    t = tabella_che_contiene(d, 'DEFINISCI: numeri e prenotazione')
    for r in reversed(t.rows[5:]):
        D.riscrivi_cella(r.cells[0], str(int(r.cells[0].text) + 1))
    D.clona_riga(t, RIGA_RACCORDO_1)
    riga_di(t, '4')._tr.addnext(t.rows[-1]._tr)
    c = riga_di(t, '6').cells
    assert c[1].text.startswith('DEFINISCI, gemello k: documenti'), c[1].text
    D.riscrivi_cella(c[2], c[2].text.rstrip('.') + '; il testo dell’atto è quello composto da '
                     'ANSC (R010, senza filigrana).')
    D.riscrivi_cella(c[3], c[3].text + '; R010 /anteprima/evento')
    c = riga_di(t, '8').cells
    assert 'definizione' in c[1].text, c[1].text
    D.riscrivi_cella(c[1], 'DEFINISCI, gemello k: testo da ANSC e definizione')
    D.riscrivi_cella(c[2], 'Subito dopo la firma dell’ufficiale: il testo recuperato da ANSC '
                     'diventa il documento dell’atto di SIPO, poi la definizione; si passa al '
                     'gemello k+1.')
    D.riscrivi_cella(c[3], 'ATTO_SCANSIONATO; /finalizzaAtto')
    sostituisci_figura(d, 'Caso 1: le pagine', png('gem8_flusso_1.pptx.png'), 5.9,
                       'Caso 1: le pagine, i servizi e gli stati, con le righe dello store')
    ancora = para_che_inizia(d, 'Un gemello alla volta.')._p
    inserisci_prima(ancora, lambda: [voce(d, a, b) for a, b in REGOLE_NUOVE_1], d)

    def sezioni_1():
        heading(d, 3, 'Il testo dell’atto')
        par(d, TESTO_1_INTRO)
        for a, b in TESTO_1_VOCI:
            voce(d, a, b)
        heading(d, 3, 'La finestra di raccordo dei numeri comunali')
        par(d, RACCORDO_INTRO)
        for a, b in RACCORDO_VOCI:
            voce(d, a, b)
        figura(d, png('gem8_c1_raccordo.png'), LARGO, 'Caso 1: la finestra di raccordo dei '
               'numeri comunali dopo la prenotazione (ipotesi)')
        heading(d, 3, 'La sequenza delle schermate del caso 1')
        tabella(d, SEQ_1, [0.3, 1.55, 1.35, 1.35, 2.05])
        figura(d, png('gem8_seq_caso1.png'), LARGO, 'Caso 1: la sequenza delle schermate')
        figura(d, png('gem8_c1_gemello.png'), LARGO, 'Caso 1: il gemello 2 sul passo della firma '
               'del dichiarante, con il testo composto da ANSC (ipotesi)')
        figura(d, png('gem8_c1_testo.png'), LARGO, 'Caso 1: il gemello 2 formato, il testo '
               'recuperato da ANSC e l’atto definito in SIPO (ipotesi)')
        figura(d, png('gem8_c1_esito.png'), LARGO, 'Caso 1: l’esito del parto (ipotesi)')
        par(d, SEQ_1_NOTA)
    inserisci_prima(D.h(d, 3, 'Quando qualcosa non va a buon fine')._p, sezioni_1, d)

    # 4. caso 2
    t = tabella_che_contiene(d, 'SIPO, pagina «Dati per ANSC» del parto')
    r = riga_di(t, '4')
    D.riscrivi_cella(r.cells[1], 'SIPO, finestra di raccordo e pratica guidata')
    D.riscrivi_cella(r.cells[2], 'La finestra mostra in grande il numero comunale di ciascun '
                     'nato e l’ordine in cui riportarlo; la pratica guidata presenta un gemello '
                     'alla volta con numero, tipologia di nascita e testo composto da SIPO, da '
                     'copiare con COPIA TESTO.')
    r = riga_di(t, '6')
    D.riscrivi_cella(r.cells[2], r.cells[2].text.rstrip('.') + '; l’esito si mostra nella '
                     'finestra di raccordo.')
    sostituisci_figura(d, 'Caso 2: le pagine', png('gem8_flusso_2.pptx.png'), 5.9,
                       didascalia(d, 'Caso 2: le pagine').text.split(' – ', 1)[1])
    ancora = para_che_inizia(d, 'Numeri sulla web app.')._p
    inserisci_prima(ancora, lambda: [
        voce(d, 'Finestra di raccordo.', 'Dopo lo stacco la finestra di raccordo mostra i numeri '
             'da riportare sulla web app, in grande e nell’ordine di nascita; AVVIA LA PRATICA '
             'GUIDATA prosegue.'),
        voce(d, 'Pratica guidata.', 'Un gemello alla volta, con il numero, la tipologia di nascita '
             'e il testo composto da SIPO da copiare sulla web app, descritta più avanti.')], d)
    sostituisci_figura(d, 'Il caso 2: la pagina «Dati per ANSC»', png('gem8_c2_raccordo.png'),
                       LARGO, 'Il caso 2: la finestra di raccordo dei numeri comunali da riportare '
                       'sulla web app (ipotesi)')
    sostituisci_figura(d, 'Il caso 2: l’esito di RECUPERA GEMELLI', png('gem8_c2_recupero.png'),
                       LARGO, 'Il caso 2: la finestra di raccordo con l’esito di RECUPERA GEMELLI '
                       '(ipotesi)')

    def sezioni_2():
        heading(d, 3, 'La pratica guidata verso la web app')
        par(d, GUIDATA_INTRO)
        for a, b in GUIDATA_VOCI:
            voce(d, a, b)
        figura(d, png('gem8_c2_guidata.png'), LARGO, 'Caso 2: la pratica guidata sul gemello 2, '
               'con il numero comunale e il testo da copiare sulla web app (ipotesi)')
        heading(d, 3, 'Il testo dell’atto nel caso 2')
        par(d, TESTO_2)
        heading(d, 3, 'La sequenza delle schermate del caso 2')
        tabella(d, SEQ_2, [0.3, 1.55, 1.35, 1.35, 2.05])
        figura(d, png('gem8_seq_caso2.png'), LARGO, 'Caso 2: la sequenza delle schermate')
        figura(d, png('gem8_c2_riepilogo.png'), LARGO, 'Caso 2: il riepilogo dei gemelli con UC '
               'diversi (ipotesi)')
        figura(d, png('gem8_c2_esito.png'), LARGO, 'Caso 2: l’esito del parto (ipotesi)')
    inserisci_prima(D.h(d, 2, 'Nato morto e nato vivo poi deceduto nel parto plurimo')._p,
                    sezioni_2, d)

    # 5. punti aperti e riferimenti
    op = D.trova_tabella(d, 'tema', 'questione')
    for riga in GE_NUOVI:
        D.clona_riga(op, riga)
    rif = [x for x in d.tables if len(x.columns) == 3 and x.rows[0].cells[1].text.strip() == 'Riferimento']
    assert len(rif) == 1
    rif = rif[0]
    for riga in RIF_NUOVI:
        D.clona_riga(rif, riga)
    riga_di(rif, '[A12]')._tr.addnext(riga_di(rif, '[A13]')._tr)

    # 6. residui
    storia_t = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    residui = [p.text for p in d.paragraphs if '«Dati per ANSC»' in p.text] + \
              [c.text for tb in d.tables if tb._tbl is not storia_t._tbl
               for rr in tb.rows for c in rr.cells if '«Dati per ANSC»' in c.text]
    assert not residui, residui

    # 7. figure rinumerate, frontespizio, storia
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])
    for fatto in D.frontespizio(d, '0.8', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.8', 'In sintesi · SIPO oggi · La modalità di integrazione (casi 1 e 2) '
             '· Punti aperti · Riferimenti',
             'Il testo dell’atto: nel caso 1 lo compone ANSC e SIPO lo recupera (anteprima senza '
             'filigrana) e lo riporta sull’atto di SIPO alla definizione; nel caso 2 una pratica '
             'guidata cicla sugli atti SIPO dei gemelli e ne fa copiare il testo sulla web app. In '
             'entrambi i casi una finestra di raccordo mostra i numeri comunali di ciascun gemello. '
             'Sequenze delle schermate dei due casi; dove SIPO compone e conserva il testo; '
             'diagrammi aggiornati. GE-23…GE-26, [A13], [S6].')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
