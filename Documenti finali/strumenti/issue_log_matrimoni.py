# -*- coding: utf-8 -*-
"""Issue log da compilare per l'area Matrimoni (SIPO e integrazione ANSC).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/issue_log_matrimoni.py [uscita.xlsx]
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(QUI), 'ISSUE-LOG_Matrimoni_SIPO-ANSC_v0.1.xlsx')
RIGHE = 200          # righe predisposte (ID MAT-001 … MAT-200)

BORDO = Border(*(Side(style='thin', color='BFBFBF'),) * 4)
TESTA = PatternFill('solid', fgColor='8C0029')
GRUPPO = {'Identificazione': 'F2DCDB', 'Contesto': 'DDEBF7', 'Descrizione': 'FFF2CC',
          'Valutazione': 'FCE4D6', 'Lavorazione': 'E2EFDA', 'Verifica': 'EDEDED'}

LISTE = {
    'Ambiente': ['Sviluppo', 'Collaudo', 'Preproduzione ANSC', 'Produzione'],
    'Area': ['Pubblicazioni di matrimonio', 'Matrimonio civile', 'Matrimonio concordatario',
             'Matrimonio acattolico', 'Matrimonio in imminente pericolo di vita',
             'Matrimonio per procura', 'Trascrizione matrimonio dall’estero',
             'Trascrizione sentenze / provvedimenti', 'Separazione e divorzio (accordi)',
             'Riconciliazione', 'Convenzioni matrimoniali / regime patrimoniale',
             'Annotazioni', 'Agenda delle celebrazioni', 'Testimoni e firmatari',
             'Allegati e documenti', 'Stampe e anteprima', 'Ricerca e consultazione',
             'Comunicazioni', 'Integrazione ANSC', 'Integrazione ANPR', 'Altro'],
    'Tipo': ['Errore', 'Anomalia dei dati', 'Requisito mancante', 'Miglioramento',
             'Domanda / chiarimento', 'Documentazione'],
    'Componente': ['Front-end (maschera)', 'Back-end (servizio)', 'Base dati', 'Stampa Jasper',
                   'Concentratore ANSC', 'Servizio ANSC', 'Servizio ANPR', 'Configurazione',
                   'Da individuare'],
    'SN': ['S', 'N'],
    'Gravità': ['Critica', 'Alta', 'Media', 'Bassa'],
    'Priorità': ['P1 - Immediata', 'P2 - Alta', 'P3 - Normale', 'P4 - Bassa'],
    'Frequenza': ['Sempre', 'Spesso', 'A volte', 'Una sola volta'],
    'Stato': ['Aperta', 'In analisi', 'In lavorazione', 'Risolta - da verificare', 'Chiusa',
              'Riaperta', 'Respinta', 'Duplicata', 'Sospesa'],
}

# (gruppo, intestazione, larghezza, lista, nota)
COLONNE = [
    ('Identificazione', 'ID', 10, None, 'Progressivo già assegnato: non modificarlo.'),
    ('Identificazione', 'Data rilevazione', 13, 'data', 'gg/mm/aaaa'),
    ('Identificazione', 'Rilevata da', 18, None, 'Nome o gruppo di chi segnala.'),
    ('Contesto', 'Ambiente', 16, 'Ambiente', None),
    ('Contesto', 'Area', 28, 'Area', None),
    ('Contesto', 'Schermata / funzione', 26, None, 'Nome della maschera o voce di menu, '
                                                   'es. «Creazione atto – parte 2».'),
    ('Contesto', 'Tipo atto / Modello', 18, None, 'ID_CONF_TIPO_ATTO e/o Modello, se noti.'),
    ('Contesto', 'UC ANSC', 13, None, 'Codice del caso d’uso, se l’issue riguarda ANSC.'),
    ('Contesto', 'Riferimento pratica / atto', 20, None,
     'Numero pratica, numero/anno atto o idAnsc. NON nomi né codici fiscali.'),
    ('Descrizione', 'Titolo', 34, None, 'Una riga che descrive il problema.'),
    ('Descrizione', 'Descrizione', 50, None, None),
    ('Descrizione', 'Passi per riprodurre', 45, None, '1. … 2. … 3. …'),
    ('Descrizione', 'Risultato atteso', 35, None, None),
    ('Descrizione', 'Risultato ottenuto', 35, None, None),
    ('Descrizione', 'Messaggio / codice di errore', 30, None,
     'Testo esatto del messaggio, codice HTTP o codice ANSC (es. 400001).'),
    ('Descrizione', 'Immagine', 45, None,
     'Schermata della maschera. In Excel 365: Inserisci › Immagini › Inserisci nella cella.'),
    ('Descrizione', 'Altri allegati (nome file)', 24, None,
     'Es. MAT-001_1.png, MAT-001_log.txt nella cartella dell’issue log.'),
    ('Valutazione', 'Bloccante (S/N)', 11, 'SN', 'S = impedisce di completare la pratica o l’atto.'),
    ('Valutazione', 'Gravità', 11, 'Gravità', None),
    ('Valutazione', 'Priorità', 15, 'Priorità', None),
    ('Valutazione', 'Frequenza', 14, 'Frequenza', None),
    ('Valutazione', 'Esiste un aggiramento (S/N)', 13, 'SN', None),
    ('Valutazione', 'Aggiramento', 30, None, 'Come si prosegue nel frattempo.'),
    ('Valutazione', 'Tipo', 20, 'Tipo', None),
    ('Lavorazione', 'Componente', 20, 'Componente', None),
    ('Lavorazione', 'Stato', 20, 'Stato', None),
    ('Lavorazione', 'Assegnata a', 18, None, None),
    ('Lavorazione', 'Data presa in carico', 13, 'data', None),
    ('Lavorazione', 'Analisi / causa', 40, None, None),
    ('Lavorazione', 'Soluzione adottata', 40, None, None),
    ('Lavorazione', 'Rilascio / versione', 15, None, None),
    ('Lavorazione', 'Data risoluzione', 13, 'data', None),
    ('Verifica', 'Verificata da', 18, None, None),
    ('Verifica', 'Data verifica', 13, 'data', None),
    ('Verifica', 'Esito verifica', 16, None, 'OK / KO, con nota.'),
    ('Verifica', 'Riferimenti (OP, ticket, issue ANSC)', 26, None, None),
    ('Verifica', 'Note', 35, None, None),
]
IDX = {c[1]: i + 1 for i, c in enumerate(COLONNE)}


def lettera(nome):
    return get_column_letter(IDX[nome])


wb = Workbook()

# ------------------------------------------------------------------ Issue log
ws = wb.active
ws.title = 'Issue log'
ws.sheet_view.zoomScale = 90
for i, (gruppo, nome, larg, _, _) in enumerate(COLONNE, 1):
    ws.column_dimensions[get_column_letter(i)].width = larg
# riga 1: gruppi
inizio = 1
for i in range(1, len(COLONNE) + 2):
    if i > len(COLONNE) or COLONNE[i - 1][0] != COLONNE[inizio - 1][0]:
        g = COLONNE[inizio - 1][0]
        ws.merge_cells(start_row=1, start_column=inizio, end_row=1, end_column=i - 1)
        c = ws.cell(1, inizio, g.upper())
        c.font = Font(bold=True, color='404040', size=9)
        c.alignment = Alignment(horizontal='center')
        for k in range(inizio, i):
            ws.cell(1, k).fill = PatternFill('solid', fgColor=GRUPPO[g])
        inizio = i
# riga 2: intestazioni
for i, (_, nome, _, _, nota) in enumerate(COLONNE, 1):
    c = ws.cell(2, i, nome)
    c.font = Font(bold=True, color='FFFFFF')
    c.fill = TESTA
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    c.border = BORDO
    if nota:
        from openpyxl.comments import Comment
        c.comment = Comment(nota, 'Issue log')
ws.row_dimensions[2].height = 42
ws.freeze_panes = ws.cell(3, IDX['Titolo'])

for r in range(3, RIGHE + 3):
    ws.row_dimensions[r].height = 90
    for i, (_, nome, _, lista, _) in enumerate(COLONNE, 1):
        c = ws.cell(r, i)
        c.border = BORDO
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if lista == 'data':
            c.number_format = 'DD/MM/YYYY'
    ws.cell(r, 1, 'MAT-%03d' % (r - 2)).font = Font(bold=True)
ultima = RIGHE + 2
ws.auto_filter.ref = 'A2:%s%d' % (get_column_letter(len(COLONNE)), ultima)

# ------------------------------------------------------------------ Liste (nascosto)
wl = wb.create_sheet('Liste')
for j, (chiave, valori) in enumerate(LISTE.items(), 1):
    wl.cell(1, j, chiave).font = Font(bold=True)
    for k, v in enumerate(valori, 2):
        wl.cell(k, j, v)
    rif = "Liste!$%s$2:$%s$%d" % (get_column_letter(j), get_column_letter(j), len(valori) + 1)
    for _, nome, _, lista, _ in COLONNE:
        if lista == chiave:
            dv = DataValidation(type='list', formula1='=' + rif, allow_blank=True,
                                showErrorMessage=True, errorTitle='Valore non ammesso',
                                error='Scegliere un valore dall’elenco.')
            ws.add_data_validation(dv)
            dv.add('%s3:%s%d' % (lettera(nome), lettera(nome), ultima))
for _, nome, _, lista, _ in COLONNE:
    if lista == 'data':
        dv = DataValidation(type='date', operator='greaterThan', formula1='DATE(2020,1,1)',
                            allow_blank=True, showErrorMessage=True,
                            error='Inserire una data (gg/mm/aaaa).')
        ws.add_data_validation(dv)
        dv.add('%s3:%s%d' % (lettera(nome), lettera(nome), ultima))
wl.sheet_state = 'hidden'

# ------------------------------------------------------------------ evidenze
rng = 'A3:%s%d' % (get_column_letter(len(COLONNE)), ultima)
b, s = lettera('Bloccante (S/N)'), lettera('Stato')
ws.conditional_formatting.add(rng, FormulaRule(
    formula=['AND($%s3="S",$%s3<>"Chiusa",$%s3<>"Respinta",$%s3<>"Duplicata")' % (b, s, s, s)],
    fill=PatternFill('solid', fgColor='F8CBAD')))
ws.conditional_formatting.add(rng, FormulaRule(
    formula=['OR($%s3="Chiusa",$%s3="Respinta",$%s3="Duplicata")' % (s, s, s)],
    font=Font(color='808080')))

# ------------------------------------------------------------------ Riepilogo
wr = wb.create_sheet('Riepilogo', 0)
wr.column_dimensions['A'].width = 30
for col in 'BCDEFGHIJ':
    wr.column_dimensions[col].width = 13
wr['A1'] = 'Issue log Matrimoni – riepilogo'
wr['A1'].font = Font(bold=True, size=14, color='8C0029')
wr['A2'] = 'Si aggiorna da solo: conta le righe del foglio «Issue log» che hanno un titolo.'
wr['A2'].font = Font(italic=True, color='808080')

T = "'Issue log'!$%s$3:$%s$%d" % (lettera('Titolo'), lettera('Titolo'), ultima)


def col(nome):
    return "'Issue log'!$%s$3:$%s$%d" % (lettera(nome), lettera(nome), ultima)


def intesta(riga, testi):
    for j, t in enumerate(testi, 1):
        c = wr.cell(riga, j, t)
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = TESTA
        c.border = BORDO
        c.alignment = Alignment(horizontal='center', wrap_text=True)


r = 4
wr.cell(r, 1, 'Issue registrate').font = Font(bold=True)
wr.cell(r, 2, '=COUNTIF(%s,"?*")' % T)
wr.cell(r + 1, 1, 'Bloccanti ancora aperte').font = Font(bold=True, color='C00000')
wr.cell(r + 1, 2, '=COUNTIFS(%s,"?*",%s,"S")-SUMPRODUCT(COUNTIFS(%s,"?*",%s,"S",%s,'
                  '{"Chiusa","Respinta","Duplicata"}))'
        % (T, col('Bloccante (S/N)'), T, col('Bloccante (S/N)'), col('Stato')))

r = 8
intesta(r, ['Stato', 'Bloccanti', 'Non bloccanti', 'Totale'])
for k, st in enumerate(LISTE['Stato'], r + 1):
    wr.cell(k, 1, st)
    wr.cell(k, 2, '=COUNTIFS(%s,"?*",%s,A%d,%s,"S")' % (T, col('Stato'), k, col('Bloccante (S/N)')))
    wr.cell(k, 3, '=COUNTIFS(%s,"?*",%s,A%d,%s,"N")' % (T, col('Stato'), k, col('Bloccante (S/N)')))
    wr.cell(k, 4, '=COUNTIFS(%s,"?*",%s,A%d)' % (T, col('Stato'), k))
k += 1
wr.cell(k, 1, 'Stato non indicato')
wr.cell(k, 4, '=COUNTIFS(%s,"?*",%s,"")' % (T, col('Stato')))

r = k + 3
intesta(r, ['Area'] + LISTE['Gravità'] + ['Non indicata', 'Totale', 'di cui bloccanti'])
for k, ar in enumerate(LISTE['Area'], r + 1):
    wr.cell(k, 1, ar)
    for j, g in enumerate(LISTE['Gravità'], 2):
        wr.cell(k, j, '=COUNTIFS(%s,"?*",%s,$A%d,%s,"%s")' % (T, col('Area'), k, col('Gravità'), g))
    wr.cell(k, 6, '=COUNTIFS(%s,"?*",%s,$A%d,%s,"")' % (T, col('Area'), k, col('Gravità')))
    wr.cell(k, 7, '=COUNTIFS(%s,"?*",%s,$A%d)' % (T, col('Area'), k))
    wr.cell(k, 8, '=COUNTIFS(%s,"?*",%s,$A%d,%s,"S")' % (T, col('Area'), k, col('Bloccante (S/N)')))

r = k + 3
intesta(r, ['Componente', 'Aperte*', 'Totale'])
for k, co in enumerate(LISTE['Componente'], r + 1):
    wr.cell(k, 1, co)
    wr.cell(k, 2, '=COUNTIFS(%s,"?*",%s,A%d)-SUMPRODUCT(COUNTIFS(%s,"?*",%s,A%d,%s,'
                  '{"Chiusa","Respinta","Duplicata"}))'
            % (T, col('Componente'), k, T, col('Componente'), k, col('Stato')))
    wr.cell(k, 3, '=COUNTIFS(%s,"?*",%s,A%d)' % (T, col('Componente'), k))
wr.cell(k + 1, 1, '* escluse Chiusa, Respinta e Duplicata').font = Font(italic=True, color='808080')
for row in wr.iter_rows(min_row=8, max_row=k):
    for c in row:
        if c.value is not None and c.row > 8:
            c.border = BORDO

# ------------------------------------------------------------------ Istruzioni
wi = wb.create_sheet('Istruzioni', 1)
wi.column_dimensions['A'].width = 26
wi.column_dimensions['B'].width = 95
wi['A1'] = 'Come compilare l’issue log'
wi['A1'].font = Font(bold=True, size=14, color='8C0029')
REGOLE = [
    ('Una riga, una issue', 'Ogni problema ha la sua riga e il suo ID (MAT-001, MAT-002…), già '
     'assegnato. Se due segnalazioni descrivono lo stesso problema, la seconda va in stato '
     '«Duplicata» con il riferimento alla prima nella colonna «Riferimenti».'),
    ('Campi minimi', 'Data rilevazione, Rilevata da, Area, Schermata, Titolo, Descrizione, '
     'Risultato atteso e ottenuto, Bloccante (S/N). Il resto si completa in lavorazione.'),
    ('Bloccante = S', 'Quando la issue impedisce di completare la pratica o di formare l’atto '
     '(anche verso ANSC) e non esiste un aggiramento accettabile. Le bloccanti non chiuse si '
     'colorano di rosso.'),
    ('Gravità', 'Critica: perdita o alterazione di dati, atto formato in modo errato. Alta: '
     'funzione non utilizzabile. Media: funzione utilizzabile con difficoltà. Bassa: estetica, '
     'testi, comodità.'),
    ('Immagini', 'Excel 365: selezionare la cella della colonna «Immagine», poi Inserisci › '
     'Immagini › Inserisci nella cella (l’immagine segue la riga quando si filtra o si '
     'ordina). Con versioni precedenti, salvare il file come MAT-nnn_k.png nella stessa cartella '
     'e scriverne il nome in «Altri allegati».'),
    ('Dati personali', 'Prima di inserire una schermata coprire nomi, cognomi e codici fiscali '
     'dei soggetti. Nella colonna «Riferimento pratica / atto» indicare solo numero di pratica, '
     'numero/anno dell’atto o idAnsc.'),
    ('Errori ANSC', 'Riportare il messaggio esatto e, se visibile, il codice di errore (es. '
     '400001, 50002) e l’UC ANSC usato: senza questi dati la issue non è analizzabile.'),
    ('Ciclo di vita', 'Aperta → In analisi → In lavorazione → Risolta - da verificare → Chiusa '
     '(dopo esito OK di chi l’ha segnalata). Se la verifica fallisce: Riaperta.'),
    ('Riepilogo', 'Il foglio «Riepilogo» si aggiorna da solo; conta solo le righe con un titolo.'),
]
for k, (a, b_) in enumerate(REGOLE, 3):
    wi.cell(k, 1, a).font = Font(bold=True)
    wi.cell(k, 2, b_).alignment = Alignment(wrap_text=True, vertical='top')
    wi.cell(k, 1).alignment = Alignment(vertical='top')
    wi.row_dimensions[k].height = 48

wb.active = 2
wb.save(OUT)
print('scritto', OUT, '-', len(COLONNE), 'colonne,', RIGHE, 'righe predisposte')
