# -*- coding: utf-8 -*-
"""v3.13 — revisione della parte di configurazione.

Che cosa fa:
  · corregge in §8.4 le formulazioni «per operazione» rimaste dalla v2.x (dalla v3.0 i campi
    pendono dall'UC) e allinea l'elenco delle tabelle della baseline;
  · apre il capitolo 9 con la definizione del modello evento, che il documento citava
    diciassette volte senza mai dirne che cosa sia;
  · chiude il capitolo 9 con le fonti della configurazione, la catena completa dal Modello di
    SIPO al payload ANSC (con figura) e la procedura di revisione della mappatura;
  · aggiunge OP-52 sui percorsi del mapping che non si risolvono sul modello.

    /usr/bin/python3 v3_13_configurazione.py
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx  # noqa: E402

from docx_comune import (  # noqa: E402
    clona_riga, h, immagine, indice_di, para, riepilogo, segmenta, sostituisci, storia,
    tabella, trova_tabella, voce)

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.12.docx')
DST = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.13.docx')
PNG = os.path.join(QUI, 'img', 'catena_configurazione.png')


def h2(doc, prima, testo):
    return para(doc, prima, testo, stile='Heading 2')


def h3(doc, prima, testo):
    return para(doc, prima, testo, stile='Heading 3')


def p(doc, prima, testo):
    return para(doc, prima, testo)


def pb(doc, prima, testa, corpo):
    return para(doc, prima, stile='Normal', pezzi=segmenta(testa, corpo))


# ===================================================================== §8.4
def correggi_84(doc, fatti):
    sostituisci(
        doc,
        'descrive, per ogni operazione (tipo evento × tipo operazione × Modello), '
        'l’interfaccia ANSC da usare, il mapper e i campi obbligatori. È il presupposto del '
        'requisito RF-9 e il fattore che riduce l’effort, perché aggiungere un tipo di atto '
        'diventa un fatto di configurazione, non di sviluppo. Si compone di due tabelle in '
        'ANSC_USR.',
        'descrive, per ogni Modello di atto (tipo evento × tipo operazione × Modello), '
        'l’interfaccia ANSC da usare e il mapper, e — per ogni UC — i campi obbligatori con la '
        'loro provenienza in SIPO e i documenti da allegare. La distinzione fra i due livelli '
        'non è formale: il Modello dice quale maschera e quale servizio, l’UC dice quali dati, '
        'e fra i due sta la determinazione descritta al capitolo 10. È il presupposto del '
        'requisito RF-9 e il fattore che riduce l’effort, perché aggiungere un tipo di atto '
        'diventa un fatto di configurazione, non di sviluppo. Si compone delle tabelle '
        'seguenti, tutte in ANSC_USR.',
        attese=1, etichetta='§8.4 · premessa dei tre livelli', fatti=fatti)

    sostituisci(doc, 'ANSC_CFG_CAMPO — campi obbligatori e mappatura per operazione.',
                'ANSC_CFG_CAMPO — campi obbligatori e mappatura per UC.',
                attese=1, etichetta='§8.4 · «per operazione» → «per UC»', fatti=fatti)

    sostituisci(
        doc,
        'Le due tabelle sono versionate insieme (ID_VERSIONE, verso ANSC_CFG_VERSIONE) e hanno '
        'validità temporale, come le decodifiche ANSC e SIPO.',
        'Le tabelle della configurazione — ANSC_CFG_OPERAZIONE, ANSC_CFG_REGOLA con le sue '
        'condizioni, ANSC_CFG_CAMPO e ANSC_CFG_ALLEGATO — sono versionate insieme '
        '(ID_VERSIONE, verso ANSC_CFG_VERSIONE) e hanno validità temporale, come le decodifiche '
        'ANSC e SIPO. Restano fuori dalla baseline il catalogo degli UC (ANSC_ANA_UC) e i '
        'dizionari, che sono repliche di quanto ANSC pubblica e sono governati dalla propria '
        'validità temporale.',
        attese=1, etichetta='§8.4 · elenco delle tabelle della baseline', fatti=fatti)

    sostituisci(
        doc,
        '2. Determinazione dell’operazione: il front-end invia il tipo operazione, oppure lo si '
        'deduce dal tipo atto SIPO (CONF_TIPO_ATTI.ID_MODELLO_ATTO → Modello). Il concentratore '
        'risolve la riga ANSC_CFG_OPERAZIONE valida.',
        '2. Determinazione dell’operazione e dell’UC: il front-end invia il tipo operazione, '
        'oppure lo si deduce dal tipo atto SIPO (CONF_TIPO_ATTI.ID_MODELLO_ATTO → Modello). Il '
        'concentratore risolve la riga ANSC_CFG_OPERAZIONE valida e, su di essa, valuta le '
        'regole di determinazione (ANSC_CFG_REGOLA) per stabilire quale UC di ANSC corrisponda '
        'ai dati dell’atto. È l’UC, non il Modello, a governare i due passi successivi.',
        attese=1, etichetta='§8.4 · passo 2 (determinazione dell’UC)', fatti=fatti)

    sostituisci(
        doc,
        '3. Verifica (sincrona): letti i campi da ANSC_CFG_CAMPO, il concentratore controlla '
        'presenza e validità dei campi (incluse le condizioni) sul payload ricostruito da SIPO.',
        '3. Verifica (sincrona): letti da ANSC_CFG_CAMPO i campi dichiarati per l’UC determinato '
        'e da ANSC_CFG_ALLEGATO i documenti che esso richiede, il concentratore controlla '
        'presenza e validità dei campi (incluse le condizioni) sul payload ricostruito da SIPO.',
        attese=1, etichetta='§8.4 · passo 3 (campi e allegati dell’UC)', fatti=fatti)


# ============================================== capitolo 9 · apertura: il modello evento
def apri_capitolo_9(doc, modello_tab):
    a = h(doc, 2, 'Atto di morte SIPO → UC ANSC')._p

    h2(doc, a, 'Il modello evento: la struttura portante di tutti gli UC')
    p(doc, a,
      'Il presente capitolo descrive come i dati dell’atto conservati in SIPO diventino il '
      'payload atteso da ANSC. Prima della mappatura conviene però stabilire che cosa sia il '
      'bersaglio, perché su questo punto ricorre un equivoco che ha conseguenze di disegno: che '
      'ogni caso d’uso di ANSC abbia una propria struttura di payload, e che l’integrazione '
      'debba quindi produrre tante forme quante sono le tipologie di atto. Non è così. La '
      'struttura è una sola per tutto lo stato civile, ed è il modello evento.')

    h3(doc, a, 'Che cosa è il modello evento')
    p(doc, a,
      'Il modello evento è il contratto di dati di ANSC, pubblicato nel file '
      'openapi/model_evento.yaml del repository dei servizi cooperativi [R1]. È un unico albero '
      'di schemi con una sola radice, ModelEvento, dalla quale discende ogni informazione che il '
      'sistema nazionale sia in grado di ricevere per un atto di stato civile: gli intestatari, '
      'i dichiaranti, i dati dell’evento per ciascuna materia, l’atto collegato, le annotazioni '
      'contestuali, gli allegati, i dati dell’ufficio.')
    p(doc, a,
      'La misura dell’albero spiega perché convenga trattarlo come una struttura sola. Il file '
      'dichiara novanta schemi in 3.734 righe. La radice ha 111 proprietà di primo livello: '
      'cinquantasette scalari, quarantasette oggetti e sette liste. Espandendo i riferimenti si '
      'ottengono 8.256 percorsi distinti, contando una sola volta gli elementi di una lista e '
      'troncando l’espansione quando uno schema si ripresenta lungo lo stesso ramo. Il riuso è '
      'esteso: ModelSoggetto e ModelAttoCollegato compaiono quarantanove volte ciascuno, '
      'ModelEnteDichiarante trentuno, per un totale di 382 riferimenti interni. È la ragione per '
      'cui un albero di ottomila percorsi si descrive con novanta schemi soltanto.')
    p(doc, a,
      'Il modello non è un allegato del solo servizio di validazione. Su venticinque contratti '
      'ANSC, sedici lo referenziano e dieci lo impiegano per intero — R004, R005, R009, R010, '
      'R011, R013, R015, R016, R017 e R020 — sicché la medesima struttura serve tanto al '
      'deposito quanto alla consultazione, alla rettifica, all’annullamento e al provvedimento '
      'di rifiuto. L’unica variante rilevante è ModelEventoRidotto, definito nel contratto R005 '
      'con ventisette proprietà: è la proiezione che la consultazione restituisce quando non '
      'occorre l’atto completo.')
    tabella(doc, a, [
        ['Grandezza', 'Valore', 'Che cosa comporta per il disegno'],
        ['Schemi dichiarati', '90 (3.734 righe)',
         'Un solo file da sorvegliare a ogni rilascio del contratto.'],
        ['Proprietà di primo livello', '111 (57 scalari, 47 oggetti, 7 liste)',
         'La testata e i grandi blocchi di materia stanno tutti allo stesso livello.'],
        ['Percorsi distinti dell’albero', '8.256',
         'È lo spazio dei valori ammessi di ANSC_CFG_CAMPO.CAMPO_ANSC.'],
        ['Schemi in versione multilingua', '38 su 90',
         'Quasi metà dell’albero duplica rami per la resa in più lingue: 7.190 percorsi '
         'restano escludendoli.'],
        ['Riferimenti interni', '382 (ModelSoggetto e ModelAttoCollegato 49 volte ciascuno)',
         'Il codice di mappatura di un soggetto si scrive una volta e vale ovunque.'],
        ['Contratti che lo referenziano', '16 su 25 (10 per intero)',
         'La stessa struttura serve deposito, consultazione, rettifica e rifiuto.'],
        ['Proprietà deprecate', '6 al primo livello, 19 in tutto',
         'Da non mappare: l’identità dell’operatore viaggia nel token, non nel payload.'],
    ], modello_tab, larghezze=[1.5, 1.9, 3.0])
    para(doc, a, 'Il modello evento in cifre (rilevazione diretta su openapi/model_evento.yaml, '
                 'contratto 1.53.0).', corsivo=True)

    h3(doc, a, 'Un superset discriminato: struttura unica, significato per UC')
    p(doc, a,
      'La forma in cui ANSC ha risolto la varietà dello stato civile è quella del superset '
      'discriminato. Il modello contiene l’unione di tutto ciò che può servire a qualunque atto; '
      'è la testata a dichiarare, con idUsecase, di quale caso d’uso si tratti; e il modello non '
      'cambia forma di conseguenza. Non vi sono né oneOf né discriminator, e nessun campo del '
      'corpo è dichiarato obbligatorio a livello di schema: nel modello i campi sono tutti '
      'opzionali. Ne discende il fatto che governa l’intero disegno della configurazione: '
      '**chi valida deve conoscere l’UC**, perché la struttura da sola non contiene abbastanza '
      'informazione per dire se un atto sia completo.')
    p(doc, a,
      'Quanta parte dell’albero sia effettivamente esercitata lo dice il confronto con il '
      'mapping ufficiale. I 374 casi d’uso validi impiegano complessivamente 2.958 percorsi '
      'distinti, pari al 35,2 per cento dell’albero, che diventa il 40,5 per cento se si '
      'escludono i rami multilingua. Il singolo UC ne usa molti meno: da un minimo di '
      'quattordici a un massimo di 674, con una mediana di 154. Il modello è dunque un '
      'contenitore ampio del quale ciascun caso d’uso valorizza una porzione ristretta, e quale '
      'sia la porzione lo dichiara il mapping, non il modello.')

    h3(doc, a, 'Che cosa il modello non dice')
    p(doc, a,
      'Il modello evento è esaustivo sulla forma e silenzioso sul merito. Quattro informazioni '
      'necessarie a formare un atto non vi si trovano, e sono esattamente quelle che la '
      'configurazione descritta in questo capitolo deve fornire.')
    voce(doc, a, 'Quali campi siano obbligatori. ',
         'Nel modello sono tutti opzionali. L’obbligatorietà è dichiarata per UC nei file di '
         'mapping ed è verificata da R009.')
    voce(doc, a, 'Quali blocchi valgano per quale UC. ',
         'Nulla nel modello dice che i dati di matrimonio non si compilano per un decesso: la '
         'pertinenza è dichiarata altrove.')
    voce(doc, a, 'Quali documenti allegare. ',
         'Il modello prevede la struttura dell’allegato, non l’elenco di quelli richiesti dal '
         'singolo caso d’uso.')
    voce(doc, a, 'Quali formule ministeriali si applichino. ',
         'Il mapping le dichiara per 366 UC su 374; il modello non le contempla (OP-51).')
    p(doc, a,
      'A queste si aggiungono due asperità da conoscere prima di scrivere l’adattatore. La prima '
      'è che trentotto schemi su novanta sono duplicati multilingua, riconoscibili dal suffisso '
      'ML: sono la stessa informazione resa in più lingue e vanno trattati come un ramo solo, '
      'altrimenti la mappatura si raddoppia senza ragione. La seconda è che diciannove '
      'proprietà risultano deprecate, sei delle quali al primo livello; fra queste i dati '
      'dell’operatore, che nel modello di esecuzione adottato viaggiano nel token e non nel '
      'corpo del messaggio. Mapparle sarebbe lavoro destinato a essere disfatto.')

    h3(doc, a, 'Perché è la spina dorsale, e che cosa ne consegue')
    p(doc, a,
      'Il modello evento può essere assunto come struttura portante di tutta l’integrazione, e '
      'conviene farlo esplicitamente. La conseguenza pratica è che **il payload non si '
      'costruisce per caso d’uso: si costruisce una volta sola sull’albero del modello e si '
      'riempie secondo la configurazione**. L’adattatore di mappatura è perciò uno solo per '
      'tutte le famiglie di atti, non uno per famiglia; ciò che varia da un atto all’altro sono '
      'righe di configurazione, non rami di codice.')
    p(doc, a,
      'Se il modello è la spina dorsale, la configurazione ne è la vertebratura. Il catalogo '
      'degli UC (ANSC_ANA_UC) dichiara quali casi d’uso esistano; le regole di determinazione '
      'stabiliscono a quale di essi conduca un Modello del Comune secondo i dati dell’atto; '
      'ANSC_CFG_CAMPO dichiara, per l’UC, quali percorsi dell’albero valgano, se siano '
      'obbligatori e da quale colonna di SIPO si riempiano; ANSC_CFG_ALLEGATO dichiara quali '
      'documenti servano. Nessuna di queste tabelle ridefinisce la struttura: tutte la '
      'annotano. È il motivo per cui la portata dell’integrazione si misura in righe di '
      'configurazione — poco più di sessantamila per l’intero dominio — e non in numero di '
      'programmi.')
    p(doc, a,
      'Ne discende anche il modo in cui si assorbono i cambiamenti. Se cambia il modello, cambia '
      'un albero solo, e l’impatto si misura confrontando i percorsi; se cambia il mapping, '
      'cambiano righe di configurazione, e l’impatto si misura confrontando le baseline. Il '
      'capitolo 12 descrive il procedimento; qui importa che entrambi i casi si risolvano senza '
      'toccare il codice dell’adattatore.')


# ============================== capitolo 9 · chiusura: fonti, catena, procedura di revisione
def chiudi_capitolo_9(doc, modello_tab):
    a = h(doc, 1, 'Le regole di determinazione e di controllo')._p

    # ---------------------------------------------------------------- le fonti
    h2(doc, a, 'Le fonti della configurazione: quali file servono e a che cosa')
    p(doc, a,
      'La configurazione descritta nei paragrafi precedenti non si redige: si deriva da file che '
      'ANSC pubblica e che il Comune non scrive. Elencarli con precisione è parte del disegno, '
      'perché da essi dipendono tanto il primo popolamento quanto ogni revisione successiva, e '
      'perché la loro reperibilità è un presupposto operativo dell’intera soluzione (OP-36).')
    tabella(doc, a, [
        ['Fonte', 'Che cosa contiene', 'Che cosa alimenta'],
        ['openapi/model_evento.yaml',
         '90 schemi, 8.256 percorsi: la struttura del payload.',
         'Lo spazio dei valori ammessi di ANSC_CFG_CAMPO.CAMPO_ANSC e la forma che '
         'l’adattatore costruisce.'],
        ['openapi/R001–R024, R901 (25 contratti)',
         'Le operazioni cooperative, i loro percorsi e i codici di errore.',
         'ANSC_CFG_OPERAZIONE.SERVIZIO_ANSC e le schede dei servizi del capitolo 17.'],
        ['Mapping_casi_uso/3_dec_use_case.csv (ANSC_03)',
         'Il catalogo dei casi d’uso: codice numerico e codice motore.',
         'ANSC_ANA_UC (374 UC validi).'],
        ['Mapping_casi_uso/<famiglia>/<codice motore>.csv',
         '374 file, 67.674 righe, sette colonne: sezione, campo, obbligatorietà, Binding Object, '
         'Binding Field, formule, condizioni.',
         'ANSC_CFG_CAMPO (campi, obbligatorietà, condizioni) e ANSC_CFG_ALLEGATO (sezione '
         '«Allegati», 1.569 righe).'],
        ['Mapping_casi_uso/changelog_mapping.md',
         '66 revisioni del mapping dal 2023, una ogni diciassette giorni.',
         'L’intercetto della necessità di revisione (capitolo 12).'],
        ['Decodifiche/ (145 file, 143 identificativi, 1.376 righe)',
         'I valori ammessi dei campi codificati.',
         'ANSC_DIZ_CATALOGO e ANSC_DIZ_VALORE, per il tramite di R901: i file sono il '
         'riscontro, non il canale.'],
        ['Changelog.md',
         '194 rilasci datati del contratto, dal 16/10/2023 al 30/06/2026.',
         'La sorveglianza sulle modifiche di struttura.'],
        ['SIPO — CONF_TIPO_ATTI',
         'I Modelli di atto del Comune, con tipo atto e maschera.',
         'ANSC_CFG_OPERAZIONE (ID_MODELLO_ATTO, ID_CONF_TIPO_ATTO, MASCHERA_UI).'],
    ], modello_tab, larghezze=[1.7, 2.3, 2.4])
    para(doc, a, 'Le fonti della configurazione. Le prime sette sono di ANSC e non si '
                 'modificano; l’ottava è del Comune.', corsivo=True)
    pb(doc, a, 'Il lavoro umano è dove le fonti tacciono. ',
       'Da quanto precede si ricava che l’immissione manuale non è il modo in cui la '
       'configurazione si popola, e che pensarla così porterebbe a sottostimare il progetto nel '
       'punto sbagliato. Delle oltre sessantamila righe di mappatura dell’intero dominio, la '
       'quasi totalità si importa; restano tre lavorazioni che nessuna fonte può svolgere al '
       'posto del Comune: **completare la colonna SIPO** di ciascun campo, cioè dire da dove il '
       'dato si prende; **raccordare le descrizioni di allegato** ai tipi codificati per le sei '
       'che non trovano corrispondenza (OP-50); **scrivere le regole di determinazione**, che '
       'sono poche — dell’ordine di 374 — e sono l’unico punto in cui serve il giudizio del '
       'funzionario.')

    # ---------------------------------------------------------------- la catena
    h2(doc, a, 'La catena completa: dal Modello di SIPO al payload ANSC')
    p(doc, a,
      'Le tabelle di configurazione sono descritte, ciascuna al proprio posto, nei capitoli 8, '
      '9, 10, 11 e 12 e nell’Appendice A. Manca però il luogo in cui la catena si legge per '
      'intero, dalla maschera che l’operatore compila fino al messaggio che parte verso ANSC. La '
      'figura seguente la ricompone in tre fasce: le fonti, che ANSC pubblica; la '
      'configurazione, che il Comune tiene in una baseline versionata; l’esecuzione, cioè che '
      'cosa accade quando l’operatore preme «Finalizza».')
    immagine(doc, a, PNG, 6.6,
             'Dalla maschera SIPO al payload ANSC. Ogni riga di configurazione ha una fonte '
             'dichiarata e ogni passo dell’esecuzione ha una tabella che lo guida; le due '
             'tabelle in verde sono le sole scritte dal Comune.')
    p(doc, a,
      'Della fascia intermedia va notato che cosa vi stia dentro e che cosa ne resti fuori. '
      'Nella baseline stanno le quattro tabelle che il Comune governa — ANSC_CFG_OPERAZIONE, '
      'ANSC_CFG_REGOLA con le sue condizioni, ANSC_CFG_CAMPO e ANSC_CFG_ALLEGATO — perché '
      'devono attivarsi e storicizzarsi in blocco: una configurazione a metà, con i campi di una '
      'revisione e le regole di un’altra, produrrebbe atti che superano il pre-filtro e vengono '
      'respinti da R009. Ne restano fuori il catalogo degli UC e i dizionari, che sono repliche '
      'di quanto ANSC dichiara e hanno una propria validità temporale: replicarli anche nella '
      'baseline significherebbe conservare copie di una verità che non ci appartiene.')
    p(doc, a,
      'Della terza fascia va notato il quinto passo, che è quello da cui dipende il '
      'dimensionamento dello sviluppo. Determinato l’UC e superato il pre-filtro, la costruzione '
      'del payload consiste nello scrivere ciascun valore letto da SIPO nel percorso del modello '
      'che la configurazione gli assegna. Non vi è, in questo passo, alcuna logica specifica '
      'della tipologia di atto: la tipologia è già stata risolta a monte, dalle regole, e si '
      'manifesta soltanto come insieme diverso di righe di ANSC_CFG_CAMPO. È la ragione per cui '
      'l’estensione a una nuova famiglia di atti — descritta nel capitolo 22 — è un fatto di '
      'configurazione e di verifica, non di scrittura di nuovo codice di mappatura.')

    # ---------------------------------------------------- revisione della mappatura
    h2(doc, a, 'Come si rivede la mappatura fra i campi di SIPO e il modello evento')
    p(doc, a,
      'La mappatura non è un lavoro che si compia una volta. Il mapping degli UC è stato rivisto '
      'sessantasei volte dal 2023, e 355 casi d’uso su 374 sono stati toccati almeno una volta: '
      'la revisione è il regime ordinario, non l’eccezione. Il capitolo 12 stabilisce come si '
      'intercetta la necessità di rivedere e come si attiva una nuova baseline; qui si stabilisce '
      'che cosa si fa in mezzo, cioè come la mappatura si rivede senza perdere il lavoro già '
      'fatto e senza introdurre divergenze rispetto alla fonte.')

    h3(doc, a, 'Il procedimento')
    for testa, corpo in [
        ('1. Rilevare la revisione. ',
         'Dal changelog del mapping e dal changelog del contratto si ricava l’elenco degli UC '
         'toccati; la mediana storica è di undici UC per revisione, ma il massimo osservato è '
         '301, e la differenza fra i due casi è la differenza fra una verifica e un progetto.'),
        ('2. Rigenerare l’estrazione in una versione BOZZA. ',
         'I file del mapping si rileggono per intero e producono le righe di ANSC_CFG_CAMPO e '
         'ANSC_CFG_ALLEGATO di una nuova versione in stato BOZZA. Non si applicano differenziali '
         'alle righe attive: la baseline si costruisce sempre per copia integrale, per le '
         'ragioni argomentate al capitolo 12.'),
        ('3. Risolvere ogni riferimento sull’albero del modello. ',
         'La coppia Binding Object e Binding Field forma un percorso che deve esistere nel '
         'modello evento. La risoluzione normalizza gli indici di lista, perché il mapping '
         'talvolta li omette e talvolta li numera, mentre la configurazione deve conservarne una '
         'forma sola.'),
        ('4. Riportare i riferimenti non risolti, mai scartarli. ',
         'Un percorso che non trova riscontro nel modello è un’informazione, non un rifiuto: '
         'indica una divergenza fra le due fonti di ANSC e va portata all’attenzione, perché '
         'scartandola in silenzio si otterrebbe una configurazione che sembra completa e non lo '
         'è. Il paragrafo seguente riporta l’esito di questo controllo sulla base odierna.'),
        ('5. Riportare la colonna SIPO dalla versione attiva. ',
         'Per i percorsi invariati il raccordo con la colonna di SIPO si eredita dalla versione '
         'in esercizio: è il lavoro umano accumulato, ed è la sola parte della configurazione '
         'che una rigenerazione potrebbe distruggere. I percorsi nuovi restano privi di '
         'raccordo e compaiono nella lista di lavorazione del back-office.'),
        ('6. Controllare la completezza prima di attivare. ',
         'Sulla versione in bozza si verificano quattro cose: che nessun campo obbligatorio '
         'resti privo di colonna SIPO; che ogni campo codificato richiami un dizionario '
         'presente e valido; che ogni allegato richiesto abbia un tipo raccordato; e che le '
         'regole di determinazione coprano tutti i Modelli e restino mutuamente esclusive, '
         'secondo i controlli descritti al capitolo 10.'),
        ('7. Attivare in blocco e conservare la precedente. ',
         'L’attivazione porta la nuova versione in stato ATTIVA e la precedente in STORICA. '
         'Poiché lo stato dell’atto registra la versione di configurazione con cui è stato '
         'formato, resta sempre possibile ricostruire con quali regole un atto sia stato '
         'validato, e il rientro alla versione precedente è un cambio di stato.'),
    ]:
        voce(doc, a, testa, corpo)

    h3(doc, a, 'Il controllo di risolvibilità: l’esito sulla base odierna')
    p(doc, a,
      'Il controllo descritto al terzo e al quarto passo è stato eseguito sull’intera base: i '
      '374 file di mapping impiegano 2.958 percorsi distinti, dei quali 2.910 trovano riscontro '
      'nel modello evento. Ne restano quarantotto che non si risolvono, per 232 occorrenze '
      'distribuite su cinquantacinque casi d’uso. Non riguardano l’atto di morte, e quindi non '
      'incidono sul pilota, ma vanno conosciuti prima di affrontare le famiglie successive. Si '
      'distinguono in due classi, e la distinzione è importante perché solo la prima si risolve '
      'da sé.')
    pb(doc, a, 'Indice di lista omesso — quattro percorsi, 157 occorrenze. ',
       'I quattro campi delle annotazioni contestuali sono citati dal mapping come '
       'evento.datiAnnotazione.testoAnnotazione e simili, mentre nel modello datiAnnotazione è '
       'una lista di ModelDatiAnnotazione, che quei quattro campi possiede. Non è una '
       'divergenza: è una notazione diversa, e la normalizzazione degli indici prescritta al '
       'terzo passo la risolve senza intervento.')
    pb(doc, a, 'Divergenza effettiva — quarantaquattro percorsi, 75 occorrenze. ',
       'Qui il mapping dichiara campi che nel modello non esistono. La concentrazione maggiore '
       'è sotto evento.datiEventoMatrimonio.regimePatrimoniale, dove trentasette percorsi — fra '
       'cui un intero blocco assistenteLegale — non hanno riscontro: lo schema '
       'ModelRegimePatrimoniale dichiara quattordici proprietà e non contempla né '
       'l’assistente legale né gli altri campi citati. I rimanenti sette sono elencati nella '
       'tabella seguente. Nessuno di essi è ricostruibile per interpretazione, e tutti vanno '
       'chiariti con il fornitore di ANSC prima di configurare le famiglie interessate (OP-52).')
    tabella(doc, a, [
        ['Percorso dichiarato dal mapping', 'UC interessati', 'Rilievo'],
        ['evento.datiEventoMatrimonio.regimePatrimoniale.* (37 percorsi)', 'matrimoni e '
         'trascrizioni di matrimonio',
         'ModelRegimePatrimoniale ha 14 proprietà e non contiene i campi citati, fra cui il '
         'blocco assistenteLegale.'],
        ['evento.datiEventoMatrimonio.formatoDataEvento e .idFormatoDataEvento',
         'Trascr_Matr_001 e seguenti',
         'Il changelog 1.53.0 dichiara idFormatoDataEvento aggiunto a ModelMatrimonio, ma nel '
         'contratto non compare.'],
        ['evento.datiEventoUnioneCivile.appartenenzaCognomeComune e .posizioneCognomeComune',
         'UnCiv_009', 'Assenti da ModelUnioneCivile.'],
        ['evento.trascrizioneUnioneCivile.sessoPrima e .sessoDopo', 'Trascr_UnCiv_006',
         'Assenti da ModelTrascrizioneUnioneCivile.'],
        ['evento.trascrizioneCittadinanza.altraCittadinanzaRiacquistata', 'Citt_024',
         'Assente da ModelTrascrizioneCittadinanza.'],
    ], modello_tab, larghezze=[2.5, 1.5, 2.4])
    para(doc, a, 'I riferimenti del mapping che non trovano riscontro nel modello evento '
                 '(rilevazione diretta sui 374 file di mapping e su model_evento.yaml).',
         corsivo=True)

    h3(doc, a, 'Tre cose che non devono accadere')
    voce(doc, a, 'Scartare in silenzio ciò che non si risolve. ',
         'È il modo in cui una configurazione incompleta si presenta come completa. I riferimenti '
         'non risolti vanno esposti nel back-office e censiti come punti aperti.')
    voce(doc, a, 'Correggere a mano le righe importate. ',
         'La correzione sopravvive fino alla revisione successiva e poi scompare, lasciando una '
         'divergenza silenziosa rispetto al mapping ufficiale. Ciò che va corretto nel mapping si '
         'segnala ad ANSC; ciò che è del Comune sta nelle colonne del Comune.')
    voce(doc, a, 'Scrivere codice di mappatura per famiglia di atti. ',
         'L’adattatore è uno solo e lavora sull’albero del modello; ogni ramo condizionale '
         'introdotto per una famiglia è configurazione mancata, e va ricondotto a righe di '
         'ANSC_CFG_CAMPO o a una regola.')


# ===================================================================== open point
def aggiungi_op(doc):
    t = trova_tabella(doc, 'tema', 'questione', 'priorità')
    assert t.rows[-1].cells[0].text.strip() == 'OP-51', t.rows[-1].cells[0].text
    clona_riga(t, (
        'OP-52',
        'Percorsi del mapping assenti dal modello evento',
        'Quarantaquattro percorsi dichiarati dal mapping degli UC non trovano riscontro nel '
        'modello evento (232 occorrenze su 55 casi d’uso di matrimonio, unione civile, '
        'cittadinanza e trascrizione), fra cui 37 sotto regimePatrimoniale e i campi di formato '
        'della data che il changelog 1.53.0 dichiara aggiunti e che nel contratto non compaiono. '
        'Non toccano il pilota della morte, ma vanno chiariti prima di configurare le famiglie '
        'interessate: se il campo esiste, manca dal contratto; se non esiste, il mapping è da '
        'correggere.',
        'Aperto', 'Analisi / Fornitore ANSC', 'Media'))
    return len(t.rows) - 1


# ===================================================================== main
def main():
    doc = docx.Document(SRC)
    fatti = []
    modello_tab = trova_tabella(doc, 'id', 'riferimento', 'contenuto')

    correggi_84(doc, fatti)
    apri_capitolo_9(doc, modello_tab)
    chiudi_capitolo_9(doc, modello_tab)
    n_op = aggiungi_op(doc)

    # intestazione e storia
    for s in doc.sections:
        for tb in s.header.tables:
            for r in tb.rows:
                for c in r.cells:
                    for pr in c.paragraphs:
                        if 'Versione 3.12' in pr.text:
                            for run in pr.runs:
                                run.text = run.text.replace('3.12', '3.13')
    storia(doc, '03/09/2026', '3.13',
           'Modello dati (§8.4); Mappatura del payload (cap. 9); Open Point',
           'Revisione della parte di configurazione. Il capitolo 9 si apre con la definizione '
           'del modello evento — struttura, cifre, natura di superset discriminato e ciò che il '
           'modello non dice — assunto esplicitamente come struttura portante di tutti gli UC, e '
           'si chiude con le fonti della configurazione, la catena completa dal Modello di SIPO '
           'al payload ANSC (nuova figura) e la procedura di revisione della mappatura, con '
           'l’esito del controllo di risolvibilità dei riferimenti sul modello. In §8.4 corrette '
           'le formulazioni «per operazione» rimaste dalla versione 2.x, allineato l’elenco '
           'delle tabelle della baseline e reso esplicito il passo di determinazione dell’UC. '
           'Nuovo OP-52.')

    doc.save(DST)
    for f in fatti:
        print('  ·', f)
    print('open point:', n_op)
    print('capitoli/tabelle/immagini:', riepilogo(DST))
    print(DST)


if __name__ == '__main__':
    main()
