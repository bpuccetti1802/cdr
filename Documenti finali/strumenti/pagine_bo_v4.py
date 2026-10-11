# -*- coding: utf-8 -*-
"""Figure della v0.9 del disegno del back-office: la numerazione comunale riallineata alle due
pagine del sistema Side del Comune di Milano («Gestione numerazione comunale — Richiesta» e
«— Ricerca e consultazione», documento di processo v1.0) e al servizio num-ansc-sipo
dell'analisi v3.39 (contratto ansc-numerazione-v1.yaml).

  · bo_num_richiesta.png  — Numerazione comunale — richiesta (stacco e registrazione a
                            posteriori)
  · bo_num_ricerca.png    — Numerazione comunale — ricerca e consultazione, con le serie

Sostituiscono bo_numerazione.png di pagine_bo.py, che non la rigenera più.
⚠️ I numeri e gli identificativi sono inventati ma coerenti fra loro: l'identificativo
nazionale porta, in terza posizione, lo stesso numero comunale della riga (forma anno,
numero nazionale, numero comunale, codice ISTAT di Roma 058091).

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo_v4.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wireframe_bo as W   # noqa: E402

L, X = 1240, 24
C = L - 2 * X
SOTTO = ('Il numero comunale è a carico del Comune: si stacca dalla serie del registro e '
         'dell’anno, che riparte ogni anno.')


# ──────────────────────────────────────────────── Richiesta
def richiesta(dest):
    im, dr, y = W.pagina(L, 900, ['Home', 'Integrazione ANSC', 'Numerazione comunale',
                                  'Richiesta'],
                         'Numerazione comunale — richiesta', sotto=SOTTO)
    y = W.riga_campi(dr, X, y, C - 200, [
        ('Registro', 'Nascita', 'select', 4), ('Anno', '2027', 'testo', 2),
        ('Numero di elementi', '3', 'testo', 2)])
    W.bottoni_dx(dr, X + C, y - 52, [('RICHIEDI', W.BLU, True)])
    y += 2
    y = W.tabella(dr, X, y, C,
                  ['ID richiesta', 'Operatore', 'Data richiesta', 'Registro', 'Anno',
                   'Numero', 'ID ANSC', 'Stato', 'Azioni'],
                  [110, 150, 130, 100, 70, 90, 270, 140, 132], [
                      ['90211', 'RSSMRA70A01H501U', '14/03/2027', 'Nascita', '2027', '1.140',
                       '—', ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                      ['90211', 'RSSMRA70A01H501U', '14/03/2027', 'Nascita', '2027', '1.141',
                       '—', ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                      ['90211', 'RSSMRA70A01H501U', '14/03/2027', 'Nascita', '2027', '1.142',
                       '—', ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                  ])
    y = W.nota(dr, X, y + 4, C,
               'I tre numeri di un parto trigemino escono consecutivi: gli stacchi sono '
               'serializzati. La spunta segna il numero come Utilizzato e chiede '
               'l’identificativo nazionale dell’atto; la croce lo segna come Scartato. Gli '
               'stati Scartato ed Evento acquisito sono finali.')
    y += 6
    y = W.pannello(dr, X, y, C, 'Registrazione a posteriori — numero usato sulla web app '
                                'mentre SIPO non era disponibile', alt=100)
    y = W.riga_campi(dr, X + 16, y + 6, C - 232, [
        ('Registro', 'Morte', 'select', 3), ('Anno', '2027', 'testo', 2),
        ('Numero usato', '1532', 'testo', 2),
        ('Identificativo nazionale', '2027-48123-1532-058091', 'testo', 5)])
    W.bottoni_dx(dr, X + C - 16, y - 52, [('REGISTRA', W.BLU, True)])
    y += 8
    W.nota(dr, X, y, C,
           'Il numero entra nella serie come Utilizzato. Se è uguale o superiore al prossimo, '
           'la serie avanza fino a lì, così che nessuno lo riceva di nuovo; se è inferiore e '
           'libero colma un buco; se è già registrato la registrazione è respinta.', W.GIALLO)
    return W.salva(im, dest, 'bo_num_richiesta.png')


# ──────────────────────────────────────────────── Ricerca e consultazione
def ricerca(dest):
    im, dr, y = W.pagina(L, 1060, ['Home', 'Integrazione ANSC', 'Numerazione comunale',
                                   'Ricerca e consultazione'],
                         'Numerazione comunale — ricerca e consultazione',
                         azioni_dx=['CREA SERIE'], sotto=SOTTO)
    y = W.pannello(dr, X, y, C, 'Serie dell’anno 2027', alt=232)
    y = W.tabella(dr, X + 16, y, C - 32,
                  ['Registro', 'Prossimo numero', 'Disponibili', 'Utilizzati', 'Scartati',
                   'Evento acquisito', 'Buchi'],
                  [180, 170, 140, 140, 140, 170, 220], [
                      ['Nascita', '1.143', '3', '1.121', '12', '6', '0'],
                      ['Morte', '1.534', '2', '1.509', '17', '4', ('1 — vedi', W.GIALLO)],
                      ['Matrimonio', '611', '0', '598', '9', '3', '0'],
                      ['Unione civile', '15', '0', '14', '0', '0', '0'],
                      ['Cittadinanza', '388', '1', '380', '6', '0', '0'],
                  ])
    y += 6
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=150)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Registro', 'Morte', 'select', 3), ('Richieste da', '01/03/2027', 'data', 3),
        ('Richieste a', '14/03/2027', 'data', 3), ('Operatore', 'Tutti', 'select', 3),
        ('Stato', 'Tutti', 'select', 2), ('Atto SIPO', '', 'testo', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y - 6, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 28
    y = W.tabella(dr, X, y, C,
                  ['ID richiesta', 'Operatore', 'Data richiesta', 'Registro', 'Anno',
                   'Numero', 'ID ANSC', 'Atto SIPO', 'Stato', 'Azioni'],
                  [100, 150, 120, 90, 60, 80, 230, 100, 150, 112], [
                      ['90198', 'BNCLRA75B41H501K', '13/03/2027', 'Morte', '2027', '1.530',
                       '2027-48117-1530-058091', '4581270', ('UTILIZZATO', W.BLU), ['vedi']],
                      ['90204', 'RSSMRA70A01H501U', '13/03/2027', 'Morte', '2027', '1.531',
                       '—', '—', ('SCARTATO', W.MUTED), ['vedi']],
                      ['90215', 'VRDGPP68C12H501T', '14/03/2027', 'Morte', '2027', '1.532',
                       '2027-48123-1532-058091', '—', ('UTILIZZATO', W.BLU), ['vedi', 'mod']],
                      ['90219', 'BNCLRA75B41H501K', '14/03/2027', 'Morte', '2027', '1.533',
                       '—', '4581291', ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='31', pagine=7)
    W.nota(dr, X, y, C,
           'La matita su un numero Utilizzato lega l’atto di SIPO e lo porta a Evento '
           'acquisito, quando l’atto formato sulla web app viene agganciato. Un buco è un '
           'numero preso dalla serie e mai registrato: non ha una riga, e la tabella delle '
           'serie è l’unico posto in cui si vede. CREA SERIE è riservato all’amministratore.',
           W.GIALLO)
    return W.salva(im, dest, 'bo_num_ricerca.png')


if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    for f in (richiesta, ricerca):
        print('  scritto', f(dest))
