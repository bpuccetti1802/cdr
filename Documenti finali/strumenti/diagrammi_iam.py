# -*- coding: utf-8 -*-
"""Figure del documento su identità, profilazione e IAM.

  · iam_flusso.png   — il flusso OIDC target, con l'indicazione di che cosa cambia in SIPO
  · iam_raccordo.png — quali criticità dello stato di fatto l'integrazione chiude davvero

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_iam.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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


if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    os.makedirs(dest, exist_ok=True)
    for f in (flusso, raccordo, scala, sipo_auth):
        print('  scritto', f(dest))
