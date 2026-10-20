# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.11 → v0.12 (20/10/2026).

Richiesta dell'utente: rendere grafico il flusso del sottocapitolo «Il login di un operatore
nelle applicazioni nuove» (diagramma di sequenza, non a caratteri). Figura nuova
`diagrammi_iam.sequenza_login()` → img/iam_sequenza_login.png, inserita in fondo al
sottocapitolo come Figura 7; le figure seguenti scalano di uno (7→8, 8→9).
Parte dalla v0.11 salvata dall'utente alle 09:14.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_12_iam_sequenza.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
import diagrammi_iam      # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
IMG = os.path.join(FIN, 'strumenti', 'img')
SRC = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.11.docx')
DST = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.12.docx')


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)

    # le didascalie seguenti scalano di uno, dalla più alta
    for k in (8, 7):
        pp = [p for p in d.paragraphs if p.text.startswith(f'Figura {k} —')]
        assert len(pp) == 1, k
        r = [r for r in pp[0].runs if f'Figura {k}' in r.text]
        if r:
            r[0].text = r[0].text.replace(f'Figura {k}', f'Figura {k + 1}', 1)
        else:
            D.testo_di(pp[0], pp[0].text.replace(f'Figura {k}', f'Figura {k + 1}', 1))

    png = os.path.join(IMG, diagrammi_iam.sequenza_login(IMG))
    prima = D.h(d, 2, 'Le chiamate verso i back-end')._p
    D.para(d, prima, 'La figura riporta il flusso passo per passo. I passi da 1 a 11 sono '
           'comuni; il frammento alternativo distingue l’utente non censito o disabilitato, '
           'che riceve un diniego esplicito, da quello attivo, che riceve il cookie e il menu.')
    D.immagine(d, prima, png, 6.3,
               'Figura 7 — Il login di un operatore nelle applicazioni nuove: chi parla con chi, '
               'e in quale ordine.')

    D.storia(d, '20/10/2026', '0.12', 'Scelte effettuate per il TO BE — Il login di un '
             'operatore nelle applicazioni nuove',
             'Aggiunto il diagramma di sequenza del login (Figura 7); rinumerate le figure '
             'seguenti.')
    for f in D.frontespizio(d, '0.12', 'ANALISI_Identita-Profilazione-IAM_v0.12'):
        print('  ·', f)
    d.save(DST)
    cap, tab, fig = D.riepilogo(DST)
    print(f'  capitoli {cap}, tabelle {tab}, immagini {fig}')
    print('  scritto', DST)


if __name__ == '__main__':
    main()
