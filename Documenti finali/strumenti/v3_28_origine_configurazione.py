# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.27 -> v3.28 (25/09/2026).

Verifica dei wireframe contro il modello dati: due schermate mostravano la colonna
dell'origine su tabelle che non la portano più.

  · ANSC_CFG_UC non ha mai avuto COD_ORIGINE; ANSC_CFG_CAMPO l'ha persa con le modifiche
    manuali alla v3.25. La conservano ANSC_CFG_SEZIONE, ALLEGATI_USECASE, ANSC_CFG_FORMULA.
  · ⚠️ Non è un difetto dei disegni ma una conseguenza sul meccanismo di reimportazione, che
    sulla tabella più grande — i campi — non ha più il dato su cui poggia: OP-65.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_28_origine_configurazione.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.27.docx')
DST = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.28.docx')
IMG = os.path.join(BASE, 'strumenti', 'img')

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
        for nome, val in (('Data consegna', '25/09/2026'), ('Versione', '3.28')):
            try:
                D.riscrivi_cella(riga_con(t, nome).cells[1], val)
            except SystemExit:
                pass

D.storia(doc, '25/09/2026', '3.28', 'Back-office · Open Point · Wireframe',
         'Verificati i wireframe contro il modello dati. Due schermate mostravano la colonna '
         'dell’origine della riga su tabelle che non la portano: la configurazione dei casi '
         'd’uso, che non l’ha mai avuta, e quella dei campi, che l’ha persa. I disegni sono '
         'stati rifatti sulle colonne effettive e la regola di lavoro è stata riscritta di '
         'conseguenza; la conseguenza sul meccanismo di reimportazione è registrata come punto '
         'aperto.')

# 1. la regola che vale oggi, al posto di quella che valeva per tutte le schermate
D.sostituisci(doc,
              'In tutte le schermate della configurazione ogni riga mostra la propria origine '
              '— proposta, confermata, modificata, inserita — e il filtro predefinito è «non '
              'ancora esaminate».',
              'Nelle schermate delle sezioni, degli allegati e delle formule ogni riga mostra '
              'la propria origine — proposta, confermata, modificata, inserita — e il filtro '
              'predefinito è «non ancora esaminate». ⚠️ Non così per i casi d’uso e per i '
              'campi, che nel modello attuale non portano quel contrassegno: là il lavoro si '
              'ordina per sezione e per assenza della corrispondenza SIPO, che è il criterio '
              'disponibile (OP-65).', attese=1, etichetta='regola dell’origine', fatti=fatti)

# 2. la conseguenza, detta dove si descrive la reimportazione
for p in doc.paragraphs:
    if p.text.strip().startswith('La conseguenza pratica è che il lavoro di configurazione'):
        D.para(doc, p._p,
               '⚠️ Su un punto il meccanismo appena descritto non si regge da sé. La '
               'reimportazione riscrive le sole righe che nessuno ha ancora esaminato, e per '
               'saperlo legge il contrassegno di origine: ma nel modello attuale quel '
               'contrassegno sta sulle sezioni, sugli allegati e sulle formule, non sui campi '
               'né sui casi d’uso. Sulla tabella più grande — oltre sessantamila righe a '
               'regime — una reimportazione non sa distinguere ciò che un funzionario ha '
               'deciso da ciò che nessuno ha guardato, e il lavoro umano è esattamente ciò che '
               'non deve essere sovrascritto. Il punto è registrato come aperto: o il '
               'contrassegno torna sui campi, o la reimportazione si governa in un altro modo '
               'dichiarato.')
        fatti.append('conseguenza sulla reimportazione dichiarata')
        break

t = D.trova_tabella(doc, '#', 'tema', 'questione')
D.clona_riga(t, ('OP-65', 'Contrassegno di origine sulle righe di configurazione',
                 'ANSC_CFG_CAMPO ha perso COD_ORIGINE e ANSC_CFG_UC non l’ha mai avuta, '
                 'mentre sezioni, allegati e formule la conservano. È il dato su cui poggia la '
                 'regola per cui la reimportazione riscrive soltanto le righe non ancora '
                 'esaminate: senza, sulla tabella dei campi la regola non è applicabile. Va '
                 'deciso se ripristinarlo o se governare la reimportazione in altro modo.',
                 'Aperto', 'Analisi / Cliente', 'Alta'))
fatti.append('OP-65 aperto')

# 3. i disegni rifatti sulle colonne effettive
for inizio, png in (('Wireframe — Configurazione (Casi d’uso)', 'bo_config_uc.png'),
                    ('Wireframe — Configurazione (Sezioni, campi', 'bo_config_campi.png'),
                    ('Wireframe — Audit e log', 'bo_audit.png')):
    D.sostituisci_immagine(doc, inizio, os.path.join(IMG, png))
fatti.append('tre wireframe riallineati alle colonne del modello')

doc.save(DST)

import zipfile   # noqa: E402
ncom = zipfile.ZipFile(DST).read('word/comments.xml').decode().count('<w:comment ')
assert ncom == 23, f'commenti persi: {ncom}'
print('\n'.join(' · ' + f for f in fatti))
print('commenti:', ncom, '· capitoli/tabelle/immagini:', D.riepilogo(DST))
print('scritto:', os.path.relpath(DST, BASE))
