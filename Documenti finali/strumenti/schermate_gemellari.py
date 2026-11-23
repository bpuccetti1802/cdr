# -*- coding: utf-8 -*-
"""Ipotesi di schermata, nello stile di SIPO, del passo PRENOTA GEMELLI (analisi delle nascite
gemellari, v0.2, 19/11/2026).

Due immagini, con le primitive di `schermate_sipo_wf`:
  * gem_prenota_conferma.png — il riepilogo del gemello 1 dopo la divisione: l'elenco dei gemelli
    ancora senza numero e senza identificativo, PRENOTA GEMELLI attivo, VALIDA inibito, e la
    finestra di conferma;
  * gem_prenota_esito.png    — lo stesso elenco dopo la prenotazione: per ciascun gemello numero
    comunale, identificativo nazionale e stato ANSC 1 BOZZA (una riga di ANSC_STATO_ATTO ciascuno).
Nomi e codici sono di esempio; nessun dato di persone reali.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_gemellari.py
"""
import os

from PIL import Image, ImageDraw

import schermate_sipo_wf as S

DIR = os.path.join(S.IMG, 'gemellari')
COLS = ("Pos.", "Nato", "Stato del nato", "Caso d’uso ANSC (UC)", "N. comunale",
        "Identificativo nazionale", "Stato ANSC")
LARG = (50, 210, 130, 280, 110, 330, 180)
NATI = (("1", "NATO 1 — COGNOME NOME", "Nato vivo", "11111000 – Dic_Nasc_001"),
        ("2", "NATO 2 — COGNOME NOME", "Nato vivo", "11111000 – Dic_Nasc_001"))


def _testata(dr, y):
    y = S.pannello(dr, y, "Atto di nascita – parto plurimo", 112)
    larg = S.W - 2 * S.M - 24
    x = S.M + 12
    for quota, et, val in ((0.24, "Tipo atto", "1429 – gemelli in costanza di matrimonio"),
                           (0.16, "Numero gemelli", "2"), (0.20, "Atto in visione", "gemello 1 di 2"),
                           (0.20, "Stato SIPO", "1 IN LAVORAZIONE"),
                           (0.20, "Sessione ANSC", "OTP valido · 3 h 12 min")):
        w = int(larg * quota) - 12
        S.campo(dr, x, y, w, et, val, 'lettura')
        x += w + 12
    return y + 78


def _elenco(dr, y, prenotati):
    y = S.pannello(dr, y, "Gemelli della pratica – prenotazione degli atti in ANSC", 60 + 34 * 3)
    righe = []
    for pos, nome, stato, uc in NATI:
        if prenotati:
            num = str(13616 + int(pos))
            righe.append((pos, nome, stato, uc, num, "2026-%d-%s-058091" % (10527618 + int(pos), num),
                          "1 BOZZA"))
        else:
            righe.append((pos, nome, stato, uc, "—", "—", "da prenotare"))
    return S.tabella(dr, y, COLS, LARG, righe, x=S.M + 12) + 6


def conferma(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Riepilogo")
    y = _testata(dr, y)
    y = S.avviso(dr, y, "La pratica è stata divisa in 2 atti, uno per ciascun nato. Prima di "
                 "procedere all’anteprima e alla validazione gli atti dei gemelli vanno prenotati "
                 "in ANSC: la prenotazione stacca i numeri comunali e restituisce gli identificativi "
                 "nazionali, che ciascun atto riporta per i fratelli.", 'attenzione')
    y = _elenco(dr, y, False)
    y = S.pulsantiera(dr, y + 8, [("INDIETRO", True)],
                      [("PRENOTA GEMELLI", True), ("ANTEPRIMA", False), ("VALIDA", False)])
    fondo = y + 40
    im = im.crop((0, 0, S.W, fondo))
    # velo e finestra di conferma
    velo = Image.new('RGBA', im.size, (0, 0, 0, 90))
    im = Image.alpha_composite(im.convert('RGBA'), velo).convert('RGB')
    dr = ImageDraw.Draw(im)
    w, h = 640, 220
    x0, y0 = (S.W - w) // 2, 330
    dr.rectangle([x0, y0, x0 + w, y0 + h], fill='white', outline=S.BORDO)
    dr.rectangle([x0, y0, x0 + w, y0 + 44], fill=S.ROSSO)
    dr.text((x0 + 18, y0 + 11), "Prenotazione degli atti dei gemelli", font=S.f(S.N_BLD, 18),
            fill='white')
    corpo = ("Saranno staccati 2 numeri comunali consecutivi e prenotati in ANSC 2 atti, uno per "
             "ciascun gemello, con il caso d’uso indicato nell’elenco. Dopo la prenotazione il "
             "numero dei gemelli non si potrà più modificare e un atto non usato andrà cancellato. "
             "Confermi?")
    fr = S.f(S.N_REG, 15)
    for i, r in enumerate(S.avvolgi(dr, corpo, fr, w - 40)):
        dr.text((x0 + 20, y0 + 64 + i * 22), r, font=fr, fill=S.INK)
    S.bottoni_dx(dr, y0 + h - 50, [("ANNULLA", True), ("CONFERMA", True)], x_fine=x0 + w - 20)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest)
    return dest


def esito(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Riepilogo")
    bordo, fondo = S.AVVISI['ok']
    testo = ("Prenotazione effettuata: ANSC ha predisposto 2 atti in bozza. Numeri comunali 13617 "
             "e 13618 staccati da be-numeratore-comunale; gli identificativi nazionali sono "
             "registrati sugli atti dei gemelli.")
    y = S.avviso(dr, y, testo, 'ok')
    y = _testata(dr, y)
    y = _elenco(dr, y, True)
    y = S.avviso(dr, y, "Ogni gemello prosegue sul proprio atto: documenti, anteprima, "
                 "validazione e firme. GEMELLO SUCCESSIVO porta all’atto del gemello 2.", 'info')
    y = S.pulsantiera(dr, y, [("INDIETRO", False)],
                      [("PRENOTA GEMELLI", False), ("ANTEPRIMA GEMELLO 1", True)])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    S.ritaglia(im, y, dest)
    return dest


if __name__ == '__main__':
    print(conferma(os.path.join(DIR, 'gem_prenota_conferma.png')))
    print(esito(os.path.join(DIR, 'gem_prenota_esito.png')))
