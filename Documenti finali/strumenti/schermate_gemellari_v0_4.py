# -*- coding: utf-8 -*-
"""Ipotesi di schermata, nello stile di SIPO, del caso 2 del parto plurimo (gemelli con UC diversi),
analisi delle nascite gemellari v0.4 (21/11/2026). Primitive di `schermate_sipo_wf`.

  * gem4_dati_ansc.png — il riepilogo del gemello 1 quando gli UC dei nati non coincidono: avviso,
    PRENOTA GEMELLI assente, e la pagina «Dati per ANSC» del parto con i numeri comunali staccati
    in blocco, lo stato di ciascun nato e la tipologia di nascita da indicare sulla web app;
  * gem4_recupero.png  — l'esito di RECUPERA GEMELLI: per ciascun gemello l'atto ANSC trovato per
    numero comunale, i controlli di abbinamento e l'esito; DEFINISCI GEMELLI attivo solo se tutti i
    gemelli sono abbinati.
Nomi e codici sono di esempio; nessun dato di persone reali.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_gemellari_v0_4.py
"""
import os

import schermate_sipo_wf as S

DIR = os.path.join(S.IMG, 'gemellari')
NATI = (("1", "NATO 1 — COGNOME NOME", "M", "Nato vivo", "11111000", "1 nato vivo", "13617"),
        ("2", "NATO 2 — COGNOME NOME", "F", "Nato morto", "11111100", "2 nato morto", "13618"))


def _testata(dr, y, ansc="WA · ATTESA WEBAPP"):
    y = S.pannello(dr, y, "Atto di nascita – parto plurimo", 112)
    larg = S.W - 2 * S.M - 24
    x = S.M + 12
    for quota, et, val in ((0.26, "Tipo atto", "1429 – gemelli in costanza di matrimonio"),
                           (0.16, "Numero gemelli", "2"), (0.18, "Atto in visione", "gemello 1 di 2"),
                           (0.20, "Stato SIPO", "1 IN LAVORAZIONE"),
                           (0.20, "Stato ANSC", ansc)):
        w = int(larg * quota) - 12
        S.campo(dr, x, y, w, et, val, 'lettura')
        x += w + 12
    return y + 78


def dati_ansc(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Dati per ANSC")
    y = S.avviso(dr, y, "I nati di questo parto hanno casi d’uso ANSC diversi (un nato vivo e un "
                 "nato morto). ANSC non consente di prenotarli dal gestionale con un unico caso "
                 "d’uso: gli atti si formano sulla web app ANSC, con il caso d’uso di servizio "
                 "delle dichiarazioni di nascita, e si recuperano poi in SIPO con RECUPERA GEMELLI.",
                 'attenzione')
    y = _testata(dr, y)
    cols = ("Pos.", "Nato", "Sesso", "Stato del nato", "UC del nato", "Tipologia di nascita",
            "N. comunale")
    larg = (50, 250, 70, 150, 130, 230, 130)
    y = S.pannello(dr, y, "Da riportare sulla web app – Prenotazione parti gemellari", 60 + 34 * 3)
    y = S.tabella(dr, y, cols, larg, [tuple(n) for n in NATI], x=S.M + 12) + 6
    y = S.avviso(dr, y, "Sulla web app: numero gemelli 2 (nati morti compresi) e i numeri comunali "
                 "nell’ordine della tabella. In ciascuna bozza indicare nei dati generali la "
                 "tipologia di nascita del nato e riportare nella composizione gli identificativi "
                 "dei fratelli. Il testo dell’atto si copia con COPIA TESTO.", 'info')
    y = S.pulsantiera(dr, y + 8, [("INDIETRO", True)],
                      [("COPIA TESTO", True), ("RECUPERA GEMELLI", True),
                       ("DEFINISCI GEMELLI", False)])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    S.ritaglia(im, y, dest)
    return dest


def recupero(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Recupera gemelli")
    y = S.avviso(dr, y, "Recupero eseguito: ANSC ha restituito 2 atti per i numeri comunali del "
                 "parto. Entrambi sono abbinati al proprio gemello e firmati dall’ufficiale.", 'ok')
    y = _testata(dr, y)
    cols = ("Pos.", "N. comunale", "Identificativo nazionale", "Stato ANSC", "UC",
            "Intestatario ANSC", "Tipologia", "Esito")
    larg = (50, 110, 290, 170, 110, 170, 140, 120)
    righe = [(p, num, "2026-%d-%s-058091" % (10527617 + int(p), num), "5 FIRMATO DA USC",
              "11999999", "SESSO %s · 21/11/2026" % s, tip, "ABBINATO")
             for p, _n, s, _st, _uc, tip, num in NATI]
    y = S.pannello(dr, y, "Atti ANSC trovati per numero comunale (R005)", 60 + 34 * 3)
    y = S.tabella(dr, y, cols, larg, righe, x=S.M + 12) + 6
    y = S.avviso(dr, y, "Controlli per gemello: numero comunale contenuto nell’identificativo, "
                 "stato 5, caso d’uso di servizio, intestatario (sesso, data e ora di nascita) e "
                 "tipologia di nascita uguali a quelli del nato in SIPO. DEFINISCI GEMELLI definisce "
                 "gli atti in SIPO senza importare dati da ANSC.", 'info')
    y = S.pulsantiera(dr, y + 8, [("INDIETRO", True)],
                      [("RIPETI RICERCA", True), ("DEFINISCI GEMELLI", True)])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    S.ritaglia(im, y, dest)
    return dest


if __name__ == '__main__':
    print(dati_ansc(os.path.join(DIR, 'gem4_dati_ansc.png')))
    print(recupero(os.path.join(DIR, 'gem4_recupero.png')))
