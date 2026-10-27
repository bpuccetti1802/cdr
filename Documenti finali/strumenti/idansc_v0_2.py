# -*- coding: utf-8 -*-
"""STUDIO_Identificativi-ANSC-verso-ANPR v0.1 → v0.2 (27/10/2026).

⚠️ CORREZIONE DI UNA CONCLUSIONE CONSEGNATA. La v0.1 affermava che l'identificativo del
soggetto di ANSC non si può passare ad ANPR, e lo deduceva **dai soli tipi generati nel
client**. Il committente ha obiettato che il client è una fotografia della versione di
schema con cui SIPO è stato compilato, e che la documentazione ANPR va guardata a parte.
Obiezione fondata: in `anpr-9.2.9/src/wsdl/ansc/xsd/` esiste l'interfaccia
**«Predisposizione Anagrafica»**, dove `idSoggettoANSC` e `idANPR` sono **entrambi**
previsti, insieme all'identificativo della scheda comunale e di quella ANPR.

La conclusione passa quindi da «non è possibile» a «non è possibile con le operazioni che
il client implementa; è previsto in un'interfaccia che SIPO non implementa».

Interventi: riscritti il capitolo della risposta e quello delle conclusioni, aggiunto il
capitolo sulla Predisposizione Anagrafica, aggiunta la nota di metodo sul perché la v0.1
non l'aveva vista, nuovo riferimento [S8], nuovi punti aperti AN-07…AN-10.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/idansc_v0_2.py
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
SRC = os.path.join(FIN, 'STUDIO_Identificativi-ANSC-verso-ANPR_v0.1.docx')
DST = os.path.join(FIN, 'STUDIO_Identificativi-ANSC-verso-ANPR_v0.2.docx')


# --------------------------------------------------------------------- contenuti

RISPOSTA = [
    ['La domanda', 'Nelle operazioni che il client implementa',
     'Nella documentazione ANPR'],
    ['Si può passare ad ANPR l’identificativo con cui **ANSC** individua un soggetto '
     '(idSoggettoANSC)?',
     '**No.** Nessuno dei tipi generati lo prevede, e l’unico identificativo di soggetto '
     'che il client conosce è quello di ANPR.',
     '**Sì.** È previsto, facoltativo, nell’interfaccia della Predisposizione Anagrafica.'],
    ['Si può passare l’identificativo unico nazionale (il codice che SIPO chiama '
     'ID_UNICO_NAZIONALE)?',
     'È **l’identificativo di ANPR**: il codice lo riceve da ANPR e lo conserva, non lo '
     'costruisce. Nelle richieste il soggetto si individua con l’identificativo della '
     'scheda comunale.',
     '**Sì.** La stessa interfaccia lo prevede come `idANPR`, accanto agli altri tre.'],
]

IDENTIFICATIVI = [
    ['Elemento', 'Tipo', 'Che cos’è', 'In SIPO'],
    ['idSchedaSoggettoComune', 'facoltativo',
     'L’identificativo della scheda presso il comune.',
     'La chiave del soggetto nella base dati del comune.'],
    ['idSchedaSoggettoANPR', 'numerico, max 16, facoltativo',
     'L’identificativo della scheda presso ANPR.', 'ID_SCHEDA_ANPR.'],
    ['**idSoggettoANSC**', 'numerico, max 16, facoltativo',
     'L’identificativo del soggetto presso ANSC.',
     'È il dato che il disegno dell’integrazione conserva sullo store degli '
     'identificativi del soggetto.'],
    ['**idANPR**', 'alfanumerico di 9 caratteri, facoltativo',
     'L’identificativo unico nazionale della persona.',
     'ID_UNICO_NAZIONALE, che il codice valorizza proprio da questo campo.'],
]

TESTATA = [
    ['Elemento', 'Che cosa dichiara'],
    ['idNotifica', 'L’identificativo della predisposizione anagrafica.'],
    ['codMittente',
     '«Il codice ISTAT **del comune che effettua la richiesta**»: la testata attribuisce '
     'l’invio al comune.'],
    ['idTipoNotifica',
     'Il tipo di notifica anagrafica, «es. **SC01, SC02**…»: sono le stesse sigle che '
     'l’analisi dell’integrazione registra come notifiche anagrafiche destinate '
     'all’ufficio anagrafe.'],
    ['idTipoContenuto',
     '1 atto · 2 annotazione · 3 trascrizione · 4 annotazione automatica.'],
    ['idTipoEvento',
     '1 nascita · 2 morte · 3 matrimonio · 4 unione civile · 5 cittadinanza.'],
    ['idUsecase e descrizioneUsecase',
     'Il caso d’uso di ANSC che ha prodotto l’atto, con la sua descrizione.'],
    ['dataValidita', 'La data di validità dell’atto.'],
]

DUE_ATTI = [
    ['', 'tipoAttoANSC di **ANPR**', 'tipoAttoANSC di **ANSC**'],
    ['Namespace', '`sogei.it/ANPR/tipoDato`', '`sogei.it/ansc/predisposizioneAnagrafica`'],
    ['Dove si usa', 'Nelle operazioni 5008 e 2001 del client.',
     'Nel corpo della Predisposizione Anagrafica, dove è **obbligatorio**.'],
    ['Nome dell’identificativo', '`idANSC`', '`idAnsc`'],
    ['Obbligatorietà degli elementi',
     'Identificativo, comune e anno **obbligatori**; numero comunale **obbligatorio**.',
     '**Tutti facoltativi.**'],
    ['Elementi propri', '`ufficioMunicipio`, `trascritto`',
     '`composizioneCompleta`, che porta **il testo dell’atto**'],
]

CORPO = [
    ['Blocco', 'Molteplicità', 'Che cosa porta'],
    ['intestatario', 'da 1 a molti, **obbligatorio**',
     'Le generalità dell’intestatario, con i quattro identificativi. La molteplicità '
     'aperta è ciò che consente il parto plurimo e gli atti a due intestatari.'],
    ['atto', 'uno, **obbligatorio**',
     'L’atto in forma ANSC, compreso il testo completo.'],
    ['paternita, maternita', 'facoltativi',
     'Le generalità dei genitori, con i loro quattro identificativi.'],
    ['matrimonio, unioneCivile, separazione', 'facoltativi',
     'I blocchi delle famiglie corrispondenti.'],
    ['datiDecesso, datiRettifica, cittadinanza', 'facoltativi',
     'I blocchi degli altri eventi.'],
    ['datiAnagraficiANPR, datiLingua', 'facoltativi',
     'Dati anagrafici di ANPR e dati di lingua.'],
]

CAUTELE = [
    ['Cautela', 'Perché conta'],
    ['**Non c’è un WSDL.**',
     'La cartella contiene soltanto gli schemi e nove esempi: il **trasporto non è '
     'dichiarato**. È un formato di messaggio, non un servizio con un endpoint, e come '
     'viaggi va accertato prima di progettare qualunque cosa.'],
    ['**Il namespace è di ANSC, non di ANPR.**',
     'Lo schema vive nel repository della documentazione ANPR ma dichiara '
     '`sogei.it/ansc/…`. Il materiale descrive quindi un messaggio del dominio di ANSC, '
     'pubblicato dove lo deve leggere chi gestisce l’anagrafe.'],
    ['**Chi è il mittente va confermato.**',
     'La testata dice «il comune che effettua la richiesta», e questo indica il comune. Ma '
     'se la chiamata la faccia il gestionale comunale oppure ANSC per conto del comune '
     '**non è deciso da questi file**: è la domanda da porre a Sogei, ed è la stessa '
     'cautela che la prima versione di questo studio non ha osservato.'],
]

APERTI_NUOVI = [
    ('AN-07', 'Come viaggia la Predisposizione Anagrafica: gli schemi non sono accompagnati '
              'da un WSDL e il trasporto non è dichiarato. Senza questa risposta non si può '
              'dimensionare nessun intervento.', 'Presidio ANPR / Sogei'),
    ('AN-08', 'Chi emette la Predisposizione Anagrafica: il gestionale del comune, come la '
              'testata lascia intendere attribuendo l’invio al codice ISTAT del comune, '
              'oppure ANSC per conto del comune nel flusso della comunicazione anagrafica. '
              'La risposta decide se il lavoro sia nostro o se sia una funzione che '
              'riceviamo.', 'Presidio ANPR / Sogei'),
    ('AN-09', 'Se la Predisposizione Anagrafica sia alternativa o complementare alle '
              'operazioni di mutazione che i processi schedulati usano oggi: se fosse il '
              'canale previsto per gli atti formati in ANSC, gli interventi sui processi '
              'esistenti cambierebbero di segno.', 'Analisi / Presidio ANPR'),
    ('AN-10', 'Perché la documentazione ANPR non sia raggiungibile nel perimetro di lavoro '
              'ordinario: la cartella è esclusa dal versionamento e presente solo in una '
              'copia. È la ragione per cui questa interfaccia non era stata vista, e il '
              'rischio si ripresenterà su altri temi.', 'Gestione del workspace'),
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
        """Elimina il corpo di un capitolo e restituisce l'elemento su cui innestare."""
        elementi = D.sezione(d, titolo, livello)
        assert elementi, 'capitolo non trovato: %s' % titolo
        for ch in elementi[1:]:
            if D.ha_commenti(ch):
                raise SystemExit('il capitolo %s porta un commento: non si svuota' % titolo)
            ch.getparent().remove(ch)
        return elementi[0].getnext()

    # ====================================================== 1. la risposta, riscritta
    dopo = svuota('La domanda e la risposta')
    inserisci(dopo, [
        ('b', 'La domanda è se fra i dati che si possono passare ad ANPR vi siano '
              'l’identificativo con cui ANSC individua un soggetto e l’identificativo unico '
              'nazionale. La risposta dipende da **dove si guarda**, e questa distinzione è '
              'il contenuto principale dello studio.'),
        ('tab', (RISPOSTA, [2.1, 2.3, 2.2])),
        ('b', 'Ne seguono due affermazioni da tenere separate. La prima: **le operazioni che '
              'il client di SIPO implementa non prevedono l’identificativo di ANSC per il '
              'soggetto**, e nessuna configurazione lo aggiunge — il tipo degli '
              'identificativi di soggetto porta un solo campo, quello di ANPR. La seconda: '
              '**la documentazione ANPR descrive un’interfaccia in cui tutti gli '
              'identificativi convivono**, e SIPO non la implementa affatto.'),
        ('b', 'Il limite, dunque, **non è di ANPR: è del client**. E non nella forma di un '
              'campo mancante in un’operazione esistente, ma nella forma di un’interfaccia '
              'intera che non è stata realizzata. È una differenza che conta, perché '
              'sposta la questione da «non si può fare» a «è un lavoro da fare, e prima '
              'vanno chiarite tre cose».'),
        ('p', 'Sull’identificativo unico nazionale va aggiunta una precisazione che evita un '
              'malinteso ricorrente: in SIPO il campo che lo conserva è valorizzato con '
              'l’identificativo che ANPR restituisce. Non è un dato che il comune '
              'costruisce e comunica, è un dato che riceve e custodisce; nelle richieste '
              'alle operazioni di scrittura il soggetto si individua con l’identificativo '
              'della scheda comunale.'),
    ])
    fatti.append('riscritto il capitolo «La domanda e la risposta»')

    # ====================================================== 2. nota di metodo
    D.sostituisci(
        d,
        'Ogni affermazione su che cosa ANPR accetti è verificata sui tipi generati dallo '
        'schema Sogei presenti nel client [S1]: sono la rappresentazione del contratto, e '
        'in assenza della documentazione ANPR nel perimetro di lavoro sono la fonte più '
        'vicina al contratto stesso.',
        'Ogni affermazione su che cosa il client di SIPO sappia fare è verificata sui tipi '
        'generati presenti nel client [S1]. ⚠️ Quei tipi non sono però il contratto di '
        'ANPR: sono la fotografia della versione di schema con cui SIPO è stato '
        'compilato, e dedurne che cosa ANPR preveda è un passaggio illecito — è l’errore '
        'della prima versione di questo studio, corretto qui dopo un rilievo del '
        'committente. Che cosa ANPR preveda si verifica sulla sua documentazione [S8], che '
        'è a sua volta da leggere con attenzione al namespace di ciascuno schema.',
        attese=1, etichetta='nota di metodo sui tipi del client', fatti=fatti)

    # ====================================================== 3. riferimento nuovo
    rif = D.trova_tabella(d, '#', 'riferimento', 'natura')
    D.clona_riga(rif, (
        '[S8]',
        'Documentazione ANPR versione 9.2.9 — in particolare src/wsdl/ansc/xsd/, gli schemi '
        'della Predisposizione Anagrafica, e src/wsdl/ansc/esempi/, i nove esempi di '
        'messaggio. ⚠️ La cartella è esclusa dal versionamento del workspace e presente '
        'solo in copia: vedi AN-10.',
        'Specifica di Sogei'))
    fatti.append('aggiunto il riferimento [S8]')

    # ====================================================== 4. capitolo nuovo
    dopo = D.h(d, 1, 'Che cosa non si può fare')._p
    inserisci(dopo, [
        ('h1', 'La Predisposizione Anagrafica: l’interfaccia in cui gli identificativi '
               'sono previsti'),
        ('b', 'Nella documentazione ANPR, accanto agli schemi dei servizi per i comuni, c’è '
              'una cartella dedicata ad ANSC: tre schemi per circa duemila righe e '
              'duecentoquarantacinque tipi, più nove esempi di messaggio — nascita, morte '
              'con e senza coniuge, matrimonio, unione civile, cittadinanza, rettifica, '
              'discordanza anagrafica, caso d’uso di servizio. Definiscono un messaggio '
              'chiamato **predisposizione anagrafica**.'),
        ('h2', 'La testata: che cosa dichiara, e chi la manda'),
        ('tab', (TESTATA, [2.2, 4.4])),
        ('b', 'La riga che più interessa è `codMittente`, descritta come «il codice ISTAT '
              'del comune che effettua la richiesta»: **la testata attribuisce l’invio al '
              'comune**. E `idTipoNotifica` chiude il cerchio con un capitolo che l’analisi '
              'dell’integrazione ha già scritto: le sigle SC01 e seguenti sono le notifiche '
              'anagrafiche che il disegno registra come destinate all’ufficio anagrafe, e '
              'che il flusso delle conferme di ANSC sblocca o trattiene. Questa interfaccia '
              '**è** quel canale, visto dal lato di chi emette il messaggio.'),
        ('h2', 'Il corpo: un atto e i suoi soggetti'),
        ('tab', (CORPO, [1.9, 1.6, 3.1])),
        ('h2', 'I quattro identificativi, affiancati'),
        ('b', 'Il tipo delle generalità — quello che descrive l’intestatario, i genitori, il '
              'coniuge — porta **quattro identificativi, tutti facoltativi**. È il punto che '
              'risponde alla domanda dello studio, e la risposta è più ampia di quanto la '
              'domanda chiedesse: non solo l’identificativo di ANSC è previsto, ma lo è '
              '**accanto** a quello di ANPR e a quello della scheda comunale.'),
        ('tab', (IDENTIFICATIVI, [1.9, 1.6, 1.8, 1.3])),
        ('b', 'La convivenza dei quattro non è un dettaglio di schema: è la dichiarazione '
              'che il messaggio serve proprio a **mettere in corrispondenza i tre mondi**. '
              'Negli esempi i quattro compaiono insieme — l’esempio della nascita porta '
              'l’identificativo di ANSC sull’intestatario, sul padre e sulla madre, '
              'ciascuno accanto all’identificativo della scheda ANPR.'),
        ('h2', 'Due tipi omonimi che non sono la stessa cosa'),
        ('b', 'Va segnalata una trappola che costerebbe tempo a chi realizza: **esistono due '
              'tipi chiamati `tipoAttoANSC`**, in namespace diversi e con contenuto diverso. '
              'Confonderli produce un messaggio formalmente plausibile e sbagliato.'),
        ('tab', (DUE_ATTI, [1.5, 2.4, 2.7])),
        ('b', 'La differenza più rilevante è l’ultima: la forma di ANSC porta '
              '**`composizioneCompleta`**, cioè il testo dell’atto, che la forma di ANPR non '
              'prevede. Sono messaggi con scopi diversi — l’uno comunica una mutazione '
              'anagrafica citando l’atto, l’altro trasmette l’atto.'),
        ('h2', 'Che cosa SIPO ne sa oggi'),
        ('b', 'Nulla. La ricerca del namespace e del nome dell’interfaccia su tutto il '
              'codice applicativo — i front-end, i back-end, le librerie condivise — dà '
              '**zero occorrenze**. Non è un’implementazione incompleta da correggere: è '
              'un’interfaccia che non è mai stata affrontata.'),
        ('h2', 'Tre cautele prima di progettare'),
        ('tab', (CAUTELE, [2.0, 4.6])),
    ])
    fatti.append('nuovo capitolo sulla Predisposizione Anagrafica')

    # ====================================================== 5. conclusioni riscritte
    dopo = svuota('Che cosa non si può fare, e che cosa si fa invece')
    D.testo_di(Paragraph(D.h(d, 1, 'Che cosa non si può fare, e che cosa si fa invece')._p, d),
               'Che cosa si può fare, e in quale ordine')
    inserisci(dopo, [
        ('b', 'La prima versione di questo studio concludeva che il passaggio '
              'dell’identificativo del soggetto di ANSC «non è realizzabile e non va messo a '
              'piano». **La conclusione era troppo forte e va corretta.** Era vera della '
              'parte del sistema che lo studio aveva esaminato — le operazioni che il client '
              'implementa — e falsa come affermazione su ANPR.'),
        ('b', 'La formulazione corretta distingue tre cose, che conviene affrontare in '
              'quest’ordine perché la prima è a portata di mano e la terza dipende da '
              'risposte che non abbiamo.'),
        ('v', ('Passare l’atto in forma ANSC sulle operazioni esistenti.',
               'È il capitolo degli interventi di questo studio: il meccanismo esiste nel '
               'client, commuta da sé, e per i decessi l’intervento resta dentro un solo '
               'modulo. **Si può fare adesso**, con il solo accertamento delle colonne '
               '(AN-01, AN-02).')),
        ('v', ('Estendere le operazioni che la forma ANSC non trattano.',
               'Le iscrizioni e due mutazioni di matrimonio. È lavoro sul client condiviso, '
               'con un raggio più ampio: **si può fare, va pianificato** (AN-04).')),
        ('v', ('Realizzare la Predisposizione Anagrafica.',
               'È l’unica strada che porta ad ANPR gli identificativi del soggetto, e '
               'richiede un componente che oggi non esiste. **Non si può pianificare '
               'finché non si sa come viaggia il messaggio e chi lo emette** (AN-07, '
               'AN-08, AN-09).')),
        ('b', 'Resta valido, e indipendente da tutto questo, che **la corrispondenza fra gli '
              'identificativi dei tre mondi va tenuta dalla nostra parte**: lo store degli '
              'identificativi del soggetto previsto dal disegno dell’integrazione serve in '
              'ogni scenario. Se la Predisposizione Anagrafica si realizzerà, quello store '
              'è esattamente ciò che la alimenta — i quattro identificativi che il messaggio '
              'chiede sono i quattro che vi si conservano. Se non si realizzerà, resta la '
              'sede in cui il Comune sa che una persona è la stessa nei tre sistemi.'),
    ])
    fatti.append('riscritto il capitolo delle conclusioni, e rititolato')

    # ====================================================== 6. punti aperti
    aperti = D.trova_tabella(d, '#', 'questione', 'a chi compete')
    for codice, testo, compete in APERTI_NUOVI:
        D.clona_riga(aperti, (codice, testo, compete))
    D.sostituisci(
        d,
        'Sei questioni restano da chiudere. Le prime due decidono se l’intervento sia '
        'realizzabile oggi; la terza riguarda il comportamento di ANPR in esercizio, che le '
        'sorgenti non documentano.',
        'Dieci questioni restano da chiudere. Le prime due decidono se l’intervento sulle '
        'operazioni esistenti sia realizzabile oggi; la terza riguarda il comportamento di '
        'ANPR in esercizio; le ultime quattro, introdotte da questa versione, riguardano la '
        'Predisposizione Anagrafica e il modo in cui la sua documentazione è stata '
        'raggiunta.',
        attese=1, etichetta='premessa ai punti aperti', fatti=fatti)
    fatti.append('aggiunti %d punti aperti' % len(APERTI_NUOVI))

    # ====================================================== 7. frontespizio e storia
    for fatto in D.frontespizio(d, '0.2',
                                'STUDIO_Identificativi-ANSC-verso-ANPR_v0.2',
                                data='27/10/2026'):
        fatti.append(fatto)
    D.storia(d, '27/10/2026', '0.2',
             'La domanda e la risposta · Metodo · Predisposizione Anagrafica (nuovo) · '
             'Conclusioni · Punti aperti · Riferimenti',
             'Corretta la conclusione della v0.1 su rilievo del committente. La v0.1 '
             'deduceva dai soli tipi generati nel client che l’identificativo del soggetto '
             'di ANSC non si potesse passare ad ANPR: i tipi del client sono però la '
             'fotografia della versione di schema con cui SIPO è stato compilato, non il '
             'contratto di ANPR. Nella documentazione ANPR esiste l’interfaccia della '
             'Predisposizione Anagrafica, dove il tipo delle generalità porta quattro '
             'identificativi facoltativi affiancati — scheda comunale, scheda ANPR, '
             'soggetto ANSC e identificativo unico nazionale — e dove l’atto in forma ANSC '
             'è obbligatorio e porta anche il testo. Il limite è quindi del client, non di '
             'ANPR, e ha la forma di un’interfaccia intera non realizzata. Aggiunti il '
             'capitolo che la descrive, la nota di metodo, il riferimento [S8] e i punti '
             'aperti AN-07…AN-10; rititolato e riscritto il capitolo delle conclusioni.')

    d.save(DST)
    cap, tab, fig = D.riepilogo(DST)
    print('scritto %s' % os.path.basename(DST))
    for f in fatti:
        print('  ' + str(f))
    print('  capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
    print('  punti aperti: %d' % (len(aperti.rows) - 1))


if __name__ == '__main__':
    main()
