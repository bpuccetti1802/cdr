# -*- coding: utf-8 -*-
"""Figure dell'AS-IS su autenticazione e profilazione in SIPO.

  · aut_catena.png   — la catena effettiva dell'accesso, dal portale alla chiamata REST
  · prof_modello.png — le tabelle della profilazione e il perno R_UTENTI_RUOLI

⚠️ Niente emoji: Arial non ha il glifo di avvertimento. Il richiamo è un pallino
rosso con il punto esclamativo, disegnato da `badge()`.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_sicurezza.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')


def badge(dr, x, y, r=15):
    """Il richiamo di attenzione: cerchio rosso con punto esclamativo."""
    dr.ellipse([x - r, y - r, x + r, y + r], fill='#b03a48', outline='white', width=2)
    G.centra(dr, '!', G.fnt(G.F_BLD, 21), x, y - 12, 'white')


def catena():
    im, dr = G.tela(
        1580, 1215, "L’autenticazione in SIPO: la catena effettiva",
        "Dall’accesso al portale alla chiamata REST verso i back-end. Nessuno dei passi "
        "interni a SIPO verifica una credenziale.")

    G.banda(dr, 40, 92, 1540, 268, '#9aa3ad', "FUORI DA SIPO", G.MUTED)
    G.box(dr, 66, 138, 250, 104, 'grigio', "Browser dell’operatore",
          "postazione dell’ufficio")
    G.box(dr, 356, 138, 300, 104, 'viola', "SSO di portale",
          "Oracle Access Manager · comune.roma.it")
    G.box(dr, 696, 138, 330, 104, 'rosso', "Reverse proxy / giunzione",
          "inietta gli header iv-user, sysgroup, iv-codfis…")
    G.box(dr, 1066, 138, 300, 104, 'grigio', "Certificato di postazione",
          "validato qui: SIPO ne riceve il solo numero di serie")
    badge(dr, 1026, 148)
    G.freccia(dr, (316, 190), (356, 190))
    G.freccia(dr, (656, 190), (696, 190))
    G.freccia(dr, (1026, 214), (1066, 214))

    G.banda(dr, 40, 300, 1540, 754, '#2f6bb0', "SIPO — APPLICAZIONE WEB (THYMELEAF)", '#2f6bb0')
    G.box(dr, 66, 352, 440, 160, 'blu', "CdRLoginFilter",
          "registrato sul solo pattern /init/*. Legge l’identità dagli header, carica ruoli e "
          "funzionalità dal database, scrive LOGIN_USER in sessione")
    badge(dr, 492, 366)
    G.box(dr, 556, 352, 430, 160, 'blu', "CustomAuthenticationProcessingFilter",
          "costruisce PreAuthenticatedAuthenticationToken(codice fiscale, \"\"): "
          "le credenziali sono la stringa vuota")
    G.box(dr, 1036, 352, 480, 160, 'giallo', "SecurityConfig",
          "210 antMatchers().hasAnyRole() in una lista unica. "
          "Nessun anyRequest() di chiusura")
    badge(dr, 1502, 366)
    G.freccia(dr, (506, 432), (556, 432))
    G.freccia(dr, (986, 432), (1036, 432))

    G.box(dr, 66, 556, 920, 116, 'verde', "HttpSession — attributo LOGIN_USER",
          "l’oggetto User con oltre cinquanta campi: ruoli, aree tematiche, funzionalità, "
          "idOrganizzazione. È la fonte di verità applicativa: vi ricorrono 8.975 righe di codice")
    G.box(dr, 1036, 556, 480, 116, 'grigio', "SecurityContext",
          "solo le authority ROLE_<ruolo>. Nessun controller applicativo "
          "legge da qui l’identità")
    G.freccia(dr, (286, 512), (286, 556))
    G.freccia(dr, (1276, 512), (1276, 556))

    G.box(dr, 430, 716, 700, 116, 'viola', "Oracle — schema ANAG_USR",
          "UTENTI · CONF_RUOLI · R_UTENTI_RUOLI · CONF_FUNZIONALITA · "
          "CONF_AREE_TEMATICHE · CONF_AMBITO")
    G.percorso(dr, [(286, 672), (286, 774), (430, 774)])

    G.box(dr, 66, 886, 470, 140, 'giallo', "RestClient",
          "OAuth2 password grant verso /oauth/token, un token nuovo a ogni chiamata. "
          "L’utenza tecnica è scelta sul PRIMO ruolo dell’operatore")
    badge(dr, 522, 900)
    G.box(dr, 586, 886, 450, 140, 'blu', "Back-end REST",
          "45 moduli su 53. Sessione STATELESS, 171 antMatchers().authenticated(), "
          "@PreAuthorize in 374 file su liste di ruoli")
    G.box(dr, 1086, 886, 430, 140, 'rosso', "Una sola chiave di firma",
          "security.signing-key identica in 45 file: un token vale su tutti i back-end")
    badge(dr, 1502, 900)
    G.freccia(dr, (536, 956), (586, 956))
    G.freccia(dr, (1036, 956), (1086, 956))
    G.freccia(dr, (150, 672), (150, 886))

    G.legenda(dr, 66, 1076, [('viola', 'fuori dal perimetro applicativo'),
                             ('blu', 'catena di accesso'),
                             ('giallo', 'autorizzazione'),
                             ('verde', 'dove risiede l’identità'),
                             ('rosso', 'punto di fiducia non verificato')])
    G.centra(dr, "Il pallino rosso segna i quattro punti in cui la catena si fida di un "
                 "dato che non controlla.", G.fnt(G.F_ITA, 16), 790, 1152, G.MUTED)
    im.save(os.path.join(IMG, 'aut_catena.png'))
    return 'aut_catena.png'


def modello():
    im, dr = G.tela(
        1840, 1010, "Il modello dati della profilazione",
        "Il permesso non è associato al ruolo: passa sempre per l’utente, "
        "attraverso il perno R_UTENTI_RUOLI.")

    G.centra(dr, "CHE COSA SI PUÒ FARE", G.fnt(G.F_BLD, 15), 210, 92, G.MUTED)
    G.scheda(dr, 60, 116, 300, 'viola', "CONF_AMBITO",
             [('PK', 'ID_AMBITO'), ('', 'DESCRIZIONE')],
             "1=ANAGRAFE 2=STATO CIVILE 3=ELETT. 4=STAT.")
    G.scheda(dr, 60, 288, 300, 'viola', "CONF_AREE_TEMATICHE",
             [('PK', 'ID_AREE_TEMATICHE'), ('FK', 'ID_AMBITO'),
              ('', 'DESCRIZIONE, URL_PAGE'), ('', 'ORDINE (non mappata)')])
    G.scheda(dr, 60, 470, 300, 'viola', "CONF_FUNZIONALITA",
             [('PK', 'ID'), ('FK', 'ID_AREA_TEMATICA'),
              ('', 'DESCRIZIONE, URL_PAGE'), ('', 'CITTADINO')],
             "l’unico catalogo di «azioni» esistente")
    G.freccia(dr, (210, 288), (210, 222))
    G.freccia(dr, (210, 470), (210, 412))

    G.scheda(dr, 500, 300, 340, 'rosso', "R_UTENTI_RUOLI",
             [('PK', 'ID (da sequenza)'), ('FK', 'ID_UTENTE'), ('FK', 'ID_RUOLO'),
              ('FK', 'ID_AREA_TEMATICA'), ('FK', 'ID_FUNZIONALITA')],
             "nessuna validità temporale, nessun ambito")
    badge(dr, 832, 314)

    G.centra(dr, "CHI", G.fnt(G.F_BLD, 15), 1150, 92, G.MUTED)
    G.scheda(dr, 980, 116, 340, 'blu', "UTENTI",
             [('PK', 'ID'), ('', 'NOME_UTENTE, CODICE_FISCALE'),
              ('', 'FLG_ATTIVO, FLG_CANCELLATO'), ('FK', 'ID_ORGANIZZAZIONE'),
              ('FK', 'ID_SEDE_MUNICIPIO'), ('FK', 'ID_STRUTTURA_CONV')])
    G.scheda(dr, 980, 350, 340, 'blu', "CONF_RUOLI",
             [('PK', 'ID'), ('', 'DESCRIZIONE'), ('', 'RUOLO (non mappata: solo SQL)')])
    badge(dr, 1312, 364)

    G.centra(dr, "IN QUALE AMBITO", G.fnt(G.F_BLD, 15), 1610, 92, G.MUTED)
    G.scheda(dr, 1440, 116, 340, 'grigio', "CONF_STRUTTURE_INTERNE_RC",
             [('PK', 'ID'), ('', 'CODICE_STRUTTURA'), ('', 'DESCRIZIONE_STRUTTURA'),
              ('', 'FLG_GRUPPO_VIGILI')],
             "l’ambito organizzativo dell’utente")
    G.scheda(dr, 1440, 320, 340, 'grigio', "CONF_SEDE_MUNICIPIO",
             [('PK', 'ID_SEDE_MUNICIPIO')],
             "non propagata sull’oggetto User di sessione")
    badge(dr, 1772, 334)
    G.scheda(dr, 1440, 490, 340, 'grigio', "CONF_STRUTTURE_CONV",
             [('PK', 'ID')], "professionisti ed enti esterni")

    G.freccia(dr, (840, 350), (980, 250))
    G.freccia(dr, (840, 400), (980, 400))
    G.freccia(dr, (500, 350), (360, 345))
    G.freccia(dr, (500, 425), (360, 505))
    G.freccia(dr, (1320, 176), (1440, 176))
    G.percorso(dr, [(1320, 214), (1390, 214), (1390, 362), (1440, 362)])
    G.percorso(dr, [(1320, 252), (1365, 252), (1365, 532), (1440, 532)])

    G.banda(dr, 460, 664, 1260, 886, '#d9a441',
            "UTENZE TECNICHE DI BACK-END — ALTRA POPOLAZIONE", '#a8792a')
    G.scheda(dr, 500, 716, 300, 'giallo', "CONF_APP_USER",
             [('PK', 'ID'), ('', 'USERNAME, PASSWORD')],
             "non gestita dal back-office utenze")
    G.scheda(dr, 880, 716, 340, 'giallo', "CONF_APP_ROLE",
             [('PK', 'ID'), ('FK', 'ID_APP_USER'),
              ('', 'ID_CONF_RUOLI (per valore)'), ('', 'PROFILO_BE')],
             "il raccordo a CONF_RUOLI non è una relazione JPA")
    G.freccia(dr, (800, 766), (880, 766))
    G.percorso(dr, [(1050, 716), (1050, 451)], tratteggio=True,
               etichetta="per valore", pos=(1064, 560))

    G.centra(dr, "Il tratteggio è un riferimento per valore, senza vincolo di integrità. "
                 "Il pallino rosso segna ciò che manca o che il modello non dichiara.",
             G.fnt(G.F_ITA, 16), 920, 954, G.MUTED)
    im.save(os.path.join(IMG, 'prof_modello.png'))
    return 'prof_modello.png'


if __name__ == '__main__':
    for f in (catena(), modello()):
        print('scritto img/' + f)
