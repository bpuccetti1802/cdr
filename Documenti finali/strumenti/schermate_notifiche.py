# -*- coding: utf-8 -*-
"""Pagina «Gestione notifiche ANSC» in stile SIPO, per le slide di formazione (08/11/2026).

Adatta la schermata di Side di Milano («CdMI SIDe MI_ANSC _Gestione Notifiche ANSC (ID 14)
v2.docx», image5: filtri e lista con le azioni conferma / rifiuta / dettaglio) allo stile di
SIPO con le primitive di `schermate_sipo_wf`. Due scostamenti voluti, coerenti con l'analisi:
- niente «CONFERMA TUTTE LE NOTIFICHE DELLA PAGINA»: la conferma è una per notifica (PC-10,
  R008 non ha conferma massiva);
- al posto del contrassegno «OTP ✓» il tempo residuo della sessione ANSC (timer e soglia di
  guardia dell'analisi).
Dati di fantasia, Roma come comune destinatario.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/schermate_notifiche.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S   # noqa: E402
from schermate_sipo_wf import f, lx, avvolgi, M, W, INK, MUTED, BORDO, ROSSO, N_BLD, N_REG  # noqa: E402

OUT = os.path.join(S.IMG, 'formazione_usc', 'sipo_gestione_notifiche_ansc.png')
VERDE = '#2e7d32'
ROSSO_X = '#c62828'


def bottone_bianco(dr, x, y, testo):
    fb = f(N_BLD, 13)
    w = lx(dr, testo, fb) + 28
    dr.rectangle([x, y, x + w, y + 30], fill='white', outline=ROSSO, width=2)
    dr.text((x + 14, y + 7), testo, font=fb, fill=ROSSO)
    return x + w


def sessione(dr, x, y):
    ft = f(N_BLD, 13)
    t = "SESSIONE ANSC ATTIVA · 3 h 12 min"
    w = lx(dr, t, ft) + 44
    dr.rounded_rectangle([x, y, x + w, y + 30], radius=4, outline=VERDE, width=2, fill='#eef7ee')
    S.spunta(dr, x + 12, y + 10, VERDE, 2)
    dr.text((x + 32, y + 7), t, font=ft, fill=VERDE)


def azioni(dr, x, y):
    # conferma
    dr.line([(x, y + 7), (x + 5, y + 12), (x + 14, y + 1)], fill=VERDE, width=3)
    # rifiuta
    x2 = x + 30
    dr.line([(x2, y + 1), (x2 + 12, y + 13)], fill=ROSSO_X, width=3)
    dr.line([(x2 + 12, y + 1), (x2, y + 13)], fill=ROSSO_X, width=3)
    # dettaglio
    x3 = x + 58
    dr.ellipse([x3, y + 1, x3 + 20, y + 13], outline=S.BLU_ICONA, width=2)
    dr.ellipse([x3 + 7, y + 4, x3 + 13, y + 10], fill=S.BLU_ICONA)


def stato(dr, x, y, testo):
    ft = f(N_BLD, 13)
    col = {'Da approvare': ('#b26a00', '#fff4d6'), 'Approvata': (VERDE, '#eef7ee'),
           'Rifiutata': (ROSSO_X, '#fdecea')}[testo]
    w = lx(dr, testo, ft) + 16
    dr.rounded_rectangle([x, y, x + w, y + 22], radius=3, fill=col[1], outline=col[0])
    dr.text((x + 8, y + 3), testo, font=ft, fill=col[0])


COLONNE = [("Intestatario", 110), ("Comune di formazione", 100), ("Evento sorgente", 84),
           ("Registro di destinazione", 92), ("Atto di destinazione", 96), ("Ambito", 84),
           ("Descrizione", 246), ("Formazione", 86), ("ID ANSC notifica", 160),
           ("Stato", 104), ("Genere", 84), ("Azioni", 86)]

RIGHE = [
    ["ROSSI GIULIA", "MILANO (MI)", "10439234", "NASCITA", "2019-1234-1-A", "ARCHIVIO",
     "ROSSI GIULIA è stata riconosciuta quale figlia da ROSSI MARCO come da dichiarazione resa "
     "avanti all’ufficiale dello stato civile di MILANO con numero 2026-10439234-152-015146.",
     "28/10/2026 10:34", "2026-10439234-154-058091", "Da approvare", "Annotazione", None],
    ["BIANCHI LUCA", "TORINO (TO)", "10439163", "MATRIMONIO", "2021-845-2-A", "ARCHIVIO",
     "BIANCHI LUCA ha contratto matrimonio con VERDI ANNA in TORINO, atto "
     "2026-10439163-77-001272.", "27/10/2026 17:47", "2026-10439163-00000-058091",
     "Da approvare", "Annotazione", None],
    ["NERI PAOLO", "FIRENZE (FI)", "10438890", "MORTE", "", "APPROVA_PV",
     "Morte di NERI PAOLO, residente in ROMA, avvenuta in FIRENZE il 25/10/2026: richiesta di "
     "trascrizione.", "26/10/2026 09:12", "2026-10438890-31-058091", "Approvata", "Trascrizione",
     None],
]


def lista(dr, y):
    fi, fr = f(N_BLD, 13), f(N_REG, 13)
    tot = sum(w for _, w in COLONNE)
    x0 = M + (W - 2 * M - tot) // 2
    hi = 46
    dr.rectangle([x0, y, x0 + tot, y + hi], fill='#f2f2f2', outline=BORDO)
    cx = x0
    for t, w in COLONNE:
        for i, r in enumerate(avvolgi(dr, t, fi, w - 12)[:2]):
            dr.text((cx + 6, y + 6 + i * 17), r, font=fi, fill=INK)
        cx += w
    y += hi
    for riga in RIGHE:
        celle = [avvolgi(dr, v, fr, w - 12) if isinstance(v, str) else []
                 for v, (_, w) in zip(riga, COLONNE)]
        h = max(56, 14 + 17 * max(len(c) for c in celle))
        dr.rectangle([x0, y, x0 + tot, y + h], fill='white', outline=BORDO)
        cx = x0
        for j, ((_, w), righe_t) in enumerate(zip(COLONNE, celle)):
            if COLONNE[j][0] == 'Stato':
                stato(dr, cx + 6, y + h // 2 - 11, riga[j])
            elif COLONNE[j][0] == 'Azioni':
                if riga[9] == 'Da approvare':
                    azioni(dr, cx + 8, y + h // 2 - 7)
                else:
                    x3 = cx + 66 - 8
                    dr.ellipse([x3, y + h // 2 - 6, x3 + 20, y + h // 2 + 6],
                               outline=S.BLU_ICONA, width=2)
                    dr.ellipse([x3 + 7, y + h // 2 - 3, x3 + 13, y + h // 2 + 3],
                               fill=S.BLU_ICONA)
            else:
                ty = y + (h - 17 * len(righe_t)) // 2
                for r in righe_t:
                    dr.text((cx + 6, ty), r, font=fr, fill=INK)
                    ty += 17
            cx += w
        y += h
    return y


def disegna():
    im, dr, y = S.pagina("Stato Civile › Gestione notifiche ANSC", alt=1300)
    sessione(dr, M, y)
    bottone_bianco(dr, W - M - lx(dr, "SCARICA NOTIFICHE RECENTI", f(N_BLD, 13)) - 28, y, "SCARICA NOTIFICHE RECENTI")
    y += 48

    y0 = y
    y = S.pannello(dr, y, "Filtri di ricerca", 306)
    cw, gap = 300, 22
    xs = [M + 14 + i * (cw + gap) for i in range(4)]
    for x, (e, v, t) in zip(xs, [("Registro di destinazione", "Tutti", 'select'),
                                 ("Ambito", "Tutti", 'select'),
                                 ("Comune di formazione", "", 'select'),
                                 ("Proposte di annotazione", "", 'select')]):
        S.campo(dr, x, y, cw, e, v, t)
    y += 60
    x = M + 14
    for t, s in (("Nessun filtro operatore", True), ("Nessun operatore", False),
                 ("Filtro per operatore", False)):
        x = S.radio(dr, x, y, t, s)
    y += 30
    S.campo(dr, xs[0], y, cw, "Data inizio", "01/10/2026", 'data')
    S.campo(dr, xs[1], y, cw, "Data fine", "31/10/2026", 'data')
    S.campo(dr, xs[2], y, cw, "ID ANSC evento notifica", "")
    S.campo(dr, xs[3], y, cw, "ID nazionale evento sorgente", "")
    y += 60
    for x, (e, v, t) in zip(xs, [("Stato", "Da approvare", 'select'),
                                 ("Tipo contenuto notifica", "", 'select'),
                                 ("Genere notifica", "", 'select'),
                                 ("Intestatario", "", 'testo')]):
        S.campo(dr, x, y, cw, e, v, t)
    S.bottoni_dx(dr, y0 + 262, [("PULISCI", True), ("CERCA", True)], W - M - 14)
    y = y0 + 326

    dr.text((M, y), "Notifiche trovate: 3", font=f(N_BLD, 15), fill=INK)
    y = lista(dr, y + 30) + 22

    y = S.avviso(dr, y, "Confermare una notifica è un atto dell’ufficiale dello stato civile: "
                        "collega l’annotazione all’atto di Roma e sblocca la comunicazione "
                        "all’anagrafe, che parte solo quando tutti i comuni coinvolti hanno "
                        "confermato. Si conferma una notifica alla volta, nella sessione ANSC.",
                 'info')
    fl = f(N_REG, 13)
    lx0 = M
    for disegno, t in ((lambda x, yy: dr.line([(x, yy + 7), (x + 5, yy + 12), (x + 14, yy + 1)],
                                              fill=VERDE, width=3), "conferma"),
                       (lambda x, yy: (dr.line([(x, yy + 1), (x + 12, yy + 13)], fill=ROSSO_X,
                                               width=3),
                                       dr.line([(x + 12, yy + 1), (x, yy + 13)], fill=ROSSO_X,
                                               width=3)), "rifiuta"),
                       (lambda x, yy: (dr.ellipse([x, yy + 1, x + 20, yy + 13],
                                                  outline=S.BLU_ICONA, width=2),
                                       dr.ellipse([x + 7, yy + 4, x + 13, yy + 10],
                                                  fill=S.BLU_ICONA)), "dettaglio")):
        disegno(lx0, y)
        dr.text((lx0 + 28, y - 1), t, font=fl, fill=MUTED)
        lx0 += 28 + lx(dr, t, fl) + 30
    return S.ritaglia(im, y + 10, OUT)


if __name__ == '__main__':
    print(disegna())
