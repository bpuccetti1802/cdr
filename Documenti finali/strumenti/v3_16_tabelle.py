# -*- coding: utf-8 -*-
"""v3.16 — le tabelle della configurazione semplificata: nomi validi, tipi validi, un modello solo.

⚠️ Il documento conteneva DUE modelli dati incompatibili: il corpo con la configurazione
semplificata (cinque tabelle, condizione fusa nell'UC) e l'Appendice A ferma alla v3.14
(sedici tabelle, con `ANSC_CFG_UC_CONDIZIONE`, `ANSC_CFG_REGOLA` e le sue condizioni). Il DDL
avrebbe realizzato il disegno che il corpo ha superato.

⚠️ E i nomi non erano scrivibili in Oracle: `Binding Object` e `Binding Field` con lo spazio,
`DESC_CONDIZIONE_OBBLIGATORIETA_ ANSC` con uno spazio dentro, `FLG_OBBLIGATORIO (binding
field)` con le parentesi; i tipi `VARCHAR (1000)` invece di VARCHAR2, `NUMBER(100)` oltre il
massimo consentito (38), `NUMBER ()` privo di argomento.

Scelta di nomenclatura: il lato ANSC si nomina come il lato SIPO, per simmetria —
`OGGETTO_ANSC`/`CAMPO_ANSC` accanto a `TABELLA_SIPO`/`CAMPO_SIPO`. Restano senza prefisso di
ruolo come le altre colonne di questa famiglia (OP-35 raccoglie la rinomina complessiva, che
va fatta in un solo intervento e non a pezzi).

⚠️ I 21 commenti dell'autore vanno preservati: si usa `riscrivi_sicura`, che non elimina mai
una riga commentata.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.16.docx')

SCRIPT = ('⚠️ Il contenuto è codice eseguibile in forma di script. Il linguaggio non è '
          'fissato dal presente documento — PL/SQL, SpEL, JavaScript sono tutte forme '
          'praticabili — perché la scelta compete al Comune e ha conseguenze diverse su chi '
          'esegue: un linguaggio del database riporta la logica nel database, un linguaggio di '
          'espressioni richiede un valutatore nel concentratore. ')

CFG_CAMPO = [
    ['ID_CAMPO', 'NUMBER (PK)', 'Chiave tecnica.'],
    ['ID_UC', 'NUMBER (FK)',
     'UC di riferimento nel catalogo ANSC_ANA_UC. L’obbligatorietà è dichiarata per UC: gli UC '
     'di uno stesso Modello di atto hanno insiemi di campi obbligatori diversi.'],
    ['ID_VERSIONE', 'NUMBER (FK)',
     'Baseline di appartenenza (ANSC_CFG_VERSIONE): entra nella chiave di unicità ed è ciò che '
     'fa coesistere più versioni della stessa configurazione.'],
    ['SEZIONE_FE_ANSC', 'VARCHAR2(200)',
     'Area della web app di ANSC in cui il campo è richiesto. ⚠️ Non è decorazione: è il '
     'livello a cui la condizione di obbligatorietà si applica quasi sempre — su 4.437 gruppi '
     'UC × sezione il 95,4 % ha una sola condizione, valida per l’intera sezione.'],
    ['DESC_COND_OBBLIGATORIETA', 'VARCHAR2(1000)',
     'Che cosa la condizione di obbligatorietà stabilisce, in lingua corrente. È la parte '
     'leggibile da chi non sa leggere lo script.'],
    ['REGOLA_COND_OBBLIGATORIETA', 'VARCHAR2(1000)',
     SCRIPT + 'Qui lo script stabilisce se il campo sia obbligatorio.'],
    ['OGGETTO_ANSC', 'VARCHAR2(1000)',
     'Oggetto del modello evento che contiene il campo (Binding Object del mapping ufficiale), '
     'es. evento.datiDiMorte.'],
    ['CAMPO_ANSC', 'VARCHAR2(120)',
     'Campo dentro l’oggetto (Binding Field del mapping), es. dataMorte. ⚠️ Oggetto e campo si '
     'tengono distinti perché il mapping li pubblica distinti: ricomporli in un percorso unico '
     'obbligherebbe a spezzarli a ogni confronto con la fonte.'],
    ['FLG_OBBLIGATORIO', 'CHAR(1)',
     'S/N: se il campo sia obbligatorio, come dichiarato dal mapping. ⚠️ È l’obbligatorietà del '
     'campo, non della sezione che lo contiene.'],
    ['TABELLA_SIPO', 'VARCHAR2(200)', 'Tabella di SIPO da cui il valore si prende.'],
    ['CAMPO_SIPO', 'VARCHAR2(120)', 'Colonna di SIPO da cui il valore si prende.'],
    ['ID_DECODIFICA_ANSC', 'NUMBER',
     'Dizionario ANSC con cui validare il valore, quando il campo è codificato. Il raccordo al '
     'catalogo è per valore e senza chiave esterna, per non riunificare i domini di guasto '
     'della parte operativa e della parte dizionari.'],
    ['DESCRIZIONE_BUSINESS_LOGIC', 'VARCHAR2(1000)',
     'Come si ricava il valore quando non è un trasferimento diretto: estrazione da una data o '
     'da un nodo XML, ricerca di una descrizione in una tabella di decodifica, valore fisso. '
     'In lingua corrente.'],
    ['BUSINESS_LOGIC', 'VARCHAR2(1000)', SCRIPT + 'Qui lo script produce il valore.'],
    ['ORDINAMENTO', 'NUMBER', 'Ordine di presentazione e di elaborazione dei campi (1..N).'],
    ['VALORE_DEFAULT', 'VARCHAR2(1000)',
     'Valore da usare quando la sorgente SIPO non lo fornisce.'],
    ['MESSAGGIO', 'VARCHAR2(200)', 'Messaggio mostrato all’operatore in caso di mancanza.'],
    ['NOTE', 'VARCHAR2(1000)', 'Testo libero a disposizione di chi configura.'],
    ['DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici di audit previsti dallo standard di nomenclatura [R5].'],
]

CFG_UC = [
    ['ID_UC_CFG', 'NUMBER (PK)', 'Chiave tecnica.'],
    ['COD_UC_ANSC', 'VARCHAR2(20)',
     'Codice numerico dell’UC pubblicato da ANSC. ⚠️ La lunghezza non è fissa: 11111000 per la '
     'dichiarazione di nascita, 2101 per la morte in abitazione — nel catalogo compaiono codici '
     'di quattro, cinque, sei e otto cifre. La notazione puntata (2.1.0.1) usata in altri '
     'documenti è redazionale e non va scritta qui.'],
    ['COD_TIPO_EVENTO', 'VARCHAR2(20)', 'MORTE, NASCITA, …'],
    ['COD_TIPO_OPERAZIONE', 'VARCHAR2(20)', 'CREAZIONE, TRASCRIZIONE, …'],
    ['ID_MODELLO_ATTO', 'VARCHAR2(5)',
     'Modello di atto del Comune (CONF_TIPO_ATTI.ID_MODELLO_ATTO). ⚠️ Non è la chiave della '
     'riga: più UC condividono lo stesso Modello, ed è la ragione per cui la riga è per UC.'],
    ['ID_CONF_TIPO_ATTO', 'NUMBER',
     'Tipo atto SIPO da cui discendono Modello e maschera (CONF_TIPO_ATTI).'],
    ['MASCHERA_UI', 'VARCHAR2(100)',
     'Maschera di immissione corrispondente. Riportata per leggibilità: la sorgente '
     'autoritativa resta CONF_TIPO_ATTI.'],
    ['NUM_PRIORITA', 'NUMBER',
     'Ordine di valutazione fra gli UC che condividono il Modello: il primo la cui regola di '
     'scelta è soddisfatta determina l’UC.'],
    ['REGOLA_DI_SCELTA', 'VARCHAR2(2000)',
     SCRIPT + 'Qui lo script stabilisce se l’UC è quello giusto per l’atto in lavorazione, '
     'osservando i dati che SIPO ha già registrato. ⚠️ Una sola colonna esprime ogni '
     'distinzione necessaria: non esistono altri discriminanti nella configurazione.'],
    ['ID_VERSIONE', 'NUMBER (FK)', 'Baseline di appartenenza (ANSC_CFG_VERSIONE).'],
    ['DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA', 'DATE', 'Validità temporale.'],
    ['DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici previsti dallo standard di nomenclatura [R5].'],
]


def applica(doc):
    fatti = []
    tc = D.tabella_colonne(doc, 'ID_CAMPO')
    D.riscrivi_sicura(tc, CFG_CAMPO)
    fatti.append(f'ANSC_CFG_CAMPO: {len(CFG_CAMPO)} colonne, nomi e tipi validi, + ID_VERSIONE')

    tu = D.tabella_colonne(doc, 'ID_UC_CFG')
    D.riscrivi_sicura(tu, CFG_UC)
    fatti.append(f'ANSC_CFG_UC: {len(CFG_UC)} colonne, + ID_VERSIONE')

    # la parentesi vuota rimasta nel catalogo
    D.sostituisci(doc, 'Tipo di documento del canale DMNM/TS (R022/R023). (da )',
                  'Tipo di documento del canale DMNM/TS (R022/R023).',
                  attese=1, etichetta='catalogo UC: nota incompleta', fatti=fatti)
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
