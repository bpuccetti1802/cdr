# -*- coding: utf-8 -*-
"""Il workflow SIPO-ANSC come macchina a stati (WORKFLOW_Interfacce-SIPO-ANSC, 21/10/2026).

Ogni stato è una COPPIA: lo stato della pratica in SIPO (MATR_USR.ATTO.ID_STATO_PRATICA) e lo
stato dell'atto in ANSC (decodifica ANSC_11, replicato in ANSC_STATO_ATTO.STATO). Sulle frecce
c'è la pagina o il servizio che provoca il passaggio. Il workflow di riferimento è
img/workflow_ansc_sipo.pptx (capitolo 13 dell'analisi): se cambia, questa figura va riletta.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_workflow_stati.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
W, H = 1700, 1600
X, LW, LH = 560, 480, 110          # colonna principale: ascissa, larghezza, altezza degli stati
ROSSO, VERDE = '#b03a48', '#3f8f5f'

# nome: (x, y, w, h, colore, titolo, sottotitolo)
STATI = {
    'A': (X, 130, LW, 84, 'grigio', 'Nessun atto', 'SIPO —  ·  ANSC —'),
    'B': (X, 280, LW, LH, 'blu', 'In lavorazione',
          'SIPO 1 IN LAVORAZIONE  ·  ANSC nessun atto (locale IN_PREPARAZIONE)'),
    'C': (X, 500, LW, LH, 'giallo', 'Validato', 'SIPO 1  ·  ANSC 2 CONFERMATO, idAnsc assegnato'),
    'D': (1250, 500, 400, LH, 'viola', 'Da rivalidare',
          'SIPO 1  ·  ANSC 2 CONFERMATO; locale 0 BOZZA applicativa'),
    'I': (60, 500, 400, LH, 'grigio', 'Abbandonato dopo la validazione',
          'SIPO: annullamento pratica [DA VERIFICARE]  ·  ANSC 3 ANNULLATO'),
    'E': (X, 700, LW, LH, 'giallo', 'Firmato dai dichiaranti',
          'SIPO 1  ·  ANSC 4 FIRMATO DAL DICHIARANTE'),
    'F': (X, 900, LW, LH, 'giallo', 'Firmato per conformità',
          'SIPO 1  ·  ANSC 11 FIRMATO PER CONFORMITÀ'),
    'G': (X, 1150, LW, LH, 'verde', 'Atto formato',
          'SIPO 2 DEFINITO  ·  ANSC 5 FIRMATO DA USC'),
    'H': (1250, 1150, 400, LH, 'rosso', 'Sospeso in SIPO',
          'SIPO 3 (aggiornamento anagrafico non riuscito o in attesa)  ·  ANSC 5'),
    'J': (X, 1350, LW, 96, 'viola', 'Dopo la formazione',
          'ANSC 9 CANCELLATO · 3 ANNULLATO · 10 INEFFICACE'),
}


def lato(n, quale):
    x, y, w, h = STATI[n][:4]
    return {'n': (x + w / 2, y), 's': (x + w / 2, y + h), 'o': (x, y + h / 2),
            'e': (x + w, y + h / 2)}[quale]


def etichetta(dr, testo, x, y, colore=G.ARROW, allinea='s'):
    f = G.fnt(G.F_REG, 15)
    for i, rg in enumerate(testo.split('\n')):
        if allinea == 'c':
            G.centra(dr, rg, f, x, y + i * 19, colore)
        else:
            dr.text((x, y + i * 19), rg, font=f, fill=colore)


def disegna(dest=None):
    dest = dest or os.path.join(IMG, 'workflow_stati.png')
    im, dr = G.tela(W, H, 'Il workflow come macchina a stati',
                    'ogni stato è la coppia stato SIPO · stato ANSC; sulle frecce la pagina o il '
                    'servizio che provoca il passaggio')

    # la redazione interrompibile: dagli stati di lavorazione fino alla firma dell'USC
    dr.rounded_rectangle([X - 30, 262, X + LW + 30, 1030], radius=16, outline='#7b5aa6',
                         width=2)
    etichetta(dr, 'riquadro viola: la redazione\nsi interrompe e si riprende\n(COD_PAGINA_RIPRESA)',
              60, 280, '#7b5aa6')

    for n, (x, y, w, h, col, tit, sot) in STATI.items():
        G.box(dr, x, y, w, h, col, tit, sot, ts=20, ss=15)

    # A → B
    G.freccia(dr, lato('A', 's'), lato('B', 'n'))
    etichetta(dr, 'scelta del tipo di atto:\ncreazione della pratica', X + LW / 2 + 14, 226)
    # B: anello delle pagine prima della validazione
    xe, yb = X + LW, 280
    G.percorso(dr, [(xe, yb + 30), (xe + 70, yb + 30), (xe + 70, yb + 80), (xe, yb + 80)])
    etichetta(dr, 'Ricerca, Dettaglio (R005), Riepilogo (UC,\npre-filtro), Anteprima '
              '(numero comunale);\nR009 respinta: si corregge e si ripete', xe + 84, yb + 22)
    # B → C
    G.freccia(dr, lato('B', 's'), lato('C', 'n'), VERDE)
    etichetta(dr, 'Validazione: R009 accettata', X + LW / 2 + 14, 428, VERDE)
    # C ↔ D
    G.percorso(dr, [(X + LW, 525), (1250, 525)])
    etichetta(dr, 'modifica dei dati\ndopo la validazione', X + LW + 20, 478)
    G.percorso(dr, [(1250, 585), (X + LW, 585)], VERDE)
    etichetta(dr, 'nuova validazione R009', X + LW + 20, 592, VERDE)
    # C → I
    G.percorso(dr, [(X, 555), (460, 555)], ROSSO, True)
    etichetta(dr, 'R011 annulla', 470, 528, ROSSO)
    # C → E, C → F (senza firmatari), E → F
    G.freccia(dr, lato('C', 's'), lato('E', 'n'))
    etichetta(dr, 'Firme dei dichiaranti: R006 o R012', X + LW / 2 + 14, 628)
    G.percorso(dr, [(X, 585), (X - 60, 585), (X - 60, 955), (X, 955)], G.MUTED, True)
    etichetta(dr, 'senza\nfirmatari', X - 150, 740, G.MUTED)
    G.freccia(dr, lato('E', 's'), lato('F', 'n'))
    etichetta(dr, 'Conformità: R007 /attestazione/firma', X + LW / 2 + 14, 828)
    # F → G, il punto di non ritorno
    G.freccia(dr, lato('F', 's'), lato('G', 'n'), VERDE)
    etichetta(dr, 'Firma dell’USC: R007 /firma_usc,\nR014, salvataggio in SIPO',
              X + LW / 2 + 14, 1040, VERDE)
    G.linea(dr, [(60, 1124), (W - 60, 1124)], ROSSO, True, 3)
    dr.text((70, 1098), 'punto di non ritorno', font=G.fnt(G.F_BLD, 15), fill=ROSSO)
    # G ↔ H
    G.percorso(dr, [(X + LW, 1175), (1250, 1175)], ROSSO)
    etichetta(dr, 'aggiornamento anagrafico\nKO o in attesa', X + LW + 20, 1132, ROSSO)
    G.percorso(dr, [(1250, 1240), (X + LW, 1240)], VERDE)
    etichetta(dr, 'annullaSospensioneAtto', X + LW + 20, 1246, VERDE)
    # G → J
    G.percorso(dr, [lato('G', 's'), lato('J', 'n')], G.MUTED, True)
    etichetta(dr, 'R011 · rettifica di tipo annullamento ·\nannullamento per inefficacia (web app)',
              X + LW / 2 + 14, 1276, G.MUTED)

    G.legenda(dr, 60, 1490, [('grigio', 'nessun atto o abbandono'), ('blu', 'lavorazione'),
                             ('giallo', 'atto in ANSC, non formato'), ('verde', 'atto formato'),
                             ('viola', 'stati locali o successivi'), ('rosso', 'eccezione SIPO')])
    dr.text((60, 1530), 'Tratteggio: rami che non fanno parte del percorso ordinario. '
            'Verde: avanzamento; rosso: annullamento o eccezione.',
            font=G.fnt(G.F_ITA, 15), fill=G.MUTED)
    im.save(dest)
    return dest


if __name__ == '__main__':
    print('scritto:', disegna())
