# -*- coding: utf-8 -*-
"""Primitive di wireframe per il back-office dell'integrazione SIPO→ANSC.

Le convenzioni sono quelle osservate su S.I.De. (Comune di Milano) nelle schermate
raccolte in `SIDE/Grafica`: barra applicativa colorata, briciole di pane, titolo con
distintivo di sessione e azioni a destra, pannelli di filtro richiudibili, tabella dei
risultati con colonna «Azioni» e paginazione in basso a destra.

⚠️ Sono schizzi funzionali, non un progetto grafico: dicono che cosa una pagina mostra e
quali azioni offre. ⚠️ Niente emoji: Arial non ha i glifi di spunta, croce e occhio —
sono disegnati come vettori da `ic_*()`.

    /Library/Developer/CommandLineTools/usr/bin/python3 wireframe_bo.py img
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import F_BLD, F_ITA, F_REG, MUTED, avvolgi, centra, fnt  # noqa: E402

INK = '#1f2937'
BORDO = '#c7cdd6'
TENUE = '#f3f4f6'
RIGA = '#e8eaee'
BARRA = '#9b1b30'          # la barra applicativa, come in SIDE
BLU = '#2f6bb0'
VERDE = '#3f8f5f'
ROSSO = '#b03a48'
GIALLO = '#d9a441'
VIOLA = '#7b5aa6'


# ─────────────────────────────────────────────────────────────── icone
def ic_spunta(dr, x, y, c=VERDE):
    dr.line([(x, y + 5), (x + 4, y + 9), (x + 11, y)], fill=c, width=2)


def ic_croce(dr, x, y, c=ROSSO):
    dr.line([(x, y), (x + 10, y + 10)], fill=c, width=2)
    dr.line([(x + 10, y), (x, y + 10)], fill=c, width=2)


def ic_occhio(dr, x, y, c=MUTED):
    dr.ellipse([x, y, x + 16, y + 10], outline=c, width=2)
    dr.ellipse([x + 5, y + 2, x + 11, y + 8], fill=c)


def ic_matita(dr, x, y, c=BLU):
    dr.line([(x, y + 10), (x + 9, y + 1)], fill=c, width=2)
    dr.line([(x, y + 10), (x + 3, y + 10)], fill=c, width=2)


def ic_cestino(dr, x, y, c=ROSSO):
    dr.rectangle([x + 1, y + 3, x + 9, y + 11], outline=c, width=2)
    dr.line([(x - 1, y + 2), (x + 11, y + 2)], fill=c, width=2)


def ic_piu(dr, x, y, c=BLU, r=9):
    dr.ellipse([x, y, x + 2 * r, y + 2 * r], fill=c)
    dr.line([(x + r - 4, y + r), (x + r + 4, y + r)], fill='white', width=2)
    dr.line([(x + r, y + r - 4), (x + r, y + r + 4)], fill='white', width=2)


def ic_chevron(dr, x, y, giu=True, c=MUTED):
    if giu:
        dr.polygon([(x, y), (x + 10, y), (x + 5, y + 6)], fill=c)
    else:
        dr.polygon([(x, y + 6), (x + 10, y + 6), (x + 5, y)], fill=c)


def azioni(dr, x, y, quali):
    """Disegna la colonna «Azioni»: sequenza di icone."""
    for q in quali:
        {'ok': ic_spunta, 'no': ic_croce, 'vedi': ic_occhio,
         'mod': ic_matita, 'del': ic_cestino}[q](dr, x, y)
        x += 24


# ──────────────────────────────────────────────────────────── struttura
def _stemma(dr, x, y, h=34, c=BARRA):
    """Lo scudo SPQR, in forma schematica."""
    w = h * 0.72
    dr.polygon([(x, y + 6), (x + w, y + 6), (x + w, y + h * 0.6),
                (x + w / 2, y + h), (x, y + h * 0.6)], outline=c, width=2)
    dr.rectangle([x + 4, y, x + w - 4, y + 6], outline=c, width=2)
    centra(dr, 'SPQR', fnt(F_BLD, int(h * 0.26)), x + w / 2, y + h * 0.3, c)


def pagina(larg, alt, briciole, titolo, distintivo=None, azioni_dx=(), sotto=None,
           contesto=None):
    """Cornice secondo il design system di Roma Capitale.

    Tre bande: barra di servizio, testata istituzionale, contenuto. Il piè di pagina si
    aggiunge con `pie_pagina()` in coda, perché la sua altezza dipende dal contenuto.
    """
    im = Image.new('RGB', (larg, alt), '#ffffff')
    dr = ImageDraw.Draw(im)

    # barra di servizio
    dr.rectangle([0, 0, larg, 40], fill='#ffffff')
    dr.line([(0, 40), (larg, 40)], fill='#e3e5e8')
    dr.text((28, 13), 'Layout Esteso', font=fnt(F_BLD, 12), fill=INK)
    dr.rounded_rectangle([140, 12, 176, 28], radius=8, fill='#c9ccd1')
    dr.ellipse([160, 11, 178, 29], fill=BARRA)
    ic_spunta(dr, 164, 15, 'white')
    ut = 'MARIO ROSSI'
    xu = larg - 28 - 14 - 34 - dr.textlength(ut, font=fnt(F_BLD, 12))
    dr.text((xu, 13), ut, font=fnt(F_BLD, 12), fill=BARRA)
    dr.ellipse([larg - 70, 8, larg - 38, 40 - 8], fill=BARRA)
    centra(dr, 'MR', fnt(F_BLD, 12), larg - 54, 14, 'white')
    ic_chevron(dr, larg - 30, 18)

    # testata istituzionale
    dr.rectangle([0, 41, larg, 118], fill='#ffffff')
    dr.line([(0, 118), (larg, 118)], fill='#e3e5e8')
    dr.text((28, 56), 'ROMA', font=fnt(F_BLD, 42), fill=BARRA)
    _stemma(dr, 196, 60, 40)
    dr.text((252, 76), 'Roma Capitale', font=fnt(F_REG, 13), fill=BARRA)

    y = 138
    if contesto:
        dr.rounded_rectangle([24, y, larg - 24, y + 30], radius=4, fill='#f6f7f8')
        dr.text((38, y + 8), contesto, font=fnt(F_REG, 12), fill=MUTED)
        y += 42

    x = 28
    for i, b in enumerate(briciole):
        f = fnt(F_REG, 12)
        c = BARRA if i < len(briciole) - 1 else MUTED
        dr.text((x, y), b, font=f, fill=c)
        if i < len(briciole) - 1:
            dr.line([(x, y + 14), (x + dr.textlength(b, font=f), y + 14)], fill=c)
            x += dr.textlength(b, font=f) + 8
            dr.text((x, y), '›', font=f, fill=MUTED)
            x += 12
    y += 24
    dr.text((28, y), titolo, font=fnt(F_BLD, 22), fill=INK)
    xt = 28 + dr.textlength(titolo, font=fnt(F_BLD, 22)) + 20
    if distintivo:
        testo, ok = distintivo
        w = int(dr.textlength(testo, font=fnt(F_BLD, 12))) + 44
        c = VERDE if ok else ROSSO
        dr.rounded_rectangle([xt, y + 1, xt + w, y + 27], radius=4, outline=c, width=2)
        dr.text((xt + 12, y + 7), testo, font=fnt(F_BLD, 12), fill=c)
        (ic_spunta if ok else ic_croce)(dr, xt + w - 24, y + 8, c)
    xd = larg - 28
    for testo in reversed(azioni_dx):
        w = int(dr.textlength(testo, font=fnt(F_BLD, 12))) + 30
        dr.rounded_rectangle([xd - w, y, xd, y + 28], radius=4, fill=BARRA)
        dr.text((xd - w + 15, y + 7), testo, font=fnt(F_BLD, 12), fill='white')
        xd -= w + 10
    y += 40
    if sotto:
        for r in avvolgi(dr, sotto, fnt(F_ITA, 12), larg - 70):
            dr.text((28, y), r, font=fnt(F_ITA, 12), fill=MUTED)
            y += 16
        y += 8
    return im, dr, y


def pie_pagina(dr, larg, y, voci_menu=('Home', 'Supervisione atti', 'Dizionari')):
    """Il piè di pagina istituzionale: tre colonne su fondo scuro, poi la riga legale."""
    h = 210
    dr.rectangle([0, y, larg, y + h], fill='#3a3d42')
    dr.text((44, y + 22), 'ROMA', font=fnt(F_BLD, 26), fill='white')
    _stemma(dr, 148, y + 22, 28, 'white')
    colonne = [
        (44, 'CONTATTI', ['Piazza del Campidoglio 1 - 00186 (RM)', 'Partita IVA 01057861005',
                          'Codice Fiscale 02438750586', '',
                          'Ufficio Responsabile Protezione Dati (RPD)',
                          'Chiama Roma 060606', 'Tutti i contatti']),
        (430, 'MENU', list(voci_menu)),
        (760, 'SEGUICI SU', ['f  X  in  ig  yt', '', 'INFORoMA']),
    ]
    for cx, tit, righe in colonne:
        dr.text((cx, y + 76), tit, font=fnt(F_BLD, 13), fill='white')
        dr.line([(cx, y + 96), (cx + 300, y + 96)], fill='#5a5d63')
        yy = y + 106
        for r in righe:
            if r:
                dr.text((cx, yy), r, font=fnt(F_BLD if r.isupper() else F_REG, 11), fill='white')
            yy += 15
    dr.rectangle([0, y + h, larg, y + h + 40], fill='#2e3136')
    dr.text((44, y + h + 13), 'Privacy', font=fnt(F_REG, 12), fill='white')
    dr.text((140, y + h + 13), 'Cookie Policy', font=fnt(F_REG, 12), fill='white')
    return y + h + 40


def campo(dr, x, y, w, etichetta, valore=None, tipo='testo', h=36):
    """Campo con etichetta flottante, come nelle maschere di SIDE."""
    dr.rounded_rectangle([x, y, x + w, y + h], radius=4, outline=BORDO, width=1, fill='white')
    dr.rectangle([x + 9, y - 1, x + 13 + dr.textlength(etichetta, font=fnt(F_REG, 10)), y + 1],
                 fill='white')
    dr.text((x + 11, y - 6), etichetta, font=fnt(F_REG, 10), fill=MUTED)
    if valore:
        dr.text((x + 11, y + 11), valore, font=fnt(F_REG, 12), fill=INK)
    if tipo == 'select':
        ic_chevron(dr, x + w - 22, y + 15)
    elif tipo == 'data':
        dr.rounded_rectangle([x + w - 26, y + 9, x + w - 10, y + 25], radius=2,
                             outline=MUTED, width=1)
        dr.line([(x + w - 26, y + 14), (x + w - 10, y + 14)], fill=MUTED)
    return x + w


def riga_campi(dr, x, y, larg, specifiche, gap=14):
    """Una riga di campi: specifiche = [(etichetta, valore, tipo, peso), …]."""
    tot = sum(s[3] for s in specifiche)
    disp = larg - gap * (len(specifiche) - 1)
    cx = x
    for et, val, tp, peso in specifiche:
        w = int(disp * peso / tot)
        campo(dr, cx, y, w, et, val, tp)
        cx += w + gap
    return y + 52


def pannello(dr, x, y, larg, titolo, aperto=True, alt=None):
    """Pannello richiudibile: intestazione con chevron."""
    dr.rounded_rectangle([x, y, x + larg, y + 30], radius=5, fill=TENUE, outline=BORDO, width=1)
    ic_chevron(dr, x + 12, y + 12, giu=not aperto)
    dr.text((x + 32, y + 8), titolo, font=fnt(F_BLD, 12), fill=INK)
    if alt:
        dr.rounded_rectangle([x, y, x + larg, y + alt], radius=5, outline=BORDO, width=1)
        dr.rounded_rectangle([x, y, x + larg, y + 30], radius=5, fill=TENUE,
                             outline=BORDO, width=1)
        dr.rectangle([x + 1, y + 24, x + larg - 1, y + 30], fill=TENUE)
        ic_chevron(dr, x + 12, y + 12, giu=not aperto)
        dr.text((x + 32, y + 8), titolo, font=fnt(F_BLD, 12), fill=INK)
    return y + 44


def righe_etichette(dr, x, y, coppie, larg, colonne=3, passo=26):
    """Griglia di «etichetta: valore» — il riepilogo in testa a una pagina di dettaglio."""
    w = larg // colonne
    for i, (et, val) in enumerate(coppie):
        cx = x + (i % colonne) * w
        cy = y + (i // colonne) * passo
        dr.text((cx, cy), et + ':', font=fnt(F_REG, 12), fill=MUTED)
        dr.text((cx + dr.textlength(et + ': ', font=fnt(F_REG, 12)) + 4, cy), str(val),
                font=fnt(F_BLD, 12), fill=INK)
    return y + ((len(coppie) + colonne - 1) // colonne) * passo + 8


def accordion(dr, x, y, larg, voci, passo=30):
    """Elenco di sezioni richiudibili con stato di completezza (come in SIDE)."""
    for testo, stato in voci:
        dr.rounded_rectangle([x, y, x + larg, y + passo - 4], radius=4,
                             fill='#fbfbfc', outline=BORDO, width=1)
        ic_chevron(dr, x + 12, y + 10)
        dr.text((x + 32, y + 6), testo, font=fnt(F_REG, 12), fill=INK)
        w = dr.textlength(testo, font=fnt(F_REG, 12))
        if stato == 'ok':
            ic_spunta(dr, x + 42 + w, y + 7)
        elif stato == 'ko':
            ic_croce(dr, x + 42 + w, y + 7)
        y += passo
    return y + 8


def tabella(dr, x, y, larg, intestazioni, larghezze, righe, alt=30, azioni_su=None):
    # intestazione su fondo rosso istituzionale, come nel design system di Roma Capitale
    dr.rectangle([x, y, x + larg, y + 30], fill=BARRA)
    cx = x + 10
    for t, w in zip(intestazioni, larghezze):
        dr.text((cx, y + 9), t, font=fnt(F_BLD, 11), fill='white')
        cx += w
    yy = y + 30
    for i, riga in enumerate(righe):
        if i % 2:
            dr.rectangle([x, yy, x + larg, yy + alt], fill='#fafbfc')
        dr.line([(x, yy + alt), (x + larg, yy + alt)], fill=RIGA)
        cx = x + 10
        for val, w in zip(riga, larghezze):
            if isinstance(val, tuple) and len(val) == 2 and isinstance(val[1], str) \
                    and val[1].startswith('#'):
                testo, colore = val
                bw = int(dr.textlength(testo, font=fnt(F_BLD, 10))) + 20
                dr.rounded_rectangle([cx, yy + 6, cx + bw, yy + alt - 6], radius=8, fill=colore)
                centra(dr, testo, fnt(F_BLD, 10), cx + bw / 2, yy + 8, 'white')
            elif isinstance(val, list):
                azioni(dr, cx, yy + 10, val)
            else:
                dr.text((cx, yy + 9), str(val), font=fnt(F_REG, 11), fill=INK)
            cx += w
        yy += alt
    return yy + 6


def paginazione(dr, x, y, larg, totale='6', per_pagina='5 Elementi per pagina', pagine=2):
    """Impaginazione del design system: pagine a sinistra, totale al centro, scelta a destra."""
    f = fnt(F_REG, 12)
    dr.text((x + 8, y), '«', font=fnt(F_BLD, 14), fill=MUTED)
    cx = x + 36
    # con molte pagine si mostrano le prime tre, i puntini e l'ultima: altrimenti
    # la riga dei numeri invade il totale al centro.
    numeri = [str(n) for n in range(1, pagine + 1)] if pagine <= 5 else \
        ['1', '2', '3', '…', str(pagine)]
    for t in numeri:
        primo = (t == '1')
        dr.text((cx, y), t, font=fnt(F_BLD if primo else F_REG, 12),
                fill=BARRA if primo else MUTED)
        cx += int(dr.textlength(t, font=fnt(F_REG, 12))) + 22
    dr.text((cx, y), '»', font=fnt(F_BLD, 14), fill=MUTED)
    testo = 'Numero totale righe: ' + totale
    dr.text((x + larg / 2 - dr.textlength(testo, font=f) / 2, y), testo, font=f, fill=INK)
    w = int(dr.textlength(per_pagina, font=f)) + 52
    dr.rounded_rectangle([x + larg - w, y - 8, x + larg, y + 22], radius=4,
                         outline=BORDO, width=1, fill='white')
    dr.text((x + larg - w + 14, y), per_pagina, font=f, fill=INK)
    ic_chevron(dr, x + larg - 26, y + 4)
    return y + 34


def bottoni(dr, x, y, voci, h=30):
    """voci = [(testo, colore, pieno)] — allineati a sinistra dalla x indicata."""
    for v in voci:
        testo, colore, pieno = (v + (False,))[:3] if len(v) == 2 else v
        w = int(dr.textlength(testo, font=fnt(F_BLD, 12))) + 30
        if pieno:
            dr.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=colore)
            dr.text((x + 15, y + 8), testo, font=fnt(F_BLD, 12), fill='white')
        else:
            dr.rounded_rectangle([x, y, x + w, y + h], radius=5, outline=colore, width=2)
            dr.text((x + 15, y + 8), testo, font=fnt(F_BLD, 12), fill=colore)
        x += w + 10
    return y + h + 12


def bottoni_dx(dr, x_fine, y, voci, h=30):
    """Come `bottoni`, ma allineati a destra (schema PULISCI / CERCA di SIDE)."""
    larghezze = [int(dr.textlength(v[0], font=fnt(F_BLD, 12))) + 30 for v in voci]
    x = x_fine - sum(larghezze) - 10 * (len(voci) - 1)
    for v, w in zip(voci, larghezze):
        testo, colore = v[0], v[1]
        pieno = v[2] if len(v) > 2 else False
        if pieno:
            dr.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=colore)
            dr.text((x + 15, y + 8), testo, font=fnt(F_BLD, 12), fill='white')
        else:
            dr.rounded_rectangle([x, y, x + w, y + h], radius=5, outline=colore, width=2)
            dr.text((x + 15, y + 8), testo, font=fnt(F_BLD, 12), fill=colore)
        x += w + 10
    return y + h + 12


def schede(dr, x, y, larg, voci, attiva=0):
    """Linguette di navigazione interna a una pagina di dettaglio."""
    dr.line([(x, y + 30), (x + larg, y + 30)], fill=BORDO)
    for i, t in enumerate(voci):
        w = int(dr.textlength(t, font=fnt(F_BLD, 12))) + 36
        c = BLU if i == attiva else MUTED
        dr.text((x + 18, y + 8), t, font=fnt(F_BLD, 12), fill=c)
        if i == attiva:
            dr.rectangle([x, y + 28, x + w, y + 31], fill=BLU)
        x += w
    return y + 44


def nota(dr, x, y, larg, testo, colore=BLU):
    """Riquadro informativo a filetto, come gli avvisi della web app ANSC."""
    righe = avvolgi(dr, testo, fnt(F_REG, 12), larg - 40)
    h = 14 + len(righe) * 17
    dr.rectangle([x, y, x + larg, y + h], fill='#f7f9fc')
    dr.rectangle([x, y, x + 4, y + h], fill=colore)
    yy = y + 8
    for r in righe:
        dr.text((x + 16, yy), r, font=fnt(F_REG, 12), fill=INK)
        yy += 17
    return y + h + 12


def card(dr, x, y, w, h, titolo, sotto=None):
    """Riquadro del menu a mattonelle (la Home di SIDE)."""
    dr.rounded_rectangle([x, y, x + w, y + h], radius=5, outline=BORDO, width=1, fill='white')
    dr.rectangle([x, y, x + 4, y + h], fill=BARRA)
    dr.text((x + 20, y + 14), titolo, font=fnt(F_REG, 14), fill=INK)
    if sotto:
        dr.text((x + 20, y + 36), sotto, font=fnt(F_ITA, 11), fill=MUTED)


def salva(im, dest, nome, margine=26, pie=True, voci_menu=None):
    """Ritaglia il bianco in coda, aggiunge il piè di pagina istituzionale e salva.

    Così le altezze non vanno regolate a mano e il piè resta sempre attaccato al contenuto.
    """
    larg, alt = im.size
    px = im.load()
    ultima = 0
    for yy in range(alt):
        for xx in range(0, larg, 4):
            if px[xx, yy] != (255, 255, 255):
                ultima = yy
                break
    fine = min(alt, ultima + margine)
    if pie:
        alto = fine + 250
        nuova = Image.new('RGB', (larg, alto), 'white')
        nuova.paste(im.crop((0, 0, larg, fine)), (0, 0))
        dr = ImageDraw.Draw(nuova)
        pie_pagina(dr, larg, fine, voci_menu or ('Home', 'Supervisione atti', 'Dizionari'))
        im = nuova
    else:
        im = im.crop((0, 0, larg, fine))
    os.makedirs(dest, exist_ok=True)
    im.save(os.path.join(dest, nome))
    return '%s (%d×%d)' % (nome, im.size[0], im.size[1])
