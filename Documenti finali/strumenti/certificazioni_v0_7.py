# -*- coding: utf-8 -*-
"""v0.7 di «ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC» (11/11/2026).

Dal FILE REALE della v0.6 salvata dall'utente (che ha aggiunto «Come intervenire per
permettere la visualizzazione di un atto ANSC», «La risposta dalle API ANSC», «Cosa produce
ANSC»). Richiesta: un capitolo nuovo sulla funzione di SIPO «Certificati ANSC», voce del menu
principale, che cerca un atto in ANSC e poi ne genera il PDF; per ora SOLO LA RICERCA.

Fonti nuove:
  * «Sorgenti Documentali/Ricerca atto per Certificazione.mov» (110 s, web app di
    preproduzione): home con ricerca per soggetto (CF, nome, cognome, data di nascita) e per
    evento (registro, data inizio, data fine, ID Atto), risultati per evento con ricerca
    avanzata Stato/Provincia/Comune e colonne Soggetto, Registro, Tipologia atto, Data, ID Atto,
    Stato, Comune, Azioni (Visualizza atto, Consulta annotazioni, Rilascia certificazioni,
    Consulta nota tecnica); pagina «Rilascia certificazioni» con testata Registro, Tipologia
    atto, Soggetto, ID Atto, Data formazione. Atti di Cedrasco, Venezia, Seregno, Camaiore,
    Lanzada: la ricerca è nazionale;
  * Guida operativa cap. 10 (p. 69-74): «I filtri sono tutti opzionali, ti basta specificarne
    almeno uno»; ID = «numero temporaneo in caso di bozza oppure il numero nazionale in caso di
    evento firmato»; ricerca per soggetto in due passi (soggetti, poi «Visualizza» gli eventi);
  * R005 CriteriRicercaEventoSintetico / CriteriRicercaSoggetto / ModelEventoRidotto;
  * common/commo-web/.../fragments/header.html: le voci della barra sono blocchi <li> scritti
    nel frammento, ciascuno con l'elenco degli identificativi delle aree (Municipi 74-98);
  * D.M. 18/10/2022 Allegato 3 C.4.1 e Allegato 4 (rilascio da parte di tutti gli USC).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/certificazioni_v0_7.py
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import h, par, voce, tabella, figura, _versa   # noqa: E402
import diagrammi_certificazioni as DC   # noqa: E402
import schermate_certificati_ansc as SC   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.6.docx')
NOME = 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.7'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '11/11/2026'

d = docx.Document(SRC)
body = d.element.body
fatti = []


def innesta_prima(prima, scrivi):
    sect = body.find(qn('w:sectPr'))
    visti = set(body.iterchildren())
    scrivi()
    nuovi = [ch for ch in body.iterchildren() if ch not in visti and ch is not sect]
    for ch in nuovi:
        prima.addprevious(ch)


def paragrafo(inizio, stile=None):
    pp = [p for p in d.paragraphs if p.text.startswith(inizio)
          and (stile is None or p.style.name == stile)]
    if len(pp) != 1:
        raise SystemExit('paragrafo non univoco (%d): %s' % (len(pp), inizio))
    return pp[0]


def tab(*intest):
    for t in d.tables:
        if [c.text.strip() for c in t.rows[0].cells][:len(intest)] == list(intest):
            return t
    raise SystemExit('tabella non trovata: %s' % (intest,))


def riga_dopo(t, inizio, valori):
    """Clona la riga che comincia con `inizio`, la mette subito dopo e ne cambia i testi."""
    righe = [r for r in t.rows if r.cells[0].text.startswith(inizio)]
    if len(righe) != 1:
        raise SystemExit('riga non univoca: %s' % inizio)
    tr = copy.deepcopy(righe[0]._tr)
    righe[0]._tr.addnext(tr)
    nuova = [r for r in t.rows if r._tr is tr][0]
    for cella, val in zip(nuova.cells, valori):
        for p in cella.paragraphs[1:]:
            p._p.getparent().remove(p._p)
        p = cella.paragraphs[0]
        if not p.runs:
            p.add_run('')
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)
        p.runs[0].text = val


def coppia(sx, dx, larg=3.1):
    """Le due schermate affiancate, in una tabella senza bordi (come nel cap. del processo)."""
    import certificazioni_v0_3 as V3
    V3.d = d
    return V3.coppia_immagini(sx, dx, larg)


# ===================================================================== il capitolo
def capitolo():
    web = SC.figure_webapp()
    sipo = SC.figure_sipo()
    flusso = DC.ricerca_certificati_ansc()

    h(d, 1, 'Certificati ANSC: la ricerca dell’atto')
    par(d, 'La ricerca dell’ufficio certificati descritta finora parte dalla persona '
           'dell’anagrafe di Roma e arriva all’atto attraverso le tabelle di ANAG_USR. Due casi '
           'le sfuggono: gli atti formati da altri comuni per persone che non sono nell’anagrafe '
           'di Roma, e gli atti di cui SIPO non conosce l’identificativo ANSC. La funzione '
           'proposta in questo capitolo parte invece dall’atto, come la web app ANSC: una voce '
           'nuova del menu principale di SIPO, «Certificati ANSC», cerca l’atto in ANSC e da lì '
           'ne rilascia il certificato.')
    par(d, 'Il capitolo si ferma alla ricerca e alla scelta dell’atto. Il rilascio vero e '
           'proprio (tipo di certificato, richiedente, uso, firma e PDF) sarà descritto a parte, '
           'sulla registrazione della seconda metà del percorso nella web app. Le fonti sono la '
           'registrazione della ricerca nella web app di preproduzione [A13], il capitolo 10 '
           'della guida operativa [A3] e il contratto di R005 [A11].')
    par(d, 'Che un ufficiale di Roma possa certificare un atto formato da un altro comune lo '
           'dice il decreto attuativo [A14]: il servizio cooperativo di rilascio (Allegato 3, '
           'C.4.1) «consente di evadere le richieste avanzate dal cittadino al pari del servizio '
           'B.6.1», cioè della web app, che lo consente «a tutti gli ufficiali dello stato '
           'civile»; e l’Allegato 4 assicura «a tutti gli ufficiali dello stato civile» la '
           'consultazione dell’ANSC ai fini del rilascio allo sportello.')

    # ------------------------------------------------------------ la web app
    h(d, 2, 'Come cerca la web app ANSC')
    par(d, 'La home della web app propone due ricerche alternative, scelte con un selettore, e '
           'accanto due collegamenti: «Recupero evento in bozza» e «Rilascio certificato». Il '
           'secondo porta alla stessa ricerca, perché si certifica a partire da un evento '
           'trovato [A3].')
    coppia(web[0], web[1], 3.1)
    _versa(d.add_paragraph(), 'Figura 9 — La home della web app ANSC: ricerca per soggetto (a sinistra) e per '
           'evento, con l’elenco dei registri aperto (a destra). Il nome dell’operatore è '
           'coperto.', dim=9, corsivo=True)
    voce(d, 'Ricerca per soggetto.', 'Codice fiscale, nome, cognome, data di nascita. La web '
         'app mostra prima l’elenco dei soggetti che rispondono ai criteri e, con «Visualizza», '
         'gli eventi di cui il soggetto è intestatario. Nella pagina dei risultati si raffina '
         'per sesso, identificativo ANPR, identificativo ANSC e provincia di nascita.')
    voce(d, 'Ricerca per evento.', 'Registro (nascita, morte, matrimonio, unione civile, '
         'cittadinanza), data inizio, data fine, ID Atto. «I filtri sono tutti opzionali, ti '
         'basta specificarne almeno uno.» Nella pagina dei risultati si raffina per provincia, '
         'comune di formazione e stato dell’evento.')
    voce(d, 'Risultati.', 'I criteri restano in alto in forma ridotta e si possono modificare. '
         'Per ogni evento: soggetto, registro, tipologia dell’atto, data, ID Atto, stato, comune '
         'e il pulsante «Azioni». Se non c’è nessun risultato compare un messaggio e la ricerca '
         'avanzata non si mostra.')
    voce(d, 'Azioni.', 'Su un evento firmato: «Visualizza atto», «Consulta annotazioni», '
         '«Rilascia certificazioni» e, nel filmato, «Consulta nota tecnica», che la guida non '
         'elenca. Su una bozza del proprio comune: «Modifica e completa» ed «Elimina».')
    figura(d, web[2], 6.3, 'Figura 10 — I risultati di una ricerca per evento (registro '
           'Nascita, dal 01/01/2026 al 20/01/2026) e il menu «Azioni» di un atto firmato.')
    voce(d, 'Rilascia certificazioni.', 'Apre una pagina che ripete in testata registro, '
         'tipologia dell’atto, soggetto, ID Atto e data di formazione, e prosegue con la scelta '
         'del tipo di certificato. Qui finisce la ricerca.')
    figura(d, web[3], 6.3, 'Figura 11 — L’apertura di «Rilascia certificazioni»: la testata '
           'dell’atto scelto, poi il tipo di certificato.')
    par(d, 'Dal filmato si ricavano quattro fatti che servono al disegno:')
    voce(d, 'La ricerca è nazionale.', 'Un operatore di Roma ottiene atti di Cedrasco, Venezia, '
         'Seregno, Camaiore e Lanzada, tutti in stato firmato. È ciò che la guida dichiara: le '
         'bozze e gli atti secretati si vedono solo nel comune di formazione.')
    voce(d, 'Lo stato è abbreviato.', 'La web app scrive «FIRMATO» dove ANSC_11 e R005 scrivono '
         '«FIRMATO DA USC». SIPO mostra la descrizione di ANSC_11 per intero.')
    voce(d, 'L’«ID Atto» non è l’identificativo nazionale nella forma lunga.', 'È un numero di '
         'otto cifre (10232371), mentre l’identificativo che SIPO conserva ha la forma '
         'anno-progressivo nazionale-progressivo comunale-comune. La guida lo chiama «numero '
         'nazionale in caso di evento firmato». Quale criterio di R005 gli corrisponda, idEvento '
         'o una parte di idAnsc, non è scritto (CE-28).')
    voce(d, 'La certificabilità si valuta all’apertura.', 'Aprendo «Rilascia certificazioni» la '
         'pagina mostra per un istante «Questo documento non è certificabile» e poi i tipi di '
         'certificato: la verifica si fa a pagina aperta. SIPO la anticipa sull’elenco, così '
         'l’operatore non apre un atto che non potrà certificare.')

    # ------------------------------------------------------------ la voce di menu
    h(d, 2, 'La voce «Certificati ANSC» nel menu principale')
    par(d, 'Il menu di SIPO è costruito dal frammento di intestazione condiviso `header.html` '
           'di CommonWeb [S5]. Le voci della barra (Generali, Municipi, Dipartimento, Stato '
           'Civile e le altre) sono scritte nel frammento: ciascuna è un blocco che raccoglie le '
           'aree tematiche dell’utente scelte per identificativo (per «Municipi» le aree 1, 7, 9, '
           '10, 11, 13 e 15, `header.html:74-98`). Dentro l’area, le voci sono le funzionalità '
           'dell’utente, ciascuna con il proprio indirizzo di pagina. Una voce di primo livello '
           'richiede quindi un intervento sul dato e uno sul frammento.')
    tabella(d, [
        ['Che cosa', 'Dove', 'Note'],
        ['Un’area tematica nuova, «Certificati di stato civile da ANSC»', 'CONF_AREE_TEMATICHE',
         'Con un identificativo non ancora usato.'],
        ['Due funzionalità: «Ricerca atto e rilascio» e «Certificati rilasciati»',
         'CONF_FUNZIONALITA', 'Con l’indirizzo delle pagine nuove. La seconda voce è il '
         'registro delle emissioni (ANSC_CERTIFICATO) e non è trattata in questo capitolo.'],
        ['Il blocco della voce «Certificati ANSC»', '`header.html` di CommonWeb', 'Elenca '
         'l’identificativo della nuova area. Il frammento è condiviso: la voce compare nei '
         'front-end che usano CommonWeb dopo il loro rilascio.'],
        ['L’abilitazione degli operatori', 'Come per le altre funzionalità', 'La voce si vede '
         'solo se l’utente ha l’area; chi debba averla è una scelta dell’ufficio (CE-29).'],
    ], [2.2, 1.6, 2.7])
    par(d, 'In alternativa la funzione può stare dentro una voce esistente, per esempio '
           '«Stato Civile» o «Municipi», aggiungendo l’identificativo dell’area al loro elenco: '
           'l’intervento sul frammento è lo stesso, ma non si aggiunge una voce alla barra. La '
           'richiesta è per una voce propria, e la figura la mostra così (CE-29).')
    figura(d, sipo[0], 6.3, 'Figura 12 — Ipotesi: la voce «Certificati ANSC» nel menu '
           'principale di SIPO e le sue due funzionalità.')
    par(d, 'Le pagine stanno in CertificatiWeb e il servizio in cert-be: è il modulo che '
           'possiede già il rilascio allo sportello, il registro dei certificati e, dopo '
           'l’innesto descritto prima, le chiamate al concentratore. Una sola parte di SIPO parla '
           'con ANSC per i certificati, da due ingressi. Una pagina nuova in Angular è possibile, '
           'ma porterebbe nel mondo nuovo una funzione che dipende dal registro dei certificati '
           'del mondo vecchio (CE-30).')

    # ------------------------------------------------------------ il percorso
    h(d, 2, 'Il percorso nelle pagine di SIPO')
    par(d, 'Il percorso ricalca quello della web app con due differenze: la ricerca per soggetto '
           'restituisce subito gli eventi, senza l’elenco intermedio dei soggetti, perché R005 '
           'sintetica per soggetto risponde con gli eventi; e la certificabilità si mostra '
           'sull’elenco, non all’apertura del rilascio.')
    figura(d, flusso, 6.5, 'Figura 13 — Certificati ANSC: dalla voce di menu alla pagina di '
           'rilascio.')
    tabella(d, [
        ['Passo', 'Pagina o componente', 'Che cosa succede'],
        ['1', 'Menu', '«Certificati ANSC» → «Ricerca atto e rilascio».'],
        ['2', 'Ricerca atto', 'L’operatore sceglie la ricerca per evento o per soggetto e '
         'compila almeno un criterio.'],
        ['3', 'Concentratore, cercaEventiAnsc', 'Controlla i criteri, compone la richiesta di R005 '
         'sintetica con la testata, l’OTP di sessione e la firma, traccia la chiamata.'],
        ['4', 'Risultati', 'Elenco degli eventi con il giudizio di certificabilità; i filtri '
         'agiscono sull’elenco ricevuto.'],
        ['5', 'Risultati, RILASCIA', 'Si passa soltanto l’identificativo nazionale dell’atto '
         'scelto.'],
        ['6', 'Concentratore, leggiEventoAnsc', 'Rilegge l’atto per identificativo e ripete i '
         'controlli: fra la ricerca e la scelta l’atto può essere stato annullato o annotato.'],
        ['7', 'Rilascio certificazione', 'Si apre con la testata dell’atto appena letto. Il '
         'seguito è il rilascio.'],
    ], [0.6, 1.9, 4.0])

    # ------------------------------------------------------------ la ricerca
    h(d, 2, 'La pagina di ricerca')
    par(d, 'La pagina ha le due ricerche della web app, con lo stesso selettore. In alto lo stato '
           'del codice di sessione ANSC e il pulsante per rinnovarlo, come nelle altre pagine '
           'che chiamano ANSC: senza OTP valido la ricerca non parte. Un avviso ricorda che la '
           'ricerca è nazionale e che bozze e atti secretati di altri comuni non sono visibili.')
    figura(d, sipo[1], 6.3, 'Figura 14 — Ipotesi: la pagina «Certificati ANSC – Ricerca '
           'atto», con la ricerca per evento scelta.')

    h(d, 3, 'Ricerca per evento')
    par(d, 'Si chiama `/consultazione/ansc/evento/sintetico/1` di R005 [A11] con '
           '`criteriRicercaEvento`. Tutti i criteri del contratto sono facoltativi.')
    tabella(d, [
        ['Campo della pagina', 'Criterio di R005', 'Regole'],
        ['Registro', 'idTipoEvento (ANSC_01)', 'Elenco chiuso: 1 nascita, 2 morte, 3 matrimonio, '
         '4 unione civile, 5 cittadinanza.'],
        ['Data dal, Data al', 'dataDa, dataA (AAAA-MM-GG)', 'Data dal non successiva a Data al. '
         'Il contratto non dice a quale data si riferiscano: formazione, evento o registrazione '
         '(CE-31).'],
        ['Identificativo nazionale dell’atto', 'idAnsc', 'Nella forma lunga; da solo basta. '
         'Il numero di otto cifre mostrato dalla web app potrebbe corrispondere a idEvento '
         '(CE-28).'],
        ['Tipo di contenuto (avanzata)', 'idTipoContenuto (ANSC_02)', 'Proposto 1 Atto; anche 3 '
         'Trascrizione. Annotazioni e rifiuti non si certificano come atto.'],
        ['Comune di registrazione (avanzata)', 'idComuneRegistrazione', 'Codice dell’archivio '
         'comuni ANPR: Roma è 8165. Utile con il numero dell’atto.'],
        ['Numero dell’atto (avanzata)', 'idComunale', 'Il numero comunale, quello che il '
         'cittadino legge sui documenti. Il contratto lo dice «codificato ANPR_03», '
         'un’indicazione che non si capisce (CE-31).'],
    ], [1.8, 1.7, 3.0])
    par(d, 'Comune e numero dell’atto non ci sono nella web app: il contratto li offre, e allo '
           'sportello sono spesso l’unica informazione che il cittadino ha. Si propongono fra i '
           'criteri avanzati.')

    h(d, 3, 'Ricerca per soggetto')
    par(d, 'Si chiama `/consultazione/ansc/soggetto/sintetico/1` di R005 con '
           '`criteriRicercaSoggetto`. La risposta è già l’elenco degli eventi di cui la persona è '
           'intestataria.')
    tabella(d, [
        ['Campo della pagina', 'Criterio di R005', 'Note'],
        ['Codice fiscale', 'codiceFiscale', 'Da solo basta, secondo la regola proposta sotto.'],
        ['Cognome, Nome', 'cognome, nome', ''],
        ['Data di nascita', 'datanascita (AAAA-MM-GG)', ''],
        ['Sesso (avanzata)', 'sesso', ''],
        ['Comune o stato di nascita (avanzata)', 'idComuneNascita, oppure nomeComuneNascita e '
         'siglaProvinciaNascita; codiceStatoNascita', 'Codici degli archivi ANPR dei comuni e '
         'degli stati.'],
        ['Identificativo ANPR (avanzata)', 'idAnprUnico, idAnpr', 'Il più preciso: lo '
         'precompila «CERCA IN ANAGRAFE».'],
        ['Identificativo ANSC del soggetto (avanzata)', 'idAnscSoggetto', ''],
    ], [2.0, 2.4, 2.1])
    par(d, 'Regola proposta: il codice fiscale da solo, oppure cognome, nome e data di nascita '
           'insieme. La web app accetta anche meno, ma una ricerca per solo cognome a livello '
           'nazionale restituisce più eventi di quanti l’operatore possa esaminare. Quali '
           'combinazioni accetti R005 non è dichiarato (CE-31).')
    par(d, 'Il pulsante «CERCA IN ANAGRAFE» apre la ricerca anagrafica che SIPO già usa nelle '
           'altre funzioni e, scelta la persona, precompila codice fiscale, dati di nascita e '
           'l’identificativo unico nazionale da ANAG_USR.SOGGETTO.ID_UNICO_NAZIONALE. Serve per '
           'chi è nell’anagrafe di Roma; per gli altri i dati si scrivono a mano.')

    # ------------------------------------------------------------ i risultati
    h(d, 2, 'La pagina dei risultati')
    par(d, 'In alto i criteri in forma ridotta e il pulsante per modificarli; sotto i filtri e '
           'l’elenco degli eventi. Le colonne vengono dal ModelEventoRidotto della risposta [A11].')
    figura(d, sipo[2], 6.3, 'Figura 15 — Ipotesi: la pagina dei risultati, con un atto '
           'annullato che non si può certificare.')
    tabella(d, [
        ['Colonna', 'Campo di ModelEventoRidotto', 'Note'],
        ['Intestatario', 'intestatari[]: cognome, nome', 'Per matrimonio e unione civile due '
         'righe, nell’ordine della risposta.'],
        ['Registro', 'idTipoEvento', 'Descrizione di ANSC_01.'],
        ['Tipo di atto', 'descrizioneCasoUso (idUsecase)', 'Troncato, per intero al passaggio '
         'del mouse.'],
        ['Data formazione', 'dataformazione', ''],
        ['Comune', 'nomeComuneRegistrazione, siglaProvinciaRegistrazione', ''],
        ['Stato ANSC', 'stato', 'Descrizione di ANSC_11 per intero.'],
        ['Azioni', '—', 'VISUALIZZA e RILASCIA.'],
    ], [1.4, 2.6, 2.5])
    par(d, 'Restano nascosti, ma si conservano per il passo successivo: id, idAnsc, '
           'idtipocontenuto, flagsecretato, numeroatto, flagCertificatoSemplice e '
           'flagEstrattoPerRiassunto.')
    voce(d, 'Filtri.', 'Stato, provincia, comune di registrazione e intestatario. R005 non ha '
         'criteri per lo stato e la provincia: i filtri agiscono sull’elenco già ricevuto, '
         'senza nuove chiamate, come la ricerca avanzata della web app. Perché agiscano su tutto '
         'l’elenco e non sulla sola pagina, il concentratore scorre le pagine di R005 fino a un '
         'tetto configurabile (proposta: 200 eventi); oltre il tetto chiede di restringere la '
         'ricerca.')
    voce(d, 'Certificabilità.', 'Per ogni evento gli stessi controlli del passo 4 di «Come '
         'innestare la ricerca ANSC»: tipo di contenuto 1 o 3, stato 5 FIRMATO DA USC, atto non '
         'secretato. Se un controllo non passa, RILASCIA resta spento e il motivo si legge sul '
         'pulsante. Il controllo dei tipi emissibili per i casi d’uso di servizio si fa al '
         'rilascio, perché dipende dal tipo di certificato scelto.')
    voce(d, 'VISUALIZZA.', 'Mostra il riepilogo dei dati ricevuti, senza nuove chiamate. Il '
         'testo dell’atto richiederebbe un altro servizio e un altro permesso (CE-32).')
    tabella(d, [
        ['Risposta', 'Che cosa vede l’operatore'],
        ['Elenco vuoto', '«Nessun atto trovato in ANSC con questi criteri.» I filtri non si '
         'mostrano, come nella web app.'],
        ['Oltre il tetto', '«Troppi risultati: restringere la ricerca.» Con il numero totale '
         'dichiarato da ANSC.'],
        ['400', 'Criteri non accettati da ANSC: il text del messaggio ANSC.'],
        ['401, 403', 'Permesso ANSC dell’operatore insufficiente per la consultazione.'],
        ['406001, 406002', 'OTP non valido o scaduto: rinnovare il codice e ripetere.'],
        ['500', 'Errore di ANSC: la ricerca si può ripetere, perché non ha effetti.'],
    ], [1.5, 5.0])

    # ------------------------------------------------------------ la scelta
    h(d, 2, 'La scelta dell’atto e il passaggio al rilascio')
    par(d, 'RILASCIA porta alla pagina «Rilascio certificazione» con il solo identificativo '
           'nazionale. Il concentratore rilegge l’atto per identificativo con '
           '`leggiEventoAnsc` e ripete i controlli: se l’atto non è più certificabile, '
           'l’operatore torna ai risultati con il motivo. Se lo è, la pagina si apre con la '
           'testata dell’atto letto in quel momento: le stesse informazioni della testata della '
           'web app, più comune, numero e stato.')
    figura(d, sipo[3], 6.3, 'Figura 16 — Ipotesi: l’apertura di «Rilascio certificazione», '
           'dove finisce la ricerca.')
    par(d, 'La ricerca non scrive nulla nelle tabelle di SIPO. Le chiamate ad ANSC si tracciano '
           'come ogni chiamata del concentratore; poiché sono consultazioni di dati personali su '
           'scala nazionale, va deciso se conservare anche chi ha cercato chi (CE-33).')

    # ------------------------------------------------------------ concentratore
    h(d, 2, 'Che cosa serve al concentratore')
    par(d, 'Le due letture proposte in «Le letture di ANSC nel concentratore» bastano, con '
           'un’estensione:')
    tabella(d, [
        ['Operazione', 'Uso nella funzione', 'Che cosa cambia'],
        ['cercaEventiAnsc (POST /ansc/v1/eventi-ansc/ricerche)', 'Passo 3: ricerca per evento e '
         'per soggetto', 'Il corpo porta il tipo di ricerca (evento o soggetto) e i criteri '
         'corrispondenti; la risposta porta l’elenco, il totale e, per ogni evento, l’esito dei '
         'controlli di certificabilità. Oggi è prevista solo per soggetto.'],
        ['leggiEventoAnsc (GET /ansc/v1/eventi-ansc/{idAnsc})', 'Passo 6: rilettura dell’atto '
         'scelto', 'Nulla.'],
    ], [2.4, 1.8, 2.3])
    par(d, 'Per entrambe basta il permesso ANSC di consultazione parziale SCCPA; il rilascio '
           'chiederà SCCSE o il permesso pieno secondo il tipo di certificato.')

    # ------------------------------------------------------------ i due ingressi
    h(d, 2, 'I due ingressi a confronto')
    tabella(d, [
        ['', 'Innesto nell’ufficio certificati', 'Certificati ANSC'],
        ['Da dove parte', 'Dalla persona dell’anagrafe di Roma', 'Dall’atto in ANSC'],
        ['Atti raggiungibili', 'Quelli della persona di cui SIPO conosce l’identificativo, o che '
         'la ricerca per persona trova', 'Tutti gli atti firmati e non secretati in ANSC, di '
         'qualunque comune'],
        ['Ricerca', 'Automatica, all’aggiunta del certificato alla pratica', 'Dell’operatore, '
         'con i criteri della web app'],
        ['Pratica, diritti e bollo', 'Quelli della pratica dell’ufficio certificati',
         'Da decidere (CE-33)'],
        ['Rilascio', 'R002 come in «R002 in dettaglio»', 'Lo stesso: sarà descritto a parte'],
    ], [1.5, 2.5, 2.5])


def riferimenti():
    rif = tab('#', 'Riferimento', 'Natura')
    riga_dopo(rif, '[A12]', ('[A13]', 'Sorgenti Documentali/Ricerca atto per '
                             'Certificazione.mov — registrazione della ricerca di un atto per '
                             'il rilascio nella web app ANSC di preproduzione.',
                             'Registrazione'))
    riga_dopo(rif, '[A13]', ('[A14]', 'D.M. 18 ottobre 2022 (G.U. n. 269 del 17/11/2022), '
                             'Allegato 3 (servizi B.6.1, C.4.1) e Allegato 4 — '
                             'dait.interno.gov.it/documenti/decreto-sd-18-10-2022.pdf.',
                             'Norma'))
    riga_dopo(rif, '[S4]', ('[S5]', 'common/commo-web/CommonWeb, '
                            'templates/fragments/header.html — costruzione del menu principale.',
                            'Sorgente applicativo'))
    a3 = [r for r in rif.rows if r.cells[0].text == '[A3]'][0]
    a3.cells[1].paragraphs[0].runs[-1].text += ' Cap. 10, ricerca per soggetto e per evento.'
    fatti.append('Riferimenti [A13], [A14], [S5]; [A3] esteso al cap. 10')


def punti_aperti():
    ce = tab('#', 'Questione', 'A chi spetta')
    ce2 = [r for r in ce.rows if r.cells[0].text == 'CE-02'][0]
    ce2.cells[1].paragraphs[0].runs[-1].text += (
        ' In parte risolto: il D.M. 18/10/2022 (Allegato 3, C.4.1; Allegato 4) assicura il '
        'rilascio a tutti gli ufficiali dello stato civile e la web app trova atti di altri '
        'comuni [A13]. Resta da provare in preproduzione R002 su un atto di un altro comune.')
    for riga in [
        ('CE-28', 'L’«ID Atto» della web app (otto cifre, «numero nazionale» per la guida): a '
         'quale criterio di R005 corrisponda, idEvento o una parte di idAnsc, e se un operatore '
         'possa cercare con quel numero.', 'Presidio ANSC / Sogei'),
        ('CE-29', 'Collocazione e visibilità della funzione «Certificati ANSC»: voce propria '
         'nella barra o area dentro una voce esistente; quali operatori la vedono.',
         'Ufficio di stato civile / Referenti SIPO'),
        ('CE-30', 'Dove realizzare le pagine: in CertificatiWeb e cert-be, come proposto, o in un '
         'micro-frontend nuovo.', 'Architettura'),
        ('CE-31', 'Ricerche sintetiche di R005: a quale data si riferiscano dataDa e dataA; che '
         'cosa significhi «codificato ANPR_03» per idComunale; quali combinazioni minime di '
         'criteri e quanti risultati ANSC accetti.', 'Presidio ANSC / Sogei'),
        ('CE-32', 'Visualizzazione dell’atto completo dalla funzione: con quale servizio e quale '
         'permesso.', 'Presidio ANSC / Ufficio di stato civile'),
        ('CE-33', 'Pratica, diritti e bollo dei certificati rilasciati dalla funzione nuova, e '
         'conservazione delle consultazioni (chi ha cercato chi).',
         'Ufficio di stato civile / Ragioneria / Privacy'),
    ]:
        D.clona_riga(ce, riga)
    fatti.append('CE-02 aggiornato; CE-28…CE-33')


def che_cosa_cambia():
    t = tab('Dove', 'Che cosa cambia')
    riga_dopo(t, 'CertificatiWeb', ('Menu principale (CommonWeb) e CertificatiWeb',
                                    'Voce «Certificati ANSC» con le pagine di ricerca, risultati '
                                    'e apertura del rilascio (capitolo «Certificati ANSC: la '
                                    'ricerca dell’atto»).'))
    fatti.append('«Che cosa cambia in SIPO»: riga del menu e della funzione nuova')


if __name__ == '__main__':
    innesta_prima(paragrafo('Che cosa cambia in SIPO', 'Heading 1')._p, capitolo)
    fatti.append('capitolo «Certificati ANSC: la ricerca dell’atto», figure 9-16')
    # la lettura per soggetto ora serve anche alla funzione nuova
    ops = tab('Operazione proposta', 'Percorso', 'Servizio ANSC', 'Note')
    c = [r for r in ops.rows if r.cells[0].text == 'cercaEventiAnsc'][0].cells[3]
    c.paragraphs[0].runs[-1].text += (' Usata anche dalla funzione «Certificati ANSC», '
                                      'estesa alla ricerca per evento.')
    fatti.append('nota di cercaEventiAnsc')
    riferimenti()
    punti_aperti()
    che_cosa_cambia()
    for f in D.frontespizio(d, '0.7', NOME, DATA):
        fatti.append(f)
    D.storia(d, DATA, '0.7', 'Certificati ANSC: la ricerca dell’atto · Riferimenti · Punti '
             'aperti', 'Nuovo capitolo sulla funzione «Certificati ANSC» del menu principale: '
             'ricerca nella web app dalla registrazione, voce di menu, percorso, pagine di '
             'ricerca e risultati, passaggio al rilascio, operazioni del concentratore; '
             'CE-02 aggiornato, CE-28…CE-33.')
    d.save(OUT)
    for f in fatti:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tb, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tb, fig))
