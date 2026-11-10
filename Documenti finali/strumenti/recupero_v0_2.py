# -*- coding: utf-8 -*-
"""v0.2 di «ANALISI_Recupero-Atti-WebApp_SIPO-ANSC» (10/11/2026).

Si modifica il FILE REALE della v0.1, rivisto a mano dall'utente (tolto RW-13; RW-14 risolto:
il numero passa a «Scartato» dopo n giorni configurabili). Richiesta: un'idea di interfaccia
nel back-office per effettuare il recupero. Nuovo capitolo «La pagina del back-office per il
recupero» prima di «Che cosa succede dopo», con tre wireframe (pagine_bo_recupero.py):
elenco (numeri in attesa + ricerca in ANSC), aggancio, esito. Punti aperti RW-15, RW-16.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/recupero_v0_2.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import figura, h, par, tabella, voce   # noqa: E402
import pagine_bo_recupero as PB   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.1.docx')
NOME = 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.2'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '10/11/2026'
CAP = 'La pagina del back-office per il recupero'
IMG = PB.DEST

d = docx.Document(SRC)
body = d.element.body


def heading(testo, livello):
    t = [p for p in d.paragraphs if p.style.name == 'Heading %d' % livello
         and p.text.strip() == testo]
    if len(t) != 1:
        raise SystemExit('heading non univoco: ' + testo)
    return t[0]


def innesta(prima, scrivi):
    sect = body.find(qn('w:sectPr'))
    n0 = len(list(body.iterchildren()))
    scrivi()
    nuovi = [ch for ch in list(body.iterchildren())[n0 - 1:] if ch is not sect
             and ch.getparent() is body]
    for ch in nuovi:
        prima.addprevious(ch)
    return len(nuovi)


# =================================================================== tabelle
PAGINE = [
    ['Pagina', 'Scopo', 'Si arriva da', 'Servizi', 'Tabelle'],
    ['Recupero dalla web app', 'Vedere i numeri staccati in attesa dell’atto e gli atti di Roma '
     'formati in ANSC; trovare quelli da agganciare e le anomalie.', 'Menu «Integrazione ANSC»',
     'cercaNumeri di be-numeratore-comunale; R005 per il tramite del concentratore',
     'DATI_ATTO_ESTERNO, ANSC_STATO_ATTO (lettura)'],
    ['Aggancio dell’atto', 'Rileggere l’atto in ANSC, controllarlo contro il numero e l’atto di '
     'SIPO, scegliere il livello, confermare.', 'La spunta di una riga ABBINABILE, o la matita '
     'di un numero in attesa', 'R005 (rilettura), agganciaAtto',
     'ANSC_STATO_ATTO, DATI_ATTO_ESTERNO, MATR_USR.ATTO (lettura)'],
    ['Esito', 'Dire che cosa è stato scritto, dove, e che cosa non si è fatto di proposito.',
     'AGGANCIA', '—', 'ANSC_LOG_AUDIT (lettura)'],
]

ELENCO = [
    ['Elemento', 'Contenuto', 'Da dove viene'],
    ['Distintivo di sessione', 'Validità e minuti residui del codice di sessione verso ANSC; '
     'senza sessione la ricerca e l’aggancio sono inibiti.', 'Sessione del concentratore [R7]'],
    ['In sintesi', 'Tre conteggi: numeri in attesa, numeri in scadenza (meno di 2 giorni alla '
     'soglia), atti di Roma trovati in ANSC con un numero che SIPO non ha staccato.',
     'be-numeratore-comunale e ultima ricerca in ANSC'],
    ['Numeri staccati in attesa', 'Numero, data dello stacco, operatore, municipio, tipo atto '
     'previsto, atto SIPO in attesa (se c’è), giorni trascorsi, esito dell’ultima ricerca. '
     'Ordinati per anzianità; in giallo i numeri prossimi alla soglia.',
     'DATI_ATTO_ESTERNO (stato Disponibile, destinazione web app: RW-16)'],
    ['Azioni sul numero', 'Occhio: scheda del numero. Matita: ricerca in ANSC per numero '
     'comunale e, se l’atto c’è, apertura dell’aggancio.', 'R005, criterio idComunale (RW-04)'],
    ['Ricerca in ANSC', 'Intervallo di date (predefinito: oggi), tipo evento, numero comunale, '
     'identificativo ANSC, filtro sull’abbinamento.', 'R005 con il comune di Roma (RW-05)'],
    ['Risultati', 'Identificativo ANSC, numero, data, caso d’uso, intestatario, stato ANSC, '
     'abbinamento calcolato da SIPO.', 'Risposta R005 confrontata con DATI_ATTO_ESTERNO e '
     'ANSC_STATO_ATTO'],
    ['Esporta', 'Le due tabelle in un foglio di calcolo, per il controllo di fine giornata.',
     '—'],
]

ABBINAMENTI = [
    ['Abbinamento', 'Quando', 'Che cosa si può fare'],
    ['ABBINABILE', 'Stato 5 FIRMATO DA USC, comune di Roma, il numero comunale è stato staccato '
     'in SIPO ed è Disponibile, l’identificativo ANSC non è ancora in ANSC_STATO_ATTO.',
     'Aggancio.'],
    ['SENZA NUMERO SIPO', 'Atto firmato con un numero che SIPO non ha staccato, o che ha già '
     'scartato.', 'Nessun aggancio dalla pagina: è il caso di RW-03, da decidere; la riga resta '
     'evidenziata finché non è trattata.'],
    ['INCOERENTE', 'Il numero è stato staccato, ma il tipo di atto o l’intestatario non '
     'corrispondono a quanto registrato allo stacco.', 'Aggancio inibito; l’occhio mostra le '
     'differenze. Si chiarisce con l’ufficiale che ha formato l’atto (RW-03).'],
    ['NON FIRMATO', 'Stato precedente alla firma dell’ufficiale (bozza, validato, firmato dal '
     'dichiarante o per conformità).', 'Nessuna azione: l’atto si ripresenta alla ricerca '
     'successiva.'],
    ['ANNULLATO O CANCELLATO', 'Stato 3, 9 o 10.', 'Nessun aggancio. Il numero staccato segue '
     'la regola della scadenza, o si scarta subito dalla pagina della numerazione.'],
    ['GIÀ IN SIPO', 'L’identificativo ANSC è già in ANSC_STATO_ATTO: atto formato da SIPO o già '
     'agganciato.', 'Solo consultazione.'],
]

CONTROLLI = [
    ['Controllo', 'Regola', 'Se non passa'],
    ['Numero comunale', 'Uguale al numero staccato e ancora Disponibile.', 'Aggancio inibito '
     '(SENZA NUMERO SIPO).'],
    ['Comune di registrazione', 'Roma.', 'Aggancio inibito.'],
    ['Stato dell’atto', '5 FIRMATO DA USC.', 'Aggancio inibito.'],
    ['Tipo di atto', 'Coerente con il tipo atto previsto allo stacco o con l’atto SIPO in '
     'attesa.', 'Aggancio inibito (INCOERENTE).'],
    ['Intestatario', 'Stesso codice fiscale, se SIPO ne aveva uno.', 'Aggancio inibito '
     '(INCOERENTE).'],
    ['Atto di SIPO', 'Se c’è un atto in attesa della web app, l’aggancio lo completa; se non '
     'c’è, lo crea al livello L2.', 'Non è un blocco.'],
    ['Già recuperato', 'Nessuna riga di ANSC_STATO_ATTO con lo stesso identificativo ANSC.',
     'Aggancio inibito (GIÀ IN SIPO).'],
]

SERVE = [
    ['Dove', 'Che cosa serve'],
    ['Registro delle pagine del back-office', 'Tre pagine nuove sotto «Integrazione ANSC», con '
     'le abilitazioni di RW-15. Il disegno del back-office [R7] va allineato.'],
    ['be-numeratore-comunale', 'Sapere che un numero è stato staccato per la web app (RW-16); '
     'utilizzaNumero con l’identificativo ANSC; Evento acquisito (OP-79).'],
    ['Concentratore e ansc-v1.yaml', 'cercaAttiAnsc e agganciaAtto, già elencate nel capitolo '
     '«Che cosa cambia nel disegno»; agganciaAtto rilegge l’atto con R005 alla conferma e si '
     'ferma se è cambiato dall’apertura della pagina.'],
    ['ANSC_STATO_ATTO', 'Unicità dell’identificativo ANSC: due operatori che agganciano lo '
     'stesso atto insieme non possono riuscire entrambi.'],
    ['Configurazione', 'La soglia di giorni dopo la quale un numero passa a «Scartato» '
     '(RW-14) e il livello di recupero proposto per tipo atto (RW-01).'],
]

APERTI = [
    ('RW-15', 'Chi usa la pagina: proposta, consultazione a tutti gli operatori del back-office '
     'e aggancio al solo ufficiale dello stato civile, con il suo codice di sessione verso ANSC.',
     'Comune'),
    ('RW-16', 'Come SIPO sa che un numero è stato staccato per la web app: '
     'be-numeratore-comunale non registra la destinazione del numero. Proposta: un dato sulla '
     'richiesta, oppure il legame con l’atto SIPO in attesa (TL-03). Si lega a OP-79 di [R1].',
     'Analisi'),
]


# =================================================================== capitolo
def capitolo():
    h(d, 1, CAP)
    par(d, 'Le pagine di SIPO descritte in [R2] servono all’ufficiale che ritrova l’atto da cui '
           'è partito: un atto alla volta, quello che ha in mano. Manca un posto da cui si vedano '
           'insieme tutti i numeri staccati per la web app e tutti gli atti di Roma formati in '
           'ANSC, per accorgersi di ciò che nessuno ha ancora recuperato: numeri dimenticati, '
           'numeri prossimi alla scadenza, atti formati con un numero che SIPO non ha staccato. '
           'Questo posto è il back-office [R7].')
    par(d, 'La pagina proposta non è una seconda procedura. Dal back-office e dalle pagine di '
           'SIPO si arriva alla stessa operazione, **agganciaAtto**, con gli stessi controlli e lo '
           'stesso esito; cambia solo il modo di trovare l’atto.')
    voce(d, 'Sessione verso ANSC.', 'La ricerca e la rilettura chiamano R005, che oggi richiede il '
         'codice di sessione dell’ufficiale (OP-23 di [R1]). La pagina mostra il distintivo di '
         'sessione come le altre pagine del back-office che parlano con ANSC; senza sessione le '
         'tabelle locali restano consultabili, la ricerca in ANSC e l’aggancio no.')
    voce(d, 'Nessun controllo a tempo.', 'Per la stessa ragione la ricerca parte su richiesta. '
         'I numeri in attesa invece sono un dato di SIPO e si vedono sempre.')
    voce(d, 'Chi la usa.', 'Proposta: consultazione a tutti gli operatori del back-office, '
         'aggancio al solo ufficiale dello stato civile (RW-15).')

    h(d, 2, 'Le tre pagine')
    tabella(d, PAGINE, [1.2, 2.0, 1.3, 1.3, 1.3])

    h(d, 2, 'Recupero dalla web app')
    par(d, 'La pagina ha due metà. In alto ciò che SIPO sa da sé: i numeri staccati per la web '
           'app e non ancora ricondotti a un atto. In basso ciò che si chiede ad ANSC: gli atti di '
           'Roma formati in un intervallo di date, con l’abbinamento calcolato da SIPO.')
    figura(d, os.path.join(IMG, 'bo_rec_elenco.png'), 6.0,
           'Figura 2 — La pagina «Recupero dalla web app»: numeri in attesa e ricerca in ANSC.')
    tabella(d, ELENCO, [1.5, 3.3, 2.3])
    par(d, 'L’abbinamento è la colonna che guida il lavoro. Lo calcola SIPO confrontando la '
           'risposta di R005 con i numeri staccati e con lo store, perché R005 non filtra per '
           'stato (RW-06):')
    tabella(d, ABBINAMENTI, [1.6, 3.0, 2.5])

    h(d, 2, 'Aggancio dell’atto')
    par(d, 'All’apertura la pagina rilegge l’atto da ANSC, così i controlli valgono per la '
           'versione attuale e non per quella della ricerca. Mostra l’atto, i controlli e il '
           'livello di recupero proposto per quel tipo di atto; l’ufficiale può scegliere un '
           'livello diverso fra quelli disponibili. L3 è disponibile solo se il caso d’uso è '
           'configurato.')
    figura(d, os.path.join(IMG, 'bo_rec_aggancio.png'), 6.0,
           'Figura 3 — La pagina «Aggancio dell’atto»: controlli, livello, conferma.')
    tabella(d, CONTROLLI, [1.6, 3.2, 2.3])
    par(d, 'Alla conferma agganciaAtto rilegge l’atto una seconda volta e si ferma se è cambiato '
           'dall’apertura della pagina, per esempio per una nota tecnica fatta nel frattempo. '
           'Le scritture sulla base dati di SIPO avvengono insieme; il numero si aggiorna subito '
           'dopo, su be-numeratore-comunale. Se quest’ultimo passo non riesce, l’atto resta '
           'agganciato e il numero torna nell’elenco con l’indicazione da allineare.')

    h(d, 2, 'Esito')
    par(d, 'L’esito elenca i passi eseguiti con il loro luogo, e quelli che il recupero non fa '
           'di proposito: definizione, formulario, allineamento con ANPR, annotazioni e '
           'comunicazioni di SIPO. Il passaggio del numero a Evento acquisito compare come «non '
           'disponibile» finché be-numeratore-comunale non ha l’operazione (OP-79). Da qui si '
           'apre l’atto in SIPO o si torna all’elenco.')
    figura(d, os.path.join(IMG, 'bo_rec_esito.png'), 6.0,
           'Figura 4 — L’esito dell’aggancio.')

    h(d, 2, 'Che cosa serve per la pagina')
    tabella(d, SERVE, [2.0, 5.1])


# =================================================================== ritocchi
def ritocchi():
    fatti = []

    def S(v, n, a, e):
        D.sostituisci(d, v, n, attese=a, etichetta=e, fatti=fatti)

    # rinumerazione delle figure dopo il capitolo nuovo
    S('Figura 2 — Gli effetti', 'Figura 5 — Gli effetti', 1, 'figura 2 → 5')

    # il passo 3 dell'aggancio: due ingressi
    S('SIPO, pagina «Recupero Atto ANSC» [R2]', 'SIPO, pagina «Recupero Atto ANSC» [R2], o '
      'back-office, pagina «Recupero dalla web app»', 1, 'passo 3 dell’aggancio')

    # riga del back-office in «Che cosa cambia nel disegno»
    S('La categoria «In attesa della stesura sulla web app»: numeri staccati e non ancora '
      'ricondotti a un atto, con l’anzianità [R2] [R7].',
      'La pagina «Recupero dalla web app», con l’aggancio e l’esito: numeri staccati e non '
      'ancora ricondotti a un atto, con l’anzianità, e atti di Roma trovati in ANSC. È '
      'descritta nel capitolo «' + CAP + '» [R2] [R7].', 1, 'riga del back-office')

    # rinvio dalla voce sul back-office in «Come agganciare»
    p = [p for p in d.paragraphs if p.text.startswith('Il back-office tiene la lista')]
    assert len(p) == 1
    p[0].add_run(' La pagina è descritta nel capitolo «' + CAP + '».')
    fatti.append('rinvio dalla voce sul back-office')

    # scopo
    p = [p for p in d.paragraphs if p.text.startswith('Questo documento confronta le '
                                                      'strategie')]
    assert len(p) == 1
    p[0].add_run(' Propone anche la pagina del back-office da cui effettuare il recupero.')
    fatti.append('scopo')

    # punti aperti
    op = D.trova_tabella(d, '#', 'Questione', 'A chi spetta')
    for riga in APERTI:
        D.clona_riga(op, riga)
    fatti.append('RW-15, RW-16')
    return fatti


def intesta():
    for f in D.frontespizio(d, '0.2', NOME, DATA):
        print('  ' + f)
    D.storia(d, DATA, '0.2', 'Nuovo capitolo · Come agganciare · Che cosa cambia nel disegno · '
             'Punti aperti',
             'Nuovo capitolo sulla pagina del back-office per il recupero: elenco dei numeri '
             'in attesa e ricerca degli atti in ANSC, abbinamento calcolato da SIPO, aggancio '
             'con controlli e livello, esito; tre figure. Rinvii dal percorso di aggancio e dal '
             'disegno. Punti aperti RW-15 e RW-16.')


if __name__ == '__main__':
    PB.elenco(), PB.aggancio(), PB.esito()
    ancora = heading('Che cosa succede dopo', 1)._p
    n = innesta(ancora, capitolo)
    print('capitolo nuovo: %d elementi' % n)
    for f in ritocchi():
        print('  ' + f)
    intesta()
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
