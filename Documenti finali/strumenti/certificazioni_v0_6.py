# -*- coding: utf-8 -*-
"""v0.6 di «ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC» (11/11/2026).

Dal FILE REALE della v0.5 salvata dall'utente (testo identico alla generata: il salvataggio
di Word ha cambiato solo la struttura interna). Richiesta: il dettaglio della risposta ANSC a
R002 e come va gestita.

Fatti (R002 1.49.0, base_servizi.yaml, ServiceMessage in R024, Codici d'errore.xlsx):
  * CertificatoResponse = AnscResponse (testataRisposta: idComune, idOperazioneComune,
    idOperazione, idEsito; datiPaginazione; errors, infos, success, warnings di ServiceMessage
    code/severity E-W-I-S/text) + contenuto (base64), nomeFile, tipoFile (ANSC_10),
    tipoContenutoFile, idCertificato, codice, descrizione, tipologia, datavalidita (format
    date SENZA type);
  * HTTP dichiarati 200, 403, 404, tutti con lo stesso schema;
  * nessun campione di risposta R002 nel repository (i payload di prova sono richieste).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/certificazioni_v0_6.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import h, par, voce, tabella   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.5.docx')
NOME = 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.6'
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


def mono(righe):
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)


def gestione():
    h(d, 2, 'La gestione della risposta di R002')
    par(d, 'La sezione precedente elenca i campi della risposta. Questa dice come leggerla '
           'tutta, come decidere l’esito, che cosa fanno concentratore, cert-be e pagina, e '
           'dove finisce ogni dato. Il repository ANSC non contiene esempi di risposta di R002, '
           'solo di richiesta [A8]: gli esempi che seguono sono costruiti dal contratto [A1] e '
           'dall’involucro comune dei servizi, con valori di fantasia.')

    h(d, 3, 'La risposta per intero')
    par(d, 'La risposta è sempre un oggetto JSON con lo stesso schema, qualunque sia il codice '
           'HTTP (200, 403 o 404): l’involucro comune `AnscResponse` più i campi propri di R002. '
           'Un’emissione riuscita:')
    mono(['HTTP 200',
          '{',
          '  "testataRisposta": {',
          '    "idComune": 8165,',
          '    "idOperazioneComune": "<quello inviato nella richiesta>",',
          '    "idOperazione": "<identificativo ANSC dell’operazione>",',
          '    "idEsito": 0',
          '  },',
          '  "errors": [], "warnings": [], "infos": [], "success": [],',
          '  "contenuto": "JVBERi0xLjcK…",',
          '  "nomeFile": "2757.pdf",',
          '  "tipoFile": "1",',
          '  "tipoContenutoFile": "1",',
          '  "idCertificato": "2757",',
          '  "codice": "200", "descrizione": "success",',
          '  "datavalidita": "2027-05-11"',
          '}'])
    par(d, 'Una richiesta respinta, per esempio su un atto annullato:')
    mono(['HTTP 4xx',
          '{',
          '  "testataRisposta": { "idOperazioneComune": "<…>", "idOperazione": "<…>", '
          '"idEsito": <…> },',
          '  "errors": [ { "code": "401003", "severity": "E", "text": "<motivo scritto da '
          'ANSC>" } ],',
          '  "codice": "<…>", "descrizione": "<…>", "tipologia": "errore"',
          '}'])
    tabella(d, [
        ['Parte', 'Campi', 'Come va letta'],
        ['Testata', 'idComune, idOperazioneComune, idOperazione, idEsito', 'idOperazioneComune '
         'deve essere quello inviato: lega la risposta alla richiesta. idOperazione è il '
         'riferimento da citare ad ANSC. idEsito è un intero senza decodifica pubblicata '
         '(CE-27).'],
        ['Messaggi', 'errors, warnings, infos, success: elenchi di {code, severity, text}',
         'severity vale E, W, I o S. Il text è scritto per l’operatore e si mostra così '
         'com’è; il code serve alla classificazione e all’audit.'],
        ['Documento', 'contenuto, nomeFile, tipoFile, tipoContenutoFile', 'contenuto è il PDF/A '
         'in base64; nomeFile è idCertificato con l’estensione .pdf; tipoFile atteso «1», PDF; '
         'tipoContenutoFile non ha decodifica.'],
        ['Certificato', 'idCertificato, datavalidita', 'Identificativo dell’emissione presso '
         'ANSC e ultimo giorno di validità.'],
        ['Esito in chiaro', 'codice, descrizione, tipologia', 'Ripetono l’esito: «200» e '
         '«success» nel caso riuscito, tipologia «errore» negli altri.'],
    ], [1.2, 2.2, 3.1])
    par(d, 'Tre irregolarità del contratto che chi scrive il client deve conoscere:')
    voce(d, 'datavalidita non ha un tipo.', 'Il contratto dichiara solo `format: date`, senza '
         '`type: string`: alcuni generatori di client lo trattano come oggetto libero. Va letto '
         'come stringa AAAA-MM-GG.')
    voce(d, 'L’esempio di tipoFile è «3».', 'In ANSC_10 il 3 è TIF, ma il documento è un PDF '
         '(CE-19): il formato si verifica sul contenuto, non su questo campo.')
    voce(d, 'L’esito è scritto tre volte.', 'Codice HTTP, idEsito della testata e il terzetto '
         'codice, descrizione, tipologia. Il contratto non dice quale prevalga se discordano '
         '(CE-27); la regola che segue li legge in un ordine fisso.')

    h(d, 3, 'Come si decide l’esito')
    par(d, 'Il concentratore classifica ogni risposta in uno dei tre esiti previsti da '
           '`ANSC_CERTIFICATO.COD_ESITO`, applicando le regole in quest’ordine; vale la prima '
           'che si verifica:')
    tabella(d, [
        ['#', 'Condizione', 'Esito', 'Perché'],
        ['1', 'Nessuna risposta: tempo scaduto, connessione interrotta, risposta non leggibile',
         'DA_VERIFICARE', 'ANSC può aver emesso il certificato senza che SIPO lo sappia.'],
        ['2', 'HTTP 5xx', 'DA_VERIFICARE', 'Errore interno: l’emissione può essere avvenuta.'],
        ['3', 'HTTP 406 con codice 406001 o 406002', 'RIFIUTATO', 'OTP di sessione non valido o '
         'scaduto: nessuna emissione; si chiede un codice nuovo.'],
        ['4', 'HTTP 406 con codice 406004', 'RIFIUTATO', 'Firma non riuscita. Che il '
         'certificato non sia stato emesso è [DA VERIFICARE] in preproduzione.'],
        ['5', 'Altro HTTP 4xx, oppure HTTP 200 con almeno un elemento in errors', 'RIFIUTATO',
         'ANSC ha respinto la richiesta; il motivo è nel text.'],
        ['6', 'HTTP 200, errors vuoto, idCertificato valorizzato, contenuto che si decodifica in '
         'un PDF', 'EMESSO', 'È l’unico caso in cui il certificato c’è ed è in mano a SIPO.'],
        ['7', 'HTTP 200 senza errori ma con idCertificato assente o contenuto vuoto o non PDF',
         'DA_VERIFICARE', 'Risposta incoerente: il certificato può esistere in ANSC senza che '
         'SIPO ne abbia il file.'],
    ], [0.3, 2.6, 1.2, 2.4])
    par(d, 'warnings e infos non cambiano l’esito: un certificato emesso con avvisi è EMESSO, e '
           'gli avvisi si mostrano all’operatore. Le versioni 1.49.0 e 1.50.0, per esempio, '
           'aggiungono avvisi sugli estratti con annotazioni di adozione [A5].')

    h(d, 3, 'Che cosa fa SIPO, passo per passo')
    voce(d, '1. Concentratore: audit della chiamata.', 'Appena ricevuta la risposta scrive la '
         'riga di `ANSC_LOG_AUDIT` con testata, messaggi, esito e durata. Al posto del contenuto '
         'registra lunghezza e impronta SHA-256 del PDF; i parametri di firma della richiesta '
         'non si registrano.')
    voce(d, '2. Concentratore: esito.', 'Applica le regole della tabella precedente.')
    voce(d, '3. Concentratore: decodifica e controllo del PDF.', 'Solo per l’esito EMESSO: '
         'decodifica il base64 tollerando gli a capo e controlla che il risultato non sia vuoto '
         'e cominci con «%PDF». Se il controllo fallisce l’esito diventa DA_VERIFICARE.')
    voce(d, '4. Concentratore: registro delle emissioni.', 'Scrive la riga di '
         '`ANSC_CERTIFICATO` in una transazione propria, prima di rispondere a cert-be: '
         'idCertificato, datavalidita, nomeFile, esito e la riga di audit. Così un certificato '
         'emesso resta registrato anche se il passo successivo fallisce.')
    voce(d, '5. Concentratore: risposta a cert-be.', 'Restituisce esito, idCertificato, '
         'datavalidita, nome del file, i messaggi di ANSC e, per EMESSO, il PDF già '
         'decodificato.')
    voce(d, '6. cert-be: conservazione.', 'Per EMESSO salva il PDF in '
         '`CERTIFICATI.DOCUMENTO_CERTIFICATO`, come fa oggi per i certificati di ANPR, e chiude '
         'la riga del certificato nella pratica. Se il salvataggio fallisce, il certificato '
         'esiste in ANSC e in `ANSC_CERTIFICATO` ma SIPO non ne ha il file: R002 non permette '
         'di riscaricarlo (CE-26).')
    voce(d, '7. CertificatiWeb: consegna.', 'Invia il PDF al browser in download '
         '(application/pdf) con il nome restituito da ANSC e mostra il messaggio d’esito.')
    par(d, 'Sullo sportello di stato civile («Stampe e comunicazioni») la tabella CERTIFICATI '
           'non c’è: i passi da 1 a 5 restano uguali, la conservazione del PDF è CE-04 e la '
           'riga di `ESTRATTI_DOWNLOAD_LOG` si scrive come oggi.')

    h(d, 3, 'Il PDF: che cosa non si fa')
    par(d, 'Il certificato porta il sigillo del Ministero, il QR di verifica e, per estratti e '
           'copie integrali, la firma remota dell’ufficiale. Qualunque modifica del file ne '
           'invalida il valore. Quindi SIPO:')
    voce(d, 'non lo rimpagina e non lo ricompone', 'con i propri modelli Jasper;')
    voce(d, 'non vi aggiunge', 'intestazioni, filigrane, numeri di protocollo o timbri;')
    voce(d, 'non lo unisce ad altri PDF:', 'più certificati della stessa pratica restano file '
         'distinti, anche dove oggi la stampa li riunisce;')
    voce(d, 'non lo converte', 'in altri formati per mostrarlo: lo consegna così come ANSC lo ha '
         'prodotto.')

    h(d, 3, 'Dove finisce ogni dato')
    tabella(d, [
        ['Dato della risposta', 'Dove si registra'],
        ['contenuto', 'CERTIFICATI.DOCUMENTO_CERTIFICATO (ufficio certificati). In audit solo '
         'lunghezza e impronta.'],
        ['idCertificato', 'ANSC_CERTIFICATO.ID_CERTIFICATO_ANSC'],
        ['datavalidita', 'ANSC_CERTIFICATO.DATA_VALIDITA'],
        ['nomeFile', 'ANSC_CERTIFICATO.DESC_NOME_FILE; nome del file scaricato'],
        ['Esito classificato', 'ANSC_CERTIFICATO.COD_ESITO (EMESSO, RIFIUTATO, DA_VERIFICARE)'],
        ['testataRisposta (idOperazione, idEsito)', 'ANSC_LOG_AUDIT, richiamata da '
         'ANSC_CERTIFICATO.ID_AUDIT'],
        ['errors, warnings, infos', 'ANSC_LOG_AUDIT; il text si mostra all’operatore'],
        ['tipoFile, tipoContenutoFile, codice, descrizione, tipologia', 'Solo ANSC_LOG_AUDIT'],
    ], [2.4, 4.1])

    h(d, 3, 'Che cosa vede l’operatore')
    tabella(d, [
        ['Esito', 'Messaggio', 'Che cosa può fare'],
        ['EMESSO', '«Certificato emesso: n. <idCertificato>, valido fino al <data>.» Più gli '
         'eventuali avvisi di ANSC.', 'Scaricare o stampare il PDF; ristamparlo in seguito '
         'dalla pratica.'],
        ['RIFIUTATO per l’OTP', '«Il codice di sessione verso ANSC non è valido o è scaduto.»',
         'Richiedere un codice nuovo e ripetere: nessun certificato è stato emesso.'],
        ['RIFIUTATO per la firma', '«La firma remota non è riuscita.» Più il text di ANSC.',
         'Reinserire le credenziali di firma.'],
        ['RIFIUTATO', 'Il text di ANSC, per esempio il motivo per cui l’atto non è '
         'certificabile.', 'Correggere ciò che ANSC indica; non ripetere la stessa richiesta.'],
        ['DA_VERIFICARE', '«ANSC non ha dato un esito certo: il certificato potrebbe essere '
         'stato emesso.»', 'Ripetere sapendo che può nascere un secondo certificato, oppure '
         'segnalare. La ripetizione non è mai automatica (CE-08).'],
    ], [1.3, 2.9, 2.3])


if __name__ == '__main__':
    innesta_prima(paragrafo('Come si trasporta nelle schermate di SIPO', 'Heading 2')._p,
                  gestione)
    fatti.append('sezione «La gestione della risposta di R002»')
    p = paragrafo('Il contratto dichiara le risposte HTTP 200, 403 e 404')
    p.add_run(' Come si classifica la risposta e che cosa ne fa SIPO è nella sezione «La '
              'gestione della risposta di R002».')

    ce = tab('#', 'Questione', 'A chi spetta')
    for riga in [
        ('CE-26', 'Certificato emesso in ANSC ma non conservato in SIPO (errore fra la '
         'risposta e il salvataggio): R002 non permette di riscaricarlo per idCertificato. Se '
         'ANSC offra un modo di recuperarlo, o se il concentratore debba trattenere il PDF '
         'finché cert-be non ne conferma il salvataggio.', 'Presidio ANSC / Architettura'),
        ('CE-27', 'Significato di idEsito nella testata e del terzetto codice, descrizione, '
         'tipologia; quale prevalga sul codice HTTP se discordano.', 'Presidio ANSC / Sogei'),
    ]:
        D.clona_riga(ce, riga)
    fatti.append('CE-26 e CE-27')

    for f in D.frontespizio(d, '0.6', NOME, DATA):
        fatti.append(f)
    D.storia(d, DATA, '0.6', 'R002 in dettaglio · Punti aperti',
             'Nuova sezione sulla gestione della risposta di R002: risposta per intero con '
             'esempi, irregolarità del contratto, regole per decidere l’esito, passi del '
             'concentratore, di cert-be e della pagina, divieti sul PDF, destinazione di ogni '
             'dato, messaggi all’operatore; CE-26 e CE-27.')
    d.save(OUT)
    for f in fatti:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tb, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tb, fig))
