# -*- coding: utf-8 -*-
"""I due flussi logici della v0.7 dell'analisi sugli atti a testo libero (13/11/2026).

  tl_flusso_definisci.png    — §5.1, l'atto cominciato in SIPO: Riepilogo senza UC (o pagina del
                               testo libero), DATI PER ANSC, Anteprima con COPIA TESTO, stato WA,
                               WebApp, DEFINISCI con la finestra di aggancio, atto definito.
                               Sostituisce tl_flusso_recupero.png, che finiva ancora con il
                               recupero e lo stato YY · SOSPESO della v0.5.
  tl_flusso_acquisizione.png — §5.2, l'atto nato interamente sulla WebApp: numero staccato prima
                               della stesura (back-office o POST /richiesta), WebApp, pagina
                               «Recupero Atto ANSC», riepilogo, ACQUISISCI, atto creato in SIPO.

Primitive in diagrammi_comune.py; impianto da schermate_recupero_ansc.flusso().

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_testo_libero.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G                  # noqa: E402
import schermate_testo_libero as T            # noqa: E402

OUT = T.OUT
BW, BH = 520, 86


class Tela:
    """Colonna principale centrata in cx, servizi a destra in sx."""

    def __init__(self, larg, alt, titolo, sotto, cx, sx):
        self.im, self.dr = G.tela(larg, alt, titolo, sotto)
        self.cx, self.sx = cx, sx

    def passo(self, y, colore, titolo, sotto=None, x=None, w=BW, h=BH):
        x = self.cx - w / 2 if x is None else x
        G.box(self.dr, x, y, w, h, colore, titolo, sotto, ts=19, ss=15)
        return (x, y, w, h)

    def servizio(self, y, testo, h=BH):
        G.box(self.dr, self.sx, y + (h - 62) / 2, 330, 62, 'grigio', testo, ts=14)
        G.linea(self.dr, [(self.cx + BW / 2, y + h / 2), (self.sx, y + h / 2)], tratteggio=True,
                larg=2)

    def giu(self, y1, y2):
        G.freccia(self.dr, (self.cx, y1), (self.cx, y2))

    def scritta(self, testo, x, y, corsivo=False, dim=15, colore=None):
        G.centra(self.dr, testo, G.fnt(G.F_ITA if corsivo else G.F_REG, dim), x, y,
                 colore or G.ARROW)


# ================================================================ §5.1
def flusso_definisci():
    t = Tela(2000, 1850, 'Atto senza UC: dal Riepilogo alla WebApp ANSC e a DEFINISCI',
             'Pagine di SIPO, servizi chiamati e decisioni; in viola il lavoro sulla WebApp',
             cx=760, sx=1290)
    cx, dr = t.cx, t.dr

    y = 110
    t.passo(y, 'blu', '1 · Riepilogo (fase B)', 'determinazione dell’UC')
    # il tipo atto a testo libero entra direttamente a DATI PER ANSC
    G.box(dr, 40, y, 330, BH, 'blu', 'Tipo atto a testo libero',
          'pagina del testo libero di SIPO', ts=18, ss=14)
    G.rombo(dr, cx, y + 190, 300, 120, 'UC identificato?', ts=19)
    t.giu(y + BH, y + 130)
    G.box(dr, cx + 260, y + 155, 260, 70, 'grigio', 'Percorso ordinario',
          'firmatari, allegati, R009…', ts=17, ss=14)
    G.freccia(dr, (cx + 150, y + 190), (cx + 260, y + 190))
    t.scritta('sì', cx + 190, y + 166)

    y2 = y + 300
    t.giu(y + 250, y2)
    t.scritta('no', cx + 22, y + 262)
    t.passo(y2, 'rosso', '1-2 · Messaggio di rinvio alla WebApp', 'CONFERMA inibito')
    y3 = y2 + 140
    t.giu(y2 + BH, y3)
    t.passo(y3, 'blu', '3 · DATI PER ANSC', 'stacco del numero comunale')
    t.servizio(y3, 'be-numeratore-comunale · POST /richiesta')
    G.percorso(dr, [(205, y + BH), (205, y3 + BH / 2), (cx - BW / 2, y3 + BH / 2)],
               tratteggio=True, larg=2)
    t.scritta('il testo è già scritto in SIPO', 205, y3 + BH / 2 + 18, corsivo=True, dim=14,
              colore=G.MUTED)
    y4 = y3 + 140
    t.giu(y3 + BH, y4)
    t.passo(y4, 'blu', '4-5 · Anteprima: NUMERO COMUNALE in alto', 'COPIA TESTO negli appunti')
    y5 = y4 + 140
    t.giu(y4 + BH, y5)
    t.passo(y5, 'giallo', 'Store: WA · ATTESA WEBAPP',
            'atto SIPO: 1 IN LAVORAZIONE · numero: Disponibile')
    y6 = y5 + 140
    t.giu(y5 + BH, y6)
    t.passo(y6, 'viola', 'WebApp ANSC: stesura e firme',
            'UC di servizio · numero comunale · testo incollato · intestatari', h=96)
    t.scritta('→ 5 FIRMATO DA USC', cx - 110, y6 + 120, corsivo=True, dim=14, colore=G.MUTED)
    y7 = y6 + 170
    t.giu(y6 + 96, y7)
    t.passo(y7, 'blu', '5b · DEFINISCI: finestra di aggancio',
            'abilitato dallo stato WA, anche al rientro')
    t.servizio(y7, 'R005 /consultazione/ansc/evento · data, comune 8165, tipo evento')
    t.scritta('stato 5 filtrato in SIPO · preselezionato il numero coincidente', cx,
              y7 + BH + 6, corsivo=True, dim=14, colore=G.MUTED)

    yd = y7 + 220
    t.giu(y7 + BH + 28, yd - 60)
    G.rombo(dr, cx, yd, 340, 124, 'Atto con il numero fra i candidati?', ts=17)

    # ramo «no»: identificativo digitato o ricerca estesa
    rx = cx + 640
    G.box(dr, rx - 210, yd - 43, 420, BH, 'blu', 'Identificativo digitato o ricerca estesa',
          'VERIFICA dell’idAnsc · per intestatario o per date', ts=17, ss=14)
    G.freccia(dr, (cx + 170, yd), (rx - 210, yd))
    t.scritta('no', cx + 195, yd - 24)
    G.box(dr, rx - 210, yd + 70, 420, 62, 'grigio',
          'R005 evento (idAnsc / idComunale) · R005 soggetto/sintetico', ts=14)
    G.rombo(dr, rx, yd + 250, 280, 110, 'Trovato?', ts=18)
    G.freccia(dr, (rx, yd + 132), (rx, yd + 195))
    bx = rx + 170
    G.box(dr, bx, yd + 205, 260, 96, 'giallo', 'Resta in WA',
          'si riprova più tardi; il back-office ne segnala l’anzianità', ts=17, ss=13)
    G.freccia(dr, (rx + 140, yd + 250), (bx, yd + 250))
    t.scritta('no', rx + 158, yd + 222)
    G.percorso(dr, [(bx + 130, yd + 205), (bx + 130, y7 - 30), (cx + 150, y7 - 30),
                    (cx + 150, y7)], tratteggio=True, larg=2)
    t.scritta('nuovo DEFINISCI', bx - 60, y7 - 48)

    # ramo «sì»: conferma e atto definito
    yc = yd + 150
    t.giu(yd + 62, yc)
    t.scritta('sì', cx + 22, yd + 82)
    t.passo(yc, 'rosso', '6 · DEFINISCI L’ATTO', 'un passaggio solo: nessuna schermata di esito')
    G.percorso(dr, [(rx - 140, yd + 250), (cx + BW / 2, yc + BH / 2)])
    t.scritta('sì', rx - 190, yd + 222)
    yu = yc + 150
    t.giu(yc + BH, yu)
    t.passo(yu, 'verde', 'Atto definito in SIPO',
            '/finalizzaAtto: 2 DEFINITO · store: ID_ANSC e 5 FIRMATO DA USC', h=96)
    t.servizio(yu, 'be-numeratore-comunale · PUT /utilizza', h=96)

    G.legenda(dr, 160, 1800, [('blu', 'pagina SIPO'), ('rosso', 'messaggio o conferma'),
                              ('giallo', 'stato in attesa'), ('viola', 'WebApp ANSC'),
                              ('grigio', 'servizio chiamato'), ('verde', 'esito')])
    return t.im


# ================================================================ §5.2
def flusso_acquisizione():
    t = Tela(2000, 1680, 'Atto formato interamente sulla WebApp: l’acquisizione in SIPO',
             'Il numero comunale si stacca prima della stesura; in SIPO l’atto nasce '
             'all’acquisizione', cx=760, sx=1290)
    cx, dr = t.cx, t.dr

    y = 110
    t.passo(y, 'blu', '1 · Stacco del numero comunale',
            'back-office «Numerazione comunale — richiesta» o API', h=96)
    t.servizio(y, 'be-numeratore-comunale · POST /richiesta', h=96)
    y2 = y + 160
    t.giu(y + 96, y2)
    t.passo(y2, 'giallo', 'Numero: Disponibile', 'in SIPO c’è il numero, non l’atto')
    y3 = y2 + 140
    t.giu(y2 + BH, y3)
    t.passo(y3, 'viola', 'WebApp ANSC: stesura, validazione e firme',
            'qualsiasi UC · numero comunale riportato alla validazione', h=96)
    t.scritta('→ 5 FIRMATO DA USC', cx - 110, y3 + 120, corsivo=True, dim=14, colore=G.MUTED)
    y4 = y3 + 170
    t.giu(y3 + 96, y4)
    t.passo(y4, 'blu', '2 · Recupero Atto ANSC: per periodo',
            'giorno o periodo · comune · tipo evento')
    t.servizio(y4, 'R005 /consultazione/ansc/evento · dataDa, dataA, comune 8165, tipo evento')
    t.scritta('SIPO calcola «In SIPO»: idAnsc già sullo store, numeri staccati', cx,
              y4 + BH + 6, corsivo=True, dim=14, colore=G.MUTED)

    yd = y4 + 220
    t.giu(y4 + BH + 28, yd - 60)
    G.rombo(dr, cx, yd, 320, 120, 'L’atto compare?', ts=18)

    rx = cx + 640
    G.box(dr, rx - 210, yd - 43, 420, BH, 'blu', '3 · Ricerca puntuale',
          'per atto (idAnsc, numero e date) · per intestatario', ts=18, ss=14)
    G.freccia(dr, (cx + 160, yd), (rx - 210, yd))
    t.scritta('no', cx + 185, yd - 24)
    G.box(dr, rx - 210, yd + 70, 420, 62, 'grigio',
          'R005 evento (idAnsc / idComunale) · R005 soggetto/sintetico', ts=14)
    G.rombo(dr, rx, yd + 250, 280, 110, 'Trovato?', ts=18)
    G.freccia(dr, (rx, yd + 132), (rx, yd + 195))
    bx = rx + 170
    G.box(dr, bx, yd + 205, 260, 96, 'giallo', 'Non ancora firmato',
          'si riprova più tardi; il numero resta Disponibile', ts=17, ss=13)
    G.freccia(dr, (rx + 140, yd + 250), (bx, yd + 250))
    t.scritta('no', rx + 158, yd + 222)
    G.percorso(dr, [(bx + 130, yd + 205), (bx + 130, y4 - 30), (cx + 150, y4 - 30),
                    (cx + 150, y4)], tratteggio=True, larg=2)
    t.scritta('nuova ricerca', bx - 60, y4 - 48)

    yr = yd + 150
    t.giu(yd + 60, yr)
    t.scritta('sì', cx + 22, yd + 80)
    t.passo(yr, 'blu', '4 · Acquisizione Atto ANSC: riepilogo',
            'dati dell’atto · intestatari · tipo atto SIPO proposto dall’UC')
    G.percorso(dr, [(rx - 140, yd + 250), (cx + BW / 2, yr + BH / 2)])
    t.scritta('sì', rx - 190, yd + 222)

    yn = yr + 210
    t.giu(yr + BH, yn - 60)
    G.rombo(dr, cx, yn, 340, 120, 'Numero staccato da SIPO?', ts=18)
    G.box(dr, rx - 210, yn - 48, 420, 96, 'grigio', 'Avviso e decisione',
          'il numero non è fra quelli richiesti: TL-12', ts=17, ss=14)
    G.freccia(dr, (cx + 170, yn), (rx - 210, yn))
    t.scritta('no', cx + 195, yn - 24)

    ya = yn + 150
    t.giu(yn + 60, ya)
    t.scritta('sì', cx + 22, yn + 80)
    t.passo(ya, 'rosso', '5 · ACQUISISCI', 'finestra di conferma')
    G.percorso(dr, [(rx, yn + 48), (rx, ya + BH / 2), (cx + BW / 2, ya + BH / 2)],
               tratteggio=True, larg=2)
    t.scritta('con l’avviso', rx - 70, ya + BH / 2 - 18, corsivo=True, dim=14, colore=G.MUTED)
    yu = ya + 150
    t.giu(ya + BH, yu)
    t.passo(yu, 'verde', 'Atto creato in SIPO',
            '2 DEFINITO · testo · soggetti · store: ID_ANSC e 5 FIRMATO DA USC', h=96)
    t.servizio(yu, 'be-numeratore-comunale · PUT /utilizza', h=96)

    G.legenda(dr, 160, 1630, [('blu', 'pagina SIPO o back-office'),
                              ('rosso', 'conferma'), ('giallo', 'stato in attesa'),
                              ('viola', 'WebApp ANSC'), ('grigio', 'servizio o decisione'),
                              ('verde', 'esito')])
    return t.im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for nome, im in (('tl_flusso_definisci.png', flusso_definisci()),
                     ('tl_flusso_acquisizione.png', flusso_acquisizione())):
        im.save(os.path.join(OUT, nome))
        print(nome, im.size)
