# -*- coding: utf-8 -*-
"""NON RIESEGUIRE: la v0.1 è stata rivista a mano dall'utente; la v0.2 la fa
`testo_libero_v0_2.py` sul file reale. Il punto sul rilascio 1.33.0 qui sotto è
superato: ANSC non dichiara escluso il deposito R009 (vedi v0.2).

Genera la v0.1 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC» (07/11/2026).

Documento di analisi dedicato agli atti a testo libero, ricavato dal capitolo «Atti a
Testo Libero» dell'analisi di integrazione v3.56 e dalla figura dei due percorsi
(DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC). Richiesta dell'utente: considerazioni sulle due
strategie, elenco dei servizi Rxxx da usare, e lo stesso tipo di atto quando non è
possibile identificare un UC.

Fatti verificati sulle sorgenti e che reggono il documento:
- In ANSC l'atto a testo libero si chiama «caso d'uso di servizio» (Guida operativa
  ANSC, cap. 7, p. 38): 25 nel catalogo ANSC_03, 10 per gli atti, 5 per le
  trascrizioni, 10 per le annotazioni. Nel mapping i file *_999 sono 17.
- Il mapping li fa reggere su `composizioneCompleta` (la minuta scritta dall'ufficiale)
  e, per i 10 di formazione, su `motivoRecupero` obbligatorio (ANSC_96: 3 = «Caso
  d'uso non previsto nel sistema centrale»). Morte_999: 14 campi obbligatori.
- Changelog 1.33.0 (03/10/2024): «Disabilitazione casi d'uso di servizio lato servizi
  cooperativi (ID 120)». È la ragione per cui entrambe le strategie passano dalla web
  app; la portata esatta è da verificare (la prenotazione dei gemelli usa 11999999).
- R005 /consultazione/ansc/evento accetta `idComunale` (numero comunale) e
  `idComuneRegistrazione`: il ritorno in SIPO può cercare l'atto per il numero
  staccato, senza farsi digitare l'identificativo nazionale.
- SIPO ha già l'atto a testo libero: MATR_USR.ATTO.FLG_ATTO_TESTOLIBERO e la tabella
  ATTO_TESTO_LIBERO (corpi, formule di cappello e di chiusura, firma, occhio), con la
  pagina comune di statocivile-web e gli endpoint di statocivile-be.

La figura è `img/testo_libero/strategie.png`, resa con Quick Look da
DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.2.pptx (nella v0.2 i nomi del servizio di
numerazione sono quelli della v3.54: be-numeratore-comunale, POST /richiesta).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_testo_libero.py
"""
import os
import shutil
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(QUI))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
NOME = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.1'
OUT = os.path.join(BASE, 'Documenti finali', NOME + '.docx')
FIGURA = os.path.join(QUI, 'img', 'testo_libero', 'strategie.png')

TAGLIA_DA = 29
DATA = '07/11/2026'


# ------------------------------------------------------------------ primitive
def testo(par, s):
    if par.runs:
        par.runs[0].text = s
        for r in par.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        par.add_run(s)


def pezzi_di(s):
    """«testo **grassetto** e `monospazio`» -> [(testo, grassetto, mono)]."""
    out = []
    for frammento, grassetto in D.segmenta('', s):
        for i, parte in enumerate(frammento.split('`')):
            if parte:
                out.append((parte, grassetto, i % 2 == 1))
    return out


def _versa(p, s, grassetto_forzato=False, dim=None, corsivo=False):
    for txt, grassetto, mono in pezzi_di(s):
        r = p.add_run(txt)
        r.bold = grassetto or grassetto_forzato
        r.italic = corsivo or None
        if mono:
            r.font.name = 'Courier New'
            r.font.size = Pt(dim - 1 if dim else 9)
        elif dim:
            r.font.size = Pt(dim)
    return p


def h(d, livello, t):
    p = d.add_paragraph(style='Heading %d' % livello)
    p.add_run(t)
    return p


def par(d, t, stile='Normal'):
    return _versa(d.add_paragraph(style=stile), t)


def voce(d, testa, corpo):
    p = d.add_paragraph(style='List Paragraph')
    _versa(p, testa + ' ', grassetto_forzato=True)
    return _versa(p, corpo)


def tabella(d, righe, larghezze=None):
    t = d.add_table(rows=len(righe), cols=len(righe[0]))
    t.style = 'Table Grid'
    for i, riga in enumerate(righe):
        for j, v in enumerate(riga):
            cel = t.cell(i, j)
            cel.text = ''
            _versa(cel.paragraphs[0], str(v), grassetto_forzato=(i == 0), dim=9)
    if larghezze:
        for j, w in enumerate(larghezze):
            for riga in t.rows:
                riga.cells[j].width = Inches(w)
        griglia = t._tbl.find(qn('w:tblGrid'))
        if griglia is not None:
            for col, w in zip(griglia.findall(qn('w:gridCol')), larghezze):
                col.set(qn('w:w'), str(int(round(Inches(w).twips))))
        t._tbl.tblPr.append(
            docx.oxml.parse_xml('<w:tblLayout %s w:type="fixed"/>' % docx.oxml.ns.nsdecls('w')))
    d.add_paragraph()
    return t


def figura(d, png, pollici, didascalia):
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(png, width=Inches(pollici))
    _versa(d.add_paragraph(), didascalia, dim=9, corsivo=True)


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
            testo(p, 'Gli atti a testo libero e gli atti senza caso d’uso: '
                     'le due strategie, il confronto e i servizi ANSC da usare')
    return d


# =================================================================== contenuti
RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[R1]', '`ANALISI_Integrazione-ANSC_v3.56.docx` — capitoli «Atti a Testo Libero», '
             '«SIPO in relazione alla web app ANSC» (l’aggancio di un atto formato sulla '
             'web app, lo stacco del numero comunale), «La numerazione comunale», '
             '«Il flusso operativo» e il registro degli Open Point.', 'Documento di progetto'],
    ['[R2]', '`DIAGRAMMI_Atti-Non-Gestiti-SIPO-ANSC_v0.2.pptx` — i due percorsi in '
             'PowerPoint, modificabili. La v0.2 riporta i nomi correnti del servizio di '
             'numerazione.', 'Diagramma di progetto'],
    ['[A1]', 'Guida operativa ANSC (`ansc/docs/Guida_operativa_ANSC.pdf`), cap. 7 «Casi '
             'd’uso di servizio» e cap. 8 «Registrazione atto (parto gemellare)».',
     'Documentazione ANSC'],
    ['[A2]', 'Guida operativa ANSC — Servizi di ausilio, cap. 3 «Altri servizi»: '
             'glossario, certificati emissibili per caso d’uso di servizio.',
     'Documentazione ANSC'],
    ['[A3]', 'Contratti dei servizi cooperativi ANSC (`ansc/docs/openapi/`, R001–R024, '
             'R901) e modello evento (`model_evento.yaml`).', 'Contratto di terzi'],
    ['[A4]', 'Catalogo dei casi d’uso (`Decodifiche/3_dec_use_case.csv`, ANSC_03), '
             'decodifiche ANSC_11 (stati) e ANSC_96 (motivo del recupero), mapping dei '
             'casi d’uso (`Mapping_casi_uso/`, file `*_999`).', 'Dati ANSC'],
    ['[A5]', '`ansc/docs/Changelog.md` — rilascio 1.33.0 del 03/10/2024 e voci sui casi '
             'd’uso di servizio.', 'Dati ANSC'],
    ['[S1]', 'Disegno Base Dati dello Stato Civile '
             '(`B9DA959E80-05-008-05-002_v1.00.docx`), tabelle `ATTO` (§2.2.162) e '
             '`ATTO_TESTO_LIBERO` (§2.2.193).', 'Documentazione SIPO'],
    ['[S2]', 'Codice SIPO: `statocivile-web` (`AttiTestoLiberoCommonController`), '
             '`statocivile-be` (`TestoLiberoControler`), entità `AttoMatr` e '
             '`AttoTestoLibero` di `matrim-entities`.', 'Sorgente applicativo'],
    ['[S3]', 'Manuale utente dello Stato Civile di SIPO (`RC_AS SIPO_Manuale_Utente_'
             'Stato_Civile.pdf`), pp. 83, 96, 114.', 'Documentazione SIPO'],
]

SIPO_OGGI = [
    ['Elemento', 'Dove', 'Che cosa fa'],
    ['`FLG_ATTO_TESTOLIBERO`', '`MATR_USR.ATTO`, CHAR(1)',
     'Contrassegna l’atto generato a testo libero. Il Disegno Base Dati precisa che '
     'l’anteprima ha un comportamento diverso e che il tipo atto **non è significativo** '
     'per il formulario, che prende un modello apposito [S1].'],
    ['`ATTO_TESTO_LIBERO`', 'tabella, una riga per atto',
     'Il testo dell’atto: `TESTO_CORPO_1` e `TESTO_CORPO_2` (CLOB), la formula di '
     'cappello e quella di chiusura (codice e testo), `FIRMA`, `OCCHIO` (usato per le '
     'nascite) [S1].'],
    ['Pagina comune del testo libero', '`statocivile-web`',
     'Compilazione, «definisci» (`/finalizzaAtto`), anteprima (`/generaAnteprimaAtto`), '
     '«chiudi» [S2].'],
    ['Servizi di lettura e scrittura', '`statocivile-be`',
     '`/getAttiTestoLiberoCommon` e `/upsertAttiTestoLiberoCommon` '
     '(`TestoLiberoControler.java:48` e `:78`) [S2].'],
    ['Tipi atto a testo libero', 'catalogo dei tipi atto',
     'Il manuale li elenca per la morte («Morte con testo libero»), la nascita e la '
     'cittadinanza («Cittadinanza a testo libero») [S3]; pagine dedicate esistono anche '
     'nei moduli di matrimoni, unioni civili e divorzi [S2].'],
]

UC_SERVIZIO = [
    ['Codice', 'Caso d’uso di servizio', 'Tipo contenuto'],
    ['11999999', 'Dichiarazioni di nascita', '1 — atto'],
    ['12999999', 'Riconoscimenti', '1 — atto'],
    ['1399', 'Trascrizioni di nascita', '3 — trascrizione'],
    ['2199', 'Dichiarazioni di morte', '1 — atto'],
    ['2299', 'Trascrizioni di morte', '3 — trascrizione'],
    ['319999', 'Matrimoni con rito civile', '1 — atto'],
    ['329999', 'Matrimoni con rito religioso', '1 — atto'],
    ['339999', 'Trascrizioni di matrimonio', '3 — trascrizione'],
    ['349999', 'Separazioni e divorzi', '1 — atto'],
    ['359999', 'Riconciliazioni', '1 — atto'],
    ['419999', 'Unioni civili', '1 — atto'],
    ['439999', 'Trascrizioni di unioni civili', '3 — trascrizione'],
    ['449999', 'Scioglimenti', '1 — atto'],
    ['51999', 'Dichiarazioni di cittadinanza', '1 — atto'],
    ['52999', 'Trascrizioni di cittadinanza', '3 — trascrizione'],
]

MORTE_999 = [
    ['Sezione del mapping', 'Campo del modello evento', 'Che cosa porta'],
    ['Composizione libera', '`composizioneCompleta`',
     'Il testo dell’atto scritto dall’ufficiale: è il cuore del caso d’uso.'],
    ['Formula', '`999.2.1`', 'La formula di servizio, unica.'],
    ['Formazione atto', '`numeroatto`, `dataformazione`, `ora`, `minuto`',
     'Il numero comunale e l’istante di formazione.'],
    ['Dati generali', '`motivoRecupero`',
     'Il motivo per cui l’atto arriva fuori dal percorso dei casi d’uso (ANSC_96).'],
    ['Deceduto', '`intestatari[0]`: nome, sesso, data di nascita, stato di nascita con '
                 'descrizione, nazionalità con descrizione',
     'Il minimo per identificare l’intestatario e rendere l’atto certificabile.'],
]

MOTIVI = [
    ['ANSC_96', 'Descrizione', 'Pertinenza'],
    ['1', 'Indisponibilità del sistema gestionale', 'SIPO fermo: non è un testo libero.'],
    ['2', 'Atto formato fuori da casa comunale', 'Fuori perimetro.'],
    ['3', 'Caso d’uso non previsto nel sistema centrale',
     '**È il motivo degli atti di questo documento**, in entrambi i casi d’origine.'],
    ['4', 'Indisponibilità del sistema centrale', 'ANSC fermo: non è un testo libero.'],
    ['5', 'Inefficacia atto per duplicazione', 'Disattivato (fine validità anteriore all’inizio).'],
    ['101', 'ALTRO', 'Da riservare ai casi che il motivo 3 non descrive.'],
]

ORIGINI = [
    ['Situazione', 'Quando si riconosce', 'Che cosa fa SIPO', 'Esito'],
    ['L’ufficiale sceglie un tipo atto a testo libero',
     'All’inizio, alla scelta del tipo atto.',
     'Non apre le maschere del tipo atto: porta l’ufficiale allo stacco del numero.',
     'Testo libero (Gestione 2).'],
    ['Nessuna condizione di applicabilità risponde per il tipo atto, e i dati sono corretti',
     'Al Riepilogo (fase B), dopo la compilazione.',
     'Mostra il Riepilogo senza UC, senza firmatari né allegati, e il messaggio di '
     'rinvio alla web app.',
     'Testo libero (Gestione 1, o deviazione verso la Gestione 2).'],
    ['Il caso non è previsto da ANSC (nessun UC del catalogo lo descrive)',
     'Al Riepilogo, o prima se il tipo atto è noto come scoperto.',
     'Come la riga precedente.',
     'Testo libero, motivo 3.'],
    ['Nessuna condizione risponde perché i dati sono sbagliati',
     'Al Riepilogo.',
     'Segnala la categoria «UC non determinato» e chiede di correggere.',
     '**Non** è un testo libero: si correggono i dati.'],
    ['L’UC esiste in ANSC ma il Comune non l’ha ancora configurato',
     'Al Riepilogo.',
     'Come «UC non determinato».',
     'Lacuna di configurazione: si colma la configurazione; il testo libero è un ripiego '
     'ammesso solo se l’atto non può attendere.'],
    ['Più condizioni rispondono con UC diversi',
     'Al Riepilogo.',
     'Categoria «UC ambiguo»: sceglie l’ufficiale, la scelta resta registrata.',
     '**Non** è un testo libero.'],
]

GESTIONE_1 = [
    ['#', 'Passo', 'Dove', 'Servizio', 'Stato'],
    ['1', 'Stesura dell’atto fino al Riepilogo, con la ricerca dell’intestatario.',
     'SIPO', 'R005 `/consultazione/ansc/intestatario`', 'SIPO: in lavorazione'],
    ['2', 'Il Riepilogo non trova un UC: niente firmatari né allegati; messaggio di rinvio '
          'alla web app.', 'SIPO', '—', '—'],
    ['3', 'Stacco del numero comunale.', 'SIPO',
     '`be-numeratore-comunale` `POST /richiesta`', 'numero: Disponibile'],
    ['4', 'Anteprima del testo generato da SIPO, per i soli tipi atto non a testo libero.',
     'SIPO', '— (anteprima di SIPO, non R010)', '—'],
    ['5', 'L’atto passa in attesa della stesura sulla web app.', 'SIPO', '—',
     'YY · SOSPESO'],
    ['6', 'Stesura sulla web app con il caso d’uso di servizio: si può copiare il testo '
          'generato da SIPO; i soggetti vanno reinseriti. Validazione, firme e chiusura '
          'avvengono sulla web app.', 'Web app ANSC', '— (funzioni della web app)',
     'ANSC: 5 FIRMATO DA USC'],
    ['7', 'Ritorno in SIPO e ricerca dell’atto appena formato.', 'SIPO',
     'R005 `/consultazione/ansc/evento`', '—'],
    ['8', 'Importazione dei dati: `idAnsc`, `idUsecase`, versione, testo, identificativi '
          'dei soggetti.', 'SIPO', '—', '—'],
    ['9', 'Conclusione del processo in SIPO.', 'SIPO',
     '`PUT /utilizza`', 'da definire (TL-04)'],
]

GESTIONE_2 = [
    ['#', 'Passo', 'Dove', 'Servizio', 'Stato'],
    ['1', 'L’ufficiale richiede la stesura di un tipo atto a testo libero.', 'SIPO', '—', '—'],
    ['2', 'Messaggio di rinvio alla web app.', 'SIPO', '—', '—'],
    ['3', 'Pagina nuova: stacco del numero comunale, a cui l’ufficiale è indirizzato '
          'direttamente.', 'SIPO', '`be-numeratore-comunale` `POST /richiesta`',
     'numero: Disponibile'],
    ['4', 'L’atto passa in attesa della stesura sulla web app.', 'SIPO', '—',
     'YY · SOSPESO'],
    ['5', 'Stesura sulla web app con qualsiasi UC — di servizio o ordinario —, '
          'validazione, firme e chiusura.', 'Web app ANSC',
     '— (funzioni della web app)', 'ANSC: 5 FIRMATO DA USC'],
    ['6', 'Ritorno in SIPO e ricerca dell’atto appena formato.', 'SIPO',
     'R005 `/consultazione/ansc/evento`', '—'],
    ['7', 'Importazione dei dati con la transcodifica di comuni, province e nazioni: '
          '`idAnsc`, testo, soggetti, `idSoggettoAnsc`, `idSoggettoAnpr`, `idAnpr`.',
     'SIPO', '—', '—'],
    ['8', 'Conclusione del processo in SIPO.', 'SIPO', '`PUT /utilizza`',
     'da definire (TL-04)'],
]

CONFRONTO = [
    ['Criterio', 'Gestione 1', 'Gestione 2'],
    ['Quando si riconosce il caso', 'Tardi: al Riepilogo, dopo l’intera compilazione.',
     'Subito: alla scelta del tipo atto.'],
    ['Immissioni dei dati', 'Due: in SIPO e di nuovo sulla web app.',
     'Una: sulla web app. SIPO li riceve importandoli.'],
    ['Probabilità di errore', 'Alta: due immissioni dello stesso dato possono divergere, '
                              'e nessun controllo le confronta.',
     'Bassa: il dato è uno e SIPO lo riceve da ANSC.'],
    ['Testo dell’atto', 'Generato da SIPO per i tipi atto ordinari e copiabile; per i tipi '
                        'a testo libero si scrive sulla web app.',
     'Si scrive sulla web app.'],
    ['Soggetti in SIPO', 'Già presenti dalla compilazione, con l’identificativo ANSC '
                         'dell’intestatario ottenuto da R005.',
     'Nascono dall’importazione: servono la transcodifica dei luoghi e la regola «solo se '
     'vuoto» verso l’anagrafe.'],
    ['Coerenza fra SIPO e ANSC', 'Da verificare: SIPO conserva i dati della propria '
                                 'stesura, ANSC quelli della seconda.',
     'Garantita per costruzione: SIPO riporta ciò che ANSC ha formato.'],
    ['Tempo allo sportello', 'Maggiore: la compilazione in SIPO è lavoro perso.',
     'Minore.'],
    ['Che cosa resta da costruire in SIPO',
     'Il Riepilogo senza UC, il messaggio, lo stato YY, il ritorno con R005, l’importazione.',
     'La pagina dello stacco, lo stato YY, il ritorno con R005, l’importazione con la '
     'transcodifica inversa.'],
    ['Riuso', 'Basso: vale per il solo caso scoperto al Riepilogo.',
     'Alto: è lo stesso percorso dell’aggancio di un atto formato sulla web app, e si '
     'presta anche agli UC meno complessi in caso di necessità [R1].'],
]

SERVIZI = [
    ['Servizio', 'Operazione', 'A che cosa serve', 'G1', 'G2', 'Note'],
    ['R005', '`/consultazione/ansc/intestatario`',
     'Ricerca dell’intestatario durante la compilazione in SIPO.', 'sì', '—',
     'Fa parte della fase A del percorso ordinario [R1].'],
    ['R005', '`/consultazione/ansc/evento`',
     'Ritrova l’atto formato sulla web app e ne restituisce il modello evento intero, '
     'da cui si importano i dati.', 'sì', 'sì',
     'Ricerca per `idComunale` (il numero staccato) e `idComuneRegistrazione`, con '
     '`dataDa`/`dataA`; oppure per `idAnsc`.'],
    ['R005', '`/consultazione/ansc/soggetto`',
     'Completa i dati di un soggetto importato, se il modello evento non basta.',
     'facolt.', 'facolt.', 'Da usare solo se l’importazione lo richiede.'],
    ['R001', '`/allegato/{version}`',
     'Recupera i documenti allegati all’atto, contenuto compreso, per registrarli in '
     '`ALLEGATO`.', 'facolt.', 'facolt.',
     'Serve se SIPO deve conservare o mostrare i documenti (RF-17 di [R1]).'],
    ['R014', '`/evento/data-validita`',
     'Registra la data di validità anagrafica dell’atto firmato, se sulla web app non è '
     'stata indicata.', 'cond.', 'cond.', 'Solo se mancante nel modello evento importato.'],
    ['R008', '`/notifiche/getNotificheByEvento`',
     'Verifica le notifiche generate dall’atto e la loro conferma.', 'facolt.', 'facolt.',
     'Supervisione: è il cancello della comunicazione anagrafica.'],
    ['R003', '`/comunicazione`',
     'Recupera le comunicazioni ad altri enti generate dall’atto.', 'facolt.', 'facolt.',
     'Come per gli atti formati da SIPO.'],
    ['R005', '`/consultazione/ansc/evento/note/tecniche`',
     'Rileva una nota tecnica fatta in seguito sull’atto.', 'facolt.', 'facolt.',
     'Per la riconciliazione su richiesta [R1].'],
    ['R901', '`/config/decodifica/dettaglio`',
     'Dizionari ANSC per la transcodifica inversa dei valori importati.', 'ind.', 'ind.',
     'Già caricati dal componente dei dizionari: SIPO li legge in locale.'],
]

NON_DA_SIPO = [
    ['Servizio', 'Perché non lo chiama SIPO in queste strategie'],
    ['R009 `/validazione/evento`', 'Il deposito avviene sulla web app. Con un caso d’uso '
                                   'di servizio la via cooperativa è disabilitata dal '
                                   'rilascio 1.33.0 [A5].'],
    ['R010 `/anteprima/evento`', 'L’anteprima dell’atto la mostra la web app. Quella del '
                                 'passo 4 della Gestione 1 è l’anteprima di SIPO.'],
    ['R006 / R012', 'Le firme dei dichiaranti si raccolgono sulla web app.'],
    ['R007 `/firma_usc`, `/attestazione/firma`', 'La firma dell’ufficiale e quella '
                                                  'dell’attestazione di conformità si '
                                                  'appongono sulla web app.'],
    ['R011 `/evento/elimina`', 'Una bozza abbandonata sulla web app si cancella lì. SIPO '
                               'ne conosce l’esistenza solo dopo il ritorno.'],
]

TERZO = [
    ['#', 'Passo', 'Servizio ANSC'],
    ['1', 'Ricerca dell’intestatario.', 'R005 `/consultazione/ansc/intestatario`'],
    ['2', 'Caricamento dei documenti e attesa della scansione.',
     'R001 `/allegato/upload`, `/allegato/verifica`'],
    ['3', 'Stacco del numero comunale.', '`be-numeratore-comunale` `POST /richiesta`'],
    ['4', 'Testo dalla pagina del testo libero di SIPO in `composizioneCompleta`; '
          'anteprima.', 'R010 `/anteprima/evento`'],
    ['5', 'Deposito con `idUsecase` di servizio e `motivoRecupero` = 3.',
     'R009 `/validazione/evento`'],
    ['6', 'Firme dei dichiaranti.', 'R006 oppure R012'],
    ['7', 'Attestazione di conformità, se dovuta.',
     'R010 `/anteprima/attestazione`, R007 `/attestazione/firma`'],
    ['8', 'Firma dell’ufficiale e chiusura.', 'R007 `/firma_usc`, R014 `/evento/data-validita`'],
    ['—', 'Cancellazione prima della firma dell’ufficiale.', 'R011 `/evento/elimina`'],
]

DISEGNO = [
    ['Struttura', 'Che cosa serve'],
    ['`ANSC_STATO_ATTO`', 'Lo stato «YY · SOSPESO» fra gli stati applicativi, con il nome '
                          'e il codice da assegnare (TL-03); l’`ID_STATO` ANSC resta '
                          'vuoto finché l’atto non torna.'],
    ['`ANSC_STATO_ATTO.ID_MOTIVO_RECUPERO`', 'Valorizzato all’importazione dal modello '
                                             'evento (atteso 3).'],
    ['`MATR_USR.ATTO.FLG_ATTO_TESTOLIBERO`', 'Posto a 1 all’importazione, perché l’atto '
                                             'sia riconoscibile come tale in SIPO.'],
    ['`ATTO_TESTO_LIBERO`', 'Riceve `composizioneCompleta`. La divisione in corpi e '
                            'formule non è ricostruibile: il testo va per intero nel primo '
                            'corpo (TL-06).'],
    ['`ANSC_SOGGETTO_IDENTIFICATIVI`, `ANAG_USR.SOGGETTO`', 'Gli identificativi dei '
                                                            'soggetti importati, con la '
                                                            'regola «solo se vuoto» verso '
                                                            'l’anagrafe [R1].'],
    ['`DATI_ATTO_ESTERNO`', 'Il numero passa a Utilizzato con l’identificativo nazionale, '
                            'poi a 4 «Evento acquisito»: le due operazioni mancano nel '
                            'servizio (OP-79 di [R1]).'],
    ['Back-office', 'Una categoria di eccezione «In attesa della stesura sulla web app», '
                    'con l’anzianità in evidenza, e l’abbandono che porta il numero a '
                    'Scartato (`PUT /scarta`).'],
]

APERTI = [
    ['#', 'Questione', 'Chi decide'],
    ['TL-01', 'Quale strategia adottare: Gestione 2 come percorso unico, con la Gestione 1 '
              'ridotta a deviazione verso di essa (proposta di questo documento), oppure '
              'entrambe.', 'Cliente'],
    ['TL-02', 'Portata della disabilitazione dei casi d’uso di servizio sui servizi '
              'cooperativi (rilascio 1.33.0): se valga per tutti, per il deposito o anche '
              'per le altre operazioni, e se sia riattivabile per un gestionale. La '
              'prenotazione dei gemelli crea atti con il caso d’uso di servizio '
              '11999999. Se la via cooperativa fosse aperta, il terzo percorso '
              'diventerebbe possibile.', 'Fornitore ANSC'],
    ['TL-03', 'Codice e nome dello stato «YY · SOSPESO», e suo posto fra gli stati '
              'applicativi di `ANSC_STATO_ATTO`.', 'Analisi'],
    ['TL-04', 'Conclusione del processo in SIPO: stato dell’atto SIPO dopo l’importazione '
              '(definito, chiuso), chi lo conclude, se serve una conferma dell’ufficiale.',
     'Analisi / Cliente'],
    ['TL-05', 'Transcodifica inversa ANSC → SIPO: i dizionari di riconciliazione vanno da '
              'SIPO ad ANSC e la corrispondenza inversa può non essere univoca. Per i '
              'luoghi vale il codice ANPR o ISTAT; per gli altri domini va stabilita.',
     'Analisi'],
    ['TL-06', 'Collocazione del testo importato in `ATTO_TESTO_LIBERO` (primo corpo, '
              'formule vuote) e resa dell’anteprima di SIPO su un testo non composto da SIPO.',
     'Analisi / Sviluppo'],
    ['TL-07', 'Termine massimo di permanenza nello stato YY e sorte del numero staccato '
              'per un atto mai formato.', 'Cliente'],
    ['TL-08', 'Se l’uso della Gestione 2 con UC ordinari per gli UC meno complessi sia '
              'ammesso, e in quali casi: è una scelta organizzativa.', 'Cliente'],
    ['TL-09', 'Rapporto con `ALLEGATO.fg_testo_libero`: quel contrassegno indica un '
              'documento allegato, non un atto a testo libero; il nome si presta alla '
              'confusione (si lega a OP-71 di [R1]).', 'Analisi'],
    ['TL-10', 'Quali certificati rendere emissibili per l’atto con caso d’uso di servizio: '
              'si sceglie solo sulla web app (certificato semplice, estratto per '
              'riassunto) [A2].', 'Cliente'],
]


# ===================================================================== testo
def scrivi(d):
    # ------------------------------------------------------------------- 1
    h(d, 1, 'Scopo del documento')
    par(d, 'Il documento tratta gli **atti a testo libero**: gli atti il cui testo è '
           'scritto dall’Ufficiale di Stato Civile e non composto dal sistema a partire '
           'da un caso d’uso. Lo stesso percorso vale per gli atti di cui **non è '
           'possibile identificare un caso d’uso**: in entrambi i casi l’atto non può '
           'seguire il percorso automatico che SIPO segue per gli altri atti.')
    par(d, 'Riprende il capitolo «Atti a Testo Libero» dell’analisi di integrazione '
           '[R1], con le due strategie proposte, e lo sviluppa in quattro direzioni: '
           'che cosa sono questi atti in SIPO e in ANSC, quando si ricorre a essi, che '
           'cosa distingue le due strategie e quale conviene, quali servizi ANSC '
           'occorrono. Le decisioni ancora da prendere sono raccolte in coda, come punti '
           'aperti TL-01…TL-10.')
    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 5.0, 1.3])

    # ------------------------------------------------------------------- 2
    h(d, 1, 'Che cos’è un atto a testo libero')
    h(d, 2, 'In SIPO: una funzione che esiste già')
    par(d, 'SIPO conosce già l’atto a testo libero, in tutte le aree dello stato civile. '
           'L’atto porta un contrassegno, il testo sta in una tabella propria e una '
           'pagina comune ne gestisce compilazione, anteprima e chiusura:')
    tabella(d, SIPO_OGGI, [1.6, 1.5, 3.8])
    par(d, 'Ne discende un dato utile per il seguito: SIPO non ha bisogno di una '
           'struttura nuova per **conservare** un atto a testo libero. Gli serve un modo '
           'per **formarlo in ANSC**, ed è lì che sta il problema.')

    h(d, 2, 'In ANSC: il caso d’uso di servizio')
    par(d, 'ANSC non usa l’espressione «testo libero». Lo strumento corrispondente è il '
           '**caso d’uso di servizio**, che la guida operativa descrive così [A1]: '
           '«consentono di registrare eventi generici e casi particolari, di cui non '
           'esiste la categoria specifica codificata nell’albero dei casi d’uso. Si '
           'tratta di casi d’uso liberi che consentono di acquisire i soli dati '
           'strettamente indispensabili ai fini dell’emissione della certificazione […] '
           'le formule da utilizzare nella minuta dell’evento sono libere; potrai '
           'scrivere manualmente la minuta dell’atto».')
    par(d, 'Il catalogo ANSC_03 ne conta **25**: uno per tipologia di evento e per '
           'macrocategoria, cioè **10 per la formazione di atti, 5 per le trascrizioni e '
           '10 per le annotazioni** [A4]. Questi ultimi registrano solo annotazioni di '
           'tipo integrativo e non riguardano il presente documento. I quindici '
           'pertinenti:')
    tabella(d, UC_SERVIZIO, [1.1, 3.6, 1.6])
    par(d, 'Il mapping ne dichiara la struttura nei file `*_999` (diciassette: i '
           'matrimoni hanno più varianti). Pochi campi sono obbligatori, e reggono '
           'tutti su due elementi: la **minuta**, cioè il testo scritto dall’ufficiale, e '
           'il **motivo del recupero**. Per la morte (`Morte_999`) gli obbligatori sono '
           'quattordici:')
    tabella(d, MORTE_999, [1.5, 2.6, 2.8])
    par(d, 'Il motivo del recupero è obbligatorio in tutti i dieci casi d’uso di '
           'servizio di formazione, e solo in quelli [A4]. Dice ad ANSC perché l’atto '
           'arriva fuori dall’albero dei casi d’uso. Per gli atti di questo documento il '
           'valore è il 3:')
    tabella(d, MOTIVI, [0.8, 2.6, 3.5])
    par(d, 'Due caratteristiche del caso d’uso di servizio contano per il disegno. La '
           'prima: quali certificati l’atto possa produrre (certificato semplice, '
           'estratto per riassunto) si decide **per singolo atto**, con una funzione che '
           'esiste solo sulla web app [A2]. L’estratto integrale è sempre disponibile. '
           'La seconda: i dati facoltativi possono restare vuoti, quindi **un atto formato '
           'con il caso d’uso di servizio porta di norma meno dati** di uno formato con '
           'il caso d’uso specifico. Lo si ritrova al momento dell’importazione in SIPO.')

    h(d, 2, 'Perché si passa dalla web app')
    par(d, 'Il rilascio ANSC 1.33.0 del 03/10/2024 registra fra le funzioni aggiunte la '
           '«**Disabilitazione casi d’uso di servizio lato servizi cooperativi** (ID 120)» '
           '[A5]. Un gestionale comunale, quindi, non può depositare con R009 un atto con '
           'caso d’uso di servizio: lo forma la web app. È la ragione per cui entrambe '
           'le strategie del capitolo successivo passano dalla web app, e il motivo '
           'per cui la pagina del testo libero di SIPO, da sola, non basta.')
    par(d, 'La portata della disabilitazione non è descritta oltre quella riga, e un '
           'elemento ne rende incerto il confine: la prenotazione degli identificativi '
           'per il parto plurimo, che è un servizio cooperativo (R009 `/prenota/evento`), '
           'predispone atti con il caso d’uso di servizio 11999999 [A1]. Va chiesto al '
           'fornitore ANSC (TL-02). Se la via cooperativa risultasse aperta, si '
           'aprirebbe un terzo percorso, descritto più avanti.')

    # ------------------------------------------------------------------- 3
    h(d, 1, 'Quando si ricorre al testo libero')
    par(d, 'Le origini sono due. Nella prima l’ufficiale **sceglie** un tipo atto a '
           'testo libero, e il caso è noto fin dall’inizio. Nella seconda l’ufficiale '
           'compila un tipo atto ordinario e solo al Riepilogo, dove si determina l’UC, '
           '**scopre** che nessun UC si applica. È il punto (b) di OP-78 dell’analisi '
           '[R1], che per questo caso lasciava il percorso senza esito.')
    par(d, 'La seconda origine va però delimitata con cura, perché «nessun UC» ha cause '
           'diverse e solo alcune portano al testo libero:')
    tabella(d, ORIGINI, [1.8, 1.4, 2.0, 1.7])
    par(d, 'La regola che ne discende: **il testo libero è l’esito di un caso che ANSC '
           'non prevede, non il rimedio a un dato sbagliato o a una configurazione '
           'incompleta.** Se diventasse il ripiego ordinario per ogni «UC non '
           'determinato», gli atti formati con il caso d’uso di servizio crescerebbero '
           'proprio dove la configurazione è più debole, e con loro gli atti che portano '
           'meno dati. Per questo il messaggio di rinvio alla web app va mostrato solo '
           'dopo che i dati sono stati confermati, e la categoria «UC non determinato» '
           'del back-office resta distinta da quella degli atti in attesa della web app.')

    # ------------------------------------------------------------------- 4
    h(d, 1, 'Le due strategie proposte')
    par(d, 'L’analisi [R1] propone due modalità, che la figura mette a confronto su tre '
           'corsie: SIPO, lo stato dell’atto, la web app ANSC. In entrambe l’atto si forma '
           'sulla web app e il numero comunale esce da SIPO, perché SIPO è l’unico luogo in '
           'cui la serie è governata [R1]. Cambia il momento in cui il caso si riconosce, '
           'e con esso quante volte si immettono i dati.')
    figura(d, FIGURA, 6.5,
           'Figura 1 — Gli atti che SIPO non gestisce in automatico: i due percorsi '
           'attraverso la web app ANSC [R2].')

    h(d, 2, 'Gestione 1 — l’atto scoperto al Riepilogo')
    par(d, 'Vale per i tipi atto **non** a testo libero: l’atto si compila in SIPO, e '
           'l’assenza di un UC emerge al Riepilogo. L’atto si forma poi sulla web app con '
           'il caso d’uso di servizio. L’analisi la qualifica come onerosa e rischiosa.')
    tabella(d, GESTIONE_1, [0.3, 2.9, 0.9, 1.6, 1.2])

    h(d, 2, 'Gestione 2 — l’atto a testo libero riconosciuto alla richiesta')
    par(d, 'Vale per i tipi atto a testo libero: il caso si riconosce alla richiesta, '
           'SIPO stacca il numero e manda l’ufficiale sulla web app, dove l’atto si stende '
           'con qualsiasi UC. Al ritorno SIPO importa ciò che ANSC ha formato.')
    tabella(d, GESTIONE_2, [0.3, 2.9, 0.9, 1.6, 1.2])

    # ------------------------------------------------------------------- 5
    h(d, 1, 'Considerazioni sulle due strategie')
    h(d, 2, 'Il confronto')
    tabella(d, CONFRONTO, [1.5, 2.7, 2.7])
    par(d, 'L’analisi [R1] trae già la conclusione principale: la Gestione 2 riduce gli '
           'errori, perché i dati si immettono una volta sola, come la minuta. Il '
           'recupero da ANSC con R005 popola le tabelle di SIPO con soggetti compatibili '
           'con ANSC per costruzione, al prezzo di una transcodifica dei luoghi. E lo '
           'stesso percorso si presta agli UC meno complessi, quando serve.')

    h(d, 2, 'Le due strategie non sono alternative fra loro')
    par(d, 'Il confronto va letto con un’avvertenza. Le due strategie non rispondono '
           'allo stesso caso: la Gestione 2 presuppone che il testo libero sia noto alla '
           'richiesta, la Gestione 1 nasce perché non lo è. Scegliere la Gestione 2 non '
           'elimina quindi il caso scoperto al Riepilogo: lo lascia senza percorso.')
    par(d, 'La proposta di questo documento è di adottare **la Gestione 2 come percorso '
           'unico** e di ridurre la Gestione 1 a una **deviazione verso di essa**:')
    voce(d, 'Al Riepilogo senza UC',
         'SIPO non chiede di completare la stesura: stacca il numero e porta l’atto '
         'nello stato YY, come nella Gestione 2. Il testo generato da SIPO resta '
         'disponibile da copiare, ma i dati non si considerano definitivi.')
    voce(d, 'Al ritorno',
         'L’importazione è quella della Gestione 2, e **i dati di ANSC prevalgono**. I '
         'dati compilati in SIPO servono da riscontro: dove divergono da quelli importati, '
         'SIPO lo segnala all’ufficiale invece di scegliere da sé.')
    voce(d, 'Un solo meccanismo',
         'Il ritorno è lo stesso dell’aggancio di un atto formato sulla web app — per un '
         'fermo di SIPO o per un caso non configurato — che l’analisi già prevede [R1]. '
         'Tre situazioni, un percorso di ritorno, una sola importazione da costruire e '
         'collaudare.')
    par(d, 'Così la doppia immissione non scompare: diventa un **controllo**. Il prezzo è '
           'accettare che, nel caso scoperto tardi, il lavoro fatto in SIPO serva da '
           'riscontro e non da fonte.')

    h(d, 2, 'I punti deboli comuni, e come mitigarli')
    voce(d, 'Il ritorno può non avvenire.',
         'Fra lo stacco del numero e il ritorno l’atto è sospeso, e nulla costringe '
         'l’ufficiale a tornare. Servono una categoria di eccezione nel back-office con '
         'l’anzianità in evidenza e un termine massimo, scaduto il quale il numero si '
         'scarta (TL-07). È lo stesso presidio previsto per la modalità di emergenza '
         '[R1].')
    voce(d, 'L’atto va ritrovato senza ambiguità.',
         'Chiedere all’ufficiale di digitare l’identificativo nazionale espone a un errore '
         'che porterebbe dentro SIPO l’atto sbagliato. R005 accetta come criterio il '
         '**numero comunale** (`idComunale`) e il comune di registrazione: SIPO conosce il '
         'numero che ha staccato, quindi può cercare l’atto da sé e chiedere all’ufficiale '
         'solo una conferma. Il riscontro fra numero staccato e numero dell’atto trovato '
         'è anche il controllo che l’ufficiale abbia usato il numero giusto.')
    voce(d, 'La transcodifica va al contrario.',
         'I dizionari di riconciliazione sono costruiti da SIPO verso ANSC. Importando si '
         'percorrono all’inverso, e la corrispondenza inversa può non essere univoca: più '
         'valori di SIPO verso uno di ANSC. Per comuni, province e stati esteri regge il '
         'codice ANPR o ISTAT; per gli altri domini la regola va stabilita (TL-05).')
    voce(d, 'L’atto importato porta pochi dati.',
         'Con il caso d’uso di servizio i soli obbligatori sono intestatario, minuta, '
         'numero e formazione. SIPO deve accettare un atto incompleto rispetto alle '
         'proprie maschere senza bloccarne la conclusione, e le sue funzioni successive '
         '(ricerca, certificazione, annotazioni) vanno verificate su questi atti.')
    voce(d, 'L’atto può cambiare dopo il ritorno.',
         'Una nota tecnica sulla web app corregge l’atto senza passare da SIPO. Vale la '
         'regola già adottata: la riconciliazione si fa su richiesta, e chi corregge la '
         'riconcilia subito dopo [R1].')

    h(d, 2, 'Il terzo percorso, se ANSC lo consente')
    par(d, 'SIPO ha già la pagina del testo libero, e il caso d’uso di servizio chiede '
           'poco più della minuta. Se il fornitore ANSC confermasse che il deposito '
           'cooperativo del caso d’uso di servizio è ammesso (TL-02), l’atto a testo libero '
           'potrebbe formarsi **interamente in SIPO**, senza andare sulla web app e senza '
           'importazione:')
    tabella(d, TERZO, [0.3, 3.6, 3.0])
    par(d, 'Sarebbe il percorso più coerente con un sistema che resta SIPO-centrico: un '
           'solo luogo di immissione, nessuno stato sospeso, nessuna transcodifica '
           'inversa. Con la disabilitazione del rilascio 1.33.0 non è praticabile, ed è '
           'riportato qui perché la risposta del fornitore decide se riprenderlo.')

    # ------------------------------------------------------------------- 6
    h(d, 1, 'I servizi ANSC da utilizzare')
    par(d, 'Nelle due strategie SIPO non deposita e non firma: lo fa la web app. I '
           'servizi che SIPO chiama sono quindi quasi tutti **letture**, concentrate nel '
           'ritorno. Nelle colonne G1 e G2, «sì» indica il servizio necessario, «cond.» '
           'quello necessario solo in una condizione, «facolt.» quello facoltativo, '
           '«ind.» quello usato indirettamente.')
    tabella(d, SERVIZI, [0.5, 1.6, 2.1, 0.4, 0.4, 1.9])
    par(d, 'Accanto ai servizi ANSC, le strategie usano il servizio della numerazione '
           '`be-numeratore-comunale` [R1]: `POST /richiesta` allo stacco, `PUT /utilizza` '
           'alla conclusione, `PUT /scarta` all’abbandono. Il passaggio a 4 «Evento '
           'acquisito» e la registrazione dell’identificativo nazionale sul numero non '
           'hanno un’operazione: è OP-79 dell’analisi.')
    h(d, 2, 'I servizi che SIPO non chiama')
    par(d, 'Per completezza, i servizi della formazione che nelle due strategie esegue la '
           'web app, e che SIPO non chiama:')
    tabella(d, NON_DA_SIPO, [2.2, 4.7])

    # ------------------------------------------------------------------- 7
    h(d, 1, 'Effetti sul disegno')
    par(d, 'Che cosa le strategie richiedono al modello dati e al back-office '
           'dell’integrazione [R1]:')
    tabella(d, DISEGNO, [2.3, 4.6])

    # ------------------------------------------------------------------- 8
    h(d, 1, 'Punti aperti')
    par(d, 'Dieci questioni restano da chiudere. La prima è la scelta della strategia; '
           'la seconda decide se esista un terzo percorso; le altre servono a completare '
           'il disegno qualunque sia la scelta. I punti si legano a OP-66, OP-71, OP-78 e '
           'OP-79 dell’analisi di integrazione [R1].')
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
             'Prima stesura, dal capitolo «Atti a Testo Libero» dell’analisi di '
             'integrazione v3.56. Atti a testo libero in SIPO e casi d’uso di servizio in '
             'ANSC; quando si ricorre al testo libero, compreso l’UC non determinabile; le '
             'due strategie con il confronto e la proposta di un percorso unico; il terzo '
             'percorso condizionato alla risposta del fornitore; i servizi ANSC da usare; '
             'effetti sul disegno; dieci punti aperti.')


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
