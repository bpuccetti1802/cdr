# -*- coding: utf-8 -*-
"""I diagrammi dell'analisi delle nascite gemellari, v0.4 (21/11/2026), in PowerPoint con forme e
connettori nativi, modificabili dall'utente.

Nella v0.4 i due percorsi non sono più alternative in attesa di Sogei: li sceglie il parto.
  * gem4_panoramica.pptx — la scelta dopo la divisione: stesso UC per tutti i gemelli (caso 1, tutto
                           da SIPO) o UC diversi (caso 2, web app e recupero dell'intero parto);
  * gem4_flusso_1.pptx   — caso 1, a cinque corsie, con le righe dello store;
  * gem4_flusso_2.pptx   — caso 2, a cinque corsie: numeri in blocco e «Dati per ANSC» in SIPO,
                           web app, RECUPERA GEMELLI e DEFINISCI GEMELLI;
  * gem4_erd.pptx        — i legami, con la tabella nuova ANSC_SOGGETTO_ATTO.
Le versioni della v0.2 (gem_*.pptx) restano come erano.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v0_4_pptx.py
    qlmanage -t -s 2400 -o img/gemellari img/gemellari/gem4_*.pptx
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagramma_workflow_pptx as B             # noqa: E402
import diagrammi_matrimonio_pptx as M           # noqa: E402
from diagramma_annotazioni_erd_pptx import etichetta, lega, tabella   # noqa: E402

DIR = os.path.join(QUI, 'img', 'gemellari')
PAG, BAN, NI = M.PAGINA, M.BANDA, M.NIENTE

PRAT, NATTI = '1 IN LAVORAZIONE\nla sola pratica', '1 IN LAVORAZIONE\nN atti'
ATK, ATK1 = '1 IN LAVORAZIONE\natto k', '1 IN LAVORAZIONE\natto k+1'

INIZIO = [
    (PAG, 'Compilazione della pratica', 'tipo atto «gemelli»: genitori, dichiarante, N nati '
     'con i due flag', '', PRAT, '—', NI, 'A — Pratica unica'),
    (PAG, 'Genitori e dichiarante in ANSC', 'nasce la riga dell’atto della pratica, che sarà '
     'il gemello 1', 'R005 /consultazione', PRAT, '1 riga · gemello 1\nIN_LAVORAZIONE', NI,
     'A — Pratica unica'),
    (PAG, 'Riepilogo → Conferma', 'la pratica è divisa in N atti legati da '
     'ID_LAVORAZIONE_PADRE; lo store non cambia', '/performAttiPlurigemellari', NATTI,
     '1 riga · gemello 1\nIN_LAVORAZIONE', NI, 'A — Pratica unica'),
    (PAG, 'Riepilogo del gemello 1 · UC dei nati', 'UC di ciascun nato dai suoi flag: tutti '
     'uguali o no?', 'all-ansc-sipo (configurazione)', NATTI, '1 riga · gemello 1\nIN_LAVORAZIONE',
     NI, 'A — Pratica unica'),
]

# ───────────────────────────────────────────── caso 1: stesso UC, tutto da SIPO
F1B, F1C, F1D = 'B — Prenotazione', 'C — Gemello k', 'D — Chiusura'
PASSI_1 = INIZIO + [
    (PAG, 'PRENOTA GEMELLI · numeri', 'stesso UC per tutti: N numeri consecutivi',
     'be-numeratore-comunale\nPOST /richiesta', NATTI, 'N righe (2…N nuove)\nUC · NUMERO_ATTO',
     NI, F1B),
    (PAG, 'PRENOTA GEMELLI · prenotazione', 'idUsecase = l’UC comune; numero gemelli = '
     'totale; ATTI_GEMELLARI e ANSC_SOGGETTO_ATTO', 'R009 /prenota/evento', NATTI,
     'N righe\nPRENOTATO · ID_ANSC', 'N atti\n1 BOZZA', F1B),
    (BAN, 'PER CIASCUN GEMELLO k = 1 … N', 'in ordine di nascita: POS_GEMELLO = '
     'progressivoGemello', '', '', '', '', F1C),
    (PAG, 'Documenti del gemello k', 'certificato medico se nato morto o nato vivo e poi '
     'deceduto', 'R001 · preverifica', ATK, 'riga k\nDOCUMENTI_ACQUISITI', 'atto k\n1 BOZZA', F1C),
    (PAG, 'Anteprima del gemello k', 'composizione con le formule e gli idAnsc dei fratelli; '
     'campi gemellari', 'all-ansc-sipo', ATK, 'riga k\nPREVALIDATO · TXT_EVENTO',
     'atto k\n1 BOZZA', F1C),
    (PAG, '«VALIDA» del gemello k', 'sulla bozza prenotata, con lo stesso UC della '
     'prenotazione (GE-02)', 'R009 /validazione/evento', ATK, 'riga k\nVALIDATO',
     'atto k\n2 CONFERMATO', F1C),
    (PAG, 'Firma del dichiarante', 'solo cartacea, acquisita come processo verbale',
     'R006 cartacea', ATK, 'riga k\nVALIDATO', 'atto k\n4 FIRMATO DAL DICHIARANTE', F1C),
    (PAG, 'Attestazione di conformità', 'firmata dall’ufficiale', 'R007 /attestazione/firma',
     ATK, 'riga k\nVALIDATO', 'atto k\n11 FIRMATO PER CONFORMITÀ', F1C),
    (PAG, 'Firma dell’ufficiale', 'l’atto del gemello k è formato; fg_stesura_atto = 1',
     'R007 /firma_usc', ATK, 'riga k\nFIRMATO', 'atto k\n5 FIRMATO DA USC', F1C),
    (PAG, 'Definisci del gemello k', 'definizione in SIPO del solo atto k',
     '/finalizzaAtto', '2 DEFINITO\natto k', 'riga k\nFIRMATO', 'atto k\n5 FIRMATO DA USC', F1C),
    (PAG, 'GEMELLO SUCCESSIVO', 'si riparte dai documenti del gemello k+1',
     '/getNextATTONascitaGemello', ATK1, 'riga k+1\nPRENOTATO', 'atto k+1\n1 BOZZA', F1C),
    (PAG, 'Chiusura del parto', 'bozze non usate cancellate, numeri scartati',
     'R011 · PUT /scarta', '2 DEFINITO\ntutti gli atti', 'N righe FIRMATO\nnon usate: ANNULLATO',
     '5 FIRMATO DA USC\nnon usate: 9 CANCELLATO', F1D),
]
NOTA_1 = (
    'CASO 1 — TUTTI I GEMELLI CON LO STESSO UC (tutti nati vivi, tutti nati morti o tutti nati '
    'vivi e poi deceduti). La prenotazione accetta un solo idUsecase: tramite servizi cooperativi '
    'si passa l’UC specifico, e le bozze si completano con lo stesso UC (issue #571). Il numero '
    'dei gemelli è il totale, nati morti compresi (issue #611). Una riga dello store per gemello; '
    'le righe 2…N nascono a PRENOTA GEMELLI, insieme a ATTI_GEMELLARI e ANSC_SOGGETTO_ATTO.')

# ───────────────────────────────────────────── caso 2: UC diversi, web app e recupero
F2B, F2W, F2C, F2D = 'B — Verso la web app', 'Web app', 'C — Recupero', 'D — Definizione'
PASSI_2 = INIZIO + [
    (PAG, 'Riepilogo · UC diversi', 'PRENOTA GEMELLI non compare; il messaggio indica la '
     'web app; DATI PER ANSC', '', NATTI, '1 riga · gemello 1\nIN_LAVORAZIONE', NI, F2B),
    (PAG, 'DATI PER ANSC · numeri in blocco', 'N numeri consecutivi; N righe in ATTI_GEMELLARI',
     'be-numeratore-comunale\nPOST /richiesta', NATTI, 'N righe (2…N nuove)\nNUMERO_ATTO · '
     'ATTESA WEBAPP', NI, F2B),
    (PAG, 'Dati per ANSC del parto', 'per ciascun nato: posizione, numero, tipologia di '
     'nascita, dati e testo da riportare', '', NATTI, 'N righe\nATTESA WEBAPP', NI, F2B),
    (BAN, 'WEB APP ANSC — fuori da SIPO', 'prenotazione con N e i numeri di SIPO; ogni bozza '
     'completata con il caso d’uso di servizio e la tipologia di nascita; firme', '', NATTI,
     'N righe\nATTESA WEBAPP', 'N atti\n1 BOZZA → 5 FIRMATO DA USC', F2W),
    (PAG, 'RECUPERA GEMELLI (gemello 1)', 'R005 per ciascun numero comunale; abbinamento per '
     'numero e per intestatario', 'R005 /consultazione', NATTI, 'N righe\nID_ANSC · UC di '
     'servizio', 'N atti\n5 FIRMATO DA USC', F2C),
    (PAG, 'Esito del recupero', 'gemello per gemello: abbinato · non trovato · non firmato · '
     'incoerente; ANSC_SOGGETTO_ATTO', '', NATTI, 'abbinati: FIRMATO\naltri: ATTESA WEBAPP',
     'N atti\n5 FIRMATO DA USC', F2C),
    (PAG, 'DEFINISCI GEMELLI', 'solo se tutti abbinati; una /finalizzaAtto per gemello, come '
     'oggi', '/finalizzaAtto ×N', '2 DEFINITO\ntutti gli atti', 'N righe\nFIRMATO',
     '5 FIRMATO DA USC', F2D),
]
NOTA_2 = (
    'CASO 2 — GEMELLI CON UC DIVERSI (per esempio un nato vivo e un nato morto). La prenotazione '
    'ha un solo idUsecase e l’UC delle bozze non si cambia: ANSC indica il caso d’uso di servizio, '
    'specificando la tipologia di nascita nei dati generali (issue #3333), e quel caso d’uso dal '
    '9 settembre 2024 si usa solo sulla web app (#571, [A7]). La pratica resta completa in SIPO; i '
    'numeri si staccano in blocco da SIPO; il ritorno è un solo recupero per l’intero parto, che '
    'non importa dati ma aggancia ciascun atto ANSC al proprio gemello.')


def flussi():
    a = M.genera(
        PASSI_1, 'Parto plurimo — caso 1: gemelli con lo stesso UC, tutto da SIPO',
        'La pratica unica si divide in N atti; se gli UC dei nati coincidono, PRENOTA GEMELLI '
        'stacca i numeri e chiama la prenotazione con quell’UC; poi ciascun gemello percorre '
        'anteprima, validazione e firme sul proprio atto. Una riga dello store per gemello.',
        os.path.join(DIR, 'gem4_flusso_1.pptx'), nota=NOTA_1, colore_nota='blu',
        fasi_viola=(), etichetta_viola='ciclo per gemello',
        sottotitolo_niente='fino alla prenotazione')
    b = M.genera(
        PASSI_2, 'Parto plurimo — caso 2: gemelli con UC diversi, web app e recupero in SIPO',
        'Compilazione, divisione e numeri restano in SIPO; prenotazione, completamento con il caso '
        'd’uso di servizio e firme si fanno sulla web app; RECUPERA GEMELLI aggancia gli N atti in '
        'una volta e DEFINISCI GEMELLI li definisce in SIPO.',
        os.path.join(DIR, 'gem4_flusso_2.pptx'), nota=NOTA_2, colore_nota='blu',
        non_ritorno=False, fasi_viola=('Web app',), etichetta_viola='web app ANSC',
        sottotitolo_niente='finché non si va sulla web app')
    return a, b


# ───────────────────────────────────────────── panoramica: la scelta la fa il parto
CASO1_PANORAMICA = (
    ('PRENOTA GEMELLI',
     'N numeri; R009 /prenota/evento con l’UC comune: N atti in BOZZA e N idAnsc'),
    ('Per ciascun gemello k',
     'anteprima · VALIDA con lo stesso UC · firma cartacea del dichiarante · conformità · '
     'firma USC · Definisci'),
    ('Chiusura del parto', 'bozze non usate: R011 e numero scartato'))


PIEDE = (('In entrambi i casi: una riga di ANSC_STATO_ATTO, una di ATTI_GEMELLARI e una di '
          'ANSC_SOGGETTO_ATTO per ciascun gemello'),
         ('Nel caso 1 nascono alla prenotazione; nel caso 2 allo stacco dei numeri, e il '
          'legame con l’atto ANSC entra solo con il recupero'))


CASO2_PANORAMICA = (
    ('DATI PER ANSC', 'N numeri in blocco; i dati e lo stato di ciascun nato; ATTESA WEBAPP'),
    ('Web app ANSC', 'prenotazione con i numeri di SIPO; caso d’uso di servizio con la tipologia '
     'di nascita; firme'),
    ('RECUPERA GEMELLI · DEFINISCI GEMELLI',
     'R005 per numero, abbinamento per gemello, poi la definizione in SIPO'))


def panoramica(percorso=os.path.join(DIR, 'gem4_panoramica.pptx'), caso1=CASO1_PANORAMICA,
               piede=PIEDE, caso2=CASO2_PANORAMICA):
    W, H = 9.3, 6.75
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = B.rgb('ffffff')
    B.testo(sl, 0.25, 0.15, W - 0.5, 0.35, 'Parto plurimo: due casi, decisi dagli UC dei nati', 15,
            True, '1f3a5f', PP_ALIGN.CENTER)
    B.testo(sl, 0.6, 0.5, W - 1.2, 0.3, 'Stesso inizio in SIPO; dopo la divisione la scelta '
            'non è dell’operatore: dipende dallo stato di ciascun nato', 8.5, False, B.MUTED,
            PP_ALIGN.CENTER, corsivo=True)

    def box(x, y, w, h, col, tit, sub, forma=MSO_SHAPE.ROUNDED_RECTANGLE, trat=False):
        return B.riquadro(sl, x, y, w, h, col, [(tit, 9, True, None), (sub, 7, False, B.MUTED)],
                          forma=forma, tratteggio=trat)

    w3, y0 = 2.75, 0.95
    t1 = box(0.35, y0, w3, 0.7, 'blu', 'Compilazione della pratica unica',
             'tipo atto «gemelli»; R005 su genitori e dichiarante')
    t2 = box(3.27, y0, w3, 0.7, 'blu', 'Riepilogo → Conferma',
             'la pratica è divisa in N atti (/performAttiPlurigemellari)')
    t3 = box(6.19, y0, w3, 0.7, 'blu', 'UC di ciascun nato',
             'dai flag nato morto / morto prima della denuncia')
    B.freccia(sl, t1, 3, t2, 1)
    B.freccia(sl, t2, 3, t3, 1)
    B.riquadro(sl, 3.3, 1.95, 2.7, 0.85, 'giallo',
               [('Stesso UC', 9, True, None), ('per tutti i gemelli?', 7.5, False, None)],
               forma=MSO_SHAPE.DIAMOND)
    B.gomito(sl, [(7.56, y0 + 0.7), (7.56, 1.82), (4.65, 1.82), (4.65, 1.95)])

    xa, xb, wc = 0.35, 4.85, 4.1
    B.testo(sl, xa, 2.97, wc, 0.2, 'Caso 1 — tutto da SIPO', 10, True, '3f8f5f', PP_ALIGN.CENTER)
    B.testo(sl, xb, 2.97, wc, 0.2, 'Caso 2 — web app e recupero in SIPO', 10, True, '7b5aa6',
            PP_ALIGN.CENTER)
    a1, a2, a3 = (box(xa, y_, wc, 0.62, 'verde', tit, sub)
                  for y_, (tit, sub) in zip((3.25, 4.07, 4.89), caso1))
    b1 = box(xb, 3.25, wc, 0.62, 'viola', *caso2[0])
    b2 = box(xb, 4.07, wc, 0.62, 'viola', *caso2[1], trat=True)
    b3 = box(xb, 4.89, wc, 0.62, 'viola', *caso2[2])
    B.gomito(sl, [(3.3, 2.375), (0.6, 2.375), (0.6, 3.25)], colore='3f8f5f')
    B.gomito(sl, [(6.0, 2.375), (8.75, 2.375), (8.75, 3.25)], colore='7b5aa6')
    B.testo(sl, 2.75, 2.19, 0.5, 0.15, 'sì', 7.5, True, '3f8f5f')
    B.testo(sl, 6.15, 2.19, 0.5, 0.15, 'no', 7.5, True, '7b5aa6')
    for p, q in ((a1, a2), (a2, a3), (b1, b2), (b2, b3)):
        B.freccia(sl, p, 2, q, 0)
    B.riquadro(sl, 0.35, 5.75, W - 0.7, 0.7, 'blu',
               [(piede[0], 8, True, None), (piede[1], 7, False, B.MUTED)],
               forma=MSO_SHAPE.RECTANGLE)
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


# ───────────────────────────────────────────── ERD con ANSC_SOGGETTO_ATTO
RIGHE_SA = [
    ('PK', 'ID_SOGGETTO_ATTO'),
    ('FK', 'ID_ATTO_SIPO  → ANSC_STATO_ATTO'),
    ('', 'ID_NASCITA_SOGGETTO · ID_SOGGETTO'),
    ('UK', 'ID_ATTO_SIPO, COD_RUOLO'),
    ('', 'ID_ANSC_SOGGETTO'),
    ('', 'COD_ORIGINE · TS_ABBINAMENTO'),
]


def erd(percorso=os.path.join(DIR, 'gem4_erd.pptx'), righe_sa=RIGHE_SA, y_sa=6.3):
    W, H = 16.0, 8.9
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = B.rgb('ffffff')
    B.testo(sl, 0.3, 0.15, W - 0.6, 0.35, 'Parto plurimo: le righe di ANSC_STATO_ATTO e i loro '
            'legami', 15, True, '1b3a5c', PP_ALIGN.CENTER)
    B.testo(sl, 0.3, 0.5, W - 0.6, 0.25, 'Una riga per gemello; ATTI_GEMELLARI raggruppa il parto, '
            'ANSC_SOGGETTO_ATTO lega il nato al suo atto ANSC', 9.5, False, B.MUTED,
            PP_ALIGN.CENTER, corsivo=True)
    grigio, blu, verde = B.PAL['grigio'][0], B.PAL['blu'][0], B.PAL['verde'][0]

    for x, w, t, col in ((0.3, 6.6, 'MATR_USR — SIPO, stato civile', 'grigio'),
                         (7.2, 8.5, 'ANSC_USR — integrazione con ANSC', 'blu')):
        s = B.riquadro(sl, x, 0.9, w, 7.6, col, [('', 6, False, None)],
                       forma=MSO_SHAPE.RECTANGLE, tratteggio=True)
        s.fill.background()
        B.testo(sl, x + 0.1, 0.95, w - 0.2, 0.2, t, 9, True, B.PAL[col][0])

    atto = tabella(sl, 0.6, 1.35, 3.4, 'grigio', 'ATTO', [
        ('PK', 'ID_ATTO'),
        ('FK', 'ID_LAVORAZIONE_PADRE  → ATTO'),
        ('', 'NUMERO_ATTO · ANNO · PARTE · SERIE'),
        ('', 'ID_STATO_PRATICA'),
    ], nota='gemello 1 = atto della pratica (padre vuoto); gemelli 2…N puntano a lui')
    an = tabella(sl, 0.6, 3.6, 3.4, 'grigio', 'ATTO_NASCITA', [
        ('PK', 'ID_ATTO_NASCITA  = ATTO.ID_ATTO'),
        ('', 'FLG_PARTO_PLURIMO · N_TOT_GEMELLI'),
        ('', 'ID_SOGGETTO_DEFINITO'),
    ], nota='una per atto')
    ans = tabella(sl, 0.6, 5.3, 3.4, 'grigio', 'ATTO_NASCITA_SOGGETTO', [
        ('PK', 'ID'),
        ('FK', 'ID_ATTO_NASCITA  → ATTO_NASCITA'),
        ('', 'POS_GEMELLO · NOME · SESSO · DATA'),
        ('', 'FLG_NATO_MORTO · FLG_MORTO_PREDENUNCIA'),
        ('', 'ID_SOGGETTO_INTERESSATO'),
    ], nota='il nato e il suo stato; uno per atto dopo la divisione')
    sog = tabella(sl, 4.4, 6.75, 2.3, 'grigio', 'SOGGETTO', [
        ('PK', 'ID_SOGGETTO'),
    ], nota='del nato: solo dopo l’iscrizione ANPR')

    stato = tabella(sl, 7.6, 1.35, 3.9, 'blu', 'ANSC_STATO_ATTO', [
        ('PK', 'ID_ATTO_SIPO'),
        ('', 'ID_UC_ANSC · COD_LOGICA'),
        ('', 'NUMERO_ATTO · ID_ANSC'),
        ('', 'ID_STATO · STATO · COD_FASE'),
        ('', 'COD_PAGINA_RIPRESA · COD_MUNICIPIO'),
    ], nota='una riga per gemello')
    gem = tabella(sl, 7.6, 4.0, 3.9, 'verde', 'ATTI_GEMELLARI', [
        ('PK', 'id_atto_gemellare'),
        ('FK', 'id_atto_sipo  → ANSC_STATO_ATTO  (UK)'),
        ('', 'id_lavorazione_padre  (il parto)'),
        ('', 'id_richiesta_prenotazione · ty_use_case'),
        ('', 'nr_gemelli · nr_progressivo_gemello'),
        ('', 'fg_stesura_atto'),
        ('UK', 'id_lavorazione_padre, nr_progressivo'),
    ], nota='una riga per gemello; il parto = id_lavorazione_padre', nuova=True)
    sa = tabella(sl, 7.6, y_sa, 3.9, 'verde', 'ANSC_SOGGETTO_ATTO', righe_sa, nota='il soggetto e il suo atto ANSC; vale anche fuori dai gemelli', nuova=True)
    audit = tabella(sl, 12.4, 1.35, 3.0, 'blu', 'ANSC_LOG_AUDIT', [
        ('PK', 'ID_AUDIT'),
        ('FK', '→ ANSC_STATO_ATTO'),
        ('', 'FASE · RICHIESTA · RISPOSTA'),
    ], nota='prenotazione e recupero sulla riga del gemello 1')
    numer = tabella(sl, 12.4, 3.6, 3.0, 'blu', 'DATI_ATTO_ESTERNO', [
        ('PK', 'id_atto_esterno'),
        ('', 'nr_anno_atto · nr_atto_comunale'),
        ('', 'id_atto_sipo · id_ansc · stato'),
    ], nota='i numeri staccati in blocco')

    B.gomito(sl, [(0.6, 1.62), (0.42, 1.62), (0.42, 2.05), (0.6, 2.05)], colore=grigio)
    etichetta(sl, 0.0, 1.75, 'padre', grigio, w=0.45)
    lega(sl, an, 0, atto, 2, grigio)
    etichetta(sl, 2.35, 3.25, '1:1', grigio, w=0.5)
    lega(sl, ans, 0, an, 2, grigio)
    etichetta(sl, 2.35, 4.95, '1:N', grigio, w=0.5)
    B.gomito(sl, [(4.0, 6.0), (5.55, 6.0), (5.55, 6.75)], colore=grigio, tratteggio=True)
    etichetta(sl, 4.1, 6.05, 'ID_SOGGETTO_INTERESSATO', grigio, w=1.5)
    B.gomito(sl, [(7.6, 1.75), (4.0, 1.75)], colore=blu, tratteggio=True)
    etichetta(sl, 4.3, 1.52, 'ID_ATTO_SIPO per valore · 1:0..1', blu, w=2.6)
    lega(sl, gem, 0, stato, 2, verde, spessore=2.25)
    etichetta(sl, 9.6, 3.68, '1:1  FK', verde, w=0.8)
    B.gomito(sl, [(7.6, 4.5), (5.2, 4.5), (5.2, 2.15), (4.0, 2.15)], colore=verde, tratteggio=True)
    etichetta(sl, 5.3, 3.0, 'id_lavorazione_padre → ID_ATTO del gemello 1', verde, w=1.8)
    B.gomito(sl, [(7.6, 5.2), (4.75, 5.2), (4.75, 5.75), (4.0, 5.75)], colore=verde,
             tratteggio=True)
    etichetta(sl, 4.85, 4.95, 'nr_progressivo_gemello = POS_GEMELLO', verde, w=2.6)
    B.gomito(sl, [(11.5, 6.6), (11.95, 6.6), (11.95, 2.2), (11.5, 2.2)], colore=verde,
             spessore=2.25)
    etichetta(sl, 12.0, 4.9, 'FK · N:1', verde, w=0.8)
    B.gomito(sl, [(7.6, 6.85), (6.95, 6.85), (6.95, 6.35), (4.0, 6.35)], colore=verde,
             tratteggio=True)
    etichetta(sl, 4.9, 6.38, 'ID_NASCITA_SOGGETTO = ID', verde, w=1.9)
    B.gomito(sl, [(7.6, 7.3), (6.7, 7.3)], colore=verde, tratteggio=True)
    etichetta(sl, 6.6, 7.05, 'ID_SOGGETTO', verde, w=0.85)
    lega(sl, audit, 1, stato, 3, blu)
    etichetta(sl, 11.55, 1.45, '1:N', blu, w=0.6)
    B.gomito(sl, [(11.5, 2.5), (12.15, 2.5), (12.15, 4.0), (12.4, 4.0)], colore=blu,
             tratteggio=True)
    etichetta(sl, 12.2, 3.15, 'NUMERO_ATTO per valore', blu, w=1.5)

    y = 8.1
    for k, (col, t) in enumerate((('verde', 'tabella nuova'), ('blu', 'esistente in ANSC_USR'),
                                  ('grigio', 'esistente in MATR_USR'))):
        B.riquadro(sl, 7.6 + k * 2.2, y, 0.22, 0.14, col, [('', 6, False, None)],
                   forma=MSO_SHAPE.RECTANGLE)
        B.testo(sl, 7.88 + k * 2.2, y - 0.01, 1.9, 0.16, t, 8)
    B.testo(sl, 0.6, y - 0.01, 6.2, 0.18, 'linea piena = FK dichiarata · tratteggio = riferimento '
            'per valore (nessuna FK fra schemi)', 8, False, B.MUTED, corsivo=True)
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


if __name__ == '__main__':
    for p in (*flussi(), panoramica(), erd()):
        print('scritto:', os.path.relpath(p, QUI))
