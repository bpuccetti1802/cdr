# -*- coding: utf-8 -*-
"""v0.4 di «ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC» (14/11/2026).

Si modifica il FILE REALE della v0.3, che l'utente ha arricchito a mano con il capitolo
«Annotazioni - Il flusso in SIPO – Punti di intervento» e con la parte nuova del capitolo sulle
rettificative (pagina della proposta, DDL, ERD). Nessun commento di Word nel file.

Decisioni dell'utente (14/11):
  · annullamento (e, con lo stesso schema, annotazioni rettificative): devono essere possibili
    ENTRAMBE le soluzioni — web app + riallineamento (percorso A) e formazione da SIPO con R013
    (percorso B). Verificato su ANSC: guida § 9.2.1 (web app); R013 cooperativo con
    idTipoRettifica 0 (changelog 1.15.0, 1.21.0, 1.43.0 [SC]); firma USC delle rettifiche con i
    servizi cooperativi (1.32.2 → 1.37.0); i casi d'uso 2341, 14630000… non sono casi d'uso di
    servizio, quindi la disattivazione ID 120 non li tocca;
  · le tabelle nuove stanno in MATR_USR (scelta per rapidità, «ci dobbiamo tappare il naso»):
    FK dichiarate verso ANNOTAZIONE_ATTO e ANSC_STATO_ATTO, punto aperto per riallineare l'analisi.

Interventi: DDL eseguibile (virgola, spazio, schema della FK, FK nuove, COD_CANALE); due percorsi
in tutto il documento; competenza = comune, non persona; doppioni del capitolo sulle rettificative
tolti e capitolo riordinato (prima che cosa sono, poi la proposta per SIPO con pagine e DDL);
vecchia proposta di tabella sostituita da un rimando; tabelle con obbligatorietà sistemate;
formule da chat e refusi; didascalie e numerazione di tutte le figure; ERD ad alta risoluzione;
nomi e codici di persone coperti nelle schermate di sipotest; Riferimenti, Glossario, Scopo,
Storia; operazioni del concentratore; AR-07/16/21 riformulati, AR-22…AR-26.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/annullamento_v0_4.py
"""
import copy
import io
import os
import re
import sys

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.3.docx')
NOME = 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.4'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '14/11/2026'
ERD = os.path.join(QUI, 'img', 'annullamento', 'erd_annotazioni_matr_usr.png')
CAP_FLUSSO = 'Annotazioni - Il flusso in SIPO – Punti di intervento'
CAP_RETT = 'Le annotazioni rettificative: errore materiale (art. 98) e rettifica (art. 95)'

d = docx.Document(SRC)
body = d.element.body
FATTI = []


# =================================================================== primitive
def tutti_i_paragrafi():
    for p in d.paragraphs:
        yield p
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    yield p


def par(inizio, stile=None, n=1, contiene=False):
    """Paragrafi del corpo che iniziano (o contengono) un testo; ne controlla il numero."""
    trovati = [p for p in d.paragraphs
               if (inizio in p.text if contiene else p.text.strip().startswith(inizio))
               and (stile is None or p.style.name == stile)]
    if n is not None and len(trovati) != n:
        raise SystemExit('«%s»: attesi %d paragrafi, trovati %d' % (inizio[:60], n, len(trovati)))
    return trovati[0] if n == 1 else trovati


def sost(vecchio, nuovo, attese=1, etichetta=''):
    """Sostituzione che prova prima dentro un run (conserva grassetti e codice), poi sul
    paragrafo intero. Controlla il numero di occorrenze."""
    n = 0
    visti = set()
    for p in tutti_i_paragrafi():
        if p._p in visti or vecchio not in p.text:
            continue
        visti.add(p._p)
        fatto = False
        for r in p.runs:
            if vecchio in r.text:
                r.text = r.text.replace(vecchio, nuovo)
                fatto = True
                break
        if not fatto:
            if any(r.bold for r in p.runs):
                raise SystemExit('«%s» attraversa più run in un paragrafo con grassetto'
                                 % vecchio[:60])
            D.testo_di(p, p.text.replace(vecchio, nuovo))
        n += 1
    if attese is not None and n != attese:
        raise SystemExit('«%s»: attese %d occorrenze, trovate %d' % (vecchio[:60], attese, n))
    FATTI.append('%s (%d)' % (etichetta or vecchio[:50], n))


def riscrivi(p, testo):
    D.testo_di(p, testo)


def togli(el):
    el.getparent().remove(el)


def dopo_el(el):
    return el.getnext()


def clona_par(modello, testo, dopo, testa=None):
    """Copia un paragrafo (stile e carattere) e ne mette il testo; con «testa» il primo run è
    il titoletto in grassetto del modello e il secondo il corpo."""
    nuovo = copy.deepcopy(modello._p)
    dopo.addnext(nuovo)
    p = Paragraph(nuovo, modello._parent)
    runs = p.runs
    if testa is not None and len(runs) >= 2:
        runs[0].text = testa
        runs[1].text = testo
        for r in runs[2:]:
            r._r.getparent().remove(r._r)
    else:
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        if runs:
            runs[0].text = testo
            runs[0].bold = None
        else:
            p.add_run(testo)
    return p


def tabella_con(*testi):
    for t in d.tables:
        celle = [c.text.strip() for c in t.rows[0].cells] + \
                ([c.text.strip() for c in t.rows[1].cells] if len(t.rows) > 1 else [])
        if all(any(x.startswith(s) for x in celle) for s in testi):
            return t
    raise SystemExit('tabella non trovata: %s' % (testi,))


def ricostruisci(t, righe):
    """Riscrive i dati di una tabella: tiene intestazione e prima riga come modello."""
    for r in list(t.rows)[2:]:
        r._tr.getparent().remove(r._tr)
    for c, v in zip(t.rows[1].cells, righe[0]):
        D.riscrivi_cella(c, v)
    for riga in righe[1:]:
        D.clona_riga(t, riga)


def cella(t, chiave, colonna, testo):
    for r in t.rows:
        if r.cells[0].text.strip().startswith(chiave):
            D.riscrivi_cella(r.cells[colonna], testo)
            return
    raise SystemExit('riga non trovata: ' + chiave)


def heading(testo, livello):
    return par(testo, 'Heading %d' % livello)


# =================================================================== 1. immagini
def maschera(blob, rettangoli):
    im = Image.open(io.BytesIO(blob)).convert('RGB')
    dr = ImageDraw.Draw(im)
    for box, colore in rettangoli:
        if colore == 'campiona':                     # il colore del fondo, a sinistra del box
            colore = im.getpixel((box[0] - 6, (box[1] + box[3]) // 2))
        dr.rectangle(box, fill=colore)
    out = io.BytesIO()
    im.save(out, 'PNG')
    return out.getvalue()


def immagini():
    rel = d.part.related_parts
    grigio = (217, 217, 217)
    # nome dell'operatore nella testata delle schermate di sipotest
    for rid in ('rId16', 'rId23'):
        rel[rid]._blob = maschera(rel[rid].blob, [((806, 168, 888, 194), 'campiona')])
    # elenco dei risultati: ricerca per nome e cognome, codice individuale, cognome e nome
    rel['rId19']._blob = maschera(rel['rId19'].blob, [
        ((82, 240, 206, 257), 'white'), ((362, 240, 486, 257), 'white'),
        ((192, 449, 368, 508), grigio), ((192, 511, 368, 570), grigio)])
    # proposta di annotazione: titolare
    rel['rId25']._blob = maschera(rel['rId25'].blob, [
        ((214, 293, 262, 313), grigio), ((305, 293, 352, 313), grigio),
        ((247, 330, 300, 350), grigio)])
    # ERD: l'esportazione nel documento era a 720 px, illeggibile
    rel['rId27']._blob = open(ERD, 'rb').read()
    FATTI.append('schermate: nomi e codici coperti (4), ERD ad alta risoluzione')


# =================================================================== 2. testo
def testo():
    # refusi e formule da chat
    sost('PROPOSTA ANNOTAZONE', 'PROPOSTA ANNOTAZIONE')
    sost('far si che', 'far sì che', attese=2)
    sost('solo e solo se', 'solo se')
    sost('Questa pagina mostra I diversi parametri', 'Questa pagina mostra i diversi parametri')
    sost('rintracciare nel DB I record', 'rintracciare nel DB i record')
    sost('I passi da seguire sono I seguenti:', 'I passi da seguire sono i seguenti:')
    p = par('I vincoli ')
    for r in p.runs:
        if r.text == 'impost':
            r.text = 'imposti'
        r.text = r.text.replace('sono I seguenti', 'sono i seguenti')
    riscrivi(par('La funzione da chiamare'), 'La funzione da chiamare è il servizio R013 '
                                              '(contratto 1.4.0):')
    riscrivi(par('Per gli atti digitale'), 'Per gli atti digitali si è reso necessario un '
                                           'radicale ridisegno della pagina.')
    sost('Ecco un esempio per annullare', 'L’esempio che segue annulla')
    sost("L'ho costruito sul caso di prova", 'È costruito sul caso di prova')
    sost("Ho cambiato il caso d'uso, il tipo di rettifica e i dati.",
         'Sono cambiati il caso d’uso, il tipo di rettifica e i dati.')
    sost('Rispetto al caso di prova ho tolto tre gruppi di campi:',
         'Rispetto al caso di prova sono stati tolti tre gruppi di campi:')
    sost("nomeEnte è facoltativo, ma l'ho messo perché nel provvedimento c'è.",
         'nomeEnte è facoltativo, ma è valorizzato perché il provvedimento lo riporta.')
    sost("come nell'esempio precedente ho tolto i campi", 'come nell’esempio precedente sono '
                                                        'stati tolti i campi')
    sost("L'ho abbreviato con «…».", 'Nell’esempio è abbreviato con «…».')

    # la competenza: il comune, non la persona
    riscrivi(par('La competenza è dell'),
             'La competenza è dell’ufficiale dello stato civile del comune in cui l’atto è stato '
             'formato (guida operativa, § 9.2.1). Il controllo da fare è quindi sul comune: '
             'l’atto da annullare deve essere stato formato da Roma Capitale, cioè il suo comune '
             'di registrazione deve coincidere con quello della sessione. Non serve che '
             'l’ufficiale che annulla sia lo stesso che ha firmato l’atto: chiederlo '
             'bloccherebbe annullamenti legittimi, per esempio quando quell’ufficiale non è più '
             'in servizio.')

    # numero dei campi e rimando alla sezione nuova
    sost('con i 24 campi del mapping', 'con i campi del mapping (21, di cui 18 obbligatori)')
    p = par('I casi d’uso, uno per registro e per articolo, sono elencati nel capitolo')
    p.add_run(' I dati da passare, i meccanismi collegati e un esempio di chiamata sono nella '
              'sezione «Annullamento di un Atto».')

    # esempio: dettaglioRettifica = la motivazione, senza ripetere gli estremi
    p = par('"dettaglioRettifica": "Annullamento dell', contiene=True)
    riscrivi(p, p.text.split('"dettaglioRettifica"')[0] + '"dettaglioRettifica": "Annullamento '
             'dell\'atto per indebita registrazione, disposto dal provvedimento indicato",')
    t = tabella_con('Campo', 'Valore', 'Perché')
    cella(t, 'composizioneCompleta', 2,
          'La formula 190 è obbligatoria, ma il suo testo non è pubblicato: la frase è ricalcata '
          'sul caso di prova [DA VERIFICARE]. Il mapping Morte_012 non elenca '
          'composizioneCompleta: se la componga ANSC dalla formula o la debba inviare il comune '
          'non è dichiarato (AR-22).')
    D.clona_riga(t, ('dettaglioRettifica', 'la motivazione',
                     'È il «Dettaglio rettifica» del mapping, obbligatorio. Nella pagina è la '
                     'motivazione dell’annullamento: gli estremi del provvedimento stanno già in '
                     'estremiDocumento e nel testo della formula.'))
    par('Testo dell\'annotazione, nuovo.').add_run(
        ' Se lo componga SIPO o lo ricomponga ANSC non è dichiarato (AR-22).')

    # tabelle con obbligatorio e facoltativo nella stessa riga
    ricostruisci(tabella_con('Sezione', 'Campi', 'Obbligatorietà'), [
        ('Testata dell’evento', 'idUsecase dell’annotazione; tipo evento e tipo contenuto '
         '(2 = annotazione)', 'Sì'),
        ('Formazione dell’annotazione', 'numeroatto (numero comunale proprio '
         'dell’annotazione), dataformazione, ora, minuto', 'Sì'),
        ('Ente dichiarante (il tribunale)', 'enteDichiarante.estremiDocumento (estremi del '
         'provvedimento), provincia e comune dell’ente con le descrizioni', 'Sì'),
        ('', 'nomeEnte, indirizzoEnte', 'No'),
        ('Atto da annullare', 'datiRettifica.eventoCollegato: provincia e comune di '
         'registrazione con le descrizioni, numeroatto, annoAtto, dataformazione, tipologia '
         '(registro, ANSC_01)', 'Sì'),
        ('', 'datiRettifica.eventoCollegato.idAnsc', 'No'),
        ('Rettifica', 'datiRettifica.dettaglioRettifica (testo)', 'Sì'),
        ('', 'datiRettifica.idTipoRettifica = "0" (ANSC_79: 0 ANNULLAMENTO, 1 MODIFICA)',
         'Non è nel mapping: lo valorizza chi costruisce la richiesta'),
        ('Formula', '190', 'Sì'),
        ('Allegati', 'allegato generico (il provvedimento)', 'No'),
    ])
    ricostruisci(tabella_con('Sezione', 'Campi', 'Obbligatori', 'Formazione'), [
        ('Formazione', 'numeroatto (numero comunale proprio dell’annotazione), dataformazione, '
         'ora, minuto', 'Sì'),
        ('Ente dichiarante', 'estremiDocumento, provincia e comune dell’ente con le '
         'descrizioni', 'Sì'),
        ('', 'nomeEnte, indirizzoEnte', 'No'),
        ('Evento da annotare', 'evento.eventoCollegato: provincia e comune di registrazione, '
         'numeroatto, annoAtto, dataformazione, tipologia', 'Sì'),
        ('', 'evento.eventoCollegato.idAnsc', 'No'),
        ('Composizione libera', 'composizioneCompleta (il testo dell’annotazione)', 'Sì'),
        ('', 'flagAnnotazioneNonCertificabile', 'No'),
        ('Dati generali', 'decorrenza, motivoRecupero, idAttoCartaceo, flagsecretato', 'No'),
        ('Formula', '998', 'Sì'),
        ('Allegati', 'allegato generico', 'No'),
    ])
    FATTI.append('tabelle dei dati da passare: obbligatorio e facoltativo separati')


# =================================================================== 3. due percorsi
def percorsi():
    sost('L’analisi ne rinvia l’implementazione in SIPO [R1]: fino ad allora si fa sulla web '
         'app e SIPO si riallinea.',
         'Si può fare sulla web app, con il riallineamento di SIPO, oppure da SIPO con R013: i '
         'due percorsi restano entrambi disponibili.')
    sost('«ANNULLA ATTO» apre il percorso dell’annullamento ANSC (fase 1: indicazione e '
         'riallineamento).',
         '«ANNULLA ATTO» propone i due percorsi dell’annullamento ANSC: web app e '
         'riallineamento, oppure annotazione formata da SIPO.')
    sost('Fase 2: operazione di deposito della rettifica', 'Percorso B: operazione di deposito '
                                                         'della rettifica')
    sost('numero proprio per l’annotazione per rettifica (fase 2).',
         'numero proprio per l’annotazione per rettifica (percorso B).')
    sost('È lo stesso schema dell’annullamento in fase 1', 'È lo stesso schema '
                                                          'dell’annullamento nel percorso A')
    sost('seguono lo stesso destino dell’annullamento: web app e riallineamento ora, '
         'formazione da SIPO dopo.',
         'seguono lo stesso schema dell’annullamento: web app e riallineamento, oppure '
         'formazione da SIPO.')

    # sezione «Annullamento dell’atto»
    h = heading('Annullamento dell’atto: due fasi', 2)
    riscrivi(h, 'Annullamento dell’atto: due percorsi')
    p = par('Per gli atti non formati in ANSC — tutti quelli anteriori')
    riscrivi(p, p.text.replace('il documento propone quindi due fasi.',
                               'il documento propone due percorsi, entrambi disponibili: '
                               'l’ufficiale sceglie caso per caso.'))
    clona_par(p, 'Entrambi i percorsi sono ammessi da ANSC. La guida operativa descrive la '
              'rettifica di tipo annullamento sulla web app (§ 9.2.1). Con i servizi cooperativi '
              'la stessa annotazione si deposita con R013 e idTipoRettifica = 0: il contratto non '
              'chiede eventoModificato per l’annullamento (1.15.0), R013 controlla l’atto già '
              'annullato (1.21.0) e il changelog corregge espressamente la rettifica di '
              'annullamento dei servizi cooperativi (1.43.0); la firma dell’ufficiale delle '
              'rettifiche con i servizi cooperativi è stata corretta fra la 1.32.2 e la 1.37.0. I '
              'casi d’uso dell’annotazione per rettifica (2341, 14630000, 368699, 458699, 53719) '
              'non sono casi d’uso di servizio: la disattivazione dei servizi cooperativi decisa '
              'da ANSC per questi ultimi non li riguarda [R1].', p._p)
    a = par('Fase 1 — annullamento sulla web app')
    a.runs[0].text = 'Percorso A — annullamento sulla web app e riallineamento in SIPO. '
    sost('«ANNULLA ATTO» non chiama la procedura: spiega che',
         '«ANNULLA ATTO» non chiama subito la procedura: se l’ufficiale sceglie questo '
         'percorso, la pagina spiega che')
    a.add_run(' Il riallineamento registra l’annotazione anche in ANSC_ANNOTAZIONE, con '
              'COD_CANALE = WEBAPP.')
    b = par('Fase 2 — annullamento formato da SIPO')
    b.runs[0].text = 'Percorso B — annullamento formato da SIPO. '
    sost('poi gli stessi passi della fase 1.', 'poi gli stessi passi di chiusura del percorso A.')
    b.add_run(' È la pagina descritta in «La schermata di SIPO», con i dati da passare e '
              'l’esempio di chiamata della sezione «Annullamento di un Atto».')
    sost('In entrambe le fasi resta aperto', 'In entrambi i percorsi resta aperto')

    # capitolo nuovo
    riscrivi(par('Ovviamente nel caso di atto digitale'),
             'Nel caso di atto digitale, quando l’annullamento si forma da SIPO (percorso B, cfr. '
             '«Annullamento dell’atto: due percorsi»), servono più informazioni.')
    riscrivi(par('Un atto digitale soggetto'),
             'Nel percorso B un atto digitale da correggere per l’art. 98 si gestisce con R013.')

    # capitolo sulle rettificative
    sost('Si segue lo stesso criterio dell’annullamento: prima la web app con il riallineamento '
         'in SIPO, poi la formazione da SIPO.',
         'Si segue lo stesso criterio dell’annullamento: due percorsi, entrambi disponibili — la '
         'web app con il riallineamento in SIPO (A), oppure la formazione da SIPO (B).')
    riscrivi(heading('Fase 1 — web app e riallineamento', 3), 'Percorso A — web app e '
                                                              'riallineamento')
    riscrivi(heading('Fase 2 — l’annotazione formata da SIPO', 3), 'Percorso B — l’annotazione '
                                                                   'formata da SIPO')
    FATTI.append('due percorsi (A web app, B SIPO) in tutto il documento')


# =================================================================== 4. capitolo rettificative
def rettificative():
    # doppioni
    p = par('Base normativa e distinzione')
    togli(dopo_el(p._p))
    togli(p._p)
    p = par('I dati da passare: errore materiale')
    togli(dopo_el(p._p))
    togli(p._p)
    togli(par('Per la rettifica art. 95 di modifica si aggiungono')._p)
    for p in par('Meccanismi collegati', n=None):
        nx = dopo_el(p._p)
        if nx.tag == qn('w:tbl') and Table(nx, p._parent).rows[1].cells[0].text.strip() == \
                'Documenti':
            togli(nx)
            togli(p._p)
    p = par('Il servizio R013 permette la modifica dei seguenti tipi di atto:')
    togli(dopo_el(p._p))
    togli(p._p)
    riscrivi(par('Dalla nostra analisi emerge che gli atti modificabili sono dieci'),
             'I casi d’uso sono dieci, due per ciascuno dei cinque registri, tutti di tipo '
             '«annotazione» (ANSC_02 = 2) [A4]:')
    sost(' Non esiste una coppia «valore vecchio, valore nuovo»: il valore vecchio compare solo '
         'nel testo.', '', etichetta='frase ripetuta su eventoModificato')
    FATTI.append('doppioni tolti: 2 confronti art. 95/98, 2 tabelle dei dati, 1 tabella degli '
                 'effetti, 1 elenco dei casi d’uso')

    # la vecchia proposta di tabella → rimando
    p = par('Dove registrare l’annotazione')
    togli(dopo_el(p._p))                                      # tabella «Colonna proposta»
    riscrivi(p, 'Dove registrare l’annotazione: ANSC_STATO_ATTO ha per chiave l’atto di SIPO, e '
                'un’annotazione in SIPO non è un atto ma una riga del modulo delle annotazioni. '
                'Le due tabelle che la affiancano, ANSC_ANNOTAZIONE e '
                'ANSC_ANNOTAZIONE_CORREZIONE, sono descritte più avanti insieme alla pagina '
                'della proposta di annotazione.')

    # la parte nuova (pagine, DDL, ERD) passa dopo la proposta per SIPO
    corpo = list(body.iterchildren())
    h1 = heading(CAP_RETT, 1)._p
    i0 = corpo.index(h1) + 2                       # dopo l'introduzione del capitolo
    assert Paragraph(corpo[i0 - 1], d).text.startswith('Un atto firmato dall’ufficiale')
    i1 = corpo.index(heading('Che cosa sono e come si distinguono', 2)._p)
    blocco = corpo[i0:i1]
    destinazione = p._p
    modello_h3 = heading('Percorso B — l’annotazione formata da SIPO', 3)
    h3 = clona_par(modello_h3, 'La pagina della proposta di annotazione', destinazione)
    ultimo = h3._p
    for el in blocco:
        ultimo.addnext(el)
        ultimo = el
    strutture = par('Oggi la proposta vive in MATR_USR.ANNOTAZIONE_ATTO')
    clona_par(modello_h3, 'Le strutture dati della proposta',
              strutture._p.getprevious())
    cartacei = par('Gli atti cartacei. Restano annotati sul registro')
    p._p.addnext(cartacei._p)                 # resta nella proposta, prima delle pagine
    FATTI.append('capitolo sulle rettificative riordinato: %d elementi spostati' % len(blocco))

    # operazioni del concentratore
    t = tabella_con('Operazione', 'Percorso', 'Servizio ANSC')
    cella(t, 'creaAnnotazioneRettificativa', 3,
          'Nuova. Riceve il tipo (art. 95 di modifica o di annullamento, art. 98), i dati '
          'corretti e, per l’art. 95, il provvedimento; il concentratore compone evento ed, '
          'escluso l’annullamento, eventoModificato.')
    for riga in [
        ('creaAnnotazione', 'POST /ansc/v1/atti/{idAtto}/annotazioni', 'R009 /validazione/evento',
         'Nuova. Annotazione integrativa da altra amministrazione o da altro comune (casi '
         'd’uso di servizio _998_1 e _998_2).'),
        ('creaAnnotazioneModificativa', 'POST /ansc/v1/atti/{idAtto}/annotazioni-modificative',
         'R013 /annotazione/modificativa/validazione', 'Nuova. Annotazioni modificative '
         'specifiche (AR-23).'),
        ('annullaAtto', 'Esistente [R1]', 'R011', 'Scarto di un’annotazione depositata e non '
         'firmata, se ANSC lo ammette (AR-24).'),
    ]:
        D.clona_riga(t, riga)


# =================================================================== 5. DDL e strutture
def ddl():
    def trova(frammento):
        norm = ' '.join(frammento.split())
        t = [p for p in d.paragraphs if p.style.name == 'HTML Preformatted'
             and norm in ' '.join(p.text.split())]
        if len(t) != 1:
            raise SystemExit('DDL «%s»: %d righe' % (frammento, len(t)))
        return t[0]

    def riga(frammento, nuova):
        p = trova(frammento)
        riscrivi(p, nuova)
        return p

    riga('-- legami con SIPO, per valore',
         '    -- legami con SIPO: FK dichiarate, le tabelle stanno tutte in MATR_USR')
    riga('ID_ANNOTAZIONE_ATTO NUMBER,',
         '    ID_ANNOTAZIONE_ATTO         NUMBER,                   -- FK ANNOTAZIONE_ATTO.ID '
         '(assente per l’annullamento)')
    riga('ID_ATTO_SIPO NUMBER',
         '    ID_ATTO_SIPO                NUMBER          NOT NULL, -- FK '
         'ANSC_STATO_ATTO.ID_ATTO_SIPO (l’atto annotato)')
    riga('UTENTE_FIRMA VARCHAR2(40)',
         '    UTENTE_FIRMA                VARCHAR2(40),             -- l’ufficiale che ha '
         'firmato (R007)')
    fase = trova('COD_FASE VARCHAR2(20)')
    clona_par(fase, '    COD_CANALE                  VARCHAR2(10)    NOT NULL, -- SIPO '
                    '(percorso B) | WEBAPP (percorso A, riallineata)', fase._p)
    ck = trova('CONSTRAINT CK_ANSC_ANNOT_FASE CHECK')
    ultimo = ck._p.getprevious()
    for t in ['    CONSTRAINT FK_ANSC_ANNOT_PROPOSTA FOREIGN KEY (ID_ANNOTAZIONE_ATTO)',
              '        REFERENCES MATR_USR.ANNOTAZIONE_ATTO (ID),',
              '    CONSTRAINT FK_ANSC_ANNOT_STATO_ATTO FOREIGN KEY (ID_ATTO_SIPO)',
              '        REFERENCES MATR_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
              '    CONSTRAINT CK_ANSC_ANNOT_CANALE CHECK (COD_CANALE IN (\'SIPO\',\'WEBAPP\')),']:
        ultimo = clona_par(ck, t, ultimo)._p
    sost('MATR _USR.ANSC_ANNOTAZIONE', 'MATR_USR.ANSC_ANNOTAZIONE')
    sost('REFERENCES ANSC_USR.ANSC_ANNOTAZIONE', 'REFERENCES MATR_USR.ANSC_ANNOTAZIONE')
    FATTI.append('DDL: virgola, spazio, schema della FK, 2 FK nuove, COD_CANALE')

    riscrivi(par('Nella nostra visione'),
             'Nella nostra visione la tabella nuova non deve duplicare la struttura di SIPO. '
             'ANNOTAZIONE_ATTO resta la riga principale, con testo e flusso di oggi. La tabella '
             'nuova contiene solo ciò che serve ad ANSC e sta, come ANNOTAZIONE_ATTO, nello '
             'schema MATR_USR: i legami con la proposta e con lo stato dell’atto in ANSC sono FK '
             'dichiarate. Si propongono due tabelle: una testata e le righe delle correzioni. La '
             'stessa testata serve anche all’annullamento (R013 con tipo 0) e alle annotazioni '
             'da altra amministrazione (R009), e registra anche le annotazioni fatte sulla web '
             'app e riallineate (percorso A, COD_CANALE = WEBAPP). L’annullamento non passa da '
             'ANNOTAZIONE_ATTO, per questo il collegamento alla proposta è facoltativo.')
    sost('seguono [R5], come il resto di', 'seguono lo standard dei modelli dati [R5], come le '
                                           'tabelle')
    p = par('Nomi e convenzioni')
    for r in p.runs:
        if r.text == 'ANSC_USR':
            r.text = 'dell’integrazione'
    audit = par('ANSC_LOG_AUDIT', 'Normal')
    clona_par(audit, 'Le tabelle stanno in MATR_USR, accanto ad ANNOTAZIONE_ATTO: è una scelta '
              'dettata dai tempi, che permette di dichiarare le FK verso la proposta e verso lo '
              'stato dell’atto. Si discosta dall’analisi [R1], che tiene le tabelle '
              'dell’integrazione nello schema dedicato ANSC_USR per separare domini di guasto e '
              'cicli di vita: va riconsiderata (AR-25).', audit._p, testa='Lo schema. ')
    t = tabella_con('Momento', 'ANNOTAZIONE_ATTO')
    D.clona_riga(t, ('Riallineamento (percorso A)', '—',
                     'Riga con COD_CANALE = WEBAPP e fase FIRMATA, scritta da «RIALLINEA DA '
                     'ANSC» con ID_ANSC, NUMERO_ATTO e stato letti con R005; nessuna riga di '
                     'correzione.', 'R005 (lettura)'))


# =================================================================== 6. didascalie
DIDASCALIE = {
    'rId16': 'La ricerca degli atti di SIPO oggi: la linguetta «Estremi pratica» della Gestione '
             'Nascite (nome dell’operatore coperto).',
    'rId17': 'Le due soluzioni per la ricerca per identificativo ANSC: la casella che cambia il '
             'significato di Numero Atto (a sinistra) e il campo aggiuntivo (a destra).',
    'rId19': 'L’elenco dei risultati di SIPO oggi (nomi e codici coperti).',
    'rId20': 'L’elenco dei risultati proposto: per l’atto digitale il numero tradizionale tra '
             'parentesi e l’identificativo ANSC in grassetto.',
    'rId21': 'Il dettaglio dell’atto di SIPO oggi.',
    'rId22': 'Il dettaglio dell’atto proposto per un atto digitale.',
    'rId23': 'La pagina dell’annullamento di SIPO oggi (nome dell’operatore coperto).',
    'rId24': 'La pagina dell’annullamento proposta per un atto digitale (percorso B, R013).',
    'rId25': 'La proposta di annotazione di SIPO oggi (nomi e codici coperti).',
    'rId26': 'La proposta di annotazione proposta per un atto digitale: errore materiale '
             '(art. 98).',
    'rId27': 'Le tabelle delle annotazioni verso ANSC, tutte in MATR_USR.',
}


def didascalie():
    modello = par('Figura 1 — ')
    for p in list(d.paragraphs):
        rids = [b.get(qn('r:embed')) for b in p._p.iter(qn('a:blip'))]
        chiave = next((r for r in rids if r in DIDASCALIE), None)
        if chiave:
            clona_par(modello, 'Figura 0 — ' + DIDASCALIE[chiave], p._p)
    n = 0
    for p in d.paragraphs:
        m = re.match(r'^Figura \d+ — ', p.text)
        if m:
            n += 1
            riscrivi(p, re.sub(r'^Figura \d+', 'Figura %d' % n, p.text))
    FATTI.append('didascalie aggiunte: %d; figure numerate: %d' % (len(DIDASCALIE), n))


# =================================================================== 7. testata e coda
APERTI = [
    ('AR-22', 'Chi compone composizioneCompleta per l’annotazione per rettifica: il mapping '
     'Morte_012 non lo elenca (dichiara la formula 190 e il «Dettaglio rettifica»), il caso di '
     'prova ufficiale lo invia già composto. Se ANSC lo ricompone, SIPO non lo invia.',
     'Analisi / Sogei'),
    ('AR-23', 'Con quale servizio si deposita l’annotazione modificativa generica: R009 o R013 '
     '/annotazione/modificativa. Il changelog cita una correzione su «R009 Validazione caso '
     '14850000», il mapping usa datiAnnotazioneModificativa.', 'Analisi / Sogei'),
    ('AR-24', 'Scarto di un’annotazione depositata e non ancora firmata: se R011 la accetti e '
     'con quale esito; altrimenti resta in ANSC come bozza.', 'Analisi / Sogei'),
    ('AR-25', 'Collocazione delle tabelle dell’integrazione: in questo documento stanno in '
     'MATR_USR, per rapidità; l’analisi [R1] le tiene nello schema dedicato ANSC_USR. Va '
     'scelta una sola collocazione e riallineato l’altro documento, con le FK e i permessi che '
     'ne seguono.', 'Analisi / Comune'),
    ('AR-26', 'Come SIPO viene a sapere di un annullamento o di un’annotazione rettificativa '
     'fatti sulla web app senza partire da SIPO: ANSC non avvisa il comune che ha formato '
     'l’atto. Stesse opzioni di AR-12: adempimento dell’ufficio, controllo all’apertura del '
     'dettaglio o controllo periodico.', 'Analisi / Comune'),
]


def coda():
    t = tabella_con('#', 'Questione', 'Owner')
    cella(t, 'AR-07', 1,
          'Annotazioni integrative da altra amministrazione (R009, casi d’uso _998_1 e _998_2) e '
          'modificative specifiche (R013 /annotazione/modificativa): il documento ne dà servizi '
          'e dati, non ancora la pagina di SIPO né la regola che sceglie il caso d’uso a '
          'partire dal tipo di annotazione.')
    cella(t, 'AR-16', 1,
          'Da quale serie venga il numero comunale dell’annotazione: il mapping lo chiede '
          'obbligatorio e nessuna fonte dice se sia la serie degli atti. Il documento assume la '
          'serie degli atti, con il numero staccato alla conferma da be-numeratore-comunale; da '
          'confermare.')
    cella(t, 'AR-21', 1,
          'Raccordo con il modulo delle annotazioni di SIPO: la riga di ANNOTAZIONE_ATTO è ora '
          'legata ad ANSC_ANNOTAZIONE (ID_ANNOTAZIONE_ATTO). Resta da stabilire come i tipi di '
          'CONF_TIPO_ANNOTAZIONE e le formule di SIPO corrispondano ai casi d’uso e alle formule '
          'ANSC: la formula SIPO «190 – Art. 98» corrisponde alla formula ANSC 888, mentre la '
          '190 di ANSC è quella dell’art. 95. Si lega ad AR-07.')
    for riga in APERTI:
        D.clona_riga(t, riga)
    sost('Ventuno questioni, accanto agli OP-80…OP-84', 'Ventisei questioni, accanto agli '
                                                      'OP-80…OP-84')

    riscrivi(par('Il modulo delle annotazioni di SIPO resta fuori da questo documento'),
             'I capitoli «' + CAP_FLUSSO + '» e «' + CAP_RETT + '» trattano la proposta di '
             'annotazione per gli atti digitali — annullamento, errore materiale e rettifica — e '
             'le tabelle ANSC_ANNOTAZIONE e ANSC_ANNOTAZIONE_CORREZIONE che la affiancano. Per '
             'un atto formato in ANSC ogni annotazione è un atto ANSC (casi d’uso _998_*, R009, '
             'R013) e le annotazioni generate da altri comuni arrivano come notifiche [R1]: le '
             'altre annotazioni del modulo — integrative da altra amministrazione e modificative '
             'specifiche — seguono lo stesso schema, ma la loro pagina è ancora da descrivere '
             '(AR-07).')

    # scopo
    sost('compresi gli atti cartacei. Le questioni ancora da decidere sono raccolte in coda, '
         'come punti aperti AR-01…AR-21',
         'compresi gli atti cartacei. Un capitolo raccoglie i punti di intervento nelle pagine '
         'di SIPO — ricerca, elenco, dettaglio, annullamento e proposta di annotazione — per gli '
         'atti digitali. Le questioni ancora da decidere sono raccolte in coda, come punti '
         'aperti AR-01…AR-26')

    # riferimenti
    sost('ANALISI_Integrazione-ANSC_v3.58.docx', 'ANALISI_Integrazione-ANSC_v3.60.docx')
    sost('ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.5.docx', 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_'
                                                          'v0.7.docx')
    sost('ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.1.docx',
         'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.8.docx')
    rif = tabella_con('#', 'Riferimento', 'Natura')
    for riga in [
        ('[R5]', 'Naming_convention_X_DB_v1.01.docx — lo standard di nomenclatura dei modelli '
         'dati: marcatori, prefissi di colonna, nomi dei vincoli.', 'Standard aziendale'),
        ('[S5]', 'Template di statocivile-web e nascita-web (gestioneNascita.html, '
         'dettaglioAttoStatoCivile.html, annullamentoCancellazione.html, '
         'propostaAnnotazione1/2.html) ed entity di common/matrim-entities (ANNOTAZIONE_ATTO, '
         'ANNOTAZIONE_TAG_VALUES, CONF_FORMULA_ANNOTAZIONE).', 'Sorgente applicativo'),
    ]:
        D.clona_riga(rif, riga)

    glos = tabella_con('Termine', 'Significato in questo doc')
    for riga in [
        ('Atto digitale', 'Un atto formato in ANSC, con identificativo ANSC. L’atto tradizionale '
         'ha soltanto gli estremi del registro.'),
        ('Percorso A, percorso B', 'Le due vie per l’annullamento e per le annotazioni '
         'rettificative di un atto digitale: sulla web app con il riallineamento di SIPO (A), '
         'oppure formate da SIPO con R013 (B). Restano entrambe disponibili.'),
    ]:
        D.clona_riga(glos, riga)

    for f in D.frontespizio(d, '0.4', NOME, DATA):
        FATTI.append(f)
    D.storia(d, DATA, '0.4', 'Annotazioni - Il flusso in SIPO · Annotazioni rettificative · '
             'Dove e come inserirsi · Punti aperti',
             'Rilettura di coerenza della versione arricchita a mano. Annullamento e annotazioni '
             'rettificative con due percorsi entrambi disponibili (web app e riallineamento, '
             'oppure formazione da SIPO con R013), verificati sulle fonti ANSC. DDL eseguibile '
             'con le tabelle in MATR_USR, FK verso la proposta e verso lo stato dell’atto, '
             'canale; vecchia proposta di tabella sostituita. Competenza riferita al comune. '
             'Doppioni tolti e capitolo sulle rettificative riordinato. Didascalie e '
             'numerazione delle figure, ERD ad alta risoluzione, dati personali coperti nelle '
             'schermate. Operazioni del concentratore, Riferimenti, Glossario. AR-07, AR-16 e '
             'AR-21 riformulati; AR-22…AR-26.')


if __name__ == '__main__':
    immagini()
    testo()
    percorsi()
    rettificative()
    ddl()
    didascalie()
    coda()
    d.save(OUT)
    for f in FATTI:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
