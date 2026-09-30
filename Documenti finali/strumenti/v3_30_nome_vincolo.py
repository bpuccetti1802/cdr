# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.29 -> v3.30 (25/09/2026).

Un solo intervento, trovato leggendo il DDL: il vincolo di VALORE_DOMINIO si chiamava
`valore_dominio_tipo_dominio_fk`, nome ereditato alla lettera dalla sorgente di Side, dove è
esso stesso un residuo — la tabella riferita si chiama dominio_decodifica, non tipo_dominio.

⚠️ Finché le tabelle del Comune non si chiamavano TIPO_LOGICHE_DI_SCELTA era un refuso
innocuo; ora il nome allude a una tabella che nello schema esiste davvero e che con quel
vincolo non ha nulla a che vedere. Un nome che mente è peggio di un nome brutto.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_30_nome_vincolo.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.29.docx')
DST = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.30.docx')

if os.path.exists(DST):
    os.remove(DST)
shutil.copy(SRC, DST)
doc = docx.Document(DST)
fatti = []


def riga_con(t, prima_cella):
    for r in t.rows:
        if r.cells[0].text.strip() == prima_cella:
            return r
    raise SystemExit('riga non trovata: ' + prima_cella)


for t in doc.tables:
    if t.rows[0].cells[0].text.strip().lower().startswith(('area organizzativa', 'progetto')):
        for nome, val in (('Data consegna', '25/09/2026'), ('Versione', '3.30')):
            try:
                D.riscrivi_cella(riga_con(t, nome).cells[1], val)
            except SystemExit:
                pass

D.storia(doc, '25/09/2026', '3.30', 'Gestione dei dizionari · Appendice A',
         'Corretto il nome della chiave esterna di VALORE_DOMINIO, che citava una tabella '
         '«tipo_dominio» inesistente: è un residuo della sorgente da cui la struttura è '
         'ereditata, innocuo finché nello schema non è comparsa una tabella dal nome simile, '
         'e fuorviante da quando c’è. Il vincolo riferiva già la tabella giusta: cambia il '
         'nome, non il comportamento.')

D.sostituisci(doc, '  CONSTRAINT valore_dominio_tipo_dominio_fk',
              '  CONSTRAINT valore_dominio_dominio_decodifica_fk', attese=1,
              etichetta='nome del vincolo', fatti=fatti)

# la ragione, dove si descrive la struttura ereditata
for p in doc.paragraphs:
    if p.text.strip().startswith('Un vincolo del modello di origine deve essere'):
        D.para(doc, p._p,
               '⚠️ Una nota sui nomi dei vincoli, che vale come avvertenza generale quando si '
               'adotta una struttura altrui. Nella sorgente la chiave esterna di '
               'valore_dominio si chiama valore_dominio_tipo_dominio_fk, ma la tabella che '
               'riferisce è dominio_decodifica: il nome cita una tabella che nemmeno lì '
               'esiste. Finché lo schema non aveva altro, era un refuso senza conseguenze; da '
               'quando il Comune ha una tabella TIPO_LOGICHE_DI_SCELTA, quel nome allude a un '
               'legame che non c’è e manda fuori strada chi legge il DDL prima del modello. '
               'È stato quindi riportato al nome della tabella riferita. Adottare i nomi di '
               'origine è una scelta di fedeltà alla fonte: non si estende ai nomi che la '
               'fonte stessa ha sbagliato.')
        fatti.append('nota sull’adozione dei nomi ereditati')
        break

doc.save(DST)

import zipfile   # noqa: E402
z = zipfile.ZipFile(DST)
xml = z.read('word/document.xml').decode()
ncom = z.read('word/comments.xml').decode().count('<w:comment ')
assert ncom == 23, f'commenti persi: {ncom}'
import re   # noqa: E402
resti = len(re.findall(r'tipo_dominio', xml, re.I))
print('  occorrenze residue di «tipo_dominio»:', resti, '(attesa: 1, nella nota che lo spiega)')
print('\n'.join(' · ' + f for f in fatti))
print('commenti:', ncom, '· capitoli/tabelle/immagini:', D.riepilogo(DST))
print('scritto:', os.path.relpath(DST, BASE))
