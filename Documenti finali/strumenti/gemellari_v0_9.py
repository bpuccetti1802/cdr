# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.9 (21/11/2026), dal FILE REALE della v0.8 (rivista a mano
dall'utente alle 16:07: «In sintesi», apertura del caso 1, riepilogo, testo dell'atto).

Correzione (decisione dell'utente, 21/11/2026): nel caso 1 il TESTO DELL'ATTO LO GENERA SIPO.
La v0.8 lo diceva composto da ANSC e recuperato in SIPO: è sbagliato. Per le bozze prenotate da
gestionale ANSC ha chiarito (issue #2299, 25/11/2025) che «gli atti in bozza vengono generati dal
sistema senza la composizione» e che «la composizione la trasmettete voi con il servizio di
validazione successivo dell'atto». Quindi: SIPO compone il testo con il formulario, il
concentratore lo invia in composizioneCompleta con R009, R010 lo rilegge come riscontro, la
definizione in SIPO resta quella di oggi. Rivisti la sezione «Il testo dell'atto», le tabelle dei
passi e della sequenza, le schermate e i diagrammi del caso 1, GE-23, GE-24, GE-26 e [A13].
Figure: schermate_gemellari_v0_9.py (gem9_c1_*, gem9_seq_caso1), diagrammi_gemellari_v0_9_pptx.py
(gem9_flusso_1, gem9_panoramica).

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_9.py
"""
import os
import re
import sys

import docx
from docx.oxml.ns import qn

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import par, voce                         # noqa: E402
from gemellari_v0_2 import in_coda, para_che_inizia, sposta_prima  # noqa: E402
from gemellari_v0_4 import rifai_voce, riga_di, sostituisci_figura  # noqa: E402

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.8.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.9.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '21/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')
LARGO = 6.3


def png(nome):
    return os.path.join(IMG, nome)


def tabella_con_intestazione(d, *voci):
    t = [x for x in d.tables if all(v in [c.text for c in x.rows[0].cells] for v in voci)]
    assert len(t) == 1, (voci, len(t))
    return t[0]


def cambia(cella, vecchio, nuovo):
    assert vecchio in cella.text, (vecchio, cella.text)
    D.riscrivi_cella(cella, cella.text.replace(vecchio, nuovo))


# ------------------------------------------------------------------ contenuti
TESTO_INTRO = (
    'Per le bozze prenotate da gestionale il testo dell’atto lo trasmette il gestionale. ANSC lo '
    'ha chiarito a un fornitore che non otteneva l’anteprima di un atto gemellare prenotato '
    '(«Il campo evento.composizioneCompleta mancante»): con la prenotazione da gestionale «gli atti '
    'in bozza vengono generati dal sistema senza la composizione», e «la composizione la '
    'trasmettete voi con il servizio di validazione successivo dell’atto» [A12]. È ciò che la '
    'guida chiede anche sulla web app: la minuta completa, con le formule ministeriali del parto '
    'gemellare (35, 36, 37) e gli identificativi dei gemelli assegnati dalla prenotazione [A3]. Il '
    'testo di ciascun gemello lo genera quindi SIPO, che i testi degli atti li compone già con il '
    'formulario.')

TESTO_VOCI = [
    ('Quando.', 'Per il gemello k, dopo la prenotazione e prima della sua validazione: a quel '
     'punto sono noti il numero comunale del gemello e gli identificativi nazionali dei fratelli, '
     'che la prenotazione restituisce e ANSC_SOGGETTO_ATTO registra. Il testo si compone di nuovo '
     'a ogni nuova validazione (ritorno ai dati, correzione di un errore), perché segue i dati.'),
    ('Come.', 'Con il formulario di oggi (PKG_FORMULARI.FORMULARIO_GENERA_MODELLO) sull’atto SIPO '
     'del gemello, come per l’anteprima di SIPO; per i gemelli SIPO compone già un testo per '
     'ciascun atto (/generaPDFAttoFromFormularioGemelli) [S6]. Le formule sono quelle del parto '
     'gemellare che SIPO usa oggi per questi tipi atto.'),
    ('Che cosa contiene.', 'Le formule ministeriali del parto gemellare, il numero comunale '
     'staccato da DEFINISCI e gli identificativi nazionali dei fratelli. Da quali dati il '
     'formulario legga questi ultimi due è GE-26.'),
    ('Come arriva ad ANSC.', 'Il concentratore riprende il testo prodotto dal formulario (le parti '
     'intestazione, occhio, corpo e piè di pagina della vista V_GTT_TMP_ATTO_A4) e lo pone in '
     'evento.composizioneCompleta del modello evento che invia con R009 /validazione/evento. Il '
     'campo è una stringa e l’esempio del contratto è testo semplice con gli a capo [A13]. Quali '
     'parti del testo di SIPO vi entrino e come si tolga la marcatura destinata al modello di '
     'stampa è GE-24.'),
    ('Il riscontro.', 'Validato l’atto, R010 senza filigrana (presaVisione, ammessa sull’atto '
     'CONFERMATO) restituisce il PDF di ANSC con la composizione ricevuta [A13]: è la copia che il '
     'dichiarante firma, e conferma che ANSC ha il testo di SIPO. Prima della validazione '
     'un’anteprima ANSC non c’è, proprio perché la bozza non ha composizione [A12]: la pagina '
     'mostra il testo di SIPO.'),
    ('Che cosa resta in SIPO.', 'Alla definizione /finalizzaAtto genera il PDF dal formulario e lo '
     'scrive in ATTO_SCANSIONATO, come oggi [S6]: è lo stesso testo inviato ad ANSC, perché dopo la '
     'firma del dichiarante i dati sono vincolati. La definizione non cambia.'),
    ('Correzioni.', 'Prima della firma dell’ufficiale si torna ai dati e si valida di nuovo con il '
     'testo ricomposto; dopo, l’atto è formato e un errore nel testo si corregge con '
     'un’annotazione di rettifica, come per ogni atto formato in ANSC.'),
    ('Il mapping.', 'Il mapping dell’UC ordinario (per esempio Dic_Nasc_001) non dichiara '
     'composizioneCompleta: nella nascita il campo compare in 6 mapping su 289, quelli dei casi '
     'd’uso di servizio [A4]. Per le bozze prenotate ANSC lo chiede comunque: la configurazione '
     'dell’UC deve prevederlo per il parto plurimo, e la regola va confermata con Sogei (GE-23).'),
]

GE_23 = ('Composizione nel mapping', 'Il mapping degli UC ordinari della nascita non dichiara '
         'composizioneCompleta, ma per le bozze prenotate da gestionale ANSC chiede che la '
         'composizione arrivi con la validazione [A12]. Da confermare con Sogei: se il campo sia '
         'obbligatorio per tutti gli atti prenotati, se ANSC lo controlli o lo integri, e come la '
         'configurazione dell’UC lo debba dichiarare per il parto plurimo.')
GE_24 = ('Forma della composizione', 'Il testo di SIPO esce dal formulario in più parti '
         '(intestazione, occhio, corpo, piè di pagina) e con la marcatura per il modello di stampa. '
         'Quali parti entrano in composizioneCompleta, in quale forma (testo semplice, a capo) e '
         'chi la converte: il concentratore o una funzione nuova di SIPO.')
GE_26 = ('Dati del testo di SIPO', 'Il testo del gemello deve contenere il numero comunale '
         'staccato (da DEFINISCI nel caso 1, da DATI PER ANSC nel caso 2) e, nel caso 1, gli '
         'identificativi nazionali dei fratelli restituiti dalla prenotazione: da quali colonne il '
         'formulario li legga, come per gli atti a testo libero [R2].')

A13 = ('ansc/docs/openapi/model_evento.yaml — evento.composizioneCompleta (stringa, «Composizione '
       'completa dell’atto», esempio in testo semplice con gli a capo); '
       'ansc/docs/openapi/R010_anteprima.yaml — /anteprima/evento, presaVisione (anteprima senza '
       'filigrana, risposta 400 se l’atto non è CONFERMATO).')


def main():
    d = docx.Document(IN)
    fatti = []
    storia_t = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')

    # 1. In sintesi
    D.sostituisci(d, 'Il testo dell’atto lo compone ANSC: SIPO lo recupera e lo riporta sull’atto '
                  'di SIPO.', 'Il testo dell’atto lo compone SIPO con il formulario e lo '
                  'trasmette ad ANSC con la validazione, come chiede ANSC per le bozze prenotate '
                  'da gestionale.', attese=1, fatti=fatti)

    # 2. tabella dei passi del caso 1
    t = tabella_con_intestazione(d, 'Pagina o momento in SIPO')
    r = riga_di(t, '6')
    cambia(r.cells[1], 'documenti, anteprima e validazione', 'documenti, testo e validazione')
    cambia(r.cells[2], 'il testo dell’atto è quello composto da ANSC (R010, senza filigrana).',
           'il testo dell’atto lo compone SIPO con il formulario e viaggia nella validazione '
           '(composizioneCompleta); R010 lo rilegge da ANSC.')
    D.riscrivi_cella(r.cells[3], 'R001; formulario di SIPO; R009 /validazione/evento; R010 '
                     '/anteprima/evento')
    r = riga_di(t, '8')
    D.riscrivi_cella(r.cells[1], 'DEFINISCI, gemello k: definizione')
    D.riscrivi_cella(r.cells[2], 'Subito dopo la firma dell’ufficiale: definizione in SIPO, con il '
                     'PDF del testo composto da SIPO, lo stesso inviato ad ANSC; si passa al '
                     'gemello k+1.')
    D.riscrivi_cella(r.cells[3], '/finalizzaAtto')

    # 3. regola del testo
    rifai_voce(d, para_che_inizia(d, 'Il testo dell’atto. Lo compone ANSC'), 'Il testo '
               'dell’atto.', 'Lo compone SIPO con il formulario, gemello per gemello, e lo '
               'trasmette ad ANSC con la validazione, come descritto più avanti.')

    # 4. la sezione «Il testo dell'atto»: contenuto sostituito per intero
    h = D.h(d, 3, 'Il testo dell’atto', esatto=True)._p
    fine = D.h(d, 3, 'La finestra di raccordo dei numeri comunali')._p
    via = []
    e = h.getnext()
    while e is not fine:
        via.append(e)
        e = e.getnext()
    for e in via:
        assert not D.ha_commenti(e)
        e.getparent().remove(e)
    fatti.append('sezione «Il testo dell’atto»: tolti %d elementi' % len(via))
    racc = in_coda(d)
    par(d, TESTO_INTRO)
    for a, b in TESTO_VOCI:
        voce(d, a, b)
    sposta_prima(racc(), fine)

    # 5. sequenza del caso 1
    t = [x for x in d.tables if 'Si arriva con' in [c.text for c in x.rows[0].cells]
         and 'documenti, anteprima e validazione' in x.rows[3].cells[1].text]
    assert len(t) == 1, len(t)
    t = t[0]
    r = riga_di(t, '3')
    D.riscrivi_cella(r.cells[1], 'Gemello k: documenti, testo e validazione, firma del '
                     'dichiarante, conformità, firma dell’ufficiale')
    D.riscrivi_cella(r.cells[3], 'R001, formulario di SIPO, R009, R010, R006, R007')
    cambia(r.cells[4], 'il testo mostrato è quello di ANSC.', 'il testo è quello composto da '
           'SIPO, inviato con la validazione e riletto da ANSC.')
    r = riga_di(t, '4')
    D.riscrivi_cella(r.cells[1], 'Gemello k: definizione in SIPO')
    D.riscrivi_cella(r.cells[3], '/finalizzaAtto')
    D.riscrivi_cella(r.cells[4], 'L’atto formato e la sua definizione in SIPO, con il PDF del '
                     'testo inviato ad ANSC; GEMELLO SUCCESSIVO riporta alla schermata 3 per il '
                     'gemello k+1.')
    r = riga_di(t, '5')
    cambia(r.cells[4], 'ciascuno con il testo di ANSC.', 'ciascuno con il testo composto da SIPO.')

    # 6. figure del caso 1 e panoramica
    sostituisci_figura(d, 'I due casi: la scelta dopo la divisione',
                       png('gem9_panoramica.pptx.png'), LARGO,
                       'I due casi: la scelta dopo la divisione')
    sostituisci_figura(d, 'Caso 1: le pagine', png('gem9_flusso_1.pptx.png'), 5.9,
                       'Caso 1: le pagine, i servizi e gli stati, con le righe dello store')
    sostituisci_figura(d, 'Caso 1: la sequenza delle schermate', png('gem9_seq_caso1.png'), LARGO,
                       'Caso 1: la sequenza delle schermate')
    sostituisci_figura(d, 'Caso 1: il gemello 2 sul passo', png('gem9_c1_gemello.png'), LARGO,
                       'Caso 1: il gemello 2 sul passo della firma del dichiarante, con il testo '
                       'composto da SIPO e inviato ad ANSC (ipotesi)')
    sostituisci_figura(d, 'Caso 1: il gemello 2 formato', png('gem9_c1_definito.png'), LARGO,
                       'Caso 1: il gemello 2 formato in ANSC e definito in SIPO (ipotesi)')
    sostituisci_figura(d, 'Caso 1: l’esito del parto', png('gem9_c1_esito.png'), LARGO,
                       'Caso 1: l’esito del parto (ipotesi)')

    # 7. caso 2: lo stesso testo, un’altra via
    D.sostituisci(d, 'In SIPO resta il PDF che SIPO compone alla definizione (DEFINISCI GEMELLI), '
                  'come per gli atti a testo libero.', 'È lo stesso testo che SIPO genera nel '
                  'caso 1; cambia la via: lì viaggia con la validazione, qui lo copia l’ufficiale. '
                  'In SIPO resta il PDF che SIPO compone alla definizione (DEFINISCI GEMELLI), '
                  'come per gli atti a testo libero.', attese=1, fatti=fatti)

    # 8. punti aperti e riferimenti
    op = D.trova_tabella(d, 'tema', 'questione')
    for cod, (tema, q) in (('GE-23', GE_23), ('GE-24', GE_24), ('GE-26', GE_26)):
        r = riga_di(op, cod)
        D.riscrivi_cella(r.cells[1], tema)
        D.riscrivi_cella(r.cells[2], q)
    rif = [x for x in d.tables if len(x.columns) == 3
           and x.rows[0].cells[1].text.strip() == 'Riferimento']
    assert len(rif) == 1
    D.riscrivi_cella(riga_di(rif[0], '[A13]').cells[1], A13)

    # 9. nessun residuo del testo «composto da ANSC»
    vietate = ('composto da ANSC', 'recuperato da ANSC', 'testo da ANSC', 'compone ANSC',
               'lo recupera da ANSC', 'issue #418')
    testi = [p.text for p in d.paragraphs] + \
            [c.text for tb in d.tables if tb._tbl is not storia_t._tbl
             for rr in tb.rows for c in rr.cells]
    residui = [x for x in testi if any(v in x for v in vietate)]
    assert not residui, residui

    # 10. figure rinumerate, frontespizio, storia
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])
    for fatto in D.frontespizio(d, '0.9', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.9', 'In sintesi · La modalità di integrazione (caso 1) · Punti aperti · '
             'Riferimenti',
             'Corretto il testo dell’atto del caso 1: lo genera SIPO con il formulario e lo '
             'trasmette ad ANSC con la validazione (composizioneCompleta), come ANSC chiede per le '
             'bozze prenotate da gestionale; R010 lo rilegge come riscontro e la definizione in '
             'SIPO resta quella di oggi. Tolto il recupero del testo da ANSC della v0.8. Tabelle, '
             'schermate e diagrammi del caso 1 aggiornati; GE-23, GE-24, GE-26 riformulati.')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
