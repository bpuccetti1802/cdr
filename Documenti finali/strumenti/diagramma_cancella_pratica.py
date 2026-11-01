# -*- coding: utf-8 -*-
"""Diagramma di flusso della cancellazione di una pratica da SIPO, con i riflessi su ANSC.

Fonte: il testo dell'utente del 30/10/2026 (ricerca → CANCELLA PRATICA → conferma →
verifiche su ANSC_STATO_ATTO → R011 → conclusione in SIPO). I rami che il testo non
descrive sono tratteggiati e marcati [DA VERIFICARE].

Uscita: img/cancella_pratica.png
"""
import os

from diagrammi_comune import (C, MUTED, box, fnt, F_ITA, F_BLD, legenda, percorso,
                              rombo, tela, avvolgi)

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'img', 'cancella_pratica.png')

W, H = 1700, 1900
CX = 700          # colonna principale
BW, BH = 440, 96  # riquadri


def nota(dr, x, y, w, testo, colore='giallo'):
    bordo, fondo = C[colore]
    f = fnt(F_ITA, 15)
    righe = avvolgi(dr, testo, f, w - 24)
    h = len(righe) * 20 + 20
    dr.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fondo, outline=bordo, width=2)
    yy = y + 10
    for r in righe:
        dr.text((x + 12, yy), r, font=f, fill='#5b4a1f')
        yy += 20
    return h


def tratteggiato(dr, x, y, w, h, colore, titolo, sotto):
    """Riquadro con bordo tratteggiato: passo non descritto dalla fonte."""
    box(dr, x, y, w, h, colore, titolo, sotto)
    bordo, _ = C[colore]
    # sovrascrive il bordo pieno con un tratteggio bianco a intervalli
    for xx in range(x + 14, x + w - 14, 22):
        dr.line([xx, y, xx + 10, y], fill='white', width=4)
        dr.line([xx, y + h, xx + 10, y + h], fill='white', width=4)
    for yy in range(y + 14, y + h - 14, 22):
        dr.line([x, yy, x, yy + 10], fill='white', width=4)
        dr.line([x + w, yy, x + w, yy + 10], fill='white', width=4)


def disegna():
    im, dr = tela(W, H, "Cancellazione di una pratica da SIPO e riflessi su ANSC",
                  "dalla ricerca alla conclusione in SIPO · R011 solo per atti non ancora "
                  "firmati dall’USC")

    # 1. Ricerca
    y = 110
    box(dr, CX - BW // 2, y, BW, BH, 'grigio', "Ricerca della pratica",
        "SIPO, funzione di ricerca · nessuna chiamata ad ANSC")
    percorso(dr, [(CX, y + BH), (CX, y + BH + 50)])

    # 2. CANCELLA PRATICA
    y += BH + 50
    box(dr, CX - BW // 2, y, BW, BH, 'blu', "Selezione e “CANCELLA PRATICA”",
        "l’operatore seleziona la pratica da rimuovere")
    percorso(dr, [(CX, y + BH), (CX, y + BH + 50)])

    # 3. Conferma
    y += BH + 50
    cy = y + 75
    rombo(dr, CX, cy, 360, 150, "Conferma?", ts=21)
    # annulla → fine
    percorso(dr, [(CX + 180, cy), (CX + 430, cy)], etichetta="ANNULLA", pos=(CX + 300, cy - 24))
    box(dr, CX + 430, cy - 45, 330, 90, 'grigio', "Nessuna modifica",
        "si torna alla ricerca")
    percorso(dr, [(CX, cy + 75), (CX, cy + 135)], etichetta="CONFERMA",
             pos=(CX + 52, cy + 90))

    # 4. Riga in ANSC_STATO_ATTO?
    y = cy + 135
    cy = y + 85
    rombo(dr, CX, cy, 470, 170, "Riga in ANSC_STATO_ATTO per l’atto?", ts=19)
    dr.text((CX + 60, cy + 100), "per ID_ATTO_SIPO = ID_ATTO", font=fnt(F_ITA, 14), fill=MUTED)
    # No → cancellazione SIPO tradizionale
    xs = 60
    percorso(dr, [(CX - 235, cy), (xs + 320, cy)], etichetta="NO", pos=((CX - 235 + xs + 320) / 2, cy - 24))
    box(dr, xs, cy - 60, 320, 120, 'verde', "Cancellazione in SIPO",
        "procedure attuali · nulla da fare su ANSC")
    percorso(dr, [(CX, cy + 85), (CX, cy + 165)], etichetta="SÌ", pos=(CX + 24, cy + 120))

    # 5. IdANSC valorizzato?
    y = cy + 165
    cy = y + 80
    rombo(dr, CX, cy, 420, 160, "ID_ANSC valorizzato?", ts=20)

    # 5a. No → stato annullato senza ANSC
    xa = 60
    percorso(dr, [(CX - 210, cy), (xa + 320, cy)], etichetta="NO", pos=((CX - 210 + xa + 320) / 2, cy - 24))
    box(dr, xa, cy - 70, 320, 140, 'blu', "Stato dell’atto a “9 ANNULLATO”",
        "solo su ANSC_STATO_ATTO · nessuna chiamata: l’atto in ANSC non esiste")

    ya_fondo = cy + 70

    # 5b. Sì → R011
    percorso(dr, [(CX, cy + 80), (CX, cy + 150)], etichetta="SÌ", pos=(CX + 24, cy + 100))
    y = cy + 150
    box(dr, CX - BW // 2, y, BW, 110, 'viola', "R011 /evento/elimina",
        "cancellazione logica in ANSC · richiede l’intero modello evento")
    nota(dr, CX + 250, y - 6, 420,
         "Vincolo ANSC: R011 non cancella un atto già firmato dall’USC. Il testo non "
         "dice dove si controlli lo stato prima della chiamata [DA VERIFICARE].")
    percorso(dr, [(CX, y + 110), (CX, y + 160)])

    # 6. Esito R011
    y += 160
    cy = y + 75
    rombo(dr, CX, cy, 360, 150, "Esito di R011?", ts=20)
    # KO
    xk = CX + 380
    percorso(dr, [(CX + 180, cy), (xk, cy)], etichetta="ERRORE", pos=(CX + 280, cy - 24))
    tratteggiato(dr, xk, cy - 75, 400, 150, 'rosso', "Cancellazione interrotta",
                 "la pratica resta in SIPO e si mostra l’errore ANSC [DA VERIFICARE: "
                 "il testo dice solo «fare attenzione al ritorno»]")
    # OK
    percorso(dr, [(CX, cy + 75), (CX, cy + 125)], etichetta="OK", pos=(CX + 24, cy + 88))
    y = cy + 125
    tratteggiato(dr, CX - BW // 2, y, BW, 96, 'blu', "Stato dell’atto aggiornato",
                 "su ANSC_STATO_ATTO, come dopo R011 [DA VERIFICARE: non descritto]")

    # 7. Conclusione in SIPO (confluenza)
    yc = y + 96 + 90
    percorso(dr, [(CX, y + 96), (CX, yc)])
    box(dr, CX - BW // 2, yc, BW, 100, 'verde', "Conclusione dell’operazione in SIPO",
        "cancellazione della pratica secondo le procedure attuali")
    # confluenza dal ramo «nessun ID_ANSC»
    percorso(dr, [(xa + 160, ya_fondo), (xa + 160, yc + 50),
                  (CX - BW // 2, yc + 50)])

    # Note in basso
    yn = yc + 135
    nota(dr, 80, yn, W - 160,
         "Stato: nella decodifica ANSC_11 il codice 9 è CANCELLATO e ANNULLATO è il 3. "
         "Il testo chiede “9 ANNULLATO”: va deciso quale coppia ID_STATO/STATO "
         "registrare [DA VERIFICARE].")
    legenda(dr, 80, H - 50, [('grigio', "SIPO, nessun effetto"), ('blu', "SIPO / ANSC_STATO_ATTO"),
                            ('viola', "chiamata ad ANSC"), ('verde', "esito"),
                            ('rosso', "errore"), ('giallo', "decisione o nota")])
    im.save(OUT)
    print(OUT)


if __name__ == '__main__':
    disegna()
