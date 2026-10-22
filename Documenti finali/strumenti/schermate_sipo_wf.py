# -*- coding: utf-8 -*-
"""Ipotesi di schermata, nello stile di SIPO, delle pagine nuove del workflow SIPO-ANSC.

Documento: WORKFLOW_Interfacce-SIPO-ANSC (dalla v0.2, 21/10/2026). Le pagine sono quattro —
Validazione, Firme dei dichiaranti, Conformità, Firma dell'USC — più la finestra con cui si
riaprono i dati dopo le firme dei dichiaranti.

Lo stile è ricavato da due fonti, non inventato:
  · le schermate di SIPO in «Sorgenti Documentali/Immagini sipo/» (testata rossa con la scritta
    ROMA, menu orizzontale con le voci in bianco e l'utente in giallo, titolo di pagina con
    filetto, pannelli con barra grigia, etichette in grassetto sopra i campi, pulsanti
    rettangolari bordeaux in maiuscolo, linguette rosse/grigie);
  · il CSS di statocivile-web (static/css/style.css e buttonStyle.css): colore principale
    #8c0029, giallo #FFB300 per l'utente, font Titillium/UrbsDisplay — qui reso con Arial
    Narrow, che sulla macchina c'è e ne ha la larghezza.
Il contenuto delle pagine viene dai contratti ANSC (R006, R007, R009, R010, R012, R014), dalle
schermate di Side del capitolo 13.1 dell'analisi e dal documento di Milano sull'attestato di
conformità. I valori mostrati sono di esempio.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_sipo_wf.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
FD = '/System/Library/Fonts/Supplemental'
N_REG = os.path.join(FD, 'Arial Narrow.ttf')
N_BLD = os.path.join(FD, 'Arial Narrow Bold.ttf')
N_ITA = os.path.join(FD, 'Arial Narrow Italic.ttf')
SERIF = os.path.join(FD, 'Times New Roman.ttf')

ROSSO = '#8c0029'
ROSSO_SPENTO = '#d9aab6'
GIALLO = '#FFB300'
GRIGIO_TAB = '#6c757d'
GRIGIO_TAB_CHIARO = '#c4c8cc'
INK = '#222222'
MUTED = '#666666'
BORDO = '#d6d6d6'
CAMPO = '#8f8f8f'
SOLA_LETTURA = '#ebebe4'
BLU_ICONA = '#1e88e5'
AVVISI = {'info': ('#9cc3ea', '#e8f1fb'), 'attenzione': ('#e5c06b', '#fff4d6'),
          'errore': ('#e4a1ab', '#fbe3e6'), 'ok': ('#9fd0ad', '#e3f3e8')}

W = 1400
M = 34                       # margine laterale


def f(path, size):
    return ImageFont.truetype(path, size)


def lx(dr, t, font):
    return dr.textbbox((0, 0), t, font=font)[2]


def avvolgi(dr, t, font, larg):
    righe, cur = [], ''
    for p in t.split():
        prova = (cur + ' ' + p).strip()
        if lx(dr, prova, font) <= larg or not cur:
            cur = prova
        else:
            righe.append(cur)
            cur = p
    if cur:
        righe.append(cur)
    return righe


# --------------------------------------------------------------------------------- cornice
def _stemma(dr, x, y):
    oro = '#d8b46a'
    dr.polygon([(x, y + 8), (x + 26, y + 8), (x + 26, y + 30), (x + 13, y + 42), (x, y + 30)],
               outline=oro, width=2)
    for i in range(4):
        dr.rectangle([x + 2 + i * 6, y, x + 6 + i * 6, y + 6], outline=oro)


def pagina(titolo, alt=1900):
    im = Image.new('RGB', (W, alt), 'white')
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 92], fill='#9a1030')
    dr.text((70, 24), "ROMA", font=f(SERIF, 42), fill='white')
    _stemma(dr, 236, 20)
    dr.line([(0, 92), (W, 92)], fill='#e9c9d0', width=1)
    dr.rectangle([0, 93, W, 132], fill=ROSSO)
    x = 20
    fm = f(N_BLD, 15)
    for voce in ("Home", "Generali", "Municipi", "Dipartimento", "Stato Civile", "Elettorale",
                 "Coec", "Mipper", "Statistica", "Utilità"):
        dr.text((x, 104), voce, font=fm, fill='white')
        x += lx(dr, voce, fm) + 8
        if voce != "Home":
            dr.line([(x, 110), (x + 5, 116), (x + 10, 110)], fill='white', width=2)
            x += 14
        x += 26
    dr.text((W - 210, 104), "Nome Cognome", font=fm, fill=GIALLO)
    dr.text((W - 70, 104), "ESCI", font=fm, fill=GIALLO)
    # titolo di pagina, con il contrassegno di ipotesi
    dr.text((M, 152), titolo, font=f(N_BLD, 17), fill=INK)
    tag = "IPOTESI DI SCHERMATA"
    ft = f(N_BLD, 13)
    tw = lx(dr, tag, ft) + 20
    dr.rectangle([W - M - tw, 150, W - M, 174], outline=ROSSO, width=2)
    dr.text((W - M - tw + 10, 154), tag, font=ft, fill=ROSSO)
    dr.line([(M, 184), (W - M, 184)], fill='#bdbdbd', width=1)
    return im, dr, 202


def ritaglia(im, y, dest):
    im.crop((0, 0, W, y + 26)).save(dest)
    return dest


# ------------------------------------------------------------------------------- elementi
def spunta(dr, x, y, colore='white', larg=2):
    dr.line([(x, y + 5), (x + 4, y + 9), (x + 11, y)], fill=colore, width=larg)


def linguette(dr, y, voci, attiva, fatte=()):
    """Le quattro pagine nuove come linguette di SIPO: rossa l'attiva, grigie le fatte."""
    x = M
    fl = f(N_BLD, 14)
    for i, v in enumerate(voci):
        w = lx(dr, v, fl) + (52 if i in fatte else 32)
        col = ROSSO if i == attiva else GRIGIO_TAB if i in fatte else GRIGIO_TAB_CHIARO
        dr.rectangle([x, y, x + w, y + 32], fill=col)
        tx = x + 16
        if i in fatte:
            spunta(dr, tx, y + 11)
            tx += 20
        dr.text((tx, y + 7), v, font=fl, fill='white')
        x += w + 4
    dr.line([(M, y + 32), (W - M, y + 32)], fill=BORDO, width=1)
    return y + 50


def pannello(dr, y, titolo, alt, x=M, larg=None):
    larg = larg or W - 2 * M
    dr.rectangle([x, y, x + larg, y + alt], outline=BORDO, width=1, fill='white')
    dr.rectangle([x, y, x + larg, y + 36], fill='#f5f5f5', outline=BORDO)
    dr.text((x + 12, y + 9), titolo, font=f(N_BLD, 14), fill='#333333')
    cx, cy = x + larg - 22, y + 18
    dr.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=BLU_ICONA)
    dr.line([(cx - 4, cy - 1), (cx, cy + 3), (cx + 4, cy - 1)], fill='white', width=2)
    return y + 50


def campo(dr, x, y, w, etichetta, valore='', tipo='testo'):
    dr.text((x, y), etichetta, font=f(N_BLD, 14), fill=INK)
    by = y + 21
    fondo = SOLA_LETTURA if tipo == 'lettura' else 'white'
    dr.rectangle([x, by, x + w, by + 25], outline=CAMPO, width=1, fill=fondo)
    fv = f(N_REG, 14)
    if tipo == 'password' and valore:
        for i in range(len(valore)):
            dr.ellipse([x + 8 + i * 11, by + 9, x + 15 + i * 11, by + 16], fill=INK)
    elif valore and tipo != 'file':
        dr.text((x + 6, by + 4), valore, font=fv, fill=INK)
    if tipo == 'select':
        dr.line([(x + w - 16, by + 10), (x + w - 11, by + 15), (x + w - 6, by + 10)],
                fill=INK, width=2)
    if tipo == 'data':
        dr.rectangle([x + w - 20, by + 6, x + w - 7, by + 19], outline=INK)
        dr.line([(x + w - 20, by + 10), (x + w - 7, by + 10)], fill=INK)
    if tipo == 'file':
        dr.rectangle([x + 3, by + 3, x + 100, by + 22], fill='#efefef', outline='#aaaaaa')
        dr.text((x + 10, by + 5), "Scegli file", font=f(N_REG, 13), fill=INK)
        dr.text((x + 110, by + 4), valore or "Nessun file selezionato", font=fv, fill=INK)
    return by + 25


def casella(dr, x, y, testo, segnata=False, attiva=True, ft=None):
    col = INK if attiva else '#9a9a9a'
    dr.rectangle([x, y + 2, x + 14, y + 16], outline=col, width=1,
                 fill='white' if attiva else '#f0f0f0')
    if segnata:
        spunta(dr, x + 2, y + 5, col, 2)
    dr.text((x + 22, y), testo, font=ft or f(N_REG, 14), fill=col)


def radio(dr, x, y, testo, scelto=False):
    dr.ellipse([x, y + 2, x + 14, y + 16], outline=INK, width=1, fill='white')
    if scelto:
        dr.ellipse([x + 4, y + 6, x + 10, y + 12], fill=INK)
    dr.text((x + 20, y), testo, font=f(N_REG, 14), fill=INK)
    return x + 20 + lx(dr, testo, f(N_REG, 14)) + 16


def bottone(dr, x, y, testo, attivo=True):
    fb = f(N_BLD, 13)
    w = lx(dr, testo, fb) + 28
    dr.rectangle([x, y, x + w, y + 30], fill=ROSSO if attivo else ROSSO_SPENTO)
    dr.text((x + 14, y + 7), testo, font=fb, fill='white' if attivo else '#f8eef1')
    return x + w


def bottoni_dx(dr, y, voci, x_fine=W - M):
    fb = f(N_BLD, 13)
    x = x_fine - sum(lx(dr, t, fb) + 28 for t, _ in voci) - 8 * (len(voci) - 1)
    for t, attivo in voci:
        x = bottone(dr, x, y, t, attivo) + 8


def avviso(dr, y, testo, tipo='info', x=M, larg=None):
    larg = larg or W - 2 * M
    bordo, fondo = AVVISI[tipo]
    fa = f(N_REG, 14)
    righe = avvolgi(dr, testo, fa, larg - 24)
    h = 14 + 19 * len(righe)
    dr.rectangle([x, y, x + larg, y + h], fill=fondo, outline=bordo)
    for i, r in enumerate(righe):
        dr.text((x + 12, y + 7 + i * 19), r, font=fa, fill=INK)
    return y + h + 14


def tabella(dr, y, intestazioni, larghezze, righe, x=M, alt=34):
    fi, fr = f(N_BLD, 14), f(N_REG, 14)
    tot = sum(larghezze)
    dr.rectangle([x, y, x + tot, y + alt], fill='#f2f2f2', outline=BORDO)
    cx = x
    for t, w in zip(intestazioni, larghezze):
        dr.text((cx + 8, y + 8), t, font=fi, fill=INK)
        cx += w
    y += alt
    for r in righe:
        dr.rectangle([x, y, x + tot, y + alt], fill='white', outline=BORDO)
        cx = x
        for v, w in zip(r, larghezze):
            if callable(v):
                v(dr, cx + 8, y + 8)
            else:
                dr.text((cx + 8, y + 8), v, font=fr, fill=INK)
            cx += w
        y += alt
    return y + 14


# ------------------------------------------------------------------------ parti comuni
PAGINE = ("Validazione", "Firme dei dichiaranti", "Conformità", "Firma dell’USC")
UC = "11111000 – Dichiarazione entro i 10 giorni – resa dal padre"
ID_ANSC = "2026-10527619-13617-058091"


def testata_atto(dr, y, stato_ansc, id_ansc, stato_sipo="1 IN LAVORAZIONE", minuti="3 h 12 min"):
    """Il pannello che apre tutte le pagine nuove: chi è l'atto e a che punto è."""
    y0 = y
    y = pannello(dr, y, "Atto di nascita – stato dell’integrazione con ANSC", 150)
    larg = W - 2 * M - 24
    cols = [(0.34, "Caso d’uso ANSC (UC)", UC), (0.12, "Numero comunale", "13617"),
            (0.20, "Identificativo nazionale", id_ansc), (0.17, "Stato ANSC", stato_ansc),
            (0.17, "Stato SIPO", stato_sipo)]
    x = M + 12
    for quota, et, val in cols:
        w = int(larg * quota) - 12
        campo(dr, x, y, w, et, val, 'lettura')
        x += w + 12
    y += 58
    dr.text((M + 12, y), "Ufficiale dello stato civile:", font=f(N_BLD, 14), fill=INK)
    dr.text((M + 190, y), "NOME COGNOME", font=f(N_REG, 14), fill=INK)
    sess = "Sessione ANSC: OTP valido, tempo residuo " + minuti
    fs = f(N_BLD, 14)
    sw = lx(dr, sess, fs) + 24
    bordo, fondo = AVVISI['ok']
    dr.rounded_rectangle([W - M - 12 - sw, y - 4, W - M - 12, y + 20], radius=10, fill=fondo,
                         outline=bordo)
    dr.text((W - M - sw, y - 1), sess, font=fs, fill='#2e6b43')
    return y0 + 150 + 16


def pulsantiera(dr, y, sinistra, destra):
    dr.line([(M, y), (W - M, y)], fill='#bdbdbd')
    y += 16
    x = M
    for t, attivo in sinistra:
        x = bottone(dr, x, y, t, attivo) + 8
    bottoni_dx(dr, y, destra)
    return y + 30


# Dalla v0.3 del documento le pagine nuove sono SCHERMATE SEPARATE (indicazione dell'utente,
# 21/10/2026: con le linguette «si perde la transizione»). Al posto delle linguette ogni
# schermata si apre con l'esito del passaggio che l'ha aperta: è lì che la transizione si vede.
ARRIVI = (
    ("Da Anteprima:", "anteprima confermata con VALIDA. Numero comunale 13617 staccato "
     "(num-ansc-sipo); modello evento costruito e salvato (revisione 7)."),
    ("Da Validazione:", "validazione riuscita (R009). ANSC ha assegnato l’identificativo "
     "nazionale " + "2026-10527619-13617-058091" + "; stato ANSC 2 CONFERMATO."),
    ("Da Firme dei dichiaranti:", "firme acquisite. ANSC ha portato l’atto a 4 FIRMATO DAL "
     "DICHIARANTE: i dati sono vincolati."),
    ("Da Conformità:", "attestazione di conformità firmata (R007). Stato ANSC 11 FIRMATO PER "
     "CONFORMITÀ."),
    ("Da Firma dell’USC:", "atto firmato dall’ufficiale e chiuso. Stato ANSC 5 FIRMATO DA USC, "
     "pratica SIPO 2 DEFINITO."),
)


def arrivo(dr, y, indice):
    """Il banner verde di arrivo: dice da dove si viene e che cosa è cambiato."""
    testa, corpo = ARRIVI[indice]
    bordo, fondo = AVVISI['ok']
    fb, fr = f(N_BLD, 15), f(N_REG, 15)
    larg = W - 2 * M
    righe = avvolgi(dr, corpo, fr, larg - 60 - lx(dr, testa, fb))
    h = 16 + 20 * len(righe)
    dr.rectangle([M, y, M + larg, y + h], fill=fondo, outline=bordo, width=2)
    dr.rectangle([M, y, M + 6, y + h], fill='#3f8f5f')
    spunta(dr, M + 18, y + 12, '#3f8f5f', 3)
    dr.text((M + 40, y + 8), testa, font=fb, fill='#2e6b43')
    x = M + 46 + lx(dr, testa, fb)
    for i, r in enumerate(righe):
        dr.text((x, y + 8 + i * 20), r, font=fr, fill=INK)
    return y + h + 16


def ingresso(dr, y, indice, separate):
    if separate:
        return arrivo(dr, y, indice)
    return linguette(dr, y, PAGINE, indice, fatte=tuple(range(indice)))


# -------------------------------------------------------------------------------- pagine
def validazione(dest, separate=False):
    im, dr, y = pagina("Dichiarazione Nascita – Validazione ANSC")
    y = ingresso(dr, y, 0, separate)
    y = testata_atto(dr, y, "— (nessun atto)", "—")

    y0 = y
    y = pannello(dr, y, "Validazione del modello evento", 128)
    larg = (W - 2 * M - 24 - 36) // 4
    x = M + 12
    for et, val in (("Versione del modello ANSC", "1.53.0"), ("Data di formazione", "21/10/2026"),
                    ("Revisione del modello evento", "7"), ("Ultima validazione riuscita", "—")):
        campo(dr, x, y, larg, et, val, 'lettura')
        x += larg + 12
    y += 58
    dr.text((M + 12, y), "Il modello evento è costruito dai dati dell’atto e inviato ad ANSC con "
            "R009 /validazione/evento. Una risposta negativa non crea nulla in ANSC.",
            font=f(N_ITA, 14), fill=MUTED)
    y = y0 + 128 + 16

    y0 = y
    y = pannello(dr, y, "Esito della validazione", 214)
    y = avviso(dr, y, "ANSC ha restituito anomalie superabili con una forzatura: l’atto non è "
               "stato depositato. Correggere i dati oppure, se le anomalie sono volute, "
               "validare con il codice di forzatura.", 'attenzione', M + 12, W - 2 * M - 24)
    y = tabella(dr, y, ("Tipo", "Codice", "Descrizione restituita da ANSC", "Dove si corregge", ""),
                (120, 100, 690, 260, 130),
                [("Anomalia", "400003", "Dati in ingresso non corretti: data di nascita "
                  "successiva alla data di formazione", "Dettaglio – soggetto",
                  lambda d, x, yy: d.text((x, yy), "VAI ALLA PAGINA", font=f(N_BLD, 13),
                                          fill=ROSSO)),
                 ("Avviso", "—", "Esempio di avviso non bloccante", "—", "")],
                x=M + 12)
    y = y0 + 214 + 16

    y0 = y
    y = pannello(dr, y, "Forzatura (visibile solo se ANSC concede un codice di forzatura)", 132)
    campo(dr, M + 12, y, 260, "Codice di forzatura concesso da ANSC", "XXXXX_1234", 'lettura')
    casella(dr, M + 300, y + 24, "Confermo, come ufficiale dello stato civile, la forzatura delle "
            "anomalie elencate", segnata=False)
    y += 56
    dr.text((M + 12, y), "Un atto forzato entra in ANSC come anomalo: per questi atti ANSC dichiara "
            "non ancora implementato il ciclo delle conferme (OP-21, OP-41).",
            font=f(N_ITA, 14), fill=MUTED)
    y = y0 + 132 + 16

    y = pulsantiera(dr, y, [("INDIETRO", True)],
                    [("SOSPENDI", True), ("VALIDA", True), ("VALIDA CON FORZATURA", False),
                     ("AVANTI", False)])
    return ritaglia(im, y, dest)


def _firma_radio(autografa):
    def disegna(dr, x, y):
        nx = radio(dr, x, y, "Autografa", autografa)
        radio(dr, nx, y, "Digitale", not autografa)
    return disegna


def _azioni(testo):
    def disegna(dr, x, y):
        dr.text((x, y), testo, font=f(N_BLD, 13), fill=ROSSO)
    return disegna


def firme(dest, separate=False):
    im, dr, y = pagina("Dichiarazione Nascita – Firme dei dichiaranti")
    y = ingresso(dr, y, 1, separate)
    y = testata_atto(dr, y, "2 CONFERMATO", ID_ANSC)

    y0 = y
    y = pannello(dr, y, "Firmatari dell’atto (dal riepilogo)", 168)
    y = tabella(dr, y, ("Firmatario", "Ruolo", "Modalità di firma", "Email per la firma digitale",
                        "Stato della firma", "Azioni"),
                (190, 150, 210, 230, 260, 252),
                [("ROSSI PAOLO", "Dichiarante (padre)", _firma_radio(True), "—",
                  "Documento caricato, in verifica", ""),
                 ("VERDI LUCA", "Interprete", _firma_radio(False), "l.verdi@esempio.it",
                  "Link inviato, da visionare", _azioni("INVIA DI NUOVO · ANNULLA LINK"))],
                x=M + 12)
    y = y0 + 168 + 16

    y0 = y
    y = pannello(dr, y, "Firme autografe", 176)
    dr.text((M + 12, y), "1. Stampare l’anteprima dell’atto e farla firmare ai dichiaranti "
            "presenti.", font=f(N_REG, 14), fill=INK)
    bottone(dr, W - M - 12 - 230, y - 6, "STAMPA ANTEPRIMA DELL’ATTO")
    y += 34
    dr.text((M + 12, y), "2. Caricare il documento con le firme autografe (PDF, JPG, TIF, P7M).",
            font=f(N_REG, 14), fill=INK)
    y += 22
    campo(dr, M + 12, y, 620, "Documento con le firme autografe", "Processo_verbale_firme.pdf",
          'file')
    bottone(dr, M + 650, y + 19, "CARICA")
    campo(dr, M + 760, y, 240, "Stato del documento (ANSC_08)", "In elaborazione", 'lettura')
    bottone(dr, M + 1015, y + 19, "VERIFICA")
    y = y0 + 176 + 16

    y = avviso(dr, y, "Si prosegue quando ANSC porta l’atto a 4 FIRMATO DAL DICHIARANTE. "
               "Prima di qualunque firma i dati si possono riaprire con TORNA ALLA COMPILAZIONE; "
               "dopo, solo se tutti i firmatari sono in condizione di firmare di nuovo.", 'info')
    y = pulsantiera(dr, y, [("INDIETRO", True), ("TORNA ALLA COMPILAZIONE", True)],
                    [("ELIMINA EVENTO", True), ("VERIFICA STATO EVENTO", True),
                     ("SOSPENDI", True), ("AVANTI", False)])
    return ritaglia(im, y, dest)


def riapertura(dest):
    """La finestra di conferma di «Torna alla compilazione» dopo le firme dei dichiaranti."""
    larg, alt = 900, 362
    im = Image.new('RGB', (larg, alt), '#7f7f7f')
    dr = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 30, 24, larg - 30, alt - 24
    dr.rectangle([x0, y0, x1, y1], fill='white', outline=BORDO)
    dr.rectangle([x0, y0, x1, y0 + 40], fill=ROSSO)
    dr.text((x0 + 14, y0 + 10), "Riaprire i dati dell’atto?", font=f(N_BLD, 17), fill='white')
    ft = f(N_BLD, 13)
    dr.text((x1 - lx(dr, "IPOTESI DI SCHERMATA", ft) - 14, y0 + 13), "IPOTESI DI SCHERMATA",
            font=ft, fill='#f3d7de')
    y = y0 + 56
    fr = f(N_REG, 14)
    for r in avvolgi(dr, "I dichiaranti hanno già firmato. Riaprendo i dati la validazione e le "
                     "firme raccolte non valgono più: l’atto torna nello stato 0, va validato "
                     "di nuovo e tutti i firmatari dovranno firmare un’altra volta. Si può "
                     "procedere solo se ciascuno di loro è in condizione di farlo.", fr,
                     x1 - x0 - 28):
        dr.text((x0 + 14, y), r, font=fr, fill=INK)
        y += 20
    y += 10
    casella(dr, x0 + 14, y, "ROSSI PAOLO (dichiarante, firma autografa) è presente e firmerà "
            "di nuovo", segnata=True)
    y += 28
    casella(dr, x0 + 14, y, "VERDI LUCA (interprete, firma digitale) riceverà un nuovo link e "
            "firmerà di nuovo", segnata=False)
    y += 36
    bordo, fondo = AVVISI['attenzione']
    dr.rectangle([x0 + 14, y, x1 - 14, y + 48], fill=fondo, outline=bordo)
    for i, r in enumerate(avvolgi(dr, "Finché tutte le caselle non sono segnate RIAPRI I DATI "
                                  "resta disabilitato: l’alternativa è ELIMINA EVENTO (R011) "
                                  "e un atto nuovo.", fr, x1 - x0 - 52)):
        dr.text((x0 + 26, y + 6 + i * 19), r, font=fr, fill=INK)
    y += 66
    bottoni_dx(dr, y, [("ANNULLA", True), ("RIAPRI I DATI", False)], x_fine=x1 - 14)
    im.save(dest)
    return dest


def _pagina_pdf(dr, x, y, w, allegati=None):
    """Il PDF dell'attestazione così come lo genera ANSC (guida operativa, Figura 29)."""
    h = 300
    dr.rectangle([x, y, x + w, y + h], fill='#525659')
    px, pw = x + 40, w - 80
    dr.rectangle([px, y + 14, px + pw, y + h - 14], fill='white')
    cx = px + pw / 2
    fb, fr = f(N_BLD, 15), f(N_REG, 13)
    t = "Attestazione di conformità"
    dr.text((cx - lx(dr, t, fb) / 2, y + 30), t, font=fb, fill=INK)
    t = "Comune di ROMA (Provincia di RM)"
    dr.text((cx - lx(dr, t, fr) / 2, y + 54), t, font=fr, fill=INK)
    yy = y + 84
    dr.text((px + 30, yy), "Attestazione di conformità", font=f(N_BLD, 13), fill=INK)
    yy += 20
    for r in avvolgi(dr, "NOME COGNOME, ufficiale dello stato civile, attesta, che le copie "
                     "allegate ed elencate nella sezione Allegati, sono conformi ai sensi di "
                     "legge.", fr, pw - 60):
        dr.text((px + 30, yy), r, font=fr, fill=INK)
        yy += 17
    yy += 8
    dr.text((px + 30, yy), "Evento", font=f(N_BLD, 13), fill=INK)
    yy += 18
    for et, val in (("Intestatario:", "ROSSI MARIO"), ("ID atto:", ID_ANSC),
                    ("Codice caso d’uso:", "11111000")):
        dr.text((px + 30, yy), et, font=fr, fill=INK)
        dr.text((px + 170, yy), val, font=f(N_BLD, 13), fill=INK)
        yy += 16
    yy += 6
    dr.text((px + 30, yy), "Allegati", font=f(N_BLD, 13), fill=INK)
    yy += 18
    for i, riga in enumerate(allegati or ["Attestazione di nascita – Codice hash: "
                                          "c5znaSOl16V2si…"]):
        dr.text((px + 30, yy + i * 17), riga, font=fr, fill=INK)
    return y + h


def conformita(dest, separate=False):
    im, dr, y = pagina("Dichiarazione Nascita – Attestazione di conformità degli allegati")
    y = ingresso(dr, y, 2, separate)
    y = testata_atto(dr, y, "4 FIRMATO DAL DICHIARANTE", ID_ANSC)

    y0 = y
    y = pannello(dr, y, "Allegati da attestare", 248)

    def sel(segnata):
        return lambda d, x, yy: casella(d, x, yy, "", segnata)
    y = tabella(dr, y, ("", "Documento", "Tipo (ANSC_09)", "Formato", "Stato", "Note"),
                (50, 330, 260, 90, 130, 432),
                [(sel(True), "Attestazione di nascita", "Attestazione di nascita", "PDF",
                  "Inserito", "scansione di un originale cartaceo"),
                 (sel(True), "Processo verbale delle firme", "999 Processo verbale", "PDF",
                  "Inserito", "firme autografe dei dichiaranti"),
                 (sel(False), "Delega del padre", "Allegato generico", "P7M", "Inserito",
                  "già firmato digitalmente: non preselezionato")],
                x=M + 12)
    bottone(dr, M + 12, y, "GENERA ATTESTAZIONE DI CONFORMITÀ")
    y = y0 + 248 + 16

    y0 = y
    y = pannello(dr, y, "Anteprima dell’attestazione (PDF generato da ANSC, R010)", 352)
    _pagina_pdf(dr, M + 12, y, W - 2 * M - 24)
    y = y0 + 352 + 16

    y0 = y
    y = pannello(dr, y, "Firma remota dell’attestazione (R007 /attestazione/firma)", 110)
    larg = (W - 2 * M - 24 - 24) // 3
    campo(dr, M + 12, y, larg, "Utenza *", "utenza.firma.remota")
    campo(dr, M + 24 + larg, y, larg, "PIN *", "********", 'password')
    campo(dr, M + 36 + 2 * larg, y, larg, "OTP del servizio di firma *", "")
    y = y0 + 110 + 16

    y = pulsantiera(dr, y, [("INDIETRO", True), ("TORNA ALLA COMPILAZIONE", False)],
                    [("ELIMINA EVENTO", True), ("SOSPENDI", True), ("CONTINUA", False),
                     ("FIRMA", True)])
    return ritaglia(im, y, dest)


def firma_usc(dest, separate=False):
    im, dr, y = pagina("Dichiarazione Nascita – Firma dell’ufficiale dello stato civile")
    y = ingresso(dr, y, 3, separate)
    y = testata_atto(dr, y, "11 FIRMATO PER CONFORMITÀ", ID_ANSC)

    y0 = y
    y = pannello(dr, y, "Firma dell’atto", 110)
    casella(dr, M + 12, y + 24, "Comunicazione anagrafica (R014)", segnata=True,
            ft=f(N_BLD, 14))
    campo(dr, M + 330, y, 240, "Data validità evento *", "14/10/2026", 'data')
    bottone(dr, W - M - 12 - 200, y + 19, "ANTEPRIMA DELL’ATTO")
    y = y0 + 110 + 16

    y0 = y
    y = pannello(dr, y, "Firma remota dell’atto (R007 /firma_usc)", 110)
    larg = (W - 2 * M - 24 - 24) // 3
    campo(dr, M + 12, y, larg, "Utenza *", "utenza.firma.remota")
    campo(dr, M + 24 + larg, y, larg, "PIN *", "********", 'password')
    campo(dr, M + 36 + 2 * larg, y, larg, "OTP del servizio di firma *", "")
    y = y0 + 110 + 16

    y = avviso(dr, y, "CHIUDI firma l’atto in ANSC, invia la data di validità se è richiesta la "
               "comunicazione anagrafica e salva l’atto in SIPO. Dopo la firma l’atto non si "
               "modifica più: INDIETRO ed ELIMINA EVENTO si disabilitano e le correzioni "
               "diventano procedimenti di ANSC (annotazione, rettifica, annullamento).",
               'attenzione')
    y = pulsantiera(dr, y, [("INDIETRO", True)],
                    [("ELIMINA EVENTO", True), ("SOSPENDI", True), ("CHIUDI", True)])
    return ritaglia(im, y, dest)


def esito_chiusura(dest, separate=True):
    """La schermata che segue CHIUDI: l'esito delle tre operazioni della chiusura."""
    im, dr, y = pagina("Dichiarazione Nascita – Esito della chiusura dell’atto")
    y = arrivo(dr, y, 4)
    y = testata_atto(dr, y, "5 FIRMATO DA USC", ID_ANSC, "2 DEFINITO")

    def esito(testo, ok=True):
        def disegna(d, x, yy):
            colore = '#3f8f5f' if ok else '#b03a48'
            if ok:
                spunta(d, x, yy + 3, colore, 3)
            d.text((x + 20, yy), testo, font=f(N_BLD, 14), fill=colore)
        return disegna
    y0 = y
    y = pannello(dr, y, "Esito della chiusura", 238)
    y = tabella(dr, y, ("Operazione", "Servizio", "Esito", "Dettaglio"),
                (300, 280, 200, 528),
                [("Firma dell’atto", "R007 /firma_usc", esito("Riuscita"),
                  "Atto formato in ANSC: " + ID_ANSC),
                 ("Data di validità", "R014 /evento/data-validita", esito("Riuscita"),
                  "14/10/2026, comunicazione anagrafica richiesta"),
                 ("Salvataggio in SIPO", "/finalizzaAtto", esito("Riuscito"),
                  "Pratica 2 DEFINITO"),
                 ("Aggiornamento anagrafico", "InitFlow", esito("Riuscito"),
                  "Se non riesce o resta in attesa: pratica 3, sospesa in SIPO")],
                x=M + 12)
    y = y0 + 238 + 16
    y = avviso(dr, y, "L’atto non si modifica più: le correzioni diventano procedimenti di ANSC "
               "(annotazione, rettifica, annullamento). Se il salvataggio in SIPO non riesce, "
               "la stessa schermata lo mostra in rosso con RIPROVA, che ripete solo il "
               "salvataggio e mai la firma.", 'info')
    y = pulsantiera(dr, y, [("TORNA ALLA RICERCA", True)],
                    [("STAMPE", True), ("NUOVO ATTO", True)])
    return ritaglia(im, y, dest)


def percorso(dest, sorgenti):
    """La sequenza delle schermate separate, con il comando e l'esito su ogni passaggio.

    `sorgenti`: i PNG delle schermate v0.3, nell'ordine validazione, firme, conformità,
    firma dell'USC, esito della chiusura.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import diagrammi_comune as G
    VERDE, VIOLA = '#3f8f5f', '#7b5aa6'
    tw = 460
    cols = (50, 700, 1350)
    larg = 1860
    im, dr = G.tela(larg, 1400, "Il percorso fra le schermate",
                    "ogni schermata è una pagina di SIPO a sé; sulle frecce il comando, il servizio "
                    "e lo stato che ne risulta; ogni schermata si apre con l’esito del passaggio")
    miniature = []
    for p in sorgenti:
        m = Image.open(p).convert('RGB')
        miniature.append(m.resize((tw, int(m.height * tw / m.width)), Image.LANCZOS))
    ft = G.fnt(G.F_BLD, 18)

    def incolla(m, x, y, titolo):
        dr.text((x, y - 30), titolo, font=ft, fill=G.INK)
        im.paste(m, (x, y))
        dr.rectangle([x - 1, y - 1, x + m.width, y + m.height], outline='#9a9a9a', width=2)
        return (x, y, m.width, m.height)

    y1 = 170
    # l'anteprima di SIPO, pagina esistente: un segnaposto, non un'ipotesi
    ax, aw, ah = cols[0], tw, 250
    dr.text((ax, y1 - 30), "Anteprima SIPO (esistente, modificata)", font=ft, fill=G.INK)
    dr.rectangle([ax, y1, ax + aw, y1 + ah], fill='#f4f4f4', outline='#9a9a9a', width=2)
    dr.rectangle([ax, y1, ax + aw, y1 + 34], fill=ROSSO)
    for i, r in enumerate(("testo dell’atto", "numero comunale definitivo",
                           "avviso: servono utenza, PIN e OTP di firma")):
        dr.text((ax + 24, y1 + 60 + i * 30), "· " + r, font=G.fnt(G.F_REG, 17), fill=G.INK)
    dr.rectangle([ax + aw - 110, y1 + ah - 50, ax + aw - 24, y1 + ah - 20], fill=ROSSO)
    dr.text((ax + aw - 92, y1 + ah - 44), "VALIDA", font=G.fnt(G.F_BLD, 15), fill='white')
    A = (ax, y1, aw, ah)
    V = incolla(miniature[0], cols[1], y1, "1 · Validazione")
    F = incolla(miniature[1], cols[2], y1, "2 · Firme dei dichiaranti")
    y2 = y1 + max(V[3], F[3], ah) + 200
    C = incolla(miniature[2], cols[2], y2, "3 · Conformità")
    U = incolla(miniature[3], cols[1], y2, "4 · Firma dell’USC")
    E = incolla(miniature[4], cols[0], y2, "5 · Esito della chiusura")

    def et(testo, x, y, colore=G.ARROW, ts=15):
        fe = G.fnt(G.F_REG, ts)
        righe = testo.split("\n")
        lw = max(G.larghezza(dr, r, fe) for r in righe)
        dr.rectangle([x - 3, y - 2, x + lw + 3, y + len(righe) * (ts + 4)], fill='white')
        for i, r in enumerate(righe):
            dr.text((x, y + i * (ts + 4)), r, font=fe, fill=colore)

    def destra(a, b, yy, testo):
        G.freccia(dr, (a[0] + a[2], yy), (b[0], yy), VERDE)
        et(testo, a[0] + a[2] + 12, yy - 66, VERDE)

    def sinistra(a, b, yy, testo):
        G.freccia(dr, (a[0], yy), (b[0] + b[2], yy), VERDE)
        et(testo, b[0] + b[2] + 12, yy - 66, VERDE)

    destra(A, V, y1 + 120, "VALIDA\nnumero comunale\nstaccato")
    destra(V, F, y1 + 120, "AVANTI\nR009 riuscita:\nANSC 2, idAnsc")
    # firme → conformità, in verticale
    fx = F[0] + F[2] * 0.62
    G.freccia(dr, (fx, F[1] + F[3]), (fx, C[1] - 32), VERDE)
    et("AVANTI\nANSC 4 FIRMATO\nDAL DICHIARANTE", fx + 14, F[1] + F[3] + 40, VERDE)
    sinistra(C, U, y2 + 120, "AVANTI (ANSC 11)\no CONTINUA")
    sinistra(U, E, y2 + 120, "CHIUDI\nR007 · R014 ·\nsalvataggio SIPO")
    # i salti
    ya = y2 - 120
    G.linea(dr, [(V[0] + 160, V[1] + V[3]), (V[0] + 160, ya), (C[0] + 70, ya)], G.MUTED, True)
    G.freccia(dr, (C[0] + 70, ya), (C[0] + 70, C[1] - 32), G.MUTED)
    et("AVANTI [nessun firmatario]", V[0] + 176, ya - 26, G.MUTED)
    yb = y2 - 70
    G.linea(dr, [(F[0] + 110, F[1] + F[3]), (F[0] + 110, yb), (U[0] + 300, yb)], G.MUTED, True)
    G.freccia(dr, (U[0] + 300, yb), (U[0] + 300, U[1] - 32), G.MUTED)
    et("[nessun allegato da attestare: la conformità si salta]", U[0] + 316, yb + 6, G.MUTED)
    yfine = y2 + max(C[3], U[3], E[3]) + 40
    G.linea(dr, [(60, yfine), (120, yfine)], G.ARROW, True, 2)
    dr.text((134, yfine - 10), "INDIETRO riporta sempre alla schermata precedente; TORNA ALLA "
            "COMPILAZIONE, da Firme e Conformità, alle pagine dei dati secondo la regola del "
            "ritorno dopo le firme. Tratteggio: passaggi che saltano una schermata.",
            font=G.fnt(G.F_ITA, 15), fill=G.MUTED)
    im.crop((0, 0, larg, yfine + 40)).save(dest)
    return dest


SCHERMATE = {
    'wf_sch_validazione.png': validazione,
    'wf_sch_firme.png': firme,
    'wf_sch_riapertura.png': riapertura,
    'wf_sch_conformita.png': conformita,
    'wf_sch_firma_usc.png': firma_usc,
}


def disegna_tutte():
    return [fn(os.path.join(IMG, nome)) for nome, fn in SCHERMATE.items()]


# v0.3: schermate separate, con il banner di arrivo, la schermata di esito e il percorso
SCHERMATE_V3 = {
    'wf3_sch_validazione.png': validazione,
    'wf3_sch_firme.png': firme,
    'wf3_sch_conformita.png': conformita,
    'wf3_sch_firma_usc.png': firma_usc,
    'wf3_sch_esito.png': esito_chiusura,
}


def disegna_v3():
    fatti = [fn(os.path.join(IMG, nome), separate=True) for nome, fn in SCHERMATE_V3.items()]
    fatti.append(riapertura(os.path.join(IMG, 'wf_sch_riapertura.png')))
    fatti.append(percorso(os.path.join(IMG, 'wf3_percorso.png'), fatti[:5]))
    return fatti


if __name__ == '__main__':
    for p in disegna_tutte() + disegna_v3():
        print('scritto:', p)
    sys.exit(0)
