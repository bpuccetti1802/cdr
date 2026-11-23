# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.5 (21/11/2026), dal FILE REALE della v0.4.

Che cosa cambia (rilievo e decisioni dell'utente, 21/11/2026), solo nel caso 1:
  * il passo PRENOTA GEMELLI non c'è più: dopo la divisione una pagina di RIEPILOGO dei gemelli
    mostra UC e numero comunale PREVISTO (non riservato) di ciascun nato;
  * un solo DEFINISCI stacca i numeri, prenota gli atti con l'UC comune e accompagna un gemello
    alla volta per documenti, anteprima e validazione, firma del dichiarante, conformità e firma
    USC; ciascun atto si definisce in SIPO SUBITO dopo la sua firma USC;
  * errori: un esito certo si riprova o si sospende, un esito incerto si verifica con R005; gli
    atti già firmati non si toccano;
  * interruzione: il riepilogo, aperto su un parto avviato, diventa pagina di ripresa (R005 per
    gemello, nessun nuovo numero né nuova prenotazione); RINUNCIA AL PARTO solo finché nessun
    gemello è firmato dall'ufficiale;
  * figure: diagrammi_gemellari_v0_5_pptx.py (gem5_*), schermate_gemellari_v0_5.py;
    GE-09/GE-12 integrati, GE-19…GE-22; corretto «Passo del caso 1NSC» (residuo della v0.4).

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_5.py
"""
import os
import re
import sys

import docx
from docx.oxml.ns import qn

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import par, tabella, voce               # noqa: E402
from gemellari_v0_2 import (figura, heading, in_coda, para_che_inizia,  # noqa: E402
                            sposta_prima, tabella_che_contiene)
from gemellari_v0_4 import (didascalia, rifai_voce, riga_di,      # noqa: E402
                            sostituisci_figura, sostituisci_nei_run)

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.4.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.5.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '21/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')
LARGO = 6.3


def png(nome):
    return os.path.join(IMG, nome)


def inserisci_prima(d, ancora, costruisci):
    racc = in_coda(d)
    costruisci()
    sposta_prima(racc(), ancora)


def togli_figura(d, inizio):
    cap = didascalia(d, inizio)
    e = cap._p.getprevious()
    while e.tag != qn('w:p') or not e.findall('.//' + qn('pic:pic')):
        e = e.getprevious()
    for x in (e, cap._p):
        assert not D.ha_commenti(x)
        x.getparent().remove(x)


# ------------------------------------------------------------------ contenuti
INTRO_1 = (
    'Il percorso aggiunge al flusso di SIPO una pagina nuova, il riepilogo dei gemelli, e '
    'trasforma il comando DEFINISCI GEMELLI in una procedura guidata, DEFINISCI, che porta un '
    'gemello alla volta dall’anteprima alla firma dell’ufficiale e lo definisce subito in SIPO. Da '
    'Side [M1] riprende la regola di fondo: gli identificativi dei fratelli devono entrare nel '
    'testo di ciascun atto prima che sia validato, quindi la prenotazione precede l’anteprima. Il '
    'posto naturale è dopo la divisione: gli atti esistono, i dati di ciascun nato sono noti e il '
    'testo non è ancora composto. A differenza di Side la prenotazione non è un pulsante a sé ma '
    'il primo passo di DEFINISCI: numeri e atti prenotati si consumano solo quando l’ufficiale è '
    'pronto a formare gli atti.')

PASSI_1 = [
    ['#', 'Pagina o momento in SIPO', 'Che cosa succede', 'Servizi', 'Esito'],
    ['1', 'Compilazione della pratica (maschera dei gemelli)', 'Come oggi: dati dei genitori, '
     'numero dei gemelli, dati di ciascun nato con i due flag.', 'nascita-be', 'Pratica salvata.'],
    ['2', 'Riepilogo → Conferma', 'Come oggi: la pratica è divisa in N atti.',
     '/performAttiPlurigemellari', 'N atti in SIPO legati da ID_LAVORAZIONE_PADRE.'],
    ['3', 'Riepilogo dei gemelli (nuovo)', 'Per ciascun nato posizione, stato, UC e numero '
     'comunale previsto; nulla si riserva. Se gli UC differiscono la pagina porta al caso 2.',
     'lettura del numeratore (GE-19)', 'Nessuna scrittura.'],
    ['4', 'DEFINISCI: numeri e prenotazione', 'Conferma; N numeri staccati in blocco; '
     'prenotazione con l’UC comune e il numero totale dei gemelli.',
     'be-numeratore-comunale POST /richiesta; all-ansc-sipo → R009 /prenota/evento',
     'N righe in ANSC_STATO_ATTO in BOZZA, con numero comunale e idAnsc; righe in '
     'ATTI_GEMELLARI e in ANSC_SOGGETTO_ATTO.'],
    ['5', 'DEFINISCI, gemello k: documenti, anteprima e validazione', 'Certificato medico se '
     'richiesto; atto con gli identificativi dei fratelli; R009 all’apertura dell’anteprima, '
     'sulla bozza prenotata e con lo stesso UC (con quale campo: OP-46).',
     'R001; R009 /validazione/evento', 'Atto k CONFERMATO.'],
    ['6', 'DEFINISCI, gemello k: firme', 'Firma cartacea del dichiarante acquisita come processo '
     'verbale; attestazione di conformità; firma dell’ufficiale.', 'R006; R007',
     'Atto k FIRMATO DA USC.'],
    ['7', 'DEFINISCI, gemello k: definizione', 'Subito dopo la firma dell’ufficiale; poi si '
     'passa al gemello k+1.', '/finalizzaAtto', 'Atto k 2 DEFINITO in SIPO.'],
    ['8', 'Esito del parto', 'Riepilogo finale; allineamento anagrafico secondo [R1].', '—',
     'Tutti gli atti formati in ANSC e definiti in SIPO.'],
]

REGOLE_1 = [
    ('Il riepilogo.', 'Compare sul gemello 1 di una pratica divisa, finché il parto non è '
     'definito. Mostra per ciascun nato posizione, sesso, stato, UC e il numero comunale previsto, '
     'cioè quello che il numeratore assegnerebbe in quel momento: è una lettura, che non riserva '
     'nulla. Gli atti dei gemelli non si validano uno per uno dalle loro pagine: la validazione '
     'passa solo da DEFINISCI.'),
    ('Conferma.', 'DEFINISCI chiede conferma: staccati i numeri e prenotati gli atti, il numero '
     'dei gemelli non si può più cambiare.'),
    ('Numeri comunali.', 'Si staccano in blocco al DEFINISCI, con una sola richiesta al servizio '
     'be-numeratore-comunale, che garantisce numeri consecutivi [R3]. Se nel frattempo un altro '
     'operatore ha staccato numeri, quelli assegnati differiscono dai previsti: la pagina lo '
     'segnala prima di proseguire, senza trattarlo come un errore.'),
    ('UC.', 'Si determina per ciascun gemello dai suoi due flag; la prenotazione passa l’UC '
     'comune e il numero totale dei gemelli. Se gli UC differiscono DEFINISCI non compare e la '
     'pagina porta al caso 2.'),
    ('Esito della prenotazione.', 'Ciascun identificativo restituito si assegna al gemello del '
     'numero comunale che contiene: una riga di ANSC_STATO_ATTO in BOZZA per ciascun atto, con '
     'numero comunale e idAnsc, una riga della tabella dei gemelli e una di ANSC_SOGGETTO_ATTO, '
     'descritte più avanti.'),
    ('Un gemello alla volta.', 'DEFINISCI presenta l’atto del gemello 1 e, solo dopo la sua firma '
     'dell’ufficiale e la sua definizione in SIPO, quello del gemello 2, e così via, come chiede la '
     'guida ANSC [A3]. Il dichiarante firma ciascun atto; l’ufficiale firma la conformità e l’atto '
     'di ciascun gemello.'),
    ('Definizione subito.', 'Ogni atto si definisce in SIPO (/finalizzaAtto, 2 DEFINITO) appena '
     'l’ufficiale lo ha firmato. Dopo la firma l’atto in ANSC è formato e non si torna indietro: '
     'definirlo subito tiene SIPO e ANSC allineati gemello per gemello, anche se un gemello '
     'successivo si ferma. Al termine della procedura tutti gli atti sono salvati in entrambi i '
     'sistemi. Cambia il comportamento di oggi, dove DEFINISCI GEMELLI definisce tutti gli atti in '
     'sequenza alla fine.'),
]

ERRORI_INTRO = (
    'DEFINISCI attraversa, per N gemelli, una catena di chiamate ad ANSC e una definizione in SIPO '
    'per ciascuno. La regola generale è quella dell’analisi di integrazione [R1]: un esito certo si '
    'tratta, un esito incerto prima si verifica con R005 e poi si decide, mai un secondo tentativo '
    'alla cieca. Il parto aggiunge due regole: un errore ferma solo il gemello in lavorazione, '
    'perché non si passa al successivo prima della sua firma; e gli atti già firmati '
    'dall’ufficiale non si toccano.')

ERRORI = [
    ['Dove si ferma', 'Che cosa resta', 'Che cosa si fa'],
    ['Stacco dei numeri', 'Nulla: nessun numero, nessun atto.', 'Si resta sul riepilogo e si '
     'riprova.'],
    ['Prenotazione rifiutata (errore con codice)', 'Numeri staccati, nessun atto in ANSC; righe '
     'in UC_DETERMINATO.', 'Si riprova con gli stessi numeri; se si rinuncia, i numeri si '
     'scartano.'],
    ['Prenotazione dall’esito incerto', 'Non si sa se gli atti esistano.', 'R005 per numero '
     'comunale: con gli atti trovati si completano le righe; si prenota di nuovo, con gli stessi '
     'numeri, solo se non ce n’è nessuno (GE-13).'],
    ['Validazione del gemello k con errori', 'Atto k in bozza; i gemelli precedenti formati e '
     'definiti.', 'L’ufficiale corregge i dati del gemello k e DEFINISCI riprende dall’anteprima. '
     'Se la correzione cambia lo stato del nato, e quindi l’UC, il parto non è più del caso 1 '
     '(GE-20).'],
    ['Firma del dichiarante non acquisita', 'Atto k 2 CONFERMATO.', 'Si ripete il caricamento '
     '(R006) oppure si sospende.'],
    ['Conformità non firmata', 'Atto k 4 FIRMATO DAL DICHIARANTE.', 'Si riprova, anche con un '
     'nuovo codice OTP, oppure si sospende.'],
    ['Firma dell’ufficiale non riuscita, con codice (406001 OTP non valido, 406002 OTP scaduto, '
     '406004 firma non avvenuta)', 'Atto k 11 FIRMATO PER CONFORMITÀ; gemelli successivi in '
     'bozza.', 'RIPROVA LA FIRMA, chiedendo prima un nuovo codice OTP se è scaduto, oppure '
     'SOSPENDI. La ripresa parte dalla firma del gemello k.'],
    ['Firma dell’ufficiale dall’esito incerto', 'Non si sa se l’atto k sia formato.', 'R005 '
     'sull’identificativo del gemello k: se è 5 FIRMATO DA USC si prosegue con la definizione, '
     'altrimenti si ripete la firma.'],
    ['Definizione in SIPO non riuscita', 'Atto k formato in ANSC, 1 IN LAVORAZIONE in SIPO.',
     'Non si chiama più ANSC: si ripete la /finalizzaAtto, subito o alla ripresa; il gemello '
     'successivo attende (GE-21).'],
    ['Sessione OTP scaduta a metà', 'Lo stato raggiunto dal passo in corso.', 'Nuovo codice OTP '
     'e si riprova lo stesso passo; la soglia di guardia si valuta sull’intero parto (GE-12).'],
]

SOSPENDI = (
    'SOSPENDI chiude la procedura senza cambiare nulla: gli atti restano nello stato raggiunto, '
    'in ANSC e in SIPO, e il parto si riprende dal riepilogo come un parto interrotto.')

RIPRESA_1 = (
    'Una procedura che accompagna N atti può interrompersi in qualsiasi punto: l’ufficiale '
    'sospende, il browser si chiude, la sessione cade, un servizio non risponde. Dopo DEFINISCI i '
    'numeri sono staccati, gli atti esistono in ANSC e le righe dello store ci sono: la ripresa li '
    'riusa, non li rifà. Non serve un’azione di recupero a parte: è il riepilogo dei gemelli che, '
    'aperto su un parto già avviato, si presenta come pagina di ripresa con il pulsante RIPRENDI.')
RIPRESA_2 = (
    'All’apertura SIPO legge le righe del parto (ATTI_GEMELLARI e ANSC_STATO_ATTO, con '
    'l’interrogazione descritta più avanti) e, per le righe che hanno un identificativo, rilegge in '
    'ANSC lo stato di ciascun atto con R005: lo store può essere rimasto indietro rispetto ad '
    'ANSC, proprio perché la procedura si è interrotta. Lo store registra anche la pagina da cui '
    'riprendere (COD_PAGINA_RIPRESA), ma per il parto prevale lo stato letto in ANSC. Poi decide:')
RIPRESA_VOCI = [
    ('Nessun numero staccato.', 'Il riepilogo è quello ordinario: DEFINISCI parte da capo.'),
    ('Numeri staccati senza identificativi.', 'La prenotazione si è interrotta o ha avuto un '
     'esito incerto: si cercano gli atti per numero comunale (R005) e si completano le righe; se '
     'non ce n’è nessuno si prenota di nuovo con gli stessi numeri. I numeri non si staccano di '
     'nuovo.'),
    ('Atti formati e non definiti.', 'Gli atti a 5 FIRMATO DA USC con l’atto di SIPO ancora '
     '1 IN LAVORAZIONE si definiscono, senza altre chiamate ad ANSC.'),
    ('Il primo gemello non concluso.', 'RIPRENDI riparte dal passo che il suo stato in ANSC '
     'indica: 1 BOZZA documenti e validazione, 2 CONFERMATO firma del dichiarante, 4 FIRMATO DAL '
     'DICHIARANTE conformità, 11 FIRMATO PER CONFORMITÀ firma dell’ufficiale. I gemelli '
     'successivi seguono come di consueto.'),
    ('Stato inatteso.', 'Un atto a 3 ANNULLATO, 9 CANCELLATO o 10 INEFFICACE, o con un '
     'identificativo diverso da quello registrato, è stato toccato fuori da questa procedura (web '
     'app, altro operatore): la ripresa si ferma e il parto compare nella supervisione.'),
    ('Rinuncia al parto.', 'Finché nessun gemello è firmato dall’ufficiale, RINUNCIA AL PARTO '
     'cancella in ANSC gli atti prenotati (R011, 9 CANCELLATO), scarta i numeri (PUT /scarta) e '
     'rende di nuovo modificabile la pratica, compreso l’annullamento della divisione (GE-09). '
     'Dopo la prima firma dell’ufficiale la rinuncia non c’è più: gli atti formati non si '
     'cancellano e i nati restanti vanno comunque formati.'),
    ('Chi riprende.', 'Anche un ufficiale diverso da chi ha avviato il parto, con la propria '
     'sessione OTP. La firma del dichiarante, se il parto si è fermato prima, richiede di nuovo la '
     'sua presenza (GE-22).'),
]

SINTESI_NUOVA = (
    'Il caso 1 in SIPO.', 'Dopo la divisione un riepilogo mostra per ciascun gemello UC e numero '
    'comunale previsto; un solo DEFINISCI stacca i numeri, prenota gli atti e accompagna un '
    'gemello alla volta dall’anteprima alla firma dell’ufficiale, definendo ciascun atto in SIPO '
    'subito dopo. Un errore si riprova o si sospende; un parto interrotto si riprende dal '
    'riepilogo, senza nuovi numeri né nuove prenotazioni.')

GE_NUOVI = [
    ['GE-19', 'Numeri previsti nel riepilogo', 'Il riepilogo mostra i numeri che il numeratore '
     'assegnerebbe, ma be-numeratore-comunale espone quattro operazioni (richiesta, ricerca, '
     'utilizzo, scarto) e nessuna lettura del prossimo numero [R3]. Serve una lettura in più, '
     'oppure il riepilogo mostra solo la posizione. In ogni caso i numeri previsti possono cambiare '
     'fino al DEFINISCI.', 'Aperto'],
    ['GE-20', 'Correzione che cambia l’UC', 'Se durante DEFINISCI la correzione di un errore di '
     'validazione cambia lo stato di un nato, gli UC non coincidono più e la bozza prenotata di quel '
     'gemello ha l’UC sbagliato. Prima di qualunque firma dell’ufficiale si può rinunciare al parto '
     'e passare al caso 2; dopo, quel gemello non si può completare con la sua bozza. Va deciso '
     'come trattarlo e, se serve, chiesto ad ANSC.', 'Aperto'],
    ['GE-21', 'Definizione non riuscita dopo la firma', 'Se la /finalizzaAtto fallisce dopo la '
     'firma dell’ufficiale, l’atto è formato in ANSC e non definito in SIPO. Va verificato che la '
     '/finalizzaAtto si possa ripetere senza effetti doppi (PDF, iscrizione ANPR) e confermato che '
     'il gemello successivo attenda.', 'Aperto'],
    ['GE-22', 'Parto sospeso', 'La ripresa può farla un ufficiale diverso, con la propria sessione '
     'OTP; la firma del dichiarante, se manca, richiede di nuovo la sua presenza. Va deciso con '
     'l’ufficio per quanto un parto possa restare sospeso e se la supervisione debba segnalarlo '
     'dopo un termine.', 'Aperto'],
]


def main():
    d = docx.Document(IN)
    fatti = []

    # 1. In sintesi: il caso 1 in SIPO, prima di «Che cosa resta in SIPO nel caso 2»
    ancora = para_che_inizia(d, 'Che cosa resta in SIPO nel caso 2.')._p
    inserisci_prima(d, ancora, lambda: voce(d, *SINTESI_NUOVA))

    # 2. residuo della v0.4 nell'intestazione della tabella dei passi
    k = sostituisci_nei_run(d, 'caso 1NSC', 'percorso ANSC')
    assert k == 1, k
    fatti.append('«Passo del caso 1NSC» → «Passo del percorso ANSC»')

    # 3. panoramica
    sostituisci_figura(d, 'I due casi: la scelta dopo la divisione',
                       png('gem5_panoramica.pptx.png'), LARGO,
                       'I due casi: la scelta dopo la divisione')

    # 4. caso 1: apertura e tabella dei passi
    D.testo_di(para_che_inizia(d, 'Il percorso inserisce nel flusso di SIPO'), INTRO_1)
    vecchia = tabella_che_contiene(d, 'Riepilogo del gemello 1 → PRENOTA GEMELLI (nuovo)')
    inserisci_prima(d, vecchia._tbl,
                    lambda: tabella(d, PASSI_1, [0.3, 1.45, 2.25, 1.35, 1.25]))
    assert not D.ha_commenti(vecchia._tbl)
    vecchia._tbl.getparent().remove(vecchia._tbl)
    sostituisci_figura(d, 'Caso 1: le pagine', png('gem5_flusso_1.pptx.png'), 5.9,
                       'Caso 1: le pagine, i servizi e gli stati, con le righe dello store')

    # 5. regole: dal passo PRENOTA GEMELLI al riepilogo e a DEFINISCI
    D.testo_di(para_che_inizia(d, 'Regole del passo PRENOTA GEMELLI'),
               'Regole del riepilogo e di DEFINISCI:')
    vecchie = [para_che_inizia(d, t) for t in ('Quando compare.', 'Conferma. Una finestra',
                                               'Numeri comunali. Si staccano',
                                               'UC. Si determina', 'Esito. Ciascun')]
    inserisci_prima(d, vecchie[0]._p, lambda: [voce(d, t, c) for t, c in REGOLE_1])
    for p in vecchie:
        assert not D.ha_commenti(p._p)
        p._p.getparent().remove(p._p)

    # 6. figure delle schermate: riepilogo al posto della 8, la 9 si sposta negli errori
    sostituisci_figura(d, 'Il passo PRENOTA GEMELLI: il riepilogo', png('gem5_riepilogo.png'),
                       LARGO, 'Il riepilogo dei gemelli, con i numeri comunali previsti (ipotesi)')
    togli_figura(d, 'Il passo PRENOTA GEMELLI: l’esito')

    # 7. errori e ripresa, prima del caso 2
    caso2 = D.h(d, 2, 'Caso 2 — gemelli con UC diversi')._p

    def errori_e_ripresa():
        heading(d, 3, 'Quando qualcosa non va a buon fine')
        par(d, ERRORI_INTRO)
        tabella(d, ERRORI, [1.75, 1.95, 2.9])
        figura(d, png('gem5_definisci.png'), LARGO, 'DEFINISCI in corso: il gemello 1 formato e '
               'definito, la firma dell’ufficiale sul gemello 2 non riuscita (ipotesi)')
        par(d, SOSPENDI)
        heading(d, 3, 'L’interruzione e la ripresa del parto')
        par(d, RIPRESA_1)
        par(d, RIPRESA_2)
        for t, c in RIPRESA_VOCI:
            voce(d, t, c)
        figura(d, png('gem5_ripresa.pptx.png'), 5.6, 'La ripresa di un parto interrotto')
        figura(d, png('gem5_ripresa.png'), LARGO, 'Il riepilogo di un parto interrotto: lo stato '
               'letto in ANSC e il passo da cui si riprende (ipotesi)')
    inserisci_prima(d, caso2, errori_e_ripresa)

    # 8. caso 2: il riepilogo al posto di PRENOTA GEMELLI
    k = sostituisci_nei_run(d, 'Compare al posto di PRENOTA GEMELLI', 'Compare nel riepilogo dei '
                            'gemelli al posto di DEFINISCI')
    if k != 1:
        D.sostituisci(d, 'Compare al posto di PRENOTA GEMELLI', 'Compare nel riepilogo dei '
                      'gemelli al posto di DEFINISCI', attese=1, fatti=fatti)
    t2 = tabella_che_contiene(d, 'Gli UC dei nati differiscono: PRENOTA GEMELLI non compare')
    for rr in t2.rows:
        for c in rr.cells:
            if 'PRENOTA GEMELLI non compare' in c.text:
                D.riscrivi_cella(c, c.text.replace('PRENOTA GEMELLI non compare',
                                                   'DEFINISCI non compare'))
    sostituisci_figura(d, 'Caso 2: le pagine', png('gem5_flusso_2.pptx.png'), 5.9,
                       didascalia(d, 'Caso 2: le pagine').text.split(' – ', 1)[1])

    # 9. ANSC_SOGGETTO_ATTO e righe dello store
    D.sostituisci(d, 'Nel caso 1 a PRENOTA GEMELLI, una per gemello', 'Nel caso 1 alla '
                  'prenotazione, dentro DEFINISCI, una per gemello', attese=1, fatti=fatti)
    D.sostituisci(d, 'Nel caso 1 le righe dei gemelli 2…N nascono al passo PRENOTA GEMELLI',
                  'Nel caso 1 le righe dei gemelli 2…N nascono con DEFINISCI, alla prenotazione',
                  attese=1, fatti=fatti)
    rifai_voce(d, para_che_inizia(d, 'Una sola azione.'), 'Una sola azione.',
               'Stacco e prenotazione sono il primo passo di DEFINISCI e una sola azione del '
               'concentratore: i numeri, le righe nuove e l’esito della prenotazione si registrano '
               'insieme. La chiamata ad ANSC però non può stare dentro una transazione del '
               'database; gli esiti che lascia a metà sono trattati più avanti e nella ripresa del '
               'parto.')
    t = tabella_che_contiene(d, 'Righe toccate')
    D.riscrivi_cella(riga_di(t, 'PRENOTA GEMELLI: UC e numeri').cells[0], 'DEFINISCI: UC e numeri')
    D.riscrivi_cella(riga_di(t, 'PRENOTA GEMELLI: R009 /prenota/evento').cells[0],
                     'DEFINISCI: R009 /prenota/evento')
    r = riga_di(t, 'Definisci del gemello k')
    D.riscrivi_cella(r.cells[0], 'Definizione del gemello k, dentro DEFINISCI')
    D.riscrivi_cella(r.cells[2], 'Nessuna colonna: in SIPO l’atto k passa a 2 DEFINITO subito '
                     'dopo la firma dell’ufficiale.')
    r = riga_di(t, 'Chiusura del parto')
    D.riscrivi_cella(r.cells[0], 'Rinuncia al parto')
    D.riscrivi_cella(r.cells[1], 'Tutte, solo se nessun gemello è firmato dall’ufficiale')
    D.riscrivi_cella(r.cells[2], 'Dopo R011: ID_STATO 9 CANCELLATO, COD_FASE ANNULLATO. I numeri '
                     'passano a Scartato (PUT /scarta).')
    D.clona_riga(t, ['Riepilogo dei gemelli', 'Nessuna', 'Sola lettura: UC dei nati e numeri '
                     'previsti; nulla si registra.', '—'])
    riga_di(t, 'Riepilogo → Conferma: divisione')._tr.addnext(
        riga_di(t, 'Riepilogo dei gemelli')._tr)
    D.clona_riga(t, ['Ripresa del parto', 'Le righe con identificativo', 'UPDATE di ID_STATO e '
                     'STATO con lo stato letto in ANSC (R005); COD_FASE e COD_PAGINA_RIPRESA '
                     'secondo il passo da cui si riprende.', '—'])
    riga_di(t, 'Rinuncia al parto')._tr.addprevious(riga_di(t, 'Ripresa del parto')._tr)

    # 10. punti aperti
    op = D.trova_tabella(d, 'tema', 'questione')
    r = riga_di(op, 'GE-09')
    D.riscrivi_cella(r.cells[2], r.cells[2].text + ' Nel caso 1 la proposta è RINUNCIA AL '
                     'PARTO: ammessa finché nessun gemello è firmato dall’ufficiale, cancella gli '
                     'atti con R011, scarta i numeri e rende di nuovo possibile l’annullamento della '
                     'divisione; dopo la prima firma non c’è più.')
    D.riscrivi_cella(r.cells[3], 'Risolto in parte')
    r = riga_di(op, 'GE-12')
    D.riscrivi_cella(r.cells[2], r.cells[2].text + ' DEFINISCI accompagna l’intero parto: allo '
                     'scadere dell’OTP la procedura si ferma sul passo in corso e si riprende con '
                     'un nuovo codice.')
    for riga in GE_NUOVI:
        D.clona_riga(op, riga)

    # 11. nessun PRENOTA GEMELLI fuori dalla Storia
    storia_t = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    residui = [p.text for p in d.paragraphs if 'PRENOTA GEMELLI' in p.text] + \
              [c.text for tb in d.tables if tb._tbl is not storia_t._tbl
               for rr in tb.rows for c in rr.cells if 'PRENOTA GEMELLI' in c.text]
    assert not residui, residui

    # 12. figure rinumerate
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])

    # 13. frontespizio e storia
    for fatto in D.frontespizio(d, '0.5', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.5', 'In sintesi · La modalità di integrazione (caso 1) · Effetti sul '
             'disegno · Punti aperti',
             'Caso 1 rivisto: niente più passo PRENOTA GEMELLI. Dopo la divisione un riepilogo dei '
             'gemelli con i numeri comunali previsti; un solo DEFINISCI stacca i numeri, prenota '
             'gli atti e accompagna un gemello alla volta fino alla firma dell’ufficiale, '
             'definendo ciascun atto in SIPO subito dopo. Nuove sezioni sugli errori (riprova o '
             'sospendi) e sulla ripresa di un parto interrotto, con RINUNCIA AL PARTO finché '
             'nessun gemello è firmato. Diagrammi e schermate rifatti. GE-09, GE-12 integrati; '
             'GE-19…GE-22.')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
