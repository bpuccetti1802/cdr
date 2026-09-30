# -*- coding: utf-8 -*-
"""v3.18 — via i due capitoli rimasti in doppio, salvando ciò che sta solo lì.

La riscrittura della v3.17 ha prodotto i capitoli nuovi senza rimuovere i vecchi: «Costruzione
del payload» (7) e «Mappatura del payload» (11) condividono 45 paragrafi su 50; i due
«Gestione dei dizionari ANSC» (8 e 12) ne condividono 29 su 31, e hanno lo stesso titolo
nell'indice.

⚠️ Non basta cancellare. Due cose stanno solo nei capitoli vecchi:
  · **sette paragrafi** che non esistono altrove — fra cui la sezione sugli impatti al
    front-end, che è verosimilmente il contenuto destinato al capitolo 9, oggi uno stub di due
    righe;
  · **quattro ancore di commento**. I commenti sono istruzioni dell'autore e il documento
    dichiara che devono sopravvivere alle versioni: poiché i paragrafi commentati esistono
    identici nei capitoli nuovi, le ancore si spostano lì prima dell'eliminazione.
"""
import os
import sys

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.18.docx')

# capitolo vecchio -> capitolo nuovo in cui cercare il paragrafo gemello
COPPIE = {11: 7, 12: 8}


def mappa_capitoli(doc):
    """Per ogni capitolo: gli elementi che lo compongono, in ordine."""
    fuori = {}
    cap = 0
    for ch in doc.element.body.iterchildren():
        if ch.tag.endswith('}p'):
            p = Paragraph(ch, doc)
            if p.style.name == 'Heading 1' and p.text.strip():
                cap += 1
                fuori[cap] = {'titolo': p.text.strip(), 'elementi': []}
        if cap:
            fuori[cap]['elementi'].append(ch)
    return fuori


def testo(ch, doc):
    return Paragraph(ch, doc).text.strip() if ch.tag.endswith('}p') else None


def applica(doc):
    fatti = []
    capitoli = mappa_capitoli(doc)

    # ---------------------------------------------- 1. le ancore dei commenti
    spostate = 0
    for vecchio, nuovo in COPPIE.items():
        gemelli = {}
        for ch in capitoli[nuovo]['elementi']:
            t = testo(ch, doc)
            if t:
                gemelli.setdefault(t, ch)
        for ch in capitoli[vecchio]['elementi']:
            if not ch.tag.endswith('}p') or not D.ha_commenti(ch):
                continue
            t = testo(ch, doc)
            dest = gemelli.get(t)
            assert dest is not None, f'paragrafo commentato senza gemello: {t[:70]}'
            ids = D.sposta_commenti(ch, dest)
            spostate += len(set(ids))
            fatti.append(f'commento {",".join(sorted(set(ids)))} spostato dal cap. {vecchio} '
                         f'al cap. {nuovo}: «{t[:54]}»')
    fatti.append(f'ancore di commento ricollocate: {spostate}')

    # ---------------------------------------------- 2. il contenuto che sta solo nei vecchi
    for vecchio, nuovo in COPPIE.items():
        testi_nuovi = {testo(ch, doc) for ch in capitoli[nuovo]['elementi']}
        unici = [ch for ch in capitoli[vecchio]['elementi'][1:]
                 if ch.tag.endswith('}p') and testo(ch, doc)
                 and testo(ch, doc) not in testi_nuovi]
        for ch in unici:
            fatti.append(f'   ⓘ solo nel cap. {vecchio}: «{testo(ch, doc)[:80]}»')
    return fatti, capitoli


def elimina(doc, numeri=(11, 12)):
    """Elimina i capitoli indicati. Le ancore dei commenti devono essere già state spostate.

    ⚠️ Il controllo non è formale: se un elemento da eliminare porta ancora un commento, si
    interrompe. Cancellare un'ancora significherebbe far sparire un'istruzione dell'autore.
    """
    capitoli = mappa_capitoli(doc)
    fuori = []
    for n in sorted(numeri, reverse=True):
        elementi = capitoli[n]['elementi']
        for ch in elementi:
            assert not D.ha_commenti(ch), f'elemento commentato nel cap. {n}: non si elimina'
        for ch in elementi:
            ch.getparent().remove(ch)
        fuori.append(f'eliminato il cap. {n} «{capitoli[n]["titolo"][:46]}» '
                     f'({len(elementi)} elementi)')
    return fuori


if __name__ == '__main__':
    doc = docx.Document(DOC)
    fatti, _ = applica(doc)
    fatti += elimina(doc)
    for f in fatti:
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
