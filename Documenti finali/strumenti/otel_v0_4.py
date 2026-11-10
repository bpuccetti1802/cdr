# -*- coding: utf-8 -*-
"""v0.4 di «PROPOSTA_Osservabilita-OpenTelemetry»: il diagramma ER delle tabelle.

Si parte dal FILE REALE della v0.3, rivisto a mano dall'utente (titoli «Perché OT in
un’architettura a microservizi», «Gestire i log del front-end», seconda sezione «Note»).
Non rieseguire `otel_v0_3.py`.

Che cosa fa:
  * nella sezione «Le tabelle sottese» (capitolo del back-office, dove tutte le tabelle sono
    ormai definite) la figura ER (`diagrammi_otel.erd`) e la tabella dei legami;
  * un rimando alla figura dal paragrafo del registro diagnostico;
  * OT-16: nella DDL di [R1] la chiave esterna dell'audit richiama
    ANSC_STATO_ATTO(ID_STATO_ATTO), ma nella v3.60 la tabella ha come chiave ID_ATTO_SIPO e
    non ha più quella colonna;
  * il rimando al capitolo rinominato e il titolo di capitolo vuoto lasciato dopo i
    Riferimenti (produce una riga bianca nell'indice).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/otel_v0_4.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D          # noqa: E402
from otel_v0_2_api import par, voce, tabella   # noqa: E402
import diagrammi_otel           # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.3.docx')
OUT = os.path.join(BASE, 'Documenti finali', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.4.docx')
DATA = '10/11/2026'

LEGAMI = [
    ['Da', 'A', 'Legame', 'Molteplicità', 'Perché così'],
    ['ANSC_LOG_EVENTO.COD_EVENTO', 'ANSC_CFG_CODICE_EVENTO', 'Per valore', 'Molti a uno',
     'Un codice non ancora catalogato deve essere registrato lo stesso: è proprio l’evento '
     'nuovo che interessa.'],
    ['ANSC_LOG_EVENTO.TRACE_ID + SPAN_ID', 'ANSC_LOG_SPAN', 'Per valore', 'Molti a uno; uno '
     'span senza eventi è normale', 'Eventi e span arrivano dal collector separati e in tempi '
     'diversi: l’evento può precedere lo span che lo contiene.'],
    ['ANSC_LOG_SPAN.SPAN_ID_PADRE', 'ANSC_LOG_SPAN', 'Per valore', 'Molti a uno',
     'La cascata è un albero, e gli span di processi diversi arrivano in ordine qualsiasi.'],
    ['ANSC_LOG_AUDIT.TRACE_ID', 'ANSC_LOG_EVENTO, ANSC_LOG_SPAN', 'Per valore', 'Uno a molti',
     'L’audit si conserva più a lungo della diagnostica: la riga probatoria deve sopravvivere '
     'alla scadenza della sua traccia.'],
    ['ANSC_LOG_AUDIT.ID_STATO_ATTO', 'ANSC_STATO_ATTO', '**Chiave esterna**', 'Molti a uno',
     'L’unico vincolo dichiarato: è ciò che dà all’audit il suo valore probatorio. Vedi '
     'OT-16.'],
    ['ANSC_LOG_EVENTO, piano 1 (ID_ATTO_SIPO, ID_ANSC, NUMERO_ATTO)', 'ANSC_STATO_ATTO',
     'Per valore', 'Molti a uno', 'Si registrano anche eventi di un atto che nello store non '
     'c’è ancora, o non c’è più.'],
    ['ANSC_LOG_EVENTO, piano 2 (ID_ALLEGATO, ID_ANSC_ALLEGATO)', 'MATR_USR.ALLEGATO',
     'Per valore', 'Molti a uno', 'Altro schema; e l’allegato può non appartenere ancora ad '
     'alcun atto.'],
    ['ANSC_LOG_EVENTO, piano 3 (ID_SOGGETTO_SIPO, ID_ANSC_SOGGETTO)',
     'ANSC_SOGGETTO_IDENTIFICATIVI', 'Per valore', 'Molti a uno', 'Il soggetto si registra '
     'dalla prima ricerca, prima che la riga degli identificativi esista.'],
    ['ANSC_LOG_EVENTO, piano 3 (ID_SCHEDA_ANPR, ID_UNICO_NAZIONALE)', 'ANAG_USR.SOGGETTO',
     'Per valore', 'Molti a uno', 'Altro schema: nessuna chiave esterna attraversa gli schemi '
     '[R1].'],
    ['ANSC_LOG_SPAN.ID_ATTO_SIPO', 'ANSC_STATO_ATTO', 'Per valore', 'Molti a uno',
     'Come per gli eventi. Non è disegnato in figura, per leggibilità.'],
]


def schema(doc, modello, png):
    D.sostituisci(doc, 'Le tabelle sottese', 'Le tabelle sottese e i loro legami', attese=1)
    prima = D.h(doc, 1, 'Gestire i log del front-end')._p
    par(doc, prima,
        'La figura che segue mette insieme le tabelle nuove della proposta e quelle del modello '
        'dell’integrazione a cui si collegano. Si legge in due righe: in alto il registro '
        'diagnostico, le tracce e il catalogo dei codici; in basso l’audit probatorio con le '
        'colonne proposte, e le tabelle esistenti che gli eventi richiamano attraverso i tre '
        'piani di tracciabilità.')
    D.immagine(doc, prima, png, 6.5,
               'Figura 4 — Le tabelle del registro e i loro legami: una sola chiave esterna, '
               'tutti gli altri riferimenti per valore.')
    par(doc, prima,
        '**Una sola chiave esterna, ed è quella che c’era già.** Il legame fra l’audit e lo '
        'stato dell’atto resta un vincolo, perché è ciò che rende probatoria la riga. Tutti gli '
        'altri sono riferimenti per valore, e non per trascuratezza: il registro deve accettare '
        'eventi di oggetti che non esistono ancora o non esistono più, e una chiave esterna fra '
        'tabelle partizionate per giorno impedirebbe di eliminare le partizioni scadute, che è '
        'il modo previsto per la conservazione.')
    tabella(doc, prima, LEGAMI, modello, [1.6, 1.3, 0.8, 0.9, 1.9])
    par(doc, prima,
        'La ricerca segue i riferimenti per valore grazie agli indici locali su TRACE_ID e sugli '
        'identificativi dei tre piani. Dove un riferimento non trova la riga di arrivo, il '
        'back-office mostra l’evento comunque e segnala che l’oggetto non è (più) presente.')


def rimandi(doc):
    fatti = []
    D.sostituisci(doc, 'cap. «Perché serve in un’architettura a microservizi»',
                  'cap. «Perché OT in un’architettura a microservizi»', attese=1,
                  etichetta='rimando al capitolo rinominato', fatti=fatti)
    D.sostituisci(doc, 'Sedici questioni.', 'Sedici questioni.', attese=0)
    D.sostituisci(doc, 'Quindici questioni.', 'Sedici questioni.', attese=1,
                  etichetta='conteggio dei punti aperti', fatti=fatti)
    # titolo di capitolo vuoto dopo i Riferimenti: riga bianca nell'indice
    vuoti = [p for p in doc.paragraphs if p.style.name == 'Heading 1' and not p.text.strip()]
    for p in vuoti:
        p.style = doc.styles['Normal']
    fatti.append('titoli di capitolo vuoti riportati a testo normale — %d' % len(vuoti))
    # rimando alla figura dal registro diagnostico
    ancora = D.h(doc, 1, 'Dove si archivia e come si analizza')._p
    voce(doc, ancora, 'I legami con le altre tabelle.',
         'Sono riassunti nella Figura 4 e nella tabella che la segue, nel capitolo del '
         'back-office, dove anche le tracce e il catalogo dei codici sono ormai definiti.')
    # punto aperto
    D.clona_riga(D.trova_tabella(doc, 'Questione', 'A chi spetta'), (
        'OT-16', 'La DDL di ANSC_LOG_AUDIT in [R1] dichiara la chiave esterna verso '
        'ANSC_STATO_ATTO (ID_STATO_ATTO), ma nella versione corrente di [R1] ANSC_STATO_ATTO ha '
        'come chiave primaria ID_ATTO_SIPO e non ha più la colonna ID_STATO_ATTO, che la tabella '
        'descrittiva cita ancora. Così il vincolo non si crea. Va allineato in [R1]: o la colonna '
        'dell’audit diventa ID_ATTO_SIPO, o si ripristina la chiave tecnica.',
        'Redazione dell’analisi [R1]'))
    return fatti


if __name__ == '__main__':
    shutil.copyfile(SRC, OUT)
    doc = docx.Document(OUT)
    modello = D.trova_tabella(doc, 'Questione', 'A chi spetta')
    png = diagrammi_otel.erd()
    for f in rimandi(doc):
        print('  ' + f)
    schema(doc, modello, png)
    for f in D.frontespizio(doc, '0.4', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.4', DATA):
        print('  ' + f)
    D.storia(doc, DATA, '0.4', 'Il back-office del supporto · Punti aperti',
             'Aggiunto il diagramma entità-relazioni delle tabelle della proposta e dei loro '
             'legami con il modello dell’integrazione, con la tabella dei legami e la ragione '
             'di ciascuno: una sola chiave esterna, quella dell’audit verso lo stato dell’atto, '
             'tutti gli altri riferimenti per valore. Nuovo OT-16 sulla chiave esterna '
             'dell’audit, che in [R1] richiama una colonna non più presente.')
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
