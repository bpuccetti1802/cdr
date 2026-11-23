# -*- coding: utf-8 -*-
"""Lo schema delle tabelle del parto plurimo, analisi delle nascite gemellari v0.6 (21/11/2026),
in PowerPoint modificabile: ANSC_SOGGETTO_ATTO con identificativo e UC dell'atto (copie dello
store), posizione e tipo di nascita del gemello e identificativi ANSC dei gemelli adiacenti
(decisione dell'utente, 21/11/2026).

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v0_6_pptx.py
    qlmanage -t -s 2400 -o img/gemellari img/gemellari/gem6_erd.pptx
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagrammi_gemellari_v0_4_pptx as G4      # noqa: E402

RIGHE_SA = [
    ('PK', 'ID_SOGGETTO_ATTO'),
    ('FK', 'ID_ATTO_SIPO  → ANSC_STATO_ATTO'),
    ('', 'ID_ANSC · ID_UC_ANSC  (copie dello store)'),
    ('', 'ID_NASCITA_SOGGETTO · ID_SOGGETTO'),
    ('UK', 'ID_ATTO_SIPO, COD_RUOLO'),
    ('', 'ID_ANSC_SOGGETTO'),
    ('', 'NUM_PROGRESSIVO_GEMELLO · ID_TIPO_NASCITA'),
    ('', 'ID_ANSC_GEMELLO_PREC · ID_ANSC_GEMELLO_SUCC'),
    ('', 'COD_ORIGINE · TS_ABBINAMENTO'),
]

if __name__ == '__main__':
    p = G4.erd(os.path.join(G4.DIR, 'gem6_erd.pptx'), righe_sa=RIGHE_SA, y_sa=5.75)
    print('scritto:', os.path.relpath(p, QUI))
