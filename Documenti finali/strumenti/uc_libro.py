# -*- coding: utf-8 -*-
"""Un file per famiglia, un foglio per caso d'uso, nella forma del foglio compilato a mano.

`Dic_Nasc_001.xlsx` è il riferimento: dodici colonne in quell'ordine, foglio intitolato
all'usecase. Qui la forma si ripete per ogni UC della famiglia, con cinque colonne di
servizio in coda — obbligatorietà calcolata, provenienza della colonna SIPO, evidenza — che
stanno dopo le dodici e si possono ignorare.

⚠️ Ciò che arriva scritto e ciò che no:
  · la struttura viene dal mapping ufficiale dell'UC: sezione, binding, obbligatorietà;
  · la colonna SIPO viene, in quest'ordine, dal lavoro umano sullo stesso percorso, poi dal
    codice, poi dal lavoro umano dell'altra famiglia se la tabella non è specifica;
  · dove nessuno sa, la cella resta vuota e rossa. È il lavoro.

⚠️ Le due famiglie non sono nella stessa condizione: la nascita ha il foglio compilato di
Dic_Nasc_001, la morte non ha nulla. Un valore che nomina una tabella della nascita non si
propaga alla morte: stessa forma, altra sorgente.

    /usr/bin/python3 "Documenti finali/strumenti/uc_libro.py" [famiglia …]
"""
import collections
import os
import sys

import openpyxl
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uc_famiglia as UF        # noqa: E402
from uc_workbook import (ALTRA, COLORI, id_usecase, rifai_percorsi,   # noqa: E402
                         specifica_di_nascita)

BASE, CARTELLA = UF.BASE, UF.CARTELLA

# famiglia → (cartella del mapping, area del codice, foglio compilato a mano, nome del file)
FAMIGLIE = {
    'nascita': ('nascita', 'nascita', 'Dic_Nasc_001', 'MAPPATURA_UC_Nascite_v0.1.xlsx'),
    'morte': ('morte', 'decessi', None, 'MAPPATURA_UC_Morti_v0.1.xlsx'),
}

# le dodici del riferimento, nell'ordine del riferimento, poi le cinque di servizio
COL_UC = [
    ('UseCase', 11, 'id_uc'), ('Sezione FE ANSC', 22, 'sezione'),
    ('Binding Object', 30, 'bo'), ('Binding Field', 26, 'bf'),
    ('Dato obbligatorio SI/NO', 10, 'obbligatorio'),
    ('Tabella/Campo SIPO', 36, 'sipo'),
    ('Regole di transcodifica', 44, 'transcodifica'),
    ('Condizioni particolari/Logiche di business', 44, 'note'),
    ("Condizioni obbligatorieta' ANSC", 38, 'condizione'),
    ('Ordinamento', 10, 'ordinamento'), ('Operativo', 10, 'operativo'),
    ('Default', 10, 'default'),
    ("Obbligatorio per l'UC", 12, 'esito'), ('Come è stato deciso', 30, 'come'),
    ('Origine della colonna SIPO', 24, 'origine'), ('Verificato', 10, 'verificato'),
    ('Evidenza', 50, 'evidenza'),
]
COL_INDICE = [
    ('Caso d’uso', 20, 'uc'), ('ID usecase', 12, 'id_uc'), ('Foglio', 26, 'link'),
    ('Righe', 8, 'righe'), ('Obbligatori', 10, 'obbligatori'),
    ('Colonna SIPO nota', 14, 'noto'), ('Da compilare', 12, 'scoperto'),
    ('Soggetto assente', 14, 'assente'),
]


def raccogli(famiglia):
    """Le righe della famiglia, con il lato SIPO risolto e le colonne del riferimento."""
    cartella, area, sorgente, _ = FAMIGLIE[famiglia]
    righe, percorsi = UF.raccogli(cartella, area, sorgente or '__nessuno__')
    if not sorgente:
        # nessun foglio proprio: si guarda a quello dell'altra famiglia, con prudenza
        altrui = UF.lavoro_a_mano('Dic_Nasc_001')
        for r in righe:
            k = f"{r['bo']}.{r['bf']}".strip('.')
            if r['origine'] not in (UF.SCOPERTO, UF.PROPOSTA) or k not in altrui:
                continue
            sipo, transc, note = altrui[k]
            if not sipo:
                continue
            if not UF.ben_formata(sipo):
                r['note'] = f'Dal foglio di Dic_Nasc_001: {sipo} {note}'.strip()
            elif not specifica_di_nascita(sipo):
                r.update(sipo=UF.normalizza(sipo), transcodifica=transc, note=note,
                         origine=ALTRA, evidenza='Dic_Nasc_001.xlsx (altra famiglia)')
        rifai_percorsi(righe, percorsi)
    ids = id_usecase()
    ordine = collections.Counter()
    for r in righe:
        r['id_uc'] = ids.get(r['uc'], '')
        if not r['bf'] and r.get('campo'):
            r['bf'] = r['campo']          # Formula e Allegati non hanno binding: resta il nome
        ordine[(r['uc'], r['bo'])] += 1
        r['ordinamento'] = ordine[(r['uc'], r['bo'])]
        r['operativo'] = r['default'] = r['verificato'] = ''
    return righe, percorsi


def nome_foglio(uc, id_uc):
    """«11111000 Dic_Nasc_001»: l'ID davanti come nel riferimento, il codice per ritrovarlo."""
    return (f'{id_uc} {uc}' if id_uc else uc)[:31]


def _foglio(wb, nome, colonne, righe, evidenzia=None, link=False):
    ws = wb.create_sheet(nome)
    for j, (_, largh, _) in enumerate(colonne, 1):
        ws.column_dimensions[get_column_letter(j)].width = largh
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = 'F2' if link is False and len(colonne) > 12 else 'A2'
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
            c.alignment = Alignment(vertical='top',
                                    wrap_text=k in ('transcodifica', 'note', 'condizione',
                                                    'come', 'evidenza'))
            if k == 'sipo' and fill:
                c.fill = fill
            elif k == 'esito':
                c.fill = {'SI': UF.VERDE, 'CONDIZIONATO': UF.GIALLO}.get(r.get('esito'),
                                                                        UF.GRIGIO)
            if link and k == 'link' and r.get('link'):
                c.value = r['link']
                c.hyperlink = f"#'{r['link']}'!A1"
                c.font = Font(color='0563C1', underline='single')
            celle.append(c)
        ws.append(celle)
        n += 1
    ws.auto_filter.ref = f'A1:{get_column_letter(len(colonne))}{n}'
    return ws


def _istruzioni(wb, famiglia, righe, percorsi, sorgente):
    ws = wb.create_sheet('Come si compila', 0)
    ws.column_dimensions['A'].width = 42
    ws.column_dimensions['B'].width = 106
    cp = collections.Counter(p['origine'] for p in percorsi)
    cr = collections.Counter(r['origine'] for r in righe if r['origine'])
    n_uc = len({r['uc'] for r in righe})
    voci = [
        (f'Casi d’uso ANSC — famiglia «{famiglia}»',
         'Mappatura SIPO ↔ ANSC · Roma Capitale', True),
        ('Che cos’è',
         f'Un foglio per ciascuno dei {n_uc} casi d’uso della famiglia, nella forma di '
         f'Dic_Nasc_001.xlsx: le stesse dodici colonne nello stesso ordine, più cinque di '
         f'servizio in coda che si possono ignorare. Il foglio si intitola all’ID usecase '
         f'seguito dal codice, per ritrovarlo fra le linguette.', False),
        ('La colonna da compilare',
         '«Tabella/Campo SIPO», nella forma TABELLA.COLONNA. Dove il dato sta dentro un XML '
         '(SOGGETTO.DETTAGLIO_STATOCIVILE) si scrive la colonna e si spiega il percorso in '
         '«Regole di transcodifica». ⚠️ Quella cella è per una SORGENTE: un valore da '
         'calcolare (flagDichiarante=\'false\') va in «Condizioni particolari», altrimenti '
         'alla propagazione diventa una colonna che non esiste.', False),
        ('I colori della colonna SIPO', None, True),
        ('  verde', f'presa dal foglio compilato a mano di {sorgente or "—"}, stesso percorso '
                     f'ANSC. È una propagazione, non un accertamento.', False),
        ('  giallo', 'proposta dal codice, con evidenza file:riga in fondo alla riga. Da '
                     'confermare: sul banco di prova concorda con il compilatore 36 volte su '
                     '41 e nelle 5 divergenze ha torto lui. Spunta «Verificato».', False),
        ('  viola', 'presa dall’altra famiglia, dove il percorso coincide e la tabella non è '
                    'specifica (SOGGETTO, ATTO). Va verificata per questo evento.', False),
        ('  rosso', 'nessuno sa dirla: è il lavoro.', False),
        ('  grigio', 'il blocco intero non ha corrispondente in SIPO. Non è un campo da '
                     'rilevare ma una parte di maschera da progettare.', False),
        ('⚠️ Il lavoro si fa per percorso, non per UC',
         f'I casi d’uso sono {n_uc}, i percorsi ANSC distinti {len(percorsi)}: lo stesso '
         f'percorso ricorre in decine di fogli con la stessa sorgente SIPO. Il foglio «Da '
         f'compilare» li ordina per quante righe ciascuno sblocca; compilato lì, si propaga '
         f'a tutti alla rigenerazione.', False),
        ('L’obbligatorietà',
         'La colonna «Obbligatorio per l’UC» è calcolata: governa «Condizioni '
         'obbligatorieta’» — «obbligatoria» → SI, «opzionale» → NO, un’espressione → '
         'CONDIZIONATO — e «Dato obbligatorio SI/NO» vale solo dove la condizione tace. '
         '⚠️ Le due colonne del mapping si contraddicono in un terzo delle righe del dominio '
         '(su Dic_Nasc_001 «Obbligatorio» dichiara facoltativo il cognome della madre). La '
         'semantica ufficiale non è pubblicata da ANSC: va chiesta a Sogei.', False),
        ('I conti (percorsi · righe)', None, True),
    ]
    for k in (UF.A_MANO, UF.PROPOSTA, ALTRA, UF.SCOPERTO, UF.ASSENTE):
        if cp.get(k) or cr.get(k):
            voci.append((f'  · {k}', f'{cp.get(k, 0)} percorsi · {cr.get(k, 0)} righe', False))
    voci.append(('  · totale', f'{len(percorsi)} percorsi · {len(righe)} righe · {n_uc} UC',
                 False))
    for a, b, testa in voci:
        c1, c2 = WriteOnlyCell(ws, value=a), WriteOnlyCell(ws, value=b)
        c1.font = Font(bold=True, size=11 if testa else 9,
                       color='FFFFFF' if b is None else '000000')
        if b is None:
            c1.fill = UF.BLU
        c2.alignment = Alignment(wrap_text=True, vertical='top')
        ws.append([c1, c2])


def scrivi(famiglia):
    _, _, sorgente, nomefile = FAMIGLIE[famiglia]
    righe, percorsi = raccogli(famiglia)
    per_uc = collections.OrderedDict()
    for r in righe:
        per_uc.setdefault(r['uc'], []).append(r)

    wb = openpyxl.Workbook(write_only=True)
    _istruzioni(wb, famiglia, righe, percorsi, sorgente)

    indice = []
    for uc, rr in per_uc.items():
        c = collections.Counter(x['origine'] for x in rr)
        indice.append({
            'uc': uc, 'id_uc': rr[0]['id_uc'],
            'link': nome_foglio(uc, rr[0]['id_uc']), 'righe': len(rr),
            'obbligatori': sum(1 for x in rr if x['esito'] == 'SI'),
            'noto': c.get(UF.A_MANO, 0) + c.get(UF.PROPOSTA, 0) + c.get(ALTRA, 0),
            'scoperto': c.get(UF.SCOPERTO, 0), 'assente': c.get(UF.ASSENTE, 0),
        })
    _foglio(wb, 'Indice', COL_INDICE, indice, link=True,
            evidenzia=lambda r: UF.ROSSO if r['scoperto'] > r['noto'] else None)
    da_fare = sorted((p for p in percorsi if p['origine'] == UF.SCOPERTO),
                     key=lambda p: -p['n_uc'])
    _foglio(wb, 'Da compilare', UF.COL_PERC, da_fare, evidenzia=lambda p: UF.ROSSO)
    for uc, rr in per_uc.items():
        _foglio(wb, nome_foglio(uc, rr[0]['id_uc']), COL_UC, rr,
                evidenzia=lambda r: COLORI.get(r['origine'], UF.ROSSO))
    uscita = os.path.join(CARTELLA, nomefile)
    wb.save(uscita)
    return uscita, righe, percorsi, per_uc


if __name__ == '__main__':
    volute = sys.argv[1:] or ['morte', 'nascita']
    for fam in volute:
        uscita, righe, percorsi, per_uc = scrivi(fam)
        print(f'\n=== {fam} ===')
        print('scritto :', os.path.relpath(uscita, BASE))
        print('fogli   :', 2 + len(per_uc), f'({len(per_uc)} UC + istruzioni e indice)',
              '· righe:', len(righe))
        for k, v in collections.Counter(p['origine'] for p in percorsi).most_common():
            print(f'   {k or "(senza binding)":30} {v:5} percorsi')
