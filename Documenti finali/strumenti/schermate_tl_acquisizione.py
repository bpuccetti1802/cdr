# -*- coding: utf-8 -*-
"""Le pagine dell'ACQUISIZIONE in SIPO di un atto formato interamente sulla WebApp
(13/11/2026, v0.7 dell'analisi sugli atti a testo libero, §5.2).

Il caso: l'atto nasce e si chiude sulla WebApp senza essere mai cominciato in SIPO. Il numero
comunale l'ufficiale lo ha staccato PRIMA della stesura, dalla pagina di richiesta del
back-office o con POST /richiesta di be-numeratore-comunale (documento di processo della
numerazione comunale v0.5). In SIPO quindi c'è il numero, non l'atto.

Le schermate del recupero della v0.5/v0.6 (tl_3…tl_6) erano disegnate per l'atto cominciato in
SIPO («In attesa dell'atto ANSC… stato YY · SOSPESO», «Numero comunale atteso», «Aggiornare
l'atto SIPO»). Qui si ridisegnano per l'acquisizione:

  tl_7_acq_periodo.png    — «Recupero Atto ANSC», linguetta «Per periodo»: R005 evento con il
                            periodo, il comune e il tipo evento; SIPO calcola la colonna «In SIPO»
  tl_8_acq_ricerca.png    — linguetta «Ricerca puntuale»: per atto o per intestatario
  tl_9_acq_riepilogo.png  — «Acquisizione Atto ANSC»: dati letti, tipo atto SIPO proposto,
                            che cosa SIPO scrive, ACQUISISCI
  tl_10_acq_conferma.png  — la finestra di conferma

I file tl_3…tl_6 non si toccano: restano come storia delle versioni precedenti.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_tl_acquisizione.py
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_recupero_ansc as R          # noqa: E402
import schermate_testo_libero as T           # noqa: E402
from schermate_testo_libero import ANNO, BIANCO, NERO, NUMERO, ROSSO, bottone, font  # noqa: E402

OUT = T.OUT
W = R.W
OGGI = R.OGGI
ID_ANSC = R.ID_ANSC
TITOLO = 'Recupero Atto ANSC - Atti formati sulla WebApp'

COLONNE = [('', 50), ('Identificativo ANSC', 215), ('N. comunale', 110), ('Formazione', 150),
           ('Caso d’uso', 370), ('Intestatario', 175), ('Data nascita', 115),
           ('In SIPO', 255)]


def _bollino(dr, x, y, testo, fondo, bordo, colore):
    f = font(16, True)
    w = dr.textlength(testo, font=f)
    dr.rounded_rectangle((x - w / 2 - 10, y - 13, x + w / 2 + 10, y + 13), radius=6,
                         fill=fondo, outline=bordo)
    dr.text((x, y), testo, font=f, fill=colore, anchor='mm')


# ================================================================ pagina 7
def periodo():
    im, dr = R.pagina(1030, TITOLO)
    R.striscia(dr, 245, T.INFO_FONDO, T.INFO_BORDO, 'Atti firmati in ANSC.',
               'Per ciascuno SIPO indica se lo conosce già: si acquisiscono quelli che non '
               'conosce.')
    R.linguette(dr, 318, ('Per periodo', 'Ricerca puntuale'), 0)
    R.riquadro(dr, (240, 378, 1360, 548))
    R.campo(dr, 270, 392, 'Data da', OGGI)
    R.campo(dr, 640, 392, 'Data a', OGGI)
    R.campo(dr, 1010, 392, 'Comune di registrazione', 'ROMA (RM)', w=320, sola_lettura=True)
    R.campo(dr, 270, 466, 'Tipo evento', 'MORTE', tendina=True)
    R.campo(dr, 640, 466, 'Stato', '5 - FIRMATO DA USC', tendina=True)
    R.campo(dr, 1010, 466, 'Mostra', 'Solo da acquisire', w=320, tendina=True)
    bottone(dr, (1180, 562, 1262, 604), 'CERCA')
    bottone(dr, (1270, 562, 1360, 604), 'ANNULLA')
    R.nota(dr, 240, 583, 'R005 /consultazione/ansc/evento: dataDa, dataA, '
                         'idComuneRegistrazione 8165, idTipoEvento · stato e «In SIPO» li '
                         'calcola SIPO')
    dr.line((60, 625, W - 60, 625), fill=(192, 192, 192), width=2)

    righe = [
        (ID_ANSC, NUMERO, OGGI + ' 16:20', '2199 Caso d’uso di servizio (dich. di morte)',
         'GODI FILIPPO', '20/09/1964', ''),
        ('2026-9424-125-058091', '125', OGGI + ' 16:48',
         '2101 Decesso in abitazione o in luogo pubblico', 'ABATE ROSANNA', '27/12/1961', ''),
        ('2026-9426-127-058091', '127', OGGI + ' 17:05',
         '2101 Decesso in abitazione o in luogo pubblico', 'MARINI LUCIA', '02/03/1950', ''),
    ]
    fine = R.tabella(dr, 60, 650, COLONNE, righe, evidenzia=0, selezionata=0, ambra=2)
    # la colonna «In SIPO» si disegna a parte, con i bollini
    xs = 60 + sum(w for _, w in COLONNE[:-1]) + COLONNE[-1][1] / 2
    _bollino(dr, xs, 650 + 40 * 1 + 20, 'Da acquisire · numero staccato',
             R.VERDE_RIGA, R.VERDE_BORDO, (30, 100, 50))
    _bollino(dr, xs, 650 + 40 * 2 + 20, 'Da acquisire · numero staccato',
             R.VERDE_RIGA, R.VERDE_BORDO, (30, 100, 50))
    _bollino(dr, xs, 650 + 40 * 3 + 20, 'Numero non staccato da SIPO',
             R.AMBRA_FONDO, R.AMBRA_BORDO, (140, 90, 0))

    R.nota(dr, 60, fine + 22, '3 atti da acquisire su 8 firmati il %s · 5 già noti a SIPO '
                              '(formati da SIPO o già acquisiti) non sono mostrati' % OGGI,
           colore=NERO)
    R.nota(dr, 60, fine + 48, '«Numero non staccato da SIPO»: il numero comunale dell’atto '
                              'non è fra quelli richiesti a be-numeratore-comunale', dim=15)
    yb = fine + 84
    bottone(dr, (60, yb, 180, yb + 46), 'INDIETRO')
    bottone(dr, (1250, yb, 1420, yb + 46), 'RICERCA PUNTUALE')
    bottone(dr, (1430, yb, 1540, yb + 46), 'SELEZIONA')
    return im


# ================================================================ pagina 8
def ricerca():
    im, dr = R.pagina(1000, TITOLO)
    R.striscia(dr, 245, T.INFO_FONDO, T.INFO_BORDO, 'Ricerca puntuale.',
               'Per un atto fuori dal periodo, o di cui si conosce l’identificativo ANSC o '
               'l’intestatario.')
    R.linguette(dr, 318, ('Per periodo', 'Ricerca puntuale'), 1)

    R.legenda_sipo(dr, 100, 400, 780, 610, 'Per atto')
    R.campo(dr, 130, 425, 'Identificativo ANSC', 'es. 2026-9423-124-058091', w=330,
            segnaposto=True)
    R.nota(dr, 130, 505, 'oppure', colore=NERO)
    R.campo(dr, 130, 525, 'Numero comunale', NUMERO, w=150)
    R.campo(dr, 310, 525, 'Data da', '01/11/2026', w=180)
    R.campo(dr, 520, 525, 'Data a', '08/11/2026', w=180)

    R.legenda_sipo(dr, 820, 400, 1500, 610, 'Per intestatario')
    R.campo(dr, 850, 425, 'Cognome', 'GODI', w=290)
    R.campo(dr, 1170, 425, 'Nome', 'FILIPPO', w=290)
    R.campo(dr, 850, 525, 'Data di nascita', '20/09/1964', w=290)
    R.campo(dr, 1170, 525, 'Codice fiscale', '', w=290)

    bottone(dr, (1320, 626, 1402, 668), 'CERCA')
    bottone(dr, (1410, 626, 1500, 668), 'ANNULLA')
    R.nota(dr, 100, 638, 'Per atto: R005 /consultazione/ansc/evento con idAnsc, oppure '
                         'idComunale e date', dim=15)
    R.nota(dr, 100, 660, 'Per intestatario: R005 /consultazione/ansc/soggetto/sintetico',
           dim=15)
    dr.line((60, 690, W - 60, 690), fill=(192, 192, 192), width=2)

    righe = [(ID_ANSC, NUMERO, '07/11/2026 16:20', '2199 Caso d’uso di servizio (dich. di morte)',
              'GODI FILIPPO', '20/09/1964', '')]
    fine = R.tabella(dr, 60, 712, COLONNE, righe, evidenzia=0, selezionata=0)
    xs = 60 + sum(w for _, w in COLONNE[:-1]) + COLONNE[-1][1] / 2
    _bollino(dr, xs, 712 + 40 + 20, 'Da acquisire · numero staccato',
             R.VERDE_RIGA, R.VERDE_BORDO, (30, 100, 50))
    yb = fine + 50
    bottone(dr, (60, yb, 180, yb + 46), 'INDIETRO')
    bottone(dr, (1430, yb, 1540, yb + 46), 'SELEZIONA')
    return im


# ================================================================ pagina 9
def riepilogo():
    im, dr = R.pagina(1365, 'Acquisizione Atto ANSC - Atto di Morte')
    R.striscia(dr, 245, T.OK_FONDO, T.OK_BORDO, 'Atto ANSC da acquisire.',
               'Verificare i dati e il tipo atto: con ACQUISISCI SIPO crea l’atto, già '
               'definito.')

    R.legenda_sipo(dr, 60, 340, W - 60, 520, 'Atto ANSC')
    T.campo(dr, 90, 382, 'Identificativo ANSC', ID_ANSC, dim=20)
    T.campo(dr, 640, 382, 'Stato', '5 - FIRMATO DA USC', dim=20)
    xe = T.campo(dr, 90, 422, 'Numero comunale', NUMERO, dim=20)
    f = font(17, True)
    t = 'staccato da SIPO il %s · Disponibile' % OGGI
    dr.rounded_rectangle((xe + 14, 409, xe + 54 + dr.textlength(t, font=f), 435), radius=5,
                         fill=R.VERDE_RIGA, outline=R.VERDE_BORDO)
    dr.line((xe + 24, 422, xe + 30, 428, xe + 41, 414), fill=(30, 100, 50), width=3)
    dr.text((xe + 46, 422), t, font=f, fill=(30, 100, 50), anchor='lm')
    T.campo(dr, 1100, 422, 'Anno', ANNO, dim=20)
    T.campo(dr, 90, 462, 'Data formazione', OGGI, dim=20)
    T.campo(dr, 400, 462, 'Ora', '16:20', dim=20)
    T.campo(dr, 640, 462, 'Comune di registrazione', 'ROMA (RM)', dim=20)

    R.legenda_sipo(dr, 60, 565, W - 60, 705, 'Caso d’uso')
    T.campo(dr, 90, 607, 'Codice', '2199', dim=20)
    T.campo(dr, 400, 607, 'Descrizione', 'Caso d’uso di servizio (dichiarazioni di morte)',
            dim=20)
    T.campo(dr, 90, 647, 'Motivo del recupero',
            '3 - Caso d’uso non previsto nel sistema centrale', dim=20)

    R.legenda_sipo(dr, 60, 750, W - 60, 900, 'Intestatari')
    col = [('Cognome', 180), ('Nome', 180), ('Sesso', 80), ('Data nascita', 140),
           ('Luogo di nascita', 300), ('Cittadinanza', 160), ('Id ANSC soggetto', 190)]
    righe = [('GODI', 'FILIPPO', 'M', '20/09/1964', 'TORRE DEL GRECO (NA)', 'ITALIANA',
              '245912')]
    R._tabella_senza_selezione(dr, 90, 790, col, righe)

    R.legenda_sipo(dr, 60, 945, W - 60, 1040, 'Tipo atto in SIPO')
    R.campo(dr, 90, 968, 'Tipo atto', 'MORTE CON TESTO LIBERO', w=420, tendina=True)
    R.nota(dr, 540, 1010, 'proposto dal caso d’uso: 2199 è un caso d’uso di servizio → '
                          'tipo atto a testo libero dell’area', dim=16)

    R.legenda_sipo(dr, 60, 1080, W - 60, 1282, 'Con ACQUISISCI SIPO scrive')
    voci = ('l’atto nuovo, con numero comunale, anno, data di formazione e stato 2 DEFINITO;',
            'il testo dell’atto (composizione libera) e il contrassegno di atto a testo libero;',
            'lo stato ANSC: identificativo ANSC e 5 FIRMATO DA USC;',
            'il numero comunale %s: da Disponibile a Utilizzato, con l’identificativo ANSC;'
            % NUMERO,
            'i soggetti con i loro identificativi ANSC e ANPR, in anagrafe solo dove mancano.')
    for i, v in enumerate(voci):
        dr.text((95, 1118 + i * 32), '•  ' + v, font=font(19), fill=NERO, anchor='lm')

    yb = 1302
    bottone(dr, (60, yb, 180, yb + 46), 'INDIETRO')
    bottone(dr, (1400, yb, 1540, yb + 46), 'ACQUISISCI')
    return im


# ================================================================ pagina 10
def conferma(base):
    im = base.copy().convert('RGBA')
    velo = Image.new('RGBA', im.size, (0, 0, 0, 110))
    im = Image.alpha_composite(im, velo).convert('RGB')
    dr = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 400, 520, 1200, 830
    dr.rectangle((x0, y0, x1, y1), fill=BIANCO, outline=(120, 120, 120))
    dr.rectangle((x0, y0, x1, y0 + 52), fill=ROSSO)
    dr.text((x0 + 24, y0 + 26), 'Acquisizione dell’atto ANSC', font=font(22, True),
            fill=BIANCO, anchor='lm')
    righe = ('Creare in SIPO l’atto ANSC',
             ID_ANSC + ' (numero comunale %s / %s)?' % (NUMERO, ANNO),
             '',
             'L’atto sarà registrato in SIPO già definito.')
    for i, r in enumerate(righe):
        dr.text((x0 + 30, y0 + 90 + i * 32), r, font=font(21, i == 1), fill=NERO, anchor='lm')
    bottone(dr, (x1 - 300, y1 - 66, x1 - 180, y1 - 22), 'ANNULLA')
    bottone(dr, (x1 - 170, y1 - 66, x1 - 30, y1 - 22), 'ACQUISISCI')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    p9 = riepilogo()
    for nome, im in (('tl_7_acq_periodo.png', periodo()), ('tl_8_acq_ricerca.png', ricerca()),
                     ('tl_9_acq_riepilogo.png', p9), ('tl_10_acq_conferma.png', conferma(p9))):
        im.save(os.path.join(OUT, nome))
        print(nome, im.size)
