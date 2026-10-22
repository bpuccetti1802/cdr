# -*- coding: utf-8 -*-
"""Figure dei due documenti di processo adattati da Side a Roma (22/10/2026).

  · PROCESSO_Numerazione-Comunale: le pagine stanno nel BACK-OFFICE dell'integrazione, quindi
    nella cornice di Roma Capitale del disegno del back-office (wireframe_bo.py). Senza il
    registro: dalla v3.41 dell'analisi la serie è una sola per anno, di sei cifre.
      pr_num_menu.png       la voce di menu, al posto del sottomenu dei registri di Side
      pr_num_richiesta.png  la pagina di richiesta, con la registrazione a posteriori
      pr_num_utilizzato.png la finestra «Segna come utilizzato», che chiede l'idAnsc
      pr_num_ricerca.png    la pagina di ricerca e consultazione, con le serie e i buchi
  · PROCESSO_Attestato-Conformita: la pagina sta nel percorso di SIPO, quindi nello stile di
    SIPO delle ipotesi del documento del workflow (schermate_sipo_wf.py), come schermata
    separata con il banner di arrivo. Tre stati, gli stessi delle schermate di Side:
      pr_conf_iniziale.png  primo accesso, documenti tutti selezionati
      pr_conf_anteprima.png attestazione generata, firma abilitata
      pr_conf_nessuno.png   nessun documento selezionato, CONTINUA abilitato

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_processi_side.py
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S   # noqa: E402
import wireframe_bo as W        # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
L, X = 1240, 24
C = L - 2 * X
ANNO = '2026'
SOTTO = ('Il numero comunale è a carico del Comune: si stacca dalla serie dell’anno, una sola '
         'per tutti i registri, che riparte ogni anno.')
BRICIOLE = ['Home', 'Integrazione ANSC', 'Numerazione comunale']


def idansc(num):
    return f'{ANNO}-10527{num[-3:]}-{num.replace(".", "")}-058091'


# ═════════════════════════════════════════════════════════════ numerazione (back-office)
def num_menu(dest):
    im, dr, y = W.pagina(L, 720, ['Home'], 'Integrazione ANSC', distintivo=('OTP', True),
                         sotto='Seleziona l’area su cui iniziare a operare.')
    voci = [('Supervisione atti', 'gli atti che non hanno concluso il percorso ordinario'),
            ('Notifiche ANSC', 'proposte di annotazione, prese visione, solleciti'),
            ('Numerazione comunale', 'richiesta, ricerca e consultazione dei numeri'),
            ('Configurazione casi d’uso', 'UC adottati, sezioni, campi, allegati, formule'),
            ('Catalogo UC di ANSC', 'ciò che ANSC pubblica — sola consultazione'),
            ('Logiche di scelta', 'le espressioni che determinano UC, sezioni e campi')]
    w, h, gap = (C - 2 * 18) // 3, 62, 18
    for i, (t, s) in enumerate(voci):
        W.card(dr, X + (i % 3) * (w + gap), y + (i // 3) * (h + gap), w, h, t, s)
    # il sottomenu della mattonella «Numerazione comunale»
    mx, my, mw = X + 2 * (w + gap) + 30, y + h - 6, w - 30
    dr.rectangle([mx + 4, my + 4, mx + mw + 4, my + 2 * 52 + 4], fill='#d5d8dd')
    dr.rectangle([mx, my, mx + mw, my + 2 * 52], fill='white', outline=W.BORDO)
    for i, t in enumerate(('Numerazione comunale — richiesta',
                           'Numerazione comunale — ricerca e consultazione')):
        yy = my + i * 52
        if i:
            dr.line([(mx, yy), (mx + mw, yy)], fill=W.RIGA)
        dr.rectangle([mx, yy + 1, mx + 4, yy + 51], fill=W.BARRA)
        dr.text((mx + 18, yy + 17), t, font=W.fnt(W.F_REG, 14), fill=W.INK)
    yy = y + 2 * (h + gap) + 70
    W.nota(dr, X, yy, C,
           'Una sola mattonella per la numerazione, nel menu dell’integrazione: in Side le due '
           'pagine si ripetono nel sottomenu di ciascun registro, qui la serie è una sola e le '
           'pagine anche. Le voci vengono dal registro delle pagine (ANSC_CFG_PAGINA) e si '
           'vedono solo con l’abilitazione corrispondente.')
    return W.salva(im, dest, 'pr_num_menu.png')


def num_richiesta(dest):
    im, dr, y = W.pagina(L, 940, BRICIOLE + ['Richiesta'], 'Numerazione comunale — richiesta',
                         distintivo=('OTP', True), sotto=SOTTO)
    y = W.riga_campi(dr, X, y, C - 200, [('Anno', ANNO, 'select', 2),
                                         ('Numero di elementi', '3', 'testo', 2),
                                         ('Atto SIPO (facoltativo)', '', 'testo', 3)])
    W.bottoni_dx(dr, X + C, y - 52, [('RICHIEDI', W.BLU, True)])
    y += 2
    righe = []
    for n in ('118.402', '118.403', '118.404'):
        righe.append(['90211', 'RSSMRA70A01H501U', '22/10/2026', ANNO, n, '—', '—',
                      ('DISPONIBILE', W.VERDE), ['ok', 'no']])
    y = W.tabella(dr, X, y, C, ['ID richiesta', 'Operatore', 'Data richiesta', 'Anno',
                                'Numero', 'ID ANSC', 'Atto SIPO', 'Stato', 'Azioni'],
                  [110, 170, 130, 70, 100, 250, 110, 140, 112], righe)
    y = W.nota(dr, X, y + 4, C,
               'I tre numeri di un parto trigemino escono consecutivi: gli stacchi sono '
               'serializzati. La spunta segna il numero come Utilizzato e chiede '
               'l’identificativo nazionale; la croce lo segna come Scartato, dopo conferma. '
               'Scartato ed Evento acquisito sono stati finali.')
    y += 6
    y = W.pannello(dr, X, y, C, 'Registrazione a posteriori — numero usato sulla web app '
                                'mentre SIPO non era disponibile', alt=100)
    y = W.riga_campi(dr, X + 16, y + 6, C - 232, [
        ('Anno', ANNO, 'select', 2), ('Numero usato', '118.396', 'testo', 2),
        ('Identificativo nazionale', idansc('118.396'), 'testo', 5)])
    W.bottoni_dx(dr, X + C - 16, y - 52, [('REGISTRA', W.BLU, True)])
    y += 8
    W.nota(dr, X, y, C,
           'Il numero entra nella serie come Utilizzato. Se è uguale o superiore al prossimo, la '
           'serie avanza fino a lì, così che nessuno lo riceva di nuovo; se è inferiore e libero '
           'colma un buco; se è già registrato la registrazione è respinta.', W.GIALLO)
    return W.salva(im, dest, 'pr_num_richiesta.png')


def num_utilizzato(dest):
    larg, alt = 760, 330
    im = Image.new('RGB', (larg, alt), '#8a8d93')
    dr = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 30, 24, larg - 30, alt - 24
    dr.rounded_rectangle([x0, y0, x1, y1], radius=6, fill='white')
    dr.text((x0 + 24, y0 + 20), 'Segna come utilizzato', font=W.fnt(W.F_BLD, 18), fill=W.INK)
    dr.line([(x0, y0 + 56), (x1, y0 + 56)], fill=W.RIGA)
    y = W.riga_campi(dr, x0 + 24, y0 + 80, x1 - x0 - 48, [
        ('Anno', ANNO, 'lettura', 1), ('Numero comunale', '118.402', 'lettura', 1)])
    y = W.riga_campi(dr, x0 + 24, y + 14, x1 - x0 - 48, [
        ('Identificativo nazionale *', idansc('118.402'), 'testo', 3),
        ('Atto SIPO', '', 'testo', 1)])
    W.bottoni_dx(dr, x1 - 24, y + 14, [('ANNULLA', W.MUTED), ('CONFERMA', W.BLU, True)])
    dest = os.path.join(dest, 'pr_num_utilizzato.png')
    im.save(dest)
    return dest


def num_ricerca(dest):
    im, dr, y = W.pagina(L, 1080, BRICIOLE + ['Ricerca e consultazione'],
                         'Numerazione comunale — ricerca e consultazione',
                         distintivo=('OTP', True), azioni_dx=['CREA SERIE'], sotto=SOTTO)
    y = W.pannello(dr, X, y, C, 'Serie della numerazione', alt=142)
    y = W.tabella(dr, X + 16, y, C - 32,
                  ['Anno', 'Sequence', 'Prossimo numero', 'Disponibili', 'Utilizzati',
                   'Scartati', 'Evento acquisito', 'Buchi'],
                  [90, 250, 150, 120, 120, 110, 150, 170], [
                      ['2026', 'SEQ_NUM_COMUNALE_2026', '118.405', '4', '117.893', '391',
                       '112', ('2 — vedi', W.GIALLO)],
                      ['2025', 'SEQ_NUM_COMUNALE_2025', '144.286', '0', '143.702', '468',
                       '115', '0'],
                  ])
    y += 10
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=150)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Richieste da *', '22/10/2026', 'data', 3), ('Richieste a *', '22/10/2026', 'data', 3),
        ('Operatore', 'RSSMRA70A01H501U', 'select', 3), ('Stato', 'Tutti', 'select', 2),
        ('Numero', '', 'testo', 2), ('Atto SIPO', '', 'testo', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y - 6, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 28
    y = W.tabella(dr, X, y, C,
                  ['ID richiesta', 'Operatore', 'Data richiesta', 'Anno', 'Numero', 'ID ANSC',
                   'Atto SIPO', 'Stato', 'Azioni'],
                  [100, 160, 120, 60, 90, 250, 100, 150, 162], [
                      ['90198', 'BNCLRA75B41H501K', '22/10/2026', ANNO, '118.398',
                       idansc('118.398'), '4581270', ('UTILIZZATO', W.BLU), ['vedi']],
                      ['90204', 'RSSMRA70A01H501U', '22/10/2026', ANNO, '118.399', '—', '—',
                       ('SCARTATO', W.MUTED), ['vedi']],
                      ['90207', 'VRDGPP68C12H501T', '22/10/2026', ANNO, '118.400',
                       idansc('118.400'), '—', ('UTILIZZATO', W.BLU), ['vedi', 'mod']],
                      ['90209', 'RSSMRA70A01H501U', '22/10/2026', ANNO, '118.401',
                       idansc('118.401'), '4581302', ('EVENTO ACQUISITO', W.VIOLA), ['vedi']],
                      ['90211', 'RSSMRA70A01H501U', '22/10/2026', ANNO, '118.402', '—', '—',
                       ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='37', pagine=8)
    W.nota(dr, X, y, C,
           'Ordine per ID richiesta e numero, crescenti. I numeri degli atti formati in SIPO li '
           'stacca il concentratore all’anteprima, a nome dell’operatore, e nascono già legati '
           'all’atto: si riconoscono dalla colonna Atto SIPO. La '
           'matita su un numero Utilizzato lega l’atto di SIPO e lo porta a Evento acquisito, '
           'quando l’atto formato sulla web app viene agganciato. Un buco è un numero preso '
           'dalla sequence e mai registrato: non ha una riga, e lo mostra solo la tabella delle '
           'serie. CREA SERIE è riservato all’amministratore.', W.GIALLO)
    return W.salva(im, dest, 'pr_num_ricerca.png')


# ═════════════════════════════════════════════════════════════ conformità (SIPO)
def _sel(segnata, attiva=True):
    return lambda d, x, yy: S.casella(d, x, yy, '', segnata, attiva)


def conformita(dest, stato):
    """stato: 'iniziale', 'anteprima' o 'nessuno'."""
    im, dr, y = S.pagina("Dichiarazione Nascita – Attestazione di conformità degli allegati")
    y = S.arrivo(dr, y, 2)
    y = S.testata_atto(dr, y, "4 FIRMATO DAL DICHIARANTE", S.ID_ANSC)

    scelte = {'iniziale': (True, True, True), 'anteprima': (True, True, False),
              'nessuno': (False, False, False)}[stato]
    y0 = y
    y = S.pannello(dr, y, "Documenti dell’atto da attestare", 248)
    y = S.tabella(dr, y, ("", "Documento", "Tipo (ANSC_09)", "Formato", "Stato (ANSC_08)",
                          "Impronta"),
                  (50, 330, 260, 90, 170, 392),
                  [(_sel(scelte[0]), "Attestazione di nascita", "Attestazione di nascita", "PDF",
                    "Inserito", "c5znaSOl16V2siOutwh0…"),
                   (_sel(scelte[1]), "Processo verbale delle firme", "999 Processo verbale",
                    "PDF", "Inserito", "9424937f3ff137865b01…"),
                   (_sel(scelte[2]), "Delega del padre", "998 Allegato generico", "P7M",
                    "Inserito", "21d305c42509…")],
                  x=S.M + 12)
    S.bottone(dr, S.M + 12, y, "GENERA ATTESTAZIONE DI CONFORMITÀ", stato != 'nessuno')
    y = y0 + 248 + 16

    if stato == 'anteprima':
        y0 = y
        y = S.pannello(dr, y, "Anteprima dell’attestazione (PDF generato da ANSC, R010)", 352)
        S._pagina_pdf(dr, S.M + 12, y, S.W - 2 * S.M - 24,
                      ["Attestazione di nascita – Codice hash: c5znaSOl16V2si…",
                       "Processo verbale delle firme – Codice hash: 9424937f3ff1…"])
        y = y0 + 352 + 16
    else:
        y = S.avviso(dr, y, "L’anteprima dell’attestazione compare dopo GENERA: la produce "
                     "ANSC con R010 a partire dai documenti selezionati." if stato == 'iniziale'
                     else "Nessun documento selezionato: non c’è nulla da attestare. CONTINUA "
                     "salva la scelta e porta alla firma dell’ufficiale.", 'info')

    y0 = y
    y = S.pannello(dr, y, "Firma remota dell’attestazione (R007 /attestazione/firma)", 110)
    larg = (S.W - 2 * S.M - 24 - 24) // 3
    attiva = stato == 'anteprima'
    S.campo(dr, S.M + 12, y, larg, "Utenza *", "utenza.firma.remota" if attiva else "",
            'testo' if attiva else 'lettura')
    S.campo(dr, S.M + 24 + larg, y, larg, "PIN *", "********" if attiva else "",
            'password' if attiva else 'lettura')
    S.campo(dr, S.M + 36 + 2 * larg, y, larg, "OTP del servizio di firma *", "",
            'testo' if attiva else 'lettura')
    y = y0 + 110 + 16

    y = S.pulsantiera(dr, y, [("INDIETRO", True), ("TORNA ALLA COMPILAZIONE", False)],
                      [("ELIMINA EVENTO", True), ("SOSPENDI", True),
                       ("CONTINUA", stato == 'nessuno'), ("FIRMA", attiva)])
    return S.ritaglia(im, y, os.path.join(dest, f'pr_conf_{stato}.png'))


def disegna_tutte(dest=IMG):
    fatti = [num_menu(dest), num_richiesta(dest), num_utilizzato(dest), num_ricerca(dest)]
    fatti += [conformita(dest, s) for s in ('iniziale', 'anteprima', 'nessuno')]
    return fatti


if __name__ == '__main__':
    for p in disegna_tutte():
        print('scritto:', p)
