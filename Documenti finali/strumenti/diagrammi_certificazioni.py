# -*- coding: utf-8 -*-
"""Figure dell'analisi sulle certificazioni di stato civile SIPO-ANSC (v0.1, 10/11/2026).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_certificazioni.py

`img/certificazioni/instradamento.png`: dalla richiesta allo sportello al documento, con la
scelta fra il formulario di SIPO e i servizi ANSC secondo l'atto.
Le stringhe visualizzate usano il doppio apice (vedi diagrammi_comune).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import (C, INK, MUTED, ARROW, F_BLD, F_REG, F_ITA, fnt, box,  # noqa
                              pila, rombo, percorso, freccia, banda, legenda, tela, centra,
                              linea)

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'certificazioni')


def instradamento(out=os.path.join(IMG, 'instradamento.png')):
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1180
    im, dr = tela(W, H, "Da dove esce il documento: l’instradamento per atto",
                  "La richiesta nasce sempre allo sportello di stato civile in SIPO; "
                  "la fonte del documento dipende dall’atto")

    # 1 richiesta
    box(dr, 700, 100, 500, 100, 'grigio', "Lo sportello di stato civile in SIPO",
        "l’operatore sceglie l’atto e il documento", ts=20, ss=15)
    # 2 controlli comuni
    box(dr, 700, 240, 500, 100, 'grigio', "Controlli preliminari in SIPO",
        "blocco della certificazione per il soggetto · stato dell’atto", ts=20, ss=15)
    freccia(dr, (950, 200), (950, 235))
    # 3 decisione
    rombo(dr, 950, 450, 470, 170, "L’atto ha un identificativo ANSC?", ts=20)
    freccia(dr, (950, 340), (950, 362))

    # ramo NO: SIPO
    percorso(dr, [(715, 450), (360, 450), (360, 540)])
    centra(dr, "no — atto del registro tradizionale", fnt(F_BLD, 15), 520, 420, INK)
    pila(dr, 130, 545, 460, 180, 'grigio',
         ["Formulario di SIPO"],
         ["PKG_ESTRATTI, modelli Jasper", "estratti ESN · ESM · ESU · ESD",
          "plurilingue 884 · 851 · 872/874", "copia conforme dell’atto"],
         ["come oggi"])
    box(dr, 130, 770, 460, 110, 'grigio', "PDF da stampare e firmare a mano",
        "nessun sigillo, nessun QR", ts=19, ss=15)
    freccia(dr, (360, 725), (360, 765))

    # ramo SI: ANSC
    percorso(dr, [(1185, 450), (1500, 450), (1500, 500)])
    centra(dr, "sì — l’originale è in ANSC", fnt(F_BLD, 15), 1340, 420, INK)
    rombo(dr, 1500, 580, 420, 150, "Quale documento?", ts=19)

    xs = [1090, 1500, 1800]
    # tre esiti
    percorso(dr, [(1290, 580), (1090, 580), (1090, 680)])
    percorso(dr, [(1500, 655), (1500, 680)])

    percorso(dr, [(1710, 580), (1800, 580), (1800, 680)])
    pila(dr, 950, 685, 280, 200, 'blu',
         ["Certificato semplice"],
         ["R002 /certificato-semplice", "sigillo del Ministero", "QR di verifica, 6 mesi",
          "nessuna firma dell’USC"],
         ["anche profilo SCCSE"])
    pila(dr, 1250, 685, 390, 200, 'rosso',
         ["Estratto per riassunto", "o per copia integrale"],
         ["R002 /certificato, tipo 2 o 3", "firma remota dell’USC:",
          "utente, password e OTP di firma"],
         ["solo l’ufficiale"])
    pila(dr, 1665, 685, 215, 200, 'viola',
         ["Plurilingue"],
         ["R019", "sigle → annotazioni", "→ anteprima", "→ emissione"],
         ["Vienna"])

    # concentratore
    pila(dr, 950, 930, 930, 110, 'giallo',
         ["Concentratore all-ansc-sipo"],
         ["sessione OTP e token verso ANSC · restituisce il PDF/A in base64 con "
          "l’identificativo del certificato e la data di validità"])
    for x in (1090, 1445, 1772):
        freccia(dr, (x, 885), (x, 925))

    # registro comune
    box(dr, 130, 930, 760, 110, 'verde', "Registro delle emissioni in SIPO",
        "ESTRATTI_DOWNLOAD_LOG come oggi · ANSC_CERTIFICATO per le emissioni ANSC",
        ts=19, ss=15)
    percorso(dr, [(360, 880), (360, 925)])
    percorso(dr, [(950, 985), (895, 985)])

    legenda(dr, 130, 1080, [('grigio', "SIPO, come oggi"), ('blu', "senza firma dell’USC"),
                            ('rosso', "con firma remota dell’USC"),
                            ('viola', "plurilingue"), ('giallo', "concentratore"),
                            ('verde', "registro")])
    centra(dr, "Bollo, diritti ed esenzioni restano fuori da ANSC, come nel percorso di "
               "stato civile di oggi.", fnt(F_ITA, 15), W / 2, 1130, MUTED)
    im.save(out)
    return out


def sequenza_r002(out=os.path.join(IMG, 'sequenza_r002.png')):
    """Emissione di un certificato ANSC dallo sportello certificati (v0.3)."""
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1530
    im, dr = tela(W, H, "Come si ottiene il certificato da ANSC: la sequenza delle chiamate",
                  "Una consultazione prima, una sola emissione alla fine: ogni chiamata a R002 "
                  "produce un certificato nuovo")
    attori = [(230, 'grigio', "Sportello certificati", "CertificatiWeb"),
              (700, 'grigio', "cert-be", "pratica e certificati"),
              (1170, 'giallo', "all-ansc-sipo", "concentratore"),
              (1640, 'blu', "ANSC", "servizi cooperativi")]
    for x, col, t, s in attori:
        box(dr, x - 190, 100, 380, 80, col, t, s, ts=20, ss=15)
        linea(dr, [(x, 180), (x, 1450)], MUTED, tratteggio=True, larg=2)
    X = {a[2]: a[0] for a in attori}

    def msg(y, da, a, testo, sotto=None, colore=ARROW, tratt=False):
        x1, x2 = X[da], X[a]
        x1 += 8 if x2 > x1 else -8
        x2 += -10 if x2 > x1 else 10
        percorso(dr, [(x1, y), (x2, y)], colore, tratteggio=tratt, larg=3)
        cx = (x1 + x2) / 2
        centra(dr, testo, fnt(F_BLD, 16), cx, y - 26, INK)
        if sotto:
            centra(dr, sotto, fnt(F_REG, 14), cx, y + 8, MUTED)

    def fase(y, testo):
        dr.rectangle([40, y - 18, W - 40, y + 14], fill='#f3f4f6')
        dr.text((52, y - 14), testo, font=fnt(F_BLD, 17), fill='#1b3a5c')

    def nota(x, y, w, h, testo, col='verde'):
        box(dr, x, y, w, h, col, testo, None, ts=15)

    fase(225, "1 · AGGIUNGI: la riga del certificato riconosce l’atto ANSC e lo consulta")
    msg(290, "Sportello certificati", "cert-be", "aggiungi certificato",
        "intestatario e tipo scelti")
    nota(520, 330, 360, 60, "ANAG_USR.ATTO.ID_ATTO_ANSC valorizzato?")
    msg(440, "cert-be", "all-ansc-sipo", "leggi l’atto per idAnsc")
    msg(510, "all-ansc-sipo", "ANSC", "R005 /consultazione/ansc/evento/sintetico/1",
        "criteriRicercaEvento.idAnsc")
    msg(590, "ANSC", "all-ansc-sipo", "ModelEventoRidotto", "id, stato, intestatari, flag "
        "dei tipi emissibili", tratt=True)
    msg(660, "all-ansc-sipo", "cert-be", "dati per i controlli", None, tratt=True)
    nota(520, 690, 360, 70, "stato dell’atto · tipo emissibile · intestatario")
    msg(800, "cert-be", "Sportello certificati", "riepilogo dell’atto",
        "al posto dell’anteprima: nessun PDF", tratt=True)

    fase(860, "2 · EMETTI: una sola chiamata a R002, con le credenziali di firma per gli "
              "estratti")
    msg(925, "Sportello certificati", "cert-be", "emetti",
        "riassunto e copia integrale: utente, password, OTP")
    msg(1005, "cert-be", "all-ansc-sipo", "creaCertificato")
    msg(1075, "all-ansc-sipo", "ANSC", "R002 /certificato-semplice/1 · /certificato/1",
        "idAnsc, idEvento, intestatario.id, idTipoCertificato…")
    msg(1155, "ANSC", "all-ansc-sipo", "contenuto (PDF/A in base64)",
        "nomeFile, idCertificato, datavalidita", tratt=True)
    nota(990, 1185, 360, 60, "ANSC_CERTIFICATO e audit, senza il PDF", 'giallo')
    msg(1290, "all-ansc-sipo", "cert-be", "PDF decodificato e idCertificato", None, tratt=True)
    nota(520, 1310, 360, 60, "CERTIFICATI.DOCUMENTO_CERTIFICATO")
    msg(1420, "cert-be", "Sportello certificati", "PDF in download (application/pdf)",
        None, tratt=True)
    legenda(dr, 60, 1480, [('grigio', "SIPO"), ('giallo', "concentratore"), ('blu', "ANSC"),
                           ('verde', "controllo o scrittura")])
    im.save(out)
    return out


def ricerca_atto(out=os.path.join(IMG, 'ricerca_atto_intestatario.png')):
    """Dall'intestatario all'atto nell'ufficio certificati, area «Stato Civile» (cert-be)."""
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1580
    im, dr = tela(W, H, "Ufficio certificati, area «Stato Civile»: dall’intestatario all’atto",
                  "cert-be, schema ANAG_USR · il certificato è legato alla persona: l’atto si "
                  "ricava dalle sue relazioni, non si sceglie")
    # 1 intestatario
    box(dr, 610, 95, 680, 100, 'grigio', "Intestatario scelto nella pagina (CERCA)",
        "ANAG_USR.SOGGETTO.ID_SOGGETTO → CERTIFICATI.ID_SOGGETTO_INT", ts=19, ss=15)
    freccia(dr, (950, 195), (950, 228))
    # 2 rombo ANPR
    rombo(dr, 950, 300, 600, 140, "Il certificato ha un tipo ANPR? (R_CONF_CERT_ANPR)", ts=18)
    centra(dr, "sì: 5 nascita · 6 matrimonio · 25 morte · 3 cittadinanza", fnt(F_ITA, 15),
           1450, 250, MUTED)

    # ramo sì: 3002
    percorso(dr, [(1250, 300), (1560, 300), (1560, 400)])
    centra(dr, "sì", fnt(F_BLD, 16), 1400, 274, INK)
    box(dr, 1330, 405, 470, 110, 'blu', "ANPR 3002: ricerca della persona",
        "con CF e dati anagrafici; il codice individuale non si invia "
        "(PraticaCertificatiController:1196)", ts=17, ss=14)
    rombo(dr, 1565, 610, 440, 120, "Trovata in ANPR?", ts=18)
    freccia(dr, (1565, 515), (1565, 548))
    box(dr, 1330, 720, 470, 120, 'blu', "ANPR 6001 emette il certificato",
        "SIPO non cerca l’atto: il contenuto lo compone ANPR dalla scheda della persona",
        ts=17, ss=14)
    freccia(dr, (1565, 670), (1565, 715))
    centra(dr, "sì", fnt(F_BLD, 16), 1590, 680, INK)

    # ramo no ANPR → verifica atto locale
    percorso(dr, [(1345, 610), (1150, 610), (1150, 650)])
    centra(dr, "no (per la morte anche: cancellata senza decesso)", fnt(F_BLD, 14), 1180, 582, INK)
    box(dr, 820, 655, 470, 175, 'giallo', "Verifica all’aggiunta: AttoRepository",
        "5 findAttoNascitaResRomaBySoggetto (NASCITA.ID_COMUNE = 6333) · "
        "25 findAttoMorteBySoggetto · 6 findAttoMatrimonioBySoggetto · "
        "44 findAttoUnioneCivileBySoggetto — sempre con NUMERO_ATTO, ANNO e PARTE "
        "valorizzati", ts=17, ss=14)
    percorso(dr, [(1290, 790), (1310, 790), (1310, 925), (1325, 925)])
    box(dr, 1330, 890, 470, 70, 'rosso', "Nessun atto: «Impossibile rilasciare il "
        "certificato»", None, ts=15)
    centra(dr, "nessun atto", fnt(F_BLD, 14), 1380, 865, INK)
    percorso(dr, [(1055, 830), (1055, 1010)])
    dr.text((1068, 900), "atto trovato: anpr = 0 nella pratica", font=fnt(F_BLD, 14), fill=INK)
    dr.text((1068, 920), "→ ramo locale all’emissione", font=fnt(F_ITA, 14), fill=MUTED)

    # ramo no tipo ANPR
    percorso(dr, [(650, 300), (330, 300), (330, 1010)])
    centra(dr, "no: 18 nascita non residenti · 44 unione civile · 63 matrimonio …",
           fnt(F_ITA, 15), 470, 274, MUTED)

    # ramo locale: quattro catene
    dr.rectangle([40, 1015, W - 40, 1045], fill='#f3f4f6')
    dr.text((52, 1019), "Ramo locale (anteprima ed emissione): l’atto si raggiunge dalle "
            "relazioni della persona in ANAG_USR", font=fnt(F_BLD, 17), fill='#1b3a5c')
    catene = [
        ('verde', "Nascita (5, 18)", "SOGGETTO.ID_NASCITA → NASCITA.ID_ATTO → ATTO"),
        ('verde', "Morte (25)", "SOGGETTO.ID_MORTE → MORTE.ID_ATTO → ATTO"),
        ('viola', "Matrimonio (6, 63)", "MATRIMONIO con ID_SOGGETTO_MARITO o _MOGLIE = "
         "persona, FLAG_ANPR ≠ 'N', il più recente per DATA_EVENTO → ID_ATTO → ATTO"),
        ('viola', "Unione civile (44)", "UNIONECIVILE con ID_SOGGETTO_PRIMO o _SECONDO = "
         "persona, la più recente per DATA_EVENTO → ID_ATTO → ATTO"),
    ]
    for i, (col, t, s) in enumerate(catene):
        x = 60 + i * 455
        box(dr, x, 1070, 430, 190, col, t, s, ts=18, ss=15)
        percorso(dr, [(x + 215, 1260), (x + 215, 1300)])
    box(dr, 60, 1305, 1795, 130, 'grigio', "Modello «Certificato_semplice» "
        "(DocCertificatoSempliceComuneRoma)",
        "stampa sempre l’atto di NASCITA della persona e, per matrimonio, unione e morte, "
        "l’atto dell’evento: NUMERO_ATTO, PARTE, SERIE, ANNO, comune di trascrizione · "
        "se NUMERO_ATTO è vuoto stampa ATTO.ID_ATTO_ANSC", ts=18, ss=15)
    legenda(dr, 60, 1470, [('grigio', "SIPO"), ('blu', "ANPR"),
                           ('giallo', "verifica all’aggiunta"), ('verde', "evento 1:1"),
                           ('viola', "evento con due soggetti"), ('rosso', "rifiuto")])
    centra(dr, "La verifica all’aggiunta e l’emissione leggono l’atto per strade diverse: la "
               "prima pone condizioni (comune, numero, anno, parte) che la seconda non ripete.",
           fnt(F_ITA, 15), W / 2, 1530, MUTED)
    im.save(out)
    return out


def innesto_ansc(out=os.path.join(IMG, 'innesto_ricerca_ansc.png')):
    """La ricerca ANSC innestata nel flusso dell'ufficio certificati (v0.5)."""
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1820
    im, dr = tela(W, H, "Come si innesta la ricerca ANSC nell’ufficio certificati",
                  "In cert-be, all’aggiunta del certificato: per gli atti presenti in ANSC il "
                  "ramo nuovo sostituisce la verifica in ANPR e la ricerca locale")
    # 0 intestatario
    box(dr, 660, 95, 580, 80, 'grigio', "Intestatario e voce scelti (come oggi)",
        "ANAG_USR.SOGGETTO · CONF_CERTIFICATO", ts=18, ss=15)
    freccia(dr, (950, 175), (950, 200))
    # 1 voce d'atto?
    rombo(dr, 950, 265, 640, 120, "Passo 1 · Voce d’atto prevista per R002?", ts=18)
    percorso(dr, [(630, 265), (230, 265), (230, 1610)])
    centra(dr, "no", fnt(F_BLD, 16), 430, 238, INK)
    # 2 atto della persona
    freccia(dr, (950, 325), (950, 360))
    centra(dr, "sì", fnt(F_BLD, 16), 975, 330, INK)
    box(dr, 640, 365, 620, 95, 'verde', "Passo 2 · L’atto della persona in ANAG_USR",
        "stesse catene dell’emissione (una sola regola, CE-20) → ATTO.ID_ATTO_ANSC",
        ts=18, ss=15)
    freccia(dr, (950, 460), (950, 488))
    rombo(dr, 950, 545, 520, 110, "ID_ATTO_ANSC valorizzato?", ts=18)
    # 3a per identificativo
    percorso(dr, [(1210, 545), (1560, 545), (1560, 600)])
    centra(dr, "sì", fnt(F_BLD, 16), 1380, 518, INK)
    box(dr, 1320, 605, 480, 140, 'blu', "Passo 3a · Ricerca per identificativo",
        "R005 /consultazione/ansc/evento/sintetico/1 · criteriRicercaEvento.idAnsc → un "
        "ModelEventoRidotto", ts=17, ss=14)
    # 3b per persona
    percorso(dr, [(690, 545), (560, 545), (560, 600)])
    centra(dr, "no", fnt(F_BLD, 16), 625, 518, INK)
    rombo(dr, 560, 660, 460, 110, "Ricerca per persona attiva?", ts=17)
    percorso(dr, [(330, 660), (240, 660)])
    centra(dr, "no", fnt(F_BLD, 15), 290, 634, INK)
    freccia(dr, (560, 715), (560, 750))
    centra(dr, "sì (CE-24)", fnt(F_BLD, 15), 610, 722, INK)
    box(dr, 330, 755, 460, 150, 'blu', "Passo 3b · Ricerca per persona",
        "R005 /consultazione/ansc/soggetto/sintetico/1 · idAnprUnico o idAnpr, altrimenti "
        "codice fiscale e dati → elenco di ModelEventoRidotto", ts=17, ss=14)
    rombo(dr, 560, 990, 440, 110, "Eventi pertinenti?", ts=17)
    freccia(dr, (560, 905), (560, 935))
    percorso(dr, [(340, 990), (240, 990)])
    centra(dr, "nessuno", fnt(F_BLD, 15), 290, 962, INK)
    box(dr, 330, 1080, 460, 80, 'grigio', "Uno: si usa · più di uno: sceglie l’operatore",
        None, ts=16)
    freccia(dr, (560, 1045), (560, 1075))
    # 4 controlli
    linea(dr, [(790, 1120), (950, 1120)])
    percorso(dr, [(950, 1120), (950, 1185)])
    linea(dr, [(1560, 745), (1560, 1120), (950, 1120)])
    box(dr, 640, 1190, 620, 150, 'giallo', "Passo 4 · Controlli sulla risposta",
        "tipo di evento e di contenuto · intestatario = persona · stato 5 FIRMATO DA USC · "
        "atto non secretato · tipo di certificato emissibile", ts=17, ss=14)
    percorso(dr, [(1260, 1265), (1330, 1265)])
    box(dr, 1335, 1215, 465, 100, 'rosso', "Controllo non superato: rifiuto con il "
        "motivo", "non si ripiega sui dati di SIPO", ts=16, ss=14)
    # 5 pratica
    freccia(dr, (950, 1340), (950, 1370))
    box(dr, 640, 1375, 620, 95, 'verde', "Passo 5 · Nella pratica: fonte ANSC",
        "idAnsc, idEvento, intestatario.id accanto al contrassegno anpr di oggi", ts=17, ss=14)
    # 6 anteprima ed emissione
    freccia(dr, (950, 1470), (950, 1500))
    box(dr, 640, 1505, 620, 120, 'blu', "Passo 6 · Anteprima ed emissione",
        "anteprima: riepilogo dei dati · emetti: R005 di nuovo per idAnsc, poi R002 → PDF in "
        "CERTIFICATI e ANSC_CERTIFICATO", ts=17, ss=14)
    # flusso di oggi
    box(dr, 60, 1615, 400, 95, 'grigio', "Flusso di oggi",
        "ANPR 3002 / 6001 oppure ricerca e modello locale", ts=17, ss=14)
    legenda(dr, 60, 1745, [('grigio', "SIPO, come oggi"), ('verde', "SIPO, nuovo"),
                           ('blu', "chiamate ANSC"), ('giallo', "controlli"),
                           ('rosso', "rifiuto")])
    centra(dr, "Ogni chiamata ad ANSC passa dal concentratore e richiede l’OTP di sessione "
               "dell’operatore.", fnt(F_ITA, 15), 1270, 1660, MUTED)
    im.save(out)
    return out


def ricerca_certificati_ansc(out=os.path.join(IMG, 'ricerca_certificati_ansc.png')):
    """La funzione «Certificati ANSC»: dalla voce di menu alla pagina di rilascio (v0.7)."""
    os.makedirs(IMG, exist_ok=True)
    W, H = 1900, 1330
    im, dr = tela(W, H, "Certificati ANSC: la ricerca dell’atto",
                  "Le pagine sono di SIPO, le chiamate passano dal concentratore, i dati "
                  "arrivano da R005 sintetica")
    banda(dr, 40, 100, 700, 1230, C['verde'][0], "Pagine di SIPO", INK)
    banda(dr, 740, 100, 1240, 1230, C['blu'][0], "Concentratore all-ansc-sipo", INK)
    banda(dr, 1280, 100, 1860, 1230, C['viola'][0], "ANSC – R005", INK)
    # 1 menu
    box(dr, 90, 150, 560, 80, 'grigio', "1 · Menu Municipi › Certificati",
        "terza voce: «Certificati ANSC»", ts=18, ss=15)
    freccia(dr, (370, 230), (370, 262))
    # 2 ricerca
    box(dr, 90, 265, 560, 150, 'verde', "2 · Ricerca atto",
        "per evento: registro, date, identificativo nazionale (avanzata: tipo di contenuto, "
        "comune, numero) · per soggetto: codice fiscale oppure cognome, nome e data di "
        "nascita", ts=18, ss=14)
    # 3 concentratore: cerca
    percorso(dr, [(650, 340), (790, 340)])
    box(dr, 790, 280, 400, 165, 'blu', "3 · cercaEventiAnsc",
        "controlla i criteri, aggiunge testata, OTP di sessione e firma; traccia la "
        "chiamata", ts=17, ss=14)
    percorso(dr, [(1190, 315), (1330, 315)])
    box(dr, 1330, 255, 480, 110, 'viola', "evento/sintetico/1",
        "criteriRicercaEvento: idTipoEvento, dataDa, dataA, idAnsc, idTipoContenuto, "
        "idComuneRegistrazione, idComunale", ts=17, ss=13)
    percorso(dr, [(1190, 410), (1330, 410)])
    box(dr, 1330, 380, 480, 100, 'viola', "soggetto/sintetico/1",
        "criteriRicercaSoggetto: codiceFiscale, cognome, nome, datanascita, sesso, "
        "idAnpr, idAnprUnico…", ts=17, ss=13)
    centra(dr, "un tipo di ricerca per volta", fnt(F_ITA, 14), 990, 452, MUTED)
    # risposta
    percorso(dr, [(1570, 480), (1570, 560), (1190, 560)])
    centra(dr, "elenco di ModelEventoRidotto, paginato", fnt(F_REG, 14), 1430, 568, ARROW)
    box(dr, 790, 520, 400, 120, 'blu', "Esito",
        "errori ANSC tradotti in messaggi; per ogni evento il giudizio di certificabilità",
        ts=17, ss=14)
    percorso(dr, [(790, 600), (650, 600)])
    # 4 elenco
    box(dr, 90, 500, 560, 210, 'verde', "4 · Risultati",
        "intestatario, registro, caso d’uso, data, comune, stato · filtri su stato, "
        "provincia, comune, intestatario applicati all’elenco ricevuto, senza nuove "
        "chiamate · RILASCIA acceso solo per gli atti certificabili", ts=18, ss=14)
    freccia(dr, (370, 710), (370, 760))
    centra(dr, "RILASCIA", fnt(F_BLD, 14), 430, 726, INK)
    # 5 scelta
    box(dr, 90, 765, 560, 90, 'verde', "5 · Atto scelto",
        "si passa soltanto l’identificativo nazionale", ts=18, ss=14)
    percorso(dr, [(650, 810), (790, 810)])
    box(dr, 790, 745, 400, 165, 'blu', "6 · leggiEventoAnsc",
        "rilegge l’atto per idAnsc e ripete i controlli: tipo di contenuto, stato 5, "
        "non secretato, tipi emissibili", ts=17, ss=14)
    percorso(dr, [(1190, 800), (1330, 800)])
    box(dr, 1330, 750, 480, 100, 'viola', "evento/sintetico/1",
        "criteriRicercaEvento: idAnsc", ts=17, ss=13)
    percorso(dr, [(1570, 850), (1570, 960), (1190, 960)])
    centra(dr, "un solo ModelEventoRidotto", fnt(F_REG, 14), 1380, 968, ARROW)
    rombo(dr, 990, 1010, 380, 110, "Ancora certificabile?", ts=17)
    freccia(dr, (990, 910), (990, 955))
    percorso(dr, [(800, 1010), (650, 1010)])
    centra(dr, "sì", fnt(F_BLD, 15), 720, 984, INK)
    box(dr, 90, 960, 560, 110, 'verde', "7 · Rilascio certificazione",
        "si apre con la testata dell’atto letta ora: il seguito è il rilascio", ts=18, ss=14)
    percorso(dr, [(990, 1065), (990, 1110), (650, 1110)])
    centra(dr, "no", fnt(F_BLD, 15), 1015, 1072, INK)
    box(dr, 90, 1095, 560, 80, 'rosso', "Torna ai risultati con il motivo",
        "l’atto è cambiato fra la ricerca e la scelta", ts=16, ss=14)
    legenda(dr, 60, 1270, [('verde', "pagine nuove di SIPO"), ('grigio', "menu di oggi"),
                           ('blu', "concentratore"), ('viola', "servizio ANSC"),
                           ('rosso', "esito negativo")])
    im.save(out)
    return out


if __name__ == '__main__':
    print(instradamento())
    print(sequenza_r002())
    print(ricerca_atto())
    print(innesto_ansc())
    print(ricerca_certificati_ansc())
