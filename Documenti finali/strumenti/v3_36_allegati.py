# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.35 → v3.36 (10/10/2026).

La gestione dei documenti allegati: SI ADOTTA il processo del sistema Side del Comune di
Milano — logica, filosofia e tabelle — lasciando spazio ai soli aggiustamenti adattivi, che
si dichiarano uno per uno (indicazione del committente, 10/10/2026). Si mostra anche come le
interfacce di Side si riusano sulla libreria condivisa del front-end di Roma.

Sorgenti [R12]: «Processo di gestione degli allegati di un atto» v1.5 (2023), «Processo di
gestione e firma dell'attestato di conformità» v1.1 (2025), le schermate di Side del
24/09/2026 in SIDE/Grafica/. Riscontri fatti sul corpus ANSC prima di scrivere:
  * ANSC_08 = 5 stati, e il 5 oggi è «In elaborazione» (la doc. Side del 2023 lo chiama
    «Altro» e si chiede che cosa significhi);
  * ANSC_09 = 128 valori, fra cui 998 «Allegato generico» (la descrizione libera di Side) e
    999 «Processo verbale»;
  * ANSC_10 = PDF, JPG, TIF, P7M — gli stessi delle schermate del 2026 (la doc. del 2023
    diceva pdf/tiff/jpg e 5 MB; le schermate dicono 10 MB: valgono le schermate, più recenti);
  * ⚠️ ANSC_78 = TRE valori: il quarto («presenza figlio»), su cui Side costruisce C004, non
    c'è più nel dizionario pubblicato;
  * R001 = tre operazioni (upload, dettaglio con contenuto, verifica leggera): NESSUNA
    cancellazione. Side cancella solo in locale → OP-70;
  * flagAttConformita è boolean in R007/R010 e flagInclusoAttConformita è string nel modello
    evento: la trappola che la doc. Side segnala è confermata dai contratti.

Conseguenze sul modello dati, in linea con l'adozione:
  * ALLEGATI_USECASE perde fg_incluso_att_conformita: l'avevamo aggiunta noi, in Side la
    scelta è dell'ufficiale atto per atto (prima volta: tutti selezionati) e sta su ALLEGATO;
  * ty_presenza e ty_configurazione hanno ora i valori di Side → OP-61 chiuso;
  * ALLEGATO.cd_stato accoglie lo «0» locale di Side.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/immagini_side.py
    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_36_allegati.py
"""
import os
import shutil
import subprocess
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.35.docx')
DST = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.36.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

TITOLO_VECCHIO = 'Punto di attenzione: i documenti e la loro firma'
TITOLO = 'La gestione dei documenti: il processo di Side adottato in SIPO'


def commenti(p):
    return int(subprocess.run(
        ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                       "grep -o '<w:comment ' | wc -l" % repr(p)],
        capture_output=True, text=True).stdout.strip() or 0)


# ───────────────────────────────────────────── tabelle della sezione nuova
ADATTAMENTI = [
    ('Elemento', 'In Side', 'In SIPO', 'Perché'),
    ('Collocazione di ALLEGATO', 'Schema atti, accanto all’evento.',
     'MATR_USR, accanto all’atto; la chiave è id_atto_sipo invece di id_evento.',
     'SIPO non ha la tabella degli eventi di Side: l’aggancio naturale è l’atto (OP-68).'),
    ('Baseline della configurazione', 'Assente.',
     'id_versione in chiave di ALLEGATI_USECASE.',
     'Il mapping di ANSC cambia una ventina di volte l’anno: due revisioni devono poter '
     'coesistere.'),
    ('Chiave di importazione', 'Assente.', 'ds_allegato su ALLEGATI_USECASE.',
     'La configurazione di Roma si prepara dal mapping ufficiale, che nomina gli allegati per '
     'descrizione.'),
    ('Presenza condizionata', 'Codice C001…C004, con la condizione implicita nel codice '
     '(tipo di accertamento uguale al numero).',
     'Stesso codice; la condizione è scritta nel catalogo delle logiche e richiamata da '
     'cd_logica.',
     'Il caso documentato da Side è uno solo; alla scala dei 374 UC una condizione implicita '
     'nel codice non è verificabile.'),
    ('Stato locale «0»', '«Caricato su SIDe».', '«Caricato in SIPO».',
     'Solo la dicitura.'),
    ('Atti a testo libero', 'Tipo 998 «Allegato generico» con descrizione libera.',
     'Il contrassegno fg_testo_libero, aggiunto nella v3.29.',
     'Da riconciliare: potrebbe essere ridondante con il tipo 998 (OP-71).'),
    ('Cornice grafica', 'Testata e piè di pagina del Comune di Milano.',
     'Cornice istituzionale di Roma, dalla libreria condivisa.',
     'È l’unico intervento grafico: il resto si riusa.'),
]

STATI = [
    ('Stato', 'Significato', 'Anteprima', 'Azioni ammesse'),
    ('0 — Caricato in SIPO', 'Il file è nel database del Comune e non è ancora stato '
     'trasmesso. Stato locale, aggiunto da Side alla decodifica ANSC_08.',
     'Dal database locale.', 'Invia · Cancella'),
    ('1 — Ricevuto', 'ANSC ha accettato il file e lo deve ancora verificare.',
     'Dal database locale.', 'Verifica · Cancella'),
    ('2 — In corso di verifica', 'La scansione antivirus è in corso.',
     'Dal database locale.', 'Verifica · Cancella'),
    ('3 — Inserito', 'Verificato e acquisito: è l’unico stato che consente di proseguire '
     'verso il deposito.', 'Da ANSC (R001, dettaglio con contenuto).', 'Cancella'),
    ('4 — Rifiutato', 'ANSC non lo accetta: va sostituito.', 'Dal database locale.',
     'Cancella e ricarica'),
    ('5 — In elaborazione', 'Così lo dichiara oggi la decodifica ANSC_08. La documentazione '
     'di Side del 2023 lo chiama «Altro» e si chiede che cosa significhi.',
     'Da ANSC (R001, dettaglio con contenuto).', 'Cancella'),
]

RIUSO = [
    ('Elemento di Side', 'Che cosa fa', 'Componenti della libreria condivisa [R13]',
     'Adattamento per SIPO'),
    ('Sezione «Allegati» della maschera di stesura',
     'Ultima sezione della maschera, con l’esito di completezza accanto al titolo (spunta o '
     'croce).', 'accordion · badge',
     'Stessa posizione nella maschera di SIPO. Il titolo è «Allegati», non «Documenti»: '
     'indicazione esplicita di Side.'),
    ('Riga a descrizione fissa (BASE)',
     'Descrizione del tipo, asterisco se obbligatorio, scelta del file, cestino, «Visualizza '
     'documento», stato.', 'document-single-upload · button-icon · pdf-viewer · badge',
     'Nessuno.'),
    ('Righe a descrizione libera (D.LIB.M.01)',
     'Descrizione obbligatoria scritta dall’operatore, «+» per aggiungere una riga, '
     '«Rimuovi allegato» per toglierla.', 'input · document-single-upload · button-icon',
     'Nessuno.'),
    ('Bottoni INVIA e VERIFICA',
     'Mai presenti insieme: INVIA se c’è almeno un file nello stato 0; VERIFICA se ce n’è '
     'almeno uno negli stati 1 o 2 e nessuno nello stato 0.', 'button', 'Nessuno.'),
    ('Messaggi',
     'Formati e dimensione ammessi; «Nome file non ammesso. I nomi devono essere distinti.»; '
     '«Per proseguire è necessario allegare un file».', 'notification-toast · elementi di '
     'modulo con messaggio di errore', 'Testi riusati.'),
    ('Pagina dell’attestazione di conformità',
     'Elenco dei documenti con casella, GENERA, anteprima, credenziali di firma, FIRMA, '
     'CONTINUA, ELIMINA EVENTO.', 'checkbox · button · pdf-viewer · input · input-password '
     '· otp',
     'Le credenziali seguono il percorso di firma già descritto. Il codice di sessione è il '
     'bottone OTP della shell; REGISTRO DI EMERGENZA corrisponde alla modalità di emergenza '
     'di questo documento.'),
    ('Testata e piè di pagina', 'Cornice del Comune di Milano.', 'header · footer',
     'Sostituiti dalla cornice istituzionale di Roma.'),
]

FIG_BASE = ('Figura — Side, sezione «Allegati» di un atto di matrimonio nella configurazione '
            'a descrizione fissa: un tipo di documento per riga, con il «+» per caricarlo. '
            'Schermata dell’ambiente di sviluppo di Milano, 24/09/2026 [R12]; il nome '
            'dell’operatore è stato coperto.')
FIG_LIBERA = ('Figura — Side, sezione «Allegati» di un’annotazione nella configurazione a '
              'descrizione libera: due documenti nello stato «Caricato in SIDE», con il '
              'bottone INVIA che li trasmette ad ANSC. Ambiente di sviluppo di Milano, '
              '24/09/2026 [R12].')
FIG_ATTESTATO = ('Figura — Side, attestazione di conformità: l’ufficiale ha scelto i '
                 'documenti da attestare, l’attestato è stato generato e la firma è '
                 'abilitata. Da «Processo di gestione e firma dell’attestato di conformità» '
                 'v1.1 [R12]; il nome dell’operatore è stato coperto.')

# (tipo, contenuto): 'p' paragrafo · 'h3' sottotitolo · 'v' voce (testa, corpo) ·
# 'tab' (righe, larghezze) · 'img' (png, pollici, didascalia)
BLOCCHI = [
    ('p', 'La gestione dei documenti è la parte del disegno con il maggiore scarto fra ciò '
          'che la configurazione sa e ciò che SIPO sa fare: la configurazione dichiara per '
          'ciascun UC quali documenti servono, ma l’area di stato civile di SIPO non gestisce '
          'alcun documento allegato. La funzione manca; non per questo va progettata. Il '
          'sistema Side del Comune di Milano la realizza verso ANSC con tabelle, regole e '
          'maschere documentate dal 2023 [R12], e le schermate del settembre 2026 ne mostrano '
          'la realizzazione attuale.'),
    ('p', '⚠️ La scelta di questo documento è di adottarla — logica, filosofia e tabelle — '
          'lasciando spazio soltanto agli aggiustamenti che il contesto di Roma rende '
          'necessari, e di dichiararli uno per uno. Ciò che segue descrive il processo di '
          'Side come si applica a SIPO; dove SIPO se ne discosta, la tabella seguente dice '
          'dove e perché. Ciò che non vi compare si adotta così com’è.'),
    ('tab', (ADATTAMENTI, [1.3, 1.5, 1.7, 1.9])),
    ('p', ''),

    ('h3', 'Le strutture: due tabelle e tre decodifiche'),
    ('p', 'Le tabelle sono due, con compiti distinti. ALLEGATI_USECASE dice quali documenti '
          'un UC richiede, ed è configurazione; ALLEGATO registra i documenti di un atto, ed è '
          'dato operativo. Entrambe sono descritte con le loro colonne nei capitoli del '
          'modello dati e della costruzione del payload. Le decodifiche sono quelle di ANSC: '
          'ANSC_08 per lo stato del documento, ANSC_09 per il tipo — 128 valori, fra cui 998 '
          '«Allegato generico», che Side usa per i documenti a descrizione libera, e 999 '
          '«Processo verbale» — e ANSC_10 per il formato del file: PDF, JPG, TIF e P7M.'),

    ('h3', 'Quali documenti chiedere: la presenza e le due forme dell’elenco'),
    ('p', 'Determinato l’UC, l’elenco dei documenti si legge da ALLEGATI_USECASE nell’ordine '
          'di nr_ordinamento. Per ciascuno ty_presenza dice se è obbligatorio (O), facoltativo '
          '(F) o condizionato (C001…C004). L’obbligatorietà si mostra con un asterisco, come '
          'nella web app di ANSC.'),
    ('p', 'Il caso condizionato documentato da Side è uno solo, la nascita: C001…C004 rendono '
          'obbligatorio il documento il cui tipo coincide con il tipo di accertamento '
          'registrato sui dati di nascita — attestazione di nascita, constatazione di '
          'avvenuto parto, dichiarazione sostitutiva — e lasciano facoltativi gli altri. '
          '⚠️ Il quarto valore, «presenza figlio», su cui Side costruisce C004, non compare più '
          'nella decodifica ANSC_78 pubblicata, che ne conta tre: la riga che lo usa non ha '
          'oggi un valore che la attivi.'),
    ('p', 'ty_configurazione sceglie la forma della riga nella maschera:'),
    ('v', ('BASE — descrizione fissa. ', 'Un documento per tipo, con la descrizione presa da '
           'ANSC_09. È la forma ordinaria.')),
    ('v', ('D.LIB.M.01 — descrizione libera con molteplicità. ', 'L’operatore scrive la '
           'descrizione, che è obbligatoria, e può aggiungere altre righe dello stesso tipo. '
           'Il documento è trasmesso con il tipo 998 e la descrizione è conservata in '
           'ALLEGATO.ds_tipo_allegato.')),
    ('img', ('side_allegati_base.png', 5.6, FIG_BASE)),
    ('img', ('side_allegati_libera.png', 6.2, FIG_LIBERA)),
    ('p', 'I vincoli sul file sono controllati in locale, prima di ogni trasmissione. Le '
          'schermate attuali di Side dichiarano dieci megabyte al massimo, nome del file senza '
          'spazi né caratteri speciali e i quattro formati di ANSC_10; la documentazione del '
          '2023 indicava cinque megabyte e tre formati, ed è superata. Due file con lo stesso '
          'nome non sono ammessi nello stesso atto.'),

    ('h3', 'Il ciclo di vita del documento'),
    ('p', 'Il documento attraversa sei stati: lo stato locale 0, che Side aggiunge alla '
          'decodifica, e i cinque di ANSC_08. Lo stato decide quali azioni la maschera offre e '
          'da dove si legge l’anteprima.'),
    ('tab', (STATI, [1.5, 2.6, 1.6, 1.3])),
    ('p', ''),
    ('p', 'Le azioni sono quattro, e ciascuna corrisponde a un’operazione del servizio R001 '
          'oppure a un’operazione soltanto locale.'),
    ('v', ('Caricamento. ', 'L’operatore sceglie il file: è salvato in ALLEGATO con lo stato '
           '0. Nessuna chiamata ad ANSC.')),
    ('v', ('Invia. ', 'Trasmette tutti i documenti nello stato 0 con /allegato/upload. Dalla '
           'risposta si conservano l’identificativo assegnato da ANSC (id_ansc_allegato), lo '
           'stato e l’impronta (cd_hash). ⚠️ L’impronta la restituisce ANSC: il contratto ne '
           'lascia indefinito l’algoritmo («definire l’algoritmo, per es. SHA1»).')),
    ('v', ('Verifica. ', 'Rilegge con /allegato/verifica — un servizio leggero, che '
           'restituisce il solo stato — i documenti negli stati 1 e 2, e aggiorna cd_stato. '
           'Sugli stati 3, 4 e 5 non fa nulla. È il modo in cui la maschera accompagna la '
           'scansione antivirus invece di sembrare bloccata.')),
    ('v', ('Anteprima e cancellazione. ', 'L’anteprima si legge dal database locale, salvo '
           'negli stati 3 e 5, in cui si chiede ad ANSC con /allegato, che restituisce il '
           'contenuto. La cancellazione elimina la riga locale in qualunque stato e consente '
           'di caricare un altro file.')),
    ('p', '⚠️ Su quest’ultimo punto il processo di Side lascia una domanda aperta. R001 non '
          'ha un’operazione di cancellazione: un documento già trasmesso e poi cancellato in '
          'locale resta in ANSC. Che cosa ne sia — se resti orfano o se sia ignorato perché '
          'non richiamato nel modello evento depositato — non è detto né dalla documentazione '
          'di Side né dal contratto (OP-70).'),

    ('h3', 'L’attestazione di conformità'),
    ('p', 'Dal rilascio 1.40 di ANSC l’ufficiale sceglie quali documenti attestare. Side ne '
          'ha fatto una pagina propria del percorso di firma, che si adotta così com’è. Si '
          'presenta dopo la firma dei dichiaranti, se l’atto ne ha, oppure subito dopo la '
          'validazione; se l’atto non ha documenti si passa direttamente alla firma finale '
          'dell’ufficiale.'),
    ('v', ('Scelta. ', 'La pagina elenca tutti i documenti dell’atto, compreso il processo '
           'verbale delle firme dei dichiaranti. Al primo accesso sono tutti selezionati; agli '
           'accessi successivi ripropone la scelta salvata.')),
    ('v', ('Generazione. ', 'GENERA ATTESTATO DI CONFORMITÀ è abilitato finché almeno un '
           'documento è selezionato. Chiama R010 (/anteprima/attestazione) con l’elenco dei '
           'documenti e il contrassegno di ciascuno, mostra l’anteprima e salva la scelta in '
           'ALLEGATO — fg_incluso_att_conformita e fg_attestazione. Se la selezione cambia, '
           'l’anteprima scompare e va rigenerata.')),
    ('v', ('Firma. ', 'FIRMA è abilitato solo con l’anteprima visibile e chiama R007 '
           '(/attestazione/firma) con lo stesso elenco. Se nessun documento è selezionato, '
           'GENERA si disabilita e CONTINUA porta direttamente alla firma finale, salvando '
           'anch’esso la scelta.')),
    ('img', ('side_attestato.png', 6.2, FIG_ATTESTATO)),
    ('p', 'Due avvertenze tecniche, che la documentazione di Side segnala e i contratti '
          'confermano. Il contrassegno è boolean nei servizi R007 e R010 '
          '(flagAttConformita) e stringa nel modello evento (flagInclusoAttConformita): la '
          'stessa informazione viaggia in due tipi. E il campo flagAttestazione del modello '
          'evento, secondo una risposta di Sogei nel repository pubblico di ANSC citata da '
          'Side (discussione 787), si può ignorare.'),
    ('p', '⚠️ Ne discende una correzione del modello dati. Le versioni precedenti di questo '
          'documento avevano aggiunto ad ALLEGATI_USECASE un contrassegno per decidere, per '
          'UC, quali documenti includere nell’attestazione. In Side la scelta non è di '
          'configurazione: è dell’ufficiale, atto per atto, a partire da tutti selezionati, e '
          'si registra su ALLEGATO. La colonna è tolta e la parte corrispondente di OP-50 è '
          'chiusa.'),

    ('h3', 'Il riuso delle interfacce'),
    ('p', 'Le maschere di Side si riusano come disegno: struttura, stati, regole di '
          'abilitazione dei bottoni e testi dei messaggi passano a SIPO invariati. Ciascun '
          'elemento ha un corrispondente fra i componenti della libreria condivisa del '
          'front-end di Roma [R13], che offre già il caricamento di file e il visualizzatore '
          'di PDF. L’unico intervento grafico è la cornice: testata e piè di pagina diventano '
          'quelli istituzionali di Roma.'),
    ('tab', (RIUSO, [1.4, 2.1, 1.6, 1.9])),
    ('p', ''),
    ('p', '⚠️ Il riuso qui descritto è di disegno, non di codice. Il codice delle maschere di '
          'Side non è fra le sorgenti, e non è noto se sia stato realizzato con la stessa '
          'tecnologia del front-end di Roma: se lo fosse, e fosse reso disponibile, il riuso '
          'potrebbe estendersi ai componenti (OP-72). L’estensione non cambierebbe nulla di '
          'quanto descritto qui.'),

    ('h3', 'Che cosa resta da decidere'),
    ('v', ('La conservazione. ', 'ALLEGATO conserva il file nella colonna oj_allegato, cioè '
           'nel database, come in Side, e lo si adotta così. Resta la raccomandazione di '
           'valutare un archivio a oggetti quando i volumi usciranno da quelli del pilota '
           '(OP-57): la differenza è una colonna.')),
    ('v', ('La verifica della firma dei documenti. ', 'Side non verifica le firme digitali '
           'dei documenti caricati, e la documentazione non ne parla. Se il Comune decide che '
           'vadano verificate, serve un servizio che lo faccia e una regola per il caso in cui '
           'la verifica non riesca (OP-58). Va tenuta distinta dalle firme dell’atto — del '
           'dichiarante e dell’ufficiale — che ANSC governa con R006 e R007.')),
    ('v', ('Il perimetro. ', 'Se la gestione documentale nasca dentro l’integrazione ANSC — e '
           'allora serve soltanto per gli atti che si depositano — oppure sia una funzione '
           'dell’area di stato civile, e allora vale anche per gli atti che in ANSC non vanno, '
           'con conseguenze su conservazione, ricerca e cancellazione. La seconda è la scelta '
           'più costosa e la sola che non vada rifatta.')),
    ('v', ('La cancellazione dopo l’invio. ', 'Vedi sopra e OP-70.')),
]

NUOVI_OP = [
    ('OP-70', 'Cancellazione di un documento già trasmesso ad ANSC',
     'Side consente di cancellare un documento in qualunque stato, ma la cancellazione è '
     'soltanto locale e il servizio R001 non ha un’operazione per eliminarlo in ANSC. Va '
     'accertato che cosa accada al documento trasmesso e poi cancellato: se resti in ANSC '
     'senza riferimenti o se sia ignorato perché assente dal modello evento depositato. Da '
     'chiedere al Comune di Milano e, se serve, a Sogei.',
     'Aperto', 'Analisi / Comune di Milano', 'Media'),
    ('OP-71', 'Atti a testo libero e tipo «Allegato generico»',
     'Il contrassegno ALLEGATO.fg_testo_libero, aggiunto nella v3.29, distingue gli atti a '
     'testo libero dai documenti che l’UC prevede. Side ottiene un effetto vicino con il tipo '
     '998 e la configurazione a descrizione libera. Va deciso se il contrassegno resti — e '
     'allora va motivato che cosa aggiunga al tipo 998 — oppure si tolga per allinearsi a '
     'Side.', 'Aperto', 'Analisi / Cliente', 'Bassa'),
    ('OP-72', 'Disponibilità del codice delle maschere di Side',
     'Il riuso delle interfacce di Side è descritto come riuso di disegno. Se il Comune di '
     'Milano rendesse disponibile il codice delle maschere degli allegati e dell’attestazione '
     'di conformità, e la tecnologia fosse compatibile con il front-end di Roma, il riuso '
     'potrebbe estendersi ai componenti. Da chiedere.', 'Aperto', 'Cliente / Comune di Milano',
     'Bassa'),
]

R13 = ('R13', 'ANALISI_Front-End-Angular_v0.6.docx',
       'Impostazione del front-end Angular sulla libreria condivisa: catalogo dei componenti '
       '(caricamento di file, visualizzatore di PDF, elementi di modulo) su cui si mappano le '
       'interfacce riusate da Side.')

STORIA = (
    '10/10/2026', '3.36',
    'Costruzione del payload (sezione sui documenti riscritta) · Il processo di formazione '
    '(passi 5-6) · Modello dati (ALLEGATO, ALLEGATI_USECASE) · Appendice A · Riferimenti · '
    'Open Point',
    'La gestione dei documenti adotta il processo del sistema Side del Comune di Milano — '
    'logica, tabelle e maschere — con i soli aggiustamenti adattivi, elencati in una tabella '
    'con la loro ragione. La sezione «Punto di attenzione: i documenti e la loro firma» '
    'diventa «La gestione dei documenti: il processo di Side adottato in SIPO» e descrive '
    'presenza e forme dell’elenco, i sei stati del documento con le azioni ammesse, le '
    'operazioni di R001, l’attestazione di conformità e il riuso delle interfacce sui '
    'componenti della libreria condivisa, con tre schermate di Side. Chiuso OP-61 con i '
    'valori di ty_presenza e ty_configurazione. Tolto da ALLEGATI_USECASE il contrassegno '
    'dell’attestazione di conformità: in Side la scelta è dell’ufficiale atto per atto; '
    'chiusa la parte corrispondente di OP-50. Rilevato che il quarto valore di ANSC_78, su '
    'cui Side costruisce C004, non è più pubblicato. Allineato il passo 6, che collocava i '
    'documenti in un archivio a oggetti. Nuovi OP-70, OP-71, OP-72 e [R13].')


def main():
    if os.path.exists(DST):
        raise SystemExit(f'{os.path.basename(DST)} esiste già: non si sovrascrive')
    shutil.copy(SRC, DST)
    prima = commenti(DST)
    d = docx.Document(DST)
    fatti = []

    # ─────────────────────────────── 1. la sezione riscritta
    elementi = D.sezione(d, TITOLO_VECCHIO, 2)
    if not elementi:
        raise SystemExit('sezione non trovata')
    for el in elementi:
        if D.ha_commenti(el):
            raise SystemExit('la sezione da riscrivere porta un commento')
    testa = elementi[0]
    D.testo_di(Paragraph(testa, d), TITOLO)
    dopo = elementi[-1].getnext()
    for el in elementi[1:]:
        el.getparent().remove(el)
    modello = D.trova_tabella(d, 'Oggetto', 'Ruolo')
    for tipo, c in BLOCCHI:
        if tipo == 'p':
            D.para(d, dopo, c)
        elif tipo == 'h3':
            D.para(d, dopo, c, stile='Heading 3')
        elif tipo == 'v':
            D.voce(d, dopo, *c)
        elif tipo == 'tab':
            D.tabella(d, dopo, c[0], modello, c[1])
        elif tipo == 'img':
            D.immagine(d, dopo, os.path.join(IMG, c[0]), c[1], c[2])
    fatti.append(f'sezione «{TITOLO}» ({len(BLOCCHI)} blocchi, 3 tabelle, 3 figure)')

    # ─────────────────────────────── 2. passi 5-6 e funzioni mancanti
    D.sostituisci(
        d, 'I documenti caricati prima della chiusura dell’atto, sono conservati in un '
           'archivio del Comune — un archivio a oggetti o altra soluzione già nella '
           'disponibilità dell’amministrazione — e non nella base dati ANSC dell’atto. La '
           'scelta tiene separati i documenti dai dati e consente di governarne diversamente '
           'conservazione e accesso.',
        'I documenti caricati prima della chiusura dell’atto sono conservati nella tabella '
        'ALLEGATO, accanto all’atto, nello stato «Caricato in SIPO» che dice che non sono '
        'ancora stati trasmessi: è la soluzione del sistema Side, da cui la gestione dei '
        'documenti è adottata. Resta la raccomandazione di valutare un archivio a oggetti '
        'quando i volumi usciranno da quelli del pilota (OP-57).',
        attese=1, fatti=fatti, etichetta='passo 6: conservazione come in Side')
    D.sostituisci(
        d, 'Le maschere di caricamento sono quindi da realizzare, e con esse l’archivio e il '
           'raccordo con ANSC.',
        'Le maschere di caricamento sono quindi da realizzare in SIPO, ma non da progettare: '
        'si adotta il processo di Side, descritto nel paragrafo «La gestione dei documenti: il '
        'processo di Side adottato in SIPO».',
        attese=1, fatti=fatti, etichetta='passo 6: da realizzare, non da progettare')
    D.sostituisci(
        d, 'Vanno realizzate le maschere, l’archivio e l’attesa della scansione.',
        'Vanno realizzate le maschere, la conservazione e l’attesa della scansione, adottando '
        'il processo e le interfacce di Side.',
        attese=1, fatti=fatti, etichetta='funzioni mancanti: adozione da Side')

    # ─────────────────────────────── 3. ALLEGATI_USECASE: tabella delle colonne
    t = next(t for t in d.tables if t.rows[0].cells[0].text.strip() == 'Colonna'
             and any(r.cells[0].text.strip() == 'ds_allegato' for r in t.rows))
    # ⚠️ non 'ty_allegato': ce l'ha anche ALLEGATO, che viene prima nel documento
    righe = {r.cells[0].text.strip(): r for r in t.rows}
    D.riscrivi_cella(righe['ty_presenza'].cells[2],
                     'Presenza del documento, con i valori di Side: O obbligatorio, F '
                     'facoltativo, C001…C004 condizionato. Nel caso documentato da Side la '
                     'condizione è il tipo di accertamento dei dati di nascita uguale al numero '
                     'del codice; qui la condizione si scrive nel catalogo delle logiche e si '
                     'richiama da cd_logica, e il codice resta quello di Side.')
    D.riscrivi_cella(righe['ty_configurazione'].cells[2],
                     'Forma della riga nella maschera, con i valori di Side: BASE, a '
                     'descrizione fissa presa da ANSC_09; D.LIB.M.01, a descrizione libera '
                     'obbligatoria e con più righe dello stesso tipo, trasmessa con il tipo 998.')
    D.riscrivi_cella(righe['id_dominio / cd_logica'].cells[2],
                     'La condizione che rende obbligatorio un documento quando ty_presenza vale '
                     'C…, presa dal catalogo delle logiche. Adattamento rispetto a Side, dove la '
                     'condizione è implicita nel codice: è la stessa grammatica delle altre '
                     'condizioni e la valuta lo stesso motore.')
    r = righe['fg_incluso_att_conformita']
    if D.ha_commenti(r._tr):
        raise SystemExit('la riga fg_incluso_att_conformita porta un commento')
    r._tr.getparent().remove(r._tr)
    fatti.append('ALLEGATI_USECASE: valori di ty_presenza e ty_configurazione; tolta '
                 'fg_incluso_att_conformita')

    # la sorgente di Side in due stesure: va detto quale vale
    p320 = next(p for p in d.paragraphs
                if p.text.startswith('Il legame con l’UC va letto con precisione'))
    D.para(d, p320._p,
           'La struttura di origine è nota in due stesure che non coincidono: lo schema '
           'riprodotto nella documentazione di Side del 2023 porta ty_presenza di un solo '
           'carattere e un contrassegno fg_in_validita; la definizione ricevuta porta '
           'ty_presenza di dieci caratteri — quanti ne servono a C001 — e fg_operante. Vale la '
           'definizione, che è la più recente.')

    # ─────────────────────────────── 4. ALLEGATO: note delle colonne
    t = next(t for t in d.tables if t.rows[0].cells[0].text.strip() == 'Colonna'
             and any(r.cells[0].text.strip() == 'oj_allegato' for r in t.rows))
    righe = {r.cells[0].text.strip(): r for r in t.rows}
    D.riscrivi_cella(righe['ds_tipo_allegato'].cells[2],
                     'Descrizione del tipo. Per i documenti a descrizione libera (tipo 998) è '
                     'quella scritta dall’operatore, ed è obbligatoria.')
    D.riscrivi_cella(righe['fg_testo_libero'].cells[2],
                     '⚠️ Aggiunta, non presente in Side: 0/1 secondo che il documento sia fra '
                     'quelli che l’UC prevede oppure sia un atto a testo libero, redatto '
                     'dall’ufficiale e allegato. I secondi sono ammessi ma non verificabili dal '
                     'pre-filtro. Side ottiene un effetto vicino con il tipo 998: se il '
                     'contrassegno vada mantenuto è OP-71.')
    D.riscrivi_cella(righe['cd_hash'].cells[2],
                     'Impronta del file restituita da ANSC alla trasmissione, come in Side. Il '
                     'contratto ne lascia indefinito l’algoritmo.')
    D.riscrivi_cella(righe['cd_stato'].cells[2],
                     'Stato del documento: 0 «Caricato in SIPO», locale e aggiunto da Side, '
                     'più i cinque di ANSC_08 (Ricevuto, In corso di verifica, Inserito, '
                     'Rifiutato, In elaborazione). Solo «Inserito» consente di proseguire: è '
                     'l’esito della scansione antivirus, che non dipende da noi.')
    D.riscrivi_cella(righe['fg_attestazione'].cells[2],
                     '0/1. Side lo salva insieme al contrassegno seguente quando l’ufficiale '
                     'genera l’attestato; corrisponde a flagAttestazione del modello evento, che '
                     'secondo Sogei si può ignorare.')
    D.riscrivi_cella(righe['fg_incluso_att_conformita'].cells[2],
                     '0/1: se l’ufficiale ha incluso il documento nell’attestazione di '
                     'conformità. È una scelta atto per atto, salvata dai bottoni GENERA e '
                     'CONTINUA; al primo accesso alla pagina tutti i documenti sono proposti '
                     'come inclusi.')
    fatti.append('ALLEGATO: note di ds_tipo_allegato, fg_testo_libero, cd_hash, cd_stato e dei '
                 'due contrassegni')

    # ─────────────────────────────── 5. Appendice A
    ps = d.paragraphs

    def unico(testo):
        trovati = [p for p in ps if p.text.strip() == testo]
        if len(trovati) != 1:
            raise SystemExit(f'«{testo}»: attesi 1, trovati {len(trovati)}')
        return trovati[0]

    for testo in ("fg_incluso_att_conformita CHAR(1 CHAR) DEFAULT '0' NOT NULL,",
                  'CONSTRAINT allegati_usecase_att_conf_ck',
                  "CHECK (fg_incluso_att_conformita IN ('0','1'))"):
        p = unico(testo)
        if D.ha_commenti(p._p):
            raise SystemExit('riga DDL commentata: ' + testo)
        p._p.getparent().remove(p._p)
    p = unico("CONSTRAINT allegati_usecase_operante_ck CHECK (fg_operante IN ('0','1')),")
    D.testo_di(p, p.text.rstrip(','))     # ora è l'ultimo vincolo: via la virgola
    p = unico("'DA VERIFICARE: semantica nella struttura di origine (OP-61).';")
    D.testo_di(p, "  'BASE descrizione fissa (ANSC_09) | D.LIB.M.01 descrizione libera, tipo 998.';")
    D.ddl(d, p._p.getnext(), [
        'COMMENT ON COLUMN ANSC_USR.ALLEGATI_USECASE.ty_presenza IS',
        "  'O obbligatorio | F facoltativo | C001-C004 condizionato: la condizione e in cd_logica.';",
    ])
    p = unico("'Contenuto del documento. Si veda la raccomandazione sull uso di un archivio a "
              "oggetti.';")
    D.ddl(d, p._p.getnext(), [
        'COMMENT ON COLUMN MATR_USR.ALLEGATO.cd_stato IS',
        "  '0 Caricato in SIPO (locale, da Side) | 1-5 decodifica ANSC_08.';",
        'COMMENT ON COLUMN MATR_USR.ALLEGATO.fg_incluso_att_conformita IS',
        "  'Scelta dell ufficiale, atto per atto, salvata da GENERA e CONTINUA.';",
    ])
    fatti.append('Appendice A: ALLEGATI_USECASE senza il contrassegno, commenti sui valori; '
                 'ALLEGATO con i commenti su stato e contrassegno')

    # ─────────────────────────────── 6. Open Point, Riferimenti, storia
    t = next(t for t in d.tables if t.rows[0].cells[0].text.strip() == '#'
             and any(r.cells[0].text.strip() == 'OP-69' for r in t.rows))
    righe = {r.cells[0].text.strip(): r for r in t.rows}
    D.riscrivi_cella(righe['OP-61'].cells[2],
                     'Chiuso nella v3.36. La documentazione di Side sugli allegati (v1.5) '
                     'dichiara i valori: ty_presenza O, F, C001…C004; ty_configurazione BASE e '
                     'D.LIB.M.01. Per le colonne omonime di SOGGETTI_USECASE la domanda resta '
                     'aperta in OP-69.')
    D.riscrivi_cella(righe['OP-61'].cells[3], 'Chiuso')
    D.riscrivi_cella(righe['OP-50'].cells[2],
                     'Raccordo fra le sei descrizioni di allegato che il mapping usa e che non '
                     'trovano corrispondenza nel dizionario dei tipi (ANSC_09). La seconda parte '
                     '— il contrassegno di inclusione nell’attestazione di conformità — è chiusa '
                     'nella v3.36: come in Side, la scelta è dell’ufficiale atto per atto e si '
                     'registra su ALLEGATO.')
    assert t.rows[-1].cells[0].text.strip() == 'OP-69'
    for op in NUOVI_OP:
        D.clona_riga(t, op)
    t = D.trova_tabella(d, 'ID', 'Riferimento')
    assert t.rows[-1].cells[0].text.strip() == 'R12'
    D.clona_riga(t, R13)
    D.storia(d, *STORIA)
    fatti.append('OP-61 chiuso, OP-50 ridotto, OP-70/71/72, [R13], storia')

    d.save(DST)
    dopo = commenti(DST)
    if dopo != prima:
        raise SystemExit(f'commenti: {prima} prima, {dopo} dopo')
    print('\n'.join('· ' + f for f in fatti))
    print(f'commenti preservati: {dopo}')


if __name__ == '__main__':
    main()
