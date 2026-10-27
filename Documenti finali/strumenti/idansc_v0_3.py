# -*- coding: utf-8 -*-
"""STUDIO_Identificativi-ANSC-verso-ANPR v0.2 → v0.3 (27/10/2026).

Il committente ha precisato che l'obiettivo principale è **mandare `idSoggettoAnsc` ad
ANPR**, e ha chiesto l'analisi del client per sapere quali funzioni modificare. La v0.3
riorienta lo studio su quell'obiettivo e aggiunge il capitolo sul client.

Due accertamenti nuovi, entrambi sulla fonte autoritativa (gli schemi 9.2.9) e non sui
tipi generati nel client:

  · negli XSD dei servizi ai comuni la stringa «ansc» compare **otto volte, tutte
    riferite all'ATTO** (tipoAttoANSC 4, tipoNumeroAttoANSC 2, idANSC 1, attoANSC 1):
    **nessun identificativo di soggetto**. La conclusione della v0.2 regge, ma ora è
    verificata dove andava verificata;
  · ⚠️ **gli XSD imbarcati nel client sono ANTERIORI ad ANSC** — `tipoDato.xsd` del
    modulo ha **zero** occorrenze di `tipoAttoANSC`, la 9.2.9 ne ha undici — quindi il
    client è indietro rispetto allo schema pubblicato, e i suoi stessi XSD non
    descrivono più il Java dello stesso modulo.

Corollario che interessa l'obiettivo principale: **rigenerare il client non serve a
mandare l'identificativo del soggetto.** Serve all'atto. Per il soggetto la sola strada
resta la Predisposizione Anagrafica.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/idansc_v0_3.py
"""
import os
import shutil
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'STUDIO_Identificativi-ANSC-verso-ANPR_v0.2.docx')
DST = os.path.join(FIN, 'STUDIO_Identificativi-ANSC-verso-ANPR_v0.3.docx')


# --------------------------------------------------------------------- contenuti

OBIETTIVO = [
    ['L’obiettivo', 'Si può?', 'Per quale via', 'Che cosa lo blocca'],
    ['Mandare ad ANPR **l’identificativo del soggetto di ANSC**',
     '**Non attraverso i servizi che il comune usa.**',
     'Soltanto la **Predisposizione Anagrafica**, dove è previsto e facoltativo.',
     'Il trasporto non è dichiarato e chi emette il messaggio non è deciso dalle fonti '
     '(AN-07, AN-08).'],
    ['Mandare ad ANPR **l’identificativo dell’atto di ANSC**',
     '**Sì.**',
     'Le operazioni che portano un atto in forma ANSC: la mutazione e la cancellazione '
     'già oggi, le iscrizioni e l’AIRE dopo aver aggiornato il client.',
     'Nulla per la mutazione e la cancellazione; per le altre, la rigenerazione del '
     'client (AN-11).'],
]

ANSC_NEGLI_SCHEMI = [
    ['Dove compare «ansc» negli schemi dei servizi ai comuni', 'Occorrenze', 'Riguarda'],
    ['`tipoAttoANSC`', '4', 'l’atto'],
    ['`tipoNumeroAttoANSC`', '2', 'l’atto'],
    ['`idANSC`', '1', 'l’atto, dentro `tipoAttoANSC`'],
    ['`attoANSC`', '1', 'l’atto, dentro `tipoAttoANPR`'],
    ['**Identificativi di soggetto**', '**0**',
     '**nulla: non esistono**'],
]

STRATI = [
    ['Parte del client', 'Classi', 'Righe', 'Si modifica?'],
    ['`tipoDato`, `vocabolario*`, gli involucri per famiglia, i port `service*`',
     'circa 600', 'circa 64.700',
     '**No.** Sono generate dagli schemi: si **rigenerano**, non si editano.'],
    ['`xmlRequestGenerator`', '32', '8.402',
     'Sì. È dove si costruisce la richiesta, ed è il grosso del lavoro.'],
    ['`sicurezza`', '50', '4.154',
     'Sì. Un gestore per operazione, più la firma e i portachiavi.'],
    ['`common` (le utilità condivise)', '3', '1.427',
     'Sì. È il luogo giusto per fattorizzare un ramo comune.'],
    ['`client`, `activator`, `config`, `connessione`, `cypher`, `exception`', '14',
     'circa 1.500', 'Sì. Punto di ingresso, smistamento e configurazione.'],
]

CONFRONTO = [
    ['Schema', 'Imbarcato nel client', 'Pubblicato nella 9.2.9'],
    ['`tipoDato.xsd`', '3.632 righe', '**4.405 righe**'],
    ['`vocabolario5000mutazione.xsd`', '550', '**788**'],
    ['`5000mutazione.xsd`', '422', '**477**'],
    ['`2000cancellazione.xsd`', '214', '**247**'],
    ['`vocabolario1000iscrizione.xsd`', '544', '**566**'],
    ['**occorrenze di `tipoAttoANSC` in `tipoDato.xsd`**', '**0**', '**11**'],
    ['**elementi `attoNascitaANPR` nell’iscrizione**', '**0**', '**2**'],
    ['**elementi `attoNascitaANPR` nell’AIRE**', '**0**', '**2**'],
]

DIFETTI = [
    ['Difetto', 'Dove', 'Perché va sciolto prima'],
    ['L’ambiente è cablato a TEST',
     'Nel punto di ingresso, dove si imposta l’ambiente prima dello smistamento.',
     'Da quell’impostazione dipende il portachiavi con cui la richiesta viene firmata. '
     'Finché la riga resta, **non si può collaudare contro un ambiente diverso da '
     'TEST**: è un rilievo già tracciato nel registro delle verifiche.'],
    ['La richiesta si costruisce come stringa e si ri-deserializza',
     'Il generatore produce XML in forma di testo; il gestore lo riporta nella classe '
     'generata prima di inviarlo.',
     'Un errore di costruzione non si manifesta alla compilazione ma all’esecuzione, e '
     'il doppio passaggio raddoppia i punti in cui un campo nuovo si può perdere.'],
    ['L’accesso ai dati del chiamante è per reflection',
     'In tutti i generatori, che invocano i metodi per nome.',
     'Un campo nuovo richiede che l’oggetto passato esponga il metodo: se non lo espone '
     'il risultato è un errore in esecuzione, non un valore vuoto. Ed è il motivo per '
     'cui questi meccanismi sono invisibili a una ricerca testuale.'],
]

COSTO = [
    ['Che cosa serve per una operazione nuova', 'Dimensione'],
    ['Un gestore dedicato nel pacchetto della sicurezza: istanzia il port, attacca la '
     'firma, deserializza e invoca.', 'circa 90 righe'],
    ['Un ramo nello smistatore, sulla famiglia dell’operazione.', 'una riga'],
    ['Un ramo nel punto di ingresso, sul nome dell’operazione.', 'due righe'],
    ['Un generatore della richiesta.',
     'da 150 a 1.000 righe, secondo la complessità'],
    ['Le classi generate dagli schemi.', 'da rigenerare, non da scrivere'],
]

FUNZIONI_ATTO = [
    ['Dove', 'Funzione', 'Che cosa aggiungere'],
    ['Concentratore', '`Convert.generateAtto` (`Convert.java:1033`)',
     'Valorizzare l’identificativo ANSC dell’atto, l’anno, la data, il numero comunale e '
     'il comune, leggendoli dall’atto di anagrafe invece di lasciarli vuoti.'],
    ['Concentratore', '`Convert.attoConverter` (`:177`)', 'Lo stesso.'],
    ['Concentratore', '`Convert.generateAttoDaAggior` (`:1242`)', 'Lo stesso.'],
    ['Client', '`AnprUtilities.generateTipoAttoANPR` (`:427`)',
     'È già corretta. È però il luogo in cui fattorizzare il ramo una volta sola, invece '
     'di ripeterlo in ciascun generatore.'],
    ['Client', 'I generatori delle operazioni che i processi usano e che oggi non '
               'trattano la forma ANSC: iscrizione per nascita e altri motivi, '
               'annullamento iscrizione, cancellazione altri motivi, annullamento '
               'cancellazione, mutazione famiglia, annullamento mutazione, revoca dato, '
               'le tre dell’AIRE.',
     'Il ramo sull’identificativo, **dopo** la rigenerazione: oggi le classi generate non '
     'hanno il tipo dove scrivere il valore.'],
]

APERTI_NUOVI = [
    ('AN-11', 'Da quale versione di schema rigenerare il client, e quale versione sia in '
              'esercizio su ANPR. Gli schemi imbarcati nel modulo sono anteriori alla '
              'comparsa di ANSC: fino a quando non si sa su quale versione ANPR risponde, '
              'una rigenerazione è un salto nel vuoto. Da chiedere al fornitore e al '
              'presidio ANPR.', 'Referenti SIPO / Presidio ANPR'),
    ('AN-12', 'Quale sia la sorgente di verità degli schemi per il client: quelli '
              'imbarcati nel modulo non descrivono più il codice Java dello stesso '
              'modulo — il Java conosce il tipo dell’atto ANSC, i suoi schemi no. Prima '
              'di rigenerare va stabilito da dove si prendono gli schemi e chi li '
              'aggiorna.', 'Architettura / Referenti SIPO'),
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    fatti = []

    def inserisci(prima, blocchi):
        for tipo, contenuto in blocchi:
            if tipo == 'p':
                D.para(d, prima, contenuto)
            elif tipo == 'b':
                D.para(d, prima, pezzi=D.segmenta('', contenuto))
            elif tipo == 'v':
                D.voce(d, prima, *contenuto)
            elif tipo == 'h1':
                D.para(d, prima, contenuto, stile='Heading 1')
            elif tipo == 'h2':
                D.para(d, prima, contenuto, stile='Heading 2')
            elif tipo == 'tab':
                righe, larghezze = contenuto
                D.tabella(d, prima, righe, d.tables[0], larghezze)

    def svuota(titolo, livello=1):
        elementi = D.sezione(d, titolo, livello)
        assert elementi, 'capitolo non trovato: %s' % titolo
        for ch in elementi[1:]:
            if D.ha_commenti(ch):
                raise SystemExit('il capitolo %s porta un commento' % titolo)
            ch.getparent().remove(ch)
        return elementi[0].getnext()

    # ============================================= 1. la risposta, riorientata
    dopo = svuota('La domanda e la risposta')
    inserisci(dopo, [
        ('b', 'L’obiettivo principale è **mandare ad ANPR l’identificativo con cui ANSC '
              'individua un soggetto**. Accanto a quello si pone la questione '
              'dell’identificativo dell’atto, che ha risposta diversa: le due vanno tenute '
              'separate perché conducono a interventi diversi e a tempi diversi.'),
        ('tab', (OBIETTIVO, [1.7, 1.4, 1.9, 1.6])),
        ('b', 'Sul primo obiettivo la risposta è negativa, e questa versione la verifica '
              'dove andava verificata: **non sui tipi generati nel client, ma sugli schemi '
              'pubblicati da ANPR**. Nell’insieme degli schemi dei servizi che un comune '
              'usa, la parola «ansc» compare otto volte in tutto, e ogni volta riguarda '
              'l’atto.'),
        ('tab', (ANSC_NEGLI_SCHEMI, [3.4, 1.3, 1.9])),
        ('b', 'Non esiste quindi, in nessuna delle operazioni che il comune invoca, un '
              'elemento in cui scrivere l’identificativo del soggetto di ANSC. Quelle '
              'operazioni individuano la persona con l’identificativo di ANPR, che è una '
              'stringa di nove caratteri, e con gli identificativi della scheda; di un '
              'identificativo di provenienza esterna non hanno posto.'),
        ('b', '**L’unico canale in cui l’identificativo del soggetto è previsto è la '
              'Predisposizione Anagrafica**, descritta nel capitolo omonimo: lì convive con '
              'gli altri tre, su ciascun soggetto del messaggio. È l’unica strada, e le tre '
              'cautele che la riguardano sono anche i tre motivi per cui non si può ancora '
              'pianificare.'),
        ('b', 'Da questo discende un corollario che riguarda direttamente l’obiettivo, e '
              'che conviene dire subito perché evita un lavoro inutile: **aggiornare il '
              'client non serve a mandare l’identificativo del soggetto.** '
              'L’aggiornamento del client — di cui il capitolo seguente misura la necessità '
              'e il costo — serve all’atto, e soltanto all’atto.'),
    ])
    fatti.append('riorientato il capitolo «La domanda e la risposta» sull’obiettivo principale')

    # ============================================= 2. capitolo sul client
    dopo = D.h(d, 1, 'La Predisposizione Anagrafica')._p
    inserisci(dopo, [
        ('h1', 'Il client ANPR di SIPO: com’è fatto, e in che stato è'),
        ('b', 'Il client è l’unico confine di SIPO verso ANPR: **685 classi per circa '
              'ottantamila righe**. La distinzione che governa qualunque intervento non è '
              'però fra i pacchetti, è fra ciò che è generato dagli schemi e ciò che è '
              'scritto a mano.'),
        ('tab', (STRATI, [2.6, 0.9, 0.9, 2.2])),
        ('b', 'Circa quattro quinti del codice sono generati. Ne segue che **un campo nuovo '
              'non si aggiunge scrivendo Java**: si ottiene rigenerando le classi da uno '
              'schema che quel campo lo preveda. È il punto da cui dipende tutto il resto '
              'del capitolo.'),
        ('h2', 'Il percorso di una chiamata'),
        ('b', 'Il punto di ingresso riceve i parametri, il nome dell’operazione e '
              'l’operatore. Costruisce la richiesta scegliendo il generatore con uno '
              '**smistamento su trentasei casi**, e ne ottiene l’XML **in forma di '
              'stringa**. Imposta poi l’ambiente e la famiglia dell’operazione, e passa la '
              'mano allo smistatore, che su undici famiglie sceglie il gestore dedicato. Il '
              'gestore istanzia il port del servizio, vi attacca la firma leggendo il '
              'portachiavi dell’ambiente, riporta la stringa nella classe generata e invoca '
              'il metodo del servizio.'),
        ('p', 'Dai commenti dello smistamento si ricavano anche i nomi ufficiali delle '
              'trentasei operazioni, che gli schemi non riportano: iscrizione per nascita, '
              'iscrizione altri motivi, cancellazione per morte, mutazioni dati generali di '
              'stato civile, mutazioni liste elettorali, e così via.'),
        ('h2', 'Lo stato: gli schemi del client sono anteriori ad ANSC'),
        ('b', 'Il modulo porta le proprie copie degli schemi. Confrontate con quelle della '
              'versione 9.2.9 risultano **tutte più corte**, e la differenza non è di '
              'dettaglio.'),
        ('tab', (CONFRONTO, [3.0, 1.8, 1.8])),
        ('b', 'Le ultime tre righe sono quelle che contano. Gli schemi del client **non '
              'conoscono l’atto in forma ANSC**, mentre la 9.2.9 lo prevede, e lo prevede '
              '**anche nell’iscrizione e nell’AIRE** — cioè in due delle famiglie che i '
              'processi schedulati usano, e non solo nella mutazione.'),
        ('b', 'Ne derivano due conclusioni. La prima: **il client è indietro rispetto allo '
              'schema pubblicato**, e questo è il motivo per cui soltanto due operazioni su '
              'quindici trattano la forma ANSC. La seconda, più scomoda: **gli schemi '
              'imbarcati nel modulo non descrivono più il codice Java dello stesso '
              'modulo**, perché quel codice conosce il tipo dell’atto ANSC mentre i suoi '
              'schemi no. Non si possono quindi usare come sorgente di una rigenerazione '
              'senza prima stabilire da dove prendere gli schemi veri (AN-11, AN-12).'),
        ('h2', 'Tre difetti strutturali da sciogliere nello stesso intervento'),
        ('tab', (DIFETTI, [1.9, 2.1, 2.6])),
        ('h2', 'Quanto costa aggiungere una operazione'),
        ('b', 'La misura è presa sull’operazione di mutazione, che è la più ricca. Non c’è '
              'un registro delle operazioni né una configurazione: **tutto avviene per '
              'smistamento**, quindi ogni operazione nuova tocca gli stessi tre punti.'),
        ('tab', (COSTO, [4.2, 2.4])),
    ])
    fatti.append('nuovo capitolo sull’architettura e lo stato del client')

    # ============================================= 3. conclusioni riorientate
    dopo = svuota('Che cosa si può fare, e in quale ordine')
    inserisci(dopo, [
        ('b', 'Le due questioni — il soggetto e l’atto — hanno risposte e tempi diversi, e '
              'conviene trattarle separatamente invece di aspettare che una sblocchi '
              'l’altra.'),
        ('h2', 'Per l’identificativo del soggetto: una sola strada, oggi bloccata'),
        ('b', 'Non c’è alcun intervento sul client che porti l’identificativo del soggetto '
              'ad ANPR, perché **nelle operazioni che il comune usa non esiste l’elemento '
              'in cui scriverlo** — e non si tratta di una versione vecchia: non esiste '
              'nemmeno nella 9.2.9. La sola strada è la Predisposizione Anagrafica, che '
              'richiede un componente nuovo e non si può pianificare prima di sapere **come '
              'viaggia il messaggio** (AN-07) e **chi lo emette** (AN-08).'),
        ('b', 'Finché quelle due risposte non arrivano, l’unica cosa utile e non sprecata è '
              '**tenere la corrispondenza dalla nostra parte**: lo store degli '
              'identificativi del soggetto previsto dal disegno dell’integrazione raccoglie '
              'già i quattro codici che il messaggio chiederebbe. Serve in ogni scenario, e '
              'se la Predisposizione si realizzerà è esattamente ciò che la alimenta.'),
        ('h2', 'Per l’identificativo dell’atto: tre livelli, il primo subito'),
        ('b', 'Qui invece si può procedere, e in ordine di costo crescente.'),
        ('v', ('Primo livello, nel solo concentratore.',
               'Tre funzioni di conversione da completare perché l’atto che arriva al '
               'generatore porti l’identificativo. **Accende da sé** la forma ANSC sulle '
               'due operazioni che già la trattano, e questo copre interamente il processo '
               'dei decessi — la famiglia del pilota. Non tocca il client.')),
        ('v', ('Secondo livello, la rigenerazione del client.',
               'È il prerequisito di tutto il resto, e non è un’estensione di codice: è '
               'una rigenerazione dalle classi di uno schema aggiornato, con le domande '
               'AN-11 e AN-12 da chiudere prima. Solo dopo ha senso estendere i generatori '
               'delle iscrizioni, dell’AIRE e delle altre mutazioni.')),
        ('v', ('Terzo livello, i generatori.',
               'Il ramo sull’identificativo nei generatori delle operazioni rimaste, '
               'fattorizzato nell’utilità comune invece di essere ripetuto. È lavoro '
               'meccanico, una volta che le classi generate hanno il tipo.')),
        ('tab', (FUNZIONI_ATTO, [1.3, 2.3, 3.0])),
        ('b', 'Una raccomandazione di sequenza: il difetto dell’ambiente cablato a TEST va '
              'sciolto **per primo**, prima di qualunque altra cosa. Non perché sia il più '
              'grave, ma perché finché resta non è possibile provare nulla contro un '
              'ambiente diverso da quello di collaudo, e quindi nessuno degli interventi '
              'qui descritti può essere verificato.'),
    ])
    fatti.append('riorientate le conclusioni, separando soggetto e atto')

    # ============================================= 4. AN-04 corretto
    D.sostituisci(
        d,
        'Se estendere i generatori che non trattano la forma ANSC — le iscrizioni e le '
        'mutazioni di matrimonio — e con quale priorità: è lavoro sul client condiviso, '
        'quindi con un raggio più ampio del singolo processo.',
        'Con quale priorità estendere i generatori che non trattano la forma ANSC. '
        'Riformulato nella v0.3: non è un lavoro di sola estensione. Lo schema 9.2.9 '
        'prevede l’atto in forma ANSC anche nell’iscrizione e nell’AIRE, ma le classi '
        'generate nel client non hanno il tipo in cui scriverlo, perché sono state '
        'generate da uno schema anteriore. Il prerequisito è quindi la rigenerazione '
        '(AN-11, AN-12), e l’estensione dei generatori viene dopo.',
        attese=1, etichetta='AN-04 riformulato', fatti=fatti)

    # ============================================= 5. punti aperti
    aperti = D.trova_tabella(d, '#', 'questione', 'a chi compete')
    for codice, testo, compete in APERTI_NUOVI:
        D.clona_riga(aperti, (codice, testo, compete))
    D.sostituisci(
        d, 'Dieci questioni restano da chiudere.',
        'Dodici questioni restano da chiudere.',
        attese=1, etichetta='conteggio dei punti aperti', fatti=fatti)
    fatti.append('aggiunti %d punti aperti' % len(APERTI_NUOVI))

    # ============================================= 6. riferimento
    rif = D.trova_tabella(d, '#', 'riferimento', 'natura')
    D.clona_riga(rif, (
        '[S9]',
        'Le copie degli schemi imbarcate nel client, in '
        'common/anpr-client/AnprClient/src/main/resources: sono la sorgente da cui le '
        'classi del client risultano generate, e sono anteriori ad ANSC.',
        'Sorgente applicativo'))
    fatti.append('aggiunto il riferimento [S9]')

    # ============================================= 7. frontespizio e storia
    for fatto in D.frontespizio(d, '0.3',
                                'STUDIO_Identificativi-ANSC-verso-ANPR_v0.3',
                                data='27/10/2026'):
        fatti.append(fatto)
    D.storia(d, '27/10/2026', '0.3',
             'La domanda e la risposta · Il client ANPR (nuovo) · Conclusioni · '
             'Punti aperti · Riferimenti',
             'Riorientata sull’obiettivo principale indicato dal committente: mandare ad '
             'ANPR l’identificativo del soggetto di ANSC. La risposta negativa è ora '
             'verificata sugli schemi pubblicati da ANPR e non sui tipi generati nel '
             'client: negli schemi dei servizi ai comuni la parola ansc compare otto volte '
             'e ogni volta riguarda l’atto, mentre di identificativi di soggetto di '
             'provenienza esterna non ve ne sono. Aggiunto il capitolo sul client — '
             'quattro quinti del codice sono generati, il percorso di una chiamata, i tre '
             'difetti strutturali e il costo di una operazione nuova — con '
             'l’accertamento che gli schemi imbarcati nel modulo sono anteriori ad ANSC e '
             'non descrivono più il Java dello stesso modulo. Ne segue che aggiornare il '
             'client serve all’atto e non al soggetto, e che la rigenerazione è il '
             'prerequisito dell’estensione dei generatori: AN-04 è riformulato di '
             'conseguenza. Nuovi AN-11 e AN-12, nuovo riferimento [S9].')

    d.save(DST)
    cap, tab, fig = D.riepilogo(DST)
    print('scritto %s' % os.path.basename(DST))
    for f in fatti:
        print('  ' + str(f))
    print('  capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
    print('  punti aperti: %d' % (len(aperti.rows) - 1))


if __name__ == '__main__':
    main()
