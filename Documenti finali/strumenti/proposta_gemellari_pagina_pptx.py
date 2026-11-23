# -*- coding: utf-8 -*-
"""Proposta per il capitolo 7 dell'analisi delle nascite gemellari (22/11/2026): una sola pagina
«Gestione del parto» dopo la divisione, per il caso 1 e il caso 2. Forme native, modificabili.

    /Library/Developer/CommandLineTools/usr/bin/python3 proposta_gemellari_pagina_pptx.py
"""
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, '..', 'PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.1.pptx')

ROSSO, ROSSO_F = '8c0029', 'f6e6eb'
INK, MUTED, GRIGIO, GRIGIO_F = '222222', '666666', 'b0b0b0', 'f2f2f2'
VERDE, VERDE_F = '3f8f5f', 'e3f3e8'
BLU, BLU_F = '2f5f9f', 'e4edf8'
GIALLO, GIALLO_F = 'b58900', 'fff6d5'
BIANCO = 'ffffff'
EVID = 'fff176'


def rgb(h):
    return RGBColor.from_string(h)


def box(sl, x, y, w, h, testo='', fill=BIANCO, line=GRIGIO, pt=10, bold=False, col=INK,
        al=PP_ALIGN.LEFT, forma=MSO_SHAPE.RECTANGLE, anc=MSO_ANCHOR.TOP, lw=0.75, marg=0.06,
        dash=False, it=False):
    s = sl.shapes.add_shape(forma, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
        if dash:
            from pptx.enum.dml import MSO_LINE
            s.line.dash_style = MSO_LINE.DASH
    s.shadow.inherit = False
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anc
    for a in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'):
        setattr(tf, a, Inches(marg))
    righe = testo if isinstance(testo, (list, tuple)) else [testo]
    for i, r in enumerate(righe):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = al
        if isinstance(r, tuple):
            t, kw = r
        else:
            t, kw = r, {}
        run = p.add_run()
        run.text = t
        run.font.size = Pt(kw.get('pt', pt))
        run.font.bold = kw.get('bold', bold)
        run.font.italic = kw.get('it', it)
        run.font.name = 'Arial'
        run.font.color.rgb = rgb(kw.get('col', col))
    return s


def txt(sl, x, y, w, h, testo, **kw):
    kw.setdefault('fill', None)
    kw.setdefault('line', None)
    kw.setdefault('marg', 0.02)
    return box(sl, x, y, w, h, testo, **kw)


def btn(sl, x, y, w, t, attivo=True, primario=False, h=0.26, pt=8):
    if primario:
        f, l, c = ROSSO, ROSSO, BIANCO
    elif attivo:
        f, l, c = BIANCO, ROSSO, ROSSO
    else:
        f, l, c = GRIGIO_F, GRIGIO, GRIGIO
    return box(sl, x, y, w, h, t, fill=f, line=l, col=c, pt=pt, bold=True, al=PP_ALIGN.CENTER,
               anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.02)


def pill(sl, x, y, w, t, col, fondo, pt=7, h=0.2):
    return box(sl, x, y, w, h, t, fill=fondo, line=col, col=col, pt=pt, bold=True,
               al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE,
               marg=0.01)


def freccia(sl, x1, y1, x2, y2, col=MUTED, w=1.25, dash=False):
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2),
                                Inches(y2))
    c.line.color.rgb = rgb(col)
    c.line.width = Pt(w)
    if dash:
        from pptx.enum.dml import MSO_LINE
        c.line.dash_style = MSO_LINE.DASH
    from lxml import etree
    ln = c.line._get_or_add_ln()
    e = etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd')
    e.set('type', 'triangle')
    return c


def titolo(sl, t, sotto=None):
    box(sl, 0, 0, 13.333, 0.08, fill=ROSSO, line=None)
    txt(sl, 0.4, 0.22, 12.5, 0.5, t, pt=22, bold=True, col=ROSSO)
    if sotto:
        txt(sl, 0.4, 0.72, 12.5, 0.4, sotto, pt=12, col=MUTED)


def elenco(sl, x, y, w, h, voci, pt=12):
    righe = []
    for v in voci:
        if isinstance(v, tuple):
            righe.append(('• ' + v[0] + ' ', {'bold': True, 'pt': pt}))
            righe.append(('   ' + v[1], {'pt': pt - 1, 'col': MUTED}))
        else:
            righe.append(('• ' + v, {'pt': pt}))
    return txt(sl, x, y, w, h, righe)


def tabella(sl, x, y, w, righe, larghezze, pt=9, h_riga=0.3):
    shp = sl.shapes.add_table(len(righe), len(righe[0]), Inches(x), Inches(y), Inches(w),
                              Inches(h_riga * len(righe)))
    t = shp.table
    for j, lw in enumerate(larghezze):
        t.columns[j].width = Inches(lw)
    for i, r in enumerate(righe):
        for j, v in enumerate(r):
            c = t.cell(i, j)
            c.text = ''
            p = c.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = v
            run.font.size = Pt(pt)
            run.font.name = 'Arial'
            run.font.bold = (i == 0)
            run.font.color.rgb = rgb(BIANCO if i == 0 else INK)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(ROSSO if i == 0 else (GRIGIO_F if i % 2 == 0 else BIANCO))
            c.margin_left = c.margin_right = Inches(0.05)
            c.margin_top = c.margin_bottom = Inches(0.03)
    return t


# ───────────────────────────────────────────── la pagina (mockup)
STATI = {
    'def': ('2 DEFINITO · 5 FIRMATO DA USC', VERDE, VERDE_F),
    'corso': ('IN LAVORAZIONE', ROSSO, ROSSO_F),
    'attesa': ('IN ATTESA', MUTED, GRIGIO_F),
    'abb': ('ABBINATO · 5 FIRMATO DA USC', VERDE, VERDE_F),
    'wa': ('WA · ATTESA WEBAPP', GIALLO, GIALLO_F),
    'nontr': ('NON TROVATO', ROSSO, ROSSO_F),
}

PASSI_C1 = ['Doc.', 'Valida', 'Firma dich.', 'Conform.', 'Firma USC', 'Definito']
PASSI_C2 = ['Testo copiato', 'Atto su web app', 'Recuperato', 'Definito']


def card(sl, x, y, w, h, g, stato, passi, fatto, azioni, sel=False, nota=None):
    pos, nome, sesso, tip, uc, num, ida = g
    lab, c, f = STATI[stato]
    box(sl, x, y, w, h, fill=BIANCO if not sel else 'fffafb', line=ROSSO if sel else GRIGIO,
        lw=2.25 if sel else 0.75, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(sl, x + 0.1, y + 0.06, 2.2, 0.25, 'Gemello ' + pos + ' · ' + sesso, pt=10, bold=True)
    pill(sl, x + w - 2.05, y + 0.07, 1.95, lab, c, f)
    txt(sl, x + 0.1, y + 0.3, w - 1.3, 0.22, nome, pt=8, col=MUTED)
    txt(sl, x + 0.1, y + 0.5, w - 1.3, 0.22, tip + ' · UC ' + uc, pt=8, col=MUTED)
    # numero comunale in grande
    txt(sl, x + w - 1.25, y + 0.3, 1.15, 0.18, 'n. comunale', pt=7, col=MUTED, al=PP_ALIGN.RIGHT)
    txt(sl, x + w - 1.25, y + 0.42, 1.15, 0.4, num, pt=20, bold=True, col=ROSSO,
        al=PP_ALIGN.RIGHT)
    # idAnsc con il numero evidenziato
    if ida:
        a, b, cc, d = ida.split('-')
        s = box(sl, x + 0.1, y + 0.74, w - 1.4, 0.22, '', fill=None, line=None, marg=0.01)
        p = s.text_frame.paragraphs[0]
        for t, ev in (('idAnsc  ' + a + '-' + b + '-', False), (cc, True), ('-' + d, False)):
            r = p.add_run()
            r.text = t
            r.font.size = Pt(8)
            r.font.name = 'Courier New'
            r.font.bold = ev
            r.font.color.rgb = rgb(INK)
            if ev:
                from lxml import etree
                rpr = r._r.get_or_add_rPr()
                hl = etree.SubElement(rpr, '{http://schemas.openxmlformats.org/drawingml/2006/main}highlight')
                clr = etree.SubElement(hl, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
                clr.set('val', EVID)
    else:
        txt(sl, x + 0.1, y + 0.74, w - 1.4, 0.22, 'idAnsc  —  (non ancora noto)', pt=8,
            col=GRIGIO)
    # passi
    pw = (w - 0.2) / len(passi)
    for i, p_ in enumerate(passi):
        col, fon = ((VERDE, VERDE_F) if i < fatto else
                    (ROSSO, ROSSO_F) if i == fatto and stato == 'corso' else (GRIGIO, BIANCO))
        box(sl, x + 0.1 + i * pw, y + 1.0, pw - 0.03, 0.2, p_, fill=fon, line=col, col=col, pt=6,
            bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, marg=0.01)
    # azioni
    xb = x + 0.1
    for t, att, prim in azioni:
        bw = 0.22 + 0.078 * len(t)
        btn(sl, xb, y + h - 0.36, bw, t, att, prim)
        xb += bw + 0.08
    if nota:
        txt(sl, xb, y + h - 0.36, x + w - xb - 0.05, 0.28, nota, pt=7, col=MUTED,
            anc=MSO_ANCHOR.MIDDLE)


def testata(sl, y, caso, comandi):
    box(sl, 0.3, y, 12.73, 1.05, fill=GRIGIO_F, line=GRIGIO)
    txt(sl, 0.4, y + 0.05, 3.2, 0.25, 'Dichiarazione di nascita · parto plurimo (3 nati)',
        pt=9, bold=True, col=ROSSO)
    col = [('Madre', 'COGNOME NOME · CF ****************'),
           ('Padre', 'COGNOME NOME · CF ****************'),
           ('Dichiarante', 'il padre · presente in sala')]
    for i, (k, v) in enumerate(col):
        txt(sl, 0.4, y + 0.3 + i * 0.2, 4.0, 0.2, [(k + ': ', {'bold': True, 'pt': 8}),
                                                   ], pt=8)
        txt(sl, 1.2, y + 0.3 + i * 0.2, 3.3, 0.2, v, pt=8, col=MUTED)
    col2 = [('Data e luogo', '18/11/2026 · Roma, Policlinico'),
            ('Tipo atto', 'gemelli · Modello 30 · pratica divisa in 3 atti'), ('Caso', caso)]
    for i, (k, v) in enumerate(col2):
        txt(sl, 4.7, y + 0.1 + i * 0.2, 1.1, 0.2, k + ':', pt=8, bold=True)
        txt(sl, 5.8, y + 0.1 + i * 0.2, 3.4, 0.2, v, pt=8, col=MUTED)
    xb = 13.03 - 0.1
    for t, att, prim in reversed(comandi):
        bw = 0.22 + 0.075 * len(t)
        xb -= bw
        btn(sl, xb, y + 0.74, bw, t, att, prim)
        xb -= 0.08
    pill(sl, 10.2, y + 0.1, 2.73, 'OTP ANSC valido · 3 h 12 min', VERDE, VERDE_F, pt=8, h=0.24)


def pannello_testo(sl, x, y, w, h, titolo_, fonte, numero, comandi, bloccato=False, nota=None,
                   nascita='è nato un bambino di sesso femminile', fratelli=None):
    box(sl, x, y, w, h, fill=BIANCO, line=GRIGIO)
    txt(sl, x + 0.1, y + 0.06, w - 0.2, 0.25, titolo_, pt=10, bold=True)
    txt(sl, x + 0.1, y + 0.3, w - 0.2, 0.2, fonte, pt=7, col=MUTED)
    corpo = [('ATTO DI NASCITA n. ' + numero + ' · parte I · serie A', {'bold': True, 'pt': 8}),
             ('L’anno duemilaventisei, addì diciotto del mese di novembre, nella casa comunale, '
              'avanti a me, Ufficiale dello Stato Civile, è comparso COGNOME NOME, il quale mi ha '
              'dichiarato che il giorno diciotto novembre alle ore 10.42, nel Policlinico, dalla '
              'sua unione con COGNOME NOME ' + nascita + ', '
              'secondo di un parto gemellare [formula 36] …',
              {'pt': 8}),
             (fratelli or ('Gli atti dei fratelli: 2026-10527618-13617-058091 (precedente), '
                           '2026-10527620-13619-058091 (successivo).'), {'pt': 8, 'col': BLU}),
             ('…', {'pt': 8})]
    box(sl, x + 0.1, y + 0.52, w - 0.2, h - 1.05, corpo, fill='fcfcfc' if not bloccato else
        GRIGIO_F, line=GRIGIO if bloccato else BLU, lw=1.0, dash=not bloccato, marg=0.1)
    if nota:
        txt(sl, x + 0.1, y + h - 0.5, w - 0.2, 0.2, nota, pt=7, col=MUTED, it=True)
    xb = x + 0.1
    for t, att, prim in comandi:
        bw = 0.22 + 0.078 * len(t)
        btn(sl, xb, y + h - 0.32, bw, t, att, prim)
        xb += bw + 0.08


def slide_mockup_1(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'La pagina «Gemelli del parto» — caso 1 (stesso UC)',
           'Ipotesi: il gemello 1 è formato e definito; il gemello 2 è sulla firma del '
           'dichiarante; il gemello 3 attende')
    testata(sl, 1.15, '1 · stesso UC 11111000 · tutto da SIPO',
            [('NUMERI E PRENOTAZIONE', False, False), ('RIEPILOGO NUMERI', True, False),
             ('RINUNCIA AL PARTO', False, False)])
    G = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13617",
          "2026-10527618-13617-058091"),
         ("2", "NATO 2 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13618",
          "2026-10527619-13618-058091"),
         ("3", "NATO 3 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13619",
          "2026-10527620-13619-058091"))
    y0, h = 2.3, 1.6
    card(sl, 0.3, y0, 6.0, h, G[0], 'def', PASSI_C1, 6,
         [('APRI IL PDF', True, False)], nota='definito il 18/11 alle 12.10')
    card(sl, 0.3, y0 + h + 0.08, 6.0, h, G[1], 'corso', PASSI_C1, 2,
         [('STAMPA MODULO', True, False), ('CARICA FIRMA DICHIARANTE', True, True),
          ('DOCUMENTI', True, False)], sel=True)
    card(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G[2], 'attesa', PASSI_C1, 0,
         [('DOCUMENTI', False, False), ('VALIDA', False, False)],
         nota='si apre dopo la firma USC del gemello 2')
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO (formulario) · inviato ad ANSC con la validazione '
                   '(composizioneCompleta) · validato: non più modificabile',
                   '13618', [('STAMPA', True, False), ('ANTEPRIMA ANSC (R010)', True, False),
                             ('RIGENERA', False, False), ('SALVA', False, False)],
                   bloccato=True,
                   nota='Per modificarlo: TORNA AI DATI sul gemello (stato 0, nuova validazione).')


def slide_mockup_2(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'La stessa pagina — caso 2 (UC diversi)',
           'Ipotesi: testo del gemello 1 copiato e atto firmato sulla web app; gemello 2 '
           'selezionato, testo modificabile da copiare; gemello 3 da fare')
    testata(sl, 1.15, '2 · UC diversi · web app e recupero',
            [('NUMERI PER LA WEB APP', False, False), ('RIEPILOGO NUMERI', True, False),
             ('RECUPERA GEMELLI', True, False), ('DEFINISCI GEMELLI', False, False)])
    G = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13640",
          "2026-10531102-13640-058091"),
         ("2", "NATO 2 — COGNOME NOME", "F", "2 nato morto", "11111100", "13641", None),
         ("3", "NATO 3 — COGNOME NOME", "M", "3 nato vivo poi deceduto", "11111200", "13642",
          None))
    y0, h = 2.3, 1.6
    card(sl, 0.3, y0, 6.0, h, G[0], 'abb', PASSI_C2, 3, [('APRI WEB APP', True, False)],
         nota='recuperato: R005 per numero comunale')
    card(sl, 0.3, y0 + h + 0.08, 6.0, h, G[1], 'wa', PASSI_C2, 0,
         [('COPIA TESTO', True, True), ('APRI WEB APP', True, False),
          ('SEGNA COME FATTO', True, False)], sel=True,
         nota='certificato medico')
    card(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G[2], 'wa', PASSI_C2, 0,
         [('COPIA TESTO', True, False), ('APRI WEB APP', True, False)])
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO (formulario) · modificabile · da incollare nella '
                   'composizione libera della bozza sulla web app',
                   '13641', [('COPIA TESTO', True, True), ('STAMPA', True, False),
                             ('RIGENERA', True, False), ('SALVA', True, False)],
                   nota='Gli idAnsc dei fratelli li assegna la web app: si completano lì.',
                   nascita='è nata morta una bambina',
                   fratelli='Gli atti dei fratelli: [identificativi da completare sulla web app].')


# ───────────────────────────────────────────── le altre slide
def costruisci():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    V = prs.slide_layouts[6]

    # 1 titolo
    sl = prs.slides.add_slide(V)
    box(sl, 0, 0, 13.333, 7.5, fill=ROSSO, line=None)
    txt(sl, 0.8, 2.4, 11.7, 1.0, 'Nascite gemellari: una sola pagina dopo la divisione',
        pt=32, bold=True, col=BIANCO)
    txt(sl, 0.8, 3.4, 11.7, 1.2, ['Proposta per riscrivere il capitolo 7 «La modalità di '
                                  'integrazione» dell’analisi v0.9',
                                  'Bozza di discussione · 22/11/2026'], pt=16, col=BIANCO)

    # 2 oggi
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Perché il capitolo 7 è faticoso',
           'Oggi due casi con superfici diverse, e ogni momento ha la sua schermata o finestra')
    tabella(sl, 0.4, 1.3, 7.6, [
        ['Momento', 'Caso 1 oggi (v0.9)', 'Caso 2 oggi (v0.9)'],
        ['Dopo la divisione', 'Riepilogo gemelli', 'Riepilogo gemelli (UC diversi)'],
        ['Numeri comunali', 'DEFINISCI + finestra di raccordo', 'DATI PER ANSC + finestra di raccordo'],
        ['Lavoro sul gemello', 'procedura DEFINISCI: 6 passi per gemello', 'pratica guidata (finestra a parte)'],
        ['Testo dell’atto', 'dentro i passi, in sola lettura', 'nella pratica guidata'],
        ['Rientro', '—', 'RECUPERA GEMELLI + seconda finestra di raccordo'],
        ['Errori', 'schermata «DEFINISCI in corso»', '—'],
        ['Fine', 'Esito del parto', 'Esito del parto'],
        ['Ripresa', 'riepilogo trasformato in pagina di ripresa', 'riapertura della pratica guidata'],
    ], [1.7, 2.95, 2.95], pt=9, h_riga=0.42)
    box(sl, 8.4, 1.3, 4.5, 3.8, [('In tutto', {'bold': True, 'pt': 14, 'col': ROSSO}),
                                 ('Una dozzina fra schermate e finestre, 2 sequenze, 3 apparizioni della finestra di raccordo, '
                                  'una pagina di ripresa a parte.', {'pt': 12}),
                                 ('', {'pt': 6}),
                                 ('L’operatore cambia superficie a ogni passo e lo stato del parto '
                                  'non è mai tutto davanti a lui.', {'pt': 12}),
                                 ('', {'pt': 6}),
                                 ('Il documento descrive più le transizioni fra pagine che il '
                                  'lavoro da fare.', {'pt': 12, 'col': MUTED})],
        fill=ROSSO_F, line=ROSSO, marg=0.15)

    # 3 strategia
    sl = prs.slides.add_slide(V)
    titolo(sl, 'La strategia: una pagina, tre zone, i due casi come insiemi di azioni',
           'Dopo la divisione (/performAttiPlurigemellari) SIPO apre sempre la stessa pagina')
    elenco(sl, 0.4, 1.3, 7.2, 5.8, [
        ('Una sola pagina per il parto.', 'Sostituisce riepilogo, finestre di raccordo, procedura '
         'DEFINISCI, pratica guidata, esito e pagina di ripresa.'),
        ('Le card sono il raccordo.', 'Ogni card mostra il numero comunale in grande e l’idAnsc con '
         'il numero evidenziato: la finestra di raccordo non serve più.'),
        ('Il caso lo decide l’UC, la pagina non cambia.', 'Caso 1 e caso 2 differiscono solo per i '
         'pulsanti di testata e di card.'),
        ('Un gemello alla volta, imposto dalla pagina.', 'È attiva solo la card del primo gemello '
         'non concluso; le altre mostrano lo stato (guida ANSC p. 45).'),
        ('Il testo a destra, sempre visibile.', 'È il testo del gemello selezionato, modificabile '
         'finché l’atto non è validato (caso 1) o copiato sulla web app (caso 2).'),
        ('Aprire la pagina è già riprendere.', 'All’apertura SIPO legge lo store e, per gli atti con '
         'idAnsc, lo stato in ANSC (R005): la card riparte da lì.'),
    ], pt=13)
    # schema tre zone
    x, y = 8.1, 1.4
    box(sl, x, y, 4.8, 0.8, ['TESTATA', ('genitori · dati dell’atto · azioni di parto · OTP',
                                         {'pt': 9, 'col': MUTED})], fill=GRIGIO_F,
        line=GRIGIO, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    box(sl, x, y + 0.9, 2.2, 3.4, ['CARD DEI GEMELLI', ('una per nato, in ordine di nascita, '
                                                         'con i pulsanti del suo stato',
                                                         {'pt': 9, 'col': MUTED})],
        fill=ROSSO_F, line=ROSSO, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    box(sl, x + 2.3, y + 0.9, 2.5, 3.4, ['TESTO DELL’ATTO', ('del gemello selezionato · '
                                                             'modificabile · stampa',
                                                             {'pt': 9, 'col': MUTED})],
        fill=BLU_F, line=BLU, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    txt(sl, x, y + 4.4, 4.8, 0.6, 'La testata è bassa (circa un sesto dell’altezza); card e '
        'testo dividono il resto.', pt=10, col=MUTED, it=True)

    # 4-5 mockup
    slide_mockup_1(prs)
    slide_mockup_2(prs)

    # 6 la card
    sl = prs.slides.add_slide(V)
    titolo(sl, 'La card del gemello', 'Un box multifunzione: identità, numero, atto ANSC, '
           'avanzamento e i soli pulsanti che lo stato consente')
    card(sl, 0.5, 1.5, 6.0, 1.62, ("2", "NATO 2 — COGNOME NOME", "F", "1 nato vivo", "11111000",
                                   "13618", "2026-10527619-13618-058091"), 'corso', PASSI_C1, 2,
         [('STAMPA MODULO', True, False), ('CARICA FIRMA DICHIARANTE', True, True),
          ('DOCUMENTI', True, False)], sel=True)
    leg = [('1', 'Posizione, sesso, nome, tipologia di nascita (ANSC_107 dai due flag), UC.'),
           ('2', 'Stato in chiaro: coppia stato SIPO · stato ANSC, o lo stato dello store '
                 '(WA · ATTESA WEBAPP, ABBINATO, NON TROVATO…).'),
           ('3', 'Numero comunale in grande: è ciò che l’ufficiale confronta.'),
           ('4', 'idAnsc con il numero evidenziato: l’abbinamento si vede, non si deduce.'),
           ('5', 'Barra dei passi: fatti in verde, quello in corso in rosso.'),
           ('6', 'Pulsanti: uno primario (l’azione successiva) più quelli di supporto; '
                 'disattivati se non è il turno del gemello.')]
    y = 1.5
    for n, t in leg:
        box(sl, 6.9, y, 0.32, 0.32, n, fill=ROSSO, line=None, col=BIANCO, bold=True,
            al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.OVAL, pt=10)
        txt(sl, 7.35, y, 5.6, 0.6, t, pt=11)
        y += 0.68
    box(sl, 0.5, 3.4, 6.0, 1.6, [('Clic sulla card = selezione', {'bold': True}),
                                 ('Il pannello di destra mostra il testo di quel gemello. Si '
                                  'possono selezionare anche le card non attive, per leggere o '
                                  'stampare.', {'pt': 10, 'col': MUTED}),
                                 ('', {'pt': 4}),
                                 ('Un solo pulsante primario', {'bold': True}),
                                 ('L’ufficiale non deve sapere quale sia il passo: la card glielo '
                                  'propone.', {'pt': 10, 'col': MUTED})],
        fill=GRIGIO_F, line=GRIGIO, pt=11, marg=0.12)
    box(sl, 0.5, 5.2, 6.0, 1.6, [('Errori sulla card, non in una pagina a parte', {'bold': True}),
                                 ('Esito certo: messaggio sulla card + RIPROVA (OTP scaduto '
                                  '406002, firma 406004…).', {'pt': 10, 'col': MUTED}),
                                 ('Esito incerto: VERIFICA IN ANSC (R005), mai un secondo '
                                  'tentativo alla cieca.', {'pt': 10, 'col': MUTED})],
        fill=GRIGIO_F, line=GRIGIO, pt=11, marg=0.12)

    # 7 azioni per stato
    sl = prs.slides.add_slide(V)
    titolo(sl, 'I pulsanti della card, stato per stato',
           'Il primo pulsante di ogni riga è il primario; gli altri sono di supporto')
    tabella(sl, 0.4, 1.25, 6.3, [
        ['Caso 1 · stato del gemello', 'Pulsanti', 'Servizi'],
        ['1 BOZZA (prenotato)', 'DOCUMENTI · VALIDA', 'R001 · R009 validazione'],
        ['2 CONFERMATO', 'STAMPA MODULO · CARICA FIRMA DICHIARANTE · TORNA AI DATI', 'R006'],
        ['4 FIRMATO DAL DICHIARANTE', 'FIRMA CONFORMITÀ', 'R010 · R007'],
        ['11 FIRMATO PER CONFORMITÀ', 'FIRMA USC', 'R007, poi /finalizzaAtto'],
        ['5 · 2 DEFINITO', 'APRI IL PDF', '—'],
        ['esito incerto', 'VERIFICA IN ANSC', 'R005'],
    ], [1.9, 2.8, 1.6], pt=9, h_riga=0.5)
    tabella(sl, 6.9, 1.25, 6.0, [
        ['Caso 2 · stato del gemello', 'Pulsanti', 'Servizi'],
        ['WA · ATTESA WEBAPP', 'COPIA TESTO · APRI WEB APP · SEGNA COME FATTO', '—'],
        ['segnato come fatto', 'RECUPERA (solo questo gemello)', 'R005'],
        ['NON TROVATO · NON FIRMATO', 'RECUPERA · APRI WEB APP', 'R005'],
        ['INCOERENTE', 'DETTAGLIO (nessuna scrittura)', '—'],
        ['ABBINATO', 'APRI WEB APP', '—'],
        ['2 DEFINITO', 'APRI IL PDF', '—'],
    ], [1.8, 2.8, 1.4], pt=9, h_riga=0.5)
    txt(sl, 0.4, 5.1, 12.5, 1.6, [
        ('Caso 1: la firma USC chiude il gemello e lo definisce subito in SIPO; la card successiva '
         'si attiva da sola.', {'pt': 11}),
        ('Caso 2: la definizione resta di parto (DEFINISCI GEMELLI in testata), perché in SIPO i '
         'gemelli si definiscono insieme quando sono tutti abbinati.', {'pt': 11}),
        ('Documenti, testo e TORNA AI DATI restano disponibili fino alla firma USC del gemello.',
         {'pt': 11, 'col': MUTED})])

    # 8 testata e testo
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Le azioni di parto e le azioni sul testo',
           'In testata ciò che vale per tutti i nati; a destra ciò che vale per il testo '
           'selezionato')
    tabella(sl, 0.4, 1.25, 6.3, [
        ['Azione di parto (testata)', 'Quando', 'Che cosa fa'],
        ['NUMERI E PRENOTAZIONE (caso 1)', 'una volta, all’inizio', 'POST /richiesta N numeri + '
         'R009 /prenota/evento; righe dello store e di ANSC_SOGGETTO_ATTO'],
        ['NUMERI PER LA WEB APP (caso 2)', 'una volta, all’inizio', 'POST /richiesta N numeri; '
         'righe in WA · ATTESA WEBAPP'],
        ['RIEPILOGO NUMERI', 'sempre', 'stampa le card come promemoria su carta'],
        ['RECUPERA GEMELLI (caso 2)', 'quando gli atti sono sulla web app', 'R005 per ciascun '
         'numero, abbinamento, esito su ogni card'],
        ['DEFINISCI GEMELLI (caso 2)', 'tutti abbinati', '/finalizzaAtto per ciascun atto'],
        ['RINUNCIA AL PARTO', 'nessun gemello a 5', 'R011 + PUT /scarta; pratica modificabile'],
    ], [2.0, 1.5, 2.8], pt=9, h_riga=0.55)
    tabella(sl, 6.9, 1.25, 6.0, [
        ['Azione sul testo (destra)', 'Caso', 'Che cosa fa'],
        ['STAMPA', '1 e 2', 'il testo del gemello selezionato'],
        ['RIGENERA', '1 e 2', 'ricompone dal formulario e scarta le modifiche'],
        ['SALVA', '1 e 2', 'conserva il testo modificato (dove: domanda 2)'],
        ['COPIA TESTO', '2', 'negli appunti, per la composizione libera'],
        ['ANTEPRIMA ANSC', '1', 'R010 con presaVisione, dopo la validazione'],
    ], [1.7, 0.8, 3.5], pt=9, h_riga=0.55)
    txt(sl, 0.4, 5.3, 12.5, 1.5, [
        ('Il testo è modificabile finché non esce da SIPO: nel caso 1 fino a VALIDA, che lo invia '
         'come composizioneCompleta; nel caso 2 fino a quando l’ufficiale lo segna come copiato.',
         {'pt': 11}),
        ('Dopo, si modifica solo tornando ai dati (caso 1, prima della firma USC) o sulla web app '
         '(caso 2).', {'pt': 11, 'col': MUTED})])

    # 9 flusso
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Il percorso sulla pagina', 'Le stesse fasi nei due casi; cambia solo il '
           'canale con cui si forma l’atto')
    fasi = [('Compilazione e divisione', 'come oggi in SIPO; UC di ciascun nato dai flag',
             GRIGIO_F, GRIGIO),
            ('Apertura della pagina', 'caso dall’UC; lettura dello store (+ R005)', BLU_F, BLU),
            ('Azione di parto iniziale', 'numeri (caso 2) o numeri + prenotazione (caso 1)',
             ROSSO_F, ROSSO),
            ('Lavoro sulle card', 'un gemello alla volta, pulsante primario per stato', ROSSO_F,
             ROSSO),
            ('Parto concluso', 'tutte le card a 2 DEFINITO; la pagina resta in consultazione',
             VERDE_F, VERDE)]
    x = 0.4
    for i, (t, s, f, l) in enumerate(fasi):
        box(sl, x, 1.5, 2.3, 1.3, [(t, {'bold': True, 'pt': 12}), (s, {'pt': 9, 'col': MUTED})],
            fill=f, line=l, forma=MSO_SHAPE.ROUNDED_RECTANGLE, al=PP_ALIGN.CENTER,
            anc=MSO_ANCHOR.MIDDLE, marg=0.1)
        if i < 4:
            freccia(sl, x + 2.3, 2.15, x + 2.55, 2.15)
        x += 2.55
    # corsie
    box(sl, 0.4, 3.2, 12.5, 1.6, '', fill=BIANCO, line=GRIGIO)
    txt(sl, 0.5, 3.25, 2.0, 0.3, 'Card · caso 1', pt=11, bold=True, col=ROSSO)
    seq1 = ['DOCUMENTI', 'VALIDA (R009 + testo)', 'FIRMA DICHIARANTE (R006)',
            'FIRMA CONFORMITÀ (R007)', 'FIRMA USC (R007)', '/finalizzaAtto → card successiva']
    x = 0.5
    for i, t in enumerate(seq1):
        box(sl, x, 3.65, 1.9, 0.6, t, fill=ROSSO_F, line=ROSSO, pt=9, bold=True,
            al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
        if i < 5:
            freccia(sl, x + 1.9, 3.95, x + 2.08, 3.95)
        x += 2.08
    txt(sl, 0.5, 4.35, 12.2, 0.35, 'si ripete per ciascun gemello · errore certo: RIPROVA · '
        'esito incerto: VERIFICA IN ANSC', pt=9, col=MUTED, it=True)
    box(sl, 0.4, 5.0, 12.5, 1.9, '', fill=BIANCO, line=GRIGIO)
    txt(sl, 0.5, 5.05, 2.0, 0.3, 'Card · caso 2', pt=11, bold=True, col=GIALLO)
    seq2 = ['COPIA TESTO', 'APRI WEB APP: atto con il numero e la tipologia',
            'SEGNA COME FATTO', 'RECUPERA (card o testata, R005)', 'DEFINISCI GEMELLI (testata)']
    x = 0.5
    for i, t in enumerate(seq2):
        box(sl, x, 5.45, 2.3, 0.7, t, fill=GIALLO_F, line=GIALLO, pt=9, bold=True,
            al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
        if i < 4:
            freccia(sl, x + 2.3, 5.8, x + 2.5, 5.8)
        x += 2.5
    txt(sl, 0.5, 6.25, 12.2, 0.5, 'i primi tre passi si ripetono per ciascun gemello, nell’ordine '
        'in cui la web app li completa; recupero e definizione valgono per il parto', pt=9,
        col=MUTED, it=True)

    # 10 che cosa sparisce
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Che cosa cambia nel documento', 'Le regole di sostanza restano; cambia la '
           'superficie con cui le si esercita')
    tabella(sl, 0.4, 1.25, 12.5, [
        ['Nella v0.9', 'Nella proposta'],
        ['Riepilogo gemelli (caso 1 e caso 2)', 'testata + card prima dell’azione iniziale'],
        ['Finestra di raccordo (3 apparizioni)', 'le card: numero in grande, idAnsc evidenziato; '
         'RIEPILOGO NUMERI per la stampa'],
        ['Procedura DEFINISCI (6 passi a pagina intera)', 'pulsanti della card attiva'],
        ['Pratica guidata del caso 2', 'card del caso 2 + COPIA TESTO nel pannello del testo'],
        ['Schermata «DEFINISCI in corso»', 'messaggio e RIPROVA / VERIFICA IN ANSC sulla card'],
        ['Esito del parto', 'tutte le card in verde; la pagina resta consultabile'],
        ['Pagina di ripresa', 'nessuna: l’apertura legge store e ANSC e riparte'],
        ['Testo in sola lettura dentro i passi', 'pannello di destra, modificabile fino all’invio'],
        ['Restano invariati', 'numeri in blocco, prenotazione con l’UC specifico, abbinamento per '
         'numero, un gemello alla volta, testo di SIPO in composizioneCompleta, ANSC_SOGGETTO_ATTO, '
         'righe dello store, rinuncia'],
    ], [4.3, 8.2], pt=10, h_riga=0.5)

    # 11 nuovo indice
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Il nuovo indice del capitolo 7', 'Proposta')
    txt(sl, 0.6, 1.3, 7.0, 5.8, [
        ('7  La modalità di integrazione', {'bold': True, 'pt': 14}),
        ('7.1  Il principio: una pagina per il parto, il caso dall’UC', {'pt': 12}),
        ('7.2  La pagina «Gemelli del parto»', {'pt': 12}),
        ('        La testata · Le card dei gemelli · Il testo dell’atto', {'pt': 10, 'col': MUTED}),
        ('7.3  Le azioni di parto', {'pt': 12}),
        ('7.4  Il caso 1: i pulsanti della card, stato per stato', {'pt': 12}),
        ('7.5  Il caso 2: i pulsanti della card e il recupero', {'pt': 12}),
        ('7.6  Il testo dell’atto: composizione, modifica, invio, conservazione', {'pt': 12}),
        ('7.7  Errori, interruzione e ripresa', {'pt': 12}),
        ('7.8  Nato morto e nato vivo poi deceduto', {'pt': 12}),
        ('7.9  Punti di intervento su SIPO', {'pt': 12}),
        ('7.10 Effetti sul disegno (ANSC_SOGGETTO_ATTO, righe dello store) — invariati',
         {'pt': 12, 'col': MUTED}),
    ])
    box(sl, 8.0, 1.3, 4.9, 3.0, [('Figure previste', {'bold': True, 'pt': 13}),
                                 ('• la pagina nel caso 1 e nel caso 2', {'pt': 11}),
                                 ('• la card, con la legenda', {'pt': 11}),
                                 ('• il percorso sulla pagina (in PowerPoint)', {'pt': 11}),
                                 ('• diagramma a stati della card', {'pt': 11}),
                                 ('Spariscono le due sequenze di schermate e le figure del '
                                  'raccordo, della pratica guidata e della ripresa.',
                                  {'pt': 10, 'col': MUTED})],
        fill=GRIGIO_F, line=GRIGIO, marg=0.15)

    # 12 domande
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Domande prima di riscrivere', 'Le risposte cambiano la pagina')
    elenco(sl, 0.4, 1.3, 12.5, 5.9, [
        ('1. La «nuova strategia» è questa pagina unica?', 'O c’è dell’altro (per esempio un '
         'cambio nel modo di prenotare o di dividere) che non ho colto?'),
        ('2. Testo modificabile: dove si salva?', 'Oggi SIPO non conserva il testo (GTT_TMP_ATTO è '
         'temporanea) e /finalizzaAtto rigenera il PDF dal formulario. Un testo modificato va '
         'conservato (colonna o tabella nuova) e la definizione deve usarlo, altrimenti PDF di SIPO '
         'e atto ANSC divergono.'),
        ('3. Caso 2: recupero e definizione per gemello o per parto?', 'Propongo RECUPERA anche '
         'sulla card e DEFINISCI GEMELLI di parto, come oggi in SIPO. In alternativa: definizione '
         'gemello per gemello, come nel caso 1.'),
        ('4. Caso 1: la prenotazione resta un’azione di testata?', 'Oppure il primo VALIDA del '
         'gemello 1 stacca i numeri e prenota (un pulsante in meno, ma un effetto meno visibile).'),
        ('5. Card attiva una sola?', 'La guida ANSC chiede un gemello alla volta: propongo di '
         'disattivare i pulsanti delle altre card (restano selezionabili per testo e stampa).'),
        ('6. Firma del dichiarante solo cartacea anche nel caso 1?', 'La guida lo dice per la web '
         'app (p. 45); sui servizi cooperativi nessuna fonte. Propongo [DA VERIFICARE] + punto '
         'aperto.'),
    ], pt=13)

    prs.save(OUT)
    return OUT


if __name__ == '__main__':
    print(costruisci())
