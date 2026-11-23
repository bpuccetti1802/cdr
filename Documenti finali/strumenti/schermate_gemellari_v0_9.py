# -*- coding: utf-8 -*-
"""Schermate del caso 1 per l'analisi delle nascite gemellari v0.9 (21/11/2026).

Correzione rispetto alla v0.8 (decisione dell'utente, 21/11/2026, su issue #2299 di ANSC): per le
bozze prenotate da gestionale il TESTO DELL'ATTO LO GENERA SIPO e lo trasmette con la validazione
(composizioneCompleta). Rifatte le schermate del caso 1 che mostravano il testo «composto da ANSC»:
  gem9_c1_gemello.png  gemello 2 sul passo della firma del dichiarante
  gem9_c1_definito.png gemello 2 formato e definito in SIPO
  gem9_c1_esito.png    esito del parto
  gem9_seq_caso1.png   sequenza delle schermate del caso 1
Le altre schermate della v0.8 (raccordo, caso 2) restano valide.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_gemellari_v0_9.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schermate_sipo_wf as S                                       # noqa: E402
import schermate_gemellari_v0_8 as G8                               # noqa: E402

png = G8.png
C1 = G8.C1
PASSI = ("Documenti", "Testo e validazione", "Firma dichiarante", "Conformità", "Firma USC",
         "Definizione in SIPO")
FRATELLI = C1[0][6] + ", " + C1[2][6]


def c1_gemello(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Definisci gemelli · gemello 2 di 3", alt=1500)
    y = S.avviso(dr, y, "Da Testo e validazione: SIPO ha composto il testo dell’atto del gemello 2 "
                 "con il formulario, con il numero comunale e gli identificativi dei fratelli, e "
                 "lo ha inviato con la validazione (R009, composizioneCompleta). Stato ANSC 2 "
                 "CONFERMATO; il PDF riletto da ANSC (R010) è quello che il dichiarante firma.",
                 'ok')
    y = G8._barra_gemelli(dr, y, C1, (("2 DEFINITO", 'fatto'), ("in lavorazione", 'corso'),
                                      ("in attesa", 'attesa')))
    y = G8._passi(dr, y, PASSI, 2)
    y = G8._testata_gemello(dr, y, C1[1], "2 CONFERMATO", "1 IN LAVORAZIONE")
    xs, ws = S.M, 760
    dr.text((xs, y), "Testo dell’atto – composto da SIPO, inviato ad ANSC", font=S.f(S.N_BLD, 15),
            fill=S.INK)
    G8._testo_atto(dr, xs, y + 24, ws, 260, C1[1][5], FRATELLI, None,
                   "PDF riletto da ANSC (R010)")
    xr = xs + ws + 20
    G8._riquadro_azioni(dr, xr, y + 24, S.W - S.M - xr, "Firma del dichiarante (R006)", (
        (True, "Testo stampato e consegnato al dichiarante"),
        (None, "Caricare il PDF con la firma autografa del dichiarante"),
        (False, "Processo verbale caricato in ANSC"),
        (False, "Stato ANSC 4 FIRMATO DAL DICHIARANTE")))
    S.campo(dr, xr + 14, y + 24 + 204, S.W - S.M - xr - 28, "PDF firmato", "", 'file')
    y += 24 + 260 + 20
    y = S.pulsantiera(dr, y, [("SOSPENDI", True)], [("STAMPA", True), ("CARICA LA FIRMA", True)])
    S.ritaglia(im, y, dest)
    return dest


def c1_definito(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Definisci gemelli · gemello 2 di 3", alt=1500)
    y = S.avviso(dr, y, "Da Firma dell’USC: atto del gemello 2 firmato dall’ufficiale (R007), "
                 "stato ANSC 5 FIRMATO DA USC. L’atto è stato definito in SIPO: il suo documento è "
                 "il PDF del testo composto da SIPO, lo stesso inviato ad ANSC.", 'ok')
    y = G8._barra_gemelli(dr, y, C1, (("2 DEFINITO", 'fatto'), ("2 DEFINITO", 'fatto'),
                                      ("in attesa", 'attesa')))
    y = G8._passi(dr, y, PASSI, 6)
    y = G8._testata_gemello(dr, y, C1[1], "5 FIRMATO DA USC", "2 DEFINITO")
    xs, ws = S.M, 760
    dr.text((xs, y), "Documento dell’atto in SIPO", font=S.f(S.N_BLD, 15), fill=S.INK)
    G8._testo_atto(dr, xs, y + 24, ws, 260, C1[1][5], FRATELLI, None, "fonte: SIPO, formulario")
    xr = xs + ws + 20
    G8._riquadro_azioni(dr, xr, y + 24, S.W - S.M - xr, "Definizione del gemello 2", (
        (True, "Testo inviato ad ANSC con la validazione (composizioneCompleta)"),
        (True, "Atto firmato dall’ufficiale: 5 FIRMATO DA USC"),
        (True, "Atto definito in SIPO: /finalizzaAtto, 2 DEFINITO, PDF in ATTO_SCANSIONATO"),
        (True, "Store aggiornato: ANSC_STATO_ATTO a 5, fase FIRMATO"),
        (False, "Il gemello 3 attende: si prosegue con GEMELLO SUCCESSIVO")))
    y += 24 + 260 + 20
    y = S.pulsantiera(dr, y, [("SOSPENDI", True)], [("APRI IL PDF", True),
                                                    ("GEMELLO SUCCESSIVO", True)])
    S.ritaglia(im, y, dest)
    return dest


def c1_esito(dest):
    return G8._esito(dest, C1, "DEFINISCI concluso: i 3 atti del parto sono formati in ANSC e "
                     "definiti in SIPO, ciascuno con il testo composto da SIPO e inviato ad ANSC.",
                     "Testo dell’atto", ["di SIPO, inviato con la validazione"] * 3)


def seq_caso1(dest):
    return G8.sequenza(
        dest, "Caso 1 – gemelli con lo stesso UC: la sequenza delle schermate",
        "tutto da SIPO, anche il testo dell’atto; sulle frecce il comando e i servizi; il ciclo si "
        "ripete per ciascun gemello",
        [("Riepilogo gemelli", png('gem5_riepilogo.png')),
         ("Raccordo dei numeri comunali", png('gem8_c1_raccordo.png')),
         ("Gemello k: testo, validazione, firme", png('gem9_c1_gemello.png')),
         ("Gemello k: definizione in SIPO", png('gem9_c1_definito.png')),
         ("Esito del parto", png('gem9_c1_esito.png'))],
        ["DEFINISCI\nPOST /richiesta (N numeri)\nR009 /prenota/evento",
         "PROSEGUI\ngemello 1",
         "FIRMA USC (R007)\n/finalizzaAtto",
         "dopo l’ultimo gemello"],
        (3, 2, "GEMELLO\nSUCCESSIVO\n(k+1)"),
        "Al passo 3: documenti, testo composto da SIPO e validazione (R009 con composizioneCompleta), "
        "firma del dichiarante, conformità, firma dell’USC, con la fila dei gemelli in testa.")


if __name__ == '__main__':
    for fn, nome in ((c1_gemello, 'gem9_c1_gemello.png'), (c1_definito, 'gem9_c1_definito.png'),
                     (c1_esito, 'gem9_c1_esito.png'), (seq_caso1, 'gem9_seq_caso1.png')):
        print(fn(png(nome)))
