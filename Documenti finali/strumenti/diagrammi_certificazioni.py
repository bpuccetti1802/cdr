# -*- coding: utf-8 -*-
"""Figure dell'analisi sulle certificazioni di stato civile SIPO-ANSC (v0.1, 10/11/2026).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_certificazioni.py

`img/certificazioni/instradamento.png`: dalla richiesta allo sportello al documento, con la
scelta fra il formulario di SIPO e i servizi ANSC secondo l'atto.
Le stringhe visualizzate usano il doppio apice (vedi diagrammi_comune).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import (C, INK, MUTED, ARROW, F_BLD, F_REG, F_ITA, fnt, box,  # noqa
                              pila, rombo, percorso, freccia, banda, legenda, tela, centra)

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'certificazioni')


def instradamento(out=os.path.join(IMG, 'instradamento.png')):
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1180
    im, dr = tela(W, H, "Da dove esce il documento: l’instradamento per atto",
                  "La richiesta nasce sempre allo sportello di stato civile in SIPO; "
                  "la fonte del documento dipende dall’atto")

    # 1 richiesta
    box(dr, 700, 100, 500, 100, 'grigio', "Lo sportello di stato civile in SIPO",
        "l’operatore sceglie l’atto e il documento", ts=20, ss=15)
    # 2 controlli comuni
    box(dr, 700, 240, 500, 100, 'grigio', "Controlli preliminari in SIPO",
        "blocco della certificazione per il soggetto · stato dell’atto", ts=20, ss=15)
    freccia(dr, (950, 200), (950, 235))
    # 3 decisione
    rombo(dr, 950, 450, 470, 170, "L’atto ha un identificativo ANSC?", ts=20)
    freccia(dr, (950, 340), (950, 362))

    # ramo NO: SIPO
    percorso(dr, [(715, 450), (360, 450), (360, 540)])
    centra(dr, "no — atto del registro tradizionale", fnt(F_BLD, 15), 520, 420, INK)
    pila(dr, 130, 545, 460, 180, 'grigio',
         ["Formulario di SIPO"],
         ["PKG_ESTRATTI, modelli Jasper", "estratti ESN · ESM · ESU · ESD",
          "plurilingue 884 · 851 · 872/874", "copia conforme dell’atto"],
         ["come oggi"])
    box(dr, 130, 770, 460, 110, 'grigio', "PDF da stampare e firmare a mano",
        "nessun sigillo, nessun QR", ts=19, ss=15)
    freccia(dr, (360, 725), (360, 765))

    # ramo SI: ANSC
    percorso(dr, [(1185, 450), (1500, 450), (1500, 500)])
    centra(dr, "sì — l’originale è in ANSC", fnt(F_BLD, 15), 1340, 420, INK)
    rombo(dr, 1500, 580, 420, 150, "Quale documento?", ts=19)

    xs = [1090, 1500, 1800]
    # tre esiti
    percorso(dr, [(1290, 580), (1090, 580), (1090, 680)])
    percorso(dr, [(1500, 655), (1500, 680)])

    percorso(dr, [(1710, 580), (1800, 580), (1800, 680)])
    pila(dr, 950, 685, 280, 200, 'blu',
         ["Certificato semplice"],
         ["R002 /certificato-semplice", "sigillo del Ministero", "QR di verifica, 6 mesi",
          "nessuna firma dell’USC"],
         ["anche profilo SCCSE"])
    pila(dr, 1250, 685, 390, 200, 'rosso',
         ["Estratto per riassunto", "o per copia integrale"],
         ["R002 /certificato, tipo 2 o 3", "firma remota dell’USC:",
          "utente, password e OTP di firma"],
         ["solo l’ufficiale"])
    pila(dr, 1665, 685, 215, 200, 'viola',
         ["Plurilingue"],
         ["R019", "sigle → annotazioni", "→ anteprima", "→ emissione"],
         ["Vienna"])

    # concentratore
    pila(dr, 950, 930, 930, 110, 'giallo',
         ["Concentratore all-ansc-sipo"],
         ["sessione OTP e token verso ANSC · restituisce il PDF/A in base64 con "
          "l’identificativo del certificato e la data di validità"])
    for x in (1090, 1445, 1772):
        freccia(dr, (x, 885), (x, 925))

    # registro comune
    box(dr, 130, 930, 760, 110, 'verde', "Registro delle emissioni in SIPO",
        "ESTRATTI_DOWNLOAD_LOG come oggi · ANSC_CERTIFICATO per le emissioni ANSC",
        ts=19, ss=15)
    percorso(dr, [(360, 880), (360, 925)])
    percorso(dr, [(950, 985), (895, 985)])

    legenda(dr, 130, 1080, [('grigio', "SIPO, come oggi"), ('blu', "senza firma dell’USC"),
                            ('rosso', "con firma remota dell’USC"),
                            ('viola', "plurilingue"), ('giallo', "concentratore"),
                            ('verde', "registro")])
    centra(dr, "Bollo, diritti ed esenzioni restano fuori da ANSC, come nel percorso di "
               "stato civile di oggi.", fnt(F_ITA, 15), W / 2, 1130, MUTED)
    im.save(out)
    return out


if __name__ == '__main__':
    print(instradamento())
