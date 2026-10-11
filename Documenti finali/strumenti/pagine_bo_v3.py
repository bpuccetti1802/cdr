# -*- coding: utf-8 -*-
"""Figure della v0.8 del disegno del back-office: la gestione dei documenti e dei soggetti
per caso d'uso, adottata dal sistema Side del Comune di Milano.

  · bo_allegati.png          — Allegati dell'atto, RIFATTA sul processo di Side (sostituisce
                               quella di pagine_bo.py, che resta come storia)
  · bo_allegati_uc.png       — Allegati per caso d'uso (ALLEGATI_USECASE), pagina nuova
  · bo_soggetti_uc.png       — Soggetti per caso d'uso (SOGGETTI_USECASE), pagina nuova
  · bo_carica_file.png       — Caricamento da file, comune alle due

⚠️ I valori della pagina dei soggetti e il verbale del caricamento sono quelli VERI del file
di Side `Sorgenti Documentali/Tabella SOGGETTI_USECASE.csv` (UC 2101, conteggi del file):
se il file cambia, rieseguire `verbale_soggetti()` e riportare i numeri. Gli allegati
dell'UC 2101 sono quelli del mapping ufficiale (Morte_001.csv: entrambi facoltativi).
I codici di logica («D2 · …») sono esempi, come nelle altre pagine.

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo_v3.py img
"""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wireframe_bo as W   # noqa: E402
from diagrammi_comune import F_BLD, fnt   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_SOGG = os.path.join(BASE, 'Sorgenti Documentali', 'Tabella SOGGETTI_USECASE.csv')
CATALOGO = os.path.join(BASE, 'ansc', 'docs', 'Decodifiche', '3_dec_use_case.csv')

L, X = 1240, 24
C = L - 2 * X
SOTTO = ('Versione in lavorazione: v13 — BOZZA. Le modifiche non hanno effetto finché la '
         'versione non è attivata.')


def verbale_soggetti():
    """I numeri del caricamento del file di Side, calcolati dal file e non scritti a mano."""
    with open(CSV_SOGG, encoding='utf-8') as f:
        lettore = csv.DictReader(f)
        colonne = lettore.fieldnames
        righe = list(lettore)
    with open(CATALOGO, encoding='utf-8-sig') as f:
        catalogo = {r['ID'] for r in csv.DictReader(f)}
    uc = {r['cd_usecase'] for r in righe}
    chiavi = collections.Counter((r['cd_usecase'], r['cd_soggetto']) for r in righe)
    presenza = collections.Counter(r['ty_presenza'] for r in righe)
    return {
        'colonne': len(colonne), 'righe': len(righe), 'uc': len(uc),
        'fuori_catalogo': sorted(uc - catalogo),
        'duplicate': sum(1 for v in chiavi.values() if v > 1),
        'presenza': presenza,
        'non_documentati': {k: v for k, v in presenza.items() if k not in ('O', 'F', 'C')},
        'configurazioni': len({r['ty_configurazione'] for r in righe}),
        'non_operanti': sum(1 for r in righe if r['fg_operante'] == '0'),
        'note': sum(1 for r in righe if r['tx_note'].strip()),
    }


def migl(n):
    return f'{n:,}'.replace(',', '.')


# ──────────────────────────────────────────────── Allegati dell'atto (rifatta)
def allegati(dest):
    im, dr, y = W.pagina(L, 860,
                         ['Home', 'Integrazione ANSC', 'Supervisione atti',
                          '2026/0041287', 'Allegati'],
                         'Allegati dell’atto 2026/0041287',
                         sotto='UC 2101 — Morte in abitazione a Roma. Il processo è quello '
                               'di Side: caricamento in SIPO, invio, verifica fino a '
                               '«Inserito».')
    y = W.nota(dr, X, y, C,
               'La dimensione del file non deve superare 10 Mb; il nome non deve contenere '
               'spazi o caratteri speciali; sono ammessi PDF, JPG, TIF, P7M. Un documento è '
               'utilizzabile solo quando ANSC lo dichiara «Inserito».')
    dr.text((X, y), 'Documenti previsti dall’UC (ALLEGATI_USECASE)', font=fnt(F_BLD, 13),
            fill=W.INK)
    y += 24
    y = W.tabella(dr, X, y, C,
                  ['Tipo (ANSC_09)', 'Presenza', 'Forma', 'File', 'Stato',
                   'Nell’attestazione', 'Azioni'],
                  [260, 90, 100, 230, 220, 140, 120], [
                      ['32 · Certificato necroscopico', 'F', 'BASE', 'cert_necro.pdf',
                       ('3 · INSERITO', W.VERDE), 'Sì', ['vedi', 'del']],
                      ['127 · Documento autorizzativo', 'F', 'BASE', 'autorizzazione.pdf',
                       ('0 · CARICATO IN SIPO', W.BLU), '—', ['vedi', 'del']],
                  ])
    dr.text((X, y + 6), 'Altri documenti — 998 Allegato generico (D.LIB.M.01)',
            font=fnt(F_BLD, 13), fill=W.INK)
    y += 34
    W.campo(dr, X, y, 420, 'Descrizione del documento *', 'Verbale di ricognizione')
    W.ic_piu(dr, X + 440, y + 9)
    y += 52
    y = W.tabella(dr, X, y, C,
                  ['Descrizione', 'File', 'Caricato da', 'Stato', 'Nell’attestazione',
                   'Azioni'],
                  [300, 280, 160, 220, 140, 60], [
                      ['Verbale di ricognizione', 'verbale_01.pdf', 'g.rossi',
                       ('0 · CARICATO IN SIPO', W.BLU), '—', ['del']],
                  ])
    y = W.bottoni(dr, X, y + 4, [('INVIA', W.BLU, True), ('INDIETRO', W.MUTED)])
    W.nota(dr, X, y, C,
           'INVIA compare perché almeno un documento è nello stato 0; VERIFICA compare solo '
           'quando nessuno è più nello stato 0 e almeno uno è negli stati 1 o 2. I due bottoni '
           'non sono mai presenti insieme. La colonna dell’attestazione riporta la scelta '
           'fatta dall’ufficiale al momento della firma: qui si legge, non si decide.',
           W.GIALLO)
    return W.salva(im, dest, 'bo_allegati.png')


# ──────────────────────────────────────────────── Allegati per caso d'uso
def allegati_uc(dest):
    im, dr, y = W.pagina(L, 860, ['Home', 'Integrazione ANSC', 'Allegati per caso d’uso'],
                         'Allegati per caso d’uso',
                         azioni_dx=['CARICA DA FILE', 'ESPORTA CSV', 'NUOVA RIGA'],
                         sotto=SOTTO)
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=96)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Versione', 'v13 — BOZZA', 'select', 3), ('Registro', 'Tutti', 'select', 2),
        ('Codice UC', '', 'testo', 2), ('Tipo allegato', '', 'select', 3),
        ('Presenza', 'Tutte', 'select', 2), ('Operante', 'Sì', 'select', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Tipo', 'Descrizione (ANSC_09)', 'Presenza', 'Forma',
                   'Condizione', 'Ord.', 'Op.', 'Azioni'],
                  [100, 60, 370, 90, 120, 160, 60, 60, 172], [
                      ['2101', '32', 'Certificato necroscopico', 'F', 'BASE', '—', '1',
                       ('1', W.VERDE), ['mod', 'del']],
                      ['2101', '127', 'Documento autorizzativo', 'F', 'BASE', '—', '2',
                       ('1', W.VERDE), ['mod', 'del']],
                      ['11111000', '1', 'Attestazione di nascita', 'C001', 'BASE',
                       'D2 · ACCERT_1', '1', ('1', W.VERDE), ['mod', 'del']],
                      ['11111000', '2', 'Constatazione di avvenuto parto', 'C002', 'BASE',
                       'D2 · ACCERT_2', '2', ('1', W.VERDE), ['mod', 'del']],
                      ['11111000', '3', 'Dichiarazione di nascita sostitutiva …', 'C003',
                       'BASE', 'D2 · ACCERT_3', '3', ('1', W.VERDE), ['mod', 'del']],
                      ['14400000', '998', 'Allegato generico', 'F', 'D.LIB.M.01', '—',
                       '1', ('1', W.VERDE), ['mod', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='1.569', pagine=20)
    W.nota(dr, X, y, C,
           'La matita apre la riga in modifica; il cestino la disattiva (operante a 0) e non '
           'la cancella. CARICA DA FILE accetta il formato in cui Side esporta la tabella; '
           'ESPORTA CSV produce lo stesso formato, così che un file esportato possa essere '
           'ricaricato tale e quale.')
    return W.salva(im, dest, 'bo_allegati_uc.png')


# ──────────────────────────────────────────────── Soggetti per caso d'uso
def soggetti_uc(dest):
    v = verbale_soggetti()
    im, dr, y = W.pagina(L, 860, ['Home', 'Integrazione ANSC', 'Soggetti per caso d’uso'],
                         'Soggetti per caso d’uso',
                         azioni_dx=['CARICA DA FILE', 'ESPORTA CSV', 'NUOVA RIGA'],
                         sotto=SOTTO)
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=96)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Versione', 'v13 — BOZZA', 'select', 3), ('Codice UC', '2101', 'testo', 2),
        ('Ruolo', 'Tutti', 'select', 2), ('Presenza', 'Tutte', 'select', 2),
        ('Operante', 'Sì', 'select', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Codice', 'Tipo (modello evento)', 'Nome', 'Presenza',
                   'Configurazione', 'Dich.', 'Comp.', 'Firma', 'Ord.', 'Azioni'],
                  [80, 150, 150, 200, 80, 120, 60, 60, 60, 50, 182], [
                      ['2101', 'DECEDUTO', 'intestatari', 'Deceduto', 'O', 'BASEDEC',
                       '0', '0', '0', '1', ['mod', 'del']],
                      ['2101', 'COMPARENTE1', 'comparente1', 'Comparente dichiarante', 'O',
                       'BASENOINT', '1', '1', '1', '2', ['mod', 'del']],
                      ['2101', 'COMPARENTE2', 'comparente2', 'Secondo comparente',
                       ('C02', W.GIALLO), 'BASENOINT', '0', '1', '1', '3', ['mod', 'del']],
                      ['2101', 'CONIUGE', 'coniuge', 'Coniuge', ('CSTCIV', W.GIALLO),
                       'BASECONI', '0', '0', '0', '4', ['mod', 'del']],
                      ['2101', 'UNITOCIVILMENTE', 'coniuge', 'Unito Civilmente',
                       ('CSTCIV', W.GIALLO), 'BASECONI', '0', '0', '0', '5', ['mod', 'del']],
                      ['2101', 'INTERPR', 'interprete', 'Interprete', 'C', 'BASEOPFI',
                       '0', '0', '0', '6', ['mod', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale=migl(v['righe']), pagine=6)
    W.nota(dr, X, y, C,
           'Righe del file di Side per l’UC 2101. In giallo i valori di presenza che la '
           'documentazione di Side non spiega: il caricamento li accetta e li segnala. I '
           'tre contrassegni di ruolo non vengono dal mapping di ANSC: si compilano qui.',
           W.GIALLO)
    return W.salva(im, dest, 'bo_soggetti_uc.png')


# ──────────────────────────────────────────────── Caricamento da file
def carica_file(dest):
    v = verbale_soggetti()
    im, dr, y = W.pagina(L, 900,
                         ['Home', 'Integrazione ANSC', 'Soggetti per caso d’uso',
                          'Caricamento da file'],
                         'Caricamento da file', sotto=SOTTO)
    y = W.riga_campi(dr, X, y, C, [
        ('Tabella di destinazione', 'SOGGETTI_USECASE', 'select', 3),
        ('File *', 'Tabella SOGGETTI_USECASE.csv', 'testo', 4),
        ('Versione di destinazione', 'v13 — BOZZA', 'select', 2)])
    y = W.riga_campi(dr, X, y, C, [
        ('Modalità', 'Sostituisci le righe degli UC presenti nel file', 'select', 5),
        ('Solo simulazione', 'Sì', 'select', 2), ('Separatore', 'virgola', 'select', 2)])
    y = W.bottoni(dr, X, y, [('CONTROLLA', W.BLU, True), ('APPLICA', W.MUTED),
                             ('ANNULLA', W.MUTED)])
    dr.text((X, y), 'Verbale dei controlli', font=fnt(F_BLD, 13), fill=W.INK)
    y += 24
    nd = ' · '.join(f'{k} {v}' for k, v in sorted(v['non_documentati'].items(),
                                                   key=lambda kv: -kv[1]))
    fc = ', '.join(v['fuori_catalogo']) or '—'
    y = W.tabella(dr, X, y, C, ['Controllo', 'Esito', 'Dettaglio'], [330, 150, 712], [
        ['Intestazione', ('OK', W.VERDE), f'{v["colonne"]} colonne su {v["colonne"]}, '
                                          'nei nomi della definizione'],
        ['Righe lette', ('OK', W.VERDE), f'{migl(v["righe"])} righe, {v["uc"]} UC distinti'],
        ['Chiavi duplicate (UC + soggetto)', ('OK', W.VERDE), str(v['duplicate'])],
        ['UC assenti dal catalogo di ANSC', ('AVVISO', W.GIALLO),
         f'{len(v["fuori_catalogo"])} — {fc}: righe caricate, da verificare'],
        ['Presenza con valori non documentati', ('AVVISO', W.GIALLO), nd],
        ['Codici di configurazione', ('AVVISO', W.GIALLO),
         f'{v["configurazioni"]} distinti, senza un catalogo con cui confrontarli'],
        ['Righe non operanti', ('INFO', W.BLU), f'{v["non_operanti"]}: caricate con '
                                                'operante a 0'],
        ['Campi tecnici del file', ('INFO', W.BLU), 'codici operatore e istanti di Side '
                                                    'non riportati: si registra chi carica'],
        ['Effetto sulla versione v13', ('SIMULATO', W.MUTED),
         f'{migl(v["righe"])} da inserire · 0 da aggiornare · 0 da disattivare'],
    ])
    W.nota(dr, X, y, C,
           'Il caricamento si prova prima di eseguirlo: con «Solo simulazione» il verbale '
           'dice che cosa accadrebbe senza scrivere nulla. Gli errori bloccano APPLICA; gli '
           'avvisi no, ma restano nel verbale, che si conserva nel registro dei comandi.')
    return W.salva(im, dest, 'bo_carica_file.png')


if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    print(verbale_soggetti())
    for f in (allegati, allegati_uc, soggetti_uc, carica_file):
        print('  scritto', f(dest))
