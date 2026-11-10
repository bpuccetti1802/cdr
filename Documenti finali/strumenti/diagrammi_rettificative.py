# -*- coding: utf-8 -*-
"""Figura del capitolo «Le annotazioni rettificative» (ANALISI_Annullamento-Cancellazione-
Rettifiche v0.3, 10/11/2026): l'annotazione per errore materiale formata da SIPO (fase 2).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_rettificative.py

Tre corsie (SIPO · servizi del Comune · ANSC), nove passi numerati, gli effetti in fondo.
Le stringhe visualizzate usano il doppio apice (vedi diagrammi_comune).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import (C, INK, MUTED, F_BLD, F_REG, F_ITA, fnt, box, percorso,  # noqa
                              banda, legenda, tela, centra)

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'annullamento')

CORSIE = {'sipo': (130, 330, 'grigio', "SIPO"),
          'servizi': (350, 520, 'giallo', "Servizi del Comune"),
          'ansc': (540, 740, 'blu', "ANSC (attraverso all-ansc-sipo)")}

PASSI = [
    ('sipo', "Dettaglio dell’atto", "atto con identificativo ANSC, stato 5: «ANNOTAZIONE PER "
     "ERRORE MATERIALE»"),
    ('ansc', "R005", "legge l’atto completo per idAnsc: è la base dell’atto corretto"),
    ('sipo', "Pagina comune", "i cinque registri hanno lo stesso mapping: si modificano i dati "
     "anagrafici"),
    ('sipo', "Dalla differenza", "il testo con la formula 888 e l’atto corretto, dagli stessi "
     "dati"),
    ('servizi', "Numero comunale", "be-numeratore-comunale: l’annotazione ha un numero proprio"),
    ('ansc', "R013", "/rettifica/validazione: evento ed eventoModificato"),
    ('ansc', "R007", "firma dell’ufficiale; attestazione se richiesta"),
    ('ansc', "R005", "verifica dell’annotazione e dell’atto corretto"),
    ('sipo', "Aggiornamento", "dati dell’atto, registro dell’annotazione, numero utilizzato"),
]


def errore_materiale(out=os.path.join(IMG, 'errore_materiale_flusso.png')):
    os.makedirs(IMG, exist_ok=True)
    W, H = 2000, 960
    im, dr = tela(W, H, "L’annotazione per errore materiale formata da SIPO",
                  "Fase 2 della proposta: nove passi, tre corsie; nella fase 1 i passi 3, 4, 6 e 7 si "
                  "fanno sulla web app")
    for y1, y2, col, nome in CORSIE.values():
        banda(dr, 30, y1, W - 30, y2, C[col][0], nome, C[col][0], ts=17)

    x0, larg, passo = 60, 192, 210
    riq = []
    for i, (corsia, titolo, sotto) in enumerate(PASSI):
        y1, y2, col, _ = CORSIE[corsia]
        x = x0 + i * passo
        y = y1 + 42
        h = (y2 - y1) - 58
        box(dr, x, y, larg, h, col, "%d · %s" % (i + 1, titolo), sotto, ts=17, ss=13)
        riq.append((x, y, x + larg, y + h))

    for a, b in zip(riq, riq[1:]):
        ya = (a[1] + a[3]) / 2
        yb = (b[1] + b[3]) / 2
        xm = (a[2] + b[0]) / 2
        if abs(ya - yb) < 2:
            percorso(dr, [(a[2], ya), (b[0], yb)])
        else:
            percorso(dr, [(a[2], ya), (xm, ya), (xm, yb), (b[0], yb)])

    # effetti
    yE = 770
    centra(dr, "Gli effetti in ANSC", fnt(F_BLD, 18), W / 2, yE, INK)
    effetti = ["certificati ed estratti per riassunto con i dati corretti",
               "copia integrale con l’annotazione a margine",
               "notifica al comune dell’atto principale e al comune di residenza",
               "da qui in poi la nota tecnica non è più possibile"]
    xs = [60, 540, 1020, 1500]
    for x, t in zip(xs, effetti):
        box(dr, x, yE + 34, 440, 66, 'verde', t, None, ts=15)

    legenda(dr, 60, 920, [('grigio', "SIPO"), ('giallo', "servizi del Comune"),
                          ('blu', "ANSC"), ('verde', "effetti")])
    im.save(out)
    return out


if __name__ == '__main__':
    print(errore_materiale())
