# -*- coding: utf-8 -*-
"""Proposta per il capitolo 7 dell'analisi delle nascite gemellari, v0.3 (22/11/2026).

Recepisce le decisioni dell'utente sulla v0.2:
  1. lo stato nella card si scrive senza codice («FIRMATO DA USC», non «5 FIRMATO DA USC») e
     FIRMATO DA USC è verde;
  2. caso 1: niente pulsante SALVA IN SIPO, alla firma dell'USC l'atto si salva in SIPO da sé;
  3. in testata RINUNCIA AL PARTO diventa CANCELLA PRATICA;
  4. documenti e firmatari di ciascun atto si raccolgono nella pagina di Riepilogo;
  5. verificato: anche nel caso 2 gli atti si prenotano, con l'UC di servizio 11999999; si
     completano poi sulla web app, non con i servizi cooperativi;
  6. RIGENERA non serve: l'abbinamento SIPO/ANSC c'è dall'origine e il testo si compone come
     nel caso 1, con gli idAnsc dei fratelli.
Le risposte A/B/C della v0.2 sono riportate fra le decisioni.

    /Library/Developer/CommandLineTools/usr/bin/python3 proposta_gemellari_pagina_v0_3_pptx.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import proposta_gemellari_pagina_pptx as P                          # noqa: E402
from proposta_gemellari_pagina_pptx import (box, txt, freccia, titolo, elenco,  # noqa: E402
                                            tabella, card, testata, pannello_testo, ROSSO,
                                            ROSSO_F, INK, MUTED, GRIGIO, GRIGIO_F, VERDE,
                                            VERDE_F, BLU, BLU_F, GIALLO, GIALLO_F, BIANCO)

OUT = os.path.join(os.path.dirname(P.OUT), 'PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.3.pptx')

# stati senza codice; FIRMATO DA USC in verde
P.STATI.update({
    'corso': ('CONFERMATO', ROSSO, ROSSO_F),
    'usc': ('FIRMATO DA USC', VERDE, VERDE_F),
    'bozza': ('BOZZA (prenotato)', BLU, BLU_F),
    'wa2': ('BOZZA · ATTESA WEBAPP', GIALLO, GIALLO_F),
    'rec': ('FIRMATO DA USC · DA AGGIORNARE', VERDE, VERDE_F),
})
PASSI_C1 = ['Valida', 'Firma dich.', 'Conform.', 'Firma USC', 'Salvato in SIPO']
PASSI_C2 = ['Testo copiato', 'Atto su web app', 'Recuperato da ANSC', 'Aggiornato in SIPO']
DOC = ' · 3 documenti, 2 firmatari (dal Riepilogo)'

G1 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11111000" + DOC, "13617",
       "2026-10527618-13617-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "1 nato vivo", "11111000" + DOC, "13618",
       "2026-10527619-13618-058091"),
      ("3", "NATO 3 — COGNOME NOME", "F", "1 nato vivo", "11111000" + DOC, "13619",
       "2026-10527620-13619-058091"))
G2 = (("1", "NATO 1 — COGNOME NOME", "M", "1 nato vivo", "11999999 (servizio)", "13640",
       "2026-10531102-13640-058091"),
      ("2", "NATO 2 — COGNOME NOME", "F", "2 nato morto", "11999999 (servizio)", "13641",
       "2026-10531103-13641-058091"),
      ("3", "NATO 3 — COGNOME NOME", "M", "3 nato vivo poi deceduto", "11999999 (servizio)",
       "13642", "2026-10531104-13642-058091"))
COMANDI_TESTATA = [('RIEPILOGO NUMERI', True, False), ('CANCELLA PRATICA', True, False)]


def banner(sl, righe, fill, line, col):
    box(sl, 6.6, 0.2, 6.43, 0.8, righe, fill=fill, line=line, lw=1.5, pt=11, col=col,
        anc=MSO_ANCHOR.MIDDLE, al=PP_ALIGN.CENTER, forma=MSO_SHAPE.ROUNDED_RECTANGLE)


def mockup_1(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Caso 1 · stesso UC',
           'Gemello 1 concluso · gemello 2 alla firma del dichiarante · gemello 3 in bozza')
    testata(sl, 1.15, '1 · stesso UC · numeri staccati e atti prenotati alla divisione',
            COMANDI_TESTATA)
    y0, h = 2.3, 1.6
    card(sl, 0.3, y0, 6.0, h, G1[0], 'usc', PASSI_C1, 5,
         [('APRI IL PDF', True, False), ('STAMPA', True, False)],
         nota='salvato in SIPO alla firma dell’USC: 2 DEFINITO')
    card(sl, 0.3, y0 + h + 0.08, 6.0, h, G1[1], 'corso', PASSI_C1, 1,
         [('FIRMA ELETTRONICA', True, True), ('FIRMA SU CARTA', True, False),
          ('TORNA AI DATI', True, False)], sel=True)
    card(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G1[2], 'bozza', PASSI_C1, 0,
         [('VALIDA', True, True)],
         nota='lavorabile in qualsiasi ordine: non firmato dall’USC')
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO con gli idAnsc dei fratelli · salvato nella tabella dei '
                   'gemelli · inviato ad ANSC con la validazione (composizioneCompleta) · '
                   'validato: non più modificabile',
                   '13618', [('STAMPA', True, False), ('ANTEPRIMA ANSC (R010)', True, False),
                             ('SALVA TESTO', False, False)],
                   bloccato=True,
                   nota='Per modificarlo: TORNA AI DATI sul gemello (stato 0, nuova validazione).')
    banner(sl, [('Caso 1 · FIRMA USC conclude il gemello', {'bold': True, 'col': BIANCO}),
                ('  alla firma SIPO salva da sé: /finalizzaAtto con il testo salvato, atto a '
                 '2 DEFINITO. Nessun pulsante di salvataggio.', {'col': BIANCO, 'pt': 10})],
           ROSSO, None, BIANCO)


def mockup_2(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Caso 2 · UC diversi',
           'Prenotati con 11999999 · gemello 1 recuperato · 2 e 3 sulla web app')
    testata(sl, 1.15, '2 · UC diversi · numeri e prenotazione (11999999) alla divisione',
            COMANDI_TESTATA)
    y0, h = 2.3, 1.6
    card(sl, 0.3, y0, 6.0, h, G2[0], 'rec', PASSI_C2, 3,
         [('AGGIORNA SIPO DA ANSC', True, True), ('CONFRONTA', True, False)],
         nota='3 differenze')
    card(sl, 0.3, y0 + h + 0.08, 6.0, h, G2[1], 'wa2', PASSI_C2, 0,
         [('COPIA TESTO', True, True), ('APRI WEB APP', True, False),
          ('RECUPERA DA ANSC', True, False)], sel=True)
    card(sl, 0.3, y0 + 2 * (h + 0.08), 6.0, h, G2[2], 'wa2', PASSI_C2, 0,
         [('COPIA TESTO', True, False), ('APRI WEB APP', True, False),
          ('RECUPERA DA ANSC', True, False)])
    pannello_testo(sl, 6.45, y0, 6.58, 3 * h + 0.16, 'Testo dell’atto · gemello 2',
                   'composto da SIPO come nel caso 1 · salvato nella tabella dei gemelli · da '
                   'incollare nella composizione libera della bozza prenotata, sulla web app',
                   '13641', [('COPIA TESTO', True, True), ('STAMPA', True, False),
                             ('SALVA TESTO', True, False)],
                   nota='Gli idAnsc dei fratelli sono noti dalla prenotazione: il testo è '
                        'completo prima di aprire la web app.',
                   nascita='è nata morta una bambina',
                   fratelli='Gli atti dei fratelli: 2026-10531102-13640-058091 (precedente), '
                            '2026-10531104-13642-058091 (successivo).')
    banner(sl, [('Caso 2 · RECUPERA DA ANSC → AGGIORNA SIPO DA ANSC', {'bold': True}),
                ('  l’atto si completa e si firma sulla web app; ANSC è la fonte, i dati si '
                 'riportano in SIPO, poi /finalizzaAtto.', {'pt': 10})],
           GIALLO_F, GIALLO, INK)


def conclusione(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Come si conclude un gemello: due direzioni opposte',
           'In entrambi i casi gli atti sono prenotati alla divisione; cambia dove si completano '
           'e da dove arrivano i dati')
    for k, (x, col, fon, tit, sotto, passi, fonte) in enumerate((
            (0.4, ROSSO, ROSSO_F, 'Caso 1 · servizi cooperativi',
             'l’atto si completa da SIPO e va in ANSC: SIPO → ANSC',
             [('FIRMA USC (R007)', 'atto formato in ANSC: FIRMATO DA USC'),
              ('Salvataggio automatico', 'nessun pulsante: SIPO lo esegue all’esito positivo '
                                         'della firma'),
              ('/finalizzaAtto', 'PDF dal testo salvato nella tabella dei gemelli; '
                                 'allineamento anagrafico come oggi'),
              ('2 DEFINITO', 'il gemello è concluso in SIPO')],
             'Fonte dei dati: SIPO. Da ANSC si legge solo lo stato.'),
            (6.85, GIALLO, GIALLO_F, 'Caso 2 · web app',
             'l’atto si completa sulla web app e torna in SIPO: ANSC → SIPO',
             [('Bozza prenotata completata e firmata', 'sulla web app, con il testo copiato '
                                                       'da SIPO'),
              ('RECUPERA DA ANSC', 'R005 per idAnsc, noto dalla prenotazione; controlli: '
                                   'stato, intestatario, tipologia di nascita'),
              ('AGGIORNA SIPO DA ANSC', 'tutti i campi obbligatori in ANSC sull’atto SIPO; '
                                        'differenze mostrate prima'),
              ('/finalizzaAtto · 2 DEFINITO', 'il gemello è concluso in SIPO')],
             'Fonte dei dati: ANSC. SIPO si allinea a ciò che è stato formato.'))):
        box(sl, x, 1.3, 6.1, 5.6, '', fill=BIANCO, line=col, lw=2.0)
        txt(sl, x + 0.2, 1.4, 5.7, 0.4, tit, pt=14, bold=True, col=col if k == 0 else INK)
        txt(sl, x + 0.2, 1.8, 5.7, 0.3, sotto, pt=11, col=MUTED)
        y = 2.3
        for i, (t, s) in enumerate(passi):
            box(sl, x + 0.4, y, 5.3, 0.8, [(t, {'bold': True, 'pt': 12}),
                                           (s, {'pt': 9, 'col': MUTED})],
                fill=fon, line=col, forma=MSO_SHAPE.ROUNDED_RECTANGLE, marg=0.1,
                anc=MSO_ANCHOR.MIDDLE)
            if i < len(passi) - 1:
                freccia(sl, x + 3.05, y + 0.8, x + 3.05, y + 1.0)
            y += 1.0
        txt(sl, x + 0.2, 6.35, 5.7, 0.5, fonte, pt=10, it=True, col=INK)


def riepilogo(prs):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    titolo(sl, 'Documenti e firmatari: si raccolgono nel Riepilogo, atto per atto',
           'Prima della divisione; la pagina dei gemelli non ha più il pulsante DOCUMENTI')
    tabella(sl, 0.4, 1.3, 7.6, [
        ['Nel Riepilogo, per ciascun nato', 'Che cosa si raccoglie', 'Dove finisce'],
        ['Documenti', 'i documenti richiesti dall’UC del nato (es. attestazione di nascita, '
         'delega), caricati e verificati in SIPO', 'ALLEGATO, legato all’atto del nato dopo la '
         'divisione'],
        ['Firmatari', 'chi firma l’atto: dichiarante, eventuale interprete, testimoni dove '
         'previsti', 'elenco dei firmatari dell’atto'],
        ['Riscontro', 'mancanze segnalate prima di dividere', '—'],
    ], [1.6, 3.6, 2.4], pt=9, h_riga=0.7)
    elenco(sl, 8.3, 1.3, 4.7, 5.6, [
        ('Caso 1.', 'Alla VALIDA del gemello SIPO carica i documenti in ANSC (R001) e poi '
         'valida (R009). La firma usa l’elenco dei firmatari già raccolto.'),
        ('Caso 2.', 'I documenti e i firmatari raccolti in SIPO servono a completare la bozza '
         'sulla web app: come vi arrivino è il punto D della pagina delle decisioni.'),
        ('Sulla card resta un’indicazione,', 'non un’azione: quanti documenti e firmatari ha '
         'l’atto.'),
    ], pt=12)


def costruisci():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    V = prs.slide_layouts[6]

    sl = prs.slides.add_slide(V)
    box(sl, 0, 0, 13.333, 7.5, fill=ROSSO, line=None)
    txt(sl, 0.8, 2.4, 11.7, 1.0, 'Nascite gemellari: una sola pagina dopo la divisione',
        pt=32, bold=True, col=BIANCO)
    txt(sl, 0.8, 3.4, 11.7, 1.2, ['Proposta per riscrivere il capitolo 7 «La modalità di '
                                  'integrazione» · v0.3, con le decisioni del 22/11/2026',
                                  'Bozza di discussione'], pt=16, col=BIANCO)

    # strategia
    sl = prs.slides.add_slide(V)
    titolo(sl, 'La strategia: una pagina, tre zone, due modi di concludere',
           'Dopo la divisione SIPO apre sempre la stessa pagina; numeri e prenotazione ci sono '
           'già, in entrambi i casi')
    elenco(sl, 0.4, 1.3, 7.3, 5.9, [
        ('Documenti e firmatari nel Riepilogo.', 'Si raccolgono atto per atto prima di dividere.'),
        ('La divisione fa tutto il lavoro di parto.', 'Se riesce, SIPO stacca i numeri comunali e '
         'prenota gli atti in ANSC: con l’UC specifico nel caso 1, con l’UC di servizio 11999999 '
         'nel caso 2.'),
        ('Una sola pagina per il parto.', 'Sostituisce riepilogo gemelli, finestre di raccordo, '
         'procedura DEFINISCI, pratica guidata, esito e pagina di ripresa.'),
        ('Le card sono il raccordo.', 'Numero comunale in grande, idAnsc con il numero evidenziato, '
         'noto in entrambi i casi.'),
        ('Si lavora sul gemello di turno o su quello selezionato,', 'purché non già firmato '
         'dall’USC.'),
        ('Il testo a destra, salvato nella tabella dei gemelli.', 'Composto da SIPO con gli '
         'idAnsc dei fratelli, nei due casi allo stesso modo.'),
        ('Due conclusioni diverse.', 'Caso 1: alla firma dell’USC l’atto si salva in SIPO da sé '
         '(SIPO → ANSC). Caso 2: RECUPERA DA ANSC e AGGIORNA SIPO DA ANSC (ANSC → SIPO).'),
        ('Aprire la pagina è già riprendere.', 'Store + R005 per gli atti prenotati.'),
    ], pt=12)
    x, y = 8.1, 1.4
    box(sl, x, y, 4.8, 0.8, ['TESTATA', ('genitori · dati dell’atto · OTP · riepilogo numeri · '
                                         'cancella pratica', {'pt': 9, 'col': MUTED})],
        fill=GRIGIO_F, line=GRIGIO, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    box(sl, x, y + 0.9, 2.2, 3.4, ['CARD DEI GEMELLI', ('una per nato, con i pulsanti del suo '
                                                         'stato', {'pt': 9, 'col': MUTED})],
        fill=ROSSO_F, line=ROSSO, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    box(sl, x + 2.3, y + 0.9, 2.5, 3.4, ['TESTO DELL’ATTO', ('del gemello selezionato · '
                                                             'modificabile · stampa',
                                                             {'pt': 9, 'col': MUTED})],
        fill=BLU_F, line=BLU, pt=11, bold=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)

    riepilogo(prs)
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
        ['BOZZA (prenotato)', 'VALIDA', 'R001 · R009 validazione'],
        ['CONFERMATO', 'FIRMA ELETTRONICA · FIRMA SU CARTA · TORNA AI DATI',
         'R012 · R006'],
        ['FIRMATO DAL DICHIARANTE', 'FIRMA CONFORMITÀ', 'R010 · R007'],
        ['FIRMATO PER CONFORMITÀ', 'FIRMA USC', 'R007, poi /finalizzaAtto da sé'],
        ['FIRMATO DA USC', 'APRI IL PDF · STAMPA', '—'],
        ['FIRMATO DA USC · NON SALVATO IN SIPO', 'RIPROVA IL SALVATAGGIO', '/finalizzaAtto'],
        ['esito incerto', 'VERIFICA IN ANSC', 'R005'],
    ], [1.9, 2.8, 1.6], pt=9, h_riga=0.46)
    tabella(sl, 6.9, 1.25, 6.0, [
        ['Caso 2 · stato del gemello', 'Pulsanti', 'Servizi'],
        ['BOZZA · ATTESA WEBAPP', 'COPIA TESTO · APRI WEB APP · RECUPERA DA ANSC', '—'],
        ['NON FIRMATO (letto in ANSC)', 'APRI WEB APP · RECUPERA DA ANSC', 'R005'],
        ['INCOERENTE', 'CONFRONTA (nessuna scrittura)', '—'],
        ['FIRMATO DA USC · DA AGGIORNARE', 'AGGIORNA SIPO DA ANSC · CONFRONTA',
         'R005 · /finalizzaAtto'],
        ['FIRMATO DA USC', 'APRI IL PDF · STAMPA', '—'],
    ], [1.8, 2.8, 1.4], pt=9, h_riga=0.46)
    txt(sl, 0.4, 5.15, 12.5, 1.8, [
        ('Gli stati si scrivono senza codice; FIRMATO DA USC è verde.', {'pt': 11}),
        ('Firma del dichiarante nel caso 1: elettronica (R012) o su carta (R006). La sola firma '
         'su carta vale per la web app, cioè per il caso 2.', {'pt': 11}),
        ('Nel caso 2 il recupero è per idAnsc: la bozza prenotata lo ha già, quindi il gemello si '
         'trova sempre; resta da controllare che sia firmato e coerente.',
         {'pt': 11, 'col': MUTED})])

    # azioni di parto e testo
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Che cosa fa la divisione, che cosa resta in testata, che cosa fa il testo',
           'Il lavoro di parto si sposta nella pagina precedente')
    tabella(sl, 0.4, 1.25, 6.3, [
        ['Momento o azione', 'Che cosa fa'],
        ['Divisione riuscita · caso 1', '/performAttiPlurigemellari, POST /richiesta (N numeri), '
         'R009 /prenota/evento con l’UC specifico'],
        ['Divisione riuscita · caso 2', '/performAttiPlurigemellari, POST /richiesta (N numeri), '
         'R009 /prenota/evento con l’UC 11999999'],
        ['Numeri o prenotazione non riusciti', 'la divisione resta; avviso e solo RECUPERA NUMERI '
         'E PRENOTAZIONE (R005 prima di ritentare)'],
        ['RIEPILOGO NUMERI (testata)', 'stampa le card come promemoria'],
        ['CANCELLA PRATICA (testata)', 'nessun gemello FIRMATO DA USC: R011 sulle bozze, '
         'PUT /scarta dei numeri, cancellazione della pratica in SIPO'],
    ], [2.0, 4.3], pt=9, h_riga=0.6)
    tabella(sl, 6.9, 1.25, 6.0, [
        ['Azione sul testo (destra)', 'Caso', 'Che cosa fa'],
        ['SALVA TESTO', '1 e 2', 'deposita il testo nel campo della tabella dei gemelli'],
        ['STAMPA', '1 e 2', 'il testo del gemello selezionato'],
        ['COPIA TESTO', '2', 'negli appunti, per la composizione libera della bozza'],
        ['ANTEPRIMA ANSC', '1', 'R010 con presaVisione, dopo la validazione'],
    ], [1.7, 0.8, 3.5], pt=9, h_riga=0.6)
    txt(sl, 0.4, 5.3, 12.5, 1.6, [
        ('Non c’è più RIGENERA: l’abbinamento fra atto SIPO e atto ANSC esiste dalla '
         'prenotazione, e il testo si compone una volta con numeri e idAnsc dei fratelli.',
         {'pt': 11}),
        ('Il testo è modificabile finché non esce da SIPO: nel caso 1 fino a VALIDA, che lo invia '
         'come composizioneCompleta; nel caso 2 finché l’atto non è recuperato.', {'pt': 11}),
        ('Il campo del testo nella tabella dei gemelli serve a modifica, invio o copia, e PDF '
         'della definizione.', {'pt': 11, 'col': MUTED})])

    # percorso
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Il percorso', 'Le stesse fasi nei due casi; cambiano il canale con cui si '
           'completa l’atto e la direzione della conclusione')
    fasi = [('Compilazione', 'come oggi in SIPO; UC di ciascun nato dai flag', GRIGIO_F, GRIGIO),
            ('Riepilogo', 'documenti e firmatari per atto', GRIGIO_F, GRIGIO),
            ('Divisione', 'atti separati, numeri comunali, prenotazione ANSC', ROSSO_F, ROSSO),
            ('Lavoro sulle card', 'gemello di turno o selezionato, non firmato dall’USC',
             ROSSO_F, ROSSO),
            ('Parto concluso', 'tutte le card FIRMATO DA USC, atti SIPO 2 DEFINITO',
             VERDE_F, VERDE)]
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
             ['VALIDA (R001 + R009 con il testo)', 'FIRMA DICHIARANTE (R012 o R006)',
              'FIRMA CONFORMITÀ (R007)', 'FIRMA USC (R007)', 'salvato in SIPO da sé '
                                                             '(/finalizzaAtto)'],
             'per ciascun gemello, in qualsiasi ordine · errore certo: RIPROVA · esito incerto: '
             'VERIFICA IN ANSC'),
            (5.0, 'Card · caso 2', GIALLO, GIALLO_F,
             ['COPIA TESTO', 'APRI WEB APP: bozza prenotata', 'completamento e firma sulla '
                                                              'web app',
              'RECUPERA DA ANSC (R005 per idAnsc)', 'AGGIORNA SIPO DA ANSC (/finalizzaAtto)'],
             'per ciascun gemello, nell’ordine in cui la web app li completa')):
        box(sl, 0.4, yy, 12.5, 1.65, '', fill=BIANCO, line=GRIGIO)
        txt(sl, 0.5, yy + 0.05, 3.0, 0.3, tit, pt=11, bold=True, col=col)
        x = 0.5
        for i, t in enumerate(seq):
            ultimo = i == len(seq) - 1
            box(sl, x, yy + 0.45, 2.3, 0.65, t, fill=col if ultimo else fon, line=col, pt=9,
                bold=True, col=BIANCO if ultimo and col == ROSSO else INK, al=PP_ALIGN.CENTER,
                anc=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE,
                dash=ultimo and col == ROSSO)
            if not ultimo:
                freccia(sl, x + 2.3, yy + 0.78, x + 2.5, yy + 0.78)
            x += 2.5
        txt(sl, 0.5, yy + 1.2, 12.2, 0.35, nota, pt=9, col=MUTED, it=True)

    # che cosa cambia
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Che cosa cambia nel documento', 'Rispetto alla v0.9 dell’analisi')
    tabella(sl, 0.4, 1.25, 12.5, [
        ['Nella v0.9', 'Nella proposta'],
        ['DEFINISCI / DATI PER ANSC stacca i numeri (e prenota nel caso 1)',
         'la divisione stacca i numeri e prenota in entrambi i casi'],
        ['Caso 2: nessuna prenotazione, numeri da riportare a mano sulla web app',
         'caso 2: bozze prenotate con 11999999, completate sulla web app'],
        ['Riepilogo gemelli e finestra di raccordo', 'testata + card'],
        ['Documenti caricati gemello per gemello', 'documenti e firmatari nel Riepilogo, per atto'],
        ['Un gemello alla volta, in ordine', 'gemello di turno o selezionato, in qualsiasi ordine'],
        ['Firma del dichiarante solo su carta', 'caso 1: elettronica (R012) o su carta (R006)'],
        ['Caso 2: RECUPERA e DEFINISCI GEMELLI per il parto, ricerca per numero comunale',
         'caso 2: RECUPERA DA ANSC (per idAnsc) e AGGIORNA SIPO DA ANSC, per gemello'],
        ['Testo ricomposto dal formulario, non conservato', 'testo in un campo di '
         'ANSC_SOGGETTO_ATTO; la definizione lo usa'],
        ['RINUNCIA AL PARTO; esito del parto e pagina di ripresa',
         'CANCELLA PRATICA; la pagina stessa fa da esito e da ripresa'],
    ], [5.6, 6.9], pt=10, h_riga=0.48)

    # decisioni e punti residui
    sl = prs.slides.add_slide(V)
    titolo(sl, 'Le decisioni prese e quattro punti ancora da fissare')
    tabella(sl, 0.4, 1.15, 12.5, [
        ['Tema', 'Decisione'],
        ['Pagina e testo', 'una sola pagina, testata + card + testo; testo in un campo della '
         'tabella dei gemelli, senza RIGENERA'],
        ['Divisione', 'numeri e prenotazione automatici (caso 1 UC specifico, caso 2 11999999); se '
         'falliscono la divisione resta e si offre RECUPERA NUMERI E PRENOTAZIONE'],
        ['Card', 'di turno o selezionata, non firmata dall’USC, qualsiasi ordine; stati senza '
         'codice, FIRMATO DA USC in verde'],
        ['Conclusione', 'caso 1 salvataggio automatico alla firma USC; caso 2 AGGIORNA SIPO DA '
         'ANSC con tutti i campi obbligatori in ANSC'],
        ['Documenti, firme', 'documenti e firmatari nel Riepilogo; firma del dichiarante anche '
         'elettronica nel caso 1'],
    ], [2.2, 10.3], pt=10, h_riga=0.4)
    elenco(sl, 0.4, 3.75, 12.5, 3.6, [
        ('D. Caso 2: come arrivano i documenti sulla bozza.', 'Propongo di provare R001 sulla '
         'bozza prenotata, così l’operatore non li ricarica sulla web app; se ANSC non lo ammette '
         'per l’UC di servizio, si caricano sulla web app scaricandoli da SIPO.'),
        ('E. Salvataggio automatico non riuscito.', 'Propongo: la card resta FIRMATO DA USC con '
         'l’avviso «non salvato in SIPO» e il solo RIPROVA IL SALVATAGGIO; nessun ritorno ai dati.'),
        ('F. Caso 2: RECUPERA e AGGIORNA in un solo passo?', 'Propongo di tenerli distinti, perché '
         'l’aggiornamento scrive su SIPO e le differenze vanno viste prima.'),
        ('G. CANCELLA PRATICA.', 'Propongo: ammessa solo se nessun gemello è FIRMATO DA USC; '
         'cancella le bozze in ANSC (R011), scarta i numeri e cancella la pratica in SIPO.'),
    ], pt=11)

    prs.save(OUT)
    return OUT


if __name__ == '__main__':
    print(costruisci())
