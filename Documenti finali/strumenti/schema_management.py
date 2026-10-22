# -*- coding: utf-8 -*-
"""Lettura delle DDL PostgreSQL dello schema «management» (roma-capitale-management, L4).

Fonte: Sorgenti Documentali/management-schema.sql — l'estrazione della sola struttura dello
schema in esercizio (24 tabelle, 8 sequenze, nessun dato). Il file è nel formato di DBeaver:
ogni CREATE TABLE sta su una riga sola, i commenti seguono la tabella.

leggi() restituisce le tabelle con colonne, tipi, obbligatorietà, valori predefiniti, vincoli
e commenti, e le sequenze: è la base unica da cui il generatore della versione dell'analisi
ricava sia le tabelle descrittive sia la DDL per Oracle.
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQL = os.path.join(BASE, 'Sorgenti Documentali', 'management-schema.sql')


def _spezza(s):
    """Divide per virgola al livello zero delle parentesi."""
    out, liv, cur = [], 0, ''
    for ch in s:
        if ch == '(':
            liv += 1
        elif ch == ')':
            liv -= 1
        if ch == ',' and liv == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def _colonne(lista):
    return [c.strip() for c in lista.split(',')]


def leggi(percorso=SQL):
    testo = open(percorso, encoding='utf-8').read()
    seq = {}
    for m in re.finditer(r'CREATE SEQUENCE management\.(\w+)(.*?)NO CYCLE;', testo, re.S):
        start = int(re.search(r'START (\d+)', m.group(2)).group(1))
        seq[m.group(1)] = start
    tabelle = {}
    for m in re.finditer(r'CREATE TABLE management\.(\w+) \((.*)\);\s*$', testo, re.M):
        nome, corpo = m.group(1), m.group(2)
        t = dict(nome=nome, col=[], pk=None, pk_nome=None, uk=[], fk=[], commento=None)
        for voce in _spezza(corpo):
            if voce.startswith('CONSTRAINT'):
                cm = re.match(r'CONSTRAINT (\w+) (PRIMARY KEY|UNIQUE|FOREIGN KEY) \(([^)]*)\)'
                              r'(?: REFERENCES management\.(\w+)\(([^)]*)\))?', voce)
                cn, tipo, cc, rif, rc = cm.groups()
                if tipo == 'PRIMARY KEY':
                    t['pk'], t['pk_nome'] = _colonne(cc), cn
                elif tipo == 'UNIQUE':
                    t['uk'].append((cn, _colonne(cc), 'vincolo'))
                else:
                    t['fk'].append((cn, _colonne(cc), rif, _colonne(rc)))
                continue
            cm = re.match(r'(\w+) (\w+(?:\(\d+\))?)( DEFAULT (.+?))?( NOT NULL| NULL)$', voce)
            assert cm, voce
            t['col'].append(dict(nome=cm.group(1), tipo=cm.group(2), default=cm.group(4),
                                 obbl=cm.group(5).strip() == 'NOT NULL', commento=None))
        tabelle[nome] = t
    for m in re.finditer(r'CREATE UNIQUE INDEX (\w+) ON management\.(\w+) USING btree '
                         r'\(([^)]*)\);', testo):
        tabelle[m.group(2)]['uk'].append((m.group(1), _colonne(m.group(3)), 'indice'))
    for m in re.finditer(r"COMMENT ON TABLE management\.(\w+) IS '((?:[^']|'')*)';", testo):
        tabelle[m.group(1)]['commento'] = m.group(2).replace("''", "'")
    for m in re.finditer(r"COMMENT ON COLUMN management\.(\w+)\.(\w+) IS '((?:[^']|'')*)';",
                         testo):
        for c in tabelle[m.group(1)]['col']:
            if c['nome'] == m.group(2):
                c['commento'] = m.group(3).replace("''", "'")
    return tabelle, seq


if __name__ == '__main__':
    tab, seq = leggi()
    print(len(tab), 'tabelle,', len(seq), 'sequenze')
    print(sum(len(t['fk']) for t in tab.values()), 'chiavi esterne,',
          sum(len(t['uk']) for t in tab.values()), 'unicità')
    for t in tab.values():
        print(f"  {t['nome']:34} col {len(t['col']):2}  pk {t['pk']}  fk {len(t['fk'])}")
