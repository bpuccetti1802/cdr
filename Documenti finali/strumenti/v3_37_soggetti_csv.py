# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.36 → v3.37 (10/10/2026).

Si riporta il contenuto di `Sorgenti Documentali/Tabella SOGGETTI_USECASE.csv`, l'esportazione
della tabella compilata dal Comune di Milano (ricevuta il 10/10/2026), che risponde a buona
parte di OP-69. I numeri si CALCOLANO dal file, non si scrivono a mano (stessa funzione usata
per il verbale del back-office: `pagine_bo_v3.verbale_soggetti`).

Verificato sul file e sul corpus ANSC:
  * 1.167 righe, 278 UC, 0 chiavi duplicate; 277 UC nel catalogo ANSC_03, uno no (11413030);
  * per registro (UC in vigore nel catalogo): nascita 174/206, morte 13/26, matrimonio 27/45,
    unione civile 17/31, cittadinanza 47/65;
  * ty_soggetto = nome del blocco del modello evento in 941 righe su 1.167 (proprietà di primo
    livello: intestatari, interprete, madre, padre, dichiarante, coniuge, richiedente); le altre
    usano prefissi propri (m., uc., citt.) o nomi senza riscontro;
  * ty_presenza: O, C, F come per gli allegati, ma C senza numero, più CSTCIV, FO, C02 che
    nessuna fonte spiega; ty_configurazione: 60 codici di maschera di Side;
  * le note registrano i riallineamenti alle versioni di ANSC (1.27 … 1.48).

Si aggiunge [R14] = il disegno del back-office v0.8, che governa le due tabelle e il
caricamento da file.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_37_soggetti_csv.py
"""
import collections
import csv
import os
import shutil
import subprocess
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
import pagine_bo_v3 as P3   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.36.docx')
DST = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.37.docx')
M = P3.migl
PRIMO_LIVELLO = {'intestatari', 'interprete', 'madre', 'padre', 'dichiarante', 'coniuge',
                 'richiedente'}
REGISTRI = {'1': 'nascita', '2': 'morte', '3': 'matrimonio', '4': 'unione civile',
            '5': 'cittadinanza'}


def commenti(p):
    return int(subprocess.run(
        ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                       "grep -o '<w:comment ' | wc -l" % repr(p)],
        capture_output=True, text=True).stdout.strip() or 0)


def numeri():
    v = P3.verbale_soggetti()
    with open(P3.CSV_SOGG, encoding='utf-8') as f:
        righe = list(csv.DictReader(f))
    with open(P3.CATALOGO, encoding='utf-8-sig') as f:
        cat = list(csv.DictReader(f))
    validi = {r['ID'] for r in cat if r['DATAFINEVALIDITA'].startswith('9999')}
    uc = {r['cd_usecase'] for r in righe}
    per = collections.Counter(k[0] for k in uc)
    tot = collections.Counter(k[0] for k in validi)
    v['registri'] = '; '.join(f'{REGISTRI[k]} {per[k]} su {tot[k]}' for k in sorted(REGISTRI))
    v['diretti'] = sum(r['ty_soggetto'] in PRIMO_LIVELLO for r in righe)
    v['cd_soggetto'] = len({r['cd_soggetto'] for r in righe})
    v['ty_soggetto'] = len({r['ty_soggetto'] for r in righe})
    v['dich'] = sum(r['fg_dichiarante'] == '1' for r in righe)
    v['comp'] = sum(r['fg_comparente'] == '1' for r in righe)
    v['firma'] = sum(r['fg_firmatario'] == '1' for r in righe)
    return v


def main():
    if os.path.exists(DST):
        raise SystemExit(f'{os.path.basename(DST)} esiste già: non si sovrascrive')
    shutil.copy(SRC, DST)
    prima = commenti(DST)
    d = docx.Document(DST)
    v = numeri()
    p = v['presenza']
    fatti = []

    # ─────────────────────────── 1. le note delle colonne
    t = next(t for t in d.tables if t.rows[0].cells[0].text.strip() == 'Colonna'
             and any(r.cells[0].text.strip() == 'cd_soggetto' for r in t.rows))
    righe = {r.cells[0].text.strip(): r for r in t.rows}
    D.riscrivi_cella(righe['cd_soggetto'].cells[2],
                     f'Codice del soggetto nella nomenclatura di Side: {v["cd_soggetto"]} '
                     'valori nel file ricevuto, come PADRE, MADRE, INT_NAS, INTERPR, '
                     'COMPARENTE1. Non è il percorso del modello evento: quello sta nella '
                     'colonna seguente.')
    D.riscrivi_cella(righe['ty_soggetto'].cells[2],
                     f'Tipo del soggetto: {v["ty_soggetto"]} valori nel file. In '
                     f'{M(v["diretti"])} righe su {M(v["righe"])} coincide con la radice di un '
                     'blocco del modello evento (intestatari, interprete, madre, padre, '
                     'dichiarante, coniuge, richiedente); le altre usano prefissi propri di '
                     'Side — m. per il matrimonio, uc. per l’unione civile, citt. per la '
                     'cittadinanza — o nomi che nel modello non hanno riscontro. È il raccordo '
                     'con OGGETTO_ANSC di ANSC_CFG_SEZIONE.')
    D.riscrivi_cella(righe['ty_presenza'].cells[2],
                     f'Presenza richiesta. Nel file: O {p["O"]}, C {p["C"]}, F {p["F"]}, e tre '
                     f'valori che nessuna fonte spiega — CSTCIV {p["CSTCIV"]}, FO {p["FO"]}, '
                     f'C02 {p["C02"]}. Diversamente dagli allegati, C non porta il numero. '
                     '[DA VERIFICARE: la semantica dei tre valori e dove stia la condizione '
                     'di C (OP-69).]')
    D.riscrivi_cella(righe['ty_configurazione'].cells[2],
                     f'Codice della maschera con cui Side presenta il soggetto: '
                     f'{v["configurazioni"]} valori nel file, come BASE, BASESD, NASC01, '
                     'BASENOINT, PROCUR01. [DA VERIFICARE: le definizioni delle maschere non '
                     'sono fra le sorgenti (OP-69).]')
    fatti.append('note di cd_soggetto, ty_soggetto, ty_presenza, ty_configurazione dal file')

    # ─────────────────────────── 2. il contenuto ricevuto
    ancora = next(p_ for p_ in d.paragraphs
                  if p_.text.startswith('Le scelte di adozione sono quelle già fatte per '
                                        'ALLEGATI_USECASE'))
    D.para(d, ancora._p,
           f'Il Comune di Milano ha fornito anche il contenuto della tabella, come '
           f'esportazione [R12]: {M(v["righe"])} righe su {v["uc"]} casi d’uso, nessuna chiave '
           f'duplicata. Per registro, sui casi d’uso in vigore nel catalogo di ANSC: '
           f'{v["registri"]}. Un solo caso d’uso, {", ".join(v["fuori_catalogo"])}, non '
           f'compare nel catalogo pubblicato. I ruoli sono valorizzati: {v["dich"]} righe '
           f'dichiaranti, {v["comp"]} comparenti, {v["firma"]} firmatarie.')
    D.para(d, ancora._p,
           '⚠️ Il file conferma due scelte di questo documento e ne precisa una terza. '
           'Conferma che i ruoli sono lavoro di compilazione: Milano li ha scritti a mano, '
           'riga per riga. Conferma che la configurazione va versionata: le note registrano i '
           'riallineamenti alle versioni di ANSC, dalla 1.27 alla 1.48, perché la tabella di '
           'Side non ha altro modo di dire a quale pubblicazione corrisponda. Precisa il '
           'raccordo con le sezioni: ty_soggetto, e non cd_soggetto, è il nome del blocco del '
           'modello evento.')
    D.para(d, ancora._p,
           'Il disegno del back-office [R14] governa la tabella in una pagina propria e prevede '
           'il caricamento da file nel formato di questa esportazione: caricato in simulazione '
           'su una bozza vuota, il file non produce errori e dà tre avvisi — il caso d’uso '
           'assente dal catalogo, i valori di presenza non documentati e i codici di maschera '
           'senza catalogo.')
    fatti.append('tre paragrafi sul contenuto ricevuto')

    D.sostituisci(d, 'Va deciso quale delle due governi la presenza e come si raccordino le '
                     'righe, il che dipende dai valori di cd_soggetto (OP-69).',
                  'Va deciso quale delle due governi la presenza. Il raccordo delle righe è '
                  'invece in buona parte possibile: passa per ty_soggetto, che nel file di Side '
                  'coincide con il nome del blocco del modello evento in '
                  f'{M(v["diretti"])} righe su {M(v["righe"])} (OP-69).',
                  attese=1, fatti=fatti, etichetta='sovrapposizione: il raccordo via ty_soggetto')
    D.sostituisci(d, 'e il contenuto della tabella per gli UC che Milano ha già configurato, '
                     'sono da richiedere al Comune di Milano (OP-69). Per la stessa ragione la '
                     'manutenzione della tabella dal back-office non è ancora disegnata.',
                  'sono da richiedere al Comune di Milano (OP-69). Il contenuto, invece, è '
                  'arrivato, ed è descritto sopra; la manutenzione della tabella dal back-office '
                  'è disegnata in [R14].',
                  attese=1, fatti=fatti, etichetta='interfacce ancora assenti, contenuto arrivato')

    # ─────────────────────────── 3. allegati: dove si governano
    D.sostituisci(d, 'la schermata «Campi per UC» mette a disposizione una sezione, '
                     '«Allegati», e l’importazione dal mapping popola entrambe in una sola '
                     'esecuzione.',
                  'la schermata «Campi per UC» mette a disposizione una sezione, «Allegati», e '
                  'l’importazione dal mapping popola entrambe in una sola esecuzione. Il '
                  'back-office ha inoltre una pagina che governa la tabella attraverso tutti '
                  'gli UC, con il caricamento da file nel formato di esportazione di Side [R14].',
                  attese=1, fatti=fatti, etichetta='allegati: pagina dedicata nel back-office')

    # ─────────────────────────── 4. OP-69, riferimenti, storia
    t = next(t for t in d.tables if t.rows[0].cells[0].text.strip() == '#'
             and any(r.cells[0].text.strip() == 'OP-69' for r in t.rows))
    r = next(r for r in t.rows if r.cells[0].text.strip() == 'OP-69')
    D.riscrivi_cella(r.cells[2],
                     'Ridotto nella v3.37: il contenuto della tabella è arrivato '
                     f'({M(v["righe"])} righe, {v["uc"]} UC) e ne ha chiarito cd_soggetto e '
                     'ty_soggetto. Restano da chiedere al Comune di Milano: la semantica dei '
                     'valori di presenza CSTCIV, FO e C02 e dove stia la condizione di C; le '
                     f'definizioni dei {v["configurazioni"]} codici di maschera; il caso d’uso '
                     f'{", ".join(v["fuori_catalogo"])}, assente dal catalogo; le interfacce '
                     'con cui Side gestisce la tabella e il corpo delle tre funzioni dei '
                     'trigger. Resta da decidere se la presenza di un soggetto la governi '
                     'ty_presenza o la logica della sezione in ANSC_CFG_SEZIONE.')
    t = D.trova_tabella(d, 'ID', 'Riferimento')
    r12 = next(r for r in t.rows if r.cells[0].text.strip() == 'R12')
    D.riscrivi_cella(r12.cells[2], r12.cells[2].text.strip() +
                     ' Contenuto ricevuto: Tabella SOGGETTI_USECASE.csv, esportazione della '
                     'tabella compilata.')
    assert t.rows[-1].cells[0].text.strip() == 'R13'
    D.clona_riga(t, ('R14', 'DISEGNO_Back-Office_ANSC_v0.8.docx',
                     'Disegno del back-office pagina per pagina. Dalla v0.8 governa '
                     'ALLEGATI_USECASE e SOGGETTI_USECASE in pagine proprie, con il caricamento '
                     'da file nel formato di esportazione di Side.'))
    D.storia(d, '10/10/2026', '3.37',
             'Costruzione del payload («I soggetti previsti dall’UC», «Gli allegati richiesti '
             'dall’UC») · Riferimenti · Open Point',
             'Riportato il contenuto della tabella dei soggetti per caso d’uso fornito dal '
             f'Comune di Milano: {M(v["righe"])} righe su {v["uc"]} casi d’uso, con la '
             'ripartizione per registro e i ruoli valorizzati. Il file chiarisce che il nome '
             'del blocco del modello evento sta in ty_soggetto e non in cd_soggetto, e rende '
             'quindi possibile il raccordo con le sezioni; mostra valori di presenza e codici '
             'di maschera che nessuna fonte spiega. OP-69 ridotto a ciò che resta da chiedere. '
             'Aggiunto [R14], il disegno del back-office che governa le due tabelle.')
    fatti.append('OP-69 ridotto, [R12] esteso, [R14], storia')

    d.save(DST)
    dopo = commenti(DST)
    if dopo != prima:
        raise SystemExit(f'commenti: {prima} prima, {dopo} dopo')
    print('\n'.join('· ' + f for f in fatti))
    print(f'commenti preservati: {dopo}')


if __name__ == '__main__':
    main()
