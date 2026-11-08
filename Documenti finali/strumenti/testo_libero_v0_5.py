# -*- coding: utf-8 -*-
"""v0.5 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC» (07/11/2026), dalla v0.4 sul file reale.

Inserisce il capitolo «Le pagine di SIPO: dal Riepilogo senza UC al recupero dell’atto», fra «Le
due strategie proposte» e le considerazioni, con il flusso logico e le pagine disegnate su
richiesta dell'utente (strumenti/schermate_testo_libero.py e schermate_recupero_ansc.py, figure in
img/testo_libero/). Riallinea i servizi (R005 /consultazione/ansc/soggetto/sintetico per la ricerca
per intestatario), gli effetti sul disegno e i punti aperti (TL-12: numero comunale diverso).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/testo_libero_v0_5.py
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import _versa, figura, h, par, tabella, voce   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
IMG = os.path.join(QUI, 'img', 'testo_libero')
SRC = os.path.join(FIN, 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.4.docx')
NOME = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.5'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '07/11/2026'

d = docx.Document(SRC)
body = d.element.body


def img(nome):
    return os.path.join(IMG, nome)


# ------------------------------------------------------------------ il capitolo nuovo
prima = len(list(body.iterchildren()))

h(d, 1, 'Le pagine di SIPO: dal Riepilogo senza UC al recupero dell’atto')
par(d, 'Il capitolo disegna le pagine di SIPO per una **dichiarazione** di cui al Riepilogo non si '
       'identifica un UC: è il percorso della Gestione 1, con il ritorno in SIPO comune anche alla '
       'Gestione 2. Le pagine partono da schermate reali di SIPO (Riepilogo, Anteprima, Gestione '
       'Decessi), ritoccate secondo la sequenza indicata dal committente; i numeri gialli sulle '
       'figure sono i passi della sequenza. L’esempio è un atto di morte in abitazione a Roma.')

h(d, 2, 'Il flusso logico')
par(d, 'Il flusso va dalla determinazione dell’UC alla conclusione dell’atto in SIPO. A destra '
       'sono indicati i servizi chiamati; in viola il lavoro che l’ufficiale svolge sulla WebApp, '
       'fuori da SIPO.')
figura(d, img('tl_flusso_recupero.png'), 5.2,
       'Figura 2 — Atto senza UC: dalla WebApp ANSC al recupero in SIPO.')
par(d, 'Due cicli regolano il ritorno. Se fra gli atti del giorno non c’è il numero comunale '
       'staccato, si passa alla ricerca puntuale; se anche questa non trova l’atto, l’atto SIPO '
       'resta nello stato YY · SOSPESO e la ricerca si ripete più tardi, con il back-office che ne '
       'segnala l’anzianità.')

h(d, 2, 'Passi 1-3 — il Riepilogo senza UC')
figura(d, img('tl_1_riepilogo_senza_uc.png'), 6.3,
       'Figura 3 — Riepilogo senza UC: messaggio, bottone di prosecuzione inibito, DATI PER ANSC.')
voce(d, '1 — Il messaggio.',
     'Quando il Riepilogo non identifica un UC, la pagina mostra: «Attenzione: Non è stato '
     'identificato uno Usecase ANSC. Si prega di passare alla WebApp per formare un atto a testo '
     'libero. Al termine delle operazioni sulla webApp rientrare in Sipo per completare le '
     'operazioni».')
voce(d, '2 — Il bottone di prosecuzione è inibito.',
     'È il bottone che porta all’Anteprima, nella pagina reale chiamato CONFERMA: senza UC il '
     'percorso ordinario non può proseguire.')
voce(d, '3 — DATI PER ANSC.',
     'Il bottone nuovo stacca il numero comunale (`be-numeratore-comunale` `POST /richiesta`) e '
     'apre l’Anteprima.')

h(d, 2, 'Passi 4-5 — l’Anteprima con il numero comunale')
figura(d, img('tl_2_anteprima_numero.png'), 6.3,
       'Figura 4 — Anteprima: il numero comunale in alto e COPIA TESTO.')
voce(d, '4 — Il numero comunale, in alto e ben visibile.',
     'Un pannello in testa alla pagina riporta il numero staccato e l’anno, con l’istruzione di '
     'riportarlo nel campo «Numero comunale» dell’atto sulla WebApp; lo stesso numero compare '
     'evidenziato nella testata dell’atto.')
voce(d, '5 — COPIA TESTO.',
     'Il bottone nuovo copia negli appunti il testo dell’atto redatto in SIPO, da incollare nella '
     'composizione libera sulla WebApp. Da qui l’atto SIPO passa nello stato YY · SOSPESO e il '
     'numero comunale resta Disponibile fino al rientro.')

h(d, 2, 'Passo 6 — il recupero: gli atti del giorno')
figura(d, img('tl_3_recupero_atti_del_giorno.png'), 6.3,
       'Figura 5 — Recupero dell’atto ANSC: gli atti del giorno, con evidenziato il numero '
       'comunale staccato.')
par(d, 'Al rientro, la pagina «Recupero Atto ANSC» propone gli atti formati nel giorno, ottenuti '
       'con R005 `/consultazione/ansc/evento`. I criteri sono già compilati:')
tabella(d, [
    ['Criterio nella pagina', 'Valore proposto', 'In R005'],
    ['Data da, Data a', 'il giorno corrente', '`dataDa`, `dataA`'],
    ['Comune di registrazione', 'ROMA (RM), in sola lettura',
     '`idComuneRegistrazione` = 8165, l’identificativo di Roma nell’archivio dei comuni di ANPR '
     '(l’esempio del contratto, 2780, è Cesena)'],
    ['Tipo evento', 'quello del tipo atto (MORTE)', '`idTipoEvento`, decodifica ANSC_01 (2)'],
    ['Stato', '5 - FIRMATO DA USC',
     'Nessun criterio: R005 non filtra per stato. SIPO filtra la risposta sul campo `stato`.'],
    ['Numero comunale atteso', 'il numero staccato, in sola lettura',
     'Non è un criterio: SIPO confronta `numeroatto` di ogni atto e **evidenzia e preseleziona** '
     'quello che coincide.'],
], [1.8, 2.0, 3.1])
par(d, 'Lo stato 5 della decodifica ANSC_11 è FIRMATO DA USC, cioè l’atto chiuso sulla WebApp. Lo '
       'stato CONFERMATO è il 2, e indica un atto validato ma non ancora firmato: non va '
       'recuperato. La tabella dei risultati riporta identificativo ANSC, numero comunale, data e '
       'ora di formazione, UC con la descrizione, intestatario, data di nascita e stato.')

h(d, 2, 'La ricerca puntuale')
figura(d, img('tl_4_recupero_ricerca_puntuale.png'), 6.3,
       'Figura 6 — Recupero dell’atto ANSC: la ricerca puntuale.')
par(d, 'Se fra gli atti del giorno il numero comunale non compare, la pagina lo dice e propone la '
       'seconda linguetta, con due modi di cercare:')
voce(d, 'Per atto.',
     'Con l’identificativo ANSC, se l’ufficiale lo ha annotato, oppure con il numero comunale su un '
     'intervallo di date più largo: R005 `/consultazione/ansc/evento` con `idAnsc`, oppure '
     '`idComunale`, `dataDa` e `dataA`.')
voce(d, 'Per intestatario.',
     'Con cognome, nome, data di nascita o codice fiscale: R005 '
     '`/consultazione/ansc/soggetto/sintetico`, che restituisce gli eventi del soggetto.')
par(d, 'Il caso tipico è l’atto chiuso dopo la mezzanotte, fuori dall’intervallo degli atti del '
       'giorno, oppure un numero comunale scritto in modo diverso sulla WebApp (TL-12).')

h(d, 2, 'Il riepilogo dell’atto ANSC e la conferma')
figura(d, img('tl_5_riepilogo_atto_ansc.png'), 6.3,
       'Figura 7 — Riepilogo dell’atto ANSC prima della conferma.')
par(d, 'Selezionato l’atto, il riepilogo mostra ciò che SIPO registrerà:')
voce(d, 'Atto ANSC.',
     'Identificativo ANSC, stato, numero comunale con il riscontro rispetto al numero staccato, '
     'anno, data e ora di formazione, comune di registrazione.')
voce(d, 'Caso d’uso.',
     'Codice e descrizione (la descrizione dalla decodifica ANSC_03), e il motivo del recupero.')
voce(d, 'Intestatari.',
     'Per ciascuno cognome, nome, sesso, data e luogo di nascita, cittadinanza e identificativo '
     'ANSC del soggetto.')
voce(d, 'Che cosa SIPO aggiorna.',
     'L’atto SIPO (identificativo ANSC, anno, numero comunale, data di formazione), lo stato ANSC e '
     'il contrassegno di atto a testo libero, il numero comunale che passa da Disponibile a '
     'Utilizzato (`PUT /utilizza`), gli identificativi dei soggetti, in anagrafe solo dove mancano.')
figura(d, img('tl_6_conferma.png'), 6.3,
       'Figura 8 — La conferma, che aggiorna SIPO e conclude l’operazione.')
par(d, 'La conferma è esplicita: una finestra riepiloga identificativo ANSC e numero comunale e '
       'avverte che l’operazione conclude l’atto in SIPO. Lo stato finale dell’atto SIPO resta da '
       'stabilire (TL-04).')

nuovi = list(body.iterchildren())[prima - 1:]   # il primo nuovo prende il posto di sectPr
nuovi = [e for e in nuovi if e.tag != qn('w:sectPr')]
ancora = [p for p in d.paragraphs if p.style.name == 'Heading 1'
          and p.text.strip() == 'Considerazioni sulle due strategie']
assert len(ancora) == 1
for e in nuovi:
    ancora[0]._p.addprevious(e)


# ------------------------------------------------------------------ riallineamenti
def trova(inizio):
    t = [p for p in d.paragraphs if p.text.startswith(inizio)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:50]))
    return t[0]


def svuota(p):
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)


def riga_di(colonna0, colonna1=None):
    t = [(tb, r) for tb in d.tables for r in tb.rows if r.cells[0].text.strip() == colonna0
         and (colonna1 is None or r.cells[1].text.strip() == colonna1)]
    if len(t) != 1:
        raise SystemExit('attesa 1 riga, trovate %d: %s %s' % (len(t), colonna0, colonna1))
    return t[0]


def scrivi(c, testo):
    for extra in c.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    svuota(c.paragraphs[0])
    _versa(c.paragraphs[0], testo, dim=9)


def riga_dopo(r, valori):
    tr = copy.deepcopy(r._tr)
    r._tr.addnext(tr)
    from docx.table import _Row
    nuova = _Row(tr, r._parent)
    for c, v in zip(nuova.cells, valori):
        scrivi(c, v)


p = trova('Riprende il capitolo «Atti a Testo Libero»')
testo = p.text.replace('TL-01…TL-11', 'TL-01…TL-12').replace(
    'quali servizi ANSC occorrono.', 'quali servizi ANSC occorrono, e come si presentano le pagine '
    'di SIPO.')
svuota(p)
_versa(p, testo)

_, r = riga_di('R005', '/consultazione/ansc/evento')
scrivi(r.cells[5], 'Atti del giorno: `dataDa`/`dataA`, `idComuneRegistrazione` 8165, `idTipoEvento`; '
                   'lo stato si filtra in SIPO. Ricerca puntuale: `idAnsc`, oppure `idComunale` e '
                   'date.')
riga_dopo(r, ['R005', '/consultazione/ansc/soggetto/sintetico',
              'Ricerca puntuale per intestatario: restituisce gli eventi del soggetto.',
              'cond.', 'cond.', 'Solo se fra gli atti del giorno il numero comunale non compare.'])

_, r = riga_di('Conclusione dell’atto')
riga_dopo(r, ['Pagine di SIPO',
              'Riepilogo senza UC con il messaggio e DATI PER ANSC; pannello del numero comunale e '
              'COPIA TESTO nell’Anteprima; pagina nuova «Recupero Atto ANSC» con due linguette; '
              'pagina nuova «Riepilogo Atto ANSC» con la conferma.'])

p = trova('Undici questioni restano da chiudere.')
testo = p.text.replace('Undici questioni', 'Dodici questioni')
svuota(p)
_versa(p, testo)
_, r = riga_di('TL-11')
riga_dopo(r, ['TL-12', 'Che cosa fare se l’atto ritrovato porta un numero comunale diverso da quello '
                       'staccato: bloccare la conferma, oppure consentirla con un avviso e chiudere '
                       'come Scartato il numero staccato. Un numero sbagliato in un atto firmato si '
                       'corregge solo con la nota tecnica sulla WebApp.', 'Cliente / Analisi'])

for fatto in D.frontespizio(d, '0.5', NOME):
    print('  ' + fatto)
D.storia(d, DATA, '0.5', 'Nuovo capitolo «Le pagine di SIPO» · 1 · 6 · 7 · Punti aperti',
         'Aggiunti il flusso logico e le pagine di SIPO per la dichiarazione senza UC: Riepilogo '
         'con il messaggio di rinvio, Anteprima con il numero comunale in alto e COPIA TESTO, '
         'recupero dell’atto con R005 (atti del giorno e ricerca puntuale), riepilogo dell’atto ANSC '
         'e conferma. Aggiunta la ricerca per intestatario fra i servizi, le pagine fra gli effetti '
         'sul disegno e TL-12.')

d.save(OUT)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
