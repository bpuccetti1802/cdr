# -*- coding: utf-8 -*-
"""Figure della proposta sull'osservabilità (dalla v0.3).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_otel.py

Produce `img/otel_transizione.png`: il percorso dei dati nel periodo di transizione, dal
programma alla tabella Oracle e al back-office, con il ripiego su console e l'ingresso del
browser. Le stringhe visualizzate usano il doppio apice (vedi diagrammi_comune).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import (C, INK, MUTED, ARROW, F_BLD, F_REG, F_ITA, fnt, box,  # noqa
                              pila, percorso, freccia, banda, legenda, tela, centra,
                              scheda, linea)

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')


def transizione(out=os.path.join(IMG, 'otel_transizione.png')):
    W, H = 1900, 1060
    im, dr = tela(W, H, "Dove vanno i dati nel periodo di transizione",
                  "Dal programma alla tabella e al back-office: tutto resta dentro il cluster "
                  "e la base dati del Comune")

    # perimetro: rete comunale e cluster
    banda(dr, 30, 100, W - 30, 900, C['blu'][0], "Rete comunale — cluster Kubernetes di SIPO",
          C['blu'][0])

    # sorgenti
    x0, w0 = 70, 400
    pila(dr, x0, 160, w0, 150, 'grigio',
         ["Back-end e pod nuovi"],
         ["all-ansc-sipo, dec-ansc-sipo,", "be-numeratore-comunale, automazione,",
          "statocivile-be e i back-end di area"],
         ["libreria osservabilita-sipo + SDK"])
    pila(dr, x0, 350, w0, 130, 'grigio',
         ["Front-end Thymeleaf"],
         ["35 applicazioni, filtro in CommonWeb:", "il contesto nasce qui e va al back-end"],
         ["stessa libreria, lato server"])
    pila(dr, x0, 540, w0, 130, 'viola',
         ["Micro-frontend Angular"],
         ["nel browser dell’operatore:", "accumula gli eventi e li consegna a blocchi"],
         ["libreria condivisa dei micro-frontend"])

    # collector
    xc, wc = 620, 380
    pila(dr, xc, 200, wc, 330, 'giallo',
         ["Collector OpenTelemetry"],
         ["servizio interno, porte 4317 / 4318", "",
          "limite di memoria", "scarta TRACE e DEBUG in produzione",
          "cancella gli attributi vietati", "(seconda barriera dopo la libreria)",
          "raggruppa a blocchi", "coda su disco e ritentativo"],
         ["nessun dato esce dal cluster"])

    # servizio
    xs, ws = 1130, 330
    pila(dr, xs, 200, ws, 330, 'verde',
         ["be-osservabilita"],
         ["riceve OTLP dal collector", "e scrive su Oracle a blocchi", "",
          "riceve gli eventi del browser", "(creaEventi, dietro lo stesso", "ingresso delle altre API)",
          "", "espone le letture al back-office"],
         ["lo «scarico su misura»"])

    # oracle
    xo, wo = 1560, 300
    pila(dr, xo, 200, wo, 330, 'blu',
         ["Oracle 12 — ANSC_USR"],
         ["ANSC_LOG_EVENTO", "ANSC_LOG_SPAN", "partizionate per giorno", "",
          "ANSC_CFG_CODICE_EVENTO", "il catalogo dei codici", "",
          "scadenza: si elimina", "la partizione"],
         ["job notturno"])

    # audit separato
    box(dr, 1560, 600, 300, 120, 'rosso', "ANSC_LOG_AUDIT",
        "probatorio: lo scrive il concentratore, come oggi", ts=19, ss=15)
    percorso(dr, [(420, 160), (420, 145), (1510, 145), (1510, 660), (1555, 660)],
              C['rosso'][0], larg=2)
    centra(dr, "il concentratore registra le chiamate ad ANSC, ora con TRACE_ID",
           fnt(F_ITA, 14), 960, 150, C['rosso'][0])

    # back-office
    box(dr, 1130, 600, 330, 120, 'verde', "Back-office del supporto",
        "Errori e diagnostica · Dettaglio della traccia", ts=19, ss=15)
    freccia(dr, (1295, 535), (1295, 595), etichetta=None)
    centra(dr, "letture", fnt(F_REG, 13), 1250, 555, MUTED)

    # frecce principali
    percorso(dr, [(470, 235), (615, 300)])
    percorso(dr, [(470, 415), (615, 420)])
    centra(dr, "OTLP", fnt(F_BLD, 15), 545, 330, INK)
    freccia(dr, (1000, 365), (1125, 365), etichetta="OTLP / HTTP")
    freccia(dr, (1460, 365), (1555, 365), etichetta="JDBC")

    # browser: niente collector, passa dall'ingresso delle API
    percorso(dr, [(470, 605), (1065, 605), (1065, 470), (1125, 470)], C['viola'][0],
             tratteggio=True)
    centra(dr, "POST /api/v1/osservabilita/eventi (INFO e oltre)", fnt(F_REG, 14),
           770, 615, C['viola'][0])

    # ripiego su console
    box(dr, 70, 740, 400, 120, 'grigio', "Standard output del pod",
        "come oggi: resta il ripiego se tutto il resto è fermo", ts=19, ss=15)
    percorso(dr, [(270, 345), (270, 315)], MUTED)
    percorso(dr, [(40 + 10, 235), (50, 800), (65, 800)], MUTED, tratteggio=True)
    box(dr, 620, 760, 380, 90, 'grigio', "kubectl logs",
        "sistemisti, senza correlazione nei 28 moduli", ts=18, ss=14)
    freccia(dr, (470, 800), (615, 805))

    legenda(dr, 70, 930, [('grigio', "programmi esistenti e nuovi"),
                          ('giallo', "trasporto"), ('verde', "servizio e pagine nuove"),
                          ('blu', "base dati"), ('rosso', "audit probatorio, stesso mestiere"),
                          ('viola', "browser")])
    centra(dr, "La linea tratteggiata viola non attraversa il collector: il browser non lo vede "
               "e scrive solo attraverso l’API, autenticato e limitato.",
           fnt(F_ITA, 15), W / 2, 985, MUTED)
    im.save(out)
    return out


def erd(out=os.path.join(IMG, 'otel_erd.png')):
    """Le tabelle del registro e i loro legami con il modello dell'integrazione.

    Una sola chiave esterna dichiarata (audit -> stato dell'atto); tutto il resto è per
    valore, di proposito: il registro deve accettare eventi di oggetti che non esistono
    ancora, o non più.
    """
    W, H = 1990, 1050
    im, dr = tela(W, H, "Le tabelle del registro e i loro legami",
                  "In alto le tabelle nuove della proposta, in basso quelle del modello "
                  "dell’integrazione a cui si collegano")
    banda(dr, 30, 100, W - 30, 500, C['blu'][0],
          "NUOVE — registro diagnostico, tracce e catalogo dei codici", C['blu'][0])
    banda(dr, 30, 590, W - 30, 900, C['grigio'][0],
          "ESISTENTI — modello dati dell’integrazione [R1]", C['grigio'][0])

    cod = scheda(dr, 60, 200, 420, 'verde', "ANSC_CFG_CODICE_EVENTO", [
        ('PK', "COD_EVENTO"), ('', "COD_ORIGINE, COD_LIVELLO"), ('', "DESC_EVENTO"),
        ('', "TXT_AZIONE_PRIMO_LIV"), ('', "COD_GRUPPO_COMPETENTE"),
        ('', "TXT_NOTE_SECONDO_LIV"), ('', "COD_CODICE_REMOTO"),
        ('', "FLG_RIPETIBILE, FLG_ATTIVO"), ('', "TS_INS … UTENTE_UPD")],
        "il catalogo: lo cura il supporto")
    ev = scheda(dr, 700, 150, 540, 'blu', "ANSC_LOG_EVENTO", [
        ('PK', "ID_EVENTO"), ('P', "TS_EVENTO  (in UTC, partizione per giorno)"),
        ('', "TRACE_ID, SPAN_ID"), ('', "COD_LIVELLO, NUM_SEVERITA"),
        ('', "COD_ORIGINE, COD_EVENTO"), ('', "COD_SERVIZIO, COD_VERSIONE_SW, COD_AMBIENTE"),
        ('', "DESC_MESSAGGIO, TXT_ATTRIBUTI, TXT_ECCEZIONE"),
        ('1', "ID_ATTO_SIPO, ID_ANSC"), ('1', "NUMERO_ATTO, COD_MUNICIPIO"),
        ('2', "ID_ALLEGATO, ID_ANSC_ALLEGATO"), ('3', "ID_SOGGETTO_SIPO, ID_ANSC_SOGGETTO"),
        ('3', "ID_SCHEDA_ANPR, ID_UNICO_NAZIONALE"), ('', "UTENTE, COD_POSTAZIONE")],
        "nessuna chiave esterna: tutti i riferimenti per valore")
    sp = scheda(dr, 1450, 200, 440, 'blu', "ANSC_LOG_SPAN", [
        ('', "TRACE_ID, SPAN_ID"), ('', "SPAN_ID_PADRE"),
        ('P', "TS_INIZIO  (in UTC, partizione)"), ('', "NUM_DURATA_MS"),
        ('', "COD_NOME_PASSO"), ('', "COD_TIPO, COD_ESITO"),
        ('', "COD_SERVIZIO, COD_VERSIONE_SW"), ('1', "ID_ATTO_SIPO"), ('', "TXT_ATTRIBUTI")],
        "nessuna chiave primaria, di proposito")

    hh = 150
    Y = 650
    au = scheda(dr, 60, Y, 380, 'rosso', "ANSC_LOG_AUDIT", [
        ('PK', "ID_AUDIT"), ('FK', "ID_STATO_ATTO"), ('', "FASE, ESITO, DURATA_MS"),
        ('', "RICHIESTA, RISPOSTA, OPERATORE"), ('+', "TRACE_ID, SPAN_ID"),
        ('+', "COD_SERVIZIO, COD_VERSIONE_SW"), ('+', "ID_OPERAZIONE_COMUNE"),
        ('+', "COD_ESITO_ANSC")], "+ colonne proposte", hh=220)
    st = scheda(dr, 520, Y, 340, 'grigio', "ANSC_STATO_ATTO", [
        ('PK', "ID_ATTO_SIPO"), ('', "ID_ANSC, NUMERO_ATTO"), ('', "COD_MUNICIPIO, STATO")],
        "lo stato dell’atto in ANSC", hh=hh)
    al = scheda(dr, 900, Y, 330, 'grigio', "MATR_USR.ALLEGATO", [
        ('PK', "id_allegato"), ('', "id_ansc_allegato"), ('', "id_atto_sipo")],
        "i documenti di un atto", hh=hh)
    so = scheda(dr, 1270, Y, 350, 'grigio', "ANSC_SOGGETTO_IDENTIFICATIVI", [
        ('PK', "ID_SOGGETTO_IDENTIFICATIVI"), ('', "ID_SOGGETTO_SIPO"),
        ('', "ID_ANSC_SOGGETTO"), ('', "ID_ATTO_SIPO")], "il soggetto in ANSC", hh=hh)
    an = scheda(dr, 1660, Y, 290, 'grigio', "ANAG_USR.SOGGETTO", [
        ('', "ID_SCHEDA_ANPR"), ('', "ID_UNICO_NAZIONALE")],
        "i codici ANPR, non duplicati", hh=hh)

    f13 = fnt(F_REG, 14)
    fb = fnt(F_BLD, 14)

    def etichetta(x, y, testo, colore=MUTED, f=f13):
        dr.text((x, y), testo, font=f, fill=colore)

    # catalogo <- evento (N:1 per valore)
    y = 330
    percorso(dr, [(ev[0], y), (cod[2], y)], MUTED, tratteggio=True, larg=2)
    etichetta(500, y - 40, "COD_EVENTO", INK, fb)
    etichetta(500, y - 20, "molti eventi · un codice")
    # evento -> span (N:1 per valore)
    y = 330
    percorso(dr, [(ev[2], y), (sp[0], y)], MUTED, tratteggio=True, larg=2)
    etichetta(1258, y - 40, "TRACE_ID + SPAN_ID", INK, fb)
    etichetta(1258, y - 20, "molti eventi · un passo")
    # span -> span padre
    y1, y2 = sp[1] + 80, sp[1] + 140
    linea(dr, [(sp[2], y1), (sp[2] + 30, y1), (sp[2] + 30, y2)], MUTED, True, 2)
    percorso(dr, [(sp[2] + 30, y2), (sp[2], y2)], MUTED, tratteggio=True, larg=2)
    etichetta(sp[2] - 150, sp[1] - 26, "SPAN_ID_PADRE: l’albero", INK, fb)

    # audit -> stato atto: l'unica chiave esterna
    ym = au[1] + 70
    percorso(dr, [(au[2], ym), (st[0], ym)], ARROW, larg=3)
    etichetta(au[2] + 6, ym - 22, "FK (OT-16)", INK, fb)
    # audit <-> evento per traccia
    xa = 250
    linea(dr, [(xa, au[1]), (xa, 525), (720, 525)], MUTED, True, 2)
    percorso(dr, [(720, 525), (720, ev[3])], MUTED, tratteggio=True, larg=2)
    etichetta(270, 532, "TRACE_ID: dalla riga probatoria alla diagnosi", INK, fb)

    # evento -> esistenti, per piano
    base = ev[3]
    percorso(dr, [(760, base), (760, 545), (690, 545), (690, st[1])], MUTED,
             tratteggio=True, larg=2)
    etichetta(600, Y - 26, "piano 1", INK, fb)
    percorso(dr, [(1065, base), (1065, al[1])], MUTED, tratteggio=True, larg=2)
    etichetta(1075, Y - 26, "piano 2", INK, fb)
    percorso(dr, [(1170, base), (1170, 560), (1445, 560), (1445, so[1])], MUTED,
             tratteggio=True, larg=2)
    etichetta(1455, Y - 26, "piano 3", INK, fb)
    percorso(dr, [(1215, base), (1215, 545), (1805, 545), (1805, an[1])], MUTED,
             tratteggio=True, larg=2)
    etichetta(1815, Y - 26, "piano 3", INK, fb)

    # legenda
    y = 925
    legenda(dr, 60, y, [('verde', "configurazione"), ('blu', "registro"),
                        ('rosso', "audit probatorio"), ('grigio', "tabelle esistenti")])
    y = 962
    linea(dr, [(62, y + 8), (122, y + 8)], ARROW, False, 3)
    etichetta(132, y, "chiave esterna dichiarata")
    linea(dr, [(380, y + 8), (440, y + 8)], MUTED, True, 3)
    etichetta(450, y, "riferimento per valore, senza vincolo")
    etichetta(800, y, "PK chiave primaria · FK chiave esterna · P chiave di partizione · "
                      "1 2 3 piani di tracciabilità · + colonna nuova")
    centra(dr, "I legami fra le tabelle esistenti sono nello schema di [R1] e qui non si "
               "ripetono.", fnt(F_ITA, 15), W / 2, 1005, MUTED)
    im.save(out)
    return out


if __name__ == '__main__':
    print(transizione())
    print(erd())
