# -*- coding: utf-8 -*-
"""v0.3 di «ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC» (11/11/2026).

Si modifica il FILE REALE della v0.2, rivista a mano dall'utente (capitolo «L'attuale
processo di richiesta dei certificati» con le schermate di CertificatiWeb, registro
ESTRATTI_DOWNLOAD_LOG). Richiesta dell'utente: verificare le incongruenze, curare
l'impaginazione delle immagini, analizzare in dettaglio l'uso di R002 (metodo, risultato,
buone pratiche) per trasporre il certificato ANSC nelle schermate di SIPO.

Fatti verificati l'11/11 (contratti, payload di prova, note, codice):
  * R002: la risposta è il PDF/A in base64 + idCertificato + datavalidita, nessun dato
    strutturato del certificato; nessuna anteprima del certificato fra i servizi cooperativi
    (la web app la mostra, R010 è l'anteprima dell'ATTO); version = major ANSC («1»).
  * R005 /consultazione/ansc/evento/sintetico (permesso SCCPA) restituisce
    ModelEventoRidotto: id, idAnsc, stato, intestatari, flagCertificatoSemplice,
    flagEstrattoPerRiassunto, flagsecretato, datiLingua.
  * Ufficio certificati (cert-web/cert-be): area «Stato Civile» = CONF_CERTIFICATO.
    FLG_ANAG_SC='S'; 5/6/25/3 da ANPR 6001 (R_CONF_CERT_ANPR) o in locale; estratti
    (17, 19-24, 26) e copie integrali (27-31) «non ancora gestito»
    (CertificatiController:765-767); il modello locale stampa ID_ATTO_ANSC se manca il
    numero d'atto (DocCertificatoSempliceComuneRoma:133, :153). «Stampa» produce la lista
    dei certificati della pratica, l'anteprima è il pulsante di riga.
Impaginazione: le due schermate della pagina «Nuovo certificato a sportello» erano una
flottante dietro al testo e una deformata (588x742 px a 2,74x2,52 in) con sei righe vuote
di spaziatura → tabella a due celle senza bordi; testo prima di ogni figura, didascalie
numerate; nome e codice fiscale coperti nelle schermate (img/certificazioni/sportello_*).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/certificazioni_v0_3.py
"""
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import h, par, voce, tabella, figura   # noqa: E402
import diagrammi_certificazioni as DC   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.2.docx')
NOME = 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.3'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '11/11/2026'
IMG = os.path.join(QUI, 'img', 'certificazioni')

d = docx.Document(SRC)
body = d.element.body
fatti = []


# ------------------------------------------------------------------ primitive locali
def nuovi_elementi(scrivi):
    sect = body.find(qn('w:sectPr'))
    prima = list(body.iterchildren())      # si tengono gli elementi, non i loro id
    visti = set(prima)
    scrivi()
    return [ch for ch in body.iterchildren() if ch not in visti and ch is not sect]


def innesta_dopo(dopo, scrivi):
    nuovi = nuovi_elementi(scrivi)
    for ch in reversed(nuovi):
        dopo.addnext(ch)
    return nuovi


def innesta_prima(prima, scrivi):
    nuovi = nuovi_elementi(scrivi)
    for ch in nuovi:
        prima.addprevious(ch)
    return nuovi


def paragrafo(inizio, stile=None):
    pp = [p for p in d.paragraphs if p.text.startswith(inizio)
          and (stile is None or p.style.name == stile)]
    if len(pp) != 1:
        raise SystemExit('paragrafo non univoco (%d): %s' % (len(pp), inizio))
    return pp[0]


def corpo(p, nuovo, teste=1):
    """Riscrive il corpo di una voce e conserva le prime `teste` run (la testa in grassetto)."""
    rr = p.runs
    rr[teste].text = nuovo
    for r in rr[teste + 1:]:
        r._r.getparent().remove(r._r)


def tab(*intest):
    for t in d.tables:
        testa = [c.text.strip() for c in t.rows[0].cells]
        if testa[:len(intest)] == list(intest):
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


def coppia_immagini(sx, dx, larg=3.1):
    """Due schermate affiancate in una tabella senza bordi, ciascuna nelle proporzioni vere."""
    t = d.add_table(rows=1, cols=2)
    tblPr = t._tbl.tblPr
    bordi = OxmlElement('w:tblBorders')
    for lato in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        b = OxmlElement('w:' + lato)
        b.set(qn('w:val'), 'nil')
        bordi.append(b)
    tblPr.append(bordi)
    for cella, png in zip(t.rows[0].cells, (sx, dx)):
        cella.width = Inches(larg + 0.1)
        p = cella.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(png, width=Inches(larg))
    return t


def didascalia(t):
    figura_p = d.add_paragraph()
    r = figura_p.add_run(t)
    r.italic = True
    r.font.size = Pt(9)


# ------------------------------------------------------------------ 1. il processo attuale
def processo_attuale():
    h1 = paragrafo('L’attuale Processo di richiesta', 'Heading 1')
    D.testo_di(h1, 'L’attuale processo di richiesta dei certificati')
    h2 = paragrafo('Come intervenire per permettere la visualizzazione', 'Heading 2')
    D.testo_di(h2, 'Come intervenire per permettere la visualizzazione di un atto ANSC')
    h_fonte = paragrafo('La fonte del documento', 'Heading 1')

    # via il contenuto della v0.2 fra le intestazioni (immagini, righe vuote, testo)
    def fra(a, b):
        out, el = [], a._p.getnext()
        while el is not None and el is not b._p:
            out.append(el)
            el = el.getnext()
        return out
    for el in fra(h1, h2) + fra(h2, h_fonte):
        if D.ha_commenti(el):
            raise SystemExit('elemento con commento: non si cancella')
        body.remove(el)

    def scrivi_processo():
        par(d, 'I certificati sugli atti di stato civile si chiedono anche dall’ufficio '
               'certificati di SIPO (CertificatiWeb e cert-be), nella stessa pagina dei '
               'certificati anagrafici [S4]. Il processo comincia dal menu principale: alla '
               'voce «Certificati» dei Municipi si apre la gestione dei certificati, senza '
               'distinzione fra anagrafe e stato civile.')
        figura(d, os.path.join(IMG, 'sportello_menu.png'), 6.0,
               'Figura 1 — Il menu principale: la voce «Certificati» dei Municipi.')
        par(d, 'Nella pagina «Nuovo certificato a sportello» si indicano intestatario e '
               'richiedente e, in fondo, si sceglie il certificato: il tipo (semplice o '
               'contestuale), l’area («Anagrafici» o «Stato Civile»), il certificato, il numero '
               'di copie e la finalità d’uso.')
        coppia_immagini(os.path.join(IMG, 'sportello_form_a.png'),
                        os.path.join(IMG, 'sportello_form_b.png'))
        didascalia('Figura 2 — La pagina «Nuovo certificato a sportello»: intestatario e '
                   'richiedente a sinistra; residenza, documento e scelta del certificato a '
                   'destra.')
        par(d, 'Nel particolare, l’area che permette la scelta è la seguente:')
        figura(d, os.path.join(IMG, 'sportello_scelta.png'), 5.0,
               'Figura 3 — La scelta del certificato: tipo, area e certificato.')
        par(d, 'Con l’area «Stato Civile» l’elenco viene da `ANAG_USR.CONF_CERTIFICATO`, '
               "filtrato sulla colonna `FLG_ANAG_SC = 'S'` (cert-be, ConfCertificatoController, "
               'righe 28-70). I pulsanti fanno cose diverse:')
        voce(d, 'Aggiungi.', 'Registra la richiesta nella pratica (PRATICA_CERTIFICATI, '
             'CERTIFICATI) e verifica che il certificato si possa produrre.')
        voce(d, 'Anteprima.', 'Sulla riga del certificato aggiunto: restituisce il PDF con la '
             'filigrana «ANTEPRIMA».')
        voce(d, 'Stampa.', 'Stampa il riepilogo della pratica, cioè la lista dei certificati '
             'richiesti; non stampa il certificato.')
        voce(d, 'Emissione.', 'Il certificato definitivo si emette dal dettaglio della pratica '
             'e si conserva in `CERTIFICATI.DOCUMENTO_CERTIFICATO`.')
        figura(d, os.path.join(IMG, 'sportello_anteprima.png'), 4.0,
               'Figura 4 — L’anteprima di un certificato prodotto oggi da SIPO (certificato di '
               'esistenza in vita, area «Stato Civile»); i dati personali sono coperti.')

        h(d, 2, 'Come SIPO produce oggi i certificati dell’area «Stato Civile»')
        par(d, 'L’area «Stato Civile» comprende certificati d’atto e certificati che '
               'nascono dall’anagrafe. I primi passano da ANPR o da un modello locale; '
               'estratti e copie integrali sono in catalogo ma non vengono prodotti.')
        tabella(d, [
            ['Voci di CONF_CERTIFICATO', 'Come si producono oggi', 'Da quali dati'],
            ['5 Nascita, 6 Matrimonio, 25 Morte, 3 Cittadinanza',
             'ANPR, operazione 6001 (R_CONF_CERT_ANPR). Nascita, matrimonio e morte si '
             'producono in locale se la persona non è in ANPR e SIPO ne ha l’atto.',
             'Scheda ANPR; in locale ANAG_USR: SOGGETTO, NASCITA, MATRIMONIO, MORTE, ATTO.'],
            ['18 Nascita dei nati a Roma non residenti, 44 Unione civile, 63 Matrimonio',
             'In locale, modello Jasper «Certificato_semplice».', 'ANAG_USR, come sopra.'],
            ['7 e 9 Diritti politici, 13 Cittadinanza AIRE, 15 Esistenza in vita, 32-35 '
             'certificati storici', 'In locale, stesso modello.',
             'ANAG_USR. Non sono certificazioni di un atto di stato civile.'],
            ['17, 19-24, 26 Estratti di nascita, matrimonio, unione civile e morte',
             'Non prodotti: il ramo locale li respinge come «non ancora gestito» '
             '(CertificatiController, righe 765-767) e non hanno corrispondenza ANPR.', '—'],
            ['27-31 Copie integrali', 'Non prodotte, per la stessa ragione.', '—'],
        ], [2.0, 2.6, 1.9])
        voce(d, 'Il certificato è legato alla persona.', 'L’operatore indica l’intestatario; '
             'l’atto è quello che ANAG_USR collega alla persona (nascita, matrimonio, morte). '
             'Non si sceglie un atto.')
        voce(d, 'L’identificativo ANSC è già letto.', 'Il modello locale stampa '
             '`ATTO.ID_ATTO_ANSC` al posto del numero d’atto quando questo manca '
             '(DocCertificatoSempliceComuneRoma, righe 133 e 153). È il solo punto del '
             'percorso in cui ANSC compare.')
        voce(d, 'Anteprima ed emissione sono due chiamate distinte.', 'Verso ANPR l’anteprima è '
             'una richiesta 6001 con modalità di emissione «anteprima»; verso il modello '
             'locale è lo stesso documento con la filigrana.')
    innesta_dopo(h1._p, scrivi_processo)

    def scrivi_intervento():
        par(d, 'Dal punto di vista del flusso operativo della richiesta non cambia niente: '
               'stesse pagine, stessi pulsanti. Nell’impianto logico, quando il sistema cerca '
               'di recuperare le informazioni, verifica se l’atto della persona ha un '
               'identificativo ANSC: in `ANAG_USR.ATTO.ID_ATTO_ANSC`, che cert-be già legge, '
               'oppure in `ANSC_STATO_ATTO` per gli atti formati con il nuovo percorso.')
        par(d, 'Se l’identificativo è valorizzato si attiva il recupero da ANSC, che richiede '
               'l’OTP di sessione dell’operatore. La logica di instradamento è nel capitolo '
               '«La proposta di integrazione»; le chiamate, una per una, nel capitolo «R002 in '
               'dettaglio: come si ottiene il certificato da ANSC».')
        par(d, 'Le schermate restano le stesse, il documento no. ANSC restituisce un PDF/A già '
               'composto, con il proprio impianto grafico, il sigillo del Ministero e il QR di '
               'verifica: SIPO lo mostra e lo stampa così com’è, senza ricomporlo con i propri '
               'modelli. Cambiano due comportamenti:')
        voce(d, 'L’anteprima.', 'Per un atto ANSC il pulsante «Anteprima» non può produrre un '
             'PDF, perché i servizi cooperativi non offrono l’anteprima del certificato: ogni '
             'chiamata a R002 emette un certificato.')
        voce(d, 'La firma.', 'Per estratti e copie integrali l’emissione chiede le credenziali di '
             'firma remota dell’ufficiale.')
        par(d, 'Estratti e copie integrali, che l’ufficio certificati ha in catalogo ma non '
               'produce, diventano emissibili per gli atti con identificativo ANSC.')
    innesta_dopo(h2._p, scrivi_intervento)
    fatti.append('capitolo «L’attuale processo»: testo e figure 1-4 ricomposti')


# ------------------------------------------------------------------ 2. capitolo R002
def capitolo_r002():
    h(d, 1, 'R002 in dettaglio: come si ottiene il certificato da ANSC')
    par(d, 'Il capitolo risponde a tre domande: quale operazione chiamare, che cosa aspettarsi '
           'in risposta, quali buone pratiche sono documentate. Le fonti sono il contratto [A1], '
           'il payload di prova [A8], la nota sulla retrocompatibilità [A9], i codici d’errore '
           '[A10], la consultazione [A11], le guide [A3] [A4] e il changelog [A5].')
    voce(d, 'La risposta è un documento, non dati.', 'R002 restituisce il certificato già '
         'composto, un PDF/A in base64, con il suo identificativo e la data di validità. Non '
         'restituisce i dati del certificato in forma strutturata. Per mostrare nelle schermate '
         'di SIPO i dati dell’atto si usa la consultazione R005; per mostrare il certificato si '
         'visualizza il PDF.')
    voce(d, 'Ogni chiamata è un’emissione.', 'Non esiste fra i servizi cooperativi '
         'un’anteprima del certificato: la web app la mostra prima del pulsante «Ottieni '
         'certificazione» [A3], ma il servizio corrispondente non è pubblicato. R010 produce '
         'l’anteprima dell’atto, non del certificato, e chiede l’intero modello evento.')

    h(d, 2, 'Quale operazione chiamare')
    tabella(d, [
        ['Documento', 'Operazione', 'Permesso ANSC', 'Firma'],
        ['Certificato semplice (idTipoCertificato 1)', 'POST …/certificazione/'
         'certificato-semplice/1', 'Pieno oppure SCCSE',
         'Nessuna: parametriFirma non va inviato.'],
        ['Estratto per riassunto (2)', 'POST …/certificazione/certificato/1',
         'Pieno; non accessibile con SCCSE', 'parametriFirma obbligatorio.'],
        ['Estratto per copia integrale (3), anche semplificato',
         'POST …/certificazione/certificato/1', 'Pieno; non accessibile con SCCSE',
         'parametriFirma obbligatorio.'],
    ], [2.0, 2.2, 1.3, 1.0])
    voce(d, 'Indirizzi.', 'Produzione https://anscservice.anpr.interno.it/services/service/'
         'certificazione; preproduzione https://anscservicepre.anpr.interno.it/services/'
         'service/certificazione [A1].')
    voce(d, 'Versione nel percorso.', 'Il segmento {version} è la versione maggiore di ANSC, '
         'oggi «1», e il servizio controlla che coincida [A9]. Non è la versione del contratto '
         '(1.49.0).')
    voce(d, 'Metodo e formato.', 'POST con corpo JSON anche se l’operazione non modifica '
         'l’atto; la risposta è JSON.')
    voce(d, 'Chi chiama.', 'Solo il concentratore all-ansc-sipo, con il token JWT e la firma '
         'JWS dell’impianto [R1]. L’identità dell’operatore viene dal token, insieme all’OTP '
         'della sessione; il corpo non la porta.')
    voce(d, 'Quale delle due per il certificato semplice.', 'Il contratto le dichiara con lo '
         'stesso corpo; la seconda è aperta anche al permesso SCCSE (changelog 1.51.0). Per il '
         'tipo 1 conviene usare sempre /certificato-semplice, che funziona con entrambi i '
         'permessi.')

    h(d, 2, 'Che cosa serve prima: la consultazione dell’atto')
    par(d, 'Oltre a idAnsc, la richiesta porta l’identificativo interno dell’evento (idEvento) '
           'e l’intestatario come soggetto ANSC; il payload di prova li valorizza entrambi, con '
           'l’intestatario indicato dal solo id [A8]. SIPO conosce l’idAnsc, non gli altri due. '
           'Si ottengono dalla consultazione sintetica R005 '
           '`/consultazione/ansc/evento/sintetico/1` con `criteriRicercaEvento.idAnsc` [A11], '
           'aperta anche al permesso di consultazione parziale SCCPA. La stessa risposta, '
           '`ModelEventoRidotto`, porta i dati per i controlli da fare prima di emettere:')
    tabella(d, [
        ['Campo della risposta', 'A che cosa serve'],
        ['id', 'È l’idEvento della richiesta R002.'],
        ['intestatari[].id', 'È intestatario.id. Per gli atti con due intestatari (matrimonio, '
         'unione civile) si sceglie quello per cui si chiede il certificato.'],
        ['idTipoEvento', 'È l’idTipoEvento della richiesta (ANSC_01: 1 nascita, 2 morte, '
         '3 matrimonio, 4 unione civile, 5 cittadinanza); dice anche se paternità e maternità '
         'o uso matrimonio hanno senso.'],
        ['stato', 'Se l’atto è in uno stato che consente la certificazione (CE-03).'],
        ['idUsecase, flagCertificatoSemplice, flagEstrattoPerRiassunto', 'Per i casi d’uso di '
         'servizio dice quali tipi sono emissibili; la copia integrale lo è sempre [A4].'],
        ['flagsecretato', 'Atto secretato: le fonti non dicono come la certificazione lo '
         'tratti (CE-03).'],
        ['datiLingua', 'Se l’atto è formato anche in altre lingue; Roma non è un comune '
         'multilingua [A12].'],
    ], [2.2, 4.3])
    par(d, 'Se l’intestatario ha già l’identificativo ANSC in `ANSC_SOGGETTO_IDENTIFICATIVI` '
           '[R1] il dato può venire da lì, ma la consultazione serve comunque per idEvento e per '
           'i controlli.')

    h(d, 2, 'La richiesta')
    tabella(d, [
        ['Campo', 'Contenuto', 'Da dove lo prende SIPO', 'Note'],
        ['testataRichiesta', 'idComune, idOperazioneComune, dataOraRichiesta (date-time), '
         'nomeApplicativo, versioneApplicativo, fornitoreApplicativo', 'Concentratore',
         'idOperazioneComune univoco per chiamata e registrato nell’audit: è il riferimento '
         'per ritrovare la chiamata presso ANSC.'],
        ['idAnsc', 'Identificativo nazionale dell’atto', 'ANAG_USR.ATTO.ID_ATTO_ANSC o '
         'ANSC_STATO_ATTO.ID_ANSC', ''],
        ['idEvento', 'Identificativo interno dell’evento', 'R005 sintetica, campo id', ''],
        ['intestatario', 'ModelSoggetto; basta id', 'R005 sintetica, intestatari[].id',
         'ANSC verifica che l’intestatario appartenga all’evento.'],
        ['richiedente', 'ModelSoggetto: codice fiscale, cognome, nome, sesso, nascita, '
         'residenza, nazionalità', 'Richiedente della pratica', 'Il contratto non lo rende '
         'obbligatorio; il payload di prova lo valorizza. È un dato personale: si invia solo '
         'quanto serve.'],
        ['enteRichiedente', 'ModelEnteEstero', 'Quando richiede un ente terzo', ''],
        ['idTipoCertificato', '1, 2 o 3', 'Voce di CONF_CERTIFICATO (tabella più avanti)',
         'I valori sono scritti solo nella descrizione del contratto.'],
        ['idTipoEvento', 'ANSC_01', 'R005 sintetica', ''],
        ['conPaternitaMaternita', 'boolean', 'Voce con paternità e maternità', 'Solo nascita.'],
        ['usoMatrimonio', 'boolean', 'Finalità d’uso', 'Solo certificati semplici e riassunti '
         'di nascita e matrimonio: altrimenti ANSC rifiuta («Tipo di certificato non valido con '
         'uso matrimonio», changelog 1.34.0).'],
        ['idTipoUso', 'ANSC_113, sei valori', 'Finalità d’uso scelta', 'Il raccordo con le '
         'finalità di SIPO è da definire (CE-05).'],
        ['codiciLingueCertificato', 'Elenco di codici lingua', 'Non si invia',
         'Solo per i comuni abilitati a lingue aggiuntive [A12].'],
        ['flagSemplificato', 'boolean', 'Scelta dell’operatore', 'Solo tipo 3: copia '
         'integrale senza metadati.'],
        ['parametriFirma', 'idTipoFirma, idModalitaInput, inputFirma1-3',
         'Finestra delle credenziali dell’ufficiale', 'Solo tipi 2 e 3.'],
    ], [1.4, 1.7, 1.6, 1.8])
    par(d, 'I parametri di firma, uno per uno [A1]:')
    voce(d, 'idTipoFirma.', '«1», l’unico valore di ANSC_28 («Primo lotto firma ANSC»). Il '
         'contratto avverte che i parametri obbligatori possono cambiare con il fornitore della '
         'firma remota.')
    voce(d, 'idModalitaInput.', '«2», cioè base64: «1», in chiaro, non è accettato in '
         'produzione.')
    voce(d, 'inputFirma1, inputFirma2, inputFirma3.', 'Nome utente della firma remota, per '
         'intero e con l’eventuale dominio; password; OTP di firma. Non si registrano né '
         'nell’audit né nei log.')
    par(d, 'Un esempio di richiesta di estratto per riassunto, ricavato dal payload di prova '
           '[A8] con i parametri di firma che il contratto oggi richiede; i valori fra parentesi '
           'angolari sono segnaposto:')
    mono([
        'POST https://anscservicepre.anpr.interno.it/services/service/certificazione/certificato/1',
        '{',
        '  "testataRichiesta": {',
        '    "idComune": 8165,',
        '    "idOperazioneComune": "<identificativo univoco della chiamata>",',
        '    "dataOraRichiesta": "2026-11-11T10:15:00.000Z",',
        '    "nomeApplicativo": "SIPO",',
        '    "versioneApplicativo": "<versione>",',
        '    "fornitoreApplicativo": "<fornitore>"',
        '  },',
        '  "idAnsc": "<idAnsc dell’atto>",',
        '  "idEvento": "<id da R005 sintetica>",',
        '  "intestatario": { "id": "<intestatari[].id da R005 sintetica>" },',
        '  "richiedente": { "codiceFiscale": "<CF>", "cognome": "<…>", "nome": "<…>" },',
        '  "idTipoCertificato": "2",',
        '  "idTipoEvento": "1",',
        '  "conPaternitaMaternita": true,',
        '  "idTipoUso": "1",',
        '  "parametriFirma": {',
        '    "idTipoFirma": "1",',
        '    "idModalitaInput": "2",',
        '    "inputFirma1": "<utente in base64>",',
        '    "inputFirma2": "<password in base64>",',
        '    "inputFirma3": "<OTP di firma in base64>"',
        '  }',
        '}',
    ])

    h(d, 2, 'Dalla scelta allo sportello al tipo di R002')
    par(d, 'Proposta di corrispondenza fra le voci dell’area «Stato Civile» e i parametri di '
           'R002; le voci senza un tipo evidente sono in CE-16.')
    tabella(d, [
        ['Voci di CONF_CERTIFICATO', 'Operazione e tipo', 'Parametri'],
        ['5 Nascita, 18 Nascita (non residenti)', '/certificato-semplice, tipo 1',
         'idTipoEvento 1. Oggi la 5 va ad ANPR (CE-15).'],
        ['6 e 63 Matrimonio', '/certificato-semplice, tipo 1', 'idTipoEvento 3 (CE-15).'],
        ['44 Unione civile', '/certificato-semplice, tipo 1', 'idTipoEvento 4.'],
        ['25 Morte', '/certificato-semplice, tipo 1', 'idTipoEvento 2 (CE-15).'],
        ['19 Estratto di nascita con paternità e maternità', '/certificato, tipo 2',
         'idTipoEvento 1, conPaternitaMaternita.'],
        ['17 Estratto di nascita per uso', '/certificato, tipo 2', 'idTipoEvento 1, '
         'idTipoUso o usoMatrimonio secondo l’uso (CE-16).'],
        ['20 Estratto matrimonio, 21 unione civile, 24 morte', '/certificato, tipo 2',
         'idTipoEvento 3, 4, 2.'],
        ['22, 23, 26 «Estratto certificato» di matrimonio, unione civile, morte',
         'Tipo 1 o 2', 'Da decidere (CE-16).'],
        ['27-31 Copie integrali', '/certificato, tipo 3', 'idTipoEvento secondo l’atto (30 = '
         'cittadinanza, 5); flagSemplificato a scelta.'],
        ['3, 7, 9, 13, 15, 32-35', 'Nessuno', 'Non sono certificazioni di un atto: restano '
         'come sono.'],
    ], [2.4, 1.7, 2.4])

    h(d, 2, 'La risposta')
    tabella(d, [
        ['Campo', 'Contenuto', 'Uso in SIPO'],
        ['testataRisposta.idOperazione', 'Identificativo ANSC dell’operazione',
         'Audit, accanto a idOperazioneComune.'],
        ['testataRisposta.idEsito', 'Esito numerico', 'Audit.'],
        ['contenuto', 'Il certificato: PDF/A in base64', 'Si decodifica, si mostra e si '
         'conserva in CERTIFICATI.DOCUMENTO_CERTIFICATO.'],
        ['nomeFile', '<idCertificato>.pdf (changelog 1.17.0)', 'Nome del file scaricato.'],
        ['tipoFile', 'ANSC_10: 1 PDF, 2 JPG, 3 TIF, 4 P7M', 'Atteso 1; l’esempio del contratto '
         'riporta «3» (CE-19).'],
        ['tipoContenutoFile', 'Nessuna decodifica dichiarata', 'Non si usa.'],
        ['idCertificato', 'Identificativo del certificato', 'ANSC_CERTIFICATO.'
         'ID_CERTIFICATO_ANSC.'],
        ['datavalidita', 'Data di fine validità (changelog 1.38.0)', 'ANSC_CERTIFICATO.'
         'DATA_VALIDITA; il QR è verificabile per sei mesi dall’emissione.'],
        ['codice, descrizione, tipologia', 'Esito in chiaro: «200», «success»; tipologia '
         '«errore»', 'Messaggio all’operatore.'],
        ['errors, warnings, infos, success', 'ServiceMessage: code, severity, text',
         'Il text si mostra all’operatore così come ANSC lo restituisce.'],
    ], [1.9, 2.3, 2.3])
    par(d, 'Il contratto dichiara le risposte HTTP 200, 403 e 404 [A1]. Dal file dei codici '
           'd’errore [A10], quelli che interessano la certificazione:')
    tabella(d, [
        ['HTTP', 'Codice', 'Significato', 'Che cosa fa SIPO'],
        ['400', '400001-400003', 'Dati mancanti o non corretti', 'Corregge la richiesta; non '
         'la ripete uguale.'],
        ['401', '401001, 401002', 'Utente non autorizzato', 'Permesso ANSC dell’operatore '
         '(SCCSE o pieno).'],
        ['401', '401003', 'Evento non valido', 'Stato dell’atto o rettifica di annullamento: '
         'messaggio all’operatore.'],
        ['404', '404001', 'Dati non presenti', 'Atto o intestatario non trovati: verificare '
         'idAnsc, idEvento e intestatario.'],
        ['406', '406001, 406002', 'OTP non valido o scaduto', 'Nuovo codice di sessione e nuova '
         'richiesta.'],
        ['406', '406003', 'Evento non trovato', 'Come 404001.'],
        ['406', '406004', 'Firma non avvenuta', 'Credenziali di firma da reinserire. Se in '
         'questo caso il certificato non sia stato emesso è [DA VERIFICARE].'],
        ['500', '500', 'Errore interno', 'Esito incerto: non si ripete alla cieca (CE-08).'],
    ], [0.6, 1.2, 1.8, 2.9])

    h(d, 2, 'Come si trasporta nelle schermate di SIPO')
    par(d, 'Le pagine dell’ufficio certificati restano quelle di oggi; cambia ciò che accade '
           'dietro i pulsanti quando l’atto della persona ha un identificativo ANSC.')
    figura(d, DC.sequenza_r002(), 6.5,
           'Figura 6 — La sequenza delle chiamate per un certificato ANSC: consultazione '
           'all’aggiunta, una sola emissione alla fine.')
    voce(d, 'Aggiungi.', 'cert-be riconosce l’atto ANSC e lo consulta con R005: a questo passo '
         'non si emette nulla. Oggi «Aggiungi» chiama ANPR in modalità di emissione per '
         'verificare il certificato; con R002 non si può fare, perché ogni chiamata emette un '
         'certificato.')
    voce(d, 'Anteprima.', 'Per un atto ANSC mostra il riepilogo letto con R005 (tipo di atto, '
         'intestatario, stato, tipi emissibili), non un PDF (CE-18).')
    voce(d, 'Emetti.', 'Una sola chiamata a R002. Per estratti e copie integrali si apre prima '
         'la finestra delle credenziali di firma. Il PDF ricevuto si conserva in '
         'CERTIFICATI.DOCUMENTO_CERTIFICATO, come oggi, e si registra in ANSC_CERTIFICATO.')
    voce(d, 'Visualizzazione.', 'Il PDF arriva al browser come oggi, in download '
         '(application/pdf). Non si ricompone né si rimpagina: sigillo, QR e firma valgono sul '
         'file così come ANSC lo ha prodotto.')
    voce(d, 'Ristampa.', 'Si ristampa il PDF conservato; una nuova chiamata a R002 sarebbe un '
         'nuovo certificato.')

    h(d, 2, 'Le buone pratiche')
    par(d, 'Documentate dalle fonti ANSC:')
    tabella(d, [
        ['Pratica', 'Fonte'],
        ['Usare /certificato-semplice per il tipo 1 e /certificato per i tipi 2 e 3.',
         '[A1]; changelog 1.51.0'],
        ['Non inviare parametriFirma per il certificato semplice; inviarli sempre per '
         'riassunto e copia integrale.', '[A1]; changelog 1.49.0'],
        ['Credenziali di firma in base64 (idModalitaInput = 2): «in chiaro» non è accettato in '
         'produzione.', '[A1]'],
        ['Nome utente della firma remota per intero, con il dominio.', '[A1]'],
        ['Nel percorso la versione maggiore di ANSC, non quella del contratto.', '[A9]'],
        ['Lingue aggiuntive solo per i comuni abilitati, che devono richiederle per ottenerle.',
         '[A12]'],
        ['Certificato e riassunto riportano i dati già modificati dalle annotazioni, senza '
         'annotazione a margine; una rettifica di annullamento ne inibisce l’emissione; la '
         'copia integrale riporta le annotazioni.', '[A3] cap. 12'],
        ['Per gli atti con caso d’uso di servizio controllare i tipi emissibili; la copia '
         'integrale è sempre disponibile.', '[A4] § 3.3'],
        ['Dopo una nota tecnica i certificati riportano i dati corretti.', '[A4] § 3.5.6'],
        ['Il file si chiama come idCertificato; vale fino a datavalidita; il QR si verifica '
         'per sei mesi.', 'Changelog 1.17.0 e 1.38.0'],
    ], [4.9, 1.6])
    par(d, 'Non documentate dalle fonti; le propone questo documento:')
    voce(d, 'Una consultazione prima, un’emissione sola.', 'R005 sintetica per i dati e i '
         'controlli; R002 solo alla conferma dell’operatore.')
    voce(d, 'Nessun nuovo tentativo automatico.', 'ANSC non dichiara idempotenza e non offre '
         'un’operazione per sapere quali certificati ha emesso: ripetere dopo un errore 500 o '
         'una risposta mancata può produrre due certificati (CE-08). L’esito incerto si '
         'registra come DA_VERIFICARE e si mostra all’operatore.')
    voce(d, 'Un identificativo per chiamata.', 'idOperazioneComune univoco, registrato insieme '
         'a idOperazione restituito da ANSC.')
    voce(d, 'Il PDF si conserva in SIPO.', 'Nessuna operazione di R002 permette di riscaricare '
         'un certificato già emesso (CE-04).')
    voce(d, 'Il contenuto si controlla prima di mostrarlo.', 'Il file deve cominciare con '
         '«%PDF», qualunque sia il valore di tipoFile (CE-19).')
    voce(d, 'Audit minimo.', 'In ANSC_LOG_AUDIT non si conservano né il PDF né i parametri di '
         'firma; i dati del richiedente solo se l’ufficio decide di registrarli.')
    voce(d, 'Il messaggio di ANSC all’operatore.', 'In caso di rifiuto si mostra il text del '
         'ServiceMessage, non un errore generico: è da lì che l’operatore capisce, per esempio, '
         'che l’atto è annullato.')
    voce(d, 'Collaudo in preproduzione, tipo per tipo.', 'Il payload di prova è del 2023 [A8] '
         'e per la copia integrale non porta i parametri di firma che oggi servono: i casi vanno '
         'riprovati su atti veri in preproduzione (CE-01).')


# ------------------------------------------------------------------ 3. ritocchi puntuali
def ritocchi():
    # perimetro
    corpo(paragrafo('Solo lo stato civile.'),
          'Il documento tratta i certificati, gli estratti e le copie integrali che SIPO '
          'rilascia sugli atti di stato civile: dallo sportello di stato civile (maschera '
          '«Stampe e comunicazioni») e dall’ufficio certificati, quando l’operatore sceglie '
          'l’area «Stato Civile». Restano fuori i certificati anagrafici (area «Anagrafici»), il '
          'portale dei certificati online e le richieste di estratto dei cittadini sul portale '
          'ANPR (R024).')
    p = paragrafo('Ufficio certificati.', 'List Paragraph')
    p.runs[0].text = 'Certificati anagrafici. '
    corpo(p, 'Quelli che cert-web e cert-be producono da ANAG_USR o chiedono ad ANPR '
             '(operazione 6001) con l’area «Anagrafici» restano come sono. L’area «Stato '
             'Civile» rientra invece nel perimetro.')
    fatti.append('perimetro: area «Stato Civile» dell’ufficio certificati inclusa')

    S('la fonte è decisa dall’atto, non l’operatore', 'la fonte è decisa dall’atto, non '
      'dall’operatore', 1, '«non dall’operatore»')
    S('Il registro attuale ESTRATTIDOWNLOAD_LOG registra', 'Il registro attuale '
      'ESTRATTI_DOWNLOAD_LOG registra', 1, 'refuso ESTRATTI_DOWNLOAD_LOG')
    p = paragrafo('Il registro attuale ESTRATTI_DOWNLOAD_LOG')
    p.add_run(' Riguarda lo sportello di stato civile: l’ufficio certificati registra le '
              'proprie emissioni nella pratica e in CERTIFICATI, dove conserva anche il PDF.')
    S('una tabella nello schema MATR_USR, con i nomi', 'una tabella nello schema ANSC_USR, con '
      'i nomi', 1, 'schema della tabella proposta (ANSC_USR come la DDL)')

    # tabella dei documenti
    t = tab('Documento', 'In SIPO, oggi', 'In ANSC', 'Firma in ANSC')
    for r in t.rows[1:]:
        doc_, cella = r.cells[0].text, r.cells[1]
        if doc_.startswith('Certificato semplice'):
            D.riscrivi_cella(cella, 'Lo sportello di stato civile non lo emette; l’ufficio '
                             'certificati, area «Stato Civile», rilascia i certificati di '
                             'nascita, matrimonio, unione civile e morte, da ANPR (6001) o da '
                             'ANAG_USR.')
        elif doc_.startswith('Estratto per riassunto'):
            D.riscrivi_cella(cella, cella.text + ' L’ufficio certificati li ha in catalogo ma '
                             'non li produce.')
        elif doc_.startswith('Estratto per copia integrale'):
            D.riscrivi_cella(cella, cella.text + ' L’ufficio certificati le ha in catalogo ma '
                             'non le produce.')
    fatti.append('tabella dei documenti: colonna «In SIPO, oggi»')

    t = tab('Percorso', 'Da dove parte', 'Che cosa chiama', 'Che cosa produce')
    D.clona_riga(t, ('Certificato dall’ufficio certificati',
                     'CertificatiWeb, «Nuovo certificato a sportello», area «Stato Civile»',
                     'certificati/recuperaCertificato (cert-be, CertificatiController:321) → '
                     'ANPR 6001 oppure modello locale «Certificato_semplice» su ANAG_USR',
                     'PDF in anteprima o definitivo; CERTIFICATI.DOCUMENTO_CERTIFICATO.'))
    t = tab('Dove', 'Che cosa cambia')
    for riga in [('CertificatiWeb (ufficio certificati)', 'Per un atto ANSC: riepilogo '
                  'dell’atto al posto dell’anteprima; finestra delle credenziali di firma per '
                  'estratti e copie integrali; il PDF di ANSC in download come oggi.'),
                 ('cert-be', 'Instradamento per atto in recuperaCertificato: se l’atto della '
                  'persona ha ID_ATTO_ANSC chiama il concentratore invece di ANPR o del modello '
                  'locale; conserva il PDF in CERTIFICATI.DOCUMENTO_CERTIFICATO.')]:
        nuova = D.clona_riga(t, riga)
        # dopo la riga di statocivile-be
        ancora = [r for r in t.rows if r.cells[0].text == 'statocivile-be'][0]
        ancora._tr.addnext(nuova._tr) if riga[0] == 'cert-be' else \
            ancora._tr.addprevious(nuova._tr)
    fatti.append('righe nuove: percorsi, che cosa cambia in SIPO')

    # glossario e riferimenti
    g = tab('Termine', 'Significato', 'Nota')
    for riga in [('Ufficio certificati', 'Il modulo di SIPO che rilascia i certificati allo '
                  'sportello (CertificatiWeb, cert-be).', 'Area «Stato Civile» = '
                  "CONF_CERTIFICATO.FLG_ANAG_SC = 'S'."),
                 ('Emissione', 'Una chiamata a R002 andata a buon fine.', 'Produce un '
                  'certificato con il suo idCertificato: non esiste un’anteprima.')]:
        D.clona_riga(g, riga)
    rif = tab('#', 'Riferimento', 'Natura')
    a7 = [r for r in rif.rows if r.cells[0].text == '[A7]'][0]
    nuove = []
    for riga in [('[A8]', 'ansc/docs/CasiTest/payload_test/R002_certificazione.json — payload '
                  'di prova della richiesta (rilascio 1.9.0).', 'Sorgente ANSC'),
                 ('[A9]', 'ansc/docs/Note/NotaRetrocompatibilitaServizi — versione nel '
                  'percorso dei servizi.', 'Nota ANSC'),
                 ('[A10]', 'ansc/docs/openapi/Codici d’errore.xlsx — codici HTTP e di errore '
                  'dei servizi.', 'Sorgente ANSC'),
                 ('[A11]', 'ansc/docs/openapi/R005_consultazione_ansc.yaml — consultazione '
                  'sintetica dell’evento, ModelEventoRidotto.', 'Contratto ANSC'),
                 ('[A12]', 'ansc/docs/Note/SpecificheMultilingua/QuickstartMultilingua.md — '
                  'lingue aggiuntive in R002.', 'Nota ANSC')]:
        nuove.append(D.clona_riga(rif, riga)._tr)
    for tr in reversed(nuove):
        a7._tr.addnext(tr)
    D.clona_riga(rif, ('[S4]', 'front-end/cert-web e back-end/cert-be — «Nuovo certificato a '
                       'sportello», ConfCertificatoController, CertificatiController; '
                       'common/pdf-generator (DocCertificatoSempliceComuneRoma); dati di '
                       'configurazione CONF_CERTIFICATO e R_CONF_CERT_ANPR in sipo-root/sql.',
                       'Sorgente applicativo'))
    fatti.append('glossario +2, riferimenti [A8]-[A12] e [S4]')

    # punti aperti
    ce = tab('#', 'Questione', 'A chi spetta')
    for r in ce.rows:
        if r.cells[0].text == 'CE-04':
            D.riscrivi_cella(r.cells[1], 'Se SIPO debba conservare il PDF emesso da ANSC o '
                             'soltanto il suo identificativo. R002 non offre un’operazione per '
                             'riscaricare un certificato già emesso: una ristampa da ANSC è '
                             'un’emissione nuova. L’ufficio certificati conserva già il PDF in '
                             'CERTIFICATI.DOCUMENTO_CERTIFICATO; la proposta è di fare lo '
                             'stesso.')
    for riga in [
        ('CE-15', 'Certificati di nascita, matrimonio e morte che l’ufficio certificati chiede '
         'oggi ad ANPR (6001): per un atto con identificativo ANSC, se emetterli da ANSC (R002, '
         'tipo 1) o continuare con ANPR.', 'Ufficio di stato civile / Anagrafe'),
        ('CE-16', 'Corrispondenza fra le voci di CONF_CERTIFICATO e i tipi di R002: «estratto '
         'certificato» (22, 23, 26) ed «estratto di nascita per uso» (17) non hanno un tipo '
         'evidente.', 'Ufficio di stato civile'),
        ('CE-17', 'Se un operatore con il solo permesso SCCSE possa usare la consultazione '
         'sintetica di R005 (permesso SCCPA) per i controlli prima dell’emissione.',
         'Presidio ANSC / Sogei'),
        ('CE-18', 'Che cosa mostri il pulsante «Anteprima» per un atto ANSC: il riepilogo dei '
         'dati (proposta) oppure un’emissione vera, con un certificato in più.',
         'Ufficio di stato civile / Referenti SIPO'),
        ('CE-19', 'Valori di tipoFile e tipoContenutoFile nella risposta: l’esempio del '
         'contratto indica «3», che in ANSC_10 è TIF, per un PDF; tipoContenutoFile non ha '
         'decodifica. Da verificare in preproduzione.', 'Presidio ANSC / Sogei'),
    ]:
        D.clona_riga(ce, riga)
    fatti.append('CE-04 riformulato, CE-15…CE-19')


if __name__ == '__main__':
    S('Figura 1 — Dalla richiesta', 'Figura 5 — Dalla richiesta', 1, 'figura 1 → 5')
    processo_attuale()
    innesta_prima(paragrafo('Che cosa cambia in SIPO', 'Heading 1')._p, capitolo_r002)
    fatti.append('capitolo «R002 in dettaglio» con la figura 6')
    ritocchi()
    for f in D.frontespizio(d, '0.3', NOME, DATA):
        fatti.append(f)
    D.storia(d, '10/11/2026', '0.2', 'L’attuale processo di richiesta dei certificati · Il '
             'registro delle emissioni', 'Revisione del redattore: processo di richiesta '
             'dall’ufficio certificati con le schermate; descrizione di ESTRATTI_DOWNLOAD_LOG e '
             'dei suoi punti di scrittura.')
    D.storia(d, DATA, '0.3', 'Perimetro · L’attuale processo · R002 in dettaglio (nuovo) · '
             'Che cosa cambia in SIPO · Punti aperti',
             'Area «Stato Civile» dell’ufficio certificati nel perimetro; come la produce oggi '
             'SIPO; uso di R002 in dettaglio: operazione, consultazione preliminare, richiesta, '
             'risposta, codici d’errore, sequenza nelle schermate, buone pratiche; figure '
             'ricomposte e numerate; CE-15…CE-19.')
    d.save(OUT)
    for f in fatti:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tb, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tb, fig))
