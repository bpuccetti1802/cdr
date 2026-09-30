# -*- coding: utf-8 -*-
"""v3.16 — il back-office segue la configurazione semplificata.

Tre disallineamenti da correggere:
⚠️ resta una schermata «Regole di controllo e di generazione» per una tabella che il modello
   semplificato non ha più — la logica è rientrata nelle colonne di ANSC_CFG_CAMPO;
⚠️ manca la funzione che il documento nomina in tre punti e il commento [47] chiede
   esplicitamente: l'importazione dei fogli Excel, che oggi è descritta come un'operazione
   senza una schermata che la ospiti;
⚠️ la schermata dei casi d'uso non nomina la regola di scelta, che è il campo su cui il
   funzionario lavora davvero.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.16.docx')

IMPORTAZIONE = [
    'Importazione della configurazione',
    'Caricamento dei fogli Excel da cui la configurazione si precompila: un foglio per caso '
    'd’uso con i campi, gli allegati e le formule, più il foglio dei casi d’uso con Modello, '
    'tipo atto e maschera. È la funzione che il documento nomina in più punti e che qui trova '
    'la propria sede.',
    'Carica il foglio, mostra l’anteprima di ciò che verrebbe scritto — righe nuove, righe '
    'modificate, righe che l’operatore aveva già esaminato e che l’importazione non tocca — '
    'conferma o annulla, consulta lo storico dei caricamenti con esito e conteggi.',
    'Admin',
]

REGOLE_ERA = 'Regole di controllo e di generazione'


def applica(doc):
    fatti = []
    t = D.trova_tabella(doc, 'Schermata', 'Scopo', 'Azioni principali', 'Ruolo')

    for riga in t.rows:
        nome = riga.cells[0].text.strip()

        if nome.startswith(REGOLA_ERA if False else REGOLE_ERA):
            if D.ha_commenti(riga._tr):
                fatti.append('⚠️ riga «Regole» commentata: lasciata, va decisa dall’autore')
                continue
            # la sostituisco invece di toglierla: la funzione serve ancora, cambia oggetto
            for j, v in enumerate(IMPORTAZIONE):
                D.riscrivi_cella(riga.cells[j], v)
            fatti.append('schermata «Regole …» → «Importazione della configurazione» '
                         '(la tabella delle regole non esiste più nel modello semplificato)')

        if nome.startswith('Configurazione — Casi d’uso'):
            D.riscrivi_cella(riga.cells[1],
                             'ANSC_CFG_UC: una riga per UC adottato, con il Modello di atto a '
                             'cui si applica, il tipo atto, la maschera, la priorità fra gli UC '
                             'dello stesso Modello e la regola di scelta che lo seleziona.')
            D.riscrivi_cella(riga.cells[2],
                             'Nuovo UC, ordina la priorità, scrive e prova la regola di scelta '
                             'su un atto reale, apre campi, allegati e formule dell’UC.')
            fatti.append('schermata «Casi d’uso»: nominata la regola di scelta')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
