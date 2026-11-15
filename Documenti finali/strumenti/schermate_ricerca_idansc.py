# -*- coding: utf-8 -*-
"""La pagina di ricerca degli atti di SIPO adeguata ad ANSC: le due possibilità (14/11/2026,
analisi su annullamento, cancellazione e rettifiche, cap. «Il flusso attuale in SIPO»).

La pagina è quella della linguetta «Estremi pratica» delle aree (es. Sezione Nascite,
gestioneNascita.html righe 285-366): Tipo Atto · Numero Atto (maxlength 6) · Parte e Serie /
Esponente · Anno / Stato, poi CERCA, ANNULLA e CREA ATTO. Per ritrovare un atto redatto in ANSC
il valore da raccogliere è l'identificativo ANSC (ANNO-progressivo nazionale-progressivo
comunale-codice ISTAT, 23 caratteri):

  · A — un campo aggiuntivo «Identificativo ANSC» nello spazio libero della seconda riga;
  · B — una casella «Ricerca per identificativo ANSC» che cambia il significato del campo
        Numero Atto (etichetta, lunghezza) e spegne i campi che non servono.

Lo screenshot originale non è fra le sorgenti: la pagina è ridisegnata nello stile di SIPO
con le primitive di schermate_sipo_wf.

Terza figura (C): l'elenco dei risultati, dove la colonna «Numero Atto Esteso» di un atto
digitale mostra il numero tradizionale tra parentesi e sotto, in grassetto, l'identificativo
ANSC. Dati di fantasia: la schermata di partenza conteneva nomi di persone reali. Le modifiche sono contrassegnate in giallo e numerate.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_ricerca_idansc.py
"""
import os

from PIL import ImageDraw

import schermate_sipo_wf as S
from schermate_sipo_wf import (BORDO, CAMPO, INK, M, MUTED, N_BLD, N_ITA, N_REG, ROSSO, W,
                               bottone, casella, campo, f, lx)

OUT = os.path.join(S.IMG, 'annullamento')
EVIDENZA = '#fff4d6'
GIALLO_BORDO = '#e5a800'
SPENTO = '#f0f0f0'
ROSSO_CHIARO = '#b8506a'
ID_ANSC = '2026-0000731-124-058091'


def pastiglia(dr, x, y, n):
    dr.ellipse([x - 13, y - 13, x + 13, y + 13], fill=S.GIALLO, outline=INK, width=2)
    dr.text((x, y), str(n), font=f(N_BLD, 16), fill=INK, anchor='mm')


def evidenzia(dr, box):
    """Riquadro tratteggiato attorno all'elemento nuovo o modificato."""
    x0, y0, x1, y1 = box
    dr.rectangle(box, fill=None)
    for xa in range(x0, x1, 12):
        dr.line([(xa, y0), (min(xa + 7, x1), y0)], fill=GIALLO_BORDO, width=3)
        dr.line([(xa, y1), (min(xa + 7, x1), y1)], fill=GIALLO_BORDO, width=3)
    for ya in range(y0, y1, 12):
        dr.line([(x0, ya), (x0, min(ya + 7, y1))], fill=GIALLO_BORDO, width=3)
        dr.line([(x1, ya), (x1, min(ya + 7, y1))], fill=GIALLO_BORDO, width=3)


def campo_spento(dr, x, y, w, etichetta, tipo='testo'):
    dr.text((x, y), etichetta, font=f(N_BLD, 14), fill='#9a9a9a')
    by = y + 21
    dr.rectangle([x, by, x + w, by + 25], outline='#c4c4c4', width=1, fill=SPENTO)
    if tipo == 'select':
        dr.text((x + 6, by + 4), "-- Selezionare --", font=f(N_REG, 14), fill='#b0b0b0')
        dr.line([(x + w - 16, by + 10), (x + w - 11, by + 15), (x + w - 6, by + 10)],
                fill='#b0b0b0', width=2)
    return by + 25


def cornice(titolo):
    """Testata, titolo di area, legenda «Ricerca» e linguette come in SIPO."""
    im, dr, y = S.pagina(titolo, alt=1100)
    dr.text((M, y), "Sezione Nascite", font=f(N_BLD, 16), fill=INK)
    y += 34
    # fieldset «Ricerca»
    global Y_FIELD
    Y_FIELD = y + 10
    dr.rectangle([M + 14, y, M + 90, y + 22], fill='white')
    dr.text((M + 20, y + 2), "Ricerca", font=f(N_BLD, 15), fill=INK)
    y += 40
    # linguette centrate
    fl = f(N_BLD, 14)
    voci = ["Estremi anagrafici", "Codice fiscale", "Codice individuale", "Estremi pratica"]
    larg = [lx(dr, v, fl) + 36 for v in voci]
    x = (W - sum(larg) - 4 * 3) // 2
    for v, w in zip(voci, larg):
        col = ROSSO if v == "Estremi pratica" else S.GRIGIO_TAB
        dr.rectangle([x, y, x + w, y + 32], fill=col)
        dr.text((x + 18, y + 7), v, font=fl, fill='white')
        x += w + 4
    y += 48
    global Y_BOX
    Y_BOX = y
    return im, dr, y


COL = [M + 60, M + 480, M + 900]     # le tre colonne col-md-4
WC = 330


def piede(dr, y):
    """CERCA e ANNULLA dentro il riquadro della linguetta, CREA ATTO sotto il fieldset."""
    x = S.bottone(dr, W - M - 230, y, "CERCA")
    S.bottone(dr, x + 8, y, "ANNULLA")
    # riquadro della linguetta (bordo grigio come nel template) e fieldset «Ricerca»
    dr.rectangle([M + 30, Y_BOX, W - M - 30, y + 48], outline='#8f8f8f', width=2)
    dr.line([(M, Y_FIELD), (M + 14, Y_FIELD)], fill=BORDO)
    dr.line([(M + 90, Y_FIELD), (W - M, Y_FIELD)], fill=BORDO)
    dr.line([(M, Y_FIELD), (M, y + 72)], fill=BORDO)
    dr.line([(W - M, Y_FIELD), (W - M, y + 72)], fill=BORDO)
    dr.line([(M, y + 72), (W - M, y + 72)], fill=BORDO)
    dr.rectangle([M, y + 92, M + 110, y + 122], fill=ROSSO)
    dr.text((M + 14, y + 99), "CREA ATTO", font=f(N_BLD, 13), fill='white')
    return y + 122


def nota(dr, y, righe):
    dr.line([(M, y), (W - M, y)], fill=BORDO, width=1)
    y += 14
    for n, t in righe:
        pastiglia(dr, M + 14, y + 10, n)
        dr.text((M + 38, y + 1), t, font=f(N_REG, 15), fill=INK)
        y += 30
    return y


# ======================================================== A) il campo aggiuntivo
def variante_a(dest):
    im, dr, y = cornice("Ricerca atto — variante A: campo aggiuntivo «Identificativo ANSC»")
    y0 = y + 20
    campo_spento(dr, COL[0], y0, WC, "Tipo Atto", 'select')
    campo_spento(dr, COL[1], y0, 150, "Numero Atto")
    campo_spento(dr, COL[2], y0, WC, "Parte e Serie", 'select')
    y1 = y0 + 70
    campo_spento(dr, COL[0], y1, 80, "Esponente")
    campo_spento(dr, COL[1], y1, 120, "Anno")
    # il campo nuovo, nello spazio libero della terza colonna
    dr.rectangle([COL[2] - 10, y1 - 8, COL[2] + WC + 10, y1 + 56], fill=EVIDENZA)
    campo(dr, COL[2], y1, WC, "Identificativo ANSC", ID_ANSC)
    evidenzia(dr, (COL[2] - 10, y1 - 8, COL[2] + WC + 10, y1 + 56))
    pastiglia(dr, COL[2] + WC + 10, y1 - 8, 1)
    dr.text((COL[2], y1 + 62), "anno-progr. nazionale-progr. comunale-ISTAT",
            font=f(N_ITA, 13), fill=MUTED)
    y2 = y1 + 90
    campo_spento(dr, COL[0], y2, 200, "Stato", 'select')
    # avviso sotto i campi
    ya = y2 + 66
    dr.rectangle([COL[0], ya, W - M - 60, ya + 34], fill=EVIDENZA, outline=GIALLO_BORDO)
    dr.text((COL[0] + 12, ya + 8), "Con l’identificativo ANSC valorizzato la ricerca avviene "
            "solo su quello: gli altri estremi sono disabilitati.", font=f(N_REG, 15), fill=INK)
    pastiglia(dr, W - M - 60, ya, 2)
    yf = nota(dr, piede(dr, ya + 54) + 30, [
        (1, "Campo nuovo, facoltativo: l’identificativo ANSC dell’atto (23 caratteri), "
            "nello spazio libero della seconda riga."),
        (2, "Valorizzato l’identificativo, Tipo Atto, Numero, Parte e Serie, Esponente, Anno "
            "e Stato si spengono; svuotandolo tornano attivi.")])
    S.ritaglia(im, yf, dest)
    return dest


# ======================================================== B) la casella che cambia significato
def variante_b(dest):
    im, dr, y = cornice("Ricerca atto — variante B: casella «Ricerca per identificativo ANSC»")
    # la casella, in testa al riquadro
    yc = y + 18
    dr.rectangle([COL[0] - 10, yc - 8, COL[0] + 300, yc + 26], fill=EVIDENZA)
    casella(dr, COL[0], yc, "Ricerca per identificativo ANSC", segnata=True,
            ft=f(N_BLD, 15))
    evidenzia(dr, (COL[0] - 10, yc - 8, COL[0] + 300, yc + 26))
    pastiglia(dr, COL[0] + 300, yc - 8, 1)
    y0 = yc + 44
    campo_spento(dr, COL[0], y0, WC, "Tipo Atto", 'select')
    # Numero Atto che cambia significato
    wn = 330
    dr.rectangle([COL[1] - 10, y0 - 8, COL[1] + wn + 10, y0 + 56], fill=EVIDENZA)
    campo(dr, COL[1], y0, wn, "Identificativo ANSC", ID_ANSC)
    dr.text((COL[1] + lx(dr, "Identificativo ANSC", f(N_BLD, 14)) + 8, y0 + 1),
            "(al posto di Numero Atto)", font=f(N_ITA, 13), fill=MUTED)
    evidenzia(dr, (COL[1] - 10, y0 - 8, COL[1] + wn + 10, y0 + 56))
    pastiglia(dr, COL[1] + wn + 10, y0 - 8, 2)
    dr.text((COL[1], y0 + 62), "anno-progr. nazionale-progr. comunale-ISTAT",
            font=f(N_ITA, 13), fill=MUTED)
    campo_spento(dr, COL[2], y0, WC, "Parte e Serie", 'select')
    y1 = y0 + 90
    campo_spento(dr, COL[0], y1, 80, "Esponente")
    campo_spento(dr, COL[1], y1, 120, "Anno")
    y2 = y1 + 70
    campo_spento(dr, COL[0], y2, 200, "Stato", 'select')
    pastiglia(dr, COL[0] + 220, y2 + 34, 3)
    yf = nota(dr, piede(dr, y2 + 70) + 30, [
        (1, "Casella nuova, spenta per difetto: la pagina resta quella di oggi."),
        (2, "Con la casella segnata il campo Numero Atto diventa «Identificativo ANSC»: "
            "lunghezza da 6 a 23 caratteri, controllo del formato."),
        (3, "Gli altri estremi non servono e si spengono; togliendo la spunta il campo torna "
            "Numero Atto e si svuota.")])
    S.ritaglia(im, yf, dest)
    return dest


# ======================================================== C) l'elenco dei risultati
RIGHE = [
    # (data pratica, anno, cod. individuale, cognome, nome, data nascita, sesso, data atto,
    #  tipo atto, stato, numero atto esteso, idAnsc, esponente) — dati di fantasia
    ('07/03/2026', '2026', '5001184', 'ROSSI', 'GIULIA', '04/03/2026', 'F', '07/03/2026',
     'Iscrizione da Pubblico Ufficiale figlio nato in costanza di matrimonio', 'DEFINITO',
     '00124/1A21/2026', ID_ANSC, '21'),
    ('12/02/2020', '2020', '6108891', 'ROSSI', 'GIULIA', '04/02/2020', 'F', '12/02/2020',
     'Iscrizione da Pubblico Ufficiale figlio nato in costanza di matrimonio', 'DEFINITO',
     '00093/1A21/2020', None, '21'),
]


def risultati(dest):
    """L'elenco dei risultati con la colonna «Numero Atto Esteso» adeguata agli atti digitali."""
    im, dr, y = S.pagina("Gestione Nascite — elenco dei risultati: «Numero Atto Esteso» per gli "
                         "atti digitali", alt=1200)
    # ── la ricerca (Estremi anagrafici), come in SIPO
    dr.text((M + 14, y), "Ricerca", font=f(N_BLD, 15), fill=INK)
    yt = y + 34
    fl = f(N_BLD, 14)
    voci = ["Estremi anagrafici", "Codice fiscale", "Codice individuale", "Estremi pratica"]
    larg = [lx(dr, v, fl) + 36 for v in voci]
    x = (W - sum(larg) - 12) // 2
    for v, w in zip(voci, larg):
        dr.rectangle([x, yt, x + w, yt + 32], fill=ROSSO if v == voci[0] else S.GRIGIO_TAB)
        dr.text((x + 18, yt + 7), v, font=fl, fill='white')
        x += w + 4
    yb = yt + 46
    c = [M + 60, M + 480, M + 900]
    campo(dr, c[0], yb + 12, 330, "Cognome", "rossi")
    campo(dr, c[1], yb + 12, 250, "Nome", "giulia")
    casella(dr, c[1] + 262, yb + 37, "parziale")
    campo(dr, c[2], yb + 12, 330, "Sesso", "F", 'select')
    campo(dr, c[0], yb + 72, 250, "Data di nascita (Da)", "gg/mm/aaaa", 'data')
    campo(dr, c[1], yb + 72, 250, "Data di nascita (A)", "gg/mm/aaaa", 'data')
    campo(dr, c[2], yb + 72, 250, "Anno nascita", "")
    x = S.bottone(dr, W - M - 230, yb + 138, "CERCA")
    S.bottone(dr, x + 8, yb + 138, "ANNULLA")
    dr.rectangle([M + 30, yb, W - M - 30, yb + 180], outline='#8f8f8f', width=2)
    dr.line([(M, yb + 200), (W - M, yb + 200)], fill=BORDO, width=2)

    # ── l'elenco
    y = yb + 224
    teste = ['', 'Data\nPratica', 'Anno', 'Codice\nIndividuale', 'Cognome', 'Nome',
             'Data\nNascita', 'Sesso', 'Data Atto', 'Tipo Atto', 'Stato',
             'Numero Atto\nEsteso', 'Esponente']
    lw = [36, 84, 52, 92, 92, 84, 84, 50, 88, 250, 82, 182, 78]
    xs = [M]
    for w in lw:
        xs.append(xs[-1] + w)
    ht = 50
    dr.rectangle([M, y, xs[-1], y + ht], fill=ROSSO)
    fh = f(N_BLD, 13)
    for i, t in enumerate(teste):
        righe = t.split('\n')
        for k, r in enumerate(righe):
            dr.text(((xs[i] + xs[i + 1]) / 2, y + ht / 2 + (k - (len(righe) - 1) / 2) * 16),
                    r, font=fh, fill='white', anchor='mm')
    y += ht
    fr, fb = f(N_REG, 13), f(N_BLD, 14)
    for n, riga in enumerate(RIGHE):
        hr = 78
        dr.rectangle([M, y, xs[-1], y + hr], outline=BORDO, fill='white')
        for xi in xs[1:-1]:
            dr.line([(xi, y), (xi, y + hr)], fill=BORDO)
        cy = y + hr / 2
        dr.ellipse([M + 11, cy - 7, M + 25, cy + 7], outline=INK, fill='white')
        if n == 0:
            dr.ellipse([M + 15, cy - 3, M + 21, cy + 3], fill=S.BLU_ICONA)
        (dp, an, ci, co, no, dn, se, da, ta, st, est, ida, esp) = riga
        for i, v in zip(range(1, 13), (dp, an, ci, co, no, dn, se, da, ta, st, None, esp)):
            if v is None:
                continue
            xc = (xs[i] + xs[i + 1]) / 2
            if i == 9:
                rr = S.avvolgi(dr, v, fr, lw[i] - 12)
                for k, r in enumerate(rr):
                    dr.text((xc, cy + (k - (len(rr) - 1) / 2) * 16), r, font=fr, fill=INK,
                            anchor='mm')
            else:
                dr.text((xc, cy), v, font=fr, fill=INK, anchor='mm')
        xc = (xs[11] + xs[12]) / 2
        if ida:
            box = (int(xs[11]) + 4, int(y) + 6, int(xs[12]) - 4, int(y + hr) - 6)
            dr.rectangle(box, fill=EVIDENZA)
            dr.text((xc, cy - 12), '(' + est + ')', font=fr, fill=MUTED, anchor='mm')
            dr.text((xc, cy + 12), ida, font=fb, fill=INK, anchor='mm')
            evidenzia(dr, box)
            pastiglia(dr, box[2], box[1], 1)
        else:
            dr.text((xc, cy), est, font=fr, fill=INK, anchor='mm')
            pastiglia(dr, xs[12] - 16, y + 14, 2)
        y += hr
    # paginazione e pulsanti
    y += 24
    dr.rectangle([W // 2 - 16, y, W // 2 + 16, y + 30], fill=ROSSO_CHIARO)
    dr.text((W // 2, y + 15), "1", font=f(N_BLD, 14), fill='white', anchor='mm')
    y += 54
    dr.rectangle([M, y, M + 110, y + 30], fill=ROSSO)
    dr.text((M + 14, y + 7), "CREA ATTO", font=f(N_BLD, 13), fill='white')
    S.bottoni_dx(dr, y, [("CANCELLA PRATICA", True), ("RIPRENDI LAVORAZIONE", True)],
                 x_fine=xs[-1])
    S.bottoni_dx(dr, y + 42, [("DETTAGLIO PRATICA", True), ("STAMPE E COMUNICAZIONI", True)],
                 x_fine=xs[-1])
    yf = nota(dr, y + 100, [
        (1, "Atto digitale (formato in ANSC): il numero atto esteso tradizionale tra parentesi "
            "tonde e sotto, in grassetto, l’identificativo ANSC."),
        (2, "Atto tradizionale: la cella resta com’è oggi.")])
    S.ritaglia(im, yf, dest)
    return dest


# ======================================================== D) il dettaglio dell'atto
def _coppia(dr, x, y, etichetta, valore, grassetto=False, colore=INK):
    fe = f(N_BLD, 15)
    dr.text((x, y), etichetta + " :", font=fe, fill=INK)
    xv = x + lx(dr, etichetta + " : ", fe)
    dr.text((xv, y), valore, font=f(N_BLD if grassetto else N_REG, 15), fill=colore)
    return xv + lx(dr, valore, f(N_BLD if grassetto else N_REG, 15))


def dettaglio(dest):
    """Il «Dettaglio Atto Nascita» con i dati ANSC accanto a quelli tradizionali."""
    im, dr, y = S.pagina("Dettaglio Atto Nascita — i dati ANSC di un atto digitale", alt=1000)
    dr.text((M, y), "Dettaglio Atto Nascita", font=f(N_BLD, 16), fill=INK)
    y += 38
    yp = y
    dr.text((M + 20, y + 4), "Dati Atto", font=f(N_BLD, 16), fill=INK)
    y += 44
    c = [M + 40, M + 460, M + 900]
    _coppia(dr, c[0], y, "Tipologia Atto", "Iscrizione da Pubblico Ufficiale - Iscrizione da "
            "Pubblico Ufficiale figlio nato in costanza di matrimonio")
    _coppia(dr, c[2] + 160, y, "Scansionato", "No")
    y += 32
    _coppia(dr, c[0], y, "Data Atto", "07/03/2026")
    _coppia(dr, c[1] - 140, y, "Orario Atto", "11:08")
    _coppia(dr, c[2] - 220, y, "Esito", "Nessuno")
    y += 32
    _coppia(dr, c[0], y, "Stato Pratica", "DEFINITO")
    y += 32
    # estremi tradizionali: tra parentesi, come nell'elenco dei risultati
    dr.rectangle([c[0] - 12, y - 8, W - M - 28, y + 64], fill=EVIDENZA)
    _coppia(dr, c[0], y, "Numero Atto", "(00124)", colore=MUTED)
    y2 = y + 32
    _coppia(dr, c[0], y2, "Parte", "(1)", colore=MUTED)
    _coppia(dr, c[0] + 150, y2, "Serie", "(A)", colore=MUTED)
    _coppia(dr, c[0] + 300, y2, "Esponente", "(21)", colore=MUTED)
    _coppia(dr, c[0] + 480, y2, "Anno", "(2026)", colore=MUTED)
    evidenzia(dr, (c[0] - 12, y - 8, W - M - 28, y + 64))
    pastiglia(dr, W - M - 28, y - 8, 1)
    y = y2 + 52
    # la riga nuova dei dati ANSC
    dr.rectangle([c[0] - 12, y - 8, W - M - 28, y + 64], fill=EVIDENZA)
    _coppia(dr, c[0], y, "Identificativo ANSC", ID_ANSC, grassetto=True)
    _coppia(dr, c[1] + 40, y, "Stato ANSC", "5 - FIRMATO DA USC", grassetto=True)
    _coppia(dr, c[2] + 80, y, "Data formazione ANSC", "07/03/2026")
    y2 = y + 32
    _coppia(dr, c[0], y2, "Numero nazionale", "0000731")
    _coppia(dr, c[1] + 40, y2, "Numero comunale", "124")
    _coppia(dr, c[2] + 80, y2, "Comune (ISTAT)", "058091")
    evidenzia(dr, (c[0] - 12, y - 8, W - M - 28, y + 64))
    pastiglia(dr, W - M - 28, y - 8, 2)
    y = y2 + 56
    dr.rectangle([M, yp, W - M, y], outline=BORDO, width=1)
    # pulsanti come nella pagina
    y += 22
    x = S.bottone(dr, M + 40, y, "REGISTRO")
    S.bottone(dr, x + 40, y, "DOWNLOAD")
    xa = W - M - 190
    S.bottone(dr, xa, y, "ANNULLA ATTO")
    evidenzia(dr, (xa - 6, y - 6, xa + lx(dr, "ANNULLA ATTO", f(N_BLD, 13)) + 34, y + 36))
    pastiglia(dr, xa + lx(dr, "ANNULLA ATTO", f(N_BLD, 13)) + 34, y - 6, 3)
    y += 70
    S.bottoni_dx(dr, y, [("PROPOSTA ANNOTAZIONE", True), ("AGGIORNAMENTO ANAGRAFICO", True)],
                 x_fine=W - M - 40)
    yf = nota(dr, y + 66, [
        (1, "Estremi tradizionali (numero, parte, serie, esponente, anno) tra parentesi tonde, "
            "come nell’elenco dei risultati."),
        (2, "Riga nuova, solo per gli atti digitali: identificativo ANSC in grassetto, stato ANSC "
            "dallo store, numero nazionale, comunale, ISTAT e data di formazione."),
        (3, "Per un atto digitale ANNULLA ATTO non chiama più la sola procedura di SIPO: "
            "segue il percorso ANSC descritto in questo documento.")])
    S.ritaglia(im, yf, dest)
    return dest


# ======================================================== E) la pagina dell'annullamento
def _sezione(dr, y, titolo):
    dr.text((M + 20, y), titolo, font=f(N_BLD, 16), fill=INK)
    dr.line([(M + 20, y + 26), (W - M - 20, y + 26)], fill=BORDO, width=1)
    return y + 40


def _area(dr, x, y, w, h, testo, fondo='white', ft=None):
    dr.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=fondo)
    righe = S.avvolgi(dr, testo, ft or f(N_REG, 15), w - 24)
    for k, r in enumerate(righe):
        dr.text((x + 12, y + 10 + k * 21), r, font=ft or f(N_REG, 15), fill=INK)


def annullamento(dest):
    """La pagina «Annullamento atto» (annullamentoCancellazione.html) adeguata a R013."""
    im, dr, y = S.pagina("Annullamento atto — atto formato in ANSC: i dati di R013", alt=1500)
    dr.text((M, y), "Annullamento atto", font=f(N_BLD, 16), fill=INK)
    y += 40
    c = [M + 40, M + 460, M + 900]

    # 1. l'atto da annullare, in sola lettura
    y = _sezione(dr, y, "Atto da annullare")
    y0 = y
    _coppia(dr, c[0], y, "Tipo atto", "Morte in abitazione a Roma")
    _coppia(dr, c[1] + 40, y, "Estremi", "(00124/1A21/2026)", colore=MUTED)
    _coppia(dr, c[2] + 40, y, "Data formazione", "07/03/2026")
    y += 30
    _coppia(dr, c[0], y, "Identificativo ANSC", ID_ANSC, grassetto=True)
    _coppia(dr, c[1] + 40, y, "Stato ANSC", "5 - FIRMATO DA USC", grassetto=True)
    pastiglia(dr, W - M - 30, y0 - 4, 1)
    y += 50

    # 2. il provvedimento: enteDichiarante
    y = _sezione(dr, y, "Provvedimento che dispone l’annullamento (ente dichiarante)")
    yb = y
    dr.rectangle([M + 28, y - 8, W - M - 28, y + 132], fill=EVIDENZA)
    campo(dr, c[0], y, 330, "Ente *", "Tribunale di Roma")
    campo(dr, c[1], y, 160, "Provincia *", "RM", 'select')
    campo(dr, c[1] + 190, y, 230, "Comune *", "ROMA", 'select')
    campo(dr, c[2] + 40, y, 320, "Indirizzo", "")
    y += 66
    campo(dr, c[0], y, 330, "Tipo di provvedimento *", "Decreto", 'select')
    campo(dr, c[1], y, 160, "Numero *", "1234/2026")
    campo(dr, c[1] + 190, y, 160, "Data *", "20/10/2026", 'data')
    dr.text((c[2] + 40, y + 26), "→ estremiDocumento: «Decreto n. 1234/2026 del 20/10/2026»",
            font=f(N_ITA, 14), fill=MUTED)
    y += 66
    evidenzia(dr, (M + 28, yb - 8, W - M - 28, y))
    pastiglia(dr, W - M - 28, yb - 8, 2)
    y += 24

    # 3. la motivazione: dettaglioRettifica
    y = _sezione(dr, y, "Motivazione annullamento *")
    yb = y
    _area(dr, c[0], y, W - 2 * M - 120, 64,
          "Annullamento dell’atto per indebita registrazione, disposto dal provvedimento "
          "indicato sopra.")
    dr.text((c[0], y + 72), "Campo di oggi: diventa datiRettifica.dettaglioRettifica e resta la "
            "motivazione dell’annullamento in SIPO.", font=f(N_ITA, 14), fill=MUTED)
    evidenzia(dr, (c[0] - 10, yb - 8, W - M - 70, yb + 96))
    pastiglia(dr, W - M - 70, yb - 8, 3)
    y += 120

    # 4. il testo dell'annotazione: composizioneCompleta
    y = _sezione(dr, y, "Testo dell’annotazione (formula 190)")
    yb = y
    _area(dr, c[0], y, W - 2 * M - 120, 64,
          "Con provvedimento del Tribunale di ROMA (RM) numero 1234/2026 in data 20/10/2026 "
          "l’atto di cui sopra è stato annullato.", fondo=S.SOLA_LETTURA)
    dr.text((c[0], y + 72), "Composto da SIPO con i dati del provvedimento: si aggiorna da "
            "solo, non si scrive a mano.", font=f(N_ITA, 14), fill=MUTED)
    evidenzia(dr, (c[0] - 10, yb - 8, W - M - 70, yb + 96))
    pastiglia(dr, W - M - 70, yb - 8, 4)
    y += 120

    # 5. i dati dell'annotazione che SIPO valorizza da sé
    y = _sezione(dr, y, "Dati dell’annotazione (valorizzati da SIPO)")
    yb = y
    _coppia(dr, c[0], y, "Caso d’uso", "2341 - Annotazione per rettifica")
    _coppia(dr, c[1] + 40, y, "Tipo rettifica", "0 - ANNULLAMENTO")
    y += 30
    _coppia(dr, c[0], y, "Numero comunale", "staccato alla conferma")
    _coppia(dr, c[1] + 40, y, "Data e ora di formazione", "alla conferma")
    pastiglia(dr, W - M - 30, yb - 4, 5)
    y += 50
    dr.line([(M, y), (W - M, y)], fill='#bdbdbd', width=1)
    y += 24
    S.bottone(dr, M + 20, y, "INDIETRO")
    xb = W - M - 20 - (lx(dr, "CONFERMA ANNULLAMENTO", f(N_BLD, 13)) + 28)
    S.bottone(dr, xb, y, "CONFERMA ANNULLAMENTO")
    dr.text((xb - 14, y + 7), "deposito con R013, poi firma dell’ufficiale con R007",
            font=f(N_ITA, 14), fill=MUTED, anchor='ra')
    yf = nota(dr, y + 56, [
        (1, "Sola lettura: l’atto da annullare. Ne vengono datiRettifica.eventoCollegato "
            "(comune, numero, anno, data, registro, idAnsc)."),
        (2, "Nuovo: il provvedimento. Obbligatorio per il caso d’uso 2341 (enteDichiarante); "
            "tipo, numero e data compongono estremiDocumento."),
        (3, "Il campo di oggi: datiRettifica.dettaglioRettifica."),
        (4, "Nuovo: composizioneCompleta, il testo della formula 190 composto con i dati del "
            "provvedimento."),
        (5, "Valori che l’operatore non scrive: idUsecase, idTipoRettifica, numero comunale "
            "dell’annotazione, data e ora.")])
    S.ritaglia(im, yf, dest)
    return dest


# ======================================================== F) la proposta di annotazione (art. 98)
def proposta_art98(dest):
    """«Inserimento proposta di annotazione» per un atto digitale: errore materiale (art. 98)."""
    im, dr, y = S.pagina("Inserimento proposta di annotazione — atto digitale: errore materiale "
                         "(art. 98)", alt=1700)
    dr.text((M, y), "Inserimento proposta di annotazione", font=f(N_BLD, 16), fill=INK)
    y += 40
    c = [M + 40, M + 460, M + 900]

    # 1. dettaglio atto, con l'identificativo ANSC
    y = _sezione(dr, y, "Dettaglio atto")
    y0 = y
    _coppia(dr, c[0], y, "Numero", "(00040)", colore=MUTED)
    _coppia(dr, c[0] + 170, y, "Parte", "(1)", colore=MUTED)
    _coppia(dr, c[0] + 290, y, "Serie", "(A)", colore=MUTED)
    _coppia(dr, c[0] + 410, y, "Esponente", "(21)", colore=MUTED)
    _coppia(dr, c[0] + 570, y, "Anno", "(2026)", colore=MUTED)
    _coppia(dr, c[2] + 40, y, "Area", "NASCITE")
    y += 30
    _coppia(dr, c[0], y, "Identificativo ANSC", "2026-0000522-40-058091", grassetto=True)
    _coppia(dr, c[1] + 40, y, "Stato ANSC", "5 - FIRMATO DA USC", grassetto=True)
    y += 30
    _coppia(dr, c[0], y, "Titolare", "ROSSI GIULIA")
    _coppia(dr, c[1] + 40, y, "Sesso", "F")
    _coppia(dr, c[2] + 40, y, "Data di nascita", "04/02/2026")
    pastiglia(dr, W - M - 30, y0 - 4, 1)
    y += 50

    # 2. nuova annotazione, con la corrispondenza ANSC
    y = _sezione(dr, y, "Nuova annotazione")
    campo(dr, c[0], y, 330, "Tipo atto", "Nascita", 'lettura')
    campo(dr, c[1], y, 330, "Tipo annotazione", "Rettificazione", 'lettura')
    campo(dr, c[2], y, 330, "Formula", "190 - Art. 98", 'lettura')
    y += 64
    yb = y
    dr.rectangle([M + 28, y - 6, W - M - 28, y + 30], fill=EVIDENZA)
    dr.text((c[0], y + 4), "In ANSC:", font=f(N_BLD, 15), fill=INK)
    _coppia(dr, c[0] + 80, y + 4, "Caso d’uso", "14640000 - Annotazione per errore materiale")
    _coppia(dr, c[1] + 160, y + 4, "Formula ANSC", "888")
    _coppia(dr, c[2] + 80, y + 4, "Tipo rettifica", "1 - MODIFICA")
    evidenzia(dr, (M + 28, yb - 6, W - M - 28, yb + 30))
    pastiglia(dr, W - M - 28, yb - 6, 2)
    y += 60

    # 3. le correzioni: dato scelto, valore attuale letto, valore nuovo
    y = _sezione(dr, y, "Correzioni (art. 98: dati anagrafici del titolare, della madre e del "
                        "padre)")
    yb = y
    teste = ["Dato da correggere", "Valore da sostituire (dall’atto in ANSC)",
             "Valore con cui sostituire", ""]
    lw = [330, 400, 400, 90]
    xs = [c[0]]
    for w in lw:
        xs.append(xs[-1] + w)
    dr.rectangle([xs[0], y, xs[-1], y + 34], fill=ROSSO)
    for i, t in enumerate(teste):
        dr.text((xs[i] + 10, y + 8), t, font=f(N_BLD, 14), fill='white')
    y += 34
    righe = [("Titolare · Nome", "GIULIA", "GIULIANA"),
             ("Madre · Cognome", "BIANCHII", "BIANCHI")]
    for dato, ante, nuovo in righe:
        dr.rectangle([xs[0], y, xs[-1], y + 44], outline=BORDO, fill='white')
        for xi in xs[1:-1]:
            dr.line([(xi, y), (xi, y + 44)], fill=BORDO)
        dr.rectangle([xs[0] + 8, y + 9, xs[1] - 8, y + 35], outline=CAMPO, fill='white')
        dr.text((xs[0] + 14, y + 13), dato, font=f(N_REG, 14), fill=INK)
        dr.line([(xs[1] - 24, y + 19), (xs[1] - 19, y + 24), (xs[1] - 14, y + 19)], fill=INK,
                width=2)
        dr.rectangle([xs[1] + 8, y + 9, xs[2] - 8, y + 35], outline=CAMPO, fill=S.SOLA_LETTURA)
        dr.text((xs[1] + 14, y + 13), ante, font=f(N_REG, 14), fill=INK)
        dr.rectangle([xs[2] + 8, y + 9, xs[3] - 8, y + 35], outline=CAMPO, fill='white')
        dr.text((xs[2] + 14, y + 13), nuovo, font=f(N_BLD, 14), fill=INK)
        xm = (xs[3] + xs[4]) / 2       # la croce per togliere la riga, disegnata a linee
        dr.line([(xm - 6, y + 16), (xm + 6, y + 28)], fill=ROSSO, width=3)
        dr.line([(xm - 6, y + 28), (xm + 6, y + 16)], fill=ROSSO, width=3)
        y += 44
    dr.text((xs[0], y + 10), "+ AGGIUNGI CORREZIONE", font=f(N_BLD, 14), fill=S.BLU_ICONA)
    y += 40
    evidenzia(dr, (xs[0] - 10, yb - 8, xs[-1] + 10, y))
    pastiglia(dr, xs[-1] + 10, yb - 8, 3)
    y += 30

    # 4. il testo, composto dalle correzioni
    y = _sezione(dr, y, "Rettificazione")
    yb = y
    _area(dr, c[0], y, W - 2 * M - 120, 86,
          "Ai sensi dell’art. 98 1° comma D.P.R. 396/2000 si provvede alla correzione dell’errore "
          "materiale sull’atto controscritto nel senso che laddove si legge: GIULIA debba invece "
          "leggersi GIULIANA; laddove si legge: BIANCHII debba invece leggersi BIANCHI",
          fondo=S.SOLA_LETTURA)
    dr.text((c[0], y + 94), "Composto dalle righe della tabella: non si scrive a mano, così il "
            "testo e l’atto corretto dicono la stessa cosa.", font=f(N_ITA, 14), fill=MUTED)
    evidenzia(dr, (c[0] - 10, yb - 8, W - M - 70, yb + 118))
    pastiglia(dr, W - M - 70, yb - 8, 4)
    y += 140

    # 5. i dati che SIPO valorizza
    y = _sezione(dr, y, "Dati dell’annotazione per ANSC (valorizzati da SIPO)")
    yb = y
    _coppia(dr, c[0], y, "Numero comunale", "staccato alla conferma")
    _coppia(dr, c[1] + 40, y, "Data e ora di formazione", "alla conferma")
    y += 30
    _coppia(dr, c[0], y, "Atto corretto (eventoModificato)", "atto letto da ANSC con le "
            "correzioni applicate")
    pastiglia(dr, W - M - 30, yb - 4, 5)
    y += 50
    dr.line([(M, y), (W - M, y)], fill='#bdbdbd', width=1)
    y += 24
    S.bottone(dr, M + 20, y, "INDIETRO")
    xb = W - M - 20 - (lx(dr, "SALVA PROPOSTA", f(N_BLD, 13)) + 28)
    S.bottone(dr, xb, y, "SALVA PROPOSTA")
    yf = nota(dr, y + 56, [
        (1, "Estremi tradizionali tra parentesi e identificativo ANSC in grassetto: ne vengono "
            "datiRettifica.eventoCollegato."),
        (2, "Nuovo: la corrispondenza con ANSC. La formula 190 di SIPO per l’art. 98 diventa il "
            "caso d’uso dell’errore materiale con la formula 888 di ANSC."),
        (3, "Al posto dei due campi liberi: il dato si sceglie fra quelli correggibili, il valore "
            "da sostituire si legge dall’atto, l’operatore scrive solo il nuovo."),
        (4, "composizioneCompleta: la formula con i valori della tabella, in sola lettura."),
        (5, "eventoModificato, numero comunale, data e ora: li costruisce SIPO.")])
    S.ritaglia(im, yf, dest)
    return dest


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for nome, fn in (('ricerca_idansc_a_campo.png', variante_a),
                     ('ricerca_idansc_b_casella.png', variante_b),
                     ('ricerca_idansc_c_risultati.png', risultati),
                     ('ricerca_idansc_d_dettaglio.png', dettaglio),
                     ('annullamento_r013.png', annullamento),
                     ('proposta_art98.png', proposta_art98)):
        print(fn(os.path.join(OUT, nome)))
