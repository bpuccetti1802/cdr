# -*- coding: utf-8 -*-
"""Il Riepilogo della pratica dei gemelli con documenti e firmatari per ciascun nato
(22/11/2026), costruito sulla schermata reale di SIPO «Riepilogo Atto - Dichiarazione Nascita Figli
Gemelli» (figura 2 dell'analisi): testata, «Dati Atto» e pulsanti sono quelli veri, ingranditi;
l'avviso è riscritto e la sezione «Documenti e firmatari per atto» è nuova.
Il nome dell'operatore è coperto.

Dati dell'esempio, dalle sorgenti ANSC: gemello 2 nato morto (UC 11111100, Dic_Nasc_002: certificato
medico obbligatorio; attestazione di nascita condizionata a tipoAccertamento = 1); firmatari da
SOGGETTI_USECASE (padre dichiarante e firmatario, madre non firmataria, interprete condizionato).

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_gemellari_riepilogo.py SORGENTE.png
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'img', 'gemellari', 'gem10_riepilogo.png')
FD = '/System/Library/Fonts/Supplemental'
K = 2                                           # fattore di ingrandimento
W = 922 * K

ROSSO, GIALLO_BARRA, BLU_VAL = (131, 1, 26), (203, 165, 7), (54, 99, 154)
INK, ETICH, BORDO, LEGENDA = (34, 34, 34), (80, 80, 80), (216, 216, 216), (110, 110, 110)
VERDE, VERDE_F, ARANCIO, ARANCIO_F = (63, 143, 95), (227, 243, 232), (181, 110, 0), (255, 244, 214)
GRIGIO, GRIGIO_F, OPERATORE = (150, 150, 150), (242, 242, 242), (245, 166, 35)


def f(nome, pt):
    return ImageFont.truetype(os.path.join(FD, nome), pt)


REG, BLD, ITA = (lambda p: f('Arial Narrow.ttf', p)), (lambda p: f('Arial Narrow Bold.ttf', p)), \
    (lambda p: f('Arial Narrow Italic.ttf', p))


def su(im, box):
    """Ritaglio dell'originale (coordinate originali) ingrandito di K."""
    c = im.crop(box)
    return c.resize((c.width * K, c.height * K), Image.LANCZOS)


def bottone(dr, x, y, t, prim=True, pt=15, h=34):
    w = int(dr.textlength(t, font=BLD(pt))) + 28
    if prim:
        dr.rectangle((x, y, x + w, y + h), fill=ROSSO)
        dr.text((x + 14, y + h / 2), t, font=BLD(pt), fill='white', anchor='lm')
    else:
        dr.rectangle((x, y, x + w, y + h), outline=ROSSO, width=2, fill='white')
        dr.text((x + 14, y + h / 2), t, font=BLD(pt), fill=ROSSO, anchor='lm')
    return w


def link(dr, x, y, t, pt=15):
    dr.text((x, y), t, font=BLD(pt), fill=BLU_VAL, anchor='lm')
    return int(dr.textlength(t, font=BLD(pt)))


def pill(dr, x, y, t, col, fondo, pt=14):
    w = int(dr.textlength(t, font=BLD(pt))) + 20
    dr.rounded_rectangle((x, y - 13, x + w, y + 13), 12, fill=fondo, outline=col, width=2)
    dr.text((x + 10, y), t, font=BLD(pt), fill=col, anchor='lm')
    return w


def casella(dr, x, y, on, fissa=False):
    dr.rectangle((x, y - 9, x + 18, y + 9), outline=GRIGIO if fissa else ROSSO, width=2,
                 fill=GRIGIO_F if fissa else 'white')
    if on:
        dr.line((x + 4, y, x + 8, y + 5, x + 15, y - 6), fill=GRIGIO if fissa else ROSSO, width=3)


def fieldset(dr, x0, y0, x1, y1, legenda):
    dr.rounded_rectangle((x0, y0, x1, y1), 8, outline=BORDO, width=2, fill='white')
    w = int(dr.textlength(legenda, font=REG(19)))
    dr.rectangle((x0 + 14, y0 - 12, x0 + 26 + w, y0 + 12), fill='white')
    dr.text((x0 + 20, y0), legenda, font=REG(19), fill=LEGENDA, anchor='lm')


def tabella(dr, x, y, col, righe, h=40, pt=15):
    """col = [(intestazione, larghezza)]; righe = liste di celle (testo o funzione(dr,x,yc))."""
    tot = sum(w for _, w in col)
    dr.rectangle((x, y, x + tot, y + h), fill=GRIGIO_F)
    xx = x
    for t, w in col:
        dr.text((xx + 10, y + h / 2), t, font=BLD(pt), fill=INK, anchor='lm')
        xx += w
    y += h
    for r in righe:
        dr.line((x, y + h, x + tot, y + h), fill=BORDO, width=1)
        xx = x
        for (t, w), v in zip(col, r):
            if callable(v):
                v(dr, xx + 10, y + h / 2)
            elif v:
                dr.text((xx + 10, y + h / 2), v, font=REG(pt), fill=INK, anchor='lm')
            xx += w
        y += h
    return y


def costruisci(sorgente):
    im = Image.open(sorgente).convert('RGB')
    assert im.size == (922, 420), im.size
    testa = su(im, (0, 0, 922, 131))                     # testata, menu, percorso
    dati = su(im, (0, 232, 922, 346))                    # «Dati Atto»
    piede = su(im, (0, 352, 922, 400))                   # INDIETRO · CONFERMA
    icona = su(im, (24, 138, 46, 160))

    H = 2600
    c = Image.new('RGB', (W, H), 'white')
    c.paste(testa, (0, 0))
    dr = ImageDraw.Draw(c)
    # nome dell'operatore coperto
    dr.rectangle((815 * K, 60 * K, 880 * K, 76 * K), fill=ROSSO)
    dr.text((818 * K, 68 * K), 'Operatore', font=BLD(17), fill=OPERATORE, anchor='lm')

    # ── avviso riscritto
    y = 270
    dr.rectangle((26, y, 34, y + 214), fill=GIALLO_BARRA)
    c.paste(icona, (58, y + 14))
    dr.text((110, y + 34), 'Attenzione!', font=BLD(25), fill=INK, anchor='lm')
    for k, t in enumerate((
            'Se si conferma, la pratica verrà divisa in 3 atti diversi, ciascuno per ogni nato; '
            'SIPO staccherà i numeri comunali e prenoterà gli atti in ANSC.',
            'Prima di confermare, controllare per ciascun gemello i documenti previsti e i '
            'firmatari, nella sezione «Documenti e firmatari per atto».')):
        dr.text((110, y + 80 + k * 30), t, font=REG(19), fill=INK, anchor='lm')
    w = pill(dr, 110, y + 150, 'Gemello 2: manca 1 documento obbligatorio', ARANCIO, ARANCIO_F,
             pt=15)
    dr.text((110 + w + 14, y + 150), 'la conferma è consentita; il documento servirà prima del '
            'completamento dell’atto', font=ITA(16), fill=ETICH, anchor='lm')
    bottone(dr, 120, y + 180, 'CONFERMA', h=32)
    y += 236

    # ── Dati Atto (originale)
    c.paste(dati, (0, y))
    y += dati.height + 30

    # ── sezione nuova
    x0, x1 = 50, W - 50
    top = y
    # linguette dei gemelli
    yy = top + 36
    gem = [('Gemello 1 · M · nato vivo', 'UC 11111000', 'completo', True),
           ('Gemello 2 · F · nato morto', 'UC 11111100', '1 mancante', False),
           ('Gemello 3 · F · nato vivo', 'UC 11111000', 'completo', True)]
    xx = x0 + 24
    for k, (t, uc, stato, ok) in enumerate(gem):
        attiva = k == 1
        w = 400
        dr.rectangle((xx, yy, xx + w, yy + 64), fill=ROSSO if attiva else 'white',
                     outline=ROSSO, width=2)
        col = 'white' if attiva else ROSSO
        dr.text((xx + 16, yy + 20), t, font=BLD(18), fill=col, anchor='lm')
        dr.text((xx + 16, yy + 46), uc, font=REG(16), fill=col, anchor='lm')
        pill(dr, xx + 250, yy + 46, stato,
             VERDE if ok else ARANCIO, VERDE_F if ok else ARANCIO_F, pt=13)
        xx += w + 12
    yy += 64
    dr.line((x0 + 24, yy, x1 - 24, yy), fill=ROSSO, width=3)
    yy += 30
    dr.text((x0 + 24, yy), 'NATO 2 — COGNOME NOME · nata morta il 19/11/2026 alle 17:02 · 2° '
            'di 3 · UC 11111100 – Dichiarazione entro i 10 giorni – resa dal padre (nato morto)',
            font=REG(17), fill=INK, anchor='lm')
    yy += 22
    dr.text((x0 + 24, yy + 10), 'Documenti dal mapping del caso d’uso (ALLEGATI_USECASE); '
            'firmatari da SOGGETTI_USECASE e dai dati della pratica.', font=ITA(15),
            fill=ETICH, anchor='lm')

    # documenti
    yy += 48
    dr.text((x0 + 24, yy), 'Documenti previsti', font=BLD(21), fill=ROSSO, anchor='lm')
    yy += 22

    def stato_pill(t, col, fondo):
        return lambda d, x, yc: pill(d, x, yc, t, col, fondo, pt=13)

    def azioni(*v):
        def g(d, x, yc):
            for t in v:
                x += link(d, x, yc, t) + 18
        return g
    col = [('Documento', 520), ('Presenza', 330), ('File', 270), ('Stato', 190),
           ('Azioni', 380)]
    yy = tabella(dr, x0 + 24, yy, col, [
        ['Certificato medico attestante che il bambino è nato morto', 'Obbligatorio', '—',
         stato_pill('Mancante', ARANCIO, ARANCIO_F), azioni('CARICA')],
        ['Attestazione di nascita', 'Condizionato · accertamento con attestazione',
         'attestazione_g2.pdf', stato_pill('Caricato', VERDE, VERDE_F),
         azioni('VISUALIZZA', 'SOSTITUISCI', 'ELIMINA')],
        ['Autorizzazione del tribunale', 'Facoltativo', '—', '', azioni('CARICA')],
        ['Documento autorizzativo', 'Facoltativo', '—', '', azioni('CARICA')],
    ], h=44)
    dr.text((x0 + 34, yy + 22), 'Non richiesti per questo nato (accertamento con attestazione): '
            'Constatazione di avvenuto parto · Dichiarazione di nascita sostitutiva resa da '
            'dichiarante', font=ITA(15), fill=ETICH, anchor='lm')
    yy += 44
    dr.text((x0 + 34, yy + 12), 'I documenti restano in SIPO (stato «Caricato in SIPO») e vanno '
            'in ANSC alla validazione dell’atto.', font=ITA(15), fill=ETICH, anchor='lm')

    # firmatari
    yy += 60
    dr.text((x0 + 24, yy), 'Firmatari', font=BLD(21), fill=ROSSO, anchor='lm')
    bw = 0
    xb = x1 - 24
    for t in ('COPIA SUGLI ALTRI GEMELLI', 'AGGIUNGI INTERPRETE'):
        w = int(dr.textlength(t, font=BLD(15))) + 28
        xb -= w
        bottone(dr, xb, yy - 17, t, prim=False)
        xb -= 14
    yy += 22

    def spunta(on, fissa=False):
        return lambda d, x, yc: casella(d, x + 20, yc, on, fissa)
    col = [('Soggetto', 470), ('Ruolo nell’atto', 300), ('Dichiarante', 160),
           ('Firmatario', 160), ('Note', 600)]
    yy = tabella(dr, x0 + 24, yy, col, [
        ['Padre · COGNOME NOME · CF ****************', 'padre', spunta(True, True),
         spunta(True, True), 'obbligatorio per l’UC: dichiara e firma'],
        ['Madre · COGNOME NOME · CF ****************', 'madre', spunta(False), spunta(False),
         'può essere indicata come dichiarante e firmataria'],
        ['Nato 2 — COGNOME NOME', 'intestatario', '', '', 'non firma'],
        ['Interprete', 'condizionato', '', '', 'solo se il dichiarante non comprende la lingua: '
         'AGGIUNGI INTERPRETE'],
    ], h=44)
    yy += 26
    dr.text((x0 + 34, yy), 'Dichiaranti per questo atto: 1. Il modo di firma (elettronica o su '
            'carta) si sceglie al momento della firma, nella pagina «Gemelli del parto».',
            font=ITA(15), fill=ETICH, anchor='lm')
    yy += 40
    return c, top, yy, piede


def main(sorgente):
    c2, top, fondo, piede = costruisci(sorgente)
    dr = ImageDraw.Draw(c2)
    # la cornice si disegna dopo il contenuto, solo il bordo, senza riempimento
    x0, x1 = 50, W - 50
    dr.rounded_rectangle((x0, top, x1, fondo), 8, outline=BORDO, width=2)
    leg = 'Documenti e firmatari per atto'
    w = int(dr.textlength(leg, font=REG(19)))
    dr.rectangle((x0 + 14, top - 12, x0 + 26 + w, top + 12), fill='white')
    dr.text((x0 + 20, top), leg, font=REG(19), fill=LEGENDA, anchor='lm')
    y = fondo + 30
    c2.paste(piede, (0, y))
    y += piede.height + 20
    c2 = c2.crop((0, 0, W, y))
    c2.save(OUT)
    return OUT


if __name__ == '__main__':
    print(main(sys.argv[1]))
