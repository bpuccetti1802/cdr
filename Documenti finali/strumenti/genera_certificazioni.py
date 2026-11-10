# -*- coding: utf-8 -*-
"""Genera la v0.1 di «ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC» (10/11/2026).

Dal template DAD (svuotamento del corpo dopo l'elemento 29, come gli altri documenti di
analisi). Decisioni dell'utente prima della stesura:
  1. si parla delle certificazioni di STATO CIVILE (non dei certificati di postazione);
  2. per un atto con identificativo ANSC il documento si emette da ANSC;
  3. perimetro = solo stato civile: fuori l'ufficio certificati (cert-web/cert-be,
     ANAG_USR), il portale online e le richieste dei cittadini (R024);
  4. i difetti del codice esistente trovati nella ricognizione sono un tema separato.

Fatti verificati (contratti, decodifiche, changelog, codice) — vedi i rapporti del 10/11:
  * R002 1.49.0: /certificato e /certificato-semplice, stesso corpo; idTipoCertificato
    1 semplice · 2 riassunto · 3 copia integrale; parametriFirma solo per 2 e 3;
    risposta PDF base64 + idCertificato + datavalidita. Nessun campo obbligatorio.
  * R019 1.33.0: 4 operazioni per i plurilingue, ANSC_114 (4 tipi); nessun parametriFirma.
  * Changelog: 1.17.0 sigillo, QR, PDF/A; 1.38.0 QR valido 6 mesi e datavalidita;
    1.51.0 /certificato-semplice e profilo SCCSE; 1.32.3/1.49.0/1.49.1/1.50.0 firma
    remota degli estratti; 1.35.0 copia integrale semplificata e «emissione possibile per
    atti non in stato conclusivo» (corretto).
  * SIPO: estratti da PKG_ESTRATTI (ImplFlowController:86, FormularioServiceImpl:153),
    plurilingue (AttiScansionatiController:209, UtilityController:8563), copia conforme
    in ATTO_SCANSIONATO.DOCUMENTO_CONFORME, registro ESTRATTI_DOWNLOAD_LOG; nessuna
    firma digitale; nessun riferimento ad ANSC nel percorso.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_certificazioni.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import testo, h, par, voce, tabella, figura   # noqa: E402
import diagrammi_certificazioni   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(QUI))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
NOME = 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.1'
OUT = os.path.join(BASE, 'Documenti finali', NOME + '.docx')
TAGLIA_DA = 29
DATA = '10/11/2026'


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
            testo(p, 'Le certificazioni di stato civile: come le produce SIPO, che cosa offre '
                     'ANSC e come integrarle')
    return d


# =================================================================== tabelle
GLOSSARIO = [
    ['Termine', 'Significato', 'Nota'],
    ['Certificato semplice', 'Documento che attesta i dati essenziali di un evento di stato '
     'civile.', 'In ANSC: R002, tipo 1. Esce con il sigillo del Ministero, senza firma '
     'dell’ufficiale.'],
    ['Estratto per riassunto', 'Documento che riporta in sintesi il contenuto dell’atto e le '
     'annotazioni che lo modificano.', 'In ANSC: R002, tipo 2. Richiede la firma remota '
     'dell’ufficiale.'],
    ['Estratto per copia integrale', 'La riproduzione dell’atto con tutte le annotazioni a '
     'margine.', 'In ANSC: R002, tipo 3, anche nella forma «semplificata» senza metadati. In '
     'SIPO ne fa le veci la copia conforme dell’atto.'],
    ['Plurilingue', 'Estratto internazionale secondo le convenzioni di Vienna e Monaco.',
     'In ANSC: R019, tipi della decodifica ANSC_114.'],
    ['Instradamento per atto', 'La regola proposta: la fonte del documento la decide l’atto, '
     'non l’operatore.', 'Atto con identificativo ANSC → ANSC; altrimenti → SIPO.'],
    ['SCCSE', 'Permesso ANSC «Emissione certificati semplici».', 'Dà accesso a '
     '/certificato-semplice e non a /certificato.'],
    ['USC', 'Ufficiale dello stato civile.', ''],
]

RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[R1]', 'ANALISI_Integrazione-ANSC (versione corrente) — architettura, concentratore '
     'all-ansc-sipo, sessione OTP, store ANSC_STATO_ATTO, schede dei servizi R002 e R019.',
     'Documento di progetto'],
    ['[R2]', 'ansc-v1.yaml e SPEC_API_Integrazione-ANSC (versione corrente) — il contratto '
     'del concentratore.', 'Documento di progetto'],
    ['[R3]', 'Naming_convention_X_DB_v1.01 — nomenclatura degli oggetti di base dati.',
     'Standard aziendale'],
    ['[A1]', 'ansc/docs/openapi/R002_certificazione.yaml, info.version 1.49.0.',
     'Contratto ANSC'],
    ['[A2]', 'ansc/docs/openapi/R019_certificato_internazionale.yaml, info.version 1.33.0.',
     'Contratto ANSC'],
    ['[A3]', 'ansc/docs/Guida_operativa_ANSC.pdf — cap. 12, rilascio delle certificazioni ed '
     'effetti delle annotazioni.', 'Guida ANSC'],
    ['[A4]', 'ansc/docs/Guida_operativa_ANSC_Servizi_di_ausilio.pdf — certificati emissibili, '
     'nota tecnica, certificato internazionale.', 'Guida ANSC'],
    ['[A5]', 'ansc/docs/Changelog.md — le versioni citate nel testo.', 'Sorgente ANSC'],
    ['[A6]', 'ansc/docs/Decodifiche — ANSC_01, ANSC_10, ANSC_28, ANSC_29, ANSC_113, ANSC_114, '
     'ANSC_115.', 'Sorgente ANSC'],
    ['[A7]', 'ansc/docs/openapi/model_evento.yaml — certificabile, flagCertificatoSemplice, '
     'flagEstrattoPerRiassunto, flagAnnotazioneNonCertificabile.', 'Contratto ANSC'],
    ['[S1]', 'front-end/statocivile-web e back-end/statocivile-be — maschera «Stampe e '
     'comunicazioni», ImplFlowController, AttiScansionatiController, FormularioServiceImpl, '
     'UtilityController.', 'Sorgente applicativo'],
    ['[S2]', 'front-end/commonsc-web — maschera «Ricerca soggetto estratti».',
     'Sorgente applicativo'],
    ['[S3]', 'common/pdf-gen-sc, common/matrim-entities, common/commonsc-entities — modelli '
     'Jasper, entità TEMPLATE, ESTRATTI_DOWNLOAD_LOG, ATTO_SCANSIONATO.',
     'Sorgente applicativo'],
]

DOCUMENTI = [
    ['Documento', 'In SIPO, oggi', 'In ANSC', 'Firma in ANSC'],
    ['Certificato semplice', 'Non lo emette lo sportello di stato civile.',
     'R002 /certificato-semplice, tipo 1.', 'Nessuna firma dell’USC: sigillo del Ministero '
     'e QR di verifica.'],
    ['Estratto per riassunto', 'Formulario PKG_ESTRATTI: ESN nascita, ESM matrimonio, ESU '
     'unione civile, ESD morte, e le varianti «sospeso» ESNSC, ESMSC, ESUSC, ESDSC.',
     'R002 /certificato, tipo 2.', 'Firma remota dell’USC con OTP di firma.'],
    ['Estratto per copia integrale', 'Copia conforme generata alla formazione dell’atto e '
     'conservata in ATTO_SCANSIONATO.DOCUMENTO_CONFORME.', 'R002 /certificato, tipo 3, anche '
     'semplificato.', 'Firma remota dell’USC con OTP di firma.'],
    ['Plurilingue di nascita', 'Modello 884.', 'R019, ANSC_114 tipo 1 (Modulo A).',
     'Non dichiarata.'],
    ['Plurilingue di matrimonio', 'Modello 851 (in SIPO si chiama certificato).',
     'R019, ANSC_114 tipo 2 (Modulo B).', 'Non dichiarata.'],
    ['Plurilingue di morte', 'Modelli 872 (foglio bianco) e 874 (prestampato).',
     'R019, ANSC_114 tipo 3 (Modulo C).', 'Non dichiarata.'],
    ['Certificato di capacità matrimoniale', 'Non presente.', 'R019, ANSC_114 tipo 4, valido '
     'sei mesi.', 'Non dichiarata.'],
    ['Estratto di cittadinanza', 'Non presente nel formulario.', 'R002 ammette '
     'l’evento cittadinanza (ANSC_01 = 5); quali tipi siano emissibili non è dichiarato.',
     '—'],
]

FLUSSI_SIPO = [
    ['Percorso', 'Da dove parte', 'Che cosa chiama', 'Che cosa produce'],
    ['Estratto dalla maschera «Stampe e comunicazioni»', 'StampeComunicazioniController.stampa, '
     'ramo ESTRATTO (statocivile-web)', 'POST /generaEstrattoDaFormulario '
     '(ImplFlowController:86) → PKG_ESTRATTI.CONTROLLO_ESTRATTO e FORMULARIO_GENERA_ESTRATTO '
     '(FormularioServiceImpl:189 e :153) → testo in GTT_ESTRATTO → modello Jasper da TEMPLATE',
     'PDF dell’estratto; riga in ESTRATTI_DOWNLOAD_LOG.'],
    ['Estratto da «Ricerca soggetto estratti»', 'RicercaSoggettoEstrattiController '
     '(commonsc-web)', 'Lo stesso servizio.', 'PDF dell’estratto.'],
    ['Plurilingue', 'Maschera dello stato civile', 'POST /getDataForEstrattiPlurilingueMaschera '
     '(AttiScansionatiController:209) → funzioni ESTRATTO_PLURILINGUE e '
     'ESTRATTO_PLURILINGUE_MAT (UtilityController:8563) → GTT_PL_ESTRATTI_*; '
     'l’operatore corregge i campi e genera con i modelli 884, 851, 872/874',
     'PDF plurilingue; riga in ESTRATTI_DOWNLOAD_LOG con tipo PLURILINGUE.'],
    ['Copia conforme', 'Formazione dell’atto', 'Modello ID_TEMPLATE+1 di '
     'CONF_TIPO_MODELLO_ATTO (ImplFlow:612-641)', 'PDF salvato in '
     'ATTO_SCANSIONATO.DOCUMENTO_CONFORME; si ristampa con /scaricaAttoScansionato.'],
]

CONFRONTO = [
    ['Aspetto', 'SIPO, oggi', 'ANSC'],
    ['Da che cosa nasce il testo', 'Dai dati di MATR_USR, ricomposti dal formulario ogni '
     'volta.', 'Dall’atto in ANSC, con le annotazioni registrate in ANSC.'],
    ['Come si individua l’atto', 'Per soggetto e codice individuale, oppure numero, parte, '
     'serie, esponente e anno.', 'idAnsc o idEvento.'],
    ['Annotazioni', 'Quelle che SIPO conosce.', 'Tutte quelle registrate in ANSC, anche da '
     'altri comuni; regole dichiarate per riassunto e copia integrale.'],
    ['Firma', 'Stampa e firma a mano.', 'Certificato semplice con sigillo; estratti con '
     'firma remota dell’USC.'],
    ['Verifica', 'Nessuna.', 'QR di verifica, valido sei mesi dall’emissione.'],
    ['Formato', 'PDF.', 'PDF/A.'],
    ['Registro', 'ESTRATTI_DOWNLOAD_LOG: utente, municipio, estremi dell’atto, tipo di '
     'estratto e di rilascio. Niente richiedente, uso, numerazione.', 'ANSC registra '
     'l’emissione e restituisce idCertificato e data di validità.'],
    ['Uso del documento', 'Non si registra nel percorso di stato civile.', 'idTipoUso, '
     'decodifica ANSC_113, sei valori.'],
    ['Bollo e diritti', 'Non gestiti nel percorso di stato civile.', 'Assenti da contratti, '
     'guide e changelog.'],
    ['Lingue aggiuntive', 'Solo i plurilingue.', 'codiciLingueCertificato in R002; una sola '
     'lingua attiva nella tabella ANPR richiamata (DE).'],
    ['Su quali atti', 'Su ogni atto presente in MATR_USR.', 'Sugli atti presenti in ANSC: '
     'formati in digitale o recuperati.'],
]

ANNOTAZIONI = [
    ['Che cosa è successo all’atto', 'Certificato e riassunto', 'Copia integrale'],
    ['Annotazione integrativa', 'La riportano.', 'La riporta.'],
    ['Annotazione modificativa', 'Riportano già i dati modificati, senza annotazione.',
     'Mostra l’annotazione a margine.'],
    ['Rettifica di annullamento', 'Emissione inibita.', 'Emissibile.'],
    ['Nota tecnica (solo web app)', 'Riportano i dati corretti.', 'Riporta i dati corretti.'],
]

CORRISPONDENZA = [
    ['Richiesta allo sportello', 'Servizio ANSC', 'Parametri principali'],
    ['Certificato di nascita, matrimonio, unione civile, morte', 'R002 /certificato-semplice',
     'idTipoCertificato 1, idTipoEvento (ANSC_01), conPaternitaMaternita per la nascita, '
     'usoMatrimonio, idTipoUso.'],
    ['Estratto per riassunto (oggi ESN, ESM, ESU, ESD)', 'R002 /certificato',
     'idTipoCertificato 2, idTipoEvento, usoMatrimonio, idTipoUso, parametriFirma.'],
    ['Copia integrale (oggi la copia conforme)', 'R002 /certificato', 'idTipoCertificato 3, '
     'flagSemplificato, parametriFirma.'],
    ['Plurilingue di nascita, matrimonio, morte', 'R019, in sequenza', 'idTipoCertificato '
     '(ANSC_114) 1, 2, 3; enunciazioni selezionate; dataRilascio.'],
    ['Certificato di capacità matrimoniale', 'R019, in sequenza', 'idTipoCertificato 4.'],
    ['Lingue aggiuntive', 'R002', 'codiciLingueCertificato.'],
]

OPERAZIONI = [
    ['Operazione proposta', 'Percorso', 'Servizio ANSC', 'Effetti'],
    ['creaCertificato', 'POST /ansc/v1/atti/{idAtto}/certificati', 'R002 /certificato-semplice '
     'per il tipo 1; R002 /certificato per i tipi 2 e 3', 'Emette il documento e lo registra '
     'in ANSC_CERTIFICATO. Per i tipi 2 e 3 richiede le credenziali di firma.'],
    ['elencaCertificati', 'GET /ansc/v1/atti/{idAtto}/certificati', '—', 'Nessuno: legge '
     'ANSC_CERTIFICATO.'],
    ['elencaSigleEnunciazioni', 'GET /ansc/v1/certificati-internazionali/sigle', 'R019 '
     'sigle-enunciazioni', 'Nessuno.'],
    ['elencaAnnotazioniCertificabili', 'GET /ansc/v1/atti/{idAtto}/certificati-internazionali/'
     'annotazioni', 'R019 annotazioni', 'Nessuno.'],
    ['creaAnteprimaCertificatoInternazionale', 'POST /ansc/v1/atti/{idAtto}/'
     'certificati-internazionali/anteprime', 'R019 preview', 'Nessuno.'],
    ['creaCertificatoInternazionale', 'POST /ansc/v1/atti/{idAtto}/certificati-internazionali',
     'R019 create', 'Emette e registra in ANSC_CERTIFICATO.'],
]

IMPATTI = [
    ['Dove', 'Che cosa cambia'],
    ['Maschera «Stampe e comunicazioni» (statocivile-web)', 'Nel ramo dell’estratto, se '
     'l’atto ha l’identificativo ANSC: scelta del tipo (certificato, riassunto, copia '
     'integrale), dell’uso (ANSC_113), di paternità e maternità, dell’uso matrimonio; '
     'per gli estratti la finestra delle credenziali di firma, la stessa della firma '
     'dell’atto.'],
    ['Maschera «Ricerca soggetto estratti» (commonsc-web)', 'La stessa scelta, quando '
     'l’estratto riguarda un atto con identificativo ANSC.'],
    ['Maschera dei plurilingue', 'Per un atto ANSC non si precompila dalle funzioni '
     'ESTRATTO_PLURILINGUE: si presentano le sigle e le annotazioni di R019, l’anteprima e '
     'l’emissione.'],
    ['statocivile-be', 'Un servizio che decide l’instradamento e, per gli atti ANSC, chiama '
     'il concentratore invece del formulario. Continua a scrivere ESTRATTI_DOWNLOAD_LOG.'],
    ['Concentratore all-ansc-sipo e ansc-v1.yaml', 'Le sei operazioni del capitolo precedente; '
     'il contratto e la specifica delle API vanno aggiornati e rigenerati.'],
    ['Modello dati ANSC_USR', 'La tabella ANSC_CERTIFICATO.'],
    ['Profilazione ANSC', 'Il permesso SCCSE agli operatori che emettono soltanto certificati '
     'semplici; il permesso pieno agli ufficiali.'],
]

CORREZIONI_R1 = [
    ['Dove, in [R1]', 'Che cosa dice', 'Che cosa va scritto'],
    ['Scheda R002 e inventario delle funzioni', '«La certificazione resta in SIPO»; R002 «non '
     'impiegato nel pilota».', 'La certificazione degli atti con identificativo ANSC si fa con '
     'R002 e R019 attraverso il concentratore; SIPO resta la fonte per gli atti del registro '
     'tradizionale. Rinvio a questo documento.'],
    ['Scheda R002, modalità di adozione', '«Ogni emissione è un atto di firma '
     'dell’ufficiale»; nelle trappole: emettere un certificato consuma un OTP di firma.',
     'Vale per gli estratti (tipi 2 e 3). Il certificato semplice non porta parametri di firma '
     'ed esce con il sigillo del Ministero.'],
    ['Inventario delle operazioni ANSC', 'R002 con due operazioni a «permesso ridotto» e '
     'pieno.', 'Invariato; aggiungere che il permesso ridotto è SCCSE (versione 1.51.0).'],
]

APERTI = [
    ['#', 'Questione', 'A chi spetta'],
    ['CE-01', 'Quali campi di R002 siano davvero obbligatori: il contratto non ne dichiara '
     'nessuno. In particolare se basti idAnsc o serva anche idEvento, e se l’intestatario '
     'vada sempre indicato. Da provare in preproduzione.', 'Presidio ANSC / Sogei'],
    ['CE-02', 'Se il Comune possa certificare con R002 atti formati da altri comuni. Nessuna '
     'fonte lo dice in modo esplicito; il changelog 1.38.3 impedisce solo di modificare la '
     'tipologia di certificazione di un atto prodotto da altro comune.', 'Presidio ANSC / '
     'Sogei'],
    ['CE-03', 'In quale stato l’atto sia certificabile. Il contratto non pone vincoli; la '
     'guida lega il rilascio agli atti firmati e il changelog 1.35.0 corregge l’emissione '
     'su atti non in stato conclusivo.', 'Presidio ANSC / Sogei'],
    ['CE-04', 'Se SIPO debba conservare il PDF emesso da ANSC o soltanto il suo '
     'identificativo. Una ristampa da ANSC produce un’emissione nuova.', 'Referenti SIPO / '
     'Conservazione'],
    ['CE-05', 'Bollo, diritti ed esenzioni: ANSC non li tratta. Se l’uso dichiarato (ANSC_113) '
     'debba avere un raccordo con le esenzioni del Comune, e dove registrarlo.',
     'Ufficio di stato civile / Ragioneria'],
    ['CE-06', 'Come sia firmato o sigillato il certificato internazionale di R019: il contratto '
     'non porta parametri di firma e nessuna fonte lo dichiara.', 'Presidio ANSC / Sogei'],
    ['CE-07', 'Emissibilità degli atti con caso d’uso di servizio: i flag del modello evento '
     'non compaiono nel mapping e la scelta si fa dalla web app («Gestione certificati '
     'emissibili»). Si lega a OP-85 di [R1].', 'Ufficio di stato civile / Architettura'],
    ['CE-08', 'Che cosa fare se la risposta di R002 non arriva dopo una richiesta di estratto '
     'firmato: ripetere produce un secondo certificato. Serve un modo di sapere se '
     'l’emissione è avvenuta.', 'Presidio ANSC / Architettura'],
    ['CE-09', 'Lingue aggiuntive: la nota ANSC rinvia alla tabella 14 di ANPR, con il solo '
     'tedesco attivo. Se e quando servano altre lingue.', 'Ufficio di stato civile'],
    ['CE-10', 'Chi abbia il permesso SCCSE e chi il permesso pieno: è una scelta di '
     'organizzazione e di abilitazioni ANSC.', 'Ufficio di stato civile'],
    ['CE-11', 'La guida operativa (p. 79) invita a scaricare il PDF e «eventualmente stamparlo '
     'e firmarlo»; contratto e changelog impongono la firma remota per gli estratti. Si '
     'assume la firma remota.', 'Presidio ANSC / Sogei'],
    ['CE-12', 'Disallineamenti delle fonti: R002 si dichiara 1.49.0 ma contiene '
     '/certificato-semplice della 1.51.0; il changelog 1.53.0 attribuisce a R002 un campo '
     '(flagScartoDigitale) che sta solo nel modello evento e percorsi che stanno in R019.',
     'Presidio ANSC / Sogei'],
    ['CE-13', 'Significato delle varianti di estratto «sospeso» di SIPO (ESNSC, ESMSC, ESUSC, '
     'ESDSC) e se abbiano un corrispondente in ANSC.', 'Referenti SIPO'],
    ['CE-14', 'Richieste di estratto dei cittadini dal portale ANPR (R024): fuori dal perimetro '
     'di questo documento; finché non si integrano si lavorano sulla web app ANSC.',
     'Ufficio di stato civile'],
]


# =================================================================== testo
def ddl(d, righe):
    """Righe di codice in Courier New, senza spazio fra l'una e l'altra."""
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)


def scrivi(d):
    h(d, 1, 'Scopo del documento')
    par(d, 'Questo documento analizza come si producono le certificazioni di stato civile — '
           'certificati, estratti per riassunto, copie integrali, plurilingue — in SIPO e in '
           'ANSC, e propone come integrarle. È un approfondimento dell’analisi di integrazione '
           '[R1], che finora aveva lasciato la certificazione fuori dal perimetro.')
    h(d, 2, 'Perimetro e scelte già compiute')
    voce(d, 'Solo lo stato civile.', 'Il documento tratta i documenti che lo sportello di '
         'stato civile emette sugli atti. Restano fuori l’ufficio certificati di SIPO, che '
         'lavora sull’anagrafe e chiede ad ANPR i certificati anagrafici, il portale dei '
         'certificati online e le richieste di estratto dei cittadini sul portale ANPR (R024).')
    voce(d, 'La fonte la decide l’atto.', 'Per un atto che ha un identificativo ANSC il '
         'documento si emette da ANSC; per gli altri SIPO continua a produrlo come oggi.')
    voce(d, 'Il codice esistente si descrive, non si giudica.', 'I rilievi sul codice di SIPO '
         'emersi durante la ricognizione sono raccolti a parte.')
    h(d, 2, 'Metodo e fonti')
    par(d, 'La parte ANSC viene dai contratti, dalle guide, dalle decodifiche e dal changelog '
           'del repository pubblico [A1]–[A7]; la parte SIPO dal codice [S1]–[S3]. Dove le fonti '
           'tacciono il documento lo dichiara e apre un punto aperto. La proposta è nostra ed è '
           'distinta da ciò che le fonti dicono.')
    h(d, 2, 'Glossario')
    tabella(d, GLOSSARIO, [1.6, 2.6, 2.2])
    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 4.6, 1.2])

    # ------------------------------------------------------------------
    h(d, 1, 'I documenti di stato civile')
    par(d, 'I nomi non coincidono nei due sistemi, e la tabella che segue fa da dizionario. In '
           'ANSC i documenti di R002 si distinguono con un solo campo, idTipoCertificato, i cui '
           'tre valori sono scritti nella descrizione del contratto e non in una decodifica; '
           'quelli di R019 seguono la decodifica ANSC_114.')
    tabella(d, DOCUMENTI, [1.4, 2.0, 1.6, 1.4])
    par(d, 'La decodifica ANSC_115 («default · certificato semplice · estratto per riassunto · '
           'semplice e riassunto») è pubblicata ma nessun contratto la richiama; ANSC_29 '
           '(«certificabile · parzialmente · non certificabile») serve solo agli atti con caso '
           'd’uso di servizio, per i quali i tipi emissibili non sono fissi.')

    # ------------------------------------------------------------------
    h(d, 1, 'Come SIPO produce oggi le certificazioni di stato civile')
    h(d, 2, 'I percorsi')
    par(d, 'Nello stato civile i documenti nascono dai dati di MATR_USR. Il testo non è '
           'conservato: lo ricompone a ogni richiesta un formulario PL/SQL, e un modello Jasper '
           'lo impagina. Il corpo dei package (PKG_ESTRATTI, PKG_FORMULARI) e il contenuto dei '
           'modelli vivi, che stanno nella tabella TEMPLATE, non sono fra le sorgenti.')
    tabella(d, FLUSSI_SIPO, [1.3, 1.5, 2.3, 1.3])
    h(d, 2, 'Firma, registro e collegamento con ANSC')
    voce(d, 'Nessuna firma digitale.', 'Né i modelli né i servizi applicano firma, sigillo o '
         'contrassegno: il documento si stampa e l’ufficiale lo firma a mano.')
    voce(d, 'Un registro essenziale.', 'ESTRATTI_DOWNLOAD_LOG conserva data, utente, '
         'organizzazione, municipio, estremi dell’atto (numero, parte, serie, anno, esponente), '
         'tipo di estratto (NORMALE o PLURILINGUE) e di rilascio. Non conserva richiedente, '
         'uso, bollo né una numerazione del documento.')
    voce(d, 'Nessun legame con ANSC.', 'Nel percorso di emissione dello stato civile '
         'l’identificativo ANSC non compare: l’atto si cerca per soggetto o per estremi del '
         'registro tradizionale. Un atto formato in ANSC che SIPO non ha per intero non ha su '
         'che cosa essere ricomposto.')

    # ------------------------------------------------------------------
    h(d, 1, 'Che cosa offre ANSC')
    h(d, 2, 'Le operazioni')
    par(d, 'Sono sei, in due contratti, tutte POST con la versione nel percorso [A1] [A2].')
    voce(d, 'R002 /certificato e /certificato-semplice.', 'Stesso corpo, stessa risposta; '
         'differiscono per il permesso: la seconda è accessibile anche con il permesso SCCSE, '
         'aggiunto nella versione 1.51.0. La richiesta porta idAnsc e idEvento, richiedente, '
         'ente richiedente, intestatario, idTipoCertificato, idTipoEvento, '
         'conPaternitaMaternita, usoMatrimonio, codiciLingueCertificato, idTipoUso (ANSC_113), '
         'flagSemplificato e, solo per gli estratti, parametriFirma. La risposta restituisce il '
         'PDF in base64, il nome del file, idCertificato e la data di fine validità. Nessun '
         'campo è dichiarato obbligatorio (CE-01).')
    voce(d, 'R019, quattro operazioni per i plurilingue.', 'Sigle delle enunciazioni, '
         'annotazioni dell’evento, anteprima ed emissione, da usare in questa sequenza. La '
         'guida avverte che le sigle non selezionate non compaiono sull’estratto.')
    h(d, 2, 'Firma e sessione')
    par(d, 'È il punto in cui ANSC differisce di più da SIPO, e anche quello su cui [R1] va '
           'corretto. Il **certificato semplice non porta parametri di firma**: dalla versione '
           '1.17.0 esce con il sigillo del Ministero, il QR di verifica e in formato PDF/A, e '
           'dalla 1.38.0 il QR vale sei mesi dall’emissione. Gli **estratti** — riassunto e '
           'copia integrale — richiedono invece la **firma remota dell’ufficiale**, con utente, '
           'password e OTP di firma, lo stesso schema della firma dell’atto (versioni 1.32.3, '
           '1.49.0, 1.49.1, 1.50.0). Ogni chiamata richiede comunque la sessione OTP del '
           'concentratore. R019 non dichiara come sia firmato il plurilingue (CE-06).')
    h(d, 2, 'Le annotazioni e i casi particolari')
    par(d, 'ANSC applica da sé le annotazioni registrate sull’atto, comprese quelle fatte da '
           'altri comuni [A3]:')
    tabella(d, ANNOTAZIONI, [2.0, 2.3, 2.1])
    voce(d, 'Atti con caso d’uso di servizio.', 'I tipi emissibili non sono fissi: si scelgono '
         'dalla web app («Gestione certificati emissibili», solo per gli atti del proprio '
         'comune) o con i campi certificabile, flagCertificatoSemplice e '
         'flagEstrattoPerRiassunto del modello evento, che però non compaiono nel mapping. La '
         'copia integrale è sempre disponibile.')
    voce(d, 'Annotazioni non certificabili.', 'Il modello evento porta '
         'flagAnnotazioneNonCertificabile, presente in 66 righe del mapping, sempre facoltativo.')
    voce(d, 'Adozioni.', 'Le versioni 1.49.0 e 1.50.0 aggiungono avvisi e correzioni sugli '
         'estratti con annotazioni di adozione; nessuna regola di inibizione è dichiarata.')
    h(d, 2, 'Che cosa resta alla sola web app')
    par(d, 'La scelta dei certificati emissibili per i casi d’uso di servizio e la nota tecnica, '
           'che modifica ciò che le certificazioni riportano, non hanno operazioni nei '
           'contratti.')

    # ------------------------------------------------------------------
    h(d, 1, 'Il confronto')
    tabella(d, CONFRONTO, [1.5, 2.4, 2.5])

    # ------------------------------------------------------------------
    h(d, 1, 'Chi è la fonte del documento')
    par(d, 'Per un atto formato in digitale l’originale sta in ANSC. Le annotazioni fatte da '
           'altri comuni, le rettifiche e le note tecniche arrivano lì e non nel database di '
           'SIPO, che di quell’atto conserva i dati di formazione. Un estratto ricomposto da SIPO '
           'con i dati locali può quindi divergere dall’atto vero, ed è un documento firmato '
           'dall’ufficiale. Per lo stesso atto, i due sistemi potrebbero rilasciare due '
           'documenti diversi.')
    par(d, 'Per gli atti del registro tradizionale vale il contrario: ANSC non li ha, o li ha '
           'solo se recuperati, e SIPO resta la sola fonte.')
    par(d, 'Ne discende la regola proposta: **la fonte la decide l’atto, non l’operatore**. '
           'L’operatore continua a lavorare dallo sportello di SIPO, che riconosce l’atto e '
           'sceglie da sé dove produrre il documento.')

    # ------------------------------------------------------------------
    h(d, 1, 'La proposta di integrazione')
    h(d, 2, 'L’instradamento per atto')
    figura(d, diagrammi_certificazioni.instradamento(), 6.5,
           'Figura 1 — Dalla richiesta allo sportello al documento: la fonte la decide l’atto.')
    voce(d, 'La regola.', 'Se l’atto ha un identificativo ANSC — nello store ANSC_STATO_ATTO, '
         'oppure in ANAG_USR.ATTO.ID_ATTO_ANSC per gli atti agganciati — il documento si emette '
         'da ANSC; altrimenti dal formulario di SIPO.')
    voce(d, 'I controlli restano in SIPO.', 'Prima di chiamare ANSC, SIPO verifica il blocco '
         'della certificazione del soggetto e lo stato dell’atto, come per ogni altro documento.')
    voce(d, 'Ciò che ANSC rifiuta si mostra com’è.', 'Una rettifica di annullamento inibisce '
         'certificato e riassunto: l’operatore deve leggere il motivo restituito da ANSC, non '
         'un errore generico.')
    h(d, 2, 'La corrispondenza fra le richieste e i servizi')
    tabella(d, CORRISPONDENZA, [2.0, 1.6, 2.8])
    par(d, 'Allo sportello di stato civile si aggiunge il certificato semplice, che oggi non '
           'emette: con il permesso SCCSE lo può rilasciare anche un operatore che non è '
           'ufficiale, perché non richiede la sua firma.')
    h(d, 2, 'La firma degli estratti')
    par(d, 'Per riassunto e copia integrale l’ufficiale inserisce utente, password e OTP di '
           'firma, nella stessa finestra della firma dell’atto. Le credenziali vanno al '
           'concentratore e da lì ad ANSC, con il valore codificato in base64 che il contratto '
           'richiede in produzione. Il certificato semplice e i plurilingue non chiedono nulla.')
    h(d, 2, 'Le operazioni del concentratore')
    par(d, 'Il concentratore all-ansc-sipo è il solo componente che parla con ANSC [R1]; '
           'servono sei operazioni nuove nel suo contratto [R2], con i nomi delle convenzioni '
           'già in uso.')
    tabella(d, OPERAZIONI, [1.6, 2.1, 1.4, 1.3])
    h(d, 2, 'Il registro delle emissioni')
    par(d, 'Il registro di oggi non ha dove mettere l’identificativo del certificato, la data di '
           'validità e l’uso dichiarato. Si propone una tabella nello schema ANSC_USR, con i '
           'nomi dello standard [R3]; ESTRATTI_DOWNLOAD_LOG continua a ricevere una riga per '
           'ogni emissione, con un tipo di rilascio ANSC, perché le statistiche di oggi restino '
           'confrontabili.')
    ddl(d, [
        'CREATE TABLE ANSC_USR.ANSC_CERTIFICATO (',
        '  ID_CERTIFICATO        NUMBER GENERATED ALWAYS AS IDENTITY,',
        '  ID_CERTIFICATO_ANSC   VARCHAR2(50 CHAR),          -- idCertificato restituito',
        '  ID_ATTO_SIPO          NUMBER        NOT NULL,     -- per valore',
        '  ID_ANSC               VARCHAR2(50 CHAR) NOT NULL,',
        '  COD_SERVIZIO_ANSC     VARCHAR2(10 CHAR) NOT NULL, -- R002, R019',
        '  ID_TIPO_CERTIFICATO   VARCHAR2(5 CHAR)  NOT NULL, -- R002: 1 2 3; R019: ANSC_114',
        '  ID_TIPO_EVENTO        VARCHAR2(10 CHAR),          -- ANSC_01',
        '  ID_TIPO_USO           VARCHAR2(5 CHAR),           -- ANSC_113',
        "  FLG_PATERNITA_MATERNITA CHAR(1) DEFAULT 'N' NOT NULL,",
        "  FLG_USO_MATRIMONIO    CHAR(1) DEFAULT 'N' NOT NULL,",
        "  FLG_SEMPLIFICATO      CHAR(1) DEFAULT 'N' NOT NULL,",
        '  COD_LINGUE            VARCHAR2(100 CHAR),',
        '  ID_SOGGETTO_SIPO      NUMBER,                     -- intestatario, per valore',
        '  DATA_VALIDITA         DATE,',
        '  DESC_NOME_FILE        VARCHAR2(200 CHAR),',
        '  COD_ESITO             VARCHAR2(20 CHAR) NOT NULL, -- EMESSO RIFIUTATO DA_VERIFICARE',
        '  ID_AUDIT              NUMBER,                     -- la chiamata, per valore',
        '  COD_MUNICIPIO         VARCHAR2(10 CHAR),',
        '  TS_INS                TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
        '  UTENTE_INS            VARCHAR2(40 CHAR) NOT NULL,',
        '  CONSTRAINT PK_ANSC_CERTIFICATO PRIMARY KEY (ID_CERTIFICATO),',
        '  CONSTRAINT CK_ANSC_CERT_SERVIZIO CHECK (COD_SERVIZIO_ANSC IN (\'R002\',\'R019\')),',
        '  CONSTRAINT CK_ANSC_CERT_ESITO',
        "    CHECK (COD_ESITO IN ('EMESSO','RIFIUTATO','DA_VERIFICARE')),",
        "  CONSTRAINT CK_ANSC_CERT_PAT CHECK (FLG_PATERNITA_MATERNITA IN ('S','N')),",
        "  CONSTRAINT CK_ANSC_CERT_MATR CHECK (FLG_USO_MATRIMONIO IN ('S','N')),",
        "  CONSTRAINT CK_ANSC_CERT_SEMPL CHECK (FLG_SEMPLIFICATO IN ('S','N'))",
        ') TABLESPACE ANSC_USR;',
        '',
        'CREATE INDEX IX_ANSC_CERTIFICATO_ATTO ON ANSC_USR.ANSC_CERTIFICATO (ID_ATTO_SIPO);',
    ])
    par(d, 'La tabella delle emissioni ANSC.')
    voce(d, 'Riferimenti per valore.', 'L’atto, il soggetto e la riga di audit si richiamano '
         'per valore, come gli altri oggetti dello schema che toccano SIPO [R1].')
    voce(d, 'Il tipo dipende dal servizio.', 'ID_TIPO_CERTIFICATO si legge insieme a '
         'COD_SERVIZIO_ANSC: in R002 vale 1, 2 o 3, in R019 segue ANSC_114.')
    voce(d, 'Nessun dato del richiedente.', 'Come il registro di oggi. Se serva registrarlo è '
         'una decisione dell’ufficio, e allora andrà trattato come dato personale.')
    voce(d, 'Il PDF non è nella tabella.', 'Se conservarlo è CE-04.')
    h(d, 2, 'Bollo, diritti ed esenzioni')
    par(d, 'ANSC non li tratta e il percorso di stato civile di SIPO oggi non li registra. '
           'L’integrazione non cambia questo stato di cose; l’uso dichiarato ad ANSC (ANSC_113) '
           'è però l’unico dato che potrebbe raccordarsi alle esenzioni, ed è CE-05.')

    # ------------------------------------------------------------------
    h(d, 1, 'Che cosa cambia in SIPO')
    tabella(d, IMPATTI, [2.0, 4.4])
    par(d, 'Il percorso dei documenti sugli atti del registro tradizionale non cambia.')

    # ------------------------------------------------------------------
    h(d, 1, 'Correzioni da riportare nell’analisi di integrazione')
    par(d, 'Due affermazioni di [R1] vanno riviste alla luce di questo documento.')
    tabella(d, CORREZIONI_R1, [1.5, 2.2, 2.7])

    # ------------------------------------------------------------------
    h(d, 1, 'Fuori dal perimetro')
    voce(d, 'Ufficio certificati.', 'cert-web e cert-be lavorano su ANAG_USR e chiedono ad ANPR '
         '(operazione 6001) i certificati anagrafici di nascita, matrimonio e morte; il loro '
         'catalogo comprende anche estratti e copie integrali, che però non generano.')
    voce(d, 'Certificati online.', 'Il portale del Comune offre solo voci prodotte '
         'dall’ufficio certificati; nessun estratto.')
    voce(d, 'Richieste dei cittadini sul portale ANPR (R024).', 'Riguardano gli estratti degli '
         'atti digitali di nascita, matrimonio e unione civile, arrivano all’ufficiale del '
         'comune che ha formato l’atto e si lavorano oggi sulla web app (CE-14).')
    voce(d, 'Certificato necroscopico.', 'Appartiene al canale sanitario (R022, R023), non '
         'alla certificazione.')

    # ------------------------------------------------------------------
    h(d, 1, 'Punti aperti')
    tabella(d, APERTI, [0.7, 4.3, 1.4])

    h(d, 1, 'Il percorso di adozione')
    voce(d, 'Primo — il certificato semplice.', 'Non richiede la firma dell’ufficiale: è il '
         'modo più semplice di provare R002, l’instradamento e il registro.')
    voce(d, 'Secondo — gli estratti.', 'Riassunto e copia integrale con la firma remota, dopo '
         'aver chiuso CE-01, CE-03 e CE-08 in preproduzione.')
    voce(d, 'Terzo — i plurilingue.', 'R019 con la sequenza delle quattro operazioni, dopo '
         'CE-06.')


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
             'Prima stesura. Documenti di stato civile nei due sistemi; come SIPO li produce '
             'oggi; operazioni, firma e annotazioni in ANSC; confronto; la fonte del documento; '
             'proposta di instradamento per atto, corrispondenza con R002 e R019, firma degli '
             'estratti, sei operazioni del concentratore, tabella ANSC_CERTIFICATO; impatti su '
             'SIPO; correzioni a [R1]; quattordici punti aperti.')


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
