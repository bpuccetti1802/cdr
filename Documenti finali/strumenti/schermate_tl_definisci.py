# -*- coding: utf-8 -*-
"""Le due schermate del passo «DEFINISCI» per gli atti a testo libero (12/11/2026, decisione
dell'utente).

Il cambiamento: nell'Anteprima, dopo COPIA TESTO, compare **DEFINISCI**. Il bottone apre una
**modale** di aggancio all'atto ANSC — criteri già noti (numero comunale, data, comune, tipo
evento), candidati proposti con quello coincidente preselezionato, in alternativa l'inserimento
diretto dell'identificativo ANSC. Confermando, **l'atto è terminato e si esce**: percorso di
salvataggio ordinario di SIPO (stato 2 DEFINITO) e `ANSC_STATO_ATTO` con `ID_ANSC`.

⚠️ `DEFINISCI` non è un passo speciale: è la chiusura ordinaria di SIPO. La sola condizione
in più è conoscere l'atto ANSC che si sta chiudendo. Ed è **lo stato sullo store** ad
abilitarlo, non il clic nella sessione del browser: l'operatore esce da SIPO, forma l'atto sulla
WebApp e rientra dopo minuti, magari riaprendo la pagina.

Le schermate del «Recupero Atto ANSC» (tl_3…tl_6) **restano**: servono agli atti nati
interamente sulla WebApp, che in SIPO non hanno mai avuto una bozza né un numero staccato.

  · tl_2_anteprima_numero.png   — rifatta: la barra dei bottoni diventa a tre
  · tl_2b_definisci_modale.png  — nuova: la modale di aggancio

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_tl_definisci.py
"""
import os

from PIL import Image, ImageDraw

import schermate_testo_libero as S
from schermate_testo_libero import (BIANCO, BORDO, GRIGIO, NERO, ROSSO, SPENTO_TESTO,
                                    bottone, font, pastiglia)

OUT = S.OUT
BLU = S.BLU
SELEZIONE = (255, 248, 225)        # la riga preselezionata, come il pannello del numero
INTESTA = (245, 246, 248)

ID_ANSC = '2026-0000731-124-058091'
CANDIDATI = [
    # (idAnsc, numero comunale, data e ora, intestatario, stato)
    (ID_ANSC, '124', '07/11/2026 15:42', 'GODI FILIPPO', '5 — FIRMATO DA USC'),
    ('2026-0000730-123-058091', '123', '07/11/2026 11:08', 'RUSSO ANNA', '5 — FIRMATO DA USC'),
    ('2026-0000729-122-058091', '122', '07/11/2026 09:51', 'CONTI MARIO', '5 — FIRMATO DA USC'),
]


# ------------------------------------------------------------------ primitive
def pastiglia2(dr, xy, testo, r=19):
    """Come S.pastiglia ma con il corpo adattato: «5b» a 24pt sbordava dal cerchio."""
    x, y = xy
    dr.ellipse((x - r, y - r, x + r, y + r), fill=S.GIALLO, outline=NERO, width=2)
    dr.text((x, y), testo, font=font(24 if len(testo) < 2 else 19, True), fill=NERO, anchor='mm')


def radio(dr, x, y, scelto):
    dr.ellipse((x - 11, y - 11, x + 11, y + 11), outline=BLU if scelto else GRIGIO, width=2)
    if scelto:
        dr.ellipse((x - 5, y - 5, x + 5, y + 5), fill=BLU)


def campo_testo(dr, box, segnaposto, testo=''):
    dr.rectangle(box, fill=BIANCO, outline=BORDO, width=2)
    dr.text((box[0] + 14, (box[1] + box[3]) / 2), testo or segnaposto, font=font(21),
            fill=NERO if testo else (170, 172, 176), anchor='lm')


# =========================================================== 1) l'Anteprima a tre bottoni
def anteprima_con_definisci():
    """Ridisegna la barra in fondo: INDIETRO · COPIA TESTO · DEFINISCI (inibito)."""
    im = S.anteprima()
    dr = ImageDraw.Draw(im)
    yb = im.height - 68

    # si ripulisce la zona dei bottoni di destra e si ricompone a tre
    dr.rectangle((1000, yb - 40, im.width, yb + 56), fill=BIANCO)
    # ⚠️ la pulizia cancella il bordo del riquadro dell'atto: va ricucito
    bordo_y = im.height - 96
    dr.line((1000, bordo_y, 1825, bordo_y), fill=ROSSO, width=3)
    dr.line((1824, bordo_y - 40, 1824, bordo_y), fill=ROSSO, width=3)

    dr.text((1375, yb + 24), 'copia negli appunti il testo dell’atto',
            font=font(19), fill=GRIGIO, anchor='rm')
    bottone(dr, (1395, yb, 1560, yb + 48), 'COPIA TESTO')
    pastiglia(dr, (1395, yb), 5)

    bottone(dr, (1640, yb, 1825, yb + 48), 'DEFINISCI', attivo=False)
    pastiglia2(dr, (1640, yb), '5b')
    dr.text((1825, yb - 16), 'si abilita quando l’atto è stato formato sulla WebApp',
            font=font(18), fill=GRIGIO, anchor='rm')
    return im


# =========================================================== 2) la modale di aggancio
def modale():
    base = anteprima_con_definisci()
    # il DEFINISCI della pagina sotto è ormai attivo: è stato premuto
    dr = ImageDraw.Draw(base)
    dr.rectangle((1400, base.height - 112, base.width, base.height - 80), fill=BIANCO)
    bottone(dr, (1640, base.height - 68, 1825, base.height - 20), 'DEFINISCI')

    # velo sulla pagina
    velo = Image.new('RGB', base.size, (0, 0, 0))
    im = Image.blend(base, velo, 0.55)
    dr = ImageDraw.Draw(im)

    x0, x1 = 230, im.width - 230
    y0 = 150
    y1 = y0 + 730        # altezza calcolata sul contenuto, non sulla pagina
    dr.rectangle((x0, y0, x1, y1), fill=BIANCO, outline=ROSSO, width=3)

    # testata
    dr.rectangle((x0, y0, x1, y0 + 66), fill=ROSSO)
    dr.text((x0 + 26, y0 + 33), 'DEFINISCI L’ATTO — aggancio all’atto formato su ANSC',
            font=font(26, True), fill=BIANCO, anchor='lm')
    dr.text((x1 - 26, y0 + 33), '×', font=font(34, True), fill=BIANCO, anchor='rm')

    y = y0 + 100
    dr.text((x0 + 26, y), 'Criteri di ricerca, già noti a SIPO', font=font(23, True),
            fill=NERO, anchor='lm')
    y += 40
    dr.rectangle((x0 + 26, y, x1 - 26, y + 60), fill=INTESTA, outline=BORDO, width=1)
    cx = x0 + 48
    for etichetta, valore in (('Data', '07/11/2026'), ('Comune', 'ROMA (RM)'),
                              ('Tipo evento', 'MORTE'), ('N. comunale atteso', '124 / 2026')):
        cx = S.campo(dr, cx, y + 30, etichetta, valore, dim=21) + 60
    y += 92

    # ── i candidati
    dr.text((x0 + 26, y), 'Atti formati oggi sulla WebApp e non ancora agganciati',
            font=font(23, True), fill=NERO, anchor='lm')
    dr.text((x1 - 26, y), '%d trovati' % len(CANDIDATI), font=font(20), fill=GRIGIO, anchor='rm')
    y += 30

    col = (x0 + 70, x0 + 500, x0 + 650, x0 + 900)
    dr.rectangle((x0 + 26, y, x1 - 26, y + 42), fill=INTESTA, outline=BORDO, width=1)
    for cx, testa in zip(col, ('IDENTIFICATIVO ANSC', 'N. COM.', 'DATA E ORA',
                               'INTESTATARIO')):
        dr.text((cx, y + 21), testa, font=font(19, True), fill=GRIGIO, anchor='lm')
    y += 42
    for i, (ida, num, quando, chi, stato) in enumerate(CANDIDATI):
        alt = 52
        scelto = i == 0
        dr.rectangle((x0 + 26, y, x1 - 26, y + alt),
                     fill=SELEZIONE if scelto else BIANCO, outline=BORDO, width=1)
        if scelto:
            dr.rectangle((x0 + 26, y, x0 + 32, y + alt), fill=ROSSO)
        radio(dr, x0 + 48, y + alt / 2, scelto)
        for cx, val, grassetto in zip(col, (ida, num, quando, chi),
                                      (True, True, False, False)):
            dr.text((cx, y + alt / 2), val, font=font(21, grassetto),
                    fill=NERO if grassetto else (70, 74, 78), anchor='lm')
        if scelto:
            et = 'numero comunale coincidente'
            w = dr.textlength(et, font=font(18, True))
            dr.rounded_rectangle((x1 - 60 - w, y + 12, x1 - 44, y + alt - 12), radius=10,
                                 fill=SELEZIONE, outline=ROSSO, width=1)
            dr.text((x1 - 52, y + alt / 2), et, font=font(18, True), fill=ROSSO, anchor='rm')
        y += alt
    dr.text((x0 + 26, y + 20), 'Sono elencati i soli atti in stato 5 \u2014 FIRMATO DA USC: '
            'un atto validato ma non ancora firmato non si aggancia.',
            font=font(19), fill=GRIGIO, anchor='lm')
    y += 48

    # ── l'inserimento diretto
    dr.line((x0 + 26, y, x1 - 26, y), fill=BORDO, width=1)
    y += 26
    dr.text((x0 + 26, y + 22), 'Oppure indica l’identificativo ANSC, se annotato:',
            font=font(22), fill=NERO, anchor='lm')
    campo_testo(dr, (x0 + 560, y, x0 + 1060, y + 44), '2026-0000000-000-000000')
    dr.text((x0 + 1080, y + 22), 'VERIFICA', font=font(21, True), fill=BLU, anchor='lm')
    y += 62
    domanda = 'Non compare fra i candidati?  '
    rimando = 'Ricerca estesa per intestatario o per data'
    f21 = font(21)
    dr.text((x0 + 26, y + 18), domanda, font=f21, fill=NERO, anchor='lm')
    xr = x0 + 26 + dr.textlength(domanda, font=f21)
    dr.text((xr, y + 18), rimando, font=f21, fill=BLU, anchor='lm')
    dr.line((xr, y + 32, xr + dr.textlength(rimando, font=f21), y + 32), fill=BLU, width=1)

    # ── piede
    yb = y1 - 76
    dr.line((x0, yb - 18, x1, yb - 18), fill=BORDO, width=1)
    dr.rectangle((x0 + 26, yb, x0 + 176, yb + 48), fill=BIANCO, outline=(190, 192, 196), width=2)
    dr.text((x0 + 101, yb + 24), 'ANNULLA', font=font(17, True), fill=SPENTO_TESTO, anchor='mm')
    bottone(dr, (x1 - 316, yb, x1 - 26, yb + 48), 'DEFINISCI L’ATTO')
    pastiglia(dr, (x1 - 316, yb), 6)
    dr.text((x1 - 336, yb + 24), 'l’atto è concluso: SIPO salva e si esce',
            font=font(19), fill=GRIGIO, anchor='rm')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for nome, im in (('tl_2_anteprima_numero.png', anteprima_con_definisci()),
                     ('tl_2b_definisci_modale.png', modale())):
        im.save(os.path.join(OUT, nome))
        print(nome, im.size)
