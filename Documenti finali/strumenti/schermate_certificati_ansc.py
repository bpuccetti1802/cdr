# -*- coding: utf-8 -*-
"""Figure del capitolo «Certificati ANSC: la ricerca dell'atto» (analisi certificazioni v0.7).

Due famiglie:
  · ritagli del filmato «Sorgenti Documentali/Ricerca atto per Certificazione.mov» (web app ANSC
    di preproduzione): si toglie la cornice del browser e si copre il nome dell'operatore;
  · ipotesi di schermata della funzione nuova di SIPO, nello stile di schermate_sipo_wf.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_certificati_ansc.py
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S  # noqa: E402
from schermate_sipo_wf import (f, lx, N_REG, N_BLD, SERIF, ROSSO, GIALLO, INK, MUTED, BORDO,  # noqa
                               AVVISI, M, W, campo, radio, bottone, avviso, pannello, spunta)

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOV = os.path.join(BASE, 'Sorgenti Documentali', 'Ricerca atto per Certificazione.mov')
OUT = os.path.join(S.IMG, 'certificazioni')


# ------------------------------------------------------------------------- web app ANSC
def _fotogramma(secondi):
    tmp = tempfile.mkdtemp()
    dest = os.path.join(tmp, 'f.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(secondi), '-i', MOV, '-frames:v', '1',
                    dest], check=True)
    return Image.open(dest).convert('RGB')


def _copri_nome(im, y_nome):
    """Copre «Ciao, <nome dell'operatore>» con il colore della testata."""
    dr = ImageDraw.Draw(im)
    fondo = im.getpixel((1000, y_nome - 40))
    dr.rectangle([1095, y_nome - 18, 1360, y_nome + 18], fill=fondo)
    dr.text((1107, y_nome - 11), "Ciao, NOME COGNOME", font=f(N_BLD, 19), fill='white')


def webapp(secondi, y_nome, alto, basso, dest, scala=1.0, senza_riquadri=False):
    im = _fotogramma(secondi)
    # il filmato è in risoluzione doppia rispetto ai fotogrammi d'esempio: si riporta a 1494
    if im.width != 1494:
        im = im.resize((1494, round(im.height * 1494 / im.width)), Image.LANCZOS)
    _copri_nome(im, y_nome)
    if senza_riquadri:
        # i collegamenti della home («Recupero evento in bozza», «Rilascio certificato») non
        # riguardano la ricerca: si coprono con il fondo della pagina
        dr = ImageDraw.Draw(im)
        dr.rectangle([560, 620, 920, 800], fill=im.getpixel((1000, 700)))
    im = im.crop((24, alto, 1470, basso))
    if scala != 1.0:
        im = im.resize((round(im.width * scala), round(im.height * scala)), Image.LANCZOS)
    im.save(dest)
    return dest


def figure_webapp():
    os.makedirs(OUT, exist_ok=True)
    return [
        webapp(1.0, 214, 136, 790, os.path.join(OUT, 'webapp_ricerca_soggetto.png'),
               senza_riquadri=True),
        webapp(10.0, 214, 136, 790, os.path.join(OUT, 'webapp_ricerca_evento.png'),
               senza_riquadri=True),
        webapp(28.0, 268, 136, 1058, os.path.join(OUT, 'webapp_risultati_azioni.png')),
        webapp(34.0, 268, 136, 1058, os.path.join(OUT, 'webapp_rilascio_testata.png')),
    ]


# ------------------------------------------------------------------------------- SIPO
VOCI = ("Home", "Generali", "Municipi", "Dipartimento", "Stato Civile", "Elettorale", "Coec",
        "Mipper", "Statistica", "Utilità")
MENU_VERO = os.path.join(BASE, 'Sorgenti Documentali', 'Immagini sipo', 'menu principale',
                         'Screenshot 2026-11-10 alle 17.22.52.png')


def _barra(dr, attiva=None):
    """Testata e menu principale di SIPO con la voce nuova; restituisce la x della voce attiva."""
    dr.rectangle([0, 0, W, 92], fill='#9a1030')
    dr.text((70, 24), "ROMA", font=f(SERIF, 42), fill='white')
    S._stemma(dr, 236, 20)
    dr.rectangle([0, 93, W, 132], fill=S.ROSSO)
    x, fm, xa = 20, f(N_BLD, 15), None
    for voce in VOCI:
        if voce == attiva:
            dr.rectangle([x - 10, 93, x + lx(dr, voce, fm) + 30, 132], fill='#5e001b')
            xa = x - 10
        dr.text((x, 104), voce, font=fm, fill='white')
        x += lx(dr, voce, fm) + 8
        if voce != "Home":
            dr.line([(x, 110), (x + 5, 116), (x + 10, 110)], fill='white', width=2)
            x += 14
        x += 22
    dr.text((W - 175, 104), "Nome Cognome", font=fm, fill=GIALLO)
    dr.text((W - 52, 104), "ESCI", font=fm, fill=GIALLO)
    return xa


def _titolo(dr, titolo, y=152):
    dr.text((M, y), titolo, font=f(N_BLD, 17), fill=INK)
    tag = "IPOTESI DI SCHERMATA"
    ft = f(N_BLD, 13)
    tw = lx(dr, tag, ft) + 20
    dr.rectangle([W - M - tw, y - 2, W - M, y + 22], outline=ROSSO, width=2)
    dr.text((W - M - tw + 10, y + 2), tag, font=ft, fill=ROSSO)
    dr.line([(M, y + 32), (W - M, y + 32)], fill='#bdbdbd', width=1)
    return y + 50


def _sessione(dr, y, testo="OTP ANSC valido · 3 h 12 min", stato='ok'):
    """Lo stato del codice di sessione ANSC, sotto il titolo, con il pulsante per rinnovarlo."""
    bordo, fondo = AVVISI[stato]
    fs = f(N_BLD, 14)
    sw = lx(dr, testo, fs) + 28
    x0 = W - M - sw - 150
    dr.rounded_rectangle([x0, y, x0 + sw, y + 28], radius=12, fill=fondo, outline=bordo)
    dr.text((x0 + 14, y + 5), testo, font=fs, fill='#2e6b43' if stato == 'ok' else INK)
    bottone(dr, W - M - 138, y - 1, "RINNOVA OTP")
    return y + 44


def menu(dest):
    """Lo screenshot vero del menu Municipi, con la terza voce nell'area «Certificati»."""
    im = Image.open(MENU_VERO).convert('RGB')
    dr = ImageDraw.Draw(im)
    dr.rectangle([955, 190, 1060, 222], fill='white')            # cursore e suggerimento
    dr.rectangle([1305, 145, 1380, 166], fill=im.getpixel((1300, 140)))   # nome dell'utente
    dr.text((1310, 148), "Nome Cognome", font=f(N_BLD, 12), fill='#f5a623')
    x, y = 871, 270
    dr.text((x, y), "Certificati ANSC", font=f(N_REG, 12), fill='#7a1530')
    w = lx(dr, "Certificati ANSC", f(N_REG, 12))
    dr.rounded_rectangle([x - 6, y - 4, x + w + 6, y + 18], radius=4, outline=ROSSO, width=2)
    dr.text((x + w + 16, y + 1), "voce nuova", font=f(S.N_ITA, 13), fill=ROSSO)
    im = im.crop((0, 62, im.width, 440))
    dr = ImageDraw.Draw(im)
    tag = "IPOTESI"
    ft = f(N_BLD, 13)
    tw = lx(dr, tag, ft) + 20
    dr.rectangle([im.width - 30 - tw, im.height - 34, im.width - 30, im.height - 10],
                 outline=ROSSO, width=2)
    dr.text((im.width - 20 - tw, im.height - 30), tag, font=ft, fill=ROSSO)
    im.save(dest)
    return dest


def ricerca(dest):
    im = Image.new('RGB', (W, 1000), 'white')
    dr = ImageDraw.Draw(im)
    _barra(dr)
    y = _titolo(dr, "Certificati ANSC – Ricerca atto")
    y = _sessione(dr, y)
    y = avviso(dr, y, "La ricerca è nazionale: si trovano gli atti formati da qualunque comune, "
               "purché firmati e non secretati. Le bozze e gli atti secretati di altri comuni "
               "non sono visibili.")
    # scelta della modalità
    x = radio(dr, M, y, "Ricerca per evento", scelto=True)
    radio(dr, x + 20, y, "Ricerca per soggetto")
    y += 36
    # pannello per evento
    yp = y
    y = pannello(dr, y, "Ricerca per evento – basta un criterio", 250)
    larg = W - 2 * M - 24
    cols = [(0.20, "Registro", "Nascita", 'select'), (0.17, "Data dal", "01/01/2026", 'data'),
            (0.17, "Data al", "20/01/2026", 'data'),
            (0.46, "Identificativo nazionale dell’atto", "", 'testo')]
    xx = M + 12
    for q, et, val, tipo in cols:
        w = int(larg * q) - 12
        campo(dr, xx, y, w, et, val, tipo)
        xx += w + 12
    y += 66
    dr.text((M + 12, y), "Ricerca avanzata", font=f(N_BLD, 14), fill=ROSSO)
    y += 24
    cols = [(0.20, "Tipo di contenuto", "Atto", 'select'),
            (0.30, "Comune di registrazione", "ROMA", 'select'),
            (0.17, "Numero dell’atto", "", 'testo')]
    xx = M + 12
    for q, et, val, tipo in cols:
        w = int(larg * q) - 12
        campo(dr, xx, y, w, et, val, tipo)
        xx += w + 12
    S.bottoni_dx(dr, yp + 205, [("PULISCI", True), ("CERCA", True)], W - M - 12)
    y = yp + 268
    # pannello per soggetto, spento finché non si sceglie
    yp = y
    y = pannello(dr, y, "Ricerca per soggetto – codice fiscale, oppure cognome, nome e data "
                 "di nascita", 196)
    cols = [(0.26, "Codice fiscale", "", 'testo'), (0.24, "Cognome", "", 'testo'),
            (0.24, "Nome", "", 'testo'), (0.26, "Data di nascita", "", 'data')]
    xx = M + 12
    for q, et, val, tipo in cols:
        w = int(larg * q) - 12
        campo(dr, xx, y, w, et, val, tipo)
        xx += w + 12
    y += 66
    dr.text((M + 12, y), "Ricerca avanzata: sesso · comune o stato di nascita · identificativo "
            "ANPR · identificativo ANSC del soggetto", font=f(N_REG, 14), fill=MUTED)
    bottone(dr, M + 12, y + 30, "CERCA IN ANAGRAFE")
    dr.text((M + 170, y + 36), "precompila con i dati e l’identificativo ANPR di una persona "
            "dell’anagrafe di Roma", font=f(S.N_ITA, 14), fill=MUTED)
    # velo sul pannello non scelto
    velo = Image.new('RGBA', (W - 2 * M + 1, 197), (255, 255, 255, 140))
    im.paste(velo, (M, yp), velo)
    im.crop((0, 0, W, yp + 220)).save(dest)
    return dest


RIGHE = [
    ("ROSSI BEATRICE", "Nascita", "Dichiarazione entro i 10 giorni – resa dalla madre",
     "20/01/2026", "CEDRASCO (SO)", "FIRMATO DA USC", True),
    ("SPANK CANDY", "Nascita", "Dichiarazione tardiva di filiazione fuori del matrimonio…",
     "20/01/2026", "VENEZIA (VE)", "FIRMATO DA USC", True),
    ("VERDI CLAUDIA", "Nascita", "Dichiarazione nei termini di filiazione fuori dal matrimonio…",
     "20/01/2026", "SEREGNO (MB)", "FIRMATO DA USC", True),
    ("ROSSI PAOLO", "Nascita", "Dichiarazione entro i 10 giorni – resa dal padre con…",
     "20/01/2026", "CAMAIORE (LU)", "ANNULLATO", False),
    ("BIANCHI LUCA", "Nascita", "Dichiarazione entro i 10 giorni – resa dal padre",
     "19/01/2026", "ROMA (RM)", "FIRMATO DA USC", True),
]


def risultati(dest):
    im = Image.new('RGB', (W, 1000), 'white')
    dr = ImageDraw.Draw(im)
    _barra(dr)
    y = _titolo(dr, "Certificati ANSC – Risultati della ricerca")
    y = _sessione(dr, y)
    # criteri in forma ridotta
    fb, fr = f(N_BLD, 14), f(N_REG, 14)
    testo = "Per evento · Registro: Nascita · dal 01/01/2026 al 20/01/2026"
    tw = lx(dr, testo, fb) + 30
    dr.rounded_rectangle([M, y, M + tw, y + 30], radius=14, outline=S.CAMPO, fill='#f7f7f7')
    dr.text((M + 15, y + 6), testo, font=fb, fill=INK)
    bottone(dr, M + tw + 14, y, "MODIFICA RICERCA")
    y += 48
    # raffinamento sull'elenco già ricevuto
    larg = W - 2 * M
    cols = [(0.18, "Stato", "Seleziona", 'select'), (0.18, "Provincia", "Seleziona", 'select'),
            (0.24, "Comune di registrazione", "Seleziona", 'select'),
            (0.20, "Intestatario contiene", "", 'testo')]
    xx = M
    for q, et, val, tipo in cols:
        w = int(larg * q) - 12
        campo(dr, xx, y, w, et, val, tipo)
        xx += w + 12
    bottone(dr, xx + 4, y + 18, "FILTRA")
    dr.text((xx + 90, y + 24), "Azzera filtri", font=f(N_REG, 14), fill=ROSSO)
    y += 64
    dr.text((M, y), "38 atti trovati · pagina 1 di 2 (20 per pagina) · i filtri agiscono "
            "sull’elenco già ricevuto", font=f(S.N_ITA, 14), fill=MUTED)
    y += 28
    intest = ["Intestatario", "Registro", "Tipo di atto (caso d’uso)", "Data form.",
              "Comune", "Stato ANSC", "Azioni"]
    larg_c = [170, 90, 440, 100, 160, 150, 222]

    def stato(testo, ok):
        def disegna(d, x, yy):
            d.text((x, yy), testo, font=fb, fill='#2e7d32' if ok else '#b71c1c')
        return disegna

    def azioni(ok):
        def disegna(d, x, yy):
            x2 = bottone(d, x, yy - 4, "VISUALIZZA")
            bottone(d, x2 + 8, yy - 4, "RILASCIA", attivo=ok)
        return disegna

    righe = [(r[0], r[1], r[2], r[3], r[4], stato(r[5], r[6]), azioni(r[6])) for r in RIGHE]
    y = S.tabella(dr, y, intest, larg_c, righe, alt=42)
    y = avviso(dr, y, "ROSSI PAOLO – atto annullato: non si rilasciano certificazioni. "
               "Il pulsante RILASCIA resta spento e il motivo si legge passando sul pulsante.",
               'attenzione')
    # paginazione
    dr.text((W - M - 250, y), "‹ precedente   1   2   successiva ›", font=fr, fill=ROSSO)
    im.crop((0, 0, W, y + 40)).save(dest)
    return dest


def apertura_rilascio(dest):
    im = Image.new('RGB', (W, 700), 'white')
    dr = ImageDraw.Draw(im)
    _barra(dr)
    y = _titolo(dr, "Certificati ANSC – Rilascio certificazione")
    y = _sessione(dr, y)
    y = pannello(dr, y, "Atto da certificare (letto da ANSC per identificativo nazionale "
                 "alle 10:42)", 168)
    larg = W - 2 * M - 24
    cols = [(0.12, "Registro", "Nascita"),
            (0.40, "Tipo di atto (caso d’uso)", "11111000 Dichiarazione entro i 10 giorni"),
            (0.18, "Intestatario", "BIANCHI LUCA"),
            (0.30, "Identificativo nazionale", "2026-10232371-13617-058091")]
    xx = M + 12
    for q, et, val in cols:
        w = int(larg * q) - 12
        campo(dr, xx, y, w, et, val, 'lettura')
        xx += w + 12
    y += 56
    cols = [(0.12, "Data formazione", "19/01/2026"), (0.20, "Comune", "ROMA (RM)"),
            (0.12, "Numero atto", "13617"), (0.18, "Stato ANSC", "FIRMATO DA USC")]
    xx = M + 12
    for q, et, val in cols:
        w = int(larg * q) - 12
        campo(dr, xx, y, w, et, val, 'lettura')
        xx += w + 12
    y += 82
    y = avviso(dr, y, "Da qui comincia il rilascio vero e proprio: tipo di certificato, "
               "richiedente, uso e firma.", 'info')
    im.crop((0, 0, W, y + 10)).save(dest)
    return dest


def figure_sipo():
    os.makedirs(OUT, exist_ok=True)
    return [menu(os.path.join(OUT, 'cansc_menu.png')),
            ricerca(os.path.join(OUT, 'cansc_ricerca.png')),
            risultati(os.path.join(OUT, 'cansc_risultati.png')),
            apertura_rilascio(os.path.join(OUT, 'cansc_apertura_rilascio.png'))]


if __name__ == '__main__':
    for p in figure_webapp() + figure_sipo():
        print(p)
