# -*- coding: utf-8 -*-
"""v0.5 di «ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC» (11/11/2026).

Dal FILE REALE della v0.4. Richiesta dell'utente: aggiungere al capitolo «L'attuale processo
di richiesta dei certificati» il modo di innestare la ricerca ANSC nel flusso dell'ufficio
certificati, con i passaggi ANSC nel dettaglio.

Fatti (R005 1.4.0, decodifiche, ansc-v1.yaml):
  * /consultazione/ansc/evento/sintetico/{version} (SCCPA) con CriteriRicercaEventoSintetico
    (idAnsc, idComunale, idEvento, idTipoEvento, idTipoContenuto, dataDa, dataA,
    idComuneRegistrazione) → modelEventoDTO[] di ModelEventoRidotto;
  * /consultazione/ansc/soggetto/sintetico/{version} (SCCPA) con CriteriRicercaSoggetto
    (idAnpr, idAnprUnico, idAnscSoggetto, codiceFiscale, cognome, nome, sesso,
    idComuneNascita o nomeComuneNascita+siglaProvinciaNascita, codiceStatoNascita,
    nomeStatoNascita, datanascita) → ModelEventoRidotto[];
  * ModelEventoRidotto: id, idAnsc, idTipoEvento, idtipocontenuto (ANSC_02), idUsecase,
    descrizioneCasoUso, stato (ANSC_11, esempio «BOZZA» = descrizione), flagsecretato,
    dataformazione…, numeroatto, intestatari (matrimonio: 0 sposo, 1 sposa), datiLingua,
    flagCertificatoSemplice, flagEstrattoPerRiassunto;
  * ansc-v1.yaml non ha letture per idAnsc né per persona → due operazioni proposte.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/certificazioni_v0_5.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import h, par, voce, tabella, figura   # noqa: E402
import diagrammi_certificazioni as DC   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.4.docx')
NOME = 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.5'
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


def S(v, n, a, e):
    D.sostituisci(d, v, n, attese=a, etichetta=e, fatti=fatti)


def mono(righe):
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)


TESTATA = ['  "testataRichiesta": {',
           '    "idComune": 8165,',
           '    "idOperazioneComune": "<identificativo univoco della chiamata>",',
           '    "dataOraRichiesta": "2026-11-11T10:15:00.000Z",',
           '    "nomeApplicativo": "SIPO", "versioneApplicativo": "<versione>",',
           '    "fornitoreApplicativo": "<fornitore>"',
           '  },',
           '  "datiPaginazione": { "numPagina": 1, "numRecordPagina": 20, '
           '"numRecordTotali": 0 },']


def innesto():
    h(d, 2, 'Come innestare la ricerca ANSC')
    par(d, 'La ricerca ANSC si innesta in cert-be all’aggiunta del certificato alla pratica, '
           'prima della scelta fra ANPR e modello locale. Le pagine non cambiano: si aggiunge un '
           'ramo che, per gli atti presenti in ANSC, prende il posto sia della verifica in ANPR '
           'sia della ricerca in locale, e che porta con sé fino all’emissione gli identificativi '
           'ANSC dell’atto e dell’intestatario. La figura mostra il flusso con l’innesto; i '
           'passi sono descritti uno per uno.')
    figura(d, DC.innesto_ansc(), 6.5,
           'Figura 6 — La ricerca ANSC innestata nel flusso dell’ufficio certificati.')
    tabella(d, [
        ['Momento', 'Oggi', 'Con l’innesto, per un atto presente in ANSC'],
        ['Aggiungi', 'ANPR 3002, oppure le interrogazioni di AttoRepository',
         'Passi 1-4: ricerca in ANSC e controlli; nessuna chiamata ad ANPR'],
        ['Pratica', 'Nel dato XML della pratica il contrassegno anpr (1 o 0)',
         'Passo 5: anche la fonte ANSC con idAnsc, idEvento e intestatario.id'],
        ['Anteprima', 'PDF con la filigrana, da ANPR o dal modello locale',
         'Passo 6: riepilogo dei dati letti in ANSC, senza PDF'],
        ['Emetti', 'ANPR 6001 o modello locale; PDF in CERTIFICATI',
         'Passo 6: nuova lettura in ANSC, poi R002; PDF in CERTIFICATI e ANSC_CERTIFICATO'],
    ], [1.0, 2.5, 3.0])

    h(d, 3, 'Passo 1 — Quali certificati entrano nella ricerca')
    par(d, 'Solo le voci di CONF_CERTIFICATO che corrispondono a un tipo di R002, elencate in '
           '«Dalla scelta allo sportello al tipo di R002»: certificati di nascita, matrimonio, '
           'unione civile e morte, estratti e copie integrali. Le altre voci dell’area «Stato '
           'Civile» (diritti politici, esistenza in vita, certificati storici…) seguono il flusso '
           'di oggi. Per nascita, matrimonio e morte, che oggi passano da ANPR, l’innesto vale se '
           'si decide di emetterli da ANSC (CE-15); altrimenti la ricerca riguarda estratti, copie '
           'integrali e le voci prodotte in locale.')

    h(d, 3, 'Passo 2 — L’atto della persona e il suo identificativo ANSC')
    par(d, 'cert-be raggiunge l’atto della persona con le stesse catene del ramo locale '
           '(SOGGETTO → NASCITA, MORTE, MATRIMONIO o UNIONECIVILE → ATTO), così che aggiunta ed '
           'emissione partano dallo stesso atto (CE-20), e legge `ANAG_USR.ATTO.ID_ATTO_ANSC`. Se '
           'è valorizzato si cerca per identificativo (passo 3a); se non lo è, l’atto è del '
           'registro tradizionale oppure SIPO non ne conosce l’identificativo, e si può cercare '
           'per persona (passo 3b).')

    h(d, 3, 'Passo 3a — Ricerca per identificativo')
    par(d, 'È la ricerca ordinaria. Il concentratore chiama la consultazione sintetica '
           'dell’evento [A11], aperta anche al permesso di consultazione parziale SCCPA:')
    mono(['POST https://anscservicepre.anpr.interno.it/services/service/ricerca/'
          'consultazione/ansc/evento/sintetico/1', '{'] + TESTATA +
         ['  "criteriRicercaEvento": { "idAnsc": "<ANAG_USR.ATTO.ID_ATTO_ANSC>" }', '}'])
    par(d, 'La risposta porta l’elenco `modelEventoDTO`, che per un identificativo nazionale '
           'contiene un evento solo. Un esempio dei campi che servono, con valori di '
           'fantasia:')
    mono(['{',
          '  "testataRisposta": { "idOperazione": "<id ANSC>", "idEsito": 0, … },',
          '  "modelEventoDTO": [ {',
          '    "id": "256343",',
          '    "idAnsc": "<idAnsc>",',
          '    "idTipoEvento": "1",  "idtipocontenuto": "1",',
          '    "idUsecase": "11111000",  "descrizioneCasoUso": "<descrizione>",',
          '    "stato": "FIRMATO DA USC",  "flagsecretato": "0",',
          '    "dataformazione": "<data>",  "numeroatto": "<numero comunale>",',
          '    "nomeComuneRegistrazione": "ROMA",',
          '    "intestatari": [ { "id": "434703", "codiceFiscale": "<CF>", '
          '"idANPR": "<id unico>", … } ],',
          '    "flagCertificatoSemplice": null,  "flagEstrattoPerRiassunto": null',
          '  } ]',
          '}'])
    tabella(d, [
        ['Campo', 'Che cosa se ne fa'],
        ['id', 'È l’idEvento che R002 chiede; si conserva nella pratica.'],
        ['intestatari[].id', 'È l’intestatario.id di R002, dopo aver riconosciuto la persona '
         '(passo 4).'],
        ['idTipoEvento, idtipocontenuto', 'Controllo di coerenza con la voce richiesta.'],
        ['stato, flagsecretato', 'Controllo di certificabilità.'],
        ['idUsecase, flagCertificatoSemplice, flagEstrattoPerRiassunto', 'Tipi emissibili per '
         'gli atti con caso d’uso di servizio.'],
        ['descrizioneCasoUso, dataformazione, numeroatto, nomeComuneRegistrazione',
         'Riepilogo mostrato all’operatore al posto dell’anteprima.'],
        ['datiLingua', 'Solo informativo: Roma non è un comune multilingua.'],
    ], [2.6, 3.9])

    h(d, 3, 'Passo 3b — Ricerca per persona')
    par(d, 'Serve quando l’atto c’è in ANSC ma SIPO non ne conosce l’identificativo: un atto '
           'formato da un altro comune per una persona dell’anagrafe di Roma, oppure un atto '
           'formato a Roma il cui identificativo non è stato riportato in `ANAG_USR.ATTO` '
           '(OP-29 di [R1]). Se attivarla è una scelta (CE-24). Il concentratore chiama la '
           'consultazione sintetica per soggetto [A11], anch’essa aperta al permesso SCCPA, con '
           'il criterio più forte disponibile:')
    tabella(d, [
        ['Ordine', 'Criterio di R005', 'Da dove lo prende SIPO'],
        ['1', 'idAnprUnico', 'ANAG_USR.SOGGETTO.ID_UNICO_NAZIONALE'],
        ['2', 'idAnpr', 'ANAG_USR.SOGGETTO.ID_SCHEDA_ANPR'],
        ['3', 'idAnscSoggetto', 'ANSC_SOGGETTO_IDENTIFICATIVI, se la persona vi compare [R1]'],
        ['4', 'codiceFiscale con cognome, nome, sesso, datanascita e luogo di nascita '
         '(idComuneNascita, oppure nomeComuneNascita e siglaProvinciaNascita; per i nati '
         'all’estero codiceStatoNascita)', 'ANAG_USR.SOGGETTO e NASCITA'],
    ], [0.7, 3.3, 2.5])
    mono(['POST https://anscservicepre.anpr.interno.it/services/service/ricerca/'
          'consultazione/ansc/soggetto/sintetico/1', '{'] + TESTATA +
         ['  "criteriRicercaSoggetto": { "idAnprUnico": "<ID_UNICO_NAZIONALE>" }', '}'])
    par(d, 'La risposta è un elenco di `ModelEventoRidotto`, uno per evento della persona, '
           'paginato secondo `datiPaginazione`. Dall’elenco si tengono gli eventi pertinenti: '
           'idTipoEvento della voce richiesta, idtipocontenuto 1 (atto) o 3 (trascrizione), la '
           'persona fra gli intestatari. Se ne resta uno si usa; se ne restano più, per esempio due '
           'matrimoni, li sceglie l’operatore; se non ne resta nessuno, si segue il flusso di oggi. '
           'Il contratto non dice se l’elenco comprenda anche gli eventi in cui la persona compare '
           'in un ruolo diverso da intestatario, per esempio come genitore o dichiarante (CE-22): '
           'per questo il filtro sugli intestatari non è facoltativo.')

    h(d, 3, 'Passo 4 — I controlli sulla risposta')
    par(d, 'Si fanno su ogni evento trovato, al passo 3a o al 3b. Se uno non passa, la '
           'richiesta è respinta con il motivo. Non si ripiega sui dati di SIPO: per un atto '
           'che è in ANSC, i dati di SIPO possono non riportare annotazioni e correzioni.')
    tabella(d, [
        ['Controllo', 'Campo', 'Regola', 'Se non passa'],
        ['Evento trovato', 'modelEventoDTO', 'Per idAnsc, un evento solo',
         '«Atto non trovato in ANSC»: l’identificativo in SIPO va verificato.'],
        ['Tipo di contenuto', 'idtipocontenuto', '1 atto o 3 trascrizione (ANSC_02)',
         'Annotazioni e rifiuti non si certificano come atto.'],
        ['Tipo di evento', 'idTipoEvento', 'Quello della voce: 1 nascita, 2 morte, 3 '
         'matrimonio, 4 unione civile, 5 cittadinanza', 'L’atto non corrisponde al certificato '
         'richiesto.'],
        ['Intestatario', 'intestatari[]', 'La persona è fra gli intestatari: per codice '
         'fiscale, poi idANPR = ID_UNICO_NAZIONALE, poi idsoggettoanpr = ID_SCHEDA_ANPR. Nel '
         'matrimonio l’elemento 0 è lo sposo, l’1 la sposa', 'La persona non è intestataria '
         'dell’atto.'],
        ['Stato', 'stato (ANSC_11)', '5 FIRMATO DA USC (CE-03)', '3 annullato, 9 cancellato, '
         '10 inefficace: motivo esplicito. 1, 2, 4, 11: atto non ancora concluso.'],
        ['Segreto', 'flagsecretato', '«0»', 'Atto secretato: il trattamento non è dichiarato '
         '(CE-03).'],
        ['Tipo emissibile', 'idUsecase, flagCertificatoSemplice, flagEstrattoPerRiassunto',
         'Per i casi d’uso di servizio, tipo 1 e 2 solo con il flag a true; il tipo 3 sempre',
         'Il tipo di certificato non è emissibile per quell’atto.'],
    ], [1.1, 1.5, 2.1, 1.8])
    par(d, 'Lo stato arriva come descrizione: l’esempio del contratto è «BOZZA», non «1». Il '
           'confronto si fa sulla descrizione di ANSC_11 finché la preproduzione non mostra '
           'altro (CE-22).')

    h(d, 3, 'Passo 5 — Che cosa si registra nella pratica')
    par(d, 'Oggi la pratica annota nel suo dato XML se un certificato va chiesto ad ANPR '
           '(«anpr» a 1 o a 0). Accanto si registra la fonte ANSC con i tre identificativi che '
           'servono all’emissione: idAnsc, idEvento e intestatario.id, insieme alla data della '
           'lettura. All’emissione cert-be non ricalcola nulla: legge la fonte dalla pratica, '
           'come fa oggi con il contrassegno anpr.')

    h(d, 3, 'Passo 6 — Anteprima ed emissione')
    voce(d, 'Anteprima.', 'Mostra il riepilogo della lettura: caso d’uso, data di formazione, '
         'comune di registrazione, numero dell’atto, intestatari, stato e tipi emissibili. Non '
         'chiama R002, che emetterebbe un certificato (CE-18).')
    voce(d, 'Emetti.', 'Rilegge l’evento per idAnsc con la stessa consultazione del passo 3a e '
         'ripete i controlli del passo 4: fra l’aggiunta e l’emissione l’atto può essere stato '
         'annullato o annotato. Poi chiama R002 come descritto nel capitolo «R002 in dettaglio», '
         'conserva il PDF in CERTIFICATI.DOCUMENTO_CERTIFICATO e registra l’emissione in '
         'ANSC_CERTIFICATO.')

    h(d, 3, 'Sessione, permessi ed errori')
    voce(d, 'Sessione.', 'Ogni chiamata ad ANSC passa dal concentratore e richiede l’OTP di '
         'sessione dell’operatore. CertificatiWeb deve quindi mostrare nella testata lo stato '
         'dell’OTP e il pulsante per richiederlo, come le pagine del back-office.')
    voce(d, 'Permessi.', 'Per le due consultazioni sintetiche basta il permesso SCCPA; per il '
         'certificato semplice SCCSE, per estratti e copie integrali il permesso pieno. Gli '
         'operatori dell’ufficio certificati devono avere un’utenza ANSC e operare da una '
         'postazione registrata (CE-25).')
    tabella(d, [
        ['Risposta di R005', 'Passo 3a', 'Passo 3b'],
        ['200 con elenco vuoto', 'L’identificativo in SIPO non trova l’atto: segnalazione, '
         'nessun ripiego', 'Nessun evento in ANSC: flusso di oggi'],
        ['401, 403', 'Permesso ANSC dell’operatore insufficiente', 'Come a sinistra'],
        ['406001, 406002', 'OTP non valido o scaduto: nuovo codice e nuova lettura',
         'Come a sinistra'],
        ['400, 500', 'Errore: la lettura si può ripetere, perché non ha effetti',
         'Come a sinistra'],
    ], [1.6, 2.6, 2.3])
    par(d, 'È la differenza da tenere presente: una lettura con R005 si può ripetere senza '
           'conseguenze, un’emissione con R002 no.')

    h(d, 3, 'Le letture di ANSC nel concentratore')
    par(d, 'Il contratto del concentratore [R2] non ha oggi una lettura di ANSC per '
           'identificativo né per persona. L’innesto ne richiede due, che si aggiungono a quelle '
           'già proposte in «Le operazioni del concentratore»:')
    tabella(d, [
        ['Operazione proposta', 'Percorso', 'Servizio ANSC', 'Note'],
        ['leggiEventoAnsc', 'GET /ansc/v1/eventi-ansc/{idAnsc}',
         'R005 /consultazione/ansc/evento/sintetico', 'Passi 3a e 6.'],
        ['cercaEventiAnsc', 'POST /ansc/v1/eventi-ansc/ricerche',
         'R005 /consultazione/ansc/soggetto/sintetico', 'Passo 3b. POST perché i criteri sono '
         'dati personali e non devono stare nel percorso né nei parametri della richiesta.'],
    ], [1.5, 2.0, 1.7, 1.3])
    par(d, 'Le operazioni già proposte usano come chiave l’atto di SIPO (`/atti/{idAtto}`); '
           'nell’ufficio certificati l’atto noto è quello di ANAG_USR e la chiave naturale è '
           'idAnsc (CE-23).')


if __name__ == '__main__':
    S('Figura 7 — La sequenza', 'Figura 8 — La sequenza', 1, 'figura 7 → 8')
    S('Figura 6 — Dalla richiesta', 'Figura 7 — Dalla richiesta', 1, 'figura 6 → 7')
    innesta_prima(paragrafo('Come intervenire per permettere la visualizzazione',
                            'Heading 2')._p, innesto)
    fatti.append('sezione «Come innestare la ricerca ANSC» con la figura 6')

    S('servono sei operazioni nuove nel suo contratto', 'servono otto operazioni nuove nel suo '
      'contratto', 1, 'operazioni del concentratore: sei → otto')
    p = paragrafo('Il concentratore all-ansc-sipo è il solo componente')
    p.add_run(' Le due letture di ANSC usate dall’ufficio certificati sono descritte in «Come '
              'innestare la ricerca ANSC».')
    ops = tab('Operazione proposta', 'Percorso', 'Servizio ANSC', 'Effetti')
    D.clona_riga(ops, ('leggiEventoAnsc', 'GET /ansc/v1/eventi-ansc/{idAnsc}',
                       'R005 /consultazione/ansc/evento/sintetico', 'Nessuno.'))
    D.clona_riga(ops, ('cercaEventiAnsc', 'POST /ansc/v1/eventi-ansc/ricerche',
                       'R005 /consultazione/ansc/soggetto/sintetico', 'Nessuno.'))
    S('Le sei operazioni del capitolo precedente', 'Le otto operazioni proposte in «Le '
      'operazioni del concentratore»', 1, 'rinvio della tabella «Che cosa cambia in SIPO»')

    cambia = tab('Dove', 'Che cosa cambia')
    for r in cambia.rows:
        if r.cells[0].text == 'cert-be':
            D.riscrivi_cella(r.cells[1], 'All’aggiunta, per le voci d’atto: ricerca in ANSC per '
                             'identificativo o per persona, controlli e registrazione della '
                             'fonte ANSC nella pratica, al posto di ANPR e della ricerca locale; '
                             'all’emissione nuova lettura e R002; PDF in '
                             'CERTIFICATI.DOCUMENTO_CERTIFICATO.')
        elif r.cells[0].text.startswith('CertificatiWeb'):
            D.riscrivi_cella(r.cells[1], r.cells[1].text.rstrip('.') + '; nella testata lo '
                             'stato dell’OTP e il pulsante per richiederlo; la scelta fra più '
                             'eventi trovati con la ricerca per persona.')
    S('Il flusso di oggi è nella sezione precedente; la logica', 'Il flusso di oggi è nella '
      'sezione «Dall’intestatario all’atto: il flusso della ricerca», l’innesto della ricerca '
      'ANSC in «Come innestare la ricerca ANSC»; la logica', 1, 'rinvii alle due sezioni')

    ce = tab('#', 'Questione', 'A chi spetta')
    for riga in [
        ('CE-22', 'Consultazioni sintetiche di R005: se la ricerca per soggetto restituisca solo '
         'gli eventi di cui la persona è intestataria o anche quelli in cui compare in altri '
         'ruoli; se comprenda gli eventi di altri comuni; se lo stato arrivi come descrizione o '
         'come codice di ANSC_11. Da provare in preproduzione.', 'Presidio ANSC / Sogei'),
        ('CE-23', 'Chiave delle operazioni del concentratore usate dall’ufficio certificati: '
         'idAnsc invece dell’atto di SIPO, che lì è quello di ANAG_USR.',
         'Architettura'),
        ('CE-24', 'Se attivare la ricerca per persona per gli atti senza ID_ATTO_ANSC in '
         'ANAG_USR e, quando trova l’atto, se riportarne l’identificativo in ANAG_USR.ATTO '
         '(OP-29 di [R1]).', 'Ufficio di stato civile / Referenti SIPO'),
        ('CE-25', 'Operatori dell’ufficio certificati in ANSC: utenza, permessi (SCCPA, SCCSE o '
         'pieno), postazione registrata e codice OTP.', 'Ufficio di stato civile / Presidio '
         'ANSC'),
    ]:
        D.clona_riga(ce, riga)
    fatti.append('due operazioni del concentratore, righe aggiornate, CE-22…CE-25')

    for f in D.frontespizio(d, '0.5', NOME, DATA):
        fatti.append(f)
    D.storia(d, DATA, '0.5', 'L’attuale processo di richiesta dei certificati · Le operazioni '
             'del concentratore · Che cosa cambia in SIPO · Punti aperti',
             'Nuova sezione su come innestare la ricerca ANSC nell’ufficio certificati: passi '
             'ANSC nel dettaglio (consultazioni sintetiche R005 per identificativo e per '
             'persona, controlli, registrazione nella pratica, anteprima ed emissione), con '
             'figura; due operazioni del concentratore; CE-22…CE-25.')
    d.save(OUT)
    for f in fatti:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tb, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tb, fig))
