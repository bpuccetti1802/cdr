# -*- coding: utf-8 -*-
"""Figure della v0.11 del disegno del back-office, riallineate all'analisi v3.53 e alle
decisioni del 28/10/2026.

  · bo_mfe.png            — senza la pagina «Logiche di scelta»; il servizio della numerazione
                            è be-numeratore-comunale, con le sue API /api/v1/numerazione-comunale
  · bo_atto.png           — dettaglio dell'atto: niente Modello né versione sull'atto, i campi
                            raggruppati per oggetto del modello evento (non più sezioni)
  · bo_uc_elenco.png      — ANSC_CFG_UC legata al tipo atto (niente Modello né maschera);
                            la logica di scelta è un codice libero
  · bo_uc_dettaglio.png   — ANSC_CFG_CAMPO con l'alias SIPO, senza sezioni né logiche di campo
  · bo_catalogo_uc.png    — il catalogo è ANSC_CFG_UC (ANSC_ANA_UC non esiste più)
  · bo_versioni.png       — il report d'impatto senza le logiche
  · bo_allegati_uc.png    — la condizione è un codice libero (cd_logica), senza dominio
  · bo_num_richiesta.png  — senza registro e senza registrazione a posteriori
  · bo_num_ricerca.png    — i filtri di GET /ricerca, senza serie né CREA SERIE
  · bo_home.png           — senza la mattonella delle logiche
  · bo_riconciliazione.png, bo_riconciliazione_dettaglio.png — senza CONDIZIONE
  · bo_comandi.png        — l'importazione del mapping senza sezioni

Le figure si scrivono in img/bo_v0_11, per non sovrascrivere quelle omonime che
diagrammi_backoffice.py produce per l'analisi.

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo_v6.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402
import wireframe_bo as W   # noqa: E402
from diagrammi_comune import F_ITA, F_REG, MUTED, centra, fnt   # noqa: E402

L, X = 1240, 24
C = L - 2 * X
SOTTO_V = ('Versione in lavorazione: v13 — BOZZA. Le modifiche non hanno effetto finché la '
           'versione non è attivata.')


# ───────────────────────────────────────────────── composizione a micro-frontend
def mfe(dest):
    im, dr = G.tela(1420, 922, "Il back-office come insieme di micro-frontend",
                    "Quattro unità di rilascio, una per area; le pagine sono rotte a "
                    "caricamento differito dentro ciascuna.")
    G.box(dr, 500, 96, 420, 78, 'viola', "Shell (host)",
          "testata, piè di pagina, profilo, sessione, rotte di primo livello")
    G.box(dr, 60, 96, 380, 78, 'grigio', "Libreria condivisa",
          "componenti, tema, guardie, servizio di sessione — condivisa come singleton")
    G.freccia(dr, (440, 135), (500, 135))
    G.box(dr, 980, 96, 380, 78, 'giallo', "Registro delle pagine",
          "ANSC_CFG_APPLICAZIONE · ANSC_CFG_PAGINA · _ABILITAZ · _TEMA")
    G.freccia(dr, (920, 135), (980, 135))
    G.centra(dr, "legge il menu", fnt(F_ITA, 13), 950, 74, MUTED)
    G.banda(dr, 60, 210, 1380, 740, '#2f6bb0',
            "QUATTRO REMOTE — UNA PER AREA, RILASCIABILI SEPARATAMENTE", '#2f6bb0')
    aree = [
        ('Operativa', 'verde', ['Supervisione atti', 'Dettaglio atto',
                                'Allegati dell’atto', 'Identificativi soggetti',
                                'Numerazione — richiesta', 'Numerazione — ricerca']),
        ('Notifiche', 'giallo', ['Gestione notifiche']),
        ('Configurazione', 'blu', ['UC — elenco', 'UC — dettaglio', 'Catalogo UC',
                                   'Dizionari', 'Riconciliazione', 'Versioni',
                                   'Allegati per UC', 'Soggetti per UC',
                                   'Caricamento da file']),
        ('Servizio', 'grigio', ['Comandi e operazioni', 'Pagine e menu']),
    ]
    x = 90
    for nome, col, pagine in aree:
        G.box(dr, x, 252, 300, 62, col, "mfe-" + nome.lower(), nome)
        G.freccia(dr, (x + 150, 192), (x + 150, 252))
        yy = 338
        for p in pagine:
            dr.rounded_rectangle([x + 20, yy, x + 280, yy + 30], radius=5,
                                 outline='#c7cdd6', width=2, fill='white')
            dr.text((x + 34, yy + 8), p, font=fnt(F_REG, 14), fill='#1f2937')
            yy += 38
        centra(dr, "rotte a caricamento differito", fnt(F_ITA, 13), x + 150, yy + 6, MUTED)
        x += 330
    G.box(dr, 480, 776, 460, 62, 'rosso', "Concentratore all-ansc-sipo",
          "l’unico che parla con ANSC: PKCS#12, sessione OTP, firma")
    G.freccia(dr, (710, 740), (710, 776))
    G.centra(dr, "API /ansc/v1", fnt(F_ITA, 13), 790, 744, MUTED)
    G.box(dr, 980, 776, 400, 62, 'rosso', "Servizio be-numeratore-comunale",
          "numerazione comunale: non parla con ANSC")
    G.freccia(dr, (1180, 740), (1180, 776))
    G.centra(dr, "API /api/v1/numerazione-comunale", fnt(F_ITA, 13), 1068, 744, MUTED)
    G.legenda(dr, 60, 872, [('viola', 'ospite'), ('grigio', 'condiviso'),
                            ('giallo', 'configurazione'), ('rosso', 'back-end')])
    im.save(os.path.join(dest, 'bo_mfe.png'))
    return 'bo_mfe.png'


# ───────────────────────────────────────────────── dettaglio dell'atto
def atto(dest):
    im, dr, y = W.pagina(L, 880,
                         ['Home', 'Integrazione ANSC', 'Supervisione atti', '2026/0041287'],
                         'Atto 2026/0041287 — [2101] Morte in abitazione',
                         distintivo=('OTP', True),
                         azioni_dx=['REGISTRO DI EMERGENZA'])
    y = W.pannello(dr, X, y, C, 'Scenario — atto SIPO salvato il 24/09/2026 alle 09:41',
                   alt=104)
    y = W.righe_etichette(dr, X + 20, y + 2, [
        ('Registro', 'Morte'), ('Modello', '01'), ('Numero comunale', '13.557'),
        ('UC determinato', '2101 (Morte_001)'), ('Origine UC', 'AUTOMATICA'),
        ('Stato ANSC', '— (non ancora validato)')], C - 40)
    y += 14
    y = W.schede(dr, X, y, C, ['Campi per oggetto', 'Soggetti', 'Allegati', 'Cronologia',
                               'Modello evento inviato'], attiva=0)
    y = W.accordion(dr, X, y, C, [
        ('evento', 'ok'), ('defunto', 'ok'), ('dichiarante', 'ko'),
        ('luogoDecesso', 'ok'), ('formula', 'ok'), ('allegati', 'ko')])
    y = W.nota(dr, X, y, C,
               'Oggetto «dichiarante»: il campo dichiarante.idANPR è obbligatorio per l’UC '
               '2101 e non è valorizzato in SIPO. La preverifica lo segnala prima del '
               'deposito; ANSC lo rifiuterebbe con codice 400001.', W.ROSSO)
    y = W.tabella(dr, X, y, C,
                  ['Momento', 'Fase', 'Servizio', 'Esito', 'Durata', 'Operatore'],
                  [150, 140, 200, 190, 100, 200], [
                      ['24/09 09:41', 'Lavorazione', '—', ('UC DETERMINATO', W.VERDE),
                       '—', 'g.rossi'],
                      ['24/09 10:02', 'Documenti', 'R001 creaAllegato', ('OK', W.VERDE),
                       '1.204 ms', 'g.rossi'],
                      ['24/09 10:18', 'Validazione', 'R009 /validazione/evento',
                       ('KO 400001', W.ROSSO), '890 ms', 'g.rossi'],
                  ])
    W.bottoni(dr, X, y + 6, [
        ('RIPRENDI DA VALIDAZIONE', W.BLU, True), ('RICONCILIA CON ANSC', W.BLU),
        ('SCARICA MODELLO EVENTO', W.MUTED), ('ANNULLA ATTO', W.ROSSO)])
    return W.salva(im, dest, 'bo_atto.png')


# ───────────────────────────────────────────────── configurazione UC — elenco
def uc_elenco(dest):
    im, dr, y = W.pagina(L, 760, ['Home', 'Integrazione ANSC', 'Configurazione casi d’uso'],
                         'Configurazione dei casi d’uso',
                         azioni_dx=['IMPORTA DA MAPPING', 'NUOVO UC'], sotto=SOTTO_V)
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=96)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Famiglia', 'Morte', 'select', 3), ('Codice UC', '', 'testo', 2),
        ('Tipo atto', '', 'testo', 2), ('Stato', 'Attivi', 'select', 2),
        ('Versione', 'v13 — BOZZA', 'select', 3)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Descrizione', 'Tipo atto', 'Priorità', 'Logica di scelta',
                   'Interrogazione', 'Stato', 'Azioni'],
                  [90, 330, 100, 90, 170, 170, 120, 122], [
                      ['2101', 'Morte in abitazione a Roma', '301', '10', 'L003', 'Q2101',
                       ('ATTIVO', W.VERDE), ['mod', 'vedi']],
                      ['2102', 'Morte in ospedale a Roma', '303', '20', 'L004', 'Q2102',
                       ('ATTIVO', W.VERDE), ['mod', 'vedi']],
                      ['2103', 'Morte in casa di cura', '304', '30', 'L005', '—',
                       ('BOZZA', W.GIALLO), ['mod', 'vedi']],
                      ['2201', 'Trascrizione morte altro comune', '311', '40', 'L011',
                       'Q2201', ('ATTIVO', W.VERDE), ['mod', 'vedi']],
                      ['2999', 'Caso d’uso di servizio — recupero', '—', '99', '—', '—',
                       ('SOSPESO', W.MUTED), ['mod', 'vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='25', pagine=3)
    W.nota(dr, X, y, C,
           'La priorità decide quale UC vince quando più logiche rispondono sullo stesso '
           'tipo atto: il primo in ordine di priorità è quello adottato. La logica è un '
           'codice libero, valutato dal codice applicativo. Senza tipo atto l’UC è nel '
           'catalogo ma non ancora adottato.')
    return W.salva(im, dest, 'bo_uc_elenco.png')


# ───────────────────────────────────────────────── configurazione UC — dettaglio
def uc_dettaglio(dest):
    im, dr, y = W.pagina(L, 880,
                         ['Home', 'Integrazione ANSC', 'Configurazione casi d’uso', '2101'],
                         '[2101] Morte in abitazione a Roma',
                         azioni_dx=['SIMULA SU ATTO REALE', 'SALVA'],
                         sotto='Versione v13 — BOZZA · Tipo atto 301 · Logica L003 · '
                               'Interrogazione Q2101')
    y = W.schede(dr, X, y, C,
                 ['Dati generali', 'Campi', 'Allegati', 'Soggetti', 'Formule'], attiva=1)
    y = W.riga_campi(dr, X, y, C, [
        ('Oggetto', 'defunto', 'select', 3), ('Solo obbligatori', 'No', 'select', 2),
        ('Senza alias SIPO', 'Sì', 'select', 3), ('Cerca campo', '', 'testo', 3)])
    y = W.tabella(dr, X, y, C,
                  ['Oggetto ANSC', 'Campo ANSC', 'Obbl.', 'Obblig. evento', 'Alias SIPO',
                   'Decodifica', 'Ord.', 'Operativo', 'Azioni'],
                  [140, 170, 60, 130, 250, 110, 60, 100, 98], [
                      ['defunto', 'cognome', 'SI', '—', 'defunto.cognome', '—', '1',
                       '1', ['mod']],
                      ['defunto', 'nome', 'SI', '—', 'defunto.nome', '—', '2', '1',
                       ['mod']],
                      ['defunto', 'sesso', 'SI', '—', 'defunto.sesso', 'ANSC_07', '3', '1',
                       ['mod']],
                      ['defunto', 'idANPR', 'SI', '—', ('DA COMPLETARE', W.ROSSO), '—', '4',
                       '1', ['mod']],
                      ['defunto', 'dataEvento', 'SI', '—', 'atto.dataDecesso', '—', '5',
                       '1', ['mod']],
                      ['luogoDecesso', 'idComune', 'SI', '—', 'luogo.comune', 'ANSC_02',
                       '6', '1', ['mod']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='85', pagine=9)
    y = W.nota(dr, X, y, C,
               'Quattro campi obbligatori dell’UC non hanno ancora un alias SIPO. Finché '
               'restano scoperti la preverifica li segnala e l’atto non può essere '
               'depositato. Gli alias mostrati sono esempi.', W.ROSSO)
    W.bottoni(dr, X, y, [('AGGIUNGI CAMPO', W.BLU), ('REIMPORTA OGGETTO', W.MUTED),
                         ('ESPORTA IN EXCEL', W.MUTED)])
    return W.salva(im, dest, 'bo_uc_dettaglio.png')


# ───────────────────────────────────────────────── catalogo UC
def catalogo(dest):
    im, dr, y = W.pagina(L, 640, ['Home', 'Integrazione ANSC', 'Catalogo UC di ANSC'],
                         'Catalogo dei casi d’uso pubblicati da ANSC',
                         azioni_dx=['AGGIORNA DA ANSC'],
                         sotto='Sola consultazione: è ciò che ANSC dichiara, nelle righe di '
                               'ANSC_CFG_UC della versione v13 — BOZZA.')
    y = W.riga_campi(dr, X, y, C, [
        ('Famiglia', 'Morte', 'select', 3), ('Codice UC', '', 'testo', 2),
        ('Codice motore', '', 'testo', 3), ('Validi al', '26/09/2026', 'data', 3)])
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Codice motore', 'Descrizione', 'Famiglia', 'Tipo contenuto',
                   'Inizio validità', 'Fine validità', 'Adottato'],
                  [90, 150, 330, 120, 110, 130, 130, 120], [
                      ['2101', 'Morte_001', 'Dichiarazione di morte in abitazione',
                       'Morte', '1', '16/10/2023', '—', ('SI', W.VERDE)],
                      ['2102', 'Morte_002', 'Dichiarazione di morte in ospedale',
                       'Morte', '1', '16/10/2023', '—', ('SI', W.VERDE)],
                      ['2104', 'Morte_004', 'Dichiarazione di morte — ignoto',
                       'Morte', '1', '16/10/2023', '—', ('NO', W.MUTED)],
                      ['2999', 'Morte_999', 'Caso d’uso di servizio (recupero)',
                       'Morte', '1', '12/06/2025', '—', ('SI', W.VERDE)],
                      ['2107', 'Morte_007', 'Caso d’uso ritirato',
                       'Morte', '1', '16/10/2023', '31/12/2025', ('NO', W.MUTED)],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='374', pagine=38)
    W.nota(dr, X, y, C,
           'ANSC non cancella un caso d’uso: gli chiude la validità. Un UC con fine validità '
           'valorizzata e ancora adottato — legato a un tipo atto — è una discordanza che il '
           'report d’impatto segnala.')
    return W.salva(im, dest, 'bo_catalogo_uc.png')


# ───────────────────────────────────────────────── versioni
def versioni(dest):
    im, dr, y = W.pagina(L, 800, ['Home', 'Integrazione ANSC', 'Versioni della configurazione'],
                         'Versioni della configurazione',
                         azioni_dx=['NUOVA BOZZA DA ATTIVA'],
                         sotto='Una sola versione può essere ATTIVA. '
                               'Le modifiche si fanno sulla BOZZA e diventano effettive con '
                               'l’attivazione.')
    y = W.tabella(dr, X, y, C,
                  ['Versione', 'Stato', 'Versione ANSC', 'UC toccati', 'Descrizione',
                   'Attivata il', 'Da', 'Azioni'],
                  [90, 120, 130, 100, 330, 120, 130, 130], [
                      ['v13', ('BOZZA', W.GIALLO), '1.53.0', '23',
                       'Recepimento revisione mapping del 20/09', '—', '—',
                       ['mod', 'vedi', 'del']],
                      ['v12', ('ATTIVA', W.VERDE), '1.52.0', '11',
                       'Allineamento allegati morte', '01/09/2026', 'c.lombardi', ['vedi']],
                      ['v11', ('STORICA', W.MUTED), '1.52.0', '4',
                       'Correzione riconciliazione ANSC_09', '12/08/2026', 'c.lombardi',
                       ['vedi']],
                      ['v10', ('STORICA', W.MUTED), '1.51.0', '301',
                       'Revisione massiva del mapping', '02/07/2026', 'b.puccetti', ['vedi']],
                  ])
    y += 6
    y = W.pannello(dr, X, y, C, 'Report d’impatto della bozza v13', alt=202)
    yy = y + 4
    for testo, valore, colore in [
        ('Casi d’uso toccati dalla revisione', '23', W.INK),
        ('Campi nuovi senza alias SIPO', '17', W.ROSSO),
        ('Campi non più presenti nel mapping', '4', W.GIALLO),
        ('UC ritirati da ANSC e ancora adottati', '1', W.ROSSO),
        ('Valori di decodifica non riconciliati', '9', W.ROSSO),
    ]:
        dr.text((X + 24, yy), testo, font=fnt(F_REG, 12), fill=MUTED)
        dr.text((X + 460, yy), valore, font=fnt(G.F_BLD, 12), fill=colore)
        yy += 24
    W.bottoni(dr, X + 24, yy + 6,
              [('ATTIVA LA VERSIONE', W.VERDE, True), ('SCARICA IL REPORT', W.MUTED),
               ('CONFRONTA CON L’ATTIVA', W.MUTED)])
    W.nota(dr, X + 600, y + 4, C - 624,
           'L’attivazione è consentita anche con scostamenti aperti, ma richiede conferma '
           'esplicita: gli atti che usano quei casi d’uso si fermeranno in preverifica. '
           'Il ritorno alla versione precedente è un cambio di stato, non un ripristino.',
           W.GIALLO)
    return W.salva(im, dest, 'bo_versioni.png')


# ───────────────────────────────────────────────── allegati per caso d'uso
def allegati_uc(dest):
    im, dr, y = W.pagina(L, 860, ['Home', 'Integrazione ANSC', 'Allegati per caso d’uso'],
                         'Allegati per caso d’uso',
                         azioni_dx=['CARICA DA FILE', 'ESPORTA CSV', 'NUOVA RIGA'],
                         sotto=SOTTO_V)
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=96)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Versione', 'v13 — BOZZA', 'select', 3), ('Registro', 'Tutti', 'select', 2),
        ('Codice UC', '', 'testo', 2), ('Tipo allegato', '', 'select', 3),
        ('Presenza', 'Tutte', 'select', 2), ('Operante', 'Sì', 'select', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Tipo', 'Descrizione (ANSC_09)', 'Presenza', 'Forma',
                   'Condizione', 'Ord.', 'Op.', 'Azioni'],
                  [100, 60, 370, 90, 120, 160, 60, 60, 172], [
                      ['2101', '32', 'Certificato necroscopico', 'F', 'BASE', '—', '1',
                       ('1', W.VERDE), ['mod', 'del']],
                      ['2101', '127', 'Documento autorizzativo', 'F', 'BASE', '—', '2',
                       ('1', W.VERDE), ['mod', 'del']],
                      ['11111000', '1', 'Attestazione di nascita', 'C001', 'BASE',
                       'ACCERT_1', '1', ('1', W.VERDE), ['mod', 'del']],
                      ['11111000', '2', 'Constatazione di avvenuto parto', 'C002', 'BASE',
                       'ACCERT_2', '2', ('1', W.VERDE), ['mod', 'del']],
                      ['11111000', '3', 'Dichiarazione di nascita sostitutiva …', 'C003',
                       'BASE', 'ACCERT_3', '3', ('1', W.VERDE), ['mod', 'del']],
                      ['14400000', '998', 'Allegato generico', 'F', 'D.LIB.M.01', '—',
                       '1', ('1', W.VERDE), ['mod', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='1.569', pagine=20)
    W.nota(dr, X, y, C,
           'La condizione è un codice di logica libero (cd_logica), valutato dal codice '
           'applicativo. La matita apre la riga in modifica; il cestino la disattiva '
           '(operante a 0) e non la cancella. CARICA DA FILE ed ESPORTA CSV usano lo stesso '
           'formato, quello in cui Side esporta la tabella.')
    return W.salva(im, dest, 'bo_allegati_uc.png')


# ───────────────────────────────────────────────── numerazione comunale
SOTTO_N = ('Il numero comunale è a carico del Comune: si stacca dalla serie dell’anno, unica '
           'per tutti i registri, tramite il servizio be-numeratore-comunale.')


def num_richiesta(dest):
    im, dr, y = W.pagina(L, 640, ['Home', 'Integrazione ANSC', 'Numerazione comunale',
                                  'Richiesta'],
                         'Numerazione comunale — richiesta', sotto=SOTTO_N)
    y = W.riga_campi(dr, X, y, C - 200, [
        ('Anno', '2027', 'testo', 3), ('Numero di elementi', '3', 'testo', 3)])
    W.bottoni_dx(dr, X + C, y - 52, [('RICHIEDI', W.BLU, True)])
    y += 2
    y = W.tabella(dr, X, y, C,
                  ['ID richiesta', 'Operatore', 'Data richiesta', 'Anno', 'Numero',
                   'Atto SIPO', 'Stato', 'Azioni'],
                  [130, 150, 150, 90, 120, 180, 180, 192], [
                      ['90211', 'admin', '14/03/2027', '2027', '1.140', '—',
                       ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                      ['90211', 'admin', '14/03/2027', '2027', '1.141', '—',
                       ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                      ['90211', 'admin', '14/03/2027', '2027', '1.142', '—',
                       ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                  ])
    W.nota(dr, X, y + 4, C,
           'I tre numeri di un parto trigemino escono consecutivi (POST /richiesta). La '
           'spunta segna il numero come Utilizzato (PUT /utilizza), con l’atto di SIPO se è '
           'noto; la croce lo segna come Scartato (PUT /scarta). Il servizio registra oggi '
           'come operatore sempre «admin».')
    return W.salva(im, dest, 'bo_num_richiesta.png')


def num_ricerca(dest):
    im, dr, y = W.pagina(L, 820, ['Home', 'Integrazione ANSC', 'Numerazione comunale',
                                  'Ricerca e consultazione'],
                         'Numerazione comunale — ricerca e consultazione', sotto=SOTTO_N)
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=196)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Anno', '2027', 'testo', 2), ('Stato', 'Tutti', 'select', 2),
        ('Numero', '', 'testo', 2), ('ID richiesta', '', 'testo', 2),
        ('Atto SIPO', '', 'testo', 2)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('Richieste da', '01/03/2027', 'data', 3), ('Richieste a', '14/03/2027', 'data', 3),
        ('Operatore', '', 'testo', 3)])
    y = W.bottoni_dx(dr, X + C - 16, y - 6, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 28
    y = W.tabella(dr, X, y, C,
                  ['ID richiesta', 'Operatore', 'Data richiesta', 'Anno', 'Numero',
                   'ID ANSC', 'Atto SIPO', 'Stato', 'Azioni'],
                  [110, 110, 130, 70, 90, 250, 120, 150, 162], [
                      ['90198', 'admin', '13/03/2027', '2027', '1.530', '—', '4581270',
                       ('UTILIZZATO', W.BLU), ['vedi']],
                      ['90204', 'admin', '13/03/2027', '2027', '1.531', '—', '—',
                       ('SCARTATO', W.MUTED), ['vedi']],
                      ['90215', 'admin', '14/03/2027', '2027', '1.532', '—', '—',
                       ('UTILIZZATO', W.BLU), ['vedi']],
                      ['90219', 'admin', '14/03/2027', '2027', '1.533', '—', '4581291',
                       ('DISPONIBILE', W.VERDE), ['vedi', 'ok', 'no']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='31', pagine=7)
    W.nota(dr, X, y, C,
           'I filtri sono i parametri di GET /ricerca. La colonna «ID ANSC» resta vuota: '
           'nessuna operazione del servizio la scrive. Lo stato della serie con i suoi '
           'buchi, la registrazione a posteriori e lo stato Evento acquisito non hanno '
           'ancora un’operazione (OP-79 dell’analisi).', W.GIALLO)
    return W.salva(im, dest, 'bo_num_ricerca.png')


# ───────────────────────────────────────────────── home, riconciliazione e comandi
def home(dest):
    im, dr, y = W.pagina(L, 700, ['Home'], 'Integrazione ANSC',
                         distintivo=('OTP', True),
                         sotto='Seleziona l’area su cui iniziare a operare.')
    voci = [
        ('Supervisione atti', 'gli atti che non hanno concluso il percorso ordinario'),
        ('Notifiche ANSC', 'proposte di annotazione, prese visione, solleciti'),
        ('Numerazione comunale', 'stacco e restituzione dei numeri'),
        ('Configurazione casi d’uso', 'UC adottati, campi, allegati, formule'),
        ('Catalogo UC di ANSC', 'ciò che ANSC pubblica — sola consultazione'),
        ('Dizionari ANSC', 'domini e valori scaricati con R901'),
        ('Riconciliazione decodifiche', 'la corrispondenza fra valori SIPO e valori ANSC'),
        ('Versioni della configurazione', 'bozza, attiva, storiche e report d’impatto'),
        ('Comandi di servizio', 'importazioni, scarichi, verifiche'),
        ('Audit e tracciato', 'che cosa è stato inviato, quando e da chi'),
        ('Postazioni e certificati', 'il registro delle postazioni abilitate'),
    ]
    w, h, gap = (C - 2 * 18) // 3, 62, 18
    for i, (t, s) in enumerate(voci):
        W.card(dr, X + (i % 3) * (w + gap), y + (i // 3) * (h + gap), w, h, t, s)
    yy = y + 4 * (h + gap) + 10
    W.nota(dr, X, yy, C,
           'La sessione ANSC dura quattro ore. Il distintivo in alto segnala se è attiva: '
           'le azioni che dialogano con ANSC sono disabilitate quando non lo è.')
    return W.salva(im, dest, 'bo_home.png')

def riconciliazione(dest):
    im, dr, y = W.pagina(L, 760, ['Home', 'Integrazione ANSC', 'Riconciliazione decodifiche'],
                         'Riconciliazione delle decodifiche',
                         azioni_dx=['IMPORTA DA EXCEL', 'NUOVA CORRISPONDENZA'],
                         sotto='La corrispondenza fra i valori delle tabelle CONF_* di SIPO '
                               'e i valori dei dizionari di ANSC. Versione v13 — BOZZA.')
    y = W.riga_campi(dr, X, y, C, [
        ('Decodifica ANSC', '7 — dec_sesso', 'select', 4),
        ('Schema e tabella SIPO', 'MATR_USR.CONF_SESSO', 'select', 4),
        ('Solo non riconciliati', 'Sì', 'select', 2), ('Validi al', '29/09/2026', 'data', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    # ⚠️ l'ordine delle colonne non è indifferente: prima ciò che ANSC dichiara — che è
    # certo — poi ciò che SIPO deve far corrispondere, che è il lavoro da fare.
    y = W.tabella(dr, X, y, C,
                  ['Decodifica', 'Valore ANSC', 'Descrizione ANSC', 'Valore SIPO',
                   'Descrizione SIPO', 'Campo SIPO', 'Validità', 'Azioni'],
                  [90, 100, 230, 130, 210, 220, 120, 92], [
                      ['7', '1', 'MASCHIO', 'M', 'MASCHIO', 'SOGGETTO.SESSO',
                       'dal 01/01/2026', ['mod', 'del']],
                      ['7', '2', 'FEMMINA', 'F', 'FEMMINA', 'SOGGETTO.SESSO',
                       'dal 01/01/2026', ['mod', 'del']],
                      ['9', '104', 'Certificato necroscopico', '7', 'CERT. NECROSCOPICO',
                       'CONF_ALLEGATI.ID_TIPO', 'dal 01/01/2026', ['mod', 'del']],
                      ['9', '112', 'Nulla osta autorità giudiziaria',
                       ('DA MAPPARE', W.ROSSO), '—', '—', '—', ['mod', 'del']],
                      ['26', '3', 'Procura fuori tempo massimo', '3', 'PROCURA',
                       'CONF_COMUNICAZ.ID_ENTE', 'dal 01/01/2026',
                       ['mod', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='612', pagine=62)
    W.nota(dr, X, y, C,
           'Le colonne di ANSC stanno a sinistra perché sono il dato certo: il dominio '
           'dichiara i suoi valori e non si discutono. Quelle di SIPO stanno a destra perché '
           'sono il lavoro da fare, ed è lì che compare «da mappare». Un valore ANSC senza '
           'corrispondenza SIPO blocca in preverifica ogni atto che lo usi.', W.ROSSO)
    return W.salva(im, dest, 'bo_riconciliazione.png')

def riconciliazione_dettaglio(dest):
    """La maschera con cui si inserisce o si corregge una corrispondenza.

    ⚠️ L'ordine dei due pannelli è la traduzione grafica della scelta di modello: ciò che
    ANSC dichiara è dato, ciò che SIPO deve far corrispondere è lavoro.
    """
    im, dr, y = W.pagina(L, 900,
                         ['Home', 'Integrazione ANSC', 'Riconciliazione decodifiche',
                          'Nuova corrispondenza'],
                         'Nuova corrispondenza',
                         azioni_dx=['SALVA E PROSSIMA', 'SALVA'],
                         sotto='Versione v13 — BOZZA. La corrispondenza vale da quando si '
                               'dichiara: quelle in vigore non si sovrascrivono, si chiudono.')

    y = W.pannello(dr, X, y, C, 'Lato ANSC — dichiarato dal dominio, non modificabile',
                   alt=124)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Decodifica', '9 — dec_tipo_allegato', 'select', 4),
        ('Valore ANSC *', '112', 'select', 2),
        ('Descrizione ANSC', 'Nulla osta autorità giudiziaria', 'testo', 4),
        ('Validità in ANSC', 'dal 16/10/2023', 'testo', 2)])
    y += 10

    y = W.pannello(dr, X, y, C, 'Lato SIPO — da completare', alt=190)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Schema', 'MATR_USR', 'select', 2),
        ('Tabella', 'CONF_ALLEGATI', 'select', 4),
        ('Campo', 'ID_TIPO', 'select', 3)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('Valore SIPO', '', 'select', 2),
        ('Descrizione SIPO', '', 'testo', 5),
        ('Stato', 'DA MAPPARE', 'testo', 2)])
    y += 10

    y = W.pannello(dr, X, y, C, 'Validità della corrispondenza', alt=124)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Valida dal *', '29/09/2026', 'data', 2),
        ('Valida fino al', '31/12/9999', 'data', 2)])
    y += 10

    y = W.nota(dr, X, y, C,
               'Il valore di ANSC è obbligatorio, quello di SIPO no: una riga senza valore '
               'SIPO è la dichiarazione che quel valore ammesso da ANSC non ha ancora un '
               'corrispondente locale. È ciò che la pagina d’elenco mostra come «da '
               'mappare», ed è il lavoro da fare.', W.GIALLO)
    W.nota(dr, X, y, C,
           'Esiste già una corrispondenza per questa decodifica, questo valore ANSC e questo '
           'campo, valida dal 01/01/2026. Salvando, quella verrà chiusa alla data indicata e '
           'la nuova varrà da lì in avanti: gli atti già depositati restano leggibili con la '
           'corrispondenza in vigore allora.', W.ROSSO)
    return W.salva(im, dest, 'bo_riconciliazione_dettaglio.png')

def comandi(dest):
    im, dr, y = W.pagina(L, 720, ['Home', 'Integrazione ANSC', 'Comandi di servizio'],
                         'Comandi e operazioni di servizio',
                         sotto='Le stesse operazioni sono eseguibili da riga di comando. '
                               'Qui se ne governa l’avvio e se ne consulta l’esito.')
    y = W.tabella(dr, X, y, C,
                  ['Comando', 'Che cosa fa', 'Ultima esecuzione', 'Esito', 'Durata',
                   'Azioni'],
                  [230, 380, 150, 140, 100, 192], [
                      ['Scarico dizionari (R901)',
                       'Ricarica domini e valori dai dizionari di ANSC', '20/09 04:12',
                       ('OK', W.VERDE), '4 m 10 s', ['vedi']],
                      ['Importazione mapping UC',
                       'Prepara campi, allegati e formule nella bozza',
                       '20/09 05:02', ('OK', W.VERDE), '11 m 38 s', ['vedi']],
                      ['Verifica di copertura',
                       'Elenca i campi obbligatori senza alias SIPO',
                       '25/09 09:00', ('CON RILIEVI', W.GIALLO), '52 s', ['vedi']],
                      ['Riconciliazione massiva',
                       'Richiede ad ANSC lo stato reale degli atti indeterminati',
                       '25/09 18:00', ('OK', W.VERDE), '2 m 04 s', ['vedi']],
                      ['Controllo revisioni ANSC',
                       'Confronta le versioni pubblicate con quelle in uso', '26/09 06:00',
                       ('NUOVA REVISIONE', W.BLU), '8 s', ['vedi']],
                  ])
    y += 6
    y = W.pannello(dr, X, y, C, 'Avvio di un comando', alt=150)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Comando', 'Importazione mapping UC', 'select', 4),
        ('Versione di destinazione', 'v13 — BOZZA', 'select', 3),
        ('Famiglia', 'Morte', 'select', 2), ('Solo simulazione', 'Sì', 'select', 2)])
    W.bottoni(dr, X + 16, y, [('AVVIA', W.BLU, True), ('VEDI REGISTRO', W.MUTED)])
    return W.salva(im, dest, 'bo_comandi.png')


FIGURE = (mfe, home, atto, uc_elenco, uc_dettaglio, catalogo, versioni, allegati_uc,
          num_richiesta, num_ricerca, riconciliazione, riconciliazione_dettaglio, comandi)

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(base, 'img', 'bo_v0_11')
    os.makedirs(dest, exist_ok=True)
    for f in FIGURE:
        print('  scritto', f(dest))
