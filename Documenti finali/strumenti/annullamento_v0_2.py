# -*- coding: utf-8 -*-
"""v0.2 di «ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC» (08/11/2026).

Parte dalla v0.1 RIVISTA A MANO dall'utente (salvata alle 10:34): si modifica il file reale,
`genera_annullamento_rettifiche.py` NON va più rieseguito.

Richiesta: il flusso e le indicazioni per le rettifiche tecniche di un atto firmato e chiuso,
verificati sulle informazioni ANSC. Fonti verificate:
- Guida operativa ANSC — Servizi di ausilio, § 3.5 «Correzione evento tramite nota tecnica»
  (pp. 15-22 a stampa): finalità (metadati inesatti per malfunzionamento di ANSC o del
  gestionale, errori dell'ufficiale), solo web app, solo il comune che ha redatto l'atto, stato
  FIRMATO DALL'USC, nessuna annotazione modificativa successiva, numero nazionale, testo della
  modifica, §§ 3.5.1-3.5.4 (dati errati, mancanti, eccedenti, annotazioni contestuali), § 3.5.5
  consultazione, § 3.5.6 impatto sulle certificazioni; § 3.4 allegati errati (motivazione
  obbligatoria, attestazione di conformità e firma remota); §§ 3.1-3.3, 3.6 gli altri servizi.
- model_evento.yaml: `noteTecniche` (lista di stringhe), `datiNotaTecnica` → `ModelNotaTecnica`
  (`eventoDaModificare`, `notaTecnica`), senza data, operatore, motivo o stato.
- R005 `/consultazione/ansc/evento/note/tecniche/{version}` con `idEvento` (id interno ANSC).
- Changelog: 1.25.0 introduzione (solo web app, cooperativo solo consultazione), 1.27.0 allegati e
  attestazione, 1.27.5 motivo obbligatorio, 1.35.0 disabilitata, 1.40.0 ripristinata, 1.43.0
  comunicazioni anagrafiche, 1.46.0/1.46.3 notifiche, 1.48.6 disassociazione, 1.49.0 annotazioni
  sull'atto principale, 1.53.0 intestatario con duplicazione e riconciliazione.
- ANSC_79 valore 3 NOTATECNICARETTIFICA: nessuna fonte lo spiega.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/annullamento_v0_2.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import figura, h, par, tabella, voce, _versa   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.1.docx')
NOME = 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.2'
OUT = os.path.join(FIN, NOME + '.docx')
IMG = os.path.join(QUI, 'img', 'annullamento')
DATA = '08/11/2026'

d = docx.Document(SRC)
body = d.element.body
FIGURE_PRIMA = len(d.inline_shapes)


def heading(testo, livello):
    t = [p for p in d.paragraphs if p.style.name == 'Heading %d' % livello
         and p.text.strip() == testo]
    if len(t) != 1:
        raise SystemExit('heading non univoco: ' + testo)
    return t[0]


def innesta(prima, scrivi):
    """Scrive in coda al documento con le primitive di genera_testo_libero e sposta il
    blocco prima dell'elemento «prima»."""
    sect = body.find(qn('w:sectPr'))
    n0 = len(list(body.iterchildren()))
    scrivi()
    nuovi = [ch for ch in list(body.iterchildren())[n0 - 1:] if ch is not sect
             and ch.getparent() is body]
    # n0 - 1: l'ultimo figlio prima della scrittura è sectPr, che resta in fondo
    for ch in nuovi:
        prima.addprevious(ch)
    return len(nuovi)


# =================================================================== capitolo 4
NOTA_COSA = [
    ['Situazione dell’atto', 'Che cosa consente la nota tecnica', 'Guida'],
    ['Sezioni previste dal caso d’uso ma con dati errati o incompleti',
     'Modificare i dati, aggiungerne, eliminarne, «nel rispetto delle obbligatorietà previste '
     'per il caso d’uso»; «possono essere modificati tutti i dati presenti nelle varie sezioni», '
     'per esempio data e ora dell’evento.', '§ 3.5.1'],
    ['Sezioni obbligatorie non registrate (per esempio madre e padre mancanti per un '
     'malfunzionamento)', 'Inserire le informazioni obbligatorie mancanti prima di concludere.',
     '§ 3.5.2'],
    ['Dati o sezioni non previsti dal caso d’uso', 'Eliminarli dalla sezione «Dati eccedenti».',
     '§ 3.5.3'],
    ['Annotazioni contestuali errate', 'Modificarne descrizione, tipologia, testo e attributo '
     'di certificabilità, oppure eliminarle (da «Dati eccedenti»).', '§ 3.5.4'],
]

ALTRE_CORREZIONI = [
    ['Servizio (web app, «Altri servizi»)', 'Che cosa corregge', 'Firma', 'Servizio cooperativo'],
    ['Gestione degli allegati errati (§ 3.4)', 'Toglie, sostituisce o aggiunge documenti '
     'allegati a un evento del proprio comune; motivazione obbligatoria nella «Nota di modifica».',
     'Attestazione di conformità e firma remota', 'No'],
    ['Correzione annotazione (§ 3.2)', 'La minuta di un’annotazione non automatica e non '
     'contestuale del proprio comune.', 'Firma remota', 'R017; sulla web app disabilitata dalla '
     '1.52.0'],
    ['Gestione data decorrenza anagrafica (§ 3.1)', 'Aggiunge la data di decorrenza mancante.',
     '—', 'No'],
    ['Gestione certificati emissibili (§ 3.3)', 'I certificati emissibili per gli eventi con '
     'caso d’uso di servizio.', '—', 'No'],
    ['Riconciliazione soggetto per id (§ 3.6)', 'Fonde due anagrafiche ANSC identiche, o allinea '
     'l’anagrafica ANSC a quella ANPR (codice fiscale, residenza, identificativo ANPR).', '—',
     'R018; l’annullamento della riconciliazione dalla 1.53.0'],
    ['Disassociazione annotazione', 'Scollega un’annotazione dall’atto; dalla 1.48.6 anche le '
     'note tecniche. Non descritta nella guida.', '—', 'No'],
]


def capitolo_4():
    h(d, 2, 'Le rettifiche tecniche di un atto firmato e chiuso')
    par(d, 'Accanto alle rettifiche dell’ordinamento (art. 95 e 98), che formano un atto nuovo, '
           'ANSC offre strumenti di **correzione tecnica**: non richiedono un provvedimento, non '
           'producono un’annotazione con numero proprio e intervengono sui dati dell’atto già '
           'formato. Stanno tutti sulla web app, nel menù «Altri servizi», e sono riservati al '
           'comune che ha formato l’atto [A3]. Il principale è la nota tecnica.')

    h(d, 3, 'La nota tecnica: a che cosa serve')
    par(d, 'La guida dei servizi di ausilio (§ 3.5) la descrive così: «La funzionalità consente '
           'ai Comuni di correggere atti che presentano delle inesattezze nei metadati causate '
           'da: temporaneo malfunzionamento del sistema centrale; temporaneo malfunzionamento del '
           'gestionale comunale; errori dell’ufficiale dello stato civile». Gli atti da correggere '
           'hanno informazioni essenziali mancanti, informazioni non attinenti al caso d’uso '
           'scelto o annotazioni contestuali errate.')
    par(d, 'Tre vincoli la delimitano:')
    voce(d, 'Solo web app.', '«Data la straordinarietà dell’operazione e la necessità di '
         'controllare centralmente la funzionalità particolarmente delicata, l’inserimento della '
         'nota tecnica sarà possibile esclusivamente dalla Web Application di ANSC». Per i servizi '
         'cooperativi esiste solo la consultazione (changelog 1.25.0).')
    voce(d, 'Solo il comune che ha redatto l’atto.', 'E solo su un atto nello stato «FIRMATO '
         'DALL’USC» su cui non siano state apposte successivamente annotazioni modificative.')
    voce(d, 'Una storia instabile.', 'Introdotta con la 1.25.0 (febbraio 2024), disabilitata con '
         'la 1.35.0 (dicembre 2024), ripristinata con la 1.40.0 (aprile 2025) e poi estesa più '
         'volte. Il perimetro è cambiato a ogni rilascio [A5].')

    h(d, 3, 'Il processo sulla web app')
    figura(d, os.path.join(IMG, 'nota_tecnica_webapp.png'), 5.6,
           'Figura 4 — La correzione dell’atto tramite nota tecnica (Guida dei servizi di '
           'ausilio, § 3.5).')
    voce(d, '1. Evento da modificare.', 'L’ufficiale indica il **numero nazionale** dell’atto '
         '(idAnsc). Il sistema verifica che l’atto sia del comune in sessione e nello stato '
         '«FIRMATO DA USC».')
    voce(d, '2. Testo e motivo.', 'L’ufficiale scrive il testo della modifica; il motivo '
         'dell’utilizzo è obbligatorio dalla 1.27.5. Il sistema chiede conferma prima di '
         'procedere.')
    voce(d, '3. Correzione.', 'I dati dell’atto si presentano in modifica, secondo la tabella '
         'che segue.')
    voce(d, '4. Allegati e conclusione.', 'Dalla 1.27.0 la nota tecnica gestisce allegati e '
         'attestazione di conformità. La guida non dice se l’ufficiale firmi la nota con OTP: il '
         'changelog cita un errore «su firma USC» corretto nella 1.29.5, indizio di una firma che '
         'nessun documento descrive [DA VERIFICARE].')
    tabella(d, NOTA_COSA, [2.1, 4.0, 0.8])
    par(d, 'Il changelog ha esteso via via i dati correggibili: la descrizione del caso d’uso '
           '(1.27.5), il regime patrimoniale di matrimoni e unioni (1.32.0), la tipologia '
           'dell’atto collegato (1.32.10), il numero comunale (1.33.0), lo stato civile del '
           'soggetto e la data di decorrenza delle annotazioni contestuali (1.41.2), il '
           'contrassegno di firmatario dell’officiante (1.43.2) e, dalla 1.53.0, il soggetto '
           'intestatario, con duplicazione e riconciliazione automatica. La guida non elenca dati '
           'che non si possano correggere: l’unico limite dichiarato sono le obbligatorietà del '
           'caso d’uso.')

    h(d, 3, 'Gli effetti')
    voce(d, 'Certificati ed estratti.', '«Una volta registrata la nota tecnica, le certificazioni '
         'e gli estratti conterranno i dati dell’atto già corretto» (§ 3.5.6). Dalla 1.46.3 '
         'l’anteprima dell’estratto integrale (R010) si comporta allo stesso modo dal gestionale e '
         'dalla web app.')
    voce(d, 'Consultazione.', '«La nota tecnica è consultabile come le altre annotazioni '
         'associate all’atto originario» (§ 3.5.5). Per i servizi cooperativi c’è R005 '
         '`/consultazione/ansc/evento/note/tecniche`, che chiede l’`idEvento` (l’identificativo '
         'interno di ANSC, non l’idAnsc) e restituisce eventi; nel modello la nota sta in '
         '`datiNotaTecnica` (`eventoDaModificare`, `notaTecnica`) e in `noteTecniche`, una lista di '
         'testi.')
    voce(d, 'Conservazione.', 'La nota tecnica è inviata al sistema di conservazione digitale '
         '(guida e 1.35.0).')
    voce(d, 'Anagrafe e altri comuni.', 'Dalla 1.43.0 una nota tecnica genera le comunicazioni '
         'anagrafiche; dalla 1.46.0 rigenera le notifiche quando cambia il comune AIRE e dalla '
         '1.46.3 tiene conto dell’adesione del comune di competenza; dalla 1.49.0 rigenera le '
         'annotazioni sull’atto principale quando la nota corregge un atto secondario.')

    h(d, 3, 'Le altre correzioni tecniche')
    par(d, 'Gli altri servizi del menù «Altri servizi» intervengono su un atto formato senza '
           'essere rettifiche [A3] [A5]:')
    tabella(d, ALTRE_CORREZIONI, [1.7, 2.6, 1.2, 1.4])
    par(d, 'Per SIPO conta soprattutto la gestione degli allegati errati: cambia i documenti di un '
           'atto che SIPO conserva in `ALLEGATO` [R1], e va riallineata come la nota tecnica.')

    h(d, 3, 'Ciò che le fonti non dicono sulla nota tecnica')
    voce(d, 'La firma.', 'Se l’ufficiale firmi la nota tecnica, e con quale OTP: la guida lo dice '
         'per gli allegati errati e per la correzione di un’annotazione, non per la nota tecnica '
         '(AR-11).')
    voce(d, 'Il tipo 3.', 'ANSC_79 ha NOTATECNICA (2) e NOTATECNICARETTIFICA (3); nessun '
         'documento spiega il secondo (AR-11).')
    voce(d, 'Come lo sa un gestionale.', 'Nessuna notifica e nessuna comunicazione avvisano il '
         'comune che su un atto è stata fatta una nota tecnica; il modello non ha date di ultima '
         'modifica né versioni dell’atto, e la nota stessa non porta data, autore o motivo. '
         'L’unico modo è chiedere a R005, atto per atto (AR-12).')
    voce(d, 'Un servizio cooperativo per farla.', 'Non c’è, e nessun documento ne annuncia uno.')


# =================================================================== capitolo 5
PASSI_SIPO = [
    ['#', 'Passo', 'Dove', 'Indicazione'],
    ['1', '«RETTIFICA TECNICA» nel dettaglio dell’atto', '`statocivile-web`, '
     '`DettaglioAttoStatoCivileController.checkShowButton`', 'Compare al posto di «RETTIFICA '
     'ATTO» quando `ANSC_STATO_ATTO` ha `ID_ANSC` e stato 5. Nessun limite di orario: la regola '
     'della mezzanotte non vale per l’atto formato in ANSC.'],
    ['2', 'Pagina di avvio', '`statocivile-web`, pagina nuova', 'Mostra idAnsc e numero comunale '
     'in evidenza, il caso d’uso, il percorso sulla web app («Altri servizi» → «Correzione '
     'evento tramite nota tecnica») e i vincoli; avverte se SIPO conosce annotazioni '
     'modificative successive, che rendono la nota impossibile. COPIA IDANSC. Registra l’avvio '
     'in `ANSC_LOG_AUDIT`, così la vista di supervisione elenca le rettifiche tecniche avviate e '
     'non riallineate.'],
    ['3', 'Nota tecnica sulla web app', 'Web app ANSC', 'L’ufficiale la compila e la conclude. '
     'SIPO non interviene.'],
    ['4', '«RIALLINEA DA ANSC»', '`statocivile-be` e `all-ansc-sipo`', 'R005 evento per idAnsc '
     '(restituisce l’atto corretto e il suo `id` interno), poi R005 note tecniche con quell’`id`. '
     'Se non risultano note tecniche nuove, nulla cambia.'],
    ['5', 'Confronto', '`statocivile-be`', 'Il modello letto si confronta con quello depositato, '
     'conservato sull’atto in `ANSC_STATO_ATTO.TXT_EVENTO` [R1]: le differenze sono esattamente '
     'ciò che la nota ha cambiato. Ogni percorso cambiato si riporta alla colonna di SIPO con '
     '`ANSC_CFG_CAMPO` (`ALIAS_CAMPO_SIPO`); i percorsi senza colonna (annotazioni contestuali, '
     'allegati, dati che SIPO non ha) si elencano a parte.'],
    ['6', 'Conferma e aggiornamento', '`statocivile-be`', 'L’operatore vede valore SIPO, valore '
     'ANSC e testo della nota, e conferma. I dati di SIPO si aggiornano **senza riaprire '
     'l’atto**: lo stato resta 2 DEFINITO, nessun `FLG_RETTIFICA_INCORSO`. Il modello corretto si '
     'registra in `ANSC_LOG_AUDIT`; `TXT_EVENTO` conserva quello depositato.'],
    ['7', 'Anagrafe', '—', 'Nessuna chiamata ad `all-anpr-sipo`: le comunicazioni anagrafiche le '
     'genera ANSC dalla 1.43.0 (AR-04).'],
]


def capitolo_5():
    h(d, 2, 'La rettifica tecnica: flusso e indicazioni per SIPO')
    par(d, 'La nota tecnica si fa solo sulla web app: SIPO non può formarla. Il suo compito è '
           'portare l’ufficiale alla web app con i dati giusti e, dopo, **riportare in SIPO** ciò '
           'che la nota ha cambiato. È lo stesso schema dell’annullamento in fase 1 e del recupero '
           'degli atti a testo libero [R2].')
    figura(d, os.path.join(IMG, 'rettifica_tecnica_flusso.png'), 6.6,
           'Figura 6 — La rettifica tecnica di un atto firmato e chiuso: il flusso fra SIPO e la '
           'web app.')
    tabella(d, PASSI_SIPO, [0.3, 1.5, 1.7, 3.4])

    h(d, 3, 'Indicazioni')
    voce(d, 'Nota tecnica o annotazione?', 'La guida ammette la nota tecnica anche per gli errori '
         'dell’ufficiale nei metadati, e l’annotazione per errore materiale (art. 98) corregge '
         'anch’essa dati dell’atto. La differenza pratica: la nota tecnica cambia l’atto senza '
         'lasciare un atto nuovo, l’annotazione forma un atto con numero, firma e '
         'certificabilità propri. Il criterio di scelta va fissato dallo stato civile (AR-10).')
    voce(d, 'Il caso tipico per SIPO.', 'Un dato giusto in SIPO e sbagliato in ANSC, per un '
         'difetto di mappatura o di costruzione del modello evento. Si corregge in ANSC con la '
         'nota tecnica e il confronto non trova nulla da riportare in SIPO. Va corretta anche la '
         'configurazione (`ANSC_CFG_CAMPO`), altrimenti l’errore si ripete sull’atto successivo '
         'dello stesso caso d’uso.')
    voce(d, 'Il caso inverso.', 'Un dato sbagliato in entrambi (l’errore è a monte, nella '
         'compilazione): la nota tecnica corregge ANSC e il riallineamento corregge SIPO. È il '
         'solo modo per correggere un atto formato senza riaprirlo.')
    voce(d, 'Nessuna notifica.', 'ANSC non avvisa: se l’ufficiale fa la nota tecnica entrando '
         'direttamente nella web app, SIPO non lo sa. Il riallineamento è un adempimento '
         'dell’ufficio, come la riconciliazione dopo le operazioni fatte sulla web app [R1]; '
         'l’avvio da SIPO (passo 2) serve anche a lasciarne traccia. Un controllo periodico '
         'costerebbe due chiamate R005 per ogni atto (AR-12).')
    voce(d, 'Allegati errati.', 'Stesso schema: avvio da SIPO, correzione sulla web app, rilettura '
         'dei documenti dell’atto e aggiornamento di `ALLEGATO`.')
    voce(d, 'Nessun effetto sulle altre azioni.', 'L’atto resta definito: «ANNULLA ATTO» e '
         '«PROPOSTA ANNOTAZIONE» restano disponibili come prima. Dopo un’annotazione modificativa '
         'la nota tecnica non è più possibile, quindi l’ordine delle operazioni conta.')
    voce(d, 'Il contratto del concentratore.', 'Il riallineamento usa due operazioni di R005 '
         '(evento per idAnsc e note tecniche): vanno esposte da `all-ansc-sipo` in '
         '`ansc-v1.yaml` se non ci sono già. Sono letture: non richiedono la firma.')


# =================================================================== esecuzione
ap_c4 = heading('Ciò che le fonti non dicono', 2)
ap_c5 = heading('Proposta di annotazione', 2)
n4 = innesta(ap_c4._p, capitolo_4)
n5 = innesta(ap_c5._p, capitolo_5)

fatti = []
# figure: la vecchia Figura 4 (cancellazione) diventa 5; le nuove sono 4 e 6
D.sostituisci(d, 'Figura 4 — La cancellazione di una pratica', 'Figura 5 — La cancellazione '
              'di una pratica', attese=1, fatti=fatti)
D.sostituisci(d, 'Le questioni ancora da decidere sono raccolte in coda, come punti aperti '
              'AR-01…AR-09', 'Le questioni ancora da decidere sono raccolte in coda, come punti '
              'aperti AR-01…AR-13', attese=1, fatti=fatti)
D.sostituisci(d, 'Nove questioni, accanto', 'Tredici questioni, accanto', attese=1, fatti=fatti)
D.sostituisci(d, 'Guida operativa — Servizi di ausilio, pp. 8, 16-17.',
              'Guida operativa — Servizi di ausilio, cap. 3 «Altri servizi», §§ 3.1-3.6 '
              '(pp. 5-25 a stampa), in particolare § 3.4 (allegati errati) e § 3.5 (correzione '
              'evento tramite nota tecnica).', attese=1, fatti=fatti)

# il pulsante nascosto ha ora un sostituto
nasc = [p for p in d.paragraphs if p.text.startswith('Nascondere il pulsante.')]
assert len(nasc) == 1
_versa(nasc[0], ' Al suo posto compare «RETTIFICA TECNICA», descritta più avanti.')

# riga della nota tecnica nella tabella della scelta
for t in d.tables:
    for r in t.rows:
        if r.cells[0].text.startswith('Un dato tecnico o un metadato'):
            D.riscrivi_cella(r.cells[3], 'Riallineamento dei dati in SIPO dopo la correzione, '
                             'con il flusso della rettifica tecnica (più avanti).')

# glossario
gl = D.trova_tabella(d, 'termine', 'significato in questo documento')
D.clona_riga(gl, ('Rettifica tecnica', 'La correzione dei dati di un atto formato senza '
                  'provvedimento e senza atto nuovo: in ANSC la nota tecnica e gli altri '
                  'servizi del menù «Altri servizi» della web app, riservati al comune che ha '
                  'formato l’atto.'))

# punti aperti
ap = D.trova_tabella(d, '#', 'questione', 'owner')
for r in ap.rows:
    if r.cells[0].text.strip() == 'AR-06':
        D.riscrivi_cella(r.cells[1], 'Se il confronto del riallineamento dopo una nota tecnica '
                         'debba limitarsi ai campi configurati per il caso d’uso o estendersi '
                         'all’intero modello evento.')
for riga in [
    ('AR-10', 'Criterio di scelta fra nota tecnica e annotazione per errore materiale (art. 98) '
              'per gli errori dell’ufficiale: la guida ammette entrambe. È una regola dello stato '
              'civile.', 'Comune'),
    ('AR-11', 'Firma della nota tecnica (se l’ufficiale firma, e con quale OTP) e significato '
              'del tipo 3 NOTATECNICARETTIFICA di ANSC_79.', 'Analisi / Sogei'),
    ('AR-12', 'Come SIPO viene a sapere di una nota tecnica fatta sulla web app senza passare da '
              'SIPO: ANSC non notifica. Adempimento dell’ufficio, controllo all’apertura del '
              'dettaglio o controllo periodico.', 'Analisi / Comune'),
    ('AR-13', 'Aggiornamento dei dati di SIPO senza riaprire l’atto: quali tabelle, con quale '
              'servizio e con quali permessi; trattamento dei percorsi senza colonna SIPO.',
     'Sviluppo SIPO'),
]:
    D.clona_riga(ap, riga)

for f in D.frontespizio(d, '0.2', NOME):
    print('  ' + f)
D.storia(d, DATA, '0.2', 'Che cosa prevede ANSC · Dove e come inserirsi · Punti aperti',
         'Le rettifiche tecniche di un atto firmato e chiuso: la nota tecnica (finalità, vincoli, '
         'processo sulla web app, dati correggibili, effetti) e gli altri servizi di correzione '
         'della web app, verificati sulla guida dei servizi di ausilio e sul changelog; il flusso '
         'fra SIPO e la web app con il riallineamento dei dati senza riaprire l’atto; AR-10…AR-13.')

assert len(d.inline_shapes) == FIGURE_PRIMA + 2
d.save(OUT)
print('elementi innestati: cap. 4 %d, cap. 5 %d' % (n4, n5))
for f in fatti:
    print('  ' + f)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
