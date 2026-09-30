# -*- coding: utf-8 -*-
"""Tutti gli UC di una famiglia, con il lavoro già fatto propagato e il residuo isolato.

Il foglio compilato a mano di un UC (`documenti elaborati intermedi/<UC>.xlsx`) vale molto
oltre il proprio caso d'uso: il percorso ANSC `madre.cognome` è lo stesso in tutta la
famiglia, e con esso la colonna SIPO. Sulle nascite 78 percorsi compilati coprono 9.822
righe su 23.307 — il 42 % — senza scrivere altro.

⚠️ Il lavoro NON si organizza per caso d'uso ma PER PERCORSO. Compilare 143 fogli significa
riscrivere 143 volte la stessa cosa; compilare i percorsi distinti ancora scoperti — 109 —
li completa tutti. Il foglio «Da compilare» è quello: ordinato per quante righe ciascun
percorso sblocca, così il lavoro parte da dove rende di più.

⚠️ L'eredità è una PROPAGAZIONE, non un accertamento: vale perché il percorso ANSC coincide,
ma UC di maschere diverse possono attingere a tabelle diverse (i casi di servizio `*_998_*`
soprattutto). La colonna «Origine» lo dichiara riga per riga: non si spaccia per rilevato ciò
che è dedotto.

    /usr/bin/python3 "Documenti finali/strumenti/uc_famiglia.py" [famiglia] [area] [UC sorgente]
"""
import collections
import csv
import glob
import os
import re
import sys

import openpyxl
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ponte_ansc_sipo as PT   # noqa: E402
import sipo_dizionario as SD   # noqa: E402
from completa_uc import esito_obbligatorieta   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARTELLA = os.path.join(BASE, 'documenti elaborati intermedi')
BLU = PatternFill('solid', fgColor='1F3864')
VERDE = PatternFill('solid', fgColor='E6F2E6')
GIALLO = PatternFill('solid', fgColor='FFF2CC')
ROSSO = PatternFill('solid', fgColor='FCE4E4')
GRIGIO = PatternFill('solid', fgColor='F2F2F2')

A_MANO = 'compilata a mano'
PROPOSTA = 'proposta automatica'
SCOPERTO = 'DA COMPILARE'
ASSENTE = 'soggetto assente in SIPO'


def lavoro_a_mano(uc_sorgente):
    """Percorso ANSC → (colonna SIPO, transcodifica, note), dal foglio compilato a mano."""
    f = os.path.join(CARTELLA, uc_sorgente + '.xlsx')
    if not os.path.exists(f):
        return {}      # famiglia senza foglio compilato: non è un errore, è il caso morte
    ws = openpyxl.load_workbook(f).active
    fuori = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not any(v not in (None, '') for v in r):
            continue
        k = f'{r[2]}.{r[3]}'.strip('.')
        # ⚠️ si eredita anche dove la colonna SIPO è vuota ma c'è una regola o una nota:
        # «Fisso = ITALIA» su intestatari[0].idStatoNascita è lavoro umano quanto una colonna,
        # e prenderlo solo dalle righe con la colonna piena lo perderebbe.
        if r[5] or r[6] or r[7]:
            fuori[k] = (str(r[5] or ''), str(r[6] or ''), str(r[7] or ''))
    return fuori


def ben_formata(valore):
    """Una colonna SIPO è TABELLA.COLONNA: tutto il resto è una nota, e va trattato da nota.

    ⚠️ Nel foglio compilato a mano la cella «Tabella/Campo SIPO» ospita anche annotazioni —
    `flagDichiarante='false'` — che descrivono un valore da calcolare, non una sorgente.
    Propagarle come colonne le trasformerebbe in dati falsi.
    """
    v = (valore or '').strip()
    if not v or '.' not in v:
        return False
    tab, _, col = v.partition('.')
    return bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', tab)
                and re.match(r'[A-Za-z][A-Za-z0-9_]*', col.split('(')[0].strip())
                and tab.upper() == tab)


def normalizza(valore):
    """Il nome della tabella in maiuscolo: il dizionario a volte restituisce quello della classe."""
    v = (valore or '').strip()
    if '.' not in v:
        return v
    tab, _, resto = v.partition('.')
    return f'{tab.upper()}.{resto}'


def raccogli(famiglia, area, uc_sorgente):
    mano = lavoro_a_mano(uc_sorgente)
    ponte = PT.Ponte(area, ent=SD.entita(('common', 'back-end')))
    memo = {}

    def risolvi(k):
        if k not in memo:
            p = re.sub(r'^evento\.?', '', k).strip('.')
            e = ponte.risolvi(p)
            d = ponte.dettaglio(e['percorso_sipo']) if e['percorso_sipo'] else None
            dest = (d or {}).get('destinazione') or {}
            memo[k] = (normalizza(f"{dest.get('tabella', '')}.{dest['colonna']}")
                       if dest.get('colonna') else '',
                       dest.get('evidenza', ''), e['grado'])
        return memo[k]

    righe, percorsi = [], collections.OrderedDict()
    for f in sorted(glob.glob(os.path.join(BASE, 'ansc', 'docs', 'Mapping_casi_uso',
                                           famiglia, '*.csv'))):
        uc = os.path.basename(f)[:-4]
        with open(f, encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if (r.get('Sezione') or '').strip() == 'Sezione':
                    continue
                bo = (r.get('Binding Object') or '').strip()
                bf = (r.get('Binding Field') or '').strip()
                k = f'{bo}.{bf}'.strip('.')
                esito, come = esito_obbligatorieta(r.get('Obbligatorio'),
                                                   r.get("Condizioni obbligatorieta'"))
                sipo = transc = note = evid = ''
                if not k:
                    origine = ''            # Formula e Allegati non hanno binding
                elif k in mano:
                    sipo, transc, note = mano[k]
                    evid = f'{uc_sorgente}.xlsx'
                    if sipo and not ben_formata(sipo):
                        # è un'annotazione, non una colonna: si sposta fra le note
                        note = (f'{sipo} {note}').strip()
                        sipo = ''
                    if sipo:
                        origine = A_MANO
                    else:
                        # la nota si propaga, ma la colonna resta da rilevare: non si spaccia
                        # per compilata una riga che non ha una destinazione
                        prop, ev, grado = risolvi(k)
                        if prop:
                            sipo, origine, evid = prop, PROPOSTA, ev
                        else:
                            origine = (ASSENTE if grado == 'soggetto assente in SIPO'
                                       else SCOPERTO)
                else:
                    prop, ev, grado = risolvi(k)
                    if prop:
                        sipo, origine, evid = prop, PROPOSTA, ev
                    elif grado == 'soggetto assente in SIPO':
                        origine = ASSENTE
                    else:
                        origine = SCOPERTO
                righe.append({
                    'uc': uc, 'sezione': r.get('Sezione', ''), 'campo': r.get('Campo', ''),
                    'bo': bo, 'bf': bf, 'obbligatorio': r.get('Obbligatorio', ''),
                    'sipo': sipo, 'transcodifica': transc, 'note': note,
                    'condizione': r.get("Condizioni obbligatorieta'", ''),
                    'esito': esito, 'come': come, 'origine': origine, 'evidenza': evid,
                })
                if k:
                    a = percorsi.setdefault(k, {'percorso': k, 'bo': bo, 'bf': bf,
                                                'origine': origine, 'sipo': sipo,
                                                'evidenza': evid, 'n_uc': 0, 'n_obbl': 0,
                                                '_uc': set(), 'sezioni': set()})
                    a['_uc'].add(uc)
                    a['sezioni'].add(r.get('Sezione', ''))
                    if esito == 'SI':
                        a['n_obbl'] += 1
    for a in percorsi.values():
        a['n_uc'] = len(a['_uc'])
        a['sezioni'] = ', '.join(sorted(x for x in a['sezioni'] if x))[:120]
    return righe, list(percorsi.values())


def _foglio(wb, nome, colonne, righe, evidenzia=None):
    ws = wb.create_sheet(nome)
    for j, (_, largh, _) in enumerate(colonne, 1):
        ws.column_dimensions[get_column_letter(j)].width = largh
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = 'A2'
    testa = []
    for titolo, _, _ in colonne:
        c = WriteOnlyCell(ws, value=titolo)
        c.font = Font(bold=True, color='FFFFFF', size=9)
        c.fill = BLU
        c.alignment = Alignment(vertical='center', wrap_text=True)
        testa.append(c)
    ws.append(testa)
    n = 1
    for r in righe:
        fill = evidenzia(r) if evidenzia else None
        vals = [r.get(k, '') for _, _, k in colonne]
        if fill:
            celle = []
            for v in vals:
                c = WriteOnlyCell(ws, value=v)
                c.fill = fill
                celle.append(c)
            ws.append(celle)
        else:
            ws.append(vals)
        n += 1
    ws.auto_filter.ref = f'A1:{get_column_letter(len(colonne))}{n}'
    return ws


COL_RIGHE = [
    ('UC', 16, 'uc'), ('Sezione', 22, 'sezione'), ('Campo', 30, 'campo'),
    ('Binding Object', 30, 'bo'), ('Binding Field', 24, 'bf'),
    ('Dato obbligatorio SI/NO', 10, 'obbligatorio'),
    ("Condizioni obbligatorieta' ANSC", 40, 'condizione'),
    ("Obbligatorio per l'UC", 12, 'esito'), ('Come è stato deciso', 30, 'come'),
    ('Tabella/Campo SIPO', 34, 'sipo'), ('Origine della colonna SIPO', 20, 'origine'),
    ('Regole di transcodifica', 44, 'transcodifica'),
    ('Condizioni particolari/Logiche di business', 44, 'note'),
    ('Evidenza', 46, 'evidenza'),
]
COL_PERC = [
    ('Percorso ANSC', 46, 'percorso'), ('Binding Object', 30, 'bo'),
    ('Binding Field', 24, 'bf'), ('Sezioni in cui compare', 40, 'sezioni'),
    ('UC che lo usano', 9, 'n_uc'), ('di cui lo dichiarano obbligatorio', 10, 'n_obbl'),
    ('Tabella/Campo SIPO', 34, 'sipo'), ('Origine', 20, 'origine'),
    ('Evidenza', 46, 'evidenza'),
]
COLORI = {A_MANO: VERDE, PROPOSTA: GIALLO, SCOPERTO: ROSSO, ASSENTE: GRIGIO}


def _legenda(wb, righe, percorsi, famiglia, uc_sorgente):
    ws = wb.create_sheet('Legenda', 0)
    ws.column_dimensions['A'].width = 42
    ws.column_dimensions['B'].width = 104
    cp = collections.Counter(p['origine'] for p in percorsi)
    cr = collections.Counter(r['origine'] for r in righe if r['origine'])
    ce = collections.Counter(r['esito'] for r in righe)
    voci = [
        (f'Mappatura degli UC — famiglia «{famiglia}»', 'SIPO ↔ ANSC · Roma Capitale', True),
        ('Che cos’è',
         f'Tutti i casi d’uso della famiglia, con la colonna SIPO propagata dal foglio '
         f'compilato a mano di {uc_sorgente} e, dove quello tace, proposta dal codice. '
         f'Si rigenera con «Documenti finali/strumenti/uc_famiglia.py»: non si corregge a '
         f'mano, se non nel foglio di lavoro dell’UC sorgente.', False),
        ('⚠️ Il lavoro si fa PER PERCORSO, non per UC',
         f'I casi d’uso sono {len({r["uc"] for r in righe})}, ma i percorsi ANSC distinti '
         f'sono {len(percorsi)}. Lo stesso percorso ricorre in decine di UC con la stessa '
         f'sorgente SIPO: compilarlo una volta lo risolve ovunque. Il foglio «Da compilare» '
         f'è ordinato per quante righe ciascun percorso sblocca.', False),
        ('Le quattro origini della colonna SIPO', None, True),
        (f'  {A_MANO}',
         f'Presa dal foglio di {uc_sorgente}, dove il percorso coincide. ⚠️ È una '
         f'PROPAGAZIONE: vale perché il percorso ANSC è lo stesso, ma UC di maschere diverse '
         f'possono attingere a tabelle diverse — i casi di servizio in particolare.', False),
        (f'  {PROPOSTA}',
         'Ricavata dal codice risalendo maschera → DTO → colonna. Sul banco di prova di '
         'Dic_Nasc_001 concorda con la compilazione a mano 36 volte su 41, e le 5 '
         'divergenze danno ragione al compilatore: è un suggerimento, non un rilievo.', False),
        (f'  {SCOPERTO}',
         'Il percorso esiste in SIPO ma la colonna non è stata determinata: è il lavoro che '
         'resta, ed è nel foglio omonimo.', False),
        (f'  {ASSENTE}',
         'Manca l’intero blocco (i comparenti, l’ente dichiarante, l’interprete…): non è un '
         'campo da rilevare ma una parte di maschera da progettare.', False),
        ('I conti', None, True),
    ]
    for k in (A_MANO, PROPOSTA, SCOPERTO, ASSENTE):
        voci.append((f'  · {k}', f'{cp.get(k, 0)} percorsi · {cr.get(k, 0)} righe UC×campo',
                     False))
    voci += [
        ('  · totale', f'{len(percorsi)} percorsi · {len(righe)} righe', False),
        ('L’obbligatorietà', None, True),
        ('  la regola',
         'Governa la colonna «Condizioni obbligatorieta’»; «Obbligatorio» interviene solo '
         'dove quella tace. ⚠️ Le due colonne del mapping si contraddicono in un terzo delle '
         'righe: su Dic_Nasc_001 «Obbligatorio» dichiara facoltativo il cognome della madre. '
         'La semantica ufficiale non è pubblicata: va chiesta a Sogei.', False),
        ('  esito su questa famiglia',
         ' · '.join(f'{k or "(non dichiarato)"}: {v}' for k, v in ce.most_common()), False),
    ]
    for a, b, testa in voci:
        # in streaming la cella si stila prima di appenderla: non si torna indietro
        c1, c2 = WriteOnlyCell(ws, value=a), WriteOnlyCell(ws, value=b)
        c1.font = Font(bold=True, size=11 if testa else 9,
                       color='FFFFFF' if b is None else '000000')
        if b is None:
            c1.fill = BLU
        c2.alignment = Alignment(wrap_text=True, vertical='top')
        ws.append([c1, c2])


if __name__ == '__main__':
    fam = sys.argv[1] if len(sys.argv) > 1 else 'nascita'
    area = sys.argv[2] if len(sys.argv) > 2 else 'nascita'
    src = sys.argv[3] if len(sys.argv) > 3 else 'Dic_Nasc_001'
    righe, percorsi = raccogli(fam, area, src)
    uscita = os.path.join(CARTELLA, f'MAPPATURA_UC_{fam}_v0.1.xlsx')
    wb = openpyxl.Workbook(write_only=True)
    _legenda(wb, righe, percorsi, fam, src)
    da_fare = sorted((p for p in percorsi if p['origine'] == SCOPERTO),
                     key=lambda p: -p['n_uc'])
    _foglio(wb, 'Da compilare', COL_PERC, da_fare, evidenzia=lambda p: ROSSO)
    _foglio(wb, 'Percorsi (tutti)', COL_PERC, sorted(percorsi, key=lambda p: -p['n_uc']),
            evidenzia=lambda p: COLORI.get(p['origine']))
    _foglio(wb, 'Tutti gli UC', COL_RIGHE, righe,
            evidenzia=lambda r: COLORI.get(r['origine']))
    _foglio(wb, 'Soggetti assenti in SIPO', COL_PERC,
            sorted((p for p in percorsi if p['origine'] == ASSENTE),
                   key=lambda p: -p['n_uc']), evidenzia=lambda p: GRIGIO)
    wb.save(uscita)
    print('scritto :', os.path.relpath(uscita, BASE))
    print('UC      :', len({r['uc'] for r in righe}), '· righe:', len(righe),
          '· percorsi distinti:', len(percorsi))
    for k, v in collections.Counter(p['origine'] for p in percorsi).most_common():
        print(f'   {k or "(senza binding)":26} {v:5} percorsi')
