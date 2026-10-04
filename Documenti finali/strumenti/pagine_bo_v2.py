# -*- coding: utf-8 -*-
"""Figure aggiunte nella v0.2 del disegno del back-office.

  · bo_mfe.png            — la composizione a micro-frontend e il registro che governa il menu
  · bo_chrome.png         — anatomia di testata e piè di pagina, con la ripartizione shell/MFE
  · bo_amministrazione.png — la pagina «Pagine e menu» del registro

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo_v2.py img
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402
import wireframe_bo as W   # noqa: E402
from diagrammi_comune import F_BLD, F_ITA, F_REG, MUTED, centra, fnt   # noqa: E402

L, X = 1240, 24
C = L - 2 * X


# ───────────────────────────────────────────────── 1. composizione a MFE
def mfe(dest):
    im, dr = G.tela(1420, 846, "Il back-office come insieme di micro-frontend",
                    "Quattro unità di rilascio, una per area; le pagine sono rotte a "
                    "caricamento differito dentro ciascuna.")

    G.box(dr, 500, 96, 420, 78, 'viola', "Shell (host)",
          "testata, piè di pagina, profilo, sessione, rotte di primo livello")
    G.box(dr, 60, 96, 380, 78, 'grigio', "Libreria condivisa",
          "componenti, tema, guardie, servizio di sessione — condivisa come singleton")
    G.freccia(dr, (440, 135), (500, 135))

    G.box(dr, 980, 96, 380, 78, 'giallo', "Registro delle pagine",
          "ANSC_CFG_APPLICAZIONE · ANSC_CFG_PAGINA · _ABILITAZ · _TEMA")
    G.freccia(dr, (920, 135), (980, 135))
    G.centra(dr, "legge il menu", fnt(F_ITA, 13), 950, 74, MUTED)

    G.banda(dr, 60, 210, 1380, 664, '#2f6bb0',
            "QUATTRO REMOTE — UNA PER AREA, RILASCIABILI SEPARATAMENTE", '#2f6bb0')
    aree = [
        ('Operativa', 'verde', ['Supervisione atti', 'Dettaglio atto',
                                'Allegati dell’atto', 'Numerazione comunale']),
        ('Notifiche', 'giallo', ['Gestione notifiche']),
        ('Configurazione', 'blu', ['UC — elenco', 'UC — dettaglio', 'Catalogo UC',
                                   'Logiche di scelta', 'Dizionari',
                                   'Riconciliazione', 'Versioni']),
        ('Servizio', 'grigio', ['Comandi e operazioni', 'Pagine e menu']),
    ]
    x = 90
    for nome, col, pagine in aree:
        G.box(dr, x, 252, 300, 62, col, "mfe-" + nome.lower(), nome)
        G.freccia(dr, (x + 150, 192), (x + 150, 252))
        yy = 338
        for p in pagine:
            dr.rounded_rectangle([x + 20, yy, x + 280, yy + 30], radius=5,
                                 outline='#c7cdd6', width=2, fill='white')
            dr.text((x + 34, yy + 8), p, font=fnt(F_REG, 14), fill='#1f2937')
            yy += 38
        centra(dr, "rotte a caricamento differito", fnt(F_ITA, 13), x + 150, yy + 6, MUTED)
        x += 330

    G.box(dr, 480, 700, 460, 62, 'rosso', "Concentratore all-ansc-sipo",
          "l’unico che parla con ANSC: PKCS#12, sessione OTP, firma")
    G.freccia(dr, (710, 664), (710, 700))
    G.centra(dr, "API /ansc/v1", fnt(F_ITA, 13), 790, 668, MUTED)

    G.legenda(dr, 60, 796, [('viola', 'ospite'), ('grigio', 'condiviso'),
                            ('giallo', 'configurazione'), ('rosso', 'back-end')])
    im.save(os.path.join(dest, 'bo_mfe.png'))
    return 'bo_mfe.png'


# ─────────────────────────────────────────── 2. anatomia di testata e piè
def chrome(dest):
    """Anatomia della cornice, sul design system di Roma Capitale.

    ⚠️ L'ambiente non compare: il committente non intende modificare l'interfaccia
    istituzionale. Resta una raccomandazione nel testo, non un elemento disegnato.
    """
    im = Image.new('RGB', (L, 1120), 'white')
    dr = ImageDraw.Draw(im)
    centra(dr, "Anatomia della cornice", fnt(F_BLD, 24), L / 2, 18, '#1b3a5c')
    centra(dr, "In grigio ciò che fornisce la shell; a filetto blu ciò che il "
               "micro-frontend contribuisce.", fnt(F_ITA, 14), L / 2, 52, MUTED)

    y = 92
    # barra di servizio
    dr.rectangle([X, y, L - X, y + 38], fill='#f6f7f8', outline='#e3e5e8')
    dr.text((X + 16, y + 12), 'Layout Esteso', font=fnt(F_BLD, 12), fill=W.INK)
    dr.rounded_rectangle([X + 120, y + 11, X + 156, y + 27], radius=8, fill='#c9ccd1')
    dr.ellipse([X + 140, y + 10, X + 158, y + 28], fill=W.BARRA)
    W.ic_spunta(dr, X + 144, y + 14, 'white')
    dr.text((L - X - 200, y + 12), 'MARIO ROSSI', font=fnt(F_BLD, 12), fill=W.BARRA)
    dr.ellipse([L - X - 84, y + 7, L - X - 52, y + 31], fill=W.BARRA)
    centra(dr, 'MR', fnt(F_BLD, 12), L - X - 68, y + 13, 'white')
    W.ic_chevron(dr, L - X - 42, y + 17)
    dr.text((X + 16, y + 46), 'barra di servizio della shell — preferenza di layout, '
                              'utente e menu del profilo', font=fnt(F_ITA, 12), fill=MUTED)

    # testata istituzionale
    y2 = y + 72
    dr.rectangle([X, y2, L - X, y2 + 78], fill='white', outline='#e3e5e8')
    dr.text((X + 20, y2 + 16), 'ROMA', font=fnt(F_BLD, 40), fill=W.BARRA)
    W._stemma(dr, X + 180, y2 + 20, 38, W.BARRA)
    dr.text((X + 232, y2 + 34), 'Roma Capitale', font=fnt(F_REG, 13), fill=W.BARRA)
    dr.text((X + 16, y2 + 86), 'testata istituzionale della shell — identica in ogni '
                               'applicazione dell’ente', font=fnt(F_ITA, 12), fill=MUTED)

    # fascia del micro-frontend
    y3 = y2 + 112
    dr.rounded_rectangle([X, y3, L - X, y3 + 104], radius=6, outline='#2f6bb0', width=2)
    dr.text((L - X - 260, y3 + 8), 'contribuito dal micro-frontend',
            font=fnt(F_BLD, 12), fill='#2f6bb0')
    dr.text((X + 16, y3 + 12), 'Home › Integrazione ANSC › Supervisione atti',
            font=fnt(F_REG, 12), fill=W.BARRA)
    dr.text((X + 16, y3 + 38), 'Supervisione atti', font=fnt(F_BLD, 20), fill='#1f2937')
    w = dr.textlength('Supervisione atti', font=fnt(F_BLD, 20))
    dr.rounded_rectangle([X + 32 + w, y3 + 38, X + 176 + w, y3 + 64], radius=4,
                         outline=W.VERDE, width=2)
    dr.text((X + 44 + w, y3 + 44), 'OTP · 3h 12m', font=fnt(F_BLD, 12), fill=W.VERDE)
    dr.text((X + 16, y3 + 76), 'briciole di pane · titolo · distintivo di sessione con '
                               'tempo residuo · azioni della pagina',
            font=fnt(F_ITA, 12), fill=MUTED)

    # contenuto
    y4 = y3 + 124
    dr.rounded_rectangle([X, y4, L - X, y4 + 110], radius=6, outline='#c7cdd6', width=2,
                         fill='#fbfcfd')
    centra(dr, "contenuto della pagina", fnt(F_ITA, 15), L / 2, y4 + 46, MUTED)

    # piè di pagina istituzionale
    y5 = y4 + 134
    W.pie_pagina(dr, L, y5, ('Home', 'Supervisione atti', 'Dizionari'))
    dr.text((X + 16, y5 + 258), 'piè di pagina istituzionale della shell — contatti, menu, '
                                'canali, riferimenti legali', font=fnt(F_ITA, 12), fill=MUTED)

    dr.text((X, y5 + 292),
            'Due elementi che il disegno raccomanda e che oggi la cornice istituzionale non '
            'prevede: l’indicazione dell’ambiente e la versione di build.',
            font=fnt(F_REG, 13), fill='#1f2937')
    dr.text((X, y5 + 312),
            'Restano nel testo come raccomandazione, non come elemento disegnato, finché non '
            'saranno concordati con chi governa il design system.',
            font=fnt(F_REG, 13), fill='#1f2937')
    im.save(os.path.join(dest, 'bo_chrome.png'))
    return 'bo_chrome.png'


# ─────────────────────────────────────── 3. amministrazione pagine e menu
def amministrazione(dest):
    im, dr, y = W.pagina(L, 820, ['Home', 'Integrazione ANSC', 'Pagine e menu'],
                         'Pagine e menu',
                         azioni_dx=['ANTEPRIMA DEL MENU'],
                         sotto='Governa che cosa compare nella home, in quale ordine, con '
                               'quale aspetto e per chi. Le modifiche valgono dal prossimo '
                               'caricamento del menu.')
    y = W.riga_campi(dr, X, y, C, [
        ('Applicazione', 'Tutte', 'select', 3), ('Stato', 'Tutti', 'select', 2),
        ('Abilitazione richiesta', '', 'testo', 3), ('Cerca titolo', '', 'testo', 3)])
    y = W.tabella(dr, X, y, C,
                  ['Applicazione', 'Pagina', 'Titolo nel menu', 'Icona', 'Ordine',
                   'In menu', 'Abilitazioni', 'Stato', 'Azioni'],
                  [130, 150, 230, 80, 70, 76, 160, 110, 186], [
                      ['mfe-operativa', 'atti', 'Supervisione atti', 'list', '10',
                       'SI', 'ANSC_ATTI_LEGGI', ('ATTIVA', W.VERDE), ['mod', 'vedi']],
                      ['mfe-operativa', 'atto', 'Dettaglio atto', 'file', '—',
                       'NO', 'ANSC_ATTI_LEGGI', ('ATTIVA', W.VERDE), ['mod', 'vedi']],
                      ['mfe-notifiche', 'notifiche', 'Notifiche ANSC', 'bell', '20',
                       'SI', 'ANSC_NOTIF_GESTISCI', ('ATTIVA', W.VERDE), ['mod', 'vedi']],
                      ['mfe-configurazione', 'uc', 'Configurazione casi d’uso', 'cog', '40',
                       'SI', 'ANSC_CFG_SCRIVI +1', ('ATTIVA', W.VERDE), ['mod', 'vedi']],
                      ['mfe-configurazione', 'formule', 'Formule ministeriali', 'doc', '55',
                       'SI', 'ANSC_CFG_SCRIVI', ('SOSPESA', W.GIALLO), ['mod', 'vedi']],
                      ['mfe-servizio', 'postazioni', 'Postazioni e certificati', 'key', '90',
                       'SI', 'ANSC_AMM_POSTAZIONI', ('NON RILASCIATA', W.MUTED),
                       ['mod', 'vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='16', pagine=2)
    y = W.pannello(dr, X, y, C, 'Modifica della pagina «Supervisione atti»', alt=214)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Titolo nel menu', 'Supervisione atti', 'testo', 4),
        ('Icona', 'list', 'select', 2), ('Ordine', '10', 'testo', 1),
        ('Stato', 'ATTIVA', 'select', 2), ('Mostra nel menu', 'Sì', 'select', 2)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('Sottotitolo', 'gli atti che non hanno concluso il percorso ordinario', 'testo', 6),
        ('Guida in linea', '/guide/supervisione-atti', 'testo', 4)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('Abilitazione di accesso', 'ANSC_ATTI_LEGGI', 'select', 4),
        ('Abilitazioni di azione', 'ANSC_ATTI_RICONCILIA, ANSC_ATTI_ESPORTA', 'testo', 6)])
    W.bottoni(dr, X + 16, y, [('SALVA', W.BLU, True), ('ANNULLA', W.MUTED)])
    return W.salva(im, dest, 'bo_amministrazione.png')


# ────────────────────── 4. riconciliazione: inserimento e modifica
def riconciliazione_dettaglio(dest):
    """La maschera con cui si inserisce o si corregge una corrispondenza.

    ⚠️ L'ordine dei due pannelli è la traduzione grafica della scelta di modello: ciò che
    ANSC dichiara è dato, ciò che SIPO deve far corrispondere è lavoro.
    """
    im, dr, y = W.pagina(L, 900,
                         ['Home', 'Integrazione ANSC', 'Riconciliazione decodifiche',
                          'Nuova corrispondenza'],
                         'Nuova corrispondenza',
                         azioni_dx=['SALVA E PROSSIMA', 'SALVA'],
                         sotto='Versione v13 — BOZZA. La corrispondenza vale da quando si '
                               'dichiara: quelle in vigore non si sovrascrivono, si chiudono.')

    y = W.pannello(dr, X, y, C, 'Lato ANSC — dichiarato dal dominio, non modificabile',
                   alt=124)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Decodifica', '9 — dec_tipo_allegato', 'select', 4),
        ('Valore ANSC *', '112', 'select', 2),
        ('Descrizione ANSC', 'Nulla osta autorità giudiziaria', 'testo', 4),
        ('Validità in ANSC', 'dal 16/10/2023', 'testo', 2)])
    y += 10

    y = W.pannello(dr, X, y, C, 'Lato SIPO — da completare', alt=190)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Schema', 'MATR_USR', 'select', 2),
        ('Tabella', 'CONF_ALLEGATI', 'select', 4),
        ('Campo', 'ID_TIPO', 'select', 3)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('Valore SIPO', '', 'select', 2),
        ('Descrizione SIPO', '', 'testo', 5),
        ('Stato', 'DA MAPPARE', 'testo', 2)])
    y += 10

    y = W.pannello(dr, X, y, C, 'Condizione e validità della corrispondenza', alt=124)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Condizione (facoltativa)', '', 'testo', 6),
        ('Valida dal *', '29/09/2026', 'data', 2),
        ('Valida fino al', '31/12/9999', 'data', 2)])
    y += 10

    y = W.nota(dr, X, y, C,
               'Il valore di ANSC è obbligatorio, quello di SIPO no: una riga senza valore '
               'SIPO è la dichiarazione che quel valore ammesso da ANSC non ha ancora un '
               'corrispondente locale. È ciò che la pagina d’elenco mostra come «da '
               'mappare», ed è il lavoro da fare.', W.GIALLO)
    W.nota(dr, X, y, C,
           'Esiste già una corrispondenza per questa decodifica, questo valore ANSC e questo '
           'campo, valida dal 01/01/2026. Salvando, quella verrà chiusa alla data indicata e '
           'la nuova varrà da lì in avanti: gli atti già depositati restano leggibili con la '
           'corrispondenza in vigore allora.', W.ROSSO)
    return W.salva(im, dest, 'bo_riconciliazione_dettaglio.png')


# ───────────────────────── 5. postazioni e certificati (remote mfOperation)
def certificati(dest):
    """La gestione dei certificati di postazione, come da «screen-app-certificati».

    ⚠️ Il disegno riprende le schermate reali fornite dal committente: ricerca per nome,
    elenco con menu di riga, modulo di caricamento che sostituisce la riga di ricerca.
    """
    im, dr, y = W.pagina(L, 980,
                         ['Home', 'Integrazione ANSC', 'Postazioni e certificati'],
                         'Postazioni e certificati',
                         sotto='Il registro dei certificati abilitati a dialogare con ANPR e '
                               'con ANSC. Ogni riga è una postazione.')

    dr.text((X, y), 'Modo ricerca', font=fnt(F_BLD, 12), fill=W.MUTED)
    y += 20
    W.campo(dr, X, y, 420, 'Nome Certificato', 'Inserisci il nome del certificato')
    W.bottoni(dr, X + 440, y + 3, [('CERCA', W.ROSSO, True), ('ANNULLA', W.MUTED, True),
                                   ('CARICA CERTIFICATO', W.BARRA, True)])
    y += 64

    dr.text((X, y), 'Modo inserimento — sostituisce la riga di ricerca',
            font=fnt(F_BLD, 12), fill=W.MUTED)
    y += 20
    W.campo(dr, X, y, 300, 'Nome Certificato', '058091-PC-2611')
    W.campo(dr, X + 316, y, 240, 'Password', '••••••••')
    W.bottoni(dr, X + 572, y + 3, [('SELEZIONA CERTIFICATO', W.BARRA, True)])
    dr.text((X + 790, y + 12), '058091-PC-2611.p12', font=fnt(F_REG, 12), fill=W.INK)
    W.bottoni(dr, X + 980, y + 3, [('SALVA', W.ROSSO, True), ('ANNULLA', W.MUTED, True)])
    y += 70

    y = W.tabella(dr, X, y, C,
                  ['Certificato', 'Sede', 'Caricato il', 'Caricato da', 'Stato', 'Azioni'],
                  [260, 140, 150, 180, 180, 282], [
                      ['058091-PC-2593', '058091', '12/03/2026', 'm.rossi',
                       ('ATTIVO', W.VERDE), ['vedi', 'del']],
                      ['058091-PC-0300', '058091', '12/03/2026', 'm.rossi',
                       ('ATTIVO', W.VERDE), ['vedi', 'del']],
                      ['058091-PC-0088', '058091', '04/09/2026', 'g.bianchi',
                       ('ATTIVO', W.VERDE), ['vedi', 'del']],
                      ['058091-PC-0304', '058091', '04/09/2026', 'g.bianchi',
                       ('IN SCADENZA', W.GIALLO), ['vedi', 'del']],
                      ['058091-PC-2611', '058091', '02/10/2026', 'm.rossi',
                       ('ATTIVO', W.VERDE), ['vedi', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='7', pagine=2)

    y = W.nota(dr, X, y, C,
               'La cancellazione passa dal menu di riga e chiede conferma in una finestra '
               'che nomina il certificato: «Sei sicuro di voler eliminare il certificato '
               '058091-PC-2611?». L’esito del caricamento è una notifica in alto a destra, '
               'non un cambio di pagina.')
    W.nota(dr, X, y, C,
           'La password del contenitore PKCS#12 non va mostrata in chiaro mentre si digita, '
           'né conservata dopo il caricamento: serve solo ad aprire il file. Le colonne '
           '«Caricato il», «Caricato da» e «Stato» non sono nelle schermate fornite e sono '
           'una proposta: senza, il registro non dice quando un certificato scade né chi '
           'l’ha messo.', W.ROSSO)
    return W.salva(im, dest, 'bo_certificati.png')


if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    os.makedirs(dest, exist_ok=True)
    for f in (mfe, chrome, amministrazione, riconciliazione_dettaglio, certificati):
        print('  scritto', f(dest))
