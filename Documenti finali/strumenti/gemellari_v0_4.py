# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v0.4 (21/11/2026), dal FILE REALE della v0.3.

Che cosa cambia (approfondimento dell'utente sulle issue ANSC, 21/11/2026):
  * i due percorsi non sono più alternative in attesa di Sogei: li decide il parto. Gemelli con lo
    stesso UC → caso 1, tutto da SIPO tramite servizi cooperativi (la prenotazione porta l'UC
    specifico, le bozze si completano con quello: issue #571); gemelli con UC diversi → caso 2,
    caso d'uso di servizio con la tipologia di nascita, solo sulla web app (#3333, #3399), con
    ritorno in SIPO;
  * caso 2 (decisioni dell'utente): pratica completa in SIPO, numeri staccati tutti insieme dopo la
    divisione (DATI PER ANSC), un solo recupero per l'intero parto (RECUPERA GEMELLI) e DEFINISCI
    GEMELLI, nessuna importazione;
  * tabella nuova ANSC_SOGGETTO_ATTO, a parte da ATTI_GEMELLARI: il soggetto e il suo atto ANSC,
    valida anche fuori dai gemelli (il nato ha una riga in SOGGETTO solo dopo la definizione);
  * diagrammi rifatti (diagrammi_gemellari_v0_4_pptx.py), due schermate nuove
    (schermate_gemellari_v0_4.py); GE-01/03/04 riformulati, GE-15…GE-18; [A9]…[A12].

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_4.py
"""
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches
from docx.text.paragraph import Paragraph

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import par, tabella, voce               # noqa: E402
from gemellari_v0_2 import (codice, figura, heading, in_coda, para_che_inizia,  # noqa: E402
                            sposta_prima, tabella_che_contiene)

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.3.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.4.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '21/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')
LARGO = 6.3


def png(nome):
    return os.path.join(IMG, nome)


# ------------------------------------------------------------------ primitive locali
def e_heading(e, livello=None):
    if e.tag != qn('w:p'):
        return False
    st = e.find(qn('w:pPr') + '/' + qn('w:pStyle'))
    if st is None:
        return False
    v = st.get(qn('w:val'))
    return v.startswith('Heading') and (livello is None or v == 'Heading%d' % livello)


def togli_fino(da, a_escluso):
    """Toglie gli elementi da `da` (compreso) ad `a_escluso` (escluso); nessun commento perso."""
    e, via = da, []
    while e is not None and e is not a_escluso:
        via.append(e)
        e = e.getnext()
    assert e is a_escluso, 'ancora non trovata'
    for x in via:
        assert not D.ha_commenti(x)
        x.getparent().remove(x)
    return len(via)


def rifai_voce(d, vecchio, testa, corpo):
    racc = in_coda(d)
    voce(d, testa, corpo)
    sposta_prima(racc(), vecchio._p)
    assert not D.ha_commenti(vecchio._p)
    vecchio._p.getparent().remove(vecchio._p)


def didascalia(d, inizio):
    trovati = [p for p in d.paragraphs
               if re.match(r'Figura \d+ – ' + re.escape(inizio), p.text.strip())]
    assert len(trovati) == 1, (inizio, len(trovati))
    return trovati[0]


def sostituisci_figura(d, inizio, file_png, pollici, nuova):
    cap = didascalia(d, inizio)
    e = cap._p.getprevious()
    while e.tag != qn('w:p') or not e.findall('.//' + qn('pic:pic')):
        e = e.getprevious()
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(file_png, width=Inches(pollici))
    e.addprevious(p._p)
    e.getparent().remove(e)
    num = re.match(r'Figura \d+ – ', cap.text).group(0)
    D.testo_di(cap, num + nuova)


def riga_di(t, primo):
    trovate = [r for r in t.rows if r.cells[0].text.strip() == primo]
    assert len(trovate) == 1, (primo, len(trovate))
    return trovate[0]


def sostituisci_nei_run(d, vecchio, nuovo, esclusa=None):
    """Sostituzione dentro i singoli run, che conserva grassetti e corsivi."""
    n = 0
    tabelle = [t for t in d.tables if esclusa is None or t._tbl is not esclusa._tbl]
    paragrafi = list(d.paragraphs) + [p for t in tabelle for r in t.rows for c in r.cells
                                      for p in c.paragraphs]
    for p in paragrafi:
        for r in p.runs:
            if vecchio in r.text:
                n += r.text.count(vecchio)
                r.text = r.text.replace(vecchio, nuovo)
    return n


# ------------------------------------------------------------------ contenuti
RIF_NUOVI = [
    ['[A9]', 'github.com/italia/ansc, issue #571 «Prenotazione Evento — Richiesta Informazioni» '
     '(risposte ANSC del 22/12/2023, 10/01/2024 e 31/01/2025) e #611 «Prenotazione evento per '
     'gemelli non nati vivi» (16/01/2024): tramite servizi cooperativi la prenotazione porta l’UC '
     'specifico e le bozze si completano con quello, la web app usa il caso d’uso di servizio; il '
     'numero dei gemelli comprende i nati morti.', 'Segnalazioni ANSC'],
    ['[A10]', 'github.com/italia/ansc, issue #3333 «Parto plurimo con casi d’uso diversi» e #3399 '
     '(risposte ANSC del 10/06/2026): per i gemelli con casi d’uso diversi il caso d’uso di '
     'servizio, con la tipologia di nascita nei dati generali; correzione degli atti già formati '
     'con l’art. 98.', 'Segnalazioni ANSC'],
    ['[A11]', 'github.com/italia/ansc, issue #3380 «Gemelli con casi d’uso diversi» (aperta dal '
     '12/05/2026, «in analisi», senza risposta ANSC al 21/11/2026) e #3240 (associazione di atti '
     'di un parto gemellare formati come parti singoli, aperta).', 'Segnalazioni ANSC'],
    ['[A12]', 'github.com/italia/ansc, issue #2299 (25/11/2025: le bozze prenotate da gestionale '
     'non hanno composizione, che arriva con la validazione) e #1858 (02/09/2025: un atto formato '
     'fuori dalle bozze prenotate va registrato «partendo dalla bozza»).', 'Segnalazioni ANSC'],
]

SINTESI = [
    ('Due casi, decisi dallo stato dei nati.',
     'La prenotazione accetta un solo caso d’uso e le bozze si completano con quello. Se tutti i '
     'gemelli hanno lo stesso UC (tutti nati vivi, tutti nati morti o tutti nati vivi e poi '
     'deceduti) tramite servizi cooperativi si prenota con l’UC specifico e ciascuna bozza si '
     'completa da SIPO: è il caso 1 [A9]. Se gli UC sono diversi ANSC indica il caso d’uso di '
     'servizio, con la tipologia di nascita nei dati generali [A10], che dal 9 settembre 2024 si '
     'usa solo sulla web app [A7]: gli atti si formano lì e rientrano in SIPO con un solo recupero '
     'per l’intero parto. È il caso 2.'),
    ('Che cosa resta in SIPO nel caso 2.',
     'La pratica completa, la divisione e lo stacco in blocco dei numeri comunali; la pagina «Dati '
     'per ANSC» del parto; RECUPERA GEMELLI, che ritrova gli atti per numero comunale e li abbina '
     'ai nati, e DEFINISCI GEMELLI. Nessun dato si importa da ANSC.'),
    ('Il soggetto e il suo atto ANSC.',
     'Una tabella nuova, ANSC_SOGGETTO_ATTO, registra per ciascun nato l’atto ANSC che lo ha per '
     'intestatario: alla prenotazione nel caso 1, al recupero nel caso 2. Vale anche fuori dal '
     'parto plurimo.'),
    ('Che cosa resta aperto.',
     'Con quale campo la validazione riconosca la bozza prenotata (GE-02), l’atto di morte e '
     'l’anagrafe del nato vivo e poi deceduto (GE-05, GE-06), la risposta di ANSC alla '
     'segnalazione ancora aperta sui gemelli con casi d’uso diversi (GE-04) e i controlli '
     'dell’abbinamento al recupero (GE-18).'),
]

CASI = [
    ['Caso', 'Quando', 'Che cosa dice ANSC', 'Canale', 'Fonte'],
    ['1 — stesso UC', 'Tutti i gemelli nati vivi, tutti nati morti o tutti nati vivi e poi '
     'deceduti. Filiazione, termine e dichiarante sono del parto, quindi lo stesso stato dà lo '
     'stesso UC.', 'Si prenota con l’UC specifico; ciascuna bozza si completa con lo stesso UC; non '
     'si cambia il numero comunale e non si registrano UC «ex novo». Il numero dei gemelli è il '
     'totale, nati morti compresi.', 'Servizi cooperativi: R009 prenotazione e validazione, R006, '
     'R007.', '[A9]'],
    ['2 — UC diversi', 'Almeno un gemello in uno stato diverso dagli altri, per esempio un nato '
     'vivo e un nato morto; oppure uno stato per cui il gruppo di UC non ha una variante.',
     'Caso d’uso di servizio, specificando la tipologia di nascita nei dati generali. Gli atti già '
     'formati in modo diverso si correggono con l’art. 98.', 'Solo web app: il caso d’uso di '
     'servizio non è disponibile tramite servizi cooperativi dal 9 settembre 2024.',
     '[A10], [A7], [A9]'],
]

PASSI = [
    ['#', 'Passo del percorso ANSC', 'Caso 1 — stesso UC', 'Caso 2 — UC diversi'],
    ['1', 'Prenotazione: ANSC crea un atto in bozza per ciascun gemello e ne restituisce '
          'l’identificativo nazionale.',
     'R009 /prenota/evento tramite servizi cooperativi, con l’UC comune.',
     'Web app, con il caso d’uso di servizio [A9].'],
    ['2', 'Completamento di ciascun atto: dati, composizione con le formule e gli identificativi '
          'dei fratelli, validazione.',
     'R009 /validazione/evento sulla bozza, con lo stesso UC.',
     'Web app: il caso 11999999 «non è più disponibile tramite servizi cooperativi» [A7].'],
    ['3', 'Firma dei dichiaranti, solo cartacea, acquisita come processo verbale [A3].',
     'R006.', 'Web app.'],
    ['4', 'Firma dell’USC; poi si passa all’atto del gemello successivo [A3].',
     'R007.', 'Web app.'],
]

PASSI_2 = [
    ['#', 'Dove', 'Che cosa succede', 'Servizi', 'Esito'],
    ['1', 'SIPO, compilazione e riepilogo', 'Come oggi: pratica unica con i due flag per ciascun '
     'nato, poi divisione.', 'nascita-be, /performAttiPlurigemellari', 'N atti legati da '
     'ID_LAVORAZIONE_PADRE.'],
    ['2', 'SIPO, riepilogo del gemello 1', 'Gli UC dei nati differiscono: PRENOTA GEMELLI non '
     'compare; un avviso indica la web app e il pulsante DATI PER ANSC.',
     'all-ansc-sipo (configurazione)', '—'],
    ['3', 'SIPO, DATI PER ANSC', 'N numeri comunali consecutivi in una sola richiesta; nascono le '
     'righe dello store dei gemelli 2…N, tutte in attesa della web app; N righe in '
     'ATTI_GEMELLARI.', 'be-numeratore-comunale POST /richiesta', 'N righe nello store con '
     'NUMERO_ATTO, WA · ATTESA WEBAPP.'],
    ['4', 'SIPO, pagina «Dati per ANSC» del parto', 'Per ciascun nato: posizione, numero comunale, '
     'stato e tipologia di nascita, dati da riportare, testo da copiare.', '—', '—'],
    ['5', 'Web app ANSC', 'Prenotazione dei parti gemellari con il numero totale dei gemelli e i '
     'numeri comunali di SIPO nell’ordine di nascita; completamento di ciascuna bozza con il caso '
     'd’uso di servizio, la tipologia di nascita nei dati generali e la composizione con le formule '
     'e gli identificativi dei fratelli; firme; un gemello alla volta.', '—',
     'N atti 5 FIRMATO DA USC in ANSC.'],
    ['6', 'SIPO, RECUPERA GEMELLI (gemello 1)', 'Per ciascun numero comunale del parto, ricerca '
     'dell’atto; controlli di abbinamento; esito per gemello.', 'R005 /consultazione',
     'idAnsc sulle righe abbinate; righe in ANSC_SOGGETTO_ATTO.'],
    ['7', 'SIPO, DEFINISCI GEMELLI', 'Solo se tutti i gemelli sono abbinati: definizione di '
     'ciascun atto, come oggi una /finalizzaAtto per gemello.', '/finalizzaAtto',
     'N atti 2 DEFINITO.'],
]

REGOLE_2 = [
    ('DATI PER ANSC.', 'Compare al posto di PRENOTA GEMELLI, solo sul gemello 1 e solo quando gli '
     'UC dei nati differiscono. I numeri si staccano tutti alla prima apertura e non si '
     'ristaccano: riaprendo la pagina si rivedono gli stessi. Dopo lo stacco, l’annullamento della '
     'divisione scarta i numeri (GE-09).'),
    ('Numeri sulla web app.', 'La web app chiede il numero dei gemelli e il numero comunale di '
     'ciascuno; l’ufficiale riporta quelli di SIPO nell’ordine di nascita. La web app propone un '
     'proprio numero e dichiara cinque caratteri, mentre la serie di SIPO ne ha sei: è lo stesso '
     'tema degli atti formati sulla web app [R2] (GE-15).'),
    ('Tipologia di nascita.', 'In ciascuna bozza va indicata nei dati generali la tipologia del '
     'nato (decodifica ANSC_107: 1 nato vivo, 2 nato morto, 3 nato vivo e poi deceduto) [A10]. La '
     'pagina la mostra già tradotta dai due flag di SIPO.'),
    ('RECUPERA GEMELLI.', 'Un solo comando per il parto, sul gemello 1. Per ciascun numero comunale '
     'cerca l’atto con R005, nell’anno e per il Comune, e lo abbina al gemello che porta quel '
     'numero. I controlli: il numero comunale contenuto nell’identificativo nazionale; lo stato 5 '
     'FIRMATO DA USC; il caso d’uso di servizio delle nascite; l’intestatario (sesso, data e ora di '
     'nascita) e la tipologia di nascita uguali a quelli del nato in SIPO; il numero degli atti '
     'trovati uguale a quello dei gemelli. Il comando si può ripetere: i gemelli già abbinati non '
     'si ricercano.'),
    ('Esiti.', 'ABBINATO; NON TROVATO (nessun atto con quel numero: la web app non è ancora '
     'completata, o è stato usato un altro numero); NON FIRMATO (atto trovato ma non ancora nello '
     'stato 5); INCOERENTE (atto trovato ma con intestatario o tipologia diversi dal nato in SIPO: '
     'nessuna scrittura, lo risolve l’ufficiale). Solo ABBINATO scrive sullo store e su '
     'ANSC_SOGGETTO_ATTO.'),
    ('DEFINISCI GEMELLI.', 'Attivo solo quando tutti i gemelli sono abbinati, perché in SIPO i '
     'gemelli si definiscono insieme e il testo di ciascuno cita gli altri. Non importa dati: la '
     'pratica in SIPO è già completa. Per ciascun atto esegue /finalizzaAtto come oggi; '
     'l’allineamento anagrafico di un atto formato sulla web app segue l’analisi di integrazione '
     '[R1] (GE-16).'),
]

COLONNE_SA = [
    ['Colonna', 'Tipo', 'Note'],
    ['ID_SOGGETTO_ATTO', 'NUMBER (PK)', 'Chiave tecnica della riga (IDENTITY).'],
    ['ID_ATTO_SIPO', 'NUMBER (FK)', 'L’atto di SIPO, e attraverso lo store l’atto ANSC: chiave '
     'esterna verso ANSC_STATO_ATTO.ID_ATTO_SIPO.'],
    ['ID_NASCITA_SOGGETTO', 'NUMBER', 'Il nato come riga di ATTO_NASCITA_SOGGETTO.ID, per valore. '
     'Solo per le nascite: è il riferimento disponibile alla prenotazione e al recupero.'],
    ['ID_SOGGETTO', 'NUMBER', 'MATR_USR.SOGGETTO.ID_SOGGETTO, per valore. Per il nato si scrive '
     'alla definizione, quando SIPO crea il soggetto; per gli altri atti è il riferimento '
     'ordinario.'],
    ['COD_RUOLO', 'VARCHAR2(20)', 'Il ruolo del soggetto nell’atto ANSC: INTESTATARIO per i nati. '
     'Il dominio si estende con gli atti a due intestatari (GE-17).'],
    ['ID_ANSC_SOGGETTO', 'VARCHAR2(50)', 'L’identificativo del soggetto in ANSC restituito da R005, '
     'quando noto. Per i soggetti che hanno una riga in SOGGETTO sta in '
     'ANSC_SOGGETTO_IDENTIFICATIVI [R1]; per il nato quella riga non può esistere prima della '
     'definizione.'],
    ['COD_ORIGINE', 'VARCHAR2(20)', 'Come è nato l’abbinamento: PRENOTAZIONE (caso 1), RECUPERO '
     '(caso 2), VALIDAZIONE (atto ordinario).'],
    ['TS_ABBINAMENTO', 'TIMESTAMP', 'Quando.'],
    ['TS_INS, TS_UPD, UTENTE_INS, UTENTE_UPD', '', 'Campi tecnici [R1].'],
]

DDL_SA = [
    'CREATE TABLE ANSC_USR.ANSC_SOGGETTO_ATTO (',
    '  ID_SOGGETTO_ATTO     NUMBER GENERATED ALWAYS AS IDENTITY,',
    '  ID_ATTO_SIPO         NUMBER            NOT NULL,',
    '  ID_NASCITA_SOGGETTO  NUMBER,',
    '  ID_SOGGETTO          NUMBER,',
    '  COD_RUOLO            VARCHAR2(20 CHAR) NOT NULL,',
    '  ID_ANSC_SOGGETTO     VARCHAR2(50 CHAR),',
    '  COD_ORIGINE          VARCHAR2(20 CHAR) NOT NULL,',
    '  TS_ABBINAMENTO       TIMESTAMP         NOT NULL,',
    '  TS_INS               TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  TS_UPD               TIMESTAMP,',
    '  UTENTE_INS           VARCHAR2(40 CHAR) NOT NULL,',
    '  UTENTE_UPD           VARCHAR2(40 CHAR),',
    '  CONSTRAINT PK_ANSC_SOGGETTO_ATTO PRIMARY KEY (ID_SOGGETTO_ATTO),',
    '  CONSTRAINT UK_ANSC_SOGG_ATTO_RUOLO UNIQUE (ID_ATTO_SIPO, COD_RUOLO),',
    '  CONSTRAINT FK_ANSC_SOGG_ATTO_STATO FOREIGN KEY (ID_ATTO_SIPO)',
    '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_RIF',
    '    CHECK (ID_NASCITA_SOGGETTO IS NOT NULL OR ID_SOGGETTO IS NOT NULL),',
    '  CONSTRAINT CK_ANSC_SOGG_ATTO_ORIG',
    "    CHECK (COD_ORIGINE IN ('PRENOTAZIONE','RECUPERO','VALIDAZIONE'))",
    ');',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_NASC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_NASCITA_SOGGETTO);',
    'CREATE INDEX IX_ANSC_SOGG_ATTO_SOGG ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_SOGGETTO);',
]

GE_RISCRITTI = {
    'GE-01': ('Completamento da gestionale', 'ANSC ha chiarito che tramite servizi cooperativi la '
              'prenotazione porta l’UC specifico e le bozze si completano con quello, mentre la web '
              'app usa il caso d’uso di servizio [A9]. Vale per i gemelli con lo stesso UC (caso 1). '
              'Resta da provare in preproduzione il completamento di una bozza prenotata con l’UC '
              'ordinario. Coincide in parte con OP-46 [R1].', 'Risolto in parte'),
    'GE-03': ('Nati morti nella prenotazione', 'Il numero dei gemelli è il totale, nati morti '
              'compresi [A9]: ogni nato ha il suo atto e compare negli elenchi dei fratelli.',
              'Chiuso'),
    'GE-04': ('Parto misto', 'I gemelli con UC diversi si trattano con il caso d’uso di servizio e '
              'la tipologia di nascita, solo sulla web app [A10]: è il caso 2. La richiesta di una '
              'via tramite servizi cooperativi è aperta [A11]; se ANSC la offrirà, il caso 2 potrà '
              'seguire il percorso del caso 1.', 'Risolto in parte'),
}

GE_NUOVI = [
    ['GE-15', 'Numero comunale sulla web app', 'Nella prenotazione della web app l’ufficiale '
     'riporta i numeri staccati da SIPO. Va verificato che la web app li accetti nella forma della '
     'serie di SIPO (sei cifre, mentre ANSC dichiara cinque caratteri) e che non li sostituisca con '
     'il numero che propone [R2].', 'Aperto'],
    ['GE-16', 'Anagrafe degli atti recuperati', 'Per un atto formato sulla web app la '
     'comunicazione anagrafica la genera ANSC. Va deciso se DEFINISCI GEMELLI chiami ancora '
     'l’iscrizione ANPR di SIPO come la /finalizzaAtto di oggi, e da dove SIPO ricavi allora la '
     'riga in SOGGETTO del nato, che oggi crea dopo l’iscrizione [R1], [R2].', 'Aperto'],
    ['GE-17', 'ANSC_SOGGETTO_ATTO nell’analisi di integrazione', 'Da riportare in [R1]: la tabella, '
     'il dominio di COD_RUOLO, il raccordo con ANSC_SOGGETTO_IDENTIFICATIVI una volta creato il '
     'soggetto del nato e l’origine VALIDAZIONE per gli atti ordinari.', 'Aperto'],
    ['GE-18', 'Controlli dell’abbinamento al recupero', 'Va verificato in preproduzione che R005 '
     'ritrovi per numero comunale e anno gli atti del caso d’uso di servizio, e che restituisca per '
     'ciascuno l’intestatario con sesso, data e ora di nascita e la tipologia di nascita, su cui si '
     'fonda l’abbinamento.', 'Aperto'],
]


# ------------------------------------------------------------------ esecuzione
def main():
    d = docx.Document(IN)
    fatti = []

    # 1. riferimenti
    rif = D.trova_tabella(d, 'riferimento', 'natura')
    for riga in RIF_NUOVI:
        D.clona_riga(rif, riga)
    # le righe clonate vanno dopo [A8]
    a8 = riga_di(rif, '[A8]')._tr
    for riga in reversed(RIF_NUOVI):
        a8.addnext(riga_di(rif, riga[0])._tr)

    # 2. In sintesi
    primo = para_che_inizia(d, 'La guida ANSC fa completare i gemelli')
    ultimo = para_che_inizia(d, 'Nello store, una riga per gemello.')
    racc = in_coda(d)
    for testa, corpo in SINTESI:
        voce(d, testa, corpo)
    sposta_prima(racc(), primo._p)
    togli_fino(primo._p, ultimo._p)
    D.sostituisci(d, 'le altre si inseriscono alla prenotazione.',
                  'le altre si inseriscono alla prenotazione nel caso 1, allo stacco dei numeri '
                  'nel caso 2.', attese=1, fatti=fatti)

    # 3. la prenotazione: tabella del contratto
    t = tabella_che_contiene(d, 'listaNumeriComunali')
    r = riga_di(t, 'Richiesta: numeroGemelliNatiVivi')
    D.riscrivi_cella(r.cells[2], r.cells[2].text + ' ANSC indica di passare il totale dei gemelli, '
                     'nati morti compresi [A9].')
    r = riga_di(t, 'Richiesta: idUsecase')
    D.riscrivi_cella(r.cells[2], 'Obbligatorio e unico per tutta la chiamata. Tramite servizi '
                     'cooperativi è l’UC specifico dei nati; sulla web app è sempre il caso d’uso '
                     'di servizio [A9]. L’esempio del contratto è «1170», il payload di test usa '
                     '11111000.')
    r = riga_di(t, 'Stato degli atti creati')
    D.riscrivi_cella(r.cells[2], r.cells[2].text + ' Le bozze prenotate da gestionale non hanno '
                     'composizione: arriva con la validazione, e prima l’anteprima non è '
                     'disponibile [A12].')

    # 4. il completamento: UC e bozza
    rifai_voce(d, para_che_inizia(d, 'Con quale UC.'), 'Con quale UC.',
               'Con quello della prenotazione. Tramite servizi cooperativi la prenotazione porta '
               'l’UC specifico e le bozze si completano con quello; la web app usa sempre il caso '
               'd’uso di servizio. In entrambi i casi non si cambia il numero comunale e non si '
               'registrano UC «ex novo»: si completano le bozze generate dal sistema [A9]. La guida '
               'descrive il percorso della web app: «il caso d’uso predisposto per i parti '
               'gemellari è un caso d’uso di servizio» [A3]. Il caso di servizio delle nascite, '
               '11999999 (Dic_Nasc_999), dichiara 33 campi obbligatori — numero comunale, data e ora '
               'di formazione, motivo del recupero, nome, sesso, data, ora e stato di nascita del '
               'nato, composizione completa — ed è l’unico mapping che porti tipoNascitaSoggetto.')
    rifai_voce(d, para_che_inizia(d, 'Come si riconosce la bozza.'), 'Come si riconosce la bozza.',
               'Il modello evento porta sia l’identificativo interno sia quello nazionale, entrambi '
               '«assegnati dal sistema»; nessuna fonte dice quale valorizzare per completare la '
               'bozza prenotata invece di crearne una nuova (GE-02). Un caso reale mostra l’esito '
               'dell’errore: un atto formato fuori dalle bozze prenotate, che il supporto ANSC '
               'indica come da registrare «partendo dalla bozza» [A12].')

    # 5. la sottosezione sui servizi cooperativi diventa «Due casi»
    h3 = D.h(d, 3, 'Che cosa si può fare con i servizi cooperativi')
    stop = D.h(d, 2, 'Punti da chiarire')
    racc = in_coda(d)
    heading(d, 3, 'Due casi: gemelli con lo stesso UC o con UC diversi')
    par(d, 'La prenotazione accetta un solo caso d’uso, e la bozza non cambia caso d’uso al '
        'completamento. Da qui due casi, che non sceglie l’operatore: li decide lo stato dei nati.')
    tabella(d, CASI, [0.85, 1.55, 1.75, 1.45, 0.75])
    par(d, 'Il criterio è l’UC, non soltanto lo stato. Gli UC dei riconosciuti prima della nascita '
        'hanno solo la variante del nato vivo: un parto di riconosciuti prima della nascita con un '
        'nato morto non ha un UC ordinario per quel nato, e segue il caso 2 anche se lo stato fosse '
        'lo stesso per tutti. Nelle trascrizioni da ospedale SIPO forza i due flag a N, quindi i '
        'gemelli hanno lo stesso UC (GE-11).')
    par(d, 'I passi della guida, nei due casi:')
    tabella(d, PASSI, [0.3, 2.2, 1.9, 1.9])
    par(d, 'La segnalazione che chiede una procedura tramite servizi cooperativi per i gemelli con '
        'casi d’uso diversi è ancora aperta; nei commenti un comune riferisce di aver formato un '
        'parto gemellare ordinario e di aver riportato la morte con un’annotazione libera [A11]. Il '
        'documento non adotta questa via, che produce un atto non conforme allo stato del nato. Se '
        'ANSC aprirà il caso ai servizi cooperativi, il caso 2 potrà seguire il percorso del caso 1 '
        '(GE-04).')
    sposta_prima(racc(), h3._p)
    togli_fino(h3._p, stop._p)

    # 6. punti da chiarire
    rifai_voce(d, para_che_inizia(d, 'Il parto misto.'), 'Il parto misto.',
               'ANSC lo tratta con il caso d’uso di servizio, sulla web app [A10]; la richiesta di '
               'una via tramite servizi cooperativi è aperta [A11] (GE-04).')

    # 7. confronto
    t = tabella_che_contiene(d, 'Conseguenza per l’integrazione')
    r = riga_di(t, 'Stato del singolo nato')
    D.riscrivi_cella(r.cells[3], 'Se gli UC dei nati coincidono il parto si prenota dal '
                     'gestionale con quell’UC (caso 1); se differiscono gli atti si formano sulla '
                     'web app con il caso d’uso di servizio (caso 2).')

    # 8. integrazione: apertura e panoramica
    p = para_che_inizia(d, 'Una modalità di integrazione esiste')
    D.testo_di(p, 'I percorsi sono due, e non li sceglie l’operatore: li decide il parto. Dopo la '
               'divisione SIPO determina l’UC di ciascun nato. Se è lo stesso per tutti si segue il '
               'caso 1, tutto da SIPO, con la prenotazione tramite servizi cooperativi e la '
               'struttura di oggi (pratica unica, divisione, definizione gemello per gemello). Se '
               'differisce, il caso 2: la pratica resta completa in SIPO, i numeri si staccano in '
               'blocco, gli atti si formano sulla web app e rientrano con un solo recupero, secondo '
               'la strategia adottata per gli atti che SIPO non può formare [R2].')
    sostituisci_figura(d, 'I due percorsi di integrazione', png('gem4_panoramica.pptx.png'), LARGO,
                       'I due casi: la scelta dopo la divisione')

    # 9. caso 1
    D.testo_di(D.h(d, 2, 'Percorso A — tutto da SIPO'),
               'Caso 1 — gemelli con lo stesso UC: tutto da SIPO')
    t = tabella_che_contiene(d, 'Riepilogo del gemello 1 → PRENOTA GEMELLI (nuovo)')
    r = riga_di(t, '3')
    D.riscrivi_cella(r.cells[2], 'Gli UC dei nati coincidono: si chiedono N numeri comunali '
                     'consecutivi e si chiama la prenotazione con quell’UC e con il numero totale '
                     'dei gemelli.')
    D.riscrivi_cella(r.cells[4], 'N righe in ANSC_STATO_ATTO in BOZZA, ciascuna con numero '
                     'comunale e idAnsc; righe in ATTI_GEMELLARI e in ANSC_SOGGETTO_ATTO.')
    r = riga_di(t, '5')
    D.riscrivi_cella(r.cells[2], 'R009 sulla bozza prenotata, con lo stesso UC (con quale campo: '
                     'OP-46).')
    sostituisci_figura(d, 'Percorso A:', png('gem4_flusso_1.pptx.png'), 5.9,
                       'Caso 1: le pagine, i servizi e gli stati, con le righe dello store')
    rifai_voce(d, para_che_inizia(d, 'Quando compare.'), 'Quando compare.',
               'Solo sul primo gemello di una pratica divisa, solo se gli UC dei nati coincidono, '
               'finché la prenotazione non è fatta. VALIDA resta inibito sugli atti dei gemelli fino '
               'a prenotazione avvenuta.')
    rifai_voce(d, para_che_inizia(d, 'UC. Si determina per ciascun gemello'), 'UC.',
               'Si determina per ciascun gemello dai suoi due flag; la prenotazione passa l’UC '
               'comune e il numero totale dei gemelli. Se gli UC differiscono il pulsante non '
               'compare e la pagina porta al caso 2.')
    rifai_voce(d, para_che_inizia(d, 'Esito. Ciascun identificativo'), 'Esito.',
               'Ciascun identificativo restituito si assegna al gemello del numero comunale che '
               'contiene: una riga di ANSC_STATO_ATTO in BOZZA per ciascun atto, con numero comunale '
               'e idAnsc, una riga della tabella dei gemelli e una di ANSC_SOGGETTO_ATTO, descritte '
               'più avanti.')

    # 10. caso 2: tutta la sezione si riscrive
    hb = D.h(d, 2, 'Percorso B — la web app e il ritorno in SIPO')
    D.testo_di(hb, 'Caso 2 — gemelli con UC diversi: la web app e il recupero in SIPO')
    stop = D.h(d, 2, 'Nato morto e nato vivo poi deceduto nel parto plurimo')
    togli_fino(hb._p.getnext(), stop._p)
    racc = in_coda(d)
    par(d, 'Gli atti si formano sulla web app, perché è il solo canale del caso d’uso di servizio. '
        'Tutto il resto resta in SIPO: la pratica è compilata per intero come oggi, i numeri si '
        'staccano in blocco subito dopo la divisione, e il ritorno è un solo recupero per l’intero '
        'parto, che non importa dati ma aggancia ciascun atto ANSC al proprio gemello. È la '
        'strategia adottata per gli atti che SIPO non può formare [R2], applicata al parto invece '
        'che al singolo atto.')
    tabella(d, PASSI_2, [0.3, 1.25, 2.45, 1.2, 1.15])
    figura(d, png('gem4_flusso_2.pptx.png'), 5.9, 'Caso 2: le pagine, i servizi e gli stati, con '
           'le righe dello store')
    par(d, 'Regole dei passi del caso 2:')
    for testa, corpo in REGOLE_2:
        voce(d, testa, corpo)
    figura(d, png('gem4_dati_ansc.png'), LARGO, 'Il caso 2: la pagina «Dati per ANSC» del parto, '
           'con i numeri comunali staccati in blocco (ipotesi)')
    figura(d, png('gem4_recupero.png'), LARGO, 'Il caso 2: l’esito di RECUPERA GEMELLI (ipotesi)')
    par(d, 'Il prezzo è il doppio inserimento dei dati sulla web app, moltiplicato per il numero '
        'dei nati. Riguarda però pochi parti: nella ricognizione i parti plurimi sono 774 atti su '
        '42.239 nascite, e quelli con nati in stati diversi ne sono una frazione.')
    sposta_prima(racc(), stop._p)

    # 11. nato morto nel parto plurimo
    rifai_voce(d, para_che_inizia(d, 'UC. Ogni gemello ha l’UC'), 'UC.',
               'Ogni gemello ha l’UC della propria variante. Se la variante è la stessa per tutti '
               'l’UC è comune e vale il caso 1; altrimenti il caso 2.')
    rifai_voce(d, para_che_inizia(d, 'Prenotazione. Se i nati morti'), 'Prenotazione.',
               'Il numero dei gemelli comprende i nati morti: è l’indicazione di ANSC sul campo '
               'numeroGemelliNatiVivi [A9]. Ogni nato, vivo o morto, ha il suo atto e compare negli '
               'elenchi dei fratelli.')

    # 12. effetti sul disegno: ATTI_GEMELLARI e la tabella nuova
    t = tabella_che_contiene(d, 'id_richiesta_prenotazione')
    note = {
        'id_richiesta_prenotazione': 'La chiamata R009 /prenota/evento che ha predisposto l’atto. '
        'Vuota nel caso 2, dove la prenotazione si fa sulla web app.',
        'ty_use_case': 'L’UC passato alla prenotazione nel caso 1, che è quello di tutti i gemelli. '
        'Nel caso 2 vale 11999999, il caso d’uso di servizio, e si scrive al recupero.',
        'fg_stesura_atto': '0 da stendere, 1 atto formato (firma dell’USC nel caso 1, abbinamento al '
        'recupero nel caso 2).',
        'cd_operatore': 'Chi ha prenotato o, nel caso 2, staccato i numeri.',
    }
    for col, testo in note.items():
        D.riscrivi_cella(riga_di(t, col).cells[3], testo)
    p = para_che_inizia(d, 'Va aggiunta l’operazione di prenotazione dei gemelli')
    D.testo_di(p, 'Vanno aggiunte al concentratore due operazioni: la prenotazione dei gemelli '
               '(caso 1), che stacca i numeri, chiama R009 /prenota/evento e registra store, tabella '
               'dei gemelli e ANSC_SOGGETTO_ATTO in una sola azione; il recupero dei gemelli (caso '
               '2), che cerca gli atti con R005, li abbina e registra gli stessi dati. La chiusura '
               'riusa l’annullamento già previsto.')
    stop = D.h(d, 2, 'Le righe di ANSC_STATO_ATTO nel parto plurimo')
    racc = in_coda(d)
    heading(d, 3, 'La tabella ANSC_SOGGETTO_ATTO')
    par(d, 'L’abbinamento fra un nato e il suo atto ANSC oggi non ha un posto. Lo store lega l’atto '
        'di SIPO all’atto ANSC, ma non dice quale soggetto ne sia l’intestatario; e il nato non ha '
        'ancora una riga in SOGGETTO quando l’atto si forma. SIPO la crea solo alla definizione, '
        'dopo l’iscrizione in ANPR, clonandola dall’anagrafe e scrivendone l’identificativo in '
        'ATTO_NASCITA.ID_SOGGETTO_DEFINITO e in ATTO_NASCITA_SOGGETTO.ID_SOGGETTO_INTERESSATO '
        '(AttoNasciteFlow, righe 405-430 [S2]). Fino ad allora il nato è soltanto la sua riga di '
        'ATTO_NASCITA_SOGGETTO, una per atto dopo la divisione.')
    par(d, 'La tabella nuova sta in ANSC_USR, accanto allo store, ed è distinta da ATTI_GEMELLARI: '
        'quella raggruppa il parto, questa lega un soggetto all’atto ANSC di cui è intestatario, e '
        'vale per qualunque atto. Registra il soggetto con il riferimento disponibile quando '
        'l’abbinamento avviene e lo completa dopo.')
    tabella(d, COLONNE_SA, [1.9, 1.2, 3.2])
    codice(d, DDL_SA)
    voce(d, 'Quando nasce la riga.', 'Nel caso 1 a PRENOTA GEMELLI, una per gemello, con '
         'l’ID_NASCITA_SOGGETTO del nato che la divisione ha messo in quell’atto (GE-07). Nel caso 2 '
         'al recupero, solo per i gemelli abbinati, dopo il confronto fra l’intestatario restituito '
         'da R005 e il nato in SIPO. Fuori dal parto plurimo alla validazione dell’atto. Alla '
         'definizione si completa ID_SOGGETTO.')
    voce(d, 'Che cosa non ripete.', 'L’identificativo nazionale dell’atto: la riga richiama '
         'l’atto ANSC attraverso la chiave esterna verso lo store, che lo porta. È la regola «un '
         'dato, un posto» già applicata ad ATTI_GEMELLARI.')
    voce(d, 'Una sola riga per ruolo.', 'Il vincolo di unicità su atto e ruolo impedisce di '
         'abbinare due nati allo stesso atto, che è l’errore da cui il recupero deve difendersi.')
    sposta_prima(racc(), stop._p)
    sostituisci_figura(d, 'Le righe di ANSC_STATO_ATTO nel parto plurimo',
                       png('gem4_erd.pptx.png'), LARGO,
                       'Le righe di ANSC_STATO_ATTO nel parto plurimo e i loro legami, con '
                       'ATTI_GEMELLARI e ANSC_SOGGETTO_ATTO')

    # 13. le righe dello store
    D.sostituisci(d, 'Nel percorso A le righe dei gemelli 2…N nascono al passo PRENOTA GEMELLI',
                  'Nel caso 1 le righe dei gemelli 2…N nascono al passo PRENOTA GEMELLI', attese=1,
                  fatti=fatti)
    t = tabella_che_contiene(d, 'Righe toccate')
    r = riga_di(t, 'PRENOTA GEMELLI: R009 /prenota/evento')
    D.riscrivi_cella(r.cells[3], 'INSERT di N righe, fg_stesura_atto 0. ANSC_SOGGETTO_ATTO: N '
                     'righe, COD_ORIGINE PRENOTAZIONE.')
    r = riga_di(t, 'Definisci del gemello k')
    D.riscrivi_cella(r.cells[3], 'ANSC_SOGGETTO_ATTO: si completa ID_SOGGETTO.')
    tl = tabella_che_contiene(d, 'Gemello ↔ parto')
    D.clona_riga(tl, ['Soggetto ↔ atto ANSC', 'ANSC_SOGGETTO_ATTO.ID_ATTO_SIPO',
                      'ANSC_STATO_ATTO.ID_ATTO_SIPO', 'Chiave esterna dichiarata, unica per ruolo.',
                      'N:1'])
    D.clona_riga(tl, ['Soggetto ↔ nato in SIPO', 'ANSC_SOGGETTO_ATTO.ID_NASCITA_SOGGETTO, '
                      'ID_SOGGETTO', 'ATTO_NASCITA_SOGGETTO.ID, SOGGETTO.ID_SOGGETTO',
                      'Per valore; ID_SOGGETTO dalla definizione.', '1:1'])
    p = para_che_inizia(d, 'Un gemello nato morto che non si prenota (GE-03)')
    D.testo_di(p, 'Il nato morto si prenota insieme agli altri: conta nel numero dei gemelli e '
               'compare negli elenchi dei fratelli [A9].')
    D.testo_di(D.h(d, 3, 'Nel percorso B'), 'Nel caso 2')
    p = para_che_inizia(d, 'Le righe sono le stesse e nascono prima')
    D.testo_di(p, 'Le righe sono le stesse e nascono prima: allo stacco dei numeri con DATI PER '
               'ANSC, con le stesse colonne comuni, nello stato WA · ATTESA WEBAPP [R2]. '
               'ATTI_GEMELLARI riceve le N righe nello stesso momento, con id_richiesta_prenotazione '
               'vuoto, perché la prenotazione la fa l’ufficiale sulla web app. RECUPERA GEMELLI '
               'scrive, sulla sola riga di ciascun gemello abbinato, ID_ANSC, ID_UC_ANSC (11999999, '
               'il caso d’uso di servizio), lo stato 5 FIRMATO DA USC, COD_FASE FIRMATO e il modello '
               'evento letto; ATTI_GEMELLARI riceve ty_use_case e fg_stesura_atto 1; '
               'ANSC_SOGGETTO_ATTO la riga dell’intestatario, con COD_ORIGINE RECUPERO. La chiamata '
               'si registra in ANSC_LOG_AUDIT sulla riga del gemello 1, come la prenotazione del caso '
               '1. Un gemello non abbinato resta in attesa e la supervisione lo mostra; DEFINISCI '
               'GEMELLI attende che lo siano tutti.')

    # 14. punti aperti
    op = D.trova_tabella(d, 'tema', 'questione')
    for cod, (tema, questione, stato) in GE_RISCRITTI.items():
        r = riga_di(op, cod)
        D.riscrivi_cella(r.cells[1], tema)
        D.riscrivi_cella(r.cells[2], questione)
        D.riscrivi_cella(r.cells[3], stato)
    r = riga_di(op, 'GE-09')
    D.riscrivi_cella(r.cells[2], r.cells[2].text + ' Nel caso 2, se la divisione si annulla dopo '
                     'lo stacco, i numeri si scartano.')
    r = riga_di(op, 'GE-11')
    D.riscrivi_cella(r.cells[2], r.cells[2].text + ' Con i flag forzati a N i gemelli trascritti '
                     'hanno lo stesso UC e seguono il caso 1.')
    for riga in GE_NUOVI:
        D.clona_riga(op, riga)

    D.sostituisci(d, 'Raggruppa i gemelli in entrambi i percorsi.', 'Raggruppa i gemelli in '
                  'entrambi i casi.', attese=1, fatti=fatti)

    # 15. nomenclatura residua: «percorso A/B» → «caso 1/2» (fuori dalla Storia)
    storia_t = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for v, n in (('percorso A', 'caso 1'), ('percorso B', 'caso 2'),
                 ('Percorso A', 'Caso 1'), ('Percorso B', 'Caso 2')):
        k = sostituisci_nei_run(d, v, n, esclusa=storia_t)
        if k:
            fatti.append('%s → %s: %d' % (v, n, k))

    # 16. figure rinumerate nell'ordine in cui compaiono
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])

    # 17. frontespizio e storia
    for fatto in D.frontespizio(d, '0.4', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.4', 'In sintesi · ANSC · SIPO e ANSC a confronto · La modalità di '
             'integrazione · Punti aperti · Riferimenti',
             'I due percorsi diventano due casi decisi dagli UC dei nati, sulle risposte di ANSC '
             'alle segnalazioni pubbliche: gemelli con lo stesso UC, tutto da SIPO tramite servizi '
             'cooperativi; gemelli con UC diversi, caso d’uso di servizio sulla web app con numeri '
             'staccati in blocco da SIPO, pagina «Dati per ANSC», RECUPERA GEMELLI per l’intero '
             'parto e DEFINISCI GEMELLI. Nuova tabella ANSC_SOGGETTO_ATTO. Diagrammi e schermate '
             'rifatti. GE-01, GE-03, GE-04 riformulati; GE-15…GE-18; [A9]…[A12].')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
