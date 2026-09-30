# -*- coding: utf-8 -*-
"""Importa il catalogo degli UC (ANSC_USR.ANSC_UC) combinando le due sorgenti.

    /usr/bin/python3 "Documenti finali/importa-catalogo-uc.py" [--sql catalogo-uc.sql]

Le sorgenti sono due e nessuna basta da sola:

  1. la decodifica ufficiale ANSC_03 (ansc/docs/Decodifiche/3_dec_use_case.csv), che e'
     autoritativa per codice, descrizione e validita' ma NON pubblica il codice motore;
  2. la ricognizione del Comune (Sorgenti Documentali/Nascite_ANSC_*.xlsx, foglio «Sintesi»),
     che riprende ANSC_03 e vi aggiunge METADATI = codice motore, CATEGORIA e lo stato del
     mapping.

Il codice motore e' la chiave che apre i file di mappatura dei campi
(ansc/docs/Mapping_casi_uso/<famiglia>/<motore>.csv): senza di esso il catalogo non porta ai
campi obbligatori, che sono la ragione per cui il catalogo esiste.

Lo script NON si limita a convertire: riconcilia le due sorgenti e segnala le discordanze.
Esce con codice 1 se ne trova di bloccanti.
"""
import argparse
import csv
import glob
import os
import re
import sys
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECODIFICA = os.path.join(BASE, 'ansc', 'docs', 'Decodifiche', '3_dec_use_case.csv')
MAPPING = os.path.join(BASE, 'ansc', 'docs', 'Mapping_casi_uso')
SORGENTI = os.path.join(BASE, 'Sorgenti Documentali')

# la famiglia si deduce dalla cartella del mapping in cui vive il codice motore
FAMIGLIE = ['morte', 'nascita', 'riconoscimenti', 'matrimoni', 'unioni_civili',
            'cittadinanza', 'trascrizioni']


def norm(s):
    """Normalizza una descrizione per il confronto: spazi, accenti, maiuscole."""
    s = unicodedata.normalize('NFKD', (s or '').strip().lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', s)


def sql_str(v):
    if v is None or v == '':
        return 'NULL'
    return "'" + str(v).replace("'", "''") + "'"


def sql_data(v):
    """'2022-01-01 00:00:00.0' -> DATE '2022-01-01'."""
    if not v:
        return 'NULL'
    m = re.match(r'(\d{4}-\d{2}-\d{2})', str(v))
    return "DATE '%s'" % m.group(1) if m else 'NULL'


# ------------------------------------------------------------------ sorgente 1
def leggi_decodifica():
    if not os.path.exists(DECODIFICA):
        return None
    with open(DECODIFICA, encoding='utf-8-sig', errors='replace') as f:
        return {r['ID'].strip(): r for r in csv.DictReader(f) if r.get('ID')}


# ------------------------------------------------------------------ sorgente 2
def leggi_ricognizioni():
    """Legge il foglio «Sintesi» di tutte le ricognizioni presenti."""
    try:
        import openpyxl
    except ImportError:
        sys.exit('openpyxl non disponibile: serve per leggere le ricognizioni .xlsx')
    files = [f for f in glob.glob(os.path.join(SORGENTI, '*_ANSC_*.xlsx'))
             if not os.path.basename(f).startswith('~$')]
    voci, provenienza = {}, {}
    for f in sorted(files):
        wb = openpyxl.load_workbook(f, data_only=True)
        if 'Sintesi' not in wb.sheetnames:
            continue
        ws = wb['Sintesi']
        intest = [str(ws.cell(row=1, column=c).value or '').strip().upper()
                  for c in range(1, ws.max_column + 1)]
        try:
            col = {k: intest.index(k) + 1 for k in
                   ('ID', 'DESCRIZIONE', 'DATAINIZIOVALIDITA', 'DATAFINEVALIDITA',
                    'IDTIPOCONTENUTO', 'CATEGORIA', 'METADATI')}
        except ValueError:
            continue
        for r in range(2, ws.max_row + 1):
            cod = ws.cell(row=r, column=col['ID']).value
            if cod is None:
                continue
            cod = str(cod).strip()
            voci[cod] = {
                'cod': cod,
                'descrizione': str(ws.cell(row=r, column=col['DESCRIZIONE']).value or '').strip(),
                'da': ws.cell(row=r, column=col['DATAINIZIOVALIDITA']).value,
                'a': ws.cell(row=r, column=col['DATAFINEVALIDITA']).value,
                'tipocontenuto': ws.cell(row=r, column=col['IDTIPOCONTENUTO']).value,
                'categoria': str(ws.cell(row=r, column=col['CATEGORIA']).value or '').strip(),
                'motore': str(ws.cell(row=r, column=col['METADATI']).value or '').strip(),
            }
            provenienza[cod] = os.path.basename(f)
    return voci, provenienza


# ------------------------------------------------------------------ sorgente 3
def indice_mapping():
    """codice motore -> famiglia, per i mapping effettivamente presenti."""
    idx = {}
    for fam in FAMIGLIE:
        for f in glob.glob(os.path.join(MAPPING, fam, '*.csv')):
            idx[os.path.splitext(os.path.basename(f))[0]] = fam
    return idx


# ------------------------------------------------------------------ riconciliazione
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sql', help='file in cui scrivere gli INSERT (altrimenti su schermo)')
    ap.add_argument('--versione', default='v.13', help='versione di mapping da registrare')
    args = ap.parse_args()

    deco = leggi_decodifica()
    voci, provenienza = leggi_ricognizioni()
    mapping = indice_mapping()

    if deco is None:
        print('AVVISO: decodifica ANSC_03 non trovata; nessuna riconciliazione possibile.')
    if not voci:
        sys.exit('Nessuna ricognizione con foglio «Sintesi» trovata in Sorgenti Documentali/.')

    print('SORGENTI')
    print('  decodifica ANSC_03 : %s UC' % (len(deco) if deco else '—'))
    print('  ricognizioni       : %s UC (%s)' % (
        len(voci), ', '.join(sorted(set(provenienza.values())))))
    print('  mapping presenti   : %s codici motore' % len(mapping))

    bloccanti, avvisi, righe = [], [], []
    motori_visti = {}

    for cod in sorted(voci):
        v = voci[cod]

        # (a) l'UC deve esistere nella decodifica ufficiale
        if deco is not None and cod not in deco:
            bloccanti.append('UC %s non esiste nella decodifica ANSC_03 (%s)'
                             % (cod, provenienza[cod]))
            continue

        # (b) il codice motore e' indispensabile e deve essere univoco
        if not v['motore']:
            bloccanti.append('UC %s senza codice motore nella ricognizione' % cod)
            continue
        if v['motore'] in motori_visti:
            bloccanti.append('codice motore %s usato da piu\' UC: %s e %s'
                             % (v['motore'], motori_visti[v['motore']], cod))
            continue
        motori_visti[v['motore']] = cod

        # (c) la descrizione deve concordare con quella ufficiale
        if deco is not None:
            uff = deco[cod].get('DESCRIZIONE', '')
            if norm(uff) != norm(v['descrizione']):
                avvisi.append('UC %s: descrizione difforme\n        ANSC : %s\n        ricogn.: %s'
                              % (cod, uff.strip(), v['descrizione']))

        # (d) il mapping dei campi deve esistere, altrimenti il catalogo non porta ai campi
        famiglia = mapping.get(v['motore'])
        if famiglia is None:
            avvisi.append('UC %s (%s): nessun file di mappatura in Mapping_casi_uso/'
                          % (cod, v['motore']))
            famiglia = (v['categoria'] or 'DA_DEFINIRE').upper()

        # la validita' si prende dalla fonte autoritativa quando c'e'
        da = (deco[cod]['DATAINIZIOVALIDITA'] if deco is not None else v['da'])
        a = (deco[cod]['DATAFINEVALIDITA'] if deco is not None else v['a'])

        righe.append({
            'cod': cod, 'motore': v['motore'],
            'descrizione': (deco[cod]['DESCRIZIONE'].strip() if deco is not None
                            else v['descrizione']),
            'famiglia': famiglia.upper(),
            'categoria': v['categoria'],
            'da': da, 'a': a,
        })

    # UC della decodifica non coperti da alcuna ricognizione: informativo
    if deco is not None:
        scoperti = sorted(set(deco) - set(voci))
    else:
        scoperti = []

    print('\nRICONCILIAZIONE')
    print('  UC pronti per il carico : %d' % len(righe))
    print('  discordanze bloccanti   : %d' % len(bloccanti))
    print('  avvisi                  : %d' % len(avvisi))
    print('  UC ANSC ancora scoperti : %d (nessuna ricognizione li mappa)' % len(scoperti))

    for b in bloccanti:
        print('  BLOCCANTE  ' + b)
    for a in avvisi[:20]:
        print('  avviso     ' + a)
    if len(avvisi) > 20:
        print('  avviso     … altri %d' % (len(avvisi) - 20))

    # ---------------------------------------------------------------- SQL
    out = []
    out.append('-- Catalogo degli UC — generato da importa-catalogo-uc.py')
    out.append('-- Sorgenti: decodifica ANSC_03 (autoritativa) + ricognizioni del Comune')
    out.append('--           (codice motore, che ANSC non pubblica nella decodifica).')
    out.append('-- Rieseguibile: la MERGE aggiorna le righe esistenti e inserisce le nuove.')
    out.append('')
    for r in righe:
        out.append(
            "MERGE INTO ANSC_USR.ANSC_UC d\n"
            "USING (SELECT %s AS COD_UC_ANSC, %s AS COD_MOTORE, %s AS DESCRIZIONE,\n"
            "              %s AS COD_FAMIGLIA, %s AS COD_CATEGORIA,\n"
            "              %s AS DATA_INIZIO_VALIDITA, %s AS DATA_FINE_VALIDITA,\n"
            "              %s AS COD_VERSIONE_MAPPING FROM dual) s\n"
            "ON (d.COD_UC_ANSC = s.COD_UC_ANSC)\n"
            "WHEN MATCHED THEN UPDATE SET\n"
            "  d.COD_MOTORE = s.COD_MOTORE, d.DESCRIZIONE = s.DESCRIZIONE,\n"
            "  d.COD_FAMIGLIA = s.COD_FAMIGLIA, d.COD_CATEGORIA = s.COD_CATEGORIA,\n"
            "  d.DATA_INIZIO_VALIDITA = s.DATA_INIZIO_VALIDITA,\n"
            "  d.DATA_FINE_VALIDITA = s.DATA_FINE_VALIDITA,\n"
            "  d.COD_VERSIONE_MAPPING = s.COD_VERSIONE_MAPPING,\n"
            "  d.DATA_UPD = SYSTIMESTAMP, d.UTENTE_UPD = USER\n"
            "WHEN NOT MATCHED THEN INSERT\n"
            "  (COD_UC_ANSC, COD_MOTORE, DESCRIZIONE, COD_FAMIGLIA, COD_CATEGORIA,\n"
            "   DATA_INIZIO_VALIDITA, DATA_FINE_VALIDITA, COD_VERSIONE_MAPPING, UTENTE_INS)\n"
            "  VALUES (s.COD_UC_ANSC, s.COD_MOTORE, s.DESCRIZIONE, s.COD_FAMIGLIA,\n"
            "          s.COD_CATEGORIA, s.DATA_INIZIO_VALIDITA, s.DATA_FINE_VALIDITA,\n"
            "          s.COD_VERSIONE_MAPPING, USER);"
            % (sql_str(r['cod']), sql_str(r['motore']), sql_str(r['descrizione']),
               sql_str(r['famiglia']), sql_str(r['categoria']),
               sql_data(r['da']), sql_data(r['a']), sql_str(args.versione)))
    out.append('')
    out.append('COMMIT;')
    testo = '\n'.join(out)

    if args.sql:
        dest = args.sql if os.path.isabs(args.sql) else os.path.join(BASE, 'Documenti finali',
                                                                     args.sql)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(testo + '\n')
        print('\nSQL scritto in: %s (%d istruzioni MERGE)' % (dest, len(righe)))
    else:
        print('\n--- SQL (prime 2 istruzioni) ---')
        print('\n'.join(testo.split('\n')[:26]))
        print('… usare --sql per scrivere il file completo')

    return 1 if bloccanti else 0


if __name__ == '__main__':
    sys.exit(main())
