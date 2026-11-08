# -*- coding: utf-8 -*-
"""Schermate SIPO del percorso «Riepilogo senza UC → WebApp» (07/11/2026, richiesta dell'utente).

Parte da tre schermate REALI di SIPO (copiate in `Sorgenti Documentali/Immagini sipo/`) e le
conforma alla sequenza dettata dall'utente:

  1) Riepilogo senza UC: messaggio «Attenzione: Non è stato identificato uno Usecase ANSC…»
  2) inibito il bottone che porta all'anteprima (nella schermata reale si chiama CONFERMA)
  3) nuovo bottone «DATI PER ANSC», che ottiene il numero comunale
  4) anteprima con il nuovo numero comunale e il testo dell'atto
  5) nuovo bottone «COPIA TESTO» (testo dell'atto negli appunti)
  6) la pagina si mette in attesa dell'atto ANSC (idAnsc) prodotto dalla WebApp

Schermata 1 ← sipo_riepilogo_morte_abitazione.png (passi 1-3)
Schermata 2 ← sipo_anteprima_morte_abitazione.png (passi 4-5)
Schermata 3 ← sipo_dettaglio_atto_decesso.png, riscritta con i dati dello stesso atto (passo 6)

I numeri dei passi sono pastiglie gialle sugli elementi. Colori campionati dalle schermate;
font Arial Narrow al posto di Titillium (come in schermate_sipo_wf.py).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_testo_libero.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(QUI))
SRC = os.path.join(BASE, 'Sorgenti Documentali', 'Immagini sipo')
OUT = os.path.join(QUI, 'img', 'testo_libero')

ROSSO = (142, 0, 28)
BLU = (2, 69, 140)
NERO = (28, 32, 36)
GRIGIO = (128, 128, 128)
BORDO = (221, 221, 221)
BIANCO = (255, 255, 255)
GIALLO = (255, 179, 0)
SPENTO_FONDO, SPENTO_TESTO = (214, 216, 219), (150, 150, 150)
AVVISO_FONDO, AVVISO_BORDO = (255, 243, 205), (230, 160, 0)
OK_FONDO, OK_BORDO = (232, 245, 233), (63, 143, 95)
INFO_FONDO, INFO_BORDO = (227, 238, 250), (2, 69, 140)

F = '/System/Library/Fonts/Supplemental/'


def font(dim, grassetto=False):
    return ImageFont.truetype(F + ('Arial Narrow Bold.ttf' if grassetto else 'Arial Narrow.ttf'), dim)


NUMERO = '124'            # numero comunale di esempio (serie annuale, be-numeratore-comunale)
ANNO = '2026'

MESSAGGIO = ('Non è stato identificato uno Usecase ANSC. Si prega di passare alla WebApp per '
             'formare un atto a testo libero. Al termine delle operazioni sulla webApp rientrare '
             'in Sipo per completare le operazioni')


# ------------------------------------------------------------------ primitive
def inserisci(im, y, altezza):
    """Apre una fascia bianca alta «altezza» all'ordinata y."""
    nuovo = Image.new('RGB', (im.width, im.height + altezza), BIANCO)
    nuovo.paste(im.crop((0, 0, im.width, y)), (0, 0))
    nuovo.paste(im.crop((0, y, im.width, im.height)), (0, y + altezza))
    return nuovo


def avvolgi(dr, testo, f, larghezza):
    righe, riga = [], ''
    for parola in testo.split():
        prova = (riga + ' ' + parola).strip()
        if dr.textlength(prova, font=f) <= larghezza:
            riga = prova
        else:
            righe.append(riga)
            riga = parola
    righe.append(riga)
    return righe


def banner(dr, box, fondo, bordo, testa, testo, dim=21):
    x0, y0, x1, y1 = box
    dr.rectangle(box, fill=fondo, outline=bordo, width=2)
    dr.rectangle((x0, y0, x0 + 7, y1), fill=bordo)
    fb, fn = font(dim, True), font(dim)
    x, y = x0 + 24, y0 + 16
    dr.text((x, y), testa, font=fb, fill=NERO)
    primo = x + dr.textlength(testa + ' ', font=fb)
    righe = avvolgi(dr, testo, fn, x1 - primo - 24)
    dr.text((primo, y), righe[0], font=fn, fill=NERO)
    resto = ' '.join(righe[1:])
    for i, r in enumerate(avvolgi(dr, resto, fn, x1 - x - 24) if resto else []):
        dr.text((x, y + (i + 1) * (dim + 8)), r, font=fn, fill=NERO)


def bottone(dr, box, testo, attivo=True, dim=17):
    dr.rectangle(box, fill=ROSSO if attivo else SPENTO_FONDO)
    f = font(dim, True)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    dr.text((cx, cy), testo, font=f, fill=BIANCO if attivo else SPENTO_TESTO, anchor='mm')


def pastiglia(dr, xy, n, r=19):
    x, y = xy
    dr.ellipse((x - r, y - r, x + r, y + r), fill=GIALLO, outline=NERO, width=2)
    dr.text((x, y), str(n), font=font(24, True), fill=NERO, anchor='mm')


def cancella(dr, box):
    dr.rectangle(box, fill=BIANCO)


def campo(dr, x, y, etichetta, valore, dim=19, colore=BLU):
    """Etichetta in grassetto e valore in blu, centrati sull'ordinata y."""
    fb = font(dim, True)
    dr.text((x, y), etichetta + ' : ', font=fb, fill=NERO, anchor='lm')
    xv = x + dr.textlength(etichetta + ' : ', font=fb)
    dr.text((xv, y), valore, font=font(dim), fill=colore, anchor='lm')
    return xv + dr.textlength(valore, font=font(dim))


def legenda(dr, x0, y0, x1, y1, testo, dim=24):
    """Riquadro con la legenda che interrompe il bordo superiore, come i fieldset di SIPO."""
    dr.line((x0, y0, x0, y1), fill=BORDO, width=1)
    dr.line((x0, y1, x1, y1), fill=BORDO, width=1)
    f = font(dim)
    w = dr.textlength(testo, font=f)
    dr.line((x0, y0, x0 + 8, y0), fill=BORDO, width=1)
    dr.line((x0 + 16 + w, y0, x1, y0), fill=BORDO, width=1)
    dr.text((x0 + 12, y0), testo, font=f, fill=GRIGIO, anchor='lm')


# ================================================================ schermata 1
def riepilogo():
    im = Image.open(os.path.join(SRC, 'sipo_riepilogo_morte_abitazione.png')).convert('RGB')
    h = 80
    im = inserisci(im, 72, h)
    dr = ImageDraw.Draw(im)
    banner(dr, (30, 86, 1807, 72 + h - 10), AVVISO_FONDO, AVVISO_BORDO, 'Attenzione:', MESSAGGIO)
    pastiglia(dr, (30, 86), 1)

    y0, y1 = 695 + h, 739 + h
    cancella(dr, (1660, y0 - 5, 1810, y1 + 5))
    bottone(dr, (1680, y0, 1789, y1), 'CONFERMA', attivo=False)
    pastiglia(dr, (1789, y0), 2)
    bottone(dr, (1478, y0, 1650, y1), 'DATI PER ANSC')
    pastiglia(dr, (1478, y0), 3)
    return im


# ================================================================ schermata 2
def anteprima():
    im = Image.open(os.path.join(SRC, 'sipo_anteprima_morte_abitazione.png')).convert('RGB')
    im = im.crop((0, 0, 1897, 1000))                 # via la barra di scorrimento
    # in alto, ben visibile: il numero comunale staccato (richiesta dell'utente, 07/11/2026)
    h = 170
    im = inserisci(im, 306, h)
    dr = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 72, 320, 1825, 306 + h - 10
    dr.rectangle((x0, y0, x1, y1), fill=(255, 248, 225), outline=ROSSO, width=3)
    dr.rectangle((x0, y0, x0 + 520, y1), fill=ROSSO)
    dr.text((x0 + 30, y0 + 28), 'NUMERO COMUNALE', font=font(26, True), fill=BIANCO, anchor='lm')
    fb = font(92, True)
    dr.text((x0 + 30, y0 + 90), NUMERO, font=fb, fill=BIANCO, anchor='lm')
    dr.text((x0 + 40 + dr.textlength(NUMERO, font=fb), y0 + 104), '/ ' + ANNO,
            font=font(40, True), fill=BIANCO, anchor='lm')
    fn, fbb = font(22), font(22, True)
    dr.text((x0 + 560, y0 + 40), 'Riportare questo numero nel campo «Numero comunale» dell’atto '
            'sulla WebApp ANSC.', font=fbb, fill=NERO, anchor='lm')
    dr.text((x0 + 560, y0 + 80), 'Copiare il testo dell’atto con COPIA TESTO e incollarlo nella '
            'composizione libera.', font=fn, fill=NERO, anchor='lm')
    dr.text((x0 + 560, y0 + 118), 'Il numero è impegnato per questo atto fino al rientro in SIPO.',
            font=fn, fill=GRIGIO, anchor='lm')
    pastiglia(dr, (x0, y0), 4)

    # il numero nella testata dell'atto
    y = 484 + h
    cancella(dr, (364, y - 14, 700, y + 14))
    f = font(23)
    testo = 'Numero comunale %s' % NUMERO
    w = dr.textlength(testo, font=f)
    dr.rectangle((364, y - 14, 370 + w, y + 14), fill=(255, 241, 118))
    dr.text((367, y), testo, font=f, fill=(34, 34, 34), anchor='lm')

    # chiusura dei riquadri tagliati e barra dei bottoni
    fondo = im.height
    piede = 130
    nuovo = Image.new('RGB', (im.width, fondo + piede), BIANCO)
    nuovo.paste(im, (0, 0))
    dr = ImageDraw.Draw(nuovo)
    for x in (360, 1568):
        dr.line((x, fondo - 2, x, fondo + 12), fill=(60, 60, 60), width=2)
    dr.line((360, fondo + 12, 1568, fondo + 12), fill=(60, 60, 60), width=2)
    for x in (72, 1824):
        dr.line((x, fondo - 40, x, fondo + 34), fill=ROSSO, width=3)
    dr.line((72, fondo + 34, 1825, fondo + 34), fill=ROSSO, width=3)
    yb = fondo + 62
    bottone(dr, (72, yb, 190, yb + 48), 'INDIETRO')
    bottone(dr, (1660, yb, 1825, yb + 48), 'COPIA TESTO')
    pastiglia(dr, (1660, yb), 5)
    dr.text((1640, yb + 24), 'copia negli appunti il testo dell’atto redatto in SIPO',
            font=font(19), fill=GRIGIO, anchor='rm')
    return nuovo


# ================================================================ schermata 3
def attesa():
    im = Image.open(os.path.join(SRC, 'sipo_dettaglio_atto_decesso.png')).convert('RGB')
    dr = ImageDraw.Draw(im)

    # titolo e dati dell'atto: lo stesso atto delle prime due schermate
    cancella(dr, (40, 35, 1180, 66))
    dr.text((48, 51), 'Riepilogo Atto - Atto di Morte a Roma - Abitazione Privata',
            font=font(20, True), fill=NERO, anchor='lm')
    cancella(dr, (60, 158, 800, 330))
    campo(dr, 72, 174, 'Tipologia Atto', 'Atti di Morte a Roma - MORTE IN ABITAZIONE A ROMA')
    campo(dr, 72, 209, 'Data Atto', '07/11/2026')
    campo(dr, 370, 209, 'Orario Atto', '15:42')
    campo(dr, 72, 244, 'Stato Pratica', 'IN ATTESA ATTO ANSC', colore=(176, 96, 0))
    campo(dr, 72, 279, 'Numero Atto', '908286')
    campo(dr, 72, 314, 'Parte', '1')
    campo(dr, 255, 314, 'Esponente', '15')
    campo(dr, 482, 314, 'Anno', ANNO)
    cancella(dr, (628, 196, 800, 222))
    campo(dr, 632, 209, 'Occhio', 'Destro')

    cancella(dr, (60, 460, 1180, 670))
    campo(dr, 72, 477, 'Nominativo', 'FILIPPO GODI')
    campo(dr, 412, 477, 'Stato Civile', 'Celibe/Nubile')
    campo(dr, 72, 512, 'Nato/a il', '20/09/1964')
    campo(dr, 368, 512, 'a', 'TORRE DEL GRECO (NA)')
    campo(dr, 72, 547, 'Codice Individuale', '2568841')
    campo(dr, 72, 582, 'Luogo decesso', 'ROMA (RM)')
    campo(dr, 72, 617, 'Data Decesso', '04/11/2026')

    # avviso di attesa sotto il titolo
    h1 = 72
    im = inserisci(im, 80, h1)
    dr = ImageDraw.Draw(im)
    banner(dr, (38, 90, 1176, 80 + h1 - 6), INFO_FONDO, INFO_BORDO, 'In attesa dell’atto ANSC.',
           'Formare l’atto sulla WebApp con il numero comunale %s e il testo copiato, poi '
           'indicare qui l’idAnsc.' % NUMERO, dim=19)

    # riquadro nuovo «Atto ANSC» fra i dati dell'atto e i dati del defunto
    y = 348 + h1 + 30
    h2 = 260
    im = inserisci(im, y, h2)
    dr = ImageDraw.Draw(im)
    x0, x1, top, bot = 38, 1183, y + 22, y + h2 - 14
    legenda(dr, x0, top, x1, bot, 'Atto ANSC')
    pastiglia(dr, (x0 + 52 + dr.textlength('Atto ANSC', font=font(24)), top), 6)
    campo(dr, 72, top + 46, 'Numero comunale', NUMERO)
    campo(dr, 330, top + 46, 'Anno', ANNO)
    campo(dr, 72, top + 81, 'Testo dell’atto', 'copiato negli appunti il 07/11/2026 alle 15:58')
    xe = campo(dr, 72, top + 116, 'Stato', '')
    f = font(18, True)
    t = 'YY · SOSPESO — in attesa dell’atto formato sulla WebApp'
    w = dr.textlength(t, font=f)
    dr.rounded_rectangle((xe, top + 103, xe + w + 20, top + 129), radius=5,
                         fill=(255, 236, 179), outline=(230, 160, 0))
    dr.text((xe + 10, top + 116), t, font=f, fill=(120, 70, 0), anchor='lm')
    xi = campo(dr, 72, top + 166, 'Identificativo ANSC (idAnsc)', '')
    dr.rectangle((xi, top + 148, xi + 330, top + 184), fill=BIANCO, outline=(143, 143, 143))
    dr.text((xi + 10, top + 166), 'es. 2026-9423-124-058091', font=font(18),
            fill=(170, 170, 170), anchor='lm')
    bottone(dr, (xi + 350, top + 146, xi + 560, top + 186), 'RECUPERA ATTO ANSC', dim=16)

    # bottoni in fondo: INDIETRO resta, DOWNLOAD diventa COPIA TESTO
    yb = 743 + h1 + h2
    cancella(dr, (340, yb - 6, 1180, yb + 50))
    bottone(dr, (354, yb, 500, yb + 44), 'COPIA TESTO')
    return im


# ================================================================ sequenza
def sequenza(immagini):
    alt = 560
    pannelli = [im.resize((int(im.width * alt / im.height), alt), Image.LANCZOS) for im in immagini]
    gap, marg = 150, 40
    W = sum(p.width for p in pannelli) + gap * (len(pannelli) - 1) + 2 * marg
    tela = Image.new('RGB', (W, alt + 2 * marg + 70), BIANCO)
    dr = ImageDraw.Draw(tela)
    x = marg
    titoli = ('1-3  Riepilogo senza UC', '4-5  Anteprima con il numero comunale',
              '6  In attesa dell’atto ANSC')
    frecce = ('DATI PER ANSC', 'COPIA TESTO\n→ WebApp')
    for i, p in enumerate(pannelli):
        tela.paste(p, (x, marg + 50))
        dr.rectangle((x - 1, marg + 49, x + p.width, marg + 50 + alt), outline=(180, 180, 180))
        dr.text((x, marg + 18), titoli[i], font=font(26, True), fill=NERO, anchor='lm')
        if i < len(pannelli) - 1:
            ya = marg + 50 + alt // 2
            xa, xb = x + p.width + 15, x + p.width + gap - 15
            dr.line((xa, ya, xb - 14, ya), fill=ROSSO, width=5)
            dr.polygon([(xb, ya), (xb - 18, ya - 11), (xb - 18, ya + 11)], fill=ROSSO)
            dr.multiline_text(((xa + xb) / 2, ya - 40), frecce[i], font=font(18, True),
                              fill=ROSSO, anchor='mm', align='center')
        x += p.width + gap
    return tela


if __name__ == '__main__':
    # Le pagine 1 e 2. La pagina di attesa (attesa()) è superata dalla ricerca R005 e dal
    # riepilogo dell'atto ANSC: le genera, con la sequenza e il flusso, schermate_recupero_ansc.py.
    os.makedirs(OUT, exist_ok=True)
    for nome, im in (('tl_1_riepilogo_senza_uc.png', riepilogo()),
                     ('tl_2_anteprima_numero.png', anteprima())):
        im.save(os.path.join(OUT, nome))
        print(nome, im.size)
