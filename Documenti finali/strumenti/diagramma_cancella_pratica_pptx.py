# -*- coding: utf-8 -*-
"""Il diagramma della cancellazione di una pratica in POWERPOINT, modificabile dall'utente.

Stesso contenuto e stessa impaginazione di diagramma_cancella_pratica.py (PNG): le coordinate
sono quelle del PNG divise per PX (pixel per pollice). Forme e connettori sono nativi e i
connettori sono agganciati alle forme, quindi seguono i riquadri se l'utente li sposta.

Uscita: img/cancella_pratica.pptx

⚠️ NON RIESEGUIRE: dal 30/10/2026 il .pptx è stato ritoccato dall'utente in PowerPoint e
aggiornato dalla v3.56 (v3_56_cancellazione.py pptx). Rigenerarlo cancellerebbe quelle modifiche.
La figura nell'analisi è img/cancella_pratica/Diapositiva1.png (esportazione del .pptx).
"""
import os

from pptx import Presentation
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from diagramma_workflow_pptx import (INK, MUTED, ARROW, PAL, _punta, freccia, riquadro, rgb,
                                     testo)

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'img', 'cancella_pratica.pptx')

PX = 170.0                      # 1700 x 1900 px  →  10 x 11,18 pollici
W, H = 1700 / PX, 1900 / PX
CX = 700
DA_VERIFICARE = 'b03a48'


def i(v):
    return v / PX


def blocco(sl, x, y, w, h, colore, titolo, sotto, tratteggio=False, forma=MSO_SHAPE.ROUNDED_RECTANGLE):
    righe = [(titolo, 10.5, True, INK)]
    if sotto:
        righe.append((sotto, 8, False, MUTED))
    return riquadro(sl, i(x), i(y), i(w), i(h), colore, righe, forma=forma, tratteggio=tratteggio)


def rombo(sl, cx, cy, w, h, t):
    return riquadro(sl, i(cx - w / 2), i(cy - h / 2), i(w), i(h), 'giallo', [(t, 10, True, INK)],
                    forma=MSO_SHAPE.DIAMOND)


def etichetta(sl, x, y, t, w=120):
    testo(sl, i(x - w / 2), i(y), i(w), i(18), t, pt=8, col=ARROW, allinea=PP_ALIGN.CENTER)


def nota(sl, x, y, w, h, t):
    return riquadro(sl, i(x), i(y), i(w), i(h), 'giallo', [(t, 8, False, '5b4a1f')],
                    allinea=PP_ALIGN.LEFT)


def gomito(sl, a, ca, b, cb):
    c = sl.shapes.add_connector(MSO_CONNECTOR.ELBOW, 0, 0, 0, 0)
    c.begin_connect(a, ca)
    c.end_connect(b, cb)
    c.line.color.rgb = rgb(ARROW)
    c.line.width = Pt(1.25)
    _punta(c)
    return c


def genera(percorso=OUT):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])

    testo(sl, 0, i(18), W, i(34), "Cancellazione di una pratica da SIPO e riflessi su ANSC",
          pt=16, bold=True, col='1b3a5c', allinea=PP_ALIGN.CENTER)
    testo(sl, 0, i(62), W, i(22), "dalla ricerca alla conclusione in SIPO · R011 solo per atti "
          "non ancora firmati dall’USC", pt=9, col=MUTED, allinea=PP_ALIGN.CENTER, corsivo=True)

    BW = 440
    ricerca = blocco(sl, CX - BW / 2, 110, BW, 96, 'grigio', "Ricerca della pratica",
                     "SIPO, funzione di ricerca · nessuna chiamata ad ANSC")
    cancella = blocco(sl, CX - BW / 2, 256, BW, 96, 'blu', "Selezione e “CANCELLA PRATICA”",
                      "l’operatore seleziona la pratica da rimuovere")
    freccia(sl, ricerca, 2, cancella, 0)

    conferma = rombo(sl, CX, 477, 360, 150, "Conferma?")
    freccia(sl, cancella, 2, conferma, 0)
    nessuna = blocco(sl, 1130, 432, 330, 90, 'grigio', "Nessuna modifica", "si torna alla ricerca")
    freccia(sl, conferma, 3, nessuna, 1)
    etichetta(sl, 1000, 452, "ANNULLA")

    riga = rombo(sl, CX, 697, 470, 170, "Riga in ANSC_STATO_ATTO per l’atto?")
    freccia(sl, conferma, 2, riga, 0)
    etichetta(sl, 752, 566, "CONFERMA")
    canc_sipo = blocco(sl, 60, 637, 320, 120, 'verde', "Cancellazione in SIPO",
                       "procedure attuali · nulla da fare su ANSC")
    freccia(sl, riga, 1, canc_sipo, 3)
    etichetta(sl, 422, 672, "NO", 60)
    testo(sl, i(760), i(797), i(320), i(18), "per ID_ATTO_SIPO = ID_ATTO", pt=8, col=MUTED,
          corsivo=True)

    idansc = rombo(sl, CX, 942, 420, 160, "ID_ANSC valorizzato?")
    freccia(sl, riga, 2, idansc, 0)
    etichetta(sl, 724, 815, "SÌ", 40)
    annullato = blocco(sl, 60, 872, 320, 140, 'blu', "Stato dell’atto a “9 ANNULLATO”",
                       "solo su ANSC_STATO_ATTO · nessuna chiamata: l’atto in ANSC non esiste")
    freccia(sl, idansc, 1, annullato, 3)
    etichetta(sl, 435, 917, "NO", 60)

    r011 = blocco(sl, CX - BW / 2, 1092, BW, 110, 'viola', "R011 /evento/elimina",
                  "cancellazione logica in ANSC · richiede l’intero modello evento")
    freccia(sl, idansc, 2, r011, 0)
    etichetta(sl, 724, 1040, "SÌ", 40)
    nota(sl, 950, 1080, 440, 96, "Vincolo ANSC: R011 non cancella un atto già firmato dall’USC. "
         "Il testo non dice dove si controlli lo stato prima della chiamata [DA VERIFICARE].")

    esito = rombo(sl, CX, 1327, 360, 150, "Esito di R011?")
    freccia(sl, r011, 2, esito, 0)
    interrotta = blocco(sl, 1080, 1252, 400, 150, 'rosso', "Cancellazione interrotta",
                        "la pratica resta in SIPO e si mostra l’errore ANSC [DA VERIFICARE: il "
                        "testo dice solo «fare attenzione al ritorno»]", tratteggio=True)
    freccia(sl, esito, 3, interrotta, 1)
    etichetta(sl, 980, 1302, "ERRORE")

    aggiornato = blocco(sl, CX - BW / 2, 1452, BW, 96, 'blu', "Stato dell’atto aggiornato",
                        "su ANSC_STATO_ATTO, come dopo R011 [DA VERIFICARE: non descritto]",
                        tratteggio=True)
    freccia(sl, esito, 2, aggiornato, 0)
    etichetta(sl, 724, 1414, "OK", 40)

    conclusione = blocco(sl, CX - BW / 2, 1638, BW, 100, 'verde',
                         "Conclusione dell’operazione in SIPO",
                         "cancellazione della pratica secondo le procedure attuali")
    freccia(sl, aggiornato, 2, conclusione, 0)
    gomito(sl, annullato, 2, conclusione, 1)

    nota(sl, 80, 1768, 1540, 50, "Stato: nella decodifica ANSC_11 il codice 9 è CANCELLATO e "
         "ANNULLATO è il 3. Il testo chiede “9 ANNULLATO”: va deciso quale coppia ID_STATO/STATO "
         "registrare [DA VERIFICARE].")

    # legenda
    x = 80
    for colore, t in [('grigio', "SIPO, nessun effetto"), ('blu', "SIPO / ANSC_STATO_ATTO"),
                      ('viola', "chiamata ad ANSC"), ('verde', "esito"), ('rosso', "errore"),
                      ('giallo', "decisione o nota")]:
        riquadro(sl, i(x), i(1850), i(26), i(17), colore, [("", 6, False, INK)])
        testo(sl, i(x + 34), i(1849), i(10 * len(t) + 40), i(20), t, pt=8, col=MUTED)
        x += 34 + 10 * len(t) + 50

    prs.save(percorso)
    print(percorso)


if __name__ == '__main__':
    genera()
