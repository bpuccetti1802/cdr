# -*- coding: utf-8 -*-
"""Recupero in SIPO dell'atto formato sulla WebApp (07/11/2026, richiesta dell'utente).

Seguito di schermate_testo_libero.py (pagine 1-2: Riepilogo senza UC, Anteprima con il numero
comunale). Qui:

  3  Recupero atto ANSC — «Atti del giorno»: R005 /consultazione/ansc/evento con dataDa/dataA,
     idComuneRegistrazione (Roma = 8165 nell'archivio comuni ANPR) e idTipoEvento; R005 non ha
     un filtro di stato, quindi «stato 5» si applica in SIPO sulla risposta. L'atto con il numero
     comunale staccato è evidenziato.
  4  Recupero atto ANSC — «Ricerca puntuale», quando il numero non compare: per atto (idAnsc,
     oppure numero comunale con un intervallo di date più largo) o per intestatario
     (R005 /consultazione/ansc/soggetto/sintetico).
  5  Riepilogo atto ANSC: idAnsc, UC (codice e descrizione), intestatari essenziali, che cosa SIPO
     aggiorna alla conferma.
  6  Finestra di conferma, che aggiorna SIPO e conclude.
  +  Flusso logico (tl_flusso_recupero.png) e sequenza delle pagine (tl_sequenza.png).

Stile delle pagine nuove ricavato dalle schermate reali di SIPO: testata reale (dall'anteprima),
linguette, riquadro del modulo, tabella con intestazione rosso scuro e selezione a pulsante
radio (Gestione Decessi, `Sorgenti Documentali/Immagini sipo/Decessi/`).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_recupero_ansc.py
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_testo_libero as T          # noqa: E402
import diagrammi_comune as G                 # noqa: E402
from schermate_testo_libero import (ANNO, BIANCO, BLU, BORDO, GRIGIO, NERO, NUMERO,  # noqa: E402
                                    ROSSO, bottone, font)

W = 1600
OUT = T.OUT
ROSSO_TAB = (154, 28, 36)
GRIGIO_TAB = (108, 117, 125)
VERDE_RIGA, VERDE_BORDO = (227, 244, 230), (63, 143, 95)
AMBRA_FONDO, AMBRA_BORDO = (255, 243, 205), (230, 160, 0)
CAMPO_BORDO = (143, 143, 143)
SOLA_LETTURA = (235, 235, 228)
ID_ANSC = '2026-9423-%s-058091' % NUMERO
OGGI = '07/11/2026'


# ------------------------------------------------------------------ primitive di pagina
def pagina(altezza, titolo):
    im = Image.new('RGB', (W, altezza), BIANCO)
    testa = Image.open(os.path.join(T.SRC, 'sipo_anteprima_morte_abitazione.png')).convert('RGB')
    testa = testa.crop((0, 0, 1897, 198))
    testa = testa.resize((W, int(198 * W / 1897)), Image.LANCZOS)
    im.paste(testa, (0, 0))
    dr = ImageDraw.Draw(im)
    dr.text((60, 205), titolo, font=font(21, True), fill=NERO, anchor='lm')
    dr.line((50, 228, W - 50, 228), fill=(192, 192, 192), width=2)
    return im, dr


def striscia(dr, y, fondo, bordo, testa, testo, dim=19):
    T.banner(dr, (60, y, W - 60, y + 52), fondo, bordo, testa, testo, dim=dim)


def linguette(dr, y, voci, attiva):
    f = font(18)
    larg = [dr.textlength(v, font=f) + 40 for v in voci]
    x = (W - sum(larg) - 4 * (len(voci) - 1)) / 2
    for i, (v, w) in enumerate(zip(voci, larg)):
        dr.rectangle((x, y, x + w, y + 40), fill=ROSSO_TAB if i == attiva else GRIGIO_TAB)
        dr.text((x + w / 2, y + 20), v, font=f, fill=BIANCO, anchor='mm')
        x += w + 4
    dr.line((60, y + 40, W - 60, y + 40), fill=(220, 220, 220), width=1)


def riquadro(dr, box):
    dr.rectangle(box, outline=(120, 120, 120), width=2)


def campo(dr, x, y, etichetta, valore='', w=230, tendina=False, sola_lettura=False, segnaposto=False):
    dr.text((x, y), etichetta, font=font(18, True), fill=NERO)
    yy = y + 26
    dr.rectangle((x, yy, x + w, yy + 32), fill=SOLA_LETTURA if sola_lettura else BIANCO,
                 outline=CAMPO_BORDO)
    if valore:
        dr.text((x + 8, yy + 16), valore, font=font(17),
                fill=(160, 160, 160) if segnaposto else NERO, anchor='lm')
    if tendina:
        cx, cy = x + w - 16, yy + 16
        dr.line((cx - 6, cy - 3, cx, cy + 3, cx + 6, cy - 3), fill=NERO, width=2)


def tabella(dr, x, y, colonne, righe, evidenzia=None, selezionata=None, ambra=None, h=40):
    tot = sum(c[1] for c in colonne)
    dr.rectangle((x, y, x + tot, y + h), fill=ROSSO_TAB)
    cx = x
    for nome, w in colonne:
        dr.text((cx + w / 2, y + h / 2), nome, font=font(16, True), fill=BIANCO, anchor='mm')
        cx += w
    for i, riga in enumerate(righe):
        yy = y + h * (i + 1)
        fondo = VERDE_RIGA if i == evidenzia else (AMBRA_FONDO if i == ambra else BIANCO)
        dr.rectangle((x, yy, x + tot, yy + h), fill=fondo, outline=(60, 60, 60))
        cx = x
        for j, (val, (_, w)) in enumerate(zip([''] + list(riga), colonne)):
            if j == 0:
                r = 9
                dr.ellipse((cx + w / 2 - r, yy + h / 2 - r, cx + w / 2 + r, yy + h / 2 + r),
                           outline=(110, 110, 110), width=2, fill=BIANCO)
                if i == selezionata:
                    dr.ellipse((cx + w / 2 - 5, yy + h / 2 - 5, cx + w / 2 + 5, yy + h / 2 + 5),
                               fill=(30, 110, 230))
            else:
                f = font(16, True) if i == evidenzia else font(16)
                dr.text((cx + w / 2, yy + h / 2), val, font=f, fill=NERO, anchor='mm')
            dr.line((cx, yy, cx, yy + h), fill=(60, 60, 60))
            cx += w
        dr.line((cx, yy, cx, yy + h), fill=(60, 60, 60))
        if i == evidenzia:
            dr.rectangle((x, yy, x + 6, yy + h), fill=VERDE_BORDO)
    return y + h * (len(righe) + 1)


def nota(dr, x, y, testo, colore=GRIGIO, dim=16):
    dr.text((x, y), testo, font=font(dim), fill=colore, anchor='lm')


def legenda_sipo(dr, x0, y0, x1, y1, testo):
    T.legenda(dr, x0, y0, x1, y1, testo)
    dr.line((x1, y0, x1, y1), fill=BORDO, width=1)


INFO = ('In attesa dell’atto ANSC.',
        'Numero comunale %s / %s · intestatario FILIPPO GODI, nato il 20/09/1964 · atto SIPO '
        'nello stato YY · SOSPESO.' % (NUMERO, ANNO))
TITOLO = 'Recupero Atto ANSC - Atto di Morte a Roma - Abitazione Privata'

COLONNE = [('', 50), ('Identificativo ANSC', 220), ('Numero comunale', 130),
           ('Formazione', 150), ('Caso d’uso', 400), ('Intestatario', 190),
           ('Data nascita', 120), ('Stato', 220)]


# ================================================================ pagina 3
def atti_del_giorno():
    im, dr = pagina(1010, TITOLO)
    striscia(dr, 245, T.INFO_FONDO, T.INFO_BORDO, *INFO)
    linguette(dr, 318, ('Atti del giorno', 'Ricerca puntuale'), 0)
    riquadro(dr, (240, 378, 1360, 548))
    campo(dr, 270, 392, 'Data da', OGGI)
    campo(dr, 640, 392, 'Data a', OGGI)
    campo(dr, 1010, 392, 'Comune di registrazione', 'ROMA (RM)', w=320, sola_lettura=True)
    campo(dr, 270, 466, 'Tipo evento', 'MORTE', tendina=True)
    campo(dr, 640, 466, 'Stato', '5 - FIRMATO DA USC', tendina=True)
    campo(dr, 1010, 466, 'Numero comunale atteso', NUMERO, w=320, sola_lettura=True)
    bottone(dr, (1180, 562, 1262, 604), 'CERCA')
    bottone(dr, (1270, 562, 1360, 604), 'ANNULLA')
    nota(dr, 240, 583, 'R005 /consultazione/ansc/evento: dataDa, dataA, idComuneRegistrazione '
                       '8165, idTipoEvento 2 · lo stato si filtra in SIPO sulla risposta')
    dr.line((60, 625, W - 60, 625), fill=(192, 192, 192), width=2)

    righe = [
        ('2026-9419-119-058091', '119', OGGI + ' 09:12', '2102 Decesso in ospedale o casa di cura',
         'ROSSI CORRADO', '01/10/1900', '5 - FIRMATO DA USC'),
        ('2026-9420-120-058091', '120', OGGI + ' 10:05',
         '2101 Decesso in abitazione o in luogo pubblico', 'NICOLUCCI DAVID', '04/12/1982',
         '5 - FIRMATO DA USC'),
        ('2026-9421-122-058091', '122', OGGI + ' 11:40', '2102 Decesso in ospedale o casa di cura',
         'VERDI PAOLO', '01/10/2000', '5 - FIRMATO DA USC'),
        (ID_ANSC, NUMERO, OGGI + ' 16:20', '2199 Caso d’uso di servizio (dich. di morte)',
         'GODI FILIPPO', '20/09/1964', '5 - FIRMATO DA USC'),
        ('2026-9424-125-058091', '125', OGGI + ' 16:48',
         '2101 Decesso in abitazione o in luogo pubblico', 'ABATE ROSANNA', '27/12/1961',
         '5 - FIRMATO DA USC'),
    ]
    fine = tabella(dr, 60, 650, COLONNE, righe, evidenzia=3, selezionata=3)
    dr.rounded_rectangle((60, fine + 14, 74, fine + 28), radius=3, fill=VERDE_RIGA,
                         outline=VERDE_BORDO, width=2)
    nota(dr, 84, fine + 21, '5 atti firmati il %s · evidenziato l’atto con il numero comunale %s, '
                            'già selezionato' % (OGGI, NUMERO), colore=NERO)
    yb = fine + 62
    bottone(dr, (60, yb, 180, yb + 46), 'INDIETRO')
    bottone(dr, (1250, yb, 1420, yb + 46), 'RICERCA PUNTUALE')
    bottone(dr, (1430, yb, 1540, yb + 46), 'SELEZIONA')
    return im


# ================================================================ pagina 4
def ricerca_puntuale():
    im, dr = pagina(1000, TITOLO)
    striscia(dr, 245, T.AVVISO_FONDO, T.AVVISO_BORDO, 'Numero comunale non trovato.',
             'Fra gli atti firmati il %s nessuno porta il numero comunale %s: cercare l’atto con '
             'uno dei criteri seguenti.' % (OGGI, NUMERO))
    linguette(dr, 318, ('Atti del giorno', 'Ricerca puntuale'), 1)

    legenda_sipo(dr, 100, 400, 780, 610, 'Per atto')
    campo(dr, 130, 425, 'Identificativo ANSC', 'es. 2026-9423-124-058091', w=330, segnaposto=True)
    nota(dr, 130, 505, 'oppure', colore=NERO)
    campo(dr, 130, 525, 'Numero comunale', NUMERO, w=150)
    campo(dr, 310, 525, 'Data da', '01/11/2026', w=180)
    campo(dr, 520, 525, 'Data a', '08/11/2026', w=180)

    legenda_sipo(dr, 820, 400, 1500, 610, 'Per intestatario')
    campo(dr, 850, 425, 'Cognome', 'GODI', w=290)
    campo(dr, 1170, 425, 'Nome', 'FILIPPO', w=290)
    campo(dr, 850, 525, 'Data di nascita', '20/09/1964', w=290)
    campo(dr, 1170, 525, 'Codice fiscale', '', w=290)

    bottone(dr, (1320, 626, 1402, 668), 'CERCA')
    bottone(dr, (1410, 626, 1500, 668), 'ANNULLA')
    nota(dr, 100, 638, 'Per atto: R005 /consultazione/ansc/evento con idAnsc, oppure idComunale e '
                       'date', dim=15)
    nota(dr, 100, 660, 'Per intestatario: R005 /consultazione/ansc/soggetto/sintetico', dim=15)
    dr.line((60, 690, W - 60, 690), fill=(192, 192, 192), width=2)

    righe = [(ID_ANSC, NUMERO, '08/11/2026 00:05', '2199 Caso d’uso di servizio (dich. di morte)',
              'GODI FILIPPO', '20/09/1964', '5 - FIRMATO DA USC')]
    fine = tabella(dr, 60, 712, COLONNE, righe, evidenzia=0, selezionata=0)
    nota(dr, 60, fine + 22, 'Trovato per intestatario: l’atto è stato chiuso dopo la mezzanotte, '
                            'fuori dall’intervallo degli atti del giorno.', colore=NERO)
    yb = fine + 62
    bottone(dr, (60, yb, 180, yb + 46), 'INDIETRO')
    bottone(dr, (1430, yb, 1540, yb + 46), 'SELEZIONA')
    return im


# ================================================================ pagina 5
def riepilogo_ansc():
    im, dr = pagina(1240, 'Riepilogo Atto ANSC - Atto di Morte a Roma - Abitazione Privata')
    striscia(dr, 245, T.OK_FONDO, T.OK_BORDO, 'Atto ANSC trovato.',
             'Verificare i dati e confermare: SIPO li registra sull’atto e conclude l’operazione.')

    legenda_sipo(dr, 60, 340, W - 60, 520, 'Atto ANSC')
    T.campo(dr, 90, 382, 'Identificativo ANSC', ID_ANSC, dim=20)
    T.campo(dr, 640, 382, 'Stato', '5 - FIRMATO DA USC', dim=20)
    xe = T.campo(dr, 90, 422, 'Numero comunale', NUMERO, dim=20)
    f = font(17, True)
    t = 'corrisponde al numero staccato'
    dr.rounded_rectangle((xe + 14, 409, xe + 54 + dr.textlength(t, font=f), 435), radius=5,
                         fill=VERDE_RIGA, outline=VERDE_BORDO)
    dr.line((xe + 24, 422, xe + 30, 428, xe + 41, 414), fill=(30, 100, 50), width=3)
    dr.text((xe + 46, 422), t, font=f, fill=(30, 100, 50), anchor='lm')
    T.campo(dr, 640, 422, 'Anno', ANNO, dim=20)
    T.campo(dr, 90, 462, 'Data formazione', OGGI, dim=20)
    T.campo(dr, 400, 462, 'Ora', '16:20', dim=20)
    T.campo(dr, 640, 462, 'Comune di registrazione', 'ROMA (RM)', dim=20)

    legenda_sipo(dr, 60, 565, W - 60, 705, 'Caso d’uso')
    T.campo(dr, 90, 607, 'Codice', '2199', dim=20)
    T.campo(dr, 400, 607, 'Descrizione', 'Caso d’uso di servizio (dichiarazioni di morte)', dim=20)
    T.campo(dr, 90, 647, 'Motivo del recupero', '3 - Caso d’uso non previsto nel sistema centrale',
            dim=20)

    legenda_sipo(dr, 60, 750, W - 60, 900, 'Intestatari')
    col = [('', 0), ('Cognome', 180), ('Nome', 180), ('Sesso', 80), ('Data nascita', 140),
           ('Luogo di nascita', 300), ('Cittadinanza', 160), ('Id ANSC soggetto', 190)]
    righe = [('GODI', 'FILIPPO', 'M', '20/09/1964', 'TORRE DEL GRECO (NA)', 'ITALIANA', '245912')]
    _tabella_senza_selezione(dr, 90, 790, col[1:], righe)

    legenda_sipo(dr, 60, 945, W - 60, 1130, 'Alla conferma SIPO aggiorna')
    voci = ('l’atto SIPO: identificativo ANSC, anno, numero comunale e data di formazione;',
            'lo stato ANSC dell’atto (5 FIRMATO DA USC) e il contrassegno di atto a testo libero;',
            'il numero comunale %s: da Disponibile a Utilizzato, con l’identificativo ANSC;' % NUMERO,
            'gli identificativi dei soggetti, in anagrafe solo dove mancano.')
    for i, v in enumerate(voci):
        dr.text((95, 985 + i * 34), '•  ' + v, font=font(19), fill=NERO, anchor='lm')

    yb = 1160
    bottone(dr, (60, yb, 180, yb + 46), 'INDIETRO')
    bottone(dr, (1420, yb, 1540, yb + 46), 'CONFERMA')
    return im


def _tabella_senza_selezione(dr, x, y, colonne, righe, h=40):
    tot = sum(w for _, w in colonne)
    dr.rectangle((x, y, x + tot, y + h), fill=ROSSO_TAB)
    cx = x
    for nome, w in colonne:
        dr.text((cx + w / 2, y + h / 2), nome, font=font(16, True), fill=BIANCO, anchor='mm')
        cx += w
    for i, riga in enumerate(righe):
        yy = y + h * (i + 1)
        dr.rectangle((x, yy, x + tot, yy + h), fill=BIANCO, outline=(60, 60, 60))
        cx = x
        for val, (_, w) in zip(riga, colonne):
            dr.text((cx + w / 2, yy + h / 2), val, font=font(16), fill=BLU, anchor='mm')
            dr.line((cx, yy, cx, yy + h), fill=(60, 60, 60))
            cx += w


# ================================================================ pagina 6
def conferma(base):
    im = base.copy().convert('RGBA')
    velo = Image.new('RGBA', im.size, (0, 0, 0, 110))
    im = Image.alpha_composite(im, velo).convert('RGB')
    dr = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 420, 460, 1180, 760
    dr.rectangle((x0, y0, x1, y1), fill=BIANCO, outline=(120, 120, 120))
    dr.rectangle((x0, y0, x1, y0 + 52), fill=ROSSO)
    dr.text((x0 + 24, y0 + 26), 'Conferma aggiornamento', font=font(22, True), fill=BIANCO,
            anchor='lm')
    righe = ('Aggiornare l’atto SIPO con l’atto ANSC',
             ID_ANSC + ' (numero comunale %s / %s)?' % (NUMERO, ANNO),
             '',
             'L’operazione conclude l’atto in SIPO.')
    for i, r in enumerate(righe):
        dr.text((x0 + 30, y0 + 90 + i * 32), r, font=font(21, i == 1), fill=NERO, anchor='lm')
    bottone(dr, (x1 - 280, y1 - 66, x1 - 160, y1 - 22), 'ANNULLA')
    bottone(dr, (x1 - 150, y1 - 66, x1 - 30, y1 - 22), 'CONFERMA')
    return im


# ================================================================ flusso logico
def flusso():
    im, dr = G.tela(1760, 2060, 'Atto senza UC: dalla WebApp ANSC al recupero in SIPO',
                    'Pagine di SIPO, servizi chiamati e decisioni; in viola il lavoro sulla WebApp')
    cx, bw, bh = 560, 520, 86
    sx = 1060                                    # colonna dei servizi
    rx = 1300                                    # colonna della ricerca puntuale

    def passo(y, colore, titolo, sotto=None, x=None, w=bw, h=bh):
        x = cx - w / 2 if x is None else x
        G.box(dr, x, y, w, h, colore, titolo, sotto, ts=19, ss=15)
        return (x, y, w, h)

    def servizio(y, testo, da_x=cx + bw / 2):
        G.box(dr, sx, y + 12, 300, 62, 'grigio', testo, ts=14)
        G.linea(dr, [(da_x, y + bh / 2), (sx, y + bh / 2)], tratteggio=True, larg=2)

    y = 110
    passo(y, 'blu', '1 · Riepilogo (fase B)', 'determinazione dell’UC')
    G.rombo(dr, cx, y + 190, 300, 120, 'UC identificato?', ts=19)
    G.freccia(dr, (cx, y + bh), (cx, y + 130))
    G.box(dr, cx + 260, y + 155, 260, 70, 'grigio', 'Percorso ordinario', 'firmatari, allegati, R009…',
          ts=17, ss=14)
    G.freccia(dr, (cx + 150, y + 190), (cx + 260, y + 190))
    G.centra(dr, 'sì', G.fnt(G.F_REG, 15), cx + 190, y + 166, G.ARROW)

    y2 = y + 300
    G.freccia(dr, (cx, y + 250), (cx, y2))
    G.centra(dr, 'no', G.fnt(G.F_REG, 15), cx + 22, y + 262, G.ARROW)
    passo(y2, 'rosso', '1-2 · Messaggio di rinvio alla WebApp', 'CONFERMA inibito')
    y3 = y2 + 140
    G.freccia(dr, (cx, y2 + bh), (cx, y3))
    passo(y3, 'blu', '3 · DATI PER ANSC', 'stacco del numero comunale')
    servizio(y3, 'be-numeratore-comunale · POST /richiesta')
    y4 = y3 + 140
    G.freccia(dr, (cx, y3 + bh), (cx, y4))
    passo(y4, 'blu', '4-5 · Anteprima: NUMERO COMUNALE in alto', 'COPIA TESTO negli appunti')
    y5 = y4 + 140
    G.freccia(dr, (cx, y4 + bh), (cx, y5))
    passo(y5, 'giallo', 'Atto SIPO in YY · SOSPESO', 'numero comunale: Disponibile')
    y6 = y5 + 140
    G.freccia(dr, (cx, y5 + bh), (cx, y6))
    passo(y6, 'viola', 'WebApp ANSC: stesura e firme',
          'UC di servizio · numero comunale · testo incollato → 5 FIRMATO DA USC', h=96)
    y7 = y6 + 150
    G.freccia(dr, (cx, y6 + 96), (cx, y7))
    passo(y7, 'blu', '6 · Recupero: atti del giorno', 'evidenziato il numero comunale staccato')
    servizio(y7, 'R005 /consultazione/ansc/evento · dataDa, dataA, comune 8165, tipo evento')
    nota_y = y7 + bh + 6
    G.centra(dr, 'stato 5 filtrato in SIPO: R005 non ha il criterio', G.fnt(G.F_ITA, 14), cx, nota_y,
             G.MUTED)
    yd = y7 + 210
    G.freccia(dr, (cx, y7 + bh + 28), (cx, yd - 60))
    G.rombo(dr, cx, yd, 300, 120, 'Numero comunale trovato?', ts=18)

    # ramo «no»: ricerca puntuale
    G.box(dr, rx - 200, yd - 43, 400, bh, 'blu', 'Ricerca puntuale',
          'per atto (idAnsc, numero e date) · per intestatario', ts=19, ss=15)
    G.freccia(dr, (cx + 150, yd), (rx - 200, yd))
    G.centra(dr, 'no', G.fnt(G.F_REG, 15), cx + 175, yd - 24, G.ARROW)
    G.box(dr, rx - 200, yd + 70, 400, 62, 'grigio',
          'R005 evento (idAnsc / idComunale) · R005 soggetto/sintetico', ts=14)
    G.rombo(dr, rx, yd + 250, 280, 110, 'Trovato?', ts=18)
    G.freccia(dr, (rx, yd + 132), (rx, yd + 195))
    bx = rx + 175
    G.box(dr, bx, yd + 205, 270, 96, 'giallo', 'Resta in YY · SOSPESO',
          'si riprova più tardi; il back-office ne segnala l’anzianità', ts=17, ss=13)
    G.freccia(dr, (rx + 140, yd + 250), (bx, yd + 250))
    G.centra(dr, 'no', G.fnt(G.F_REG, 15), rx + 158, yd + 222, G.ARROW)
    G.percorso(dr, [(bx + 135, yd + 205), (bx + 135, y7 + 80), (cx + bw / 2, y7 + 80)],
               tratteggio=True, larg=2)
    G.centra(dr, 'nuova ricerca', G.fnt(G.F_REG, 14), bx + 70, y7 + 92, G.ARROW)

    # ramo «sì»: riepilogo, conferma, aggiornamento
    yr = yd + 150
    G.freccia(dr, (cx, yd + 60), (cx, yr))
    G.centra(dr, 'sì', G.fnt(G.F_REG, 15), cx + 22, yd + 80, G.ARROW)
    passo(yr, 'blu', 'Riepilogo atto ANSC', 'idAnsc · UC (codice e descrizione) · intestatari')
    G.percorso(dr, [(rx - 140, yd + 250), (cx + bw / 2, yr + bh / 2)])
    G.centra(dr, 'sì', G.fnt(G.F_REG, 15), rx - 190, yd + 222, G.ARROW)
    yc = yr + 140
    G.freccia(dr, (cx, yr + bh), (cx, yc))
    passo(yc, 'rosso', 'CONFERMA', 'finestra di conferma')
    yu = yc + 140
    G.freccia(dr, (cx, yc + bh), (cx, yu))
    passo(yu, 'verde', 'Aggiornamento di SIPO', 'atto · stato 5 · testo libero · numero Utilizzato '
                                                '· identificativi dei soggetti', h=96)
    servizio(yu, 'be-numeratore-comunale · PUT /utilizza')
    yf = yu + 150
    G.freccia(dr, (cx, yu + 96), (cx, yf))
    passo(yf, 'verde', 'Atto concluso in SIPO', 'stato finale dell’atto SIPO: TL-04', h=76)

    G.legenda(dr, 120, 2010, [('blu', 'pagina SIPO'), ('rosso', 'messaggio o conferma'),
                              ('giallo', 'stato in attesa'), ('viola', 'WebApp ANSC'),
                              ('grigio', 'servizio chiamato'), ('verde', 'aggiornamento e fine')])
    return im


# ================================================================ sequenza
def sequenza(immagini, titoli, frecce):
    alt = 520
    pann = [im.resize((int(im.width * alt / im.height), alt), Image.LANCZOS) for im in immagini]
    gap, marg = 120, 40
    larg = sum(p.width for p in pann) + gap * (len(pann) - 1) + 2 * marg
    tela = Image.new('RGB', (larg, alt + 2 * marg + 70), BIANCO)
    dr = ImageDraw.Draw(tela)
    x = marg
    for i, p in enumerate(pann):
        tela.paste(p, (x, marg + 50))
        dr.rectangle((x - 1, marg + 49, x + p.width, marg + 50 + alt), outline=(180, 180, 180))
        dr.text((x, marg + 18), titoli[i], font=font(24, True), fill=NERO, anchor='lm')
        if i < len(pann) - 1:
            ya = marg + 50 + alt // 2
            xa, xb = x + p.width + 12, x + p.width + gap - 12
            dr.line((xa, ya, xb - 14, ya), fill=ROSSO, width=5)
            dr.polygon([(xb, ya), (xb - 18, ya - 11), (xb - 18, ya + 11)], fill=ROSSO)
            dr.multiline_text(((xa + xb) / 2, ya - 44), frecce[i], font=font(16, True),
                              fill=ROSSO, anchor='mm', align='center')
        x += p.width + gap
    return tela


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    p1, p2 = T.riepilogo(), T.anteprima()
    p3, p4, p5 = atti_del_giorno(), ricerca_puntuale(), riepilogo_ansc()
    p6 = conferma(p5)
    uscite = (('tl_1_riepilogo_senza_uc.png', p1), ('tl_2_anteprima_numero.png', p2),
              ('tl_3_recupero_atti_del_giorno.png', p3), ('tl_4_recupero_ricerca_puntuale.png', p4),
              ('tl_5_riepilogo_atto_ansc.png', p5), ('tl_6_conferma.png', p6),
              ('tl_flusso_recupero.png', flusso()))
    for nome, im in uscite:
        im.save(os.path.join(OUT, nome))
        print(nome, im.size)
    sequenza([p1, p2, p3, p5, p6],
             ('1-3 Riepilogo senza UC', '4-5 Anteprima', '6 Atti del giorno', 'Riepilogo ANSC',
              'Conferma'),
             ('DATI PER\nANSC', 'COPIA TESTO\n→ WebApp\n→ rientro', 'SELEZIONA', 'CONFERMA')
             ).save(os.path.join(OUT, 'tl_sequenza.png'))
    vecchia = os.path.join(OUT, 'tl_3_attesa_atto_ansc.png')
    if os.path.exists(vecchia):
        os.remove(vecchia)
    print('tl_sequenza.png')
