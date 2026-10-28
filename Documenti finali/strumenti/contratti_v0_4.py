# -*- coding: utf-8 -*-
"""Riallinea ansc-v1.yaml all'analisi v3.54 (SPEC_API v0.4).

La configurazione del contratto era ferma alla terna evento-operazione-casistica
(ANSC_CFG_OPERAZIONE, mappatore, colonna SIPO nella forma TABELLA.COLONNA). Dalla v3.53
dell'analisi la configurazione è per UC e per tipo atto (ANSC_CFG_UC, legata con ID_TIPO_ATTO),
i campi portano l'alias SIPO compilato a mano (ANSC_CFG_CAMPO), la baseline si nomina con il
numero (COD_VERSIONE tolto) e la supervisione è per municipio, non per ufficiale.

Ogni sostituzione dichiara quante volte deve avvenire e si ferma se il conto non torna.

    /Library/Developer/CommandLineTools/usr/bin/python3 "Documenti finali/strumenti/contratti_v0_4.py"
"""
import io
import os

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(BASE, 'ansc-v1.yaml')


def sost(t, vecchio, nuovo, attese=1):
    n = t.count(vecchio)
    if n != attese:
        raise SystemExit(f'«{vecchio[:70]}»: attese {attese}, trovate {n}')
    return t.replace(vecchio, nuovo)


def blocco(t, inizio, fine, nuovo):
    """Sostituisce il testo da `inizio` (compreso) a `fine` (escluso)."""
    a = t.index(inizio)
    b = t.index(fine, a)
    assert t.count(inizio) == 1, inizio
    return t[:a] + nuovo + t[b:]


CONFIGURAZIONE = r"""  # ------------------------------------------------------------- configurazione
  /ansc/v1/back-office/configurazione/casi-uso:
    get:
      operationId: elencaCasiUso
      summary: Elenca gli UC configurati
      description: |
        Restituisce le righe della configurazione degli UC: una per UC e per tipo atto di SIPO che lo
        raggiunge, dentro una baseline, con la priorità e la logica di scelta. Un UC del catalogo
        che nessun tipo atto raggiunge ancora compare con una riga senza tipo atto.

        Si usa dalla schermata di amministrazione della configurazione.

        **Effetti**: nessuno.
      tags: [casi-uso]
      parameters:
        - { name: idVersione, in: query, required: false, description: 'Baseline della configurazione; se omessa vale quella attiva.', schema: { type: integer, format: int64 } }
        - { name: idTipoAtto, in: query, required: false, description: 'Tipo atto di SIPO.', schema: { type: integer, format: int64 } }
        - { name: codUcAnsc, in: query, required: false, description: 'Codice dell''UC pubblicato da ANSC.', schema: { type: string } }
        - { name: codFamiglia, in: query, required: false, description: 'Famiglia di evento: nascita, morte, matrimonio…', schema: { type: string } }
        - $ref: '#/components/parameters/NumPagina'
        - $ref: '#/components/parameters/NumElementi'
      responses:
        '200':
          description: Elenco delle righe di configurazione degli UC.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati:
                        type: object
                        properties:
                          casiUso:
                            type: array
                            items: { $ref: '#/components/schemas/CasoUsoConfigurato' }
                            description: Le righe della pagina richiesta.
                          navigazione: { $ref: '#/components/schemas/Navigazione' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Sola lettura, sicura e ripetibile.

  /ansc/v1/back-office/configurazione/casi-uso/{idUcCfg}:
    parameters:
      - $ref: '#/components/parameters/IdUcCfg'
    get:
      operationId: leggiCasoUso
      summary: Legge una riga della configurazione degli UC
      description: |
        Restituisce una riga della configurazione: l'UC con i dati del catalogo di ANSC, il tipo atto
        di SIPO che lo raggiunge, la priorità, la logica di scelta, l'interrogazione associata e la
        baseline.

        **Effetti**: nessuno.
      tags: [casi-uso]
      responses:
        '200':
          description: La riga di configurazione.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati: { $ref: '#/components/schemas/CasoUsoConfigurato' }
              examples:
                esempioMorteInAbitazione:
                  value:
                    esito: OK
                    messaggi: []
                    dati:
                      idUcCfg: 1
                      codUcAnsc: '2101'
                      codMotore: Morte_001
                      descUcAnsc: Dichiarazione di morte avvenuta in abitazione
                      codFamiglia: morte
                      idTipoContenuto: '1'
                      idTipoAtto: 301
                      numPriorita: 100
                      codLogicaDiScelta: null
                      codQueryUc: null
                      idVersione: 12
                      dataInizioValidita: '2026-07-20'
                      dataFineValidita: '9999-12-31'
        '404': { $ref: '#/components/responses/NonTrovato' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Sola lettura, sicura e ripetibile.
    put:
      operationId: sostituisciCasoUso
      summary: Sostituisce una riga della configurazione degli UC
      description: |
        Sostituisce integralmente la riga indicata: tipo atto, priorità, logica di scelta e
        interrogazione. I dati del catalogo (codice, motore, descrizione, famiglia, tipo di
        contenuto, validità) sono quelli pubblicati da ANSC e non si modificano da qui.

        Si usa in fase di manutenzione della configurazione, su una baseline **in stato di bozza**.

        **Effetti**: modifica la configurazione. **La baseline attiva non è modificabile**: per
        cambiare una configurazione in esercizio si crea una nuova baseline con `creaVersione`, la
        si modifica e la si rende corrente con `attivaVersione`. Ripetibile.
      tags: [casi-uso]
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CasoUsoConfigurato' }
      responses:
        '200':
          description: Riga sostituita.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati: { $ref: '#/components/schemas/CasoUsoConfigurato' }
        '409':
          description: La baseline è attiva e non modificabile.
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Busta' }
              examples:
                esempioVersioneAttiva:
                  value:
                    esito: KO
                    messaggi:
                      - tipo: ERROR
                        codice: CONFIG_VERSIONE_ATTIVA
                        descrizione: La baseline 12 è attiva. Creare una nuova baseline per modificarla.
                    dati: null
        '404': { $ref: '#/components/responses/NonTrovato' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Modifica la configurazione. Ripetibile.
      x-codici-errore:
        - codice: CONFIG_VERSIONE_ATTIVA
          condizione: 'Tentativo di modificare la baseline in esercizio.'

  /ansc/v1/back-office/configurazione/casi-uso/{idUcCfg}/campi:
    parameters:
      - $ref: '#/components/parameters/IdUcCfg'
    get:
      operationId: elencaCampi
      summary: Elenca i campi configurati per l'UC
      description: |
        Restituisce i campi del modello evento configurati per l'UC della riga indicata, nella sua
        baseline: oggetto e campo ANSC, alias SIPO, obbligatorietà, dizionario di validazione,
        ordinamento e indicatore di invio ad ANSC.

        I campi appartengono all'UC e non alla riga: righe dello stesso UC per tipi atto diversi
        restituiscono gli stessi campi, perché la tabella li richiama per valore con il codice
        dell'UC e la baseline.

        È la configurazione che il pre-filtro applica in `verificaAtto`.

        **Effetti**: nessuno.
      tags: [casi-uso]
      responses:
        '200':
          description: I campi configurati.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati:
                        type: object
                        properties:
                          campi:
                            type: array
                            items: { $ref: '#/components/schemas/CampoConfigurato' }
                            description: I campi dell'UC, in ordine.
              examples:
                esempioCampi:
                  value:
                    esito: OK
                    messaggi: []
                    dati:
                      campi:
                        - oggettoAnsc: evento.datiDiMorte
                          campoAnsc: idComuneMorte
                          aliasCampoSipo: Comune del decesso
                          flagObbligatorio: false
                          idDecodificaAnsc: null
                          obbligatorietaEvento: null
                          numOrdinamento: 12
                          flagOperativo: true
        '404': { $ref: '#/components/responses/NonTrovato' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Sola lettura, sicura e ripetibile.
    put:
      operationId: sostituisciCampi
      summary: Sostituisce i campi configurati per l'UC
      description: |
        Sostituisce integralmente l'elenco dei campi dell'UC nella baseline della riga indicata.

        Si usa dopo una revisione della mappatura e per compilare a mano l'alias SIPO. Vale il
        medesimo vincolo di `sostituisciCasoUso`: la baseline attiva non è modificabile.

        La tabella dei campi non ha vincoli di unicità né chiavi esterne, per scelta: che uno stesso
        campo non compaia due volte per lo stesso UC e la stessa baseline lo controlla l'operazione.

        **Effetti**: modifica la configurazione. Ripetibile.
      tags: [casi-uso]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                campi:
                  type: array
                  items: { $ref: '#/components/schemas/CampoConfigurato' }
                  description: L'elenco completo dei campi che sostituisce quello esistente.
      responses:
        '200':
          description: Campi sostituiti.
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Busta' }
        '409':
          description: La baseline è attiva e non modificabile.
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Busta' }
        '404': { $ref: '#/components/responses/NonTrovato' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Modifica la configurazione. Ripetibile.

  /ansc/v1/back-office/configurazione/casi-uso/{idUcCfg}/campi/importazioni:
    parameters:
      - $ref: '#/components/parameters/IdUcCfg'
    post:
      operationId: importaCampi
      summary: Importa i campi dal mapping ufficiale dei casi d'uso ANSC
      description: |
        Popola i campi dell'UC a partire dal mapping ufficiale pubblicato da ANSC — il file che
        porta il codice motore dell'UC (per esempio Morte_001) — e dai dizionari replicati in
        locale, riducendo il lavoro manuale di prima configurazione.

        Si usa quando si adotta un nuovo UC o quando il fornitore pubblica una revisione del
        mapping.

        **Effetti**: crea o aggiorna i campi dell'UC nella baseline in bozza. Ripetibile: una
        seconda importazione dello stesso mapping non produce duplicati.

        **Che cosa non fa**: non compila l'alias SIPO, che si scrive a mano. L'importazione porta il
        lato ANSC — oggetto e campo, obbligatorietà, dizionario, ordinamento — e lascia vuoto
        l'alias.
      tags: [casi-uso]
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/ImportazioneRichiesta' }
            examples:
              esempioImportazioneMorte:
                value:
                  flagSovrascriviEsistenti: false
      responses:
        '200':
          description: Esito dell'importazione, con i conteggi.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati: { $ref: '#/components/schemas/EsitoImportazione' }
              examples:
                esempioImportata:
                  value:
                    esito: OK
                    messaggi: []
                    dati:
                      numEsaminati: 219
                      numImportati: 38
                      numInvariati: 181
                      numDaCompletare: 38
        '404': { $ref: '#/components/responses/NonTrovato' }
        '409': { $ref: '#/components/responses/VersioneAttiva' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Modifica la configurazione. Ripetibile senza duplicati.

"""

VERSIONI = r"""  /ansc/v1/back-office/configurazione/versioni:
    post:
      operationId: creaVersione
      summary: Crea una nuova baseline della configurazione in stato di bozza
      description: |
        Crea una nuova baseline della configurazione, copiando integralmente quella indicata come
        punto di partenza. La baseline nasce **in stato di bozza** ed è l'unica forma in cui la
        configurazione sia modificabile. Si nomina con il proprio numero, assegnato alla creazione.

        Si usa prima di ogni intervento sulla configurazione in esercizio.

        **Effetti**: crea una baseline. Non modifica la configurazione attiva, che resta in vigore
        finché non si esegue `attivaVersione`.
      tags: [versioni]
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/VersioneRichiesta' }
            examples:
              esempioNuovaVersione:
                value:
                  idVersioneOrigine: 12
                  codVersioneAnsc: '1.48'
                  descrizione: Recepimento della revisione del mapping dei casi d'uso di morte
      responses:
        '201':
          description: Baseline creata in stato di bozza.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati: { $ref: '#/components/schemas/Versione' }
        '404': { $ref: '#/components/responses/NonTrovato' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Crea una risorsa. Non ripetibile senza effetti.

  /ansc/v1/back-office/configurazione/versioni/{idVersione}/attivazione:
    parameters:
      - $ref: '#/components/parameters/IdVersione'
    post:
      operationId: attivaVersione
      summary: Rende corrente una baseline della configurazione
      description: |
        Rende corrente la baseline indicata: da quel momento il pre-filtro e la mappatura usano la
        sua configurazione, e la baseline diventa immodificabile. Quella prima attiva passa allo
        stato STORICA.

        Si usa a valle della revisione di una bozza, tipicamente dopo averne valutato l'effetto in
        ambiente di test.

        **Effetti**: cambia la baseline attiva. **L'attivazione non ha effetto sugli atti già
        depositati**, che conservano il modello evento con cui sono stati validati.

        Ripetibile: attivare una baseline già attiva non produce effetti ulteriori.
      tags: [versioni]
      responses:
        '200':
          description: Baseline resa corrente.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Busta'
                  - type: object
                    properties:
                      dati: { $ref: '#/components/schemas/Versione' }
              examples:
                esempioAttivata:
                  value:
                    esito: OK
                    messaggi: []
                    dati:
                      idVersione: 13
                      codStato: ATTIVA
                      codVersioneAnsc: '1.48'
                      idVersioneAnsc: '1.53.0'
                      descrizione: Recepimento della revisione del mapping dei casi d'uso di morte
                      numUcToccati: 23
                      dataAttivazione: '2026-07-25T09:00:00+02:00'
                      utenteAttivazione: VRDGPP75B02H501Z
        '404': { $ref: '#/components/responses/NonTrovato' }
        '409':
          description: La baseline contiene configurazioni incomplete e non può essere attivata.
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Busta' }
        '401': { $ref: '#/components/responses/NonAutenticato' }
        '403': { $ref: '#/components/responses/NonAutorizzato' }
        '500': { $ref: '#/components/responses/ErroreInterno' }
      x-ruoli: [AMMINISTRATORE]
      x-effetti: Cambia la baseline attiva. Ripetibile.
      x-codici-errore:
        - codice: CONFIG_VERSIONE_INCOMPLETA
          condizione: 'Uno o più UC adottati hanno campi obbligatori senza alias SIPO.'

"""

SCHEMI = r"""    CasoUsoConfigurato:
      type: object
      description: |
        Una riga di ANSC_CFG_UC: un UC del catalogo di ANSC e il tipo atto di SIPO che lo
        raggiunge, dentro una baseline. I dati del catalogo si ripetono sulle righe dello stesso UC.
      properties:
        idUcCfg: { type: integer, format: int64, description: 'Identificativo della riga di configurazione.' }
        codUcAnsc: { type: string, description: 'Codice dell''UC pubblicato da ANSC; la lunghezza non è fissa (2101, 11111000).' }
        codMotore: { type: string, description: 'Codice del mapping ufficiale dell''UC, per esempio Morte_001.' }
        descUcAnsc: { type: string, nullable: true, description: 'Denominazione dell''UC pubblicata da ANSC (decodifica ANSC_03).' }
        codFamiglia: { type: string, description: 'Famiglia di evento: nascita, morte, matrimonio…' }
        idTipoContenuto: { type: string, nullable: true, description: 'Tipo di contenuto secondo la decodifica ANSC_02.' }
        idConfTipoAtto: { type: integer, format: int64, nullable: true, description: 'Configurazione del tipo atto in SIPO (CONF_TIPO_ATTI).' }
        idTipoAtto: { type: integer, format: int64, nullable: true, description: 'Tipo atto di SIPO che raggiunge l''UC; nullo per un UC del catalogo che nessun tipo atto raggiunge ancora.' }
        codStato: { type: string, nullable: true, description: 'Stato della riga di configurazione; valori ammessi da definire nell''analisi.' }
        numPriorita: { type: integer, description: 'Ordine di valutazione fra gli UC dello stesso tipo atto: il primo la cui logica è soddisfatta determina l''UC.' }
        codLogicaDiScelta: { type: string, nullable: true, description: 'Codice libero della logica che stabilisce se l''UC si applica all''atto, valutato dal codice applicativo; nessun catalogo lo descrive. Nullo: si applica sempre.' }
        codQueryUc: { type: string, nullable: true, description: 'Interrogazione da utilizzare per l''UC, in ANSC_TEMPLATE della stessa baseline.' }
        idVersione: { type: integer, format: int64, description: 'Baseline cui la riga appartiene.' }
        dataInizioValidita: { type: string, format: date, description: 'Inizio di validità dell''UC dichiarato da ANSC.' }
        dataFineValidita: { type: string, format: date, description: 'Fine di validità dell''UC dichiarata da ANSC.' }

    CampoConfigurato:
      type: object
      description: Una riga di ANSC_CFG_CAMPO, richiamata dall'UC per valore con il codice e la baseline.
      properties:
        oggettoAnsc: { type: string, description: 'Oggetto del modello evento che contiene il campo (Binding Object del mapping), per esempio evento.datiDiMorte.' }
        campoAnsc: { type: string, description: 'Campo dentro l''oggetto (Binding Field del mapping), per esempio dataMorte.' }
        aliasCampoSipo: { type: string, nullable: true, description: 'Nome con cui il dato è noto in SIPO, compilato a mano da chi configura. Nullo finché non compilato.' }
        flagObbligatorio: { type: boolean, description: 'Indica se il campo sia obbligatorio per l''UC, come dichiarato dal mapping.' }
        idDecodificaAnsc: { type: integer, nullable: true, description: 'Dizionario ANSC con cui validare il valore; nullo se il campo non è codificato.' }
        obbligatorietaEvento: { type: string, nullable: true, description: 'Obbligatorietà nel modello evento; valori ammessi e rapporto con flagObbligatorio da stabilire nell''analisi.' }
        numOrdinamento: { type: integer, description: 'Ordine di presentazione e di elaborazione del campo.' }
        flagOperativo: { type: boolean, description: 'Indica se il campo vada inviato ad ANSC.' }

    ImportazioneRichiesta:
      type: object
      properties:
        flagSovrascriviEsistenti: { type: boolean, default: false, description: 'Indica se sovrascrivere i campi già configurati o lasciarli invariati.' }

    EsitoImportazione:
      type: object
      properties:
        numEsaminati: { type: integer, description: 'Righe esaminate nel mapping di origine.' }
        numImportati: { type: integer, description: 'Campi creati o aggiornati.' }
        numInvariati: { type: integer, description: 'Campi lasciati invariati.' }
        numDaCompletare: { type: integer, description: 'Campi importati che restano senza alias SIPO.' }

    VersioneRichiesta:
      type: object
      properties:
        idVersioneOrigine: { type: integer, format: int64, nullable: true, description: 'Baseline da copiare; se omessa si parte da quella attiva.' }
        codVersioneAnsc: { type: string, nullable: true, description: 'Revisione del mapping di ANSC che la baseline recepisce.' }
        descrizione: { type: string, nullable: true, description: 'Che cosa la baseline recepisce.' }

    Versione:
      type: object
      properties:
        idVersione: { type: integer, format: int64, description: 'Numero della baseline, con cui la si nomina.' }
        codStato: { type: string, enum: [BOZZA, ATTIVA, STORICA], description: 'Stato della baseline; una sola è ATTIVA.' }
        codVersioneAnsc: { type: string, nullable: true, description: 'Revisione del mapping da cui la baseline è derivata.' }
        idVersioneAnsc: { type: string, nullable: true, description: 'Versione del modello evento da cui la baseline è derivata.' }
        descrizione: { type: string, nullable: true, description: 'Che cosa la baseline recepisce.' }
        numUcToccati: { type: integer, description: 'Quanti UC la revisione ha modificato.' }
        dataAttivazione: { type: string, format: date-time, nullable: true, description: 'Istante in cui è diventata corrente.' }
        utenteAttivazione: { type: string, nullable: true, description: 'Chi l''ha resa corrente.' }

"""


def main():
    t = io.open(F, encoding='utf-8').read()

    # info
    t = sost(t, 'version: 1.0.0', 'version: 1.1.0')
    t = sost(t, "Documentazione di analisi: `ANALISI_Integrazione-ANSC_v2.6.docx`.",
             "Documentazione di analisi: `ANALISI_Integrazione-ANSC_v3.54.docx`.")
    t = sost(t, '  - name: operazioni\n    description: La configurazione per evento, operazione e '
                'casistica che guida mappatura e verifica.',
             '  - name: casi-uso\n    description: La configurazione degli UC per tipo atto e dei '
             'loro campi, che guida mappatura e verifica.')
    t = sost(t, '  - name: versioni\n    description: Le versioni della configurazione e la loro '
                'attivazione.',
             '  - name: versioni\n    description: Le baseline della configurazione e la loro '
             'attivazione.')

    # verificaAtto e depositaBozza: dalla terna al tipo atto
    t = sost(t, "          condizione: 'Nessuna configurazione attiva per la terna "
                "evento-operazione-casistica.'",
             "          condizione: 'Nessun UC della configurazione attiva si applica al tipo "
             "atto e ai dati dell''atto.'")
    t = sost(t, "per la terna evento-operazione-casistica.\n",
             "per il tipo atto, e la logica di scelta deve determinare un UC.\n")
    t = sost(t, """                  idAttoSipo: 88012
                  codTipoEvento: MORTE
                  codTipoOperazione: CREAZIONE
                  codCasistica: DICH_ABITAZIONE
                  codVersioneConfig: v.12
      responses:""",
             """                  idAttoSipo: 88012
                  idTipoAtto: 301
      responses:""")
    t = sost(t, """                      codEventoAnsc: Morte_001
                      numCampiVerificati: 34
                      codVersioneConfig: v.12""",
             """                      codUcAnsc: '2101'
                      numCampiVerificati: 34
                      idVersione: 12""")
    t = sost(t, """                  idAttoSipo: 88012
                  codTipoEvento: MORTE
                  codTipoOperazione: CREAZIONE
                  codCasistica: DICH_ABITAZIONE
                  codVersioneConfig: v.12
                  idOperazioneComune: MORTE-88012-CREAZIONE""",
             """                  idAttoSipo: 88012
                  idTipoAtto: 301
                  idOperazioneComune: MORTE-88012-CREAZIONE""")
    t = sost(t, "                      codEventoAnsc: Morte_001\n                      dataDeposito",
             "                      codUcAnsc: '2101'\n                      dataDeposito")
    t = sost(t, """                      codTipoEvento: MORTE
                      codTipoOperazione: CREAZIONE
                      soggetto:""",
             """                      codTipoEvento: MORTE
                      codUcAnsc: '2101'
                      soggetto:""")

    # supervisione per municipio, non per ufficiale
    t = sost(t, "        - { name: operatore, in: query, required: false, description: 'Ufficiale "
                "cui l''atto è instradato.', schema: { type: string } }\n", '')
    t = sost(t, "        - { name: operatore, in: query, required: false, description: 'Ufficiale "
                "competente.', schema: { type: string } }\n", '')
    t = sost(t, "Restituisce gli atti con stato ANSC registrato, filtrabili per stato reale, "
                "ufficiale,\n        municipio,",
             "Restituisce gli atti con stato ANSC registrato, filtrabili per stato reale,\n"
             "        municipio,")
    t = sost(t, """                          operatore: VRDGPP75B02H501Z
                          idMunicipio: '01'""",
             """                          idMunicipio: '01'""")
    t = sost(t, "        Registra sull'atto un'azione non dispositiva del back-office: instradarlo "
                "a un altro\n        ufficiale, annotarlo, marcarlo come preso in carico.",
             "        Registra sull'atto un'azione non dispositiva del back-office: instradarlo "
             "a un altro\n        municipio, annotarlo, marcarlo come preso in carico.")
    t = sost(t, """                summary: Instradamento a un altro ufficiale
                value:
                  codTipoAzione: INSTRADA
                  operatoreDestinatario: BNCLRA82C41H501K
                  note: Competenza del Municipio I""",
             """                summary: Instradamento a un altro municipio
                value:
                  codTipoAzione: INSTRADA
                  idMunicipioDestinatario: '01'
                  note: Competenza del Municipio I""")
    t = sost(t, "        operatoreDestinatario: { type: string, nullable: true, description: "
                "'Ufficiale cui instradare l''atto; obbligatorio per `INSTRADA`.' }",
             "        idMunicipioDestinatario: { type: string, nullable: true, description: "
             "'Municipio cui instradare l''atto; obbligatorio per `INSTRADA`.' }")
    t = sost(t, "        operatore: { type: string, nullable: true, description: 'Ufficiale "
                "competente.' }\n", '', attese=2)

    # schemi dell'atto
    t = sost(t, """      required: [idAttoSipo, codTipoEvento, codTipoOperazione, codCasistica]
      properties:
        idAttoSipo: { type: integer, format: int64, description: 'Identificativo dell''atto in SIPO, da cui si rileggono i dati.' }
        codTipoEvento: { type: string, description: 'Tipo di evento di stato civile, per esempio MORTE.' }
        codTipoOperazione: { type: string, description: 'Operazione richiesta, per esempio CREAZIONE.' }
        codCasistica: { type: string, description: 'Casistica che distingue le varianti dell''evento, per esempio DICH_ABITAZIONE.' }
        codVersioneConfig:
          type: string
          nullable: true
          description: Versione di configurazione da applicare. Se omesso vale quella attiva.""",
             """      required: [idAttoSipo, idTipoAtto]
      properties:
        idAttoSipo: { type: integer, format: int64, description: 'Identificativo dell''atto in SIPO, da cui si rileggono i dati.' }
        idTipoAtto: { type: integer, format: int64, description: 'Tipo atto di SIPO, da cui la configurazione determina l''UC; per esempio 301, morte in abitazione a Roma.' }
        idVersione:
          type: integer
          format: int64
          nullable: true
          description: Baseline della configurazione da applicare. Se omessa vale quella attiva.""")
    t = sost(t, """        codEventoAnsc: { type: string, description: 'Evento ANSC individuato dalla configurazione.' }
        numCampiVerificati: { type: integer, description: 'Numero di campi sottoposti a controllo.' }
        codVersioneConfig: { type: string, description: 'Versione di configurazione effettivamente applicata.' }""",
             """        codUcAnsc: { type: string, description: 'UC determinato dalla configurazione.' }
        numCampiVerificati: { type: integer, description: 'Numero di campi sottoposti a controllo.' }
        idVersione: { type: integer, format: int64, description: 'Baseline effettivamente applicata.' }""")
    t = sost(t, """      required: [idAttoSipo, codTipoEvento, codTipoOperazione, codCasistica, operatore, idPostazione]
      properties:
        idAttoSipo: { type: integer, format: int64, description: 'Atto SIPO da depositare; i dati sono riletti alla chiamata.' }
        codTipoEvento: { type: string, description: 'Tipo di evento di stato civile.' }
        codTipoOperazione: { type: string, description: 'Operazione richiesta.' }
        codCasistica: { type: string, description: 'Casistica dell''evento.' }
        codVersioneConfig: { type: string, nullable: true, description: 'Versione di configurazione; se omesso vale quella attiva.' }""",
             """      required: [idAttoSipo, idTipoAtto, operatore, idPostazione]
      properties:
        idAttoSipo: { type: integer, format: int64, description: 'Atto SIPO da depositare; i dati sono riletti alla chiamata.' }
        idTipoAtto: { type: integer, format: int64, description: 'Tipo atto di SIPO. Il deposito applica sempre la baseline attiva, che l''atto non registra.' }""")
    t = sost(t, "        codEventoAnsc: { type: string, description: 'Evento ANSC con cui l''atto è "
                "stato depositato.' }",
             "        codUcAnsc: { type: string, description: 'UC con cui l''atto è stato "
             "depositato.' }")
    t = sost(t, """        codTipoEvento: { type: string, description: 'Tipo di evento di stato civile.' }
        codTipoOperazione: { type: string, description: 'Operazione.' }
        stato: { $ref: '#/components/schemas/StatoAnsc' }""",
             """        codTipoEvento: { type: string, description: 'Tipo di evento di stato civile.' }
        codUcAnsc: { type: string, nullable: true, description: 'UC determinato, se già determinato.' }
        numeroAtto: { type: string, nullable: true, description: 'Numero comunale dell''atto, se già staccato.' }
        stato: { $ref: '#/components/schemas/StatoAnsc' }""")
    t = sost(t, """        codTipoEvento: { type: string, description: 'Tipo di evento.' }
        codTipoOperazione: { type: string, description: 'Operazione.' }
        soggetto:""",
             """        codTipoEvento: { type: string, description: 'Tipo di evento.' }
        codUcAnsc: { type: string, nullable: true, description: 'UC determinato.' }
        soggetto:""")
    t = sost(t, "        codVersioneConfigAttiva: { type: string, description: 'Versione di "
                "configurazione corrente.' }",
             "        idVersioneAttiva: { type: integer, format: int64, description: 'Baseline "
             "della configurazione corrente.' }")
    t = sost(t, "Stato del componente, connettività verso ANSC, versione di configurazione attiva.",
             "Stato del componente, connettività verso ANSC, baseline della configurazione attiva.")
    t = sost(t, "        versione di configurazione attiva e le metriche di dominio.",
             "        baseline della configurazione attiva e le metriche di dominio.")

    # parametri di percorso
    t = sost(t, """    IdOperazione:
      name: idOperazione
      in: path
      required: true
      description: Identificativo dell'operazione configurata.
      schema: { type: integer, format: int64 }
      example: 1
    CodVersione:
      name: codVersione
      in: path
      required: true
      description: Codice della versione di configurazione.
      schema: { type: string }
      example: v.13""",
             """    IdUcCfg:
      name: idUcCfg
      in: path
      required: true
      description: Identificativo della riga di configurazione dell'UC.
      schema: { type: integer, format: int64 }
      example: 1
    IdVersione:
      name: idVersione
      in: path
      required: true
      description: Numero della baseline della configurazione.
      schema: { type: integer, format: int64 }
      example: 13""")
    t = sost(t, "      description: La versione di configurazione è attiva e non modificabile.",
             "      description: La baseline della configurazione è attiva e non modificabile.", attese=3)

    # blocchi riscritti
    t = blocco(t, '  # ------------------------------------------------------------- configurazione\n',
               '  /ansc/v1/back-office/configurazione/versioni:\n', CONFIGURAZIONE)
    t = blocco(t, '  /ansc/v1/back-office/configurazione/versioni:\n',
               '  # --------------------------------------------------------------------- audit\n',
               VERSIONI)
    t = blocco(t, '    OperazioneConfigurata:\n', '    RegistrazioneAuditSintesi:\n', SCHEMI)

    for residuo in ('codCasistica', 'codTipoOperazione', 'idMapper', 'codEventoAnsc',
                    'codVersione:', 'codVersioneConfig', 'IdOperazione', 'campoSipo',
                    'operatoreDestinatario', "Ufficiale competente"):
        if residuo in t:
            raise SystemExit('residuo: ' + residuo)
    yaml.safe_load(t)
    io.open(F, 'w', encoding='utf-8').write(t)
    print('scritto:', F)


if __name__ == '__main__':
    main()
