# -*- coding: utf-8 -*-
"""v3.14 — il capitolo delle regole: dalla condizione dichiarativa alla query su SIPO.

⚠️ Questa è una revoca di PC-9, non un affinamento. La v3.0 aveva scelto condizioni
dichiarative `campo/operatore/valore` proprio per NON avere codice in configurazione, dopo
aver esaminato le `CFG_RULEAPP_FORMULA` di SIPO e averle scartate perché i loro script in
`SCRIPT_EXECUTION VARCHAR2(4000)` non sono manutenibili dai funzionari. La v3.14 torna a una
forma eseguibile, e il capitolo deve dire perché e a quale prezzo, altrimenti resta un
documento che si contraddice a distanza di quattro capitoli.

La ragione del cambiamento, nelle parole dell'utente: SIPO salva l'atto sul proprio database
prima di depositarlo in ANSC; poiché SIPO non governa la scelta dei documenti da allegare
mentre ANSC la fa dipendere dall'UC, è valutando i dati già scritti — con una query
configurata — che si sceglie l'UC giusto.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

ALTERNATIVE = [
    ('Condizioni dichiarative su campi (la scelta della v3.0)',
     'Una condizione è una terna campo, operatore, valore; le condizioni di una regola sono '
     'in congiunzione. È la forma più verificabile — se ne dimostrano copertura e mutua '
     'esclusione — e non richiede al funzionario di conoscere SQL. Si è però rivelata '
     'insufficiente all’uso: i dati che discriminano l’UC non stanno in un solo posto. Il '
     'discriminante delle nascite sta sul soggetto e non sull’atto; la scelta dei documenti '
     'da allegare dipende da informazioni che vivono su tabelle diverse. Esprimere questo con '
     'terne significa aggiungere alla configurazione un modo per dichiarare da quale tabella '
     'venga ciascun campo e come si leghi all’atto: cioè reinventare le giunzioni, con una '
     'grammatica peggiore di quella che esiste già.'),
    ('Un motore di regole di mercato',
     'Scartata per la stessa ragione della v3.0: le condizioni in gioco sono congiunzioni di '
     'uguaglianze e appartenenze, non inferenze. Un motore inferenziale porterebbe un onere '
     'di esercizio e di competenze sproporzionato al problema.'),
    ('Un’interrogazione sul database di SIPO (la scelta adottata)',
     'La condizione è una query in sola lettura sulle tabelle di SIPO, associata all’atto in '
     'lavorazione. Il fondamento è di fatto, non di gusto: quando si deve stabilire quale '
     'caso d’uso si stia formando, SIPO ha già registrato l’atto sulle proprie tabelle. Il '
     'dato su cui decidere esiste, è quello vero, ed è raggiungibile con lo strumento che il '
     'sistema usa da sempre. Ogni altra forma ne costruisce una copia, e una copia può '
     'divergere.'),
]

PREZZO = [
    ('Che cosa si perde, e va detto', None),
    ('La verificabilità automatica.',
     'Una condizione dichiarativa è un dato analizzabile: si poteva stabilire, prima '
     'dell’esercizio, se esistessero combinazioni scoperte e se due regole potessero attivarsi '
     'insieme. Su una query questo non è possibile in generale. È la perdita più seria di '
     'questa versione, e non ha un rimedio equivalente: ha due mitigazioni.'),
    ('L’ordine esplicito.',
     'Gli UC che condividono un Modello si valutano nell’ordine dichiarato in NUM_PRIORITA e '
     'vince il primo la cui condizione è soddisfatta. La mutua esclusione non si dimostra più: '
     'si stabilisce. È una regola più povera ma sempre definita, e soprattutto leggibile da '
     'chi configura.'),
    ('La simulazione.',
     'Il controllo che resta è empirico: dato un atto reale di SIPO, il back-office mostra '
     'quale UC verrebbe determinato e quale condizione lo ha prodotto. Diventa il controllo '
     'principale prima di attivare una baseline, non più un ausilio.'),
]

DIFFERENZE = [
    ('Sola lettura',
     'La query è eseguita con un’utenza priva di privilegi di scrittura sugli schemi di SIPO. '
     'Il rischio che il capitolo sulla disamina del porting attribuisce alla logica nel '
     'database riguarda la logica che scrive: qui si legge soltanto.'),
    ('Descrizione obbligatoria',
     'Ogni condizione porta la propria descrizione in lingua corrente. È l’unica parte che un '
     'funzionario può rileggere senza saper leggere SQL, ed è il motivo per cui il campo non '
     'è facoltativo.'),
    ('Versionata come il resto',
     'La condizione appartiene alla baseline della configurazione: si modifica in bozza, si '
     'attiva insieme al resto, si torna indietro con un cambio di stato.'),
    ('Fuori dallo schema di SIPO',
     'Le CFG_RULE di SIPO risiedono in MATR_USR, cioè nello schema in esercizio; queste '
     'condizioni stanno in ANSC_USR e non toccano gli oggetti esistenti. È la stessa ragione '
     'per cui la parte dizionari non scrive nelle CONF_*.'),
]


def applica(doc):
    """Le sezioni si riscrivono in blocco: «Che cosa si guadagna» è una Heading 3 DENTRO la
    sezione delle alternative, e trattarle separatamente farebbe sparire la seconda insieme
    alla prima."""
    fatti = []
    tab_modello = D.trova_tabella(doc, 'Colonna', 'Tipo', 'Note')

    blocchi = [
        ('p', 'La forma da dare alle condizioni che scelgono l’UC è la decisione portante del '
              'capitolo. È stata presa fra tre alternative, e in questa versione l’esito è '
              'diverso da quello delle versioni precedenti: si riportano tutte e tre con il '
              'motivo della scelta, perché il cambiamento sia leggibile.'),
    ]
    blocchi += [('v', (t, c)) for t, c in ALTERNATIVE]
    blocchi += [
        ('h3', 'Che cosa si guadagna e che cosa si perde'),
        ('p', 'Il guadagno è la fedeltà al dato. La condizione osserva l’atto come SIPO l’ha '
              'registrato, comprese le informazioni che vivono su tabelle diverse da quella '
              'dell’atto — il soggetto, la configurazione dei tipi atto, i documenti — senza '
              'che la configurazione debba dichiarare come raggiungerle. Nessuna copia dei '
              'dati, nessun linguaggio intermedio da mantenere.'),
    ]
    for t, c in PREZZO:
        blocchi.append(('p', t) if c is None else ('v', (t, c)))
    blocchi += [
        ('h3', 'In che cosa differisce dalle regole di SIPO che erano state scartate'),
        ('p', 'Il rilievo mosso alle CFG_RULE di SIPO resta valido, e la differenza non sta '
              'nel linguaggio ma nel regime a cui la query è sottoposta.'),
    ]
    blocchi += [('v', (t, c)) for t, c in DIFFERENZE]

    D.sostituisci_sezione(doc, 'Perché regole dichiarative',
                          'La forma della condizione: le alternative considerate', blocchi)
    fatti.append(f'sezione «alternative» riscritta ({len(blocchi)} blocchi, '
                 f'con la sottosezione su guadagno e prezzo)')

    D.sostituisci_sezione(
        doc, 'La forma della regola', 'La forma della condizione',
        [('p', 'Un UC configurato porta una o più condizioni di applicabilità. Ciascuna è '
               'un’interrogazione che riceve l’identificativo dell’atto in lavorazione e '
               'restituisce una riga quando la condizione è soddisfatta: la presenza della '
               'riga è la risposta, il suo contenuto non è usato.'),
         ('p', 'Le condizioni di uno stesso UC sono in congiunzione. La disgiunzione si scrive '
               'dentro la query, ed è il punto in cui la forma scelta chiede attenzione: una '
               'query che risponde per troppe combinazioni fa scattare l’UC sbagliato senza '
               'produrre alcun errore. È la ragione della descrizione obbligatoria e della '
               'simulazione.'),
         ('tab', ([['Elemento', 'Contenuto'],
                   ['UC configurato', 'Il caso d’uso a cui la condizione appartiene: codice '
                                      'ANSC, Modello, tipo atto, maschera.'],
                   ['Interrogazione', 'Il testo della query, in sola lettura, con '
                                      'l’identificativo dell’atto come parametro.'],
                   ['Descrizione', 'Che cosa la condizione riconosce, in lingua corrente. '
                                   'Obbligatoria.'],
                   ['Ordine', 'Posizione fra le condizioni dello stesso UC.'],
                   ['Origine', 'Proposta, confermata, modificata o inserita: come per i campi '
                               'e per gli allegati.'],
                   ['Priorità dell’UC', 'Ordine di valutazione fra gli UC che condividono il '
                                        'Modello; il primo che risponde determina l’esito.']],
                  tab_modello))])
    fatti.append('sezione «forma della condizione» riscritta')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
