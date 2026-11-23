# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.3 (20/11/2026), dal FILE REALE della v0.2.

Richiesta dell'utente: chiarire se gli atti di nascita dei gemelli si possano formare con i servizi
cooperativi. Nel capitolo «ANSC», sezione «Il completamento di ciascun atto», il paragrafo finale
(«Dal 9 settembre 2024 …») diventa la sottosezione «Che cosa si può fare con i servizi cooperativi»:
  * tabella dei passi del percorso descritto da ANSC, con la disponibilità tramite servizi cooperativi
    e la fonte (prenotazione sì, completamento con il caso di servizio no, firme sì);
  * le vie che le fonti non dichiarano (bozza completata con l'UC ordinario, prenotazione con un UC
    diverso dal caso di servizio, nascite singole senza prenotazione) e i loro ostacoli;
  * il nato morto e numeroGemelliNatiVivi (GE-03);
  * la conclusione: oggi solo il percorso B è interamente coerente con le regole ANSC.
Il capitolo «La modalità di integrazione» si allinea nel paragrafo d'apertura. Storia e frontespizio.

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_3.py
"""
import os
import sys

import docx

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import par, tabella, voce               # noqa: E402
from gemellari_v0_2 import heading, in_coda, para_che_inizia, sposta_prima  # noqa: E402

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.2.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.3.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '20/11/2026'

PASSI = [
    ['#', 'Passo del percorso ANSC', 'Operazione', 'Tramite servizi cooperativi', 'Fonte'],
    ['1', 'Prenotazione: ANSC crea un atto in bozza per ciascun gemello e ne restituisce '
          'l’identificativo nazionale.',
     'R009 /prenota/evento', 'Sì. Introdotta nel rilascio 1.9.0, corretta nel 1.23.0, presente '
     'nel contratto in vigore; la comunicazione del 2024 non la nomina.', '[A1], [A6], [A7]'],
    ['2', 'Completamento di ciascun atto: dati, minuta con le formule 35-37 e gli identificativi '
          'dei fratelli, validazione.',
     'R009 /validazione/evento con il caso d’uso di servizio 11999999',
     'No. Dal 09/09/2024 il caso 11999999 «non è più disponibile tramite servizi cooperativi»; '
     'resta solo sulla web app.', '[A3] p. 43, [A7]'],
    ['3', 'Firma dei dichiaranti, solo cartacea, acquisita come processo verbale.',
     'R006 (caricamento del modulo firmato)', 'Sì.', '[A3] p. 44'],
    ['4', 'Firma dell’USC; poi si passa all’atto del gemello successivo.',
     'R007', 'Sì.', '[A3] p. 44'],
]


def main():
    d = docx.Document(IN)
    b = d.element.body

    # 1. il paragrafo finale di «Il completamento di ciascun atto» diventa una sottosezione
    vecchio = para_che_inizia(d, 'Dal 9 settembre 2024 i casi d’uso di servizio')
    assert not D.ha_commenti(vecchio._p)
    racc = in_coda(d)
    heading(d, 3, 'Che cosa si può fare con i servizi cooperativi')
    par(d, 'La risposta non è unica: dipende dal passo. Il percorso che la guida descrive per il '
        'parto plurimo ha quattro passi, e solo quello in cui l’atto si forma davvero, il '
        'completamento, è legato a un caso d’uso che ANSC ha tolto dai servizi cooperativi.')
    tabella(d, PASSI, [0.3, 2.0, 1.35, 1.95, 0.75])
    par(d, 'Dal gestionale si può quindi prenotare e firmare, ma non completare l’atto come la guida '
        'prescrive: «il caso d’uso predisposto per i parti gemellari è un caso d’uso di servizio» '
        '[A3], e i casi d’uso di servizio delle dichiarazioni, fra cui 11999999, dal 9 settembre '
        '2024 restano utilizzabili solo sulla web app [A7].')
    par(d, 'Le fonti lasciano aperte tre vie che non dichiarano. Nessuna è documentata da ANSC, e '
        'tutte vanno provate in preproduzione prima di farvi affidamento:')
    voce(d, 'Completare la bozza prenotata con l’UC ordinario del singolo nato.',
         'È la via suggerita dal payload di test della prenotazione, che passa 11111000 [A8], ed è '
         'quella su cui si regge il percorso A. Tre ostacoli: i campi gemellari del modello evento '
         'non sono in nessuno dei 374 mapping, quindi la validazione con l’UC ordinario non li '
         'richiede e non è detto che li accetti; non è noto con quale campo la validazione '
         'riconosca la bozza prenotata, e un errore produce un duplicato (GE-02); la minuta che '
         'ANSC compone per l’UC ordinario non cita i fratelli, e le formule 35-37 non compaiono '
         'in alcun mapping (GE-10).')
    voce(d, 'Prenotare con un UC diverso dal caso di servizio.',
         'idUsecase è obbligatorio nella richiesta, ma il contratto non dice quali valori accetti: '
         'l’esempio è «1170», il payload di test 11111000. Non è noto se una prenotazione con '
         '11999999 sia ancora accettata tramite servizi cooperativi, né se l’UC della bozza si '
         'possa cambiare al completamento (GE-04).')
    voce(d, 'Formare ogni gemello come una nascita singola, senza prenotazione.',
         'Tecnicamente il deposito con l’UC ordinario passa, ma gli atti non si citerebbero a '
         'vicenda, contro le formule ministeriali del parto plurimo. Il documento non la propone.')
    par(d, 'Un punto riguarda il parto misto. Il campo della richiesta si chiama '
        'numeroGemelliNatiVivi: su tre gemelli con un nato morto il contratto lascia intendere che '
        'se ne prenotino due. Nessuna fonte dice se l’atto del nato morto si prenoti comunque o si '
        'formi a parte con l’UC della sua variante (11111100, Dic_Nasc_002), né come gli atti dei '
        'fratelli lo citino (GE-03).')
    par(d, 'In conclusione, allo stato delle fonti il solo percorso interamente coerente con le '
        'regole di ANSC è quello che completa gli atti sulla web app, cioè il percorso B del '
        'capitolo seguente. Il percorso A regge sulla prenotazione e sulle firme, ma il '
        'completamento dal gestionale resta condizionato alla risposta di Sogei (GE-01). È la '
        'questione da cui dipende tutto il capitolo sull’integrazione.')
    sposta_prima(racc(), vecchio._p)
    vecchio._p.getparent().remove(vecchio._p)

    # 2. apertura del capitolo «La modalità di integrazione»
    fatti = []
    D.sostituisci(d, 'A è il percorso di riferimento se Sogei conferma il completamento con l’UC '
                  'ordinario; B è il ripiego, e coincide con la strategia adottata per gli atti che '
                  'SIPO non può formare [R2].',
                  'B è oggi il solo percorso interamente coerente con le regole di ANSC, perché '
                  'completa gli atti sulla web app, e coincide con la strategia adottata per gli atti '
                  'che SIPO non può formare [R2]; A, tutto da SIPO, diventa il percorso di '
                  'riferimento se Sogei conferma il completamento delle bozze con l’UC ordinario.',
                  attese=1, etichetta='apertura integrazione', fatti=fatti)

    # 3. GE-01: il riepilogo della risposta
    op = D.trova_tabella(d, 'tema', 'questione')
    for r in op.rows:
        if r.cells[0].text.strip() == 'GE-01':
            D.riscrivi_cella(r.cells[2], r.cells[2].text.replace(
                'Decide fra il percorso A e il percorso B.',
                'Tramite servizi cooperativi oggi si possono fare la prenotazione e le firme, non il '
                'completamento con il caso di servizio. Decide fra il percorso A e il percorso B.'))
            assert 'oggi si possono fare' in r.cells[2].text

    # 4. frontespizio e storia
    for fatto in D.frontespizio(d, '0.3', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.3', 'ANSC · La modalità di integrazione · Punti aperti',
             'Nella sezione sul completamento di ciascun atto, la sottosezione «Che cosa si può fare '
             'con i servizi cooperativi»: i quattro passi del percorso ANSC con la disponibilità '
             'tramite servizi cooperativi (prenotazione e firme sì, completamento con il caso di '
             'servizio no), le tre vie non dichiarate dalle fonti e i loro ostacoli, il nato morto '
             'nella prenotazione. Il percorso B è indicato come il solo oggi interamente coerente '
             'con le regole ANSC; il percorso A resta condizionato a GE-01.')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), fatti)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
