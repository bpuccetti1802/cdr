# -*- coding: utf-8 -*-
"""v3.14 — la rilettura di coerenza: le frasi che la nuova decisione ha reso false.

⚠️ È il passaggio che il progetto prescrive e che è già costato versioni: `verifica-conteggi`
controlla i numeri, non le formulazioni. Qui si cercano le frasi che descrivono al presente
un impianto superato — «le regole di determinazione coprono i Modelli», «i controlli di
copertura sono eseguiti automaticamente», «l'immissione manuale non è il modo in cui la
configurazione si popola» — perché un documento che si contraddice a distanza di capitoli è
peggio di uno incompleto: non si sa quale metà valga.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

# (vecchio, nuovo, occorrenze attese, etichetta)
SOSTITUZIONI = [
    # il capitolo cambia nome: la determinazione non è più una specie di regola
    ('Le regole di determinazione e di controllo',
     'La determinazione dell’UC e le regole di controllo', None, 'titolo del capitolo e rimandi'),

    # la modalità operativa
    ('Il concentratore risolve la riga ANSC_CFG_UC valida e, su di essa, valuta le regole di '
     'determinazione (ANSC_CFG_REGOLA) per stabilire quale UC di ANSC corrisponda ai dati '
     'dell’atto',
     'Il concentratore scorre gli UC configurati per quel Modello in ordine di priorità e '
     'valuta le rispettive condizioni (ANSC_CFG_UC_CONDIZIONE) sui dati che SIPO ha già '
     'registrato: il primo che risponde determina l’UC', 1, 'modalità operativa'),

    # il capitolo sulla mappatura
    ('le regole di determinazione stabiliscono a quale di essi conduca un Modello del Comune '
     'secondo i dati dell’atto',
     'le condizioni di applicabilità stabiliscono a quale di essi conduca un Modello del '
     'Comune secondo i dati dell’atto', 1, 'catena della configurazione'),

    # ⚠️ la frase che contraddice la decisione del Comune
    ('Da quanto precede si ricava che l’immissione manuale non è il modo in cui la '
     'configurazione si popola, e che pensarla così porterebbe a sottostimare il progetto nel '
     'punto sbagliato.',
     'Da quanto precede si ricava l’ordine di grandezza del lavoro. La configurazione la '
     'decidono i funzionari, ma nessuno può scrivere a mano sessantamila righe: '
     'l’importazione le prepara e l’operatore le esamina, conferma o corregge. La distinzione '
     'fra ciò che è stato proposto e ciò che qualcuno ha guardato è quindi essenziale, ed è '
     'registrata su ogni riga.', 1, 'popolamento della configurazione'),

    ('e che le regole di determinazione coprano tutti i Modelli e restino mutuamente '
     'esclusive, secondo i controlli descritti al capitolo 10.',
     'e che ogni UC attivo abbia una condizione di applicabilità e una priorità che lo '
     'distingua dagli altri UC dello stesso Modello.', 1, 'controlli prima dell’attivazione'),

    ('Prima dell’attivazione i controlli di copertura e di mutua esclusione sono eseguiti '
     'automaticamente, e il loro esito negativo impedisce l’attivazione. È il punto in cui il '
     'vantaggio della forma dichiarativa si traduce in una garanzia di esercizio.',
     'Prima dell’attivazione si verifica che ogni UC attivo abbia una condizione e una '
     'priorità, e che nessuna priorità sia ripetuta fra UC dello stesso Modello. ⚠️ La '
     'copertura e la mutua esclusione non sono più dimostrabili: su una query non si stabilisce '
     'per quali dati risponderà. Al loro posto sta la simulazione su atti reali, che per questo '
     'diventa il controllo principale e non un ausilio.', 1, 'controlli all’attivazione'),

    ('Sono tre regole di determinazione, ciascuna con due condizioni, e nessuna riga di codice.',
     'Sono tre UC configurati sullo stesso Modello, ciascuno con la propria condizione e la '
     'propria priorità.', 1, 'esempio del Modello 30'),

    ('il catalogo degli UC, l’obbligatorietà dei campi per ciascun UC, le regole di '
     'determinazione',
     'il catalogo degli UC, l’obbligatorietà dei campi per ciascun UC, le condizioni di '
     'applicabilità', 1, 'capitolo del versionamento'),

    ('regole di determinazione e di controllo, dizionari ANSC',
     'condizioni di applicabilità degli UC, regole di controllo, dizionari ANSC', 1,
     'elenco delle sezioni del back-office'),

    ('Entrambe le condizioni sono prevenibili prima dell’esercizio: sono esattamente ciò che i '
     'controlli di copertura e di mutua esclusione verificano al momento dell’attivazione di '
     'una versione di configurazione.',
     'Entrambe le condizioni si prevengono con la simulazione su atti reali prima '
     'dell’attivazione di una versione: non esiste un controllo che le escluda per '
     'costruzione, perché una condizione in forma di interrogazione non dichiara per quali '
     'dati risponderà.', 1, 'categorie di eccezione'),

    ('Si legge il Modello dell’atto dalla configurazione del tipo atto SIPO, si valutano le '
     'regole di determinazione associate a quel Modello e si ottiene l’UC applicabile. Se '
     'nessuna regola si attiva, o se ne attiva più di una, la verifica si interrompe qui con '
     'un errore esplicito',
     'Si legge il Modello dell’atto dalla configurazione del tipo atto SIPO, si scorrono gli UC '
     'configurati per quel Modello in ordine di priorità e si valuta la condizione di ciascuno '
     'sui dati già registrati: il primo che risponde determina l’UC. Se nessuno risponde la '
     'verifica si interrompe qui con un errore esplicito', 1, 'prima fase della preverifica'),

    ('quali regole di determinazione perdono copertura',
     'quali UC restano senza condizione di applicabilità', 1, 'report d’impatto'),

    ('Pre-filtro e regole di determinazione', 'Pre-filtro e determinazione dell’UC', None,
     'tabella dei componenti'),

    ('Manutenzione delle regole di determinazione',
     'Manutenzione delle condizioni di applicabilità e delle regole di controllo', None,
     'back-office'),

    ('Nessuna regola di determinazione si è attivata per il Modello dell’atto: la combinazione '
     'dei valori non è coperta dalle regole configurate',
     'Nessuna condizione di applicabilità ha risposto per il Modello dell’atto: i dati '
     'dell’atto non ricadono in alcuno degli UC configurati', 1, 'eccezione «UC non determinato»'),

    ('Più regole di determinazione si sono attivate sullo stesso atto producendo UC diversi: le '
     'condizioni si sovrappongono',
     'Più UC dello stesso Modello hanno risposto e la priorità non li distingue: le condizioni '
     'si sovrappongono', 1, 'eccezione «UC ambiguo»'),
]


def applica(doc):
    fatti = []
    for vecchio, nuovo, attese, etichetta in SOSTITUZIONI:
        D.sostituisci(doc, vecchio, nuovo, attese=attese, etichetta=etichetta, fatti=fatti)
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
