# -*- coding: utf-8 -*-
"""Due o più UC affiancati: che cosa cambia davvero fra casi d'uso vicini.

`Dic_Nasc_001/002/003` sono lo stesso Modello del Comune (30) e la scelta fra loro dipende da
due flag che stanno sul soggetto, non sull'atto. Metterli a fianco serve a vedere che cosa la
determinazione dell'UC comporta di concreto: se cambiano le sezioni, l'obbligatorietà, gli
allegati o le formule. È il riscontro che rende verificabile una regola di determinazione.

⚠️ La riga si identifica con (sezione, binding object, binding field) e — dove il binding non
c'è, cioè Allegati e Formula — con il nome del campo, perché è così che il mapping li nomina.

    /usr/bin/python3 "Documenti finali/strumenti/confronto_uc.py" nascita Dic_Nasc_001 Dic_Nasc_002 …
"""
import collections
import csv
import os
import sys

import openpyxl
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uc_famiglia as UF                      # noqa: E402
from completa_uc import esito_obbligatorieta  # noqa: E402
from uc_workbook import id_usecase            # noqa: E402

BASE, CARTELLA = UF.BASE, UF.CARTELLA


def leggi(famiglia, uc):
    f = os.path.join(BASE, 'ansc', 'docs', 'Mapping_casi_uso', famiglia, uc + '.csv')
    with open(f, encoding='utf-8-sig') as fh:
        righe = [r for r in csv.DictReader(fh) if (r.get('Sezione') or '').strip() != 'Sezione']
    fuori = collections.OrderedDict()
    for r in righe:
        bo = (r.get('Binding Object') or '').strip()
        bf = (r.get('Binding Field') or '').strip()
        k = (r.get('Sezione', ''), bo, bf or r.get('Campo', ''))
        esito, _ = esito_obbligatorieta(r.get('Obbligatorio'),
                                        r.get("Condizioni obbligatorieta'"))
        fuori[k] = {'campo': r.get('Campo', ''), 'obbligatorio': r.get('Obbligatorio', ''),
                    'condizione': (r.get("Condizioni obbligatorieta'") or '').strip(),
                    'esito': esito}
    return fuori


def confronta(famiglia, ucs, sorgente='Dic_Nasc_001'):
    letti = {uc: leggi(famiglia, uc) for uc in ucs}
    mano = UF.lavoro_a_mano(sorgente) if sorgente else {}
    chiavi = collections.OrderedDict()
    for uc in ucs:
        for k in letti[uc]:
            chiavi.setdefault(k, None)

    righe = []
    for (sez, bo, bf) in chiavi:
        percorso = f'{bo}.{bf}'.strip('.') if bo else ''
        r = {'sezione': sez, 'percorso': percorso or f'[{sez}] {bf}',
             'campo': next(letti[uc][(sez, bo, bf)]['campo'] for uc in ucs
                           if (sez, bo, bf) in letti[uc]),
             'sipo': (mano.get(percorso) or ('', '', ''))[0]}
        esiti, cond, presenze = [], [], []
        for uc in ucs:
            v = letti[uc].get((sez, bo, bf))
            # ⚠️ si confrontano i valori GREZZI, non l'esito calcolato: fra Dic_Nasc_001 e
            # 003 l'unica differenza di tutto il caso d'uso sta nella colonna «Obbligatorio»
            # (luogoFiliazione: SI per il nato vivo, NO per il nato morto) mentre la
            # condizione dice «obbligatoria» in entrambi. Un esito che privilegi una delle
            # due colonne cancellerebbe la distinzione che il confronto deve mostrare.
            r[f'{uc}_obbl'] = v['obbligatorio'] if v else '— assente —'
            r[f'{uc}_esito'] = v['esito'] if v else '— assente —'
            r[f'{uc}_cond'] = v['condizione'] if v else ''
            esiti.append((r[f'{uc}_obbl'], r[f'{uc}_esito']))
            cond.append(r[f'{uc}_cond'])
            presenze.append(v is not None)
        diff = []
        if len(set(presenze)) > 1:
            diff.append('presenza')
        if len(set(esiti)) > 1:
            diff.append('obbligatorietà')
        if len(set(cond)) > 1:
            diff.append('condizione')
        r['differenza'] = ', '.join(diff)
        righe.append(r)
    return righe


def _foglio(wb, nome, colonne, righe, evidenzia=None):
    ws = wb.create_sheet(nome)
    for j, (_, largh, _) in enumerate(colonne, 1):
        ws.column_dimensions[get_column_letter(j)].width = largh
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = 'C2'
    testa = []
    for titolo, _, _ in colonne:
        c = WriteOnlyCell(ws, value=titolo)
        c.font = Font(bold=True, color='FFFFFF', size=9)
        c.fill = UF.BLU
        c.alignment = Alignment(vertical='center', wrap_text=True)
        testa.append(c)
    ws.append(testa)
    n = 1
    for r in righe:
        fill = evidenzia(r) if evidenzia else None
        celle = []
        for _, _, k in colonne:
            c = WriteOnlyCell(ws, value=r.get(k, ''))
            c.alignment = Alignment(vertical='top', wrap_text=k.endswith('_cond'))
            if fill and (k == 'differenza' or k.endswith('_obbl') or k.endswith('_cond')):
                c.fill = fill
            elif k.endswith('_esito'):
                c.fill = {'SI': UF.VERDE, 'CONDIZIONATO': UF.GIALLO,
                          '— assente —': UF.ROSSO}.get(r.get(k), UF.GRIGIO)
            celle.append(c)
        ws.append(celle)
        n += 1
    ws.auto_filter.ref = f'A1:{get_column_letter(len(colonne))}{n}'
    return ws


def colonne_per(ucs):
    col = [('Sezione', 22, 'sezione'), ('Percorso ANSC', 44, 'percorso'),
           ('Campo (mapping)', 30, 'campo'), ('Tabella/Campo SIPO', 32, 'sipo')]
    for uc in ucs:
        col.append((f'{uc}\n«Obbligatorio»', 12, f'{uc}_obbl'))
        col.append((f'{uc}\ncondizione', 32, f'{uc}_cond'))
        col.append((f'{uc}\nesito calcolato', 13, f'{uc}_esito'))
    col.append(('Che cosa cambia', 20, 'differenza'))
    return col


def _legenda(wb, famiglia, ucs, righe, ids):
    ws = wb.create_sheet('Come leggerlo', 0)
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 104
    diverse = [r for r in righe if r['differenza']]
    per_tipo = collections.Counter(r['differenza'] for r in diverse)
    per_sez = collections.Counter(r['sezione'] for r in diverse)
    voci = [
        ('Confronto fra casi d’uso vicini', ' · '.join(f'{u} ({ids.get(u, "?")})' for u in ucs),
         True),
        ('A che serve',
         'I casi d’uso confrontati appartengono allo stesso Modello di atto del Comune: la '
         'scelta fra loro la fanno i dati, non la maschera. Qui si vede che cosa comporta '
         'quella scelta — se cambiano le sezioni, l’obbligatorietà, gli allegati o le '
         'formule. È il riscontro che rende verificabile una regola di determinazione.', False),
        ('Da confrontare con la web app',
         'Il mapping dice che cosa ANSC accetta; la web app mostra come si comporta la '
         'maschera. Le righe evidenziate sono i punti in cui i tre casi divergono: sono '
         'quelle da osservare nella registrazione.', False),
        ('I fogli', None, True),
        ('  Differenze', f'Le sole {len(diverse)} righe in cui i casi d’uso non coincidono. '
                         f'È il foglio da guardare per primo.', False),
        ('  Confronto completo', f'Tutte le {len(righe)} righe, affiancate.', False),
        ('I colori della colonna «obbligatorio»', None, True),
        ('  verde', 'SI — il campo è richiesto in quel caso d’uso.', False),
        ('  giallo', 'CONDIZIONATO — richiesto se la condizione è vera. L’espressione è '
                     'accanto: ⚠️ nella grande maggioranza dei casi è la stessa per tutta la '
                     'sezione, cioè dichiara quando la SEZIONE serve, non il singolo campo.',
         False),
        ('  rosso', 'la riga non esiste affatto in quel caso d’uso.', False),
        ('  grigio', 'NO — non richiesto.', False),
        ('Che cosa cambia, in cifre', None, True),
    ]
    for k, v in per_tipo.most_common():
        voci.append((f'  {k}', f'{v} righe', False))
    voci.append(('  per sezione',
                 ' · '.join(f'{s}: {n}' for s, n in per_sez.most_common()), False))
    for a, b, testa in voci:
        c1, c2 = WriteOnlyCell(ws, value=a), WriteOnlyCell(ws, value=b)
        c1.font = Font(bold=True, size=11 if testa else 9,
                       color='FFFFFF' if b is None else '000000')
        if b is None:
            c1.fill = UF.BLU
        c2.alignment = Alignment(wrap_text=True, vertical='top')
        ws.append([c1, c2])


if __name__ == '__main__':
    famiglia = sys.argv[1] if len(sys.argv) > 1 else 'nascita'
    ucs = sys.argv[2:] or ['Dic_Nasc_001', 'Dic_Nasc_002', 'Dic_Nasc_003']
    righe = confronta(famiglia, ucs)
    ids = id_usecase()
    col = colonne_per(ucs)
    wb = openpyxl.Workbook(write_only=True)
    _legenda(wb, famiglia, ucs, righe, ids)
    diverse = [r for r in righe if r['differenza']]
    _foglio(wb, 'Differenze', col, diverse, evidenzia=lambda r: UF.GIALLO)
    _foglio(wb, 'Confronto completo', col, righe,
            evidenzia=lambda r: UF.GIALLO if r['differenza'] else None)
    nome = 'CONFRONTO_' + '-'.join(u.replace('Dic_Nasc_', '') for u in ucs)
    uscita = os.path.join(CARTELLA, f'{nome}_v0.1.xlsx')
    wb.save(uscita)
    print('scritto :', os.path.relpath(uscita, BASE))
    print('righe   :', len(righe), '· righe che differiscono:', len(diverse))
    for k, v in collections.Counter(r['differenza'] for r in diverse).most_common():
        print(f'   {k:34} {v:4}')
