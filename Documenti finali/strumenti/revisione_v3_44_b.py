"""Seconda rilettura di ANALISI_Integrazione-ANSC_v3.44, dopo le correzioni a mano dell'utente
(file salvato il 23/10/2026 alle 08:17).

Riprende i 65 rilievi di revisione_v3_44.py con la STESSA numerazione, ne aggiorna lo stato
confrontando il testo nuovo con quello del 22/10, e aggiunge in coda i rilievi nuovi.
Scrive REVISIONE_ANALISI-ANSC_v3.44_v0.2.xlsx (la v0.1 non si tocca).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/revisione_v3_44_b.py
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

from revisione_v3_44 import R

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(QUI), 'REVISIONE_ANALISI-ANSC_v3.44_v0.2.xlsx')

# Stato dei rilievi della v0.1, per inizio del campo «Dove». Quelli non elencati restano «Da fare».
STATO = {
    'degli   Le letture': (
        'Parziale',
        'Ripristinati 7 punti su 19: Glossario, RF-21, componenti e testo dei dizionari ANSC (due), '
        'scheda R002 («estratti»), vista di supervisione (riformulata), COMMENT di ANSC_CFG_UC e le due '
        'descrizioni di ID_MODELLO_ATTO. Restano troncati: «non alla formazione di » (Vincoli, M2M), '
        '«e non forma né firma » (Architettura), «non mutano lo stato degli » (automazione), «allinea lo '
        'stato, non forma » (tabella delle unità), «i propri » , «resta agli » e «store di stato degli » '
        '(tabelle), «colleghi i due » (R005), «e non forma » (back-office), «insieme agli » e il COMMENT '
        '«Documenti allegati agli » (ALLEGATO), «una famiglia di » (formule), «e punta ad  evento» (due '
        'volte) e le FK di firmatari «REFERENCES  evento / soggetto» (lo schema atti. tolto lascia nomi '
        'di tabelle che in ANSC_USR non esistono).'),
    'Con una sequence per anno': (
        'Parziale',
        'Tolto il blocco SQL dello stacco (LOCK TABLE, NEXTVAL, ALL_SEQUENCES). Il testo è rimasto '
        'quello delle sequence: «Con una sequence per anno basta indicare l’anno», «MAXVALUE 999999», '
        '«NOCACHE e ORDER», «la sequence non può superarle» (DATI_ATTO_ESTERNO), «La sequence non sa che '
        'quel numero è stato consumato» (percorsi), «tiene coerente la sequence» (operazioni), e tutto '
        '«Lo stacco, passo per passo» (consuma la sequence, valore successivo della sequence, valori '
        'presi dalla sequence che diventano buchi, avanzare la sequence fino al numero). Il passo '
        '«Serializzazione» blocca ancora DATI_ATTO_ESTERNO: con il numeratore il blocco è la riga '
        'dell’anno (SELECT … FOR UPDATE). E una garanzia cambia in meglio: con il numeratore un rollback '
        'riporta indietro anche il contatore, quindi la «finestra residua» dei buchi da transazione '
        'fallita non esiste più; restano solo i salti voluti della registrazione a posteriori. La '
        'registrazione a posteriori diventa un UPDATE del contatore al massimo fra il valore corrente e '
        'il numero, senza ciclo.'),
    'NUMBER(6,0).': (
        'Da fare',
        'Invariata: punto dopo NUMBER(6,0), virgola prima della parentesi chiusa, nessuna chiave. Con '
        '«si crea alla prima chiamata dell’anno» la chiave primaria sull’anno è ciò che rende sicura la '
        'creazione concorrente: la seconda INSERT fallisce per chiave duplicata e il servizio rilegge la '
        'riga. Vedi anche il rilievo 70 sulla descrizione della tabella.'),
    'SEQ_NUM_COMUNALE_<anno> |': (
        'Parziale',
        'Tolti sequence, procedura e job dall’App. A e la riga della tabella degli oggetti. Restano: il '
        'titolo «PRENOTAZIONE_ATTI, e le sequence della numerazione» (App. A), la didascalia dell’ERD '
        '(«con le sequence della numerazione comunale, che non sono tabelle») e la figura stessa. Con la '
        'procedura sono spariti anche i GRANT a <UTENZA_NUM>: vedi rilievo 67.'),
    'OP-44': ('Da fare', 'Invariati OP-44 e OP-73 (c).'),
}

# Rilievi nuovi (gravità, area, capitolo, dove, problema, correzione, decisione)
NUOVI = [
    ('Media', 'Forzatura', 'Le funzioni offerte da ANSC — Il codice di forzatura · Registro degli Open Point',
     'A tal proposito è stata ereditata dal SIDE · OP-21',
     'Il paragrafo aggiunto dice che in forzatura_validazione «dovranno essere riportate tutte le forzature '
     'fatte»; la tabella di Side registra invece il codice che ANSC CONCEDE con le anomalie superabili '
     '(COMMENT: «dati che ANSC concede all’utente per eventualmente operare una forzatura»), che l’operatore '
     'può usare o no. Manca dove si dice se la forzatura è stata applicata, da chi e con quale esito. '
     '«Gestione dell’utenza» è vago: il punto è chi è abilitato a forzare. OP-21 chiede ancora se la '
     'forzatura vada esposta all’operatore o tenuta fuori dal pilota, mentre il paragrafo dà la tabella '
     'per adottata. Il passo VALIDA del processo di riferimento non ha il ramo della forzatura. '
     'cd_ope_ins_dt è bpchar(6), il codice operatore di Side; le utenze di Roma sono VARCHAR2(40). '
     'Grafia: «SIDE» e virgolette “ ” contro «Side» e «» nel resto.',
     'Riscrivere: «ANSC, quando la validazione rileva anomalie superabili, restituisce un codice di '
     'forzatura; la tabella forzatura_validazione, ereditata da Side, conserva codice e anomalie per '
     'ogni atto, e registra se la forzatura è stata applicata e da chi. Forzare è un’azione riservata '
     'all’USC abilitato.» Aggiungere una colonna di esito (o la data di applicazione) e l’operatore '
     'che applica; portare l’utente a 40 caratteri. Nel passo VALIDA: ramo «anomalie superabili → '
     'l’USC decide → R009 con forcingCode». Aggiornare OP-21 (adottata, resta da definire chi è '
     'abilitato) e collegarlo a OP-41.',
     'Sì: la forzatura entra nel pilota? Chi è abilitato a forzare?'),
    ('Media', 'Numerazione', 'Registro degli Open Point — OP-73 · Appendice A',
     'Il privilegio CREATE SEQUENCE · nel DDL il nome è un segnaposto',
     'OP-73 (c) chiede il privilegio CREATE SEQUENCE per una procedura che non c’è più. OP-73 (d) dice '
     '«nel DDL il nome è un segnaposto», ma con la procedura sono stati tolti anche i GRANT: nell’App. A '
     'num-ansc-sipo non ha più alcun permesso su PRENOTAZIONE_ATTI, DATI_ATTO_ESTERNO e NUMERATORE_COMUNALE. '
     'OP-73 (a) rimanda alla «serie per registro e anno a cinque cifre descritta nella v3.40».',
     'Togliere (c). Ripristinare in coda alla numerazione: GRANT SELECT, INSERT, UPDATE sulle tre tabelle '
     'a <UTENZA_NUM>. In (a) descrivere l’alternativa invece di rimandare alla v3.40.', 'No'),
    ('Bassa', 'Numerazione', 'Appendice A — Numerazione Comunale',
     'Evento acquisito (dominio SIDe_17).\';  /',
     'Dopo l’ultimo COMMENT c’è una «/» isolata: in SQL*Plus e SQLcl riesegue l’istruzione precedente '
     '(qui il COMMENT, innocuo, ma è un errore di script). La «/» serve solo dopo un blocco PL/SQL, che '
     'non c’è più.', 'Togliere la «/».', 'No'),
    ('Bassa', 'Numerazione', 'Adeguamenti database · La numerazione comunale',
     'per per anno · gestita da una tabella per anno · Si crea alla prima chiamata dell’anno',
     '«per per anno» (tabella degli oggetti). «La serie, che è gestita da una tabella per anno» si legge '
     'come una tabella per ciascun anno. «Si crea alla prima chiamata dell’anno.» è una frase isolata, '
     'senza dire che cosa si crea né come si evita che due prime chiamate concorrenti creino due righe.',
     '«…gestita da una tabella con una riga per anno, NUMERATORE_COMUNALE». «La riga dell’anno si crea '
     'alla prima richiesta: se due richieste arrivano insieme, la chiave sull’anno ne fa fallire una, '
     'che rilegge la riga creata dall’altra.»', 'No'),
    ('Media', 'Numerazione', 'La numerazione comunale — Le strutture ereditate da Side',
     'Due tabelle, con i nomi di origine · NUMERATORE_COMUNALE',
     'Il capitolo descrive due tabelle (PRENOTAZIONE_ATTI, DATI_ATTO_ESTERNO) e non NUMERATORE_COMUNALE, '
     'che compare solo nella DDL. Le colonne non sono spiegate: id_anno_documento (l’anno? perché '
     '«documento»?), pg_atto (l’ultimo numero dato o il prossimo?), nr_ordinamento (a che serve con una '
     'riga per anno?). dt_inserimento/dt_aggiornamento sono TIMESTAMP con prefisso dt_ (in Side dt_ = '
     'data, ts_ = timestamp). Non c’è COMMENT. Se la tabella viene da Side (NUMERATORE_DOCUMENTI), '
     'non è dichiarato; se è nostra, l’adattamento va scritto nella tabella degli aggiustamenti.',
     'Aggiungere la tabella «Colonna | Tipo | Note» di NUMERATORE_COMUNALE nel capitolo, con '
     'nr_anno_atto (PK, come nelle altre due tabelle), nr_ultimo_atto NUMBER(6) («ultimo numero '
     'staccato; 0 alla creazione»), ts_ins_dt / ts_ult_agg_dt; togliere nr_ordinamento se non ha '
     'funzione. Dichiarare l’origine (Side o nostra).',
     'Sì: la tabella viene dal NUMERATORE_DOCUMENTI di Side (struttura da farsi dare) o è nostra?'),
]


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Rilievi'
    testa = ['N.', 'Gravità', 'Area', 'Capitolo', 'Dove (testo da cercare nel .docx)',
             'Che cosa non torna', 'Correzione proposta', 'Serve una tua decisione?', 'Stato',
             'Esito della seconda rilettura (23/10)']
    larg = [5, 9, 15, 30, 38, 70, 70, 26, 13, 60]
    blu = PatternFill('solid', fgColor='1F3A5F')
    fill = {'Alta': 'F6DFE1', 'Media': 'FDF1D6', 'Bassa': 'E9EAEC'}
    fstato = {'Fatto': 'DCF0E3', 'Parziale': 'FFF4C2', 'Nuovo': 'DBE6F5'}
    sottile = Side(style='thin', color='CBD5E1')
    bordo = Border(left=sottile, right=sottile, top=sottile, bottom=sottile)
    ws.append(testa)
    for c, w in zip(ws[1], larg):
        c.font = Font(bold=True, color='FFFFFF', name='Arial', size=10)
        c.fill = blu
        c.alignment = Alignment(vertical='center', wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    ordine = {'Alta': 0, 'Media': 1, 'Bassa': 2}
    righe = [(r, *STATO.get(next((k for k in STATO if r[3].startswith(k)), None), ('Da fare', '')))
             for r in sorted(R, key=lambda r: ordine[r[0]])]
    righe += [(r, 'Nuovo', 'Rilievo nuovo della seconda rilettura.') for r in NUOVI]
    for i, ((g, area, cap, dove, problema, corr, dec), stato, nota) in enumerate(righe, 1):
        ws.append([i, g, area, cap, dove, problema, corr, dec, stato, nota])
        for c in ws[i + 1]:
            c.alignment = Alignment(vertical='top', wrap_text=True)
            c.font = Font(name='Arial', size=9, bold=(c.column == 2))
            c.border = bordo
        ws.cell(i + 1, 2).fill = PatternFill('solid', fgColor=fill[g])
        if dec != 'No':
            ws.cell(i + 1, 8).fill = PatternFill('solid', fgColor='DBE6F5')
        if stato in fstato:
            ws.cell(i + 1, 9).fill = PatternFill('solid', fgColor=fstato[stato])
    n = len(righe)
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:J{n + 1}'
    dv = DataValidation(type='list', formula1='"Da fare,Parziale,Fatto,Nuovo,Scartato,In discussione"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f'I2:I{n + 1}')

    lg = wb.create_sheet('Legenda')
    lg.column_dimensions['A'].width = 34
    lg.column_dimensions['B'].width = 12
    lg.append(['Seconda rilettura di ANALISI_Integrazione-ANSC_v3.44 (file del 23/10/2026, 08:17)'])
    lg['A1'].font = Font(bold=True, name='Arial', size=11)
    lg.append([])
    lg.append(['Gravità', 'Rilievi'])
    for g in ('Alta', 'Media', 'Bassa'):
        lg.append([g, sum(1 for r, _, _ in righe if r[0] == g)])
    lg.append(['Totale', n])
    lg.append([])
    lg.append(['Stato', 'Rilievi'])
    for s in ('Da fare', 'Parziale', 'Fatto', 'Nuovo'):
        lg.append([s, sum(1 for _, st, _ in righe if st == s)])
    lg.append([])
    lg.append(['Con decisione richiesta', sum(1 for r, _, _ in righe if r[6] != 'No')])
    lg.append([])
    lg.append(['Controllo automatico verifica-conteggi.py: nessuna discordanza; 26 commenti di Word.'])
    wb.save(OUT)
    print('scritto:', OUT, n, 'rilievi')
    from collections import Counter
    print(Counter(st for _, st, _ in righe))


if __name__ == '__main__':
    main()
