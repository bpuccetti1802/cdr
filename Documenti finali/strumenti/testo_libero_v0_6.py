# -*- coding: utf-8 -*-
"""v0.6 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC»: il passo DEFINISCI.

⚠️ Si parte dal FILE REALE della v0.5, che l'utente ha rimaneggiato e che porta **due commenti
di Word** ancorati al paragrafo dello store («dettagliare gli stati di fase», «Chiedere a
Rosa»): quel paragrafo non si tocca.

Il cambiamento, deciso con l'utente il 12/11/2026. Nell'Anteprima, dopo COPIA TESTO, compare
**DEFINISCI**, che apre una **modale** di aggancio all'atto ANSC. Scelto o digitato l'idAnsc,
**l'atto e' terminato e si esce**: percorso di salvataggio ordinario di SIPO (stato 2 DEFINITO)
e `ANSC_STATO_ATTO` con `ID_ANSC`. Un passaggio solo, nessuna schermata di esito.

⚠️ Le pagine del «Recupero Atto ANSC» NON si rimuovono: cambiano destinatario. Servono agli atti
**nati interamente sulla WebApp**, che in SIPO non hanno mai avuto una bozza ne' un numero
staccato. Sono due casi diversi e meritano due strade, e il documento ora lo dice.

Rinumerazione delle figure: la modale entra come Figura 5 e le successive scalano di uno.
Verificato prima di farlo che ogni «Figura N» compaia **una sola volta**, cioe' solo nelle
didascalie: nel testo non ci sono rimandi per numero da riallineare.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/testo_libero_v0_6.py
"""
import os
import shutil
import sys

import docx
from docx.shared import Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
NOME = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC'
SRC = os.path.join(FIN, NOME + '_v0.5.docx')
OUT = os.path.join(FIN, NOME + '_v0.6.docx')
IMG = os.path.join(FIN, 'strumenti', 'img', 'testo_libero')
DATA = '12/11/2026'


# ------------------------------------------------------------------ primitive
def pezzi_di(s):
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
    """Celle con il markup interpretato, apici inversi compresi."""
    t = D.tabella(doc, prima, [['' for _ in r] for r in righe], modello, larghezze)
    for i, riga in enumerate(righe):
        for j, val in enumerate(riga):
            cel = t.cell(i, j)
            cel.paragraphs[0]._p.getparent().remove(cel.paragraphs[0]._p)
            p = cel.add_paragraph()
            p.alignment = D.GIUST
            for txt, grassetto, mono in pezzi_di(str(val)):
                r = p.add_run(txt)
                r.bold = grassetto or i == 0
                r.font.size = Pt(8 if mono else 9)
                if mono:
                    r.font.name = 'Courier New'
    return t


# =================================================================== contenuti
CRITERI = [
    ['Criterio', 'Valore, già noto a SIPO', 'In R005'],
    ['Data', 'Il giorno corrente.', '`dataDa`, `dataA`'],
    ['Comune di registrazione', 'ROMA (RM), in sola lettura.', '`idComuneRegistrazione` = 8165'],
    ['Tipo evento', 'Quello del tipo atto (MORTE).',
     '`idTipoEvento`, decodifica ANSC_01'],
    ['Numero comunale atteso', 'Il numero staccato, in sola lettura.',
     '**Non è un criterio**: SIPO confronta `numeroatto` di ciascun atto e preseleziona '
     'quello che coincide.'],
    ['Stato', '5 — FIRMATO DA USC.',
     'Nessun criterio: R005 non filtra per stato, la risposta la filtra SIPO.'],
]

CONFERMA = [
    ['Dove', 'Che cosa viene scritto'],
    ['`ANSC_STATO_ATTO`', '`ID_ANSC` dell’atto agganciato; lo stato passa da `WA` a '
     '**5 FIRMATO DA USC**, che è la replica di ciò che ANSC dichiara; `COD_FASE` a '
     '`FIRMATO`. Restano il numero comunale e il contrassegno di atto a testo libero.'],
    ['L’atto di SIPO', '`ID_STATO_PRATICA` da 1 a **2 DEFINITO** e '
     '`DATA_DEFINIZIONE_ATTO`, come per qualunque altro atto: è lo stesso '
     '`/finalizzaAtto` del percorso ordinario.'],
    ['Il numeratore comunale', 'Il numero smette di essere impegnato e diventa **utilizzato**, '
     'con l’identificativo ANSC che lo giustifica.'],
]


def scrivi(doc, modello):
    # ── 1) la figura 4 cambia: la barra dei bottoni diventa a tre
    esito = D.sostituisci_immagine(doc, 'Figura 4', os.path.join(
        IMG, 'tl_2_anteprima_numero.png'))
    print('  figura 4 sostituita:', esito)
    if not esito:
        raise SystemExit('la figura 4 non e\' stata sostituita')
    D.sostituisci(doc, 'Figura 4 — Anteprima: il numero comunale in alto e COPIA TESTO.',
                  'Figura 4 — Anteprima: il numero comunale in alto, COPIA TESTO e '
                  'DEFINISCI, che resta inibito finché l’atto non è stato formato '
                  'sulla WebApp.', attese=1, etichetta='didascalia 4')

    # ── 2) le figure successive scalano di uno (in ordine decrescente, per non accavallarsi)
    for vecchio in (8, 7, 6, 5):
        D.sostituisci(doc, 'Figura %d —' % vecchio, 'Figura %d —' % (vecchio + 1),
                      attese=1, etichetta='rinumerazione figura %d' % vecchio)

    # ── 3) la nota «5 bis» dell'utente diventa la sezione vera
    nota = None
    for p in doc.paragraphs:
        if p.text.strip().startswith('5 bis aggiungere'):
            nota = p
            break
    if nota is None:
        raise SystemExit('nota «5 bis» non trovata')

    h(doc, nota._p, 3, 'Passo 5 bis — DEFINISCI: l’aggancio all’atto ANSC')
    D.testo_di(nota, '')
    _versa(nota, '**5 bis — DEFINISCI.** Il bottone compare accanto a COPIA TESTO e resta '
                 'inibito finché l’atto non è stato formato sulla WebApp. '
                 'È **lo stato sullo store ad abilitarlo, non il clic nella sessione del '
                 'browser**: l’operatore esce da SIPO, forma l’atto sulla WebApp e '
                 'rientra dopo minuti, magari riaprendo la pagina. Se dipendesse dal clic, al '
                 'rientro il bottone sparirebbe; dipendendo dallo stato `WA`, al rientro è '
                 'già lì.')

    # ── 4) il corpo della sezione nuova, prima del capitolo del recupero
    ancora = D.h(doc, 3, 'Passo 6 — il recupero')._p

    par(doc, ancora, 'DEFINISCI non è un passo speciale di questo percorso: **è la '
                     'chiusura ordinaria di SIPO**, la stessa di un atto qualunque. La sola '
                     'condizione in più è che SIPO sappia **quale** atto ANSC sta '
                     'chiudendo, e quindi ne conosca l’identificativo. Per questo il '
                     'bottone apre una finestra di aggancio invece di salvare subito.')
    D.immagine(doc, ancora, os.path.join(IMG, 'tl_2b_definisci_modale.png'), 6.1,
               'Figura 5 — La finestra di aggancio: criteri già noti, candidati con '
               'quello coincidente preselezionato, e l’inserimento diretto '
               'dell’identificativo.')
    par(doc, ancora, 'La finestra **non chiede di digitare nulla**, perché i criteri sono '
                     'già tutti in mano a SIPO. La ricerca parte all’apertura, con '
                     'R005 `/consultazione/ansc/evento`.')
    tabella(doc, ancora, CRITERI, modello, [1.5, 2.3, 2.6])
    par(doc, ancora, 'I candidati sono gli atti formati nel giorno e non ancora agganciati, '
                     'elencati con identificativo ANSC, numero comunale, data e ora di '
                     'formazione e intestatario. **Quello il cui numero comunale coincide con '
                     'il numero staccato è già selezionato** e porta il distintivo che '
                     'lo dichiara: nel caso ordinario all’ufficiale resta solo da '
                     'confermare.')
    voce(doc, ancora, 'L’inserimento diretto.', 'Se l’ufficiale ha annotato '
         'l’identificativo ANSC sulla WebApp può **digitarlo** invece di sceglierlo, e '
         'VERIFICA ne controlla l’esistenza e lo stato. È la via più rapida quando '
         'i candidati del giorno sono molti.')
    voce(doc, ancora, 'Quando l’atto non compare.', 'Un rimando porta alla **ricerca '
         'estesa** descritta nei paragrafi seguenti, per intestatario o su un intervallo di date '
         'più largo. Non si duplica dentro la finestra ciò che esiste già come '
         'pagina.')
    voce(doc, ancora, 'Solo gli atti firmati.', 'L’elenco mostra i soli atti in stato '
         '**5 FIRMATO DA USC**. Un atto validato ma non ancora firmato è in stato 2 '
         'CONFERMATO e **non si aggancia**: agganciarlo lascerebbe in SIPO un atto definito a '
         'fronte di un atto ANSC che può ancora cambiare.')

    par(doc, ancora, '**6 — DEFINISCI L’ATTO.** La conferma è un passaggio solo: '
                     'non c’è una schermata di esito, perché con essa **l’atto '
                     'è concluso e si esce**. In quel momento:')
    tabella(doc, ancora, CONFERMA, modello, [1.5, 4.9])
    par(doc, ancora, 'La scelta di un passaggio solo ha un prezzo, che conviene dichiarare: '
                     '**agganciare l’atto sbagliato è un errore che si corregge male**, '
                     'perché chiude in SIPO un atto legandolo a un identificativo altrui. '
                     'Lo mitigano tre cose già nella finestra — la preselezione sul '
                     'numero comunale, il distintivo che la motiva e il riepilogo dei dati '
                     'dell’atto scelto — ma resta un punto in cui l’attenzione '
                     'dell’ufficiale è l’ultima difesa.')

    # ── 5) il capitolo del recupero cambia destinatario, non contenuto
    h(doc, ancora, 3, 'Gli atti nati interamente sulla WebApp')
    par(doc, ancora, 'Le pagine che seguono **restano, e servono a un caso diverso**: '
                     'l’atto che nasce e si chiude sulla WebApp senza essere mai '
                     'cominciato in SIPO. Lì non c’è una bozza da definire e il '
                     'numero comunale non è stato staccato da SIPO: va letto dall’atto '
                     'e il percorso parte dalla ricerca, non dall’Anteprima.')
    tabella(doc, ancora, [
        ['', 'Atto cominciato in SIPO', 'Atto nato sulla WebApp'],
        ['Il numero comunale', 'Staccato da SIPO: è già noto e impegnato.',
         'Assegnato sulla WebApp: va letto dall’atto.'],
        ['Da dove si parte', 'Dall’Anteprima, con DEFINISCI.',
         'Dalla pagina «Recupero Atto ANSC».'],
        ['Come si chiude', 'Un passaggio solo: finestra di aggancio e conferma.',
         'Ricerca, riepilogo e conferma.'],
        ['Figure', '4 e 5', '6, 7, 8 e 9'],
    ], modello, [1.3, 2.6, 2.5])


def intesta(doc):
    for fatto in D.frontespizio(doc, '0.6', NOME + '_v0.6', DATA):
        print('  ' + fatto)
    D.storia(doc, DATA, '0.6', 'Le pagine di SIPO',
             'Nuovo passo DEFINISCI, deciso con il committente. Nell’Anteprima, dopo COPIA '
             'TESTO, compare un bottone DEFINISCI che resta inibito finché l’atto non '
             'è stato formato sulla WebApp; la sua abilitazione dipende dallo stato sullo '
             'store e non dal clic, perché l’operatore esce da SIPO e rientra dopo '
             'minuti. Il bottone apre una finestra di aggancio all’atto ANSC con i criteri '
             'già noti — data, comune, tipo evento e numero comunale atteso — e i '
             'candidati del giorno, con quello dal numero comunale coincidente preselezionato; '
             'in alternativa l’identificativo ANSC si può digitare. La conferma è '
             'un passaggio solo: l’atto è concluso e si esce, con il percorso di '
             'salvataggio ordinario di SIPO (stato 2 DEFINITO) e ANSC_STATO_ATTO che riceve '
             'ID_ANSC e lo stato 5. Le pagine del recupero restano e cambiano destinatario: '
             'servono agli atti nati interamente sulla WebApp, e una tabella distingue i due '
             'casi. Figura 4 rifatta, nuova Figura 5, le successive rinumerate.')


if __name__ == '__main__':
    shutil.copyfile(SRC, OUT)
    doc = docx.Document(OUT)
    scrivi(doc, doc.tables[-1])
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
