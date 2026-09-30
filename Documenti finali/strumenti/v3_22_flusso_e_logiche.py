# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.21 -> v3.22 (24/09/2026).

Recepisce il modello di configurazione della sorgente `Integrazione_SIPO_ANSC.xlsx` e il
flusso descritto in `Identificazione_UC_Costruzione_Payload_1.1.docx`:

  1. CATALOGO DELLE LOGICHE — due tabelle nuove, TIPO_DOMINIO e VALORI_DOMINIO: le logiche
     si scrivono una volta e si citano per codice, invece di ripetersi dentro ogni riga.
     ⚠️ NON sono i dizionari ANSC (DOMINIO_DECODIFICA/VALORE_DOMINIO): stesso vocabolario,
     altro contenuto, numerazione separata.
  2. LE SEZIONI DIVENTANO UN LIVELLO — ANSC_CFG_SEZIONE: la condizione di attivazione di un
     blocco del modello evento si scrive una volta per sezione, non su ciascuno dei suoi campi.
  3. L'UC DETERMINATO SI SCRIVE SULL'ATTO — ANSC_STATO_ATTO porta COD_UC_ANSC e COD_LOGICA;
     ANSC_XREF non conserva più nulla di proprio e si elimina (chiude OP-25).
  4. IL FLUSSO OPERATIVO con, per ogni passo, che cosa legge, che cosa scrive e la traccia
     che lascia in ANSC_LOG_AUDIT.
  5. PUNTO DI ATTENZIONE sui documenti e sulla loro firma, lato front-end e lato back-end.

Si MODIFICA il file reale della v3.21 (26 commenti di Word da preservare), mai rigenerare.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_22_flusso_e_logiche.py
"""
import os
import shutil
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.21.docx')
DST = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.22.docx')
IMG = os.path.join(BASE, 'strumenti', 'img')

if os.path.exists(DST):
    os.remove(DST)          # lo script riparte sempre dalla v3.21: è la sua unica sorgente
shutil.copy(SRC, DST)
doc = docx.Document(DST)
fatti = []


# ────────────────────────────────────────────────────────────── utilità locali
def par(inizio, stile=None):
    t = [p for p in doc.paragraphs
         if p.text.strip().startswith(inizio) and (stile is None or p.style.name == stile)]
    if len(t) != 1:
        raise SystemExit(f'attesa 1 occorrenza di «{inizio[:60]}», trovate {len(t)}')
    return t[0]


def riga_con(t, prima_cella):
    for r in t.rows:
        if r.cells[0].text.strip() == prima_cella:
            return r
    raise SystemExit('riga non trovata: ' + prima_cella)


def elimina(elementi, cosa):
    """Rimuove elementi XML, rifiutandosi di cancellare ciò che porta un commento."""
    for e in elementi:
        if D.ha_commenti(e):
            raise SystemExit(f'{cosa}: c’è un commento di Word ancorato qui, non si cancella')
    for e in elementi:
        e.getparent().remove(e)
    fatti.append('eliminato: ' + cosa)


def sezione_elementi(heading, livelli=('Heading 1', 'Heading 2', 'Heading 3')):
    """Gli elementi dal paragrafo dato (escluso) fino al successivo heading di pari o
    superiore livello."""
    lv = int(heading.style.name.split()[-1])
    fuori, out = False, []
    e = heading._p.getnext()
    while e is not None and not fuori:
        if e.tag.endswith('}p'):
            st = Paragraph(e, doc).style.name
            if st in livelli and int(st.split()[-1]) <= lv:
                break
        out.append(e)
        e = e.getnext()
    return out


def inserisci_riga(t, dopo, valori):
    nuova = D.clona_riga(t, valori)
    riga_con(t, dopo)._tr.addnext(nuova._tr)
    return nuova


def togli_riga(t, prima_cella):
    r = riga_con(t, prima_cella)
    if D.ha_commenti(r._tr):
        raise SystemExit(f'riga «{prima_cella}» commentata: non si cancella')
    t._tbl.remove(r._tr)


def mono(testo):
    t = [p for p in doc.paragraphs if p.text.rstrip() == testo.rstrip()]
    if len(t) != 1:
        raise SystemExit(f'riga DDL non univoca: «{testo[:60]}» ({len(t)})')
    return t[0]


def blocco_ddl(create_line):
    """Dal CREATE dato fino al «) TABLESPACE ANSC_USR;» che lo chiude."""
    p = mono(create_line)
    out, e = [p._p], p._p.getnext()
    while e is not None:
        out.append(e)
        if e.tag.endswith('}p') and Paragraph(e, doc).text.strip().startswith(') TABLESPACE'):
            return out
        e = e.getnext()
    raise SystemExit('blocco DDL non chiuso: ' + create_line)


def sostituisci_blocco(create_line, righe):
    el = blocco_ddl(create_line)
    dopo = el[-1].getnext()
    elimina(el, 'blocco DDL ' + create_line.split('.')[-1].split()[0])
    D.ddl(doc, dopo, righe)


def ddl_dopo(ancora_testo, righe):
    D.ddl(doc, mono(ancora_testo)._p.getnext(), righe)


MOD = D.trova_tabella(doc, 'colonna', 'tipo', 'note')   # modello di stile per le tabelle nuove


# ═══════════════════════════════════════════ 1. scheda informativa e storia
scheda = [t for t in doc.tables if t.rows[0].cells[0].text.strip().lower().startswith(
    ('area organizzativa', 'progetto'))]
for t in scheda:
    for nome, val in (('Data consegna', '24/09/2026'), ('Versione', '3.22')):
        try:
            D.riscrivi_cella(riga_con(t, nome).cells[1], val)
        except SystemExit:
            pass

D.storia(doc, '24/09/2026', '3.22',
         'Adeguamenti database · Flusso operativo · Costruzione del payload · Impatti FE · '
         'Decisioni · Open Point · Appendice A',
         'Recepito il modello di configurazione della sorgente del Comune: le logiche di '
         'scelta dell’UC e di attivazione delle sezioni si dichiarano una volta sola in un '
         'catalogo (TIPO_DOMINIO e VALORI_DOMINIO) e si citano per codice; le sezioni del '
         'modello evento diventano un livello proprio della configurazione '
         '(ANSC_CFG_SEZIONE). L’UC determinato e la logica che lo ha prodotto si registrano '
         'sull’atto: ANSC_XREF non conserva più alcun dato proprio ed è eliminata (OP-25 '
         'chiuso). Riscritto il capitolo del flusso operativo con, per ogni passo, ciò che '
         'legge, ciò che scrive e la traccia che lascia in ANSC_LOG_AUDIT. Aggiunto il punto '
         'di attenzione sulla gestione documentale e sulla firma digitale dei documenti '
         '(OP-57, OP-58) e registrata la transcodifica dei valori fra SIPO e ANSC (OP-59).')


# ═══════════════════════════════════════════ 2. il catalogo delle logiche (cap. 5.3)
ancora = D.h(doc, 2, 'Struttura dettagliata delle tabelle di configurazione')
dopo = sezione_elementi(ancora)[0]      # si innesta in testa alla sezione

D.para(doc, dopo, 'Il catalogo delle logiche', stile='Heading 3')
for t in [
    'Due tabelle reggono ciò che la configurazione deve poter decidere senza che nessuno '
    'scriva codice: quale UC si applica a un atto, e quando una sezione del modello evento va '
    'popolata. In entrambi i casi la condizione non è scritta dentro la riga che la usa ma in '
    'un catalogo, e la riga la richiama per codice.',
    'La differenza non è di forma. La stessa condizione — «nato vivo», «nato morto», «rito '
    'cattolico» — vale per molti UC e per molti Modelli: scritta dentro ogni riga si '
    'ripeterebbe decine di volte, e una correzione andrebbe fatta decine di volte con la '
    'certezza di dimenticarne qualcuna. Scritta una volta nel catalogo, si corregge in un '
    'punto solo e si vede dove è usata.',
    '⚠️ Le due tabelle hanno nomi vicini a quelli dei dizionari ANSC (DOMINIO_DECODIFICA e '
    'VALORE_DOMINIO) ma non sono la stessa cosa e non vanno confuse: i dizionari replicano i '
    'valori ammessi che ANSC pubblica, il catalogo delle logiche contiene decisioni del '
    'Comune. In particolare la loro numerazione è separata e interna: il dominio 1 del '
    'catalogo è la logica di scelta dell’UC, non la decodifica ANSC_01. La riconciliazione '
    'dei nomi è registrata come punto aperto (OP-56).',
]:
    D.para(doc, dopo, t)

D.para(doc, dopo, 'TIPO_DOMINIO — i domini di logica.')
D.tabella(doc, dopo, [
    ('Colonna', 'Tipo', 'Note'),
    ('ID_DOMINIO', 'NUMBER (PK)', 'Identificativo del dominio. ⚠️ Numerazione propria del '
     'Comune, distinta da quella delle decodifiche ANSC.'),
    ('DESCRIZIONE', 'VARCHAR2(200)', 'A che cosa serve il dominio. Oggi sono due: 1 = logica '
     'di scelta dell’UC, 2 = logica di attivazione di una sezione.'),
    ('DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici di audit previsti dallo standard di nomenclatura [R5].'),
], MOD)

D.para(doc, dopo, 'VALORI_DOMINIO — le logiche, scritte una volta sola.')
D.tabella(doc, dopo, [
    ('Colonna', 'Tipo', 'Note'),
    ('ID_DOMINIO', 'NUMBER (PK, FK)', 'Dominio di appartenenza (TIPO_DOMINIO).'),
    ('COD_LOGICA', 'VARCHAR2(30) (PK)', 'Nome della logica, con cui la configurazione la '
     'richiama: NASC_VIVO, NASC_MORTO, MATR_CAT, OBBLIGATORIA, OMISSIBILE, INTERPRETE.'),
    ('DESCRIZIONE', 'VARCHAR2(1000)', 'Che cosa la logica stabilisce, in lingua corrente: è '
     'la parte che il funzionario legge e su cui si assume la responsabilità.'),
    ('TXT_LOGICA', 'VARCHAR2(2000)', '⚠️ L’espressione valutata sui dati che SIPO ha già '
     'registrato, per esempio ATTO_NASCITA.FLG_NATO_MORTO=\'N\' e '
     'ATTO_NASCITA.FLG_MORTO_PREDENUNCIA=\'N\'. Il linguaggio non è fissato dal presente '
     'documento: è scelta del Comune, come per le altre colonne di logica.'),
    ('DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici di audit previsti dallo standard di nomenclatura [R5].'),
], MOD)

for t in [
    'Alcune logiche del secondo dominio non sono condizioni ma dichiarazioni: OBBLIGATORIA '
    'significa che la sezione si costruisce sempre, OPZIONALE che ANSC non la pretende, e '
    '⚠️ OMISSIBILE che la sezione si può omettere perché il dato che la discrimina non '
    'esiste in SIPO. Quest’ultima merita attenzione: è il modo in cui la configurazione '
    'registra, senza nasconderlo, che una parte del modello evento non è alimentabile con i '
    'dati che il Comune possiede oggi.',
]:
    D.para(doc, dopo, t)

D.para(doc, dopo, 'ANSC_CFG_SEZIONE — quando una sezione si popola', stile='Heading 3')
for t in [
    'Il mapping ufficiale non elenca soltanto campi: li raggruppa in sezioni — Madre, Padre, '
    'Dichiarante, Soggetto intervenuto, Ufficiale dello Stato Civile — e la condizione che '
    'decide se una sezione serve è dichiarata a quel livello, non sul singolo campo. Nella '
    'v3.21 la condizione stava su ANSC_CFG_CAMPO e si ripeteva identica su tutte le righe '
    'della stessa sezione: trentaquattro volte per la madre, trentaquattro per il padre, in '
    'un solo UC di nascita.',
    'La sezione diventa quindi un livello proprio della configurazione. Ne discendono tre '
    'conseguenze: la condizione si scrive una volta, la tabella dei campi perde tre colonne '
    'su oltre sessantamila righe, e il costruttore del payload ha un ordine naturale di '
    'lavoro — prima decide quali blocchi costruire, poi li riempie.',
]:
    D.para(doc, dopo, t)
D.tabella(doc, dopo, [
    ('Colonna', 'Tipo', 'Note'),
    ('ID_SEZIONE', 'NUMBER (PK)', 'Chiave tecnica.'),
    ('ID_VERSIONE', 'NUMBER (FK)', 'Baseline di appartenenza (ANSC_CFG_VERSIONE). È qui, e '
     'non più sui campi, che la baseline si dichiara.'),
    ('ID_UC', 'NUMBER (FK)', 'UC di riferimento nel catalogo ANSC_ANA_UC: le sezioni '
     'richieste differiscono fra UC dello stesso Modello.'),
    ('SEZIONE_FE_ANSC', 'VARCHAR2(200)', 'Nome della sezione come compare nel mapping e nella '
     'web app di ANSC.'),
    ('OGGETTO_ANSC', 'VARCHAR2(1000)', 'Radice del blocco nel modello evento: evento.madre, '
     'evento.interprete, evento.intestatari[0].'),
    ('DESCRIZIONE', 'VARCHAR2(1000)', 'Che cosa stabilisce la condizione, in lingua corrente, '
     'come la dichiara il mapping.'),
    ('ID_DOMINIO / COD_LOGICA', 'NUMBER / VARCHAR2(30) (FK)', 'La logica di attivazione, '
     'presa dal catalogo (dominio 2).'),
    ('NUM_ORDINE', 'NUMBER', 'Ordine di costruzione delle sezioni.'),
    ('COD_ORIGINE', 'VARCHAR2(20)', 'PROPOSTO, CONFERMATO, MODIFICATO, INSERITO: come per '
     'campi, allegati e formule. Governa la reimportazione.'),
    ('DATA_INS / DATA_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici di audit previsti dallo standard di nomenclatura [R5].'),
], MOD)
D.para(doc, dopo, 'Vincolo di unicità su (ID_VERSIONE, ID_UC, OGGETTO_ANSC): una sola '
                  'dichiarazione per blocco, dentro una baseline.')
fatti.append('cap. 5.3: catalogo delle logiche e ANSC_CFG_SEZIONE')


# ═══════════════════════════════════════════ 3. schede modificate
# 3a — ANSC_STATO_ATTO: l'UC determinato e la logica che lo ha prodotto
t = D.tabella_colonne(doc, 'ID_STATO_ATTO')
inserisci_riga(t, 'ID_MODELLO_ATTO', (
    'COD_UC_ANSC', 'VARCHAR2(20)',
    'UC determinato al passo «Completa». ⚠️ È il dato che rende ripetibile la lettura '
    'dell’atto: il Modello da solo non basta, perché più UC lo condividono.'))
inserisci_riga(t, 'COD_UC_ANSC', (
    'COD_LOGICA', 'VARCHAR2(30)',
    'Logica del catalogo che ha determinato l’UC (VALORI_DOMINIO, dominio 1). Senza di essa '
    'la determinazione non è spiegabile a posteriori: è ciò che la vista di supervisione '
    'mostra accanto all’UC.'))
fatti.append('ANSC_STATO_ATTO: COD_UC_ANSC e COD_LOGICA')

# 3b — ANSC_CFG_UC: la logica non è più una colonna di testo
t = D.tabella_colonne(doc, 'ID_UC_CFG')
r = riga_con(t, 'LOGICA_DI_SCELTA')
D.riscrivi_cella(r.cells[0], 'ID_DOMINIO / COD_LOGICA')
D.riscrivi_cella(r.cells[1], 'NUMBER / VARCHAR2(30) (FK)')
D.riscrivi_cella(r.cells[2], 'La logica che stabilisce se l’UC si applica all’atto in '
                             'lavorazione, presa dal catalogo (dominio 1). ⚠️ Nella v3.21 '
                             'era una colonna di testo per riga: la stessa condizione si '
                             'ripeteva su ogni UC che la usa. Vuota significa «si applica '
                             'sempre»: è il caso dei Modelli che indirizzano un solo UC.')

# 3c — ANSC_CFG_CAMPO: le sezioni escono, resta il campo
t = D.tabella_colonne(doc, 'ID_CAMPO')
r = riga_con(t, 'ID_UC')
D.riscrivi_cella(r.cells[0], 'ID_SEZIONE')
D.riscrivi_cella(r.cells[1], 'NUMBER (FK)')
D.riscrivi_cella(r.cells[2], 'Sezione di appartenenza (ANSC_CFG_SEZIONE), che porta l’UC e '
                             'la baseline. ⚠️ Il campo non nomina più né l’uno né l’altra: '
                             'li eredita, e non possono divergere.')
for c in ('ID_VERSIONE', 'SEZIONE_FE_ANSC', 'DESC_COND_OBBLIGATORIETA_EVENTO',
          'LOGICA_COND_OBBLIGATORIETA_EVENTO'):
    togli_riga(t, c)
fatti.append('ANSC_CFG_CAMPO: quattro colonne in meno, aggancio alla sezione')

# 3d — la tabella d'insieme del capitolo
t = D.trova_tabella(doc, 'oggetto', 'ruolo', 'note principali')
togli_riga(t, 'ANSC_XREF')
r = riga_con(t, 'ANSC_CFG_UC — la regola di scelta')
D.riscrivi_cella(r.cells[0], 'ANSC_CFG_UC — la scelta dell’UC')
D.riscrivi_cella(r.cells[2], 'La riga dichiara quale UC si adotta per un Modello e con quale '
                             'priorità; la condizione che decide sta nel catalogo delle '
                             'logiche ed è richiamata per codice (ID_DOMINIO, COD_LOGICA). '
                             'Struttura al capitolo «La determinazione dell’UC e le regole di '
                             'controllo».')
inserisci_riga(t, 'ANSC_CFG_UC — la scelta dell’UC', (
    'ANSC_CFG_SEZIONE',
    'Sezioni del modello evento richieste da ciascun UC, con la condizione che le attiva.',
    'Sta fra l’UC e i campi: porta la baseline e la logica di attivazione, e i campi vi '
    'pendono. Evita che la stessa condizione si ripeta su ogni campo della sezione.'))
inserisci_riga(t, 'ANSC_CFG_SEZIONE', (
    'TIPO_DOMINIO e VALORI_DOMINIO',
    'Catalogo delle logiche decise dal Comune: scelta dell’UC (dominio 1) e attivazione delle '
    'sezioni (dominio 2).',
    '⚠️ Da non confondere con i dizionari ANSC, che hanno nomi simili e contenuto diverso: '
    'qui stanno decisioni del Comune, lì valori pubblicati da ANSC. Numerazioni separate '
    '(OP-56).'))
fatti.append('tabella d’insieme del capitolo 5 aggiornata')

# 3e — via la scheda di ANSC_XREF
h = par('ANSC_XREF — mappa durevole', stile='Heading 3')
elimina([h._p] + sezione_elementi(h), 'scheda ANSC_XREF')


# ═══════════════════════════════════════════ 4. il flusso operativo (cap. 6)
h = D.h(doc, 1, 'Gli step del processo di integrazione SIPO-ANSC')
elimina(sezione_elementi(h), 'vecchio corpo del capitolo sugli step')
D.testo_di(h, 'Il flusso operativo: dall’atto di SIPO all’atto formato')
dopo = h._p.getnext()

for t in [
    'Definite le tabelle, il presente capitolo ne descrive l’uso in sequenza: dall’atto '
    'salvato in SIPO all’atto formato in ANSC. Per ciascun passo si dichiarano tre cose — che '
    'cosa legge, che cosa lascia scritto e con quale fase l’operazione viene tracciata — '
    'perché una traccia che non sia prevista nel disegno non la scrive nessuno, e la si '
    'scopre mancante il giorno in cui occorre spiegare che cosa è accaduto a un atto.',
]:
    D.para(doc, dopo, t)
D.immagine(doc, dopo, os.path.join(IMG, 'flusso_operativo.png'), 6.3,
           'Il flusso operativo. In rosso i passi che chiamano ANSC, in blu quelli che si '
           'svolgono nel concentratore; la colonna di destra è la fase con cui ciascun passo '
           'si registra in ANSC_LOG_AUDIT.')

D.tabella(doc, dopo, [
    ('Passo', 'Che cosa legge', 'Che cosa scrive', 'Traccia'),
    ('1 — Salvataggio dell’atto', 'Le maschere di SIPO.', 'L’atto nelle tabelle di SIPO: da '
     'qui l’identificativo ID_ATTO_SIPO, che correla tutto il resto.', '—'),
    ('2 — «Completa»: determinazione dell’UC',
     'ANSC_CFG_UC per la coppia tipo atto e Modello, nella baseline ATTIVA, in ordine di '
     'NUM_PRIORITA; per ciascuna riga la logica richiamata in VALORI_DOMINIO.',
     'ANSC_STATO_ATTO: la riga dell’atto, con COD_UC_ANSC, COD_LOGICA, ID_VERSIONE e stato '
     'IN_PREPARAZIONE.', 'DETERMINAZIONE'),
    ('3 — «Verifica»: il pre-filtro locale (RF-9)',
     'ANSC_CFG_SEZIONE per sapere quali blocchi servono, ANSC_CFG_CAMPO per i campi '
     'obbligatori, ANSC_CFG_ALLEGATO per i documenti, V_ANSC_DIZ_VALIDO per i valori ammessi.',
     'Nulla di definitivo: l’esito è l’elenco di ciò che manca, mostrato all’operatore.',
     'PREVERIFICA'),
    ('4 — I documenti: caricamento e invio (R001)',
     'ANSC_CFG_ALLEGATO: quali documenti l’UC richiede.',
     'ALLEGATO: il file, la sua impronta, lo stato restituito da ANSC e l’identificativo '
     'dell’allegato. ⚠️ Solo lo stato «Inserito» consente di proseguire.', 'ALLEGATI'),
    ('5 — La ricerca dei soggetti (R005)',
     'ANSC, per identificativo o per dati anagrafici.',
     'L’identificativo nazionale del soggetto nel payload in costruzione. ⚠️ Passo '
     'obbligatorio: senza di esso il deposito richiede il collegamento manuale, che la nota '
     'di processo ANSC definisce fortemente sconsigliato.', 'SOGGETTO'),
    ('6 — La costruzione del payload',
     'ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO, ANSC_CFG_FORMULA e i dizionari per le transcodifiche.',
     'ANSC_STATO_ATTO.TXT_PAYLOAD: il modello evento come è stato costruito.', 'PAYLOAD'),
    ('7 — L’anteprima (R010), facoltativa',
     'Il payload costruito: R010 richiede l’intero modello evento, non un identificativo.',
     'Nulla: è una lettura. Serve a mostrare all’ufficiale il testo dell’atto prima che '
     'l’identificativo nazionale sia consumato.', 'ANTEPRIMA'),
    ('8 — «Valida»: il deposito (R009)', 'Il payload costruito.',
     'ANSC_STATO_ATTO: ID_ANSC, ID_OPERAZIONE_ANSC e stato CONFERMATO. ⚠️ Da qui '
     'l’identificativo nazionale è consumato.', 'DEPOSITO'),
    ('9 — Le firme (R006, R007)',
     'Lo stato reale dell’atto, quando occorre riprendere una lavorazione interrotta.',
     'ANSC_STATO_ATTO: stato FIRMATO_DICHIARANTE e poi FIRMATO_USC, che è l’atto formato.',
     'FIRMA_DICH, FIRMA_USC'),
], MOD)
D.para(doc, dopo, 'I passi del flusso, con la configurazione che li guida e la traccia che '
                  'lasciano.', corsivo=True)

D.para(doc, dopo, 'La determinazione dell’UC', stile='Heading 2')
for t in [
    'Il front-end chiede il completamento passando tre dati: l’identificativo dell’atto, il '
    'tipo atto e il Modello. Il concentratore cerca in ANSC_CFG_UC le righe che li '
    'corrispondono ⚠️ limitatamente alla baseline ATTIVA, le ordina per priorità crescente e '
    'valuta la logica di ciascuna sui dati che SIPO ha già registrato. Vince la prima riga la '
    'cui logica è soddisfatta, e le righe senza logica si applicano sempre: sono i Modelli '
    'che indirizzano un solo UC.',
    'Il filtro sulla baseline non è un dettaglio: senza di esso la stessa configurazione '
    'esiste in più versioni e la ricerca restituisce righe di revisioni diverse. È la ragione '
    'per cui ID_VERSIONE è nella chiave di unicità della configurazione.',
    'Due esiti su tre non producono un UC, e vanno trattati diversamente.',
]:
    D.para(doc, dopo, t)
D.tabella(doc, dopo, [
    ('Esito della ricerca', 'Comportamento'),
    ('Una sola riga valida', 'Si registra l’UC e la logica che l’ha determinato su '
     'ANSC_STATO_ATTO e si prosegue.'),
    ('Nessuna riga valida', 'La lavorazione si ferma con un messaggio che dice che per quel '
     'Modello nessun caso d’uso è applicabile. È la categoria di eccezione «UC non '
     'determinato»: può essere un dato dell’atto o una lacuna della configurazione, e in '
     'entrambi i casi va guardata prima di procedere.'),
    ('Più righe valide', 'La priorità le ordina e la prima vince: è il meccanismo previsto, '
     'non un ripiego. Se due righe hanno la stessa priorità la configurazione è ambigua e la '
     'lavorazione si ferma: categoria «UC ambiguo».'),
    ('⚠️ La scelta non si chiede all’operatore', 'Mostrare a video gli UC candidati e farne '
     'scegliere uno trasferirebbe allo sportello una decisione che è di configurazione: due '
     'atti identici finirebbero su UC diversi secondo chi li lavora, e l’errore non '
     'lascerebbe traccia di sé. L’ambiguità si corregge nella configurazione, dove è visibile '
     'a chi la governa.'),
], MOD)

D.para(doc, dopo, 'La traccia di ciò che accade', stile='Heading 2')
for t in [
    'Ogni passo lascia una riga in ANSC_LOG_AUDIT con la propria fase, l’esito e, per le '
    'chiamate, la richiesta e la risposta. ⚠️ La traccia non riguarda soltanto le chiamate '
    'verso ANSC: anche la determinazione dell’UC, il pre-filtro e la costruzione del payload '
    'ne lasciano una, perché sono le decisioni che spiegano il payload. Un atto rifiutato da '
    'ANSC si comprende leggendo che cosa è stato deciso prima di inviarlo, non soltanto che '
    'cosa è stato inviato.',
    'Le due tracce non si sovrappongono. ANSC_LOG_AUDIT conserva il decorso, passo per passo, '
    'ed è soggetto a minimizzazione perché contiene dati particolari; ANSC_STATO_ATTO conserva '
    'l’esito e il payload del deposito, che deve sopravvivere alla purga dell’audit perché '
    'l’atto è formato e la sua ricostruzione non è più possibile: la configurazione che lo ha '
    'prodotto cambia in media una volta ogni diciassette giorni.',
    'Dell’audit va dichiarato anche ciò che non deve contenere: le credenziali di firma, il '
    'codice di sessione e i dati dei soggetti oltre a quanto serve a ricondurre la chiamata '
    'all’atto. Il capitolo «Sicurezza e configurazione» ne tratta insieme alla conservazione.',
]:
    D.para(doc, dopo, t)
fatti.append('capitolo del flusso operativo riscritto, con figura e tabella del logging')


# ═══════════════════════════════════════════ 5. punto di attenzione: i documenti
h = D.h(doc, 2, 'Gli allegati richiesti dall’UC')
el = sezione_elementi(h)
dopo = el[-1].getnext()
D.para(doc, dopo, 'Punto di attenzione: i documenti e la loro firma', stile='Heading 2')
for t in [
    '⚠️ La gestione dei documenti è la parte del disegno con il maggiore scarto fra ciò che '
    'la configurazione sa già e ciò che il sistema sa fare. La configurazione dichiara, per '
    'ciascun UC, quali documenti servono e quali sono obbligatori; ma l’area di stato civile '
    'di SIPO non gestisce alcun documento allegato, e non esiste quindi né la maschera con '
    'cui si caricano, né il luogo in cui si conservano fino al deposito, né la funzione che '
    'li trasmette ad ANSC. Non è una funzione da riprogettare: è una funzione da costruire, e '
    'va dimensionata come tale.',
]:
    D.para(doc, dopo, t)

D.para(doc, dopo, 'Che cosa serve lato front-end')
for testa, corpo in [
    ('La maschera di caricamento. ', 'Un’area della lavorazione dell’atto che mostri l’elenco '
     'dei documenti richiesti dall’UC determinato — non dal Modello — distinguendo gli '
     'obbligatori dai facoltativi, e consenta di caricare, sostituire e togliere un file. La '
     'libreria condivisa del front-end offre già i componenti di caricamento e il '
     'visualizzatore di PDF: l’intervento non è grafico.'),
    ('Lo stato di ciascun documento. ', 'Dopo l’invio, il documento attraversa la scansione '
     'antivirus di ANSC e soltanto lo stato «Inserito» consente di proseguire. ⚠️ È uno stato '
     'altrui e asincrono: la maschera deve mostrarlo e consentire di rileggerlo, non '
     'presumerlo dall’esito del caricamento.'),
    ('L’attestazione di conformità. ', 'Per i documenti che vi rientrano occorre un '
     'contrassegno visibile e modificabile dall’ufficiale: è una scelta del Comune, che il '
     'mapping non dichiara.'),
    ('⚠️ I documenti firmati digitalmente. ', 'Se un documento arriva firmato — un certificato '
     'necroscopico, un provvedimento, una delega — il front-end deve mostrarne l’esito della '
     'verifica e non soltanto il file: chi carica non è in grado di distinguere una firma '
     'valida da una scaduta guardando un’icona. Il browser non verifica le firme, e nessuna '
     'libreria di interfaccia può farlo in modo attendibile: la verifica è del back-end e il '
     'front-end ne presenta il risultato.'),
]:
    D.voce(doc, dopo, testa, corpo)

D.para(doc, dopo, 'Che cosa serve lato back-end')
for testa, corpo in [
    ('La conservazione fino al deposito. ', 'La tabella ALLEGATO conserva il documento nella '
     'colonna oj_allegato, cioè dentro la base dati. È la struttura ereditata dal sistema '
     'Side e la si adotta così com’è, con la raccomandazione già espressa di valutare un '
     'archivio a oggetti quando i volumi usciranno da quelli del pilota (OP-57).'),
    ('L’impronta e l’identità del file. ', 'Il calcolo dell’impronta alla ricezione è ciò che '
     'consente di dire, in seguito, che il documento trasmesso è quello conservato. La colonna '
     'esiste: va riempita, e va deciso con quale algoritmo.'),
    ('L’invio e l’attesa (R001). ', 'Il documento si trasmette prima del deposito e '
     'l’identificativo restituito da ANSC si conserva sull’allegato: è ciò che rende '
     'realizzabile RF-17, cioè rileggere da SIPO un documento che risiede in ANSC.'),
    ('⚠️ La verifica della firma. ', 'Se il Comune decide che i documenti firmati vanno '
     'verificati, servono un servizio che lo faccia e una regola che dica che cosa accade '
     'quando la verifica non riesce: si blocca la lavorazione o si segnala e si prosegue. Il '
     'presente documento non lo decide e non lo presume: lo registra come punto aperto '
     '(OP-58). ⚠️ Va tenuta distinta dalle due firme del percorso — quella del dichiarante e '
     'quella dell’ufficiale — che riguardano l’atto e non i suoi allegati, e che ANSC governa '
     'con R006 e R007.'),
    ('I formati e le dimensioni ammesse. ', 'ANSC dichiara i formati in una propria '
     'decodifica: il controllo va fatto in locale prima dell’invio, insieme al resto del '
     'pre-filtro, perché un documento rifiutato dopo il caricamento è tempo dello sportello.'),
]:
    D.voce(doc, dopo, testa, corpo)
D.para(doc, dopo, 'Il punto da chiarire prima dello sviluppo è di perimetro, non tecnico: se '
                  'la gestione documentale nasca dentro l’integrazione ANSC — e allora serve '
                  'soltanto per gli atti che si depositano — oppure sia una funzione dell’area '
                  'di stato civile, e allora vale anche per gli atti che in ANSC non vanno, '
                  'con conseguenze su conservazione, ricerca e cancellazione. La seconda è la '
                  'scelta più costosa e la sola che non vada rifatta.')
fatti.append('nuovo punto di attenzione sui documenti e sulla firma')


# ═══════════════════════════════════════════ 6. impatti FE e DB
t = D.trova_tabella(doc, 'schermata / componente', 'tipo intervento')
D.clona_riga(t, ('Lavorazione dell’atto — sezione «Documenti»', 'Maschera nuova',
                 'Elenco dei documenti richiesti dall’UC determinato, con obbligatorietà, '
                 'caricamento, sostituzione, anteprima e stato restituito da ANSC. Oggi '
                 'l’area di stato civile non gestisce allegati: la maschera non esiste.',
                 'Alta'))
D.clona_riga(t, ('Lavorazione dell’atto — esito della firma di un documento',
                 'Campo di sola lettura',
                 'Dove il documento caricato è firmato digitalmente, mostrare l’esito della '
                 'verifica effettuata dal back-end. Subordinato alla decisione su OP-58.',
                 'Media'))
D.clona_riga(t, ('Lavorazione dell’atto — barra della sessione ANSC', 'Componente nuovo',
                 'Tempo residuo della sessione e avviso sotto la soglia di guardia, perché '
                 'una sequenza lunga non si interrompa a metà.', 'Media'))

t = D.trova_tabella(doc, 'oggetto db', 'tipo intervento')
D.clona_riga(t, ('ANSC_USR.ALLEGATO — colonne della firma', 'Modifica tabella nuova',
                 'Se la verifica della firma dei documenti rientra nel perimetro (OP-58), '
                 'occorrono le colonne che ne conservano l’esito e il momento: senza, la '
                 'verifica si ripete a ogni lettura e non è opponibile.'))
fatti.append('impatti FE e DB aggiornati')


# ═══════════════════════════════════════════ 7. PC-9
h = D.h(doc, 2, 'PC-9')
el = sezione_elementi(h)
dopo = el[-1].getnext()
for t in [
    '⚠️ Revisione della v3.22: la decisione resta, cambia dove la condizione risiede. Nella '
    'v3.21 la logica di scelta era una colonna di ANSC_CFG_UC, cioè un testo per riga; ora è '
    'una riga del catalogo delle logiche, richiamata per codice. Il guadagno è che la stessa '
    'condizione non si ripete — «nato vivo» vale per molti UC e per molti Modelli — e che si '
    'può dire, interrogando la configurazione, quali UC dipendono da una logica prima di '
    'modificarla.',
    'Resta invariato ciò che la decisione aveva già accettato: le condizioni sono valutate '
    'dal concentratore e non in procedure di base dati, non sono dimostrabili per copertura e '
    'mutua esclusione, e il controllo principale è la simulazione su atti reali. Resta anche '
    'il prezzo: il linguaggio dell’espressione non è fissato dal presente documento.',
]:
    D.para(doc, dopo, t)
fatti.append('PC-9 aggiornata')


# ═══════════════════════════════════════════ 8. Appendice A — il DDL
# 8a — le due tabelle del catalogo, prima di chi le referenzia
ddl_dopo('CREATE TABLE ANSC_USR.ANSC_CFG_UC (', [])   # verifica che l'ancora esista
D.ddl(doc, mono('CREATE TABLE ANSC_USR.ANSC_CFG_UC (')._p, [
    'CREATE TABLE ANSC_USR.TIPO_DOMINIO (',
    '  ID_DOMINIO           NUMBER             NOT NULL,',
    '  DESCRIZIONE          VARCHAR2(200 CHAR) NOT NULL,',
    '  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  UTENTE_INS           VARCHAR2(40 CHAR),',
    '  UTENTE_UPD           VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_TIPO_DOMINIO PRIMARY KEY (ID_DOMINIO)',
    ') TABLESPACE ANSC_USR;',
    'COMMENT ON TABLE ANSC_USR.TIPO_DOMINIO IS',
    "  'Domini delle logiche decise dal Comune: 1 scelta dell UC, 2 attivazione di sezione.",
    "   ATTENZIONE: non sono le decodifiche ANSC (DOMINIO_DECODIFICA): numerazione separata.';",
    ' ',
    'CREATE TABLE ANSC_USR.VALORI_DOMINIO (',
    '  ID_DOMINIO           NUMBER             NOT NULL,',
    '  COD_LOGICA           VARCHAR2(30 CHAR)  NOT NULL,',
    '  DESCRIZIONE          VARCHAR2(1000 CHAR) NOT NULL,',
    '  TXT_LOGICA           VARCHAR2(2000 CHAR),',
    '  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  UTENTE_INS           VARCHAR2(40 CHAR),',
    '  UTENTE_UPD           VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_VALORI_DOMINIO PRIMARY KEY (ID_DOMINIO, COD_LOGICA),',
    '  CONSTRAINT FK_VALORI_DOMINIO_TIPO',
    '    FOREIGN KEY (ID_DOMINIO) REFERENCES ANSC_USR.TIPO_DOMINIO (ID_DOMINIO)',
    ') TABLESPACE ANSC_USR;',
    'COMMENT ON COLUMN ANSC_USR.VALORI_DOMINIO.DESCRIZIONE IS',
    "  'Che cosa la logica stabilisce, in lingua corrente: e la parte che il funzionario legge",
    "   e approva. Obbligatoria: una logica senza descrizione non e governabile.';",
    'COMMENT ON COLUMN ANSC_USR.VALORI_DOMINIO.TXT_LOGICA IS',
    "  'Espressione valutata sui dati gia registrati da SIPO. Linguaggio non fissato dal",
    "   documento: e scelta del Comune. Vuota per le logiche dichiarative (OBBLIGATORIA...).';",
    ' ',
])

# 8b — ANSC_CFG_UC: la colonna di testo diventa un riferimento al catalogo
sostituisci_blocco('CREATE TABLE ANSC_USR.ANSC_CFG_UC (', [
    'CREATE TABLE ANSC_USR.ANSC_CFG_UC (',
    '  ID_UC_CFG            NUMBER GENERATED ALWAYS AS IDENTITY,',
    '  COD_UC_ANSC          VARCHAR2(20 CHAR)  NOT NULL,',
    '  COD_TIPO_EVENTO      VARCHAR2(20 CHAR)  NOT NULL,',
    '  COD_TIPO_OPERAZIONE  VARCHAR2(20 CHAR)  NOT NULL,',
    '  ID_MODELLO_ATTO      VARCHAR2(5 CHAR)   NOT NULL,',
    '  ID_CONF_TIPO_ATTO    NUMBER,',
    '  MASCHERA_UI          VARCHAR2(100 CHAR),',
    '  SERIE                VARCHAR2(10 CHAR),',
    '  NUM_PRIORITA         NUMBER DEFAULT 100 NOT NULL,',
    '  ID_DOMINIO           NUMBER DEFAULT 1,',
    '  COD_LOGICA           VARCHAR2(30 CHAR),',
    '  ID_VERSIONE          NUMBER             NOT NULL,',
    '  DATA_INIZIO_VALIDITA DATE DEFAULT SYSDATE            NOT NULL,',
    '  DATA_FINE_VALIDITA   DATE DEFAULT DATE \'9999-12-31\'  NOT NULL,',
    '  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  UTENTE_INS           VARCHAR2(40 CHAR),',
    '  UTENTE_UPD           VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_ANSC_CFG_UC PRIMARY KEY (ID_UC_CFG),',
    '  CONSTRAINT FK_ANSC_CFG_UC_VERSIONE',
    '    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),',
    '  CONSTRAINT FK_ANSC_CFG_UC_LOGICA',
    '    FOREIGN KEY (ID_DOMINIO, COD_LOGICA)',
    '    REFERENCES ANSC_USR.VALORI_DOMINIO (ID_DOMINIO, COD_LOGICA),',
    '  CONSTRAINT UK_ANSC_CFG_UC UNIQUE (COD_UC_ANSC, ID_VERSIONE)',
    ') TABLESPACE ANSC_USR;',
    'CREATE INDEX ANSC_USR.IX_ANSC_CFG_UC_MODELLO',
    '  ON ANSC_USR.ANSC_CFG_UC (ID_VERSIONE, ID_CONF_TIPO_ATTO, ID_MODELLO_ATTO,',
    '                           NUM_PRIORITA) TABLESPACE ANSC_USR;',
    'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.COD_LOGICA IS',
    "  'Logica di scelta presa dal catalogo (dominio 1). Vuota significa: si applica sempre.';",
    'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.NUM_PRIORITA IS',
    "  'Ordine di valutazione fra gli UC dello stesso Modello: il primo la cui logica e",
    "   soddisfatta determina l UC. Due righe con la stessa priorita sono una ambiguita.';",
])

# 8c — ANSC_CFG_SEZIONE, nuova, prima dei campi che vi pendono
D.ddl(doc, mono('CREATE TABLE ANSC_USR.ANSC_CFG_CAMPO (')._p, [
    'CREATE TABLE ANSC_USR.ANSC_CFG_SEZIONE (',
    '  ID_SEZIONE           NUMBER GENERATED ALWAYS AS IDENTITY,',
    '  ID_VERSIONE          NUMBER             NOT NULL,',
    '  ID_UC                NUMBER             NOT NULL,',
    '  SEZIONE_FE_ANSC      VARCHAR2(200 CHAR) NOT NULL,',
    '  OGGETTO_ANSC         VARCHAR2(1000 CHAR) NOT NULL,',
    '  DESCRIZIONE          VARCHAR2(1000 CHAR),',
    '  ID_DOMINIO           NUMBER DEFAULT 2,',
    '  COD_LOGICA           VARCHAR2(30 CHAR),',
    '  NUM_ORDINE           NUMBER DEFAULT 1   NOT NULL,',
    '  COD_ORIGINE          VARCHAR2(20 CHAR) DEFAULT \'PROPOSTO\' NOT NULL,',
    '  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  UTENTE_INS           VARCHAR2(40 CHAR),',
    '  UTENTE_UPD           VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_ANSC_CFG_SEZIONE PRIMARY KEY (ID_SEZIONE),',
    '  CONSTRAINT FK_ANSC_CFG_SEZIONE_UC',
    '    FOREIGN KEY (ID_UC) REFERENCES ANSC_USR.ANSC_ANA_UC (ID_UC),',
    '  CONSTRAINT FK_ANSC_CFG_SEZIONE_VERSIONE',
    '    FOREIGN KEY (ID_VERSIONE) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),',
    '  CONSTRAINT FK_ANSC_CFG_SEZIONE_LOGICA',
    '    FOREIGN KEY (ID_DOMINIO, COD_LOGICA)',
    '    REFERENCES ANSC_USR.VALORI_DOMINIO (ID_DOMINIO, COD_LOGICA),',
    '  CONSTRAINT UK_ANSC_CFG_SEZIONE UNIQUE (ID_VERSIONE, ID_UC, OGGETTO_ANSC),',
    '  CONSTRAINT CK_ANSC_CFG_SEZIONE_ORIG',
    "    CHECK (COD_ORIGINE IN ('PROPOSTO','CONFERMATO','MODIFICATO','INSERITO'))",
    ') TABLESPACE ANSC_USR;',
    'COMMENT ON TABLE ANSC_USR.ANSC_CFG_SEZIONE IS',
    "  'Sezioni del modello evento richieste da un UC e condizione che le attiva. Sta fra",
    "   l UC e i campi: la condizione si scrive una volta, non su ogni campo della sezione.';",
    ' ',
])

# 8d — ANSC_CFG_CAMPO: pende dalla sezione
sostituisci_blocco('CREATE TABLE ANSC_USR.ANSC_CFG_CAMPO (', [
    'CREATE TABLE ANSC_USR.ANSC_CFG_CAMPO (',
    '  ID_CAMPO             NUMBER GENERATED ALWAYS AS IDENTITY,',
    '  ID_SEZIONE           NUMBER             NOT NULL,',
    '  OGGETTO_ANSC         VARCHAR2(1000 CHAR) NOT NULL,',
    '  CAMPO_ANSC           VARCHAR2(120 CHAR)  NOT NULL,',
    '  FLG_OBBLIGATORIO     CHAR(1) DEFAULT \'N\' NOT NULL,',
    '  SCHEMA_SIPO          VARCHAR2(200 CHAR),',
    '  TABELLA_SIPO         VARCHAR2(200 CHAR),',
    '  CAMPO_SIPO           VARCHAR2(120 CHAR),',
    '  ID_DECODIFICA_ANSC   NUMBER,',
    '  DESCRIZIONE_BUSINESS_LOGIC VARCHAR2(1000 CHAR),',
    '  BUSINESS_LOGIC       VARCHAR2(1000 CHAR),',
    '  ORDINAMENTO          NUMBER DEFAULT 1   NOT NULL,',
    '  OPERATIVO            CHAR(1) DEFAULT \'1\' NOT NULL,',
    '  VALORE_DEFAULT       VARCHAR2(1000 CHAR),',
    '  MESSAGGIO            VARCHAR2(200 CHAR),',
    '  NOTE                 VARCHAR2(1000 CHAR),',
    '  COD_ORIGINE          VARCHAR2(20 CHAR) DEFAULT \'PROPOSTO\' NOT NULL,',
    '  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  UTENTE_INS           VARCHAR2(40 CHAR),',
    '  UTENTE_UPD           VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_ANSC_CFG_CAMPO PRIMARY KEY (ID_CAMPO),',
    '  CONSTRAINT FK_ANSC_CFG_CAMPO_SEZIONE',
    '    FOREIGN KEY (ID_SEZIONE) REFERENCES ANSC_USR.ANSC_CFG_SEZIONE (ID_SEZIONE),',
    '  CONSTRAINT UK_ANSC_CFG_CAMPO UNIQUE (ID_SEZIONE, OGGETTO_ANSC, CAMPO_ANSC),',
    "  CONSTRAINT CK_ANSC_CFG_CAMPO_OBBL CHECK (FLG_OBBLIGATORIO IN ('S','N')),",
    "  CONSTRAINT CK_ANSC_CFG_CAMPO_OPERATIVO CHECK (OPERATIVO IN ('0','1')),",
    '  CONSTRAINT CK_ANSC_CFG_CAMPO_ORIG',
    "    CHECK (COD_ORIGINE IN ('PROPOSTO','CONFERMATO','MODIFICATO','INSERITO'))",
    ') TABLESPACE ANSC_USR;',
    'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.ID_SEZIONE IS',
    "  'Sezione di appartenenza: porta l UC e la baseline, che il campo non ripete.';",
    'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.OGGETTO_ANSC IS',
    "  'Binding Object del mapping ufficiale: l oggetto del modello evento che contiene il campo.';",
    'COMMENT ON COLUMN ANSC_USR.ANSC_CFG_CAMPO.BUSINESS_LOGIC IS',
    "  'Script che produce il valore quando non e un trasferimento diretto. Linguaggio non fissato.';",
])

# 8e — ANSC_STATO_ATTO: due colonne nuove
D.ddl(doc, mono('  CHIAVE_ANTI_DUPLICATO   VARCHAR2(64 CHAR)  NOT NULL,')._p.getnext(), [
    '  COD_UC_ANSC             VARCHAR2(20 CHAR),',
    '  COD_LOGICA              VARCHAR2(30 CHAR),',
])

# 8f — ANSC_LOG_AUDIT: le fasi del flusso
D.testo_di(mono("    CHECK (FASE IN ('VERIFICA','ALLEGATI','SOGGETTO','DEPOSITO',"),
           "    CHECK (FASE IN ('DETERMINAZIONE','PREVERIFICA','ALLEGATI','SOGGETTO',")
D.testo_di(mono("                    'FIRMA_DICH','FIRMA_USC','RICONCILIAZIONE')),"),
           "                    'PAYLOAD','ANTEPRIMA','DEPOSITO','FIRMA_DICH','FIRMA_USC',"
           "\n                    'ANNULLAMENTO','RICONCILIAZIONE')),")

# 8g — via il DDL di ANSC_XREF
el = blocco_ddl('CREATE TABLE ANSC_USR.ANSC_XREF (')
coda = []
e = el[-1].getnext()
while e is not None and not (e.tag.endswith('}p') and Paragraph(e, doc).text.strip()
                             .startswith('ANSC_LOG_AUDIT')):
    coda.append(e)
    e = e.getnext()
elimina([mono('ANSC_XREF')._p] + el + coda, 'DDL di ANSC_XREF')
fatti.append('Appendice A: DDL aggiornato')


# 8h — le due COMMENT rimaste orfane della vecchia colonna di testo
orfani = [mono('COMMENT ON COLUMN ANSC_USR.ANSC_CFG_UC.LOGICA_DI_SCELTA IS')._p]
for _ in range(5):                       # le due COMMENT superate: 6 paragrafi in tutto
    orfani.append(orfani[-1].getnext())
atteso = 'determina l UC.'
assert Paragraph(orfani[-1], doc).text.strip().endswith("determina l UC.';"), \
    'la coda delle COMMENT superate non è quella attesa'
elimina(orfani, 'COMMENT superate di ANSC_CFG_UC')

# 8i — i due rimandi alla tabella eliminata
D.sostituisci(doc, 'si registra in ANSC_XREF.', 'si registra nello store di stato.',
              attese=1, etichetta='rimando ad ANSC_XREF', fatti=fatti)
D.sostituisci(doc, 'la v3.21 vi aggiunge SERIE, SCHEMA_SIPO, TABELLA_SIPO, OPERATIVO e '
                   'LOGICA_DI_SCELTA, introdotte con la revisione delle schede',
              'la v3.21 vi aggiunge SERIE, SCHEMA_SIPO, TABELLA_SIPO e OPERATIVO, e la v3.22 '
              'la DESCRIZIONE del catalogo delle logiche', attese=1,
              etichetta='OP-35: elenco delle colonne', fatti=fatti)


# ═══════════════════════════════════════════ 9. requisiti e open point
t = D.trova_tabella(doc, 'id', 'requisito', 'nota')
D.clona_riga(t, ('RF-18', 'Ogni passo del percorso — determinazione dell’UC, pre-filtro, '
                 'costruzione del payload, chiamate ad ANSC, firme — lascia una traccia con '
                 'la propria fase, l’esito e l’identificazione dell’operatore.',
                 'È ciò che consente di spiegare a posteriori che cosa è stato inviato e '
                 'perché. Capitolo «Il flusso operativo».'))

t = D.trova_tabella(doc, '#', 'tema', 'questione')
r = riga_con(t, 'OP-25')
D.riscrivi_cella(r.cells[2], 'Chiuso nella v3.22: l’UC determinato e la logica che lo ha '
                             'prodotto sono registrati su ANSC_STATO_ATTO, che già conservava '
                             'identificativo nazionale, protocollo e stato. ANSC_XREF non '
                             'conservava più alcun dato proprio ed è stata eliminata; il '
                             'raccordo fra notifica e atto passa per ID_ANSC dello store di '
                             'stato.')
D.riscrivi_cella(r.cells[3], 'Chiuso')
D.riscrivi_cella(r.cells[5], '—')
for num, tema, questione, owner, prio in [
    ('OP-56', 'Nomi del catalogo delle logiche',
     'TIPO_DOMINIO e VALORI_DOMINIO sono i nomi della sorgente del Comune e somigliano a '
     'quelli dei dizionari ANSC (DOMINIO_DECODIFICA, VALORE_DOMINIO), con i quali non hanno '
     'nulla in comune salvo la forma. Va deciso se rinominarli con il marcatore di '
     'configurazione dello standard [R5], in un solo intervento insieme a OP-35.',
     'Analisi / Cliente', 'Media'),
    ('OP-57', 'Conservazione dei documenti',
     'Dove risiedono i documenti allegati fino al deposito e per quanto vi restano: dentro la '
     'base dati, come la struttura ereditata prevede, oppure in un archivio a oggetti. La '
     'differenza è una colonna finché i volumi sono quelli del pilota; a regime sono '
     'centoquarantamila atti l’anno.', 'Cliente / Sistemi Informativi', 'Alta'),
    ('OP-58', 'Verifica della firma dei documenti',
     'Se i documenti firmati digitalmente debbano essere verificati dal sistema, con quale '
     'servizio, e che cosa accade quando la verifica non riesce: se la lavorazione si ferma o '
     'se l’esito è soltanto segnalato all’ufficiale. Da chiudere prima di disegnare le '
     'maschere di caricamento.', 'Cliente', 'Alta'),
    ('OP-59', 'Transcodifica dei valori fra SIPO e ANSC',
     'La configurazione dichiara quale dizionario ANSC valida un campo, non come si traduce '
     'un valore di SIPO nel corrispondente valore ANSC. La sorgente del Comune prevede un '
     'foglio di riconciliazione con validità temporale: va stabilito se diventi una tabella '
     'della configurazione, e chi la compila.', 'Analisi / Cliente', 'Alta'),
]:
    D.clona_riga(t, (num, tema, questione, 'Aperto', owner, prio))
fatti.append('registro degli open point: OP-25 chiuso, OP-56…59 aperti')


# ═══════════════════════════════════════════ 10. figure e salvataggio
D.sostituisci_immagine(doc, 'Schema ANSC_USR.', os.path.join(IMG, 'erd_ansc_usr.png'))
fatti.append('ERD rigenerato')

doc.save(DST)

# ────────────────────────────────────────────────────────────── controlli
import zipfile   # noqa: E402
z = zipfile.ZipFile(DST)
xml = z.read('word/document.xml').decode()
corpo = '\n'.join(p.text for p in docx.Document(DST).paragraphs)
assert 'ANSC_XREF' not in corpo, 'resta un riferimento ad ANSC_XREF fuori dalle tabelle'
# le sole citazioni ammesse sono quelle storiche: la Storia del Documento cita per mestiere
# le formulazioni superate, e il registro degli OP deve dire che cosa è stato chiuso.
assert xml.count('LOGICA_DI_SCELTA') == 1, (
    f"attesa 1 citazione storica di LOGICA_DI_SCELTA, {xml.count('LOGICA_DI_SCELTA')}")
# 5 = due righe della Storia del Documento, due del registro OP e la voce rimasta nel TOC,
# che è un campo di Word e si aggiorna con F9.
assert xml.count('ANSC_XREF') == 5, (
    f"attese 5 citazioni residue di ANSC_XREF, {xml.count('ANSC_XREF')}")
ncom = z.read('word/comments.xml').decode().count('<w:comment ')
d2 = docx.Document(DST)
for p in d2.paragraphs:
    if p.style.name.startswith('Heading') and len(p.text) > 95:
        raise SystemExit('heading anomalo: ' + p.text[:70])
print('\n'.join(' · ' + f for f in fatti))
print('commenti:', ncom, '· capitoli/tabelle/immagini:', D.riepilogo(DST))
print('scritto:', os.path.relpath(DST, BASE))


# ═══════════════════════════════════════════ 11. allineamenti del resto del testo
doc = docx.Document(DST)
fatti2 = []

# 11a — la regola che rende il catalogo governabile senza versionarlo
D.para(doc, par('TIPO_DOMINIO — i domini di logica')._p,
       '⚠️ Il catalogo non appartiene alla baseline, e da ciò discende una regola: le logiche '
       'non si riscrivono, si aggiungono. Cambiare il testo di una logica già in uso '
       'cambierebbe il significato di ogni riga che la richiama, comprese quelle delle '
       'baseline storiche e degli atti già formati con esse. Se la condizione cambia si '
       'introduce un codice nuovo e si aggiorna la configurazione che deve adottarlo: il '
       'codice vecchio resta, e resta leggibile ciò che è stato deciso ieri.')

# 11b — le tabelle citate per nome nei capitoli precedenti
D.sostituisci(doc, 'La configurazione risiede nelle tabelle ANSC_CFG_UC e ANSC_CFG_CAMPO di '
                   'ANSC_USR',
              'La configurazione risiede nelle tabelle ANSC_CFG_UC, ANSC_CFG_SEZIONE e '
              'ANSC_CFG_CAMPO di ANSC_USR', attese=1, etichetta='cap. 7.3: tabelle citate',
              fatti=fatti2)
D.sostituisci(doc, 'ANSC_CFG_UC con la sua regola di scelta, ANSC_CFG_CAMPO, '
                   'ANSC_CFG_ALLEGATO e ANSC_CFG_FORMULA',
              'ANSC_CFG_UC, ANSC_CFG_SEZIONE, ANSC_CFG_CAMPO, ANSC_CFG_ALLEGATO e '
              'ANSC_CFG_FORMULA', attese=1, etichetta='cap. 7.5: elenco della baseline',
              fatti=fatti2)
D.sostituisci(doc, 'il primo la cui regola di scelta è soddisfatta determina l’UC',
              'il primo la cui logica è soddisfatta determina l’UC', attese=1,
              etichetta='scheda NUM_PRIORITA', fatti=fatti2)

# 11c — il back-office: la schermata che governa il catalogo
t = D.trova_tabella(doc, 'schermata', 'scopo', 'azioni principali')
r = riga_con(t, 'Configurazione — Casi d’uso')
D.riscrivi_cella(r.cells[1], 'ANSC_CFG_UC: una riga per UC adottato, con il Modello di atto a '
                             'cui si applica, il tipo atto, la maschera, la priorità fra gli '
                             'UC dello stesso Modello e la logica che lo seleziona, scelta fra '
                             'quelle del catalogo.')
nuova = D.clona_riga(t, (
    'Configurazione — Catalogo delle logiche',
    'TIPO_DOMINIO e VALORI_DOMINIO: le logiche di scelta dell’UC e di attivazione delle '
    'sezioni, ciascuna con la propria descrizione e l’espressione che la realizza.',
    'Consulta, verifica dove una logica è usata prima di toccarla, aggiunge una logica nuova, '
    'la prova su un atto reale. ⚠️ Non consente di riscrivere una logica in uso.',
    'Admin'))
r._tr.addnext(nuova._tr)

# 11d — la figura della catena, che mostra le tabelle della configurazione
D.sostituisci_immagine(doc, 'Dalla maschera SIPO al payload ANSC.',
                       os.path.join(IMG, 'catena_configurazione.png'))
fatti2.append('figura della catena rigenerata')

doc.save(DST)
print('\n'.join(' · ' + f for f in fatti2))
print('finale:', D.riepilogo(DST))
