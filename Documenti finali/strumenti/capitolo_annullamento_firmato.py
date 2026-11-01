# -*- coding: utf-8 -*-
"""Capitolo «L'annullamento di un atto già firmato», da inserire a mano nell'analisi ANSC.

Richiesta dell'utente (01/11/2026): creare il capitolo in un file a parte; l'inserimento
nell'analisi lo fa lui. Il file parte dalla v3.56 svuotata, così stili, tabelle e testata
sono quelli dell'analisi e il copia-incolla in Word li conserva.

Fonti (ansc/docs/):
  · Note/NotaProcessoAnnotazioniAndQuickCoopServiceFlow (v1.3.0), § 3.1 e § 4.2;
  · Guida_operativa_ANSC.pdf, § 9.2.1 e § 9.2.2;
  · Guida_operativa_ANSC_Servizi_di_ausilio.pdf, § 3.5 (nota tecnica);
  · openapi/R013_rettifica_validazione.yaml e CasiTest/payload_test/R013_inserimento_annotazione_rettifica.json;
  · Mapping_casi_uso: Dic_Nasc_118, Morte_012, Matr_017, UnCiv_007, Citt_047 (letti qui);
  · Decodifiche: ANSC_03, ANSC_11, ANSC_79; Changelog.md (1.23.0, 1.41.0, 1.47.0, 1.52.0, 1.53.0).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/capitolo_annullamento_firmato.py
"""
import csv
import copy
import os
import sys

import docx
from docx.oxml.ns import qn

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402
from diagrammi_comune import C, banda, box, legenda, percorso, tela  # noqa: E402
from diagramma_cancella_pratica import nota, tratteggiato  # noqa: E402

BASE = os.path.dirname(QUI)
RADICE = os.path.dirname(BASE)
SRC = os.path.join(BASE, 'ANALISI_Integrazione-ANSC_v3.56.docx')
OUT = os.path.join(BASE, 'CAPITOLO_Annullamento-Atto-Firmato_ANSC_v0.1.docx')
PNG = os.path.join(QUI, 'img', 'annullamento_atto_firmato.png')
MAPPING = os.path.join(RADICE, 'ansc', 'docs', 'Mapping_casi_uso')

UC = [  # registro, codice UC (ANSC_03), codice motore, file del mapping
    ('Nascita', '14630000', 'Dic_Nasc_118', 'nascita/Dic_Nasc_118.csv'),
    ('Morte', '2341', 'Morte_012', 'morte/Morte_012.csv'),
    ('Matrimonio', '368699', 'Matr_017', 'matrimoni/Matr_017.csv'),
    ('Unione civile', '458699', 'UnCiv_007', 'unioni_civili/UnCiv_007.csv'),
    ('Cittadinanza', '53719', 'Citt_047', 'cittadinanza/Citt_047.csv'),
]


# ───────────────────────────────────────────────────────────── mapping
def leggi_mapping(rel):
    righe = list(csv.reader(open(os.path.join(MAPPING, rel), encoding='utf-8')))
    testa = righe[0]
    return [r for r in righe[1:] if r != testa]


def campi():
    """I campi del caso d'uso della morte (il pilota) e il confronto con gli altri quattro."""
    morte = leggi_mapping('morte/Morte_012.csv')
    chiave = lambda r: tuple(r[:5] + [r[6]])  # noqa: E731
    base = {chiave(r) for r in morte}
    diversi = {}
    for _, _, _, rel in UC:
        altre = {chiave(r) for r in leggi_mapping(rel)}
        if altre != base:
            diversi[rel] = (altre - base, base - altre)
    return morte, diversi


# ───────────────────────────────────────────────────────────── figura
def figura():
    W, H = 1700, 1380
    im, dr = tela(W, H, "Annullamento di un atto già firmato: la rettifica di tipo annullamento",
                  "un evento nuovo, l’annotazione, che richiama l’atto da annullare · "
                  "fonti: nota di processo ANSC § 3.1, guida operativa § 9.2.1, R013")
    banda(dr, 30, 96, 830, H - 70, C['blu'][0], "SIPO", C['blu'][0])
    banda(dr, 870, 96, 1670, H - 70, C['viola'][0], "ANSC", C['viola'][0])
    xs, xa, bw, bh = 110, 950, 640, 112
    ys = [150, 312, 474, 636, 798]

    box(dr, xs, ys[0], bw, bh, 'grigio', "Provvedimento di una terza amministrazione",
        "tipicamente il tribunale (art. 95) · competente l’ufficiale del comune che ha "
        "formato l’atto")
    box(dr, xs, ys[1], bw, bh, 'blu', "Annotazione per rettifica",
        "caso d’uso del registro dell’atto (es. 2341 Morte_012) · si individua l’atto "
        "da annullare")
    box(dr, xs, ys[2], bw, bh, 'blu', "Compilazione",
        "ente dichiarante · evento da rettificare · dettaglio della rettifica · "
        "formula 190 · allegato facoltativo")
    box(dr, xs, ys[3], bw, bh, 'blu', "Numero comunale dell’annotazione",
        "l’annotazione è un atto: numero, data e ora di formazione propri")
    box(dr, xs, ys[4], bw, bh, 'giallo', "Tipo di rettifica: ANNULLAMENTO",
        "datiRettifica.idTipoRettifica = 0 (ANSC_79) · non è nel mapping: lo valorizza "
        "il concentratore")
    for a, b in zip(ys, ys[1:]):
        percorso(dr, [(xs + bw / 2, a + bh), (xs + bw / 2, b)])

    box(dr, xa, ys[4], bw, bh, 'viola', "R013 /rettifica/validazione/evento",
        "per l’annullamento solo «evento», senza «eventoModificato»")
    percorso(dr, [(xs + bw, ys[4] + bh / 2), (xa, ys[4] + bh / 2)])
    y7 = ys[4] + bh + 50
    tratteggiato(dr, xa, y7, bw, bh, 'viola', "Firma dell’ufficiale",
                 "nessun dichiarante · via servizi cooperativi non descritta: R007 "
                 "[DA VERIFICARE]")
    percorso(dr, [(xa + bw / 2, ys[4] + bh), (xa + bw / 2, y7)])
    y8 = y7 + bh + 50
    box(dr, xa, y8, bw, 150, 'verde', "Effetti in ANSC",
        "annotazione a margine della copia integrale · certificato semplice ed estratto "
        "per riassunto inibiti · invio in conservazione")
    percorso(dr, [(xa + bw / 2, y7 + bh), (xa + bw / 2, y8)])
    tratteggiato(dr, xs, y8, bw, 150, 'blu', "Riallineamento in SIPO",
                 "R005 sull’atto annullato e stato registrato su ANSC_STATO_ATTO "
                 "[DA VERIFICARE: quale stato ANSC_11]")
    percorso(dr, [(xa, y8 + 75), (xs + bw, y8 + 75)])
    nota(dr, xa, 150, bw,
         "Dopo la firma dell’ufficiale R011 non è più ammessa, e né l’errore materiale "
         "(art. 98) né la nota tecnica possono annullare un atto. L’annullamento per "
         "inefficacia, solo dalla web app, è disabilitato dalla versione 1.52.0.")
    legenda(dr, 60, H - 50, [('grigio', "fuori dai sistemi"), ('blu', "SIPO"),
                             ('giallo', "scelta"), ('viola', "chiamata o passo in ANSC"),
                             ('verde', "esito")])
    im.save(PNG)
    print('scritto:', PNG)


# ───────────────────────────────────────────────────────────── documento
def svuota(doc):
    corpo = doc.element.body
    for el in list(corpo):
        if el.tag != qn('w:sectPr'):
            corpo.remove(el)


def documento():
    doc = docx.Document(SRC)
    modello = copy.deepcopy(next(t for t in doc.tables
                                 if t.rows[0].cells[0].text.strip() == 'Momento')._tbl)
    svuota(doc)
    corpo = doc.element.body
    corpo.insert(0, modello)                       # serve a D.tabella, si toglie alla fine
    from docx.table import Table
    mod = Table(modello, doc)
    fine = corpo.find(qn('w:sectPr'))

    def h(liv, t):
        D.para(doc, fine, t, stile=f'Heading {liv}')

    def p(t):
        D.para(doc, fine, t)

    def v(testa, corpo_):
        D.voce(doc, fine, testa, corpo_)

    def tab(righe, larghezze):
        D.tabella(doc, fine, righe, mod, larghezze)
        D.para(doc, fine, '')

    morte, diversi = campi()

    h(1, 'L’annullamento di un atto già firmato')
    p('Il capitolo «Annullamento/Cancellazione Atto in lavorazione» tratta la cancellazione '
      'di un atto prima della firma dell’ufficiale, che si fa con R011. Dopo la firma R011 '
      'rifiuta l’atto (il controllo è stato aggiunto al servizio, come riporta il changelog) e '
      'l’atto non si cancella più. Le fonti ANSC documentano una sola via per annullarlo: '
      'registrare un evento nuovo, l’annotazione per rettifica di tipo annullamento, che lascia '
      'l’atto nel registro e ne impedisce la certificazione.')
    p('Il processo è descritto dalla nota di processo ANSC «Annotazioni e flusso base servizi '
      'cooperativi» (versione 1.3.0, § 3.1), dalla guida operativa ANSC (§ 9.2.1), dal contratto '
      'R013 e dal suo esempio di richiesta (R013_inserimento_annotazione_rettifica.json); i dati '
      'richiesti vengono dal mapping dei casi d’uso.')

    h(2, 'Gli strumenti che intervengono su un atto firmato')
    p('ANSC offre più strumenti per intervenire su un atto già formato, ma solo uno lo annulla.')
    tab([['Strumento', 'Canale', 'Che cosa fa', 'Annulla l’atto'],
         ['Cancellazione logica (R011)', 'Servizio cooperativo',
          'Elimina un evento depositato e non ancora firmato dall’ufficiale.',
          'No: un atto 5 FIRMATO DA USC è rifiutato.'],
         ['Annotazione per rettifica, tipo annullamento', 'R013 e web app',
          'Evento nuovo, su provvedimento di una terza amministrazione, che richiama l’atto.',
          'Sì: è l’unica via documentata.'],
         ['Annotazione per rettifica, tipo modifica', 'R013 e web app',
          'Modifica i dati dell’atto: certificati ed estratti riportano i dati corretti.',
          'No.'],
         ['Annotazione per errore materiale (art. 98)', 'R013 e web app',
          'Corregge i dati anagrafici dell’intestatario e, per la nascita, dei genitori.',
          'No: la nota dice che «NON può comportare l’annullamento».'],
         ['Correzione tramite nota tecnica', 'Solo web app',
          'Corregge i metadati di un atto FIRMATO DA USC su cui non siano state apposte '
          'annotazioni modificative.', 'No.'],
         ['Annullamento per inefficacia', 'Solo web app',
          'Porta l’atto a 10 INEFFICACE. Introdotto con la versione 1.41.0, nessuna guida ne '
          'descrive il processo.', 'Non oggi: disabilitato dalla versione 1.52.0 del '
          '04/06/2026.']],
        [1.6, 1.0, 2.6, 1.6])

    h(2, 'Il processo')
    p('La rettifica di tipo annullamento non è un’operazione sull’atto: è la formazione di un '
      'atto nuovo, un’annotazione, con numero comunale, data, ora e firma propri, che richiama '
      'l’atto da annullare.')
    v('Il provvedimento. ', 'All’origine c’è il provvedimento di una terza amministrazione, '
      'tipicamente il tribunale (art. 95). La competenza è dell’ufficiale dello stato civile '
      'del comune che ha formato l’atto.')
    v('Il caso d’uso. ', 'Per ogni registro ANSC prevede un caso d’uso «Annotazione per '
      'rettifica» (tabella più avanti). L’evento è un’annotazione (idtipocontenuto 2) e porta '
      'in datiRettifica.eventoCollegato gli estremi dell’atto da rettificare.')
    v('La compilazione. ', 'Si acquisiscono l’ente dichiarante, l’evento da rettificare, il '
      'dettaglio della rettifica, che aggiorna la composizione con la formula ministeriale '
      'dedicata, e i dati di formazione dell’annotazione. Nella web app il tipo di rettifica si '
      'sceglie dopo i dati: alla conferma il sistema chiede se si tratti di annullamento o di '
      'modifica dell’evento.')
    v('La validazione. ', 'Si chiama R013 /rettifica/validazione/evento/{version} con '
      'datiRettifica.idTipoRettifica = 0 (ANNULLAMENTO, decodifica ANSC_79). Per l’annullamento '
      'il servizio richiede soltanto «evento»: «eventoModificato», cioè l’atto completo già '
      'rettificato, serve solo alla rettifica di modifica. La risposta restituisce entrambi i '
      'modelli; gli esiti dichiarati sono 200, 403 e 404.')
    v('La firma. ', 'Per l’annullamento la web app «propone direttamente la pagina di '
      'acquisizione firma dell’ufficiale»: non ci sono dichiaranti né altri firmatari. Per i '
      'servizi cooperativi la firma non è descritta; che avvenga con R007, come per ogni altro '
      'evento, è un’ipotesi [DA VERIFICARE].')
    v('Le verifiche. ', 'Il comune consulta l’evento rettificato ed emette la copia integrale, '
      'che riporta la rettifica a margine.')
    D.immagine(doc, fine, PNG, 6.3,
               'Il processo di annullamento di un atto già firmato: la rettifica di tipo '
               'annullamento.')

    h(2, 'I casi d’uso e i dati richiesti')
    tab([['Registro', 'Codice UC (ANSC_03)', 'Codice motore']]
        + [[r, c, m] for r, c, m, _ in UC], [1.6, 1.8, 1.8])
    altri = [rel for rel in diversi]
    extra = sum(len(d[0]) for d in diversi.values())
    p(f'I cinque mapping dichiarano gli stessi {len(morte)} campi'
      + (f'; quello della cittadinanza ne aggiunge {extra}, tutti facoltativi, per l’atto '
         'collegato di cittadinanza (evento.eventoCollegatoCittadinanza).'
         if altri == ['cittadinanza/Citt_047.csv']
         and all(r[5] == 'opzionale' for r in diversi[altri[0]][0])
         and not diversi[altri[0]][1] else '.')
      + ' La tabella riporta quelli della morte (Morte_012).')
    righe = [['Sezione', 'Campo', 'Obbligatorio', 'Percorso nel modello evento']]
    for r in morte:
        percorso_m = f'{r[3]}.{r[4]}' if r[3] else '—'
        righe.append([r[0], r[1], r[2], percorso_m])
    tab(righe, [1.4, 1.8, 0.9, 2.7])
    p('Due osservazioni. L’atto da annullare si individua per comune, provincia, numero '
      'comunale, anno, data e tipo di registro, tutti obbligatori, mentre l’identificativo '
      'nazionale (idAnsc) è facoltativo. E il tipo di rettifica '
      '(datiRettifica.idTipoRettifica) non compare in nessuno dei 374 mapping: la '
      'configurazione importata non lo conterrà, e a valorizzarlo dovrà essere il '
      'concentratore, come già avviene per progressivoGemello nel parto plurimo.')

    h(2, 'Gli effetti in ANSC')
    v('Copia integrale. ', 'La rettifica compare sempre come annotazione a margine.')
    v('Certificato semplice ed estratto per riassunto. ', 'ANSC ne inibisce l’emissione.')
    v('Conservazione. ', 'Gli atti rettificati e annullati sono inviati al sistema di '
      'conservazione (versione 1.47.0).')
    v('Annotazioni automatiche. ', 'La versione 1.53.0 corregge il «flusso di gestione di '
      'annotazione automatica di Atto Annullato»: ANSC gestisce le annotazioni generate '
      'dall’atto annullato, ma le fonti non ne descrivono il comportamento.')
    p('Le fonti non dicono quale stato della decodifica ANSC_11 assuma l’atto annullato: lo '
      'stato 3 ANNULLATO esiste, ma nessun documento lo lega alla rettifica. Non descrivono '
      'neppure le conseguenze verso l’anagrafe e verso gli altri comuni: le notifiche sono '
      'documentate per l’errore materiale e per le annotazioni modificative, non per '
      'l’annullamento.')

    h(2, 'Che cosa comporta per SIPO')
    v('Non è la rettifica di oggi. ', 'In SIPO /updLavorazioneRettifica riporta un atto '
      'definito allo stato 1, con FLG_RETTIFICA_INCORSO, e lo si corregge. Un atto formato in '
      'ANSC non si riapre: per quegli atti la correzione, e a maggior ragione l’annullamento, '
      'diventa la formazione di un’annotazione.')
    v('Una maschera nuova. ', 'Serve una pagina per l’annotazione per rettifica. Poiché i '
      'cinque casi d’uso chiedono gli stessi dati, salvo i campi facoltativi della '
      'cittadinanza, una pagina comune ai registri è sufficiente.')
    v('Il numero comunale. ', 'L’annotazione ha un numero proprio, staccato come per ogni atto '
      'da be-numeratore-comunale.')
    v('Il percorso presidiato. ', 'La validazione R013 e la firma dell’ufficiale avvengono '
      'nella sessione OTP, come per la formazione. L’annotazione ha la propria riga in '
      'ANSC_STATO_ATTO; per l’atto annullato, dopo la firma, si rilegge lo stato con R005 e lo '
      'si registra sulla sua riga.')
    v('Il contratto. ', 'Il concentratore conosce un solo servizio di deposito, R009, mentre i '
      'servizi che portano un evento in ANSC sono sette (OP-45): R013 va aggiunto ad '
      'ansc-v1.yaml.')
    v('La configurazione. ', 'I cinque casi d’uso si configurano come gli altri in '
      'ANSC_CFG_UC; il tipo di rettifica lo valorizza il concentratore.')

    h(2, 'Punti aperti')
    p('Numerazione proposta in coda al registro degli Open Point.')
    tab([['#', 'Tema', 'Questione', 'Stato', 'Owner', 'Priorità'],
         ['OP-80', 'Stato dell’atto annullato con rettifica',
          'Quale stato della decodifica ANSC_11 assume l’atto dopo la firma dell’annotazione '
          'per rettifica di tipo annullamento (3 ANNULLATO?). Da accertare in preproduzione con '
          'R005.', 'Aperto', 'Analisi / Sogei', 'Alta'],
         ['OP-81', 'Firma dell’annotazione per rettifica',
          'Con quale servizio si firma l’annotazione per via cooperativa (R007?) e se richieda '
          'l’attestazione di conformità degli allegati.', 'Aperto', 'Analisi / Sogei', 'Alta'],
         ['OP-82', 'Conseguenze dell’annullamento',
          'Effetti verso l’anagrafe e verso gli altri comuni: comunicazioni, notifiche e '
          'annotazioni automatiche generate dall’atto annullato.', 'Aperto', 'Analisi / Sogei',
          'Media'],
         ['OP-83', 'Annullamento per inefficacia',
          'Disabilitato dalla versione 1.52.0: se e quando tornerà disponibile, con quale '
          'processo e con quali termini.', 'Aperto', 'Sogei', 'Bassa'],
         ['OP-84', 'Rettifica in SIPO degli atti formati in ANSC',
          'Pagina dell’annotazione per rettifica (comune ai registri o per registro) e '
          'trattamento della rettifica attuale di SIPO, che riapre l’atto, per gli atti già '
          'formati in ANSC.', 'Aperto', 'Analisi / Comune', 'Alta']],
        [0.55, 1.3, 2.75, 0.6, 0.9, 0.6])

    corpo.remove(modello)
    doc.save(OUT)
    print('scritto:', OUT)


if __name__ == '__main__':
    figura()
    documento()
