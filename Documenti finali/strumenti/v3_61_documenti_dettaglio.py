# -*- coding: utf-8 -*-
"""v3.61 dell'analisi ANSC (24/11/2026), dalla v3.60 sul file reale.

Recepisce, in forma di sintesi con rinvio, i documenti di dettaglio scritti dopo la v3.60
(decisioni dell'utente del 24/11/2026):
  [R18] nascite gemellari v1.0 (+ proposta della pagina v0.4 e dimostratore)
  [R19] annullamento, cancellazione e rettifiche v0.4
  [R16] atti a testo libero v0.7 (aggiornato)   [R21] recupero degli atti dalla web app v0.3
  [R20] certificazioni di stato civile v0.8      [R22] osservabilità OpenTelemetry v0.4 (solo
  riferimento)   [R23] processo della numerazione comunale v0.5   [R24] studio identificativi v0.5
Scelte: le annotazioni restano in MATR_USR con il legame verso lo store dichiarato fra schemi;
OpenTelemetry solo citato; /finalizzaAtto a DEFINISCI per l'atto cominciato in SIPO, mai
all'acquisizione di un atto nato sulla web app (scheda essenziale, completa solo se
configurato); firma elettronica R012 ammessa per i gemelli del caso 1.
Le DDL (App. A), le tabelle descrittive e l'ERD si allineano nella v3.62, con lo script della
base dati. Nessun paragrafo con ancore di commento viene riscritto.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_61_documenti_dettaglio.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
IMG = os.path.join(QUI, 'img')
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.60.docx')
OUT = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.61.docx')
DATA = '24/11/2026'

d = docx.Document(SRC)
ANCORE = len(d.element.body.findall('.//' + qn('w:commentRangeStart')))
FATTI = []


# ------------------------------------------------------------------ primitive locali
def trova(inizio, dentro=None):
    """Paragrafo unico (fuori dalle tabelle) che comincia con il testo dato."""
    ps = dentro if dentro is not None else d.paragraphs
    t = [p for p in ps if p.text.strip().startswith(inizio)]
    if len(t) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(t), inizio[:70]))
    if D.ha_commenti(t[0]._p):
        raise SystemExit('paragrafo commentato: ' + inizio[:60])
    return t[0]


def nella_sezione(titolo, livello, inizio):
    ps = [Paragraph(e, d) for e in D.sezione(d, titolo, livello) if e.tag == qn('w:p')]
    return trova(inizio, ps)


def riscrivi(p, *pezzi):
    """pezzi: stringhe (normali) o tuple (testo, True) per il grassetto."""
    if D.ha_commenti(p._p):
        raise SystemExit('paragrafo commentato: ' + p.text[:60])
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)
    for x in pezzi:
        t, b = (x, False) if isinstance(x, str) else x
        r = p.add_run(t)
        if b:
            r.bold = True


def lead(p, testa, corpo):
    riscrivi(p, (testa, True), corpo)


def tab_con(*chiavi):
    """Tabella che contiene tutte le chiavi in qualche cella della prima colonna o testata."""
    ris = []
    for t in d.tables:
        prime = {r.cells[0].text.strip() for r in t.rows}
        testa = ' | '.join(c.text.strip() for c in t.rows[0].cells)
        if all(k in prime or k in testa for k in chiavi):
            ris.append(t)
    if len(ris) != 1:
        raise SystemExit('tabella %s: trovate %d' % (chiavi, len(ris)))
    return ris[0]


def riga(t, chiave, colonna=0):
    r = [x for x in t.rows if x.cells[colonna].text.strip() == chiave]
    if len(r) != 1:
        raise SystemExit('riga %s: trovate %d' % (chiave, len(r)))
    return r[0]


def cella(t, chiave, j, testo, colonna=0):
    D.riscrivi_cella(riga(t, chiave, colonna).cells[j], testo)


def sost(vecchio, nuovo, attese=1):
    D.sostituisci(d, vecchio, nuovo, attese=attese, fatti=FATTI)


def blocchi(prima, elenco, modello=None):
    """Inserisce prima dell'elemento `prima` una sequenza di blocchi.

    ('p', testo) · ('v', testa, corpo) · ('l', testa, corpo) paragrafo con lead-in ·
    ('h2'|'h3', titolo) · ('img', png, pollici, didascalia) · ('tab', righe, larghezze)
    """
    for b in elenco:
        k = b[0]
        if k == 'p':
            D.para(d, prima, b[1])
        elif k == 'l':
            D.para(d, prima, pezzi=[(b[1], True), (b[2], False)])
        elif k == 'v':
            D.voce(d, prima, b[1], b[2])
        elif k in ('h1', 'h2', 'h3'):
            D.para(d, prima, b[1], stile='Heading ' + k[1])
        elif k == 'img':
            D.immagine(d, prima, os.path.join(IMG, b[1]), b[2], b[3])
        elif k == 'tab':
            D.tabella(d, prima, b[1], modello=modello, larghezze=b[2])


def svuota(titolo, livello):
    """Svuota una sezione lasciandone il titolo; restituisce l'elemento dopo il titolo."""
    el = D.sezione(d, titolo, livello)
    assert el, titolo
    for e in el[1:]:
        if D.ha_commenti(e):
            raise SystemExit('sezione con commenti: ' + titolo)
        e.getparent().remove(e)
    return el[0].getnext()


MODELLO = tab_con('Fase', 'A — Dati anagrafici e dettaglio')      # tabella delle quattro fasi

# ================================================================== 1. Riferimenti
rif = tab_con('R14', 'R16', 'R17')
cella(rif, 'R14', 1, 'DISEGNO_Back-Office_ANSC_v0.x.docx (versione corrente: v0.11)')
cella(rif, 'R16', 1, 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.x.docx (versione corrente: v0.7)')
cella(rif, 'R16', 2,
      'Documento specifico sugli atti a testo libero e sugli atti senza UC determinabile: casi '
      'd’uso di servizio di ANSC, la strategia adottata (compilazione e testo in SIPO, numero '
      'comunale staccato da SIPO, stesura sulla web app, ritorno con DEFINISCI), l’acquisizione '
      'degli atti formati interamente sulla web app, le pagine di SIPO e i servizi ANSC da usare.')
NUOVI_RIF = [
    ('R18', 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.x.docx (versione corrente: v1.0), con '
            'PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.4.pptx e '
            'DIMOSTRATORE_Pagina-Gemelli_SIPO-ANSC_v0.1.html',
     'Parti plurimi: i due casi decisi dagli UC dei nati, la divisione della pratica con lo '
     'stacco dei numeri e la prenotazione R009, la pagina «Gemelli del parto» e le sue finestre, '
     'il testo dell’atto generato da SIPO, la tabella ANSC_SOGGETTO_ATTO, i punti aperti GE-nn. '
     'Il capitolo «La modalità di integrazione» è scritto come manuale per lo sviluppatore.'),
    ('R19', 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.x.docx (versione '
            'corrente: v0.4)',
     'Cancellazione della pratica, annullamento e rettifica dell’atto: come lavora oggi SIPO, '
     'che cosa prevede ANSC, i due percorsi (web app e riallineamento, oppure formazione da SIPO '
     'con R013), la rettifica tecnica, le annotazioni rettificative per errore materiale '
     '(art. 98) e per rettifica (art. 95), le tabelle ANSC_ANNOTAZIONE e '
     'ANSC_ANNOTAZIONE_CORREZIONE, i punti aperti AR-nn.'),
    ('R20', 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.x.docx (versione corrente: v0.8)',
     'Certificazioni di stato civile in SIPO e in ANSC: instradamento per atto, R002 (firma '
     'solo per riassunto e copia integrale) e R019, innesto nello sportello e nell’ufficio '
     'certificati, funzione «Certificati ANSC», operazioni del concentratore, tabella '
     'ANSC_CERTIFICATO, punti aperti CE-nn.'),
    ('R21', 'ANALISI_Recupero-Atti-WebApp_SIPO-ANSC_v0.x.docx (versione corrente: v0.3)',
     'Atti formati sulla web app con numero comunale staccato in SIPO: i quattro livelli di '
     'presenza in SIPO, la pagina di back-office per il recupero con l’abbinamento calcolato '
     'da SIPO, l’aggancio con rilettura R005, lo stato dell’OTP nella testata, i punti aperti '
     'RW-nn.'),
    ('R22', 'PROPOSTA_Osservabilita-OpenTelemetry_v0.x.docx (versione corrente: v0.4)',
     'Proposta di osservabilità con OpenTelemetry: correlazione su tre livelli (traccia, '
     'dominio, identificativo di operazione verso ANSC e ANPR), livelli e origini degli eventi, '
     'registri diagnostici accanto ad ANSC_LOG_AUDIT, catalogo dei codici di errore, servizio '
     'be-osservabilita, pagine di diagnostica, punti aperti OT-nn. È una proposta: il presente '
     'documento la cita senza adottarne le strutture.'),
    ('R23', 'PROCESSO_Numerazione-Comunale_SIPO-ANSC_v0.x.docx (versione corrente: v0.5)',
     'Il processo della numerazione comunale ereditato da Side e adattato a Roma: attori, '
     'scenari, pagine di richiesta e di ricerca del back-office, servizio '
     'be-numeratore-comunale, punti aperti NC-nn.'),
    ('R24', 'STUDIO_Identificativi-ANSC-verso-ANPR_v0.x.docx (versione corrente: v0.5)',
     'Se e come l’identificativo dell’atto ANSC si trasmette ad ANPR: la forma ANSC dell’atto '
     'negli schemi ANPR, i punti del client che la trattano, i processi schedulati che '
     'aggiornano ANPR, il punto in cui la catena si interrompe (la conversione nel '
     'concentratore all-anpr-sipo) e gli interventi.'),
]
for r in NUOVI_RIF:
    D.clona_riga(rif, r)
FATTI.append('Riferimenti: R14 e R16 aggiornati, R18…R24 nuovi')

# ================================================================== 2. Requisiti
req = tab_con('RF-19', 'RF-22')
cella(req, 'RF-19', 2,
      'Il Riepilogo (fase B) non si chiude senza UC: campi, documenti e formule ne dipendono. '
      'Se nessun UC è determinabile l’atto segue la strategia degli atti a testo libero: '
      'stesura sulla web app e ritorno con DEFINISCI [R16].')
D.clona_riga(req, (
    'RF-23',
    'Certificati, estratti e copie integrali di un atto formato in ANSC si emettono da ANSC '
    '(R002, R019) attraverso il concentratore; gli atti del registro tradizionale si '
    'certificano con il formulario di SIPO. La fonte la decide l’atto, non l’operatore.',
    'L’originale dell’atto digitale e le sue annotazioni stanno in ANSC. Vedi il capitolo «La '
    'certificazione degli atti formati in ANSC» e [R20].'))
FATTI.append('RF-19 integrato, RF-23 nuovo')

# ================================================================== 3. Le quattro fasi
fb = trova('Fase B — il Riepilogo.')
fb.add_run(' Se nessun UC è determinabile — un atto a testo libero o un caso che ANSC non '
           'prevede — il Riepilogo non si chiude ma indirizza l’ufficiale alla web app: CONFERMA '
           'è inibito, DATI PER ANSC stacca il numero comunale, l’atto si forma sulla web app e '
           'torna in SIPO con DEFINISCI (capitolo «Atti a Testo Libero», [R16]).')
rit = trova('Il ritorno ai dati dopo la validazione.')
blocchi(rit._p.getnext(), [
    ('l', 'Il parto plurimo. ',
     'Per i gemelli le fasi valgono per ciascun atto, con una variante [R18]. Nel Riepilogo '
     'della pratica unica si raccolgono documenti e firmatari per ciascun nato; alla conferma '
     'SIPO divide la pratica in un atto per nato, determina l’UC di ciascuno, stacca in blocco '
     'i numeri comunali e prenota gli atti in ANSC con R009 /prenota/evento, che li crea in '
     'bozza. Se gli UC dei nati coincidono, gli atti si completano da SIPO un gemello alla volta '
     'nella pagina «Gemelli del parto»: le fasi C e D si ripetono per ciascuno, i documenti si '
     'trasmettono con R001 al momento della validazione e l’atto si definisce in SIPO subito '
     'dopo la firma dell’ufficiale. Se gli UC differiscono, gli atti si completano sulla web app '
     'e tornano in SIPO con il recupero. Lo store porta una riga per gemello, e la tabella '
     'ANSC_SOGGETTO_ATTO lega i nati ai propri atti e i gemelli fra loro.'),
])
FATTI.append('Le quattro fasi: uscita senza UC (fase B) e parto plurimo')

# ================================================================== 4. I log
h_payload = D.h(d, 1, 'Costruzione del payload')
blocchi(h_payload._p, [
    ('p', 'Una proposta di osservabilità per l’intera catena — correlazione fra front-end, '
          'back-end, concentratori, ANSC e ANPR, livelli e origini degli eventi, registri '
          'diagnostici accanto all’audit, catalogo dei codici di errore — è descritta in un '
          'documento a parte [R22]. Il presente documento la cita senza adottarne le strutture: '
          'ANSC_LOG_AUDIT resta il registro probatorio dell’atto.'),
])

# ================================================================== 5. Processo: due correzioni
sost('le fonti dicono che inibisce certificati ed estratti,',
     'le fonti dicono che inibisce il certificato semplice e l’estratto per riassunto, mentre la '
     'copia integrale resta emissibile,')
sost("Non c'è nessuna finestra fino a mezzanotte: nessun controllo su data o ora. Un atto "
     "definito si riapre in qualunque momento con la rettifica.",
     "La finestra fino a mezzanotte esiste nel back-end: /checkAttoScansionato "
     "(DettaglioAttiController) consente di riaprire con la rettifica un atto definito fino alle "
     "23:59:59 del giorno della pratica [R19].")

# ================================================================== 6. Atti a Testo Libero
dopo = svuota('Atti a Testo Libero', 1)
blocchi(dopo, [
    ('p', 'Gli atti a testo libero, e in generale gli atti per i quali nel Riepilogo non si '
          'determina un UC, sono trattati in un documento specifico [R16], al quale si rinvia '
          'per i casi d’uso di servizio di ANSC, le pagine di SIPO e i servizi da usare. Qui se '
          'ne riporta la strategia adottata.'),
    ('l', 'La strategia adottata. ',
     'È una sintesi delle due modalità considerate in precedenza, e vale sia per le '
     'dichiarazioni, per le quali i casi d’uso di servizio sono disponibili solo sulla web app '
     '[R15], sia per le trascrizioni. L’atto si compila in SIPO, che ne compone il testo e resta '
     'la fonte dei dati; il numero comunale lo stacca SIPO prima di andare sulla web app; l’atto '
     'si forma sulla web app con il caso d’uso di servizio; al ritorno non si importano dati: '
     'DEFINISCI aggancia l’atto ANSC e definisce l’atto SIPO in un passaggio solo.'),
    ('img', 'testo_libero/strategia_adottata.png', 4.6,
     'La strategia adottata per gli atti che SIPO non gestisce in automatico [R16].'),
    ('tab', [
        ['#', 'Passo', 'Dove', 'Servizio', 'Stato'],
        ['1', 'Stesura dell’atto fino al Riepilogo, con la ricerca dell’intestatario. Per un '
              'tipo atto a testo libero il testo si scrive nella pagina del testo libero di SIPO '
              'e si passa al passo 3.', 'SIPO', 'R005 /consultazione/ansc/intestatario',
         'SIPO: 1 IN LAVORAZIONE'],
        ['2', 'Il Riepilogo non trova un UC: messaggio di rinvio alla web app, CONFERMA inibito, '
              'niente firmatari né documenti.', 'SIPO', '—', '—'],
        ['3', 'DATI PER ANSC: stacco del numero comunale.', 'SIPO',
         'be-numeratore-comunale POST /richiesta', 'numero: Disponibile'],
        ['4', 'Anteprima con il numero comunale in evidenza; COPIA TESTO copia il testo composto '
              'o scritto in SIPO.', 'SIPO', '—', 'store: WA · ATTESA WEBAPP'],
        ['5', 'Stesura sulla web app con il caso d’uso di servizio: numero comunale, testo, '
              'intestatari; validazione, firme e chiusura.', 'Web app ANSC',
         '— (funzioni della web app)', 'ANSC: 5 FIRMATO DA USC'],
        ['6', 'DEFINISCI: finestra di aggancio con l’atto dal numero comunale coincidente già '
              'selezionato.', 'SIPO', 'R005 /consultazione/ansc/evento', '—'],
        ['7', 'Conferma: l’atto è definito con il percorso di salvataggio ordinario.', 'SIPO',
         '/finalizzaAtto; be-numeratore-comunale PUT /utilizza',
         'SIPO: 2 DEFINITO · store: 5 FIRMATO DA USC · numero: Utilizzato'],
    ], [0.3, 2.6, 0.8, 1.5, 1.3]),
    ('p', 'I passi della strategia adottata, con i servizi chiamati e gli stati [R16].'),
    ('p', 'Fra l’Anteprima e DEFINISCI lo store tiene l’atto in attesa della web app e l’atto di '
          'SIPO resta in 1 IN LAVORAZIONE; la vista di supervisione elenca questi atti con la loro '
          'anzianità, perché un atto in attesa da giorni è un atto che nessuno ha concluso. Come '
          'registrare l’attesa nello store è aperto (OP-94).'),
    ('l', 'Perché DEFINISCI esegue la definizione di SIPO. ',
     'DEFINISCI usa lo stesso /finalizzaAtto del percorso ordinario, con l’allineamento '
     'anagrafico di SIPO. È ciò che serve: per un caso d’uso di servizio ANSC non genera '
     'annotazioni automatiche e non predispone la comunicazione anagrafica [R15]. La conclusione '
     'dell’atto ricorda all’ufficiale le annotazioni sugli atti collegati, che restano a carico '
     'dell’ufficio (OP-96).'),
    ('l', 'Il tipo atto a testo libero. ',
     'Il tipo atto a testo libero scelto all’inizio segue la stessa strada: il testo si scrive '
     'nella pagina del testo libero che SIPO ha già (MATR_USR.ATTO.FLG_ATTO_TESTOLIBERO e '
     'ATTO_TESTO_LIBERO) e da lì si passa a DATI PER ANSC.'),
    ('l', 'Gli atti formati interamente sulla web app. ',
     'Un atto può nascere sulla web app senza essere mai cominciato in SIPO. Il punto di aggancio '
     'è il numero comunale, staccato prima dal back-office o con il servizio della numerazione; '
     'il rientro è descritto nel capitolo «SIPO in relazione alla web app ANSC», paragrafo '
     '«L’aggancio di un atto formato sulla web app».'),
], modello=MODELLO)
FATTI.append('Atti a Testo Libero: riscritto sulla strategia adottata, figura sostituita')

# ================================================================== 7. Cancellazione in lavorazione
p9 = trova('- Se lo stato è 9')
riscrivi(p9, '- Se lo stato è 9 non chiamare ANSC e concludere la cancellazione in SIPO: l’atto '
             'era già stato cancellato, per esempio dopo un esito indeterminato riconciliato [R19]')
h_stato = D.h(d, 2, 'Lo stato dopo la cancellazione')
blocchi(h_stato._p, [
    ('l', 'Dove nel codice. ',
     'Le sei aree passano tutte dal servizio /cancellaAnnullaAtto di statocivile-be: il '
     'controllo su ANSC_STATO_ATTO e la chiamata R011 vanno inseriti lì, per l’operazione '
     'ANNULLAMENTOPRATICA, prima della procedura PL/SQL e dell’allineamento ANPR. L’ordine è '
     'vincolante perché il servizio non è transazionale: chiamare la procedura prima di ANSC '
     'lascerebbe in SIPO una pratica cancellata e in ANSC un evento vivo (OP-90). I passi e i '
     'punti del codice sono nel documento specifico [R19].'),
    ('l', 'Il parto plurimo. ',
     'Per i gemelli la cancellazione riguarda l’intero parto: R011 per ciascun atto prenotato e '
     'PUT /scarta per ciascun numero comunale, ammessa soltanto finché nessun gemello è firmato '
     'dall’ufficiale [R18].'),
])

# ================================================================== 8. Atto firmato
sost('Per i servizi cooperativi la firma non è descritta; che avvenga con R007, come per ogni '
     'altro evento, è un’ipotesi DA VERIFICARE.',
     'Con i servizi cooperativi la firma è quella dell’ufficiale con R007: il registro delle '
     'modifiche ne riporta la correzione per le rettifiche fra le versioni 1.32.2 e 1.37.0 [R19]; '
     'resta da accertare se serva anche l’attestazione di conformità (OP-81).')
sost('I cinque mapping dichiarano gli stessi 24 campi;',
     'I cinque mapping dichiarano gli stessi 21 campi, 18 dei quali obbligatori, oltre alla '
     'formula e all’allegato;')

h_csipo = D.h(d, 2, 'Che cosa comporta per SIPO')
dopo = svuota('Che cosa comporta per SIPO', 2)
D.testo_di(h_csipo, 'Che cosa comporta per SIPO: due percorsi')
blocchi(dopo, [
    ('p', 'L’annullamento di un atto formato in ANSC si fa per due vie, entrambe ammesse da ANSC '
          'e lasciate alla scelta dell’ufficiale caso per caso [R19].'),
    ('v', 'Percorso A — web app e riallineamento. ',
     'Per un atto con identificativo ANSC e stato 5 «ANNULLA ATTO» non esegue subito la '
     'procedura di SIPO: indica che l’annullamento si fa con l’annotazione per rettifica sulla '
     'web app e offre «RIALLINEA DA ANSC», che legge l’atto con R005 (con flagRettifica, per '
     'avere l’ultima rettifica), mostra l’annotazione trovata e, alla conferma, annulla l’atto in '
     'SIPO e aggiorna ANSC_STATO_ATTO.'),
    ('v', 'Percorso B — l’annotazione formata da SIPO. ',
     'Una pagina comune ai registri, perché i cinque casi d’uso chiedono gli stessi dati, con un '
     'numero comunale proprio dal servizio della numerazione, R013 con idTipoRettifica = 0, la '
     'firma dell’ufficiale con R007 e gli stessi passi di chiusura del percorso A. Il '
     'concentratore deve esporre il deposito della rettifica (creaAnnotazioneRettificativa), che '
     'oggi manca nel contratto (OP-45).'),
    ('l', 'Non è la rettifica di oggi. ',
     'In SIPO /updLavorazioneRettifica riporta un atto definito allo stato 1 e lo si corregge. '
     'Un atto formato in ANSC non si riapre: per quegli atti «RETTIFICA ATTO» non si mostra, e '
     '/checkAttoScansionato e /updLavorazioneRettifica rispondono negativamente prima della '
     'regola della mezzanotte. Al suo posto compare «RETTIFICA TECNICA» (paragrafo «La rettifica '
     'tecnica e il riallineamento»).'),
    ('l', 'L’anagrafe. ',
     'In entrambi i percorsi resta da stabilire l’allineamento anagrafico: oggi SIPO lo esegue '
     'a ogni annullamento, mentre per un atto formato in ANSC gli effetti anagrafici potrebbero '
     'arrivare da ANSC, e farli due volte sarebbe un errore (OP-82).'),
    ('l', 'La configurazione. ',
     'I cinque casi d’uso si configurano come gli altri in ANSC_CFG_UC; il tipo di rettifica lo '
     'valorizza il concentratore.'),
])

h_pa = D.h(d, 2, 'Punti aperti', esatto=True)
blocchi(h_pa._p, [
    ('h2', 'Le annotazioni rettificative: errore materiale (art. 98) e rettifica (art. 95)'),
    ('p', 'Un atto firmato non si modifica: si annota. Accanto all’annullamento, la stessa '
          'operazione R013 /rettifica/validazione/evento serve due annotazioni che correggono '
          'l’atto, trattate per esteso nel documento specifico [R19].'),
    ('v', 'Errore materiale (art. 98). ',
     'Lo promuove l’ufficiale d’ufficio e non può annullare l’atto, soltanto correggerlo: i dati '
     'correggibili sono quelli anagrafici dell’intestatario e, nelle nascite, dei genitori. '
     'Formula 888; la correzione viaggia nel testo (composizioneCompleta, «dove è scritto … deve '
     'leggersi …») e nell’atto intero già corretto (eventoModificato).'),
    ('v', 'Rettifica (art. 95). ',
     'Nasce dal provvedimento di un’altra amministrazione e può modificare l’atto oppure '
     'annullarlo. Formula 190; il testo sta in datiRettifica.dettaglioRettifica.'),
    ('tab', [
        ['Registro', 'Rettifica (art. 95)', 'Errore materiale (art. 98)'],
        ['Nascita', '14630000 · Dic_Nasc_118', '14640000 · Dic_Nasc_119'],
        ['Morte', '2341 · Morte_012', '2342 · Morte_013'],
        ['Matrimonio', '368699 · Matr_017', '368799 · Matr_018'],
        ['Unione civile', '458699 · UnCiv_007', '458799 · UnCiv_008'],
        ['Cittadinanza', '53719 · Citt_047', '53729 · Citt_048'],
    ], [1.4, 2.4, 2.4]),
    ('p', 'I dieci casi d’uso delle annotazioni rettificative, due per registro.'),
    ('p', 'I mapping di nascita, morte, matrimonio e unione civile sono identici; la cittadinanza '
          'aggiunge tredici campi facoltativi. Nessuno dei dieci contiene i campi dei soggetti, '
          'il tipo di rettifica o l’atto corretto: la correzione strutturata la compone il '
          'concentratore, ricavando testo e atto corretto dalla stessa differenza, perché i due '
          'canali dicano la stessa cosa. La competenza è del comune che ha formato l’atto; la '
          'firma è dell’ufficiale (R007).'),
    ('p', 'Come per l’annullamento, i percorsi sono due: web app e riallineamento, oppure '
          'annotazione formata da SIPO, con una pagina sola per i cinque registri. Il secondo '
          'richiede al concentratore le operazioni creaAnnotazioneRettificativa (R013 '
          '/rettifica), creaAnnotazione (R009, casi d’uso _998_1 e _998_2) e '
          'creaAnnotazioneModificativa (R013 /annotazione/modificativa).'),
    ('img', 'annullamento/errore_materiale_flusso.png', 6.0,
     'L’annotazione per errore materiale formata da SIPO (percorso B) [R19].'),
    ('l', 'Dove si registra l’annotazione. ',
     'ANSC_STATO_ATTO ha per chiave l’atto di SIPO, e in SIPO un’annotazione non è un atto ma '
     'una riga del modulo delle annotazioni (ANNOTAZIONE_ATTO). L’annotazione formata verso ANSC '
     'si registra perciò in due tabelle proprie, ANSC_ANNOTAZIONE e ANSC_ANNOTAZIONE_CORREZIONE, '
     'collocate in MATR_USR accanto al modulo delle annotazioni, come ALLEGATO: sono un dato '
     'dell’atto, non del componente. Il legame con lo store dell’atto, che sta in ANSC_USR, '
     'attraversa gli schemi e va dichiarato come tale. La loro struttura è nel documento '
     'specifico [R19].'),
    ('l', 'Gli atti cartacei. ',
     'L’annotazione modificativa su atto cartaceo ha casi d’uso propri (*_998_4, '
     'Dic_Nasc_998_5) con la formula 998 a testo libero; il servizio con cui depositarla non è '
     'dichiarato, e se il Comune debba registrare in ANSC le annotazioni dei propri atti cartacei '
     'è aperto (OP-92).'),
], modello=MODELLO)

# i punti aperti del capitolo passano nel registro
reg = [t for t in d.tables if [c.text.strip() for c in t.rows[0].cells][:4] ==
       ['#', 'Tema', 'Questione', 'Stato'] and 'OP-79' in {r.cells[0].text.strip() for r in t.rows}]
cap = [t for t in d.tables if [c.text.strip() for c in t.rows[0].cells][:4] ==
       ['#', 'Tema', 'Questione', 'Stato'] and 'OP-80' in {r.cells[0].text.strip() for r in t.rows}]
assert len(reg) == 1 and len(cap) == 1 and reg[0]._tbl is not cap[0]._tbl
REG = reg[0]
ancora = riga(REG, 'OP-79')._tr
for r in reversed(list(cap[0].rows)[1:]):
    ancora.addnext(r._tr)
dopo = svuota('Punti aperti', 2)
blocchi(dopo, [('p', 'I punti aperti del capitolo, da OP-80 a OP-84, sono riportati nel registro '
                     'degli Open Point.')])
FATTI.append('Atto firmato: due percorsi, annotazioni rettificative, OP-80…84 nel registro')

# ================================================================== 9. SIPO e la web app
h_agg = D.h(d, 2, 'L’aggancio di un atto formato sulla web app')
blocchi(h_agg._p, [
    ('h2', 'La rettifica tecnica e il riallineamento'),
    ('p', 'La nota tecnica corregge i metadati di un atto firmato dall’ufficiale e si fa '
          'soltanto sulla web app, dal comune che ha redatto l’atto, finché sull’atto non sono '
          'state apposte annotazioni modificative. ANSC non avvisa: se la nota si fa entrando '
          'direttamente nella web app, SIPO non lo sa. Il documento specifico [R19] propone di '
          'portare l’ufficiale alla web app da SIPO e di riportare poi in SIPO ciò che la nota ha '
          'cambiato.'),
    ('tab', [
        ['#', 'Passo', 'Che cosa accade'],
        ['1', '«RETTIFICA TECNICA» nel dettaglio dell’atto',
         'Compare al posto di «RETTIFICA ATTO» per un atto con identificativo ANSC e stato 5, '
         'senza limite di orario.'],
        ['2', 'Pagina di avvio', 'Mostra identificativo nazionale e numero comunale, il percorso '
         'sulla web app e i vincoli; registra l’avvio in ANSC_LOG_AUDIT, così che la vista di '
         'supervisione elenchi le rettifiche avviate e non riallineate.'],
        ['3', 'Nota tecnica sulla web app', 'L’ufficiale la compila e la conclude; SIPO non '
         'interviene.'],
        ['4', '«RIALLINEA DA ANSC»', 'R005 sull’evento per identificativo nazionale, poi R005 '
         'sulle note tecniche dell’evento.'],
        ['5', 'Confronto', 'Il modello letto si confronta con quello depositato '
         '(ANSC_STATO_ATTO.TXT_EVENTO); ogni percorso cambiato si riporta alla colonna di SIPO '
         'con ANSC_CFG_CAMPO.ALIAS_CAMPO_SIPO, quelli senza colonna si elencano a parte.'],
        ['6', 'Conferma', 'I dati di SIPO si aggiornano senza riaprire l’atto: lo stato resta 2 '
         'DEFINITO.'],
        ['7', 'Anagrafe', 'Nessun allineamento anagrafico da SIPO: le comunicazioni le genera '
         'ANSC.'],
    ], [0.3, 1.9, 4.0]),
    ('p', 'La rettifica tecnica, passo per passo [R19].'),
    ('img', 'annullamento/rettifica_tecnica_flusso.png', 6.0,
     'La rettifica tecnica di un atto firmato: il flusso fra SIPO e la web app [R19].'),
    ('p', 'Lo stesso schema vale per gli allegati errati: avvio da SIPO, correzione sulla web '
          'app, rilettura dei documenti dell’atto e aggiornamento di ALLEGATO. Il riallineamento '
          'è un adempimento dell’ufficio, come la riconciliazione del paragrafo precedente; '
          'l’avvio da SIPO serve anche a lasciarne traccia (OP-43).'),
], modello=MODELLO)

dopo = svuota('L’aggancio di un atto formato sulla web app', 2)
blocchi(dopo, [
    ('p', 'Un atto può nascere sulla web app: perché nel Riepilogo non si determina un UC, perché '
          'SIPO era fermo, o perché l’ufficiale lo ha steso direttamente lì. In tutti questi casi '
          'l’atto esiste in ANSC, è formato e firmato, e SIPO deve saperlo. ANSC non avvisa, non '
          'offre un servizio di recupero e non registra da quale canale l’atto è nato: il recupero '
          'è a carico del Comune, ed è ANSC stessa a suggerire alle case software di svilupparlo '
          '[R15].'),
    ('l', 'Due vie di ritorno. ',
     'Il ritorno dipende da dove l’atto è cominciato, e la differenza decide se si esegua la '
     'definizione di SIPO.'),
    ('v', 'L’atto cominciato in SIPO. ',
     'È il caso degli atti a testo libero e di quelli senza UC (capitolo «Atti a Testo Libero», '
     '[R16]). L’atto c’è già in SIPO, con i suoi dati e il suo testo: manca soltanto '
     'l’identificativo nazionale. DEFINISCI cerca con R005 gli atti formati nel giorno, '
     'preseleziona quello il cui numero comunale coincide con il numero staccato e, alla '
     'conferma, registra l’identificativo sullo store, segna il numero come utilizzato e '
     'definisce l’atto con /finalizzaAtto. La definizione di SIPO serve: per un caso d’uso di '
     'servizio ANSC non predispone la comunicazione anagrafica.'),
    ('v', 'L’atto nato sulla web app. ',
     'L’atto non esiste in SIPO e va creato. Lo si ritrova con R005 e lo si acquisisce: SIPO '
     'scrive l’atto già definito, con il canale WEBAPP sullo store, e non esegue /finalizzaAtto, '
     'che rifarebbe il documento, le annotazioni e l’allineamento anagrafico che per un caso '
     'd’uso ordinario ANSC ha già avviato [R21].'),
    ('l', 'Quanto dell’atto entra in SIPO. ',
     'Il recupero distingue quattro livelli di presenza in SIPO, dal solo numero all’importazione '
     'completa [R21]. Il riferimento all’atto — identificativo nazionale, numero comunale, data, '
     'canale — si registra per tutti; per l’atto nato sulla web app si acquisisce la scheda '
     'essenziale (atto, area, intestatari, testo), e l’importazione completa solo per gli UC '
     'ordinari la cui configurazione consente la transcodifica inversa del modello evento '
     '(OP-66).'),
    ('img', 'recupero/livelli.png', 6.0,
     'I quattro livelli di presenza in SIPO di un atto formato sulla web app [R21].'),
    ('l', 'I controlli. ',
     'Prima di agganciare o di acquisire, SIPO rilegge l’atto con R005 e ne verifica lo stato '
     '(5 FIRMATO DA USC: un atto soltanto validato può ancora cambiare), il tipo atto, '
     'l’intestatario e il numero comunale. Un atto il cui numero non è fra quelli staccati da '
     'SIPO non si aggancia senza una decisione esplicita (OP-95).'),
    ('l', 'Dove si lavora. ',
     'Le pagine sono descritte nei documenti specifici: la finestra di DEFINISCI e le pagine '
     '«Recupero Atto ANSC» e «Acquisizione Atto ANSC» in [R16], la pagina di recupero del '
     'back-office, con l’abbinamento calcolato da SIPO, in [R21]. Il concentratore espone la '
     'ricerca (cercaAttiAnsc) e l’aggancio (agganciaAtto), da aggiungere al contratto. Chi usi '
     'quale superficie, e se debbano restare entrambe, è da decidere (OP-97).'),
    ('h3', 'Lo stacco del numero comunale'),
    ('p', 'Il numero comunale lo assegna il Comune: nessun servizio di ANSC lo attribuisce. '
          'L’identificativo nazionale lo riporta al proprio interno, ed è ciò che consente di '
          'abbinare l’atto al numero staccato, ma non lo genera. Ne discende che, se un atto si '
          'forma sulla web app, il numero deve comunque uscire da SIPO, perché SIPO è l’unico '
          'luogo in cui la serie è governata. Un numero scelto a mano sulla web app è un numero '
          'che nessuno ha riservato.'),
    ('p', 'Il numero si stacca dalle maschere di SIPO con DATI PER ANSC, quando l’atto è '
          'cominciato in SIPO, oppure dal back-office o con il servizio della numerazione, quando '
          'l’atto nasce sulla web app [R23]; risulta impegnato da quel momento, e il ritorno '
          'dell’atto lo segna come utilizzato. Un numero staccato e non utilizzato si chiude: dopo '
          'un numero di giorni configurabile passa a Scartato, altrimenti la serie presenta buchi '
          'che nessuno sa spiegare a distanza di tempo [R21].'),
    ('p', 'Come la funzione si realizzi — la serie, le strutture ereditate da Side e i percorsi — '
          'è descritto nel paragrafo «La numerazione comunale».'),
], modello=MODELLO)
FATTI.append('SIPO e la web app: rettifica tecnica nuova, aggancio riscritto su due vie')

# ================================================================== 10. Certificazione (capitolo nuovo)
h_num = D.h(d, 1, 'La numerazione comunale')
blocchi(h_num._p, [
    ('h1', 'La certificazione degli atti formati in ANSC'),
    ('p', 'Un atto formato in ANSC ha l’originale in ANSC: le annotazioni fatte da altri comuni, '
          'le rettifiche e le note tecniche stanno lì, e non nel database di SIPO, che dell’atto '
          'conserva i dati di formazione. Un certificato ricomposto da SIPO con i dati locali '
          'potrebbe quindi divergere dall’atto vero pur essendo firmato. Il documento specifico '
          '[R20] ne trae la regola che segue e ne descrive l’innesto nello sportello di stato '
          'civile e nell’ufficio certificati.'),
    ('h2', 'L’instradamento per atto'),
    ('p', 'La fonte del documento la decide l’atto, non l’operatore. Se l’atto ha un '
          'identificativo ANSC — nello store ANSC_STATO_ATTO, oppure in ANAG_USR.ATTO.ID_ATTO_ANSC '
          'per gli atti agganciati — certificati, estratti e copie integrali si emettono da ANSC '
          'attraverso il concentratore; altrimenti dal formulario di SIPO, come oggi. L’operatore '
          'continua a lavorare dallo sportello di SIPO, che riconosce l’atto e sceglie da sé dove '
          'produrre il documento. I controlli restano in SIPO: prima di chiamare ANSC si '
          'verificano il blocco della certificazione del soggetto e lo stato dell’atto.'),
    ('img', 'certificazioni/instradamento.png', 6.0,
     'Dalla richiesta allo sportello al documento: la fonte la decide l’atto [R20].'),
    ('h2', 'I servizi e la firma'),
    ('tab', [
        ['Richiesta allo sportello', 'Servizio ANSC', 'Firma'],
        ['Certificato di nascita, matrimonio, unione civile, morte',
         'R002 /certificato-semplice, tipo 1',
         'Nessuna: sigillo del Ministero e QR di verifica.'],
        ['Estratto per riassunto', 'R002 /certificato, tipo 2',
         'Firma remota dell’ufficiale (parametri di firma, con OTP).'],
        ['Copia integrale', 'R002 /certificato, tipo 3', 'Firma remota dell’ufficiale.'],
        ['Plurilingue di nascita, matrimonio, morte; capacità matrimoniale',
         'R019, in sequenza: sigle, annotazioni, anteprima, emissione',
         'Non dichiarata dal contratto (OP-98).'],
    ], [2.3, 2.2, 1.7]),
    ('p', 'Le richieste dello sportello e i servizi ANSC che le soddisfano [R20].'),
    ('p', 'Tre caratteristiche del servizio cambiano il comportamento dello sportello. Il '
          'certificato semplice non richiede la firma dell’ufficiale, e con il permesso ridotto '
          'lo può rilasciare anche un operatore che non è ufficiale. R002 non ha un’anteprima: '
          'ogni chiamata emette un certificato, e per un atto ANSC il pulsante «Anteprima» di '
          'SIPO non può produrre un documento. La risposta è un PDF/A già composto, con il sigillo '
          'e il QR, che SIPO mostra e stampa così com’è.'),
    ('p', 'Prima dell’emissione si consulta l’atto con R005 nella forma sintetica, che restituisce '
          'l’identificativo interno dell’evento, quello dell’intestatario, lo stato e i tipi di '
          'documento emissibili. L’esito di R002 si classifica come emesso, rifiutato o da '
          'verificare, e un esito incerto non si ripete alla cieca: ripetere significherebbe '
          'emettere un secondo certificato.'),
    ('h2', 'I due ingressi'),
    ('p', 'Il primo ingresso è quello di oggi: lo sportello di stato civile e l’area «Stato '
          'Civile» dell’ufficio certificati (cert-web, cert-be), dove la ricerca dell’atto della '
          'persona, se trova un identificativo ANSC, attiva il recupero da ANSC. Il secondo è una '
          'funzione nuova di SIPO, «Certificati ANSC», terza voce dell’area «Certificati» del menu '
          'dei municipi, che cerca l’atto in ANSC come la web app — anche gli atti di altri '
          'comuni, che in SIPO non esistono — e porta al rilascio.'),
    ('h2', 'Che cosa serve al componente'),
    ('v', 'Le operazioni. ',
     'Otto operazioni nuove del concentratore, da aggiungere al contratto ansc-v1.yaml e alla '
     'specifica [R8]: creaCertificato ed elencaCertificati (R002), elencaSigleEnunciazioni, '
     'elencaAnnotazioniCertificabili, creaAnteprimaCertificatoInternazionale e '
     'creaCertificatoInternazionale (R019), leggiEventoAnsc e cercaEventiAnsc (R005 nella forma '
     'sintetica).'),
    ('v', 'Il registro delle emissioni. ',
     'Una tabella ANSC_CERTIFICATO in ANSC_USR registra ogni emissione con il suo esito, '
     'l’identificativo del certificato restituito da ANSC e la data di validità; la struttura è '
     'nel documento specifico [R20].'),
    ('v', 'La sessione. ',
     'L’OTP di sessione entra anche nell’ufficio certificati, con il tempo residuo; per estratti '
     'e copie integrali servono le credenziali di firma remota dell’ufficiale, nella stessa '
     'finestra della firma dell’atto.'),
    ('v', 'Gli operatori. ',
     'Gli operatori che emettono da ANSC devono avere utenza, permessi (consultazione, certificato '
     'semplice o pieno) e postazione registrata (OP-101).'),
    ('p', 'Restano fuori dal perimetro l’area «Anagrafici» dell’ufficio certificati e i '
          'certificati richiesti online dai cittadini (R024). La decisione è registrata come '
          'PC-11.'),
], modello=MODELLO)
FATTI.append('Capitolo nuovo «La certificazione degli atti formati in ANSC»')

# ================================================================== 11. Numerazione: percorsi
perc = [t for t in d.tables if t.rows[0].cells[0].text.strip() == 'Percorso'
        and 'Parto plurimo' in {r.cells[0].text.strip() for r in t.rows}
        and 'Atto formato sulla web app' in {r.cells[0].text.strip() for r in t.rows}]
assert len(perc) == 2, len(perc)
t84 = [t for t in perc if 'Quando si stacca' in t.rows[0].cells[1].text][0]
t85 = [t for t in perc if 'Chi chiama' in t.rows[0].cells[1].text][0]
cella(t84, 'Atto formato sulla web app', 1,
      'Prima della stesura sulla web app: dalle maschere di SIPO con DATI PER ANSC, se l’atto è '
      'cominciato in SIPO [R16]; dalla pagina di richiesta del back-office o con POST /richiesta, '
      'se nasce sulla web app.')
cella(t84, 'Atto formato sulla web app', 2,
      '1 Disponibile → 2 Utilizzato al ritorno dell’atto (DEFINISCI o acquisizione), oppure 3 '
      'Scartato; un numero non utilizzato passa a Scartato dopo un numero di giorni configurabile '
      '[R21]. Con l’aggancio dell’atto in SIPO → 4 Evento acquisito.')
cella(t84, 'Parto plurimo', 1,
      'In blocco alla divisione della pratica, tanti numeri quanti i nati, prima della '
      'prenotazione R009 che li richiede tutti [R18].')
cella(t85, 'Atto formato sulla web app', 1,
      'L’ufficiale, dalle maschere di SIPO (DATI PER ANSC) o dalla pagina della numerazione; un '
      'altro applicativo, con POST /richiesta')
cella(t85, 'Atto formato sulla web app', 2,
      'POST /richiesta; poi PUT /utilizza al ritorno dell’atto, oppure PUT /scarta. La '
      'destinazione del numero alla web app, la scadenza dopo un numero di giorni e il passaggio a '
      'Evento acquisito non hanno un’operazione (OP-79).')
cella(t85, 'Parto plurimo', 1, 'Il concentratore operativo, alla divisione della pratica')
cella(t85, 'Parto plurimo', 2,
      'POST /richiesta con numeroElementi pari ai nati, poi la prenotazione R009; ciascun numero '
      'segue la sorte del proprio atto, e quello di un gemello chiuso si scarta [R18].')
FATTI.append('Numerazione: percorsi «web app» e «parto plurimo» riallineati')

# ================================================================== 12. Le funzioni offerte da ANSC
cifre = tab_con('Grandezza', 'Contratti pubblicati')
cella(cifre, 'Operazioni impiegate dal disegno attuale', 1, '36')
cella(cifre, 'Servizi impiegati dal disegno attuale', 1, '15 su 25')
lead(trova('Il rapporto fra le ultime due righe è la misura del perimetro'),
     '', 'Il rapporto fra le ultime due righe è la misura del perimetro: il disegno impegna poco '
         'più della metà dei servizi disponibili, e ciò che resta fuori è soprattutto il canale '
         'sanitario, lo sportello del cittadino e parte del dominio esteso — adozioni, '
         'provvedimento di rifiuto, correzione di annotazione — che il Comune non ha ancora '
         'aperto.')
fam = tab_con('Famiglia', 'Certificazione', 'Deposito degli eventi')
cella(fam, 'Certificazione', 3, 'Per gli atti formati in ANSC il documento si emette da ANSC [R20].')
cella(fam, 'Deposito degli eventi', 3,
      'Portano un evento dentro ANSC. Il disegno ne usa due: la validazione (R009) e la rettifica '
      '(R013).')
USO = {
    ('R009', '/prenota/evento'): 'Sì — parto plurimo, alla divisione della pratica [R18]',
    ('R013', '/rettifica/validazione/evento'):
        'Sì — annullamento e annotazioni rettificative, percorso B [R19]',
    ('R012', '/firmadichiarante/annulla-link'): 'Sì — firma elettronica del dichiarante',
    ('R012', '/firmadichiarante/invio-email'): 'Sì — firma elettronica del dichiarante',
    ('R012', '/firmadichiarante/pooling-statoatto'): 'Sì — firma elettronica del dichiarante',
    ('R005', '/consultazione/ansc/evento/sintetico'): 'Sì — certificazione [R20]',
    ('R005', '/consultazione/ansc/soggetto/sintetico'): 'Sì — certificazione e recupero [R20] [R21]',
    ('R002', '/certificato'): 'Sì — atti formati in ANSC [R20]',
    ('R002', '/certificato-semplice'): 'Sì — atti formati in ANSC [R20]',
    ('R019', '/certificato-internazionale/annotazioni'): 'Sì — certificati plurilingue [R20]',
    ('R019', '/certificato-internazionale/create'): 'Sì — certificati plurilingue [R20]',
    ('R019', '/certificato-internazionale/preview'): 'Sì — certificati plurilingue [R20]',
    ('R019', '/certificato-internazionale/sigle-enunciazioni'): 'Sì — certificati plurilingue [R20]',
}
fatte = set()
for t in d.tables:
    testa = [c.text.strip() for c in t.rows[0].cells]
    if testa[:2] != ['Serv.', 'Percorso'] or testa[-1] != 'Uso nel disegno':
        continue
    for r in t.rows[1:]:
        k = (r.cells[0].text.strip(), r.cells[1].text.strip())
        if k in USO:
            D.riscrivi_cella(r.cells[-1], USO[k])
            fatte.add(k)
assert fatte == set(USO), set(USO) - fatte
# conteggio di controllo sull'inventario
si, servizi = 0, set()
for t in d.tables:
    testa = [c.text.strip() for c in t.rows[0].cells]
    if testa[:2] == ['Serv.', 'Percorso'] and testa[-1] == 'Uso nel disegno':
        for r in t.rows[1:]:
            if r.cells[-1].text.strip().startswith('Sì'):
                si += 1
                servizi.add(r.cells[0].text.strip())
assert (si, len(servizi)) == (36, 15), (si, len(servizi))
sost('Il disegno attuale conosce una sola operazione di deposito, quella di R009 ma sull’intero '
     'dominio',
     'Il disegno conosce due operazioni di deposito — la validazione di R009 e la rettifica di '
     'R013, per l’annullamento e le annotazioni rettificative — ma sull’intero dominio')
FATTI.append('Funzioni ANSC: inventario «Uso nel disegno» (36 operazioni, 15 servizi)')

# ================================================================== 13. R009: parto plurimo
dopo = svuota('La prenotazione degli identificativi per il parto plurimo', 3)
blocchi(dopo, [
    ('p', 'La terza operazione di R009 è quella meno documentata e la più fraintendibile, perché '
          'il nome promette meno di quanto faccia. La guida operativa è esplicita — il servizio '
          '«restituisce gli identificativi unici nazionali degli atti di ciascun gemello» e '
          '«predispone gli atti di ciascun gemello, che dovrai completare acquisendo metadati e '
          'firme» — e la risposta lo conferma, restituendo accanto agli identificativi nazionali '
          'anche quelli interni degli eventi. Dopo la chiamata esistono in ANSC N atti in stato '
          'di bozza.'),
    ('p', 'Il modello evento, nel blocco dei dati di nascita, porta due liste — gli atti dei '
          'fratelli precedenti e quelli dei fratelli successivi — che contengono gli '
          'identificativi nazionali degli altri gemelli. L’atto del primo nato deve quindi citare '
          'l’identificativo del secondo, e viceversa, e ANSC non consente di aggiornare un atto '
          'depositato. È una dipendenza circolare, che senza un’assegnazione anticipata degli '
          'identificativi non ha soluzione. La prenotazione serve a spezzarla.'),
    ('l', 'Due casi, decisi dagli UC dei nati. ',
     'Le risposte pubblicate da ANSC nel proprio repository hanno chiarito come la prenotazione '
     'si usi dal gestionale [R18]. Se tutti i nati hanno lo stesso UC, la prenotazione porta '
     'quell’UC e le bozze si completano con esso tramite i servizi cooperativi (caso 1). Se gli '
     'UC differiscono — per esempio un nato vivo e un nato morto — si prenota con il caso d’uso '
     'di servizio 11999999, gli atti si completano sulla web app e tornano in SIPO con il '
     'recupero (caso 2). Il numero da passare è il totale dei nati, nati morti compresi.'),
    ('tab', [
        ['Passo', 'Operazione', 'Stato dell’atto'],
        ['Divisione della pratica', 'In SIPO, alla conferma del Riepilogo: un atto per nato, '
         'l’UC di ciascuno, i numeri comunali in blocco dal servizio della numerazione.',
         'In ANSC nulla; in SIPO N atti in 1 IN LAVORAZIONE.'],
        ['Prenotazione', 'R009 /prenota/evento con il numero dei nati, la lista dei numeri '
         'comunali e l’UC (11999999 nel caso 2).',
         'Nascono N atti in BOZZA, ciascuno con il proprio identificativo nazionale.'],
        ['Completamento', 'Caso 1: R001, R009 /validazione/evento con la composizione, firme '
         'R006 o R012 e R007, un gemello alla volta. Caso 2: sulla web app, poi il recupero.',
         'CONFERMATO, poi fino a FIRMATO DA USC.'],
        ['Chiusura', 'R011, la cancellazione logica già prevista.',
         '9 CANCELLATO. L’identificativo nazionale resta consumato.'],
    ], [1.3, 3.2, 1.7]),
    ('p', 'Il ciclo di vita di una prenotazione.'),
    ('p', 'Ne discende che gli atti prenotati sono, per il Comune, atti a tutti gli effetti fin '
          'dal momento della prenotazione: vanno registrati nello store di stato subito, una riga '
          'per gemello, e vanno sorvegliati. Una prenotazione dimenticata non è un numero '
          'sprecato, è un atto aperto in ANSC. La prenotazione va aggiunta al contratto del '
          'concentratore; la chiusura riusa la cancellazione logica.'),
    ('p', 'Che cosa comporta, in concreto, registrare un parto plurimo:'),
    ('v', 'La composizione la genera SIPO. ',
     'Le bozze prenotate nascono senza composizione, e ANSC chiede di trasmetterla con la '
     'validazione successiva. SIPO la compone con il proprio formulario, con le formule '
     'ministeriali del parto gemellare e gli identificativi dei fratelli, e la invia in '
     'composizioneCompleta; il testo si conserva su ANSC_SOGGETTO_ATTO. Il mapping degli UC '
     'ordinari non dichiara il campo: va confermato con il fornitore (OP-86).'),
    ('v', 'La firma del dichiarante. ',
     'La guida esclude la firma elettronica per i parti gemellari sulla web app, quindi nel caso '
     '2. Nel caso 1 il disegno ammette sia la firma su carta (R006) sia quella elettronica '
     '(R012), da provare in preproduzione (OP-87).'),
    ('v', 'Si completa un gemello alla volta. ',
     'Un parto trigemino sono tre finalizzazioni consecutive, e la sessione OTP deve reggerle: è '
     'un caso in cui il margine residuo minimo va valutato sull’intera lavorazione e non sul '
     'singolo atto.'),
    ('v', 'I numeri comunali si allocano in blocco e in anticipo. ',
     'Li stacca il concentratore alla divisione, prima della prenotazione che li richiede tutti. '
     'Se un gemello viene chiuso, il suo numero si scarta.'),
    ('v', 'Documenti e firmatari prima della divisione. ',
     'Si raccolgono nel Riepilogo per ciascun nato quando gli atti dei gemelli successivi al '
     'primo non esistono ancora, mentre ALLEGATO e firmatari hanno la chiave sull’atto (OP-88).'),
    ('v', 'I campi gemellari non compaiono in alcun mapping. ',
     'Il numero dei gemelli e il progressivo del singolo nato esistono nel modello evento ma '
     'nessuno dei casi d’uso pubblicati li dichiara: li valorizza il concentratore.'),
    ('p', 'La pagina «Gemelli del parto», le sue finestre e le transizioni di stato sono descritte, '
          'come manuale per lo sviluppatore, nel documento specifico [R18].'),
    ('img', 'gemellari/gem10_navigazione.pptx.png', 6.0,
     'Le pagine e le finestre del parto plurimo: dal Riepilogo alla pagina «Gemelli del parto» '
     '[R18].'),
], modello=MODELLO)
FATTI.append('R009: prenotazione del parto plurimo riscritta sui due casi')

# ================================================================== 14. Schede dei servizi
r002 = tab_con('Percorso', '/certificato', '/certificato-semplice')
cella(r002, '/certificato', 1, 'Rilascia l’estratto per riassunto e la copia integrale (tipi 2 e 3).')
cella(r002, '/certificato', 2,
      'idAnsc e idEvento, intestatario, richiedente, tipo di certificato e di uso, lingue; '
      'parametriFirma per i tipi 2 e 3')
cella(r002, '/certificato', 3,
      'Restituisce il PDF/A in base64 e ne registra l’emissione; il documento è firmato '
      'dall’ufficiale.')
cella(r002, '/certificato-semplice', 1,
      'Rilascia il certificato semplice (tipo 1), anche con il permesso ridotto.')
cella(r002, '/certificato-semplice', 2, 'Come sopra, senza parametri di firma.')
cella(r002, '/certificato-semplice', 3, 'Documento con il sigillo del Ministero e il QR di verifica.')
lead(nella_sezione('R002 — Certificazione', 2, 'Prerequisiti.'), 'Prerequisiti. ',
     'Sessione OTP attiva. Le credenziali di firma remota dell’ufficiale servono soltanto per '
     'l’estratto per riassunto e la copia integrale, che portano i parametri di firma; il '
     'certificato semplice esce con il sigillo del Ministero e il QR di verifica, senza firma.')
lead(nella_sezione('R002 — Certificazione', 2, 'Modalità di adozione.'), 'Modalità di adozione. ',
     'Adottato per gli atti con identificativo ANSC: la fonte del documento la decide l’atto '
     '(capitolo «La certificazione degli atti formati in ANSC», [R20]). Prima dell’emissione si '
     'consulta l’atto con R005 nella forma sintetica; non esiste un’anteprima, ogni chiamata '
     'emette un certificato.')
lead(nella_sezione('R002 — Certificazione', 2, 'Uso nel disegno.'), 'Uso nel disegno. ',
     'Sì — atti formati in ANSC [R20]')
lead(nella_sezione('R006 — Firma cartacea', 2, 'Modalità di adozione.'), 'Modalità di adozione. ',
     'È la modalità del pilota: per gli atti di morte la firma del dichiarante è cartacea. Per i '
     'parti gemellari è l’unica ammessa sulla web app; nel caso 1, completato da SIPO, si affianca '
     'alla firma elettronica (R012) [R18].')
r011 = tab_con('Percorso', '/evento/elimina')
cella(r011, '/evento/elimina', 3, 'Porta l’evento allo stato 9 CANCELLATO.')
lead(nella_sezione('R012 — Firma elettronica', 2, 'Modalità di adozione.'), 'Modalità di adozione. ',
     'Non impiegata nel pilota, dove la firma è cartacea. Per i parti gemellari la guida la '
     'esclude sulla web app; nel caso 1, completato da SIPO, il disegno la prevede accanto alla '
     'firma su carta, da provare in preproduzione (OP-87). Chi la adotta deve prevedere '
     'un’attesa non presidiata: fra invio e conferma passa tempo indeterminato, e l’atto resta in '
     'uno stato intermedio.')
lead(nella_sezione('R012 — Firma elettronica', 2, 'Uso nel disegno.'), 'Uso nel disegno. ',
     'Sì — firma elettronica del dichiarante')
r013 = tab_con('Percorso', '/rettifica/validazione/evento', '/annotazione/modificativa/validazione/evento')
cella(r013, '/rettifica/validazione/evento', 2,
      'evento (l’annotazione) e, per correggere, eventoModificato (l’atto già corretto); per '
      'l’annullamento basta evento')
riscrivi(nella_sezione('R013 — Rettifica', 2, 'Deposita le annotazioni che modificano'),
         'Deposita le annotazioni che correggono o modificano un atto già formato: la rettifica '
         'disposta da un’autorità terza (art. 95), che può anche annullare l’atto, l’annotazione '
         'per errore materiale (art. 98), promossa dall’ufficiale, e le annotazioni modificative '
         '(cambio di generalità del genitore, regime patrimoniale, cambio di sesso).')
lead(nella_sezione('R013 — Rettifica', 2, 'Modalità di adozione.'), 'Modalità di adozione. ',
     'Adottato per l’annullamento e per le annotazioni rettificative formate da SIPO (percorso B, '
     '[R19]). Per correggere, il corpo porta due modelli evento: l’annotazione e l’atto già '
     'corretto per intero, che non è un differenziale; per l’annullamento basta l’annotazione. La '
     'risposta non ha campi propri per gli identificativi, che stanno dentro l’evento '
     'restituito.')
lead(nella_sezione('R013 — Rettifica', 2, 'Uso nel disegno.'), 'Uso nel disegno. ',
     'Sì — annullamento e annotazioni rettificative [R19]')
nella_sezione('R017 — Correzione', 2, 'Trappole e avvertenze.').add_run(
    ' Sulla web app la correzione di annotazione è stata disabilitata con la versione 1.52.0 e '
    'allineata all’errore materiale con la 1.53.0 [R19].')
lead(nella_sezione('R019 — Certificati internazionali', 2, 'Modalità di adozione.'),
     'Modalità di adozione. ',
     'Adottato per i certificati plurilingue degli atti formati in ANSC [R20]. Va prevista la '
     'selezione esplicita delle enunciazioni: la guida avverte che le sigle non selezionate non '
     'compaiono sull’estratto.')
nella_sezione('R019 — Certificati internazionali', 2, 'Avvertenze.').add_run(
    ' Il contratto non dichiara la firma del certificato (OP-98).')
lead(nella_sezione('R019 — Certificati internazionali', 2, 'Uso nel disegno.'), 'Uso nel disegno. ',
     'Sì — certificati plurilingue [R20]')
# scheda R009
r009 = tab_con('Percorso', '/validazione/evento', '/collegamento/evento', '/prenota/evento')
cella(r009, '/prenota/evento', 2,
      'numero dei nati, nati morti compresi; lista dei numeri comunali; caso d’uso')
nella_sezione('R009 — Validazione e deposito', 2, 'Modalità di adozione.').add_run(
    ' I casi sono due, secondo gli UC dei nati [R18].')
nella_sezione('R009 — Validazione e deposito', 2, 'Avvertenze.').add_run(
    ' La prenotazione dei gemelli con il caso d’uso 11999999 resta possibile dal gestionale, '
    'come verificato dal Comune [R18].')
FATTI.append('Schede: R002, R006, R009, R011, R012, R013, R017, R019')

# ================================================================== 15. PC-11
h_sic = D.h(d, 1, 'Sicurezza e configurazione')
blocchi(h_sic._p, [
    ('h2', 'PC-11 — Un atto formato in ANSC si certifica da ANSC'),
    ('p', 'La fonte del certificato è decisa dall’atto: per un atto con identificativo ANSC '
          'certificati, estratti e copie integrali si emettono con R002 e R019 attraverso il '
          'concentratore, perché l’originale e le sue annotazioni stanno in ANSC; per gli altri '
          'atti resta il formulario di SIPO. Alternativa scartata: ricomporre in SIPO anche gli '
          'atti ANSC, che produrrebbe documenti firmati potenzialmente divergenti dall’atto vero. '
          'Prezzo accettato: la sessione OTP e, per estratti e copie integrali, la firma remota '
          'dell’ufficiale entrano nello sportello dei certificati. Vedi il capitolo «La '
          'certificazione degli atti formati in ANSC» e [R20].'),
])

# ================================================================== 16. Open Point
def op(codice, questione=None, stato=None):
    r = riga(REG, codice)
    if questione is not None:
        D.riscrivi_cella(r.cells[2], questione)
    if stato is not None:
        D.riscrivi_cella(r.cells[3], stato)


op('OP-31', 'Chiuso. Verso ANSC si forma un atto per ciascun nato; la pratica unica di SIPO si '
   'divide in N atti legati da ATTO.ID_LAVORAZIONE_PADRE, lo store porta una riga per gemello e '
   'ANSC_SOGGETTO_ATTO lega i nati ai propri atti. Il numero da passare alla prenotazione è il '
   'totale dei nati, nati morti compresi; i nati con UC diversi seguono il caso 2 [R18].', 'Chiuso')
op('OP-43', 'La nota tecnica si fa solo sulla web app, dal comune che ha redatto l’atto, e ANSC '
   'non la notifica. Va stabilito come SIPO ne venga a sapere (adempimento dell’ufficio con '
   'l’avvio da SIPO, controllo all’apertura del dettaglio o controllo periodico), se l’ufficiale '
   'la firmi e con quale OTP, e che cosa significhi il tipo 3 NOTATECNICARETTIFICA della '
   'decodifica ANSC_79. Il riallineamento è descritto in «La rettifica tecnica e il '
   'riallineamento» [R19].')
op('OP-45', 'Ricognizione di quale servizio di deposito serva a ciascun caso d’uso: oltre a R009 '
   'esistono sei servizi che portano un evento in ANSC (rettifica, annotazione modificativa, '
   'adozione internazionale, adozione multi intestatario, correzione di annotazione, '
   'provvedimento di rifiuto). Il concentratore ne conosce due: R009 e, per l’annullamento e le '
   'annotazioni rettificative, R013 [R19].')
op('OP-46', 'Meccanica del completamento di una bozza prenotata: con quale campo la validazione '
   'riconosca l’atto già creato dalla prenotazione, dato che il modello evento porta sia '
   'l’identificativo interno sia quello nazionale. Un errore non produce un errore ma un '
   'duplicato: da verificare in preproduzione. La prenotazione con il caso d’uso 11999999 resta '
   'possibile dal gestionale, come verificato dal Comune, e nel caso 1 le bozze si completano con '
   'l’UC specifico; il numero di una prenotazione chiusa si scarta con PUT /scarta [R18].')
op('OP-66', 'Chiuso. Il riferimento all’atto (identificativo nazionale, numero comunale, data, '
   'canale) si registra per tutti gli atti formati sulla web app; per l’atto nato sulla web app si '
   'acquisisce la scheda essenziale (atto, area, intestatari, testo) e l’importazione completa '
   'solo per gli UC ordinari la cui configurazione consente la transcodifica inversa [R21]. La '
   'certificazione non è fra i criteri: un atto con identificativo ANSC si certifica da ANSC '
   '[R20].', 'Chiuso')
op('OP-78', 'Due aspetti della scelta dell’UC. (a) La pagina dei dati anagrafici legge da '
   'SOGGETTI_USECASE quale soggetto sia l’intestatario, ma l’UC si determina soltanto nel '
   'Riepilogo: quando il Modello indirizza più UC con intestatari diversi va stabilito su quale UC '
   'si legga l’intestatario, o se la pagina debba attendere la determinazione. (b) Chiuso: quando '
   'nessun UC è determinabile l’atto segue la strategia adottata per gli atti a testo libero, per '
   'le dichiarazioni come per le trascrizioni (capitolo «Atti a Testo Libero», [R16]). Si lega a '
   'OP-32.')
r79 = riga(REG, 'OP-79')
D.riscrivi_cella(r79.cells[2], r79.cells[2].text.strip() +
                 ' (f) La destinazione del numero alla web app e il passaggio a Scartato dopo un '
                 'numero di giorni configurabile [R21].')
op('OP-81', 'In parte chiuso: la firma dell’annotazione per rettifica è dell’ufficiale con R007 '
   '[R19]. Resta da accertare se l’annotazione richieda anche l’attestazione di conformità degli '
   'allegati.')
r82 = riga(REG, 'OP-82')
D.riscrivi_cella(r82.cells[2], r82.cells[2].text.strip() +
                 ' Comprende l’allineamento anagrafico di SIPO: oggi lo esegue a ogni annullamento, '
                 'e per un atto formato in ANSC farlo due volte sarebbe un errore [R19].')
op('OP-84', 'Chiuso. Per l’atto formato in ANSC la rettifica di SIPO non si offre; annullamento e '
   'annotazioni rettificative seguono due percorsi, web app e riallineamento oppure formazione da '
   'SIPO con R013, e la rettifica tecnica usa il riallineamento [R19].', 'Chiuso')
r85 = riga(REG, 'OP-85')
D.riscrivi_cella(r85.cells[2], r85.cells[2].text.strip() +
                 ' Le dichiarazioni a testo libero o senza UC seguono la strategia adottata, con la '
                 'stesura sulla web app e DEFINISCI (capitolo «Atti a Testo Libero», [R16]); resta '
                 'aperto il rientro di una dichiarazione lavorata in emergenza.')

NUOVI_OP = [
    ('OP-86', 'Composizione del testo delle bozze prenotate',
     'Per le bozze prenotate dei gemelli ANSC chiede che la composizione arrivi con la '
     'validazione, ma il mapping degli UC ordinari non dichiara composizioneCompleta. Va '
     'confermato con il fornitore, insieme alla forma attesa del testo (parti, formule, '
     'identificativi dei fratelli) [R18].', 'Analisi / Fornitore ANSC', 'Media'),
    ('OP-87', 'Firma elettronica dei dichiaranti dei gemelli',
     'Nel caso 1 il disegno ammette la firma elettronica (R012) accanto a quella su carta, mentre '
     'la guida la esclude per i parti gemellari sulla web app: da provare in preproduzione '
     '[R18].', 'Analisi / Fornitore ANSC', 'Media'),
    ('OP-88', 'Documenti e firmatari prima della divisione',
     'Nel Riepilogo della pratica unica documenti e firmatari si raccolgono per ciascun nato, '
     'quando gli atti dei gemelli successivi al primo non esistono ancora, mentre ALLEGATO e '
     'firmatari hanno la chiave sull’atto. Va scelta la struttura d’appoggio [R18].',
     'Analisi', 'Alta'),
    ('OP-89', 'Cambio di UC dopo la prenotazione',
     'Se dopo la prenotazione l’UC di un gemello cambia, la bozza prenotata non si rivalida con un '
     'altro caso d’uso; per il caso 2 va stabilito quale motivo del recupero (ANSC_96) dichiarare '
     '[R18].', 'Analisi / Fornitore ANSC', 'Media'),
    ('OP-90', 'Procedure di cancellazione e annullamento di SIPO',
     'Il corpo corrente di PKG_PRATICA (annullaPRATICA, annullaATTO, cancellaATTO) non è fra le '
     'sorgenti, e il servizio /cancellaAnnullaAtto non è transazionale: con R011 nel mezzo l’ordine '
     'dei passi diventa vincolante [R19].', 'Sviluppo SIPO', 'Alta'),
    ('OP-91', 'Identificativi e tipo delle annotazioni rettificative',
     'Il valore di idTipoRettifica per l’errore materiale (1 nella nota di processo, assente dai '
     'mapping), lo stato dell’annotazione e dell’atto dopo la firma, e dove R013 restituisca gli '
     'identificativi dell’annotazione [R19].', 'Analisi / Fornitore ANSC', 'Media'),
    ('OP-92', 'Annotazioni su atto cartaceo',
     'Con quale servizio si depositano le annotazioni modificative su atto cartaceo (casi d’uso '
     '*_998_4) e se il Comune debba registrare in ANSC le annotazioni dei propri atti cartacei '
     '[R19].', 'Comune / Fornitore ANSC', 'Alta'),
    ('OP-93', 'Numero comunale dell’annotazione',
     'Il mapping chiede un numero comunale per l’annotazione e nessuna fonte dice da quale serie '
     'venga. Il documento specifico assume la serie degli atti [R19].', 'Comune / Analisi', 'Media'),
    ('OP-94', 'Stato di attesa della web app',
     'Lo store tiene l’atto in attesa della web app fra l’Anteprima e DEFINISCI, ma STATO replica i '
     'codici numerici di ANSC_11: va scelto dove registrare l’attesa (stato applicativo, come lo 0, '
     'oppure COD_FASE) e quale sia il termine massimo di permanenza [R16].', 'Analisi', 'Media'),
    ('OP-95', 'Numero comunale diverso da quello staccato',
     'Un atto formato sulla web app con un numero non staccato da SIPO, o diverso da quello '
     'staccato per lui: se si aggancia o si acquisisce con un avviso, oppure si respinge [R16] '
     '[R21].', 'Comune / Analisi', 'Media'),
    ('OP-96', 'Adempimenti anagrafici degli atti formati sulla web app',
     'Per un atto nato sulla web app con UC ordinario la comunicazione anagrafica la predispone ANSC '
     'e SIPO non la ripete; per un caso d’uso di servizio ANSC non la predispone e DEFINISCI la '
     'esegue con /finalizzaAtto. La regola va confermata, insieme alle annotazioni sugli atti '
     'collegati che il caso d’uso di servizio non genera [R16] [R21].', 'Analisi / Comune', 'Alta'),
    ('OP-97', 'Le pagine del recupero',
     'Il recupero degli atti formati sulla web app è descritto su due superfici: le pagine di SIPO '
     '«Recupero Atto ANSC» e «Acquisizione Atto ANSC» [R16] e la pagina del back-office [R21]. Va '
     'deciso chi le usa e se restino entrambe.', 'Comune / Analisi', 'Media'),
    ('OP-98', 'Dati e firma dei certificati',
     'I campi obbligatori di R002 (identificativi dell’evento e dell’intestatario), lo stato '
     'dell’atto che consente la certificazione, il trattamento dell’atto secretato e la firma dei '
     'certificati plurilingue di R019, che il contratto non dichiara [R20].',
     'Analisi / Fornitore ANSC', 'Media'),
    ('OP-99', 'Conservazione, bollo e diritti dei certificati ANSC',
     'Se e dove conservare il PDF restituito da ANSC, che non è riscaricabile; come trattare bollo, '
     'diritti ed esenzioni, che ANSC non gestisce; come tracciare le consultazioni [R20].',
     'Comune / Analisi', 'Media'),
    ('OP-100', 'Atto su cui decidere l’instradamento e certificati ANPR',
     'Su quale atto si decide la fonte del certificato quando la persona ne ha più d’uno, e se i '
     'certificati oggi chiesti ad ANPR debbano passare ad ANSC per gli atti digitali [R20].',
     'Analisi / Comune', 'Alta'),
    ('OP-101', 'Operatori dell’ufficio certificati in ANSC',
     'Utenza, permessi (consultazione, certificato semplice o pieno) e postazione registrata degli '
     'operatori dell’ufficio certificati che emettono da ANSC [R20].', 'Comune / Fornitore ANSC',
     'Media'),
]
for c, tema, q, owner, prio in NUOVI_OP:
    D.clona_riga(REG, (c, tema, q, 'Aperto', owner, prio))
FATTI.append('Open Point: OP-31/66/84 chiusi, OP-43/45/46/78/79/81/82/85 riformulati, '
             'OP-86…OP-101 nuovi')

# ================================================================== 17. Back-office
cat = tab_con('Categoria', 'Da riprendere', 'In emergenza da rientrare')
for valori in [
    ('Parto plurimo incompleto', 'BOZZA / CONFERMATO',
     'Gemelli prenotati e non completati, oppure un gemello firmato in ANSC e non definito in SIPO',
     'Ripresa dalla pagina «Gemelli del parto», che rilegge lo stato di ciascun gemello con R005; '
     'oppure chiusura del gemello (R011) [R18]', 'R005 → R009 / R011'),
    ('In attesa della stesura sulla web app', 'Nessuno (in ANSC l’atto non è ancora noto)',
     'Atto senza UC o a testo libero, con il numero staccato, non ancora definito con DEFINISCI',
     'Sollecito all’ufficiale, oppure abbandono con lo scarto del numero. Ordinare per anzianità '
     '[R16].', 'R005'),
    ('Rettifica tecnica da riallineare', 'FIRMATO DA USC',
     'Rettifica tecnica avviata da SIPO e non seguita dal riallineamento',
     'Riallineamento dei dati di SIPO con «RIALLINEA DA ANSC» [R19]', 'R005'),
]:
    D.clona_riga(cat, valori)
az = tab_con('Stato reale', 'FIRMATO DA USC', 'BOZZA (atto prenotato)')
cella(az, 'FIRMATO DA USC', 1,
      'Riconcilia (R005) — back-office; dal dettaglio dell’atto in SIPO: RETTIFICA TECNICA, '
      'ANNULLA ATTO e annotazioni rettificative (web app e riallineamento, oppure R013) — USC')
cella(az, 'FIRMATO DA USC', 2,
      'L’atto è formato: non si riapre, si annota o si corregge con gli istituti di ANSC [R19].')
cella(az, 'BOZZA (atto prenotato)', 1,
      'Completa nella pagina «Gemelli del parto» → conferma; Chiudi la prenotazione (R011)')
FATTI.append('Back-office: tre categorie di eccezione, azioni per FIRMATO DA USC e BOZZA')

# ================================================================== 18. testata e storia
for fatto in D.frontespizio(d, '3.61', 'ANALISI_Integrazione-ANSC_v3.61') or []:
    FATTI.append(str(fatto))
for sez in d.sections:
    for t in sez.header.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip() == 'Versione 3.60':
                    D.riscrivi_cella(c, 'Versione 3.61')
D.storia(d, DATA, '3.61',
         'Riferimenti · Requisiti · Le quattro fasi · I Log · Atti a Testo Libero · Cancellazione · '
         'Atto firmato · SIPO e la web app · La certificazione degli atti formati in ANSC (nuovo) · '
         'Numerazione · Funzioni ANSC (R009) · Schede · PC-11 · Open Point · Back-office',
         'Recepiti, in sintesi e con rinvio, i documenti di dettaglio: nascite gemellari [R18], '
         'annullamento, cancellazione e rettifiche [R19], atti a testo libero [R16], '
         'certificazioni [R20], recupero dalla web app [R21]; citati l’osservabilità [R22], il '
         'processo della numerazione [R23] e lo studio sugli identificativi verso ANPR [R24]. '
         'Corrette le affermazioni superate (certificazione, firma del dichiarante per i gemelli, '
         'esito di R011, finestra fino a mezzanotte). RF-23, PC-11, OP-86…OP-101.')

assert len(d.element.body.findall('.//' + qn('w:commentRangeStart'))) == ANCORE
d.save(OUT)
for f in FATTI:
    print('  ' + f)
print('ancore di commento:', ANCORE)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
