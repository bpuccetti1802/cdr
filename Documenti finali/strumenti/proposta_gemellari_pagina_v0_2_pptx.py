# -*- coding: utf-8 -*-
"""Proposta per il capitolo 7 dell'analisi delle nascite gemellari, v0.2 (22/11/2026).

Recepisce le decisioni dell'utente sulla v0.1:
  1. la pagina va bene; va evidenziato come si conclude un gemello: nel caso 1 SALVA IN SIPO
     conclude l'operazione in SIPO, nel caso 2 i dati si recuperano da ANSC e si aggiornano in SIPO;
  2. il testo dell'atto si deposita in un campo della nuova tabella dei gemelli
     (ANSC_SOGGETTO_ATTO);
  3. nel caso 2 recupero e definizione sono per gemello;
  4. lo stacco dei numeri (e nel caso 1 la prenotazione ANSC) è automatico e intrinseco alla
     divisione della pratica, se va a buon fine;
  5. si lavora sulla card di turno o su quella selezionata, purché non già firmata dall'USC;
  6. nel caso 1 la firma del dichiarante è ammessa anche elettronica (la sola cartacea vale per
     la web app).

    /Library/Developer/CommandLineTools/usr/bin/python3 proposta_gemellari_pagina_v0_2_pptx.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import proposta_gemellari_pagina_pptx as P                          # noqa: E402
from proposta_gemellari_pagina_pptx import (box, txt, btn, pill, freccia, titolo, elenco,  # noqa
                                            tabella, card, testata, pannello_testo, ROSSO,
                                            ROSSO_F, INK, MUTED, GRIGIO, GRIGIO_F, VERDE,
                                            VERDE_F, BLU, BLU_F, GIALLO, GIALLO_F, BIANCO)

OUT = os.path.join(os.path.dirname(P.OUT), 'PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.2.pptx')

P.STATI.update({
    'usc': ('5 FIRMATO DA USC · SIPO 1', ROSSO, ROSSO_F),
    'bozza': ('1 BOZZA (prenotato)', BLU, BLU_F),
    'rec': ('RECUPERATO · 5 FIRMATO DA USC', BLU, BLU_F),
})
PASSI_C1 = ['Doc.', 'Valida', 'Firma dich.', 'Conform.', 'Firma USC', 'Salva in SIPO']
PASSI_C2 = ['Testo copiato', 'Atto su web app', 'Recuperato da ANSC', 'Aggiornato in SIPO']

G1 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13617",
       "2026-10527618-13617-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13618",
       "2026-10527619-13618-058091"),
      ("3", "NATO 3 — COGNOME NOME", "F", "1 nato vivo", "11111000", "13619",
       "2026-10527620-13619-058091"))
G2 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000", "13640",
       "2026-10531102-13640-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "2 nato morto", "11111100", "13641", None),
      ("3", "NATO 3 — COGNOME NOME", "M", "3 nato vivo poi deceduto", "11111200", "13642", None))


def mockup_1(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Caso 1 · stesso UC',
           'Gemello 1 da salvare · gemello 2 alla firma del dichiarante · gemello 3 in bozza')
    testata(sl, 1.15, '1 · stesso UC · numeri staccati e atti prenotati alla divisione',
            [('RIEPILOGO NUMERI', True, False), ('RINUNCIA AL PARTO', True, False)])
    y0, h = 2.3, 1.6
    card(sl, 0.3, y0, 6.0, h, G1[0], 'usc', PASSI_C1, 5,
         [('SALVA IN SIPO', True, True), ('ANTEPRIMA ANSC', True, False)],
         nota='conclude il gemello in SIPO')
    card(sl, 0.3, y0 + h + 0.08, 6.0, h, G1[1], 'corso', PASSI_C1, 2,
         [('FIRMA ELETTRONICA', True, True), ('FIRMA SU CARTA', True, False),
          ('TORNA AI DATI', True, False)], sel=True)
    card(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G1[2], 'bozza', PASSI_C1, 0,
         [('VALIDA', True, True), ('DOCUMENTI', True, False)],
         nota='lavorabile: non firmato dall’USC')
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO · salvato nella tabella dei gemelli · inviato ad ANSC con la '
                   'validazione (composizioneCompleta) · validato: non più modificabile',
                   '13618', [('STAMPA', True, False), ('ANTEPRIMA ANSC (R010)', True, False),
                             ('RIGENERA', False, False), ('SALVA TESTO', False, False)],
                   bloccato=True,
                   nota='Per modificarlo: TORNA AI DATI sul gemello (stato 0, nuova validazione).')
    # evidenza della conclusione
    box(sl, 6.6, 0.2, 6.43, 0.8, [('Caso 1 · SALVA IN SIPO', {'bold': True, 'col': BIANCO}),
                                  ('  conclude il gemello in SIPO: /finalizzaAtto con il testo '
                                   'salvato, atto a 2 DEFINITO. SIPO è la fonte, ANSC ha già '
                                   'ricevuto.', {'col': BIANCO, 'pt': 10})],
        fill=ROSSO, line=None, pt=11, anc=MSO_ANCHOR.MIDDLE, al=PP_ALIGN.CENTER,
        forma=MSO_SHAPE.ROUNDED_RECTANGLE)


def mockup_2(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Caso 2 · UC diversi',
           'Gemello 1 recuperato da ANSC · gemello 2 testo da copiare · gemello 3 da fare')
    testata(sl, 1.15, '2 · UC diversi · numeri staccati alla divisione',
            [('RIEPILOGO NUMERI', True, False), ('RINUNCIA AL PARTO', True, False)])
    y0, h = 2.3, 1.6
    card(sl, 0.3, y0, 6.0, h, G2[0], 'rec', PASSI_C2, 3,
         [('AGGIORNA SIPO DA ANSC', True, True), ('CONFRONTA', True, False)],
         nota='3 differenze')
    card(sl, 0.3, y0 + h + 0.08, 6.0, h, G2[1], 'wa', PASSI_C2, 0,
         [('COPIA TESTO', True, True), ('APRI WEB APP', True, False),
          ('RECUPERA DA ANSC', True, False)], sel=True)
    card(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G2[2], 'wa', PASSI_C2, 0,
         [('COPIA TESTO', True, False), ('APRI WEB APP', True, False),
          ('RECUPERA DA ANSC', True, False)])
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO · salvato nella tabella dei gemelli · da incollare nella '
                   'composizione libera della bozza sulla web app',
                   '13641', [('COPIA TESTO', True, True), ('STAMPA', True, False),
                             ('RIGENERA', True, False), ('SALVA TESTO', True, False)],
                   nota='Gli idAnsc dei fratelli li assegna la web app: si completano lì.',
                   nascita='è nata morta una bambina',
                   fratelli='Gli atti dei fratelli: [identificativi da completare sulla web app].')
    box(sl, 6.6, 0.2, 6.43, 0.8, [('Caso 2 · RECUPERA DA ANSC → AGGIORNA SIPO DA ANSC',
                                   {'bold': True, 'col': INK}),
                                  ('  ANSC è la fonte: i dati dell’atto firmato si riportano in '
                                   'SIPO, poi /finalizzaAtto.', {'col': INK, 'pt': 10})],
        fill=GIALLO_F, line=GIALLO, lw=1.5, pt=11, anc=MSO_ANCHOR.MIDDLE, al=PP_ALIGN.CENTER,
        forma=MSO_SHAPE.ROUNDED_RECTANGLE)


def conclusione(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Come si conclude un gemello: due direzioni opposte',
           'È la differenza di sostanza fra i due casi, e la pagina la rende con due pulsanti '
           'diversi')
    for k, (x, col, fon, tit, sotto, passi, fonte) in enumerate((
            (0.4, ROSSO, ROSSO_F, 'Caso 1 · SALVA IN SIPO',
             'l’atto nasce in SIPO e va in ANSC: SIPO → ANSC',
             [('Firma USC (R007)', 'atto formato in ANSC · 5 FIRMATO DA USC'),
              ('SALVA IN SIPO', 'pulsante primario della card, subito dopo la firma'),
              ('/finalizzaAtto', 'PDF dal testo salvato nella tabella dei gemelli; '
                                 'allineamento anagrafico come oggi'),
              ('2 DEFINITO', 'il gemello è concluso in SIPO')],
             'Fonte dei dati: SIPO. Nulla si legge da ANSC, salvo la verifica dello stato.'),
            (6.85, GIALLO, GIALLO_F, 'Caso 2 · RECUPERA → AGGIORNA SIPO DA ANSC',
             'l’atto nasce sulla web app e torna in SIPO: ANSC → SIPO',
             [('Atto firmato sulla web app', 'con il numero comunale di SIPO'),
              ('RECUPERA DA ANSC', 'R005 per numero comunale; controlli: numero nell’idAnsc, '
                                   'stato 5, UC, intestatario'),
              ('AGGIORNA SIPO DA ANSC', 'i dati dell’atto ANSC sull’atto SIPO; testo ANSC nella '
                                        'tabella dei gemelli; differenze mostrate prima'),
              ('/finalizzaAtto · 2 DEFINITO', 'il gemello è concluso in SIPO')],
             'Fonte dei dati: ANSC. SIPO si allinea a ciò che è stato formato.'))):
        box(sl, x, 1.3, 6.1, 5.6, '', fill=BIANCO, line=col, lw=2.0)
        txt(sl, x + 0.2, 1.4, 5.7, 0.4, tit, pt=14, bold=True, col=col if k == 0 else INK)
        txt(sl, x + 0.2, 1.8, 5.7, 0.3, sotto, pt=11, col=MUTED)
        y = 2.3
        for i, (t, s) in enumerate(passi):
            box(sl, x + 0.4, y, 5.3, 0.8, [(t, {'bold': True, 'pt': 12}), (s, {'pt': 9,
                                                                               'col': MUTED})],
                fill=fon, line=col, forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.1,
                anc=MSO_ANCHOR.MIDDLE)
            if i < len(passi) - 1:
                freccia(sl, x + 3.05, y + 0.8, x + 3.05, y + 1.0)
            y += 1.0
        txt(sl, x + 0.2, 6.35, 5.7, 0.5, fonte, pt=10, it=True, col=INK)


def costruisci():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    V = prs.slide_layouts[6]

    sl = prs.slides.add_slide(V)
    box(sl, 0, 0, 13.333, 7.5, fill=ROSSO, line=None)
    txt(sl, 0.8, 2.4, 11.7, 1.0, 'Nascite gemellari: una sola pagina dopo la divisione',
        pt=32, bold=True, col=BIANCO)
    txt(sl, 0.8, 3.4, 11.7, 1.2, ['Proposta per riscrivere il capitolo 7 «La modalità di '
                                  'integrazione» · v0.2, con le decisioni del 22/11/2026',
                                  'Bozza di discussione'], pt=16, col=BIANCO)

    # strategia
    sl = prs.slides.add_slide(V)
    titolo(sl, 'La strategia: una pagina, tre zone, due modi di concludere',
           'Dopo la divisione SIPO apre sempre la stessa pagina; i numeri ci sono già')
    elenco(sl, 0.4, 1.3, 7.3, 5.9, [
        ('La divisione fa tutto il lavoro di parto.', 'Se la pratica si divide in atti separati e la '
         'divisione va a buon fine, SIPO stacca subito i numeri comunali e, nel caso 1, prenota gli '
         'atti in ANSC. Nessun pulsante di parto per farlo.'),
        ('Una sola pagina per il parto.', 'Sostituisce riepilogo, finestre di raccordo, procedura '
         'DEFINISCI, pratica guidata, esito e pagina di ripresa.'),
        ('Le card sono il raccordo.', 'Numero comunale in grande, idAnsc con il numero evidenziato.'),
        ('Si lavora sul gemello di turno o su quello selezionato,', 'purché non già firmato '
         'dall’USC. Il caso 2 procede gemello per gemello, recupero compreso.'),
        ('Il testo a destra, salvato nella tabella dei gemelli.', 'Modificabile finché non esce da '
         'SIPO; da lì lo legge anche la definizione.'),
        ('Due conclusioni diverse.', 'Caso 1: SALVA IN SIPO (SIPO → ANSC). Caso 2: RECUPERA DA '
         'ANSC e AGGIORNA SIPO DA ANSC (ANSC → SIPO).'),
        ('Aprire la pagina è già riprendere.', 'Store + R005 per gli atti con idAnsc.'),
    ], pt=12)
    x, y = 8.1, 1.4
    box(sl, x, y, 4.8, 0.8, ['TESTATA', ('genitori · dati dell’atto · OTP · riepilogo numeri · '
                                         'rinuncia', {'pt': 9, 'col': MUTED})], fill=GRIGIO_F,
        line=GRIGIO, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    box(sl, x, y + 0.9, 2.2, 3.4, ['CARD DEI GEMELLI', ('una per nato, con i pulsanti del suo '
                                                         'stato e il pulsante di conclusione',
                                                         {'pt': 9, 'col': MUTED})],
        fill=ROSSO_F, line=ROSSO, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    box(sl, x + 2.3, y + 0.9, 2.5, 3.4, ['TESTO DELL’ATTO', ('del gemello selezionato · '
                                                             'modificabile · stampa',
                                                             {'pt': 9, 'col': MUTED})],
        fill=BLU_F, line=BLU, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)

    mockup_1(prs)
    mockup_2(prs)
    conclusione(prs)

    # pulsanti per stato
    sl = prs.slides.add_slide(V)
    titolo(sl, 'I pulsanti della card, stato per stato',
           'Il primo pulsante di ogni riga è il primario · attivi sulla card di turno o '
           'selezionata, se non firmata dall’USC')
    tabella(sl, 0.4, 1.25, 6.3, [
        ['Caso 1 · stato del gemello', 'Pulsanti', 'Servizi'],
        ['1 BOZZA (prenotato)', 'VALIDA · DOCUMENTI', 'R001 · R009 validazione'],
        ['2 CONFERMATO', 'FIRMA ELETTRONICA · FIRMA SU CARTA · TORNA AI DATI',
         'R012 · R006'],
        ['4 FIRMATO DAL DICHIARANTE', 'FIRMA CONFORMITÀ', 'R010 · R007'],
        ['11 FIRMATO PER CONFORMITÀ', 'FIRMA USC', 'R007'],
        ['5 FIRMATO DA USC · SIPO 1', 'SALVA IN SIPO', '/finalizzaAtto'],
        ['5 · 2 DEFINITO', 'APRI IL PDF', '—'],
        ['esito incerto', 'VERIFICA IN ANSC', 'R005'],
    ], [1.9, 2.8, 1.6], pt=9, h_riga=0.46)
    tabella(sl, 6.9, 1.25, 6.0, [
        ['Caso 2 · stato del gemello', 'Pulsanti', 'Servizi'],
        ['WA · ATTESA WEBAPP', 'COPIA TESTO · APRI WEB APP · RECUPERA DA ANSC', '—'],
        ['NON TROVATO · NON FIRMATO', 'RECUPERA DA ANSC · APRI WEB APP', 'R005'],
        ['INCOERENTE', 'CONFRONTA (nessuna scrittura)', '—'],
        ['RECUPERATO', 'AGGIORNA SIPO DA ANSC · CONFRONTA', 'R005 · /finalizzaAtto'],
        ['2 DEFINITO', 'APRI IL PDF', '—'],
    ], [1.8, 2.8, 1.4], pt=9, h_riga=0.46)
    txt(sl, 0.4, 5.15, 12.5, 1.8, [
        ('Firma del dichiarante nel caso 1: elettronica (R012) o su carta (R006). La sola firma '
         'su carta vale per la web app, cioè per il caso 2.', {'pt': 11}),
        ('Un gemello firmato dall’USC non si lavora più: resta selezionabile per leggere e '
         'stampare.', {'pt': 11}),
        ('Nel caso 2 recupero e aggiornamento sono per gemello: non serve aspettare gli altri.',
         {'pt': 11, 'col': MUTED})])

    # azioni di parto e testo
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Che cosa fa la divisione, che cosa resta in testata, che cosa fa il testo',
           'Il lavoro di parto si sposta nella pagina precedente')
    tabella(sl, 0.4, 1.25, 6.3, [
        ['Momento o azione', 'Che cosa fa'],
        ['Divisione riuscita · caso 1', '/performAttiPlurigemellari, poi POST /richiesta '
         '(N numeri) e R009 /prenota/evento; righe dello store e di ANSC_SOGGETTO_ATTO'],
        ['Divisione riuscita · caso 2', '/performAttiPlurigemellari, poi POST /richiesta '
         '(N numeri); righe in WA · ATTESA WEBAPP'],
        ['Divisione non riuscita', 'nessun numero, nessuna prenotazione: si resta sulla '
         'pratica'],
        ['RIEPILOGO NUMERI (testata)', 'stampa le card come promemoria'],
        ['RINUNCIA AL PARTO (testata)', 'nessun gemello a 5: R011 + PUT /scarta; pratica '
         'modificabile'],
    ], [2.0, 4.3], pt=9, h_riga=0.6)
    tabella(sl, 6.9, 1.25, 6.0, [
        ['Azione sul testo (destra)', 'Caso', 'Che cosa fa'],
        ['SALVA TESTO', '1 e 2', 'deposita il testo nel campo della tabella dei gemelli'],
        ['RIGENERA', '1 e 2', 'ricompone dal formulario e scarta le modifiche'],
        ['STAMPA', '1 e 2', 'il testo del gemello selezionato'],
        ['COPIA TESTO', '2', 'negli appunti, per la composizione libera'],
        ['ANTEPRIMA ANSC', '1', 'R010 con presaVisione, dopo la validazione'],
    ], [1.7, 0.8, 3.5], pt=9, h_riga=0.6)
    txt(sl, 0.4, 5.3, 12.5, 1.6, [
        ('Il testo è modificabile finché non esce da SIPO: nel caso 1 fino a VALIDA, che lo invia '
         'come composizioneCompleta; nel caso 2 finché l’atto non è recuperato.', {'pt': 11}),
        ('Nella tabella dei gemelli il campo del testo serve a tre cose: modifica, invio ad ANSC e '
         'PDF della definizione, che non lo rigenera più dal formulario.',
         {'pt': 11, 'col': MUTED})])

    # percorso
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Il percorso sulla pagina', 'Le stesse fasi nei due casi; cambiano il canale '
           'con cui si forma l’atto e la direzione della conclusione')
    fasi = [('Compilazione', 'come oggi in SIPO; UC di ciascun nato dai flag', GRIGIO_F, GRIGIO),
            ('Divisione', 'atti separati + numeri comunali; caso 1 anche prenotazione ANSC',
             ROSSO_F, ROSSO),
            ('Apertura della pagina', 'caso dall’UC; store + R005', BLU_F, BLU),
            ('Lavoro sulle card', 'gemello di turno o selezionato, non firmato dall’USC',
             ROSSO_F, ROSSO),
            ('Parto concluso', 'tutte le card a 2 DEFINITO', VERDE_F, VERDE)]
    x = 0.4
    for i, (t, s, f, l) in enumerate(fasi):
        box(sl, x, 1.5, 2.3, 1.3, [(t, {'bold': True, 'pt': 12}), (s, {'pt': 9, 'col': MUTED})],
            fill=f, line=l, forma=MSO_SHAPE.ROUNDED_RECTANGLE, al=PP_ALIGN.CENTER,
            anc=MSO_ANCHOR.MIDDLE, marg=0.1)
        if i < 4:
            freccia(sl, x + 2.3, 2.15, x + 2.55, 2.15)
        x += 2.55
    for (yy, tit, col, fon, seq, nota) in (
            (3.2, 'Card · caso 1', ROSSO, ROSSO_F,
             ['DOCUMENTI · VALIDA (R009 + testo)', 'FIRMA DICHIARANTE (R012 o R006)',
              'FIRMA CONFORMITÀ (R007)', 'FIRMA USC (R007)', 'SALVA IN SIPO (/finalizzaAtto)'],
             'per ciascun gemello · errore certo: RIPROVA · esito incerto: VERIFICA IN ANSC'),
            (5.0, 'Card · caso 2', GIALLO, GIALLO_F,
             ['COPIA TESTO', 'APRI WEB APP: atto con numero e tipologia', 'firma sulla web app',
              'RECUPERA DA ANSC (R005)', 'AGGIORNA SIPO DA ANSC (/finalizzaAtto)'],
             'per ciascun gemello, nell’ordine in cui la web app li completa')):
        box(sl, 0.4, yy, 12.5, 1.65, '', fill=BIANCO, line=GRIGIO)
        txt(sl, 0.5, yy + 0.05, 3.0, 0.3, tit, pt=11, bold=True, col=col)
        x = 0.5
        for i, t in enumerate(seq):
            ultimo = i == len(seq) - 1
            box(sl, x, yy + 0.45, 2.3, 0.65, t, fill=col if ultimo else fon, line=col, pt=9,
                bold=True, col=BIANCO if ultimo and col == ROSSO else INK, al=PP_ALIGN.CENTER,
                anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
            if not ultimo:
                freccia(sl, x + 2.3, yy + 0.78, x + 2.5, yy + 0.78)
            x += 2.5
        txt(sl, 0.5, yy + 1.2, 12.2, 0.35, nota, pt=9, col=MUTED, it=True)

    # che cosa cambia
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Che cosa cambia nel documento', 'Rispetto alla v0.9 dell’analisi')
    tabella(sl, 0.4, 1.25, 12.5, [
        ['Nella v0.9', 'Nella proposta'],
        ['DEFINISCI / DATI PER ANSC stacca i numeri (e prenota)', 'li fa la divisione, se riesce'],
        ['Riepilogo gemelli e finestra di raccordo (3 apparizioni)', 'testata + card'],
        ['Procedura DEFINISCI, pratica guidata, «DEFINISCI in corso»', 'pulsanti della card, '
         'errori sulla card'],
        ['Un gemello alla volta, in ordine', 'gemello di turno o selezionato, se non firmato '
         'dall’USC'],
        ['Firma del dichiarante solo su carta', 'caso 1: elettronica (R012) o su carta (R006)'],
        ['Definizione automatica dopo la firma USC', 'caso 1: SALVA IN SIPO'],
        ['Caso 2: RECUPERA e DEFINISCI GEMELLI per il parto, nessuna importazione',
         'caso 2: RECUPERA DA ANSC e AGGIORNA SIPO DA ANSC per gemello, con i dati di ANSC'],
        ['Testo ricomposto dal formulario, non conservato', 'testo in un campo di '
         'ANSC_SOGGETTO_ATTO; la definizione lo usa'],
        ['Esito del parto e pagina di ripresa', 'nessuna: la pagina stessa'],
    ], [5.0, 7.5], pt=10, h_riga=0.48)

    # domande residue
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Le decisioni prese e tre punti ancora da fissare')
    tabella(sl, 0.4, 1.2, 12.5, [
        ['Tema', 'Decisione'],
        ['Pagina', 'una sola, testata + card + testo'],
        ['Testo', 'campo nella tabella dei gemelli'],
        ['Caso 2', 'recupero e aggiornamento per gemello'],
        ['Numeri e prenotazione', 'automatici alla divisione riuscita'],
        ['Card lavorabile', 'di turno o selezionata, non firmata dall’USC'],
        ['Firma del dichiarante', 'caso 1 anche elettronica; solo carta per la web app'],
    ], [3.0, 9.5], pt=10, h_riga=0.36)
    elenco(sl, 0.4, 4.0, 12.5, 3.3, [
        ('A. Divisione riuscita ma prenotazione o stacco non riusciti.', 'Propongo: la divisione '
         'resta, la pagina si apre con un avviso e il solo comando COMPLETA NUMERI E PRENOTAZIONE '
         '(con R005 prima di ritentare la prenotazione). In alternativa si annulla la divisione.'),
        ('B. AGGIORNA SIPO DA ANSC: quali dati.', 'Tutti i campi mappati (ALIAS_CAMPO_SIPO di '
         'ANSC_CFG_CAMPO) con le differenze mostrate prima, oppure solo identificativi, stato e '
         'testo? Propongo tutti, con conferma sulle differenze.'),
        ('C. Gemelli fuori ordine nel caso 1.', 'Gli idAnsc dei fratelli sono noti dalla '
         'prenotazione, quindi il testo di ciascuno si può comporre subito: lavorare il gemello 3 '
         'prima del 2 non crea problemi per ANSC. Lo confermo nel documento?'),
    ], pt=12)

    prs.save(OUT)
    return OUT


if __name__ == '__main__':
    print(costruisci())
