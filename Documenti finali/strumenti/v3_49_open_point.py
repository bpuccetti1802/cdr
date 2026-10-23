# -*- coding: utf-8 -*-
"""v3.49 dell'analisi ANSC, dalla v3.48 (23/10/2026): due open point chiesti dall'utente.

  OP-77  le contraddizioni del §«Il passo VALIDA» con la regola del ritorno ai dati (stato 0):
         le risolverà l'utente;
  OP-78  quale UC valga prima del Riepilogo (l'intestatario si legge da SOGGETTI_USECASE nella
         pagina dei dati anagrafici) e l'esito di un UC non determinabile, che può sfociare in
         un atto a testo libero, la cui modalità non è ancora scelta.
Nella fase A di «Le quattro fasi» il [DA VERIFICARE] diventa il rimando a OP-78.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_49_open_point.py
"""
import os
import sys

import docx

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.48.docx')
OUT = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.49.docx')

NUOVI = [
    ('OP-77', 'Il passo «VALIDA» e il ritorno ai dati',
     'Il paragrafo sul passo «VALIDA» descrive la pagina che segue la validazione come pagina '
     'finale di solo salvataggio in SIPO, da cui «non si potrà più tornare indietro». La sezione '
     '«Le quattro fasi» e la nota sullo stato bozza consentono invece di tornare ai dati fino alla '
     'firma dell’ufficiale, con lo stato 0 e una nuova validazione dello stesso atto, e dopo le '
     'firme dei dichiaranti solo se tutti possono firmare di nuovo. Le due descrizioni vanno '
     'ricondotte a una; si lega a OP-75 (a) e a OP-76 (c).',
     'Aperto', 'Analisi', 'Media'),
    ('OP-78', 'L’UC prima del Riepilogo e l’UC non determinabile',
     'Due aspetti della scelta dell’UC. (a) La pagina dei dati anagrafici legge da '
     'SOGGETTI_USECASE quale soggetto sia l’intestatario, ma l’UC si determina soltanto nel '
     'Riepilogo: quando il Modello indirizza più UC con intestatari diversi va stabilito su quale '
     'UC si legga l’intestatario, o se la pagina debba attendere la determinazione. (b) Quando '
     'nessun UC è determinabile, o il caso non è previsto da ANSC, l’atto può sfociare in un atto a '
     'testo libero, le cui due modalità sono descritte nella sezione «Atti a Testo Libero» ma non '
     'ancora scelte: finché la scelta non è fatta il percorso non ha un esito per questo caso. Si '
     'lega a OP-32 e a OP-66.',
     'Aperto', 'Analisi / Cliente', 'Alta'),
]


def main():
    if os.path.exists(OUT):
        raise SystemExit('esiste già: ' + OUT)
    doc = docx.Document(SRC)
    t = next(t for t in doc.tables if t.rows[1].cells[0].text.startswith('OP-'))
    if t.rows[-1].cells[0].text.strip() != 'OP-76':
        raise SystemExit('ultima riga inattesa: ' + t.rows[-1].cells[0].text)
    for valori in NUOVI:
        r = D.clona_riga(t, valori)
        if D.ha_commenti(r._tr):
            raise SystemExit('la riga clonata porta un commento')
    D.sostituisci(doc, ' [DA VERIFICARE: quale UC si legga quando il Modello ne indirizza più '
                       'd’uno con intestatari diversi, perché la determinazione vera avviene nel '
                       'Riepilogo]',
                  ', ma l’UC si determina soltanto nel Riepilogo: quale UC valga prima, quando il '
                  'Modello ne indirizza più d’uno, è aperto (OP-78)', attese=1)
    D.storia(doc, '23/10/2026', '3.49', 'Il flusso operativo (Le quattro fasi) · Open Point',
             'Aggiunti OP-77 (il passo «VALIDA» descritto come punto di non ritorno, in contrasto '
             'con il ritorno ai dati fino alla firma dell’ufficiale) e OP-78 (quale UC valga prima '
             'del Riepilogo per individuare l’intestatario, e l’UC non determinabile che può '
             'sfociare in un atto a testo libero, la cui modalità non è ancora scelta).')
    D.frontespizio(doc, '3.49', 'ANALISI_Integrazione-ANSC_v3.49')
    doc.save(OUT)
    print('scritto:', OUT)


if __name__ == '__main__':
    main()
