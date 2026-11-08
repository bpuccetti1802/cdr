# -*- coding: utf-8 -*-
"""v3.57 dell'analisi ANSC (07/11/2026), dalla v3.56 salvata (03/11, 17:11) sul file reale.

Recepisce la comunicazione ANSC sui casi d'uso di servizio fornita dal committente
(`Sorgenti Documentali/Comunicazione_ANSC_Casi-uso-servizio_servizi-cooperativi.txt`):
dal 09/09/2024 i 10 casi d'uso di servizio delle dichiarazioni non sono disponibili tramite
servizi cooperativi (solo web app, con il motivo indicato dall'ufficiale); restano
cooperativi i 5 delle trascrizioni e quelli delle annotazioni (fase ibrida). I casi d'uso di
servizio non generano annotazioni automatiche, non controllano i metadati, non predispongono
le comunicazioni anagrafiche. ANSC suggerisce servizi di recupero degli atti registrati sulla
web app.

Interventi SOLO ADDITIVI (paragrafi nuovi, frasi in coda, righe nuove), per non toccare le
ancore dei commenti di Word:
  - «Indisponibilità e rientro»: il caso d'uso di servizio non è più il veicolo del rientro
    delle dichiarazioni dal gestionale; il mapping dichiara motivoRecupero solo nei casi d'uso
    di servizio e in alcuni di annotazione (famiglia _998) -> OP-85.
  - «Atti a Testo Libero»: paragrafo con il rinvio al documento dedicato [R16].
  - «Funzionalità disponibili solo sulla web app»: riga nuova.
  - «L'aggancio di un atto formato sulla web app»: il recupero è suggerito da ANSC.
  - Parto plurimo (cap. funzioni ANSC, R009): 11999999 non più cooperativo -> OP-46.
  - Scheda R009, «Avvertenze»: frase in coda.
  - Registro: OP-46 e OP-78 integrati, nuovo OP-85; Riferimenti R15, R16; Storia.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_57_casi_uso_servizio.py
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.56.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.57.docx')
DATA = '07/11/2026'

d = docx.Document(SRC)


def conta_commenti():
    return len(d.element.body.findall('.//' + qn('w:commentRangeStart')))


COMMENTI = conta_commenti()


def trova(inizio, stile=None):
    t = [p for p in d.paragraphs if p.text.strip().startswith(inizio)
         and (stile is None or p.style.name == stile)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:60]))
    return t[0]


def dopo(p, testo, grassetto_iniziale=None):
    """Paragrafo nuovo dopo p, con le proprietà di paragrafo di p e testo semplice."""
    nuovo = docx.oxml.OxmlElement('w:p')
    p._p.addnext(nuovo)
    q = Paragraph(nuovo, p._parent)
    if p._p.pPr is not None:
        q._p.insert(0, copy.deepcopy(p._p.pPr))
    if grassetto_iniziale:
        q.add_run(grassetto_iniziale + ' ').bold = True
    q.add_run(testo)
    return q


def in_coda(p, testo):
    """Aggiunge una frase in fondo al paragrafo, senza toccare i run esistenti."""
    p.add_run(' ' + testo)


def riga_di(chiave, intestazione=None):
    t = [(tb, r) for tb in d.tables for r in tb.rows if r.cells[0].text.strip() == chiave
         and (intestazione is None or tb.rows[0].cells[0].text.strip() == intestazione)]
    if len(t) != 1:
        raise SystemExit('attesa 1 riga, trovate %d: %s' % (len(t), chiave))
    return t[0]


def coda_cella(chiave, colonna, testo):
    c = riga_di(chiave)[1].cells[colonna]
    c.paragraphs[-1].add_run(' ' + testo)


def riga_dopo(chiave, valori, intestazione=None):
    """Riga nuova subito dopo quella di «chiave», con la sua formattazione."""
    _, r = riga_di(chiave, intestazione)
    tr = copy.deepcopy(r._tr)
    r._tr.addnext(tr)
    from docx.table import _Row
    nuova = _Row(tr, r._parent)
    for cella, val in zip(nuova.cells, valori):
        for p in cella.paragraphs[1:]:
            p._p.getparent().remove(p._p)
        p = cella.paragraphs[0]
        if not p.runs:
            p.add_run('')
        for x in p.runs[1:]:
            x._r.getparent().remove(x._r)
        p.runs[0].text = val
    return nuova


# ------------------------------------------------------------ riferimenti
riga_dopo('R14', ['R15', 'Sorgenti Documentali/Comunicazione_ANSC_Casi-uso-servizio_servizi-'
                         'cooperativi.txt',
                  'Comunicazione ANSC sui casi d’uso di servizio, in vigore dal 09/09/2024 '
                  '(nel registro dei rilasci: voce «ID 120» del rilascio 1.33.0). I dieci delle '
                  'dichiarazioni non sono più disponibili tramite servizi cooperativi; restano '
                  'quelli delle trascrizioni e delle annotazioni, per la fase ibrida.'])
riga_dopo('R15', ['R16', 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.4.docx',
                  'Analisi degli atti a testo libero e degli atti senza UC determinabile: le due '
                  'strategie della web app per le dichiarazioni, il percorso interamente in SIPO '
                  'per le trascrizioni, i servizi ANSC da usare.'])

# ------------------------------------------------------------ rientro
p = trova('Il veicolo del rientro non è un servizio dedicato')
dopo(p, 'Una comunicazione successiva di ANSC [R15] restringe però questo veicolo. Dal 9 '
        'settembre 2024 i dieci casi d’uso di servizio delle dichiarazioni non sono più '
        'disponibili tramite servizi cooperativi: si usano solo sulla web app, dove l’ufficiale '
        'deve indicare il motivo del ricorso, e ANSC ne chiede un uso monitorato e limitato ai '
        'casi strettamente necessari, perché non generano annotazioni automatiche, non '
        'consentono il controllo dei metadati e non predispongono le comunicazioni anagrafiche. '
        'Restano cooperativi i cinque delle trascrizioni e quelli delle annotazioni, necessari '
        'alla fase ibrida. Ne segue che il rientro di una dichiarazione con il caso d’uso di '
        'servizio non si fa più dal gestionale ma dalla web app. Dal gestionale resta il '
        'deposito con il caso d’uso specifico, nel quale però il mapping non prevede il motivo '
        'del recupero: lo dichiara soltanto nei casi d’uso di servizio e in alcuni casi d’uso di '
        'annotazione. [DA VERIFICARE: se R009 accetti e conservi il motivo del recupero su un '
        'caso d’uso specifico] (OP-85).')

# ------------------------------------------------------------ atti a testo libero
p = trova('Un altro elemnto da non sottovalutare')
dopo(p, 'Il tema è sviluppato nel documento dedicato [R16], che tiene conto di una comunicazione '
        'ANSC [R15]. I casi d’uso di servizio delle dichiarazioni — il corrispettivo ANSC '
        'dell’atto a testo libero — sono disponibili solo sulla web app: per le dichiarazioni le '
        'due modalità sono quindi l’unica via. Quelli delle trascrizioni restano disponibili '
        'tramite servizi cooperativi, e per le trascrizioni l’atto a testo libero può formarsi '
        'interamente in SIPO, finché dura la fase ibrida. In ogni caso un atto formato con caso '
        'd’uso di servizio non genera annotazioni automatiche né comunicazioni anagrafiche: '
        'quegli adempimenti restano all’ufficio.')

# ------------------------------------------------------------ solo web app
riga_dopo('Annullamento per inefficacia',
          ['Formazione con i casi d’uso di servizio delle dichiarazioni',
           'Dal 9 settembre 2024 i dieci casi d’uso di servizio delle dichiarazioni non sono '
           'disponibili tramite servizi cooperativi; sulla web app l’ufficiale deve indicare il '
           'motivo del ricorso [R15]. Restano cooperativi quelli delle trascrizioni e delle '
           'annotazioni.',
           'Una dichiarazione a testo libero, o senza UC applicabile, nasce sempre sulla web app '
           'e va riportata in SIPO con l’aggancio.'], intestazione='Funzione')

# ------------------------------------------------------------ aggancio
p = trova('Dove il recupero si fa, il modo è quello proposto in revisione')
dopo(p, 'Il recupero non è una scelta del solo Comune. ANSC stessa suggerisce alle case software '
        'di sviluppare servizi per il recupero degli atti registrati sulla web app, per mantenere '
        'l’allineamento con i gestionali locali e svolgere gli adempimenti successivi alla '
        'registrazione [R15]. È la contropartita dei casi d’uso che il gestionale non può più '
        'depositare.')

# ------------------------------------------------------------ parto plurimo
p = trova('Il caso d’uso è quello di servizio.')
dopo(p, 'Il caso d’uso 11999999 non è più disponibile tramite servizi cooperativi dal 9 settembre '
        '2024 [R15], e la guida colloca la prenotazione nel menu della web app. Se la prenotazione '
        'con R009 /prenota/evento e il completamento delle bozze siano ancora possibili dal '
        'gestionale è da verificare (OP-46).', grassetto_iniziale='Il caso d’uso non è più '
                                                                  'cooperativo.')

# ------------------------------------------------------------ scheda R009
in_coda(trova('Avvertenze. Ripetere la chiamata deposita un secondo evento.'),
        'I casi d’uso di servizio delle dichiarazioni non sono accettati tramite servizi '
        'cooperativi dal 9 settembre 2024; quelli delle trascrizioni e delle annotazioni sì '
        '[R15].')

# ------------------------------------------------------------ registro degli open point
coda_cella('OP-46', 2, 'Si aggiunge un vincolo: il caso d’uso 11999999 non è più disponibile '
                       'tramite servizi cooperativi dal 9 settembre 2024 [R15]; va accertato se '
                       'la prenotazione e il completamento delle bozze siano ancora possibili dal '
                       'gestionale o solo dalla web app.')
coda_cella('OP-78', 2, 'Per il punto (b) vedi [R16]: per le dichiarazioni il testo libero passa '
                       'necessariamente dalla web app, per le trascrizioni può restare in SIPO.')
riga_dopo('OP-79', ['OP-85', 'Rientro delle dichiarazioni senza caso d’uso di servizio',
                    'Dal 9 settembre 2024 i casi d’uso di servizio delle dichiarazioni non sono '
                    'disponibili tramite servizi cooperativi [R15]. Va accertato se il rientro di '
                    'una dichiarazione lavorata in emergenza possa avvenire dal gestionale con il '
                    'caso d’uso specifico e il motivo del recupero, che il mapping non dichiara per '
                    'quei casi d’uso, oppure debba passare dalla web app con l’aggancio successivo.'])
# le colonne di stato, responsabile e priorità ricalcano OP-79: si riscrivono esplicitamente
_, r85 = riga_di('OP-85')
for i, val in ((3, 'Aperto'), (4, 'Analisi / Fornitore ANSC'), (5, 'Alta')):
    if i < len(r85.cells):
        c = r85.cells[i]
        c.paragraphs[0].runs[0].text = val
        for x in c.paragraphs[0].runs[1:]:
            x._r.getparent().remove(x._r)

# ------------------------------------------------------------ testata e storia
for fatto in D.frontespizio(d, '3.57', 'ANALISI_Integrazione-ANSC_v3.57'):
    print('  ' + fatto)
D.storia(d, DATA, '3.57',
         'Vincoli ANSC (rientro) · Atti a Testo Libero · SIPO e la web app · Funzioni ANSC (R009, '
         'parto plurimo) · Schede (R009) · Open Point · Riferimenti',
         'Recepita la comunicazione ANSC sui casi d’uso di servizio: dal 9 settembre 2024 quelli '
         'delle dichiarazioni sono disponibili solo sulla web app, quelli delle trascrizioni e '
         'delle annotazioni restano cooperativi per la fase ibrida. Il caso d’uso di servizio non '
         'è più il veicolo del rientro delle dichiarazioni dal gestionale (OP-85); la '
         'dichiarazione a testo libero nasce sempre sulla web app e si recupera con l’aggancio, '
         'che ANSC stessa suggerisce; il parto plurimo va riverificato (OP-46). Rinvio al '
         'documento sugli atti a testo libero [R16].')

# la testata di pagina scrive «Versione 3.56»: frontespizio() riconosce solo «…vX.Y»
for sez in d.sections:
    for t in sez.header.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip() == 'Versione 3.56':
                    D.riscrivi_cella(c, 'Versione 3.57')

assert conta_commenti() == COMMENTI, 'ancore di commento cambiate'
d.save(OUT)
print('commenti (ancore):', COMMENTI)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
