# -*- coding: utf-8 -*-
"""Diagrammi PowerPoint dell'analisi delle nascite gemellari v0.9 (21/11/2026): il caso 1 con il
testo dell'atto GENERATO DA SIPO e trasmesso con la validazione (composizioneCompleta), come
indica ANSC per le bozze prenotate da gestionale (issue #2299).

  * gem9_flusso_1, gem9_panoramica. PNG con qlmanage -t -s 2400.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_gemellari_v0_9_pptx.py
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import diagrammi_matrimonio_pptx as M           # noqa: E402
import diagrammi_gemellari_v0_4_pptx as G4      # noqa: E402
import diagrammi_gemellari_v0_5_pptx as G5      # noqa: E402

DIR = G4.DIR


def flusso_1():
    passi = list(G5.PASSI_1)
    k = [i for i, t in enumerate(passi) if t[1] == 'DEFINISCI · numeri e prenotazione'][0]
    t = passi[k]
    passi.insert(k + 1, (t[0], 'Raccordo dei numeri comunali', 'finestra: per ciascun gemello il '
                         'numero comunale in grande e l’idAnsc che lo contiene; PROSEGUI',
                         '', t[4], 'N righe\nPRENOTATO · NUMERO_ATTO · ID_ANSC', 'N atti\n1 BOZZA',
                         t[7]))
    i = [k for k, x in enumerate(passi) if x[1] == 'Anteprima · Validazione del gemello k'][0]
    t = passi[i]
    passi[i] = (t[0], 'Testo e validazione del gemello k', 'SIPO compone il testo con il '
                'formulario (numero comunale, idAnsc dei fratelli); R009 lo trasmette',
                'PKG_FORMULARI\nR009 composizioneCompleta', *t[4:])
    return M.genera(
        passi, 'Parto plurimo — caso 1: gemelli con lo stesso UC, tutto da SIPO',
        'Dopo la divisione il riepilogo mostra i dati che il numeratore assegnerà; DEFINISCI '
        'stacca i numeri, prenota gli atti, mostra il raccordo dei numeri e accompagna un gemello '
        'alla volta fino alla firma; il testo di ciascun atto lo compone SIPO e lo invia ad ANSC.',
        os.path.join(DIR, 'gem9_flusso_1.pptx'), nota=G5.NOTA_1, colore_nota='blu',
        fasi_viola=(), etichetta_viola='ciclo per gemello',
        sottotitolo_niente='fino alla prenotazione')


def panoramica():
    return G4.panoramica(os.path.join(DIR, 'gem9_panoramica.pptx'), caso1=(
        ('Riepilogo dei gemelli', 'per ciascun nato UC comune e numero comunale previsto, non '
         'riservato'),
        ('DEFINISCI · raccordo dei numeri', 'N numeri e R009 /prenota/evento; poi per ciascun '
         'gemello testo di SIPO inviato con la validazione, firme, definizione'),
        ('Esito del parto · ripresa', 'tutti formati e definiti; se interrotto, RIPRENDI dal '
         'riepilogo senza nuovi numeri')),
        piede=('In entrambi i casi il testo dell’atto lo compone SIPO; una finestra di raccordo '
               'mostra i numeri comunali; una riga di ANSC_STATO_ATTO e una di ANSC_SOGGETTO_ATTO '
               'per gemello',
               'Caso 1: il testo viaggia con la validazione (composizioneCompleta). Caso 2: '
               'l’ufficiale lo copia sulla web app'),
        caso2=(('DATI PER ANSC · pratica guidata', 'N numeri in blocco e raccordo; poi un gemello '
                'alla volta con COPIA TESTO; ATTESA WEBAPP'),
               ('Web app ANSC', 'prenotazione con i numeri di SIPO; caso d’uso di servizio con la '
                'tipologia di nascita e il testo copiato; firme'),
               ('RECUPERA GEMELLI · DEFINISCI GEMELLI', 'R005 per numero, raccordo e abbinamento '
                'per gemello, poi la definizione in SIPO')))


if __name__ == '__main__':
    for p in (flusso_1(), panoramica()):
        print('scritto:', os.path.relpath(p, QUI))
