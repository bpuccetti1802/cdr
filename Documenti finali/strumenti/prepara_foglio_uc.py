# -*- coding: utf-8 -*-
"""Prepara il foglio di lavoro di un UC: la forma compilata a mano, già istruita.

È il gemello di `completa_uc.py`, per il caso opposto: là si completava un foglio esistente,
qui se ne crea uno dove non c'è nulla. La forma è quella di `Dic_Nasc_001.xlsx` — stesse
dodici colonne, foglio intitolato all'ID usecase — perché è il foglio che si compila a mano
e cambiare forma a metà lavoro costa più di quanto renda.

Che cosa arriva già scritto e che cosa no:
  · la struttura — sezione, binding, obbligatorietà — dal mapping ufficiale dell'UC;
  · l'esito dell'obbligatorietà, calcolato con la regola che governa la condizione;
  · la colonna SIPO, DOVE il codice sa dirla, in giallo e con la sua evidenza `file:riga`;
  · nulla dove nessuno sa: la cella resta vuota, in rosso, ed è il lavoro.

⚠️ Una proposta in giallo non è un rilievo: sul banco di prova di Dic_Nasc_001 il ponte
concorda con il compilatore 36 volte su 41, e le 5 divergenze gli danno torto tutte. La
colonna «Verificato» esiste per questo — si spunta quando l'occhio umano è passato.

    /usr/bin/python3 "Documenti finali/strumenti/prepara_foglio_uc.py" [UC] [famiglia] [area]
"""
import collections
import csv
import os
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ponte_ansc_sipo as PT   # noqa: E402
import sipo_dizionario as SD   # noqa: E402
import uc_famiglia as UF       # noqa: E402
from completa_uc import esito_obbligatorieta   # noqa: E402
from uc_workbook import id_usecase, specifica_di_nascita   # noqa: E402

BASE = UF.BASE
CARTELLA = UF.CARTELLA
BLU = UF.BLU
GIALLO = UF.GIALLO
ROSSO = UF.ROSSO
VERDE = UF.VERDE
VIOLA = PatternFill('solid', fgColor='EDE4F5')
GRIGIO = UF.GRIGIO
BORDO = Border(*[Side(style='thin', color='BFBFBF')] * 4)

COLONNE = [
    ('UseCase', 11), ('Sezione FE ANSC', 22), ('Binding Object', 30),
    ('Binding Field', 26), ('Dato obbligatorio SI/NO', 10),
    ('Tabella/Campo SIPO', 36), ('Regole di transcodifica', 44),
    ('Condizioni particolari/Logiche di business', 44),
    ("Condizioni obbligatorieta' ANSC", 38), ('Ordinamento', 10), ('Operativo', 10),
    ('Default', 10),
    # ---- colonne di servizio, non presenti nel foglio originale
    ("Obbligatorio per l'UC", 12), ('Come è stato deciso', 30),
    ('Origine della colonna SIPO', 24), ('Verificato', 10), ('Evidenza', 50),
]


def prepara(uc='Morte_001', famiglia='morte', area='decessi', altra_famiglia='Dic_Nasc_001'):
    ids = id_usecase()
    id_uc = ids.get(uc, uc)
    ponte = PT.Ponte(area, ent=SD.entita(('common', 'back-end')))
    mano_altra = UF.lavoro_a_mano(altra_famiglia) if altra_famiglia else {}

    f = os.path.join(BASE, 'ansc', 'docs', 'Mapping_casi_uso', famiglia, uc + '.csv')
    with open(f, encoding='utf-8-sig') as fh:
        mapping = [r for r in csv.DictReader(fh) if (r.get('Sezione') or '').strip() != 'Sezione']

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = str(id_uc)
    for j, (titolo, largh) in enumerate(COLONNE, 1):
        c = ws.cell(row=1, column=j, value=titolo)
        c.font = Font(bold=True, color='FFFFFF', size=9)
        c.fill = BLU
        c.alignment = Alignment(vertical='center', wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = largh
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = 'F2'

    ordine = collections.Counter()
    conta = collections.Counter()
    r = 2
    for m in mapping:
        bo = (m.get('Binding Object') or '').strip()
        bf = (m.get('Binding Field') or '').strip()
        k = f'{bo}.{bf}'.strip('.')
        esito, come = esito_obbligatorieta(m.get('Obbligatorio'),
                                           m.get("Condizioni obbligatorieta'"))
        sipo = origine = evidenza = nota_altrui = ''
        if not k:
            origine = ''                       # Formula e Allegati non hanno binding
        else:
            p = re.sub(r'^evento\.?', '', k).strip('.')
            e = ponte.risolvi(p)
            d = ponte.dettaglio(e['percorso_sipo']) if e['percorso_sipo'] else None
            dest = (d or {}).get('destinazione') or {}
            # ⚠️ precedenza: il lavoro umano di un'altra famiglia batte la proposta
            # automatica. Su `numeroatto` il compilatore ha scelto ATTO.NUM_COMUNALE_ANSC e
            # il codice propone ATTO.NUMERO_ATTO: sono due colonne diverse, e chi ha deciso
            # sapeva quale delle due ANSC vuole.
            altrui = mano_altra.get(k, ('', '', ''))
            if altrui[0] and UF.ben_formata(altrui[0]) \
                    and not specifica_di_nascita(altrui[0]):
                sipo = UF.normalizza(altrui[0])
                origine = 'suggerita da altra famiglia'
                evidenza = f'{altra_famiglia}.xlsx — verificare che valga per questo evento'
            elif dest.get('colonna'):
                sipo = UF.normalizza(f"{dest.get('tabella', '')}.{dest['colonna']}")
                origine, evidenza = UF.PROPOSTA, dest.get('evidenza', '')
            elif altrui[0] and not UF.ben_formata(altrui[0]):
                # non è una colonna ma una nota: si riporta come tale e la cella resta da fare
                nota_altrui = (f'Dal foglio di {altra_famiglia}: {altrui[0]}')
                origine = UF.SCOPERTO
                evidenza = 'annotazione propagata, non una colonna'
            elif e['grado'] == 'soggetto assente in SIPO':
                origine = UF.ASSENTE
                evidenza = e['nota_soggetto']
            else:
                origine = UF.SCOPERTO
                evidenza = e['grado']
        conta[origine or '(senza binding)'] += 1
        ordine[bo] += 1
        valori = [id_uc, m.get('Sezione', ''), bo, bf or m.get('Campo', ''),
                  m.get('Obbligatorio', ''), sipo, '', nota_altrui,
                  m.get("Condizioni obbligatorieta'", ''), ordine[bo], '', '',
                  esito, come, origine, '', evidenza]
        for j, v in enumerate(valori, 1):
            c = ws.cell(row=r, column=j, value=v)
            c.alignment = Alignment(vertical='top', wrap_text=j in (7, 8, 9, 14, 17))
            c.border = BORDO
            if j == 6:                      # la colonna che si compila
                c.fill = {UF.PROPOSTA: GIALLO, 'suggerita da altra famiglia': VIOLA,
                          UF.ASSENTE: GRIGIO, UF.SCOPERTO: ROSSO}.get(origine, GRIGIO)
            elif j == 13:
                c.fill = {'SI': VERDE, 'CONDIZIONATO': GIALLO}.get(esito, GRIGIO)
        r += 1
    ws.auto_filter.ref = f'A1:{get_column_letter(len(COLONNE))}{r - 1}'
    return wb, ws, conta, len(mapping), id_uc


def _istruzioni(wb, uc, conta, n, id_uc):
    ws = wb.create_sheet('Come si compila', 0)
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 106
    voci = [
        (f'Foglio di lavoro — {uc} (usecase {id_uc})',
         'Mappatura SIPO ↔ ANSC · Roma Capitale', True),
        ('Che cosa devi fare', None, True),
        ('  la colonna da compilare',
         '«Tabella/Campo SIPO», nella forma TABELLA.COLONNA. Dove il dato sta dentro un XML '
         '(SOGGETTO.DETTAGLIO_STATOCIVILE) si scrive la colonna e si spiega il percorso in '
         '«Regole di transcodifica», come nel foglio delle nascite.', False),
        ('  i colori dicono da dove viene', None, False),
        ('    giallo', 'proposta dal codice, con l’evidenza file:riga in fondo alla riga. '
                       '⚠️ Da confermare: sul banco di prova delle nascite il meccanismo '
                       'concorda con il compilatore 36 volte su 41, e nelle 5 divergenze ha '
                       'torto lui. Spunta «Verificato» quando l’hai controllata.', False),
        ('    viola', 'presa dal foglio delle nascite, dove il percorso ANSC è lo stesso e la '
                      'tabella non è specifica della nascita (SOGGETTO, ATTO). Va verificata '
                      'per l’evento morte.', False),
        ('    rosso', 'nessuno sa dirla: è il lavoro. Il campo esiste in SIPO, la colonna no.',
         False),
        ('    grigio', 'il blocco intero non ha corrispondente in SIPO (i comparenti, '
                       'l’unito civilmente, il soggetto intervenuto…). Non è un campo da '
                       'rilevare ma una parte di maschera da progettare: non compilarla, '
                       'semmai annotala.', False),
        ('  che cosa NON devi toccare',
         'Le colonne di servizio (le ultime cinque) si ricalcolano a ogni rigenerazione. Le '
         'prime nove sono la struttura del mapping ufficiale: se cambiano è perché ANSC ha '
         'pubblicato una revisione.', False),
        ('Che cosa succede dopo', None, True),
        ('  la propagazione',
         'Questo foglio è la sorgente del lavoro umano per la famiglia morte, come '
         'Dic_Nasc_001.xlsx lo è per le nascite. Rigenerando '
         '«strumenti/uc_workbook.py» ogni percorso che compili qui si propaga a TUTTI i 25 '
         'UC di morte in cui lo stesso percorso ANSC ricorre: si compila una volta.', False),
        ('  l’ordine conveniente',
         'Il foglio «Da compilare» di MAPPATURA_UC_Nascite-Morti_v0.1.xlsx ordina i percorsi '
         'per quante righe ciascuno sblocca. Partire da lì rende più che scorrere questo '
         'foglio dall’alto.', False),
        ('L’obbligatorietà', None, True),
        ('  come è stata decisa',
         'La colonna «Obbligatorio per l’UC» è calcolata: governa «Condizioni '
         'obbligatorieta’» — «obbligatoria» → SI, «opzionale» → NO, un’espressione → '
         'CONDIZIONATO — e la colonna «Dato obbligatorio SI/NO» del mapping vale solo dove '
         'la condizione tace. ⚠️ Le due colonne del mapping si contraddicono in un terzo '
         'delle righe del dominio; la semantica ufficiale non è pubblicata da ANSC e va '
         'chiesta a Sogei.', False),
        ('Questo UC in cifre', None, True),
        ('  righe', f'{n} righe dal mapping ufficiale di {uc}', False),
    ]
    for k, v in conta.most_common():
        voci.append((f'  {k}', f'{v} righe', False))
    for a, b, testa in voci:
        ws.append([a, b])
        c = ws.cell(row=ws.max_row, column=1)
        c.font = Font(bold=True, size=11 if testa else 9,
                      color='FFFFFF' if b is None else '000000')
        if b is None:
            c.fill = BLU
        ws.cell(row=ws.max_row, column=2).alignment = Alignment(wrap_text=True,
                                                                vertical='top')
    return ws


if __name__ == '__main__':
    uc = sys.argv[1] if len(sys.argv) > 1 else 'Morte_001'
    fam = sys.argv[2] if len(sys.argv) > 2 else 'morte'
    area = sys.argv[3] if len(sys.argv) > 3 else 'decessi'
    wb, ws, conta, n, id_uc = prepara(uc, fam, area)
    _istruzioni(wb, uc, conta, n, id_uc)
    uscita = os.path.join(CARTELLA, uc + '.xlsx')
    if os.path.exists(uscita):
        uscita = os.path.join(CARTELLA, uc + '_generato.xlsx')
        print('⚠️  il foglio esisteva già: scrivo accanto, non sopra')
    wb.save(uscita)
    print('scritto :', os.path.relpath(uscita, BASE))
    print('foglio  :', ws.title, '·', n, 'righe')
    for k, v in conta.most_common():
        print(f'   {k:30} {v:4}')
