# -*- coding: utf-8 -*-
"""I wireframe del back-office del componente ANSC.

Sono schizzi funzionali, non un progetto grafico: dicono che cosa una schermata mostra e
quali azioni offre, non come sarà disegnata. ⚠️ Vanno rifatti quando cambia il modello dati o
l'elenco delle azioni: uno schizzo che mostra colonne che non esistono più induce in errore
chi lo legge per capire che cosa si deve costruire.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_backoffice.py img
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import F_BLD, F_ITA, F_REG, MUTED, avvolgi, centra, fnt  # noqa: E402

INK, BORDO, TENUE = '#1f2937', '#c7cdd6', '#f3f4f6'
BLU, VERDE, ROSSO, GIALLO, VIOLA = '#2f6bb0', '#3f8f5f', '#b03a48', '#d9a441', '#7b5aa6'


# ────────────────────────────────────────────────────────────── primitive
def finestra(larg, alt, titolo, ruolo):
    im = Image.new('RGB', (larg, alt), 'white')
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([10, 10, larg - 10, alt - 10], radius=10, outline=BORDO, width=2,
                         fill='white')
    dr.rounded_rectangle([10, 10, larg - 10, 46], radius=10, fill=TENUE, outline=BORDO, width=2)
    dr.rectangle([12, 38, larg - 12, 46], fill=TENUE)
    dr.text((26, 20), titolo, font=fnt(F_BLD, 15), fill=INK)
    dr.text((larg - 26 - dr.textlength(ruolo, font=fnt(F_REG, 13)), 22), ruolo,
            font=fnt(F_REG, 13), fill=MUTED)
    return im, dr


def testata(dr, x, y, titolo, sotto, larg=1100):
    dr.text((x, y), titolo, font=fnt(F_BLD, 22), fill=INK)
    yy = y + 32
    for riga in avvolgi(dr, sotto, fnt(F_ITA, 13), larg):
        dr.text((x, yy), riga, font=fnt(F_ITA, 13), fill=MUTED)
        yy += 17
    return yy + 6


def filtri(dr, x, y, voci, larg=None):
    for v in voci:
        w = larg or int(dr.textlength(v, font=fnt(F_REG, 13))) + 42
        dr.rounded_rectangle([x, y, x + w, y + 26], radius=6, outline=BORDO, width=2)
        dr.text((x + 12, y + 5), v, font=fnt(F_REG, 13), fill=MUTED)
        cx, cy = x + w - 16, y + 12
        dr.polygon([(cx - 5, cy - 2), (cx + 5, cy - 2), (cx, cy + 4)], fill=MUTED)
        x += w + 12
    return y + 38


def chip(dr, x, y, voci):
    for n, testo, colore in voci:
        w = int(dr.textlength(testo, font=fnt(F_REG, 13))) + 56
        dr.rounded_rectangle([x, y, x + w, y + 28], radius=14, outline=colore, width=2)
        dr.ellipse([x + 8, y + 6, x + 24, y + 22], fill=colore)
        centra(dr, str(n), fnt(F_BLD, 11), x + 16, y + 8, 'white')
        dr.text((x + 32, y + 6), testo, font=fnt(F_REG, 13), fill=INK)
        x += w + 10
    return y + 40


def tabella(dr, x, y, larg, intestazioni, larghezze, righe, alt=34):
    dr.rounded_rectangle([x, y, x + larg, y + 30], radius=6, fill=TENUE, outline=BORDO, width=1)
    cx = x + 12
    for t, w in zip(intestazioni, larghezze):
        dr.text((cx, y + 8), t, font=fnt(F_BLD, 13), fill=INK)
        cx += w
    yy = y + 30
    for i, riga in enumerate(righe):
        if i % 2:
            dr.rectangle([x, yy, x + larg, yy + alt], fill='#fafbfc')
        dr.line([(x, yy + alt), (x + larg, yy + alt)], fill='#e8eaee')
        cx = x + 12
        for val, w in zip(riga, larghezze):
            if isinstance(val, tuple):           # (testo, colore) = badge
                testo, colore = val
                bw = int(dr.textlength(testo, font=fnt(F_BLD, 11))) + 22
                dr.rounded_rectangle([cx, yy + 8, cx + bw, yy + alt - 8], radius=9, fill=colore)
                centra(dr, testo, fnt(F_BLD, 11), cx + bw / 2, yy + 11, 'white')
            else:
                dr.text((cx, yy + 10), str(val), font=fnt(F_REG, 13), fill=INK)
            cx += w
        yy += alt
    return yy + 10


def pannello(dr, x, y, larg, alt, titolo):
    dr.rounded_rectangle([x, y, x + larg, y + alt], radius=8, outline=BORDO, width=2,
                         fill='#fcfdfe')
    dr.text((x + 16, y + 14), titolo, font=fnt(F_BLD, 15), fill=INK)
    return y + 44


def bottoni(dr, x, y, voci):
    for testo, colore in voci:
        w = int(dr.textlength(testo, font=fnt(F_BLD, 13))) + 30
        dr.rounded_rectangle([x, y, x + w, y + 30], radius=6, outline=colore, width=2)
        dr.text((x + 15, y + 8), testo, font=fnt(F_BLD, 13), fill=colore)
        x += w + 12
    return y + 42


def righe(dr, x, y, testi, font=None, colore=None, passo=19):
    for t in testi:
        dr.text((x, y), t, font=font or fnt(F_REG, 13), fill=colore or MUTED)
        y += passo
    return y


# ────────────────────────────────────────────────────────── le schermate
def supervisione(dest):
    im, dr = finestra(1180, 680, 'SIPO · Integrazione ANSC — Supervisione atti',
                      'Ruolo: USC / Supporto')
    y = testata(dr, 26, 62, 'Supervisione atti',
                'atti che non si sono conclusi nel flusso ordinario — eccezioni da lavorare. Il '
                'back-office diagnostica e riconcilia (letture); le scritture avvengono in '
                '«Finalizza».')
    y = filtri(dr, 26, y, ['Municipio', 'Ufficiale', 'Categoria', 'Fase', 'Stato ANSC',
                           'Atto / idAnsc'])
    y = chip(dr, 26, y, [(5, 'Da riprendere', GIALLO), (2, 'Indeterminati', VIOLA),
                         (3, 'Scartati', ROSSO), (1, 'UC ambiguo', BLU),
                         (2, 'Valore non traducibile', ROSSO), (1, 'In emergenza', VERDE)])
    tabella(dr, 26, y, 660,
            ['Atto', 'Fase', 'Stato ANSC', 'Problema', 'Uff.'],
            [70, 130, 140, 230, 70],
            [['88044', 'VALIDATO', ('CONFERMATO', GIALLO), 'OTP scaduto in firma', 'Rossi'],
             ['88051', 'VALIDATO', ('FIRM. DICHIAR.', VIOLA), 'Firma USC: provider giù', 'Rossi'],
             ['88060', 'VALIDATO', ('—', '#9aa3af'), 'Timeout R009 → riconcilia', 'Verdi'],
             ['88072', 'PREVALIDATO', ('IN_PREPARAZ.', '#9aa3af'), 'R009: campo assente',
              'Bianchi'],
             ['88079', 'UC_DETERMIN.', ('IN_PREPARAZ.', '#9aa3af'), 'UC ambiguo: 2 candidati',
              'Rossi'],
             ['88085', 'PREVALIDATO', ('IN_PREPARAZ.', '#9aa3af'),
              'Valore SIPO senza corrisp.', 'Verdi']])

    yy = pannello(dr, 706, y, 448, 430, 'Dettaglio · atto 88044')
    yy = righe(dr, 722, yy, ['MORTE / CREAZIONE · Rossi Mario · municipio II'])
    dr.text((722, yy + 4), 'Stato reale in ANSC (R005): CONFERMATO', font=fnt(F_BLD, 13),
            fill=GIALLO)
    yy = righe(dr, 722, yy + 26,
               ['idAnsc 2026-…-04 · numero comunale 1188/2026',
                'UC 2101 · logica NASC_VIVO · origine AUTOMATICA',
                'baseline v12 · fase VALIDATO'])
    dr.text((722, yy + 8), 'Timeline (audit)', font=fnt(F_BLD, 14), fill=INK)
    yy += 32
    for fase, esito, ora, col in [('DETERMINAZIONE', 'OK', '10.06.55', VERDE),
                                  ('PREVERIFICA', 'OK', '10.06.58', VERDE),
                                  ('ALLEGATI (R001)', 'OK', '10.07.01', VERDE),
                                  ('SOGGETTO (R005)', 'OK', '10.07.02', VERDE),
                                  ('PAYLOAD', 'OK', '10.07.02', VERDE),
                                  ('DEPOSITO (R009)', 'OK', '10.07.03', VERDE),
                                  ('FIRMA_USC (R007)', 'KO 406002 «OTP scaduto»', '10.11.40',
                                   ROSSO)]:
        dr.ellipse([724, yy + 5, 731, yy + 12], fill=MUTED)
        dr.text((740, yy), fase, font=fnt(F_REG, 13), fill=INK)
        dr.text((900, yy), esito, font=fnt(F_REG, 13), fill=col)
        dr.text((1096, yy), ora, font=fnt(F_REG, 12), fill=MUTED)
        yy += 22
    yy = bottoni(dr, 722, yy + 12, [('Riconcilia (R005)', VIOLA),
                                    ('Apri in «Finalizza» (USC)', BLU)])
    yy = bottoni(dr, 722, yy - 8, [('Registro di emergenza', '#6b7280'),
                                   ('Annulla la bozza (R011)', ROSSO)])
    righe(dr, 722, yy, ['Letture e diagnosi dal back-office. Deposito, firma e annullamento',
                        'sono scritture: avvengono in «Finalizza», nella sessione dell’USC.'],
          font=fnt(F_ITA, 12))
    im.save(dest)
    return dest


def config_uc(dest):
    im, dr = finestra(1180, 540, 'SIPO · Integrazione ANSC — Configurazione · Casi d’uso',
                      'Ruolo: Amministratore')
    y = testata(dr, 26, 62, 'Configurazione — Casi d’uso',
                'una riga per UC adottato: a quale Modello si applica, con quale priorità e con '
                'quale logica di scelta. La logica si prende dal catalogo, non si riscrive qui.')
    y = filtri(dr, 26, y, ['Baseline: v12 (ATTIVA)', 'Tipo evento', 'Modello', 'Validità'])
    y = tabella(dr, 26, y, 1128,
                ['UC', 'Descrizione', 'Modello / tipo atto', 'Prior.', 'Logica di scelta',
                 'Stato', 'Validità', ''],
                [80, 280, 190, 70, 190, 90, 150, 90],
                [['2101', 'Morte in abitazione a Roma', '01 · 301', '1', '—',
                  ('ATTIVO', VERDE), 'dal 01/01/2026', 'apri »'],
                 ['2102', 'Morte in struttura sanitaria', '03 · 303', '1', '—',
                  ('ATTIVO', VERDE), 'dal 01/01/2026', 'apri »'],
                 ['11111000', 'Dichiarazione entro 10 gg', '30 · 1515', '1', 'NASC_VIVO',
                  ('ATTIVO', VERDE), 'dal 01/01/2026', 'apri »'],
                 ['11111100', 'Dichiarazione — nato morto', '30 · 1515', '2', 'NASC_MORTO',
                  ('ATTIVO', VERDE), 'dal 01/01/2026', 'apri »'],
                 ['11111200', 'Nato vivo poi deceduto', '30 · 1515', '3', 'NASC_VIMO',
                  ('ATTIVO', VERDE), 'dal 01/01/2026', 'apri »']])
    y = bottoni(dr, 26, y, [('Nuovo UC', BLU), ('Ordina priorità', '#6b7280'),
                            ('Simula su un atto reale', VERDE),
                            ('Apri il catalogo delle logiche', VIOLA)])
    righe(dr, 26, y + 6,
          ['ATTENZIONE: Due righe con lo stesso Modello e la stessa priorità sono una configurazione '
           'ambigua: la simulazione la mostra prima che un atto la incontri allo sportello.',
           'Una riga non si cancella: si chiude la validità. Gli atti già formati devono restare '
           'leggibili con la configurazione in vigore allora.'],
          font=fnt(F_ITA, 13))
    im.save(dest)
    return dest


def config_campi(dest):
    im, dr = finestra(1180, 580,
                      'SIPO · Integrazione ANSC — Configurazione · UC 11111000',
                      'Ruolo: Amministratore')
    y = testata(dr, 26, 62, 'Sezioni, campi, allegati e formule dell’UC',
                'quattro schede per un solo UC: le sezioni dicono quali blocchi si popolano, i '
                'campi da dove viene ogni dato, gli allegati quali documenti servono, le formule '
                'quali diciture sono previste.')
    for i, (testo, attiva) in enumerate([('Sezioni (11)', False), ('Campi (199)', True),
                                         ('Allegati (5)', False), ('Formule (8)', False)]):
        x = 26 + i * 150
        colore = BLU if attiva else BORDO
        dr.rounded_rectangle([x, y, x + 140, y + 32], radius=6, outline=colore,
                             width=3 if attiva else 2)
        centra(dr, testo, fnt(F_BLD if attiva else F_REG, 13), x + 70, y + 9,
               BLU if attiva else MUTED)
    y += 46
    y = filtri(dr, 26, y, ['Sezione: Madre', 'Solo obbligatori', 'Senza corrispondenza SIPO'])
    y = tabella(dr, 26, y, 1128,
                ['Oggetto · campo ANSC', 'Obbl.', 'Schema · tabella · colonna SIPO',
                 'Decodifica', 'Logica del campo', 'Operativo', 'Ord.'],
                [290, 70, 320, 120, 180, 100, 60],
                [['evento.madre.cognome', 'NO', 'MATR_USR · SOGGETTO · COGNOME', '—', '—',
                  ('SÌ', VERDE), '12'],
                 ['evento.madre.nome', 'SI', 'MATR_USR · SOGGETTO · NOME', '—', '—',
                  ('SÌ', VERDE), '13'],
                 ['evento.madre.dataNascita', 'SI', 'MATR_USR · SOGGETTO · DATA_NASCITA', '—',
                  'DATA_COMPLETA', ('SÌ', VERDE), '14'],
                 ['evento.madre.idstatocivile', 'SI', 'MATR_USR · SOGGETTO · DETTAGLIO_SC',
                  'ANSC_61', 'riconciliazione »', ('SÌ', VERDE), '15'],
                 ['evento.madre.idANPR', 'NO', '— (assente in SIPO)', '—', '—',
                  ('NO', '#9aa3af'), '16']])
    y = bottoni(dr, 26, y, [('Precompila dal foglio', BLU),
                            ('Apri la riconciliazione dei valori', VIOLA),
                            ('Simula la costruzione del payload', VERDE)])
    righe(dr, 26, y + 6,
          ['La colonna «Logica del campo» richiama il catalogo (dominio 3): la trasformazione si '
           'scrive una volta e vale per tutti i campi che la citano.',
           'ATTENZIONE: Un campo con decodifica ANSC e senza riconciliazione dei valori supera la '
           'configurazione ma non la costruzione del payload: il pre-filtro lo segnala.'],
          font=fnt(F_ITA, 13))
    im.save(dest)
    return dest


def riconciliazione(dest):
    im, dr = finestra(1180, 520,
                      'SIPO · Integrazione ANSC — Riconciliazione dei valori',
                      'Ruolo: Amministratore')
    y = testata(dr, 26, 62, 'Riconciliazione dei valori fra SIPO e ANSC',
                'per ogni decodifica ANSC, che cosa diventa un valore di SIPO. I dizionari dicono '
                'quali valori ANSC ammette; qui si dichiara la corrispondenza, con la sua '
                'validità.')
    y = filtri(dr, 26, y, ['Decodifica: ANSC_61', 'Tabella SIPO: CONF_STATO_CIVILE',
                           'Solo da completare'])
    y = tabella(dr, 26, y, 1128,
                ['Valore SIPO', 'Descrizione SIPO', '→', 'Valore ANSC', 'Descrizione ANSC',
                 'Condizione', 'Validità'],
                [110, 270, 40, 110, 250, 170, 178],
                [['1', 'Celibe / nubile', '→', '1', 'CELIBE/NUBILE', '—', 'dal 01/01/2026'],
                 ['2', 'Coniugato/a', '→', '2', 'CONIUGATO/A', '—', 'dal 01/01/2026'],
                 ['3', 'Vedovo/a', '→', '3', 'VEDOVO/A', '—', 'dal 01/01/2026'],
                 ['4', 'Divorziato/a', '→', ('da definire', ROSSO), '—', '—', '—'],
                 ['9', 'Non dichiarato', '→', ('da definire', ROSSO), '—',
                  'solo se idANPR assente', '—']])
    y = bottoni(dr, 26, y, [('Nuova corrispondenza', BLU),
                            ('Apri la decodifica ANSC (valori validi)', VIOLA),
                            ('Apri la tabella SIPO', '#6b7280'),
                            ('Chiudi validità', GIALLO)])
    righe(dr, 26, y + 6,
          ['Il raccordo si costruisce per coppie: la decodifica di ANSC da una parte, la tabella '
           'di configurazione di SIPO dall’altra. Delle 30 decodifiche in elenco, quattro '
           'dichiarano già la tabella SIPO.',
           'ATTENZIONE: Una corrispondenza non si riscrive: si chiude e se ne apre una nuova, perché gli '
           'atti formati vanno riletti con la corrispondenza in vigore allora.'],
          font=fnt(F_ITA, 13))
    im.save(dest)
    return dest


def comandi(dest):
    im, dr = finestra(1180, 560, 'SIPO · Integrazione ANSC — Comandi ed esecuzioni',
                      'Ruolo: Amministratore')
    y = testata(dr, 26, 62, 'Comandi ed esecuzioni',
                'ogni comando è disponibile dal back-office e da riga di comando: stessa '
                'implementazione, stessi controlli, stessa traccia. La riga di comando serve le '
                'finestre di manutenzione e i casi in cui l’interfaccia non è raggiungibile.')
    y = tabella(dr, 26, y, 1128,
                ['Comando', 'Che cosa fa', 'Equivalente da riga di comando', 'Ultima esecuzione'],
                [250, 330, 330, 218],
                [['Allinea i dizionari', 'R901: elenco, dettaglio, carico',
                  'ansc dizionari allinea --modo COMPLETO', '24/09 09.12 · OK · 3 aggiornate'],
                 ['Simula l’allineamento', 'mostra il differenziale, non scrive',
                  'ansc dizionari allinea --modo SIMULAZIONE', '24/09 09.05 · OK'],
                 ['Importa la configurazione', 'legge il foglio, prepara le righe PROPOSTE',
                  'ansc configurazione importa --file <xlsx>', '23/09 17.40 · OK · 2.939 righe'],
                 ['Attiva una baseline', 'porta una bozza in ATTIVA',
                  'ansc baseline attiva --cod v12', '22/09 11.03 · OK'],
                 ['Scarica le notifiche', 'R008: aggiorna lo store locale',
                  'ansc notifiche scarica', '24/09 08.00 · OK · 41 nuove'],
                 ['Riconcilia un atto', 'R005: accerta lo stato reale',
                  'ansc atto riconcilia --id 88060', '24/09 10.22 · OK']])
    y = bottoni(dr, 26, y, [('Esegui', BLU), ('Storico delle esecuzioni', '#6b7280'),
                            ('Scarica il registro', '#6b7280')])
    righe(dr, 26, y + 6,
          ['Tre regole valgono per entrambe le vie. L’esecuzione è sempre attribuita a una '
           'persona, anche da riga di comando: un comando senza operatore non è tracciabile.',
           'Ogni esecuzione lascia una riga nell’audit, con il proprio esito e i propri conteggi.',
           'ATTENZIONE: I comandi che contattano ANSC entro una sessione OTP non sono eseguibili da riga '
           'di comando finché OP-23 resta aperto: senza operatore presente non c’è sessione.'],
          font=fnt(F_ITA, 13))
    im.save(dest)
    return dest


def ricerca(dest):
    im, dr = finestra(1180, 560, 'SIPO · Integrazione ANSC — Ricerca e tracciabilità',
                      'Ruolo: tutti')
    y = testata(dr, 26, 62, 'Ricerca e tracciabilità',
                'un atto si ritrova per chiave SIPO, per identificativo nazionale, per numero '
                'comunale o per soggetto; la scheda mostra il percorso end-to-end.')
    y = filtri(dr, 26, y, ['Atto SIPO', 'idAnsc', 'Numero comunale', 'Soggetto', 'Periodo'])
    y = tabella(dr, 26, y, 1128,
                ['Atto', 'Evento', 'UC', 'idAnsc', 'N. comunale', 'Fase', 'Stato ANSC'],
                [90, 130, 120, 230, 150, 180, 220],
                [['88044', 'MORTE', '2101', '2026-9423-26624-058091', '1188/2026', 'FIRMATO',
                  ('FIRMATO USC', VERDE)],
                 ['88060', 'MORTE', '2101', '—', '1190/2026', 'VALIDATO', ('—', '#9aa3af')],
                 ['90112', 'NASCITA', '11111000', '2026-9423-27001-058091', '204/2026',
                  'FIRMATO', ('FIRMATO USC', VERDE)]])
    yy = pannello(dr, 26, y, 1128, 210, 'Percorso dell’atto 88044')
    passi = [('Determinazione', 'UC 2101 · NASC_VIVO', VERDE),
             ('Prevalidazione', 'nessuna mancanza', VERDE),
             ('Documenti', '2 su 2 · Inserito', VERDE),
             ('Soggetto', 'R005 · trovato', VERDE),
             ('Payload', 'baseline v12', VERDE),
             ('Deposito', 'R009 · idAnsc', VERDE),
             ('Firme', 'R006 · R007', VERDE)]
    x = 44
    for nome, nota, col in passi:
        dr.rounded_rectangle([x, yy, x + 142, yy + 62], radius=8, outline=col, width=2)
        centra(dr, nome, fnt(F_BLD, 12), x + 71, yy + 12, INK)
        for i, rg in enumerate(avvolgi(dr, nota, fnt(F_REG, 11), 126)):
            centra(dr, rg, fnt(F_REG, 11), x + 71, yy + 32 + i * 14, MUTED)
        if nome != 'Firme':
            dr.line([(x + 146, yy + 31), (x + 154, yy + 31)], fill=MUTED, width=2)
        x += 158
    righe(dr, 44, yy + 84,
          ['La stessa scheda serve la diagnosi e il supporto a Sogei: per ogni passo restano '
           'fase, esito e messaggio restituito da ANSC.',
           'ATTENZIONE: La ricerca per identificativo nazionale e per numero comunale oggi non esiste in '
           'SIPO: è una delle interfacce da costruire (OP-29, OP-30).'],
          font=fnt(F_ITA, 13))
    im.save(dest)
    return dest


def audit(dest):
    im, dr = finestra(1180, 560, 'SIPO · Integrazione ANSC — Audit e log', 'Ruolo: Auditor / Supporto')
    y = testata(dr, 26, 62, 'Audit e log',
                'ogni passo del percorso lascia una riga: non solo le chiamate verso ANSC, ma '
                'anche le decisioni prese in locale, che sono ciò che spiega il payload.')
    y = filtri(dr, 26, y, ['Atto', 'Fase', 'Esito', 'Operatore', 'Periodo'])
    y = tabella(dr, 26, y, 1128,
                ['Data', 'Atto', 'Fase', 'Esito', 'Durata (ms)', 'Operatore',
                 'Dalla risposta'],
                [150, 90, 200, 120, 90, 140, 338],
                [['24/09 10.06.55', '88044', 'DETERMINAZIONE', ('OK', VERDE), '12 ms', 'rossi',
                  'UC 2101 · logica NASC_VIVO'],
                 ['24/09 10.06.58', '88044', 'PREVERIFICA', ('OK', VERDE), '40 ms', 'rossi',
                  'nessuna mancanza'],
                 ['24/09 10.07.01', '88044', 'ALLEGATI', ('OK', VERDE), '820 ms', 'rossi',
                  'R001 · 2 allegati · stato Inserito'],
                 ['24/09 10.07.02', '88044', 'PAYLOAD', ('OK', VERDE), '35 ms', 'rossi',
                  'baseline v12 · 199 campi'],
                 ['24/09 10.07.03', '88044', 'DEPOSITO', ('OK', VERDE), '1,2 s', 'rossi',
                  'R009 · idAnsc 2026-…-04'],
                 ['24/09 10.11.40', '88044', 'FIRMA_USC', ('KO', ROSSO), '0,9 s', 'rossi',
                  '406002 «OTP scaduto»']])
    y = bottoni(dr, 26, y, [('Apri richiesta / risposta', BLU), ('Esporta', '#6b7280')])
    righe(dr, 26, y + 6,
          ['Le fasi sono quelle del flusso operativo: DETERMINAZIONE, PREVERIFICA, ALLEGATI, '
           'SOGGETTO, PAYLOAD, ANTEPRIMA, DEPOSITO, FIRMA_DICH, FIRMA_USC, ANNULLAMENTO, '
           'RICONCILIAZIONE.',
           'ATTENZIONE: L’audit conserva richiesta e risposta, quindi dati particolari: è soggetto a '
           'minimizzazione e a purga. Il payload del deposito resta sull’atto, che alla purga '
           'sopravvive.'],
          font=fnt(F_ITA, 13))
    im.save(dest)
    return dest


SCHERMATE = [(supervisione, 'bo_supervisione.png'), (config_uc, 'bo_config_uc.png'),
             (config_campi, 'bo_config_campi.png'), (riconciliazione, 'bo_riconciliazione.png'),
             (comandi, 'bo_comandi.png'), (ricerca, 'bo_ricerca.png'), (audit, 'bo_audit.png')]

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'img')
    os.makedirs(out, exist_ok=True)
    for f, nome in SCHERMATE:
        print('scritto:', f(os.path.join(out, nome)))
