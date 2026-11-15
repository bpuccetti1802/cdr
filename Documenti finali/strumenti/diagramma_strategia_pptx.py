# -*- coding: utf-8 -*-
"""La strategia adottata per gli atti che SIPO non gestisce in automatico (13/11/2026, v0.7
dell'analisi sugli atti a testo libero, cap. 4), su una pagina PowerPoint con forme e connettori
nativi, modificabile dall'utente come le due gestioni della v0.2.

È la sintesi delle due gestioni dell'analisi di integrazione:
  · dalla Gestione 1 — l'atto si compila in SIPO, che ne compone il testo;
  · dalla Gestione 2 — il numero comunale lo stacca SIPO prima di andare sulla WebApp;
  · nuovo — al ritorno non si importano i dati: DEFINISCI aggancia l'atto ANSC e definisce l'atto
    SIPO con un passaggio solo.

Le corsie sono quelle della v0.2 (SIPO · stato · WebApp), con la funzione pannello() di
diagramma_testo_libero_pptx.py. Esce come DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.3.pptx: la v0.2,
con le due gestioni, resta com'è.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagramma_strategia_pptx.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagramma_testo_libero_pptx import ROSSO, pannello              # noqa: E402
from diagramma_workflow_pptx import INK, MUTED, rgb, riquadro, testo  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(QUI), 'DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.3.pptx')
W = 8.2

MSG = '«Non è stato identificato uno Usecase ANSC. Passare alla WebApp per formare un atto a ' \
      'testo libero e rientrare in SIPO per completare le operazioni.»'

PASSI = [
    ('S', 'blu', [('Stesura dell’atto in SIPO', 8.5, True, None),
                  ('fino al Riepilogo; per un tipo atto a testo libero, nella pagina del testo '
                   'libero', 7, False, MUTED)], 0.5, 'R005 · intestatario', False),
    ('D', 'bianco', [('Riepilogo:', 7, True, None),
                     ('esiste un UC per l’atto?', 7, True, None)], 0.62, None, False),
    ('S', 'rosso', [('Messaggio del sistema', 8, True, ROSSO), (MSG, 6.5, False, INK),
                    ('CONFERMA inibito', 6.5, False, MUTED)], 0.72, None, False),
    ('S', 'blu', [('DATI PER ANSC', 8.5, True, None),
                  ('stacco del numero comunale', 7, False, MUTED)], 0.44,
     'be-numeratore-comunale · POST /richiesta', False),
    ('S', 'blu', [('Anteprima', 8.5, True, None),
                  ('numero comunale in alto · COPIA TESTO', 7, False, MUTED)], 0.44, None, False),
    ('T', 'giallo', [('WA · ATTESA WEBAPP', 8, True, None),
                     ('atto SIPO: 1 IN LAVORAZIONE', 6.5, False, MUTED)], 0.5, None, False),
    ('A', 'viola', [('Stesura e firme sulla WebApp', 8.5, True, None),
                    ('UC di servizio · numero comunale · testo incollato · intestatari', 7, False,
                     MUTED)], 0.62, None, False),
    ('T', 'giallo', [('5 FIRMATO DA USC', 8, True, None),
                     ('in ANSC', 6.5, False, MUTED)], 0.44, None, False),
    ('S', 'blu', [('DEFINISCI', 8.5, True, None),
                  ('abilitato dallo stato WA · finestra di aggancio, preselezione sul numero '
                   'comunale', 7, False, MUTED)], 0.56, 'R005 · consultazione dell’atto', False),
    ('S', 'verde', [('Atto definito in SIPO', 8.5, True, None),
                    ('2 DEFINITO · store: ID_ANSC e 5 FIRMATO DA USC · numero Utilizzato', 7,
                     False, INK)], 0.56, 'be-numeratore-comunale · PUT /utilizza', False),
]


def genera(percorso=OUT):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(9.0)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = rgb('ffffff')

    testo(sl, 0.3, 0.18, W - 0.6, 0.35, 'Gli atti che SIPO non gestisce in automatico: la '
          'strategia adottata', 13, True, '1f3a5f', PP_ALIGN.CENTER)
    testo(sl, 0.3, 0.5, W - 0.6, 0.25, 'Sintesi delle due gestioni: compilazione e numero in '
          'SIPO, stesura sulla WebApp, aggancio al rientro', 8.5, False, MUTED, PP_ALIGN.CENTER,
          corsivo=True)
    ytot = pannello(sl, 0.3, 'Dichiarazioni e trascrizioni senza UC, o a testo libero',
                    'L’atto si compila in SIPO; si forma sulla WebApp con il caso d’uso di '
                    'servizio; SIPO lo definisce con DEFINISCI', PASSI)

    yl = ytot + 0.3
    voci = [('blu', 'passo in SIPO'), ('bianco', 'servizio chiamato'),
            ('rosso', 'messaggio all’USC'), ('giallo', 'stato dell’atto'),
            ('viola', 'passo sulla WebApp ANSC'), ('verde', 'esito')]
    for k, (col, t) in enumerate(voci):
        xk, yk = 0.4 + (k % 3) * 2.5, yl + (k // 3) * 0.2
        riquadro(sl, xk, yk, 0.22, 0.12, col, [('', 6, False, None)], forma=MSO_SHAPE.RECTANGLE)
        testo(sl, xk + 0.28, yk - 0.015, 2.1, 0.15, t, 7.5)
    prs.slide_height = Inches(yl + 0.55)

    prs.save(percorso)
    return percorso


if __name__ == '__main__':
    print('scritto:', genera(sys.argv[1] if len(sys.argv) > 1 else OUT))
