# -*- coding: utf-8 -*-
"""Figure della v0.10 del disegno del back-office: gli identificativi del soggetto ottenuti da
R005, registrati come stabilisce la v3.40 dell'analisi (ANSC_SOGGETTO_IDENTIFICATIVI per
l'identificativo ANSC, ANAG_USR.SOGGETTO per i due codici ANPR, scritti solo se vuoti).

  · bo_identificativi.png — Identificativi dei soggetti: le eccezioni della scrittura dei
                            codici ANPR, l'elenco e il confronto anagrafe ↔ R005
  · bo_atto.png           — Dettaglio dell'atto rigenerato con la scheda «Soggetti»
                            (pagine_bo.atto, una linguetta in più)

⚠️ Nomi, codici fiscali e identificativi sono inventati. La forma dell'identificativo unico
nazionale (nove caratteri alfanumerici) segue l'esempio del contratto R005 («ABCDE1234»).

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo_v5.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wireframe_bo as W   # noqa: E402
import pagine_bo as P      # noqa: E402

L, X = 1240, 24
C = L - 2 * X


def identificativi(dest):
    im, dr, y = W.pagina(L, 1200, ['Home', 'Integrazione ANSC', 'Identificativi dei soggetti'],
                         'Identificativi dei soggetti', azioni_dx=['ESPORTA'],
                         sotto='Che cosa ha dato la consultazione R005 dei soggetti, e dove i '
                               'codici ANPR non si sono potuti scrivere.')
    y = W.pannello(dr, X, y, C, 'Da trattare', alt=178)
    y = W.tabella(dr, X + 16, y, C - 32, ['Esito dei codici ANPR', 'Soggetti', 'Che cosa significa'],
                  [240, 110, 810], [
                      [('DISCORDANTE', W.ROSSO), '7',
                       'L’anagrafe porta un codice diverso da quello restituito da ANSC: non '
                       'sovrascritto'],
                      [('NON NUMERICO', W.GIALLO), '1',
                       'L’identificativo della scheda non entra nella colonna numerica'],
                      [('ASSENTE ANAGRAFE', W.VIOLA), '23',
                       'Il soggetto non ha una riga anagrafica: i codici non si conservano'],
                  ])
    y += 18
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=150)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Esito dei codici ANPR', 'DISCORDANTE', 'select', 3),
        ('Esito della ricerca', 'Tutti', 'select', 3), ('Atto SIPO', '', 'testo', 2),
        ('Codice fiscale', '', 'testo', 3), ('Ricerca da', '01/03/2027', 'data', 2),
        ('Ricerca a', '14/03/2027', 'data', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y - 6, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 28
    y = W.tabella(dr, X, y, C,
                  ['Soggetto', 'Codice fiscale', 'Atto SIPO', 'Identificativo ANSC', 'Ricerca',
                   'Codici ANPR', 'Data ricerca', 'Operatore', 'Azioni'],
                  [150, 160, 100, 140, 110, 150, 110, 140, 132], [
                      ['ROSSI MARIO', 'RSSMRA41C12H501Z', '4581270', '8841203',
                       ('TROVATO', W.VERDE), ('DISCORDANTE', W.ROSSO), '13/03/2027',
                       'BNCLRA75B41H501K', ['vedi', 'mod']],
                      ['ESPOSITO ANNA', 'SPSNNA52H45F839W', '4581288', '9013377',
                       ('SCELTO', W.BLU), ('DISCORDANTE', W.ROSSO), '14/03/2027',
                       'RSSMRA70A01H501U', ['vedi', 'mod']],
                      ['COLOMBO LUCA', 'CLMLCU88D03F205P', '4581291', '9013410',
                       ('TROVATO', W.VERDE), ('DISCORDANTE', W.ROSSO), '14/03/2027',
                       'VRDGPP68C12H501T', ['vedi', 'mod']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='7', pagine=2)
    y = W.pannello(dr, X, y, C, 'Confronto — ROSSI MARIO, atto 4581270', alt=176)
    y = W.tabella(dr, X + 16, y, C - 32,
                  ['Codice', 'In anagrafe (ANAG_USR.SOGGETTO)',
                   'Restituito da R005 il 13/03/2027', 'Confronto'],
                  [300, 300, 320, 240], [
                      ['Identificativo della scheda ANPR', '104829331', '104829377',
                       ('DIVERSO', W.ROSSO)],
                      ['Identificativo unico nazionale', 'QX7K2M41B', 'QX7K2M41B',
                       ('UGUALE', W.VERDE)],
                      ['Identificativo del soggetto in ANSC', '—', '8841203',
                       ('REGISTRATO', W.BLU)],
                  ])
    y += 16
    W.nota(dr, X, y, C,
           'La pagina non scrive sull’anagrafe: il codice registrato in ANAG_USR.SOGGETTO lo '
           'hanno scritto i canali di allineamento con ANPR, e la consultazione non lo '
           'contraddice. L’occhio apre la risposta di R005 conservata nell’audit; la matita '
           'riporta all’atto di SIPO, dove una nuova consultazione dal riepilogo dei soggetti '
           'aggiorna l’esito quando la discordanza è stata risolta.', W.GIALLO)
    return W.salva(im, dest, 'bo_identificativi.png')


def atto(dest):
    """Il dettaglio dell'atto di pagine_bo, con la linguetta «Soggetti» fra le schede."""
    originale = W.schede

    def schede(dr, x, y, larg, voci, attiva=0):
        if 'Sezioni e campi' in voci and 'Soggetti' not in voci:
            voci = voci[:1] + ['Soggetti'] + voci[1:]
        return originale(dr, x, y, larg, voci, attiva)
    W.schede = schede
    try:
        return P.atto(dest)
    finally:
        W.schede = originale


if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    for f in (identificativi, atto):
        print('  scritto', f(dest))
