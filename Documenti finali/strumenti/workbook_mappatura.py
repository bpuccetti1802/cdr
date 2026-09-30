# -*- coding: utf-8 -*-
"""Genera il workbook della mappatura campo per campo ANSC ↔ modello evento ↔ SIPO.

Non contiene regole: le prende da `mappatura_uc.py`. Se ANSC pubblica una revisione del
mapping, si riesegue — non si corregge a mano il foglio.

    /usr/bin/python3 "Documenti finali/strumenti/workbook_mappatura.py" [file.xlsx]

Fogli prodotti:
  Legenda            che cos'è, da dove viene, quanto lavoro umano resta
  Percorsi           IL FOGLIO DI LAVORO: una riga per (famiglia, percorso), colonna SIPO da completare
  Mappatura          il fabbisogno dichiarato da ANSC, riga per riga (UC × campo)
  Allegati           gli allegati richiesti per UC, con il codice ANSC_09 raccordato
  Formule            le formule ministeriali dichiarate per UC (oggi non configurate, OP-51)
  Casi d'uso         i 374 UC con i loro numeri
  Non risolti        i percorsi del mapping che il modello evento non conosce (OP-52)
"""
import collections
import os
import sys

import openpyxl
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mappatura_uc as M  # noqa: E402
import mappatura_sipo as MS  # noqa: E402
import ponte_ansc_sipo as PT  # noqa: E402
import sipo_dizionario as SD  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USCITA = os.path.join(BASE, 'Documenti finali', 'MAPPATURA_Campi_ANSC-SIPO_v0.2.xlsx')

BLU = PatternFill('solid', fgColor='1F3864')
GRIGIO = PatternFill('solid', fgColor='EDEDED')
GIALLO = PatternFill('solid', fgColor='FFF2CC')
ROSSO = PatternFill('solid', fgColor='FCE4E4')
VERDE = PatternFill('solid', fgColor='E6F2E6')
BORDO = Border(*(Side(style='thin', color='BFBFBF'),) * 4)


def foglio(wb, nome, colonne, righe, evidenzia=None):
    """Un foglio con intestazione bloccata, filtro automatico e larghezze dichiarate.

    `colonne` = [(titolo, larghezza, chiave)], `evidenzia` = f(riga) -> PatternFill|None.

    Funziona sia sul workbook ordinario sia su uno aperto in `write_only=True`, dove le
    righe vengono scritte man mano invece di restare in memoria. Serve per i fogli grandi:
    una mappatura di due famiglie sfiora il milione di celle, e in modalità ordinaria
    openpyxl le tiene tutte come oggetti — il processo viene ucciso prima di salvare.
    ⚠️ In write_only larghezze, blocco dei riquadri e altezza della prima riga vanno
    impostati PRIMA del primo append: openpyxl chiude la testata del foglio lì.
    """
    ws = wb.create_sheet(nome)
    streaming = getattr(wb, 'write_only', False)
    ultima = get_column_letter(len(colonne))

    for j, (_, largh, _) in enumerate(colonne, 1):
        ws.column_dimensions[get_column_letter(j)].width = largh
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = 'A2'

    intestazione = []
    for titolo, _, _ in colonne:
        c = WriteOnlyCell(ws, value=titolo) if streaming else titolo
        intestazione.append(c)
    ws.append(intestazione)
    if not streaming:
        for j in range(1, len(colonne) + 1):
            ws.cell(row=1, column=j).font = Font(bold=True, color='FFFFFF', size=9)
            ws.cell(row=1, column=j).fill = BLU
            ws.cell(row=1, column=j).alignment = Alignment(vertical='center',
                                                           wrap_text=True)
    else:
        for c in intestazione:
            c.font = Font(bold=True, color='FFFFFF', size=9)
            c.fill = BLU
            c.alignment = Alignment(vertical='center', wrap_text=True)

    n = 1
    for r in righe:
        valori = [r.get(k, '') for _, _, k in colonne]
        fill = evidenzia(r) if evidenzia else None
        if streaming:
            if fill:
                celle = []
                for v in valori:
                    c = WriteOnlyCell(ws, value=v)
                    c.fill = fill
                    celle.append(c)
                ws.append(celle)
            else:
                ws.append(valori)
        else:
            ws.append(valori)
            if fill:
                for j in range(1, len(colonne) + 1):
                    ws.cell(row=ws.max_row, column=j).fill = fill
        n += 1

    ws.auto_filter.ref = f'A1:{ultima}{n}'
    return ws


def si_no(v):
    return 'Sì' if v else ''


def costruisci(percorso=USCITA):
    modello = M.Modello()
    sipo = M.lato_sipo(modello)
    righe = M.mappatura(modello, sipo)

    # Il lato DB si risolve dove esiste una ricognizione E il codice dell'area: morte (pilota)
    # e nascita. Per le altre famiglie le colonne restano vuote, ed è un'informazione: dice
    # esattamente dove il lavoro non è ancora stato fatto.
    ent = SD.entita()
    vuote = {k: '' for k in (
        'sipo_ricognizione', 'sipo_maschera', 'sipo_riferito_a_questo_uc', 'sipo_campo_dto',
        'sipo_grado', 'sipo_certezza_etichetta', 'sipo_tabella', 'sipo_colonna',
        'sipo_percorso_xml', 'sipo_tipo_java', 'sipo_genere', 'sipo_ambiguo', 'sipo_motivo',
        'evidenza_maschera', 'evidenza_salvataggio', 'conversione_richiesta',
        'conversione_regola')}
    # ⚠️ Dalla v0.2 il lato SIPO lo risolve il PONTE (`ponte_ansc_sipo`), non più il raccordo
    # per etichetta di `mappatura_sipo`: si parte dal percorso del modello evento e si passa
    # per il soggetto, perché «Cognome» non dice di chi e una maschera di nascita ne ha
    # undici. La ricognizione funzionale resta come riscontro indipendente.
    arricchite, risolutori = {}, {}
    for fam, area in (('morte', 'decessi'), ('nascita', 'nascita')):
        ponte = PT.Ponte(area, ent=ent)
        # il risolutore per etichetta non alimenta più la mappatura, ma serve ancora al
        # foglio «Dizionario SIPO»: lì la domanda è l'inversa (dove va a finire OGNI campo
        # della maschera), e per quella l'etichetta è il nome giusto.
        risolutori[area] = MS.risolutore(area, ent)
        for r in PT.arricchisci(fam, ponte, modello, sipo, righe):
            arricchite[(r['motore'], r['sezione'], r['campo'], r['binding'])] = r
    righe = [arricchite.get((r['motore'], r['sezione'], r['campo'], r['binding']),
                            dict(r, **vuote)) for r in righe]

    campi = [r for r in righe if r['binding']]
    allegati = [r for r in righe if r['sezione'] == 'Allegati']
    formule = [r for r in righe if r['sezione'] == 'Formula']

    # write_only: 63.531 righe di mappatura non stanno in memoria come oggetti-cella.
    wb = openpyxl.Workbook(write_only=True)

    # ---------------------------------------------------------------- Percorsi
    agg = collections.OrderedDict()
    for r in campi:
        k = (r['famiglia'], r['percorso'])
        a = agg.get(k)
        if a is None:
            a = agg[k] = {
                'famiglia': r['famiglia'], 'percorso': r['percorso'],
                'risolto': si_no(r['risolto']), 'tipo': r['tipo'], 'formato': r['formato'],
                'lista': si_no(r['lista']), 'decodifica': r['decodifica'],
                'deprecato': si_no(r['deprecato']),
                'descrizione_campo': r['descrizione_campo'][:900],
                'classe': r['classe'], 'regola': r['regola'],
                'n_uc': 0, 'n_obbl': 0, '_cond': set(), '_uc': set(),
                'sipo_stato': r['sipo_stato'], 'sipo_campo': r['sipo_campo'],
                'sipo_tipo': r['sipo_tipo'], 'sipo_note': r['sipo_note'],
                'sipo_fonte': r['sipo_fonte'], '_risolto': r['risolto'],
                'sipo_ricognizione': r.get('sipo_ricognizione', ''),
                'sipo_campo_dto': r.get('sipo_campo_dto', ''),
                'sipo_tabella': r.get('sipo_tabella', ''),
                'sipo_colonna': r.get('sipo_colonna', ''),
                'sipo_percorso_xml': r.get('sipo_percorso_xml', ''),
                'sipo_tipo_java': r.get('sipo_tipo_java', ''),
                'sipo_genere': r.get('sipo_genere', ''),
                'conversione_richiesta': r.get('conversione_richiesta', ''),
                'conversione_regola': r.get('conversione_regola', ''),
                'evidenza_maschera': r.get('evidenza_maschera', ''),
                'evidenza_salvataggio': r.get('evidenza_salvataggio', ''),
                'sipo_altrove_campo': r['sipo_altrove_campo'],
                'sipo_altrove_uc': r['sipo_altrove_uc'],
            }
        a['_uc'].add(r['motore'])
        if r['obbligatorio'].upper().startswith('S'):
            a['n_obbl'] += 1
        if r['condizione']:
            a['_cond'].add(r['condizione'])
        if r.get('sipo_colonna') and not a['sipo_colonna']:
            for k in ('sipo_ricognizione', 'sipo_campo_dto', 'sipo_tabella', 'sipo_colonna',
                      'sipo_percorso_xml', 'sipo_tipo_java', 'sipo_genere',
                      'conversione_richiesta', 'conversione_regola', 'evidenza_maschera',
                      'evidenza_salvataggio'):
                a[k] = r.get(k, '')
        if r['sipo_campo'] and not a['sipo_campo']:
            a.update(sipo_campo=r['sipo_campo'], sipo_tipo=r['sipo_tipo'],
                     sipo_note=r['sipo_note'], sipo_fonte=r['sipo_fonte'],
                     sipo_stato=r['sipo_stato'])
    for a in agg.values():
        a['n_uc'] = len(a['_uc'])
        a['n_cond'] = len(a['_cond'])
        a['condizioni'] = ' | '.join(sorted(a['_cond']))[:900]

    ordine = {f: i for i, f in enumerate(
        ['Morte', 'Nascita', 'Riconoscimenti', 'Matrimoni', 'Unioni civili',
         'Cittadinanza', 'Trascrizioni'])}
    percorsi = sorted(agg.values(),
                      key=lambda a: (ordine.get(a['famiglia'], 9), -a['n_uc'], a['percorso']))

    foglio(wb, 'Percorsi', [
        ('Famiglia', 14, 'famiglia'),
        ('Percorso nel modello evento', 52, 'percorso'),
        ('UC che lo usano', 9, 'n_uc'),
        ('di cui obbligatorio', 9, 'n_obbl'),
        ('Condizioni distinte', 9, 'n_cond'),
        ('Risolto sul modello', 9, 'risolto'),
        ('Tipo', 11, 'tipo'), ('Formato', 11, 'formato'), ('Lista', 7, 'lista'),
        ('Decodifica ANSC', 12, 'decodifica'), ('Deprecato', 9, 'deprecato'),
        ('Classe di conversione', 22, 'classe'),
        ('Regola di conversione', 60, 'regola'),
        ('Descrizione dal contratto', 50, 'descrizione_campo'),
        ('Campo della maschera SIPO', 28, 'sipo_ricognizione'),
        ('Proprietà del DTO', 26, 'sipo_campo_dto'),
        ('TABELLA SIPO', 22, 'sipo_tabella'),
        ('COLONNA SIPO', 26, 'sipo_colonna'),
        ('Percorso XML', 38, 'sipo_percorso_xml'),
        ('Tipo in SIPO', 13, 'sipo_tipo_java'),
        ('Grado di accertamento', 18, 'sipo_genere'),
        ('Conversione richiesta', 10, 'conversione_richiesta'),
        ('Conversione — che cosa serve fare', 66, 'conversione_regola'),
        ('Evidenza (maschera)', 38, 'evidenza_maschera'),
        ('Evidenza (salvataggio)', 38, 'evidenza_salvataggio'),
        ('Rilievo disponibile per un altro UC', 26, 'sipo_altrove_campo'),
        ('Note della ricognizione', 34, 'sipo_note'),
        ('Fonte del rilievo', 22, 'sipo_fonte'),
    ], percorsi,
        evidenzia=lambda r: ROSSO if not r['_risolto'] else (
            VERDE if r['sipo_genere'] in ('colonna', 'xml')
            else GIALLO if not r['sipo_colonna'] else None))

    # ---------------------------------------------------------------- Mappatura
    foglio(wb, 'Mappatura', [
        ('Famiglia', 14, 'famiglia'),
        ('UC (codice motore)', 16, 'motore'),
        ('UC (codice ANSC)', 12, 'uc'),
        ('Descrizione UC', 40, 'descrizione_uc'),
        ('Sezione', 22, 'sezione'),
        ('Campo (mapping)', 34, 'campo'),
        ('Obbligatorio', 10, 'obbligatorio'),
        ('Condizione di obbligatorietà', 40, 'condizione'),
        ('Percorso nel modello evento', 52, 'percorso'),
        ('Binding dichiarato dal mapping', 46, 'binding'),
        ('Risolto', 8, '_risolto'),
        ('Tipo', 11, 'tipo'), ('Formato', 11, 'formato'),
        ('Decodifica ANSC', 12, 'decodifica'),
        ('Classe di conversione', 22, 'classe'),
        ('Campo della maschera SIPO', 30, 'sipo_ricognizione'),
        ('Maschera', 18, 'sipo_maschera'),
        ('Rilevato per questo UC', 10, 'sipo_riferito_a_questo_uc'),
        ('Proprietà del DTO', 28, 'sipo_campo_dto'),
        ('TABELLA SIPO', 24, 'sipo_tabella'),
        ('COLONNA SIPO', 28, 'sipo_colonna'),
        ('Percorso XML (dentro la colonna)', 40, 'sipo_percorso_xml'),
        ('Tipo in SIPO', 14, 'sipo_tipo_java'),
        ('Grado di accertamento', 20, 'sipo_genere'),
        ('Via di risoluzione', 30, 'sipo_grado'),
        ('Conversione richiesta', 10, 'conversione_richiesta'),
        ('Conversione — che cosa serve fare', 70, 'conversione_regola'),
        ('Evidenza (maschera)', 40, 'evidenza_maschera'),
        ('Evidenza (salvataggio)', 40, 'evidenza_salvataggio'),
        ('Perché non risolto', 46, 'sipo_motivo'),
    ], [dict(r, _risolto=si_no(r['risolto'])) for r in campi],
        evidenzia=lambda r: (VERDE if r.get('sipo_genere') in ('colonna', 'xml')
                             else GIALLO if r.get('sipo_genere') == 'convenzione' else None))

    # ---------------------------------------------------------------- Allegati
    foglio(wb, 'Allegati', [
        ('Famiglia', 14, 'famiglia'),
        ('UC (codice motore)', 16, 'motore'),
        ('UC (codice ANSC)', 12, 'uc'),
        ('Descrizione UC', 40, 'descrizione_uc'),
        ('Descrizione allegato (dal mapping)', 52, 'campo'),
        ('Obbligatorio', 10, 'obbligatorio'),
        ('Condizione di obbligatorietà', 46, 'condizione'),
        ('Codice ANSC_09', 12, 'allegato_codice'),
        ('Descrizione ufficiale ANSC_09', 46, 'allegato_descrizione'),
    ], allegati, evidenzia=lambda r: ROSSO if not r['allegato_codice'] else None)

    # ---------------------------------------------------------------- Formule
    foglio(wb, 'Formule', [
        ('Famiglia', 14, 'famiglia'),
        ('UC (codice motore)', 16, 'motore'),
        ('UC (codice ANSC)', 12, 'uc'),
        ('Descrizione UC', 40, 'descrizione_uc'),
        ('Formula (dal mapping)', 60, 'campo'),
        ('Obbligatorio', 10, 'obbligatorio'),
        ('Note di obbligatorietà', 50, 'formule'),
    ], formule)

    # ---------------------------------------------------------------- Casi d'uso
    per_uc = collections.OrderedDict()
    for r in righe:
        u = per_uc.setdefault(r['motore'], {
            'famiglia': r['famiglia'], 'motore': r['motore'], 'uc': r['uc'],
            'descrizione_uc': r['descrizione_uc'], 'n_campi': 0, 'n_obbl': 0,
            'n_alleg': 0, 'n_alleg_obbl': 0, 'n_formule': 0, 'n_non_risolti': 0,
            'n_sipo': 0, '_perc': set(),
        })
        if r['sezione'] == 'Allegati':
            u['n_alleg'] += 1
            u['n_alleg_obbl'] += r['obbligatorio'].upper().startswith('S')
        elif r['sezione'] == 'Formula':
            u['n_formule'] += 1
        else:
            u['n_campi'] += 1
            u['_perc'].add(r['percorso'])
            u['n_obbl'] += r['obbligatorio'].upper().startswith('S')
            u['n_non_risolti'] += not r['risolto']
            u['n_sipo'] += bool(r['sipo_campo'])
    for u in per_uc.values():
        u['n_perc'] = len(u['_perc'])
        u['copertura'] = round(u['n_sipo'] / u['n_campi'], 3) if u['n_campi'] else 0
    foglio(wb, "Casi d'uso", [
        ('Famiglia', 14, 'famiglia'),
        ('UC (codice motore)', 16, 'motore'),
        ('UC (codice ANSC)', 12, 'uc'),
        ('Descrizione UC', 46, 'descrizione_uc'),
        ('Campi dichiarati', 10, 'n_campi'),
        ('Percorsi distinti', 10, 'n_perc'),
        ('Campi obbligatori', 10, 'n_obbl'),
        ('Percorsi non risolti', 10, 'n_non_risolti'),
        ('Righe con lato SIPO', 10, 'n_sipo'),
        ('Copertura lato SIPO', 10, 'copertura'),
        ('Allegati', 9, 'n_alleg'),
        ('di cui obbligatori', 9, 'n_alleg_obbl'),
        ('Formule', 9, 'n_formule'),
    ], sorted(per_uc.values(), key=lambda u: (ordine.get(u['famiglia'], 9), u['motore'])),
        evidenzia=lambda u: ROSSO if u['n_non_risolti'] else None)

    # ---------------------------------------------------------------- Non risolti
    nr = collections.OrderedDict()
    for r in campi:
        if r['risolto']:
            continue
        a = nr.setdefault(r['percorso'], {
            'percorso': r['percorso'], 'binding': r['binding'], 'occorrenze': 0,
            '_uc': set(), '_fam': set(), '_sez': set(), '_campi': set()})
        a['occorrenze'] += 1
        a['_uc'].add(r['motore'])
        a['_fam'].add(r['famiglia'])
        a['_sez'].add(r['sezione'])
        a['_campi'].add(r['campo'])
    for a in nr.values():
        a['n_uc'] = len(a['_uc'])
        a['famiglie'] = ', '.join(sorted(a['_fam']))
        a['sezioni'] = ', '.join(sorted(a['_sez']))
        a['campi'] = ' | '.join(sorted(a['_campi']))[:500]
        a['uc'] = ', '.join(sorted(a['_uc']))[:500]
    foglio(wb, 'Non risolti', [
        ('Percorso non risolto', 60, 'percorso'),
        ('Binding dichiarato dal mapping', 60, 'binding'),
        ('Occorrenze', 10, 'occorrenze'),
        ('UC coinvolti', 10, 'n_uc'),
        ('Famiglie', 24, 'famiglie'),
        ('Sezioni', 30, 'sezioni'),
        ('Nome del campo nel mapping', 46, 'campi'),
        ('Elenco degli UC', 60, 'uc'),
    ], sorted(nr.values(), key=lambda a: -a['occorrenze']))

    # ---------------------------------------------------------------- Dizionario SIPO
    # Il dizionario è un prodotto a sé: dice dove sta ogni campo delle maschere, e resta utile
    # anche fuori dall'integrazione ANSC (è la mappa che nessun documento del sistema contiene).
    diz, collegate = [], set()
    for r in righe:
        if r.get('sipo_campo_dto'):
            collegate.add((r['sipo_maschera'], r['sipo_campo_dto']))
    for area, ris in risolutori.items():
        for (maschera, _), v in sorted(ris['per_nome'].items()):
            d = MS._destinazione(v) or MS.per_convenzione(ris, v['campo_dto']) or {}
            diz.append({
                'area': area, 'maschera': maschera, 'etichetta': v['etichetta'],
                'campo_dto': v['campo_dto'],
                'certezza_etichetta': v['certezza_etichetta'],
                'tabella': d.get('tabella', ''), 'colonna': d.get('colonna', ''),
                'percorso_xml': d.get('percorso_xml', ''), 'tipo_java': d.get('tipo_java', ''),
                'genere': d.get('genere', ''), 'motivo': d.get('motivo', ''),
                'evidenza_maschera': v['evidenza_maschera'],
                'evidenza_salvataggio': d.get('evidenza', ''),
                'collegato': si_no((maschera, v['campo_dto']) in collegate),
            })
    foglio(wb, 'Dizionario SIPO', [
        ('Area', 12, 'area'), ('Maschera', 20, 'maschera'),
        ('Etichetta', 34, 'etichetta'), ('Proprietà del DTO', 30, 'campo_dto'),
        ('TABELLA', 24, 'tabella'), ('COLONNA', 28, 'colonna'),
        ('Percorso XML', 40, 'percorso_xml'), ('Tipo in SIPO', 14, 'tipo_java'),
        ('Grado di accertamento', 18, 'genere'),
        ('Etichetta appaiata per', 16, 'certezza_etichetta'),
        ('Collegato a un campo ANSC', 12, 'collegato'),
        ('Evidenza (maschera)', 42, 'evidenza_maschera'),
        ('Evidenza (salvataggio)', 42, 'evidenza_salvataggio'),
        ('Perché non risolto', 46, 'motivo'),
    ], diz, evidenzia=lambda d: (GIALLO if d['collegato'] != 'Sì' and d['colonna'] else None))

    # ---------------------------------------------------------------- Legenda
    ws = wb.create_sheet('Legenda', 0)
    ws.column_dimensions['A'].width = 46
    ws.column_dimensions['B'].width = 96

    def riga(a, b='', testa=False):
        # in streaming la cella si stila PRIMA di appenderla: non si torna indietro
        c1, c2 = WriteOnlyCell(ws, value=a), WriteOnlyCell(ws, value=b)
        c1.font = Font(bold=True, size=11 if testa else 9,
                       color='1F3864' if testa else '000000')
        c1.alignment = Alignment(vertical='top', wrap_text=True)
        c2.alignment = Alignment(vertical='top', wrap_text=True)
        c2.font = Font(size=9)
        if testa:
            c1.fill = GRIGIO
            c2.fill = GRIGIO
        ws.append([c1, c2])

    n_perc = len({r['percorso'] for r in campi})
    n_sipo_perc = len({r['percorso'] for r in campi if r['sipo_campo']})
    n_nr = len(nr)
    n_col = sum(1 for r in campi if r.get('sipo_colonna'))
    n_acc = sum(1 for r in campi if r.get('sipo_genere') in ('colonna', 'xml'))
    n_xml = sum(1 for r in campi if r.get('sipo_genere') == 'xml')
    n_conv = sum(1 for r in campi if r.get('conversione_richiesta') == 'Sì')
    riga('Mappatura dei campi ANSC ↔ SIPO', 'Integrazione SIPO → ANSC · Roma Capitale', True)
    riga('Che cos’è',
         'Per ciascun caso d’uso di ANSC: i campi che il caso d’uso richiede, il punto in cui '
         'stanno nel modello evento, il campo corrispondente nel DB di SIPO e la conversione '
         'necessaria. È la forma di lavoro delle tabelle ANSC_CFG_CAMPO e ANSC_CFG_ALLEGATO.')
    riga('Come si aggiorna',
         'Si rigenera con «Documenti finali/strumenti/workbook_mappatura.py». Non si corregge a '
         'mano: quando ANSC pubblica una revisione del mapping la correzione manuale andrebbe '
         'persa. Il lato SIPO non si scrive a mano nemmeno la prima volta — si ricava dal '
         'codice, e dove il codice non lo dice la casella resta vuota con la ragione accanto.')
    riga('Come si ricava il campo del DB', '', True)
    riga('La catena',
         'La ricognizione funzionale nomina i campi con l’ETICHETTA della maschera; la '
         'configurazione ha bisogno della COLONNA. Il legame non sta in nessun documento, sta '
         'nel codice: etichetta (messages.properties) → campo del form (th:field nel template '
         'della maschera dichiarata dalla ricognizione) → proprietà del DTO → assegnazione nel '
         'controller di salvataggio → @Column dell’entity → COLONNA. Ogni riga porta le '
         'evidenze file:riga dei due anelli verificabili.')
    riga('Grado di accertamento',
         '«colonna» = la catena arriva a una colonna vera. «xml» = il dato non è una colonna ma '
         'un nodo dentro un XMLType (vedi sotto). «convenzione» = la colonna è PROPOSTA perché '
         'porta lo stesso nome della proprietà, e va confermata: succede dove la persistenza '
         'passa da un ModelMapper (nascite) e le assegnazioni non sono leggibili.')
    riga('Via di risoluzione',
         'Dice come si è appaiata l’etichetta: nella maschera dichiarata (evidenza piena), per '
         'nome del campo (vale per i campi nascosti), per qualificatore fra parentesi («Data '
         'Atto (Ora)»), o in un’altra maschera della stessa area (analogia: da guardare).')
    riga('⚠️ Il dato dentro l’XML',
         f'{n_xml} righe non hanno una colonna: stanno in SOGGETTO.DETTAGLIO_STATOCIVILE, che è '
         'un XMLType. Cittadinanza, stato civile, residenza, luogo di nascita e perfino un '
         'contenitore generico EXTRAFIELDS/FIELD vivono lì dentro. Per l’adattatore non è un '
         'dettaglio: quei valori si leggono con XPath e possono mancare nel documento.')
    riga('⚠️ I campi della numerazione',
         'numeroatto, anno, parte, serie ed esponente sono <input hidden>: non li scrive '
         'l’operatore, li assegna il flusso di numerazione. È il dato che ANSC chiede come '
         'evento.numeroatto, ed è il punto su cui insiste OP-44 (allocazione in concorrenza).')
    riga('I fogli', '', True)
    riga('Percorsi',
         f'IL FOGLIO DI LAVORO: {len(percorsi)} righe (famiglia × percorso), {n_perc} percorsi '
         'distinti. Verde = colonna accertata; giallo = manca il lato SIPO; rosso = il percorso '
         'non esiste nel modello evento.')
    riga('Mappatura', f'{len(campi)} righe: il fabbisogno riga per riga (UC × campo) con il '
                      'lato SIPO e la conversione. È ciò che alimenta ANSC_CFG_CAMPO.')
    riga('Allegati', f'{len(allegati)} righe: gli allegati richiesti per UC, con il codice '
                     'ANSC_09 raccordato per descrizione normalizzata. In rosso le descrizioni '
                     'senza corrispondenza → OP-50.')
    riga('Formule', f'{len(formule)} righe: le formule ministeriali dichiarate per UC. Oggi non '
                    'sono configurate e ANSC non ne pubblica il catalogo → OP-51.')
    riga("Casi d'uso", f'{len(per_uc)} UC con i rispettivi numeri e la copertura del lato SIPO.')
    riga('Non risolti', f'{n_nr} percorsi che il modello evento non conosce, per '
                        f'{sum(a["occorrenze"] for a in nr.values())} occorrenze → OP-52. '
                        'Si riportano, non si scartano: una configurazione che li ignora '
                        'sembra completa e non lo è.')
    riga('Dizionario SIPO',
         f'{len(diz)} campi delle maschere di Decessi e Nascite con la loro colonna: è la mappa '
         'che nessun documento del sistema contiene, e serve anche fuori da ANSC. In giallo i '
         'campi che hanno una colonna ma che nessun campo ANSC richiede — l’altra metà del '
         'divario, utile quanto la prima.')
    riga('Che cosa è già risolto', '', True)
    riga('Campi con il DB individuato',
         f'{n_col} righe su {len(campi)}, di cui {n_acc} accertate sulla catena del codice e '
         f'{n_col - n_acc} proposte per convenzione dei nomi.')
    riga('Conversione richiesta',
         f'{n_conv} righe la richiedono: traduzione di codifica verso i dizionari ANSC, '
         'traduzione territoriale verso i codici ANPR, estrazione da XML, formati di data, '
         'contrassegni S/N, scomposizione di un campo unico in due.')
    riga('Aree coperte',
         'Decessi (pilota) e Nascite: sono le due per cui esiste una ricognizione funzionale. '
         'Per le altre cinque famiglie le colonne del lato SIPO restano vuote — non è una '
         'lacuna del generatore, è lavoro non ancora fatto.')
    riga('Che cosa resta', '', True)
    riga('Colonna SIPO', f'{n_sipo_perc} percorsi su {n_perc} hanno un riscontro nella '
                         f'ricognizione: ne restano {n_perc - n_sipo_perc} da rilevare.')
    riga('Allegati senza codice',
         f'{len({r["campo"] for r in allegati if not r["allegato_codice"]})} descrizioni su '
         f'{len({r["campo"] for r in allegati})} da raccordare a mano, una volta sola (OP-50).')
    riga('Regole di determinazione',
         f'{len(per_uc)} regole circa, da scrivere: sono poche e richiedono giudizio, mentre i '
         'campi si importano.')
    riga('Percorsi non risolti', f'{n_nr} da chiarire con il fornitore prima di configurare le '
                                 'famiglie interessate (OP-52).')

    wb.save(percorso)
    return percorso, {
        'dizionario_sipo': len(diz),
        'campi_sipo_non_collegati': sum(1 for d in diz if d['collegato'] != 'Sì'),
        'con_colonna': sum(1 for r in campi if r.get('sipo_colonna')),
        'colonna_accertata': sum(1 for r in campi
                                 if r.get('sipo_genere') in ('colonna', 'xml')),
        'percorsi': len(percorsi), 'campi': len(campi), 'allegati': len(allegati),
        'formule': len(formule), 'uc': len(per_uc), 'non_risolti': n_nr,
        'percorsi_distinti': n_perc, 'con_sipo': n_sipo_perc,
    }


if __name__ == '__main__':
    p, n = costruisci(sys.argv[1] if len(sys.argv) > 1 else USCITA)
    print(p)
    for k, v in n.items():
        print(f'  {k:20} {v}')
