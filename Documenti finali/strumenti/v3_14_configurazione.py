# -*- coding: utf-8 -*-
"""v3.14 — la configurazione diventa un dato del Comune: l'UC al centro, la query come condizione.

Che cosa cambia rispetto alla v3.13, e perché.

⚠️ **L'UC sostituisce il Modello come oggetto centrale della configurazione.** Finora la
tabella portante era `ANSC_CFG_OPERAZIONE`, una riga per Modello di atto, con una colonna
`COD_UC_ANSC` valorizzata «solo quando la corrispondenza è univoca». Erano due luoghi in cui
l'UC poteva essere dichiarato — la colonna e le regole — senza una precedenza scritta. Il
funzionario però configura ragionando per caso d'uso: la riga diventa una per UC.

⚠️ **Le regole di determinazione diventano query sul database di SIPO.** Deciso con l'utente:
SIPO salva l'atto sul proprio database prima di depositarlo in ANSC, quindi i dati su cui
decidere sono già lì. Non è una scelta di comodo: è ciò che consente di scegliere l'UC
guardando l'atto reale invece di una condizione astratta. Sostituisce la forma dichiarativa
`campo/operatore/valore` di PC-9 (v3.0).

⚠️ **La precompilazione non è più la fonte: è un suggerimento.** La configurazione la
scrivono i funzionari; l'importazione dal mapping ufficiale prepara le righe in stato
«proposto». Da qui la colonna `COD_ORIGINE`, che è ciò che impedisce a una reimportazione di
cancellare il giudizio umano: si riscrivono solo le righe che nessuno ha ancora guardato.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

# --------------------------------------------------------------- ANSC_CFG_UC
CFG_UC = [
    ('ID_UC_CFG', 'NUMBER (PK)', 'Chiave tecnica.'),
    ('COD_UC_ANSC', 'VARCHAR2(20)',
     'Codice dell’UC pubblicato da ANSC (es. 11111000). Riferimento per valore al catalogo '
     'ANSC_ANA_UC: si nomina il codice nazionale, non la riga locale, così la configurazione '
     'può nominare un UC prima che il catalogo sia ricaricato.'),
    ('COD_TIPO_EVENTO', 'VARCHAR2(20)', 'MORTE, NASCITA, …'),
    ('COD_TIPO_OPERAZIONE', 'VARCHAR2(20)', 'CREAZIONE, TRASCRIZIONE, …'),
    ('ID_MODELLO_ATTO', 'VARCHAR2(5)',
     'Modello di atto del Comune (CONF_TIPO_ATTI.ID_MODELLO_ATTO). ⚠️ Non è più la chiave '
     'della riga: più UC condividono lo stesso Modello, ed è la ragione per cui la riga è '
     'per UC e non per Modello.'),
    ('ID_CONF_TIPO_ATTO', 'NUMBER',
     'Tipo atto SIPO da cui discendono Modello e maschera (CONF_TIPO_ATTI).'),
    ('MASCHERA_UI', 'VARCHAR2(100)',
     'Maschera di immissione corrispondente. Riportata per leggibilità: la sorgente '
     'autoritativa resta CONF_TIPO_ATTI.'),
    ('NUM_PRIORITA', 'NUMBER',
     'Ordine di valutazione fra gli UC che condividono il Modello. Il primo la cui condizione '
     'è soddisfatta determina l’UC; l’ordine esplicito sostituisce la mutua esclusione '
     'dimostrata, che una condizione in forma di query non consente di verificare.'),
    ('SERVIZIO_ANSC', 'VARCHAR2(20)',
     'Interfaccia ANSC dell’operazione (es. R009 per la validazione e il deposito).'),
    ('ID_TIPO_DOCUMENTO', 'VARCHAR2(20)', 'Tipo di documento del canale DMNM/TS (R022/R023).'),
    ('ID_MAPPER', 'VARCHAR2(40)',
     'Strategia di mapping SIPO → ANSC selezionata dal concentratore.'),
    ('FLG_TRASCRIZIONE', 'CHAR(1)', 'S/N: valorizza i dati dell’atto di provenienza.'),
    ('FLG_FIRMA', 'CHAR(1)',
     'S/N, default «S»: nessun atto è formato senza la firma dell’ufficiale.'),
    ('FLG_ATTIVO', 'CHAR(1)',
     'S/N. Un UC può essere censito e non ancora configurato compiutamente: il flag distingue '
     'ciò che è in esercizio da ciò che è in preparazione, e permette di partire dagli UC più '
     'frequenti senza che gli altri interferiscano.'),
    ('ID_VERSIONE', 'NUMBER (FK)', 'Baseline di appartenenza (ANSC_CFG_VERSIONE).'),
    ('DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA', 'DATE', 'Validità temporale.'),
    ('DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici previsti dallo standard di nomenclatura [R5].'),
]

# ------------------------------------------------- ANSC_CFG_UC_CONDIZIONE
CFG_UC_COND = [
    ('ID_CONDIZIONE', 'NUMBER (PK)', 'Chiave tecnica.'),
    ('ID_UC_CFG', 'NUMBER (FK)', 'UC configurato a cui la condizione appartiene.'),
    ('TXT_QUERY', 'CLOB',
     'Interrogazione sul database di SIPO che stabilisce se l’UC si applica all’atto in '
     'lavorazione. Riceve l’identificativo dell’atto come parametro di associazione e '
     'restituisce una riga quando la condizione è soddisfatta. ⚠️ È eseguita in sola lettura, '
     'con un’utenza che non possiede privilegi di scrittura sugli schemi di SIPO.'),
    ('DESCRIZIONE', 'VARCHAR2(400)',
     'Che cosa la condizione riconosce, in lingua corrente. Obbligatoria: è l’unica parte '
     'della condizione che un funzionario può rileggere senza saper leggere SQL.'),
    ('NUM_ORDINE', 'NUMBER',
     'Ordine di valutazione fra le condizioni dello stesso UC; sono in congiunzione.'),
    ('COD_ORIGINE', 'VARCHAR2(20)',
     'PROPOSTA, CONFERMATA, MODIFICATA, INSERITA (cfr. il paragrafo sulla precompilazione).'),
    ('DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici previsti dallo standard di nomenclatura [R5].'),
]

ORIGINE = ('COD_ORIGINE', 'VARCHAR2(20)',
           'Provenienza del valore: PROPOSTO (dalla precompilazione, non ancora esaminato), '
           'CONFERMATO (l’operatore l’ha validato), MODIFICATO (l’operatore ha cambiato il '
           'valore proposto), INSERITO (non veniva da alcuna precompilazione). ⚠️ Governa la '
           'reimportazione: si riscrivono le sole righe PROPOSTO.')


def riscrivi_tabella(t, righe):
    """⚠️ Distrugge i commenti ancorati alle celle: usare `riscrivi_sicura` sui documenti
    che ne contengono. Resta per i casi in cui la tabella è certamente senza ancore."""
    """Riscrive una tabella «Colonna | Tipo | Note» conservandone la formattazione.

    Le righe in eccesso si svuotano e si eliminano; quelle mancanti si clonano dall'ultima,
    che è il modo in cui `clona_riga` eredita bordi, font e larghezze.
    """
    while len(t.rows) - 1 < len(righe):
        D.clona_riga(t, [c.text for c in t.rows[-1].cells])
    for i, valori in enumerate(righe, start=1):
        for j, v in enumerate(valori):
            cella = t.rows[i].cells[j]
            if cella.paragraphs and cella.paragraphs[0].runs:
                D.testo_di(cella.paragraphs[0], v)
                for p in cella.paragraphs[1:]:
                    p._p.getparent().remove(p._p)
            else:
                cella.text = v
    for i in range(len(t.rows) - 1, len(righe), -1):
        t._tbl.remove(t.rows[i]._tr)


MONDI = [
    ('Il primo insieme descrive il lato del Comune: ANSC_CFG_UC dichiara, per ciascun caso '
     'd’uso che il Comune adotta, il Modello di atto a cui si applica con il suo tipo atto e '
     'la sua maschera, l’interfaccia ANSC da chiamare e la strategia di mappatura. È una riga '
     'per UC, e non più una per Modello: allo stesso Modello corrispondono più UC, e il '
     'funzionario che configura ragiona per caso d’uso.'),
    ('Il secondo descrive il lato di ANSC: ANSC_ANA_UC è il catalogo degli UC, con il codice, '
     'il codice motore e la descrizione pubblicati dal sistema nazionale; ANSC_CFG_CAMPO ne '
     'dichiara i campi con la loro obbligatorietà, ANSC_CFG_ALLEGATO i documenti richiesti. '
     'Il catalogo si replica da ANSC; le altre due le decide il Comune, con l’aiuto della '
     'precompilazione descritta più avanti.'),
    ('Il terzo è il ponte, e in questa versione cambia forma: le condizioni di applicabilità '
     'dell’UC (ANSC_CFG_UC_CONDIZIONE) sono interrogazioni sul database di SIPO. Non è una '
     'scelta di comodo. SIPO registra l’atto sulle proprie tabelle prima di depositarlo in '
     'ANSC: quando si deve stabilire quale caso d’uso si stia formando, il dato è già scritto, '
     'e interrogarlo direttamente è più fedele che riprodurne una copia in condizioni '
     'astratte. È anche ciò che permette di decidere in base a informazioni che SIPO possiede '
     'e ANSC no — l’esempio dell’utente è la scelta dei documenti da allegare, che in SIPO '
     'non è governata e in ANSC dipende dall’UC.'),
]

PRECOMPILAZIONE = [
    ('La configurazione la scrivono i funzionari del Comune. Il mapping ufficiale di ANSC non '
     'è la fonte della configurazione ma il suo punto di partenza: l’importazione prepara le '
     'righe, l’operatore le esamina e decide. È una correzione di rotta rispetto alle versioni '
     'precedenti, che descrivevano l’importazione come «il meccanismo principale di '
     'popolamento»; la ragione è che il mapping dichiara ciò che ANSC accetta, non ciò che il '
     'Comune vuole registrare, e le due cose non coincidono sempre.'),
    ('Perché la precompilazione resti un aiuto e non diventi un padrone, ogni riga di '
     'ANSC_CFG_CAMPO e di ANSC_CFG_ALLEGATO dichiara da dove viene il proprio valore.'),
]

ORIGINI = [
    ('Proposto', 'La riga viene dall’importazione e nessuno l’ha ancora esaminata. È il '
                 'materiale di lavoro: il back-office la presenta per prima.'),
    ('Confermato', 'L’operatore l’ha esaminata e validata così com’era.'),
    ('Modificato', 'L’operatore ha cambiato il valore proposto. La differenza rispetto alla '
                   'proposta resta visibile: è la traccia di una decisione.'),
    ('Inserito', 'La riga non veniva da alcuna precompilazione: l’ha scritta l’operatore.'),
]

REGOLA_REIMPORTAZIONE = (
    'Da qui la regola che governa ogni reimportazione successiva: si riscrivono le sole righe '
    'in stato «proposto». Per le altre l’importazione produce un elenco di scostamenti — che '
    'cosa ANSC dichiara ora, che cosa il Comune aveva deciso — e non scrive nulla. Senza '
    'questa distinzione la prima revisione del mapping cancellerebbe mesi di lavoro, ed è il '
    'rischio che le versioni precedenti affrontavano con una procedura anziché con una '
    'struttura.')


def prosa(doc):
    """La prosa che accompagna le tabelle: i tre mondi, la precompilazione, il flusso d'uso."""
    fatti = []
    D.sostituisci(doc, 'ANSC_CFG_OPERAZIONE \u2014 anagrafica delle operazioni supportate.',
                  'ANSC_CFG_UC \u2014 i casi d\u2019uso configurati dal Comune.',
                  attese=1, etichetta='titolo della tabella', fatti=fatti)

    # i tre mondi: si riscrivono i tre paragrafi esistenti, uno per uno
    ancore = ['Il primo insieme descrive il lato del Comune',
              'Il secondo descrive il lato di ANSC',
              'Il terzo \u00e8 il ponte']
    for ancora, testo in zip(ancore, MONDI):
        trovato = next((p for p in doc.paragraphs if p.text.strip().startswith(ancora)), None)
        assert trovato is not None, f'paragrafo non trovato: {ancora}'
        D.testo_di(trovato, testo)
    fatti.append('tre mondi della configurazione riscritti')

    # la precompilazione, subito prima di «Modalità operativa»
    mod = next(p for p in doc.paragraphs if p.text.strip().startswith('Modalit\u00e0 operativa'))
    prima = mod._p
    D.para(doc, prima, 'La precompilazione e il governo del dato', stile='Heading 3')
    for t in PRECOMPILAZIONE:
        D.para(doc, prima, t)
    for testa, corpo in ORIGINI:
        D.voce(doc, prima, testa, corpo)
    D.para(doc, prima, REGOLA_REIMPORTAZIONE)
    fatti.append('nuovo paragrafo «La precompilazione e il governo del dato»')
    return fatti


def applica(doc):
    fatti = []
    fatti += prosa(doc)

    # ---------------------------------------------------------- ANSC_CFG_UC
    t = D.tabella_colonne(doc, 'ID_OPERAZIONE')
    assert t is not None, 'tabella ANSC_CFG_OPERAZIONE non trovata'
    riscrivi_tabella(t, CFG_UC)
    fatti.append(f'ANSC_CFG_UC: {len(CFG_UC)} colonne')

    # ------------------------------------------- ANSC_CFG_UC_CONDIZIONE (nuova)
    ancora = next(p for p in doc.paragraphs
                  if p.text.strip().startswith('ANSC_CFG_CAMPO \u2014'))
    D.para(doc, ancora._p,
           'ANSC_CFG_UC_CONDIZIONE \u2014 quando l\u2019UC si applica.')
    D.tabella(doc, ancora._p,
              [['Colonna', 'Tipo', 'Note']] + [list(r) for r in CFG_UC_COND], modello=t)
    D.para(doc, ancora._p,
           'Le condizioni di uno stesso UC sono in congiunzione: l\u2019UC si applica se tutte '
           'sono soddisfatte. La disgiunzione si ottiene con una seconda condizione scritta '
           'nella query stessa, che \u00e8 il prezzo della forma scelta \u2014 e la ragione per cui '
           'la descrizione in lingua corrente \u00e8 obbligatoria.')
    fatti.append(f'ANSC_CFG_UC_CONDIZIONE: {len(CFG_UC_COND)} colonne')

    # ------------------------------------------------- ANSC_CFG_CAMPO: origine
    tc = D.tabella_colonne(doc, 'ID_CAMPO')
    assert tc is not None, 'tabella ANSC_CFG_CAMPO non trovata'
    esistenti = [r.cells[0].text.strip() for r in tc.rows]
    if 'COD_ORIGINE' not in esistenti:
        # si inserisce prima dei campi tecnici, che restano in coda
        valori = [[c.text for c in r.cells] for r in tc.rows[1:]]
        tecnici = [v for v in valori if v[0].startswith('DATA_INS')]
        altri = [v for v in valori if not v[0].startswith('DATA_INS')]
        riscrivi_tabella(tc, altri + [list(ORIGINE)] + tecnici)
        fatti.append('ANSC_CFG_CAMPO: aggiunta COD_ORIGINE')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato:', os.path.basename(DOC))
