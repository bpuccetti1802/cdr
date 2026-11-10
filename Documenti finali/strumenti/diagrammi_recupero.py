# -*- coding: utf-8 -*-
"""Figure dell'analisi «Recupero in SIPO degli atti formati sulla web app ANSC» (v0.1,
10/11/2026).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_recupero.py

`img/recupero/livelli.png`: i quattro livelli di presenza dell'atto in SIPO, che cosa scrive
ciascuno e che cosa rende possibile.
`img/recupero/dopo.png`: che cosa succede dopo la firma sulla web app, per ciascun effetto.
Le stringhe visualizzate usano il doppio apice (vedi diagrammi_comune).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import (C, INK, MUTED, F_BLD, F_REG, F_ITA, fnt, box, pila,  # noqa
                              percorso, freccia, banda, legenda, tela, centra)

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'recupero')

LIVELLI = [
    ('grigio', "L0 · Il numero", "DATI_ATTO_ESTERNO: numero Utilizzato, idAnsc collegato",
     "si sa che il numero è stato usato e da quale atto ANSC"),
    ('blu', "L1 · Il riferimento", "+ ANSC_STATO_ATTO (canale WEBAPP, stato, modello evento) "
     "+ ANAG_USR.ATTO con le colonne ANSC",
     "ricerca per idAnsc o numero · certificazione da ANSC · ANPR riceve l’atto in forma ANSC"),
    ('verde', "L2 · La scheda essenziale", "+ MATR_USR.ATTO e tabella d’area, intestatari, "
     "testo dell’atto, PDF se ottenibile",
     "ricerche e dettaglio di SIPO · sportello · annotazioni di SIPO · statistiche"),
    ('rosso', "L3 · L’importazione completa", "+ tutte le tabelle d’area dal modello evento, "
     "con la mappatura inversa",
     "SIPO come se l’atto l’avesse formato lui: costo alto, e la mappatura inversa non è "
     "univoca"),
]


def livelli(out=os.path.join(IMG, 'livelli.png')):
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 900
    im, dr = tela(W, H, "Quanto deve esistere in SIPO un atto formato sulla web app",
                  "Quattro livelli cumulativi: ciascuno scrive di più e rende possibile di più")
    x0, y0, alt, sc = 80, 120, 150, 40
    for i, (col, tit, scrive, abilita) in enumerate(LIVELLI):
        x = x0 + i * 60
        y = y0 + (len(LIVELLI) - 1 - i) * (alt + sc) - 0
        w = 1700 - i * 60 - (len(LIVELLI) - 1 - i) * 0
        bordo, fondo = C[col]
        dr.rounded_rectangle([x, y, x + 1100, y + alt], radius=14, fill=fondo, outline=bordo,
                             width=3)
        dr.text((x + 24, y + 18), tit, font=fnt(F_BLD, 24), fill=INK)
        dr.text((x + 24, y + 62), scrive, font=fnt(F_REG, 17), fill=MUTED)
        dr.text((x + 24, y + 100), "→ " + abilita, font=fnt(F_ITA, 17), fill=bordo)
    # freccia del costo
    percorso(dr, [(1700, 720), (1700, 140)], C['rosso'][0], larg=4)
    centra(dr, "costo e", fnt(F_BLD, 18), 1700, 740, C['rosso'][0])
    centra(dr, "dipendenza", fnt(F_BLD, 18), 1700, 762, C['rosso'][0])
    centra(dr, "dalla mappatura", fnt(F_BLD, 18), 1700, 784, C['rosso'][0])
    centra(dr, "Proposta: L1 subito per tutti gli atti, L2 come regola, L3 solo per i casi "
               "d’uso ordinari che lo giustificano.", fnt(F_ITA, 17), W / 2, 850, MUTED)
    im.save(out)
    return out


def dopo(out=os.path.join(IMG, 'dopo.png')):
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1000
    im, dr = tela(W, H, "Che cosa succede dopo la firma sulla web app",
                  "Per ciascun effetto: chi lo produce, e che cosa deve fare o non fare SIPO")
    box(dr, 700, 100, 500, 90, 'blu', "Atto firmato sulla web app",
        "stato 5 FIRMATO DA USC, numero comunale staccato in SIPO", ts=20, ss=15)
    righe = [
        ("Anagrafe e ANPR", "ANSC predispone la comunicazione anagrafica e la notifica "
         "all’anagrafe tramite ANPR", "SIPO non chiama all-anpr-sipo: si eviterebbe il doppio "
         "aggiornamento"),
        ("Annotazioni sugli atti collegati", "ANSC, con le notifiche agli altri comuni "
         "(non per i casi d’uso di servizio)", "SIPO non le rigenera; le legge con R005"),
        ("Comunicazioni agli enti", "ANSC le predispone; si scaricano con R003",
         "il back-office le rende visibili"),
        ("PDF dell’atto", "ANSC: R010 rinviando il modello evento, o estratto con firma",
         "SIPO conserva il PDF solo se ottenibile senza firma"),
        ("Certificati ed estratti", "ANSC (R002, R019)", "instradamento per atto: da ANSC"),
        ("Modifiche successive", "Web app: nota tecnica, rettifiche, annullamento",
         "SIPO le scopre solo rileggendo con R005: riallineamento su richiesta"),
    ]
    y = 230
    for tema, chi, sipo in righe:
        box(dr, 60, y, 380, 100, 'grigio', tema, None, ts=18)
        box(dr, 470, y, 650, 100, 'blu', "Chi lo produce", chi, ts=15, ss=14)
        box(dr, 1150, y, 690, 100, 'verde', "Che cosa fa SIPO", sipo, ts=15, ss=14)
        y += 118
    legenda(dr, 60, 950, [('grigio', "effetto"), ('blu', "ANSC"), ('verde', "SIPO")])
    im.save(out)
    return out


if __name__ == '__main__':
    print(livelli())
    print(dopo())
