# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.41 → v3.42 (15/10/2026).

Nel capitolo «Il processo di gestione dei dati ANSC in SIPO», dopo la tabella del workflow, il
diagramma funzionale con i cambi di stato (richiesta dell'utente). La figura è disegnata in
PowerPoint con forme native (strumenti/img/workflow_ansc_sipo.pptx, generato da
diagramma_workflow_pptx.py) perché l'utente la possa modificare; il PNG inserito è l'esportazione
di PowerPoint (PDF → Quick Look), quindi coincide con il file modificabile.

⚠️ Se l'utente modifica il .pptx, il PNG nel .docx NON si aggiorna da solo: va riesportato e
sostituito (D.sostituisci_immagine con l'inizio della didascalia).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagramma_workflow_pptx.py
    (esportazione in PDF da PowerPoint, poi qlmanage -t -s 2400 → img/workflow_ansc_sipo.png)
    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_42_workflow.py
"""
import os
import shutil
import subprocess
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.41.docx')
DST = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.42.docx')
PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'workflow_ansc_sipo.png')

INTRO = ('La figura che segue riporta la tabella in forma di diagramma: in colonna le pagine di '
         'SIPO, il servizio che ciascuna chiama, lo stato dell’atto in ANSC secondo la decodifica '
         'ANSC_11 e lo stato in SIPO. Fino alla validazione in ANSC non esiste alcun atto; la '
         'validazione lo crea nello stato CONFERMATO e ogni firma lo fa avanzare, mentre in SIPO '
         'l’atto resta in lavorazione fino al passo «Definisci». Se la validazione fallisce '
         'l’operatore torna alle pagine dei dati; se non ci sono firmatari la pagina delle firme '
         'si salta. La firma dell’USC è il punto di non ritorno.')
DIDASCALIA = ('Il flusso di gestione dell’atto: pagine di SIPO, servizi chiamati e cambi di stato in '
              'ANSC e in SIPO. Il diagramma è modificabile nel file '
              'strumenti/img/workflow_ansc_sipo.pptx.')

STORIA = ('15/10/2026', '3.42', 'Il processo di gestione dei dati ANSC in SIPO',
          'Aggiunto il diagramma funzionale del workflow, ricavato dalla tabella dei passaggi e '
          'dalla tabella degli stati: le pagine di SIPO, i servizi chiamati, i cambi di stato '
          'dell’atto in ANSC e in SIPO, il ritorno sull’esito negativo della validazione, il salto '
          'delle firme senza firmatari, il punto di non ritorno e gli stati successivi alla '
          'formazione. Il diagramma è disegnato in PowerPoint, perché resti modificabile.')


def commenti(p):
    return int(subprocess.run(
        ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                       "grep -o '<w:comment ' | wc -l" % repr(p)],
        capture_output=True, text=True).stdout.strip() or 0)


def main():
    if os.path.exists(DST):
        raise SystemExit('esiste già: ' + DST)
    shutil.copy(SRC, DST)
    prima = commenti(DST)
    d = docx.Document(DST)

    t = D.trova_tabella(d, 'Passaggio', 'Immagine di riferimento', 'STATO ANSC', 'Stato SIPO')
    dopo = t._tbl.getnext()
    D.para(d, dopo, INTRO)
    D.immagine(d, dopo, PNG, 6.0, DIDASCALIA)

    D.storia(d, *STORIA)
    fatti = D.frontespizio(d, '3.42', data='15/10/2026')
    for s in d.sections:
        for tt in s.header.tables:
            for rr in tt.rows:
                for c in rr.cells:
                    if c.text.strip() == 'Versione 3.41':
                        D.riscrivi_cella(c, 'Versione 3.42')
                        fatti.append('testata: Versione 3.42')
    d.save(DST)
    dopo_c = commenti(DST)
    for f in fatti:
        print('  ' + f)
    print(f'  commenti di Word conservati: {prima} → {dopo_c}')
    if dopo_c != prima:
        raise SystemExit('commenti persi')
    print('  scritto', DST, D.riepilogo(DST))


if __name__ == '__main__':
    main()
