# -*- coding: utf-8 -*-
"""v0.3 di «ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC» (10/11/2026).

Si modifica il FILE REALE della v0.2. Nuovo capitolo «Le annotazioni rettificative: errore
materiale (art. 98) e rettifica (art. 95)», prima di «Dove e come inserirsi». Decisioni
dell'utente: il capitolo sta in questo documento (non in quello sugli atti a testo libero);
art. 98 al centro, art. 95 nello stesso capitolo, annotazione modificativa e R017 come
confronto; proposta per SIPO in due fasi come per l'annullamento; annotazioni su atto
cartaceo incluse.

Fatti verificati (rapporto del 10/11 e controlli diretti):
  * R013 1.4.0: /rettifica/validazione/evento (art. 95 e 98) e
    /annotazione/modificativa/validazione/evento; nessun operationId; richiesta evento +
    eventoModificato (required fuori dall'allOf); risposta senza idEvento/idAnsc/forcingCode
    propri; idAnsc nell'evento (changelog 1.14.0).
  * 10 UC (ANSC_03 righe 198-199, 231-232, 279-280, 308-309, 375-376); mapping identici fra
    nascita, morte, matrimonio, unione (md5); Morte_012 = 23 righe, 21 campi, 18 SI, formula
    190; Morte_013 = 16 righe, 14 campi, 13 SI, formula 888, correzione in composizioneCompleta;
    Citt_047/048 + 13 campi facoltativi.
  * Guida §9.2.1 «La competenza è dell'ufficiale dello stato civile dove è stato formato
    l'atto da rettificare»; §9.2.2 art. 98 «NON può comportare l'annullamento»; avviso «devi
    procedere alla modifica esplicita dei dati da correggere».
  * Nota di processo §3.2.1: errore materiale con idTipoRettifica 1 ed eventoModificato =
    atto completo già corretto; esempio CasiTest R013_inserimento_annotazione_errore_materiale.
  * Annotazione modificativa su atto cartaceo: 1.33.0 (ID 95); UC 14860000 Dic_Nasc_998_5,
    2351 Morte_998_4, 369100 Matr_998_4, 459100 UnCiv_998_4, 53810 Citt_998_4 (mapping
    identici): formula 998, composizione libera, evento.eventoCollegato con gli estremi.

Le figure successive sono rinumerate (5 → 6, 6 → 7).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/annullamento_v0_3.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import figura, h, par, tabella, voce   # noqa: E402
import diagrammi_rettificative   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.2.docx')
NOME = 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.3'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '10/11/2026'
CAP = 'Le annotazioni rettificative: errore materiale (art. 98) e rettifica (art. 95)'

d = docx.Document(SRC)
body = d.element.body


def heading(testo, livello):
    t = [p for p in d.paragraphs if p.style.name == 'Heading %d' % livello
         and p.text.strip() == testo]
    if len(t) != 1:
        raise SystemExit('heading non univoco: ' + testo)
    return t[0]


def innesta(prima, scrivi):
    """Scrive in coda con le primitive di genera_testo_libero e sposta il blocco prima
    dell'elemento «prima»."""
    sect = body.find(qn('w:sectPr'))
    n0 = len(list(body.iterchildren()))
    scrivi()
    nuovi = [ch for ch in list(body.iterchildren())[n0 - 1:] if ch is not sect
             and ch.getparent() is body]
    for ch in nuovi:
        prima.addprevious(ch)
    return len(nuovi)


# =================================================================== tabelle
STRUMENTI = [
    ['Strumento', 'Chi lo promuove', 'Può annullare', 'Casi d’uso e formula', 'Servizio',
     'Firma'],
    ['Annotazione per errore materiale (art. 98)', 'L’ufficiale, d’ufficio', 'No: solo '
     'correggere', 'Uno per registro (Dic_Nasc_119, Morte_013…); formula 888',
     'R013 /rettifica/validazione', 'Ufficiale (R007)'],
    ['Annotazione per rettifica (art. 95)', 'Un provvedimento di un’altra amministrazione '
     '(per esempio il tribunale)', 'Sì (tipo 0) oppure modifica (tipo 1)', 'Uno per registro '
     '(Dic_Nasc_118, Morte_012…); formula 190', 'R013 /rettifica/validazione',
     'Ufficiale (R007)'],
    ['Annotazione modificativa', 'Provvedimenti specifici: cambio di generalità del '
     'genitore, regime patrimoniale, cambio di sesso', 'No', 'Dic_Nasc_120 e casi d’uso '
     '_998_', 'R013 /annotazione/modificativa/validazione', 'Non descritta'],
    ['Annotazione modificativa su atto cartaceo', 'Il comune', 'No', 'Uno per registro '
     '(*_998_4, Dic_Nasc_998_5); formula 998, testo libero', 'Non dichiarato (AR-20)',
     'Non descritta'],
    ['Correzione di un’annotazione', 'L’ufficiale', 'No', '—', 'R017', 'Firma remota'],
    ['Nota tecnica', 'Il comune che ha redatto l’atto', 'No', '—', 'Solo web app',
     'Non descritta (AR-11)'],
]

CASI_USO = [
    ['Registro', 'Rettifica (art. 95)', 'Errore materiale (art. 98)'],
    ['Nascita', '14630000 · Dic_Nasc_118', '14640000 · Dic_Nasc_119'],
    ['Morte', '2341 · Morte_012', '2342 · Morte_013'],
    ['Matrimonio', '368699 · Matr_017', '368799 · Matr_018'],
    ['Unione civile', '458699 · UnCiv_007', '458799 · UnCiv_008'],
    ['Cittadinanza', '53719 · Citt_047', '53729 · Citt_048'],
]

SEZIONI = [
    ['Sezione del mapping', 'Rettifica (art. 95)', 'Errore materiale (art. 98)'],
    ['Formula', '190, obbligatoria', '888, obbligatoria'],
    ['Allegato generico', 'Facoltativo', 'Facoltativo'],
    ['Formazione atto', 'Numero comunale, data, ora e minuto: tutti obbligatori', 'Uguale'],
    ['Ente dichiarante', 'Estremi del documento, provincia e comune dell’ente obbligatori; nome '
     'dell’ente e indirizzo facoltativi', 'Assente'],
    ['Evento da rettificare / da correggere', 'Provincia, comune, numero comunale, anno, data '
     'e tipo di registro obbligatori; idAnsc facoltativo', 'Uguale'],
    ['Testo', 'datiRettifica.dettaglioRettifica', 'composizioneCompleta («Dettaglio '
     'correzione»)'],
    ['In tutto', '21 campi, 18 obbligatori', '14 campi, 13 obbligatori'],
]

FLUSSO = [
    ['#', 'Passo', 'Sulla web app (guida § 9.2.2)', 'Con i servizi cooperativi', 'Fonte'],
    ['1', 'Scelta', 'Menù del registro → Annotazioni → «Annotazioni per rettifica / errore '
     'materiale» → errore materiale', '—', 'Guida'],
    ['2', 'L’atto da correggere', '«Evento digitale da ricercare nel sistema»', 'R005 per '
     'idAnsc, anche con flagRettifica per leggere l’ultima rettifica', 'Dedotto'],
    ['3', 'Il testo della correzione', 'Testo con la formula dedicata', 'composizioneCompleta; '
     'nell’esempio anche dettaglioRettifica', 'Mapping, esempio'],
    ['4', 'La modifica dei dati', 'Avviso «devi procedere alla modifica esplicita dei dati da '
     'correggere», poi l’atto originale modificabile', 'eventoModificato = l’atto intero già '
     'corretto', 'Guida, nota di processo'],
    ['5', 'Il numero comunale', '—', 'evento.numeroatto, obbligatorio', 'Mapping; la serie non '
     'è dichiarata'],
    ['6', 'Il deposito', 'Salva', 'R013 /rettifica/validazione', 'Contratto'],
    ['7', 'L’attestazione di conformità', 'Non descritta', 'Indizio nel changelog 1.32.2',
     'Changelog'],
    ['8', 'La firma', 'Firma dell’ufficiale', 'R007 /firma_usc sull’annotazione', 'Guida e '
     'changelog; il parametro è dedotto'],
    ['9', 'La verifica', '—', 'R005', 'Dedotto'],
]

STORIA = [
    ['Versione', 'Che cosa'],
    ['1.5.0 (03/03/2023)', 'R013, decodifica ANSC_79, annotazioni di rettifica sulla web app.'],
    ['1.6.0 (07/04/2023)', 'Annotazioni per errore materiale.'],
    ['1.9.1 (19/06/2023)', 'evento ed eventoModificato dichiarati obbligatori.'],
    ['1.14.0 (09/10/2023)', 'Corretta la restituzione dell’idAnsc.'],
    ['1.15.0 (16/10/2023)', 'eventoModificato non obbligatorio per la rettifica di '
     'annullamento.'],
    ['1.20.0 (01/12/2023)', 'L’operazione per le annotazioni modificative; flagRettifica in '
     'R005.'],
    ['1.21.0 (11/12/2023)', 'Controllo sull’atto già annullato.'],
    ['1.32.2 → 1.37.0 (08/2024 → 02/2025)', 'Correzioni sulla firma dell’ufficiale delle '
     'rettifiche con i servizi cooperativi.'],
    ['1.33.0 (03/10/2024)', 'Annotazione modificativa su atti cartacei (ID 95).'],
    ['1.38.0 (04/03/2025)', 'Controllo dell’identificativo di ogni intestatario nell’atto '
     'rettificato.'],
    ['1.44.2, 1.46.2 (10-11/2025)', 'L’identificativo di eventoModificato non è più un '
     'controllo bloccante, solo un avviso.'],
    ['1.47.0 (22/12/2025)', 'Notifica automatica al comune che detiene l’atto principale dopo '
     'un errore materiale su un evento secondario; conservazione degli atti rettificati.'],
    ['1.49.0 (03/03/2026)', 'Corretto l’invio della notifica anagrafica al comune di residenza '
     'per l’errore materiale; rigenerazione delle annotazioni sull’atto principale.'],
    ['1.53.0 (30/06/2026)', 'Correzione per errore materiale riferita a un’altra annotazione '
     '(R017).'],
]

CARTACEI = [
    ['Registro', 'Caso d’uso'],
    ['Nascita', '14860000 · Dic_Nasc_998_5'],
    ['Morte', '2351 · Morte_998_4'],
    ['Matrimonio', '369100 · Matr_998_4'],
    ['Unione civile', '459100 · UnCiv_998_4'],
    ['Cittadinanza', '53810 · Citt_998_4'],
]

OPERAZIONI = [
    ['Operazione', 'Percorso', 'Servizio ANSC', 'Nota'],
    ['creaAnnotazioneRettificativa', 'POST /ansc/v1/atti/{idAtto}/annotazioni-rettificative',
     'R013 /rettifica/validazione', 'Nuova. Riceve tipo (art. 95 o 98), dati corretti, '
     'provvedimento per l’art. 95; il concentratore compone evento ed eventoModificato.'],
    ['firmaAtto', 'POST /ansc/v1/atti/{idAtto}/firme', 'R007', 'Esistente [R1], usata '
     'sull’annotazione.'],
    ['leggiAtto, riconciliazioni', 'Esistenti [R1]', 'R005', 'Lettura dell’atto e verifica.'],
]

REGISTRO = [
    ['Colonna proposta', 'Contenuto'],
    ['ID_ANNOTAZIONE_RETT', 'Chiave tecnica.'],
    ['ID_ATTO_SIPO', 'L’atto annotato, per valore.'],
    ['ID_ANNOTAZIONE_ATTO', 'La riga del modulo delle annotazioni di SIPO, se c’è (AR-21).'],
    ['COD_UC_ANSC, COD_ARTICOLO', 'Il caso d’uso e l’articolo (95 o 98).'],
    ['ID_TIPO_RETTIFICA', 'ANSC_79 (AR-14).'],
    ['ID_ANSC, ID_EVENTO_ANSC', 'Gli identificativi dell’annotazione in ANSC.'],
    ['NUMERO_ATTO', 'Il numero comunale dell’annotazione.'],
    ['ID_STATO, STATO', 'Lo stato ANSC_11 dell’annotazione.'],
    ['TXT_EVENTO, TXT_EVENTO_MODIFICATO', 'Ciò che è stato depositato.'],
    ['TS_INS, UTENTE_INS, TS_UPD, UTENTE_UPD', 'Campi tecnici.'],
]

APERTI = [
    ('AR-14', 'Valore di idTipoRettifica per l’errore materiale: la nota di processo e '
     'l’esempio usano 1 (MODIFICA), nessun mapping lo dichiara; i valori 3 e 4 di ANSC_79 non '
     'sono spiegati da nessuna fonte.', 'Analisi / Sogei'),
    ('AR-15', 'Stato dell’annotazione dopo R013 e dopo la firma, e stato dell’atto corretto; '
     'dove R013 restituisca gli identificativi (la risposta non ha campi propri, a differenza '
     'di R009).', 'Analisi / Sogei'),
    ('AR-16', 'Da quale serie venga il numero comunale dell’annotazione: il mapping lo chiede '
     'obbligatorio, nessuna fonte dice se sia la serie degli atti.', 'Comune / Analisi'),
    ('AR-17', 'Se l’annotazione richieda l’attestazione di conformità, come lascia intendere '
     'il changelog 1.32.2.', 'Analisi / Sogei'),
    ('AR-18', 'Il testo delle formule 888 e 190: non è pubblicato in nessuna fonte ANSC.',
     'Comune / Sogei'),
    ('AR-19', 'Quali dati si possano correggere con l’art. 98: la guida dice i dati '
     'anagrafici dell’intestatario e, nelle nascite, dei genitori; non c’è un elenco, e ANSC '
     'applica controlli propri (1.34.3, 1.50.0).', 'Comune / Sogei'),
    ('AR-20', 'Annotazioni su atto cartaceo: con quale servizio si depositano e se il Comune '
     'debba registrarle in ANSC per i propri atti cartacei, compresa la correzione per errore '
     'materiale su un atto cartaceo.', 'Comune / Sogei'),
    ('AR-21', 'Raccordo con il modulo delle annotazioni di SIPO: come i tipi di '
     'CONF_TIPO_ANNOTAZIONE (contenuto non fra le sorgenti) corrispondano ai casi d’uso ANSC e '
     'se l’annotazione formata in ANSC debba avere una riga in ANNOTAZIONE_ATTO. Si lega ad '
     'AR-07.', 'Analisi / Sviluppo SIPO'),
]


# =================================================================== capitolo
def capitolo():
    h(d, 1, CAP)
    par(d, 'Un atto firmato dall’ufficiale in ANSC non si modifica: si annota. Questo capitolo '
           'tratta le annotazioni che correggono o annullano un atto formato, con al centro '
           'quella per errore materiale (art. 98 del D.P.R. 396/2000), che l’ufficiale fa da '
           'sé, e accanto quella per rettifica (art. 95), che nasce da un provvedimento. '
           'Condividono servizio e struttura, e per questo si descrivono insieme. Le altre '
           'annotazioni compaiono solo come confronto.')

    h(d, 2, 'Che cosa sono e come si distinguono')
    tabella(d, STRUMENTI, [1.3, 1.3, 0.8, 1.3, 1.1, 0.8])
    voce(d, 'La competenza.', '«La competenza è dell’ufficiale dello stato civile dove è stato '
         'formato l’atto da rettificare» (Guida operativa, § 9.2.1). Vale per entrambe le '
         'annotazioni, e l’atto da correggere è un «evento digitale da ricercare nel '
         'sistema».')
    voce(d, 'Che cosa corregge l’art. 98.', '«A differenza della rettifica, l’errore materiale '
         'NON può comportare l’annullamento dell’atto cui si riferisce ma soltanto la '
         'correzione» (§ 9.2.2). I dati correggibili sono quelli anagrafici dell’intestatario '
         'e, nelle nascite, della madre e del padre.')

    h(d, 2, 'I casi d’uso')
    par(d, 'Sono dieci, due per ciascuno dei cinque registri, tutti di tipo «annotazione» '
           '(ANSC_02 = 2) [A4]:')
    tabella(d, CASI_USO, [1.6, 2.4, 2.4])
    voce(d, 'Un solo mapping per quattro registri.', 'I file di nascita, morte, matrimonio e '
         'unione civile sono identici byte per byte, sia per la rettifica sia per l’errore '
         'materiale. La cittadinanza aggiunge tredici campi facoltativi sull’atto collegato di '
         'cittadinanza.')
    voce(d, 'Niente casi d’uso per riconoscimenti e trascrizioni.', 'L’atto da correggere si '
         'indica con il tipo di registro (ANSC_01) e il tipo di contenuto (atto o '
         'trascrizione): che una trascrizione si corregga con il caso d’uso del suo registro '
         'è una deduzione.')
    par(d, 'Che cosa chiede il mapping, sezione per sezione (morte; gli altri registri sono '
           'uguali):')
    tabella(d, SEZIONI, [1.6, 2.6, 2.2])
    voce(d, 'Nessun dato anagrafico nel mapping.', 'I dieci file descrivono soltanto '
         'l’annotazione: non contengono i campi dei soggetti, né idTipoRettifica, né '
         'eventoModificato. La correzione vera viaggia altrove, come si vede più avanti.')
    voce(d, 'Nessun firmatario oltre l’ufficiale.', 'La tabella dei soggetti per caso d’uso '
         'compilata da Milano non ha righe per questi dieci casi d’uso, e la guida porta dal '
         'salvataggio direttamente alla firma dell’ufficiale.')

    h(d, 2, 'Il servizio R013')
    par(d, 'R013 (contratto 1.4.0) ha due operazioni, nessuna delle due con operationId [A1]:')
    voce(d, '/rettifica/validazione/evento.', 'Serve sia la rettifica sia l’errore materiale. '
         'La richiesta porta evento, l’annotazione, ed eventoModificato, l’atto corretto; il '
         'contratto dichiara obbligatorio il solo evento, ma scrive il vincolo accanto '
         'all’allOf invece che dentro, dove alcuni generatori di client lo ignorano. La '
         'risposta restituisce gli stessi due oggetti.')
    voce(d, '/annotazione/modificativa/validazione/evento.', 'Serve le annotazioni '
         'modificative (cambio di generalità del genitore, regime patrimoniale, cambio di '
         'sesso) e usa datiAnnotazioneModificativa invece di datiRettifica. Aggiunta nella '
         'versione 1.20.0.')
    voce(d, 'Che cosa manca rispetto a R009.', 'Nessun campo proprio per idEvento, idAnsc e '
         'codice di forzatura: gli identificativi dell’annotazione possono stare solo dentro '
         'l’evento restituito (la versione 1.14.0 ne ha corretto la restituzione). Nessuna '
         'forzatura (AR-15).')

    h(d, 2, 'Come si rappresenta la correzione')
    par(d, 'La correzione viaggia su due canali, e nessuna fonte dice che ANSC li confronti.')
    voce(d, 'Il testo.', 'In composizioneCompleta, con la formula 888: nell’esempio ufficiale '
         '«Ai sensi dell’art. 98, c. 1 del D.P.R. n. 396/2000 l’atto soprascritto viene '
         'corretto nel senso che dove è scritto X deve leggersi Y». Il testo della formula non '
         'è pubblicato (AR-18).')
    voce(d, 'L’atto corretto.', 'In eventoModificato, l’atto intero con i dati già corretti e '
         'gli stessi identificativi dell’originale (nota di processo, § 3.2.1). Non esiste una '
         'coppia «valore vecchio, valore nuovo»: il valore vecchio sta solo nel testo.')
    voce(d, 'Il tipo.', 'idTipoRettifica = 1 (MODIFICA) nella nota di processo e '
         'nell’esempio; nessun mapping lo dichiara (AR-14).')
    voce(d, 'Una conseguenza per chi costruisce la richiesta.', 'Testo e atto corretto devono '
         'dire la stessa cosa. Lo stesso esempio ufficiale non lo fa: il nome è corretto '
         'nell’atto, ma la composizione dell’atto modificato parla ancora di un altro nome e '
         'di un altro sesso. Il modo sicuro è ricavare entrambi dalla stessa differenza.')

    h(d, 2, 'Il flusso')
    tabella(d, FLUSSO, [0.3, 1.1, 1.8, 1.9, 1.3])
    par(d, 'Nessuna fonte prevede la firma di un dichiarante né un’anteprima con R010.')

    h(d, 2, 'Gli effetti')
    voce(d, 'Sui documenti.', 'Certificati ed estratti per riassunto escono con i dati già '
         'corretti; la copia integrale riporta l’annotazione a margine (guida §§ 9.2 e 12.2) '
         '[R4].')
    voce(d, 'Sulla nota tecnica.', 'Dopo un’annotazione modificativa la nota tecnica non è più '
         'possibile (servizi di ausilio, § 3.5): conta l’ordine delle operazioni (AR-10).')
    voce(d, 'Sugli altri comuni e sull’anagrafe.', 'Dalla 1.47.0 parte una notifica al comune '
         'che detiene l’atto principale quando l’errore materiale riguarda un evento '
         'secondario; dalla 1.49.0 la notifica anagrafica al comune di residenza. Lo dice solo '
         'il changelog.')
    voce(d, 'Sulle annotazioni automatiche.', 'Si rigenerano sull’atto principale (1.49.0, '
         '1.50.0, 1.53.0).')
    voce(d, 'Sull’atto corretto.', 'Il suo stato dopo l’annotazione non è dichiarato '
         '(AR-15).')

    h(d, 2, 'Le annotazioni su atto cartaceo')
    par(d, 'Gli atti di Roma anteriori all’adozione sono cartacei, ed è su questi che cadrà la '
           'maggior parte delle annotazioni per anni. La versione 1.33.0 ha aggiunto '
           '«Annotazione modificativa su atti cartacei» (ID 95), con un caso d’uso per '
           'registro e lo stesso mapping per tutti:')
    tabella(d, CARTACEI, [2.0, 4.4])
    voce(d, 'Testo libero.', 'Formula 998 e composizione libera obbligatorie; facoltativo il '
         'contrassegno di non certificabilità.')
    voce(d, 'L’atto annotato.', 'Si indica con i soli estremi del registro cartaceo — '
         'provincia, comune, numero, anno e data — in evento.eventoCollegato, non in '
         'datiRettifica: manca l’idAnsc, perché l’atto in ANSC non c’è.')
    voce(d, 'Dati facoltativi.', 'Decorrenza, motivo e descrizione del recupero, identificativo '
         'dell’atto cartaceo, contrassegno di atto secretato.')
    voce(d, 'Nessuna correzione strutturata.', 'Non c’è eventoModificato: ANSC non ha i dati '
         'dell’atto cartaceo da correggere.')
    voce(d, 'Che cosa non si sa.', 'Quale servizio li depositi, e se il Comune debba '
         'registrare in ANSC le annotazioni dei propri atti cartacei, compresa la correzione '
         'per errore materiale, oppure soltanto annotarle sul registro come oggi (AR-20).')

    h(d, 2, 'La storia nel changelog')
    tabella(d, STORIA, [1.8, 4.6])

    h(d, 2, 'Che cosa le fonti non dicono')
    for testa, corpo in [
        ('Il tipo di rettifica dell’art. 98.', 'AR-14.'),
        ('Lo stato dell’annotazione e dell’atto corretto, e dove stiano gli identificativi '
         'restituiti.', 'AR-15.'),
        ('La serie del numero comunale dell’annotazione.', 'AR-16.'),
        ('Se serva l’attestazione di conformità.', 'AR-17.'),
        ('Il testo delle formule 888 e 190.', 'AR-18.'),
        ('L’elenco dei dati correggibili con l’art. 98.', 'AR-19.'),
        ('Il servizio delle annotazioni su atto cartaceo.', 'AR-20.'),
        ('Come si firma l’annotazione con i servizi cooperativi.', 'Il changelog documenta '
         'correzioni, nessun documento descrive il passo (OP-81 di [R1]).'),
    ]:
        voce(d, testa, corpo)

    h(d, 2, 'La proposta per SIPO')
    par(d, 'Si segue lo stesso criterio dell’annullamento: prima la web app con il '
           'riallineamento in SIPO, poi la formazione da SIPO.')
    h(d, 3, 'Fase 1 — web app e riallineamento')
    voce(d, 'Dove si avvia.', 'Nel dettaglio di un atto con identificativo ANSC e stato 5, '
         '«ANNOTAZIONE PER ERRORE MATERIALE» e «ANNOTAZIONE PER RETTIFICA» aprono una pagina '
         'di indicazioni, come per la rettifica tecnica: idAnsc e numero comunale in evidenza, '
         'il percorso sulla web app, i vincoli (competenza del comune di formazione, nota '
         'tecnica preclusa dopo).')
    voce(d, 'Il numero comunale si stacca in SIPO.', 'L’annotazione ha un numero proprio: lo '
         'dà be-numeratore-comunale prima di andare sulla web app, come per un atto formato '
         'sulla web app (AR-16).')
    voce(d, 'Il riallineamento.', '«RIALLINEA DA ANSC» legge l’atto con R005 (flagRettifica '
         'per l’ultima rettifica), lo confronta con quello depositato e riporta in SIPO i dati '
         'cambiati, con lo stesso meccanismo della rettifica tecnica; registra poi '
         'l’annotazione e il suo identificativo.')
    h(d, 3, 'Fase 2 — l’annotazione formata da SIPO')
    figura(d, diagrammi_rettificative.errore_materiale(), 6.5,
           'Figura 5 — L’annotazione per errore materiale formata da SIPO.')
    voce(d, 'Una pagina sola per i cinque registri.', 'Il mapping è identico: la pagina mostra '
         'gli estremi dell’atto, precompilati, e i dati anagrafici modificabili — '
         'dell’intestatario e, nelle nascite, dei genitori — con il valore attuale accanto.')
    voce(d, 'Testo e atto corretto dalla stessa differenza.', 'SIPO compone il testo con la '
         'formula 888 («dove è scritto … deve leggersi …») e l’atto corretto partendo da quello '
         'letto con R005 e applicandovi le modifiche. È ciò che tiene coerenti i due canali.')
    voce(d, 'L’art. 95 sulla stessa pagina.', 'Si aggiungono l’ente dichiarante con gli estremi '
         'del provvedimento, la scelta fra modifica e annullamento e la formula 190. '
         'L’annullamento non chiede l’atto corretto.')
    voce(d, 'Firma e chiusura.', 'R013 attraverso il concentratore, la firma dell’ufficiale '
         'nella stessa finestra della firma dell’atto, la verifica con R005; poi SIPO aggiorna i '
         'propri dati senza riaprire l’atto e segna il numero come utilizzato.')
    par(d, 'Le operazioni del concentratore:')
    tabella(d, OPERAZIONI, [1.5, 2.0, 1.2, 1.7])
    par(d, 'Dove registrare l’annotazione: ANSC_STATO_ATTO ha per chiave l’atto di SIPO, e '
           'un’annotazione in SIPO non è un atto ma una riga del modulo delle annotazioni. Si '
           'propone una tabella propria nello schema ANSC_USR:')
    tabella(d, REGISTRO, [2.4, 4.0])
    voce(d, 'Gli atti cartacei.', 'Restano annotati sul registro come oggi. Se AR-20 stabilirà '
         'che vanno registrati anche in ANSC, la stessa pagina servirà con il caso d’uso '
         'cartaceo e il testo libero.')


def ritocchi():
    fatti = []

    def S(v, n, a, e):
        D.sostituisci(d, v, n, attese=a, etichetta=e, fatti=fatti)

    S('Le questioni ancora da decidere sono raccolte in coda, come punti aperti '
      'AR-01…AR-13, accanto agli OP-80…OP-84 dell’analisi.',
      'Un capitolo a parte tratta le annotazioni rettificative — errore materiale (art. 98) e '
      'rettifica (art. 95) — compresi gli atti cartacei. Le questioni ancora da decidere sono '
      'raccolte in coda, come punti aperti AR-01…AR-21, accanto agli OP-80…OP-84 '
      'dell’analisi.', 1, 'scopo')
    S('Tredici questioni, accanto agli OP-80…OP-84 dell’analisi [R1].',
      'Ventuno questioni, accanto agli OP-80…OP-84 dell’analisi [R1].', 1, 'punti aperti')
    S('Errore materiale (art. 98). Caso d’uso proprio (Morte_013, Dic_Nasc_119…), formula 888, '
      'testo della correzione in composizioneCompleta. Corregge i dati anagrafici; non può '
      'annullare.',
      'Errore materiale (art. 98). Caso d’uso proprio, formula 888; corregge i dati '
      'anagrafici e non può annullare. È descritto nel capitolo «' + CAP + '».', 1,
      'rinvio dall’errore materiale')
    S('Il modulo delle annotazioni di SIPO resta fuori da questo documento.',
      'Il modulo delle annotazioni di SIPO resta fuori da questo documento, salvo le '
      'annotazioni rettificative, trattate nel capitolo «' + CAP + '».', 1,
      'rinvio dalla proposta di annotazione')
    # figure successive
    S('Figura 6 — La rettifica tecnica', 'Figura 7 — La rettifica tecnica', 1, 'figura 6 → 7')
    S('Figura 5 — La cancellazione', 'Figura 6 — La cancellazione', 1, 'figura 5 → 6')

    # la tabella dei casi d'uso passa al capitolo nuovo
    intro = [p for p in d.paragraphs if p.text.startswith('I casi d’uso sono uno per '
                                                         'registro, affiancati')]
    assert len(intro) == 1
    t = D.trova_tabella(d, 'Registro', 'Annotazione per rettifica')
    t._tbl.getparent().remove(t._tbl)
    D.testo_di(intro[0], 'I casi d’uso, uno per registro e per articolo, sono elencati nel '
                         'capitolo «' + CAP + '».')
    fatti.append('tabella dei casi d’uso spostata nel capitolo nuovo')

    # glossario
    glos = D.trova_tabella(d, 'Termine', 'Significato in questo doc')
    for riga in [
        ('Annotazione per errore materiale', 'La correzione d’ufficio di un atto formato (art. '
         '98 del D.P.R. 396/2000): in ANSC un’annotazione con caso d’uso, numero e firma propri; '
         'non annulla.'),
        ('Annotazione per rettifica', 'La correzione o l’annullamento di un atto formato su '
         'provvedimento di un’altra amministrazione (art. 95).'),
        ('eventoModificato', 'In R013, l’atto intero con i dati già corretti, inviato accanto '
         'all’annotazione.'),
        ('Annotazione su atto cartaceo', 'L’annotazione registrata in ANSC su un atto che in '
         'ANSC non c’è, indicato con gli estremi del registro.'),
    ]:
        D.clona_riga(glos, riga)

    # riferimenti
    rif = D.trova_tabella(d, 'Riferimento', 'Natura')
    for riga in [
        ('[R4]', 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.1.docx — gli effetti delle '
         'annotazioni su certificati ed estratti.', 'Documento di progetto'),
        ('[A6]', 'Guida operativa ANSC, § 9.2 (pp. 55-67) e § 12.2 (p. 84); nota di processo '
         '[A2], §§ 3.1.1 e 3.2.1; esempi ansc/docs/CasiTest/payload_test/'
         'R013_inserimento_annotazione_errore_materiale.json e …_rettifica.json; '
         'CasiTest/ANSC_Piano_Test.xlsx, foglio «Elenco UC di rettifica».',
         'Documentazione ANSC'),
        ('[A7]', 'Mapping dei casi d’uso Dic_Nasc_118/119, Morte_012/013, Matr_017/018, '
         'UnCiv_007/008, Citt_047/048 e dei casi d’uso su atto cartaceo (*_998_4, '
         'Dic_Nasc_998_5); changelog_mapping.md.', 'Dati ANSC'),
    ]:
        D.clona_riga(rif, riga)

    # punti aperti
    op = D.trova_tabella(d, '#', 'Questione', 'Owner')
    for riga in APERTI:
        D.clona_riga(op, riga)
    return fatti


def intesta():
    for f in D.frontespizio(d, '0.3', NOME, DATA):
        print('  ' + f)
    D.storia(d, DATA, '0.3', 'Nuovo capitolo · Che cosa prevede ANSC · Punti aperti',
             'Nuovo capitolo sulle annotazioni rettificative: errore materiale (art. 98) e '
             'rettifica (art. 95). Strumenti a confronto, i dieci casi d’uso con il mapping '
             'sezione per sezione, il servizio R013, come si rappresenta la correzione, il flusso '
             'sulla web app e con i servizi cooperativi, gli effetti, le annotazioni su atto '
             'cartaceo, la storia nel changelog, le lacune delle fonti, la proposta per SIPO in '
             'due fasi con figura, operazioni del concentratore e registro delle annotazioni. '
             'Figure successive rinumerate. Punti aperti AR-14…AR-21.')


if __name__ == '__main__':
    ancora = heading('Dove e come inserirsi', 1)._p
    n = innesta(ancora, capitolo)
    print('capitolo nuovo: %d elementi' % n)
    for f in ritocchi():
        print('  ' + f)
    intesta()
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
