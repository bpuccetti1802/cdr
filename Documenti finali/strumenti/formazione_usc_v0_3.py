"""Corso USC v0.3: dalla v0.2 con le immagini inserite a mano dall'utente (07/11/2026).

Mette in evidenza che l'atto firmato in ANSC non si corregge più entro le ore 24, come invece
avviene oggi. Solo sostituzioni di testo dentro i run: forme, immagini e formattazione restano.
Uso: python formazione_usc_v0_3.py   (dalla cartella Documenti finali)
"""
from pptx import Presentation

SRC = "FORMAZIONE_USC_Nuove-funzionalita-SIPO-ANSC_v0.2.pptx"
OUT = "FORMAZIONE_USC_Nuove-funzionalita-SIPO-ANSC_v0.3.pptx"

# (vecchio, nuovo, occorrenze attese)
SOSTITUZIONI = [
    ("Oggi un atto si corregge fino a fine giornata. Con ANSC, dopo la firma dell'ufficiale l'atto è formato: "
     "si interviene solo con rettifica o annotazione.",
     "Oggi un atto si corregge fino alle ore 24. Con ANSC, firmato dall'ufficiale, l'atto è formato e non "
     "cambia più: solo rettifica o annotazione.", 1),
    ("Firma = punto di non ritorno", "Niente più correzioni entro le 24", 1),
    ("Dopo la firma dell'ufficiale l'atto non si modifica più",
     "Firmato in ANSC, l'atto non si corregge più, neanche entro le ore 24", 2),
    ("Una correzione si fa sul foglio, entro la giornata", "Una correzione si fa entro le ore 24", 1),
    ("Fino a lì si può tornare ai dati; dopo, l'atto è formato.",
     "Dopo, l'atto non si corregge più, neanche entro le ore 24.", 1),
    ("Solo rettifica o annotazione", "Niente correzioni entro le 24: solo rettifica o annotazione", 1),
    # ritocchi della v0.2 persi nel salvataggio delle 11:34 (fatto da una copia aperta prima del ritocco)
    (" · codice motore Dic_Nasc_001 · per la morte i codici sono più corti (2101)", " · codice motore Dic_Nasc_001", 1),
    ("1515 · Modello 30 · Dichiarazione di nascita", "1515 · Modello 30 · Nascita", 1),
    # note per il docente
    ("Firma: oggi a Roma un atto si corregge fino a mezzanotte; con ANSC la finestra si chiude con la firma "
     "dell'ufficiale, dopo serve una rettifica.",
     "Firma: oggi a Roma un atto si corregge fino alle ore 24 del giorno in cui è formato; con ANSC la finestra "
     "si chiude con la firma dell'ufficiale e dopo serve una rettifica. È il cambiamento di prassi più importante: "
     "insistere sul controllo dell'anteprima prima di firmare.", 1),
]


def cornici(pres):
    for s in pres.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                yield sh.text_frame
            if sh.has_table:
                for r in sh.table.rows:
                    for c in r.cells:
                        yield c.text_frame
        if s.has_notes_slide and s.notes_slide.notes_text_frame is not None:
            yield s.notes_slide.notes_text_frame


pres = Presentation(SRC)
for vecchio, nuovo, attese in SOSTITUZIONI:
    n = 0
    for tf in cornici(pres):
        for p in tf.paragraphs:
            for r in p.runs:
                if vecchio in r.text:
                    r.text = r.text.replace(vecchio, nuovo)
                    n += 1
    if n != attese:
        raise SystemExit(f"attese {attese}, trovate {n}: {vecchio[:60]}")
    print(f"{n}  {vecchio[:60]}")
pres.save(OUT)
print("scritto", OUT)
