# -*- coding: utf-8 -*-
"""Pagina «Anteprima · Validazione» di SIPO, seconda stesura (08/11/2026).

Indicazioni dell'utente sulla prima stesura (schermate_anteprima_validazione.py):
  - restano la parte superiore (arrivo, testata) e l'atto a sinistra;
  - a destra i metadati del payload (modello evento) in sezioni ad accordion, ciascuna con il
    suo check;
  - l'esito ricalca la risposta di ANSC (AnscResponse: testataRisposta, errors/warnings/infos/
    success di ServiceMessage {code, severity, text}; per R009 idEvento, idAnsc, idTipoEvento,
    forcingCode);
  - la forzatura si chiede con un pulsante e una finestra (spunto: schermata di Side con
    «Attenzione! Il soggetto è già presente con id …», PROSEGUI ACCETTANDO LE ANOMALIE / TORNA
    ALLA COMPILAZIONE);
  - al caricamento la pagina valida da sé (R009) con i dati raccolti nelle pagine precedenti;
  - se la validazione riesce, un messaggio lo dice e si passa alla pagina successiva.

Le sezioni sono quelle del mapping ANSC Morte_001 (UC 2101) presenti nell'atto di esempio.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_anteprima_validazione_v2.py
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S   # noqa: E402
import schermate_anteprima_validazione as A   # noqa: E402
from schermate_sipo_wf import (f, lx, avvolgi, M, W, INK, MUTED, BORDO, ROSSO, N_BLD,  # noqa: E402
                               N_REG, N_ITA, AVVISI)

OUT = os.path.join(S.IMG, 'anteprima_validazione', 'v2')
X, L = A.X_DX, A.L_DX
VERDE, ROSSO_X, AMBRA = A.VERDE, A.ROSSO_X, A.AMBRA

# sezioni del modello evento (mapping Morte_001), con i campi valorizzati dall'atto di esempio
SEZIONI = [
    ("Formazione atto", [("Numero comunale", "004218"), ("Data formazione", "08/11/2026"),
                         ("Ora formazione", "10"), ("Minuti formazione", "30")]),
    ("Dettagli evento", [("Caso d’uso", "2101"), ("Tipo evento", "2 MORTE")]),
    ("Deceduto", [("Cognome", "ROSSI"), ("Nome", "MARIO"), ("Sesso", "M"),
                  ("Data nascita", "03/06/1950"), ("Stato nascita", "ITALIA"),
                  ("Comune nascita", "NAPOLI (NA)"), ("Nazionalità", "ITALIANA"),
                  ("Identificativo ANSC soggetto", "2262046")]),
    ("Comparente 1 – dichiarante", [("Cognome", "BIANCHI"), ("Nome", "LAURA"), ("Sesso", "F"),
                                     ("Data nascita", ""), ("Stato nascita", "ITALIA"),
                                     ("Flag dichiarante", "sì"), ("Flag comparente", "sì")]),
    ("Dati decesso", [("Data decesso", "06/11/2026"), ("Ora e minuti", "14:20"),
                      ("Luogo", "ROMA – VIA DEI GERANI 14, abitazione")]),
    ("Atto di nascita del deceduto", [("Comune", "NAPOLI"), ("Anno", "1950")]),
    ("Formula", [("Formule adottate", "1")]),
    ("Allegati", [("Certificato necroscopico", "R001 · 3 Inserito")]),
]


# ------------------------------------------------------------------------------ accordion
def chevron(dr, x, y, aperto):
    if aperto:
        dr.line([(x, y + 3), (x + 6, y + 9), (x + 12, y + 3)], fill=INK, width=2)
    else:
        dr.line([(x + 3, y), (x + 9, y + 6), (x + 3, y + 12)], fill=INK, width=2)


def accordion(dr, y, stati, aperta=None, errore_campo=None):
    """stati: sezione → 'ok' | 'ko' | 'att' | 'attesa'. aperta: sezione espansa."""
    xi, li = X + 12, L - 24
    for nome, campi in SEZIONI:
        st = stati.get(nome, 'ok')
        fondo = {'ko': '#fbe3e6', 'att': '#fff4d6'}.get(st, 'white')
        dr.rectangle([xi, y, xi + li, y + 38], fill=fondo, outline=BORDO)
        chevron(dr, xi + 12, y + 13, nome == aperta)
        dr.text((xi + 34, y + 10), nome, font=f(N_BLD, 14), fill=INK)
        n = "%d campi" % len(campi) if len(campi) != 1 else "1 campo"
        dr.text((xi + li - 120, y + 11), n, font=f(N_REG, 13), fill=MUTED)
        if st == 'attesa':
            dr.text((xi + li - 34, y + 10), "…", font=f(N_BLD, 15), fill=MUTED)
        else:
            A.icona(dr, xi + li - 30, y + 10, st)
        y += 38
        if nome == aperta:
            for et, val in campi:
                ko = errore_campo == et
                dr.rectangle([xi, y, xi + li, y + 28], fill='#fdf3f4' if ko else '#fafafa',
                             outline=BORDO)
                dr.text((xi + 34, y + 6), et, font=f(N_REG, 13), fill=MUTED)
                dr.text((xi + 250, y + 5), val or "— non compilato", font=f(N_BLD, 14),
                        fill=ROSSO_X if ko else INK)
                if ko:
                    dr.text((xi + li - 150, y + 6), "CORREGGI NEL DETTAGLIO", font=f(N_BLD, 12),
                            fill=ROSSO)
                y += 28
    return y + 10


def metadati(dr, y, stati, aperta=None, errore_campo=None, nota=None):
    def contenuto(d, yy):
        yy = accordion(d, yy, stati, aperta, errore_campo)
        if nota:
            for r in avvolgi(d, nota, f(N_ITA, 13), L - 24):
                d.text((X + 12, yy), r, font=f(N_ITA, 13), fill=MUTED)
                yy += 17
        return yy
    return A.blocco(dr, y, "Modello evento inviato ad ANSC – UC 2101", contenuto)


# ----------------------------------------------------------------------------------- esito
def messaggi(dr, y, righe):
    """Tabella dei ServiceMessage: elenco, code, severity, text."""
    xi = X + 12
    larg = (88, 80, 80, L - 24 - 248)
    fi, fr = f(N_BLD, 13), f(N_REG, 13)
    tot = sum(larg)
    dr.rectangle([xi, y, xi + tot, y + 28], fill='#f2f2f2', outline=BORDO)
    cx = xi
    for t, w in zip(("elenco", "code", "severity", "text"), larg):
        dr.text((cx + 6, y + 6), t, font=fi, fill=INK)
        cx += w
    y += 28
    for riga in righe:
        celle = [avvolgi(dr, v, fr, w - 12) for v, w in zip(riga, larg)]
        h = 10 + 17 * max(len(c) for c in celle)
        dr.rectangle([xi, y, xi + tot, y + h], fill='white', outline=BORDO)
        cx = xi
        for c, w in zip(celle, larg):
            for i, r in enumerate(c):
                dr.text((cx + 6, y + 5 + 17 * i), r, font=fr, fill=INK)
            cx += w
        y += h
    return y + 10


def chiave_valore(dr, y, coppie):
    xi, li = X + 12, L - 24
    for et, val in coppie:
        dr.rectangle([xi, y, xi + li, y + 28], fill='white', outline=BORDO)
        dr.text((xi + 8, y + 6), et, font=f(N_REG, 13), fill=MUTED)
        dr.text((xi + 200, y + 5), val, font=f(N_BLD, 14), fill=INK)
        y += 28
    return y + 10


def spinner(dr, x, y):
    for i in range(8):
        import math
        a = i * math.pi / 4
        c = 90 + i * 20
        dr.ellipse([x + 12 + 10 * math.cos(a) - 3, y + 12 + 10 * math.sin(a) - 3,
                    x + 12 + 10 * math.cos(a) + 3, y + 12 + 10 * math.sin(a) + 3],
                   fill=(c, c, c))


def esito(dr, y, caso):
    def contenuto(d, yy):
        xi, li = X + 12, L - 24
        if caso == 'attesa':
            spinner(d, xi, yy)
            d.text((xi + 36, yy + 3), "Validazione in corso: R009 /validazione/evento con i dati "
                   "raccolti nelle pagine precedenti…", font=f(N_REG, 14), fill=INK)
            return yy + 34
        if caso == 'ok':
            yy = S.avviso(d, yy, "Validazione riuscita (HTTP 200): atto depositato in ANSC, "
                          "stato 2 CONFERMATO.", 'ok', xi, li)
            return chiave_valore(d, yy, [("idOperazione", "c903f4d1-52aa-4b07"),
                                         ("idAnsc", A.ID_ANSC), ("idEvento", "4245234"),
                                         ("idTipoEvento", "2 MORTE")])
        if caso == 'errori':
            yy = S.avviso(d, yy, "Validazione respinta (HTTP 400): l’atto non è stato depositato e "
                          "in ANSC non resta nulla. Il numero comunale resta all’atto.",
                          'errore', xi, li)
            yy = chiave_valore(d, yy, [("idOperazione", "a71c0e52-3d4b-4f1e"),
                                       ("forcingCode", "— non restituito")])
            return messaggi(d, yy, [
                ("errors", "400001", "ERROR", "Campo obbligatorio non compilato: "
                 "evento.datiEventoMorte.comparente1.dataNascita")])
        # anomalie superabili
        yy = S.avviso(d, yy, "ANSC segnala anomalie superabili e restituisce un codice di "
                      "forzatura: l’atto non è stato depositato. Si correggono i dati oppure "
                      "l’ufficiale dello stato civile forza la validazione.", 'attenzione', xi, li)
        yy = chiave_valore(d, yy, [("idOperazione", "b25e9a10-7c81-44d2"),
                                   ("forcingCode", "XXXXX_1234")])
        return messaggi(d, yy, [
            ("errors", "—", "—", "Il soggetto è già presente con id 2262046,9516739")])
    return A.blocco(dr, y, "Esito della validazione – risposta di ANSC", contenuto)


# ---------------------------------------------------------------------------------- finestra
def finestra(im, titolo, righe, voci, colore=ROSSO, y_centro=640):
    """Finestra modale sopra la pagina oscurata, sul modello della schermata di Side."""
    velo = Image.new('RGBA', im.size, (0, 0, 0, 105))
    base = im.convert('RGBA')
    base.alpha_composite(velo)
    im.paste(base.convert('RGB'))
    dr = ImageDraw.Draw(im)
    w = 620
    x0 = (W - w) // 2
    fr = f(N_REG, 15)
    corpo = []
    for stile, t in righe:
        font = {'b': f(N_BLD, 15), 'i': f(N_ITA, 14), 'r': fr}[stile]
        corpo += [(font, r, MUTED if stile == 'i' else INK) for r in avvolgi(dr, t, font, w - 48)]
        corpo.append(None)
    h = 56 + 24 + sum(22 if c else 8 for c in corpo) + 70
    y0 = y_centro - h // 2
    dr.rectangle([x0 + 4, y0 + 6, x0 + w + 4, y0 + h + 6], fill='#3a3a3a')
    dr.rectangle([x0, y0, x0 + w, y0 + h], fill='white')
    dr.rectangle([x0, y0, x0 + w, y0 + 52], fill=colore)
    dr.text((x0 + 22, y0 + 14), titolo, font=f(N_BLD, 19), fill='white')
    y = y0 + 52 + 22
    for c in corpo:
        if c is None:
            y += 8
            continue
        font, r, col = c
        dr.text((x0 + 24, y), r, font=font, fill=col)
        y += 22
    y += 12
    fb = f(N_BLD, 13)
    larghe = [lx(dr, t, fb) + 40 for t, _ in voci]
    x = x0 + w - 24 - sum(larghe) - 14 * (len(voci) - 1)
    for (t, pieno), bw in zip(voci, larghe):
        if pieno:
            dr.rectangle([x, y, x + bw, y + 40], fill=colore)
            dr.text((x + 20, y + 12), t, font=fb, fill='white')
        else:
            dr.rectangle([x, y, x + bw, y + 40], fill='white', outline=colore, width=2)
            dr.text((x + 20, y + 12), t, font=fb, fill=colore)
        x += bw + 14


# -------------------------------------------------------------------------------- pagine
def disegna(caso, nome):
    im, dr, y = S.pagina("Dichiarazione Morte – Anteprima Atto · Validazione ANSC", alt=1900)
    y = A.arrivo(dr, y)
    if caso == 'ok':
        y = A.testata(dr, y, "2 CONFERMATO", A.ID_ANSC)
    else:
        y = A.testata(dr, y, "— (nessun atto)", "—")
    ytop = y
    if caso == 'attesa':
        yd = metadati(dr, ytop, {n: 'attesa' for n, _ in SEZIONI},
                      nota="I check si accendono con la risposta di ANSC.")
        yd = esito(dr, yd, 'attesa')
    elif caso == 'errori':
        yd = metadati(dr, ytop, {"Comparente 1 – dichiarante": 'ko'},
                      aperta="Comparente 1 – dichiarante", errore_campo="Data nascita")
        yd = esito(dr, yd, 'errori')
    elif caso == 'forzatura':
        yd = metadati(dr, ytop, {"Deceduto": 'att'}, aperta="Deceduto",
                      errore_campo="Identificativo ANSC soggetto")
        yd = esito(dr, yd, 'forzatura')
    else:
        yd = metadati(dr, ytop, {})
        yd = esito(dr, yd, 'ok')
    ys = A.anteprima(im, dr, ytop, max(yd - ytop - 42, 640))
    y = max(yd, ys + 16)
    forz = caso == 'forzatura'
    attivi = caso in ('errori', 'forzatura')
    y = S.pulsantiera(dr, y, [("TORNA AI DATI", caso != 'attesa')],
                      [("INTERROMPI", caso != 'attesa'), ("VALIDA DI NUOVO", attivi),
                       ("FORZA LA VALIDAZIONE", forz)])
    im = im.crop((0, 0, W, y + 26))
    if forz:
        finestra(im, "Attenzione!", [
            ('r', "ANSC ha restituito queste anomalie:"),
            ('b', "Il soggetto è già presente con id 2262046,9516739"),
            ('r', "Proseguendo, la validazione si ripete con il codice di forzatura XXXXX_1234 "
                  "restituito da ANSC e l’atto entra in ANSC come anomalo."),
            ('i', "Riservato all’ufficiale dello stato civile: la forzatura si registra con il suo "
                  "identificativo e le anomalie accettate.")],
            [("TORNA ALLA COMPILAZIONE", False), ("PROSEGUI ACCETTANDO LE ANOMALIE", True)],
            y_centro=im.height // 2)
    elif caso == 'ok':
        finestra(im, "Validazione riuscita", [
            ('r', "L’atto è stato depositato in ANSC nello stato 2 CONFERMATO."),
            ('b', "Identificativo nazionale " + A.ID_ANSC),
            ('r', "idEvento 4245234 · idTipoEvento 2 MORTE: salvati sull’atto con il modello "
                  "evento validato."),
            ('i', "Si passa alla pagina delle firme dei dichiaranti.")],
            [("PROSEGUI", True)], colore='#2e7d32', y_centro=im.height // 2)
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, nome)
    im.save(dest)
    return dest


if __name__ == '__main__':
    print(disegna('attesa', 'av2_1_caricamento.png'))
    print(disegna('errori', 'av2_2_ko_errori.png'))
    print(disegna('forzatura', 'av2_3_forzatura.png'))
    print(disegna('ok', 'av2_4_ok.png'))
