# -*- coding: utf-8 -*-
"""v3.56 dell'analisi ANSC, dalla v3.55 salvata dall'utente (31/10/2026).

Decisioni dell'utente (01/11/2026) sull'annullamento dell'atto in ANSC:

  1. R011 porta l'atto a 9 CANCELLATO (non 3 ANNULLATO) ovunque, con la fonte: il contratto
     non lo dichiara, lo dicono ANSC_11, il changelog 1.23.0 e il flusso di Side;
  2. tabella degli stati: «Cancellazione prima della firma dell'ufficiale», e la riga
     «3 ANNULLATO INEFFICACE» divisa in due (rettifica di annullamento / inefficacia);
  3. annullamento per inefficacia: disabilitato dalla 1.52.0 (04/06/2026), tolto «solo per
     duplicati, entro un mese», che nelle fonti non c'è;
  4. il 9 CANCELLATO scritto su un atto senza idAnsc è un uso locale, come lo stato 0;
  5. capitolo della cancellazione: esito di R011 e ciò che R011 non sistema;
  6. diagramma: si ritocca il .pptx DELL'UTENTE (non si rigenera da
     diagramma_cancella_pratica_pptx.py, che perderebbe le sue modifiche) e si sostituisce il
     PNG esportato da PowerPoint.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_56_cancellazione.py pptx
      → poi esportare da PowerPoint in strumenti/img/cancella_pratica/Diapositiva1.png
    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_56_cancellazione.py docx
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402
from v3_53_ddl_sviluppatori import sost, par, dopo  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.55.docx')
OUT = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.56.docx')
PPTX = os.path.join(QUI, 'img', 'cancella_pratica.pptx')
PNG = os.path.join(QUI, 'img', 'cancella_pratica', 'Diapositiva1.png')

FONTE_9 = ('Il contratto R011 non dichiara lo stato che ne risulta (la risposta è il solo '
           'involucro): lo indicano la decodifica ANSC_11, in cui lo stato 9 CANCELLATO compare '
           'dal 20/12/2023, il changelog della versione 1.23.0 («R011: Cancellazione Atto – '
           'Eliminazione fisica / annullamento») e il flusso di Side, che a risposta positiva '
           'scrive 9 sull’evento.')


# ───────────────────────────────────────────────────────────── PowerPoint
def _testo_forma(forma, righe):
    """Riscrive i paragrafi di una forma conservando il carattere del primo run di ciascuno."""
    paragrafi = forma.text_frame.paragraphs
    if len(paragrafi) != len(righe):
        raise SystemExit(f'{forma.name}: {len(paragrafi)} paragrafi, attesi {len(righe)}')
    for p, testo in zip(paragrafi, righe):
        p.runs[0].text = testo
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)


def pptx():
    from pptx import Presentation
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    prs = Presentation(PPTX)
    forme = {s.name: s for s in prs.slides[0].shapes}
    nuovi = {
        'Rounded Rectangle 21': ['Stato dell’atto a “9 CANCELLATO”',
                                 'solo su ANSC_STATO_ATTO, uso locale · '
                                 'l’atto in ANSC non esiste'],
        'Rounded Rectangle 27': ['Vincolo ANSC: R011 rifiuta l’atto 5 FIRMATO DA USC. SIPO lo '
                                 'controlla prima sullo stato replicato, come Side; per gli '
                                 'stati 4 e 11 [DA VERIFICARE].'],
        'Rounded Rectangle 30': ['Cancellazione interrotta',
                                 'la pratica resta in SIPO · R005 legge lo stato reale: se è '
                                 'già 9 CANCELLATO si allinea e si conclude, altrimenti '
                                 'l’atto va fra le eccezioni'],
        'Rounded Rectangle 33': ['Stato dell’atto a “9 CANCELLATO”',
                                 'su ANSC_STATO_ATTO · numero comunale scartato (PUT /scarta)'],
    }
    for nome, righe in nuovi.items():
        _testo_forma(forme[nome], righe)
    # i due esiti di R011 ora sono descritti nel documento: bordo pieno
    for nome in ('Rounded Rectangle 30', 'Rounded Rectangle 33'):
        forme[nome].line.dash_style = MSO_LINE_DASH_STYLE.SOLID
    prs.save(PPTX)
    print('scritto:', PPTX)


# ───────────────────────────────────────────────────────────── 1. stato dopo R011
def stato_r011(doc):
    sost(doc, 'eliminabile via R011 [DA VERIFICARE: se lo stato che ne risulta sia 3 ANNULLATO '
              'o 9 CANCELLATO, che il contratto non dichiara])',
         'eliminabile via R011, che lo porta a 9 CANCELLATO)')
    sost(doc, 'eventuale R011 «annulla» → ANNULLATO.', 'eventuale R011 → 9 CANCELLATO.')
    sost(doc, 'RIFIUTATA (provvedimento di rifiuto R016), ANNULLATO (R011))',
         'RIFIUTATA (provvedimento di rifiuto R016), CANCELLATO (R011))')
    sost(doc, 'RIFIUTATA per provvedimento di rifiuto R016, ANNULLATO via R011,',
         'RIFIUTATA per provvedimento di rifiuto R016, CANCELLATO via R011,')
    sost(doc, 'R011 «annulla» → ANNULLATO. Prima della validazione',
         'R011 «elimina» → CANCELLATO, possibile solo prima della firma dell’USC. '
         + FONTE_9 + ' Prima della validazione')
    sost(doc, 'L’atto passa ad ANNULLATO. L’identificativo nazionale resta consumato.',
         'L’atto passa a 9 CANCELLATO. L’identificativo nazionale resta consumato.')


# ───────────────────────────────────────────────────────────── 2. tabella degli stati
def tabella_stati(doc):
    t = next(t for t in doc.tables if t.rows[0].cells[0].text.strip() == 'Momento')
    for r in t.rows:
        if r.cells[0].text.startswith('Cancellazione della firma'):
            D.riscrivi_cella(r.cells[0], 'Cancellazione prima della firma dell’ufficiale')
            break
    else:
        raise SystemExit('riga della cancellazione non trovata')
    riga = next(r for r in t.rows if r.cells[1].text.startswith('3 ANNULLATO'))
    nuova = copy.deepcopy(riga._tr)
    riga._tr.addnext(nuova)
    D.riscrivi_cella(riga.cells[1], '3 ANNULLATO')
    D.riscrivi_cella(riga.cells[2],
                     'rettifica di tipo annullamento (R013 e caso d’uso «Annotazione per '
                     'rettifica») [DA VERIFICARE: le fonti dicono che inibisce certificati ed '
                     'estratti, non quale stato assuma l’atto rettificato]')
    seconda = next(r for r in t.rows if r._tr is nuova)
    D.riscrivi_cella(seconda.cells[0], 'Dopo la formazione')
    D.riscrivi_cella(seconda.cells[1], '10 INEFFICACE')
    D.riscrivi_cella(seconda.cells[2],
                     'annullamento per inefficacia, solo dalla web app; disabilitato dalla '
                     'versione 1.52.0 del 04/06/2026')


# ───────────────────────────────────────────────────────────── 3. inefficacia
def inefficacia(doc):
    sost(doc, 'Solo per duplicati, entro un mese dalla formazione.',
         'Disabilitata dalla versione 1.52.0 del 04/06/2026 («Disabilitazione servizio di '
         'annullamento per inefficacia»).')
    sost(doc, 'restano l’annullamento per inefficacia, solo dalla web app ed entro un mese, '
              'oppure l’annotazione di rettifica.',
         'resta l’annotazione di rettifica di tipo annullamento (R013); l’annullamento per '
         'inefficacia, solo dalla web app, è disabilitato dalla versione 1.52.0. Lo stato che '
         'R011 produce è 9 CANCELLATO: il contratto non lo dichiara, lo indicano la decodifica '
         'ANSC_11, il changelog 1.23.0 e il flusso di Side.')
    sost(doc, 'e l’unica azione di annullamento disponibile ai servizi cooperativi.',
         'e l’unica via, fra i servizi cooperativi, per eliminare un evento non ancora formato; '
         'un atto già formato si annulla con la rettifica di tipo annullamento (R013).')


# ───────────────────────────────────────────────────────────── 4. 9 senza idAnsc
def uso_locale(doc):
    sost(doc, 'Prima della validazione in ANSC non esiste alcun atto e il codice è vuoto.',
         'Prima della validazione in ANSC non esiste alcun atto e il codice è vuoto. Fa '
         'eccezione la cancellazione di una pratica mai depositata: il 9 CANCELLATO scritto su '
         'un atto senza idAnsc è un uso locale, come lo stato 0 (si veda il capitolo '
         '«Annullamento/Cancellazione Atto in lavorazione»).')


# ───────────────────────────────────────────────────────────── 5. capitolo della cancellazione
def capitolo(doc):
    p = par(doc, 'Non è stato valorizzato IdANSC. In tal caso bisognerà assegnare')
    D.testo_di(p, p.text.rstrip() + '. È un uso locale: l’atto in ANSC non esiste e lo stato '
               'non replica nulla.')
    p = par(doc, 'Se è stato valorizzato IdANSC allora dovrà essere richiamata la funzione R011')
    D.testo_di(p, 'Se è stato valorizzato IdANSC allora dovrà essere richiamata la funzione R011, '
               'trattandone l’esito come descritto in «Se R011 non va a buon fine».')

    # coda del capitolo: prima del capitolo successivo
    succ = D.h(doc, 1, 'Il flusso in ingresso')
    ancora = succ._p

    def h2(testo):
        D.para(doc, ancora, testo, stile='Heading 2')

    def testo(t):
        D.para(doc, ancora, t)

    def elenco(testa, corpo):
        D.para(doc, ancora, stile='List Paragraph', pezzi=D.segmenta(testa, corpo))

    h2('Lo stato dopo la cancellazione')
    testo('La cancellazione con R011 porta l’atto in ANSC allo stato 9 CANCELLATO. ' + FONTE_9
          + ' Lo stato 3 ANNULLATO è un’altra cosa: riguarda un atto già formato e nasce dalla '
          'rettifica di tipo annullamento (R013), non da R011.')
    testo('Prima della chiamata SIPO controlla lo stato replicato su ANSC_STATO_ATTO, come fa '
          'Side: con 5 FIRMATO DA USC la cancellazione non si propone, perché ANSC la '
          'rifiuterebbe (il controllo è stato aggiunto a R011, come riporta il changelog). Per '
          'gli stati 4 FIRMATO DAL DICHIARANTE e 11 FIRMATO PER CONFORMITA le fonti non dicono '
          'se R011 li accetti [DA VERIFICARE].')

    h2('Se R011 non va a buon fine')
    testo('R011 risponde 200 a cancellazione riuscita, 400 per dati non validi, 403 se l’utente '
          'non è autorizzato e 404 se il modello evento non è presente in ANSC; fra i codici '
          'di errore pubblicati i pertinenti sono 400003, 401003 «Evento non valido», 404001 e '
          '406003 «Evento non trovato». La risposta non riporta lo stato. In caso di errore:')
    elenco('La pratica non si cancella. ', 'In SIPO resta com’è e lo stato su ANSC_STATO_ATTO '
           'non cambia.')
    elenco('Si legge lo stato reale con R005. ', 'Se l’atto risulta già 9 CANCELLATO — per '
           'esempio dopo un esito indeterminato — si allinea la riga e si conclude in SIPO; se '
           'risulta firmato dall’USC la cancellazione non è più possibile e resta la rettifica; '
           'negli altri casi si mostra l’errore ANSC e l’atto compare fra le eccezioni della '
           'vista di supervisione.')
    elenco('Un timeout non è un errore. ', 'L’esito è indeterminato e si chiude con R005, come '
           'per gli altri passi verso ANSC: mai una seconda chiamata alla cieca.')
    testo('Side, in caso di errore, si limita al messaggio «Disallineamento tra sipo e ANSC».')

    h2('Ciò che R011 non sistema')
    testo('La cancellazione dell’evento non porta con sé gli oggetti collegati all’atto, che '
          'vanno trattati dal Comune:')
    elenco('Gli allegati. ', 'R001 non ha un’operazione di cancellazione: i documenti già '
           'trasmessi restano in ANSC.')
    elenco('Il link di firma elettronica. ', 'Se al dichiarante è stato inviato un link di firma '
           '(R012) non ancora usato, si annulla con /firmadichiarante/annulla-link [DA '
           'VERIFICARE: se R011 lo invalidi da sé].')
    elenco('Il numero comunale. ', 'Se all’atto era associato un numero, si segna come '
           'scartato con PUT /scarta di be-numeratore-comunale; altrimenti nella ricerca dei '
           'numeri resta assegnato a un atto che non esiste.')


# ───────────────────────────────────────────────────────────── 6. figura
def figura(doc):
    p = par(doc, 'Concludere l’operazione in SIPO')
    for el in p._p.itersiblings():
        blips = el.findall('.//' + qn('a:blip'))
        if blips:
            rid = blips[0].get(qn('r:embed'))
            doc.part.related_parts[rid]._blob = open(PNG, 'rb').read()
            return
    raise SystemExit('figura del capitolo non trovata')


def main_docx():
    doc = docx.Document(SRC)
    stato_r011(doc)
    tabella_stati(doc)
    inefficacia(doc)
    uso_locale(doc)
    capitolo(doc)
    figura(doc)
    D.storia(doc, '01/11/2026', '3.56',
             'Vincoli imposti dal contratto ANSC · Modello dati · Il processo di gestione dei '
             'dati ANSC in SIPO · Annullamento/Cancellazione Atto in lavorazione · SIPO e la '
             'web app ANSC · Schede dei servizi ANSC',
             'Lo stato prodotto da R011 è 9 CANCELLATO, non 3 ANNULLATO: corretto in tutti i '
             'punti, con la fonte. Nella tabella degli stati separati 3 ANNULLATO (rettifica di '
             'annullamento) e 10 INEFFICACE. L’annullamento per inefficacia è disabilitato dalla '
             'versione 1.52.0 di ANSC. Il 9 CANCELLATO senza idAnsc è un uso locale. Il capitolo '
             'sulla cancellazione descrive l’esito di R011 e ciò che R011 non sistema (allegati, '
             'link di firma, numero comunale); diagramma aggiornato.')
    D.frontespizio(doc, '3.56', 'ANALISI_Integrazione-ANSC_v3.56')
    doc.save(OUT)
    print('scritto:', OUT)


if __name__ == '__main__':
    {'pptx': pptx, 'docx': main_docx}[sys.argv[1]]()
