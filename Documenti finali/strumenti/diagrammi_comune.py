# -*- coding: utf-8 -*-
"""Primitive di disegno per i diagrammi del documento di analisi.

Stile: riquadri arrotondati con bordo colorato e riempimento tenue, titolo in grassetto e
sottotitolo grigio, frecce grigie, legenda in basso. Tutti i diagrammi del documento sono
prodotti con queste primitive: usarle mantiene le figure coerenti fra loro.

NOTA IMPORTANTE PER CHI SCRIVE I TESTI
Le stringhe di testo visualizzato usano il DOPPIO APICE come delimitatore, così l'apostrofo
tipografico italiano (U+2019) può comparire liberamente. I marcatori markdown non esistono
qui: il grassetto si ottiene scegliendo il font, non scrivendo asterischi.

Questo file sta in «Documenti finali/strumenti/» e non nello scratchpad, che è di sessione e
viene ripulito: nell'agosto 2026 la ripulitura ha fatto perdere tutti i generatori.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont  # noqa: F401  (Image serve ai chiamanti)

FONT_DIR = '/System/Library/Fonts/Supplemental'
F_REG = os.path.join(FONT_DIR, 'Arial.ttf')
F_BLD = os.path.join(FONT_DIR, 'Arial Bold.ttf')
F_ITA = os.path.join(FONT_DIR, 'Arial Italic.ttf')

C = {
    'grigio': ('#6b7280', '#e9eaec'),
    'blu': ('#2f6bb0', '#dbe6f5'),
    'rosso': ('#b03a48', '#f6dfe1'),
    'giallo': ('#d9a441', '#fdf1d6'),
    'verde': ('#3f8f5f', '#dcefe1'),
    'viola': ('#7b5aa6', '#ece5f5'),
}
INK = '#1f2937'
MUTED = '#6b7280'
ARROW = '#4b5563'


def fnt(path, size):
    return ImageFont.truetype(path, size)


def larghezza(dr, txt, font):
    return dr.textbbox((0, 0), txt, font=font)[2]


def centra(dr, txt, font, cx, y, fill=INK):
    dr.text((cx - larghezza(dr, txt, font) / 2, y), txt, font=font, fill=fill)


def avvolgi(dr, txt, font, larg):
    righe, corrente = [], ''
    for parola in txt.split():
        prova = (corrente + ' ' + parola).strip()
        if larghezza(dr, prova, font) <= larg or not corrente:
            corrente = prova
        else:
            righe.append(corrente)
            corrente = parola
    if corrente:
        righe.append(corrente)
    return righe


def box(dr, x, y, w, h, colore, titolo, sotto=None, r=14, ts=21, ss=16):
    """Riquadro con titolo e sottotitolo, entrambi centrati e mandati a capo da soli."""
    bordo, fondo = C[colore]
    dr.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fondo, outline=bordo, width=3)
    f_tit, f_sot = fnt(F_BLD, ts), fnt(F_REG, ss)
    righe_t = avvolgi(dr, titolo, f_tit, w - 26)
    righe_s = avvolgi(dr, sotto, f_sot, w - 26) if sotto else []
    ht = len(righe_t) * (ts + 5)
    hs = len(righe_s) * (ss + 4)
    cy = y + (h - ht - hs - (6 if righe_s else 0)) / 2
    for rg in righe_t:
        centra(dr, rg, f_tit, x + w / 2, cy)
        cy += ts + 5
    if righe_s:
        cy += 6
        for rg in righe_s:
            centra(dr, rg, f_sot, x + w / 2, cy, MUTED)
            cy += ss + 4


def scheda(dr, x, y, w, colore, titolo, righe, nota=None, ts=17, cs=14, hh=None):
    """Riquadro «a scheda»: intestazione colorata, poi righe (etichetta, testo).

    È la forma usata dagli schemi entità-relazioni: l'etichetta è PK/UK/FK o vuota.
    """
    bordo, fondo = C[colore]
    h = hh or (34 + len(righe) * 19 + (20 if nota else 0) + 10)
    dr.rounded_rectangle([x, y, x + w, y + h], radius=9, fill='white', outline=bordo, width=3)
    dr.rounded_rectangle([x, y, x + w, y + 30], radius=9, fill=fondo, outline=bordo, width=3)
    dr.rectangle([x + 2, y + 22, x + w - 2, y + 30], fill=fondo)
    centra(dr, titolo, fnt(F_BLD, ts), x + w / 2, y + 6, INK)
    yy = y + 36
    for etichetta, testo in righe:
        dr.text((x + 10, yy), etichetta, font=fnt(F_BLD, 13), fill=bordo)
        dr.text((x + 40, yy), testo, font=fnt(F_REG, cs), fill=INK)
        yy += 19
    if nota:
        dr.text((x + 10, yy + 2), nota, font=fnt(F_ITA, 13), fill=MUTED)
    return (x, y, x + w, y + h)


def pila(dr, x, y, w, h, colore, righe_grassetto, righe_normali, righe_corsive=(),
         bordo_col=None, fondo_col=None):
    """Riquadro con più righe centrate, in tre stili: per i diagrammi «a colonne»."""
    bordo, fondo = C[colore]
    dr.rounded_rectangle([x, y, x + w, y + h], radius=10,
                         fill=fondo_col or fondo, outline=bordo_col or bordo, width=3)
    yy = y + 12
    for rg in righe_grassetto:
        centra(dr, rg, fnt(F_BLD, 17), x + w / 2, yy, INK)
        yy += 21
    yy += 4
    for rg in righe_normali:
        centra(dr, rg, fnt(F_REG, 14), x + w / 2, yy, MUTED)
        yy += 18
    if righe_corsive:
        yy += 4
        for rg in righe_corsive:
            centra(dr, rg, fnt(F_ITA, 14), x + w / 2, yy, bordo)
            yy += 18


def rombo(dr, cx, cy, w, h, testo, ts=20):
    bordo, fondo = C['giallo']
    dr.polygon([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
               fill=fondo, outline=bordo)
    for d in range(3):
        dr.polygon([(cx, cy - h / 2 + d), (cx + w / 2 - d, cy),
                    (cx, cy + h / 2 - d), (cx - w / 2 + d, cy)], outline=bordo)
    f = fnt(F_BLD, ts)
    righe = avvolgi(dr, testo, f, w - 70)
    cyy = cy - len(righe) * (ts + 4) / 2
    for rg in righe:
        centra(dr, rg, f, cx, cyy)
        cyy += ts + 4


def punta(dr, p, ang, colore, larg=3, l=11):
    for s in (2.6, -2.6):
        dr.line([p[0], p[1], p[0] + l * math.cos(ang + s), p[1] + l * math.sin(ang + s)],
                fill=colore, width=larg)


def segmento(dr, p1, p2, colore, tratteggio, larg):
    x1, y1 = p1
    x2, y2 = p2
    if not tratteggio:
        dr.line([x1, y1, x2, y2], fill=colore, width=larg)
        return
    d = math.hypot(x2 - x1, y2 - y1)
    n = max(int(d // 13), 1)
    for i in range(n):
        if i % 2:
            continue
        a, b = i / n, min((i + 1) / n, 1)
        dr.line([x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                 x1 + (x2 - x1) * b, y1 + (y2 - y1) * b], fill=colore, width=larg)


def linea(dr, punti, colore=ARROW, tratteggio=False, larg=3):
    """Polilinea SENZA punta: per i tratti che confluiscono in un percorso comune."""
    for i in range(len(punti) - 1):
        segmento(dr, punti[i], punti[i + 1], colore, tratteggio, larg)


def percorso(dr, punti, colore=ARROW, tratteggio=False, larg=3, etichetta=None, pos=None,
             ts=13):
    """Polilinea con una sola punta in fondo; l'etichetta si posiziona a mano."""
    linea(dr, punti, colore, tratteggio, larg)
    a, b = punti[-2], punti[-1]
    punta(dr, b, math.atan2(b[1] - a[1], b[0] - a[0]), colore, larg)
    if etichetta and pos:
        centra(dr, etichetta, fnt(F_REG, ts), pos[0], pos[1], colore)


def freccia(dr, p1, p2, colore=ARROW, larg=3, etichetta=None, dy=-16):
    percorso(dr, [p1, p2], colore, larg=larg)
    if etichetta:
        centra(dr, etichetta, fnt(F_REG, 13), (p1[0] + p2[0]) / 2,
               (p1[1] + p2[1]) / 2 + dy, colore)


def banda(dr, x1, y1, x2, y2, colore_bordo, titolo, colore_testo, ts=18):
    dr.rounded_rectangle([x1, y1, x2, y2], radius=14, outline=colore_bordo, width=2)
    dr.text((x1 + 16, y1 + 8), titolo, font=fnt(F_BLD, ts), fill=colore_testo)


def legenda(dr, x, y, voci, ss=16):
    f = fnt(F_REG, ss)
    cx = x
    for colore, etichetta in voci:
        bordo, fondo = C[colore]
        dr.rounded_rectangle([cx, y, cx + 26, y + 17], radius=4, fill=fondo,
                             outline=bordo, width=2)
        dr.text((cx + 34, y - 1), etichetta, font=f, fill=MUTED)
        cx += 34 + larghezza(dr, etichetta, f) + 34


def tela(larghezza_px, altezza_px, titolo, sottotitolo=None):
    """Crea l'immagine con titolo e sottotitolo già impaginati."""
    im = Image.new('RGB', (larghezza_px, altezza_px), 'white')
    dr = ImageDraw.Draw(im)
    centra(dr, titolo, fnt(F_BLD, 27), larghezza_px / 2, 20, '#1b3a5c')
    if sottotitolo:
        centra(dr, sottotitolo, fnt(F_ITA, 16), larghezza_px / 2, 56, MUTED)
    return im, dr
