# -*- coding: utf-8 -*-
"""Diagrammi di flusso dei due percorsi per gli atti che SIPO non gestisce in automatico
(richiesta dell'utente del 22/10/2026), su UNA pagina PowerPoint con forme e connettori nativi,
così che l'utente li possa modificare.

  Gestione 1 — l'atto si stende in SIPO e solo al Riepilogo si scopre che non ha un UC: numero
               comunale, eventuale anteprima del testo generato, stato «YY Sospeso», stesura
               sulla web app con un UC di servizio, ritorno in SIPO con R005, importazione.
  Gestione 2 — l'atto (es. a testo libero) si riconosce alla richiesta: nuova pagina col numero
               comunale, stato «YY Sospeso», stesura sulla web app con qualsiasi UC, ritorno in
               SIPO con R005, importazione con transcodifica.

La conclusione in SIPO è marcata «?!» come nel testo dell'utente: non è ancora definita. «YY» è il
codice di stato che l'utente non ha ancora assegnato.

Corsie per ciascun processo: SIPO · stato ANSC · web app ANSC. Primitive da
diagramma_workflow_pptx.py.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagramma_testo_libero_pptx.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagramma_workflow_pptx import (INK, MUTED, freccia, gomito, linea, rgb,  # noqa: E402
                                     riquadro, testo)

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(QUI), 'DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.1.pptx')

W, H = 16.0, 9.0
Y0, GAP = 1.52, 0.13
ROSSO = 'b03a48'
MSG = '«Non è possibile gestire in automatico questo atto in SIPO; devi inserirlo direttamente ' \
      'in WebApp e ritornare su SIPO per concluderlo.»'

# passi: (corsia, colore, righe di testo, altezza, servizio a fianco, tratteggio)
#   corsia: S = SIPO, D = diamante in SIPO, T = stato ANSC, A = web app ANSC
P1 = [
    ('S', 'blu', [('Stesura dell’atto su SIPO', 8.5, True, None),
                  ('fino alla pagina di Riepilogo', 7, False, MUTED)], 0.44, None, False),
    ('D', 'bianco', [('Riepilogo:', 7, True, None),
                     ('esiste un UC per l’atto?', 7, True, None)], 0.62, None, False),
    ('S', 'blu', [('Riepilogo senza UC', 8.5, True, None),
                  ('non si presentano la lista dei firmatari né quella degli allegati', 7, False,
                   MUTED)], 0.5, None, False),
    ('S', 'rosso', [('Messaggio del sistema', 8, True, ROSSO), (MSG, 6.5, False, INK)], 0.62, None,
     False),
    ('S', 'blu', [('Stacco del numero comunale', 8.5, True, None)], 0.44,
     'num-ansc-sipo · creaPrenotazione', False),
    ('S', 'blu', [('Anteprima: testo dell’atto generato', 8.5, True, None),
                  ('solo per i tipi atto NON a testo libero, il cui testo è generato', 7, False,
                   MUTED)], 0.5, None, True),
    ('T', 'giallo', [('YY · SOSPESO', 8.5, True, None),
                     ('in attesa della stesura sulla web app', 6.5, False, MUTED)], 0.5, None,
     False),
    ('A', 'viola', [('Stesura dell’atto sulla web app', 8.5, True, None),
                    ('con un UC di servizio; si può copiare il testo generato da SIPO', 7, False,
                     MUTED)], 0.6, None, False),
    ('S', 'blu', [('Ritorno in SIPO', 8.5, True, None),
                  ('ricerca dell’atto appena steso sulla web app', 7, False, MUTED)], 0.48,
     'R005 · consultazione dell’atto', False),
    ('S', 'blu', [('Importazione dei dati', 8.5, True, None),
                  ('idAnsc · idUsecase · idVersion', 7, False, INK),
                  ('testo · idSoggettoAnsc · …', 7, False, INK)], 0.62, None, False),
    ('S', 'grigio', [('?! Conclusione del processo in SIPO', 8.5, True, ROSSO),
                     ('da definire', 7, False, MUTED)], 0.46, None, True),
]

P2 = [
    ('S', 'blu', [('Richiesta di stesura di un tipo atto', 8.5, True, None),
                  ('l’USC sceglie, ad esempio, un atto a testo libero', 7, False, MUTED)], 0.5,
     None, False),
    ('S', 'rosso', [('Messaggio del sistema', 8, True, ROSSO), (MSG, 6.5, False, INK)], 0.62, None,
     False),
    ('S', 'blu', [('Nuova pagina: stacco del numero comunale', 8.5, True, None),
                  ('l’USC vi è indirizzato direttamente', 7, False, MUTED)], 0.5,
     'num-ansc-sipo · creaPrenotazione', False),
    ('T', 'giallo', [('YY · SOSPESO', 8.5, True, None),
                     ('in attesa della stesura sulla web app', 6.5, False, MUTED)], 0.5, None,
     False),
    ('A', 'viola', [('Stesura dell’atto sulla web app', 8.5, True, None),
                    ('con qualsiasi UC', 7, False, MUTED)], 0.5, None, False),
    ('S', 'blu', [('Ritorno in SIPO', 8.5, True, None),
                  ('ricerca dell’atto appena steso sulla web app', 7, False, MUTED)], 0.48,
     'R005 · consultazione dell’atto', False),
    ('S', 'blu', [('Importazione dei dati', 8.5, True, None),
                  ('transcodifica di comuni, province e nazioni, …', 7, False, INK),
                  ('idAnsc · testo · soggetti', 7, False, INK),
                  ('idSoggettoAnsc · idSoggettoAnpr · idAnpr · …', 7, False, INK)], 0.78, None,
     False),
    ('S', 'grigio', [('?! Conclusione del processo in SIPO', 8.5, True, ROSSO),
                     ('da definire', 7, False, MUTED)], 0.46, None, True),
]


def pannello(sl, x0, titolo, sottotitolo, passi):
    """Un processo nelle sue tre corsie. x0 = margine sinistro del pannello (largo 7.6")."""
    corsie = {'S': (x0, 3.45, 'SIPO'), 'T': (x0 + 3.55, 1.75, 'Stato ANSC'),
              'A': (x0 + 5.40, 2.20, 'Web app ANSC')}
    testo(sl, x0, 0.80, 7.6, 0.25, titolo, 11, True, '1f3a5f')
    testo(sl, x0, 1.03, 7.6, 0.2, sottotitolo, 8, False, MUTED, corsivo=True)
    ytot = Y0 + sum(p[3] for p in passi) + GAP * (len(passi) - 1)
    for cx, cw, nome in corsie.values():
        s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(Y0 - 0.25), Inches(cw),
                                Inches(ytot - Y0 + 0.37))
        s.fill.solid()
        s.fill.fore_color.rgb = rgb('f5f7fa')
        s.line.fill.background()
        s.shadow.inherit = False
        testo(sl, cx, Y0 - 0.23, cw, 0.18, nome, 8, True, INK, PP_ALIGN.CENTER)

    xs, ws = x0 + 0.10, 2.25                 # colonna principale di SIPO
    xl, wl = x0 + 2.45, 0.92                 # a fianco: servizi e uscita del «Sì»
    forme, y = [], Y0
    for k, (corsia, col, righe, h, servizio, tratt) in enumerate(passi):
        if corsia == 'D':
            f = riquadro(sl, xs, y, ws, h, col, righe, forma=MSO_SHAPE.DIAMOND)
            si = riquadro(sl, xl, y + 0.05, wl, h - 0.10, 'grigio',
                          [('Percorso ordinario', 7.5, True, None),
                           ('firmatari, allegati, R009…', 6.5, False, MUTED)],
                          tratteggio=True)
            freccia(sl, f, 3, si, 1)
            testo(sl, xs + ws - 0.05, y + h / 2 - 0.17, 0.25, 0.14, 'Sì', 7, True, INK)
            testo(sl, xs + ws / 2 + 0.06, y + h + 0.005, 0.3, 0.14, 'No', 7, True, INK)
        elif corsia == 'S':
            f = riquadro(sl, xs, y, ws, h, col, righe, tratteggio=tratt)
        else:
            cx, cw, _ = corsie[corsia]
            f = riquadro(sl, cx + 0.12, y, cw - 0.24, h, col, righe, tratteggio=tratt)
        if servizio:
            sv = riquadro(sl, xl, y + 0.04, wl, h - 0.08, 'bianco', [(servizio, 6.5, False, None)],
                          forma=MSO_SHAPE.RECTANGLE)
            freccia(sl, f, 3, sv, 1, colore='94a3b8', spessore=0.9)
        forme.append((corsia, f, y, h))
        y += h + GAP

    # collegamenti fra passi consecutivi
    for (ca, a, ya, ha), (cb, b, yb, hb) in zip(forme, forme[1:]):
        lato = lambda c: 'S' if c == 'D' else c                         # noqa: E731
        if lato(ca) == lato(cb):
            freccia(sl, a, 2, b, 0)
            continue
        ax = a.left / 914400 + a.width / 914400 / 2
        bx = b.left / 914400 + b.width / 914400 / 2
        # cambio di corsia: giù da A, di lato nell'intervallo fra i due passi, giù su B
        # (dal fondo e non dal fianco, così la linea non attraversa i riquadri dei servizi)
        ym = yb - GAP / 2
        gomito(sl, [(ax, ya + ha), (ax, ym), (bx, ym), (bx, yb)])
    return ytot


def genera(percorso=OUT):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = rgb('ffffff')

    testo(sl, 0.3, 0.18, 15.4, 0.35, 'Gli atti che SIPO non gestisce in automatico: i due percorsi '
          'attraverso la web app ANSC', 15, True, '1f3a5f', PP_ALIGN.CENTER)
    testo(sl, 0.3, 0.5, 15.4, 0.25, 'Stesura sulla web app, numero comunale e ritorno in SIPO '
          'per l’importazione dei dati', 8.5, False, MUTED, PP_ALIGN.CENTER, corsivo=True)

    y1 = pannello(sl, 0.3, 'Gestione 1 — atti a testo libero o non gestiti (onerosa/rischiosa)',
                  'Per i tipi atto NON a testo libero inseriti in web app con un UC di servizio: '
                  'l’assenza di UC si scopre al Riepilogo', P1)
    y2 = pannello(sl, 8.1, 'Gestione 2 — atti a testo libero',
                  'Per i tipi atto a testo libero inseriti in web app con qualsiasi UC: il caso '
                  'si riconosce alla richiesta', P2)
    linea(sl, 8.0, 0.80, 8.0, max(y1, y2) + 0.1, 'cbd5e1', tratteggio=False, spessore=1)

    # legenda, sotto il pannello più corto (il secondo)
    yl = y2 + 0.35
    voci = [('blu', 'passo in SIPO'), ('bianco', 'servizio chiamato'), ('rosso', 'messaggio all’USC'),
            ('giallo', 'stato dell’atto (YY = codice da assegnare)'),
            ('viola', 'passo sulla web app ANSC'), ('grigio', 'tratteggio: condizionato o da definire')]
    for k, (col, t) in enumerate(voci):
        xk, yk = 8.2 + (k % 2) * 3.7, yl + (k // 2) * 0.2
        riquadro(sl, xk, yk, 0.22, 0.12, col, [('', 6, False, None)], forma=MSO_SHAPE.RECTANGLE)
        testo(sl, xk + 0.28, yk - 0.015, 3.3, 0.15, t, 7.5)

    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


if __name__ == '__main__':
    print('scritto:', genera(sys.argv[1] if len(sys.argv) > 1 else OUT))
