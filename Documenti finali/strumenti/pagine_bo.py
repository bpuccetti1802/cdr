# -*- coding: utf-8 -*-
"""Le pagine del back-office dell'integrazione SIPO→ANSC, in forma di wireframe.

Una funzione per pagina; il nome del file prodotto è il nome della funzione con prefisso
«bo_». Le convenzioni grafiche stanno in `wireframe_bo.py` e derivano da S.I.De.

⚠️ Quando cambia il modello dati queste pagine vanno rifatte: un wireframe che mostra una
colonna che non esiste più induce in errore chi lo legge per costruire.

    /Library/Developer/CommandLineTools/usr/bin/python3 pagine_bo.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wireframe_bo as W   # noqa: E402
from diagrammi_comune import F_BLD, F_ITA, F_REG, MUTED, centra, fnt  # noqa: E402

L = 1240          # larghezza della pagina
X = 24            # margine sinistro del contenuto
C = L - 2 * X     # larghezza utile


# ─────────────────────────────────────────────────────────────── 1. home
def home(dest):
    im, dr, y = W.pagina(L, 700, ['Home'], 'Integrazione ANSC',
                         distintivo=('OTP', True),
                         sotto='Seleziona l’area su cui iniziare a operare.')
    voci = [
        ('Supervisione atti', 'gli atti che non hanno concluso il percorso ordinario'),
        ('Notifiche ANSC', 'proposte di annotazione, prese visione, solleciti'),
        ('Numerazione comunale', 'stacco e restituzione dei numeri'),
        ('Configurazione casi d’uso', 'UC adottati, sezioni, campi, allegati, formule'),
        ('Catalogo UC di ANSC', 'ciò che ANSC pubblica — sola consultazione'),
        ('Logiche di scelta', 'le espressioni che determinano UC, sezioni e campi'),
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


# ──────────────────────────────────────────────────── 2. supervisione atti
def atti(dest):
    im, dr, y = W.pagina(L, 820, ['Home', 'Integrazione ANSC', 'Supervisione atti'],
                         'Supervisione atti', distintivo=('OTP', True),
                         azioni_dx=['RICONCILIA SELEZIONATI', 'ESPORTA'])
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=196)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Fase', 'Validazione', 'select', 3), ('Stato ANSC', 'Tutti', 'select', 3),
        ('Categoria di eccezione', 'Rifiutati in validazione', 'select', 4),
        ('Municipio', 'Tutti', 'select', 2)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('Registro', 'Morte', 'select', 2), ('UC', '2101', 'testo', 2),
        ('ID ANSC', '', 'testo', 3), ('Numero comunale', '', 'testo', 2),
        ('Data da', '01/09/2026', 'data', 2), ('Data a', '26/09/2026', 'data', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 8
    y = W.chipbar(dr, X, y) if hasattr(W, 'chipbar') else y
    righe = [
        ['2026/0041287', 'Morte', '2101', 'Validazione', ('RIFIUTATA', W.ROSSO),
         '2026-10438958-00000-058091', '13.557', 'g.rossi', ['vedi', 'mod']],
        ['2026/0041290', 'Morte', '2102', 'Documenti', ('IN CORSO', W.GIALLO),
         '—', '13.558', 'g.rossi', ['vedi', 'mod']],
        ['2026/0041301', 'Nascita', '11111000', 'Firma', ('INDETERMINATO', W.VIOLA),
         '2026-10438961-00000-058091', '13.559', 'm.bianchi', ['vedi', 'ok']],
        ['2026/0041305', 'Morte', '—', 'Lavorazione', ('UC AMBIGUO', W.GIALLO),
         '—', '—', 'm.bianchi', ['vedi', 'mod']],
        ['2026/0041312', 'Nascita', '11111200', 'Validazione', ('EMERGENZA', W.VIOLA),
         '—', '13.561', 'a.verdi', ['vedi', 'mod']],
        ['2026/0041318', 'Morte', '2101', 'Firma', ('BOZZA', W.BLU),
         '2026-10438970-00000-058091', '13.562', 'a.verdi', ['vedi', 'no']],
    ]
    y = W.tabella(dr, X, y, C,
                  ['Atto SIPO', 'Registro', 'UC', 'Fase', 'Stato', 'ID ANSC',
                   'N. comunale', 'Operatore', 'Azioni'],
                  [120, 84, 96, 108, 132, 250, 110, 110, 90], righe)
    W.paginazione(dr, X, y + 4, C, totale='214', pagine=4)
    return W.salva(im, dest, 'bo_atti.png')


# ───────────────────────────────────────────────────────── 3. dettaglio atto
def atto(dest):
    im, dr, y = W.pagina(L, 880,
                         ['Home', 'Integrazione ANSC', 'Supervisione atti', '2026/0041287'],
                         'Atto 2026/0041287 — [2101] Morte in abitazione',
                         distintivo=('OTP', True),
                         azioni_dx=['REGISTRO DI EMERGENZA'])
    y = W.pannello(dr, X, y, C, 'Scenario — atto SIPO salvato il 24/09/2026 alle 09:41',
                   alt=104)
    y = W.righe_etichette(dr, X + 20, y + 2, [
        ('Registro', 'Morte'), ('Modello', '01'), ('Tipo atto', '301'),
        ('UC determinato', '2101 (Morte_001)'), ('Origine UC', 'LOGICA'),
        ('Versione configurazione', 'v12 — ATTIVA')], C - 40)
    y += 14
    y = W.schede(dr, X, y, C,
                 ['Sezioni e campi', 'Allegati', 'Cronologia', 'Payload inviato'], attiva=0)
    y = W.accordion(dr, X, y, C, [
        ('Dati generali', 'ok'), ('Defunto', 'ok'), ('Dichiarante', 'ko'),
        ('Luogo del decesso', 'ok'), ('Formula', 'ok'), ('Allegati', 'ko')])
    y = W.nota(dr, X, y, C,
               'Sezione «Dichiarante»: il campo dichiarante.idANPR è obbligatorio per l’UC '
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
    y = W.bottoni(dr, X, y + 6, [
        ('RIPRENDI DA VALIDAZIONE', W.BLU, True), ('RICONCILIA CON ANSC', W.BLU),
        ('SCARICA PAYLOAD', W.MUTED), ('ANNULLA ATTO', W.ROSSO)])
    return W.salva(im, dest, 'bo_atto.png')


# ─────────────────────────────────────────────────────────── 4. allegati
def allegati(dest):
    im, dr, y = W.pagina(L, 720,
                         ['Home', 'Integrazione ANSC', 'Supervisione atti',
                          '2026/0041287', 'Allegati'],
                         'Allegati dell’atto 2026/0041287', distintivo=('OTP', True))
    y = W.nota(dr, X, y, C,
               'La dimensione del file non deve superare 10 Mb; il nome non deve contenere '
               'spazi o caratteri speciali; sono ammessi PDF, JPG, TIF, P7M. Un allegato è '
               'utilizzabile solo quando ANSC lo dichiara «Inserito».')
    dr.text((X, y), 'Documenti richiesti dall’UC 2101', font=fnt(F_BLD, 13), fill=W.INK)
    y += 24
    y = W.tabella(dr, X, y, C,
                  ['Descrizione (ALLEGATI_USECASE)', 'Obbl.', 'Condizione', 'File',
                   'Stato ANSC', 'Conformità', 'Azioni'],
                  [330, 60, 180, 220, 130, 100, 120], [
                      ['Certificato necroscopico', 'SI', '—', 'cert_necro.pdf',
                       ('INSERITO', W.VERDE), 'SI', ['vedi', 'del']],
                      ['Scheda ISTAT di morte', 'SI', '—', 'istat_morte.pdf',
                       ('IN SCANSIONE', W.GIALLO), 'NO', ['vedi', 'del']],
                      ['Nulla osta autorità giudiziaria', 'NO', 'se morte violenta', '—',
                       ('ASSENTE', W.MUTED), '—', ['ok']],
                      ['Delega del dichiarante', 'NO', 'se dichiarante = 3', '—',
                       ('ASSENTE', W.MUTED), '—', ['ok']],
                  ])
    dr.text((X, y + 6), 'Atti a testo libero', font=fnt(F_BLD, 13), fill=W.INK)
    y += 30
    W.campo(dr, X, y, 420, 'Descrizione del documento', 'Verbale di ricognizione')
    W.ic_piu(dr, X + 438, y + 9)
    y += 52
    y = W.tabella(dr, X, y, C,
                  ['Descrizione', 'File', 'Caricato da', 'Stato ANSC', 'Azioni'],
                  [330, 300, 200, 220, 120], [
                      ['Verbale di ricognizione', 'verbale_01.pdf', 'g.rossi',
                       ('INSERITO', W.VERDE), ['vedi', 'del']],
                  ])
    W.bottoni(dr, X, y + 6, [('INVIA AD ANSC', W.BLU, True), ('INDIETRO', W.MUTED)])
    return W.salva(im, dest, 'bo_allegati.png')


# ─────────────────────────────────────────────────────────── 5. notifiche
def notifiche(dest):
    im, dr, y = W.pagina(L, 800, ['Home', 'Integrazione ANSC', 'Notifiche ANSC'],
                         'Gestione notifiche ANSC', distintivo=('OTP', True),
                         azioni_dx=['SCARICA NOTIFICHE RECENTI'])
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=140)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Genere', 'Annotazione', 'select', 3), ('Stato', 'Da approvare', 'select', 3),
        ('Comune di formazione', 'Tutti', 'select', 4),
        ('Sollecito', 'Tutti', 'select', 2)])
    y = W.riga_campi(dr, X + 16, y, C - 32, [
        ('ID ANSC notifica', '', 'testo', 4), ('Intestatario', '', 'testo', 3),
        ('Data da', '01/09/2026', 'data', 2), ('Data a', '26/09/2026', 'data', 2)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['Intestatario', 'Genere', 'Comune form.', 'Descrizione', 'Formazione',
                   'Stato', 'Sollecito', 'Azioni'],
                  [180, 110, 120, 330, 100, 120, 100, 100], [
                      ['ALESSANDRO MARTINI', 'Annotazione', 'MILANO',
                       'Annotazione automatica id 2026-10438958…', '25/04/2026',
                       ('DA APPROVARE', W.GIALLO), '—', ['ok', 'no', 'vedi']],
                      ['STEFANIA DISTEFANO', 'Trascrizione', 'LISSONE',
                       'Annotazione automatica id 2026-10438956…', '25/04/2026',
                       ('DA APPROVARE', W.GIALLO), ('SCADUTO', W.ROSSO),
                       ['ok', 'no', 'vedi']],
                      ['JIOGO ZHU', 'Annotazione', 'MILANO',
                       'Annotazione automatica id 2026-10438869…', '24/04/2026',
                       ('APPROVATA', W.VERDE), '—', ['vedi']],
                      ['PAOLO VERDI', 'Presa visione', 'ROMA',
                       'Atto di morte registrato con numero 2026-10437342…', '16/06/2026',
                       ('RIFIUTATA', W.ROSSO), '—', ['vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='87', pagine=9)
    y = W.nota(dr, X, y, C,
               'La conferma è per singola notifica: non esiste selezione multipla. Finché '
               'tutti i comuni coinvolti non hanno confermato, la comunicazione anagrafica '
               'non parte; un solo rifiuto la annulla.')
    return W.salva(im, dest, 'bo_notifiche.png')


# ──────────────────────────────────────────────── 6. configurazione UC (elenco)
def uc_elenco(dest):
    im, dr, y = W.pagina(L, 760, ['Home', 'Integrazione ANSC', 'Configurazione casi d’uso'],
                         'Configurazione dei casi d’uso',
                         azioni_dx=['IMPORTA DA MAPPING', 'NUOVO UC'],
                         sotto='Versione in lavorazione: v13 — BOZZA. '
                               'Le modifiche non hanno effetto finché la versione non è attivata.')
    y = W.pannello(dr, X, y, C, 'Filtri di ricerca', alt=96)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Registro / tipo evento', 'Morte', 'select', 3), ('Codice UC', '', 'testo', 2),
        ('Modello atto', '', 'testo', 2), ('Stato', 'Attivi', 'select', 2),
        ('Versione', 'v13 — BOZZA', 'select', 3)])
    y = W.bottoni_dx(dr, X + C - 16, y, [('PULISCI', W.MUTED), ('CERCA', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Descrizione', 'Modello', 'Tipo atto', 'Maschera',
                   'Priorità', 'Logica di scelta', 'Stato', 'Azioni'],
                  [90, 300, 80, 86, 130, 80, 200, 110, 100], [
                      ['2101', 'Morte in abitazione a Roma', '01', '301',
                       'attoMorteTipo01', '10', 'D1 · L003', ('ATTIVO', W.VERDE),
                       ['mod', 'vedi']],
                      ['2102', 'Morte in ospedale a Roma', '03', '303',
                       'attoMorteTipo03', '20', 'D1 · L004', ('ATTIVO', W.VERDE),
                       ['mod', 'vedi']],
                      ['2103', 'Morte in casa di cura', '04', '304',
                       'attoMorteTipo04', '30', 'D1 · L005', ('BOZZA', W.GIALLO),
                       ['mod', 'vedi']],
                      ['2201', 'Trascrizione morte altro comune', '11', '311',
                       'attoMorteTipo11', '40', 'D1 · L011', ('ATTIVO', W.VERDE),
                       ['mod', 'vedi']],
                      ['2999', 'Caso d’uso di servizio — recupero', '—', '—', '—',
                       '99', '—', ('SOSPESO', W.MUTED), ['mod', 'vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='25', pagine=3)
    W.nota(dr, X, y, C,
           'La priorità decide quale UC vince quando più logiche rispondono sullo stesso '
           'atto: il primo in ordine di priorità è quello adottato. Senza logica di scelta '
           'l’UC è candidato ma non determinabile automaticamente.')
    return W.salva(im, dest, 'bo_uc_elenco.png')


# ─────────────────────────────────────────── 7. configurazione UC (dettaglio)
def uc_dettaglio(dest):
    im, dr, y = W.pagina(L, 880,
                         ['Home', 'Integrazione ANSC', 'Configurazione casi d’uso', '2101'],
                         '[2101] Morte in abitazione a Roma',
                         azioni_dx=['SIMULA SU ATTO REALE', 'SALVA'],
                         sotto='Versione v13 — BOZZA · Modello 01 · Tipo atto 301 · '
                               'Maschera attoMorteTipo01')
    y = W.schede(dr, X, y, C,
                 ['Dati generali', 'Sezioni', 'Campi', 'Allegati', 'Formule'], attiva=2)
    y = W.riga_campi(dr, X, y, C, [
        ('Sezione', 'Defunto', 'select', 3), ('Solo obbligatori', 'No', 'select', 2),
        ('Senza corrispondenza SIPO', 'Sì', 'select', 3), ('Cerca campo', '', 'testo', 3)])
    y = W.tabella(dr, X, y, C,
                  ['Oggetto ANSC', 'Campo ANSC', 'Obbl.', 'Schema', 'Tabella SIPO',
                   'Campo SIPO', 'Decodifica', 'Logica', 'Azioni'],
                  [140, 170, 56, 80, 150, 160, 110, 130, 90], [
                      ['defunto', 'cognome', 'SI', 'MATR_USR', 'SOGGETTO', 'COGNOME',
                       '—', '—', ['mod']],
                      ['defunto', 'nome', 'SI', 'MATR_USR', 'SOGGETTO', 'NOME',
                       '—', '—', ['mod']],
                      ['defunto', 'sesso', 'SI', 'MATR_USR', 'SOGGETTO', 'SESSO',
                       'ANSC_07', 'D3 · L021', ['mod']],
                      ['defunto', 'idANPR', 'SI', '—', '—', '—', '—',
                       ('DA COMPLETARE', W.ROSSO), ['mod']],
                      ['defunto', 'dataEvento', 'SI', 'MATR_USR', 'ATTO_DECESSO',
                       'DATA_DECESSO', '—', 'D3 · L022', ['mod']],
                      ['luogoDecesso', 'idComune', 'SI', 'ANAG_USR', 'COMUNE',
                       'CODICE_ISTAT', 'ANSC_02', '—', ['mod']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='85', pagine=9)
    y = W.nota(dr, X, y, C,
               'Quattro campi obbligatori dell’UC non hanno ancora una corrispondenza in '
               'SIPO. Finché restano scoperti la preverifica li segnala e l’atto non può '
               'essere depositato.', W.ROSSO)
    W.bottoni(dr, X, y, [('AGGIUNGI CAMPO', W.BLU), ('REIMPORTA SEZIONE', W.MUTED),
                         ('ESPORTA IN EXCEL', W.MUTED)])
    return W.salva(im, dest, 'bo_uc_dettaglio.png')


# ──────────────────────────────────────────────────────── 8. catalogo UC
def catalogo(dest):
    im, dr, y = W.pagina(L, 640, ['Home', 'Integrazione ANSC', 'Catalogo UC di ANSC'],
                         'Catalogo dei casi d’uso pubblicati da ANSC',
                         azioni_dx=['AGGIORNA DA ANSC'],
                         sotto='Sola consultazione: è ciò che ANSC dichiara. '
                               'Ultimo aggiornamento 20/09/2026, versione mapping 1.53.0.')
    y = W.riga_campi(dr, X, y, C, [
        ('Famiglia', 'Morte', 'select', 3), ('Codice UC', '', 'testo', 2),
        ('Codice motore', '', 'testo', 3), ('Validi al', '26/09/2026', 'data', 3)])
    y = W.tabella(dr, X, y, C,
                  ['Cod. UC', 'Codice motore', 'Descrizione', 'Famiglia', 'Tipo evento',
                   'Inizio validità', 'Fine validità', 'Adottato'],
                  [90, 150, 330, 120, 110, 130, 130, 120], [
                      ['2101', 'Morte_001', 'Dichiarazione di morte in abitazione',
                       'Morte', '2', '16/10/2023', '—', ('SI', W.VERDE)],
                      ['2102', 'Morte_002', 'Dichiarazione di morte in ospedale',
                       'Morte', '2', '16/10/2023', '—', ('SI', W.VERDE)],
                      ['2104', 'Morte_004', 'Dichiarazione di morte — ignoto',
                       'Morte', '2', '16/10/2023', '—', ('NO', W.MUTED)],
                      ['2999', 'Morte_999', 'Caso d’uso di servizio (recupero)',
                       'Morte', '2', '12/06/2025', '—', ('SI', W.VERDE)],
                      ['2107', 'Morte_007', 'Caso d’uso ritirato',
                       'Morte', '2', '16/10/2023', '31/12/2025', ('NO', W.MUTED)],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='374', pagine=38)
    W.nota(dr, X, y, C,
           'ANSC non cancella un caso d’uso: gli chiude la validità. Un UC con fine validità '
           'valorizzata e ancora adottato nella configurazione è una discordanza che il '
           'report d’impatto segnala.')
    return W.salva(im, dest, 'bo_catalogo_uc.png')


# ───────────────────────────────────────────────────────── 9. logiche di scelta
def logiche(dest):
    im, dr, y = W.pagina(L, 780, ['Home', 'Integrazione ANSC', 'Logiche di scelta'],
                         'Logiche di scelta', azioni_dx=['NUOVA LOGICA'],
                         sotto='Le espressioni che il concentratore valuta sui dati '
                               'dell’atto già salvato in SIPO.')
    y = W.riga_campi(dr, X, y, C, [
        ('Dominio', '1 — Scelta dell’UC', 'select', 5), ('Codice', '', 'testo', 2),
        ('Cerca nel testo', '', 'testo', 5)])
    y = W.tabella(dr, X, y, C,
                  ['Dominio', 'Codice', 'Descrizione', 'Espressione', 'Usata da', 'Azioni'],
                  [200, 90, 300, 380, 110, 112], [
                      ['1 — Scelta UC', 'L003', 'Morte in abitazione',
                       'ATTO_DECESSO.ID_LUOGO_DECESSO = 1', '1 UC', ['mod', 'del']],
                      ['1 — Scelta UC', 'L004', 'Morte in ospedale',
                       'ATTO_DECESSO.ID_LUOGO_DECESSO = 2', '1 UC', ['mod', 'del']],
                      ['2 — Presenza sezione', 'L012', 'Dichiarante delegato',
                       'ATTO_DECESSO.ID_DICHIARANTE = 3', '4 sezioni', ['mod', 'del']],
                      ['3 — Logica di campo', 'L021', 'Sesso da decodifica',
                       'RICONCILIA(\'ANSC_07\', SOGGETTO.SESSO)', '12 campi',
                       ['mod', 'del']],
                      ['3 — Logica di campo', 'L022', 'Data in formato ANSC',
                       'FORMATO_DATA(ATTO_DECESSO.DATA_DECESSO, \'YYYY-MM-DD\')',
                       '9 campi', ['mod', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='64', pagine=7)
    y = W.pannello(dr, X, y, C, 'Simulazione su atto reale', alt=150)
    y = W.riga_campi(dr, X + 16, y + 6, C - 32, [
        ('Atto SIPO', '2026/0041287', 'testo', 3), ('Logica', 'L003', 'select', 3)])
    W.bottoni(dr, X + 16, y, [('ESEGUI SIMULAZIONE', W.BLU, True)])
    dr.text((X + 340, y + 6), 'Esito: VERO  ·  UC determinato: 2101  ·  durata 42 ms',
            font=fnt(F_BLD, 12), fill=W.VERDE)
    return W.salva(im, dest, 'bo_logiche.png')


# ────────────────────────────────────────────────────────── 10. dizionari
def dizionari(dest):
    im, dr, y = W.pagina(L, 760, ['Home', 'Integrazione ANSC', 'Dizionari ANSC'],
                         'Dizionari ANSC', azioni_dx=['SCARICA DA ANSC (R901)'],
                         sotto='Ultimo scarico completato il 20/09/2026 alle 04:12 — '
                               '145 tabelle, 1.376 valori.')
    y = W.riga_campi(dr, X, y, C, [
        ('Dominio', '7 — dec_sesso', 'select', 5),
        ('Valore o descrizione', '', 'testo', 4), ('Validi al', '29/09/2026', 'data', 3)])
    dr.text((X, y), 'Domini — da R901 /config/decodifica/elenco',
            font=fnt(F_BLD, 13), fill=W.INK)
    y += 24
    y = W.tabella(dr, X, y, 560,
                  ['ID', 'Nome della tabella', 'Versione', 'Valori', 'Usato da'],
                  [60, 230, 90, 80, 100], [
                      ['7', 'dec_sesso', '1.4.0', '2', '12 campi'],
                      ['9', 'dec_tipo_allegato', '1.9.2', '128', '31 allegati'],
                      ['11', 'dec_stato_evento', '1.4.0', '11', 'stato atto'],
                      ['134', 'dec_dichiarante_trascr_nascita', '1.2.0', '6', '2 campi'],
                      ['134', 'dec_dichiarante_trascr_postuma', '1.2.0', '5', '1 campo'],
                  ])
    dr.text((X + 600, y - 202), 'Valori — dal CSV di R901 /config/decodifica/dettaglio',
            font=fnt(F_BLD, 13), fill=W.INK)
    W.tabella(dr, X + 600, y - 178, C - 600,
              ['ID', 'Descrizione', 'Ordin.', 'Inizio validità', 'Fine validità'],
              [60, 190, 70, 120, 122], [
                  ['1', 'MASCHIO', '1', '01/01/1900', '31/12/9999'],
                  ['2', 'FEMMINA', '2', '01/01/1900', '31/12/9999'],
              ])
    y = W.nota(dr, X, y + 8, C,
               'R901 restituisce l’elenco con tre soli dati per tabella — identificativo, '
               'nome e versione — e il dettaglio come CSV in base64, compresso per '
               'impostazione predefinita, con le colonne ID, DESCRIZIONE, '
               'DATAINIZIOVALIDITA, DATAFINEVALIDITA, ORDINAMENTO. Le colonne «Valori» e '
               '«Usato da» sono conteggi calcolati in locale, non dati di ANSC.')
    y = W.nota(dr, X, y, C,
               'Due identificativi su 143 coprono due tabelle diverse (134 e 135): per '
               'questo la chiave comprende il nome della tabella e non il solo '
               'identificativo. La versione è il dato che consente di accorgersi che una '
               'tabella è cambiata senza riscaricarla.', W.GIALLO)
    W.bottoni(dr, X, y, [('STORICO DEGLI SCARICHI', W.MUTED), ('ESPORTA', W.MUTED)])
    return W.salva(im, dest, 'bo_dizionari.png')


# ────────────────────────────────────────────────── 11. riconciliazione
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
                   'Descrizione SIPO', 'Campo SIPO', 'Condizione', 'Validità', 'Azioni'],
                  [90, 100, 190, 120, 180, 170, 150, 110, 82], [
                      ['7', '1', 'MASCHIO', 'M', 'MASCHIO', 'SOGGETTO.SESSO', '—',
                       'dal 01/01/2026', ['mod', 'del']],
                      ['7', '2', 'FEMMINA', 'F', 'FEMMINA', 'SOGGETTO.SESSO', '—',
                       'dal 01/01/2026', ['mod', 'del']],
                      ['9', '104', 'Certificato necroscopico', '7', 'CERT. NECROSCOPICO',
                       'CONF_ALLEGATI.ID_TIPO', '—', 'dal 01/01/2026', ['mod', 'del']],
                      ['9', '112', 'Nulla osta autorità giudiziaria',
                       ('DA MAPPARE', W.ROSSO), '—', '—', '—', '—', ['mod', 'del']],
                      ['26', '3', 'Procura fuori tempo massimo', '3', 'PROCURA',
                       'CONF_COMUNICAZ.ID_ENTE', 'se termine superato', 'dal 01/01/2026',
                       ['mod', 'del']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='612', pagine=62)
    W.nota(dr, X, y, C,
           'Le colonne di ANSC stanno a sinistra perché sono il dato certo: il dominio '
           'dichiara i suoi valori e non si discutono. Quelle di SIPO stanno a destra perché '
           'sono il lavoro da fare, ed è lì che compare «da mappare». Un valore ANSC senza '
           'corrispondenza SIPO blocca in preverifica ogni atto che lo usi.', W.ROSSO)
    return W.salva(im, dest, 'bo_riconciliazione.png')


# ─────────────────────────────────────────────────────────── 12. versioni
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
                       'Allineamento allegati morte', '01/09/2026', 'c.lombardi',
                       ['vedi']],
                      ['v11', ('STORICA', W.MUTED), '1.52.0', '4',
                       'Correzione riconciliazione ANSC_09', '12/08/2026', 'c.lombardi',
                       ['vedi']],
                      ['v10', ('STORICA', W.MUTED), '1.51.0', '301',
                       'Revisione massiva del mapping', '02/07/2026', 'b.puccetti',
                       ['vedi']],
                  ])
    y += 6
    y = W.pannello(dr, X, y, C, 'Report d’impatto della bozza v13', alt=226)
    yy = y + 4
    for testo, valore, colore in [
        ('Casi d’uso toccati dalla revisione', '23', W.INK),
        ('Campi nuovi senza corrispondenza SIPO', '17', W.ROSSO),
        ('Campi non più presenti nel mapping', '4', W.GIALLO),
        ('Logiche di scelta che perdono copertura', '2', W.ROSSO),
        ('UC ritirati da ANSC e ancora adottati', '1', W.ROSSO),
        ('Valori di decodifica non riconciliati', '9', W.ROSSO),
    ]:
        dr.text((X + 24, yy), testo, font=fnt(F_REG, 12), fill=MUTED)
        dr.text((X + 460, yy), valore, font=fnt(F_BLD, 12), fill=colore)
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


# ──────────────────────────────────────────────────────────── 13. comandi
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
                       'Prepara sezioni, campi, allegati e formule nella bozza',
                       '20/09 05:02', ('OK', W.VERDE), '11 m 38 s', ['vedi']],
                      ['Verifica di copertura',
                       'Elenca i campi obbligatori senza corrispondenza SIPO',
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


# ──────────────────────────────────────────────────────── 14. numerazione
def numerazione(dest):
    im, dr, y = W.pagina(L, 640, ['Home', 'Integrazione ANSC', 'Numerazione comunale'],
                         'Numerazione comunale — stacco e restituzione',
                         distintivo=('OTP', True),
                         sotto='Il numero comunale è a carico del Comune: nessun servizio '
                               'di ANSC lo assegna.')
    y = W.riga_campi(dr, X, y, C, [
        ('Registro', 'Morte', 'select', 3), ('Anno', '2026', 'testo', 2),
        ('Numero di elementi', '2', 'testo', 3)])
    y = W.bottoni_dx(dr, X + C - 16, y - 8, [('RICHIEDI', W.BLU, True)])
    y += 6
    y = W.tabella(dr, X, y, C,
                  ['ID richiesta', 'Operatore', 'Data', 'Registro', 'Anno', 'Numero',
                   'ID ANSC', 'Stato', 'Azioni'],
                  [110, 130, 110, 110, 80, 110, 280, 140, 120], [
                      ['174', 'g.rossi', '26/09/2026', 'Morte', '2026', '13.557', '—',
                       ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                      ['174', 'g.rossi', '26/09/2026', 'Morte', '2026', '13.558', '—',
                       ('DISPONIBILE', W.VERDE), ['ok', 'no']],
                      ['173', 'm.bianchi', '25/09/2026', 'Morte', '2026', '13.556',
                       '2026-10438958-00000-058091', ('CONSUMATO', W.MUTED), ['vedi']],
                      ['172', 'a.verdi', '25/09/2026', 'Nascita', '2026', '13.555', '—',
                       ('RESTITUITO', W.GIALLO), ['vedi']],
                  ])
    y = W.paginazione(dr, X, y + 4, C, totale='1.284', pagine=20)
    W.nota(dr, X, y, C,
           'Per il parto plurimo i numeri vanno staccati in blocco e in anticipo, perché la '
           'prenotazione in ANSC li richiede tutti insieme. Un numero non usato va restituito '
           'esplicitamente: la numerazione non tollera salti.', W.GIALLO)
    return W.salva(im, dest, 'bo_numerazione.png')


PAGINE = [home, atti, atto, allegati, notifiche, uc_elenco, uc_dettaglio, catalogo,
          logiche, dizionari, riconciliazione, versioni, comandi, numerazione]

if __name__ == '__main__':
    dest = sys.argv[1] if len(sys.argv) > 1 else 'img'
    base = os.path.dirname(os.path.abspath(__file__))
    dest = dest if os.path.isabs(dest) else os.path.join(base, dest)
    for f in PAGINE:
        print('  scritto', f(dest))
