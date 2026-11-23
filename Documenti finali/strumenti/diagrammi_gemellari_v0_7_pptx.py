# -*- coding: utf-8 -*-
"""I diagrammi dell'analisi delle nascite gemellari v0.7 (21/11/2026), in PowerPoint modificabile.

Decisione dell'utente (21/11/2026): ATTI_GEMELLARI (tabella di Side) NON si crea; le sue colonne
utili confluiscono in ANSC_SOGGETTO_ATTO, che riceve la chiave del parto ID_LAVORAZIONE_PADRE.
  * gem7_erd.pptx        — i legami senza ATTI_GEMELLARI;
  * gem7_panoramica.pptx — il piede dei due casi senza ATTI_GEMELLARI;
  * gem7_flusso_2.pptx   — caso 2: allo stacco dei numeri nessuna riga della tabella dei gemelli;
  * gem7_ripresa.pptx    — la ripresa legge ANSC_SOGGETTO_ATTO e ANSC_STATO_ATTO.
Il flusso del caso 1 resta gem5_flusso_1 (non nominava ATTI_GEMELLARI).

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v0_7_pptx.py
    qlmanage -t -s 2400 -o img/gemellari img/gemellari/gem7_*.pptx
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.util import Inches, Pt

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagramma_workflow_pptx as B             # noqa: E402
import diagrammi_matrimonio_pptx as M           # noqa: E402
import diagrammi_gemellari_v0_4_pptx as G4      # noqa: E402
import diagrammi_gemellari_v0_5_pptx as G5      # noqa: E402
from diagramma_annotazioni_erd_pptx import etichetta, lega, tabella   # noqa: E402

DIR = G4.DIR


def fk(sl, x1, y1, x2, y2, colore):
    """Chiave esterna dritta, con la punta sul padre (x2, y2)."""
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2),
                                Inches(y2))
    c.line.color.rgb = B.rgb(colore)
    c.line.width = Pt(2.25)
    B._punta(c)
    return c


def erd(percorso=os.path.join(DIR, 'gem7_erd.pptx')):
    W, H = 16.0, 8.9
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = B.rgb('ffffff')
    B.testo(sl, 0.3, 0.15, W - 0.6, 0.35, 'Parto plurimo: le righe di ANSC_STATO_ATTO e i loro '
            'legami', 15, True, '1b3a5c', PP_ALIGN.CENTER)
    B.testo(sl, 0.3, 0.5, W - 0.6, 0.25, 'Una riga per gemello nello store; ANSC_SOGGETTO_ATTO '
            'lega il nato al suo atto ANSC e raggruppa il parto', 9.5, False, B.MUTED,
            PP_ALIGN.CENTER, corsivo=True)
    grigio, blu, verde = B.PAL['grigio'][0], B.PAL['blu'][0], B.PAL['verde'][0]
    for x, w, t, col in ((0.3, 6.6, 'MATR_USR — SIPO, stato civile', 'grigio'),
                         (7.2, 8.5, 'ANSC_USR — integrazione con ANSC', 'blu')):
        s = B.riquadro(sl, x, 0.9, w, 7.6, col, [('', 6, False, None)],
                       forma=MSO_SHAPE.RECTANGLE, tratteggio=True)
        s.fill.background()
        B.testo(sl, x + 0.1, 0.95, w - 0.2, 0.2, t, 9, True, B.PAL[col][0])

    atto = tabella(sl, 0.6, 1.35, 3.4, 'grigio', 'ATTO', [
        ('PK', 'ID_ATTO'), ('FK', 'ID_LAVORAZIONE_PADRE  → ATTO'),
        ('', 'NUMERO_ATTO · ANNO · PARTE · SERIE'), ('', 'ID_STATO_PRATICA'),
    ], nota='gemello 1 = atto della pratica (padre vuoto); gemelli 2…N puntano a lui')
    an = tabella(sl, 0.6, 3.6, 3.4, 'grigio', 'ATTO_NASCITA', [
        ('PK', 'ID_ATTO_NASCITA  = ATTO.ID_ATTO'), ('', 'FLG_PARTO_PLURIMO · N_TOT_GEMELLI'),
        ('', 'ID_SOGGETTO_DEFINITO'),
    ], nota='una per atto')
    ans = tabella(sl, 0.6, 5.3, 3.4, 'grigio', 'ATTO_NASCITA_SOGGETTO', [
        ('PK', 'ID'), ('FK', 'ID_ATTO_NASCITA  → ATTO_NASCITA'),
        ('', 'POS_GEMELLO · NOME · SESSO · DATA'), ('', 'FLG_NATO_MORTO · FLG_MORTO_PREDENUNCIA'),
        ('', 'ID_SOGGETTO_INTERESSATO'),
    ], nota='il nato e il suo stato; uno per atto dopo la divisione')
    tabella(sl, 4.4, 6.75, 2.3, 'grigio', 'SOGGETTO', [('PK', 'ID_SOGGETTO')],
            nota='del nato: solo dopo l’iscrizione ANPR')

    stato = tabella(sl, 7.6, 1.35, 3.9, 'blu', 'ANSC_STATO_ATTO', [
        ('PK', 'ID_ATTO_SIPO'), ('', 'ID_UC_ANSC · COD_LOGICA'), ('', 'NUMERO_ATTO · ID_ANSC'),
        ('', 'ID_STATO · STATO · COD_FASE'), ('', 'COD_PAGINA_RIPRESA · COD_MUNICIPIO'),
    ], nota='una riga per gemello')
    tabella(sl, 7.6, 4.0, 4.3, 'verde', 'ANSC_SOGGETTO_ATTO', [
        ('PK', 'ID_SOGGETTO_ATTO'),
        ('FK', 'ID_ATTO_SIPO  → ANSC_STATO_ATTO'),
        ('FK', 'ID_LAVORAZIONE_PADRE  → ANSC_STATO_ATTO (gemello 1)'),
        ('', 'ID_ANSC · ID_UC_ANSC  (copie dello store)'),
        ('', 'ID_NASCITA_SOGGETTO · ID_SOGGETTO · ID_ANSC_SOGGETTO'),
        ('UK', 'ID_ATTO_SIPO, COD_RUOLO'),
        ('UK', 'ID_LAVORAZIONE_PADRE, NUM_PROGRESSIVO_GEMELLO'),
        ('', 'NUM_PROGRESSIVO_GEMELLO · ID_TIPO_NASCITA'),
        ('', 'ID_ANSC_GEMELLO_PREC · ID_ANSC_GEMELLO_SUCC'),
        ('', 'COD_ORIGINE · TS_ABBINAMENTO'),
    ], nota='il nato, il suo atto ANSC e il parto; vale anche fuori dai gemelli', nuova=True)
    audit = tabella(sl, 12.4, 1.35, 3.0, 'blu', 'ANSC_LOG_AUDIT', [
        ('PK', 'ID_AUDIT'), ('FK', '→ ANSC_STATO_ATTO'), ('', 'FASE · RICHIESTA · RISPOSTA'),
    ], nota='prenotazione e recupero sulla riga del gemello 1')
    tabella(sl, 12.4, 3.6, 3.0, 'blu', 'DATI_ATTO_ESTERNO', [
        ('PK', 'id_atto_esterno'), ('', 'nr_anno_atto · nr_atto_comunale'),
        ('', 'id_atto_sipo · id_ansc · stato'),
    ], nota='i numeri staccati in blocco')

    # MATR_USR
    B.gomito(sl, [(0.6, 1.62), (0.42, 1.62), (0.42, 2.05), (0.6, 2.05)], colore=grigio)
    etichetta(sl, 0.0, 1.75, 'padre', grigio, w=0.45)
    lega(sl, an, 0, atto, 2, grigio)
    etichetta(sl, 2.35, 3.25, '1:1', grigio, w=0.5)
    lega(sl, ans, 0, an, 2, grigio)
    etichetta(sl, 2.35, 4.95, '1:N', grigio, w=0.5)
    B.gomito(sl, [(4.0, 6.0), (5.55, 6.0), (5.55, 6.75)], colore=grigio, tratteggio=True)
    etichetta(sl, 4.1, 6.05, 'ID_SOGGETTO_INTERESSATO', grigio, w=1.5)
    # SIPO → ANSC_USR, per valore
    B.gomito(sl, [(7.6, 1.75), (4.0, 1.75)], colore=blu, tratteggio=True)
    etichetta(sl, 4.3, 1.52, 'ID_ATTO_SIPO per valore · 1:0..1', blu, w=2.6)
    B.gomito(sl, [(4.0, 2.15), (5.2, 2.15), (5.2, 4.45), (7.6, 4.45)], colore=verde,
             tratteggio=True)
    etichetta(sl, 5.25, 4.0, 'ID_LAVORAZIONE_PADRE = ID_ATTO del gemello 1', verde, w=1.85)
    B.gomito(sl, [(4.0, 5.6), (6.6, 5.6), (6.6, 5.0), (7.6, 5.0)], colore=verde, tratteggio=True)
    etichetta(sl, 4.1, 5.35, 'ID_NASCITA_SOGGETTO = ID · progressivo = POS_GEMELLO', verde, w=2.5)
    B.gomito(sl, [(6.7, 7.0), (7.3, 7.0), (7.3, 5.75), (7.6, 5.75)], colore=verde,
             tratteggio=True)
    etichetta(sl, 6.75, 7.05, 'ID_SOGGETTO', verde, w=0.85)
    # FK dentro ANSC_USR
    fk(sl, 8.6, 4.0, 8.6, 2.58, verde)
    etichetta(sl, 8.7, 3.1, 'ID_ATTO_SIPO · FK · N:1', verde, w=1.5)
    fk(sl, 11.0, 4.0, 11.0, 2.58, verde)
    etichetta(sl, 9.5, 3.5, 'ID_LAVORAZIONE_PADRE · FK · il parto', verde, w=1.45)
    lega(sl, audit, 1, stato, 3, blu)
    etichetta(sl, 11.55, 1.45, '1:N', blu, w=0.6)
    B.gomito(sl, [(11.5, 2.4), (12.15, 2.4), (12.15, 4.0), (12.4, 4.0)], colore=blu,
             tratteggio=True)
    etichetta(sl, 12.2, 3.0, 'NUMERO_ATTO per valore', blu, w=1.5)

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


def panoramica():
    return G4.panoramica(os.path.join(DIR, 'gem7_panoramica.pptx'), caso1=(
        ('Riepilogo dei gemelli', 'per ciascun nato UC comune e numero comunale previsto, non '
         'riservato'),
        ('DEFINISCI', 'N numeri e R009 /prenota/evento; poi per ciascun gemello anteprima e '
         'VALIDA · firma del dichiarante · conformità · firma USC · definizione in SIPO'),
        ('Esito del parto · ripresa', 'tutti formati e definiti; se interrotto, RIPRENDI dal '
         'riepilogo senza nuovi numeri')),
        piede=('In entrambi i casi: una riga di ANSC_STATO_ATTO e una di ANSC_SOGGETTO_ATTO per '
               'ciascun gemello',
               'Nel caso 1 la riga del nato nasce alla prenotazione; nel caso 2 al recupero, quando '
               'l’atto formato sulla web app si abbina al gemello'))


def flusso_2():
    passi = []
    for t in G4.PASSI_2:
        if t[1] == 'Riepilogo · UC diversi':
            t = (t[0], t[1], 'riepilogo dei gemelli: DEFINISCI non compare; il messaggio indica '
                 'la web app; DATI PER ANSC') + t[3:]
        elif t[1] == 'DATI PER ANSC · numeri in blocco':
            t = (t[0], t[1], 'N numeri consecutivi; il parto resta raggruppato in SIPO') + t[3:]
        elif t[1] == 'Esito del recupero':
            t = (t[0], t[1], 'gemello per gemello: abbinato · non trovato · non firmato · '
                 'incoerente; riga del nato in ANSC_SOGGETTO_ATTO') + t[3:]
        passi.append(t)
    return M.genera(
        passi, 'Parto plurimo — caso 2: gemelli con UC diversi, web app e recupero in SIPO',
        'Compilazione, divisione e numeri restano in SIPO; prenotazione, completamento con il caso '
        'd’uso di servizio e firme si fanno sulla web app; RECUPERA GEMELLI aggancia gli N atti in '
        'una volta e DEFINISCI GEMELLI li definisce in SIPO.',
        os.path.join(DIR, 'gem7_flusso_2.pptx'), nota=G4.NOTA_2, colore_nota='blu',
        non_ritorno=False, fasi_viola=('Web app',), etichetta_viola='web app ANSC',
        sottotitolo_niente='finché non si va sulla web app')


def ripresa():
    return G5.ripresa(os.path.join(DIR, 'gem7_ripresa.pptx'),
                      righe_parto='le righe del parto: ANSC_SOGGETTO_ATTO e ANSC_STATO_ATTO')


if __name__ == '__main__':
    for p in (erd(), panoramica(), flusso_2(), ripresa()):
        print('scritto:', os.path.relpath(p, QUI))
