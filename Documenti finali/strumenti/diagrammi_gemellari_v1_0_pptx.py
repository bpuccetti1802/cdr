# -*- coding: utf-8 -*-
"""Figure dell'analisi delle nascite gemellari v1.0 (22/11/2026).

1. Tre diagrammi nativi e modificabili in PowerPoint (img/gemellari/gem10_*.pptx + PNG):
   - gem10_navigazione: le pagine, le modali e le transizioni fra loro;
   - gem10_stati_1: gli stati della card nel caso 1 (ANSC_11 · COD_FASE · stato SIPO);
   - gem10_stati_2: gli stati della card nel caso 2.
2. I ritagli delle slide di PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.4.pptx (mockup e modali),
   senza titolo e senza note: img/gemellari/gem10_s*.png.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v1_0_pptx.py
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from proposta_gemellari_pagina_pptx import (box, txt, freccia, ROSSO, ROSSO_F, INK,  # noqa: E402
                                            MUTED, GRIGIO, GRIGIO_F, VERDE, VERDE_F, BLU,
                                            BLU_F, GIALLO, GIALLO_F, BIANCO)
import proposta_gemellari_pagina_v0_4_pptx as P4                    # noqa: E402

IMG = os.path.join(QUI, 'img', 'gemellari')
PROPOSTA = P4.OUT


def nuova(w=13.333, h=7.5):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(w), Inches(h)
    return prs, prs.slides.add_slide(prs.slide_layouts[6])


def nodo(sl, x, y, w, h, t, sotto=None, c=ROSSO, f=ROSSO_F, pt=11, tratt=False):
    righe = [(t, {'bold': True, 'pt': pt})]
    if sotto:
        righe.append((sotto, {'pt': pt - 3, 'col': MUTED}))
    return box(sl, x, y, w, h, righe, fill=f, line=c, lw=1.5, al=PP_ALIGN.CENTER,
               anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.06, dash=tratt)


def etichetta(sl, x, y, w, t, pt=8, col=INK, al=PP_ALIGN.CENTER):
    txt(sl, x, y, w, 0.3, t, pt=pt, col=col, al=al, anc=MSO_ANCHOR.MIDDLE)


def esporta(prs, nome):
    out = os.path.join(IMG, nome + '.pptx')
    prs.save(out)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['qlmanage', '-t', '-s', '2400', '-o', tmp, out], capture_output=True)
        png = os.path.join(tmp, nome + '.pptx.png')
        os.replace(png, out + '.png')
    return out + '.png'


# ───────────────────────────────────────────── 1. navigazione
def navigazione():
    prs, sl = nuova(13.333, 7.5)
    nodo(sl, 0.3, 0.4, 2.3, 1.0, 'Maschera dei gemelli', 'compilazione come oggi', GRIGIO,
         GRIGIO_F)
    nodo(sl, 3.0, 0.4, 2.6, 1.0, 'Riepilogo', 'documenti e firmatari per atto · CONFERMA',
         GRIGIO, GRIGIO_F)
    nodo(sl, 6.0, 0.4, 3.0, 1.0, 'Divisione automatica', 'N atti · N numeri · prenotazione '
         '(UC specifico o 11999999)', ROSSO, ROSSO_F)
    nodo(sl, 9.6, 0.25, 3.4, 1.3, 'Pagina «Gemelli del parto»', 'testata · card dei gemelli · '
         'testo dell’atto', ROSSO, BIANCO, pt=13)
    freccia(sl, 2.6, 0.9, 3.0, 0.9)
    freccia(sl, 5.6, 0.9, 6.0, 0.9)
    freccia(sl, 9.0, 0.9, 9.6, 0.9)
    etichetta(sl, 5.5, 1.45, 4.0, 'numeri o prenotazione non riusciti: la pagina offre solo '
              'RECUPERA NUMERI E PRENOTAZIONE', pt=7, col=ROSSO)
    etichetta(sl, 9.6, 1.6, 3.4, 'si apre anche dal dettaglio di un gemello: aprirla è riprendere',
              pt=7, col=MUTED)
    # tre colonne di modali
    col = [(0.3, 'Testata', GRIGIO, GRIGIO_F, ['Riepilogo numeri', 'Cancella pratica',
                                               'Recupera numeri e prenotazione']),
           (3.4, 'Card · caso 1', ROSSO, ROSSO_F, ['Validazione', 'Firma dei dichiaranti',
                                                    'Attestazione di conformità', 'Firma dell’USC',
                                                    'Verifica in ANSC', 'Riprova il salvataggio']),
           (6.9, 'Card · caso 2', GIALLO, GIALLO_F, ['Dati per la web app', 'Web app ANSC '
                                                     '(esterna)', 'Recupera da ANSC',
                                                     'Aggiorna SIPO da ANSC']),
           (10.2, 'Testo dell’atto', BLU, BLU_F, ['Salva testo', 'Stampa', 'Copia testo (caso 2)',
                                                   'Anteprima ANSC (caso 1)'])]
    box(sl, 0.2, 2.15, 12.95, 5.05, '', fill=None, line=GRIGIO, dash=True)
    txt(sl, 0.3, 2.2, 6, 0.3, 'Dalla pagina «Gemelli del parto»: modali e comandi', pt=10,
        bold=True, col=ROSSO)
    for x, t, c, f, voci in col:
        nodo(sl, x, 2.6, 2.8, 0.5, t, None, c, f, pt=11)
        for i, v in enumerate(voci):
            est = 'esterna' in v
            nodo(sl, x + 0.15, 3.3 + i * 0.62, 2.5, 0.48, v, None, c, BIANCO, pt=9, tratt=est)
            if i and t.startswith('Card'):
                freccia(sl, x + 1.4, 3.3 + i * 0.62 - 0.14, x + 1.4, 3.3 + i * 0.62, col=c)
    etichetta(sl, 3.4, 6.82, 6.3, 'Le frecce verticali sono l’ordine dei passi; nel caso 1 la '
              'conformità si salta senza firme su carta', pt=7, col=MUTED)
    return esporta(prs, 'gem10_navigazione')


# ───────────────────────────────────────────── 2. stati della card
def stato(sl, x, y, w, nome, ansc, fase, sipo, c, f):
    box(sl, x, y, w, 1.05, [(nome, {'bold': True, 'pt': 10, 'col': c}),
                            ('ANSC_11: ' + ansc, {'pt': 7}), ('COD_FASE: ' + fase, {'pt': 7}),
                            ('SIPO: ' + sipo, {'pt': 7, 'col': MUTED})],
        fill=f, line=c, lw=1.5, forma=MSO_SHAPE.ROUNDED_RECTANGLE, al=PP_ALIGN.CENTER,
        anc=MSO_ANCHOR.MIDDLE, marg=0.04)


def stati_1():
    prs, sl = nuova(13.333, 5.6)
    S = [('BOZZA (prenotato)', '1 BOZZA', 'PRENOTATO', '1 IN LAVORAZIONE', BLU, BLU_F),
         ('CONFERMATO', '2 CONFERMATO', 'VALIDATO', '1 IN LAVORAZIONE', ROSSO, ROSSO_F),
         ('FIRMATO DAL DICHIARANTE', '4 FIRMATO DAL DICHIARANTE', 'VALIDATO',
          '1 IN LAVORAZIONE', ROSSO, ROSSO_F),
         ('FIRMATO PER CONFORMITÀ', '11 FIRMATO PER CONFORMITÀ', 'VALIDATO',
          '1 IN LAVORAZIONE', ROSSO, ROSSO_F),
         ('FIRMATO DA USC', '5 FIRMATO DA USC', 'FIRMATO', '2 DEFINITO', VERDE, VERDE_F)]
    xs = [0.2, 2.85, 5.5, 8.15, 10.8]
    y = 1.3
    for x, s in zip(xs, S):
        stato(sl, x, y, 2.3, *s)
    lab = ['Validazione · VALIDA\nR001 + R009', 'Firma dei dichiaranti\nR012 / R006',
           'Conformità · R010 + R007\n(solo con firme su carta)', 'Firma dell’USC\nR007 + '
           '/finalizzaAtto']
    for i in range(4):
        freccia(sl, xs[i] + 2.3, y + 0.52, xs[i + 1], y + 0.52, col=INK)
        txt(sl, xs[i] + 2.0, y - 0.62, 0.95, 0.6, lab[i], pt=7, al=PP_ALIGN.CENTER,
            anc=MSO_ANCHOR.BOTTOM)
    # salto della conformità
    freccia(sl, 6.65, y + 1.05, 6.65, y + 1.45, col=VERDE)
    freccia(sl, 6.65, y + 1.45, 11.95, y + 1.45, col=VERDE)
    freccia(sl, 11.95, y + 1.45, 11.95, y + 1.05, col=VERDE)
    txt(sl, 7.0, y + 1.47, 4.5, 0.3, 'nessuna firma su carta (o nessun dichiarante): Firma '
        'dell’USC subito', pt=7, col=VERDE)
    # ritorno ai dati
    freccia(sl, 4.0, y + 1.05, 4.0, y + 2.0, col=ROSSO, dash=True)
    freccia(sl, 4.0, y + 2.0, 1.35, y + 2.0, col=ROSSO, dash=True)
    freccia(sl, 1.35, y + 2.0, 1.35, y + 1.05, col=ROSSO, dash=True)
    txt(sl, 1.5, y + 2.02, 2.4, 0.4, 'TORNA AI DATI (dalla modale di firma): stato 0, nuova '
        'validazione', pt=7, col=ROSSO)
    # eccezioni
    nodo(sl, 8.15, 4.2, 2.3, 0.85, 'Esito incerto', 'VERIFICA IN ANSC (R005)', GIALLO,
         GIALLO_F, pt=9)
    nodo(sl, 10.8, 4.2, 2.3, 0.85, 'Non salvato in SIPO', 'RIPROVA IL SALVATAGGIO', ROSSO,
         ROSSO_F, pt=9)
    freccia(sl, 9.3, y + 1.05, 9.3, 4.2, col=GIALLO, dash=True)
    freccia(sl, 11.95, 4.2, 11.95, y + 1.05, col=ROSSO, dash=True)
    txt(sl, 9.4, 3.2, 2.4, 0.5, 'firma senza risposta', pt=7, col=GIALLO)
    txt(sl, 12.0, 3.2, 1.3, 0.6, 'firmato in ANSC, /finalizzaAtto non riuscita', pt=7, col=ROSSO)
    nodo(sl, 0.2, 4.2, 4.0, 0.85, 'CANCELLA PRATICA (testata)', 'solo se nessun gemello è '
         'FIRMATO DA USC: R011 → 9 CANCELLATO', GRIGIO, GRIGIO_F, pt=9)
    txt(sl, 0.2, 0.1, 12.9, 0.4, 'Caso 1 · gli stati della card di un gemello e i pulsanti che '
        'li fanno avanzare', pt=13, bold=True, col=ROSSO)
    return esporta(prs, 'gem10_stati_1')


def stati_2():
    prs, sl = nuova(13.333, 5.6)
    S = [('BOZZA · ATTESA WEBAPP', '1 BOZZA (11999999)', 'PRENOTATO', '1 IN LAVORAZIONE',
          GIALLO, GIALLO_F),
         ('FIRMATO DA USC · DA AGGIORNARE', '5 FIRMATO DA USC', 'RECUPERATO', '1 IN LAVORAZIONE',
          VERDE, VERDE_F),
         ('FIRMATO DA USC', '5 FIRMATO DA USC', 'FIRMATO', '2 DEFINITO', VERDE, VERDE_F)]
    xs = [0.6, 5.0, 9.6]
    y = 1.3
    for x, s in zip(xs, S):
        stato(sl, x, y, 3.1, *s)
    freccia(sl, 3.7, y + 0.52, 5.0, y + 0.52, col=INK)
    freccia(sl, 8.1, y + 0.52, 9.6, y + 0.52, col=INK)
    txt(sl, 3.6, y - 0.75, 1.5, 0.7, 'Dati per la web app → web app → Recupera da ANSC (R005)',
        pt=7, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.BOTTOM)
    txt(sl, 8.0, y - 0.75, 1.7, 0.7, 'Aggiorna SIPO da ANSC + /finalizzaAtto', pt=7,
        al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.BOTTOM)
    nodo(sl, 0.6, 3.6, 3.1, 0.85, 'NON FIRMATO', 'letto in ANSC: non ancora 5 · si torna alla '
         'web app', GIALLO, GIALLO_F, pt=9)
    nodo(sl, 4.0, 3.6, 3.1, 0.85, 'INCOERENTE', 'intestatario o tipologia diversi · nessuna '
         'scrittura', ROSSO, ROSSO_F, pt=9)
    freccia(sl, 2.0, y + 1.05, 2.0, 3.6, col=GIALLO, dash=True)
    freccia(sl, 2.4, 3.6, 2.4, y + 1.05, col=GIALLO, dash=True)
    freccia(sl, 3.4, y + 1.05, 5.2, 3.6, col=ROSSO, dash=True)
    txt(sl, 2.5, 2.7, 1.6, 0.5, 'Recupera da ANSC', pt=7, col=GIALLO)
    nodo(sl, 8.6, 3.6, 4.1, 0.85, 'CANCELLA PRATICA (testata)', 'solo se nessun gemello è '
         'FIRMATO DA USC: R011 sulle bozze', GRIGIO, GRIGIO_F, pt=9)
    txt(sl, 0.2, 0.1, 12.9, 0.4, 'Caso 2 · gli stati della card di un gemello: l’atto si forma '
        'sulla web app e torna in SIPO', pt=13, bold=True, col=ROSSO)
    return esporta(prs, 'gem10_stati_2')


# ───────────────────────────────────────────── 3. ritagli della proposta
RITAGLI = {   # slide (1-based) del file REALE (l'utente ha tolto la slide «Che cosa cambia»): (nome, x0, y0, x1, y1) in pollici
    2: ('gem10_s_card', 0.3, 1.25, 6.8, 6.3),
    3: ('gem10_s_caso1', 0.25, 1.1, 13.1, 7.45),
    4: ('gem10_s_validazione', 0.3, 1.15, 8.85, 7.35),
    5: ('gem10_s_firma_dich', 0.3, 1.15, 8.85, 7.35),
    6: ('gem10_s_conformita', 0.3, 1.15, 8.85, 7.35),
    7: ('gem10_s_firma_usc', 0.3, 1.15, 8.85, 7.35),
    8: ('gem10_s_caso2', 0.25, 1.1, 13.1, 7.45),
    9: ('gem10_s_dati_webapp', 0.3, 1.15, 8.85, 7.35),
    10: ('gem10_s_recupera', 0.35, 1.2, 13.0, 7.2),
    11: ('gem10_s_percorso', 0.35, 1.25, 12.95, 6.05),
}


def ritagli():
    fatti = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, (nome, x0, y0, x1, y1) in RITAGLI.items():
            prs = Presentation(PROPOSTA)
            ids = prs.slides._sldIdLst
            for j, s in reversed(list(enumerate(list(ids)))):
                if j != n - 1:
                    ids.remove(s)
            f = os.path.join(tmp, 's%02d.pptx' % n)
            prs.save(f)
            subprocess.run(['qlmanage', '-t', '-s', '2400', '-o', tmp, f], capture_output=True)
            im = Image.open(f + '.png')
            k = im.width / 13.333
            out = os.path.join(IMG, nome + '.png')
            im.crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k))).save(out)
            fatti.append(out)
    return fatti


# ───────────────────────────────────────────── 4. ERD (dalla v0.7, con il testo dell'atto)
def erd():
    """gem7_erd con TXT_TESTO_ATTO su ANSC_SOGGETTO_ATTO e le colonne vere di DATI_ATTO_ESTERNO."""
    import inspect
    import diagrammi_gemellari_v0_7_pptx as G7
    src = inspect.getsource(G7.erd).replace('def erd(', 'def erd10(')
    src = src.replace("        ('', 'COD_ORIGINE · TS_ABBINAMENTO'),\n",
                      "        ('', 'COD_ORIGINE · TS_ABBINAMENTO'),\n"
                      "        ('', 'TXT_TESTO_ATTO · TS_TESTO_ATTO  (testo dell’atto)'),\n")
    src = src.replace("""        ('PK', 'id_atto_esterno'), ('', 'nr_anno_atto · nr_atto_comunale'),
        ('', 'id_atto_sipo · id_ansc · stato'),""", """        ('PK', 'id_prenotazione_atti · nr_atto_comunale'),
        ('', 'nr_anno_atto · cd_stato_numero_prenotato'), ('', 'id_atto_sipo · id_ansc_collegato'),""")
    src = src.replace("'prenotazione e recupero sulla riga del gemello 1'",
                      "'prenotazione sulla riga del gemello 1'")
    assert 'TXT_TESTO_ATTO' in src and 'id_ansc_collegato' in src
    ns = vars(G7)
    exec(src, ns)
    out = os.path.join(IMG, 'gem10_erd.pptx')
    ns['erd10'](out)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['qlmanage', '-t', '-s', '2400', '-o', tmp, out], capture_output=True)
        os.replace(os.path.join(tmp, 'gem10_erd.pptx.png'), out + '.png')
    return out + '.png'


if __name__ == '__main__':
    for f in [navigazione(), stati_1(), stati_2(), erd()] + ritagli():
        print(os.path.relpath(f, QUI))
