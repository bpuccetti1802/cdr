# -*- coding: utf-8 -*-
"""Pagine del back-office per il recupero in SIPO degli atti formati sulla web app ANSC
(ANALISI_Recupero-Atti-WebApp_SIPO-ANSC v0.2, 10/11/2026).

  · bo_rec_elenco.png   — «Recupero dalla web app»: numeri staccati in attesa e ricerca in ANSC
  · bo_rec_aggancio.png — «Aggancio dell'atto»: controlli, livello di recupero, conferma
  · bo_rec_esito.png    — esito dell'aggancio: che cosa è stato scritto e che cosa no
  · bo_rec_otp.png      — la finestra aperta dal pulsante dell'OTP nella testata

Nella barra di servizio, accanto all'utente, lo stato del codice di sessione verso ANSC e il
pulsante RICHIEDI OTP / RINNOVA OTP (v0.3, rilievo dell'utente).

Cornice di Roma Capitale (wireframe_bo), come le altre pagine del back-office. Nomi, codici
fiscali, numeri e identificativi sono inventati.

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo_recupero.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wireframe_bo as W   # noqa: E402

L, X = 1240, 24
C = L - 2 * X
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'recupero')
BRICIOLE = ['Home', 'Integrazione ANSC', 'Recupero dalla web app']
MENU = ('Home', 'Supervisione atti', 'Recupero dalla web app')


def testata_otp(dr, minuti=161):
    """Stato dell'OTP e pulsante nella barra di servizio, a sinistra dell'utente."""
    f = W.fnt(W.F_BLD, 12)
    xu = L - 28 - 14 - 34 - dr.textlength('MARIO ROSSI', font=f)
    xr = xu - 28
    etichetta = 'RINNOVA OTP' if minuti else 'RICHIEDI OTP'
    wb = int(dr.textlength(etichetta, font=f)) + 44
    dr.rounded_rectangle([xr - wb, 7, xr, 33], radius=4, fill=W.BARRA)
    # chiave
    kx, ky = xr - wb + 12, 14
    dr.ellipse([kx, ky, kx + 10, ky + 10], outline='white', width=2)
    dr.line([(kx + 10, ky + 5), (kx + 20, ky + 5)], fill='white', width=2)
    dr.line([(kx + 17, ky + 5), (kx + 17, ky + 10)], fill='white', width=2)
    dr.text((xr - wb + 36, 13), etichetta, font=f, fill='white')
    if minuti:
        stato, col = 'OTP ANSC valido · %d h %02d min' % (minuti // 60, minuti % 60), W.VERDE
    else:
        stato, col = 'OTP ANSC assente', W.ROSSO
    ws = dr.textlength(stato, font=f)
    xs = xr - wb - 16 - ws
    dr.text((xs, 13), stato, font=f, fill=col)
    dr.ellipse([xs - 16, 15, xs - 6, 25], fill=col)


def pagina(*a, minuti=161, **k):
    im, dr, y = W.pagina(L, *a, **k)
    testata_otp(dr, minuti)
    return im, dr, y


def elenco(dest=DEST):
    im, dr, y = pagina(1500, BRICIOLE, 'Recupero dalla web app',
                         azioni_dx=['ESPORTA'],
                         sotto='Atti formati sulla web app con un numero staccato in SIPO: '
                               'si ritrovano in ANSC e si agganciano all’atto di SIPO.')
    # in sintesi
    y = W.pannello(dr, X, y, C, 'In sintesi', alt=178)
    y = W.tabella(dr, X + 16, y, C - 32, ['Situazione', 'Quanti', 'Che cosa significa'],
                  [300, 90, 770], [
                      [('IN ATTESA', W.BLU), '12',
                       'Numeri staccati per la web app e non ancora ricondotti a un atto ANSC'],
                      [('IN SCADENZA', W.GIALLO), '3',
                       'Mancano meno di 2 giorni al passaggio automatico a «Scartato»'],
                      [('SENZA NUMERO SIPO', W.ROSSO), '1',
                       'Atto di Roma trovato in ANSC con un numero che SIPO non ha staccato'],
                  ])
    y += 18
    # numeri in attesa
    y = W.pannello(dr, X, y, C, 'Numeri staccati in attesa dell’atto ANSC')
    y = W.tabella(dr, X, y, C,
                  ['Numero', 'Staccato il', 'Operatore', 'Municipio', 'Tipo atto previsto',
                   'Atto SIPO', 'Giorni', 'Ultima ricerca', 'Azioni'],
                  [90, 110, 160, 90, 230, 100, 80, 200, 132], [
                      ['004812', '12/03/2027', 'BNCLRA75B41H501K', 'I',
                       'Dichiarazione di nascita', '4581302', '1', 'non eseguita',
                       ['vedi', 'mod']],
                      ['004797', '10/03/2027', 'RSSMRA70A01H501U', 'VII',
                       'Dichiarazione di morte', '—', '3', '13/03 · nessun atto',
                       ['vedi', 'mod']],
                      ['004760', '07/03/2027', 'VRDGPP68C12H501T', 'XII',
                       'Riconoscimento', '4580977', ('6', W.GIALLO), '12/03 · nessun atto',
                       ['vedi', 'mod']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='12', pagine=3)
    y = W.nota(dr, X, y - 4, C,
           'L’occhio apre la scheda del numero (chi, quando, per quale atto). La matita cerca '
           'in ANSC l’atto con quel numero comunale (R005, criterio idComunale) e, se lo trova, '
           'porta all’aggancio. I numeri oltre la soglia configurata passano a «Scartato» da '
           'soli e lasciano l’elenco.')
    y += 10
    # ricerca in ANSC
    y = W.pannello(dr, X, y, C, 'Ricerca in ANSC degli atti di Roma', alt=150)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Data da', '13/03/2027', 'data', 2), ('Data a', '13/03/2027', 'data', 2),
        ('Tipo evento', 'Tutti', 'select', 3), ('Numero comunale', '', 'testo', 2),
        ('Identificativo ANSC', '', 'testo', 2),
        ('Abbinamento', 'Tutti tranne recuperati', 'select', 3)])
    y = W.bottoni_dx(dr, X + C - 16, y - 6, [('PULISCI', W.MUTED),
                                               ('CERCA IN ANSC', W.BLU, True)])
    y += 28
    y = W.tabella(dr, X, y, C,
                  ['Identificativo ANSC', 'Numero', 'Formato il', 'Caso d’uso',
                   'Intestatario', 'Stato ANSC', 'Abbinamento', 'Azioni'],
                  [140, 80, 110, 210, 200, 150, 190, 112], [
                      ['9017734', '004812', '13/03/2027', 'Dic_Nasc_008',
                       'KOWALSKA ZOFIA', ('FIRMATO DA USC', W.VERDE),
                       ('ABBINABILE', W.VERDE), ['vedi', 'ok']],
                      ['9017761', '004818', '13/03/2027', 'Morte_002', 'BIANCHI PIETRO',
                       ('FIRMATO DA USC', W.VERDE), ('SENZA NUMERO SIPO', W.ROSSO),
                       ['vedi']],
                      ['9017790', '004811', '13/03/2027', 'Dic_Nasc_001', 'GALLI SOFIA',
                       ('FIRMATO DA USC', W.VERDE), ('GIÀ IN SIPO', W.MUTED), ['vedi']],
                      ['9017802', '—', '13/03/2027', 'Morte_001', 'NERI GIULIA',
                       ('VALIDATO', W.GIALLO), ('NON FIRMATO', W.GIALLO), ['vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='4', pagine=1)
    W.nota(dr, X, y - 4, C,
           'La ricerca chiama R005 con il comune di Roma e l’intervallo di date; lo stato e '
           'l’abbinamento li calcola SIPO sulla risposta. La spunta porta all’aggancio ed è '
           'attiva solo per gli atti ABBINABILI; gli altri si guardano con l’occhio. «GIÀ IN '
           'SIPO» comprende gli atti formati da SIPO, che non si recuperano.', W.GIALLO)
    return W.salva(im, dest, 'bo_rec_elenco.png', voci_menu=MENU)


def aggancio(dest=DEST):
    im, dr, y = pagina(1500, BRICIOLE + ['Aggancio'],
                         'Aggancio dell’atto ANSC 9017734',
                         sotto='L’atto è stato riletto da ANSC all’apertura della pagina: i '
                               'controlli valgono per la versione attuale.')
    y = W.pannello(dr, X, y, C, 'L’atto in ANSC', alt=128)
    y = W.righe_etichette(dr, X + 16, y, [
        ('Identificativo ANSC', '9017734'), ('Numero comunale', '004812'),
        ('Anno', '2027'), ('Caso d’uso', '11114000 · Dic_Nasc_008'),
        ('Stato', '5 FIRMATO DA USC'), ('Formato il', '13/03/2027 11:42'),
        ('Intestatario', 'KOWALSKA ZOFIA'), ('Codice fiscale', 'KWLZFO27C53Z127S'),
        ('Ufficiale', 'BNCLRA75B41H501K')], C - 32)
    y += 14
    y = W.pannello(dr, X, y, C, 'Controlli')
    y = W.tabella(dr, X, y, C, ['Controllo', 'In ANSC', 'In SIPO', 'Esito'],
                  [300, 330, 330, 232], [
                      ['Numero comunale', '004812', '004812 · Disponibile',
                       ('UGUALE', W.VERDE)],
                      ['Comune di registrazione', 'ROMA', 'ROMA', ('UGUALE', W.VERDE)],
                      ['Stato dell’atto', '5 FIRMATO DA USC', '—', ('AMMESSO', W.VERDE)],
                      ['Tipo di atto', 'Dichiarazione di nascita', 'Dichiarazione di nascita',
                       ('COERENTE', W.VERDE)],
                      ['Intestatario', 'KWLZFO27C53Z127S', 'KWLZFO27C53Z127S',
                       ('UGUALE', W.VERDE)],
                      ['Atto di SIPO', '—', '4581302 · in attesa della web app',
                       ('DA COMPLETARE', W.BLU)],
                      ['Già recuperato', '—', 'nessun aggancio per 9017734',
                       ('NO', W.VERDE)],
                  ])
    y += 10
    y = W.pannello(dr, X, y, C, 'Livello del recupero', alt=176)
    for i, (sel, tit, desc, attivo) in enumerate([
        (False, 'L1 · Il riferimento', 'store con canale WEBAPP e modello evento, colonne ANSC '
         'dell’atto in anagrafe', True),
        (True, 'L2 · La scheda essenziale', 'in più: atto di stato civile, intestatari e '
         'testo dell’atto — proposto per questo tipo di atto', True),
        (False, 'L3 · L’importazione completa', 'non disponibile: Dic_Nasc_008 è un caso '
         'd’uso non configurato', False)]):
        yy = y + i * 40
        col = W.INK if attivo else W.MUTED
        dr.ellipse([X + 20, yy + 2, X + 36, yy + 18], outline=col, width=2)
        if sel:
            dr.ellipse([X + 24, yy + 6, X + 32, yy + 14], fill=W.BLU)
        dr.text((X + 48, yy + 1), tit, font=W.fnt(W.F_BLD, 12), fill=col)
        dr.text((X + 270, yy + 1), desc, font=W.fnt(W.F_REG, 12), fill=col)
    y += 140
    y = W.nota(dr, X, y, C,
           'Con la conferma SIPO scrive i dati del livello scelto e segna il numero come '
           'Utilizzato con l’identificativo ANSC. Non definisce l’atto, non genera il formulario '
           'né le annotazioni, non chiama ANPR: l’allineamento anagrafico lo ha già predisposto '
           'ANSC.', W.GIALLO)
    y += 6
    W.bottoni_dx(dr, X + C, y, [('ANNULLA', W.MUTED), ('AGGANCIA', W.BLU, True)])
    return W.salva(im, dest, 'bo_rec_aggancio.png', voci_menu=MENU)


def esito(dest=DEST):
    im, dr, y = pagina(1100, BRICIOLE + ['Esito'], 'Atto ANSC 9017734 agganciato',
                         distintivo=('AGGANCIATO', True),
                         sotto='Recupero di livello L2 eseguito il 13/03/2027 alle 15:07 da '
                               'BNCLRA75B41H501K.')
    y = W.pannello(dr, X, y, C, 'Che cosa è stato scritto')
    y = W.tabella(dr, X, y, C, ['Passo', 'Dove', 'Esito'], [420, 520, 252], [
        ['Stato dell’atto, canale WEBAPP, modello evento', 'ANSC_STATO_ATTO',
         ('ESEGUITO', W.VERDE)],
        ['Colonne ANSC dell’atto in anagrafe', 'ANAG_USR.ATTO', ('ESEGUITO', W.VERDE)],
        ['Atto di stato civile, intestatari e testo', 'MATR_USR.ATTO e tabella d’area',
         ('ESEGUITO', W.VERDE)],
        ['Identificativi dei soggetti, solo dove mancano', 'ANSC_SOGGETTO_IDENTIFICATIVI',
         ('ESEGUITO', W.VERDE)],
        ['Numero 004812 → Utilizzato con 9017734', 'be-numeratore-comunale',
         ('ESEGUITO', W.VERDE)],
        ['Numero → Evento acquisito', 'be-numeratore-comunale',
         ('NON DISPONIBILE', W.GIALLO)],
        ['Traccia dell’operazione', 'ANSC_LOG_AUDIT', ('ESEGUITO', W.VERDE)],
    ])
    y += 10
    y = W.pannello(dr, X, y, C, 'Che cosa non si è fatto, di proposito')
    y = W.tabella(dr, X, y, C, ['Operazione', 'Perché'], [420, 772], [
        ['Definizione dell’atto e formulario', 'L’atto è già formato e firmato in ANSC'],
        ['Allineamento con ANPR', 'La comunicazione anagrafica la predispone ANSC'],
        ['Annotazioni e comunicazioni di SIPO', 'Le genera ANSC con le notifiche'],
    ])
    y += 10
    W.bottoni_dx(dr, X + C, y, [('TORNA ALL’ELENCO', W.MUTED),
                                  ('APRI L’ATTO IN SIPO', W.BLU, True)])
    return W.salva(im, dest, 'bo_rec_esito.png', voci_menu=MENU)


def otp(dest=DEST):
    """La finestra aperta da RICHIEDI OTP, sulla pagina dell'elenco senza sessione."""
    from PIL import Image, ImageDraw
    im, dr, y = pagina(760, BRICIOLE, 'Recupero dalla web app', minuti=0,
                       sotto='Atti formati sulla web app con un numero staccato in SIPO: '
                             'si ritrovano in ANSC e si agganciano all’atto di SIPO.')
    y = W.pannello(dr, X, y, C, 'Numeri staccati in attesa dell’atto ANSC')
    W.tabella(dr, X, y, C, ['Numero', 'Staccato il', 'Operatore', 'Tipo atto previsto',
                            'Giorni', 'Azioni'], [120, 140, 220, 400, 120, 192], [
        ['004812', '12/03/2027', 'BNCLRA75B41H501K', 'Dichiarazione di nascita', '1',
         ['vedi', 'mod']],
        ['004797', '10/03/2027', 'RSSMRA70A01H501U', 'Dichiarazione di morte', '3',
         ['vedi', 'mod']],
        ['004760', '07/03/2027', 'VRDGPP68C12H501T', 'Riconoscimento', '6',
         ['vedi', 'mod']]])
    # velo sul contenuto, la testata resta leggibile
    velo = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(velo).rectangle([0, 120, L, im.size[1]], fill=(31, 41, 55, 120))
    im = Image.alpha_composite(im.convert('RGBA'), velo).convert('RGB')
    dr = ImageDraw.Draw(im)
    mx, my, mw, mh = 270, 150, 700, 470
    dr.rounded_rectangle([mx, my, mx + mw, my + mh], radius=8, fill='white',
                         outline=W.BORDO)
    dr.text((mx + 24, my + 20), 'Codice di sessione verso ANSC', font=W.fnt(W.F_BLD, 18),
            fill=W.INK)
    W.ic_croce(dr, mx + mw - 34, my + 22, W.MUTED)
    dr.line([(mx, my + 56), (mx + mw, my + 56)], fill=W.RIGA)
    yy = my + 72
    for t in ['1.  Apri la web app OTP di ANSC e accedi con smart card o SPID.',
              '2.  Genera il codice: vale 4 ore.',
              '3.  Incollalo qui sotto e conferma.']:
        dr.text((mx + 24, yy), t, font=W.fnt(W.F_REG, 13), fill=W.INK)
        yy += 24
    W.bottoni(dr, mx + 24, yy + 8, [('APRI LA WEB APP OTP', W.BLU)])
    W.campo(dr, mx + 24, yy + 70, mw - 48, 'Codice OTP', '••••••••')
    yy = W.nota(dr, mx + 24, yy + 128, mw - 48,
                'Il codice va al concentratore, che lo custodisce legato a te e a questa '
                'postazione e lo usa per ogni chiamata ad ANSC fino alla scadenza. Il browser '
                'non lo conserva.')
    yy = W.nota(dr, mx + 24, yy, mw - 48,
                'Sotto i 15 minuti residui lo stato in testata diventa giallo: conviene '
                'rinnovare prima di una ricerca o di un aggancio, per non fermarsi a metà.',
                W.GIALLO)
    W.bottoni_dx(dr, mx + mw - 24, my + mh - 50, [('ANNULLA', W.MUTED),
                                                  ('CONFERMA', W.BLU, True)])
    return W.salva(im, dest, 'bo_rec_otp.png', voci_menu=MENU)


if __name__ == '__main__':
    for f in (elenco, aggancio, esito, otp):
        print('  scritto', f())
