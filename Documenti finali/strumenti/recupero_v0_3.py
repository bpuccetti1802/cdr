# -*- coding: utf-8 -*-
"""v0.3 di «ANALISI_Recupero-Atti-WebApp_SIPO-ANSC» (10/11/2026).

Si modifica il FILE REALE della v0.2 (salvato in Word dall'utente). Rilievo dell'utente: nelle
pagine del back-office manca, nella testata, il pulsante che richiede il token OTP.
  * le tre figure del capitolo «La pagina del back-office per il recupero» sono sostituite:
    stato dell'OTP e pulsante RICHIEDI/RINNOVA OTP nella barra di servizio, accanto all'utente;
  * nuova figura con la finestra aperta dal pulsante (Figura 2), le successive rinumerate;
  * testo della voce sulla sessione, riga della tabella degli elementi, riga in «Che cosa serve».

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/recupero_v0_3.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import figura, par   # noqa: E402
import pagine_bo_recupero as PB   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.2.docx')
NOME = 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.3'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '10/11/2026'
IMG = PB.DEST

d = docx.Document(SRC)
body = d.element.body
fatti = []


def innesta_dopo(dopo, scrivi):
    sect = body.find(qn('w:sectPr'))
    n0 = len(list(body.iterchildren()))
    scrivi()
    nuovi = [ch for ch in list(body.iterchildren())[n0 - 1:] if ch is not sect
             and ch.getparent() is body]
    for ch in reversed(nuovi):
        dopo.addnext(ch)
    return len(nuovi)


def nel_run(p, vecchio, nuovo):
    """Sostituisce dentro un solo run, per non perdere il grassetto della testa della voce."""
    rr = [r for r in p.runs if vecchio in r.text]
    if len(rr) != 1:
        raise SystemExit('run non univoco: ' + vecchio[:50])
    rr[0].text = rr[0].text.replace(vecchio, nuovo)


def S(v, n, a, e):
    D.sostituisci(d, v, n, attese=a, etichetta=e, fatti=fatti)


if __name__ == '__main__':
    PB.elenco(), PB.aggancio(), PB.esito(), PB.otp()

    # 1. figure esistenti: prima il blob, poi la numerazione (dall'ultima)
    for did, png in [('Figura 2 — La pagina «Recupero', 'bo_rec_elenco.png'),
                     ('Figura 3 — La pagina «Aggancio', 'bo_rec_aggancio.png'),
                     ('Figura 4 — L’esito', 'bo_rec_esito.png')]:
        D.sostituisci_immagine(d, did, os.path.join(IMG, png))
    fatti.append('figure 2-4 sostituite')
    for a, b in [(5, 6), (4, 5), (3, 4), (2, 3)]:
        S('Figura %d — ' % a, 'Figura %d — ' % b, 1, 'figura %d → %d' % (a, b))

    # 2. voce sulla sessione e figura della finestra
    voce = [p for p in d.paragraphs if p.text.startswith('Sessione verso ANSC.')]
    assert len(voce) == 1
    nel_run(voce[0], 'La pagina mostra il distintivo di sessione come le altre pagine del '
                     'back-office che parlano con ANSC;',
            'Nella testata, accanto all’utente, la pagina mostra lo stato del codice di '
            'sessione e il pulsante per richiederlo;')

    def scrivi():
        par(d, 'Lo stato e il pulsante stanno nella barra di servizio, quindi si vedono da ogni '
               'pagina e non dipendono da quella aperta:')
        for t in ['**OTP ANSC assente**, in rosso, con il pulsante **RICHIEDI OTP**: ricerca in '
                  'ANSC e aggancio sono inibiti, le tabelle di SIPO restano consultabili.',
                  '**OTP ANSC valido**, in verde, con il tempo residuo e il pulsante **RINNOVA '
                  'OTP**.',
                  'Sotto i 15 minuti residui, la soglia di guardia proposta in [R1], lo stato '
                  'diventa giallo: conviene rinnovare prima di avviare una ricerca o un aggancio, '
                  'per non fermarsi a metà.']:
            par(d, t, 'List Paragraph')
        par(d, 'Il pulsante apre la finestra della figura: l’ufficiale genera il codice sulla '
               'web app OTP di ANSC, con smart card o SPID, e lo incolla. Con CONFERMA il '
               'codice va al concentratore (PUT /ansc/v1/sessione), che lo custodisce legato '
               'all’ufficiale e alla postazione e lo usa per le chiamate ad ANSC fino alla '
               'scadenza; il browser non lo conserva. Se il codice scade durante un’operazione, '
               'l’operazione si ferma con un messaggio e la finestra si riapre.')
        figura(d, os.path.join(IMG, 'bo_rec_otp.png'), 6.0,
               'Figura 2 — Il pulsante RICHIEDI OTP nella testata e la finestra del codice di '
               'sessione verso ANSC.')
    n = innesta_dopo(voce[0]._p, scrivi)
    fatti.append('stato e pulsante dell’OTP, figura 2 — %d elementi' % n)

    # 3. tabelle
    S('Distintivo di sessione', 'Stato dell’OTP e pulsante (testata)', 1, 'riga della sessione')
    S('Validità e minuti residui del codice di sessione verso ANSC; senza sessione la ricerca '
      'e l’aggancio sono inibiti.',
      'Nella barra di servizio, accanto all’utente: stato del codice di sessione verso ANSC '
      '(assente, valido con i minuti residui, in scadenza) e pulsante RICHIEDI OTP o RINNOVA '
      'OTP. Senza codice la ricerca e l’aggancio sono inibiti.', 1, 'contenuto della riga')
    serve = D.trova_tabella(d, 'Dove', 'Che cosa serve')
    righe = [r for r in serve.rows if r.cells[0].text == 'Registro delle pagine del back-office']
    assert len(righe) == 1
    nuova = D.clona_riga(serve, ('Testata del back-office', 'Stato dell’OTP e pulsante RICHIEDI '
                                 'OTP nella barra di servizio, comuni a tutte le pagine che '
                                 'parlano con ANSC. Il disegno del back-office [R7] oggi mette '
                                 'lo stato accanto al titolo: va allineato.'))
    ultima = serve.rows[-1]._tr
    righe[0]._tr.addnext(ultima)
    fatti.append('riga «Testata del back-office»')

    for f in D.frontespizio(d, '0.3', NOME, DATA):
        fatti.append(f)
    D.storia(d, DATA, '0.3', 'La pagina del back-office per il recupero · Che cosa cambia nel '
             'disegno',
             'Nella testata delle pagine di recupero lo stato del codice di sessione verso ANSC '
             'e il pulsante RICHIEDI OTP o RINNOVA OTP; nuova figura con la finestra del codice; '
             'figure successive rinumerate.')
    d.save(OUT)
    for f in fatti:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
