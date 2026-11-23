# -*- coding: utf-8 -*-
"""Diagrammi PowerPoint dell'analisi delle nascite gemellari v0.8 (21/11/2026).

  * gem8_flusso_1 — caso 1 con la finestra di raccordo dei numeri dopo la prenotazione e il
    testo dell'atto recuperato da ANSC e riportato in SIPO alla definizione di ciascun gemello;
  * gem8_flusso_2 — caso 2 con la finestra di raccordo prima della web app, la pratica guidata
    (un gemello alla volta, COPIA TESTO) e la finestra di raccordo dopo il recupero;
  * gem8_panoramica — i due casi con le stesse novità.
I PNG si ottengono con qlmanage (-t -s 2400), come per le versioni precedenti.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v0_8_pptx.py
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagrammi_matrimonio_pptx as M           # noqa: E402
import diagrammi_gemellari_v0_4_pptx as G4      # noqa: E402
import diagrammi_gemellari_v0_5_pptx as G5      # noqa: E402

DIR = G4.DIR


def _sostituisci(passi, titolo, nuovo):
    i = [k for k, t in enumerate(passi) if t[1] == titolo]
    assert len(i) == 1, titolo
    passi[i[0]] = nuovo


def flusso_1():
    passi = list(G5.PASSI_1)
    k = [i for i, t in enumerate(passi) if t[1] == 'DEFINISCI · numeri e prenotazione'][0]
    t = passi[k]
    passi.insert(k + 1, (t[0], 'Raccordo dei numeri comunali', 'finestra: per ciascun gemello il '
                         'numero comunale in grande e l’idAnsc che lo contiene; PROSEGUI',
                         '', t[4], 'N righe\nPRENOTATO · NUMERO_ATTO · ID_ANSC', 'N atti\n1 BOZZA',
                         t[7]))
    t = [x for x in passi if x[1] == 'Anteprima · Validazione del gemello k'][0]
    _sostituisci(passi, t[1], (t[0], t[1], 'testo composto da ANSC con gli idAnsc dei fratelli; '
                               'R009 all’apertura, poi R010 senza filigrana', 'R009 /validazione/'
                               'evento\nR010 /anteprima/evento', *t[4:]))
    t = [x for x in passi if x[1] == 'Definizione del gemello k'][0]
    _sostituisci(passi, t[1], (t[0], 'Testo da ANSC e definizione', 'il testo dell’atto viene '
                               'da ANSC e si riporta sull’atto SIPO; poi la definizione',
                               'ATTO_SCANSIONATO\n/finalizzaAtto', *t[4:]))
    return M.genera(
        passi, 'Parto plurimo — caso 1: gemelli con lo stesso UC, tutto da SIPO',
        'Dopo la divisione il riepilogo mostra i dati che il numeratore assegnerà; DEFINISCI '
        'stacca i numeri, prenota gli atti, mostra il raccordo dei numeri e accompagna un gemello '
        'alla volta fino alla firma; il testo dell’atto si recupera da ANSC.',
        os.path.join(DIR, 'gem8_flusso_1.pptx'), nota=G5.NOTA_1, colore_nota='blu',
        fasi_viola=(), etichetta_viola='ciclo per gemello',
        sottotitolo_niente='fino alla prenotazione')


def flusso_2():
    passi = []
    for t in G4.PASSI_2:
        if t[1] == 'Riepilogo · UC diversi':
            t = (t[0], t[1], 'riepilogo dei gemelli: DEFINISCI non compare; il messaggio indica '
                 'la web app; DATI PER ANSC') + t[3:]
        elif t[1] == 'DATI PER ANSC · numeri in blocco':
            t = (t[0], t[1], 'N numeri consecutivi; il parto resta raggruppato in SIPO') + t[3:]
        elif t[1] == 'Dati per ANSC del parto':
            passi.append((t[0], 'Raccordo dei numeri · da riportare', 'finestra: il numero '
                          'comunale di ciascun gemello in grande e l’ordine sulla web app', *t[3:]))
            t = (t[0], 'Pratica guidata · gemello k', 'un gemello alla volta: numero, tipologia '
                 'di nascita, testo di SIPO con COPIA TESTO; promemoria', *t[3:])
        elif t[1] == 'Esito del recupero':
            t = (t[0], 'Raccordo dei numeri · esito del recupero', 'gemello per gemello: '
                 'abbinato · non trovato · non firmato · incoerente; riga in ANSC_SOGGETTO_ATTO') \
                + t[3:]
        passi.append(t)
    return M.genera(
        passi, 'Parto plurimo — caso 2: gemelli con UC diversi, web app e recupero in SIPO',
        'Compilazione, divisione e numeri restano in SIPO; la pratica guidata porta i testi dei '
        'gemelli sulla web app, dove si prenotano, si completano e si firmano gli atti; '
        'RECUPERA GEMELLI aggancia gli N atti e DEFINISCI GEMELLI li definisce in SIPO.',
        os.path.join(DIR, 'gem8_flusso_2.pptx'), nota=G4.NOTA_2, colore_nota='blu',
        non_ritorno=False, fasi_viola=('Web app',), etichetta_viola='web app ANSC',
        sottotitolo_niente='finché non si va sulla web app')


def panoramica():
    return G4.panoramica(os.path.join(DIR, 'gem8_panoramica.pptx'), caso1=(
        ('Riepilogo dei gemelli', 'per ciascun nato UC comune e numero comunale previsto, non '
         'riservato'),
        ('DEFINISCI · raccordo dei numeri', 'N numeri e R009 /prenota/evento; poi per ciascun '
         'gemello validazione, firme, testo da ANSC riportato in SIPO, definizione'),
        ('Esito del parto · ripresa', 'tutti formati e definiti; se interrotto, RIPRENDI dal '
         'riepilogo senza nuovi numeri')),
        piede=('In entrambi i casi: una riga di ANSC_STATO_ATTO e una di ANSC_SOGGETTO_ATTO per '
               'ciascun gemello; una finestra di raccordo mostra i numeri comunali',
               'Nel caso 1 la riga del nato nasce alla prenotazione; nel caso 2 al recupero, quando '
               'l’atto formato sulla web app si abbina al gemello'),
        caso2=(('DATI PER ANSC · pratica guidata', 'N numeri in blocco e raccordo; poi un gemello '
                'alla volta con COPIA TESTO; ATTESA WEBAPP'),
               ('Web app ANSC', 'prenotazione con i numeri di SIPO; caso d’uso di servizio con la '
                'tipologia di nascita e il testo copiato; firme'),
               ('RECUPERA GEMELLI · DEFINISCI GEMELLI', 'R005 per numero, raccordo e abbinamento '
                'per gemello, poi la definizione in SIPO')))


if __name__ == '__main__':
    for p in (flusso_1(), flusso_2(), panoramica()):
        print('scritto:', os.path.relpath(p, QUI))
