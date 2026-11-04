# -*- coding: utf-8 -*-
"""Genera la v0.4 di «STUDIO_Identificativi-ANSC-verso-ANPR».

La v0.4 cambia perimetro su indicazione del committente: **si tratta soltanto
l'identificativo dell'ATTO**. Ogni riferimento all'identificativo del soggetto è
rimosso — spariscono il capitolo sulla Predisposizione Anagrafica e la metà della
risposta che lo riguardava — e al loro posto entra il merito della richiesta nuova:
**dove intervenire nei processi schedulati** per renderli compatibili con gli atti
formati in ANSC.

Tre correzioni sostanziali rispetto alla v0.3, tutte verificate:

1. Gli schemi imbarcati nel client NON sono anteriori ad ANSC. Il `tipoDato.xsd` del
   modulo e quello della 9.2.9 concordano su ogni nome ANSC (`tipoAttoANSC` 4 e 4) e
   divergono per due soli complexType, entrambi sulla poligamia. Lo scostamento reale
   è puntuale: tre slot in `1000iscrizione.xsd`, e nient'altro su otto schemi.
2. La divergenza fra XSD imbarcati e Java generato esiste ma va nei DUE sensi: per
   `tipoAttoANSC` ci sono entrambi; per `attoNascitaANPR` dell'AIRE c'è l'XSD e manca
   il campo nella classe. È questo il fatto da dichiarare a chi rigenera.
3. I punti del client che trattano la forma ANSC sono QUATTRO, non due.

Risultato che vale la pena non riscoprire: la commutazione del client legge **cinque
colonne** di `ANAG_USR.ATTO`, non una. Valorizzare il solo `ID_ATTO_ANSC` produce un
payload invalido, perché comune, anno e numero comunale sono obbligatori nello schema.

Gli apici inversi del sorgente diventano Courier New: nella v0.3 ne sono finiti 128
letterali nel documento consegnato.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/idansc_v0_4.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
OUT = os.path.join(BASE, 'Documenti finali',
                   'STUDIO_Identificativi-ANSC-verso-ANPR_v0.4.docx')

TAGLIA_DA = 29
DATA = '30/10/2026'


# ------------------------------------------------------------------ primitive
def testo(par, s):
    if par.runs:
        par.runs[0].text = s
        for r in par.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        par.add_run(s)


def pezzi_di(s):
    """«testo **grassetto** e `monospazio`» -> [(testo, grassetto, mono)].

    La v0.3 usava la sola `segmenta` di docx_comune, che conosce `**` e lascia
    passare gli apici inversi: nel documento consegnato ne sono rimasti 128
    letterali. Qui l'apice inverso diventa Courier New.
    """
    out = []
    for frammento, grassetto in D.segmenta('', s):
        for i, parte in enumerate(frammento.split('`')):
            if parte:
                out.append((parte, grassetto, i % 2 == 1))
    return out


def _versa(p, s, grassetto_forzato=False, dim=None):
    for txt, grassetto, mono in pezzi_di(s):
        r = p.add_run(txt)
        r.bold = grassetto or grassetto_forzato
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
    # La testa passa dall'interprete come il corpo: nella prima stesura della v0.4
    # restavano 12 apici inversi letterali, tutti provenienti da qui.
    p = d.add_paragraph(style='List Paragraph')
    _versa(p, testa + ' ', grassetto_forzato=True)
    return _versa(p, corpo)


def codice(d, righe):
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()


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
            testo(p, 'L’identificativo dell’atto ANSC verso ANPR: dove si '
                     'interviene nel client, nel concentratore e nei processi schedulati')
    return d


# =================================================================== contenuti
RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[S1]', '`common/anpr-client` — il client ANPR di SIPO: tipi generati dallo '
             'schema Sogei, generatori XML delle richieste, utilità comuni, schemi '
             'imbarcati in `src/main/wsdl`.', 'Sorgente applicativo'],
    ['[S2]', '`back-end/all-anpr-sipo` — il concentratore verso ANPR per lo stato '
             'civile: endpoint di allineamento e i due convertitori `Convert` e '
             '`ConvertSC`.', 'Sorgente applicativo'],
    ['[S3]', '`back-end/all-nas-be`, `all-dec-be`, `all-matr-be` — i tre processi '
             'schedulati di allineamento verso ANPR per nascite, decessi e cittadinanza, '
             'matrimoni.', 'Sorgente applicativo'],
    ['[S4]', '`back-end/int-be` — il processo che alimenta la coda degli eventi da '
             'allineare; `back-end/prog-be` e `back-end/cri-on-anpr-be` — i processi '
             'schedulati dell’elettorale e dei cambi di residenza online.',
     'Sorgente applicativo'],
    ['[S5]', '`common/anagrafe-entities` — le entità di `ANAG_USR`, fra cui '
             '`ATTO` con le colonne di ANSC, e la logica che le scrive e le azzera.',
     'Sorgente applicativo'],
    ['[S6]', '`back-end/varana-be` e `back-end/matrim-be` — i back-end da cui '
             'l’identificativo dell’atto ANSC entra oggi in SIPO.',
     'Sorgente applicativo'],
    ['[A1]', 'Documentazione ufficiale ANPR, versione 9.2.9 — WSDL e XSD dei servizi '
             'ai comuni in `src/wsdl/comuni/`. È il contratto, e non coincide con gli '
             'schemi imbarcati nel client.', 'Contratto di terzi'],
    ['[R1]', '`ANALISI_Integrazione-ANSC` (versione corrente) — il disegno della '
             'formazione degli atti su ANSC, da cui proviene la nozione di identificativo '
             'nazionale dell’atto.', 'Documento di progetto'],
]

TIPO_ATTO_ANSC = [
    ['Elemento', 'Tipo nello schema', 'Obbl.', 'Che cos’è'],
    ['idANSC', 'tipoNumeroAttoANSC', 'sì',
     'L’identificativo nazionale dell’atto formato in ANSC.'],
    ['comuneRegistrazione', 'tipoComune', 'sì',
     'Il comune che ha registrato l’atto.'],
    ['anno', 'numerico4', 'sì', 'L’anno dell’atto.'],
    ['numeroComunale', 'tipoNumeroAtto', 'sì',
     'Il numero attribuito dal Comune. È obbligatorio: la forma ANSC **non '
     'sostituisce la numerazione comunale**, la accompagna.'],
    ['ufficioMunicipio', 'tipoUfficioMunicipio', 'no', 'L’ufficio o il municipio.'],
    ['dataFormazioneAtto', 'tipoDataAnagrafica', 'no',
     'La data in cui l’atto è stato formato.'],
    ['trascritto', 'numerico1', 'no',
     'Il contrassegno di atto trascritto perché formato altrove.'],
]

OPERAZIONI = [
    ['Operazione ANPR', 'Posto nello schema del client', 'Classe Java generata',
     'Codice che lo valorizza'],
    ['**5008** mutazione dei dati generali di stato civile — atto di nascita',
     'sì', 'sì', '**sì**'],
    ['**5008** mutazione — evento di morte', 'sì', 'sì', '**sì**'],
    ['**2001** cancellazione per morte', 'sì, per il tramite di `tipoDatiEvento`',
     'sì', '**sì**'],
    ['Altri eventi che passano da `tipoDatiEvento` (scioglimento di unione civile)',
     'sì', 'sì', '**sì**'],
    ['**A001 / A002** iscrizione AIRE', 'sì — `A000aire.xsd:46` e `:112`',
     '**no**: `RichiestaA001.java` porta il solo `attoNascita`', 'no'],
    ['**1001 / 1002** iscrizione in anagrafe',
     '**no** — i tre slot esistono in [A1] e mancano nel client', 'no', 'no'],
    ['2000 cancellazione (altri motivi), 3000 consultazione, P000 servizi al cittadino',
     'nessuno slot, in entrambi gli alberi', '—', '—'],
]

SCOSTAMENTO = [
    ['Schema di operazione', 'Slot nel client', 'Slot in [A1]', 'Esito'],
    ['`1000iscrizione.xsd`', '0', '3', '**mancano tre slot nel client**'],
    ['`2000cancellazione.xsd`', '0', '0', 'allineato'],
    ['`3000consultazione.xsd`', '0', '0', 'allineato'],
    ['`4000estrazione.xsd`', '5', '5', 'allineato'],
    ['`5000mutazione.xsd`', '2', '2', 'allineato'],
    ['`6001certificazione.xsd`', '1', '1', 'allineato'],
    ['`A000aire.xsd`', '2', '2', 'allineato'],
    ['`P000sc.xsd`', '0', '0', 'allineato'],
]

COLONNE = [
    ['Colonna di `ANAG_USR.ATTO`', 'Campo di `Atto.java`', 'Dove finisce nel payload',
     'Obbl. nello schema'],
    ['`ID_ATTO_ANSC` (riga 161)', '`idAttoAnsc`',
     '`idANSC`, e **è il contrassegno della commutazione**', 'sì'],
    ['`ID_COMUNE` (riga 169)', '`comune`', '`comuneRegistrazione`', 'sì'],
    ['`ANNO_ANSC` (riga 164)', '`annoAnsc`', '`anno`', 'sì'],
    ['`NUMERO_COMUNALE` (riga 175)', '`numeroComunale`', '`numeroComunale`', 'sì'],
    ['`DATA_ANSC` (riga 180)', '`dataAnsc`', '`dataFormazioneAtto`', 'no'],
    ['`NUMERO_NAZIONALE` (riga 172)', '`numeroNazionale`',
     'in nessun punto: la commutazione non lo legge', '—'],
]

BATCH = [
    ['Processo', 'Modulo', 'Orario', 'Che cosa fa', 'Porta atti di stato civile'],
    ['Alimentazione della coda degli eventi', '`int-be`, `BatchModController:38`',
     '23:00', 'Elabora le modifiche della giornata e lascia gli eventi da allineare nella '
     'coda che i tre processi delle 05:00 consumano.',
     'no: non chiama ANPR, prepara il lavoro'],
    ['Allineamento nascite', '`all-nas-be`, `AllineamentoNasciteBL:34`', '05:00',
     'Per ogni evento di nascita, annullamento o rettifica recupera i dati anagrafici e '
     'chiede al concentratore l’allineamento. Il concentratore sceglie fra '
     '**1001, 1002, A001, A002, A006** per l’iscrizione e **5008** per la mutazione.',
     '**sì**'],
    ['Allineamento decessi e cittadinanza',
     '`all-dec-be`, `AllineamentoDecCittBL:32`', '05:00',
     'Decesso, annullamento di decesso, vedovanza, annullamento di vedovanza, '
     'cittadinanza. Il concentratore usa **2001, 2003, 2011, 5001, 5008**.',
     '**sì**'],
    ['Allineamento matrimoni e unioni civili',
     '`all-matr-be`, `AllineamentoMatrimonioBL:29`', '05:00',
     'Matrimonio, rettifica, cessazione. Il concentratore usa **5008, 5012, 5013**.',
     '**sì**'],
    ['Elettorale', '`prog-be`, `AnprManager`', '01:00',
     'Allineamenti di pertinenza elettorale. Non costruisce estremi di atto.', 'no'],
    ['Cambi di residenza online',
     '`cri-on-anpr-be`, `RecuperaPraticheCriAnpr`', '04:00, 11:00, 17:00',
     'Recupera e aggiorna le pratiche di cambio di residenza presentate dal cittadino '
     '(**P001, P002, P003**) e consulta i soggetti (**3002**).', 'no'],
]

STRATI = [
    ['#', 'Strato', 'Che cosa fa oggi', 'Perché la forma ANSC non parte'],
    ['1', 'Il processo schedulato — `AllineamentoNasciteBL`, `AllineamentoDecCittBL`, '
          '`AllineamentoMatrimonioBL`',
     'Legge gli eventi dalla coda, chiede i dati anagrafici della persona e li passa al '
     'concentratore in un oggetto di richiesta.',
     'I dati che passa vengono dal sistema anagrafico di provenienza, non da SIPO: '
     'l’identificativo dell’atto ANSC non è fra di essi.'],
    ['2', 'Gli endpoint del concentratore — `anpr/AllineamentoNascitaAnpr`, '
          '`anpr/AllineamentoDecCittAnpr`, `anpr/AllineamentoMatrimonioAnpr`',
     'Scelgono l’operazione ANPR secondo il caso e costruiscono l’oggetto di '
     'dominio da inviare.',
     'La scelta dell’operazione è corretta; il difetto sta nel contenuto '
     'dell’atto, che arriva dallo strato sotto.'],
    ['3', 'La conversione — `common/Convert.java`, `generateAtto:1033`, '
          '`attoConverter:177`, `generateAttoDaAggior:1250`',
     'Costruisce l’`Atto` dagli estremi dell’atto del sistema di provenienza.',
     '**È qui che la catena si interrompe**: nessuna delle tre funzioni valorizza le '
     'colonne di ANSC. Nel modulo la sigla ANSC non compare mai.'],
    ['4', 'La struttura di trasporto — `EstremiAttodiStatoCivile` per il percorso dei '
          'processi, `dtoSC/AttoVO` per il percorso in linea',
     'Porta gli estremi dell’atto: numero, anno, parte, serie, esponente, comuni, '
     'tipo.',
     'Sette campi la prima, nove la seconda, e **nessuno dei due porta '
     'l’identificativo ANSC**: la colonna non ha un posto in cui viaggiare.'],
    ['5', 'Il client — `AnprUtilities.generateTipoAttoANPR:435`',
     'Legge l’identificativo e, se lo trova, costruisce la forma ANSC; altrimenti '
     'quella classica.',
     'Funziona: trova sempre il valore vuoto, quindi produce sempre la forma classica. '
     '**Non va modificato.**'],
]

INTERVENTI = [
    ['#', 'Intervento', 'Dove', 'Che cosa comporta'],
    ['I1', 'Dare alla conversione la possibilità di leggere l’atto di SIPO',
     '`all-anpr-sipo`, `common/Convert.java`',
     'La conversione gira già su Oracle e usa i repository per comuni e tipi atto: '
     'può ritrovare l’atto di `ANAG_USR.ATTO` e leggerne le cinque colonne. '
     'È l’intervento che **sblocca tutti i processi in una volta**, perché '
     'i tre condividono il convertitore.'],
    ['I2', 'Valorizzare le cinque colonne sull’oggetto di dominio',
     '`Convert.generateAtto:1033` e le altre due funzioni di conversione',
     'Cinque assegnazioni, da fare **insieme**: la commutazione del client le legge tutte '
     'e tre di esse sono obbligatorie nello schema.'],
    ['I3', 'Decidere il criterio con cui si ritrova l’atto',
     'Lo stesso punto di I1',
     'I processi identificano la persona con il codice individuale, non con la chiave '
     'tecnica dell’atto. Serve il raccordo fra evento e atto. È il punto che '
     'richiede una decisione, non solo codice.'],
    ['I4', 'Portare la forma ANSC anche nelle iscrizioni AIRE',
     '`anpr-client`, classi di richiesta A001 e A002, e i tre generatori AIRE',
     'Lo slot esiste già negli schemi imbarcati: va rigenerata la classe di '
     'richiesta, che oggi non porta il campo, e poi esteso il generatore.'],
    ['I5', 'Portare la forma ANSC nelle iscrizioni in anagrafe',
     '`anpr-client`, `src/main/wsdl/1000iscrizione.xsd` e i generatori 1001 e 1002',
     'È il solo caso in cui manca anche lo schema: va riallineato a [A1], poi '
     'rigenerate le classi, poi estesi i generatori.'],
    ['I6', 'Estendere il percorso in linea dello stato civile',
     '`all-anpr-sipo`, `dtoSC/AttoVO` e `common/ConvertSC.java:655`',
     'Serve se si vuole la forma ANSC anche sulle chiamate che partono dalle maschere e '
     'non dai processi. Il campo va aggiunto alla struttura di trasporto e copiato nella '
     'conversione.'],
]

PER_PROCESSO = [
    ['Processo', 'Che cosa serve', 'Esito atteso'],
    ['Allineamento decessi e cittadinanza', 'I1, I2, I3',
     '**È il caso più favorevole.** Le operazioni che usa per il decesso '
     '— 2001 e 5008 — trattano già la forma ANSC in schema, classi e '
     'codice: non si tocca il client. Ed è la famiglia del pilota.'],
    ['Allineamento matrimoni e unioni civili', 'I1, I2, I3',
     'Le operazioni 5008, 5012 e 5013 passano da `tipoDatiEvento`, che ha lo slot, e il '
     'client lo valorizza. Vale la stessa conclusione dei decessi.'],
    ['Allineamento nascite', 'I1, I2, I3, I4, I5',
     'Si sdoppia. La **mutazione** (5008) funziona come i decessi. L’**iscrizione** '
     'no: per l’AIRE manca la classe, per l’anagrafe manca anche lo schema. '
     'Finché non si interviene, l’atto di nascita arriva ad ANPR nella forma '
     'ANSC quando muta e nella forma classica quando si iscrive.'],
    ['Elettorale, cambi di residenza online', 'nessuno',
     'Non pertinenti: non costruiscono estremi di atto di stato civile.'],
    ['Alimentazione della coda', 'nessuno',
     'Non pertinente al contenuto dell’atto: prepara gli eventi, non li converte.'],
]

DIFETTI = [
    ['#', 'Difetto', 'Dove', 'Perché pesa su questo intervento'],
    ['D1', 'L’ambiente è cablato al valore di collaudo',
     '`AnprClient.java:78`', 'Da quel valore dipende il portachiavi con cui la richiesta '
     'viene firmata (`RequestHandler.java:44`). Finché resta cablato **non si '
     'può provare l’intervento in un ambiente diverso da quello di collaudo**: '
     'è il primo nodo da sciogliere, prima di scrivere codice.'],
    ['D2', 'La richiesta viene costruita come stringa e poi ri-letta nella classe generata',
     'I generatori di `xmlRequestGenerator`, poi gli esecutori per operazione',
     'Un campo nuovo va aggiunto in due posti e i due possono divergere senza che nulla '
     'lo segnali.'],
    ['D3', 'I dati di dominio sono letti per riflessione, non per tipo',
     '`AnprUtilities`, i generatori',
     'Un campo che cambia nome non dà errore di compilazione ma di esecuzione, e una '
     'ricerca per nome di campo non trova i punti d’uso.'],
]

APERTI = [
    ['#', 'Questione', 'A chi spetta'],
    ['AN-01', 'Se per gli atti che i processi notturni allineano le colonne di ANSC di '
              '`ANAG_USR.ATTO` risultino popolate. Oggi vengono scritte dalle maschere '
              '(`AttoAnscBL.creaAttoAnsc`, chiamata da `varana-be` e da `matrim-be`): '
              'per un atto formato dal nuovo componente il percorso di scrittura va '
              'stabilito. **Senza questo, gli interventi non hanno dato da trasportare.**',
     'Referenti SIPO'],
    ['AN-02', 'Con quale criterio la conversione ritrova l’atto a partire '
              'dall’evento. I processi portano il codice individuale della persona; '
              'SIPO non espone una ricerca di atti per identificativo nazionale né '
              'per numero comunale. È l’intervento I3.',
     'Architettura / Referenti SIPO'],
    ['AN-03', 'Quale numero comunale vada in `numeroComunale`: quello della serie di SIPO '
              'o quello attribuito nel percorso di formazione su ANSC. Lo schema lo rende '
              'obbligatorio, quindi la scelta non si può rinviare.',
     'Referenti SIPO / Ufficio di stato civile'],
    ['AN-04', 'Come ANPR si comporti in esercizio ricevendo la forma ANSC: le sorgenti '
              'dichiarano lo schema, non le regole di accettazione. Da provare in '
              'preproduzione, e il difetto D1 va sciolto prima.',
     'Presidio ANPR / Sogei'],
    ['AN-05', 'Su quale versione di schema ANPR risponda l’ambiente in esercizio. '
              'Serve prima di rigenerare le classi per gli interventi I4 e I5: '
              'riallineare a una versione diversa da quella servita introdurrebbe un '
              'difetto nuovo.', 'Presidio ANPR / Fornitore'],
    ['AN-06', 'Quale sia la sorgente di verità degli schemi per il client e chi la '
              'aggiorni. Gli schemi imbarcati e il codice generato divergono nei due '
              'sensi: va stabilito da dove si prendono e con quale cadenza si riallineano.',
     'Architettura / Referenti SIPO'],
    ['AN-07', 'Se la forma ANSC vada usata anche quando l’atto è trascritto '
              'perché formato altrove. Lo schema ha il contrassegno '
              '`trascritto` fra i campi facoltativi, ma l’identificativo nazionale '
              'in quel caso è di un altro comune.',
     'Ufficio di stato civile'],
    ['AN-08', 'Se il percorso in linea dello stato civile debba essere allineato insieme '
              'ai processi notturni oppure dopo. È l’intervento I6, e la scelta '
              'cambia l’ampiezza del rilascio.', 'Referenti SIPO'],
    ['AN-09', 'Come si comporta la conversione quando l’atto ha '
              'l’identificativo di ANSC incompleto — per esempio il solo '
              '`ID_ATTO_ANSC` senza il comune. Serve una regola dichiarata: inviare la '
              'forma classica, oppure fermare l’allineamento e segnalarlo.',
     'Architettura'],
]


def scrivi(d):
    # =============================================================== 1
    h(d, 1, 'Scopo del documento')
    par(d, 'Questo documento risponde a una domanda sola: **c’è modo di passare '
           'ad ANPR l’identificativo di un atto formato in ANSC, e dove si '
           'interviene per farlo?** La risposta è affermativa, e la parte '
           'interessante non è il sì: è che il meccanismo esiste già '
           'negli schemi di ANPR e **in parte funziona già nel client di SIPO**, '
           'mentre quello che manca sta altrove — nella conversione dei dati dentro '
           'il concentratore, e per una famiglia di operazioni negli schemi imbarcati nel '
           'client.')
    par(d, 'Il perimetro è **l’identificativo dell’atto**, e soltanto '
           'quello.')
    par(d, 'La seconda metà del documento è operativa e risponde alla domanda '
           'nella forma in cui è stata posta: **dove intervenire nei processi '
           'schedulati** che oggi aggiornano ANPR, per renderli compatibili con gli atti '
           'formati su ANSC. Per ciascuno si dice che cosa serve e che cosa si ottiene.')

    h(d, 2, 'Metodo e fonti')
    par(d, 'Ogni affermazione tecnica è ricondotta al punto del sorgente che la '
           'sostiene, nella forma `file:riga`. Sono state usate tre categorie di fonte, e '
           'la distinzione fra la prima e la seconda è essenziale:')
    voce(d, 'Il contratto di ANPR.',
         'Gli schemi della documentazione ufficiale, versione 9.2.9 [A1]. È '
         'ciò che ANPR dichiara di accettare.')
    voce(d, 'Gli schemi imbarcati nel client.',
         'Gli stessi schemi nella copia che vive dentro il modulo di SIPO [S1]. **Non '
         'sono il contratto**: sono la fotografia di una versione, e possono essere '
         'indietro. In questo documento le due cose sono sempre distinte, e il confronto '
         'nome per nome è riportato.')
    voce(d, 'Il codice applicativo.',
         'Il client, il concentratore, i processi schedulati, le entità di base dati '
         '[S1]–[S6]. È ciò che SIPO fa davvero, che è un '
         'sottoinsieme di ciò che potrebbe fare.')
    par(d, 'Una cautela di metodo che conviene enunciare, perché vale oltre questo '
           'documento: **il client non è il contratto di ANPR**. Dedurre che una '
           'cosa non sia prevista dal fatto che il client non la implementa è un '
           'errore, e una prima stesura di questo studio lo ha commesso. Che cosa ANPR '
           'preveda si verifica sulla documentazione di ANPR.')

    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 4.4, 1.6])

    # =============================================================== 2
    h(d, 1, 'La risposta, in breve')
    par(d, 'Sì, l’identificativo dell’atto ANSC si può passare ad '
           'ANPR. Quattro fatti compongono la risposta, e il quarto è quello che '
           'sposta il lavoro.')
    voce(d, 'Lo schema lo prevede.',
         'Esiste un tipo dedicato per l’atto in forma ANSC, e un contenitore che '
         'ammette l’atto in una delle due forme, classica oppure ANSC.')
    voce(d, 'Il client lo implementa, e commuta da sé.',
         'In quattro punti il client verifica se l’atto porti '
         'l’identificativo di ANSC e, se lo porta, costruisce la forma ANSC senza '
         'che nessuno gliela chieda.')
    voce(d, 'Non tutte le operazioni lo ammettono.',
         'La mutazione dei dati di stato civile e la cancellazione per morte sì; '
         'l’iscrizione in anagrafe e l’iscrizione AIRE no, ciascuna per una '
         'ragione diversa.')
    voce(d, 'Oggi non parte mai, e non per colpa del client.',
         'Nei processi che aggiornano ANPR la conversione dei dati **non valorizza le '
         'colonne di ANSC**. La commutazione trova il valore vuoto e produce sempre la '
         'forma classica. È lì che si interviene.')

    # =============================================================== 3
    h(d, 1, 'Che cosa ANPR accetta')

    h(d, 2, 'Il tipo dell’atto in forma ANSC')
    par(d, 'Lo schema dei tipi di dato dichiara `tipoAttoANSC`, con sette elementi di cui '
           'quattro obbligatori. Il dato da osservare è il quarto: il numero '
           'comunale resta obbligatorio, quindi adottare la forma ANSC **non dispensa '
           'dalla numerazione comunale** — la affianca all’identificativo '
           'nazionale.')
    tabella(d, TIPO_ATTO_ANSC, [1.5, 1.5, 0.6, 3.0])

    h(d, 2, 'Il meccanismo: due elementi gemelli, non una sostituzione')
    par(d, 'La forma ANSC non rimpiazza l’atto classico. Il contenitore '
           '`tipoAttoANPR` è una scelta fra due alternative:')
    codice(d, [
        '<xs:complexType name="tipoAttoANPR">',
        '    <xs:choice>',
        '        <xs:element name="atto"     type="tipoAtto"     minOccurs="0" maxOccurs="1"/>',
        '        <xs:element name="attoANSC" type="tipoAttoANSC" minOccurs="0" maxOccurs="1"/>',
        '    </xs:choice>',
        '</xs:complexType>',
    ])
    par(d, 'E nei punti in cui l’atto compare, gli schemi affiancano **due elementi '
           'gemelli**: quello storico, di tipo classico, e quello nuovo, di tipo '
           '`tipoAttoANPR`. Nel blocco dei dati di evento, per esempio, convivono '
           '`attoEvento` e `attoEventoANPR`; nei dati di nascita, `attoNascita` e '
           '`attoNascitaANPR`. Si valorizza l’uno **oppure** l’altro.')
    par(d, 'Questa è una buona notizia per il disegno: l’adozione della forma '
           'ANSC è **additiva e reversibile**, e si può fare un’operazione '
           'alla volta senza toccare ciò che già funziona.')

    h(d, 2, 'In quali operazioni la forma ANSC è ammessa')
    par(d, 'Qui la risposta si articola, e conviene leggerla su tre colonne distinte: se '
           'lo **schema** del client abbia il posto, se la **classe Java** generata abbia '
           'il campo, se esista **codice** che lo valorizzi. I tre livelli non coincidono, '
           'e la differenza è esattamente la misura del lavoro.')
    tabella(d, OPERAZIONI, [2.2, 1.9, 1.5, 1.0])
    par(d, 'Si legge così: dove le tre colonne dicono sì, **funziona oggi**; '
           'dove manca la sola classe Java, basta rigenerarla ed estendere il generatore; '
           'dove manca anche lo slot nello schema, prima va riallineato lo schema. '
           'L’unico caso del terzo tipo è l’iscrizione in anagrafe.')

    # =============================================================== 4
    h(d, 1, 'Il meccanismo è già nel client, e commuta da sé')
    par(d, 'Il punto che decide è una funzione di utilità del client, '
           '`AnprUtilities.generateTipoAttoANPR` (`:435`). Ricevuto un oggetto di '
           'dominio, ne estrae l’atto e **interroga l’identificativo di ANSC**: '
           'se c’è costruisce la forma ANSC, altrimenti quella classica.')
    codice(d, [
        'Object atto = classObject.getMethod("getAtto").invoke(object);',
        'if (atto != null) {',
        '    tipoAttoANPR = new TipoAttoANPR();',
        '    String idAttoAnsc = (String) attoClass.getMethod("getIdAttoAnsc").invoke(atto);',
        '    if (idAttoAnsc != null) {',
        '        // ATTO ANSC',
        '        ...',
        '        tipoAttoANPR.setAttoANSC(tipoAttoANSC);',
        '    } else if (controllaAttoDaInviareAdAnpr(atto, attoClass)) {',
        '        // ATTO NORMALE',
        '    }',
        '}',
    ])
    par(d, 'Due osservazioni su questo frammento, entrambe con conseguenze pratiche. La '
           'prima: **nessuno sceglie la forma**, la scelta è un effetto del dato. '
           'Chi popola la colonna ottiene la forma ANSC; chi non la popola ottiene la '
           'forma classica, e non si accorge di nulla. La seconda: i dati sono letti '
           '**per riflessione**, cioè invocando i metodi per nome. Perciò una '
           'ricerca testuale del nome del campo nel codice non trova questi punti — '
           'ed è la ragione per cui il meccanismo può sembrare inesistente.')
    par(d, 'I punti che trattano la forma ANSC sono **quattro**:')
    voce(d, '`Richiesta5008XmlGenerator:118` e `:357`.',
         'La mutazione dei dati generali di stato civile, per l’atto di nascita.')
    voce(d, '`Richiesta5008XmlGenerator:1036`.',
         'La stessa operazione, per l’evento di morte.')
    voce(d, '`Richiesta2001XmlGenerator:172`.', 'La cancellazione per morte.')
    voce(d, '`AnprUtilities:297` e `:352`.',
         'Il blocco dei dati di evento, usato anche dallo scioglimento di unione civile.')

    h(d, 2, 'La commutazione legge cinque colonne, non una')
    par(d, 'Questo è il dettaglio che più facilmente si sbaglia. Il ramo ANSC '
           'non si accontenta dell’identificativo: costruisce il tipo leggendo '
           '**cinque campi dell’atto**, e tre di essi sono obbligatori nello schema. '
           'Valorizzare il solo identificativo produce un payload incompleto, quindi '
           'rifiutato.')
    tabella(d, COLONNE, [1.8, 1.3, 2.4, 0.8])
    par(d, 'Da notare che il comune letto è quello della colonna `ID_COMUNE`, che '
           '**è una terza colonna di comune**, distinta da quelle di iscrizione e di '
           'trascrizione usate dall’atto classico. Chi valorizzasse le sole colonne '
           'classiche non otterrebbe il comune di registrazione.')
    par(d, 'Le sei colonne di ANSC si comportano del resto come un’unità anche '
           'in SIPO: `AttoAnscBL.creaAttoAnsc` le scrive tutte insieme, scomponendo '
           'l’identificativo nazionale nelle sue parti, e `eliminaAttoAnsc` le azzera '
           'tutte insieme. **Vanno trattate come un blocco, non come campi indipendenti.**')

    # =============================================================== 5
    h(d, 1, 'Da dove viene oggi l’identificativo dell’atto')
    par(d, 'In SIPO l’identificativo esiste già, e ha un posto suo: '
           '`ANAG_USR.ATTO`, nelle colonne elencate sopra (`Atto.java:161,164,169,172,'
           '175,180`). Non è una struttura da creare.')
    par(d, 'Chi la scrive, però, è oggi una cosa sola: **l’operatore dalle '
           'maschere**. La funzione che scompone l’identificativo e popola il blocco '
           'è richiamata soltanto dal back-end delle variazioni anagrafiche e da '
           'quello dei matrimoni [S6]. Nessun processo automatico la invoca.')
    par(d, 'Da qui discende il primo punto aperto, e non è un dettaglio: se per gli '
           'atti che i processi notturni allineano quelle colonne non risultano popolate, '
           'gli interventi descritti nel seguito **non avrebbero nulla da trasportare**. '
           'Va accertato prima di cominciare, ed è AN-01.')
    par(d, 'Vale la pena aggiungere una nota sull’asimmetria delle due tabelle di '
           'atto. L’atto di anagrafe porta l’identificativo del **proprio** '
           'atto; l’atto di stato civile porta soltanto i riferimenti di un atto '
           '**trascritto** perché formato altrove. Chi cerca '
           'l’identificativo nella tabella dello stato civile non lo trova, e la '
           'conclusione sbagliata viene facile.')

    # =============================================================== 6
    h(d, 1, 'I processi che aggiornano ANPR')
    par(d, 'I processi schedulati di SIPO sono realizzati con il solo meccanismo di '
           'pianificazione del contenitore applicativo: nessun pianificatore esterno, '
           'nessun lavoro pianificato dall’orchestratore. Sono dichiarazioni nel '
           'codice, e si leggono nel codice.')
    par(d, 'Di tutti i processi pianificati, **sei** riguardano ANPR, e solo **tre** '
           'portano atti di stato civile. Gli altri tre sono comunque in tabella, perché '
           'escluderli con una ragione è parte della risposta.')
    tabella(d, BATCH, [1.5, 1.4, 0.8, 2.6, 1.0])

    h(d, 2, 'Come è fatta la catena')
    par(d, 'I tre processi che contano hanno la stessa forma, e un fatto li caratterizza: '
           '**non chiamano ANPR**. Chiamano il concentratore, che traduce. La sequenza, '
           'per ogni evento della coda:')
    voce(d, '1.',
         'Il processo chiede al concentratore l’elenco degli eventi da allineare, '
         'per famiglia di codici.')
    voce(d, '2.',
         'Per ciascun evento recupera i dati anagrafici della persona dal sistema di '
         'provenienza, interrogandolo per codice individuale.')
    voce(d, '3.',
         'Riempie un oggetto di richiesta con quei dati, il codice individuale, il tipo '
         'di evento e il codice di famiglia.')
    voce(d, '4.',
         'Chiama l’endpoint del concentratore che corrisponde al tipo di evento: '
         'allineamento di nascita, di decesso, di vedovanza, di matrimonio e così '
         'via.')
    voce(d, '5.',
         'Il concentratore sceglie l’operazione ANPR, converte i dati in '
         'oggetti di dominio e invoca il client.')
    par(d, 'La conseguenza di disegno è immediata, e orienta tutto il resto: '
           '**l’identificativo dell’atto ANSC non può arrivare dal '
           'sistema anagrafico di provenienza**, che non ha quel campo nei propri estremi '
           'di atto. Deve essere letto da SIPO. E il luogo in cui SIPO è '
           'raggiungibile lungo questa catena è il concentratore, non il processo: '
           'il processo dialoga per servizi, il concentratore ha la base dati.')

    # =============================================================== 7
    h(d, 1, 'Dove si interrompe la catena')
    par(d, 'La catena ha cinque strati. Il difetto sta nel terzo, e il quarto spiega '
           'perché il terzo non può risolversi da solo.')
    tabella(d, STRATI, [0.4, 1.9, 2.2, 2.8])
    par(d, 'In una riga: **la conversione non valorizza le colonne di ANSC, e la '
           'struttura con cui i dati le arrivano non le porta.** Nel modulo del '
           'concentratore la sigla ANSC non compare in nessun punto. Il client è '
           'pronto e aspetta un valore che nessuno gli mette.')
    par(d, 'Si noti che i due percorsi del concentratore usano **due convertitori '
           'distinti**: quello dei processi notturni costruisce l’atto dagli estremi '
           'del sistema di provenienza, quello delle chiamate in linea dallo stato civile '
           'lo costruisce dalla struttura di SIPO. Nessuno dei due porta il campo, ma il '
           'secondo è più vicino ad averlo, perché la sua sorgente **è** '
           'SIPO.')

    # =============================================================== 8
    h(d, 1, 'Gli interventi')

    h(d, 2, 'La decisione che viene prima: chi arricchisce l’atto')
    par(d, 'Prima del codice c’è una scelta di impianto, e ha due risposte '
           'possibili. L’identificativo può essere aggiunto **dal processo**, '
           'che lo leggerebbe e lo passerebbe al concentratore in un campo nuovo della '
           'struttura di richiesta; oppure **dal concentratore**, che lo leggerebbe da '
           'sé al momento della conversione.')
    par(d, 'La seconda strada è preferibile, per tre ragioni. Il concentratore ha '
           'già la base dati e la usa (nella conversione in linea interroga i '
           'repository dei comuni e dei tipi di atto). I tre processi condividono il '
           'convertitore, quindi **un intervento solo li serve tutti**. E la struttura di '
           'trasporto resta invariata, il che significa un’interfaccia in meno da '
           'far evolvere.')
    par(d, 'La prima strada ha un pregio che va riconosciuto: tiene la lettura di SIPO '
           'fuori dal concentratore, che è un traduttore. Se si preferisse questa, '
           'l’intervento I1 si sposta nei tre processi e la struttura di richiesta '
           'guadagna un campo. Il resto non cambia.')

    h(d, 2, 'Gli interventi, uno per uno')
    tabella(d, INTERVENTI, [0.4, 1.9, 1.9, 3.0])

    h(d, 2, 'Processo per processo')
    par(d, 'Tradotto sui tre processi che portano atti, il quadro è questo. '
           'Conviene leggerlo come un ordine di lavoro: il primo caso è anche il '
           'più semplice, e il più utile da fare prima.')
    tabella(d, PER_PROCESSO, [1.6, 1.1, 4.5])

    h(d, 2, 'L’ordine che conviene')
    par(d, 'Tre gradini, di costo crescente, e il primo dà già un risultato '
           'completo su una famiglia di atti.')
    voce(d, 'Primo gradino: decessi e matrimoni.',
         'Schema, classi e codice del client sono pronti. Serve soltanto la conversione '
         '— gli interventi I1, I2 e I3 — e con essa i due processi passano '
         'alla forma ANSC. Nessuna modifica al client, che è condiviso da tutto '
         'SIPO: è il vantaggio che rende questo gradino il primo.')
    voce(d, 'Secondo gradino: iscrizioni AIRE.',
         'Lo slot esiste già negli schemi del client. Va rigenerata la classe di '
         'richiesta ed esteso il generatore — intervento I4. Qui si tocca il client, '
         'quindi il rilascio è più largo.')
    voce(d, 'Terzo gradino: iscrizioni in anagrafe.',
         'Lo slot manca anche nello schema imbarcato. Va riallineato allo schema '
         'ufficiale, poi rigenerate le classi, poi estesi i due generatori — '
         'intervento I5. È il solo caso in cui il client è davvero indietro '
         'rispetto ad ANPR.')
    par(d, 'Finché il terzo gradino non è fatto, la nascita ha un comportamento '
           'misto che va detto per chiarezza: l’atto arriva ad ANPR nella forma ANSC '
           'quando i dati **mutano**, e nella forma classica quando la persona si '
           '**iscrive**. Non è un errore, è l’effetto del perimetro '
           'raggiunto; ma è meglio saperlo che scoprirlo.')

    # =============================================================== 9
    h(d, 1, 'Il client ANPR di SIPO: com’è fatto, e in che stato è')
    par(d, 'Gli interventi del secondo e del terzo gradino toccano il client. Questo '
           'capitolo dice che cosa comporta toccarlo.')

    h(d, 2, 'Il percorso di una chiamata')
    par(d, 'Il modulo conta circa seicentottanta classi e ottantamila righe, ma la '
           'proporzione è rassicurante: **circa quattro quinti sono generati dagli '
           'schemi**, e il codice scritto a mano è concentrato nei generatori delle '
           'richieste, nelle utilità comuni e nella sicurezza. Il percorso di una '
           'chiamata:')
    voce(d, '1.',
         'Il chiamante invoca il metodo unico di ingresso, passando i parametri e il '
         'nome dell’operazione.')
    voce(d, '2.',
         'Un primo selettore, su trentasei casi, instrada verso il generatore '
         'dell’operazione. I nomi ufficiali delle operazioni **stanno nei commenti '
         'di questo selettore**, non negli schemi: è l’unico posto in cui '
         'leggerli.')
    voce(d, '3.',
         'Il generatore costruisce la richiesta e la restituisce **come stringa**.')
    voce(d, '4.',
         'Un secondo selettore, per famiglia di operazioni, instrada verso '
         'l’esecutore, che firma la richiesta e **ri-legge la stringa** nella classe '
         'generata dallo schema.')
    par(d, 'Non esiste un registro delle operazioni: tutto passa per selettori a casi. '
           'Aggiungere un’operazione significa perciò toccare **quattro** punti '
           '— un caso nel primo selettore, un caso nel secondo, un esecutore nuovo, '
           'un generatore nuovo — più le classi rigenerate. Per gli interventi '
           'di questo documento non serve aggiungere operazioni: servono '
           'l’estensione di generatori esistenti e la rigenerazione di alcune classi.')

    h(d, 2, 'Lo stato degli schemi: lo scostamento è puntuale')
    par(d, 'Qui va corretto un giudizio di una stesura precedente. Gli schemi imbarcati '
           'nel client **non sono anteriori ad ANSC**: il confronto nome per nome con '
           '[A1] mostra che il tipo dell’atto in forma ANSC c’è, '
           'identico, con lo stesso numero di occorrenze, e che i due alberi dei tipi di '
           'dato divergono per **due soli tipi**, entrambi estranei a questo tema.')
    par(d, 'Lo scostamento vero è uno, e sta in un solo schema di operazione:')
    tabella(d, SCOSTAMENTO, [2.0, 1.3, 1.3, 2.6])
    par(d, 'Sette schemi su otto sono allineati. L’unico scostamento sono i tre '
           'posti dell’iscrizione, ed è esattamente la ragione per cui '
           'l’intervento I5 costa più degli altri.')
    par(d, 'C’è però una seconda divergenza, più insidiosa perché '
           'non si vede confrontando gli schemi: **gli schemi imbarcati e il codice Java '
           'generato dallo stesso modulo non si corrispondono, e la discordanza va nei due '
           'sensi.** Per il tipo dell’atto in forma ANSC esistono entrambi. Per il '
           'posto dell’atto nelle iscrizioni AIRE esiste lo schema e **manca il '
           'campo nella classe**. Significa che le classi non sono state rigenerate '
           'dall’ultimo aggiornamento degli schemi, e che nessuno dei due artefatti '
           'da solo descrive il modulo. È il punto AN-06, e va chiuso prima di '
           'rigenerare qualunque cosa.')

    h(d, 2, 'Tre difetti da sciogliere nello stesso intervento')
    par(d, 'Tre caratteristiche del modulo non sono pertinenti al tema ma lo '
           'condizionano. Il primo è bloccante per il collaudo.')
    tabella(d, DIFETTI, [0.4, 1.9, 1.7, 3.2])

    # =============================================================== 10
    h(d, 1, 'Punti aperti')
    par(d, 'Nove questioni restano da chiudere. Le prime tre decidono se gli interventi '
           'siano realizzabili e con quale contenuto; la quarta e la quinta riguardano il '
           'comportamento di ANPR e la versione in esercizio, che le sorgenti non '
           'documentano; le ultime quattro sono scelte di disegno e di perimetro.')
    tabella(d, APERTI, [0.8, 4.6, 1.2])


def intesta(d):
    """Compila il riquadro di testa, la testata di pagina e la Storia del Documento."""
    for r in d.tables[0].rows:
        if len(r.cells) < 2:
            continue
        etichetta = r.cells[0].text.strip().lower()
        valore = {'progetto': 'SIPO — Integrazione con ANSC',
                  'data consegna': DATA}.get(etichetta)
        if valore:
            D.riscrivi_cella(r.cells[1], valore)
    for fatto in D.frontespizio(d, '0.4',
                                'STUDIO_Identificativi-ANSC-verso-ANPR_v0.4'):
        print('  ' + fatto)
    storia = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for r in list(storia.rows[1:]):
        if not any(c.text.strip() for c in r.cells):
            r._tr.getparent().remove(r._tr)
    for versione, sintesi in [
        ('0.1', 'Prima stesura, sulla base degli schemi generati nel client.'),
        ('0.2', 'Corretto l’errore di metodo della v0.1: il client non è il '
                'contratto di ANPR. Verifica condotta sulla documentazione ufficiale.'),
        ('0.3', 'Ricognizione dell’architettura del client e del suo stato.'),
        ('0.4', 'Perimetro ristretto al solo identificativo dell’atto, con la '
                'rimozione del capitolo estraneo a questo tema. Aggiunti '
                'l’inventario dei processi '
                'schedulati che aggiornano ANPR, i cinque strati in cui la catena si '
                'interrompe e gli interventi necessari — per strato, per processo e '
                'in ordine di convenienza. Tre correzioni alla v0.3: gli schemi del '
                'client non sono anteriori ad ANSC e lo scostamento è di tre soli '
                'posti in un solo schema; la discordanza fra schemi imbarcati e codice '
                'generato va nei due sensi; i punti del client che trattano la forma ANSC '
                'sono quattro, non due. Chiarito che la commutazione legge cinque colonne '
                'e non una. Nove punti aperti.'),
    ]:
        D.storia(d, DATA if versione == '0.4' else '27/10/2026', versione, 'Tutti', sintesi)


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tab, fig))
