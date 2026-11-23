# -*- coding: utf-8 -*-
"""ANALISI_Nascite-Gemellari_SIPO-ANSC v0.2 (19/11/2026), dal FILE REALE della v0.1 rivista a mano
dall'utente (screenshot di SIPO nelle figure 1 e 2, figura 3 diventata «Errore nella divisione»,
ritocchi al testo). NON rieseguire genera_nascite_gemellari.py: perderebbe quelle modifiche.

Che cosa fa:
  * immagini al posto dei segnaposto che si possono produrre: la prenotazione sulla web app (dalle
    figure 38-40 della guida operativa ANSC [A3]), i due percorsi (panoramica), il passo PRENOTA
    GEMELLI (due ipotesi di schermata); restano segnaposto le due schermate reali di SIPO
    (errore nella divisione, anteprima dei gemelli), che vanno catturate dall'applicazione;
  * due flussi a cinque corsie (percorso A, percorso B) con la corsia dello store ANSC_STATO_ATTO;
  * nuova sezione «Le righe di ANSC_STATO_ATTO nel parto plurimo»: una riga per gemello, quando si
    inseriscono e si aggiornano, come sono legate (ERD), elenchi dei fratelli, esiti anomali della
    prenotazione, percorso B;
  * ATTI_GEMELLARI rivista: raggruppamento per pratica (id_lavorazione_padre), FK verso
    ANSC_STATO_ATTO, id_richiesta_prenotazione e ty_use_case facoltativi, tolto nr_atto_comunale;
  * figure rinumerate in ordine; GE-13, GE-14; [S5]; Storia e frontespizio.

Figure: diagrammi_gemellari_pptx.py (+ qlmanage), schermate_gemellari.py.

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v0_2.py
"""
import copy
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image, ImageDraw, ImageFont

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import _versa, h, par, tabella, voce        # noqa: E402

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.1.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.2.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '19/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')
GUIDA = os.path.join(BASE, '..', 'ansc', 'docs', 'Guida_operativa_ANSC.pdf')
LARGO = 6.3


# ------------------------------------------------------------------ primitive di posizionamento
def corpo(d):
    return d.element.body


def in_coda(d):
    """Gli elementi aggiunti in fondo al corpo da una funzione, da spostare altrove."""
    b = corpo(d)
    vecchi = list(b)

    def raccogli():
        return [e for e in b if e.tag != qn('w:sectPr') and not any(e is v for v in vecchi)]
    return raccogli


def sposta_prima(elementi, ancora):
    for e in elementi:
        ancora.addprevious(e)


def para_che_inizia(d, inizio):
    trovati = [p for p in d.paragraphs if p.text.strip().startswith(inizio)]
    assert len(trovati) == 1, (inizio, len(trovati))
    return trovati[0]


def tabella_che_contiene(d, testo):
    trovate = [t for t in d.tables if any(testo in c.text for r in t.rows for c in r.cells)]
    assert len(trovate) == 1, (testo, len(trovate))
    return trovate[0]


def heading(d, livello, t):
    try:
        return h(d, livello, t)
    except KeyError:
        return h(d, 2, t)


def figura(d, png, pollici, didascalia):
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(png, width=Inches(pollici))
    cap = d.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _versa(cap, 'Figura 0 – ' + didascalia, dim=9, corsivo=True)


def codice(d, righe):
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()


def segnaposto_con_immagine(d, tab, png, pollici):
    """Sostituisce la tabella-segnaposto con un paragrafo centrato che porta l'immagine."""
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(png, width=Inches(pollici))
    tab._tbl.addprevious(p._p)
    tab._tbl.getparent().remove(tab._tbl)
    return p


def didascalia_dopo(p_immagine):
    """Il paragrafo di didascalia che segue un'immagine o un segnaposto."""
    e = p_immagine._p.getnext()
    while e is not None and e.tag == qn('w:p') and not Paragraph(e, None).text.strip():
        e = e.getnext()
    cap = Paragraph(e, p_immagine._parent)
    assert cap.text.startswith('Figura'), cap.text
    return cap


def riscrivi_didascalia(cap, testo):
    num = re.match(r'Figura \d+ – ', cap.text).group(0)
    D.testo_di(cap, num + testo)


# ------------------------------------------------------------------ immagini preparate qui
def webapp_png():
    """Figure 38-40 della guida operativa ANSC (p. 41-42 del PDF), una sotto l'altra."""
    out = os.path.join(IMG, 'gem_webapp_prenotazione.png')
    pagine = os.path.join(IMG, 'guida')
    os.makedirs(pagine, exist_ok=True)
    js = os.path.join(pagine, 'render.js')
    with open(js, 'w') as f:
        f.write("ObjC.import('PDFKit');ObjC.import('AppKit');function run(a){var d=$.PDFDocument."
                "alloc.initWithURL($.NSURL.fileURLWithPath(a[0]));for(var i=2;i<a.length;i++){var "
                "n=parseInt(a[i]);var im=d.pageAtIndex(n-1).thumbnailOfSizeForBox($.NSMakeSize"
                "(1700,2200),0);im.TIFFRepresentation.writeToFileAtomically(a[1]+'/p'+n+'.tiff',"
                "true);}return 'ok';}")
    os.system('osascript -l JavaScript "%s" "%s" "%s" 41 42 >/dev/null' % (js, os.path.abspath(GUIDA),
                                                                       pagine))
    for n in (41, 42):
        os.system('sips -s format png "%s/p%d.tiff" --out "%s/p%d.png" >/dev/null' %
                  (pagine, n, pagine, n))
    p41 = Image.open(os.path.join(pagine, 'p41.png')).convert('RGB')
    p42 = Image.open(os.path.join(pagine, 'p42.png')).convert('RGB')
    ritagli = [p41.crop((204, 1470, 1480, 1952)), p42.crop((204, 340, 1460, 786)),
               p42.crop((204, 985, 1452, 1460))]
    etichette = ('1  Numero dei gemelli e tipo evento', '2  Un numero comunale per ciascun gemello',
                 '3  Gli identificativi nazionali degli atti predisposti')
    larg = max(r.width for r in ritagli)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 26)
    alt = sum(r.height + 60 for r in ritagli)
    tela = Image.new('RGB', (larg, alt), 'white')
    dr = ImageDraw.Draw(tela)
    y = 0
    for r, et in zip(ritagli, etichette):
        dr.text((6, y + 14), et, font=font, fill='#1f3a5f')
        tela.paste(r, (0, y + 52))
        y += r.height + 60
    tela.save(out)
    return out


def png(nome):
    p = os.path.join(IMG, nome)
    assert os.path.exists(p), p
    return p


# ------------------------------------------------------------------ testi della sezione nuova
RIGHE_STORE = [
    ['Momento', 'Righe toccate', 'Operazione e colonne', 'ATTI_GEMELLARI'],
    ['Dati anagrafici: R005 su genitori e dichiarante', 'Gemello 1 (l’atto della pratica)',
     'INSERT. COD_FASE IN_LAVORAZIONE, COD_PAGINA_RIPRESA DETTAGLIO, colonne comuni '
     '(ID_TIPO_EVENTO, ID_TIPO_CONTENUTO, COD_TIPO_OPERAZIONE, ID_MODELLO_ATTO, COD_MUNICIPIO, '
     'FLG_EMERGENZA).', '—'],
    ['Riepilogo → Conferma: divisione', 'Nessuna', 'La procedura di divisione sta in MATR_USR e '
     'non scrive in ANSC_USR: gli atti 2…N esistono in SIPO e non ancora nello store.', '—'],
    ['PRENOTA GEMELLI: UC e numeri', 'Gemello 1: UPDATE. Gemelli 2…N: INSERT.',
     'ID_UC_ANSC, COD_LOGICA, COD_ORIGINE_UC, NUMERO_ATTO, COD_FASE UC_DETERMINATO. Le righe '
     'nuove copiano dal gemello 1 le colonne comuni; UC e numero sono di ciascun gemello.', '—'],
    ['PRENOTA GEMELLI: R009 /prenota/evento', 'Tutte', 'UPDATE. ID_ANSC, ID_STATO 1 e STATO BOZZA, '
     'COD_FASE PRENOTATO, TXT_EVENTO iniziale con id e idAnsc restituiti.',
     'INSERT di N righe, fg_stesura_atto 0.'],
    ['Documenti e anteprima del gemello k', 'Riga k', 'COD_FASE DOCUMENTI_ACQUISITI, poi '
     'PREVALIDATO; TXT_EVENTO con i campi gemellari e gli elenchi dei fratelli; NUM_REVISIONE, '
     'COD_PAGINA_RIPRESA.', '—'],
    ['«VALIDA» del gemello k', 'Riga k', 'ID_STATO 2 CONFERMATO, TS_VALIDAZIONE, COD_FASE '
     'VALIDATO. L’idAnsc restituito deve coincidere con quello prenotato: se differisce, la '
     'validazione ha creato un atto nuovo (GE-02).', '—'],
    ['Firme del gemello k', 'Riga k', 'ID_STATO 4, poi 11, poi 5 FIRMATO DA USC; COD_FASE FIRMATO '
     'alla firma dell’ufficiale.', 'fg_stesura_atto 1.'],
    ['Definisci del gemello k', 'Riga k', 'Nessuna colonna: in SIPO l’atto k passa a 2 DEFINITO.',
     '—'],
    ['Chiusura del parto', 'Righe dei gemelli non usati', 'Dopo R011: ID_STATO 9 CANCELLATO, '
     'COD_FASE ANNULLATO. Il numero passa a Scartato (PUT /scarta).',
     'Invariate: conservano il legame con il parto.'],
]

LEGAMI = [
    ['Legame', 'Da', 'A', 'Come', 'Cardinalità'],
    ['Gemello ↔ stato in ANSC', 'ATTI_GEMELLARI.id_atto_sipo', 'ANSC_STATO_ATTO.ID_ATTO_SIPO',
     'Chiave esterna dichiarata, con vincolo di unicità sulla colonna.', '1:1'],
    ['Stato in ANSC ↔ atto SIPO', 'ANSC_STATO_ATTO.ID_ATTO_SIPO', 'ATTO.ID_ATTO (MATR_USR)',
     'Per valore, come in tutto lo schema ANSC_USR.', '1:0..1'],
    ['Gemello ↔ parto', 'ATTI_GEMELLARI.id_lavorazione_padre', 'ATTO.ID_ATTO del gemello 1',
     'Per valore; è la chiave del raggruppamento.', 'N:1'],
    ['Posizione', 'ATTI_GEMELLARI.nr_progressivo_gemello', 'ATTO_NASCITA_SOGGETTO.POS_GEMELLO',
     'Per valore; uguali per regola (GE-08).', '1:1'],
    ['Numero comunale', 'ANSC_STATO_ATTO.NUMERO_ATTO', 'DATI_ATTO_ESTERNO.nr_atto_comunale',
     'Per valore.', '1:1'],
    ['Fratelli in ANSC', 'attiGemelliPrec, attiGemelliSucc nel modello evento',
     'ANSC_STATO_ATTO.ID_ANSC dei fratelli', 'Calcolati a ogni composizione, non registrati.',
     '—'],
]

ANOMALIE = [
    ['Esito della prenotazione', 'Che cosa significa', 'Che cosa si fa sulle righe'],
    ['Rifiuto certo (errore con codice)', 'In ANSC non è stato creato alcun atto.',
     'Le righe restano in UC_DETERMINATO con i loro numeri; ULTIMO_ERRORE sulla riga del gemello '
     '1. Si ritenta con gli stessi numeri, oppure, se si rinuncia, i numeri si scartano.'],
    ['Esito indeterminato (tempo scaduto, risposta illeggibile)', 'Non si sa se gli atti esistano.',
     'Nessun secondo tentativo alla cieca: si cercano in ANSC gli atti con i numeri comunali '
     'passati (R005, per numero comunale e data) e si completano le righe con gli identificativi '
     'trovati; si ritenta solo se non ne esiste alcuno (GE-13).'],
    ['Meno identificativi dei gemelli', 'ANSC ha predisposto un numero di atti diverso.',
     'Si assegnano gli identificativi che si abbinano per numero comunale; le righe rimaste senza '
     'identificativo vanno in errore e compaiono nella supervisione (GE-13).'],
    ['Annullamento della divisione dopo la prenotazione', 'Atti in ANSC senza un atto in SIPO.',
     'R011 per ciascun gemello; le righe restano, a 9 CANCELLATO, come storico, con le righe di '
     'ATTI_GEMELLARI; i numeri si scartano (GE-09).'],
]

QUERY = [
    'SELECT g.nr_progressivo_gemello, s.ID_ATTO_SIPO, s.ID_UC_ANSC, s.NUMERO_ATTO,',
    '       s.ID_ANSC, s.ID_STATO, s.STATO, s.COD_FASE',
    '  FROM ANSC_USR.ATTI_GEMELLARI g',
    '  JOIN ANSC_USR.ANSC_STATO_ATTO s ON s.ID_ATTO_SIPO = g.id_atto_sipo',
    ' WHERE g.id_lavorazione_padre = (SELECT id_lavorazione_padre',
    '                                   FROM ANSC_USR.ATTI_GEMELLARI',
    '                                  WHERE id_atto_sipo = :idAtto)',
    ' ORDER BY g.nr_progressivo_gemello;',
]

DDL = [
    'CREATE TABLE ANSC_USR.ATTI_GEMELLARI (',
    '  id_atto_gemellare         NUMBER GENERATED ALWAYS AS IDENTITY,',
    '  id_lavorazione_padre      NUMBER            NOT NULL,',
    '  id_atto_sipo              NUMBER            NOT NULL,',
    '  id_richiesta_prenotazione NUMBER,',
    '  ty_use_case               VARCHAR2(10 CHAR),',
    '  nr_gemelli                NUMBER(2)         NOT NULL,',
    '  nr_progressivo_gemello    NUMBER(2)         NOT NULL,',
    '  fg_stesura_atto           CHAR(1 CHAR) DEFAULT \'0\' NOT NULL,',
    '  cd_operatore              VARCHAR2(40 CHAR) NOT NULL,',
    '  ts_operazione             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
    '  CONSTRAINT atti_gemellari_pk PRIMARY KEY (id_atto_gemellare),',
    '  CONSTRAINT atti_gemellari_atto_uk UNIQUE (id_atto_sipo),',
    '  CONSTRAINT atti_gemellari_prog_uk',
    '    UNIQUE (id_lavorazione_padre, nr_progressivo_gemello),',
    '  CONSTRAINT atti_gemellari_stato_fk FOREIGN KEY (id_atto_sipo)',
    '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
    '  CONSTRAINT atti_gemellari_num_ck CHECK (nr_gemelli BETWEEN 2 AND 10),',
    '  CONSTRAINT atti_gemellari_prog_ck',
    '    CHECK (nr_progressivo_gemello BETWEEN 1 AND nr_gemelli),',
    '  CONSTRAINT atti_gemellari_stesura_ck CHECK (fg_stesura_atto IN (\'0\',\'1\'))',
    ');',
    'CREATE INDEX atti_gemellari_rich_ix',
    '  ON ANSC_USR.ATTI_GEMELLARI (id_richiesta_prenotazione);',
]

COLONNE = [
    ['Colonna', 'Tipo', 'Da Side', 'Note'],
    ['id_atto_gemellare', 'NUMBER (PK)', 'No', 'Chiave tecnica della riga (IDENTITY).'],
    ['id_lavorazione_padre', 'NUMBER', 'No', 'Il parto: l’ID_ATTO del gemello 1, cioè '
     'ATTO.ID_LAVORAZIONE_PADRE dei gemelli 2…N (per il gemello 1 SIPO lascia la colonna vuota e '
     'qui si scrive il suo ID_ATTO). Raggruppa i gemelli in entrambi i percorsi.'],
    ['id_atto_sipo', 'NUMBER (FK, UK)', 'Sì, come id_evento', 'L’atto SIPO del gemello; chiave '
     'esterna verso ANSC_STATO_ATTO.ID_ATTO_SIPO.'],
    ['id_richiesta_prenotazione', 'NUMBER', 'Sì', 'La chiamata R009 /prenota/evento che ha '
     'predisposto l’atto. Vuota nel percorso B, dove la prenotazione si fa sulla web app.'],
    ['ty_use_case', 'VARCHAR2(10)', 'Sì', 'L’UC passato alla prenotazione, uno per parto. L’UC '
     'del singolo gemello sta in ANSC_STATO_ATTO.ID_UC_ANSC e in un parto misto può differire '
     '(GE-04). Vuota nel percorso B.'],
    ['nr_gemelli', 'NUMBER(2)', 'Sì', 'Numero dei gemelli del parto.'],
    ['nr_progressivo_gemello', 'NUMBER(2)', 'Sì', 'Posizione del gemello = POS_GEMELLO = '
     'progressivoGemello.'],
    ['fg_stesura_atto', 'CHAR(1)', 'Sì', '0 da stendere, 1 atto formato (firma dell’USC, o '
     'aggancio nel percorso B).'],
    ['cd_operatore', 'VARCHAR2(40)', 'Sì', 'Chi ha prenotato o, nel percorso B, staccato i '
     'numeri.'],
    ['ts_operazione', 'TIMESTAMP', 'Sì', 'Quando.'],
]


def sezione_store(d):
    heading(d, 2, 'Le righe di ANSC_STATO_ATTO nel parto plurimo')
    par(d, 'Lo store dello stato ANSC è descritto nell’analisi di integrazione [R1]: una riga per '
        'atto di SIPO, con chiave ID_ATTO_SIPO, che porta l’UC determinato, il numero comunale, '
        'l’identificativo nazionale, lo stato replicato da ANSC (ID_STATO e STATO), la fase della '
        'lavorazione locale (COD_FASE) e il modello evento in redazione (TXT_EVENTO). Il parto '
        'plurimo non cambia la tabella: cambia quante righe ci sono, quando nascono e come si '
        'tengono insieme.')

    heading(d, 3, 'Una riga per gemello')
    par(d, 'La regola discende dalla chiave. La divisione crea un atto di SIPO per ciascun nato, e '
        'ANSC tratta ogni gemello come un atto a sé, con il proprio identificativo, il proprio '
        'stato e le proprie firme. Le righe sono quindi N, una per gemello; nessuna riga '
        'rappresenta il parto nel suo insieme.')
    par(d, 'Il gemello 1 è l’atto della pratica. SIPO non crea un atto in più per la pratica: '
        'l’atto su cui si compila diventa, con la divisione, l’atto del primo nato, e gli atti '
        'dei gemelli successivi lo richiamano con ATTO.ID_LAVORAZIONE_PADRE, che per il gemello 1 '
        'resta vuota (le interrogazioni dei gemelli in AttoMatrRepository, righe 139-145 [S3], e '
        'il ramo del primo figlio in RicercaController di nascita-be, riga 2687 [S1]). La riga '
        'dello store nata nella fase dei dati, con la ricerca R005 dei genitori e del '
        'dichiarante, appartiene quindi già al gemello 1: non si sposta e non si duplica.')

    heading(d, 3, 'Quando si inseriscono e si aggiornano')
    par(d, 'Nel percorso A le righe dei gemelli 2…N nascono al passo PRENOTA GEMELLI; da lì '
        'ciascuna segue il proprio atto. La tabella riporta, momento per momento, quali righe '
        'cambiano e come.')
    tabella(d, RIGHE_STORE, [1.45, 1.25, 2.6, 1.2])
    voce(d, 'Una sola azione.', 'I due passi di PRENOTA GEMELLI sono una sola azione del '
         'concentratore: i numeri, le righe nuove e l’esito della prenotazione si registrano '
         'insieme. La chiamata ad ANSC però non può stare dentro una transazione del database; '
         'gli esiti che lascia a metà sono trattati più avanti.')
    voce(d, 'Abbinamento per numero.', 'Gli identificativi restituiti non si assegnano '
         'confidando nell’ordine delle due liste. L’identificativo nazionale contiene il numero '
         'comunale (anno, progressivo nazionale, numero comunale, codice ISTAT, come mostra la '
         'guida [A3] e come lo scompone AttoAnscBL in SIPO [S5]): ciascun idAnsc va alla riga che '
         'ha quel NUMERO_ATTO.')
    voce(d, 'Due valori nuovi.', 'COD_FASE riceve il valore PRENOTATO: l’atto esiste in ANSC come '
         'bozza predisposta, e UC e numero non si cambiano più senza cancellarlo. Fra le fasi di '
         'ANSC_LOG_AUDIT va aggiunta PRENOTAZIONE: la chiamata si registra una volta, sulla riga '
         'del gemello 1; le chiamate successive ciascuna sulla riga del proprio gemello (GE-14).')

    heading(d, 3, 'Come le righe sono legate fra loro')
    par(d, 'ANSC_STATO_ATTO non porta alcuna colonna del parto, e non deve portarne: la riga '
        'descrive un atto, e quasi tutti gli atti non sono gemellari. Il legame sta in '
        'ATTI_GEMELLARI, che ha una riga per gemello e la collega alla riga dello store con una '
        'chiave esterna: le due tabelle stanno nello stesso schema, quindi il vincolo si può '
        'dichiarare. Verso SIPO i legami restano per valore, come in tutto ANSC_USR.')
    figura(d, png('gem_erd.pptx.png'), LARGO, 'Le righe di ANSC_STATO_ATTO nel parto plurimo e i '
           'loro legami')
    tabella(d, LEGAMI, [1.15, 1.6, 1.55, 1.6, 0.6])
    par(d, 'Tutti i gemelli di un atto si ritrovano con una sola interrogazione, partendo da '
        'qualunque di essi:')
    codice(d, QUERY)

    heading(d, 3, 'Gli elenchi dei fratelli')
    par(d, 'attiGemelliPrec e attiGemelliSucc del gemello k si calcolano da questa '
        'interrogazione: i primi sono gli ID_ANSC dei gemelli con progressivo minore di k, i '
        'secondi quelli con progressivo maggiore, nell’ordine del progressivo. numeroGemelli è il '
        'numero delle righe del parto, progressivoGemello il progressivo della riga, '
        'partoGemellare vale SI. I valori si scrivono solo nel TXT_EVENTO della riga k, a ogni '
        'composizione del modello evento; non hanno una colonna propria, per la regola già '
        'dichiarata negli adattamenti a Side.')
    par(d, 'Un gemello nato morto che non si prenota (GE-03) non ha una riga in ATTI_GEMELLARI: la '
        'sua riga di ANSC_STATO_ATTO nasce e vive come quella di un atto ordinario, e il legame '
        'con il parto resta solo in SIPO. Se numeroGemelli debba contarlo comunque fa parte dello '
        'stesso punto aperto.')

    heading(d, 3, 'Gli esiti anomali della prenotazione')
    par(d, 'La prenotazione crea N atti con una sola chiamata, quindi un esito incerto riguarda N '
        'atti insieme. Vale la regola dell’analisi di integrazione [R1]: davanti a un esito '
        'indeterminato prima si verifica, poi si decide.')
    tabella(d, ANOMALIE, [1.6, 1.6, 3.3])

    heading(d, 3, 'Nel percorso B')
    par(d, 'Le righe sono le stesse e nascono prima: allo stacco dei numeri, con le stesse colonne '
        'comuni, e passano all’attesa della web app con la pagina «Dati per ANSC» [R2]. '
        'ATTI_GEMELLARI riceve le N righe nello stesso momento, con id_richiesta_prenotazione e '
        'ty_use_case vuoti, perché la prenotazione la fa l’ufficiale sulla web app. Al ritorno, '
        'DEFINISCI su ciascun gemello cerca l’atto in ANSC (R005) per numero comunale, verifica '
        'l’abbinamento e scrive sulla riga k ID_ANSC, ID_UC_ANSC, lo stato 5 FIRMATO DA USC, '
        'COD_FASE FIRMATO e il modello evento letto; fg_stesura_atto passa a 1. Un gemello non '
        'agganciato resta in attesa, e la supervisione lo mostra.')


GE_NUOVI = [
    ['GE-13', 'Esito incerto della prenotazione', 'Una prenotazione con esito indeterminato o '
     'parziale riguarda N atti. Va verificato in preproduzione che R005 ritrovi le bozze '
     'predisposte per numero comunale e data, dato che non offre un criterio di stato, e che '
     'l’identificativo nazionale restituito contenga sempre il numero comunale passato.',
     'Aperto'],
    ['GE-14', 'Allineamento con l’analisi di integrazione', 'Da riportare in [R1]: il valore '
     'PRENOTATO di COD_FASE, la fase PRENOTAZIONE di ANSC_LOG_AUDIT e la chiave di '
     'ANSC_STATO_ATTO, che la DDL dichiara su ID_ATTO_SIPO mentre la scheda descrittiva e la '
     'chiave esterna dell’audit richiamano ancora ID_STATO_ATTO. La chiave esterna di '
     'ATTI_GEMELLARI dipende da questa scelta.', 'Aperto'],
]


# ------------------------------------------------------------------ esecuzione
def main():
    d = docx.Document(IN)

    # 1. segnaposto della figura 3: descrizione allineata alla didascalia dell'utente
    t = tabella_che_contiene(d, 'riepilogo della pratica gemellare con il messaggio')
    cel = t.rows[0].cells[0]
    D.testo_di(cel.paragraphs[1], 'Schermata di SIPO: il messaggio d’errore mostrato quando la '
               'divisione della pratica non riesce e l’inserimento viene annullato. Coprire nomi e '
               'codici fiscali.')

    # 2. prenotazione sulla web app: le figure della guida
    t = tabella_che_contiene(d, 'Schermata della web app ANSC: prenotazione')
    p = segnaposto_con_immagine(d, t, webapp_png(), 5.6)
    riscrivi_didascalia(didascalia_dopo(p), 'La prenotazione sulla web app ANSC (guida operativa '
                        '[A3], figure 38-40)')

    # 3. panoramica dei due percorsi
    t = tabella_che_contiene(d, 'Diagramma a corsie (SIPO')
    p = segnaposto_con_immagine(d, t, png('gem_panoramica.pptx.png'), LARGO)

    # 4. flusso A, dopo la tabella dei passi
    ancora = para_che_inizia(d, 'Regole del passo PRENOTA GEMELLI')
    racc = in_coda(d)
    par(d, 'La figura segue il percorso su cinque corsie: la pagina di SIPO, il servizio '
        'chiamato, lo stato dell’atto in SIPO, le righe dello store ANSC_STATO_ATTO e lo stato in '
        'ANSC. Dalla banda «Per ciascun gemello» le corsie mostrano il solo gemello in '
        'lavorazione.')
    figura(d, png('gem_flusso_a.pptx.png'), 5.9, 'Percorso A: le pagine, i servizi e gli stati, '
           'con le righe dello store')
    sposta_prima(racc(), ancora._p)

    # 5. il passo PRENOTA GEMELLI: due ipotesi di schermata
    t = tabella_che_contiene(d, 'Ipotesi di schermata SIPO: riepilogo del primo gemello')
    p = segnaposto_con_immagine(d, t, png('gem_prenota_conferma.png'), LARGO)
    cap = didascalia_dopo(p)
    riscrivi_didascalia(cap, 'Il passo PRENOTA GEMELLI: il riepilogo del gemello 1 e la finestra '
                        'di conferma (ipotesi)')
    racc = in_coda(d)
    figura(d, png('gem_prenota_esito.png'), LARGO, 'Il passo PRENOTA GEMELLI: l’esito, con numero '
           'comunale, identificativo nazionale e stato ANSC di ciascun gemello (ipotesi)')
    nuovi = racc()
    for e in reversed(nuovi):
        cap._p.addnext(e)

    # 6. regola dell'esito: abbinamento per numero comunale
    D.sostituisci(d, 'Esito. Gli identificativi restituiti si assegnano ai gemelli nell’ordine di '
                  'nascita: una riga', 'Esito. Ciascun identificativo restituito si assegna al '
                  'gemello del numero comunale che contiene: una riga', attese=1)

    # 7. flusso B
    ancora = para_che_inizia(d, 'Il prezzo è il doppio inserimento')
    racc = in_coda(d)
    figura(d, png('gem_flusso_b.pptx.png'), 5.9, 'Percorso B: le pagine, i servizi e gli stati, '
           'con le righe dello store')
    sposta_prima(racc(), ancora._p)

    # 8. ATTI_GEMELLARI rivista
    D.sostituisci(d, 'Una riga per atto prenotato; le righe di un parto condividono la richiesta '
                  'di prenotazione.', 'Una riga per gemello; le righe di un parto condividono la '
                  'pratica di origine (id_lavorazione_padre), che le raggruppa anche quando la '
                  'prenotazione si fa sulla web app.', attese=1)
    vecchia = tabella_che_contiene(d, 'id_atto_gemellare')
    racc = in_coda(d)
    tabella(d, COLONNE, [1.6, 1.05, 0.9, 3.0])
    codice(d, DDL)
    nuovi = racc()
    # via la vecchia tabella, il suo paragrafo vuoto e la DDL vecchia
    e = vecchia._tbl.getnext()
    vecchia._tbl.addprevious(nuovi[0])
    for x in nuovi[1:]:
        vecchia._tbl.addprevious(x)
    via = [vecchia._tbl]
    while e is not None:
        tx = Paragraph(e, None).text.strip() if e.tag == qn('w:p') else None
        if e.tag != qn('w:p'):
            break
        via.append(e)
        if tx == ');':
            break
        e = e.getnext()
    assert Paragraph(via[-1], None).text.strip() == ');'
    for x in via:
        x.getparent().remove(x)

    adatt = tabella_che_contiene(d, 'id_lavorazione_padre e nr_atto_comunale')
    for r in adatt.rows:
        if r.cells[1].text.startswith('id_lavorazione_padre e nr_atto_comunale'):
            D.riscrivi_cella(r.cells[1], 'id_lavorazione_padre, chiave del raggruppamento.')
            D.riscrivi_cella(r.cells[2], 'Raggruppa i gemelli anche quando la prenotazione non '
                             'passa da SIPO (percorso B). Il numero comunale non si ripete: sta in '
                             'ANSC_STATO_ATTO.NUMERO_ATTO e in DATI_ATTO_ESTERNO.')
    D.sostituisci(d, 'ANSC_STATO_ATTO riceve le righe dei gemelli alla prenotazione, in BOZZA. Una '
                  'prenotazione dimenticata è un atto aperto in ANSC: la vista di supervisione del '
                  'back-office deve mostrarla.', 'ANSC_STATO_ATTO ha una riga per gemello; '
                  'quando nascono, come cambiano e come si legano è descritto nel paragrafo '
                  'seguente. Una prenotazione dimenticata è un atto aperto in ANSC: la vista di '
                  'supervisione del back-office deve mostrarla.', attese=1)

    # 9. la sezione nuova, prima dei Punti aperti
    ancora = D.h(d, 1, 'Punti aperti')
    racc = in_coda(d)
    sezione_store(d)
    sposta_prima(racc(), ancora._p)

    # 10. In sintesi: una voce
    ancora = D.h(d, 1, 'I tre stati del nato')
    racc = in_coda(d)
    voce(d, 'Nello store, una riga per gemello.', 'ANSC_STATO_ATTO ha una riga per atto di SIPO: '
         'la riga nata con la pratica diventa quella del gemello 1, le altre si inseriscono alla '
         'prenotazione. ATTI_GEMELLARI le raggruppa per pratica e lega ciascuna alla propria riga '
         'dello store; gli elenchi dei fratelli si calcolano, non si registrano.')
    sposta_prima(racc(), ancora._p)

    # 11. punti aperti e riferimenti
    op = D.trova_tabella(d, 'tema', 'questione')
    for riga in GE_NUOVI:
        D.clona_riga(op, riga)
    rif = D.trova_tabella(d, 'riferimento', 'natura')
    D.clona_riga(rif, ['[S5]', 'common/anagrafe-entities — AttoAnscBL: scomposizione '
                       'dell’identificativo nazionale in anno, numero nazionale, numero comunale e '
                       'comune.', 'Sorgente applicativo'])

    # 12. figure rinumerate nell'ordine in cui compaiono
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])

    # 13. frontespizio e storia
    for fatto in D.frontespizio(d, '0.2', NOME, DATA):
        print('  ' + fatto)
    D.storia(d, DATA, '0.2', 'In sintesi · SIPO oggi · ANSC · La modalità di integrazione · '
             'Punti aperti · Riferimenti',
             'Immagini al posto dei segnaposto: prenotazione sulla web app (dalla guida ANSC), i due '
             'percorsi, il passo PRENOTA GEMELLI; flussi a cinque corsie dei percorsi A e B. Nuova '
             'sezione sulle righe di ANSC_STATO_ATTO nel parto plurimo: una per gemello, quando si '
             'inseriscono e si aggiornano, come si legano (diagramma), elenchi dei fratelli, esiti '
             'anomali della prenotazione. ATTI_GEMELLARI raggruppa per pratica e ha la chiave '
             'esterna verso lo store. Figure rinumerate. GE-13, GE-14, [S5].')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
