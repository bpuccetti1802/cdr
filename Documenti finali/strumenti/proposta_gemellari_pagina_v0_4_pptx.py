# -*- coding: utf-8 -*-
"""Proposta per il capitolo 7 dell'analisi delle nascite gemellari, v0.4 (22/11/2026).

Recepisce le richieste dell'utente sulla v0.3:
  1. i passi della card (Valida, Firma dichiaranti, Conformità, Firma USC) sono PULSANTI che
     aprono una modale; solo «Salvato in SIPO» è un chip;
  2. i dichiaranti possono essere uno, due o nessuno: la firma si chiede nella modale;
  3. la conformità è cliccabile solo se c'è almeno una firma su carta;
  4. la firma dell'USC avviene in una modale;
  5. caso 2: card con più informazioni sui gemelli e modale di dettaglio con tutti i dati che
     servono a compilare a mano la bozza sulla web app (sezioni del mapping Dic_Nasc_999);
  6. le modali sono disegnate una per una.
Il dimostratore HTML per gli sviluppatori è a parte: DIMOSTRATORE_Pagina-Gemelli_SIPO-ANSC_v0.1.html.

    /Library/Developer/CommandLineTools/usr/bin/python3 proposta_gemellari_pagina_v0_4_pptx.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import proposta_gemellari_pagina_pptx as P                          # noqa: E402
from proposta_gemellari_pagina_pptx import (box, txt, freccia, titolo, elenco, btn, pill,  # noqa
                                            tabella, testata, pannello_testo, rgb, ROSSO,
                                            ROSSO_F, INK, MUTED, GRIGIO, GRIGIO_F, VERDE,
                                            VERDE_F, BLU, BLU_F, GIALLO, GIALLO_F, BIANCO, EVID)

OUT = os.path.join(os.path.dirname(P.OUT), 'PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.4.pptx')

STATI = {
    'bozza': ('BOZZA (prenotato)', BLU, BLU_F),
    'conf': ('CONFERMATO', ROSSO, ROSSO_F),
    'fdich': ('FIRMATO DAL DICHIARANTE', ROSSO, ROSSO_F),
    'fconf': ('FIRMATO PER CONFORMITÀ', ROSSO, ROSSO_F),
    'usc': ('FIRMATO DA USC', VERDE, VERDE_F),
    'wa': ('BOZZA · ATTESA WEBAPP', GIALLO, GIALLO_F),
    'rec': ('FIRMATO DA USC · DA AGGIORNARE', VERDE, VERDE_F),
}
COMANDI_TESTATA = [('RIEPILOGO NUMERI', True, False), ('CANCELLA PRATICA', True, False)]

# stato di un passo: 'fatto' · 'attivo' (primario) · 'abil' · 'disab' · 'nonserve'
def passo(sl, x, y, w, t, st, h=0.28):
    if st == 'fatto':
        return box(sl, x, y, w, h, '✓ ' + t, fill=VERDE_F, line=VERDE, col=VERDE, pt=7,
                   bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
                   forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.01)
    if st == 'nonserve':
        return box(sl, x, y, w, h, t + ' · non serve', fill=BIANCO, line=GRIGIO, col=GRIGIO,
                   pt=6, it=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
                   forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.01, dash=True)
    return btn(sl, x, y, w, t, st != 'disab', st == 'attivo', h=h, pt=7)


def chip(sl, x, y, w, fatto, errore=False, h=0.24):
    if errore:
        return pill(sl, x, y + 0.02, w, 'Non salvato in SIPO', ROSSO, ROSSO_F, h=h)
    if fatto:
        return pill(sl, x, y + 0.02, w, '● Salvato in SIPO', VERDE, VERDE_F, h=h)
    return pill(sl, x, y + 0.02, w, '○ Salvato in SIPO', GRIGIO, BIANCO, h=h)


def idansc(sl, x, y, w, ida, pt=8):
    a, b, cc, d = ida.split('-')
    s = box(sl, x, y, w, 0.22, '', fill=None, line=None, marg=0.01)
    p = s.text_frame.paragraphs[0]
    for t, ev in (('idAnsc  ' + a + '-' + b + '-', False), (cc, True), ('-' + d, False)):
        r = p.add_run()
        r.text = t
        r.font.size = Pt(pt)
        r.font.name = 'Courier New'
        r.font.bold = ev
        r.font.color.rgb = rgb(INK)
        if ev:
            from lxml import etree
            rpr = r._r.get_or_add_rPr()
            hl = etree.SubElement(rpr, '{http://schemas.openxmlformats.org/drawingml/2006/main}'
                                       'highlight')
            clr = etree.SubElement(hl, '{http://schemas.openxmlformats.org/drawingml/2006/main}'
                                       'srgbClr')
            clr.set('val', EVID)


def card4(sl, x, y, w, h, g, stato, passi, secondari=(), sel=False, nota=None, info=None,
          salvato=False, errore=False):
    """g = (pos, nome, sesso, tipologia, uc, numero, idAnsc)."""
    pos, nome, sesso, tip, uc, num, ida = g
    lab, c, f = STATI[stato]
    box(sl, x, y, w, h, fill='fffafb' if sel else BIANCO, line=ROSSO if sel else GRIGIO,
        lw=2.25 if sel else 0.75, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(sl, x + 0.1, y + 0.05, 2.4, 0.25, 'Gemello ' + pos + ' · ' + sesso, pt=10, bold=True)
    pill(sl, x + w - 2.25, y + 0.06, 2.15, lab, c, f)
    txt(sl, x + 0.1, y + 0.28, w - 1.4, 0.2, nome, pt=8, col=MUTED)
    txt(sl, x + 0.1, y + 0.45, w - 1.4, 0.2, tip + ' · UC ' + uc, pt=8, col=MUTED)
    dy = 0
    if info:
        txt(sl, x + 0.1, y + 0.62, w - 1.4, 0.2, info, pt=7, col=INK)
        dy = 0.15
    txt(sl, x + w - 1.25, y + 0.3, 1.15, 0.18, 'n. comunale', pt=7, col=MUTED, al=PP_ALIGN.RIGHT)
    txt(sl, x + w - 1.25, y + 0.42, 1.15, 0.4, num, pt=20, bold=True, col=ROSSO,
        al=PP_ALIGN.RIGHT)
    idansc(sl, x + 0.1, y + 0.66 + dy, w - 1.4, ida)
    # passi: pulsanti + chip finale
    yb = y + 0.95 + dy
    wc = 1.15
    pw = (w - 0.2 - wc - 0.05) / len(passi)
    for i, (t, st) in enumerate(passi):
        passo(sl, x + 0.1 + i * pw, yb, pw - 0.05, t, st)
    chip(sl, x + w - 0.1 - wc, yb, wc, salvato, errore)
    xb = x + 0.1
    for t in secondari:
        bw = 0.2 + 0.07 * len(t)
        box(sl, xb, y + h - 0.3, bw, 0.22, t, fill=None, line=None, col=BLU, pt=7, bold=True,
            al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, marg=0.01)
        xb += bw + 0.05
    if nota:
        txt(sl, xb + 0.05, y + h - 0.3, x + w - xb - 0.15, 0.22, nota, pt=7, col=MUTED, it=True,
            anc=MSO_ANCHOR.MIDDLE)


# ───────────────────────────────────────────── primitive delle modali
def sfondo(sl, etichetta='la pagina dei gemelli, oscurata'):
    box(sl, 0.3, 1.15, 8.55, 6.2, fill='cfcfcf', line=None)
    txt(sl, 0.4, 1.2, 4, 0.2, etichetta, pt=7, col='7a7a7a', it=True)


def modale(sl, tit, sotto=None, x=0.6, y=1.4, w=7.95, h=5.75):
    box(sl, x + 0.04, y + 0.04, w, h, fill='9a9a9a', line=None)
    box(sl, x, y, w, h, fill=BIANCO, line=GRIGIO)
    box(sl, x, y, w, 0.42, tit, fill=ROSSO, line=None, col=BIANCO, pt=11, bold=True,
        anc=MSO_ANCHOR.MIDDLE, marg=0.12)
    txt(sl, x + w - 0.35, y + 0.07, 0.3, 0.3, '✕', pt=12, bold=True, col=BIANCO)
    if sotto:
        txt(sl, x + 0.12, y + 0.47, w - 0.24, 0.22, sotto, pt=8, col=MUTED)
    return x, y, w, h


def piede(sl, m, bottoni, nota=None):
    x, y, w, h = m
    box(sl, x, y + h - 0.5, w, 0.005, fill=GRIGIO, line=None)
    xb = x + w - 0.12
    for t, att, prim in reversed(bottoni):
        bw = 0.25 + 0.075 * len(t)
        xb -= bw
        btn(sl, xb, y + h - 0.4, bw, t, att, prim, h=0.28)
        xb -= 0.1
    if nota:
        txt(sl, x + 0.12, y + h - 0.42, xb - x - 0.2, 0.32, nota, pt=7, col=MUTED, it=True,
            anc=MSO_ANCHOR.MIDDLE)


def sezione(sl, x, y, w, t):
    txt(sl, x, y, w, 0.22, t, pt=9, bold=True, col=ROSSO)
    box(sl, x, y + 0.22, w, 0.005, fill=ROSSO_F, line=None)


def campo(sl, x, y, w, etich, valore, copia=False, we=1.6, pt=8, h=0.22):
    txt(sl, x, y, we, h, etich, pt=pt - 1, col=MUTED)
    box(sl, x + we, y, w - we - (0.3 if copia else 0), h, valore, fill='fafafa', line='dddddd',
        pt=pt, marg=0.04, anc=MSO_ANCHOR.MIDDLE)
    if copia:
        box(sl, x + w - 0.26, y, 0.26, h, '⧉', fill=BIANCO, line=ROSSO, col=ROSSO, pt=8,
            al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE, marg=0)


def note(sl, voci, y=1.25, pt=10):
    elenco(sl, 9.05, y, 4.0, 6.1, voci, pt=pt)


def radio(sl, x, y, t, on=False, pt=8):
    box(sl, x, y + 0.04, 0.13, 0.13, '', fill=ROSSO if on else BIANCO, line=ROSSO,
        forma=MSO_SHAPE.OVAL)
    txt(sl, x + 0.17, y, 2.6, 0.22, t, pt=pt, bold=on)


def spunta(sl, x, y, t, on=True, pt=8, fisso=False, w=4.5):
    box(sl, x, y + 0.04, 0.14, 0.14, '✓' if on else '', fill=GRIGIO_F if fisso else BIANCO,
        line=GRIGIO if fisso else ROSSO, col=ROSSO, pt=7, bold=True, al=PP_ALIGN.CENTER,
        anc=MSO_ANCHOR.MIDDLE, marg=0)
    txt(sl, x + 0.2, y, w, 0.22, t, pt=pt)


# ───────────────────────────────────────────── dati del dimostratore
G1 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13617",
       "2026-10527618-13617-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13618",
       "2026-10527619-13618-058091"),
      ("3", "NATO 3 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13619",
       "2026-10527620-13619-058091"))
G2 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11999999 (servizio)", "13640",
       "2026-10531102-13640-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "2 nato morto", "11999999 (servizio)", "13641",
       "2026-10531103-13641-058091"),
      ("3", "NATO 3 — COGNOME NOME", "M", "3 nato vivo poi deceduto", "11999999 (servizio)",
       "13642", "2026-10531104-13642-058091"))
P1 = ['Valida', 'Firma dichiaranti', 'Conformità', 'Firma USC']
P2 = ['Dati per la web app', 'Web app', 'Recupera da ANSC', 'Aggiorna SIPO']


def passi(nomi, stati):
    return list(zip(nomi, stati))


# ───────────────────────────────────────────── slide
def s_richieste(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Che cosa cambia rispetto alla v0.3', 'Le richieste del 22/11 e come sono recepite')
    tabella(sl, 0.4, 1.25, 12.5, [
        ['Richiesta', 'Come è recepita'],
        ['I passi della card sono pulsanti che aprono una modale',
         'Valida, Firma dichiaranti, Conformità e Firma USC sono pulsanti; l’azione e i dati '
         'specifici stanno nella modale. Il pulsante del passo di turno è il primario.'],
        ['Solo «Salvato in SIPO» è un chip', 'chip in coda ai passi: grigio finché /finalizzaAtto '
         'non riesce, verde dopo, rosso se il salvataggio automatico non riesce'],
        ['Dichiaranti: uno, due o nessuno; la firma si chiede nella modale',
         'la modale elenca i dichiaranti raccolti nel Riepilogo e per ciascuno chiede la firma '
         'elettronica (R012) o su carta (R006); senza dichiaranti lo dice e si prosegue'],
        ['Conformità cliccabile solo con firme su carta',
         'il pulsante si abilita se almeno un dichiarante ha firmato su carta; altrimenti '
         'compare «Conformità · non serve» e la firma USC si apre subito'],
        ['Firma dell’USC in una modale', 'riepilogo, anteprima ANSC, credenziali di firma '
         'remota, poi firma (R007) e salvataggio in SIPO, mostrati in sequenza'],
        ['Caso 2: più informazioni sui gemelli', 'la card mostra nascita, ora, luogo e posizione '
         'nel parto; la modale «Dati per la web app» riporta, sezione per sezione, i campi '
         'del caso di servizio 11999999 con il pulsante per copiarli'],
        ['Dimostratore HTML', 'un solo file, senza dipendenze, con le due pagine, le card e '
         'tutte le modali funzionanti su dati fittizi e il registro delle chiamate simulate'],
    ], [3.6, 8.9], pt=10, h_riga=0.62)


def s_card(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'La card: passi come pulsanti, chip finale',
           'Che cosa abilita ciascun pulsante · la card è lavorabile se di turno o selezionata e '
           'non firmata dall’USC')
    card4(sl, 0.4, 1.3, 6.3, 1.55, G1[1], 'fdich',
          passi(P1, ['fatto', 'fatto', 'attivo', 'disab']), secondari=('STAMPA',),
          nota='una firma su carta: serve la conformità')
    card4(sl, 0.4, 3.0, 6.3, 1.55, G1[0], 'fdich',
          passi(P1, ['fatto', 'fatto', 'nonserve', 'attivo']), secondari=('STAMPA',),
          nota='firma elettronica: la conformità non serve')
    card4(sl, 0.4, 4.7, 6.3, 1.55, G1[2], 'usc',
          passi(P1, ['fatto', 'fatto', 'nonserve', 'fatto']),
          secondari=('APRI IL PDF', 'STAMPA'), salvato=True)
    tabella(sl, 6.95, 1.3, 6.0, [
        ['Pulsante', 'Si abilita quando', 'Apre'],
        ['Valida', 'BOZZA (prenotato), anche dopo TORNA AI DATI', 'Validazione · R001 + R009'],
        ['Firma dichiaranti', 'CONFERMATO', 'Firma dei dichiaranti · R012 o R006'],
        ['Conformità', 'FIRMATO DAL DICHIARANTE e almeno una firma su carta',
         'Attestazione di conformità · R010 + R007'],
        ['Firma USC', 'FIRMATO PER CONFORMITÀ, o FIRMATO DAL DICHIARANTE senza firme su carta',
         'Firma dell’USC · R007, poi /finalizzaAtto'],
        ['chip Salvato in SIPO', 'non è un pulsante: si accende a /finalizzaAtto riuscita',
         '—'],
    ], [1.35, 2.6, 2.05], pt=8, h_riga=0.5)
    txt(sl, 6.95, 4.55, 6.0, 1.9, [
        ('Passo fatto: verde con la spunta, non più cliccabile (si riapre solo con TORNA AI DATI '
         'dalla modale di firma).', {'pt': 9}),
        ('Azioni secondarie, come collegamenti: STAMPA · APRI IL PDF · TORNA AI DATI · VERIFICA '
         'IN ANSC (esito incerto).', {'pt': 9}),
        ('Chip rosso «Non salvato in SIPO»: la card offre RIPROVA IL SALVATAGGIO (punto E).',
         {'pt': 9, 'col': MUTED})])


def s_mockup_1(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Caso 1 · stesso UC', 'Gemello 1 concluso · gemello 2 validato, in attesa della '
           'firma dei dichiaranti · gemello 3 in bozza')
    testata(sl, 1.15, '1 · stesso UC · numeri staccati e atti prenotati alla divisione',
            COMANDI_TESTATA)
    y0, h = 2.3, 1.6
    card4(sl, 0.3, y0, 6.0, h, G1[0], 'usc', passi(P1, ['fatto', 'fatto', 'nonserve', 'fatto']),
          secondari=('APRI IL PDF', 'STAMPA'), salvato=True, nota='2 DEFINITO il 18/11 alle 12.10')
    card4(sl, 0.3, y0 + h + 0.08, 6.0, h, G1[1], 'conf',
          passi(P1, ['fatto', 'attivo', 'disab', 'disab']), secondari=('STAMPA',), sel=True,
          nota='2 dichiaranti (dal Riepilogo)')
    card4(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G1[2], 'bozza',
          passi(P1, ['abil', 'disab', 'disab', 'disab']), secondari=('STAMPA',),
          nota='lavorabile in qualsiasi ordine')
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO con gli idAnsc dei fratelli · inviato con la validazione '
                   '(composizioneCompleta) · validato: non più modificabile',
                   '13618', [('STAMPA', True, False), ('ANTEPRIMA ANSC (R010)', True, False),
                             ('SALVA TESTO', False, False)], bloccato=True,
                   nota='Per modificarlo: TORNA AI DATI dalla modale di firma dei dichiaranti.')


def s_valida(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Modale «Validazione»', 'Si apre da Valida · caso 1')
    sfondo(sl)
    m = modale(sl, 'Validazione · gemello 3 · n. 13619',
               'Atto prenotato 2026-10527620-13619-058091 · UC 11111000 · si inviano ad ANSC i '
               'documenti e poi l’atto con il suo testo')
    x, y, w, _ = m
    sezione(sl, x + 0.15, y + 0.75, w - 0.3, 'Che cosa si invia')
    tabella(sl, x + 0.15, y + 1.05, w - 0.3, [
        ['Elemento', 'Origine', 'Stato'],
        ['Dati dell’atto', 'pratica SIPO · UC 11111000', 'pronto'],
        ['Testo dell’atto (composizioneCompleta)', 'campo della tabella dei gemelli · salvato '
         'alle 11.02', 'pronto'],
        ['Attestazione di nascita · PDF', 'Riepilogo', 'inviato · Inserito (R001)'],
        ['Documento del dichiarante · PDF', 'Riepilogo', 'inviato · Inserito (R001)'],
        ['Delega · PDF', 'Riepilogo', 'in verifica antivirus…'],
        ['Firmatari: padre, madre', 'Riepilogo', 'nel modello evento'],
    ], [3.1, 2.6, 1.95], pt=8, h_riga=0.3)
    sezione(sl, x + 0.15, y + 3.3, w - 0.3, 'Esito di ANSC (R009)')
    box(sl, x + 0.15, y + 3.6, w - 0.3, 1.5, [
        ('Anomalie superabili · forcingCode restituito', {'bold': True, 'pt': 9, 'col': GIALLO}),
        ('W  · evento.datiDiNascita.oraNascita · ora di nascita successiva a quella del '
         'gemello successivo', {'pt': 8}),
        ('Errori bloccanti: nessuno', {'pt': 8, 'col': MUTED}),
        ('L’USC può forzare: seconda chiamata R009 con il forcingCode. Gli altri ruoli tornano '
         'ai dati.', {'pt': 8, 'col': MUTED, 'it': True})],
        fill=GIALLO_F, line=GIALLO, marg=0.1)
    piede(sl, m, [('ANNULLA', True, False), ('FORZA LA VALIDAZIONE', True, False),
                  ('VALIDA', True, True)],
          nota='Esito positivo: CONFERMATO, la modale si chiude')
    note(sl, [('Sequenza.', 'R001 per ogni documento non ancora in ANSC, attesa dello stato '
               '«Inserito» (ANSC_08), poi R009 /validazione/evento sull’atto prenotato.'),
              ('Testo.', 'Va in composizioneCompleta; dopo la validazione non si modifica più.'),
              ('Esito.', 'Positivo → CONFERMATO. Errori → si resta in BOZZA, con l’elenco. '
               'Anomalie superabili → FORZA LA VALIDAZIONE, solo per l’USC.'),
              ('Esito incerto.', 'La modale non ripete R009: VERIFICA IN ANSC (R005).')])


def s_firma_dich(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Modale «Firma dei dichiaranti»', 'Si apre da Firma dichiaranti · uno, due o '
           'nessun dichiarante, come raccolti nel Riepilogo')
    sfondo(sl)
    m = modale(sl, 'Firma dei dichiaranti · gemello 2 · n. 13618',
               'Dichiaranti dal Riepilogo: 2 · ciascuno firma in modo elettronico o su carta')
    x, y, w, _ = m
    for k, (chi, el, stato, col) in enumerate((
            ('Padre · COGNOME NOME · CF ****************', True,
             'Link inviato a p****@****.it alle 11.20 · in attesa della presa visione', GIALLO),
            ('Madre · COGNOME NOME · CF ****************', False,
             'Modulo stampato · file firmato caricato: firma_madre.pdf', VERDE))):
        yy = y + 0.8 + k * 1.75
        box(sl, x + 0.15, yy, w - 0.3, 1.6, fill='fbfbfb', line=GRIGIO)
        txt(sl, x + 0.25, yy + 0.06, 5, 0.22, chi, pt=9, bold=True)
        radio(sl, x + 0.25, yy + 0.35, 'Firma elettronica (R012)', el)
        radio(sl, x + 3.2, yy + 0.35, 'Firma su carta (R006)', not el)
        if el:
            campo(sl, x + 0.25, yy + 0.65, 4.8, 'Email del dichiarante', 'p****@****.it', we=1.4)
            btn(sl, x + 5.15, yy + 0.65, 1.0, 'INVIA LINK', False, h=0.22, pt=7)
            btn(sl, x + 6.2, yy + 0.65, 1.3, 'AGGIORNA STATO', True, h=0.22, pt=7)
        else:
            btn(sl, x + 0.25, yy + 0.65, 1.4, 'STAMPA MODULO', True, h=0.22, pt=7)
            btn(sl, x + 1.75, yy + 0.65, 1.9, 'CARICA FILE FIRMATO', True, h=0.22, pt=7)
        pill(sl, x + 0.25, yy + 1.05, w - 0.6, stato, col,
             GIALLO_F if col == GIALLO else VERDE_F, pt=7, h=0.24)
        txt(sl, x + 0.25, yy + 1.32, w - 0.5, 0.22,
            'ANNULLA LINK (R012 annulla-link) · cambia modalità' if el else
            'Il file copre tutti i dichiaranti su carta (listaFirmatari di R006)',
            pt=7, col=MUTED, it=True)
    txt(sl, x + 0.15, y + 4.35, w - 0.3, 0.6, [
        ('Con una firma su carta si abilita la Conformità.', {'pt': 8, 'bold': True}),
        ('Nessun dichiarante: la modale lo dice e CONFERMA porta subito alla firma dell’USC.',
         {'pt': 8, 'col': MUTED})])
    piede(sl, m, [('TORNA AI DATI', True, False), ('ANNULLA', True, False),
                  ('CONFERMA LE FIRME', False, False)],
          nota='Si abilita a firme complete')
    note(sl, [('Firma elettronica.', 'R012 invio-email: un link per dichiarante; lo stato si '
               'legge con pooling-statoatto (0 da visionare, 1 visionato, 2 annullato).'),
              ('Firma su carta.', 'Modulo stampato da SIPO, firmato in sala, caricato con R006 '
               'insieme all’elenco dei firmatari.'),
              ('Esito.', 'FIRMATO DAL DICHIARANTE. Con almeno una firma su carta si abilita '
               'Conformità; altrimenti Firma USC.'),
              ('TORNA AI DATI.', 'Riporta l’atto in bozza per una nuova validazione; dopo una '
               'firma solo se tutti i firmatari possono firmare di nuovo.'),
              ('Da verificare (H).', 'Se ANSC ammetta elettronica e carta sullo stesso atto, e '
               'come tratti l’atto senza dichiaranti.')], pt=9)


def s_conformita(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Modale «Attestazione di conformità»', 'Si apre da Conformità · solo se almeno '
           'un dichiarante ha firmato su carta')
    sfondo(sl)
    m = modale(sl, 'Attestazione di conformità · gemello 2 · n. 13618',
               'L’USC attesta che le copie per immagine dei documenti cartacei sono conformi '
               'agli originali')
    x, y, w, _ = m
    sezione(sl, x + 0.15, y + 0.75, w - 0.3, 'Documenti inclusi nell’attestazione')
    for k, (t, on, fisso) in enumerate((
            ('Modulo firmato dalla madre (R006) · firma_madre.pdf · sempre incluso', True, True),
            ('Attestazione di nascita · PDF', True, False),
            ('Documento del dichiarante · PDF', True, False),
            ('Delega · P7M · già firmato digitalmente', False, False))):
        spunta(sl, x + 0.25, y + 1.08 + k * 0.28, t, on, fisso=fisso, w=6.8)
    btn(sl, x + 0.25, y + 2.3, 2.6, 'ANTEPRIMA ATTESTAZIONE (R010)', True, h=0.26, pt=7)
    sezione(sl, x + 0.15, y + 2.75, w - 0.3, 'Firma remota dell’USC')
    campo(sl, x + 0.25, y + 3.08, 4.6, 'Utente di firma', 'utente.firma', we=1.5)
    campo(sl, x + 0.25, y + 3.36, 4.6, 'PIN', '••••••', we=1.5)
    campo(sl, x + 0.25, y + 3.64, 4.6, 'OTP di firma', '', we=1.5)
    txt(sl, x + 5.0, y + 3.08, 2.8, 0.8, 'Credenziali del servizio di firma remota: non sono '
        'l’OTP della sessione ANSC in testata.', pt=7, col=MUTED, it=True)
    piede(sl, m, [('ANNULLA', True, False), ('FIRMA PER CONFORMITÀ', True, True)],
          nota='Esito: FIRMATO PER CONFORMITÀ, si abilita Firma USC')
    note(sl, [('Servizi.', 'R010 /anteprima/attestazione per vedere l’attestazione; R007 '
               '/attestazione/firma con gli allegati e il loro flagAttConformita.'),
              ('Selezione.', 'Il modulo firmato su carta è sempre incluso. Gli altri documenti '
               'sono preselezionati; l’USC può escluderli (i P7M sono già firmati).'),
              ('Credenziali.', 'Inviate in base64: la modalità «in chiaro» non è accettata in '
               'produzione.'),
              ('Senza firme su carta', 'questa modale non si apre: il pulsante mostra '
               '«Conformità · non serve».')], pt=10)


def s_firma_usc(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Modale «Firma dell’USC»', 'Si apre da Firma USC · firma l’atto in ANSC e lo '
           'salva in SIPO, senza altri pulsanti')
    sfondo(sl)
    m = modale(sl, 'Firma dell’USC · gemello 2 · n. 13618',
               'Dopo la firma l’atto è formato: non si torna più ai dati')
    x, y, w, _ = m
    sezione(sl, x + 0.15, y + 0.75, w - 0.3, 'L’atto')
    for k, (e, v) in enumerate((('Numero comunale', '13618 · parte I · serie A'),
                                ('idAnsc', '2026-10527619-13618-058091'),
                                ('Intestatario', 'NATO 2 — COGNOME NOME · F · 1 nato vivo'),
                                ('Firme raccolte', 'padre (elettronica) · madre (su carta) · '
                                                   'conformità'))):
        campo(sl, x + 0.25, y + 1.05 + k * 0.27, w - 0.5, e, v, we=1.6)
    btn(sl, x + 0.25, y + 2.2, 2.2, 'ANTEPRIMA ATTO (R010)', True, h=0.26, pt=7)
    spunta(sl, x + 2.6, y + 2.22, 'Ho letto il testo dell’atto', True, w=3)
    sezione(sl, x + 0.15, y + 2.65, w - 0.3, 'Firma remota dell’USC')
    campo(sl, x + 0.25, y + 2.98, 4.6, 'Utente di firma', 'utente.firma', we=1.5)
    campo(sl, x + 0.25, y + 3.26, 4.6, 'PIN', '••••••', we=1.5)
    campo(sl, x + 0.25, y + 3.54, 4.6, 'OTP di firma', '482 913', we=1.5)
    sezione(sl, x + 0.15, y + 3.95, w - 0.3, 'Avanzamento')
    for k, (t, c, f) in enumerate((('1 · Firma in ANSC (R007) · FIRMATO DA USC', VERDE, VERDE_F),
                                   ('2 · Salvataggio in SIPO (/finalizzaAtto) · 2 DEFINITO',
                                    VERDE, VERDE_F))):
        pill(sl, x + 0.25 + k * 3.75, y + 4.28, 3.6, '✓ ' + t, c, f, pt=7, h=0.26)
    txt(sl, x + 0.25, y + 4.6, w - 0.5, 0.3, 'Se il salvataggio non riesce: l’atto resta '
        'FIRMATO DA USC, chip rosso e RIPROVA IL SALVATAGGIO (punto E).', pt=7, col=MUTED, it=True)
    piede(sl, m, [('ANNULLA', True, False), ('FIRMA L’ATTO', True, True)])
    note(sl, [('Servizi.', 'R010 /anteprima/evento con presaVisione; R007 /firma_usc con i '
               'parametri di firma; poi /finalizzaAtto da sé.'),
              ('Avanzamento.', 'I due passi si vedono nella modale; alla fine la modale si '
               'chiude e il chip della card diventa verde.'),
              ('Esito incerto della firma.', 'Niente nuova firma alla cieca: VERIFICA IN ANSC '
               '(R005) legge lo stato.'),
              ('PDF.', 'Generato da SIPO con il testo salvato: è lo stesso testo inviato ad '
               'ANSC.')], pt=10)


def s_mockup_2(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Caso 2 · UC diversi', 'Card con più informazioni · gemello 1 recuperato · '
           'gemello 2 selezionato · gemello 3 da fare')
    testata(sl, 1.15, '2 · UC diversi · numeri e prenotazione (11999999) alla divisione',
            COMANDI_TESTATA)
    y0, h = 2.3, 1.65
    inf = ('nato il 18/11/2026 alle 10.41 · Policlinico · 1° di 3 · 2 documenti · dichiarante '
           'il padre', 'nata il 18/11/2026 alle 10.43 · Policlinico · 2° di 3 · certificato '
           'medico · dichiarante il padre', 'nato il 18/11/2026 alle 10.46 · Policlinico · 3° di '
           '3 · certificato medico · dichiarante il padre')
    card4(sl, 0.3, y0, 6.0, h, G2[0], 'rec', passi(P2, ['fatto', 'fatto', 'fatto', 'attivo']),
          secondari=('DETTAGLIO',), info=inf[0], nota='3 differenze da riportare')
    card4(sl, 0.3, y0 + h + 0.06, 6.0, h, G2[1], 'wa', passi(P2, ['fatto', 'attivo', 'abil',
                                                                  'disab']),
          secondari=('DETTAGLIO', 'COPIA TESTO'), info=inf[1], sel=True)
    card4(sl, 0.3, y0 + 2 * (h + 0.06), 6.0, h, G2[2], 'wa',
          passi(P2, ['attivo', 'abil', 'abil', 'disab']), secondari=('DETTAGLIO', 'COPIA TESTO'),
          info=inf[2])
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.12, 'Testo dell’atto · gemello 2',
                   'composto da SIPO come nel caso 1 · da incollare nella composizione libera '
                   'della bozza prenotata, sulla web app',
                   '13641', [('COPIA TESTO', True, True), ('STAMPA', True, False),
                             ('SALVA TESTO', True, False)],
                   nota='Gli idAnsc dei fratelli sono noti dalla prenotazione.',
                   nascita='è nata morta una bambina',
                   fratelli='Gli atti dei fratelli: 2026-10531102-13640-058091 (precedente), '
                            '2026-10531104-13642-058091 (successivo).')


def s_dati_webapp(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Modale «Dati per la web app»', 'Si apre da Dati per la web app o da DETTAGLIO · '
           'le sezioni del caso di servizio 11999999, nell’ordine della web app')
    sfondo(sl)
    m = modale(sl, 'Dati per la web app · gemello 2 · n. 13641',
               'Bozza prenotata 2026-10531103-13641-058091 · UC 11999999 · ogni valore si copia '
               'con ⧉', h=5.85)
    x, y, w, _ = m
    # linguette delle sezioni
    lin = ['Formazione', 'Dati generali', 'Soggetto', 'Madre', 'Padre', 'Dichiarante',
           'Composizione', 'Allegati']
    xl = x + 0.15
    for i, t in enumerate(lin):
        lw = 0.25 + 0.07 * len(t)
        box(sl, xl, y + 0.75, lw, 0.24, t, fill=ROSSO if i < 3 else BIANCO,
            line=ROSSO, col=BIANCO if i < 3 else ROSSO, pt=7, bold=True, al=PP_ALIGN.CENTER,
            anc=MSO_ANCHOR.MIDDLE, marg=0.01)
        xl += lw + 0.04
    c1, c2, cw = x + 0.15, x + 4.05, 3.75
    sezione(sl, c1, y + 1.1, cw, 'Formazione atto')
    for k, (e, v) in enumerate((('Numero comunale', '13641'), ('Data formazione', '18/11/2026'),
                                ('Ora · minuti', '11 · 20'))):
        campo(sl, c1, y + 1.4 + k * 0.26, cw, e, v, True, we=1.4)
    sezione(sl, c1, y + 2.25, cw, 'Dati generali')
    for k, (e, v) in enumerate((('Tipologia nascita', '2 · nato morto (ANSC_107)'),
                                ('Motivo recupero', '[DA VERIFICARE] (ANSC_96)'),
                                ('Data · ora decorrenza', '18/11/2026 · 10.43'),
                                ('Atto secretato', 'no'))):
        campo(sl, c1, y + 2.55 + k * 0.26, cw, e, v, True, we=1.4)
    sezione(sl, c2, y + 1.1, cw, 'Soggetto (intestatario)')
    for k, (e, v) in enumerate((('Cognome · nome', 'COGNOME · NOME'), ('Sesso', 'F'),
                                ('Data nascita', '18/11/2026'), ('Ora · minuto', '10 · 43'),
                                ('Stato · comune', 'ITALIA · ROMA (RM)'),
                                ('Luogo nascita', 'Policlinico'),
                                ('Assegnazione cognome', 'cognome del padre'))):
        campo(sl, c2, y + 1.4 + k * 0.26, cw, e, v, True, we=1.45)
    sezione(sl, c1, y + 3.7, w - 0.3, 'Nel parto · composizione libera')
    campo(sl, c1, y + 4.0, w - 0.3, 'Posizione nel parto', '2° di 3 · precedente '
          '…-13640-… · successivo …-13642-…', True, we=1.4)
    campo(sl, c1, y + 4.28, w - 0.3, 'Composizione libera', 'L’anno duemilaventisei, addì '
          'diciotto del mese di novembre… (testo intero dal pannello)', True, we=1.4)
    piede(sl, m, [('STAMPA LA SCHEDA', True, False), ('APRI WEB APP', True, False),
                  ('CHIUDI', True, True)],
          nota='Madre, Padre, Dichiarante e Allegati nelle altre linguette')
    note(sl, [('Fonte dei campi.', 'Il mapping ANSC Dic_Nasc_999 (UC 11999999): Formazione atto, '
               'Dati generali, Madre, Padre, Dichiarante, Soggetto, Composizione libera, '
               'Allegati, Formula 999.1.1.'),
              ('Valori.', 'Dalla pratica SIPO dopo la divisione, già nella forma della web app '
               '(descrizioni delle decodifiche, date e ore separate).'),
              ('Allegati.', 'I documenti del Riepilogo, con SCARICA per caricarli sulla web app '
               '(punto D).'),
              ('Da verificare (I).', 'Il motivo di recupero da indicare per i gemelli con UC '
               'diversi.')], pt=10)


def s_recupera(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Modali «Recupera da ANSC» e «Aggiorna SIPO»', 'Caso 2 · due passi distinti '
           '(punto F): prima si vede, poi si scrive')
    m = modale(sl, 'Recupera da ANSC · gemello 1 · n. 13640', 'R005 per idAnsc '
               '2026-10531102-13640-058091', x=0.4, y=1.25, w=6.2, h=5.9)
    x, y, w, _ = m
    sezione(sl, x + 0.15, y + 0.75, w - 0.3, 'Controlli')
    for k, t in enumerate(('Stato in ANSC: FIRMATO DA USC', 'Intestatario: nome e sesso '
                           'coincidono', 'Tipologia di nascita: 1 nato vivo',
                           'Numero comunale nell’idAnsc: 13640')):
        pill(sl, x + 0.25, y + 1.05 + k * 0.28, w - 0.5, '✓ ' + t, VERDE, VERDE_F, pt=7, h=0.24)
    sezione(sl, x + 0.15, y + 2.25, w - 0.3, 'Differenze ANSC → SIPO')
    tabella(sl, x + 0.15, y + 2.55, w - 0.3, [
        ['Campo', 'SIPO', 'ANSC'],
        ['Ora · minuto di nascita', '10 · 41', '10 · 40'],
        ['Precisazione del cognome', '—', 'come da dichiarazione'],
        ['Data formazione', '18/11/2026', '19/11/2026'],
    ], [2.1, 1.5, 2.0], pt=8, h_riga=0.3)
    txt(sl, x + 0.15, y + 3.85, w - 0.3, 0.9, 'Se lo stato non è FIRMATO DA USC: NON FIRMATO, '
        'si torna alla web app. Se l’intestatario non coincide: INCOERENTE, nessuna scrittura.',
        pt=8, col=MUTED, it=True)
    piede(sl, m, [('CHIUDI', True, False), ('AGGIORNA SIPO', True, True)])
    m = modale(sl, 'Aggiorna SIPO da ANSC · gemello 1', 'Scrive sull’atto SIPO i campi '
               'obbligatori in ANSC, poi /finalizzaAtto', x=6.85, y=1.25, w=6.1, h=5.9)
    x, y, w, _ = m
    sezione(sl, x + 0.15, y + 0.75, w - 0.3, 'Che cosa si scrive')
    for k, t in enumerate(('Ora e minuto di nascita: 10 · 40', 'Precisazione del cognome',
                           'Data formazione: 19/11/2026', 'Testo dell’atto: quello firmato '
                           'in ANSC')):
        spunta(sl, x + 0.25, y + 1.05 + k * 0.28, t, True, fisso=True, w=5.3)
    sezione(sl, x + 0.15, y + 2.35, w - 0.3, 'Avanzamento')
    for k, t in enumerate(('1 · Dati riportati sull’atto SIPO',
                           '2 · /finalizzaAtto · 2 DEFINITO')):
        pill(sl, x + 0.25, y + 2.68 + k * 0.32, w - 0.5, '✓ ' + t, VERDE, VERDE_F, pt=7, h=0.26)
    txt(sl, x + 0.15, y + 3.5, w - 0.3, 1.2, 'Tutti i campi obbligatori in ANSC, non solo le '
        'differenze: ANSC è la fonte. Alla fine il chip della card diventa verde.', pt=8,
        col=MUTED, it=True)
    piede(sl, m, [('ANNULLA', True, False), ('CONFERMA L’AGGIORNAMENTO', True, True)])


def s_percorso(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Il percorso sulla card, pulsante per pulsante')
    for (yy, tit, col, fon, seq, nota) in (
            (1.3, 'Caso 1 · servizi cooperativi', ROSSO, ROSSO_F,
             ['Valida · modale (R001 + R009)', 'Firma dichiaranti · modale (R012 o R006)',
              'Conformità · modale (R010 + R007) · solo con firme su carta',
              'Firma USC · modale (R007)', 'chip Salvato in SIPO (/finalizzaAtto)'],
             'per ciascun gemello, in qualsiasi ordine · senza firme su carta si salta la '
             'conformità · nessun dichiarante: la modale lo dice e si prosegue'),
            (3.8, 'Caso 2 · web app', GIALLO, GIALLO_F,
             ['Dati per la web app · modale (copia dei campi)', 'Web app · bozza prenotata, '
              'completata e firmata', 'Recupera da ANSC · modale (R005 per idAnsc)',
              'Aggiorna SIPO · modale', 'chip Salvato in SIPO (/finalizzaAtto)'],
             'per ciascun gemello, nell’ordine in cui la web app li completa')):
        box(sl, 0.4, yy, 12.5, 2.2, '', fill=BIANCO, line=GRIGIO)
        txt(sl, 0.5, yy + 0.08, 4.0, 0.3, tit, pt=12, bold=True, col=col)
        x = 0.5
        for i, t in enumerate(seq):
            ultimo = i == len(seq) - 1
            box(sl, x, yy + 0.55, 2.3, 1.0, t, fill=VERDE_F if ultimo else fon,
                line=VERDE if ultimo else col, pt=9, bold=True, al=PP_ALIGN.CENTER,
                anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.08)
            if not ultimo:
                freccia(sl, x + 2.3, yy + 1.05, x + 2.5, yy + 1.05)
            x += 2.5
        txt(sl, 0.5, yy + 1.7, 12.2, 0.4, nota, pt=9, col=MUTED, it=True)
    txt(sl, 0.4, 6.2, 12.5, 0.9, [
        ('Testata invariata rispetto alla v0.3: RIEPILOGO NUMERI e CANCELLA PRATICA. Divisione '
         'invariata: numeri e prenotazione automatici, caso 1 con l’UC specifico, caso 2 con '
         '11999999.', {'pt': 10})])


def s_decisioni(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Punti da fissare', 'D-G restano dalla v0.3; H e I nascono dalle modali')
    elenco(sl, 0.4, 1.25, 12.5, 6.0, [
        ('D. Caso 2: come arrivano i documenti sulla bozza.', 'Propongo di provare R001 sulla '
         'bozza prenotata; se ANSC non lo ammette per l’UC di servizio, si caricano sulla web '
         'app scaricandoli dalla modale «Dati per la web app».'),
        ('E. Salvataggio automatico non riuscito.', 'Chip rosso «Non salvato in SIPO» e RIPROVA IL '
         'SALVATAGGIO; nessun ritorno ai dati.'),
        ('F. Recupera e Aggiorna distinti.', 'Due modali: la prima mostra controlli e differenze, '
         'la seconda scrive.'),
        ('G. CANCELLA PRATICA.', 'Solo se nessun gemello è FIRMATO DA USC: R011 sulle bozze, PUT '
         '/scarta dei numeri, cancellazione della pratica in SIPO.'),
        ('H. Firme dei dichiaranti.', 'Da verificare in preproduzione: se lo stesso atto ammette '
         'una firma elettronica (R012) e una su carta (R006); come ANSC porta a FIRMATO DAL '
         'DICHIARANTE un atto senza dichiaranti.'),
        ('I. Motivo di recupero nel caso 2.', 'Il mapping di 11999999 rende obbligatorio '
         'motivoRecupero (ANSC_96): quale valore usare per i gemelli con UC diversi va chiesto '
         'ad ANSC.'),
    ], pt=12)


def costruisci():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    box(sl, 0, 0, 13.333, 7.5, fill=ROSSO, line=None)
    txt(sl, 0.8, 2.4, 11.7, 1.0, 'Nascite gemellari: la pagina dopo la divisione e le sue modali',
        pt=30, bold=True, col=BIANCO)
    txt(sl, 0.8, 3.4, 11.7, 1.2, ['Proposta per riscrivere il capitolo 7 «La modalità di '
                                  'integrazione» · v0.4, con le richieste del 22/11/2026',
                                  'Bozza di discussione · dimostratore HTML a parte'],
        pt=16, col=BIANCO)
    s_richieste(prs)
    s_card(prs)
    s_mockup_1(prs)
    s_valida(prs)
    s_firma_dich(prs)
    s_conformita(prs)
    s_firma_usc(prs)
    s_mockup_2(prs)
    s_dati_webapp(prs)
    s_recupera(prs)
    s_percorso(prs)
    s_decisioni(prs)
    prs.save(OUT)
    return OUT


if __name__ == '__main__':
    print(costruisci())
