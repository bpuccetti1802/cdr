# -*- coding: utf-8 -*-
"""Il percorso di formazione di un atto: che cosa fa l'operatore in SIPO, che cosa chiede ad ANSC.

⚠️ Il diagramma dice due cose che l'elenco dei passi non può dire da solo:
  · **dove il percorso si biforca** — l'acquisizione del token è facoltativa, e la scelta si
    paga alla fine, non subito: senza token non si cerca il soggetto in ANSC, e senza
    identificativo del soggetto il deposito richiede il collegamento manuale dell'evento, che
    la nota ANSC definisce «fortemente sconsigliato»;
  · **dove il punto di non ritorno cade** — con l'avvio della firma l'atto non è più
    modificabile, e questo confligge con la prassi attuale di Roma, che consente correzioni
    fino alla mezzanotte.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

# (numero, titolo, dettaglio, servizio ANSC o None, colore)
PASSI = [
    ('1', 'Scelta dell’operazione', 'dal menu di SIPO: il tipo atto determina\n'
                                    'Modello, maschera e configurazione', None, 'blu'),
    ('2', 'Acquisizione del token', 'l’USC genera l’OTP sulla web app di ANSC\n'
                                    'e lo consegna a SIPO — È FACOLTATIVA', 'web app OTP', 'giallo'),
    ('3', 'Compilazione in SIPO', 'tutti i dati che le maschere\n'
                                  'già prevedono: nessuna novità', None, 'blu'),
    ('4', 'Ricerca degli intestatari', 'recupera l’identificativo nazionale\n'
                                       'del soggetto — solo con token valido', 'R005', 'verde'),
    ('5', 'Dati e documenti per ANSC', 'i campi che SIPO non prevede e gli allegati\n'
                                       'obbligatori per l’UC determinato', None, 'blu'),
    ('6', 'Registrazione dei file', 'archiviazione locale del Comune, poi invio\n'
                                    'ad ANSC e attesa della scansione', 'R001', 'verde'),
    ('7', 'Deposito e firme', 'l’atto entra in ANSC e riceve l’identificativo\n'
                              'nazionale; poi firmano dichiarante e ufficiale', 'R009 · R006 · R007',
     'verde'),
    ('8', 'Atto formato', 'con l’avvio della firma l’atto\n'
                          'non è più modificabile', None, 'rosso'),
]


def disegna(percorso=None):
    percorso = percorso or os.path.join(IMG, 'formazione_atto.png')
    W, H = 1560, 1450
    im, dr = G.tela(W, H, 'La formazione di un atto: SIPO e ANSC',
                    'l’operatore lavora nelle maschere di SIPO; ANSC interviene in quattro '
                    'momenti, e in uno solo è facoltativo')
    G.banda(dr, 40, 120, 820, 1170, '#2f6bb0', 'SIPO — dove l’operatore lavora', '#25548a')
    G.banda(dr, 900, 120, 1520, 1170, '#3f8f5f', 'ANSC — che cosa si chiede', '#2f6b4a')

    y = 170
    centri = {}
    for num, titolo, dett, servizio, colore in PASSI:
        h = 96
        bordo, fondo = G.C[colore]
        dr.rounded_rectangle([70, y, 780, y + h], radius=12, fill=fondo, outline=bordo, width=3)
        dr.ellipse([88, y + 30, 126, y + 68], fill=bordo, outline=bordo)
        G.centra(dr, num, G.fnt(G.F_BLD, 22), 107, y + 36, 'white')
        dr.text((146, y + 16), titolo, font=G.fnt(G.F_BLD, 21), fill=G.INK)
        yy = y + 44
        for riga in dett.split('\n'):
            dr.text((146, yy), riga, font=G.fnt(G.F_REG, 16), fill=G.MUTED)
            yy += 21
        centri[num] = (y, y + h)
        if servizio:
            bx, bf = G.C['verde' if servizio.startswith('R') else 'giallo']
            larg = 300 if len(servizio) < 20 else 380
            dr.rounded_rectangle([950, y + 18, 950 + larg, y + h - 18], radius=10,
                                 fill=bf, outline=bx, width=3)
            G.centra(dr, servizio, G.fnt(G.F_BLD, 19), 950 + larg / 2, y + 36, G.INK)
            G.percorso(dr, [(784, y + h / 2), (946, y + h / 2)], bx, False, 3)
        y += h + 26

    # il ramo di chi non acquisisce il token
    x1 = 800
    G.linea(dr, [(x1, centri['2'][1] - 20), (x1 + 40, centri['2'][1] - 20),
                 (x1 + 40, centri['4'][0] + 48), (784, centri['4'][0] + 48)],
            G.C['rosso'][0], True, 3)
    dr.text((846, centri['2'][1] - 6), 'senza token:', font=G.fnt(G.F_BLD, 16),
            fill=G.C['rosso'][0])
    dr.text((846, centri['2'][1] + 16), 'la ricerca è inibita', font=G.fnt(G.F_ITA, 16),
            fill=G.MUTED)

    # il punto di non ritorno
    yr = centri['8'][0] - 14
    dr.line([70, yr, 1500, yr], fill=G.C['rosso'][0], width=3)
    dr.text((860, yr + 8), 'PUNTO DI NON RITORNO',
            font=G.fnt(G.F_BLD, 18), fill=G.C['rosso'][0])
    dr.text((860, yr + 32), 'oltre questa linea l’atto non si modifica più',
            font=G.fnt(G.F_ITA, 16), fill=G.MUTED)

    G.box(dr, 60, 1210, 720, 160, 'rosso', 'Che cosa cambia per l’operatore',
          'Oggi a Roma un atto si corregge fino alla mezzanotte. Con ANSC la finestra si '
          'chiude quando comincia la firma: dopo, la correzione non è più una modifica ma '
          'un procedimento — annotazione, rettifica o annullamento.')
    G.box(dr, 810, 1210, 710, 160, 'giallo', 'Il prezzo di saltare il passo 2',
          'Senza identificativo nazionale del soggetto gli automatismi di ANSC non scattano: '
          'al deposito occorre collegare l’evento a mano, e la nota di processo ANSC lo '
          'definisce «fortemente sconsigliato».')

    G.legenda(dr, 60, H - 42, [('blu', 'passi che restano in SIPO'),
                               ('verde', 'passi che chiamano ANSC'),
                               ('giallo', 'passo facoltativo'),
                               ('rosso', 'punto di non ritorno')])
    im.save(percorso)
    return percorso


if __name__ == '__main__':
    os.makedirs(IMG, exist_ok=True)
    print('scritto:', os.path.relpath(disegna(), BASE))
