# -*- coding: utf-8 -*-
"""Pagina «Anteprima · Validazione» di SIPO, come dalla scheda del processo (08/11/2026).

Scheda (img/workflow_ansc_sipo.pptx, riga «Anteprima · Validazione (nuova pagina)»): validazione
di metadati e allegati; si salvano gli idAnsc; preparazione del payload e invio R009; gestione
di errori e forzature → stato ANSC 2 CONFERMATO. Scelte dell'utente: testo dell'atto con
pannello di validazione accanto, esito KO ed esito OK, forzatura attiva, atto di morte.

Tre schermate:
  av_1_ko_errori.png     R009 respinge (400001/400003): niente in ANSC, si corregge e si rivalida
  av_2_ko_forzatura.png  R009 segnala anomalie superabili e restituisce il forcingCode
  av_3_ok.png            R009 deposita: idAnsc, idEvento, idTipoEvento salvati, 2 CONFERMATO

Fonti: R009_validazione.yaml (forcingCode in richiesta e risposta; idEvento/idAnsc/idTipoEvento),
Changelog ANSC (forcingCode per omocodia dell'intestatario e atti atipici), «Codici d'errore.xlsx»,
Mapping Morte_001 (UC 2101, allegati facoltativi), ANSC_01 (2 = MORTE), ANSC_08 (3 Inserito),
analisi v3.58 («Il codice di forzatura», forzatura_validazione). Dati di fantasia.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_anteprima_validazione.py
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S   # noqa: E402
from schermate_sipo_wf import (f, lx, avvolgi, M, W, INK, MUTED, BORDO, ROSSO, N_BLD,  # noqa: E402
                               N_REG, N_ITA, AVVISI)

OUT = os.path.join(S.IMG, 'anteprima_validazione')
VERDE = '#2e7d32'
ROSSO_X = '#c62828'
AMBRA = '#b26a00'

UC = "2101 – Decesso in abitazione o in luogo pubblico"
NUM = "004218"
ID_ANSC = "2026-10527702-4218-058091"

COL_SX = 660                       # larghezza dell'anteprima
X_DX = M + COL_SX + 20             # colonna dei pannelli
L_DX = W - M - X_DX


# ------------------------------------------------------------------------- parti comuni
def blocco(dr, y, titolo, contenuto):
    """Pannello alto quanto il contenuto: prima si misura su una tela di prova, poi si disegna."""
    prova = ImageDraw.Draw(Image.new('RGB', (W, 3000), 'white'))
    alt = contenuto(prova, y + 50) - y + 6
    S.pannello(dr, y, titolo, alt, X_DX, L_DX)
    contenuto(dr, y + 50)
    return y + alt + 16


def arrivo(dr, y):
    testa = "Da Anteprima:"
    corpo = ("VALIDA. Numero comunale " + NUM + " staccato da be-numeratore-comunale; modello "
             "evento costruito dai dati dell’atto (revisione 3) e inviato ad ANSC con "
             "R009 /validazione/evento.")
    bordo, fondo = AVVISI['ok']
    fb, fr = f(N_BLD, 15), f(N_REG, 15)
    larg = W - 2 * M
    righe = avvolgi(dr, corpo, fr, larg - 60 - lx(dr, testa, fb))
    h = 16 + 20 * len(righe)
    dr.rectangle([M, y, M + larg, y + h], fill=fondo, outline=bordo, width=2)
    dr.rectangle([M, y, M + 6, y + h], fill='#3f8f5f')
    S.spunta(dr, M + 18, y + 12, '#3f8f5f', 3)
    dr.text((M + 40, y + 8), testa, font=fb, fill='#2e6b43')
    x = M + 46 + lx(dr, testa, fb)
    for i, r in enumerate(righe):
        dr.text((x, y + 8 + i * 20), r, font=fr, fill=INK)
    return y + h + 16


def testata(dr, y, stato_ansc, id_ansc):
    y0 = y
    y = S.pannello(dr, y, "Atto di morte – stato dell’integrazione con ANSC", 150)
    larg = W - 2 * M - 24
    x = M + 12
    for quota, et, val in ((0.34, "Caso d’uso ANSC (UC)", UC), (0.12, "Numero comunale", NUM),
                           (0.20, "Identificativo nazionale", id_ansc),
                           (0.17, "Stato ANSC", stato_ansc), (0.17, "Stato SIPO", "1 IN LAVORAZIONE")):
        w = int(larg * quota) - 12
        S.campo(dr, x, y, w, et, val, 'lettura')
        x += w + 12
    y += 58
    dr.text((M + 12, y), "Ufficiale dello stato civile:", font=f(N_BLD, 14), fill=INK)
    dr.text((M + 190, y), "NOME COGNOME", font=f(N_REG, 14), fill=INK)
    sess = "Sessione ANSC: OTP valido, tempo residuo 2 h 48 min"
    fs = f(N_BLD, 14)
    sw = lx(dr, sess, fs) + 24
    bordo, fondo = AVVISI['ok']
    dr.rounded_rectangle([W - M - 12 - sw, y - 4, W - M - 12, y + 20], radius=10, fill=fondo,
                         outline=bordo)
    dr.text((W - M - sw, y - 1), sess, font=fs, fill='#2e6b43')
    return y0 + 150 + 16


TESTO = [
    "L’anno DUEMILAVENTISEI, addì OTTO del mese di NOVEMBRE alle ore DIECI e minuti TRENTA "
    "nella casa Comunale.",
    "Avanti a me NOME COGNOME Ufficiale dello Stato Civile di Roma Capitale per delegazione "
    "avuta, è comparsa BIANCHI LAURA nata in ROMA (RM) il 12 MARZO 1980, residente in "
    "ROMA (RM), che mi ha dichiarato quanto segue:",
    "Il giorno SEI del mese di NOVEMBRE dell’anno DUEMILAVENTISEI alle ore QUATTORDICI e "
    "minuti VENTI, nella casa posta in ROMA, VIA DEI GERANI 14,",
    "è morto: ROSSI MARIO",
    "nato in NAPOLI (NA) il 3 GIUGNO 1950",
    "residente in: ROMA (RM)",
    "cittadinanza: ITALIANA",
    "che era CONIUGATO con BIANCHI LAURA.",
    "Il presente atto viene letto all’intervenuta, la quale, insieme con me, lo sottoscrive.",
]


def anteprima(im, dr, y, alt):
    """Il testo dell'atto come nella pagina «Anteprima Atto» di SIPO, con la filigrana."""
    x0, x1 = M, M + COL_SX
    dr.text((x0, y), "Anteprima dell’atto", font=f(N_BLD, 15), fill=INK)
    y += 26
    dr.rectangle([x0, y, x1, y + alt], outline=ROSSO, width=2)
    px0, px1 = x0 + 40, x1 - 40
    py = y + 34
    # riquadro di testa
    dr.rectangle([px0, py, px1, py + 96], outline='#444444', width=1)
    sx = px0 + int((px1 - px0) * 0.62)
    dr.line([(sx, py), (sx, py + 96)], fill='#444444')
    dr.text((px0 + 8, py + 8), "ATTI DI MORTE", font=f(N_BLD, 16), fill=INK)
    dr.text((px0 + 8, py + 32), "Numero comunale " + NUM, font=f(N_REG, 15), fill=INK)
    dr.text((px0 + 8, py + 56), "UC ANSC " + UC.split(' ')[0], font=f(N_REG, 15), fill=INK)
    for i, t in enumerate(("C: ROSSI", "N: MARIO", "S: M")):
        dr.text((sx + 8, py + 8 + i * 22), t, font=f(N_BLD, 15), fill=INK)
    # corpo
    by = py + 96
    corpo_alt = alt - (by - y) - 34
    dr.rectangle([px0, by, px1, by + corpo_alt], outline='#444444', width=1)
    ft = f(N_REG, 15)
    ty = by + 14
    for par in TESTO:
        for r in avvolgi(dr, par, ft, px1 - px0 - 20):
            dr.text((px0 + 10, ty), r, font=ft, fill=INK)
            ty += 21
        ty += 4
    ty += 20
    dr.text((px0 + 10, ty), "." * 60, font=ft, fill=INK)
    dr.text((px0 + 10, ty + 22), "La dichiarante", font=f(N_REG, 13), fill=MUTED)
    dr.text((px1 - 190, ty + 60), "L’Ufficiale dello Stato Civile", font=ft, fill=INK)
    dr.text((px1 - 190, ty + 96), "." * 38, font=ft, fill=INK)
    # filigrana
    strato = Image.new('RGBA', (COL_SX, alt), (0, 0, 0, 0))
    ds = ImageDraw.Draw(strato)
    fw = f(N_BLD, 120)
    tw = lx(ds, "ANTEPRIMA", fw)
    testo = Image.new('RGBA', (tw + 20, 160), (0, 0, 0, 0))
    ImageDraw.Draw(testo).text((10, 0), "ANTEPRIMA", font=fw, fill=(120, 120, 120, 55))
    testo = testo.rotate(58, expand=True)
    strato.paste(testo, ((COL_SX - testo.width) // 2, (alt - testo.height) // 2), testo)
    im.paste(strato, (x0, y), strato)
    return y + alt


def icona(dr, x, y, esito):
    if esito == 'ok':
        dr.ellipse([x, y, x + 18, y + 18], fill=VERDE)
        S.spunta(dr, x + 4, y + 5, 'white', 2)
    elif esito == 'ko':
        dr.ellipse([x, y, x + 18, y + 18], fill=ROSSO_X)
        dr.line([(x + 5, y + 5), (x + 13, y + 13)], fill='white', width=2)
        dr.line([(x + 13, y + 5), (x + 5, y + 13)], fill='white', width=2)
    elif esito == 'att':
        dr.ellipse([x, y, x + 18, y + 18], fill=AMBRA)
        dr.text((x + 7, y), "!", font=f(N_BLD, 15), fill='white')
    else:                                           # neutro
        dr.ellipse([x, y, x + 18, y + 18], outline='#9a9a9a', width=2)


def voce(dr, x, y, larg, esito, titolo, dettaglio):
    icona(dr, x, y + 1, esito)
    dr.text((x + 28, y), titolo, font=f(N_BLD, 14), fill=INK)
    y += 20
    for r in avvolgi(dr, dettaglio, f(N_REG, 13), larg - 28):
        dr.text((x + 28, y), r, font=f(N_REG, 13), fill=MUTED)
        y += 17
    return y + 8


def controlli(dr, y):
    """Pannello dei controlli locali: metadati e allegati, prima e dopo l'invio."""
    return blocco(dr, y, "Metadati e allegati – controlli prima dell’invio", _controlli)


def _controlli(dr, y):
    x, w = X_DX + 14, L_DX - 28
    y = voce(dr, x, y, w, 'ok', "Dati obbligatori dell’UC 2101",
             "tutti i campi che la configurazione dell’UC dichiara obbligatori sono valorizzati")
    y = voce(dr, x, y, w, 'ok', "Decodifiche",
             "i valori SIPO sono tradotti nei dizionari ANSC (stato civile, cittadinanza, luogo)")
    y = voce(dr, x, y, w, 'ok', "Soggetti cercati in ANSC (R005)",
             "deceduto e dichiarante: identificativo ANSC presente")
    y = voce(dr, x, y, w, 'ok', "Certificato necroscopico – R001",
             "certificato_necroscopico.pdf · stato ANSC 3 Inserito · facoltativo per l’UC")
    y = voce(dr, x, y, w, 'neutro', "Documento autorizzativo",
             "non caricato · facoltativo per l’UC")
    return voce(dr, x, y, w, 'ok', "Firmatari",
                "BIANCHI LAURA, dichiarante · firma autografa sulla stampa, poi scansione (R006)")


def tabella_esiti(dr, y, righe):
    """Segnalazioni restituite da R009: tipo, descrizione, dove si corregge."""
    x = X_DX + 12
    larg = (110, 250, L_DX - 24 - 360)
    fi, fr = f(N_BLD, 13), f(N_REG, 13)
    tot = sum(larg)
    dr.rectangle([x, y, x + tot, y + 30], fill='#f2f2f2', outline=BORDO)
    cx = x
    for t, w in zip(("Tipo", "Descrizione restituita da ANSC", "Dove si corregge"), larg):
        dr.text((cx + 6, y + 7), t, font=fi, fill=INK)
        cx += w
    y += 30
    for tipo, desc, dove in righe:
        celle = [avvolgi(dr, tipo, fr, larg[0] - 12), avvolgi(dr, desc, fr, larg[1] - 12),
                 avvolgi(dr, dove, fr, larg[2] - 12)]
        h = 12 + 17 * max(len(c) for c in celle) + 20
        dr.rectangle([x, y, x + tot, y + h], fill='white', outline=BORDO)
        cx = x
        for j, (c, w) in enumerate(zip(celle, larg)):
            ty = y + 7
            for r in c:
                dr.text((cx + 6, ty), r, font=fr, fill=INK)
                ty += 17
            if j == 2:
                dr.text((cx + 6, ty + 2), "VAI ALLA PAGINA", font=f(N_BLD, 12), fill=ROSSO)
            cx += w
        y += h
    return y + 12


def esito(dr, y, caso):
    return blocco(dr, y, "Esito della validazione – R009", lambda d, yy: _esito(d, yy, caso))


def _esito(dr, y, caso):
    xi, li = X_DX + 12, L_DX - 24
    if caso == 'errori':
        y = S.avviso(dr, y, "ANSC ha respinto la validazione: l’atto non è stato depositato e in "
                     "ANSC non resta nulla. Il numero comunale " + NUM + " resta all’atto. "
                     "Correggere i dati e validare di nuovo.", 'errore', xi, li)
        y = tabella_esiti(dr, y, [
            ("Errore 400001", "Campo obbligatorio non compilato: data di nascita del "
             "comparente 1", "Dettaglio – dichiarante"),
            ("Errore 400003", "Dati in ingresso non corretti: ora del decesso", "Dettaglio – "
             "evento")])
    elif caso == 'forzatura':
        y = S.avviso(dr, y, "ANSC segnala anomalie superabili e restituisce un codice di "
                     "forzatura: l’atto non è stato depositato. Se i dati sono giusti l’ufficiale "
                     "può validare con forzatura, altrimenti si correggono.", 'attenzione', xi, li)
        y = tabella_esiti(dr, y, [
            ("Anomalia superabile", "Intestatario con anagrafica identica a un soggetto già "
             "presente in ANSC (omocodia)", "Dettaglio – deceduto")])
    else:
        y = S.avviso(dr, y, "Validazione riuscita: l’atto è depositato in ANSC nello stato "
                     "2 CONFERMATO. Si prosegue con le firme.", 'ok', xi, li)
        fi, fr = f(N_BLD, 13), f(N_REG, 13)
        dr.text((xi, y), "Identificativi restituiti da ANSC e salvati sull’atto", font=fi, fill=INK)
        y += 24
        for et, val in (("idAnsc – identificativo nazionale", ID_ANSC),
                        ("idEvento – identificativo interno", "4245234"),
                        ("idTipoEvento", "2 MORTE")):
            dr.rectangle([xi, y, xi + li, y + 28], fill='white', outline=BORDO)
            dr.text((xi + 8, y + 6), et, font=fr, fill=MUTED)
            dr.text((xi + 250, y + 6), val, font=f(N_BLD, 14), fill=INK)
            y += 28
        y += 10
        for r in avvolgi(dr, "Con l’esito si salva il modello evento validato (revisione 3): se "
                         "i dati cambiano prima della firma dell’ufficiale, l’atto torna in bozza "
                         "e si valida di nuovo con lo stesso identificativo nazionale.",
                         f(N_ITA, 13), li):
            dr.text((xi, y), r, font=f(N_ITA, 13), fill=MUTED)
            y += 17
    return y


def forzatura(dr, y, attiva):
    return blocco(dr, y, "Forzatura – riservata all’ufficiale dello stato civile",
                  lambda d, yy: _forzatura(d, yy, attiva))


def _forzatura(dr, y, attiva):
    xi, li = X_DX + 12, L_DX - 24
    w2 = (li - 12) // 2
    if attiva:
        S.campo(dr, xi, y, w2, "Codice di forzatura restituito", "XXXXX_1234", 'lettura')
        S.campo(dr, xi + w2 + 12, y, w2, "Ufficiale che forza", "NOME COGNOME", 'lettura')
        y += 62
        righe = avvolgi(dr, "Confermo, come ufficiale dello stato civile, che le anomalie elencate "
                        "corrispondono alla realtà e chiedo di validare con forzatura",
                        f(N_REG, 14), li - 26)
        S.casella(dr, xi, y, righe[0], segnata=True)
        for i, r in enumerate(righe[1:], 1):
            dr.text((xi + 22, y + i * 19), r, font=f(N_REG, 14), fill=INK)
        y += 19 * len(righe) + 10
        nota = ("R009 si ripete con il codice di forzatura. A operazione avvenuta codice, anomalie "
                "e ufficiale si registrano in forzatura_validazione. Per gli atti anomali ANSC "
                "dichiara non ancora implementato il ciclo delle conferme.")
        col = MUTED
    else:
        S.campo(dr, xi, y, w2, "Codice di forzatura restituito", "", 'lettura')
        S.campo(dr, xi + w2 + 12, y, w2, "Ufficiale che forza", "", 'lettura')
        y += 62
        S.casella(dr, xi, y, "Confermo la forzatura delle anomalie elencate", attiva=False)
        y += 30
        nota = ("Non disponibile: ANSC non ha restituito un codice di forzatura. Gli errori "
                "elencati non sono superabili e vanno corretti.")
        col = MUTED
    for r in avvolgi(dr, nota, f(N_ITA, 13), li):
        dr.text((xi, y), r, font=f(N_ITA, 13), fill=col)
        y += 17
    return y


# -------------------------------------------------------------------------------- pagine
def disegna(caso, nome):
    im, dr, y = S.pagina("Dichiarazione Morte – Anteprima Atto · Validazione ANSC", alt=1900)
    y = arrivo(dr, y)
    if caso == 'ok':
        y = testata(dr, y, "2 CONFERMATO", ID_ANSC)
    else:
        y = testata(dr, y, "— (nessun atto)", "—")
    ytop = y
    yd = controlli(dr, ytop)
    yd = esito(dr, yd, caso)
    if caso != 'ok':
        yd = forzatura(dr, yd, caso == 'forzatura')
    ys = anteprima(im, dr, ytop, max(yd - ytop - 42, 640))
    y = max(yd, ys + 16)
    destra = {
        'errori': [("INTERROMPI", True), ("VALIDA DI NUOVO", True),
                   ("VALIDA CON FORZATURA", False), ("FIRME DEI DICHIARANTI", False)],
        'forzatura': [("INTERROMPI", True), ("VALIDA DI NUOVO", True),
                      ("VALIDA CON FORZATURA", True), ("FIRME DEI DICHIARANTI", False)],
        'ok': [("INTERROMPI", True), ("VALIDA DI NUOVO", False),
               ("VALIDA CON FORZATURA", False), ("FIRME DEI DICHIARANTI", True)],
    }[caso]
    y = S.pulsantiera(dr, y, [("TORNA AI DATI", True)], destra)
    os.makedirs(OUT, exist_ok=True)
    return S.ritaglia(im, y, os.path.join(OUT, nome))


if __name__ == '__main__':
    print(disegna('errori', 'av_1_ko_errori.png'))
    print(disegna('forzatura', 'av_2_ko_forzatura.png'))
    print(disegna('ok', 'av_3_ok.png'))
