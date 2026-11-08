# -*- coding: utf-8 -*-
"""v0.3 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC» (07/11/2026), dalla v0.2 sul file reale.

Rilievo dell'utente: il §5.4 «Il terzo percorso, se ANSC lo consente» poggiava ancora sul
presupposto superato dalla v0.2, cioè che il deposito cooperativo del caso d'uso di servizio
fosse escluso salvo concessione del fornitore. Corretto il presupposto, il contratto R009 non
pone restrizioni: il terzo percorso (atto a testo libero formato interamente in SIPO) diventa
il PERCORSO DI RIFERIMENTO, da verificare con una prova in preproduzione; le due strategie
della web app restano come RIPIEGO.

Riallineati a cascata: §2.3 ultimo paragrafo, §5.2 ultima frase, §5.4 (titolo e testo),
introduzione del cap. 6, introduzione dei punti aperti, TL-01; corretta la riga 0.2 della
Storia, che citava il §5.3 invece del §5.4.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/testo_libero_v0_3.py
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import _versa   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.2.docx')
NOME = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.3'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '07/11/2026'

d = docx.Document(SRC)


def _svuota(p):
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)


def paragrafo(inizio, nuovo, stile=None):
    trovati = [p for p in d.paragraphs if p.text.startswith(inizio)
               and (stile is None or p.style.name == stile)]
    if len(trovati) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(trovati), inizio[:60]))
    p = trovati[0]
    if D.ha_commenti(p._p):
        raise SystemExit('paragrafo commentato: ' + inizio[:60])
    _svuota(p)
    _versa(p, nuovo)
    return p


def dopo(p, testo):
    nuovo = docx.oxml.OxmlElement('w:p')
    p._p.addnext(nuovo)
    q = Paragraph(nuovo, p._parent)
    if p._p.pPr is not None:
        q._p.insert(0, copy.deepcopy(p._p.pPr))
    _versa(q, testo)
    return q


def cella(chiave, colonna, nuovo):
    trovate = [r for t in d.tables for r in t.rows if r.cells[0].text.strip() == chiave]
    if len(trovate) != 1:
        raise SystemExit('attesa 1 riga, trovate %d: %s' % (len(trovate), chiave))
    c = trovate[0].cells[colonna]
    for extra in c.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    _svuota(c.paragraphs[0])
    _versa(c.paragraphs[0], nuovo, dim=9)


# ------------------------------------------------------------------ §2.3
paragrafo('Non è quindi accertato che un gestionale',
          'Non è quindi accertato che un gestionale comunale non possa depositare con R009 un '
          'atto con caso d’uso di servizio, e il contratto non lo vieta. Ne discende un terzo '
          'percorso, in cui l’atto a testo libero si forma interamente in SIPO: è descritto '
          'nelle considerazioni ed è proposto come **percorso di riferimento**, da verificare '
          'con una prova in preproduzione (TL-02). Le due strategie del capitolo successivo, '
          'che passano dalla web app, restano come **ripiego** se la prova non riesce.')

# ------------------------------------------------------------------ §5.2
paragrafo('Così la doppia immissione non scompare',
          'Così la doppia immissione non scompare: diventa un **controllo**. Il prezzo è '
          'accettare che, nel caso scoperto tardi, il lavoro fatto in SIPO serva da riscontro '
          'e non da fonte. La proposta vale se l’atto deve formarsi sulla web app, cioè nel '
          'ripiego: il percorso di riferimento è il terzo, descritto qui sotto.')

# ------------------------------------------------------------------ §5.4
titolo = [p for p in d.paragraphs if p.style.name == 'Heading 2'
          and p.text.strip() == 'Il terzo percorso, se ANSC lo consente']
assert len(titolo) == 1
_svuota(titolo[0])
titolo[0].add_run('Il terzo percorso: l’atto formato interamente in SIPO')

paragrafo('SIPO ha già la pagina del testo libero',
          'Le due strategie nascono da un presupposto: che l’atto a testo libero debba '
          'formarsi sulla web app. Il presupposto non regge. Il contratto di R009 non pone '
          'restrizioni sui casi d’uso ammessi, e la sola riga che parla di una disabilitazione '
          'non ne dice la portata, mentre altri elementi vanno in senso contrario (§2.3). '
          'SIPO ha già la pagina del testo libero, e il caso d’uso di servizio chiede poco più '
          'della minuta. L’atto a testo libero può quindi formarsi **interamente in SIPO**, '
          'con i servizi cooperativi, senza andare sulla web app e senza importazione:')

p = paragrafo('Sarebbe il percorso più coerente',
              'Rispetto al percorso degli altri atti cambiano due cose sole. Il **testo** viene '
              'dalla pagina del testo libero (`ATTO_TESTO_LIBERO`) invece di essere composto, e '
              'va in `composizioneCompleta`. L’**UC** non si determina: è il caso d’uso di '
              'servizio del registro e del tipo di contenuto, uno dei quindici del §2.2, con il '
              'motivo del recupero 3. Validazione, firme, attestazione di conformità e chiusura '
              'sono quelle già disegnate per gli altri atti [R1].')
p = dopo(p, 'È il percorso più coerente con un sistema che resta SIPO-centrico: un solo luogo '
            'di immissione, nessuno stato sospeso, nessuna transcodifica inversa, nessun '
            'ritorno da presidiare. Copre anche il caso scoperto al Riepilogo: senza UC '
            'determinato, l’atto passa alla pagina del testo libero di SIPO conservando i dati '
            'già compilati, invece di essere steso di nuovo sulla web app. La differenza fra le '
            'due origini si riduce così al momento in cui si apre la pagina del testo libero. '
            'Per queste ragioni il documento lo propone come **percorso di riferimento**, e '
            'tiene le due strategie della web app come **ripiego**.')
paragrafo('Se lo si adotta, due cautele.',
          'Prima di costruirlo serve una verifica sola: **provare in preproduzione il deposito '
          'con R009 di un atto con caso d’uso di servizio**, almeno una volta per tipo di '
          'contenuto (atto e trascrizione). È il punto su cui le fonti sono incerte, e la '
          'risposta di ANSC a un deposito non ammesso non è documentata: nessuno dei codici di '
          'errore pubblicati la descrive [A3]. La conferma del fornitore (TL-02) completa la '
          'prova ma non la sostituisce. Se la prova fallisce, si adotta il ripiego. Restano '
          'comunque sulla web app le funzioni che solo lì esistono: la modifica successiva dei '
          'certificati emissibili [A2] e la nota tecnica.')

# ------------------------------------------------------------------ cap. 6
paragrafo('Nelle due strategie SIPO non deposita e non firma',
          'Nel percorso di riferimento SIPO usa i servizi della formazione degli altri atti, '
          'elencati con i loro passi nel paragrafo «Il terzo percorso». Le tabelle che seguono '
          'riguardano il ripiego: nelle due strategie SIPO non deposita e non firma, lo fa la '
          'web app, e i servizi che SIPO chiama sono quindi quasi tutti **letture**, '
          'concentrate nel ritorno. Nelle colonne G1 e G2, «sì» indica il servizio necessario, '
          '«cond.» quello necessario solo in una condizione, «facolt.» quello facoltativo, '
          '«ind.» quello usato indirettamente.')

# ------------------------------------------------------------------ punti aperti
paragrafo('Dieci questioni restano da chiudere.',
          'Dieci questioni restano da chiudere. La prima è la scelta della strategia; la '
          'seconda decide se il percorso di riferimento sia praticabile; le altre servono a '
          'completare il disegno, e in buona parte riguardano il solo ripiego (TL-03…TL-07). '
          'I punti si legano a OP-66, OP-71, OP-78 e OP-79 dell’analisi di integrazione [R1].')
cella('TL-01', 1, 'Quale strategia adottare: il terzo percorso, interamente in SIPO, se la '
                  'prova del deposito con caso d’uso di servizio riesce (TL-02); altrimenti, '
                  'come ripiego, la Gestione 2 come percorso unico, con la Gestione 1 ridotta '
                  'a deviazione verso di essa (proposta di questo documento), oppure entrambe.')

# ------------------------------------------------------------------ storia
storia = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
riga = [r for r in storia.rows if r.cells[1].text.strip() == '0.2']
assert len(riga) == 1
D.riscrivi_cella(riga[0].cells[2], '2.2 · 2.3 · 5.2 · 5.4 · 6 · Punti aperti · Riferimenti')
for fatto in D.frontespizio(d, '0.3', NOME):
    print('  ' + fatto)
D.storia(d, DATA, '0.3', '2.3 · 5.2 · 5.4 · 6 · Punti aperti',
         'Il terzo percorso, con l’atto a testo libero formato interamente in SIPO, poggiava '
         'ancora sul presupposto superato nella v0.2. Diventa il percorso di riferimento, da '
         'verificare con una prova in preproduzione del deposito con caso d’uso di servizio; '
         'le due strategie della web app restano come ripiego. Precisato che rispetto agli '
         'altri atti cambiano soltanto il testo e l’UC. Riallineati l’introduzione dei servizi, '
         'TL-01 e la riga 0.2 della Storia.')

d.save(OUT)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
