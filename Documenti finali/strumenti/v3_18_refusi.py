# -*- coding: utf-8 -*-
"""v3.18 — refusi, nomi superati e la riformulazione di RF-16.

⚠️ Le occorrenze nella «Storia del Documento» NON si toccano: quella tabella cita per
mestiere le formulazioni delle versioni precedenti, ed è la sola parte del documento in cui un
nome superato è al suo posto.

⚠️ RF-16 va precisato perché, nella formulazione attuale, afferma qualcosa che il mapping
smentisce: il modello evento chiede l'identificativo del soggetto in 92 blocchi distinti —
madre, padre, dichiarante, interprete, coniuge, ufficiale — e in nessuno di essi lo dichiara
obbligatorio. Ciò che il requisito vuole dire è un impegno del Comune, non una proprietà del
modello: si valorizza per gli intestatari e non per gli altri.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.18.docx')

REFUSI = [
    ('Elenco tabelle decodica ANSC', 'Elenco delle tabelle di decodifica ANSC', 1, 'decodica'),
    ('ANAS_CFG_CAMPO', 'ANSC_CFG_CAMPO', 1, 'ANAS_CFG_CAMPO'),
    ('ANAS_CGF_UC', 'ANSC_CFG_UC', 1, 'ANAS_CGF_UC'),
    ('dovranno essere consuntabili', 'dovranno essere consultabili', 1, 'consuntabili'),
    ('del 6/9/26 , nella qual', 'del 6/9/26, nella qual', 1, 'spazio prima della virgola'),
]

SUPERATI = [
    ('ANSC_CFG_UC con le sue condizioni di applicabilità, ANSC_CFG_CAMPO, '
     'ANSC_CFG_ALLEGATO, ANSC_CFG_FORMULA e ANSC_CFG_REGOLA per i controlli e le generazioni',
     'ANSC_CFG_UC con la sua regola di scelta, ANSC_CFG_CAMPO, ANSC_CFG_ALLEGATO e '
     'ANSC_CFG_FORMULA', 1, 'elenco delle tabelle nella baseline'),
    ('ANSC_CFG_UC e ANSC_CFG_REGOLA portano una colonna di versione',
     'ANSC_CFG_UC e ANSC_CFG_CAMPO portano una colonna di versione', 1,
     'i semi del versionamento'),
    ('Famiglia ANSC_REGOLA_*', 'ANSC_CFG_UC — la regola di scelta', None,
     'tabella degli oggetti dello schema'),
    ('ANSC_CFG_REGOLA e ANSC_CFG_REGOLA_CONDIZIONE: l’intestazione della regola con la sua '
     'specie, il Modello di ambito, l’esito e la priorità, e le condizioni in forma '
     'campo-operatore-valore.',
     'La regola che sceglie l’UC risiede in ANSC_CFG_UC.REGOLA_DI_SCELTA: è uno script '
     'valutato sui dati che SIPO ha già registrato, e non una tabella di condizioni.', None,
     'nota della tabella degli oggetti'),
]

RF16 = ('Gli intestatari dell’atto — i soggetti a cui l’atto si riferisce — devono essere '
        'valorizzati con il proprio identificativo nazionale (ANSC o ANPR), recuperato con la '
        'consultazione R005. ⚠️ Per gli altri soggetti del modello evento (madre, padre, '
        'dichiarante, interprete, coniuge, ufficiale) l’identificativo non è valorizzato dal '
        'Comune: il modello lo prevede in 92 blocchi distinti ma non lo dichiara obbligatorio '
        'in nessuno.')


def applica(doc):
    fatti = []
    for vecchio, nuovo, attese, etichetta in REFUSI + SUPERATI:
        D.sostituisci(doc, vecchio, nuovo, attese=attese, etichetta=etichetta, fatti=fatti)

    # RF-16: la riformulazione
    t = D.trova_tabella(doc, 'ID', 'Requisito', 'Nota')
    for r in t.rows:
        if r.cells[0].text.strip() == 'RF-16':
            D.riscrivi_cella(r.cells[1], RF16)
            fatti.append('RF-16 riformulato')
    # la riga vuota in coda
    for i in range(len(t.rows) - 1, 0, -1):
        if not any(c.text.strip() for c in t.rows[i].cells):
            if D.ha_commenti(t.rows[i]._tr):
                continue
            t._tbl.remove(t.rows[i]._tr)
            fatti.append('rimossa la riga vuota in coda alla tabella dei requisiti')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
