# -*- coding: utf-8 -*-
"""La tabella ALLEGATO stava nel capitolo sbagliato.

Era descritta dentro «Il flusso in ingresso: notifiche, comunicazioni e solleciti», nel paragrafo
sullo store delle notifiche, per la sola ragione che lì c'era una sezione intitolata «Il modello
dati». Ma ALLEGATO non ha niente a che vedere con le notifiche: registra i documenti di un atto,
è una tabella operativa, e chi la cerca la cerca dove stanno le altre operative.

Si sposta in «Adeguamenti database» → «Struttura dettagliata delle tabelle operative», in coda
alle tre che già ci sono, e si aggiunge la riga che mancava nell'elenco d'apertura del capitolo.

⚠️ Si spostano gli ELEMENTI XML, non il testo: così le eventuali ancore di commento viaggiano
con i paragrafi invece di essere distrutte e ricreate.
"""
import os
import sys

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from v3_21_allineamento import DEST   # noqa: E402

INIZIO = 'ALLEGATO — i documenti allegati all’atto.'
FINE = 'Struttura dettagliata delle tabelle di configurazione'
CODA = 'La raccomandazione è quindi di prevedere fin dall’inizio'

RIGA_ELENCO = ('ALLEGATO',
               'Documenti allegati a un atto, fino al deposito in ANSC.',
               'Ereditata dal sistema Side del Comune di Milano con i nomi di origine. ⚠️ Non si '
               'sovrappone ad ANSC_CFG_ALLEGATO: questa registra i documenti di un atto, quella '
               'dichiara quali documenti un UC richiede.')

NOTA = ('⚠️ Alle tre tabelle native si aggiunge ALLEGATO, ereditata dal sistema Side del Comune '
        'di Milano e adottata con i nomi di origine: la sua grammatica dei prefissi — ty_, ds_, '
        'nm_, oj_, cd_, fg_, ts_, dt_, nr_ — convive quindi con quella dello standard [R5] '
        'dentro lo stesso schema. È una conseguenza voluta della scelta di ereditare invece di '
        'riscrivere, e va conosciuta leggendo il DDL.')


def blocco(doc, dal_titolo, fino_al_titolo):
    """Gli elementi dal heading indicato fino a quello di arrivo, escluso."""
    corpo = list(doc.element.body.iterchildren())
    inizio = fine = None
    for i, ch in enumerate(corpo):
        if not ch.tag.endswith('}p'):
            continue
        t = Paragraph(ch, doc).text.strip()
        if inizio is None and t.startswith(dal_titolo):
            inizio = i
        elif inizio is not None and t.startswith(fino_al_titolo):
            fine = i
            break
    if inizio is None or fine is None:
        raise SystemExit('blocco non individuato')
    return corpo[inizio:fine]


def main():
    doc = docx.Document(DEST)

    # ── 1. il blocco da spostare: dal titolo fino alla raccomandazione sull'archivio a oggetti
    corpo = list(doc.element.body.iterchildren())
    inizio = next(i for i, ch in enumerate(corpo)
                  if ch.tag.endswith('}p') and Paragraph(ch, doc).text.strip().startswith(INIZIO))
    fine = next(i for i, ch in enumerate(corpo)
                if i > inizio and ch.tag.endswith('}p')
                and Paragraph(ch, doc).text.strip().startswith(CODA))
    elementi = corpo[inizio:fine + 1]
    assert any(e.tag.endswith('}tbl') for e in elementi), 'la tabella ALLEGATO non è nel blocco'

    # ── 2. la destinazione: prima della sezione sulle tabelle di configurazione
    ancora = next(ch for ch in doc.element.body.iterchildren()
                  if ch.tag.endswith('}p')
                  and Paragraph(ch, doc).style.name == 'Heading 2'
                  and Paragraph(ch, doc).text.strip().startswith(FINE))
    for el in elementi:
        el.getparent().remove(el)
        ancora.addprevious(el)

    # ── 3. la nota sulla convivenza delle due nomenclature, in testa alla sezione operative
    testa = next(ch for ch in doc.element.body.iterchildren()
                 if ch.tag.endswith('}p')
                 and Paragraph(ch, doc).text.strip().startswith('Le tabelle seguono le convenzioni'))
    p = D.para(doc, testa, NOTA)
    testa.addnext(p._p)

    # ── 4. la riga che mancava nell'elenco d'apertura del capitolo
    t = D.trova_tabella(doc, 'oggetto', 'ruolo', 'note principali')
    assert t is not None, 'elenco delle tabelle non trovato'
    rif = next(r for r in t.rows[1:] if r.cells[0].text.strip() == 'ANSC_LOG_AUDIT')
    import copy
    tr = copy.deepcopy(rif._tr)
    rif._tr.addnext(tr)
    from docx.table import _Row
    for cella, val in zip(_Row(tr, t).cells, RIGA_ELENCO):
        for pp in cella.paragraphs[1:]:
            pp._p.getparent().remove(pp._p)
        D.riscrivi_cella(cella, val)

    doc.save(DEST)
    print('spostati', len(elementi), 'elementi ·',
          sum(1 for e in elementi if e.tag.endswith('}tbl')), 'tabella')


if __name__ == '__main__':
    main()
