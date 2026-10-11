# -*- coding: utf-8 -*-
"""Le schermate del sistema Side del Comune di Milano usate nell'analisi ANSC (v3.36).

Le sorgenti sono due: le schermate in `SIDE/Grafica/` e le immagini incorporate nei
documenti di processo «CdMI SIDe MI_ANSC» in `Sorgenti Documentali/`. Si estraggono da lì
ogni volta, invece di copiarle a mano, perché sia chiaro da dove viene ciascuna figura.

⚠️ Le schermate riportano nella testata il NOME DELL'OPERATORE collegato (ambiente di
sviluppo di Milano). Non serve al documento ed è un dato personale di un terzo: si copre con
il colore della testata. Le coordinate sono per immagine; se una sorgente cambia, vanno
ricontrollate guardando il PNG prodotto.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/immagini_side.py
"""
import io
import os
import zipfile

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
SORG = os.path.join(BASE, 'Sorgenti Documentali')
GRAF = os.path.join(BASE, 'SIDE', 'Grafica')
# ⚠️ si cerca per prefisso: nel nome del file l'apostrofo è quello dritto, e scriverlo a mano
# in una stringa con l'apostrofo tipografico non lo trova (ci sono cascato)
ATTESTATO = next(f for f in os.listdir(SORG)
                 if f.startswith('CdMI SIDe MI_ANSC - Processo di gestione e firma')
                 and f.endswith('v1.1.docx'))

# (file di uscita, sorgente, ritaglio (sx, alto, dx, basso) o None, riquadro del nome)
FIGURE = [
    ('side_allegati_base.png',
     ('png', os.path.join(GRAF, 'Screenshot 2026-09-24 alle 11.13.46.png')),
     None, (800, 6, 924, 38)),
    ('side_allegati_libera.png',
     ('png', os.path.join(GRAF, 'Screenshot 2026-09-24 alle 11.23.31.png')),
     (0, 32, None, None), (1215, 40, 1420, 68)),          # via la barra del browser
    ('side_attestato.png',
     ('docx', os.path.join(SORG, ATTESTATO), 'image8.png'),
     None, (1295, 14, 1452, 46)),
]


def carica(sorgente):
    if sorgente[0] == 'png':
        return Image.open(sorgente[1]).convert('RGB')
    with zipfile.ZipFile(sorgente[1]) as z:
        return Image.open(io.BytesIO(z.read('word/media/' + sorgente[2]))).convert('RGB')


def main():
    os.makedirs(IMG, exist_ok=True)
    for nome, sorgente, ritaglio, nome_op in FIGURE:
        im = carica(sorgente)
        # il riquadro del nome si riferisce all'immagine originale: si copre prima del ritaglio
        x0, y0, x1, y1 = nome_op
        rosso = im.getpixel((x0 - 6, (y0 + y1) // 2))
        ImageDraw.Draw(im).rectangle(nome_op, fill=rosso)
        if ritaglio:
            sx, al, dx, ba = ritaglio
            im = im.crop((sx, al, dx or im.width, ba or im.height))
        im.save(os.path.join(IMG, nome))
        print('scritto:', nome, im.size)


if __name__ == '__main__':
    main()
