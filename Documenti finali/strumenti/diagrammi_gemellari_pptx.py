# -*- coding: utf-8 -*-
"""I diagrammi dell'analisi delle nascite gemellari (v0.2, 19/11/2026), in PowerPoint con forme e
connettori nativi: modificabili dall'utente come quelli del workflow e del matrimonio.

  * gem_panoramica.pptx  — i due percorsi, con lo stesso inizio in SIPO (Figura «I due percorsi»);
  * gem_flusso_a.pptx    — percorso A, tutto da SIPO, a cinque corsie (pagina · servizio · stato
                           SIPO · store ANSC_STATO_ATTO · stato ANSC), con le righe dello store
                           gemello per gemello;
  * gem_flusso_b.pptx    — percorso B, web app e ritorno in SIPO, stesse corsie;
  * gem_erd.pptx         — come si legano le righe: ATTO e i dati di nascita in MATR_USR,
                           ANSC_STATO_ATTO e ATTI_GEMELLARI in ANSC_USR.

Le corsie dei flussi riusano `diagrammi_matrimonio_pptx.genera`, le tabelle dell'ERD le primitive
di `diagramma_annotazioni_erd_pptx`. Le PNG per il .docx si ottengono con
    qlmanage -t -s 2400 -o img/gemellari img/gemellari/<nome>.pptx

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_pptx.py
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

# ───────────────────────────────────────────── percorso A: tutto da SIPO
FA, FB, FC, FD = ('A — Pratica unica', 'B — Prenotazione', 'C — Gemello k', 'D — Chiusura')
PRAT, NATTI = '1 IN LAVORAZIONE\nla sola pratica', '1 IN LAVORAZIONE\nN atti'
ATK, ATK1 = '1 IN LAVORAZIONE\natto k', '1 IN LAVORAZIONE\natto k+1'

PASSI_A = [
    (PAG, 'Compilazione della pratica', 'tipo atto «gemelli»: genitori, dichiarante, N nati '
     'con i due flag', '', PRAT, '—', NI, FA),
    (PAG, 'Genitori e dichiarante in ANSC', 'nasce la riga dell’atto della pratica, che sarà '
     'il gemello 1', 'R005 /consultazione', PRAT, '1 riga · gemello 1\nIN_LAVORAZIONE', NI, FA),
    (PAG, 'Riepilogo → Conferma', 'la pratica è divisa in N atti legati da '
     'ID_LAVORAZIONE_PADRE; lo store non cambia', '/performAttiPlurigemellari', NATTI,
     '1 riga · gemello 1\nIN_LAVORAZIONE', NI, FA),
    (PAG, 'PRENOTA GEMELLI · UC e numeri', 'UC di ciascun nato dai suoi flag; N numeri '
     'consecutivi', 'be-numeratore-comunale\nPOST /richiesta', NATTI,
     'N righe (2…N nuove)\nUC · NUMERO_ATTO', NI, FB),
    (PAG, 'PRENOTA GEMELLI · prenotazione', 'una chiamata per il parto; N righe in '
     'ATTI_GEMELLARI', 'R009 /prenota/evento', NATTI, 'N righe\nPRENOTATO · ID_ANSC',
     'N atti\n1 BOZZA', FB),
    (BAN, 'PER CIASCUN GEMELLO k = 1 … N', 'in ordine di nascita: POS_GEMELLO = '
     'progressivoGemello', '', '', '', '', FC),
    (PAG, 'Documenti del gemello k', 'certificato medico se nato morto o nato vivo e poi '
     'deceduto', 'R001 · preverifica', ATK, 'riga k\nDOCUMENTI_ACQUISITI', 'atto k\n1 BOZZA', FC),
    (PAG, 'Anteprima del gemello k', 'modello evento con i campi gemellari e gli idAnsc dei '
     'fratelli', 'all-ansc-sipo', ATK, 'riga k\nPREVALIDATO · TXT_EVENTO', 'atto k\n1 BOZZA', FC),
    (PAG, '«VALIDA» del gemello k', 'sulla bozza prenotata: id e idAnsc nel modello evento '
     '(GE-02)', 'R009 /validazione/evento', ATK, 'riga k\nVALIDATO', 'atto k\n2 CONFERMATO', FC),
    (PAG, 'Firma del dichiarante', 'solo cartacea, acquisita come processo verbale',
     'R006 cartacea', ATK, 'riga k\nVALIDATO', 'atto k\n4 FIRMATO DAL DICHIARANTE', FC),
    (PAG, 'Attestazione di conformità', 'firmata dall’ufficiale', 'R007 /attestazione/firma',
     ATK, 'riga k\nVALIDATO', 'atto k\n11 FIRMATO PER CONFORMITÀ', FC),
    (PAG, 'Firma dell’ufficiale', 'l’atto del gemello k è formato; fg_stesura_atto = 1',
     'R007 /firma_usc', ATK, 'riga k\nFIRMATO', 'atto k\n5 FIRMATO DA USC', FC),
    (PAG, 'Definisci del gemello k', 'definizione in SIPO del solo atto k',
     'salvataggio in SIPO', '2 DEFINITO\natto k', 'riga k\nFIRMATO', 'atto k\n5 FIRMATO DA USC',
     FC),
    (PAG, 'GEMELLO SUCCESSIVO', 'si riparte dai documenti del gemello k+1',
     '/getNextATTONascitaGemello', ATK1, 'riga k+1\nPRENOTATO', 'atto k+1\n1 BOZZA', FC),
    (PAG, 'Chiusura del parto', 'bozze non usate cancellate, numeri scartati',
     'R011 · PUT /scarta', '2 DEFINITO\ntutti gli atti', 'N righe FIRMATO\nnon usate: ANNULLATO',
     '5 FIRMATO DA USC\nnon usate: 9 CANCELLATO', FD),
]

NOTA_A = (
    'UNA RIGA PER GEMELLO. La chiave di ANSC_STATO_ATTO è l’atto di SIPO (ID_ATTO_SIPO) e la '
    'divisione crea un atto per nato: le righe sono N. Prima della divisione ne esiste una sola, '
    'quella dell’atto della pratica, che diventa il gemello 1 (ID_LAVORAZIONE_PADRE vuoto; gli '
    'altri atti puntano a lui). Le righe 2…N si inseriscono al passo PRENOTA GEMELLI, nella '
    'stessa transazione che registra i numeri e la prenotazione; da lì ogni riga ha la sua vita, '
    'e dalla banda «Per ciascun gemello» la corsia dello store mostra la sola riga del gemello '
    'in lavorazione.')

# ───────────────────────────────────────────── percorso B: web app e ritorno in SIPO
GB, GW, GC, GD = ('B — Verso la web app', 'Web app', 'C — Ritorno in SIPO', 'D — Chiusura')
PASSI_B = PASSI_A[:3] + [
    (PAG, 'Numeri comunali in blocco', 'N numeri consecutivi, uno per gemello',
     'be-numeratore-comunale\nPOST /richiesta', NATTI, 'N righe (2…N nuove)\nNUMERO_ATTO',
     NI, GB),
    (PAG, 'Dati per ANSC', 'i dati di ciascun gemello da riportare; N righe in ATTI_GEMELLARI',
     '', NATTI, 'N righe\nATTESA WEBAPP', NI, GB),
    (BAN, 'WEB APP ANSC — fuori da SIPO', 'prenotazione con i numeri staccati; completamento e '
     'firme gemello per gemello [A3]', '', NATTI, 'N righe\nATTESA WEBAPP',
     'N atti\n1 BOZZA → 5 FIRMATO DA USC', GW),
    (PAG, 'DEFINISCI del gemello k', 'aggancio all’atto ANSC per numero comunale o idAnsc; '
     'verifica dell’abbinamento', 'R005 /consultazione', '2 DEFINITO\natto k',
     'riga k\nFIRMATO · ID_ANSC', 'atto k\n5 FIRMATO DA USC', GC),
    (PAG, 'GEMELLO SUCCESSIVO', 'stesso aggancio per il gemello k+1',
     '/getNextATTONascitaGemello', ATK1, 'riga k+1\nATTESA WEBAPP', 'atto k+1\n5 FIRMATO DA USC',
     GC),
    (PAG, 'Chiusura del parto', 'un gemello non agganciato resta in ATTESA WEBAPP e compare '
     'nella supervisione', '', '2 DEFINITO\ntutti gli atti', 'N righe\nFIRMATO',
     '5 FIRMATO DA USC', GD),
]

NOTA_B = (
    'Le righe dello store sono le stesse del percorso A — una per gemello, inserite quando si '
    'staccano i numeri — ma l’identificativo nazionale vi entra solo al ritorno, con l’aggancio: '
    'prima di DEFINISCI SIPO non sa che cosa sia avvenuto sulla web app. La prenotazione non è '
    'chiamata da SIPO, quindi ATTI_GEMELLARI raggruppa i gemelli per pratica '
    '(id_lavorazione_padre) e id_richiesta_prenotazione resta vuoto.')


def flussi():
    a = M.genera(
        PASSI_A, 'Parto plurimo — percorso A: tutto da SIPO',
        'La pratica unica si divide in N atti; PRENOTA GEMELLI stacca i numeri e chiama la '
        'prenotazione; poi ciascun gemello percorre anteprima, validazione e firme sul proprio '
        'atto, fino all’ultimo. Lo store ANSC_STATO_ATTO ha una riga per gemello.',
        os.path.join(DIR, 'gem_flusso_a.pptx'), nota=NOTA_A, colore_nota='blu',
        fasi_viola=(), etichetta_viola='ciclo per gemello', sottotitolo_niente='fino alla prenotazione')
    b = M.genera(
        PASSI_B, 'Parto plurimo — percorso B: la web app e il ritorno in SIPO',
        'Compilazione, divisione e numeri restano in SIPO; prenotazione, completamento e firme si '
        'fanno sulla web app; ciascun atto torna in SIPO con DEFINISCI, che lo aggancia all’atto '
        'ANSC.', os.path.join(DIR, 'gem_flusso_b.pptx'), nota=NOTA_B, colore_nota='blu',
        non_ritorno=False, fasi_viola=('Web app',), etichetta_viola='web app ANSC',
        sottotitolo_niente='finché non si va sulla web app')
    return a, b


# ───────────────────────────────────────────── panoramica dei due percorsi
def panoramica(percorso=os.path.join(DIR, 'gem_panoramica.pptx')):
    W, H = 9.3, 6.6
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = B.rgb('ffffff')
    B.testo(sl, 0.25, 0.15, W - 0.5, 0.35, 'Parto plurimo: i due percorsi di integrazione', 15,
            True, '1f3a5f', PP_ALIGN.CENTER)
    B.testo(sl, 0.6, 0.5, W - 1.2, 0.3, 'Stesso inizio in SIPO; A se Sogei conferma il '
            'completamento delle bozze da gestionale (GE-01), B altrimenti', 8.5, False, B.MUTED,
            PP_ALIGN.CENTER, corsivo=True)

    def box(x, y, w, h, col, tit, sub, forma=MSO_SHAPE.ROUNDED_RECTANGLE, trat=False):
        return B.riquadro(sl, x, y, w, h, col, [(tit, 9, True, None), (sub, 7, False, B.MUTED)],
                          forma=forma, tratteggio=trat)

    w3, y0 = 2.75, 0.95
    t1 = box(0.35, y0, w3, 0.7, 'blu', 'Compilazione della pratica unica',
             'tipo atto «gemelli»; R005 su genitori e dichiarante')
    t2 = box(3.27, y0, w3, 0.7, 'blu', 'Riepilogo → Conferma',
             'la pratica è divisa in N atti (/performAttiPlurigemellari)')
    t3 = box(6.19, y0, w3 - 0.0, 0.7, 'blu', 'Numeri comunali in blocco',
             'be-numeratore-comunale: N numeri consecutivi')
    B.freccia(sl, t1, 3, t2, 1)
    B.freccia(sl, t2, 3, t3, 1)
    d = B.riquadro(sl, 3.45, 1.95, 2.4, 0.8, 'giallo',
                   [('GE-01', 9, True, None), ('completamento da gestionale?', 7.5, False, None)],
                   forma=MSO_SHAPE.DIAMOND)
    B.gomito(sl, [(7.56, y0 + 0.7), (7.56, 1.82), (4.65, 1.82), (4.65, 1.95)])

    xa, xb, wc = 0.35, 4.85, 4.1
    B.testo(sl, xa, 2.95, wc, 0.2, 'A — tutto da SIPO (riferimento)', 10, True, '3f8f5f',
            PP_ALIGN.CENTER)
    B.testo(sl, xb, 2.95, wc, 0.2, 'B — web app e ritorno in SIPO (ripiego)', 10, True, '7b5aa6',
            PP_ALIGN.CENTER)
    a1 = box(xa, 3.25, wc, 0.62, 'verde', 'PRENOTA GEMELLI',
             'R009 /prenota/evento: N atti in BOZZA e N idAnsc')
    a2 = box(xa, 4.07, wc, 0.62, 'verde', 'Per ciascun gemello k',
             'anteprima · VALIDA · firma cartacea del dichiarante · conformità · firma USC · '
             'Definisci')
    a3 = box(xa, 4.89, wc, 0.62, 'verde', 'Chiusura del parto',
             'bozze non usate: R011 e numero scartato')
    b1 = box(xb, 3.25, wc, 0.62, 'viola', 'Dati per ANSC',
             'i dati di ciascun gemello; le righe vanno in ATTESA WEBAPP')
    b2 = box(xb, 4.07, wc, 0.62, 'viola', 'Web app ANSC',
             'prenotazione, completamento e firme, gemello per gemello', trat=True)
    b3 = box(xb, 4.89, wc, 0.62, 'viola', 'DEFINISCI del gemello k',
             'aggancio all’atto ANSC (R005) e definizione in SIPO')
    B.gomito(sl, [(3.45, 2.35), (0.6, 2.35), (0.6, 3.25)], colore='3f8f5f')
    B.gomito(sl, [(5.85, 2.35), (8.75, 2.35), (8.75, 3.25)], colore='7b5aa6')
    B.testo(sl, 2.9, 2.17, 0.5, 0.15, 'sì', 7.5, True, '3f8f5f')
    B.testo(sl, 6.0, 2.17, 0.5, 0.15, 'no', 7.5, True, '7b5aa6')
    for p, q in ((a1, a2), (a2, a3), (b1, b2), (b2, b3)):
        B.freccia(sl, p, 2, q, 0)
    B.riquadro(sl, 0.35, 5.75, W - 0.7, 0.55, 'blu',
               [('In entrambi i percorsi: una riga di ANSC_STATO_ATTO e una di ATTI_GEMELLARI '
                 'per ciascun gemello, raggruppate dalla pratica di origine', 8, True, None)],
               forma=MSO_SHAPE.RECTANGLE)
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


# ───────────────────────────────────────────── ERD: come si legano le righe
def erd(percorso=os.path.join(DIR, 'gem_erd.pptx')):
    W, H = 16.0, 8.4
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = B.rgb('ffffff')
    B.testo(sl, 0.3, 0.15, W - 0.6, 0.35, 'Parto plurimo: le righe di ANSC_STATO_ATTO e i loro '
            'legami', 15, True, '1b3a5c', PP_ALIGN.CENTER)
    B.testo(sl, 0.3, 0.5, W - 0.6, 0.25, 'Una riga per gemello, perché una riga per atto di SIPO; '
            'il parto le raggruppa attraverso ATTI_GEMELLARI', 9.5, False, B.MUTED,
            PP_ALIGN.CENTER, corsivo=True)
    grigio, blu, verde = B.PAL['grigio'][0], B.PAL['blu'][0], B.PAL['verde'][0]

    # bande di schema
    for x, w, t, col in ((0.3, 6.6, 'MATR_USR — SIPO, stato civile', 'grigio'),
                         (7.2, 8.5, 'ANSC_USR — integrazione con ANSC', 'blu')):
        s = B.riquadro(sl, x, 0.9, w, 7.1, col, [('', 6, False, None)],
                       forma=MSO_SHAPE.RECTANGLE, tratteggio=True)
        s.fill.background()
        B.testo(sl, x + 0.1, 0.95, w - 0.2, 0.2, t, 9, True, B.PAL[col][0])

    atto = tabella(sl, 0.6, 1.35, 3.4, 'grigio', 'ATTO', [
        ('PK', 'ID_ATTO'),
        ('FK', 'ID_LAVORAZIONE_PADRE  → ATTO'),
        ('', 'NUMERO_ATTO · ANNO · PARTE · SERIE'),
        ('', 'ID_STATO_PRATICA'),
    ], nota='gemello 1 = atto della pratica (padre vuoto); gemelli 2…N puntano a lui')
    an = tabella(sl, 0.6, 3.75, 3.4, 'grigio', 'ATTO_NASCITA', [
        ('PK', 'ID_ATTO_NASCITA  = ATTO.ID_ATTO'),
        ('', 'FLG_PARTO_PLURIMO'),
        ('', 'N_TOT_GEMELLI'),
    ], nota='una per atto')
    ans = tabella(sl, 0.6, 5.65, 3.4, 'grigio', 'ATTO_NASCITA_SOGGETTO', [
        ('PK', 'ID'),
        ('FK', 'ID_ATTO_NASCITA  → ATTO_NASCITA'),
        ('', 'POS_GEMELLO'),
        ('', 'FLG_NATO_MORTO · FLG_MORTO_PREDENUNCIA'),
    ], nota='il nato e il suo stato')

    stato = tabella(sl, 7.6, 1.35, 3.9, 'blu', 'ANSC_STATO_ATTO', [
        ('PK', 'ID_ATTO_SIPO'),
        ('', 'ID_UC_ANSC · COD_LOGICA'),
        ('', 'NUMERO_ATTO · ID_ANSC'),
        ('', 'ID_STATO · STATO · COD_FASE'),
        ('', 'TXT_EVENTO · NUM_REVISIONE'),
        ('', 'COD_PAGINA_RIPRESA · COD_MUNICIPIO'),
    ], nota='una riga per gemello')
    gem = tabella(sl, 7.6, 4.45, 3.9, 'verde', 'ATTI_GEMELLARI', [
        ('PK', 'id_atto_gemellare'),
        ('FK', 'id_atto_sipo  → ANSC_STATO_ATTO  (UK)'),
        ('', 'id_lavorazione_padre  (il parto)'),
        ('', 'id_richiesta_prenotazione'),
        ('', 'ty_use_case · nr_gemelli'),
        ('', 'nr_progressivo_gemello'),
        ('', 'fg_stesura_atto'),
        ('UK', 'id_lavorazione_padre, nr_progressivo'),
    ], nota='una riga per gemello; il parto = id_lavorazione_padre', nuova=True)
    audit = tabella(sl, 12.4, 1.35, 3.0, 'blu', 'ANSC_LOG_AUDIT', [
        ('PK', 'ID_AUDIT'),
        ('FK', '→ ANSC_STATO_ATTO'),
        ('', 'FASE · RICHIESTA · RISPOSTA'),
    ], nota='la prenotazione si registra sulla riga del gemello 1')
    numer = tabella(sl, 12.4, 3.6, 3.0, 'blu', 'DATI_ATTO_ESTERNO', [
        ('PK', 'id_atto_esterno'),
        ('', 'nr_anno_atto · nr_atto_comunale'),
        ('', 'id_atto_sipo · id_ansc · stato'),
    ], nota='i numeri staccati in blocco')

    B.gomito(sl, [(0.6, 1.62), (0.42, 1.62), (0.42, 2.05), (0.6, 2.05)], colore=grigio)  # autorelazione
    etichetta(sl, 0.0, 1.75, 'padre', grigio, w=0.45)
    lega(sl, an, 0, atto, 2, grigio)
    etichetta(sl, 2.35, 3.35, '1:1', grigio, w=0.5)
    lega(sl, ans, 0, an, 2, grigio)
    etichetta(sl, 2.35, 5.3, '1:N', grigio, w=0.5)
    B.gomito(sl, [(7.6, 1.75), (4.0, 1.75)], colore=blu, tratteggio=True)
    etichetta(sl, 4.3, 1.52, 'ID_ATTO_SIPO per valore · 1:0..1', blu, w=2.6)
    lega(sl, gem, 0, stato, 2, verde, spessore=2.25)
    etichetta(sl, 9.6, 4.1, '1:1  FK', verde, w=0.8)
    B.gomito(sl, [(7.6, 4.95), (5.2, 4.95), (5.2, 2.15), (4.0, 2.15)], colore=verde, tratteggio=True)
    etichetta(sl, 5.3, 3.3, 'id_lavorazione_padre → ID_ATTO del gemello 1', verde, w=2.2)
    B.gomito(sl, [(7.6, 5.75), (4.6, 5.75), (4.6, 6.25), (4.0, 6.25)], colore=verde, tratteggio=True)
    etichetta(sl, 4.7, 5.5, 'nr_progressivo_gemello = POS_GEMELLO', verde, w=2.8)
    lega(sl, audit, 1, stato, 3, blu)
    etichetta(sl, 11.55, 1.55, '1:N', blu, w=0.6)
    B.gomito(sl, [(11.5, 2.5), (11.95, 2.5), (11.95, 4.0), (12.4, 4.0)], colore=blu, tratteggio=True)
    etichetta(sl, 10.4, 3.2, 'NUMERO_ATTO per valore', blu, w=1.5)

    y = 7.55
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
