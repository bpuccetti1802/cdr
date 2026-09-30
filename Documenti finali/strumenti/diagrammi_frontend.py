# -*- coding: utf-8 -*-
"""Le tre figure del documento sul front-end Angular.

  · fe_architettura   — chi sta dove: shell, micro-frontend, libreria condivisa, e il confine
                        oltre il quale il browser non passa mai (i concentratori);
  · fe_tema           — la catena del tema, da Bootstrap Italia alla schermata, e dove si
                        interviene e dove no;
  · fe_caricamento    — caricamento all'avvio (com'è oggi) contro caricamento differito
                        (come deve essere), e che cosa resta comunque all'avvio;
  · fe_schermate      — gli otto passi della formazione dell'atto, con il componente che
                        ciascuno usa: serve a dimostrare che quasi nulla va disegnato da zero.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_frontend.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402


# ───────────────────────────────────────────────────────── architettura

def architettura(dest):
    im, dr = G.tela(1560, 1120, "Il front-end a micro-frontend",
                    "la shell carica una sola volta la libreria e la condivide con tutti i "
                    "micro-frontend; il browser non raggiunge mai ANSC")

    G.banda(dr, 40, 100, 1520, 432, "#2f6bb0", "BROWSER DELL’OPERATORE", "#25548a")
    G.box(dr, 70, 150, 300, 110, "blu", "Shell (host)",
          "rotte di primo livello, layout, config.json")
    G.box(dr, 410, 150, 300, 110, "verde", "MF Stato civile",
          "caricato alla navigazione")
    G.box(dr, 750, 150, 300, 110, "verde", "MF Integrazione ANSC",
          "caricato alla navigazione")
    G.box(dr, 1090, 150, 300, 110, "verde", "MF Back-office",
          "caricato alla navigazione")

    G.box(dr, 70, 320, 1320, 90, "viola", "mf-shared-library — remoteEntry.js",
          "caricata dalla shell UNA volta e condivisa con tutti: design system, componenti, "
          "client HTTP e intercettori, servizi di sessione, abilitazioni, configurazione")
    for x in (220, 560, 900, 1240):
        G.percorso(dr, [(x, 262), (x, 318)], G.MUTED, True, 2)

    G.banda(dr, 40, 470, 1520, 730, "#3f8f5f", "RETE DEL COMUNE",
            "#2f6b47")
    G.box(dr, 70, 520, 300, 100, "grigio", "Servizio di accesso",
          "dell’ente — da definire")
    G.box(dr, 410, 520, 300, 100, "grigio", "Back-end SIPO", "API REST sullo schema esistente")
    G.box(dr, 750, 520, 300, 100, "rosso", "all-ansc-sipo",
          "PKCS#12, OTP di sessione, JWT/JWS")
    G.box(dr, 1090, 520, 300, 100, "rosso", "dec-ansc-sipo", "dizionari (via il primo)")
    G.box(dr, 70, 640, 300, 70, "grigio", "config.json", "uno per ambiente")

    for x in (220, 560, 900, 1240):
        G.freccia(dr, (x, 434), (x, 518), G.ARROW, 2)
    G.freccia(dr, (1088, 570), (1052, 570), G.ARROW, 2)
    dr.text((1064, 482), "R901 per il tramite", font=G.fnt(G.F_ITA, 15), fill=G.MUTED)
    dr.text((1064, 500), "del concentratore", font=G.fnt(G.F_ITA, 15), fill=G.MUTED)

    G.box(dr, 750, 800, 640, 90, "giallo", "ANSC — piattaforma nazionale",
          "raggiunta soltanto dai concentratori, mai dal browser")
    G.freccia(dr, (900, 622), (900, 798), G.ARROW, 3)

    y = 930
    dr.text((70, y), "Tre conseguenze che il disegno impone:", font=G.fnt(G.F_BLD, 18),
            fill="#25548a")
    for i, t in enumerate([
        "la libreria è caricata una sola volta e condivisa: shell e micro-frontend devono avere "
        "la STESSA versione di Angular;",
        "i micro-frontend si caricano quando l’operatore ci arriva, non all’avvio: la shell "
        "conosce le rotte, non il codice;",
        "la sessione OTP verso ANSC vive nel concentratore, non nel browser: il front-end la "
        "consegna e ne mostra il tempo residuo.",
    ]):
        dr.text((90, y + 32 + i * 26), "· " + t, font=G.fnt(G.F_REG, 16), fill=G.MUTED)

    G.legenda(dr, 70, 1070, [("blu", "shell"), ("verde", "micro-frontend"),
                             ("viola", "libreria condivisa"), ("rosso", "concentratori"),
                             ("giallo", "esterno")])
    im.save(dest)
    return dest


# ─────────────────────────────────────────────────── il caricamento

def caricamento(dest):
    im, dr = G.tela(1560, 940, "Caricamento all’avvio e caricamento differito",
                    "a sinistra come funzionano oggi le applicazioni, a destra come devono "
                    "funzionare")

    G.banda(dr, 40, 100, 770, 700, "#b03a48", "OGGI — TUTTO ALL’AVVIO", "#8a2d38")
    G.banda(dr, 790, 100, 1520, 700, "#3f8f5f", "DA ADOTTARE — SU RICHIESTA", "#2f6b47")

    # sinistra: un solo blocco che contiene tutto, scaricato prima della prima schermata
    G.box(dr, 70, 150, 670, 80, "blu", "Avvio della shell", "prima schermata disponibile solo "
          "quando è arrivato tutto")
    G.freccia(dr, (405, 232), (405, 262), G.ARROW, 3)
    bordo, fondo = G.C["rosso"]
    dr.rounded_rectangle([70, 265, 740, 560], radius=12, fill=fondo, outline=bordo, width=3)
    dr.text((90, 278), "Scaricato e inizializzato subito", font=G.fnt(G.F_BLD, 18), fill=G.INK)
    for i, t in enumerate(["libreria condivisa", "MF Stato civile — tutte le maschere",
                           "MF Integrazione ANSC — finalizzazione, documenti, sessione",
                           "MF Back-office — supervisione, notifiche, configurazione",
                           "anche ciò che l’operatore non aprirà, o non può aprire"]):
        dr.text((110, 318 + i * 44), "· " + t, font=G.fnt(G.F_REG, 17),
                fill=G.INK if i < 4 else "#8a2d38")
    for i, t in enumerate(["avvio lento, che cresce a ogni schermata migrata",
                           "un remote irraggiungibile ferma l’intera applicazione",
                           "ogni rilascio di un remote tocca l’avvio di tutti"]):
        dr.text((90, 585 + i * 34), "– " + t, font=G.fnt(G.F_ITA, 16), fill="#8a2d38")

    # destra: shell minima, poi i remote alla navigazione
    G.box(dr, 820, 150, 670, 80, "blu", "Avvio della shell",
          "layout, rotte di primo livello, libreria condivisa")
    y = 270
    for nome, quando in (("MF Stato civile", "quando si apre un atto"),
                         ("MF Integrazione ANSC", "quando si finalizza"),
                         ("MF Back-office", "solo per chi ha l’abilitazione")):
        G.box(dr, 1000, y, 490, 70, "verde", nome, quando, ts=18, ss=15)
        G.percorso(dr, [(860, 232), (860, y + 35), (998, y + 35)], G.ARROW, True, 2)
        y += 95
    for i, t in enumerate(["la prima schermata arriva subito",
                           "un remote guasto spegne una voce, non l’applicazione",
                           "ciascun remote si rilascia senza toccare gli altri"]):
        dr.text((840, 585 + i * 34), "+ " + t, font=G.fnt(G.F_ITA, 16), fill="#2f6b47")

    dr.text((60, 740), "Che cosa NON diventa differito", font=G.fnt(G.F_BLD, 19), fill="#25548a")
    for i, t in enumerate([
        "la libreria condivisa: è la base comune, la shell la carica una volta e la mette a "
        "disposizione di tutti;",
        "il confine asincrono di main.ts (import di bootstrap): serve alla federazione per "
        "negoziare le dipendenze condivise e non è caricamento differito;",
        "le rotte: la shell le conosce tutte, ciò che rimanda è il codice che le realizza.",
    ]):
        for j, rg in enumerate(G.avvolgi(dr, t, G.fnt(G.F_REG, 16), 1400)):
            dr.text((80, 776 + i * 56 + j * 22), ("· " if j == 0 else "   ") + rg,
                    font=G.fnt(G.F_REG, 16), fill=G.MUTED)
    im.save(dest)
    return dest


# ───────────────────────────────────────────────────────────── il tema

def tema(dest):
    im, dr = G.tela(1560, 900, 'La catena del tema',
                    'si personalizza in un punto solo: ciò che sta sopra non si tocca, ciò che '
                    'sta sotto lo eredita')

    passi = [
        ('Bootstrap Italia', ['il design system del Paese', 'AGID · Designers Italia'],
         'giallo', 'non si modifica'),
        ('Personalizzazione', ['boostrap-italia-custom.scss', '$primary: #8E001C'],
         'rosso', 'un file, poche righe'),
        ('Utility del tema', ['20 file in styles/theme', 'palette, spacing, flex…'],
         'verde', 'si estende'),
        ('Componente', ['58 componenti standalone', 'prefisso app-rc-'],
         'blu', 'si usa, non si riscrive'),
        ('Schermata', ['le maschere del progetto', 'nessun CSS proprio'],
         'viola', 'qui non si tematizza'),
    ]
    x = 50
    for titolo, righe, colore, nota in passi:
        G.pila(dr, x, 140, 270, 170, colore, [titolo], righe, [nota])
        if x < 1100:
            G.freccia(dr, (x + 270, 225), (x + 292, 225), G.ARROW, 3)
        x += 292

    G.banda(dr, 40, 360, 1520, 640, '#7b5aa6', 'CHE COSA IL TEMA GIÀ DECIDE', '#5f4483')
    voci = [
        ('Colore', 'primario #8E001C, più quattro gradazioni; sette famiglie semantiche '
                   '(primary, secondary, info, success, warning, error, grey)'),
        ('Tipografia', 'Titillium Web per il testo, Lora per i titoli editoriali, Roboto Mono '
                       'per il monospaziato — i font di Designers Italia, serviti dagli assets'),
        ('Spaziature e griglia', 'utility già pronte: spacing, sizing, flex, grid, breakpoints, '
                                 'display, position'),
        ('Comportamento', 'accordion, header, menu, navbar, sidebar, stepper e carousel hanno '
                          'già le loro correzioni rispetto al comportamento nativo'),
        ('Icone', 'Font Awesome 6 (solid) e lo sprite SVG di Bootstrap Italia'),
    ]
    y = 400
    for testa, corpo in voci:
        dr.text((70, y), testa, font=G.fnt(G.F_BLD, 18), fill='#5f4483')
        for i, rg in enumerate(G.avvolgi(dr, corpo, G.fnt(G.F_REG, 16), 1180)):
            dr.text((320, y + i * 22), rg, font=G.fnt(G.F_REG, 16), fill=G.MUTED)
        y += 48

    dr.text((70, 680), 'La regola che ne discende', font=G.fnt(G.F_BLD, 19), fill='#b03a48')
    for i, t in enumerate([
        'Nessuna schermata definisce colori, font o spaziature proprie: se una cosa non si '
        'ottiene con le utility, manca una utility — e si aggiunge alla libreria, non alla '
        'schermata.',
        'Nessun componente si riscrive localmente: se serve una variante, si estende il '
        'componente condiviso e la variante torna a tutti.',
        'ATTENZIONE: è la differenza fra avere un design system e averne una copia per progetto. La '
        'seconda si scopre quando il committente cambia un colore.',
    ]):
        for j, rg in enumerate(G.avvolgi(dr, t, G.fnt(G.F_REG, 16), 1400)):
            dr.text((90, 714 + i * 52 + j * 22), ('· ' if j == 0 else '   ') + rg,
                    font=G.fnt(G.F_REG, 16), fill=G.MUTED)
    im.save(dest)
    return dest


# ───────────────────────────────────────────────────────── le schermate

def schermate(dest):
    im, dr = G.tela(1560, 1000, 'Gli otto passi e i componenti che li realizzano',
                    'quasi nulla va disegnato da zero: la colonna di destra dice che cosa manca '
                    'davvero')

    passi = [
        ('1 · Scelta dell’operazione', 'menu di SIPO, tipo atto', 'menu · navbar · breadcrumb',
         ''),
        ('2 · Acquisizione del token', 'l’OTP generato sulla web app ANSC',
         'otp · notification-toast', 'consegna del codice di sessione, con tempo residuo'),
        ('3 · Compilazione', 'le maschere di SIPO', 'form-elements (20) · accordion · grid',
         'campi solo-ANSC'),
        ('4 · Ricerca degli intestatari', 'R005 per il tramite del concentratore',
         'select-autocomplete · table · modal', ''),
        ('5 · Dati e documenti richiesti', 'ciò che l’UC determinato pretende',
         'stepper · table · badge', ''),
        ('6 · Registrazione dei file', 'gli allegati, fino al deposito',
         'upload-drag-drop · document-single-upload · pdf-viewer',
         'maschere di caricamento dei documenti'),
        ('7 · Deposito e firma', 'R009 poi R006/R007', 'stepper · spinner · modal',
         'stato ANSC nelle maschere di ricerca e dettaglio'),
        ('8 · Atto formato', 'il punto di non ritorno', 'notification-toast · card-wrapper', ''),
    ]
    y = 110
    dr.text((60, y), 'Passo', font=G.fnt(G.F_BLD, 17), fill='#25548a')
    dr.text((470, y), 'Componenti della libreria', font=G.fnt(G.F_BLD, 17), fill='#3f8f5f')
    dr.text((1130, y), 'Che cosa manca', font=G.fnt(G.F_BLD, 17), fill='#b03a48')
    y += 30
    for titolo, sotto, comp, manca in passi:
        bordo, fondo = G.C['blu']
        dr.rounded_rectangle([50, y, 450, y + 74], radius=9, fill=fondo, outline=bordo, width=2)
        dr.text((66, y + 12), titolo, font=G.fnt(G.F_BLD, 16), fill=G.INK)
        dr.text((66, y + 38), sotto, font=G.fnt(G.F_ITA, 14), fill=G.MUTED)

        bordo, fondo = G.C['verde']
        dr.rounded_rectangle([470, y, 1100, y + 74], radius=9, fill=fondo, outline=bordo, width=2)
        for i, rg in enumerate(G.avvolgi(dr, comp, G.fnt(G.F_REG, 15), 600)):
            dr.text((486, y + 14 + i * 21), rg, font=G.fnt(G.F_REG, 15), fill=G.INK)
        G.freccia(dr, (452, y + 37), (468, y + 37), G.ARROW, 2)

        if manca:
            bordo, fondo = G.C['rosso']
            dr.rounded_rectangle([1120, y, 1510, y + 74], radius=9, fill=fondo, outline=bordo,
                                 width=2)
            for i, rg in enumerate(G.avvolgi(dr, manca, G.fnt(G.F_REG, 15), 360)):
                dr.text((1136, y + 24 + i * 21), rg, font=G.fnt(G.F_REG, 15), fill=G.INK)
        y += 88

    dr.text((60, y + 10), 'ATTENZIONE: le quattro voci in rosso sono le sole funzioni da costruire, e '
                          'nessuna è un problema di grafica: sono maschere che SIPO non ha.',
            font=G.fnt(G.F_BLD, 17), fill='#b03a48')
    im.save(dest)
    return dest


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    for f, nome in ((architettura, 'fe_architettura.png'), (tema, 'fe_tema.png'),
                    (schermate, 'fe_schermate.png'), (caricamento, 'fe_caricamento.png')):
        print('scritto:', f(os.path.join(out, nome)))
