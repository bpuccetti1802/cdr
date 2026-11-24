# -*- coding: utf-8 -*-
"""Confronto fra gli script della base dati degli sviluppatori e il documento di analisi.

Legge la cartella degli script (CREATE, poi ALTER, nell'ordine) e, dal .docx, la DDL
dell'Appendice A (paragrafi in Courier New) e le tabelle descrittive «Colonna | Tipo | …».
Per ogni tabella confronta colonne, tipi, chiave primaria e chiavi esterne; scrive un
rapporto .xlsx e stampa la sintesi.

    python3 strumenti/verifica_ddl.py <cartella script> <analisi.docx> <rapporto.xlsx>

Le righe commentate (--) degli script sono ignorate. Il nome di tabella si confronta
senza schema e senza apici; lo schema dichiarato è riportato a parte.
"""
import os
import re
import sys

import docx
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

PAROLE_CHIUSE = ('CONSTRAINT', 'PRIMARY', 'FOREIGN', 'UNIQUE', 'CHECK', 'SUPPLEMENTAL')
TIPI = (r'NUMBER|VARCHAR2|NVARCHAR2|VARCHAR|CHAR|NCHAR|DATE|TIMESTAMP|CLOB|NCLOB|BLOB|'
        r'INTEGER|FLOAT|RAW|LONG|XMLTYPE|BOOLEAN')


def senza_commenti(s):
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    return '\n'.join(l.split('--')[0] if not l.strip().startswith('--') else ''
                     for l in s.splitlines())


def nome(x):
    x = x.replace('"', '').strip()
    return x.split('.')[-1].upper(), (x.split('.')[0].upper() if '.' in x else '')


def blocco(s, i):
    """Restituisce il contenuto fra la parentesi aperta in posizione i e la sua chiusa."""
    liv = 0
    for j in range(i, len(s)):
        if s[j] == '(':
            liv += 1
        elif s[j] == ')':
            liv -= 1
            if liv == 0:
                return s[i + 1:j], j
    return s[i + 1:], len(s)   # parentesi sbilanciate: si prende tutto, e lo si segnala


def spezza(s):
    out, liv, cur = [], 0, ''
    for ch in s:
        if ch == '(':
            liv += 1
        elif ch == ')':
            liv -= 1
        if ch == ',' and liv == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def tipo_di(resto):
    resto = re.sub(r'\s+', ' ', resto).upper()
    resto = re.sub(r'\s*\(\s*', '(', resto)
    resto = re.sub(r'\s*\)', ')', resto)
    resto = re.sub(r'\s*,\s*', ',', resto)
    m = re.match(r'(TIMESTAMP(\(\d+\))?( WITH (LOCAL )?TIME ZONE)?|[A-Z0-9_]+(\([^)]*\))?)', resto)
    t = m.group(1) if m else resto.split(' ')[0]
    t = t.replace(' CHAR)', ')').replace(' BYTE)', ')').replace('(6)', '') \
        if t.startswith('TIMESTAMP') else t.replace(' CHAR)', ')').replace(' BYTE)', ')')
    t = re.sub(r'\((\d+) ?(CHAR|BYTE)\)', r'(\1)', t)
    t = re.sub(r'^NUMBER\((\d+),0\)$', r'NUMBER(\1)', t)
    return t


def analizza(sql, origine):
    sql = senza_commenti(sql)
    tab = {}
    # Lettura tollerante: l'istruzione arriva fino al primo «;»; le colonne si riconoscono
    # riga per riga (nome seguito da un tipo Oracle), così una parentesi mancante non fa
    # sconfinare la lettura nell'istruzione successiva. Lo sbilanciamento si segnala.
    for m in re.finditer(r'CREATE\s+TABLE\s+([\w\."$#]+)\s*\(', sql, re.I):
        n, sch = nome(m.group(1))
        fine = sql.find(';', m.end())
        fine = len(sql) if fine < 0 else fine
        corpo = sql[m.end():fine]
        t = tab.setdefault(n, {'schema': sch, 'col': {}, 'pk': '', 'fk': [], 'uk': [],
                               'origine': origine, 'note': []})
        bil = 1 + corpo.count('(') - corpo.count(')')
        if bil != 0:
            t['note'].append('parentesi sbilanciate (%+d)' % bil)
        righe = []
        for v in corpo.split('\n'):
            v = v.strip()
            if not v:
                continue
            nuova = (re.match(r'"?\w+"?\s+(' + TIPI + r')\b', v, re.I)
                     or v.split()[0].upper().replace('"', '') in PAROLE_CHIUSE)
            if righe and not nuova:
                righe[-1] += ' ' + v          # riga di continuazione
            else:
                righe.append(v)
        for v in righe:
            v = v.rstrip(',').strip()
            testa = v.split()[0].upper().replace('"', '')
            if testa in PAROLE_CHIUSE:
                vincolo(t, v)
                continue
            mc = re.match(r'"?(\w+)"?\s+(' + TIPI + r')\b(.*)', v, re.I)
            if not mc:
                continue
            col = mc.group(1).upper()
            resto = mc.group(2) + mc.group(3)
            t['col'][col] = {'tipo': tipo_di(resto),
                             'nn': bool(re.search(r'NOT\s+NULL', resto, re.I))}
            if re.search(r'PRIMARY\s+KEY', resto, re.I):
                t['pk'] = col
            for c in re.findall(r'CONSTRAINT\s+.*', resto, re.I):
                vincolo(t, c)
    for m in re.finditer(r'ALTER\s+TABLE\s+([\w\."$#]+)\s+ADD\s+(.+?);', sql, re.I | re.S):
        n, _ = nome(m.group(1))
        t = tab.get(n)
        resto = m.group(2).strip()
        if t is None:
            tab[n] = t = {'schema': '', 'col': {}, 'pk': '', 'fk': [], 'uk': [],
                          'origine': origine + ' (solo ALTER)', 'note': []}
        if re.match(r'(CONSTRAINT|PRIMARY|FOREIGN|UNIQUE|CHECK)\b', resto, re.I):
            vincolo(t, resto)
        else:
            if resto.startswith('('):
                resto = blocco(resto, 0)[0]
            for v in spezza(resto):
                parti = v.replace('"', '').split(None, 1)
                if len(parti) == 2:
                    t['col'][parti[0].upper()] = {'tipo': tipo_di(parti[1]), 'nn': False,
                                                  'alter': True}
    for m in re.finditer(r'CREATE\s+(OR\s+REPLACE\s+)?TRIGGER\s+([\w\."$#]+).*?\bON\s+([\w\."$#]+)',
                         sql, re.I | re.S):
        n, _ = nome(m.group(3))
        tab.setdefault('#TRIGGER', {'schema': '', 'col': {}, 'pk': '', 'fk': [], 'uk': [],
                                    'origine': origine, 'note': []})['note'].append(
            '%s su %s' % (m.group(2), m.group(3)))
    return tab


def vincolo(t, v):
    u = re.sub(r'\s+', ' ', v.replace('"', '')).upper()
    nomev = re.match(r'CONSTRAINT (\S+)', u)
    nomev = nomev.group(1) if nomev else ''
    m = re.search(r'PRIMARY KEY ?\(([^)]*)\)', u)
    if m:
        t['pk'] = ','.join(x.strip() for x in m.group(1).split(','))
        t['pk_nome'] = nomev
    m = re.search(r'FOREIGN KEY ?\(([^)]*)\) ?REFERENCES ([\w\.$#]+) ?(\(([^)]*)\))?', u)
    if m:
        t['fk'].append('%s -> %s(%s)' % (m.group(1).replace(' ', ''), m.group(2),
                                         (m.group(4) or 'PK').replace(' ', '')))
    m = re.search(r'UNIQUE ?\(([^)]*)\)', u)
    if m:
        t['uk'].append(m.group(1).replace(' ', ''))


def leggi_cartella(cart):
    sql = {}
    ordine = []
    for sotto in ('TABELLE - CREAZIONE', 'TABELLE - ALTER', 'TRIGGER'):
        p = os.path.join(cart, sotto)
        if not os.path.isdir(p):
            continue
        for f in sorted(os.listdir(p)):
            if f.upper().endswith('.SQL'):
                ordine.append(os.path.join(sotto, f))
    tab = {}
    for rel in ordine:
        s = open(os.path.join(cart, rel), encoding='utf-8', errors='replace').read()
        for n, t in analizza(s, rel).items():
            if n in tab and n != '#TRIGGER':
                tab[n]['col'].update(t['col'])
                tab[n]['fk'] += t['fk']
                tab[n]['uk'] += t['uk']
                tab[n]['pk'] = tab[n]['pk'] or t['pk']
                tab[n]['origine'] += ' + ' + rel
            elif n == '#TRIGGER' and n in tab:
                tab[n]['note'] += t['note']
            else:
                tab[n] = t
    return tab


def leggi_docx(path):
    d = docx.Document(path)
    righe = [p.text for p in d.paragraphs
             if any(r.font.name == 'Courier New' for r in p.runs)]
    ddl = analizza('\n'.join(righe), 'App. A')
    descr = []
    for i, t in enumerate(d.tables):
        h = [c.text.strip() for c in t.rows[0].cells]
        if len(h) >= 2 and h[0] == 'Colonna' and h[1] == 'Tipo':
            cols = {}
            for r in t.rows[1:]:
                c = r.cells[0].text.strip().split()[0].upper() if r.cells[0].text.strip() else ''
                if c:
                    cols[c] = tipo_di(r.cells[1].text) if r.cells[1].text.strip() else ''
            descr.append((i, cols))
    return ddl, descr


def assegna(descr, universo):
    """Una tabella descrittiva non porta il nome della tabella: la si attribuisce per
    massima sovrapposizione di colonne."""
    ris = {}
    for i, cols in descr:
        best, sc = None, 0
        for n, t in universo.items():
            s = len(set(cols) & set(t['col']))
            if s > sc:
                best, sc = n, s
        ris.setdefault(best or '?', []).append((i, cols, sc))
    return ris


def main(cart, path_docx, out):
    db = leggi_cartella(cart)
    ddl, descr = leggi_docx(path_docx)
    trig = db.pop('#TRIGGER', None)
    ddl.pop('#TRIGGER', None)
    universo = dict(ddl)
    for n, t in db.items():
        universo.setdefault(n, t)
    desc_per = assegna(descr, universo)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Tabelle'
    ws.append(['Tabella', 'Negli script', 'File', 'Schema (script)', 'In App. A',
               'Schema (App. A)', 'Tabella descrittiva', 'Col. script', 'Col. App. A',
               'Solo script', 'Solo App. A', 'Tipi diversi', 'PK script', 'PK App. A',
               'FK script', 'FK App. A', 'Note'])
    wc = wb.create_sheet('Colonne')
    wc.append(['Tabella', 'Colonna', 'Script', 'App. A', 'Descrittiva', 'Esito'])
    sintesi = []
    for n in sorted(set(db) | set(ddl)):
        a, b = db.get(n), ddl.get(n)
        ca, cb = (a or {}).get('col', {}), (b or {}).get('col', {})
        dsc = desc_per.get(n, [])
        cd = dsc[0][1] if dsc else {}
        solo_a = sorted(set(ca) - set(cb)) if a and b else []
        solo_b = sorted(set(cb) - set(ca)) if a and b else []
        diversi = sorted(c for c in set(ca) & set(cb) if ca[c]['tipo'] != cb[c]['tipo'])
        note = list((a or {}).get('note', [])) + ['App. A: ' + x for x in (b or {}).get('note', [])]
        ws.append([n, 'sì' if a else 'NO', (a or {}).get('origine', ''), (a or {}).get('schema', ''),
                   'sì' if b else 'NO', (b or {}).get('schema', ''),
                   ', '.join('tab. %d' % (x[0] + 1) for x in dsc) or '—',
                   len(ca), len(cb), ', '.join(solo_a), ', '.join(solo_b),
                   ', '.join('%s %s≠%s' % (c, ca[c]['tipo'], cb[c]['tipo']) for c in diversi),
                   (a or {}).get('pk', ''), (b or {}).get('pk', ''),
                   '; '.join((a or {}).get('fk', [])), '; '.join((b or {}).get('fk', [])),
                   '; '.join(note)])
        for c in sorted(set(ca) | set(cb) | set(cd)):
            ta, tb = ca.get(c, {}).get('tipo', ''), cb.get(c, {}).get('tipo', '')
            td = cd.get(c)
            if not a:
                es = 'tabella assente dagli script'
            elif not b:
                es = 'tabella assente dall’App. A'
            elif ta and not tb:
                es = 'solo negli script'
            elif tb and not ta:
                es = 'solo nell’App. A'
            elif ta != tb:
                es = 'tipo diverso'
            else:
                es = 'uguale'
            if td is not None and not ta and a:
                es += ' · descrittiva non negli script'
            wc.append([n, c, ta, tb, '' if td is None else (td or '(senza tipo)'), es])
        sintesi.append((n, bool(a), bool(b), len(solo_a), len(solo_b), len(diversi)))
    wt = wb.create_sheet('Trigger')
    wt.append(['Trigger negli script'])
    for x in (trig or {}).get('note', []):
        wt.append([x])
    for s in wb.worksheets:
        for c in s[1]:
            c.font = Font(bold=True, color='FFFFFF')
            c.fill = PatternFill('solid', fgColor='8C0029')
            c.alignment = Alignment(wrap_text=True, vertical='top')
        s.freeze_panes = 'A2'
        s.auto_filter.ref = s.dimensions
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = 22
    wb.save(out)
    for n, a, b, x, y, z in sintesi:
        print('%-32s script:%-2s appA:%-2s solo_script:%-2d solo_appA:%-2d tipi≠:%d'
              % (n, 'sì' if a else 'NO', 'sì' if b else 'NO', x, y, z))
    print('trigger:', (trig or {}).get('note'))
    print('scritto', out)


if __name__ == '__main__':
    main(*sys.argv[1:4])
