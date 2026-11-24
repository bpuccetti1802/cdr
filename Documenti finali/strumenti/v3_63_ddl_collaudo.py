# -*- coding: utf-8 -*-
"""v3.63 dell'analisi ANSC (24/11/2026), dalla v3.62 sul file reale.

Allineamento agli script della base dati di collaudo, che gli sviluppatori tengono su Box
(«DDL Roma / COLLAUDO - DDL e DML», copia in Sorgenti Documentali/DDL Roma/) = [R25].
Decisioni dell'utente (24/11/2026):
  1. le tabelle stanno, per ora, in MATR_USR;
  2. l'Appendice A non riporta più la DDL: una descrizione e il raggruppamento logico dei
     soli nomi; le estensioni *_EXTEND2 di SIPO entrano nell'analisi, descritte;
  3. su tutte le tabelle fanno fede gli script: il documento si ritocca dove serve.
Il confronto colonna per colonna è prodotto da strumenti/verifica_ddl.py.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_63_ddl_collaudo.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Inches
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.62.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.63.docx')
DATA = '24/11/2026'
ERD = os.path.join(QUI, 'img', 'erd_ansc_usr.png')

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))
FATTI = []


def par(inizio):
    t = [p for p in d.paragraphs if p.text.strip().startswith(inizio)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:70]))
    return t[0]


def riscrivi(p, testo):
    D.testo_di(p, testo)


def togli(el):
    if D.ha_commenti(el):
        raise SystemExit('elemento commentato: ' + ''.join(
            x.text or '' for x in el.iter(qn('w:t')))[:60])
    el.getparent().remove(el)


def sost(vecchio, nuovo, attese=1):
    D.sostituisci(d, vecchio, nuovo, attese=attese, fatti=FATTI)


def tab_colonna(prima_colonna_riga, sotto=None):
    """La tabella «Colonna | Tipo | Note» che contiene una data prima cella."""
    ris = []
    for t in d.tables:
        if [c.text.strip() for c in t.rows[0].cells][:2] != ['Colonna', 'Tipo']:
            continue
        if any(r.cells[0].text.strip() == prima_colonna_riga for r in t.rows):
            ris.append(t)
    if len(ris) != 1:
        raise SystemExit('tabella con %s: %d' % (prima_colonna_riga, len(ris)))
    return ris[0]


def righe_di(t):
    return {r.cells[0].text.strip(): (r.cells[1].text.strip(), r.cells[2].text.strip())
            for r in t.rows[1:]}


def riga(t, chiave, j=0):
    r = [x for x in t.rows if x.cells[j].text.strip() == chiave]
    if len(r) != 1:
        raise SystemExit('riga %s: %d' % (chiave, len(r)))
    return r[0]


def larghezze(t):
    g = t._tbl.find(qn('w:tblGrid'))
    return [int(c.get(qn('w:w'))) / 1440 for c in g.findall(qn('w:gridCol'))]


# ============================================================ 1. Riferimenti, glossario
rif = D.trova_tabella(d, 'ID', 'Riferimento', 'Contenuto')
D.riscrivi_cella(riga(rif, 'R5').cells[2],
                 riga(rif, 'R5').cells[2].text.replace(
                     'Definisce la nomenclatura adottata dallo schema ANSC_USR.',
                     'Definisce la nomenclatura adottata dalle tabelle dell’integrazione, '
                     'salvo quelle ereditate dal sistema Side.'))
D.clona_riga(rif, (
    'R25', 'DDL Roma — COLLAUDO, DDL e DML: cartella degli script della base dati su Box '
    '(app.box.com/folder/433579156431), fotografia del 24/11/2026',
    'Gli script della base dati tenuti dagli sviluppatori: creazione delle tabelle, '
    'modifiche alle tabelle esistenti, trigger, viste, indici, dati iniziali e '
    'aggiornamenti. È la fonte della struttura delle tabelle; il presente documento ne '
    'descrive il significato.'))
FATTI.append('Riferimenti: R25 (script della base dati), R5 senza ANSC_USR')

glo = D.trova_tabella(d, 'Termine', 'Significato')
D.riscrivi_cella(riga(glo, 'Store di stato ANSC').cells[1],
                 'Tabella ANSC_STATO_ATTO di MATR_USR: una riga per atto, con lo stato '
                 'dell’atto in ANSC (decodifica ANSC_11) e la fase della lavorazione in '
                 'SIPO. Il modello evento sta in ANSC_PAYLOAD, con la stessa chiave.')
c = riga(glo, 'Dizionario ANSC (decodifica)').cells[1]
D.riscrivi_cella(c, c.text.replace('tabelle locali di ANSC_USR', 'tabelle locali di MATR_USR'))
FATTI.append('Glossario: store di stato e dizionario in MATR_USR')

# ============================================================ 2. componenti
comp = [t for t in d.tables if t.rows[0].cells[-1].text.strip() == 'Unità di deployment autonoma'][0]
c = riga(comp, 'Concentratore dei dizionari dec-ansc-sipo (nuovo)').cells[1]
D.riscrivi_cella(c, c.text.replace('carico nelle tabelle ANSC_DIZ_* di ANSC_USR (RF-10)',
                                   'carico nelle tabelle DOMINIO_DECODIFICA e VALORE_DOMINIO '
                                   '(RF-10)'))
r = riga(comp, 'Store di stato ANSC (schema ANSC_USR)')
D.riscrivi_cella(r.cells[0], 'Store di stato ANSC (ANSC_STATO_ATTO)')
D.riscrivi_cella(r.cells[1], r.cells[1].text.replace('Una riga per atto × operazione',
                                                     'Una riga per atto'))
D.riscrivi_cella(r.cells[2], 'No — tabelle Oracle in MATR_USR')
FATTI.append('Componenti: store e dizionari in MATR_USR')

# ============================================================ 3. Adeguamenti database
riscrivi(par('Per l’implementazione dell’integrazione tra SIPO ed ANSC verrà creato'),
         'Le tabelle dell’integrazione fra SIPO e ANSC stanno, per ora, nello schema di '
         'stato civile MATR_USR, accanto alle tabelle degli atti. La loro struttura è '
         'quella degli script della base dati tenuti dagli sviluppatori [R25]: il presente '
         'documento ne descrive il significato e non la ripete.')
riscrivi(par('La scelta mantiene la logica del “tutto additivo”'),
         'La scelta privilegia la rapidità di realizzazione: le tabelle nuove condividono '
         'lo schema e i permessi di quelle di SIPO, e possono legarsi all’atto senza '
         'attraversare schemi. Ne discendono due differenze rispetto all’impostazione '
         'interamente additiva da cui l’analisi era partita (RNF-7): alcune tabelle '
         'esistenti ricevono colonne nuove, e per ciascun registro una tabella di '
         'estensione, in relazione uno a uno con l’atto, accoglie i dati che ANSC richiede '
         'e SIPO non ha (si veda più avanti). Parte dei dizionari e della configurazione è '
         'ereditata dal sistema Side del Comune di Milano con i nomi di origine. Se lo '
         'schema dedicato vada ripreso prima dell’esercizio è aperto (OP-104).')
riscrivi(par('Lo store di stato registra la chiave dell’atto e i discriminanti di tipo'),
         'Lo store di stato registra la chiave dell’atto e i discriminanti di tipo (evento, '
         'contenuto, operazione), e i dati prevalidati sono riletti da SIPO al momento del '
         'deposito e della firma.')
pr = par('La proposta di default non modifica alcuna tabella d’atto esistente.')
riscrivi(pr, 'La colonna «stato_ansc» sulla tabella dell’atto di morte, proposta in passato '
             'per rendere lo stato ANSC visibile nelle interrogazioni esistenti, non è fra gli '
             'script (OP-11). Gli script intervengono invece sulle tabelle di SIPO nei modi '
             'descritti di seguito.')

ogg = D.trova_tabella(d, 'Oggetto', 'Ruolo', 'Note principali')
lg = larghezze(ogg)
dopo = pr._p.getnext()
D.para(d, dopo, pezzi=[('Le estensioni delle tabelle di SIPO. ', True),
                        ('Per i dati che ANSC richiede e le maschere di SIPO non raccolgono, '
                         'gli script affiancano alla tabella ATTO di MATR_USR una tabella di '
                         'estensione per registro, in relazione uno a uno con l’atto (chiave '
                         'ID_ATTO, che è anche chiave esterna verso ATTO), e aggiungono colonne '
                         'a quattro tabelle esistenti. I dati nuovi stanno così accanto a '
                         'quelli dell’atto, dove le maschere li leggono e li scrivono; molte '
                         'colonne dichiarano in commento il percorso del modello evento che '
                         'alimentano. Il dettaglio delle colonne è negli script [R25].', False)])
D.tabella(d, dopo, [
    ('Tabella', 'Contenuto'),
    ('ATTO_NASCITA_EXTEND2', 'Registro delle nascite: riconoscimenti prenatali, stato di '
     'nascita dei genitori, coniuge e suo atto di nascita, decreto, autorità e consolato '
     'richiedenti, consenso e ente che lo rilascia, riassunto della trascrizione, '
     'certificazione consolare.'),
    ('ATTO_DECESSO_EXTEND2', 'Registro delle morti: comunicazione e testo della trascrizione, '
     'ente e nazione dell’ente.'),
    ('ATTO_MATRIMONIO_EXTEND2', 'Registro dei matrimoni: stato ANSC, identificativo ANPR '
     'dell’officiante, rito acattolico riconosciuto, identificativo ANSC del matrimonio a cui '
     'un divorzio si riferisce.'),
    ('ATTO_UNIONE_EXTEND2', 'Registro delle unioni civili: numero civico della costituzione, '
     'trascrizione dell’estinzione e del rigetto dell’opposizione, con estremi, ente, '
     'provincia e comune.'),
    ('ATTO_CITTADINANZA_EXTEND2', 'Registro della cittadinanza: decreto, giuramento e relativo '
     'verbale, tutore, richiesta e accertamento, attestazione del sindaco, apolidia, consolato '
     'e autorità mittenti, riassunto della dichiarazione.'),
    ('ATTO_DIVORZIO_EXTEND2', 'Trascrizione dei divorzi: estremi dei documenti, deposito del '
     'provvedimento, ricezione dell’atto, richiedente, testo della trascrizione, foro '
     'dell’avvocato.'),
    ('ATTO_DELEGA', 'Deleghe ricevute da un altro comune o da un consolato: data, provincia, '
     'comune, stato estero, consolato e ufficiale richiedenti, testo della delega.'),
    ('ATTO_TESTO_FORMULATO', 'Il testo dell’atto composto da SIPO — titolo, intestazione, '
     'corpo, spalla, annotazioni, firma —, una riga per atto.'),
    ('Colonne aggiunte', 'MATR_USR.ATTO.NUM_COMUNALE_ANSC, il numero comunale dell’atto in '
     'ANSC; ID_ANPR su ANAG_USR.COMUNE, ANAG_USR.PROVINCIA e ANAG_USR.CONF_STATO_ESTERO, il '
     'codice ANPR del luogo.'),
], ogg, larghezze=[lg[0], sum(lg[1:])])
D.para(d, dopo, 'Le estensioni delle tabelle di SIPO e le colonne aggiunte.', corsivo=True)
FATTI.append('Adeguamenti database: MATR_USR, estensioni *_EXTEND2 e colonne aggiunte')

# tabella «Oggetto | Ruolo | Note principali»
r = riga(ogg, 'ANSC_STATO_ATTO')
D.riscrivi_cella(r.cells[2], 'Una riga per atto (chiave ID_ATTO_SIPO): tipo evento, contenuto '
                 'e operazione, UC determinato, stato del ciclo di vita reale in ANSC '
                 '(decodifica ANSC_11, codice e descrizione), idAnsc, numero comunale, '
                 'municipio, fase della lavorazione e pagina da cui riprendere una redazione '
                 'interrotta. La supervisione è una vista su questo store.')
r = riga(ogg, 'ANSC_TEMPLATE')
D.riscrivi_cella(r.cells[0], 'ANSC_CFG_TEMPLATE')
D.riscrivi_cella(r.cells[2], 'Una riga per interrogazione, con chiave il solo codice; ANSC_CFG_UC '
                 'la richiama con COD_QUERY_UC. È un concetto distinto dalla logica di scelta, '
                 'che decide se l’UC si applica all’atto.')
r = riga(ogg, 'ANSC_SOGGETTO_IDENTIFICATIVI')
D.riscrivi_cella(r.cells[2], 'Una riga per soggetto dell’atto, con l’identificativo ANSC '
                 'ottenuto da R005, i due codici ANPR, i dati anagrafici, il ruolo nell’UC e la '
                 'traccia della ricerca.')
for c in (riga(ogg, 'Famiglia ANSC_CFG_*').cells[2],
          riga(ogg, 'DOMINIO_DECODIFICA e VALORE_DOMINIO').cells[2]):
    D.riscrivi_cella(c, c.text.replace('DDL in Appendice A', 'struttura negli script [R25]'))
for valori in (
    ('ANSC_PAYLOAD', 'Il modello evento dell’atto.', 'Una riga per atto, con la stessa chiave '
     'dello store: il modello evento intero, quando è stato generato e quando validato.'),
    ('FIRMATARI', 'I firmatari dell’atto e lo stato della firma.', 'Ereditata da Side. Una riga '
     'per soggetto firmatario (ANSC_SOGGETTO_IDENTIFICATIVI), con il tipo di firma (R006 o R012), '
     'lo stato della firma e la presa visione.'),
    ('FORZATURA_VALIDAZIONE', 'Le validazioni forzate.', 'Ereditata da Side. Il codice di '
     'forzatura usato, le anomalie superate e chi l’ha chiesto.'),
    ('SOGGETTI_EVENTO', 'Soggetti dell’atto con il loro ruolo.', 'Presente negli script, senza '
     'chiave e senza campi tecnici; le colonne ripetono in buona parte '
     'ANSC_SOGGETTO_IDENTIFICATIVI. Uso da chiarire (OP-102).'),
    ('COMUNICAZ_ANAGRAFICA_USECASE', 'La comunicazione anagrafica per UC.', 'Ereditata da Side: '
     'per ciascun UC il tipo di comunicazione anagrafica alla firma e la data di decorrenza da '
     'usare (R014).'),
    ('ANSC_CFG_VERSIONE', 'La baseline della configurazione.', 'Stati BOZZA, ATTIVA, STORICA, '
     'una sola ATTIVA. Negli script non tutta la configurazione vi è legata (OP-103).'),
    ('ANSC_CFG_DOMINIO_SIPO', 'Dove vive in SIPO un dominio di decodifica ANSC.', 'Popolata a '
     'mano; calcola la forma della decodifica che RICONCILIAZ_DIZIONARI usa.'),
    ('RICONCILIAZ_DIZIONARI', 'Corrispondenza fra valori di SIPO e valori di ANSC.', 'Per '
     'decodifica e per campo di SIPO, con validità temporale.'),
):
    D.clona_riga(ogg, valori)
FATTI.append('Elenco delle tabelle: 8 righe aggiunte, store e template corretti')

riscrivi(par('Le tabelle seguono le convenzioni di SIPO (schema dedicato ANSC_USR'),
         'Le tabelle stanno nello schema MATR_USR, con i tipi di Oracle 12.2; il tipo JSON '
         'nativo non è disponibile nella versione in uso e i modelli JSON sono CLOB. Gli '
         'identificativi sono NUMBER con sequenza o IDENTITY; le colonne temporali sono DATE, '
         'con prefisso DATA_, o TIMESTAMP, con prefisso TS_, salvo le tabelle ereditate da '
         'Side, che conservano i propri prefissi. La struttura di riferimento è quella degli '
         'script [R25]: le tabelle che seguono ne riportano le colonne e il significato, e '
         'riassumono in una riga i campi tecnici.')

# ============================================================ 4. ANSC_STATO_ATTO e ANSC_PAYLOAD
t = tab_colonna('TXT_EVENTO')
v = righe_di(t)
nuove = [('ID_ATTO_SIPO', 'NUMBER (PK)', 'Chiave dell’atto in SIPO (ID_ATTO) e chiave della '
          'tabella: una riga per atto. Negli script il vincolo si chiama PK_MATR_USR_ATTO.')]
for k in ('ID_TIPO_EVENTO', 'ID_TIPO_CONTENUTO'):
    nuove.append((k,) + v[k])
nuove.append(('COD_TIPO_OPERAZIONE', v['COD_TIPO_OPERAZIONE'][0],
              v['COD_TIPO_OPERAZIONE'][1] + ' Valore predefinito CREAZIONE.'))
for k in ('ID_UC_ANSC', 'ID_ANSC', 'COD_LOGICA', 'COD_ORIGINE_UC', 'COD_FASE', 'NUMERO_ATTO',
          'FLG_EMERGENZA', 'ID_ATTO_CARTACEO', 'ID_MOTIVO_RECUPERO', 'COD_MOTIVO_RECUPERO'):
    nuove.append((k,) + v[k])
nuove += [
    ('TS_DECORRENZA', 'TIMESTAMP', 'dataDecorrenza con ora e minuto (R014): oraDecorrenza e '
     'minutoDecorrenza si ricavano dalla colonna.'),
    ('ID_VERSIONE_ANSC',) + v['ID_VERSIONE_ANSC'],
    ('ID_STATO / STATO', 'NUMBER / VARCHAR2(100)', v['ID_STATO / STATO'][1]
     + ' Valori predefiniti 0 e BOZZA.'),
    ('FLG_SECRETATO',) + v['FLG_SECRETATO'],
    ('COD_RUOLO_OPERATORE', v['COD_RUOLO_OPERATORE'][0], v['COD_RUOLO_OPERATORE'][1]
     + ' Valore predefinito 2.'),
    ('FLG_CASA_COMUNALE', 'CHAR(1)', 'redattoNellaCasaComunale: 0/1, valore predefinito 1.'),
    ('DATA_VALIDITA_EVENTO', 'DATE', 'Data di validità dell’evento. [DA VERIFICARE: quale campo '
     'del modello evento alimenti la colonna, che non è fra i campi della testata.]'),
]
for k in ('TS_VALIDAZIONE', 'COD_PAGINA_RIPRESA', 'NUM_REVISIONE', 'COD_MUNICIPIO',
          'ULTIMO_ERRORE', 'TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD'):
    nuove.append((k,) + v[k])
D.riscrivi_sicura(t, nuove)
riscrivi(par('Indici: chiave primaria ID_STATO_ATTO'),
         'Chiave primaria ID_ATTO_SIPO: la riga si ritrova direttamente dall’atto. Il modello '
         'evento non sta in questa tabella ma in ANSC_PAYLOAD, con la stessa chiave.')
sost('La tabella lega l’atto redatto in SIPO all’atto in redazione in ANSC, ne conserva il '
     'modello evento intero e consente',
     'La tabella lega l’atto redatto in SIPO all’atto in redazione in ANSC, con ANSC_PAYLOAD '
     'ne conserva il modello evento intero e consente')

# testata del modello evento: dove si registra ciascun campo
tt = D.trova_tabella(d, 'Riga', 'Campo', 'Dove si registra')
for n, dove, nota in (
    ('11', '— nel JSON', 'Resta nel modello evento: gli script non hanno una colonna per la '
                         'data di formazione.'),
    ('12', '— derivato', 'Da dataformazione, nel modello evento.'),
    ('13', '— derivato', 'Da dataformazione, nel modello evento.'),
    ('14', '— derivato', 'Da dataformazione, nel modello evento.'),
    ('15', '— derivato', 'Da dataformazione, nel modello evento.'),
    ('16', '— derivato', 'Da dataformazione, nel modello evento.'),
    ('28', '— derivato', 'Da TS_DECORRENZA.'),
    ('29', '— derivato', 'Da TS_DECORRENZA.'),
):
    rr = riga(tt, n)
    D.riscrivi_cella(rr.cells[3], dove)
    D.riscrivi_cella(rr.cells[4], nota)
riscrivi(par('Dei trentadue campi 17 hanno una colonna'),
         'Dei trentadue campi 14 hanno una colonna in questa tabella, 8 si ricavano da altri '
         'campi, 7 restano nel modello evento e 3 sono deprecati da ANSC.')

# ANSC_PAYLOAD: sezione nuova prima di ANSC_LOG_AUDIT
audit_h = D.h(d, 3, 'ANSC_LOG_AUDIT')
D.para(d, audit_h._p, 'ANSC_PAYLOAD — il modello evento dell’atto.', stile='Heading 3')
D.para(d, audit_h._p, 'Il modello evento intero, così come è in redazione, sta in una tabella '
       'a parte con la stessa chiave dello store di stato: una riga per atto. Si riscrive a ogni '
       'salvataggio; formato l’atto coincide con ciò che è stato depositato e firmato, ed è il '
       'payload conservato di cui dicono i paragrafi precedenti. Il legame con ANSC_STATO_ATTO '
       'è per valore: gli script non dichiarano una chiave esterna.')
lt = tab_colonna('FASE')
D.tabella(d, audit_h._p, [
    ('Colonna', 'Tipo', 'Note'),
    ('ID_ATTO_SIPO', 'NUMBER (PK)', 'Chiave dell’atto in SIPO, come in ANSC_STATO_ATTO.'),
    ('TXT_PAYLOAD', 'CLOB', 'Il modello evento intero. Gli script non dichiarano il vincolo '
     '«IS JSON».'),
    ('TS_GENERAZIONE', 'TIMESTAMP', 'Quando il modello è stato costruito l’ultima volta.'),
    ('TS_VALIDAZIONE', 'TIMESTAMP', 'Quando il modello è stato validato da ANSC (R009).'),
    ('TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD', 'TIMESTAMP / VARCHAR2(40)',
     'Campi tecnici.'),
], lt, larghezze=larghezze(lt))
FATTI.append('ANSC_STATO_ATTO allineata (PK ID_ATTO_SIPO, senza TXT_EVENTO); ANSC_PAYLOAD descritta')

# il modello evento: TXT_EVENTO -> ANSC_PAYLOAD.TXT_PAYLOAD
sost('ANSC_STATO_ATTO.TXT_EVENTO: il modello evento in redazione, aggiornato a ogni salvataggio.',
     'ANSC_PAYLOAD.TXT_PAYLOAD: il modello evento in redazione, aggiornato a ogni salvataggio.')
sost('Il modello evento, in ANSC_STATO_ATTO.TXT_EVENTO.', 'Il modello evento, in '
     'ANSC_PAYLOAD.TXT_PAYLOAD.')
sost('(ANSC_STATO_ATTO.TXT_EVENTO)', '(ANSC_PAYLOAD.TXT_PAYLOAD)')
sost('il modello evento depositato (TXT_EVENTO)', 'il modello evento depositato '
     '(ANSC_PAYLOAD.TXT_PAYLOAD)')
sost('aggiorna anche, in ANSC_STATO_ATTO, il modello evento e la pagina raggiunta',
     'aggiorna anche il modello evento, in ANSC_PAYLOAD, e la pagina raggiunta, in '
     'ANSC_STATO_ATTO')
sost('ANSC_CFG_CAMPO, ANSC_CFG_FORMULA e i dizionari per le transcodifiche.',
     'ANSC_CFG_CAMPO e i dizionari per le transcodifiche.')

# ANSC_LOG_AUDIT
D.riscrivi_cella(riga(lt, 'ID_STATO_ATTO').cells[2],
                 'Riferimento all’atto. Negli script la chiave esterna punta a '
                 'MATR_USR_ATTO(ID_STATO_ATTO), che non esiste: la tabella dell’atto è '
                 'ANSC_STATO_ATTO, con chiave ID_ATTO_SIPO. Gli sviluppatori hanno previsto di '
                 'rinominare la colonna in ID_ATTO_SIPO (OP-102).')

# ALLEGATO
sost('Senza vincolo di integrità, perché nessuna chiave esterna attraversa gli schemi.',
     'Senza vincolo di integrità negli script.')

# ============================================================ 5. ANSC_SOGGETTO_IDENTIFICATIVI
t = tab_colonna('COD_ESITO_ANPR')
v = righe_di(t)
D.riscrivi_sicura(t, [
    ('ID_SOGGETTO_IDENTIFICATIVI',) + v['ID_SOGGETTO_IDENTIFICATIVI'],
    ('ID_ATTO_SIPO',) + v['ID_ATTO_SIPO'],
    ('ID_SOGGETTO_SIPO', 'NUMBER', 'Il soggetto di stato civile, MATR_USR.SOGGETTO.ID_SOGGETTO, '
     'per valore: gli script non dichiarano né chiave esterna né vincolo di unicità.'),
    ('ID_ANSC_SOGGETTO',) + v['ID_ANSC_SOGGETTO'],
    ('ID_SCHEDA_ANPR / ID_UNICO_NAZIONALE', 'VARCHAR2(50)', 'I due codici ANPR restituiti da '
     'R005, conservati accanto all’identificativo ANSC perché la base di stato civile è '
     'separata dall’anagrafe.'),
    ('NOME / COGNOME / DATA_NASCITA / SESSO / CODICE_FISCALE',
     'VARCHAR2(250) / VARCHAR2(250) / DATE / CHAR(1) / VARCHAR2(16)',
     'I dati anagrafici del soggetto, come cercati o come restituiti da R005.'),
    ('CD_SOGGETTO / TY_SOGGETTO / NM_SOGGETTO / TY_PRESENZA',
     'VARCHAR2(50) / VARCHAR2(250) / VARCHAR2(250) / VARCHAR2(20)',
     'Quale persona dell’UC è il soggetto, con i codici di SOGGETTI_USECASE.'),
    ('FG_DICHIARANTE / FG_COMPARENTE / FG_FIRMATARIO', 'CHAR(1)', 'I ruoli del soggetto '
     'nell’atto, ripresi da SOGGETTI_USECASE.'),
    ('NR_ORDINAMENTO', 'NUMBER(5)', 'Ordine di presentazione.'),
    ('COD_ESITO_RICERCA_ANSC', 'VARCHAR2(20)', v['COD_ESITO_RICERCA'][1]),
    ('COD_ESITO_ANSC', 'VARCHAR2(20)', '[DA VERIFICARE: significato. Il disegno prevedeva qui '
     'l’esito della scrittura dei codici ANPR su ANAG_USR.SOGGETTO — SCRITTO, COINCIDENTE, '
     'DISCORDANTE —; negli script la colonna si chiama COD_ESITO_ANSC.]'),
    ('TS_RICERCA / UTENTE_RICERCA',) + v['TS_RICERCA / UTENTE_RICERCA'],
    ('ID_AUDIT',) + v['ID_AUDIT'],
    ('TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD',) + v['TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD'],
])
cod = D.trova_tabella(d, 'Codice', 'Nome in ANSC', 'Dove si registra')
D.riscrivi_cella(riga(cod, 'Identificativo della scheda ANPR').cells[2],
                 'ANSC_SOGGETTO_IDENTIFICATIVI.ID_SCHEDA_ANPR; in anagrafe '
                 'ANAG_USR.SOGGETTO.ID_SCHEDA_ANPR, colonna esistente')
D.riscrivi_cella(riga(cod, 'Identificativo unico nazionale').cells[2],
                 'ANSC_SOGGETTO_IDENTIFICATIVI.ID_UNICO_NAZIONALE; in anagrafe '
                 'ANAG_USR.SOGGETTO.ID_UNICO_NAZIONALE, colonna esistente')
p = par(') oppure inserire in ANSC_SOGGETTO_IDENTIFICATIVI le informazioni.')
p.add_run(' Gli script della base dati adottano questa seconda via: i due codici stanno nella '
          'tabella. La scrittura su ANAG_USR descritta di seguito resta perciò da confermare.')
riscrivi(par('I valori restituiti da R005 restano nella risposta conservata in ANSC_LOG_AUDIT'),
         'La risposta integrale di R005 resta in ANSC_LOG_AUDIT; nella tabella si riportano '
         'gli identificativi e i dati anagrafici che servono alla lavorazione.')
FATTI.append('ANSC_SOGGETTO_IDENTIFICATIVI allineata (codici ANPR, dati anagrafici, ruoli)')

# ============================================================ 6. configurazione
t = tab_colonna('ID_UC_CFG')
v = righe_di(t)
cq = v['COD_QUERY_UC'][1]
cq = cq[cq.find('È un concetto'):] if 'È un concetto' in cq else ''
D.riscrivi_sicura(t, [
    ('ID', 'NUMBER (PK)', 'Chiave tecnica.'),
    ('ID_USECASE', 'VARCHAR2(20)', v['COD_UC_ANSC'][1] + ' Negli script si chiama ID_USECASE; '
     'lo stesso dato si chiama COD_UC_ANSC in ANSC_CFG_CAMPO e cd_usecase nelle tabelle di '
     'Side, e gli sviluppatori ne hanno previsto l’uniformazione.'),
    ('COD_MOTORE',) + v['COD_MOTORE'],
    ('DESC_UC_ANSC',) + v['DESC_UC_ANSC'],
    ('COD_FAMIGLIA',) + v['COD_FAMIGLIA'],
    ('ID_TIPO_EVENTO', 'VARCHAR2(10)', 'idTipoEvento, decodifica ANSC_01: il registro dell’UC.'),
    ('ID_TIPO_CONTENUTO',) + v['ID_TIPO_CONTENUTO'],
    ('ID_CONF_TIPO_ATTO',) + v['ID_CONF_TIPO_ATTO'],
    ('ID_TIPO_ATTO',) + v['ID_TIPO_ATTO'],
    ('STATO',) + v['STATO'],
    ('NUM_PRIORITA',) + v['NUM_PRIORITA'],
    ('LOGICA_DI_SCELTA',) + v['LOGICA_DI_SCELTA'],
    ('COD_QUERY_UC', 'VARCHAR2(50) (FK)', ('L’interrogazione da utilizzare per l’UC: chiave '
     'esterna verso ANSC_CFG_TEMPLATE, che ha per chiave il solo codice. ' + cq).strip()),
    ('ID_VERSIONE', 'NUMBER', 'Baseline di appartenenza (ANSC_CFG_VERSIONE); valore '
     'predefinito 1. Negli script non è vincolata da chiave esterna (OP-103).'),
    ('DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA',) + v['DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA'],
    ('TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD',) + v['TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD'],
])
sost('campi, formule, allegati, soggetti e interrogazioni non lo richiamano',
     'campi, allegati e soggetti non lo richiamano')
sost('con la coppia COD_UC_ANSC e ID_VERSIONE: il codice pubblicato da ANSC è ciò che le righe '
     'dello stesso UC hanno in comune.',
     'con il codice pubblicato da ANSC — ID_USECASE in questa tabella, COD_UC_ANSC in '
     'ANSC_CFG_CAMPO, cd_usecase nelle tabelle di Side —, che è ciò che le righe dello stesso '
     'UC hanno in comune.')

t = tab_colonna('ALIAS_CAMPO_SIPO')
v = righe_di(t)
righe = []
for k in v:
    if k == 'ID_VERSIONE':
        continue
    if k == 'COD_UC_ANSC':
        righe.append((k, v[k][0], 'Codice dell’UC pubblicato da ANSC: richiama '
                      'ANSC_CFG_UC.ID_USECASE per valore, come ALLEGATI_USECASE e '
                      'SOGGETTI_USECASE. Negli script la riga non porta la baseline (OP-103).'))
        continue
    righe.append((k,) + v[k])
    if k == 'OPERATIVO':
        righe.append(('VALORE_DEFAULT', 'VARCHAR2(200)', 'Valore predefinito del campo, quando '
                      'SIPO non lo fornisce.'))
D.riscrivi_sicura(t, righe)

t = tab_colonna('QUERY_UC')
D.riscrivi_cella(riga(t, 'COD_QUERY_UC').cells[1], 'VARCHAR2(50) (PK)')
D.riscrivi_cella(riga(t, 'COD_QUERY_UC').cells[2], 'Codice dell’interrogazione e chiave della '
                 'tabella: è il valore che ANSC_CFG_UC.COD_QUERY_UC richiama.')
riscrivi(par('La tabella appartiene alla baseline: alla creazione di una nuova versione le '
             'interrogazioni'),
         'Negli script la tabella non porta la baseline: un’interrogazione vale per codice in '
         'tutte le versioni della configurazione, e una sua modifica vale anche per le baseline '
         'storiche (OP-103).')
FATTI.append('ANSC_CFG_UC, ANSC_CFG_CAMPO, ANSC_CFG_TEMPLATE allineate')

# ANSC_CFG_FORMULA: non è negli script
pf = par('ANSC_CFG_FORMULA — le diciture previste dall’UC.')
tf = pf._p.getnext()
assert tf.tag == qn('w:tbl')
togli(tf)
togli(pf._p)
p = par('Lo stesso tracciato dichiara, accanto a sezioni e allegati, una terza categoria')
p.add_run(' Gli script della base dati non comprendono una tabella delle formule: la '
          'configurazione per UC proposta nelle versioni precedenti (ANSC_CFG_FORMULA) non è '
          'realizzata, e il punto resta aperto (OP-51).')
sost('SOGGETTI_USECASE e ANSC_CFG_FORMULA — perché', 'SOGGETTI_USECASE — perché')
p = par('Della fascia intermedia va notato che cosa vi stia dentro')
p.add_run(' Negli script della base dati, però, ANSC_CFG_TEMPLATE e ANSC_CFG_CAMPO non '
          'portano la baseline (OP-103).')
sost('ANSC_CFG_CAMPO, ALLEGATI_USECASE e ANSC_CFG_FORMULA per singolo UC: come ogni dato è '
     'noto in SIPO e se va inviato, quali documenti servono e quali diciture sono previste.',
     'ANSC_CFG_CAMPO e ALLEGATI_USECASE per singolo UC: come ogni dato è noto in SIPO e se va '
     'inviato e quali documenti servono.')
FATTI.append('ANSC_CFG_FORMULA tolta (non negli script), OP-51 riformulato')

# ============================================================ 7. dizionari
t = tab_colonna('cd_versione')
D.riscrivi_sicura(t, [
    ('id_dominio',) + righe_di(t)['id_dominio'],
    ('nm_dominio',) + righe_di(t)['nm_dominio'],
    ('id_versione', 'NUMBER', 'Versione della tabella dichiarata da ANSC nell’elenco di R901. '
     'Negli script la colonna è numerica, mentre R901 restituisce una stringa del tipo '
     '«1.4.0», che non vi entra (OP-102).'),
])
t = tab_colonna('tx_attributi')
v = righe_di(t)
D.riscrivi_sicura(t, [
    ('id_dominio', 'NUMBER(10) (PK)', 'Decodifica di appartenenza. Negli script la chiave è '
     '(id_dominio, id_valore), senza nm_dominio e senza chiave esterna verso '
     'DOMINIO_DECODIFICA: le due decodifiche che condividono l’identificativo (ANSC_134 e '
     'ANSC_135) non si possono caricare entrambe (OP-102).'),
    ('id_valore',) + v['id_valore'],
    ('ds_valore',) + v['ds_valore'],
    ('dt_inizio_validita / dt_fine_validita',) + v['dt_inizio_validita / dt_fine_validita'],
    ('nr_ordinamento', 'NUMBER(10)', v['nr_ordinamento'][1]),
    ('cd_valore', 'VARCHAR2(10)', 'Presente negli script. Il tracciato di R901 ha un solo '
     'identificativo per riga. [DA VERIFICARE: con che cosa si valorizza.]'),
])
riscrivi(par('Una nota sui nomi dei vincoli, che vale come avvertenza generale'),
         'Negli script VALORE_DOMINIO non dichiara una chiave esterna verso DOMINIO_DECODIFICA: '
         'il legame è per valore, sull’identificativo della decodifica.')
sost('Il DDL completo è in Appendice A.', 'La vista non è ancora fra gli script della base '
     'dati [R25].')
riscrivi(par('Il confronto fra ciò che il servizio dà e ciò che il modello prevedeva'),
         'Il confronto fra ciò che il servizio dà e ciò che il modello prevede porta tre '
         'osservazioni. cd_valore, che gli script conservano, non ha fonte nel tracciato di '
         'R901. La versione della tabella va conservata, perché è l’appiglio che rende '
         'l’intercetto delle revisioni una sola chiamata leggera invece di centoquarantacinque '
         'scarichi. Le colonne in più che due tabelle portano (il tipo di contenuto dei casi '
         'd’uso, il codice del consolato) non hanno una colonna negli script.')

t = tab_colonna('ID_RICONCILIAZIONE')
v = righe_di(t)
D.riscrivi_sicura(t, [
    ('ID_RICONCILIAZIONE',) + v['ID_RICONCILIAZIONE'],
    ('ID_VERSIONE',) + v['ID_VERSIONE'],
    ('DECODIFICA', 'VARCHAR2(100)', v['DECODIFICA'][1]),
    ('VALORE_SIPO / DESCRIZIONE_SIPO',) + v['VALORE_SIPO / DESCRIZIONE_SIPO'],
    ('VALORE_ANSC / DESCRIZIONE_ANSC',) + v['VALORE_ANSC / DESCRIZIONE_ANSC'],
    ('CONDIZIONE', 'VARCHAR2(1000)', 'Presente negli script. Il disegno l’aveva tolta: una '
     'traduzione che dipende dal contesto si esprime con una riga per contesto. [DA VERIFICARE '
     'con gli sviluppatori: uso previsto.]'),
    ('ID_DOMINIO_SIPO', 'NUMBER', 'Il dominio in ANSC_CFG_DOMINIO_SIPO, per chiave; gli script '
     'non dichiarano la chiave esterna.'),
    ('SCHEMA_SIPO / TABELLA_SIPO / CAMPO_SIPO', 'VARCHAR2(30)', 'Dove sta in SIPO il valore '
     'locale (si veda più avanti).'),
    ('DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA',) + v['DATA_INIZIO_VALIDITA / DATA_FINE_VALIDITA'],
    ('TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD',) + v['TS_INS / TS_UPD / UTENTE_INS / UTENTE_UPD'],
])
riscrivi(par('Vincolo di unicità su (ID_VERSIONE, DECODIFICA, VALORE_ANSC'),
         'Gli script non dichiarano un vincolo di unicità, ma un indice su (DECODIFICA, '
         'VALORE_SIPO): che a ciascun valore ammesso da ANSC corrisponda un solo valore locale, '
         'dentro una baseline, per un campo e per un periodo, lo controlla quindi '
         'l’applicazione. Né VALORE_ANSC né VALORE_SIPO sono obbligatorie: resta '
         'rappresentabile la riga «questo valore di ANSC non ha ancora corrispondente», che è '
         'il lavoro che la pagina di riconciliazione mostra.')
FATTI.append('Dizionari: DOMINIO_DECODIFICA, VALORE_DOMINIO, RICONCILIAZ_DIZIONARI allineate')

# ============================================================ 8. numerazione
t = tab_colonna('num_atto')
v = righe_di(t)
D.riscrivi_sicura(t, [
    ('id_anno_documento', v['id_anno_documento'][0], v['id_anno_documento'][1]
     + ' Gli script creano la riga del 2026 insieme alla tabella.'),
    ('pg_atto', 'NUMBER(6)', v['num_atto'][1].replace('num_atto', 'pg_atto')),
    ('dt_inserimento', 'TIMESTAMP', v['ts_inserimento'][1]),
    ('dt_aggiornamento', 'TIMESTAMP', v['ts_aggiornamento'][1]),
])
sost('num_atto', 'pg_atto', attese=5)   # 3 nel testo, 2 nella DDL dell'App. A che si toglie
FATTI.append('NUMERATORE_COMUNALE con i nomi di Side degli script (pg_atto, dt_*)')

# ============================================================ 9. altri ritocchi sullo schema
sost('La configurazione risiede nelle tabelle ANSC_CFG_UC e ANSC_CFG_CAMPO di ANSC_USR',
     'La configurazione risiede nelle tabelle ANSC_CFG_UC e ANSC_CFG_CAMPO di MATR_USR')
sost('i dizionari ANSC sono esposti da ANSC_USR attraverso la vista di sola lettura',
     'i dizionari ANSC sono esposti attraverso la vista di sola lettura')
sost('Il legame con lo store dell’atto, che sta in ANSC_USR, attraversa gli schemi e va '
     'dichiarato come tale.',
     'Lo store dell’atto sta nello stesso schema, e il legame può essere una chiave esterna.')
sost('raggiunge ANSC_USR.', 'raggiunge MATR_USR.')
# rimando orfano: PC-3 non esiste più, la frase sta dentro PC-5
sost('chiude gli esiti indeterminati (PC-3) e ripristina', 'chiude gli esiti indeterminati e '
     'ripristina')

# ============================================================ 10. ERD
D.sostituisci_immagine(d, 'Schema ANSC_USR, con ALLEGATO', ERD)
riscrivi(par('Schema ANSC_USR, con ALLEGATO'),
         'Le tabelle dell’integrazione nello schema MATR_USR. Le frecce piene sono le chiavi '
         'esterne dichiarate negli script della base dati [R25]; le tratteggiate sono '
         'riferimenti per valore, senza vincolo di integrità. Le estensioni delle tabelle '
         'd’atto di SIPO non sono rappresentate.')
FATTI.append('ERD rigenerato dagli script')

# ============================================================ 11. versionamento
hv = D.h(d, 1, 'Il versionamento della configurazione')
pv = hv._p.getnext()
D.para(d, pv, pezzi=[('Lo stato nella base dati. ', True), (
    'Il capitolo descrive la baseline come è stata disegnata. Negli script della base dati '
    '[R25] è presente solo in parte: ANSC_CFG_VERSIONE esiste, ma ANSC_CFG_CAMPO e '
    'ANSC_CFG_TEMPLATE non ne portano il riferimento, ANSC_CFG_UC lo porta senza chiave '
    'esterna, e le note degli sviluppatori prevedono di toglierlo anche da ALLEGATI_USECASE e '
    'SOGGETTI_USECASE e valutano di eliminare ANSC_CFG_VERSIONE. Se la direzione è confermata, '
    'la copia integrale descritta di seguito non è realizzabile e il capitolo va riscritto; la '
    'decisione è in OP-103.', False)])
FATTI.append('Versionamento: paragrafo sullo stato nella base dati (OP-103)')

# ============================================================ 12. Open point
REG = D.trova_tabella(d, '#', 'Tema', 'Questione', 'Stato', 'Owner', 'Priorità')
D.riscrivi_cella(riga(REG, 'OP-51').cells[2],
                 'Gli script della base dati non comprendono una tabella delle formule: la '
                 'configurazione per UC proposta nelle versioni precedenti (ANSC_CFG_FORMULA) '
                 'non è realizzata. ANSC non pubblica i testi: le decodifiche ANSC_119 e '
                 'ANSC_120 contengono numeri di formula per il caso secretato e non secretato, '
                 'non le diciture. Resta da stabilire se le formule si configurino in SIPO, chi '
                 'trascriva i 233 testi dalla normativa e li tenga allineati, visto che '
                 'concorrono alla composizione dell’atto.')
for valori in (
    ('OP-102', 'Difetti degli script della base dati',
     'Il confronto con gli script [R25] mostra punti da correggere prima dell’esercizio. '
     '(a) Le CREATE di ANSC_CFG_UC e di ANSC_CFG_DOMINIO_SIPO non chiudono la parentesi della '
     'tabella. (b) Le chiavi esterne di ANSC_LOG_AUDIT e di FORZATURA_VALIDAZIONE puntano a '
     'MATR_USR_ATTO(ID_STATO_ATTO), che non esiste; il trigger TRG_MATR_USR_ATTO_BU è '
     'dichiarato sulla stessa tabella inesistente. La tabella dell’atto è ANSC_STATO_ATTO, con '
     'chiave ID_ATTO_SIPO, e le note degli sviluppatori prevedono già la rinomina delle '
     'colonne. (c) VALORE_DOMINIO ha la chiave (id_dominio, id_valore) senza nm_dominio: '
     'ANSC_134 e ANSC_135 non si possono caricare entrambe. (d) DOMINIO_DECODIFICA.ID_VERSIONE '
     'è numerica, la versione dichiarata da R901 è una stringa. (e) SOGGETTI_EVENTO non ha '
     'chiave né campi tecnici e ripete ANSC_SOGGETTO_IDENTIFICATIVI: uso da chiarire. '
     '(f) FIRMATARI ha chiave sul solo ID_SOGGETTO_IDENTIFICATIVI. (g) Lo stesso codice '
     'dell’UC ha tre nomi (ID_USECASE, COD_UC_ANSC, CD_USECASE). (h) In '
     'ATTO_DECESSO_EXTEND2 TESTO_TRASCR_MORTE è una DATE; in ATTO_MATRIMONIO_EXTEND2 il '
     'commento del rito cita ANSC_10, che è la decodifica dei formati degli allegati. '
     '(i) Diversi vincoli hanno nomi di sistema (SYS_C…) o senza prefisso, contro [R5].',
     'Aperto', 'Sviluppo / Base dati', 'Alta'),
    ('OP-103', 'Baseline della configurazione',
     'Negli script ANSC_CFG_CAMPO e ANSC_CFG_TEMPLATE non portano ID_VERSIONE, ANSC_CFG_UC la '
     'porta senza chiave esterna, e le note degli sviluppatori prevedono di toglierla da '
     'ALLEGATI_USECASE e SOGGETTI_USECASE e valutano di eliminare ANSC_CFG_VERSIONE. Il '
     'capitolo «Il versionamento della configurazione» descrive invece una baseline per copia '
     'integrale. Va deciso se il versionamento resta, e allora la base dati va completata, o '
     'si abbandona, e allora il capitolo si riscrive con il modo in cui si recepiscono le '
     'revisioni del mapping di ANSC.', 'Aperto', 'Comune / Sviluppo', 'Alta'),
    ('OP-104', 'Schema delle tabelle dell’integrazione',
     'Le tabelle stanno, per ora, in MATR_USR. Va confermato prima dell’esercizio, con le '
     'conseguenze sui permessi del componente, sul salvataggio e sul ripristino dello schema '
     'di stato civile, e sulla separazione fra la parte operativa e la parte dei dizionari.',
     'Aperto', 'Comune / Base dati', 'Media'),
    ('OP-105', 'Tabelle progettate e non ancora negli script',
     'I documenti di dettaglio progettano tabelle che gli script non contengono ancora: '
     'ANSC_SOGGETTO_ATTO [R18], ANSC_ANNOTAZIONE e ANSC_ANNOTAZIONE_CORREZIONE [R19], '
     'ANSC_CERTIFICATO [R20]; manca anche la vista V_ANSC_DIZ_VALIDO. Vanno create o '
     'dichiarate superate.', 'Aperto', 'Analisi / Sviluppo', 'Media'),
):
    D.clona_riga(REG, valori)
FATTI.append('OP-51 riformulato; OP-102…OP-105 nuovi')

# ============================================================ 13. Appendice A
hA = D.h(d, 1, 'Appendice A')
hB = D.h(d, 1, 'Appendice B')
D.testo_di(hA, 'Appendice A — Le tabelle della base dati')
corpo = list(d.element.body.iterchildren())
ia, ib = corpo.index(hA._p), corpo.index(hB._p)
da_togliere = corpo[ia + 1:ib]
idiz = next(i for i, e in enumerate(da_togliere)
            if e.tag == qn('w:p') and Paragraph(e, d).text.strip() == 'Tabelle dei dizionari')

D.para(d, hB._p, 'La struttura delle tabelle non è riportata in questo documento: fa fede '
       'quella degli script della base dati [R25], tenuti dagli sviluppatori e ordinati per '
       'specie di oggetto — creazione delle tabelle, modifiche alle tabelle esistenti, trigger, '
       'viste, indici, dati iniziali e aggiornamenti. Il significato delle tabelle è descritto '
       'nel capitolo «Adeguamenti database» e nei capitoli che le usano. Il confronto fra gli '
       'script e il documento si ripete a ogni nuova consegna degli script.')
D.para(d, hB._p, 'Le tabelle stanno, per ora, nello schema MATR_USR, e si raggruppano come '
       'segue.')
gruppi = D.tabella(d, hB._p, [
    ('Raggruppamento', 'Tabelle'),
    ('Operative — l’atto e la sua lavorazione', 'ANSC_STATO_ATTO, ANSC_PAYLOAD, ANSC_LOG_AUDIT, '
     'ALLEGATO, FIRMATARI, FORZATURA_VALIDAZIONE, ANSC_SOGGETTO_IDENTIFICATIVI, SOGGETTI_EVENTO'),
    ('Flusso in ingresso', 'ANSC_NOTIFICA'),
    ('Configurazione', 'ANSC_CFG_VERSIONE, ANSC_CFG_UC, ANSC_CFG_TEMPLATE, ANSC_CFG_CAMPO, '
     'ALLEGATI_USECASE, SOGGETTI_USECASE, COMUNICAZ_ANAGRAFICA_USECASE'),
    ('Dizionari', 'DOMINIO_DECODIFICA, VALORE_DOMINIO, ANSC_CFG_DOMINIO_SIPO, '
     'RICONCILIAZ_DIZIONARI'),
    ('Numerazione comunale', 'NUMERATORE_COMUNALE, PRENOTAZIONE_ATTI, DATI_ATTO_ESTERNO'),
    ('Estensioni delle tabelle di SIPO', 'ATTO_NASCITA_EXTEND2, ATTO_DECESSO_EXTEND2, '
     'ATTO_MATRIMONIO_EXTEND2, ATTO_UNIONE_EXTEND2, ATTO_CITTADINANZA_EXTEND2, '
     'ATTO_DIVORZIO_EXTEND2, ATTO_DELEGA, ATTO_TESTO_FORMULATO; colonne aggiunte ad ATTO, '
     'COMUNE, PROVINCIA e CONF_STATO_ESTERO'),
    ('Altri oggetti', 'Trigger TRG_MATR_USR_ATTO_BU; viste ATTI_PER_TIPOATTO e V_CONF_TIPI_ATTO'),
    ('Previste e non ancora negli script', 'ANSC_SOGGETTO_ATTO [R18], ANSC_ANNOTAZIONE e '
     'ANSC_ANNOTAZIONE_CORREZIONE [R19], ANSC_CERTIFICATO [R20]; vista V_ANSC_DIZ_VALIDO '
     '(OP-105)'),
], ogg, larghezze=[lg[0], sum(lg[1:])])
D.para(d, hB._p, 'Il raggruppamento logico delle tabelle della base dati.', corsivo=True)

# le ancore di commento dell'appendice si spostano sulla riga del gruppo che nomina le tabelle
cella_oper = gruppi.rows[1].cells[1].paragraphs[0]._p
cella_diz = gruppi.rows[4].cells[1].paragraphs[0]._p
for i, e in enumerate(da_togliere):
    dest = cella_diz if i > idiz else cella_oper
    for pe in ([e] if e.tag == qn('w:p') else list(e.iter(qn('w:p')))):
        if D.ha_commenti(pe):
            D.sposta_commenti(pe, dest)
for e in da_togliere:
    togli(e)
FATTI.append('Appendice A: senza DDL, descrizione e raggruppamento; 4 ancore spostate')

# ============================================================ 14. testata e storia
for fatto in D.frontespizio(d, '3.63', 'ANALISI_Integrazione-ANSC_v3.63') or []:
    FATTI.append(str(fatto))
for sez in d.sections:
    for tb in sez.header.tables:
        for rr in tb.rows:
            for c in rr.cells:
                if c.text.strip() == 'Versione 3.62':
                    D.riscrivi_cella(c, 'Versione 3.63')
D.storia(d, DATA, '3.63',
         'Riferimenti · Glossario · Componenti · Adeguamenti database · Configurazione · '
         'Dizionari · Numerazione comunale · Versionamento · Open Point · Appendice A',
         'Allineamento agli script della base dati di collaudo [R25], che fanno fede: tabelle '
         'in MATR_USR, estensioni delle tabelle d’atto di SIPO, tabelle descrittive e ERD '
         'riallineati, ANSC_PAYLOAD descritta, ANSC_CFG_FORMULA tolta. L’Appendice A non '
         'riporta più la DDL ma il raggruppamento delle tabelle. OP-102…OP-105.')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE, 'ancore perse'
d.save(OUT)
for f in FATTI:
    print('  ' + f)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
