# -*- coding: utf-8 -*-
"""I diagrammi del caso 1 del parto plurimo, analisi delle nascite gemellari v0.5 (21/11/2026), in
PowerPoint con forme e connettori nativi, modificabili dall'utente.

Decisioni dell'utente (21/11/2026): il passo PRENOTA GEMELLI non c'è più. Dopo la divisione una
pagina di riepilogo mostra i dati previsti; un solo DEFINISCI stacca i numeri, prenota gli atti e
accompagna i gemelli uno alla volta fino alla firma USC, definendo in SIPO ciascun atto subito
dopo; gli errori si riprovano o sospendono; il parto interrotto si riprende dal riepilogo.

  * gem5_flusso_1.pptx   — caso 1, a cinque corsie, con le righe dello store;
  * gem5_flusso_2.pptx   — caso 2 della v0.4, con il riepilogo dei gemelli al posto di PRENOTA
                           GEMELLI;
  * gem5_panoramica.pptx — i due casi, con il caso 1 aggiornato;
  * gem5_ripresa.pptx    — la ripresa di un parto interrotto: che cosa si rilegge in ANSC e da
                           dove si riparte.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v0_5_pptx.py
    qlmanage -t -s 2400 -o img/gemellari img/gemellari/gem5_*.pptx
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagramma_workflow_pptx as B             # noqa: E402
import diagrammi_matrimonio_pptx as M           # noqa: E402
import diagrammi_gemellari_v0_4_pptx as G4      # noqa: E402

DIR = G4.DIR
PAG, BAN, NI = G4.PAG, G4.BAN, G4.NI
NATTI, ATK = G4.NATTI, G4.ATK

FB, FC, FD = 'B — Riepilogo', 'C — Definisci', 'D — Esito'
PASSI_1 = G4.INIZIO + [
    (PAG, 'Riepilogo dei gemelli', 'per ciascun nato: stato, UC comune e numero comunale '
     'PREVISTO; nulla è ancora riservato', 'be-numeratore-comunale\n(lettura, GE-19)', NATTI,
     '1 riga · gemello 1\nIN_LAVORAZIONE', NI, FB),
    (PAG, 'DEFINISCI · numeri e prenotazione', 'una sola azione: N numeri staccati, R009 con '
     'l’UC comune e il totale dei gemelli', 'POST /richiesta\nR009 /prenota/evento', NATTI,
     'N righe\nPRENOTATO · NUMERO_ATTO · ID_ANSC', 'N atti\n1 BOZZA', FC),
    (BAN, 'PER CIASCUN GEMELLO k = 1 … N', 'dentro DEFINISCI, in ordine di nascita; si passa '
     'al gemello k+1 solo dopo la definizione del gemello k', '', '', '', '', FC),
    (PAG, 'Documenti del gemello k', 'certificato medico se nato morto o nato vivo e poi '
     'deceduto', 'R001 · preverifica', ATK, 'riga k\nDOCUMENTI_ACQUISITI', 'atto k\n1 BOZZA', FC),
    (PAG, 'Anteprima · Validazione del gemello k', 'atto con gli idAnsc dei fratelli; R009 '
     'all’apertura, sulla bozza prenotata', 'R009 /validazione/evento', ATK, 'riga k\nVALIDATO',
     'atto k\n2 CONFERMATO', FC),
    (PAG, 'Firma del dichiarante', 'cartacea, acquisita come processo verbale', 'R006',
     ATK, 'riga k\nVALIDATO', 'atto k\n4 FIRMATO DAL DICHIARANTE', FC),
    (PAG, 'Conformità', 'attestazione firmata dall’ufficiale', 'R007 /attestazione/firma',
     ATK, 'riga k\nVALIDATO', 'atto k\n11 FIRMATO PER CONFORMITÀ', FC),
    (PAG, 'Firma dell’ufficiale', 'l’atto del gemello k è formato: non si torna indietro',
     'R007 /firma_usc', ATK, 'riga k\nFIRMATO', 'atto k\n5 FIRMATO DA USC', FC),
    (PAG, 'Definizione del gemello k', 'subito, in SIPO: ANSC e SIPO allineati gemello per '
     'gemello', '/finalizzaAtto', '2 DEFINITO\natto k', 'riga k\nFIRMATO', 'atto k\n5 FIRMATO DA USC',
     FC),
    (PAG, 'Esito del parto', 'tutti gli atti formati in ANSC e definiti in SIPO; allineamento '
     'anagrafico secondo [R1]', '', '2 DEFINITO\ntutti gli atti', 'N righe\nFIRMATO',
     'N atti\n5 FIRMATO DA USC', FD),
]
NOTA_1 = (
    'CASO 1 — TUTTI I GEMELLI CON LO STESSO UC. Il riepilogo mostra i numeri previsti senza '
    'riservarli; DEFINISCI li stacca e prenota gli atti con l’UC comune (issue #571), il numero '
    'dei gemelli è il totale (#611). Un errore ferma il gemello in lavorazione: si riprova o si '
    'sospende, e un parto sospeso o interrotto si riprende dal riepilogo, che rilegge in ANSC lo '
    'stato di ogni atto e non stacca né prenota di nuovo.')


def flusso():
    return M.genera(
        PASSI_1, 'Parto plurimo — caso 1: gemelli con lo stesso UC, tutto da SIPO',
        'Dopo la divisione il riepilogo mostra i dati che il numeratore assegnerà; DEFINISCI '
        'stacca i numeri, prenota gli atti e accompagna un gemello alla volta per anteprima, '
        'validazione, firme e definizione in SIPO.',
        os.path.join(DIR, 'gem5_flusso_1.pptx'), nota=NOTA_1, colore_nota='blu',
        fasi_viola=(), etichetta_viola='ciclo per gemello',
        sottotitolo_niente='fino alla prenotazione')


def flusso_2():
    """Il caso 2 della v0.4 con il riepilogo dei gemelli al posto di PRENOTA GEMELLI."""
    passi = [(t[0], t[1], 'riepilogo dei gemelli: DEFINISCI non compare; il messaggio indica '
              'la web app; DATI PER ANSC') + t[3:] if t[1] == 'Riepilogo · UC diversi' else t
             for t in G4.PASSI_2]
    assert passi != G4.PASSI_2
    return M.genera(
        passi, 'Parto plurimo — caso 2: gemelli con UC diversi, web app e recupero in SIPO',
        'Compilazione, divisione e numeri restano in SIPO; prenotazione, completamento con il caso '
        'd’uso di servizio e firme si fanno sulla web app; RECUPERA GEMELLI aggancia gli N atti in '
        'una volta e DEFINISCI GEMELLI li definisce in SIPO.',
        os.path.join(DIR, 'gem5_flusso_2.pptx'), nota=G4.NOTA_2, colore_nota='blu',
        non_ritorno=False, fasi_viola=('Web app',), etichetta_viola='web app ANSC',
        sottotitolo_niente='finché non si va sulla web app')


def panoramica():
    return G4.panoramica(os.path.join(DIR, 'gem5_panoramica.pptx'), caso1=(
        ('Riepilogo dei gemelli', 'per ciascun nato UC comune e numero comunale previsto, non '
         'riservato'),
        ('DEFINISCI', 'N numeri e R009 /prenota/evento; poi per ciascun gemello anteprima e '
         'VALIDA · firma del dichiarante · conformità · firma USC · definizione in SIPO'),
        ('Esito del parto · ripresa', 'tutti formati e definiti; se interrotto, RIPRENDI dal '
         'riepilogo senza nuovi numeri')))


def ripresa(percorso=os.path.join(DIR, 'gem5_ripresa.pptx'),
            righe_parto='le righe del parto: ATTI_GEMELLARI e ANSC_STATO_ATTO'):
    W, H = 10.0, 9.0
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = B.rgb('ffffff')
    B.testo(sl, 0.25, 0.15, W - 0.5, 0.35, 'Parto plurimo, caso 1: la ripresa di un parto '
            'interrotto', 15, True, '1f3a5f', PP_ALIGN.CENTER)
    B.testo(sl, 0.6, 0.5, W - 1.2, 0.3, 'Prima si verifica in ANSC, poi si decide: i numeri già '
            'staccati e gli atti già prenotati non si rifanno', 8.5, False, B.MUTED,
            PP_ALIGN.CENTER, corsivo=True)

    def box(x, y, w, h, col, tit, sub, forma=MSO_SHAPE.ROUNDED_RECTANGLE, trat=False):
        return B.riquadro(sl, x, y, w, h, col, [(tit, 9, True, None), (sub, 7, False, B.MUTED)],
                          forma=forma, tratteggio=trat)

    def rombo(x, y, w, h, tit, sub):
        return B.riquadro(sl, x, y, w, h, 'giallo', [(tit, 8.5, True, None),
                                                     (sub, 7, False, None)],
                          forma=MSO_SHAPE.DIAMOND)

    xc, wc = 3.3, 3.4
    a = box(xc, 0.95, wc, 0.62, 'blu', 'Apertura del riepilogo o di un atto del parto',
            righe_parto)
    d1 = rombo(xc + 0.25, 1.85, wc - 0.5, 0.95, 'Numeri staccati?', 'NUMERO_ATTO sulle righe')
    n1 = box(0.3, 1.99, 2.6, 0.66, 'verde', 'Riepilogo ordinario',
             'numeri previsti; DEFINISCI parte da capo')
    d2 = rombo(xc + 0.25, 3.05, wc - 0.5, 0.95, 'Identificativi ANSC?', 'ID_ANSC sulle righe')
    n2 = box(7.1, 2.95, 2.6, 1.15, 'giallo', 'Prenotazione dall’esito incerto',
             'R005 per numero comunale: atti trovati → si completano le righe; nessun atto → '
             'nuova prenotazione con gli STESSI numeri; mai alla cieca')
    r1 = box(xc, 4.3, wc, 0.66, 'blu', 'R005 per ciascun gemello',
             'lo stato letto in ANSC sostituisce quello dello store')
    r2 = box(xc, 5.2, wc, 0.66, 'verde', 'Formati e non definiti',
             'stato 5 in ANSC e 1 in SIPO: /finalizzaAtto, senza chiamare ANSC')
    r3 = box(xc, 6.1, wc, 1.0, 'verde', 'Primo gemello non concluso',
             'si riprende dal passo che il suo stato indica: 1 BOZZA → documenti e validazione · '
             '2 CONFERMATO → firma del dichiarante · 4 → conformità · 11 → firma USC')
    r4 = box(xc, 7.4, wc, 0.62, 'verde', 'DEFINISCI prosegue', 'gemello per gemello fino '
             'all’esito del parto')
    x1 = box(0.3, 4.3, 2.6, 1.15, 'rosso', 'Stato inatteso',
             '3, 9, 10 o un idAnsc diverso: la ripresa si ferma; supervisione e ricerca della '
             'causa (web app, altro operatore)', trat=True)
    x2 = box(7.1, 4.3, 2.6, 1.6, 'rosso', 'RINUNCIA AL PARTO',
             'solo se nessun gemello è a 5: R011 su ogni atto prenotato (→ 9 CANCELLATO), '
             'PUT /scarta dei numeri; la pratica torna modificabile', trat=True)

    B.freccia(sl, a, 2, d1, 0)
    B.freccia(sl, d1, 1, n1, 3, colore='3f8f5f')
    B.testo(sl, 2.95, 2.1, 0.5, 0.15, 'no', 7.5, True, '3f8f5f')
    B.freccia(sl, d1, 2, d2, 0)
    B.testo(sl, 5.05, 2.83, 0.5, 0.15, 'sì', 7.5, True, B.INK)
    B.freccia(sl, d2, 3, n2, 1, colore='a07a00')
    B.testo(sl, 6.45, 3.32, 0.5, 0.15, 'no', 7.5, True, 'a07a00')
    B.freccia(sl, d2, 2, r1, 0)
    B.testo(sl, 5.05, 4.03, 0.5, 0.15, 'sì', 7.5, True, B.INK)
    B.gomito(sl, [(8.4, 4.1), (8.4, 4.2), (6.75, 4.2), (6.75, 4.45), (6.7, 4.45)],
             colore='a07a00')
    B.freccia(sl, r1, 1, x1, 3, colore='b00020', tratteggio=True)
    for p, q in ((r1, r2), (r2, r3), (r3, r4)):
        B.freccia(sl, p, 2, q, 0)
    B.gomito(sl, [(6.7, 6.6), (7.0, 6.6), (7.0, 5.9), (7.1, 5.9)], colore='b00020',
             tratteggio=True)
    B.testo(sl, 7.05, 6.0, 2.6, 0.3, 'in alternativa, finché nessun gemello è formato', 7,
            False, 'b00020', corsivo=True)
    B.riquadro(sl, 0.3, 8.2, W - 0.6, 0.6, 'blu',
               [('Gli atti già firmati dall’ufficiale non si toccano', 8, True, None),
                ('Un gemello formato in ANSC è definito in SIPO anche dalla ripresa; ciò che '
                 'ancora manca si riprende dal suo stato vero, letto in ANSC', 7, False, B.MUTED)],
               forma=MSO_SHAPE.RECTANGLE)
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


if __name__ == '__main__':
    for p in (flusso(), flusso_2(), panoramica(), ripresa()):
        print('scritto:', os.path.relpath(p, QUI))
