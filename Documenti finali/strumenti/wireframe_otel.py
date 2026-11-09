# -*- coding: utf-8 -*-
"""Le due pagine del back-office di supporto proposto in
`PROPOSTA_Osservabilita-OpenTelemetry`, nello stile delle altre pagine del back-office
(`wireframe_bo.py`, design system di Roma Capitale).

  · otel_bo_errori.png   — la worklist degli errori: si filtra per periodo, origine, livello
                           e servizio, e ogni riga porta l'identificativo di traccia, che e'
                           la chiave per passare al dettaglio.
  · otel_bo_traccia.png  — una traccia aperta: la cascata degli span attraverso i pod, con le
                           durate, e sotto gli eventi agganciati a ciascuno.

⚠️ La seconda pagina non e' un modulo: e' una cascata disegnata a mano con rettangoli, perche'
nessuna primitiva di `wireframe_bo` rappresenta una sequenza temporale. Le barre sono in scala
sui millisecondi dichiarati in DURATE, cosi' la figura resta vera se si cambiano i numeri.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/wireframe_otel.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wireframe_bo as W   # noqa: E402
from diagrammi_comune import F_BLD, F_ITA, F_REG, MUTED, centra, fnt   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(QUI, 'img')

L, X = 1240, 24
C = L - 2 * X

MENU = ('Home', 'Supervisione atti', 'Errori e diagnostica')

# ── i colori dei distintivi, per origine e per livello
ORIGINE = {'FE': W.BLU, 'BE': '#6b7280', 'DB': '#7b5aa6', 'ANSC': W.BARRA,
           'ANPR': '#b5651d', 'INFRA': '#0f766e', 'CONF': W.GIALLO}
LIVELLO = {'ERROR': W.ROSSO, 'WARN': W.GIALLO, 'INFO': W.BLU, 'FATAL': '#7f1d1d'}


def errori(dest):
    """La worklist: che cosa è andato storto, da dove viene e chi deve guardarlo."""
    im, dr, y = W.pagina(
        L, 820, ['Home', 'Errori e diagnostica', 'Elenco'], 'Errori e diagnostica',
        azioni_dx=['ESPORTA', 'AGGIORNA'],
        sotto='Gli eventi di livello WARN e superiore delle ultime 24 ore. '
              'L’origine dice a quale gruppo di supporto compete, non dove l’errore è '
              'comparso.')

    y = W.riga_campi(dr, X, y, C, [
        ('Dal', '09/11/2026 00:00', 'data', 3), ('Al', '09/11/2026 18:00', 'data', 3),
        ('Livello', 'ERROR e oltre', 'select', 3), ('Ambiente', 'Produzione', 'select', 3)])
    y = W.riga_campi(dr, X, y, C, [
        ('Origine', 'Tutte', 'select', 3), ('Servizio', 'Tutti', 'select', 3),
        ('Codice evento', '', 'testo', 3), ('Identificativo di traccia', '', 'testo', 3)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6

    # ⚠️ la colonna «origine» viene prima del servizio: è la classificazione che smista il
    # biglietto, mentre il servizio dice soltanto quale processo ha scritto la riga.
    y = W.tabella(dr, X, y, C,
                  ['Ora', 'Liv.', 'Origine', 'Servizio', 'Codice', 'Messaggio',
                   'Atto', 'Traccia', 'Az.'],
                  [86, 70, 86, 150, 130, 358, 86, 134, 52], [
                      ['17:42:11', ('ERROR', LIVELLO['ERROR']), ('ANSC', ORIGINE['ANSC']),
                       'all-ansc-sipo', 'ANSC-400001',
                       'Campo obbligatorio mancante: numeroTestimoni', '1842/2026',
                       '4bf92f35…4736', ['vedi']],
                      ['17:38:04', ('ERROR', LIVELLO['ERROR']), ('DB', ORIGINE['DB']),
                       'be-numeratore', 'DB-ORA-00060',
                       'Deadlock sullo stacco del numero comunale', '1841/2026',
                       '9c2a7d10…b118', ['vedi']],
                      ['17:31:55', ('WARN', LIVELLO['WARN']), ('INFRA', ORIGINE['INFRA']),
                       'all-ansc-sipo', 'INFRA-OTP-SCAD',
                       'Codice di sessione scaduto durante la sequenza di firma', '1839/2026',
                       '77ab03ce…21d9', ['vedi']],
                      ['17:20:30', ('ERROR', LIVELLO['ERROR']), ('FE', ORIGINE['FE']),
                       'mfOperation', 'FE-CHIAMATA-KO',
                       'Chiamata a /ansc/v1/atti fallita dopo 3 tentativi', '—',
                       '0d41c6aa…5502', ['vedi']],
                      ['16:58:12', ('ERROR', LIVELLO['ERROR']), ('CONF', ORIGINE['CONF']),
                       'all-ansc-sipo', 'CONF-UC-AMBIGUO',
                       'Due righe di configurazione applicabili allo stesso atto', '1835/2026',
                       '5e8810bf…cc47', ['vedi']],
                      ['16:44:07', ('WARN', LIVELLO['WARN']), ('ANPR', ORIGINE['ANPR']),
                       'all-anpr-sipo', 'ANPR-5008-KO',
                       'Mutazione rifiutata: soggetto non trovato', '—',
                       'ba37f204…9e60', ['vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='48', pagine=10)

    W.nota(dr, X, y, C,
           'Una riga senza numero di atto non è un difetto dell’elenco: gli eventi che non '
           'riguardano un atto — il caricamento di un dizionario, lo stacco di un numero, una '
           'chiamata del front-end — oggi non hanno dove essere registrati, perché '
           'ANSC_LOG_AUDIT è legata all’atto da una chiave esterna. È la ragione principale '
           'per cui serve un secondo registro accanto a quello probatorio.', W.BLU)
    return W.salva(im, dest, 'otel_bo_errori.png', voci_menu=MENU)


# ── la cascata: (profondità, servizio, operazione, inizio ms, durata ms, esito)
DURATE = [
    (0, 'mfOperation', 'VALIDA — azione dell’operatore', 0, 2180, 'ko'),
    (1, 'all-ansc-sipo', 'POST /ansc/v1/atti/1842/validazione', 40, 2090, 'ko'),
    (2, 'be-numeratore', 'POST /api/v1/numerazione-comunale/richiesta', 70, 180, 'ok'),
    (2, 'all-ansc-sipo', 'preverifica locale (configurazione)', 270, 140, 'ok'),
    (2, 'all-ansc-sipo', 'costruzione del payload', 420, 210, 'ok'),
    (2, 'ANSC', 'R009 /validazione/evento', 650, 1460, 'ko'),
    (3, 'ANSC', 'HTTP 400 — codice 400001', 2080, 20, 'ko'),
]

EVENTI = [
    ('17:42:09.114', 'INFO', 'BE', 'all-ansc-sipo', 'DEPOSITO-AVVIO',
     'Avvio della validazione per l’atto 1842/2026, caso d’uso 311111'),
    ('17:42:09.298', 'INFO', 'BE', 'be-numeratore', 'NUM-STACCO',
     'Numero comunale 001842 staccato per l’anno 2026'),
    ('17:42:10.760', 'WARN', 'ANSC', 'all-ansc-sipo', 'ANSC-LENTO',
     'R009 oltre la soglia di attenzione: 1.460 ms'),
    ('17:42:11.182', 'ERROR', 'ANSC', 'all-ansc-sipo', 'ANSC-400001',
     'Campo obbligatorio mancante: evento.datiEventoMatrimonio.numeroTestimoni'),
]


def traccia(dest):
    """Il dettaglio: la stessa azione vista come sequenza, attraverso i processi."""
    im, dr, y = W.pagina(
        L, 980, ['Home', 'Errori e diagnostica', 'Traccia'],
        'Traccia 4bf92f3577b34da6a3ce929d0e0e4736',
        azioni_dx=['COPIA IDENTIFICATIVO', 'APRI L’ATTO'],
        sotto='Una sola azione dell’operatore, vista attraverso i processi che ha '
              'attraversato. È ciò che oggi non si può ricostruire.')

    y = W.righe_etichette(dr, X, y, [
        ('Atto', '1842/2026 — matrimonio'), ('Caso d’uso', '311111 — Matr_001'),
        ('Operatore', 'm.rossi'), ('Postazione', 'USC-MUN-01'),
        ('Avvio', '09/11/2026 17:42:09.114'), ('Durata totale', '2.180 ms'),
        ('Esito', 'ERRORE — ANSC-400001'), ('Ambiente', 'Produzione'),
        ('Versione', 'all-ansc-sipo 1.4.2'),
    ], C, colonne=3)
    y += 10

    # ── la cascata degli span
    y = W.pannello(dr, X, y, C, 'La sequenza, in scala sui tempi')
    x0, larg_barre = X + 250, C - 250 - 150
    scala = larg_barre / 2200.0
    # righello
    for ms in range(0, 2201, 500):
        xx = x0 + ms * scala
        dr.line([(xx, y + 2), (xx, y + 10 + len(DURATE) * 30)], fill='#eef0f3')
        dr.text((xx - 10, y - 12), '%d ms' % ms, font=fnt(F_REG, 9), fill=MUTED)
    for prof, servizio, operazione, inizio, durata, esito in DURATE:
        colore = W.ROSSO if esito == 'ko' else W.VERDE
        dr.text((X + 12 + prof * 14, y + 7), servizio, font=fnt(F_BLD, 10), fill=W.INK)
        bx, bw = x0 + inizio * scala, max(6, durata * scala)
        dr.rounded_rectangle([bx, y + 5, bx + bw, y + 21], radius=5, fill=colore)
        et = '%s — %d ms' % (operazione, durata)
        if bw > 320:
            dr.text((bx + 8, y + 8), et, font=fnt(F_REG, 10), fill='white')
        else:
            dr.text((bx + bw + 8, y + 8), et, font=fnt(F_REG, 10), fill=W.INK)
        y += 30
    y += 14

    # ── gli eventi agganciati
    y = W.pannello(dr, X, y, C, 'Gli eventi registrati lungo la traccia')
    y = W.tabella(dr, X, y, C, ['Ora', 'Liv.', 'Origine', 'Servizio', 'Codice', 'Messaggio'],
                  [120, 70, 86, 150, 140, 586],
                  [[o, (lv, LIVELLO[lv]), (og, ORIGINE[og]), sv, cd, ms]
                   for o, lv, og, sv, cd, ms in EVENTI])

    W.nota(dr, X, y + 6, C,
           'La riga in errore e quella di attenzione appartengono alla stessa traccia delle '
           'righe di avvio: è questo che permette di dire «l’atto 1842 si è fermato perché '
           'mancavano i testimoni, dopo che il numero comunale era già stato staccato». '
           'Senza identificativo di traccia le sei righe resterebbero in quattro registri '
           'separati, senza nulla che le leghi.', W.VERDE)
    return W.salva(im, dest, 'otel_bo_traccia.png', voci_menu=MENU)


if __name__ == '__main__':
    for f in (errori, traccia):
        print('scritto:', os.path.relpath(f(DEST), os.path.dirname(QUI)))
