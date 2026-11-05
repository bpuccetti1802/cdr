# -*- coding: utf-8 -*-
"""I due flussi specializzati per il MATRIMONIO, in PowerPoint con forme e connettori nativi,
sulla falsariga di `diagramma_workflow_pptx.py`.

⚠️ CORREZIONE D'IMPIANTO (utente, 05/11/2026), che la prima stesura sbagliava: **l'obiettivo è
l'atto DIGITALE**, non un atto cartaceo da riportare su ANSC. La preparazione avviene in SIPO e
nello store locale (`ANSC_STATO_ATTO`); il cartaceo, se c'è, è un «di cui». Nella v1 di questi
diagrammi la banda della cerimonia diceva «l'atto si legge e si firma su carta», che faceva della
carta l'atto e di ANSC la sua trascrizione: capovolto.

Impianto del flusso A, nell'ipotesi dell'utente:
  * fino alla data del matrimonio si svolgono in SIPO le attività propedeutiche (pubblicazioni,
    prenotazione, dati degli sposi) e **l'unica chiamata ad ANSC è R005 sugli intestatari**, in
    sola lettura; la riga dello store nasce qui;
  * finita la celebrazione, l'USC chiama i testimoni: si inseriscono gli ultimi dati, si stacca
    il numero comunale e **si predispone il payload**, con gli adempimenti sulle varie tabelle;
  * poi il deposito e le firme.

CINQUE corsie, perché lo stato è in tre posti e non in due: pagina di SIPO · servizio chiamato ·
stato in SIPO (`ID_STATO_PRATICA`) · **store locale `ANSC_STATO_ATTO` (`COD_FASE`)** · stato in
ANSC (`ANSC_11`). I valori di COD_FASE sono quelli della v3.56: IN_LAVORAZIONE, UC_DETERMINATO,
DOCUMENTI_ACQUISITI, PREVALIDATO, VALIDATO, FIRMATO, ANNULLATO.

La domanda da sottoporre all'esperto è nel riquadro in coda alla A: **come firmano i presenti un
atto digitale.** R012 è elettronica ma vuole una chiamata, una email e una sessione di firma
remota PER CIASCUN firmatario (`emailDichiarante` singolare, `firmatario` un solo ModelSoggetto,
risposta `idPresaVisione`); R006 carica un file unico e dichiara tutti i firmatari in
`listaFirmatari`. Con 5-6 firmatari obbligatori presenti in sala, R006 è l'unica praticabile — e
il foglio che si carica è un **allegato** dell'atto digitale, non l'atto.

Il flusso B resta il percorso degradato: lì l'atto si forma davvero su carta, ed è legittimo
perché è un recupero — ma allora l'UC è `Matr_999` e `motivoRecupero` (ANSC_96) è obbligatorio.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_matrimonio_pptx.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagramma_workflow_pptx as B   # noqa: E402  — riuso le primitive, non le riscrivo

OUT_A = os.path.join(QUI, 'img', 'flusso_matr_diretta.pptx')
OUT_B = os.path.join(QUI, 'img', 'flusso_matr_differito.pptx')

W = 9.3
STRIP = (0.18, 0.17)
COL = {'A': (0.44, 2.62), 'B': (3.18, 1.74), 'C': (5.04, 1.10), 'D': (6.26, 1.52),
       'E': (7.90, 1.22)}
INTEST = {'A': 'Pagina di SIPO', 'B': 'Servizio chiamato', 'C': 'Stato in SIPO',
          'D': 'Store locale ANSC_STATO_ATTO', 'E': 'Stato in ANSC'}
Y0, RH, GAP = 1.52, 0.46, 0.085

PAGINA, BANDA = 'pagina', 'banda'
NIENTE = 'Nessun atto in ANSC'

# ───────────────────────────────────────────── A: l'atto digitale, preparato e depositato dopo
# (tipo, titolo, sottotitolo, servizio, stato SIPO, COD_FASE dello store, stato ANSC, fase)
FA, FB, FC, FD = ('A — Dati e attività propedeutiche', 'B — Riepilogo',
                  'C — Anteprima e «VALIDA»', 'D — Firme e definizione')
CEL = 'Celebrazione'

PASSI_A = [
    (PAGINA, 'Pubblicazioni e prenotazione della sala',
     'settimane prima: pubblicazioni, sala, data e ora, officiante', '',
     '1 IN LAVORAZIONE', '—', NIENTE, FA),
    (PAGINA, 'Apertura dell’atto',
     'numero provvisorio in SIPO; nasce la riga nello store', '',
     '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FA),
    (PAGINA, 'Dati degli sposi e dell’atto',
     'rito, regime, genitori e tutori, autorizzazioni, impedimenti', '',
     '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FA),
    (PAGINA, 'Sposo e sposa in ANSC',
     'unica chiamata ad ANSC prima della cerimonia; scrive ANSC_SOGGETTO_IDENTIFICATIVI',
     'R005 /consultazione', '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FA),
    (BANDA, 'CELEBRAZIONE',
     'l’USC celebra; nessun atto è ancora formato, né digitale né cartaceo', '',
     '', '', '', CEL),
    (PAGINA, 'Testimoni, interprete e comparenti',
     'l’USC li chiama: numeroTestimoni e 8 campi per ciascuno', '',
     '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FB),
    (PAGINA, 'Riepilogo: UC e firmatari',
     'l’UC si determina dai dati; i firmatari entrano in ANSC_USR.firmatari',
     'preverifica locale', '1 IN LAVORAZIONE', 'UC_DETERMINATO', NIENTE, FB),
    (PAGINA, 'Documenti e verifica locale',
     'allegati se previsti dall’UC; pre-filtro campo per campo',
     'R001 · preverifica', '1 IN LAVORAZIONE', 'DOCUMENTI_ACQUISITI', NIENTE, FB),
    (PAGINA, 'Numero comunale',
     'staccato adesso, nell’ordine delle celebrazioni; scrive NUMERO_ATTO',
     'be-numeratore-comunale\nPOST /richiesta', '1 IN LAVORAZIONE', 'PREVALIDATO', NIENTE, FC),
    (PAGINA, 'Costruzione del payload',
     'si compone dalla configurazione e si conserva: TXT_EVENTO, testata, ID_VERSIONE', '',
     '1 IN LAVORAZIONE', 'PREVALIDATO', NIENTE, FC),
    (PAGINA, 'Anteprima e «VALIDA»',
     'l’atto digitale entra in ANSC; ID_ANSC si salva sullo store',
     'R009 /validazione/evento', '1 IN LAVORAZIONE', 'VALIDATO', '2 CONFERMATO', FC),
    (PAGINA, 'Firme dei firmatari',
     'in ANSC_USR.firmatari, per ciascuno, ty_firma e cd_stato_firma',
     'R006 cartacea · R012 elettronica', '1 IN LAVORAZIONE', 'VALIDATO',
     '4 FIRMATO DAL DICHIARANTE', FD),
    (PAGINA, 'Attestazione di conformità', 'firmata dall’ufficiale',
     'R007 /attestazione/firma', '1 IN LAVORAZIONE', 'VALIDATO',
     '11 FIRMATO PER CONFORMITÀ', FD),
    (PAGINA, 'Firma dell’ufficiale', 'l’atto digitale è formato', 'R007 /firma_usc',
     '1 IN LAVORAZIONE', 'FIRMATO', '5 FIRMATO DA USC', FD),
    (PAGINA, 'Definisci', 'salvataggio in SIPO', 'salvataggio in SIPO', '2 DEFINITO',
     'FIRMATO', '5 FIRMATO DA USC', FD),
    (PAGINA, 'Chiudi', 'l’atto non si modifica più', '', '2 DEFINITO', 'FIRMATO',
     '5 FIRMATO DA USC', FD),
]

# ─────────────────────────────────────────────────── B: percorso degradato, l'atto nasce su carta
FB1, FB2, FB3 = ('A — Attività propedeutiche', 'Recupero',
                 'B — Deposito tardivo e firme')
PASSI_B = [
    (PAGINA, 'Pubblicazioni e prenotazione della sala',
     'settimane prima: pubblicazioni, sala, data e ora, officiante', '',
     '1 IN LAVORAZIONE', '—', NIENTE, FB1),
    (PAGINA, 'Dati degli sposi e dell’atto',
     'rito, regime, genitori e tutori, autorizzazioni, impedimenti', '',
     '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FB1),
    (BANDA, 'CELEBRAZIONE — l’atto si forma SU CARTA',
     'i testimoni si identificano in sala; la carta è l’atto, non un «di cui»', '',
     '', '', '', FB2),
    (BANDA, 'INTERRUZIONE: ore o giorni',
     'l’atto esiste su carta e non esiste in ANSC', '', '', '', '', FB2),
    (PAGINA, 'Testimoni inseriti a posteriori',
     'trascritti dal cartaceo, senza gli interessati presenti', '',
     '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FB3),
    (PAGINA, 'Soggetti in ANSC', 'se R005 non trova un soggetto, si scopre adesso',
     'R005 /consultazione', '1 IN LAVORAZIONE', 'IN_LAVORAZIONE', NIENTE, FB3),
    (PAGINA, 'Riepilogo: UC DI SERVIZIO Matr_999',
     'motivoRecupero (ANSC_96) obbligatorio e idAttoCartaceo',
     'preverifica locale', '1 IN LAVORAZIONE', 'UC_DETERMINATO', NIENTE, FB3),
    (PAGINA, 'Numero comunale', 'staccato fuori dall’ordine di celebrazione',
     'be-numeratore-comunale\nPOST /richiesta', '1 IN LAVORAZIONE', 'PREVALIDATO', NIENTE, FB3),
    (PAGINA, 'Anteprima e «VALIDA»', 'un rifiuto qui riguarda un atto già celebrato e firmato',
     'R009 /validazione/evento', '1 IN LAVORAZIONE', 'VALIDATO', '2 CONFERMATO', FB3),
    (PAGINA, 'Caricamento del cartaceo firmato', 'solo la via cartacea: R012 non è applicabile',
     'R006 cartacea', '1 IN LAVORAZIONE', 'VALIDATO', '4 FIRMATO DAL DICHIARANTE', FB3),
    (PAGINA, 'Attestazione di conformità', 'firmata dall’ufficiale', 'R007 /attestazione/firma',
     '1 IN LAVORAZIONE', 'VALIDATO', '11 FIRMATO PER CONFORMITÀ', FB3),
    (PAGINA, 'Firma dell’ufficiale', 'utenza, PIN e OTP della firma remota', 'R007 /firma_usc',
     '1 IN LAVORAZIONE', 'FIRMATO', '5 FIRMATO DA USC', FB3),
    (PAGINA, 'Definisci', 'salvataggio in SIPO', 'salvataggio in SIPO', '2 DEFINITO', 'FIRMATO',
     '5 FIRMATO DA USC', FB3),
    (PAGINA, 'Chiudi', 'l’atto non si modifica più', '', '2 DEFINITO', 'FIRMATO',
     '5 FIRMATO DA USC', FB3),
]

RILIEVI_B = [
    ('L’UC non è più quello di celebrazione', 'un atto formato fuori dal percorso di ANSC rientra '
     'con Matr_999, dove motivoRecupero è obbligatorio: e fra i sei valori di ANSC_96 nessuno '
     'significa «differimento scelto». Resterebbe 101 ALTRO, dichiarato su ogni matrimonio.'),
    ('Il rifiuto arriva troppo tardi', 'R009 può rispondere 400001 per un campo obbligatorio '
     'mancante. In diretta si corregge con gli interessati presenti; qui l’atto è già firmato.'),
    ('I numeri comunali non seguono le celebrazioni',
     'il numeratore dà i numeri nell’ordine in cui sono chiesti, non in quello delle cerimonie.'),
    ('La ricerca del soggetto non ha più margine', 'senza idAnscSoggetto serve '
     '/collegamento/evento, che la nota ANSC dichiara «fortemente sconsigliato».'),
    ('I termini corrono', 'oltre il termine l’atto è tardivo e scatta la comunicazione alla '
     'procura (ANSC_26 tipo 3).'),
    ('L’effetto anagrafico slitta', 'la comunicazione all’anagrafe segue il deposito: lo stato '
     'civile dei coniugi resta disallineato per tutta l’attesa.'),
]

DOMANDA_A = (
    'DA SOTTOPORRE ALL’ESPERTO — come firmano i presenti un atto digitale.  '
    'R012 è elettronica ma vuole una chiamata, una email e una sessione di firma remota PER '
    'CIASCUN firmatario (emailDichiarante singolare, firmatario un solo ModelSoggetto): con i '
    '5-6 firmatari obbligatori del matrimonio, in sala, non è praticabile.  R006 invece carica '
    'un file unico e dichiara tutti i firmatari in listaFirmatari.  Allora il foglio firmato in '
    'sala è un ALLEGATO dell’atto digitale — il «di cui» — e non l’atto: l’atto resta quello '
    'depositato in ANSC. Resta da confermare che R006 sia richiamabile più volte sullo stesso '
    'atto, se le firme si raccogliessero in più riprese.')


def y(i):
    return Y0 + i * (RH + GAP)


def _blocchi(passi, indice, prosegue=True):
    """Righe consecutive con la stessa etichetta -> (etichetta, da, a).
    Con `prosegue`, le bande ereditano l'etichetta precedente e non spezzano il blocco."""
    out, corrente = [], None
    for i, p in enumerate(passi):
        et = p[indice] if (p[0] == PAGINA or not prosegue) else corrente
        if not et:
            corrente = None
            continue
        corrente = et
        if out and out[-1][0] == et and out[-1][2] == i - 1:
            out[-1] = (et, out[-1][1], i)
        else:
            out.append((et, i, i))
    return out


def genera(passi, titolo, sottotitolo, percorso, rilievi=None, nota=None, colore_nota='verde'):
    righe = len(passi)
    coda = (2.62 if rilievi else 0.0) + (1.00 if nota else 0.0) + 0.45
    h_pagina = y(righe - 1) + RH + 0.30 + coda
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(h_pagina)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    bg = sl.background.fill
    bg.solid()
    bg.fore_color.rgb = B.rgb('ffffff')

    B.testo(sl, 0.25, 0.18, W - 0.5, 0.35, titolo, 15, True, '1f3a5f', PP_ALIGN.CENTER)
    B.testo(sl, 0.9, 0.54, W - 1.8, 0.56, sottotitolo, 8.5, False, B.MUTED, PP_ALIGN.CENTER,
            corsivo=True)

    for k, (x, w) in COL.items():
        B.testo(sl, x, 1.14, w, 0.30, INTEST[k], 8.5, True, B.INK, PP_ALIGN.CENTER)
        B.linea(sl, x, 1.42, x + w, 1.42, 'cbd5e1', tratteggio=False, spessore=1)

    # ── striscia delle fasi
    for et, da, a in _blocchi(passi, 7, prosegue=False):
        cerimonia = et in ('Celebrazione', 'Recupero')
        B.riquadro(sl, STRIP[0], y(da), STRIP[1], y(a) + RH - y(da),
                   'viola' if cerimonia else 'grigio',
                   [(et.split(' —')[0] if not cerimonia else '◆', 13, True,
                     '7b5aa6' if cerimonia else B.INK)], forma=MSO_SHAPE.RECTANGLE)

    # ── corsia A (pagine e bande) e corsia B (servizi)
    forme = []
    for i, p in enumerate(passi):
        tipo, tit, sotto, servizio = p[0], p[1], p[2], p[3]
        if tipo == BANDA:
            rosso = tit.startswith('INTERRUZIONE')
            s = B.riquadro(sl, COL['A'][0], y(i), COL['A'][1], RH,
                           'rosso' if rosso else 'viola',
                           [(tit, 9 if len(tit) > 18 else 10, True, None),
                            (sotto, 6.6, False, B.MUTED)],
                           forma=MSO_SHAPE.RECTANGLE, tratteggio=rosso)
        else:
            s = B.riquadro(sl, COL['A'][0], y(i), COL['A'][1], RH, 'blu',
                           [(tit, 8.5, True, None), (sotto, 6.4, False, B.MUTED)])
        forme.append(s)
        if servizio and tipo == PAGINA:
            sv = B.riquadro(sl, COL['B'][0], y(i) + 0.05, COL['B'][1], RH - 0.10, 'bianco',
                            [(servizio, 7, False, None)], forma=MSO_SHAPE.RECTANGLE)
            B.freccia(sl, s, 3, sv, 1, colore='94a3b8', spessore=0.9)
    for i in range(righe - 1):
        B.freccia(sl, forme[i], 2, forme[i + 1], 0)

    # ── corsie C (SIPO), D (store locale), E (ANSC)
    for indice, chiave, colore in ((4, 'C', 'verde'), (5, 'D', 'blu'), (6, 'E', 'giallo')):
        x, w = COL[chiave]
        prec = None
        for et, da, a in _blocchi(passi, indice):
            vuoto = et in (NIENTE, '—')
            testi = ([(NIENTE, 7.5, True, None), ('fino alla validazione', 6.2, False, B.MUTED)]
                     if et == NIENTE else
                     [(r, 7.5 if k == 0 else 6.5, k == 0, None)
                      for k, r in enumerate(et.split('\n'))])
            s = B.riquadro(sl, x, y(da), w, y(a) + RH - y(da), 'grigio' if vuoto else colore,
                           testi, tratteggio=vuoto)
            if prec is not None:
                B.freccia(sl, prec, 2, s, 0)
            prec = s

    # ── punto di non ritorno, subito dopo la firma dell'ufficiale
    i_usc = next(i for i, p in enumerate(passi) if p[1].startswith('Firma dell'))
    yn = y(i_usc + 1) - GAP / 2
    B.linea(sl, 0.2, yn, COL['C'][0] - 0.06, yn, 'b03a48')
    B.testo(sl, 2.6, yn + 0.010, COL['C'][0] - 0.06 - 2.6, 0.10, 'punto di non ritorno',
            6.5, True, 'b03a48', PP_ALIGN.RIGHT)

    # ── coda
    yb = y(righe - 1) + RH + 0.26
    if nota:
        B.riquadro(sl, 0.44, yb, W - 0.88, 0.88, colore_nota, [(nota, 7.4, False, None)],
                   forma=MSO_SHAPE.RECTANGLE, allinea=PP_ALIGN.LEFT)
        yb += 1.00
    if rilievi:
        B.testo(sl, 0.44, yb, 6.0, 0.2, 'Che cosa si paga differendo', 9.5, True, 'b03a48')
        yb += 0.22
        for k, (capo, corpo) in enumerate(rilievi):
            B.riquadro(sl, 0.44, yb + k * 0.33, W - 0.88, 0.30, 'rosso',
                       [(capo + ' — ' + corpo, 7, False, None)], forma=MSO_SHAPE.RECTANGLE,
                       allinea=PP_ALIGN.LEFT)
        yb += len(rilievi) * 0.33 + 0.06

    fasi = ' · '.join(dict.fromkeys(p[7] for p in passi if p[7]))
    B.testo(sl, 0.44, yb + 0.04, W - 0.88, 0.16, 'Fasi: ' + fasi, 6.8, False, B.MUTED)
    yb += 0.24
    voci = [('blu', 'pagina di SIPO · store locale'), ('bianco', 'servizio chiamato'),
            ('verde', 'stato in SIPO'), ('giallo', 'stato in ANSC (ANSC_11)'),
            ('viola', 'cerimonia')]
    if rilievi:
        voci.append(('rosso', 'interruzione e rilievi'))
    for k, (col, t) in enumerate(voci):
        B.riquadro(sl, 0.44 + k * 1.48, yb, 0.2, 0.12, col, [('', 6, False, None)],
                   forma=MSO_SHAPE.RECTANGLE)
        B.testo(sl, 0.67 + k * 1.48, yb - 0.015, 1.3, 0.15, t, 6.5)

    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


def genera_tutti():
    a = genera(
        PASSI_A, 'Matrimonio — flusso A: l’atto digitale, formato dopo la celebrazione',
        'Fino alla data del matrimonio si lavora in SIPO e si chiama ANSC solo in lettura (R005 '
        'sugli intestatari). Finita la cerimonia, l’USC chiama i testimoni: ultimi dati, numero '
        'comunale, payload, deposito e firme. UC ordinario di celebrazione.',
        OUT_A, nota=DOMANDA_A, colore_nota='giallo')
    b = genera(
        PASSI_B, 'Matrimonio — flusso B: salvataggio in ANSC differito',
        'L’atto si forma e si firma su carta; il percorso ANSC si svolge in una lavorazione '
        'successiva. Non è una variante organizzativa: è un recupero, e cambia l’UC.',
        OUT_B, rilievi=RILIEVI_B)
    return a, b


if __name__ == '__main__':
    for p in genera_tutti():
        print('scritto:', os.path.relpath(p, os.path.dirname(os.path.dirname(QUI))))
