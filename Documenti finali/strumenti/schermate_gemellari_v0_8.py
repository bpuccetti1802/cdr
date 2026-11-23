# -*- coding: utf-8 -*-
"""Ipotesi di schermata, nello stile di SIPO, per l'analisi delle nascite gemellari v0.8
(21/11/2026). Primitive di `schermate_sipo_wf`.

Decisioni dell'utente (21/11/2026):
  * caso 1 (stesso UC): il testo dell'atto lo compone ANSC; SIPO lo recupera da ANSC e lo
    riporta sull'atto di SIPO;
  * caso 2 (UC diversi): si lavora come per gli atti a testo libero, ciclando sugli atti SIPO
    dei gemelli e permettendo la copia del testo sulla web app, con una PRATICA GUIDATA;
  * in entrambi i casi una FINESTRA DI RACCORDO mostra con chiarezza i numeri comunali di
    ciascun gemello, per l'abbinamento corretto;
  * la SEQUENZA DELLE SCHERMATE dei due casi.

Schermate (img/gemellari/):
  gem8_c1_raccordo.png   finestra di raccordo dopo la prenotazione (caso 1)
  gem8_c1_gemello.png    DEFINISCI, gemello 2 di 3, sul passo della firma del dichiarante
  gem8_c1_testo.png      gemello 2 formato: testo recuperato da ANSC e atto definito in SIPO
  gem8_c1_esito.png      esito del parto (caso 1)
  gem8_c2_riepilogo.png  riepilogo dei gemelli con UC diversi (caso 2)
  gem8_c2_raccordo.png   finestra di raccordo prima della web app (caso 2)
  gem8_c2_guidata.png    pratica guidata per la web app, gemello 2 di 3
  gem8_c2_recupero.png   finestra di raccordo dopo RECUPERA GEMELLI (caso 2)
  gem8_c2_esito.png      esito del parto (caso 2)
  gem8_seq_caso1.png, gem8_seq_caso2.png   la sequenza delle schermate
Nomi e codici sono di esempio; nessun dato di persone reali.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_gemellari_v0_8.py
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S                                       # noqa: E402
import schermate_gemellari_v0_5 as G5                               # noqa: E402

DIR = os.path.join(S.IMG, 'gemellari')
FATTO, ERRORE, ATTESA, CORSO = '#2e6b43', '#b00020', '#7a7a7a', S.ROSSO
VERDE, VERDE_F = '#3f8f5f', '#e3f3e8'
GIALLO_EVID = '#fff176'

# caso 1: stesso UC
C1 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13617",
       "2026-10527618-13617-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13618",
       "2026-10527619-13618-058091"),
      ("3", "NATO 3 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13619",
       "2026-10527620-13619-058091"))
# caso 2: UC diversi (nato vivo, nato morto, nato vivo poi deceduto)
C2 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13640",
       "2026-10531102-13640-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "2 nato morto", "11111100", "13641",
       "2026-10531103-13641-058091"),
      ("3", "NATO 3 — COGNOME NOME", "M", "3 nato vivo poi deceduto", "11111200", "13642",
       "2026-10531104-13642-058091"))


def _salva(im, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest)
    return dest


# ------------------------------------------------------------------ la finestra di raccordo
def _id_evidenziato(dr, x, y, id_ansc, numero, ft, evidenzia=True):
    """L'identificativo nazionale con il numero comunale che contiene evidenziato."""
    if not id_ansc:
        dr.text((x, y), "assegnato dalla web app", font=S.f(S.N_ITA, 15), fill=S.MUTED)
        return
    prima, _, dopo = id_ansc.partition("-" + numero + "-")
    pezzi = ((prima + "-", None), (numero, GIALLO_EVID if evidenzia else None), ("-" + dopo, None))
    for testo, fondo in pezzi:
        w = S.lx(dr, testo, ft)
        if fondo:
            dr.rectangle([x - 2, y - 2, x + w + 2, y + 20], fill=fondo)
        dr.text((x, y), testo, font=ft, fill=S.INK)
        x += w


def _pastiglia(dr, x, y, testo, bordo, fondo, colore):
    ft = S.f(S.N_BLD, 14)
    w = S.lx(dr, testo, ft) + 24
    dr.rounded_rectangle([x, y, x + w, y + 26], radius=13, fill=fondo, outline=bordo, width=2)
    dr.text((x + 12, y + 5), testo, font=ft, fill=colore)
    return x + w


def _scheda(dr, x, y, w, g, modo):
    """Una scheda per gemello: chi è, il numero comunale in grande, l'identificativo, l'esito.

    modo: 'prenotato' (caso 1), 'da_riportare' (caso 2 prima della web app), 'recuperato'.
    """
    pos, nome, sesso, tipo, uc, num, id_ansc = g
    h = 372
    dr.rectangle([x, y, x + w, y + h], fill='white', outline=S.BORDO, width=2)
    dr.rectangle([x, y, x + w, y + 34], fill='#f2f2f2', outline=S.BORDO)
    dr.text((x + 12, y + 8), "Gemello %s di 3" % pos, font=S.f(S.N_BLD, 16), fill=S.INK)
    fr, fb = S.f(S.N_REG, 14), S.f(S.N_BLD, 14)
    yy = y + 44
    for et, val in (("Nato", nome), ("Sesso", sesso), ("Tipologia di nascita", tipo),
                    ("UC del nato", uc)):
        dr.text((x + 12, yy), et, font=fr, fill=S.MUTED)
        dr.text((x + 150, yy), val, font=fb, fill=S.INK)
        yy += 21
    # il numero comunale in grande
    yy += 6
    dr.rectangle([x + 12, yy, x + w - 12, yy + 84], fill=S.ROSSO)
    dr.text((x + 24, yy + 6), "NUMERO COMUNALE", font=S.f(S.N_BLD, 14), fill='white')
    fbig = S.f(S.N_BLD, 52)
    dr.text((x + 24, yy + 22), num, font=fbig, fill='white')
    dr.text((x + 30 + S.lx(dr, num, fbig), yy + 50), "/ 2026", font=S.f(S.N_BLD, 20),
            fill='white')
    if modo == 'da_riportare':
        t = "%s° sulla web app" % pos
        dr.text((x + w - 24 - S.lx(dr, t, S.f(S.N_BLD, 16)), yy + 30), t,
                font=S.f(S.N_BLD, 16), fill='#ffd54f')
    yy += 96
    dr.text((x + 12, yy), "Identificativo nazionale", font=fr, fill=S.MUTED)
    yy += 20
    _id_evidenziato(dr, x + 12, yy, id_ansc if modo != 'da_riportare' else None, num,
                    S.f(S.N_BLD, 16))
    yy += 32
    if modo == 'da_riportare':
        _pastiglia(dr, x + 12, yy, "DA RIPORTARE SULLA WEB APP", '#9cc3ea', '#e8f1fb', '#1b4f8a')
    else:
        S.spunta(dr, x + 14, yy + 4, VERDE, 3)
        dr.text((x + 34, yy), "numero contenuto nell’identificativo", font=fr, fill=FATTO)
        yy += 22
        if modo == 'recuperato':
            S.spunta(dr, x + 14, yy + 4, VERDE, 3)
            dr.text((x + 34, yy), "5 FIRMATO DA USC · intestatario e tipologia", font=fr,
                    fill=FATTO)
        else:
            S.spunta(dr, x + 14, yy + 4, VERDE, 3)
            dr.text((x + 34, yy), "previsto %s = assegnato %s" % (num, num), font=fr, fill=FATTO)
        yy += 28
        _pastiglia(dr, x + 12, yy, "ABBINATO", '#9fd0ad', VERDE_F, FATTO)
    return y + h


def _finestra(titolo, intro, gemelli, modo, nota, bottoni, alt=760):
    larg = S.W
    im = Image.new('RGB', (larg, alt), '#7f7f7f')
    dr = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 30, 24, larg - 30, alt - 24
    dr.rectangle([x0, y0, x1, y1], fill='white', outline=S.BORDO)
    dr.rectangle([x0, y0, x1, y0 + 42], fill=S.ROSSO)
    dr.text((x0 + 16, y0 + 10), titolo, font=S.f(S.N_BLD, 18), fill='white')
    ft = S.f(S.N_BLD, 13)
    dr.text((x1 - S.lx(dr, "IPOTESI DI SCHERMATA", ft) - 16, y0 + 14), "IPOTESI DI SCHERMATA",
            font=ft, fill='#f3d7de')
    y = S.avviso(dr, y0 + 58, intro, 'info', x=x0 + 16, larg=x1 - x0 - 32)
    w = (x1 - x0 - 32 - 2 * 16) // 3
    for i, g in enumerate(gemelli):
        _scheda(dr, x0 + 16 + i * (w + 16), y, w, g, modo)
    y += 372 + 14
    y = S.avviso(dr, y, nota, 'attenzione', x=x0 + 16, larg=x1 - x0 - 32)
    S.bottoni_dx(dr, y + 4, bottoni, x_fine=x1 - 16)
    im = im.crop((0, 0, larg, y + 4 + 30 + 20 + 24))
    ImageDraw.Draw(im).rectangle([30, im.height - 24, larg - 30, im.height], fill='#7f7f7f')
    ImageDraw.Draw(im).line([(30, im.height - 24), (larg - 30, im.height - 24)], fill=S.BORDO)
    return im


def c1_raccordo(dest):
    im = _finestra(
        "Raccordo dei numeri comunali – prenotazione riuscita",
        "DEFINISCI ha staccato 3 numeri comunali consecutivi (be-numeratore-comunale) e ANSC ha "
        "prenotato 3 atti con il caso d’uso 11111000 (R009 /prenota/evento). Ciascun "
        "identificativo nazionale è abbinato al gemello del numero comunale che contiene: "
        "verificare che ogni nato abbia il suo numero prima di proseguire.",
        C1, 'prenotato',
        "I numeri sono riservati e gli atti esistono in ANSC in BOZZA: da qui in avanti il numero "
        "dei gemelli non si può più modificare. Con PROSEGUI si apre l’atto del gemello 1.",
        [("SOSPENDI", True), ("STAMPA PROMEMORIA", True), ("PROSEGUI CON IL GEMELLO 1", True)])
    return _salva(im, dest)


def c2_raccordo(dest):
    im = _finestra(
        "Raccordo dei numeri comunali – da riportare sulla web app ANSC",
        "I nati hanno casi d’uso ANSC diversi: gli atti si formano sulla web app. DATI PER ANSC "
        "ha staccato 3 numeri comunali consecutivi. Sulla web app indicare 3 gemelli (nati morti "
        "compresi) e riportare i numeri nell’ordine qui sotto; in ciascuna bozza indicare la "
        "tipologia di nascita del nato.",
        C2, 'da_riportare',
        "I numeri sono riservati a questi atti fino al rientro in SIPO. Con AVVIA LA PRATICA "
        "GUIDATA SIPO presenta un gemello alla volta, con il suo numero e il testo da copiare.",
        [("INDIETRO", True), ("STAMPA PROMEMORIA", True), ("AVVIA LA PRATICA GUIDATA", True)])
    return _salva(im, dest)


def c2_recupero(dest):
    im = _finestra(
        "Raccordo dei numeri comunali – esito di RECUPERA GEMELLI",
        "Per ciascun numero comunale del parto SIPO ha cercato in ANSC l’atto del Comune "
        "nell’anno (R005) e lo ha confrontato con il gemello che porta quel numero: numero "
        "contenuto nell’identificativo, stato 5 FIRMATO DA USC, intestatario (sesso, data e ora "
        "di nascita) e tipologia di nascita.",
        C2, 'recuperato',
        "Tutti i gemelli sono abbinati: DEFINISCI GEMELLI definisce gli atti in SIPO. Un esito "
        "NON TROVATO, NON FIRMATO o INCOERENTE ferma la definizione dell’intero parto.",
        [("CHIUDI", True), ("DEFINISCI GEMELLI", True)])
    return _salva(im, dest)


# ------------------------------------------------------------------ elementi delle pagine
def _barra_gemelli(dr, y, gemelli, stati):
    """La fila dei gemelli: numero comunale e stato di ciascuno; il corrente in evidenza."""
    larg = S.W - 2 * S.M
    w = (larg - 2 * 14) // 3
    for i, (g, (stato, tipo)) in enumerate(zip(gemelli, stati)):
        x = S.M + i * (w + 14)
        fondo, bordo, col = {'fatto': (VERDE_F, '#9fd0ad', FATTO),
                             'corso': ('#fbeef1', S.ROSSO, S.ROSSO),
                             'attesa': ('#f4f4f4', S.BORDO, ATTESA)}[tipo]
        dr.rectangle([x, y, x + w, y + 64], fill=fondo, outline=bordo, width=3 if tipo == 'corso'
                     else 1)
        dr.text((x + 14, y + 8), "Gemello %s · %s" % (g[0], g[3]), font=S.f(S.N_BLD, 14),
                fill=S.INK)
        dr.text((x + 14, y + 30), "N. comunale", font=S.f(S.N_REG, 13), fill=S.MUTED)
        dr.text((x + 90, y + 24), g[5], font=S.f(S.N_BLD, 26), fill=col)
        ts = S.f(S.N_BLD, 14)
        dr.text((x + w - 14 - S.lx(dr, stato, ts), y + 36), stato, font=ts, fill=col)
        if tipo == 'fatto':
            S.spunta(dr, x + w - 30, y + 12, VERDE, 3)
    return y + 64 + 16


def _passi(dr, y, voci, corrente):
    """I passi del gemello in lavorazione."""
    larg = S.W - 2 * S.M
    w = larg / len(voci)
    for i, v in enumerate(voci):
        x = S.M + i * w
        if i < corrente:
            fondo, col = VERDE, 'white'
        elif i == corrente:
            fondo, col = S.ROSSO, 'white'
        else:
            fondo, col = '#e6e6e6', '#555555'
        dr.polygon([(x, y), (x + w - 12, y), (x + w, y + 17), (x + w - 12, y + 34), (x, y + 34),
                    (x + 12, y + 17)], fill=fondo)
        ft = S.f(S.N_BLD, 13)
        t = ("%d · %s" % (i + 1, v))
        dr.text((x + (w - S.lx(dr, t, ft)) / 2, y + 9), t, font=ft, fill=col)
    return y + 34 + 18


def _testo_atto(dr, x, y, w, h, numero, gemelli, filigrana, fonte,
                nascita="è nato un bambino di sesso femminile, gemello con altri due, a cui dà il nome di NOME"):
    dr.rectangle([x, y, x + w, y + h], fill='#525659')
    px, pw = x + 26, w - 52
    dr.rectangle([px, y + 12, px + pw, y + h - 12], fill='white')
    fb, fr = S.f(S.N_BLD, 14), S.f(S.N_REG, 13)
    yy = y + 26
    dr.text((px + 18, yy), "ATTI DI NASCITA", font=fb, fill=S.INK)
    dr.text((px + pw - 18 - S.lx(dr, fonte, S.f(S.N_ITA, 12)), yy + 2), fonte,
            font=S.f(S.N_ITA, 12), fill=S.MUTED)
    yy += 20
    t = "Numero comunale " + numero
    dr.rectangle([px + 16, yy - 1, px + 20 + S.lx(dr, t, fr), yy + 17], fill=GIALLO_EVID)
    dr.text((px + 18, yy), t, font=fr, fill=S.INK)
    yy += 28
    corpo = ("L’anno DUEMILAVENTISEI, addì VENTUNO del mese di NOVEMBRE nella Casa Comunale. "
             "Avanti a me NOME COGNOME, Ufficiale dello Stato Civile del Comune di ROMA, è "
             "comparso COGNOME NOME, il quale mi ha dichiarato che il giorno DICIOTTO del mese di "
             "NOVEMBRE dell’anno DUEMILAVENTISEI, nella struttura sanitaria in ROMA, da COGNOME "
             "NOME " + nascita + ". Atti dei gemelli: " + gemelli + ".")
    for r in S.avvolgi(dr, corpo, fr, pw - 36):
        if yy > y + h - 40:
            break
        dr.text((px + 18, yy), r, font=fr, fill=S.INK)
        yy += 18
    if filigrana:
        dr.text((px + pw / 2 - 90, y + h / 2 - 10), filigrana, font=S.f(S.N_BLD, 34),
                fill='#dddddd')
    return y + h


def _riquadro_azioni(dr, x, y, w, titolo, righe):
    h = 40 + 30 * len(righe) + 30
    dr.rectangle([x, y, x + w, y + h], fill='white', outline=S.BORDO)
    dr.rectangle([x, y, x + w, y + 34], fill='#f5f5f5', outline=S.BORDO)
    dr.text((x + 12, y + 9), titolo, font=S.f(S.N_BLD, 14), fill='#333333')
    yy = y + 46
    for fatto, testo in righe:
        if fatto is True:
            S.spunta(dr, x + 14, yy + 4, VERDE, 3)
            col = FATTO
        elif fatto is None:
            dr.ellipse([x + 14, yy + 2, x + 28, yy + 16], outline=S.ROSSO, width=2)
            col = S.ROSSO
        else:
            dr.rectangle([x + 14, yy + 2, x + 28, yy + 16], outline=S.INK, fill='white')
            col = S.INK
        rr = S.avvolgi(dr, testo, S.f(S.N_REG, 14), w - 50)[:2]
        for i, r in enumerate(rr):
            dr.text((x + 38, yy + i * 18), r, font=S.f(S.N_REG, 14), fill=col)
        yy += 30 + 18 * (len(rr) - 1)
    return y + h


def _testata_gemello(dr, y, g, stato_ansc, stato_sipo, id_ansc=None):
    y0 = y
    y = S.pannello(dr, y, "Atto di nascita del gemello %s – stato dell’integrazione con ANSC"
                   % g[0], 96)
    larg = S.W - 2 * S.M - 24
    x = S.M + 12
    for quota, et, val in ((0.26, "Caso d’uso ANSC (UC)", g[4] + " – Dic_Nasc_001"),
                           (0.12, "Numero comunale", g[5]),
                           (0.24, "Identificativo nazionale", id_ansc or g[6]),
                           (0.19, "Stato ANSC", stato_ansc), (0.19, "Stato SIPO", stato_sipo)):
        w = int(larg * quota) - 12
        S.campo(dr, x, y, w, et, val, 'lettura')
        x += w + 12
    return y0 + 96 + 14


PASSI_C1 = ("Documenti", "Anteprima e validazione", "Firma dichiarante", "Conformità",
            "Firma USC", "Testo da ANSC e definizione")


def c1_gemello(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Definisci gemelli · gemello 2 di 3", alt=1500)
    y = S.arrivo(dr, y, 1) if False else y
    bordo, fondo = S.AVVISI['ok']
    y = S.avviso(dr, y, "Da Anteprima e validazione: atto del gemello 2 validato (R009), stato "
                 "ANSC 2 CONFERMATO. Il testo mostrato è quello composto da ANSC (R010, copia per "
                 "la presa visione): è il testo che il dichiarante firma.", 'ok')
    y = _barra_gemelli(dr, y, C1, (("2 DEFINITO", 'fatto'), ("in lavorazione", 'corso'),
                                   ("in attesa", 'attesa')))
    y = _passi(dr, y, PASSI_C1, 2)
    y = _testata_gemello(dr, y, C1[1], "2 CONFERMATO", "1 IN LAVORAZIONE")
    xs, ws = S.M, 760
    dr.text((xs, y), "Testo dell’atto – composto da ANSC", font=S.f(S.N_BLD, 15), fill=S.INK)
    _testo_atto(dr, xs, y + 24, ws, 260, C1[1][5], C1[0][6] + ", " + C1[2][6], None,
                "fonte: ANSC, R010 presa visione")
    xr = xs + ws + 20
    _riquadro_azioni(dr, xr, y + 24, S.W - S.M - xr, "Firma del dichiarante (R006)", (
        (True, "Testo stampato e consegnato al dichiarante"),
        (None, "Caricare il PDF con la firma autografa del dichiarante"),
        (False, "Processo verbale caricato in ANSC"),
        (False, "Stato ANSC 4 FIRMATO DAL DICHIARANTE")))
    S.campo(dr, xr + 14, y + 24 + 190, S.W - S.M - xr - 28, "PDF firmato", "", 'file')
    y += 24 + 260 + 20
    y = S.pulsantiera(dr, y, [("SOSPENDI", True)], [("STAMPA", True), ("CARICA LA FIRMA", True)])
    S.ritaglia(im, y, dest)
    return dest


def c1_testo(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Definisci gemelli · gemello 2 di 3", alt=1500)
    y = S.avviso(dr, y, "Da Firma dell’USC: atto del gemello 2 firmato dall’ufficiale (R007), "
                 "stato ANSC 5 FIRMATO DA USC. L’atto è formato in ANSC: il suo testo è stato "
                 "recuperato da ANSC e riportato sull’atto di SIPO, che è stato definito.", 'ok')
    y = _barra_gemelli(dr, y, C1, (("2 DEFINITO", 'fatto'), ("2 DEFINITO", 'fatto'),
                                   ("in attesa", 'attesa')))
    y = _passi(dr, y, PASSI_C1, 6)
    y = _testata_gemello(dr, y, C1[1], "5 FIRMATO DA USC", "2 DEFINITO")
    xs, ws = S.M, 760
    dr.text((xs, y), "Testo dell’atto salvato in SIPO – fonte ANSC", font=S.f(S.N_BLD, 15),
            fill=S.INK)
    _testo_atto(dr, xs, y + 24, ws, 260, C1[1][5], C1[0][6] + ", " + C1[2][6], None,
                "fonte: ANSC")
    xr = xs + ws + 20
    _riquadro_azioni(dr, xr, y + 24, S.W - S.M - xr, "Riporto in SIPO", (
        (True, "Testo dell’atto recuperato da ANSC (il PDF della presa visione, R010)"),
        (True, "Salvato come documento dell’atto di SIPO (ATTO_SCANSIONATO), al posto del testo "
               "composto da SIPO"),
        (True, "Atto definito in SIPO: /finalizzaAtto, 2 DEFINITO"),
        (True, "Store aggiornato: ANSC_STATO_ATTO a 5, fase FIRMATO"),
        (False, "Il gemello 3 attende: si prosegue con GEMELLO SUCCESSIVO")))
    y += 24 + 260 + 20
    y = S.pulsantiera(dr, y, [("SOSPENDI", True)], [("APRI IL PDF", True),
                                                    ("GEMELLO SUCCESSIVO", True)])
    S.ritaglia(im, y, dest)
    return dest


def _esito(dest, gemelli, intro, colonna_testo, valori_testo):
    im, dr, y = S.pagina("Dichiarazione Nascita – Esito del parto")
    y = S.avviso(dr, y, intro, 'ok')
    y = G5._testata(dr, y, gemello="—", sessione="OTP valido · 2 h 05 min")
    cols = ("Pos.", "Nato", "N. comunale", "Identificativo nazionale", "Stato ANSC",
            "Stato SIPO", colonna_testo)
    larg = (50, 230, 110, 240, 170, 130, 370)
    ok = lambda t: G5._colore(t, FATTO)                             # noqa: E731
    righe = [(g[0], g[1], g[5], g[6], "5 FIRMATO DA USC", "2 DEFINITO", ok(v))
             for g, v in zip(gemelli, valori_testo)]
    y = S.pannello(dr, y, "Gemelli della pratica – atti formati in ANSC e definiti in SIPO",
                   60 + 34 * 4)
    y = S.tabella(dr, y, cols, larg, righe, x=S.M + 12) + 6
    y = S.pulsantiera(dr, y + 8, [("TORNA AL DETTAGLIO", True)], [("APRI I PDF", True)])
    S.ritaglia(im, y, dest)
    return dest


def c1_esito(dest):
    return _esito(dest, C1, "DEFINISCI concluso: i 3 atti del parto sono formati in ANSC e "
                  "definiti in SIPO, ciascuno con il testo recuperato da ANSC.",
                  "Testo in SIPO", ["da ANSC"] * 3)


def c2_esito(dest):
    return _esito(dest, C2, "DEFINISCI GEMELLI concluso: i 3 atti formati sulla web app sono "
                  "agganciati ai gemelli e definiti in SIPO.", "Testo in SIPO",
                  ["di SIPO, copiato sulla web app"] * 3)


def c2_riepilogo(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Riepilogo gemelli")
    y = S.avviso(dr, y, "La pratica è stata divisa in 3 atti. I nati hanno casi d’uso ANSC "
                 "diversi (nato vivo, nato morto, nato vivo poi deceduto): gli atti si formano "
                 "sulla web app ANSC. DATI PER ANSC stacca i numeri comunali e avvia la pratica "
                 "guidata.", 'attenzione')
    y = G5._testata(dr, y, sessione="OTP valido · 3 h 12 min")
    cols = ("Pos.", "Nato", "Sesso", "Tipologia di nascita", "Caso d’uso ANSC",
            "N. comunale previsto", "Stato SIPO")
    larg = (50, 260, 70, 230, 160, 190, 200)
    righe = [(g[0], g[1], g[2], g[3], g[4], g[5], "1 IN LAVORAZIONE") for g in C2]
    y = S.pannello(dr, y, "Gemelli della pratica – dati che saranno assegnati", 60 + 34 * 4)
    y = S.tabella(dr, y, cols, larg, righe, x=S.M + 12) + 6
    y = S.pulsantiera(dr, y + 8, [("INDIETRO", True)],
                      [("ANTEPRIMA GEMELLI", True), ("DATI PER ANSC", True)])
    S.ritaglia(im, y, dest)
    return dest


def c2_guidata(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Pratica guidata per la web app · gemello 2 "
                         "di 3", alt=1600)
    y = _barra_gemelli(dr, y, C2, (("testo copiato", 'fatto'), ("in lavorazione", 'corso'),
                                   ("da fare", 'attesa')))
    g = C2[1]
    # il numero comunale in grande, come per gli atti a testo libero
    x0, x1 = S.M, S.W - S.M
    dr.rectangle([x0, y, x1, y + 120], outline=S.ROSSO, width=3, fill='#fff8e6')
    dr.rectangle([x0, y, x0 + 380, y + 120], fill=S.ROSSO)
    dr.text((x0 + 20, y + 10), "GEMELLO 2 · NUMERO COMUNALE", font=S.f(S.N_BLD, 16),
            fill='white')
    fbig = S.f(S.N_BLD, 64)
    dr.text((x0 + 20, y + 32), g[5], font=fbig, fill='white')
    dr.text((x0 + 30 + S.lx(dr, g[5], fbig), y + 70), "/ 2026", font=S.f(S.N_BLD, 24),
            fill='white')
    fb, fr = S.f(S.N_BLD, 15), S.f(S.N_REG, 15)
    yy = y + 14
    for testo, ft in (("Sulla web app aprire la bozza del 2° gemello e riportarvi questo numero.",
                       fb),
                      ("Tipologia di nascita da indicare: 2 nato morto (ANSC_107). Certificato "
                       "medico obbligatorio.", fr),
                      ("Copiare il testo con COPIA TESTO e incollarlo nella composizione libera; "
                       "completare gli identificativi dei fratelli che la web app ha assegnato.",
                       fr)):
        for r in S.avvolgi(dr, testo, ft, x1 - x0 - 420):
            dr.text((x0 + 400, yy), r, font=ft, fill=S.INK)
            yy += 21
        yy += 6
    y += 120 + 18
    xs, ws = S.M, 760
    dr.text((xs, y), "Testo dell’atto – composto da SIPO", font=S.f(S.N_BLD, 15), fill=S.INK)
    _testo_atto(dr, xs, y + 24, ws, 260, g[5], "identificativi assegnati dalla web app",
                "ANTEPRIMA", "fonte: SIPO, formulario",
                "è nato morto un bambino di sesso femminile, gemello con altri due")
    xr = xs + ws + 20
    _riquadro_azioni(dr, xr, y + 24, S.W - S.M - xr, "Promemoria per la web app (gemello 2)", (
        (True, "Prenotazione dei 3 gemelli fatta sulla web app con i numeri 13640, 13641, 13642"),
        (True, "Bozza del gemello 2 aperta con il numero 13641"),
        (False, "Tipologia di nascita 2 nato morto indicata"),
        (False, "Testo incollato nella composizione libera"),
        (False, "Atto firmato sulla web app (dichiarante e ufficiale)")))
    y += 24 + 260 + 20
    y = S.avviso(dr, y, "Le caselle sono un promemoria dell’ufficiale: SIPO non vede la web app. "
                 "Quello che conta lo verifica RECUPERA GEMELLI al rientro.", 'info')
    y = S.pulsantiera(dr, y, [("GEMELLO PRECEDENTE", True), ("SOSPENDI", True)],
                      [("COPIA TESTO", True), ("GEMELLO SUCCESSIVO", True)])
    S.ritaglia(im, y, dest)
    return dest


# ------------------------------------------------------------------ la sequenza delle schermate
def sequenza(dest, titolo, sottotitolo, passi, frecce, ciclo, nota):
    """Miniature in serpentina: riga 1 da sinistra, riga 2 da destra.

    passi: [(titolo, png)]; frecce: etichette fra passo i e i+1; ciclo: (da, a, etichetta) o None.
    """
    import diagrammi_comune as G
    tw, gap, n_col = 520, 170, 3
    larg = 60 + n_col * tw + (n_col - 1) * gap + 60
    mini = []
    for _, p in passi:
        m = Image.open(p).convert('RGB')
        hh = int(m.height * tw / m.width)
        mini.append(m.resize((tw, min(hh, 520)), Image.LANCZOS) if hh <= 520 else
                    m.resize((tw, hh), Image.LANCZOS).crop((0, 0, tw, 520)))
    righe = [mini[i:i + n_col] for i in range(0, len(mini), n_col)]
    alt_righe = [max(m.height for m in r) for r in righe]
    alt = 150 + sum(alt_righe) + 150 * (len(righe) - 1) + 80
    im, dr = G.tela(larg, alt, titolo, sottotitolo)
    ft = G.fnt(G.F_BLD, 18)
    box = []
    y = 150
    for ri, r in enumerate(righe):
        for ci, m in enumerate(r):
            col = ci if ri % 2 == 0 else n_col - 1 - ci
            x = 60 + col * (tw + gap)
            k = ri * n_col + ci
            dr.text((x, y - 32), "%d · %s" % (k + 1, passi[k][0]), font=ft, fill=G.INK)
            im.paste(m, (x, y))
            dr.rectangle([x - 1, y - 1, x + m.width, y + m.height], outline='#9a9a9a', width=2)
            box.append((x, y, m.width, m.height))
        y += alt_righe[ri] + 150

    def et(testo, x, y, colore=VERDE, ts=15, centro=False):
        fe = G.fnt(G.F_REG, ts)
        rr = testo.split("\n")
        lw = max(G.larghezza(dr, r, fe) for r in rr)
        if centro:
            x -= lw / 2
        dr.rectangle([x - 3, y - 2, x + lw + 3, y + len(rr) * (ts + 4)], fill='white')
        for i, r in enumerate(rr):
            dr.text((x, y + i * (ts + 4)), r, font=fe, fill=colore)

    for i, testo in enumerate(frecce):
        a, b = box[i], box[i + 1]
        if abs(a[1] - b[1]) < 5:                      # stessa riga
            yy = a[1] + 110
            if b[0] > a[0]:
                G.freccia(dr, (a[0] + a[2], yy), (b[0], yy), VERDE)
                et(testo, a[0] + a[2] + 10, yy + 12)
            else:
                G.freccia(dr, (a[0], yy), (b[0] + b[2], yy), VERDE)
                et(testo, b[0] + b[2] + 10, yy + 12)
        else:                                         # a capo, in verticale
            xx = a[0] + a[2] * 0.7
            G.freccia(dr, (xx, a[1] + a[3]), (xx, b[1] - 36), VERDE)
            et(testo, xx + 14, a[1] + a[3] + 30)
    if ciclo:
        da, a_, testo = ciclo
        A, B = box[da], box[a_]
        xx = A[0] + A[2] * 0.25
        G.percorso(dr, [(xx, A[1] - 36), (xx, B[1] + B[3] + 4)], G.MUTED, True)
        fe = G.fnt(G.F_REG, 15)
        rr = testo.split("\n")
        ym = (B[1] + B[3] + A[1] - 36) / 2 - len(rr) * 10
        for i, r in enumerate(rr):
            dr.text((xx - 14 - G.larghezza(dr, r, fe), ym + i * 19), r, font=fe, fill=G.MUTED)
    dr.text((60, alt - 50), nota, font=G.fnt(G.F_ITA, 15), fill=G.MUTED)
    im.save(dest)
    return dest


def png(nome):
    return os.path.join(DIR, nome)


def seq_caso1(dest):
    return sequenza(
        dest, "Caso 1 – gemelli con lo stesso UC: la sequenza delle schermate",
        "tutto da SIPO; sulle frecce il comando e i servizi; il ciclo si ripete per ciascun gemello",
        [("Riepilogo gemelli", png('gem5_riepilogo.png')),
         ("Raccordo dei numeri comunali", png('gem8_c1_raccordo.png')),
         ("Gemello k: documenti, validazione, firme", png('gem8_c1_gemello.png')),
         ("Gemello k: testo da ANSC e definizione", png('gem8_c1_testo.png')),
         ("Esito del parto", png('gem8_c1_esito.png'))],
        ["DEFINISCI\nPOST /richiesta (N numeri)\nR009 /prenota/evento",
         "PROSEGUI\ngemello 1",
         "FIRMA USC (R007)\nR010 testo · /finalizzaAtto",
         "dopo l’ultimo gemello"],
        (3, 2, "GEMELLO\nSUCCESSIVO\n(k+1)"),
        "Al passo 3 le pagine sono quelle del percorso ordinario di un atto (documenti, anteprima e "
        "validazione, firma del dichiarante, conformità, firma dell’USC), con la fila dei gemelli "
        "in testa.")


def seq_caso2(dest):
    return sequenza(
        dest, "Caso 2 – gemelli con UC diversi: la sequenza delle schermate",
        "la web app forma gli atti; SIPO stacca i numeri, guida la copia dei testi e recupera gli "
        "atti",
        [("Riepilogo gemelli", png('gem8_c2_riepilogo.png')),
         ("Raccordo dei numeri – da riportare", png('gem8_c2_raccordo.png')),
         ("Pratica guidata: gemello k", png('gem8_c2_guidata.png')),
         ("Web app ANSC (fuori da SIPO)", png('gem_webapp_prenotazione.png')),
         ("Raccordo dei numeri – esito del recupero", png('gem8_c2_recupero.png')),
         ("Esito del parto", png('gem8_c2_esito.png'))],
        ["DATI PER ANSC\nPOST /richiesta\n(N numeri)",
         "AVVIA LA PRATICA\nGUIDATA",
         "COPIA TESTO\n→ web app",
         "rientro in SIPO\nRECUPERA GEMELLI\nR005 per numero",
         "DEFINISCI GEMELLI\n/finalizzaAtto"],
        (3, 2, "GEMELLO\nSUCCESSIVO\n(k+1)"),
        "Sulla web app l’ufficiale prenota i gemelli con i numeri di SIPO, compila ciascuna bozza "
        "con la tipologia di nascita e il testo copiato, e raccoglie le firme.")


def main():
    for fn, nome in ((c1_raccordo, 'gem8_c1_raccordo.png'), (c1_gemello, 'gem8_c1_gemello.png'),
                     (c1_testo, 'gem8_c1_testo.png'), (c1_esito, 'gem8_c1_esito.png'),
                     (c2_riepilogo, 'gem8_c2_riepilogo.png'),
                     (c2_raccordo, 'gem8_c2_raccordo.png'), (c2_guidata, 'gem8_c2_guidata.png'),
                     (c2_recupero, 'gem8_c2_recupero.png'), (c2_esito, 'gem8_c2_esito.png'),
                     (seq_caso1, 'gem8_seq_caso1.png'), (seq_caso2, 'gem8_seq_caso2.png')):
        print(fn(png(nome)))


if __name__ == '__main__':
    main()
