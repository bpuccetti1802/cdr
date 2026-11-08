# -*- coding: utf-8 -*-
"""Genera la v0.1 di «ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC» (08/11/2026).

Richiesta dell'utente: un documento sulle azioni di annullamento dell'atto, cancellazione
della pratica e rettifica, a partire dall'analisi v3.58 (capitoli «Cancellazione Atto in
lavorazione» e «Annullamento/Cancellazione Atto firmato»), dalle specifiche ANSC e dal codice
SIPO: come si fa oggi e dove inserirsi.

Fatti verificati sul codice SIPO (08/11/2026):
- un solo servizio di back-end, statocivile-be POST /cancellaAnnullaAtto
  (AnnullamentoCancellazioneAttoController.java:74), sceglie la procedura dal parametro
  `operazione`: ANNULLAMENTO → pkg_pratica.annullaATTO, CANCELLAZIONE → cancellaATTO,
  ANNULLAMENTOPRATICA → annullaPRATICA; poi ATTO_EXTEND.ID_USER_CANCELLA e allineamento
  ANPR (nascite /allineamentoAnnNascitaSC → 1013 · decessi /allineamentoAnnullamentoDecessoSC
  → 2011 su 2001 · matrimoni e unioni /rettificaMatrimonioSC → 5012 su 5008; cittadinanze
  nessun ramo). Non @Transactional.
- «CANCELLA PRATICA» sulle pagine di ricerca di sei aree → ANNULLAMENTOPRATICA; stato 1 (e
  per matrimoni/unioni anche INSERITO e «definito temporaneo»), mai con rettifica in corso.
- «ANNULLA ATTO» sul dettaglio (stati 2 e 3) → pagina /annullamentoCancellazione con la
  motivazione → ANNULLAMENTO. «CANCELLA ATTO» è commentato nel template.
- «RETTIFICA ATTO»: /checkAttoScansionato (entro le 23:59:59 del giorno di DATA_PRATICA),
  /updLavorazioneRettifica (stato 1, FLG_RETTIFICA_INCORSO 'S', pkg_pratica.RettificaATTO).
- CONF_STATO_PRATICA: 1 IN LAVORAZIONE · 2 DEFINITO · 3 SOSPESO · 4 ANNULLATO · 5 CANCELLATO ·
  6 INSERITO · 7 RINUNCIA (dati dalla storia git di sipo-root, ce41f65).
- Il corpo corrente di PKG_PRATICA non è fra le sorgenti; la versione 2020 limita
  annullaATTO/cancellaATTO agli stati 1 e 6, in contrasto con le guardie del front-end.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_annullamento_rettifiche.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import figura, h, par, tabella, testo, voce   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(QUI))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
NOME = 'ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC_v0.1'
OUT = os.path.join(BASE, 'Documenti finali', NOME + '.docx')
IMG = os.path.join(QUI, 'img', 'annullamento')
TAGLIA_DA = 29
DATA = '08/11/2026'


def costruisci():
    shutil.copyfile(TEMPLATE, OUT)
    d = docx.Document(OUT)
    body = d.element.body
    for ch in list(body.iterchildren())[TAGLIA_DA:]:
        if ch.tag != qn('w:sectPr'):
            body.remove(ch)
    for p in d.paragraphs:
        if '“Lorem Ipsum”' in p.text:
            testo(p, '“Integrazione SIPO – ANSC”')
        elif p.style.name == 'Subtitle':
            testo(p, 'Cancellazione della pratica, annullamento dell’atto e rettifiche: '
                     'come lavora oggi SIPO, che cosa prevede ANSC, dove inserirsi')
    return d


# =================================================================== contenuti
RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[R1]', '`ANALISI_Integrazione-ANSC_v3.58.docx` — capitoli «Cancellazione Atto in '
             'lavorazione (ex Annullamento)», «Annullamento/Cancellazione Atto firmato», '
             '«Il processo di gestione dei dati ANSC in SIPO», «La numerazione comunale», '
             '«SIPO in relazione alla web app ANSC» e il registro degli Open Point.',
     'Documento di progetto'],
    ['[R2]', '`ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.5.docx` — il recupero in SIPO di un '
             'atto formato sulla web app (R005, riepilogo, conferma).', 'Documento di progetto'],
    ['[R3]', '`PROCEDURA_Formazione-Atto_SIPO-ANSC_v0.1.docx` — il passo della firma e la '
             'prassi di Roma di correggere un atto fino alla mezzanotte.', 'Documento di progetto'],
    ['[A1]', 'Contratti ANSC (`ansc/docs/openapi/`): `R011_cancellazione_atto.yaml`, '
             '`R013_rettifica_validazione.yaml`, `R017_annotazione_rettifica.yaml`, '
             '`R005` (consultazione, note tecniche), `model_evento.yaml` (`ModelRettifica`, '
             '`ModelNotaTecnica`).', 'Contratto di terzi'],
    ['[A2]', 'Nota di processo ANSC «Annotazioni e flusso base servizi cooperativi» '
             '(`NotaProcessoAnnotazioniAndQuickCoopServiceFlow.pdf`, v1.3.0), pp. 9-12 e 18-20.',
     'Documentazione ANSC'],
    ['[A3]', 'Guida operativa ANSC, pp. 56, 62-63, 71; Guida operativa — Servizi di ausilio, '
             'pp. 8, 16-17.', 'Documentazione ANSC'],
    ['[A4]', 'Decodifiche ANSC_11 (stati dell’evento), ANSC_79 (tipo di rettifica), ANSC_03 '
             '(casi d’uso), ANSC_96 (motivo del recupero); mapping dei casi d’uso '
             '(`Dic_Nasc_118`, `Morte_012`, `Morte_013` e corrispondenti).', 'Dati ANSC'],
    ['[A5]', '`ansc/docs/Changelog.md` — voci su cancellazione, rettifica, nota tecnica, '
             'inefficacia (rilasci 1.15.0 → 1.53.0).', 'Dati ANSC'],
    ['[S1]', 'Codice SIPO di `statocivile-web` e `statocivile-be`: '
             '`DettaglioAttoStatoCivileController`, `AnnullamentoCancellazioneController`, '
             '`AnnullamentoCancellazioneAttoController`, `DettaglioAttiController`, '
             '`UtilityController`, `PropostaAnnotazioneController`.', 'Sorgente applicativo'],
    ['[S2]', 'Codice SIPO delle aree: `decessi-web`, `nascita-web`, `matrim-web`, '
             '`divorzi-web`, `unioni-web`, `cittadinanza-web` (pagine di ricerca e pulsante '
             '«Cancella pratica»).', 'Sorgente applicativo'],
    ['[S3]', 'Concentratore ANPR `all-anpr-sipo`: `AllineamentoNascitaAnprSC`, '
             '`AllineamentoDecessoAnprSC`, `AllineamentoMatrimonioAnprSC`.', 'Sorgente applicativo'],
    ['[S4]', 'Struttura di `MATR_USR` (`sql/matr_usr.sql`: `ATTO`, `ATTO_EXTEND`, '
             '`CONF_STATO_PRATICA`, `ANNOTAZIONE_ATTO`) e, per i valori di '
             '`CONF_STATO_PRATICA` e il corpo 2020 di `PKG_PRATICA`, la storia di `sipo-root` '
             '(commit `ce41f65`).', 'Sorgente applicativo'],
]

GLOSSARIO = [
    ['Termine', 'Significato in questo documento'],
    ['Cancellazione della pratica', 'L’eliminazione logica di una pratica **in lavorazione**: '
     'l’atto non è mai stato formato. In ANSC corrisponde a R011, che porta l’evento a '
     '9 CANCELLATO.'],
    ['Annullamento dell’atto', 'La rimozione degli effetti di un atto **già formato**. In SIPO '
     'oggi è un cambio di stato (4 ANNULLATO); in ANSC è un atto nuovo, l’annotazione per '
     'rettifica di tipo annullamento (R013).'],
    ['Rettifica', 'La correzione di un atto formato. In SIPO oggi l’atto si riapre fino alla '
     'mezzanotte; in ANSC l’atto non si riapre mai e la correzione è una nota tecnica, '
     'un’annotazione per errore materiale o un’annotazione per rettifica.'],
    ['Stato SIPO', 'Lo stato della pratica, `MATR_USR.ATTO.ID_STATO_PRATICA` '
     '(`CONF_STATO_PRATICA`).'],
    ['Stato ANSC', 'Lo stato dell’evento in ANSC (decodifica ANSC_11), replicato in '
     '`ANSC_STATO_ATTO.ID_STATO` [R1].'],
]

AZIONI_OGGI = [
    ['Azione', 'Dove si avvia', 'Stati SIPO ammessi', '`operazione` → procedura', 'Allineamento ANPR'],
    ['CANCELLA PRATICA', 'Pagina di ricerca di ciascuna area (sei aree)',
     '1 IN LAVORAZIONE; per matrimoni e unioni anche 6 INSERITO e il «definito temporaneo»; '
     'mai con rettifica in corso',
     '`ANNULLAMENTOPRATICA` → `pkg_pratica.annullaPRATICA`', 'Sì, secondo l’area'],
    ['ANNULLA ATTO', 'Dettaglio dell’atto (`dettaglioAttoStatoCivile`) → pagina della motivazione',
     '2 DEFINITO, 3 SOSPESO', '`ANNULLAMENTO` → `pkg_pratica.annullaATTO`', 'Sì, secondo l’area'],
    ['CANCELLA ATTO', 'Dettaglio dell’atto — pulsante commentato nel template',
     '2, 3, 4 (guardia rimasta nel controller)', '`CANCELLAZIONE` → `pkg_pratica.cancellaATTO`',
     'Non raggiungibile'],
    ['RETTIFICA ATTO', 'Dettaglio dell’atto', '2 DEFINITO (e 3, 4 nella guardia), entro le '
     '23:59:59 del giorno della pratica', '`/updLavorazioneRettifica` → '
     '`pkg_pratica.RettificaATTO`', 'Alla nuova definizione, secondo l’area (non per le nascite)'],
    ['PROPOSTA ANNOTAZIONE', 'Dettaglio dell’atto', '2 DEFINITO', '`/salvaPropostaAnnotazione` '
     '(riga di `ANNOTAZIONE_ATTO`)', 'Al momento dell’aggiornamento anagrafico'],
]

STATI_SIPO = [
    ['ID', 'Descrizione', 'Note'],
    ['1', 'IN LAVORAZIONE', 'Lo stato della compilazione; vi ritorna anche l’atto in rettifica.'],
    ['2', 'DEFINITO', 'L’atto è definito. Nel percorso ANSC coincide con la firma dell’USC [R1].'],
    ['3', 'SOSPESO', ''],
    ['4', 'ANNULLATO', 'Esito di «ANNULLA ATTO».'],
    ['5', 'CANCELLATO', 'Esito dei vecchi `/eliminaAtto` di decessi e nascite, oggi non richiamati.'],
    ['6', 'INSERITO', ''],
    ['7', 'RINUNCIA', 'Solo matrimoni e divorzi.'],
]

ALLINEAMENTO = [
    ['Area', 'Servizio di `all-anpr-sipo`', 'Operazione ANPR'],
    ['NASCITE', '`/allineamentoAnnNascitaSC` (`AllineamentoNascitaAnprSC.java:504`)',
     '1013 annullamento dell’iscrizione, se l’ultima operazione era 1001, 1002, A001, A002 o A006'],
    ['DECESSI', '`/allineamentoAnnullamentoDecessoSC` (`AllineamentoDecessoAnprSC.java:193`)',
     '2011 annullamento della 2001; per il non residente si azzera la morte sul soggetto'],
    ['MATRIMONI, UNIONI (e divorzi)', '`/rettificaMatrimonioSC` (`AllineamentoMatrimonioAnprSC.java:660`)',
     '5012 annullamento della 5008'],
    ['CITTADINANZE', '—', 'Nessun ramo: nessun allineamento'],
]

STATI_ANSC = [
    ['ID', 'Stato ANSC_11', 'Rilievo per questo documento'],
    ['1', 'BOZZA', 'Cancellabile con R011 (sulla web app «Elimina»).'],
    ['2', 'CONFERMATO', 'Depositato con R009: cancellabile con R011.'],
    ['3', 'ANNULLATO', 'Esiste da sempre; nessuna fonte lo lega alla rettifica di tipo '
     'annullamento (OP-80).'],
    ['4', 'FIRMATO DAL DICHIARANTE', 'Se R011 lo accetti non è dichiarato [DA VERIFICARE].'],
    ['5', 'FIRMATO DA USC', 'L’atto è formato: R011 lo rifiuta. Da qui in poi solo annotazioni '
     'o nota tecnica.'],
    ['6', 'GENERATO DA SISTEMA', 'Annotazioni automatiche.'],
    ['7', 'APPROVATO', 'Flusso delle notifiche.'],
    ['8', 'RIFIUTATA', 'Provvedimento di rifiuto (R016).'],
    ['9', 'CANCELLATO', 'Esito di R011 (dal 20/12/2023).'],
    ['10', 'INEFFICACE', 'Esito dell’annullamento per inefficacia, solo web app, disabilitato '
     'dalla versione 1.52.0.'],
    ['11', 'FIRMATO PER CONFORMITA', 'Se R011 lo accetti non è dichiarato [DA VERIFICARE].'],
]

TIPI_RETTIFICA = [
    ['ANSC_79', 'Descrizione', 'Uso'],
    ['0', 'ANNULLAMENTO', 'Rettifica di annullamento: R013 richiede solo `evento`.'],
    ['1', 'MODIFICA', 'Rettifica di modifica: R013 richiede anche `eventoModificato`, l’atto '
     'completo già rettificato. Lo usa anche l’errore materiale nell’esempio di ANSC.'],
    ['2', 'NOTATECNICA', 'Nota tecnica (dalla versione 1.25.0).'],
    ['3', 'NOTATECNICARETTIFICA', ''],
    ['4', 'ANNOTAZIONERETTIFICA', 'Correzione di un’annotazione (R017).'],
]

STRUMENTI = [
    ['Strumento', 'Servizio', 'Canale', 'Che cosa fa', 'Condizioni e limiti'],
    ['Cancellazione', 'R011 `/evento/elimina`', 'Cooperativo e web app',
     'Elimina logicamente un evento non ancora formato (9 CANCELLATO).',
     'Rifiuta l’atto 5 FIRMATO DA USC. Il contratto non dichiara gli stati ammessi né lo '
     'stato risultante.'],
    ['Annotazione per rettifica, tipo annullamento', 'R013 `/rettifica/validazione/evento`',
     'Cooperativo e web app', 'Atto nuovo che richiama l’atto e ne inibisce certificato '
     'semplice ed estratto per riassunto.', 'Provvedimento di una terza amministrazione '
     '(art. 95). Numero comunale proprio. Controllo «atto già annullato» dalla 1.21.0.'],
    ['Annotazione per rettifica, tipo modifica', 'R013, idem', 'Cooperativo e web app',
     'Modifica i dati: certificati ed estratti riportano i dati corretti.',
     'Serve `eventoModificato`. Provvedimento di una terza amministrazione.'],
    ['Annotazione per errore materiale (art. 98)', 'R013, idem', 'Cooperativo e web app',
     'Corregge i dati anagrafici dell’intestatario (e dei genitori nella nascita).',
     '«NON può comportare l’annullamento». Atti del proprio comune.'],
    ['Annotazione modificativa', 'R013 `/annotazione/modificativa/validazione/evento`',
     'Cooperativo', 'Annotazioni modificative (es. cambio di generalità del genitore).',
     'Dalla versione 1.20.0.'],
    ['Correzione di un’annotazione', 'R017 `/annotazione-rettifica/validazione/evento`',
     'Cooperativo e web app', 'Corregge un’annotazione non automatica e non contestuale.',
     'Sulla web app disabilitata dalla versione 1.52.0.'],
    ['Nota tecnica', 'nessuno (R005 la consulta)', 'Solo web app',
     'Corregge i metadati di un atto formato.', 'Solo il comune che ha redatto l’atto; atto '
     'FIRMATO DA USC senza annotazioni modificative successive.'],
    ['Annullamento per inefficacia', 'nessuno', 'Solo web app', 'Porta l’atto a 10 INEFFICACE.',
     'Introdotto con la 1.41.0, disabilitato dalla 1.52.0 (04/06/2026).'],
]

UC_RETTIFICA = [
    ['Registro', 'Annotazione per rettifica', 'Annotazione per errore materiale'],
    ['Nascita', '14630000 · Dic_Nasc_118', '14640000 · Dic_Nasc_119'],
    ['Morte', '2341 · Morte_012', '2342 · Morte_013'],
    ['Matrimonio', '368699 · Matr_017', '368799 · Matr_018'],
    ['Unione civile', '458699 · UnCiv_007', '458799 · UnCiv_008'],
    ['Cittadinanza', '53719 · Citt_047', '53729 · Citt_048'],
]

CANCELLA_PASSI = [
    ['#', 'Passo', 'Dove nel codice', 'Esito'],
    ['1', 'Lettura di `ANSC_STATO_ATTO` per l’`ID_ATTO`.', '`statocivile-be`, '
     '`/cancellaAnnullaAtto`, prima della scelta della procedura', 'Nessuna riga: si prosegue '
     'come oggi.'],
    ['2', 'Stato 5 FIRMATO DA USC.', 'idem', 'KO «Atto non cancellabile perché risulta FIRMATO '
     'USC»: la pratica resta, si segnala il disallineamento (SIPO 1, ANSC 5).'],
    ['3', 'Stato 9 CANCELLATO.', 'idem', 'Nessuna chiamata ad ANSC: si conclude in SIPO (era '
     'già stato cancellato, per esempio dopo un esito indeterminato riconciliato).'],
    ['4', 'Riga senza `ID_ANSC`.', 'idem', 'Stato 9 su `ANSC_STATO_ATTO` (uso locale), poi '
     'come oggi.'],
    ['5', 'Riga con `ID_ANSC`: chiamata a `annullaAtto` del concentratore (R011).',
     '`all-ansc-sipo`, `ansc-v1.yaml`', 'OK: stato 9, poi come oggi. KO: la pratica non si '
     'cancella, si mostra l’errore ANSC. Timeout: esito indeterminato, R005, mai una seconda '
     'chiamata alla cieca.'],
    ['6', '`pkg_pratica.annullaPRATICA`, `ID_USER_CANCELLA`, allineamento ANPR.',
     'codice attuale, invariato', 'Come oggi.'],
    ['7', 'Numero comunale associato: `PUT /scarta`.', '`be-numeratore-comunale`',
     'Il numero non resta assegnato a un atto che non esiste.'],
]

INNESTI = [
    ['Punto del codice', 'Oggi', 'Intervento'],
    ['`statocivile-be` · `AnnullamentoCancellazioneAttoController.cancellaAnnullaAtto` (:74)',
     'Sceglie la procedura e allinea ANPR.',
     'Per `ANNULLAMENTOPRATICA` il controllo su `ANSC_STATO_ATTO` e R011 **prima** della '
     'procedura; per `ANNULLAMENTO` il rifiuto se l’atto è formato in ANSC e non ne risulta '
     'l’annullamento; per `CANCELLAZIONE` lo stesso rifiuto. È l’unico punto per sei aree.'],
    ['Pagine di ricerca delle sei aree · `confermaCancellazionePratica`',
     'Mostrano esito e messaggio del back-end.', 'Nessuna logica nuova: il messaggio KO di '
     'ANSC arriva nella `descrizione` della risposta. Va verificato che il testo sia mostrato '
     'in tutte le aree.'],
    ['`statocivile-web` · `DettaglioAttoStatoCivileController.checkShowButton` (:355 e seg.)',
     'Decide «ANNULLA ATTO», «RETTIFICA ATTO», «PROPOSTA ANNOTAZIONE».',
     'Per l’atto formato in ANSC: «RETTIFICA ATTO» non si mostra; «ANNULLA ATTO» apre il '
     'percorso dell’annullamento ANSC (fase 1: indicazione e riallineamento).'],
    ['`statocivile-be` · `DettaglioAttiController./checkAttoScansionato` (:1036)',
     'Regola della mezzanotte.', 'Prima della regola, KO «Atto formato in ANSC: non si '
     'riapre» se `ANSC_STATO_ATTO` ha `ID_ANSC` e stato 5.'],
    ['`statocivile-be` · `DettaglioAttiController./updLavorazioneRettifica` (:1468)',
     'Riporta l’atto in lavorazione.', 'Stesso controllo, come difesa: il servizio è '
     'raggiungibile anche senza passare dal pulsante.'],
    ['`all-ansc-sipo` · `ansc-v1.yaml`', '`annullaAtto` (R011) già previsto [R1].',
     'Fase 2: operazione di deposito della rettifica (R013) e della firma (R007), OP-45 e OP-81.'],
    ['`be-numeratore-comunale`', '`PUT /scarta`, `PUT /utilizza`.', 'Scarto alla '
     'cancellazione; numero proprio per l’annotazione per rettifica (fase 2).'],
]

RETTIFICA_SCELTA = [
    ['Che cosa va corretto', 'Strumento ANSC', 'Canale oggi', 'Effetto sull’atto in SIPO'],
    ['Un dato tecnico o un metadato (non i dati anagrafici del soggetto)', 'Nota tecnica',
     'Solo web app', 'Riallineamento dei dati in SIPO dopo la correzione [DA VERIFICARE: '
     'quali campi].'],
    ['I dati anagrafici dell’intestatario (o dei genitori nella nascita), per errore materiale',
     'Annotazione per errore materiale (art. 98), UC `*_013` / `Dic_Nasc_119`',
     'R013 o web app', 'Un atto nuovo (l’annotazione) collegato all’atto; l’atto originale '
     'resta.'],
    ['Dati dell’atto, su provvedimento', 'Annotazione per rettifica, tipo modifica',
     'R013 o web app', 'Un atto nuovo collegato; l’atto originale resta.'],
    ['L’esistenza stessa dell’atto, su provvedimento', 'Annotazione per rettifica, tipo '
     'annullamento', 'R013 o web app', 'Un atto nuovo collegato; l’atto originale diventa '
     'annullato (stato da accertare, OP-80).'],
]

APERTI = [
    ['#', 'Questione', 'Owner'],
    ['AR-01', 'Corpo corrente di `PKG_PRATICA` (`annullaPRATICA`, `annullaATTO`, '
              '`cancellaATTO`, `RettificaATTO`): non è fra le sorgenti. La versione 2020 '
              'limita `annullaATTO` e `cancellaATTO` agli stati 1 e 6, mentre il front-end li '
              'propone per gli stati 2, 3 e 4. Va letto prima di scrivere codice.',
     'Sviluppo SIPO'],
    ['AR-02', 'Se R011 accetti gli stati 4 FIRMATO DAL DICHIARANTE e 11 FIRMATO PER '
              'CONFORMITA. Decide se «CANCELLA PRATICA» resti disponibile dopo le firme dei '
              'dichiaranti.', 'Analisi / Sogei'],
    ['AR-03', 'Il «definito temporaneo» di matrimoni e unioni (stato 1 con `CAN_FINALIZZA`): '
              'a quale fase del percorso ANSC corrisponde e se la cancellazione della pratica '
              'vi resti ammessa.', 'Analisi'],
    ['AR-04', 'Allineamento ANPR dopo la cancellazione di una pratica e dopo l’annullamento di '
              'un atto formato in ANSC: se SIPO debba continuare a chiamare `all-anpr-sipo` '
              '(1013, 2011, 5012) o se gli effetti anagrafici arrivino da ANSC. Il rischio è un '
              'doppio intervento sull’anagrafe.', 'Analisi / Comune'],
    ['AR-05', 'La prassi di Roma di correggere un atto fino alla mezzanotte: con ANSC la '
              'finestra si chiude alla firma dell’USC. Va deciso con lo stato civile (si lega '
              'a [R3]).', 'Comune'],
    ['AR-06', 'Quali campi di SIPO riallineare dopo una nota tecnica fatta sulla web app, e '
              'come accorgersene: la riconciliazione è su richiesta [R1].', 'Analisi'],
    ['AR-07', 'Proposta di annotazione di SIPO e annotazioni ANSC: per gli atti formati in ANSC '
              'le annotazioni sono atti ANSC (UC `_998_*`, R013); il modulo delle annotazioni di '
              'SIPO non chiama ANSC. Da trattare in un documento dedicato.', 'Analisi'],
    ['AR-08', 'Il servizio `/cancellaAnnullaAtto` non è transazionale e l’allineamento ANPR '
              'fallito non annulla il cambio di stato: con R011 nel mezzo l’ordine dei passi '
              'diventa vincolante (R011, poi procedura, poi ANPR).', 'Sviluppo SIPO'],
    ['AR-09', 'Le chiamate di «CANCELLA PRATICA» delle aree non passano `ruoloBe` e `hostname` '
              'al back-end, che li usa per l’allineamento ANPR: da correggere insieme '
              'all’intervento.', 'Sviluppo SIPO'],
]


# ===================================================================== testo
def scrivi(d):
    # ------------------------------------------------------------------- 1
    h(d, 1, 'Scopo del documento')
    par(d, 'Il documento tratta tre azioni con cui l’ufficio dello stato civile interviene su '
           'una pratica o su un atto: la **cancellazione della pratica** in lavorazione, '
           'l’**annullamento dell’atto** e la **rettifica**. Per ciascuna descrive come la '
           'esegue oggi SIPO, che cosa prevede ANSC e dove si inserisce l’integrazione.')
    par(d, 'Parte dai due capitoli dell’analisi di integrazione dedicati alla cancellazione e '
           'all’annullamento [R1], li completa con le specifiche ANSC e con la lettura del '
           'codice di SIPO, e aggiunge la rettifica, che l’analisi tocca solo di passaggio. Le '
           'questioni ancora da decidere sono raccolte in coda, come punti aperti AR-01…AR-09, '
           'accanto agli OP-80…OP-84 dell’analisi.')
    par(d, 'Il punto da tenere presente in tutto il documento è uno solo: **in SIPO un atto '
           'definito si può ancora cambiare di stato o riaprire; in ANSC un atto firmato '
           'dall’ufficiale non si tocca più.** Quello che SIPO fa oggi con un cambio di stato, '
           'per un atto formato in ANSC diventa la formazione di un atto nuovo.')
    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 5.0, 1.3])
    h(d, 2, 'Glossario')
    tabella(d, GLOSSARIO, [1.8, 5.1])

    # ------------------------------------------------------------------- 2
    h(d, 1, 'Le tre azioni in sintesi')
    par(d, 'Lo strumento giusto non dipende dal pulsante premuto in SIPO, ma da dove si trova '
           'l’atto in ANSC. La figura incrocia le tre azioni di SIPO con le tre situazioni '
           'possibili: atto non presente in ANSC, atto depositato ma non ancora firmato '
           'dall’ufficiale, atto formato.')
    figura(d, os.path.join(IMG, 'mappa_azioni.png'), 6.6,
           'Figura 1 — Le tre azioni di SIPO e lo stato dell’atto in ANSC.')
    par(d, 'Tre conseguenze, che il resto del documento sviluppa:')
    voce(d, 'La cancellazione della pratica', 'resta un’azione di SIPO, con una chiamata ad '
         'ANSC (R011) quando l’atto vi è già stato depositato. L’intervento è piccolo e sta in '
         'un solo punto del back-end.')
    voce(d, 'L’annullamento dell’atto', 'per un atto formato in ANSC non è più un cambio di '
         'stato: è un’annotazione per rettifica di tipo annullamento, con provvedimento, numero '
         'comunale e firma propri. L’analisi ne rinvia l’implementazione in SIPO [R1]: fino ad '
         'allora si fa sulla web app e SIPO si riallinea.')
    voce(d, 'La rettifica', 'come la conosce SIPO, cioè la riapertura dell’atto fino alla '
         'mezzanotte, non esiste in ANSC. Prima della firma dell’ufficiale c’è il ritorno ai '
         'dati; dopo, solo nota tecnica o annotazioni.')

    # ------------------------------------------------------------------- 3
    h(d, 1, 'Come lavora oggi SIPO')
    par(d, 'Le azioni stanno in due posti dell’interfaccia, la pagina di ricerca di ciascuna '
           'area e il dettaglio comune dell’atto, e convergono su un solo servizio di back-end '
           '[S1] [S2]:')
    tabella(d, AZIONI_OGGI, [1.2, 1.6, 1.6, 1.5, 1.0])

    h(d, 2, 'Gli stati della pratica')
    par(d, 'Lo stato della pratica è `MATR_USR.ATTO.ID_STATO_PRATICA`, decodificato da '
           '`CONF_STATO_PRATICA` (`ID`, `DESCRIZIONE`, `AREA`). Lo script della struttura non '
           'contiene i valori; quelli che seguono vengono dall’esportazione dei dati nella '
           'storia del repository [S4] e coincidono con le costanti del front-end '
           '(`DettaglioAttoStatoCivileController.java:102-108`):')
    tabella(d, STATI_SIPO, [0.5, 1.6, 4.8])
    par(d, 'Due elementi accompagnano lo stato. `ATTO.FLG_RETTIFICA_INCORSO` (CHAR(1), '
           'predefinito N) segnala l’atto definito riaperto per rettifica; il commento della '
           'colonna dice «lo stato da DEFINITO ritorna a IN LAVORAZIONE». Il «definito '
           'temporaneo» di matrimoni e unioni non è uno stato: è lo stato 1 con '
           '`ATTO_EXTEND.CAN_FINALIZZA = S`. Per gli annullamenti e le cancellazioni `ATTO` '
           'porta data e motivo (`DATA_ANNULLAMENTO_ATTO`, `MOTIVO_ANNULLAMENTO_ATTO`, '
           '`DATA_CANCELLAZIONE_ATTO`, `MOTIVO_CANCELLAZIONE_ATTO`) e `ATTO_EXTEND` registra '
           'l’utente (`ID_USER_CANCELLA`).')

    h(d, 2, 'Il servizio unico: /cancellaAnnullaAtto')
    par(d, '`POST /cancellaAnnullaAtto` di `statocivile-be` '
           '(`AnnullamentoCancellazioneAttoController.java:74`) è il solo punto in cui SIPO '
           'cancella o annulla. Riceve `idAtto`, `motivazione`, `operazione`, `area` e '
           '`idUtente`, e lavora in quattro passi:')
    voce(d, '1. Prepara la richiesta per l’anagrafe', 'secondo l’area (nascite, matrimoni e '
         'divorzi, unioni, decessi), **prima** di cambiare lo stato. Un errore qui è ignorato.')
    voce(d, '2. Chiama la procedura', 'scelta da `operazione`: `ANNULLAMENTO` → '
         '`pkg_pratica.annullaATTO`, `CANCELLAZIONE` → `pkg_pratica.cancellaATTO`, '
         '`ANNULLAMENTOPRATICA` → `pkg_pratica.annullaPRATICA`. Ingresso: atto e motivazione; '
         'uscita: esito e messaggio.')
    voce(d, '3. Registra l’utente', 'in `ATTO_EXTEND` (`ID_USER_CANCELLA`), se l’esito non è KO.')
    voce(d, '4. Allinea l’anagrafe', 'chiamando il concentratore ANPR `all-anpr-sipo` [S3]. Se '
         'l’allineamento fallisce, l’esito della procedura resta e all’operatore arriva il '
         'messaggio di errore: il servizio non è transazionale.')
    tabella(d, ALLINEAMENTO, [1.6, 2.9, 2.4])
    par(d, 'Il corpo corrente di `PKG_PRATICA` non è fra le sorgenti. Nella versione del 2020 '
           'conservata nella storia del repository [S4] `cancellaATTO` e `annullaATTO` '
           'aggiornano soltanto stato, data e motivo, e solo per gli atti negli stati 1 e 6; '
           'il commento di testata lascia «da fare» il ripristino dell’anagrafe e la sorte di '
           'comunicazioni e annotazioni. `annullaPRATICA`, la procedura oggi usata da tutte le '
           'aree, non compare in alcuna versione disponibile. Nessuna delle procedure libera il '
           'numero dell’atto (AR-01).')

    h(d, 2, 'La cancellazione della pratica')
    par(d, 'Ogni area ha nella pagina di ricerca il pulsante «Cancella pratica». L’operatore '
           'seleziona la riga, il sistema controlla lo stato e chiede conferma '
           '(«la pratica in lavorazione verrà cancellata»); alla conferma chiama '
           '`/cancellaAnnullaAtto` con `operazione = ANNULLAMENTOPRATICA`.')
    figura(d, os.path.join(IMG, 'v358_1.png'), 6.2,
           'Figura 2 — La ricerca delle nascite con il pulsante «CANCELLA PRATICA» [R1].')
    tabella(d, [
        ['Area', 'Controller (front-end)', 'Stati ammessi'],
        ['Decessi', '`GestioneDecessiController` (`cancellaPratica` :747, conferma :791)',
         '1, senza rettifica in corso'],
        ['Nascite', '`GestioneNascitaController` (:912, conferma :960)', '1, senza rettifica in corso'],
        ['Matrimoni', '`GestioneAttiMatrimonioController` (:835, conferma :945)',
         '6, 1 e «definito temporaneo», senza rettifica in corso'],
        ['Divorzi', '`GestioneAttiSeparazioneDivorzioController` (:787, conferma :1599)',
         '6 e 1 (area inviata: MATRIMONI)'],
        ['Unioni civili', '`GestioneUnioniController` (:549, conferma :673)',
         '6, 1 e «definito temporaneo», senza rettifica in corso'],
        ['Cittadinanze', '`GestioneCittadinanzaController` (:547, conferma :700)', '1'],
    ], [1.2, 3.7, 2.0])
    par(d, 'Restano nel codice due vecchi servizi `/eliminaAtto` (decessi e nascite) che portano '
           'l’atto a 5 CANCELLATO senza controlli di ruolo: i loro richiami nel front-end sono '
           'commentati. Il servizio `annullaPratica` dei divorzi non ha chiamanti.')

    h(d, 2, 'L’annullamento dell’atto')
    par(d, 'Dal dettaglio di un atto 2 DEFINITO o 3 SOSPESO il pulsante «ANNULLA ATTO» '
           '(`dettaglioAttoStatoCivile.html:208`, nascosto per la richiesta di costituzione di '
           'unione civile) apre la pagina comune `/annullamentoCancellazione`, dove l’operatore '
           'scrive la motivazione; alla conferma il front-end chiama `/cancellaAnnullaAtto` con '
           '`operazione = ANNULLAMENTO`. Non c’è limite di tempo né un ruolo dedicato: il '
           'servizio ammette gli stessi ruoli degli altri servizi dello stato civile.')
    par(d, 'Il pulsante gemello «CANCELLA ATTO» (`operazione = CANCELLAZIONE`) è commentato nel '
           'template: il controller che lo gestisce è ancora presente.')

    h(d, 2, 'La rettifica dell’atto')
    par(d, 'La rettifica di SIPO **riapre l’atto e lo corregge sul posto**. Dal dettaglio, il '
           'pulsante «RETTIFICA ATTO» («RETTIFICA VERBALE» per la richiesta di costituzione di '
           'unione civile) compare solo se `/checkAttoScansionato` risponde positivamente:')
    voce(d, 'La regola della mezzanotte.', '`DettaglioAttiController.java:1098-1123` prende '
         '`ATTO.DATA_PRATICA`, fissa il limite alle 23:59:59 dello stesso giorno (ora di Roma) e '
         'dopo il limite risponde «Atto definito da più di 24 ore». Una regola precedente '
         '(24 ore dalla data) è rimasta commentata; il controllo sulla scansione dell’atto è '
         'disattivato.')
    voce(d, 'L’eccezione del verbale.', 'Il verbale di richiesta di costituzione di unione civile '
         'si rettifica entro 180 giorni, se non è già usato da un atto.')
    par(d, 'Alla conferma, `/updLavorazioneRettifica` (`DettaglioAttiController.java:1468`) salva '
           'lo stato precedente in `ATTO_EXTEND` (`ID_CONF_STATO_PRATICA_OLD`), riporta l’atto a '
           '1 IN LAVORAZIONE, azzera `DATA_DEFINIZIONE_ATTO`, imposta `FLG_RETTIFICA_INCORSO = S` '
           'e chiama `pkg_pratica.RettificaATTO`, che secondo il commento elimina le annotazioni '
           'proposte a mano. L’operatore viene portato alla maschera di compilazione del tipo '
           'atto. Alla nuova definizione i flussi di area riconoscono la rettifica dallo stato '
           'precedente e chiamano l’aggiornamento anagrafico di modifica (`/modificaDecessoSC`, '
           '`/modificaMatrimonioSC`); per le nascite l’anagrafe **non** è toccata e l’operatore è '
           'invitato a usare le funzioni dell’anagrafe.')
    par(d, 'Dopo la mezzanotte l’unica via è l’**annotazione**: «PROPOSTA ANNOTAZIONE» (atti '
           'definiti) crea una riga in `ANNOTAZIONE_ATTO` che punta all’atto '
           '(`ID_ATTO_TARGET`), con tipo, formula e testo, e segue il suo ciclo (proposta, '
           'stampata, scartata, apposta) nel modulo delle annotazioni. L’atto originale non '
           'cambia. Il modulo non contiene chiamate ad ANSC.')

    # ------------------------------------------------------------------- 4
    h(d, 1, 'Che cosa prevede ANSC')
    h(d, 2, 'Gli stati dell’evento')
    par(d, 'La decodifica ANSC_11 ha undici stati [A4]. Quelli che contano qui sono tre: la '
           'cancellazione porta a 9, la firma dell’ufficiale (5) chiude ogni intervento '
           'diretto, l’annullamento lascia l’atto in uno stato che le fonti non dichiarano.')
    tabella(d, STATI_ANSC, [0.5, 2.0, 4.4])

    h(d, 2, 'La cancellazione: R011')
    par(d, '`POST /evento/elimina/{version}` «elimina logicamente l’evento sulle basi dati» '
           '[A1]. Il corpo è l’involucro comune più l’**intero modello evento**, senza campi '
           'dichiarati obbligatori; le risposte sono 200 (cancellazione riuscita), 400, 403 e 404 '
           '(evento non presente). Il contratto **non dice** da quali stati la cancellazione sia '
           'ammessa né lo stato risultante: il 9 CANCELLATO si ricava dalla decodifica, dal '
           'changelog e dal flusso di Side [R1]. Il changelog documenta il servizio dalla 1.23.0 '
           '(«Cancellazione Atto – Eliminazione fisica / annullamento») e il rifiuto degli atti '
           'firmati dall’ufficiale. Sulla web app l’azione si chiama «Elimina atto» ed è '
           'proposta per gli eventi in bozza [A3]; dalla 1.49.0 l’eliminazione di una bozza '
           'disattiva il soggetto se è legato a un altro atto [A5].')

    h(d, 2, 'Gli strumenti su un atto formato')
    par(d, 'Sull’atto 5 FIRMATO DA USC ANSC non consente modifiche dirette. Gli strumenti sono '
           'questi [A1] [A2] [A3] [A5]:')
    tabella(d, STRUMENTI, [1.4, 1.4, 0.9, 1.6, 1.6])
    par(d, 'Il tipo di rettifica è un dato del modello evento (`datiRettifica.idTipoRettifica`, '
           'decodifica ANSC_79):')
    tabella(d, TIPI_RETTIFICA, [0.7, 2.0, 4.2])

    h(d, 2, 'La rettifica di tipo annullamento')
    par(d, 'È un atto nuovo, un’annotazione, che richiama l’atto da annullare in '
           '`datiRettifica.eventoCollegato` [A2]. Il processo — provvedimento di una terza '
           'amministrazione, caso d’uso «Annotazione per rettifica» del registro, compilazione, '
           'validazione con R013 e `idTipoRettifica = 0`, firma dell’ufficiale — è descritto per '
           'intero nell’analisi [R1], con i 24 campi del mapping. Qui interessano tre fatti: '
           'l’atto da annullare si individua per comune, numero comunale, anno, data e tipo di '
           'registro, mentre l’`idAnsc` è facoltativo; `idTipoRettifica` non compare in nessun '
           'mapping e lo valorizza il concentratore; ANSC non pubblica un esempio di richiesta di '
           'annullamento.')
    figura(d, os.path.join(IMG, 'v358_4.png'), 6.2,
           'Figura 3 — L’annullamento di un atto firmato: la rettifica di tipo annullamento [R1].')
    par(d, 'I casi d’uso sono uno per registro, affiancati da quelli dell’errore materiale [A4]:')
    tabella(d, UC_RETTIFICA, [1.4, 2.7, 2.8])

    h(d, 2, 'Le rettifiche che non annullano')
    voce(d, 'Rettifica di modifica.', 'Stesso servizio e stesso caso d’uso, `idTipoRettifica = 1`: '
         'R013 vuole anche `eventoModificato`, l’atto completo già rettificato; l’esempio di ANSC '
         'vi riporta `id` e `idAnsc` dell’atto originale. Certificati ed estratti escono con i '
         'dati corretti.')
    voce(d, 'Errore materiale (art. 98).', 'Caso d’uso proprio (`Morte_013`, `Dic_Nasc_119`…), '
         'formula 888, testo della correzione in `composizioneCompleta`. Corregge i dati '
         'anagrafici; non può annullare.')
    voce(d, 'Correzione di un’annotazione.', 'R017, con `idEventoAnnotazione` obbligatorio. Sulla '
         'web app è disabilitata dalla 1.52.0; la 1.53.0 annuncia un aggiornamento del servizio.')
    voce(d, 'Nota tecnica.', 'Solo web app (1.25.0: «lato servizi cooperativi è stato '
         'implementato il solo servizio di consultazione»). La fa il comune che ha redatto '
         'l’atto, sull’atto firmato dall’ufficiale e senza annotazioni modificative successive; '
         'R005 `/consultazione/ansc/evento/note/tecniche` permette di leggerla.')
    par(d, 'Per tutte, la firma è dell’ufficiale: nessuna fonte prevede la firma di un '
           'dichiarante. Il changelog documenta «Firma USC per Rettifiche» per i servizi '
           'cooperativi (1.33.3, 1.34.4), ma nessun documento descrive il passo (OP-81).')

    h(d, 2, 'Ciò che le fonti non dicono')
    voce(d, 'Gli stati ammessi da R011', 'e lo stato che ne risulta (AR-02).')
    voce(d, 'Lo stato dell’atto annullato', 'con rettifica (OP-80).')
    voce(d, 'Gli effetti dell’annullamento', 'su notifiche, annotazioni automatiche e '
         'comunicazioni anagrafiche (OP-82). Per le rettifiche il changelog documenta la '
         'rigenerazione delle notifiche e delle annotazioni (1.46.0, 1.49.0, 1.50.0) e l’invio '
         'in conservazione degli atti rettificati e annullati (1.47.0).')
    voce(d, 'L’annullamento per inefficacia', 'è privo di servizio cooperativo e oggi '
         'disabilitato (OP-83).')

    # ------------------------------------------------------------------- 5
    h(d, 1, 'Dove e come inserirsi')
    par(d, 'Un criterio regge tutti gli interventi: **la decisione si prende nel back-end, sullo '
           'stato replicato in `ANSC_STATO_ATTO`**, e il front-end si limita a mostrare o '
           'nascondere i pulsanti e a riportare i messaggi. Il motivo è pratico: sei aree '
           'chiamano lo stesso servizio, e i servizi di rettifica sono raggiungibili anche senza '
           'passare dal pulsante.')
    tabella(d, INNESTI, [2.2, 1.5, 3.2])

    h(d, 2, 'Cancellazione della pratica: R011 prima della procedura')
    par(d, 'L’analisi ha già fissato il comportamento [R1]: integrare il software solo dove c’è '
           'il pulsante «CANCELLA PRATICA», controllare lo stato su `ANSC_STATO_ATTO`, chiamare '
           'R011 se c’è un `idAnsc`, bloccare la cancellazione locale se R011 fallisce. Il codice '
           'dice **dove**: dentro `/cancellaAnnullaAtto`, per `operazione = ANNULLAMENTOPRATICA`, '
           'tra la preparazione della richiesta anagrafica e la chiamata a '
           '`pkg_pratica.annullaPRATICA`. Un solo punto copre le sei aree.')
    tabella(d, CANCELLA_PASSI, [0.3, 2.2, 1.9, 2.5])
    figura(d, os.path.join(IMG, 'v358_3.png'), 4.6,
           'Figura 4 — La cancellazione di una pratica da SIPO e i riflessi su ANSC [R1].')
    par(d, 'L’ordine è vincolante. Il servizio non è transazionale e oggi un allineamento ANPR '
           'fallito non annulla il cambio di stato; con R011 nel mezzo, chiamare la procedura '
           'prima di ANSC lascerebbe in SIPO una pratica cancellata e in ANSC un evento vivo, '
           'senza modo di accorgersene (AR-08). Il caso SIPO 1 con ANSC 5 non dovrebbe esistere, '
           'perché nel percorso ANSC la definizione coincide con la firma dell’ufficiale: se si '
           'presenta è un disallineamento e va trattato come tale, non come una cancellazione '
           'negata.')

    h(d, 2, 'Annullamento dell’atto: due fasi')
    par(d, 'Per gli atti **non** formati in ANSC — tutti quelli anteriori all’adozione — '
           '«ANNULLA ATTO» resta com’è. Per un atto con `ID_ANSC` e stato 5 il cambio di stato in '
           'SIPO non basta più: in ANSC l’atto resterebbe valido e certificabile. L’analisi '
           'rinvia l’implementazione della rettifica di annullamento a un approfondimento con lo '
           'stato civile [R1]; il documento propone quindi due fasi.')
    voce(d, 'Fase 1 — annullamento sulla web app e riallineamento in SIPO.', 'Per l’atto formato '
         'in ANSC «ANNULLA ATTO» non chiama la procedura: spiega che l’annullamento si fa con '
         'l’annotazione per rettifica sulla web app e offre «Riallinea da ANSC». Il '
         'riallineamento legge l’atto con R005 (idAnsc, con `flagRettifica` per avere l’ultima '
         'rettifica), mostra l’annotazione trovata e, a conferma dell’operatore, esegue '
         '`pkg_pratica.annullaATTO` con la motivazione e aggiorna `ANSC_STATO_ATTO`. Sono gli '
         'stessi elementi del recupero degli atti a testo libero [R2]. Il controllo nel '
         'back-end rifiuta `ANNULLAMENTO` per un atto formato in ANSC finché R005 non mostra la '
         'rettifica.')
    voce(d, 'Fase 2 — annullamento formato da SIPO.', 'Una pagina comune ai registri per '
         'l’annotazione per rettifica (i cinque casi d’uso chiedono gli stessi dati), numero '
         'comunale proprio dal numeratore, R013 con `idTipoRettifica = 0`, firma '
         'dell’ufficiale, poi gli stessi passi della fase 1. Richiede di chiudere OP-80, OP-81 e '
         'OP-84, e di aggiungere al contratto del concentratore il deposito della rettifica.')
    par(d, 'In entrambe le fasi resta aperto l’allineamento ANPR: oggi SIPO lo esegue a ogni '
           'annullamento (2011, 5012, 1013); per un atto formato in ANSC gli effetti anagrafici '
           'potrebbero arrivare da ANSC, e farli due volte sarebbe un errore (AR-04).')

    h(d, 2, 'Rettifica: l’atto formato in ANSC non si riapre')
    par(d, 'La rettifica di SIPO non ha corrispondente in ANSC. Gli interventi sono tre:')
    voce(d, 'Nascondere il pulsante.', '`checkShowButton` non mostra «RETTIFICA ATTO» per gli '
         'atti con `ID_ANSC` e stato 5, e `/checkAttoScansionato` e `/updLavorazioneRettifica` '
         'rispondono KO allo stesso controllo, prima della regola della mezzanotte.')
    voce(d, 'Prima della firma dell’ufficiale non serve.', 'Un atto depositato ma non firmato è '
         'ancora in lavorazione per SIPO: lo copre il ritorno ai dati già descritto dall’analisi '
         '(stato 0, nuova validazione dello stesso atto) [R1].')
    voce(d, 'Indirizzare lo strumento giusto.', 'Il messaggio del pulsante nascosto, o una pagina '
         'di aiuto, indica lo strumento ANSC secondo ciò che va corretto (tabella seguente). Gli '
         'strumenti con servizio cooperativo (R013) seguono lo stesso destino dell’annullamento: '
         'web app e riallineamento ora, formazione da SIPO dopo.')
    tabella(d, RETTIFICA_SCELTA, [2.0, 1.8, 1.0, 2.1])
    par(d, 'Resta la questione organizzativa più pesante: oggi a Roma un atto si corregge fino '
           'alla mezzanotte, con ANSC la finestra si chiude alla firma dell’ufficiale [R3]. È '
           'una decisione dello stato civile, non del software (AR-05).')

    h(d, 2, 'Proposta di annotazione')
    par(d, 'Il modulo delle annotazioni di SIPO resta fuori da questo documento. Va però detto '
           'che per un atto formato in ANSC un’annotazione è un atto ANSC (casi d’uso `_998_*`, '
           'R013) e che le annotazioni generate da altri comuni arrivano come notifiche [R1]: il '
           'modulo, che oggi non chiama ANSC, andrà rivisto con lo stesso criterio (AR-07).')

    # ------------------------------------------------------------------- 6
    h(d, 1, 'Punti aperti')
    par(d, 'Nove questioni, accanto agli OP-80…OP-84 dell’analisi [R1]. AR-01 va chiusa prima '
           'di scrivere codice: senza il corpo delle procedure non si sa che cosa esse facciano '
           'oggi.')
    tabella(d, APERTI, [0.7, 4.9, 1.3])


def intesta(d):
    for r in d.tables[0].rows:
        if len(r.cells) < 2:
            continue
        etichetta = r.cells[0].text.strip().lower()
        valore = {'progetto': 'SIPO — Integrazione con ANSC',
                  'data consegna': DATA}.get(etichetta)
        if valore:
            D.riscrivi_cella(r.cells[1], valore)
    for fatto in D.frontespizio(d, '0.1', NOME):
        print('  ' + fatto)
    storia = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for r in list(storia.rows[1:]):
        if not any(c.text.strip() for c in r.cells):
            r._tr.getparent().remove(r._tr)
    D.storia(d, DATA, '0.1', 'Tutti',
             'Prima stesura, dai capitoli sulla cancellazione e sull’annullamento dell’analisi '
             'di integrazione v3.58, dalle specifiche ANSC e dal codice di SIPO. Le tre azioni e '
             'lo stato dell’atto in ANSC; come lavora oggi SIPO; che cosa prevede ANSC; dove '
             'inserirsi; nove punti aperti.')


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
