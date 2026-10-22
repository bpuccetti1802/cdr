# -*- coding: utf-8 -*-
"""Figure del documento su identità, profilazione e IAM.

  · iam_flusso.png   — il flusso OIDC target, con l'indicazione di che cosa cambia in SIPO
  · iam_raccordo.png — quali criticità dello stato di fatto l'integrazione chiude davvero

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_iam.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402
import diagrammi_comune as G   # noqa: E402
from diagrammi_comune import (ARROW, F_BLD, F_ITA, F_REG, INK, MUTED,  # noqa: E402
                               centra, fnt)   # noqa: E402

ROSSO, VERDE, GIALLO, BLU = '#b03a48', '#3f8f5f', '#d9a441', '#2f6bb0'


def flusso(dest):
    im, dr = G.tela(1500, 980, "Il flusso di autenticazione target",
                    "In verde ciò che va costruito, in grigio ciò che resta com’è. "
                    "Il contratto verso i 35 front-end non cambia.")

    corsie = [(70, 'Browser', 'grigio'), (430, 'IAM di Roma Capitale', 'viola'),
              (830, 'ProfilazioneUtente', 'verde'), (1180, 'Profili e ANAG_USR', 'blu')]
    for x, nome, col in corsie:
        G.box(dr, x, 96, 250, 56, col, nome)
        dr.line([(x + 125, 152), (x + 125, 806)], fill='#d7dadf', width=2)

    passi = [
        (1, 'apre una pagina protetta', 70, 830, VERDE,
         'nessuna sessione: si genera state, nonce e code_verifier'),
        (2, '302 verso authorize', 830, 430, VERDE,
         'client_id, redirect_uri, scope, state, nonce, code_challenge'),
        (3, 'autenticazione', 70, 430, MUTED,
         'SPID / CIE / CNS per i cittadini, credenziali per i dipendenti'),
        (4, 'callback con il code', 430, 830, VERDE,
         'nuovo endpoint /oidc/callback — si verifica lo state'),
        (5, 'scambio del code in back-channel', 830, 430, VERDE,
         'si valida l’id_token: firma, iss, aud, exp, nonce'),
        (6, 'profili per codice fiscale', 830, 1180, VERDE,
         'il passo «management»: ruoli, aree, funzionalità, organizzazione'),
        (7, 'LOGIN_USER in sessione', 830, 830, GIALLO,
         'l’oggetto User non cambia: i front-end non si riscrivono'),
        (8, 'redirect alla pagina richiesta', 830, 70, MUTED,
         'goUrl convalidato sulle funzionalità abilitate'),
    ]
    y = 196
    for n, testo, da, a, colore, nota in passi:
        xa, xb = da + 125, a + 125
        dr.ellipse([58, y - 10, 82, y + 14], fill=colore)
        centra(dr, str(n), fnt(F_BLD, 14), 70, y - 8, 'white')
        if da == a:
            dr.arc([xa - 40, y - 14, xa + 40, y + 26], 180, 0, fill=colore, width=3)
            dr.text((xa + 50, y - 6), testo, font=fnt(F_BLD, 14), fill=INK)
            dr.text((xa + 50, y + 14), nota, font=fnt(F_ITA, 12), fill=MUTED)
        else:
            G.freccia(dr, (xa, y), (xb, y), colore, 3)
            mx = (xa + xb) / 2
            centra(dr, testo, fnt(F_BLD, 14), mx, y - 26, INK)
            centra(dr, nota, fnt(F_ITA, 12), mx, y + 10, MUTED)
        y += 78

    G.banda(dr, 56, 830, 1444, 918, VERDE, "CHE COSA CAMBIA DAVVERO", VERDE)
    dr.text((80, 862),
            'Cambia soltanto lo strato di ingresso dell’identità: al posto di header di cui '
            'ci si fida, un gettone firmato che si verifica.',
            font=fnt(F_REG, 15), fill=INK)
    dr.text((80, 886),
            'Ruoli, aree tematiche e funzionalità restano in ANAG_USR, e l’oggetto in '
            'sessione resta quello di oggi: i front-end si configurano, non si riscrivono.',
            font=fnt(F_REG, 15), fill=INK)
    im.save(os.path.join(dest, 'iam_flusso.png'))
    return 'iam_flusso.png'


def raccordo(dest):
    im, dr = G.tela(1500, 700, "Che cosa l’integrazione con IAM chiude, e che cosa no",
                    "Un accesso robusto davanti a servizi aperti non migliora la sicurezza "
                    "complessiva: le due cose vanno fatte insieme.")

    colonne = [
        (70, 'CHIUSE DALLA FASE 1', VERDE, [
            'Fiducia negli header non verificati',
            'Percorso alternativo «mode=local»',
            'Sessione senza timeout né attributi',
            'Convalida debole della destinazione']),
        (560, 'CHIUSE DALLA FASE 2', GIALLO, [
            'Identità dell’operatore non propagata',
            'Solo il primo ruolo decide',
            'Quarantaquattro emittenti di gettoni',
            'Operatore e postazione verso ANPR',
            'Utenze tecniche condivise']),
        (1050, 'CHE IAM NON TOCCA', ROSSO, [
            'Servizi accessibili senza gettone',
            'Segreti in chiaro nei sorgenti',
            'Nome della vista scelto dal client',
            'Trasporto non cifrato fra i servizi',
            'Dati personali nel versionamento',
            'Autorizzazione per funzione assente']),
    ]
    for x, titolo, colore, voci in colonne:
        dr.rounded_rectangle([x, 110, x + 380, 150], radius=8, fill=colore)
        centra(dr, titolo, fnt(F_BLD, 16), x + 190, 120, 'white')
        y = 172
        for v in voci:
            dr.rounded_rectangle([x, y, x + 380, y + 52], radius=6,
                                 outline='#c7cdd6', width=2, fill='white')
            for i, riga in enumerate(G.avvolgi(dr, v, fnt(F_REG, 14), 350)):
                dr.text((x + 16, y + 10 + i * 19), riga, font=fnt(F_REG, 14), fill=INK)
            y += 60

    dr.rectangle([70, 592, 1430, 596], fill=ROSSO)
    dr.text((70, 612),
            '⚠ La colonna di destra non dipende da IAM e non si risolve da sé. Il servizio '
            'aperto senza gettone, in particolare, è un intervento piccolo',
            font=fnt(F_BLD, 15), fill=ROSSO)
    dr.text((70, 636),
            'e indipendente — una clausola di chiusura nella configurazione — che conviene '
            'anticipare, perché finché resta aperto il resto conta poco.',
            font=fnt(F_BLD, 15), fill=ROSSO)
    im.save(os.path.join(dest, 'iam_raccordo.png'))
    return 'iam_raccordo.png'


def scala(dest):
    """La scala delle soluzioni: dalla piu' conservativa alla piu' coerente.

    ⚠️ Niente glifo di avvertimento nel disegno: Arial non lo ha. Si usa un pallino
    rosso con il punto esclamativo, come negli altri wireframe.
    """
    im, dr = G.tela(1560, 800, "Le soluzioni possibili",
                    "Da sinistra a destra cresce la coerenza architetturale. L’effort "
                    "cresce con essa, ma non in modo monotono: l’ultima costa meno della "
                    "penultima.")

    gradini = [
        ('S0', 'Consolidamento', 'in modalità header', MUTED,
         'nessuna integrazione OIDC', '5-10 gg', 'RI-01 · RI-06 · RI-19'),
        ('S1', 'OIDC nella libreria', 'condivisa', BLU,
         'opzione A dei documenti', '45-60 gg', '+ RI-04 · RI-17'),
        ('S2', 'Identity Broker', 'di terze parti', GIALLO,
         'opzione B dei documenti', '40-55 gg', '+ RI-04 · RI-17'),
        ('S3', 'Gateway proprio', 'di SIPO', VERDE,
         'opzione C dei documenti', '55-75 gg', '+ RI-02 · RI-16 · RI-18'),
        ('S4', 'Convergenza su ciò', 'che già esiste', VERDE,
         'msAuth, usato dalle app Angular', 'da stimare', '+ RI-02 · RI-16 · RI-18'),
    ]
    larg, base, passo = 280, 646, 46
    for i, (sigla, riga1, riga2, col, fonte, effort, chiude) in enumerate(gradini):
        x = 60 + i * 296
        y = base - (238 + i * passo)
        dr.rounded_rectangle([x, y, x + larg, base], radius=10,
                             fill='#fbfcfd', outline=col, width=3)
        dr.rounded_rectangle([x, y, x + larg, y + 38], radius=10, fill=col)
        dr.rectangle([x + 2, y + 28, x + larg - 2, y + 38], fill=col)
        centra(dr, sigla, fnt(F_BLD, 17), x + larg / 2, y + 8, 'white')
        centra(dr, riga1, fnt(F_BLD, 16), x + larg / 2, y + 56, INK)
        centra(dr, riga2, fnt(F_BLD, 16), x + larg / 2, y + 77, INK)
        centra(dr, fonte, fnt(F_ITA, 13), x + larg / 2, y + 104, MUTED)
        centra(dr, effort, fnt(F_BLD, 16), x + larg / 2, base - 70, col)
        for k, r in enumerate(G.avvolgi(dr, 'chiude ' + chiude, fnt(F_REG, 12), larg - 34)):
            centra(dr, r, fnt(F_REG, 12), x + larg / 2, base - 44 + k * 16, MUTED)

    dr.line([(60, 686), (1500, 686)], fill=MUTED, width=2)
    G.punta(dr, (1500, 686), 0, MUTED, 3, 12)
    dr.text((60, 696), 'più conservativa, meno sviluppo', font=fnt(F_ITA, 14), fill=MUTED)
    t = 'più coerente con l’architettura di destinazione'
    dr.text((1496 - dr.textlength(t, font=fnt(F_ITA, 14)), 696), t,
            font=fnt(F_ITA, 14), fill=MUTED)

    for yy, colore, testo in (
        (740, ROSSO, 'S0 non è un’alternativa alle altre: è il pavimento. Va fatto comunque, '
                     'perché nessuna delle quattro chiude i servizi che oggi rispondono '
                     'senza gettone.'),
        (766, VERDE, 'S4 è l’unica che non crea un secondo impianto di autenticazione '
                     'accanto a quello che le applicazioni Angular già usano.')):
        dr.ellipse([60, yy - 2, 78, yy + 16], fill=colore)
        centra(dr, '!', fnt(F_BLD, 14), 69, yy, 'white')
        dr.text((88, yy), testo, font=fnt(F_BLD, 14), fill=colore)
    im.save(os.path.join(dest, 'iam_scala.png'))
    return 'iam_scala.png'


def sipo_auth(dest):
    """L'architettura scelta: un solo punto di autenticazione, sipo-auth.

    ⚠️ `box()` manda a capo da solo e NON interpreta \n: i sottotitoli su più righe si
    scrivono a mano sotto il riquadro, altrimenti escono su una riga sola o tagliati.
    """
    im, dr = G.tela(1560, 1010, "L’architettura scelta: sipo-auth",
                    "Un solo componente parla con IAM ed emette il token SIPO. "
                    "I trentacinque front-end e la shell Angular non conoscono IAM; "
                    "i back-end verificano una sola firma.")

    G.box(dr, 60, 190, 170, 80, 'grigio', "Browser", "operatore o cittadino")
    G.box(dr, 268, 190, 180, 80, 'grigio', "Portale", "reverse proxy")
    centra(dr, "non inietta più l’identità:", fnt(F_ITA, 14), 358, 276, MUTED)
    centra(dr, "solo x-real-ip e x-client-sn-sipo", fnt(F_ITA, 14), 358, 294, MUTED)

    G.box(dr, 500, 120, 230, 86, 'blu', "35 FE Java", "LOGIN_USER invariato")
    G.box(dr, 500, 258, 230, 86, 'viola', "Shell Angular", "nessun gettone nel browser")

    bordo, fondo = G.C['verde']
    dr.rounded_rectangle([790, 110, 1070, 350], radius=14, fill=fondo, outline=bordo, width=3)
    centra(dr, "sipo-auth", fnt(F_BLD, 24), 930, 128, INK)
    for k, riga in enumerate((
            "unico punto di autenticazione",
            "emette il TOKEN SIPO (RS256)",
            "espone il JWKS ai back-end",
            "fa da BFF per la shell Angular")):
        centra(dr, riga, fnt(F_REG, 16), 930, 170 + k * 26, INK)
    dr.rounded_rectangle([806, 288, 1054, 330], radius=8, fill='white', outline=bordo, width=2)
    centra(dr, "HEADER  |  OIDC  |  MSAUTH", fnt(F_BLD, 16), 930, 301, bordo)

    G.box(dr, 1150, 110, 250, 96, 'viola', "IAM di Roma Capitale",
          "OIDC, un solo client registrato")
    G.box(dr, 1150, 258, 250, 92, 'giallo', "sipo-profili", "profili per codice fiscale")
    centra(dr, "→  ANAG_USR", fnt(F_BLD, 16), 1275, 360, MUTED)

    # ⚠️ il riquadro porta DUE righe di sottotitolo: box() ne centra una sola, quindi il
    # titolo si disegna con box() e le due righe si scrivono sotto, a mano.
    bordo_r, fondo_r = G.C['rosso']
    dr.rounded_rectangle([500, 596, 940, 700], radius=14, fill=fondo_r, outline=bordo_r,
                         width=3)
    centra(dr, "44 back-end", fnt(F_BLD, 21), 720, 612, INK)
    centra(dr, "RestSecurity verifica il token con il JWKS", fnt(F_REG, 16), 720, 646, INK)
    centra(dr, "ROLE_<profiloBe>: le @PreAuthorize non cambiano", fnt(F_REG, 16), 720, 670,
           INK)
    G.box(dr, 1010, 596, 390, 104, 'grigio', "All-Anpr  →  ANPR",
          "operatore e postazione presi dal token")

    for p1, p2, col, et in (
            ((230, 230), (268, 230), ARROW, None),
            ((448, 212), (500, 170), '#2f6bb0', "1"),
            ((448, 250), (500, 294), '#7b5aa6', "1"),
            ((730, 165), (790, 190), '#3f8f5f', "2"),
            ((730, 298), (790, 270), '#3f8f5f', "2"),
            ((1070, 175), (1150, 158), '#7b5aa6', "3"),
            ((1070, 290), (1150, 300), '#d9a441', "4"),
            ((880, 350), (720, 596), '#b03a48', "5"),
            ((940, 648), (1010, 648), ARROW, "6")):
        G.freccia(dr, p1, p2, col, 3)
        if et:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dr.ellipse([mx - 13, my - 28, mx + 13, my - 2], fill=col)
            centra(dr, et, fnt(F_BLD, 14), mx, my - 23, 'white')

    passi = (
        "1  il front-end non ha sessione e manda l’utente a sipo-auth",
        "2  sipo-auth non ha sessione per lui e lo manda a IAM",
        "3  l’utente si autentica su IAM; torna un codice, poi il token IAM",
        "4  sipo-auth chiede i profili per codice fiscale e registra l’accesso",
        "5  il front-end riceve il TOKEN SIPO e lo usa verso i back-end",
        "6  da back-end a back-end lo stesso token viene inoltrato",
    )
    for k, t in enumerate(passi):
        dr.text((70, 410 + k * 26), t, font=fnt(F_REG, 17), fill=INK)

    G.banda(dr, 56, 740, 1500, 840, '#b03a48', "I DUE CONFINI CHE REGGONO IL DISEGNO",
            '#b03a48')
    dr.text((80, 776),
            "Il token di IAM non esce mai da sipo-auth: i back-end vedono soltanto il "
            "token SIPO, firmato da un unico emittente.",
            font=fnt(F_REG, 17), fill=INK)
    dr.text((80, 804),
            "Il browser non riceve mai un gettone: i front-end Java lo tengono in "
            "sessione, la shell Angular non lo vede affatto.",
            font=fnt(F_REG, 17), fill=INK)

    for yy, testo in (
            (880, "Il vocabolario dell’autorizzazione non coincide: i back-end decidono su "
                  "un solo ruolo, la shell Angular su una lista di abilitazioni."),
            (914, "Il token deve portare entrambi, altrimenti il menu del back-office non "
                  "ha su che cosa filtrare.")):
        dr.ellipse([70, yy - 2, 88, yy + 16], fill='#b03a48')
        centra(dr, "!", fnt(F_BLD, 14), 79, yy, 'white')
        dr.text((100, yy), testo, font=fnt(F_BLD, 16), fill='#b03a48')
    im.save(os.path.join(dest, 'iam_sipoauth.png'))
    return 'iam_sipoauth.png'


def mse(dest):
    """L'architettura adottata dalla v0.7: i componenti della piattaforma MSE.

    Sostituisce `sipo_auth()` nella Figura 6: il punto di autenticazione non si costruisce,
    è roma-capitale-auth (L2), e i profili li dà roma-capitale-management (L4). Le sigle
    L2/L3/L4 sono quelle del diagramma di sequenza del documento della piattaforma [F12].
    Verde = esiste; giallo = esiste e va adeguato per SIPO; rosso = lato SIPO, da adeguare.
    """
    im, dr = G.tela(1560, 1060, "L’architettura adottata: la piattaforma MSE",
                    "L’autenticazione e i profili non si costruiscono: si adottano i servizi "
                    "della piattaforma e li si adegua per SIPO.")

    G.box(dr, 50, 200, 160, 80, 'grigio', "Browser", "operatore o cittadino")
    G.box(dr, 250, 200, 170, 80, 'grigio', "Portale", "reverse proxy")

    G.box(dr, 470, 118, 230, 86, 'rosso', "35 FE Java", "token in sessione, LOGIN_USER")
    G.box(dr, 470, 270, 230, 86, 'viola', "Shell Angular", "libreria MSE (rc-fe-mf)")

    def doppio(x, y, w, h, colore, titolo, righe, sigla):
        bordo, fondo = G.C[colore]
        dr.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fondo, outline=bordo,
                             width=3)
        centra(dr, titolo, fnt(F_BLD, 21), x + w / 2, y + 12, INK)
        for k, riga in enumerate(righe):
            centra(dr, riga, fnt(F_REG, 15), x + w / 2, y + 46 + k * 22, INK)
        dr.ellipse([x + w - 46, y - 16, x + w + 4, y + 18], fill=bordo)
        centra(dr, sigla, fnt(F_BLD, 15), x + w - 21, y - 9, 'white')

    doppio(770, 100, 300, 160, 'giallo', "roma-capitale-auth",
           ("unico punto di autenticazione", "OIDC con PKCE, una callback per app",
            "emette il token in un cookie HttpOnly", "da estendere con l’applicazione SIPO"),
           "L2")
    doppio(1160, 100, 340, 120, 'verde', "IAM di Roma Capitale",
           ("autentica: credenziali, SPID, CIE", "un client per applicazione"), "L3")
    doppio(1160, 280, 340, 160, 'giallo', "roma-capitale-management",
           ("utenti, profili, abilitazioni", "applicazioni, nodi, visibilità",
            "schema PostgreSQL «management»", "la gestione è da completare"), "L4")
    G.box(dr, 770, 320, 300, 84, 'verde', "Redis", "token completo, se supera la soglia")
    G.box(dr, 770, 470, 300, 96, 'verde', "roma-capitale-service-mesh",
          "instrada fra i servizi, rinnova il token")

    bordo_r, fondo_r = G.C['rosso']
    dr.rounded_rectangle([420, 640, 900, 740], radius=14, fill=fondo_r, outline=bordo_r,
                         width=3)
    centra(dr, "44 back-end di SIPO", fnt(F_BLD, 21), 660, 654, INK)
    centra(dr, "verificano il token della piattaforma", fnt(F_REG, 16), 660, 688, INK)
    centra(dr, "ROLE_<profiloBe>: le @PreAuthorize non cambiano", fnt(F_REG, 16), 660, 712,
           INK)
    G.box(dr, 1160, 640, 340, 100, 'rosso', "ANAG_USR",
          "R_UTENTI_RUOLI: fonte o proiezione")

    for p1, p2, col, et in (
            ((210, 240), (250, 240), ARROW, None),
            ((420, 222), (470, 172), '#b03a48', "1"),
            ((420, 258), (470, 306), '#7b5aa6', "1"),
            ((700, 160), (770, 170), '#d9a441', "2"),
            ((700, 312), (770, 230), '#d9a441', "2"),
            ((1070, 150), (1160, 150), '#3f8f5f', "3"),
            ((1070, 220), (1160, 330), '#d9a441', "4"),
            ((920, 260), (920, 320), '#3f8f5f', None),
            ((585, 356), (660, 640), '#b03a48', "5"),
            ((900, 690), (920, 566), '#3f8f5f', "6")):
        G.freccia(dr, p1, p2, col, 3)
        if et:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dr.ellipse([mx - 13, my - 28, mx + 13, my - 2], fill=col)
            centra(dr, et, fnt(F_BLD, 14), mx, my - 23, 'white')
    G.linea(dr, [(1330, 440), (1330, 640)], '#b03a48', tratteggio=True)
    centra(dr, "sincronizzazione", fnt(F_ITA, 14), 1420, 520, MUTED)
    centra(dr, "(cap. integrazione)", fnt(F_ITA, 14), 1420, 540, MUTED)

    passi = (
        "1  il front-end non ha sessione e chiama loginIAM con ambito e applicazione",
        "2  roma-capitale-auth reindirizza a IAM con PKCE",
        "3  IAM restituisce un codice, che auth scambia con i token IAM",
        "4  auth chiede a management utente e abilitazioni per codice fiscale",
        "5  il token della piattaforma raggiunge i back-end",
        "6  fra servizio e servizio le chiamate passano dal service mesh",
    )
    for k, t in enumerate(passi):
        dr.text((60, 410 + k * 30), t, font=fnt(F_REG, 16), fill=INK)

    G.banda(dr, 56, 790, 1500, 930, '#b03a48', "CHE COSA VA ADEGUATO PRIMA CHE SIPO ENTRI",
            '#b03a48')
    for k, testo in enumerate((
            "auth: l’applicazione SIPO va aggiunta, e oggi ogni applicazione è scritta "
            "nel codice (callback ed elenco).",
            "management: storia delle assegnazioni, nodo organizzativo, amministrazione "
            "per ambito, revoca che abbia effetto.",
            "piattaforma: chiave di firma solo nell’emittente, percorsi interni chiusi, "
            "un solo servizio che conia i token.")):
        dr.text((80, 826 + k * 30), testo, font=fnt(F_REG, 17), fill=INK)

    G.legenda(dr, 60, 966, (('verde', "esiste ed è adeguato"),
                            ('giallo', "esiste, da adeguare per SIPO"),
                            ('rosso', "lato SIPO, da adeguare")))
    im.save(os.path.join(dest, 'iam_mse.png'))
    return 'iam_mse.png'


def mse_nuovo(dest):
    """L'architettura adottata, dalla v0.11: la piattaforma MSE per il SOLO mondo nuovo.

    Sostituisce `mse()` nella Figura 6. Indirizzo dell'utente (20/10/2026): il vecchio ambiente
    (35 FE Thymeleaf, back-end, ANAG_USR, AnagrafeWeb) resta com'è e la figura lo mostra a parte,
    raggiunto dal portale con le intestazioni di oggi. Niente BFF: è roma-capitale-auth a
    consegnare il token in un cookie HttpOnly («Bearer»), e il service mesh lo legge e lo inoltra
    ai back-end come Authorization: Bearer (AuthenticationFilter.java:125 del service mesh).
    """
    im, dr = G.tela(1560, 1190, "L’architettura adottata: la piattaforma per le applicazioni nuove",
                    "Le applicazioni nuove di SIPO entrano nella piattaforma; il vecchio ambiente "
                    "resta com’è.")
    G.box(dr, 50, 200, 160, 80, 'grigio', "Browser", "operatore")
    G.box(dr, 250, 200, 170, 80, 'grigio', "Portale", "reverse proxy")
    G.box(dr, 470, 196, 230, 90, 'viola', "Shell Angular", "libreria della piattaforma")

    def doppio(x, y, w, h, colore, titolo, righe, sigla):
        bordo, fondo = G.C[colore]
        dr.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fondo, outline=bordo,
                             width=3)
        centra(dr, titolo, fnt(F_BLD, 21), x + w / 2, y + 12, INK)
        for k, riga in enumerate(righe):
            centra(dr, riga, fnt(F_REG, 15), x + w / 2, y + 46 + k * 22, INK)
        dr.ellipse([x + w - 46, y - 16, x + w + 4, y + 18], fill=bordo)
        centra(dr, sigla, fnt(F_BLD, 15), x + w - 21, y - 9, 'white')

    doppio(770, 100, 300, 160, 'giallo', "roma-capitale-auth",
           ("unico punto di autenticazione", "OIDC con PKCE, una callback per app",
            "emette il token in un cookie HttpOnly", "da estendere con le applicazioni SIPO"),
           "L2")
    doppio(1160, 100, 340, 120, 'verde', "IAM di Roma Capitale",
           ("autentica: credenziali, SPID, CIE", "un client per applicazione"), "L3")
    doppio(1160, 280, 340, 160, 'giallo', "roma-capitale-management",
           ("utenti, profili, abilitazioni", "applicazioni, nodi, visibilità",
            "dominio dei profili dedicato", "la gestione è da completare"), "L4")
    G.box(dr, 770, 320, 300, 84, 'verde', "Redis", "token completo, se supera la soglia")
    G.box(dr, 770, 470, 300, 96, 'verde', "roma-capitale-service-mesh",
          "legge il cookie, verifica, inoltra il token")
    G.box(dr, 470, 640, 430, 100, 'viola', "Back-end delle applicazioni nuove",
          "es. back-office ANSC: verificano il token e decidono sulle abilitazioni", ts=20,
          ss=15)

    for p1, p2, col, et in (
            ((210, 240), (250, 240), ARROW, None),
            ((420, 240), (470, 240), '#7b5aa6', "1"),
            ((700, 225), (770, 190), '#d9a441', "2"),
            ((1070, 150), (1160, 150), '#3f8f5f', "3"),
            ((1070, 220), (1160, 330), '#d9a441', "4"),
            ((920, 260), (920, 320), '#3f8f5f', None),
            ((640, 286), (770, 500), '#7b5aa6', "5"),
            ((860, 566), (800, 640), '#3f8f5f', "6")):
        G.freccia(dr, p1, p2, col, 3)
        if et:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dr.ellipse([mx - 13, my - 28, mx + 13, my - 2], fill=col)
            centra(dr, et, fnt(F_BLD, 14), mx, my - 23, 'white')

    passi = (
        "1  la shell non ha sessione e chiama l’accesso con ambito e applicazione",
        "2  roma-capitale-auth reindirizza a IAM con PKCE",
        "3  IAM restituisce un codice, che auth scambia con i token IAM",
        "4  auth chiede a management utente e abilitazioni per codice fiscale",
        "5  il browser chiama i servizi con il cookie; il service mesh lo verifica",
        "6  il mesh inoltra il token ai back-end come Authorization: Bearer",
    )
    for k, t in enumerate(passi):
        dr.text((60, 330 + k * 30), t, font=fnt(F_REG, 15), fill=INK)

    # --- il vecchio ambiente, a parte
    G.banda(dr, 56, 790, 1500, 940, '#6b7280', "VECCHIO AMBIENTE — RESTA COM’È", '#6b7280')
    for k, (tit, sot) in enumerate((("35 front-end Thymeleaf", "LOGIN_USER in sessione"),
                                    ("Back-end di SIPO", "utenze tecniche per profilo"),
                                    ("ANAG_USR", "ruoli, aree, R_UTENTI_RUOLI"),
                                    ("AnagrafeWeb", "gestione degli accessi"))):
        G.box(dr, 90 + k * 350, 836, 310, 80, 'grigio', tit, sot, ts=18, ss=15)
    # aggira l'elenco dei passi a sinistra, per non attraversarlo
    G.linea(dr, [(300, 280), (300, 300), (34, 300), (34, 876), (90, 876)],
            '#6b7280', False, 3)
    dr.text((60, 712), "intestazioni del portale, come oggi", font=fnt(F_ITA, 14), fill=MUTED)
    G.linea(dr, [(1330, 440), (1330, 836)], '#6b7280', tratteggio=True)
    centra(dr, "alimentazione in sola", fnt(F_ITA, 14), 1420, 600, MUTED)
    centra(dr, "lettura, se serve", fnt(F_ITA, 14), 1420, 618, MUTED)
    centra(dr, "(modalità A)", fnt(F_ITA, 14), 1420, 636, MUTED)

    G.banda(dr, 56, 970, 1500, 1110, '#b03a48',
            "CHE COSA VA ADEGUATO PRIMA CHE LE APPLICAZIONI NUOVE ENTRINO", '#b03a48')
    for k, testo in enumerate((
            "auth: le applicazioni SIPO vanno aggiunte, e oggi ogni applicazione è scritta "
            "nel codice (callback ed elenco).",
            "libreria e auth: il token non torna nel corpo delle risposte e non si conserva nel "
            "browser; protezione dalle richieste indotte.",
            "piattaforma: chiave di firma solo nell’emittente, percorsi interni chiusi, revoca "
            "che abbia effetto.")):
        dr.text((80, 1006 + k * 30), testo, font=fnt(F_REG, 17), fill=INK)

    G.legenda(dr, 60, 1146, (('verde', "esiste ed è adeguato"),
                             ('giallo', "esiste, da adeguare"),
                             ('viola', "applicazioni nuove di SIPO"),
                             ('grigio', "vecchio ambiente, invariato")))
    im.save(os.path.join(dest, 'iam_mse_nuovo.png'))
    return 'iam_mse_nuovo.png'


def sequenza_login(dest):
    """Il login di un operatore nelle applicazioni nuove (cap. Scelte, v0.12): diagramma di sequenza.

    Partecipanti e passi sono quelli del sottocapitolo «Il login di un operatore nelle
    applicazioni nuove»; il frammento «alt» è il caso dell'utente non censito o disabilitato.
    Il numero del passo sta a sinistra dell'etichetta, non sulla punta della freccia, così
    non la copre. Le linee di vita si tracciano lunghe e poi si taglia il fondo.
    """
    W, H = 1800, 2000
    im = Image.new('RGB', (W, H), 'white')
    dr = ImageDraw.Draw(im)
    centra(dr, "Il login di un operatore nelle applicazioni nuove", fnt(F_BLD, 27), W / 2, 20,
           '#1b3a5c')
    centra(dr, "Diagramma di sequenza: chi parla con chi, e in quale ordine.", fnt(F_ITA, 16),
           W / 2, 56, MUTED)
    parti = (("Operatore", "browser", 'grigio'), ("Shell Angular", "applicazione nuova", 'viola'),
             ("roma-capitale-auth", "L2", 'giallo'), ("IAM", "L3", 'verde'),
             ("roma-capitale-management", "L4", 'giallo'))
    X = [170, 500, 870, 1230, 1600]
    TOP = 100
    for x, (nome, sotto, col) in zip(X, parti):
        G.box(dr, x - 150, TOP, 300, 74, col, nome, sotto, ts=19, ss=14)
        G.linea(dr, [(x, TOP + 74), (x, H)], '#9ca3af', True, 2)

    y = [TOP + 130]
    n = [0]
    f = fnt(F_REG, 15)

    def etichetta(cx, yy, testo, col):
        """Numero cerchiato + testo, centrati insieme su cx, appena sopra la freccia."""
        n[0] += 1
        lw = G.larghezza(dr, testo, f)
        x0 = cx - (lw + 34) / 2
        dr.rectangle([x0 - 4, yy - 30, x0 + lw + 38, yy - 6], fill='white')
        dr.ellipse([x0, yy - 31, x0 + 26, yy - 5], fill=col)
        centra(dr, str(n[0]), fnt(F_BLD, 14), x0 + 13, yy - 26, 'white')
        dr.text((x0 + 34, yy - 28), testo, font=f, fill=INK)

    def msg(a, b, testo, ritorno=False, col=ARROW, passo=60):
        yy = y[0]
        G.percorso(dr, [(X[a], yy), (X[b], yy)], col, tratteggio=ritorno, larg=3)
        etichetta((X[a] + X[b]) / 2, yy, testo, col)
        y[0] += passo

    def se(a, testo, col=ARROW, passo=72):
        x, yy = X[a], y[0]
        G.percorso(dr, [(x, yy - 12), (x + 56, yy - 12), (x + 56, yy + 16), (x + 6, yy + 16)],
                   col, larg=3)
        lw = G.larghezza(dr, testo, f)
        etichetta(x + 70 + (lw + 34) / 2, yy + 14, testo, col)
        y[0] += passo

    BLU, GIALLO, VIOLA = '#2f6bb0', '#b7862c', '#7b5aa6'
    VERDE, ROSSO = '#3f8f5f', G.C['rosso'][0]
    msg(0, 1, "apre l’applicazione", col=VIOLA)
    se(1, "nessun cookie della piattaforma", col=VIOLA)
    msg(1, 2, "accesso: codice di ambito e di applicazione", col=VIOLA)
    msg(2, 3, "reindirizzamento con PKCE, attraverso il browser", col=GIALLO)
    msg(3, 0, "pagina di accesso di IAM", ritorno=True, col=VERDE)
    msg(0, 3, "credenziali, SPID o CIE: la scelta è di IAM", col=BLU)
    msg(3, 2, "ritorno sulla callback, con il codice", ritorno=True, col=VERDE)
    msg(2, 3, "scambio del codice con il verificatore PKCE", col=GIALLO)
    msg(3, 2, "token di IAM: ne ricava il codice fiscale", ritorno=True, col=VERDE)
    msg(2, 4, "chi è, per questa applicazione? codice fiscale, ambito, applicazione",
        col=GIALLO)
    msg(4, 2, "utente e abilitazioni dell’applicazione", ritorno=True, col=GIALLO, passo=40)

    # --- frammento alternativo: le due guardie, poi il riquadro attorno
    xa1, xa2 = X[0] - 130, X[4] + 160
    ya = y[0]
    y[0] = ya + 80
    msg(2, 1, "accesso negato, con un messaggio esplicito", ritorno=True, col=ROSSO, passo=36)
    yd = y[0]
    y[0] = yd + 76
    msg(2, 0, "cookie «Bearer», HttpOnly, e ritorno alla shell", ritorno=True, col=GIALLO)
    msg(1, 2, "chiede i dati dell’utente, con il cookie", col=VIOLA)
    msg(2, 1, "utente e abilitazioni, senza il token", ritorno=True, col=GIALLO)
    se(1, "costruisce il menu dalle abilitazioni", col=VIOLA, passo=40)
    yf = y[0]
    dr.rectangle([xa1, ya, xa2, yf], outline=ROSSO, width=2)
    dr.rectangle([xa1, ya, xa1 + 70, ya + 28], fill=ROSSO)
    centra(dr, "alt", fnt(F_BLD, 16), xa1 + 35, ya + 5, 'white')
    dr.text((xa1 + 84, ya + 6), "[utente non censito o disabilitato]", font=fnt(F_ITA, 15),
            fill=ROSSO)
    for xx in range(xa1, xa2, 16):
        dr.line([(xx, yd), (min(xx + 8, xa2), yd)], fill=ROSSO, width=2)
    dr.text((xa1 + 84, yd + 8), "[utente censito e attivo]", font=fnt(F_ITA, 15), fill=ROSSO)

    # --- fondo: si cancellano le linee di vita oltre il diagramma e si chiudono i partecipanti
    fondo = yf + 30
    dr.rectangle([0, fondo, W, H], fill='white')
    for x, (nome, _, col) in zip(X, parti):
        G.box(dr, x - 150, fondo, 300, 50, col, nome, ts=16)
    yb = fondo + 80
    G.banda(dr, 56, yb, W - 56, yb + 120, '#6b7280', "DA SAPERE", '#6b7280')
    dr.text((80, yb + 40), "·  Un’altra applicazione nuova trova il cookie sul dominio "
            "dell’ente: i passi da 2 a 13 non si ripetono.", font=fnt(F_REG, 17),
            fill=INK)
    dr.text((80, yb + 72), "·  Il token non deve tornare nel corpo delle risposte (MA-16); la "
            "registrazione dell’accesso, oggi, nella piattaforma non avviene (MA-17).",
            font=fnt(F_REG, 17), fill=INK)
    im = im.crop((0, 0, W, yb + 150))
    im.save(os.path.join(dest, 'iam_sequenza_login.png'))
    return 'iam_sequenza_login.png'


def management(dest):
    """Il modello dati di roma-capitale-management COME È NEL CODICE (entità JPA).

    ⚠️ Non è l'ERD del documento della piattaforma [F12], che ne mostra sette tabelle e
    precede il codice: profilo per applicazione, padre/figlie, nodi e visibilità mancano lì.
    In rosso le due cose che il codice dichiara e non governa: `id_nodo` sull'assegnazione
    non è mai scritto da un'operazione, `utente_per_profilo_get` non ha percorso di scrittura.
    """
    im, dr = G.tela(1900, 1240, "roma-capitale-management: il modello dati nel codice",
                    "Diciassette entità, ricavate dalle classi JPA del servizio. In rosso ciò "
                    "che il modello prevede e nessuna operazione scrive.")
    S = G.scheda
    a = S(dr, 40, 100, 330, 'grigio', "ambito", [("PK", "cd_ambito  CHAR(2)"),
                                                 ("", "ds_ambito")])
    ap = S(dr, 40, 215, 330, 'grigio', "applicazione", [
        ("PK", "cd_ambito, cd_applicazione (10)"), ("", "ds_endpoint, ds_context_root"),
        ("", "cd_cloud  1 | 2"), ("", "ty_auth  G (gruppo) | P (singola)"),
        ("FK", "applicazione padre"), ("", "fg_lista_strutture, fg_anonymous"),
        ("", "id_applicazione_sa  (PMAN)")])
    cf = S(dr, 40, 455, 330, 'grigio', "configurazione", [
        ("PK", "ambito, applicazione, parametro"), ("", "valore (testo)")],
        nota="configurazione remota dei servizi")
    av = S(dr, 40, 590, 330, 'grigio', "avviso", [
        ("PK", "id_avviso"), ("", "ambito, applicazione"), ("", "titolo, testo, inizio, fine")])

    ab = S(dr, 430, 100, 360, 'blu', "abilitazione", [
        ("PK", "id_abilitazione"), ("UK", "ambito, applicazione, cd_abilitazione"),
        ("", "ds_abilitazione  (10 caratteri)"), ("", "cd_esterno  (PMAN)"),
        ("FK", "id_menu")])
    mn = S(dr, 430, 290, 360, 'blu', "menu", [("PK", "id_menu"), ("", "cd_menu, ds_menu")])
    ppa = S(dr, 430, 420, 360, 'verde', "profilo_per_abilitazione", [
        ("PK", "id_profilo + id_abilitazione")])
    pr = S(dr, 430, 530, 360, 'verde', "profilo", [
        ("PK", "id_profilo"), ("", "ds_profilo"), ("", "cd_ruolo_profilo"),
        ("", "fg_profilo_default"), ("", "cd_ambito, cd_applicazione")])

    upp = S(dr, 850, 420, 360, 'viola', "utente_per_profilo", [
        ("PK", "id_utente + id_profilo"), ("FK", "id_nodo")],
        nota="id_nodo: nessuna operazione lo scrive")
    ut = S(dr, 850, 100, 360, 'viola', "utente", [
        ("PK", "id_utente"), ("", "ds_username  (unico)"),
        ("", "cd_fiscale  (unico all’inserimento)"), ("", "ds_password  (AES, reversibile)"),
        ("", "fg_attivo_sn, dt_ultimo_login"), ("", "tentativi, scadenze, ty_utente"),
        ("FK", "id_ente")])
    en = S(dr, 850, 600, 360, 'viola', "ente", [("PK", "id_ente"), ("", "cd_ente, ds_ente")])

    ns = S(dr, 1270, 100, 300, 'giallo', "nodo_struttura", [
        ("PK", "id_nodo"), ("FK", "id_struttura"), ("FK", "id_nodo_padre  (albero)"),
        ("", "cd_nodo, nm_nodo")])
    st = S(dr, 1270, 290, 300, 'giallo', "struttura", [("PK", "id_struttura"),
                                                       ("", "nm, ds")])
    npv = S(dr, 1270, 400, 300, 'giallo', "nodo_per_visibilita", [
        ("PK", "id_nodo + id_visibilita")])
    vi = S(dr, 1270, 510, 300, 'giallo', "visibilita", [
        ("PK", "id_visibilita"), ("", "nm_tabella, nm_colonna"), ("", "ds_valore"),
        ("FK", "dipendenza")], nota="filtro dei dati: tabella, colonna, valore")

    upg = S(dr, 1610, 100, 270, 'rosso', "utente_per_profilo_get", [
        ("PK", "utente + profilo"), ("", "+ codice_struttura_ged")],
        nota="solo GET-BO, nessuna scrittura")
    vso = S(dr, 1610, 260, 270, 'rosso', "v_str_organizzativa", [
        ("", "vista dell’organigramma"), ("", "codice, padre, responsabile")])

    def lega(b1, lato1, b2, lato2, colore=ARROW, tratt=False):
        def punto(b, lato):
            x1, y1, x2, y2 = b
            return {'s': (x1, (y1 + y2) / 2), 'd': (x2, (y1 + y2) / 2),
                    'a': ((x1 + x2) / 2, y1), 'b': ((x1 + x2) / 2, y2)}[lato]
        p1, p2 = punto(b1, lato1), punto(b2, lato2)
        if p1[0] == p2[0] or p1[1] == p2[1]:
            G.linea(dr, [p1, p2], colore, tratt, 2)
        else:
            mx = (p1[0] + p2[0]) / 2
            G.linea(dr, [p1, (mx, p1[1]), (mx, p2[1]), p2], colore, tratt, 2)

    lega(a, 'b', ap, 'a')
    lega(ap, 'b', cf, 'a')
    lega(ap, 'd', ab, 's')
    lega(ab, 'b', mn, 'a')
    lega(ppa, 'a', mn, 'b', ARROW, True)
    lega(ppa, 'b', pr, 'a')
    # ⚠️ i collegamenti che attraverserebbero una scheda si tracciano a mano
    G.linea(dr, [(ab[2], 200), (812, 200), (812, 450), (ppa[2], 450)], '#2f6bb0', True, 2)
    G.linea(dr, [(upp[0], 500), (820, 500), (820, 610), (pr[2], 610)], ARROW, False, 2)
    lega(ut, 'b', upp, 'a')
    lega(upp, 'b', en, 'a', ARROW, True)
    G.linea(dr, [(upp[2], 480), (1240, 480), (1240, 200), (ns[0], 200)], '#b03a48', True, 2)
    lega(ns, 'b', st, 'a')
    lega(st, 'b', npv, 'a', ARROW, True)
    lega(npv, 'b', vi, 'a')
    lega(upg, 'b', vso, 'a', '#b03a48', True)
    G.linea(dr, [(1100, ut[1]), (1100, 88), (1745, 88), (1745, upg[1])], '#b03a48', True, 2)

    dr.text((40, 760), "Come si legge", font=fnt(F_BLD, 18), fill=INK)
    for k, t in enumerate((
            "Il profilo appartiene a un’applicazione e porta un codice di ruolo: un utente "
            "riceve profili, i profili raggruppano abilitazioni.",
            "Con ty_auth = G il login su un’applicazione padre unisce le abilitazioni dei "
            "profili delle applicazioni figlie.",
            "L’assegnazione può nominare un nodo di un albero organizzativo, e il nodo porta "
            "regole di visibilità sui dati (tabella, colonna, valore).",
            "Le abilitazioni arrivano nel token come codici, senza l’applicazione: con ty_auth "
            "= G due figlie con lo stesso codice non si distinguono.",
            "Avvisi, configurazione e menu fanno del servizio anche il registro della "
            "piattaforma: il service mesh lo interroga a ogni instradamento.")):
        dr.text((40, 796 + k * 30), "·  " + t, font=fnt(F_REG, 17), fill=INK)
    G.legenda(dr, 40, 970, (('grigio', "registro della piattaforma"),
                            ('blu', "catalogo delle abilitazioni"), ('verde', "profili"),
                            ('viola', "utenti e assegnazioni"),
                            ('giallo', "organizzazione e visibilità"),
                            ('rosso', "specifico di un’applicazione (GET)")))
    im = im.crop((0, 0, 1900, 1010))
    im.save(os.path.join(dest, 'iam_management.png'))
    return 'iam_management.png'


def dominio(dest):
    """Il dominio dei profili: le tabelle di roma-capitale-management in un dominio a parte.

    Raccomandazione della v0.10 (20/10/2026): chi scrive queste tabelle decide chi entra in
    tutte le applicazioni della piattaforma, quindi vivono in un dominio proprio (PDB dedicato,
    o almeno schema dedicato), raggiunto da una sola utenza applicativa, con il proprietario
    senza accesso e nessun collegamento diretto con gli schemi di SIPO. Dalla v0.13 le tabelle
    sono quelle dello schema in esercizio (management-schema.sql): 19, più le 5 di copia escluse.
    """
    im, dr = G.tela(1900, 1130, "Il dominio dei profili: chi vi accede e come",
                    "Le tabelle di roma-capitale-management in un dominio a parte, raggiunto "
                    "da una sola utenza applicativa.")
    S = G.scheda
    # --- il dominio
    G.banda(dr, 520, 100, 1380, 760, '#2f6bb0',
            "Dominio dei profili  (PDB dedicato, o almeno schema dedicato)", '#2f6bb0')
    dr.text((540, 132), "tablespace cifrato  ·  vincoli di integrità nel database  ·  "
            "tracciamento delle modifiche", font=fnt(F_ITA, 15), fill=MUTED)
    S(dr, 545, 170, 260, 'viola', "Utenti", [("", "utente"), ("", "ente"),
                                             ("", "utente_per_profilo"),
                                             ("", "utente_profilo_per_applicazione")])
    S(dr, 830, 170, 260, 'verde', "Profili", [("", "profilo"),
                                              ("", "profilo_per_abilitazione")])
    S(dr, 1110, 170, 250, 'blu', "Catalogo", [("", "ambito"), ("", "applicazione"),
                                              ("", "abilitazione"), ("", "menu"),
                                              ("", "applicazione_padre")])
    S(dr, 545, 330, 260, 'giallo', "Organizzazione", [("", "struttura"), ("", "nodo_struttura"),
                                                      ("", "visibilita"),
                                                      ("", "nodo_per_visibilita")])
    S(dr, 830, 330, 260, 'grigio', "Registro della piattaforma",
      [("", "configurazione"), ("", "avviso")])
    S(dr, 1110, 330, 250, 'rosso', "Di una sola applicazione",
      [("", "utente_per_profilo_get"), ("", "v_str_organizzativa")])
    # proprietario e ruoli dentro il dominio
    G.box(dr, 545, 520, 260, 110, 'grigio', "Proprietario dello schema",
          "senza accesso: solo i rilasci", ts=18, ss=15)
    G.box(dr, 830, 520, 260, 110, 'blu', "Ruolo applicativo",
          "lettura e scrittura sulle sole tabelle", ts=18, ss=15)
    G.box(dr, 1110, 520, 250, 110, 'verde', "Ruolo di sola lettura",
          "revisione degli accessi", ts=18, ss=15)
    dr.text((545, 660), "Nessun privilegio di sistema all’utenza applicativa; sinonimi "
            "privati, così il codice del servizio non cambia.", font=fnt(F_REG, 15), fill=INK)
    dr.text((545, 690), "Credenziali di connessione fuori dalla configurazione versionata; "
            "connessione cifrata.", font=fnt(F_REG, 15), fill=INK)
    dr.text((545, 720), "Le cinque tabelle di copia dello schema in esercizio non entrano nel "
            "dominio.", font=fnt(F_REG, 15), fill=INK)

    # --- a sinistra: i servizi
    G.box(dr, 40, 150, 380, 120, 'blu', "roma-capitale-management",
          "unico servizio che si collega al dominio", ts=19, ss=15)
    G.box(dr, 40, 340, 380, 100, 'grigio', "roma-capitale-auth", "legge per API, non per base dati",
          ts=19, ss=15)
    G.box(dr, 40, 480, 380, 100, 'grigio', "service mesh", "legge per API, non per base dati",
          ts=19, ss=15)
    G.freccia(dr, (420, 210), (520, 210), '#2f6bb0', 3)
    dr.text((428, 222), "utenza", font=fnt(F_REG, 14), fill=MUTED)
    dr.text((428, 240), "applicativa", font=fnt(F_REG, 14), fill=MUTED)
    G.freccia(dr, (230, 340), (230, 270), ARROW, 3)
    G.linea(dr, [(30, 530), (20, 530), (20, 300), (230, 300)], ARROW, False, 3)
    dr.text((240, 296), "API interne", font=fnt(F_REG, 14), fill=MUTED)
    G.box(dr, 40, 630, 380, 110, 'grigio', "Regola di rete",
          "il servizio di base dati accetta solo i pod di management e l’accesso "
          "amministrativo", ts=18, ss=15)

    # --- a destra: tracciamento e amministrazione
    G.box(dr, 1440, 150, 420, 120, 'verde', "Tracciamento",
          "modifiche a utenti, profili e assegnazioni, conservato fuori dal dominio",
          ts=19, ss=15)
    G.freccia(dr, (1380, 210), (1440, 210), '#3f8f5f', 3)
    G.box(dr, 1440, 330, 420, 120, 'giallo', "Amministratori della base dati",
          "accesso privilegiato tracciato; separazione dei compiti", ts=19, ss=15)
    G.freccia(dr, (1440, 390), (1380, 390), '#d9a441', 3, )
    G.box(dr, 1440, 510, 420, 120, 'grigio', "Ambienti di prova",
          "dati sintetici o mascherati, mai una copia della produzione", ts=19, ss=15)

    # --- in basso: SIPO, separato
    G.banda(dr, 520, 830, 1380, 960, '#b03a48', "Schemi di SIPO", '#b03a48')
    for k, nome in enumerate(("MATR_USR", "ANAG_USR", "ANSC_USR")):
        G.box(dr, 560 + k * 270, 875, 240, 60, 'rosso', nome, ts=18)
    G.linea(dr, [(950, 760), (950, 830)], '#b03a48', True, 3)
    dr.text((970, 780), "nessun collegamento diretto: niente database link, sinonimi o "
            "chiavi esterne", font=fnt(F_REG, 15), fill='#b03a48')
    dr.text((970, 800), "fra i due mondi; se servono dati, passano dalle API",
            font=fnt(F_REG, 15), fill='#b03a48')

    G.legenda(dr, 40, 1000, (('viola', "utenti e assegnazioni"), ('verde', "profili"),
                             ('blu', "catalogo"), ('giallo', "organizzazione"),
                             ('grigio', "registro della piattaforma"),
                             ('rosso', "specifico di un’applicazione · schemi di SIPO")))
    im = im.crop((0, 0, 1900, 1040))
    im.save(os.path.join(dest, 'iam_dominio.png'))
    return 'iam_dominio.png'


if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    os.makedirs(dest, exist_ok=True)
    for f in (flusso, raccordo, scala, sipo_auth, mse, mse_nuovo, sequenza_login, management, dominio):
        print('  scritto', f(dest))
