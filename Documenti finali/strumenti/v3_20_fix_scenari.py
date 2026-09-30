# -*- coding: utf-8 -*-
"""La tabella degli scenari aveva due intestazioni: il foglio ne porta una di titolo e una vera.

Si tiene una riga sola, che nomina il campo come lo nomina la sorgente.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D  # noqa: E402
from v3_20_notifiche import DOC  # noqa: E402

TESTA = ['Genere (idGenereNotifiche, ANSC_101)', 'Canale (idcanalenotifica)',
         'Evento (flageventocartaceo)', 'Scenario', 'Ambito (cd_azione_canale)']

doc = docx.Document(DOC)
fatti = 0
for t in doc.tables:
    if [c.text.strip() for c in t.rows[0].cells][:2] == ['Genere', 'Canale']:
        t.rows[1]._tr.getparent().remove(t.rows[1]._tr)
        for cella, testo in zip(t.rows[0].cells, TESTA):
            D.riscrivi_cella(cella, testo)
        fatti += 1
assert fatti == 1, fatti
doc.save(DOC)
print('intestazione degli scenari sistemata; righe:',
      len(D.trova_tabella(doc, 'scenario', 'ambito (cd_azione_canale)').rows))
