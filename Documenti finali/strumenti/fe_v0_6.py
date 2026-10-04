# -*- coding: utf-8 -*-
"""ANALISI_Front-End-Angular v0.5 → v0.6 (02/10/2026).

Rilievo del committente: «non ci siamo persi qualche schermata che avevamo già definito
(es dizionari...)?». Il confronto con la v0.4 dice che dalla v0.4 non si è perso nulla —
tutti i 55 titoli e tutte le 16 tabelle sono ancora lì — ma conferma il rilievo nella
sostanza: la mappa delle schermate copriva **undici** voci, di cui il back-office era
rappresentato da tre righe generiche («supervisione», «notifiche», «configurazione»),
mentre il disegno del back-office ne definisce **diciassette** pagine, Dizionari ANSC e
Riconciliazione comprese. Aggiungendo nella v0.5 un capitolo per le sole schermate dei
certificati l'asimmetria è diventata evidente.

Interventi:
  1. nuova sezione «Le schermate del back-office» con l'inventario pagina per pagina dei
     componenti di libreria, derivato dalle tabelle «Campi, colonne e azioni» del disegno;
  2. corretti i conteggi che la v0.5 ha reso incoerenti: «undici schermate» → venticinque,
     «le funzioni da costruire sono quattro» → cinque (il capitolo dei certificati già
     dichiarava di essere «la quinta»);
  3. «tre micro-frontend» → quattro: mfOperation era stato introdotto nella v0.5 senza
     aggiornare l'elenco;
  4. [F8] era citato e non definito nei Riferimenti: citazione pendente, ora chiusa;
  5. due refusi nella frase riscritta a mano dal committente.

⚠️ Si modifica il file reale: porta riscritture manuali del committente.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/fe_v0_6.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Front-End-Angular_v0.5.docx')
DST = os.path.join(BASE, 'Documenti finali', 'ANALISI_Front-End-Angular_v0.6.docx')

# Inventario derivato dalle tabelle «Campi, colonne e azioni» del disegno del back-office
# [F8]: una riga per pagina, nell'ordine del capitolo «Le pagine».
BO_SCHERMATE = [
    ['Pagina del back-office', 'Componenti esistenti', 'Da costruire'],

    ['La home: il menu delle aree',
     'card-wrapper · grid · icon · badge (distintivo OTP) · navbar',
     'Nulla di grafico. Va costruita la lettura delle voci, che nel primo rilascio '
     'viene da un ConfigMap e non dalle quattro tabelle del registro.'],

    ['Supervisione atti',
     'table · table-toolbar · checkbox-table · select · daterange-picker · badge · '
     'button-icon · button · modal',
     '⚠️ La ricerca per identificativo ANSC o numero comunale: in SIPO non esiste alcun '
     'servizio che ritrovi un atto da quei valori. È un servizio da costruire, non una '
     'schermata.'],

    ['Dettaglio dell’atto',
     'accordion · tabs-horizontal · badge · button · modal · notification-toast',
     '—'],

    ['Allegati dell’atto',
     'table · upload-drag-drop · document-single-upload · input · checkbox · '
     'button-icon · badge · pdf-viewer',
     'Niente di proprio: condivide con il passo 6 le maschere di caricamento, che sono '
     'già fra le cinque funzioni da costruire.'],

    ['Gestione delle notifiche',
     'table · table-toolbar · select · badge · button-icon · modal',
     '—'],

    ['Configurazione dei casi d’uso — elenco',
     'table · table-toolbar · select · badge · button-icon · button · modal',
     '—'],

    ['Configurazione di un caso d’uso — dettaglio',
     'tabs-horizontal · table · select · select-autocomplete · input · checkbox · '
     'textarea · modal · spinner',
     'La vista di esito della simulazione su atto reale. I componenti ci sono tutti; '
     'la composizione — campo atteso, valore prodotto, scostamento — è nuova e va '
     'disegnata una volta sola, perché serve anche al confronto fra versioni.'],

    ['Catalogo dei casi d’uso di ANSC',
     'table · table-toolbar · date-picker · badge · button',
     '—'],

    ['Logiche di scelta',
     'table · select · textarea (a carattere fisso) · button-icon · modal · badge',
     '⚠️ L’area di modifica dell’espressione. Un’area di testo basta a immetterla, ma '
     'non evidenzia la sintassi e non segnala un errore di scrittura: se serva un '
     'editor dedicato è un punto aperto (OP-FE-16).'],

    ['Dizionari ANSC',
     'grid a due pannelli · table (domini e valori) · table-toolbar · date-picker · '
     'badge · button · modal',
     '—'],

    ['Riconciliazione delle decodifiche — elenco',
     'table · table-toolbar · select · select-autocomplete · input · badge («da '
     'mappare») · upload · button · modal',
     '—'],

    ['Riconciliazione delle decodifiche — dettaglio',
     'input · select · select-autocomplete · date-picker · badge · button · modal',
     '—'],

    ['Versioni della configurazione',
     'table · accordion (report d’impatto) · badge · button · button-icon · modal',
     'Il confronto riga per riga fra bozza e versione attiva: è la stessa composizione '
     'della simulazione, e per questo le due vanno disegnate insieme.'],

    ['Comandi e operazioni di servizio',
     'table · select · checkbox · button · spinner · notification-toast · modal',
     'Nessun componente. Il comando gira in secondo piano e la pagina non attende: '
     'serve l’interrogazione periodica dello stato, che è comportamento della '
     'schermata e non elemento grafico.'],

    ['Numerazione comunale',
     'table · input-number · button · button-icon · badge · modal',
     '—'],

    ['Pagine e menu',
     'table · select · checkbox · input-number · input · button · button-icon · modal',
     'L’anteprima del menu per un profilo scelto: riusa i componenti della home, '
     'mostrandoli con le abilitazioni di un altro utente.'],

    ['Postazioni e certificati',
     'table · table-toolbar · input · input-password · document-single-upload · '
     'button · button-icon · modal · notification-toast',
     'È la quinta funzione da costruire, descritta per esteso più avanti in questo '
     'stesso capitolo.'],
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    fatti = []

    # ---------------------------------------------------------------- 1. i conteggi
    D.sostituisci(
        d,
        'su undici schermate, le funzioni realmente da costruire sono quattro, e nessuna '
        'di esse è un problema di grafica. Sono maschere che SIPO non ha — il caricamento '
        'dei documenti, i campi che ANSC richiede e SIPO non raccoglie, la consegna del '
        'codice di sessione, lo stato ANSC nelle maschere di ricerca. Tutto il resto è '
        'composizione di componenti esistenti.',
        'su venticinque schermate — gli otto passi del percorso e le diciassette pagine '
        'del back-office — le funzioni realmente da costruire sono cinque, e nessuna di '
        'esse è un problema di grafica. Sono maschere che SIPO non ha: il caricamento dei '
        'documenti, i campi che ANSC richiede e SIPO non raccoglie, la consegna del codice '
        'di sessione, lo stato ANSC nelle maschere di ricerca e la gestione dei certificati '
        'di postazione. Tutto il resto è composizione di componenti esistenti, e le sezioni '
        'che chiudono il capitolo descrivono le cinque una per una.',
        attese=1, etichetta='conteggio delle schermate e delle funzioni', fatti=fatti)

    D.sostituisci(
        d, 'si prevedono tre micro-frontend: le maschere di stato civile, la parte di '
           'integrazione ANSC (finalizzazione, documenti, sessione) e il back-office. La '
           'suddivisione non è un dettaglio implementativo: segue i tre gruppi di utenti e '
           'i tre ritmi di rilascio.',
        'si prevedono quattro micro-frontend: le maschere di stato civile, la parte di '
        'integrazione ANSC (finalizzazione, documenti, sessione), il back-office e le '
        'operazioni di postazione. La suddivisione non è un dettaglio implementativo: segue '
        'i gruppi di utenti e i ritmi di rilascio.',
        attese=1, etichetta='quattro micro-frontend invece di tre', fatti=fatti)

    D.sostituisci(
        d, 'È la quinta funzione da costruire e non compariva fra le quattro del paragrafo '
           'precedente, perché',
        'È la quinta funzione da costruire e non compare fra le quattro del percorso di '
        'formazione, perché',
        attese=1, etichetta='rimando della quinta funzione', fatti=fatti)

    # ---------------------------------------------------------------- 2. due refusi
    D.sostituisci(
        d, 'la prima porzione del Sistema già terminate nella versione “stan alone” '
           'appartiene al remote delle operazioni, mfOperation che è la scelta coerente',
        'la prima porzione del Sistema già terminata nella versione «stand alone», '
        'appartiene al remote delle operazioni, mfOperation, che è la scelta coerente',
        attese=1, etichetta='refusi nella frase su mfOperation', fatti=fatti)

    # ---------------------------------------------------------------- 3. [F8] pendente
    t = D.trova_tabella(d, 'ID', 'Riferimento')
    D.clona_riga(t, (
        '[F8]', 'DISEGNO_Back-Office_ANSC_v0.5.docx',
        'Il disegno del back-office: struttura documentale, registro delle pagine e del '
        'menu, e una scheda per ciascuna delle pagine con le tabelle sottese e il '
        'comportamento di campi e bottoni. È la fonte dell’inventario dei componenti del '
        'back-office.'))
    fatti.append('[F8] definito nei Riferimenti: era citato e non dichiarato')

    # ---------------------------------------------------------------- 4. l'inventario
    ancora = D.h(d, 3, 'La maschera della sessione')

    def par(t, stile='Normal'):
        return D.para(d, ancora._p, t, stile=stile)

    par('Le schermate del back-office', 'Heading 3')
    par('Le schermate del percorso di formazione non sono tutte le schermate del '
        'front-end. Il back-office ne ha altre diciassette, già disegnate pagina per '
        'pagina nel documento dedicato [F8], e sulla tabella precedente comparivano '
        'aggregate in tre voci — supervisione, notifiche, configurazione — che non '
        'bastano a dire quali componenti servano. **La tabella seguente le riporta una '
        'per una**, nello stesso ordine del disegno, perché è l’inventario dei componenti '
        'ciò che permette di dire quanto resti da costruire: senza di esso una pagina '
        'come i dizionari o la riconciliazione delle decodifiche resta un titolo, non una '
        'stima.')
    par('⚠️ **Una avvertenza sul senso della colonna di destra.** «Da costruire» qui non '
        'significa «da disegnare»: significa che non esiste nella libreria un componente '
        'o una composizione già fatta. Tre voci ricorrono, e sono di natura diversa fra '
        'loro: una è un **servizio** che manca a SIPO — ritrovare un atto dal suo '
        'identificativo nazionale; due sono **composizioni** da disegnare una volta e '
        'riusare — l’esito di una simulazione e il confronto fra due versioni della '
        'configurazione, che hanno la stessa forma; una è una **decisione aperta** — se '
        'l’espressione di una logica di scelta meriti un editor con evidenziazione della '
        'sintassi.')
    # ⚠️ le didascalie di questo documento NON usano lo stile «Caption»: sono paragrafi
    # Normal con il corsivo e il corpo 9. Lo stile Caption è 11 pt e giustificato, e si
    # distinguerebbe dalle altre figure del documento.
    cap = par('Le diciassette pagine del back-office e i componenti che le realizzano. Le '
              'righe con un trattino a destra sono interamente composizione di componenti '
              'esistenti.')
    for r in cap.runs:
        r.italic = True
        r.font.size = docx.shared.Pt(9)
    D.tabella(d, ancora._p, BO_SCHERMATE, modello=d.tables[9],
              larghezze=[1.65, 2.55, 2.7])
    par('⚠️ **Il conto delle pagine non coincide con quello dei micro-frontend, e non '
        'deve.** Sedici di queste diciassette pagine stanno in un solo micro-frontend, il '
        'back-office; la diciassettesima — postazioni e certificati — sta in mfOperation, '
        'perché amministra gli strumenti con cui una postazione si presenta agli enti '
        'esterni e non la configurazione dell’integrazione. La granularità del '
        'micro-frontend segue il ritmo di rilascio, non il numero delle pagine: è la '
        'ragione per cui il disegno del back-office [F8] non prevede un micro-frontend '
        'per pagina.')
    fatti.append('nuova sezione «Le schermate del back-office» con le 17 pagine')

    # ---------------------------------------------------------------- 5. punto aperto
    t = D.trova_tabella(d, '#', 'Questione')
    esistenti = [r.cells[0].text.strip() for r in t.rows[1:]]
    n = max(int(x.rsplit('-', 1)[1]) for x in esistenti if x.startswith('OP-FE-')) + 1
    D.clona_riga(t, (
        'OP-FE-%d' % n,
        'Se l’immissione delle espressioni delle logiche di scelta richieda un editor con '
        'evidenziazione della sintassi e controllo di scrittura, o se basti un’area di '
        'testo. ⚠️ Dipende da quale linguaggio il committente adotterà per le espressioni, '
        'scelta che l’analisi lascia volutamente aperta.',
        'Architettura / Cliente'))
    fatti.append('OP-FE-%d aperto (editor delle espressioni)' % n)

    # ---------------------------------------------------------------- 6. testata e storia
    for tab in d.tables:
        if tab.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tab.rows:
                v = {'Versione': '0.6',
                     'Documento': 'ANALISI_Front-End-Angular_v0.6'}.get(
                        r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '02/10/2026', '0.6', 'Architettura · Processi Front-End · Riferimenti · '
             'Punti aperti',
             'Completato l’inventario delle schermate, che copriva gli otto passi del '
             'percorso di formazione ma rappresentava il back-office con tre voci '
             'aggregate: le diciassette pagine del disegno del back-office — fra cui i '
             'dizionari ANSC e la riconciliazione delle decodifiche — hanno ora ciascuna i '
             'propri componenti di libreria e il proprio residuo da costruire. Corretti di '
             'conseguenza i conteggi in prosa (venticinque schermate, cinque funzioni da '
             'costruire) e l’elenco dei micro-frontend, che non comprendeva mfOperation '
             'introdotto nella versione precedente. Aggiunto ai Riferimenti il disegno del '
             'back-office, che era citato come [F8] senza essere dichiarato. Un punto '
             'aperto nuovo.')
    fatti.append('testata e storia aggiornate')

    # ---------------------------------------------------------------- 7. grassetti
    def grassetti(p):
        if '**' not in p.text or D.ha_commenti(p._p):
            return 0
        pezzi = D.segmenta('', p.text)
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        for testo, gr in pezzi:
            run = p.add_run(testo)
            run.bold = gr
        return 1
    n = sum(grassetti(p) for p in d.paragraphs)
    for tab in d.tables:
        for r in tab.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    n += grassetti(p)
    fatti.append('%d paragrafi con grassetto applicato' % n)

    d.save(DST)
    print('\n'.join(' · ' + f for f in fatti))
    print('capitoli/tabelle/immagini:', D.riepilogo(DST))
    print('scritto:', os.path.relpath(DST, BASE))


if __name__ == '__main__':
    main()
